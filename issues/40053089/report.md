# Security: Extensions can capture contents of local files using Page.captureScreenshot with fromSurface set to false

| Field | Value |
|-------|-------|
| **Issue ID** | [40053089](https://issues.chromium.org/issues/40053089) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions |
| **Platforms** | Windows |
| **Reporter** | de...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2020-08-14 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When using the chrome.debugger API, one of the methods an extension can call is Page.captureScreenshot. That method allows a screenshot of the frame being debugged to be captured.

When the fromSurface parameter passed to that method is set to false, the screenshot is captured from the view, rather than the surface. One consequence of that is that any content drawn on top of the debugged frame will be captured in the screenshot.

An extension can use that fact to capture the contents of local files.

**VERSION**  

Chrome Version: Tested on 84.0.4147.125 (stable) and 86.0.4233.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. Install the attached extension. Ensure that "Allow access to file URLs" isn't checked.
2. Once installed, the extension will download local\_file.html.
3. Once the download has completed, the extension will open local\_file.html in a new tab.
4. local\_file.html contains two subframes: one that loads file:///c:/ and another that loads iframe.html from within the extension. Because the second frame has an absolute position, it will be drawn underneath the first frame.
5. The extension will then attach the debugger to iframe.html and call Page.captureScreenshot with fromSurface set to false.
6. Once the extension has received the screenshot data, it will make the following call:

chrome.tabs.create({url: "data:image/png;base64," + screenshotData});

The resulting tab should show that the contents of the file:///c:/ frame have been captured. This is true even though the file:///c:/ frame is a sibling of the captured frame and not contained within it.

This issue is similar to <https://crbug.com/chromium/1116444>, which also uses Page.captureScreenshot.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [background.js](attachments/background.js) (text/plain, 2.8 KB)
- [iframe.html](attachments/iframe.html) (text/plain, 100 B)
- [iframe.js](attachments/iframe.js) (text/plain, 187 B)
- [local_file.html](attachments/local_file.html) (text/plain, 1.1 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 323 B)
- [background.js](attachments/background.js) (text/plain, 2.5 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 247 B)

## Timeline

### va...@chromium.org (2020-08-15)

1116444, 1116450 are similar to 1113565 so assigning to caseq@ and adding some other folks as well.

[Monorail components: Platform>DevTools Platform>Extensions]

### [Deleted User] (2020-08-15)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-15)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-28)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-11)

caseq: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

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

### ca...@chromium.org (2021-09-13)

This had the same underlying cause as https://crbug.com/chromium/1116444 and has been addressed along with that one in 
https://chromium-review.googlesource.com/c/chromium/src/+/2584806

The exploit currently fails with:

Unchecked runtime.lastError: {"code":-32000,"message":"Command can only be executed on top-level targets"}



### ca...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-09-14)

I don't think this issue is a duplicate. While the original demonstration extension does now fail because it's attempting to call Page.captureScreenshot for a nested frame, it's simple enough to adjust the extension so that it calls Page.captureScreenshot on a top-level frame, but still captures the contents of a local file.

I've attached an updated extension here that demonstrates that. To test:

1. Install the attached extension. Ensure that "Allow access to file URLs" isn't checked.
2. Once installed, the extension will open two new tabs: one containing manifest.json and one containing file:///c:/.
3. The extension will then attach the debugger to the manifest.json tab and call Page.captureScreenshot with fromSurface set to false.
4. Immediately after making that call, the extension will mark the file:///c:/ tab as active.
5. Once the extension has received the screenshot data, it will make the following call:

chrome.tabs.create({url: "data:image/png;base64," + screenshotData});

The resulting tab should show that the contents of the file:///c:/ tab have been captured (along with the rest of the browser window). This is true even though the extension isn't attached to the file:///c:/ tab.

### de...@gmail.com (2021-09-14)

I think the specific reason the behavior described in the previous comment occurs is because there's a delay (of 1/6th of a second) when capturing a screenshot from the view:

https://source.chromium.org/chromium/chromium/src/+/master:content/browser/renderer_host/render_widget_host_impl.cc;l=3356;drc=279d90cbebb0be2bff181c693e6c06cb4ac0f3e8

During that delay, if another tab is made active, the screenshot will ultimately show the contents of that tab, rather than the tab being debugged.

I think the fact that the screenshot is captured from the OS-level window is also part of it, since it means that whatever is shown within that window at the time is what will be captured, regardless of whether that's the original tab or another tab.

### aj...@google.com (2021-09-16)

caseq: (security marshal here) could you re-evaluate if this is a duplicate following https://crbug.com/chromium/1116450#c27 - thanks

### ca...@chromium.org (2021-09-16)

Thanks for the new exploit, David, I'll take a look into this!

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-04-20)

I wonder what use case do chrome extensions have to capture screenshots not from the surface?
Can we only allow capturing from the surface for extensions?

### ds...@chromium.org (2022-04-22)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2e8037c888191e014f208393af3a5bf5da4f83df

commit 2e8037c888191e014f208393af3a5bf5da4f83df
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Apr 25 12:18:01 2022

Only allow capturing screenshots from surface for chrome extensions.

Bug: 1116450
Change-Id: Ia4e081dbd44e0d3e2f85248b9e4ec9306e3ceb72
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3599349
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#995663}

[modify] https://crrev.com/2e8037c888191e014f208393af3a5bf5da4f83df/content/browser/devtools/protocol/page_handler.cc
[modify] https://crrev.com/2e8037c888191e014f208393af3a5bf5da4f83df/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/2e8037c888191e014f208393af3a5bf5da4f83df/content/browser/devtools/protocol/page_handler.h
[modify] https://crrev.com/2e8037c888191e014f208393af3a5bf5da4f83df/content/browser/devtools/render_frame_devtools_agent_host.cc


### ds...@chromium.org (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-06)

Thank you for this report, David! Due to the mitigations of this issue requiring an installed extension and the user gesture required to trigger this information leak issue, the VRP Panel has decided to award you $3,000 for this report. Thank you for another detailed report and taking the time to report this issue to us - including catching it still reproduced and providing a secondary POC! 

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1116450?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions]
[Monorail mergedinto: crbug.com/chromium/1116444]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053089)*
