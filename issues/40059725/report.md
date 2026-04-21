# AddressSanitizer: heap-use-after-free in content::ScreenlockMonitor::RemoveObserver content/browser/

| Field | Value |
|-------|-------|
| **Issue ID** | [40059725](https://issues.chromium.org/issues/40059725) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | he...@google.com |
| **Created** | 2022-05-23 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

#Reproduce  

The problem was found by my fuzzer running on CF(CC Security team for access permission <https://clusterfuzz.com/testcase-detail/5689697418543104>),  

But it cannot be reproduced stably, CF may not automatically report.  

After manual analysis, the root cause of the vulnerability is clearly understood.

Type of crash  

browser process(Sandbox escape)

**Problem Description:**  

#Analysis

1. VideoCaptureManager is a RefCountedThreadSafe object and has a raw\_ptr to ScreenlockMonitor[2]
2. When ProcessDeviceStartRequestQueue is called, the this pointer is passed as a parameter, causing the life cycle of VideoCaptureManager to be bound to the callback[1]
3. When browser is shutdown, ScreenlockMonitor is freed, and then ui\_thread\_executor\_ is reset, causing the callback at [1] to be released, which in turn causes the VideoCaptureManager destructor to trigger, and finally causes UAF

```
//https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/video_capture_manager.cc;drc=3f264e6e605b35f5bcd64cb6070d70c70c7236a7;l=328  
void VideoCaptureManager::ProcessDeviceStartRequestQueue() {  
  DCHECK_CURRENTLY_ON(BrowserThread::IO);  
  TRACE_EVENT_INSTANT0(TRACE_DISABLED_BY_DEFAULT("video_and_image_capture"),  
                       "VideoCaptureManager::ProcessDeviceStartRequestQueue",  
                       TRACE_EVENT_SCOPE_PROCESS);  
 ...CUT...  
  
  // The method CreateAndStartDeviceAsync() is going to run asynchronously.  
  // Since we may be removing the controller while it is executing, we need to  
  // pass it shared ownership to itself so that it stays alive while executing.  
  // And since the execution may make callbacks into |this|, we also need  
  // to pass it shared ownership to |this|.  
  // TODO(chfremer): Check if request->params() can actually be different from  
  // controller->parameters, and simplify if this is not the case.  
  controller->CreateAndStartDeviceAsync(  
      request->params(), static_cast<VideoCaptureDeviceLaunchObserver\*>(this),  
      base::BindOnce([](scoped_refptr<VideoCaptureManager>,  
                        scoped_refptr<VideoCaptureController>) {},  
                     scoped_refptr<VideoCaptureManager>(this),						<<[1]  
                     GetControllerSharedRef(controller)));  
}  
  
//https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/video_capture_manager.h;drc=3f264e6e605b35f5bcd64cb6070d70c70c7236a7;l=340  
class CONTENT_EXPORT VideoCaptureManager  
    : public MediaStreamProvider,  
      public VideoCaptureDeviceLaunchObserver,  
      public ScreenlockObserver {  
 public:  
 ...CUT...  
  
  const std::unique_ptr<VideoCaptureProvider> video_capture_provider_;  
  base::RepeatingCallback<void(const std::string&)> emit_log_message_cb_;  
  raw_ptr<ScreenlockMonitor> screenlock_monitor_;									<<[2]  
    
//  
void BrowserMainLoop::PostCreateMainMessageLoop() {  
...CUT...  
  {  
    TRACE_EVENT0("startup", "BrowserMainLoop::Subsystem:ScreenlockMonitor");  
    std::unique_ptr<ScreenlockMonitorSource> screenlock_monitor_source =  
        std::make_unique<ScreenlockMonitorDeviceSource>();  
    screenlock_monitor_ = std::make_unique<ScreenlockMonitor>(						<<[3]  
        std::move(screenlock_monitor_source));  
  }    

```

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 17.5 KB)

## Timeline

### dt...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>GetUserMedia]

### [Deleted User] (2022-05-24)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-05-25)

This is reported by the fuzzer running on clusterfuzz, which can trigger sbx directly, without the need for a compromised rendering process.
All info is here https://clusterfuzz.com/testcase-detail/5689697418543104

### dr...@chromium.org (2022-05-25)

I can't reproduce this manually, and ClusterFuzz only has the one revision, so setting FoundIn for that one revision.

Assigning High severity as this is memory process corruption on shutdown.

eladolon@, herre@ - can you take a look?

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-26)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-26)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2022-05-27)

Tony has sent a CL to fix this, so reassigning to him.

### gi...@appspot.gserviceaccount.com (2022-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bc6911f9138a99b899e70775e2670f70f0a6b42e

commit bc6911f9138a99b899e70775e2670f70f0a6b42e
Author: Tony Herre <toprice@chromium.org>
Date: Fri May 27 13:30:30 2022

Remove VideoCaptureManager's raw_ptr to ScreenlockMonitor

Instead always call the static Get() to get the per-process singleton,
or null if it's already been destroyed.

Bug: 1328045
Change-Id: I814d6bec178646c422885481b90ddf6de6adb697
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3669051
Commit-Queue: Tony Herre <toprice@chromium.org>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1008223}

[modify] https://crrev.com/bc6911f9138a99b899e70775e2670f70f0a6b42e/content/browser/renderer_host/media/media_stream_manager.cc
[modify] https://crrev.com/bc6911f9138a99b899e70775e2670f70f0a6b42e/content/browser/renderer_host/media/video_capture_manager.h
[modify] https://crrev.com/bc6911f9138a99b899e70775e2670f70f0a6b42e/content/browser/renderer_host/media/video_capture_manager.cc
[modify] https://crrev.com/bc6911f9138a99b899e70775e2670f70f0a6b42e/content/browser/renderer_host/media/video_capture_manager_unittest.cc


### he...@google.com (2022-05-27)

That change removes the raw pointer causing this issue. Now we'll get the pointer to the singleton ScreenlockMonitor every time we need it and check it's not been nulled out before use.
No further work is required for 104.

### [Deleted User] (2022-05-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-01)

Congratulations! The VRP Panel has decided to award you $10,000 for this report + $1,000 fuzzer bonus. While this issue does result in browser process memory corruptions without the need for a compromised rendered, this issue is triggered on shutdown making it much harder to exploit. Thank you for your efforts and your contributions to Chrome Fuzzing + reporting this issue to us. 

### am...@google.com (2022-06-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-11)

Not requesting merge to dev (M104) because latest trunk commit (1008223) appears to be prior to dev branch point (1012729). If this is incorrect, please replace the Merge-NA-104 label with Merge-Request-104. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1328045?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059725)*
