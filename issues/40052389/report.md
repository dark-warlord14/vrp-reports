# Security: Improper Theme name sanitization in theme manager.

| Field | Value |
|-------|-------|
| **Issue ID** | [40052389](https://issues.chromium.org/issues/40052389) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ar...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2020-05-22 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

A malicious theme can be created which has XSS payload in the name part of the manifest.json triggers the injected Code into the HTML when opening the colors a theme section of the theme manager and it is not sanitized. Since CSP is in place, scripts are restricted but an attacker can use this vulnerability to inject a clickbait with a link to perform the malicious operation in the client browser.

**VERSION**  

Chrome Version 83.0.4103.61 + [stable]  

Operating System: [Ubuntu 18.04 LTS]

**REPRODUCTION CASE**

1. Create a standard theme using any theme manager or manually and edit the name inside the manifest.json to '"name":"<a href=https://accounts.google.com/Logout>click for free logout</a>"'
2. Repack all the content into a crx file or load it manually for testing purposes. In a real attack scenario, it could be uploaded in the chrome web store.
3. Once loaded, open the theme manager in the right bottom side of the home screen of google chrome and navigate to Colour and theme.
4. Now the attacker's HTML code is being injected in the name section of the theme and in this case of the payload it creates a hyperlink to logout from all google account for PoC.

## Attachments

- [arun.crx](attachments/arun.crx) (application/octet-stream, 3.9 KB)
- [arun.pem](attachments/arun.pem) (application/octet-stream, 1.7 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 743 B)
- [images - 2020-11-18T123825.323.jpeg](attachments/images - 2020-11-18T123825.323.jpeg) (image/jpeg, 26.3 KB)

## Timeline

### ke...@chromium.org (2020-05-25)

Thanks for the report. This issue appears to be already resolved on Canary though. Can you confirm?

[Monorail components: UI>Browser>Themes]

### ar...@gmail.com (2020-05-25)

[Comment Deleted]

### [Deleted User] (2020-05-25)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2020-05-26)

Hmm. I can repro on Stable but Canary shows the HTML tags properly escaped.

It doesn't work with script tags, which would be awful, but you can add something like a form and a submit button which might have some potential for shenanigans, maybe. At the very least those tags should be escaped properly.

pkasting@: Can you PTAL for thoughts and triage?

### ar...@gmail.com (2020-05-26)

[Comment Deleted]

### [Deleted User] (2020-05-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pk...@chromium.org (2020-05-27)

This isn't the browser's theme system but rather the NTP customization page.  Not sure who the best owner here is.  Maybe yyushkina@ can triage better.

[Monorail components: -UI>Browser>Themes UI>Browser>NewTabPage]

### yy...@chromium.org (2020-05-27)

Oumar or rest of NTP team - can you PTAL?

### ar...@gmail.com (2020-05-31)

[Comment Deleted]

### ar...@gmail.com (2020-06-24)

peeps! No updates?? 

### me...@chromium.org (2020-07-07)

owone, can you PTAL?

### me...@chromium.org (2020-07-07)

[Comment Deleted]

### ar...@gmail.com (2020-07-23)

[Comment Deleted]

### ar...@gmail.com (2020-08-07)

[Comment Deleted]

### ar...@gmail.com (2020-08-23)

[Comment Deleted]

### ar...@gmail.com (2020-08-30)

[Comment Deleted]

### ke...@chromium.org (2020-08-30)

owone@: Are you able to have a look at this, or pass it to someone who can?

### ar...@gmail.com (2020-08-31)

[Comment Deleted]

### ar...@gmail.com (2020-09-22)

[Comment Deleted]

### ar...@gmail.com (2020-10-20)

[Comment Deleted]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ar...@gmail.com (2020-11-09)

I think we are at 6 month mark! yaay🎊🎊🎊

### ar...@gmail.com (2020-11-18)

[Empty comment from Monorail migration]

### ar...@gmail.com (2020-12-15)

[Comment Deleted]

### ar...@gmail.com (2020-12-29)

Happy new year peeps!!


### ke...@chromium.org (2020-12-30)

Trying assigning to an NTP OWNER. aee@ are you able to take a look or help find a new owner?

### ar...@gmail.com (2021-01-10)

[Comment Deleted]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### ar...@gmail.com (2021-04-14)

[Comment Deleted]

### ae...@chromium.org (2021-04-21)

[Empty comment from Monorail migration]

### ar...@gmail.com (2021-06-02)

1 year and no updates? 

### ar...@gmail.com (2021-07-14)

🤷🏻 No response?  I am never going to report anything for this browser. Deleting this report as well.
Disappointed. 

### aj...@google.com (2021-09-17)

Marking this as Fixed as it seemed to be fixed in Canary a while ago (https://crbug.com/chromium/1085762#c4). Reporter: please let us know if this still reproduces.

### aj...@google.com (2021-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-17)

[Empty comment from Monorail migration]

### ar...@gmail.com (2021-10-05)

yes. It is fixed in the recent public release as well now. 

### am...@google.com (2021-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-11)

Hello, OP! Since this bug was not merged into the issue that resolved the issue you reported, and we wanted to apologize that your report went without a response for so long, so we hope you will accept this condolence reward of $500. A member of our finance team will be in touch soon to arrange payment. 

Also, on behalf of the VRP Panel, I wanted to let you know we all appreciated you meme in https://crbug.com/chromium/1085762#c23. We hope you don't mind, but we've undeleted it hoping that others will get to appreciate it also. :) 

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-12-24)

This issue was migrated from crbug.com/chromium/1085762?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052389)*
