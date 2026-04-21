# Security: UAF in gcm::GCMDriver::Shutdown

| Field | Value |
|-------|-------|
| **Issue ID** | [40075409](https://issues.chromium.org/issues/40075409) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2023-10-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in gcm::GCMDriver::Shutdown

**VERSION**  

Chromium 120.0.6080.0 (Developer Build) (64-bit)  

Revision 5bb79c7cd3f3b57a90cdf0d7dbe98649173f9391-refs/heads/main@{#1213004}  

Platform ChromiumOS Linux

**REPRODUCTION CASE**  

run the command:  

 `./chrome --user-data-dir=/tmp --enable-features=CellularCarrierLock`

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==29292==ERROR: AddressSanitizer: heap-use-after-free on address 0x50600019af08 at pc 0x563f333c5193 bp 0x7ffd3710d990 sp 0x7ffd3710d988  

READ of size 8 at 0x50600019af08 thread T0 (chrome)  

==29292==WARNING: invalid path to external symbolizer!  

==29292==WARNING: Failed to use and restart external symbolizer!  

#0 0x563f333c5192 in \_\_tree\_next\_iter<std::\_\_Cr::\_\_tree\_end\_node<std::\_\_Cr::\_\_tree\_node\_base<void \*> \*> \*, std::\_\_Cr::\_\_tree\_node\_base<void \*> \*> ./../../third\_party/libc++/src/include/\_\_tree:208:14  

#1 0x563f333c5192 in operator++ ./../../third\_party/libc++/src/include/\_\_tree:949:11  

#2 0x563f333c5192 in operator++ ./../../third\_party/libc++/src/include/map:985:41  

#3 0x563f333c5192 in gcm::GCMDriver::Shutdown() ./../../components/gcm\_driver/gcm\_driver.cc:242:37  

#4 0x563f34d0a8ea in gcm::GCMDriverDesktop::Shutdown() ./../../components/gcm\_driver/gcm\_driver\_desktop.cc:596:14  

#5 0x563f34c236da in BrowserProcessImpl::StartTearDown() ./../../chrome/browser/browser\_process\_impl.cc:522:18  

#6 0x563f34c1ed82 in ChromeBrowserMainParts::PostMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1870:21  

#7 0x563f2877c346 in ash::ChromeBrowserMainPartsAsh::PostMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1693:32  

#8 0x563f2299162b in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() ./../../content/browser/browser\_main\_loop.cc:1145:13  

#9 0x563f22997ce9 in content::BrowserMainRunnerImpl::Shutdown() ./../../content/browser/browser\_main\_runner\_impl.cc:176:17  

#10 0x563f22989574 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:43:16  

#11 0x563f2a0bdf5f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:707:10  

#12 0x563f2a0c18ff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1298:10  

#13 0x563f2a0c1274 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1142:12  

#14 0x563f2a0badd7 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:334:36  

#15 0x563f2a0bba2e in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:347:10  

#16 0x563f18d441b0 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#17 0x7f3154a29d8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

0x50600019af08 is located 8 bytes inside of 64-byte region [0x50600019af00,0x50600019af40)  

freed by thread T0 (chrome) here:  

#0 0x563f18d4237d in operator delete(void\*) *asan\_rtl*:3  

#1 0x563f333ca033 in \_\_libcpp\_operator\_delete<void \*> ./../../third\_party/libc++/src/include/new:282:3  

#2 0x563f333ca033 in \_\_do\_deallocate\_handle\_size<> ./../../third\_party/libc++/src/include/new:306:10  

#3 0x563f333ca033 in \_\_libcpp\_deallocate ./../../third\_party/libc++/src/include/new:322:14  

#4 0x563f333ca033 in deallocate ./../../third\_party/libc++/src/include/\_\_memory/allocator.h:130:13  

#5 0x563f333ca033 in deallocate ./../../third\_party/libc++/src/include/\_\_memory/allocator\_traits.h:288:13  

#6 0x563f333ca033 in erase ./../../third\_party/libc++/src/include/\_\_tree:2438:5  

#7 0x563f333ca033 in unsigned long std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, gcm::GCMAppHandler\*>, std::\_\_Cr::\_\_map\_value\_compare<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, gcm::GCMAppHandler\*>, std::\_\_Cr::less<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>>, true>, std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, gcm::GCMAppHandler\*>>>::\_\_erase\_unique<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>>(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&) ./../../third\_party/libc++/src/include/\_\_tree:2459:5  

#8 0x563f34d0aefd in gcm::GCMDriverDesktop::RemoveAppHandler(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&) ./../../components/gcm\_driver/gcm\_driver\_desktop.cc:612:14  

#9 0x563f44ceed08 in ash::carrier\_lock::FcmTopicSubscriberImpl::ShutdownHandler() ./../../chromeos/ash/components/carrier\_lock/fcm\_topic\_subscriber\_impl.cc:176:18  

#10 0x563f333c5081 in gcm::GCMDriver::Shutdown() ./../../components/gcm\_driver/gcm\_driver.cc:244:19  

#11 0x563f34d0a8ea in gcm::GCMDriverDesktop::Shutdown() ./../../components/gcm\_driver/gcm\_driver\_desktop.cc:596:14  

#12 0x563f34c236da in BrowserProcessImpl::StartTearDown() ./../../chrome/browser/browser\_process\_impl.cc:522:18  

#13 0x563f34c1ed82 in ChromeBrowserMainParts::PostMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1870:21  

#14 0x563f2877c346 in ash::ChromeBrowserMainPartsAsh::PostMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1693:32  

#15 0x563f2299162b in content::BrowserMainLoop::ShutdownThreadsAndCleanUp() ./../../content/browser/browser\_main\_loop.cc:1145:13  

#16 0x563f22997ce9 in content::BrowserMainRunnerImpl::Shutdown() ./../../content/browser/browser\_main\_runner\_impl.cc:176:17  

#17 0x563f22989574 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:43:16  

#18 0x563f2a0bdf5f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:707:10  

#19 0x563f2a0c18ff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1298:10  

#20 0x563f2a0c1274 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1142:12  

#21 0x563f2a0badd7 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:334:36  

#22 0x563f2a0bba2e in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:347:10  

#23 0x563f18d441b0 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#24 0x7f3154a29d8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

previously allocated by thread T0 (chrome) here:  

#0 0x563f18d41b1d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x563f333c9b35 in \_\_libcpp\_operator\_new<unsigned long> ./../../third\_party/libc++/src/include/new:272:10  

#2 0x563f333c9b35 in \_\_libcpp\_allocate ./../../third\_party/libc++/src/include/new:298:10  

#3 0x563f333c9b35 in allocate ./../../third\_party/libc++/src/include/\_\_memory/allocator.h:114:38  

#4 0x563f333c9b35 in allocate ./../../third\_party/libc++/src/include/\_\_memory/allocator\_traits.h:268:20  

#5 0x563f333c9b35 in \_\_construct\_node<const std::\_\_Cr::piecewise\_construct\_t &, std::\_\_Cr::tuple<const std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char> > &>, std::\_\_Cr::tuple<> > ./../../third\_party/libc++/src/include/\_\_tree:2147:23  

#6 0x563f333c9b35 in std::\_\_Cr::pair<std::\_\_Cr::\_\_tree\_iterator<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, gcm::GCMAppHandler\*>, std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, gcm::GCMAppHandler\*>, void\*>\*, long>, bool> std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, gcm::GCMAppHandler\*>, std::\_\_Cr::\_\_map\_value\_compare<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, gcm::GCMAppHandler\*>, std::\_\_Cr::less<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>>, true>, std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, gcm::GCMAppHandler\*>>>::\_\_emplace\_unique\_key\_args<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::piecewise\_construct\_t const&, std::\_\_Cr::tuple<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&>, std::\_\_Cr::tuple<>>(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, std::\_\_Cr::piecewise\_construct\_t const&, std::\_\_Cr::tuple<std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&>&&, std::\_\_Cr::tuple<>&&) ./../../third\_party/libc++/src/include/\_\_tree:2110:29  

#7 0x563f333c529c in operator[] ./../../third\_party/libc++/src/include/map:1692:20  

#8 0x563f333c529c in gcm::GCMDriver::AddAppHandler(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, gcm::GCMAppHandler\*) ./../../components/gcm\_driver/gcm\_driver.cc:254:3  

#9 0x563f34d0aea9 in gcm::GCMDriverDesktop::AddAppHandler(std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>> const&, gcm::GCMAppHandler\*) ./../../components/gcm\_driver/gcm\_driver\_desktop.cc:604:14  

#10 0x563f44cecbc5 in ash::carrier\_lock::FcmTopicSubscriberImpl::FcmTopicSubscriberImpl(gcm::GCMDriver\*, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, std::\_\_Cr::basic\_string<char, std::\_\_Cr::char\_traits<char>, std::\_\_Cr::allocator<char>>, scoped\_refptr[network::SharedURLLoaderFactory](javascript:void(0);)) ./../../chromeos/ash/components/carrier\_lock/fcm\_topic\_subscriber\_impl.cc:30:19  

#11 0x563f44ce23cc in make\_unique<ash::carrier\_lock::FcmTopicSubscriberImpl, gcm::GCMDriver \*&, const char (&)[33], const char (&)[13], scoped\_refptr[network::SharedURLLoaderFactory](javascript:void(0);) &> ./../../third\_party/libc++/src/include/\_\_memory/unique\_ptr.h:685:30  

#12 0x563f44ce23cc in ash::carrier\_lock::CarrierLockManager::Create(PrefService\*, gcm::GCMDriver\*, scoped\_refptr[network::SharedURLLoaderFactory](javascript:void(0);)) ./../../chromeos/ash/components/carrier\_lock/carrier\_lock\_manager.cc:205:19  

#13 0x563f28775669 in ash::ChromeBrowserMainPartsAsh::PreProfileInit() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:1049:29  

#14 0x563f34c1bf4d in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() ./../../chrome/browser/chrome\_browser\_main.cc:1523:3  

#15 0x563f34c1ba05 in ChromeBrowserMainParts::PreMainMessageLoopRun() ./../../chrome/browser/chrome\_browser\_main.cc:1197:18  

#16 0x563f28773da1 in ash::ChromeBrowserMainPartsAsh::PreMainMessageLoopRun() ./../../chrome/browser/ash/chrome\_browser\_main\_parts\_ash.cc:863:39  

#17 0x563f2298e6d8 in content::BrowserMainLoop::PreMainMessageLoopRun() ./../../content/browser/browser\_main\_loop.cc:1002:28  

#18 0x563f22994bb9 in Invoke<int (content::BrowserMainLoop::\*)(), content::BrowserMainLoop \*> ./../../base/functional/bind\_internal.h:713:12  

#19 0x563f22994bb9 in MakeItSo<int (content::BrowserMainLoop::\*)(), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> > > ./../../base/functional/bind\_internal.h:868:12  

#20 0x563f22994bb9 in RunImpl<int (content::BrowserMainLoop::\*)(), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> >, 0UL> ./../../base/functional/bind\_internal.h:968:12  

#21 0x563f22994bb9 in base::internal::Invoker<base::internal::BindState<int (content::BrowserMainLoop::\*)(), base::internal::UnretainedWrapper<content::BrowserMainLoop, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>>, int ()>::RunOnce(base::internal::BindStateBase\*) ./../../base/functional/bind\_internal.h:919:12  

#22 0x563f1a0c2c47 in base::OnceCallback<int ()>::Run() && ./../../base/functional/callback.h:154:12  

#23 0x563f23faea8c in content::StartupTaskRunner::RunAllTasksNow() ./../../content/browser/startup\_task\_runner.cc:42:29  

#24 0x563f2298da75 in content::BrowserMainLoop::CreateStartupTasks() ./../../content/browser/browser\_main\_loop.cc:913:25  

#25 0x563f2299723d in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams) ./../../content/browser/browser\_main\_runner\_impl.cc:139:15  

#26 0x563f22989492 in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:32  

#27 0x563f2a0bdf5f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:707:10  

#28 0x563f2a0c18ff in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1298:10  

#29 0x563f2a0c1274 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1142:12  

#30 0x563f2a0badd7 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:334:36  

#31 0x563f2a0bba2e in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:347:10  

#32 0x563f18d441b0 in ChromeMain ./../../chrome/app/chrome\_main.cc:190:12  

#33 0x7f3154a29d8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

SUMMARY: AddressSanitizer: heap-use-after-free (/home/kuer/chromium\_version/latest\_asan/chrome+0x2e11f192) (BuildId: fe643444119443ca)  

Shadow bytes around the buggy address:  

0x50600019ac80: fd fd fd fd fa fa f7 fa fd fd fd fd fd fd fd fd  

0x50600019ad00: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa  

0x50600019ad80: fd fd fd fd fd fd fd fd fa fa f7 fa fd fd fd fd  

0x50600019ae00: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fa  

0x50600019ae80: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa  

=>0x50600019af00: fd[fd]fd fd fd fd fd fd fa fa f7 fa fd fd fd fd  

0x50600019af80: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fa  

0x50600019b000: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa  

0x50600019b080: 00 00 00 00 00 00 00 fa fa fa f7 fa 00 00 00 00  

0x50600019b100: 00 00 00 00 fa fa f7 fa 00 00 00 00 00 00 00 00  

0x50600019b180: fa fa f7 fa fd fd fd fd fd fd fd fd fa fa f7 fa  

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

==29292==ADDITIONAL INFO

==29292==Note: Please include this section with the ASan report.  

Task trace:

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==29292==END OF ADDITIONAL INFO  

==29292==ABORTING  

2023-10-21T02:03:42.800980Z ERROR nacl\_helper: [nacl\_helper\_linux.cc(354)] NaCl helper process running without a sandbox!  

Most likely you need to configure your SUID sandbox correctly

## Timeline

### [Deleted User] (2023-10-23)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-10-23)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-24)

Dear Reporter,

Thank you for your report!

We have migrated our ChromeOS VRP process to a new system, which is described here: 

https://bughunters.google.com/about/rules/4919474699501568/chromeos-vulnerability-reward-program-rules

Could you please use our new form/process and re-submit this ChromeOS report?

https://bughunters.google.com/report/vrp  --> select ChromeOS as the product

### 0x...@gmail.com (2023-10-30)

Hi, the ChromeOS VRP comment:
Chrome bugs on Ubuntu need to be reported directly to the Chrome VRP

https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules

Since Chrome uses a different issue tracker we can't transfer your bug directly. We will close this bug but feel free to update with the Chrome bug number.

### ch...@google.com (2023-11-06)

Thanks for the heads-up...will close this one as Obsolete

### am...@chromium.org (2023-11-08)

Hello OP, thank you for reaching out. Apologies you've been given a bit of the run around here.
There's not enough actionable information in this report to fully triage this issue. Can you please provide a POC, steps to reproduce, or other technical information we can use to triage this issue. 
I am assigning a *tentative* severity of high since this is a UAF in the browser process, so this may change based on mitigations or other information that is needed here. 
Security_Impact-None since this involves CellularCarrierLock which is behind a flag

assigning to peter@ as an owner of GCM driver and based on previous work. 
cc'ing ejcaruso@ and michazmazur@ since this appears to be specific to Cellular Carrier Lock
I've asked the OP to please provide actionable technical information to support this finding, but wanted to provide awareness of this issue in the interim. 




[Monorail components: Services>CloudMessaging]

### am...@chromium.org (2023-11-08)

for reference b/307620338 was the buganizer equivalent of this report the researcher was asked to submit, which was already closed as WontFix

### [Deleted User] (2023-11-09)

[Empty comment from Monorail migration]

### mi...@google.com (2023-11-14)

[Empty comment from Monorail migration]

### mi...@google.com (2023-11-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b8ba8d654d63eb9335cfed50b2a979dcadfa93a9

commit b8ba8d654d63eb9335cfed50b2a979dcadfa93a9
Author: Michal Mazur <michamazur@google.com>
Date: Thu Nov 30 18:12:38 2023

carrier_lock: destroy carrier lock manager before GCM driver

Fix UAF crash when stopping Chrome.

Bug: 1494751
Test: build with AddressSanitizer and test with enabled carrier lock:
      `--enable-features=CellularCarrierLock`

Change-Id: I2e4fc8d7233b43710112bf93c5492b133f2de533
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5036992
Reviewed-by: Peter Beverloo <peter@chromium.org>
Reviewed-by: Marc Treib <treib@chromium.org>
Commit-Queue: Michał Mazur <michamazur@google.com>
Reviewed-by: Gordon Seto <gordonseto@google.com>
Cr-Commit-Position: refs/heads/main@{#1231394}

[modify] https://crrev.com/b8ba8d654d63eb9335cfed50b2a979dcadfa93a9/chrome/browser/ash/chrome_browser_main_parts_ash.cc
[modify] https://crrev.com/b8ba8d654d63eb9335cfed50b2a979dcadfa93a9/chromeos/ash/components/carrier_lock/fcm_topic_subscriber_impl.cc


### an...@chromium.org (2023-11-30)

[security shepherd] peter@, yanivt@, treib@ - OP has not posted any additional information since the request was made in c#6 21 days ago. Just checking if any one of you has/needs to take a look before we close this out as WontFix?

### mi...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### mi...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-07)

Congratulations asnine! The VRP Panel has decided to award you $1,000 for this significantly mitigated security bug. We ordinarily would not extend a reward in a unlaunched feature that simply involves just starting Chrome with the feature enabled (as that would be caught upon testing a feature well before launch); however, since a crash (bug in c#13) was reported on this following your report, the combined efforts did allow this issue to be fixed sooner than later. Thank you for your efforts! 

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-08)

This issue was migrated from crbug.com/chromium/1494751?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1503910]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075409)*
