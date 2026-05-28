# The PWA's installation dialog isn't being dismissed after redirects, which allows an attacker to sho

| Field | Value |
|-------|-------|
| **Issue ID** | [351564774](https://issues.chromium.org/issues/351564774) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Mobile>Messages, UI>Browser>WebAppInstalls>Android |
| **Platforms** | Android |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | bh...@gmail.com |
| **Assignee** | la...@google.com |
| **Created** | 2024-07-07 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

go to mrnoob790.github.io/index.html
click on add homescreen and then fastly click on install app u will installation popup come in screen and website is redirect to google.com

# Problem Description

After the PWA's installation dialog is opened by the user, it is possible to redirect the attacker's page to another website, and given the dialog isn't being dismissed, it will show over cross-origin websites

# Summary

The PWA's installation dialog isn't being dismissed after redirects, which allows an attacker to sho

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [screen-20240708-011112.mp4](attachments/screen-20240708-011112.mp4) (video/mp4, 13.1 MB)
- [sw.js](attachments/sw.js) (text/javascript, 142 B)
- [dummy-sw.js](attachments/dummy-sw.js) (text/javascript, 156 B)
- [index.html](attachments/index.html) (text/html, 695 B)
- [manifest.json](attachments/manifest.json) (application/json, 1.3 KB)
- [Mon Jul 08 2024 14:06:14 GMT-0700 (Pacific Daylight Time).png](attachments/Mon Jul 08 2024 14_06_14 GMT-0700 (Pacific Daylight Time).png) (image/png, 67.7 KB)
- [VID-20240711-WA0001.mp4](attachments/VID-20240711-WA0001.mp4) (video/mp4, 10.2 MB)

## Timeline

### bh...@gmail.com (2024-07-07)

deleted

### bh...@gmail.com (2024-07-07)

there is no need  to disable popup blocker 

### bh...@gmail.com (2024-07-08)

all chrome stable canary beta  dev  vulnerable for that 

### wf...@chromium.org (2024-07-08)

The dialog does contain an origin, it says it's mrnoob790.github.io... see screenshot

### bh...@gmail.com (2024-07-08)

sorry actually  its not change the origin in popup .but u will see after the redirect to different web the pwa installer popup is not closed 

### wf...@chromium.org (2024-07-08)

this looks very similar to [issue 40061289](https://issues.chromium.org/issues/40061289), has this regressed or is this a different bug?

### bh...@gmail.com (2024-07-08)

yup its totally similar to that  but thats working in window.

### dm...@chromium.org (2024-07-08)

ah - yes this is Android. I don't believe Android install implemented the protections from that bug. Routing to Ella to triage.

### bh...@gmail.com (2024-07-10)

do i need to upload canary beta dev . poc or that stable one is ok 

### ei...@chromium.org (2024-07-10)

This seems to be the same as issue 40064636. lazzzis@ mind take a look?

### dm...@chromium.org (2024-07-10)

As per Ella - "the issue is with the model dialog in Clank, twellington@'s team owns this space. Maybe "UI>Browser>Mobile>Messages""

### la...@google.com (2024-07-10)

The tab modal lifetime handler dismisses the dialog once TabObserver#onPageLoadStarted is triggered. On my side, the onPageLoadStarted is triggered before the PwaUniversalInstallBottomSheetCoordinator#onInstallClicked. That's the reason why the dialog stays on google.com.

The test site starts redirection on the Window#onblur <https://github.com/mrnoob790/mrnoob790.github.io/blob/main/index.html#L11>. This method is triggered once a bottom sheet is showing, including the PWAInstallBottomSheet and the BookmarkBottomSheet.

Disallowing click events during BottomSheet's animation should fix the issue.

add bottom sheet owner

### bh...@gmail.com (2024-07-11)

so there is one more issue on window/mac/linux not tested on chrome os  if u install the pwa  it will not show any icon in desktop and  launcher . for using that pwa u need to open mrnoob790.github.io/index html then click there then the pwa will be open 

### tw...@google.com (2024-07-11)

> The tab modal lifetime handler dismisses the dialog once TabObserver#onPageLoadStarted is triggered. On my side, the onPageLoadStarted is triggered before the

I'm not quite following the flow. The "Install app" dialog is coming from mrnoob790.github.io after the user is on google.com.  The "Install app" is a javascript dialog triggered by the webpage, correct?

So it would seem the request to enqueue the dialog is coming in after #onPageLoadStarted for google.com?

> Disallowing click events during BottomSheet's animation should fix the issue.

This seems like it could be a nice UX improvement generally so that UI that's in motion isn't getting touch events. Might make sense to do that at the bottom sheet level. mdjones@ wdyt?

### la...@google.com (2024-07-11)

> The "Install app" is a javascript dialog triggered by the webpage, correct?

no. It is a [dialog](https://source.chromium.org/chromium/chromium/src/+/main:components/webapps/browser/android/java/src/org/chromium/components/webapps/pwa_universal_install/PwaUniversalInstallBottomSheetCoordinator.java;l=192;drc=2385479e028cfd50420ff8a4406da113d65622c6;bpv=1;bpt=1?q=PwaUniversalInstallBottomSheetCoordinator&ss=chromium%2Fchromium%2Fsrc) triggered by Chrome when "install app" in the bottom sheet is clicked.

### tw...@google.com (2024-07-11)

I wonder if we ought to be more defensive somewhere and check the current URL before enqueuing the dialog... I'm not sure just preventing taps on the bottom sheet will fully resolve the race condition between the page redirecting & PWA code requesting to enqueue the dialog.

Two options I see:
1) Update PWA code to handle this case
2) TabModalDialogLifetimeHandler doesn't currently have the information it needs since it'd have to know what URL the dialog should be associated with, not just what Tab... but perhaps we could update APIs so that enqueued tab modal dialogs have an associated URL and are rejected if the URLs don't match

### bh...@gmail.com (2024-07-12)

why the priority and serverity didnt change yet ? and why on desktop pwa install not show the app on desktop 

### pe...@google.com (2024-07-13)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### bh...@gmail.com (2024-07-16)

i also think Disallowing click events during BottomSheet's animation should fix the issue.

### la...@google.com (2024-07-17)

> why on desktop pwa install not show the app on desktop

Please file a bug under the component Chromium > UI > Browser > WebAppInstalls > Desktop. Thanks!

### bh...@gmail.com (2024-07-17)

okk will do after these issue fixed

### bh...@gmail.com (2024-07-18)

any update on these 

### bh...@gmail.com (2024-07-19)

hi need little help one of my security bug ticket i mistakenly touched uncc now am not able to see that report in reported by me section can u please help me to get back to that ticket 

### la...@google.com (2024-07-19)

Re #23: will pick this up when time available.

Re #24: you are on the cc list

### bh...@gmail.com (2024-07-19)

thanks for update

### la...@google.com (2024-07-19)

I am sorry but I am also unable to add you back if I am not on the cc list of that report.

### bh...@gmail.com (2024-07-19)

deleted

### bh...@gmail.com (2024-08-02)

hey any update 

### bh...@gmail.com (2024-08-13)

deleted

### bh...@gmail.com (2024-08-27)

deleted

### bh...@gmail.com (2024-09-13)

any update 

### la...@google.com (2024-09-16)

in engineer's backlog

### bh...@gmail.com (2024-09-16)

okk looks like its take time

### bh...@gmail.com (2024-12-13)

hi any update ? 

### ap...@google.com (2024-12-19)

Project: chromium/src  

Branch: main  

Author: Lijin Shen <[lazzzis@google.com](mailto:lazzzis@google.com)>  

Link:      <https://chromium-review.googlesource.com/6102411>

[clank-q4-fixit] Disable touch when bottom sheet is animating

---


Expand for full commit details
```
[clank-q4-fixit] Disable touch when bottom sheet is animating 
 
Bug: 351564774 
Change-Id: I7f7b94f3b82945361bff8703d3e6fc5aa2cf9234 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6102411 
Reviewed-by: Matthew Jones <mdjones@chromium.org> 
Commit-Queue: Lijin Shen <lazzzis@google.com> 
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com> 
Cr-Commit-Position: refs/heads/main@{#1398821}

```

---

Files:

- M `chrome/android/expectations/lint-baseline.xml`
- M `components/browser_ui/bottomsheet/android/internal/BUILD.gn`
- M `components/browser_ui/bottomsheet/android/internal/java/src/org/chromium/components/browser_ui/bottomsheet/BottomSheet.java`
- D `components/browser_ui/bottomsheet/android/internal/java/src/org/chromium/components/browser_ui/bottomsheet/TouchRestrictingFrameLayout.java`
- M `components/browser_ui/bottomsheet/android/java/res/layout/bottom_sheet.xml`

---

Hash: 83df5710daca3a1fbdde22c0b9e5fde6cf8db81c  

Date:  Thu Dec 19 13:16:42 2024


---

### ap...@google.com (2024-12-27)

Project: chromium/src  

Branch: main  

Author: Lijin Shen <[lazzzis@google.com](mailto:lazzzis@google.com)>  

Link:      <https://chromium-review.googlesource.com/6125438>

Revert "[clank-q4-fixit] Disable touch when bottom sheet is animating"

---


Expand for full commit details
```
Revert "[clank-q4-fixit] Disable touch when bottom sheet is animating" 
 
This reverts commit 83df5710daca3a1fbdde22c0b9e5fde6cf8db81c. 
 
Reason for revert: crbug.com/385190306 
 
Original change's description: 
> [clank-q4-fixit] Disable touch when bottom sheet is animating 
> 
> Bug: 351564774 
> Change-Id: I7f7b94f3b82945361bff8703d3e6fc5aa2cf9234 
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6102411 
> Reviewed-by: Matthew Jones <mdjones@chromium.org> 
> Commit-Queue: Lijin Shen <lazzzis@google.com> 
> Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com> 
> Cr-Commit-Position: refs/heads/main@{#1398821} 
 
Bug: 351564774, 385571307, 385190306 
Change-Id: I0fc3b3a80ba0e943a251ef400b7dedb481e99067 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6125438 
Commit-Queue: Lijin Shen <lazzzis@google.com> 
Owners-Override: Lijin Shen <lazzzis@google.com> 
Reviewed-by: Wenyu Fu <wenyufu@chromium.org> 
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
Cr-Commit-Position: refs/heads/main@{#1400556}

```

---

Files:

- M `chrome/android/expectations/lint-baseline.xml`
- M `components/browser_ui/bottomsheet/android/internal/BUILD.gn`
- M `components/browser_ui/bottomsheet/android/internal/java/src/org/chromium/components/browser_ui/bottomsheet/BottomSheet.java`
- A `components/browser_ui/bottomsheet/android/internal/java/src/org/chromium/components/browser_ui/bottomsheet/TouchRestrictingFrameLayout.java`
- M `components/browser_ui/bottomsheet/android/java/res/layout/bottom_sheet.xml`

---

Hash: 34a5702d35bc66b7b7fad537800c8b4782c195be  

Date:  Fri Dec 27 11:55:26 2024


---

### bh...@gmail.com (2025-01-06)

hi any update ? 

### ap...@google.com (2025-01-10)

Project: chromium/src  

Branch: main  

Author: Lijin Shen <[lazzzis@google.com](mailto:lazzzis@google.com)>  

Link:      <https://chromium-review.googlesource.com/6127355>

[clank-q4-fixit] Fix TouchRestrictingFrameLayout not disabling touch

---


Expand for full commit details
```
[clank-q4-fixit] Fix TouchRestrictingFrameLayout not disabling touch 
 
When touch is disabled, both onInterceptTouchEvent and onTouchEvent 
should return true to prevent touch events from being consumed. 
 
This is the an alternative approach to crrev.com/c/6102411 which 
has been reverted. 
 
Bug: 351564774 
Change-Id: I4228146d13c7fd16f99631623c533fe20f0156b8 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6127355 
Reviewed-by: Wenyu Fu <wenyufu@chromium.org> 
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com> 
Commit-Queue: Lijin Shen <lazzzis@google.com> 
Reviewed-by: Matthew Jones <mdjones@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1405020}

```

---

Files:

- M `components/browser_ui/bottomsheet/android/internal/java/src/org/chromium/components/browser_ui/bottomsheet/BottomSheet.java`
- M `components/browser_ui/bottomsheet/android/internal/java/src/org/chromium/components/browser_ui/bottomsheet/TouchRestrictingFrameLayout.java`

---

Hash: 451e0c795b8f02415cec29e68400e46bbe435bec  

Date:  Fri Jan 10 14:30:44 2025


---

### pe...@google.com (2025-01-13)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### bh...@gmail.com (2025-01-14)

yea am waiting for the labels add to these ticket 

### am...@chromium.org (2025-01-14)

S3 issues should no longer require a `found in`, I've updated `found in` sincce that is the current oldest active release channel and given this bug was reported much earlier than that milestone

### bh...@gmail.com (2025-01-14)

what about the cve and reward ? .

### pe...@google.com (2025-01-14)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### am...@chromium.org (2025-01-14)

Decisions for potential VRP rewards are made only after the bug is resolved. [1] Since this bug was only resolved yesterday, it will be reviewed during a VRP Panel session at a further VRP Panel session.

CVEs are issued at the time a fix is released in a Stable channel update of Chrome. This fix was just landed in the 134 milestone. Fixes for low severity issues are not backmerged to other, earlier release channels of Chrome. So this fix will ship in the milestone release of 134, currently scheduled for 4 March 2025.

[1] <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#how-do-i-know-if-my-bug-report-is-possibly-eligible-for-a-vrp-reward>
[2] <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#how-do-i-know-if-my-bug-report-is-possibly-eligible-for-a-vrp-reward>

### bh...@gmail.com (2025-01-14)

actually there is no label of  reward top pannel  thats why i asked 

### bh...@gmail.com (2025-01-20)

any update on reward

### sp...@google.com (2025-01-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
low impact security UI issue 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-23)

