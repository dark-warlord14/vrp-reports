# Security: Heap-buffer-overflow in AAHairlineOp::onPrepareDraws

| Field | Value |
|-------|-------|
| **Issue ID** | [40090760](https://issues.chromium.org/issues/40090760) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-03-12 |
| **Bounty** | $3,000.00 |

## Description

Heap-buffer-overflow in AAHairlineOp::onPrepareDraws

**VULNERABILITY DETAILS**  

<https://cs.chromium.org/chromium/src/third_party/skia/src/gpu/ops/GrAAHairLinePathRenderer.cpp?type=cs&l=1003>

1000 sk\_sp<const GrBuffer> quadsIndexBuffer = get\_quads\_index\_buffer(target->resourceProvider());  

1001  

1002 size\_t vertexStride = sizeof(BezierVertex);  

1003 int vertexCount = kQuadNumVertices \* quadCount + kQuadNumVertices \* conicCount;  

1004 void \*vertices = target->makeVertexSpace(vertexStride, vertexCount,  

1005 &vertexBuffer, &firstVertex);  

1006  

1007 if (!vertices || !quadsIndexBuffer) {  

1008 SkDebugf("Could not allocate vertices\n");  

1009 return;  

1010 }  

1011  

1012 // Setup vertices  

1013 BezierVertex\* bezVerts = reinterpret\_cast<BezierVertex\*>(vertices);  

1014  

1015 int unsubdivQuadCnt = quads.count() / 3;  

1016 for (int i = 0; i < unsubdivQuadCnt; ++i) {  

1017 SkASSERT(qSubdivs[i] >= 0);  

1018 add\_quads(&quads[3\*i], qSubdivs[i], toDevice, toSrc, &bezVerts);  

1019 }

In line 1003, an integer overflow will happened when quadCount is larger than 0xffffffff/5.

**VERSION**  

Chrome Version:  

Version 65.0.3325.146 (Official Build) (64-bit)  

Version 65.0.3325.146 (Developer Build) (64-bit)  

Operating System:  

Ubuntu 16.04.4 LTS

**REPRODUCTION CASE**  

run chrome with poc.html and wait it 30 seconds.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: tab Crash State: ~/Downloads/asan-linux-stable-65.0.3325.146$ ./chrome <http://localhost/chromium/skia/poc.html> ATTENTION: default value of option force\_s3tc\_enable overridden by environment. [5998:5998:0312/123056.437285:ERROR:sandbox\_linux.cc(375)] InitializeSandbox() called with multiple threads in process gpu-process.

==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7f1ce4203828 at pc 0x556112e07b65 bp 0x7ffe52c8fff0 sp 0x7ffe52c8ffe8  

WRITE of size 4 at 0x7f1ce4203828 thread T0 (chrome)  

#0 0x556112e07b64 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe213b64)  

#1 0x556112e06a10 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe212a10)  

#2 0x556112e069ac (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe2129ac)  

#3 0x556112e069ac (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe2129ac)  

#4 0x556112e069ac (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe2129ac)  

#5 0x556112e04324 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe210324)  

#6 0x556112d929d5 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe19e9d5)  

#7 0x556112d48d09 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe154d09)  

#8 0x556112d251c0 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe1311c0)  

#9 0x556112d246f4 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe1306f4)  

#10 0x556112d259e7 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe1319e7)  

#11 0x556112d11e12 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe11de12)  

#12 0x5561131b7981 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe5c3981)  

#13 0x55611abe04e3 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15fec4e3)  

#14 0x55611abd066a (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15fdc66a)  

#15 0x55611ab81c86 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15f8dc86)  

#16 0x55611ab7c2ae (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15f882ae)  

#17 0x55611ab7b233 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15f87233)  

#18 0x55611cbf9857 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x18005857)  

#19 0x55611668e7b9 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x11a9a7b9)  

#20 0x5561155a28f9 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x109ae8f9)  

#21 0x5561155a1920 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x109ad920)  

#22 0x55611578bf66 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x10b97f66)  

#23 0x5561157a07f1 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x10bac7f1)  

#24 0x556112465ccb (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd871ccb)  

#25 0x5561115ce47f (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xc9da47f)  

#26 0x5561115ccc8e (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xc9d8c8e)  

#27 0x556112465ccb (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd871ccb)  

#28 0x5561115dbfdd (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xc9e7fdd)  

#29 0x556112465ccb (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd871ccb)  

#30 0x5561124c5c85 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd8d1c85)  

#31 0x5561124c761c (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd8d361c)  

#32 0x5561124ce6b3 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd8da6b3)  

#33 0x556112546be1 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd952be1)  

#34 0x55611fca9bee (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x1b0b5bee)  

#35 0x556111a5c586 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xce68586)  

#36 0x556111a5f888 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xce6b888)  

#37 0x556111a83669 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xce8f669)  

#38 0x556111a5bda4 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xce67da4)  

#39 0x55610bf26985 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x7332985)  

#40 0x7f1d1674182f (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

0x7f1ce4203828 is located 40 bytes to the right of 536870912-byte region [0x7f1cc4203800,0x7f1ce4203800)  

allocated by thread T0 (chrome) here:  

#0 0x55610bef94ca (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x73054ca)  

#1 0x5561127c458d (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xdbd058d)  

#2 0x556112d2b3c0 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe1373c0)  

#3 0x556112d2a7e0 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe1367e0)  

#4 0x556112d2c855 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe138855)  

#5 0x556112e04216 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe210216)  

#6 0x556112d929d5 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe19e9d5)  

#7 0x556112d48d09 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe154d09)  

#8 0x556112d251c0 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe1311c0)  

#9 0x556112d246f4 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe1306f4)  

#10 0x556112d259e7 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe1319e7)  

#11 0x556112d11e12 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe11de12)  

#12 0x5561131b7981 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe5c3981)  

#13 0x55611abe04e3 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15fec4e3)  

#14 0x55611abd066a (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15fdc66a)  

#15 0x55611ab81c86 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15f8dc86)  

#16 0x55611ab7c2ae (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15f882ae)  

#17 0x55611ab7b233 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x15f87233)  

#18 0x55611cbf9857 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x18005857)  

#19 0x55611668e7b9 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x11a9a7b9)  

#20 0x5561155a28f9 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x109ae8f9)  

#21 0x5561155a1920 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x109ad920)  

#22 0x55611578bf66 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x10b97f66)  

#23 0x5561157a07f1 (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0x10bac7f1)  

#24 0x556112465ccb (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd871ccb)  

#25 0x5561115ce47f (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xc9da47f)  

#26 0x5561115ccc8e (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xc9d8c8e)  

#27 0x556112465ccb (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd871ccb)  

#28 0x5561115dbfdd (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xc9e7fdd)  

#29 0x556112465ccb (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xd871ccb)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/szj/Downloads/asan-linux-stable-65.0.3325.146/chrome+0xe213b64)  

Shadow bytes around the buggy address:  

0x0fe41c8386b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe41c8386c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe41c8386d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe41c8386e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0fe41c8386f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0fe41c838700: fa fa fa fa fa[fa]fa fa fa fa fa fa fa fa fa fa  

0x0fe41c838710: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fe41c838720: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fe41c838730: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fe41c838740: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0fe41c838750: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==1==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 419 B)

