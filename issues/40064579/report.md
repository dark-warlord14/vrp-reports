# Security: Chrome iOS iframe SandBox Download

| Field | Value |
|-------|-------|
| **Issue ID** | [40064579](https://issues.chromium.org/issues/40064579) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ia...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2023-05-15 |
| **Bounty** | $1,000.00 |

## Description

By inspiring an older report, interestingly noted that this vulnerability is affecting Safari iOS (Webkit) which should be taken care by Apple only. Hence reported to them. Report OE194060593136

Seems like Chrome Android is also vulnerable.

As of now Safari don't have this feature but I have reported and hopefully they will implement it.

Detail report is attached.
As chrome is also affected adding the same report here too.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-05-15)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-05-17)

Does this repro for you on Android? It seems to work correctly for me.

What feature are you saying Safari does not support? I think it does have the iframe sandbox attribute.

### ia...@gmail.com (2023-05-18)

@kenrb - Yes its working for me as well on Android with Android OS 13 Security Patch March 2023.

Safari - I doubt that this is something which Chrome may not able to work on iOS. but on Android they will able to look, so I reported this to apple as well.

Chrome team can you confirm please.

### [Deleted User] (2023-05-18)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2023-05-18)

I've tried on a couple of different devices. Chrome Canary and Stable on Android both load the download.txt in the new tab without initiating a download. It initiates a download if I remove the iframe sandbox and try again.

Do you have a video of this reproducing on Android?

### ke...@chromium.org (2023-05-18)

Actually I will change this to an iOS only bug to track the issue on the Chrome side. Do you have the radar number for the report you filed with Apple?

If you can provide a video for Android demonstrating this problem, please file another bug with that and detailed repro instructions.

ajuma@: This is a low severity security issue, I don't know if there is anything to do on your side.

[Monorail components: Mobile>iOSWeb>Security]

### [Deleted User] (2023-05-18)

[Empty comment from Monorail migration]

### aj...@chromium.org (2023-05-19)

Not much we can do on our side -- the concept of sandboxed iframes is entirely within WebKit, so we don't find out whether a download is coming from sandboxed or non-sandboxed frame.

### [Deleted User] (2023-05-19)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-05-21)

Yes, Reported to Apple today only and here is the report number OE1940801785616

### ia...@gmail.com (2023-05-21)

is it possible to add some one from Apple Team here just to keep a track of the bug?

### aj...@chromium.org (2023-05-23)

> is it possible to add some one from Apple Team here just to keep a track of the bug?

The typical workflow is to report to Apple and then let them track the bug in their own bug tracking system. To have a more interactive way of reporting WebKit bugs (where you can get direct responses from the Apple WebKit team) consider filing WebKit security bugs at https://bugs.webkit.org/enter_bug.cgi?product=Security .

### ia...@gmail.com (2023-05-27)

Can we add ddkil...@apple.com in this report?

### aj...@chromium.org (2023-05-29)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-06-26)

Just an update that, Apple will publish in fix in Fall 2023.

### aj...@chromium.org (2023-06-26)

Thanks for the update!

### aj...@chromium.org (2023-09-26)

Fixed in iOS 17.

### [Deleted User] (2023-09-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-05)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report. Thank you for reporting this issue to us and WebKit! 

### am...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-03)

This issue was migrated from crbug.com/chromium/1445712?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064579)*
