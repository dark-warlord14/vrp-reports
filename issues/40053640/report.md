# Security: [ANGLE] Invalid memory access in libglesv2!rx::IndexDataManager::streamIndexData

| Field | Value |
|-------|-------|
| **Issue ID** | [40053640](https://issues.chromium.org/issues/40053640) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Blink>WebGPU, Internals>GPU>ANGLE |
| **Platforms** | Fuchsia, Linux, Windows |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | jm...@chromium.org |
| **Created** | 2020-10-16 |
| **Bounty** | $15,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

When the WebGL2RenderingContext.drawRangeElements() API is processed in the ANGLE library, IndexDataManager::prepareIndexData is called internally.  

In prepareIndexData, if glBuffer is a null pointer, the second argument of streamIndexData becomes indices. This value is the last parameter(offset) of the drawRangeElements, a 4-byte integer which can be arbitrarily set.

```
// https://chromium.googlesource.com/angle/angle/+/master/src/libANGLE/renderer/d3d/IndexDataManager.cpp#163  
angle::Result IndexDataManager::prepareIndexData(const gl::Context \*context,  
                                                 gl::DrawElementsType srcType,  
                                                 gl::DrawElementsType dstType,  
                                                 GLsizei count,  
                                                 gl::Buffer \*glBuffer,  
                                                 const void \*indices,  
                                                 TranslatedIndexData \*translated)  
{  
    GLuint srcTypeBytes = gl::GetDrawElementsTypeSize(srcType);  
    GLuint srcTypeShift = gl::GetDrawElementsTypeShift(srcType);  
    GLuint dstTypeShift = gl::GetDrawElementsTypeShift(dstType);  
  
    BufferD3D \*buffer = glBuffer ? GetImplAs<BufferD3D>(glBuffer) : nullptr;  
  
    translated->indexType                 = dstType;  
    translated->srcIndexData.srcBuffer    = buffer;  
    translated->srcIndexData.srcIndices   = indices;  
    translated->srcIndexData.srcIndexType = srcType;  
    translated->srcIndexData.srcCount     = count;  
  
    // Context can be nullptr in perf tests.  
    bool primitiveRestartFixedIndexEnabled =  
        context ? context->getState().isPrimitiveRestartEnabled() : false;  
  
    // Case 1: the indices are passed by pointer, which forces the streaming of index data  
    if (glBuffer == nullptr)  
    {  
        translated->storage = nullptr;  
        return streamIndexData(context, indices, count, srcType, dstType,             // <--  
                               primitiveRestartFixedIndexEnabled, translated);  
    }  

```

The value is passed as the 3rd argument of the ConvertIndices method and used as a input pointer as follows.

```
// https://chromium.googlesource.com/angle/angle/+/master/src/libANGLE/renderer/d3d/IndexDataManager.cpp#56  
void ConvertIndices(gl::DrawElementsType sourceType,  
                    gl::DrawElementsType destinationType,  
                    const void \*input,                                                // <--  
                    GLsizei count,  
                    void \*output,  
                    bool usePrimitiveRestartFixedIndex)  
{  
    if (sourceType == destinationType)  
    {  
        const GLuint dstTypeSize = gl::GetDrawElementsTypeSize(destinationType);  
        memcpy(output, input, count \* dstTypeSize);  
        return;  
    }  
    if (sourceType == gl::DrawElementsType::UnsignedByte)  
    {  
        ASSERT(destinationType == gl::DrawElementsType::UnsignedShort);  
        ConvertIndexArray<GLubyte, GLushort>(input, sourceType, output, destinationType, count,  
                                             usePrimitiveRestartFixedIndex);  
    }  
    else if (sourceType == gl::DrawElementsType::UnsignedShort)  
    {  
        ASSERT(destinationType == gl::DrawElementsType::UnsignedInt);  
        ConvertIndexArray<GLushort, GLuint>(input, sourceType, output, destinationType, count,  
                                            usePrimitiveRestartFixedIndex);  
    }  
    else  
        UNREACHABLE();  
}  

```

Crash can appear in two forms. If sourceType and destinationType are the same, you can manipulate memcpy's source pointer.

```
memcpy(output, 0x41424344(rdi), 0x12345(r12))  
  
0:000> p  
rax=0000000000000001 rbx=0000000000000001 rcx=0000016cdbabb000  
rdx=0000000041424344 rsi=0000016cdee53690 rdi=0000016cda7e6590  
rip=00007ffcd4e7e068 rsp=00000009d27fdd30 rbp=000000000002468a  
 r8=000000000002468a  r9=0000016cda7179ac r10=0000000001000800  
r11=00000009d27fd960 r12=0000000000012345 r13=0000016cdbabb000  
r14=0000000041424344 r15=0000000000000001  
iopl=0         nv up ei pl zr na po nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246  
libglesv2!rx::`anonymous namespace'::ConvertIndices+0xe [inlined in libglesv2!rx::`anonymous namespace'::StreamInIndexBuffer+0xc8]:  
00007ffc`d4e7e068 e8c3f73b00      call    libglesv2!memcpy (00007ffc`d523d830)  
  
