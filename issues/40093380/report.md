# UAP in blink::UpdatePlaceHolderImage

| Field | Value |
|-------|-------|
| **Issue ID** | [40093380](https://issues.chromium.org/issues/40093380) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Canvas |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | fs...@chromium.org |
| **Created** | 2018-12-11 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. Install Node.js include npm and express(cuz there is a node webserver)
2. Make a dirctory named "htm" in the same dir with sw.js. Put crash.html and release other resource files into the "htm" dir.
3. Run node ws.js and,if every thing setting up correctly,nothing will echo from console.
4.Download latest chromium asan build. asan-linux-release-613801 tested to be fine.
5.Run ./chrome http://127.0.0.1:8605/crash.html

What is the expected behavior?

What went wrong?
1. Install Node.js include npm and express(cuz there is a node webserver)
2. Make a dirctory named "htm" in the same dir with sw.js and put crash.html and other resource files into the "htm" dir.
3. Run node ws.js and,if every thing setting up correctly,nothing will echo from console.
4.Download latest chromium asan build. asan-linux-release-613801 tested to be fine.
5.Run ./chrome http://127.0.0.1:8605/crash.html

Can stably get UAP crash.Seems like that placeholder_canvas is invalid and when calling its virtul function ,crash happened.

Placeholder_canvas's memory is poisoned while the releaseFrameToDispatcher task is transforming between main thread and worker thread.
But i'm curious about that what makes placeholder_canvas's memory poisoned only could be freeing it.So it should be a UAF rather than a UAP.
Could there something else make s_placeholderRegistry's element value invalid before erase it or oilpan gc poisons the memory before free it？

Did this work before? N/A 

Chrome version: 73.0.3631.0   Channel: stable
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [asan.log](attachments/asan.log) (text/plain, 7.4 KB)

## Timeline

### cd...@gmail.com (2018-12-11)

UAP in UpdatePlaceholderImage
And log see asan.log


### ca...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

[Monorail components: Blink>Paint]

### ca...@chromium.org (2018-12-11)

Assigning High severity since this is memory corruption in the renderer process.

### ca...@chromium.org (2018-12-11)

Assigning to mcasas from the owner's file, and (relatively) recent activity in the method. Also cc'ing a few more folks from the owner's file.

mcasas: Can you take a look at this? (and reassign if appropriate). Thanks

### sh...@chromium.org (2018-12-26)

mcasas: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2018-12-26)

I might have touched the file in the context of lowLatency development,
but I don't think I have manipulated its logic in any meaningful way,
so sending it back to fserb@ for triaging.

### sh...@chromium.org (2018-12-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-10)

fserb: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2019-01-25)

Friendly sheriff ping fserb@: Can you please take a look, or help find a better owner if you aren't the right person to fix this? We try to fix all high severity security bugs within 60 days. Thanks!

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-10)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2019-02-20)

85cb2f71a50dd7da960d31cd599df1cd9d6487b9 might (?) be relevant: "Remove WTF::WeakPtr entirely and replace it with base::WeakPtr." A semi-random guess.

We really need to get this bug fixed. It is High severity and past its deadline. Thanks to anyone who can help.



### sl...@chromium.org (2019-02-20)

[Empty comment from Monorail migration]

### sc...@chromium.org (2019-02-21)

I'll look at it given I have everything in place.

### sc...@chromium.org (2019-02-21)

I'm getting the crash stack below, with some logging.

An OffscreenCanvas is creating a CanvasResourceDispatcher which is a CompositorFrameSyncClient that receives mojo messages to produce a frame (OnBeginFrame). However, the OffscreenCanvas client of the CanvasResourceDispatcher is garbage collected with no notification of any kind to it's frame sink that it is no longer valid.

The fix is probably just to clear the client on the frame_dispatcher_ when the OffscreenCanvas is Dispose'd. I'll put up a patch to do that.

The test case is a mess and not really suitable. I have no idea how to construct an test case for this, so manual testing might be enough.

fserb@, thoughts?

As an aside, how would the thing sending the messages know that the frame_sync on the other end is deleted, when that happens? Does it need to?

--------------------

