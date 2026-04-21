# Security: UAF in in safe_browsing::IncidentReportingService::AddIncident(browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061003](https://issues.chromium.org/issues/40061003) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | xi...@chromium.org |
| **Created** | 2022-09-16 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in in safe\_browsing::IncidentReportingService::AddIncident in the browser process

**VERSION**  

Chrome Version: 107.0.5302.0 (Developer Build) (64-bit)  

Operating System: Windows 10 Version 21H2 (Build 19044.2006)

**REPRODUCTION CASE**

1. put the attachements into the extension\_path folder
2. run the command:  
   
   chrome.exe --user-data-dir=c:/any --remote-debugging-port=9222 --load-extension="extenssion\_path" about:blank

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

# Crash log:

==35508==ERROR: AddressSanitizer: heap-use-after-free on address 0x1235575bee40 at pc 0x7fff91de07e4 bp 0x0051077fdf20 sp 0x0051077fdf68  

READ of size 8 at 0x1235575bee40 thread T0  

==35508==WARNING: Failed to use and restart external symbolizer!  

#0 0x7fff91de07e3 in safe\_browsing::IncidentReportingService::AddIncident C:\b\s\w\ir\cache\builder\src\chrome\browser\safe\_browsing\incident\_reporting\incident\_reporting\_service.cc:566  

#1 0x7fff91ddf2d1 in safe\_browsing::IncidentReportingService::Receiver::AddIncidentOnMainThread C:\b\s\w\ir\cache\builder\src\chrome\browser\safe\_browsing\incident\_reporting\incident\_reporting\_service.cc:272  

#2 0x7fff91ddf0ba in safe\_browsing::IncidentReportingService::Receiver::AddIncidentForProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\safe\_browsing\incident\_reporting\incident\_reporting\_service.cc:229  

#3 0x7fff955ac397 in safe\_browsing::PreferenceValidationDelegate::OnAtomicPreferenceValidation C:\b\s\w\ir\cache\builder\src\chrome\browser\safe\_browsing\incident\_reporting\preference\_validation\_delegate.cc:83  

#4 0x7fff8587aec6 in prefs::mojom::TrackedPreferenceValidationDelegateStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\services\preferences\public\mojom\tracked\_preference\_validation\_delegate.mojom.cc:333  

#5 0x7fff875c6235 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:989  

#6 0x7fff8a31834e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#7 0x7fff875ca2de in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:689  

#8 0x7fff875e047e in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1096  

#9 0x7fff875df36e in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:716  

#10 0x7fff8a31834e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#11 0x7fff875c0890 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:561  

#12 0x7fff875c21b1 in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:618  

#13 0x7fff875c370b in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(),base::WeakPtr[mojo::Connector](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:843  

#14 0x7fff87305fca in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:133  

#15 0x7fff8a1b7585 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#16 0x7fff8a1b6556 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:292  

#17 0x7fff873b5396 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#18 0x7fff873b33db in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#19 0x7fff8a1b981b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:577  

#20 0x7fff872a13a2 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#21 0x7fff7ef6d057 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1046  

#22 0x7fff7ef73267 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:157  

#23 0x7fff7ef660d1 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#24 0x7fff86e3183f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:698  

#25 0x7fff86e348f1 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1232  

#26 0x7fff86e3418f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1091  

#27 0x7fff86e3001b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:342  

#28 0x7fff86e306fe in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:370  

#29 0x7fff7aea14ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182  

#30 0x7ff601995bfe in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162  

#31 0x7ff601992bd7 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#32 0x7ff601dad93f in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#33 0x7ff855837033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#34 0x7ff855b026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x1235575bee40 is located 0 bytes inside of 440-byte region [0x1235575bee40,0x1235575beff8)  

freed by thread T0 here:  

#0 0x7ff601a3f95c in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7fff8a0b61c7 in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:872  

#2 0x7fff8a0cfdb3 in ProfileDestroyer::DestroyOriginalProfileNow C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:196  

#3 0x7fff8a0ccc8a in ProfileDestroyer::DestroyProfileWhenAppropriateWithTimeout C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:119  

#4 0x7fff8710a199 in ProfileManager::ProfileInfo::~ProfileInfo C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1771  

