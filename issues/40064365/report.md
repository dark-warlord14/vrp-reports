# Security: UAF in content::BrowserPluginGuest::GetProspectiveOuterDocument()  in browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [40064365](https://issues.chromium.org/issues/40064365) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Apps>BrowserTag, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2023-05-04 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in content::BrowserPluginGuest::GetProspectiveOuterDocument() in browser process

**VERSION**  

Chromium 115.0.5751.0 (Developer Build) (64-bit)  

Revision 2ad890f4358ed25b5376d658a007d5cd9b968e27-refs/heads/main@{#1139369}  

OS Linux

**REPRODUCTION CASE**

1. put manifest.json,background.js,index.html into extension path.
2. put poc.html in the webserver path and run `python3 -m http.server 8000`
3. run the command:  
   
   chrome --user-data-dir=/tmp/any --enable-tracing --load-extension="webview\_extension\_path"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser.]

# [2815759:2815759:0504/160335.314280:ERROR:chrome\_browser\_cloud\_management\_controller.cc(162)] Cloud management controller initialization aborted as CBCM is not enabled. [2815759:2815759:0504/160335.768580:ERROR:object\_proxy.cc(590)] Failed to call method: org.freedesktop.portal.Settings.Read: object\_path= /org/freedesktop/portal/desktop: org.freedesktop.portal.Error.NotFound: Requested setting not found [2815832:8:0504/160336.124707:ERROR:command\_buffer\_proxy\_impl.cc(128)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.

==2815759==ERROR: AddressSanitizer: heap-use-after-free on address 0x6190004b5f80 at pc 0x55e2f93aa69f bp 0x7ffc6ca63fd0 sp 0x7ffc6ca63fc8  

READ of size 1 at 0x6190004b5f80 thread T0 (chrome)  

==2815759==WARNING: invalid path to external symbolizer!  

==2815759==WARNING: Failed to use and restart external symbolizer!  

#0 0x55e2f93aa69e in base::internal::(anonymous namespace)::CrashImmediatelyOnUseAfterFree(unsigned long) *asan\_rtl*:17  

#1 0x55e2f93aa1f9 in base::internal::(anonymous namespace)::SafelyUnwrapForDereference(unsigned long) *asan\_rtl*:5  

#2 0x55e2f09ada4a in SafelyUnwrapPtrForDereference[content::BrowserPluginGuestDelegate](javascript:void(0);) ./../../base/allocator/partition\_allocator/pointers/raw\_ptr\_hookable\_impl.h:75:7  

#3 0x55e2f09ada4a in GetForDereference ./../../base/allocator/partition\_allocator/pointers/raw\_ptr.h:1023:12  

#4 0x55e2f09ada4a in operator-> ./../../base/allocator/partition\_allocator/pointers/raw\_ptr.h:791:12  

#5 0x55e2f09ada4a in content::BrowserPluginGuest::GetProspectiveOuterDocument() ./../../content/browser/browser\_plugin/browser\_plugin\_guest.cc:101:7  

#6 0x55e2f2618aa4 in GetProspectiveOuterDocument ./../../content/browser/web\_contents/web\_contents\_impl.cc:9529:36  

#7 0x55e2f2618aa4 in non-virtual thunk to content::WebContentsImpl::GetProspectiveOuterDocument() ./../../content/browser/web\_contents/web\_contents\_impl.cc:0:0  

#8 0x55e2f19caa86 in content::FrameTreeNode::GetParentOrOuterDocumentHelper(bool, bool) const ./../../content/browser/renderer\_host/frame\_tree\_node.cc:382:34  

#9 0x55e2f1d9944b in content::RenderFrameHostImpl::WriteIntoTrace(perfetto::TracedProto[perfetto::protos::pbzero::RenderFrameHost](javascript:void(0);)) const ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:5877:31  

#10 0x55e2f186891d in WriteImpl<content::RenderFrameHostImpl &> ./../../third\_party/perfetto/include/perfetto/tracing/traced\_value.h:341:9  

#11 0x55e2f186891d in WriteIntoTracedValue<content::RenderFrameHostImpl &> ./../../third\_party/perfetto/include/perfetto/tracing/traced\_value.h:483:3  

#12 0x55e2f186891d in WriteIntoTrace ./../../third\_party/perfetto/include/perfetto/tracing/traced\_value.h:670:5  

#13 0x55e2f186891d in decltype(TraceFormatTraits<perfetto::base::remove\_cvref[content::RenderFrameHostImpl\\*&](javascript:void(0);)::type>::WriteIntoTrace(decltype(std::\_\_declval[content::RenderFrameHostImpl\\*&](javascript:void(0);)(0)) std::Cr::declval[perfetto::TracedValue](javascript:void(0);)()(), std::declval[content::RenderFrameHostImpl\\*&](javascript:void(0);)()), (void)()) perfetto::internal::WriteImpl[content::RenderFrameHostImpl\\*&](javascript:void(0);)(perfetto::base::priority\_tag<3ul>, perfetto::TracedValue, content::RenderFrameHostImpl\*&) ./../../third\_party/perfetto/include/perfetto/tracing/traced\_value.h:364:3  

#14 0x55e2f18686ad in WriteIntoTracedValue<content::RenderFrameHostImpl \*&> ./../../third\_party/perfetto/include/perfetto/tracing/traced\_value.h:483:3  

#15 0x55e2f18686ad in void perfetto::EventContext::AddDebugAnnotation<char const\*&, content::RenderFrameHostImpl\*&>(char const\*&, content::RenderFrameHostImpl\*&) ./../../third\_party/perfetto/include/perfetto/tracing/event\_context.h:118:5  

