#  heap-use-after-free in PrintDialogGtk::~PrintDialogGtk()

| Field | Value |
|-------|-------|
| **Issue ID** | [390459306](https://issues.chromium.org/issues/390459306) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Printing |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2025-01-17 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
heap-use-after-free in PrintDialogGtk::~PrintDialogGtk()

VERSION
Chromium	133.0.6931.0 (Developer Build) (64-bit) 
OS	Linux

REPRODUCTION CASE
1. Download the latest linux asan build
2. run the command:
./chrome --user-data-dir=/tmp/test --no-sandbox --disable-print-preview --load-extension=extension_dir about:blank

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab]
=================================================================
==1776395==ERROR: AddressSanitizer: heap-use-after-free on address 0x7d208e7afe28 at pc 0x5594b6214b9e bp 0x7ffd54106430 sp 0x7ffd54106428
READ of size 8 at 0x7d208e7afe28 thread T0 (chrome)
==1776395==WARNING: invalid path to external symbolizer!
==1776395==WARNING: Failed to use and restart external symbolizer!
    #0 0x5594b6214b9d in begin ./../../third_party/libc++/src/include/__vector/vector.h:344:109
    #1 0x5594b6214b9d in operator()<std::__Cr::vector<base::internal::CheckedObserverAdapter, std::__Cr::allocator<base::internal::CheckedObserverAdapter> > &> ./../../third_party/libc++/src/include/__ranges/access.h:75:12
    #2 0x5594b6214b9d in find_if<std::__Cr::vector<base::internal::CheckedObserverAdapter, std::__Cr::allocator<base::internal::CheckedObserverAdapter> > &, (lambda at ../../base/observer_list.h:330:21), std::__Cr::identity, std::__Cr::random_access_iterator_tag> ./../../base/ranges/algorithm.h:470:26
    #3 0x5594b6214b9d in base::ObserverList<aura::WindowObserver, true, true, base::internal::CheckedObserverAdapter>::RemoveObserver(aura::WindowObserver const*) ./../../base/observer_list.h:329:21
    #4 0x5594ba7fe649 in PrintDialogGtk::~PrintDialogGtk() ./../../ui/gtk/printing/print_dialog_gtk.cc:204:15
    #5 0x5594ba7fef83 in PrintDialogGtk::~PrintDialogGtk() ./../../ui/gtk/printing/print_dialog_gtk.cc:198:35
    #6 0x5594ba805432 in DestructOnSequence ./../../base/memory/ref_counted_delete_on_sequence.h:73:7
    #7 0x5594ba805432 in Release ./../../base/memory/ref_counted_delete_on_sequence.h:54:7
    #8 0x5594ba805432 in PrintDialogGtk::ReleaseDialog() ./../../ui/gtk/printing/print_dialog_gtk.cc:504:3
    #9 0x5594b8de9b81 in printing::PrintingContextLinux::~PrintingContextLinux() ./../../printing/printing_context_linux.cc:47:40
    #10 0x5594b8de9cf3 in printing::PrintingContextLinux::~PrintingContextLinux() ./../../printing/printing_context_linux.cc:43:47
    #11 0x5594ae506be9 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #12 0x5594ae506be9 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #13 0x5594ae506be9 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:269:71
    #14 0x5594ae506be9 in printing::PrinterQuery::~PrinterQuery() ./../../chrome/browser/printing/printer_query.cc:132:1
    #15 0x5594ae557389 in ~PrinterQueryOop ./../../chrome/browser/printing/printer_query_oop.cc:26:35
    #16 0x5594ae557389 in printing::PrinterQueryOop::~PrinterQueryOop() ./../../chrome/browser/printing/printer_query_oop.cc:26:35
    #17 0x5594ae581350 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #18 0x5594ae581350 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #19 0x5594ae581350 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:269:71
    #20 0x5594ae581350 in printing::(anonymous namespace)::OnDidScriptedPrint(scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery>>, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)>) ./../../chrome/browser/printing/print_view_manager_base.cc:146:1
    #21 0x5594ae5859b5 in Invoke<void (*)(scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery> >, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)>), scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery> >, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)> > ./../../base/functional/bind_internal.h:662:12
    #22 0x5594ae5859b5 in MakeItSo<void (*)(scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery> >, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)>), std::__Cr::tuple<scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery> >, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)> > > ./../../base/functional/bind_internal.h:921:12
    #23 0x5594ae5859b5 in RunImpl<void (*)(scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery> >, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)>), std::__Cr::tuple<scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery> >, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)> >, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1058:14
    #24 0x5594ae5859b5 in base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery>>, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)>), scoped_refptr<printing::PrintQueriesQueue>&&, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery>>&&, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)>&&>, base::internal::BindState<false, true, false, void (*)(scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery>>, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)>), scoped_refptr<printing::PrintQueriesQueue>, std::__Cr::unique_ptr<printing::PrinterQuery, std::__Cr::default_delete<printing::PrinterQuery>>, base::OnceCallback<void (mojo::StructPtr<printing::mojom::PrintPagesParams>)>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #25 0x5594ae5070b9 in Run ./../../base/functional/callback.h:156:12
    #26 0x5594ae5070b9 in printing::PrinterQuery::GetSettingsDone(base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings>>, printing::mojom::ResultCode) ./../../chrome/browser/printing/printer_query.cc:151:23
    #27 0x5594ae50a275 in Invoke<void (printing::PrinterQuery::*)(base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings> >, printing::mojom::ResultCode), printing::PrinterQuery *, base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings> >, printing::mojom::ResultCode> ./../../base/functional/bind_internal.h:729:12
    #28 0x5594ae50a275 in MakeItSo<void (printing::PrinterQuery::*)(base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings> >, printing::mojom::ResultCode), std::__Cr::tuple<base::internal::UnretainedWrapper<printing::PrinterQuery, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings> >, printing::mojom::ResultCode> > ./../../base/functional/bind_internal.h:921:12
    #29 0x5594ae50a275 in RunImpl<void (printing::PrinterQuery::*)(base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings> >, printing::mojom::ResultCode), std::__Cr::tuple<base::internal::UnretainedWrapper<printing::PrinterQuery, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings> >, printing::mojom::ResultCode>, 0UL, 1UL, 2UL, 3UL, 4UL> ./../../base/functional/bind_internal.h:1058:14
    #30 0x5594ae50a275 in base::internal::Invoker<base::internal::FunctorTraits<void (printing::PrinterQuery::*&&)(base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings>>, printing::mojom::ResultCode), printing::PrinterQuery*, base::OnceCallback<void ()>&&, std::__Cr::optional<bool>&&, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings>>&&, printing::mojom::ResultCode&&>, base::internal::BindState<true, true, false, void (printing::PrinterQuery::*)(base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings>>, printing::mojom::ResultCode), base::internal::UnretainedWrapper<printing::PrinterQuery, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings>>, printing::mojom::ResultCode>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #31 0x5594aeb59a32 in Run ./../../base/functional/callback.h:156:12
    #32 0x5594aeb59a32 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:210:34
    #33 0x5594aebc2f38 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:474:11)> ./../../base/task/common/task_annotator.h:106:5
    #34 0x5594aebc2f38 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:472:23
    #35 0x5594aebc1cda in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:40
    #36 0x5594aebc3c6a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #37 0x5594aed2675c in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:702:48
    #38 0x5594aebc482c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12
    #39 0x5594aeae91df in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #40 0x5594a523c902 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1099:18
    #41 0x5594a5243edc in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:156:15
    #42 0x5594a5233588 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:34:28
    #43 0x5594abc8a51f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:714:10
    #44 0x5594abc8dc25 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1292:10
    #45 0x5594abc8d306 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1144:12
    #46 0x5594abc87f0d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:348:36
    #47 0x5594abc884fb in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:361:10
    #48 0x55949a3d6a0a in ChromeMain ./../../chrome/app/chrome_main.cc:222:12
    #49 0x7fc08f995082 in __libc_start_main /build/glibc-LcI20x/glibc-2.31/csu/../csu/libc-start.c:308:16

