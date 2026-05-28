# clickjacking (enterjacking) download notification when a pip window closes

| Field | Value |
|-------|-------|
| **Issue ID** | [392375329](https://issues.chromium.org/issues/392375329) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2025-01-27 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

VULNERABILITY DETAILS
when opening a popup window in the pip window and at the same time the popup window is downloading a file and the pip window is closed the focus changes to the file that has been downloaded (download notification) this causes the file to be opened

VERSION
Chrome Version: Version 134.0.6981.0 (Official Build) canary (64-bit)
Operating System: Windows OS

REPRODUCTION CASE
1. open pocv.html
2. do enter 5-6 times fastly



CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- pocv.html (text/html, 1.5 KB)
- bandicam 2025-01-27 08-45-25-929.mp4 (video/mp4, 1.7 MB)
- bandicam 2025-02-24 15-01-45-096.mp4 (video/mp4, 2.6 MB)
- version 134.mp4 (video/mp4, 1.6 MB)
- version 136.mp4 (video/mp4, 2.2 MB)
- [enterjacking.html](attachments/enterjacking.html) (text/html, 1.5 KB)
- [bandicam 2025-05-31 04-21-18-553.mp4](attachments/bandicam 2025-05-31 04-21-18-553.mp4) (video/mp4, 1.4 MB)
- bandicam 2025-10-23 15-36-08-756.mp4 (video/mp4, 1.4 MB)
- [enterjacking (1).html](attachments/enterjacking (1).html) (text/html, 1.5 KB)

## Timeline

### aj...@google.com (2025-01-27)

Thanks, this is a bit of a stretch as it requires significant user interaction. It is also very similar to [issue 41496084](https://issues.chromium.org/issues/41496084) and might be root-caused as a dupe after investigation.

### aj...@google.com (2025-01-27)

The fix might be to stop the downloads notification from having focus at all - so sending to that team.

### ch...@chromium.org (2025-01-27)

I can take a look for download bubble... Though this looks like a lot of user interaction. I think we had some discussion about focus and it was decided that for a11y reasons we *should* focus the download bubble. Let me try to dig up those discussions and/or revisit with UX folks.

### pe...@google.com (2025-01-28)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2025-02-24)

hello, I have tried POC again, but in the latest version of Chrome, the bug has been fixed where (POC can no longer be reproduced) the download bubble does not appear in the pop up window (the download runs immediately without the download bubble appearing) so this is safe from enterjacking vulnerabilities

### ch...@chromium.org (2025-02-24)

Interesting. This may be a side effect of the new pinnable download button. Not sure what exactly would have changed to affect this, though. cc corising for pinnable toolbar button.

### co...@chromium.org (2025-02-24)

This shouldn't be related to the changes I've made though I'm not able to repro the issue to test with the flag enabled/disabled. I didn't make any changes to the downloads bubble itself (other than to change what button it anchors to).

### sa...@gmail.com (2025-03-18)

hi i can reproduce the poc in Version 134.0.6998.89 (Official Build) (64-bit) . but i can't reproduce it in Version 136.0.7073.0 (Official Build) canary (64 bit) (download bubble doesn't appear) is this fixed in version 136? i updated the poc .


REPRODUCTION CASE
1. open enterjacking.html
2. do enter 5-6 times fastly

### ch...@chromium.org (2025-05-30)

What I think is happening here, (accidentally got confused with another [issue 421348748](https://issues.chromium.org/issues/421348748), but the following actually applies to this issue):

Yep, it's a specific interaction with PIP windows. When the Pip window is closed, it activates the Browser, and then there's special [logic](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/download/bubble/download_toolbar_ui_controller.cc;l=791-796;drc=167e8ff1fd7d025bc0814b51b15ea0663f1ae790) to activate the download bubble. In general the download bubble [doesn't](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/download/bubble/download_toolbar_ui_controller.cc;l=1090-1093;drc=167e8ff1fd7d025bc0814b51b15ea0663f1ae790) start focused like that.

Ideally we could just not do that...

I think it was originally a workaround for some close-on-deactivate issues, but I think enough things have changed in that space (e.g. how tab modal stuff gets managed etc.) that I should revisit this and see if there's a different workaround that won't interact poorly with PiP windows.

### sa...@gmail.com (2025-05-30)

hi thank you this is different from crbug.com/392375329 on crbug.com/392375329 when pipwindow is closed focus automatically changes to download prompt.

on https://issues.chromium.org/issues/421348748  occurs when downloading a file and focus is directed to site information then the download prompt appears, focus does not change to download prompt (still on site information) then when pressing enter the focus changes to download prompt (no need close the pip window)

### dx...@google.com (2025-10-14)

Project: chromium/src  

Branch:  main  

Author:  Lily Chen [chlily@chromium.org](mailto:chlily@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7041986>

Protect download bubble from unintended key events

---


Expand for full commit details
```
     
    This change considers key events when protecting the download bubble row 
    view from unintended user input. Clicking (or pressing Enter) on the 
    download bubble row view may result in opening a downloaded file. The 
    existing InputEventActivationProtector prevents clicks too soon after 
    showing the download bubble (500 ms). After this change, key events are 
    subject to the delay as well. 
     
    This is only a partial mitigation for a number of variants of 
    "enterjacking" on the download bubble, because the 500 ms delay may not 
    be sufficient to catch all unintended keypresses. 
     
    Bug: 392375329, 405727341, 421348748, 421877606 
    Change-Id: Ia6252f397966dd1d5cb539bf5c58f348effebadc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7041986 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Auto-Submit: Lily Chen <chlily@chromium.org> 
    Commit-Queue: Lily Chen <chlily@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1529740}

```

---

Files:

- M `chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc`

---

Hash: [8be46d66315fc47df5634d7cface5b62d7673b26](https://chromiumdash.appspot.com/commit/8be46d66315fc47df5634d7cface5b62d7673b26)  

Date: Tue Oct 14 20:12:42 2025


---

### sa...@gmail.com (2025-10-15)

is this bug already fixed?

### ch...@chromium.org (2025-10-15)

Hm, it seems the original POC and the updated POC are both no longer working on stable now (M141), but I'm not sure what changed to fix it. I don't think what I thought was the root cause ([comment #10](https://issues.chromium.org/issues/392375329#comment10)) was fixed, but maybe somewhere along the way, a change in the download bubble, PIP windows, popup windows, or browser activation in general could have fixed this.

### sa...@gmail.com (2025-10-23)

hi i confirmed i cannot reproduced it in Version 143.0.7488.0 (Official Build) canary (64-bit). with a long download delay the bubbles are clearly visible

### sa...@gmail.com (2025-10-29)

hi ch..@chromium.org may you set it to fixed?

### sp...@google.com (2025-12-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Security UI Spoofing (Low Impact)


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/392375329)*
