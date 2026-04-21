# Security: heap-use-after-free chrome/browser/profiles/profile_destroyer.cc:137:16 (chromeOS)

| Field | Value |
|-------|-------|
| **Issue ID** | [40059994](https://issues.chromium.org/issues/40059994) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2022-06-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This issue need to install extensions from issue #1297404 and UaF on linux-chromeOS

**VERSION**  

Chrome Version: Chromium 105.0.5126.0  

Operating System: linux-chromeOS

**REPRODUCTION CASE**  

enable dual display  

(1) Install extensions  

(2) wait ~5sec then sign-out with CTRL + Q (2 times). In real devices, after logout, will redirect to login page.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==3818072==ERROR: AddressSanitizer: heap-use-after-free on address 0x6110005a0180 at pc 0x562e4b1e49c7 bp 0x7ffdd28879d0 sp 0x7ffdd28879c8  

READ of size 8 at 0x6110005a0180 thread T0 (chrome)  

SCARINESS: 51 (8-byte-read-heap-use-after-free)  

#0 0x562e4b1e49c6 in ProfileDestroyer::DestroyProfileNow(Profile\*) chrome/browser/profiles/profile\_destroyer.cc:137:16  

#1 0x562e4b1e4a56 in Timeout chrome/browser/profiles/profile\_destroyer.cc:296:3  

#2 0x562e4b1e4a56 in ProfileDestroyer::DestroyPendingProfilesForShutdown() chrome/browser/profiles/profile\_destroyer.cc:105:16  

#3 0x562e4b227589 in ProfileManager::~ProfileManager() chrome/browser/profiles/profile\_manager.cc:556:3  

#4 0x562e4b21423f in ProfileManager::~ProfileManager() chrome/browser/profiles/profile\_manager.cc:527:35  

#5 0x562e4ac15224 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#6 0x562e4ac15224 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#7 0x562e4ac15224 in BrowserProcessImpl::StartTearDown() chrome/browser/browser\_process\_impl.cc:452:22  

#8 0x562e4ac11ead in ChromeBrowserMainParts::PostMainMessageLoopRun() chrome/browser/chrome\_browser\_main.cc:1901:21  

#9 0x562e3ccf8a29 in ash::ChromeBrowserMainPartsAsh::PostMainMessageLoopRun() chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1565:32  

#10 0x562e39b4cb4b in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() content/browser/browser\_main\_loop.cc:1078:13  

#11 0x562e39b50b91 in content::BrowserMainRunnerImpl::Shutdown() content/browser/browser\_main\_runner\_impl.cc:184:17  

#12 0x562e39b468dc in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:32:16  

#13 0x562e431d2894 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:678:10  

#14 0x562e431d53f5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1188:10  

#15 0x562e431d484d in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1059:12  

#16 0x562e431ce196 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#17 0x562e431cf502 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#18 0x562e34a201d0 in ChromeMain chrome/app/chrome\_main.cc:182:12  

#19 0x7efed357a082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

0x6110005a0180 is located 0 bytes inside of 232-byte region [0x6110005a0180,0x6110005a0268)  

freed by thread T0 (chrome) here:  

#0 0x562e34a1e26d in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x562e4b1df4b4 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#2 0x562e4b1df4b4 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#3 0x562e4b1df4b4 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#4 0x562e4b1df4b4 in ~pair buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:40:29  

#5 0x562e4b1df4b4 in void std::Cr::allocator\_traits<std::Cr::allocator<std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, void\*>>>::destroy<std::Cr::pair<Profile::OTRProfileID const, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, void, void>(std::Cr::allocator<std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, void\*>>&, std::Cr::pair<Profile::OTRProfileID const, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>\*) buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:319:15  

#6 0x562e4b1e0ff3 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, std::Cr::\_\_map\_value\_compare<Profile::OTRProfileID, std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, std::Cr::less[Profile::OTRProfileID](javascript:void(0);), true>, std::Cr::allocator<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>>>::erase(std::Cr::\_\_tree\_const\_iterator<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, void\*>\*, long>) buildtools/third\_party/libc++/trunk/include/\_\_tree:2425:5  

#7 0x562e4b1e0dc5 in unsigned long std::Cr::\_\_tree<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, std::Cr::\_\_map\_value\_compare<Profile::OTRProfileID, std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>, std::Cr::less[Profile::OTRProfileID](javascript:void(0);), true>, std::Cr::allocator<std::Cr::\_\_value\_type<Profile::OTRProfileID, std::Cr::unique\_ptr<Profile, std::Cr::default\_delete<Profile>>>>>::\_\_erase\_unique[Profile::OTRProfileID](javascript:void(0);)(Profile::OTRProfileID const&) buildtools/third\_party/libc++/trunk/include/\_\_tree:2448:5  

#8 0x562e4b1db500 in erase buildtools/third\_party/libc++/trunk/include/map:1369:25  

#9 0x562e4b1db500 in ProfileImpl::DestroyOffTheRecordProfile(Profile\*) chrome/browser/profiles/profile\_impl.cc:1016:17  

#10 0x562e4b1e4d3d in ProfileDestroyer::DestroyOffTheRecordProfileNow(Profile\*) chrome/browser/profiles/profile\_destroyer.cc:123:34  

#11 0x562e4b1d998f in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile\_impl.cc:896:5  

#12 0x562e4b1da10d in ProfileImpl::~ProfileImpl() chrome/browser/profiles/profile\_impl.cc:857:29  

#13 0x562e4b1e57fb in ProfileDestroyer::DestroyOriginalProfileNow(Profile\*) chrome/browser/profiles/profile\_destroyer.cc:174:3  

#14 0x562e4b1e3b1f in ProfileDestroyer::DestroyProfileWhenAppropriate(Profile\*) chrome/browser/profiles/profile\_destroyer.cc:97:3  

#15 0x562e4b223961 in ProfileManager::ProfileInfo::~ProfileInfo() chrome/browser/profiles/profile\_manager.cc:1784:3  

#16 0x562e4b22abb0 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#17 0x562e4b22abb0 in std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>::reset(ProfileManager::ProfileInfo\*) buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#18 0x562e4b228724 in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#19 0x562e4b228724 in ~pair buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:40:29  

#20 0x562e4b228724 in destroy<std::Cr::pair<const base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >, void, void> buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:319:15  

#21 0x562e4b228724 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::\_\_map\_value\_compare<base::FilePath, std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, std::Cr::less[base::FilePath](javascript:void(0);), true>, std::Cr::allocator<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>>>::destroy(std::Cr::\_\_tree\_node<std::Cr::\_\_value\_type<base::FilePath, std::Cr::unique\_ptr<ProfileManager::ProfileInfo, std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)>>, void\*>\*) buildtools/third\_party/libc++/trunk/include/\_\_tree:1804:9  

#22 0x562e4b227531 in clear buildtools/third\_party/libc++/trunk/include/\_\_tree:1841:5  

#23 0x562e4b227531 in clear buildtools/third\_party/libc++/trunk/include/map:1374:37  

#24 0x562e4b227531 in ProfileManager::~ProfileManager() chrome/browser/profiles/profile\_manager.cc:555:18  

#25 0x562e4b21423f in ProfileManager::~ProfileManager() chrome/browser/profiles/profile\_manager.cc:527:35  

#26 0x562e4ac15224 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#27 0x562e4ac15224 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#28 0x562e4ac15224 in BrowserProcessImpl::StartTearDown() chrome/browser/browser\_process\_impl.cc:452:22  

#29 0x562e4ac11ead in ChromeBrowserMainParts::PostMainMessageLoopRun() chrome/browser/chrome\_browser\_main.cc:1901:21  

#30 0x562e3ccf8a29 in ash::ChromeBrowserMainPartsAsh::PostMainMessageLoopRun() chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1565:32  

#31 0x562e39b4cb4b in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() content/browser/browser\_main\_loop.cc:1078:13  

#32 0x562e39b50b91 in content::BrowserMainRunnerImpl::Shutdown() content/browser/browser\_main\_runner\_impl.cc:184:17  

#33 0x562e39b468dc in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:32:16  

#34 0x562e431d2894 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:678:10  

#35 0x562e431d53f5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1188:10  

#36 0x562e431d484d in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1059:12  

#37 0x562e431ce196 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#38 0x562e431cf502 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#39 0x562e34a201d0 in ChromeMain chrome/app/chrome\_main.cc:182:12  

#40 0x7efed357a082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

previously allocated by thread T0 (chrome) here:  

#0 0x562e34a1da0d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x562e4b1ea8f5 in make\_unique<OffTheRecordProfileImpl, Profile \*&, const Profile::OTRProfileID &> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:717:28  

#2 0x562e4b1ea8f5 in Profile::CreateOffTheRecordProfile(Profile\*, Profile::OTRProfileID const&) chrome/browser/profiles/off\_the\_record\_profile\_impl.cc:636:15  

#3 0x562e4b1dacbf in ProfileImpl::GetOffTheRecordProfile(Profile::OTRProfileID const&, bool) chrome/browser/profiles/profile\_impl.cc:995:7  

#4 0x562e3bc892eb in Profile::GetPrimaryOTRProfile(bool) chrome/browser/profiles/profile.cc:490:10  

#5 0x562e4dc5f333 in extensions::WindowsCreateFunction::Run() chrome/browser/extensions/api/tabs/tabs\_api.cc:626:30  

#6 0x562e3b845b78 in ExtensionFunction::RunWithValidation() extensions/browser/extension\_function.cc:541:10  

#7 0x562e3b84ca69 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, int, base::OnceCallback<void (ExtensionFunction::ResponseType, base::Value::List, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&)>) extensions/browser/extension\_function\_dispatcher.cc:408:15  

#8 0x562e3b84d79c in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker(extensions::mojom::RequestParams const&, int) extensions/browser/extension\_function\_dispatcher.cc:296:3  

#9 0x562e3b89e113 in DispatchToMethodImpl<extensions::ExtensionServiceWorkerMessageFilter \*, void (extensions::ExtensionServiceWorkerMessageFilter::\*)(const extensions::mojom::RequestParams &), std::Cr::tuple[extensions::mojom::RequestParams](javascript:void(0);), 0UL> base/tuple.h:52:3  

#10 0x562e3b89e113 in DispatchToMethod<extensions::ExtensionServiceWorkerMessageFilter \*, void (extensions::ExtensionServiceWorkerMessageFilter::\*)(const extensions::mojom::RequestParams &), std::Cr::tuple[extensions::mojom::RequestParams](javascript:void(0);) > base/tuple.h:60:3  

#11 0x562e3b89e113 in DispatchToMethod<extensions::ExtensionServiceWorkerMessageFilter, void (extensions::ExtensionServiceWorkerMessageFilter::\*)(const extensions::mojom::RequestParams &), void, std::Cr::tuple[extensions::mojom::RequestParams](javascript:void(0);) > ipc/ipc\_message\_templates.h:53:3  

#12 0x562e3b89e113 in bool IPC::MessageT<ExtensionHostMsg\_RequestWorker\_Meta, std::Cr::tuple[extensions::mojom::RequestParams](javascript:void(0);), void>::Dispatch<extensions::ExtensionServiceWorkerMessageFilter, extensions::ExtensionServiceWorkerMessageFilter, void, void (extensions::ExtensionServiceWorkerMessageFilter::\*)(extensions::mojom::RequestParams const&)>(IPC::Message const\*, extensions::ExtensionServiceWorkerMessageFilter\*, extensions::ExtensionServiceWorkerMessageFilter\*, void\*, void (extensions::ExtensionServiceWorkerMessageFilter::\*)(extensions::mojom::RequestParams const&)) ipc/ipc\_message\_templates.h:141:7  

#13 0x562e3b89dce3 in extensions::ExtensionServiceWorkerMessageFilter::OnMessageReceived(IPC::Message const&) extensions/browser/extension\_service\_worker\_message\_filter.cc:111:5  

#14 0x562e434908f6 in Run base/callback.h:143:12  

#15 0x562e434908f6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:135:32  

#16 0x562e434d2061 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:410:29)> base/task/common/task\_annotator.h:74:5  

#17 0x562e434d2061 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:408:21  

#18 0x562e434d1468 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:286:41  

#19 0x562e434d2e31 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#20 0x562e435d8d99 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_libevent.cc:195:55  

#21 0x562e434d3650 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:535:12  

#22 0x562e433fff8f in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#23 0x562e39b4c6a2 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser\_main\_loop.cc:1039:18  

#24 0x562e39b50a8b in content::BrowserMainRunnerImpl::Run() content/browser/browser\_main\_runner\_impl.cc:157:15  

#25 0x562e39b468aa in content::BrowserMain(content::MainFunctionParams) content/browser/browser\_main.cc:30:28  

#26 0x562e431d2894 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:678:10  

#27 0x562e431d53f5 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content\_main\_runner\_impl.cc:1188:10  

#28 0x562e431d484d in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1059:12  

#29 0x562e431ce196 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:407:36  

#30 0x562e431cf502 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:435:10  

#31 0x562e34a201d0 in ChromeMain chrome/app/chrome\_main.cc:182:12  

#32 0x7efed357a082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/profiles/profile\_destroyer.cc:137:16 in ProfileDestroyer::DestroyProfileNow(Profile\*)  

Shadow bytes around the buggy address:  

0x0c22800abfe0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c22800abff0: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x0c22800ac000: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c22800ac010: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c22800ac020: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c22800ac030:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c22800ac040: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x0c22800ac050: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c22800ac060: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c22800ac070: fd fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c22800ac080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==3818072==ABORTING

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 388 B)
- [service_worker.js](attachments/service_worker.js) (text/plain, 10.1 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-06-17)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-18)

