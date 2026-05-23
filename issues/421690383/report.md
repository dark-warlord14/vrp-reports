# Improper eliding of data uri causes URL spoofing in preview page.

| Field | Value |
|-------|-------|
| **Issue ID** | [421690383](https://issues.chromium.org/issues/421690383) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Security (Use Subcomponent)>UrlFormatting |
| **Platforms** | Android |
| **Chrome Version** | 136.0.7103.127 |
| **Reporter** | x4...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2025-06-01 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

1. Visit <https://gojo-satorou-v7.github.io/chigorin/mahoraga.html> or host the code `<a href="data://text/html,<iframe src='https://example.com/https://google.com/fakepath1'>">click_me</a>`
2. Hold on the click me button and click on preview button.
3. Notice that the url shows ...google.com/fakepath

# Problem Description

## There are two problems:

1. First being obviously the incorrect eliding of the address which causes the url spoofing.
2. Second being that the html code in the data url is being rendered on the page which causes more damage than only the url spoofing. In version 129.0.6668.70 this vulnerability did not occur because first the data scheme and full url was being shown and also the html code was not rendered by the page.

The rendering of the code is more problematic as it allows potential vulnerabilities like clickjacking or script execution.

# Additional Comments

I believe it works on version 130.x.x.x since I've tested it on 130.0.6723.40 and it works but it does not work on version 129.0.6668.70
It works till the latest version 136.x.x.x [check POC]

# Summary

Improper eliding of data uri causes URL spoofing in preview page.

# Custom Questions

#### Reporter credit:

Abhishek Kumar

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: No

## Attachments

- [not working version 129.x.mp4](attachments/not working version 129.x.mp4) (video/mp4, 8.0 MB)
- [POC urlspoof.mp4](attachments/POC urlspoof.mp4) (video/mp4, 3.9 MB)
- [Fri Dec 19 2025 23:18:17 GMT+0530 (India Standard Time).png](attachments/Fri Dec 19 2025 23_18_17 GMT+0530 (India Standard Time).png) (image/png, 160.0 KB)
- [Screenshot_20260211_231949.png](attachments/Screenshot_20260211_231949.png) (image/png, 457.0 KB)

## Timeline

### x4...@gmail.com (2025-06-01)

I strongly believe that this commit might have caused this vulnerability <https://github.com/chromium/chromium/commit/6c1a0cec38d714f2c82c9bdb319409c597781acd>

### th...@chromium.org (2025-06-02)

[security shepherd]
I can mostly reproduce this on Android -- my version shows ".../https://google.com/fakepath1'>". It does seem like "data://text/html" should be displayed first in this case (not be clipped off). This is somewhat similar to older bug https://crbug.com/40095327. Setting low severity and Found In of extended stable.

Tentatively triaging to shaktisahu@ based on #comment2 -- could you PTAL or retriage as appropriate?

### ch...@google.com (2025-06-03)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### x4...@gmail.com (2025-06-11)

Hello,

The recently disclosed report <https://issues.chromium.org/issues/362545037> showing the same attack potential is now public.
Chrome users might be at risk. Please fix it asap.

### am...@chromium.org (2025-06-11)

Hello, this is a low severity, lower impact issue so please be advised that this issue does not have an SLO.
I am going to go ahead and re-assign to jinsukkim@ who was worked on the fix for [issue 362545037](https://issues.chromium.org/issues/362545037).

While the original report was just disclosed today, this is a lower impact issue with low attacker utility, so I did not plan on restricting it.
I did change my mind to avoid a bunch of reports of duplicates of that this issue showing demonstrating this is not fully resolved.

### x4...@gmail.com (2025-12-19)

Hi, this bug seems to be fixed. The preview page option doesn't appear now when holding over a data url.

### x4...@gmail.com (2026-01-15)

Friendly reminder: This bug seems to be fixed kindly check and close this bug.

Thanks!

### wf...@chromium.org (2026-02-11)

The VRP panel believes that a reasonable and prudent user would not suffer any safety consequences as a result of this issue.

### x4...@gmail.com (2026-02-17)

I'd like the panel to re-review the report on the following basis:
Technical aspect: the preview page renders entire code of the data payload with a near perfect url spoof (poc: <https://gojo-satorou-v7.github.io/chigorin/mahoraga.html>) however I agree it requires a lot of social-engineering for a full exploit.

Historical aspect: report <https://issues.chromium.org/issues/40056009> and <https://issues.chromium.org/issues/362545037> demonstrate the same impact same vulnerability which were awarded $1000.

### x4...@gmail.com (2026-03-15)

Any updates on the panel decision? Moreover I would like to point out that this vulnerability could also be considered as a top-level navigation bypass to data uri.

### jd...@google.com (2026-03-27)

Hi, the panel has it in the backlog for review and will revert once complete.  Its still pending. Apologies for the delay as we work through the backlog.  Thanks

### ch...@google.com (2026-05-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-05-19)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

The panel reviewed this again based on reporters request, and stands by the decision made to not award as noted in Comment 9

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

## Bounty Award

> The panel reviewed this again based on reporters request, and stands by the decision made to not award as noted in Comment 9
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Please fill out a [short anonymous survey](https://goo.gl/I

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/421690383)*
