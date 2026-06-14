# Security: heap-use-after-free in check_client_download_request.cc when in incognito mode

| Field | Value |
|-------|-------|
| **Issue ID** | [40091050](https://issues.chromium.org/issues/40091050) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2018-04-09 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36

Steps to reproduce the problem:
chrome Version: 67.0.3392.0 (Developer Build) (64-bit)
ubuntu version: 16.04

Security: heap-use-after-free in check_client_download_request.cc

1.Get new version chrome:
 a) Build source code 
    config args.gn file as below:
		use_sanitizer_coverage = true
		is_asan = true
		is_debug = false
		enable_nacl = false
		treat_warnings_as_errors = false
	ninja -j16 -C out/chrome_asan chrome
  b) Or just download newst chrome binary version:
	asan-linux-debug-549093.zip	2018-04-08 23:57:45	1619.37MB	549093	22bb0f8b4e1a9ee17bc14e9c31bb42bd8d4239b3
	https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-debug%2Fasan-linux-debug-549093.zip?generation=1523231865537112&alt=media
2.Build a mini web server.
	I used python twisted module to build the webserver.
	1) cp 1.swf webserver/res/1.swf
	2) python webserver/web.py

3. 
	1) Drag crash.html to chrome browser. 
	2) May need to perform several refreshes(F5), and then close the browser.
	3) And get  "heap-use-after-free"

What is the expected behavior?