0x7d208e7afe28 is located 424 bytes inside of 544-byte region [0x7d208e7afc80,0x7d208e7afea0)
freed by thread T0 (chrome) here:
    #0 0x55949a3d4a3d in operator delete(void*) _asan_rtl_:3
    #1 0x5594a6e44e15 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #2 0x5594a6e44e15 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #3 0x5594a6e44e15 in content::WebContentsViewAura::~WebContentsViewAura() ./../../content/browser/web_contents/web_contents_view_aura.cc:687:11
    #4 0x5594a6e452c3 in content::WebContentsViewAura::~WebContentsViewAura() ./../../content/browser/web_contents/web_contents_view_aura.cc:679:45
    #5 0x5594a6d0b25f in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #6 0x5594a6d0b25f in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #7 0x5594a6d0b25f in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:269:71
    #8 0x5594a6d0b25f in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web_contents/web_contents_impl.cc:1474:1
    #9 0x5594a6d0e4d3 in content::WebContentsImpl::~WebContentsImpl() ./../../content/browser/web_contents/web_contents_impl.cc:1325:37
    #10 0x5594a8cba228 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #11 0x5594a8cba228 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #12 0x5594a8cba228 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:269:71
    #13 0x5594a8cba228 in ~AppWindowContentsImpl ./../../extensions/browser/app_window/app_window_contents.cc:28:47
    #14 0x5594a8cba228 in extensions::AppWindowContentsImpl::~AppWindowContentsImpl() ./../../extensions/browser/app_window/app_window_contents.cc:28:47
    #15 0x5594a8cb1a96 in operator() ./../../third_party/libc++/src/include/__memory/unique_ptr.h:78:5
    #16 0x5594a8cb1a96 in reset ./../../third_party/libc++/src/include/__memory/unique_ptr.h:300:7
    #17 0x5594a8cb1a96 in ~unique_ptr ./../../third_party/libc++/src/include/__memory/unique_ptr.h:269:71
    #18 0x5594a8cb1a96 in extensions::AppWindow::~AppWindow() ./../../extensions/browser/app_window/app_window.cc:370:1
    #19 0x5594a8cb1ee3 in extensions::AppWindow::~AppWindow() ./../../extensions/browser/app_window/app_window.cc:368:25
    #20 0x5594a8cb3c9e in extensions::AppWindow::OnNativeClose() ./../../extensions/browser/app_window/app_window.cc:526:3
    #21 0x5594c63c7257 in operator() ./../../extensions/components/native_app_window/native_app_window_views.cc:57:30
    #22 0x5594c63c7257 in Invoke<(lambda at ../../extensions/components/native_app_window/native_app_window_views.cc:55:7), native_app_window::NativeAppWindowViews *> ./../../base/functional/bind_internal.h:647:12
    #23 0x5594c63c7257 in MakeItSo<(lambda at ../../extensions/components/native_app_window/native_app_window_views.cc:55:7), std::__Cr::tuple<base::internal::UnretainedWrapper<native_app_window::NativeAppWindowViews, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind_internal.h:921:12
    #24 0x5594c63c7257 in RunImpl<(lambda at ../../extensions/components/native_app_window/native_app_window_views.cc:55:7), std::__Cr::tuple<base::internal::UnretainedWrapper<native_app_window::NativeAppWindowViews, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind_internal.h:1058:14
    #25 0x5594c63c7257 in base::internal::Invoker<base::internal::FunctorTraits<native_app_window::NativeAppWindowViews::Init(extensions::AppWindow*, extensions::AppWindow::CreateParams const&)::$_0&&, native_app_window::NativeAppWindowViews*&&>, base::internal::BindState<false, false, false, native_app_window::NativeAppWindowViews::Init(extensions::AppWindow*, extensions::AppWindow::CreateParams const&)::$_0, base::internal::UnretainedWrapper<native_app_window::NativeAppWindowViews, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #26 0x5594b6a9d9c7 in Run ./../../base/functional/callback.h:156:12
    #27 0x5594b6a9d9c7 in views::WidgetDelegate::DeleteDelegate() ./../../ui/views/widget/widget_delegate.cc:313:25
    #28 0x5594b6a6e86c in views::Widget::HandleWidgetDestroyed() ./../../ui/views/widget/widget.cc:2582:23
    #29 0x5594b6b19d6c in views::DesktopNativeWidgetAura::OnHostClosed() ./../../ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:388:30
    #30 0x5594b6b57bb1 in views::DesktopWindowTreeHostPlatform::OnClosed() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:949:32
    #31 0x5594b6b4f6c0 in views::DesktopWindowTreeHostPlatform::CloseNow() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:421:22
    #32 0x5594b6b5c508 in Invoke<void (views::DesktopWindowTreeHostPlatform::*)(), const base::WeakPtr<views::DesktopWindowTreeHostPlatform> &> ./../../base/functional/bind_internal.h:729:12
    #33 0x5594b6b5c508 in MakeItSo<void (views::DesktopWindowTreeHostPlatform::*)(), std::__Cr::tuple<base::WeakPtr<views::DesktopWindowTreeHostPlatform> > > ./../../base/functional/bind_internal.h:945:5
    #34 0x5594b6b5c508 in RunImpl<void (views::DesktopWindowTreeHostPlatform::*)(), std::__Cr::tuple<base::WeakPtr<views::DesktopWindowTreeHostPlatform> >, 0UL> ./../../base/functional/bind_internal.h:1058:14
    #35 0x5594b6b5c508 in base::internal::Invoker<base::internal::FunctorTraits<void (views::DesktopWindowTreeHostPlatform::*&&)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform>&&>, base::internal::BindState<true, true, false, void (views::DesktopWindowTreeHostPlatform::*)(), base::WeakPtr<views::DesktopWindowTreeHostPlatform>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #36 0x5594aeb59a32 in Run ./../../base/functional/callback.h:156:12
    #37 0x5594aeb59a32 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:210:34
    #38 0x5594aebc2f38 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:474:11)> ./../../base/task/common/task_annotator.h:106:5
    #39 0x5594aebc2f38 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:472:23
    #40 0x5594aebc1cda in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:40
    #41 0x5594aebc3c6a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #42 0x5594aed2675c in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_glib.cc:702:48
    #43 0x5594aebc482c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:645:12
    #44 0x5594aeae91df in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134:14
    #45 0x5594a523c902 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser_main_loop.cc:1099:18
    #46 0x5594a5243edc in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser_main_runner_impl.cc:156:15
    #47 0x5594a5233588 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser_main.cc:34:28
    #48 0x5594abc8a51f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:714:10
    #49 0x5594abc8dc25 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content_main_runner_impl.cc:1292:10
    #50 0x5594abc8d306 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1144:12
    #51 0x5594abc87f0d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:348:36

