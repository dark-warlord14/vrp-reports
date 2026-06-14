# Signal SIGSEGV in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [355870166](https://issues.chromium.org/issues/355870166) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Regexp |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2024-07-28 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 95296
    - link: https://crrev.com/d57d08176393b280881c07719e622eaf08f4f9db 
- Commit Message

```
commit d57d08176393b280881c07719e622eaf08f4f9db
Author: pthier <pthier@chromium.org>
Date:   Thu Jul 25 15:34:41 2024 +0200

    [regexp][sandbox] Move RegExp data to trusted space
    
    Replace the generic FixedArray used to store sharable RegExp data
    with dedicated instances, that live in trusted space instead of
    inside the sandbox.
    
    Bug: 42204606
    Change-Id: I8c51248aef8d57259b561a70442f2f82999c63ab
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5713168
    Commit-Queue: Patrick Thier <pthier@chromium.org>
    Reviewed-by: Camillo Bruni <cbruni@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95296}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-95326/d8 --stress-compaction poc.js
# OUTPUT ==============================================================
Received signal 11 SEGV_ACCERR 1351000400fc

```

## Other
Please note to include the flags `--stress-compaction` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.9.0 - 12.9.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-95326.zip
2. Run: `d8 --stress-compaction poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)    

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 173 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-07-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5157919211323392.

### ph...@chromium.org (2024-07-29)

Severity S1 is provisional. FoundIn 129 is according to the bisect result.

### pe...@google.com (2024-07-29)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-07-29)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### cf...@google.com (2024-07-29)

This does not trigger on HEAD anymore.  

After bisecting it seems like [crrev.com/62534ab83b21ef4749baf042fb60285c309ba4da](https://crrev.com/62534ab83b21ef4749baf042fb60285c309ba4da) fixed this?  

olivf@ could you check if this is indeed the same root cause?

### ki...@gmail.com (2024-07-30)

I can trigger on HEAD（gs://v8-asan/linux-debug/d8-linux-debug-v8-component-95367.zip）
You can stress all CPUs and try running it several times.


### ki...@gmail.com (2024-07-31)

Still repro in latest HEAD:

```
$ /tmp/d8-linux-debug-v8-component-95399/d8 --stress-compaction /tmp/poc.js
Received signal 11 SEGV_ACCERR 2996000400f4
[1]    2592969 segmentation fault  /tmp/d8-linux-debug-v8-component-95399/d8 --stress-compaction /tmp/poc.js

```

It may need to be executed several times to reproduce it.

### ol...@chromium.org (2024-07-31)

I don't think could have been fixed by my CL. @patrick can you have a look?

### ki...@gmail.com (2024-08-02)

hello，any update？

### pt...@chromium.org (2024-08-02)

Sorry I was sick and didn't manage to take a look at this until now.
At a first glance it looks like references to trusted space objects on the stack are not updated when they are moved during compaction.
I will need to spend more time on this next week.

I can confirm that this was an unknown issue not found by our fuzzers before this report.

### ap...@google.com (2024-08-06)

Project: v8/v8
Branch: main

commit f34974b6f26cf610471eaf4bcf9f60f3174f87f9
Author: pthier <pthier@chromium.org>
Date:   Tue Aug 06 15:07:17 2024

    [maglev][sandbox] TrustedConstants are tagged pointers
    
    ... and not plain IntPtrs. Otherwise spill slots won't get updated if
    the trusted object is evacuated.
    
    Fixed: 355870166
    Bug: 42204606
    Change-Id: I1f95933d3704a55b7946a0d7784e12e0b63a9adc
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5765374
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Reviewed-by: Olivier Flückiger <olivf@chromium.org>
    Commit-Queue: Patrick Thier <pthier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95502}

M       src/maglev/maglev-graph-builder.cc
M       src/maglev/maglev-ir.h

https://chromium-review.googlesource.com/5765374


### 24...@project.gserviceaccount.com (2024-08-07)

ClusterFuzz testcase 5157919211323392 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95501:95502

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2024-08-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / the renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-16)

Congratulations Zhenghang! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-08-21)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
**Merge approved:** your change passed merge requirements and is auto-approved for M129. Please go ahead and merge the CL to branch 6668 (refs/branch-heads/6668) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pt...@chromium.org (2024-08-21)

No merge required. The fix shipped with Chromium 129.0.6642.0

### pe...@google.com (2024-11-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/355870166)*
