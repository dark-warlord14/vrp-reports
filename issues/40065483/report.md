# Security: Possible Tapjacking PWA Installation in Android Chrome.

| Field | Value |
|-------|-------|
| **Issue ID** | [40065483](https://issues.chromium.org/issues/40065483) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>WebAppInstalls>Android |
| **Platforms** | Android |
| **Reporter** | fa...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2023-06-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Android Chrome's PWA installation prompt is vulnerable to tapjacking. Therefore, an attacker could create an engaging game to lure victims into unknowingly downloading a PWA app without reading the prompt. As a result, a phishing app is created on the victim's phone without their knowledge.

**VERSION**  

Chrome Version: Chrome Dev 116.0.5803.0  

Operating System: Android 13

**REPRODUCTION CASE**

1. Download poc.zip and extract the files to a folder.
2. Host the files to a HTTPS site.
3. Open the Chrome browser on your Android device and navigate to the site at https://{YOUR-SITE}/poc.html to begin testing.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 2.5 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 2.1 MB)
- [pwa.png](attachments/pwa.png) (image/png, 20.3 KB)
- [chrome-desktop-pwa.mp4](attachments/chrome-desktop-pwa.mp4) (video/mp4, 240.9 KB)
- [app.js](attachments/app.js) (text/plain, 465 B)
- [app.webmanifest](attachments/app.webmanifest) (application/octet-stream, 704 B)
- [dummy-sw.js](attachments/dummy-sw.js) (text/plain, 156 B)
- [phishing.html](attachments/phishing.html) (text/plain, 1.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [chrome permission.mp4](attachments/chrome permission.mp4) (video/mp4, 909.8 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.6 MB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.6 MB)

## Timeline

### fa...@gmail.com (2023-06-07)

[Comment Deleted]

### [Deleted User] (2023-06-07)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-06-07)

From my testing, the desktop version of Chrome's PWA installation prompt has a safeguard method against clickjacking attacks. However, the Android version of this prompt lacks such a safeguard, making it vulnerable to tapjacking.

A solution would be to introduce a delay after taps between the DOM and the download button. On desktop, a similar safeguard is implemented to protect against Clickjacking, but it is missing on Android.

### fa...@gmail.com (2023-06-07)

You can modify the CSS values of top and left within the #redBox of poc.html to adjust the coordinates (top, left) to align with the buttons.

### aj...@google.com (2023-06-07)

Hi - please attach any poc files as individual files - not as a .zip

### fa...@gmail.com (2023-06-08)

I apologize. Here are the individual files used as proof-of-concept for this report.

### [Deleted User] (2023-06-08)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2023-06-08)

Thanks - sending to the team to take a look.

[Monorail components: UI>Browser>WebAppInstalls>Android]

### [Deleted User] (2023-06-08)

[Empty comment from Monorail migration]

### do...@chromium.org (2023-06-09)

Moving to the MWI team.

### [Deleted User] (2023-06-09)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ei...@chromium.org (2023-06-15)

unassign myself to put back to triage queue. I don't think I'll have time to work on this in the next few months.

### aj...@google.com (2023-06-15)

Hi  - security issues should have owners - please assign to someone that can make progress.

### fi...@chromium.org (2023-06-21)

This looks related to the work meacer@ did on the InputEventActivationProtector.
https://chromium-review.googlesource.com/c/chromium/src/+/1686858

Mustafa, was there any design thoughts/work done for Android as well? 

### fa...@gmail.com (2023-06-22)

The Chrome permission dialogue for Android has protection against tapjacking, whereas the PWA Installation Dialog lacks it.

### fi...@chromium.org (2023-06-22)

Yes. Unfortunately, fixes usually don't apply across products (different code base, etc).

### me...@chromium.org (2023-06-22)

Finnur: Unfortunately, no. Android required a totally different implementation due to Java bits, so I didn't work on it at the time. It shouldn't be too difficult to port it though, if anyone is interested. 

### fi...@chromium.org (2023-06-23)

Thanks for the reply, Mustafa. 

I suspected as much, but am curious as to whether the approach for Android was given any thought -- or if you have thoughts now.

Because I don't suppose there is a double-click value in the Android OS, like on Desktop, so would the approach be to just wait to enable the Install 500 ms button for 500 ms (and perhaps reset the timer on each tap)?

### fi...@chromium.org (2023-06-23)

Oops, I accidentally managed to slip in one case of a redundant "500 ms" in that last sentence. 

The user will just have to wait a whole second before clicking the button... ;)    jk

### fa...@gmail.com (2023-06-24)

Thanks for reviewing this issue. I believe the security severity is being underestimated. This vulnerability is more significant than the bug reported on crbug.com/1404230 (medium), and it can be exploited with minimum user awareness.

I look forward to your response. Have a nice day :)



