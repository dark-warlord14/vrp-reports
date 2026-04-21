# Security: [ANGLE] D3D11 : Integer Underflow in ElementsInBuffer results in wild copy

| Field | Value |
|-------|-------|
| **Issue ID** | [40058064](https://issues.chromium.org/issues/40058064) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | jm...@chromium.org |
| **Created** | 2021-11-29 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

When the dirty attribute is updated during the execution of the glDrawArraysInstanced function, if the storage type is static, the StoreStaticAttrib method is used. [1]

```
// static  
angle::Result VertexDataManager::StoreStaticAttrib(const gl::Context \*context,  
                                                   TranslatedAttribute \*translated)  
{  
...  
    if (staticBuffer->empty())  
    {  
        // Convert the entire buffer  
        int totalCount =  
            ElementsInBuffer(attrib, binding, static_cast<unsigned int>(bufferD3D->getSize()));  
        int startIndex = offset / static_cast<int>(ComputeVertexAttributeStride(attrib, binding));  
  
        if (totalCount > 0)  
        {  
            ANGLE_TRY(staticBuffer->storeStaticAttribute(context, attrib, binding, -startIndex,  
                                                         totalCount, 0, sourceData));  
        }  
    }  

```

In this method, if the static vertex buffer is empty, `totalCount` is calculated using the `ElementsInBuffer` function. [2]

```
// Warning: ensure the binding matches attrib.bindingIndex before using these functions.  
int ElementsInBuffer(const gl::VertexAttribute &attrib,  
                     const gl::VertexBinding &binding,  
                     unsigned int size)  
{  
    // Size cannot be larger than a GLsizei  
    if (size > static_cast<unsigned int>(std::numeric_limits<int>::max()))  
    {  
        size = static_cast<unsigned int>(std::numeric_limits<int>::max());  
    }  
  
    GLsizei stride = static_cast<GLsizei>(ComputeVertexAttributeStride(attrib, binding));  
    GLsizei offset = static_cast<GLsizei>(ComputeVertexAttributeOffset(attrib, binding));  
    return (size - offset % stride +  
            (stride - static_cast<GLsizei>(ComputeVertexAttributeTypeSize(attrib)))) /  
           stride;  
}  

```

If you look at the part that calculates the numerator in the formula of the return statement, [3]

```
(size - offset % stride + (stride - pixelBytes))  

```

`size` is the size of the buffer, `offset`, `stride`, and `pixelBytes` are the values specified in the argument of the `glVertexAttribPointer` function.

The problem is that the result of this formula can be negative.

```
size = 2  
pixelBytes = 4  
stride = 255  
offset = 254  
  
>>> (size - offset % stride + (stride - pixelBytes))  
-1  

```

In the above situation, the value of `totalCount` becomes `0x1010101`.

```
return (-1) / stride;  
  
>>> hex(int(0xffffffff/255))  
'0x1010101'  

```

Since `totalCount` is greater than 0, so `storeStaticAttribute` is called to copy the buffer.

```
  
inline void CopyNativeVertexData(const uint8_t \*input, size_t stride, size_t count, uint8_t \*output)  
{  
    const size_t attribSize = sizeof(T) \* inputComponentCount;  
...  
    if (inputComponentCount == outputComponentCount)  
    {  
        for (size_t i = 0; i < count; i++)  
        {  
            const T \*offsetInput = reinterpret_cast<const T \*>(input + (i \* stride));  
            T \*offsetOutput      = reinterpret_cast<T \*>(output) + i \* outputComponentCount;  
  
            memcpy(offsetOutput, offsetInput, attribSize);  
        }  
        return;  
    }  

```

As a result, a heap overflow occurs in the `CopyNativeVertexData` method. In the above routine, `count` is the `tocalCount` value.

This vulnerability seems to be exploitable because heap memory can be manipulated through overflow. In order to exploit, it would require some heap grooming.

An attacker can leverage this vulnerability to execute code in the GPU process, which is a higher privilege than the renderer process.

[1] <https://chromium.googlesource.com/angle/angle/+/c789169b4210f66e50f697d10dbfb2cf4a26d197/src/libANGLE/renderer/d3d/VertexDataManager.cpp#288>  

[2] <https://chromium.googlesource.com/angle/angle/+/c789169b4210f66e50f697d10dbfb2cf4a26d197/src/libANGLE/renderer/d3d/VertexDataManager.cpp#384>  

[3] <https://chromium.googlesource.com/angle/angle/+/c789169b4210f66e50f697d10dbfb2cf4a26d197/src/libANGLE/renderer/d3d/VertexDataManager.cpp#69>

**VERSION**  

Chrome Version: 96.0.4664.45 (Official Build) (64-bit) (stable)  

Chromium Version : 98.0.4737.0 (Developer Build) (64-bit) with AddressSanitizer  

Download Link : <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-945873.zip?generation=1638172382278585&alt=media>  

Operating System: [Windows]

**REPRODUCTION CASE**  

See attached files

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU Proces  

Crash State: See asan.log

**CREDIT INFORMATION**  

Reporter credit: Jaehun Jeong(@n3sk) of Theori

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 12.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [suggested_patch.diff](attachments/suggested_patch.diff) (text/plain, 2.7 KB)
- [test.log](attachments/test.log) (text/plain, 12.2 KB)

## Timeline

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2021-11-29)

