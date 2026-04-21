# Security: chrome.debugger API can capture cookies of host blocked by Enterprise Policy

| Field | Value |
|-------|-------|
| **Issue ID** | [40075672](https://issues.chromium.org/issues/40075672) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise, Platform>Extensions |
| **Platforms** | Linux |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2023-10-26 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

If a policy is set by an enterprise to block host using runtime\_blocked\_hosts, an extension installed on a user's system should not permit reading of cookies from a blocked host. However, using the chrome.debugger API's Network.getAllCookies, it is possible to capture cookies from a blocked host.

**VERSION**  

Chrome Version: 117.0.5938.149 (Official Build) (64-bit)  

Operating System: Linux

**REPRODUCTION CASE**

1. Download the attached files (manifest.json, background.js) and put it in a directory - the extension directory.
2. Create an enterprise policy to block a domain, such as google.com. I believe that this policy is already active for Googlers. So, if you are a Googler, you can skip this step.  
   
   To configure on Chromium for Linux, see <https://support.google.com/chrome/a/answer/7517525>, create policy using below code:

{  

"ExtensionSettings": {  

"\*": {  

"runtime\_blocked\_hosts": ["\*://\*.google.com"],  

"blocked\_permissions": []  

}  

}  

}

3. Load the extension for testing

Expected:

- Fetching cookies from google.com should not be allowed when blocked by Enterprice policy.

Actual:

- The Enterprise policy is successfully bypassed using Network.getAllCookies, and the cookies are listed in the extension console. This could potentially be further exploited to send the data to a remote server.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [background.js](attachments/background.js) (text/plain, 580 B)
- [manifest.json](attachments/manifest.json) (text/plain, 225 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 3.0 MB)
- deleted (application/octet-stream, 0 B)
- [background.js](attachments/background.js) (text/plain, 1.3 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 225 B)
- [test-policy.mp4](attachments/test-policy.mp4) (video/mp4, 2.0 MB)

## Timeline

### [Deleted User] (2023-10-26)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-10-26)

Similar issue: crbug.com/1139156

### pa...@chromium.org (2023-10-26)

[security shepherd] Thanks for the report!

Assigning to @caseq@chromium.org as this seems indeed extremely related to crbug.com/1139156.

[Monorail components: Enterprise Platform>Extensions]

### pa...@chromium.org (2023-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-26)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-10-26)

Here is a modified background.js file. It can be used for different sites blocked by Enterprise policy (modify targetSite). The attacker can then capture the site's cookies using Network.getAllCookies and potentially steal session tokens and other sensitive cookies to cause harm.

For Chrome on other platforms, see:
   * Windows - https://support.google.com/chrome/a/answer/7532015
   * macOS - https://support.google.com/chrome/a/answer/7517624
   * Linux - https://support.google.com/chrome/a/answer/7517525

### fa...@gmail.com (2023-10-26)

[Comment Deleted]

### fa...@gmail.com (2023-10-27)

Here is a modified proof-of-concept suitable for sites restricted by enterprise policies (please adjust the 'targetSite' parameter accordingly). An attacker may exploit this to extract cookies from the blocked site using the 'Network.getAllCookies' method, thereby risking the unauthorized access to session tokens and other sensitive data, which could lead to potential harm for the Enterprise.

To set up Enterprise policy of Chrome on other platforms, see:
   * Windows - https://support.google.com/chrome/a/answer/7532015
   * macOS - https://support.google.com/chrome/a/answer/7517624
   * Linux - https://support.google.com/chrome/a/answer/7517525

### [Deleted User] (2023-10-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-09)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2023-11-16)

I'm taking care (https://chromium-review.googlesource.com/c/chromium/src/+/5039174) of this one, because we were not supposed to let extensions use Network.getAllCookies, at least in the spirit of https://chromium-review.googlesource.com/c/chromium/src/+/3929023 -- Network.getAllCookies is deprecated in favor of Storage.getCookies, and this CL restricts the latter.

That said, I'm somewhat skeptical of our overall ability to honor `runtime_blocked_hosts` across CDP  -- a fine-grained per-URL access control just wasn't the original design goal and with the power of CDP it may be challenging to implement it consistently. The original contract was that once extension has a `debugger` permission, it can access _all data on all sites_. Perhaps the most practical approach when the goal is to block access to certain sites would be to disallow debugger extensions altogether. Should perhaps the enterprise policy imply this?

+dsv@, rdevlin.cronin@, adetaylor@ for visibility and thoughts.


### ad...@chromium.org (2023-11-17)

I think it would be great to document the expected security model for devtools in an FAQ here - https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md#Other - I think we've got something internal but getting it published would guide our VRP reporters to raise the most impactful and relevant bugs.

### gi...@appspot.gserviceaccount.com (2023-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/55e32689fd4e3c70cadda854a18cca7152090877

commit 55e32689fd4e3c70cadda854a18cca7152090877
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Fri Nov 17 17:48:22 2023

Do not let chrome.debugger extensions invoke Network.getAllCookies

Network.getAllCookies is deprecated in favor of Storage.getCookies
and the latter is not allowed for extensions, so we shouldn't let
extensions use the former either.

Bug: 1496250
Change-Id: I3e97e9249dbba61d1f7951ed22ef9b1bef9f2355
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5039174
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1226203}

