# UAF in blink RuleMap

| Field | Value |
|-------|-------|
| **Issue ID** | [488188166](https://issues.chromium.org/issues/488188166) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | $3,000.00 |

## Description

### Summary

When Blink builds a “diff ruleset” during stylesheet mutation, [`RuleMap::AddFilteredRulesFromOtherSet`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/rule_set.cc;l=1592) copies selected `RuleData` entries into a new `RuleMap` but ignores the boolean result of `RuleMap::Add()`. Under deliberate `AtomicString::Hash()` collisions (documented as a supported failure mode of [`RobinHoodMap`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/robin_hood_map.h;l=33)), `RuleMap::Add()` can return `false`; the copy path still treats `backing.back()` as the newly-added element and relocates bloom-hash metadata on the wrong `RuleData`. This desynchronizes `RuleData::bloom_hash_pos_` from the source ruleset backing and leads to an OOB access in [`RuleData::MovedToDifferentRuleSet`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/rule_set.cc;l=224) when copying bloom-hash slices.

### Details

The intended behavior is that adding a key to a `RuleMap` either succeeds (appending a new `RuleData` to `backing`) or, if insertion fails due to collision pressure, a safe fallback is taken. The normal RuleSet build path already anticipates this: [`RuleSet::AddToBucket`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/rule_set.cc;l=237) checks `map.Add(...)` and, on failure, places a de-bucketed copy of the rule into `universal_rules_` to preserve correctness.

In [`RuleSet::AddToBucket`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/rule_set.cc;l=237), insertion failure is explicitly treated as an adversarial collision case and handled without touching unrelated `RuleData`:

```
if (!map.Add(key, rule_data)) {
  RuleData rule_data_copy = rule_data;
  UnmarkAsCoveredByBucketing(rule_data_copy.MutableSelector());
  AddToBucket(universal_rules_, rule_data_copy);
  return;
}

```

However, the diff ruleset path (used by [`RuleSetDiff::CreateDiffRuleset`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/rule_set_diff.cc;l=50)) does not apply this pattern. In `RuleMap::AddFilteredRulesFromOtherSet`, the result of `Add()` is ignored and the code unconditionally assumes that `backing.back()` is the `RuleData` that was just appended:

In [`RuleMap::AddFilteredRulesFromOtherSet`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/rule_set.cc;l=1592), the copy loop ignores the return value from `Add()` and immediately uses `backing.back()`:

```
if (only_include.Contains(const_cast<StyleRule*>(rule_data.Rule()))) {
  Add(key, rule_data);
  new_rule_set.NewlyAddedFromDifferentRuleSet(
      rule_data, scope_seeker.Seek(rule_data.GetPosition()),
      old_rule_set, backing.back());
}

```

`RuleMap::Add()` can return `false` when the underlying Robin Hood table cannot accommodate another key with the same 24-bit `AtomicString::Hash()` (bounded probe length). This failure is explicit in the implementation:

In [`RuleMap::Add`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/rule_set.cc;l=1481):

```
RobinHoodMap<AtomicString, Extent>::Bucket* bucket = buckets.Insert(key);
if (bucket == nullptr) {
  return false;
}

```

When `Add()` fails in the diff-copy loop, `backing` is not appended, but `backing.back()` still returns the **previous** `RuleData`. `NewlyAddedFromDifferentRuleSet()` then calls `RuleData::MovedToDifferentRuleSet()` on that wrong element, which performs an unchecked copy out of the *source* ruleset’s bloom backing using the `bloom_hash_pos_` stored in the `RuleData`:

In [`RuleData::MovedToDifferentRuleSet`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/rule_set.cc;l=224), `bloom_hash_pos_` is used as an offset into `old_backing` without validating that it still refers to that backing vector:

```
unsigned new_pos = new_backing.size();
new_backing.insert(new_backing.size(),
                   old_backing.data() + bloom_hash_pos_,
                   bloom_hash_size_);
bloom_hash_pos_ = new_pos;

```

Because the wrong `RuleData` has typically already been relocated into the diff ruleset’s `bloom_hash_backing_`, its `bloom_hash_pos_` now refers to the diff backing. Reusing that value as an offset into the *source* ruleset’s `old_backing` produces an out-of-bounds source pointer passed into `Vector<uint16_t>::insert()`, leading to the OOB.

### Bisection

This issue is introduced by the commit `c3afc7e99450e707a4df6ef81b86b71d7def8c09`, which introduce the incorrect implementation for the `RuleMap::Add()` calls.

### Reproduction

Download the chrome from `https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1591355.zip`

Run command:

```
./chrome --no-sandbox poc.html

```

The ASAN crash is shown in the `asan.txt`

### Suggested Fix

In `RuleMap::AddFilteredRulesFromOtherSet`, handle `RuleMap::Add()` failure explicitly.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 43.9 KB)
- [poc.html](attachments/poc.html) (text/html, 1.3 KB)
- [uaf_asan.txt](attachments/uaf_asan.txt) (text/plain, 35.0 KB)
- [uaf_poc.html](attachments/uaf_poc.html) (text/html, 1.5 KB)

