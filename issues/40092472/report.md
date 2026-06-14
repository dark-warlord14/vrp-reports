# Security: IDN URL Spoofing with using "ы"

| Field | Value |
|-------|-------|
| **Issue ID** | [40092472](https://issues.chromium.org/issues/40092472) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Internationalization |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | jd...@chromium.org |
| **Created** | 2018-09-17 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 71.0.3553.2 (Official Build) canary (64-bit)  

Operating System: Mac

**REPRODUCTION CASE**

This "Ы" (U+042B) should be mapped to "bl".

[http://гоыох.com](http://%D0%B3%D0%BE%D1%8B%D0%BE%D1%85.com)  

[http://ыоԍԍег.com](http://%D1%8B%D0%BE%D4%8D%D4%8D%D0%B5%D0%B3.com)

## Timeline

### mb...@chromium.org (2018-09-19)

[Empty comment from Monorail migration]

[Monorail components: UI>Internationalization UI>Security>UrlFormatting]

### sh...@chromium.org (2018-09-19)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-09-25)

Shouldn't be medium severity as https://crbug.com/chromium/773930?

### me...@google.com (2018-10-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-09)

[Empty comment from Monorail migration]

### me...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-10-16)

meacer: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-03)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-01-30)

[Comment Deleted]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### ad...@google.com (2019-05-02)

[Empty comment from Monorail migration]

### ad...@google.com (2019-05-02)

https://crbug.com/chromium/897505 was a duplicate of this, but concerning a different character: ""ю". The concern about fixing these, in both cases, is that a single unicode character may expand to multiple non-unicode characters which is why this needs a bit of thought before fixing.

### dr...@chromium.org (2019-05-31)

Friendly security sheriff ping - any update on this?

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-08-07)

Mustafa, any additional thoughts on how we can fix this? Thanks!

### me...@chromium.org (2019-08-14)

No great ideas I'm afraid. We can try restricting ю and ы to cyrillic TLDs, but I'm not sure of the potential breakage there. It also doesn't solve the issue spoofing for those domains  (гоыох.ru would still work).

### jd...@chromium.org (2019-09-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-09-13)

adetaylor: do you remember anything more about the discussion on this bug? While Mustafa is OOO, I'm trying to better understand why mapping to multiple characters is a problem.

Either it's not actually a problem, or we have another bug, since we map œ to ce and æ/ӕ to ae.

### ad...@chromium.org (2019-09-13)

Sorry, no.

### jd...@chromium.org (2019-09-16)

[Empty comment from Monorail migration]

### me...@chromium.org (2019-09-23)

Mapping ы to bl is not that big of a deal. What's problematic is mapping ы to both ы and bl, i.e. trying both versions when doing skeleton matching. That would explode the number of combinations we need to check. It doesn't look like we need that though, so just a one-to-one mapping works here. https://crbug.com/chromium/835554 does a similar mapping for œ and æ, so I think we can go with that.

(I really thought there was a catch here, but I can't find one)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/11d7f93df8e1ce5dc503179df70477ac7bfd0bf7

commit 11d7f93df8e1ce5dc503179df70477ac7bfd0bf7
Author: Joe DeBlasio <jdeblasio@chromium.org>
Date: Tue Sep 24 23:09:32 2019

Add ы (U+042B) and ԍ (U+050D) to set of Cyrillic look-alikes.

This CL adds ы and ԍ to the set of Cyrillic characters that look like
Latin characters, as well as a test case to verify.

Bug: 884693
Change-Id: I0329b1c2bce2b733463346d69a2bae5d65234085
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1823320
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Commit-Queue: Joe DeBlasio <jdeblasio@chromium.org>
Auto-Submit: Joe DeBlasio <jdeblasio@chromium.org>
Cr-Commit-Position: refs/heads/master@{#699536}

[modify] https://crrev.com/11d7f93df8e1ce5dc503179df70477ac7bfd0bf7/components/url_formatter/spoof_checks/idn_spoof_checker.cc
[modify] https://crrev.com/11d7f93df8e1ce5dc503179df70477ac7bfd0bf7/components/url_formatter/spoof_checks/idn_spoof_checker_unittest.cc


### jd...@chromium.org (2019-09-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-28)

Requesting merge to beta M78 because latest trunk commit (699536) appears to be after beta branch point (693954).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-09-28)

pls confirm the fix is working on canary as intended and it is safe to merge to M78

### jd...@chromium.org (2019-09-30)

This is fine to wait until M79.

### me...@chromium.org (2019-10-02)

Reopening, looks like we missed "ю" character from 897505. We should be able to add it to the same list. Joe, do you want to address that as well?

### jd...@chromium.org (2019-10-02)

Doh. Good catch. I'll take care of it.

### na...@google.com (2019-10-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-04)

Congrats! The Panel decided to reward $500 for this report :) 

### na...@google.com (2019-10-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-11-21)

crrev.com/c/1838476 added ю, and tagged this bug. Bugdroid didn't pick it up, but marking this bug as fixed.

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/884693?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Internationalization, UI>Security>UrlFormatting]
[Monorail mergedwith: crbug.com/chromium/897505]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092472)*
