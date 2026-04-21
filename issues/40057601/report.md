# Security: heap-use-after-free in ForceSigninVerifier::SendRequestIfNetworkAvailable

| Field | Value |
|-------|-------|
| **Issue ID** | [40057601](https://issues.chromium.org/issues/40057601) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | yu...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2021-10-14 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is a similar problem to <https://crbug.com/chromium/1238268>.  

The root cause is NetworkConnectionTracker continue recevie Mojo calls after all keyed services destroied and run callback functions related to freed object without weakptr.

1. When ChromeSigninClient::VerifySyncToken called, an ForceSigninVerifier instance create as |force\_signin\_verifier\_|.  
   
   <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/signin/chrome_signin_client.cc;drc=e5a38eddbdf45d7563a00d019debd11b803af1bb;l=282>  
   
   void ChromeSigninClient::VerifySyncToken() {  
   
   #if !defined(OS\_ANDROID) && !BUILDFLAG(IS\_CHROMEOS\_ASH)  
   
   // We only verifiy the token once when Profile is just created.  
   
   if (signin\_util::IsForceSigninEnabled() && !force\_signin\_verifier\_)  
   
   force\_signin\_verifier\_ = std::make\_unique<ForceSigninVerifier>( <= ForceSigninVerifier instance create  
   
   profile\_, IdentityManagerFactory::GetForProfile(profile\_));  
   
   #endif  
   
   }
2. A callback will be created and put in |NetworkConnectionTracker::connection\_type\_callbacks\_| when ForceSigninVerifier init.  
   
   <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/signin/force_signin_verifier.cc;drc=2d4200591db661a81a1d878cfd278b061c7bc8a1;l=54>  
   
   ForceSigninVerifier::ForceSigninVerifier(  
   
   Profile\* profile,  
   
   signin::IdentityManager\* identity\_manager)  
   
   ...  
   
   SendRequest(); <= call SendRequest  
   
   }  
   
   ...  
   
   void ForceSigninVerifier::SendRequest() {  
   
   auto type = network::mojom::ConnectionType::CONNECTION\_NONE;  
   
   if (content::GetNetworkConnectionTracker()->GetConnectionType(  
   
   &type,  
   
   base::BindOnce(&ForceSigninVerifier::SendRequestIfNetworkAvailable,  
   
   base::Unretained(this)))) { <= not a weakptr  
   
   SendRequestIfNetworkAvailable(type);  
   
   }  
   
   }  
   
   <https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/network_connection_tracker.cc;drc=3d7d70920a92c08f6a16597f9f44bb28ac98d9a4;l=83>  
   
   bool NetworkConnectionTracker::GetConnectionType(  
   
   network::mojom::ConnectionType\* type,  
   
   ConnectionTypeCallback callback) {  
   
   ...  
   
   if (!task\_runner\_->RunsTasksInCurrentSequence()) {  
   
   connection\_type\_callbacks\_.push\_back(base::BindOnce(  
   
   &OnGetConnectionType, base::SequencedTaskRunnerHandle::Get(),  
   
   std::move(callback)));  
   
   } else {  
   
   connection\_type\_callbacks\_.push\_back(std::move(callback)); <= callback function store here  
   
   }  
   
   return false;  
   
   }
