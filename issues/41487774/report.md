# File Download Origin Spoof Using Long Subdomain

| Field | Value |
|-------|-------|
| **Issue ID** | [41487774](https://issues.chromium.org/issues/41487774) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | lu...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2024-01-03 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description


File Download Origin Spoof Using Long Subdomain


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome (Android)


---

### The problem


#### Please describe the technical details of the vulnerability

This vulnerability is similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1281972.
When the attacker provides the URL as follows: `longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglo.longlong.google.com.ath3r1s.top:9998/app-debug.apk`, there exists a UI Spoof in the component //*[@resource-id="com.android.chrome:id/message_container"]/android.widget.LinearLayout[1] of the com.google.android.apps.chrome.Main Activity.
The long subdomain should be shifted to the left side inside the download section of the browser so that the main domain can be seen clearly.
There are images and videos displayed in the attachment.



#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Long subdomain is shifting the main domain to the right side of the browser which can be ab-used to mask the domain of the downloaded files.



---

### The cause


#### What version of Chrome have you found the security issue in?

120-0-6099-144


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Security UI Spoofing


#### How would you like to be publicly acknowledged for your report?

Ath3r1s




## Attachments

- [991704270134_.pic.jpg](attachments/991704270134_.pic.jpg) (image/jpeg, 429.8 KB)
- [2024-01-03 16-09-55.mp4](attachments/2024-01-03 16-09-55.mp4) (video/mp4, 3.5 MB)

## Timeline

### lu...@gmail.com (2024-01-03)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2024-01-03)

[Empty comment from Monorail migration]

### ph...@chromium.org (2024-01-03)

I can reproduce.
shaktisahu@ Could you take a look as this is related to https://crbug.com/chromium/1281972

[Monorail components: UI>Browser>Bubbles>Download]

### [Deleted User] (2024-01-03)

[Empty comment from Monorail migration]

### ch...@chromium.org (2024-01-03)

This is android ui, not the desktop download bubble.

[Monorail components: -UI>Browser>Bubbles>Download UI>Browser>Downloads]

### [Deleted User] (2024-01-04)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-18)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2024-01-23)

[security shepherd] Since I work on download warnings anyway, and the fix looks straightforward, I'll just take a stab at it: https://crrev.com/c/5231260

### gi...@appspot.gserviceaccount.com (2024-01-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/72e8613d2027d7da5844b42844593ecd7e654050

commit 72e8613d2027d7da5844b42844593ecd7e654050
Author: Daniel Rubery <drubery@chromium.org>
Date: Fri Jan 26 19:37:02 2024

Elide long subdomains in download completion message

Long subdomains in this notification will be truncated, leading users
to only see less-relevant information (the subdomain) instead of the
more-relevant information (the eTLD+1). This CL fixes that, using the
same approach as https://crrev.com/c/4706260

Fixed: 1515222
Change-Id: I43b425894e8061fb7bb93fa031abc6239b0b4b7d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5231260
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1252801}

[modify] https://crrev.com/72e8613d2027d7da5844b42844593ecd7e654050/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/DownloadMessageUiControllerImpl.java
[modify] https://crrev.com/72e8613d2027d7da5844b42844593ecd7e654050/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/DownloadMessageUiControllerTest.java
[modify] https://crrev.com/72e8613d2027d7da5844b42844593ecd7e654050/chrome/browser/download/internal/android/BUILD.gn


### [Deleted User] (2024-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-02)

Congratulations Ath3r1s! The Chrome VRP Panel has decided to award you $3,000 for this report of a security UI spoof. A member of our Google p2p-vrp@ finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1515222?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### lu...@gmail.com (2024-03-08)

Hi, Can I apply a CVE ID for this issue ?

### am...@chromium.org (2024-03-08)

Hello, CVEs are issued when the fix for a security bug ships in a Stable channel release of Chrome. [1]
This fix was landed in M123 and should ship in the first release of Stable 123, scheduled for 19 March.
This bug will be updated with the CVE number directly at that time.

[1] <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/vrp-faq.md#will-i-receive-a-cve-for-my-bug>

### pe...@google.com (2024-05-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### lu...@gmail.com (2024-06-02)

Hi, it seems that I haven't received the reward for this vulnerability yet. Can someone help me follow up on this?

### am...@chromium.org (2024-06-05)

Hello, we don't handle the payments of VRP rewards. Based on the metadata from the bug in the monorail legacy tracker ([crbug.com/1515222](https://crbug.com/1515222)) when the reward was issued, the reward information was sent to the Google finance p2p-vrp team on 2 February 2024. Please reach out to p2p-vrp@ for assistance.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41487774)*
