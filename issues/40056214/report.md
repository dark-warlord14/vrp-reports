# AddressSanitizer: heap-buffer-overflow on gpu::CopyArraysToBuffer transfer_buffer_cmd_copy_helpers.h:80

| Field | Value |
|-------|-------|
| **Issue ID** | [40056214](https://issues.chromium.org/issues/40056214) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>Internals |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | sh...@google.com |
| **Created** | 2021-06-15 |
| **Bounty** | $8,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4494.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
Liunx x64

asan-linux-stable-91.0.4472.77
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-891552.zip

#Reproduce
python -m http.server 8000
chrome.exe http://localhost:8000/mini.html

What is the expected behavior?

What went wrong?
Type of crash
tab

Did this work before? N/A 

Chrome version: 92.0.4494.0  Channel: n/a
OS Version: 10.0

#Analysis
come soon

#patch
come soon

=================================================================
==4176==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x1022806bf140 at pc 0x7ff68045699f bp 0x00003fd6c2d0 sp 0x00003fd6c318
READ of size 252 at 0x1022806bf140 thread T33
==4176==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff68045699e in __asan_memcpy C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:22
    #1 0x7ffc1dc0a07f in gpu::CopyArraysToBuffer<const int,const int,const int> C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\client\transfer_buffer_cmd_copy_helpers.h:80
    #2 0x7ffc1dbb671f in gpu::gles2::GLES2Implementation::MultiDrawArraysInstancedWEBGLHelper C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\client\gles2_implementation.cc:2622
    #3 0x7ffc1dbbae3d in gpu::gles2::GLES2Implementation::MultiDrawArraysInstancedWEBGL C:\b\s\w\ir\cache\builder\src\gpu\command_buffer\client\gles2_implementation.cc:2799
    #4 0x7ffc2bf9f955 in blink::WebGLMultiDraw::multiDrawArraysInstancedImpl C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webgl\webgl_multi_draw.cc:110
    #5 0x7ffc2ccc0e03 in blink::WebGLMultiDraw::multiDrawArraysInstancedWEBGL C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webgl\webgl_multi_draw.h:57
    #6 0x7ffc2ccbe52a in blink::`anonymous namespace'::v8_webgl_multi_draw::MultiDrawArraysInstancedWEBGLOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_webgl_multi_draw.cc:133
    #7 0x7ffc18a1b27d in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:156
    #8 0x7ffc18a1838d in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #9 0x7ffc18a157c1 in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
    #10 0x7ffc18a14abe in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #11 0x7eca000bc01b  (<unknown module>)

0x1022806bf140 is located 0 bytes to the right of 256-byte region [0x1022806bf040,0x1022806bf140)
allocated by thread T33 here:
    #0 0x7ff6804570c1 in calloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:114
    #1 0x7ffc1ee6ad88 in blink::ArrayBufferContents::AllocateMemoryWithFlags C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\typed_arrays\array_buffer\array_buffer_contents.cc:134
    #2 0x7ffc24c7d761 in blink::`anonymous namespace'::ArrayBufferAllocator::Allocate C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\bindings\core\v8\v8_initializer.cc:697
    #3 0x7ffc18f06ce9 in v8::internal::Heap::AllocateExternalBackingStore C:\b\s\w\ir\cache\builder\src\v8\src\heap\heap.cc:3022
    #4 0x7ffc1933f597 in v8::internal::BackingStore::Allocate C:\b\s\w\ir\cache\builder\src\v8\src\objects\backing-store.cc:258
    #5 0x7ffc18a3b55e in v8::internal::`anonymous namespace'::ConstructBuffer C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-arraybuffer.cc:85
    #6 0x7ffc18a35f1f in v8::internal::Builtin_Impl_ArrayBufferConstructor C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-arraybuffer.cc:162
    #7 0x7ffc18a3503e in v8::internal::Builtin_ArrayBufferConstructor C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-arraybuffer.cc:136
    #8 0x7eca000bc01b  (<unknown module>)

Thread T33 created by T0 here:
    #0 0x7ff6804616b2 in __asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
    #1 0x7ffc1ca936fe in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:185
    #2 0x7ffc1ca0db8a in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:200
    #3 0x7ffc16b7e2af in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1967
    #4 0x7ffc16b60ea8 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2812
    #5 0x7ffc16b58511 in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3047
    #6 0x7ffc16b55d9e in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1066
    #7 0x7ffc16b54910 in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:821
    #8 0x7ffc168d7a05 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:523
    #9 0x7ffc16a8d2a9 in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:577
    #10 0x7ffc16a0496c in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3256
    #11 0x7ffc16a03aac in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1138
    #12 0x7ffc1ebb3646 in `anonymous namespace'::LoadURLInContents C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:387
    #13 0x7ffc1ebb09f8 in Navigate C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_navigator.cc:659
    #14 0x7ffc26161c77 in StartupBrowserCreatorImpl::OpenTabsInBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:312
    #15 0x7ffc26163a6f in StartupBrowserCreatorImpl::RestoreOrCreateBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:583
    #16 0x7ffc26160e01 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:428
    #17 0x7ffc2616047c in StartupBrowserCreatorImpl::Launch C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator_impl.cc:216
    #18 0x7ffc220f8c34 in StartupBrowserCreator::LaunchBrowser C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:589
    #19 0x7ffc220fbbb7 in StartupBrowserCreator::ProcessLastOpenedProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1203
    #20 0x7ffc220fac9c in StartupBrowserCreator::LaunchBrowserForLastProfiles C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:683
    #21 0x7ffc220fea24 in StartupBrowserCreator::StartupLaunchAfterProtocolHandler C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1154
    #22 0x7ffc220f80d0 in StartupBrowserCreator::ProcessCmdLineImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1114
    #23 0x7ffc220f66ab in StartupBrowserCreator::Start C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:524
    #24 0x7ffc1f259644 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1689
    #25 0x7ffc1f2570c0 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome_browser_main.cc:1063
    #26 0x7ffc1606d21c in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:949
    #27 0x7ffc16e2c7d7 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
    #28 0x7ffc1606c722 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:857
    #29 0x7ffc16074145 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
    #30 0x7ffc16068ce8 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
    #31 0x7ffc1c6d77ec in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:598
    #32 0x7ffc1c6da148 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1087
    #33 0x7ffc1c6d92fe in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:956
    #34 0x7ffc1c6d6676 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:386
    #35 0x7ffc1c6d6c8f in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:412
    #36 0x7ffc1246145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:151
    #37 0x7ff6803b5bb4 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:169
    #38 0x7ff6803b2be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:381
    #39 0x7ff68079fbff in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #40 0x7ffca9084d2d in BaseThreadInitThunk+0x1d (C:\WINDOWS\System32\KERNEL32.DLL+0x180014d2d)
    #41 0x7ffcaa9d5a7a in RtlUserThreadStart+0x2a (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180065a7a)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:22 in __asan_memcpy
Shadow bytes around the buggy address:
  0x0204d00d7dd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0204d00d7de0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0204d00d7df0: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa
  0x0204d00d7e00: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x0204d00d7e10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0204d00d7e20: 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa fa fa
  0x0204d00d7e30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0204d00d7e40: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x0204d00d7e50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0204d00d7e60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0204d00d7e70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==4176==ABORTING

## Attachments

- [mini.html](attachments/mini.html) (text/plain, 982 B)
- [asan.txt](attachments/asan.txt) (text/plain, 10.9 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 779 B)

## Timeline

### [Deleted User] (2021-06-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-06-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5677026974171136.

### m....@gmail.com (2021-06-16)

#analysis
The root cause of this issue is that WebGLMultiDraw::multiDrawArraysInstancedImpl[1] calls WebGLMultiDrawCommon::ValidateArray[2] to check whether the array access in the parameter is out of bounds, but they check drawcount and offset separately without considering the situation of drawcount+offset, resulting in access Out of bounds.

[1]third_party/blink/renderer/modules/webgl/webgl_multi_draw.cc:83
[2]third_party/blink/renderer/modules/webgl/webgl_multi_draw_common.cc:24

#Patch
diff --git a/third_party/blink/renderer/modules/webgl/webgl_multi_draw_common.cc b/third_party/blink/renderer/modules/webgl/webgl_multi_draw_common.cc
index e0da2d4c898..36cc36268bf 100644
--- a/third_party/blink/renderer/modules/webgl/webgl_multi_draw_common.cc
+++ b/third_party/blink/renderer/modules/webgl/webgl_multi_draw_common.cc
@@ -34,6 +34,12 @@ bool WebGLMultiDrawCommon::ValidateArray(WebGLExtensionScopedContext* scoped,
                                          outOfBoundsDescription);
     return false;
   }
