# Security: Heap-use-after-free in ProfileInfoCache::SetAuthInfoOfProfileAtIndex 

| Field | Value |
|-------|-------|
| **Issue ID** | [40084202](https://issues.chromium.org/issues/40084202) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Profiles |
| **Platforms** | Mac, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2016-04-29 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 52.0.2720.0 canary  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Visit chrome://md-settings/
2. Then visit chrome://chrome-signin/ and sign in
3. Crash!

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Browser

==3432==ERROR: AddressSanitizer: heap-use-after-free on address 0x201b965c at pc 0x064aa230 bp 0xdeadbeef sp 0x001fca30  

READ of size 4 at 0x201b965c thread T0  

==3432==WARNING: Failed to use and restart external symbolizer!  

#0 0x64aa22f in ProfileInfoCache::SetAuthInfoOfProfileAtIndex C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\profiles\profile\_info\_cache.cc:659

```
#1 0x6183f86 in ProfileAttributesEntry::SetAuthInfo C:\b\build\slave\Win_ASan_Release\build\src\chrome\browser\profiles\profile_attributes_entry.cc:272  
#2 0x66dd38c in ChromeSigninClient::OnSignedIn C:\b\build\slave\Win_ASan_Release\build\src\chrome\browser\signin\chrome_signin_client.cc:247  
#3 0xcf41203 in SigninManager::OnSignedIn C:\b\build\slave\Win_ASan_Release\build\src\components\signin\core\browser\signin_manager.cc:382  
#4 0xcf406db in SigninManager::CompletePendingSignin C:\b\build\slave\Win_ASan_Release\build\src\components\signin\core\browser\signin_manager.cc:342  
#5 0xb0a2903 in OneClickSigninSyncStarter::ConfirmAndSignin C:\b\build\slave\Win_ASan_Release\build\src\chrome\browser\ui\sync\one_click_signin_sync_starte  

```

r.cc:364  

#6 0xb0a0d7e in OneClickSigninSyncStarter::OnRegisteredForPolicy C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\ui\sync\one\_click\_signin\_sync\_s  

tarter.cc:206  

#7 0xf35ac6c in base::internal::Invoker<base::IndexSequence<0>,base::internal::BindState<base::internal::RunnableAdapter<void (ThumbnailTabHelper::\*)(const  

thumbnails::ThumbnailingContext &, const SkBitmap &) **attribute**((thiscall))>,void (ThumbnailTabHelper \*, const thumbnails::ThumbnailingContext &, const SkB  

itmap &),base::WeakPtr<ThumbnailTabHelper> >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (ThumbnailTabHelper::\*)(const thumbnails:  

:ThumbnailingContext &, const SkBitmap &) **attribute**((thiscall))> >,void (const thumbnails::ThumbnailingContext &, const SkBitmap &)>::Run C:\b\build\slave\  

Win\_ASan\_Release\build\src\base\bind\_internal.h:372  

#8 0x62919c8 in policy::UserPolicySigninService::RegisterForPolicy C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\policy\cloud\user\_policy\_sign  

in\_service.cc:77  

#9 0xb0a0853 in OneClickSigninSyncStarter::ConfirmSignin C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\ui\sync\one\_click\_signin\_sync\_starter.c  

c:152  

#10 0x66ac4cf in base::internal::Invoker<base::IndexSequence<0>,base::internal::BindState<base::internal::RunnableAdapter<void (JsonPrefStore::\*)(const bas  

e::Callback<void (),base::internal::CopyMode::Copyable> &) **attribute**((thiscall))>,void (JsonPrefStore \*, const base::Callback<void (),base::internal::CopyM  

ode::Copyable> &),base::WeakPtr<JsonPrefStore> >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (JsonPrefStore::\*)(const base::Callba  

ck<void (),base::internal::CopyMode::Copyable> &) **attribute**((thiscall))> >,void (const base::Callback<void (),base::internal::CopyMode::Copyable> &)>::Run  

C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:372  

#11 0xcf3bc4e in SigninManager::StartSignInWithRefreshToken C:\b\build\slave\Win\_ASan\_Release\build\src\components\signin\core\browser\signin\_manager.cc:11  

1  

#12 0xb09fb8a in OneClickSigninSyncStarter::OneClickSigninSyncStarter C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\ui\sync\one\_click\_signin\_s  