3. When ChromeSigninClient destroied as a keyed service (eg. close Chrome), ForceSigninVerifier instance |force\_signin\_verifier\_| will be freed too.  
   
   FREE callstack:  
   
   [~ForceSigninVerifier will be called here]  
   
   chrome.dll!ChromeSigninClient::~ChromeSigninClient() Line 124  
   
   chrome.dll!ChromeSigninClient::~ChromeSigninClient() Line 122  
   
   keyed\_service\_core.dll!std::\_\_1::default\_delete<KeyedService>::operator()(KeyedService \* \_\_ptr) Line 55  
   
   keyed\_service\_core.dll!std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>::reset(KeyedService \* \_\_p) Line 316  
   
   keyed\_service\_core.dll!std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>::~unique\_ptr() Line 269  
   
   keyed\_service\_core.dll!std::\_\_1::pair<void \*const,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>::~pair() Line 394  
   
   keyed\_service\_core.dll!std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>,void \*>>>::destroy<std::\_\_1::pair<void \*const,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>,void,void>(std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>,void \*>> &, std::\_\_1::pair<void \*const,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>> \* \_\_p) Line 320  
   
   keyed\_service\_core.dll!std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>,std::\_\_1::\_\_map\_value\_compare<void \*,std::\_\_1::\_\_value\_type<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>,std::\_\_1::less<void \*>,1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>>>::erase(std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>,std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>,void \*> \*,long long> \_\_p) Line 2424  
   
   keyed\_service\_core.dll!std::\_\_1::map<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>,std::\_\_1::less<void \*>,std::\_\_1::allocator<std::\_\_1::pair<void \*const,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>>>::erase(std::\_\_1::\_\_map\_iterator<std::\_\_1::\_\_tree\_iterator<std::\_\_1::\_\_value\_type<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>,std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService>>>,void \*> \*,long long>> \_\_p) Line 1314  
   
   keyed\_service\_core.dll!KeyedServiceFactory::Disassociate(void \* context) Line 98  
   
   keyed\_service\_core.dll!KeyedServiceFactory::ContextDestroyed(void \* context) Line 107  
   
   keyed\_service\_content.dll!BrowserContextKeyedServiceFactory::BrowserContextDestroyed(content::BrowserContext \* context) Line 87  
   
   keyed\_service\_content.dll!BrowserContextKeyedServiceFactory::ContextDestroyed(void \* context) Line 118  
   
   keyed\_service\_core.dll!DependencyManager::DestroyFactoriesInOrder(void \* context, std::\_\_1::vector<DependencyNode \*,std::\_\_1::allocator<DependencyNode \*>> & order) Line 151  
   
   keyed\_service\_core.dll!DependencyManager::PerformInterlockedTwoPhaseShutdown(DependencyManager \* dependency\_manager1, void \* context1, DependencyManager \* dependency\_manager2, void \* context2) Line 128  
   
   chrome.dll!ProfileImpl::~ProfileImpl() Line 913  
   
   chrome.dll!ProfileImpl::~ProfileImpl() Line 856  
   
   chrome.dll!ProfileDestroyer::DestroyOriginalProfileNow(Profile \* const profile) Line 138  
   
   chrome.dll!ProfileDestroyer::DestroyProfileWhenAppropriate(Profile \* const profile) Line 61  
   
   chrome.dll!ProfileManager::ProfileInfo::~ProfileInfo() Line 1627  
   
   chrome.dll!std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)::operator()(ProfileManager::ProfileInfo \* \_\_ptr) Line 54  
   
   chrome.dll!std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>::reset(ProfileManager::ProfileInfo \* \_\_p) Line 316  
   
   chrome.dll!std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>::~unique\_ptr() Line 269  
   
   chrome.dll!std::\_\_1::pair<const base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>::~~pair() Line 394  
   
   chrome.dll!std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,void \*>>>::destroy<std::\_\_1::pair<const base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,void,void>(std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,void \*>> &, std::\_\_1::pair<const base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>> \* \_\_p) Line 320  
   
   chrome.dll!std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>>>::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,void \*> \* \_\_nd) Line 1802  
   
   chrome.dll!std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>>>::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,void \*> \* \_\_nd) Line 1798  
   
   chrome.dll!std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>>>::~~\_\_tree() Line 1790  
   
   chrome.dll!std::\_\_1::map<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>,std::\_\_1::less[base::FilePath](javascript:void(0);),std::\_\_1::allocator<std::\_\_1::pair<const base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>>>::~map() Line 1103  
   
   chrome.dll!ProfileManager::~ProfileManager() Line 532  
   
   chrome.dll!ProfileManager::~ProfileManager() Line 508  
   
   chrome.dll!std::\_\_1::default\_delete<ProfileManager>::operator()(ProfileManager \* \_\_ptr) Line 55  
   
   chrome.dll!std::**1::unique\_ptr<ProfileManager,std::1::default\_delete<ProfileManager>>::reset(ProfileManager \* p) Line 316  
   
   chrome.dll!BrowserProcessImpl::StartTearDown() Line 446  
   
   chrome.dll!ChromeBrowserMainParts::PostMainMessageLoopRun() Line 1850  
   
   chrome.dll!ChromeBrowserMainPartsWin::PostMainMessageLoopRun() Line 625  
   
   content.dll!content::BrowserMainLoop::ShutdownThreadsAndCleanUp() Line 1029  
   
   content.dll!content::BrowserMainRunnerImpl::Shutdown() Line 181  
   
   content.dll!content::BrowserMain(const content::MainFunctionParams & parameters) Line 53  
   
   content.dll!content::RunBrowserProcessMain(const content::MainFunctionParams & main\_function\_params, content::ContentMainDelegate \* delegate) Line 620  
   
   content.dll!content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams & main\_params, bool start\_minimal\_browser) Line 1116  
   
   content.dll!content::ContentMainRunnerImpl::Run(bool start\_minimal\_browser) Line 983  
   
   content.dll!content::RunContentProcess(const content::ContentMainParams & params, content::ContentMainRunner \* content\_main\_runner) Line 390  
   
   content.dll!content::ContentMain(const content::ContentMainParams & params) Line 418  
   
   chrome.dll!ChromeMain(HINSTANCE \* instance, sandbox::SandboxInterfaceInfo \* sandbox\_info, int64 exe\_entry\_point\_ticks, base::PrefetchResultCode prefetch\_result\_code) Line 172  
   
   chrome.exe!MainDllLoader::Launch(HINSTANCE \* instance, base::TimeTicks exe\_entry\_point\_ticks) Line 169  
   
   chrome.exe!wWinMain(HINSTANCE \* instance, HINSTANCE** \* prev, wchar\_t \*, int) Line 382  
   
   [External Code]
