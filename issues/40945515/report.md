# Security: Stack-buffer-underflow in DataPack::GetStringPieceFromOffset when loading a malicious theme

| Field | Value |
|-------|-------|
| **Issue ID** | [40945515](https://issues.chromium.org/issues/40945515) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Themes, UI>Browser>WebUI |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | pk...@chromium.org |
| **Created** | 2023-11-24 |
| **Bounty** | $6,000.00 |

## Description

**VULNERABILITY DETAILS**  

The DataPack::GetStringPieceFromOffset method is vulnerable to integer underflow due to the way it calculates lengths of resources (`size_t length = next_offset - target_offset;`). This makes it possible craft a malicious .pak file with intentionally incorrect offsets that can return an arbitrary memory location for any GetStringPiece call (which is also used for bitmaps and raw data). One way to deliver such a pak file is to put a read-only `Cached Theme.pak` file in a Chrome theme, which is the method used in this repro. In this specific instance I'm altering the memory location of kNtpBackground, which eventually gets passed on to `web_ui_url_loader_factory.cc` and causes a stack-buffer-underflow crash.

<https://source.chromium.org/chromium/chromium/src/+/main:ui/base/resource/data_pack.cc;l=366;drc=d4a7d3fb6f5100019d6153d5cf00c60f06b1d0a2>

I've written a fix for the issue (`data_pack_fix.patch`), but I haven't submitted it on Gerrit yet since I don't know how security fixes on Gerrit should be handled in terms of confidentiality. I'd like to commit this fix to Gerrit under my name later on if that's possible.

**VERSION**  

Chrome Version: 121.0.6129.0 Dev + Stable  

Operating System: Windows 10

**REPRODUCTION CASE**  

I know you're not a huge fan of zip files, but since one of the required files is 3GiB uncompressed I figured it would make things easier for you. I've also added the Python script I made to generate the file, should you wish to avoid the zip or play around with the parameters.

1. Download and extract `poc.zip` into a folder.
2. Load the folder as an unpacked extension in Chrome.
3. Close Chrome.
4. Reopen Chrome.

If you'd like to use the Python script instead:

1. Download `manifest.json` and `generate_pak.py` into a folder.
2. (optional) Change the `offset` variable in the Python script as desired.
3. Generate the pak file with `python3 generate_pak.py`.
4. Continue from step 2 of original repro.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==6984==ERROR: AddressSanitizer: stack-buffer-underflow on address 0x1282b2589000 at pc 0x7ff65c38e9bc bp 0x00063dbfe4d0 sp 0x00063dbfe510  

READ of size 1073741824 at 0x1282b2589000 thread T7  

==6984==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff65c38e9bb in \_\_asan\_memmove C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:71  

#1 0x7ffaaecfd9c6 in std::\_\_Cr::\_\_unwrap\_and\_dispatch<std::\_\_Cr::\_\_overload<std::\_\_Cr::\_\_copy\_loop[std::\_\_Cr::\_ClassicAlgPolicy](javascript:void(0);),std::\_\_Cr::\_\_copy\_trivial>,base::CheckedContiguousIterator<const unsigned char>,base::CheckedContiguousIterator<const unsigned char>,char \*,0> C:\b\s\w\ir\cache\builder\src\third\_party\libc++\src\include\_\_algorithm\copy\_move\_common.h:109  

#2 0x7ffaaecfd71d in base::ranges::copy<base::span<const unsigned char,18446744073709551615,const unsigned char \*>,char \*,std::\_\_Cr::random\_access\_iterator\_tag,std::\_\_Cr::random\_access\_iterator\_tag> C:\b\s\w\ir\cache\builder\src\base\ranges\algorithm.h:1244  

#3 0x7ffaaecfbd2e in content::`anonymous namespace'::ReadData C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_url_loader_factory.cc:137 #4 0x7ffaaecfcf4f in base::internal::FunctorTraits<void (\*)(mojo::StructPtr<network::mojom::URLResponseHead>, const std::__Cr::map<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::less<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,std::__Cr::allocator<std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > > > > \*, bool, scoped_refptr<content::URLDataSourceImpl>, mojo::PendingRemote<network::mojom::URLLoaderClient>, std::__Cr::optional<net::HttpByteRange>, base::ElapsedTimer, scoped_refptr<base::RefCountedMemory>)>::Invoke<void (\*)(mojo::StructPtr<network::mojom::URLResponseHead>, const std::__Cr::map<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::less<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,std::__Cr::allocator<std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > > > > \*, bool, scoped_refptr<content::URLDataSourceImpl>, mojo::PendingRemote<network::mojom::URLLoaderClient>, std::__Cr::optional<net::HttpByteRange>, base::ElapsedTimer, scoped_refptr<base::RefCountedMemory>),mojo::StructPtr<network::mojom::URLResponseHead>,const std::__Cr::map<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::less<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >, C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:630 #5 0x7ffaaecfcae4 in base::internal::Invoker<base::internal::BindState<void (\*)(mojo::StructPtr<network::mojom::URLResponseHead>, const std::__Cr::map<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::less<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,std::__Cr::allocator<std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > > > > \*, bool, scoped_refptr<content::URLDataSourceImpl>, mojo::PendingRemote<network::mojom::URLLoaderClient>, std::__Cr::optional<net::HttpByteRange>, base::ElapsedTimer, scoped_refptr<base::RefCountedMemory>),mojo::StructPtr<network::mojom::URLResponseHead>,base::internal::UnretainedWrapper<const std::__Cr::map<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::less<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > >,std::__Cr::allocator<std::__Cr::pair<const std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> >,std::__Cr::basic_string<char,std::__Cr::char_traits<char>,std::__Cr::allocator<char> > > > >,base::unretained_traits::MayNotDangle,0>,bool,scoped_refptr<content::URLDataSourceImpl>,mojo::PendingRemote<network::mojom::URLLoaderClient>,std::__Cr::optional<net::HttpByteRange>,base::ElapsedTimer,scoped_refptr<base::RefCountedMemory> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:918 #6 0x7ffab3a3571d in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:201 #7 0x7ffabb7f642e in base::internal::TaskTracker::RunSkipOnShutdown C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:629 #8 0x7ffabb7f5598 in base::internal::TaskTracker::RunTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:486 #9 0x7ffabb7f4636 in base::internal::TaskTracker::RunAndPopNextTask C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\task_tracker.cc:401 #10 0x7ffac0e36efc in base::internal::WorkerThread::RunWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:423 #11 0x7ffac0e35e0f in base::internal::WorkerThread::RunPooledWorker C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:308 #12 0x7ffab394e0e1 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:140  

#13 0x7ff65c3822b9 in asan\_thread\_start C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:147  

#14 0x7ffb251c7613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)  

#15 0x7ffb25d226b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

Address 0x1282b2589000 is located in stack of thread T30 at offset 0 in frame  

#0 0x7ffab394de0f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:105

This frame has 1 object(s):  

[32, 40) 'platform\_handle' (line 117) <== Memory access at offset 0 partially underflows this variable  

HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork  

(longjmp, SEH and C++ exceptions \*are\* supported)  

Thread T30 created by T0 here:  

#0 0x7ff65c3821e2 in CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:158  

#1 0x7ffab394ceef in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:205 #2 0x7ffac0e349dc in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:186 #3 0x7ffabb802475 in base::internal::PooledSingleThreadTaskRunnerManager::CreateCOMSTATaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\pooled_single_thread_task_runner_manager.cc:658 #4 0x7ffab73838b3 in base::internal::ThreadPoolImpl::CreateCOMSTATaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_pool_impl.cc:257 #5 0x7ffab3a0b285 in base::ThreadPool::CreateCOMSTATaskRunner C:\b\s\w\ir\cache\builder\src\base\task\thread_pool.cc:113 #6 0x7ffac4805c08 in media_router::CanFirewallUseLocalPorts C:\b\s\w\ir\cache\builder\src\chrome\browser\media\router\mojo\media_route_provider_util_win.cc:37 #7 0x7ffac0016368 in media_router::MediaRouterDesktop::Initialize C:\b\s\w\ir\cache\builder\src\chrome\browser\media\router\mojo\media_router_desktop.cc:146 #8 0x7ffabace8d44 in media_router::ChromeMediaRouterFactory::BuildServiceInstanceForBrowserContext C:\b\s\w\ir\cache\builder\src\chrome\browser\media\router\chrome_media_router_factory.cc:85 #9 0x7ffab616bd33 in RefcountedBrowserContextKeyedServiceFactory::BuildServiceInstanceFor C:\b\s\w\ir\cache\builder\src\components\keyed_service\content\refcounted_browser_context_keyed_service_factory.cc:94 #10 0x7ffab4deebea in KeyedServiceFactory::GetServiceForContext C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\keyed_service_factory.cc:93 #11 0x7ffac509ac0b in MediaRouterActionController::MediaRouterActionController C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\toolbar\media_router_action_controller.cc:25 #12 0x7ffac09f715c in media_router::MediaRouterUIService::ConfigureService C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media_router\media_router_ui_service.cc:63 #13 0x7ffac09f6e62 in media_router::MediaRouterUIService::MediaRouterUIService C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media_router\media_router_ui_service.cc:33 #14 0x7ffac09f695d in media_router::MediaRouterUIService::MediaRouterUIService C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media_router\media_router_ui_service.cc:20 #15 0x7ffabb388947 in media_router::MediaRouterUIServiceFactory::BuildServiceInstanceForBrowserContext C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\media_router\media_router_ui_service_factory.cc:51 #16 0x7ffab616bd33 in RefcountedBrowserContextKeyedServiceFactory::BuildServiceInstanceFor C:\b\s\w\ir\cache\builder\src\components\keyed_service\content\refcounted_browser_context_keyed_service_factory.cc:94 #17 0x7ffab4deebea in KeyedServiceFactory::GetServiceForContext C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\keyed_service_factory.cc:93 #18 0x7ffab8607cea in DependencyManager::CreateContextServices C:\b\s\w\ir\cache\builder\src\components\keyed_service\core\dependency_manager.cc:111 #19 0x7ffab616c300 in BrowserContextDependencyManager::DoCreateBrowserContextServices C:\b\s\w\ir\cache\builder\src\components\keyed_service\content\browser_context_dependency_manager.cc:46 #20 0x7ffab7011664 in ProfileImpl::OnLocaleReady C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:1170 #21 0x7ffab700ab72 in ProfileImpl::OnPrefsLoaded C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:1214 #22 0x7ffab70077b2 in ProfileImpl::ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:528 #23 0x7ffab70067f1 in Profile::CreateProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_impl.cc:364 #24 0x7ffab37cf586 in ProfileManager::CreateProfileHelper C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1259 #25 0x7ffab37c656a in ProfileManager::CreateAndInitializeProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1804 #26 0x7ffab37c4837 in ProfileManager::GetProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:711 #27 0x7ffabaccae47 in GetStartupProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup_browser_creator.cc:1656 #28 0x7ffab6f1022f in` anonymous namespace'::CreateInitialProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:445  

#29 0x7ffab6f0d245 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1536  

#30 0x7ffab6f0c8da in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1199  

#31 0x7ffaad42c697 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1002  

#32 0x7ffaad43395d in base::internal::Invoker<base::internal::BindState<int (content::BrowserMainLoop::\*)(),base::internal::UnretainedWrapper[content::BrowserMainLoop,base::unretained\_traits::MayNotDangle,0](javascript:void(0);) >,int ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:918  

#33 0x7ffaa4f88d79 in base::OnceCallback<int ()>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:156  

#34 0x7ffaaea34982 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup\_task\_runner.cc:42  

#35 0x7ffaad42b7e2 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:913  

#36 0x7ffaad435f5f in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:139  

#37 0x7ffaad42699d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#38 0x7ffab1fdd707 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:706  

#39 0x7ffab1fe1580 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1294  

#40 0x7ffab1fe0c49 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1138  

#41 0x7ffab1fdb843 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:334  

#42 0x7ffab1fdc4f6 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:347  

#43 0x7ffaa4ac1746 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#44 0x7ff65c2d5f72 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#45 0x7ff65c2d2a5c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:392  

#46 0x7ff65c70574b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#47 0x7ffb251c7613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)  

#48 0x7ffb25d226b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

SUMMARY: AddressSanitizer: stack-buffer-underflow C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_interceptors\_memintrinsics.cpp:71 in \_\_asan\_memmove  

Shadow bytes around the buggy address:  

0x1282b2588d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1282b2588e00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1282b2588e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1282b2588f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1282b2588f80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x1282b2589000:[f1]f1 f1 f1 00 f3 f3 f3 f5 f5 f5 f5 f5 f5 f5 f5  

0x1282b2589080: f1 f1 f1 f1 f8 f3 f3 f3 f5 f5 f5 f5 f5 f5 f5 f5  

0x1282b2589100: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x1282b2589180: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x1282b2589200: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

0x1282b2589280: f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5 f5  

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

Thread T7 created by T0 here:  

#0 0x7ff65c3821e2 in CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:158  

#1 0x7ffab394ceef in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:205 #2 0x7ffac0e349dc in base::internal::WorkerThread::Start C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\worker_thread.cc:186 #3 0x7ffabb816325 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl::<lambda_2>::operator() C:\b\s\w\ir\cache\builder\src\base\task\thread_pool\thread_group_impl.cc:182 #4 0x7ffabb815e37 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<`lambda at ....\base\task\thread\_pool\thread\_group\_impl.cc:181:37'> C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_group\_impl.cc:147  

#5 0x7ffabb8155c4 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_group\_impl.cc:181  

#6 0x7ffabb80c505 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_group\_impl.cc:103  

#7 0x7ffabb80c0ce in base::internal::ThreadGroupImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_group\_impl.cc:414  

#8 0x7ffab73822fd in base::internal::ThreadPoolImpl::Start C:\b\s\w\ir\cache\builder\src\base\task\thread\_pool\thread\_pool\_impl.cc:190  

#9 0x7ffaaea33fba in content::StartBrowserThreadPool C:\b\s\w\ir\cache\builder\src\content\browser\startup\_helper.cc:115  

#10 0x7ffab1fe1c3b in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1226  

#11 0x7ffab1fe0c49 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1138  

#12 0x7ffab1fdb843 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:334  

#13 0x7ffab1fdc4f6 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:347  

#14 0x7ffaa4ac1746 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:190  

#15 0x7ff65c2d5f72 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#16 0x7ff65c2d2a5c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:392  

#17 0x7ff65c70574b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#18 0x7ffb251c7613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)  

#19 0x7ffb25d226b0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526b0)

==6984==ADDITIONAL INFO

==6984==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7ffaaecf9f94 in content::`anonymous namespace'::DataAvailable C:\b\s\w\ir\cache\builder\src\content\browser\webui\web\_ui\_url\_loader\_factory.cc:180  

#1 0x7ffab41f3fdd in mojo::Connector::PostDispatchNextMessageFromPipe C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:581  

#2 0x7ffab4222537 in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:102

==6984==END OF ADDITIONAL INFO  

==6984==ABORTING

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Lyra Rebane (rebane2001)

## Attachments

- [demo.webm](attachments/demo.webm) (video/webm, 6.0 MB)
- [generate_pak.py](attachments/generate_pak.py) (text/plain, 2.6 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 643 B)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 3.6 MB)
- [data_pack_fix.patch](attachments/data_pack_fix.patch) (text/plain, 1.6 KB)

## Timeline

### [Deleted User] (2023-11-24)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-11-26)

> I've written a fix for the issue (`data_pack_fix.patch`), but I haven't submitted it on Gerrit yet since I don't know how security fixes on Gerrit should be handled in terms of confidentiality. I'd like to commit this fix to Gerrit under my name later on if that's possible.

You can just upload the CL directly to Gerrit. I would recommend attaching a test case as well, and cleaning up the LOG statements.

That being said, I would like to call the fix out as interesting, since the crash stack is in:

     #0 0x7ff65c38e9bb in __asan_memmove C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:71
    #1 0x7ffaaecfd9c6 in std::__Cr::__unwrap_and_dispatch<std::__Cr::__overload<std::__Cr::__copy_loop<std::__Cr::_ClassicAlgPolicy>,std::__Cr::__copy_trivial>,base::CheckedContiguousIterator<const unsigned char>,base::CheckedContiguousIterator<const unsigned char>,char *,0> C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__algorithm\copy_move_common.h:109
    #2 0x7ffaaecfd71d in base::ranges::copy<base::span<const unsigned char,18446744073709551615,const unsigned char *>,char *,std::__Cr::random_access_iterator_tag,std::__Cr::random_access_iterator_tag> C:\b\s\w\ir\cache\builder\src\base\ranges\algorithm.h:1244
    #3 0x7ffaaecfbd2e in content::`anonymous namespace'::ReadData C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_url_loader_factory.cc:137

Do we need an additional fix in WebUIURLLoaderFactory? It doesn't seem like we should have a memory safety error in the URL loader code even with a malicious theme.

Triage notes:
- I am tentatively not tagging Android, but the URL loader crash above makes me very suspicious, and we need to better understand that
- I am marking this "high" since there is (some) mitigation in that this requires an explicitly malicious theme.
- However, it is also not currently clear if such a malicious theme can be published through CWS. It might be good to determine this too...

[Monorail components: Platform>Extensions UI>Browser>WebUI]

### dc...@chromium.org (2023-11-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-26)

[Empty comment from Monorail migration]

### re...@gmail.com (2023-11-26)

I think the fix in DataPack is sufficient since the reason WebUIURLLoaderFactory crashes is that it uses a malformed base::RefCountedStaticMemory from the DataPack and as a consequnce it tries to copy from a memory range it doesn't have access to. The RefCountedMemory consists of a pointer to the data and the length of data, which are both set (and attacker-controlled) when it's initialized in DataPack::GetStaticMemory.

I believe the crash is just a symptom of the memory corruption and it could just as well show up through a different code path, and I don't think there's any way for the WebUIURLLoaderFactory to check whether the RefCountedMemory is valid, but I'm not experienced with this topic so perhaps there is something that could/should be done there as well.


### re...@gmail.com (2023-11-26)

Submitted a CL at https://crrev.com/c/5059113

### [Deleted User] (2023-11-27)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@gmail.com (2023-11-29)

Could someone with permissions cc +sky@ here as a reviewer for https://crrev.com/c/5059113?

### tj...@chromium.org (2023-11-29)

[Empty comment from Monorail migration]

### sk...@chromium.org (2023-11-30)

If this issue is specific to theme files, I'm wondering if we could do the check at the time of downloading the theme file but before using and then reject the theme entirely?

### re...@gmail.com (2023-11-30)

No, this applies to all pak files, themes are just the easiest delivery method I could think of from the perspective of an attacker. Outside of security, a single-bit corruption in a .pak file shipped with Chromium could lead to similar memory corruption and stability issues, so I think it would be good to fix the problem at the source to be on the safe side with these edge-cases as well.

### sk...@chromium.org (2023-11-30)

I believe the main concern here is security, and if theme files are the only vector for the exploit to be delivered them it seems better to address the exploit for theme files. I'm not opposed to the sanity checks, but I want to make sure the theme code is gracefully handling this.

### sk...@chromium.org (2023-11-30)

Asking here as this is security sensitive. In https://chromium-review.googlesource.com/c/chromium/src/+/5059113 what happens with a malicious .pak file in a theme? Will chrome crash?

### re...@gmail.com (2023-11-30)

A malicious pak file can create a RefCountedStaticMemory with an arbitrary attacker-chosen size up to 4GB, which has various impacts depending on which code path it ends up in.

A crash is not guaranteed. In the original I am giving a RefCountedStaticMemory with a huge size to a theme's kNtpBackground resource, which ends up in web_ui_url_loader_factory.cc and crashes. However, different sizes and other code paths can cause different outcomes and don't always crash. The behaviour depends on whatever ends up using the RefCountedStaticMemory, not the data pack or theme loading logic itself.

The root cause is this integer underflowing when the resource order is wrong: https://source.chromium.org/chromium/chromium/src/+/main:ui/base/resource/data_pack.cc;l=366;drc=d4a7d3fb6f5100019d6153d5cf00c60f06b1d0a2

### sk...@chromium.org (2023-11-30)

I think the right fix is likely a combination of what you have and the theme install logic verifying the pak file is valid.

### dc...@chromium.org (2023-11-30)

> uses a malformed base::RefCountedStaticMemory

Can you clarify what 'malformed' means here?

> If this issue is specific to theme files, I'm wondering if we could do the check at the time of downloading the theme file but before using and then reject the theme entirely?

I think the security issue is specific to themes, because that could be 3p content, which is not trustworthy. It'd be the same as a security bug in an extension API–it requires installing a malicious extension to trigger.

Triggering this issue by editing pak files directly is out of the threat model.

But of course it'd be good for pak files to be valid too.

### re...@gmail.com (2023-11-30)

> Can you clarify what 'malformed' means here?

In short, a RefCountedStaticMemory with an attacker-controlled size value up to the unsigned integer limit (beyond the pak file).

Eg if our pack file is 100 bytes and I create resources at 50 bytes and 49 bytes, the RefCountedStaticMemory of the first resource will have a size of 4294967295 (49 - 50 is -1 and the length is unsigned), which is way beyond the original 100 bytes and ends up in other memory.


### sk...@chromium.org (2023-12-01)

Again, I think we should be catching this at the time we are going to install the theme, and if it it's not valid, reject it. Does that happen with your patch rebane? I'm not sure if the theme install process calls to verify the theme packs or not.

### re...@gmail.com (2023-12-01)

My patch just prevents an invalid data pack load, so it still lets you install the theme but doesn't allow the .pak file to be loaded at all.

Catching it during theme install is a bit more interesting since themes are not actually supposed to ship with a .pak file in the first place, and the browser is supposed to generate one from the manifest file and overwrite it. I am sidestepping that here by making the pak file read-only, and from reading the code of the theme install it seems like it might also be possible to crash the browser after the install has finished but before the new pak has been written to achieve the same effect. Legitimate themes should never ship with a .pak file, and because of this I think it doesn't make sense to check whether the pak file is valid during the install.

Rejecting all theme installs with .pak files entirely however would lead to issues when developing unpacked themes because Chrome will drop its own "Cached Theme.pak" file into the theme's folder, so this would prevent a reload of the theme. I can't currently think of a good way to catch and reject this during a theme install if we also want to protect unpacked themes.


### pb...@chromium.org (2023-12-05)

->sky@ since you're already engaging/reviewing here :)

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-12-13)