ync\_starter.cc:102  

#13 0xade384b in InlineSigninHelper::CreateSyncStarter C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\ui\webui\signin\inline\_login\_handler\_impl  

.cc:378  

#14 0xade2244 in InlineSigninHelper::OnClientOAuthSuccess C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\ui\webui\signin\inline\_login\_handler\_i  

mpl.cc:360  

#15 0x77e0bdc in GaiaAuthFetcher::OnOAuth2TokenPairFetched C:\b\build\slave\Win\_ASan\_Release\build\src\google\_apis\gaia\gaia\_auth\_fetcher.cc:783  

#16 0x77e4f14 in GaiaAuthFetcher::DispatchFetchedRequest C:\b\build\slave\Win\_ASan\_Release\build\src\google\_apis\gaia\gaia\_auth\_fetcher.cc:964  

#17 0x77e4abc in GaiaAuthFetcher::OnURLFetchComplete C:\b\build\slave\Win\_ASan\_Release\build\src\google\_apis\gaia\gaia\_auth\_fetcher.cc:947  

#18 0x7f4da30 in net::URLFetcherCore::OnCompletedURLRequest C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_fetcher\_core.cc:721  

#19 0x7f521b1 in base::internal::Invoker<base::IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (net::URLFetcherCore::\*)(b  

ase::TimeDelta) **attribute**((thiscall))>,void (net::URLFetcherCore \*, base::TimeDelta),net::URLFetcherCore \*,base::TimeDelta &>,base::internal::InvokeHelper<  

0,void,base::internal::RunnableAdapter<void (net::URLFetcherCore::\*)(base::TimeDelta) **attribute**((thiscall))> >,void ()>::Run C:\b\build\slave\Win\_ASan\_Rele  

ase\build\src\base\bind\_internal.h:367  

#20 0x72c0485 in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\debug\task\_annotator.cc:49  

#21 0x712b2c0 in base::MessageLoop::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:479  

#22 0x712ca17 in base::MessageLoop::DoWork C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:598  

#23 0x72c3823 in base::MessagePumpForUI::DoRunLoop C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_pump\_win.cc:173  

#24 0x72c25f6 in base::MessagePumpWin::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_pump\_win.cc:54  

#25 0x712a64b in base::MessageLoop::RunHandler C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:443  

#26 0x721b4b5 in base::RunLoop::Run+0x1c5 (C:\Users\admin\Desktop\asan-win32-release-389383\chrome.dll+0x334b4b5)  

#27 0x5d64ef8 in ChromeBrowserMainParts::MainMessageLoopRun C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\chrome\_browser\_main.cc:1855  

#28 0xb6fb37e in content::BrowserMainLoop::RunMainMessageLoopParts C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\browser\_main\_loop.cc:956  

#29 0xb69dc1f in content::BrowserMainRunnerImpl::Run C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\browser\_main\_runner.cc:154  

#30 0xb6681fa in content::BrowserMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\browser\_main.cc:46  

#31 0x6e3ac50 in content::RunNamedProcessTypeMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:381  

#32 0x6e3cb6d in content::ContentMainRunnerImpl::Run C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:742  

#33 0x6e3a804 in content::ContentMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main.cc:20  

#34 0x5b0123e in ChromeMain C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_main.cc:84  

#35 0x13badf9 in MainDllLoader::Launch C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\main\_dll\_loader\_win.cc:185  

#36 0x13b276a in main C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_exe\_main\_win.cc:267  

#37 0x1f6adb4 in \_\_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:255  

#38 0x77b73c44 in BaseThreadInitThunk+0x11 (C:\Windows\system32\kernel32.dll+0x77e33c44)  

#39 0x77a337f4 in RtlInitializeExceptionChain+0xee (C:\Windows\SYSTEM32\ntdll.dll+0x77f237f4)  

#40 0x77a337c7 in RtlInitializeExceptionChain+0xc1 (C:\Windows\SYSTEM32\ntdll.dll+0x77f237c7)

0x201b965c is located 12 bytes inside of 32-byte region [0x201b9650,0x201b9670)  

freed by thread T14 here:  

#0 0x1f54584 in free+0xa4 (C:\Users\admin\Desktop\asan-win32-release-389383\chrome.exe+0xfa4584)  

