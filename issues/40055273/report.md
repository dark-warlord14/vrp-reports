# Security: UAF in InputHandler::InputInjector::InjectKeyboardEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40055273](https://issues.chromium.org/issues/40055273) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | bm...@chromium.org |
| **Created** | 2021-03-21 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

One of the methods available via the Chrome DevTools protocol is Input.dispatchKeyEvent. That method allows the caller to dispatch key events to the target page.

When sending a browser shortcut that would result in the debugged tab being closed (such as the shortcut to close that specific tab or the entire window), the debugging session will be detached. However, that occurs in the middle of InputHandler::InputInjector::InjectKeyboardEvent, resulting in the InputInjector object being deleted midway through the method.

**VERSION**  

Chrome Version: 89.0.4389.90 (stable), 91.0.4454.0 (canary)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Install the attached extension.
2. The extension will create a create a tab, attach the debugger to it, then send a Ctrl+W key press to it using the following Input.dispatchKeyEvent call:

chrome.debugger.sendCommand({tabId: tab.id}, "Input.dispatchKeyEvent", {type: "rawKeyDown", key: "W", windowsVirtualKeyCode: 87, nativeVirtualKeyCode: 87, modifiers: 2});

This browser shortcut is handled synchronously and results in the debugged tab being closed and the debugging session being detached. However, this occurs in the middle of InputHandler::InputInjector::InjectKeyboardEvent, resulting in a use-after-free in the browser process. You can verify that by installing the extension in an asan build.

This issue is similar to <https://crbug.com/chromium/1188889>, in that they both involve a use-after-free in the browser process that results from the debugging session being detached in the middle of a handler method.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 1.1 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 206 B)

## Timeline

### [Deleted User] (2021-03-21)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-03-21)

As mentioned in the summary, browser shortcuts are handled synchronously. The close tab shortcut, specifically, will be handled at:

https://source.chromium.org/chromium/chromium/src/+/master:chrome/browser/ui/browser_command_controller.cc;l=429;drc=5976a85bac31922f62d1947e6957f06fffe9fe1d

CloseTab will then synchronously close the tab, provided there's no need to run any unload handlers (which there isn't in the demonstration above). This results in the debugging session being detached and the InputHandler and InputInjector objects being deleted. This occurs in the middle of InputHandler::InputInjector::InjectKeyboardEvent, once the following call has finished executing:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/protocol/input_handler.cc;l=412;drc=aace0cfef2d51e7f038b07d5df26d126e4160f70

### pa...@chromium.org (2021-03-22)

Thanks for this report. Looks like definitely a bug, but probably not practically exploitable? The need to install an extension with debug permission, or very specific user gestures, seem like significant preconditions to attack.

[Monorail components: Platform>DevTools]

### [Deleted User] (2021-03-22)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2021-03-22)

Neither dgozman nor einbinder still work on Chrome.

### ya...@chromium.org (2021-03-22)

I'm beginning to think that extensions should not be able to send input events via CDP.

Of course the possible use after free should still be addressed.

### ca...@chromium.org (2021-03-23)

It looks like they actually do ;-) (https://chromium-review.googlesource.com/c/chromium/src/+/2779699/)

Not sure this warrants disabling an ability to dispatch input for chrome.debugger extensions -- I assume this to be a fairly common automation use case, and while this particular bug is in the input handler, we could as well make a similar omission elsewhere.


### de...@gmail.com (2021-03-23)

Would it be possible to have the severity here re-evaluated? While the user does need to install an extension with the debugger permission, there's no more interaction required then for other issues that have been filed in this area that have a higher severity.

For example, https://crbug.com/chromium/1030411 dealt with a case in which the debugger wasn't being detached soon enough, allowing a more privileged page (the Chrome Web Store) to be scripted by an extension. That issue was marked as medium severity.

Also, the severity guidelines include "Memory corruption that requires a specific extension to be installed" under medium severity:

https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#toc-medium-severity

I'm not sure whether the use-after-free in the issue linked there (313743) was in the browser or renderer, but here it's in the browser.

### gi...@appspot.gserviceaccount.com (2021-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/93f40c84987e4926f9b69391bb6dc79f08bbd8fd

commit 93f40c84987e4926f9b69391bb6dc79f08bbd8fd
Author: Joel Einbinder <einbinder@chromium.org>
Date: Tue Mar 23 08:21:17 2021

DevTools: Fix UAF in Input.dispatchKeyboardEvent

Bug: 1190550
Change-Id: Ie0e1b5641683a45446a263624bece1aa6e90bd9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2779699
Reviewed-by: Dmitry Gozman <dgozman@chromium.org>
Commit-Queue: Joel Einbinder <einbinder@chromium.org>
Cr-Commit-Position: refs/heads/master@{#865548}

[modify] https://crrev.com/93f40c84987e4926f9b69391bb6dc79f08bbd8fd/content/browser/devtools/protocol/input_handler.cc


### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-26)

Bumping to Medium because I agree with https://crbug.com/chromium/1190550#c8.

yangguo@, it looks like this might be fixed per https://crbug.com/chromium/1190550#c9? If so please could you mark it fixed? https://crbug.com/chromium/1190550#c5 says that einbinder@ is no longer on the Chrome team. einbinder@ - if that's the case, thanks a lot for the fix!

### ya...@google.com (2021-07-26)

Benedikt, please take a look.

### bm...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-04)

Congratulations, David! The VRP Panel has decided to award you $10,000 for this report. Nice work! 

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-13)

The commit in https://crbug.com/chromium/1190550#c9 went into M91, so labelling thus. Sorry we didn't include this in the release notes back then, David, nor assign a CVE - we'll rectify that.

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1190550?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055273)*
