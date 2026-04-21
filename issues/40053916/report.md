# Security: UAF in the views::DialogDelegate in the browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [40053916](https://issues.chromium.org/issues/40053916) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2020-11-19 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in the views::DialogDelegate in the browser process when uninstall the website app.

**VERSION**  

Chrome Version: Version 89.0.4330.0 (Developer Build) (64-bit) + dev  

gs://chromium-browser-asan/win32-release\_x64/asan-win32-release\_x64-829027.zip

Operating System: Windows 10 Pro 20H2

**REPRODUCTION CASE**  

UAF of the in the browser process

1. open <https://web.dev> in the chromium and Create shortcut(choose "Open as window")
2. close all the chromium windows
3. only open the web.dev shortcut
4. uninstall the web.dev from the settings button in the upper right corner

See the gif.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

# Asan log: C:\chromium\_version\asan-win32-release\_x64-829027>"C:\chromium\_version\asan-win32-release\_x64-829027\chrome.exe" --no-sandbox --profile-directory=Default --app-id=kopcgopmdnabocfcomipdchakloooiph [8392:5680:1118/215448.049:ERROR:ssl\_client\_socket\_impl.cc(962)] handshake failed; returned -1, SSL error code 1, net\_error -101 [8392:5680:1118/215448.092:ERROR:ssl\_client\_socket\_impl.cc(962)] handshake failed; returned -1, SSL error code 1, net\_error -101

==4992==ERROR: AddressSanitizer: heap-use-after-free on address 0x12399704a078 at pc 0x7ff9fbc13a4a bp 0x00d99a7fe6b0 sp 0x00d99a7fe6f8  

READ of size 1 at 0x12399704a078 thread T0  

#0 0x7ff9fbc13a49 in views::DialogDelegate::CancelDialog(void) C:\b\s\w\ir\cache\builder\src\ui\views\window\dialog\_delegate.cc:402:7  

#1 0x7ffa007d5095 in WebAppUninstallDialogViews::~WebAppUninstallDialogViews(void) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\web\_apps\web\_app\_uninstall\_dialog\_view.cc:214:12  

#2 0x7ffa007d6331 in WebAppUninstallDialogViews::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\web_apps\web_app_uninstall_dialog_view.cc:212:59 #3 0x7ff9effcd8e6 in std::__1::__vector_base<class std::__1::unique_ptr<class content::WebUIMessageHandler, struct std::__1::default_delete<class content::WebUIMessageHandler>>, class std::__1::allocator<class std::__1::unique_ptr<class content::WebUIMessageHandler, struct std::__1::default_delete<class content::WebUIMessageHandler>>>>::~__vector_base<class std::__1::unique_ptr<class content::WebUIMessageHandler, struct std::__1::default_delete<class content::WebUIMessageHandler>>, class std::__1::allocator<class std::__1::unique_ptr<class content::WebUIMessageHandler, struct std::__1::default_delete<class content::WebUIMessageHandler>>>>(void) C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\vector:463:9 #4 0x7ff9f2c8b703 in std::__1::unique_ptr<class web_app::WebAppDialogManager, struct std::__1::default_delete<class web_app::WebAppDialogManager>>::reset(class web_app::WebAppDialogManager \*) C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory:2633:7 #5 0x7ff9fb87ae50 in [thunk]: web_app::WebAppUiManagerImpl::`vector deleting dtor'`adjustor{8}'(unsigned int) (C:\chromium_version\asan-win32-release_x64-829027\chrome.dll+0x18b8fae50) #6 0x7ff9f5696698 in web_app::WebAppProvider::~WebAppProvider(void) C:\b\s\w\ir\cache\builder\src\chrome\browser\web_applications\web_app_provider.cc:71:33 #7 0x7ff9f5697d15 in web_app::WebAppProvider::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\web\_applications\web\_app\_provider.cc:71:33  

#8 0x7ff9f2bcd2d4 in std::\_\_1::\_\_tree<struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>, class std::\_\_1::\_\_map\_value\_compare<unsigned \_\_int64, struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>, struct std::\_\_1::less<unsigned \_\_int64>, 1>, class std::\_\_1::allocator<struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>>>::erase(class std::\_\_1::\_\_tree\_const\_iterator<struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>, class std::\_\_1::\_\_tree\_node<struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>, void \*> \*, \_*int64>) C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_*tree:2519:5  

