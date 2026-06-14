# Security: Character “⠀” (U+2800) should be converted into code.

| Field | Value |
|-------|-------|
| **Issue ID** | [40051963](https://issues.chromium.org/issues/40051963) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2020-04-07 |
| **Bounty** | $500.00 |

## Description

invisible charaters such as "space" are usually converted into code when they come after the URL for example, http://google.com/%20%20%20%20%20%20%20%20%20%20%20%20%20%20index.html

There are some characters such as “⠀” (U+2800) which are not converted into code when added after the URL which may lead to URL spoofing using RTL characters since this area is really a messy area. 



## Timeline

### ra...@gmail.com (2020-04-07)

[Comment Deleted]

### xi...@chromium.org (2020-04-07)

Thanks for the report! This looks like a duplicate of crbug.com/824715. +cthomp@, could you confirm? Thanks!

[Monorail components: UI>Security>UrlFormatting]

### [Deleted User] (2020-04-09)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xi...@chromium.org (2020-04-10)

[Empty comment from Monorail migration]

### ct...@google.com (2020-04-10)

Thanks for the report. This is indeed similar to https://crbug.com/chromium/824715 where we switched to not decoding invisible characters we had previously missed. Tracking this separately as something missed from that previous bug (and since that bug has been opened since then) would be best.

I don't think U+2800 is considered to be in the spaces block, so it didn't come up when excluding spaces (in https://bugs.chromium.org/p/chromium/issues/detail?id=824715#c53). I think adding it to the exclusion list would be reasonable.

Unfortunately, it looks like unicode.org is currently down, so I can't double check the sets that might contain this and audit for similar characters -- I'll take a look next week and put together a CL updating the exclusion list.

### ct...@chromium.org (2020-04-13)

The Unicode technical site is down due to a datacenter failure, so I'll take the initial action of adding U+2800 to our "don't decode" list now and do more auditing as followup. Looking at some available Unicode data, U+2800 is explicitly not in WSpace or Formatting/Invisibles, which explains why we missed it earlier (despite it acting as... both).

### ra...@gmail.com (2020-04-13)

https://home.unicode.org/ - This site is up.

### ct...@chromium.org (2020-04-13)

Unfortunately that's just their new homepage, and doesn't have the technical documents and unicode block details :-/  (see https://home.unicode.org/technical-alert-unicode-technical-website-down/)


### ct...@chromium.org (2020-04-13)

CL up for review: https://chromium-review.googlesource.com/c/chromium/src/+/2147477

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1114475dd86b5c2fae002a26edc44941fc4d3179

commit 1114475dd86b5c2fae002a26edc44941fc4d3179
Author: Chris Thompson <cthomp@chromium.org>
Date: Mon Apr 13 22:17:25 2020

Add U+2800 to URL unescape banned list

U+2800 (BRAILLE PATTERN BLANK) isn't in the WSpace or
Formatting/Invisibles sets, but should be treated like a space for
purposes of unescaping.

Bug: 1068531
Change-Id: I151f7c803898bc86d81570a93fbe682daf1cca86
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2147477
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/heads/master@{#758627}

[modify] https://crrev.com/1114475dd86b5c2fae002a26edc44941fc4d3179/net/base/escape.cc
[modify] https://crrev.com/1114475dd86b5c2fae002a26edc44941fc4d3179/net/base/escape_unittest.cc


### ct...@chromium.org (2020-04-16)

I did another pass through various Unicode categories to try to spot any other characters we should include, but didn't come up with any that aren't already on the banned list, so marking this as Fixed. There are some edge cases (like the Ideographic Description Characters block) that might be "harder to see" but at least still render visually which I think are okay.

Resolving the BiDi re-ordering issue would more generally address this as well...

### [Deleted User] (2020-04-18)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-21)

Requesting merge to beta M83 because latest trunk commit (758627) appears to be after beta branch point (756066).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-21)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2020-04-21)

1. Yes, this is a fix for a security bug.
2. https://chromium-review.googlesource.com/c/chromium/src/+/2147477
3. Yes, verified in Canary.
4. This is a fix for a security bug.
5. No.
6. N/A

### sr...@google.com (2020-04-22)

+adetaylor@ , I am approving this change for M83 FYI

Merge approved for M83, branch:4103, please merge your changes asap


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1c086775df6987af45e4cb679efa5b642f307837

commit 1c086775df6987af45e4cb679efa5b642f307837
Author: Chris Thompson <cthomp@chromium.org>
Date: Wed Apr 22 20:22:02 2020

[M83] Add U+2800 to URL unescape banned list

U+2800 (BRAILLE PATTERN BLANK) isn't in the WSpace or
Formatting/Invisibles sets, but should be treated like a space for
purposes of unescaping.

(cherry picked from commit 1114475dd86b5c2fae002a26edc44941fc4d3179)

Bug: 1068531
Change-Id: I151f7c803898bc86d81570a93fbe682daf1cca86
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2147477
Reviewed-by: Matt Menke <mmenke@chromium.org>
Commit-Queue: Christopher Thompson <cthomp@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#758627}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2161474
Reviewed-by: Christopher Thompson <cthomp@chromium.org>
Cr-Commit-Position: refs/branch-heads/4103@{#276}
Cr-Branched-From: 8ad47e8d21f6866e4a37f47d83a860d41debf514-refs/heads/master@{#756066}

[modify] https://crrev.com/1c086775df6987af45e4cb679efa5b642f307837/net/base/escape.cc
[modify] https://crrev.com/1c086775df6987af45e4cb679efa5b642f307837/net/base/escape_unittest.cc


### na...@google.com (2020-04-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-23)

Congrats the Panel decided to award $500 for this report!

### ra...@gmail.com (2020-04-23)

[Comment Deleted]

### na...@google.com (2020-04-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-04)

Panel re-assessed as this report to be the same as the original reward value.  

### [Deleted User] (2020-07-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1068531?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1069672]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051963)*