### fa...@gmail.com (2023-06-24)

I have created a live proof-of-concept based on my report, which demonstrates the entire attack method. It shows how an attacker controled website can lure the victim into unknowingly installing a malicious Progressive Web App. This PWA can then be used for phishing or other types of attacks.

Live POC: https://fazim-pentest.000webhostapp.com/PWA/poc.html

### me...@chromium.org (2023-06-24)

> Because I don't suppose there is a double-click value in the Android OS, like on Desktop, so would the approach be to just wait to enable the Install 500 ms button for 500 ms (and perhaps reset the timer on each tap)?

Yeah, I think ignoring double clicks is reasonable and we can keep it simple on Android. Also, I think we shouldn't be limited by the 500ms. Given that this is a high risk button, I think 1 second or even multiple seconds of delay is reasonable. This UI should be rare enough for this to not be a problem.

### fi...@chromium.org (2023-07-04)

I can take a look.

### ei...@chromium.org (2023-07-04)

Thank you Finnur!

### fi...@chromium.org (2023-07-04)

It seems that the precedent here is to use PROMPT_INPUT_PROTECTION_SHORT_DELAY_MS, which is only 600ms long.

This does not seem long enough to me, as it only realistically prevents the first couple of clicks in a click sequence after the dialog is shown. I think we need to reset the timer on each check, like we do on Desktop [1].

I'm going to make that change [2] on Android as well, since it protects against both double-clicking and repeated clicks.


[1] https://source.chromium.org/chromium/chromium/src/+/main:ui/views/input_event_activation_protector.cc;l=63

[2] https://chromium-review.googlesource.com/c/chromium/src/+/4664276


### tw...@chromium.org (2023-07-05)

Looping in Lijin who landed the current protection in crrev.com/c/4242477.

The current timeout value is from a suggestion here: https://bugs.chromium.org/p/chromium/issues/detail?id=1413586#c8 which said "On desktop we use the double-click interval. On Android, we happen to have telemetry on reaction times on this exact UI [1] from an experiment where we compared cognitive load of various UIs. Based on that, the 500ms cutoff recommended by (our own) security guidelines seems to be a really good first approximation. Adding sereeena@ for additional thoughts.

[1]: https://uma.googleplex.com/p/chrome/timeline_v2?sid=77dbd1d787040ea4cd056bc13b06d76c"

### gi...@appspot.gserviceaccount.com (2023-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/35f44be58cae5ee13b8748f480b842c317b3fffb

commit 35f44be58cae5ee13b8748f480b842c317b3fffb
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Thu Jul 06 11:53:10 2023

[Android] Add a delay to webapp install button accept

This adds a short delay before buttons in the
Add to Homescreen/Install webapp dialog accept
clicks.

It also adds tracking for multiple clicks to
mirror the behavior on the Desktop side, as
per input_event_activation_protector.cc.

Bug: 1452230
Change-Id: I44d5df24659f9438528c766fe1c0058ea597369b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4664276
Reviewed-by: Lijin Shen <lazzzis@google.com>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Ella Ge <eirage@chromium.org>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1166456}

[modify] https://crrev.com/35f44be58cae5ee13b8748f480b842c317b3fffb/components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/ModalDialogView.java
[modify] https://crrev.com/35f44be58cae5ee13b8748f480b842c317b3fffb/components/webapps/browser/android/java/src/org/chromium/components/webapps/AddToHomescreenDialogView.java
[modify] https://crrev.com/35f44be58cae5ee13b8748f480b842c317b3fffb/components/webapps/browser/android/BUILD.gn


### fi...@chromium.org (2023-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### ei...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### ei...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### fi...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-11)

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/67025495bfc1081c95ef21c3745a260a5a65843a

commit 67025495bfc1081c95ef21c3745a260a5a65843a
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Wed Jul 12 00:06:24 2023

[Android] Add a delay to webapp install button accept

This adds a short delay before buttons in the
Add to Homescreen/Install webapp dialog accept
clicks.

It also adds tracking for multiple clicks to
mirror the behavior on the Desktop side, as
per input_event_activation_protector.cc.

(cherry picked from commit 35f44be58cae5ee13b8748f480b842c317b3fffb)