#1 0x5b05f56 in std::basic\_string<char,std::char\_traits<char>,std::allocator<char> >::\_Tidy C:\b\depot\_tools\win\_toolchain\vs\_files\95ddda401ec5678f15eeed0  

1d2bee08fcbc5ee97\VC\include\xstring:2253  

#2 0x7bcc3d9 in net::HttpStreamFactoryImpl::RequestStreamInternal C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_stream\_factory\_impl.cc:139  

#3 0x7bcbd5d in net::HttpStreamFactoryImpl::RequestStream C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_stream\_factory\_impl.cc:53  

#4 0x7cfca71 in net::HttpNetworkTransaction::DoCreateStream C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_network\_transaction.cc:811  

#5 0x7cf73df in net::HttpNetworkTransaction::DoLoop C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_network\_transaction.cc:674  

#6 0x7cf5e5a in net::HttpNetworkTransaction::Start C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_network\_transaction.cc:165  

#7 0x6c258e2 in DevToolsNetworkTransaction::Start C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\devtools\devtools\_network\_transaction.cc:147  

#8 0x7af5efe in net::HttpCache::Transaction::DoSendRequest C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_cache\_transaction.cc:1318  

#9 0x7aed735 in net::HttpCache::Transaction::DoLoop C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_cache\_transaction.cc:768  

#10 0x7aeed3f in net::HttpCache::Transaction::Start C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_cache\_transaction.cc:272  

#11 0x7e87476 in net::URLRequestHttpJob::StartTransactionInternal C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:641  

#12 0x7e86884 in net::URLRequestHttpJob::MaybeStartTransactionInternal C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:  

575  

#13 0x7e865ca in net::URLRequestHttpJob::StartTransaction C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:554  

#14 0x7e87d10 in net::URLRequestHttpJob::SetCookieHeaderAndStart C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:810  

#15 0x643aa43 in base::internal::Invoker<base::IndexSequence<0>,base::internal::BindState<base::internal::RunnableAdapter<void (LocalDataContainer::\*)(cons  

t std::list<BrowsingDataQuotaHelper::QuotaInfo,std::allocator[BrowsingDataQuotaHelper::QuotaInfo](javascript:void(0);) > &) **attribute**((thiscall))>,void (LocalDataContainer \*, c  

onst std::list<BrowsingDataQuotaHelper::QuotaInfo,std::allocator[BrowsingDataQuotaHelper::QuotaInfo](javascript:void(0);) > &),base::WeakPtr<LocalDataContainer> >,base::internal::I  

nvokeHelper<1,void,base::internal::RunnableAdapter<void (LocalDataContainer::\*)(const std::list<BrowsingDataQuotaHelper::QuotaInfo,std::allocator<BrowsingDataQ
uotaHelper::QuotaInfo> > &) **attribute**((thiscall))> >,void (const std::list<BrowsingDataQuotaHelper::QuotaInfo,std::allocator<BrowsingDataQuotaHelper::Quota  

Info> > &)>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:372  

#16 0x7bfa70b in net::CookieMonster::GetCookieListWithOptionsTask::Run C:\b\build\slave\Win\_ASan\_Release\build\src\net\cookies\cookie\_monster.cc:493  

#17 0x7bff2ce in net::CookieMonster::DoCookieTaskForURL C:\b\build\slave\Win\_ASan\_Release\build\src\net\cookies\cookie\_monster.cc:2276  

#18 0x7c01383 in net::CookieMonster::GetCookieListWithOptionsAsync C:\b\build\slave\Win\_ASan\_Release\build\src\net\cookies\cookie\_monster.cc:891  

#19 0x7e822e2 in net::URLRequestHttpJob::AddCookieHeaderAndStart C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:801  

#20 0x7e7ff6b in net::URLRequestHttpJob::Start C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:382  

#21 0x7863570 in net::URLRequest::StartJob C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request.cc:654  

#22 0x7862acf in net::URLRequest::BeforeRequestComplete C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request.cc:597  

#23 0x7862430 in net::URLRequest::Start C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request.cc:522  

#24 0xbde2530 in content::ResourceLoader::Resume C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\loader\resource\_loader.cc:464  

#25 0xbdeb8c5 in content::ThrottlingResourceHandler::ResumeStart C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\loader\throttling\_resource\_han  

dler.cc:184  

#26 0xbe193d3 in content::NavigationResourceThrottle::OnUIChecksPerformed C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\loader\navigation\_res  