4. NetworkConnectionTracker continue receiveing Mojo calls and run callbacks in |connection\_type\_callbacks\_|. The callback SendRequestIfNetworkAvailable related to freed ForceSigninVerifier instance will trigger UAF.  
   
   <https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/network_connection_tracker.cc;drc=3d7d70920a92c08f6a16597f9f44bb28ac98d9a4;l=149>  
   
   void NetworkConnectionTracker::OnInitialConnectionType(  
   
   network::mojom::ConnectionType type) {  
   
   base::AutoLock lock(lock\_);  
   
   base::subtle::NoBarrier\_Store(&connection\_type\_,  
   
   static\_cast[base::subtle::Atomic32](javascript:void(0);)(type));  
   
   while (!connection\_type\_callbacks\_.empty()) {  
   
   std::move(connection\_type\_callbacks\_.front()).Run(type); <= all allbacks run here  
   
   connection\_type\_callbacks\_.pop\_front();  
   
   }  
   
   }  
   
   <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/signin/force_signin_verifier.cc;drc=7f7c846b9c2d2a8faa731c9182530cc3bf8585ee;l=136>  
   
   void ForceSigninVerifier::SendRequestIfNetworkAvailable(  
   
   network::mojom::ConnectionType network\_type) {  
   
   ...  
   
   access\_token\_fetcher\_ = <= uaf triggered because of write to a freed object  
   
   std::make\_unique[signin::PrimaryAccountAccessTokenFetcher](javascript:void(0);)(  
   
   "force\_signin\_verifier", identity\_manager\_, oauth2\_scopes,  
   
   base::BindOnce(&ForceSigninVerifier::OnAccessTokenFetchComplete,  
   
   base::Unretained(this)),  
   
   signin::PrimaryAccountAccessTokenFetcher::Mode::kImmediate);  
   
   }

REUSE callstrack by Mojo call:  

[callback ForceSigninVerifier::SendRequestIfNetworkAvailable will be called here and trigger use-after-free]  

#1 0x7ffabbd73400 in network::NetworkConnectionTracker::OnInitialConnectionType C:\b\s\w\ir\cache\builder\src\services\network\public\cpp\network\_connection\_tracker.cc:150  

