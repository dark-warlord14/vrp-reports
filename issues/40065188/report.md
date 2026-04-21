# Security: v8 crash Bytecode mismatch at offset 78

| Field | Value |
|-------|-------|
| **Issue ID** | [40065188](https://issues.chromium.org/issues/40065188) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Interpreter |
| **Platforms** | Android, Linux, Mac, Windows |
| **Reporter** | be...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-06-02 |
| **Bounty** | $7,000.00 |

## Description


v8 crash Bytecode mismatch at offset 78


Steps to reproduce the problem:
build flag:
gn gen out/fuzzbuild --args='is_debug=false dcheck_always_on=true v8_static_library=true v8_enable_slow_dchecks=true v8_enable_v8_checks=true v8_enable_verify_heap=true v8_enable_verify_csa=true v8_fuzzilli=true sanitizer_coverage_flags="trace-pc-guard" target_cpu="x64"'

environment:
Ubuntu 22.04.2 LTS 5.19.0-42-generic
v8 Version: commit ef16cd37f0aa1a74e0dbd593358086cbaa5534e0 HEAD 11.6.0

run with:
d8 --allow-natives-syntax --fuzzing poc.js

output:
see the output.txt file


crash info:
#
# Fatal error in ../../src/interpreter/interpreter.cc, line 240
# Bytecode mismatch at offset 78

#
#
#
#FailureMessage Object: 0x7fff84b395d0
==== C stack trace ===============================

    out/fuzzbuild_0602/d8(+0x7d7752) [0x56153d623752]
    out/fuzzbuild_0602/d8(+0x7d6267) [0x56153d622267]
    out/fuzzbuild_0602/d8(+0x7c896f) [0x56153d61496f]
    out/fuzzbuild_0602/d8(+0x12a08cd) [0x56153e0ec8cd]
    out/fuzzbuild_0602/d8(+0x129d0cc) [0x56153e0e90cc]
    out/fuzzbuild_0602/d8(+0x129c813) [0x56153e0e8813]
    out/fuzzbuild_0602/d8(+0xb3af67) [0x56153d986f67]
    out/fuzzbuild_0602/d8(+0xb4c999) [0x56153d998999]
    out/fuzzbuild_0602/d8(+0x1b2b6b4) [0x56153e9776b4]
    out/fuzzbuild_0602/d8(+0xb4a2d2) [0x56153d9962d2]
    out/fuzzbuild_0602/d8(+0xb49594) [0x56153d995594]
    out/fuzzbuild_0602/d8(+0xb5590a) [0x56153d9a190a]
    out/fuzzbuild_0602/d8(+0xb7509c) [0x56153d9c109c]
    out/fuzzbuild_0602/d8(+0xb5b56a) [0x56153d9a756a]
    out/fuzzbuild_0602/d8(+0xb5aa2c) [0x56153d9a6a2c]
    out/fuzzbuild_0602/d8(+0x80c4ec) [0x56153d6584ec]
    out/fuzzbuild_0602/d8(+0x80cc8e) [0x56153d658c8e]
    out/fuzzbuild_0602/d8(+0x6f5a40) [0x56153d541a40]
    out/fuzzbuild_0602/d8(+0x6f4c98) [0x56153d540c98]
    out/fuzzbuild_0602/d8(+0x7138f8) [0x56153d55f8f8]
    out/fuzzbuild_0602/d8(+0x7185bb) [0x56153d5645bb]
    out/fuzzbuild_0602/d8(+0x717dd1) [0x56153d563dd1]
    out/fuzzbuild_0602/d8(+0x71b119) [0x56153d567119]
    /lib/x86_64-linux-gnu/libc.so.6(+0x29d90) [0x7fe919229d90]
    /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0x80) [0x7fe919229e40]
    out/fuzzbuild_0602/d8(_start+0x2a) [0x56153d50d02a]
Received signal 6
Aborted (core dumped)



## Attachments

- [poc.js](attachments/poc.js) (text/plain, 797 B)
- [output.txt](attachments/output.txt) (text/plain, 10.1 KB)

## Timeline

### [Deleted User] (2023-06-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-06-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6389205637464064.

### ct...@chromium.org (2023-06-02)

Clusterfuzz is having trouble reproducing this -- are you able to reproduce this and do you have a specific Chromium ASAN build revision that it repros with?

Adding Blink>JavaScript>Interpreter component for visibility.

[Monorail components: Blink>JavaScript>Interpreter]

### le...@chromium.org (2023-06-05)

Shu, might this be related to hole check elision?

### [Deleted User] (2023-06-05)

[Empty comment from Monorail migration]

### sy...@chromium.org (2023-06-06)

> Shu, might this be related to hole check elision?

Looks like it, investigating.

### sy...@chromium.org (2023-06-06)

Fix CL up at https://chromium-review.googlesource.com/c/v8/v8/+/4591496

Leszek, I'm not clear on the security ramifications of bytecode mismatch in this case. Is this actually a security problem or is it a correctness problem with source positions?

### le...@chromium.org (2023-06-06)

Bytecode mismatch can be a security problem iirc, because we might then get a mismatch between the bytecode offset being used and the actual bytecode being executed.

### gi...@appspot.gserviceaccount.com (2023-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/dc628cc1ec065265c46fa3c26a23cfcfba35bb1d

commit dc628cc1ec065265c46fa3c26a23cfcfba35bb1d
Author: Shu-yu Guo <syg@chromium.org>
Date: Tue Jun 06 00:56:53 2023