[modify] https://crrev.com/55e32689fd4e3c70cadda854a18cca7152090877/content/browser/devtools/protocol/network_handler.h
[modify] https://crrev.com/55e32689fd4e3c70cadda854a18cca7152090877/content/browser/devtools/worker_devtools_agent_host.cc
[modify] https://crrev.com/55e32689fd4e3c70cadda854a18cca7152090877/chrome/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/55e32689fd4e3c70cadda854a18cca7152090877/content/browser/devtools/shared_worker_devtools_agent_host.cc
[modify] https://crrev.com/55e32689fd4e3c70cadda854a18cca7152090877/content/browser/devtools/protocol/network_handler.cc
[modify] https://crrev.com/55e32689fd4e3c70cadda854a18cca7152090877/content/browser/devtools/service_worker_devtools_agent_host.cc
[modify] https://crrev.com/55e32689fd4e3c70cadda854a18cca7152090877/content/browser/devtools/render_frame_devtools_agent_host.cc


### fa...@gmail.com (2023-11-18)

[Comment Deleted]

### fa...@gmail.com (2023-11-18)

Hi, I would like to provide some context about this issue for the panel. I have tested this with various Chrome APIs (For instance, chrome.cookies.getAll, for which I provide a video demonstrating a test illustrating the adherence of this API to the enterprise policy). When the enterprise policy is set up for Chrome extensions, and access to any cookies from that particular blocked site is blocked due to runtime_blocked_hosts,when testing with different APIs. Ultimately, I found that chrome.debugger's Network.getAllCookies method can successfully be used to steal cookies from a blocked site using this approach. Implementing this fix could prevent such attacks.Thank you.

### fa...@gmail.com (2023-11-30)

[Comment Deleted]

### fa...@gmail.com (2023-11-30)

Hi, can we close this issue now that it's fixed? It's been open for more than a week after commit https://crbug.com/chromium/1496250#c14. Thanks!

### fa...@gmail.com (2023-11-30)

Also, please add other OS's as well. It not only impacts Linux but also other OS's supported byChrome Enterprise ( https://chromeenterprise.google/ ), similar to crbug.com/1139156.

### am...@chromium.org (2023-12-04)

I'm going to go ahead and close this issue as fixed, based on the CL in https://crbug.com/chromium/1496250#c14. Please feel free to correct if that is in error. 

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-04)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-12-14)

Congratulations Shaheen! The Chrome VRP Panel has decided to award you $2,000 for this report. The reward amount was decided based on the required precondition of the user needing to install the malicious extension with debugger permissions and convincing / social engineering a user to do that for an attacker to be able to exploit this issue. Thank you for your efforts and reporting this issue to us! 

### fa...@gmail.com (2023-12-14)

Thank you.

### fa...@gmail.com (2023-12-14)

Hi Amy, is this issue eligible for a CVE? Additionally, can we add the rest of the affected operating systems as well, for the record? Thank you.

### am...@chromium.org (2023-12-15)

Hi Shaheen, yes, this bug is eligible for a CVE. As mentioned prior, CVEs are issued when the fix ships in a Stable channel update. This fix landed in 121 and was not backmerged to other channels, so a CVE will be issued when the fix ships in the first release of M121 Stable. 

### am...@chromium.org (2023-12-15)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-23)

This issue was migrated from crbug.com/chromium/1496250?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Enterprise, Platform>Extensions]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075672)*