Thanks for the report! +arthursonzogni@, can this UaF be introduced in https://crrev.com/c/3560577? 

Setting severity to medium tentatively, because it requires an extension to install and happens during profile destruction. But it's currently not clear whether the extension is required. If not, the severity should be high. Setting OS to ChromeOS for now, but it is possible that this can be reproduced on other platforms if the root cause is related to the lifetime of the profile that is not specific to ChromeOS.

Reporter, if you can provide the following information, that would be really helpful for us to investigate:
1) Does this reproduce for versions before 105.0.5113.0? This can help us understand whether https://crrev.com/c/3560577 is the root cause.
2) Is installing the extension required? Can this be reproduced by simply tweaking sign-in/sign-out flow? The root cause seems to be related to profiles construction and destruction, but not directly related to extension APIs.

[Monorail components: Services>SignIn]

### [Deleted User] (2022-06-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2022-06-20)

Thanks!

I am not very familiar with ChromeOS/Profile/Extensions ;-(

I tried in debug mode, but it failed differently:
```
ASAN_OPTIONS=detect_odr_violation=0 ./chrome --user-data-dir="$(pwd)/test" --disable-extensions-except="$(pwd)" --load-extension="$(pwd)" --no-first-run --enable-logging=stderr about:blank
```

I got:
```
2022-06-20T10:05:30.188737Z FATAL chrome[3004391:3004391]: [extension_function.cc(479)] Check failed: did_respond() || can_be_destroyed_before_responding(). debugger.sendCommand
#0 0x56138ec71fbb (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/chrome+0x1043bfba)
#1 0x7faade88f73f (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/libbase.so+0xd9573e)
#2 0x7faade142e2d (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/libbase.so+0x648e2c)
#3 0x7faade142ca5 (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/libbase.so+0x648ca4)
#4 0x7faade20d742 (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/libbase.so+0x713741)
#5 0x7faade20e8c9 (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/libbase.so+0x7148c8)
#6 0x7faade081584 (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/libbase.so+0x587583)
#7 0x5613940af7a9 (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/chrome+0x158797a8)
#8 0x5613ab8075d5 (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/chrome+0x2cfd15d4)
#9 0x5613ab80b7d5 (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/chrome+0x2cfd57d4)
#10 0x5613ab80b7f9 (/usr/local/google/home/arthursonzogni/chromium/src/out/lacros/chrome+0x2cfd57f8)

```

I see the failing DCHECK was introduced by:
https://source.chromium.org/chromium/chromium/src/+/fa6359d11a05badd0ae70adbec4596716e803a76

It might be related, or it might deserve its own bug. +karandeepb@, could you please take a look and take the appropriate action, probably opening a bug about it?

I will try again in release mode, to get the ASAN error.

### rh...@gmail.com (2022-06-20)

Sorry for delaying in respond.

xinghuilu@,

>>> 1) Does this reproduce for versions before 105.0.5113.0? This can help us understand whether https://crrev.com/c/3560577 is the root cause.
Yes, it doesn't crash versions before 105.0.5113.0. I think the CL https://crrev.com/c/3560577 did the crash. Please refer to the screencast

