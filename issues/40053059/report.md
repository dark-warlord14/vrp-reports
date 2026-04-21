# Security: Possible for extension to escape sandbox via Input.dispatchKeyEvent and devtools_page

| Field | Value |
|-------|-------|
| **Issue ID** | [40053059](https://issues.chromium.org/issues/40053059) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>DevTools>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2020-08-12 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

When using the chrome.debugger API, one of the methods an extension can call is Input.dispatchKeyEvent. That method allows input events to be dispatched to a page being debugged.

Using the fact that it's possible to dispatch browser shortcuts using this method, an extension can open the devtools, then go through a series of steps to run code within the context of the chrome://downloads page. From there, an extension can open a downloaded executable and escape the sandbox.

**VERSION**  

Chrome Version: Tested on 84.0.4147.125 (stable) and 86.0.4231.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Install the attached extension.
2. Wait about 15 seconds.
3. The target executable (in this case, Process Explorer) should be started.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 6.4 KB)
- [chrome_inspect.js](attachments/chrome_inspect.js) (text/plain, 1.1 KB)
- [devtools.js](attachments/devtools.js) (text/plain, 3.1 KB)
- [devtools_not_connected.js](attachments/devtools_not_connected.js) (text/plain, 2.5 KB)
- [devtools_page.html](attachments/devtools_page.html) (text/plain, 107 B)
- [devtools_page.js](attachments/devtools_page.js) (text/plain, 2.4 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 246 B)
- [notifier.html](attachments/notifier.html) (text/plain, 102 B)
- [notifier.js](attachments/notifier.js) (text/plain, 59 B)
- [panel.html](attachments/panel.html) (text/plain, 32 B)

## Timeline

### de...@gmail.com (2020-08-12)

The demonstration extension here performs a few steps:

1. The extension downloads the target executable.
2. It then opens https://www.google.com/ in a new tab.
3. Once https://www.google.com/ has loaded, the extension attaches to it using chrome.debugger.attach.
4. Using Input.dispatchKeyEvent, the extension then dispatches an F12 key press to the page. This results in the devtools being opened. As the extension specifies a devtools_page entry (devtools_page.html), the devtools will load that file in an iframe when opened.
5. Once devtools_page.html has loaded, the extension will request that it create and show a devtools panel. The reason for this is detailed below.
6. The extension then navigates the page being debugged to a file within the Chrome Media Router extension. As extensions can't debug other extensions, the debugger will be detached at this point.
However, it's still possible to script the page. Although the devtools blocks embedded extensions for chrome: and devtools: pages, it currently doesn't block extensions when the target is a chrome-extension: page:

https://source.chromium.org/chromium/chromium/src/+/master:third_party/devtools-frontend/src/front_end/extensions/ExtensionServer.js;l=1052;drc=af06661c518421604efa5631c385ace2cae96bd2

This means that the devtools_page entry can still run code within the page. It uses this ability to make the following calls within the context of the Media Router page:

chrome.settingsPrivate.setPref('homepage_is_newtabpage', false);
chrome.settingsPrivate.setPref('homepage', 'javascript:...');

7. The extension then navigates the page to devtools://devtools/.
8. Once it's done that, it attaches the debugger to the devtools panel that was created in step 5.
9. An Alt+Home key event is then dispatched to the panel using the Input.dispatchKeyEvent method. This, specifically, is why the panel was created.
A browser-level shortcut doesn't necessarily need to be dispatched to the page. If the shortcut is instead dispatched to the devtools (or a frame within it), it will generally have the same effect. That is, the browser will process a shortcut dispatched to the devtools or one of its subframes in the same way as it would process the shortcut if it were dispatched to the page.
However, that will only work if the frame is visible. If the key event is dispatched to a frame that's not visible (such as the devtools_page.html frame), the browser won't process it.
Therefore, that's why the panel is shown after it's created.
In this case, Alt+Home is the shortcut key for the browser homepage. As the homepage was set to a javascript: URL in step 6, that URL will be executed against the current (devtools:) page and create a console pin.
10. The extension will then navigate the page to https://www.google.com/ again.
11. Once https://www.google.com/ has loaded, the extension will attach the debugger to it.
12. Using Input.dispatchKeyEvent, the extension dispatches two F12 key events. The first closes the devtools and the second causes it to be reopened. This is necessary for the console pin added in step 9 to be loaded, since the devtools will only initialize saved console pins once (when opening).
13. The extension then navigates the page to chrome://inspect/.
14. From here, the remaining steps are the same as those described in https://crbug.com/chromium/1067382.

### de...@gmail.com (2020-08-12)

I think there's three key pieces of behavior that the demonstration extension relies on here:

1. The first is that it's possible to dispatch browser-level shortcuts using Input.dispatchKeyEvent. That allows the extension to open and close the devtools, as well as navigate to the homepage.

For the browser to process the key event (and not just the renderer), the key event type needs to be rawKeyDown and nativeVirtualKeyCode needs to be set:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/devtools/protocol/input_handler.cc;l=617;drc=3d3ee67f6904c527aca96b54588cb1008a17b23e

2. The second piece of behavior the extension relies on (along with https://crbug.com/chromium/1106456) is the fact that a devtools_page entry remains active when the page being debugged is a chrome-extension: page. The extension uses this ability to change the homepage URL via a chrome.settingsPrivate.setPref call in the Media Router extension.

3. The third is that it's possible to execute a javascript: URL against a devtools: page.

### va...@chromium.org (2020-08-12)

Similar to https://crbug.com/chromium/1114636.

[Monorail components: Platform>DevTools Platform>DevTools>Platform]

### [Deleted User] (2020-08-13)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2020-08-14)

I do not agree with the assessment that this is a Stable Blocker.

For chrome.debugger.attach, the extension requires debugger permissions [0]. With that, the extension already can do everything DevTools can do. I'm not even sure this is a security issue at all.

[0] https://developer.chrome.com/extensions/debugger

### de...@gmail.com (2020-08-15)

Re https://crbug.com/chromium/1115460#c7:

While extensions with the debugger permission can access the DevTools protocol API in the same way the DevTools can, extensions have various limitations imposed on them. For example, they can't attach to privileged pages, such as chrome: and devtools: pages. They also don't have access to a number of the protocol methods. For instance, extensions can't call Target.attachToTarget or Browser.setDownloadBehavior.

So an extension with the debugger permission doesn't have the full set of abilities that the DevTools has.

https://crbug.com/chromium/1030411 is an example of a relatively recent bug that dealt with the debugger API. In that issue, the problem was that the debugger wasn't being detached soon enough when an extension navigated the debugged page to a privileged location (the Chrome Web Store in that case). That issue was marked as medium severity.

Here, an executable is run outside of the sandbox.

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### aj...@google.com (2020-09-28)

Adding a few people from #1114636 as this is a similar issue. Setting as Medium severity.

### [Deleted User] (2020-09-29)

caseq: Uh oh! This issue still open and hasn't been updated in the last 48 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-29)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-09-29)

Based on the description, I think this probably affects versions earlier than M86 ("tested on M84") so I think https://crbug.com/chromium/1115460#c3 is wrong. Adjusting so this no longer blocks M86 stable release.

### [Deleted User] (2020-10-14)

caseq: Uh oh! This issue still open and hasn't been updated in the last 63 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### ds...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-10-19)

Similar to crbug.com/1117173. Use aura::Window::delegate()->OnEvent() instead of WindowTreeHost::GetEventSink()->OnEventFromSource() in [1] and [2]. aura::Window::delegate()->OnEvent() should skip all the accelerators and IME handling, see [3] for an explainer.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/virtual_keyboard_private/chrome_virtual_keyboard_delegate.cc;drc=7b64df7e0a92c9a72624b859982a6532e75ae3f8;l=90
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/virtual_keyboard_private/chrome_virtual_keyboard_delegate.cc;drc=7b64df7e0a92c9a72624b859982a6532e75ae3f8;l=146
[3] https://chromium.googlesource.com/chromium/src/+/HEAD/docs/ui/input_event/index.md#:~:text=Phase%203%20%2D%20EventTarget%20regular 

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ds...@chromium.org (2021-11-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e86364149d89a818fde00c5dbe67cc3be1e807c4

commit e86364149d89a818fde00c5dbe67cc3be1e807c4
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Nov 30 14:24:36 2021

Don't send synthetic input events from chrome extensions to the browser.

Bug: 1115460
Change-Id: I4121ce81bbba679f5c98bc4c261d62ba86ebe434
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3301051
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Camille Lamy <clamy@chromium.org>
Cr-Commit-Position: refs/heads/main@{#946443}

[modify] https://crrev.com/e86364149d89a818fde00c5dbe67cc3be1e807c4/content/browser/devtools/protocol/input_handler.h
[modify] https://crrev.com/e86364149d89a818fde00c5dbe67cc3be1e807c4/content/public/browser/devtools_agent_host_client.cc
[modify] https://crrev.com/e86364149d89a818fde00c5dbe67cc3be1e807c4/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/e86364149d89a818fde00c5dbe67cc3be1e807c4/content/browser/devtools/protocol/input_handler.cc
[modify] https://crrev.com/e86364149d89a818fde00c5dbe67cc3be1e807c4/chrome/browser/devtools/protocol/devtools_protocol_test_support.h
[modify] https://crrev.com/e86364149d89a818fde00c5dbe67cc3be1e807c4/chrome/browser/devtools/protocol/devtools_protocol_test_support.cc
[modify] https://crrev.com/e86364149d89a818fde00c5dbe67cc3be1e807c4/content/public/browser/devtools_agent_host_client.h
[modify] https://crrev.com/e86364149d89a818fde00c5dbe67cc3be1e807c4/content/browser/devtools/render_frame_devtools_agent_host.cc


### ds...@chromium.org (2021-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ffddf45d9b362f1acecd15dcf3cc2525db494beb

commit ffddf45d9b362f1acecd15dcf3cc2525db494beb
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Dec 08 11:21:17 2021

Disallow executing javascript: URLs against devtools:// scheme

Bug: 1115460
Change-Id: I5b9cf302f5977997b139ff9de268205e2759b88d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3320444
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#949467}

[modify] https://crrev.com/ffddf45d9b362f1acecd15dcf3cc2525db494beb/content/renderer/render_thread_impl.cc
[modify] https://crrev.com/ffddf45d9b362f1acecd15dcf3cc2525db494beb/chrome/browser/devtools/devtools_browsertest.cc


### am...@chromium.org (2022-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/1f74767043f4410f24ddcc7cf65e067c91e89265

commit 1f74767043f4410f24ddcc7cf65e067c91e89265
Author: Danil Somsikov <dsv@chromium.org>
Date: Wed Feb 02 10:44:44 2022

Option to forbid certain origins for devtools extensions.

This is used and tested in crrev.com/c/3429170

Bug: 1115460
Change-Id: I55df48f3d10a0c2163bad068e16bd630ba4b6c8f
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/3428454
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/1f74767043f4410f24ddcc7cf65e067c91e89265/front_end/devtools_compatibility.js
[modify] https://crrev.com/1f74767043f4410f24ddcc7cf65e067c91e89265/front_end/models/extensions/ExtensionServer.ts


### gi...@appspot.gserviceaccount.com (2022-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ad761e203339d008147dd46c1a79e60301b6b058

commit ad761e203339d008147dd46c1a79e60301b6b058
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Feb 02 15:15:02 2022

Roll DevTools Frontend from 2b8d9b85fe74 to 1f74767043f4 (4 revisions)

https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/2b8d9b85fe74..1f74767043f4

2022-02-02 dsv@chromium.org Option to forbid certain origins for devtools extensions.
2022-02-02 tikuta@chromium.org devtools_plugin: mark non-relative import as external
2022-02-02 szuend@chromium.org Minify locale JSON files at build time
2022-02-02 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update DevTools DEPS.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/devtools-frontend-chromium
Please CC devtools-waterfall-sheriff-onduty@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1115460,chromium:1278663
Tbr: devtools-waterfall-sheriff-onduty@grotations.appspotmail.com
Change-Id: I6c0452f56ef92385c747ea14f9d6ad268db39209
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3431566
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#966195}

[modify] https://crrev.com/ad761e203339d008147dd46c1a79e60301b6b058/DEPS


### gi...@appspot.gserviceaccount.com (2022-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/09927ca7399717d3bb45c2948ffbb7682526b579

commit 09927ca7399717d3bb45c2948ffbb7682526b579
Author: Danil Somsikov <dsv@chromium.org>
Date: Thu Feb 03 07:04:10 2022

Disallow devtools extensions access to component extensions.

Bug: 1115460
Change-Id: I560bedd9042268a932fe4f28a5c344c218f0865c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3429170
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#966617}

[modify] https://crrev.com/09927ca7399717d3bb45c2948ffbb7682526b579/chrome/browser/devtools/devtools_browsertest.cc
[rename] https://crrev.com/09927ca7399717d3bb45c2948ffbb7682526b579/chrome/test/data/devtools/extensions/can_inspect_url/devtools.js
[rename] https://crrev.com/09927ca7399717d3bb45c2948ffbb7682526b579/chrome/test/data/devtools/extensions/can_inspect_url/manifest.json
[modify] https://crrev.com/09927ca7399717d3bb45c2948ffbb7682526b579/chrome/browser/devtools/devtools_ui_bindings.cc
[rename] https://crrev.com/09927ca7399717d3bb45c2948ffbb7682526b579/chrome/test/data/devtools/extensions/can_inspect_url/devtools.html


### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-17)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Thank you for this excellent report and your patience while we fixed and resolved this issue. 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1115460?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>DevTools>Platform]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053059)*