What went wrong?
==17100==ERROR: AddressSanitizer: heap-use-after-free on address 0x619000565990 at pc 0x555c92e3fd4e bp 0x7ffec8aed470 sp 0x7ffec8aed468
READ of size 8 at 0x619000565990 thread T0 (chrome)
    #0 0x555c92e3fd4d in safe_browsing::CheckClientDownloadRequest::OnDownloadDestroyed(download::DownloadItem*) chrome/browser/safe_browsing/download_protection/check_client_download_request.cc:187:3
    #1 0x7fe4c9326afe in download::DownloadItemImpl::~DownloadItemImpl() components/download/internal/common/download_item_impl.cc:425:14
    #2 0x7fe4c932742f in download::DownloadItemImpl::~DownloadItemImpl() components/download/internal/common/download_item_impl.cc:416:39
    #3 0x7fe4ddf78bf2 in operator() buildtools/third_party/libc++/trunk/include/memory:2286:5
    #4 0x7fe4ddf78bf2 in reset buildtools/third_party/libc++/trunk/include/memory:2599
    #5 0x7fe4ddf78bf2 in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2553
    #6 0x7fe4ddf78bf2 in std::__1::pair<unsigned int const, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >::~pair() buildtools/third_party/libc++/trunk/include/utility:312
    #7 0x7fe4ddf7891f in __destroy<std::__1::pair<const unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > > > buildtools/third_party/libc++/trunk/include/memory:1732:23
    #8 0x7fe4ddf7891f in destroy<std::__1::pair<const unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > > > buildtools/third_party/libc++/trunk/include/memory:1595
    #9 0x7fe4ddf7891f in std::__1::__hash_table<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::__unordered_map_hasher<unsigned int, std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::hash<unsigned int>, true>, std::__1::__unordered_map_equal<unsigned int, std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::equal_to<unsigned int>, true>, std::__1::allocator<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > > > >::__deallocate_node(std::__1::__hash_node_base<std::__1::__hash_node<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, void*>*>*) buildtools/third_party/libc++/trunk/include/__hash_table:1564
    #10 0x7fe4ddf8bca2 in std::__1::__hash_table<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::__unordered_map_hasher<unsigned int, std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::hash<unsigned int>, true>, std::__1::__unordered_map_equal<unsigned int, std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::equal_to<unsigned int>, true>, std::__1::allocator<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > > > >::clear() buildtools/third_party/libc++/trunk/include/__hash_table:1814:9
    #11 0x7fe4ddf3b99f in clear buildtools/third_party/libc++/trunk/include/unordered_map:1087:38
    #12 0x7fe4ddf3b99f in content::DownloadManagerImpl::Shutdown() content/browser/download/download_manager_impl.cc:544
    #13 0x555c892bc445 in DownloadCoreServiceImpl::Shutdown() chrome/browser/download/download_core_service_impl.cc:144:51
    #14 0x7fe4c7c452fc in KeyedServiceFactory::ContextShutdown(base::SupportsUserData*) components/keyed_service/core/keyed_service_factory.cc:113:17
    #15 0x7fe4c460867e in BrowserContextKeyedServiceFactory::BrowserContextShutdown(content::BrowserContext*) components/keyed_service/content/browser_context_keyed_service_factory.cc:84:24
    #16 0x7fe4c4608a30 in BrowserContextKeyedServiceFactory::ContextShutdown(base::SupportsUserData*) components/keyed_service/content/browser_context_keyed_service_factory.cc:118:3
    #17 0x7fe4c7c33790 in DependencyManager::DestroyContextServices(base::SupportsUserData*) components/keyed_service/core/dependency_manager.cc:91:14
    #18 0x7fe4c45fd11e in BrowserContextDependencyManager::DestroyBrowserContextServices(content::BrowserContext*) components/keyed_service/content/browser_context_dependency_manager.cc:52:22
    #19 0x555c8a022f91 in OffTheRecordProfileImpl::~OffTheRecordProfileImpl() chrome/browser/profiles/off_the_record_profile_impl.cc:204:51
    #20 0x555c8a02396f in OffTheRecordProfileImpl::~OffTheRecordProfileImpl() chrome/browser/profiles/off_the_record_profile_impl.cc:196:53
    #21 0x555c89feba74 in operator() buildtools/third_party/libc++/trunk/include/memory:2286:5
    #22 0x555c89feba74 in reset buildtools/third_party/libc++/trunk/include/memory:2599
    #23 0x555c89feba74 in ProfileImpl::DestroyOffTheRecordProfile() chrome/browser/profiles/profile_impl.cc:802
    #24 0x555c8a00a858 in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile*) chrome/browser/profiles/profile_destroyer.cc:69:38
    #25 0x555c96180b94 in Browser::~Browser() chrome/browser/ui/browser.cc:560:7
    #26 0x555c9618419f in Browser::~Browser() chrome/browser/ui/browser.cc:474:21
    #27 0x555c9714a33e in operator() buildtools/third_party/libc++/trunk/include/memory:2286:5
    #28 0x555c9714a33e in reset buildtools/third_party/libc++/trunk/include/memory:2599
    #29 0x555c9714a33e in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2553
    #30 0x555c9714a33e in BrowserView::~BrowserView() chrome/browser/ui/views/frame/browser_view.cc:442
    #31 0x555c9714a81f in BrowserView::~BrowserView() chrome/browser/ui/views/frame/browser_view.cc:400:29
    #32 0x7fe4c0590fda in views::View::~View() ui/views/view.cc:163:9
    #33 0x7fe4c06a12a5 in views::NonClientView::~NonClientView() ui/views/window/non_client_view.cc:56:1
    #34 0x7fe4c06a141f in views::NonClientView::~NonClientView() ui/views/window/non_client_view.cc:52:33
    #35 0x7fe4c0599f5f in operator() buildtools/third_party/libc++/trunk/include/memory:2286:5
    #36 0x7fe4c0599f5f in reset buildtools/third_party/libc++/trunk/include/memory:2599
    #37 0x7fe4c0599f5f in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2553
    #38 0x7fe4c0599f5f in views::View::DoRemoveChildView(views::View*, bool, bool, bool, views::View*) ui/views/view.cc:2139
    #39 0x7fe4c059da35 in views::View::RemoveAllChildViews(bool) ui/views/view.cc:301:5
    #40 0x7fe4c0610bbc in views::internal::RootView::~RootView() ui/views/widget/root_view.cc:184:5
    #41 0x555c971ae39b in BrowserRootView::~BrowserRootView() chrome/browser/ui/views/frame/browser_root_view.h:23:7
    #42 0x555c971ae3df in BrowserRootView::~BrowserRootView() chrome/browser/ui/views/frame/browser_root_view.h:23:7
    #43 0x7fe4c0626da7 in operator() buildtools/third_party/libc++/trunk/include/memory:2286:5
    #44 0x7fe4c0626da7 in reset buildtools/third_party/libc++/trunk/include/memory:2599
    #45 0x7fe4c0626da7 in views::Widget::DestroyRootView() ui/views/widget/widget.cc:1452
    #46 0x7fe4c0625f79 in views::Widget::~Widget() ui/views/widget/widget.cc:183:3
    #47 0x555c971a4308 in BrowserFrame::~BrowserFrame() chrome/browser/ui/views/frame/browser_frame.cc:62:1
    #48 0x555c971a444f in BrowserFrame::~BrowserFrame() chrome/browser/ui/views/frame/browser_frame.cc:61:31
    #49 0x7fe4c0746e0a in views::DesktopNativeWidgetAura::~DesktopNativeWidgetAura() ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:256:5
    #50 0x555c97964f53 in DesktopBrowserFrameAura::~DesktopBrowserFrameAura() chrome/browser/ui/views/frame/desktop_browser_frame_aura.cc:41:1
    #51 0x555c97388c7b in DesktopBrowserFrameAuraX11::~DesktopBrowserFrameAuraX11() chrome/browser/ui/views/frame/desktop_browser_frame_aurax11.cc:27:1
    #52 0x555c97388e7f in DesktopBrowserFrameAuraX11::~DesktopBrowserFrameAuraX11() chrome/browser/ui/views/frame/desktop_browser_frame_aurax11.cc:26:59
    #53 0x7fe4c074b696 in views::DesktopNativeWidgetAura::OnHostClosed() ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:324:5
    #54 0x555c979653db in DesktopBrowserFrameAura::OnHostClosed() chrome/browser/ui/views/frame/desktop_browser_frame_aura.cc:48:28
    #55 0x7fe4c07fc308 in views::DesktopWindowTreeHostX11::CloseNow() ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc:508:32
    #56 0x555c97967a59 in BrowserDesktopWindowTreeHostX11::CloseNow() chrome/browser/ui/views/frame/browser_desktop_window_tree_host_x11.cc:66:29
    #57 0x7fe4c0837ccd in void base::internal::FunctorTraits<void (views::DesktopWindowTreeHostX11::*)(), void>::Invoke<base::WeakPtr<views::DesktopWindowTreeHostX11> const&>(void (views::DesktopWindowTreeHostX11::*)(), base::WeakPtr<views::DesktopWindowTreeHostX11> const&&&) base/bind_internal.h:447:12
    #58 0x7fe4c083797b in void base::internal::InvokeHelper<true, void>::MakeItSo<void (views::DesktopWindowTreeHostX11::* const&)(), base::WeakPtr<views::DesktopWindowTreeHostX11> const&>(void (views::DesktopWindowTreeHostX11::* const&&&)(), base::WeakPtr<views::DesktopWindowTreeHostX11> const&&&) base/bind_internal.h:550:5
    #59 0x7fe4c083773e in void base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostX11::*)(), base::WeakPtr<views::DesktopWindowTreeHostX11> >, void ()>::RunImpl<void (views::DesktopWindowTreeHostX11::* const&)(), std::__1::tuple<base::WeakPtr<views::DesktopWindowTreeHostX11> > const&, 0ul>(void (views::DesktopWindowTreeHostX11::* const&&&)(), std::__1::tuple<base::WeakPtr<views::DesktopWindowTreeHostX11> > const&&&, std::__1::integer_sequence<unsigned long, 0ul>) base/bind_internal.h:604:12
    #60 0x7fe4c0837642 in base::internal::Invoker<base::internal::BindState<void (views::DesktopWindowTreeHostX11::*)(), base::WeakPtr<views::DesktopWindowTreeHostX11> >, void ()>::Run(base::internal::BindStateBase*) base/bind_internal.h:586:12
    #61 0x7fe4f41b6608 in base::OnceCallback<void ()>::Run() && base/callback.h:95:12
    #62 0x7fe4f42c7129 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:101:33
    #63 0x7fe4f44da4b7 in base::internal::IncomingTaskQueue::RunTask(base::PendingTask*) base/message_loop/incoming_task_queue.cc:124:19
    #64 0x7fe4f44f8225 in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:354:25
    #65 0x7fe4f44f8b6d in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message_loop/message_loop.cc:364:5
    #66 0x7fe4f44f94cf in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:408:16
    #67 0x7fe4f451dc7b in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:263:25
    #68 0x7fe4f451fe9f in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:109:43
    #69 0x7fe48d098196 in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4a196)