ource\_throttle.cc:235  

#27 0x633b189 in base::internal::Invoker<base::IndexSequence<0>,base::internal::BindState<base::internal::RunnableAdapter<void (printing::PrintJobWorker::\*  

)(printing::PrintingContext::Result) **attribute**((thiscall))>,void (printing::PrintJobWorker \*, printing::PrintingContext::Result),base::WeakPtr<printing::Pr  

intJobWorker> >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (printing::PrintJobWorker::\*)(printing::PrintingContext::Result) **att  

ribute**((thiscall))> >,void (printing::PrintingContext::Result)>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:372  

#28 0xbe1bd57 in base::internal::Invoker<base::IndexSequence<0>,base::internal::BindState<base::Callback<void (content::NavigationThrottle::ThrottleCheckRe  

sult),base::internal::CopyMode::Copyable>,void (content::NavigationThrottle::ThrottleCheckResult),content::NavigationThrottle::ThrottleCheckResult &>,base::int  

ernal::InvokeHelper<0,void,base::Callback<void (content::NavigationThrottle::ThrottleCheckResult),base::internal::CopyMode::Copyable> >,void ()>::Run C:\b\buil  

d\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:367  

#29 0x72c0485 in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\debug\task\_annotator.cc:49

previously allocated by thread T14 here:  

#0 0x1f54658 in malloc+0xb8 (C:\Users\admin\Desktop\asan-win32-release-389383\chrome.exe+0xfa4658)  

#1 0x12fc14bd in operator new f:\dd\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:19  

#2 0x5b06d64 in std::basic\_string<char,std::char\_traits<char>,std::allocator<char> >::\_Copy C:\b\depot\_tools\win\_toolchain\vs\_files\95ddda401ec5678f15eeed0  

1d2bee08fcbc5ee97\VC\include\xstring:2186  

#3 0x5b0657b in std::basic\_string<char,std::char\_traits<char>,std::allocator<char> >::assign C:\b\depot\_tools\win\_toolchain\vs\_files\95ddda401ec5678f15eeed  

01d2bee08fcbc5ee97\VC\include\xstring:1148  

#4 0x7bcda9a in net::HttpStreamFactoryImpl::GetAlternativeServiceFor C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_stream\_factory\_impl.cc:287  

#5 0x7bcc07a in net::HttpStreamFactoryImpl::RequestStreamInternal C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_stream\_factory\_impl.cc:110  

#6 0x7bcbd5d in net::HttpStreamFactoryImpl::RequestStream C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_stream\_factory\_impl.cc:53  

#7 0x7cfca71 in net::HttpNetworkTransaction::DoCreateStream C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_network\_transaction.cc:811  

#8 0x7cf73df in net::HttpNetworkTransaction::DoLoop C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_network\_transaction.cc:674  

#9 0x7cf5e5a in net::HttpNetworkTransaction::Start C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_network\_transaction.cc:165  

#10 0x6c258e2 in DevToolsNetworkTransaction::Start C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\devtools\devtools\_network\_transaction.cc:147  

#11 0x7af5efe in net::HttpCache::Transaction::DoSendRequest C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_cache\_transaction.cc:1318  

#12 0x7aed735 in net::HttpCache::Transaction::DoLoop C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_cache\_transaction.cc:768  

#13 0x7aeed3f in net::HttpCache::Transaction::Start C:\b\build\slave\Win\_ASan\_Release\build\src\net\http\http\_cache\_transaction.cc:272  

#14 0x7e87476 in net::URLRequestHttpJob::StartTransactionInternal C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:641  

#15 0x7e86884 in net::URLRequestHttpJob::MaybeStartTransactionInternal C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:  

575  

#16 0x7e865ca in net::URLRequestHttpJob::StartTransaction C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:554  

#17 0x7e87d10 in net::URLRequestHttpJob::SetCookieHeaderAndStart C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:810  

#18 0x643aa43 in base::internal::Invoker<base::IndexSequence<0>,base::internal::BindState<base::internal::RunnableAdapter<void (LocalDataContainer::\*)(cons  

