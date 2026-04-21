# use after poison in ImageDecoderExternal

| Field | Value |
|-------|-------|
| **Issue ID** | [40056609](https://issues.chromium.org/issues/40056609) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2021-07-21 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

Steps to reproduce the problem:
tested chrome version
Chromium 93.0.4573.0 dev build with asan
Chromium 94.0.4582.0
OS version
Ubuntu 20.04
./google-chrome --enable-experimental-web-platform-features --incognito --user-data-dir=/tmp/xx http://localhost:8000/main.html

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: use-after-poison on address 0x7ea49567e1f8 at pc 0x55edd920d65e bp 0x7ffee28b6250 sp 0x7ffee28b6248
READ of size 4 at 0x7ea49567e1f8 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x55edd920d65d in blink::ImageDecoderExternal::OnMetadata(blink::ImageDecoderCore::ImageMetadata) ./../../third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc:589
    #1 0x55edd920d65d in ?? ??:0
    #2 0x55edd920e0d7 in base::internal::Invoker<base::internal::BindState<void (blink::ImageDecoderExternal::*)(blink::ImageDecoderCore::ImageMetadata), base::WeakPtr<blink::ImageDecoderExternal> >, void (blink::ImageDecoderCore::ImageMetadata)>::RunOnce(base::internal::BindStateBase*, blink::ImageDecoderCore::ImageMetadata&&) ./../../base/bind_internal.h:509
    #3 0x55edd920e0d7 in MakeItSo<void (blink::ImageDecoderExternal::*)(blink::ImageDecoderCore::ImageMetadata), base::WeakPtr<blink::ImageDecoderExternal>, blink::ImageDecoderCore::ImageMetadata> ./../../base/bind_internal.h:668
    #4 0x55edd920e0d7 in RunImpl<void (blink::ImageDecoderExternal::*)(blink::ImageDecoderCore::ImageMetadata), std::tuple<base::WeakPtr<blink::ImageDecoderExternal> >, 0UL> ./../../base/bind_internal.h:721
    #5 0x55edd920e0d7 in RunOnce ./../../base/bind_internal.h:690
    #6 0x55edd920e0d7 in ?? ??:0
    #7 0x55edd92145c3 in void base::internal::ReplyAdapter<blink::ImageDecoderCore::ImageMetadata, blink::ImageDecoderCore::ImageMetadata>(base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::__1::unique_ptr<blink::ImageDecoderCore::ImageMetadata, std::__1::default_delete<blink::ImageDecoderCore::ImageMetadata> >*) ./../../base/callback.h:98
    #8 0x55edd92145c3 in ReplyAdapter<blink::ImageDecoderCore::ImageMetadata, blink::ImageDecoderCore::ImageMetadata> ./../../base/post_task_and_reply_with_result_internal.h:30
    #9 0x55edd92145c3 in ?? ??:0
    #10 0x55edd9214986 in base::internal::Invoker<base::internal::BindState<void (*)(base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::__1::unique_ptr<blink::ImageDecoderCore::ImageMetadata, std::__1::default_delete<blink::ImageDecoderCore::ImageMetadata> >*), base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, base::internal::OwnedWrapper<std::__1::unique_ptr<blink::ImageDecoderCore::ImageMetadata, std::__1::default_delete<blink::ImageDecoderCore::ImageMetadata> >, std::__1::default_delete<std::__1::unique_ptr<blink::ImageDecoderCore::ImageMetadata, std::__1::default_delete<blink::ImageDecoderCore::ImageMetadata> > > > >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:404
    #11 0x55edd9214986 in MakeItSo<void (*)(base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::unique_ptr<blink::ImageDecoderCore::ImageMetadata> *), base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::unique_ptr<blink::ImageDecoderCore::ImageMetadata> *> ./../../base/bind_internal.h:648
    #12 0x55edd9214986 in RunImpl<void (*)(base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, std::unique_ptr<blink::ImageDecoderCore::ImageMetadata> *), std::tuple<base::OnceCallback<void (blink::ImageDecoderCore::ImageMetadata)>, base::internal::OwnedWrapper<std::unique_ptr<blink::ImageDecoderCore::ImageMetadata> > >, 0UL, 1UL> ./../../base/bind_internal.h:721
    #13 0x55edd9214986 in RunOnce ./../../base/bind_internal.h:690
    #14 0x55edd9214986 in ?? ??:0
    #15 0x55edc6347622 in base::(anonymous namespace)::PostTaskAndReplyRelay::RunReply(base::(anonymous namespace)::PostTaskAndReplyRelay) ./../../base/callback.h:98
    #16 0x55edc6347622 in RunReply ./../../base/threading/post_task_and_reply_impl.cc:115
    #17 0x55edc6347622 in ?? ??:0
    #18 0x55edc6347868 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:404
    #19 0x55edc6347868 in MakeItSo<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), base::(anonymous namespace)::PostTaskAndReplyRelay> ./../../base/bind_internal.h:648
    #20 0x55edc6347868 in RunImpl<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay), std::tuple<base::(anonymous namespace)::PostTaskAndReplyRelay>, 0UL> ./../../base/bind_internal.h:721
    #21 0x55edc6347868 in RunOnce ./../../base/bind_internal.h:690
    #22 0x55edc6347868 in ?? ??:0
    #23 0x55edc62c2c10 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:98
    #24 0x55edc62c2c10 in RunTask ./../../base/task/common/task_annotator.cc:178
    #25 0x55edc62c2c10 in ?? ??:0
    #26 0x55edc62fcf39 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:360
    #27 0x55edc62fcf39 in ?? ??:0
    #28 0x55edc62fc6aa in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260
    #29 0x55edc62fc6aa in ?? ??:0
    #30 0x55edc62fd8e1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:?
    #31 0x55edc62fd8e1 in ?? ??:0
    #32 0x55edc61bb00f in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39
    #33 0x55edc61bb00f in ?? ??:0
    #34 0x55edc62fdfa4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:467
    #35 0x55edc62fdfa4 in ?? ??:0
    #36 0x55edc623e281 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134
    #37 0x55edc623e281 in ?? ??:0
    #38 0x55edda03d851 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:261
    #39 0x55edda03d851 in ?? ??:0
    #40 0x55edc50db490 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:569
    #41 0x55edc50db490 in ?? ??:0
    #42 0x55edc50de374 in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:955
    #43 0x55edc50de374 in ?? ??:0
    #44 0x55edc50d8c89 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:386
    #45 0x55edc50d8c89 in ?? ??:0
    #46 0x55edc50d91bc in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:412
    #47 0x55edc50d91bc in ?? ??:0
    #48 0x55edb812065d in ChromeMain ./../../chrome/app/chrome_main.cc:151
    #49 0x55edb812065d in ?? ??:0
    #50 0x7fa23c41b0b2 in __libc_start_main ??:?
    #51 0x7fa23c41b0b2 in ?? ??:0

Address 0x7ea49567e1f8 is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison (/home/exp11/chrome/chrome+0x2bb6565d)
Shadow bytes around the buggy address:
  0x0fd512ac7be0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd512ac7bf0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd512ac7c00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd512ac7c10: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd512ac7c20: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fd512ac7c30: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]
  0x0fd512ac7c40: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd512ac7c50: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd512ac7c60: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd512ac7c70: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fd512ac7c80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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