0x619000565990 is located 16 bytes inside of 1040-byte region [0x619000565980,0x619000565d90)
freed by thread T0 (chrome) here:
    #0 0x555c82606b02 in operator delete(void*) /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:149:3
    #1 0x555c92e438db in safe_browsing::CheckClientDownloadRequest::~CheckClientDownloadRequest() chrome/browser/safe_browsing/download_protection/check_client_download_request.cc:311:59
    #2 0x555c92e2d917 in void content::BrowserThread::DeleteOnThread<(content::BrowserThread::ID)0>::Destruct<safe_browsing::CheckClientDownloadRequest>(safe_browsing::CheckClientDownloadRequest const*) content/public/browser/browser_thread.h:209:9
    #3 0x555c92e2d778 in base::RefCountedThreadSafe<safe_browsing::CheckClientDownloadRequest, content::BrowserThread::DeleteOnUIThread>::Release() const base/memory/ref_counted.h:387:7
    #4 0x555c92e2d6ef in scoped_refptr<safe_browsing::CheckClientDownloadRequest>::Release(safe_browsing::CheckClientDownloadRequest*) base/memory/scoped_refptr.h:280:8
    #5 0x555c92e288ca in scoped_refptr<safe_browsing::CheckClientDownloadRequest>::~scoped_refptr() base/memory/scoped_refptr.h:208:7
    #6 0x555c92e38263 in __destroy<scoped_refptr<safe_browsing::CheckClientDownloadRequest> > buildtools/third_party/libc++/trunk/include/memory:1732:23
    #7 0x555c92e38263 in destroy<scoped_refptr<safe_browsing::CheckClientDownloadRequest> > buildtools/third_party/libc++/trunk/include/memory:1595
    #8 0x555c92e38263 in std::__1::__tree<scoped_refptr<safe_browsing::CheckClientDownloadRequest>, std::__1::less<scoped_refptr<safe_browsing::CheckClientDownloadRequest> >, std::__1::allocator<scoped_refptr<safe_browsing::CheckClientDownloadRequest> > >::erase(std::__1::__tree_const_iterator<scoped_refptr<safe_browsing::CheckClientDownloadRequest>, std::__1::__tree_node<scoped_refptr<safe_browsing::CheckClientDownloadRequest>, void*>*, long>) buildtools/third_party/libc++/trunk/include/__tree:2368
    #9 0x555c92e378fb in unsigned long std::__1::__tree<scoped_refptr<safe_browsing::CheckClientDownloadRequest>, std::__1::less<scoped_refptr<safe_browsing::CheckClientDownloadRequest> >, std::__1::allocator<scoped_refptr<safe_browsing::CheckClientDownloadRequest> > >::__erase_unique<scoped_refptr<safe_browsing::CheckClientDownloadRequest> >(scoped_refptr<safe_browsing::CheckClientDownloadRequest> const&) buildtools/third_party/libc++/trunk/include/__tree:2391:5
    #10 0x555c92e1a204 in erase buildtools/third_party/libc++/trunk/include/set:630:25
    #11 0x555c92e1a204 in safe_browsing::DownloadProtectionService::RequestFinished(safe_browsing::CheckClientDownloadRequest*) chrome/browser/safe_browsing/download_protection/download_protection_service.cc:216
    #12 0x555c92e3fa73 in safe_browsing::CheckClientDownloadRequest::FinishRequest(safe_browsing::DownloadCheckResult, safe_browsing::DownloadCheckResultReason) chrome/browser/safe_browsing/download_protection/check_client_download_request.cc:1068:14
    #13 0x555c92e3e3ac in safe_browsing::CheckClientDownloadRequest::Cancel() chrome/browser/safe_browsing/download_protection/check_client_download_request.cc:178:3
    #14 0x555c92e3fd24 in safe_browsing::CheckClientDownloadRequest::OnDownloadDestroyed(download::DownloadItem*) chrome/browser/safe_browsing/download_protection/check_client_download_request.cc:186:3
    #15 0x7fe4c9326afe in download::DownloadItemImpl::~DownloadItemImpl() components/download/internal/common/download_item_impl.cc:425:14
    #16 0x7fe4c932742f in download::DownloadItemImpl::~DownloadItemImpl() components/download/internal/common/download_item_impl.cc:416:39
    #17 0x7fe4ddf78bf2 in operator() buildtools/third_party/libc++/trunk/include/memory:2286:5
    #18 0x7fe4ddf78bf2 in reset buildtools/third_party/libc++/trunk/include/memory:2599
    #19 0x7fe4ddf78bf2 in ~unique_ptr buildtools/third_party/libc++/trunk/include/memory:2553
    #20 0x7fe4ddf78bf2 in std::__1::pair<unsigned int const, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >::~pair() buildtools/third_party/libc++/trunk/include/utility:312
    #21 0x7fe4ddf7891f in __destroy<std::__1::pair<const unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > > > buildtools/third_party/libc++/trunk/include/memory:1732:23
    #22 0x7fe4ddf7891f in destroy<std::__1::pair<const unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > > > buildtools/third_party/libc++/trunk/include/memory:1595
    #23 0x7fe4ddf7891f in std::__1::__hash_table<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::__unordered_map_hasher<unsigned int, std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::hash<unsigned int>, true>, std::__1::__unordered_map_equal<unsigned int, std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::equal_to<unsigned int>, true>, std::__1::allocator<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > > > >::__deallocate_node(std::__1::__hash_node_base<std::__1::__hash_node<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, void*>*>*) buildtools/third_party/libc++/trunk/include/__hash_table:1564
    #24 0x7fe4ddf8bca2 in std::__1::__hash_table<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::__unordered_map_hasher<unsigned int, std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::hash<unsigned int>, true>, std::__1::__unordered_map_equal<unsigned int, std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > >, std::__1::equal_to<unsigned int>, true>, std::__1::allocator<std::__1::__hash_value_type<unsigned int, std::__1::unique_ptr<download::DownloadItemImpl, std::__1::default_delete<download::DownloadItemImpl> > > > >::clear() buildtools/third_party/libc++/trunk/include/__hash_table:1814:9
    #25 0x7fe4ddf3b99f in clear buildtools/third_party/libc++/trunk/include/unordered_map:1087:38
    #26 0x7fe4ddf3b99f in content::DownloadManagerImpl::Shutdown() content/browser/download/download_manager_impl.cc:544
    #27 0x555c892bc445 in DownloadCoreServiceImpl::Shutdown() chrome/browser/download/download_core_service_impl.cc:144:51
    #28 0x7fe4c7c452fc in KeyedServiceFactory::ContextShutdown(base::SupportsUserData*) components/keyed_service/core/keyed_service_factory.cc:113:17
    #29 0x7fe4c460867e in BrowserContextKeyedServiceFactory::BrowserContextShutdown(content::BrowserContext*) components/keyed_service/content/browser_context_keyed_service_factory.cc:84:24
    #30 0x7fe4c4608a30 in BrowserContextKeyedServiceFactory::ContextShutdown(base::SupportsUserData*) components/keyed_service/content/browser_context_keyed_service_factory.cc:118:3
    #31 0x7fe4c7c33790 in DependencyManager::DestroyContextServices(base::SupportsUserData*) components/keyed_service/core/dependency_manager.cc:91:14
    #32 0x7fe4c45fd11e in BrowserContextDependencyManager::DestroyBrowserContextServices(content::BrowserContext*) components/keyed_service/content/browser_context_dependency_manager.cc:52:22
    #33 0x555c8a022f91 in OffTheRecordProfileImpl::~OffTheRecordProfileImpl() chrome/browser/profiles/off_the_record_profile_impl.cc:204:51
    #34 0x555c8a02396f in OffTheRecordProfileImpl::~OffTheRecordProfileImpl() chrome/browser/profiles/off_the_record_profile_impl.cc:196:53
    #35 0x555c89feba74 in operator() buildtools/third_party/libc++/trunk/include/memory:2286:5
    #36 0x555c89feba74 in reset buildtools/third_party/libc++/trunk/include/memory:2599
    #37 0x555c89feba74 in ProfileImpl::DestroyOffTheRecordProfile() chrome/browser/profiles/profile_impl.cc:802
    #38 0x555c8a00a858 in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile*) chrome/browser/profiles/profile_destroyer.cc:69:38
    #39 0x555c96180b94 in Browser::~Browser() chrome/browser/ui/browser.cc:560:7
    #40 0x555c9618419f in Browser::~Browser() chrome/browser/ui/browser.cc:474:21