PATCH

A suggested patch & test is attached, which simply modified to use the `CheckedNumeric` class and `totalCount` was made to be 0 in case of an incorrect result by calling `ValueOrDefault`.

```
diff --git a/src/libANGLE/renderer/d3d/VertexDataManager.cpp b/src/libANGLE/renderer/d3d/VertexDataManager.cpp
index 43fcdc8de..0b9dec1af 100644
--- a/src/libANGLE/renderer/d3d/VertexDataManager.cpp
+++ b/src/libANGLE/renderer/d3d/VertexDataManager.cpp
@@ -64,11 +64,13 @@ int ElementsInBuffer(const gl::VertexAttribute &attrib,
         size = static_cast<unsigned int>(std::numeric_limits<int>::max());
     }

-    GLsizei stride = static_cast<GLsizei>(ComputeVertexAttributeStride(attrib, binding));
-    GLsizei offset = static_cast<GLsizei>(ComputeVertexAttributeOffset(attrib, binding));
-    return (size - offset % stride +
-            (stride - static_cast<GLsizei>(ComputeVertexAttributeTypeSize(attrib)))) /
-           stride;
+    CheckedNumeric<GLsizei> stride = static_cast<GLsizei>(ComputeVertexAttributeStride(attrib, binding));
+    CheckedNumeric<GLsizei> offset = static_cast<GLsizei>(ComputeVertexAttributeOffset(attrib, binding));
+    CheckedNumeric<GLsizei> typeSize = static_cast<GLsizei>(ComputeVertexAttributeTypeSize(attrib));
+
+    CheckedNumeric<int> result = 
+        (size - offset % stride + (stride - typeSize)) / stride;
+    return result.ValueOrDefault(0);
 }
```

It seems that the `mBufferAccessValidationEnabled` flag needs to be turned on for testing. So I added a test to `RobustBufferAccessBehaviorTest`.


### cl...@chromium.org (2021-11-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5463324051177472.

### rs...@chromium.org (2021-11-29)

I’m unable to reproduce this locally, and Clusterfuzz can’t either. But the writeup and ASan trace seem plausible.

jmadill@: Can you take a look?

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2021-11-30)

FYI for Chrome ASan build, you need the `--no-sandbox` option to check for crashes. Also make sure your environment supports D3D11.

(from chrome://gpu)
GL_RENDERER	ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8681)

### [Deleted User] (2021-11-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/45028d2937bf85d3420886c4b1f37c6315722ba2

commit 45028d2937bf85d3420886c4b1f37c6315722ba2
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Nov 30 15:37:06 2021

D3D11: Fix OOB access in vertex conversion code.

This could happen when using certain combinations of stride and
offset. Fix the issue by using checked math.

Bug: chromium:1274499
Change-Id: Idba3beedad10b0c0cac2dcbecba8e420c5baa6da
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309035
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>

[modify] https://crrev.com/45028d2937bf85d3420886c4b1f37c6315722ba2/src/libANGLE/renderer/d3d/VertexDataManager.cpp
[modify] https://crrev.com/45028d2937bf85d3420886c4b1f37c6315722ba2/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/45028d2937bf85d3420886c4b1f37c6315722ba2/src/tests/angle_end2end_tests_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f14b5ca768b132469c21212227d597cdf11b75c7

commit f14b5ca768b132469c21212227d597cdf11b75c7
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Dec 01 02:19:56 2021

Roll ANGLE from ce854632690e to fc860bc16be3 (6 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/ce854632690e..fc860bc16be3

2021-11-30 ynovikov@chromium.org Skip *Vulkan_AsyncQueue angle_end2end_tests on TSAN
2021-11-30 bpastene@chromium.org Enable the chromium recipe RDB results experiment for all builds.
2021-11-30 jmadill@chromium.org D3D11: Fix OOB access in vertex conversion code.
2021-11-30 sugoi@google.com Vulkan: Use the correct format when binding a pBuffer.
2021-11-30 ynovikov@chromium.org Don't build dEQP tests on MSVC temporarily
2021-11-30 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from b510b0864113 to 5bf1cc589ddf (826 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1099979,chromium:1135718,chromium:1237561,chromium:1274499
Tbr: ynovikov@google.com
Change-Id: If4a910fcdfda56e7b10dcf66fd54cc028f3d055b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3309861
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#946830}

[modify] https://crrev.com/f14b5ca768b132469c21212227d597cdf11b75c7/DEPS


### jm...@chromium.org (2021-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-01)

Requesting merge to stable M96 because latest trunk commit (946830) appears to be after stable branch point (929512).

Requesting merge to beta M97 because latest trunk commit (946830) appears to be after beta branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-01)

Merge review required: a commit with DEPS changes was detected.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-01)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-12-01)