0:000> p  
(2558.1668): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
rax=0000016cdbabb000 rbx=0000000000000001 rcx=000000000002468a  
rdx=fffffe9365969344 rsi=0000000041424344 rdi=0000016cdbabb000  
rip=00007ffcd523d81e rsp=00000009d27fdd18 rbp=000000000002468a  
 r8=000000000002468a  r9=0000016cda7179ac r10=0000000041424344  
r11=0000016cdbabb000 r12=0000000000012345 r13=0000016cdbabb000  
r14=0000000041424344 r15=0000000000000001  
iopl=0         nv up ei pl nz na pe nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010202  
libglesv2!memcpy_repmovs+0xe:  
00007ffc`d523d81e f3a4            rep movs byte ptr [rdi],byte ptr [rsi]  

```

Another way is that if sourceType is UnsignedByte or UnsignedShort, a crash occurs by referencing the pointer in ConvertIndexArray's loop.

```
0:014> g  
(4a4.2810): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
rax=000000000000ffff rbx=0000000000000001 rcx=0000000000000000  
rdx=0000000000000100 rsi=00000000000000ff rdi=0000021ba4517a40  
rip=00007ffcd4e7e155 rsp=000000e9f3ffe050 rbp=0000000000000000  
 r8=0000021ba6cb66b0  r9=0000021ba6cb6728 r10=0000000001000800  
r11=000000e9f3ffdc80 r12=0000000000000100 r13=0000021ba6357000  
r14=0000000041424344 r15=0000000000000001  
iopl=0         nv up ei pl zr na po nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246  
libglesv2!rx::`anonymous namespace'::ConvertIndexArray+0xcd [inlined in libglesv2!rx::`anonymous namespace'::StreamInIndexBuffer+0x1b5]:  
00007ffc`d4e7e155 410fb61c2e      movzx   ebx,byte ptr [r14+rbp] ds:00000000`41424344=??  

