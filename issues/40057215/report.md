# Security:  Use After Free in FileSystemAccessManagerImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40057215](https://issues.chromium.org/issues/40057215) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2021-09-09 |
| **Bounty** | $15,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

In class FileSystemAccessManagerImpl, there is a raw pointer:

"""  

FileSystemAccessPermissionContext\* permission\_context\_;  

"""

`permission_context_` is owned by StoragePartitionImpl, on the other hand, FileSystemAccessManagerImpl is owned by StoragePartitionImpl too from annotation(in face it is NOT):

"""  

// This is the browser side implementation of the  

// FileSystemAccessManager mojom interface. This is the main entry point for  

// the File System Access API in the browser process.Instances of this class are  

// owned by StoragePartitionImpl.  

"""

So in normal situation, the raw pointer `permission_context_` in FileSystemAccessManagerImpl is safe. But FileSystemAccessManagerImpl is a RefCountedThreadSafe object so in special situation, we can add ref to it and outlives of StoragePartitionImpl, and the raw pointer `permission_context_` becomes dangling pointer.

In function `FileSystemAccessManagerImpl::DidVerifySensitiveDirectoryAccess`, there are some `base::BindOnce` call with argument `this`, this will add ref of FileSystemAccessManagerImpl.

"""  

operation\_runner().PostTaskWithThisObject(  

FROM\_HERE,  

base::BindOnce(  

&CreateAndTruncateFile, fs\_url,  

base::BindOnce(  

&FileSystemAccessManagerImpl::DidCreateAndTruncateSaveFile,  

this, binding\_context, entries.front(), fs\_url,  

std::move(callback)),  

base::SequencedTaskRunnerHandle::Get()));  

"""

So consider below situation, uaf will happen:

1. call above BindOnce function, ref count is 2, and then post task DidCreateAndTruncateSaveFile.
2. call ~StoragePartitionImpl, frees FileSystemAccessPermissionContext, and `permission_context_` becomes dangling pointer, FileSystemAccessManagerImpl's ref count is 1 so it still lives.
3. call `DidCreateAndTruncateSaveFile` => `GetSharedHandleStateForPath` => `permission_context_->GetReadPermissionGrant` and uaf happens.

how to reproduce:  

$python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/Debug/gen  

$out/Debug/chrome --enable-blink-features=MojoJS 127.0.0.1:8000/1.html  

