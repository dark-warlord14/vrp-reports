# Security: Heap-use-after-free in feedback::FeedbackData::SendReport

| Field | Value |
|-------|-------|
| **Issue ID** | [40057665](https://issues.chromium.org/issues/40057665) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Profiles, UI>Browser>ReportAnIssue |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | xi...@google.com |
| **Created** | 2021-10-20 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: 97.0.4675.0 (Developer Build) (64-bit)  

Operating System: Windows 10

**REPRODUCTION CASE**

1 Launch Chromium  

2 Click on experiments icon > Send feedback  

3 Click on "Avatar" icon and click on "Manage profiles"  

4 Delete "Person 1" and "Person 2"  

5 On the feedback dialog, type someting in the description field then click on "Send"

==8372==ERROR: AddressSanitizer: heap-use-after-free on address 0x125b2dfc2840 at pc 0x7ff8f88d2d66 bp 0x00c2917feba0 sp 0x00c2917febe8  

READ of size 8 at 0x125b2dfc2840 thread T0  

==8372==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff8f88d2d65 in feedback::FeedbackData::SendReport C:\b\s\w\ir\cache\builder\src\components\feedback\feedback\_data.cc:132  

#1 0x7ff8f924f89b in base::`anonymous namespace'::PostTaskAndReplyRelay::RunReply C:\b\s\w\ir\cache\builder\src\base\threading\post\_task\_and\_reply\_impl.cc:118  

#2 0x7ff8f924faf3 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:753  

#3 0x7ff8f6780c0a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#4 0x7ff8f925562f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:358  

#5 0x7ff8f9254d48 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#6 0x7ff8f6829846 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#7 0x7ff8f6827ad8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#8 0x7ff8f9256a45 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#9 0x7ff8f6700903 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#10 0x7ff8efa73bd9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1007  

#11 0x7ff8efa78e91 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#12 0x7ff8efa6d672 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#13 0x7ff8f2421870 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:641  

#14 0x7ff8f2424179 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1137  

#15 0x7ff8f2423363 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1004  

#16 0x7ff8f241fd72 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:390  

#17 0x7ff8f2420db4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:418  

#18 0x7ff8ebde147f in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#19 0x7ff796015b44 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#20 0x7ff796012c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#21 0x7ff79640d17f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#22 0x7ff98e737033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#23 0x7ff98fd82650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x125b2dfc2840 is located 0 bytes inside of 432-byte region [0x125b2dfc2840,0x125b2dfc29f0)  

freed by thread T0 here:  

#0 0x7ff7960c227b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff900032e35 in feedback::FeedbackUploaderChrome::~FeedbackUploaderChrome C:\b\s\w\ir\cache\builder\src\chrome\browser\feedback\feedback\_uploader\_chrome.cc:79  

#2 0x7ff8eef49c40 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<unsigned int,std::\_\_1::unique\_ptr<gpu::gles2::AbstractTexture,std::\_\_1::default\_delete[gpu::gles2::AbstractTexture](javascript:void(0);) > >,std::\_\_1::\_\_map\_value\_compare<unsigned int,std::\_\_1::\_\_value\_type<unsigned int,std::\_\_1::unique\_ptr<gpu::gles2::AbstractTexture,std::\_\_1::default\_delete[gpu::gles2::AbstractTexture](javascript:void(0);) > >,std::\_\_1::less<unsigned int>,1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<unsigned int,std::\_\_1::unique\_ptr<gpu::gles2::AbstractTexture,std::\_\_1::default\_delete[gpu::gles2::AbstractTexture](javascript:void(0);) > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2422  

#3 0x7ff8f786ee7c in KeyedServiceFactory::Disassociate C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\keyed\_service\_factory.cc:97  

#4 0x7ff8f786f10c in KeyedServiceFactory::ContextDestroyed C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\keyed\_service\_factory.cc:107  

#5 0x7ff8fa1da527 in DependencyManager::PerformInterlockedTwoPhaseShutdown C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\dependency\_manager.cc:127  

#6 0x7ff8f917d7f8 in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:909  

#7 0x7ff8f91817ef in ProfileImpl::~ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:856  

#8 0x7ff8f9193f47 in ProfileDestroyer::DestroyOriginalProfileNow C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:133  

#9 0x7ff8f919377b in ProfileDestroyer::DestroyProfileWhenAppropriate C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_destroyer.cc:61  

#10 0x7ff8f659efcf in ProfileManager::ProfileInfo::~ProfileInfo C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1629  

#11 0x7ff8f65a5d23 in std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) >::reset C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h:315  

#12 0x7ff8f65a621a in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2422  

#13 0x7ff8f65a616f in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::\_\_map\_value\_compare<base::FilePath,std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > >,std::\_\_1::less[base::FilePath](javascript:void(0);),1>,std::\_\_1::allocator<std::\_\_1::\_\_value\_type<base::FilePath,std::\_\_1::unique\_ptr<ProfileManager::ProfileInfo,std::\_\_1::default\_delete[ProfileManager::ProfileInfo](javascript:void(0);) > > > >::\_\_erase\_unique[base::FilePath](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2445  

#14 0x7ff8f659c5ee in ProfileManager::RemoveProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1734  

#15 0x7ff8f659c327 in ProfileManager::DeleteProfileIfNoKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1456  

#16 0x7ff8f659bd17 in ProfileManager::RemoveKeepAlive C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1418  

#17 0x7ff8f6780c0a in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#18 0x7ff8f925562f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:358  

#19 0x7ff8f9254d48 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#20 0x7ff8f6829846 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#21 0x7ff8f6827ad8 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#22 0x7ff8f9256a45 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:463  

#23 0x7ff8f6700903 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#24 0x7ff8efa73bd9 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1007  

#25 0x7ff8efa78e91 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#26 0x7ff8efa6d672 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:49  

#27 0x7ff8f2421870 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:641

previously allocated by thread T0 here:  

#0 0x7ff7960c237b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff908ef2a6a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff8fbf42e8d in feedback::FeedbackUploaderFactoryChrome::BuildServiceInstanceFor C:\b\s\w\ir\cache\builder\src\chrome\browser\feedback\feedback\_uploader\_factory\_chrome.cc:48  

#3 0x7ff8f87b06ff in BrowserContextKeyedServiceFactory::BuildServiceInstanceFor C:\b\s\w\ir\cache\builder\src\components\keyed\_service\content\browser\_context\_keyed\_service\_factory.cc:95  

#4 0x7ff8f786e644 in KeyedServiceFactory::GetServiceForContext C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\keyed\_service\_factory.cc:80  

#5 0x7ff8fa1d9ae9 in DependencyManager::CreateContextServices C:\b\s\w\ir\cache\builder\src\components\keyed\_service\core\dependency\_manager.cc:87  

#6 0x7ff8f87afba8 in BrowserContextDependencyManager::DoCreateBrowserContextServices C:\b\s\w\ir\cache\builder\src\components\keyed\_service\content\browser\_context\_dependency\_manager.cc:46  

#7 0x7ff8f917fff9 in ProfileImpl::OnLocaleReady C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:1104  

#8 0x7ff8f91799d4 in ProfileImpl::OnPrefsLoaded C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:1145  

#9 0x7ff8f9176d22 in ProfileImpl::ProfileImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:535  

#10 0x7ff8f9175eb4 in Profile::CreateProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_impl.cc:365  

#11 0x7ff8f659a3c9 in ProfileManager::CreateProfileHelper C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1341  

#12 0x7ff8f658e9a0 in ProfileManager::CreateAndInitializeProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1772  

#13 0x7ff8f658c350 in ProfileManager::GetProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:744  

#14 0x7ff8f658de56 in ProfileManager::GetActiveUserOrOffTheRecordProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1695  

#15 0x7ff8f658e008 in ProfileManager::GetActiveUserProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:706  

#16 0x7ff90180c8c9 in FeedbackDialog::CreateOrShow C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\feedback\feedback\_dialog.cc:57  

#17 0x7ff8fdd607c3 in chrome::ShowFeedbackPage C:\b\s\w\ir\cache\builder\src\chrome\browser\feedback\show\_feedback\_page.cc:222  

#18 0x7ff8fdd6020a in chrome::ShowFeedbackPage C:\b\s\w\ir\cache\builder\src\chrome\browser\feedback\show\_feedback\_page.cc:187  

#19 0x7ff90648d245 in `anonymous namespace'::ShowFeedbackPage C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\toolbar\chrome_labs_item_view.cc:41 #20 0x7ff90648f789 in base::internal::FunctorTraits<void (\*)(Browser \*, std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> >, std::__1::basic_string<char16_t,std::__1::char_traits<char16_t>,std::__1::allocator<char16_t> >),void>::Invoke<void (\*const &)(Browser \*, std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> >, std::__1::basic_string<char16_t,std::__1::char_traits<char16_t>,std::__1::allocator<char16_t> >),Browser \*,const std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > &,const std::__1::basic_string<char16_t,std::__1::char_traits<char16_t>,std::__1::allocator<char16_t> > &> C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:426 #21 0x7ff90648f520 in base::internal::Invoker<base::internal::BindState<void (\*)(Browser \*, std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> >, std::__1::basic_string<char16_t,std::__1::char_traits<char16_t>,std::__1::allocator<char16_t> >),base::internal::UnretainedWrapper<Browser>,std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> >,std::__1::basic_string<char16_t,std::__1::char_traits<char16_t>,std::__1::allocator<char16_t> > >,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:766 #22 0x7ff8f649cde9 in base::internal::Invoker<base::internal::BindState<`lambda at ../../ui/views/controls/button/button.cc:110:31',base::RepeatingCallback<void ()> >,void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:766  

#23 0x7ff8f649a7bb in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:632  

#24 0x7ff8f6496b5d in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:66  

#25 0x7ff8f8dfb9ca in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button\_controller.cc:59  

#26 0x7ff8f64d4fe0 in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3068  

#27 0x7ff8ffce3536 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\components\feedback\feedback\_data.cc:132 in feedback::FeedbackData::SendReport  

Shadow bytes around the buggy address:  

0x047e938f84b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x047e938f84c0: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x047e938f84d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x047e938f84e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x047e938f84f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x047e938f8500: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd  

0x047e938f8510: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x047e938f8520: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x047e938f8530: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x047e938f8540: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x047e938f8550: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==8372==ABORTING

## Attachments

- [screen.mp4](attachments/screen.mp4) (video/mp4, 8.7 MB)

## Timeline

### [Deleted User] (2021-10-20)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-10-20)

jimmyxgong@, please take a look? Marking as Low severity due to user interaction required, I think we might even want to remove security labels unless we determine that this is more easily exploitable in some way.

[Monorail components: UI>Browser>ReportAnIssue]

### [Deleted User] (2021-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-20)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2021-10-28)

+xiangdongkong@ PTAL

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### xi...@google.com (2021-12-10)

owone@google.com Can you find someone from the browser team to take a look? 

### ow...@google.com (2021-12-13)

[Empty comment from Monorail migration]

### dp...@chromium.org (2021-12-14)

cc'ing OWNERS from [1], since the problem seems to happen within 

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/feedback/OWNERS
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/feedback/feedback_data.cc

### mu...@chromium.org (2021-12-14)

[Empty comment from Monorail migration]

### mu...@chromium.org (2021-12-14)

Copying from the stack trace above:

Used by:
    #0 0x7ff8f88d2d65 in feedback::FeedbackData::SendReport C:\b\s\w\ir\cache\builder\src\components\feedback\feedback_data.cc:132


Freed by:

    #1 0x7ff900032e35 in feedback::FeedbackUploaderChrome::~FeedbackUploaderChrome C:\b\s\w\ir\cache\builder\src\chrome\browser\feedback\feedback_uploader_chrome.cc:79

This seem like entirely a problem within Feedback. Is this something you can look at, Xiangdong?

[Monorail components: OS>Systems>Feedback]

### xi...@google.com (2021-12-14)

I do not think we can trigger the issue on Chome OS. This makes it hard to troubleshoot and verify fix.  I think it will be an easier task for the Browser team. 

### dp...@chromium.org (2021-12-14)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Profiles]

### ze...@chromium.org (2021-12-14)

[Empty comment from Monorail migration]

### xi...@google.com (2021-12-15)

nicolaso@chromium.org Do you think this one has been fixed by 1228248? Thanks

### xi...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### al...@chromium.org (2021-12-23)

Continuing our discussion from https://crbug.com/chromium/1282006 here, since this is a canonical bug now.

from https://crbug.com/1282006#c12:
> It is normal that FeedbackData outlives the dialog for after the user sends a report, the dialog will be closed shortly. The backend may need to gather more logs before uploading the data and thus may take some time. So yes, a better solution may be to reject the submit request in the first place if the profile used to open the feedback UI has been deleted. The question is how to detect the profile change? 

If FeedbackDialog is the last think that keeps a Profile alive (i.e there are no other browser windows from this profile), you might run into this risk quite often, since the profile will be destroyed as soon as the dialog is closed.

There have been a recent discussion about how to organize the code that depends on Profile* [1] (sorry, Google-internal links). I think [2] provides an excellent list of recommendations. In general, it is not recommended to observe Profile lifetime directly (though, it's possible through ProfileObserver). There are usually better ways.

In your case, FeedbackData depends on a FeedbackUploader and not on a Profile* itself. Weak pointer (https://crrev.com/c/3347697) already eliminates the risk of UaF. FeedbackData might be more proactive and cancel all running tasks as soon as FeedbackUploader is destroyed. This can be implemented by exposing observer methods from FeedbackUploader and subscribing FeedbackData to observe FeedbackUploader.

[1] https://groups.google.com/a/google.com/g/chromium-dev-internal/c/EM963SZmgrs/m/oKF79EkzAAAJ
[2] https://groups.google.com/a/google.com/g/chromium-dev-internal/c/EM963SZmgrs/m/6Br0HAs_AAAJ

### gi...@appspot.gserviceaccount.com (2021-12-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6b080f05f59dbf5ef53fafed634de2ec0bf4fb8e

commit 6b080f05f59dbf5ef53fafed634de2ec0bf4fb8e
Author: xiangdong kong <xiangdongkong@google.com>
Date: Wed Dec 29 00:08:37 2021

change feedback uploader member in feedback data from raw_ptr to weakptr

This is to fix the security-related heap-use-after-free issue that
occurs in the following scenario:
1) Open the feedback app, enter some description
2) Delete existing profile(s)
3) Send the feedback