#16 0x55e2f1c4e8b0 in WriteTrackEventArgs<content::RenderFrameHostImpl \*&> ./../../third\_party/perfetto/include/perfetto/tracing/internal/write\_track\_event\_args.h:171:13  

#17 0x55e2f1c4e8b0 in operator() ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:766:11  

#18 0x55e2f1c4e8b0 in void perfetto::DataSource<base::perfetto\_track\_event::TrackEvent, perfetto::internal::TrackEventDataSourceTraits>::TraceWithInstances<perfetto::internal::TrackEventDataSource<base::perfetto\_track\_event::TrackEvent, &base::perfetto\_track\_event::internal::kCategoryRegistry>::CategoryTracePointTraits, void perfetto::internal::TrackEventDataSource<base::perfetto\_track\_event::TrackEvent, &base::perfetto\_track\_event::internal::kCategoryRegistry>::TraceForCategoryImpl<unsigned long, perfetto::StaticString, perfetto::Track, perfetto::TraceTimestamp, void, void, char const (&) [18], content::RenderFrameHostImpl\*&>(unsigned int, unsigned long const&, perfetto::StaticString const&, perfetto::protos::pbzero::perfetto\_pbzero\_enum\_TrackEvent::Type, perfetto::Track const&, perfetto::TraceTimestamp const&, char const (&) [18], content::RenderFrameHostImpl\*&)::'lambda'(perfetto::DataSource<base::perfetto\_track\_event::TrackEvent, perfetto::internal::TrackEventDataSourceTraits>::TraceContext)>(unsigned int, perfetto::StaticString, unsigned long::TracePointData) ./../../third\_party/perfetto/include/perfetto/tracing/data\_source.h:395:7  

#19 0x55e2f1c4dd8c in TraceWithInstances<unsigned long, (lambda at ../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:756:30)> ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:779:7  

#20 0x55e2f1c4dd8c in TraceForCategoryImpl<unsigned long, perfetto::StaticString, perfetto::Track, perfetto::TraceTimestamp, void, void, const char (&)[18], content::RenderFrameHostImpl \*&> ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:755:5  

#21 0x55e2f1c4dd8c in void perfetto::internal::TrackEventDataSource<base::perfetto\_track\_event::TrackEvent, &base::perfetto\_track\_event::internal::kCategoryRegistry>::TraceForCategory<unsigned long, perfetto::StaticString, char const (&) [18], content::RenderFrameHostImpl\*&>(unsigned int, unsigned long const&, perfetto::StaticString const&, perfetto::protos::pbzero::perfetto\_pbzero\_enum\_TrackEvent::Type, char const (&) [18], content::RenderFrameHostImpl\*&) ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:330:5  

#22 0x55e2f25e1afc in operator() ./../../content/browser/web\_contents/web\_contents\_impl.cc:7011:3  

#23 0x55e2f25e1afc in operator() ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:307:43  

#24 0x55e2f25e1afc in CallIfEnabled<perfetto::internal::TrackEventDataSource<base::perfetto\_track\_event::TrackEvent, &base::perfetto\_track\_event::internal::kCategoryRegistry>::CategoryTracePointTraits, (lambda at ../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:307:9)> ./../../third\_party/perfetto/include/perfetto/tracing/data\_source.h:365:5  

#25 0x55e2f25e1afc in CallIfCategoryEnabled<(lambda at ../../content/browser/web\_contents/web\_contents\_impl.cc:7011:3)> ./../../third\_party/perfetto/include/perfetto/tracing/internal/track\_event\_data\_source.h:306:5  

#26 0x55e2f25e1afc in operator() ./../../content/browser/web\_contents/web\_contents\_impl.cc:7011:3  

#27 0x55e2f25e1afc in content::WebContentsImpl::RenderFrameDeleted(content::RenderFrameHostImpl\*) ./../../content/browser/web\_contents/web\_contents\_impl.cc:7011:3  

#28 0x55e2f1d7229d in content::RenderFrameHostImpl::RenderFrameDeleted() ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:3498:16  

#29 0x55e2f19bdf64 in content::FrameTree::Shutdown() ./../../content/browser/renderer\_host/frame\_tree.cc:987:39  

#30 0x55e2f2553712 in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1140:23  

#31 0x55e2f2556fcd in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1073:37  

#32 0x55e2f26b93d6 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#33 0x55e2f26b93d6 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#34 0x55e2f26b93d6 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#35 0x55e2f26b93d6 in ~CreatedWindow ./../../content/browser/web\_contents/web\_contents\_impl.cc:557:31  

#36 0x55e2f26b93d6 in ~pair ./../../buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:77:29  

#37 0x55e2f26b93d6 in \_\_destroy\_at<std::Cr::pair<const content::GlobalRoutingID, content::CreatedWindow>, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:66:13  

#38 0x55e2f26b93d6 in destroy\_at<std::Cr::pair<const content::GlobalRoutingID, content::CreatedWindow>, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:101:5  

#39 0x55e2f26b93d6 in destroy<std::Cr::pair<const content::GlobalRoutingID, content::CreatedWindow>, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:323:9  

#40 0x55e2f26b93d6 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<content::GlobalRoutingID, content::CreatedWindow>, std::Cr::\_\_map\_value\_compare<content::GlobalRoutingID, std::Cr::\_\_value\_type<content::GlobalRoutingID, content::CreatedWindow>, std::Cr::less[content::GlobalRoutingID](javascript:void(0);), true>, std::Cr::allocator<std::Cr::\_\_value\_type<content::GlobalRoutingID, content::CreatedWindow>>>::destroy(std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<content::GlobalRoutingID, content::CreatedWindow>, void\*>\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1811:9  

