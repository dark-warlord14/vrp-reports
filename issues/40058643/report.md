# Security: heap-use-after-free on third_party/abseil-cpp/absl/types/internal/optional.h:208:13 in optional_data (chromeOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40058643](https://issues.chromium.org/issues/40058643) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API, UI>Browser>TopChrome>TabStrip |
| **Platforms** | Mac, Windows, ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2022-01-31 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36

Steps to reproduce the problem:
I will post screencast and details on next comment

What is the expected behavior?
not crash

What went wrong?
=================================================================
==24684==ERROR: AddressSanitizer: heap-use-after-free on address 0x6180001d4b20 at pc 0x563cdf843839 bp 0x7ffe66ae5470 sp 0x7ffe66ae5468
READ of size 1 at 0x6180001d4b20 thread T0 (chrome)
    #0 0x563cdf843838 in optional_data third_party/abseil-cpp/absl/types/internal/optional.h:208:13
    #1 0x563cdf843838 in optional third_party/abseil-cpp/absl/types/optional.h:139:3
    #2 0x563cdf843838 in group chrome/browser/ui/views/tabs/tab_slot_view.h:38:65
    #3 0x563cdf843838 in TabStripLayoutHelper::SlotIsCollapsedTab(int) const chrome/browser/ui/views/tabs/tab_strip_layout_helper.cc:443:69
    #4 0x563cdf840e52 in TabStripLayoutHelper::CalculateIdealBounds(absl::optional<int>) chrome/browser/ui/views/tabs/tab_strip_layout_helper.cc:299:54
    #5 0x563cdf842aca in TabStripLayoutHelper::CalculateMinimumWidth() chrome/browser/ui/views/tabs/tab_strip_layout_helper.cc:230:41
    #6 0x563cdf7fdae8 in TabStrip::GetMinimumSize() const chrome/browser/ui/views/tabs/tab_strip.cc:2169:45
    #7 0x563cd86562af in get ui/views/layout/flex_layout_types.cc:62:15
    #8 0x563cd86562af in operator-> ui/views/layout/flex_layout_types.cc:58:48
    #9 0x563cd86562af in views::(anonymous namespace)::GetPreferredSize(views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool, views::View const*, views::SizeBounds const&) ui/views/layout/flex_layout_types.cc:202:51
    #10 0x563cd865767c in Invoke<gfx::Size (*const &)(views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool, const views::View *, const views::SizeBounds &), const views::MinimumFlexSizeRule &, const views::MaximumFlexSizeRule &, const views::MinimumFlexSizeRule &, const views::MaximumFlexSizeRule &, const bool &, const views::View *, const views::SizeBounds &> base/bind_internal.h:437:12
    #11 0x563cd865767c in MakeItSo<gfx::Size (*const &)(views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool, const views::View *, const views::SizeBounds &), const views::MinimumFlexSizeRule &, const views::MaximumFlexSizeRule &, const views::MinimumFlexSizeRule &, const views::MaximumFlexSizeRule &, const bool &, const views::View *, const views::SizeBounds &> base/bind_internal.h:706:12
    #12 0x563cd865767c in RunImpl<gfx::Size (*const &)(views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool, const views::View *, const views::SizeBounds &), const std::__1::tuple<views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool> &, 0UL, 1UL, 2UL, 3UL, 4UL> base/bind_internal.h:779:12
    #13 0x563cd865767c in base::internal::Invoker<base::internal::BindState<gfx::Size (*)(views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool, views::View const*, views::SizeBounds const&), views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool>, gfx::Size (views::View const*, views::SizeBounds const&)>::Run(base::internal::BindStateBase*, views::View const*, views::SizeBounds const&) base/bind_internal.h:761:12
    #14 0x563cd864cdd7 in Run base/callback.h:241:12
    #15 0x563cd864cdd7 in views::FlexLayout::GetPreferredSizeForRule(base::RepeatingCallback<gfx::Size (views::View const*, views::SizeBounds const&)> const&, views::View const*, views::SizeBound const&) const ui/views/layout/flex_layout.cc:483:12
    #16 0x563cd8648f1d in views::FlexLayout::InitializeChildData(views::NormalizedSizeBounds const&, views::FlexLayout::FlexLayoutData&, std::__1::map<int, std::__1::list<unsigned long, std::__1::allocator<unsigned long> >, std::__1::less<int>, std::__1::allocator<std::__1::pair<int const, std::__1::list<unsigned long, std::__1::allocator<unsigned long> > > > >&) const ui/views/layout/flex_layout.cc:548:9
    #17 0x563cd8647aef in views::FlexLayout::CalculateProposedLayout(views::SizeBounds const&) const ui/views/layout/flex_layout.cc:421:3
    #18 0x563cd866972e in views::LayoutManagerBase::GetProposedLayout(gfx::Size const&) const ui/views/layout/layout_manager_base.cc:104:22
    #19 0x563cd8668e82 in views::LayoutManagerBase::GetAvailableSize(views::View const*, views::View const*) const ui/views/layout/layout_manager_base.cc:68:5
    #20 0x563cd8695474 in views::View::GetAvailableSize(views::View const*) const ui/views/view.cc:563:32
    #21 0x563cdf7f10db in TabStrip::GetAvailableWidthForTabStrip() const chrome/browser/ui/views/tabs/tab_strip.cc:3182:26
    #22 0x563cdf7f23b4 in TabStrip::UpdateIdealBounds() chrome/browser/ui/views/tabs/tab_strip.cc:3168:27
    #23 0x563cdf7f32be in TabStrip::OnGroupVisualsChanged(tab_groups::TabGroupId const&, tab_groups::TabGroupVisualData const*, tab_groups::TabGroupVisualData const*) chrome/browser/ui/views/tabs/tab_strip.cc:1277:3
    #24 0x563cde9595fc in TabStripModel::ChangeTabGroupVisuals(tab_groups::TabGroupId const&, TabGroupChange::VisualsChange const&) chrome/browser/ui/tabs/tab_strip_model.cc:1229:14
    #25 0x563cde942469 in TabGroup::AddTab() chrome/browser/ui/tabs/tab_group.cc:68:18
    #26 0x563cde957284 in TabStripModel::GroupTab(int, tab_groups::TabGroupId const&) chrome/browser/ui/tabs/tab_strip_model.cc:2247:37
    #27 0x563cde947529 in TabStripModel::InsertWebContentsAtImpl(int, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, absl::optional<tab_groups::TabGroupId>) chrome/browser/ui/tabs/tab_strip_model.cc:1759:5
    #28 0x563cde946ba4 in TabStripModel::InsertWebContentsAt(int, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, absl::optional<tab_groups::TabGroupId>) chrome/browser/ui/tabs/tab_strip_model.cc:366:10
    #29 0x563cdd21c30d in extensions::TabGroupsMoveFunction::MoveGroup(int, int, int*, tab_groups::TabGroupId*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*) chrome/browser/extensions/api/tab_groups/tab_groups_api.cc:296:27
    #30 0x563cdd21ba8b in extensions::TabGroupsMoveFunction::Run() chrome/browser/extensions/api/tab_groups/tab_groups_api.cc:217:8
    #31 0x563ccb2f9638 in ExtensionFunction::RunWithValidation() extensions/browser/extension_function.cc:514:10
    #32 0x563ccb300002 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost*, int, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) extensions/browser/extension_function_dispatcher.cc:401:15
    #33 0x563ccb300d0c in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker(extensions::mojom::RequestParams const&, int) extensions/browser/extension_function_dispatcher.cc:293:3
    #34 0x563ccb34f501 in DispatchToMethodImpl<extensions::ExtensionServiceWorkerMessageFilter *, void (extensions::ExtensionServiceWorkerMessageFilter::*)(const extensions::mojom::RequestParams &), std::__1::tuple<extensions::mojom::RequestParams>, 0UL> base/tuple.h:52:3
    #35 0x563ccb34f501 in DispatchToMethod<extensions::ExtensionServiceWorkerMessageFilter *, void (extensions::ExtensionServiceWorkerMessageFilter::*)(const extensions::mojom::RequestParams &), std::__1::tuple<extensions::mojom::RequestParams> > base/tuple.h:60:3
    #36 0x563ccb34f501 in DispatchToMethod<extensions::ExtensionServiceWorkerMessageFilter, void (extensions::ExtensionServiceWorkerMessageFilter::*)(const extensions::mojom::RequestParams &), void, std::__1::tuple<extensions::mojom::RequestParams> > ipc/ipc_message_templates.h:53:3
    #37 0x563ccb34f501 in bool IPC::MessageT<ExtensionHostMsg_RequestWorker_Meta, std::__1::tuple<extensions::mojom::RequestParams>, void>::Dispatch<extensions::ExtensionServiceWorkerMessageFilter, extensions::ExtensionServiceWorkerMessageFilter, void, void (extensions::ExtensionServiceWorkerMessageFilter::*)(extensions::mojom::RequestParams const&)>(IPC::Message const*, extensions::ExtensionServiceWorkerMessageFilter*, extensions::ExtensionServiceWorkerMessageFilter*, void*, void (extensions::ExtensionServiceWorkerMessageFilter::*)(extensions::mojom::RequestParams const&)) ipc/ipc_message_templates.h:141:7
    #38 0x563ccb34f0d9 in extensions::ExtensionServiceWorkerMessageFilter::OnMessageReceived(IPC::Message const&) extensions/browser/extension_service_worker_message_filter.cc:108:5
    #39 0x563cd272ba66 in Run base/callback.h:142:12
    #40 0x563cd272ba66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #41 0x563cd276baa3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #42 0x563cd276baa3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #43 0x563cd276b2f2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #44 0x563cd276c661 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #45 0x563cd28a9fad in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #46 0x563cd276cd1a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #47 0x563cd26a655c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #48 0x563cc93e4ef2 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1053:18
    #49 0x563cc93e9475 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:155:15
    #50 0x563cc93df24a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #51 0x563cd2483c4f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:641:10
    #52 0x563cd2486753 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1165:10
    #53 0x563cd2485b2a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1031:12
    #54 0x563cd24803c4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:399:36
    #55 0x563cd2480a40 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:427:10
    #56 0x563cc4a25e0a in ChromeMain chrome/app/chrome_main.cc:176:12
    #57 0x563cc4a25bdf in main chrome/app/chrome_exe_main_aura.cc:17:10
    #58 0x7f6e5e8f50b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6180001d4b20 is located 672 bytes inside of 816-byte region [0x6180001d4880,0x6180001d4bb0)
