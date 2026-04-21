# Security: heap-use-after-free in ExtensionFunction::Shutdown

| Field | Value |
|-------|-------|
| **Issue ID** | [40058550](https://issues.chromium.org/issues/40058550) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2022-01-21 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

Closing the browser and opening an extension action popup at the same time causes a UAF in the browser process.

**VERSION**  

Chrome Version: 99.0.4837.0  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Install the attached extension (no extension permissions required)

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser Crash State:

==33308==ERROR: AddressSanitizer: heap-use-after-free on address 0x121a6ca58f78 at pc 0x7ff8204756d6 bp 0x00a42f7fe620 sp 0x00a42f7fe668  

WRITE of size 8 at 0x121a6ca58f78 thread T0  

==33308==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff8204756d5 in ExtensionFunction::Shutdown C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function.cc:598  

#1 0x7ff8201901cc in base::OnceCallbackList<void ()>::RunCallback<> C:\b\s\w\ir\cache\builder\src\base\callback\_list.h:298  

#2 0x7ff82018f8ee in base::internal::CallbackListBase<base::OnceCallbackList<void ()> >::Notify<> C:\b\s\w\ir\cache\builder\src\base\callback\_list.h:219  

#3 0x7ff82908b8db in DependencyManager::PerformInterlockedTwoPhaseShutdown C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\dependency\_manager.cc:123  

#4 0x7ff827f8b23d in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:913  

#5 0x7ff827f8ef1d in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:860  

#6 0x7ff827fa0b9f in ProfileDestroyer::DestroyOriginalProfileNow C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:133  

#7 0x7ff827fa03d3 in ProfileDestroyer::DestroyProfileWhenAppropriate C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:61  

#8 0x7ff82530c791 in ProfileManager::ProfileInfo::~ProfileInfo C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1683  

#9 0x7ff8253130b7 in std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:315  

#10 0x7ff8253135ae in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2422  

#11 0x7ff825313503 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::\_\_erase\_unique[base::FilePath](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2445  

#12 0x7ff825309ec2 in ProfileManager::RemoveProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1788  

#13 0x7ff825309c38 in ProfileManager::DeleteProfileIfNoKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1518  

#14 0x7ff825309705 in ProfileManager::RemoveKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1475  

#15 0x7ff8254f8f74 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#16 0x7ff828068f45 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#17 0x7ff828068618 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#18 0x7ff8255a5086 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#19 0x7ff8255a3318 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#20 0x7ff82806a611 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#21 0x7ff825477ae3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#22 0x7ff81e5e4fed in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#23 0x7ff81e5ea40d in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#24 0x7ff81e5de675 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#25 0x7ff821092e2f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#26 0x7ff821095e6f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1161  

#27 0x7ff821094fa2 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1027  

#28 0x7ff821091229 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:399  

#29 0x7ff821092302 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:427  

#30 0x7ff81a90148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#31 0x7ff60f0c5b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#32 0x7ff60f0c2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#33 0x7ff60f4c2fbf in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#34 0x7ff8e0047033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#35 0x7ff8e06e2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x121a6ca58f78 is located 312 bytes inside of 424-byte region [0x121a6ca58e40,0x121a6ca58fe8)  

freed by thread T0 here:  

#0 0x7ff60f172b2b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff82caf0f27 in extensions::ActionOpenPopupFunction::~ActionOpenPopupFunction C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\api\extension\_action\extension\_action\_api.cc:633  

#2 0x7ff8202409c6 in content::BrowserThread::DeleteOnThread[content::BrowserThread::UI](javascript:void(0);)::Destruct<ExtensionFunction> C:\b\s\w\ir\cache\builder\src\content\public\browser\browser\_thread.h:156  

#3 0x7ff82047569b in ExtensionFunction::Shutdown C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function.cc:598  

#4 0x7ff8201901cc in base::OnceCallbackList<void ()>::RunCallback<> C:\b\s\w\ir\cache\builder\src\base\callback\_list.h:298  

#5 0x7ff82018f8ee in base::internal::CallbackListBase<base::OnceCallbackList<void ()> >::Notify<> C:\b\s\w\ir\cache\builder\src\base\callback\_list.h:219  

#6 0x7ff82908b8db in DependencyManager::PerformInterlockedTwoPhaseShutdown C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\dependency\_manager.cc:123  

#7 0x7ff827f8b23d in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:913  

#8 0x7ff827f8ef1d in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:860  

#9 0x7ff827fa0b9f in ProfileDestroyer::DestroyOriginalProfileNow C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:133  

#10 0x7ff827fa03d3 in ProfileDestroyer::DestroyProfileWhenAppropriate C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:61  

#11 0x7ff82530c791 in ProfileManager::ProfileInfo::~ProfileInfo C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1683  

#12 0x7ff8253130b7 in std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:315  

#13 0x7ff8253135ae in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2422  

#14 0x7ff825313503 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::\_\_erase\_unique[base::FilePath](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2445  

#15 0x7ff825309ec2 in ProfileManager::RemoveProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1788  

#16 0x7ff825309c38 in ProfileManager::DeleteProfileIfNoKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1518  

#17 0x7ff825309705 in ProfileManager::RemoveKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1475  

#18 0x7ff8254f8f74 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#19 0x7ff828068f45 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#20 0x7ff828068618 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#21 0x7ff8255a5086 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#22 0x7ff8255a3318 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#23 0x7ff82806a611 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#24 0x7ff825477ae3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#25 0x7ff81e5e4fed in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#26 0x7ff81e5ea40d in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#27 0x7ff81e5de675 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30

previously allocated by thread T0 here:  

#0 0x7ff60f172c2b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff837c3a57e in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff834013863 in base::MakeRefCounted[extensions::ActionOpenPopupFunction](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\base\memory\scoped\_refptr.h:98  

#3 0x7ff83400330c in NewExtensionFunction[extensions::ActionOpenPopupFunction](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function\_registry.h:22  

#4 0x7ff82047fa2b in ExtensionFunctionRegistry::NewFunction C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function\_registry.cc:43  

#5 0x7ff82047c935 in extensions::ExtensionFunctionDispatcher::CreateExtensionFunction C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function\_dispatcher.cc:509  

#6 0x7ff82047abc2 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function\_dispatcher.cc:331  

#7 0x7ff82047c0c5 in extensions::ExtensionFunctionDispatcher::DispatchForServiceWorker C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function\_dispatcher.cc:293  

#8 0x7ff8204d511e in IPC::MessageT<ExtensionHostMsg\_RequestWorker\_Meta,std::\_\_1::tuple[extensions::mojom::RequestParams](javascript:void(0);),void>::Dispatch<extensions::ExtensionServiceWorkerMessageFilter,extensions::ExtensionServiceWorkerMessageFilter,void,void (extensions::ExtensionServiceWorkerMessageFilter::\*)(const extensions::mojom::RequestParams &)> C:\b\s\w\ir\cache\builder\src\ipc\ipc\_message\_templates.h:140  

#9 0x7ff8204d4a5b in extensions::ExtensionServiceWorkerMessageFilter::OnMessageReceived C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_service\_worker\_message\_filter.cc:108  

#10 0x7ff8254f8f74 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#11 0x7ff828068f45 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#12 0x7ff828068618 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#13 0x7ff8255a5086 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#14 0x7ff8255a3318 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#15 0x7ff82806a611 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#16 0x7ff825477ae3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#17 0x7ff81e5e4fed in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#18 0x7ff81e5ea40d in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#19 0x7ff81e5de675 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#20 0x7ff821092e2f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#21 0x7ff821095e6f in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1161  

#22 0x7ff821094fa2 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1027  

#23 0x7ff821091229 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:399  

#24 0x7ff821092302 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:427  

#25 0x7ff81a90148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#26 0x7ff60f0c5b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167  

#27 0x7ff60f0c2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function.cc:598 in ExtensionFunction::Shutdown  

Shadow bytes around the buggy address:  

0x0435ba24b190: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0435ba24b1a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0435ba24b1b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0435ba24b1c0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0435ba24b1d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0435ba24b1e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]  

