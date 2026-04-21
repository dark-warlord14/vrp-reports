# The PWA's installation dialog isn't being dismissed after redirects, which allows an attacker to show it on cross-origin pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40061289](https://issues.chromium.org/issues/40061289) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2022-10-09 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

After the PWA's installation dialog is opened by the user, it is possible to redirect the attacker's page to another website, and given the dialog isn't being dismissed, it will show over cross-origin websites.

This vulnerability can be chained with <https://crbug.com/chromium/1372911> which allows an attacker to control the message displayed on the PWA's installation dialog as well as hide/spoof the origin on it.

I have attached a video (repro.mkv) reproducing the attack.

**VERSION**  

Chrome Version: 105.0.5195.125 (Official Build) (64-bit)  

Operating System: Ubuntu 20.04

**REPRODUCTION CASE**

1. Download "index.html", "manifest.json", "script.js", "sw.js" and serve the files through a web server.
2. Access <http://localhost> and click on the install button located in the top-right position of the address bar.
3. A spoofed PWA's installation dialog will be shown over a cross-origin page with an attacker-controlled message and without an origin being displayed.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [index.html](attachments/index.html) (text/plain, 695 B)
- [manifest.json](attachments/manifest.json) (text/plain, 1.3 KB)
- [script.js](attachments/script.js) (text/plain, 84 B)
- [sw.js](attachments/sw.js) (text/plain, 142 B)
- [repro.mkv](attachments/repro.mkv) (application/octet-stream, 1.6 MB)

## Timeline

### [Deleted User] (2022-10-09)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-09)

The redirection further adds to user misdirection (origin is already hidden using https://crbug.com/1372911) by making the user think that the PWA is associated with the redirected page (like google.com as shown in demo).

Setting same severity(medium) and foundin(105) as https://crbug.com/1372911.

Not familiar with this code so CCing some people based on best guess. Please feel to re-route as appropriate. Thanks.

[Monorail components: UI>Browser>WebAppInstalls]

### [Deleted User] (2022-10-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2022-10-11)

dmurph: a related bug. Note that the easiest way to fix this is probably just to close the installation prompt on navigation.

I'm also downgrading this bug to sev-low -- without the other related bug, the installation prompt would show the true origin on the page.

### he...@gmail.com (2022-10-11)

Hey, doesn't this bug meet the threshold for medium severity even though the attacker's origin is shown in the dialog over the cross-origin page? In the past, I reported similar issues (dialog showing over a cross-origin page with the attacker's origin being displayed) and it was considered a medium security issue (https://crbug.com/chromium/1259694).

Also, I would like to note that the two bugs are being chained together to achieve a higher impact. Not sure whether this is taken into account when deciding the severity of the individual bugs or only during the VRP's panel consideration.

### dm...@chromium.org (2022-11-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### dm...@chromium.org (2022-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-08)

This issue appears to be a duplicate of and resolved by the fixes for https://crbug.com/chromium/1450203. Closing this issue as fixed for verification and to trigger ingress to VRP Panel for assessment. Once this is complete will merge https://crbug.com/chromium/1450203 into this one.

### [Deleted User] (2023-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-08)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-11)

Congratulations Luan! The Chrome VRP Panel has decided to award you $4,000 for this report. Thank you for your efforts and reporting this issue to us, as well as your patience until it was closed and was able to be assessed by the Panel. Thanks for bringing it to my attention at ESCAL8 -- much appreciated and nice work! 

### am...@chromium.org (2023-10-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-10-13)

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

### [Deleted User] (2024-01-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-14)

This issue was migrated from crbug.com/chromium/1372919?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1450203]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061289)*
