# Security: WebAssembly UAF in catch block with stale memory start pointer

| Field | Value |
|-------|-------|
| **Issue ID** | [40061453](https://issues.chromium.org/issues/40061453) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | gz...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2022-10-24 |
| **Bounty** | $21,000.00 |

## Description

**VULNERABILITY DETAILS**

WebAssembly memory start and size are stored as wasm instance fields. The WasmGraphBuilder caches the corresponding TurboFan nodes and only reloads them when necessary. One such reload is following a function call:

<https://github.com/v8/v8/blob/28f763b5949d053c62e95db2f997a9f13b2e3065/src/wasm/graph-builder-interface.cc#L1944>

CheckForException(  

decoder, builder\_->CallIndirect(  

call\_info.table\_index(), call\_info.sig\_index(),  

base::VectorOf(arg\_nodes),  

base::VectorOf(return\_nodes), decoder->position()));  

...  

// The invoked function could have used grow\_memory, so we need to  

// reload mem\_size and mem\_start.  

LoadContextIntoSsa(ssa\_env\_, decoder);

The invoked function may have increased memory size, which may have moved the memory, so memory start and size are reloaded within LoadContextIntoSsa().

Notice the CheckForException() though. It can jump to the catch block of a surrounding try-catch before the memory fields are reloaded. So suppose we have the following:

func thrower  

grow memory  

throw

func bad  

/\* cache memory start pointer \*/  

load mem[0]  

try  

thrower()  

catch  

/\* can use a stale memory start pointer \*/  

store mem[0] = 42

The thrower() grows memory and then throws an exception. The catch block can UAF a stale memory start pointer.

**VERSION**  

Chrome Version: 107.0.5304.54 beta  

Operating System: Android 12, Pixel 4

MINIMAL POC

Open min.html. The renderer will SIGSEGV:

Thread 15 "CrRendererMain" received signal SIGSEGV, Segmentation fault.  

(gdb) i r  

...  

r1 0x2a 42  

r2 0x5f4f0000 1599012864  

...  

pc 0x3d4f6520 0x3d4f6520  

...  

(gdb) x/1i $pc  

=> 0x3d4f6520: str r1, [r2]

The 'str' instruction is the i32.store in min.wat's catch block:

i32.const 0  

i32.const 42  

i32.store

The r2 register holds the stale memory start pointer.

Tested on Pixel 4, 5, 6, dev, beta and stable and linux x64 stable.

32-BIT EXPLOIT

On a 64-bit chrome, the V8 sandbox should mitigate the immediate harm. 32-bit chrome is exploitable.

Here's an exploit for Pixel 4, which still has a 32-bit chrome. It uses the UAF to write shellcode into another wasm module's RWX code. Note that wasm code is normally W^X, but during tier-up it's temporarily switched to RWX, which suffices to corrupt it.

Open exploit.html on Pixel 4 chrome 107.0.5304.54 beta. The shellcode renames the renderer thread to "pwned":

flame:/ $ ps -AT -o CMD,CMDLINE | grep pwned  

pwned com.chrome.beta:sandboxed\_process0:org.chromium.content.app.SandboxedProcessService0:10

Reporter credit: [gzobqq@gmail.com](mailto:gzobqq@gmail.com)

## Attachments

- [min.html](attachments/min.html) (text/plain, 1.6 KB)
- [min.wat](attachments/min.wat) (application/octet-stream, 306 B)
- [exploit.html](attachments/exploit.html) (text/plain, 926 B)
- [exploit-worker.js](attachments/exploit-worker.js) (text/plain, 18.5 KB)

## Timeline

### [Deleted User] (2022-10-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-10-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5760689878794240.

### cl...@chromium.org (2022-10-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5206430526406656

Fuzzer: None
Job Type: linux32_asan_d8
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x674b0000
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux32_asan_d8&revision=83927

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5206430526406656

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2022-10-26)

Thanks for the report! I can reproduce it locally (on a 32-bit build) and Clusterfuzz also seems to be able to repro it. Now waiting for the bisecting to finish.

### cl...@chromium.org (2022-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-10-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2022-10-26)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/906459f1423e140bc789660b48143c331f183b8a (Reland "[wasm][eh] Ship exception handling").

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### th...@chromium.org (2022-10-26)