t std::list<BrowsingDataQuotaHelper::QuotaInfo,std::allocator[BrowsingDataQuotaHelper::QuotaInfo](javascript:void(0);) > &) **attribute**((thiscall))>,void (LocalDataContainer \*, c  

onst std::list<BrowsingDataQuotaHelper::QuotaInfo,std::allocator[BrowsingDataQuotaHelper::QuotaInfo](javascript:void(0);) > &),base::WeakPtr<LocalDataContainer> >,base::internal::I  

nvokeHelper<1,void,base::internal::RunnableAdapter<void (LocalDataContainer::\*)(const std::list<BrowsingDataQuotaHelper::QuotaInfo,std::allocator<BrowsingDataQ
uotaHelper::QuotaInfo> > &) **attribute**((thiscall))> >,void (const std::list<BrowsingDataQuotaHelper::QuotaInfo,std::allocator<BrowsingDataQuotaHelper::Quota  

Info> > &)>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:372  

#19 0x7bfa70b in net::CookieMonster::GetCookieListWithOptionsTask::Run C:\b\build\slave\Win\_ASan\_Release\build\src\net\cookies\cookie\_monster.cc:493  

#20 0x7bff2ce in net::CookieMonster::DoCookieTaskForURL C:\b\build\slave\Win\_ASan\_Release\build\src\net\cookies\cookie\_monster.cc:2276  

#21 0x7c01383 in net::CookieMonster::GetCookieListWithOptionsAsync C:\b\build\slave\Win\_ASan\_Release\build\src\net\cookies\cookie\_monster.cc:891  

#22 0x7e822e2 in net::URLRequestHttpJob::AddCookieHeaderAndStart C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:801  

#23 0x7e7ff6b in net::URLRequestHttpJob::Start C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request\_http\_job.cc:382  

#24 0x7863570 in net::URLRequest::StartJob C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request.cc:654  

#25 0x7862acf in net::URLRequest::BeforeRequestComplete C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request.cc:597  

#26 0x7862430 in net::URLRequest::Start C:\b\build\slave\Win\_ASan\_Release\build\src\net\url\_request\url\_request.cc:522  

#27 0xbde2530 in content::ResourceLoader::Resume C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\loader\resource\_loader.cc:464  

#28 0xbdeb8c5 in content::ThrottlingResourceHandler::ResumeStart C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\loader\throttling\_resource\_han  

dler.cc:184  

#29 0xbe193d3 in content::NavigationResourceThrottle::OnUIChecksPerformed C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\loader\navigation\_res  

ource\_throttle.cc:235

Thread T14 created by T0 here:  

#0 0x1f612c0 in \_\_asan\_wrap\_CreateThread+0x60 (C:\Users\admin\Desktop\asan-win32-release-389383\chrome.exe+0xfb12c0)  

#1 0x71c4137 in base::`anonymous namespace'::CreateThreadInternal C:\b\build\slave\Win\_ASan\_Release\build\src\base\threading\platform\_thread\_win.cc:120  

#2 0x71c4093 in base::PlatformThread::CreateWithPriority C:\b\build\slave\Win\_ASan\_Release\build\src\base\threading\platform\_thread\_win.cc:197  

#3 0x71315db in base::Thread::StartWithOptions C:\b\build\slave\Win\_ASan\_Release\build\src\base\threading\thread.cc:116  

#4 0xb310aa0 in content::BrowserThreadImpl::StartWithOptions C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\browser\_thread\_impl.cc:316  

#5 0xb6f5cd0 in content::BrowserMainLoop::CreateThreads C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\browser\_main\_loop.cc:919  

#6 0xbf6319a in content::StartupTaskRunner::RunAllTasksNow C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\startup\_task\_runner.cc:40  

#7 0xb6f4678 in content::BrowserMainLoop::CreateStartupTasks C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\browser\_main\_loop.cc:826  

#8 0xb69d08e in content::BrowserMainRunnerImpl::Initialize C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\browser\_main\_runner.cc:139  

#9 0xb6681c0 in content::BrowserMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\browser\browser\_main.cc:42  

#10 0x6e3ac50 in content::RunNamedProcessTypeMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:381  

#11 0x6e3cb6d in content::ContentMainRunnerImpl::Run C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:742  

#12 0x6e3a804 in content::ContentMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main.cc:20  

#13 0x5b0123e in ChromeMain C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_main.cc:84  

#14 0x13badf9 in MainDllLoader::Launch C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\main\_dll\_loader\_win.cc:185  

