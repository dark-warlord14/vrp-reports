# [Android] Security: Chrome Page Preview Bypass SameSite Strict Cookies

| Field | Value |
|-------|-------|
| **Issue ID** | [385662278](https://issues.chromium.org/issues/385662278) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Preload>LinkPreview, UI>Browser>Mobile>PreviewTab |
| **Platforms** | Android |
| **Reporter** | ja...@gmail.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2024-12-23 |
| **Bounty** | $2,000.00 |

## Description

This is a copy of <https://crbug.com/385260469> to track the same problem in Chrome on Android's Preview Page feature.

---

### Report description

Security: Chrome Link Preview Bypass SameSite Strict Cookies

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

SameSite Strict Cookies shouldn't be sent from Cross Site requests even from Top Level Navigations, Opening new windows etc.
This is bypassed in Chrome Link Previews.

YouTube POC - <https://youtu.be/MKnkr_zWTIA>

Steps to Reproduce -

1. Visit <https://httpbin.org/cookies/set/test/test>, intercept response from Burp & modify `Set-Cookie: test=test; Path=/` to `Set-Cookie: test=test; SameSite=Strict; Path=/;` .
2. Now in google search, search for httpbin.org, open the link from google search, notice from Burp Suite, in httpbin.org request, `test` cookie isn't sent from cross site request as expected.
3. Now again do google search for httpbin.org, Instead of clicking on link, right click on link, then click `Preview Link`.
4. Notice in Burp Suite, `test` cookie is sent in cross site request.

#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Attacker can bypass samesite restrictions & perform GET based CSRF attacks or cause harm to users.

---

### The cause

#### What version of Chrome have you found the security issue in?

Version 130.0.6723.70 (Official Build) (64-bit)

#### Is the security issue related to a crash?

No

#### Choose the type of vulnerability

Site Isolation Bypass

#### How would you like to be publicly acknowledged for your report?

Jayateertha Guruprasad

## Timeline

### pe...@google.com (2024-12-24)

Setting milestone because of s2 severity.

### pe...@google.com (2024-12-24)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2025-01-07)

donnd: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-01-22)

donnd: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ah...@google.com (2025-06-04)

[Secondary Security Shepherd]

The bug from which this issue is forked (<https://crbug.com/385260469>) is marked as SecurityImpact-None and low severity. Should we update this bug similarly?

### to...@chromium.org (2025-07-07)

I don't think so.
This is forked because the same problem happens on a different feature.
In the original bug, the feature is disabled. That's the reason for the SecurityImpact-None.
But this Android Preview is a different feature that was launched and has been enabled by default.

### ah...@google.com (2025-07-11)

Thanks for the clarification @to...@chromium.org.

Assigning back to you since I am not the right owner. If this is not on your end, could you help us find an owner please?

Thanks!

### to...@chromium.org (2026-02-17)

This is filed against Mobile>Preview tab, and its description says this is Ephemeral Tab feature.
So, the following OWNERS file will be for the right owner.
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/android/ephemeraltab/OWNERS

Let me assign jinsukkim@ from the file.

### ji...@chromium.org (2026-02-17)

Would somebody add me to [b/385260469](https://issues.chromium.org/issues/385260469) so I can understand the issue from which this was forked better?

### to...@chromium.org (2026-02-17)

[b/385260469](https://issues.chromium.org/issues/385260469) was for an experiment feature that hasn't been launched, or practically cancelled.
It's just kept open until the whole code is removed from the repos.

### vi...@google.com (2026-02-19)

According to [comment #11](https://issues.chromium.org/issues/385662278#comment11), this is a cleanup and it doesn't seem to grant a P1. Downgrading to P2.

### to...@chromium.org (2026-03-09)

The [comment #11](https://issues.chromium.org/issues/385662278#comment11) is about the linked bug and not for this.
Both are the same reports, but this is for the Android Ephemeral Tab, and the other [b/385260469](https://issues.chromium.org/issues/385260469) is for the Desktop Link-Preview.
As the Link-Preview is a cancelled feature, we haven't provided a fix, and there is no further information there, unfortunately. That's what I meant. Sorry for the confusion.

On the other hand, this is a launched feature, available on Android Chrome. So, still P1 is the right priority.
We had a similar issue on Prerender IIRC. So the Prerender team may have an example fix?

### dx...@google.com (2026-04-17)

Project: chromium/src  

Branch:  main  

Author:  Jinsuk Kim [jinsukkim@chromium.org](mailto:jinsukkim@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7766064>

[PreviewTab] Fix SameSite Strict Cookie bypass

---


Expand for full commit details
```
     
    When a user selects "Preview page" from the context menu, the browser 
    creates a new WebContents for the ephemeral tab. This navigation was 
    being treated as a standard, browser-initiated navigation, which made 
    the network stack perceive it as a first-party request (similar to 
    typing a URL in the address bar), which incorrectly includes Strict 
    cookies even if the source site is different. 
     
    To fix this, this CL adds the initiator origin of the page where the 
    context menu was triggered is captured and passed into the navigation 
    parameters of the preview tab. EphemeralTabCoordinator#requestOpenSheet 
    now accepts the initiator as well to build the correct LoadUrlParams to 
    use for navigation. 
     
    Bug: 385662278 
    Change-Id: Ie841d3f14f890815df2e3b795d134bc875985a27 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7766064 
    Reviewed-by: Theresa Wellington <twellington@chromium.org> 
    Commit-Queue: Jinsuk Kim <jinsukkim@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1616874}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/page_info/PageInfoAboutThisSiteController.java`
- M `chrome/android/java/src/org/chromium/chrome/browser/tab/TabContextMenuItemDelegate.java`
- M `chrome/android/javatests/src/org/chromium/chrome/browser/previewtab/PreviewTabTest.java`
- M `chrome/browser/ui/android/autofill/internal/java/src/org/chromium/chrome/browser/ui/autofill/ephemeraltab/PaymentsWindowCoordinator.java`
- M `chrome/browser/ui/android/autofill/internal/java/src/org/chromium/chrome/browser/ui/autofill/ephemeraltab/PaymentsWindowCoordinatorTest.java`
- M `chrome/browser/ui/android/ephemeraltab/java/src/org/chromium/chrome/browser/ephemeraltab/EphemeralTabCoordinator.java`
- M `chrome/browser/ui/android/ephemeraltab/java/src/org/chromium/chrome/browser/ephemeraltab/EphemeralTabMediator.java`

---

Hash: [62735f62914783d07bc9f4618c725ac8d94358c9](https://chromiumdash.appspot.com/commit/62735f62914783d07bc9f4618c725ac8d94358c9)  

Date: Fri Apr 17 21:53:38 2026


---

### ja...@gmail.com (2026-05-19)

Hi team,

As this is fixed, May I know about the bounty status ?

Thanks
Jayateertha G

### ja...@gmail.com (2026-06-03)

Hi team,

As the bug is already fixed and also in plan to be released in M149, kindly let me know about the bounty status.

Thanks
Jayateertha G

### sp...@google.com (2026-06-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/385662278)*