0x0435ba24b1f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x0435ba24b200: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0435ba24b210: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0435ba24b220: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0435ba24b230: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

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

==33308==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [background.js](attachments/background.js) (text/plain, 150 B)
- [manifest.json](attachments/manifest.json) (text/plain, 247 B)
- deleted (application/octet-stream, 0 B)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 383.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 25.5 KB)

## Timeline

### [Deleted User] (2022-01-21)

[Empty comment from Monorail migration]

### st...@gmail.com (2022-01-21)

[Empty comment from Monorail migration]

### aj...@google.com (2022-01-21)

Thanks we appreciate the video and files uploaded as attachments.

This repros immediately on Windows HEAD

I have a feeling the problem is really the base::Unretained here:-

void ExtensionFunction::SetDispatcher(
    const base::WeakPtr<extensions::ExtensionFunctionDispatcher>& dispatcher) {
  dispatcher_ = dispatcher;

  // Update |browser_context_| to the one from the dispatcher. Make it reset to
  // nullptr on shutdown.
  if (!dispatcher_ || !dispatcher_->browser_context()) {
    browser_context_ = nullptr;
    shutdown_subscription_ = base::CallbackListSubscription();
    return;
  }
  browser_context_ = dispatcher_->browser_context();
  shutdown_subscription_ =
      BrowserContextShutdownNotifierFactory::GetInstance()
          ->Get(browser_context_)
          ->Subscribe(base::BindRepeating(&ExtensionFunction::Shutdown,
                                          base::Unretained(this)));
}

Assigning to nicolaso based on CL https://chromium-review.googlesource.com/c/chromium/src/+/2774246