## Timeline

### he...@gmail.com (2026-02-27)

We can both trigger the OOB and the UAF crash in blink RuleMap by using different triggering method. If we delete the rule before match, we can get UAF.

### he...@gmail.com (2026-02-27)

Attach the poc & asan trace which triggers UAF on asan-linux-release-1591355 chrome.

### li...@chromium.org (2026-02-27)

@se...@chromium.org do you mind taking a look or rerouting as necessary?

### ch...@google.com (2026-02-28)

Setting milestone because of s0/s1 severity.

### se...@chromium.org (2026-03-02)

Thanks for the report. This looks like a legitimate issue to me, I'll have a look.

### se...@chromium.org (2026-03-02)

To me, this looks like an out-of-bounds read, not a use-after-free. It should be fixed nevertheless, of course.

### dx...@google.com (2026-03-02)

Project: chromium/src  

Branch:  main  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7623313>

Fix out-of-bounds read in diff rulesets.

---


Expand for full commit details
```
     
    When merging diff rulesets, if Add() failed (due to a deliberate hash 
    collision, causing RobinHoodMap to refuse the insertion), we would 
    call NewlyAddedFromDifferentRuleSet() twice on the same RuleData, 
    causing us to potentially read data past the end of the Bloom filter 
    backing. 
     
    In addition to actually fixing the issue, we mark Add() as [[nodiscard]] 
    so that it cannot happen again, and we also spanify 
    MovedToDifferentRuleSet() so that a similar error would cause a CHECK 
    failure instead of reading out-of-bounds. 
     
    Fixed: 488188166 
    Change-Id: I38974eaa150c7c1e32482febea632b8371731aae 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623313 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1592383}

```

---

Files:

- M `third_party/blink/renderer/core/css/rule_set.cc`
- M `third_party/blink/renderer/core/css/rule_set.h`
- A `third_party/blink/web_tests/external/wpt/css/selectors/hash-collision-cssom.html`

---

Hash: [2bfa338165eef94983c6cd35e281450d994d2215](https://chromiumdash.appspot.com/commit/2bfa338165eef94983c6cd35e281450d994d2215)  

Date: Mon Mar 2 13:05:56 2026


---

### ch...@google.com (2026-03-03)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1592383) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1592383) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1592383) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-03)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-03)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-03)

Merge review required: M144 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-03-04)

No crashes in Canary, but we don't plan any more M144 or M145 releases. So approved for M146 only.

### ch...@google.com (2026-03-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-03-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7665929>

Fix out-of-bounds read in diff rulesets.

---


Expand for full commit details
```
     
    When merging diff rulesets, if Add() failed (due to a deliberate hash 
    collision, causing RobinHoodMap to refuse the insertion), we would 
    call NewlyAddedFromDifferentRuleSet() twice on the same RuleData, 
    causing us to potentially read data past the end of the Bloom filter 
    backing. 
     
    In addition to actually fixing the issue, we mark Add() as [[nodiscard]] 
    so that it cannot happen again, and we also spanify 
    MovedToDifferentRuleSet() so that a similar error would cause a CHECK 
    failure instead of reading out-of-bounds. 
     
    (cherry picked from commit 2bfa338165eef94983c6cd35e281450d994d2215) 
     
    Fixed: 488188166 
    Change-Id: I38974eaa150c7c1e32482febea632b8371731aae 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623313 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1592383} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665929 
    Auto-Submit: Steinar H Gunderson <sesse@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2646} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/core/css/rule_set.cc`
- M `third_party/blink/renderer/core/css/rule_set.h`
- A `third_party/blink/web_tests/external/wpt/css/selectors/hash-collision-cssom.html`

---

