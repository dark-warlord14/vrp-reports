# Security: Content Security Policy Bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40094709](https://issues.chromium.org/issues/40094709) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2019-04-23 |
| **Bounty** | $3,000.00 |

## Description

similar to https://crbug.com/chromium/669086 and https://crbug.com/chromium/747847
but when navigate iframe to javascript scheme , the problem comes again.

see poc.html


## Attachments

- [poc.html](attachments/poc.html) (text/plain, 170 B)
- [Screenshot from 2020-05-14 15-05-13.png](attachments/Screenshot from 2020-05-14 15-05-13.png) (image/png, 163.4 KB)

## Timeline

### mm...@chromium.org (2019-04-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy]

### mm...@chromium.org (2019-04-23)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-23)

CC'ing dddliv3@gmail.com who has reported exactly the same issue around the same time, just 44 minutes later.

### sh...@chromium.org (2019-04-24)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-04-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dd...@gmail.com (2019-04-25)

I have a question about the duplication of 955361 and 955350. 

The pocs of the two vulnerabilities are different. 

Is the reason for judging the two vulnerabilities as duplicates because the causes of the two vulnerabilities are the same? the same underlying implementation?

By the way,  my poc of 955361 can also be executed successfully in safari, but https://crbug.com/chromium/955350 can't. And I have also reported it to Apple.




### mm...@chromium.org (2019-04-30)

Yes, as far as I understood, the root cause is exactly the same, which means these issues are duplicates.

It also looked to me that both reporters are representing Tencent's Xuanwu Lab, so I wasn't even sure whether the vulnerability was found independently or together.

If you believe the root cause is different, please comment on that and either myself or my colleagues will separate the issues. And if that's the case, I apologize for the mistriage.

### sh...@chromium.org (2019-05-07)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-21)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-07-01)

andypaicu@, could you please take a look? This issue has been reported more than 2 months ago.

### an...@chromium.org (2019-07-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-08-19)

mkwst@: this issue is now pretty old. Can you take a look and see what the next step is? Thanks very much.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### ar...@chromium.org (2020-04-23)

Assigning this to me, because I already have a fix I made for bug: 
https://bugs.chromium.org/p/chromium/issues/detail?id=1064676#c16

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d

commit e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Mon Apr 27 09:39:30 2020

Forward CSP, even for the initial empty document.

https://crbug.com/chromium/1064676 has been fixed by:
  https://chromium-review.googlesource.com/c/chromium/src/+/2111170
And tested by:
  https://chromium-review.googlesource.com/c/chromium/src/+/2144012

The bug was fixed for every CSP checked in the renderer process. However
there are still an issue for the one checked in the browser process. It
turns out the CSP in the initial empty document weren't properly
propagated to the browser process.

This patch:
  1) Fix the bug by sending the CSP of the initial empty document.
  2) Add a regression test (WPT).

This patch can potentially also fix:
 - https://crbug.com/1072719
 - https://crbug.com/955350
(I haven't checked. I will do it later after landing this patch)

Bug: 1064676, 1072719, 955350
Change-Id: Ie5325035c74d9e2476d6c80af3e5d5c9068ea928
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2159242
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Auto-Submit: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#762769}

[modify] https://crrev.com/e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d/third_party/blink/renderer/core/loader/document_loader.cc
[add] https://crrev.com/e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/frame-src-javascript-url.html
[add] https://crrev.com/e9a4cd15f16c2cf24c31133120d4c7f0fa5f505d/third_party/blink/web_tests/external/wpt/content-security-policy/inheritance/support/empty.html


### ar...@chromium.org (2020-05-14)

I confirm the two patches I made for https://crbug.com/chromium/1064676 fixed the bug (This was a duplicate)

Fixed by:
- https://chromium-review.googlesource.com/c/chromium/src/+/2159242
- https://chromium-review.googlesource.com/c/chromium/src/+/2111170

Here is a screenshot before/after

### ma...@gmail.com (2020-07-30)

[Comment Deleted]

### ad...@chromium.org (2020-07-30)

Thanks for bringing this to our attention. As mentioned on https://crbug.com/chromium/1064676, we'll discuss this at next week's VRP panel.

### [Deleted User] (2020-07-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-05)

ma7h1as.l, congratulations! The VRP panel has decided to award you $3000 for this bug, apologies for not spotting the duplicate earlier. I will also arrange to credit you in the release notes.

### ma...@gmail.com (2020-08-06)

#26 thank you so much for solving the problem.

### ad...@google.com (2020-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/955350?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/955361]
[Monorail mergedinto: crbug.com/chromium/1064676]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094709)*