[1:1:0221/125506.122209:ERROR:canvas_resource_dispatcher.cc(67)] this is 0x61400000f840 client is 0x7ed421679b10
[1:1:0221/125506.125130:ERROR:offscreen_canvas.cc(293)] Created 0x61400000f840 client 0x7ed421679ab0
[1:1:0221/125506.854655:ERROR:offscreen_canvas.cc(70)] Disposing 0x7ed421679ab0
[1:1:0221/125506.872928:ERROR:canvas_resource_dispatcher.cc(345)] Client is 0x7ed421679b10
=================================================================
==1==ERROR: AddressSanitizer: use-after-poison on address 0x7ed421679b10 at pc 0x7fa4b122a5dc bp 0x7ffe29584c90 sp 0x7ffe29584c88
READ of size 8 at 0x7ed421679b10 thread T0 (content_shell)
    #0 0x7fa4b122a5db in blink::CanvasResourceDispatcher::OnBeginFrame(viz::BeginFrameArgs const&, WTF::HashMap<unsigned int, mojo::StructPtr<gfx::mojom::blink::PresentationFeedback>, WTF::IntHash<unsigned int>, WTF::HashTraits<unsigned int>, WTF::HashTraits<mojo::StructPtr<gfx::mojom::blink::PresentationFeedback> >, WTF::PartitionAllocator>) ./../../third_party/blink/renderer/platform/graphics/canvas_resource_dispatcher.cc:346:15
    #1 0x7fa4b438d279 in viz::mojom::blink::CompositorFrameSinkClientStubDispatch::Accept(viz::mojom::blink::CompositorFrameSinkClient*, mojo::Message*) ./gen/services/viz/public/interfaces/compositing/compositor_frame_sink.mojom-blink.cc:1356:13
    #2 0x7fa4b11cc0dd in viz::mojom::blink::CompositorFrameSinkClientStub<mojo::RawPtrImplRefTraits<viz::mojom::blink::CompositorFrameSinkClient> >::Accept(mojo::Message*) ./gen/services/viz/public/interfaces/compositing/compositor_frame_sink.mojom-blink.h:253:12
    #3 0x7fa5046c82a9 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:423:32
    #4 0x7fa5046c7268 in mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:133:18
    #5 0x7fa5046c3683 in mojo::FilterChain::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/filter_chain.cc:40:17
    #6 0x7fa5046cccb3 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:306:19
    #7 0x7fa5046f174d in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:873:42
    #8 0x7fa5046efef7 in mojo::internal::MultiplexRouter::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:594:38
    #9 0x7fa5046c3683 in mojo::FilterChain::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/filter_chain.cc:40:17
    #10 0x7fa50468394b in mojo::Connector::DispatchMessage(mojo::Message) ./../../mojo/public/cpp/bindings/lib/connector.cc:525:49
    #11 0x7fa50468222a in mojo::Connector::DispatchNextMessageInQueue() ./../../mojo/public/cpp/bindings/lib/connector.cc:555:17
    #12 0x7fa5046943a8 in bool base::internal::FunctorTraits<bool (mojo::Connector::*)(), void>::Invoke<bool (mojo::Connector::*)(), base::WeakPtr<mojo::Connector> >(bool (mojo::Connector::*)(), base::WeakPtr<mojo::Connector>&&) ./../../base/bind_internal.h:518:12
    #13 0x7fa5046940f5 in void base::internal::FunctorTraits<base::internal::IgnoreResultHelper<bool (mojo::Connector::*)()>, void>::Invoke<base::internal::IgnoreResultHelper<bool (mojo::Connector::*)()>, base::WeakPtr<mojo::Connector> >(base::internal::IgnoreResultHelper<bool (mojo::Connector::*)()>&&, base::WeakPtr<mojo::Connector>&&) ./../../base/bind_internal.h:563:5
    #14 0x7fa504693eb7 in void base::internal::InvokeHelper<true, void>::MakeItSo<base::internal::IgnoreResultHelper<bool (mojo::Connector::*)()>, base::WeakPtr<mojo::Connector> >(base::internal::IgnoreResultHelper<bool (mojo::Connector::*)()>&&, base::WeakPtr<mojo::Connector>&&) ./../../base/bind_internal.h:638:5
    #15 0x7fa504693e41 in void base::internal::Invoker<base::internal::BindState<base::internal::IgnoreResultHelper<bool (mojo::Connector::*)()>, base::WeakPtr<mojo::Connector> >, void ()>::RunImpl<base::internal::IgnoreResultHelper<bool (mojo::Connector::*)()>, std::__Cr::tuple<base::WeakPtr<mojo::Connector> >, 0ul>(base::internal::IgnoreResultHelper<bool (mojo::Connector::*)()>&&, std::__Cr::tuple<base::WeakPtr<mojo::Connector> >&&, std::__Cr::integer_sequence<unsigned long, 0ul>) ./../../base/bind_internal.h:691:12
    #16 0x7fa504693d2d in base::internal::Invoker<base::internal::BindState<base::internal::IgnoreResultHelper<bool (mojo::Connector::*)()>, base::WeakPtr<mojo::Connector> >, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:660:12
    #17 0x7fa504cafce1 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:99:12
    #18 0x7fa505108edc in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/task/common/task_annotator.cc:104:33
    #19 0x7fa5051b9df1 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:336:21
    #20 0x7fa5051b8619 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:217:7
    #21 0x7fa5051ba625 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #22 0x7fa504e8ac23 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:39:55
    #23 0x7fa5051bc713 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:403:12
    #24 0x7fa504ff8d98 in base::RunLoop::Run() ./../../base/run_loop.cc:157:14
    #25 0x7fa4fabe434c in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:218:16
    #26 0x7fa4fb68a85b in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:504:14
    #27 0x7fa4fb68b63b in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:581:12
    #28 0x7fa4fb68e06d in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:870:10
    #29 0x7fa4fb683559 in content::ContentServiceManagerMainDelegate::RunEmbedderProcess() ./../../content/app/content_service_manager_main_delegate.cc:52:32
    #30 0x7fa48434429c in service_manager::Main(service_manager::MainParams const&) ./../../services/service_manager/embedder/main.cc:416:29
    #31 0x7fa4fb68a202 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:19:10
    #32 0x559179ed402c in main ./../../content/shell/app/shell_main.cc:39:10
    #33 0x7fa4874882b0 in __libc_start_main ??:0:0

