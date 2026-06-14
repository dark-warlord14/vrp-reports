# Security: tel: protocal spoofing 2

| Field | Value |
|-------|-------|
| **Issue ID** | [40051228](https://issues.chromium.org/issues/40051228) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ti...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2020-01-14 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The bubble will display the initiating origin if it is different from the current top level content.(<https://bugs.chromium.org/p/chromium/issues/detail?id=1036832#c6>)  

However if the "sandbox" property in the iframe element, the bubble will not display the initiating origin.  

This will cause a tel: protocal spoofing.

This maybe effects other bubble, I don't test other bubbles.

**VERSION**  

Chrome Version: Version 81.0.4021.2 (Official Build) dev (64-bit)  

Operating System: Windows10 Pro 1909

**REPRODUCTION CASE**

1. put poc.html and iframe.html in a different domain. Such as xxx.com/poc.html zzz.com/iframe.html
2. set the iframe.src as zzz.com/iframe.html
3. open the xxx.com/poc.html
4. click "ClickMe" to watch the different bubble.

Expect:  

The two bubbles are the same.

In fact:  

If the iframe element has a sandbox property, the bubble doesn't display the initiating origin.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 161 B)
- [iframe.html](attachments/iframe.html) (text/plain, 40 B)
- [nosandbox.jpg](attachments/nosandbox.jpg) (image/jpeg, 53.2 KB)
- [sandbox.jpg](attachments/sandbox.jpg) (image/jpeg, 51.8 KB)
- [test.jpg](attachments/test.jpg) (image/jpeg, 42.8 KB)

## Timeline

### ct...@chromium.org (2020-01-15)

knollr@ can you take a look at this report as well? The cross-origin initiated dialog definitely should include the hostname (it looks like wherever the dialog is getting this URL has it set to empty when it comes from a sandboxed iframe, but I'm not sure what code that is so I don't know why).

Reporter: Have you tested this against other versions as well, or does this only reproduce against M-81 / Canary?

[Monorail components: UI>Browser>Sharing]

### sh...@chromium.org (2020-01-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@gmail.com (2020-01-18)

When open an external protocol in the iframe with 'sandbox' property , it will not display the origin.It only displays "A website wants to open this application."
I think this issue will affect all the version(M79/M80/M81)


### kn...@chromium.org (2020-01-18)

Thanks for the report!
Seems like we're passing the initiating origin from [1]. That value is used for the Click to Call dialog shown in the first screenshots, but also for the general external protocol dialog shown in https://crbug.com/chromium/1041749#c3. Assigning to Emily who added this initially in [2].

@Emily: do you know how we can get the real origin if an iframe is marked as sandboxed? I don't know how that works / where to get the value from.

[1]: https://cs.chromium.org/chromium/src/content/browser/loader/navigation_url_loader_impl.cc?l=717&rcl=3d5dce1be8248e1155ac994d5da0ad315fbdfb5f
[2]: https://chromium-review.googlesource.com/c/chromium/src/+/1829932

### sh...@chromium.org (2020-01-28)

estark: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2020-01-28)

Hmm, this is tricky. I wouldn't expect that we'd be able to get to the origin that created the sandboxed frame, and I'm not sure it would make sense to show it; after all, the real origin is an opaque origin. Since we can't expect users to reason about opaque origins, I'd really prefer to solve this by removing external protocol navigations for non-understandable origins, of which sandboxed frames would be one example. Therefore, I'll mark this as blocked on https://crbug.com/chromium/1011429.

I'm relabeling this as Security_Impact-Stable. This isn't really a recent regression; we used to not show the origin for any request at all, so I wouldn't call this a regression.

### [Deleted User] (2020-02-14)

estark: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-15)

estark: Uh oh! This issue still open and hasn't been updated in the last 17 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-16)

estark: Uh oh! This issue still open and hasn't been updated in the last 18 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-17)

estark: Uh oh! This issue still open and hasn't been updated in the last 19 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-18)

estark: Uh oh! This issue still open and hasn't been updated in the last 20 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2020-02-18)

I recently learned that there is a concept called "precursor origin" that might be useful here, so I'll take a look at whether that'll work as a stopgap fix until we dive into https://crbug.com/chromium/1011429. Should be able to take a look this afternoon.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7cfe6fc556524635d4ac71362dd968e0d0dc7659

commit 7cfe6fc556524635d4ac71362dd968e0d0dc7659
Author: Emily Stark <estark@google.com>
Date: Wed Feb 19 05:19:01 2020

Display precursor origins when applicable in external protocol dialog

External protocol dialogs display the origin that initiated the
external protocol request. The initiating origin helps the user
attribute the request to a particular site, so that they can decide if
they can trust that site to launch an external application. When the
initiating origin was opaque (such as from a sandboxed iframe), the
dialog would display no origin or a generic message, so the user
didn't have any information for making a trust decision. This CL
converts the initiating origin to its precursor origin (the origin
that created the initiating origin) when creating the external
protocol dialog. Displaying the precursor origin gives the user more
useful information for making a trust decision.

Bug: 1041749
Change-Id: I0b21d20e13d7d71db361746dbb18df8d980339bd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2063420
Commit-Queue: Emily Stark <estark@chromium.org>
Reviewed-by: Mustafa Emre Acer <meacer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#742492}

[modify] https://crrev.com/7cfe6fc556524635d4ac71362dd968e0d0dc7659/chrome/browser/external_protocol/external_protocol_handler.cc
[modify] https://crrev.com/7cfe6fc556524635d4ac71362dd968e0d0dc7659/chrome/browser/external_protocol/external_protocol_handler.h
[modify] https://crrev.com/7cfe6fc556524635d4ac71362dd968e0d0dc7659/chrome/browser/external_protocol/external_protocol_handler_unittest.cc


### es...@chromium.org (2020-02-19)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-19)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-24)

[Empty comment from Monorail migration]

### ti...@gmail.com (2020-02-26)

PS:  https://crbug.com/chromium/1036832  +  https://crbug.com/chromium/1041749  maybe a better attacker

### na...@google.com (2020-02-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-27)

Congrats the Panel decided to award $500 for this report!

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-04-15)

 Hello! We consider all attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### is...@google.com (2021-04-15)

This issue was migrated from crbug.com/chromium/1041749?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1011429]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051228)*