>>> 2) Is installing the extension required? Can this be reproduced by simply tweaking sign-in/sign-out flow? 
Yes, install the extensions is required in order to trigger the UaF, I'm currently had no repro steps without installing the extensions. 

>>> The root cause seems to be related to profiles construction and destruction, but not directly related to extension APIs. 
Yes, the symbols is looks like the profiles, not related to presentation API, but presentation API does help to create a profiles. 


arthursonzogni@, I uploading the screencast versions before and after 105.0.5113.0. Also I will test on Ubuntu with dual display later today, to check if it crash on other platforms.

Repro  steps:
(1) Install extensions and pass --ash-host-window-bounds="0+0-1280x800*1,1300+0-1280x800*1" in command line to active dual display.
(2) Active extension and click display 2 after presentation API is fired.
(3) Wait ~3sec and signout.


### rh...@gmail.com (2022-06-20)

running on debug build chromeOS with steps from https://crbug.com/chromium/1337388#c7 , the DCHECK(web_contents)[1] is falling

```
2022-06-20T12:08:12.958094Z FATAL chrome[203176:203176]: [browser_finder.cc(231)] Check failed: web_contents. 
#0 0x7fc1109bd9ff base::debug::CollectStackTrace()
#1 0x7fc11072b9aa base::debug::StackTrace::StackTrace()
#2 0x7fc11072b965 base::debug::StackTrace::StackTrace()
#3 0x7fc1107785b7 logging::LogMessage::~LogMessage()
#4 0x7fc110778d99 logging::LogMessage::~LogMessage()
#5 0x7fc1106e76fb logging::CheckError::~CheckError()
#6 0x55b5c0a19da3 chrome::FindBrowserWithWebContents()
#7 0x55b5c0a234c3 BrowserLiveTabContext::FindContextForWebContents()
#8 0x55b5bf0b7782 extensions::SessionsRestoreFunction::RestoreMostRecentlyClosed()
#9 0x55b5bf0b8442 extensions::SessionsRestoreFunction::Run()

```

