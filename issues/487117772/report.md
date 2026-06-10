# UAF in blink::PendingInvalidations

| Field | Value |
|-------|-------|
| **Issue ID** | [487117772](https://issues.chromium.org/issues/487117772) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2026-02-24 |
| **Bounty** | $10,000.00 |

## Description

### Summary

`PendingInvalidations::ScheduleInvalidationSetsForNode()` takes a `NodeInvalidationSets&` reference to a value stored inside `PendingInvalidations::pending_invalidation_map_` (a `HeapHashMap`) and then calls `PossiblyScheduleNthPseudoInvalidations(node)` while that reference is still live. `PossiblyScheduleNthPseudoInvalidations()` can synchronously re-enter invalidation scheduling on the parent (via `StyleEngine::ScheduleNthPseudoInvalidations(parent)`), which can insert into the same `HeapHashMap` and trigger `Rehash()`. That rehash frees/poisons the old hash table backing, invalidating the outer reference. Therefore, when the outer frame resumes, it access the stale `NodeInvalidationSets` and crash with UAF.

#### Details

[`PendingInvalidations::ScheduleInvalidationSetsForNode`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/invalidation/pending_invalidations.cc;l=21) keeps a reference into `pending_invalidation_map_` while calling out to a helper that can re-enter scheduling:

```
NodeInvalidationSets& pending_invalidations = EnsurePendingInvalidations(node);
for (auto& invalidation_set : invalidation_lists.siblings) {
  if (pending_invalidations.Siblings().Contains(invalidation_set)) {
    continue;
  }
  if (invalidation_set->InvalidatesNth()) {
    PossiblyScheduleNthPseudoInvalidations(node);
  }
  pending_invalidations.Siblings().push_back(invalidation_set);
}

```

The callout is synchronous. In [`PossiblyScheduleNthPseudoInvalidations`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/style_engine.cc;l=1459), when the parent has positional-rule flags set, it immediately schedules nth invalidations on the parent:

```
if ((parent->ChildrenAffectedByForwardPositionalRules() && node.nextSibling()) ||
    (parent->ChildrenAffectedByBackwardPositionalRules() &&
     node.previousSibling())) {
  node.GetDocument().GetStyleEngine().ScheduleNthPseudoInvalidations(*parent);
}

```

`StyleEngine::ScheduleNthPseudoInvalidations()` then re-enters the same `PendingInvalidations` instance ([source](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/style_engine.cc;l=2111)):

```
pending_invalidations_.ScheduleInvalidationSetsForNode(invalidation_lists,
                                                       nth_parent);

```

The re-entrant call can insert into the same `HeapHashMap` via [`PendingInvalidations::EnsurePendingInvalidations`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/invalidation/pending_invalidations.cc;l=213):

```
PendingInvalidationMap::AddResult add_result =
    pending_invalidation_map_.insert(&node, NodeInvalidationSets());
return add_result.stored_value->value;

```

When the insertion crosses the hash table's expansion threshold and `MustRehashInPlace()` is true, [`HashTable::Expand`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/wtf/hash_table.h;l=1619) can do a same-size rehash:

```
// ...
else if (MustRehashInPlace()) {
  new_size = table_size_;
} else {
  new_size = table_size_ * 2;
}
return Rehash(new_size, entry);

```

When returned to the outer `ScheduleInvalidationSetsForNode()` frame, it continues operating on the stale `pending_invalidations` reference. The next `Vector` access through that stale/invalid value (`Vector::size()` in `wtf/vector.h:1348`) and triggers the UAF.

### Bisection

This issue is introduced by the commit `c98887131608ef87756a77a3493aac8b6b8ec02e`, hence it affects all stable versions.

### Reproduction

Download the chrome from <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1588577.zip>

Run the following commandline:

```
./chrome --no-sandbox poc.html

```

You would get the ASAN crash with UAP in `asan.txt`.

### Suggested Fix

Avoid holding references/pointers into `pending_invalidation_map_` across any call that can re-enter `PendingInvalidations` and mutate/rehash the same map.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 32.0 KB)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)

## Timeline

### li...@chromium.org (2026-02-24)

@an...@chromium.org - do you mind taking a look or rerouting as necessary?

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  main  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7606599>

Describe a vector of segments as "segments", not "tokens"

---