freed by thread T0 (chrome) here:
    #0 0x563cc4a23e4d in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x563cdf8296d6 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x563cdf8296d6 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x563cdf8296d6 in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x563cdf8296d6 in TabGroupViews::~TabGroupViews() chrome/browser/ui/views/tabs/tab_group_views.cc:35:3
    #5 0x563cdf80aa16 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #6 0x563cdf80aa16 in std::__1::unique_ptr<TabGroupViews, std::__1::default_delete<TabGroupViews> >::reset(TabGroupViews*) buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #7 0x563cdf7f1c5d in operator= buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:234:5
    #8 0x563cdf7f1c5d in TabStrip::OnGroupCreated(tab_groups::TabGroupId const&) chrome/browser/ui/views/tabs/tab_strip.cc:1245:23
    #9 0x563cdf7aeecf in BrowserTabStripController::OnTabGroupChanged(TabGroupChange const&) chrome/browser/ui/views/tabs/browser_tab_strip_controller.cc:670:18
    #10 0x563cde9588d5 in TabStripModel::CreateTabGroup(tab_groups::TabGroupId const&) chrome/browser/ui/tabs/tab_strip_model.cc:1208:14
    #11 0x563cde9423e2 in TabGroup::AddTab() chrome/browser/ui/tabs/tab_group.cc:65:18
    #12 0x563cde957284 in TabStripModel::GroupTab(int, tab_groups::TabGroupId const&) chrome/browser/ui/tabs/tab_strip_model.cc:2247:37
    #13 0x563cde947529 in TabStripModel::InsertWebContentsAtImpl(int, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, absl::optional<tab_groups::TabGroupId>) chrome/browser/ui/tabs/tab_strip_model.cc:1759:5
    #14 0x563cde946ba4 in TabStripModel::InsertWebContentsAt(int, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, absl::optional<tab_groups::TabGroupId>) chrome/browser/ui/tabs/tab_strip_model.cc:366:10
    #15 0x563cdd21c30d in extensions::TabGroupsMoveFunction::MoveGroup(int, int, int*, tab_groups::TabGroupId*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >*) chrome/browser/extensions/api/tab_groups/tab_groups_api.cc:296:27
    #16 0x563cdd21ba8b in extensions::TabGroupsMoveFunction::Run() chrome/browser/extensions/api/tab_groups/tab_groups_api.cc:217:8
    #17 0x563ccb2f9638 in ExtensionFunction::RunWithValidation() extensions/browser/extension_function.cc:514:10
    #18 0x563ccb300002 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost*, int, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&)>) extensions/browser/extension_function_dispatcher.cc:401:15
    #19 0x563ccb300d0c in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker(extensions::mojom::RequestParams const&, int) extensions/browser/extension_function_dispatcher.cc:293:3
    #20 0x563ccb34f501 in DispatchToMethodImpl<extensions::ExtensionServiceWorkerMessageFilter *, void (extensions::ExtensionServiceWorkerMessageFilter::*)(const extensions::mojom::RequestParams &), std::__1::tuple<extensions::mojom::RequestParams>, 0UL> base/tuple.h:52:3
    #21 0x563ccb34f501 in DispatchToMethod<extensions::ExtensionServiceWorkerMessageFilter *, void (extensions::ExtensionServiceWorkerMessageFilter::*)(const extensions::mojom::RequestParams &), std::__1::tuple<extensions::mojom::RequestParams> > base/tuple.h:60:3
    #22 0x563ccb34f501 in DispatchToMethod<extensions::ExtensionServiceWorkerMessageFilter, void (extensions::ExtensionServiceWorkerMessageFilter::*)(const extensions::mojom::RequestParams &), void, std::__1::tuple<extensions::mojom::RequestParams> > ipc/ipc_message_templates.h:53:3
    #23 0x563ccb34f501 in bool IPC::MessageT<ExtensionHostMsg_RequestWorker_Meta, std::__1::tuple<extensions::mojom::RequestParams>, void>::Dispatch<extensions::ExtensionServiceWorkerMessageFilter, extensions::ExtensionServiceWorkerMessageFilter, void, void (extensions::ExtensionServiceWorkerMessageFilter::*)(extensions::mojom::RequestParams const&)>(IPC::Message const*, extensions::ExtensionServiceWorkerMessageFilter*, extensions::ExtensionServiceWorkerMessageFilter*, void*, void (extensions::ExtensionServiceWorkerMessageFilter::*)(extensions::mojom::RequestParams const&)) ipc/ipc_message_templates.h:141:7
    #24 0x563ccb34f0d9 in extensions::ExtensionServiceWorkerMessageFilter::OnMessageReceived(IPC::Message const&) extensions/browser/extension_service_worker_message_filter.cc:108:5
    #25 0x563cd272ba66 in Run base/callback.h:142:12
    #26 0x563cd272ba66 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task_annotator.cc:135:32
    #27 0x563cd276baa3 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:29)> base/task/common/task_annotator.h:74:5
    #28 0x563cd276baa3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:356:21
    #29 0x563cd276b2f2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #30 0x563cd276c661 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #31 0x563cd28a9fad in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:195:55
    #32 0x563cd276cd1a in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:468:12
    #33 0x563cd26a655c in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #34 0x563cc93e4ef2 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1053:18
    #35 0x563cc93e9475 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:155:15
    #36 0x563cc93df24a in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:30:28
    #37 0x563cd2483c4f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:641:10
    #38 0x563cd2486753 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1165:10
    #39 0x563cd2485b2a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1031:12

