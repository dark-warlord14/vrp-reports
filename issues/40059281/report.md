# AddressSanitizer: heap-use-after-free element.cc:3611 in blink::Element::RecalcOwnStyle

| Field | Value |
|-------|-------|
| **Issue ID** | [40059281](https://issues.chromium.org/issues/40059281) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2022-04-02 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
asan-win32-release_x64-988236

#Reproduce
1. chrome --no-sandbox --user-data-dir=test poc.html
2. Click any where

What is the expected behavior?

What went wrong?
Type of crash
render tab

#Analysis
Coming soon

#asan
=================================================================
==15596==ERROR: AddressSanitizer: heap-use-after-free on address 0x124a472f26e8 at pc 0x7ffae3e85610 bp 0x003d85dfbfa0 sp 0x003d85dfbfe8
READ of size 8 at 0x124a472f26e8 thread T0
==15596==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffae3e8560f in blink::Element::RecalcOwnStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3611
    #1 0x7ffae3e7fbcd in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3358
    #2 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #3 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #4 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #5 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #6 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #7 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #8 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #9 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #10 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #11 0x7ffae3e805db in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3445
    #12 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #13 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #14 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #15 0x7ffae3e805db in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3445
    #16 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #17 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #18 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #19 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #20 0x7ffae411413b in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2649
    #21 0x7ffae4116917 in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2672
    #22 0x7ffae4117440 in blink::StyleEngine::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2764
    #23 0x7ffae3b61f3f in blink::Document::UpdateStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2192
    #24 0x7ffae3b5fe8a in blink::Document::UpdateStyleAndLayoutTreeForThisDocument C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2143
    #25 0x7ffae3aba5f4 in blink::LocalFrameView::UpdateStyleAndLayoutInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3234
    #26 0x7ffae3a9eab0 in blink::LocalFrameView::UpdateStyleAndLayout C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3187
    #27 0x7ffae3ab038d in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3107
    #28 0x7ffae3aac657 in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2556
    #29 0x7ffae3aaacfe in blink::LocalFrameView::UpdateLifecyclePhasesInternal C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2388
    #30 0x7ffae3aa83ce in blink::LocalFrameView::UpdateLifecyclePhases C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2329
    #31 0x7ffae69ce328 in blink::PageAnimator::UpdateLifecycleToLayoutClean C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\page\page_animator.cc:169
    #32 0x7ffae3a5fe5a in blink::WebFrameWidgetImpl::UpdateLifecycle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:1295
    #33 0x7ffae3f02cca in blink::WebViewImpl::ResizeViewWhileAnchored C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_view_impl.cc:1254
    #34 0x7ffae3f03790 in blink::WebViewImpl::ResizeWithBrowserControls C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\exported\web_view_impl.cc:1325
    #35 0x7ffae3a63145 in blink::WebFrameWidgetImpl::ApplyVisualPropertiesSizing C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:1521
    #36 0x7ffae3a616ff in blink::WebFrameWidgetImpl::UpdateVisualProperties C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:1427
    #37 0x7ffae6b669b7 in blink::WidgetBase::UpdateVisualProperties C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\widget\widget_base.cc:405
    #38 0x7ffadcfe44d0 in blink::mojom::blink::WidgetStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\widget\platform_widget.mojom-blink.cc:1934
    #39 0x7ffadecf64bc in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:922
    #40 0x7ffae199c1a2 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #41 0x7ffadecfa104 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:664
    #42 0x7ffadf6309fb in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1010
    #43 0x7ffadf62a637 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:748
    #44 0x7ffade9c5ef4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #45 0x7ffae1876d85 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:386
    #46 0x7ffae1876379 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:291
    #47 0x7ffae185379a in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:39
    #48 0x7ffae18784f0 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:498
    #49 0x7ffade940af3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #50 0x7ffae136da4a in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:290
    #51 0x7ffade56f92b in content::RunOtherNamedProcessTypeMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:682
    #52 0x7ffade571567 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1021
    #53 0x7ffade56df5b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:407
    #54 0x7ffade56e6e4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:435
    #55 0x7ffad34314ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:176
    #56 0x7ff7c5c25b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #57 0x7ff7c5c22b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #58 0x7ff7c601f6ab in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #59 0x7ffb6df77033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
    #60 0x7ffb6e962650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x124a472f26e8 is located 8 bytes inside of 112-byte region [0x124a472f26e0,0x124a472f2750)
freed by thread T0 here:
    #0 0x7ff7c5cce89b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ffaeac1ae65 in blink::StyleResolverState::~StyleResolverState C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver_state.cc:91
    #2 0x7ffae717744c in blink::StyleResolver::ResolveStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:943
    #3 0x7ffae3e7da18 in blink::Element::OriginalStyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3244
    #4 0x7ffae3e7cbcc in blink::Element::StyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3200
    #5 0x7ffae3e82376 in blink::Element::RecalcOwnStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3604
    #6 0x7ffae3e7fbcd in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3358
    #7 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #8 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #9 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #10 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #11 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #12 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #13 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #14 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #15 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #16 0x7ffae3e805db in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3445
    #17 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #18 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #19 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #20 0x7ffae3e805db in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3445
    #21 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #22 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #23 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #24 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #25 0x7ffae411413b in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2649
    #26 0x7ffae4116917 in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2672
    #27 0x7ffae4117440 in blink::StyleEngine::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:2764

previously allocated by thread T0 here:
    #0 0x7ff7c5cce99b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffad34a42dd in base::PartitionRoot<1>::Alloc C:\b\s\w\ir\cache\builder\src\base\allocator\partition_allocator\partition_root.h:1922
    #2 0x7ffae6d9edd6 in blink::ComputedStyle::Clone C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\style\computed_style.cc:181
    #3 0x7ffae717a6a1 in blink::StyleResolver::ApplyInheritance C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:968
    #4 0x7ffae717aff5 in blink::StyleResolver::InitStyleAndApplyInheritance C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:992
    #5 0x7ffae717d33c in blink::StyleResolver::ApplyBaseStyleNoCache C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:1179
    #6 0x7ffae7177ffc in blink::StyleResolver::ApplyBaseStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:1369
    #7 0x7ffae71767ee in blink::StyleResolver::ResolveStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:879
    #8 0x7ffae3e7da18 in blink::Element::OriginalStyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3244
    #9 0x7ffae3e7cbcc in blink::Element::StyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3200
    #10 0x7ffae3e82376 in blink::Element::RecalcOwnStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3604
    #11 0x7ffae3e7fbcd in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3358
    #12 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #13 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #14 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #15 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #16 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #17 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #18 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #19 0x7ffae3e805db in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3445
    #20 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #21 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #22 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #23 0x7ffae3e805db in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3445
    #24 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #25 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452
    #26 0x7ffae41c5215 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1384
    #27 0x7ffae3e80758 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3452

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3611 in blink::Element::RecalcOwnStyle
Shadow bytes around the buggy address:
  0x047d900de480: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x047d900de490: fd fd fa fa fa fa fa fa fa fa fd fd fd fd fd fd
  0x047d900de4a0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x047d900de4b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x047d900de4c0: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
=>0x047d900de4d0: fd fd fd fd fa fa fa fa fa fa fa fa fd[fd]fd fd
  0x047d900de4e0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa
  0x047d900de4f0: fa fa 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x047d900de500: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x047d900de510: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa 00 00
  0x047d900de520: 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa
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
==15596==ABORTING

Did this work before? N/A 

Chrome version: 102.0.0.0  Channel: n/a
OS Version: 10.0

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 789 B)
- [asan.txt](attachments/asan.txt) (text/plain, 19.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 19.6 KB)

