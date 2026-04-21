# Security: heap-use-after-free in WebsiteSettingsInfoBarDelegate::Create

| Field | Value |
|-------|-------|
| **Issue ID** | [40082112](https://issues.chromium.org/issues/40082112) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Infobars |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2015-05-21 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 45.0.2407.0 canary (32 bits)  

Operating System: Windows 7

**REPRODUCTION CASE**  

(Watch the video)

============================================================================================================  

==6472==ERROR: AddressSanitizer: heap-use-after-free on address 0x278d4540 at pc 0x11d08164 bp 0xdeadbeef sp 0x00aecc08  

READ of size 4 at 0x278d4540 thread T0  

#0 0x11d08163 in WebsiteSettingsInfoBarDelegate::Create C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\ui\website\_settings\website\_settings\_infobar\_delegate.cc:20  

#1 0x11b6dc60 in WebsiteSettings::OnUIClosing C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\ui\website\_settings\website\_settings.cc:372  

#2 0x11751473 in WebsiteSettingsPopupView::OnWidgetDestroying C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\ui\views\website\_settings\website\_settings\_popup\_view.  

cc:383  

#3 0xf6d67c2 in views::Widget::OnNativeWidgetDestroying C:\b\build\slave\Win\_ASan\_Release\build\src\ui\views\widget\widget.cc:1108  

#4 0xf86f510 in views::DesktopWindowTreeHostWin::HandleDestroying C:\b\build\slave\Win\_ASan\_Release\build\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:758  

#5 0xf8cfb81 in views::HWNDMessageHandler::OnDestroy C:\b\build\slave\Win\_ASan\_Release\build\src\ui\views\win\hwnd\_message\_handler.cc:1389  

#6 0xf8c4c47 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\build\slave\Win\_ASan\_Release\build\src\ui\views\win\hwnd\_message\_handler.h:390  

#7 0xf8c0f7a in views::HWNDMessageHandler::OnWndProc C:\b\build\slave\Win\_ASan\_Release\build\src\ui\views\win\hwnd\_message\_handler.cc:896  

#8 0x137d36af in gfx::WindowImpl::WndProc c:\b\build\slave\win\_asan\_release\build\src\ui\gfx\win\window\_impl.cc:315  

#9 0x75f586ee in IsThreadDesktopComposited+0x11e (C:\Windows\system32\USER32.dll+0x186ee)  

#10 0x75f58875 in IsThreadDesktopComposited+0x2a5 (C:\Windows\system32\USER32.dll+0x18875)  

#11 0x75f570f3 in InflateRect+0x73 (C:\Windows\system32\USER32.dll+0x170f3)  

#12 0x75f5738e in DefWindowProcW+0x143 (C:\Windows\system32\USER32.dll+0x1738e)  

#13 0x7748642d in KiUserCallbackDispatcher+0x2d (C:\Windows\SYSTEM32\ntdll.dll+0x4642d)  

#14 0xc3760de in base::internal::Invoker<IndexSequence<0>,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall WrenchToolbarButton::\*)(void)>,void \_\_cdec  

l(WrenchToolbarButton \*),base::internal::TypeList<base::WeakPtr<WrenchToolbarButton> > >,base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr<WrenchToolbarButton> >

> ,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (\_\_thiscall WrenchToolbarButton::\*)(void)>,base::internal::TypeList<base::WeakPtr<WrenchToolbarButton>  
> 
> const &> >,void \_\_cdecl(void)>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:176  
> 
> #15 0x7673cd0 in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\callback.h:396  
> 
> #16 0x750f4cb in base::MessageLoop::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:444  
> 
> #17 0x7510a60 in base::MessageLoop::DoWork C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:454

AddressSanitizer can not describe address in more detail (wild memory access suspected).  

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\browser\ui\website\_settings\website\_settings\_infobar\_delegate.cc:20 in WebsiteSet  

tingsInfoBarDelegate::Create  

Shadow bytes around the buggy address:  

0x34f1a850: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x34f1a860: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x34f1a870: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x34f1a880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x34f1a890: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x34f1a8a0: fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa  

0x34f1a8b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x34f1a8c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x34f1a8d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x34f1a8e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x34f1a8f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

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

==6472==ABORTING  

==6472==AddressSanitizer: while reporting a bug found another one. Ignoring.

## Attachments

- [PoC.html](attachments/PoC.html) (text/html, 234 B)
- [872131.mp4](attachments/872131.mp4) (application/octet-stream, 603.0 KB)

## Timeline

### in...@chromium.org (2015-05-21)

Peter, can you please take a look or suggest an owner. We are in a security fixit this week, so any help is highly appreciated. The repro looks pretty simple and minimized. 

### pk...@chromium.org (2015-05-21)

Looks like Markus owns this UI?

It seems like the general problem here is that the website settings code shows an infobar when the popup closes if some of the permissions changed, but in this case the popup is closing because the whole browser is being torn down, and the infobar service no longer exists.

In turn this makes me wonder why the WebsiteSettings object is keeping an InfoBarService* to begin with, instead of simply looking up the appropriate WebContents and its appropriate InfoBarService when it needs to.  Presumably in the course of these lookups it would notice that one of both of these objects no longer exist.

### cl...@chromium.org (2015-05-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### oc...@chromium.org (2015-06-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-06-03)

Reproduced in r323865

### cl...@chromium.org (2015-06-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-05)

markusheintz@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@google.com (2015-06-15)

Markus - can you please provide an update? (even if that update is no progress). I'd like to get a fix into M44 beta well before it gets close to stable promotion.

### ch...@gmail.com (2015-06-18)

Markus, Could you please take a look at this issue. Please note that this is high severity security bug that needs to be fixed.


### cl...@chromium.org (2015-06-19)

markusheintz@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-07-03)

