# heap-buffer-overflow in WebMediaPlayerMSCompositor::ReplaceCurrentFrameWithACopyInternal()

| Field | Value |
|-------|-------|
| **Issue ID** | [40057545](https://issues.chromium.org/issues/40057545) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia, Blink>WebRTC>Video |
| **Platforms** | Android, Linux, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | kr...@chromium.org |
| **Created** | 2021-10-08 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36

Steps to reproduce the problem:
Operating System:
Ubuntu 20.04

chromium version:
Version 96.0.4655.0 (Developer Build) (64-bit)
Version 96.0.4664.0 (Developer Build) (64-bit)

1  ./chrome  --user-data-dir=/tmp/22  --incognito http://localhost:8605/crash.html
2. Click button to repro crash.

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60300002b4f8 at pc 0x555fad84d4fa bp 0x7fff0a4d94d0 sp 0x7fff0a4d94c8
READ of size 4 at 0x60300002b4f8 thread T0 (chrome)
    #0 0x555fad84d4f9 in blink::WebMediaPlayerMSCompositor::ReplaceCurrentFrameWithACopyInternal() ./../../third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc:?
    #1 0x555fad84d4f9 in ReplaceCurrentFrameWithACopyInternal ./../../third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc:764
    #2 0x555fad84d4f9 in ?? ??:0
    #3 0x555f9b8848b0 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:142
    #4 0x555f9b8848b0 in RunTask ./../../base/task/common/task_annotator.cc:178
    #5 0x555f9b8848b0 in ?? ??:0
    #6 0x555f9b8bc159 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:357
    #7 0x555f9b8bc159 in ?? ??:0
    #8 0x555f9b8bb987 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260
    #9 0x555f9b8bb987 in ?? ??:0
    #10 0x555f9b8bcac1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:?
    #11 0x555f9b8bcac1 in ?? ??:0
    #12 0x555f9b77d11f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:38
    #13 0x555f9b77d11f in ?? ??:0
    #14 0x555f9b8bd18b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:462
    #15 0x555f9b8bd18b in ?? ??:0
    #16 0x555f9b800029 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:140
    #17 0x555f9b800029 in ?? ??:0
    #18 0x555faf9492f2 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:265
    #19 0x555faf9492f2 in ?? ??:0
    #20 0x555f9a643d34 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:594
    #21 0x555f9a643d34 in ?? ??:0
    #22 0x555f9a647ea1 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:985
    #23 0x555f9a647ea1 in ?? ??:0
    #24 0x555f9a641367 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:390
    #25 0x555f9a641367 in ?? ??:0
    #26 0x555f9a642f82 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:418
    #27 0x555f9a642f82 in ?? ??:0
    #28 0x555f8d6ca255 in ChromeMain ./../../chrome/app/chrome_main.cc:172
    #29 0x555f8d6ca255 in ?? ??:0
    #30 0x7f61baf430b2 in __libc_start_main ??:?
    #31 0x7f61baf430b2 in ?? ??:0

0x60300002b4f8 is located 0 bytes to the right of 24-byte region [0x60300002b4e0,0x60300002b4f8)
allocated by thread T0 (chrome) here:
    #0 0x555f8d6c79ed in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95
    #1 0x555f8d6c79ed in ?? ??:0
    #2 0x555f906c1208 in media::VideoFrameLayout::VideoFrameLayout(media::VideoFrameLayout const&) ./../../buildtools/third_party/libc++/trunk/include/new:235
    #3 0x555f906c1208 in __libcpp_allocate ./../../buildtools/third_party/libc++/trunk/include/new:261
    #4 0x555f906c1208 in allocate ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator.h:82
    #5 0x555f906c1208 in allocate ./../../buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:261
    #6 0x555f906c1208 in __vallocate ./../../buildtools/third_party/libc++/trunk/include/vector:994
    #7 0x555f906c1208 in vector ./../../buildtools/third_party/libc++/trunk/include/vector:1259
    #8 0x555f906c1208 in VideoFrameLayout ./../../media/base/video_frame_layout.cc:155
    #9 0x555f906c1208 in ?? ??:0
    #10 0x555f906bdc0f in media::VideoFrame::VideoFrame(media::VideoFrameLayout const&, media::VideoFrame::StorageType, gfx::Rect const&, gfx::Size const&, base::TimeDelta, media::VideoFrame::FrameControlType) ./../../media/base/video_frame.cc:1364
    #11 0x555f906bdc0f in ?? ??:0
    #12 0x555f906b562c in media::VideoFrame::WrapExternalDataWithLayout(media::VideoFrameLayout const&, gfx::Rect const&, gfx::Size const&, unsigned char*, unsigned long, base::TimeDelta) ./../../media/base/video_frame.cc:442
    #13 0x555f906b562c in ?? ??:0
    #14 0x555f906ce889 in media::CreateFromSkImage(sk_sp<SkImage>, gfx::Rect const&, gfx::Size const&, base::TimeDelta, bool) ./../../media/base/video_util.cc:974
    #15 0x555f906ce889 in ?? ??:0
    #16 0x555fada0998d in blink::VideoFrame::Create(blink::ScriptState*, blink::V8UnionCSSImageValueOrHTMLCanvasElementOrHTMLImageElementOrHTMLVideoElementOrImageBitmapOrOffscreenCanvasOrSVGImageElementOrVideoFrame const*, blink::VideoFrameInit const*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/webcodecs/video_frame.cc:574
    #17 0x555fada0998d in ?? ??:0
    #18 0x555fada374d5 in blink::(anonymous namespace)::v8_video_frame::ConstructorOverload1(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:253
    #19 0x555fada374d5 in ?? ??:0
    #20 0x555fada32dca in blink::(anonymous namespace)::v8_video_frame::ConstructorCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_video_frame.cc:?
    #21 0x555fada32dca in ?? ??:0
    #22 0x555f95ec6f77 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:152
    #23 0x555f95ec6f77 in ?? ??:0
    #24 0x555f95ec3d2d in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<true>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArguments) ./../../v8/src/builtins/builtins-api.cc:112
    #25 0x555f95ec3d2d in ?? ??:0
    #26 0x555f95ec257d in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:138
    #27 0x555f95ec257d in ?? ??:0
    #11 0x7edb00080d77  (<unknown module>)
    #12 0x7edb00009bae  (<unknown module>)
    #13 0x7edb0011957a  (<unknown module>)
    #14 0x7edb0000c6e0  (<unknown module>)
    #15 0x7edb0000c6e0  (<unknown module>)
    #16 0x7edb0000c6e0  (<unknown module>)
    #17 0x7edb0000a6db  (<unknown module>)
    #18 0x7edb0000a406  (<unknown module>)
    #28 0x555f961a344f in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:152
    #29 0x555f961a344f in Invoke ./../../v8/src/execution/execution.cc:383
    #30 0x555f961a344f in ?? ??:0
    #31 0x555f961a23f3 in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*) ./../../v8/src/execution/execution.cc:478
    #32 0x555f961a23f3 in ?? ??:0
    #33 0x555f95de9488 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*) ./../../v8/src/api/api.cc:5164
    #34 0x555f95de9488 in ?? ??:0
    #35 0x555fa8051509 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*) ./../../third_party/blink/renderer/bindings/core/v8/v8_script_runner.cc:723
    #36 0x555fa8051509 in ?? ??:0
    #37 0x555fab46b66a in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)2>::Call(int, v8::Local<v8::Value>*) ./../../third_party/blink/renderer/bindings/core/v8/callback_invoke_helper.cc:132
    #38 0x555fab46b66a in ?? ??:0
    #39 0x555fab476970 in blink::V8EventHandlerNonNull::InvokeWithoutRunnabilityCheck(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_event_handler_non_null.cc:184
    #40 0x555fab476970 in ?? ??:0
    #41 0x555fa8c7129a in blink::JSEventHandler::InvokeInternal(blink::EventTarget&, blink::Event&, v8::Local<v8::Value>) ./../../third_party/blink/renderer/bindings/core/v8/js_event_handler.cc:135
    #42 0x555fa8c7129a in ?? ??:0
    #43 0x555fa7b710e2 in blink::JSBasedEventListener::Invoke(blink::ExecutionContext*, blink::Event*) ./../../third_party/blink/renderer/bindings/core/v8/js_based_event_listener.cc:150
    #44 0x555fa7b710e2 in ?? ??:0
    #45 0x555fa7b566e7 in blink::EventTarget::FireEventListeners(blink::Event&, blink::EventTargetData*, blink::HeapVector<blink::RegisteredEventListener, 1u>&) ./../../third_party/blink/renderer/core/dom/events/event_target.cc:896
    #46 0x555fa7b566e7 in ?? ??:0
    #47 0x555fa7b54701 in blink::EventTarget::FireEventListeners(blink::Event&) ./../../third_party/blink/renderer/core/dom/events/event_target.cc:810
    #48 0x555fa7b54701 in ?? ??:0
    #49 0x555fa7b0299f in blink::LocalDOMWindow::DispatchEvent(blink::Event&, blink::EventTarget*) ./../../third_party/blink/renderer/core/frame/local_dom_window.cc:1927
    #50 0x555fa7b0299f in ?? ??:0

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/test/asan-linux-release/chrome+0x2a94a4f9)
Shadow bytes around the buggy address:
  0x0c067fffd640: fa fa 00 00 00 fa fa fa fd fd fd fa fa fa 00 00
  0x0c067fffd650: 00 00 fa fa 00 00 00 00 fa fa 00 00 00 fa fa fa
  0x0c067fffd660: 00 00 00 00 fa fa 00 00 00 fa fa fa 00 00 00 fa
  0x0c067fffd670: fa fa 00 00 00 00 fa fa fd fd fd fa fa fa 00 00
  0x0c067fffd680: 00 fa fa fa 00 00 00 00 fa fa 00 00 00 fa fa fa