Hi sky@! [security shepherd here]

Did you reach a resolution for your concerns with the proposed patch? It'd be helpful if you could share an update on this bug with your planned next steps or any blockers/what else you'd need before being able to resolve the issue.

Thanks for taking another look.

### sk...@chromium.org (2023-12-14)

I understand there is the potential for problems, what I'm unsure on is if this can actually happen.

rebane2001@gmail.com says "and the browser is supposed to generate one from the manifest file and overwrite it." Unless the browser can be tricked into writing a bogus pak file, then it seems like the attack can't happen. Perhaps I'm missing something?

I'm going to downgrade this. If I am misunderstanding, please increase the priority appropriately.

### re...@gmail.com (2023-12-14)

You can prevent the browser from overwriting the attacker's pak file, check https://crbug.com/chromium/1504936#c19. In my original repro I set the attacker's pak file to read-only inside the zip to achieve this. Try the repro if you'd like to see it in action.

### sk...@chromium.org (2023-12-14)

Thanks for the details.

It seems like the issue is more during theme install. If the browser needs to over-write a pak file, then we should ensure that actually happens. Does that make sense?

### re...@gmail.com (2023-12-14)

Yes, but this may need some work as currently the pak write gets scheduled to be written after the theme is already installed. I also believe that the underflow fix should be implemented regardless.