previously allocated by thread T0 (chrome) here:
    #0 0x563cc4a235ed in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x563cdf82941d in make_unique<TabGroupHeader, const base::raw_ptr<TabStrip, base::internal::RawPtrNoOpImpl> &, const tab_groups::TabGroupId &> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:28
    #2 0x563cdf82941d in TabGroupViews::TabGroupViews(TabStrip*, tab_groups::TabGroupId const&) chrome/browser/ui/views/tabs/tab_group_views.cc:27:7
    #3 0x563cdf7f1b8e in make_unique<TabGroupViews, TabStrip *, const tab_groups::TabGroupId &> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:32
    #4 0x563cdf7f1b8e in TabStrip::OnGroupCreated(tab_groups::TabGroupId const&) chrome/browser/ui/views/tabs/tab_strip.cc:1243:21
    #5 0x563cdf7aeecf in BrowserTabStripController::OnTabGroupChanged(TabGroupChange const&) chrome/browser/ui/views/tabs/browser_tab_strip_controller.cc:670:18
    #6 0x563cde9588d5 in TabStripModel::CreateTabGroup(tab_groups::TabGroupId const&) chrome/browser/ui/tabs/tab_strip_model.cc:1208:14
    #7 0x563cde9423e2 in TabGroup::AddTab() chrome/browser/ui/tabs/tab_group.cc:65:18
    #8 0x563cde957284 in TabStripModel::GroupTab(int, tab_groups::TabGroupId const&) chrome/browser/ui/tabs/tab_strip_model.cc:2247:37
    #9 0x563cde947529 in TabStripModel::InsertWebContentsAtImpl(int, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, absl::optional<tab_groups::TabGroupId>) chrome/browser/ui/tabs/tab_strip_model.cc:1759:5
    #10 0x563cde946ba4 in TabStripModel::InsertWebContentsAt(int, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, absl::optional<tab_groups::TabGroupId>) chrome/browser/ui/tabs/tab_strip_model.cc:366:10
    #11 0x563cdf7cf899 in TabDragController::Attach(TabDragContext*, gfx::Point const&, std::__1::unique_ptr<TabDragController, std::__1::default_delete<TabDragController> >, bool) chrome/browser/ui/views/tabs/tab_drag_controller.cc:1176:46
    #12 0x563cdf7d831c in DetachAndAttachToNewContext chrome/browser/ui/views/tabs/tab_drag_controller.cc:1059:3
    #13 0x563cdf7d831c in TabDragController::DetachIntoNewBrowserAndRunMoveLoop(gfx::Point const&) chrome/browser/ui/views/tabs/tab_drag_controller.cc:1339:3
    #14 0x563cdf7d672e in TabDragController::DragBrowserToNewTabStrip(TabDragContext*, gfx::Point const&) chrome/browser/ui/views/tabs/tab_drag_controller.cc:867:5
    #15 0x563cdf7d41de in TabDragController::ContinueDragging(gfx::Point const&) chrome/browser/ui/views/tabs/tab_drag_controller.cc:837:9
    #16 0x563cdf7ce951 in TabDragController::Drag(gfx::Point const&) chrome/browser/ui/views/tabs/tab_drag_controller.cc:601:7
    #17 0x563cdf7fa3e2 in TabStrip::TabDragContextImpl::ContinueDrag(views::View*, ui::LocatedEvent const&) chrome/browser/ui/views/tabs/tab_strip.cc:395:25
    #18 0x563cdf80302f in TabStrip::OnMouseDragged(ui::MouseEvent const&) chrome/browser/ui/views/tabs/tab_strip.cc:3259:3
    #19 0x563cd869f96a in views::View::ProcessMouseDragged(ui::MouseEvent*) ui/views/view.cc:3051:9
    #20 0x563cd48efe3b in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #21 0x563cd48ef400 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #22 0x563cd48eeed4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #23 0x563cd48eec40 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #24 0x563cd86bd767 in views::internal::RootView::OnMouseDragged(ui::MouseEvent const&) ui/views/widget/root_view.cc:463:9
    #25 0x563cd86d26bf in views::Widget::OnMouseEvent(ui::MouseEvent*) ui/views/widget/widget.cc:1555:22
    #26 0x563cd48efe3b in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:190:12
    #27 0x563cd48ef400 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:139:5
    #28 0x563cd48eeed4 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:83:14
    #29 0x563cd48eec40 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:55:15
    #30 0x563cd82a724f in ui::EventProcessor::OnEventFromSource(ui::Event*) ui/events/event_processor.cc:49:17
    #31 0x563cd48f33de in ui::EventSource::DeliverEventToSink(ui::Event*) ui/events/event_source.cc:118:16
    #32 0x563cd48f38d6 in ui::EventSource::EventRewriterContinuationImpl::SendEvent(ui::Event const*) ui/events/event_source.cc:66:14

