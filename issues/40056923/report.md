# Security: [ANGLE] Stack buffer overwrite in rx::StateManager11::syncVertexBuffersAndInputLayout

| Field | Value |
|-------|-------|
| **Issue ID** | [40056923](https://issues.chromium.org/issues/40056923) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | jm...@chromium.org |
| **Created** | 2021-08-18 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

The array `mAttribLocationToD3DSemantic` is filled with -1 (0xffffffff) during the initialization process of the `GL_LinkProgram` [1]

```
void ProgramD3D::reset()  
{  
...  
    mAttribLocationToD3DSemantic.fill(-1);  

```

During the execution of `GL_DrawArrays`, the `SortAttributesByLayout` function loads the value of this semantic array into `d3dSemantic` [2]

```
void SortAttributesByLayout(const ProgramD3D &programD3D,  
                            const std::vector<TranslatedAttribute> &vertexArrayAttribs,  
                            const std::vector<TranslatedAttribute> &currentValueAttribs,  
                            AttribIndexArray \*sortedD3DSemanticsOut,  
                            std::vector<const TranslatedAttribute \*> \*sortedAttributesOut)  
{  
    const AttribIndexArray &locationToSemantic = programD3D.getAttribLocationToD3DSemantics();  
  
    for (auto locationIndex : executable.getActiveAttribLocationsMask())  
    {  
        int d3dSemantic = locationToSemantic[locationIndex];  
        if (sortedAttributesOut->size() <= static_cast<size_t>(d3dSemantic))  
        {  
            sortedAttributesOut->resize(d3dSemantic + 1);  
        }  
  
        (\*sortedD3DSemanticsOut)[d3dSemantic] = d3dSemantic;  

```

See the last line of the code block [3], it writes a value to `sortedD3DSemanticsOut` using `d3dSemantic` as an index.  

However, this is problematic because the index value can be negative.

Since `sortedD3DSemanticsOut` is located on the stack, the upper byte of the pointer address located at index `-1` can be overwrited.

```
0:001> t  
rax=0000021c79a26750 rbx=0000021c79a5e758 rcx=0000000000000000  
rdx=0000000000000000 rsi=0000000000000008 rdi=0000021c799c3500  
rip=00007ff9b6c03059 rsp=000000d52cffdbd0 rbp=0000021c00dddfc0  
 r8=0000000000000004  r9=000000000000004f r10=0000000000000000  
r11=0000000000000246 r12=0000021c00dd21f0 r13=0000021c799c3da8  
r14=0000000000000100 r15=ffffffffffffffff                   // r15 == d3dSemantic (-1)  
iopl=0         nv up ei pl zr na po nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246  
libglesv2!rx::`anonymous namespace'::SortAttributesByLayout+0x66 [inlined in libglesv2!rx::StateManager11::syncVertexBuffersAndInputLayout+0xd9]:  
00007ff9`b6c03059 46897cbc60      mov     dword ptr [rsp+r15\*4+60h],r15d ss:000000d5`2cffdc2c=0000021c  
  
0:001> dq 000000d52cffdc28  
000000d5`2cffdc28  0000021c`00df1ac8 aaaaaaaa`aaaaaaaa  
000000d5`2cffdc38  aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa  
000000d5`2cffdc48  aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa  
000000d5`2cffdc58  aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa  
000000d5`2cffdc68  aaaaaaaa`aaaaaaaa 0000968d`4e71eab2  
000000d5`2cffdc78  00007ff9`b6c02888 0000021c`799c3500  
000000d5`2cffdc88  00000000`00000004 00000000`0000004f  
000000d5`2cffdc98  00000000`00060000 00000000`00000011  
  
0:001> t  
rax=0000021c79a26750 rbx=0000021c79a5e758 rcx=0000000000000000  
rdx=0000000000000000 rsi=0000000000000008 rdi=0000021c799c3500  
rip=00007ff9b6c0305e rsp=000000d52cffdbd0 rbp=0000021c00dddfc0  
 r8=0000000000000004  r9=000000000000004f r10=0000000000000000  
r11=0000000000000246 r12=0000021c00dd21f0 r13=0000021c799c3da8  
r14=0000000000000100 r15=ffffffffffffffff  
iopl=0         nv up ei pl zr na po nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246  
libglesv2!std::__1::vector<rx::TranslatedAttribute,std::allocator<rx::TranslatedAttribute> >::operator[] [inlined in libglesv2!rx::StateManager11::syncVertexBuffersAndInputLayout+0xde]:  
00007ff9`b6c0305e 488b0b          mov     rcx,qword ptr [rbx] ds:0000021c`79a5e758=0000021c02a4f9a0  
  
0:001> dq 000000d52cffdc28  
000000d5`2cffdc28  ffffffff`00df1ac8 aaaaaaaa`aaaaaaaa      // << modified stack value  
000000d5`2cffdc38  aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa  
000000d5`2cffdc48  aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa  
000000d5`2cffdc58  aaaaaaaa`aaaaaaaa aaaaaaaa`aaaaaaaa  
000000d5`2cffdc68  aaaaaaaa`aaaaaaaa 0000968d`4e71eab2  
000000d5`2cffdc78  00007ff9`b6c02888 0000021c`799c3500  
000000d5`2cffdc88  00000000`00000004 00000000`0000004f  
000000d5`2cffdc98  00000000`00060000 00000000`00000011  

```

This vulnerability seems to be exploitable because it can overwrite values on the stack with arbitrary values.  

An attacker can leverage this vulnerability to execute code in the GPU process, which is a higher privilege than the renderer process.

I think the patch needs to check if the index is negative or exceeds the size of the output array. Below is pseudo code and not tested.

```
void SortAttributesByLayout(const ProgramD3D &programD3D,  
                            const std::vector<TranslatedAttribute> &vertexArrayAttribs,  
                            const std::vector<TranslatedAttribute> &currentValueAttribs,  
                            AttribIndexArray \*sortedD3DSemanticsOut,  
                            std::vector<const TranslatedAttribute \*> \*sortedAttributesOut)  
{  
    const AttribIndexArray &locationToSemantic = programD3D.getAttribLocationToD3DSemantics();  
  
    for (auto locationIndex : executable.getActiveAttribLocationsMask())  
    {  
        int d3dSemantic = locationToSemantic[locationIndex];  
        if (sortedAttributesOut->size() <= static_cast<size_t>(d3dSemantic))  
        {  
            sortedAttributesOut->resize(d3dSemantic + 1);  
        }  
  
+       if((d3dSemantic < 0) || (d3dSemantic >= sortedD3DSemanticsOut.size()))  
+       {  
+           continue;  
+       }  
  
        (\*sortedD3DSemanticsOut)[d3dSemantic] = d3dSemantic;  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/ProgramD3D.cpp;l=3040;drc=7e040640ef1ce4dcc2c7b17c851b2536129405e1>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/d3d11/StateManager11.cpp;l=201;drc=7e040640ef1ce4dcc2c7b17c851b2536129405e1>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/renderer/d3d/d3d11/StateManager11.cpp;l=207;drc=7e040640ef1ce4dcc2c7b17c851b2536129405e1>

**VERSION**  

Chrome Version: 95.0.4613.0 (Developer Build) (64-bit) (Asan Build)  

Revision: ef56d63d56f5d73a5d84259688f1dccd12c56713-refs/heads/master@{#912887}  

Download Link: <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-912887.zip?generation=1629264469780369&alt=media>  

Operating System: Windows 10 OS Version 2009 (Build 19042.1110)

**REPRODUCTION CASE**  

See attached files

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU Proces  

Crash State: See asan.log

**CREDIT INFORMATION**  

Reporter credit: Jaehun Jeong(@n3sk) of Theori

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 7.0 KB)
- [patch_test.diff](attachments/patch_test.diff) (text/plain, 1.9 KB)
- [test.asan.log](attachments/test.asan.log) (text/plain, 7.0 KB)
- [patch_test.diff](attachments/patch_test.diff) (text/plain, 1.9 KB)

## Timeline

### [Deleted User] (2021-08-18)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2021-08-19)

I added the suggested patch and test code. But my fix throw the below error.

```
[ RUN      ] WebGL2ValidationStateChangeTest.SortNegativeD3DSemantics/ES3_D3D11
Warning: Debug.cpp:180 (insertMessage): GL error: HIGH: Internal D3D11 error: HRESULT: 0x80070057: Error allocating InputLayout
[       OK ] WebGL2ValidationStateChangeTest.SortNegativeD3DSemantics/ES3_D3D11 (85 ms)
[----------] 1 test from WebGL2ValidationStateChangeTest (88 ms total)
```

### ne...@nesk.kr (2021-08-19)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2021-08-20)

I added the suggested patch and test code. But my fix throw the below error.

```
[ RUN      ] WebGL2ValidationStateChangeTest.SortNegativeD3DSemantics/ES3_D3D11
Warning: Debug.cpp:180 (insertMessage): GL error: HIGH: Internal D3D11 error: HRESULT: 0x80070057: Error allocating InputLayout
[       OK ] WebGL2ValidationStateChangeTest.SortNegativeD3DSemantics/ES3_D3D11 (85 ms)
[----------] 1 test from WebGL2ValidationStateChangeTest (88 ms total)
```

### dr...@chromium.org (2021-08-26)

jmadill@ - can you take a look?

[Monorail components: Internals>GPU>ANGLE]

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-02)

jmadill: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-09-03)

+more ANGLE folks, can something please investigate this? Thanks!

### do...@chromium.org (2021-09-03)

Actually +more ANGLE folks, can someone please take a look at this?

### jm...@chromium.org (2021-09-03)

I'll look, sorry for the delay.

### jm...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### jm...@chromium.org (2021-09-03)

Fix in progress, and opened WebGL issue: https://github.com/KhronosGroup/WebGL/issues/3331

### jm...@chromium.org (2021-09-03)

ANGLE fix blocked on Chromium CL that also will need to roll into ANGLE, then the ANGLE fix will need to roll in Chrome

https://chromium-review.googlesource.com/c/angle/angle/+/3140496
https://chromium-review.googlesource.com/c/chromium/src/+/3138657

### gi...@appspot.gserviceaccount.com (2021-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8ef1e4544ed5214608039d969940347d8f98e543

commit 8ef1e4544ed5214608039d969940347d8f98e543
Author: Yuly Novikov <ynovikov@chromium.org>
Date: Fri Sep 03 22:51:47 2021

Skip WebGL conformance/programs/program-test.html on all platforms

To unblock ANGLE CL http://crrev.com/c/3140496, which modifies behaviour
to make it an error to draw after the current program fails to re-link.

Bug: 1241123
Bug: angleproject:6358
Change-Id: I40a1f4843f902533745cc9527379def9d777a578
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140226
Auto-Submit: Yuly Novikov <ynovikov@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#918281}

[modify] https://crrev.com/8ef1e4544ed5214608039d969940347d8f98e543/content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
[modify] https://crrev.com/8ef1e4544ed5214608039d969940347d8f98e543/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-09-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/3ae1f33606d674e81aeda7f952b190332955d8ba

commit 3ae1f33606d674e81aeda7f952b190332955d8ba
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri Sep 03 13:34:10 2021

WebGL: Make unsuccessful links fail subsequent draw calls.

This protects against incomplete state updates during a failed
link call that can interfere with draw calls.

Bug: angleproject:6358
Bug: chromium:1241123
Change-Id: Ie892654c3a58c69d6e35ba3c41758ab6269d8193
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3140496
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>

[modify] https://crrev.com/3ae1f33606d674e81aeda7f952b190332955d8ba/src/libANGLE/validationES.cpp
[modify] https://crrev.com/3ae1f33606d674e81aeda7f952b190332955d8ba/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/3ae1f33606d674e81aeda7f952b190332955d8ba/src/tests/gl_tests/GLSLTest.cpp


### gi...@appspot.gserviceaccount.com (2021-09-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/13813150f6d357dea403b16b8162a1e813f782ab

commit 13813150f6d357dea403b16b8162a1e813f782ab
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Sep 04 05:17:14 2021

Roll ANGLE from ab187c35b601 to 3ae1f33606d6 (2 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/ab187c35b601..3ae1f33606d6

2021-09-04 jmadill@chromium.org WebGL: Make unsuccessful links fail subsequent draw calls.
2021-09-04 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from f60c2130504a to 8ef1e4544ed5 (272 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC geofflang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win-asan;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1241123
Tbr: geofflang@google.com
Change-Id: Id29fccfd4a079c83a961dc2a66519819fa37aa74
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3142263
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#918352}

[modify] https://crrev.com/13813150f6d357dea403b16b8162a1e813f782ab/DEPS


### kb...@chromium.org (2021-09-05)

[Empty comment from Monorail migration]

### kb...@chromium.org (2021-09-05)

[Empty comment from Monorail migration]

### kb...@chromium.org (2021-09-05)

Apple, Mozilla folks - you'll probably want to cherry-pick the above fix. It's known only to affect the D3D backend but perhaps other backends haven't been investigated yet.

### jm...@chromium.org (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

Requesting merge to extended stable M92 because latest trunk commit (918352) appears to be after extended stable branch point (885287).

Requesting merge to stable M93 because latest trunk commit (918352) appears to be after stable branch point (902210).

Requesting merge to beta M94 because latest trunk commit (918352) appears to be after beta branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-08)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jm...@chromium.org (2021-09-08)

1. yes
2. https://chromium-review.googlesource.com/c/angle/angle/+/3140496 and https://chromium-review.googlesource.com/c/chromium/src/+/3140226
3. yes
4. M93
5. stack buffer overwrite in GPU process
6. no
7. n/a

### sr...@google.com (2021-09-08)

Merge approved for M94 branch:4606 pls merge asap

### am...@chromium.org (2021-09-08)

Merge approved for M93, please merge to branch 4577 by 2pm PDT tomorrow (Thursday), 9 September so this can be included in next week's stable security refresh. 
Also, please merge to M92 (branch 4515) so this can be included in the Extended stable channel as we transition to the 4W stable channel release cycle. Thank you. 


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5e71bf44897b6741994978e25315f7936ba848d5

commit 5e71bf44897b6741994978e25315f7936ba848d5
Author: Yuly Novikov <ynovikov@chromium.org>
Date: Thu Sep 09 19:57:17 2021

Skip WebGL conformance/programs/program-test.html on all platforms

To unblock ANGLE CL http://crrev.com/c/3140496, which modifies behaviour
to make it an error to draw after the current program fails to re-link.

(cherry picked from commit 8ef1e4544ed5214608039d969940347d8f98e543)

Bug: 1241123
Bug: angleproject:6358
Change-Id: I40a1f4843f902533745cc9527379def9d777a578
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140226
Auto-Submit: Yuly Novikov <ynovikov@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/heads/main@{#918281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3149375
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#898}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/5e71bf44897b6741994978e25315f7936ba848d5/content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
[modify] https://crrev.com/5e71bf44897b6741994978e25315f7936ba848d5/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/13842c96c2926db7b11c6851d959bc88d76956f3

commit 13842c96c2926db7b11c6851d959bc88d76956f3
Author: Yuly Novikov <ynovikov@chromium.org>
Date: Thu Sep 09 20:00:43 2021

Skip WebGL conformance/programs/program-test.html on all platforms

To unblock ANGLE CL http://crrev.com/c/3140496, which modifies behaviour
to make it an error to draw after the current program fails to re-link.

(cherry picked from commit 8ef1e4544ed5214608039d969940347d8f98e543)

Bug: 1241123
Bug: angleproject:6358
Change-Id: I40a1f4843f902533745cc9527379def9d777a578
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140226
Auto-Submit: Yuly Novikov <ynovikov@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/heads/main@{#918281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3150594
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#2117}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/13842c96c2926db7b11c6851d959bc88d76956f3/content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
[modify] https://crrev.com/13842c96c2926db7b11c6851d959bc88d76956f3/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d5be352cb121d3836b075f500ae7977ad0d9b8fa

commit d5be352cb121d3836b075f500ae7977ad0d9b8fa
Author: Yuly Novikov <ynovikov@chromium.org>
Date: Thu Sep 09 20:00:08 2021

Skip WebGL conformance/programs/program-test.html on all platforms

To unblock ANGLE CL http://crrev.com/c/3140496, which modifies behaviour
to make it an error to draw after the current program fails to re-link.

(cherry picked from commit 8ef1e4544ed5214608039d969940347d8f98e543)

Bug: 1241123
Bug: angleproject:6358
Change-Id: I40a1f4843f902533745cc9527379def9d777a578
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140226
Auto-Submit: Yuly Novikov <ynovikov@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/heads/main@{#918281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3149576
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#1223}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/d5be352cb121d3836b075f500ae7977ad0d9b8fa/content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
[modify] https://crrev.com/d5be352cb121d3836b075f500ae7977ad0d9b8fa/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/13842c96c2926db7b11c6851d959bc88d76956f3

commit 13842c96c2926db7b11c6851d959bc88d76956f3
Author: Yuly Novikov <ynovikov@chromium.org>
Date: Thu Sep 09 20:00:43 2021

Skip WebGL conformance/programs/program-test.html on all platforms

To unblock ANGLE CL http://crrev.com/c/3140496, which modifies behaviour
to make it an error to draw after the current program fails to re-link.

(cherry picked from commit 8ef1e4544ed5214608039d969940347d8f98e543)

Bug: 1241123
Bug: angleproject:6358
Change-Id: I40a1f4843f902533745cc9527379def9d777a578
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140226
Auto-Submit: Yuly Novikov <ynovikov@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/heads/main@{#918281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3150594
Auto-Submit: Jamie Madill <jmadill@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#2117}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/13842c96c2926db7b11c6851d959bc88d76956f3/content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
[modify] https://crrev.com/13842c96c2926db7b11c6851d959bc88d76956f3/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/018f85dea11fd5e41725750c6958695a6b8e8409

commit 018f85dea11fd5e41725750c6958695a6b8e8409
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri Sep 03 13:34:10 2021

WebGL: Make unsuccessful links fail subsequent draw calls.

This protects against incomplete state updates during a failed
link call that can interfere with draw calls.

Bug: angleproject:6358
Bug: chromium:1241123
Change-Id: Ie892654c3a58c69d6e35ba3c41758ab6269d8193
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3140496
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3152556
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/018f85dea11fd5e41725750c6958695a6b8e8409/src/libANGLE/validationES.cpp


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/e32351083626d20ef50be7a2141b6b47deb04807

commit e32351083626d20ef50be7a2141b6b47deb04807
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri Sep 03 13:34:10 2021

WebGL: Make unsuccessful links fail subsequent draw calls.

This protects against incomplete state updates during a failed
link call that can interfere with draw calls.

Bug: angleproject:6358
Bug: chromium:1241123
Change-Id: Ie892654c3a58c69d6e35ba3c41758ab6269d8193
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3140496
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3150262
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/e32351083626d20ef50be7a2141b6b47deb04807/src/libANGLE/validationES.cpp


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/cd251c370d4b5ce1573680a323e091ef74c6eca8

commit cd251c370d4b5ce1573680a323e091ef74c6eca8
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri Sep 03 13:34:10 2021

WebGL: Make unsuccessful links fail subsequent draw calls.

This protects against incomplete state updates during a failed
link call that can interfere with draw calls.

Bug: angleproject:6358
Bug: chromium:1241123
Change-Id: Ie892654c3a58c69d6e35ba3c41758ab6269d8193
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3140496
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3152555
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/cd251c370d4b5ce1573680a323e091ef74c6eca8/src/libANGLE/validationES.cpp


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/e32351083626d20ef50be7a2141b6b47deb04807

commit e32351083626d20ef50be7a2141b6b47deb04807
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri Sep 03 13:34:10 2021

WebGL: Make unsuccessful links fail subsequent draw calls.

This protects against incomplete state updates during a failed
link call that can interfere with draw calls.

Bug: angleproject:6358
Bug: chromium:1241123
Change-Id: Ie892654c3a58c69d6e35ba3c41758ab6269d8193
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3140496
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3150262
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/e32351083626d20ef50be7a2141b6b47deb04807/src/libANGLE/validationES.cpp


### am...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-13)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/326b4628e56f798a2a7e87249bfa7f9145482280

commit 326b4628e56f798a2a7e87249bfa7f9145482280
Author: Jamie Madill <jmadill@chromium.org>
Date: Fri Sep 03 13:34:10 2021

[M90-LTS] WebGL: Make unsuccessful links fail subsequent draw calls.

M90-LTS comment: merge conflicts were resolved using other cherry-picks
of this CL as an example.

This protects against incomplete state updates during a failed
link call that can interfere with draw calls.

Bug: angleproject:6358
Bug: chromium:1241123
Change-Id: Ie892654c3a58c69d6e35ba3c41758ab6269d8193
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3140496
Reviewed-by: Geoff Lang <geofflang@chromium.org>
Commit-Queue: Yuly Novikov <ynovikov@chromium.org>
(cherry picked from commit 3ae1f33606d674e81aeda7f952b190332955d8ba)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3160210
Reviewed-by: Jamie Madill <jmadill@chromium.org>

[modify] https://crrev.com/326b4628e56f798a2a7e87249bfa7f9145482280/src/libANGLE/validationES.cpp


### am...@google.com (2021-09-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-15)

Congratulations! The VRP Panel has decided to award you $7500 for this report. Thank you for this report and nice work! 

### gi...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d272bf701fe2a448f58d6bcaecb0134a2acb9a7c

commit d272bf701fe2a448f58d6bcaecb0134a2acb9a7c
Author: Yuly Novikov <ynovikov@chromium.org>
Date: Thu Sep 16 12:38:23 2021

[M90-LTS] Skip WebGL conformance/programs/program-test.html on all platforms

To unblock ANGLE CL http://crrev.com/c/3140496, which modifies behaviour
to make it an error to draw after the current program fails to re-link.

(cherry picked from commit 8ef1e4544ed5214608039d969940347d8f98e543)

Bug: 1241123
Bug: angleproject:6358
Change-Id: I40a1f4843f902533745cc9527379def9d777a578
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140226
Auto-Submit: Yuly Novikov <ynovikov@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/heads/main@{#918281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3160640
Reviewed-by: Yuly Novikov <ynovikov@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1608}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/d272bf701fe2a448f58d6bcaecb0134a2acb9a7c/content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
[modify] https://crrev.com/d272bf701fe2a448f58d6bcaecb0134a2acb9a7c/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt


### vo...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-12-20)

Hello nesk@, we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### gi...@appspot.gserviceaccount.com (2022-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0c51b54c2ff10a9e35144e4359825abd7246510f

commit 0c51b54c2ff10a9e35144e4359825abd7246510f
Author: Kenneth Russell <kbr@chromium.org>
Date: Tue Feb 01 03:31:37 2022

Roll WebGL b1f3776..cf04aeb

https://chromium.googlesource.com/external/khronosgroup/webgl.git/+log/b1f3776..cf04aeb

Removed suppression for program-test.html on passthrough command
decoder.

Bug: angleproject:6358
Bug: 1241123
Bug: 1290867
Cq-Include-Trybots: luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-angle-rel
Change-Id: I4fbea250763c745847429e3027fed75392b46c69
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3426788
Reviewed-by: Austin Eng <enga@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#965514}

[modify] https://crrev.com/0c51b54c2ff10a9e35144e4359825abd7246510f/content/test/gpu/gpu_tests/test_expectations/webgl2_conformance_expectations.txt
[modify] https://crrev.com/0c51b54c2ff10a9e35144e4359825abd7246510f/content/test/gpu/gpu_tests/test_expectations/webgl_conformance_expectations.txt
[modify] https://crrev.com/0c51b54c2ff10a9e35144e4359825abd7246510f/DEPS
[modify] https://crrev.com/0c51b54c2ff10a9e35144e4359825abd7246510f/content/test/gpu/gpu_tests/webgl_conformance_revision.txt


### kb...@chromium.org (2022-03-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1241123?no_tracker_redirect=1

[Monorail blocking: crbug.com/angleproject/6358, crbug.com/chromium/953120]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056923)*