### sk...@chromium.org (2023-12-14)

I'm passing this to extensions, as it seems to me the core issue is how extensions is operating.

### rd...@chromium.org (2023-12-14)

This seems related to themes, not extensions.

pkasting@, mind taking a look as a themes owner?

Also bumping priority to match security severity.

### rd...@chromium.org (2023-12-14)

[Empty comment from Monorail migration]

[Monorail components: -Platform>Extensions UI>Browser>Themes]

### [Deleted User] (2023-12-14)

pkasting: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pk...@chromium.org (2023-12-15)

The theme .pak is supposed to be a cache. If loading it fails, the browser should handle gracefully and the user-visible effect should be the same as if there had been no .pak to begin with (browser attempts to overwrite with a valid .pak). If writing fails, we don't care, because the only effect is that the next startup won't gain the cache benefits it otherwise would have, and we'll try the write again.

If we implement both the above, there is neither need nor benefit to trying to detect and reject theme installs containing invalid .pak files, malicious or not.

I haven't looked yet, but I'm assuming the underflow fix will implement the above entirely, and thus should be sufficient. It's EOD for me, will look more closely at https://chromium-review.googlesource.com/c/chromium/src/+/5059113 tomorrow.

### re...@gmail.com (2023-12-15)

Yep, that's how Chrome handles .pak files currently. Once the fix is implemented, a pak file causing the underflow will just fail to load and default to the code path you described, acting as if there was never a .pak file in the first place.

