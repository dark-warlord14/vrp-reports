# when the filename contains a very long with special character can break/remove the extension of file in download buble

| Field | Value |
|-------|-------|
| **Issue ID** | [467442136](https://issues.chromium.org/issues/467442136) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2025-12-10 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS
this bug almost simillar of https://issues.chromium.org/issues/423956129 (this happened on extension dialog)

when the filename contains a very long filename with the addition (꧁ᬊᬁ ᬊ᭄꧂ツ) this can break/remove the extension of file in download buble (normally when using long filename without ꧂ it still show the extension of file. but when using ꧁ᬊᬁ it can break the text),so that it leads to spoof.

Steps to reproduce:
1. Open spooffile.html
2. click on spoof file button (for spoof)


VERSION
Chrome Version 145.0.7571.0 (Official Build) canary (64-bit)
Operating System: Windows 11

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [truncatedfiledownload.png](attachments/truncatedfiledownload.png) (image/png, 19.2 KB)
- [normalfiledownload.png](attachments/normalfiledownload.png) (image/png, 8.0 KB)
- [bandicam 2025-12-10 10-02-33-636.mp4](attachments/bandicam 2025-12-10 10-02-33-636.mp4) (video/mp4, 2.5 MB)
- [spooffile.html](attachments/spooffile.html) (text/html, 950 B)
- [Wed Dec 10 2025 16:16:32 GMT-0800 (Pacific Standard Time).png](attachments/Wed Dec 10 2025 16_16_32 GMT-0800 (Pacific Standard Time).png) (image/png, 22.1 KB)

## Timeline

### li...@chromium.org (2025-12-10)

This seems similar to [crbug.com/461845669](https://crbug.com/461845669) where there's minimal sanitization around the download name. Reassigning to @ch...@chromium.org -- do you mind taking a look at this?

### ch...@chromium.org (2025-12-10)

Have only taken a look at the screenshots, but at first glance this seems like an issue with the multi line label and computing the space required to show it. When it's security-relevant to display the label properly (completely without it being cut off). @kerenzhu, mind taking a look?

### ch...@chromium.org (2025-12-10)

I might be missing something, but I don't see anything in download\_bubble\_row\_view.cc that manually sets the height of the label, so I think it's coming from some parent Views/LayoutManagers?

### ke...@chromium.org (2025-12-10)

This is going to be a difficult bug. We lack experts on RenderText which handles text eliding and line breaking.

### ke...@chromium.org (2025-12-10)

+David who used to work on RenderText.

### da...@chromium.org (2025-12-10)

This reminds of a similar bug where text descenders were cut off due to the scrollbar. <https://issues.chromium.org/u/1/issues/40889519>

re: [#comment4](https://issues.chromium.org/issues/467442136#comment4)

+1 it looks like the preferred height is incorrect (might even be capped somewhere) which is causing the file extension part of the string to be hidden and the top of the text to be cut off. What's the expected behavior if we have a really long string? Does the string ever get capped or do we just expand vertically into a scroll view?

### ch...@chromium.org (2025-12-10)

> +1 it looks like the preferred height is incorrect (might even be capped somewhere) which is causing the file extension part of the string to be hidden and the top of the text to be cut off. What's the expected behavior if we have a really long string? Does the string ever get capped or do we just expand vertically into a scroll view?

Thanks for checking. I think there shouldn't be a height cap, since it's in a scroll view anyway. It should just scroll for as long as it needs to.

### ch...@chromium.org (2025-12-10)

To clarify, I meant the DownloadBubbleRowView is contained inside a scroll view anyway: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/download/bubble/download_bubble_primary_view.cc;l=62;drc=f4b1a5f91e14941349a0319b35f71d3efb7350af>

### da...@chromium.org (2025-12-11)

Thanks. Did some investigation and it looks like the Label breaks the text properly into 5 lines. The problem is that the label height only accounts for the default line height of 20 while the special character has text ascenders and descenders that causes it to extend beyond that.

IE. Manually increasing the line height (`primary_label_->SetLineHeight(48);`) fixes the problem and shows the full text of the special character string.

This is a tricky bug. One potential solution is to have Label respect the visual height and not the layout height but this is a nontrivial fix. We have to be careful so the label doesn't regress when calculating its line height.

### da...@chromium.org (2025-12-12)

Originally I thought using visual height would be nontrivial because there's a perf gap where you may not want to deal with all of the shaping but it turns out that RenderText code is really inefficient and we already shape the text when you call helper methods like GetRequiredLines (no wonder we cache everything in RenderText).
I think I have a fix for this.

### ch...@chromium.org (2025-12-12)

Thanks David for the speedy investigation! Reassigning to you since it looks like you're working on a fix.

### dx...@google.com (2025-12-16)

Project: chromium/src  

Branch:  main  

Author:  David Yeung [dayeung@chromium.org](mailto:dayeung@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7256959>

Fix Multiline label height for glyphs w/ high ascenders and descenders

---


Expand for full commit details
```
     
    Label::GetBoundedTextSize calculated the text height solely based on the 
    baseline height. This ignored the actual visual height of the rendered 
    text, causing truncation for strings containing characters with large 
    ascenders or descenders. 
     
    This caused bugs with the DownloadBubble where filenames with special 
    characters were vertically cut off. 
     
    Fix is to use the maximum between the text's visual height and the 
    baseline height. 
     
    https://screenshot.googleplex.com/9DZJj79aNFGHccv 
     
    Ash pixel test label was also adjusted because of the change. No major 
    visual changes, just slight visual offset. Instead of triaging, ash 
    pixel tests require updating the revision number. 
     
    Fixed: 467442136 
    Change-Id: Id0a8b2e95353896e44800801fa508f4e17b7a3f4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7256959 
    Reviewed-by: David Black <dmblack@google.com> 
    Reviewed-by: Keren Zhu <kerenzhu@chromium.org> 
    Reviewed-by: Andrew Xu <andrewxu@google.com> 
    Commit-Queue: David Black <dmblack@google.com> 
    Auto-Submit: David Yeung <dayeung@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1559108}

```

---

Files:

- M `ash/clipboard/views/clipboard_history_item_view_pixeltest.cc`
- M `ui/views/controls/label.cc`

---

Hash: [62c1a660407ec8f7589a271587ffee39bc215751](https://chromiumdash.appspot.com/commit/62c1a660407ec8f7589a271587ffee39bc215751)  

Date: Tue Dec 16 03:00:09 2025


---

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
low impact security ui spoof via standard UI gestures


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> low impact security ui spoof via standard UI gestures

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/467442136)*