#41 0x55e2f255462e in ~\_\_tree ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1799:3  

#42 0x55e2f255462e in ~map ./../../buildtools/third\_party/libc++/trunk/include/map:1175:5  

#43 0x55e2f255462e in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1184:1  

#44 0x55e2f2556fcd in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1073:37  

#45 0x55e2f254f026 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#46 0x55e2f254f026 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#47 0x55e2f254f026 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#48 0x55e2f254f026 in content::WebContentsImpl::WebContentsTreeNode::OnFrameTreeNodeDestroyed(content::FrameTreeNode\*) ./../../content/browser/web\_contents/web\_contents\_impl.cc:845:3  

#49 0x55e2f19c8111 in content::FrameTreeNode::~FrameTreeNode() ./../../content/browser/renderer\_host/frame\_tree\_node.cc:262:14  

#50 0x55e2f19c9ecd in content::FrameTreeNode::~FrameTreeNode() ./../../content/browser/renderer\_host/frame\_tree\_node.cc:211:33  

#51 0x55e2f1d5be16 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#52 0x55e2f1d5be16 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#53 0x55e2f1d5be16 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#54 0x55e2f1d5be16 in \_\_destroy\_at<std::Cr::unique\_ptr<content::FrameTreeNode, std::Cr::default\_delete[content::FrameTreeNode](javascript:void(0);) >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:66:13  

#55 0x55e2f1d5be16 in destroy\_at<std::Cr::unique\_ptr<content::FrameTreeNode, std::Cr::default\_delete[content::FrameTreeNode](javascript:void(0);) >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:101:5  

#56 0x55e2f1d5be16 in destroy<std::Cr::unique\_ptr<content::FrameTreeNode, std::Cr::default\_delete[content::FrameTreeNode](javascript:void(0);) >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:323:9  

#57 0x55e2f1d5be16 in \_\_base\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:838:9  

#58 0x55e2f1d5be16 in \_\_clear ./../../buildtools/third\_party/libc++/trunk/include/vector:832:29  

#59 0x55e2f1d5be16 in operator() ./../../buildtools/third\_party/libc++/trunk/include/vector:448:20  

#60 0x55e2f1d5be16 in ~vector ./../../buildtools/third\_party/libc++/trunk/include/vector:458:67  

#61 0x55e2f1d5be16 in content::RenderFrameHostImpl::ResetChildren() ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:4392:1  

#62 0x55e2f19bdf18 in content::FrameTree::Shutdown() ./../../content/browser/renderer\_host/frame\_tree.cc:976:39  

#63 0x55e2f2553712 in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1140:23  

#64 0x55e2f2556fcd in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1073:37  

#65 0x55e2f452d46c in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#66 0x55e2f452d46c in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#67 0x55e2f452d46c in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#68 0x55e2f452d46c in ~AppWindowContentsImpl ./../../extensions/browser/app\_window/app\_window\_contents.cc:29:47  

#69 0x55e2f452d46c in extensions::AppWindowContentsImpl::~AppWindowContentsImpl() ./../../extensions/browser/app\_window/app\_window\_contents.cc:29:47  

#70 0x55e2f452455b in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#71 0x55e2f452455b in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#72 0x55e2f452455b in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#73 0x55e2f452455b in extensions::AppWindow::~AppWindow() ./../../extensions/browser/app\_window/app\_window.cc:336:1  

#74 0x55e2f452480d in extensions::AppWindow::~AppWindow() ./../../extensions/browser/app\_window/app\_window.cc:334:25  

#75 0x55e2f4526736 in extensions::AppWindow::OnNativeClose() ./../../extensions/browser/app\_window/app\_window.cc:498:3  

#76 0x55e310d96e26 in operator() ./../../extensions/components/native\_app\_window/native\_app\_window\_views.cc:53:30  

#77 0x55e310d96e26 in Invoke<(lambda at ../../extensions/components/native\_app\_window/native\_app\_window\_views.cc:51:7), native\_app\_window::NativeAppWindowViews \*> ./../../base/functional/bind\_internal.h:621:12  

#78 0x55e310d96e26 in MakeItSo<(lambda at ../../extensions/components/native\_app\_window/native\_app\_window\_views.cc:51:7), std::Cr::tuple<base::internal::UnretainedWrapper<native\_app\_window::NativeAppWindowViews, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > > ./../../base/functional/bind\_internal.h:925:12  

#79 0x55e310d96e26 in RunImpl<(lambda at ../../extensions/components/native\_app\_window/native\_app\_window\_views.cc:51:7), std::Cr::tuple<base::internal::UnretainedWrapper<native\_app\_window::NativeAppWindowViews, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#80 0x55e310d96e26 in base::internal::Invoker<base::internal::BindState<native\_app\_window::NativeAppWindowViews::Init(extensions::AppWindow\*, extensions::AppWindow::CreateParams const&)::$\_0, base::internal::UnretainedWrapper<native\_app\_window::NativeAppWindowViews, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#81 0x55e304a88712 in Run ./../../base/functional/callback.h:152:12  

#82 0x55e304a88712 in views::WidgetDelegate::DeleteDelegate() ./../../ui/views/widget/widget\_delegate.cc:233:25  

#83 0x55e304a6e311 in views::Widget::OnNativeWidgetDestroyed() ./../../ui/views/widget/widget.cc:1600:25  

#84 0x55e304b379c9 in views::DesktopNativeWidgetAura::OnHostClosed() ./../../ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc:391:30  

