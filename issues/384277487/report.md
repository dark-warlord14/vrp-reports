# window.open doesn't correctly consume user gestures on IOS and Android

| Field | Value |
|-------|-------|
| **Issue ID** | [384277487](https://issues.chromium.org/issues/384277487) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>Mobile |
| **Platforms** | iOS |
| **Reporter** | el...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2024-12-15 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

Chrome restricts opening popups to trusted/active user gesture such as onclick event. Unless the user has explicitly allowed popups from a website, only 1 popup can be created for each user gesture. The gesture should be consumed by the popup opening action. 

This doesn't hold true on Google Chrome on IOS and on Android. On IOS, with 1 user gesture, infinite(?) number of popups can be created, while on Android -  2 popups. 

This mainly impacts user-experience and I'm fairly certain it's being somewhat abused by adware websites already (as I've seen a few websites create several popups from a single user gesture), but it also has certain security implications as it can be a powerful tool that makes certain client-side vulnerabilities easier to carry out and hide. It makes it possible to send 100s of top-level requests which is a powerful tool. 

VERSION
Chrome Versions: 
131.0.6778.134 IOS
131.0.6778.135 Android




REPRODUCTION CASE

An HTML file is attached. 

Otherwise you can visit https://jp3.eu/chrome_popups2.html where I have my payload. 

Clicking/touching once anywhere should spawn 2 popups on Android and over 100 on IOS.


CREDIT INFORMATION

Reporter credit: hakupiku

## Attachments

- chrome_popups2.html (text/html, 1.2 KB)
- crbug384277487.zip (application/zip, 101.6 KB)

## Timeline

### an...@chromium.org (2024-12-16)

[security shepherd]: Thank you for the report. Triaging this to [mustaq@chromium.org](mailto:mustaq@chromium.org) who may. have some expertise on this.

Hi [mustaq@chromium.org](mailto:mustaq@chromium.org), The window.open popup is restricted to two popups on Android, but on iOS it's over 100 per the user. Is this an intended behavior?

### mu...@chromium.org (2024-12-16)

This sounds bad for sure:

[a] Chrome on iOS uses WebKit (not Blink), but unlimited number of popups is a big issue. Chrome used to consume user activation at the browser process popup code, I am not sure why this is not working here.

[b] Two popups on Android is not great but not terrible either. I can reproduce this on Linux too.

[c] On Linux, I saw popups opening on `onfocus` (or a similar other) event without any user interaction on the page. I had difficulty getting rid of the repro page: every click on the tab to focus it opened two popup tabs and took focus away!

Bumping up the priority to P1 because both [a] and [c] look terrible.

### mu...@chromium.org (2024-12-16)

cc-ed [vmpstr@chromium.org](mailto:vmpstr@chromium.org) for prioritization.

### mu...@chromium.org (2024-12-16)

Assigning to [clamy@chromium.org](mailto:clamy@chromium.org) for prioritization and possibly some browser-side investigation (what changed there).

### pe...@google.com (2024-12-17)

Setting milestone because of s2 severity.

### pe...@google.com (2024-12-17)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-12-31)

clamy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2025-01-15)

clamy: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### el...@gmail.com (2025-01-28)

Hi,

I wanted to just update that, some websites are definitely abusing this in the wild. I just got 5 popups from clicking on a link in a website using Chrome on my Iphone. 




### cl...@google.com (2025-01-29)

Assigning this to cthomp who has more experience with UX for investigation.

### ct...@chromium.org (2025-01-29)

Digging into the iOS code, I think our browser-side popup blocking is limited by known upstream bugs in user gesture detection. See <https://source.chromium.org/chromium/chromium/src/+/main:ios/web/web_state/ui/crw_wk_ui_handler.mm;l=157;drc=69ad3067faf616b1618b4b49a1cf7fccb171dac2> (that feeds the `initiatedByUser` bit down to the code that checks if popups should be blocked and an infobar shown to the user [1](https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/web/model/web_state_delegate_browser_agent.mm;l=223;drc=69ad3067faf616b1618b4b49a1cf7fccb171dac2)). That code refers to [Issue 40561701](https://issues.chromium.org/issues/40561701) and an rdar filed with Apple. (This is all just based on spelunking in `ios/` code based on my middling understanding of how iOS Chrome is layered on top of WKWebView.)

Adding more iOS experts as I think the iOS bug here is the higher priority part of this report. gambard@ do you know who might be a good iOS owner for this, both to prod the Apple/WebKit bugs and to see if we can mitigate this on our end?

### ga...@google.com (2025-01-30)

Sadly I don't think there is much we can do here. Note that it also reproduce on Safari (with less tabs being opened but still > 1).
Olivier: could you take a look at the radar?
Mark: as lead for fundamentals.

### el...@gmail.com (2025-01-30)

It does reproduce on Safari but the issue seems somewhat different on Safari. On Safari, I haven't managed to get more than 3 popups, so it seems more like a race condition or a similar issue (it's always mousdown, mouseup, pointerdown, etc); At the very least the user gesture is consumed at some point, while it seems to me that Chrome on IOS doesn't consume the gesture at all?

