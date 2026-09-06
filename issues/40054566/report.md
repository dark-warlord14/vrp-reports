# Security: transferring WebAssembly.Memory's buffer allows shared read/write access across threads

| Field | Value |
|-------|-------|
| **Issue ID** | [40054566](https://issues.chromium.org/issues/40054566) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | gd...@chromium.org |
| **Created** | 2021-01-24 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Transferring the ArrayBuffer associated with a non-shared WebAssembly.Memory object to a worker gives both the main thread and the worker thread read/write access to the buffer contents.

According to the HTML specification, such a transfer should throw a TypeError instead, preventing the problem. Firefox and Safari behave correctly. See also:  

\* the note about [[ArrayBufferDetachKey]] in <https://html.spec.whatwg.org/multipage/structured-data.html#structuredserializewithtransfer>  

\* the issue that introduced this spec change: <https://github.com/whatwg/html/issues/4601>

This incorrect behavior allows constructing a high-precision timer similar to the one in Listing A.6 from the paper "Fantastic Timers and Where to Find Them: High-Resolution Microarchitectural Attacks in JavaScript" (<https://gruss.cc/files/fantastictimers.pdf>). However, since this timer uses WebAssembly.Memory instead of SharedArrayBuffer, it is not affected by the restrictions imposed on SharedArrayBuffer usage (<https://developer.chrome.com/blog/enabling-shared-array-buffer/>). In other words: it works even if the web page is \*not\* cross-origin isolated.

**VERSION**  

Chrome Version: 88.0.4324.104 stable, 90.0.4398.0 canary  

Operating System: Windows 10 2004 (build 19041.450)

**REPRODUCTION CASE**  

The attached HTML page contains a proof-of-concept of a high-precision timer, adapted from Listing A.6 from the paper mentioned above. The main difference with the paper is that the new timer creates and transfers a WebAssembly.Memory's buffer instead of a SharedArrayBuffer.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

N/A

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Mattias Buelens

## Attachments

- [wasm-memory-timer.html](attachments/wasm-memory-timer.html) (text/plain, 689 B)

## Timeline

### [Deleted User] (2021-01-24)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-01-25)

Adding some folks from v8/src/wasm/OWNERS
Setting the severity to High out of an abundance of caution since it is clearly not Critical (thanks adetaylor@)

I haven' been able to confirm it.

[Monorail components: Blink>JavaScript>WebAssembly]

### ah...@chromium.org (2021-01-25)

[Empty comment from Monorail migration]

### gd...@chromium.org (2021-01-26)

I can reproduce this on Canary, it looks like the buffer accessor for the WasmMemoryObject may not be setting the detached flag, and so it does not throw the DataCloneError on serialize as it should. Haven't had a chance to verify this yet as my Chrome checkout grew stale. 

### [Deleted User] (2021-01-26)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-26)

[Empty comment from Monorail migration]

### ma...@gmail.com (2021-01-26)

https://crbug.com/chromium/961059 might be related. Although that one claims that the buffer gets copied when transferring, which is not the case as shown by this issue. (Perhaps Chrome's behavior changed sometime after that other issue was opened?)

### ad...@chromium.org (2021-01-26)

It would be good to bisect this to understand when this new behavior was introduced. I can repro on Chrome 87.

### gd...@chromium.org (2021-01-27)

Sorry to backtrack, I remembered wrong -  the JS API for WebAssembly does not specify that a buffer should be detached when the getter method is called (it does for grow, but not for the getter), both Safari and Firefox throw a type error. As this is not specified, the default behavior in Chrome was not changed. 

More context in this github issue as well - https://github.com/whatwg/html/issues/4601. I'll have to dig a little bit more to see why the copy behavior is no longer working. Given that we haven't added any UMA metrics, the copy behavior was less than ideal and that asm.js buffers are no longer special I'm inclined towards aligning with Firefox and Safari. Are there any objections to this? 

### ad...@chromium.org (2021-01-27)

As per https://crbug.com/chromium/961059, the thought was to move towards aligning with the spec, Firefox, and Safari but given how long this has been a non-error I was worried that we might want to measure before just changing it.

That said, given that this has gone from being a spec bug to being a security issue I'm more comfortable with making a breaking change to get us better-aligned at this point.

With gdeepti out today, I'm going to try to pin down the history here, but will likely assign this to her to make actual changes.

### ad...@chromium.org (2021-01-27)

I bisected, narrowing it down to the revision range https://chromium.googlesource.com/chromium/src/+log/a9fa0793981d568a8fbc44edf403450039507d84..64330518bb33fa79fd81cd385fdd137f4fb7779b, within which is ahaas's https://chromium.googlesource.com/chromium/src/+/7fc06d6289398b3ccb01bd2cb1180ef0c9eb25da.

So it seems the reported issue was an accidental side-effect of ArrayBuffer refactoring in Blink (in March of last year).

The "good" news here is it means we've already changed the semantics of this operation once (in a pretty significant way, allowing cross-thread sharing of a non-shared buffer!), so changing the logic to throw instead continues to seem like a good plan.

### gd...@chromium.org (2021-01-28)

[Empty comment from Monorail migration]

### ah...@chromium.org (2021-01-28)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/dfcf1e86fac0a7b067caf8fdfc13eaf3e3f445e4

commit dfcf1e86fac0a7b067caf8fdfc13eaf3e3f445e4
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Thu Jan 28 21:44:42 2021

[wasm] PostMessage of Memory.buffer should throw

PostMessage of an ArrayBuffer that is not detachable should result
in a DataCloneError.

Bug: chromium:1170176, chromium:961059
Change-Id: Ib89bbc10d2b58918067fd1a90365cad10a0db9ec
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2653810
Reviewed-by: Adam Klein <adamk@chromium.org>
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
Cr-Commit-Position: refs/heads/master@{#72415}

[modify] https://crrev.com/dfcf1e86fac0a7b067caf8fdfc13eaf3e3f445e4/test/mjsunit/wasm/worker-memory.js
[modify] https://crrev.com/dfcf1e86fac0a7b067caf8fdfc13eaf3e3f445e4/src/objects/value-serializer.cc
[modify] https://crrev.com/dfcf1e86fac0a7b067caf8fdfc13eaf3e3f445e4/src/common/message-template.h


### gd...@chromium.org (2021-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-28)

This bug requires manual review: M89's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@google.com (2021-01-28)

+adetaylor@ (Security TPM) for M88 and M89 merge review.  CL listed at #14 is not made it to canary yet, landed  57 mins back. 

### ad...@chromium.org (2021-01-28)

I'd say we definitely should not merge this to M88 since it's a potentially web-platform-visible behavior change.

gdeepti@, mkwst@, as this is a high severity bug it'd be great to merge this to M89, but only if you think the risks of breaking legitimate use-cases are negligible.

### gd...@chromium.org (2021-01-28)

I requested merge to 88 as the Target-88 label was applied by sheriffbot, I'd be okay with merging only to 89. Given the current behavior, I don't think that the use cases that would rely on a non-shared ArrayBuffer's backing store to be shared between threads are legitimate. Also see https://crbug.com/chromium/1170176#c11 by adamk@, that there was a significant change made to this behavior earlier, and there were no reports of breakage so far. Any cross-browser application should not be depending on this as this does not work in Firefox or Safari.  

### ad...@chromium.org (2021-01-29)

Thanks. In that case, approving merge to M89, branch 4389.

### [Deleted User] (2021-02-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/bd856dd3eea4b197b7b3896c4fd9f856d12c8725

commit bd856dd3eea4b197b7b3896c4fd9f856d12c8725
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Mon Feb 01 20:31:29 2021

Merged:[wasm] PostMessage of Memory.buffer should throw

PostMessage of an ArrayBuffer that is not detachable should result
in a DataCloneError.

Bug: chromium:1170176, chromium:961059

(cherry picked from commit dfcf1e86fac0a7b067caf8fdfc13eaf3e3f445e4)

Change-Id: I8063e8605ef30571f1787be7b90041befc20fe98

No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I8063e8605ef30571f1787be7b90041befc20fe98
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2664128
Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
Reviewed-by: Bill Budge <bbudge@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.9@{#29}
Cr-Branched-From: 16b9bbbd581c25391981aa03180b76aa60463a3e-refs/heads/8.9.255@{#1}
Cr-Branched-From: d16a2a688498bd1c3e6a49edb25d8c4ca56232dc-refs/heads/master@{#72039}

[modify] https://crrev.com/bd856dd3eea4b197b7b3896c4fd9f856d12c8725/test/mjsunit/wasm/worker-memory.js
[modify] https://crrev.com/bd856dd3eea4b197b7b3896c4fd9f856d12c8725/src/objects/value-serializer.cc
[modify] https://crrev.com/bd856dd3eea4b197b7b3896c4fd9f856d12c8725/src/common/message-template.h


### pb...@google.com (2021-02-02)

Please merge the CL to M89 branch asap, so that they would be part of tomorrows Beta release.

### cl...@chromium.org (2021-02-02)

The merge was done in #22.

### ad...@chromium.org (2021-02-03)

https://crbug.com/chromium/1174253 is probably a duplicate of this. I'm approving merge to M88 - please go ahead and merge.

### ad...@chromium.org (2021-02-03)

[Empty comment from Monorail migration]

### sr...@google.com (2021-02-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-02-04)

M88 merge CL (thank srinivassista@ and govind@)!
https://chromium-review.googlesource.com/c/v8/v8/+/2674169

(https://crbug.com/chromium/1174253 is a "duplicate" in the sense that it has the same root cause, but different consequences)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/36abafa0a3168ef664a363fce8f9840b43daa2af

commit 36abafa0a3168ef664a363fce8f9840b43daa2af
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Thu Feb 04 00:09:20 2021

[Merged ][wasm] PostMessage of Memory.buffer should throw

PostMessage of an ArrayBuffer that is not detachable should result
in a DataCloneError.

TBR=gdeepti@chromium.org

(cherry picked from commit dfcf1e86fac0a7b067caf8fdfc13eaf3e3f445e4)

Bug: chromium:1170176, chromium:961059
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: Ife852df032841b7001375acd5e101d614c4b0771
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2674169
Reviewed-by: Zhi An Ng <zhin@chromium.org>
Commit-Queue: Zhi An Ng <zhin@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.8@{#30}
Cr-Branched-From: 2dbcdc105b963ee2501c82139eef7e0603977ff0-refs/heads/8.8.278@{#1}
Cr-Branched-From: 366d30c99049b3f1c673f8a93deb9f879d0fa9f0-refs/heads/master@{#71094}

[modify] https://crrev.com/36abafa0a3168ef664a363fce8f9840b43daa2af/test/mjsunit/wasm/worker-memory.js
[modify] https://crrev.com/36abafa0a3168ef664a363fce8f9840b43daa2af/src/objects/value-serializer.cc
[modify] https://crrev.com/36abafa0a3168ef664a363fce8f9840b43daa2af/src/common/message-template.h


### go...@chromium.org (2021-02-04)

Merged to M88 at #29. Adjusting merge labels. 

### ad...@chromium.org (2021-02-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-02-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-02-04)

This crash occurs very frequently on linux platform and is likely preventing the fuzzer None from making much progress. Fixing this will allow more bugs to be found.

Marking this bug as a blocker for next Beta release.

If this is incorrect, please add the ClusterFuzz-Wrong label and remove the ReleaseBlock-Beta label.

### cl...@chromium.org (2021-02-04)

ClusterFuzz testcase 5680973040386048 appears to be flaky, updating reproducibility label.

### ad...@chromium.org (2021-02-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-02-04)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-04)

Marking this as Fixed - please correct me if I'm wrong.

### ad...@google.com (2021-02-04)

[Empty comment from Monorail migration]

### sr...@google.com (2021-02-04)

M88.0.4324.150 build is in progress and test team is qualifying this during day time ( IST). Can some one from V8 team help verify this fix in M89 beta release that went out today ( that has this fix) and also check if any other issues happen due to this. ( See https://crbug.com/chromium/1170176#c19 and #18), we want to ensure we cover these concerns before stable roll out tomorrow for this fix. hablich@ , vahl@ 

### ad...@google.com (2021-02-04)

See https://crbug.com/chromium/1174253#c15 for verification that the fix is correctly merged into 88.0.4324.150.

### ad...@google.com (2021-02-04)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-04)

[Empty comment from Monorail migration]

### vi...@google.com (2021-02-04)

Looks like fix has already been verified by V8 QA team, and talked to  srinivassista@ ,sanity test on latest Chrome beta has been performed by BrApp test team. We don't have any additional Blink regression tests to run here. 


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/89b949b3307eb99dcafa5347607d32a5f3592a1d

commit 89b949b3307eb99dcafa5347607d32a5f3592a1d
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Thu Feb 04 18:41:58 2021

[wasm] PostMessage of Memory.buffer should throw

PostMessage of an ArrayBuffer that is not detachable should result
in a DataCloneError.

(cherry picked from commit dfcf1e86fac0a7b067caf8fdfc13eaf3e3f445e4)

Bug: chromium:1170176, chromium:961059
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: Ib89bbc10d2b58918067fd1a90365cad10a0db9ec
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2653810
Reviewed-by: Adam Klein <adamk@chromium.org>
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#72415}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2675930
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Jana Grill <janagrill@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.6@{#60}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/89b949b3307eb99dcafa5347607d32a5f3592a1d/test/mjsunit/wasm/worker-memory.js
[modify] https://crrev.com/89b949b3307eb99dcafa5347607d32a5f3592a1d/src/objects/value-serializer.cc
[modify] https://crrev.com/89b949b3307eb99dcafa5347607d32a5f3592a1d/src/common/message-template.h


### [Deleted User] (2021-02-04)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-04)

redacted

### ad...@google.com (2021-02-05)

[Empty comment from Monorail migration]

### vs...@google.com (2021-02-05)

[Empty comment from Monorail migration]

### vs...@google.com (2021-02-05)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-10)

Congratulations, Mattias - the VRP Panel has decided to award you $7,500 for this report! A member of our finance team will reach out to you soon to arrange payment. Thank you for your efforts and nice work! 

### am...@google.com (2021-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1170176?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1174253]
[Monorail components added to Component Tags custom field.]

### ma...@gmail.com (2026-08-25)

I see this bug still has limited visibility. Can this be made publicly visible, seeing that it's been fixed for more than 5 years now? Thanks.

### aj...@google.com (2026-08-31)

Removing embargo as we can now make certain comments limited visibility.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054566)*