previously allocated by thread T0 (chrome) here:
    #0 0x55949a3d41dd in operator new(unsigned long) _asan_rtl_:3
    #1 0x5594a6e4774e in make_unique<aura::Window, content::WebContentsViewAura *, aura::client::WindowType, 0> ./../../third_party/libc++/src/include/__memory/unique_ptr.h:767:26
    #2 0x5594a6e4774e in content::WebContentsViewAura::CreateAuraWindow(aura::Window*) ./../../content/browser/web_contents/web_contents_view_aura.cc:948:7
    #3 0x5594a6e47c48 in content::WebContentsViewAura::CreateView(aura::Window*) ./../../content/browser/web_contents/web_contents_view_aura.cc:994:3
    #4 0x5594a6d3bf81 in content::WebContentsImpl::Init(content::WebContents::CreateParams const&, blink::FramePolicy) ./../../content/browser/web_contents/web_contents_impl.cc:3825:10
    #5 0x5594a6cffac0 in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl*) ./../../content/browser/web_contents/web_contents_impl.cc:1555:17
    #6 0x5594a8cba704 in extensions::AppWindowContentsImpl::Initialize(content::BrowserContext*, content::RenderFrameHost*, GURL const&) ./../../extensions/browser/app_window/app_window_contents.cc:40:19
    #7 0x5594a8caf35a in extensions::AppWindow::Init(GURL const&, std::__Cr::unique_ptr<extensions::AppWindowContents, std::__Cr::default_delete<extensions::AppWindowContents>>, content::RenderFrameHost*, extensions::AppWindow::CreateParams const&) ./../../extensions/browser/app_window/app_window.cc:290:25
    #8 0x5594a8e234f0 in extensions::AppWindowCreateFunction::Run() ./../../extensions/browser/api/app_window/app_window_api.cc:382:15
    #9 0x5594a8ac8919 in ExtensionFunction::RunWithValidation() ./../../extensions/browser/extension_function.cc:493:10
    #10 0x5594a8ad814d in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost*, content::RenderProcessHost&, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value::List, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>) ./../../extensions/browser/extension_function_dispatcher.cc:442:15
    #11 0x5594a8ad6808 in extensions::ExtensionFunctionDispatcher::Dispatch(mojo::StructPtr<extensions::mojom::RequestParams>, content::RenderFrameHost&, base::OnceCallback<void (bool, base::Value::List, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>) ./../../extensions/browser/extension_function_dispatcher.cc:200:3
    #12 0x5594a8ac1e4c in extensions::ExtensionFrameHost::Request(mojo::StructPtr<extensions::mojom::RequestParams>, base::OnceCallback<void (bool, base::Value::List, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, mojo::StructPtr<extensions::mojom::ExtraResponseData>)>) ./../../extensions/browser/extension_frame_host.cc:64:9
    #13 0x5594a7e7a727 in extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder(extensions::mojom::LocalFrameHost*, mojo::Message*, std::__Cr::unique_ptr<mojo::MessageReceiverWithStatus, std::__Cr::default_delete<mojo::MessageReceiverWithStatus>>) ./gen/extensions/common/mojom/frame.mojom.cc:3957:13
    #14 0x5594ae95990c in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1005:56
    #15 0x5594ae9750ad in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:48:24
    #16 0x5594ae95f18e in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:724:20
    #17 0x5594b123791e in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1202:24
    #18 0x5594b1239823 in Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> ./../../base/functional/bind_internal.h:729:12
    #19 0x5594b1239823 in MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification> > ./../../base/functional/bind_internal.h:921:12
    #20 0x5594b1239823 in RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0UL, 1UL, 2UL> ./../../base/functional/bind_internal.h:1058:14
    #21 0x5594b1239823 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:971:12
    #22 0x5594aeb59a32 in Run ./../../base/functional/callback.h:156:12
    #23 0x5594aeb59a32 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:210:34
    #24 0x5594aebc2f38 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:474:11)> ./../../base/task/common/task_annotator.h:106:5
    #25 0x5594aebc2f38 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:472:23
    #26 0x5594aebc1cda in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:332:40
    #27 0x5594aebc3c6a in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #28 0x5594aed25e22 in base::MessagePumpGlib::HandleDispatch() ./../../base/message_loop/message_pump_glib.cc:656:46
    #29 0x5594aed28b98 in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) ./../../base/message_loop/message_pump_glib.cc:275:43
    #30 0x7fc09115417c in g_main_context_dispatch ??:0:0