previously allocated by thread T0 (chrome) here:
    #0 0x555c82605f22 in operator new(unsigned long) /b/build/slave/linux_upload_clang/build/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cc:92:3
    #1 0x555c92e1424f in safe_browsing::DownloadProtectionService::CheckClientDownload(download::DownloadItem*, base::RepeatingCallback<void (safe_browsing::DownloadCheckResult)> const&) chrome/browser/safe_browsing/download_protection/download_protection_service.cc:132:7
    #2 0x555c892f30a1 in ChromeDownloadManagerDelegate::IsDownloadReadyForCompletion(download::DownloadItem*, base::RepeatingCallback<void ()> const&) chrome/browser/download/chrome_download_manager_delegate.cc:427:16
    #3 0x555c892f5a54 in ChromeDownloadManagerDelegate::ShouldCompleteDownload(download::DownloadItem*, base::RepeatingCallback<void ()> const&) chrome/browser/download/chrome_download_manager_delegate.cc:485:10
    #4 0x7fe4ddf39d10 in content::DownloadManagerImpl::ShouldCompleteDownload(download::DownloadItemImpl*, base::RepeatingCallback<void ()> const&) content/browser/download/download_manager_impl.cc:467:18
    #5 0x7fe4c93654b0 in download::DownloadItemImpl::IsDownloadReadyForCompletion(base::RepeatingCallback<void ()> const&) components/download/internal/common/download_item_impl.cc:2099:19
    #6 0x7fe4c932b0ea in download::DownloadItemImpl::MaybeCompleteDownload() components/download/internal/common/download_item_impl.cc:1693:8
    #7 0x7fe4c9362d9e in download::DownloadItemImpl::OnTargetResolved() components/download/internal/common/download_item_impl.cc:1677:3
    #8 0x7fe4c9363a75 in download::DownloadItemImpl::OnDownloadRenamedToIntermediateName(download::DownloadInterruptReason, base::FilePath const&) components/download/internal/common/download_item_impl.cc:1638:3
    #9 0x7fe4c93a18be in void base::internal::FunctorTraits<void (download::DownloadItemImpl::*)(download::DownloadInterruptReason, base::FilePath const&), void>::Invoke<base::WeakPtr<download::DownloadItemImpl> const&, download::DownloadInterruptReason, base::FilePath const&>(void (download::DownloadItemImpl::*)(download::DownloadInterruptReason, base::FilePath const&), base::WeakPtr<download::DownloadItemImpl> const&&&, download::DownloadInterruptReason&&, base::FilePath const&&&) base/bind_internal.h:447:12
    #10 0x7fe4c93a153b in void base::internal::InvokeHelper<true, void>::MakeItSo<void (download::DownloadItemImpl::* const&)(download::DownloadInterruptReason, base::FilePath const&), base::WeakPtr<download::DownloadItemImpl> const&, download::DownloadInterruptReason, base::FilePath const&>(void (download::DownloadItemImpl::* const&&&)(download::DownloadInterruptReason, base::FilePath const&), base::WeakPtr<download::DownloadItemImpl> const&&&, download::DownloadInterruptReason&&, base::FilePath const&&&) base/bind_internal.h:550:5
    #11 0x7fe4c93a1291 in void base::internal::Invoker<base::internal::BindState<void (download::DownloadItemImpl::*)(download::DownloadInterruptReason, base::FilePath const&), base::WeakPtr<download::DownloadItemImpl> >, void (download::DownloadInterruptReason, base::FilePath const&)>::RunImpl<void (download::DownloadItemImpl::* const&)(download::DownloadInterruptReason, base::FilePath const&), std::__1::tuple<base::WeakPtr<download::DownloadItemImpl> > const&, 0ul>(void (download::DownloadItemImpl::* const&&&)(download::DownloadInterruptReason, base::FilePath const&), std::__1::tuple<base::WeakPtr<download::DownloadItemImpl> > const&&&, std::__1::integer_sequence<unsigned long, 0ul>, download::DownloadInterruptReason&&, base::FilePath const&) base/bind_internal.h:604:12
    #12 0x7fe4c93a10b3 in base::internal::Invoker<base::internal::BindState<void (download::DownloadItemImpl::*)(download::DownloadInterruptReason, base::FilePath const&), base::WeakPtr<download::DownloadItemImpl> >, void (download::DownloadInterruptReason, base::FilePath const&)>::Run(base::internal::BindStateBase*, download::DownloadInterruptReason, base::FilePath const&) base/bind_internal.h:586:12
    #13 0x7fe4c930a773 in base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>::Run(download::DownloadInterruptReason, base::FilePath const&) && base/callback.h:135:12
    #14 0x7fe4c930a49b in void base::internal::FunctorTraits<base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>, void>::Invoke<base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>, download::DownloadInterruptReason, base::FilePath>(base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>&&, download::DownloadInterruptReason&&, base::FilePath&&) base/bind_internal.h:506:49
    #15 0x7fe4c930a133 in void base::internal::InvokeHelper<false, void>::MakeItSo<base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>, download::DownloadInterruptReason, base::FilePath>(base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>&&, download::DownloadInterruptReason&&, base::FilePath&&) base/bind_internal.h:530:12
    #16 0x7fe4c930a0bb in void base::internal::Invoker<base::internal::BindState<base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>, download::DownloadInterruptReason, base::FilePath>, void ()>::RunImpl<base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>, std::__1::tuple<download::DownloadInterruptReason, base::FilePath>, 0ul, 1ul>(base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>&&, std::__1::tuple<download::DownloadInterruptReason, base::FilePath>&&, std::__1::integer_sequence<unsigned long, 0ul, 1ul>) base/bind_internal.h:604:12
    #17 0x7fe4c9309f7f in base::internal::Invoker<base::internal::BindState<base::RepeatingCallback<void (download::DownloadInterruptReason, base::FilePath const&)>, download::DownloadInterruptReason, base::FilePath>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:572:12
    #18 0x7fe4f41b6608 in base::OnceCallback<void ()>::Run() && base/callback.h:95:12
    #19 0x7fe4f42c7129 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/debug/task_annotator.cc:101:33
    #20 0x7fe4f44da4b7 in base::internal::IncomingTaskQueue::RunTask(base::PendingTask*) base/message_loop/incoming_task_queue.cc:124:19
    #21 0x7fe4f44f8225 in base::MessageLoop::RunTask(base::PendingTask*) base/message_loop/message_loop.cc:354:25
    #22 0x7fe4f44f8b6d in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message_loop/message_loop.cc:364:5
    #23 0x7fe4f44f94cf in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:408:16
    #24 0x7fe4f451dc7b in base::MessagePumpGlib::HandleDispatch() base/message_loop/message_pump_glib.cc:263:25
    #25 0x7fe4f451fe9f in base::(anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_loop/message_pump_glib.cc:109:43
    #26 0x7fe48d098196 in g_main_context_dispatch (/lib/x86_64-linux-gnu/libglib-2.0.so.0+0x4a196)

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/safe_browsing/download_protection/check_client_download_request.cc:187:3 in safe_browsing::CheckClientDownloadRequest::OnDownloadDestroyed(download::DownloadItem*)
Shadow bytes around the buggy address:
  0x0c32800a4ae0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800a4af0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800a4b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800a4b10: fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c32800a4b20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0c32800a4b30: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800a4b40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800a4b50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800a4b60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800a4b70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800a4b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
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
==17100==ABORTING