$click trigger, wait about 4-8 seconds(it need to race here and depend on hardware, so may be it is not stable to reproduce, if you can't, change the time here), and click confirm save file.

The fix:  

I think the FileSystemAccessManagerImpl need to create a `Shutdown` function like FileSystemContext and ~StoragePartitionImpl will call it. In `Shutdown` function, it will clear the raw pointer `permission_context_`. There are many places like `if (permission_context_)` in FileSystemAccessManagerImpl's methods, so I think you may be forget to create a `Shuntdown` function for FileSystemAccessManagerImpl.

\*Please note that this bug may be can trigger with normal render process(not compromised) as the mojo interfaces can be called from web API. I use MojoJS just a convenience and for race more stable. It is not necessary.

As it need to race to trigger the bug, so may be it is not stable to reproduce, please try more times. But the bug is clear in code.

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash:browser  

Crash State:  

==780772==ERROR: AddressSanitizer: heap-use-after-free on address 0x12195242be40 at pc 0x7ff82e6009cf bp 0x00076f1fe7c0 sp 0x00076f1fe808  

READ of size 8 at 0x12195242be40 thread T0  

#0 0x7ff82e6009ce in content::FileSystemAccessManagerImpl::GetSharedHandleStateForPath(class base::FilePath const &, class url::Origin const &, enum content::FileSystemAccessPermissionContext::HandleType, enum content::FileSystemAccessPermissionContext::UserAction) src\content\browser\file\_system\_access\file\_system\_access\_manager\_impl.cc:1377:39  

#1 0x7ff82e60a5e4 in content::FileSystemAccessManagerImpl::DidCreateAndTruncateSaveFile(struct content::FileSystemAccessEntryFactory::BindingContext const &, struct content::FileSystemChooser::ResultEntry const &, class storage::FileSystemURL const &, class base::OnceCallback<(class mojo::InlinedStructPtr<class blink::mojom::FileSystemAccessError>, class std::\_\_1::vector<class mojo::StructPtr<class blink::mojom::FileSystemAccessEntry>, class std::\_\_1::allocator<class mojo::StructPtr<class blink::mojom::FileSystemAccessEntry>>>)>, bool) src\content\browser\file\_system\_access\file\_system\_access\_manager\_impl.cc:1253:43  

#2 0x7ff82e61de3e in base::internal::FunctorTraits<void (content::FileSystemAccessManagerImpl::\*)(const content::FileSystemAccessEntryFactory::BindingContext &, const content::FileSystemChooser::ResultEntry &, const storage::FileSystemURL &, base::OnceCallback<void (mojo::InlinedStructPtr[blink::mojom::FileSystemAccessError](javascript:void(0);), std::\_\_1::vector<mojo::StructPtr[blink::mojom::FileSystemAccessEntry](javascript:void(0);),std::\_\_1::allocator<mojo::StructPtr[blink::mojom::FileSystemAccessEntry](javascript:void(0);) > >)>, bool),void>::Invoke src\base\bind\_internal.h:509  

#3 0x7ff82e61de3e in base::internal::InvokeHelper<0,void>::MakeItSo src\base\bind\_internal.h:648  

#4 0x7ff82e61de3e in base::internal::Invoker<base::internal::BindState<void (content::FileSystemAccessManagerImpl::\*)(const content::FileSystemAccessEntryFactory::BindingContext &, const content::FileSystemChooser::ResultEntry &, const storage::FileSystemURL &, base::OnceCallback<void (mojo::InlinedStructPtr[blink::mojom::FileSystemAccessError](javascript:void(0);), std::\_\_1::vector<mojo::StructPtr[blink::mojom::FileSystemAccessEntry](javascript:void(0);),std::\_\_1::allocator<mojo::StructPtr[blink::mojom::FileSystemAccessEntry](javascript:void(0);) > >)>, bool),scoped\_refptr[content::FileSystemAccessManagerImpl](javascript:void(0);),content::FileSystemAccessEntryFactory::BindingContext,content::FileSystemChooser::ResultEntry,storage::FileSystemURL,base::OnceCallback<void (mojo::InlinedStructPtr[blink::mojom::FileSystemAccessError](javascript:void(0);), std::\_\_1::vector<mojo::StructPtr[blink::mojom::FileSystemAccessEntry](javascript:void(0);),std::\_\_1::allocator<mojo::StructPtr[blink::mojom::FileSystemAccessEntry](javascript:void(0);) > >)> >,void (bool)>::RunImpl src\base\bind\_internal.h:721  

#5 0x7ff82e61de3e in base::internal::Invoker<struct base::internal::BindState<void (\_\_cdecl content::FileSystemAccessManagerImpl::\*)(struct content::FileSystemAccessEntryFactory::BindingContext const &, struct content::FileSystemChooser::ResultEntry const &, class storage::FileSystemURL const &, class base::OnceCallback<(class mojo::InlinedStructPtr<class blink::mojom::FileSystemAccessError>, class std::\_\_1::vector<class mojo::StructPtr<class blink::mojom::FileSystemAccessEntry>, class std::\_\_1::allocator<class mojo::StructPtr<class blink::mojom::FileSystemAccessEntry>>>)>, bool), class scoped\_refptr<class content::FileSystemAccessManagerImpl>, struct content::FileSystemAccessEntryFactory::BindingContext, struct content::FileSystemChooser::ResultEntry, class storage::FileSystemURL, class base::OnceCallback<void \_\_cdecl(class mojo::InlinedStructPtr<class blink::mojom::FileSystemAccessError>, class std::\_\_1::vector<class mojo::StructPtr<class blink::mojom::FileSystemAccessEntry>, class std::**1::allocator<class mojo::StructPtr<class blink::mojom::FileSystemAccessEntry>>>)>>, (bool)>::RunOnce(class base::internal::BindStateBase \*, bool) src\base\bind\_internal.h:690:12  

#6 0x7ff829bccdee in base::OnceCallback<(bool)>::Run(bool) && src\base\callback.h:98:12  

#7 0x7ff82bfbf543 in base::internal::FunctorTraits<class base::OnceCallback<(bool)>, void>::Invoke<class base::OnceCallback<(bool)>, bool>(class base::OnceCallback<(bool)> &&, bool &&) src\base\bind\_internal.h:608:49  

#8 0x7ff83689b16c in base::OnceCallback<void ()>::Run src\base\callback.h:99  

#9 0x7ff83689b16c in base::TaskAnnotator::RunTask(char const \*, struct base::PendingTask \*) src\base\task\common\task\_annotator.cc:178:33  

#10 0x7ff839a9ea6a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \*) src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360:23  

#11 0x7ff839a9d44d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260:36  

#12 0x7ff836981779 in base::MessagePumpForUI::DoRunLoop(void) src\base\message\_loop\message\_pump\_win.cc:220:67  

#13 0x7ff83697eaae in base::MessagePumpWin::Run(class base::MessagePump::Delegate \*) src\base\message\_loop\message\_pump\_win.cc:78:3  

#14 0x7ff839aa0ddd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467:12  

#15 0x7ff8368147d5 in base::RunLoop::Run(class base::Location const &) src\base\run\_loop.cc:134:14  

#16 0x7ff82e0f6455 in content::BrowserMainLoop::RunMainMessageLoop(void) src\content\browser\browser\_main\_loop.cc:988:18  

#17 0x7ff82e0fc8b1 in content::BrowserMainRunnerImpl::Run(void) src\content\browser\browser\_main\_runner\_impl.cc:152:15  

#18 0x7ff82e0eec68 in content::BrowserMain(struct content::MainFunctionParams const &) src\content\browser\browser\_main.cc:49:28  

#19 0x7ff83141708d in content::RunBrowserProcessMain(struct content::MainFunctionParams const &, class content::ContentMainDelegate \*) src\content\app\content\_main\_runner\_impl.cc:608:10  

#20 0x7ff83141a190 in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams &, bool) src\content\app\content\_main\_runner\_impl.cc:1104:10  

#21 0x7ff8314191cc in content::ContentMainRunnerImpl::Run(bool) src\content\app\content\_main\_runner\_impl.cc:971:12  

#22 0x7ff83141555f in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner \*) src\content\app\content\_main.cc:390:36  

#23 0x7ff8314165cc in content::ContentMain(struct content::ContentMainParams const &) src\content\app\content\_main.cc:418:10  

#24 0x7ff8297a14a7 in ChromeMain src\chrome\app\chrome\_main.cc:172:12  

#25 0x7ff6221c7858 in MainDllLoader::Launch(struct HINSTANCE**\*, class base::TimeTicks) src\chrome\app\main\_dll\_loader\_win.cc:169:12  

#26 0x7ff6221c33a4 in main src\chrome\app\chrome\_exe\_main\_win.cc:382:20  

#27 0x7ff6226c88df in invoke\_main d:\a01\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:78  

#28 0x7ff6226c88df in \_\_scrt\_common\_main\_seh d:\a01\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#29 0x7ff93ef87033 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#30 0x7ff940b22650 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x12195242be40 is located 0 bytes inside of 448-byte region [0x12195242be40,0x12195242c000)  

freed by thread T0 here:  

#0 0x7ff62227943b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff8429173ea in [thunk]: ChromeFileSystemAccessPermissionContext::`vector deleting dtor'`adjustor{8}'(unsigned int) (src\out\ASAN\_8\_14\chrome.dll+0x1991773ea)  

#2 0x7ff82d37b8bc in std::\_\_1::default\_delete[gpu::gles2::AbstractTexture](javascript:void(0);)::operator() src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:54  

#3 0x7ff82d37b8bc in std::\_\_1::unique\_ptr<gpu::gles2::AbstractTexture,std::\_\_1::default\_delete[gpu::gles2::AbstractTexture](javascript:void(0);) >::reset src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:315  

#4 0x7ff82d37b8bc in std::\_\_1::unique\_ptr<gpu::gles2::AbstractTexture,std::\_\_1::default\_delete[gpu::gles2::AbstractTexture](javascript:void(0);) >::~unique\_ptr src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:269  

#5 0x7ff82d37b8bc in std::\_\_1::pair<const unsigned int,std::\_\_1::unique\_ptr<gpu::gles2::AbstractTexture,std::\_\_1::default\_delete[gpu::gles2::AbstractTexture](javascript:void(0);) > >::~pair src\buildtools\third\_party\libc++\trunk\include\utility:394  

#6 0x7ff82d37b8bc in std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<unsigned int,std::\_\_1::unique\_ptr<gpu::gles2::AbstractTexture,std::\_\_1::default\_delete[gpu::gles2::AbstractTexture](javascript:void(0);) > >,void \*> > >::destroy src\buildtools\third\_party\libc++\trunk\include\_\_memory\allocator\_traits.h:318  

#7 0x7ff82d37b8bc in std::\_\_1::\_\_tree<struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>, class std::\_\_1::\_\_map\_value\_compare<unsigned \_\_int64, struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>, struct std::\_\_1::less<unsigned \_\_int64>, 1>, class std::\_\_1::allocator<struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>>>::erase(class std::\_\_1::\_\_tree\_const\_iterator<struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>, class std::\_\_1::\_\_tree\_node<struct std::\_\_1::\_\_value\_type<unsigned \_\_int64, class std::\_\_1::unique\_ptr<class mojo::MessageReceiver, struct std::\_\_1::default\_delete<class mojo::MessageReceiver>>>, void \*> \*, \_\_int64>) src\buildtools\third\_party\libc++\trunk\include\_\_tree:2422:5  

#8 0x7ff837c0289e in std::\_\_1::map<void \*,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService> >,std::\_\_1::less<void \*>,std::\_\_1::allocator<std::\_\_1::pair<void \*const,std::\_\_1::unique\_ptr<KeyedService,std::\_\_1::default\_delete<KeyedService> > > > >::erase src\buildtools\third\_party\libc++\trunk\include\map:1314  

#9 0x7ff837c0289e in KeyedServiceFactory::Disassociate(void \*) src\components\keyed\_service\core\keyed\_service\_factory.cc:97:14  

#10 0x7ff837c02b2e in KeyedServiceFactory::ContextDestroyed(void \*) src\components\keyed\_service\core\keyed\_service\_factory.cc:107:3  

#11 0x7ff83abe7bcb in DependencyManager::DestroyFactoriesInOrder src\components\keyed\_service\core\dependency\_manager.cc:151  

#12 0x7ff83abe7bcb in DependencyManager::PerformInterlockedTwoPhaseShutdown(class DependencyManager \*, void \*, class DependencyManager \*, void \*) src\components\keyed\_service\core\dependency\_manager.cc:127:3  

#13 0x7ff839980a81 in ProfileImpl::~ProfileImpl(void) src\chrome\browser\profiles\profile\_impl.cc:894:3  

#14 0x7ff839985b09 in ProfileImpl::`scalar deleting dtor'(unsigned int) src\chrome\browser\profiles\profile\_impl.cc:850:29  

#15 0x7ff83999b49d in ProfileDestroyer::DestroyOriginalProfileNow(class Profile \*const) src\chrome\browser\profiles\profile\_destroyer.cc:133:3  

#16 0x7ff83999ab4d in ProfileDestroyer::DestroyProfileWhenAppropriate(class Profile \*const) src\chrome\browser\profiles\profile\_destroyer.cc:61:5  

#17 0x7ff83661d992 in ProfileManager::ProfileInfo::~ProfileInfo(void) src\chrome\browser\profiles\profile\_manager.cc:1600:3  

#18 0x7ff8366276cd in std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);)::operator() src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:54  

#19 0x7ff8366276cd in std::\_\_1::unique\_ptr<class ProfileManager::ProfileInfo, struct std::\_\_1::default\_delete<class ProfileManager::ProfileInfo>>::reset(class ProfileManager::ProfileInfo \*) src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:315:7  

#20 0x7ff8366278ac in std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) >::~unique\_ptr src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:269  

#21 0x7ff8366278ac in std::\_\_1::pair<const base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >::~pair src\buildtools\third\_party\libc++\trunk\include\utility:394  

#22 0x7ff8366278ac in std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,void \*> > >::destroy src\buildtools\third\_party\libc++\trunk\include\_\_memory\allocator\_traits.h:318  

#23 0x7ff8366278ac in std::\_\_1::\_\_tree<struct std::\_\_1::\_\_value\_type<class base::FilePath, class std::\_\_1::unique\_ptr<class ProfileManager::ProfileInfo, struct std::\_\_1::default\_delete<class ProfileManager::ProfileInfo>>>, class std::\_\_1::\_\_map\_value\_compare<class base::FilePath, struct std::\_\_1::\_\_value\_type<class base::FilePath, class std::\_\_1::unique\_ptr<class ProfileManager::ProfileInfo, struct std::\_\_1::default\_delete<class ProfileManager::ProfileInfo>>>, struct std::\_\_1::less<class base::FilePath>, 1>, class std::\_\_1::allocator<struct std::\_\_1::\_\_value\_type<class base::FilePath, class std::\_\_1::unique\_ptr<class ProfileManager::ProfileInfo, struct std::\_\_1::default\_delete<class ProfileManager::ProfileInfo>>>>>::erase(class std::\_\_1::\_\_tree\_const\_iterator<struct std::\_\_1::\_\_value\_type<class base::FilePath, class std::\_\_1::unique\_ptr<class ProfileManager::ProfileInfo, struct std::\_\_1::default\_delete<class ProfileManager::ProfileInfo>>>, class std::\_\_1::\_\_tree\_node<struct std::\_\_1::\_\_value\_type<class base::FilePath, class std::\_\_1::unique\_ptr<class ProfileManager::ProfileInfo, struct std::\_\_1::default\_delete<class ProfileManager::ProfileInfo>>>, void \*> \*, \_\_int64>) src\buildtools\third\_party\libc++\trunk\include\_\_tree:2422:5  

#24 0x7ff836627801 in std::\_\_1::\_\_tree<struct std::\_\_1::\_\_value\_type<class base::FilePath, class std::\_\_1::unique\_ptr<class ProfileManager::ProfileInfo, struct std::\_\_1::default\_delete<class ProfileManager::ProfileInfo>>>, class std::\_\_1::\_\_map\_value\_compare<class base::FilePath, struct std::\_\_1::\_\_value\_type<class base::FilePath, class std::\_\_1::unique\_ptr<class ProfileManager::ProfileInfo, struct std::\_\_1::default\_delete<class ProfileManager::ProfileInfo>>>, struct std::\_\_1::less<class base::FilePath>, 1>, class std::\_\_1::allocator<struct std::\_\_1::\_\_value\_type<class base::FilePath, class std::\_\_1::unique\_ptr<class ProfileManager::ProfileInfo, struct std::\_\_1::default\_delete<class ProfileManager::ProfileInfo>>>>>::\_\_erase\_unique<class base::FilePath>(class base::FilePath const &) src\buildtools\third\_party\libc++\trunk\include\_\_tree:2445:5  

#25 0x7ff83661ab63 in std::\_\_1::map<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) >,std::\_\_1::less[base::FilePath](javascript:void(0);),std::\_\_1::allocator<std::\_\_1::pair<const base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::erase src\buildtools\third\_party\libc++\trunk\include\map:1317  

#26 0x7ff83661ab63 in ProfileManager::RemoveProfile(class base::FilePath const &) src\chrome\browser\profiles\profile\_manager.cc:1705:18  

#27 0x7ff83661a7f5 in ProfileManager::DeleteProfileIfNoKeepAlive(class ProfileManager::ProfileInfo const \*) src\chrome\browser\profiles\profile\_manager.cc:1428:3  

#28 0x7ff836619f54 in ProfileManager::RemoveKeepAlive(class Profile const \*, enum ProfileKeepAliveOrigin) src\chrome\browser\profiles\profile\_manager.cc:1390:3  

#29 0x7ff83ba86844 in ScopedProfileKeepAlive::RemoveKeepAliveOnUIThread(class Profile const \*, enum ProfileKeepAliveOrigin) src\chrome\browser\profiles\scoped\_profile\_keep\_alive.cc:44:22  

#30 0x7ff83689b16c in base::OnceCallback<void ()>::Run src\base\callback.h:99  

#31 0x7ff83689b16c in base::TaskAnnotator::RunTask(char const \*, struct base::PendingTask \*) src\base\task\common\task\_annotator.cc:178:33  

#32 0x7ff839a9ea6a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \*) src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360:23  

#33 0x7ff839a9d44d in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(void) src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260:36  

#34 0x7ff836981779 in base::MessagePumpForUI::DoRunLoop(void) src\base\message\_loop\message\_pump\_win.cc:220:67  

#35 0x7ff83697eaae in base::MessagePumpWin::Run(class base::MessagePump::Delegate \*) src\base\message\_loop\message\_pump\_win.cc:78:3  

#36 0x7ff839aa0ddd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467:12  

#37 0x7ff8368147d5 in base::RunLoop::Run(class base::Location const &) src\base\run\_loop.cc:134:14  

#38 0x7ff82e0f6455 in content::BrowserMainLoop::RunMainMessageLoop(void) src\content\browser\browser\_main\_loop.cc:988:18  

#39 0x7ff82e0fc8b1 in content::BrowserMainRunnerImpl::Run(void) src\content\browser\browser\_main\_runner\_impl.cc:152:15  

#40 0x7ff82e0eec68 in content::BrowserMain(struct content::MainFunctionParams const &) src\content\browser\browser\_main.cc:49:28

previously allocated by thread T0 here:  

#0 0x7ff62227953b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff84c28acae in operator new(unsigned \_\_int64) d:\a01\_work\2\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff83d93a25e in FileSystemAccessPermissionContextFactory::BuildServiceInstanceFor(class content::BrowserContext \*) const src\chrome\browser\file\_system\_access\file\_system\_access\_permission\_context\_factory.cc:56:10  

#3 0x7ff838e127ad in BrowserContextKeyedServiceFactory::BuildServiceInstanceFor(void \*) const src\components\keyed\_service\content\browser\_context\_keyed\_service\_factory.cc:95:7  

#4 0x7ff837c01f3f in KeyedServiceFactory::GetServiceForContext(void \*, bool) src\components\keyed\_service\core\keyed\_service\_factory.cc:80:15  

#5 0x7ff83d93a0da in FileSystemAccessPermissionContextFactory::GetForProfile(class content::BrowserContext \*) src\chrome\browser\file\_system\_access\file\_system\_access\_permission\_context\_factory.cc:19:22  

#6 0x7ff82f306830 in content::StoragePartitionImpl::Initialize(class content::StoragePartitionImpl \*) src\content\browser\storage\_partition\_impl.cc:1244:29  

#7 0x7ff82f348c22 in content::StoragePartitionImplMap::Get(class content::StoragePartitionConfig const &, bool) src\content\browser\storage\_partition\_impl\_map.cc:353:14  

#8 0x7ff82e09eb88 in content::BrowserContext::GetStoragePartition(class content::StoragePartitionConfig const &, bool) src\content\browser\browser\_context.cc:145:52  

#9 0x7ff82e09f4ce in content::BrowserContext::GetDefaultStoragePartition(void) src\content\browser\browser\_context.cc:187:10  

#10 0x7ff841a34489 in OptimizationGuideKeyedService::Initialize(void) src\chrome\browser\optimization\_guide\optimization\_guide\_keyed\_service.cc:90:35  

#11 0x7ff841a34083 in OptimizationGuideKeyedService::OptimizationGuideKeyedService(class content::BrowserContext \*) src\chrome\browser\optimization\_guide\optimization\_guide\_keyed\_service.cc:74:3  

#12 0x7ff838e127ad in BrowserContextKeyedServiceFactory::BuildServiceInstanceFor(void \*) const src\components\keyed\_service\content\browser\_context\_keyed\_service\_factory.cc:95:7  

#13 0x7ff837c01f3f in KeyedServiceFactory::GetServiceForContext(void \*, bool) src\components\keyed\_service\core\keyed\_service\_factory.cc:80:15  

#14 0x7ff83abe703c in DependencyManager::CreateContextServices(void \*, bool) src\components\keyed\_service\core\dependency\_manager.cc:87:16  

#15 0x7ff838e11bdc in BrowserContextDependencyManager::DoCreateBrowserContextServices(class content::BrowserContext \*, bool) src\components\keyed\_service\content\browser\_context\_dependency\_manager.cc:46:22  

#16 0x7ff839983637 in ProfileImpl::OnLocaleReady(enum Profile::CreateMode) src\chrome\browser\profiles\profile\_impl.cc:1099:51  

#17 0x7ff83997cbb0 in ProfileImpl::OnPrefsLoaded(enum Profile::CreateMode, bool) src\chrome\browser\profiles\profile\_impl.cc:1140:3  

#18 0x7ff83997a032 in ProfileImpl::ProfileImpl(class base::FilePath const &, class Profile::Delegate \*, enum Profile::CreateMode, class base::Time, class scoped\_refptr<class base::SequencedTaskRunner>) src\chrome\browser\profiles\profile\_impl.cc:554:5  

#19 0x7ff839978f2d in Profile::CreateProfile(class base::FilePath const &, class Profile::Delegate \*, enum Profile::CreateMode) src\chrome\browser\profiles\profile\_impl.cc:382:59  

#20 0x7ff836617cc3 in ProfileManager::CreateProfileHelper(class base::FilePath const &) src\chrome\browser\profiles\profile\_manager.cc:1313:10  

#21 0x7ff83660af21 in ProfileManager::CreateAndInitializeProfile(class base::FilePath const &) src\chrome\browser\profiles\profile\_manager.cc:1743:38  

#22 0x7ff836608150 in ProfileManager::GetProfile(class base::FilePath const &) src\chrome\browser\profiles\profile\_manager.cc:737:10  

#23 0x7ff83ce3799e in GetStartupProfile(class base::FilePath const &, class base::CommandLine const &) src\chrome\browser\ui\startup\startup\_browser\_creator.cc:1534:39  

#24 0x7ff8396c81f0 in `anonymous namespace'::CreatePrimaryProfile src\chrome\browser\chrome\_browser\_main.cc:415:18  

#25 0x7ff8396c4fcd in ChromeBrowserMainParts::PreMainMessageLoopRunImpl(void) src\chrome\browser\chrome\_browser\_main.cc:1403:37  

#26 0x7ff8396c3a9c in ChromeBrowserMainParts::PreMainMessageLoopRun(void) src\chrome\browser\chrome\_browser\_main.cc:1052:18  

#27 0x7ff82e0f40ee in content::BrowserMainLoop::PreMainMessageLoopRun(void) src\content\browser\browser\_main\_loop.cc:938:28

SUMMARY: AddressSanitizer: heap-use-after-free src\content\browser\file\_system\_access\file\_system\_access\_manager\_impl.cc:1377:39 in content::FileSystemAccessManagerImpl::GetSharedHandleStateForPath(class base::FilePath const &, class url::Origin const &, enum content::FileSystemAccessPermissionContext::HandleType, enum content::FileSystemAccessPermissionContext::UserAction)  

Shadow bytes around the buggy address:  

0x04347c885770: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x04347c885780: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x04347c885790: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04347c8857a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04347c8857b0: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

=>0x04347c8857c0: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x04347c8857d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04347c8857e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04347c8857f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04347c885800: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x04347c885810: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==780772==ABORTING

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: SorryMybad(@S0rryMybad) of Kunlun Lab

## Attachments

- [1.html](attachments/1.html) (text/plain, 1.8 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 512 B)

## Timeline

### [Deleted User] (2021-09-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-09-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5709519387426816.

### cl...@chromium.org (2021-09-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5760223623839744.

### ad...@google.com (2021-09-09)

I can't reproduce this (using asan-linux-release-902206 on Linux x64).

It feels to me like your PoC may not be working right in my environment? Or I'm misunderstanding your instructions. The window.close() function doesn't work. Developer tools says "Scripts may close only the windows that were opened by them.". Yet from the stack traces you've provided, this looks like a profile destruction bug.

Also, the inclusion of midi_service.mojom.js appears to be unnecessary?



### ad...@google.com (2021-09-09)

Whilst I can't reproduce this, the description of the root cause behind the UaF is very clear and meets the bar for us to pass this on beyond the security team.

Severity:

Browser process UaF, triggerable via Mojo from renderer process => high severity.

The stack traces provided suggest that this happens on profile destruction only. It shouldn't normally be possible for a website to cause this; the site has to induce the user to close a window (e.g. an Incognito window). Therefore we usually mitigate profile destruction bugs down by a level => rating this medium.

FoundIn: not sure yet. Unfortunately the reporter doesn't specify the exact version they used, so I'm having a hard time matching up line numbers with their stack trace.

### ad...@google.com (2021-09-09)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>FileSystem]

### me...@chromium.org (2021-09-09)

asully: Can you try to fix this? I think the suggested solution (of having some kind of Shutdown method called by StoragePartitionImpl that nulls out the permission context) sounds reasonable.

### ad...@google.com (2021-09-09)

It looks to me like the fundamental ownership stuff in this code hasn't changed since 93.0.4577.63, so marking as FoundIn-93.

### [Deleted User] (2021-09-09)

[Empty comment from Monorail migration]

### so...@gmail.com (2021-09-09)

Re https://crbug.com/chromium/1248030#c5:

The window.close() should be work, I think you misunderstanding my instructions. You need to use "out/Debug/chrome --enable-blink-features=MojoJS  127.0.0.1:8000/1.html" to open the 1.html website and 1.html is the last tab of Chromium, and window.close() should work and close all the processes.

On the other hand, from a compromised window, it is very easy to patch(please note that this is not need if you follow my instructions I said above) the related logic in "void DOMWindow::Close(LocalDOMWindow* incumbent_window)":
"""
diff --git a/third_party/blink/renderer/core/frame/dom_window.cc b/third_party/blink/renderer/core/frame/dom_window.cc
index b52271f53c5e..46b78332a7c6 100644
--- a/third_party/blink/renderer/core/frame/dom_window.cc
+++ b/third_party/blink/renderer/core/frame/dom_window.cc
@@ -364,18 +364,7 @@ void DOMWindow::Close(LocalDOMWindow* incumbent_window) {
   bool allow_scripts_to_close_windows =
       settings && settings->GetAllowScriptsToCloseWindows();

-  if (!page->OpenedByDOM() && GetFrame()->Client()->BackForwardLength() > 1 &&
-      !allow_scripts_to_close_windows) {
-    active_document->domWindow()->GetFrameConsole()->AddMessage(
-        MakeGarbageCollected<ConsoleMessage>(
-            mojom::ConsoleMessageSource::kJavaScript,
-            mojom::ConsoleMessageLevel::kWarning,
-            "Scripts may close only the windows that were opened by them."));
-    return;
-  }
-
-  if (!GetFrame()->ShouldClose())
-    return;
+

   ExecutionContext* execution_context = nullptr;
   if (auto* local_dom_window = DynamicTo<LocalDOMWindow>(this)) {
"""

So I think " It shouldn't normally be possible for a website to cause this; the site has to induce the user to close a window (e.g. an Incognito window). Therefore we usually mitigate profile destruction bugs down by a level => rating this medium." is wrong. This bug should be "Security_Severity-High".

### ad...@google.com (2021-09-09)

[Empty comment from Monorail migration]

### ad...@google.com (2021-09-10)

Re https://crbug.com/chromium/1248030#c10 - OK, I learned today that websites can self-close if they are opened from the command-line. window.close() did indeed work when the site was opened that way. Nevertheless it's not _normally_ possible for a website to close itself, so profile deletion bugs are regarded as somewhat less serious than other UaFs.

As it happens, I still can't reproduce the UaF - Chrome closes normally. But that could be timing anyway.

### so...@gmail.com (2021-09-10)

Re https://crbug.com/chromium/1248030#c12, so from a compromised renderer, it is easy to close itself as we can modify renderer memory and bypass this check I mention in https://crbug.com/chromium/1248030#c10:
"""
if (!page->OpenedByDOM() && GetFrame()->Client()->BackForwardLength() > 1 &&
      !allow_scripts_to_close_windows) {
"""

You still consider it's not _normally_ possible for a website to close itself?

### [Deleted User] (2021-09-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/951339b41022b08a67ad94ba5960b05c84bf4cf2

commit 951339b41022b08a67ad94ba5960b05c84bf4cf2
Author: Austin Sullivan <asully@chromium.org>
Date: Fri Sep 10 21:13:44 2021

FSA: Fix race condition in manager

Bug: 1248030
Change-Id: I1ea819d1d6ac63ec8f400a45c893da49596235ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3154425
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#920376}

[modify] https://crrev.com/951339b41022b08a67ad94ba5960b05c84bf4cf2/content/browser/file_system_access/file_system_access_manager_impl.cc
[modify] https://crrev.com/951339b41022b08a67ad94ba5960b05c84bf4cf2/content/browser/file_system_access/file_system_access_manager_impl.h
[modify] https://crrev.com/951339b41022b08a67ad94ba5960b05c84bf4cf2/content/browser/storage_partition_impl.cc


### as...@chromium.org (2021-09-10)

It looks like both myself and clusterfuzz were unable to reproduce this crash, but the change which just landed should have fixed it. 

@OP: Once this change hits Canary, can you confirm this bug no longer reproduces? (You can check which release this change is in here: https://chromiumdash.appspot.com/commit/951339b41022b08a67ad94ba5960b05c84bf4cf2)

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

Requesting merge to beta M94 because latest trunk commit (920376) appears to be after beta branch point (911515).

Requesting merge to dev M95 because latest trunk commit (920376) appears to be after dev branch point (920003).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-11)

This bug requires manual review: We are only 9 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-12)

