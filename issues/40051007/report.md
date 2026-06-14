# Security: Autocomplete preview text leak #4: using ::first-line pseudo-element

| Field | Value |
|-------|-------|
| **Issue ID** | [40051007](https://issues.chromium.org/issues/40051007) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2019-12-17 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

Previously, I reported <https://bugs.chromium.org/p/chromium/issues/detail?id=916838>, a flaw in how autocomplete preview text is handled that allows stored autocomplete data to be leaked from the user's browser to a malicious webpage. The attack depended on changing the font-family of the textarea and observing the impact on its scrollWidth property, then using this to infer the exact sequence of characters present in the textarea.

The specific exploit was patched by making the user agent stylesheet specify a font-family with !important for textarea preview text, thus preventing it from being overridden.

However, the exploit can be trivially made to work again by simply modifying the font-family of the ::first-line pseudo-element of the textarea instead of the textarea itself. This is demonstrated below.

COMMENTARY

This is now the fourth variant of this exploit I've reported (see previous reports at <https://bugs.chromium.org/p/chromium/issues/detail?id=916838>, <https://bugs.chromium.org/p/chromium/issues/detail?id=951487>, <https://bugs.chromium.org/p/chromium/issues/detail?id=1013882>), and I have a fifth variant as well that I'll file shortly afterwards. I don't know what my next trick will be if these latest two are patched, but I would be willing to bet that I will find one if these are patched via the same tactic of simply blocking me from setting a particular blacklist of CSS properties and selectors. Something more is needed to fix this hole for good.

To repeat a suggestion I've made previously: the scrollWidth property of a textarea should be made to simply not reflect any preview text within it. For instance, it could always return 0 (or some more programmer-friendly value, like what the width would be if it were empty) if accessed while preview text is being displayed. This would instantly kill all the attacks I've proposed so far, since they all ultimately rely on being able to read .scrollWidth to get information about the textarea's content. (There MAY be side channels usable for this attack that don't depend on .scrollWidth, like setting the font-family to a font with expensive-to-render ligatures and somehow measuring the time cost of rendering the preview text in that font. But fixing the .scrollWidth leak still seems useful!)

**VERSION**  

Chrome Version: 79.0.3945.88 beta  

Operating System: macOS 10.14.6

**REPRODUCTION CASE**  

Host the attached HTML file on a webserver with a valid SSL certificate.

Access the page over HTTPS, from an installation of Google Chrome that has at least one credit card number saved in the autocomplete system.

Press the up or down arrow key.

The card number will appear in an alert, demonstrating that it has been successfully read by JavaScript (and could therefore now be trivially sent to an external server).

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Mark Amery

## Attachments

- [demo.html](attachments/demo.html) (text/plain, 4.3 KB)

## Timeline

### wf...@chromium.org (2019-12-18)

hi battre@chromium.org here is another issue related to https://crbug.com/chromium/951487 - can you take a look, please? Also see https://crbug.com/chromium/1035063.

[Monorail components: UI>Browser>Autofill]

### ba...@chromium.org (2019-12-18)

I fully agree with the statement that we should mock out scrollWidth. Koji, I am OOO for two weeks and so is most of my team. Is this something you could look into?

### ba...@chromium.org (2019-12-18)

Submitted https://chromium-review.googlesource.com/c/chromium/src/+/1972849 for review.

### sh...@chromium.org (2019-12-18)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/39f06061af8da287363cba093071ec348ef642c2

commit 39f06061af8da287363cba093071ec348ef642c2
Author: Dominic Battre <battre@chromium.org>
Date: Thu Dec 19 04:05:13 2019

Override scroll{Width,Height} in suggest state

We have added

  input::-internal-input-suggested,
  textarea::-internal-input-suggested {
      font: -webkit-small-control !important;
  }

to html.css to prevent that the scrollWidth/scrollHeight attributes of
an input element disclose information about autofill content that is in
suggest (preview) state.

This CL mocks out the scrollWidth/scrollHeight values in preview state
and may allow us to disable the font overriding again.

