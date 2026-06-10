# Security: URL spoof using CJK combining character (U+3099 U+309A)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092064](https://issues.chromium.org/issues/40092064) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | zx...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-07-30 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36

Steps to reproduce the problem:
http://xn--google-1m4e.com/

What is the expected behavior?

What went wrong?
Latin characters are allowed mixing with one CJK character, but when mixing with CJK combining character(U+3099 U+309A), it may lead to url spoofing

Did this work before? N/A 

Chrome version: 68.0.3440.75  Channel: stable
OS Version: OS X 10.13.6
Flash Version: Shockwave Flash 30.0 r0

## Attachments

- [mac.png](attachments/mac.png) (image/png, 10.3 KB)
- [windows.jpg](attachments/windows.jpg) (image/jpeg, 2.3 KB)

## Timeline

### zx...@gmail.com (2018-07-30)

It seems more confusable on Windows than Mac

### mb...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

[Monorail components: UI>Security>UrlFormatting]

### jd...@chromium.org (2018-10-18)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-06-25)

This sounds like a straightforward fix: We shouldn't allow any of those characters (U+3099 U+309A) when used out of context.

https://cs.chromium.org/chromium/src/components/url_formatter/idn_spoof_checker.cc?rcl=22c184b6368c6169ba023f2c868169e638512093&l=311 is a good place to start.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a6429414c3cb6f719e621968a9ab38a63ee3eef1

commit a6429414c3cb6f719e621968a9ab38a63ee3eef1
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Thu Jul 25 22:27:14 2019

Disallow combining Kana voiced sound marks (U+3099 and U+309A) in IDN

This CL disallows U+3099 and U+309A characters from domain names. Any IDN
containing these characters will be displayed as punycode.

As of July 2019, these characters are not used in any popular domains.

Bug: 868846
Change-Id: I7e36b30d7dcaf167fb3a6eb23b96f0aa4bd393ee
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1717494
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#681043}

[modify] https://crrev.com/a6429414c3cb6f719e621968a9ab38a63ee3eef1/components/url_formatter/spoof_checks/idn_spoof_checker.cc
[modify] https://crrev.com/a6429414c3cb6f719e621968a9ab38a63ee3eef1/components/url_formatter/spoof_checks/idn_spoof_checker_unittest.cc


### me...@chromium.org (2019-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-27)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-07-29)

I think these are fairly good spoofs, I'd like to raise to medium severity. It made to M7, and I don't think we need to merge it to stable.

### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-30)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-30)

Requesting merge to M76 because latest trunk commit (681043) appears to be after beta branch point (665002).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-30)

This bug requires manual review: Request affecting a post-stable build
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

### go...@chromium.org (2019-07-30)

We already cut M76 stable RC. 

+adetaylor@, could you ptal if this need a merge to M76? And if yes, will it be ok to include in next M76 stable respin (if any)?


### ad...@chromium.org (2019-07-30)

Let's merge to M76 for the first stable respin - it looks like a trivial fix. (I am completely confident that there will be M76 stable respins :) )

### na...@google.com (2019-08-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-01)

Congrats! The Panel decided to reward you $1,000 for this report! 

### na...@google.com (2019-08-01)

[Empty comment from Monorail migration]

### ab...@google.com (2019-08-02)

meacer@ are you sure this will be a safe merge to M76? 

### me...@chromium.org (2019-08-02)

It's a minimal change, should be safe to merge. I looked at real world domains and none seemed to be affected.

### ab...@google.com (2019-08-05)

Approved - branch:3809

### me...@chromium.org (2019-08-05)

This turned out to be a nontrivial merge as the files have been moved and edited further. adetaylor@ and I agreed that we can do away with merging to M-76. It already made to M77 so there isn't more to do here. 

abdulsyed@: Should I just drop Merge-Approved-76 label?

### sh...@chromium.org (2019-08-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-08-22)

meacer@  Want to get clarification on your https://crbug.com/chromium/868846#c23, are you saying this merge is not needed for M76 and we are ok to wait for M77?

### ct...@chromium.org (2019-08-22)

meacer is OOO but my understanding is that the merge was abandoned due to being too complex for the added benefit. We are okay with waiting until M-77.

### sr...@google.com (2019-08-22)

updating the merge-approved label for M76 per https://crbug.com/chromium/868846#c27 so we dont track this change for merge

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/868846?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092064)*
