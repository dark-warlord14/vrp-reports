# Lao could lead to idn spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40091113](https://issues.chromium.org/issues/40091113) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Mac |
| **Reporter** | zx...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2018-04-15 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36

Steps to reproduce the problem:
http://xn--o7c4g.com/
http://xn--o7ca8kb.com/

What is the expected behavior?

What went wrong?
ຣ (U+0EA3) => s
໐ (U+0ED0) => o
ດ (U+0E94) => n
ຮ (U+0EAE) => s
ບ (U+0E9A) => u

for example, `so.com` and `soso.com` in top domain list could be spoofed by this two characters: ຣ໐

Did this work before? N/A 

Chrome version: 65.0.3325.181  Channel: stable
OS Version: OS X 10.13.4
Flash Version: Shockwave Flash 29.0 r0

## Attachments

- [soso.png](attachments/soso.png) (image/png, 7.1 KB)

## Timeline

### ca...@chromium.org (2018-04-16)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Security>UrlFormatting]

### ca...@chromium.org (2018-04-16)

[Empty comment from Monorail migration]

### mg...@chromium.org (2018-04-17)

jshin deals with domain name spoofing.

### js...@chromium.org (2018-04-17)

U+0e11 (ฑ) and U+0e17 (ท) in Thai can have a similar issue. 


### zx...@gmail.com (2018-04-18)

As you mentioned Thai, I considered about it yet,U+0E01(ก) is more similar to `n` in address bar than U+0e11 (ฑ) and U+0e17 (ท), and U+0E1A (บ) is similar to `u` as well, but there is no more characters looks like common latin characters, maybe U+0E1E (พ) is one

### sh...@chromium.org (2018-05-02)

jshin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-05-16)

jshin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2018-05-22)

https://chromium-review.googlesource.com/c/chromium/src/+/1058710

### bu...@chromium.org (2018-05-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8ac035c31d42cedcc2a772d7765622dc9f406240

commit 8ac035c31d42cedcc2a772d7765622dc9f406240
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue May 29 20:16:30 2018

Add Lao/Thai spoofable entries


    U+0E1E (พ) => w
    U+0E9E (ພ) => w
    U+0E9F (ຟ) => w

    U+0EA3 (ຣ) => s
    U+0EAE (ຮ) => s

    U+0E1A (บ) => u
    U+0E9A (ບ) => u

    Note that U+0E1F(ฟ) and U+0E23 (ร) were added a while ago.

BUG=833143
TEST=components_unittests --gtest_filter=*IDN*

Change-Id: I882e7d272cdca1d80aa23be94b4d7906ff8653c1
Reviewed-on: https://chromium-review.googlesource.com/1058710
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#562565}
[modify] https://crrev.com/8ac035c31d42cedcc2a772d7765622dc9f406240/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/8ac035c31d42cedcc2a772d7765622dc9f406240/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/8ac035c31d42cedcc2a772d7765622dc9f406240/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/8ac035c31d42cedcc2a772d7765622dc9f406240/components/url_formatter/url_formatter_unittest.cc


### sh...@chromium.org (2018-05-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2018-06-01)

Fixed in trunk. Will see if we want to merge to M-67. 

### sh...@chromium.org (2018-06-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-08)

This bug requires manual review: M68 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2018-06-08)

Approving merge for 68. BRanch:3440

### aw...@chromium.org (2018-06-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-06-08)

Thanks zxyrzg02@ for the report! The VRP panel decided to award $500 for this report.

### aw...@google.com (2018-06-09)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-06-18)

Pls merge you change to M68 branch 3440 ASAP so we can pick it up for this week Beta release. Merge has to happen latest by 1:00 PM PT tomorrow, Tuesday (06/19), so we can pick it up for Wednesday Beta release.





### ab...@google.com (2018-07-03)

Has this been merged yet to M68?

### bu...@chromium.org (2018-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/66b0b8146b61b90c87a4100d76ab9c8e4723d42c

commit 66b0b8146b61b90c87a4100d76ab9c8e4723d42c
Author: Jungshik Shin <jshin@chromium.org>
Date: Wed Jul 18 00:05:52 2018

[M68 branch] Add Lao/Thai spoofable entries

    U+0E1E (พ) => w
    U+0E9E (ພ) => w
    U+0E9F (ຟ) => w

    U+0EA3 (ຣ) => s
    U+0EAE (ຮ) => s

    U+0E1A (บ) => u
    U+0E9A (ບ) => u

    Note that U+0E1F(ฟ) and U+0E23 (ร) were added a while ago.

BUG=833143
TEST=components_unittests --gtest_filter=*IDN*
TBR=abdulsyed@chromium.org,meacer@chromium.org

Change-Id: I882e7d272cdca1d80aa23be94b4d7906ff8653c1
Reviewed-on: https://chromium-review.googlesource.com/1058710
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#562565}
Reviewed-on: https://chromium-review.googlesource.com/1141215
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3440@{#708}
Cr-Branched-From: 010ddcfda246975d194964ccf20038ebbdec6084-refs/heads/master@{#561733}
[modify] https://crrev.com/66b0b8146b61b90c87a4100d76ab9c8e4723d42c/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/66b0b8146b61b90c87a4100d76ab9c8e4723d42c/components/url_formatter/top_domains/test_domains.list
[modify] https://crrev.com/66b0b8146b61b90c87a4100d76ab9c8e4723d42c/components/url_formatter/top_domains/test_skeletons.gperf
[modify] https://crrev.com/66b0b8146b61b90c87a4100d76ab9c8e4723d42c/components/url_formatter/url_formatter_unittest.cc


### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### a-...@gtempaccount.com (2024-01-10)

JFYI, after https://chromium-review.googlesource.com/c/chromium/src/+/4725142
 `so.com` and `soso.com` are not in top domain list and could be spoofed as originally reported.

### is...@google.com (2024-01-10)

This issue was migrated from crbug.com/chromium/833143?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091113)*
