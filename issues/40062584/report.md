# UAP in  blink::WebGPUSwapBufferProvider::DiscardCurrentSwapBuffer(with --enable-unsafe-webgpu)

| Field | Value |
|-------|-------|
| **Issue ID** | [40062584](https://issues.chromium.org/issues/40062584) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | cw...@chromium.org |
| **Created** | 2023-01-10 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

ubuntu 22.04,macos 12.6  

macos  

tested chrome version:  

Chromium 110.0.5478.4  

Chromium 111.0.5521.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1089145.zip)

repro steps  

(1)python3 -m http.server 8000 |path to poc folder|  

(2)Launch Chrome with the following flags:  

./chrome /home/cowboy/asan-linux-release/chrome --user-data-dir=/tmp/x1 --use-fake-device-for-media-stream --user-data-dir=/tmp/x1 --enable-unsafe-webgpu --incognito --use-fake-ui-for-media-stream <http://localhost:8000/crash.html>  

(3) The crash(not gpu,render process) should be reproducible within a minute. I mostly reproduce memory crashes with no ASAN instrumented log, and rarely reproduce use-after-poison.

Note: Except for the --enable-unsafe-webgpu flag, the other flags are not mandatory, they are just for convenience in reproducing and testing.

**Problem Description:**  

not yet detail anlayze, but it seems like a use-after-free issue.  

WebGPUSwapBufferProvider has a raw pointer \_client[0],and it is Initialized with GPUCanvasContext[1].  