## Timeline

### cl...@chromium.org (2018-03-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4753998218002432.

### mb...@chromium.org (2018-03-12)

bsalomon: Would you mind taking a look at this or helping us find another owner?

[Monorail components: Internals>Skia]

### sh...@chromium.org (2018-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-13)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/296de50b4c2e31f94b8c3fafae8fcd7bcfb00e0b

commit 296de50b4c2e31f94b8c3fafae8fcd7bcfb00e0b
Author: Brian Salomon <bsalomon@google.com>
Date: Tue Mar 13 17:42:32 2018

Fix possible overflows in hair line path renderer vertex counts

Bug: chromium:820913
Change-Id: I77f9b40cf6173369a4a1b943d71734c305893e09
Reviewed-on: https://skia-review.googlesource.com/114140
Reviewed-by: Brian Osman <brianosman@google.com>
Commit-Queue: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/296de50b4c2e31f94b8c3fafae8fcd7bcfb00e0b/src/gpu/ops/GrAAHairLinePathRenderer.cpp


### ct...@chromium.org (2018-03-20)

bsalomon: Does the CL from #5 fix this, or is there remaining work to be done?

### [Deleted User] (2018-03-20)

[Empty comment from Monorail migration]

### [Deleted User] (2018-03-20)

Do we need to cherry pick this?

