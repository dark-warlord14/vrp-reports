# Security: Chrome iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40064432](https://issues.chromium.org/issues/40064432) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | ia...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2023-05-08 |
| **Bounty** | $1,000.00 |

## Description

Affecting Chrome iOS Version 113.0.5672.69
Tested On iPhone 12 Running 16.4.1 (a)

#Summary
A sandboxed iframe, particularly without the "allow-same-origin" flag set, can generate a popup window containing HTTP content, even when the window's source is an HTTPS site. In this scenario, the browser does not block the mixed content and does not display any warning indicating its inclusion.


Steps
======
1.Download iframe.html & index.html (attached) and place all files in same directory

2. Browser index.html in Chrome iOS ex. http://site.com/index.html and click on Open Button and it will load a http URL in an Iframe tag

That iframe should be blocked, given that the site is loaded over https. Instead, the iframe loads successfully. The browser also doesn't display any indication that there's mixed content on the page.


This may fall under ExternalDependency as per Chrome Bug Report. Already reported to Apple Report ID - OE09432617177


## Attachments

- [iframe.html](attachments/iframe.html) (text/plain, 158 B)
- [index.html](attachments/index.html) (text/plain, 152 B)

## Timeline

### [Deleted User] (2023-05-08)

[Empty comment from Monorail migration]

### bb...@google.com (2023-05-08)

[Empty comment from Monorail migration]

[Monorail components: Internals>Sandbox>SiteIsolation]

### bb...@google.com (2023-05-08)

Confirmed locally on 113.0.5672.69, on iOS 16.1.2

Appears to be only iOS (does not work on other platforms I have tried) and likely an External Dependency


### bb...@google.com (2023-05-08)

[Empty comment from Monorail migration]

### na...@chromium.org (2023-05-08)

Site Isolation is not present on iOS, since we use underlying WKWebView from Apple. Moving over to iOSWeb>Security component.

[Monorail components: -Internals>Sandbox>SiteIsolation Mobile>iOSWeb>Security]

### aj...@chromium.org (2023-05-09)

Marking as external dependency. As noted above, this has already been reported to Apple.

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ia...@gmail.com (2023-05-21)

is it possible to add some one from Apple Team here just to keep a track of the bug?

### ia...@gmail.com (2023-05-27)

Can we add ddkil...@apple.com in this report?

### aj...@chromium.org (2023-05-29)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-07-01)

Apple Team responded that "They are working to address this in a security update later this summer and aim to have a beta available for testing in the coming weeks."

@ajuma@chromium.org I suggest we should make this at least medium based on the vulnerability behaviour and exposure of sensitive information into the network which allow MITM attacks.


### aj...@chromium.org (2023-07-04)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-08-11)

Hello Team, the vulnerability is now fixed in recent apple security update. You may check as well.

### dd...@apple.com (2023-08-11)

Tracked here for WebKit:

https://crbug.com/chromium/257331: Framed pages have ability to bypass Mixed Content restrictions
<https://bugs.webkit.org/show_bug.cgi?id=257331>

Fixed in iOS 16.6.


### aj...@chromium.org (2023-08-11)

Thanks for the update!

### [Deleted User] (2023-08-11)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2023-08-11)

Trying to use Foundin-NA to make sheriffbot happy.

### [Deleted User] (2023-08-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-14)

[Empty comment from Monorail migration]

### ia...@gmail.com (2023-08-31)

Dear VRP Team, is there any update bounty bounty decision?

### ia...@gmail.com (2023-09-04)

Just an input for VRP Team.

The impact of my report is,  If a website is configured to use HTTPS (secure HTTP) but can still be loaded as HTTP (unsecured HTTP) through a vulnerability in cweb browser which is fixed now and once it loaded the sensitive data will get travel into network in simple text format which is easily readable by other users seating on the same network. it can have several significant negative impacts on security and user trust:

1.Data Interception: The primary purpose of HTTPS is to encrypt the data transmitted between the user's browser and the web server. When a website can be loaded as HTTP, this encryption is bypassed, making it easier for attackers to intercept sensitive information exchanged between the user and the website. This can include login credentials, personal data, financial information, and more.

2.Man-in-the-Middle (MitM) Attacks: Attackers can exploit this vulnerability to conduct Man-in-the-Middle attacks, where they intercept and manipulate the communication between the user and the website. They can inject malicious content or steal data without the user's knowledge.

3.Mixed Content Issues: Loading some resources over HTTP while the main page uses HTTPS can trigger mixed content warnings in modern browsers. This can lead to broken functionality or an insecure browsing experience.



### am...@chromium.org (2023-09-08)

The VRP has just reconvened from a two-week pause in VRP Panel sessions. Thank you for your patience as we will review this issue in a future VRP Panel session. 

### ia...@gmail.com (2023-09-11)

Sire, Thanks for the update 

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations! The VRP Panel has decided to award you $1,000 for this report based on this report as presented and impact in terms of exploit mitigation bypass / information leak. Thank you for your efforts in reporting this issue to us and Apple! 

### ia...@gmail.com (2023-09-15)

Thank you. BTW, guess what? Today is my birthday and I got the bounty :) 

### am...@chromium.org (2023-09-16)

Happy belated birthday! Glad we were able to get you a gift of a VRP reward on your day! Cheers!!

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-11-17)

Hi again Narendra, We consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Thanks!

### is...@google.com (2023-11-17)

This issue was migrated from crbug.com/chromium/1443571?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064432)*
