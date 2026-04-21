# Security: UAF in  base::ObserverList<ash::eche_app::EcheConnectionStatusObserver::Observer

| Field | Value |
|-------|-------|
| **Issue ID** | [40063621](https://issues.chromium.org/issues/40063621) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Profiles, UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | cr...@google.com |
| **Created** | 2023-03-16 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in base::ObserverList<ash::eche\_app::EcheConnectionStatusObserver::Observer

**VERSION**  

Chromium 113.0.5656.0 (Developer Build) (64-bit)  

Revision 04b90a4bf75a2a4e235fba953ef3bc8a5b8e2b6d-refs/heads/main@{#1118021}  

ChromiumOS in linux

**REPRODUCTION CASE**

1. Download the latest asan build ChromiumOS(linux-release-chromeos/asan-linux-release-1118021.zip  
   
   ) and run the command:  
   
   ./chrome --user-data-dir=/tmp/any --enable-features=EcheNetworkConnectionState
2. Close the ChromiumOS and trigger the UAF

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**

=================================================================  

==5314==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b0000fc158 at pc 0x55db3e819e1b bp 0x7ffd6f872d70 sp 0x7ffd6f872d68  

READ of size 8 at 0x60b0000fc158 thread T0 (chrome)  

==5314==WARNING: invalid path to external symbolizer!  

==5314==WARNING: Failed to use and restart external symbolizer!  

#0 0x55db3e819e1a in begin ./../../buildtools/third\_party/libc++/trunk/include/vector:1426:30  

#1 0x55db3e819e1a in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:44:37  

#2 0x55db3e819e1a in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:105:10  

#3 0x55db3e819e1a in find\_if<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &, (lambda at ../../base/observer\_list.h:288:21), base::identity, std::Cr::random\_access\_iterator\_tag> ./../../base/ranges/algorithm.h:483:26  

#4 0x55db3e819e1a in base::ObserverList<ash::eche\_app::EcheConnectionStatusObserver::Observer, false, true, base::internal::CheckedObserverAdapter>::RemoveObserver(ash::eche\_app::EcheConnectionStatusObserver::Observer const\*) ./../../base/observer\_list.h:287:21  

#5 0x55db3e80a86f in ash::phonehub::RecentAppsInteractionHandlerImpl::~RecentAppsInteractionHandlerImpl() ./../../chromeos/ash/components/phonehub/recent\_apps\_interaction\_handler\_impl.cc:58:39  

#6 0x55db3e80a9f5 in ash::phonehub::RecentAppsInteractionHandlerImpl::~RecentAppsInteractionHandlerImpl() ./../../chromeos/ash/components/phonehub/recent\_apps\_interaction\_handler\_impl.cc:55:71  

#7 0x55db3e7d7082 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#8 0x55db3e7d7082 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#9 0x55db3e7d7082 in ash::phonehub::PhoneHubManagerImpl::Shutdown() ./../../chromeos/ash/components/phonehub/phone\_hub\_manager\_impl.cc:294:36  

#10 0x55db3ac7a748 in ShutdownFactoriesInOrder ./../../components/keyed\_service/core/dependency\_manager.cc:172:14  

#11 0x55db3ac7a748 in DependencyManager::PerformInterlockedTwoPhaseShutdown(DependencyManager\*, void\*, DependencyManager\*, void\*) ./../../components/keyed\_service/core/dependency\_manager.cc:149:3  

#12 0x55db3f2e4f50 in ProfileImpl::~ProfileImpl() ./../../chrome/browser/profiles/profile\_impl.cc:927:3  

#13 0x55db3f2e564f in ProfileImpl::~ProfileImpl() ./../../chrome/browser/profiles/profile\_impl.cc:873:29  

#14 0x55db3f2f3e1b in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#15 0x55db3f2f3e1b in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#16 0x55db3f2f3e1b in ProfileDestroyer::DestroyOriginalProfileNow(std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>) ./../../chrome/browser/profiles/profile\_destroyer.cc:273:11  

#17 0x55db3f2f0ed0 in Timeout ./../../chrome/browser/profiles/profile\_destroyer.cc:435:3  

#18 0x55db3f2f0ed0 in ProfileDestroyer::Start(std::Cr::set<content::RenderProcessHost\*, std::Cr::less[content::RenderProcessHost\\*](javascript:void(0);), std::Cr::allocator[content::RenderProcessHost\\*](javascript:void(0);)> const&) ./../../chrome/browser/profiles/profile\_destroyer.cc:326:5  

#19 0x55db3f2efae2 in ProfileDestroyer::DestroyOriginalProfileWhenAppropriateWithTimeout(std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>, base::TimeDelta) ./../../chrome/browser/profiles/profile\_destroyer.cc:152:22  

#20 0x55db3f307f0e in ProfileManager::ProfileInfo::~ProfileInfo() ./../../chrome/browser/profiles/profile\_manager.cc:1541:3  

#21 0x55db3f30f0fc in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#22 0x55db3f30f0fc in std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>::reset[abi:v170000](javascript:void(0);) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#23 0x55db3f30c8af in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#24 0x55db3f30c8af in ~pair ./../../buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:61:29  

#25 0x55db3f30c8af in void std::Cr::\_\_destroy\_at[abi:v170000]<std::Cr::pair<base::FilePath const, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, 0>(std::Cr::pair<base::FilePath const, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:66:13  

#26 0x55db3f30c878 in destroy\_at<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:101:5  

#27 0x55db3f30c878 in destroy<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:323:9  

#28 0x55db3f30c878 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::\_\_map\_value\_compare<base::FilePath, std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::less[base::FilePath](javascript:void(0);), true>, std::Cr::allocator<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>>>::destroy(std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, void\*>\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1814:9  

#29 0x55db3f30b5a8 in clear ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1851:5  

#30 0x55db3f30b5a8 in clear ./../../buildtools/third\_party/libc++/trunk/include/map:1393:37  

#31 0x55db3f30b5a8 in ProfileManager::~ProfileManager() ./../../chrome/browser/profiles/profile\_manager.cc:430:18  

#32 0x55db3f2fb4ff in ProfileManager::~ProfileManager() ./../../chrome/browser/profiles/profile\_manager.cc:402:35  

#33 0x55db3ebb60b4 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#34 0x55db3ebb60b4 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#35 0x55db3ebb60b4 in BrowserProcessImpl::StartTearDown() ./../../chrome/browser/browser\_process\_impl.cc:505:22  

#36 0x55db3ebb2112 in ChromeBrowserMainParts::PostMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1897:21  

#37 0x55db33b62893 in ash::ChromeBrowserMainPartsAsh::PostMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1597:32  

#38 0x55db2e5552ab in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() ./../../content/browser/browser\_main\_loop.cc:1130:13  

#39 0x55db2e55a251 in content::BrowserMainRunnerImpl::Shutdown() ./../../content/browser/browser\_main\_runner\_impl.cc:176:17  

#40 0x55db2e54e435 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:16  

#41 0x55db35052b2e in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:740:10  

#42 0x55db350569c5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1311:10  

#43 0x55db350563a6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1165:12  

#44 0x55db3504fd70 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#45 0x55db350509a2 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#46 0x55db25c9bb37 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#47 0x7f7796bc2082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x60b0000fc158 is located 56 bytes inside of 112-byte region [0x60b0000fc120,0x60b0000fc190)  

freed by thread T0 (chrome) here:  

#0 0x55db25c99a1d in operator delete(void\*) *asan\_rtl*:3  

#1 0x55db4ba556a5 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#2 0x55db4ba556a5 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#3 0x55db4ba556a5 in ash::eche\_app::EcheAppManager::Shutdown() ./../../ash/webui/eche\_app\_ui/eche\_app\_manager.cc:182:36  

#4 0x55db3ac7a748 in ShutdownFactoriesInOrder ./../../components/keyed\_service/core/dependency\_manager.cc:172:14  

#5 0x55db3ac7a748 in DependencyManager::PerformInterlockedTwoPhaseShutdown(DependencyManager\*, void\*, DependencyManager\*, void\*) ./../../components/keyed\_service/core/dependency\_manager.cc:149:3  

#6 0x55db3f2e4f50 in ProfileImpl::~ProfileImpl() ./../../chrome/browser/profiles/profile\_impl.cc:927:3  

#7 0x55db3f2e564f in ProfileImpl::~ProfileImpl() ./../../chrome/browser/profiles/profile\_impl.cc:873:29  

#8 0x55db3f2f3e1b in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#9 0x55db3f2f3e1b in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#10 0x55db3f2f3e1b in ProfileDestroyer::DestroyOriginalProfileNow(std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>) ./../../chrome/browser/profiles/profile\_destroyer.cc:273:11  

#11 0x55db3f2f0ed0 in Timeout ./../../chrome/browser/profiles/profile\_destroyer.cc:435:3  

#12 0x55db3f2f0ed0 in ProfileDestroyer::Start(std::Cr::set<content::RenderProcessHost\*, std::Cr::less[content::RenderProcessHost\\*](javascript:void(0);), std::Cr::allocator[content::RenderProcessHost\\*](javascript:void(0);)> const&) ./../../chrome/browser/profiles/profile\_destroyer.cc:326:5  

#13 0x55db3f2efae2 in ProfileDestroyer::DestroyOriginalProfileWhenAppropriateWithTimeout(std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>, base::TimeDelta) ./../../chrome/browser/profiles/profile\_destroyer.cc:152:22  

#14 0x55db3f307f0e in ProfileManager::ProfileInfo::~ProfileInfo() ./../../chrome/browser/profiles/profile\_manager.cc:1541:3  

#15 0x55db3f30f0fc in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#16 0x55db3f30f0fc in std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>::reset[abi:v170000](javascript:void(0);) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#17 0x55db3f30c8af in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:263:75  

#18 0x55db3f30c8af in ~pair ./../../buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:61:29  

#19 0x55db3f30c8af in void std::Cr::\_\_destroy\_at[abi:v170000]<std::Cr::pair<base::FilePath const, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, 0>(std::Cr::pair<base::FilePath const, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:66:13  

#20 0x55db3f30c878 in destroy\_at<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:101:5  

#21 0x55db3f30c878 in destroy<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:323:9  

#22 0x55db3f30c878 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::\_\_map\_value\_compare<base::FilePath, std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::less[base::FilePath](javascript:void(0);), true>, std::Cr::allocator<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>>>::destroy(std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, void\*>\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1814:9  

#23 0x55db3f30b5a8 in clear ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1851:5  

#24 0x55db3f30b5a8 in clear ./../../buildtools/third\_party/libc++/trunk/include/map:1393:37  

#25 0x55db3f30b5a8 in ProfileManager::~ProfileManager() ./../../chrome/browser/profiles/profile\_manager.cc:430:18  

#26 0x55db3f2fb4ff in ProfileManager::~ProfileManager() ./../../chrome/browser/profiles/profile\_manager.cc:402:35  

#27 0x55db3ebb60b4 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:65:5  

#28 0x55db3ebb60b4 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:297:7  

#29 0x55db3ebb60b4 in BrowserProcessImpl::StartTearDown() ./../../chrome/browser/browser\_process\_impl.cc:505:22  

#30 0x55db3ebb2112 in ChromeBrowserMainParts::PostMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1897:21  

#31 0x55db33b62893 in ash::ChromeBrowserMainPartsAsh::PostMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1597:32  

#32 0x55db2e5552ab in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() ./../../content/browser/browser\_main\_loop.cc:1130:13  

#33 0x55db2e55a251 in content::BrowserMainRunnerImpl::Shutdown() ./../../content/browser/browser\_main\_runner\_impl.cc:176:17  

#34 0x55db2e54e435 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:34:16  

#35 0x55db35052b2e in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:740:10  

#36 0x55db350569c5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1311:10  

#37 0x55db350563a6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1165:12  

#38 0x55db3504fd70 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#39 0x55db350509a2 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#40 0x55db25c9bb37 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#41 0x7f7796bc2082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:  

#0 0x55db25c991bd in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55db4ba5409f in make\_unique[ash::eche\_app::EcheConnectionStatusObserver](javascript:void(0);) ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:26  

#2 0x55db4ba5409f in ash::eche\_app::EcheAppManager::EcheAppManager(PrefService\*, std::Cr::unique\_ptr<ash::eche\_app::SystemInfo, std::Cr::default\_delete[ash::eche\_app::SystemInfo](javascript:void(0);)>, ash::phonehub::PhoneHubManager\*, ash::device\_sync::DeviceSyncClient\*, ash::multidevice\_setup::MultiDeviceSetupClient\*, ash::secure\_channel::SecureChannelClient\*, std::Cr::unique\_ptr<ash::secure\_channel::PresenceMonitorClient, std::Cr::default\_delete[ash::secure\_channel::PresenceMonitorClient](javascript:void(0);)>, base::RepeatingCallback<void (absl::optional<long> const&, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>> const&, absl::optional<long> const&, gfx::Image const&, std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>> const&)>, base::RepeatingCallback<void (absl::optional<std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>>> const&, absl::optional<std::Cr::basic\_string<char16\_t, std::Cr::char\_traits<char16\_t>, std::Cr::allocator<char16\_t>>> const&, std::Cr::unique\_ptr<ash::eche\_app::LaunchAppHelper::NotificationInfo, std::Cr::default\_delete[ash::eche\_app::LaunchAppHelper::NotificationInfo](javascript:void(0);)>)>, base::RepeatingCallback<void (std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&)>) ./../../ash/webui/eche\_app\_ui/eche\_app\_manager.cc:116:11  

#3 0x55db33d2aea7 in ash::eche\_app::EcheAppManagerFactory::BuildServiceInstanceFor(content::BrowserContext\*) const ./../../chrome/browser/ash/eche\_app/eche\_app\_manager\_factory.cc:263:14  

#4 0x55db3ac818f6 in KeyedServiceFactory::GetServiceForContext(void\*, bool) ./../../components/keyed\_service/core/keyed\_service\_factory.cc:93:15  

#5 0x55db342bba05 in ash::UserSessionInitializer::OnUserSessionStarted(bool) ./../../chrome/browser/ash/login/session/user\_session\_initializer.cc:282:5  

#6 0x55db3e180a96 in session\_manager::SessionManager::SessionStarted() ./../../components/session\_manager/core/session\_manager.cc:73:14  

#7 0x55db342b9725 in ash::ChromeSessionManager::SessionStarted() ./../../chrome/browser/ash/login/session/chrome\_session\_manager.cc:394:36  

#8 0x55db342b92ef in ash::(anonymous namespace)::StartUserSession(Profile\*, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&) ./../../chrome/browser/ash/login/session/chrome\_session\_manager.cc:195:45  

#9 0x55db342b8455 in ash::ChromeSessionManager::Initialize(base::CommandLine const&, Profile\*, bool) ./../../chrome/browser/ash/login/session/chrome\_session\_manager.cc:390:3  

#10 0x55db33b5f4b4 in ash::ChromeBrowserMainPartsAsh::PostProfileInit(Profile\*, bool) ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1226:60  

#11 0x55db3ebab87a in CallPostProfileInit ./../../chrome/browser/chrome\_browser\_main.cc:1206:3  

#12 0x55db3ebab87a in ChromeBrowserMainParts::ProfileInitManager::ProfileInitManager(ChromeBrowserMainParts\*, Profile\*) ./../../chrome/browser/chrome\_browser\_main.cc:548:20  

#13 0x55db3ebafd8b in make\_unique<ChromeBrowserMainParts::ProfileInitManager, ChromeBrowserMainParts \*, Profile \*&> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:686:30  

#14 0x55db3ebafd8b in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome\_browser\_main.cc:1613:27  

#15 0x55db3ebaf225 in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1147:18  

#16 0x55db33b5b6e8 in ash::ChromeBrowserMainPartsAsh::PreMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:840:39  

#17 0x55db2e55279c in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser\_main\_loop.cc:985:28  

#18 0x55db2f84a487 in Run ./../../base/functional/callback.h:152:12  

#19 0x55db2f84a487 in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup\_task\_runner.cc:44:29  

#20 0x55db2e551c71 in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser\_main\_loop.cc:895:25  

#21 0x55db2e5599e2 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser\_main\_runner\_impl.cc:139:15  

#22 0x55db2e54e3c4 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:28:32  

#23 0x55db35052b2e in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:740:10  

#24 0x55db350569c5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1311:10  

#25 0x55db350563a6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1165:12  

#26 0x55db3504fd70 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:326:36  

#27 0x55db350509a2 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:343:10  

#28 0x55db25c9bb37 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#29 0x7f7796bc2082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/kuer/chromium\_version/latest\_asan/chrome+0x2a2dae1a) (BuildId: 412a511d02cf1cd3)  

Shadow bytes around the buggy address:  

0x60b0000fbe80: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x60b0000fbf00: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x60b0000fbf80: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x60b0000fc000: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fd fd  

0x60b0000fc080: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

=>0x60b0000fc100: fa fa fa fa fd fd fd fd fd fd fd[fd]fd fd fd fd  

0x60b0000fc180: fd fd fa fa fa fa fa fa fa fa 00 00 00 00 00 00  

0x60b0000fc200: 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa  

0x60b0000fc280: 00 00 00 00 00 00 00 00 00 00 00 00 00 fa fa fa  

0x60b0000fc300: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x60b0000fc380: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd  

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

==5314==ADDITIONAL INFO

==5314==Note: Please include this section with the ASan report.  

Task trace:

==5314==END OF ADDITIONAL INFO  

==5314==ABORTING

## Timeline

### [Deleted User] (2023-03-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2023-03-16)

Severity mitigated by profile destruction.

[Monorail components: UI>Browser>Profiles]

### [Deleted User] (2023-03-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@google.com (2023-03-20)

[Empty comment from Monorail migration]

### th...@google.com (2023-03-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-03-20)

Looking at https://source.chromium.org/chromium/chromium/src/+/main:chromeos/ash/components/phonehub/recent_apps_interaction_handler_impl.cc;l=58?q=RecentAppsInteractionHandlerImpl&ss=chromium, it looks like crisrael@ has been working in this area.

[Monorail components: UI>Shell]

### [Deleted User] (2023-03-24)

[Empty comment from Monorail migration]

### cr...@google.com (2023-03-27)

TAL now, thanks.

### cr...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### cr...@google.com (2023-03-27)

The fix is in review, going to reach out to M113 TPM to determine if this should be merged back or not.

### gi...@appspot.gserviceaccount.com (2023-03-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/50d9aa1803a9b6d9b4c9a6eddcd044ad28d79963

commit 50d9aa1803a9b6d9b4c9a6eddcd044ad28d79963
Author: Crisrael Lucero <crisrael@google.com>
Date: Tue Mar 28 15:17:40 2023

[Eche] Fix heap UAF on shutdown

This fixes a UAF by RecentAppsInteractionHandler during shutdown when
it attempts to stop listening to EcheConnectionStatusHandler, which by
then has already been freed in EcheAppManager.

Test: verified when shutting down Chrome the UAF no longer appears when
kEcheSWA and kEcheNetworkConnectionState are enabled. Also manually
verified that app streaming still works.

Fixed: 1425058
Change-Id: If3a774c14c5c348e8db16f1e245cec4c0c4ff9b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4375507
Reviewed-by: Jon Mann <jonmann@chromium.org>
Commit-Queue: Crisrael Lucero <crisrael@google.com>
Reviewed-by: Pu Shi <pushi@google.com>
Cr-Commit-Position: refs/heads/main@{#1123040}

[modify] https://crrev.com/50d9aa1803a9b6d9b4c9a6eddcd044ad28d79963/chromeos/ash/components/phonehub/recent_apps_interaction_handler_impl.cc
[modify] https://crrev.com/50d9aa1803a9b6d9b4c9a6eddcd044ad28d79963/ash/webui/eche_app_ui/eche_app_manager.h
[modify] https://crrev.com/50d9aa1803a9b6d9b4c9a6eddcd044ad28d79963/ash/webui/eche_app_ui/eche_app_manager.cc


### cr...@google.com (2023-03-28)

[Empty comment from Monorail migration]

### cr...@google.com (2023-03-28)

Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
This is a fix for a security issue (heap UAF).

What changes specifically would you like to merge? Please link to Gerrit.
https://crrev.com/c/4375507

Have the changes been released and tested on canary?
No

Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
Yes. This is behind the EcheNetworkConnectionState but there are no active experiments with that flag.

[Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?
No. Engprod testing is not required.

If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
This merge doesn't address an issue on the stable channel. Verification is not needed by the test team.

### ma...@google.com (2023-03-28)

Can we verify that this no longer occurs on canary prior to merging into M113?

### cr...@google.com (2023-03-28)

Sounds good. The fix landed on ToT recently so when it gets to Canary I'll verify again alongside members of our team.

### [Deleted User] (2023-03-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-29)

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

### ma...@google.com (2023-04-03)

Friendly ping!

### cr...@google.com (2023-04-03)

We're currently waiting until the change (landed in 5682) gets onto the current serving Canary build (currently 5676 according to https://chromiumdash.appspot.com/serving-builds?deviceCategory=Chrome%20OS). Would verifying on current ToT be sufficient or should we continue waiting until 5682+ becomes the official Canary build?

### cr...@google.com (2023-04-03)

Actually some boards are already on 5689 for Canary. Will verify now.

### cr...@google.com (2023-04-03)

Re-answering questions posted by sheriffbot since fix has now been tested on Canary and there is now a finch experiment for just dogfooders behind the flag:

1. Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
This is a fix for a security issue (heap UAF).

2. What changes specifically would you like to merge? Please link to Gerrit.
https://crrev.com/c/4375507

3. Have the changes been released and tested on canary?
Yes, fix landed in 5682 and tested on 5689 Canary.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
Yes. This is behind the EcheNetworkConnectionState, this flag is only active for dogfooders and not to the public on any release channels.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?
No. Engprod testing is not required.

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
This merge doesn't address an issue on the stable channel. Verification is not needed by the test team.

### ma...@google.com (2023-04-03)

Merge approved, M113

### ma...@google.com (2023-04-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9db7a9c77751d30610659e88f5f94817ac9328bf

commit 9db7a9c77751d30610659e88f5f94817ac9328bf
Author: Crisrael Lucero <crisrael@google.com>
Date: Mon Apr 03 23:57:53 2023

[M113][Eche] Fix heap UAF on shutdown

This fixes a UAF by RecentAppsInteractionHandler during shutdown when
it attempts to stop listening to EcheConnectionStatusHandler, which by
then has already been freed in EcheAppManager.

Test: verified when shutting down Chrome the UAF no longer appears when
kEcheSWA and kEcheNetworkConnectionState are enabled. Also manually
verified that app streaming still works.

(cherry picked from commit 50d9aa1803a9b6d9b4c9a6eddcd044ad28d79963)

Fixed: 1425058
Change-Id: If3a774c14c5c348e8db16f1e245cec4c0c4ff9b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4375507
Reviewed-by: Jon Mann <jonmann@chromium.org>
Commit-Queue: Crisrael Lucero <crisrael@google.com>
Reviewed-by: Pu Shi <pushi@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1123040}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4396106
Cr-Commit-Position: refs/branch-heads/5672@{#241}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/9db7a9c77751d30610659e88f5f94817ac9328bf/chromeos/ash/components/phonehub/recent_apps_interaction_handler_impl.cc
[modify] https://crrev.com/9db7a9c77751d30610659e88f5f94817ac9328bf/ash/webui/eche_app_ui/eche_app_manager.h
[modify] https://crrev.com/9db7a9c77751d30610659e88f5f94817ac9328bf/ash/webui/eche_app_ui/eche_app_manager.cc


### am...@chromium.org (2023-04-12)

SI-None as this issue impacts an unlaunched feature (--EcheNetworkConnectionState)

### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations, asnine! The VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### ch...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-02)

issue is SI-None, no release label is needed here 

### am...@chromium.org (2023-05-02)

[Comment Deleted]

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### gm...@google.com (2023-06-21)

[Empty comment from Monorail migration]

### vo...@google.com (2023-06-27)

[Empty comment from Monorail migration]

### gm...@google.com (2023-06-28)

Rejecting for 108 since it's a medium severity that affects only ChromeOS.

### gm...@google.com (2023-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-04)

This issue was migrated from crbug.com/chromium/1425058?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Profiles, UI>Shell]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063621)*
