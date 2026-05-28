# Chrome bookmarks menu crash due to assertion failure in BookmarkMenuDelegate

| Field | Value |
|-------|-------|
| **Issue ID** | [434499328](https://issues.chromium.org/issues/434499328) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>Bookmarks |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ta...@gmail.com |
| **Assignee** | dl...@chromium.org |
| **Created** | 2025-07-27 |
| **Bounty** | Confirmed (amount unknown) |

## Description

---

### Report description

Chrome bookmarks menu crash due to assertion failure in BookmarkMenuDelegate

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

The Chrome browser's bookmark menu contains an assertion failure related to submenu handling, which causes the browser to crash. Specifically, when BookmarkMenuDelegate::BuildOtherNodeMenuHeader() is called, the assertion !menu->HasSubmenu() || menu->GetSubmenu()->children().empty() fails, leading to a fatal crash.

Please describe the technical details of the vulnerability
During drag-and-drop or reordering operations on bookmark menu nodes, the internal menu object's submenu state can become inconsistent. The menu may report having a submenu while its child nodes are not properly cleared, triggering an assertion failure. An attacker can craft a specific bookmark tree structure or manipulate bookmark drag actions to trigger this assertion, causing the browser process to crash (denial of service). This issue arises from insufficient consistency checks between submenu existence and its child nodes.

To reproduce the vulnerability:

1. Create a new bookmark with the title test and the URL: <https://nb.fidelity.com/static/mybenefits/netbenefitslogin/#/login>.
2. Create a new folder under the "Other bookmarks" section.
3. Click the three-dot menu in the upper-right corner of Chrome, and select "Show Bookmarks Bar".
4. Drag the newly created bookmark into the newly created folder.
5. Repeat the drag-and-drop operation multiple times — sometimes dragging the bookmark out of the folder and back in again.
6. In some cases, the browser crashes immediately. In other cases, it takes several repetitions before a crash occurs.
7. The crash is caused by an assertion failure, as shown in the attached logs.

> Log file is included as an attachment.

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

An attacker with local or remote access could exploit this vulnerability by inducing the user to perform specific bookmark menu interactions, leading to a browser crash. This could result in denial of service and impact browser stability. Moreover, this flaw may be a sign of deeper memory or state management issues that could potentially be leveraged for more severe attacks.

---

### The cause

#### What version of Chrome have you found the security issue in?

140.0.7282.0 (开发者内部版本) /138.0.7204.168 (正式版本) （64 位）

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Tan Jiashuo

## Attachments

- [chrome.log](attachments/chrome.log) (text/x-log, 19.1 KB)
- [chrome.log](attachments/chrome.log) (text/x-log, 19.1 KB)
- [1.txt](attachments/1.txt) (text/plain, 720 B)
- [2025-07-29 10-10-20.mkv](attachments/2025-07-29 10-10-20.mkv) (video/x-matroska, 20.0 MB)
- [asan](attachments/asan) (application/octet-stream, 8.4 KB)

## Timeline

### me...@google.com (2025-07-28)

Thanks for the report. I've been unable to repro, but it's possible that I'm not interacting with the UI in the right way. Could you please attach a screen capture as well?

Given that this is a CHECK failure, it sounds like a stability issue rather than security.

dljames: Could you please take a look as the owner of bookmarks? Thanks.

### me...@google.com (2025-07-28)

Tentatively assigning low severity assuming this has security implications. This requires a lot of user gestures and is unlikely to be used to mount an attack.

### ch...@google.com (2025-07-29)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ta...@gmail.com (2025-07-31)

This crash is caused by a memory safety issue due to a buffer over-read, which occurs when Chrome handles X11 drag-and-drop of bookmarks. The stack trace suggests that a raw_ptr<T> may have become invalid at the time of use—either due to being freed or null—leading to a null pointer dereference or use-after-free (UAF). This vulnerability could result in a crash, information disclosure, and, in severe cases, remote code execution.





### ta...@gmail.com (2025-07-31)

the presence of raw_ptr.h in the stack trace suggests that the raw_ptr<t> mechanism detected an attempt to access freed memory.

### dl...@chromium.org (2025-07-31)

Hi! I was able to reproduce this on my end following the screencast Tan submitted using linux chrome version 140.0.7327.0 (Developer Build) unknown (64-bit) .

Here is a partial stack trace that I encountered which matches the logs provided in [comment#1](https://issues.chromium.org/issues/434499328#comment1)

```
[1729426:1729426:0731/172002.815968:FATAL:chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.cc:1232] Check failed: !menu->HasSubmenu() || menu->GetSubmenu()->children().empty(). 
#0 0x7f261152b8d2 base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1052:7]
#1 0x7f2611507b81 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:255:20]
#2 0x7f26113c576a logging::LogMessage::Flush() [../../base/logging.cc:705:29]
#3 0x7f26113c5640 logging::LogMessage::~LogMessage() [../../base/logging.cc:694:3]
#4 0x7f26113a3362 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() [../../base/check.cc:164:3]
#5 0x7f26113a2f0b logging::CheckNoreturnError::~CheckNoreturnError() [../../base/check.cc:321:16]
#6 0x557a62397370 BookmarkMenuDelegate::BuildOtherNodeMenuHeader() [../../chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.cc:1232:3]
#7 0x557a623924c8 BookmarkMenuDelegate::BuildMenu() [../../chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.cc:1094:5]
#8 0x557a6239535d BookmarkMenuDelegate::WillShowMenu() [../../chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.cc:616:7]
#9 0x7f2606cfd538 views::MenuController::OpenMenuImpl() [../../ui/views/controls/menu/menu_controller.cc:2388:26]
#10 0x7f2606cfb58f views::MenuController::CommitPendingSelection() [../../ui/views/controls/menu/menu_controller.cc:2380:3]
#11 0x7f2606cf3cbb views::MenuController::SetSelection() [../../ui/views/controls/menu/menu_controller.cc:1694:5]
#12 0x7f2606cf4310 views::MenuController::SelectItemAndOpenSubmenu() [../../ui/views/controls/menu/menu_controller.cc:816:3]
#13 0x557a6239571c BookmarkMenuDelegate::BookmarkNodeMoved() [../../chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.cc:676:28]
#14 0x557a6089445a BookmarkMergedSurfaceService::Move() [../../chrome/browser/bookmarks/bookmark_merged_surface_service.cc:294:16]
#15 0x557a5feb6cc7 BookmarkUIOperationsHelperMergedSurfaces::MoveBookmarkNodeData() [../../chrome/browser/ui/bookmarks/bookmark_ui_operations_helper.cc:506:30]
#16 0x557a5feb3b75 internal::BookmarkUIOperationsHelper::DropBookmarks() [../../chrome/browser/ui/bookmarks/bookmark_ui_operations_helper.cc:133:3]

```

I'll report back with any additional findings today, thanks!

### dl...@chromium.org (2025-07-31)

The fix for this can be found here: <https://chromium-review.googlesource.com/c/chromium/src/+/6806896>

Should be landing shortly. I don't have a consistent reproduction step - I was able to reproduce this on only one of the devices I was testing with. This means we won't have a regression test for this scenario but I figured it is better to mitigate the crash first.

### dx...@google.com (2025-07-31)

Project: chromium/src  

Branch:  main  

Author:  dljames [dljames@chromium.org](mailto:dljames@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6806896>

[Bookmarks] Ensure the Other folder is empty before rebuilding it

---


Expand for full commit details
```
     
    A CHECK could fail in BookmarkMenuDelegate::BuildOtherNodeMenuHeader 
    during certain drag-and-drop scenarios leaving the menu in an 
    inconsistent state. 
     
    This resulted in the "Other bookmarks" submenu consisting of the 
    separator. The WillShowMenu logic would then attempt to rebuild the menu 
    but the CHECK condition would fail because the menu is not empty due to 
    the separator. 
     
    This change enforces that the "Other bookmarks" menu should be empty 
    before adding new items. 
     
    #top-chrome-bug-fixit 
     
    Change-Id: I75ca25f935ed4b308a7e12dd18ff47b9b0c71b4b 
    Bug: 434499328 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6806896 
    Reviewed-by: Kaan Alsan <alsan@chromium.org> 
    Commit-Queue: Darryl James <dljames@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1495015}

```

---

Files:

- M `chrome/browser/ui/views/bookmarks/bookmark_menu_delegate.cc`

---

Hash: [f91452d872eba7630e07b1e76a8e817909220662](http://crrev.com/f91452d872eba7630e07b1e76a8e817909220662)  

Date: Thu Jul 31 19:22:04 2025


---

### sp...@google.com (2025-09-04)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. This appears to be a CHECK failure and also is in code that appears to be in code that would be BRP protected and not result in an exploitable security issue. Furthermore, this issue is not remote exploitable and involves significant direct user interactions preconditions to the extent, even if potentially exploitable, we would consider this significantly mitigated. As such, we are unfortunately unable to extend a Chrome VRP reward for this report.  

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-11-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. This appears to be a CHECK failure and also is in code that appears to be in code that would be BRP protected and not result in an exploitable security issue. Furthermore, this issue is not remote exploitable and involves significant direct user interactions preconditions to the extent, even if potentially exploitable, we would consider this significantly mitigated. As such, we are unfortunately unable to extend a Chrome VRP reward for this report.  
> 
> Please note that t

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/434499328)*