Chrome version:  93.0.4573.0  Channel: dev
OS Version: 20.04

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 757 B)
- [main.html](attachments/main.html) (text/plain, 335 B)
- [testharness.js](attachments/testharness.js) (text/plain, 151.3 KB)
- [testharnessreport.js](attachments/testharnessreport.js) (text/plain, 14.2 KB)

## Timeline

### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### do...@chromium.org (2021-07-21)

Thanks for the report. +dalecurtis +sandersd, do you mind taking a look please? Assigning medium severity for a memory corruption vulnerability in the renderer and FoundIn-93.

[Monorail components: Blink>Media>WebCodecs]

### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-21)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-07-21)

Thanks for the report. Off the top of my head I'm not sure how this could happen. It seems like a pending metadata request was in flight after destruction, but destruction shouldn't start until all requests are resolved, HasPendingActivity() ensures this.

In a developer build I get the following DCHECK:

[52272:23092:0721/103258.327:FATAL:script_state.h(89)] Check failed: script_state->ContextIsValid().
Backtrace:
        base::debug::CollectStackTrace [0x00007FFC6E63BFC2+18] (o:\base\debug\stack_trace_win.cc:303)
        base::debug::StackTrace::StackTrace [0x00007FFC6E5179C2+18] (o:\base\debug\stack_trace.cc:197)
        logging::LogMessage::~LogMessage [0x00007FFC6E5361D8+136] (o:\base\logging.cc:590)
        logging::LogMessage::~LogMessage [0x00007FFC6E537520+16] (o:\base\logging.cc:583)
        blink::ScriptState::Scope::Scope [0x00007FFC453E93C5+149] (o:\third_party\blink\renderer\platform\bindings\script_state.h:90)
        blink::ReadableStreamBytesConsumer::BeginRead [0x00007FFC45B3472D+189] (o:\third_party\blink\renderer\core\fetch\readable_stream_bytes_consumer.cc:136)
        blink::ImageDecoderExternal::OnStateChange [0x00007FFC42520102+242] (o:\third_party\blink\renderer\modules\webcodecs\image_decoder_external.cc:369)
        blink::ImageDecoderExternal::ImageDecoderExternal [0x00007FFC4251FCAF+1791] (o:\third_party\blink\renderer\modules\webcodecs\image_decoder_external.cc:183)
        blink::MakeGarbageCollectedTrait<blink::ImageDecoderExternal>::Call<blink::ScriptState *&,const blink::ImageDecoderInit *&,blink::ExceptionState &> [0x00007FFC42523EA7+63] (o:\third_party\blink\renderer\platform\heap\impl\heap.h:529)
        blink::ImageDecoderExternal::Create [0x00007FFC4251F193+51] (o:\third_party\blink\renderer\modules\webcodecs\image_decoder_external.cc:77)
        blink::`anonymous namespace'::v8_image_decoder::ConstructorCallback [0x00007FFC41B72C87+423] (o:\fake\prefix\gen\third_party\blink\renderer\bindings\modules\v8\v8_image_decoder.cc:191)
        v8::internal::FunctionCallbackArguments::Call [0x00007FFC480B761F+1039] (o:\v8\src\api\api-arguments-inl.h:156)
        v8::internal::`anonymous namespace'::HandleApiCallHelper<1> [0x00007FFC480B4C17+1175] (o:\v8\src\builtins\builtins-api.cc:112)
        v8::internal::Builtin_Impl_HandleApiCall [0x00007FFC480B374C+396] (o:\v8\src\builtins\builtins-api.cc:138)
        v8::internal::Builtin_HandleApiCall [0x00007FFC480B320E+126] (o:\v8\src\builtins\builtins-api.cc:130)
        (No symbol) [0x0000302E000CF87C]