1. wild copy
2. https://chromium-review.googlesource.com/c/angle/angle/+/3309035
3. yes
4. no

### am...@chromium.org (2021-12-02)

merge approved; please merge to M96/branch 4664 by EOD today so this fix can be included in tomorrow's stable cut 

also approved for merge to M97, please merge to branch 4692 at your earliest convenience - thanks! 

### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/257c45272b7e517859bd67771265e6a51b60fc3e

commit 257c45272b7e517859bd67771265e6a51b60fc3e
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Nov 30 15:37:06 2021

D3D11: Fix OOB access in vertex conversion code.

This could happen when using certain combinations of stride and
offset. Fix the issue by using checked math.

Bug: chromium:1274499
Change-Id: Idba3beedad10b0c0cac2dcbecba8e420c5baa6da
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309035
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit 45028d2937bf85d3420886c4b1f37c6315722ba2)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3313402
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/257c45272b7e517859bd67771265e6a51b60fc3e/src/libANGLE/renderer/d3d/VertexDataManager.cpp
[modify] https://crrev.com/257c45272b7e517859bd67771265e6a51b60fc3e/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/257c45272b7e517859bd67771265e6a51b60fc3e/src/tests/angle_end2end_tests_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ba81e019e482fa415ed03be7ecde479e4b3d265e

commit ba81e019e482fa415ed03be7ecde479e4b3d265e
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Nov 30 15:37:06 2021

D3D11: Fix OOB access in vertex conversion code.

This could happen when using certain combinations of stride and
offset. Fix the issue by using checked math.

Bug: chromium:1274499
Change-Id: Idba3beedad10b0c0cac2dcbecba8e420c5baa6da
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309035
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit 45028d2937bf85d3420886c4b1f37c6315722ba2)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3313403
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/ba81e019e482fa415ed03be7ecde479e4b3d265e/src/libANGLE/renderer/d3d/VertexDataManager.cpp
[modify] https://crrev.com/ba81e019e482fa415ed03be7ecde479e4b3d265e/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/ba81e019e482fa415ed03be7ecde479e4b3d265e/src/tests/angle_end2end_tests_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/257c45272b7e517859bd67771265e6a51b60fc3e

commit 257c45272b7e517859bd67771265e6a51b60fc3e
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Nov 30 15:37:06 2021

D3D11: Fix OOB access in vertex conversion code.

This could happen when using certain combinations of stride and
offset. Fix the issue by using checked math.

Bug: chromium:1274499
Change-Id: Idba3beedad10b0c0cac2dcbecba8e420c5baa6da
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309035
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Geoff Lang <geofflang@chromium.org>
(cherry picked from commit 45028d2937bf85d3420886c4b1f37c6315722ba2)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3313402
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/257c45272b7e517859bd67771265e6a51b60fc3e/src/libANGLE/renderer/d3d/VertexDataManager.cpp
[modify] https://crrev.com/257c45272b7e517859bd67771265e6a51b60fc3e/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/257c45272b7e517859bd67771265e6a51b60fc3e/src/tests/angle_end2end_tests_expectations.txt


### ma...@google.com (2021-12-02)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-12-02)

So https://crbug.com/chromium/1274499#c18 and https://crbug.com/chromium/1274499#c19 are likely breaking the M96 and M97 windows builders - see crbug.com/1276075.

### ma...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/df0f7133799ca6aa0d31802b22d919c6197051cf

commit df0f7133799ca6aa0d31802b22d919c6197051cf
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Dec 02 21:51:03 2021

Revert "D3D11: Fix OOB access in vertex conversion code."

This reverts commit 257c45272b7e517859bd67771265e6a51b60fc3e.

Reason for revert: Depends on a CL that wasn't cherry picked.

Original change's description:
> D3D11: Fix OOB access in vertex conversion code.
>
> This could happen when using certain combinations of stride and
> offset. Fix the issue by using checked math.
>
> Bug: chromium:1274499
> Change-Id: Idba3beedad10b0c0cac2dcbecba8e420c5baa6da
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309035
> Reviewed-by: Jamie Madill <jmadill@chromium.org>
> Reviewed-by: Geoff Lang <geofflang@chromium.org>
> Commit-Queue: Geoff Lang <geofflang@chromium.org>
> (cherry picked from commit 45028d2937bf85d3420886c4b1f37c6315722ba2)
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3313402
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