SUMMARY: AddressSanitizer: heap-use-after-free (/chromium/chrome+0x2ac6eb9d) (BuildId: 37afaba83e6dd329)
Shadow bytes around the buggy address:
  0x7d208e7afb80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d208e7afc00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7d208e7afc80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d208e7afd00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7d208e7afd80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7d208e7afe00: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x7d208e7afe80: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d208e7aff00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa
  0x7d208e7aff80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d208e7b0000: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7d208e7b0080: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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

==1776395==ADDITIONAL INFO

==1776395==Note: Please include this section with the ASan report.
Task trace:
    #0 0x5594ae5073c8 in printing::PrinterQuery::PostSettingsDone(base::OnceCallback<void ()>, std::__Cr::optional<bool>, std::__Cr::unique_ptr<printing::PrintSettings, std::__Cr::default_delete<printing::PrintSettings>>, printing::mojom::ResultCode) ./../../chrome/browser/printing/printer_query.cc:162:7
    #1 0x5594b6b4ed7b in views::DesktopWindowTreeHostPlatform::Close() ./../../ui/views/widget/desktop_aura/desktop_window_tree_host_platform.cc:382:7
    #2 0x5594a9d92c7e in ChromeRuntimeAPIDelegate::ReloadExtension(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&) ./../../chrome/browser/extensions/api/runtime/chrome_runtime_api_delegate.cc:222:9
    #3 0x5594b1229772 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1141:13


