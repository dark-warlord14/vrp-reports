# Security: heap-after-free on components/exo/extended_drag_source.cc (Lacros)

| Field | Value |
|-------|-------|
| **Issue ID** | [40059790](https://issues.chromium.org/issues/40059790) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Shell>UIFoundations |
| **Platforms** | ChromeOS |
| **Reporter** | rh...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-05-29 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When dragging a new tab the |GetDisplayNearestWindow| is holding drag\_source\_window\_. Since in the first attempt detaching tab |GetDisplayNearestWindow| didn't get notify if the drag\_source\_window\_ has been released then the second attempt join/merge into browser cause UaF.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/exo/extended_drag_source.cc;drc=b0092c498210587441a9fcc2ff92f45acf54c632;l=362>

**VERSION**  

Chrome Version: 104.0.5090.0 + Dev  

Operating System: Linux-ChromeOS

**REPRODUCTION CASE**  

(1) Open new browser and add one NTP.  

(2) Detach one tab then merge the tab.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==414511==ERROR: AddressSanitizer: heap-use-after-free on address 0x61500077c2f8 at pc 0x7f86bf8eca4f bp 0x7ffc54cc0480 sp 0x7ffc54cc0478  

READ of size 8 at 0x61500077c2f8 thread T0 (chrome)  

SCARINESS: 51 (8-byte-read-heap-use-after-free)  

2022-05-29T03:09:52.074618Z ERROR chrome[414511:414550]: [object\_proxy.cc(623)] Failed to call method: org.chromium.debugd.GetPerfOutputV2: object\_path= /org/chromium/debugd: org.freedesktop.DBus.Error.ServiceUnknown: The name org.chromium.debugd was not provided by any .service files  

#0 0x7f86bf8eca4e in operator bool base/memory/raw\_ptr.h:806:59  

#1 0x7f86bf8eca4e in IsRootWindow ui/aura/window.h:216:40  

#2 0x7f86bf8eca4e in GetRootWindow ui/aura/window.cc:340:10  

#3 0x7f86bf8eca4e in aura::Window::GetRootWindow() ui/aura/window.cc:336:41  

#4 0x7f86bbc5e64a in ash::ScreenAsh::GetDisplayNearestWindow(aura::Window\*) const ash/display/screen\_ash.cc:139:45  

#5 0x55aed408f1f7 in exo::ExtendedDragSource::OnDraggedWindowVisibilityChanged(bool) components/exo/extended\_drag\_source.cc:362:48  

#6 0x7f86bf8f6c45 in aura::Window::NotifyWindowVisibilityChangedAtReceiver(aura::Window\*, bool) ui/aura/window.cc:1215:14  

#7 0x7f86bf8f671c in aura::Window::NotifyWindowVisibilityChangedDown(aura::Window\*, bool) ui/aura/window.cc:1221:8  

#8 0x7f86bf8f4a5b in aura::Window::NotifyWindowVisibilityChanged(aura::Window\*, bool) ui/aura/window.cc:1202:8  

#9 0x7f86bf8ed03f in aura::Window::SetVisibleInternal(bool) ui/aura/window.cc:1018:3  

#10 0x7f86beff0fcb in views::NativeWidgetAura::Show(ui::WindowShowState, gfx::Rect const&) ui/views/widget/native\_widget\_aura.cc:615:12  

#11 0x7f86bef8ea7e in views::Widget::Show() ui/views/widget/widget.cc:726:23  

#12 0x55aed40b6238 in exo::ShellSurfaceBase::CommitWidget() components/exo/shell\_surface\_base.cc:1734:14  

#13 0x55aed40b5691 in exo::ShellSurfaceBase::OnSurfaceCommit() components/exo/shell\_surface\_base.cc:848:3  

#14 0x55aed405eda3 in exo::Surface::Commit() components/exo/surface.cc:805:16  

#15 0x55aedb69a294 in ffi\_call\_unix64 crtstuff.c

0x61500077c2f8 is located 248 bytes inside of 504-byte region [0x61500077c200,0x61500077c3f8)  

freed by thread T0 (chrome) here:  

#0 0x55aece4d37dd in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x7f86bef8e511 in views::Widget::CloseNow() ui/views/widget/widget.cc:705:19  

#2 0x55aed40ae210 in exo::ShellSurfaceBase::~ShellSurfaceBase() components/exo/shell\_surface\_base.cc:358:14  

#3 0x55aed40a5e07 in exo::ShellSurface::~ShellSurface() components/exo/shell\_surface.cc:132:1  

#4 0x55aed40d3591 in ~XdgShellSurface components/exo/xdg\_shell\_surface.cc:27:38  

#5 0x55aed40d3591 in exo::XdgShellSurface::~XdgShellSurface() components/exo/xdg\_shell\_surface.cc:27:37  

#6 0x55aece50b91d in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#7 0x55aece50b91d in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#8 0x55aece50b91d in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#9 0x55aece50b91d in ~WaylandXdgSurface components/exo/wayland/xdg\_shell.cc:783:39  

#10 0x55aece50b91d in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#11 0x55aece50b91d in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#12 0x55aece50b91d in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#13 0x55aece50b91d in void exo::wayland::DestroyUserData[exo::wayland::WaylandXdgSurface](javascript:void(0);)(wl\_resource\*) components/exo/wayland/server\_util.h:40:3  

#14 0x55aed410ba02 in destroy\_resource third\_party/wayland/src/src/wayland-server.c:724:3  

#15 0x55aed410b89e in wl\_resource\_destroy third\_party/wayland/src/src/wayland-server.c:741:2  

#16 0x55aedb69a294 in ffi\_call\_unix64 crtstuff.c

previously allocated by thread T0 (chrome) here:  

#0 0x55aece4d2f7d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x7f86befec947 in views::NativeWidgetAura::NativeWidgetAura(views::internal::NativeWidgetDelegate\*) ui/views/widget/native\_widget\_aura.cc:105:15  

#2 0x7f86beff571b in views::internal::NativeWidgetPrivate::CreateNativeWidget(views::internal::NativeWidgetDelegate\*) ui/views/widget/native\_widget\_aura.cc:1196:14  

#3 0x7f86bef879eb in CreateNativeWidget ui/views/widget/widget.cc:85:10  

#4 0x7f86bef879eb in views::Widget::Init(views::Widget::InitParams) ui/views/widget/widget.cc:382:20  

#5 0x55aed40baae2 in exo::ShellSurfaceBase::CreateShellSurfaceWidget(ui::WindowShowState) components/exo/shell\_surface\_base.cc:1312:12  

#6 0x55aed40aae4f in exo::ShellSurface::OnPreWidgetCommit() components/exo/shell\_surface.cc:526:5  

#7 0x55aed40b5685 in exo::ShellSurfaceBase::OnSurfaceCommit() components/exo/shell\_surface\_base.cc:845:8  

#8 0x55aed405eda3 in exo::Surface::Commit() components/exo/surface.cc:805:16  

#9 0x55aedb69a294 in ffi\_call\_unix64 crtstuff.c

SUMMARY: AddressSanitizer: heap-use-after-free base/memory/raw\_ptr.h:806:59 in operator bool  

Shadow bytes around the buggy address:  

0x0c2a800e7800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800e7810: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800e7820: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800e7830: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a800e7840: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c2a800e7850: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]  

