# Initiator origin not propagated on cross-profile navigations

| Field | Value |
|-------|-------|
| **Issue ID** | [40067517](https://issues.chromium.org/issues/40067517) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Internals>Permissions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2023-07-17 |
| **Bounty** | $500.00 |

## Description

Normally it should open a link like ms-calculator:: , tel:// , or whatsapp: and different link should show Extension URL Access.

After open link in new tab/window/incognito URL permission is show, but if link open link as different profile URL permission not show.

**VERSION**

Chrome Version: Version 116.0.5810.0 (Developer Build) (64-bit)  

Operating System: Win 11

**REPRODUCTION CASE**

1. Open Link URL
2. Click open link as different profile

MITIGATION

Please showing the initiator origin URL when a user ends up on an external protocol using if open link as different profile

Thanks

## Attachments

- [open.html](attachments/open.html) (text/plain, 205 B)
- [POC.mp4](attachments/POC.mp4) (video/mp4, 520.2 KB)
- [POC_Update.mp4](attachments/POC_Update.mp4) (video/mp4, 402.8 KB)
- [POC.mp4](attachments/POC_53017933.mp4) (video/mp4, 377.1 KB)
- [pdf-calc.html](attachments/pdf-calc.html) (text/plain, 865 B)

## Timeline

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### bo...@google.com (2023-07-17)

I think I see the concern, but I'm unclear on the steps to reproduce. 

In the demo recording you start in profile "2" and open the link as profile "1", which then presents the permission prompt as expected. 

Then while still in profile "2", you open the link as profile "3", which presents the permission prompt, but appears to incorrectly open the external handler despite the user not clicking to allow the action. 

So does this behavior occur only when there are 3 (or more) profiles, and the user transitions between specific pairs? 

I'm assuming this is a desktop-only issue, and setting FoundIn-114 with Medium severity. 

[Monorail components: Internals>Permissions]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### al...@gmail.com (2023-07-18)

hi bookholt 

Im clarification for the new video, maybe you saw the wrong video because the link still doesn't appear in the show URL if you open it in a different profile.

So there is no difference between profile "2" or "3", because when you open all profiles the results are the same not show prompt URL

Thanks

For this detail video :

1. Link open.html open in profile "2"
2. Open link as different profile like profile "1" or "3" not show URL

Thanks

### [Deleted User] (2023-07-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@gmail.com (2023-07-29)

A hyperlink inside a pdf file shown by the chrome pdf-viewer can link to a like ms-calculator:: can be opened as a new tab and show prompt URL. But After link open in different profile chrome not show prompt URL.

MITIGATION 

Please showing the initiator origin URL when a user ends up on an external protocol using if open link as different profile

Ref : https://bugs.chromium.org/p/chromium/issues/detail?id=528505

Thanks

### al...@gmail.com (2023-07-29)

Script pdf-calc

### el...@google.com (2023-07-31)

engedy@ Do you know who is an owner of such a prompt (see video https://crbug.com/chromium/1465276#c7)? 

### [Deleted User] (2023-07-31)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@gmail.com (2023-08-08)

Any Update for this report ?

Thanks

### [Deleted User] (2023-08-15)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-08-17)

Also looping in ellyjones@ -- do you know the answer to https://crbug.com/chromium/1465276#c9?

### el...@chromium.org (2023-08-17)

It's the external protocol dialog, and it has no particular owner. I'm fixing a related bug (https://crbug.com/chromium/1457702) so I can take this one too if andypaicu@ wants.

### an...@chromium.org (2023-08-18)

Thank you ellyjones@, I don't currently have cycles to look at this.

### al...@gmail.com (2023-09-08)

any update for this report ?

Thanks

### al...@gmail.com (2023-10-10)

any update for this report ?

Thanks

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### al...@gmail.com (2023-11-24)

any update for this report ?

Thanks

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### al...@gmail.com (2024-01-08)

after change year 
any update for this report ?


Thanks 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1465276?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### el...@chromium.org (2024-02-21)

I reproduced this locally. It is fairly straightforward.

1. Create a page (I used jsfiddle) containing this HTML: <a href="tel://1234567890">oops</a>
2. Left-click the link. The external protocol dialog will contain the origin the page is served from.
3. Right-click the link and choose to open in another profile. The external protocol dialog will have "a website" instead of the real origin.

### ap...@google.com (2024-02-28)

Project: chromium/src
Branch: main

commit 440c83d4177962e1d1e434b8928374eac08c5b68
Author: Elly Fong-Jones <ellyjones@google.com>
Date:   Wed Feb 28 18:18:07 2024

    contextmenu: propagate initiator when opening in profile
    
    When opening a link in another profile via the renderer context menu, we
    need to pass the initiating origin through in case that link causes the
    external protocol dialog to be displayed - otherwise, the external
    protocol dialog won't be attributed to the origin the link came from.
    
    Fixed: 40067517
    Change-Id: I0ceb2f1cd06d3c1917cec8bcca24885a2b124f40
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5313953
    Auto-Submit: Elly FJ <ellyjones@chromium.org>
    Reviewed-by: Avi Drissman <avi@chromium.org>
    Commit-Queue: Avi Drissman <avi@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1266525}

M       chrome/browser/renderer_context_menu/render_view_context_menu.cc

https://chromium-review.googlesource.com/5313953


### al...@gmail.com (2024-02-29)

Thanks for update fixed

If release CVE Please add :
 Reported by Kang Ali of Punggawa Sibersecurity

Thanks

### al...@gmail.com (2024-03-06)

After fixed, any update for reward bounty ?

Thanks 

### am...@chromium.org (2024-03-07)

Thank you for the report. It appears that an origin is simply not presented rather there being the potential for incorrect security UI and origin spoofing. I've reduced severity to reflect the low risk and potential security implications to users. Since we were able to make a beneficial change based on your report, the Chrome VRP Panel has decided to extend a $500 thank you reward for this report. A member of the Google p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us.

re: [comment #34](https://issues.chromium.org/issues/40067517#comment34), while we endeavor to make reward decisions as quickly as possible after a bug is fixed, the Chrome VRP Panel only meets once per week. The report was closed after last week's Panel so it was assessed this week. Thank you for your patience.

### am...@google.com (2024-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### al...@gmail.com (2024-03-07)

Thanks for the reward

will this report get a CVE ?

Thanks

### am...@chromium.org (2024-03-09)

I was remiss in not fully adjusting this to accurately reflect this as bug and fully reduce the severity the first time around. Since we do not consider the lack of an origin to be security vulnerability, I've updated this issue to reflect that.

in response to #37, OP while we do appreciate this report, as mentioned in here and in the reward judgement this isn't really considered a security vulnerability. Since this is not an exploitable security vulnerability, we'll be unable to issue a CVE for this issue.

### pe...@google.com (2024-06-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067517)*
