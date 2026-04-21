# Security: Picture in picture can hide fullscreen notification

| Field | Value |
|-------|-------|
| **Issue ID** | [40063918](https://issues.chromium.org/issues/40063918) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Windows |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2023-04-06 |
| **Bounty** | $1,000.00 |

## Description

redacted

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-04-06)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-04-06)

Assigning severity and owner based on past fullscreen related bugs. avi@ please re-route if necessary, thanks!

[Monorail components: UI>Browser>FullScreen]

### [Deleted User] (2023-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-07)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2023-04-10)

[Empty comment from Monorail migration]

### av...@chromium.org (2023-04-18)

FYI note that this is the same fundamental issue as https://crbug.com/chromium/1433581.

### ad...@google.com (2023-04-25)

pkasting@ hello!

It sounds like we have a window Z-order issue for every platform except Mac (see https://bugs.chromium.org/p/chromium/issues/detail?id=1433581#c10) and we might need to write some code to shuffle windows to comply (as best we can) with the Z-ordering which is properly respected on Mac only. I wondered if you might be a good person to (eventually) tackle that?

### av...@chromium.org (2023-04-25)

+kerenzhu from the Views team who’s done work in this area.

### ke...@chromium.org (2023-04-25)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-04-25)

On Aura, ZOrderLevel::kFloatingWindow, kFloatingUIElement and kSecuritySurface are equivalent. They all mean "always on top". The challenge is, there's no way to order among always-on-top windows on Windows. There is a frequently referenced blog about this "racing to the topmost" problem  [1] 

We might be able to work around that by playing with the timing of "set as always-on-top", although I have low confidence over this approach.

I don't know about Linux, but I can investigate. 

+dayeung who might also be interested in this. 

[1] https://devblogs.microsoft.com/oldnewthing/20110310-00/?p=11253

### es...@chromium.org (2023-04-27)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-05-04)

It seems that *double clicking* on open fullscreen is the key step to reproduce. If I click only once on the button, the fullscreen notification is on the topmost. This was tested on Windows. 

### ke...@chromium.org (2023-05-05)

On Windows, this issue may result from an undocumented behavior of the Window Manager.

Typically, the order of always-on-top windows is determined by the sequence in which they appear. The most recently shown window will be at the top. However, if any of these windows are child windows with non-topmost parents, they will be moved behind other always-on-top windows when their parent gains focus.

In the original report, the fullscreen notification is parented to the browser window, while the PiP window has no parent. The second click on the button activates the browser window, causing the notification to move behind the PiP window.

Given that this specific root cause is unique to Windows, it is likely a Windows-only bug. I have tested on Linux and ChromeOS. On Linux, the PiP is not displayed in fullscreen, while on ChromeOS, the PiP always remains on top. I don't know about Android and Fuchsia but I am also dropping their tags. 

### ev...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### ev...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-05-16)

I have a workaround CL https://chromium-review.googlesource.com/c/chromium/src/+/4508964. I am trying to find a more holistic solution per PK's suggestion. 

### [Deleted User] (2023-05-31)

kerenzhu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2023-06-14)

Hello any updates??

### [Deleted User] (2023-06-15)

kerenzhu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2023-06-28)

Hello any updates?


### gi...@appspot.gserviceaccount.com (2023-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0667d948a735286525995a75c2e305826fd1fda5

commit 0667d948a735286525995a75c2e305826fd1fda5
Author: Keren Zhu <kerenzhu@chromium.org>
Date: Thu Jun 29 03:45:31 2023

[win] Use top-level widget for fullscreen notification

On Windows, a topmost child window will be placed behind other topmost
windows when its parent gains focus. This is undesired for the
fullscreen notification, a security-related window, which was being
occluded by the PiP window under certain circumstances.

Fix this by showing fullscreen notification in a top-level widget.

Bug: 1431043, 1459121
Change-Id: I7c2823ccd0485acd65da39ed066675bd06486795
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4508964
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1163941}

[modify] https://crrev.com/0667d948a735286525995a75c2e305826fd1fda5/components/fullscreen_control/subtle_notification_view.cc


### sa...@gmail.com (2023-07-13)

Hello any updates?

### ke...@chromium.org (2023-07-13)

This should have been fixed. 

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-17)

This fix landed on 117 and should be merged to 116. 
Merge approved https://crrev.com/c/4508964; please merge this fix to branch 5845 at your earliest convenience. 

### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/350fc3d2a053c19951d67bed34a10977b27764c6

commit 350fc3d2a053c19951d67bed34a10977b27764c6
Author: Keren Zhu <kerenzhu@chromium.org>
Date: Tue Jul 18 21:01:24 2023

[m116][win] Use top-level widget for fullscreen notification

On Windows, a topmost child window will be placed behind other topmost
windows when its parent gains focus. This is undesired for the
fullscreen notification, a security-related window, which was being
occluded by the PiP window under certain circumstances.

Fix this by showing fullscreen notification in a top-level widget.

(cherry picked from commit 0667d948a735286525995a75c2e305826fd1fda5)

Bug: 1431043, 1459121
Change-Id: I7c2823ccd0485acd65da39ed066675bd06486795
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4508964
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1163941}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4690248
Commit-Queue: Peter Kasting <pkasting@chromium.org>
Auto-Submit: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#580}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/350fc3d2a053c19951d67bed34a10977b27764c6/components/fullscreen_control/subtle_notification_view.cc


### am...@google.com (2023-07-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-19)

Congratulations Hafiizh! The VRP Panel has decided to award you $1,000 for this report. We appreciate your efforts here, the reward amount was decided based on the limitations of this spoof and overall impact of this issue. 
We did sincerely appreciate the conciseness of the report -- but we also very much enjoyed your bear video and the use of music in your demonstration video! Thank you for your efforts as well as entertaining us through your report. 

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-07-31)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-07-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1431043?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1433581, crbug.com/chromium/1445293, crbug.com/chromium/1445382, crbug.com/chromium/1456870, crbug.com/chromium/1468900]
[Monorail components added to Component Tags custom field.]

### aj...@chromium.org (2025-10-28)

reporter: please remove restriction settings - chrome issues should be public once fixed.

### sa...@gmail.com (2025-10-29)

Im sorry i have unrestricted it but it automatically deleted by system

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063918)*
