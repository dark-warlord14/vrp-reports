# Security: ChromeVox on ChromeOS uses HTTP without SSL for some requests:

| Field | Value |
|-------|-------|
| **Issue ID** | [40084807](https://issues.chromium.org/issues/40084807) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Accessibility |
| **Platforms** | ChromeOS |
| **Reporter** | ya...@nightwatchcybersecurity.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2016-07-12 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

ChromeVox on ChromeOS uses HTTP without SSL for some requests:

We saw the following URLs:  

[http://fonts.googleapis.com/css?family=Droid+Sans+Mono|Roboto:400,700,700italic](http://fonts.googleapis.com/css?family=Droid+Sans+Mono%7CRoboto:400,700,700italic)

<http://fonts.gstatic.com/s/roboto/v15/t6Nd4cfPRhZP44Q5QAjcC44P5ICox8Kq3LLUNMylGO4.woff2>

**VERSION**  

Chrome Version: 51.0.2704.106 (stable)  

Operating System: ChromeOS 8172.62.0 (stable)

**REPRODUCTION CASE** :

1. Setup a proxy with WiFi.
2. Switch ChromeOS device to use proxy.
3. Restart the device and on the login screen enable ChromeVox.
4. Observe calls to HTTP without SSL.

## Timeline

### ri...@chromium.org (2016-07-13)

Mind taking a look at this one, dtseng@?

### sh...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### ta...@google.com (2016-07-13)

[Empty comment from Monorail migration]

[Monorail components: UI>Accessibility]

### me...@chromium.org (2016-07-13)

Are these URLs being embedded on chrome-extension:// pages? If so, https://crbug.com/chromium/398790 might be relevant.

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-03-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-07-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### dt...@chromium.org (2017-09-18)

https://codereview.chromium.org/2776293002

### ya...@nightwatchcybersecurity.com (2017-09-18)

Does this get a CVE and/or qualify for a bounty?

### me...@chromium.org (2017-09-18)

+awhalley for https://crbug.com/chromium/627300#c15.

### aw...@chromium.org (2017-09-18)

Looks like this wasn't marked as fixed when the release it was fixed in was released :-)  Marking with M-62 to get that picked up for release note and CVE allocation then (though shout if you need it sooner and I can do it manually)

We don't usually reward for low severity bugs, but we'll take a look in a future VRP panel.

### sh...@chromium.org (2017-09-19)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-20)

The VRP panel decided to award $500 for this report.  Also, how would you like to be credited on the release notes when 

### aw...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2017-10-20)

Thank you! Please credit "Nightwatch Cybersecurity Research" in the notes.

Is there a CVE being assigned?

### aw...@google.com (2017-10-26)

Pardon the delay, CVE assigned.

### ya...@nightwatchcybersecurity.com (2017-10-26)

Thank you! At what point is it ok to disclose publicly? I checked the list of changes for Chrome 62 and don't see this one there.

### aw...@chromium.org (2017-10-28)

This bug will be automatically opened 14 weeks after the fix date. This was indeed released with Chrome OS 62, which went stable yesterday.  Expect the release notes to be updated with this and a few other security bugs in about a week.

Please feel free to disclose this publically after 7th November, so folks have some time to update their systems to 62.

Thanks again for the report!

### aw...@chromium.org (2017-11-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@nightwatchcybersecurity.com (2018-01-01)

Our advisory published here, thank you!

https://wwws.nightwatchcybersecurity.com/2018/01/01/chromeos-doesnt-always-use-ssl-during-startup-cve-2017-15397/

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/627300?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084807)*