```
Browser* FindBrowserWithWebContents(const WebContents* web_contents) {
  DCHECK(web_contents); <-- here
  auto& all_tabs = AllTabContentses();
  auto it = std::find(all_tabs.begin(), all_tabs.end(), web_contents);

  return (it == all_tabs.end()) ? nullptr : it.browser();
}
```

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_finder.cc;l=230-236?q=browser_finder.cc&ss=chromium%2Fchromium%2Fsrc

### ar...@chromium.org (2022-06-20)

We should revert my patch. I will do it soon.
I would to be able to reproduce the issue before moving forward, because without a regression test, we are going to repeat the same things again and again blindly. Also, it seems there are several failing DCHECK, so I suspect we are missing a few here and here.

### ar...@chromium.org (2022-06-20)

I confirm reverting this patch cause the issue not to show up.

Here was my command:
./out/lacros/chrome --ash-debug-shortcuts --ash-dev-shortcuts --ash-host-window-bounds="0+0-1280x800*1,1399+0-1280x800*1" --user-data-dir=/tmp/x6290 --enable-features=DesksTemplates,DesksCloseAll 2>&1 | ~/chromium/src/tools/valgrind/asan/asan_symbolize.py

It will be reverted here:
https://chromium-review.googlesource.com/c/chromium/src/+/3714253

