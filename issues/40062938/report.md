# Security: Android permission prompt tapjacking

| Field | Value |
|-------|-------|
| **Issue ID** | [40062938](https://issues.chromium.org/issues/40062938) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Permissions>Prompts |
| **Platforms** | Android |
| **Reporter** | st...@gmail.com |
| **Assignee** | la...@chromium.org |
| **Created** | 2023-02-07 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The permission prompt UI on Android is not protected against subsequent taps.

If an attacker tricks the user into double-tapping on specific point on the screen (for example in a cookie clicker game), opening a permission prompt dialog will cause the user to inadvertantly tap the Allow button.

**VERSION**  

Chrome Version: 112.0.5579.0 + stable  

Operating System: Android 13

**REPRODUCTION CASE**

1. Open poc.html
2. Double-tap the cookie

**Possible fix (from the docs)** (docs/security/security-considerations-for-browser-ui.md):

> ### Introduce a short delay before the UI's call-to-action activates
> 
> If multiple clicks/gestures aren't feasible, consider introducing a short delay  
> 
> between when the browser UI is shown and the call-to-action activates. For  
> 
> example, if the user must click a button to grant a permission, introduce a  
> 
> delay before the button becomes active once the permission prompt is  
> 
> shown. Chrome uses short and long delays in various UI:
> 
> - For large security-sensitive browser surfaces like interstitials, three  
>   
>   seconds is typically considered a delay that is long enough to let the user  
>   
>   notice that the UI is showing without being too disruptive to the typical user  
>   
>   experience.
> - For smaller UI surfaces such as dialog boxes, a shorter delay like 500ms can  
>   
>   be more practical. `InputEventActivationProtector` is a helper class that ignores UI  
>   
>   events that happen within 500ms of the sensitive UI being displayed.

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [cookie.png](attachments/cookie.png) (image/png, 4.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 649 B)
- [poc.webm](attachments/poc.webm) (video/webm, 282.8 KB)
- [button-freeze.mp4](attachments/button-freeze.mp4) (video/mp4, 3.5 MB)

## Timeline

### [Deleted User] (2023-02-07)

[Empty comment from Monorail migration]

### fl...@google.com (2023-02-07)

Hi and thanks for the bug report!  I was able to reproduce this on my Android device.

battre@, I'm hoping you're at least a good starting place for assigning this bug.  It looks similar to crbug/1411524 to me, though I'm not familiar enough with this part of the codebase to mark it as a duplicate; it would be helpful to have your analysis of whether this is separate or the same root cause.  (And please reassign if you're not the right one for this.)

[Monorail components: UI>Browser]

### ba...@chromium.org (2023-02-07)

Balazs, do you still own permissions? Is this in your realm? For Autofill we introduced an artificial delay the user needs to wait between showing a suggestion and accepting it.

### en...@chromium.org (2023-02-07)

Thank you for routing, Dominic. Yes, my team has actually done quite a bit of work on the InputEventActivationProtector, which protects against this kind of click jacking on desktop. However, we have less experience with Android UI.

