# Security: Incorrect Security UI in link preview

| Field | Value |
|-------|-------|
| **Issue ID** | [40056009](https://issues.chromium.org/issues/40056009) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile>PreviewTab |
| **Platforms** | Android |
| **Reporter** | zy...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2021-05-26 |
| **Bounty** | $1,000.00 |

## Description

Steps to reproduce the problem:
1.visit poc.html
```
<!DOCTYPE html>
<html>
  <body>
      <h1>
    <a href="data:                                                                      thisisaveryveryveryveryveryveryveryveryverylongstring.google.com/,trust me">Long press to preview Google</a>
</h1>
  </body>
</html>
```
2.long press that link and then click preview link
3.page spoof

What is the expected behavior?
domain show as "data:xxxxxx"

What went wrong?
domain show as "longstring.google.com/,"

Did this work before? N/A 

Chrome version: 93.0.4520.000  Channel: canary
OS Version: 11
Flash Version:

## Attachments

- [preview_poc.jpg](attachments/preview_poc.jpg) (image/jpeg, 1.4 MB)
- [poc_preview.html](attachments/poc_preview.html) (text/plain, 263 B)
- [poc.html](attachments/poc.html) (text/plain, 198 B)
- [screen-20220310-111933.mp4](attachments/screen-20220310-111933.mp4) (video/mp4, 7.9 MB)
- [test.html](attachments/test.html) (text/plain, 379 B)
- [screen-20221208-112407.mov](attachments/screen-20221208-112407.mov) (video/quicktime, 4.9 MB)

## Timeline

### zy...@gmail.com (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-26)

Reproduced on Chrome 91.0.4472.77. 

This might be a duplicate of https://crbug.com/chromium/1048387.

Severity guidelines say that a URL spoof "where only certain URLs can be displayed, or with other mitigating factors" is medium.

[Monorail components: UI>Browser>Mobile>PreviewTab]

### [Deleted User] (2021-05-27)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2021-05-31)

The domain is showed as "data:...google.com/," but got truncated due to the limited space in the text view.

### ad...@google.com (2021-06-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-15)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-06-23)

Let's target M94 for this.

I'm not sure I understand what's happening here. Is the href invalid, or just a "data:" which does not get validated?

Offhand I don't have a plan for a fix for this, so if anyone has an idea let us know.

### [Deleted User] (2021-06-29)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### zy...@gmail.com (2021-10-19)

Hi, how is the situation on this issue?

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### zy...@gmail.com (2021-11-24)

Any update here?

### [Deleted User] (2021-12-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2022-03-07)

Jinsuk, since this is assigned to you and https://crbug.com/chromium/1222155 just got closed as wontfix, can you take a look to see if they are related or a duplicate, so we can adjust priority, close, or take appropriate action?

### zy...@gmail.com (2022-03-10)

of course, they are not the same question, please see this video, preview tab has a incorrectly method to show the domain in ominibox.

### zy...@gmail.com (2022-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-25)

This issue has not been updated for 60 or more days - lowering its priority to P2.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### zy...@gmail.com (2022-11-09)

[Comment Deleted]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### zy...@gmail.com (2022-12-06)

Anyone can track this issue, it's been a year and a half.

### do...@chromium.org (2022-12-07)

+twellington for visibility. 

I wonder if there is any upcoming fixit that we could use to carve out time to address this. 

IIRC the biggest issue is settling on a design, but I don't see that discussion here, or in the possible duplicate listed in https://crbug.com/chromium/1213445#c3 so I think there's yet another duplicate that did discuss this but failed to propose a workable improvement. Can we get help from someone on the Security team for triage? zyzengstorm@ can you help with that? Since visibility is limited for security bugs it might be hard to simply collect all the duplicates!

### tw...@chromium.org (2022-12-07)

I thought we already had guidance on how to properly elide URLs for security + some helper classes used in e.g. page info.  This CL actually just moved ElidedUrlTextView to a more accessible place: https://chromium-review.googlesource.com/c/chromium/src/+/4064126

What's the current logic for URL display in the preview tab toolbar?

### ji...@chromium.org (2022-12-07)

Uses org.chromium.components.url_formatter.UrlFormatter:  https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/compositor/bottombar/ephemeraltab/EphemeralTabSheetContent.java;l=207

Thanks for the pointer. Let me check if the ElidedUrlTextView can mitigate the reported issue.

### zy...@gmail.com (2022-12-07)

Thanks for tracking and analyzing this issue, since it was a issue reported about 1 year ago, I would check it again today, please wait a moment.

### zy...@gmail.com (2022-12-08)

I could reproduce this in M108 on android. I also write a new PoC to illustrate the root cause was that domain is wrongly displayed from right-to-left ,instead left-to-right.

Please check it.

### zy...@gmail.com (2022-12-08)

the video: https://drive.google.com/file/d/1HljY299Pi1SxnyViTyOWmYnGjWscP33P/view?usp=share_link

### do...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### zy...@gmail.com (2023-01-10)

Happy New year and Any updates here?

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### zy...@gmail.com (2023-02-17)

Any updates here, it has been submitted for almost 2 years.

### zy...@gmail.com (2023-02-28)

Attach the video of https://crbug.com/chromium/1213445#c47

### zy...@gmail.com (2023-03-24)

hi, any update here?

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### zy...@gmail.com (2023-05-09)

Hello, @jinsukkim! I was wondering if there have been any updates on this issue?

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### sr...@google.com (2023-12-04)

[Empty comment from Monorail migration]

### zy...@gmail.com (2023-12-05)

Are there any updates?

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

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

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1213445?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1507667]
[Monorail components added to Component Tags custom field.]