```

This vulnerability seems to be exploitable because the source buffer and length of the memory to be copied can be arbitrarily manipulated. An attacker can leverage this vulnerability to execute code in the GPU process, which is a higher privilege than the renderer process.

I think the root cause of problem seems to be not handling errors in StateCache when the binding of the VertexArray is changed.  

When DrawElement is called, ValidateDrawElementsStates is called before the method is actually processed, where "elementArrayBuffer" is checked to see if it is bound.

```
const char \*ValidateDrawElementsStates(const Context \*context)  
{  
...  
    const VertexArray \*vao     = state.getVertexArray();  
    Buffer \*elementArrayBuffer = vao->getElementArrayBuffer();  
  
    if (elementArrayBuffer)  
    {  
...  
    }  
    else  
    {  
        // [WebGL 1.0] Section 6.2 No Client Side Arrays  
        // If an indexed draw command (drawElements) is called and no WebGLBuffer is bound to  
        // the ELEMENT_ARRAY_BUFFER binding point, an INVALID_OPERATION error is generated.  
        if (!context->getState().areClientArraysEnabled() ||  
            context->getExtensions().webglCompatibility)  
        {  
            return kMustHaveElementArrayBinding;  
        }  
    }  

```

On the first drawElement call, "element array buffer" is bound, so the check passes and the result is stored in the cache. But secondly, when drawRangeElements is called, VertexArray is created and bound before that, element array buffer is not bound to the array object.

However, when the binding is changed to VertexArray, the cache is not updated in the StateCache::onVertexArrayBindingChange, so the check passes when calling drawRangeElements, which causes the above problem. The expected patch is as follows.

```
void StateCache::onVertexArrayBindingChange(Context \*context)  
{  
    updateActiveAttribsMask(context);  
    updateVertexElementLimits(context);  
    updateBasicDrawStatesError();  
+   updateBasicDrawElementsError();  
}  

```

**VERSION**

Chrome Version: 86.0.4240.75 (Official Build) (64-bit) Stable, 87.0.4280.20 (Official Build) dev (64-bit) (cohort: Dev)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**

See attached files  

Type of crash: [GPU Process]

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Jaehun Jeong(@n3sk) of Theori

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.5 KB)
- [crash1.log](attachments/crash1.log) (text/plain, 11.2 KB)
- [crash2.log](attachments/crash2.log) (text/plain, 11.0 KB)
- [crash3.log](attachments/crash3.log) (text/plain, 6.4 KB)
- [patch_test.diff](attachments/patch_test.diff) (text/plain, 2.1 KB)

## Timeline

### ne...@nesk.kr (2020-10-18)

I added the suggested patch and test code.

In Linux, different stack traces appeared, but the bugs have the same effect.

### pa...@chromium.org (2020-10-19)

Thanks for this report!

cwallez, could you please take a look or pass this bug to someone likely? Thank you!

[Monorail components: Blink>WebGL Blink>WebGPU Internals>GPU>ANGLE]

### pa...@chromium.org (2020-10-19)

I don't know how/if this would affect Fuchsia. Wez, any thoughts?

### jm...@chromium.org (2020-10-19)

[Empty comment from Monorail migration]

### jm...@chromium.org (2020-10-19)

[Empty comment from Monorail migration]

### jm...@chromium.org (2020-10-20)

One-line fix up here: https://chromium-review.googlesource.com/c/angle/angle/+/2485581

This is in the ANGLE front-end so can also affect Linux and Fuchsia. Seems to affect stable so we'll try to merge this as far back as we can.

### [Deleted User] (2020-10-20)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/2882e1afd98253db2d6e5bb892dd3bfd3c69cb6a

commit 2882e1afd98253db2d6e5bb892dd3bfd3c69cb6a
Author: Jamie Madill <jmadill@chromium.org>
Date: Tue Oct 20 18:25:15 2020

Fix missing validation cache update on VAO binding.

Bug: chromium:1139398
Change-Id: I85a0d7a72bc2c97b07ebc5f86effd8e36aefd544
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2485581
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/2882e1afd98253db2d6e5bb892dd3bfd3c69cb6a/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/2882e1afd98253db2d6e5bb892dd3bfd3c69cb6a/src/libANGLE/Context.cpp
[modify] https://crrev.com/2882e1afd98253db2d6e5bb892dd3bfd3c69cb6a/src/libANGLE/Context.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ebd011599692527eb04ac11901ea1064dfffa153

commit ebd011599692527eb04ac11901ea1064dfffa153
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Oct 20 23:14:10 2020

Roll ANGLE from c55cd6b43d55 to 637786a9a862 (7 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/c55cd6b43d55..637786a9a862

2020-10-20 cnorthrop@google.com Tests: Add Arena of Valor trace
2020-10-20 geofflang@google.com Generate CONTEXT_LOST errors on every GL call.
2020-10-20 geofflang@google.com Add Queries and Setters for resource initialization state.
2020-10-20 courtneygo@google.com Vulkan: functionally complete worker thread
2020-10-20 jmadill@chromium.org Fix missing validation cache update on VAO binding.
2020-10-20 jmadill@chromium.org Suppress timing out GLES 31 tests on GL/Linux.
2020-10-20 syoussefi@chromium.org Vulkan: Pull generic SPIR-V transform functionality into base class

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC jonahr@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win-asan;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1132514,chromium:1137241,chromium:1139398
Tbr: jonahr@google.com
Test: Test: angle_perftest --gtest_filter="*arena*"
Change-Id: I5c86409d0607b087df8fc86d0e6f5c4386b6d4a1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2488022
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#819150}

[modify] https://crrev.com/ebd011599692527eb04ac11901ea1064dfffa153/DEPS


### jm...@chromium.org (2020-10-21)

Fixed in ToT. Will monitor in Canary a few days then request a merge back.

### [Deleted User] (2020-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-21)

Requesting merge to stable M86 because latest trunk commit (819150) appears to be after stable branch point (800218).

Requesting merge to beta M87 because latest trunk commit (819150) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-21)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2020-10-22)

jmadill@ - please address the merge questionnaire in c#13 when you are ready 

### jm...@chromium.org (2020-10-22)

 lakpamarthy@ -

1. yes, it's automated, tested in canary for 24, and safe (one line change to update a cache)
2. https://chromium-review.googlesource.com/c/angle/angle/+/2485581
3. yes
4. 86 and 87
5. security risk from invalid memory access. see description of the issue.
6. no
7. N/A

### la...@google.com (2020-10-23)

merge approved for M87 branch 4280

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ef7561d3473e09994252978f8a103912c3a99b2e

commit ef7561d3473e09994252978f8a103912c3a99b2e
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri Oct 23 17:19:45 2020

Fix missing validation cache update on VAO binding.

Bug: chromium:1139398
Change-Id: I85a0d7a72bc2c97b07ebc5f86effd8e36aefd544
(cherry picked from commit 2882e1afd98253db2d6e5bb892dd3bfd3c69cb6a)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2495289
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/ef7561d3473e09994252978f8a103912c3a99b2e/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/ef7561d3473e09994252978f8a103912c3a99b2e/src/libANGLE/Context.cpp
[modify] https://crrev.com/ef7561d3473e09994252978f8a103912c3a99b2e/src/libANGLE/Context.h


### ad...@chromium.org (2020-10-23)

I'll approve merge for M86 as we get a bit closer to the next M86 security refresh date, assuming this is still all looking good.

### ad...@google.com (2020-10-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-27)

Approving merge to M86, branch 4240, assuming this is still all looking good.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/fee4fc126724e0ae75e7eac7bdfda3de2627421e

commit fee4fc126724e0ae75e7eac7bdfda3de2627421e
Author: Jamie Madill <jmadill@chromium.org>
Date: Wed Oct 28 19:17:00 2020

Fix missing validation cache update on VAO binding.

Bug: chromium:1139398
Change-Id: I85a0d7a72bc2c97b07ebc5f86effd8e36aefd544
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2485581
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Jamie Madill <jmadill@chromium.org>
(cherry picked from commit 2882e1afd98253db2d6e5bb892dd3bfd3c69cb6a)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/2506197
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/fee4fc126724e0ae75e7eac7bdfda3de2627421e/src/tests/gl_tests/StateChangeTest.cpp
[modify] https://crrev.com/fee4fc126724e0ae75e7eac7bdfda3de2627421e/src/libANGLE/Context.cpp
[modify] https://crrev.com/fee4fc126724e0ae75e7eac7bdfda3de2627421e/src/libANGLE/Context.h


### ad...@google.com (2020-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-28)

Congratulations! The VRP panel has decided to award $15,000 for this bug. Someone from our finance team will be in touch.

### ad...@google.com (2020-10-29)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-08-19)

Hello n3sk- we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1139398?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebGL, Blink>WebGPU, Internals>GPU>ANGLE]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053640)*
