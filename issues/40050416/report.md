# Security: Autocomplete preview text STILL leaks credit card numbers - attacker can simply override system-ui font

| Field | Value |
|-------|-------|
| **Issue ID** | [40050416](https://issues.chromium.org/issues/40050416) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fonts, UI>Browser>Autofill |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2019-10-12 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

Previously, I reported <https://bugs.chromium.org/p/chromium/issues/detail?id=916838> (now public), which allowed credit card numbers to be leaked through a tactic that, in part, involved changing the font of an <input> element while autocomplete preview text containing a credit card number was being displayed within it, and observing how this affected the element's scrollWidth.

This was fixed by pinning the font-family CSS property of autocomplete preview text to system-ui.

However, after this fix, the font can still be changed by instead adding new @font-face declarations to the page that change the system-ui font itself. This allows the same exploit (or others involving font changes) to be used; all the attacker needs to change is the mechanism of changing the font, which must now be to introduce a new @font-face, instead of changing the font-family property.

As with both my previous security bug reports, this attack only requires the attacker to socially engineer the victim into pressing the up or down arrow key, and gives no indication to the victim that their credit card number has been accessed by the attacking site.

**VERSION**  

Chrome Version: [78.0.3904.50] + [beta]  

Operating System: [macOS Mojave 10.14.6]

**REPRODUCTION CASE**  

Host the attached HTML file on a webserver with a valid SSL certificate.

Access the page over HTTPS, from an installation of Google Chrome that has at least one credit card number saved in the autocomplete system.

Press the up or down arrow key.

The card number will appear in an alert, demonstrating that it has been successfully read by JavaScript (and could therefore now be trivially sent to an external server).

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: [Mark Amery]

## Attachments

- [page2.html](attachments/page2.html) (text/plain, 4.0 KB)
- [not-working.png](attachments/not-working.png) (image/png, 18.8 KB)

## Timeline

### aj...@google.com (2019-10-14)

Thanks for the report. I will confirm on Monday if the component team doesn't beat me to it.

[Monorail components: UI>Browser>Autofill]

### aj...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-14)

[Empty comment from Monorail migration]

### aj...@google.com (2019-10-14)

I cannot currently reproduce this.

On Stable I see a card number of '0...0'. On Canary I do not see an alert.

Could you provide a video of the attack working, or an improved POC?

### aj...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-15)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-10-17)

[Empty comment from Monorail migration]

### ca...@chromium.org (2019-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-27)

rogerm: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@chromium.org (2019-10-28)

[Empty comment from Monorail migration]

### ba...@chromium.org (2019-10-29)

You gotta be kidding me!

Thanks for the report.

### ba...@chromium.org (2019-10-29)

kojii@ WDYT of not allowing a website to override the system-ui font? Would that be an option?

### ro...@chromium.org (2019-10-29)

That was the understanding I came away with after checking with the platform folks: that the system ui was controlled outside of the browser.

 :(

### ko...@chromium.org (2019-10-29)

Tab, do you happen to know if the spec allows author to override `system-ui` and other generic families by @font-face rule?

### ba...@chromium.org (2019-11-01)

[Empty comment from Monorail migration]

### ta...@google.com (2019-11-01)

Per spec, no, you can't override the generic fonts.

You *can* define a @font-face named "serif" or "system-ui" with no problem; that's valid and allowed. But those can only be referenced in font-family by using a string: `font-family: "system-ui";`.

If you use a keyword matching one of the generic families, like `font-family: system-ui;`, it *always* refers to the predefined generic family, with no regards for any user-defined font families. (See <https://drafts.csswg.org/css-fonts-4/#family-name-syntax> for details.)

If we're not following that, and allowing @font-face rules to override the predefined system-ui keyword, then that's a bug on our part.

### ba...@chromium.org (2019-11-01)

kojii@ can you help fixing this?

### ko...@chromium.org (2019-11-02)

Yes, absolutely. Let me talk to a few experts for how to fix this.

### ko...@chromium.org (2019-11-04)

[Empty comment from Monorail migration]

### ko...@chromium.org (2019-11-04)

[Empty comment from Monorail migration]

### fu...@chromium.org (2019-11-04)

Doesn't look we recognize system-ui as a keyword. If this is not an issue for keywords like serif and monospace, the fix should be to add system-ui as a keyword in css_value_keywords.json5 and handle the keyword in the code the same places as other such font family names.


### ko...@chromium.org (2019-11-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>Fonts]

### ko...@chromium.org (2019-11-05)

WIP
https://chromium-review.googlesource.com/c/chromium/src/+/1899637

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cc17930b5e93864e7f56a9d5dbfd3a1d3bee62c7

commit cc17930b5e93864e7f56a9d5dbfd3a1d3bee62c7
Author: Koji Ishii <kojii@chromium.org>
Date: Wed Nov 06 17:25:27 2019

Prevent `system-ui` to match `@font-face`

This patch prevents the `system-ui` font family name to match
fonts defined by `@font-face` rules.

Per spec:
https://drafts.csswg.org/css-fonts-4/#family-name-syntax
All generic family names should not match when not quoted.
Supporting it requires more plumbing from the style system
to the font system, and it is not included in this patch.

Bug: 1013882, 1021568
Change-Id: If1aec2254e3aab41bed207a005b4c981d344d7ca
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1899637
Reviewed-by: Dominik Röttsches <drott@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Xiaocheng Hu <xiaochengh@chromium.org>
Commit-Queue: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#713055}

[modify] https://crrev.com/cc17930b5e93864e7f56a9d5dbfd3a1d3bee62c7/third_party/blink/renderer/core/css/font_face_cache.cc
[add] https://crrev.com/cc17930b5e93864e7f56a9d5dbfd3a1d3bee62c7/third_party/blink/web_tests/external/wpt/css/css-fonts/generic-family-keywords-001.html


### ko...@chromium.org (2019-11-06)

Should be fixed now.

### sh...@chromium.org (2019-11-08)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-18)

Requesting merge to beta M79 because latest trunk commit (713055) appears to be after beta branch point (706915).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-18)

This bug requires manual review: M79's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-11-18)

How is the change looking in canary so far?

+adetaylor@ (Security TPM) for M79 merge review. If merge is approved and merged latest by tomorrow, Tuesday noon, then we can pick it up for this week beta release on Wednesday. 

### ad...@chromium.org (2019-11-18)

As an externally-reported medium it would be great to merge to beta, yes. Assuming we don't expect web compatibility breakage here. Thanks!

### ko...@chromium.org (2019-11-18)

> How is the change looking in canary so far?

We're not seeing any regression nor crash reports on this yet.

> 2. Links to the CLs you are requesting to merge.

https://crbug.com/chromium/1013882#c26
https://chromium-review.googlesource.com/c/chromium/src/+/1899637

> 3. Has the change landed and been verified on master/ToT?

80.0.3962.0

> 4. Why are these changes required in this milestone after branch?

Found after branch.

> 5. Is this a new feature?
> 6. If it is a new feature, is it behind a flag using finch?

No.


### go...@chromium.org (2019-11-18)

Approving merge to M79 branch 3945 based on comments #33 and #34, please merge ASAP. 

### go...@chromium.org (2019-11-18)

Please merge your change to M79 branch 3945 ASAP so we can pick it up for this week Beta release. Thank you.

### go...@chromium.org (2019-11-19)

Please merge your change to M79 branch 3945 by 12:30 PM PT, today so we can pick it up for tomorrow's beta release. Thank you.

### dr...@chromium.org (2019-11-19)

I believe this has been merged in https://chromium-review.googlesource.com/c/chromium/src/+/1921934 - I am not sure why the bot did not mark it as merged.


### go...@chromium.org (2019-11-19)

Adjusting labels per https://crbug.com/chromium/1013882#c38. Thank you.

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats! The Panel decided to reward $5,000  for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1013882?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fonts, UI>Browser>Autofill]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050416)*
