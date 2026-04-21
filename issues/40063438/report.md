# Security: Using popups, Incognito Mode-specific external protocol prompts can be overlaid on other origins on Android.

| Field | Value |
|-------|-------|
| **Issue ID** | [40063438](https://issues.chromium.org/issues/40063438) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>Intents, UI>Browser>Incognito |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-03-07 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

While retesting <https://bugs.chromium.org/p/chromium/issues/detail?id=1404621>, I noticed that the incognito mode-specific external protocol prompt can still be overlaid by using a popup instead of a top-level navigation.

This requires the popup-blocker to be disabled.

**VERSION**  

Chrome Version: 113.0.5633.0 Canary  

Operating System: Android 13

**REPRODUCTION CASE**

1. Download Chrome canary so you can test the fix at <https://bugs.chromium.org/p/chromium/issues/detail?id=1404621>
2. Go to Settings > Site Settings > Popups and redirects > set to Allowed, to disable popup blocker.
3. Now open new incognito tab and go to <https://spice-flicker-squirrel.glitch.me/apple-spoof-2.html>
4. The prompt overlay on <https://apple.com> and cause potential user confusion (as "This site" would refer to the site presented in omnibox which is apple.com), click "Leave" will open phone app

apple-spoof-2.html

```
<script>  
location.href="tel:1111"  
setTimeout('window.open("https://apple.com")', 500)  
</script>  

```

The main difference from the previous report PoC is that we are now using window.open() to open <https://apple.com> instead of location.href. This will trigger a popup instead of a top-level navigation.

Not sure if you're using ModalDialogManager class but if you are, then passing ModalDialogManager.ModalDialogType.TAB for the incognito dialog should probably work for both cases, according to a similar bug I reported <https://chromium.googlesource.com/chromium/src/+/5e9547cb44713c1944f499c8b633aaa43fb46013/components/webapps/browser/android/java/src/org/chromium/components/webapps/AddToHomescreenDialogView.java#133>

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Timeline

### [Deleted User] (2023-03-07)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-03-08)

assigning as per https://crbug.com/chromium/1404621

[Monorail components: Mobile>Intents UI>Browser>Incognito]

### [Deleted User] (2023-03-08)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2023-03-08)

Thanks for the report. Given you have to allow popups for this, and the original issue was already very low on the severity, this is borderline not worth fixing.

Unfortunately the code is very old and pre-dates the ModalDialogManager, and migrating to it would be annoying. If we ever get around to updating all of our AlertDialogs in Chrome to the ModalDialogManager this issue will go away.

### mt...@chromium.org (2023-07-13)

roagarwal is turning the incognito dialog into a modal dialog which I believe should fix this issue.

### mt...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e5d62ba06f8af010799b746244d3e66bdc05b7c8

commit e5d62ba06f8af010799b746244d3e66bdc05b7c8
Author: Rohit Agarwal <roagarwal@chromium.org>
Date: Thu Jul 13 19:13:55 2023

Android: Migrate Leave Incognito mode from alert dialog to Modal dialog

This CL migrates the usage of AlertDialog to Modal dialog for
ExternalNavigationHandler which solely used it for the
"Leave Incognito mode?" confirmation dialog.

The use of AlertDialog had limitations which resulted in issue stated
in crbug.com/1462104, around click-jacking. The click-jacking issue
has been solved elsewhere for permission dialogs (which are powered
by Chrome's modal dialog framework) by introducing some
delay when the buttons in the dialog becomes functional.

Following the same, this CL upgrades the AlertDialog to use Chrome's
Modal dialog support instead.

Demo: https://drive.google.com/file/d/1dkOr2hQodrjS4Ogy7qjiQZPWfAXGtqcN/view?usp=sharing
Bug: 1462104, 1422272, b/291039251
Change-Id: I51d53492f2aca3a5642ea794652997537a3273e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4681767
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Rohit Agarwal <roagarwal@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Lijin Shen <lazzzis@google.com>
Cr-Commit-Position: refs/heads/main@{#1170075}

[modify] https://crrev.com/e5d62ba06f8af010799b746244d3e66bdc05b7c8/components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java
[modify] https://crrev.com/e5d62ba06f8af010799b746244d3e66bdc05b7c8/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java
[modify] https://crrev.com/e5d62ba06f8af010799b746244d3e66bdc05b7c8/chrome/android/javatests/src/org/chromium/chrome/browser/externalnav/UrlOverridingTest.java


### ha...@gmail.com (2023-07-13)

From a cursory glance at the code, this CL doesn't solve this this problem

This is because of small issue:
(1) mModalDialogManager.showDialog(mPropertyModel, ModalDialogManager.APP) should be mModalDialogManager.showDialog(mPropertyModel, ModalDialogManager.TAB) to tie the dialog to the tab to dismiss the prompt.



### mt...@chromium.org (2023-07-13)

roagarwal said they would test this and change it to ModalDialogManager.TAB if it doesn't fix this bug (their change was for a different bug, but we tagged this one too as it was related)

### gi...@appspot.gserviceaccount.com (2023-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b5256e2bc923787841ade1a033420493bb3c8dc7

commit b5256e2bc923787841ade1a033420493bb3c8dc7
Author: Rohit Agarwal <roagarwal@chromium.org>
Date: Fri Jul 14 15:40:43 2023

Android: Update "Leave Incognito mode?" dialog type to TAB

This CL changes the type of the "Leave Incognito mode?" dialog from APP
to TAB, as the dialog is opened in the context of the current tab and
should be dismissed if the tab changes in the background. Using ModalDialogType.APP unfortunately prevents that as such dismissal logic
are handled by TabModelLifetimeHandler, which works on TAB based
dialogs.

Demo: https://drive.google.com/file/d/11LZQWlu3k4Nu9OxR4nxOoxYolhFc16OD/view?usp=sharing
Bug: 1422272
Change-Id: Ic1920325664987d164c85890cacb10a94d2cc854
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4686981
Commit-Queue: Rohit Agarwal <roagarwal@chromium.org>
Reviewed-by: Michael Thiessen <mthiesse@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1170540}

[modify] https://crrev.com/b5256e2bc923787841ade1a033420493bb3c8dc7/components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java


### ro...@chromium.org (2023-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-21)

Thank you for the report, Axel! The VRP Panel decided to award you $500 for this issue, based on the significant limitations and impact of this issue, especially since prompts are necessary and cannot be eliminated. :) 
Thank you for your efforts to follow-up and report this issue to us nevertheless! 

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1422272?no_tracker_redirect=1

[Multiple monorail components: Mobile>Intents, UI>Browser>Incognito]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063438)*