#9 0x7ff9fa729de4 in KeyedServiceFactory::Disassociate(void \*) C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\keyed\_service\_factory.cc:97:14  

#10 0x7ff9fa72a074 in KeyedServiceFactory::ContextDestroyed(void \*) C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\keyed\_service\_factory.cc:107:3  

#11 0x7ff9fcdd5f4d in DependencyManager::PerformInterlockedTwoPhaseShutdown(class DependencyManager \*, void \*, class DependencyManager \*, void \*) C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\dependency\_manager.cc:111:3  

#12 0x7ff9fc0ebe64 in ProfileImpl::~ProfileImpl(void) C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:818:3  

#13 0x7ff9fc0f1885 in ProfileImpl::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.h:774 #14 0x7ff9fc108d46 in ProfileDestroyer::DestroyRegularProfileNow(class Profile \*const) C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:104:3 #15 0x7ff9fc10886b in ProfileDestroyer::DestroyProfileWhenAppropriate(class Profile \*const) C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_destroyer.cc:52:5 #16 0x7ff9f9a2efae in ProfileManager::ProfileInfo::~ProfileInfo(void) C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1437:3 #17 0x7ff9f9a370a9 in std::__1::unique_ptr<struct ProfileManager::ProfileInfo, struct std::__1::default_delete<struct ProfileManager::ProfileInfo>>::reset(struct ProfileManager::ProfileInfo \*) C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\memory:2633:7 #18 0x7ff9f9a345e3 in std::__1::__tree<struct std::__1::__value_type<class base::FilePath, class std::__1::unique_ptr<struct ProfileManager::ProfileInfo, struct std::__1::default_delete<struct ProfileManager::ProfileInfo>>>, class std::__1::__map_value_compare<class base::FilePath, struct std::__1::__value_type<class base::FilePath, class std::__1::unique_ptr<struct ProfileManager::ProfileInfo, struct std::__1::default_delete<struct ProfileManager::ProfileInfo>>>, struct std::__1::less<class base::FilePath>, 1>, class std::__1::allocator<struct std::__1::__value_type<class base::FilePath, class std::__1::unique_ptr<struct ProfileManager::ProfileInfo, struct std::__1::default_delete<struct ProfileManager::ProfileInfo>>>>>::destroy(class std::__1::__tree_node<struct std::__1::__value_type<class base::FilePath, class std::__1::unique_ptr<struct ProfileManager::ProfileInfo, struct std::__1::default_delete<struct ProfileManager::ProfileInfo>>>, void \*> \*) C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__tree:1833:9 #19 0x7ff9f9a37f34 in ProfileManager::~ProfileManager(void) C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:377:1 #20 0x7ff9f9a3387f in ProfileManager::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.h:375  

#21 0x7ff9feb59368 in BrowserProcessImpl::StartTearDown(void) C:\b\s\w\ir\cache\builder\src\chrome\browser\browser\_process\_impl.cc:432:22  

#22 0x7ff9fbec01db in ChromeBrowserMainParts::PostMainMessageLoopRun(void) C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1750:21  

#23 0x7ff9f36a67cb in content::BrowserMainLoop::ShutdownThreadsAndCleanUp(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1057:13  

#24 0x7ff9f36abff8 in content::BrowserMainRunnerImpl::Shutdown(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:178:17  

#25 0x7ff9f369e6f0 in content::BrowserMain(struct content::MainFunctionParams const &) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49:16  

#26 0x7ff9f9426761 in content::RunBrowserProcessMain(struct content::MainFunctionParams const &, class content::ContentMainDelegate \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:520:10  

#27 0x7ff9f9428f87 in content::ContentMainRunnerImpl::RunServiceManager(struct content::MainFunctionParams &, bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1007:10  

#28 0x7ff9f942832f in content::ContentMainRunnerImpl::Run(bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:882:12  

#29 0x7ff9f9425157 in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372:36  

#30 0x7ff9f942572b in content::ContentMain(struct content::ContentMainParams const &) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398:10  

#31 0x7ff9eff8145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:130:12  

#32 0x7ff746a85bbf in MainDllLoader::Launch(struct HINSTANCE**\*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169:12  

#33 0x7ff746a829b7 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:345:20  

#34 0x7ff746e56d7f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#35 0x7ffa4ded7033 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#36 0x7ffa4edbcec0 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18004cec0)

0x12399704a078 is located 504 bytes inside of 1328-byte region [0x123997049e80,0x12399704a3b0)  

freed by thread T0 here:  