### sk...@chromium.org (2023-12-15)

Correct me if I'm wrong, but it seems the issue is the theme is supplying the pak file, and chrome doesn't override the pak file. I get that detecting the theme file is bogus will fix this as well, but shouldn't we prevent themes from doing this in the first place?

### pk...@chromium.org (2023-12-15)

By "prevent" I assume you mean "refuse to install a theme that tries".
* We'd have to code this to only apply to webstore themes, not unpacked ones, which makes things more complex.
* If the author is malicious, user safety isn't improved.
* If the author isn't malicious (e.g. they accidentally left a bogus .pak in their upload), this only frustrates users to no value.

Is there an upside to trying to detect this and refuse the install?

### sk...@chromium.org (2023-12-15)

I think this depends upon how we handle a bad pak file. If we detect it *and* show a dialog, then I agree there is little value.

### pk...@chromium.org (2023-12-15)

What would the dialog say? Theme contained corrupt cached data, we'll rebuild it [OK]?

I feel like I'm fundamentally missing something.

### sk...@chromium.org (2023-12-15)

I was assuming the action would be to ignore the theme entirely if the pak isn't valid. If the action is to rebuild, then I agree with you we should just do it.

### re...@gmail.com (2023-12-15)

Yep, the current behavior is already the rebuild behavior. It just doesn't happen for this bug since the underflow check is missing and Chrome thinks the pak file is valid while it isn't. Once the CL is implemented, Chrome will see the pak as invalid and rebuild it as it's supposed to.