When WebGPUSwapBufferProvider is destructed, it will call \_client->ReleaseWGPUTextureAccessIfNeeded() to release the texture, but the \_client is already destructed in somewhere(I'm not quite sure where it has been released), so it will cause a use-after-free issue.

[0]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/graphics/gpu/webgpu_swap_buffer_provider.h;drc=a87e40167cf39c63a990aa2da654893ee5c627ff;l=154>  

[1]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webgpu/gpu_canvas_context.cc;drc=a87e40167cf39c63a990aa2da654893ee5c627ff;l=370>

Received signal 11 SEGV\_ACCERR 7e89007043d8  

#0 0x55f389a289b7 in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4434:13  

#1 0x55f39b56059c in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:894:7  

#2 0x55f39b2a54f2 in StackTrace ./../../base/debug/stack\_trace.cc:221:12  

#3 0x55f39b2a54f2 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:218:28  

#4 0x55f39b55ef3e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) ./../../base/debug/stack\_trace\_posix.cc:387:3  

#5 0x7f7d9a640520 in \_\_GI\_\_\_sigaction :?  

#6 0x55f3b13f7e22 in ReleaseWGPUTextureAccessIfNeeded ./../../third\_party/blink/renderer/platform/graphics/gpu/webgpu\_swap\_buffer\_provider.cc:126:12  

#7 0x55f3b13f7e22 in blink::WebGPUSwapBufferProvider::DiscardCurrentSwapBuffer() ./../../third\_party/blink/renderer/platform/graphics/gpu/webgpu\_swap\_buffer\_provider.cc:136:3  

#8 0x55f3b13f73c8 in Neuter ./../../third\_party/blink/renderer/platform/graphics/gpu/webgpu\_swap\_buffer\_provider.cc:150:3  

#9 0x55f3b13f73c8 in blink::WebGPUSwapBufferProvider::~WebGPUSwapBufferProvider() ./../../third\_party/blink/renderer/platform/graphics/gpu/webgpu\_swap\_buffer\_provider.cc:65:3  

#10 0x55f3b13f7bbd in blink::WebGPUSwapBufferProvider::~WebGPUSwapBufferProvider() ./../../third\_party/blink/renderer/platform/graphics/gpu/webgpu\_swap\_buffer\_provider.cc:64:55  

#11 0x55f3b13fc906 in DeleteInternal[blink::WebGPUSwapBufferProvider](javascript:void(0);) ./../../third\_party/blink/renderer/platform/wtf/ref\_counted.h:54:5  

#12 0x55f3b13fc906 in Destruct ./../../third\_party/blink/renderer/platform/wtf/ref\_counted.h:35:5  

#13 0x55f3b13fc906 in Release ./../../base/memory/ref\_counted.h:356:7  

#14 0x55f3b13fc906 in Release ./../../base/memory/scoped\_refptr.h:379:8  

#15 0x55f3b13fc906 in ~scoped\_refptr ./../../base/memory/scoped\_refptr.h:279:7  

#16 0x55f3b13fc906 in ~\_\_tuple\_leaf ./../../buildtools/third\_party/libc++/trunk/include/tuple:260:7  

#17 0x55f3b13fc906 in ~\_\_tuple\_impl ./../../buildtools/third\_party/libc++/trunk/include/tuple:446:37  

#18 0x55f3b13fc906 in ~tuple ./../../buildtools/third\_party/libc++/trunk/include/tuple:533:28  

#19 0x55f3b13fc906 in ~BindState ./../../base/functional/bind\_internal.h:1171:24  

#20 0x55f3b13fc906 in base::internal::BindState<void (blink::WebGPUSwapBufferProvider::\*)(scoped\_refptr[blink::WebGPUSwapBufferProvider::SwapBuffer](javascript:void(0);), gpu::SyncToken const&, bool), scoped\_refptr[blink::WebGPUSwapBufferProvider](javascript:void(0);), scoped\_refptr[blink::WebGPUSwapBufferProvider::SwapBuffer](javascript:void(0);)>::Destroy(base::internal::BindStateBase const\*) ./../../base/functional/bind\_internal.h:1174:5  

#21 0x55f3ab27cb49 in ~OnceCallback ./../../base/functional/callback.h:96:27  

#22 0x55f3ab27cb49 in blink::ExternalCanvasResource::~ExternalCanvasResource() ./../../third\_party/blink/renderer/platform/graphics/canvas\_resource.cc:822:1  

#23 0x55f3ab27cc2d in blink::ExternalCanvasResource::~ExternalCanvasResource() ./../../third\_party/blink/renderer/platform/graphics/canvas\_resource.cc:820:51  

#24 0x55f3ab272e74 in DeleteInternal[blink::CanvasResource](javascript:void(0);) ./../../third\_party/blink/renderer/platform/wtf/thread\_safe\_ref\_counted.h:65:5  

#25 0x55f3ab272e74 in Destruct ./../../third\_party/blink/renderer/platform/wtf/thread\_safe\_ref\_counted.h:45:5  

#26 0x55f3ab272e74 in Release ./../../base/memory/ref\_counted.h:418:7  

#27 0x55f3ab272e74 in blink::CanvasResource::Release() ./../../third\_party/blink/renderer/platform/graphics/canvas\_resource.cc:93:48  

#28 0x55f3ab39803b in Release ./../../base/memory/scoped\_refptr.h:379:8  

#29 0x55f3ab39803b in ~scoped\_refptr ./../../base/memory/scoped\_refptr.h:279:7  

#30 0x55f3ab39803b in ~\_\_tuple\_leaf ./../../buildtools/third\_party/libc++/trunk/include/tuple:260:7  

#31 0x55f3ab39803b in ~\_\_tuple\_impl ./../../buildtools/third\_party/libc++/trunk/include/tuple:446:37  

#32 0x55f3ab39803b in ~tuple ./../../buildtools/third\_party/libc++/trunk/include/tuple:533:28  

#33 0x55f3ab39803b in ~BindState ./../../base/functional/bind\_internal.h

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5478.4 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 2.0 KB)
- [asan-not-instrumented-crash.log](attachments/asan-not-instrumented-crash.log) (text/plain, 17.0 KB)
- [multi_video_main.js](attachments/multi_video_main.js) (text/plain, 7.2 KB)
- [multi_video_worker.js](attachments/multi_video_worker.js) (text/plain, 622 B)
- [launcher.sh](attachments/launcher.sh) (text/plain, 836 B)
- [test.html](attachments/test.html) (text/plain, 1.8 KB)

## Timeline

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6708291051913216.

### dc...@chromium.org (2023-01-14)

Hmmm... I ran it locally for over a minute and couldn't get it to crash.

asan-linux-release-1089145$ ./chrome --user-data-dir=$(mktemp -d) --use-fake-device-for-media-stream --enable-unsafe-webgpu --use-fake-ui-for-media-stream http://localhost:9000/crash.html

Am I missing anything in my setup?

### em...@gmail.com (2023-01-14)

The repro steps are correct. 
You try the script in the attachment and open multiple browsers to test it.
./launcher.sh 2>&1|grep -E "SEGV_ACCERR|use-after-free|use-after-poison"
I think the issue is related to hardware (a real pc with an NVIDIA GPU is required to reproduce it)

### em...@gmail.com (2023-01-14)

[Empty comment from Monorail migration]

### bo...@google.com (2023-01-18)

I was able to reproduce a variant of this crash, ILL_ILLOPN ...