SUMMARY: AddressSanitizer: heap-use-after-free third_party/abseil-cpp/absl/types/internal/optional.h:208:13 in optional_data
Shadow bytes around the buggy address:
  0x0c3080032910: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032920: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032930: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032940: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032950: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c3080032960: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd
  0x0c3080032970: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa
  0x0c3080032980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3080032990: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c30800329a0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c30800329b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
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
==24684==ABORTING

Did this work before? N/A 

Chrome version: 100.0.4861.0  Channel: dev
OS Version: linux-chromeOS

## Attachments

- [service_worker.js](attachments/service_worker.js) (text/plain, 2.0 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 243 B)
- [screencast_1292451.webm](attachments/screencast_1292451.webm) (video/webm, 4.7 MB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-01-31)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-01-31)

Similar to issue #1202102, I modified a few line codes from the source. This issue only reproduces on ChromeOS, and I've tested on another OS like Chrome in Linux it couldn't repro.

Poc:

(1) Install the extension.
(2) Drag the pinned tab.

I uploaded screen-cast for visibility.



### al...@google.com (2022-01-31)

[Empty comment from Monorail migration]

[Monorail components: UI>Shell]

### tb...@chromium.org (2022-01-31)

Adding it to our team's triage queue, and +dpenning. Looks like another extensions + drag UAF.