#0 0x7ff746b241ab in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffa007d61c7 in WebAppUninstallDialogDelegateView::`scalar deleting dtor'(unsigned int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\web\_apps\web\_app\_uninstall\_dialog\_view.cc:120:73  

#2 0x7ff9fbc17755 in views::WidgetDelegate::DeleteDelegate(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget\_delegate.cc:223:5  

#3 0x7ff9f955b173 in views::Widget::OnNativeWidgetDestroyed(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1172:21  

#4 0x7ffa0268c5b6 in views::DesktopNativeWidgetAura::OnHostClosed(void) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc:342:28  

#5 0x7ffa0266ad36 in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned \_\_int64, **int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1029:18  

#6 0x7ff9fc4153b2 in gfx::WindowImpl::WndProc(struct HWND**\*, unsigned int, unsigned \_\_int64, **int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:308:18  

#7 0x7ff9fc413ec3 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND**\*, unsigned int, unsigned \_\_int64, **int64)>(struct HWND**\*, unsigned int, unsigned \_\_int64, \_\_int64) C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74:10  

#8 0x7ffa4e71e857 (C:\WINDOWS\System32\user32.dll+0x18000e857)  

#9 0x7ffa4e71e3db (C:\WINDOWS\System32\user32.dll+0x18000e3db)  

#10 0x7ffa4e736a37 (C:\WINDOWS\System32\user32.dll+0x180026a37)  

#11 0x7ffa4ee0fbd3 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18009fbd3)  

#12 0x7ffa4c8c2383 (C:\WINDOWS\System32\win32u.dll+0x180002383)  

#13 0x7ff9f96b238f in base::TaskAnnotator::RunTask(char const \*, struct base::PendingTask \*) C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:163:33  

#14 0x7ff9fbd7fd89 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \*) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351:25  

#15 0x7ff9fbd7f369 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:264:36  

#16 0x7ff9f9760e60 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:224:63  

#17 0x7ff9f975e9ca in base::MessagePumpWin::Run(class base::MessagePump::Delegate \*) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:80:3  

#18 0x7ff9fbd8224f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:460:12  

#19 0x7ff9f9666cc5 in base::RunLoop::Run(void) C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:124:14  

#20 0x7ff9fbebfc01 in ChromeBrowserMainParts::MainMessageLoopRun(int \*) C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1710:15  

#21 0x7ff9f36a6063 in content::BrowserMainLoop::RunMainMessageLoopParts(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1019:29  

#22 0x7ff9f36abe53 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:150:15  

#23 0x7ff9f369e6aa in content::BrowserMain(struct content::MainFunctionParams const &) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:47:28  

#24 0x7ff9f9426761 in content::RunBrowserProcessMain(struct content::MainFunctionParams const &, class content::ContentMainDelegate \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:520:10  

#25 0x7ff9f9428f87 in content::ContentMainRunnerImpl::RunServiceManager(struct content::MainFunctionParams &, bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1007:10  

#26 0x7ff9f942832f in content::ContentMainRunnerImpl::Run(bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:882:12  

#27 0x7ff9f9425157 in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372:36  

#28 0x7ff9f942572b in content::ContentMain(struct content::ContentMainParams const &) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398:10

previously allocated by thread T0 here:  

#0 0x7ff746b242ab in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffa0ae0278a in operator new(unsigned \_\_int64) d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffa007d5b1a in WebAppUninstallDialogViews::OnIconsRead(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\web\_apps\web\_app\_uninstall\_dialog\_view.cc:256:11  

#3 0x7ffa007d696f in base::internal::FunctorTraits<void (\_\_cdecl WebAppUninstallDialogViews::\*)(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>), void>::Invoke<void (\_\_cdecl WebAppUninstallDialogViews::\*)(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>), class base::WeakPtr<class WebAppUninstallDialogViews>, class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>>(void (\_\_cdecl WebAppUninstallDialogViews::\*)(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>), class base::WeakPtr<class WebAppUninstallDialogViews> &&, class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>> &&) C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:498:12  

#4 0x7ffa007d66da in base::internal::Invoker<struct base::internal::BindState<void (\_\_cdecl WebAppUninstallDialogViews::\*)(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>), class base::WeakPtr<class WebAppUninstallDialogViews>>, (class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>)>::RunOnce(class base::internal::BindStateBase \*, class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>> &&) C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:679:12  

#5 0x7ff9f56673ea in base::OnceCallback<(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>)>::Run(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>) && C:\b\s\w\ir\cache\builder\src\base\callback.h:101:12  