### sk...@chromium.org (2023-12-15)

Great, it all makes sense to me then. Sorry for the confusion.

### gi...@appspot.gserviceaccount.com (2023-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c4b2e6246ad0e95eaf0727bb25a2e4969155e989

commit c4b2e6246ad0e95eaf0727bb25a2e4969155e989
Author: Lyra Rebane <rebane2001@gmail.com>
Date: Mon Dec 18 19:53:17 2023

Verify resource order in data pack files

This CL adds a resource order check when loading a data pack or calling DataPack::GetStringPiece to make sure the resources are ordered sequentially in memory.

Bug: 1504936
Change-Id: Ie3bf1d9dbac937407355935a859a5daa9ce84350
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5059113
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Peter Boström <pbos@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1238675}

[modify] https://crrev.com/c4b2e6246ad0e95eaf0727bb25a2e4969155e989/ui/base/resource/data_pack_unittest.cc
[modify] https://crrev.com/c4b2e6246ad0e95eaf0727bb25a2e4969155e989/ui/base/resource/data_pack.cc
[modify] https://crrev.com/c4b2e6246ad0e95eaf0727bb25a2e4969155e989/ui/base/resource/data_pack_literal.h
[modify] https://crrev.com/c4b2e6246ad0e95eaf0727bb25a2e4969155e989/AUTHORS
[modify] https://crrev.com/c4b2e6246ad0e95eaf0727bb25a2e4969155e989/ui/base/resource/data_pack_literal.cc


