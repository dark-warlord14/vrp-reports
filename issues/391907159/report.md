# WasmCode "resurrection" using the WasmImportWrapperCache can lead to JIT allocation UaF, causing memory corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [391907159](https://issues.chromium.org/issues/391907159) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@popax21.dev |
| **Assignee** | jk...@chromium.org |
| **Created** | 2025-01-24 |
| **Bounty** | $55,000.00 |

## Description

`WasmCode` are ref-counted objects which represent a corresponding JIT allocation containing Wasm code. These objects are not freed immediately when their reference count reaches zero - instead they are added to a list of "potentially dead code" (`WasmEngine::potentially_dead_code_`). Once enough "potentially dead code" has accumulated, the Wasm code GC kicks in - its responsibility is to check whether code is truly dead (i.e. not in use by any isolate), and any such code is moved to the `WasmEngine::dead_code_` list, before at last being freed.

This transition from the `potentially_dead_code_` set to the `dead_code_` set has one noteworthy edge case: if the reference count of the `WasmCode` object has increased since the code object was initially declared "potentially dead", the object is still moved to the `dead_code_` set as usual, however it is not freed afterwards. Instead, the next time the reference count drops to zero, the `WasmCode` object is instead freed immediately, bypassing the Wasm code GC in the process. Going of comments in the related source code, it seems that this mechanism is intentional, and is meant to deal with temporary Wasm code references held by other threads as part of e.g. walking the stack.

However, this behavior can be abused if a `WasmCode` instance were to be "resurrected", as in made accessible to regular JS code again. In practice this can occur through the `WasmImportWrapperCache`: it only removes cache entries for import wrappers once these wrappers are actually freed, not once their reference count initially reaches zero. This allows import wrapper tierups / other cache lookups to "resurrect" a wrapper which is currently in the `potentially_dead_code_` set. The consequences of this resurrection are severe: the next time the wrapper's reference count drops to zero (by e.g. removing it from all dispatch tables), it (and its corresponding JIT allocation) is immediately freed, even if the wrapper's code is currently live and part of the stack.

Exploiting this issue is not as trivial as simply spraying new JIT code to replace the freed wrapper's code, since `WasmCodeAllocator` instances never reuse old freed allocations for new allocation requests. However, the premature free of the `WasmCode` object also messes up the invariants of the per-isolate Wasm code lookup cache, which assumes that code may only be freed as part of a Wasm code GC or a `NativeModule` being freed. Since neither applies in this case, the lookup cache is never cleared, which results in it still containing a dangling pointer to the freed `WasmCode` instance. An attacker can then spray the heap with new `WasmCode` instances to take control over the metadata of the dangling wrapper's stack frame, which allows them to e.g. prevent the GC from picking up references stored in said stack frame, which in return leads to dangling heap objects which can be used by an attacker to take full control over the heap. Additionally, it is also feasible that a more sophisticated spray could allow an attacker to take control over several critical pointers / metadata fields stored in `WasmCode` instances, which could feasibly allow them to escape the sandbox.

See attached the following two files:

- `poc.js`: a simple POC for this issue, triggering a DCHECK in the `WasmCodeLookupCache` as a result of the dangling `WasmCode` pointer still being present in the cache.
- `exploit.js`: a fully developed RCE exploit using this issue. Note that this doesn't use the bug described here to escape the sandbox; instead, for the sake of speeding up this report, it reuses the sandbox escape I've reported in [issue 384186547](https://issues.chromium.org/issues/384186547). This issue has already been fixed, however the fix has not been shipped as part M132 yet.
  - Note that this exploit chain requires access to SharedArrayBuffers, which requires that the HTTP server hosting the exploit sets the correct HTTP headers
  - A hosted version of this exploit featuring a WebSocket-based logging harness is also available at `https://cytc.popax21.dev/d34d09ffb752e30529a8cd3e341ea592c9a87a9ff1885ee5889873562bbbcc28`
  - I have confirmed that this exploit chain can be used to obtain RCE targeting both Google Chrome 132.0.6834.83 as well as Chromium 131.0.6778.264 (note that targeting M131 requires swapping out a constant in the exploit code).

There are two possible ways I am aware of regarding how this issue might be fixed:

- invalidate / remove `WasmImportWrapperCache` entries as soon as the wrapper's reference count reaches zero. This removes this particular avenue of resurrecting `WasmCode` instances, but leaves the door open for a similar issue to reoccur in the future if there ever was another way to obtain a long-lived reference to a `WasmCode` instance in the `potentially_dead_code_` set.
- rework / remove the underlying mechanism allowing for the resurrection of `WasmCode` instances. This could for example be done by not adding the `WasmCode` instance to the `dead_code_` set if the reference count has increased - this effectively fully resurrects the object, making it wait for the next Wasm GC invocation once its refcount drops to zero once more. This has the downside of potentially increasing the lifetime of `WasmCode` objects whose only remaining references are temporary in nature arbitrarily, so this approach would require proper benchmarking (or additional logic to only fully resurrect objects which have long-lived references) before being implemented.

Reporter Credit: if applicable, please credit my pseudonym Popax21 in regards to this report.

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 4.0 KB)
- [exploit.js](attachments/exploit.js) (text/javascript, 60.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-01-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4998468003102720.

### aj...@google.com (2025-01-24)

Thanks for the detailed description and repro - CF has already hit the DCHECK - setting sev=High and FoundIn=132 based on comments in report and sending to the v8 rotation.

### 24...@project.gserviceaccount.com (2025-01-24)

Detailed Report: https://clusterfuzz.com/testcase?key=4998468003102720

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  entry->code == wasm::GetWasmCodeManager()->LookupCode(pc) in wasm-code-manager.c
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95827:95828

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4998468003102720

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pe...@google.com (2025-01-25)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-25)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cf...@google.com (2025-01-28)

Thank you for this great report!  

jkummerow@, could you PTAL at this?

### ap...@google.com (2025-01-31)

Project: v8/v8  

Branch: main  

Author: Jakob Kummerow <[jkummerow@chromium.org](mailto:jkummerow@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6218221>

[wasm] Replace {dead\_code\_} set with {is\_dying\_} bit

---


Expand for full commit details
```
[wasm] Replace {dead_code_} set with {is_dying_} bit 
 
This saves some memory, and fixes a bug. 
 
Fixed: 391907159 
Change-Id: I18bbd6e1084de0cbb2f78284de80e2296b901ee1 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6218221 
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98428}

```

---

Files:

- M `src/wasm/wasm-code-manager.h`
- M `src/wasm/wasm-engine.cc`
- M `src/wasm/wasm-engine.h`
- M `src/wasm/wasm-import-wrapper-cache.cc`
- M `src/wasm/wasm-objects.cc`
- M `test/cctest/wasm/wasm-run-utils.cc`

---

Hash: 33ca4f51e5dbba9817eba16fd3249e66a880cf33  

Date:  Thu Jan 30 21:17:20 2025


---

### jk...@chromium.org (2025-01-31)

Thanks again for the report, excellent work!

### pe...@google.com (2025-01-31)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M132. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M133. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2025-02-01)

ClusterFuzz testcase 4998468003102720 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98427:98428

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2025-02-01)

Merge review required: M133 has already been cut for stable release.

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
Owners: andywu (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### pe...@google.com (2025-02-01)

Merge review required: M132 is already shipping to stable.

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

### am...@chromium.org (2025-02-05)

merges approved for <https://crrev.com/c/6218221> based on nearly week's worth of canary coverage and no issues
please merge this fix to 133 Stable / 13.3 and 132 Extended Stable / 13.2 at your earliest convenience, by EOD tomorrow, 6 February

### sp...@google.com (2025-02-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
high-quality report demonstrating RCE in a sandboxed process / the renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-06)