Your change meets the bar and is auto-approved for M95. Please go ahead and merge the CL to branch 4638 (refs/branch-heads/4638) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), harrysouders@(iOS), None@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-09-13)

has this been verified on canary? , can you pls answer https://crbug.com/chromium/1248030#c21 for merge review. 

### pb...@google.com (2021-09-13)

Your change has been approved for M95. Please go ahead and merge the CL to branch 4638 manually asap so that it would be part of this week’s Dev release i.e., tomorrow.

### pb...@google.com (2021-09-13)

Your change has been approved for M95. Please go ahead and merge the CL to branch 4638 manually asap so that it would be part of this week’s Dev release i.e., tomorrow.

### gi...@appspot.gserviceaccount.com (2021-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bfc77020c6ffcaf5216577ba2e5dc7344d0f5fd6

commit bfc77020c6ffcaf5216577ba2e5dc7344d0f5fd6
Author: Austin Sullivan <asully@chromium.org>
Date: Mon Sep 13 23:19:52 2021

FSA: Fix race condition in manager

(cherry picked from commit 951339b41022b08a67ad94ba5960b05c84bf4cf2)

Bug: 1248030
Change-Id: I1ea819d1d6ac63ec8f400a45c893da49596235ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3154425
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#920376}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3158788
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4638@{#26}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/bfc77020c6ffcaf5216577ba2e5dc7344d0f5fd6/content/browser/file_system_access/file_system_access_manager_impl.cc
[modify] https://crrev.com/bfc77020c6ffcaf5216577ba2e5dc7344d0f5fd6/content/browser/file_system_access/file_system_access_manager_impl.h
[modify] https://crrev.com/bfc77020c6ffcaf5216577ba2e5dc7344d0f5fd6/content/browser/storage_partition_impl.cc


### sr...@google.com (2021-09-14)

since this is hard to repro and we are cutting stable RC for m94 today, we will wait for the reporter to confirm this is working as intended before we take merge to M94 and include in first re-spin

### so...@gmail.com (2021-09-15)

Re c#27:

Yes, good fix.

### sr...@google.com (2021-09-15)

Merge approved for m94 branch:4606 ( We will take in next M94 release)

### gi...@appspot.gserviceaccount.com (2021-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e528a5a8d839f8b382d25821a2807546f97d2cc

commit 4e528a5a8d839f8b382d25821a2807546f97d2cc
Author: Austin Sullivan <asully@chromium.org>
Date: Wed Sep 15 23:57:27 2021

FSA: Fix race condition in manager

(cherry picked from commit 951339b41022b08a67ad94ba5960b05c84bf4cf2)

Bug: 1248030
Change-Id: I1ea819d1d6ac63ec8f400a45c893da49596235ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3154425
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#920376}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3160301
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#1077}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/4e528a5a8d839f8b382d25821a2807546f97d2cc/content/browser/file_system_access/file_system_access_manager_impl.cc
[modify] https://crrev.com/4e528a5a8d839f8b382d25821a2807546f97d2cc/content/browser/file_system_access/file_system_access_manager_impl.h
[modify] https://crrev.com/4e528a5a8d839f8b382d25821a2807546f97d2cc/content/browser/storage_partition_impl.cc


### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2021-09-28)

[Empty comment from Monorail migration]

### gi...@google.com (2021-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f703dacd1a1d9a80cd7486cdb1936f11ef8138a5

commit f703dacd1a1d9a80cd7486cdb1936f11ef8138a5
Author: Austin Sullivan <asully@chromium.org>
Date: Wed Sep 29 08:20:51 2021

[M90-LTS] FSA: Fix race condition in manager

(cherry picked from commit 951339b41022b08a67ad94ba5960b05c84bf4cf2)

Bug: 1248030
Change-Id: I1ea819d1d6ac63ec8f400a45c893da49596235ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3154425
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#920376}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3182123
Reviewed-by: Austin Sullivan <asully@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1624}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/f703dacd1a1d9a80cd7486cdb1936f11ef8138a5/content/browser/file_system_access/file_system_access_manager_impl.h
[modify] https://crrev.com/f703dacd1a1d9a80cd7486cdb1936f11ef8138a5/content/browser/storage_partition_impl.cc
[modify] https://crrev.com/f703dacd1a1d9a80cd7486cdb1936f11ef8138a5/content/browser/file_system_access/file_system_access_manager_impl.cc


### rz...@google.com (2021-09-29)

[Empty comment from Monorail migration]

### so...@gmail.com (2021-10-06)

Hi, any update of bounty?

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### so...@gmail.com (2021-10-11)

c#38
Any update for bounty? 

### am...@google.com (2021-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-13)

Congratulations - the VRP Panel has decided to award you $15,000 for this report! Thank you for your efforts and nice finding! 

### am...@google.com (2021-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1248030?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057215)*