### sh...@chromium.org (2018-03-21)

[Empty comment from Monorail migration]

### ct...@chromium.org (2018-03-21)

We should probably merge this into M66 at least.

### [Deleted User] (2018-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-21)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@google.com (2018-03-21)

Has this been verified in canary?

### cl...@chromium.org (2018-03-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4604834700066816.

### ct...@chromium.org (2018-03-21)

I manually verified the crash in asan-linux-release-541902 (from before the CL in #5), and the crash did not occur in asan-linux-release-544583 (from after the CL).

I've re-uploaded the test case to clusterfuzz with a greatly increased timeout to let clusterfuzz try to verify it as well.

### cm...@google.com (2018-03-23)

[Empty comment from Monorail migration]

### [Deleted User] (2018-03-23)

Cherry-picked back to M66 here: https://skia-review.googlesource.com/c/skia/+/116184

Do we want to go back to M65 as well?

### ct...@chromium.org (2018-03-23)

Hmm yeah, probably, since this is Severity-High. The fix is small and seems safe. It wouldn't hurt to merge into M65 in case it can get picked up in a respin. Adding merge request label.

### bu...@chromium.org (2018-03-23)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/884c480d8aa569dbe21b44719ee5ff355f2518b1

commit 884c480d8aa569dbe21b44719ee5ff355f2518b1
Author: Brian Salomon <bsalomon@google.com>
Date: Fri Mar 23 16:57:51 2018

[M65 Cherry Pick] Fix possible overflows in hair line path renderer vertex counts

No-Tree-Checks: true
No-Try: true
No-Presubmit: true
Bug: chromium:820913
Change-Id: I77f9b40cf6173369a4a1b943d71734c305893e09
Reviewed-On: https://skia-review.googlesource.com/114140
Reviewed-By: Brian Osman <brianosman@google.com>
Commit-Queue: Brian Salomon <bsalomon@google.com>
Reviewed-on: https://skia-review.googlesource.com/116184
Reviewed-by: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/884c480d8aa569dbe21b44719ee5ff355f2518b1/src/gpu/ops/GrAAHairLinePathRenderer.cpp


### go...@chromium.org (2018-03-23)

+awhalley@ (Security TPM) for M65 merge review. Please note merge listed at #17 didn't got out to M66 Beta yet. Thank you.

### [Deleted User] (2018-03-23)

I will be on vacation for a week. I've prepared a cherry pick CL and locally verified it. Assigning brianosman@ to click the submit button if the merger is approved:

https://skia-review.googlesource.com/c/skia/+/116220

### aw...@google.com (2018-03-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2018-03-28)

+cc Jonathan, Kevin since it was not found in our fuzzing ? Or did we find it too with some different stack ? I think we found some crashes in AAHairlineOp ?

### kj...@chromium.org (2018-03-29)

The skia-side afl fuzzing had some flakey results from the debug GPU fuzzer that went away around the time bsaloman landed the fix.  I didn't look too much into it at the time, but now I strongly believe this was the underlying bug.

It would be nice to get the native GPU fuzzer into oss-fuzz so we can have more consistent and less noisy results.

### in...@chromium.org (2018-03-29)

Does that require a real GPU ?

### kj...@chromium.org (2018-03-29)

I think so, which may make it difficult for oss-fuzz.  metzman was looking into afl-persistant mode which was looking promising for using a native GL fuzzer Skia-side

### in...@chromium.org (2018-03-29)

We might think about https://cloud.google.com/gpu/.

### aw...@chromium.org (2018-04-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-01)

Hello! The VRP panel decided to award $3,000 for this report!  (And also kindly ask that you symbolize the stack next time :)

Also, how would you like to be credited in release notes?

### aw...@google.com (2018-04-01)

[Empty comment from Monorail migration]

### zh...@gmail.com (2018-04-02)

[Comment Deleted]

### go...@chromium.org (2018-04-06)

Rejecting merge to M65 as we're not planning any further M65 releases. 
awhalley@, Please let me know if there is any concern here. Thank you.

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/820913?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090760)*