Bug: chromium:1274499
Change-Id: Ie8982c2ad9dde8b1aeda712850246bb63eca6f57
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3313701
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/df0f7133799ca6aa0d31802b22d919c6197051cf/src/libANGLE/renderer/d3d/VertexDataManager.cpp
[modify] https://crrev.com/df0f7133799ca6aa0d31802b22d919c6197051cf/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/df0f7133799ca6aa0d31802b22d919c6197051cf/src/tests/angle_end2end_tests_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/db3efec73e6fb963c7c32c6376771bf97f5f6633

commit db3efec73e6fb963c7c32c6376771bf97f5f6633
Author: Jamie Madill <jmadill@chromium.org>
Date: Thu Dec 02 21:51:31 2021

Revert "D3D11: Fix OOB access in vertex conversion code."

This reverts commit ba81e019e482fa415ed03be7ecde479e4b3d265e.

Reason for revert: Depends on a CL that wasn't cherry picked.

Original change's description:
> D3D11: Fix OOB access in vertex conversion code.
>
> This could happen when using certain combinations of stride and
> offset. Fix the issue by using checked math.
>
> Bug: chromium:1274499
> Change-Id: Idba3beedad10b0c0cac2dcbecba8e420c5baa6da
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3309035
> Reviewed-by: Jamie Madill <jmadill@chromium.org>
> Reviewed-by: Geoff Lang <geofflang@chromium.org>
> Commit-Queue: Geoff Lang <geofflang@chromium.org>
> (cherry picked from commit 45028d2937bf85d3420886c4b1f37c6315722ba2)
> Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3313403
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

Bug: chromium:1274499
Change-Id: I58268c7989b07688de1dcca99502675eb95e7c1a
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3313702
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/db3efec73e6fb963c7c32c6376771bf97f5f6633/src/libANGLE/renderer/d3d/VertexDataManager.cpp
[modify] https://crrev.com/db3efec73e6fb963c7c32c6376771bf97f5f6633/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/db3efec73e6fb963c7c32c6376771bf97f5f6633/src/tests/angle_end2end_tests_expectations.txt


### jm...@chromium.org (2021-12-02)

This is still fixed in ToT.

### jm...@chromium.org (2021-12-02)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-12-02)

Thanks!

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cc44ae61f37b54fd6ad1115f06c3cc9bddeb6162

commit cc44ae61f37b54fd6ad1115f06c3cc9bddeb6162
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Jan 04 17:28:55 2022

M96: D3D11: Fix OOB access in vertex conversion code.

This could happen when using certain combinations of stride and
offset. Fix the issue by using checked math.

Bug: chromium:1274499
Change-Id: I3e286a30fe128ab4684ee5e172dc9e3345e3b2f4
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3365657
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/cc44ae61f37b54fd6ad1115f06c3cc9bddeb6162/src/libANGLE/renderer/d3d/VertexDataManager.cpp


### gi...@appspot.gserviceaccount.com (2022-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/9272f74e28630f6784fae7ef9d817e5fe91a7fbc

commit 9272f74e28630f6784fae7ef9d817e5fe91a7fbc
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Jan 04 17:28:55 2022

M97: D3D11: Fix OOB access in vertex conversion code.

This could happen when using certain combinations of stride and
offset. Fix the issue by using checked math.

Bug: chromium:1274499
Change-Id: I3e286a30fe128ab4684ee5e172dc9e3345e3b2f4
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3365656
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/9272f74e28630f6784fae7ef9d817e5fe91a7fbc/src/libANGLE/renderer/d3d/VertexDataManager.cpp


### gi...@appspot.gserviceaccount.com (2022-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cc44ae61f37b54fd6ad1115f06c3cc9bddeb6162

commit cc44ae61f37b54fd6ad1115f06c3cc9bddeb6162
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Jan 04 17:28:55 2022

M96: D3D11: Fix OOB access in vertex conversion code.

This could happen when using certain combinations of stride and
offset. Fix the issue by using checked math.

Bug: chromium:1274499
Change-Id: I3e286a30fe128ab4684ee5e172dc9e3345e3b2f4
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3365657
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>

[modify] https://crrev.com/cc44ae61f37b54fd6ad1115f06c3cc9bddeb6162/src/libANGLE/renderer/d3d/VertexDataManager.cpp


### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

Congratulations! The VRP Panel has decided to award you $7500 for this report (not $7200 as labeled above, that was a mistake :)). Thank you for your report and nice work! 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1274499?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1276075]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058064)*