#6 0x7ff9f566b261 in base::internal::ReplyAdapter<class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>, class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>>(class base::OnceCallback<(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>)>, class std::\_\_1::unique\_ptr<class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>, struct std::\_\_1::default\_delete<class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>>> \*) C:\b\s\w\ir\cache\builder\src\base\post\_task\_and\_reply\_with\_result\_internal.h:30:23  

#7 0x7ff9f566b634 in base::internal::Invoker<struct base::internal::BindState<void (\_\_cdecl \*)(class base::OnceCallback<(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>)>, class std::\_\_1::unique\_ptr<class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>, struct std::\_\_1::default\_delete<class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>>> \*), class base::OnceCallback<void \_\_cdecl(class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>)>, class base::internal::OwnedWrapper<class std::\_\_1::unique\_ptr<class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>, struct std::\_\_1::default\_delete<class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>>>, struct std::\_\_1::default\_delete<class std::\_\_1::unique\_ptr<class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::\_\_1::pair<int const, class SkBitmap>>>, struct std::\_\_1::default\_delete<class std::\_\_1::map<int, class SkBitmap, struct std::\_\_1::less<int>, class std::\_\_1::allocator<struct std::**1::pair<int const, class SkBitmap>>>>>>>>, (void)>::RunOnce(class base::internal::BindStateBase \*) C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:679:12  

#8 0x7ff9fbd715cb in base::`anonymous namespace'::PostTaskAndReplyRelay::RunReply C:\b\s\w\ir\cache\builder\src\base\threading\post\_task\_and\_reply\_impl.cc:115:29  

#9 0x7ff9fbd71823 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:679:12  

#10 0x7ff9f96b238f in base::TaskAnnotator::RunTask(char const \*, struct base::PendingTask \*) C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:163:33  

#11 0x7ff9fbd7fd89 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \*) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351:25  

#12 0x7ff9fbd7f369 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:264:36  

#13 0x7ff9f9760e60 in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:224:63  

#14 0x7ff9f975e9ca in base::MessagePumpWin::Run(class base::MessagePump::Delegate \*) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:80:3  

#15 0x7ff9fbd8224f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:460:12  

#16 0x7ff9f9666cc5 in base::RunLoop::Run(void) C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:124:14  

#17 0x7ff9fbebfc01 in ChromeBrowserMainParts::MainMessageLoopRun(int \*) C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1710:15  

#18 0x7ff9f36a6063 in content::BrowserMainLoop::RunMainMessageLoopParts(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1019:29  

#19 0x7ff9f36abe53 in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:150:15  

#20 0x7ff9f369e6aa in content::BrowserMain(struct content::MainFunctionParams const &) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:47:28  

#21 0x7ff9f9426761 in content::RunBrowserProcessMain(struct content::MainFunctionParams const &, class content::ContentMainDelegate \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:520:10  

#22 0x7ff9f9428f87 in content::ContentMainRunnerImpl::RunServiceManager(struct content::MainFunctionParams &, bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1007:10  

#23 0x7ff9f942832f in content::ContentMainRunnerImpl::Run(bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:882:12  

#24 0x7ff9f9425157 in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372:36  

#25 0x7ff9f942572b in content::ContentMain(struct content::ContentMainParams const &) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398:10  

#26 0x7ff9eff8145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:130:12  

#27 0x7ff746a85bbf in MainDllLoader::Launch(struct HINSTANCE**\*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169:12  

#28 0x7ff746a829b7 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:345:20

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\ui\views\window\dialog\_delegate.cc:402:7 in views::DialogDelegate::CancelDialog(void)  

Shadow bytes around the buggy address:  

0x044cc9d893b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x044cc9d893c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x044cc9d893d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x044cc9d893e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x044cc9d893f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x044cc9d89400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]  

0x044cc9d89410: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x044cc9d89420: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x044cc9d89430: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x044cc9d89440: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x044cc9d89450: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

Shadow gap: cc  

==4992==ABORTING

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 24.2 KB)
- [app_uninstall_uaf.gif](attachments/app_uninstall_uaf.gif) (image/gif, 6.0 MB)

## Timeline

### [Deleted User] (2020-11-19)

[Empty comment from Monorail migration]

### mb...@chromium.org (2020-11-19)

[Empty comment from Monorail migration]

[Monorail components: Platform>Apps]

### [Deleted User] (2020-11-21)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-11-22)