Good catch, thanks. I'll prepare the fix.

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### ti...@chromium.org (2022-10-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/f517e518af26b7eac23c9e328b463eb1e8ee3499

commit f517e518af26b7eac23c9e328b463eb1e8ee3499
Author: Thibaud Michaud <thibaudm@chromium.org>
Date: Wed Oct 26 15:03:36 2022

[wasm] Reload cached instance fields in catch handler

The memory start and size are reloaded after a call in case the call
grows the memory. We should also reload them when the call throws.

We don't need to reload in the 'delegate' case since this will be
handled by the catch handler that it delegates to.

R=jkummerow@chromium.org

Bug: chromium:1377816
Change-Id: Ied1cdb6ed83c1de6a5992df21d776aca9ccf02e6
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3982115
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83959}

[modify] https://crrev.com/f517e518af26b7eac23c9e328b463eb1e8ee3499/src/wasm/graph-builder-interface.cc


### cl...@chromium.org (2022-10-27)

ClusterFuzz testcase 5206430526406656 is verified as fixed in https://clusterfuzz.com/revisions?job=linux32_asan_d8&range=83958:83959

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-31)

This issue did not appear to get a severity or correct foundin when originally reported, added above. Also, in the interest of time, I'm going to manually add merge review labels to help ensure this fix gets backmerged in a timely manner to the correct release branches

### [Deleted User] (2022-10-31)

Merge review required: M108 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-31)

Merge review required: M107 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-31)

Merge review required: M106 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-10-31)

108 merge approved, please merge this fix to the relevant branch for M108 in the V8 repo at your earliest convenience

### sr...@google.com (2022-11-01)

This bug has been approved for M108, I am cutting beta RC for this week today around 3pm PST, please help complete your merges asap to M108 branch so they can be part of beta release this week and can get more beta coverage. 

### [Deleted User] (2022-11-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-01)

m107 and m106 merges approved, please merge this fix to the relevant v8 branches for m107 and m106 by 11am PST Friday, 4 November so this fix can be included in the next security refresh for m107/Stable and m106/Extended Stable -- thank you 

### [Deleted User] (2022-11-02)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1377816&entry.364066060=External&entry.958145677=Linux&entry.763880440=Stable&entry.1678852700=High&entry.763402679=Blink>JavaScript>Runtime&entry.975983575=thibaudm@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/4161cd30cd12905735971047f90642cb5c1e3a3b

commit 4161cd30cd12905735971047f90642cb5c1e3a3b
Author: Thibaud Michaud <thibaudm@google.com>
Date: Wed Nov 02 11:10:22 2022

Merged: [wasm] Reload cached instance fields in catch handler

Revision: f517e518af26b7eac23c9e328b463eb1e8ee3499

BUG=chromium:1377816
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jkummerow@chromium.org