#5 0x7fff87111f8b in std::Cr::unique\_ptr<ProfileManager::ProfileInfo,std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:281  

#6 0x7fff871123a4 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<base::FilePath,std::Cr::unique\_ptr<ProfileManager::ProfileInfo,std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::Cr::\_\_map\_value\_compare<base::FilePath,std::Cr::\_\_value\_type<base::FilePath,std::Cr::unique\_ptr<ProfileManager::ProfileInfo,std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::Cr::less[base::FilePath](javascript:void(0);),1>,std::Cr::allocator<std::Cr::\_\_value\_type<base::FilePath,std::Cr::unique\_ptr<ProfileManager::ProfileInfo,std::Cr::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2427  

#7 0x7fff8710a83b in ProfileManager::OnProfileCreationFinished C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1969  

#8 0x7fff8a0ae2a9 in ProfileImpl::OnPrefsLoaded C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:1167  

#9 0x7fff8a0b697c in base::internal::Invoker<base::internal::BindState<void (ProfileImpl::\*)(Profile::CreateMode, bool),base::internal::UnretainedWrapper<ProfileImpl>,Profile::CreateMode>,void (bool)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:843  

#10 0x7fff8abd7d7c in PrefNotifierImpl::OnInitializationCompleted C:\b\s\w\ir\cache\builder\src\components\prefs\pref\_notifier\_impl.cc:126  

#11 0x7fff7e592930 in policy::ConfigurationPolicyPrefStore::OnPolicyServiceInitialized C:\b\s\w\ir\cache\builder\src\components\policy\core\browser\configuration\_policy\_pref\_store.cc:109  

#12 0x7fff7e65deb7 in policy::PolicyServiceImpl::MaybeNotifyPolicyDomainStatusChange C:\b\s\w\ir\cache\builder\src\components\policy\core\common\policy\_service\_impl.cc:488  

#13 0x7fff7e65c05b in policy::PolicyServiceImpl::MergeAndTriggerUpdates C:\b\s\w\ir\cache\builder\src\components\policy\core\common\policy\_service\_impl.cc:433  

#14 0x7fff7e66079c in base::internal::Invoker<base::internal::BindState<void (policy::PolicyServiceImpl::\*)(),base::WeakPtr[policy::PolicyServiceImpl](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:843  

#15 0x7fff87305fca in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:133  

#16 0x7fff8a1b7585 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#17 0x7fff8a1b6556 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:292  

#18 0x7fff873b5396 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#19 0x7fff873b33db in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#20 0x7fff8a1b981b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:577  

#21 0x7fff872a13a2 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#22 0x7fff7ef6d057 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1046  

#23 0x7fff7ef73267 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:157  

#24 0x7fff7ef660d1 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#25 0x7fff86e3183f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:698  

#26 0x7fff86e348f1 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1232  

#27 0x7fff86e3418f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1091

previously allocated by thread T0 here:  

#0 0x7ff601a3fa5c in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7fff9b04dbee in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7fff8a0aa90a in Profile::CreateProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:366  

#3 0x7fff871053ec in ProfileManager::CreateProfileAsyncHelper C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1455  

#4 0x7fff870f973f in ProfileManager::CreateProfileAsync C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:843  

#5 0x7fff87110d2f in base::internal::Invoker<base::internal::BindState<void (ProfileManager::\*)(const base::FilePath &, base::OnceCallback<void (Profile \*)>, base::OnceCallback<void (Profile \*)>),base::WeakPtr<ProfileManager>,base::FilePath,base::OnceCallback<void (Profile \*)>,base::OnceCallback<void (Profile \*)> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:843  

#6 0x7fff87305fca in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:133  

#7 0x7fff8a1b7585 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#8 0x7fff8a1b6556 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:292  

#9 0x7fff873b5396 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#10 0x7fff873b33db in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#11 0x7fff8a1b981b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:577  

#12 0x7fff872a13a2 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#13 0x7fff7ef6d057 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1046  

#14 0x7fff7ef73267 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:157  

#15 0x7fff7ef660d1 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#16 0x7fff86e3183f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:698  

#17 0x7fff86e348f1 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1232  

