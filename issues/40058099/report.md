# Security: UAF in ScreenCaptureMachineAndroid::OnActivityResult

| Field | Value |
|-------|-------|
| **Issue ID** | [40058099](https://issues.chromium.org/issues/40058099) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia, Internals>Media>ScreenCapture |
| **Platforms** | Android |
| **Reporter** | jt...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2021-12-02 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

The Java object ScreenCapture takes a raw pointer nativeScreenCaptureMachineAndroid in the constructor and stores it as a member [1].

```
ScreenCapture(long nativeScreenCaptureMachineAndroid) {  
    mNativeScreenCaptureMachineAndroid = nativeScreenCaptureMachineAndroid; // ===> [1]  
}  

```

While starting screen capture on Android, it will first show a prompt by calling startActivityForResult [2] and get the result in function onActivityResult, in which the native pointer is used for JNI call [3]. However, a UAF would occur if the c++ object ScreenCaptureMachineAndroid that the pointer refers to has been freed before the prompt activity is closed.

```
@CalledByNative  
public boolean startPrompt() {  
    // skip...  
    try {  
        startActivityForResult(   // ===> [2]  
                mMediaProjectionManager.createScreenCaptureIntent(), REQUEST_MEDIA_PROJECTION);  
    } catch (android.content.ActivityNotFoundException e) {  
        Log.e(TAG, "ScreenCaptureException " + e);  
        return false;  
    }  
    return true;  
}  
  
@Override  
public void onActivityResult(int requestCode, int resultCode, Intent data) {  
    // skip...  
    ScreenCaptureJni.get().onActivityResult(mNativeScreenCaptureMachineAndroid,  // ===> [3]  
            ScreenCapture.this, resultCode == Activity.RESULT_OK);  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:media/capture/content/android/java/src/org/chromium/media/ScreenCapture.java;l=94;drc=32f574f6df1d37b0d9ed765fe138270414d79e49>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:media/capture/content/android/java/src/org/chromium/media/ScreenCapture.java;l=276;drc=32f574f6df1d37b0d9ed765fe138270414d79e49>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:media/capture/content/android/java/src/org/chromium/media/ScreenCapture.java;l=294;drc=32f574f6df1d37b0d9ed765fe138270414d79e49>

**VERSION**  

Chrome Version: 96.0.4664.45 (stable) + dev  

Operating System: Android

**REPRODUCTION CASE**

1. Setup a local HTTP server  
   
   python -m SimpleHTTPServer 8000
2. Create a port forwarding from Android device to the local machine  
   
   adb reverse tcp:8000 tcp:8000
3. Run following command to launch asan build chrome on Android  
   
   out/Default/bin/chrome\_public\_apk run --args='--enable-features=UserMediaScreenCapturing'

and navigate to <http://localhost:8000/poc.html>

4. Click the 'Allow' button that appears at the bottom of the page.
5. Wait for about 5 seconds (to free ScreenCaptureMachineAndroid object) and click the 'CANCEL' button on the prompt.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 336 B)
- [asan.log](attachments/asan.log) (text/plain, 8.9 KB)

## Timeline

### [Deleted User] (2021-12-02)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-12-02)

alcooper@: can you please take a look at this? Feel free to re-assign as needed, but I think you're at least in the right ballpark.

I'm rating this as a high severity vulnerability, since it is a use-after-free in the browser process that can be triggered from the web, but requires nontrivial user interaction. Because UserMediaScreenCapturing doesn't look to be enabled anywhere, though, it's Impact-None. (This bug should be blocking for any UserMediaScreenCapturing rollout.)

[Monorail components: Blink>GetUserMedia]

### al...@chromium.org (2021-12-02)

That's correct, it's not currently enabled anywhere to my knowledge. I believe this is fixable by having the native object notify the Java object on it's destruction, as this seems like a pattern I've seen before.

[Monorail components: Internals>Media>ScreenCapture]

### gi...@appspot.gserviceaccount.com (2021-12-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f9daf45b5563540323451b937315781fde75510f

commit f9daf45b5563540323451b937315781fde75510f
Author: Alexander Cooper <alcooper@chromium.org>
Date: Fri Dec 03 02:25:21 2021

Notify Android ScreenCapture when native capturer is destroyed

The Java ScreenCapture class causes a system prompt to appear; however,
it is possible for the underlying native object to have been destroyed
while waiting for a response to this system prompt (due to e.g. a timed
reload/navigation). In this case, we shouldn't try to call back to the
native class, and should just bail out.

This causes the native object to notify the corresponding Java object
when it is destroyed so that the java object will no longer attempt to
notify the native object that the prompt has been answered.

The ScreenCaptureMachineAndroid is owned by the
ScreenCaptureDeviceAndroid which guarantees that capture will be stopped
before the ScreenCaptureMachineAndroid is destroyed, thus we do not need
check that the ScreenCaptureMachineAndroid pointer stays valid while
actively performing capture.

Fixed: 1275892
Change-Id: I71978f00448a339fcb20cfeadd421542507d47ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3312596
Commit-Queue: Alexander Cooper <alcooper@chromium.org>
Auto-Submit: Alexander Cooper <alcooper@chromium.org>
Reviewed-by: Mark Foltz <mfoltz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#947840}

[modify] https://crrev.com/f9daf45b5563540323451b937315781fde75510f/media/capture/content/android/screen_capture_machine_android.cc
[modify] https://crrev.com/f9daf45b5563540323451b937315781fde75510f/media/capture/content/android/java/src/org/chromium/media/ScreenCapture.java


### [Deleted User] (2021-12-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-03)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-13)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Thank you for your report and excellent work! 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-03-11)

This issue was migrated from crbug.com/chromium/1275892?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GetUserMedia, Internals>Media>ScreenCapture]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-28)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058099)*