Expand for full commit details
```
     
    The specification uses the term "tokens" to refer to a sequence 
    of V8CSSUnparsedSegment objects, and CSSUnparsedValue has adopted 
    this terminology. While it is usually a good idea for Blink 
    to mirror the language used in specifications, "tokens" is very 
    confusing here, since it always means CSSParserTokens in every other 
    place in the style code. 
     
    Bug: 487117772 
    Change-Id: I2dc132c4e618e398e1f8bdabc03a8d2ab6c118e7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7606599 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Reviewed-by: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1590040}

```

---

Files:

- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc`
- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.h`

---

Hash: [45c5a70d984d630370e9ee15265f88381251a55a](https://chromiumdash.appspot.com/commit/45c5a70d984d630370e9ee15265f88381251a55a)  

Date: Wed Feb 25 11:24:19 2026


---

### an...@chromium.org (2026-02-25)

Oops, that CL is not related to this bug. I linked it here accidentally.

### ch...@google.com (2026-02-25)

Setting milestone because of s0/s1 severity.

### an...@chromium.org (2026-03-03)

Actually, sesse@ can have this one, since it's caused by nth-pseudo invalidation.

### se...@chromium.org (2026-03-03)

I'll have a look.

The bisection cannot be right; c98887131608ef87756a77a3493aac8b6b8ec02e is an unrelated roll.

### he...@gmail.com (2026-03-03)

Ops, there's typo in the original bisection, I paste the wrong commit hash there. I think the correct bisection should be <https://chromium-review.googlesource.com/c/chromium/src/+/4152470> which introduce the implementation of `invalidation` and the `PossiblyScheduleNthPseudoInvalidations(node);`

Many thanks!

### se...@chromium.org (2026-03-03)

Yes, I think this is a likely place for this bug.

### se...@chromium.org (2026-03-03)

This seems like a genuine UAF to me.

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7628401>

Fix use-after-free in PendingInvalidationMap.

---


Expand for full commit details
```
     
    When processing NodeInvalidationSets, we hold on to a reference to it 
    even as we modify the PendingInvalidationMap it is part of 
    (through a recursive call to schedule other nth-child invalidation sets). 
    PendingInvalidationMap is a HeapHashMap, which is not node-based, 
    and thus, insertions may invalidate pointers to the buckets, causing 
    a use-after-free. 
     
    We could have refreshed the pointer after operations that could modify 
    the map, but it seems much safer to just store pointers in the map 
    instead, at the cost of slightly more allocations. 
     
    The test is fairly complicated and depends on details of when HashMap 
    chooses to rehash, so it was seen as not useful to keep permanently 
    in the test repository and thus not included. 
     
    Fixed: 487117772 
    Change-Id: I0ace920e5497dd1f3c6c1ae61fc8aa551eb334c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7628401 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1593196}

```

---

Files:

- M `third_party/blink/renderer/core/css/invalidation/pending_invalidations.cc`
- M `third_party/blink/renderer/core/css/invalidation/pending_invalidations.h`
- M `third_party/blink/renderer/core/css/invalidation/style_invalidator.cc`

---

Hash: [b28cbf5d52921a913f3dd1f5416358fe33b54ab9](https://chromiumdash.appspot.com/commit/b28cbf5d52921a913f3dd1f5416358fe33b54ab9)  

Date: Tue Mar 3 14:38:58 2026


---

### ch...@google.com (2026-03-03)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-04)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1593196) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1593196) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1593196) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-04)

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

### ch...@google.com (2026-03-04)

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

### ch...@google.com (2026-03-04)

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

### dr...@chromium.org (2026-03-07)

No crashes in Canary, approved to merge to M146. We don't plan more releases to M144 or M145, so removing those merges.

### ch...@google.com (2026-03-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7666025>

Fix use-after-free in PendingInvalidationMap.

---


Expand for full commit details
```
     
    When processing NodeInvalidationSets, we hold on to a reference to it 
    even as we modify the PendingInvalidationMap it is part of 
    (through a recursive call to schedule other nth-child invalidation sets). 
    PendingInvalidationMap is a HeapHashMap, which is not node-based, 
    and thus, insertions may invalidate pointers to the buckets, causing 
    a use-after-free. 
     
    We could have refreshed the pointer after operations that could modify 
    the map, but it seems much safer to just store pointers in the map 
    instead, at the cost of slightly more allocations. 
     
    The test is fairly complicated and depends on details of when HashMap 
    chooses to rehash, so it was seen as not useful to keep permanently 
    in the test repository and thus not included. 
     
    (cherry picked from commit b28cbf5d52921a913f3dd1f5416358fe33b54ab9) 
     
    Fixed: 487117772 
    Change-Id: I0ace920e5497dd1f3c6c1ae61fc8aa551eb334c0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7628401 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1593196} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666025 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2649} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/core/css/invalidation/pending_invalidations.cc`
- M `third_party/blink/renderer/core/css/invalidation/pending_invalidations.h`
- M `third_party/blink/renderer/core/css/invalidation/style_invalidator.cc`

---

Hash: [298c143f68c0f3581e78f45523e02c36dd28414d](https://chromiumdash.appspot.com/commit/298c143f68c0f3581e78f45523e02c36dd28414d)  

Date: Mon Mar 16 11:28:50 2026


---

### pe...@google.com (2026-03-16)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-03-18)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7668834>
2. Low - no conflicts
3. M146
4. Yes.

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High Quality. Renderer RCE / memory corruption in a sandboxed process


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

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7668834>

[M138-LTS] Fix use-after-free in PendingInvalidationMap.

---


Expand for full commit details
```
     
    When processing NodeInvalidationSets, we hold on to a reference to it 
    even as we modify the PendingInvalidationMap it is part of 
    (through a recursive call to schedule other nth-child invalidation sets). 
    PendingInvalidationMap is a HeapHashMap, which is not node-based, 
    and thus, insertions may invalidate pointers to the buckets, causing 
    a use-after-free. 
     
    We could have refreshed the pointer after operations that could modify 
    the map, but it seems much safer to just store pointers in the map 
    instead, at the cost of slightly more allocations. 
     
    The test is fairly complicated and depends on details of when HashMap 
    chooses to rehash, so it was seen as not useful to keep permanently 
    in the test repository and thus not included. 
     
    Fixed: 487117772 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7628401 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1593196} 
    (cherry picked from commit b28cbf5d52921a913f3dd1f5416358fe33b54ab9) 
     
    Change-Id: I163fdb691c75f7b68ab405fe6e7692f2f96a25f2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7668834 
    Reviewed-by: Steinar H Gunderson <sesse@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3530} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/core/css/invalidation/pending_invalidations.cc`
- M `third_party/blink/renderer/core/css/invalidation/pending_invalidations.h`
- M `third_party/blink/renderer/core/css/invalidation/style_invalidator.cc`

---

Hash: [7c1cd0cd41852245a23590bb240120b07e676cad](https://chromiumdash.appspot.com/commit/7c1cd0cd41852245a23590bb240120b07e676cad)  

Date: Wed Apr 8 14:32:54 2026


---

### pe...@google.com (2026-05-07)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-05-07)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7830877>
2. Low. No conflicts
3. 138 and 146
4. Yes.

### dx...@google.com (2026-05-19)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7830877>

[M144-LTS] Fix use-after-free in PendingInvalidationMap.

---


Expand for full commit details
```
     
    When processing NodeInvalidationSets, we hold on to a reference to it 
    even as we modify the PendingInvalidationMap it is part of 
    (through a recursive call to schedule other nth-child invalidation sets). 
    PendingInvalidationMap is a HeapHashMap, which is not node-based, 
    and thus, insertions may invalidate pointers to the buckets, causing 
    a use-after-free. 
     
    We could have refreshed the pointer after operations that could modify 
    the map, but it seems much safer to just store pointers in the map 
    instead, at the cost of slightly more allocations. 
     
    The test is fairly complicated and depends on details of when HashMap 
    chooses to rehash, so it was seen as not useful to keep permanently 
    in the test repository and thus not included. 
     
    Fixed: 487117772 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7628401 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1593196} 
    (cherry picked from commit b28cbf5d52921a913f3dd1f5416358fe33b54ab9) 
     
    Change-Id: I6c02995cc95ad87a6c2e7593c7ac5dfab158b1e5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7830877 
    Reviewed-by: Steinar H Gunderson <sesse@chromium.org> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Owners-Override: Michael Ershov <miersh@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4874} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/core/css/invalidation/pending_invalidations.cc`
- M `third_party/blink/renderer/core/css/invalidation/pending_invalidations.h`
- M `third_party/blink/renderer/core/css/invalidation/style_invalidator.cc`

---

Hash: [456c5402af50b490cd105114293420b7b889e92f](https://chromiumdash.appspot.com/commit/456c5402af50b490cd105114293420b7b889e92f)  

Date: Tue May 19 22:37:44 2026


---

### ch...@google.com (2026-06-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487117772)*