+  
+  if (size - offset < static_cast<uint32_t>(drawcount)) {
+    scoped->Context()->SynthesizeGLError(GL_INVALID_OPERATION, function_name,
+                                         outOfBoundsDescription);
+    return false;
+  }
   return true;
 }
 

### ts...@chromium.org (2021-06-18)

kbr - maybe you could help find an appropriate owner for this. Thanks.

[Monorail components: Blink>WebGL]

### ts...@chromium.org (2021-06-19)

Actually assigning this time.

### ts...@chromium.org (2021-06-19)

[Empty comment from Monorail migration]

### kb...@chromium.org (2021-06-21)

Thanks for the great bug report.

Shrek, could you please take this bug? It's in the renderer-process-side validation code for multi-draw. Thanks.


[Monorail components: Internals>GPU>Internals]

### mp...@chromium.org (2021-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-23)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7d0a12ce19fed024d56b95a692d888fe3ef14e2f

commit 7d0a12ce19fed024d56b95a692d888fe3ef14e2f
Author: Shrek Shao <shrekshao@google.com>
Date: Thu Jun 24 01:57:08 2021

Fix multidraw validation drawcount + offset out of bounds

Bug: 1219886
Change-Id: I8a84664150758370d9a77ee22ac5549bead0e37e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2977850
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#895423}

