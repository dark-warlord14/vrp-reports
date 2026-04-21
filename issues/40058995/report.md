# [TurboFan]v8 crashed when compling optimization

| Field | Value |
|-------|-------|
| **Issue ID** | [40058995](https://issues.chromium.org/issues/40058995) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vi...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2022-03-07 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36

Steps to reproduce the problem:
1.run the d8 with attach file: ./d8 1.js --allow-natives-syntax --expose-gc
2.
3.

What is the expected behavior?
v8 crashed

What went wrong?
crashed stack
Received signal 11 SEGV_MAPERR 7f74eca7a000

==== C stack trace ===============================

 [0x556de900299b]
 [0x7f74f87cee43]
 [0x7f74f87cebbf]
 [0x7f74efd16980]
 [0x7f74700841ae]
[end of stack trace]

Did this work before? N/A 

Chrome version: 99.0.4844.51  Channel: stable
OS Version: 10.0

test with the newest build:
https://chromium.googlesource.com/v8/v8/+/d666faeb49c1bccb2f9a5380bc3674c528ff2cf7

## Attachments

- [1.js](attachments/1.js) (text/plain, 489 B)
- [2222.PNG](attachments/2222.PNG) (image/png, 46.4 KB)

## Timeline

### [Deleted User] (2022-03-07)

[Empty comment from Monorail migration]

### vi...@gmail.com (2022-03-07)

I found the crash jit code and it crashed at address 0x7fff700841ab:
0x7fff70084180   140  4c8b4db8             REX.W movq r9,[rbp-0x48]
0x7fff70084184   144  4c8b7dc8             REX.W movq r15,[rbp-0x38]
0x7fff70084188   148  4c8b45d0             REX.W movq r8,[rbp-0x30]
0x7fff7008418c   14c  4c8b65d8             REX.W movq r12,[rbp-0x28]
                  -- B4 start (loop up to 25) --
0x7fff70084190   150  498bbd70010000       REX.W movq rdi,[r13+0x170] (root (undefined_value))
0x7fff70084197   157  48be9574440055110000 REX.W movq rsi,0x115500447495    ;; object: 0x115500447495 <NativeContext[269]>
0x7fff700841a1   161  4183f905             cmpl r9,0x5
0x7fff700841a5   165  0f84b1010000         jz 0x7fff7008435c  <+0x31c>
                  -- B5 start (in loop 4) --
0x7fff700841ab   16b  6647392478           cmpw [r8+r15*2],r12----------------------------------------------> crash here
0x7fff700841b0   170  410f95c3             setnzl r11l
0x7fff700841b4   174  450fb6db             movzxbl r11,r11
0x7fff700841b8   178  498bd9               REX.W movq rbx,r9
0x7fff700841bb   17b  83c301               addl rbx,0x1
0x7fff700841be   17e  0f80ec020000         jo 0x7fff700844b0  <+0x470>
0x7fff700841c4   184  4d8b8d98c50000       REX.W movq r9,[r13+0xc598] (external value (Heap::NewSpaceAllocationTopAddress()))
0x7fff700841cb   18b  498d514c             REX.W leaq rdx,[r9+0x4c]
0x7fff700841cf   18f  4c895dc0             REX.W movq [rbp-0x40],r11
0x7fff700841d3   193  493995a0c50000       REX.W cmpq [r13+0xc5a0] (external value (Heap::NewSpaceAllocationLimitAddress())),rdx
0x7fff700841da   19a  0f8602020000         jna 0x7fff700843e2  <+0x3a2>


### vi...@gmail.com (2022-03-07)

you can test with this build 
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-asan-linux-debug-v8-component-79377.zip?generation=1646620584003616&alt=media

### cl...@chromium.org (2022-03-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5667603854721024.

### bo...@chromium.org (2022-03-08)

Thanks for the report!

I'm unable to reproduce this crash with an ASAN d8 build from tip of tree so it may have been incidentally fixed between stable and head. We'll see if ClusterFuzz has more luck. 

In the meantime, if you can attempt to reproduce this from the tip of tree that would be helpful. 

[Monorail components: Blink>JavaScript>Compiler]

### is...@chromium.org (2022-03-09)

[Empty comment from Monorail migration]

### is...@chromium.org (2022-03-09)

[Empty comment from Monorail migration]

### is...@chromium.org (2022-03-09)

Thank you for the report!

I reproduced the issue on ToT (b953542909416a5be11220d9adf6da1aff1f009c).

out/x64.debug/d8 --allow-natives-syntax --expose-gc test.js --predictable

The issue seems to be that after gc() call the v2 array is collected by GC and its array buffer is swept and deallocated BUT the generated code at line "if (v5) {" still tries to access the array buffer of v2 via spilled value on the stack.

Simplified repro:

=== test.js ===
function main() {
  const v2 = new Int16Array(52570);
  const v5 = v2[0] != 0;
  for (let i = 0; i < 1; i++) {
    gc();
  }
  if (v5) { // <-------------- BOOM
    print("boom");
  }
}
%PrepareFunctionForOptimization(main);
main();
main();
%OptimizeFunctionOnNextCall(main);
main();

### cl...@chromium.org (2022-03-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4800143320481792.

### bo...@chromium.org (2022-03-09)

I was able to reproduce this test case using the latest ASAN v8 build d8-asan-no-inline-linux-release-v8-component-79425

### [Deleted User] (2022-03-09)

[Empty comment from Monorail migration]

### vi...@gmail.com (2022-03-10)

hello bookholt, I think this bug can be exploited by heap spary, so the severity should be high

### vi...@gmail.com (2022-03-10)

@ishell, thank you for your  description,  that's correct, I debugprint the v2 array, found the external_pointer value is same as SEGV_ACCESS address.

### cl...@chromium.org (2022-03-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5738201893109760.

### cl...@chromium.org (2022-03-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5956663273914368.

### bo...@chromium.org (2022-03-10)

@virustracker, you are correct regarding High severity as this could be leveraged for RCE in the renderer process sandbox. 

### [Deleted User] (2022-03-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2022-03-14)

I think this is caused by https://chromium-review.googlesource.com/c/v8/v8/+/3477094

### te...@chromium.org (2022-03-14)

The exploit makes use of this new optimization and doesn't reproduce anymore without it. So unless proven otherwise, I think this only affects Chrome 101, in particular not stable.

### [Deleted User] (2022-03-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/71a9fcc950f1b8efb27543961745ab0262cda7c4

commit 71a9fcc950f1b8efb27543961745ab0262cda7c4
Author: Darius Mercadier <dmercadier@chromium.org>
Date: Mon Mar 14 16:46:57 2022

Revert "[compiler] let InstructionSelector duplicate branch conditions"

This reverts commit 3d5d99ffd9bd0dd433cfdf8ba9b207648ff51ea9.

Reason for revert: causes this crash: https://bugs.chromium.org/p/chromium/issues/detail?id=1303458

Original change's description:
> [compiler] let InstructionSelector duplicate branch conditions
>
> Bug: v8:12484
> Change-Id: I44c2028efadbd70e7711f01d107995e0462f05d4
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3477094
> Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
> Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#79239}

Bug: chromium:1303458, v8:12484
Change-Id: I129467bcb2507f2fba894f5dd58304eb139f739c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3522069
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#79469}

[modify] https://crrev.com/71a9fcc950f1b8efb27543961745ab0262cda7c4/src/compiler/backend/x64/instruction-selector-x64.cc


### dm...@chromium.org (2022-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-19)

This is sufficiently serious that it should be merged to dev. I can't currently determine details for that channel, so please assess whether this is already merged.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-21)

Merge approved: your change passed merge requirements and is auto-approved for M101. Please go ahead and merge the CL to branch 4951 (refs/branch-heads/4951) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: None (Android), None (iOS), None (ChromeOS), None (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-03-22)

Your change has been approved for M101 branch,please go ahead and merge the CL's to M101 branch manually asap so that they would be part of this week's first M99 Dev release.

### dm...@chromium.org (2022-03-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-31)

Congratulations -- the VRP Panel has decided to award you $5000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### vi...@gmail.com (2022-04-19)

Hello, will this bug assign a CVE？


### am...@chromium.org (2022-04-20)

Hello-- thanks for your question. CVEs are issued when the fix is shipped in a Stable channel release. The CVE will be updated directly on the report at that time. 

### vi...@gmail.com (2022-04-20)

Thank you. So when will the CVE be given? if you assign CVE you can use this acknowlegement: Weibo Wang(@ma1fan)  at Numen Cyber Security Lab.

### am...@chromium.org (2022-04-20)

This should go out in M101 Stable on 26 April. CVE will be assigned then. And yes, we can use the information you have provided in the acknowledgments. 

### vi...@gmail.com (2022-04-27)

Hello,  I don't see this bug's CVE information at the page 26 April release announce（ https://chromereleases.googleblog.com/）

### am...@chromium.org (2022-04-27)

Apologies, I relayed the incorrect information in comments #33 and #35 as I neglected reviewing the security impact and that this issue was discovered in Head/TOT rather than impacting the Stable channel release at the time. 
Chrome's policy is normally to assign CVEs only for bugs affecting our Stable channel. We can make a one-off exception, but it will not be immediately as that is outside our normal policy and process. It also would not appear in the release notes as the release notes cover patches shipped for vulnerabilities discovered in Stable channel releases which is why it did not appear in today's release notes. Again, my apologies for the original incorrect information. 

### [Deleted User] (2022-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-06-21)

This issue was migrated from crbug.com/chromium/1303458?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058995)*