#2 0x7ffab233f815 in network::mojom::NetworkChangeManagerClientStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\services\network\public\mojom\network\_change\_manager.mojom.cc:164  

#3 0x7ffabb1310d9 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:898  

#4 0x7ffabd8db1b6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#5 0x7ffabb134964 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:655  

#6 0x7ffabb148dc9 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1099  

#7 0x7ffabb147b5b in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:719  

#8 0x7ffabd8db1b6 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#9 0x7ffabb12be9a in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:546  

#10 0x7ffabb12d6e7 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:604  

#11 0x7ffabb17d646 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#12 0x7ffabade560a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#13 0x7ffabd798e62 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360  

#14 0x7ffabd7984c2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260  

#15 0x7ffabae8d046 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#16 0x7ffabae8b298 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#17 0x7ffabd79a35e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467  

#18 0x7ffabad67973 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#19 0x7ffab43414a3 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:987  

#20 0x7ffab434681d in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#21 0x7ffab433ab1a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#22 0x7ffab6bb1024 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:608  

#23 0x7ffab6bb38c0 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1104  

#24 0x7ffab6bb2aa7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:971  

#25 0x7ffab6baf52a in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:390  

#26 0x7ffab6bb056c in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:418  

#27 0x7ffab05a145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:168  

#28 0x7ff69fee5b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#29 0x7ff69fee2be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#30 0x7ff6a02d132f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#31 0x7ffb3ae17033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#32 0x7ffb3ba22650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

Use weakptr bind callback function in ForceSigninVerifier::SendRequest will fix this.

**VERSION**  

Chrome Version: stable  

Operating System: except Android and ChromeOS

**REPRODUCTION CASE**  

I found this one by cause analysis of another <https://crbug.com/chromium/1238268> I submitted earlier. It need user signin and hard to trigger because lack of Google API Token in source code build version.  

If needed, I will try to make a patch based PoC.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

Reporter credit: Wei Yuan of MoyunSec VLab

## Timeline

### [Deleted User] (2021-10-14)

[Empty comment from Monorail migration]

### bd...@chromium.org (2021-10-14)

Hi David, can you take a look at this?

@yuanvi.cn if you can provide a POC that'd be great or some repro steps

[Monorail components: Services>SignIn]

### [Deleted User] (2021-10-14)

[Empty comment from Monorail migration]

### yu...@gmail.com (2021-10-15)

According to the source code logic, maybe repro this needs following steps:

1. Sign in a user and turn on data sync (I am not sure if this can trigger ChromeSigninClient::VerifySyncToken call and need pass IsForceSigninEnabled() check)
2. Turn off network connection and reopen chrome (ForceSigninVerifier will post SendRequestIfNetworkAvailable callback in NetworkConnectionTracker)
3. close Chrome (free keyed service ChromeSigninClient and ForceSigninVerifier) and turn on network connection (trigger NetworkConnectionTracker::OnInitialConnectionType and run callbacks)
4. uaf will trigger in ForceSigninVerifier::SendRequestIfNetworkAvailable 

In step 3, it needs the actions happened exactly,  maybe you can patch the source code to stable repro it.
Also NetworkConnectionTracker::OnInitialConnectionType can be trigger by Mojo call. It can simplify step 2 and 3.

This is my simple analysis, for your reference.

### dr...@chromium.org (2021-10-15)

Thank you for the very detailed report, I don't think we need a repro case in order to fix it. The repro case would only help in assessing the severity of the bug (e.g. if there is a reliable way to repro this manually), but I don't know if this really matters as we can fix it anyway regardless of the severity.

By looking at the code, it's very clear that  ForceSigninVerifier::SendRequest() should not use base::Unretained(), and use a weak pointer instead.


### dr...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-10-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/79772972a0d41572db52073e310711b5b2cac23f

commit 79772972a0d41572db52073e310711b5b2cac23f
Author: David Roger <droger@chromium.org>
Date: Fri Oct 15 17:02:37 2021

Fix Use-After-Free in ForceSigninVerifier