## Timeline

### [Deleted User] (2022-04-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5900610335211520.

### hc...@google.com (2022-04-04)

Able to reproduce on 102.0.4979.0 win

did not repro on 102.0.4970.0 linux or 99.0.4844.0 linux

dalecurtis@, would you be able to help figure out what's going on here or point us to someone who might know? PoC has to do with Video stuff so I put it in here, not sure if that's the actual root cause though.

[Monorail components: Blink>Media]

### [Deleted User] (2022-04-04)

[Empty comment from Monorail migration]

### da...@chromium.org (2022-04-04)

I'm not sure why this is tagged media, it's in style, so =>futhark for triage.

[Monorail components: -Blink>Media Blink>CSS]

### [Deleted User] (2022-04-05)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fu...@chromium.org (2022-04-06)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-04-07)

The problem is as following:

1. Style recalc for video with mediaControls.css triggers load of svg images for the media controls.
2. SVG images are loaded in separate documents. For this local resource the SVG finishes parsing synchronously
3. The SVG image document hits the hack in [1] which allows script handlers to run for the document loading the svg while it is in the middle of style recalc. 
4. The script run does a dom mutation resulting in style invalidation which hits the DCHECK in [2].
5. Later crashes.

I haven't studied what makes it crash specifically, but running scripts from without style recalc should not happen.