#85 0x55e304b25d1b in views::DesktopWindowTreeHostPlatform::OnClosed() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:847:32  

#86 0x55e304b1e3fc in views::DesktopWindowTreeHostPlatform::CloseNow() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:406:22  

#87 0x55e304b2a023 in Invoke<void (views::DesktopWindowTreeHostPlatform::\*)(), const base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) &> ./../../base/functional/bind\_internal.h:746:12  

#88 0x55e304b2a023 in MakeItSo<void (views::DesktopWindowTreeHostPlatform::\*)(), std::Cr::tuple<base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) > > ./../../base/functional/bind\_internal.h:953:5  

#89 0x55e304b2a023 in RunImpl<void (views::DesktopWindowTreeHostPlatform::\*)(), std::Cr::tuple<base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#90 0x55e304b2a023 in base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostPlatform::\*)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);)>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#91 0x55e2f94d91b7 in Run ./../../base/functional/callback.h:152:12  

#92 0x55e2f94d91b7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#93 0x55e2f95459f5 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#94 0x55e2f95459f5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#95 0x55e2f9544915 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#96 0x55e2f9546a34 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#97 0x55e2f96c2cf4 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:670:48  

#98 0x55e2f9547769 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:651:12  

#99 0x55e2f9456855 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#100 0x55e2f09a3293 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1067:18  

#101 0x55e2f09ab076 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:158:15  

#102 0x55e2f0999eea in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:28  

#103 0x55e2f686b234 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:706:10  

#104 0x55e2f686f834 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1276:10  

#105 0x55e2f686f07d in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1130:12  

#106 0x55e2f6867fbf in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#107 0x55e2f6868530 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#108 0x55e2e77c33e6 in ChromeMain ./../../chrome/app/chrome\_main.cc:187:12  

#109 0x7fbf9344c082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6190004b5f80 is located 0 bytes inside of 904-byte region [0x6190004b5f80,0x6190004b6308)  

freed by thread T0 (chrome) here:  

#0 0x55e2e77c118d in operator delete(void\*) *asan\_rtl*:3  

#1 0x55e2f255682b in void content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)()>(void (content::WebContentsObserver::\*)()) ./../../content/browser/web\_contents/web\_contents\_impl.h:1556:9  

#2 0x55e2f2553966 in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1181:14  

#3 0x55e2f2556fcd in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1073:37  

#4 0x55e2f254f026 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#5 0x55e2f254f026 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#6 0x55e2f254f026 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#7 0x55e2f254f026 in content::WebContentsImpl::WebContentsTreeNode::OnFrameTreeNodeDestroyed(content::FrameTreeNode\*) ./../../content/browser/web\_contents/web\_contents\_impl.cc:845:3  

#8 0x55e2f19c8111 in content::FrameTreeNode::~FrameTreeNode() ./../../content/browser/renderer\_host/frame\_tree\_node.cc:262:14  

#9 0x55e2f19c9ecd in content::FrameTreeNode::~FrameTreeNode() ./../../content/browser/renderer\_host/frame\_tree\_node.cc:211:33  

#10 0x55e2f1d5be16 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#11 0x55e2f1d5be16 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#12 0x55e2f1d5be16 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#13 0x55e2f1d5be16 in \_\_destroy\_at<std::Cr::unique\_ptr<content::FrameTreeNode, std::Cr::default\_delete[content::FrameTreeNode](javascript:void(0);) >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:66:13  

#14 0x55e2f1d5be16 in destroy\_at<std::Cr::unique\_ptr<content::FrameTreeNode, std::Cr::default\_delete[content::FrameTreeNode](javascript:void(0);) >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:101:5  

#15 0x55e2f1d5be16 in destroy<std::Cr::unique\_ptr<content::FrameTreeNode, std::Cr::default\_delete[content::FrameTreeNode](javascript:void(0);) >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:323:9  

#16 0x55e2f1d5be16 in \_\_base\_destruct\_at\_end ./../../buildtools/third\_party/libc++/trunk/include/vector:838:9  

#17 0x55e2f1d5be16 in \_\_clear ./../../buildtools/third\_party/libc++/trunk/include/vector:832:29  

#18 0x55e2f1d5be16 in operator() ./../../buildtools/third\_party/libc++/trunk/include/vector:448:20  

#19 0x55e2f1d5be16 in ~vector ./../../buildtools/third\_party/libc++/trunk/include/vector:458:67  

#20 0x55e2f1d5be16 in content::RenderFrameHostImpl::ResetChildren() ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:4392:1  

#21 0x55e2f19bdf18 in content::FrameTree::Shutdown() ./../../content/browser/renderer\_host/frame\_tree.cc:976:39  

#22 0x55e2f2553712 in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1140:23  

#23 0x55e2f2556fcd in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web\_contents/web\_contents\_impl.cc:1073:37  

#24 0x55e2f452d46c in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#25 0x55e2f452d46c in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#26 0x55e2f452d46c in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#27 0x55e2f452d46c in ~AppWindowContentsImpl ./../../extensions/browser/app\_window/app\_window\_contents.cc:29:47  

#28 0x55e2f452d46c in extensions::AppWindowContentsImpl::~AppWindowContentsImpl() ./../../extensions/browser/app\_window/app\_window\_contents.cc:29:47  

#29 0x55e2f452455b in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#30 0x55e2f452455b in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#31 0x55e2f452455b in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#32 0x55e2f452455b in extensions::AppWindow::~AppWindow() ./../../extensions/browser/app\_window/app\_window.cc:336:1  

