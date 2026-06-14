# Security: Credit card information leakage in Chrome autofill

| Field | Value |
|-------|-------|
| **Issue ID** | [40091813](https://issues.chromium.org/issues/40091813) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ca...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2018-06-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Early in 2017, numerous security researches published articles relating to the information leakage within the Chrome autofill feature. The vulnerability raised within these articles related to the possibility for remote websites to harvest excessive amounts of personal information by requesting a limited amount of information from the user whilst stealing additional information in hidden (hidden from view) input form fields. The autofill feature within Chrome would populate the requested fields as well as the hidden fields thereby allowing malicious sites to harvest information the user may not be aware of including credit card information.  

A mitigating control in Chrome was implemented which separated autofill information into address information and credit card information. This would limit the amount of information obtainable by malicious scripts to only harvesting that which would be deemed part of the same information set as what was originally shared by the user i.e. personal information only, or credit card information only.  

This report highlights some short comings in the currently implemented solution within Chrome and how it can be used to deceive a user into submitting personal and credit card information under the pretences of auto populating a limited information set relating to their name, surname and email address.

**VERSION**  

Chrome Version: Version 67.0.3396.99 (Official Build) (64-bit) + stable  

Operating System: Mac OSX 10.13.3

**REPRODUCTION CASE**  

Attached form1

## Attachments

- [Google Chrome vulnerability disclosure.pdf](attachments/Google Chrome vulnerability disclosure.pdf) (application/pdf, 835.7 KB)
- [form1.html](attachments/form1.html) (text/plain, 2.8 KB)

## Timeline

### in...@chromium.org (2018-06-29)

mathp@, can you please help to triage or find an owner.

[Monorail components: UI>Browser>Autofill]

### ma...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### se...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### se...@chromium.org (2018-06-29)

Thanks for the report. What I find really surprising is that when the user clicks on the now cc-name field, they see the cc-name without the credit card icon next to it. This seems like a bug, I'm investigating now.

### ca...@gmail.com (2018-07-02)

Cool.

It is really misleading for the average user. For credit card data, I much prefer the Firefox "click to fill each field" method, but it is a trade of on usability.

### se...@chromium.org (2018-07-04)

For sure. I this case we should show more clearly that a credit card field is about to be filled. Working on the fix now, Thanks for reporting.

### bu...@chromium.org (2018-07-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b025e82307a8490501bb030266cd955c391abcb7

commit b025e82307a8490501bb030266cd955c391abcb7
Author: sebsg <sebsg@chromium.org>
Date: Mon Jul 09 15:29:17 2018

[AF] Don't simplify/dedupe suggestions for (partially) filled sections.

Since Autofill does not fill field by field anymore, this simplifying
and deduping of suggestions is not useful anymore.

Bug: 858820
Cq-Include-Trybots: luci.chromium.try:ios-simulator-full-configs;master.tryserver.chromium.mac:ios-simulator-cronet
Change-Id: I36f7cfe425a0bdbf5ba7503a3d96773b405cc19b
Reviewed-on: https://chromium-review.googlesource.com/1128255
Reviewed-by: Roger McFarlane <rogerm@chromium.org>
Commit-Queue: Sebastien Seguin-Gagnon <sebsg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#573315}
[modify] https://crrev.com/b025e82307a8490501bb030266cd955c391abcb7/components/autofill/core/browser/autofill_manager.cc
[modify] https://crrev.com/b025e82307a8490501bb030266cd955c391abcb7/components/autofill/core/browser/autofill_manager.h
[modify] https://crrev.com/b025e82307a8490501bb030266cd955c391abcb7/components/autofill/core/browser/autofill_manager_unittest.cc
[modify] https://crrev.com/b025e82307a8490501bb030266cd955c391abcb7/components/autofill/core/browser/autofill_metrics_unittest.cc


### se...@chromium.org (2018-07-09)

This should make it more obvious that we are now filling a credit card.

### ca...@gmail.com (2018-07-10)

Cool, any idea when this update will make it into a final / test release so I can check it?

Also, is this kind of issue  eligible for the bug bounty / hall of fame?

### se...@chromium.org (2018-07-10)

It should be in the most recent Canary cut. Look at the version number and if it's 69.0.3487.0 the fix should be in it.

I think the whole bounty thing kicks off when the bug is fixed, but I don't know much about that. I'll check how it works otherwise.

I'll wait for you to confirm the fix as well before marking as fixed.

Thanks!

### ca...@gmail.com (2018-07-10)

Excellent, I have a canary build I will update tomorrow and validate.

Do I have to mark as fixed? If so, can you let me know how?

Appreciate it.

### se...@chromium.org (2018-07-10)

I don't know if you can, so just let me know when you have tested, I can flip the state of the bug easily.

### es...@chromium.org (2018-07-10)

Setting OS labels; please correct if they're wrong.

### ca...@gmail.com (2018-07-11)

Hi,

Checked the latest canary build. the new fix looks good. pretty obvious from a UI perspective and then it pops up with the CVC check to share credit card details as well.

Nice!

### se...@chromium.org (2018-07-11)

Thanks! The CVC check only happens for one type of card though, if the user has decided to keep a local copy of it, we won't ask for it. The rest of the UI should remain the same though.

Thanks again for filing the bug.

### se...@chromium.org (2018-07-11)

+ awhalley@chromium.org for the reward process.

### aw...@google.com (2018-07-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-11)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-07-13)

[Empty comment from Monorail migration]

### ca...@gmail.com (2018-07-22)

Hi,

Just checking, is there anything else I am supposed to do one this? I see it is still tagged restrict-view.

Regards,
Cailan

### aw...@google.com (2018-07-23)

Hi cailan.sacks@ - I don't believe so. It'll be automatically opened up to the public 14 weeks after it's marked fixed (October 17th). We're also a little behind on brining bugs to the VRP panel, but expect an update within a couple of weeks.

### aw...@google.com (2018-07-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-07-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-07-30)

Thanks for the report cailan.sacks@! The VRP panel decided to award $1,000 for this report. A member of our finance team will be in touch to arrange payment. Also, how would you like to appear in Chrome release notes?

### aw...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### ca...@gmail.com (2018-07-31)

Hi,

Thanks, much appreciated!

Not sure if I properly understand what you mean by "how would you like to appear...", but the Google profile associated with cailan.sacks@gmail.com would be fine for appearance in the release notes.

Groovy,
C

### sh...@chromium.org (2018-08-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-08-03)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### se...@chromium.org (2018-08-03)

The fix was landed on M69 before the branch. There is no need to merge.

### ca...@gmail.com (2018-08-12)

Hi,

I have not been contacted by anyone in the finance team.

Also, just checking, will cailan.sacks@gmail.con be in the credits for the bug release?

Regards,
C

### aw...@google.com (2018-08-13)

Hello - sorry about that, I've just followed up with the team in question.  I currently have your credit down as just "Cailan Sacks" - let me know if you'd like that changed.

### ca...@gmail.com (2018-08-13)

Cool, thanks. All sorted

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/858820?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091813)*
