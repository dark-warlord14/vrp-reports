# Security: Heap-use-after-free in payments::`anonymous namespace'::SheetView::RequestFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40087627](https://issues.chromium.org/issues/40087627) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Payments |
| **Reporter** | ch...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2017-05-13 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 60.0.3097 canary
Operating System: windows 7

Desktop web payments crash when selecting an input field (add an address).

https://emerald-eon.appspot.com

rax=00000000217b8a00 rbx=00000000239a0ec8 rcx=00000000217b8a00
rdx=6573776f7262ffff rsi=00000000215993d0 rdi=000000000f8ab320
rip=000007fef05d7bcf rsp=00000000003dd660 rbp=00000000003dd7e0
 r8=0000000000000000  r9=000000001bfd99d0 r10=000000001bfd99d0
r11=00000000003dd6a8 r12=000000000df71840 r13=00000000000002bc
r14=0000000000000000 r15=0000000000000556
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=0000  ds=0000  es=0000  fs=0053  gs=002b             efl=00010206
*** WARNING: Unable to verify checksum for chrome.dll
chrome_7feee290000!payments::`anonymous namespace'::SheetView::RequestFocus+0x4b:
000007fe`f05d7bcf ff9270010000    call    qword ptr [rdx+170h] ds:6573776f`7263016f=????????????????
0:000> k
  *** Stack trace for last set context - .thread/.cxr resets it
Child-SP          RetAddr           Call Site
00000000`003dd660 000007fe`f05d1337 chrome_7feee290000!payments::`anonymous namespace'::SheetView::RequestFocus+0x4b [c:\b\c\b\win64_pgo\src\chrome\browser\ui\views\payments\payment_request_sheet_controller.cc @ 81]
00000000`003dd6b0 000007fe`f0426aef chrome_7feee290000!ViewStack::RequestFocus+0x33 [c:\b\c\b\win64_pgo\src\chrome\browser\ui\views\payments\view_stack.cc @ 105]
00000000`003dd6e0 000007fe`f042697b chrome_7feee290000!constrained_window::NativeWebContentsModalDialogManagerViews::Focus+0x47 [c:\b\c\b\win64_pgo\src\components\constrained_window\native_web_contents_modal_dialog_manager_views.cc @ 133]
00000000`003dd710 000007fe`efac8ade chrome_7feee290000!constrained_window::NativeWebContentsModalDialogManagerViews::Show+0xcf [c:\b\c\b\win64_pgo\src\components\constrained_window\native_web_contents_modal_dialog_manager_views.cc @ 108]
00000000`003dd750 000007fe`ee99c642 chrome_7feee290000!web_modal::WebContentsModalDialogManager::WasShown+0x46 [c:\b\c\b\win64_pgo\src\components\web_modal\web_contents_modal_dialog_manager.cc @ 160]
00000000`003dd780 000007fe`ee9af39e chrome_7feee290000!content::WebContentsImpl::WasShown+0x12a [c:\b\c\b\win64_pgo\src\content\browser\web_contents\web_contents_impl.cc @ 1470]
00000000`003dd7f0 000007fe`ef6c022d chrome_7feee290000!content::WebContentsViewAura::OnWindowVisibilityChanged+0x2a [c:\b\c\b\win64_pgo\src\content\browser\web_contents\web_contents_view_aura.cc @ 1330]
00000000`003dd820 000007fe`ef6c02bd chrome_7feee290000!aura::Window::NotifyWindowVisibilityChangedAtReceiver+0x89 [c:\b\c\b\win64_pgo\src\ui\aura\window.cc @ 935]
00000000`003dd8c0 000007fe`ef6bf8d0 chrome_7feee290000!aura::Window::NotifyWindowVisibilityChangedDown+0x21 [c:\b\c\b\win64_pgo\src\ui\aura\window.cc @ 941]
00000000`003dd930 000007fe`eec5053b chrome_7feee290000!aura::Window::SetVisible+0x180 [c:\b\c\b\win64_pgo\src\ui\aura\window.cc @ 716]
00000000`003dd9a0 000007fe`eec3e792 chrome_7feee290000!views::NativeViewHostAura::ShowWidget+0x16b [c:\b\c\b\win64_pgo\src\ui\views\controls\native\native_view_host_aura.cc @ 165]
00000000`003dda40 000007fe`f05424a2 chrome_7feee290000!views::NativeViewHost::Layout+0xfa [c:\b\c\b\win64_pgo\src\ui\views\controls\native\native_view_host.cc @ 98]
00000000`003ddab0 000007fe`f0541e9f chrome_7feee290000!views::WebView::AttachWebContents+0x9a [c:\b\c\b\win64_pgo\src\ui\views\controls\webview\webview.cc @ 331]
00000000`003ddae0 000007fe`efdbc1c0 chrome_7feee290000!views::WebView::SetWebContents+0x123 [c:\b\c\b\win64_pgo\src\ui\views\controls\webview\webview.cc @ 81]
00000000`003ddb10 000007fe`efd0f439 chrome_7feee290000!BrowserView::OnActiveTabChanged+0x184 [c:\b\c\b\win64_pgo\src\chrome\browser\ui\views\frame\browser_view.cc @ 826]
00000000`003ddb50 000007fe`efd0b8c8 chrome_7feee290000!Browser::ActiveTabChanged+0xd5 [c:\b\c\b\win64_pgo\src\chrome\browser\ui\browser.cc @ 1072]
00000000`003ddc60 000007fe`efd0b9a3 chrome_7feee290000!TabStripModel::NotifyIfActiveTabChanged+0xb4 [c:\b\c\b\win64_pgo\src\chrome\browser\ui\tabs\tab_strip_model.cc @ 1261]
00000000`003ddce0 000007fe`efd097ed chrome_7feee290000!TabStripModel::SetSelection+0x8b [c:\b\c\b\win64_pgo\src\chrome\browser\ui\tabs\tab_strip_model.cc @ 1288]
00000000`003ddd80 000007fe`efdca709 chrome_7feee290000!TabStripModel::ActivateTabAt+0x79 [c:\b\c\b\win64_pgo\src\chrome\browser\ui\tabs\tab_strip_model.cc @ 419]
00000000`003ddde0 000007fe`efded939 chrome_7feee290000!TabStrip::SelectTab+0x39 [c:\b\c\b\win64_pgo\src\chrome\browser\ui\views\tabs\tab_strip.cc @ 1080]


