# UAP due to largearray and removechild()

| Field | Value |
|-------|-------|
| **Issue ID** | [390633126](https://issues.chromium.org/issues/390633126) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS, Blink>GarbageCollection |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 134.0.6963.0 |
| **Reporter** | da...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2025-01-18 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Host test.html + test.js with python -m http.server 9003
2. lanuch chrome with: --no-sandbox --enable-logging --v=1 <http://localhost:9003>
3. Click on test.html
4. Wait for the UAP to occur (ranges from 5-60 minutes)

# Problem Description

This reproduces for me both on windows10 22H2 (win32-release\_x64\_asan-win32-release\_x64-1405230) and ubuntu24.04.1 LTS (linux-release\_asan-linux-release-1407906).

The issue is likely in the document.body.removechild() - as Ive done tests without it and it does not yield the same result.
Some caveats:
Chrome\_debug.log-files will swell to ~2gb.
The 'hung' tab can show up on linux, just keep waiting (see PoC.webm). Sadly my ASAN-stacktrace from linux doesnt include symbols but it only takes ~20 minutes for it to trigger the UAP.
On windows 9000+ handles can be seen and seems rather excessive.

# Summary

UAP due to largearray and removechild()

# Custom Questions

#### Type of crash:

tab

#### Crash state:

```
=================================================================
==4988==ERROR: AddressSanitizer: use-after-poison on address 0x7e85d0f00850 at pc 0x7ffcd4f7d2cf bp 0x00497f9ecf40 sp 0x00497f9ecf88
WRITE of size 4 at 0x7e85d0f00850 thread T0
    #0 0x7ffcd4f7d2ce in cppgc::internal::MemberBase<cppgc::internal::CompressedPointer>::MemberBase C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\member.h:44
    #1 0x7ffcd4f7d2ce in cppgc::internal::BasicMember<blink::ComputedStyleBase::StyleGridData,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer>::BasicMember C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\member.h:287
    #2 0x7ffcd4f7d2ce in cppgc::internal::BasicMember<blink::ComputedStyleBase::StyleGridData,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer>::BasicMember C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\member.h:112
    #3 0x7ffcd4f7d2ce in blink::ComputedStyleBase::StyleRareNonInheritedUsageLessThan14PercentSubData::StyleRareNonInheritedUsageLessThan14PercentSubData(class blink::ComputedStyleBase::StyleRareNonInheritedUsageLessThan14PercentSubData const &) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\core\style\computed_style_base.cc:6996:7
    #4 0x7ffcd3bda3ae in cppgc::MakeGarbageCollectedTrait<blink::ComputedStyleBase::StyleRareNonInheritedUsageLessThan14PercentSubData>::Call C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\allocation.h:241
    #5 0x7ffcd3bda3ae in cppgc::MakeGarbageCollected C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\allocation.h:279
    #6 0x7ffcd3bda3ae in blink::MakeGarbageCollected C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\heap\garbage_collected.h:37
    #7 0x7ffcd3bda3ae in blink::ComputedStyleBase::StyleRareNonInheritedUsageLessThan14PercentSubData::Copy C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\core\style\computed_style_base.h:5657
    #8 0x7ffcd3bda3ae in blink::ComputedStyleBuilderBase::Access C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\core\style\computed_style_base.h:22382
    #9 0x7ffcd3bda3ae in blink::ComputedStyleBuilderBase::SetOverflowClipMargin(class std::__Cr::optional<class blink::StyleOverflowClipMargin> const &) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\core\style\computed_style_base.h:15051:7
    #10 0x7ffcd7d8f01f in blink::css_longhand::OverflowClipMargin::ApplyValue(class blink::StyleResolverState &, class blink::CSSValue const &, enum blink::CSSProperty::ValueMode) const C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\renderer\core\css\properties\longhands.cc:10318:24
    #11 0x7ffcd819a870 in blink::StyleBuilder::ApplyPhysicalProperty(class blink::CSSProperty const &, class blink::StyleResolverState &, class blink::CSSValue const &, enum blink::CSSProperty::ValueMode) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_builder.cc:132:28
    #12 0x7ffcd81a67a9 in blink::StyleCascade::LookupAndApplyDeclaration(class blink::CSSProperty const &, class blink::CascadePriority *, class blink::CascadeResolver &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:844:3
    #13 0x7ffcd819f3ab in blink::StyleCascade::ApplyMatchResult(class blink::CascadeResolver &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:684:5
    #14 0x7ffcd819b1e8 in blink::StyleCascade::Apply(class blink::CascadeFilter) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:219:3
    #15 0x7ffcd3f1d89e in blink::StyleResolver::ApplyPropertiesFromCascade(class blink::StyleResolverState &, class blink::StyleCascade &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:2803:11
    #16 0x7ffcd3f1b6c9 in blink::StyleResolver::ApplyBaseStyleNoCache(class blink::Element *, class blink::StyleRecalcContext const &, class blink::StyleRequest const &, class blink::StyleResolverState &, class blink::StyleCascade &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:1666:5
    #17 0x7ffcd3f14886 in blink::StyleResolver::ApplyBaseStyle(class blink::Element *, class blink::StyleRecalcContext const &, class blink::StyleRequest const &, class blink::StyleResolverState &, class blink::StyleCascade &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:1874:3
    #18 0x7ffcd3f12f72 in blink::StyleResolver::ResolveStyle(class blink::Element *, class blink::StyleRecalcContext const &, class blink::StyleRequest const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:1226:3
    #19 0x7ffcd0048b76 in blink::Element::OriginalStyleForLayoutObject(class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3767:43
    #20 0x7ffcd00483a1 in blink::Element::StyleForLayoutObject(class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3724:13
    #21 0x7ffcd004c730 in blink::Element::RecalcOwnStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:4270:17
    #22 0x7ffcd0049f7b in blink::Element::RecalcStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:3920:20
    #23 0x7ffcd02f8c57 in blink::ContainerNode::RecalcDescendantStyles(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &, class blink::Element &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1653:22
    #24 0x7ffcd004abbe in blink::Element::RecalcStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:4055:7
    #25 0x7ffcd02f8c57 in blink::ContainerNode::RecalcDescendantStyles(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &, class blink::Element &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\container_node.cc:1653:22
    #26 0x7ffcd004abbe in blink::Element::RecalcStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\element.cc:4055:7
    #27 0x7ffcd04c36b7 in blink::StyleEngine::RecalcStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:3769:16
    #28 0x7ffcd04c79c1 in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:3810
    #29 0x7ffcd04c79c1 in blink::StyleEngine::UpdateStyleAndLayoutTree(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\css\style_engine.cc:3928:7
    #30 0x7ffccfb42463 in blink::Document::UpdateStyle(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2505:16
    #31 0x7ffccfb3f7ef in blink::Document::UpdateStyleAndLayoutTreeForThisDocument(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2444:3
    #32 0x7ffccfb3e673 in blink::Document::UpdateStyleAndLayoutTree(class blink::LayoutUpgrade &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2304:5
    #33 0x7ffccfb3e5e0 in blink::Document::UpdateStyleAndLayoutTree(class blink::LayoutUpgrade &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2295:26
    #34 0x7ffccfb33a2f in blink::Document::UpdateStyleAndLayoutTree(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\dom\document.cc:2279:3
    #35 0x7ffccfd5c955 in blink::FrameSelection::FocusedOrActiveStateChanged(void) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\editing\frame_selection.cc:1052:17
    #36 0x7ffcc440883a in blink::mojom::blink::FrameWidgetStubDispatch::Accept(class blink::mojom::blink::FrameWidget *, class mojo::Message *) C:\b\s\w\ir\cache\builder\src\out\069a-Win_ASan_Releas\gen\third_party\blink\public\mojom\page\widget.mojom-blink.cc:2473:13
    #37 0x7ffcc7639197 in mojo::InterfaceEndpointClient::HandleValidatedMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1051:54
    #38 0x7ffccc78fd2a in mojo::MessageDispatcher::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43:19
    #39 0x7ffcc763f065 in mojo::InterfaceEndpointClient::HandleIncomingMessage(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:724:20
    #40 0x7ffcc7f46640 in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1202:24
    #41 0x7ffcc7f48838 in base::internal::DecayedFunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::(anonymous namespace)::ScopedUrgentMessageNotification &&>::Invoke C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:729
    #42 0x7ffcc7f48838 in base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::(anonymous namespace)::ScopedUrgentMessageNotification &&>,void,0,1,2>::MakeItSo C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:921
    #43 0x7ffcc7f48838 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::(anonymous namespace)::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification),scoped_refptr<IPC::ChannelAssociatedGroupController>,mojo::Message,IPC::(anonymous namespace)::ScopedUrgentMessageNotification>,void ()>::RunImpl C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1058
    #44 0x7ffcc7f48838 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification),IPC::ChannelAssociatedGroupController *&&,mojo::Message &&,IPC::(anonymous namespace)::ScopedUrgentMessageNotification &&>,base::internal::BindState<1,1,0,void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification),scoped_refptr<IPC::ChannelAssociatedGroupController>,mojo::Message,IPC::(anonymous namespace)::ScopedUrgentMessageNotification>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:971:12
    #45 0x7ffcc77d9c3c in base::OnceCallback<void ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156
    #46 0x7ffcc77d9c3c in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:210:34
    #47 0x7ffccc82ad04 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.h:106
    #48 0x7ffccc82ad04 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470:23
    #49 0x7ffccc829a59 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #50 0x7ffccc86ca6e in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc:40:55
    #51 0x7ffccc82c9f2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:643:12
    #52 0x7ffcc7839bee in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:134:14
    #53 0x7ffccb87aa83 in content::RendererMain(struct content::MainFunctionParams) C:\b\s\w\ir\cache\builder\src\content\renderer\renderer_main.cc:335:16
    #54 0x7ffcc55acd31 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:773:14
    #55 0x7ffcc55aef70 in content::ContentMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1142:10
    #56 0x7ffcc55a3255 in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:348:36
    #57 0x7ffcc55a3dfd in content::ContentMain(struct content::ContentMainParams) C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:361:10
    #58 0x7ffcb6521681 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:222:12
    #59 0x7ff6f98d45ed in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:201:12
    #60 0x7ff6f98d1fe4 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:352:20
    #61 0x7ff6f9ec3abb in invoke_main D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:78
    #62 0x7ff6f9ec3abb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #63 0x7ffd4bf27373  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017373)
    #64 0x7ffd4c57cc90  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cc90)

Address 0x7e85d0f00850 is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\v8\include\cppgc\member.h:44 in cppgc::internal::MemberBase<cppgc::internal::CompressedPointer>::MemberBase
Shadow bytes around the buggy address:
  0x7e85d0f00580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e85d0f00600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e85d0f00680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e85d0f00700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e85d0f00780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7e85d0f00800: 00 00 00 00 00 00 00 00 00 00[f7]f7 f7 f7 f7 f7
  0x7e85d0f00880: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e85d0f00900: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e85d0f00980: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e85d0f00a00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e85d0f00a80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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

==4988==ADDITIONAL INFO

==4988==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffcc7f38751 in IPC::ChannelAssociatedGroupController::Accept(class mojo::Message *) C:\b\s\w\ir\cache\builder\src\ipc\ipc_mojo_bootstrap.cc:1141:13

Command line: `"C:\Users\mellowroot\Desktop\win32-release_x64_asan-win32-release_x64-1405230\chrome.exe" --type=renderer --string-annotations --no-pre-read-main-dll --no-sandbox --file-url-path-alias="/gen=C:\Users\mellowroot\Desktop\win32-release_x64_asan-win32-release_x64-1405230\gen" --video-capture-use-gpu-memory-buffer --lang=sv --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1737028041293379 --launch-time-ticks=90644084040 --metrics-shmem-handle=3136,i,3122032994045002869,2675567667981578191,2097152 --field-trial-handle=3152,i,3608694310888667673,2414865939528888527,262144 --variations-seed-version --enable-logging=handle --log-file=3156 --v=1 --mojo-platform-channel-handle=3148 /prefetch:1`

==4988==END OF ADDITIONAL INFO
==4988==ABORTING

```
#### Reporter credit:

Daniel Fröjdendahl

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- chrome_debug_win10-1405230.txt (text/plain, 17.1 KB)
- chrome_debug_win10-1405230-v2.txt (text/plain, 19.0 KB)
- linux-release_asan-linux-release-1407906.txt (text/plain, 14.2 KB)
- manyHandles.PNG (image/png, 26.9 KB)
- PoC.webm (video/webm, 21.1 MB)
- test.html (text/html, 635 B)
- test.js (text/javascript, 515 B)
- variations-linux.txt (text/plain, 133.6 KB)
- 1507bb54-8016-4bda-b8be-3b9977f71f41-Stable.dmp (application/octet-stream, 4.5 MB)
- variations-local-linux.txt (text/plain, 134.0 KB)
- ASANCmdVariations.txt (text/plain, 141.0 KB)
- CanaryCmdVariations.txt (text/plain, 67.0 KB)
- postShutdown.PNG (image/png, 145.4 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-01-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6675499791089664.

### ad...@google.com (2025-01-20)

Thanks for the report - I'll try to reproduce. I've also uploaded it to ClusterFuzz in case it can do so, though I'm not too hopeful there.

### cl...@appspot.gserviceaccount.com (2025-01-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5791495462256640.

### ad...@google.com (2025-01-20)

ClusterFuzz is unwilling to accept a timeout greater than 120 seconds so I think it's unlikely to reproduce there.

### ad...@google.com (2025-01-20)

I've tried reproducing this at length but with no success. I'm going to assume it's a real bug which can be used to achieve renderer RCE, so I'm labeling as such. Since I can't reproduce it I'm unable to set an accurate FoundIn - but since the specified revision is after M133 branch point I'm going to label as impacting 134. If this also impacts earlier versions, please adjust the FoundIn field.

The call stack seems to be slightly more about style than layout, so I'm hoping andruud@, you'd be a good owner to take this further?

### pe...@google.com (2025-01-20)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2025-01-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### an...@chromium.org (2025-01-22)

I can't reproduce this either.

It *seems* that MemberBase.raw\_ is somehow poisoned here when initializing a compressed pointer (ASAN is complaining about WRITE size=4). Not sure how that's possible, since this happens in the `MakeGarbageCollected` call of the object holding that Member, though without repro I can't really investigate further.

Possibly non-actionable, but assigning to memory team for their opinion.

### pe...@google.com (2025-01-22)

The issue's primary component must be in the Component Tags, so re-adding it. To change the primary component, use the edit button at the top of the issue, just above the title.

### ml...@chromium.org (2025-01-23)

Oilpan poisons dead memory and the stack here indicates that there's an acces to this memory. This should not happen as dead memory is unreachable.

We are not aware of any bugs in the GC. Historically, these are almost always issues in Blink where some code is too smart and works around the GC API for reasons which then leads to these issues.

Let me move this into CSS as it's likely related to this area but keep it assigned to me to have a look at surrounding code.

### ml...@chromium.org (2025-01-23)

I couldn't find anything obvious, nor properly reproduce this.

We have not moved anything in GC land wrt to this area. While GC bugs did exist in the past they were exceedingly rare and for most parts there were mis-uses of the API in Blink.

I will unassign myself so that this gets back into the component queue as we just don't have the capacity to debug all the memory corruptions of Blink. What's needed here is a better repro to trace back where memory was poisoned.

### ct...@chromium.org (2025-01-24)

(Current security shepherd here.)

@reporter: Have you had any success coming up with a PoC that repros faster or more consistently? This will likely be hard for our teams to diagnose based on what is effectively just an ASAN stack trace, and may be unactionable in its current form.

### da...@gmail.com (2025-01-24)

Hello again, its so strange you're unable to reproduce as for me its working everytime I try. In an attempt of symbolizing the crash on linux I decided to build chromium locally for the first time.
Upon trying to reproduce and collect logs I noticed that it doesnt reproduce on my locally built chromium.
I wondered why, and compared the variations of the builds, which do differ quite a bit and would be my guess on its non reproduceability?
Im guessing here but "**BFCacheOpenBroadcastChannel<BackForwardCacheBroadcastChannel**" and "**KillSpareRenderOnMemoryPressure<KillSpareRenderOnMemoryPressure**" both seem like it might affect the outcome here?
Just looking at it visually on **linux\_asan\_1407906** and **win32-release\_x64-1405230** I can clearly see *iframes* being added to the page which eventually lead to the UAP. The iframes simply arnt there when I test on my locally built chromium (Linux 134.0.6974.0).

For the sake of completeness, I tested the PoC on my Stable chrome on windows ( 131.0.6778.267 (64 bits) ) which do crash the tab with an "OOM" sad-tab - the .dmp file is in the attachment.
I'll for sure do my best and change the PoC in order to reproduce on my locally built chromium too :) But please do compare variations as I'm hoping its something along these lines that might cause the non reproduce-ability.

### pe...@google.com (2025-01-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### ct...@chromium.org (2025-01-24)

It looks like BFCacheOpenBroadcastChannel<BackForwardCacheBroadcastChannel is in the fieldtrial testing config in some way so should apply to Chromium builds by default, but KillSpareRenderOnMemoryPressure is not, so it may be possible that that has some impact. I tried running linux asan r1407906 with:

`./chrome --no-sandbox --enable-logging --user-data-dir=/tmp/blrop2 --enable-features=KillSpareRenderOnMemoryPressure,BFCacheOpenBroadcastChannel --v=1 http://localhost:9003`

it took a long time (maybe about an hour on my cloudtop?) but this did finally trigger an ASAN trace:

```
=================================================================
==3845580==ERROR: AddressSanitizer: use-after-poison on address 0x7bce16e00850 at pc 0x55ced2bb74e0 bp 0x7ffe384dcbc0 sp 0x7ffe384dcbb8
WRITE of size 8 at 0x7bce16e00850 thread T0 (chrome)
==3845580==WARNING: invalid path to external symbolizer!
==3845580==WARNING: Failed to use and restart external symbolizer!
    #0 0x55ced2bb74df  (/usr/local/google/home/cthomp/asan-1407906/chrome+0x2a8824df) (BuildId: f3a509bc9c2df88c)
    #1 0x55ceda3aa924  (/usr/local/google/home/cthomp/asan-1407906/chrome+0x32075924) (BuildId: f3a509bc9c2df88c)

```

Running the test case against official Chrome Stable crashes the tab quite quickly. Looking at the crash report (crash/25abf4aa7ba1df1e) this seems to just be a OOM though.

Re-assigning back to mlippautz@ since it looks like we have a way to reproduce this now.

### aj...@google.com (2025-01-24)

Ditto repros for me on Windows - as this does take a long time i'm going to mark it as Medium.

```
=================================================================
==21228==ERROR: AddressSanitizer: use-after-poison on address 0x7ec58e6c0850 at pc 0x7fff65794f17 bp 0x00592f7ea9a0 sp 0x00592f7ea9e8
WRITE of size 4 at 0x7ec58e6c0850 thread T0
    #0 0x7fff65794f16 in blink::ComputedStyleBase::StyleRareNonInheritedUsageLessThan14PercentSubData::StyleRareNonInheritedUsageLessThan14PercentSubData(class blink::ComputedStyleBase::StyleRareNonInheritedUsageLessThan14PercentSubData const &) D:\chromium\src\out\asan\gen\third_party\blink\renderer\core\style\computed_style_base.cc:6996:7
    #1 0x7fff63ed8dbc in blink::ComputedStyleBuilderBase::SetOverflowClipMargin(class std::__Cr::optional<class blink::StyleOverflowClipMargin> &&) D:\chromium\src\out\asan\gen\third_party\blink\renderer\core\style\computed_style_base.h:15081:7
    #2 0x7fff6951761b in blink::css_longhand::OverflowClipMargin::ApplyValue(class blink::StyleResolverState &, class blink::CSSValue const &, enum blink::CSSProperty::ValueMode) const D:\chromium\src\out\asan\gen\third_party\blink\renderer\core\css\properties\longhands.cc:10700:24
    #3 0x7fff69a2ca4b in blink::StyleBuilder::ApplyPhysicalProperty(class blink::CSSProperty const &, class blink::StyleResolverState &, class blink::CSSValue const &, enum blink::CSSProperty::ValueMode) D:\chromium\src\third_party\blink\renderer\core\css\resolver\style_builder.cc:132:28
    #4 0x7fff69a3bfc9 in blink::StyleCascade::LookupAndApplyDeclaration(class blink::CSSProperty const &, class blink::CascadePriority *, class blink::CascadeResolver &) D:\chromium\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:855:3
    #5 0x7fff69a32a23 in blink::StyleCascade::ApplyMatchResult(class blink::CascadeResolver &) D:\chromium\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:695:5
    #6 0x7fff69a2d4a6 in blink::StyleCascade::Apply(class blink::CascadeFilter) D:\chromium\src\third_party\blink\renderer\core\css\resolver\style_cascade.cc:230:3
    #7 0x7fff643102db in blink::StyleResolver::ApplyPropertiesFromCascade(class blink::StyleResolverState &, class blink::StyleCascade &) D:\chromium\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:2832:11
    #8 0x7fff6430a7bb in blink::StyleResolver::ApplyBaseStyleNoCache(class blink::Element *, class blink::StyleRecalcContext const &, class blink::StyleRequest const &, class blink::StyleResolverState &, class blink::StyleCascade &) D:\chromium\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:1675:5
    #9 0x7fff643050a9 in blink::StyleResolver::ApplyBaseStyle(class blink::Element *, class blink::StyleRecalcContext const &, class blink::StyleRequest const &, class blink::StyleResolverState &, class blink::StyleCascade &) D:\chromium\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:1883:3
    #10 0x7fff64302d45 in blink::StyleResolver::ResolveStyle(class blink::Element *, class blink::StyleRecalcContext const &, class blink::StyleRequest const &) D:\chromium\src\third_party\blink\renderer\core\css\resolver\style_resolver.cc:1235:3
    #11 0x7fff5f26be0c in blink::Element::OriginalStyleForLayoutObject(class blink::StyleRecalcContext const &) D:\chromium\src\third_party\blink\renderer\core\dom\element.cc:3799:43
    #12 0x7fff5f26b4fd in blink::Element::StyleForLayoutObject(class blink::StyleRecalcContext const &) D:\chromium\src\third_party\blink\renderer\core\dom\element.cc:3756:13
    #13 0x7fff5f2709dd in blink::Element::RecalcOwnStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) D:\chromium\src\third_party\blink\renderer\core\dom\element.cc:4302:17
    #14 0x7fff5f26d75a in blink::Element::RecalcStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) D:\chromium\src\third_party\blink\renderer\core\dom\element.cc:3952:20
    #15 0x7fff5f5bc88a in blink::ContainerNode::RecalcDescendantStyles(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &, class blink::Element &) D:\chromium\src\third_party\blink\renderer\core\dom\container_node.cc:1666:22
    #16 0x7fff5f26ea3b in blink::Element::RecalcStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) D:\chromium\src\third_party\blink\renderer\core\dom\element.cc:4087:7
    #17 0x7fff5f7edf64 in blink::StyleEngine::RecalcStyle(class blink::StyleRecalcChange, class blink::StyleRecalcContext const &) D:\chromium\src\third_party\blink\renderer\core\css\style_engine.cc:3775:16
    #18 0x7fff5f7f2e1d in blink::StyleEngine::UpdateStyleAndLayoutTree(void) D:\chromium\src\third_party\blink\renderer\core\css\style_engine.cc:3934:7
    #19 0x7fff5ec3107c in blink::Document::UpdateStyle(void) D:\chromium\src\third_party\blink\renderer\core\dom\document.cc:2517:16
    #20 0x7fff5ec2da6b in blink::Document::UpdateStyleAndLayoutTreeForThisDocument(void) D:\chromium\src\third_party\blink\renderer\core\dom\document.cc:2455:3
    #21 0x7fff5ee1228d in blink::LocalFrameView::UpdateStyleAndLayoutInternal(void) D:\chromium\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3214:30
    #22 0x7fff5edfaea6 in blink::LocalFrameView::UpdateStyleAndLayout(void) D:\chromium\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3158:18
    #23 0x7fff5ee0cdca in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive(void) D:\chromium\src\third_party\blink\renderer\core\frame\local_frame_view.cc:3081:3
    #24 0x7fff5ee09b42 in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases(enum blink::DocumentLifecycle::LifecycleState) D:\chromium\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2524:3
    #25 0x7fff5ee089f7 in blink::LocalFrameView::UpdateLifecyclePhasesInternal(enum blink::DocumentLifecycle::LifecycleState) D:\chromium\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2268:9
    #26 0x7fff5ee0434f in blink::LocalFrameView::UpdateLifecyclePhases(enum blink::DocumentLifecycle::LifecycleState, enum blink::DocumentUpdateReason) D:\chromium\src\third_party\blink\renderer\core\frame\local_frame_view.cc:2201:3
    #27 0x7fff5eee928d in blink::LayoutView::HitTest(class blink::HitTestLocation const &, class blink::HitTestResult &) D:\chromium\src\third_party\blink\renderer\core\layout\layout_view.cc:143:24
    #28 0x7fff5ec56bda in blink::Document::PerformMouseEventHitTest(class blink::HitTestRequest const &, struct blink::PhysicalOffset const &, class blink::WebMouseEvent const &) D:\chromium\src\third_party\blink\renderer\core\dom\document.cc:4904:20
    #29 0x7fff5f15df32 in blink::EventHandler::GetMouseEventTarget(class blink::HitTestRequest const &, class blink::WebMouseEvent const &) D:\chromium\src\third_party\blink\renderer\core\input\event_handler.cc:2592:33
    #30 0x7fff5f160c72 in blink::EventHandler::HandleMouseMoveOrLeaveEvent(class blink::WebMouseEvent const &, class WTF::Vector<class blink::WebMouseEvent, 0, class WTF::PartitionAllocator> const &, class WTF::Vector<class blink::WebMouseEvent, 0, class WTF::PartitionAllocator> const &, class blink::HitTestResult *, class blink::HitTestLocation *) D:\chromium\src\third_party\blink\renderer\core\input\event_handler.cc:1149:11
    #31 0x7fff5f15f400 in blink::EventHandler::HandleMouseMoveEvent(class blink::WebMouseEvent const &, class WTF::Vector<class blink::WebMouseEvent, 0, class WTF::PartitionAllocator> const &, class WTF::Vector<class blink::WebMouseEvent, 0, class WTF::PartitionAllocator> const &) D:\chromium\src\third_party\blink\renderer\core\input\event_handler.cc:1011:7
    #32 0x7fff648932aa in blink::WidgetEventHandler::HandleMouseMove(class blink::LocalFrame &, class blink::WebMouseEvent const &, class std::__Cr::vector<class std::__Cr::unique_ptr<class blink::WebInputEvent, struct std::__Cr::default_delete<class blink::WebInputEvent>>, class std::__Cr::allocator<class std::__Cr::unique_ptr<class blink::WebInputEvent, struct std::__Cr::default_delete<class blink::WebInputEvent>>>> const &, class std::__Cr::vector<class std::__Cr::unique_ptr<class blink::WebInputEvent, struct std::__Cr::default_delete<class blink::WebInputEvent>>, class std::__Cr::allocator<class std::__Cr::unique_ptr<class blink::WebInputEvent, struct std::__Cr::default_delete<class blink::WebInputEvent>>>> const &) D:\chromium\src\third_party\blink\renderer\core\input\widget_event_handler.cc:155:32
    #33 0x7fff64892745 in blink::WidgetEventHandler::HandleInputEvent(class blink::WebCoalescedInputEvent const &, class blink::LocalFrame *) D:\chromium\src\third_party\blink\renderer\core\input\widget_event_handler.cc:68:7
    #34 0x7fff5edab83f in blink::WebFrameWidgetImpl::HandleInputEvent(class blink::WebCoalescedInputEvent const &) D:\chromium\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:3165:30
    #35 0x7fff649282ec in blink::WidgetBaseInputHandler::HandleInputEvent(class blink::WebCoalescedInputEvent const &, class std::__Cr::unique_ptr<class cc::EventMetrics, struct std::__Cr::default_delete<class cc::EventMetrics>>, class base::OnceCallback<(enum blink::mojom::InputEventResultState, class ui::LatencyInfo const &, class std::__Cr::unique_ptr<struct blink::InputHandlerProxy::DidOverscrollParams, struct std::__Cr::default_delete<struct blink::InputHandlerProxy::DidOverscrollParams>>, class std::__Cr::optional<enum cc::TouchAction>)>) D:\chromium\src\third_party\blink\renderer\platform\widget\input\widget_base_input_handler.cc:416:40
    #36 0x7fff648995b1 in blink::WidgetInputHandlerManager::HandleInputEvent(class blink::WebCoalescedInputEvent const &, class std::__Cr::unique_ptr<class cc::EventMetrics, struct std::__Cr::default_delete<class cc::EventMetrics>>, class base::OnceCallback<(enum blink::mojom::InputEventResultState, class ui::LatencyInfo const &, class mojo::StructPtr<class blink::mojom::blink::DidOverscrollParams>, class std::__Cr::optional<enum cc::TouchAction>)>) D:\chromium\src\third_party\blink\renderer\platform\widget\input\widget_input_handler_manager.cc:422:28
    #37 0x7fff6490a69d in blink::MainThreadEventQueue::HandleEventOnMainThread(class blink::WebCoalescedInputEvent const &, class blink::WebInputEventAttribution const &, class std::__Cr::unique_ptr<class cc::EventMetrics, struct std::__Cr::default_delete<class cc::EventMetrics>>, class base::OnceCallback<(enum blink::mojom::InputEventResultState, class ui::LatencyInfo const &, class mojo::StructPtr<class blink::mojom::blink::DidOverscrollParams>, class std::__Cr::optional<enum cc::TouchAction>)>) D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:794:24
    #38 0x7fff6490ed73 in blink::QueuedWebInputEvent::Dispatch(class blink::MainThreadEventQueue *) D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:191:17
    #39 0x7fff649083e0 in blink::MainThreadEventQueue::DispatchEvents(void) D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:568:11
    #40 0x7fff649158f2 in base::internal::Invoker<struct base::internal::FunctorTraits<void (__cdecl blink::MainThreadEventQueue::*&&)(void), class blink::MainThreadEventQueue *&&>, struct base::internal::BindState<1, 1, 0, void (__cdecl blink::MainThreadEventQueue::*)(void), class scoped_refptr<class blink::MainThreadEventQueue>>, (void)>::RunOnce(class base::internal::BindStateBase *) D:\chromium\src\base\functional\bind_internal.h:971:12
    #41 0x7fff547f0e31 in base::TaskAnnotator::RunTaskImpl(struct base::PendingTask &) D:\chromium\src\base\task\common\task_annotator.cc:210:34
    #42 0x7fff5ab2ee4c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::LazyNow *) D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:470:23
    #43 0x7fff5ab2d65a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330:40
    #44 0x7fff5ab848b2 in base::MessagePumpDefault::Run(class base::MessagePump::Delegate *) D:\chromium\src\base\message_loop\message_pump_default.cc:42:55
    #45 0x7fff5ab30f02 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:643:12
    #46 0x7fff54886529 in base::RunLoop::Run(class base::Location const &) D:\chromium\src\base\run_loop.cc:134:14
    #47 0x7fff59700cb0 in content::RendererMain(struct content::MainFunctionParams) D:\chromium\src\content\renderer\renderer_main.cc:351:16
    #48 0x7fff51b1ab08 in content::RunOtherNamedProcessTypeMain(class std::__Cr::basic_string<char, struct std::__Cr::char_traits<char>, class std::__Cr::allocator<char>> const &, struct content::MainFunctionParams, class content::ContentMainDelegate *) D:\chromium\src\content\app\content_main_runner_impl.cc:773:14
    #49 0x7fff51b1dbc9 in content::ContentMainRunnerImpl::Run(void) D:\chromium\src\content\app\content_main_runner_impl.cc:1145:10
    #50 0x7fff51b0e6ba in content::RunContentProcess(struct content::ContentMainParams, class content::ContentMainRunner *) D:\chromium\src\content\app\content_main.cc:348:36
    #51 0x7fff51b0eebe in content::ContentMain(struct content::ContentMainParams) D:\chromium\src\content\app\content_main.cc:361:10
    #52 0x7fff3dbf17bb in ChromeMain D:\chromium\src\chrome\app\chrome_main.cc:222:12
    #53 0x7ff66d294a0e in MainDllLoader::Launch(struct HINSTANCE__*, class base::TimeTicks) D:\chromium\src\chrome\app\main_dll_loader_win.cc:201:12
    #54 0x7ff66d2923dd in main D:\chromium\src\chrome\app\chrome_exe_main_win.cc:352:20
    #55 0x7ff66d9e31bb in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #56 0x7ff821fe259c  (C:\WINDOWS\System32\KERNEL32.DLL+0x18001259c)
    #57 0x7ff8236aaf37  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18005af37)

Address 0x7ec58e6c0850 is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison D:\chromium\src\out\asan\gen\third_party\blink\renderer\core\style\computed_style_base.cc:6996:7 in blink::ComputedStyleBase::StyleRareNonInheritedUsageLessThan14PercentSubData::StyleRareNonInheritedUsageLessThan14PercentSubData(class blink::ComputedStyleBase::StyleRareNonInheritedUsageLessThan14PercentSubData const &)
Shadow bytes around the buggy address:
  0x7ec58e6c0580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ec58e6c0600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ec58e6c0680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ec58e6c0700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ec58e6c0780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ec58e6c0800: 00 00 00 00 00 00 00 00 00 00[f7]f7 f7 f7 f7 f7
  0x7ec58e6c0880: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ec58e6c0900: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ec58e6c0980: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ec58e6c0a00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ec58e6c0a80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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

==21228==ADDITIONAL INFO

==21228==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fff64906f5a in blink::MainThreadEventQueue::QueueClosure(class base::OnceCallback<(void)>) D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:521:5
    #1 0x7fff54b8ffff in mojo::SimpleWatcher::Context::Notify(unsigned int, struct MojoHandleSignalsState, unsigned int) D:\chromium\src\mojo\public\cpp\system\simple_watcher.cc:102:13


Command line: `"d:\chromium\src\out\Asan\chrome.exe" --type=renderer --user-data-dir="d:\temp\asan-profile" --enable-dinosaur-easter-egg-alt-images --no-pre-read-main-dll --no-sandbox --enable-blink-features=MojoJS --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=1 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1736381809671507 --launch-time-ticks=1364987808056 --metrics-shmem-handle=3328,i,10625246121598558423,3691858493217921350,2097152 --field-trial-handle=1976,i,7652723820714088891,16028158892933470956,262144 --variations-seed-version --enable-logging=handle --log-file=3336 --v=1 --mojo-platform-channel-handle=3324 /prefetch:1`


==21228==END OF ADDITIONAL INFO
==21228==ABORTING

```

### ml...@chromium.org (2025-01-24)

I am inclined to think this is the same as [issue 391018461](https://issues.chromium.org/issues/391018461) which I have debugged today.

The symptoms are the same:

- Long running, requiring 4G+ heap.
- Large stack (likely triggering a GC somewhere along the way)
- UAP on something that (likely) has been allocated recently.

Can you try reproducing once <https://chromiumdash.appspot.com/commits?commit=dc2bf8b84f69728863e5e679d4488e3e0fb40b6c&platform=Windows> makes it onto a Canary?

The broken code has not made it past Dev, which also matches that Stable just crashes with OOM.

### pe...@google.com (2025-01-30)

The NextAction date has arrived: 2025-01-30
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### da...@gmail.com (2025-01-31)

#19 - is there something I need to retest? I can see it 'Needs-Feedback' label was added yesterday :)

### pe...@google.com (2025-01-31)

Thank you for providing more feedback. Adding the requester to the CC list.

### ml...@chromium.org (2025-01-31)

I could not reproduce this issue in here but fixed a bug. The fix has made it to Canary and Dev (see [comment #19](https://issues.chromium.org/issues/390633126#comment19)).

It would be amazing if you could check if the issue still persists.

### da...@gmail.com (2025-01-31)

Hello again! After some retests on Windows10, Canary (134.0.6990.2) and ASAN-1414083 (134.0.6991.0) I can conclude that I **cannot reproduce** the UAP. It is hard for me to tell if the patch is working or if there's some cmd-variations at play here that could cause it to not reproduce (as it did for triage at first - my apologizes but I learned something here!).
As for memory allocations I guess it is assumed to allocate a lot, as well as the many handles. I do have to kill the last process of chromium.exe (and chrome.exe on canary) manually via task-manager as even post shutdown of chrome there's one process still lurking around, obviously something minor compared to the actual UAP, **See image attached**. I also attached the **cmdline-variations** incase I did something wrong here.

To conclude: **Not reproduceable** on windows 10

### pe...@google.com (2025-01-31)

Thank you for providing more feedback. Adding the requester to the CC list.

### ml...@chromium.org (2025-02-03)

Thanks for clarifying in [comment #24](https://issues.chromium.org/issues/390633126#comment24). I think this is the same as [issue 391018461](https://issues.chromium.org/issues/391018461). I will just mark this as fixed and update the component here.

### pe...@google.com (2025-02-05)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

- M134, which branched on 2025-02-03 (Chromium branch: 6998, Chromium branch position: 1415337)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at <https://chromiumdash.appspot.com/schedule>).

To learn more about the merge process, including how to land any required merges, see <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>.

### pe...@google.com (2025-02-05)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M134. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [134].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ml...@chromium.org (2025-02-05)

This is the same as [issue 391018461](https://issues.chromium.org/issues/391018461) and there's no merge needed.

I didn't dupe the bug to make it easier to see timelines for potential VRP rewards.

### sp...@google.com (2025-02-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of moderately mitigated memory corruption in a sandboxed process / the renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-06)

Congratulations! Thank you for this report. Given the timing issues to reproduce and, therefore, the lessened potential for attacker control and exploitability in a real world scenario, we consider this a moderately mitigated issue and have rewarded it accordingly. Thank you for your efforts and reporting this issue to us!

### da...@gmail.com (2025-02-06)

Yay! Thank you for the bounty - Hopefully the one first out of many :)

Some simple questions, just so I can learn more:

1. Besides time (understandably a mitigating factor) was there a experimental flag (KillSpareRenderOnMemoryPressure) here that also mitigated the issue?
2. Ive seen these chromium T-Shirts posted on social media - how would one go about obtaining one of these? :P (I think it'll do very well for question 3)
3. I was thinking of doing a smaller write-up for this, obviously I'll wait until its OK to publish ~90 days?

This has been fun and a humbling learning experience :) again thanks!

### ml...@chromium.org (2025-02-06)

> Besides time (understandably a mitigating factor) was there a experimental flag (KillSpareRenderOnMemoryPressure) here that also mitigated the issue?

The bug requires heaps >4G and certain conditions in the object graph. Killing a renderer before running into such "memory pressure" would have mitigated it. I do not know whether `KillSpareRenderOnMemoryPressure` is enough to mitigate this completely.

### pe...@google.com (2025-02-06)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

- M134, which branched on 2025-02-03 (Chromium branch: 6998, Chromium branch position: 1415337)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at <https://chromiumdash.appspot.com/schedule>).

To learn more about the merge process, including how to land any required merges, see <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>.

### ml...@chromium.org (2025-02-06)

Broken code landed in M134: <https://chromium-review.googlesource.com/c/v8/v8/+/6164787>

Fix landed in M134: <https://chromium-review.googlesource.com/6198226>

### am...@chromium.org (2025-02-06)

> 2. Ive seen these chromium T-Shirts posted on social media - how would one go about obtaining one of these? :P (I think it'll do very well for question 3)

Since #1 was already answered above, I'll respond to #2 and #3
I'm assuming you mean the Chrome VRP t-shirt. We just did our first run of those for our top n researchers of 2024 + other meaningful contributions from last year, such as interesting Chromium related security conference talks we saw, etc.
So if you're a top reporter in 2025 or speak at a conference, we will likely do another run of these later in the year for those contributions.

> 3. I was thinking of doing a smaller write-up for this, obviously I'll wait until its OK to publish ~90 days?
>    We would request that you wait until this issue is publicly disclosed, which is 14 weeks when the bug is fixed.
>    That will happen automatically, by my math, on 5 May 2025. Though this report in particular was closed on 4 February, so that will actually happen automatically on 14 May.

To be transparent other report, provided by another VRP reporter will be automatically opened earlier than this report since that was the issue the fix was landed on.
We extended a reward for this issue, based on the demonstration provided, since this issue was reported two days earlier. The other report provided a different demonstration which facilitated the fix, and in absence of knowing about this report, we had already rewarded this issue based on that report.

### pe...@google.com (2025-02-07)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

- M134, which branched on 2025-02-03 (Chromium branch: 6998, Chromium branch position: 1415337)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove TBD-## from the Merge field and replace it with NA-## (where ## corresponds to the milestone under evaluation). If a merge is necessary, the requested milestone(s) to the Merge-Request field. If you're not sure, reach out to the relevant release manager (can be found at <https://chromiumdash.appspot.com/schedule>).

To learn more about the merge process, including how to land any required merges, see <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>.

### da...@gmail.com (2025-02-22)

redacted

### ch...@google.com (2025-05-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of moderately mitigated memory corruption in a sandboxed process / the renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/390633126)*
