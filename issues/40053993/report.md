# Security: Cast tab can appear after navigation to a different origin

| Field | Value |
|-------|-------|
| **Issue ID** | [40053993](https://issues.chromium.org/issues/40053993) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Cast>UI |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mf...@chromium.org |
| **Created** | 2020-11-26 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: 89.0.4336.0 (Official Build) canary (x86\_64)  

Operating System: macOS

**REPRODUCTION CASE**

1. go to any website e.g google.com
2. open the testcase <http://127.0.0.1:8000/testcase.html>
3. Click on the button
4. Go Backward to google.com

This bug allows web content to tamper with trusted browser UI.

## Attachments

- [testcase.html](attachments/testcase.html) (text/plain, 500 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 2.5 MB)

## Timeline

### [Deleted User] (2020-11-26)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-11-30)

Security sheriff here: Thanks for the report. I think the bug here is that the Cast dialog isn't dismissed on navigation. That said, this requires the user have a "trusted" page in their history and go back to it (I think that if the script tries to navigate the page, it will dismiss the dialog), the dialog includes the actual origin being casted, and the script triggering the cast dialog can only cast itself rather than arbitrary web content.

Of note: Using the browser "Cast..." option to cast a tab brings up the same dialog, but it _does_ get correctly dismissed on navigation.

Conservatively setting this to Severity-Low in case there is a more useful attack lurking here, but this might just be a polish bug for PresentationRequest.

[Monorail components: Internals>Cast>UI]

### mf...@chromium.org (2020-11-30)

The PresentationRequest won't be very useful because the document that requested it shouldn't be available after top navigation.

But we should probably discard any pending PresentationRequests on navigation to be on the safe side.

takumif@, WDYT?

### ta...@chromium.org (2020-11-30)

I see that the sample code does recursion to endlessly call PresentationRequset#start(). It seems that the dialog is being re-opened between the user click to navigate and the actual navigation, and it sticks around.

The dialog wouldn't do anything unless the user clicks on a Cast device in the dialog, at which point either the original receiver page would be cast, or it might fail because the PresentationRequest is gone on the renderer side. Unless I'm missing a security concern and sites would try to exploit it, this is not a scenario users are likely to hit.

I wasn't able to repro the navigation with the sample code -- after clicking on the back button it'd just stay on the same page, with the favicon spinning.

### mf...@chromium.org (2020-12-11)

Given the unreliable PoC and the fact that no user data is put at risk, putting this in the backlog.


### [Deleted User] (2020-12-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### aj...@google.com (2021-09-16)

mfoltz: we like for security bugs to have owners - please assign to someone else or CC in more people if that would help to resolve this issue.

### [Deleted User] (2021-09-16)

[Empty comment from Monorail migration]

### mf...@chromium.org (2021-09-17)

No plans to look at this any time soon.


### ch...@gmail.com (2021-09-17)

I'm no longer able to repro this on 96.0.4645.0 canary on Windows.

### aj...@google.com (2021-09-17)

Following https://crbug.com/chromium/1152952#c19 let's assume we have fixed this. Thanks for re-evaluating!

### [Deleted User] (2021-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-18)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-28)

Hi Khalil, this issue appears to be addressed via another fix. The VRP Panel would like to extend to you a $1000 award as we appreciate you reporting this to us and your patience while this report got resolved! Thank you! 

### ch...@gmail.com (2021-09-28)

Thanks as ever!

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2022-12-14)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

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

This issue was migrated from crbug.com/chromium/1152952?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053993)*
