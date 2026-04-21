# Security: UAF in WebContentsFrameTracker

| Field | Value |
|-------|-------|
| **Issue ID** | [40060046](https://issues.chromium.org/issues/40060046) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>SurfaceCapture |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Reporter** | le...@gmail.com |
| **Assignee** | kl...@chromium.org |
| **Created** | 2022-06-22 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**

Since tracker\_[1] will be sent to UIThread for destruction, it will not be destroyed immediately when WebContentsVideoCaptureDevice gets destructed:

```
std::unique_ptr<WebContentsFrameTracker, BrowserThread::DeleteOnUIThread>  
      tracker_;  

```

So there could be a race between its destructor and the other UIthread task SetCapturedContentSize[2]. This will make the weak pointer protection invalid.

```
GetUIThreadTaskRunner({})->PostTask(  
          FROM_HERE,  
          base::BindOnce(&WebContentsFrameTracker::SetCapturedContentSize,  
                         tracker_->AsWeakPtr(), new_size));  

```

And SetCapturedContentSize will finally access[3] the dangling pointer contents\_.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/web_contents_video_capture_device.h;l=78;drc=480e0e6fd0de59a38aa25145a7f58eaf4b03fb98>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/web_contents_video_capture_device.cc;l=86;drc=b3a3859e45fbc943eb148c38ea12d25a58051e27>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/media/capture/web_contents_frame_tracker.cc;l=88;drc=70b0ee470bd53a63da6c4194579e8c2865db2b79>

**VERSION**  

Chrome Version: head

**REPRODUCTION CASE**

1. apply poc.patch to simulate a compromised renderer
2. $ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=WebContentsCaptureHiDPI --auto-select-tab-capture-source-by-title="Poc Page" "<http://localhost:8000/poc.html>"

note: --auto-select-tab-capture-source-by-title is for the convenience of testing, it has nothing to do with the vulnerability itself. You can also manually select the tab to capture.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 17.7 KB)
- [poc.patch](attachments/poc.patch) (text/plain, 4.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 417 B)
- [windows.asan](attachments/windows.asan) (text/plain, 18.6 KB)

## Timeline

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-22)

Cannot repro on linux head

### aj...@google.com (2022-06-22)

Repros on Windows HEAD.

### aj...@google.com (2022-06-22)

-> klausw based on commit that added the feature flag.

FoundIn 104 as that is when 480e0e6  was first released.
Sev=High as a uaf in browser from a compromised renderer.

If the flag is not enabled for any users then feel free to set security_impact=none but fix this before the feature rolls out.

[Monorail components: Internals>Media>SurfaceCapture]

### aj...@google.com (2022-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kl...@chromium.org (2022-06-23)

I'll work on a fix, but do you have a link to best practices to help avoid this type of issue?

> So there could be a race between its destructor and the other UIthread task SetCapturedContentSize[2]. This will make the weak pointer protection invalid.

I thought that a weak pointer was sufficient protection against use-after-free in posted tasks, so I clearly need to update my mental model here.

### kl...@chromium.org (2022-06-23)

> If the flag is not enabled for any users then feel free to set security_impact=none but fix this before the feature rolls out.

At this point the flag is disabled by default and needs to be enabled manually, there aren't any finch experiments or origin trials that would activate it.

We've been doing some limited internal testing, so "not enabled for any users" isn't strictly true, but I assume that's still compatible with treating it as Security_Impact-None?

### we...@chromium.org (2022-06-23)

Re #10: It's hard to reason about the threading behaviour of these classes in their current state; I'd recommend:

1. Using SequenceBound<> to hold the WebContentsFrameTracker, on the UI thread.
2. Adding sequence-checks to each method to verify that it is being called correctly.
3. Remove use of SupportsWeakPtr<> from both classes.  WebContentsVideoCaptureDevice should instead use a WeakPtrFactory, and WebContentsFrameTracker needn't have a WeakPtr associated with it at all, once it is held in a SequenceBound.

Re-ordering of tasks posted to the WebContentsFrameTracker will not result in UaF, because tasks are bound to WeakPtr.

However, each PostTask is fetching the WeakPtr by calling to the |tracker_|, which is itself a member of the WebContentsVideoCapture device.

If that object were to be called from multiple threads, for example, then you'd have a UaF on |tracker_|, with or without the WeakPtrs.

### le...@gmail.com (2022-06-24)

> I thought that a weak pointer was sufficient protection against use-after-free in posted tasks, so I clearly need to update my mental model here.

Sorry for the misunderstanding. The target object being freed in this uaf bug is WebContents instead of WebContentsFrameTracker. The race I said means: that because WebContentsFrameTracker will not be destroyed synchronously when WebContents gets destructed, there is a chance that the task SetCapturedContentSize could run after the WebContents is destructed but before WebContentsFrameTracker gets destructed.

~WebContents
run SetCapturedContentSize <<----will access the dangling pointer contents_
~WebContentsFrameTracker

The WebContentsFrameTracker has not been destroyed before or during the running of SetCapturedContentSize, so the task will run successfully. This is what I said "make the weak pointer protection invalid", it doesn't really invalid. Sorry again for my unclear description.



The Security_Impact should be None, but according to the Severity Guidelines:

