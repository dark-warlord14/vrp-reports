# kMainSRTDownloadURL is HTTP

| Field | Value |
|-------|-------|
| **Issue ID** | [40083963](https://issues.chromium.org/issues/40083963) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2016-1693 |
| **Reporter** | np...@chromium.org |
| **Assignee** | ma...@chromium.org |
| **Created** | 2016-03-29 |
| **Bounty** | $500.00 |

## Description

the kMainSRTDownloadURL is HTTP.  Should be HTTPS.

https://code.google.com/p/chromium/codesearch#chromium/src/chrome/browser/safe_browsing/srt_field_trial_win.cc&q=f:/safe_browsing%20http://.*%5C.com%20-file:test&sq=package:chromium&l=28&ct=rc&cd=15&dr=C


## Timeline

### ma...@chromium.org (2016-03-30)

Marc-Antoine, can you take care of this please?


### ma...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### ma...@chromium.org (2016-04-20)

I'll do it... I'm there now...

### bu...@chromium.org (2016-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ff7b8097333f0abd117606334dc925b09a2b247f

commit ff7b8097333f0abd117606334dc925b09a2b247f
Author: mad <mad@chromium.org>
Date: Wed Apr 20 19:39:45 2016

Explicitly use HTTPS to download the CCT binary

TBR=mattm@chromium.org
BUG=598752

Review URL: https://codereview.chromium.org/1908613002

Cr-Commit-Position: refs/heads/master@{#388555}

[modify] https://crrev.com/ff7b8097333f0abd117606334dc925b09a2b247f/chrome/browser/safe_browsing/srt_field_trial_win.cc


### wf...@chromium.org (2016-04-20)

does this need a merge?

### wf...@chromium.org (2016-04-20)

This was already reported internally before the external report in https://crbug.com/chromium/603609 so I'm passing this to the VRP panel to decide if we can reward this or not.

### ja...@gmail.com (2016-04-20)

wfh@ does it mean no reward for my https://crbug.com/chromium/603609? 

### wf...@chromium.org (2016-04-20)

re: #7 that will be up to the VRP panel to decide.

### va...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

[Monorail components: Services>Safebrowsing]

### sh...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

### ma...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

### ma...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-21)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### ti...@google.com (2016-04-21)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### am...@chromium.org (2016-04-21)

OS-Windows by the looks of it.  Up to the desktop folks.

### go...@chromium.org (2016-04-22)

Before we approve merge to M50, Could you please confirm whether this bug is baked/verified in Canary and safe to merge? 

### go...@chromium.org (2016-04-22)

Please merge your change to M51 branch 2704 before 5:00 PM PST Monday (04/25/16) so we can take it for next week M51 Beta candidate cut. Thank you.

### bu...@chromium.org (2016-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e2cb81025e77fc6ba0b8c0019a34d44aa8f9a00e

commit e2cb81025e77fc6ba0b8c0019a34d44aa8f9a00e
Author: Marc-Andre (MAD) Decoste <mad@google.com>
Date: Mon Apr 25 21:11:32 2016

Explicitly use HTTPS to download the CCT binary

TBR=mattm@chromium.org
BUG=598752

Review URL: https://codereview.chromium.org/1908613002

Cr-Commit-Position: refs/heads/master@{#388555}
(cherry picked from commit ff7b8097333f0abd117606334dc925b09a2b247f)

Review URL: https://codereview.chromium.org/1919043002 .

Cr-Commit-Position: refs/branch-heads/2704@{#229}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/e2cb81025e77fc6ba0b8c0019a34d44aa8f9a00e/chrome/browser/safe_browsing/srt_field_trial_win.cc


### ma...@chromium.org (2016-04-25)

About the merge to M50, this bug is baked/verified in Canary and safe to merge.

But there's another discussion about on duplicate https://crbug.com/chromium/603609 where the security severity label was set to low (as I just did on this bug) so it might not be important enough to merge up to stable.

Opinions?

### go...@chromium.org (2016-05-06)

[Comment Deleted]

### ti...@google.com (2016-05-06)

FWIW, we don't merge Sec-Sev-Low to stable, so this can roll in with the initial M51 release unless there's a strong objection.

Updating labels for M-51. If you want this to go in an M-50 patch, remove the "release" label and please add "Merge-triage"

### ja...@gmail.com (2016-05-26)

[Comment Deleted]

### ja...@gmail.com (2016-05-26)

Tim - Thanks for the reward could you please credit me as "Khalil Zhani" not "jackwillzac"and Cc "chromium.khalil@gmail.com" as the right reporter.


### ti...@google.com (2016-05-26)

Updated:

As you've already seen, the reward was $500 :) CVE-ID is CVE-2016-1693.

I'll add your payment into next wee's payment process. Thanks Khalil (and I'll note this email address as yours for future reference)

### ti...@google.com (2016-05-26)

Also, just to note that we'd usually not reward this issue as your report is a duplicate of an existing issue. That said, we used our discretion to pay you anyway as your report sped up the resolution and brought more attention to this issue.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/598752?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/603609]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083963)*