Command line: `chrome --user-data-dir=/tmp/test--no-sandbox --disable-print-preview --load-extension=/extension --flag-switches-begin --flag-switches-end --ozone-platform-hint=auto --ozone-platform=x11 --file-url-path-alias=/gen=/chromium/gen about:blank`


MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==1776395==END OF ADDITIONAL INFO
==1776395==ABORTING
[1776959:1776959:0100/000000.797177:ERROR:child_process_sandbox_support_impl_linux.cc(108)] GetRenderStyleForStrike did not receive a response for family and size: Times New Roman, 25


## Attachments

- extension.zip (application/zip, 2.6 KB)
- script.js (text/javascript, 285 B)
- manifest.json (application/json, 5.8 KB)
- index.html (text/html, 66 B)
- background.js (text/javascript, 82 B)

## Timeline

### ad...@google.com (2025-01-17)

I was able to reproduce this with asan-linux-release-1402768.zip (133) but not with 132 nor 134.

### ad...@google.com (2025-01-17)

OK, I was eventually able to reproduce it on Canary 134 as well (134.0.6962.0). It happens only about 1 in 8 times for me.

### ad...@google.com (2025-01-17)

I managed to reproduce on 132 as well.

### ad...@google.com (2025-01-17)

I'm labeling this as Security\_Impact-None because I think the nonstandard `--disable-print-preview` flag seems to be a mandatory part of the reproduction steps. This makes sense because the GTK dialog in question doesn't appear at all so long as print preview is enabled.