#15 0x13b276a in main C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_exe\_main\_win.cc:267  

#16 0x1f6adb4 in \_\_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:255  

#17 0x77b73c44 in BaseThreadInitThunk+0x11 (C:\Windows\system32\kernel32.dll+0x77e33c44)  

#18 0x77a337f4 in RtlInitializeExceptionChain+0xee (C:\Windows\SYSTEM32\ntdll.dll+0x77f237f4)  

#19 0x77a337c7 in RtlInitializeExceptionChain+0xc1 (C:\Windows\SYSTEM32\ntdll.dll+0x77f237c7)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\profiles\profile\_info\_cache.cc:659 in ProfileInfoCach  

e::SetAuthInfoOfProfileAtIndex  

Shadow bytes around the buggy address:  

0x34037270: 00 00 00 04 fa fa 00 00 00 fa fa fa fd fd fd fa  

0x34037280: fa fa 00 00 00 fa fa fa 00 00 00 fa fa fa 00 00  

0x34037290: 00 fa fa fa fd fd fd fa fa fa 00 00 00 fa fa fa  

0x340372a0: fd fd fd fd fa fa 00 00 04 fa fa fa fd fd fd fa  

0x340372b0: fa fa fd fd fd fd fa fa fd fd fd fa fa fa fd fd  

=>0x340372c0: fd fa fa fa fd fd fd fa fa fa fd[fd]fd fd fa fa  

0x340372d0: fd fd fd fa fa fa fd fd fd fd fa fa fd fd fd fa  

0x340372e0: fa fa fd fd fd fa fa fa 00 00 00 fa fa fa fd fd  

0x340372f0: fd fd fa fa fd fd fd fd fa fa 00 00 04 fa fa fa  

0x34037300: 00 00 00 fa fa fa 00 00 00 fa fa fa 00 00 04 fa  

0x34037310: fa fa 00 00 04 fa fa fa 00 00 00 fa fa fa 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

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

==3432==ABORTING

## Attachments

- [Recording.mp4](attachments/Recording.mp4) (application/octet-stream, 1.2 MB)

## Timeline

### ch...@gmail.com (2016-04-30)

[Empty comment from Monorail migration]

### rs...@chromium.org (2016-05-02)

mlerman: I think this may be from recent refactorings by an external contributor as part of https://crbug.com/chromium/305720. Can you help triage?

[Monorail components: UI>Browser>Profiles]

### ml...@chromium.org (2016-05-02)

crash report: e572d06c00000000 https://crash.corp.google.com/browse?stbtiq=e572d06c00000000, I repro-ed this very easily.

### ml...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### ml...@chromium.org (2016-05-02)

That repro & crash report was on a Mac.

### ml...@chromium.org (2016-05-02)

Assigning to Anthony, he'll take a look at it.

### an...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-02)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ts...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7426febf7c71bba00d58289d4066753012a04d81

commit 7426febf7c71bba00d58289d4066753012a04d81
Author: anthonyvd <anthonyvd@chromium.org>
Date: Tue May 03 19:11:06 2016

Fix a used-after-free caused by an unremoved Observer.

ProfileInfoHandler starts observing the ProfileInfoCache when it receives the
JavascriptAllowed event and stops on JavascriptDisallowed, which isn't always
called. This CL uses ScopedObserver to ensure ProfileInfoHandler instances are
never freed without removing themselves as Observers.

BUG=607921

Review-Url: https://codereview.chromium.org/1942323002
Cr-Commit-Position: refs/heads/master@{#391320}

[modify] https://crrev.com/7426febf7c71bba00d58289d4066753012a04d81/chrome/browser/ui/webui/settings/profile_info_handler.cc
[modify] https://crrev.com/7426febf7c71bba00d58289d4066753012a04d81/chrome/browser/ui/webui/settings/profile_info_handler.h


### an...@chromium.org (2016-05-03)

tommycli@ any idea if this was also an issue in M51 and would require a merge?

### to...@chromium.org (2016-05-03)

Hi, no merge required.

The ProfileInfoHandler was a new file from 04/19. https://codereview.chromium.org/1900913002

That's after the 51 branch point, so the bug shouldn't exist in M51.

Thanks for fixing this!

Tommy

### rs...@chromium.org (2016-05-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-05-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-20)

Congrats! $1,000 for this one.

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/607921?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084202)*