[Monorail components: UI>Browser>TopChrome>TabStrip]

### al...@google.com (2022-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-31)

[Empty comment from Monorail migration]

### al...@google.com (2022-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-01)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### co...@chromium.org (2022-02-04)

[Empty comment from Monorail migration]

[Monorail components: -UI>Shell]

### rh...@gmail.com (2022-02-12)

Hi Developer and Security,

I've tested Chrome Dev and Stable on Windows VM and it does repro. Do you mind to change the title or remove (chromeOS on the title?) and change the OS impact.

(1) Chromium	100.0.4884.0 (Developer Build) (64-bit)  Revision	cf517208a47818861c8b3d4fee1c5ec59588f743-refs/heads/main@{#970217}
(2) Version 98.0.4758.82 (Official Build) (64-bit)

==3532==ERROR: AddressSanitizer: heap-use-after-free on address 0x1279f31f0f28 at pc 0x7fffe45c6bcc bp 0x00573abfd720 sp 0x00573abfd768
READ of size 1 at 0x1279f31f0f28 thread T0
==3532==WARNING: Failed to use and restart external symbolizer!
    #0 0x7fffe45c6bcb in TabStripLayoutHelper::SlotIsCollapsedTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip_layout_helper.cc:443
    #1 0x7fffe45c3b6d in TabStripLayoutHelper::CalculateIdealBounds C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip_layout_helper.cc:299
    #2 0x7fffe45c5c08 in TabStripLayoutHelper::CalculateMinimumWidth C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip_layout_helper.cc:230
    #3 0x7fffe14c01b2 in TabStrip::GetMinimumSize C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:2181
    #4 0x7fffdccc1978 in views::`anonymous namespace'::GetPreferredSize C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex_layout_types.cc:202
    #5 0x7fffdccc3108 in base::internal::Invoker<base::internal::BindState<gfx::Size (*)(views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool, const views::View *, const views::SizeBounds &),views::MinimumFlexSizeRule,views::MaximumFlexSizeRule,views::MinimumFlexSizeRule,views::MaximumFlexSizeRule,bool>,gfx::Size (const views::View *, const views::SizeBounds &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:761
    #6 0x7fffdbf2ef17 in views::FlexLayout::GetPreferredSizeForRule C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex_layout.cc:483
    #7 0x7fffdbf2aa64 in views::FlexLayout::InitializeChildData C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex_layout.cc:548
    #8 0x7fffdbf29402 in views::FlexLayout::CalculateProposedLayout C:\b\s\w\ir\cache\builder\src\ui\views\layout\flex_layout.cc:421
    #9 0x7fffded8c68f in views::LayoutManagerBase::GetProposedLayout C:\b\s\w\ir\cache\builder\src\ui\views\layout\layout_manager_base.cc:104
    #10 0x7fffded8be0b in views::LayoutManagerBase::GetAvailableSize C:\b\s\w\ir\cache\builder\src\ui\views\layout\layout_manager_base.cc:68
    #11 0x7fffd70093ad in views::View::GetAvailableSize C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:563
    #12 0x7fffe14b22fe in TabStrip::GetAvailableWidthForTabStrip C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:3226
    #13 0x7fffe14b3c28 in TabStrip::UpdateIdealBounds C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:3212
    #14 0x7fffe14b4ea6 in TabStrip::OnGroupVisualsChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:1379
    #15 0x7fffe14a9729 in BrowserTabStripController::OnTabGroupChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:718
    #16 0x7fffd987674d in TabStripModel::ChangeTabGroupVisuals C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1298
    #17 0x7fffdbf162e6 in TabGroup::AddTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_group.cc:68
    #18 0x7fffd9873d6b in TabStripModel::GroupTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:2368
    #19 0x7fffd9860e8b in TabStripModel::InsertWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1851
    #20 0x7fffd9860336 in TabStripModel::InsertWebContentsAt C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:395
    #21 0x7fffe74bf20d in extensions::TabGroupsMoveFunction::MoveGroup C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\tab_groups\tab_groups_api.cc:317
    #22 0x7fffe74be6a9 in extensions::TabGroupsMoveFunction::Run C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\tab_groups\tab_groups_api.cc:224
    #23 0x7fffd2122f85 in ExtensionFunction::RunWithValidation C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function.cc:515
    #24 0x7fffd212a332 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:401
    #25 0x7fffd212b285 in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:293
    #26 0x7fffd2184b0e in IPC::MessageT<ExtensionHostMsg_RequestWorker_Meta,std::__1::tuple<extensions::mojom::RequestParams>,void>::Dispatch<extensions::ExtensionServiceWorkerMessageFilter,extensions::ExtensionServiceWorkerMessageFilter,void,void (extensions::ExtensionServiceWorkerMessageFilter::*)(const extensions::mojom::RequestParams &)> C:\b\s\w\ir\cache\builder\src\ipc\ipc_message_templates.h:141
    #27 0x7fffd218444b in extensions::ExtensionServiceWorkerMessageFilter::OnMessageReceived C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_service_worker_message_filter.cc:108
    #28 0x7fffd72f03b4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #29 0x7fffda087c25 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:387
    #30 0x7fffda0871f9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:292
    #31 0x7fffd739c2c6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #32 0x7fffd739a558 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #33 0x7fffda089351 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:499
    #34 0x7fffd726fb03 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #35 0x7fffd0268d8d in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1056
    #36 0x7fffd026e1eb in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:155
    #37 0x7fffd02623e5 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #38 0x7fffd2d6ad0b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:642
    #39 0x7fffd2d6df5e in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1175
    #40 0x7fffd2d6d09e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1042
    #41 0x7fffd2d69986 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:399
    #42 0x7fffd2d6a10a in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:427
    #43 0x7fffcc3914ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:176
    #44 0x7ff6187b5b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #45 0x7ff6187b2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #46 0x7ff618bb4e7f in __scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #47 0x7ff8206f8363 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180008363)
    #48 0x7ff821165e90 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180065e90)

0x1279f31f0f28 is located 680 bytes inside of 832-byte region [0x1279f31f0c80,0x1279f31f0fc0)
freed by thread T0 here:
    #0 0x7ff6188622cb in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7fffe45d72ff in TabGroupHeader::~TabGroupHeader C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_group_header.cc:127
    #2 0x7fffe45cfd7f in TabGroupViews::~TabGroupViews C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_group_views.cc:37
    #3 0x7fffe14cef95 in std::__1::unique_ptr<TabGroupViews,std::__1::default_delete<TabGroupViews> >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h:315
    #4 0x7fffe14b320e in TabStrip::OnGroupCreated C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:1347
    #5 0x7fffe14a9236 in BrowserTabStripController::OnTabGroupChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:680
    #6 0x7fffd98757dc in TabStripModel::CreateTabGroup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1268
    #7 0x7fffdbf1625d in TabGroup::AddTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_group.cc:65
    #8 0x7fffd9873d6b in TabStripModel::GroupTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:2368
    #9 0x7fffd9860e8b in TabStripModel::InsertWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1851
    #10 0x7fffd9860336 in TabStripModel::InsertWebContentsAt C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:395
    #11 0x7fffe74bf20d in extensions::TabGroupsMoveFunction::MoveGroup C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\tab_groups\tab_groups_api.cc:317
    #12 0x7fffe74be6a9 in extensions::TabGroupsMoveFunction::Run C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\tab_groups\tab_groups_api.cc:224
    #13 0x7fffd2122f85 in ExtensionFunction::RunWithValidation C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function.cc:515
    #14 0x7fffd212a332 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:401
    #15 0x7fffd212b285 in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_function_dispatcher.cc:293
    #16 0x7fffd2184b0e in IPC::MessageT<ExtensionHostMsg_RequestWorker_Meta,std::__1::tuple<extensions::mojom::RequestParams>,void>::Dispatch<extensions::ExtensionServiceWorkerMessageFilter,extensions::ExtensionServiceWorkerMessageFilter,void,void (extensions::ExtensionServiceWorkerMessageFilter::*)(const extensions::mojom::RequestParams &)> C:\b\s\w\ir\cache\builder\src\ipc\ipc_message_templates.h:141
    #17 0x7fffd218444b in extensions::ExtensionServiceWorkerMessageFilter::OnMessageReceived C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_service_worker_message_filter.cc:108
    #18 0x7fffd72f03b4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #19 0x7fffda087c25 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:387
    #20 0x7fffda0871f9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:292
    #21 0x7fffd739c2c6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
    #22 0x7fffd739a558 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #23 0x7fffda089351 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:499
    #24 0x7fffd726fb03 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #25 0x7fffd0268d8d in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1056
    #26 0x7fffd026e1eb in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:155
    #27 0x7fffd02623e5 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30

previously allocated by thread T0 here:
    #0 0x7ff6188623cb in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7fffe99bb47e in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7fffe45cfa17 in TabGroupViews::TabGroupViews C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_group_views.cc:28
    #3 0x7fffe14b30fc in TabStrip::OnGroupCreated C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:1345
    #4 0x7fffe14a9236 in BrowserTabStripController::OnTabGroupChanged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser_tab_strip_controller.cc:680
    #5 0x7fffd98757dc in TabStripModel::CreateTabGroup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1268
    #6 0x7fffdbf1625d in TabGroup::AddTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_group.cc:65
    #7 0x7fffd9873d6b in TabStripModel::GroupTab C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:2368
    #8 0x7fffd9860e8b in TabStripModel::InsertWebContentsAtImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:1851
    #9 0x7fffd9860336 in TabStripModel::InsertWebContentsAt C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab_strip_model.cc:395
    #10 0x7fffe45a1f6f in TabDragController::Attach C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_drag_controller.cc:1343
    #11 0x7fffe45a9936 in TabDragController::DetachAndAttachToNewContext C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_drag_controller.cc:1226
    #12 0x7fffe45aca8e in TabDragController::DetachIntoNewBrowserAndRunMoveLoop C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_drag_controller.cc:1506
    #13 0x7fffe45abba9 in TabDragController::DragBrowserToNewTabStrip C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_drag_controller.cc:979
    #14 0x7fffe45a7b38 in TabDragController::ContinueDragging C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_drag_controller.cc:949
    #15 0x7fffe45a0b3f in TabDragController::Drag C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_drag_controller.cc:674
    #16 0x7fffe14bd00b in TabStrip::TabDragContextImpl::ContinueDrag C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:485
    #17 0x7fffe14c6846 in TabStrip::OnMouseDragged C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip.cc:3303
    #18 0x7fffd701576b in views::View::ProcessMouseDragged C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3051
    #19 0x7fffd7fccaed in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:190
    #20 0x7fffd7fcc00d in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:139
    #21 0x7fffd7fcb8f7 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:83
    #22 0x7fffd7fcb538 in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:55
    #23 0x7fffd9cbd86f in views::internal::RootView::OnMouseDragged C:\b\s\w\ir\cache\builder\src\ui\views\widget\root_view.cc:463
    #24 0x7fffd703d6bb in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1559
    #25 0x7fffd7fccaed in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:190
    #26 0x7fffd7fcc00d in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:139
    #27 0x7fffd7fcb8f7 in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event_dispatcher.cc:83

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab_strip_layout_helper.cc:443 in TabStripLayoutHelper::SlotIsCollapsedTab
Shadow bytes around the buggy address:
  0x04993153e190: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04993153e1a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04993153e1b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04993153e1c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04993153e1d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x04993153e1e0: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x04993153e1f0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x04993153e200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x04993153e210: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04993153e220: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04993153e230: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==3532==ABORTING

### [Deleted User] (2022-02-14)

dpenning: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@gmail.com (2022-02-17)

Hello,

any update on this?

### rh...@gmail.com (2022-02-18)

mac stable: crash/653443c8-71ff-48c6-879e-3246c0713dda

### [Deleted User] (2022-02-28)

dpenning: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-04-04)

