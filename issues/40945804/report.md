# Security: iOS file picker dialog can be shown over a different tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40945804](https://issues.chromium.org/issues/40945804) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | iOS |
| **Reporter** | ho...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2023-11-25 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to display a file or image picker dialog over a different tab.

Similar bug: <https://bugs.chromium.org/p/chromium/issues/detail?id=1414936>

**VERSION**  

Chrome Version: 119.0.6045.169 + stable  

Operating System: iOS 17.1

**REPRODUCTION CASE**  

0. Host the poc.html

1. Open poc.html
2. Touch the page
3. Select option appears in new tab

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: jubsan fasim

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-11-25)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-27)

[Empty comment from Monorail migration]

### sk...@chromium.org (2023-11-30)

Assigning to iOS navigation (though this may be a file chooser bug - feel free to reassign back if this is the case).

[Monorail components: UI>Browser>Navigation]

### aj...@chromium.org (2023-11-30)

This reproduces in every 3rd-party browser on iOS that I checked (Chrome, Firefox, Edge) but not in Safari. Since WebKit is responsible for displaying this dialog, it needs to either expose an API to let the embedder close the dialog on tab switch, or make this dialog view be a child of the associated WKWebView, so it will naturally appear/disappear as that WKWebView is shown/hidden.

I'll file a WebKit bug.

### aj...@chromium.org (2023-11-30)

Filed https://bugs.webkit.org/show_bug.cgi?id=265602

### [Deleted User] (2023-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-01)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-05)

[Empty comment from Monorail migration]

### ho...@gmail.com (2024-01-02)

Hey,its been a month any updates?

### aj...@chromium.org (2024-01-02)

As noted in https://crbug.com/chromium/1505203#c5, this bug is blocked on Apple fixing https://bugs.webkit.org/show_bug.cgi?id=265602. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1505203?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-04)

ajuma: Uh oh! This issue still open and hasn't been updated in the last 32 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-02-19)

ajuma: Uh oh! This issue still open and hasn't been updated in the last 47 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### aj...@chromium.org (2024-02-19)

This is an ExternalDependency.

### aj...@google.com (2024-05-16)

Fixed in iOS 17.5 by <https://github.com/WebKit/WebKit/commit/a3524e350ec963e6a9a7d30b736b898505cb1a4e>

### ho...@gmail.com (2024-05-17)

Thanks team for fixing the bug. :)

### sp...@google.com (2024-05-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
baseline report of security UI bug -- the reward amount was decided based on the low risk / user impact posed by this issue

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are not already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### am...@chromium.org (2024-05-22)

Thank you for your efforts and reporting this issue to us!

### ho...@gmail.com (2024-05-23)

deleted

### pe...@google.com (2024-08-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline report of security UI bug -- the reward amount was decided based on the low risk / user impact posed by this issue
> 
> Thank you for your efforts and helping us make Chrome more secure for all users!
> 
> Cheers,
> Chrome VRP Panel Bot
> 
> 
> P.S. Two other things we'd like to mention:
> 
> * Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a 

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40945804)*