#33 0x55e2f452480d in extensions::AppWindow::~AppWindow() ./../../extensions/browser/app\_window/app\_window.cc:334:25  

#34 0x55e2f4526736 in extensions::AppWindow::OnNativeClose() ./../../extensions/browser/app\_window/app\_window.cc:498:3  

#35 0x55e310d96e26 in operator() ./../../extensions/components/native\_app\_window/native\_app\_window\_views.cc:53:30  

#36 0x55e310d96e26 in Invoke<(lambda at ../../extensions/components/native\_app\_window/native\_app\_window\_views.cc:51:7), native\_app\_window::NativeAppWindowViews \*> ./../../base/functional/bind\_internal.h:621:12  

#37 0x55e310d96e26 in MakeItSo<(lambda at ../../extensions/components/native\_app\_window/native\_app\_window\_views.cc:51:7), std::Cr::tuple<base::internal::UnretainedWrapper<native\_app\_window::NativeAppWindowViews, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> > > ./../../base/functional/bind\_internal.h:925:12  

#38 0x55e310d96e26 in RunImpl<(lambda at ../../extensions/components/native\_app\_window/native\_app\_window\_views.cc:51:7), std::Cr::tuple<base::internal::UnretainedWrapper<native\_app\_window::NativeAppWindowViews, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#39 0x55e310d96e26 in base::internal::Invoker<base::internal::BindState<native\_app\_window::NativeAppWindowViews::Init(extensions::AppWindow\*, extensions::AppWindow::CreateParams const&)::$\_0, base::internal::UnretainedWrapper<native\_app\_window::NativeAppWindowViews, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#40 0x55e304a88712 in Run ./../../base/functional/callback.h:152:12  

#41 0x55e304a88712 in views::WidgetDelegate::DeleteDelegate() ./../../ui/views/widget/widget\_delegate.cc:233:25  

#42 0x55e304a6e311 in views::Widget::OnNativeWidgetDestroyed() ./../../ui/views/widget/widget.cc:1600:25  

#43 0x55e304b379c9 in views::DesktopNativeWidgetAura::OnHostClosed() ./../../ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc:391:30  

#44 0x55e304b25d1b in views::DesktopWindowTreeHostPlatform::OnClosed() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:847:32  

#45 0x55e304b1e3fc in views::DesktopWindowTreeHostPlatform::CloseNow() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:406:22  

#46 0x55e304b2a023 in Invoke<void (views::DesktopWindowTreeHostPlatform::\*)(), const base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) &> ./../../base/functional/bind\_internal.h:746:12  

#47 0x55e304b2a023 in MakeItSo<void (views::DesktopWindowTreeHostPlatform::\*)(), std::Cr::tuple<base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) > > ./../../base/functional/bind\_internal.h:953:5  

#48 0x55e304b2a023 in RunImpl<void (views::DesktopWindowTreeHostPlatform::\*)(), std::Cr::tuple<base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);) >, 0UL> ./../../base/functional/bind\_internal.h:1025:12  

#49 0x55e304b2a023 in base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostPlatform::\*)(), base::WeakPtr[views::DesktopWindowTreeHostPlatform](javascript:void(0);)>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#50 0x55e2f94d91b7 in Run ./../../base/functional/callback.h:152:12  

#51 0x55e2f94d91b7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#52 0x55e2f95459f5 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#53 0x55e2f95459f5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#54 0x55e2f9544915 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#55 0x55e2f9546a34 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#56 0x55e2f96c2cf4 in base::MessagePumpGlib::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_glib.cc:670:48  

#57 0x55e2f9547769 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:651:12  

#58 0x55e2f9456855 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:134:14  

#59 0x55e2f09a3293 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1067:18

previously allocated by thread T0 (chrome) here:  

#0 0x55e2e77c092d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55e2f46b1133 in extensions::WebViewGuest::Create(content::WebContents\*) ./../../extensions/browser/guest\_view/web\_view/web\_view\_guest.cc:272:27  

#2 0x55e2f468c163 in Invoke<std::Cr::unique\_ptr<guest\_view::GuestViewBase, std::Cr::default\_delete<guest\_view::GuestViewBase> > (\*const &)(content::WebContents \*), content::WebContents \*> ./../../base/functional/bind\_internal.h:636:12  

#3 0x55e2f468c163 in MakeItSo<std::Cr::unique\_ptr<guest\_view::GuestViewBase, std::Cr::default\_delete<guest\_view::GuestViewBase> > (\*const &)(content::WebContents \*), const std::Cr::tuple<> &, content::WebContents \*> ./../../base/functional/bind\_internal.h:925:12  

#4 0x55e2f468c163 in RunImpl<std::Cr::unique\_ptr<guest\_view::GuestViewBase, std::Cr::default\_delete<guest\_view::GuestViewBase> > (\*const &)(content::WebContents \*), const std::Cr::tuple<> &> ./../../base/functional/bind\_internal.h:1025:12  

#5 0x55e2f468c163 in base::internal::Invoker<base::internal::BindState<std::Cr::unique\_ptr<guest\_view::GuestViewBase, std::Cr::default\_delete<guest\_view::GuestViewBase>> (\*)(content::WebContents\*)>, std::Cr::unique\_ptr<guest\_view::GuestViewBase, std::Cr::default\_delete<guest\_view::GuestViewBase>> (content::WebContents\*)>::Run(base::internal::BindStateBase\*, content::WebContents\*) ./../../base/functional/bind\_internal.h:989:12  

#6 0x55e303285509 in Run ./../../base/functional/callback.h:333:12  

