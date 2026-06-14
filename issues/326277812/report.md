# UAF in ActiveDevicesMediaCoordinator::GotDeviceIdsOpenedForWebContents

| Field | Value |
|-------|-------|
| **Issue ID** | [326277812](https://issues.chromium.org/issues/326277812) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>UI |
| **Platforms** | Windows |
| **Reporter** | jt...@gmail.com |
| **Assignee** | br...@chromium.org |
| **Created** | 2024-02-22 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

When feature kCameraMicPreview is enabled, content view of the permissions subpages in page info would contain camera and mic preview. The function `ActiveDevicesMediaCoordinator::UpdateMediaCoordinatorList` calls `WebContentsImpl::GetMediaCaptureRawDeviceIdsOpened` which binds a raw `this` pointer (using base::Unretained) to a streaming devices fetch callback [1]. By the time the callback runs, the ActiveDevicesMediaCoordinator might have been destroyed, leading to UAF.

```
void ActiveDevicesMediaCoordinator::UpdateMediaCoordinatorList() {
  if (!web_contents_.MaybeValid()) {
    return;
  }

  web_contents_->GetMediaCaptureRawDeviceIdsOpened(
      stream_type_,
      base::BindOnce(
          &ActiveDevicesMediaCoordinator::GotDeviceIdsOpenedForWebContents,
          base::Unretained(this)));  // ==> [1]
}

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/media_preview/active_devices_media_coordinator.cc;l=98;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090>

**BISECTION**

This was introduced in <https://chromium.googlesource.com/chromium/src/+/4460397c446b02f07001affae38fb7b346097a89>

**Fix Suggestion**

Using WeakPtr instead of base::Unretained, see fix.diff for details :)

**VERSION**

Chrome Version: beta

**REPRODUCTION CASE**

For the convenience of reproducing, apply the attached patch.diff first

1. Host poc.html
   
   python3 -m http.server 8000
2. Run
   
   out\Asan\chrome.exe --enable-features=OneTimePermission,CameraMicPreview <http://localhost:8000/poc.html>
3. Click page info button then click permission subpage button

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser

Crash State: see asan.log for details

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 15.4 KB)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.8 KB)
- [poc.html](attachments/poc.html) (text/html, 426 B)
- [fix.diff](attachments/fix.diff) (text/x-diff, 2.9 KB)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 4.4 MB)

## Timeline

### jt...@gmail.com (2024-02-22)

Upload a recording of repro. Tested on: Chromium 123.0.6307.1 asan build 64-bit on Windows 10

### ah...@google.com (2024-02-22)

[primary security shepherd]
Thanks for the report!
I was not able to reproduce locally due to device not having camera/mic.
Provisionally Setting severity to High (memory corruption in the browser process that requires specific user interaction)
https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#TOC-High-severity

Provisionally setting Security_Impact-None since requires some non-default feature flags
Provisionally Setting OS to windows.

@br...@chromium.org could you please take a look?
Thanks,

### ap...@google.com (2024-02-22)

Project: chromium/src
Branch: main

commit 626bd505edcb1253fb02116a03bf6fe84c2ded54
Author: Bryant Chandler <bryantchandler@chromium.org>
Date:   Thu Feb 22 17:37:54 2024

    [media_preview] Fix use-after-free bug in ActiveDevicesMediaCoordinator
    
    `ActiveDevicesMediaCoordinator` passed a `this` pointer to `WebContents`
    unretained, but it's possible for `WebContents` to outlive it. This
    CL changes to a `WeakPtr` to address that problem.
    
    Fixed: 326277812
    Change-Id: I506ca8e774da84715c356013e7eb8411e075f4f2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5319030
    Reviewed-by: Ahmed Moussa <ahmedmoussa@google.com>
    Commit-Queue: Bryant Chandler <bryantchandler@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1264043}

M       chrome/browser/ui/views/media_preview/active_devices_media_coordinator.cc
M       chrome/browser/ui/views/media_preview/active_devices_media_coordinator.h

https://chromium-review.googlesource.com/5319030


### am...@google.com (2024-02-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-29)

Congratulations on another one, Rong! The Chrome VRP Panel has decided to award you $1,000 for this heavily mitigated UAF in the browser process, mitigated by BRP protection and user interaction, + $1,000 bisect bonus + $1,000 patch bonus. Thank you for your all your efforts here in discovering and reporting this issue to us!

### pe...@google.com (2024-05-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/326277812)*
