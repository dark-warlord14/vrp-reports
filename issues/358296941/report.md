# UAF in NoPasskeysBottomSheetBridge::OnDismissed

| Field | Value |
|-------|-------|
| **Issue ID** | [358296941](https://issues.chromium.org/issues/358296941) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Passwords |
| **Platforms** | Android |
| **Reporter** | jt...@gmail.com |
| **Assignee** | fr...@chromium.org |
| **Created** | 2024-08-08 |
| **Bounty** | $36,000.00 |

## Description

VULNERABILITY DETAILS
On Android platform, a render process can call `ShowKeyboardReplacingSurface` to send a mojo message which instructs the browser to show a popup or accessory with password suggestions. On the browser side it calls to `TouchToFillController::Show` with the following sequence: (some of them run async)

ContentPasswordManagerDriver::ShowKeyboardReplacingSurface
  ChromePasswordManagerClient::ShowKeyboardReplacingSurface
    ChromePasswordManagerClient::MaybeShowAccountStorageNotice
      ChromePasswordManagerClient::ShowKeyboardReplacingSurfaceOnAccountStorageNoticeDone
        TouchToFillController::Show

And if there is no passkeys it then calls to `NoPasskeysBottomSheetBridge::Show`, which create a java object `NoPasskeysBottomSheetBridge(java)` [1]. The java object holds a native pointer to the C++ object `NoPasskeysBottomSheetBridge` [2], which is owned by `TouchToFillController`. When the frame is navigating away, `TouchToFillController` gets notified via WebContentsObserver and then reset the `NoPasskeysBottomSheetBridge` object [3]. During this process there is no code to notify the java side that `NoPasskeysBottomSheetBridge` is destroyed, which results in UAF when the native pointer is accessed through JNI call.

```
void Create(ui::WindowAndroid* window_android) override {      ==> [1]
  java_object_.Reset(Java_NoPasskeysBottomSheetBridge_Constructor(
      jni_zero::AttachCurrentThread(),
      reinterpret_cast<intptr_t>(bridge_.get()),
      window_android->GetJavaObject()));
}

NoPasskeysBottomSheetBridge(
        long nativeNoPasskeysBottomSheetBridge,
        WeakReference<Context> context,
        WeakReference<BottomSheetController> bottomSheetController) {
    mNativeBridge = nativeNoPasskeysBottomSheetBridge;      // ==> [2]
    mNoPasskeysSheet =
            new NoPasskeysBottomSheetCoordinator(context, bottomSheetController, this);
}

void TouchToFillController::OnDismiss() {
  view_.reset();
  no_passkeys_bridge_.reset();      // ==> [3]
  if (!ttf_delegate_) {
    // TODO(crbug.com/40274966): Remove this check when
    // PasswordSuggestionBottomSheetV2 is launched
    return;
  }
  // Unretained is safe here because TouchToFillController owns the delegate.
  ttf_delegate_->OnDismiss(base::BindOnce(
      &TouchToFillController::ActionCompleted, base::Unretained(this)));
}
```

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/password_manager/no_passkeys/android/no_passkeys_bottom_sheet_bridge.cc;l=25;drc=5203366d4cf174b9331ee33563e0520f10b60828
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/password_manager/no_passkeys/internal/android/java/src/org/chromium/chrome/browser/touch_to_fill/no_passkeys/NoPasskeysBottomSheetBridge.java;l=38;drc=5203366d4cf174b9331ee33563e0520f10b60828
[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/touch_to_fill/password_manager/touch_to_fill_controller.cc;l=188;drc=5203366d4cf174b9331ee33563e0520f10b60828

VERSION
Chrome Version: stable + dev
Operating System: Android

REPRODUCTION CASE
1. Apply the attached patch.diff, this is to simulate a compromised renderer

2. Host poc.html at localhost
python3 -m http.server 8000
adb reverse tcp:8000 tcp:8000

3. Launch asan build chromium on Android
out/Default/bin/chrome_public_apk run --args='--disable-features=PasswordSuggestionBottomSheetV2'

and navigate to http://localhost:8000/poc.html

Note that feature PasswordSuggestionBottomSheetV2 is disabled by default, but may be enabled on some custom builds. So we need to disable it explicitly here.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State: see asan.log for details

== ADDITIONAL INFO ==
compromised renderer requirement: yes
miracle ptr protected: no

Bisection:
This was introduced in https://chromium.googlesource.com/chromium/src/+/7aa06e75a81c6331613c36881da6cf3734a400d5

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 36.7 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 787 B)
- [poc.html](attachments/poc.html) (text/html, 691 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 3.8 MB)

## Timeline

### jt...@gmail.com (2024-08-08)

Upload a repro screen recording

### ts...@google.com (2024-08-08)

Setting provisional severity and found-in based on analysis, asan trace, and bisect while awaiting reproduction.

### ts...@google.com (2024-08-08)

Assigning per suspect CL, PTAL and re-assign as appropriate.

### ap...@google.com (2024-08-09)

Project: chromium/src
Branch: main

commit 3765f8e73a477b47daaf835a7ba74b8e205f63b6
Author: Friedrich Horschig <fhorschig@chromium.org>
Date:   Fri Aug 09 10:27:30 2024

    [Android][CredMan] Dismiss No-Passkeys sheet on destruction
    
    The dismissal is important to prevent the java bridge to call back into
    the c++ bridge after the latter has been destructed.
    
    Fixed: 358296941
    Change-Id: I74929725a88420ca4689ea0571b7e19cecbe814f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776745
    Reviewed-by: Timofey Chudakov <tchudakov@google.com>
    Commit-Queue: Friedrich Horschig <fhorschig@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1339553}