markusheintz@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-07-18)

markusheintz@: Uh oh! This issue is still open and hasn't been updated in the last 57 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-07-21)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### ch...@gmail.com (2015-08-21)

Any updates on this bug?

### cl...@chromium.org (2015-08-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5314858512285696

Uploader: palmer@chromium.org
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: 
Crash Address: 
Crash State:
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv954pHAW9BehAHuvMC4LqQpDv_rC0ltSZQU-rCyR_A-qpf1zOZA7y5ZTVSRODC86OFX-2ALK3rjehidigTJcrR8QEPNiZivuomrAYihCfrAoASEQY1_Y4oQEKRBS2gedM7yX7VQ-brK57kfwWuyOjte34vv4iQ


Additional requirements: Requires HTTP

Filer: palmer

### pa...@chromium.org (2015-08-24)

Disturbingly, I reproduced this on (non-ASAN) Mac OS X as well. Crash ID bafe090015365ce6 (97850ae0-1203-480a-8dfd-25d6b1798f2f)

The need for the user to allow pop-ups somewhat mitigates the severity of this, though, right?

### pa...@chromium.org (2015-08-24)

Linux (ASAN), too. And non-ASAN Windows.

Also, there is a weird behavior in a non-crashing case: If you don't interact with a permission setting, but just leave the Origin Info Bubble up, when the google.com tab closes, the bubble stays up and shows over the previous tab (e.g. file:///.../poc.html). But it's still the OIB for google.com, and says so.

So, an OIB should be attached to its tab, or to its WebContents, and should be properly closed with the tab or WebContents goes away. But that doesn't seem to be happening. Investigating...

### pa...@chromium.org (2015-08-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f2cba0d13b3a6d76dedede66731e5ca253d3b2af

commit f2cba0d13b3a6d76dedede66731e5ca253d3b2af
Author: palmer <palmer@chromium.org>
Date: Thu Aug 27 23:15:06 2015

Fix UAF in Origin Info Bubble and permission settings UI.

In addition to fixing the UAF, will this also fix the problem of the bubble
showing over the previous tab (if the bubble is open when the tab it was opened
for closes).

BUG=490492
TBR=tedchoc

Review URL: https://codereview.chromium.org/1317443002

Cr-Commit-Position: refs/heads/master@{#346023}

[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/android/connection_info_popup_android.cc
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/android/website_settings_popup_android.cc
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/cocoa/website_settings/website_settings_bubble_controller.h
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/cocoa/website_settings/website_settings_bubble_controller.mm
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/cocoa/website_settings/website_settings_bubble_controller_unittest.mm
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/views/website_settings/website_settings_popup_view.cc
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/views/website_settings/website_settings_popup_view.h
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/website_settings/website_settings.cc
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/website_settings/website_settings.h
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/website_settings/website_settings_ui.h
[modify] http://crrev.com/f2cba0d13b3a6d76dedede66731e5ca253d3b2af/chrome/browser/ui/website_settings/website_settings_unittest.cc


### pa...@chromium.org (2015-08-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-28)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-12)

FYI I'm working on the assumption that this will roll in off trunk due to it being a non-trivial UI change. If you want this in an M-46 patch and can vouch for it playing nicely with M46, please let me know so we can ship this to users more quickly (and remove Merge-NA and replace with Merge-Triage).

Marking as shipping with M-47.

### ti...@google.com (2015-12-01)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Our reward panel awarded you $1000 for this report - congratulations!

Reward panel notes: Too much user interaction needed for a higher reward, although nice use after free in browser process. 

Thanks again for the report!

### cl...@chromium.org (2015-12-04)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/490492?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082112)*
