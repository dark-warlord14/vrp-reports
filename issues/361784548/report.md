# heap-use-after-free on media_router::MediaRouterDialogControllerAndroid::CancelPresentationRequest

| Field | Value |
|-------|-------|
| **Issue ID** | [361784548](https://issues.chromium.org/issues/361784548) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>PresentationAPI |
| **Platforms** | Android |
| **Chrome Version** | 127.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2024-08-23 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

repro:

1. apply patch.
2. host poc.html
3. click `presentationRequst.start()` button
4. wait tab close. then uaf.
   see mov.

# Problem Description

1. variant of pattern the [issue 358296941](https://issues.chromium.org/issues/358296941). there didn't dismiss view after `MediaRouterDialogControllerAndroid` destuct.

```
MediaRouterDialogControllerAndroid::~MediaRouterDialogControllerAndroid() {}

```

2. Then the java port exists a `raw pointer` to `MediaRouterDialogControllerAndroid`

```
public class BrowserMediaRouterDialogController implements MediaRouteDialogDelegate {
    private static final String MEDIA_ROUTE_CONTROLLER_DIALOG_FRAGMENT =
            "android.support.v7.mediarouter:MediaRouteControllerDialogFragment";

    private final long mNativeDialogController;
    private BaseMediaRouteDialogManager mDialogManager;
    private WebContents mWebContents;
-------------------------------------------------------------------------------------
MediaRouterDialogControllerAndroid::MediaRouterDialogControllerAndroid(
    WebContents* web_contents)
    : content::WebContentsUserData<MediaRouterDialogControllerAndroid>(
          *web_contents),
      MediaRouterDialogController(web_contents) {
  JNIEnv* env = base::android::AttachCurrentThread();
  java_dialog_controller_.Reset(Java_BrowserMediaRouterDialogController_create(
      env, reinterpret_cast<jlong>(this), web_contents->GetJavaWebContents()));

```

3. So if you call the JNI callback here after destruction, it will cause UAF

```
    @Override
    public void onSinkSelected(String sourceUrn, MediaSink sink) {
        mDialogManager = null;
        BrowserMediaRouterDialogControllerJni.get()
                .onSinkSelected(
                        mNativeDialogController,
                        BrowserMediaRouterDialogController.this,
                        sourceUrn,
                        sink.getId());
    }

    @Override
    public void onRouteClosed(String mediaRouteId) {
        mDialogManager = null;
        BrowserMediaRouterDialogControllerJni.get()
                .onRouteClosed(
                        mNativeDialogController,
                        BrowserMediaRouterDialogController.this,
                        mediaRouteId);
    }

    @Override
    public void onDialogCancelled() {
        // For MediaRouteControllerDialog this method will be called in case the route is closed
        // since it only call onDismiss() and there's no way to distinguish between the two.
        // Here we can figure it out: if mDialogManager is null, onRouteClosed() was called and
        // there's no need to tell the native controller the dialog has been cancelled.
        if (mDialogManager == null) return;

        mDialogManager = null;
        BrowserMediaRouterDialogControllerJni.get()
                .onDialogCancelled(
                        mNativeDialogController, BrowserMediaRouterDialogController.this);
    }

```

[0].<https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/browser/android/media_router_dialog_controller_android.cc;l=135;bpv=0;bpt=1>
[1].<https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/browser/android/java/src/org/chromium/components/media_router/BrowserMediaRouterDialogController.java;l=28?q=OnMediaSourceNotSupported&ss=chromium%2Fchromium%2Fsrc>
[2].<https://source.chromium.org/chromium/chromium/src/+/main:components/media_router/browser/android/java/src/org/chromium/components/media_router/BrowserMediaRouterDialogController.java;l=117?q=OnMediaSourceNotSupported&ss=chromium%2Fchromium%2Fsrc>

bitset: <https://source.chromium.org/chromium/chromium/src/+/52efd93fe1dee30d791a21f844b563fa4d375b50>

why need patch:
I don't have a device that my phone can scan, so I had to fake a few devices, but it seems that I didn't add them successfully. I originally wanted to trigger the `onSinkSelected` callback, but it seems that this works, and the patch does not affect the code logic.

# Summary

heap-use-after-free on media\_router::MediaRouterDialogControllerAndroid::CancelPresentationRequest

# Custom Questions

#### Type of crash:

browser

#### Crash state:

see asan.log

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- sym.log (text/plain, 774 B)
- poc.html (text/html, 218 B)
- mov.mp4 (video/mp4, 5.2 MB)
- [asan.log](attachments/asan.log) (text/plain, 24.1 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 3.4 KB)
- asan.log (text/plain, 58.1 KB)
- [sym-free.txt](attachments/sym-free.txt) (text/plain, 10.1 KB)
- [crash.txt](attachments/crash.txt) (text/plain, 16.9 KB)

## Timeline

### li...@gmail.com (2024-08-23)

sorry, forget to upload patch :

local version

```
> git log
  Use google_apis::AddDefaultAPIKeyToRequest() rather than manually setting key
    
  Bug: b/354922516, b/355544759
  Change-Id: I9751517085a81588201369aaf93

```

### li...@gmail.com (2024-08-23)

fix suggestions:
dismiss the view after class destroyed.

### ar...@chromium.org (2024-08-26)

*(security shepherd)*

Thanks! I hosted the reproducer on:
<https://nosy-thoughtful-snowplow.glitch.me/>
Unfortunately, I was unable to reproduce the issue. I attempted without ASAN, but couldn't build with it.

This would be a `MiraclePtr Status: NOT PROTECTED`, because we are referencing a C++ pointer from Java, and we aren't supporting this case with MiraclePtr.

[tguilbert@chromium.org](mailto:tguilbert@chromium.org) could you please take a look? Feel free to close as WorkAsIntended if the uploaded patch caused this.

If reproducible, this would be classified as Memory corruption in the browser process on Android: Critical severity.

I'll leave FoundIn unfilled until someone (tguilbert@ or the next security shepherd) can reproduce.

### tg...@chromium.org (2024-08-27)

=> mfoltz@, could you suggest someone who has more recently worked with this code? Feel free to reassign this to me if there isn't an obvious owner.

### li...@gmail.com (2024-08-27)

It seems that the asan.log I posted is a bit strange, I will re-upload it.

To repro, just set the timeout of the poc to 2000ms.

### mf...@chromium.org (2024-08-27)

Muyao, can you repro a browser crash using the PoC in [comment #4](https://issues.chromium.org/issues/361784548#comment4)? (See the video as well)

If so, I think calling CloseDialog() on the Java side in the dtor of the MediaRouterDialogControllerAndroid would be a potential fix; I can put up a speculative patch but am travelling and don't have a way to repro here or verify a fix.

### li...@gmail.com (2024-08-27)

symbol of free.

### pe...@google.com (2024-08-27)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mu...@google.com (2024-08-27)

I was able to reproduce the issue on Chrome stable 128.0.6613.88. It doesn't repro reliably though.

> I think calling CloseDialog() on the Java side in the dtor of the MediaRouterDialogControllerAndroid would be a potential fix

I will start working on it and verify if that fixes the issue.

### ti...@chromium.org (2024-08-27)

(security shepherd)

I was able to reproduce on an MTE enabled device on 127 reliably, attaching the stacktrace for posterity. Marking FoundIn-128. Keeping this as S1 due to the amount of user interaction required [1]

[1] <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md>

### mu...@google.com (2024-08-28)

CL waiting for review : <https://chromium-review.googlesource.com/c/chromium/src/+/5819835>

I tested it locally and this fix ensures that the device picker dialog is always closed after the page requesting to cast closes.

### pe...@google.com (2024-08-28)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-08-28)

Project: chromium/src
Branch: main

commit e51a64c9af60bddb50141a835ac32e061e81d25f
Author: Muyao Xu <muyaoxu@google.com>
Date:   Wed Aug 28 16:59:18 2024

    Close the Media Router device picker dialog on page closed
    
    The code to close the dialog on page destruction exists, but it failed
    to close the dialog because MediaRouteChooserDialogManager inaccurately
    shows the dialog has been closed, causing an early return in
    BrowserMediaRouterDialogController::closeDialog().
    
    This CL changes the controller to always close the dialog regardless of
    whether the dialog is showing or not.
    
    Bug: 361784548
    Change-Id: If94fa9fb60c9e691564a04630730dab4dbd2bf01
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5819835
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Commit-Queue: Muyao Xu <muyaoxu@google.com>
    Cr-Commit-Position: refs/heads/main@{#1348098}

M       components/media_router/browser/android/java/src/org/chromium/components/media_router/BrowserMediaRouterDialogController.java

https://chromium-review.googlesource.com/5819835


### mu...@google.com (2024-08-30)

Verified in the latest canary build 130.0.6687.0

### pe...@google.com (2024-08-31)

Security Merge Request Consideration: Requesting merge to stable (M128) because latest trunk commit (1348098) appears to be after stable branch point (1331488).
Security Merge Request Consideration: Requesting merge to beta (M129) because latest trunk commit (1348098) appears to be after beta branch point (1343869).
Security Merge Request - Manual Review: Merge review required: M128 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M129 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### mu...@google.com (2024-09-03)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/5819835>

2. Has this fix been verified on Canary to not pose any stability regressions?

Yes.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. Test steps:

0. Prerequisite: at least one cast device connected to the local network.
1. Visit <https://serve-dot-zipline.appspot.com/asset/61f0e78d-a346-519a-be3f-c50b0ed49259/zpc/q34hqvvlzvp/>
2. Click on the "play" button, then the "prompt" button to bring up the cast device selector dialog
3. Wait for about 5 seconds and the current tab should close.
4. Expected result: the cast device selector dialog also closes

### pg...@google.com (2024-09-03)

this fix has been in canary for a while, and I spot a few Dialog related crashes, but all were introduced before this fix landed. I do not see other stability issues that could be relevant to this fix (but please take another look at canary crashes to confirm!)

Merge approved for M128 - please merge to branch 6613 by Thursday September 5th EOD MTV time to get this fix into the next M128 stable respin!  

Merge approved for M129 - please merge to branch 6668 at your earliest convenience to get this fix into the next M129 beta release!

### ap...@google.com (2024-09-04)

Project: chromium/src
Branch: refs/branch-heads/6668

commit 739d3fc4830cf25624ba619d0612b4404253c861
Author: Muyao Xu <muyaoxu@google.com>
Date:   Wed Sep 04 02:38:34 2024

    [M129] Close the Media Router device picker dialog on page closed
    
    The code to close the dialog on page destruction exists, but it failed
    to close the dialog because MediaRouteChooserDialogManager inaccurately
    shows the dialog has been closed, causing an early return in
    BrowserMediaRouterDialogController::closeDialog().
    
    This CL changes the controller to always close the dialog regardless of
    whether the dialog is showing or not.
    
    (cherry picked from commit e51a64c9af60bddb50141a835ac32e061e81d25f)
    
    Bug: 361784548
    Change-Id: If94fa9fb60c9e691564a04630730dab4dbd2bf01
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5819835
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Commit-Queue: Muyao Xu <muyaoxu@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1348098}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5834036
    Commit-Queue: Ahmed Moussa <ahmedmoussa@google.com>
    Reviewed-by: Ahmed Moussa <ahmedmoussa@google.com>
    Auto-Submit: Muyao Xu <muyaoxu@google.com>
    Cr-Commit-Position: refs/branch-heads/6668@{#823}
    Cr-Branched-From: 05bc664984ca075216b7f2198c88b9725bfa1b9b-refs/heads/main@{#1343869}

M       components/media_router/browser/android/java/src/org/chromium/components/media_router/BrowserMediaRouterDialogController.java

https://chromium-review.googlesource.com/5834036


### ap...@google.com (2024-09-04)

Project: chromium/src
Branch: refs/branch-heads/6613

commit 3a47911f2108f5b362dc2321149fe47986aadd65
Author: Muyao Xu <muyaoxu@google.com>
Date:   Wed Sep 04 02:48:11 2024

    [M128] Close the Media Router device picker dialog on page closed
    
    The code to close the dialog on page destruction exists, but it failed
    to close the dialog because MediaRouteChooserDialogManager inaccurately
    shows the dialog has been closed, causing an early return in
    BrowserMediaRouterDialogController::closeDialog().
    
    This CL changes the controller to always close the dialog regardless of
    whether the dialog is showing or not.
    
    (cherry picked from commit e51a64c9af60bddb50141a835ac32e061e81d25f)
    
    Bug: 361784548
    Change-Id: If94fa9fb60c9e691564a04630730dab4dbd2bf01
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5819835
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Mark Foltz <mfoltz@chromium.org>
    Commit-Queue: Muyao Xu <muyaoxu@google.com>
    Cr-Original-Commit-Position: refs/heads/main@{#1348098}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5834723
    Auto-Submit: Muyao Xu <muyaoxu@google.com>
    Reviewed-by: Ahmed Moussa <ahmedmoussa@google.com>
    Commit-Queue: Ahmed Moussa <ahmedmoussa@google.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#1542}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       components/media_router/browser/android/java/src/org/chromium/components/media_router/BrowserMediaRouterDialogController.java

https://chromium-review.googlesource.com/5834723


### sp...@google.com (2024-09-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for report of a highly mitigated security bug in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-04)

Congratulations lime! The reward amount was determined to be mildy mitigated based on preconditions for user activation and/or UI interaction required to trigger this issue. Thank you for your efforts and reporting this issue to us.

### li...@gmail.com (2024-09-05)

Thanks, Amy. :)

### pe...@google.com (2024-12-07)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/361784548)*
