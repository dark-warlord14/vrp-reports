# Security: heap-use-after-free on IsLacrosWindow ash/drag_drop/tab_drag_drop_delegate.cc (Lacros)

| Field | Value |
|-------|-------|
| **Issue ID** | [40059882](https://issues.chromium.org/issues/40059882) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | OS>LaCrOS>Tablet, UI>Browser>TopChrome>TabStrip>ThumbnailTabStrip |
| **Reporter** | rh...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2022-06-07 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When do dragging tab groups into splitview, the browser is crashed. Tested on Chromium 104.0.5106.0, before this version I see no crash.

**VERSION**  

Chrome Version: 104.0.5106.0 + Lacros  

Operating System: linux-chromeOS

**REPRODUCTION CASE**  

(\*) Tablet mode Lacros  

(\*) Have at least one tabgroups, drag over into splitview and release the drag.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

==224316==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000572230 at pc 0x7f6a9563393b bp 0x7ffd8f319900 sp 0x7ffd8f3198f8  

READ of size 8 at 0x615000572230 thread T0 (chrome)  

SCARINESS: 51 (8-byte-read-heap-use-after-free)  

#0 0x7f6a9563393a in \_\_root buildtools/third\_party/libc++/trunk/include/\_\_tree:1082:59  

#1 0x7f6a9563393a in find<const void \*> buildtools/third\_party/libc++/trunk/include/\_\_tree:2480:45  

#2 0x7f6a9563393a in find buildtools/third\_party/libc++/trunk/include/map:1445:68  

#3 0x7f6a9563393a in ui::PropertyHandler::GetPropertyInternal(void const\*, long, bool) const ui/base/class\_property.cc:72:36  

#4 0x7f6a90372495 in IsLacrosWindow ash/drag\_drop/tab\_drag\_drop\_delegate.cc:68:36  

#5 0x7f6a90372495 in ash::TabDragDropDelegate::OnNewBrowserWindowCreated(gfx::Point const&, aura::Window\*) ash/drag\_drop/tab\_drag\_drop\_delegate.cc:169:20  

#6 0x55e4b7a9311b in Run base/callback.h:143:12  

#7 0x55e4b7a9311b in CrosapiNewWindowDelegate::WindowObserver::OnWindowVisibilityChanged(aura::Window\*, bool) chrome/browser/ui/ash/crosapi\_new\_window\_delegate.cc:68:25  

#8 0x7f6a9401bc45 in aura::Window::NotifyWindowVisibilityChangedAtReceiver(aura::Window\*, bool) ui/aura/window.cc:1215:14  

#9 0x7f6a9401b71c in aura::Window::NotifyWindowVisibilityChangedDown(aura::Window\*, bool) ui/aura/window.cc:1221:8  

#10 0x7f6a94019a5b in aura::Window::NotifyWindowVisibilityChanged(aura::Window\*, bool) ui/aura/window.cc:1202:8  

#11 0x7f6a9401203f in aura::Window::SetVisibleInternal(bool) ui/aura/window.cc:1018:3  

#12 0x7f6a9370489b in views::NativeWidgetAura::Show(ui::WindowShowState, gfx::Rect const&) ui/views/widget/native\_widget\_aura.cc:615:12  

#13 0x7f6a936a234e in views::Widget::Show() ui/views/widget/widget.cc:726:23  

#14 0x55e4b26d9190 in exo::ShellSurfaceBase::CommitWidget() components/exo/shell\_surface\_base.cc:1750:14  

#15 0x55e4b26d85e9 in exo::ShellSurfaceBase::OnSurfaceCommit() components/exo/shell\_surface\_base.cc:857:3  

#16 0x55e4b2681913 in exo::Surface::Commit() components/exo/surface.cc:805:16  

#17 0x55e4b9d19b24 in ffi\_call\_unix64 crtstuff.c

0x615000572230 is located 176 bytes inside of 504-byte region [0x615000572180,0x615000572378)  

freed by thread T0 (chrome) here:  

#0 0x55e4acad6d9d in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x7f6a936a1de1 in views::Widget::CloseNow() ui/views/widget/widget.cc:705:19  

#2 0x55e4b26d0e62 in exo::ShellSurfaceBase::~ShellSurfaceBase() components/exo/shell\_surface\_base.cc:358:14  

#3 0x55e4b26c8a67 in exo::ShellSurface::~ShellSurface() components/exo/shell\_surface.cc:132:1  

#4 0x55e4b26f65e1 in ~XdgShellSurface components/exo/xdg\_shell\_surface.cc:27:38  

#5 0x55e4b26f65e1 in exo::XdgShellSurface::~XdgShellSurface() components/exo/xdg\_shell\_surface.cc:27:37  

#6 0x55e4acb0f87d in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#7 0x55e4acb0f87d in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#8 0x55e4acb0f87d in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#9 0x55e4acb0f87d in ~WaylandXdgSurface components/exo/wayland/xdg\_shell.cc:783:39  

#10 0x55e4acb0f87d in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:51:5  

#11 0x55e4acb0f87d in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:308:7  

#12 0x55e4acb0f87d in ~unique\_ptr buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:262:19  

#13 0x55e4acb0f87d in void exo::wayland::DestroyUserData[exo::wayland::WaylandXdgSurface](javascript:void(0);)(wl\_resource\*) components/exo/wayland/server\_util.h:40:3  

#14 0x55e4b272ea22 in destroy\_resource third\_party/wayland/src/src/wayland-server.c:724:3  

#15 0x55e4b272e8be in wl\_resource\_destroy third\_party/wayland/src/src/wayland-server.c:741:2  

#16 0x55e4b9d19b24 in ffi\_call\_unix64 crtstuff.c

previously allocated by thread T0 (chrome) here:  

#0 0x55e4acad653d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x7f6a93700217 in views::NativeWidgetAura::NativeWidgetAura(views::internal::NativeWidgetDelegate\*) ui/views/widget/native\_widget\_aura.cc:105:15  

#2 0x7f6a93708feb in views::internal::NativeWidgetPrivate::CreateNativeWidget(views::internal::NativeWidgetDelegate\*) ui/views/widget/native\_widget\_aura.cc:1196:14  

#3 0x7f6a9369b2bb in CreateNativeWidget ui/views/widget/widget.cc:85:10  

#4 0x7f6a9369b2bb in views::Widget::Init(views::Widget::InitParams) ui/views/widget/widget.cc:382:20  

#5 0x55e4b26ddae4 in exo::ShellSurfaceBase::CreateShellSurfaceWidget(ui::WindowShowState) components/exo/shell\_surface\_base.cc:1328:12  

#6 0x55e4b26cdaaf in exo::ShellSurface::OnPreWidgetCommit() components/exo/shell\_surface.cc:526:5  

#7 0x55e4b26d85dd in exo::ShellSurfaceBase::OnSurfaceCommit() components/exo/shell\_surface\_base.cc:854:8  

#8 0x55e4b2681913 in exo::Surface::Commit() components/exo/surface.cc:805:16  

#9 0x55e4b9d19b24 in ffi\_call\_unix64 crtstuff.c

SUMMARY: AddressSanitizer: heap-use-after-free buildtools/third\_party/libc++/trunk/include/\_\_tree:1082:59 in \_\_root  

Shadow bytes around the buggy address:  

0x0c2a800a63f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800a6400: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800a6410: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

0x0c2a800a6420: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a800a6430: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c2a800a6440: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd  

0x0c2a800a6450: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800a6460: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x0c2a800a6470: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2a800a6480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2a800a6490: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==224316==ABORTING

## Attachments

- [1333995_screencast_00003.webm](attachments/1333995_screencast_00003.webm) (video/webm, 3.4 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### rh...@gmail.com (2022-06-07)

uploading screencast

### [Deleted User] (2022-06-07)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-06-07)

I think there's a no checks on function ash/drag_drop/tab_drag_drop_delegate.cc[1], when isLacrosWindow is holding |source_window_| and is getting freed and reuse after, it's could lead to heap UaF.
```
void TabDragDropDelegate::OnNewBrowserWindowCreated(
    const gfx::Point& location_in_screen,
    aura::Window* new_window) {
  auto is_lacros = IsLacrosWindow(source_window_);

  // https://crbug.com/1286203:
  // It's possible new window is created when the dragged WebContents
  // closes itself during the drag session.
  if (!new_window) {
    if (is_lacros && !crosapi::lacros_startup_state::IsLacrosPrimaryEnabled()) {
      LOG(ERROR)
          << "New browser window creation for tab detaching failed.\n"
          << "Check whether about:flags#lacros-primary is enabled or "
          << "--enable-features=LacrosPrimary is passed in when launching Ash";
    }
    return;
  }
```

[1]https://source.chromium.org/chromium/chromium/src/+/main:ash/drag_drop/tab_drag_drop_delegate.cc;l=166-182?q=ash%2Fdrag_drop%2Ftab_drag_drop_delegate.cc&ss=chromium%2Fchromium%2Fsrc

### ye...@google.com (2022-06-07)

Assignign to yuhengh@ since they're working on  https://crbug.com/1286203. I see that the fix for 1286203 is not complete, yuhengh@ would you say this bug is brand new or should it be marked as a dupe?

### [Deleted User] (2022-06-07)

[Empty comment from Monorail migration]

### rh...@gmail.com (2022-06-14)

[Comment Deleted]

### rh...@gmail.com (2022-06-14)

Sorry wrong bug!

### xi...@chromium.org (2022-06-15)

yuhengh@, friendly ping for https://crbug.com/chromium/1333995#c4. Also cc'ed folks who is on https://crrev.com/c/3368343.

[Monorail components: OS>LaCrOS>Tablet]

### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-06-15)

I think https://crbug.com/1286203 fixed part of the issue. I will revisit this and 1286203 later this week.

### to...@igalia.com (2022-06-15)

May I get cc'ed to https://crbug.com/chromium/1286203?

### [Deleted User] (2022-06-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-16)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-23)

[Empty comment from Monorail migration]

### to...@igalia.com (2022-07-07)

+djmm, xdai, erikchen

I believe the source of the problem here is a UX issue:

Scenario 1:
When there is only ONE TAB in the tabstrip, it is not possible to drag this one tab out.

Scenario 2:
- In this case, there is one GROUP OF TABS - that is dragged similarly as if it was the scenario above (one tab) - the dragging seems allowed.

Question: from a UX perspective, should an user be able to drag a group of tabs out of a Chrome window, if there is not further tabs?

Basically, we could fix the bug by not allowing the dragging in scenario_2 to take place, similarly to what happens in scenario_1...



### er...@chromium.org (2022-07-07)

Not sure who's in charge of tab groups. I suspect not allowing tab dragging is the right approach. +robliao

### rh...@gmail.com (2022-07-07)

Sorry adding comment. I don't know if chromeOS dev are different with Chrome on other platforms (Win,Mac,Linux) but for tab groups maybe we can cc tbergquist@chromium.org. I had several bugs from tab groups on Windows.

### ro...@chromium.org (2022-07-07)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>TopChrome>TabStrip>ThumbnailTabStrip]

### yu...@chromium.org (2022-07-11)

@tonikitoo I think we can disallow dragging a single tab group with no other tabs outside similar to the single tab case. I'm assuming your CL https://chromium-review.googlesource.com/c/chromium/src/+/3747280 does not fix this issue. Is it correct?

### to...@igalia.com (2022-07-19)

(sorry about the delay, I was OOO last week)

re https://crbug.com/chromium/1333995#c19: this is correct, yuhengh@... my CL does not relate to the fix proposed here in https://crbug.com/chromium/1333995#c15

Please let me know if I can be of help fixing this issue.

### rh...@gmail.com (2022-07-20)

tonik@ yuhengh@,

I think this issue was not related to the UX issue. If we look into the chrome browser(ash) on chromeOS, dragging a single tab group is allowed and does not crash. 
I have no idea if the behavior could differ between ash and lacros.

Please refer to the screencast. I think there is a missing condition where the lacros tab group is dragging and entering splitview or snapping?

### [Deleted User] (2022-07-25)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-25)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-25)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2022-07-25)

This is RBS blocking M104 promotion. Is it going to be fixed this week?

### yu...@chromium.org (2022-07-25)

This is a Lacros issue. Is M104  promotion for Lacros also? Yes, I'm going work on it this week.

### yu...@chromium.org (2022-07-26)

Bump down to 1 since it's a Lacros issue.

### dj...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### sr...@google.com (2022-07-27)

M104 promotion to lacros wlll be next week. 

### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cd107be3ebbdc44b666330a67ba9dde1b9647a6d

commit cd107be3ebbdc44b666330a67ba9dde1b9647a6d
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Thu Jul 28 23:00:18 2022

WebUI tab strip: do not allow dragging a single tab group

Dragging a single tab group with no other tab or tab group outside
itself to split screen is problematic because the current browser will not have any tabs and will be closed.

Previously the code do not allow dragging a single tab. In this CL
the logic is revised to do not allow dragging a single tab or a single tab group with no other tab or tab group outside itself.

Bug: 1333995
Change-Id: Ie590817852ded8ec465470bb7e5cf852a868eabe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3789615
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1029506}

[modify] https://crrev.com/cd107be3ebbdc44b666330a67ba9dde1b9647a6d/chrome/test/data/webui/tab_strip/tab_list_test.ts
[modify] https://crrev.com/cd107be3ebbdc44b666330a67ba9dde1b9647a6d/chrome/browser/resources/tab_strip/tab_list.ts


### yu...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

Merge approved: your change passed merge requirements and is auto-approved for M105. Please go ahead and merge the CL to branch 5195 (refs/branch-heads/5195) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-29)

