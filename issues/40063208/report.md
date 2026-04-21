# Security: Document PIP inherits wrong origin when opened from an extension popup

| Field | Value |
|-------|-------|
| **Issue ID** | [40063208](https://issues.chromium.org/issues/40063208) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-02-23 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

A PIP2 window opened from an extension popup shows the origin of the active tab, not the extension popup itself.

This allows an extension to programatically open a PIP2 window with spoofed security origin UI.

When a PIP window is being created in PictureInPictureWindowManager::EnterDocumentPictureInPicture, it accepts `parent_web_contents` as the first argument.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc;l=90>

// Shows a PIP window using the window controller for document picture in  

// picture.  

//  

// Document picture-in-picture mode is triggered from the Renderer via  

// WindowOpenDisposition::NEW\_PICTURE\_IN\_PICTURE, and the browser  

// (i.e. Chrome's BrowserNavigator) then calls this method to create the  

// window. There's no corresponding path through the WebContentsDelegate, so  

// it doesn't have a failure state.  

void EnterDocumentPictureInPicture(content::WebContents\* parent\_web\_contents,  

content::WebContents\* child\_web\_contents);

The parent web contents is passed in browser\_navigator.cc from `params->source_contents`.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=870>

// If this is a Picture in Picture window, then notify the pip manager about  

// it. This enables the opener and pip window to stay connected, so that (for  

// example), the pip window does not outlive the opener.  

if (params->disposition == WindowOpenDisposition::NEW\_PICTURE\_IN\_PICTURE) {  

PictureInPictureWindowManager::GetInstance()->EnterDocumentPictureInPicture(  

params->source\_contents, contents\_to\_navigate\_or\_insert);  

}

Because `params->source_contents` was null at this point, it is set to the active web contents. This is where the incorrect origin of the PIP2 comes from.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/browser_navigator.cc;l=639>

// If no source WebContents was specified, we use the selected one from  

// the target browser. This must happen first, before  

// GetBrowserForDisposition() has a chance to replace |params->browser| with  

// another one.  

if (!params->source\_contents && params->browser) {  

params->source\_contents =  

params->browser->tab\_strip\_model()->GetActiveWebContents();  

}

**VERSION**  

Chrome Version: 112.0.5612.0 + beta  

Operating System: Windows 11

Flag: #document-picture-in-picture-api

**REPRODUCTION CASE**

1. Install the attached extension (no extension permission required)
2. Press a key / click (transient user activation)

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [background.js](attachments/background.js) (text/plain, 218 B)
- [manifest.json](attachments/manifest.json) (text/plain, 223 B)
- [popup.html](attachments/popup.html) (text/plain, 170 B)
- [popup.js](attachments/popup.js) (text/plain, 370 B)
- [poc.webm](attachments/poc.webm) (video/webm, 641.2 KB)

## Timeline

### [Deleted User] (2023-02-23)

[Empty comment from Monorail migration]

### sr...@google.com (2023-02-23)

Thanks, I was able to reproduce this behavior.
Marking it as Medium since it's an UI spoof from a malicious extension.

[Monorail components: Blink>Media>PictureInPicture]

### [Deleted User] (2023-02-23)

[Empty comment from Monorail migration]

### li...@google.com (2023-02-23)

=> steimel@ who has been looking at similar issues.

### [Deleted User] (2023-02-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-09)

steimel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@chromium.org (2023-03-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d48afaac427e37792229c5b86b07e3bebdf7f9f9

commit d48afaac427e37792229c5b86b07e3bebdf7f9f9
Author: Tommy Steimel <steimel@chromium.org>
Date: Mon Mar 13 23:03:16 2023

pip2: Don't allow PiP windows to be opened from an extension popup

This CL blocks picture-in-picture windows from opening without a source
contents. This prevents a spoofing bug where the currently active tab
is set as the parent to the PiP window when the PiP window is actually
owned by an extension popup.

Bug: 1418549
Change-Id: I1c3eb6dc62b63df04860ca7248c0bfa4b3d2ceaa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4336356
Reviewed-by: Peter Boström <pbos@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1116663}

[modify] https://crrev.com/d48afaac427e37792229c5b86b07e3bebdf7f9f9/chrome/browser/ui/browser_navigator.cc
[modify] https://crrev.com/d48afaac427e37792229c5b86b07e3bebdf7f9f9/chrome/browser/ui/browser_navigator_browsertest.cc


### st...@chromium.org (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations, Thomas! The VRP Panel has decided to award you $2,000 for this report. Thank you for your effort and reporting this issue to us! 

### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### st...@chromium.org (2023-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1418549?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063208)*