[interpreter] Use |= in Variable::ForceHoleInitialization

Variables that need hole initialization are never downgraded from
needing hole initialization to not needing hole initialization. They
also track whether they have hole-check uses in the same scope or a
nested scope, which is currently being incorrectly overwritten when
setting one or the other.

Bug: chromium:1450771, v8:13723
Change-Id: I7da3721cdd184d51eda40a70f5d83acf896718e9
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4591496
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Auto-Submit: Shu-yu Guo <syg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88075}

[modify] https://crrev.com/dc628cc1ec065265c46fa3c26a23cfcfba35bb1d/src/ast/variables.h


### aj...@google.com (2023-06-06)

Adding tentative labels.

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### sy...@chromium.org (2023-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-07)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1450771&entry.364066060=External&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Interpreter&entry.975983575=syg@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-07)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-07)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: M114 is already shipping to stable.

Merge review required: M115 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2023-06-07)

[Empty comment from Monorail migration]

### sy...@chromium.org (2023-06-07)

This does not need merge to 114, only to 115, because before 5593d76d69094933d115d496d14aa0c2fde0c266, which is in 115 only, the analysis that has this bug is off by default.

1. Which CLs should be backmerged? (Please include Gerrit links.)

3 CLs need to merged, in the following order:

https://chromium-review.googlesource.com/c/v8/v8/+/4552603
https://chromium-review.googlesource.com/c/v8/v8/+/4571379
https://chromium-review.googlesource.com/c/v8/v8/+/4591496

2. Has this fix been tested on Canary?

Yes

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

Yes, and not that I'm aware of.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

No.

### sy...@chromium.org (2023-06-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-08)

https://chromium-review.googlesource.com/c/v8/v8/+/4552603
https://chromium-review.googlesource.com/c/v8/v8/+/4571379
https://chromium-review.googlesource.com/c/v8/v8/+/4591496

approved for merge to M115, please merge these fixes to 11.5-lkgr at your earliest convenience 

### [Deleted User] (2023-06-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-06-12)

[Empty comment from Monorail migration]

### go...@chromium.org (2023-06-12)

Please merge your change to M115 by  10:00 AM PT tomorrow, Tuesday so we can take it in for this week's beta release.

Branch Details: https://chromiumdash.appspot.com/branches

### sa...@google.com (2023-06-13)

I believe this issue was only introduced in https://bugs.chromium.org/p/chromium/issues/detail?id=1451719#c5 on May 30th (according to some of the deduplicated bugs), so the FoundIn seems wrong here. 

### [Deleted User] (2023-06-13)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/50dfeabc3c747758b4beb71bf38a7ddc57234284

commit 50dfeabc3c747758b4beb71bf38a7ddc57234284
Author: Shu-yu Guo <syg@chromium.org>
Date: Tue Jun 13 15:14:36 2023

Merged: CLs related to TDZ elision var numbering bug

Merged: [interpreter] Don't number non-lexicals in TDZ elision
Revision: 260b62db02dd50a839829fe0af8f3edc31f5d375

Merged: [interpreter] Refine hole check numbering for initialization
Revision: f72cbd53ed999d0027877e3a80e54f9bd4951698

Merged: [interpreter] Use |= in Variable::ForceHoleInitialization
Revision: dc628cc1ec065265c46fa3c26a23cfcfba35bb1d

Bug: chromium:1448545,chromium:1450771,v8:13723
Change-Id: Ie08b443061b48545bb65b3acbe4044fe604aaae8
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4610688
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/branch-heads/11.5@{#16}
Cr-Branched-From: 0c4044b7336787781646e48b2f98f0c7d1b400a5-refs/heads/11.5.150@{#1}
Cr-Branched-From: b71d3038a7d99c79e1c21239e8ae07da5fc8c90b-refs/heads/main@{#87781}

[modify] https://crrev.com/50dfeabc3c747758b4beb71bf38a7ddc57234284/src/interpreter/bytecode-generator.cc
[modify] https://crrev.com/50dfeabc3c747758b4beb71bf38a7ddc57234284/src/ast/scopes.cc
[modify] https://crrev.com/50dfeabc3c747758b4beb71bf38a7ddc57234284/src/ast/variables.cc
[add] https://crrev.com/50dfeabc3c747758b4beb71bf38a7ddc57234284/test/mjsunit/regress/regress-crbug-1448545.js
[modify] https://crrev.com/50dfeabc3c747758b4beb71bf38a7ddc57234284/src/ast/variables.h


### gi...@appspot.gserviceaccount.com (2023-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eebb971918cf1b21daa97cd4c00c7984681aa7a6

commit eebb971918cf1b21daa97cd4c00c7984681aa7a6
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Jun 14 17:03:59 2023

Roll v8 11.5 from 44c8785fbc82 to 571a725c9044 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/44c8785fbc82..571a725c9044

2023-06-14 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 11.5.150.9
2023-06-14 syg@chromium.org Merged: CLs related to TDZ elision var numbering bug

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-11-5-chromium-m115
Please CC liviurau@google.com,v8-waterfall-sheriff@grotations.appspotmail.com,vahl@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 11.5: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m115: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1448545,chromium:1450771
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: Ib60685ff276f8d9b0ed08203e52cd98d901aaf67
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4615824
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5790@{#753}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/eebb971918cf1b21daa97cd4c00c7984681aa7a6/DEPS


### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. A member of our finance team will reach out to you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1450771?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1451090, crbug.com/chromium/1451719]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065188)*
