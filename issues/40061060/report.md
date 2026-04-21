# Security: UAF in ash::network_diagnostics::DnsResolutionRoutine::CreateHostResolver() (browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061060](https://issues.chromium.org/issues/40061060) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Apps>Diagnostics>Connectivity |
| **Platforms** | ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | kh...@google.com |
| **Created** | 2022-09-20 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in ash::network\_diagnostics::DnsResolutionRoutine::CreateHostResolver() in the browser process.

**VERSION**  

Chromium 108.0.5305.0 (Developer Build) (64-bit)  

Revision b9b45a5a28c5240943f5f43f16abf2e84e962315-refs/heads/main@{#1048072}  

ChromiumOS build run in Ubuntu

**REPRODUCTION CASE**  

When I fuzz the chrome.send('sendFeedbackReport',) method in the chrome://connectivity-diagnostics/ in the ChromiumOS,the UAF occured.  

However I cannot reproduce this issue.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

Asan log:

2022-09-19T04:34:51.882517Z ERROR chrome[22860:22860]: [proximity\_auth\_profile\_pref\_manager.cc(185)] Failed to find local state prefs for current user.

# DevTools listening on ws://127.0.0.1:9222/devtools/browser/d6416aaa-da2c-4669-bc24-2da923952450 2022-09-19T04:34:52.082073Z ERROR chrome[22860:22860]: [download\_prefs.cc(155)] DownloadPrefs::DownloadPrefs0,1,/home/fuzz/Downloads 2022-09-19T04:34:52.082144Z ERROR chrome[22860:22860]: [download\_prefs.cc(155)] DownloadPrefs::DownloadPrefs0,1,/home/fuzz/Downloads 2022-09-19T04:34:52.110951Z ERROR chrome[22860:22860]: [rgb\_keyboard\_manager.cc(67)] Attempted to set RGB keyboard color, but flag is disabled. 2022-09-19T04:34:52.153522Z ERROR chrome[22860:22871]: [component\_loader.cc(116)] Can't load /usr/share/chromeos-assets/speech\_synthesis/patts/manifest.json: Manifest file is missing or unreadable 2022-09-19T04:34:52.153585Z ERROR chrome[22860:22871]: [component\_loader.cc(116)] Can't load /usr/share/chromeos-assets/speech\_synthesis/espeak-ng/manifest.json: Manifest file is missing or unreadable 2022-09-19T04:34:52.250600Z ERROR chrome[22860:22860]: [disk\_mount\_manager.cc(521)] Cannot mount 'fusebox://fusebox' as '': kInvalidArgument 2022-09-19T04:34:52.250664Z ERROR chrome[22860:22860]: [fusebox\_mounter.cc(108)] fusebox://fusebox mount error kInvalidArgument 2022-09-19T04:34:52.278363Z ERROR chrome[22860:22860]: [display\_manager\_util.cc(191)] Check failed: false. Received a DSF not on the list: 1.5 2022-09-19T04:34:52.322048Z ERROR chrome[22860:22860]: [rgb\_keyboard\_manager.cc(67)] Attempted to set RGB keyboard color, but flag is disabled. 2022-09-19T04:34:52.402045Z ERROR chrome[22860:22860]: [display\_manager\_util.cc(191)] Check failed: false. Received a DSF not on the list: 1.5 2022-09-19T04:34:52.402221Z ERROR chrome[22860:22860]: [display\_manager\_util.cc(191)] Check failed: false. Received a DSF not on the list: 1.5 2022-09-19T04:34:52.443630Z ERROR chrome[22860:22860]: [disk\_mount\_manager.cc(521)] Cannot mount 'drivefs://BEB7726D6FDCB9F521DD0429CF9403BB' as '': kInvalidArgument 2022-09-19T04:34:52.672318Z ERROR chrome[22860:22860]: [token\_handle\_fetcher.cc(105)] Could not get access token to backfill token handlerInvalid credentials (credentials rejected by client). 2022-09-19T04:34:52.672380Z ERROR chrome[22860:22860]: [user\_session\_manager.cc(2434)] OAuth2 token handle fetch failed. 2022-09-19T04:34:52.672691Z ERROR chrome[22860:22860]: [account\_info\_fetcher.cc(62)] OnGetTokenFailure: Invalid credentials (credentials rejected by client). 2022-09-19T04:34:53.414117Z ERROR chrome[22860:22860]: [display\_manager\_util.cc(191)] Check failed: false. Received a DSF not on the list: 1.5 2022-09-19T04:34:53.414283Z ERROR chrome[22860:22860]: [display\_manager\_util.cc(191)] Check failed: false. Received a DSF not on the list: 1.5 2022-09-19T04:34:54.567404Z ERROR chrome[22860:22877]: [als\_reader.cc(52)] Missing num of als 2022-09-19T04:34:57.490170Z ERROR chrome[22860:22860]: [disk\_mount\_manager.cc(521)] Cannot mount 'drivefs://5F9732F68815308202EADFB2C96ECC2C' as '': kInvalidArgument 2022-09-19T04:34:59.915027Z ERROR nacl\_helper: [nacl\_helper\_linux.cc(315)] NaCl helper process running without a sandbox! Most likely you need to configure your SUID sandbox correctly 2022-09-19T04:34:59.946762Z ERROR chrome[22860:22860]: [zygote\_communication\_linux.cc(275)] Failed to send GetTerminationStatus message to zygote 2022-09-19T04:34:59.965525Z ERROR chrome[22860:22860]: [zygote\_communication\_linux.cc(275)] Failed to send GetTerminationStatus message to zygote 2022-09-19T04:34:59.970250Z ERROR chrome[22860:22860]: [zygote\_communication\_linux.cc(275)] Failed to send GetTerminationStatus message to zygote 2022-09-19T04:34:59.988396Z ERROR chrome[22860:22860]: [zygote\_communication\_linux.cc(275)] Failed to send GetTerminationStatus message to zygote 2022-09-19T04:34:59.991465Z ERROR chrome[22860:22860]: [zygote\_communication\_linux.cc(275)] Failed to send GetTerminationStatus message to zygote 2022-09-19T04:34:59.994095Z ERROR chrome[22860:22860]: [zygote\_communication\_linux.cc(275)] Failed to send GetTerminationStatus message to zygote 2022-09-19T04:34:59.994909Z ERROR chrome[22860:22860]: [zygote\_communication\_linux.cc(275)] Failed to send GetTerminationStatus message to zygote

==22860==ERROR: AddressSanitizer: heap-use-after-free on address 0x6020000d0390 at pc 0x564a04c9a2c8 bp 0x7ffd3fe46eb0 sp 0x7ffd3fe46ea8  

READ of size 8 at 0x6020000d0390 thread T0 (chrome)  

==22860==WARNING: invalid path to external symbolizer!  

==22860==WARNING: Failed to use and restart external symbolizer!  

#0 0x564a04c9a2c7 in ash::network\_diagnostics::DnsResolutionRoutine::CreateHostResolver() ./../../chrome/browser/ash/net/network\_diagnostics/dns\_resolution\_routine.cc:80:22  

#1 0x564a04c9b17b in ash::network\_diagnostics::DnsResolutionRoutine::OnMojoConnectionError() ./../../chrome/browser/ash/net/network\_diagnostics/dns\_resolution\_routine.cc:85:3  

#2 0x564a094dc4d3 in Run ./../../base/callback.h:145:12  

#3 0x564a094dc4d3 in mojo::InterfaceEndpointClient::NotifyError(absl::optional[mojo::DisconnectReason](javascript:void(0);) const&) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:725:31  

#4 0x564a094f8d13 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1016:13  

#5 0x564a094f36b1 in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:929:15  

#6 0x564a094f0b6f in mojo::internal::MultiplexRouter::OnPipeConnectionError(bool) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:839:3  

#7 0x564a094cf8e1 in Run ./../../base/callback.h:145:12  

#8 0x564a094cf8e1 in mojo::Connector::HandleError(bool, bool) ./../../mojo/public/cpp/bindings/lib/connector.cc:688:44  

#9 0x5649fb493102 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/callback.h:267:12  

#10 0x564a08a368cd in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/callback.h:267:12  

#11 0x564a08a3652d in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#12 0x564a072f975c in Run ./../../base/callback.h:145:12  

#13 0x564a072f975c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:133:32  

#14 0x564a0733e900 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:442:29)> ./../../base/task/common/task\_annotator.h:72:5  

#15 0x564a0733e900 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:440:21  

#16 0x564a0733da0d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:296:30  

#17 0x564a0733fb74 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#18 0x564a07451f58 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:293:55  

#19 0x564a07340625 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:599:12  

#20 0x564a0728edd9 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#21 0x5649fcb64f4c in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1046:18  

#22 0x5649fcb69dbb in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:157:15  

#23 0x5649fcb5f3ca in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#24 0x564a070400d3 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:698:10  

#25 0x564a0704278f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1232:10  

#26 0x564a070421a6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1091:12  

#27 0x564a0703c0d4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:342:36  

#28 0x564a0703c682 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:370:10  

#29 0x5649f7a65c50 in ChromeMain ./../../chrome/app/chrome\_main.cc:182:12  

#30 0x7f211afa1082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6020000d0390 is located 0 bytes inside of 16-byte region [0x6020000d0390,0x6020000d03a0)  

freed by thread T0 (chrome) here:  

#0 0x5649f7a63ced in operator delete(void\*) *asan\_rtl*:3  

#1 0x5649fd44aeca in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#2 0x5649fd44aeca in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#3 0x5649fd44aeca in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#4 0x5649fd44aeca in ~InterfacePtrState ./../../mojo/public/cpp/bindings/lib/interface\_ptr\_state.h:140:32  

#5 0x5649fd44aeca in mojo::Remote[network::mojom::NetworkContext](javascript:void(0);)::reset() ./../../mojo/public/cpp/bindings/remote.h:216:3  

#6 0x5649fdb69dae in content::StoragePartitionImpl::InitNetworkContext() ./../../content/browser/storage\_partition\_impl.cc:2905:20  

#7 0x564a094dc4d3 in Run ./../../base/callback.h:145:12  

#8 0x564a094dc4d3 in mojo::InterfaceEndpointClient::NotifyError(absl::optional[mojo::DisconnectReason](javascript:void(0);) const&) ./../../mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:725:31  

#9 0x564a094f8d13 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:1016:13  

#10 0x564a094f36b1 in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:929:15  

#11 0x564a094f0b6f in mojo::internal::MultiplexRouter::OnPipeConnectionError(bool) ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:839:3  

#12 0x564a094cf8e1 in Run ./../../base/callback.h:145:12  

#13 0x564a094cf8e1 in mojo::Connector::HandleError(bool, bool) ./../../mojo/public/cpp/bindings/lib/connector.cc:688:44  

#14 0x5649fb493102 in base::RepeatingCallback<void (unsigned int)>::Run(unsigned int) const & ./../../base/callback.h:267:12  

#15 0x564a08a368cd in base::RepeatingCallback<void (unsigned int, mojo::HandleSignalsState const&)>::Run(unsigned int, mojo::HandleSignalsState const&) const & ./../../base/callback.h:267:12  

#16 0x564a08a3652d in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) ./../../mojo/public/cpp/system/simple\_watcher.cc:278:14  

#17 0x564a072f975c in Run ./../../base/callback.h:145:12  

#18 0x564a072f975c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:133:32  

#19 0x564a0733e900 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:442:29)> ./../../base/task/common/task\_annotator.h:72:5  

#20 0x564a0733e900 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:440:21  

#21 0x564a0733da0d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:296:30  

#22 0x564a0733fb74 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#23 0x564a07451f58 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:293:55  

#24 0x564a07340625 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:599:12  

#25 0x564a0728edd9 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#26 0x5649fcb64f4c in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1046:18  

#27 0x5649fcb69dbb in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:157:15  

#28 0x5649fcb5f3ca in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#29 0x564a070400d3 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:698:10  

#30 0x564a0704278f in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1232:10  

#31 0x564a070421a6 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1091:12  

#32 0x564a0703c0d4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:342:36  

#33 0x564a0703c682 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:370:10  

#34 0x5649f7a65c50 in ChromeMain ./../../chrome/app/chrome\_main.cc:182:12  

#35 0x7f211afa1082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:  

#0 0x5649f7a6348d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x5649fd44b6df in make\_unique<network::mojom::NetworkContextProxy, mojo::InterfaceEndpointClient \*> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:670:26  

#2 0x5649fd44b6df in mojo::internal::InterfacePtrState[network::mojom::NetworkContext](javascript:void(0);)::ConfigureProxyIfNecessary() ./../../mojo/public/cpp/bindings/lib/interface\_ptr\_state.h:267:16  

#3 0x5649fd44c876 in mojo::Remote[network::mojom::NetworkContext](javascript:void(0);)::BindNewPipeAndPassReceiver(scoped\_refptr[base::SequencedTaskRunner](javascript:void(0);)) ./../../mojo/public/cpp/bindings/remote.h:248:5  

#4 0x5649fdb69dbf in BindNewPipeAndPassReceiver ./../../mojo/public/cpp/bindings/remote.h:237:12  

#5 0x5649fdb69dbf in content::StoragePartitionImpl::InitNetworkContext() ./../../content/browser/storage\_partition\_impl.cc:2907:24  

#6 0x5649fdb693c4 in content::StoragePartitionImpl::GetNetworkContext() ./../../content/browser/storage\_partition\_impl.cc:1423:5  

#7 0x5649fdbd8c2b in content::URLLoaderFactoryGetter::HandleNetworkFactoryRequestOnUIThread(mojo::PendingReceiver[network::mojom::URLLoaderFactory](javascript:void(0);), bool) ./../../content/browser/url\_loader\_factory\_getter.cc:304:15  

#8 0x5649fdbd8858 in content::URLLoaderFactoryGetter::Initialize(content::StoragePartitionImpl\*) ./../../content/browser/url\_loader\_factory\_getter.cc:143:3  

#9 0x5649fdb66527 in content::StoragePartitionImpl::Initialize(content::StoragePartitionImpl\*) ./../../content/browser/storage\_partition\_impl.cc:1291:31  

#10 0x5649fdb941d4 in content::StoragePartitionImplMap::Get(content::StoragePartitionConfig const&, bool) ./../../content/browser/storage\_partition\_impl\_map.cc:351:14  

#11 0x5649fcae3989 in content::BrowserContext::GetStoragePartition(content::StoragePartitionConfig const&, bool) ./../../content/browser/browser\_context.cc:138:52  

#12 0x5649fcae423a in content::BrowserContext::GetDefaultStoragePartition() ./../../content/browser/browser\_context.cc:190:10  

#13 0x564a0edd10ae in OptimizationGuideKeyedService::Initialize() ./../../chrome/browser/optimization\_guide/optimization\_guide\_keyed\_service.cc:156:35  

#14 0x564a0edd0d4f in OptimizationGuideKeyedServiceFactory::BuildServiceInstanceFor(content::BrowserContext\*) const ./../../chrome/browser/optimization\_guide/optimization\_guide\_keyed\_service\_factory.cc:54:14  

#15 0x564a0ac0a494 in KeyedServiceFactory::GetServiceForContext(void\*, bool) ./../../components/keyed\_service/core/keyed\_service\_factory.cc:93:15  

#16 0x564a0ac0371d in DependencyManager::CreateContextServices(void\*, bool) ./../../components/keyed\_service/core/dependency\_manager.cc:0:0  

#17 0x564a10504579 in BrowserContextDependencyManager::DoCreateBrowserContextServices(content::BrowserContext\*, bool) ./../../components/keyed\_service/content/browser\_context\_dependency\_manager.cc:46:22  

#18 0x564a0f015033 in ProfileImpl::OnLocaleReady(Profile::CreateMode) ./../../chrome/browser/profiles/profile\_impl.cc:1148:51  

#19 0x564a0f00fb98 in ProfileImpl::OnPrefsLoaded(Profile::CreateMode, bool) ./../../chrome/browser/profiles/profile\_impl.cc:1176:5  

#20 0x564a0f00e8a2 in ProfileImpl::ProfileImpl(base::FilePath const&, Profile::Delegate\*, Profile::CreateMode, base::Time, scoped\_refptr[base::SequencedTaskRunner](javascript:void(0);)) ./../../chrome/browser/profiles/profile\_impl.cc:532:5  

#21 0x564a0f00c858 in Profile::CreateProfile(base::FilePath const&, Profile::Delegate\*, Profile::CreateMode) ./../../chrome/browser/profiles/profile\_impl.cc:367:59  

#22 0x564a0f062f75 in ProfileManager::CreateAndInitializeProfile(base::FilePath const&) ./../../chrome/browser/profiles/profile\_manager.cc:1914:38  

#23 0x564a0f061d79 in ProfileManager::GetProfile(base::FilePath const&) ./../../chrome/browser/profiles/profile\_manager.cc:791:10  

#24 0x564a0f0626e4 in ProfileManager::CreateInitialProfile() ./../../chrome/browser/profiles/profile\_manager.cc:766:24  

#25 0x564a0ea18165 in CreateInitialProfile ./../../chrome/browser/chrome\_browser\_main.cc:413:19  

#26 0x564a0ea18165 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome\_browser\_main.cc:1572:37  

#27 0x564a0ea178dc in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1164:18  

#28 0x564a047e7a26 in ash::ChromeBrowserMainPartsAsh::PreMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:815:39  

#29 0x5649fcb63150 in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser\_main\_loop.cc:950:28  

#30 0x5649fdb61362 in Run ./../../base/callback.h:145:12  

#31 0x5649fdb61362 in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup\_task\_runner.cc:43:29  

#32 0x5649fcb6275c in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser\_main\_loop.cc:861:25  

#33 0x5649fcb695b1 in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser\_main\_runner\_impl.cc:136:15

SUMMARY: AddressSanitizer: heap-use-after-free (/home/fuzz/chromium\_version/latest\_asan/chrome+0x1c1092c7) (BuildId: 1824ccec45c5251a)  

Shadow bytes around the buggy address:  

0x6020000d0100: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fd  

0x6020000d0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fd fd  

0x6020000d0200: fa fa fa fa fa fa fd fd fa fa fd fd fa fa fd fa  

0x6020000d0280: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x6020000d0300: fa fa 00 fa fa fa fd fd fa fa fd fd fa fa fd fa  

=>0x6020000d0380: fa fa[fd]fd fa fa fd fa fa fa fd fa fa fa fd fa  

0x6020000d0400: fa fa fd fa fa fa 00 fa fa fa fd fd fa fa fd fd  

0x6020000d0480: fa fa fd fa fa fa fd fa fa fa fa fa fa fa fa fa  

0x6020000d0500: fa fa fd fd fa fa fa fa fa fa fd fd fa fa fa fa  

0x6020000d0580: fa fa fa fa fa fa fa fa fa fa fd fd fa fa fa fa  

0x6020000d0600: fa fa fd fd fa fa fa fa fa fa fa fa fa fa fa fa  

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

==22860==ABORTING

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 422 B)
- [background.js](attachments/background.js) (text/plain, 567 B)
- [injection.js](attachments/injection.js) (text/plain, 1.1 KB)