Thank you for your efforts and reporting this issue to us.

### bh...@gmail.com (2025-01-23)

reward is little low acording to similar issues reward ? 

### bh...@gmail.com (2025-01-23)

Appeal reward reason: i u can see similar type vuln recived 2000 bounty and i got 500 atleast increase it to 1000 or 1500

### am...@chromium.org (2025-01-23)

The level of user interaction here was sufficiently high with a very low potential for user harm.
The linked bug was publicly available at the time of this report and this report does not demonstrate a similar impact.
Issues requiring significant user interaction with low to no reasonable potential for user harm may not be considered security bugs or eligible for a VRP rewards.
Because we were able to make a security relevant change here, we did want to acknowledge that with a small reward.

### bh...@gmail.com (2025-01-23)

okkk

On Fri, 24 Jan, 2025, 3:40 am , <buganizer-system@google.com> wrote:

> Replying to this email means your email address will be shared with the
> team that works on this product.
> https://issues.chromium.org/issues/351564774
>
> *Changed*
>
> *am...@chromium.org <am...@chromium.org> added comment #52
> <https://issues.chromium.org/issues/351564774#comment52>:*
>
> The level of user interaction here was sufficiently high with a very low
> potential for user harm. The linked bug was publicly available at the time
> of this report and this report does not demonstrate a similar impact.
> Issues requiring significant user interaction with low to no reasonable
> potential for user harm may not be considered security bugs or eligible for
> a VRP rewards. Because we were able to make a security relevant change
> here, we did want to acknowledge that with a small reward.
>
> _______________________________
>
> *Reference Info: 351564774 The PWA's installation dialog isn't being
> dismissed after redirects, which allows an attacker to sho*
> component:  Public Trackers > 1362134 > Chromium > UI > Browser > Mobile
> > Messages <https://issues.chromium.org/components/1457320>
> status:  Fixed
> reporter:  bharatadhikari008@gmail.com
> assignee:  la...@google.com
> cc:  bharatadhikari008@gmail.com, di...@chromium.org, dm...@chromium.org,
> and 7 more
> collaborators:  se...@chromium.org
> type:  Vulnerability
> access level:  Limited visibility
> priority:  P2
> severity:  S3
> found in:  130
> hotlist:  external_security_report
> <https://issues.chromium.org/hotlists/5433527>, reward-inprocess
> <https://issues.chromium.org/hotlists/5432630>, Security_Impact-Extended
> <https://issues.chromium.org/hotlists/5432548>
> retention:  Component default
> BuildNumber:  126.0.0.0
> Component Ancestor Tags:  UI, UI>Browser, UI>Browser>Mobile,
> UI>Browser>Mobile>Messages, UI>Browser>WebAppInstalls,
> UI>Browser>WebAppInstalls>Android
> Component Tags:  UI>Browser>Mobile>Messages,
> UI>Browser>WebAppInstalls>Android
> Fixed By Code Changes:
> https://chromium-review.googlesource.com/c/chromium/src/+/6127355
> OS:  Android
> vrp-reward:  500
>
>
> Generated by Google IssueTracker notification system.
>
> You're receiving this email because you are subscribed to updates on
> Google IssueTracker issue 351564774
> <https://issues.chromium.org/issues/351564774> where you have the roles:
> cc, reporter
> Unsubscribe from this issue.
> <https://issues.chromium.org/issues/351564774?unsubscribe=true>
>


### bh...@gmail.com (2025-02-25)

thanks for the reward for credit please put my name Bharat(mrnoob

### bh...@gmail.com (2025-03-05)

hey when willl cve will published for these issue and credit will come in ur releases

### ch...@google.com (2025-04-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### bh...@gmail.com (2025-06-27)

hey no cve for these issue ?

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/351564774)*
