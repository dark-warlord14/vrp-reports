# Arbitrary Wasm type confusion due to missing struct field mutability check on canonicalization

| Field | Value |
|-------|-------|
| **Issue ID** | [382291459](https://issues.chromium.org/issues/382291459) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2024-12-05 |
| **Bounty** | $55,000.00 |

## Description

### VULNERABILITY DETAILS

#### Summary

Arbitrary Wasm type confusion due to missing struct field mutability check on canonicalization. Mutability checks are missing for struct fields at [`CanonicalEquality::EqualStructType()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/canonical-types.h;drc=a4d354fa54ba3e6a0f061c6b959be408ead5db95;l=326), allowing type confusion between arbitrary Wasm types.

This is a variant of [b/381696874](https://issues.chromium.org/issues/381696874).

#### Details

I've pointed out in [b/381696874](https://issues.chromium.org/issues/381696874) that if we have a broken `CanonicalEquality` check that may be exploitable, we can use the birthday attack to cause a hash collision and trigger the bug. [`CanonicalEquality::EqualStructType()`](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/wasm/canonical-types.h;drc=a4d354fa54ba3e6a0f061c6b959be408ead5db95;l=326) is missing mutability checks for its fields:

```
    bool EqualStructType(const CanonicalStructType& type1,
                         const CanonicalStructType& type2) const {
      return std::equal(
          type1.fields().begin(), type1.fields().end(), type2.fields().begin(),
          type2.fields().end(),
          std::bind_front(&CanonicalEquality::EqualValueType, this));
    }

```

This can be exploited by a casting chain of `struct {const ref null none} -> struct {const ref null any} -> struct {mut ref null any}` where the last cast is due to broken canonicalization, and the first cast is through legal subtype relationship. This allows us to overwrite `ref null none` with a value of `ref null any` type, resulting in arbitrary Wasm type confusion.

The attached PoC/exploit has a precomputed hash-colliding struct type that uses either `const ref null any` or `mut ref null any` for its 40 field types.

#### Bisect

Bug likely introduced by <https://crrev.com/c/6049646> in M133 that attempts to fix [b/379009132](https://issues.chromium.org/issues/379009132) by removing relative type indexs from canonical types. Note that the commit is already backported to [M132](https://crrev.com/c/6049645) and [M131](https://crrev.com/c/6049646).

### VERSION

- M133: <https://crrev.com/c/6049646>
- M132: <https://crrev.com/c/6049645>
- M131: <https://crrev.com/c/6049646>

Chrome Version: 131.0.6778.108, 132.0.6834.32, 133.0.6848.0 ~ latest  

Operating System: All

### REPRODUCTION CASE

Attached as `poc.js` which exploits the hash collision + type confusion to obtain in-sandbox exploit primitives, and then crashes on arbitrary caged write attempt.

Also attached is yet another full exploit `exp.html` that pops `calc` on Windows x64 Chrome, tested against Canary 133.0.6877.0.

### FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Renderer  

Crash State: Crashes on arbitrary caged write attempt from JIT-compiled Wasm function (on d8, `poc.js`), arbitrary code execution (on Chrome, `exp.html`)

### CREDIT INFORMATION

Reporter credit: Seunghyun Lee (@0x10n) of CMU CyLab

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 76.6 KB)
- [exp.html](attachments/exp.html) (text/html, 86.1 KB)

## Timeline

### se...@gmail.com (2024-12-05)

Links for the original patch commit on M133 should be <https://crrev.com/c/6035175>, sorry!

---

FYI on [b/381687256](https://issues.chromium.org/issues/381687256), if we are going to fuzz canonicalization, we need some sort of a "power reduction" mechanism on hashing to induce issues masked behind hash collisions. We can also write a separate harness that does not involve hashing.

### cl...@appspot.gserviceaccount.com (2024-12-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4504362348904448.

### am...@chromium.org (2024-12-05)

Thanks for another one on this, Seunghyun.

I'm not going to attempt to repro this locally given the track on these issues, but I have uploaded the POC to clusterfuzz.
Going to go ahead and triage this based on known information and past reports.

Despite the original issue was introduced in 133, setting Foundin to 131 since the original fix was backmerged to 131

### cl...@chromium.org (2024-12-05)

Hmpf. Working on it. Thanks for the report, Seunghyun!

### cl...@chromium.org (2024-12-05)

Fix: <https://crrev.com/c/6074536>

### ap...@google.com (2024-12-05)

Project: v8/v8  

Branch: main  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6074536>

[wasm] Fix comparison of canonical struct types

---


Expand for full commit details
```
[wasm] Fix comparison of canonical struct types 
 
In addition to the field types we should also check the mutability. 
 
R=jkummerow@chromium.org 
 
Fixed: 382291459 
Change-Id: I46c5d9ece184a49699dd1c1e44c3b6f08646334b 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6074536 
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Clemens Backes <clemensb@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#97587}

```

---

Files:

- M `src/wasm/canonical-types.h`

---

Hash: 3852cf8b5bceed6a76e4537fc0aa191f9ed672a3  

Date:  Thu Dec 05 19:41:22 2024


---

### 24...@project.gserviceaccount.com (2024-12-06)

ClusterFuzz testcase 4504362348904448 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=97586:97587

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### cl...@chromium.org (2024-12-06)

Released in 133.0.6880.0.

### pe...@google.com (2024-12-06)

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

### pe...@google.com (2024-12-06)

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

### jk...@chromium.org (2024-12-09)

#10/#11:

1. Fixes a security bug
2. <https://chromium-review.googlesource.com/6074536>
3. Yes, 133.0.6880.0
4. No
5. N/A
6. No manual testing required.

### am...@chromium.org (2024-12-10)

<https://crrev.com/c/6074536> approved for merges, please merge to 13.2 asap so this fix can be included in next beta; please merge to 13.1 by EOD Thursday 12 December so this fix can be included in next week's Stable update

### ap...@google.com (2024-12-10)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6086196>

Merged: [wasm] Fix comparison of canonical struct types

---


Expand for full commit details
```
Merged: [wasm] Fix comparison of canonical struct types 
 
In addition to the field types we should also check the mutability. 
 
R=jkummerow@chromium.org 
 
Fixed: 382291459 
(cherry picked from commit 3852cf8b5bceed6a76e4537fc0aa191f9ed672a3) 
 
Change-Id: I382164ed5534dd23c0c7a630690b57ae6ad7a4e1 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6086196 
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.2@{#34} 
Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/wasm/canonical-types.h`

---

Hash: 92ed656a375cc0fa3346f00f7e0d9faf0df04db2  

Date:  Thu Dec 05 19:41:22 2024


---

### pe...@google.com (2024-12-10)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2024-12-10)

Project: v8/v8  

Branch: refs/branch-heads/13.1  

Author: Clemens Backes <[clemensb@chromium.org](mailto:clemensb@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6086197>

Merged: [wasm] Fix comparison of canonical struct types

---


Expand for full commit details
```
Merged: [wasm] Fix comparison of canonical struct types 
 
In addition to the field types we should also check the mutability. 
 
R=jkummerow@chromium.org 
 
Fixed: 382291459 
(cherry picked from commit 3852cf8b5bceed6a76e4537fc0aa191f9ed672a3) 
 
Change-Id: I3841b3cfda8e605d724e8695397837eba653ce76 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6086197 
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.1@{#32} 
Cr-Branched-From: 7998da66cb2883ef9734743857713b1194212d9a-refs/heads/13.1.201@{#1} 
Cr-Branched-From: 5e9af2a913539cf67091def99b62f49afece6f56-refs/heads/main@{#96554}

```

---

Files:

- M `src/wasm/canonical-types.h`

---

Hash: 7615ae1b9982bc7f7a55bc85cb9bd7f4beec3fe2  

Date:  Thu Dec 05 19:41:22 2024


---

### qk...@google.com (2024-12-11)

Labeling as LTS-NotApplicable-126 because the suspected CL[1] was not merged to M126 according to the description.

[1] https://crrev.com/c/6049646

### sp...@google.com (2024-12-12)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
high quality report of demonstrated RCE in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-12)

Congratulations on another one Seunghyun! Thank you for your excellent and thorough efforts here and reporting this issue to us -- great work!

### se...@gmail.com (2024-12-12)

Re [comment#19](https://issues.chromium.org/issues/382291459#comment19): Thanks! I would like to donate the reward as done with my recent previous reports.

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

### ch...@google.com (2025-03-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/382291459)*
