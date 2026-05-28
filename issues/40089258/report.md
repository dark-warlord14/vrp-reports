# iframe sandbox bypass with SW openWindow()

| Field | Value |
|-------|-------|
| **Issue ID** | [40089258](https://issues.chromium.org/issues/40089258) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Blink>ServiceWorker |
| **Platforms** | Mac |
| **Reporter** | s....@gmail.com |
| **Assignee** | mk...@chromium.org |
| **Created** | 2017-10-08 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36

Steps to reproduce the problem:
1. Go to https://vuln.shhnjk.com/sandbye.html
2. Click on allow notification.
3. Click on notification.

What is the expected behavior?
Popup and modal are blocked.

What went wrong?
https://vuln.shhnjk.com/sandbye.html has iframe sandbox without allow-popups and allow-modals. So popups and modals should be prevented. But Service Worker's openWindow() can bypass this restriction.

Did this work before? N/A 

Chrome version: 61.0.3163.100  Channel: stable
OS Version: OS X 10.13.0
Flash Version:

## Timeline

### el...@chromium.org (2017-10-09)

This seems like it could be by-design (given the use-case of notifications, and the fact that the ServiceWorker could well be alive in service of some other tab). 

[Monorail components: Blink>SecurityFeature Blink>ServiceWorker]

### s....@gmail.com (2017-10-09)

Okay, so second PoC with CSP sandbox.

https://vuln.shhnjk.com/sandbye.php

Since CSP is also applied to SW script, it should be prevented in any tab where service worker has control to.

### mk...@chromium.org (2017-10-09)

Hrm. I certainly agree with Eric's assessment of the initial report (though I'd further note that notifications are not modal dialogs; so far as I know, sandboxing without `allow-modals` doesn't affect the ability to produce them).

The latter report is something we probably need to deal with in the relevant specs, as I don't think it's at all clear what sandboxing a service worker actually means. Right now, it looks like the HTML spec only talks about sandboxing flag sets as applied to Documents, Service Workers doesn't reference the flag set in https://www.w3.org/TR/service-workers-1/#clients-openwindow, and I'm pretty sure Chrome doesn't do any special processing of those flags as applied to workers.

That seems like something we ought to fix, but unfortunately, I think it's something we need to think about first to determine what a fix should look like.

I'm inclined to open this up as something we should add, but I think it's an expected result of current specs and implementations.

+annevankesteren@ for thoughts from HTML's perspective.

### mk...@chromium.org (2017-10-09)

[Empty comment from Monorail migration]

### an...@gmail.com (2017-10-09)

For the initial case: it seems problematic that a third-party can get access to capabilities it doesn't otherwise have just by installing a service worker. I think I would argue it should be sandboxed in that case and openWindow() should be restricted (even when not sandboxed), unless there's some other reason for that service worker to run.

For the subsequent case I think it would make sense to make sandboxing work for workers. We already discussed that in the context of giving them an opaque origin. We should probably go through the various sandboxing flags and see what they might mean within a worker context. I agree that's new functionality and can be discussed publicly.

### s....@gmail.com (2017-10-09)

Just FYI, if you use notification API without openWindow, popup is blocked correctly.

https://vuln.shhnjk.com/sand_doc.html

So this is nothing to do with notification for initial case.

### an...@gmail.com (2017-10-09)

My bad, I missed that. I concur with the earlier analysis in that case.

### s....@gmail.com (2017-10-09)

Sorry, it was FYI to Mike and Eric :(

Summary:

Clicking notification > window.open() > Blocked

Clicking notification > SW > openWindow() > Allowed

>This seems like it could be by-design (given the use-case of notifications)
Use-case of notifications is correctly blocked without SW.





### s....@gmail.com (2017-10-17)

I would appreciate if Anne or Mike starts discussing this on relevant specs to fix the issue. 

Thanks!

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### es...@chromium.org (2018-02-18)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

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

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

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

This issue was migrated from crbug.com/chromium/772759?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Blink>ServiceWorker]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2025-03-26)

this is not fixed, temporarily closing as fixed

### sp...@google.com (2025-03-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact web platform privilege escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-26)

Hi Jun, thank you for this older report back in 2017.
We are going through some of our oldest issues categorized as low severity security bugs and determining for both potential disclosure and VRP Reward. 
While this issue is not yet resolve and given the lower potential for exploitability and harm to those using Chrome, we do feel it would be valuable to the wider community to open this one for public visibility given that any resolution is contingent on a spec change. 
In the interim, we've gone ahead and assessed it for VRP reward as well. Cheers!

### s....@gmail.com (2025-03-28)

Thanks!

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089258)*
