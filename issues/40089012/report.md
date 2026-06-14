# Security: heap buffer overflow in WebGLImageConversion::PackPixels

| Field | Value |
|-------|-------|
| **Issue ID** | [40089012](https://issues.chromium.org/issues/40089012) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU |
| **Platforms** | Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | zm...@chromium.org |
| **Created** | 2017-09-14 |
| **Bounty** | $3,000.00 |

## Description

This is tested on Windows 10 / Chrome Version 61.0.3163.91 (Official Build) (64-bit)

A heap buffer overflow in WebGLImageConversion::PackPixels


5:020> r
rax=0000000000000000 rbx=4141414141414141 rcx=0000039f180015a0
rdx=00000000000000a0 rsi=00007ffedd999628 rdi=0000000000000008
rip=00007ffedaaad883 rsp=0000001ef69fcd00 rbp=0000000000000001
 r8=0000000000000004  r9=0000000000000004 r10=00007ffedd9980e0
r11=000000007fffefff r12=0000000000001909 r13=0000008b24694950
r14=00007ffedd9980e0 r15=0000000000000000
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome_child!base::ByteSwap [inlined in chrome_child!WTF::PartitionAllocator::AllocateVectorBacking<std::unique_ptr<blink::ServerTimingHeader,std::default_delete<blink::ServerTimingHeader> > >+0xc3]:
00007ffe`daaad883 488b03          mov     rax,qword ptr [rbx] ds:41414141`41414141=????????????????
5:020> k
 # Child-SP          RetAddr           Call Site
00 (Inline Function) --------`-------- chrome_child!base::ByteSwap [c:\b\c\b\win64_pgo\src\base\sys_byteorder.h @ 44]
01 (Inline Function) --------`-------- chrome_child!base::ByteSwapUintPtrT [c:\b\c\b\win64_pgo\src\base\sys_byteorder.h @ 59]
02 (Inline Function) --------`-------- chrome_child!base::PartitionFreelistMask [c:\b\c\b\win64_pgo\src\base\allocator\partition_allocator\partition_alloc.h @ 501]
03 (Inline Function) --------`-------- chrome_child!base::PartitionBucketAlloc+0xb [c:\b\c\b\win64_pgo\src\base\allocator\partition_allocator\partition_alloc.h @ 670]
04 (Inline Function) --------`-------- chrome_child!base::PartitionAllocGenericFlags+0xae [c:\b\c\b\win64_pgo\src\base\allocator\partition_allocator\partition_alloc.h @ 803]
05 (Inline Function) --------`-------- chrome_child!base::PartitionAllocGeneric+0xae [c:\b\c\b\win64_pgo\src\base\allocator\partition_allocator\partition_alloc.h @ 813]
06 (Inline Function) --------`-------- chrome_child!WTF::Partitions::BufferMalloc+0xae [c:\b\c\b\win64_pgo\src\third_party\webkit\source\platform\wtf\allocator\partitions.h @ 107]
07 (Inline Function) --------`-------- chrome_child!WTF::PartitionAllocator::AllocateBacking+0xae [c:\b\c\b\win64_pgo\src\third_party\webkit\source\platform\wtf\allocator\partitionallocator.cpp @ 13]
08 0000001e`f69fcd00 00007ffe`da549a40 chrome_child!WTF::PartitionAllocator::AllocateVectorBacking<std::unique_ptr<blink::ServerTimingHeader,std::default_delete<blink::ServerTimingHeader> > >+0xc3 [c:\b\c\b\win64_pgo\src\third_party\webkit\source\platform\wtf\allocator\partitionallocator.h @ 48]
09 0000001e`f69fcd40 00007ffe`da549955 chrome_child!WTF::VectorBufferBase<unsigned char,0,WTF::PartitionAllocator>::AllocateBuffer+0x20 [c:\b\c\b\win64_pgo\src\third_party\webkit\source\platform\wtf\vector.h @ 378]
0a 0000001e`f69fcd70 00007ffe`da5498b5 chrome_child!WTF::Vector<unsigned char,0,WTF::PartitionAllocator>::ReserveCapacity+0x2d [c:\b\c\b\win64_pgo\src\third_party\webkit\source\platform\wtf\vector.h @ 1607]
0b 0000001e`f69fcdb0 00007ffe`dc8a26fb chrome_child!WTF::Vector<unsigned char,0,WTF::PartitionAllocator>::resize+0x25 [c:\b\c\b\win64_pgo\src\third_party\webkit\source\platform\wtf\vector.h @ 1552]
0c 0000001e`f69fcde0 00007ffe`dc7ba2e3 chrome_child!blink::WebGLImageConversion::ExtractTextureData+0x6f [c:\b\c\b\win64_pgo\src\third_party\webkit\source\platform\graphics\gpu\webglimageconversion.cpp @ 3047]
0d 0000001e`f69fce90 00007ffe`dc7c4869 chrome_child!blink::WebGLRenderingContextBase::TexImageHelperDOMArrayBufferView+0x21f [c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webgl\webglrenderingcontextbase.cpp @ 4641]
0e 0000001e`f69fcf70 00007ffe`dc97200a chrome_child!blink::WebGLRenderingContextBase::texImage2D+0x85 [c:\b\c\b\win64_pgo\src\third_party\webkit\source\modules\webgl\webglrenderingcontextbase.cpp @ 4686]
0f 0000001e`f69fd010 00007ffe`dc972b9c chrome_child!blink::WebGLRenderingContextV8Internal::texImage2D1Method+0x2ca [c:\b\c\b\win64_pgo\src\out\release_x64\gen\blink\bindings\modules\v8\v8webglrenderingcontext.cpp @ 2723]
10 0000001e`f69fd0f0 00007ffe`da29cce2 chrome_child!blink::WebGLRenderingContextV8Internal::texImage2DMethod+0xb0 [c:\b\c\b\win64_pgo\src\out\release_x64\gen\blink\bindings\modules\v8\v8webglrenderingcontext.cpp @ 2973]
11 (Inline Function) --------`-------- chrome_child!v8::internal::FunctionCallbackArguments::Call+0xaf [c:\b\c\b\win64_pgo\src\v8\src\api-arguments.cc @ 25]
12 0000001e`f69fd160 00007ffe`da29c98d chrome_child!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>+0x2d2 [c:\b\c\b\win64_pgo\src\v8\src\builtins\builtins-api.cc @ 112]
13 0000001e`f69fd360 00007ffe`da29c8b2 chrome_child!v8::internal::Builtin_Impl_HandleApiCall+0xcd [c:\b\c\b\win64_pgo\src\v8\src\builtins\builtins-api.cc @ 142]
14 0000001e`f69fd400 00000051`02d847a1 chrome_child!v8::internal::Builtin_HandleApiCall+0x32 [c:\b\c\b\win64_pgo\src\v8\src\builtins\builtins-api.cc @ 130]
15 0000001e`f69fd440 00000000`00000000 0x00000051`02d847a1
5:020> !lmi chrome_child.dll
Loaded Module Info: [chrome_child.dll] 
         Module: chrome_child
   Base Address: 00007ffed9ff0000
     Image Name: C:\Program Files (x86)\Google\Chrome\Application\61.0.3163.91\chrome_child.dll
   Machine Type: 34404 (X64)
     Time Stamp: 59ba3a6c Thu Sep 14 13:44:36 2017
           Size: 3d02000
       CheckSum: 3b2958a
Characteristics: 2022  
Debug Data Dirs: Type  Size     VA  Pointer
             CODEVIEW    54, 36d5200, 36d3200 RSDS - GUID: {ED508005-1CFC-4049-A121-CA890450C0AC}
               Age: 1, Pdb: C:\b\c\b\win64_pgo\src\out\Release_x64\chrome_child.dll.pdb
                   ??   5e8, 36d5254, 36d3254 [Data not mapped]
     Image Type: FILE     - Image read successfully from debugger.
                 C:\Program Files (x86)\Google\Chrome\Application\61.0.3163.91\chrome_child.dll
    Symbol Type: PDB      - Symbols loaded successfully from image path.
                 c:\symbols\chrome_child.dll.pdb\ED5080051CFC4049A121CA890450C0AC1\chrome_child.dll.pdb
       Compiler: MASM - front end [0.0 bld 0] - back end [14.0 bld 24210]
    Load Report: private symbols & lines, source indexed 
                 c:\symbols\chrome_child.dll.pdb\ED5080051CFC4049A121CA890450C0AC1\chrome_child.dll.pdb



## Attachments

- [Chrome_Stable_ByteSwap.html](attachments/Chrome_Stable_ByteSwap.html) (text/plain, 2.5 KB)

## Timeline

### cl...@chromium.org (2017-09-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6337349276663808.

### me...@chromium.org (2017-09-15)

Thanks for the report. I can repro the crash on Windows.

kbr: Do you mind taking a look and reassign if necessary? Thanks!

[Monorail components: Blink>WebGL Internals>GPU]

### kb...@chromium.org (2017-09-15)

Yes, will do. Could you assign a priority to the bug?


### me...@chromium.org (2017-09-15)

Thanks Ken! It's P1 because of severity-high. 

### zm...@chromium.org (2017-09-15)

Let me grab this from Ken.

### sh...@chromium.org (2017-09-16)

[Empty comment from Monorail migration]

### kb...@chromium.org (2017-09-16)

Thanks much Mo.


### zm...@chromium.org (2017-09-26)

This is caused by call texImage2D with invalid params (format=LUMINANCE /type=UNSIGNED_SHORT). Usually the GPU service side will catch such issues. Unfortunately, flip_y is set to true so we need to re-pack the data on the client side, and since we don't validate format/type combo on the client side, therefore in packing algorithm, we triggered a NOTREACHED() statement.  The heap buffer overflow is due to NOTREACHED() is ignored on release build therefore the codepath is unexpected.

### zm...@chromium.org (2017-09-26)

Fix is uploaded here: https://chromium-review.googlesource.com/c/chromium/src/+/685487

Conformance test is uploaded here: https://github.com/KhronosGroup/WebGL/pull/2522

### bu...@chromium.org (2017-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/73ac8f4a66c057b6b22a1c2c6e042c77ef39450d

commit 73ac8f4a66c057b6b22a1c2c6e042c77ef39450d
Author: Zhenyao Mo <zmo@chromium.org>
Date: Wed Sep 27 03:17:24 2017

Handle invalid format/type in texture uploading when FlipY/PremultiplyAlpha is set.

Currently if uploading from ArrayBuffer, NOTREACHED() will be hit in such situations
and in Release build, after hitting NOTREACHED() statement, unintended code path is taken.

BUG=765469
TEST=webgl_conformance
R=kbr@chromium.org

Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: Icf1ab03723b6c13595bd6c4dbc4e5fa40fdf9d96
Reviewed-on: https://chromium-review.googlesource.com/685487
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#504568}
[modify] https://crrev.com/73ac8f4a66c057b6b22a1c2c6e042c77ef39450d/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp
[modify] https://crrev.com/73ac8f4a66c057b6b22a1c2c6e042c77ef39450d/third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp


### zm...@chromium.org (2017-09-27)

I am not sure if we want to merge back to M61 because it's already late and this heap overflow is on the renderer side, but let me request it anyway and please advise.

### as...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-09-27)

+awhalley@ (Security TPM) for M61 merge review. The change is not yet baked in Beta.

Note: M61 is already out at 100% for Desktop and Android and we're not planning stable respin unless critical issues arise.

### sh...@chromium.org (2017-09-28)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-09-28)

Approving merge to M62. Branch:3202

### ab...@chromium.org (2017-09-28)

Removing Merge-Approved for M62.

### ab...@chromium.org (2017-09-28)

+asymmetric - can you please review if this security bug is okay to merge in M62?

### sh...@chromium.org (2017-09-28)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-10-02)

abdulsyed@ - Good for M62

### go...@chromium.org (2017-10-02)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-10-02)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-10-02)

Approving merge for M62. Branch:3202

### kb...@chromium.org (2017-10-02)

Mo's out sick today so I'll help him by doing the merge to M62.


### bu...@chromium.org (2017-10-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/81bf40a0a17d3150fd5890be9921e9926bd8bdf9

commit 81bf40a0a17d3150fd5890be9921e9926bd8bdf9
Author: Kenneth Russell <kbr@chromium.org>
Date: Mon Oct 02 22:24:28 2017

Handle invalid format/type in texture uploading when FlipY/PremultiplyAlpha is set.

Currently if uploading from ArrayBuffer, NOTREACHED() will be hit in such situations
and in Release build, after hitting NOTREACHED() statement, unintended code path is taken.

BUG=765469
TEST=webgl_conformance
R=kbr@chromium.org
TBR=zmo@chromium.org

(cherry picked from commit 73ac8f4a66c057b6b22a1c2c6e042c77ef39450d)

Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: Icf1ab03723b6c13595bd6c4dbc4e5fa40fdf9d96
Reviewed-on: https://chromium-review.googlesource.com/685487
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Zhenyao Mo <zmo@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#504568}
Reviewed-on: https://chromium-review.googlesource.com/696284
Cr-Commit-Position: refs/branch-heads/3202@{#554}
Cr-Branched-From: fa6a5d87adff761bc16afc5498c3f5944c1daa68-refs/heads/master@{#499098}
[modify] https://crrev.com/81bf40a0a17d3150fd5890be9921e9926bd8bdf9/third_party/WebKit/Source/modules/webgl/WebGLRenderingContextBase.cpp
[modify] https://crrev.com/81bf40a0a17d3150fd5890be9921e9926bd8bdf9/third_party/WebKit/Source/platform/graphics/gpu/WebGLImageConversion.cpp


### aw...@chromium.org (2017-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-06)

And $3,000 for this one, omair@!

### aw...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### kb...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/09a81d3609c63f62d4775e087cbefdd7468da170

commit 09a81d3609c63f62d4775e087cbefdd7468da170
Author: Kenneth Russell <kbr@chromium.org>
Date: Tue Nov 14 06:54:56 2017

Roll WebGL 34842fa..12192b9

https://chromium.googlesource.com/external/khronosgroup/webgl.git/+log/34842fa..12192b9

BUG=765469, 768969, 769989, 772651

TEST=bots

TBR=zmo@chromium.org, kainino@chromium.org

CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.android:android_optional_gpu_tests_rel

Cq-Include-Trybots: master.tryserver.chromium.android:android_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel
Change-Id: I180314943cb6427b916790f5ae5bf295c87330ea
Reviewed-on: https://chromium-review.googlesource.com/764818
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#516218}
[modify] https://crrev.com/09a81d3609c63f62d4775e087cbefdd7468da170/DEPS
[modify] https://crrev.com/09a81d3609c63f62d4775e087cbefdd7468da170/content/test/gpu/gpu_tests/webgl2_conformance_expectations.py
[modify] https://crrev.com/09a81d3609c63f62d4775e087cbefdd7468da170/content/test/gpu/gpu_tests/webgl_conformance_expectations.py
[modify] https://crrev.com/09a81d3609c63f62d4775e087cbefdd7468da170/content/test/gpu/gpu_tests/webgl_conformance_revision.txt


### sh...@chromium.org (2018-01-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/765469?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU]
[Monorail blocking: crbug.com/chromium/774174]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089012)*