=>0x0c067fffd690: 00 00 00 fa fa fa fd fd fd fa fa fa 00 00 00[fa]
  0x0c067fffd6a0: fa fa fd fd fd fa fa fa 00 00 00 00 fa fa 00 00
  0x0c067fffd6b0: 00 fa fa fa 00 00 00 fa fa fa 00 00 00 00 fa fa
  0x0c067fffd6c0: 00 00 00 00 fa fa 00 00 00 fa fa fa 00 00 00 fa
  0x0c067fffd6d0: fa fa 00 00 00 fa fa fa fd fd fd fa fa fa 00 00
  0x0c067fffd6e0: 00 fa fa fa 00 00 00 fa fa fa fd fd fd fa fa fa
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
==1==ABORTING

Did this work before? N/A 

Chrome version: 96.0.4655.0  Channel: n/a
OS Version: 20.04

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 855 B)
- [test.txt](attachments/test.txt) (text/plain, 4 B)
- [crash.html](attachments/crash.html) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2021-10-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-10-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5652814245986304.

### xi...@chromium.org (2021-10-08)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-10-11)

Thanks for the report. I'm able to reproduce on Linux. FWIW, before the heap-buffer-overflow happens, I also hit:

[2329855:1:1010/222250.860952:FATAL:webmediaplayer_ms_compositor.cc(90)] Check failed: frame->format() == media::PIXEL_FORMAT_I420A || frame->format() == media::PIXEL_FORMAT_I420 || frame->format() == media::PIXEL_FORMAT_NV12.