Bug: 1035058
Change-Id: I36a4a3498c240e15c7d72de1746f9697bb875e9e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1972849
Commit-Queue: Koji Ishii <kojii@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Commit-Position: refs/heads/master@{#726255}

[modify] https://crrev.com/39f06061af8da287363cba093071ec348ef642c2/third_party/blink/renderer/core/html/resources/html.css
[modify] https://crrev.com/39f06061af8da287363cba093071ec348ef642c2/third_party/blink/renderer/core/layout/layout_text_control_multi_line.cc
[modify] https://crrev.com/39f06061af8da287363cba093071ec348ef642c2/third_party/blink/renderer/core/layout/layout_text_control_multi_line.h
[modify] https://crrev.com/39f06061af8da287363cba093071ec348ef642c2/third_party/blink/renderer/core/layout/layout_text_control_single_line.cc
[add] https://crrev.com/39f06061af8da287363cba093071ec348ef642c2/third_party/blink/web_tests/fast/forms/text/input-appearance-scroll-size-mocked.html
[modify] https://crrev.com/39f06061af8da287363cba093071ec348ef642c2/third_party/blink/web_tests/fast/forms/text/input-appearance-scroll-size.html


### sh...@chromium.org (2020-01-01)

battre: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2020-01-02)

 markrobertamery@ Could you please verify that this fixes crbug.com/1035063 (which I could not verify) and this bug? This should have landed in any Chrome >81.0.4002.0, i.e. in any Chrome Canary, but not on Dev Channel, yet.

### ma...@gmail.com (2020-01-03)

Yep, I can confirm this fixes both this bug and https://bugs.chromium.org/p/chromium/issues/detail?id=1035063.

### ba...@chromium.org (2020-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-03)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2020-01-03)

1. Given that this a security issue, I think that it meets the guidelines.
2. https://chromium-review.googlesource.com/c/chromium/src/+/1972849
3. Yes, as per https://crbug.com/chromium/1035058#c8 and my own experiments
4. Bug allows to reveal credit card data in while the form is in preview mode
5. No
6. n/a

### ma...@gmail.com (2020-01-03)

I just discovered that somebody has independently discovered that ::first-line can be used to bypass these styling restrictions and posted about it at https://stackoverflow.com/a/59448852/1709587, five days after I reported this issue. It looks to me like that poster didn't recognise that what they were posting was a security vulnerability and just innocently wanted to provide a workaround to help people style their forms properly. Nonetheless, to anyone reading that post who is aware that the styling restrictions exist for security reasons in the first place, the security implications of the workaround will be clear.

### sh...@chromium.org (2020-01-03)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-01-03)

merge approved for M80 , branch:3987

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7a9e7a968aa77eae1410b40dbddd8b0dab44406a

commit 7a9e7a968aa77eae1410b40dbddd8b0dab44406a
Author: Dominic Battre <battre@chromium.org>
Date: Fri Jan 03 20:01:10 2020

Override scroll{Width,Height} in suggest state

We have added

  input::-internal-input-suggested,
  textarea::-internal-input-suggested {
      font: -webkit-small-control !important;
  }

to html.css to prevent that the scrollWidth/scrollHeight attributes of
an input element disclose information about autofill content that is in
suggest (preview) state.

This CL mocks out the scrollWidth/scrollHeight values in preview state
and may allow us to disable the font overriding again.

TBR=kojii@chromium.org
(cherry picked from commit 39f06061af8da287363cba093071ec348ef642c2)

Bug: 1035058
Change-Id: I36a4a3498c240e15c7d72de1746f9697bb875e9e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1972849
Commit-Queue: Koji Ishii <kojii@chromium.org>
Reviewed-by: Koji Ishii <kojii@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#726255}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1986791
Commit-Queue: Dominic Battré <battre@chromium.org>
Reviewed-by: Dominic Battré <battre@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#396}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/7a9e7a968aa77eae1410b40dbddd8b0dab44406a/third_party/blink/renderer/core/html/resources/html.css
[modify] https://crrev.com/7a9e7a968aa77eae1410b40dbddd8b0dab44406a/third_party/blink/renderer/core/layout/layout_text_control_multi_line.cc
[modify] https://crrev.com/7a9e7a968aa77eae1410b40dbddd8b0dab44406a/third_party/blink/renderer/core/layout/layout_text_control_multi_line.h
[modify] https://crrev.com/7a9e7a968aa77eae1410b40dbddd8b0dab44406a/third_party/blink/renderer/core/layout/layout_text_control_single_line.cc
[add] https://crrev.com/7a9e7a968aa77eae1410b40dbddd8b0dab44406a/third_party/blink/web_tests/fast/forms/text/input-appearance-scroll-size-mocked.html
[modify] https://crrev.com/7a9e7a968aa77eae1410b40dbddd8b0dab44406a/third_party/blink/web_tests/fast/forms/text/input-appearance-scroll-size.html


### sh...@chromium.org (2020-01-04)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-06)

[Empty comment from Monorail migration]

### ba...@chromium.org (2020-01-07)

Natasha, could you please assess whether you want me to merge this to M79.

### na...@google.com (2020-01-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-09)

Congrats! The Panel decided to reward $5,000 for this report!

Would you like to donate this reward?

### na...@google.com (2020-01-10)

[Empty comment from Monorail migration]

### ba...@chromium.org (2020-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-03)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1035058?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1035063]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051007)*