[modify] https://crrev.com/7d0a12ce19fed024d56b95a692d888fe3ef14e2f/third_party/blink/renderer/modules/webgl/webgl_multi_draw_common.cc


### kb...@chromium.org (2021-06-24)

Shrek's CL above fixes this. Does the fix need to be merged back to any release branches, per the indicated security severity?


### [Deleted User] (2021-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-24)

Requesting merge to stable M91 because latest trunk commit (895423) appears to be after stable branch point (870763).

Requesting merge to beta M92 because latest trunk commit (895423) appears to be after beta branch point (885287).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-25)

This bug requires manual review: M92's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mp...@chromium.org (2021-06-25)

Yeah as it is a High Severity, low risk fix, we should merge this as soon as possible to Beta. Thanks!

Would you consider using base/numerics/safe_math.h (a header-only library) for your addition and inequality checks? I am concerned about integer overflows, even though they would appear improbable in this case.

### kb...@chromium.org (2021-06-25)

mpdenton@: thanks for your review. I also asked about using safe_math on the CL; it turns out the 2 values being added are each 32-bit unsigned ints, so by adding them into a 64-bit unsigned int, overflow can't happen.

Regarding the merge request:

1. Yes
2. https://chromium-review.googlesource.com/c/chromium/src/+/2977850
3. Yes
4. We think it's OK to just merge this to M92 and not M91.
5. Missing validation, allowing out-of-bounds reads in the renderer process.
6. No
7. N/A


### am...@chromium.org (2021-06-28)

Merge approved to M92, please merge to branch 4515 at your earliest convenience. Thanks!

### sr...@google.com (2021-06-28)

Merge approved for M92 branch:4515 please merge asap so we can include in this week's beta release. ( Beta RC build will be cut tomorrow at 3pm PST)

### kb...@chromium.org (2021-06-28)

Merging in https://chromium-review.googlesource.com/c/chromium/src/+/2988885 .


### gi...@appspot.gserviceaccount.com (2021-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e60cc80ff744a88da6076297dbb2b3ff3047d29f

commit e60cc80ff744a88da6076297dbb2b3ff3047d29f
Author: Shrek Shao <shrekshao@google.com>
Date: Tue Jun 29 01:17:03 2021

[M92] Fix multidraw validation drawcount + offset out of bounds

(cherry picked from commit 7d0a12ce19fed024d56b95a692d888fe3ef14e2f)

Bug: 1219886
Change-Id: I8a84664150758370d9a77ee22ac5549bead0e37e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2977850
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#895423}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2988885
Reviewed-by: Shrek Shao <shrekshao@google.com>
Reviewed-by: Austin Eng <enga@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#1101}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/e60cc80ff744a88da6076297dbb2b3ff3047d29f/third_party/blink/renderer/modules/webgl/webgl_multi_draw_common.cc


### kb...@chromium.org (2021-06-29)

[Empty comment from Monorail migration]

### sr...@google.com (2021-06-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-07-02)

Congratulations - the VRP Panel has decided to award you $8500 - $7500 for the report + $1000 patch bonus. Thanks for the report and patch! Nice work!

### am...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### m....@gmail.com (2021-07-03)

[Comment Deleted]

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-21)

[Empty comment from Monorail migration]

### gi...@google.com (2021-07-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0cd64b399cc0321e6c6a996a50e22bc760647be7

commit 0cd64b399cc0321e6c6a996a50e22bc760647be7
Author: Shrek Shao <shrekshao@google.com>
Date: Tue Jul 27 17:02:00 2021

[M90-LTS] Fix multidraw validation drawcount + offset out of bounds

(cherry picked from commit 7d0a12ce19fed024d56b95a692d888fe3ef14e2f)

Bug: 1219886
Change-Id: I8a84664150758370d9a77ee22ac5549bead0e37e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2977850
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#895423}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3041457
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1542}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/0cd64b399cc0321e6c6a996a50e22bc760647be7/third_party/blink/renderer/modules/webgl/webgl_multi_draw_common.cc


### rz...@google.com (2021-07-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1219886?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056214)*