Address 0x7ed421679b10 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison (/usr/local/google/home/schenney/development/chromium_sec/src/out/DebugAsanGN/libblink_platform.so+0x2dee5db)
Shadow bytes around the buggy address:
  0x0fdb042c7310: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdb042c7320: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdb042c7330: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdb042c7340: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdb042c7350: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fdb042c7360: f7 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdb042c7370: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdb042c7380: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdb042c7390: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdb042c73a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdb042c73b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==1==ABORTING




### sc...@chromium.org (2019-02-21)

Clearing the client moves the crash to be a straight up null pointer on the incoming OnBeginFrame message once the CanvasResourceProvider is actually deleted.

Passing to fserb@ to either implement the fix that closes the mojo pipe or otherwise tell me how to do it. I looked but it's very non-obvious because the CanvasResourceDispatcher always seems to assume it has an embedder connecteed.

Or should the OffscreenCanvas live on, by converting the client_ pointer in CanvasResourceProvider into a WeakMember or something.

[Monorail components: -Blink>Paint Blink>Canvas]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6a7063ae61cf031630b48bdcdb09863ffc199962

commit 6a7063ae61cf031630b48bdcdb09863ffc199962
Author: Fernando Serboncini <fserb@chromium.org>
Date: Wed Feb 27 02:38:14 2019

Clean up CanvasResourceDispatcher on finalizer

We may have pending mojo messages after GC, so we want to drop the
dispatcher as soon as possible.

Bug: 929757,913964
Change-Id: I5789bcbb55aada4a74c67a28758f07686f8911c0
Reviewed-on: https://chromium-review.googlesource.com/c/1489175
Reviewed-by: Ken Rockot <rockot@google.com>
Commit-Queue: Ken Rockot <rockot@google.com>
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Auto-Submit: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#635833}
[modify] https://crrev.com/6a7063ae61cf031630b48bdcdb09863ffc199962/third_party/blink/renderer/core/html/canvas/html_canvas_element.cc
[modify] https://crrev.com/6a7063ae61cf031630b48bdcdb09863ffc199962/third_party/blink/renderer/core/offscreencanvas/offscreen_canvas.cc


### fs...@chromium.org (2019-02-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-05)

This bug requires manual review: We are only 6 days from stable.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2019-03-05)

[Empty comment from Monorail migration]

### ab...@google.com (2019-03-05)

branch:3683

### fs...@chromium.org (2019-03-05)

merged.

### cr...@appspot.gserviceaccount.com (2019-03-05)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/8cbb211d93b114c2bc348837d787aa5c8e545e40

Commit: 8cbb211d93b114c2bc348837d787aa5c8e545e40
Author: fserb@chromium.org
Commiter: fserb@chromium.org
Date: 2019-03-05 14:34:27 +0000 UTC

Clean up CanvasResourceDispatcher on finalizer

We may have pending mojo messages after GC, so we want to drop the
dispatcher as soon as possible.

Bug: 929757,913964
Change-Id: I5789bcbb55aada4a74c67a28758f07686f8911c0
Reviewed-on: https://chromium-review.googlesource.com/c/1489175
Reviewed-by: Ken Rockot <rockot@google.com>
Commit-Queue: Ken Rockot <rockot@google.com>
Commit-Queue: Fernando Serboncini <fserb@chromium.org>
Auto-Submit: Fernando Serboncini <fserb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#635833}(cherry picked from commit 6a7063ae61cf031630b48bdcdb09863ffc199962)
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1503613
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Cr-Commit-Position: refs/branch-heads/3683@{#745}
Cr-Branched-From: e51029943e0a38dd794b73caaf6373d5496ae783-refs/heads/master@{#625896}

### na...@google.com (2019-03-07)

fserb - The Vulnerability Reward Panel is trying to evaluate this bug in relation to: 

crbug/917688
crbug/919046
crbug/929757

and what the difference was between these three reports and if they were all covered by the same fix. 


### aw...@chromium.org (2019-03-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-14)

Congrats! The Panel decided to reward $3,000 for this report :) 

### cd...@gmail.com (2019-03-15)

Wow,thank you for the reward.Have good day.：)

### aw...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-05-22)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-06-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/913964?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093380)*