Received signal 4 ILL_ILLOPN 55dd1ca6a0a8                                                                                                                                                                                                                                                           #0 0x55dcf2db0507 (/opt/chromium/trunk/src/out/x64.asan/chrome+0x22351506)                                                                                                                                                                                                                          
#1 0x55dd1d0fe42c (/opt/chromium/trunk/src/out/x64.asan/chrome+0x4c69f42b)                                                                                                                                                                                                                          #2 0x55dd1c9b30e4 (/opt/chromium/trunk/src/out/x64.asan/chrome+0x4bf540e3)                                                                                                                                                                                                                          #3 0x55dd1c9b2f55 (/opt/chromium/trunk/src/out/x64.asan/chrome+0x4bf53f54)                                                                                                                                                                                                                          
#4 0x55dd1d0fca4e (/opt/chromium/trunk/src/out/x64.asan/chrome+0x4c69da4d)                                                                                                                                                                                                                          
#5 0x7f7cd0a5af90 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x3bf8f)                                                                                                                                                                                                                                     
#6 0x55dd1ca6a0a8 (/opt/chromium/trunk/src/out/x64.asan/chrome+0x4c00b0a7)                                                                                                                                                                                                                          
#7 0x55dd1ca6a9f9 (/opt/chromium/trunk/src/out/x64.asan/chrome+0x4c00b9f8)                                                                                                                                                                                                                          
#8 0x55dd1c95d5f4 (/opt/chromium/trunk/src/out/x64.asan/chrome+0x4befe5f3)                                                                                                                                                                                                                          
#9 0x55dd1ccd38dd (/opt/chromium/trunk/src/out/x64.asan/chrome+0x4c2748dc)                                                                                                                                                                                                                          #10 0x55dd3c7cd23f (/opt/chromium/trunk/src/out/x64.asan/chrome+0x6bd6e23e)                                                                                                                                                                                                                         #11 0x55dd3c7cd14b (/opt/chromium/trunk/src/out/x64.asan/chrome+0x6bd6e14a)                                                                                                                                                                                                                         #12 0x55dd3c7cd110 (/opt/chromium/trunk/src/out/x64.asan/chrome+0x6bd6e10f)                                                                                                                                                                                                                         #13 0x55dd3c7cb259 (/opt/chromium/....

... but as you can see the symbolizer isn't cooperating despite me piping the output through asan_symbolize.py :-(

Due to the difficulty in reproducing this crash I'm trusting the reporter's assessment that 110 is impacted and setting FoundIn accordingly. I'm also assuming all platform on which WebGPU is (soon) shipping are affected, but have only verified Linux. 

Severity High because memory corruption in the sandboxed renderer process. 

[Monorail components: Blink>WebGPU]

### bo...@google.com (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### cw...@chromium.org (2023-01-18)

Looking at the code, it seems that the problem is that this BindOnce keeps the SwapBufferProvider alive, potentially longer than the GPUCanvasContext that could get GCed between the time we give the resource to the compositor and the time the mailbox is no longer used. The fix would be to add a finalizer to the GPUCanvasContext that severs the connection with the client, and adding checks in WebGPUSwapBufferProvider that the client is not nullptr before calling it. https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/graphics/gpu/webgpu_swap_buffer_provider.cc;drc=6cd8e5eec521e6ff5d818bf2ff336813f7fea890;l=292

I'll try to make a repro case that's more consistent with ASAN and a fix.

blundell@ FYI this callback is used to recycle shared images for the WebGPU canvas. The code wouldn't exist if we had something like a SharedImageStream concept.

### [Deleted User] (2023-01-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bl...@chromium.org (2023-01-19)

Interesting, thanks! Let's make sure to track use cases like these as design guidance and motivation for down the line.

### cw...@chromium.org (2023-01-19)

I can kinda of flackily repro with the test attached. Every other reload of that file with the devtools open crashes in ~5-10 seconds.

### gi...@appspot.gserviceaccount.com (2023-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/410d3aeadd061b15c4654012102cce45f326ab4b

commit 410d3aeadd061b15c4654012102cce45f326ab4b
Author: Corentin Wallez <cwallez@chromium.org>
Date: Thu Jan 19 21:28:41 2023

GPUCanvasContext: sever link with swap buffers on destruction

Otherwise the WebGPUSwapBufferProvider could keep a pointer to the
GPUCanvasContext and call methods on it after it was destroyed. This
happened when the WebGPUSwapBufferProvider was giving images to an
onscreen OffscreenCanvas and the GPUCanvasContext was GCed in between
the PrepareTransferrableResource and the callback that the compositor
was done with the resource (which later calls into the client).

Fix this by Neuter()ing the SwapBufferProvider in the GPUCanvasContext
destructor. It is ok to do this in the GC object destructor because
WebGPUSwapBufferProvider is not a GC object.

Fixed: chromium:1406265
Change-Id: Ib78af5ce8f32fd1ba5718043c20fa652065e2ea4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4181166
Commit-Queue: Corentin Wallez <cwallez@chromium.org>
Reviewed-by: Austin Eng <enga@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1094672}

