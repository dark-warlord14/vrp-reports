# uaf in ui::PropertyHandler::GetPropertyInternal(with )

| Field | Value |
|-------|-------|
| **Issue ID** | [40061216](https://issues.chromium.org/issues/40061216) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Accessibility, UI>Accessibility |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2022-10-03 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

ubuntu22.04  

chrome version:  

Chromium 108.0.5338.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1054148.zip)  

Chromium 107.0.5304.10

repro steps:

1. install puppeteer  
   
   npm i puppeteer  
   
   2.node launch.js

repro immediately after 10 seconds

**Problem Description:**  

I found this issue as early as June. It can be reproduced directly in the browser(with --enable-features=AccessibilityTreeForViews launch flag).  

However, during the analysis period, it did not reproduce again after updating chrome version.  

recently I found that it has reproduced in the new version,But there is currently no way to reproduce it directly, only through puppeteer.  

More precisely, the uaf will be reproduced when calling "puppeteer's function: browser.close()".

**Additional Comments:**

\*\*Chrome version: \*\* 107.0.5304.10 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [launch.js](attachments/launch.js) (text/plain, 809 B)
- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 26.9 KB)
- [asan2.log](attachments/asan2.log) (text/plain, 28.4 KB)

## Timeline

### [Deleted User] (2022-10-03)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-10-03)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-10-04)

dtseng@ can you PTAL as OWNER of ax_aura_obj_cache.cc? My shot in the dark is that https://chromium-review.googlesource.com/c/chromium/src/+/2801464 has something to do with this.

It looks like this bug triggers because the puppeteer browser.close() action will reach ExitIgnoreUnloadHandlers() (see https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/devtools/protocol/browser_handler.cc;drc=74e6b58d295dae0f6445e29f8ef0f1cb1d841684;l=115).

This code path can be triggered when Chrome is forced closed for a pending update, and looks to trigger by default on ChromeOS: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_browser_main_posix.cc;drc=74e6b58d295dae0f6445e29f8ef0f1cb1d841684;l=129.

So I'm treating this as a normal security bug as it's reachable outside of puppeteer testing conditions.

The free and use stack traces overlap quite a bit. They start differing after BrowserCloseManager::CloseBrowser() in chrome/browser/lifetime/browser_close_manager.cc:

void BrowserCloseManager::CloseBrowsers() {
  // ...

  // Make a copy of the BrowserList to simplify the case where we need to
  // destroy a Browser during the loop.
  std::vector<Browser*> browser_list_copy;
  std::copy(BrowserList::GetInstance()->begin(),
            BrowserList::GetInstance()->end(),
            std::back_inserter(browser_list_copy));

  bool ignore_unload_handlers = browser_shutdown::ShouldIgnoreUnloadHandlers();

  for (auto* browser : browser_list_copy) {
    browser->window()->Close();                                                                                                       // <--- 2
    if (ignore_unload_handlers) {
      // This path is hit during logoff/power-down. In this case we won't get
      // a final message and so we force the browser to be deleted.
      // Close doesn't immediately destroy the browser
      // (Browser::TabStripEmpty() uses invoke later) but when we're ending the
      // session we need to make sure the browser is destroyed now. So, invoke
      // DestroyBrowser to make sure the browser is deleted and cleanup can
      // happen.
      while (browser->tab_strip_model()->count())
        browser->tab_strip_model()->DetachAndDeleteWebContentsAt(0);
      browser->window()->DestroyBrowser();                                                                                 // <--- 1
      // Destroying the browser should have removed it from the browser list.
      DCHECK(!base::Contains(*BrowserList::GetInstance(), browser));
    }
  }

  // ...
}

Line 1 leads to deleting a aura::Window (a child owned by its parent) here: https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/window.cc;drc=3e1a26c44c024d97dc9a4c09bbc6a2365398ca2c;l=928

Line 2 (presumably on another run through the loop) somehow accesses a property on the same aura::Window which causes a UAF.


Because of the tight race window and the one-shot nature of this browser-shutdown UAF, marking this as medium severity.

[Monorail components: Internals>Accessibility UI>Accessibility]

### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### mp...@chromium.org (2022-10-04)

FWIW the PoC looks very benign and you can test it without security concerns.

### [Deleted User] (2022-10-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ec97e10f34c2ba56491290382ca7751b1c0225c7

commit ec97e10f34c2ba56491290382ca7751b1c0225c7
Author: David Tseng <dtseng@google.com>
Date: Thu Oct 06 21:30:34 2022

Remove unneeded codepath AXWidgetObjWrapper::OnVisibilityChanged

This function was once needed[1] because focus changes might not be
conveyed when widgets were hidden.

Since then, focus is computed by AutomationInternalCustomBindings based
on raw tree updates, so this specific path is no longer needed.

This also has the benefit of avoiding a potential UAF (see bug) which
gets triggered when trying to dispatch a focus change during shutdown.

1. https://codereview.chromium.org/2456673002

R=katie@chromium.org

Bug: 1370562
AX-Relnotes: n/a
Test: cq. Manually open find dialog and press escape as per crbug.com/659813 and see bug does not occur.
Change-Id: I495a17defcdbe4be6e562f61a4d1834efa349543
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3938387
Reviewed-by: Katie Dektar <katie@chromium.org>
Commit-Queue: David Tseng <dtseng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1056019}

[modify] https://crrev.com/ec97e10f34c2ba56491290382ca7751b1c0225c7/ui/views/accessibility/ax_aura_obj_cache.h
[modify] https://crrev.com/ec97e10f34c2ba56491290382ca7751b1c0225c7/ui/views/accessibility/ax_widget_obj_wrapper.cc
[modify] https://crrev.com/ec97e10f34c2ba56491290382ca7751b1c0225c7/ui/views/accessibility/ax_widget_obj_wrapper.h


### gi...@appspot.gserviceaccount.com (2022-10-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ba128ad64ff3919d25a25396cba01e3e7046a55b

commit ba128ad64ff3919d25a25396cba01e3e7046a55b
Author: David Tseng <dtseng@google.com>
Date: Thu Oct 13 19:37:39 2022

Loosen destruction path in AXWindowObjWrapper

This change keeps around the root aura Window until it is actually
destroyed. Currently, we remove it during window destroying.

Bug: 1370562
Change-Id: I45c664d38dc704c12713aa8f6647e4bcd4e579dc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3934748
Reviewed-by: Katie Dektar <katie@chromium.org>
Commit-Queue: David Tseng <dtseng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1058875}

[modify] https://crrev.com/ba128ad64ff3919d25a25396cba01e3e7046a55b/ui/views/accessibility/ax_window_obj_wrapper.cc


### [Deleted User] (2022-10-17)

dtseng: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-31)

dtseng: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-28)

Confirmed with dtseng@ that this issue is resolved. 


### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1370562?no_tracker_redirect=1

[Multiple monorail components: Internals>Accessibility, UI>Accessibility]
[Monorail components added to Component Tags custom field.]

### ni...@google.com (2024-06-18)

Marking verified per  comment 13

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061216)*
