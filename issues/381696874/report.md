# Arbitrary Wasm type confusion due to improper fix of b/380397544

| Field | Value |
|-------|-------|
| **Issue ID** | [381696874](https://issues.chromium.org/issues/381696874) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2024-12-02 |
| **Bounty** | $55,000.00 |

## Description

### VULNERABILITY DETAILS

A bit unfortunate that even after a series of patches canonicalization is still broken, we really need a proactive approach rather than reactive bug discovery & patches.

#### Summary

Arbitrary Wasm type confusion due to improper fix of [b/380397544](https://issues.chromium.org/issues/380397544) (which attempts to fix a broken patch for [b/379009132](https://issues.chromium.org/issues/379009132), which in turn attempts to fix a broken patch for [b/371565065](https://issues.chromium.org/issues/371565065) + [b/354408144](https://issues.chromium.org/issues/354408144)). `HeapType` checks are missing for generic Wasm heap types at [`CanonicalEquality::EqualValueType()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/canonical-types.h;drc=592f1915dbe12bf8d6abf680e2ba029e23eeed4b;l=303), allowing type confusion between arbitrary Wasm types.

#### Details

I've pointed out in [b/380397544](https://issues.chromium.org/issues/380397544) that after <https://crrev.com/c/6035175> v8 does not distinguish between (relative) recursion group based index vs. (absolute) canonical index, which leads to different recursion group to be mistakenly canonicalized into the same index and thus lead to arbitrary type confusion between Wasm types. <https://crrev.com/c/6048961> attempts to fix this by checking for relative types on type index comparison. Equality checks for `CanonicalValueType`s go through the following code at [`CanonicalEquality::EqualValueType()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/canonical-types.h;drc=592f1915dbe12bf8d6abf680e2ba029e23eeed4b;l=303):

```
    bool EqualValueType(CanonicalValueType type1,
                        CanonicalValueType type2) const {
      if (type1.kind() != type2.kind()) return false;
      if (type1.has_index() &&
          !EqualTypeIndex(type1.ref_index(), type2.ref_index())) {
        return false;
      }
      return true;
    }

```

We see that if `!type1.has_index()`, that is, if the left-hand side of the equality comparison has a generic heap type, then the comparison always returns true no matter what the heap type of `type2` is. This results in the equality comparator of `Canonical(Singleton)Group` to consider different reference types to be the same under the aformentioned case and thus may lead to arbitrary Wasm type confusion again.

However, this issue is not immediately evident as we use `std::unordered_set<Canonical(Singleton)Group>` to find pre-existing canonicalization results. This uses `CanonicalHashing` as a hashing function for the hashmap. Thus, to trigger this issue we must find two different recursion group that is considered equal by `CanonicalEquality`, but which **at the same time also has a hash collision** when hashed via `CanonicalHashing`.

`CanonicalHashing` uses `base::Hasher` which is based on MurmurHash64A and thus returns a 64bit hash value. **Birthday attack allows us to find a collision in ~50% chance with 2^32 samples** which is very feasible (in minutes, if not seconds). By precomputing offline the hash values for struct types that either has `ref null any` or `ref null none` as its fields and iterating this selection for >32 fields we can easily create >2^32 different inputs that are all considerered equal by `CanonicalEquality`, but which has random-ish hash values in which we are likely to find at least a single duplicate hash value. By using such precomputed colliding struct types we can canonicalize two different struct types into the same canonical index and cause arbitrary Wasm type confusion.

The attached PoC/exploit has a precomputed hash-colliding struct type that uses either `ref null any` or `ref null none` for its 40 field types. It tries two colliding pairs, one that works before <https://crrev.com/c/6055121> and one that works after that as the patch affects hashing results.

#### Bisect

Bug introduced by <https://crrev.com/c/6048961> in M133 that attempts to fix [b/380397544](https://issues.chromium.org/issues/380397544) by accounting for relative type indices. Note that the commit is already backported to [M132](https://crrev.com/c/6054730) and [M131](https://crrev.com/c/6054989).

### VERSION

- M133: <https://crrev.com/c/6048961>
- M132: <https://crrev.com/c/6054730>
- M131: <https://crrev.com/c/6054989>

Chrome Version: 133.0.6862.0 ~ latest / M131 head / M132 head  

Operating System: All

### REPRODUCTION CASE

Attached as `poc.js` which exploits the hash collision + type confusion to obtain in-sandbox exploit primitives, and then crashes on arbitrary caged write attempt.

Also attached is yet another full exploit `exp.html` that pops `calc` on Windows x64 Chrome, tested against Canary 133.0.6871.0.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Renderer  

Crash State: Crashes on arbitrary caged write attempt from JIT-compiled Wasm function (on d8, `poc.js`), arbitrary code execution (on Chrome, `exp.html`)

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n) of CMU CyLab

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 76.5 KB)
- [exp.html](attachments/exp.html) (text/html, 86.0 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-12-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5907880888696832.

### ti...@chromium.org (2024-12-02)

[Security shepherd] CCing current v8 shepherd. Provisionally triaging, please adjust as necessary.

### cl...@chromium.org (2024-12-02)

Thanks again for the great writeup!

The bug in this case is that the code (and its author) assumed that `type1.kind() == type2.kind()` implies `type1.has_index() == type2.has_index()`.

As the fix is pretty straight-forward, I'll upload it right away, but then I'll also spend some time to finally write a fuzzer (or FuzzTest, let's see) for type canonicalization. It's really bad that we had three bugs on top of each other without any fuzzers to find them.

Note though that none of the previous fixes was "wrong" in itself. It was just that every fix had another missed cornercase. And by our policy to not upload regression tests with in-the-wild bugs we also didn't give our general JS fuzzers a chance to find the bugs. But the chance would probably also have been low to find them in a general JS fuzzer.

### 24...@project.gserviceaccount.com (2024-12-02)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-12-02)

Detailed Report: https://clusterfuzz.com/testcase?key=5907880888696832

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x79b500000007
Crash State:
  Builtins_JSToWasmWrapperAsm
  Builtins_JSToWasmWrapper
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=97470:97471

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5907880888696832

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ap...@google.com (2024-12-02)

Project: v8/v8  

Branch: main  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6063041>

[wasm] Fix equality of canonical value types

---


Expand for full commit details
```
[wasm] Fix equality of canonical value types 
 
We were incorrectly assuming that the value kind implies indexedness. 
Fix this, and also compare generic (non-indexes) ref types. 
 
R=jkummerow@chromium.org 
 
Fixed: 381696874 
Change-Id: Ie74ea8cb20d14f1b8d7d6a09701bc45cf91a913e 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6063041 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97503}

```

---

Files:

- M `src/wasm/canonical-types.h`

---

Hash: a4d354fa54ba3e6a0f061c6b959be408ead5db95  

Date:  Mon Dec 02 15:42:19 2024


---

### pe...@google.com (2024-12-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-12-02)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-12-02)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M130. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M131. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### se...@gmail.com (2024-12-02)

Re #4: Great that we now have a check for `type1.has_index() == type2.has_index()` too, it seems that otherwise we might have considered generic heaptype references as relative references inside recursion groups that "transiently" cross the `kV8MaxWasmTypes` boundary while canonicalizing without ever triggering the `CHECK_LT()` at `CanonicalValueType::FromIndex()`. Note that this `CHECK_LT()` is currently a huge load-bearing check stopping transient `kV8MaxWasmTypes` overflows at canonicalization from being exploitable which might be worth explicitly documenting.

### 24...@project.gserviceaccount.com (2024-12-03)

ClusterFuzz testcase 5907880888696832 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=97502:97503

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### cl...@chromium.org (2024-12-03)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://crrev.com/c/6063041>

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes, since 133.0.6874.0

3. Does this fix pose any potential non-verifiable stability risks?

Not more than any other fix.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

No.

6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pe...@google.com (2024-12-03)

Merge review required: M132 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), alonbajayo (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-12-03)

Merge review required: M131 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-12-03)