Did this work before? N/A 

Chrome version: 67.0.3392.0  Channel: dev
OS Version: ubuntu version: 16.04
Flash Version: Shockwave Flash 29.0 r0

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [repro_video.mp4](attachments/repro_video.mp4) (video/mp4, 8.9 MB)
- [repro_video2.mp4](attachments/repro_video2.mp4) (video/mp4, 9.0 MB)
- [asan_symbolized2.log](attachments/asan_symbolized2.log) (text/plain, 51.5 KB)
- [ASANsymbolizedvmodule.log](attachments/ASANsymbolizedvmodule.log) (text/plain, 51.2 KB)

## Timeline

### cd...@gmail.com (2018-04-09)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-04-09)

have to run chrome with --incogniton option.
./chrome --incognito

### ji...@chromium.org (2018-04-09)

[Comment Deleted]

[Monorail components: Services>Safebrowsing]

### ji...@chromium.org (2018-04-10)

Based on stacktrace, it fails at a DCHECK, and no similar crash found in crash/ for M67.

Will look at this at our weekly triage meeting. 

### ji...@chromium.org (2018-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-04-13)

Based on https://crbug.com/chromium/830303#c4, lowering the priority and removing RBS label.

### sh...@chromium.org (2018-04-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-18)

[Empty comment from Monorail migration]

