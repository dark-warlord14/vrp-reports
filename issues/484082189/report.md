# Security Regression: Trusted UI (Omnibox) fails to render/disappears due to CoordinatorLayout migration logic failure.

| Field | Value |
|-------|-------|
| **Issue ID** | [484082189](https://issues.chromium.org/issues/484082189) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | Android |
| **Reporter** | mo...@gmail.com |
| **Assignee** | pn...@google.com |
| **Created** | 2026-02-13 |
| **Bounty** | $2,000.00 |

## Description

1. Executive Summary

A rendering regression was identified in Chromium for Android (arm64), causing the URL Bar (Omnibox) to disappear or render incorrectly when positioned at the bottom of the screen. The issue was introduced in Revision 1501003 during a structural migration of the toolbar container from OptimizedFrameLayout to CoordinatorLayout. This change conflicts with high-DPI resource handling on specific devices (e.g., Realme 12), leading to layout inflation errors and breaking the Trusted UI boundary.

2. Issue Description 

Affected Version: Chromium Builds starting from Revision 1501003.

Device Specifics: Verified on Realme 12 (Android 15), likely affects other high-DPI devices.

Trigger Condition: The issue manifests specifically when the "Bottom Toolbar" setting is enabled (or forced via flags), moving the URL bar to the bottom of the screen.

3. Bisect & Regression Range

Using manual binary search (bisect) on Android_Arm64 snapshots, the regression was isolated to a specific range:

Last Known Good Revision: 1500987

First Bad Revision: 1501016

Culprit Commit Position: refs/heads/main@{#1501003}

4. Identification of the Culprit

Commit Hash: e981dd46821f563acaa6a5a3d8fd51e046e311e2.

Title: [Toolbar] Rework hairline positioning.

Change Log: "Rework hairline positioning... This does require switching the toolbar container to be a CoordinatorLayout... Instead of manual manipulation."

5. Technical Root Cause Analysis

The root cause is a logic failure in how the new CoordinatorLayout handles the toolbar's vertical positioning compared to the previous FrameLayout implementation, specifically when interacting with high-density display resources.

A. Structural Change 
The culprit commit replaced the root container of the toolbar in control_container.xml:

Removed: org.chromium.components.browser_ui.widget.ViewResourceFrameLayout

Added: androidx.coordinatorlayout.widget.CoordinatorLayout

Additional Evidence in ToolbarControlContainer.java:
The file now explicitly casts layout params to CoordinatorLayout.LayoutParams in mutateLayoutParams(), confirming that the container strictly enforces the new layout hierarchy which fails to handle the Hi-DPI scaling correctly.

B. Logic Regression in ToolbarPositionController.java 
Upon inspecting the source code of ToolbarPositionController.java, specifically the updateCurrentPosition() method:

Removal of Explicit Offsets:
The legacy code used to manually calculate and set the Y-translation (setTranslationY) based on screen height and offsets. This guaranteed the view was placed within visible bounds.

Reliance on Gravity:
The new implementation relies entirely on CoordinatorLayout.LayoutParams and gravity anchors:
// Code Snippet from ToolbarPositionController.java (New Logic)
CoordinatorLayout.LayoutParams hairlineLayoutParams =
        mControlContainer.mutateHairlineLayoutParams();

// Logic relies solely on flipping gravity
hairlineLayoutParams.anchorGravity =
        newControlsPosition == ControlsPosition.TOP ? Gravity.BOTTOM : Gravity.TOP;

LayoutParams layoutParams = mControlContainer.mutateLayoutParams();
int verticalGravity =
        newControlsPosition == ControlsPosition.TOP ? Gravity.TOP : Gravity.BOTTOM;

layoutParams.gravity = Gravity.START | verticalGravity;

C. The Conflict
The reliance on Gravity.BOTTOM failed because of a preceding commit 1500950 (Enable hi-dpi resources).

The new Hi-DPI assets likely altered the measured height of the toolbar children.

CoordinatorLayout requires precise measurement passes (onMeasure). If the inner views (Omnibox icons) have mismatched dimensions due to the new resources, the CoordinatorLayout may calculate a zero height or push the view off-screen, whereas the old FrameLayout would have forced it to render regardless of measurement errors.

Security Impact Analysis:
According to Chrome's security guidelines, a UI spoof is critical if it "convinces the user they are currently on origin A when in fact they are on origin B".

This regression (caused by CoordinatorLayout migration) actively corrupts the primary 'Security Cue' (the Origin/URL text) that a "reasonable and prudent user" relies on.

Specifically, the failure in CoordinatorLayout to handle Hi-DPI measurements causes the domain text view to be shifted off-screen or rendered with incorrect padding, effectively truncating the origin or leaving the URL bar blank during keyboard interaction. This renders the domain unreadable, denying the user the ability to verify the origin and directly facilitating the criteria mentioned in your guidelines.

Unlike a design choice, this is a code failure in ToolbarPositionController.java that breaks the trusted UI boundary involuntarily.

7. Reproduction Steps 

Install Chromium Android_Arm64 build 1501016 (or any build after 1501003).

Launch the browser.

Navigate to chrome://flags or Settings.

Enable "Bottom Toolbar" (or Android Bottom Toolbar flag).

Relaunch the browser and open any webpage.

Tap on an input field to trigger the virtual keyboard.

Observation:
Upon triggering the virtual keyboard, the bottom-anchored Omnibox layout fails, causing the domain origin text to be either shifted off-screen, or rendered with zero height, making the origin unreadable.

8. Proposed Fix / Recommendation

To resolve this regression, the CoordinatorLayout implementation in ToolbarPositionController.java must account for the safe area insets and potential measurement discrepancies caused by Hi-DPI assets.

Immediate Mitigation: Revert commit e981dd4 to restore OptimizedFrameLayout stability.

Long-term Fix: Modify updateCurrentPosition() to ensure a minimum valid height is enforced and that layoutParams.bottomMargin correctly accounts for the device's navigation bar/gesture area when Gravity.BOTTOM is applied.


## Attachments

- [Github_Proof_IOS](attachments/Github_Proof_IOS) (image/png, 304.4 KB)
- [Github_Proof_Android.JPG](attachments/Github_Proof_Android.JPG) (image/jpeg, 73.3 KB)
- [DigitalOcean_Proof_IOS](attachments/DigitalOcean_Proof_IOS) (image/png, 502.8 KB)
- [DigitalOcean_Proof_Android.JPG](attachments/DigitalOcean_Proof_Android.JPG) (image/jpeg, 75.1 KB)
- [Chromium_Tracker_Proof_IOS](attachments/Chromium_Tracker_Proof_IOS) (image/png, 466.9 KB)
- [Chromium_Tracker_Proof_Android.JPG](attachments/Chromium_Tracker_Proof_Android.JPG) (image/jpeg, 51.8 KB)
- [Github_Proofs_Xiaomi.jpg](attachments/Github_Proofs_Xiaomi.jpg) (image/jpeg, 171.3 KB)
- [DigitalOcean_Proofs_Xiaomi.jpg](attachments/DigitalOcean_Proofs_Xiaomi.jpg) (image/jpeg, 332.8 KB)
- [Chromium_Proofs_Xiaomi.jpg](attachments/Chromium_Proofs_Xiaomi.jpg) (image/jpeg, 228.7 KB)
- [Github_Proofs_Xiaomi.png](attachments/Github_Proofs_Xiaomi.png) (image/png, 283.0 KB)
- [DigitalOcean_Proofs_Xiaomi.png](attachments/DigitalOcean_Proofs_Xiaomi.png) (image/png, 439.9 KB)
- [Chromium_Proofs_Xiaomi.png](attachments/Chromium_Proofs_Xiaomi.png) (image/png, 347.5 KB)
- [Poc1.jpeg](attachments/Poc1.jpeg) (image/jpeg, 71.9 KB)
- [Poc_Spoofing.mp4](attachments/Poc_Spoofing.mp4) (video/mp4, 1.5 MB)
- [poc_omnibox.html](attachments/poc_omnibox.html) (text/html, 2.0 KB)
- [poc_omnibox.html](attachments/poc_omnibox_74495630.html) (text/html, 4.6 KB)

## Timeline

### ma...@google.com (2026-02-13)

Security shepherd: Haven't tried reproducing this since it appears to depend on the device type, so labels provisional. I'm unsure whether we can consider this a security bug without seeing more of how this behaves in reality, but treating it as a Low Severity UI issue for now.

pnoland@, could you PTAL?

### pn...@google.com (2026-02-13)

I don't think this description, which is clearly AI-generated, is remotely correct in its analysis of the cause but the screenshots do show a UI issue. I will see if I can repro.

### mo...@gmail.com (2026-02-13)

Hi pnoland@,

You are absolutely right to question the initial analysis—I traced it statically without runtime debugging, so the specific code path regarding StatusMediator might be speculative.

However, the security impact is critical and reproducible.

The core issue is not just a UI glitch; the URL bar remains visible but displays blank (no domain text) or shows only 1-2 characters when text is pushed off-screen. This occurs when the keyboard appears in Bottom Toolbar mode

To Reproduce

Crucial: Enable "Address bar at bottom" in Settings (or via chrome://flags/#android-bottom-toolbar).

Open any HTTPS page (e.g., google.com).

Tap an input field -> Keyboard appears.

Observation: The URL bar remains visible but renders blank (no domain text displayed). In some cases, the domain text is pushed to the right edge, showing only 1-2 characters. This allows the page to display a fake URL bar in the empty space, spoofing the origin.

Thanks

### pn...@google.com (2026-02-13)

> The core issue is not just a UI glitch; the URL bar remains visible but displays blank (no domain text) or shows only 1-2 characters when text is pushed off-screen. *This occurs when the keyboard appears in Bottom Toolbar mode*

Emphasis mine: that's the thing, this isn't happening consistently in these conditions. I know this because I use https websites with the bottom toolbar every day and tested this feature consistently over the course of development and during the remediation of other, related vulnerabilities. There's some other variable affecting when this triggers. Can you confirm the specific device and chrome version you used to reproduce?

### mo...@gmail.com (2026-02-13)

Hi pnoland@,

Thanks for testing. Here are the exact specs where I consistently reproduce:

Device: Realme 12
Android Version: 15
Chrome Version: 144.0.7559.132 (Stable)- 147.0.7685.0(Canary)

### mo...@gmail.com (2026-02-13)

Additional proof:

Device: Xiaomi Redmi 13
Android: 15
Chrome: 144.0.7559.132 (Stable) - 147.0.7685.0(Canary)

Screenshots attached.

### mo...@gmail.com (2026-02-13)

Screenshots attached

### ch...@google.com (2026-02-14)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mo...@gmail.com (2026-02-14)

Hi pnoland

I admit I was premature in my initial assessment of Sections 5 and 8. I have re-evaluated the behavior to correct the record and isolate the actual root cause immediately, to save time and resources.

I have successfully isolated the exact trigger condition. This is an RTL (Right-to-Left) Layout Regression. The domain disappears from the bottom address bar only when the browser's user interface language is set to RTL (Arabic).

Updated Repro Steps:
1. Change Chrome language to Arabic.
2. Enable "Address bar at bottom".
3. Open any page (e.g., google.com).
4. Tap the input field.

Switching back to English (LTR) fixes the issue immediately. This confirms the regression is in the RTL handling logic of the new Toolbar container.

Please verify with an RTL locale.

Thanks

### mo...@gmail.com (2026-02-14)

I wanted to share a insight from my bisect analysis that might explain why this issue slipped

1. I confirmed via binary search (bisect) that this issue was introduced precisely in the commit that migrated the toolbar container from FrameLayout to CoordinatorLayout. Before this structural change, the Bottom Toolbar worked correctly in all locales.

2. (RTL + CoordinatorLayout):
The regression appears specific to how the new CoordinatorLayout handles layout mirroring in RTL (Right-to-Left) languages.
In summary, the switch to CoordinatorLayout inadvertently broke the RTL support for bottom-anchored elements, resulting in a persistent spoofing vector for Arabic users.
Thanks for your time reviewing this

### mo...@gmail.com (2026-02-17)

Just checking in to see if you needed any further details or logs regarding the RTL reproduction steps provided earlier.

Please let me know if there's anything else I can assist

Thanks

### pn...@google.com (2026-02-17)

Confirmed I can repro with RTL

### mo...@gmail.com (2026-02-25)

thanks for confirming reproduction in RTL.
I’m adding additional evidence to clarify exploitability and user impact beyond RTL truncation:
When Chrome UI locale is RTL and the on-screen keyboard is open (triggered by focusing a login input field), the mini origin bar truncation can hide the attacker-controlled registrable domain while leaving an attacker-chosen trusted-looking fragment visible (e.g., “google.com”, “paypal”, etc. depending on domain length).

### dx...@google.com (2026-02-27)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7610025>

[mobar] Fix RTL mobar animation

---


Expand for full commit details
```
     
    The starting position of the location bar is different for RTL, which 
    we need to account for when calculating the final translationX. 
     
    Bug: 484082189 
    Change-Id: I3ed5c3954c0e4c7a290936521ad2a101c42b7f14 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7610025 
    Reviewed-by: Sky Malice <skym@chromium.org> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1591207}

```

---

Files:

- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarController.java`
- M `chrome/browser/ui/android/toolbar/java/src/org/chromium/chrome/browser/toolbar/MiniOriginBarControllerTest.java`

---

Hash: [eaf32e20c8801aa6cc4494186fd4b2b2580aaa02](https://chromiumdash.appspot.com/commit/eaf32e20c8801aa6cc4494186fd4b2b2580aaa02)  

Date: Fri Feb 27 01:02:44 2026


---

### mo...@gmail.com (2026-02-27)

Thank you for the quick fix and your collaboration on resolving this issue

I have tested the latest update on Chrome version 147.0.7707.0 (1591213) , and I am no longer able to reproduce

### mo...@gmail.com (2026-02-27)

Fixed in Chrome Canary 147.0.7708.0  unable to reproduce

### mo...@gmail.com (2026-03-04)

Poc HTML file attached for reference

### mo...@gmail.com (2026-03-18)

I hope this finds you well. I am writing to respectfully follow up on the report currently pending the VRP panel's decision.
I sincerely appreciate the team's dedication and thank you for your continued efforts.

### mo...@gmail.com (2026-03-19)

I appreciate your patience with my follow ups. Please find attached a cleaner PoC for a more precise demonstration of the issue.

### mo...@gmail.com (2026-04-29)

Hello Google VRP Team,

I hope this message finds you well.

I'm writing to kindly follow up on this report. I noticed that the fix has been shipped in the stable release, and I wanted to check in to see if there are any updates regarding the reward decision

Thank you for your time and for the great work you do through the VRP program.

Best regards

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline, Security UI Spoofing


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### mo...@gmail.com (2026-05-19)

Dear Chrome VRP Panel,

Thank you for the reward and for reviewing this report.

I would like to respectfully request reconsideration based on a few points.

Regarding impact, this vulnerability enables three distinct attack scenarios:

1. The mobar appears completely blank, leaving the user with no visible origin indicator.
2. An attacker can overlay a fake mobar in the empty space and display any content they choose.
3. A long domain structured as google.com.attacker-domain.com causes the mobar to truncate and display only the trusted prefix, giving the user the impression they are on a legitimate origin.

Regarding comparable reports on the same surface:
Issue #438226517 required a multi-step gesture.
Issue #446463993 required the VirtualKeyboard API with precise timing.
Issue #461532432 required two taps.

The trigger here is a single tap on any standard input field with no special API or timing dependency.

Additionally, as noted at the beginning of the report, I was able to identify the exact culprit commit via git bisect, tracing the regression to the FrameLayout to CoordinatorLayout migration. I hope this contribution is taken into consideration, and I kindly ask the panel to reconsider the evaluation with this context in mind.

I appreciate your time and hope this context is useful in the evaluation.

### mo...@gmail.com (2026-05-19)

Please add this issue to the Security-VRP-Reassessment-Request hotlist (id:8186354).

### jd...@google.com (2026-05-26)

Hi mohamedhesham9173@gmail.com,

The panel reviewed your reassessment request and have decided to add an additional $1000 for the bisection you provided.

Thanks

### sp...@google.com (2026-05-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Reassessment resulted in an additional $1000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### mo...@gmail.com (2026-05-30)

Dear Chrome VRP Panel,

Thank you for the reassessment I'm glad the bisect contribution was recognized and reflected in the updated reward.

I would like to raise one final point respectfully. I believe the panel may have applied the updated guidelines announced in March, which set the base reward for S3 issues at $1,000, however this report was submitted and fixed before that policy was announced. Based on the Chrome VRP FAQ, reports are rewarded under the rules in effect at the time of submission, and I feel the panel may have overlooked this detail.

I would also like to note that similar reports on the same surface, such as issues #438226517, #446463993, and #461532432, were assessed at S2. I mention this only as context, and I leave the severity assessment entirely to the panel's judgment.

Would it be possible to request another reassessment based on this point?

Thank you for your time and consideration.

### aj...@google.com (2026-06-08)

(no need to re-add the hotlist when it is in reward-topanel)

### sp...@google.com (2026-06-08)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

bug; not web exploitable.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-06-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### [Deleted User] (2026-06-11)

deleted

### mo...@gmail.com (2026-06-11)

I appreciate the response, however I would like to respectfully note that this issue was previously rewarded, confirming it was assessed as a valid security vulnerability. The fix was also shipped in Chrome Canary 147.0.7708.0, which I verified personally.

The "not web exploitable" rationale appears inconsistent with the prior reward decision. Could the panel please clarify?

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484082189)*