## Timeline

### 0x...@gmail.com (2022-09-20)

It seems that the sendFeedbackReport will call the network_diagnostics function and cause the UAF.
The fuzz testcase is in the attachments but it seems cannot reproduce this UAF.

### [Deleted User] (2022-09-20)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2022-09-20)

Although I cannot manually reproduce this issue, the same testcase cause a lof of the same UAF crashes in my fuzzer.

### aj...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### ps...@google.com (2022-09-21)

khegde@ - assigning to you since you are the owner of network diagnostics. Please re-route as needed.

[Monorail components: Platform>Apps>Diagnostics>Connectivity]

### [Deleted User] (2022-09-21)

[Empty comment from Monorail migration]

### ps...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-22)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-22)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kh...@google.com (2022-09-22)

The culprit is very likely this part:

void DnsResolutionRoutine::CreateHostResolver() {
  host_resolver_.reset();
  network_context()->CreateHostResolver(
      net::DnsConfigOverrides(), host_resolver_.BindNewPipeAndPassReceiver());
}

void DnsResolutionRoutine::OnMojoConnectionError() {
  CreateHostResolver();
  OnComplete(net::ERR_NAME_NOT_RESOLVED, net::ResolveErrorInfo(net::ERR_FAILED),
             /*resolved_addresses=*/absl::nullopt,
             /*endpoint_results_with_metadata=*/absl::nullopt);
}

