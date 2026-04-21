# URL spoofing using tel:

| Field | Value |
|-------|-------|
| **Issue ID** | [40056198](https://issues.chromium.org/issues/40056198) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser |
| **Platforms** | Windows |
| **Reporter** | ra...@gmail.com |
| **Assignee** | kn...@chromium.org |
| **Created** | 2021-06-13 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36

Steps to reproduce the problem:
Similar to https://crbug.com/chromium/1005596

1. Open the apple.html
2. Right click on the link and open it in incognito mode

What is the expected behavior?
the destination of file does appear in normal mode but doesn't appear in incognito mode.

What went wrong?
described above.

Did this work before? N/A 

Chrome version: 91.0.4472.101  Channel: stable
OS Version: 10.0

In the video, I've shown that in incognito mode the box doesn't show the destination of the file, but it shows in normal mode and guest mode.

## Attachments

- [apple.html](attachments/apple.html) (text/plain, 197 B)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 825.2 KB)
- [incognito.png](attachments/incognito.png) (image/png, 13.6 KB)

## Timeline

### [Deleted User] (2021-06-13)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-06-14)

knollr@ PTAL? Is this related to your change from https://crbug.com/chromium/754304 or https://crbug.com/chromium/1005596?

[Monorail components: UI>Browser]

### [Deleted User] (2021-06-14)

[Empty comment from Monorail migration]

### kn...@chromium.org (2021-06-24)

Thanks for the report!
So the scenario here would be if e.g. evil.com is embedded in an iframe of legit.com and the user right clicks a link to en external protocol in the iframe and selects "Open Link in Incognito Window"? In that case we don't tell the user that this came from evil.com and they might thing it's from legit.com (even though the new window has no content from legit.com).

I think this is caused by us not setting the initiating origin when using this context menu [1] as we don't seem to want to send the referrer header to OTR windows.
A fix would be to just set the initiating origin regardless of OTR or not, uploaded a CL: crrev.com/c/2983301

[1]: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/renderer_context_menu/render_view_context_menu.cc;l=2303;drc=a5184a57a5dd8c32d219a5df2e28f01faf3a03de

### kn...@chromium.org (2021-06-29)

+some folks for visibility on the bug

### gi...@appspot.gserviceaccount.com (2021-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2f311f6b6df602d7e92d992293387ee55bc7cfeb

commit 2f311f6b6df602d7e92d992293387ee55bc7cfeb
Author: Richard Knoll <knollr@chromium.org>
Date: Wed Jul 21 00:16:13 2021

Always populate the initiator origin

We show the initiator origin to the user in some browser UIs like
external protocol dialogs. This is meant to make spoofing harder as the
user would see the malicious origin where the external protocol link
came from. This also needs to be done when opening links into a new
Incognito window. We do need to make sure not to set the referrer header
for those requests though.

Bug: 1219354
Change-Id: Id00c6a6f9ba8e34433a8c042e3f7c2b7b2fca271
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2983301
Reviewed-by: Ramin Halavati <rhalavati@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Richard Knoll <knollr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#903713}

[modify] https://crrev.com/2f311f6b6df602d7e92d992293387ee55bc7cfeb/chrome/browser/renderer_context_menu/render_view_context_menu.cc
[modify] https://crrev.com/2f311f6b6df602d7e92d992293387ee55bc7cfeb/components/renderer_context_menu/render_view_context_menu_base.cc


### kn...@chromium.org (2021-07-26)

Fixed in 94.0.4583.0, we're now showing the initiator origin when a user ends up on an external protocol using "Open Link in Incognito Window", see attached screenshot.

### kn...@chromium.org (2021-07-26)

[Comment Deleted]

### [Deleted User] (2021-07-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-11)

Congratulations, the VRP Panel has decided to award you $1,000 for this report. Thank you for reporting this issue! 

### ra...@gmail.com (2021-08-11)

Request to VRP Panel: Can you please recheck this bug as this bug is similar (or reproduces) https://crbug.com/chromium/1005596 - So the reward should match, right?

### am...@chromium.org (2021-08-11)

Please note that there is another related bug tagged in the same comment above that garnered only a $1000 reward. Regardless, the reward decisions made by the VRP Panel are not just based on security bug type and impact, but the report quality and other factors. The VRP Panel discussed this today and determined this reward amount is commensurate for this report. I am happy to bring it back to the panel for reconsideration, but please know we did have this discussion about this report already. Thank you! 

### am...@google.com (2021-08-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-08-18)

hello, rayyanh@, the VRP Panel declines to adjust the reward amount as the original reward amount has been deemed as adequate for this report. 
It was also recommended that you review the Chromium Community Code of Conduct (https://chromium.googlesource.com/chromium/src/+/refs/heads/main/CODE_OF_CONDUCT.md) as some of your comments to the security team and developers in bug reports and emails over time are potentially violating this code of conduct. 

We greatly appreciate your bug reports, but please remember to be respectful and kind to the community members with whom you interact in the course of discussing security issues. Thank you! 

### ra...@gmail.com (2021-08-18)

"as some of your comments to the security team and developers in bug reports and emails over time are potentially violating this code of conduct. " 

I'm so sorry If some of my comments were potentially violating the code of conduct, please note that It was never my intention to hurt someone. I'll be careful next time.

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-11-02)

This issue was migrated from crbug.com/chromium/1219354?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056198)*