Merge review required: M104 has already been cut for stable release.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-08-01)

[Bulk Edit] Your change has been approved for M105 branch(go/chrome-branches),please go ahead and merge the CL to M105 branch manually by 2PM PST today so that they would be part of tomorrow's(Aug-01st-2022) Dev and the same build would be promoted to Beta later this week on Thursday which is our first M105 Beta.

### [Deleted User] (2022-08-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/16dc12f9381c3d20b8fa2fa8ed171731d72986ee

commit 16dc12f9381c3d20b8fa2fa8ed171731d72986ee
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Wed Aug 03 15:36:30 2022

WebUI tab strip: do not allow dragging a single tab group

Dragging a single tab group with no other tab or tab group outside
itself to split screen is problematic because the current browser will not have any tabs and will be closed.

Previously the code do not allow dragging a single tab. In this CL
the logic is revised to do not allow dragging a single tab or a single tab group with no other tab or tab group outside itself.

(cherry picked from commit cd107be3ebbdc44b666330a67ba9dde1b9647a6d)

Bug: 1333995
Change-Id: Ie590817852ded8ec465470bb7e5cf852a868eabe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3789615
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1029506}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3805543
Cr-Commit-Position: refs/branch-heads/5195@{#185}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/16dc12f9381c3d20b8fa2fa8ed171731d72986ee/chrome/test/data/webui/tab_strip/tab_list_test.ts
[modify] https://crrev.com/16dc12f9381c3d20b8fa2fa8ed171731d72986ee/chrome/browser/resources/tab_strip/tab_list.ts


### am...@chromium.org (2022-08-04)

m104 merge approved, please merge this fix to branch 5112 at your earliest convenience 

### am...@chromium.org (2022-08-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-04)

Congratulations, Rheza! The VRP Panel has decided to award you $3000 for this report. The reward amount was decided upon based on this issue being significantly mitigated by not being remote exploitable and the user interaction required. Thank you for your efforts and reporting this issue to us. 

### gi...@appspot.gserviceaccount.com (2022-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5de320cba424da3bb0515d699ff506b879bf789b

commit 5de320cba424da3bb0515d699ff506b879bf789b
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Fri Aug 05 20:48:24 2022

[M104 merge] WebUI tab strip: do not allow dragging a single tab group

Dragging a single tab group with no other tab or tab group outside
itself to split screen is problematic because the current browser will not have any tabs and will be closed.

Previously the code do not allow dragging a single tab. In this CL
the logic is revised to do not allow dragging a single tab or a single tab group with no other tab or tab group outside itself.

(cherry picked from commit cd107be3ebbdc44b666330a67ba9dde1b9647a6d)

Bug: 1333995
Change-Id: Ie590817852ded8ec465470bb7e5cf852a868eabe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3789615
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1029506}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3811235
Cr-Commit-Position: refs/branch-heads/5112@{#1402}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/5de320cba424da3bb0515d699ff506b879bf789b/chrome/test/data/webui/tab_strip/tab_list_test.ts
[modify] https://crrev.com/5de320cba424da3bb0515d699ff506b879bf789b/chrome/browser/resources/tab_strip/tab_list.ts


### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-08-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-25)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-08-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1333995?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: OS>LaCrOS>Tablet, UI>Browser>TopChrome>TabStrip>ThumbnailTabStrip]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059882)*