#18 0x7fff86e3418f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1091  

#19 0x7fff86e3001b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:342  

#20 0x7fff86e306fe in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:370  

#21 0x7fff7aea14ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182  

#22 0x7ff601995bfe in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162  

#23 0x7ff601992bd7 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#24 0x7ff601dad93f in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#25 0x7ff855837033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#26 0x7ff855b026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\chrome\browser\safe\_browsing\incident\_reporting\incident\_reporting\_service.cc:566 in safe\_browsing::IncidentReportingService::AddIncident  

Shadow bytes around the buggy address:  

0x1235575beb80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1235575bec00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

0x1235575bec80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1235575bed00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1235575bed80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x1235575bee00: fa fa fa fa fa fa f7 fa[fd]fd fd fd fd fd fd fd  

0x1235575bee80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1235575bef00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1235575bef80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x1235575bf000: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

0x1235575bf080: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

MiraclePtr Status: MANUAL ANALYSIS REQUIRED  

A pointer to the same region was extracted from a raw\_ptr<T> object prior to the crash.  

To determine the protection status, enable extraction warnings and check whether the raw\_ptr<T>  

object can be destroyed or overwritten between the extraction and use.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 422 B)
- [background.js](attachments/background.js) (text/plain, 557 B)
- [injection.js](attachments/injection.js) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2022-09-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-16)

DNR on linux, got localhost refused to connect. Taking asan trace in cl description as a sufficient starting point.



### ts...@chromium.org (2022-09-16)

[Empty comment from Monorail migration]

[Monorail components: Services>Safebrowsing]

### ts...@chromium.org (2022-09-16)

Assigning per chrome/browser/safe_browsing/incident_reporting/OWNERS

### ts...@chromium.org (2022-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-17)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pr...@chromium.org (2022-09-19)

Re-assigning to @vakh for triaging

### dr...@chromium.org (2022-09-28)

(Bugs with owners are automatically considered triaged)

### va...@chromium.org (2022-09-30)

=> xinghuilu@ who volunteered to look into this.

### [Deleted User] (2022-10-01)

xinghuilu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-10-03)

Thanks for the report! I'll take a look. It is likely affecting other desktop platforms too. I agree with high severity since it is a UAF in the browser process during shutdown.

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-10-03)

I'm able to reproduce the crash on Linux with a small tweak: I need to remove the proto_value_state != TPIncident::UNKNOWN check[1] to actually trigger the code path.

I think the root cause is that the profile_[2] pointer was destroyed before AddIncidentForProfile is called. We need to observe the profile destroy event by implementing profile_observer[3].

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.cc;l=70;drc=a2a75509d6058498d6e00ca225455a53b1006188
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.h;l=55;drc=a2a75509d6058498d6e00ca225455a53b1006188
[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profiles/profile_observer.h;l=29;drc=a2a75509d6058498d6e00ca225455a53b1006188

### [Deleted User] (2022-10-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/57d96518a0ab600d75b118fbeec2d7a3f526ed2a

commit 57d96518a0ab600d75b118fbeec2d7a3f526ed2a
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Tue Oct 04 20:37:41 2022

Reset the profile pointer in PreferenceValidationDelegate before the profile is destroyed.

Bug: 1364662
Change-Id: I24678c1f5030474c9193a5552463da6ffbdec6d5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3929491
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Reviewed-by: Daniel Rubery <drubery@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1054911}

[modify] https://crrev.com/57d96518a0ab600d75b118fbeec2d7a3f526ed2a/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.cc
[modify] https://crrev.com/57d96518a0ab600d75b118fbeec2d7a3f526ed2a/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate_unittest.cc
[modify] https://crrev.com/57d96518a0ab600d75b118fbeec2d7a3f526ed2a/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.h


### xi...@chromium.org (2022-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-05)

Requesting merge to stable M106 because latest trunk commit (1054911) appears to be after stable branch point (1036826).

Requesting merge to beta M107 because latest trunk commit (1054911) appears to be after beta branch point (1047731).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-05)

Merge review required: M107 is already shipping to beta.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-05)

Merge review required: M106 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2022-10-05)

