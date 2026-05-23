# Security: Bypassing of security interstitials using debugger API

| Field | Value |
|-------|-------|
| **Issue ID** | [40057865](https://issues.chromium.org/issues/40057865) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jo...@pa.uc3m.es |
| **Assignee** | ds...@chromium.org |
| **Created** | 2021-11-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

An extension with access to the "chrome.debugger" API can attach to tabs  

displaying a security interstitial without requiring higher privileges as  

such dialogs are loaded in a regular web renderer process outside the  

"chrome://" scheme (kUnreachableWebDataURL).

An attacker who convinced a user to install a malicious extension can then  

evaluate a JavaScript expression to modify the security message or skip it  

altogether when a proceed button is available.

**VERSION**  

Chrome Version: 95.0.4638.69 stable  

Operating System: Windows 10 21H1, OS build 19043.1320

**REPRODUCTION CASE**

1. Install and enable the provided extension
2. Trigger an interstitial (e.g., by visiting <https://expired.badssl.com/>  
   
   or <https://testsafebrowsing.appspot.com/s/phishing.html>)

The PoC extension will automatically skip the interstitial without  

requiring further user interaction.

**CREDIT INFORMATION**  

Reporter credit: José Miguel Moreno  

Computer Security Lab (COSEC) at UC3M

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 301 B)
- [background.js](attachments/background.js) (text/plain, 1.9 KB)

## Timeline

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions>API]

### [Deleted User] (2021-11-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### rd...@chromium.org (2021-11-18)

Interesting find!

This is explicitly allowed here [1], which was added here [2] as part of https://crbug.com/chromium/882589.  The intention there was to allow the extension to stay connected if the web page threw an error (with "offline" as the main error motivating the change) - that's, I think, still desirable.  But we probably don't want to allow extensions to modify interstitials.

nasko@, lukasza@ - would it make sense to serve security interstitials at a different address than other errors?  Alternatively, we might be able to look at the WebContennts' last commit error code and make a determination there - but it'd be simpler if we could just filter on URL.

Tentatively passing this to danilsomsikov as a debugger owner.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/debugger/debugger_api.cc;l=99-100;drc=535cf78ce1fa21d1f67a092f60ebfe76d9eef882
[2] https://chromium-review.googlesource.com/c/chromium/src/+/1217599/

### ds...@chromium.org (2021-12-16)

[Empty comment from Monorail migration]

### ds...@chromium.org (2022-02-15)

[Empty comment from Monorail migration]

### jo...@pa.uc3m.es (2022-04-22)

Any updates on this?

### ds...@chromium.org (2022-04-22)

Yup, please see crrev.com/c/3594083

### na...@chromium.org (2022-04-22)

Should we be closing this bug as fixed then?

### ds...@chromium.org (2022-04-25)

It's not landed yet. Will close the bug as soon as it does.

### gi...@appspot.gserviceaccount.com (2022-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2d1a92dd76bbe7d7e5463c8ec57edba721793247

commit 2d1a92dd76bbe7d7e5463c8ec57edba721793247
Author: Danil Somsikov <dsv@chromium.org>
Date: Tue Apr 26 15:12:21 2022

Disallow chrome.debugger connection to security interstitial.

Bug: 1268445
Change-Id: I581415e584a1874bdb071c8263a41e214c72bb09
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3594083
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Auto-Submit: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#996187}

[modify] https://crrev.com/2d1a92dd76bbe7d7e5463c8ec57edba721793247/chrome/browser/extensions/api/debugger/debugger_api.cc
[modify] https://crrev.com/2d1a92dd76bbe7d7e5463c8ec57edba721793247/chrome/browser/extensions/BUILD.gn
[modify] https://crrev.com/2d1a92dd76bbe7d7e5463c8ec57edba721793247/chrome/browser/extensions/api/debugger/debugger_apitest.cc


### ds...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-26)

[Empty comment from Monorail migration]

### jo...@pa.uc3m.es (2022-05-30)

Hello! Could you could assign a CVE number to this vulnerability?

### am...@google.com (2022-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-13)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and reporting this issue to us. 

To answer your question in C#17, CVE IDs are assigned at the time a the fix for the issue ships in a stable channel release. As this is a low severity issue, the fix has not yet shipped in a stable channel release. It appears it was landed in 103 and will ship with the 103 stable channel release Tuesday, June 24 and will receive a CVE at that time. 

### am...@google.com (2022-06-16)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-08-02)

This issue was migrated from crbug.com/chromium/1268445?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057865)*