#7 0x55e303285509 in guest\_view::GuestViewManager::CreateGuestInternal(content::WebContents\*, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&) ./../../components/guest\_view/browser/guest\_view\_manager.cc:436:37  

#8 0x55e303286397 in guest\_view::GuestViewManager::CreateGuestWithWebContentsParams(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, content::WebContents\*, content::WebContents::CreateParams const&) ./../../components/guest\_view/browser/guest\_view\_manager.cc:221:7  

#9 0x55e303276df3 in guest\_view::GuestViewBase::CreateNewGuestWindow(content::WebContents::CreateParams const&) ./../../components/guest\_view/browser/guest\_view\_base.cc:387:33  

#10 0x55e2f2591cd0 in content::WebContentsImpl::CreateNewWindow(content::RenderFrameHostImpl\*, content::mojom::CreateNewWindowParams const&, bool, bool, content::SessionStorageNamespace\*) ./../../content/browser/web\_contents/web\_contents\_impl.cc:4156:36  

#11 0x55e2f1db059d in content::RenderFrameHostImpl::CreateNewWindow(mojo::StructPtr[content::mojom::CreateNewWindowParams](javascript:void(0);), base::OnceCallback<void (content::mojom::CreateNewWindowStatus, mojo::StructPtr[content::mojom::CreateNewWindowReply](javascript:void(0);))>) ./../../content/browser/renderer\_host/render\_frame\_host\_impl.cc:7851:18  

#12 0x55e2ecc219ef in content::mojom::FrameHostStubDispatch::AcceptWithResponder(content::mojom::FrameHost\*, mojo::Message\*, std::Cr::unique\_ptr<mojo::MessageReceiverWithStatus, std::Cr::default\_delete[mojo::MessageReceiverWithStatus](javascript:void(0);)>) ./gen/content/common/frame.mojom.cc:5668:13  

#13 0x55e2fbe5e888 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:970:56  

#14 0x55e2fbe7c41c in mojo::MessageDispatcher::Accept(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/message\_dispatcher.cc:48:24  

#15 0x55e2fbe642e8 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:701:20  

#16 0x55e2fc34e76c in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptSyncMessage(unsigned int, unsigned int) ./../../ipc/ipc\_mojo\_bootstrap.cc:1109:24  

#17 0x55e2fc34f82f in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(unsigned int, unsigned int), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, unsigned int, unsigned int> ./../../base/functional/bind\_internal.h:746:12  

#18 0x55e2fc34f82f in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(unsigned int, unsigned int), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, unsigned int, unsigned int> > ./../../base/functional/bind\_internal.h:925:12  

#19 0x55e2fc34f82f in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(unsigned int, unsigned int), std::Cr::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, unsigned int, unsigned int>, 0UL, 1UL, 2UL> ./../../base/functional/bind\_internal.h:1025:12  

#20 0x55e2fc34f82f in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(unsigned int, unsigned int), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, unsigned int, unsigned int>, void ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:976:12  

#21 0x55e2f94d91b7 in Run ./../../base/functional/callback.h:152:12  

#22 0x55e2f94d91b7 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:186:34  

#23 0x55e2f95459f5 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:488:11)> ./../../base/task/common/task\_annotator.h:89:5  

#24 0x55e2f95459f5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:23  

#25 0x55e2f9544915 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:351:41  

#26 0x55e2f9546a34 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#27 0x55e2f96c235a in base::MessagePumpGlib::HandleDispatch() ./../../base/message\_loop/message\_pump\_glib.cc:625:46  

#28 0x55e2f96c5212 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) ./../../base/message\_loop/message\_pump\_glib.cc:274:43  

#29 0x7fbf94b6717c in g\_main\_context\_dispatch ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/build/chrome+0x1f32369e) (BuildId: 9276cee4a560fa04)  

Shadow bytes around the buggy address:  

0x6190004b5d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x6190004b5d80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x6190004b5e00: fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x6190004b5e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x6190004b5f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa  

=>0x6190004b5f80:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x6190004b6000: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x6190004b6080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x6190004b6100: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x6190004b6180: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x6190004b6200: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb

==2815759==ADDITIONAL INFO

==2815759==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x55e304b1dba5 in views::DesktopWindowTreeHostPlatform::Close() ./../../ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_platform.cc:368:7  

#1 0x55e2fc3407dd in IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept(mojo::Message\*) ./../../ipc/ipc\_mojo\_bootstrap.cc:1011:13  

#2 0x55e2fbeefa1e in mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int) ./../../mojo/public/cpp/system/simple\_watcher.cc:102:13

MiraclePtr Status: PROTECTED  

This crash occurred while a raw\_ptr<T> object containing a dangling pointer was being dereferenced.  

MiraclePtr is expected to make this crash non-exploitable once fully enabled.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==2815759==END OF ADDITIONAL INFO  

==2815759==ABORTING

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 345 B)
- [background.js](attachments/background.js) (text/plain, 165 B)
- [index.html](attachments/index.html) (text/plain, 111 B)
- [poc.html](attachments/poc.html) (text/plain, 3.8 KB)

## Timeline

### [Deleted User] (2023-05-04)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-05-05)

+guest_view folks, do you mind taking a look? A browser process UaF is usually critical severity, but needing an extension to be installed drops this down to High severity I think.

[Monorail components: Platform>Extensions]

### [Deleted User] (2023-05-05)

[Empty comment from Monorail migration]

### mc...@chromium.org (2023-05-05)

Not sure if it affects the severity, but this also appears to require tracing to be enabled.