Bug: 1452230
Change-Id: I44d5df24659f9438528c766fe1c0058ea597369b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4664276
Reviewed-by: Lijin Shen <lazzzis@google.com>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
Reviewed-by: Ella Ge <eirage@chromium.org>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1166456}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4677337
Cr-Commit-Position: refs/branch-heads/5845@{#428}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/67025495bfc1081c95ef21c3745a260a5a65843a/components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/ModalDialogView.java
[modify] https://crrev.com/67025495bfc1081c95ef21c3745a260a5a65843a/components/webapps/browser/android/java/src/org/chromium/components/webapps/AddToHomescreenDialogView.java
[modify] https://crrev.com/67025495bfc1081c95ef21c3745a260a5a65843a/components/webapps/browser/android/BUILD.gn


### am...@chromium.org (2023-07-17)

Hi finnur@ thanks for resolving this issue so quickly. For future reference, low severity security bugs should not be backmerged. Sheriffbot auto-approved it based on timing, so I see it's already been merged. That's fine, but please try to avoid this for future reference, especially for bugs specific to Android. 

### fa...@gmail.com (2023-07-18)

Hi again, there hasn't been an update on severity after https://crbug.com/chromium/1452230#c21. This is the simplest of tapjacking, where a double tap an attacker site can install web apps on a user's phone without the user's knowledge. Additionally, these web apps lack an origin indicator, which is present in desktop PWAs. As a result, it becomes easy to create a clone of another app with a logo and UI that are indistinguishable from a legitimate user app (see https://crbug.com/chromium/1452230#c21 demo). Could you please reevaluate the severity? This issue deserves at least a medium severity rating.

### am...@chromium.org (2023-08-10)

Thank you for this report. The severity has gone unchanged since c#21 because this does issue does not appear to have any security consequences. The permission being granted simply allows for a PWA install, which on its own does not grant any particular permissions or privilege that would put a user at risk. In VRP assessment, we have decided that this permission on its own it's not especially consequential to security and this issue should not be a considered a security bug. 
As such, this report is unfortunately not eligible for a VRP reward. 

### am...@chromium.org (2023-08-10)

[Empty comment from Monorail migration]

### fa...@gmail.com (2023-08-11)

Hi, in Android PWAs, the address bar is not shown. As a result, it becomes easy to create a clone of another app with identical logos and UI, making it indistinguishable from a legitimate user app. This can be used to harvest sensitive information by presenting it as a user app.

### fa...@gmail.com (2023-08-11)

Please watch this demo, with a focus on the final video that demonstrates a PWA app without any address bar.

### am...@chromium.org (2023-08-11)

Thank for reaching out, thanks for taking the extra steps to demonstrate this issue. We're happy to re-review and will discuss as a team next week. Thank you for your patience in the interim. 

### am...@chromium.org (2023-08-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-16)

Thank you for your newest POC to demonstrate this issue. We have decided to award you $1,000 for demonstrating the highest potential abuse of this issue. The reward amount was decided on based on that the user would see a new app and recognize it should not be there and easily delete it. Also, if the user did notice the installation prompt it does display the correct origin. Thank you for your efforts and reporting this issue to us! 

### fa...@gmail.com (2023-08-16)

Yes, the user may see it, but if they double-tap the PoC the dialog without the clickjack protection, the dialog will close quickly with approval, and the user could be unaware of the origin. Additionally, the installed apps can also be different, such as a pro version of the app or free subscriptions/rewards app for phishing. 

Thank you for fixing the issue, and thank you for reconsidering and rewarding me for my work.

### fi...@chromium.org (2023-08-17)

@amyressler (https://crbug.com/chromium/1452230#c36): I see this issue has been upped in priority, so the point is now moot, but I'll try to remember your guidance in the future. I would point out, though, that the fix I backmerged also added extra protection for the issue described in https://crbug.com/chromium/1413586, which involves Android permissions, such as Location and Camera -- so the issue was perhaps slightly more important than the labeling made it seem like. 

### am...@google.com (2023-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2024-01-24)

Appeal reward reason: Hi, I feel that my vulnerability was not fully awarded when reading crbug.com/1442018, which is very similar to an issue involving a long press of 'Enter' compared to mine on Android with a double tap, functioning as clickjacking. I believe I deserve an additional 500 since I only received a bounty of 1000, in contrast to a similar issue mentioned above, which received 1500 on Windows. Usually, Android Chromium is more widely used compared to the desktop, and the advantage of my vulnerability, as seen in this video: https://bugs.chromium.org/p/chromium/issues/detail?id=1452230#c41 (Explanation: https://bugs.chromium.org/p/chromium/issues/detail?id=1452230#c40), is that it almost acts as a clone of the app on Android, while the desktop version usually shows the origin, making it more effective.

### am...@chromium.org (2024-01-24)

The $500 difference in reward amounts in comparison to the similar report of https://crbug.com/chromium/1442018 was due to the other reporting receiving a $500 bisect bonus. They achieved this bisect bonus by clearly explaining and demonstrating the issue on all the active release channels at the time of the report. Please see https://g.co/chrome/vrp/#bisect-bonus for more information. 
Based on this information and explanation, we'll need to politely decline the appeal / reassessment request in https://crbug.com/chromium/1452230#c49. 

### is...@google.com (2024-01-24)

This issue was migrated from crbug.com/chromium/1452230?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1463095, crbug.com/chromium/1463251]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065483)*
