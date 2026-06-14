# Security: Long extension name allows spoofing of Debugging InfoBar

| Field | Value |
|-------|-------|
| **Issue ID** | [40090846](https://issues.chromium.org/issues/40090846) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2018-03-19 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 67.0.3374.0 (Official Build) canary (64-bit)
Operating System: MacOS 

This is a hyphothetical attack like in https://crbug.com/chromium/673163.

1. Install the extension.
2. Observe the bubble is over the wrong origin
 
Note: I couldn't repro this on M65.

## Attachments

- [test case.zip](attachments/test case.zip) (application/octet-stream, 3.2 KB)
- [Screen Shot 2018-03-19 at 05.51.43.png](attachments/Screen Shot 2018-03-19 at 05.51.43.png) (image/png, 198.4 KB)

## Timeline

### es...@chromium.org (2018-03-19)

I'm a little confused what's going on here. It definitely seems non-ideal that we don't truncate the extension name so that the extension gets to control the whole contents of the infobar. However, I'm not sure if there's something weird about the infobar showing up on www.google.com; if the extension is debugging that tab, why do you say that the infobar is over the wrong origin?

[Monorail components: Platform>Apps>DevTools Platform>Extensions]

### dg...@chromium.org (2018-03-19)

Note that extension is effectively debugging the browser, so we show infobar on every tab.

Truncating is a good call though.


### el...@chromium.org (2018-03-20)

The Infobar isn't shown in Chrome 65 likely because the call to debugger.attach() in the extension fails with the error "Cannot access contents of the page. Extension manifest must request permission to access the respective host." It's not clear to me whether that call should also be failing in Chrome 67, or whether the failure was a bug in 65.

https://cs.chromium.org/chromium/src/chrome/browser/extensions/api/debugger/extension_dev_tools_infobar.cc?l=69&rcl=343599182ba14cb3d98c869c1afb01edc738e296

<message name="IDS_DEV_TOOLS_INFOBAR_LABEL" desc="Label displayed in an infobar when external debugger is attached to the browser">
  "<ph name="CLIENT_NAME">$1<ex>Extension Foo</ex></ph>" is debugging this browser
</message>

### el...@chromium.org (2018-03-20)

Weaknesses in the restrictions on debugger.attach look like a longstanding issue, see e.g. Issue  456994, https://crbug.com/chromium/805224

### es...@chromium.org (2018-03-20)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-03-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-20)

[Empty comment from Monorail migration]

### ts...@chromium.org (2018-05-03)

dgozman@ - are you the right person to drive this to completion? Otherwise, please re-assign as appropriate.

### dg...@chromium.org (2018-05-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fbeba958bb83c05ec8cc54e285a4a9ca10d1b311

commit fbeba958bb83c05ec8cc54e285a4a9ca10d1b311
Author: Dmitry Gozman <dgozman@chromium.org>
Date: Wed May 09 18:14:50 2018

Allow to specify elide behavior for confrim infobar message

Used in "<extension name> is debugging this browser" infobar.

Bug: 823194
Change-Id: Iff6627097c020cccca8f7cc3e21a803a41fd8f2c
Reviewed-on: https://chromium-review.googlesource.com/1048064
Commit-Queue: Dmitry Gozman <dgozman@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/master@{#557245}
[modify] https://crrev.com/fbeba958bb83c05ec8cc54e285a4a9ca10d1b311/chrome/browser/devtools/global_confirm_info_bar.cc
[modify] https://crrev.com/fbeba958bb83c05ec8cc54e285a4a9ca10d1b311/chrome/browser/extensions/api/debugger/extension_dev_tools_infobar.cc
[modify] https://crrev.com/fbeba958bb83c05ec8cc54e285a4a9ca10d1b311/chrome/browser/ui/views/infobars/confirm_infobar.cc
[modify] https://crrev.com/fbeba958bb83c05ec8cc54e285a4a9ca10d1b311/components/infobars/core/confirm_infobar_delegate.cc
[modify] https://crrev.com/fbeba958bb83c05ec8cc54e285a4a9ca10d1b311/components/infobars/core/confirm_infobar_delegate.h


### dg...@chromium.org (2018-05-09)

This should be fixed for all platforms which use views (linux and windows atm).

### sh...@chromium.org (2018-05-10)

[Empty comment from Monorail migration]

### aw...@google.com (2018-05-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-05-21)

$500 for this one :-)

### aw...@chromium.org (2018-05-21)

[Empty comment from Monorail migration]

### dg...@chromium.org (2018-05-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-05-29)

[Empty comment from Monorail migration]

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/823194?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/845270]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090846)*
