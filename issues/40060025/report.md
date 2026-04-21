#  heap-use-after-free in RenderViewContextMenu::ExecuteCommand

| Field | Value |
|-------|-------|
| **Issue ID** | [40060025](https://issues.chromium.org/issues/40060025) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Views, UI>Browser>QuickCommands |
| **Platforms** | Windows |
| **Reporter** | xp...@gmail.com |
| **Assignee** | lg...@chromium.org |
| **Created** | 2022-06-21 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. Enable chrome://flags/#quick-commands and restart.
2. Press CTRL + SPACE to open quick commands.
3. Right click quick commands input field and enable enhanced spell check. From context menu: Spell Check > Use Enhanced Spell Check  
   
   uaf ensues!

**Problem Description:**  

UAF in RenderViewContextMenu::ExecuteCommand

**Additional Comments:**

\*\*Chrome version: \*\* 105.0.5132.0 \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [WindowsTerminal_hrvSbnxb1X.mp4](attachments/WindowsTerminal_hrvSbnxb1X.mp4) (video/mp4, 9.1 MB)
- [asan_.txt](attachments/asan_.txt) (text/plain, 15.9 KB)
- [asan.log](attachments/asan.log) (text/plain, 22.3 KB)

## Timeline

### [Deleted User] (2022-06-21)

[Empty comment from Monorail migration]

### xp...@gmail.com (2022-06-21)

attached ASan

### aj...@chromium.org (2022-06-21)

This repros following the steps in the description. Six clicks.

QuickCommands is disabled by default https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/ui_features.cc;drc=169c6cc102b39295a5bfe2f2a176b42b1c2fe2c4;l=76

Severity: Medium - Memory corruption in the browser process, requiring a non-standard flag and user interaction

Setting impact None as I cannot see the trial on the Finch dashboard.

lgrey - is the QuickCommands feature enabled for any users?

[Monorail components: Internals>Views UI>Browser>QuickCommands]

### aj...@chromium.org (2022-06-21)

+ some views owners for visibility

### lg...@chromium.org (2022-06-21)

> lgrey - is the QuickCommands feature enabled for any users?
Not at the moment unless they're opted in via flags

### ad...@google.com (2022-06-21)

(auto-cc on security bug)

### lg...@chromium.org (2022-06-22)

So the deal here is that this menu options pops up a modal(!?). This deactivates QuickCommands, so it hides, but the menu is still trying to execute a command.

I guess the thing to do here is to disable context menus, which is how Tab Search escapes this fate. I waffled on this a bit (some of the stuff in the context menu is appropriate for a UI text field) but overall, I think for an interface that's explicitly all about the keyboard, nobody will die if they can't paste via context menu.

### pb...@chromium.org (2022-06-23)

Can the MenuRunner own the model here, or otherwise be notified of the model's destruction?

Feels like the lifetime of RenderViewContextMenuViews should at least be tied to the lifetime of the menu so the menu shouldn't try to execute anything here imo. Menu should implicitly be closed/destructed or at least not execute any commands here.

Imo views::MenuRunner should be able to accept a unique_ptr<MenuModel> and not just a raw pointer but I haven't thought very hard about it. This setup is just UAFs waiting to happen.

And since we're talking views UAFs, +kylixrd@ wdyt?

### pb...@chromium.org (2022-06-23)

In this case where the menu would retain ownership of its menumodel the menumodel itself would need to make sure it's not doing UAFs by holding on to raw pointers to webcontents or anything that may destruct under its feet.

### lg...@chromium.org (2022-06-23)

Re: lifetime of the menu
    #2 0x7ffdcfb64afb in views::MenuModelAdapter::ExecuteCommand(int, int) D:\chromium\src\ui\views\controls\menu\menu_model_adapter.cc:170:12
    #3 0x7ffdc690b1ac in views::internal::MenuRunnerImpl::OnMenuClosed(enum views::internal::MenuControllerDelegate::NotifyType, class views::MenuItemView *, int) D:\chromium\src\ui\views\controls\menu\menu_runner_impl.cc:233:29
    #4 0x7ffdcb9f8d6c in views::MenuController::ExitMenu(void) D:\chromium\src\ui\views\controls\menu\menu_controller.cc:3179:13

I don't have all this stuff paged in but it seems like it's doing this "by design"

### pb...@chromium.org (2022-06-23)

Yeah I think all the MenuRunner API stuff assumes that the MenuModel will outlive the MenuRunner.

### gi...@appspot.gserviceaccount.com (2022-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e3ccf4d52c31c77c38dc4a62a332bb227ec64c2

commit 4e3ccf4d52c31c77c38dc4a62a332bb227ec64c2
Author: Leonard Grey <lgrey@chromium.org>
Date: Fri Jun 24 22:44:45 2022

QuickCommands: disable context menu

Bug: 1338057
Change-Id: Ia006b2077da14a3ebe5e5d51e8679e691d52916c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3718266
Commit-Queue: Leonard Grey <lgrey@chromium.org>
Reviewed-by: Elly Fong-Jones <ellyjones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1017865}

[modify] https://crrev.com/4e3ccf4d52c31c77c38dc4a62a332bb227ec64c2/chrome/browser/ui/views/commander_frontend_views.cc


### aj...@google.com (2022-06-25)

Can this be marked as Fixed or are more CLs necessary?

### lg...@chromium.org (2022-07-06)

Sorry for the delay was OOO. I think this immediate bug is fixed. pbos@'s ideas about lifetime are probably worth pursuing (AFAICT!) but I think the views team is better suited to doing that than me.

### [Deleted User] (2022-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-06)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-04)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. While this was a high-quality report, this issue is significantly mitigated by heavy/nearly  implausible amount user interaction. Thank you for your efforts and reporting this issue to us! 

### xp...@gmail.com (2022-08-05)

Thank you as always.

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-10-12)

This issue was migrated from crbug.com/chromium/1338057?no_tracker_redirect=1

[Multiple monorail components: Internals>Views, UI>Browser>QuickCommands]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060025)*