0x0c2a800e7860: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800e7870: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c2a800e7880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a800e7890: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800e78a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==414511==ABORTING

## Attachments

- [screencast__00083.webm](attachments/screencast_00083.webm) (video/webm, 2.5 MB)
- [screencast_00022.webm](attachments/screencast_00022.webm) (video/webm, 2.9 MB)
- [screencast_00021.webm](attachments/screencast_00021.webm) (video/webm, 2.7 MB)

## Timeline

### [Deleted User] (2022-05-29)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-05-30)

Over to ChromeOS triage

### ps...@google.com (2022-06-07)

[Empty comment from Monorail migration]

[Monorail components: UI>Shell]

### af...@chromium.org (2022-06-07)

[Empty comment from Monorail migration]

[Monorail components: -UI>Shell UI>Shell>UIFoundations]

### ps...@google.com (2022-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-08)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-06-08)

Thanks for the report and the analysis, I'll investigate.

### al...@chromium.org (2022-06-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d167aaa3da3277a4c583db1812de88eba928895d

commit d167aaa3da3277a4c583db1812de88eba928895d
Author: Addison Luh <aluh@chromium.org>
Date: Thu Jun 09 07:31:54 2022

[lacros] Fix use-after-free when merging/splitting browser tab.

When merging and splitting a browser tab from a single-tab window into another browser window, there's a race condition between when exo destroys the drag source window and when the dragged window is being shown. The dragged window uses the drag source window to determine its initial bounds on the screen, but when the drag source window has already been freed, it accesses freed memory, causing the use-after-free memory violation.