twellington@, I recall that pavely@ used to work on the system overlay detector logic (https://developer.android.com/topic/security/risks/tapjacking), but he seems to be working on something else now. Is there someone on your team who could pick up this work so that we have the same level of protections on Android as we do on desktop?

### tw...@chromium.org (2023-02-07)

This doesn't sound like an overlay protection problem but rather if you double click, the permission prompt is accepted... maybe we just need to enforce the permission dialog being on screen for a certain amount of time before the buttons respond.

Is there someone in Security UX who might be able to help advise?

[Monorail components: -UI>Browser UI>Browser>Permissions>Prompts]

### en...@chromium.org (2023-02-07)

Yeah, this is "temporal" click-jacking as opposed to spatial click-jacking that Pavel worked on. I am happy to advise (and review CLs) from the security UX side, I just don't have much Android-specific expertise.

### tw...@chromium.org (2023-02-07)

I'm wondering if we can have a UXer help inform the rules of how long content must be on screen before taps are accepted. Then it should be hopefully straight forward to code up :)

+Elvin -- not sure if there's any general Android UX guidance on this?

### en...@chromium.org (2023-02-07)

On desktop we use the double-click interval. On Android, we happen to have telemetry on reaction times on this exact UI [1] from an experiment where we compared cognitive load of various UIs. Based on that, the 500ms cutoff recommended by (our own) security guidelines seems to be a really good first approximation. Adding sereeena@ for additional thoughts.

[1]: https://uma.googleplex.com/p/chrome/timeline_v2?sid=77dbd1d787040ea4cd056bc13b06d76c

### tw...@chromium.org (2023-02-07)

Starting with 500ms sgtm!

@Lijin -- can you please look at updating the modal dialog APIs to support this for permission dialogs?

### [Deleted User] (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2023-02-09)

Should this delay be one-time for first time showing or also effective for the second time of showing? E.g. should we wait for 500ms again when users enter overview and then return to the page?

Screen record: waiting for 1000ms in this demo: https://drive.google.com/file/d/1Teea42yWqqjKPrw3Rupd8hBdXLhDJ-G_/view?usp=share_link&resourcekey=0-kPEoFW2N5PLaDFUQs9rkMw

### en...@chromium.org (2023-02-09)

Re: returning from overview, my thinking is that if the prompt was "glued" to the tab and it was visible in the thumbnail, we would not wait again. However, that does not seem to be the case. It is not shown in the thumbnail, and there is a roughly 0.5 second delay after the tab is shown again but before the prompt is shown again (with animation). A strategically placed button in the content area can still trick users into granting. Although I would classify this as very low risk, this is an edge case, so the potential risk of us breaking anything by adding the delay on subsequent impressions is also very low. TL;DR: I would apply the delay on every impression.

One thing that was not clear to me based on the video, just to make sure we are on the same page: we are disabling buttons for 500 ms _after_ the prompt is shown, and not delaying showing the prompt, right?

### la...@chromium.org (2023-02-09)

> we are disabling buttons for 500 ms _after_ the prompt is shown, and not delaying showing the prompt, right?

Ah, you are right! I misconfigured the dialog by delaying showing the prompt in the demo. Will show dialog at once but take 0.5s to allow button to be accepted.

### la...@chromium.org (2023-02-13)

[Comment Deleted]

### la...@chromium.org (2023-02-13)

Demo (extended to 1s for testing)

### gi...@appspot.gserviceaccount.com (2023-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/67b09985c3d5a7f9e6971e8e84c71797bfa72468

commit 67b09985c3d5a7f9e6971e8e84c71797bfa72468
Author: Lijin Shen <lazzzis@google.com>
Date: Thu Mar 02 19:10:26 2023

Disable permission dialog buttons for the initial 500ms.

This CL adds a new property in ModalDialog so that in the initial 500ms, none of the buttons does not accept any click event.

This change breaks many tests depending on permission dialog and so
this CL also adds a helper function to disable this feature in tests

Bug: 1413586
Change-Id: Id74344bc09c06f5828504cb0e6f503b84472053c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4242477
Reviewed-by: Bo Liu <boliu@chromium.org>
Reviewed-by: Balazs Engedy <engedy@chromium.org>
Reviewed-by: Theresa Sullivan <twellington@chromium.org>
Commit-Queue: Lijin Shen <lazzzis@google.com>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1112348}

[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/ModalDialogTestUtils.java
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/ModalDialogView.java
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/chrome/android/javatests/src/org/chromium/chrome/browser/permissions/PermissionTestRule.java
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/chrome/android/javatests/src/org/chromium/chrome/browser/notifications/NotificationTestRule.java
[add] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/features.h
[add] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/features.cc
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/permissions/android/java/src/org/chromium/components/permissions/PermissionDialogModel.java
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/AppModalPresenter.java
[add] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/ModalDialogFeatureList.java
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/BUILD.gn
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/weblayer/BUILD.gn
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/TabModalPresenter.java
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/ModalDialogViewTest.java
[add] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/modaldialog_feature_list.cc
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/chrome/browser/BUILD.gn
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/chrome/android/javatests/src/org/chromium/chrome/browser/incognito/IncognitoPermissionLeakageTest.java
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/ui/android/java/src/org/chromium/ui/UiUtils.java
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/components/browser_ui/modaldialog/android/java/src/org/chromium/components/browser_ui/modaldialog/ModalDialogViewBinder.java
[modify] https://crrev.com/67b09985c3d5a7f9e6971e8e84c71797bfa72468/ui/android/java/src/org/chromium/ui/modaldialog/ModalDialogProperties.java


### en...@chromium.org (2023-03-21)

stw.stw.tom@, the changes are live on Dev/Canary, could you please verify the mitigation?

### [Deleted User] (2023-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

[Empty comment from Monorail migration]

### st...@gmail.com (2023-03-23)

I can verify that the mitigation is applied on 113.0.5670.0

### am...@google.com (2023-03-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-30)

Congratulations, Thomas! The VRP Panel has decided to award you $2,000 for this report. We did not deduct any reward amount even though we all wanted cookies after assessing this report :D 
Thank you for your efforts and reporting this issue to us! 

### st...@gmail.com (2023-03-31)

Thanks, Amy! Sending some over :D

'🍪'.repeat(256)

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-27)

This issue was migrated from crbug.com/chromium/1413586?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062938)*