### zy...@gmail.com (2024-03-21)

This vulnerability has not been updated for 3 year! Is there any new progress?

### pe...@google.com (2024-10-26)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 688 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

jinsukkim: Uh oh! This issue still open and hasn't been updated in the last 703 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ar...@chromium.org (2024-12-13)

**(Secondary security shepherd)**

Hi can reproduce. The previous shows:
...ongstring.google.com/,strust me.

[jinsukkim@chromium.org](mailto:jinsukkim@chromium.org): Could you please post an update about this bug? Are you going to fix it?

(I am going to ping on chat as well)

### zy...@gmail.com (2025-04-01)

Any updates on this? Although it's an S2 severity issue, it's been nearly 4 years since it was reported.

### ji...@chromium.org (2025-04-28)

Unfortunately the suggestion in [#comment44](https://issues.chromium.org/issues/40056009#comment44) (ElidedUrlTextView) doesn't help. The class attempts its best to show the given URL's origin, but data: URL origin isn't defined. GURL, the go-to URL handler returns an empty string for data: scheme URI. This seems to be [the expected result](https://source.chromium.org/chromium/chromium/src/+/main:url/android/javatests/src/org/chromium/url/GURLJavaTest.java;l=135;drc=b35b169c63a97963e7bfa22c62a0acd007a027a2) of URLs of similar formats.

Possible approaches may be:

1. Enhance ElideUrlTextView to handle data: URLs to return a string that preserves the scheme. The expected string in this case "data: (many spaces) thisisaverylong....google.com/,trustme" would be something like "data:...google.com/"
2. Just do not allow data: URL in preview tab. CCT is [already doing it](https://chromium-review.googlesource.com/6184388).

### tw...@chromium.org (2025-04-28)

#2 seems reasonable to me

### ji...@chromium.org (2025-04-28)

Thanks! #2 will also address similar hacks like [b/371840039](https://issues.chromium.org/issues/371840039).

### ji...@chromium.org (2025-05-02)

Fixed by <https://chromium-review.googlesource.com/c/chromium/src/+/6495694>

### ch...@google.com (2025-05-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-05-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-08-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056009)*