Task trace:
Backtrace:
        IPC::`anonymous namespace'::ChannelAssociatedGroupController::Accept [0x00007FFC81333E2F+1615] (o:\ipc\ipc_mojo_bootstrap.cc:937)

### da...@chromium.org (2021-07-21)

Canary ASAN crash:
https://crash.corp.google.com/browse?stbtiq=354d6b761d88e0d0

### da...@chromium.org (2021-07-21)

https://chromium-review.googlesource.com/c/chromium/src/+/3043451

### da...@chromium.org (2021-07-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/51ce1f3e2b091e3104a737996a388bca8f4c92a7

commit 51ce1f3e2b091e3104a737996a388bca8f4c92a7
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Wed Jul 21 21:01:28 2021

[WebCodecs] Disallow ImageDecoder creation with a destroyed context.

We won't get a OnContextDestroyed() callback later, so this can end
up being problematic if any tasks are queued via WeakPtr.

R=jbroman

Fixed: 1231432
Change-Id: I4c74865719f34a8fc9d5dfe585003fbe74aa5147
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3043451
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Jeremy Roman <jbroman@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#904042}

[modify] https://crrev.com/51ce1f3e2b091e3104a737996a388bca8f4c92a7/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/51ce1f3e2b091e3104a737996a388bca8f4c92a7/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-22)

This release blocking issue appears to be targeted for M93, which has already branched. Because this issue was marked as fixed after branch point, a merge of any CLs which landed on or after July 15 may be required. Please review whether or not any CLs should be merged ASAP, and if a merge is necessary apply the label Merge-Request-93 to begin the merge review process. If no merge is required, please simply remove the Merge-TBD label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-07-22)

[Comment Deleted]

### em...@gmail.com (2021-07-23)

url:gs://chromium-browser-asan/linux-release/asan-linux-release-904573.zip 
Version 94.0.4584.0 (Developer Build) (64-bit)
I tested  many times with the above version, and the issue did not reproduce again.

### [Deleted User] (2021-07-24)

Requesting merge to dev M93 because latest trunk commit (904042) appears to be after dev branch point (902210).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-25)

Your change meets the bar and is auto-approved for M93. Please go ahead and merge the CL to branch 4577 (refs/branch-heads/4577) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-07-25)

Your change has been approved for M93. Please go ahead and merge the CL to branch 4577 manually asap so that it would be part of this week's Dev/Beta release.

### da...@chromium.org (2021-07-26)

In CQ now: https://chromium-review.googlesource.com/c/chromium/src/+/3053080

### da...@chromium.org (2021-07-26)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2021-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f3a48dca66e5da514c76d6618151efca243b7ad6

commit f3a48dca66e5da514c76d6618151efca243b7ad6
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Mon Jul 26 19:22:20 2021

Merge M93: "[WebCodecs] Disallow ImageDecoder creation with a destroyed context."

We won't get a OnContextDestroyed() callback later, so this can end
up being problematic if any tasks are queued via WeakPtr.

R=​jbroman

(cherry picked from commit 51ce1f3e2b091e3104a737996a388bca8f4c92a7)

Fixed: 1231432
Change-Id: I4c74865719f34a8fc9d5dfe585003fbe74aa5147
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3043451
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Jeremy Roman <jbroman@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#904042}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3053080
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4577@{#183}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/f3a48dca66e5da514c76d6618151efca243b7ad6/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/f3a48dca66e5da514c76d6618151efca243b7ad6/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### pb...@google.com (2021-07-27)

All required changes have been merged to M93 branch hence dropping the Merge-TBD label.

### am...@google.com (2021-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-28)

Congratulations emilykim@, the VRP Panel has decided to award you $5000 for this report. Nice work! 

### am...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### ma...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c51d1ef1ee2bfa5a4b110dc7144773b1f1ddee44

commit c51d1ef1ee2bfa5a4b110dc7144773b1f1ddee44
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Wed Sep 08 18:59:28 2021

[M90-LTS][WebCodecs] Disallow ImageDecoder creation with a destroyed context.

We won't get a OnContextDestroyed() callback later, so this can end
up being problematic if any tasks are queued via WeakPtr.

M90 merge conflicts:
* image_decoder_external.cc
  Automerge failed because of different initializer list in ImageDecoderExternal.
  The second part is just formatting, skipped altogeter.
  No actual conflicts.
* image_decoder_external_test.cc
  Automerge failed because of missing tests in M90.
  Use old ImageDecoderExternal::canDecodeType instead of
  IsTypeSupported and ImageDecoderExternal::isTypeSupported 
  (changed in crrev.com/c/2733922 after M90).

(cherry picked from commit 51ce1f3e2b091e3104a737996a388bca8f4c92a7)

(cherry picked from commit f3a48dca66e5da514c76d6618151efca243b7ad6)

Fixed: 1231432
Change-Id: I4c74865719f34a8fc9d5dfe585003fbe74aa5147
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3043451
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Jeremy Roman <jbroman@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#904042}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3053080
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/4577@{#183}
Cr-Original-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3148415
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1587}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/c51d1ef1ee2bfa5a4b110dc7144773b1f1ddee44/third_party/blink/renderer/modules/webcodecs/image_decoder_external.cc
[modify] https://crrev.com/c51d1ef1ee2bfa5a4b110dc7144773b1f1ddee44/third_party/blink/renderer/modules/webcodecs/image_decoder_external_test.cc


### as...@google.com (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-01-05)

Hello OP/emilykim@, we consider attachments/pocs included with reports to be an integral part of the report (https://bughunters.google.com/about/rules/5745167867576320), so I've undeleted them. Thank you! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1231432?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056609)*