Take a much simpler POC like this, which opens 10 popups on Chrome and only 1 on Safari :

```
<script>    
        for(let i=0; i<10;i++){
                window.addEventListener("click", e => window.open("https://google.com"))
        }
</script>

```

The issue that Safari has seems to be more similar to the one Chrome has on Android (2 popups).

What about the [comment #3](https://issues.chromium.org/issues/384277487#comment3) by [mustaq@chromium.org](mailto:mustaq@chromium.org) which says the POC page opens popups without user interaction on Linux. This is something I hadn't noticed myself.

### ol...@google.com (2025-01-30)

re #13: there is no activity on the radar since its creation in 2015.

### mi...@google.com (2025-01-31)

I did some investigation, here are some notes from it:

- Even with no injected JS, this still occurs so injection JS doesn't seem to be relevant.
- Every call to `BlockedPopupTabHelper::ShouldBlockPopup` returns Yes (CONTENT\_SETTING\_BLOCK is always returned from settings\_map->GetContentSetting) so some of these are not recognized as popups. (likely due to initiatedByUser == true)
- Many new windows are blocked, but there are always a group which get through for the initial touch on the page. For example, with one test with no injected JS, 308 new windows were blocked by `initiatedByUser` being false, but 7 were marked as `initiatedByUser`. Another test blocked 302 windows but 13 were opened. Similar numbers were observed after testing which injected JS.
- Each call where `initiatedByUser` is true will result in another new window being allowed/opened
- I tested on an iOS 16.4 simulator and the issue exists there as well. (More tabs were even opened in that case, about 32, tested on an iPad 10th Gen Sim)
- The windows are allowed during a 2 second period because of [this check](https://source.chromium.org/chromium/chromium/src/+/main:ios/web/web_state/user_interaction_state.mm;l=88?q=UserInteractionState::HasUserTappedRecently&ss=chromium%2Fchromium%2Fsrc) against `kMaximumDelayForUserInteraction`. This check is being hit every time until the 2 second timeout because `UserInteractionState::ResetLastTransferTime` takes longer than that to be called.
- Disabling `BetterUserGestureDetection` seems to have no effect so that logic may either be broken or unnecessary now.

Overall, the issue appears to be caused by this: The instance of `UserInteractionState` which gets the initial user touch never has `SetLastUserInteraction(nullptr)` called which is why it continues to be allowed to open additional tabs until the 2 second timeout.

I'll continue to explore why this is the case and if we should "consume" the touch either faster or after a specific number of windows have been opened. However, I do worry which real use cases could break here. For example, consider that a single click on a webpage could legitimately need to open more than a single window based on a single user click. Maybe we need to determine a specific limit or reduce the timeout? (Maybe Safari seems consistent in only opening 3 tabs because they have defined that as their upper limit?)

### mi...@google.com (2025-01-31)

In re-reading [#comment1](https://issues.chromium.org/issues/384277487#comment1), I was wondering about "Chrome restricts opening popups to trusted/active user gesture such as onclick event. Unless the user has explicitly allowed popups from a website, only 1 popup can be created for each user gesture. The gesture should be consumed by the popup opening action."

Do you know if this documented somewhere or is it based on testing / implementation?

### ct...@chromium.org (2025-01-31)

FYI window.open() is a generally treated as a [transient activation consuming API](https://developer.mozilla.org/en-US/docs/Web/Security/User_activation#transient_activation) although off-hand I'm not sure where/if this is explicitly specified in the HTML spec. I personally don't think we would have much risk of breaking non-abusive use cases if we consumed the user activation.

On Desktop/Android, Chrome will show a permission prompt to the user if a site tries to open more windows without an activation -- if that is granted then we disable the popup blocker.

### el...@gmail.com (2025-01-31)

Re: #17

I'm not sure where exactly it's documented, but I've found the implementation to be quite standard across browsers -- 1 popup per user gesture unless the user has granted permissions to the website to open windows without a trusted user gesture.

I'm quite certain websites are already adapted towards only 1 window opening from a single user click. The fact that you can open 3 windows on Safari is also most certainly a bug on Safari. (It also doesn't work on desktop)

### mi...@google.com (2025-02-05)

eldzey333@, I looked into this more and have a few more updates. There are many webkit bugs referencing window.open [for example](https://bugs.webkit.org/show_bug.cgi?id=283318). I also found a reference to a "Verify window.open user gesture" feature in [this bug](https://bugs.webkit.org/show_bug.cgi?id=274859), but it seems to be disabled in Safari desktop even though many windows do not open there.

I recommend that you file this directly against webkit with your PoC. The behavior seems very broken that the touch isn't consumed by window.open. (You can use the attached sample project in your report which is what I was using locally to test. It includes your PoC in a very simple WKWebView sample app.) A single click on the webpage leads to 188 requests to open new windows.

Separately, I'll keep looking into the logic in Chrome and see if I can consume the gesture on our side as a workaround.

### el...@gmail.com (2025-02-05)

#20 I'm reporting it to webkit now.

Am I allowed to make any reference to this report (considering its confidentiality)? I don't want to take credit for a sample app I didn't write myself so I want to mention that it was provided by the Google team.

### mi...@google.com (2025-02-05)

Yes, you can reference this report via URL like <http://crbug.com/384277487>. Additionally, you can say the sample project was provided by me in this bug and that we suggested you file it with WebKit directly. (Only folks listed on this bug will be able to see the content.)

For example, something like this:
"To ease testing, you can use the attached sample project, which was provided by a Chrome engineer in [crbug.com/384277487](https://crbug.com/384277487)"

You can also use my chromium account to CC me on the WebKit bug if you'd like. My chromium email is [michaeldo@chromium.org](mailto:michaeldo@chromium.org)

(Also, please share the webkit bug link here once filed even if you don't CC me.)

### el...@gmail.com (2025-02-05)

Filed at <https://bugs.webkit.org/show_bug.cgi?id=287101> and you should be CC-ed as well. Thanks.

### ap...@google.com (2025-02-06)

Project: chromium/src  

Branch: main  

Author: Mike Dougherty <[michaeldo@chromium.org](mailto:michaeldo@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6234612>

Opening a new window must consume the user interaction

---


Expand for full commit details
```
Opening a new window must consume the user interaction 
 
Fixed: 384277487 
Change-Id: I2ca328eb252f595a021c4f2763b0b824172b4233 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6234612 
Auto-Submit: Mike Dougherty <michaeldo@chromium.org> 
Reviewed-by: Sylvain Defresne <sdefresne@chromium.org> 
Commit-Queue: Sylvain Defresne <sdefresne@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1416798}

```

---

Files:

- M `ios/web/web_state/ui/crw_web_controller.mm`

---

Hash: fffafb04642de6923b068740eae1a52aceddffe8  

Date:  Thu Feb 06 07:55:06 2025


---

### mi...@google.com (2025-02-06)

I think we should merge this back to M134 since we just branched this week (and we are unlikely to get any feedback from canary/dev by letting this bake there.)

### pe...@google.com (2025-02-07)

**Merge approved:** your change passed merge requirements and is auto-approved for M134. Please go ahead and merge the CL to branch 6998 (refs/branch-heads/6998) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ap...@google.com (2025-02-07)

Project: chromium/src  

Branch: refs/branch-heads/6998  

Author: Mike Dougherty <[michaeldo@chromium.org](mailto:michaeldo@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6244899>

[M134] Opening a new window must consume the user interaction

---


Expand for full commit details
```
[M134] Opening a new window must consume the user interaction 
 
(cherry picked from commit fffafb04642de6923b068740eae1a52aceddffe8) 
 
Fixed: 384277487 
Change-Id: I2ca328eb252f595a021c4f2763b0b824172b4233 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6234612 
Auto-Submit: Mike Dougherty <michaeldo@chromium.org> 
Reviewed-by: Sylvain Defresne <sdefresne@chromium.org> 
Commit-Queue: Sylvain Defresne <sdefresne@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1416798} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6244899 
Commit-Queue: Mike Dougherty <michaeldo@chromium.org> 
Reviewed-by: Sergio Collazos <sczs@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6998@{#207} 
Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}

```

---

Files:

- M `ios/web/web_state/ui/crw_web_controller.mm`

---

Hash: 583cdadeefdec1c38866ad33fe0adc2d41451141  

Date:  Fri Feb 07 11:40:59 2025


---

### sp...@google.com (2025-02-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
for report of lower impact issue where the potential for user harm are more DOS / abuse side rather than potential for security harm; we were able to make a helpful change so the reward acknowledges that 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-14)

Thank you for your efforts, hakupiku, and reporting this issue to us.

### el...@gmail.com (2025-02-15)

Thanks for the reward!
Have a good weekend.
Cheers!

### am...@chromium.org (2025-03-04)

Updating this issue to reflect the low potential for security impact and the impact being more DOS / abuse related, which falls outside Chrome's threat model.

### ch...@google.com (2025-05-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/384277487)*
