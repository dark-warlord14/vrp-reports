# Bypass of https://issues.chromium.org/issues/333708039

| Field | Value |
|-------|-------|
| **Issue ID** | [371247941](https://issues.chromium.org/issues/371247941) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Geometry |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2024-10-03 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS

This vulnerability is similar to https://issues.chromium.org/issues/333708039, in this bug when the cursor focus on google one tap button  after that the opacity the frame set 0 (obscured by "click me see funny cats" button) the focus still to  google tap button lead to click jacking
 
VERSION
Chrome Version 131.0.6755.0 (Official Build) canary (64-bit)
Operating System: Windows 10

REPRODUCTION CASE
1. open https://thundering-unruly-windflower.glitch.me/spoofh.html
2. click on  "click me see funny cats" button


CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If
this bug is included, how would you like to be credited?
Reporter credit: Hafiizh (https://www.linkedin.com/in/hafiizh-7aa6bb31/)




## Attachments

- [bandicam 2024-10-04 04-12-43-143.mp4](attachments/bandicam 2024-10-04 04-12-43-143.mp4) (video/mp4, 1.9 MB)
- [spoofh.html](attachments/spoofh.html) (text/html, 2.2 KB)
- [gis.html](attachments/gis.html) (text/html, 946 B)
- [spoofhnew.html](attachments/spoofhnew.html) (text/html, 2.7 KB)
- [bandicam 2024-10-21 07-51-51-804.mp4](attachments/bandicam 2024-10-21 07-51-51-804.mp4) (video/mp4, 1.9 MB)
- [bandicam 2024-10-21 08-25-57-832.mp4](attachments/bandicam 2024-10-21 08-25-57-832.mp4) (video/mp4, 1.6 MB)
- [bandicam 2024-10-25 08-01-33-765.mp4](attachments/bandicam 2024-10-25 08-01-33-765.mp4) (video/mp4, 2.2 MB)

## Timeline

### hc...@google.com (2024-10-03)

Can you please follow the instructions in <https://www.chromium.org/Home/chromium-security/reporting-security-bugs/> and attach any artifacts as well as any other instructions needed for us to reproduce the issue?

### pe...@google.com (2024-10-03)

Thank you for providing more feedback. Adding the requester to the CC list.

### sa...@gmail.com (2024-10-03)

for iframe source (https://pocs.work/pocs/2024/google-one-tap-clickjacking/gis.html):




### sa...@gmail.com (2024-10-04)

another poc:
1. open spoofhnew.html
2. move the cursor into button (to make sure the poc works, make sure google one tap is shown quickly after it disappears because of the opacity: 5%)
3 click on the button

### ca...@chromium.org (2024-10-04)

I'm able to reproduce in current stable, I'll triage this similarly to crbug.com/333708039. szager: Can you PTAL and further triage? Thanks

### pe...@google.com (2024-10-05)

Setting milestone because of s2 severity.

### pe...@google.com (2024-10-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-10-05)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-10-05)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### am...@chromium.org (2024-10-07)

If this is a bypass of [crbug.com/333708039](https://crbug.com/333708039) it would have been introduced much earlier than M130 or at least by the fix for that issue (<https://crrev.com/c5540331>); setting to M128 according (as that is the current oldest active release channel)

### pe...@google.com (2024-10-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### sa...@gmail.com (2024-10-08)

if it fails to reproduce please change in this section :
setTimeout("document.getElementById('x').style.opacity='5%'",300);

change the time (300ms) to be bigger for example : 400,500,etc

### pe...@google.com (2024-10-19)

szager: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sz...@chromium.org (2024-10-20)

I'm not able to reproduce any actual exploit from this. When I click on the button multiple times, eventually I get a "Sign in with Google" popup window asking for confirmation. As long as I "cancel" that, the login fails. I believe the popup window is evidence of the fact that the iframe detected that it was not visible; otherwise it would have permitted the authentication without showing a popup.

I'll leave this open for another week to gather feedback, in case I'm missing something.

### sa...@gmail.com (2024-10-21)

i can reproduce in version : 
Chrome Version 131.0.6768.4 (Official Build) dev (64-bit) 
Chrome Version 132.0.6788.0 (Official Build) canary (64-bit)

### sz...@chromium.org (2024-10-21)

I was able to reproduce this by using a longer setTimeout delay; I have a fix in review.

### ap...@google.com (2024-10-24)

Project: chromium/src  

Branch: main  

Author: Stefan Zager <[szager@chromium.org](mailto:szager@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5950965>

IntersectionObserver -- properly handle "unknown" occlusion state

---


Expand for full commit details
```
IntersectionObserver -- properly handle "unknown" occlusion state 
 
If we most recently reported a target as "guaranteed visible", then in 
the interest of avoiding false positives we must transition to "not 
guaranteed visible" if the frame occlusion state becomes "unknown". 
 
This CL also makes a child frame inherit its parent's "not visible" 
occlusion state rather than calling it "unknown", which is technically 
more correct. 
 
Bug: chromium:371247941 
Change-Id: I4d721dd252d013deac14a12f1f2922830ef2a8a4 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5950965 
Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org> 
Commit-Queue: Stefan Zager <szager@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1373093}

```

---

Files:

- M `third_party/blink/renderer/core/frame/frame_view.cc`
- M `third_party/blink/renderer/core/intersection_observer/intersection_observation.cc`
- A `third_party/blink/web_tests/external/wpt/intersection-observer/resources/v2-midframe.sub.html`
- M `third_party/blink/web_tests/external/wpt/intersection-observer/resources/v2-subframe.html`
- A `third_party/blink/web_tests/external/wpt/intersection-observer/v2/nested-cross-origin.sub.html`

---

Hash: 7b2e3f7ff30d5dcf17cd5c00f0554a44eec2c2a1  

Date:  Thu Oct 24 02:35:39 2024


---

### sa...@gmail.com (2024-10-24)

has this bug been fixed?

### sz...@chromium.org (2024-10-25)

It should be fixed in current Canary channel Chrome; it will reach Dev channel in about a week.

### sa...@gmail.com (2024-10-25)

i have tested in version 132.0.6796.0 (Official Build) canary (64-bit) , i cannot reproduced it. Can the status of this report be changed to fixed?

### pe...@google.com (2024-10-28)

The NextAction date has arrived: 2024-10-28
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### sa...@gmail.com (2024-11-14)

Hi, has there been a decision from the Chrome VRP panel regarding bounty rewards?

### am...@chromium.org (2024-11-18)

Hello, this is in our queue, but there have been a number of high severity issues for us to assess in the last few weeks. This issue should be assessed this week or next. As always, when assessment has taken place a reward decision will be provided here. Thank you for you patience in the meantime.

### sp...@google.com (2024-11-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of moderate impact security UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-20)

Congratulations Hafiizh! Thank you for your efforts and reporting this issue to us.

### sa...@gmail.com (2024-11-21)

thank you amy..

### am...@chromium.org (2025-01-14)

the original content of this report was set as `restricted content`; which should not be a setting used for the information in a Chrome security bug report, the following is the content from the original report:

=====================
VULNERABILITY DETAILS============

This vulnerability is similar to <https://issues.chromium.org/issues/333708039>, in this bug when the cursor focus on google one tap button after that the opacity the frame set 0 (obscured by "click me see funny cats" button) the focus still to google tap button lead to click jacking

VERSION
Chrome Version 131.0.6755.0 (Official Build) canary (64-bit)
Operating System: Windows 10

REPRODUCTION CASE

1. open <https://thundering-unruly-windflower.glitch.me/spoofh.html>
2. click on "click me see funny cats" button

### qk...@google.com (2025-01-17)

Labeling as LTS-NotApplicable-126 because M126 doesn't have the suspected CL[1] and the bug was introduced from M128 according to the comment #11. 

[1] https://chromium-review.googlesource.com/c/chromium/src/+/5540331

### pe...@google.com (2025-02-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/371247941)*
