# Security: UaF in FileSelectHelper::FileSelectedWithExtraInfo 

| Field | Value |
|-------|-------|
| **Issue ID** | [40080721](https://issues.chromium.org/issues/40080721) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | ch...@gmail.com |
| **Assignee** | hi...@chromium.org |
| **Created** | 2014-10-26 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: Google Chrome 40.0.2200.1 canary SyzyASan  

Operating System: Win7

**REPRODUCTION CASE**

1. Launch Chrome Canary.
2. Launch Incognito window, Ctrl+N.
3. Open PoC.html on Incognito window as a fresh page (as in 1.png) and click on  
   
   the input element to get the select file dialog then as you can  
   
   see the page "PoC.html"must be closed (Incognito window) after executing window.close() method as in 2.png.
4. Select some file and click on Open button.
5. Boom!!

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

eax=0017f420 ebx=0017f458 ecx=01f3d230 edx=00000037 esi=f01dc9a6 edi=1052d8c0  

eip=5bc4cad9 esp=0017f410 ebp=0017f43c iopl=0 nv up ei pl nz na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010202  

chrome\_5aaf0000!FileSelectHelper::FileSelectedWithExtraInfo+0x2c:  

5bc4cad9 ff9694000000 call dword ptr [esi+0x94] ds:0023:f01dca3a=????????  

0:000> k  

ChildEBP RetAddr  

0017f43c 5b73bb47 chrome\_5aaf0000!FileSelectHelper::FileSelectedWithExtraInfo+0x2c [c:\b\build\slave\win\build\src\chrome\browser\file\_select\_helper.cc @ 125]  

0017f4a4 5b692154 chrome\_5aaf0000!Browser::FileSelected+0x30 [c:\b\build\slave\win\build\src\chrome\browser\ui\browser.cc @ 1930]  

0017f4bc 5b6928d2 chrome\_5aaf0000!`anonymous namespace'::SelectFileDialogImpl::FileSelected+0x1a [c:\b\build\slave\win\build\src\ui\shell_dialogs\select_file_dialog_win.cc @ 552] 0017f4d8 5b69297b chrome_5aaf0000!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall` anonymous namespace'::SelectFileDialogImpl::\*)(base::FilePath const &,int,void \*,ui::BaseShellDialogImpl::RunState)>,void \_\_cdecl(`anonymous namespace'::SelectFileDialogImpl \* const &,base::FilePath const &,unsigned int const &,void \* const &,ui::BaseShellDialogImpl::RunState const &)>::MakeItSo+0x23 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 993] 0017f4fc 5ab4f682 chrome_5aaf0000!base::internal::Invoker<5,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall` anonymous namespace'::SelectFileDialogImpl::\*)(base::FilePath const &,int,void \*,ui::BaseShellDialogImpl::RunState)>,void \_\_cdecl(`anonymous namespace'::SelectFileDialogImpl \*,base::FilePath const &,int,void \*,ui::BaseShellDialogImpl::RunState),void __cdecl(`anonymous namespace'::SelectFileDialogImpl \*,base::FilePath,unsigned int,void \*,ui::BaseShellDialogImpl::RunState)>,void \_\_cdecl(`anonymous namespace'::SelectFileDialogImpl \*,base::FilePath const &,int,void \*,ui::BaseShellDialogImpl::RunState)>::Run+0x25 [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 1811]  

0017f5a4 5ab4f2a9 chrome\_5aaf0000!base::debug::TaskAnnotator::RunTask+0x32c [c:\b\build\slave\win\build\src\base\debug\task\_annotator.cc @ 62]  

0017f5dc 5ab4ed53 chrome\_5aaf0000!base::MessageLoop::RunTask+0xe4 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 449]  

0017f720 5abd4b43 chrome\_5aaf0000!base::MessageLoop::DoWork+0x375 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 566]  

0017f74c 5ab4e8f1 chrome\_5aaf0000!base::MessagePumpForUI::DoRunLoop+0x5f [c:\b\build\slave\win\build\src\base\message\_loop\message\_pump\_win.cc @ 203]  

0017f788 5ab45e0c chrome\_5aaf0000!base::MessageLoop::StartHistogrammer+0xa7 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 535]  

0017f798 5ab4e74c chrome\_5aaf0000!tracked\_objects::TaskStopwatch::TaskStopwatch+0x3f [c:\b\build\slave\win\build\src\base\tracked\_objects.cc @ 860]  

0017f7c0 5adec3e5 chrome\_5aaf0000!base::RunLoop::Run+0x2d [c:\b\build\slave\win\build\src\base\run\_loop.cc @ 55]  

0017f808 5adec324 chrome\_5aaf0000!ChromeBrowserMainParts::MainMessageLoopRun+0xa4 [c:\b\build\slave\win\build\src\chrome\browser\chrome\_browser\_main.cc @ 1614]  

0017f81c 5adec2ec chrome\_5aaf0000!content::BrowserMainLoop::RunMainMessageLoopParts+0x2d [c:\b\build\slave\win\build\src\content\browser\browser\_main\_loop.cc @ 761]  

0017f82c 5ab10ad9 chrome\_5aaf0000!content::BrowserMainRunnerImpl::Run+0x13 [c:\b\build\slave\win\build\src\content\browser\browser\_main\_runner.cc @ 223]  

0017f85c 5ab108c0 chrome\_5aaf0000!content::BrowserMain+0x83 [c:\b\build\slave\win\build\src\content\browser\browser\_main.cc @ 26]  

0017f870 5ab1083c chrome\_5aaf0000!content::RunNamedProcessTypeMain+0x61 [c:\b\build\slave\win\build\src\content\app\content\_main\_runner.cc @ 419]  

0017f8d0 5aafc663 chrome\_5aaf0000!content::ContentMainRunnerImpl::Run+0x66 [c:\b\build\slave\win\build\src\content\app\content\_main\_runner.cc @ 768]  

0017f8e0 5aafb6c7 chrome\_5aaf0000!content::ContentMain+0x23 [c:\b\build\slave\win\build\src\content\app\content\_main.cc @ 19]  

\*\*\* WARNING: Unable to verify checksum for chrome.exe  

0017f928 001b50af chrome\_5aaf0000!ChromeMain+0x61 [c:\b\build\slave\win\build\src\chrome\app\chrome\_main.cc @ 60]

## Attachments

- [1.png](attachments/1.png) (image/png, 60.1 KB)
- [PoC.html](attachments/PoC.html) (text/html, 111 B)
- [2.png](attachments/2.png) (image/png, 85.0 KB)

## Timeline

### in...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### ch...@gmail.com (2014-10-26)

[Comment Deleted]

### ch...@gmail.com (2014-10-26)

[Comment Deleted]

### ch...@gmail.com (2014-10-26)

I think this is only a problem on Windows, but I could be wrong.

When the page closes itself while the select file dialog is open, FileSelectHelper::FileSelectedWithExtraInfo was called after the listener has been destroyed.

### cl...@chromium.org (2014-10-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-03)

hirono@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### wf...@chromium.org (2014-11-03)

I could not replicate this in syzyasan 38.0.2124.1 (the closest I could find to stable) but could in sysyasan 40.0.2200.1.  I'll try do do a manual bisect, and will update the impact appropriately.

### wf...@chromium.org (2014-11-03)

manually bisected to somewhere between 40.0.2184.0 and 40.0.2185.0

https://chromium.googlesource.com/chromium/src/+log/40.0.2184.0..40.0.2185.0?pretty=fuller&n=10000

suspect 22de64a3653834acad2580ded12857385e3d4d65 as this matches https://crbug.com/chromium/427272#c5 and behavior seen.

### wf...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-03)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### er...@chromium.org (2014-11-04)

I don't have a Windows machine, so I'm not a great candidate for fixing this bug. That being said, the source of the crash is obvious, and reverting my CL doesn't actually fix the problem. I'm reassigning to hirono, to find an appropriate person to fix the problem.

Overview: The window gets closed, but the file picker is still present. The file picker has a pointer reference to a Profile (the incognito profile), which has already been destroyed. It attempts to dereference the pointer and crashes.

The reason my CL exposed this crash is that it changed the order of the logic in FileSelectedWithExtraInfo to match the logic order in MultiFilesSelectedWithExtraInfo. I strongly suspect that if you used an <input type="file" multiple> and selected multiple files, Chrome would crash regardless of the presence of my CL. Reverting my CL doesn't solve the problem.

There are a couple of obvious solutions that come to mind:
1) On Mac, the window can't be window.closed() while the file picker is open. The logic on Windows can be changed to mirror this logic.
2) If the render_view_host_ has been destroyed, assume that the Profile* has been destroyed. The logic in FileSelectedWithExtraInfo (prior to my CL) used to implicitly rely on this assumption. We could change FileSelectedWithExtraInfo and MultiFilesSelectedWithExtraInfo to match this behavior. While this logic works, it's dangerous, since it makes assumptions about the lifetime of the Profile vs the lifetime of the render_view_host_, which are not necessarily tied together.
3) Watch for destruction of the Profile/window, and clear the Profile when this happens (or set some other flag). Update the code in file_select_helper.cc to use this flag.

### hi...@chromium.org (2014-11-05)

Sorry for missing the issue and thank you for explanation!

I made a CL crbug.com/702773003, but I also don't have windows machine.
@wfh - Could you help me to check the CL solves the issue?

Thanks!


### hi...@chromium.org (2014-11-05)

crbug.com/702773003 -> crrev.com/702773003

### bu...@chromium.org (2014-11-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a4a32af218cf03ac89db4a27d12681f8a1ba9108

commit a4a32af218cf03ac89db4a27d12681f8a1ba9108
Author: hirono <hirono@chromium.org>
Date: Fri Nov 07 03:17:29 2014

Add existence checks for Profile to FileSelectHelper.

Previously FileSelectHelper may access |profile_| member after the |profile_| is
deleted.

BUG=427272
TEST=None

Review URL: https://codereview.chromium.org/702773003

Cr-Commit-Position: refs/heads/master@{#303171}

[modify] https://chromium.googlesource.com/chromium/src.git/+/a4a32af218cf03ac89db4a27d12681f8a1ba9108/chrome/browser/file_select_helper.cc


### hi...@chromium.org (2014-11-07)

I cannot check it on windows. Could someone verify it? Thanks!


### cl...@chromium.org (2014-11-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### ch...@gmail.com (2014-11-08)

This is fixed on latest canary. Thank you!

### in...@chromium.org (2014-12-15)

regression fixed before branch point, no merge needed.

### ti...@google.com (2015-01-22)

$1000 for this report.

### cl...@chromium.org (2015-02-13)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/427272?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/427200, crbug.com/chromium/427518]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080721)*