Hash: [ce7f30c93bba490b0e6586ac92c519934ad460bc](https://chromiumdash.appspot.com/commit/ce7f30c93bba490b0e6586ac92c519934ad460bc)  

Date: Mon Mar 16 10:53:51 2026


---

### pe...@google.com (2026-03-16)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-03-30)

1. one CL: <https://chromium-review.git.corp.google.com/c/chromium/src/+/7682152>
2. Medium - Two conflicts found when merging (as detailed in the CL description).
3. 146
4. Yes. Specially because this issue was introduced in commit c3afc7e9 (from 2023).

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline with bisect. User information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### an...@google.com (2026-03-31)

Merge approved for LTS-138

### dx...@google.com (2026-04-08)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7682152>

[M138-LTS] Fix out-of-bounds read in diff rulesets.

---


Expand for full commit details
```
     
    M138 merge issues: 
      third_party/blink/renderer/core/css/rule_set.cc 
        In MovedToDifferentRuleSet(), UNSAFE_TODO was still being used 
        instead of UNSAFE_BUFFERS (see https://crrev.com/c/7368039). Also, 
        in AddFilteredRulesFromOtherSet(), IncludeRule() was being used 
        instead of simply only_include.Contains (see 
        https://crrev.com/c/7013292). 
     
    When merging diff rulesets, if Add() failed (due to a deliberate hash 
    collision, causing RobinHoodMap to refuse the insertion), we would call NewlyAddedFromDifferentRuleSet() twice on the same RuleData, causing us to potentially read data past the end of the Bloom filter backing. 
     
    In addition to actually fixing the issue, we mark Add() as [[nodiscard]] so that it cannot happen again, and we also spanify 
    MovedToDifferentRuleSet() so that a similar error would cause a CHECK 
    failure instead of reading out-of-bounds. 
     
    Fixed: 488188166 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623313 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1592383} 
     
    (cherry picked from commit 2bfa338165eef94983c6cd35e281450d994d2215) 
     
    Change-Id: Ice2e81e8f54d4af743b7a054151d17bece17f078 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7682152 
    Reviewed-by: Steinar H Gunderson <sesse@chromium.org> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3529} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/core/css/rule_set.cc`
- M `third_party/blink/renderer/core/css/rule_set.h`
- A `third_party/blink/web_tests/external/wpt/css/selectors/hash-collision-cssom.html`

---

Hash: [348705c5d01e8ca32e26c7768782a80c8eb1e6f8](https://chromiumdash.appspot.com/commit/348705c5d01e8ca32e26c7768782a80c8eb1e6f8)  

Date: Wed Apr 8 14:25:25 2026


---

### pe...@google.com (2026-05-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-08)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7833129>
2. Low. There was one single conflict found when merging (as detailed in the CL description).
3. 138 and 146
4. Yes

### dx...@google.com (2026-05-19)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7833129>

[M144-LTS] Fix out-of-bounds read in diff rulesets.

---


Expand for full commit details
```
     
    M144 merge issues: 
      third_party/blink/renderer/core/css/rule_set.cc 
        In MovedToDifferentRuleSet(), UNSAFE_TODO was still being used 
        instead of UNSAFE_BUFFERS (see https://crrev.com/c/7368039). 
     
    When merging diff rulesets, if Add() failed (due to a deliberate hash 
    collision, causing RobinHoodMap to refuse the insertion), we would 
    call NewlyAddedFromDifferentRuleSet() twice on the same RuleData, 
    causing us to potentially read data past the end of the Bloom filter 
    backing. 
     
    In addition to actually fixing the issue, we mark Add() as [[nodiscard]] 
    so that it cannot happen again, and we also spanify 
    MovedToDifferentRuleSet() so that a similar error would cause a CHECK 
    failure instead of reading out-of-bounds. 
     
    Fixed: 488188166 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7623313 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1592383} 
    (cherry picked from commit 2bfa338165eef94983c6cd35e281450d994d2215) 
     
    Change-Id: I44daa66f87fd9ecbdfb9ec7c492e3020414bae16 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7833129 
    Owners-Override: Michael Ershov <miersh@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Reviewed-by: Steinar H Gunderson <sesse@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4873} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/core/css/rule_set.cc`
- M `third_party/blink/renderer/core/css/rule_set.h`
- A `third_party/blink/web_tests/external/wpt/css/selectors/hash-collision-cssom.html`

---

Hash: [285461590e8c20d388eef98a852f57a6139bb5b7](https://chromiumdash.appspot.com/commit/285461590e8c20d388eef98a852f57a6139bb5b7)  

Date: Tue May 19 22:19:32 2026


---

### ch...@google.com (2026-06-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488188166)*