On a Mojo connection error, we make yet another Mojo call "network_context()->CreateHostResolver(...". Making a call on the corrupted connection could be causing the issue. The fix is only reset "host_resolver_" (cleanup purposes). 

This is also affecting dns_latency_routine.cc, which I will fix as well.

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-07)

khegde: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2022-10-18)

Any updates here Kartik? This is a bit out of SLO now.

### kh...@google.com (2022-10-19)

Apologies, got a bit distracted by some other work and dropped this. The change is in progress. Will send out a CL soon. 

### gi...@appspot.gserviceaccount.com (2022-10-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf88f513d8b905fc0ba060d2ced7a6b1c9c0ada6

commit cf88f513d8b905fc0ba060d2ced7a6b1c9c0ada6
Author: Kartik Hegde <khegde@chromium.org>
Date: Thu Oct 20 21:43:58 2022

network_diagnostics: Fix broken cleanup process

BUG=crbug.com/1365945
TEST=./out/Default/unit_tests --gtest_filter=HttpsLatencyRoutineTest.*
./out/Default/unit_tests --gtest_filter=DnsLatencyRoutineTest.*
./out/Default/unit_tests --gtest_filter=DnsResolutionRoutineTest.*

Change-Id: I78e1cfd5f63ac0223fde24bafc18d4632df206ad
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3969477
Quick-Run: Kartik Hegde <khegde@chromium.org>
Commit-Queue: Steven Bennetts <stevenjb@chromium.org>
Auto-Submit: Kartik Hegde <khegde@chromium.org>
Commit-Queue: Kartik Hegde <khegde@chromium.org>
Reviewed-by: Steven Bennetts <stevenjb@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1061831}

[modify] https://crrev.com/cf88f513d8b905fc0ba060d2ced7a6b1c9c0ada6/chrome/browser/ash/net/network_diagnostics/dns_latency_routine.cc
[modify] https://crrev.com/cf88f513d8b905fc0ba060d2ced7a6b1c9c0ada6/chrome/browser/ash/net/network_diagnostics/https_latency_routine.cc
[modify] https://crrev.com/cf88f513d8b905fc0ba060d2ced7a6b1c9c0ada6/chrome/browser/ash/net/network_diagnostics/dns_resolution_routine.cc


### kh...@google.com (2022-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-21)

Requesting merge to dev M108 because latest trunk commit (1061831) appears to be after dev branch point (1058933).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-21)

Merge review required: M108 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations, asnine! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### ob...@google.com (2022-11-04)

Approved for M-108.

### [Deleted User] (2022-11-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1365945?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-10-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061060)*