### np...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### ji...@chromium.org (2018-04-20)

I cannot reproduce this issue on HEAD (68.0.3401.0). 

Could you confirm the following details:

1. Did this crash only happen on downloading 1.swf  file you provided? Or it happened for other executable downloads.
2. When you dragged the crash.html file to browser, did you see any download warning?
3. When did you close browser? Immediately after the download started? After seeing the warning? or else (I did try to refresh the page multiple times , but cannot repro this crash.)

### cd...@gmail.com (2018-04-21)

Hi,@jialiul
I tested it again in asan-linux-debug-551605(Version 68.0.3400.0 (Developer Build) (64-bit)）, and it can be successfully reproduced.
For the questions:
1) I tested it with other normal swf files and it can be replicated, so it not be relevant to the swf content.

2）As you can see from the video, there will be warning("this type of file can harm blabla") at the bottom of browser after the download is successful.

3)As you can see from the video, I just F5 2 times, and closed before second swf file warning popup. After many tests, when the download starts, and the warning message has not yet appeared, it can be stably reproduced.


### sh...@chromium.org (2018-04-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-04-21)

[Empty comment from Monorail migration]

### ji...@chromium.org (2018-04-24)

Thanks cdsrc2016@! Now I can occasionally repro this issue (something like 1 out of 10 tries). The timing of closing browser seems quite subtle. 
I have a tiny CL up to fix this issue.