### ar...@chromium.org (2022-06-20)

I added some debug lines.

The OTR profile destruction is requested from both:
- PresentationReceiverWindowController::~PresentationReceiverWindowController via ProfileDestroyer::DestroyProfileWhenAppropriated
- ProfileManager::~ProfileManager() via ProfileDestroyer::DestroyOffTheRecordProfileNow() during shutdown.

So, it looks like the OTR profile lifetime is managed by both the PresentationReceiverWindowController and the ProfileManager without coordination.

nicolaso@ what kind of ownership model is expected for this? Or the one you would like to see instead.

### ni...@chromium.org (2022-06-20)

> PresentationReceiverWindowController::~PresentationReceiverWindowController

OK, so this class creates its own unique OTR profile. This is rather atypical, but there are a couple other call-sites like this [1]. Another likely culprit is DevTools, for instance [2].

> nicolaso@ what kind of ownership model is expected for this?

Classes like PresentationReceiverWindowController should preserve the ability to destroy their Profile early, when they know it's unused (like they're doing now via ProfileDestroyer). This is using resources responsibly.

And ~ProfileManager should ensure that any OTR profiles that *haven't* been destroyed yet, are destroyed. The original CL does that well.

IMO it should be OK to call DestroyProfileWhenAppropriate() method multiple times on the same profile, as it may not succeed immediately. It's easier to allow multiple "destructions" than to keep track of a profile's state in multiple places. The second call should just be a no-op.