+kron@ as the owner of webmediaplayer_ms to take a look. Thanks!

[Monorail components: Blink>GetUserMedia Blink>WebRTC>Video]

### [Deleted User] (2021-10-11)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-10-11)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-10-11)

The video format is ARGB and HasTextures() == false which is currently not supported by the CopyFrame function in webmediaplayer_ms_compositor.cc.

### [Deleted User] (2021-10-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-11)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2021-10-11)

A CL to fix this issue is ready for review,
https://chromium-review.googlesource.com/c/chromium/src/+/3218052


### kr...@chromium.org (2021-10-12)

Here's a slight modification of crash.html that doesn't require a webserver. I've changed the code to draw a house and then pause the video.
It doesn't always crash unless built with DCHECK's but it can be seen that the video is not correctly copied when it's paused, so the house disappears if one selects another tab and then go back.

### kr...@chromium.org (2021-10-12)

I've only reproduced this on Linux.

### gi...@appspot.gserviceaccount.com (2021-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2bf77002c58a05e1c673e28f6cca5882fe4e7e97

commit 2bf77002c58a05e1c673e28f6cca5882fe4e7e97
Author: Johannes Kron <kron@chromium.org>
Date: Tue Oct 12 12:45:39 2021

[wmp_ms] Add support for ARGB software frames to copy-on-pause

Fixed: chromium:1257891
Change-Id: I576b01d317b738f71989be7c6da2a77894bc0215
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3218052
Reviewed-by: Ilya Nikolaevskiy <ilnik@chromium.org>
Commit-Queue: Johannes Kron <kron@chromium.org>
Cr-Commit-Position: refs/heads/main@{#930514}

[modify] https://crrev.com/2bf77002c58a05e1c673e28f6cca5882fe4e7e97/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc


### [Deleted User] (2021-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-12)

Requesting merge to dev M96 because latest trunk commit (930514) appears to be after dev branch point (929512).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-10-12)

Apprioving merge to M96, branch 4664.

### kr...@chromium.org (2021-10-13)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-10-13)

Sorry for the noise, I had an old view and didn't see Comments #15-#18 when I added my merge request.

### kr...@chromium.org (2021-10-13)

By disabling hardware acceleration I was able to reproduce the problem also on MacOS and Windows.

This also affects M94 and M95.


### [Deleted User] (2021-10-13)

Merge review required: M95 has already been cut for stable release.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-13)

Merge review required: M94 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2021-10-13)

Hi,
here are answers to the questions above:

1. This is a security fix and hence fit within the criteria for both M94 and M95.
2. The CL that is requested to be merged is https://chromium-review.googlesource.com/c/chromium/src/+/3218052
3. The fix has been tested on Canary and ToT.
4. No, not a new feature.
6. I don't think it should be considered a major issue at this point.

