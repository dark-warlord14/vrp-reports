# Security: fullscreen notification overlap

| Field | Value |
|-------|-------|
| **Issue ID** | [40092417](https://issues.chromium.org/issues/40092417) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2018-09-10 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 69  

Operating System: windows 7

similar to <https://crbug.com/chromium/776418> , <https://crbug.com/chromium/806162>

online demo: <http://f.3cm.me/r/fullscreen.html>

see fullscreen.gif for reproduce steps

press anykey and you will overlap the notification

patch:  

maybe put the UI always on top is a good idea.

## Attachments

- [fullscreen.gif](attachments/fullscreen.gif) (image/gif, 95.7 KB)
- [fullscreen.html](attachments/fullscreen.html) (text/plain, 427 B)
- [fullscreen2.html](attachments/fullscreen2.html) (text/plain, 518 B)

## Timeline

### ma...@gmail.com (2018-09-10)

the main problem is :
it should kick it->opener->opener out of fullscreen mode
but it just check it->opener if kick it out of fullscreen mode

idea:
the check function should be recursive

### mp...@google.com (2018-09-10)

Thanks for the report!

Hi avi@, you handled both of the previous bugs, would you mind taking this one as well? If not can you please assign an owner or assign back to me for triage?

Thanks!

[Monorail components: UI>Browser>FullScreen]

### sh...@chromium.org (2018-09-11)

[Empty comment from Monorail migration]

### rs...@chromium.org (2018-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-24)

avi: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-10-08)

ma7h1as.l@gmail.com: The URL is no longer accessible. Can you please attach the html file here?

### ma...@gmail.com (2018-10-08)

re #6 sorry, the URL changed to http://1vpctucm.3cm.me/fullscreen.html

### me...@chromium.org (2018-10-08)

Attaching the files.

### sh...@chromium.org (2018-10-09)

avi: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

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

### av...@chromium.org (2019-06-19)

https://crbug.com/chromium/882363#c7's repro yields

[24198:1295:0619/194131.555345:INFO:CONSOLE(10)] "Uncaught TypeError: Cannot read property 'document' of null", source: http://1vpctucm.3cm.me/fullscreen2.html (10)

I still have a fix in mind, but can't test it.

### av...@chromium.org (2019-06-20)

OK, if you always allow popups for the site, it fails again:

[24515:1295:0619/200704.197466:INFO:CONSOLE(10)] "Failed to execute 'requestFullscreen' on 'Element': API can only be initiated by a user gesture.", source: http://1vpctucm.3cm.me/fullscreen2.html (10)

I still think adding paranoia to the fullscreen dropper is warranted.

### ma...@gmail.com (2019-06-20)

re #20 seems something was changed in those days' update , I'll write another POC , for the convenient of testing by you.

### ma...@gmail.com (2019-06-20)

http://applestore.ac.cn/f1  just click it , fullscreen notification will be overlapped again.

### av...@chromium.org (2019-06-20)

I can't get the new version (https://crbug.com/chromium/882363#c22) to work in 77.0.3824.6. I keep getting kicked out of fullscreen with the display of the popup.

I have a hardening in https://crrev.com/c/1668368 . When that lands, if you can test with Canary that'd be appreciated. Thanks!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/734edf88b49c56ba9ccfaccdeb3171fad6f6c0b8

commit 734edf88b49c56ba9ccfaccdeb3171fad6f6c0b8
Author: Avi Drissman <avi@chromium.org>
Date: Thu Jun 20 22:10:10 2019

Improve dropping fullscreen for security.

If dropping fullscreen for security, drop all pages in the
opener chain that are in fullscreen.

BUG=882363
TEST=as in bug

Change-Id: Ia730989dd77ff05fd724b1ead97dfa836e5b19e2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1668368
Commit-Queue: Avi Drissman <avi@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#671076}

[modify] https://crrev.com/734edf88b49c56ba9ccfaccdeb3171fad6f6c0b8/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/734edf88b49c56ba9ccfaccdeb3171fad6f6c0b8/content/browser/web_contents/web_contents_impl_browsertest.cc


### av...@google.com (2019-06-21)

This will be in the next canary, which will probably be numbered 77.0.3832.0. Can you verify in that canary?

### ma...@gmail.com (2019-06-21)

re #25 I'll test if the patch works , at next canary.

### av...@chromium.org (2019-07-15)

Ping; how does this look?

### va...@chromium.org (2019-07-16)

[Empty comment from Monorail migration]

### ma...@gmail.com (2019-07-16)

[Comment Deleted]

### ma...@gmail.com (2019-07-16)

re #28  The original issue was reported 1 year ago , The time is too long to be able to confirm whether this patch or historical update fixes the problem.  But I can no longer reproduce it in canary , so the issue is fixed.

### av...@chromium.org (2019-07-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-07-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-23)

Requesting merge to M76 because latest trunk commit (671076) appears to be after beta branch point (665002).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-23)

This bug requires manual review: We are only 6 days from stable.
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
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2019-07-23)

This has been present since M69. Let's target 77 for this fix.

### na...@google.com (2019-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-07-30)

Congrats the Panel decided to reward $1,000 for this report!

### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

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

This issue was migrated from crbug.com/chromium/882363?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092417)*
