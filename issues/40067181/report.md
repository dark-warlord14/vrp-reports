# Security: Segment Fault in v8 wasm at address > page size

| Field | Value |
|-------|-------|
| **Issue ID** | [40067181](https://issues.chromium.org/issues/40067181) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2023-07-11 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 88364
    - link: https://crrev.com/a81cc3b433d1660528b5da5c97a4396ab35debe7 
- Commit Message

```
commit a81cc3b433d1660528b5da5c97a4396ab35debe7
Author: JianxiaoLuIntel <jianxiao.lu@intel.com>
Date:   Fri Jun 16 13:07:26 2023 +0800

    Reland "[test][revec] Improve test run wasm simd for revec"
    
    This reland commit 31b769abf90c3bff182250c9e9faf479f5f635e4.
    
    Bug fixing: Return the tests if AVX2 is not supported
    
    Original change's description:
    > [test][revec] Improve test run wasm simd for revec
    >
    > Current revec test frame work mainly consist of two part:
    > revec-unittest and test-run-wasm-simd. The revec-unittest can only
    > check if the revec success, but can not check the execution result.
    > The tests in test-run-wasm-simd can verify the execution result, but
    > can not check if the revec success. (When revec failed, those tests
    > can also get correct execution result). Those limitation may cause
    > unchecked bugs get landed.
    >
    > To solve this problem, this patch improve revec tests in
    > test-run-wasm-simd by introducing node-observer. When revec success,
    > it will record those new created simd256 nodes, then the test will
    > check if the expected simd256 nodes is created base on that.
    >
    >
    > Bug: v8:12716
    > Change-Id: I26f2bf688b46b2b9da105baa4ba127d48f053bfd
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4600454
    > Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    > Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
    > Commit-Queue: Jianxiao Lu <jianxiao.lu@intel.com>
    > Cr-Commit-Position: refs/heads/main@{#88225}
    
    Change-Id: I3bfcb46286463ac786fd181d5e723bf8a93e8202
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4615439
    Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Jianxiao Lu <jianxiao.lu@intel.com>
    Cr-Commit-Position: refs/heads/main@{#88364}

```

## CRASH LOG
- release output

```bash
# CMD: /tmp/d8-linux-release-v8-component-88799/d8 --allow-natives-syntax --experimental-wasm-gc --experimental-wasm-revectorize poc.js
# OUTPUT ==============================================================
Received signal 11 SEGV_MAPERR 00000000eb60

==== C stack trace ===============================

 [0x55ab8c494867]
 [0x7fa804042520]
 [0x55ab8c1796a8]
 [0x55ab8c067ed1]
 [0x55ab8c05f3dd]
 [0x55ab8c05ba37]
 [0x55ab8c158917]
 [0x55ab8bcddcdc]
 [0x55ab8bcdd362]
 [0x55ab8bd092cd]
 [0x55ab8bd08c57]
 [0x55ab8c495cbb]
 [0x55ab8c498b3b]
 [0x55ab8c491d52]
 [0x7fa804094b43]
 [0x7fa804126a00]
[end of stack trace]

```

## Other1
Please note to include the flags `--allow-natives-syntax --experimental-wasm-gc --experimental-wasm-revectorize` for clusterfuzz classification.

## Other2
According to the description, an npd (null pointer dereference) larger than one page should be considered a security issue, and it may be worth obtaining a v8 bug bounty.

https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#why-aren_t-null-pointer-dereferences-considered-security-bugs
```
Null pointer dereferences with consistent, small, fixed offsets are not considered security bugs. A read or write to the NULL page results in a non-exploitable crash. If the offset is larger than a page, or if there's uncertainty about whether the offset is controllable, it is considered a security bug.
```

0xeb60 is larger than one page.

VERSION
Tested on v8 version: 11.6.0 - 11.7.0

REPRODUCTION CASE
1. Download release v8 from: gs://v8-asan/linux-release/d8-linux-release-v8-component-88799.zip
2. Run: `d8 --allow-natives-syntax --experimental-wasm-gc --experimental-wasm-revectorize poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

## Attachments

- [wasm.js](attachments/wasm.js) (text/plain, 4.2 KB)
- [wasm.js](attachments/wasm_53102300.js) (text/plain, 4.2 KB)

## Timeline

### je...@gmail.com (2023-07-11)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 88364
    - link: https://crrev.com/a81cc3b433d1660528b5da5c97a4396ab35debe7 
- Commit Message

```
commit a81cc3b433d1660528b5da5c97a4396ab35debe7
Author: JianxiaoLuIntel <jianxiao.lu@intel.com>
Date:   Fri Jun 16 13:07:26 2023 +0800

    Reland "[test][revec] Improve test run wasm simd for revec"
    
    This reland commit 31b769abf90c3bff182250c9e9faf479f5f635e4.
    
    Bug fixing: Return the tests if AVX2 is not supported
    
    Original change's description:
    > [test][revec] Improve test run wasm simd for revec
    >
    > Current revec test frame work mainly consist of two part:
    > revec-unittest and test-run-wasm-simd. The revec-unittest can only
    > check if the revec success, but can not check the execution result.
    > The tests in test-run-wasm-simd can verify the execution result, but
    > can not check if the revec success. (When revec failed, those tests
    > can also get correct execution result). Those limitation may cause
    > unchecked bugs get landed.
    >
    > To solve this problem, this patch improve revec tests in
    > test-run-wasm-simd by introducing node-observer. When revec success,
    > it will record those new created simd256 nodes, then the test will
    > check if the expected simd256 nodes is created base on that.
    >
    >
    > Bug: v8:12716
    > Change-Id: I26f2bf688b46b2b9da105baa4ba127d48f053bfd
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4600454
    > Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    > Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
    > Commit-Queue: Jianxiao Lu <jianxiao.lu@intel.com>
    > Cr-Commit-Position: refs/heads/main@{#88225}
    
    Change-Id: I3bfcb46286463ac786fd181d5e723bf8a93e8202
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4615439
    Reviewed-by: Thibaud Michaud <thibaudm@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Jianxiao Lu <jianxiao.lu@intel.com>
    Cr-Commit-Position: refs/heads/main@{#88364}

```

## CRASH LOG
- release output

```bash
# CMD: /tmp/d8-linux-release-v8-component-88799/d8 --allow-natives-syntax --experimental-wasm-gc --experimental-wasm-revectorize poc.js
# OUTPUT ==============================================================
Received signal 11 SEGV_MAPERR 00000000eb60

==== C stack trace ===============================

 [0x55ab8c494867]
 [0x7fa804042520]
 [0x55ab8c1796a8]
 [0x55ab8c067ed1]
 [0x55ab8c05f3dd]
 [0x55ab8c05ba37]
 [0x55ab8c158917]
 [0x55ab8bcddcdc]
 [0x55ab8bcdd362]
 [0x55ab8bd092cd]
 [0x55ab8bd08c57]
 [0x55ab8c495cbb]
 [0x55ab8c498b3b]
 [0x55ab8c491d52]
 [0x7fa804094b43]
 [0x7fa804126a00]
[end of stack trace]

```

## Other1
Please note to include the flags `--allow-natives-syntax --experimental-wasm-gc --experimental-wasm-revectorize` for clusterfuzz classification.

## Other2
According to the description, an npd (null pointer dereference) larger than one page should be considered a security issue, and it may be worth obtaining a v8 bug bounty.

https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#why-aren_t-null-pointer-dereferences-considered-security-bugs
```
Null pointer dereferences with consistent, small, fixed offsets are not considered security bugs. A read or write to the NULL page results in a non-exploitable crash. If the offset is larger than a page, or if there's uncertainty about whether the offset is controllable, it is considered a security bug.
```

0xeb60 is larger than one page.

VERSION
Tested on v8 version: 11.6.0 - 11.7.0

REPRODUCTION CASE
1. Download release v8 from: gs://v8-asan/linux-release/d8-linux-release-v8-component-88799.zip
2. Run: `d8 --allow-natives-syntax --experimental-wasm-gc --experimental-wasm-revectorize poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-07-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4859344841277440.

### da...@chromium.org (2023-07-11)

Thanks for the report. The --experimental-wasm-gc --experimental-wasm-revectorize flags are not enabled by default, so this won't have security implications at the moment.

https://source.chromium.org/chromium/chromium/src/+/main:v8/src/flags/flag-definitions.h;l=1437-1438?q=experimental_wasm_revectorize&ss=chromium%2Fchromium%2Fsrc

Provisionally setting FoundIn to extended stable, but as there's no security implication if these flags are needed, no merge should be required.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2023-07-11)

Detailed Report: https://clusterfuzz.com/testcase?key=4859344841277440

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x00000000eb68
Crash State:
  v8::internal::Isolate::node_observer
  v8::internal::compiler::Revectorizer::Revectorizer
  v8::internal::compiler::RevectorizePhase::Run
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=88363:88364

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4859344841277440

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### [Deleted User] (2023-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-12)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-07-13)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Compiler]

### cf...@google.com (2023-07-13)

Hey @thibaudm,
could you PTAL? 
This bisects to crrev.com/a81cc3b433d1660528b5da5c97a4396ab35debe7.

### th...@chromium.org (2023-07-13)

I'm hitting a DCHECK here because we don't have an isolate (background compile thread):
https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/revectorizer.cc;drc=62c276ad490c140013681b6e2b7c7e6299db138c;l=819

I prepared a fix which I'll send shortly (I leave the observer null if there is no isolate, the observer is only needed for tests).

However I'm still hitting another DCHECK in wasm-gc-lowering.cc after this fix, it looks completely unrelated so I'll run another local bisect with the first fix applied.

### je...@gmail.com (2023-07-13)

[Comment Deleted]

### je...@gmail.com (2023-07-13)

[Comment Deleted]

### je...@gmail.com (2023-07-13)

[Comment Deleted]

### je...@gmail.com (2023-07-13)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2023-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c531a65d76e9361c4a67df287c5ed1c3894146d3

commit c531a65d76e9361c4a67df287c5ed1c3894146d3
Author: Thibaud Michaud <thibaudm@chromium.org>
Date: Thu Jul 13 14:43:33 2023

[revec] Fix null isolate dereference

Only set the node observer if we do have an isolate. This should always
be the case for tests, and the observer is not needed otherwise.

R=nicohartmann@chromium.org
CC=jianxiao.lu@intel.com

Bug: chromium:1463850
Change-Id: I5376d837cea8d7f5d632f4f95527a406d129114a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4683628
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#88921}

[modify] https://crrev.com/c531a65d76e9361c4a67df287c5ed1c3894146d3/src/compiler/revectorizer.cc


### je...@gmail.com (2023-07-14)

[Comment Deleted]

### cl...@chromium.org (2023-07-14)

ClusterFuzz testcase 4859344841277440 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=88920:88921

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-14)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M114. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

Merge review required: M114 is already shipping to stable.

Merge review required: M115 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-17)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1463850&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript,Blink>JavaScript>Compiler&entry.975983575=thibaudm@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2023-07-17)