### gi...@appspot.gserviceaccount.com (2021-10-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a53c0fa309f46cc4db678863af959a0ea8a11d99

commit a53c0fa309f46cc4db678863af959a0ea8a11d99
Author: Johannes Kron <kron@chromium.org>
Date: Wed Oct 13 14:52:43 2021

Merge M96: [wmp_ms] Add support for ARGB software frames to copy-on-pause

(cherry picked from commit 2bf77002c58a05e1c673e28f6cca5882fe4e7e97)

Fixed: chromium:1257891
Change-Id: I576b01d317b738f71989be7c6da2a77894bc0215
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3218052
Reviewed-by: Ilya Nikolaevskiy <ilnik@chromium.org>
Commit-Queue: Johannes Kron <kron@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#930514}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3220612
Cr-Commit-Position: refs/branch-heads/4664@{#76}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/a53c0fa309f46cc4db678863af959a0ea8a11d99/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc


### ad...@google.com (2021-10-13)

Thanks, I'm following up with xinghuilu@ who (per https://crbug.com/chromium/1257891#c4) couldn't reproduce this on M94/M95, before approving merge. We'd probably want to give this a bit more time in Canary anyway before merging to those branches.

### xi...@chromium.org (2021-10-13)

Adjust FoundIn label based on https://crbug.com/chromium/1257891#c21.

### ad...@google.com (2021-10-13)

Removing RBS because this is no longer deemed a recent regression. Let's give this a couple of days before merging to M94/M95.

### ad...@google.com (2021-10-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

now that this has had more time on Canary, unless there are any stability issues or other concerns, please go ahead and merge to M95 (branch 4638) and M94 (branch 4606) in order for this fix to be included in the first respins of stable and extended stable respectively 

### gi...@appspot.gserviceaccount.com (2021-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/92fef0689ea79b1911b091744a6a427fbdfc54da

commit 92fef0689ea79b1911b091744a6a427fbdfc54da
Author: Johannes Kron <kron@chromium.org>
Date: Wed Oct 20 12:07:31 2021

Merge M95: [wmp_ms] Add support for ARGB software frames to copy-on-pause

(cherry picked from commit 2bf77002c58a05e1c673e28f6cca5882fe4e7e97)

Fixed: chromium:1257891
Change-Id: I576b01d317b738f71989be7c6da2a77894bc0215
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3218052
Reviewed-by: Ilya Nikolaevskiy <ilnik@chromium.org>
Commit-Queue: Johannes Kron <kron@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#930514}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3234517
Cr-Commit-Position: refs/branch-heads/4638@{#932}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/92fef0689ea79b1911b091744a6a427fbdfc54da/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc


### gi...@appspot.gserviceaccount.com (2021-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/203094d7af9057826861a59930d2aecf6e7820bf

commit 203094d7af9057826861a59930d2aecf6e7820bf
Author: Johannes Kron <kron@chromium.org>
Date: Wed Oct 20 12:19:04 2021

Merge M94: [wmp_ms] Add support for ARGB software frames to copy-on-pause

(cherry picked from commit 2bf77002c58a05e1c673e28f6cca5882fe4e7e97)

Fixed: chromium:1257891
Change-Id: I576b01d317b738f71989be7c6da2a77894bc0215
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3218052
Reviewed-by: Ilya Nikolaevskiy <ilnik@chromium.org>
Commit-Queue: Johannes Kron <kron@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#930514}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3234536
Cr-Commit-Position: refs/branch-heads/4606@{#1385}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/203094d7af9057826861a59930d2aecf6e7820bf/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc


### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $7500 for this report. Thanks for this report and nice work! 

### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### vo...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### vo...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### gi...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/94ac09ce3fa8919e550e6e0df171143295b5c362

commit 94ac09ce3fa8919e550e6e0df171143295b5c362
Author: Johannes Kron <kron@chromium.org>
Date: Tue Nov 02 00:24:56 2021

[M90-LTS][wmp_ms] Add support for ARGB software frames to copy-on-pause

(cherry picked from commit 2bf77002c58a05e1c673e28f6cca5882fe4e7e97)

(cherry picked from commit 203094d7af9057826861a59930d2aecf6e7820bf)

Fixed: chromium:1257891
Change-Id: I576b01d317b738f71989be7c6da2a77894bc0215
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3218052
Commit-Queue: Johannes Kron <kron@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#930514}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3234536
Cr-Original-Commit-Position: refs/branch-heads/4606@{#1385}
Cr-Original-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3240723
Reviewed-by: Johannes Kron <kron@chromium.org>
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1651}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/94ac09ce3fa8919e550e6e0df171143295b5c362/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc


### vo...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1257891?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GetUserMedia, Blink>WebRTC>Video]
[Monorail mergedwith: crbug.com/chromium/1257892]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057545)*