It looks like WebViewGuest is being destroyed and then we try to access it as BrowserPluginGuest::delegate_ which is dangling.

[Monorail components: Platform>Apps>BrowserTag]

### [Deleted User] (2023-05-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2023-05-08)

In this case, we have a webview create a popup window and between the time of the renderer creating and showing the new window, the new guest web contents is owned by the opener web contents directly (WebContentsImpl::pending_contents_), not by WebViewGuest. If we destroy the opener webview at this time, the new webview is also destroyed, but the order of deletion is such that the new guest contents outlives its WebViewGuest and then while being deleted, it tries to access the WebViewGuest through the delegate.

### mc...@chromium.org (2023-05-08)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/4515455

### gi...@appspot.gserviceaccount.com (2023-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/db32d6929cf3177b52b034541e5bd6d3e19e18ca

commit db32d6929cf3177b52b034541e5bd6d3e19e18ca
Author: Kevin McNee <mcnee@chromium.org>
Date: Tue May 09 20:42:32 2023

Store BrowserPluginGuestDelegate as a weak ptr

In the case where a webview creates a popup window, the opener web
contents temporarily owns the new guest web contents between the
renderer creating and showing the window. If the opener is destroyed at
this time, the new guest (WebViewGuest) is destroyed as well. Due to
the ordering of the destruction of the new guest web contents, it may
attempt to access the destroyed WebViewGuest through the delegate
interface. We now access this delegate through a weak ptr.

Low-Coverage-Reason: NOTREACHED
Bug: 1442516
Change-Id: I417431ad487bc9db0551c1e0363379c5ff455d59
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4515455
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1141602}

[modify] https://crrev.com/db32d6929cf3177b52b034541e5bd6d3e19e18ca/content/browser/browser_plugin/browser_plugin_guest.cc
[modify] https://crrev.com/db32d6929cf3177b52b034541e5bd6d3e19e18ca/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/db32d6929cf3177b52b034541e5bd6d3e19e18ca/content/browser/browser_plugin/browser_plugin_guest.h
[modify] https://crrev.com/db32d6929cf3177b52b034541e5bd6d3e19e18ca/content/public/browser/browser_plugin_guest_delegate.cc
[modify] https://crrev.com/db32d6929cf3177b52b034541e5bd6d3e19e18ca/components/guest_view/browser/guest_view_base.cc
[modify] https://crrev.com/db32d6929cf3177b52b034541e5bd6d3e19e18ca/content/public/browser/browser_plugin_guest_delegate.h
[modify] https://crrev.com/db32d6929cf3177b52b034541e5bd6d3e19e18ca/components/guest_view/browser/guest_view_base.h


### mc...@chromium.org (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

Requesting merge to extended stable M112 because latest trunk commit (1141602) appears to be after extended stable branch point (1109224).

Requesting merge to stable M113 because latest trunk commit (1141602) appears to be after stable branch point (1121455).

Requesting merge to beta M114 because latest trunk commit (1141602) appears to be after beta branch point (1135570).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2023-05-10)

1. https://chromium-review.googlesource.com/c/chromium/src/+/4515455
2. I've manually tested on ToT.
3. No stability concerns. The fix is simply switching to the use of a weak ptr. No crash reports for the associated canary release appear related.
4. No.
5. No. There is automated test coverage introduced by the CL.

### [Deleted User] (2023-05-10)

Merge review required: M114 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-10)

Merge review required: M113 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-10)

Merge review required: M112 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2023-05-10)

See https://crbug.com/chromium/1442516#c13 for responses.

### am...@chromium.org (2023-05-12)

Thanks for the fix and responses to the merge questionnaire, Kevin. 
M114 /113 / 112 merges approved 

Please merge to M114 / branch 5735
Please merge to M113 / branch 5672 and M112 / branch 5615 by 10am Monday, 15 May so this fix can be in the next M113/Stable and M112/Extended security respins. Thank you!

### mc...@chromium.org (2023-05-12)

M114: https://chromium-review.googlesource.com/c/chromium/src/+/4528155
M113: https://chromium-review.googlesource.com/c/chromium/src/+/4527298
M112: https://chromium-review.googlesource.com/c/chromium/src/+/4527301

### gi...@appspot.gserviceaccount.com (2023-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9b6ca211234b057a9ce4184a3315741dc040ecbf

commit 9b6ca211234b057a9ce4184a3315741dc040ecbf
Author: Kevin McNee <mcnee@chromium.org>
Date: Fri May 12 19:53:19 2023

M114: Store BrowserPluginGuestDelegate as a weak ptr

Store BrowserPluginGuestDelegate as a weak ptr

In the case where a webview creates a popup window, the opener web
contents temporarily owns the new guest web contents between the
renderer creating and showing the window. If the opener is destroyed at
this time, the new guest (WebViewGuest) is destroyed as well. Due to
the ordering of the destruction of the new guest web contents, it may
attempt to access the destroyed WebViewGuest through the delegate
interface. We now access this delegate through a weak ptr.

(cherry picked from commit db32d6929cf3177b52b034541e5bd6d3e19e18ca)