FoundIn=96 as commit predates that.
Sev=High as browser UAF that requires an extension.

At first glance this seems to be very controllable.




[Monorail components: Platform>Extensions]

### [Deleted User] (2022-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@chromium.org (2022-01-24)

> I have a feeling the problem is really the base::Unretained here:

It seems more complicated than that. This only seems to affect chrome.action.openPopup(), as opposed to all ExtensionFunctions.

I think the issue is here [1]. This function does something unusual with its refcount that might explain this crash. I'm still investigating, so I don't have a complete picture yet

> Sev=High as browser UAF that requires an extension.
> At first glance this seems to be very controllable.

If Sev=High, what does that mean WRT merging strategy? i.e., once a fix is landed, should I try to merge it into current the current Stable?

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/extension_action/extension_action_api.cc;l=712;drc=f568aedcc729dbe7746eebe57a1723ae0760220b

### aj...@google.com (2022-01-24)

Thanks for taking a look! For merging - once you've landed a CL you think solves the problem, mark this bug as Fixed and robots will then hassle you about what to merge where.

### ni...@chromium.org (2022-01-25)

Actually, it looks like the culprit CL is crrev.com/c/3352910, which landed ~2 weeks ago (so, M99).

So the issue is, that Shutdown() looks like this:

void ExtensionFunction::Shutdown() {
  OnBrowserContextShutdown();
  browser_context_ = nullptr;
}

And OnBrowserContextShutdown() looks like this:

void ActionOpenPopupFunction::OnBrowserContextShutdown() {
  host_registry_observation_.Reset();
  Release();
}

Release() frees the ExtensionFunction. But when control goes back to Shutdown(), it tries to set ` browser_context_' to nullptr. That's our UaF.

### [Deleted User] (2022-01-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9c07c7f7e9872b22cc6215c4cb0af7398ef421cc

commit 9c07c7f7e9872b22cc6215c4cb0af7398ef421cc
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date: Wed Jan 26 14:53:20 2022

[Extensions] Fix a crash in ActionOpenPopupFunction

The object deleted itself in OnBrowserContextShutdown(), which caused
a use-after-free when control was handed back to Shutdown(), which
assumed the object was still valid.

Hold a scoped_refptr<> in the caller, so destruction is delayed until
Shutdown() completes.

Bug: 1289715
Change-Id: I097bfa25987d68cd2f1c04a6dccda8b908bc05a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3415550
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Cr-Commit-Position: refs/heads/main@{#963506}

[modify] https://crrev.com/9c07c7f7e9872b22cc6215c4cb0af7398ef421cc/extensions/browser/extension_function.cc


### ni...@chromium.org (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-26)

Requesting merge to dev M99 because latest trunk commit (963506) appears to be after dev branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-27)

Merge approved: your change passed merge requirements and is auto-approved for M99. Please go ahead and merge the CL to branch 4844 (refs/branch-heads/4844) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-01-27)

Your change has been approved for M99 branch 4844,please go ahead and merge the CL's manually asap so that they would be part of tomorrow's M99 Dev release.

### ni...@chromium.org (2022-01-27)

The cherry-pick is in progress here: crrev.com/c/3420951

Just waiting for an LGTM so I can submit

### gi...@appspot.gserviceaccount.com (2022-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1528ca8b3d99450ce0274778f0682e2793541328

commit 1528ca8b3d99450ce0274778f0682e2793541328
Author: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Date: Thu Jan 27 20:15:21 2022

M99 merge: [Extensions] Fix a crash in ActionOpenPopupFunction

The object deleted itself in OnBrowserContextShutdown(), which caused
a use-after-free when control was handed back to Shutdown(), which
assumed the object was still valid.

Hold a scoped_refptr<> in the caller, so destruction is delayed until
Shutdown() completes.

(cherry picked from commit 9c07c7f7e9872b22cc6215c4cb0af7398ef421cc)

Bug: 1289715
Change-Id: I097bfa25987d68cd2f1c04a6dccda8b908bc05a5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3415550
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#963506}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3420951
Auto-Submit: Nicolas Ouellet-Payeur <nicolaso@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4844@{#84}
Cr-Branched-From: 007241ce2e6c8e5a7b306cc36c730cd07cd38825-refs/heads/main@{#961656}

[modify] https://crrev.com/1528ca8b3d99450ce0274778f0682e2793541328/extensions/browser/extension_function.cc


### [Deleted User] (2022-01-27)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ni...@chromium.org (2022-01-28)

#1 - No, not a regression.

#2 - The bug was introduced in crrev.com/c/3352910, which landed in M99. We don't need an LTS merge.

### rz...@google.com (2022-01-31)

Labelling as not applicable as it is not needed in M96 (reasons in https://crbug.com/chromium/1289715#c21)

### am...@google.com (2022-02-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-04)

Congratulations, Thomas! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and great work! 

### am...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1289715?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058550)*