Removing some flags since this is not a security issue.

### et...@gmail.com (2023-07-17)

[Comment Deleted]

### je...@gmail.com (2023-07-17)

[Comment Deleted]

### th...@chromium.org (2023-07-17)

The reason we don't consider this a security bug is that this requires manually enabling an experimental flag (wasm revectorization), so this does not affect end users.
For the wasm GC bug, you are correct in the other issue that the origin trial makes this eligible for VRP. But per Jakob's last comment it sounds like this is also not a security issue for a different reason.

### je...@gmail.com (2023-07-17)

[Comment Deleted]

### je...@gmail.com (2023-07-17)

[Comment Deleted]

### je...@gmail.com (2023-07-17)

[Comment Deleted]

### th...@chromium.org (2023-07-17)

Hello,
Thanks for the clarification, this is indeed a mistake on our part and the flag should have been marked as experimental, we will update it.
Adding back the security flags, we will leave this up to the VRP panel whether this is eligible for a reward.
Apologies for the confusion and thanks for the report.

### je...@gmail.com (2023-07-17)

[Comment Deleted]

### th...@chromium.org (2023-07-17)

I don't appear to have the right permission to add the reward-topanel flag, this is normally set by the sheriffbot.
CC sroettger, can you set it manually, or do you know someone who can?

### sr...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e8b8b94fa8125391eb3ef0195ce8c4ff66da79a2

commit e8b8b94fa8125391eb3ef0195ce8c4ff66da79a2
Author: Thibaud Michaud <thibaudm@chromium.org>
Date: Mon Jul 17 11:56:57 2023

[wasm][revec] Mark revectorization as experimental

R=clemensb@chromium.org

Bug: chromium:1463850
Change-Id: I66a9e9f5f3eea2455f69b60b3a909d6affb0c880
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4689698
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89027}

[modify] https://crrev.com/e8b8b94fa8125391eb3ef0195ce8c4ff66da79a2/src/flags/flag-definitions.h


### am...@google.com (2023-07-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-19)

Thank you for this report, Jerry, and congratulations on another find. This issue appears to be significantly mitigated and not likely to be able to be exploited. If you can demonstrate or provide analysis of how this issue could be exploited in a real world scenario, we would be happy to reassess for a potential change in reward amount. Since there was a lot of communication here and this also resulted in wasm revectorization being appropriately set as --experimental, we did want to extend to you a $1,000 reward for your effort here. 


### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-18)

[Description Changed]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1463850?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067181)*