> Conversely, we do not consider it a mitigating factor if a vulnerability applies only to a particular group of users. For instance, a Critical vulnerability is still considered Critical even if it applies only to Linux or to those users running with accessibility features enabled.

The Security_Severity may keep High.

### kl...@chromium.org (2022-06-24)

Proposed fixes:

https://chromium-review.googlesource.com/c/chromium/src/+/3721469/ (fix context_ excessive lifetime, add web_context() null check)

https://chromium-review.googlesource.com/c/chromium/src/+/3724180 (refactor the classes to use SequenceBound<WebContentsFrameTracker> to simplify logic, as suggested by wez@ in https://crbug.com/chromium/1338591#c12)

### kl...@chromium.org (2022-06-24)

Correction to #14, web_context() should have been web_contents().

The first of the patches is intended to be backportable to 104, but it'll likely need to be manually edited due to (fairly trivial) merge conflicts since the affected code was modified post-branch. I'm not sure if that's appropriate in this case.

### aj...@google.com (2022-06-25)

Agree that this should be High for completeness. Thanks for all the analysis wez!

### we...@chromium.org (2022-06-25)

Happy to help, though as per leecraso@gmail's https://crbug.com/chromium/1338591#c13 it seems I'd missed the actual crux of the problem!

### gi...@appspot.gserviceaccount.com (2022-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b20f19a0ad176cc750a5612f364eda28ddcf7d53

commit b20f19a0ad176cc750a5612f364eda28ddcf7d53
Author: Klaus Weidner <klausw@chromium.org>
Date: Tue Jun 28 19:24:22 2022

Clarify context_ lifetime in WebContentsFrameTracker

The context_ object's lifetime should be equivalent to
the corresponding web_contents() value, but this wasn't
strictly enforced. Update the comments and add DCHECKs
to clarify. Also skip trying to update HiDPI scaling
when there are no active web_contents().

Bug: 1338591
Change-Id: I8da4e741b742f42e325b045ff2a8cf8e41b55425
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3721469
Commit-Queue: Klaus Weidner <klausw@chromium.org>
Reviewed-by: Alexander Cooper <alcooper@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1018797}

[modify] https://crrev.com/b20f19a0ad176cc750a5612f364eda28ddcf7d53/content/browser/media/capture/web_contents_frame_tracker.cc


### kl...@chromium.org (2022-06-30)

Setting to fixed now that patch r1018797 was submitted. I have a backport to the 104.0.5112 branch ready, this needed a bit of manual editing since the patch didn't apply cleanly. I haven't uploaded it yet since https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md#security-merge-triage says that the sherrifbot automation will request a merge if appropriate.

(Please let me know in case I misunderstood this or if you definitely want it backported, I wanted to avoid drawing attention to it on public gerrit in case it's not going to get merged.)

### [Deleted User] (2022-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c73e035a1528a80f9036e96829c09f95a0e15ef9

commit c73e035a1528a80f9036e96829c09f95a0e15ef9
Author: Klaus Weidner <klausw@chromium.org>
Date: Thu Jun 30 21:25:35 2022

Refactor frame tracker to SequenceBound

Instead of having both WebContentsFrameTracker and
WebContentsVideoCaptureDevice reference each other via WeakPtrs,
use a SequenceBound<WebContentsFrameTracker> owned by
WebContentsVideoCaptureDevice instead.

This requires moving construction of the WebContentsFrameTracker off of
the Device thread and onto the UI thread, where all of its methods had
previously expected to be run. Also add sequence checkers to both
classes to help enforce consistent usage.

Bug: 1338591
Change-Id: I94b48a1c3afe21e0cbcaad9be9cce7583900d3a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3724180
Reviewed-by: Alexander Cooper <alcooper@chromium.org>
Reviewed-by: Will Cassella <cassew@chromium.org>
Commit-Queue: Klaus Weidner <klausw@chromium.org>
Reviewed-by: Wez <wez@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1019831}

[modify] https://crrev.com/c73e035a1528a80f9036e96829c09f95a0e15ef9/content/browser/media/capture/web_contents_frame_tracker_unittest.cc
[modify] https://crrev.com/c73e035a1528a80f9036e96829c09f95a0e15ef9/content/browser/renderer_host/media/in_process_launched_video_capture_device.cc
[modify] https://crrev.com/c73e035a1528a80f9036e96829c09f95a0e15ef9/media/capture/video/video_capture_device.h
[modify] https://crrev.com/c73e035a1528a80f9036e96829c09f95a0e15ef9/content/browser/media/capture/web_contents_frame_tracker.h
[modify] https://crrev.com/c73e035a1528a80f9036e96829c09f95a0e15ef9/content/browser/media/capture/web_contents_frame_tracker.cc
[modify] https://crrev.com/c73e035a1528a80f9036e96829c09f95a0e15ef9/content/browser/media/capture/web_contents_video_capture_device.cc
[modify] https://crrev.com/c73e035a1528a80f9036e96829c09f95a0e15ef9/content/browser/media/capture/web_contents_video_capture_device.h


### am...@google.com (2022-07-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-06)

Congratulations, Leecraso and Guang Gong! The VRP Panel has decided to award you $20,000 for this report. Thank you for your efforts and great work! 

### am...@google.com (2022-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1338591?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060046)*