Low-Coverage-Reason: NOTREACHED
Bug: 1442516
Change-Id: I417431ad487bc9db0551c1e0363379c5ff455d59
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4515455
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1141602}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4528155
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#540}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/9b6ca211234b057a9ce4184a3315741dc040ecbf/content/browser/browser_plugin/browser_plugin_guest.cc
[modify] https://crrev.com/9b6ca211234b057a9ce4184a3315741dc040ecbf/content/browser/browser_plugin/browser_plugin_guest.h
[modify] https://crrev.com/9b6ca211234b057a9ce4184a3315741dc040ecbf/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/9b6ca211234b057a9ce4184a3315741dc040ecbf/content/public/browser/browser_plugin_guest_delegate.cc
[modify] https://crrev.com/9b6ca211234b057a9ce4184a3315741dc040ecbf/components/guest_view/browser/guest_view_base.cc
[modify] https://crrev.com/9b6ca211234b057a9ce4184a3315741dc040ecbf/content/public/browser/browser_plugin_guest_delegate.h
[modify] https://crrev.com/9b6ca211234b057a9ce4184a3315741dc040ecbf/components/guest_view/browser/guest_view_base.h


### gi...@appspot.gserviceaccount.com (2023-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/49d3308d2fdeb276f92e118b7eb7007b676e0fa1

commit 49d3308d2fdeb276f92e118b7eb7007b676e0fa1
Author: Kevin McNee <mcnee@chromium.org>
Date: Fri May 12 20:03:34 2023

M112: Store BrowserPluginGuestDelegate as a weak ptr

Store BrowserPluginGuestDelegate as a weak ptr

In the case where a webview creates a popup window, the opener web
contents temporarily owns the new guest web contents between the
renderer creating and showing the window. If the opener is destroyed at
this time, the new guest (WebViewGuest) is destroyed as well. Due to
the ordering of the destruction of the new guest web contents, it may
attempt to access the destroyed WebViewGuest through the delegate
interface. We now access this delegate through a weak ptr.

(cherry picked from commit db32d6929cf3177b52b034541e5bd6d3e19e18ca)

Low-Coverage-Reason: NOTREACHED
Bug: 1442516
Change-Id: I417431ad487bc9db0551c1e0363379c5ff455d59
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4515455
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1141602}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4527301
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#1419}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/49d3308d2fdeb276f92e118b7eb7007b676e0fa1/content/browser/browser_plugin/browser_plugin_guest.cc
[modify] https://crrev.com/49d3308d2fdeb276f92e118b7eb7007b676e0fa1/content/browser/browser_plugin/browser_plugin_guest.h
[modify] https://crrev.com/49d3308d2fdeb276f92e118b7eb7007b676e0fa1/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/49d3308d2fdeb276f92e118b7eb7007b676e0fa1/content/public/browser/browser_plugin_guest_delegate.cc
[modify] https://crrev.com/49d3308d2fdeb276f92e118b7eb7007b676e0fa1/components/guest_view/browser/guest_view_base.cc
[modify] https://crrev.com/49d3308d2fdeb276f92e118b7eb7007b676e0fa1/content/public/browser/browser_plugin_guest_delegate.h
[modify] https://crrev.com/49d3308d2fdeb276f92e118b7eb7007b676e0fa1/components/guest_view/browser/guest_view_base.h


### gi...@appspot.gserviceaccount.com (2023-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e8b6b816e06cf4a2f5f3714bb155106c28825ade

commit e8b6b816e06cf4a2f5f3714bb155106c28825ade
Author: Kevin McNee <mcnee@chromium.org>
Date: Fri May 12 20:45:27 2023

M113: Store BrowserPluginGuestDelegate as a weak ptr

Store BrowserPluginGuestDelegate as a weak ptr

In the case where a webview creates a popup window, the opener web
contents temporarily owns the new guest web contents between the
renderer creating and showing the window. If the opener is destroyed at
this time, the new guest (WebViewGuest) is destroyed as well. Due to
the ordering of the destruction of the new guest web contents, it may
attempt to access the destroyed WebViewGuest through the delegate
interface. We now access this delegate through a weak ptr.

(cherry picked from commit db32d6929cf3177b52b034541e5bd6d3e19e18ca)

Low-Coverage-Reason: NOTREACHED
Bug: 1442516
Change-Id: I417431ad487bc9db0551c1e0363379c5ff455d59
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4515455
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1141602}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4527298
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Commit-Queue: Alex Moshchuk <alexmos@chromium.org>
Cr-Commit-Position: refs/branch-heads/5672@{#1174}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/e8b6b816e06cf4a2f5f3714bb155106c28825ade/content/browser/browser_plugin/browser_plugin_guest.cc
[modify] https://crrev.com/e8b6b816e06cf4a2f5f3714bb155106c28825ade/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/e8b6b816e06cf4a2f5f3714bb155106c28825ade/content/browser/browser_plugin/browser_plugin_guest.h
[modify] https://crrev.com/e8b6b816e06cf4a2f5f3714bb155106c28825ade/content/public/browser/browser_plugin_guest_delegate.cc
[modify] https://crrev.com/e8b6b816e06cf4a2f5f3714bb155106c28825ade/components/guest_view/browser/guest_view_base.cc
[modify] https://crrev.com/e8b6b816e06cf4a2f5f3714bb155106c28825ade/content/public/browser/browser_plugin_guest_delegate.h
[modify] https://crrev.com/e8b6b816e06cf4a2f5f3714bb155106c28825ade/components/guest_view/browser/guest_view_base.h


### am...@chromium.org (2023-05-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-18)

Congratulations, asnine! The VRP Panel has decided to award you $10,000 for this report of a mildly mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### gm...@google.com (2023-05-25)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-26)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-30)

1. Just https://crrev.com/c/4567345
2. Low, just had a few simple conflicts with type declarations and functions around the changed code that aren't present in 108
3. 112, 113 114
4. Yes

### gm...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-31)

Not needed in 108, see the comments on https://crrev.com/c/4567345

### [Deleted User] (2023-08-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1442516?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Apps>BrowserTag, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064365)*