## Attachments

- [Recording #16.mp4](attachments/Recording #16.mp4) (video/mp4, 744.5 KB)

## Timeline

### ch...@gmail.com (2017-05-15)

Crash/9c7fa06aa8000000.

### in...@chromium.org (2017-05-15)

Looks like regression from https://chromium.googlesource.com/chromium/src/+/818ada352c5ec2c3b9da4baf2c9da3472f016fcc.

[Monorail components: Blink>Payments]

### sh...@chromium.org (2017-05-15)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2017-05-15)

I think I can repro this (my crash report is being processed).

It looks like we're updating the editor while the dialog is hidden because of a callback being triggered by the provinces/territory data being done loading.

https://codereview.chromium.org/2881643002 should address this specific editor case and I'll make a patch to make sure this isn't possible in the future.

### an...@chromium.org (2017-05-15)

Got an immediate patch for this @ https://chromium-review.googlesource.com/c/506229/

### bu...@chromium.org (2017-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/432f27040519cf196480248215fe77a3aed822a7

commit 432f27040519cf196480248215fe77a3aed822a7
Author: Anthony Vallee-Dubois <anthonyvd@chromium.org>
Date: Mon May 15 14:36:31 2017

[Web Payments] Prevent use-after-free after the content is updated

This CL changes SheetView to set its first_focusable_ member to null when
the view it points to is removed from the hierarchy. Since the focusing code
handles it being null properly, this change prevents a use-after-free that
could occur when the controller subclasses didn't update the first_focusable_
correctly after updating their content.

Bug: 721988
Change-Id: I4d6749f3e6025ce602c56b8231b1079cab57505c
Reviewed-on: https://chromium-review.googlesource.com/506229
Reviewed-by: Mathieu Perreault <mathp@chromium.org>
Commit-Queue: Anthony Vallee-Dubois <anthonyvd@chromium.org>
Cr-Commit-Position: refs/heads/master@{#471752}
[modify] https://crrev.com/432f27040519cf196480248215fe77a3aed822a7/chrome/browser/ui/views/payments/payment_request_sheet_controller.cc


### an...@chromium.org (2017-05-15)

This issue shouldn't reproduce after r471752.

### aw...@chromium.org (2017-05-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-22)

Hi! The panel decided to award $500 for this report, but noted that they would consider a higher amount if it could be shown without so much user interaction.

### aw...@chromium.org (2017-05-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-08-22)

This issue was migrated from crbug.com/chromium/721988?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087627)*