Hi any update on this issue?

### rh...@gmail.com (2022-04-25)

Hi,

Would it be possible to get an update?

Thank you in advance

### dp...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### dp...@google.com (2022-04-25)

passing to tbergquist@ to see if we can make some progress.

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-06-08)

Friendly ping, Can you update on the status of this bug? 

### rh...@gmail.com (2022-06-20)

Friendly ping! Would it be possible to get an update?


### rh...@gmail.com (2022-06-30)

Hi,

Would it be possible to get an update? Since this issue was also effected on windows https://crbug.com/chromium/1292451#c12 and mac https://crbug.com/chromium/1292451#c15. 


### tb...@chromium.org (2022-06-30)

[Empty comment from Monorail migration]

### tb...@chromium.org (2022-07-01)

Just linearizing the extension here, since I find the callback-oriented stuff quite hard to read:
1. Create a window W with tabs A, B, and C, where A and B are in a group and all tabs have actual URLs (so restore picks them up).
2. Close tab A. Now it's in session restore history, yay.
3. Wait for user to begin a header drag, dragging tab B by its group header out of window W, creating a new window Q containing just tab B in its group.
4. Restore tab A (in immediate response to tab B being inserted into window Q). I believe this is inserted back into window W - I'll go into why below.
5. Move the tab group into the window W (I think) containing the newly restored tab.
6. Boom, UAF is happen trying to move a group into a window where it already exists.

