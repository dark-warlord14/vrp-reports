# Security:  the autofill prompt appears together with the requesfullscreen, the autofill prompt does not close   it can confuse lead to spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40064688](https://issues.chromium.org/issues/40064688) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | jk...@google.com |
| **Created** | 2023-05-19 |
| **Bounty** | $1,000.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-05-19)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-05-19)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-05-21)

deleted

### sa...@gmail.com (2023-05-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2023-05-22)

Hi mlerman@ I see that you work on Chrome autofill, and would like your input on this bug and how it should be addressed. In the PoC, the autofill form pops up for a split second at the time fullscreen mode. I did not reproduce this on my end. Thanks for your help!

[Monorail components: UI>Browser>Autofill]

### [Deleted User] (2023-05-22)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-05-22)

and if we do it quickly (press arrow down and enter) the auto fill doesn't appear when entering fullscreen mode and it auto fills to the form.

### ha...@google.com (2023-05-23)

Removing OS Chrome label and adding windows since the report mentions windows and it doesn't look like a CrOS specific bug

### ch...@google.com (2023-05-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-03)

mlerman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2023-06-18)

hello any updates?

### [Deleted User] (2023-06-18)

mlerman: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@gmail.com (2023-07-12)

Hello any updates?  

### sa...@gmail.com (2023-08-02)

Hello any updates?

### sa...@gmail.com (2023-08-12)

Helo any updates?

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### ml...@chromium.org (2023-08-18)

The Autofill Popup is clearly visible, and it is displayed on top of the full screen experience. The notification window fades fairly quickly.

Given Autofill has a time-delay requirement (i.e. if the user hits down + enter in very quick successful, Autofill doesn't fill), the user has sufficient opportunity to be aware of the popup and understand that they're interesting with Autofill. So this seems like a non-issue to me.

schwering@, thoughts?


### sa...@gmail.com (2023-08-19)

I do it quickly (press arrow down and enter) the auto fill popup doesn't appear when entering fullscreen mode and the autofill fill the form 

### sa...@gmail.com (2023-08-19)

I do it on comment https://crbug.com/chromium/1447271#c7

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-11-02)

Helo any updates 

### sc...@google.com (2023-11-02)

I generally agree with https://crbug.com/chromium/1447271#c20.

Since Chrome looks very laggy in https://crbug.com/chromium/1447271#c7, I suspect that the Autofill popup is not showing due to the timing issue Jan is working on (I can't find the bug number). Assigning to Jan for confirmation.

### jk...@google.com (2023-11-09)

[Empty comment from Monorail migration]

### jk...@google.com (2023-11-09)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-11-23)

Hello any updates?

### jk...@google.com (2023-11-23)

We are aware of the bug but are currently blocked on fixing the issue that's causing the existing security measures not to work properly.

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### sa...@gmail.com (2023-12-27)

Hello any updates?

### jk...@google.com (2024-01-03)

I believe that I have a fix for the root cause that is blocking this issue (1475902) that is currently in review. There should hopefully be some news in a few weeks.

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

### jk...@google.com (2024-01-23)

Unfortunately, I have tried, but I simply cannot reproduce this locally - the popup is never accepted for me.

In the meantime, I improved our clickjacking protection for another issue. Could you check whether starting the last Chrome Canary (122.0.6260.0 or newer) with the following command line parameter solves the issue for you? --enable-features=AutofillPopupImprovedTimingChecks

Thanks,
Jan

### sa...@gmail.com (2024-01-23)

redacted

### jk...@google.com (2024-01-23)

Thank you for testing so quickly - much appreciated!

Yes, the popup needs to have been shown for at least 500ms before any enter keystrokes are accepted. At this point, I think it's fair to assume that accepting the Autofill popup was intentional. In fact, we have had that requirement for a while - the timing may just have been off in some cases.

The trouble is that I still am not able to verify that the exploit actually worked without the flag. Can you still reproduce the original issue if you leave out the additional command line parameters?

What do you mean by "Is the fix for other bugs affected by this bug"?

Thanks,
Jan

### sa...@gmail.com (2024-01-23)

I have tried it and had to do 2x enter to fill the autofill.
Sorry, what I meant was a fix for another bug so this bug has also is fixed

### is...@google.com (2024-01-23)

This issue was migrated from crbug.com/chromium/1447271?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1475902]
[Monorail mergedwith: crbug.com/chromium/1498815]
[Monorail components added to Component Tags custom field.]

### sa...@gmail.com (2024-03-18)

hello any updates?

### jk...@google.com (2024-03-18)

This is currently rolling out to stable. We're doing it carefully to make sure nothing breaks. We expect it to be on 100% stable in about a month.

### jk...@google.com (2024-05-02)

Hi,

This should now have reached 100% stable on the current stable build. Could you please verify that it is working as expected?

Thanks,
Jan

### sa...@gmail.com (2024-05-02)

deleted

### sa...@gmail.com (2024-07-02)

hello any updates?

### jk...@google.com (2024-07-02)

Can you try again on the latest Canary version?

Apologies for the repeated requests, but I have never been able to reproduce this locally, regardless of OS. As a result, it's very hard to understand whether it can still be reproduced.

Thanks,
Jan

### sa...@gmail.com (2024-07-02)

hi jan 
i tested on  128.0.6571.0 (Official Build) canary (64-bit) there is delay when do enter on mode fullscreen

### jk...@google.com (2024-07-09)

Hi,

I don't see any exploit on the video that you are sharing. Are you saying this is now fixed?
That being said, I don't see an exploit in the initial video, either.

Thanks,
Jan

### jk...@google.com (2024-08-14)

Ping here - could you confirm that this is fixed?

### sa...@gmail.com (2024-08-14)

it seems to be fixed but i don't know what version last time i tried it on version 128.0.6571.0 (Official Build) canary (64-bit). i tried the poc on version 113 and it worked

### sp...@google.com (2024-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
$1,000 thank you for your report, which provided information to confirm a timing change would be helpful making a security-relevant improvement


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-22)

Congratulations Hafiizh! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-11-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $1,000 thank you for your report, which provided information to confirm a timing change would be helpful making a security-relevant improvement

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064688)*