Congratulations Popax21! Thank you for the excellent work here and reporting this issue to us -- excellent stuff!

### ap...@google.com (2025-02-06)

Project: v8/v8  

Branch: refs/branch-heads/13.3  

Author: Jakob Kummerow <[jkummerow@chromium.org](mailto:jkummerow@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6239495>

Merged: [wasm] Replace {dead\_code\_} set with {is\_dying\_} bit

---


Expand for full commit details
```
Merged: [wasm] Replace {dead_code_} set with {is_dying_} bit 
 
This saves some memory, and fixes a bug. 
 
Fixed: 391907159 
(cherry picked from commit 33ca4f51e5dbba9817eba16fd3249e66a880cf33) 
 
Change-Id: I3324f33bbf7b6a191b508e854ef92c9e9a5efba5 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6239495 
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.3@{#38} 
Cr-Branched-From: 41dacffe436aeb9311879cb07648f1e36609a804-refs/heads/13.3.415@{#1} 
Cr-Branched-From: 3348638c0af67c885b30891a358c89a917ac9759-refs/heads/main@{#97937}

```

---

Files:

- M `src/wasm/wasm-code-manager.h`
- M `src/wasm/wasm-engine.cc`
- M `src/wasm/wasm-engine.h`
- M `src/wasm/wasm-import-wrapper-cache.cc`
- M `src/wasm/wasm-objects.cc`
- M `test/cctest/wasm/wasm-run-utils.cc`

---

Hash: 19ad509f7b61ef75bfb7a0b93f6246db1c78826d  

Date:  Thu Feb 06 14:18:48 2025


---

### pe...@google.com (2025-02-06)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2025-02-06)

Project: v8/v8  

Branch: refs/branch-heads/13.2  

Author: Jakob Kummerow <[jkummerow@chromium.org](mailto:jkummerow@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6239106>

Merged: [wasm] Replace {dead\_code\_} set with {is\_dying\_} bit

---


Expand for full commit details
```
Merged: [wasm] Replace {dead_code_} set with {is_dying_} bit 
 
This saves some memory, and fixes a bug. 
 
Fixed: 391907159 
(cherry picked from commit 33ca4f51e5dbba9817eba16fd3249e66a880cf33) 
 
Change-Id: Iad93b3e7290c25ddcedf806cc85c4401a5fcb0fc 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6239106 
Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
Cr-Commit-Position: refs/branch-heads/13.2@{#76} 
Cr-Branched-From: 24068c59cedad9ee976ddc05431f5f497b1ebd71-refs/heads/13.2.152@{#1} 
Cr-Branched-From: 6054ba94db0969220be4f94dc1677fc4696bdc4f-refs/heads/main@{#97085}

```

---

Files:

- M `src/wasm/wasm-code-manager.h`
- M `src/wasm/wasm-engine.cc`
- M `src/wasm/wasm-engine.h`
- M `src/wasm/wasm-import-wrapper-cache.cc`
- M `src/wasm/wasm-objects.cc`
- M `test/cctest/wasm/wasm-run-utils.cc`

---

Hash: 924c1a79f1398960f20b97ace5ab7ffbd9db2d06  

Date:  Thu Feb 06 14:42:13 2025


---

### jk...@chromium.org (2025-02-06)

#18: Already merged to M132. And I've verified that the fix landed before the M134 branch point. So we're all good here.

### qk...@google.com (2025-02-10)

Labeled LTS-Merge-Merge-132 for M132 LTS because the fix[1] was already merged to M132 branch. And, labeled LTS-NotApplicable-126 because there were many conflicts when trying to merge the fix to the M126 branch. It was difficult to find when the issue started to happen,  I guess that this issue might happen after M126 release because the code base for the fix was different.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/6239106

### ch...@google.com (2025-05-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/391907159)*