So the key thing that seems to be going wrong to me, at first glance, is that the restore happens in response to the tab being inserted, and tab insertion and grouping are *not* atomic actions (i.e. it does the insertion, notifies about it, does the grouping, then notifies about that), so instead of being restored into the window Q containing the rest of the group, it's inserted into the original window W.

The extensions-can't-do-stuff-during-drag prohibition doesn't apply to step 5 because step 4 also cancels the drag session. Session restore itself isn't subject to that prohibition, IIRC, so step 4 isn't blocked, either.

Possible solutions:
1. CHECK when creating a group that already exists in that window.
2. CHECK when creating a group that already exists in *any* window.
3. Subject session restore to the extensions-can't-do-stuff-during-drag prohibition, so step 4 is blocked until the drag ends.
4. Make tab insertion and grouping atomic, i.e. bundle those notifications together. This one is a big can of worms, but I think dpenning@ is thinking about it.

Solution 4 seems like the ideal one in many ways, but it's a big project. I'm thinking that combining solutions 2 and 3 would be the way to go right now - 2 turns a class of security issues (tab groups split across windows) into crashes, and 3 fixes one particular way of invoking that class of issues.

### tb...@chromium.org (2022-07-01)

Okay, I think I might have gotten some details mixed up in exactly what state the two windows W and Q are in when the restore and the group move go through. This is really complicated - will have to go through more carefully, probably actually run the repro, some other time.

The TL;DR is still valid, though - the extension is able to interrupt the tabstrip while it's in the middle of some compound operation which assumes it won't be interrupted, so we get into a state that should be impossible to reach, and code that assumes that state is impossible becomes vulnerable to UAFs. The tricky bit is that this repro may be doing things to tabstrip in window W while tabstrip in window Q is in the middle of an operation (or vice versa).

While I'm here, solution option number 5: Make the reentrancy checks in TabStripModel CHECK instead of DCHECK. This solution might not actually cover this repro, if the issue does in fact lie with doing a restore while a tab group briefly doesn't actually exist, but could help prevent other related issues.

### tb...@chromium.org (2022-07-06)

[Empty comment from Monorail migration]

### tb...@chromium.org (2022-07-06)

I suspect https://chromium-review.googlesource.com/c/chromium/src/+/3404696 will apply to this case. Indeed, I can't repro locally on my Mac - that CL might be related.

I put up two CLs related to this anyways, to make sure we're covering the whole space of possible issues.

### gi...@appspot.gserviceaccount.com (2022-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9eb1144a00489057b9b103547f1e7f643f84443f

commit 9eb1144a00489057b9b103547f1e7f643f84443f
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Thu Jul 07 18:14:03 2022

CHECK when a group is added twice to the same TabGroupModel.

Bug: 1292451
Change-Id: Ibcded88ce98e3caaef95d135d9a6eb9e2e01db05
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749553
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: David Pennington <dpenning@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1021767}