See https://crbug.com/1259864 for details about the crash.

Fixed: 1259864
Change-Id: Ibb959201e948e11c752b95b5e1d0a1e9396f2248
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3226161
Commit-Queue: David Roger <droger@chromium.org>
Reviewed-by: Sylvain Defresne <sdefresne@chromium.org>
Cr-Commit-Position: refs/heads/main@{#932072}

[modify] https://crrev.com/79772972a0d41572db52073e310711b5b2cac23f/chrome/browser/signin/force_signin_verifier.cc
[modify] https://crrev.com/79772972a0d41572db52073e310711b5b2cac23f/chrome/browser/signin/force_signin_verifier_unittest.cc


### [Deleted User] (2021-10-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-15)

Requesting merge to stable M94 because latest trunk commit (932072) appears to be after stable branch point (911515).

Requesting merge to beta M95 because latest trunk commit (932072) appears to be after beta branch point (920003).

Requesting merge to dev M96 because latest trunk commit (932072) appears to be after dev branch point (929512).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-16)

Merge approved: your change passed merge requirements and is auto-approved for M96. Please go ahead and merge the CL to branch 4664 (refs/branch-heads/4664) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-16)

Merge review required: M95 has already been cut for stable release.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-16)

Merge review required: M94 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2021-10-18)

1. This is a security fix (crash fix). However, please note that:
  - this is not a regression, the bug existed since 2018
  - this is a crash on exit, depending on specific policy being set (BrowserSignin=2), which limits the severity
  - the fix is very simple and the cherry pick is not risky
2. https://crrev.com/c/3226161
3. No, we don't have any manual repro for the crash.
4. No.
5. N/A
6. No, there are no known manual repro steps

### gi...@appspot.gserviceaccount.com (2021-10-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9f9874f3fdb261ab56899ac68fb9e9caa858c250

commit 9f9874f3fdb261ab56899ac68fb9e9caa858c250
Author: David Roger <droger@chromium.org>
Date: Mon Oct 18 10:06:54 2021

Fix Use-After-Free in ForceSigninVerifier

See https://crbug.com/1259864 for details about the crash.

(cherry picked from commit 79772972a0d41572db52073e310711b5b2cac23f)