M       chrome/browser/touch_to_fill/password_manager/no_passkeys/android/no_passkeys_bottom_sheet_bridge.cc
M       chrome/browser/touch_to_fill/password_manager/no_passkeys/android/no_passkeys_bottom_sheet_bridge_unittest.cc

https://chromium-review.googlesource.com/5776745


### pe...@google.com (2024-08-09)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-08-09)

Requesting merge to extended stable (M126) because latest trunk commit (1339553) appears to be after extended stable branch point (1300313).
Requesting merge to stable (M127) because latest trunk commit (1339553) appears to be after stable branch point (1313161).
Requesting merge to beta (M128) because latest trunk commit (1339553) appears to be after beta branch point (1331488).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-08-10)

Merge review required: M128 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-08-10)

Merge review required: M127 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-08-10)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### fr...@chromium.org (2024-08-12)

1. The change is security-relevant for M126 and later. The UAF is accessible in M126 and later.
2. <https://chromium-review.googlesource.com/c/chromium/src/+/5776745>
3. Verified that the surface behaves as expected on 129.0.6652.0 which includes <https://chromium-review.googlesource.com/c/chromium/src/+/5776745>.
4. The issue is Finch-gated but 100% rolled out to all Android clients. Rolling back would mean loss of access to Passkeys.
6. It's not manually verifiable by the test team. (I.e. the absence of a UAF after closing the sheet.)

### am...@chromium.org (2024-08-12)

<https://crrev.com/c/5776745> approved for merge to M128; please merge this fix to branch 6613 immediately so this fix can be included in tomorrow's cut of M128 Early Stable

The final update of M127 Stable was already cut for release tomorrow and there are not further planned releases of M126 Extended, so no backmerges for M127 or M126 are needed

### ap...@google.com (2024-08-13)

Project: chromium/src
Branch: refs/branch-heads/6613

commit 853eb5a57c9b44e8c36067bbf24b04f7064c3cd3
Author: Friedrich Horschig <fhorschig@chromium.org>
Date:   Tue Aug 13 09:04:37 2024

    [M128][Android][CredMan] Dismiss No-Passkeys sheet on destruction
    
    The dismissal is important to prevent the java bridge to call back into
    the c++ bridge after the latter has been destructed.
    
    (cherry picked from commit 3765f8e73a477b47daaf835a7ba74b8e205f63b6)
    
    Fixed: 358296941
    Change-Id: I74929725a88420ca4689ea0571b7e19cecbe814f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5776745
    Reviewed-by: Timofey Chudakov <tchudakov@google.com>
    Commit-Queue: Friedrich Horschig <fhorschig@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1339553}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5785833
    Auto-Submit: Friedrich Horschig <fhorschig@chromium.org>
    Commit-Queue: Timofey Chudakov <tchudakov@google.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#985}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       chrome/browser/touch_to_fill/password_manager/no_passkeys/android/no_passkeys_bottom_sheet_bridge.cc
M       chrome/browser/touch_to_fill/password_manager/no_passkeys/android/no_passkeys_bottom_sheet_bridge_unittest.cc

https://chromium-review.googlesource.com/5785833


### sp...@google.com (2024-08-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

Rationale for this decision:
$35,000 for high quality report of non-mitigated memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-16)

Congratulations on another one, Rong! Very good finding and great work. Thank you for your efforts and reporting this issue to us -- nice work!

### jt...@gmail.com (2024-08-16)

Thank you Amy, as always for your quick response and kind support, cheers : )

### pe...@google.com (2024-11-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/358296941)*