1. High severity security bug.
2. https://crrev.com/c/3929491
3. Yes
4. No
5. N/A
6. No manual verification required.

### am...@chromium.org (2022-10-07)

107 merge approved, please merge to branch 5304
106 merge approved, please merge to branch 5249 by 10am PST, Monday, 10 October so this fix can be included in the next Stable security respin - thank you! 

### gi...@appspot.gserviceaccount.com (2022-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2190488addeeb3f33b43bf78324ab6e6ef90f495

commit 2190488addeeb3f33b43bf78324ab6e6ef90f495
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Fri Oct 07 22:31:49 2022

[M107] Reset the profile pointer in PreferenceValidationDelegate before the profile is destroyed.

(cherry picked from commit 57d96518a0ab600d75b118fbeec2d7a3f526ed2a)

Bug: 1364662
Change-Id: I24678c1f5030474c9193a5552463da6ffbdec6d5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3929491
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Reviewed-by: Daniel Rubery <drubery@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1054911}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3939997
Auto-Submit: Xinghui Lu <xinghuilu@chromium.org>
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Cr-Commit-Position: refs/branch-heads/5304@{#533}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/2190488addeeb3f33b43bf78324ab6e6ef90f495/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.cc
[modify] https://crrev.com/2190488addeeb3f33b43bf78324ab6e6ef90f495/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate_unittest.cc
[modify] https://crrev.com/2190488addeeb3f33b43bf78324ab6e6ef90f495/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.h


### [Deleted User] (2022-10-07)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b6dea0059e2295d112b6e63eedb90373a81b89b4

commit b6dea0059e2295d112b6e63eedb90373a81b89b4
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Fri Oct 07 22:40:20 2022

[M106] Reset the profile pointer in PreferenceValidationDelegate before the profile is destroyed.

(cherry picked from commit 57d96518a0ab600d75b118fbeec2d7a3f526ed2a)

Bug: 1364662
Change-Id: I24678c1f5030474c9193a5552463da6ffbdec6d5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3929491
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Reviewed-by: Daniel Rubery <drubery@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1054911}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3939135
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Auto-Submit: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#778}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/b6dea0059e2295d112b6e63eedb90373a81b89b4/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.cc
[modify] https://crrev.com/b6dea0059e2295d112b6e63eedb90373a81b89b4/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate_unittest.cc
[modify] https://crrev.com/b6dea0059e2295d112b6e63eedb90373a81b89b4/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.h


### am...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### vo...@google.com (2022-10-11)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations, asnine! The VRP Panel has decided to award you $7,000 for this report of this mildly mitigated security bug. Thank you for your efforts in discovering this issue and reporting it to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### vo...@google.com (2022-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2022-10-18)

1. Just one https://crrev.com/c/3944306
2. Low - small changes, no conflicts with M102
3. M106
4. Yes

### gm...@google.com (2022-10-18)

[Empty comment from Monorail migration]

### vo...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### gm...@google.com (2022-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-28)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-10-31)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/faebe902d480359521e2bd81d305dcbc3a5af308

commit faebe902d480359521e2bd81d305dcbc3a5af308
Author: Xinghui Lu <xinghuilu@chromium.org>
Date: Wed Nov 02 13:46:18 2022

[M102-LTS] Reset the profile pointer in PreferenceValidationDelegate before the profile is destroyed.

(cherry picked from commit 57d96518a0ab600d75b118fbeec2d7a3f526ed2a)

(cherry picked from commit b6dea0059e2295d112b6e63eedb90373a81b89b4)

Bug: 1364662
Change-Id: I24678c1f5030474c9193a5552463da6ffbdec6d5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3929491
Commit-Queue: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1054911}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3939135
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Auto-Submit: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5249@{#778}
Cr-Original-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3944306
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1379}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/faebe902d480359521e2bd81d305dcbc3a5af308/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.cc
[modify] https://crrev.com/faebe902d480359521e2bd81d305dcbc3a5af308/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate_unittest.cc
[modify] https://crrev.com/faebe902d480359521e2bd81d305dcbc3a5af308/chrome/browser/safe_browsing/incident_reporting/preference_validation_delegate.h


### vo...@google.com (2022-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1364662?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061003)*
