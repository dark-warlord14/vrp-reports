# Security: tel: URL scheme reference origin spoof in chrome iOS (repro issue 674887) 

| Field | Value |
|-------|-------|
| **Issue ID** | [40094308](https://issues.chromium.org/issues/40094308) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>Intents |
| **Platforms** | iOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ol...@google.com |
| **Created** | 2019-03-16 |
| **Bounty** | $500.00 |

## Description

Chrome Version: 74.0.3729.6 beta  

Operating System: iOS

**REPRODUCTION CASE**

Reference : <https://crbug.com/chromium/674887>

1. Go to <https://lbstyle.github.io/test.html>  
   
   2 Click on the link

## Attachments

- [DB2DF880-FAB4-4818-A8C1-001F18747D38.png](attachments/DB2DF880-FAB4-4818-A8C1-001F18747D38.png) (image/png, 170.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 139 B)

## Timeline

### ch...@gmail.com (2019-03-16)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-03-18)

Reporter: please upload the source to your test pages, as per the instructions when filing a bug.

People who see this bug: do not click on links supplied by reporters.

### ch...@gmail.com (2019-03-18)

Oh okey! 

### wf...@chromium.org (2019-03-18)

Thanks for the quick reply, and the bug! :)

This does indeed seem non-ideal. I wonder if this is also another upstream webkit bug?

eugenebut@ can you take a look and triage this bug further?

### eu...@chromium.org (2019-03-18)

Mohammad, do you know who presents phone call dialog? iOS or Chrome? If Chrome, can we cancel the dialog after the navigation?

[Monorail components: Mobile>Intents]

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### mr...@chromium.org (2019-04-29)

As far as i know, It's OS prompt and i don't think we have any control over it.  + pkl@ who at some point worked on mailto & calls 


### eu...@chromium.org (2019-04-29)

Mohammad, is this problem reproducible in Safari / stock WKWebView ?

### pk...@chromium.org (2019-04-29)

From what I remember, we used to intercept tel:// and present an alert asking user for permission. More recent iOS versions start prompting for permission at the system level and Chrome stopped prompting user for permission and let iOS handle it.
 

### mr...@chromium.org (2019-05-08)

This is reproducable in Safari in iOS 12.2

### eu...@chromium.org (2019-05-08)

Should we file radar for this issue?

### mr...@chromium.org (2019-05-08)

rdar://50583609 was filed

### sh...@chromium.org (2019-07-31)

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

### ct...@chromium.org (2020-05-12)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-05-12)

https://crbug.com/chromium/1081743 is a slight variation on this same bug, using:

var x = window.open('tel://12345678910');
x.window.open('https://www.apple.com');

To trigger the same result.

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### kk...@chromium.org (2020-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### eu...@chromium.org (2021-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

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

### aj...@chromium.org (2024-01-02)

[Empty comment from Monorail migration]

### aj...@chromium.org (2024-01-02)

This bug hasn't been updated in a while, but is blocked on FB8917378, getting an API to find out when OS handling of a tel: URL is finished (so that we can block navigations while this handling is in progress).

### ol...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/11138218a976d5318cb0cef739229a7b7584bfc8

commit 11138218a976d5318cb0cef739229a7b7584bfc8
Author: Olivier ROBIN <olivierrobin@google.com>
Date: Mon Jan 08 13:19:14 2024

Delay navigation until app foreground after external app launches

When an external application is launched chrome is not always put
in background (this is notably the case with system application that
show a confirmation popup to the user).
In that case, a quick navigation when Chrome is inactive foreground
could lead to spoofing.

This CL postpone navigations until the Chrome is back in active state
to avoid showing the wrong page to the user.

Bug: 942807
Change-Id: I11635ba6827b9572a99058c0781aa0f978cc3a34
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5158433
Reviewed-by: Rohit Rao <rohitrao@chromium.org>
Reviewed-by: Quentin Pubert <qpubert@google.com>
Commit-Queue: Olivier Robin <olivierrobin@chromium.org>
Reviewed-by: Ali Juma <ajuma@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1244012}

[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/app_launcher/model/app_launcher_tab_helper.h
[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/app_launcher/model/app_launcher_tab_helper.mm
[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/shared/public/features/features.h
[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/app_launcher/model/app_launcher_browser_agent.h
[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/app_launcher/model/app_launcher_browser_agent.mm
[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/app_launcher/model/BUILD.gn
[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/shared/public/features/features.mm
[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/app_launcher/model/app_launcher_tab_helper_unittest.mm
[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/app_launcher/model/app_launcher_browser_agent_unittest.mm
[modify] https://crrev.com/11138218a976d5318cb0cef739229a7b7584bfc8/ios/chrome/browser/app_launcher/model/app_launcher_tab_helper_delegate.h


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

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/942807?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1081743, crbug.com/chromium/1505822]
[Monorail components added to Component Tags custom field.]

### ch...@gmail.com (2024-04-24)

I think this issue has been fixed for a long time.

### aj...@google.com (2024-04-24)

Yes, this is fixed at least since January (the fix in comment 55), not sure if it was even fixed earlier than that.

### sp...@google.com (2024-05-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
This is a low impact, low severity issue which would not be considered a security issue in Chrome at this time. It was, however, triaged as low severity in 2019 at the time of reporting and also given the delay in rewarding this issue, we would like to extend to you a $500 thank you reward. Thanks for your report and your patience! 

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. Two other things we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.
* If you are already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have already registered, there is no need to repeat the process and you’ll automatically be paid soon. If you have any payment related questions or issues, please reach out to p2p-vrp@google.com.

### pe...@google.com (2024-08-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094308)*