[modify] https://crrev.com/410d3aeadd061b15c4654012102cce45f326ab4b/third_party/blink/renderer/modules/webgpu/gpu_canvas_context.h
[modify] https://crrev.com/410d3aeadd061b15c4654012102cce45f326ab4b/third_party/blink/renderer/modules/webgpu/gpu_canvas_context.cc
[modify] https://crrev.com/410d3aeadd061b15c4654012102cce45f326ab4b/third_party/blink/renderer/platform/graphics/gpu/webgpu_swap_buffer_provider.cc


### cw...@chromium.org (2023-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-20)

Merge review required: M110 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-20)

Merge review required: M109 is already shipping to stable.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### bo...@chromium.org (2023-01-23)

Somehow I missed that --enable-unsafe-webgpu was required to trigger the bug even though it's in the bug title. 

Adding SI-None due to requirement for non-standard flag. Sorry about that. 

### pg...@google.com (2023-01-23)

removing the ReleaseBlock-Stable for the new security impact

### am...@chromium.org (2023-01-23)

This would have been an RBS for M110, not M109. But not an RBS, but sheriffbot thought as such due to the original SI-Beta label. 
No m109 would have been required for this issue. 

No backmerge is needed due to that this is SI-None.



### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### cw...@chromium.org (2023-01-27)

Re https://crbug.com/chromium/1406265#c17 for M110

1. Why does your merge fit within the merge criteria for these milestones?

  Yes, it is a security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.

  https://chromium-review.googlesource.com/c/chromium/src/+/4181166

3. Have the changes been released and tested on canary?

  Yes for about a week now.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

  No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

  N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

  N/A this is for Beta

### cw...@chromium.org (2023-01-27)

Re https://crbug.com/chromium/1406265#c18 for M110

1. Why does your merge fit within the merge criteria for these milestones?

  Yes, it is a severity-high security issue.

2. What changes specifically would you like to merge? Please link to Gerrit.

  https://chromium-review.googlesource.com/c/chromium/src/+/4181166

3. Have the changes been released and tested on canary?

  Yes for about a week now.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

  No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

  N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

  No manual verification needed.

### cw...@chromium.org (2023-01-27)

Re https://crbug.com/chromium/1406265#c21, bookholt@, the report was using --enable-unsafe-webgpu, because it is on Linux, but the same issue could repro on macOS with Origin Trials, so I don't think it should be SI-None but instead SI-Stable. Please advise.

### am...@chromium.org (2023-01-27)

Thanks cwallez@, since this can repro on MacOS in OT, this should be SI-Beta since this was reproed only as back as 110 which was/is still beta. 
This fix has been on canary for a week with no discernible issues, so going ahead and approved for merge to M110. Please merge to branch 5481 at your earliest convenience. 

### ka...@chromium.org (2023-01-27)

Merge opened https://chromium-review.googlesource.com/c/chromium/src/+/4201046

### gi...@appspot.gserviceaccount.com (2023-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/59750becd22864037740c56195cca64f4c5c3913

commit 59750becd22864037740c56195cca64f4c5c3913
Author: Corentin Wallez <cwallez@chromium.org>
Date: Fri Jan 27 21:56:52 2023

GPUCanvasContext: sever link with swap buffers on destruction

Otherwise the WebGPUSwapBufferProvider could keep a pointer to the
GPUCanvasContext and call methods on it after it was destroyed. This
happened when the WebGPUSwapBufferProvider was giving images to an
onscreen OffscreenCanvas and the GPUCanvasContext was GCed in between
the PrepareTransferrableResource and the callback that the compositor
was done with the resource (which later calls into the client).

Fix this by Neuter()ing the SwapBufferProvider in the GPUCanvasContext
destructor. It is ok to do this in the GC object destructor because
WebGPUSwapBufferProvider is not a GC object.

(cherry picked from commit 410d3aeadd061b15c4654012102cce45f326ab4b)

Fixed: chromium:1406265
Change-Id: Ib78af5ce8f32fd1ba5718043c20fa652065e2ea4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4181166
Commit-Queue: Corentin Wallez <cwallez@chromium.org>
Reviewed-by: Austin Eng <enga@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1094672}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4201046
Commit-Queue: Kai Ninomiya <kainino@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5481@{#733}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/59750becd22864037740c56195cca64f4c5c3913/third_party/blink/renderer/modules/webgpu/gpu_canvas_context.h
[modify] https://crrev.com/59750becd22864037740c56195cca64f4c5c3913/third_party/blink/renderer/modules/webgpu/gpu_canvas_context.cc
[modify] https://crrev.com/59750becd22864037740c56195cca64f4c5c3913/third_party/blink/renderer/platform/graphics/gpu/webgpu_swap_buffer_provider.cc


### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1406265?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062584)*