Fixed: 1259864
Change-Id: Ibb959201e948e11c752b95b5e1d0a1e9396f2248
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3226161
Commit-Queue: David Roger <droger@chromium.org>
Reviewed-by: Sylvain Defresne <sdefresne@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#932072}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3229263
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: David Roger <droger@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4664@{#169}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/9f9874f3fdb261ab56899ac68fb9e9caa858c250/chrome/browser/signin/force_signin_verifier.cc
[modify] https://crrev.com/9f9874f3fdb261ab56899ac68fb9e9caa858c250/chrome/browser/signin/force_signin_verifier_unittest.cc


### am...@chromium.org (2021-10-19)

approved for merge to M95 and M94, please merge to branches 4638 and 4606 respectively; these fixes will be included in the first respins for stable and extended stable channels. Thanks!

### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thanks for this report and nice work! 

### gi...@appspot.gserviceaccount.com (2021-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2dc6b4aa93063bd0c3283e605b59a26f60b13a01

commit 2dc6b4aa93063bd0c3283e605b59a26f60b13a01
Author: David Roger <droger@chromium.org>
Date: Wed Oct 20 23:36:54 2021

Fix Use-After-Free in ForceSigninVerifier

See https://crbug.com/1259864 for details about the crash.

(cherry picked from commit 79772972a0d41572db52073e310711b5b2cac23f)

Fixed: 1259864
Change-Id: Ibb959201e948e11c752b95b5e1d0a1e9396f2248
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3226161
Commit-Queue: David Roger <droger@chromium.org>
Reviewed-by: Sylvain Defresne <sdefresne@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#932072}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3234960
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: David Roger <droger@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4606@{#1387}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/2dc6b4aa93063bd0c3283e605b59a26f60b13a01/chrome/browser/signin/force_signin_verifier.cc
[modify] https://crrev.com/2dc6b4aa93063bd0c3283e605b59a26f60b13a01/chrome/browser/signin/force_signin_verifier_unittest.cc


### gi...@appspot.gserviceaccount.com (2021-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4dc66405bae74b709ce69d507aa2fb062b7e7d57

commit 4dc66405bae74b709ce69d507aa2fb062b7e7d57
Author: David Roger <droger@chromium.org>
Date: Wed Oct 20 23:45:15 2021

Fix Use-After-Free in ForceSigninVerifier

See https://crbug.com/1259864 for details about the crash.

(cherry picked from commit 79772972a0d41572db52073e310711b5b2cac23f)

Fixed: 1259864
Change-Id: Ibb959201e948e11c752b95b5e1d0a1e9396f2248
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3226161
Commit-Queue: David Roger <droger@chromium.org>
Reviewed-by: Sylvain Defresne <sdefresne@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#932072}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3234530
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: David Roger <droger@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4638@{#943}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/4dc66405bae74b709ce69d507aa2fb062b7e7d57/chrome/browser/signin/force_signin_verifier.cc
[modify] https://crrev.com/4dc66405bae74b709ce69d507aa2fb062b7e7d57/chrome/browser/signin/force_signin_verifier_unittest.cc


### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-28)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### gi...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fd22c9fd6f15b982160d41839b9af9046697c52f

commit fd22c9fd6f15b982160d41839b9af9046697c52f
Author: David Roger <droger@chromium.org>
Date: Thu Nov 04 11:18:26 2021

[M90-LTS] Fix Use-After-Free in ForceSigninVerifier

See https://crbug.com/1259864 for details about the crash.

(cherry picked from commit 79772972a0d41572db52073e310711b5b2cac23f)

Fixed: 1259864
Change-Id: Ibb959201e948e11c752b95b5e1d0a1e9396f2248
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3226161
Commit-Queue: David Roger <droger@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#932072}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3253392
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1654}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/fd22c9fd6f15b982160d41839b9af9046697c52f/chrome/browser/signin/force_signin_verifier.cc
[modify] https://crrev.com/fd22c9fd6f15b982160d41839b9af9046697c52f/chrome/browser/signin/force_signin_verifier_unittest.cc


### rz...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/18dfa590d29525cb6294399ec0c46c398dca9418

commit 18dfa590d29525cb6294399ec0c46c398dca9418
Author: David Roger <droger@chromium.org>
Date: Thu Nov 04 17:32:28 2021

Revert "[M90-LTS] Fix Use-After-Free in ForceSigninVerifier"

This reverts commit fd22c9fd6f15b982160d41839b9af9046697c52f.

Reason for revert: breaks compile because this CL depends on
https://crrev.com/c/2891862

Original change's description:
> [M90-LTS] Fix Use-After-Free in ForceSigninVerifier
>
> See https://crbug.com/1259864 for details about the crash.
>
> (cherry picked from commit 79772972a0d41572db52073e310711b5b2cac23f)
>
> Fixed: 1259864
> Change-Id: Ibb959201e948e11c752b95b5e1d0a1e9396f2248
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3226161
> Commit-Queue: David Roger <droger@chromium.org>
> Cr-Original-Commit-Position: refs/heads/main@{#932072}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3253392
> Reviewed-by: David Roger <droger@chromium.org>
> Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
> Cr-Commit-Position: refs/branch-heads/4430@{#1654}
> Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

Change-Id: Ia784b4ebbd4259831f37fc81a482132d04d25210
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3260611
Auto-Submit: David Roger <droger@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1660}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/18dfa590d29525cb6294399ec0c46c398dca9418/chrome/browser/signin/force_signin_verifier.cc
[modify] https://crrev.com/18dfa590d29525cb6294399ec0c46c398dca9418/chrome/browser/signin/force_signin_verifier_unittest.cc


### dr...@chromium.org (2021-11-04)

Resetting merge flags after the revert. The fix is actually not trivial to cherry pick (see https://crbug.com/1266843#c2)

### am...@google.com (2021-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1259864?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057601)*
