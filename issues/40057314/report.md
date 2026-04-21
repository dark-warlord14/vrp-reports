# Security: URL spoofing using LATIN SMALL LETTER L WITH STROKE

| Field | Value |
|-------|-------|
| **Issue ID** | [40057314](https://issues.chromium.org/issues/40057314) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Security (Use Subcomponent)>UrlFormatting |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2021-09-19 |
| **Bounty** | $500.00 |

## Description

The U+0142 ł LATIN SMALL LETTER L WITH STROKE can be confused with letter "t" in iOS and it should be converted to punnycode 

for eg: 
https://xn--youube-5db.com/



letter with details:

U+0142 ł LATIN SMALL LETTER L WITH STROKE



## Attachments

- [spoofing in iOS.jpeg](attachments/spoofing in iOS.jpeg) (image/jpeg, 42.5 KB)

## Timeline

### [Deleted User] (2021-09-19)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-09-20)

Passing to meacer for further triage as our confusable expert.

meacer: if this is valid can you help further triage and assign a severity? Thanks.

[Monorail components: UI>Browser>LookalikeChecks]

### ca...@chromium.org (2021-09-20)

(added all OSs since the character looks similar everywhere)

### [Deleted User] (2021-09-20)

[Empty comment from Monorail migration]

### me...@google.com (2021-09-20)

This is on the fence, but I think treating it as low severity is a safe option. I also agree that it's not limited to iOS.

The difficulty here is that this character looks both like l and t, but we currently don't have a way of assigning multiple skeletons to characters. So if we map this character to t, then someone will file a bug with gmaił[.]com. I don't think we can do much until we find a solution for https://crbug.com/chromium/843352.

### jd...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

[Monorail components: -UI>Browser>LookalikeChecks UI>Security>UrlFormatting]

### ra...@gmail.com (2021-09-20)

since you cannot assign multiple skeletons to character, to consider more safer option, this character should be more treat like a "t" than "l" because when using this as an "l" people would notice the stroke in it more than it would notice the different b/w this character and "t" - like you can tell from this something us wrong with "l" in gmail because l doesn't have any stroke like "t". Wand then you yourself can file a new bug with the same character to get it on record.

### [Deleted User] (2021-09-21)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2021-09-30)

As I said, visual similarity is pretty subjective and depends on various things like context, fonts, platform etc. For example, if you use the character as googłe[.]com, that also looks very convincing. I'd rather not make a judgement call here, we should fix the underlying issue instead (https://crbug.com/chromium/843352).


### me...@google.com (2022-04-21)

CL at https://chromium-review.googlesource.com/c/chromium/src/+/3598360

### gi...@appspot.gserviceaccount.com (2022-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9b292a093a025d41b429bc8254744834f2eee029

commit 9b292a093a025d41b429bc8254744834f2eee029
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Thu Apr 21 22:17:22 2022

Lookalikes: Compute hostname variants with and without diacritics

Presently, we generate supplemental hostnames from an input hostname
after removing the hostname's diacritics. This allows us to normalize
a hostname so that attackers can't evade lookalike protections by adding
diacritics.

However, some characters in a hostname can become confusable with other
characters when they are added diacritics. For example,  LATIN SMALL
LETTER L normally not confusable with "t", but LATIN SMALL LETTER L WITH
STROKE (ł) is on some fonts and platforms.

The solution for this would be to add a multiple skeleton mapping for ł
so that the generated supplemental hostnames would have both "l" and "t"
variants in them. This currently doesn't work though, because of the
diacritic removal mentioned above, and a hostname like łest[.]com is
passed as lest[.]com to supplemental hostname generation.

This CL runs the supplemental hostname generation over both the
diacritic and non-diacritic versions of the hostname. This allows us to
generate both lest[.]com and test[.]com as supplemental hostnames.

As a result of this change, we'll be able to prevent additional spoofs
that use characters with diacritics that are confusable with other
characters.

Bug: 1250993
Change-Id: I592602281bffd7f75fc97f32280a46ffcf8fd3ed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3598360
Reviewed-by: Joe DeBlasio <jdeblasio@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#994949}

[modify] https://crrev.com/9b292a093a025d41b429bc8254744834f2eee029/components/url_formatter/spoof_checks/idn_spoof_checker_unittest.cc
[modify] https://crrev.com/9b292a093a025d41b429bc8254744834f2eee029/components/url_formatter/spoof_checks/skeleton_generator.cc


### gi...@appspot.gserviceaccount.com (2022-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/52da78dea42c65ad8f056be73a021c8d60c97599

commit 52da78dea42c65ad8f056be73a021c8d60c97599
Author: Mustafa Emre Acer <meacer@chromium.org>
Date: Fri Apr 22 01:51:00 2022

Lookalikes: Optimize supplemental hostname generation for diacritics

crrev.com/c/3598360 added supplemental hostname generation for hostname
with and without removing their diacritics. This effectively doubles the
work we do for supplemental hostname generation.

This CL adds a check to see if there are any characters in the hostname
that have diacritics and map to multiple skeletons. If not, supplemental
hostname generation is only done with the diacritics removed.

Bug: 1250993
Test: Manual
Change-Id: I2234fdfbdd4d5a8bceadb100470b35a93ea57506
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3601256
Reviewed-by: Joe DeBlasio <jdeblasio@chromium.org>
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#995010}

[modify] https://crrev.com/52da78dea42c65ad8f056be73a021c8d60c97599/components/url_formatter/spoof_checks/skeleton_generator.cc
[modify] https://crrev.com/52da78dea42c65ad8f056be73a021c8d60c97599/components/url_formatter/spoof_checks/skeleton_generator.h


### me...@google.com (2022-04-22)

[Empty comment from Monorail migration]

### me...@google.com (2022-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-28)

Thank you for this report! The VRP Panel has decided to award you $500 for this report as a thank you for reporting this issue. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2022-07-29)

This issue was migrated from crbug.com/chromium/1250993?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/843352]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057314)*