### [Deleted User] (2023-12-30)

pkasting: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@gmail.com (2023-12-30)

The CL for the fix was merged, so I'd say it's fine to mark this as fixed from my side, unless it needs to be cherry-picked to releases or something.

### sk...@chromium.org (2024-01-02)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-02)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-02)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-02)

Requesting merge to stable M120 because latest trunk commit (1238675) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1238675) appears to be after beta branch point (1233107).

Merge review required: M120 is already shipping to stable.

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2024-01-03)

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://chromium-review.googlesource.com/c/chromium/src/+/5059113

2. Has this fix been tested on Canary?

No.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

Fix landed ~2 weeks ago and so far have not seen any issues.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

First comment describes how to repo. Note also that patch includes test coverage, which is hopefully good enough.

### am...@google.com (2024-01-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### re...@gmail.com (2024-01-03)

Thank you so much, this is awesome news to start the year with :)!

### [Deleted User] (2024-01-03)

Requesting merge to stable M120 because latest trunk commit (1238675) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1238675) appears to be after beta branch point (1233107).

Merge review required: M120 is already shipping to stable.

Merge review required: M121 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120, 121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2024-01-03)

Congratulations Lyra! As you have seen above already :) the Chrome VRP Panel has decided to award you $6,000 for this report of mitigated memory corruption in the browser process + patch bonus! Nice work on that patch and committing it. Thank you for your efforts and reporting this issue to us and again nice work on that patch! Happy New Year to you! 

