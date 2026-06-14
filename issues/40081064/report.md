# Heap-use-after-free in OpenPDFInReaderBubbleView::ButtonPressed

| Field | Value |
|-------|-------|
| **Issue ID** | [40081064](https://issues.chromium.org/issues/40081064) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF, UI |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2014-12-24 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 41.0.2257.0 canary / 39.0.2171.95 dev-m  

Operating System: Win7  

Crash ID: 5dc199ce255e6925

STEPS

1. Open repro-pdf.html
2. Click on the button to open test.pdf link in new tab and click on pdf bubble as in "1.png" then after 5s the page will be changed as in 2.png
3. click on "DONE" button or Open in Adobe Reader link.

The problem is that if a tab is changed location or closed via JavaScript, bubble isn't closing and is stays open.

eax=f8242b1e ebx=0c711718 ecx=09bcfb80 edx=0c711700 esi=0b95ac3c edi=0017eb60  

eip=60fbed1b esp=0017ea24 ebp=0017ea34 iopl=0 nv up ei pl nz na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010206  

chrome\_602c0000!OpenPDFInReaderBubbleView::ButtonPressed+0x8:  

60fbed1b ff5018 call dword ptr [eax+18h] ds:0023:f8242b36=????????  

0:000> k  

ChildEBP RetAddr  

0017ea24 6144cc46 chrome\_602c0000!OpenPDFInReaderBubbleView::ButtonPressed+0x8 [c:\b\build\slave\win\build\src\chrome\browser\ui\views\open\_pdf\_in\_reader\_bubble\_view.cc @ 68]  

0017ea34 61458256 chrome\_602c0000!views::Button::NotifyClick+0x17 [c:\b\build\slave\win\build\src\ui\views\controls\button\button.cc @ 75]  

0017ea50 614433d1 chrome\_602c0000!views::CustomButton::OnMouseReleased+0x62 [c:\b\build\slave\win\build\src\ui\views\controls\button\custom\_button.cc @ 157]  

0017ea6c 61443117 chrome\_602c0000!views::View::ProcessMouseReleased+0x6f [c:\b\build\slave\win\build\src\ui\views\view.cc @ 2299]  

0017ea80 605aae89 chrome\_602c0000!views::View::OnMouseEvent+0x8e [c:\b\build\slave\win\build\src\ui\views\view.cc @ 988]  

0017ea94 605abc75 chrome\_602c0000!ui::EventHandler::OnEvent+0x32 [c:\b\build\slave\win\build\src\ui\events\event\_handler.cc @ 29]  

0017eaac 605aae1a chrome\_602c0000!ui::EventTarget::OnEvent+0x32 [c:\b\build\slave\win\build\src\ui\events\event\_target.cc @ 64]  

0017eac4 605aac26 chrome\_602c0000!ui::EventDispatcher::DispatchEvent+0x3d [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 190]  

0017eae0 605aab26 chrome\_602c0000!ui::EventDispatcher::ProcessEvent+0x86 [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 138]  

0017eb14 605aa16c chrome\_602c0000!ui::EventDispatcherDelegate::DispatchEventToTarget+0x2a [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 86]  

0017eb3c 61461863 chrome\_602c0000!ui::EventDispatcherDelegate::DispatchEvent+0x5b [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 57]  

0017ed14 6144969f chrome\_602c0000!views::internal::RootView::OnMouseReleased+0x8a [c:\b\build\slave\win\build\src\ui\views\widget\root\_view.cc @ 456]  

0017ed44 6144ac6b chrome\_602c0000!views::Widget::OnMouseEvent+0xc3 [c:\b\build\slave\win\build\src\ui\views\widget\widget.cc @ 1233]  

0017ed58 605aae89 chrome\_602c0000!views::DesktopNativeWidgetAura::OnMouseEvent+0x31 [c:\b\build\slave\win\build\src\ui\views\widget\desktop\_aura\desktop\_native\_widget\_aura.cc @ 1043]  

0017ed6c 605abc6c chrome\_602c0000!ui::EventHandler::OnEvent+0x32 [c:\b\build\slave\win\build\src\ui\events\event\_handler.cc @ 29]  

0017ed84 605aae1a chrome\_602c0000!ui::EventTarget::OnEvent+0x29 [c:\b\build\slave\win\build\src\ui\events\event\_target.cc @ 63]  

0017ed9c 605aac26 chrome\_602c0000!ui::EventDispatcher::DispatchEvent+0x3d [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 190]  

0017edb8 605aab26 chrome\_602c0000!ui::EventDispatcher::ProcessEvent+0x86 [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 138]  

0017edec 605aa16c chrome\_602c0000!ui::EventDispatcherDelegate::DispatchEventToTarget+0x2a [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 86]  

0017ee14 605a971d chrome\_602c0000!ui::EventDispatcherDelegate::DispatchEvent+0x5b [c:\b\build\slave\win\build\src\ui\events\event\_dispatcher.cc @ 57]

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 3.5 MB)
- [1.png](attachments/1.png) (image/png, 125.0 KB)
- [2.png](attachments/2.png) (image/png, 88.1 KB)
- [repro-pdf.html](attachments/repro-pdf.html) (text/html, 185 B)

## Timeline

### rs...@chromium.org (2014-12-24)

bauerb: According to the history, you added this code a long time ago.

### cl...@chromium.org (2014-12-24)

[Empty comment from Monorail migration]

### ba...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### rs...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### ba...@chromium.org (2015-01-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/432eb007ad1d67d12d2a9d69a0f6e78b9efee9b1

commit 432eb007ad1d67d12d2a9d69a0f6e78b9efee9b1
Author: bauerb <bauerb@chromium.org>
Date: Tue Jan 06 23:17:45 2015

Hide the "Open PDF in Reader" bubble on navigations.

BUG=444957

Review URL: https://codereview.chromium.org/831283002

Cr-Commit-Position: refs/heads/master@{#310167}

[modify] http://crrev.com/432eb007ad1d67d12d2a9d69a0f6e78b9efee9b1/chrome/browser/ui/views/location_bar/open_pdf_in_reader_view.cc


### ba...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### ba...@chromium.org (2015-01-07)

Robert, do you want me to merge this to M40?

### cl...@chromium.org (2015-01-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-07)

This can just roll in M41, no need to merge this medium severity bug.

### ti...@google.com (2015-04-14)

Congratulations - $500 for this report.

Notes from panel: Use-after-free though required a very unique set of interactions that seems unlikely, which is why the reward amount is lower than usual.

Even though this fix rolled out with a patch to M41, we'll mention it in our release notes for M42.

### cl...@chromium.org (2015-04-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/444957?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, UI]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081064)*