Merge review required: M130 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### cl...@chromium.org (2024-12-03)

See [comment #13](https://issues.chromium.org/issues/381696874#comment13)

### am...@chromium.org (2024-12-04)

merges approved for <https://crrev.com/c/6063041>, please merge by EOD tomorrow, Thursday, 5 December so this fix can be included in next week's updates

### sp...@google.com (2024-12-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
high-quality report of demonstrated RCE in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-05)

Thank you for finding another variant here, Seunghyun! Appreciate your swift efforts and thorough reporting once again.

### cl...@chromium.org (2024-12-05)

This does not affect 130, actually, just as <https://crbug.com/379009132> and <https://crbug.com/380397544>. Updating labels.

### ap...@google.com (2024-12-05)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6074451>

Merged: [wasm] Fix equality of canonical value types

---


Expand for full commit details
```
Merged: [wasm] Fix equality of canonical value types 
 
We were incorrectly assuming that the value kind implies indexedness. 
Fix this, and also compare generic (non-indexes) ref types. 
 
R=jkummerow@chromium.org 
 
Bug: 381696874 
(cherry picked from commit a4d354fa54ba3e6a0f061c6b959be408ead5db95) 
 
Change-Id: I9a4478f980a659f1667b0fc1759ee310f72c70ba 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6074451 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.2@{#30} 
Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/wasm/canonical-types.h`