[1] https://source.chromium.org/chromium/chromium/src/+/838bfc18567c38022325b4044460b33085eb5bfc:third_party/blink/renderer/core/dom/document.cc;l=6652-6655
[2] https://source.chromium.org/chromium/chromium/src/+/838bfc18567c38022325b4044460b33085eb5bfc:third_party/blink/renderer/core/css/style_engine.cc;l=941


### fu...@chromium.org (2022-04-07)

"running scripts from _within_ style recalc should not happen."


### fu...@chromium.org (2022-04-07)

This is the CL that intoduced the check point: https://crrev.com/8316042650f8ad

I'm not sure where this really should be fixed. There is https://crbug.com/chromium/961428 which says that check point should be removed. Is the problem that SVG images are synchronously parsed when loaded?

I don't know.

Mason, this is connected to element registration, parsing and event handlers. Do you have any idea how to untangle this?


[Monorail components: -Blink>CSS Blink>DOM]

### fs...@opera.com (2022-04-07)

> ...running scripts from _within_ style recalc should not happen.

Wouldn't you have a ScriptForbiddenScope on the stack then? (Which would also avoid performing the microtask checkpoint.) Adding a DCHECK to that effect in a reasonable location might be good. (I looked through parts of the stack and spotted inconsistencies.)

SVGImage always _parses_ synchronously, yes. (And in this case I guess the data may be available synchronously as well?)

### fs...@opera.com (2022-04-08)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-04-08)

fs@: Ah, yes. Strange if style recalc doesn't have that already. I'll take a look.

### fu...@chromium.org (2022-04-08)

[Empty comment from Monorail migration]

### fu...@chromium.org (2022-04-08)

[Empty comment from Monorail migration]

[Monorail components: -Blink>DOM Blink>CSS]

### fu...@chromium.org (2022-04-08)

https://chromium-review.googlesource.com/c/chromium/src/+/3578736

### gi...@appspot.gserviceaccount.com (2022-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2b255ecf2b4ab82ce84cd9c0b21c5dd937bfa0de

commit 2b255ecf2b4ab82ce84cd9c0b21c5dd937bfa0de
Author: Rune Lillesveen <futhark@chromium.org>
Date: Fri Apr 08 17:12:14 2022

Disallow scripting in style recalc

Fixes crash when loading SVG CSS resource for video controls.

Bug: 1312699
Change-Id: I35b6fc2876c8184536dad95d347525c57ff98c02
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3578736
Reviewed-by: Fredrik Söderquist <fs@opera.com>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#990459}

[modify] https://crrev.com/2b255ecf2b4ab82ce84cd9c0b21c5dd937bfa0de/third_party/blink/renderer/core/css/style_engine.cc
[add] https://crrev.com/2b255ecf2b4ab82ce84cd9c0b21c5dd937bfa0de/third_party/blink/web_tests/external/wpt/fullscreen/crashtests/chrome-1312699.html


### fu...@chromium.org (2022-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-09)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-15)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts and nice work! 

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-16)

Not requesting merge to dev (M102) because latest trunk commit (990459) appears to be prior to dev branch point (992738). If this is incorrect, please replace the Merge-NA-102 label with Merge-Request-102. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1312699?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059281)*