This is a bug in the feedback::FeedbackData class which can outlive a
profile while one of its non-owned members, i.e. uploader_, a
keyedService, gets destroyed with a profile.

The FeedbackData is initialized after user hits "send" to submit a
report. It is an async process to collect different pieces of data.
Since it is not recommended to observe Profile lifetime directly, we can
either store the uploader as a weak_ptr or refactor the
feedback::FeedbackUploader to expose observer method to be subscribed by
FeedbackData. The latter is way more complex to implement without
obvious benefit. The scenario is a rare use case too. Therefore, I here
choose the weak_ptr approach so that if the uploader_ has been
destroyed when FeedbackData is about to upload the report, FeedbackData
will skip calling the uploader_ to upload the report. Thus, the UaF bug
is avoided.

This is not a perfect solution from the user's perspective. Ideally, if
the feedback app is opened with a profile, and then the profile is
deleted, the app should be closed or notify the user that it should be
reopened in order to send a report due to profile change. But this is a
rare case and outside of the scope.

Bug: 1261713
Change-Id: I5092fdb10b0b1fefeca327d86019f569c3fd0367
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3347697
Reviewed-by: Alex Ilin <alexilin@chromium.org>
Reviewed-by: Miriam Zimmerman <mutexlox@chromium.org>
Commit-Queue: Xiangdong Kong <xiangdongkong@google.com>
Cr-Commit-Position: refs/heads/main@{#954372}

[modify] https://crrev.com/6b080f05f59dbf5ef53fafed634de2ec0bf4fb8e/components/feedback/feedback_data_unittest.cc
[modify] https://crrev.com/6b080f05f59dbf5ef53fafed634de2ec0bf4fb8e/components/feedback/feedback_data.cc
[modify] https://crrev.com/6b080f05f59dbf5ef53fafed634de2ec0bf4fb8e/extensions/browser/api/feedback_private/feedback_service_unittest.cc
[modify] https://crrev.com/6b080f05f59dbf5ef53fafed634de2ec0bf4fb8e/extensions/browser/api/feedback_private/feedback_private_api.cc
[modify] https://crrev.com/6b080f05f59dbf5ef53fafed634de2ec0bf4fb8e/components/feedback/feedback_data.h


### xi...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-23)

Thank you for this report, Khalil. The VRP Panel has decided to award you $1,000 for this report given that this is not web accessible, the amount of user interaction and unusual, non-standard workflow required to trigger this issue. Thank you for your efforts! 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-04-12)

This issue was migrated from crbug.com/chromium/1261713?no_tracker_redirect=1

[Multiple monorail components: OS>Systems>Feedback, UI>Browser>Profiles, UI>Browser>ReportAnIssue]
[Monorail mergedwith: crbug.com/chromium/1282006]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057665)*