The fix makes the ExtendedDragSource instance observe the drag source window to detect when it has been destroyed and falls back to a best guess for where to show the dragged window.

Bug: 1330125
Change-Id: Id02e034355fef9eafd3a078e9a121c5be44afc65
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3697499
Reviewed-by: Mitsuru Oshima <oshima@chromium.org>
Auto-Submit: Addison Luh <aluh@chromium.org>
Commit-Queue: Mitsuru Oshima <oshima@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1012373}

[modify] https://crrev.com/d167aaa3da3277a4c583db1812de88eba928895d/components/exo/extended_drag_source.cc
[modify] https://crrev.com/d167aaa3da3277a4c583db1812de88eba928895d/components/exo/extended_drag_source_unittest.cc
[modify] https://crrev.com/d167aaa3da3277a4c583db1812de88eba928895d/components/exo/extended_drag_source.h


### al...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-09)

Merge rejected: M103 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-06-09)

Thanks aluh@ for quick fix!

### [Deleted User] (2022-06-09)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ps...@google.com (2022-06-13)

[Empty comment from Monorail migration]

### ps...@google.com (2022-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-29)

Congratulations, Rheza! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### rh...@gmail.com (2022-06-29)

amy@,

Thanks for the rewards. I was hoping the reward was similar to another browser crash or remote attack from the browser, and I was shocked by the achievement rewards. Unfortunately, the achievement reward seems lower than usual remote exploit from the browser, the whole browser crashes, and Heap UaF too. I knew this issue could perform from a remote. My mistake didn't provide HTML or plugins, but since this UaF issue can be triggered with a simple movement/poc, I consider not providing that ( crafted html or plugin ) stuff. 

In order to get a re-assessment, I'm deciding to borrow the PoC from two public bugs. For example, I took two different bugs that PoC were similar with my issue. Tested with the fix removed.
(1) https://bugs.chromium.org/p/chromium/issues/detail?id=1202598 (plugin needed, refer to screencast_00021)
(2) https://bugs.chromium.org/p/chromium/issues/detail?id=1197436 (crafted html, refer to screencast_00022)
 
I look forward to hearing good news

### am...@chromium.org (2022-06-30)

Hi Rheza, I'm happy to put this one in the queue for reassessment for a potential reward amount adjustment. 
Just a few things you should know up front to help level-set expectations: 

1) this bug isn't remote exploitable and requires a user interaction of dragging to trigger this bug; these are some substantial mitigation that reduce exploitability potential, similar to other bugs you have submitted and rewarded in this reward range

2) the two bugs you link for comparison in https://crbug.com/chromium/1330125#c25 are older bugs and received VRP reward decisions over a year ago - in April of 2021; since that time we have updated our policies around rewards for mitigated bugs. This update was directly communicated to the researcher community in February 2022 as well as on the VRP rules, rewards, and policies page [1]

"We have recently updated the page to include clarifying information to help answer some of the questions you have asked us about particular reward decisions. 
There is a recent trend of reports away from issues triggered by remote content to issues that are strongly or solely dependent on user interaction. While we appreciate your efforts to discover and report these bugs, these issues are not as impactful or exploitable as those that demonstrate exploitability through remote content. 

To reduce ambiguity and to provide more clarification, we have updated our Rewards section on our Rules page:
The amounts listed are for good quality reports that don't require complex or unlikely user interaction. Reports of issues that rely heavily or solely on user interaction, instead of being triggered by remote content, will generally receive significantly reduced rewards. Less convincing or more constrained bug submissions will likely qualify for reduced reward amounts, as chosen at the discretion of the reward panel.
Reports of issues that involve implausible interaction, interactions a user would not be realistically convinced to perform, may not be rewarded. " 

The same bugs you link would be receiving reduced rewards if they were reported now/since that policy change. 

I hope this helps provide some context. 

[1] https://g.co/chrome/vrp 

### am...@chromium.org (2022-07-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1330125?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1324713]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059790)*