cdsrc2016@, It sounds like you can more consistently repro this issue. Could you patch the above CL to give it a try? I'm not 100% sure if this indeed will fix the problem. 

Thanks! 

Also + other team members to help repro and test.

### cd...@gmail.com (2018-04-24)

Hi,晚上好~
Where can I see the CL?


### ji...@chromium.org (2018-04-24)

Oops, my bad. Hitting send too fast. Here's link to the change:
https://chromium-review.googlesource.com/c/chromium/src/+/1024864


### cd...@gmail.com (2018-04-24)

Hi,
I patched CL to new chromium(Version 68.0.3404.0),and still get UAF consistently.




### ji...@chromium.org (2018-04-24)

Thanks for the quick reply!  Really appreciate for your help here. 

Could you append "2>&1 | tools/valgrind/asan/asan_symbolize.py"  to the command line when you trigger chromium, such that the output will be symbolized?  I'd like to see if the crashing point has changed. Thanks!


### cd...@gmail.com (2018-04-24)

Hi,here is a asan log file.
Thanks~~

### va...@chromium.org (2018-04-24)

I changed the POC to:

<head>
    <meta http-equiv="refresh" content="1">
</head>
<body>
<object type="image/svg+xml" data="http://127.0.0.1:8605/res/1.swf" >
</object>
</body>