I'm rating this as S1 because it's a browser process UaF but with the precondition of an extension being installed. In practice, the extension uninstalls itself and it seems like this crash probably involves winning a race, so it is *probably* hard to exploit this bug. Arguably therefore this should be S2, but let's err on the side of caution and keep it at S1 in case there are easier ways to exploit.

Note for future internal reproducers: I reproduced this on redshell using the ASAN builds retrieved by `fetchchromium`.

### xi...@chromium.org (2025-02-03)

[secondary security shepherd] awscreen@, friendly ping. Could you let us know if you are the right owner of this bug?

### th...@chromium.org (2025-02-04)

Looks like <https://crrev.com/1368999> fixed a nullptr crash, and caused this bug instead. Fix coming up.

### ap...@google.com (2025-02-04)

Project: chromium/src  

Branch: main  

Author: Lei Zhang <[thestig@chromium.org](mailto:thestig@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6229467>

Always clear GObject data in gtk::ClearAuraTransientParent()

---


Expand for full commit details
```
Always clear GObject data in gtk::ClearAuraTransientParent() 
 
Prior to https://crrev.com/1368999, gtk::ClearAuraTransientParent() can 
cause a nullptr deference crash due to the no RootWindow case. Now, that 
same case means ClearAuraTransientParent() becomes a no-op. This creates 
a new problem where the GObject data is stale. This follow-up reorders 
the ClearAuraTransientParent() implementation so it always clears the 
GObject data. Then there is no stale data, and no nullptr crash. 
 
Bug: 390459306 
Change-Id: Ia5ae03612e13d71f75d8258dfcc0ebb755d11116 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6229467 
Commit-Queue: Lei Zhang <thestig@chromium.org> 
Reviewed-by: Thomas Anderson <thomasanderson@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1415751}

```

---

Files:

- M `ui/gtk/gtk_util.cc`

---

Hash: ed9ec72d7cfa58b387eb47b43598d481a72df8fe  

Date:  Tue Feb 04 12:11:14 2025


---

### dr...@chromium.org (2025-02-13)

Extension contents for posterity

### sp...@google.com (2025-02-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of highly mitigated security bug in a non-sandboxed process, mitigated by precondition to install malicious extension, race condition, precondition of passing the --disable-print-preview, and limited attacker control from the single attempt given extension install and race condition 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-14)

Congratulations and thank you for reporting this issue to us!

### ch...@google.com (2025-05-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of highly mitigated security bug in a non-sandboxed process, mitigated by precondition to install malicious extension, race condition, precondition of passing the --disable-print-preview, and limited attacker control from the single attempt given extension install and race condition

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/390459306)*