[modify] https://crrev.com/9eb1144a00489057b9b103547f1e7f643f84443f/chrome/browser/ui/tabs/tab_group_model.cc


### rh...@gmail.com (2022-07-07)

Taylor,

Thanks for the analysis on https://crbug.com/chromium/1292451#c28, and https://crbug.com/chromium/1292451#c29. Also for the fix CL on #32, I really appreciate. Also can you give an advices to the dev team there for issue #1333995? There's bugs on tab groups in Lacros.

Thanks in advance

### tb...@chromium.org (2022-07-08)

No probs!

I don't have permission on that security bug, please CC me if you want my input

### [Deleted User] (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/19281762203088e1dc65e571a1d29c354d7e331c

commit 19281762203088e1dc65e571a1d29c354d7e331c
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Mon Jul 11 23:24:41 2022

Prevent extensions from using session restore during a tab drag session.

This brings the sessions api to parity with the tabs api, where tabstrip modifications during a tab drag session are not permitted.

Bug: 1292451
Change-Id: I3b6ffebea99e3537230fc91b5f13d9c0ea31fe82
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749086
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Reviewed-by: David Pennington <dpenning@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1022950}

[modify] https://crrev.com/19281762203088e1dc65e571a1d29c354d7e331c/chrome/browser/extensions/api/sessions/sessions_apitest.cc
[modify] https://crrev.com/19281762203088e1dc65e571a1d29c354d7e331c/chrome/browser/extensions/api/sessions/sessions_api.cc


### am...@chromium.org (2022-07-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-25)

It appears our bot friend did not make it to cover down on merge labels for this issue, given the rather small fix and the quite large amount of bake time this fix has had on canary, approving for M104 merge. 
Please go ahead and merge this fix to branch 5112 asap/NLT 12p PDT tomorrow/Tuesday, 26 July so this fix can be included in M104 stable cut tomorrow -- thank you! 

### gi...@appspot.gserviceaccount.com (2022-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fb293338bf40c01c43b798014af9687ba6471236

commit fb293338bf40c01c43b798014af9687ba6471236
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue Jul 26 17:21:25 2022

Prevent extensions from using session restore during a tab drag session.

This brings the sessions api to parity with the tabs api, where tabstrip modifications during a tab drag session are not permitted.

(cherry picked from commit 19281762203088e1dc65e571a1d29c354d7e331c)

Bug: 1292451
Change-Id: I3b6ffebea99e3537230fc91b5f13d9c0ea31fe82
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749086
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Reviewed-by: David Pennington <dpenning@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3787631
Reviewed-by: Krishna Govind <govind@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Auto-Submit: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5112@{#1205}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/fb293338bf40c01c43b798014af9687ba6471236/chrome/browser/extensions/api/sessions/sessions_apitest.cc
[modify] https://crrev.com/fb293338bf40c01c43b798014af9687ba6471236/chrome/browser/extensions/api/sessions/sessions_api.cc


### [Deleted User] (2022-07-26)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2022-07-28)

Congratulations, Rheza! The VRP Panel has decided to award you $2,000 for this report. The reward amount was decided up based on the mitigations of an extension and user interaction required, but also that the lower impact and exploitability from this issue. RCE does not appear likely or possible from this issue, as this results in a single byte read. Thank you for your efforts and reporting this issue to us.

### rh...@gmail.com (2022-07-28)

Thanks for the rewards.

### rz...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-28)

1. https://crrev.com/c/3788414
2. Low, no conflicts
3. 104
4. Yes

### gm...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-02)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions>API]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-09)

1. Just https://crrev.com/c/3816907
2. Low, no conflicts
3. 104
4. Yes

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d5d1ca138a1002175cbe17e031307aa233ae8737

commit d5d1ca138a1002175cbe17e031307aa233ae8737
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Fri Aug 12 09:31:22 2022

[M102-LTS] Prevent extensions from using session restore during a tab drag session.

This brings the sessions api to parity with the tabs api, where tabstrip modifications during a tab drag session are not permitted.

(cherry picked from commit 19281762203088e1dc65e571a1d29c354d7e331c)

Bug: 1292451
Change-Id: I3b6ffebea99e3537230fc91b5f13d9c0ea31fe82
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749086
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3816907
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1293}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/d5d1ca138a1002175cbe17e031307aa233ae8737/chrome/browser/extensions/api/sessions/sessions_apitest.cc
[modify] https://crrev.com/d5d1ca138a1002175cbe17e031307aa233ae8737/chrome/browser/extensions/api/sessions/sessions_api.cc


### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a2ee31572f38abaa087f72da25f56a49c1f6ae95

commit a2ee31572f38abaa087f72da25f56a49c1f6ae95
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Fri Aug 12 10:31:32 2022

[M96-LTS] Prevent extensions from using session restore during a tab drag session.

This brings the sessions api to parity with the tabs api, where tabstrip modifications during a tab drag session are not permitted.

(cherry picked from commit 19281762203088e1dc65e571a1d29c354d7e331c)

Bug: 1292451
Change-Id: I3b6ffebea99e3537230fc91b5f13d9c0ea31fe82
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3749086
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1022950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3788414
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1672}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/a2ee31572f38abaa087f72da25f56a49c1f6ae95/chrome/browser/extensions/api/sessions/sessions_apitest.cc
[modify] https://crrev.com/a2ee31572f38abaa087f72da25f56a49c1f6ae95/chrome/browser/extensions/api/sessions/sessions_api.cc


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1292451?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Extensions>API, UI>Browser>TopChrome>TabStrip]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058643)*