[Empty comment from Monorail migration]

### be...@chromium.org (2020-11-30)

Updating component and removing assignee to get it into the right triage queue. Also +cc some people so they can see it.

[Monorail components: -Platform>Apps UI>Browser>WebAppInstalls]

### dm...@chromium.org (2020-12-02)

Investigating now

### dm...@chromium.org (2020-12-02)

[Empty comment from Monorail migration]

### dm...@chromium.org (2020-12-02)

Patch here:
https://chromium-review.googlesource.com/c/chromium/src/+/2568934
cc-ing parties who might be interested.

Root cause is that the *View is being destroyed in between the 'Uninstall' call to the WebAppProvider system, and the destruction of the *Views object. The view_ pointer wasn't cleared, so the *Views object tries to call into the *View. hence, UAF.

This can only be triggered if there is only a WebApp window open (no other browser window), and the user triggers uninstall using the 3-dot menu.

### [Deleted User] (2020-12-02)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2c0cc942e1af71ba87e5e2964c04f8d8c55902d7

commit 2c0cc942e1af71ba87e5e2964c04f8d8c55902d7
Author: Daniel Murphy <dmurph@chromium.org>
Date: Wed Dec 02 20:44:04 2020

[dPWA] Clean up raw pointers during uninstallation flow.

This change cleans up how the WebAppUninstallDialogView triggers the
uninstallation callback from the parent WebAppUninstallDialogViews.
This also explicitly clears some raw pointers to prevent possible use
after free if the View is destroyed before the Views object.


        repro to ensure the issue is fixed.

Tested: Automated test is confirmed to catch bug, and manually tested
Bug: 1150798
Change-Id: I7acbc5dd172ff120214af23c0a5050956a3fbcd8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2568934
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Chase Phillips <cmp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#832949}

[modify] https://crrev.com/2c0cc942e1af71ba87e5e2964c04f8d8c55902d7/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_browsertest.cc
[modify] https://crrev.com/2c0cc942e1af71ba87e5e2964c04f8d8c55902d7/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_view.cc
[modify] https://crrev.com/2c0cc942e1af71ba87e5e2964c04f8d8c55902d7/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_view.h


### dm...@chromium.org (2020-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-03)

This bug requires manual review: M88's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2020-12-04)

1 - yes
2. - https://chromium-review.googlesource.com/c/chromium/src/+/2568934
3. Yes
4. No
5. Security bug
6. No
7. N/A


### sr...@google.com (2020-12-04)

Merge approved for M88 branch:4324 please merge asap

### [Deleted User] (2020-12-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-12-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-10)

Congratulations, the VRP panel has decided to award $5000 for this bug.

### ad...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a44338bf546209196a9ba470a198354e21c35bc2

commit a44338bf546209196a9ba470a198354e21c35bc2
Author: Daniel Murphy <dmurph@chromium.org>
Date: Fri Dec 11 18:25:48 2020

[dPWA] Clean up raw pointers during uninstallation flow.

This change cleans up how the WebAppUninstallDialogView triggers the
uninstallation callback from the parent WebAppUninstallDialogViews.
This also explicitly clears some raw pointers to prevent possible use
after free if the View is destroyed before the Views object.

        repro to ensure the issue is fixed.
(cherry picked from commit 2c0cc942e1af71ba87e5e2964c04f8d8c55902d7)

Tested: Automated test is confirmed to catch bug, and manually Tested
Bug: 1150798
Change-Id: I7acbc5dd172ff120214af23c0a5050956a3fbcd8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2568934
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Chase Phillips <cmp@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#832949}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587389
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/4234@{#4}
Cr-Branched-From: 3ddb9b702f08b29e1b37b21ea53c674698dba25b-refs/heads/master@{#798298}

[modify] https://crrev.com/a44338bf546209196a9ba470a198354e21c35bc2/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_browsertest.cc
[modify] https://crrev.com/a44338bf546209196a9ba470a198354e21c35bc2/chrome/browser/ui/views/web_apps/web_app_uninstall_dialog_view.cc


### sr...@google.com (2020-12-14)

Please help complete the merges before end of day Monday dec 14, (PST). The final beta release candidate will be cut during tuesday Dec 15 and I would like to include all these merges in. This will be the last beta release for this year ( no releases for 2 weeks)

### sr...@google.com (2020-12-14)

Removing merge-approved label per https://crbug.com/chromium/1150798#c24

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1150798?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053916)*