---

Hash: aad03217f482b90f34ae559ca3492295f56e648e  

Date:  Thu Dec 05 10:59:01 2024


---

### ap...@google.com (2024-12-05)

Project: v8/v8  

Branch: refs/branch-heads/13.1  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6072809>

Merged: [wasm] Fix equality of canonical value types

---


Expand for full commit details
```
Merged: [wasm] Fix equality of canonical value types 
 
We were incorrectly assuming that the value kind implies indexedness. 
Fix this, and also compare generic (non-indexes) ref types. 
 
R=jkummerow@chromium.org 
 
Bug: 381696874 
(cherry picked from commit a4d354fa54ba3e6a0f061c6b959be408ead5db95) 
 
Change-Id: Ifede1a3dea898967a930528f1e9fc5eefcfa4c8b 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6072809 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.1@{#30} 
Cr-Branched-From: 7998da66cb2883ef9734743857713b1194212d9a-refs/heads/13.1.201@{#1} 
Cr-Branched-From: 5e9af2a913539cf67091def99b62f49afece6f56-refs/heads/main@{#96554}

```

---

Files:

- M `src/wasm/canonical-types.h`

---

Hash: 77b731808358c705674ee5a24fbcd186bdb845d3  

Date:  Thu Dec 05 11:34:26 2024


---

### pe...@google.com (2024-12-05)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2024-12-05)

Labeling as LTS-NotApplicable-126 because the suspected CL[1] were only merged to M131 and M132, not merged to M126. So we don't need to merge back the fix[2] to M126 LTS.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/6048961
[2] https://chromium-review.googlesource.com/c/v8/v8/+/6063041

### se...@gmail.com (2024-12-05)

Re [comment#19](https://issues.chromium.org/issues/381696874#comment19): Thanks! I would like to donate the reward as done with my recent previous reports.

### ap...@google.com (2025-01-09)

Project: v8/v8  

Branch: main  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6162737>

[wasm] Add regression tests for relative canonical type indexes

---


Expand for full commit details
```
[wasm] Add regression tests for relative canonical type indexes 
 
Add regression tests for four fixed bugs. 
 
Bug: 379009132, 380397544, 381696874, 382291459 
Change-Id: I7b50170a8e462204e1de54698e7c848d190689cd 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6162737 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98025}

```

---

Files:

- A `test/mjsunit/regress/wasm/regress-379009132.js`
- A `test/mjsunit/regress/wasm/regress-380397544.js`
- A `test/mjsunit/regress/wasm/regress-381696874.js`
- A `test/mjsunit/regress/wasm/regress-382291459.js`

---

Hash: ed5cd496163651ad81699424d2b95a77cffc8c32  

Date:  Thu Jan 09 13:40:41 2025


---

### ch...@google.com (2025-03-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/381696874)*