### am...@chromium.org (2024-01-04)

Thanks for responding to the merge questionnaire sky@. So, I'm also not seeing any issues related to Canary, but since we are in the middle of Stable Channel 120 right now and this is somewhat mitigated by with some preconditions of getting a malicious them into the webstore and convincing a user to install the them, I'm going to suggest we strictly backmerge the fix to 121/ Beta and not Stable. 
Please let me know if there are any issues with this. 
Please merge https://crrev.com/c/5059113 to branch 6167 at your earliest convenience. 

### gi...@appspot.gserviceaccount.com (2024-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bfba41e2f9a87818f2f5b784ef45baa67a121217

commit bfba41e2f9a87818f2f5b784ef45baa67a121217
Author: Lyra Rebane <rebane2001@gmail.com>
Date: Fri Jan 05 16:19:39 2024

[M121] Verify resource order in data pack files

This CL adds a resource order check when loading a data pack or calling DataPack::GetStringPiece to make sure the resources are ordered sequentially in memory.

(cherry picked from commit c4b2e6246ad0e95eaf0727bb25a2e4969155e989)

Bug: 1504936
Change-Id: Ie3bf1d9dbac937407355935a859a5daa9ce84350
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5059113
Reviewed-by: Scott Violet <sky@chromium.org>
Commit-Queue: Peter Boström <pbos@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1238675}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5169012
Auto-Submit: Scott Violet <sky@chromium.org>
Commit-Queue: Scott Violet <sky@chromium.org>
Cr-Commit-Position: refs/branch-heads/6167@{#1059}
Cr-Branched-From: 222e786949e76e342d325ea0d008b4b6273f3a89-refs/heads/main@{#1233107}

[modify] https://crrev.com/bfba41e2f9a87818f2f5b784ef45baa67a121217/ui/base/resource/data_pack.cc
[modify] https://crrev.com/bfba41e2f9a87818f2f5b784ef45baa67a121217/ui/base/resource/data_pack_unittest.cc
[modify] https://crrev.com/bfba41e2f9a87818f2f5b784ef45baa67a121217/ui/base/resource/data_pack_literal.h
[modify] https://crrev.com/bfba41e2f9a87818f2f5b784ef45baa67a121217/AUTHORS
[modify] https://crrev.com/bfba41e2f9a87818f2f5b784ef45baa67a121217/ui/base/resource/data_pack_literal.cc


### [Deleted User] (2024-01-05)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@gmail.com (2024-01-05)

1. Was this issue a regression for the milestone it was found in?

No, it's been around for a long time.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### am...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-17)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2024-01-17)

1. https://crrev.com/c/5177426
2. Low, no conflicts
3. 121
4. Yes

### na...@google.com (2024-01-22)

Merge delayed for LTS-114 until the fix goes out in stable M-120 or M-121 whichever is first.

### pg...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-23)

This issue was migrated from crbug.com/chromium/1504936?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Themes, UI>Browser>WebUI]
[Monorail components added to Component Tags custom field.]

### na...@google.com (2024-02-07)

Approved merge for LTS-114.
Added the hotlist LTS-Merge-Approved-114

### ap...@google.com (2024-02-09)

Project: chromium/src
Branch: refs/branch-heads/5735

commit e38543b73bab9fbb04f802bb66a5178c45f5d2cb
Author: Lyra Rebane <rebane2001@gmail.com>
Date:   Fri Feb 09 20:31:56 2024

    [M114-LTS] Verify resource order in data pack files
    
    This CL adds a resource order check when loading a data pack or calling DataPack::GetStringPiece to make sure the resources are ordered sequentially in memory.
    
    (cherry picked from commit c4b2e6246ad0e95eaf0727bb25a2e4969155e989)
    
    Bug: 1504936
    Change-Id: Ie3bf1d9dbac937407355935a859a5daa9ce84350
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5059113
    Commit-Queue: Peter Boström <pbos@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1238675}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5177426
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
    Owners-Override: Victor Gabriel Savu <vsavu@google.com>
    Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
    Reviewed-by: Peter Boström <pbos@chromium.org>
    Cr-Commit-Position: refs/branch-heads/5735@{#1690}
    Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

M       AUTHORS
M       ui/base/resource/data_pack.cc
M       ui/base/resource/data_pack_literal.cc
M       ui/base/resource/data_pack_literal.h
M       ui/base/resource/data_pack_unittest.cc

https://chromium-review.googlesource.com/5177426


### pe...@google.com (2024-04-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945515)*
