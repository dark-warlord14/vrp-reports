# Security: Visually-perfect domain spoofing using dotless-i plus combining mark

| Field | Value |
|-------|-------|
| **Issue ID** | [40089312](https://issues.chromium.org/issues/40089312) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox, UI>Internationalization |
| **Platforms** | Mac, Windows |
| **Reporter** | jf...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-10-15 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS

Any domain name that includes an accented letter "i" (such as ï or î) can be trivially spoofed using the Unicode dotless-i character "ı" followed by a combining mark, which will be visually indistinguishable from the "normal" accented letter.

(This is similar to other recently-addressed spoofing risks such as diacritics that might easily be overlooked -- e.g. U+0307 on i/j/l. In such cases, however, the spoof depends on the system having poor font support that fails to render the accent in a visible position, and/or user carelessness in overlooking a small yet correctly-rendered mark. This case is in my opinion more serious, in that it provides a visually "perfect" spoof, given good font support.)

VERSION

Chrome Version: Version 61.0.3163.100 (Official Build) (64-bit)
Operating System: macOS 10.12.1

REPRODUCTION CASE

Example URLs:

http://xn--nave-6pa.com (http://naïve.com, using U+00EF "i with dieresis") can be spoofed by http://xn--nave-mza04z.com (http://naı̈ve.com, where "ı̈" is the sequence U+0131 "dotless i", U+0308 "combining dieresis").

Similarly, xn--dner-0pa.com (dîner.com) vs xn--dner-lza40z.com (dı̂ner.com), and likewise for any domain name that includes an accented "i".


This category of spoof is an inherent problem in Unicode, because accented "i" forms are equivalent to the dotted letter "i" (U+0069) with a combining mark; the dotless "ı" (U+0131) is a separate letter with no canonical equivalence to "i", yet when a combining mark is added, it becomes visually indistinguishable.

These spoofs will therefore succeed on any system with reasonably complete font support for the combining marks in the URL bar. This applies to current versions of both Windows and macOS, at least, and likely to other systems as well.

To resolve this issue, I believe any domain name that includes dotless-i followed by a combining mark above should be displayed as punycode in the browser's URL bar, instead of its Unicode IDN form.

## Timeline

### el...@chromium.org (2017-10-15)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Omnibox UI>Internationalization]

### wf...@chromium.org (2017-10-16)

jshin I wonder if you could take a look at this bug?

[Monorail components: UI>Security>UrlFormatting]

### js...@chromium.org (2017-10-17)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-10-17)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-10-17)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-10-17)

See also https://crbug.com/chromium/727092 

### jf...@gmail.com (2017-10-17)

I'm not able to see the issues (https://crbug.com/chromium/750239 or https://crbug.com/chromium/727092) mentioned above, but AFAICT the change that was applied in https://chromium-review.googlesource.com/c/chromium/src/+/709919 and references https://crbug.com/chromium/750239 is only addressing the use of U+0307 COMBINING DOT ABOVE to spoof a plain letter "i". It did not resolve the issue for accented letters; a sequence like U+0131,U+0308 can still be used to spoof the letter ï (i-dieresis, U+00EF).

### sh...@chromium.org (2017-10-17)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-11-13)

> It did not resolve the issue for accented letters; a sequence like U+0131,U+0308

Which is why I de-duped this bug from https://crbug.com/chromium/750239. The crbug.com UI is confusing/misleading in that de-duping does not drop 'Merged' field while status is changed back to Assigned/Unconfirmed/Untriaged, etc. 

I'll block dotless-i from being followed by a combining mark for now. 




### js...@chromium.org (2017-11-14)

BTW, compared with https://crbug.com/chromium/750239, this one will affect far fewer number of domains (for now) because this is a spoofing against IDN domains. 

A CL is up at https://chromium-review.googlesource.com/c/chromium/src/+/767888 . 

This is a sub-issue of https://crbug.com/chromium/727092. 



### bu...@chromium.org (2017-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a30f64b4ae13255535a4947616fce484c54207df

commit a30f64b4ae13255535a4947616fce484c54207df
Author: Jungshik Shin <jshin@chromium.org>
Date: Fri Nov 17 23:34:48 2017

Block dotless-i / j + a combining mark

U+0131 (doltess i) and U+0237 (dotless j) are blocked from being
followed by a combining mark in U+0300 block.

Bug: 774842
Test: See the bug
Change-Id: I92aac0e97233184864d060fd0f137a90b042c679
Reviewed-on: https://chromium-review.googlesource.com/767888
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/master@{#517605}
[modify] https://crrev.com/a30f64b4ae13255535a4947616fce484c54207df/components/url_formatter/idn_spoof_checker.cc
[modify] https://crrev.com/a30f64b4ae13255535a4947616fce484c54207df/components/url_formatter/url_formatter_unittest.cc


### js...@chromium.org (2017-11-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-19)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-01)

Nice one! The Chrome VRP panel decided to award $500 for this report. A member of our finance team will be in touch to arrange for payment. Also, how would you like to be credited in our release notes?

### jf...@gmail.com (2017-12-01)

Thanks, much appreciated!

FYI regarding disclosure, the Firefox equivalent of this issue was reported to Mozilla at the same time as the Chromium report here (October 15th); it was fixed in the recent Firefox 57 release, though as of now the bug report has not yet been made public.

As for release notes, I'm not sure what kind of details you need... I'm "Jonathan Kew <jfkthame@gmail.com>", or whatever equivalent form you typically present things in.

### aw...@chromium.org (2017-12-01)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-10-19)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-19)

This issue was migrated from crbug.com/chromium/774842?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Internationalization, UI>Security>UrlFormatting]
[Monorail mergedinto: crbug.com/chromium/750239]
[Monorail components added to Component Tags custom field.]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089312)*