You could replace the set<ProfileDestroyer*> with a map<Profile*, ProfileDestroyer*>. That way there's only one PendingDestroyer per profile. Calling DestroyProfileWhenAppropriate() a second time should be a no-op, and calling DestroyProfileNow() should cancel the pending ProfileDestroyer on that profile.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile.h;l=93-105;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/devtools_browser_context_manager.cc;l=91;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4

### ar...@chromium.org (2022-06-22)

It got reverted in:
https://chromium-review.googlesource.com/c/chromium/src/+/3714253

Version: 105.0.5135.0

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cf2ba42acf6977eb009c5d93625d343e6dce6eed

commit cf2ba42acf6977eb009c5d93625d343e6dce6eed
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Thu Jun 23 14:11:33 2022

Reland "Unify/Correct ProfileDestroyer implementation."

It got reverted in:
https://chromium-review.googlesource.com/c/chromium/src/+/3714253

The problem was that an OTR profile destruction is requested from two
locations:
-PresentationReceiverWindowController::~PresentationReceiverWindowController
- ProfileManager::~ProfileManager()

To solve this, we follow @nicolaso advice:
https://bugs.chromium.org/p/chromium/issues/detail?id=1337388#c12

We allow two requests to destroy the same profile. The first request
is canceled and replaced by the new one.

See the diff in between patchset 1 and N for what has been added in the reland:
https://chromium-review.googlesource.com/c/chromium/src/+/3714294/1..2

> Unify/Correct ProfileDestroyer implementation.
>
> This patch is a dependency of:
> https://chromium-review.googlesource.com/c/chromium/src/+/3620393/1
> were WebContents destruction are going to be deferred into a new task.
>
> The ProfileDestroyer currently has several problems:
> 1. Depending on whether the profile is an incognito one or not,
>    the profile is either destroyed immediately or we wait for the
>    associated RenderProcessHost to shutdown first.
> 2. The ProfileDestroyer assert there are no remaining RenderProcessHost
>    associated with a Profile. However, (1) do not provide this
>    guarantee for non-incognito profiles.
> 3. The implementation doesn't wait for RenderProcess Shutdown when they
>    have been added in between calling the ProfileDestroyer and
>    destroying the profile.
>
> This patch unify the Incognito/Normal profile destruction. It also make
> the ProfileDestroyer to take into account new RenderProcessHost.
>
> Change-Id: Ia28f384502bfd57466fca94a0234e325984139ef
> Bug: 1308391,1311962
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3560577


Bug: 1308391,1311962,1337388
Change-Id: I4963c99b47ac125a5a30dcbcabe096dc3718cae6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3714294
Reviewed-by: David Roger <droger@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1017147}

[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/profiles/profile_destroyer.cc
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/profiles/profile_manager.cc
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/test/base/testing_profile_manager.cc
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/ui/views/bubble/webui_bubble_manager_unittest.cc
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/browser_process_impl.h
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/profiles/profile_destroyer.h
[modify] https://crrev.com/cf2ba42acf6977eb009c5d93625d343e6dce6eed/chrome/browser/profiles/profile_destroyer_unittest.cc


### [Deleted User] (2022-07-22)

Not requesting merge to dev (M105) because latest trunk commit (1017147) appears to be prior to dev branch point (1027018). If this is incorrect, please replace the Merge-NA-105 label with Merge-Request-105. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-29)

Congratulations, Rheza. The VRP Panel has decided to award you $1,000 for this report. The reward amount was decided upon due to this issue being highly mitigated by not being remote exploitable, reliant on profile destruction, and the high degree of user interaction required. Thank you for your efforts and reporting this issue to us.

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1337388?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059994)*
