# Security: Possible to download files from sandboxed frames

| Field | Value |
|-------|-------|
| **Issue ID** | [40052718](https://issues.chromium.org/issues/40052718) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2020-06-30 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

In the most recent version of Chrome, it's not possible to download files from a sandboxed frame, unless the allow-downloads flag is set. However, if a sandboxed frame calls window.open with the noopener option and a download URL, the download will proceed. This is true even though the download wouldn't work if window was first opened and then the download was attempted.

**VERSION**  

Chrome Version: Tested on 83.0.4103.116 (stable) and 86.0.4186.0 (canary)  

Operating System: Windows 10, version 1909

**REPRODUCTION CASE**

1. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 server.py 8080

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page includes a sandboxed iframe:

<iframe src="iframe.html" sandbox="allow-scripts allow-popups"></iframe>

5. Click within this iframe. This will open a new window using the following call:

window.open("download.txt", "\_blank", "noopener");

This should result in download.txt being downloaded.

Note that, in contrast, the following calls don't work:

Without noopener:

window.open("download.txt", "\_blank");

With noopener, but download attempted after opening window:

window.open("page.html", "\_blank", "noopener");  

location.href = "download.txt"; // This would be run from page.html.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [download.txt](attachments/download.txt) (text/plain, 1 B)
- [iframe.html](attachments/iframe.html) (text/plain, 113 B)
- [iframe.js](attachments/iframe.js) (text/plain, 121 B)
- [index.html](attachments/index.html) (text/plain, 152 B)
- [server.py](attachments/server.py) (text/plain, 488 B)

## Timeline

### ca...@chromium.org (2020-06-30)

clamy: Can you help further triage this from the web platform side? Thanks

I assigned low severity based on other iframe sandbox bypass bugs.

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### ca...@chromium.org (2020-06-30)

Actually assigning to clamy

### [Deleted User] (2020-07-01)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

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

### an...@google.com (2021-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6984c746bf1f7fd6745bd062b4b51f49cc717000

commit 6984c746bf1f7fd6745bd062b4b51f49cc717000
Author: Antonio Sartori <antoniosartori@chromium.org>
Date: Thu Aug 26 08:03:41 2021

Pass NavigationDownloadPolicy in CreateNewWindowParams

When opening popups with noopener, navigations are performed directly
by the CreateNewWindow mojo call. This mojo call was not sending the
NavigationDownloadPolicy parameter, allowing in this way to bypass
sandbox for download.

Bug: 1100761
Change-Id: I4f212738f8145460fb0bb3c420020c6cdbfa5551
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3033504
Commit-Queue: Antonio Sartori <antoniosartori@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Yao Xiao <yaoxia@chromium.org>
Cr-Commit-Position: refs/heads/main@{#915500}

[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/content/browser/renderer_host/navigation_controller_impl.cc
[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/content/browser/renderer_host/navigation_controller_impl.h
[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/content/common/frame.mojom
[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/content/public/browser/navigation_controller.h
[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/content/renderer/render_view_impl.cc
[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/third_party/blink/common/navigation/navigation_policy.cc
[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/third_party/blink/public/common/navigation/navigation_policy.h
[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/third_party/blink/web_tests/android/ChromeWPTOverrideExpectations
[modify] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/third_party/blink/web_tests/android/WebLayerWPTOverrideExpectations
[delete] https://crrev.com/43eee3c6c2b06d9c2d28caedf7de834269dfaff7/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_anchor_download_allow_downloads.sub.tentative.html
[add] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_anchor_download_allow_downloads.tentative.html
[delete] https://crrev.com/43eee3c6c2b06d9c2d28caedf7de834269dfaff7/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_anchor_download_block_downloads.sub.tentative.html
[add] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_anchor_download_block_downloads.tentative.html
[add] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_window_open_download_allow_downloads.tentative.html
[add] https://crrev.com/6984c746bf1f7fd6745bd062b4b51f49cc717000/third_party/blink/web_tests/external/wpt/html/semantics/embedded-content/the-iframe-element/iframe_sandbox_window_open_download_block_downloads.tentative.html


### an...@chromium.org (2021-08-26)

Fixed by #17.

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-01)

Congratulations, David! The VRP Panel has decided to award you $3000 for this report. Thank you for another high-quality and detailed submission! 

### am...@google.com (2021-09-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-02)

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1100761?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052718)*