The page now auto-refreshes every second and tries to download the .swf fie but I still can't repro it.

I tried this on ToT and on asan-linux-debug-551829.

### va...@chromium.org (2018-04-24)

OP: Could you please run chrome with: --vmodule="*download*=2" and share the output with us? Thanks.

### ji...@chromium.org (2018-04-24)

RE #22, downloading multiple files doesn't trigger crash, but shutting down the browser when CheckClientDownloadRequest is in flight (occasionally) does. 
I was able to reproduce the crash a couple of times. 

So far I reached the conclusion this crash is caused by DownloadManagerImpl instance is somehow destructed before ChromeDownloadManagerDelegate:: CheckClientDownloadDone(..) is called. But I couldn't figure out why that is possible. 

Will keep digging tomorrow. 

### cd...@gmail.com (2018-04-24)

The attachment is a log file with the "--vmodule="*download*=2"" option added. After adding the "--vmodule="*download*=2"" option, no difference was found at the first sight.
By the way,did you run chrome with  --incogniton option? I consistently repro in incogniton mode.

### ji...@chromium.org (2018-04-24)

[Empty comment from Monorail migration]

### ji...@chromium.org (2018-04-25)

Thanks cdsrc2016@! To answer your question. Yes, I used --incognito option in all my repros. It's probably because the safe browsing requests come back so quickly that there's a very tiny time window in which this can be reproduced on my workstation (I blame the fast network. )

I updated the CL to handle shutdown differently. Could you patch the latest patch (#3) of https://chromium-review.googlesource.com/c/chromium/src/+/1024864  and give it another try?  
I'd like to see if there's still crash. If it is how the stack trace looks like now.

Thank you so so much!




### cd...@gmail.com (2018-04-25)

Hi, @jialiul
I tested more than 20 times and no UAF or other Unexpected errors appeared again.^-^

### ji...@chromium.org (2018-04-25)

Thanks for confirming! 

### bu...@chromium.org (2018-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f6e3ee58f03d5b993a6d1d563b67993e7a0d1db2

commit f6e3ee58f03d5b993a6d1d563b67993e7a0d1db2
Author: Jialiu Lin <jialiul@chromium.org>
Date: Fri Apr 27 00:06:37 2018

Handle CheckClientDownloadRequest different when download is destroyed to avoid crash

When a download is being destroyed while a CheckClientDownloadRequest
is in-flight, we ignore the callback to CheckClientDownloadDone.
This prevents crash that caused by DownloadManagerImpl being destructed
before CheckClientDownloadDone during browser shutdown.

A new UMA enum is added to track this special case.

Bug: 830303
Change-Id: Iff5146a163e357ebd9b97b97cf48c6d7af9a7783
Reviewed-on: https://chromium-review.googlesource.com/1024864
Commit-Queue: Jialiu Lin <jialiul@chromium.org>
Reviewed-by: Varun Khaneja <vakh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#554201}
[modify] https://crrev.com/f6e3ee58f03d5b993a6d1d563b67993e7a0d1db2/chrome/browser/safe_browsing/download_protection/check_client_download_request.cc
[modify] https://crrev.com/f6e3ee58f03d5b993a6d1d563b67993e7a0d1db2/chrome/browser/safe_browsing/download_protection/check_client_download_request.h
[modify] https://crrev.com/f6e3ee58f03d5b993a6d1d563b67993e7a0d1db2/chrome/browser/safe_browsing/download_protection/download_protection_service.cc
[modify] https://crrev.com/f6e3ee58f03d5b993a6d1d563b67993e7a0d1db2/chrome/browser/safe_browsing/download_protection/download_protection_service_unittest.cc
[modify] https://crrev.com/f6e3ee58f03d5b993a6d1d563b67993e7a0d1db2/chrome/browser/safe_browsing/download_protection/download_protection_util.h
[modify] https://crrev.com/f6e3ee58f03d5b993a6d1d563b67993e7a0d1db2/tools/metrics/histograms/enums.xml


### ji...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-04)

Nice on cdsrc2016@, the Chrome VRP panel decided to award $3,000 for this report.

### aw...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

### cd...@gmail.com (2018-06-07)

Hi,is this bug can get CVE?

thank you~~~

### sh...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2018-06-08)

Removing merge request label. The code in #30 was landed in April. It should already been in 68 (branch at May 24).
Something wrong with sheriffbot@ maybe? 

### sh...@chromium.org (2018-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/830303?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091050)*