Change-Id: Iaf2bad43e6b2d55fa4f5c022ed85cbc2d48b1aa3
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3999282
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.8@{#24}
Cr-Branched-From: f1bc03fd6b4c201abd9f0fd9d51fb989150f97b9-refs/heads/10.8.168@{#1}
Cr-Branched-From: 237de893e1c0a0628a57d0f5797483d3add7f005-refs/heads/main@{#83672}

[modify] https://crrev.com/4161cd30cd12905735971047f90642cb5c1e3a3b/src/wasm/graph-builder-interface.cc


### gi...@appspot.gserviceaccount.com (2022-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/77fa9d88c1e5cf3c76779703bb90b2527c4268a6

commit 77fa9d88c1e5cf3c76779703bb90b2527c4268a6
Author: Thibaud Michaud <thibaudm@chromium.org>
Date: Wed Oct 26 15:03:36 2022

Merged: [wasm] Reload cached instance fields in catch handler

R=​jkummerow@chromium.org

Bug: chromium:1377816
(cherry picked from commit f517e518af26b7eac23c9e328b463eb1e8ee3499)

Change-Id: I5f073c88feb3736acfd04af4896908f5b49678a3
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3999133
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.7@{#36}
Cr-Branched-From: 4d2145cfb13e82642cda005b2f3fc7fad8ce0f67-refs/heads/10.7.193@{#1}
Cr-Branched-From: 95216968f57b136d9ef7afbbe40c9970b2758520-refs/heads/main@{#83201}

[modify] https://crrev.com/77fa9d88c1e5cf3c76779703bb90b2527c4268a6/src/wasm/graph-builder-interface.cc


### gi...@appspot.gserviceaccount.com (2022-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/2ac0620a5bbbf23cf24b0cf531fdf342954836c1

commit 2ac0620a5bbbf23cf24b0cf531fdf342954836c1
Author: Thibaud Michaud <thibaudm@chromium.org>
Date: Wed Oct 26 15:03:36 2022

Merged: [wasm] Reload cached instance fields in catch handler

Bug: chromium:1377816
(cherry picked from commit f517e518af26b7eac23c9e328b463eb1e8ee3499)

Change-Id: I993bcff0389a1ba134e89e8ac5299d742ddd150c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3999134
Commit-Queue: Thibaud Michaud <thibaudm@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.6@{#47}
Cr-Branched-From: 41bc7435693fbce8ef86753cd9239e30550a3e2d-refs/heads/10.6.194@{#1}
Cr-Branched-From: d5f29b929ce7746409201d77f44048f3e9529b40-refs/heads/main@{#82548}

[modify] https://crrev.com/2ac0620a5bbbf23cf24b0cf531fdf342954836c1/src/wasm/graph-builder-interface.cc


### gi...@appspot.gserviceaccount.com (2022-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7722232a5bd9a54d9e3f11fbf35a8ab6af7365c0

commit 7722232a5bd9a54d9e3f11fbf35a8ab6af7365c0
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 02 18:03:25 2022

Roll v8 10.7 from 5a8a4a69ac84 to bda5eca04123 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/5a8a4a69ac84..bda5eca04123

2022-11-02 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.7.193.19
2022-11-02 thibaudm@chromium.org Merged: [wasm] Reload cached instance fields in catch handler

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-1
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.7: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m107: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1377816
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I5b9329974545d94b6aaee9974ba81f0162dc298f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3999605
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5304@{#1150}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/7722232a5bd9a54d9e3f11fbf35a8ab6af7365c0/DEPS


### gi...@appspot.gserviceaccount.com (2022-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2d8beef2433a1eaf369e21d36e125dfa0cc3356d

commit 2d8beef2433a1eaf369e21d36e125dfa0cc3356d
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 02 19:28:45 2022

Roll v8 10.6 from 35a563902756 to 11e619e5ea7a (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/35a563902756..11e619e5ea7a

2022-11-02 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.6.194.24
2022-11-02 thibaudm@chromium.org Merged: [wasm] Reload cached instance fields in catch handler

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-2
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.6: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m106: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1377816
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I7a160adb6cdbb802de85c689d67d7c7a0cf14d98
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3999683
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5249@{#900}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/2d8beef2433a1eaf369e21d36e125dfa0cc3356d/DEPS


### gi...@appspot.gserviceaccount.com (2022-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/08a1daf9080b9c25929315261aeb4521b673aae3

commit 08a1daf9080b9c25929315261aeb4521b673aae3
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Nov 02 20:44:20 2022

Roll v8 10.8 from 207d1fe27dae to 1544f19d5d03 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/207d1fe27dae..1544f19d5d03

2022-11-02 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.8.168.13
2022-11-02 thibaudm@google.com Merged: [wasm] Reload cached instance fields in catch handler

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-0
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.8: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m108: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1377816
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I35604064554a6eb3eee9a67b0930cec424cc4c84
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3999023
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#531}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/08a1daf9080b9c25929315261aeb4521b673aae3/DEPS


### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations, gzobqq! The VRP Panel has decided to award you $20,000 for this report to include the V8 exploit bonus + $1,000 bisect bonus for a total VRP reward of $21,000. Nice finding and report! Thank you for your efforts in discovering and reporting this issue to us!

### gz...@gmail.com (2022-11-03)

Great, thanks!

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-08)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-09)

[Empty comment from Monorail migration]

### ti...@google.com (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1377816?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061453)*
