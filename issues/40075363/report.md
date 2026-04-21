# heap-buffer-overflow in ~SingleShotFrameHandler(imagecapture/image_capture_frame_grabber.cc)

| Field | Value |
|-------|-------|
| **Issue ID** | [40075363](https://issues.chromium.org/issues/40075363) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>ImageCapture, Blink>Scheduling |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2023-10-21 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os version:

- ubuntu 22.04  
  
  tested chrome version:  
  
  Chromium 120.0.6073.0  
  
  Chromium 120.0.6080.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1213059.zip)  
  
  repro steps:  
  
  1 python3 -m http.server 8000 --dir=|PATH|  
  
  2 ./chrome --user-data-dir=/tmp/xx4 --js-flags=--shared-string-table,--expose-gc --no-sandbox <http://localhost:8000/crash.html> <http://localhost:8000/crash.html> <http://localhost:8000/crash.html> <http://localhost:8000/crash.html> --disable-gpu

Need to wait for 2-3 minutes to reproduce. If it doesn't reproduce, you can try again or open more tabs.

Bisect:  

This problem is introduced in this commit:<https://chromium.googlesource.com/chromium/src/+/1288c07551e931c18a41fea2316e258d00d51213>  

<https://chromium-review.googlesource.com/c/chromium/src/+/4936177>  

According to the chromiumdash, this proble affects DEV version after 120.0.6073.0.

**Problem Description:**  

==1823896==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x5250000278e8 at pc 0x5571de07a18f bp 0x7f17d74dda20 sp 0x7f17d74dda18  

WRITE of size 16 at 0x5250000278e8 thread T5 (Chrome\_ChildIOT)  

#0 0x5571de07a18e in v8::internal::HandleScope::ZapRange(unsigned long\*, unsigned long\*) ./../../v8/src/handles/handles.cc:194:8  

#1 0x5571ddb91dcf in CloseScope ./../../v8/src/handles/handles-inl.h:217:3  

#2 0x5571ddb91dcf in CloseAndEscape[v8::internal::JSMessageObject](javascript:void(0);) ./../../v8/src/handles/handles-inl.h:235:3  

#3 0x5571ddb91dcf in v8::Exception::CreateMessage(v8::Isolate\*, v8::Local[v8::Value](javascript:void(0);)) ./../../v8/src/api/api.cc:10609:13  

#4 0x5571f6db9790 in blink::PromiseRejectHandler(v8::PromiseRejectMessage, blink::RejectedPromises&, blink::ScriptState\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_initializer.cc:278:7  

#5 0x5571f6db44db in blink::PromiseRejectHandlerInMainThread(v8::PromiseRejectMessage) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_initializer.cc:320:3  

#6 0x5571de01593f in v8::internal::Isolate::ReportPromiseReject(v8::internal::Handle[v8::internal::JSPromise](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::PromiseRejectEvent) ./../../v8/src/execution/isolate.cc:5940:3  

#7 0x5571debbe3e0 in v8::internal::JSPromise::Reject(v8::internal::Handle[v8::internal::JSPromise](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), bool) ./../../v8/src/objects/objects.cc:4843:14  

#8 0x5571ddb77cab in v8::Promise::Resolver::Reject(v8::Local[v8::Context](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);)) ./../../v8/src/api/api.cc:8504:7  

#9 0x5571f6dd5588 in blink::ScriptPromise::InternalResolver::Reject(v8::Local[v8::Value](javascript:void(0);)) ./../../third\_party/blink/renderer/bindings/core/v8/script\_promise.cc:205:56  

#10 0x5571f6dd3183 in blink::ScriptPromiseResolver::ResolveOrRejectImmediately() ./../../third\_party/blink/renderer/bindings/core/v8/script\_promise\_resolver.cc:153:15  

#11 0x5571f749780b in void blink::ScriptPromiseResolver::ResolveOrReject[blink::ToV8UndefinedGenerator](javascript:void(0);)(blink::ToV8UndefinedGenerator, blink::ScriptPromiseResolver::ResolutionState) ./../../third\_party/blink/renderer/bindings/core/v8/script\_promise\_resolver.h:207:5  

#12 0x5571fdc921b9 in Reject[blink::ToV8UndefinedGenerator](javascript:void(0);) ./../../third\_party/blink/renderer/bindings/core/v8/script\_promise\_resolver.h:70:5  

#13 0x5571fdc921b9 in Reject ./../../third\_party/blink/renderer/bindings/core/v8/script\_promise\_resolver.h:74:19  

#14 0x5571fdc921b9 in OnError ./../../third\_party/blink/renderer/bindings/core/v8/callback\_promise\_adapter.h:191:17  

#15 0x5571fdc921b9 in blink::ImageCaptureFrameGrabber::OnSkImage(blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void>>, sk\_sp<SkImage>) ./../../third\_party/blink/renderer/modules/imagecapture/image\_capture\_frame\_grabber.cc:366:32  

#16 0x5571fdc9340d in void base::internal::FunctorTraits<void (blink::ImageCaptureFrameGrabber::\*)(blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void>>, sk\_sp<SkImage>), void>::Invoke<void (blink::ImageCaptureFrameGrabber::\*)(blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void>>, sk\_sp<SkImage>), base::WeakPtr[blink::ImageCaptureFrameGrabber](javascript:void(0);) const&, blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void>>, sk\_sp<SkImage>>(void (blink::ImageCaptureFrameGrabber::\*)(blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void>>, sk\_sp<SkImage>), base::WeakPtr[blink::ImageCaptureFrameGrabber](javascript:void(0);) const&, blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void>>&&, sk\_sp<SkImage>&&) ./../../base/functional/bind\_internal.h:713:12  

#17 0x5571fdc9319f in MakeItSo<void (blink::ImageCaptureFrameGrabber::\*)(blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void> >, sk\_sp<SkImage>), std::\_\_Cr::tuple<base::WeakPtr[blink::ImageCaptureFrameGrabber](javascript:void(0);), blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void> > >, sk\_sp<SkImage> > ./../../base/functional/bind\_internal.h:896:5  

#18 0x5571fdc9319f in RunImpl<void (blink::ImageCaptureFrameGrabber::\*)(blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void> >, sk\_sp<SkImage>), std::\_\_Cr::tuple<base::WeakPtr[blink::ImageCaptureFrameGrabber](javascript:void(0);), blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap, void> > >, 0UL, 1UL> ./../../base/functional/bind\_internal.h:968:12  

#19 0x5571fdc9319f in base::internal::Invoker<base::internal::BindState<void (blink::ImageCa

**Additional Comments:**

\*\*Chrome version: \*\* 120.0.6073.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.8 KB)
- [asan.log](attachments/asan.log) (text/plain, 23.9 KB)
- [security-check-failed.log](attachments/security-check-failed.log) (text/plain, 18.4 KB)
- [null-dereference.log](attachments/null-dereference.log) (text/plain, 14.9 KB)

## Timeline

### [Deleted User] (2023-10-21)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-10-21)

Sorry, I forgot to remove some unnecessary flags. You don't need --js-flags=--shared-string-table,--expose-gc, but these parameters won't affect the result either.

### em...@gmail.com (2023-10-21)

After multiple tests, it was found that there are more different crashes that can be reproduced. I will upload all of them for reference.

### ma...@chromium.org (2023-10-24)

[Empty comment from Monorail migration]

[Monorail components: Blink>ImageCapture]

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-10-24)

For some reason a PostCrossThreadTask in MediaStreamVideoTrack::FrameDeliverer::RemoveCallbackOnVideoTaskRunner() [1] does not actually post the task and destroys the callback on the video task runner/IO thread.
Not sure if this is a bug there, but will fix it by always running the callback on the main thread in ImageCaptureFrameGrabber.

StackTrace by forcing a CHECK in the SingleShotFrameHandler destructor (#5), shows it's called synchronously from PostCrossThreadTask (#39)

#0 0x7f2f66bae11c base::debug::CollectStackTrace()
#1 0x7f2f66b5ec3a base::debug::StackTrace::StackTrace()
#2 0x7f2f66b5ebf5 base::debug::StackTrace::StackTrace()
#3 0x7f2f6687fa19 logging::LogMessage::~LogMessage()
#4 0x7f2f668802f9 logging::LogMessage::~LogMessage()
#5 0x7f2f6682514d logging::CheckError::~CheckError()
#6 0x7f2f20713ca9 blink::ImageCaptureFrameGrabber::SingleShotFrameHandler::~SingleShotFrameHandler()
#7 0x7f2f20718c07 WTF::ThreadSafeRefCounted<>::DeleteInternal<>()
#8 0x7f2f20718bd5 WTF::DefaultThreadSafeRefCountedTraits<>::Destruct()
#9 0x7f2f20718baf base::RefCountedThreadSafe<>::Release()
#10 0x7f2f20718b72 scoped_refptr<>::Release()
#11 0x7f2f20715b5a scoped_refptr<>::~scoped_refptr()
#12 0x7f2f20717595 std::__Cr::__tuple_leaf<>::~__tuple_leaf()
#13 0x7f2f20717e15 std::__Cr::__tuple_impl<>::~__tuple_impl()
#14 0x7f2f20717df5 std::__Cr::tuple<>::~tuple()
#15 0x7f2f20717dcd base::internal::BindState<>::~BindState()
#16 0x7f2f20717d37 base::internal::BindState<>::Destroy()
#17 0x7f2f66861cfa base::internal::BindStateBaseRefCountTraits::Destruct()
#18 0x7f2f668621ff base::RefCountedThreadSafe<>::Release()
#19 0x7f2f668621b2 scoped_refptr<>::Release()
#20 0x7f2f668620fa scoped_refptr<>::~scoped_refptr()
#21 0x7f2f66861ee5 base::internal::BindStateHolder::~BindStateHolder()
#22 0x7f2f20246e25 base::RepeatingCallback<>::~RepeatingCallback()
#23 0x7f2f20255725 WTF::CrossThreadFunction<>::~CrossThreadFunction()
#24 0x7f2f20b05525 std::__Cr::__tuple_leaf<>::~__tuple_leaf()
#25 0x7f2f20b054e6 std::__Cr::__tuple_impl<>::~__tuple_impl()
#26 0x7f2f20b054b5 std::__Cr::tuple<>::~tuple()
#27 0x7f2f20aff43d base::internal::BindState<>::~BindState()
#28 0x7f2f20aff3e7 base::internal::BindState<>::Destroy()
#29 0x7f2f66861cfa base::internal::BindStateBaseRefCountTraits::Destruct()
#30 0x7f2f668621ff base::RefCountedThreadSafe<>::Release()
#31 0x7f2f668621b2 scoped_refptr<>::Release()
#32 0x7f2f668620fa scoped_refptr<>::~scoped_refptr()
#33 0x7f2f66861ee5 base::internal::BindStateHolder::~BindStateHolder()
#34 0x7f2f66818f55 base::OnceCallback<>::~OnceCallback()
#35 0x7f2f66a511e3 base::sequence_manager::internal::PostedTask::~PostedTask()
#36 0x7f2f66a2fe55 base::sequence_manager::internal::TaskQueueImpl::TaskRunner::PostDelayedTask()
#37 0x7f2f264e505b blink::scheduler::BlinkSchedulerSingleThreadTaskRunner::PostDelayedTask()
#38 0x7f2f66a7adbf base::TaskRunner::PostTask()
#39 0x7f2f200b7e8f blink::PostCrossThreadTask()
#40 0x7f2f20af928b blink::MediaStreamVideoTrack::FrameDeliverer::RemoveCallbackOnVideoTaskRunner()
#41 0x7f2f20b050af base::internal::FunctorTraits<>::Invoke<>()
#42 0x7f2f20b04ff6 base::internal::InvokeHelper<>::MakeItSo<>()
#43 0x7f2f20b04f5d base::internal::Invoker<>::RunImpl<>()
#44 0x7f2f20b04ec7 base::internal::Invoker<>::RunOnce()
#45 0x7f2f668190cb base::OnceCallback<>::Run()

[1] https://crsrc.org/c/third_party/blink/renderer/modules/mediastream/media_stream_video_track.cc;l=449;drc=abbfc06e9b070c9ea64af2b233624646cef00252;bpv=0;bpt=1



### gu...@chromium.org (2023-10-24)

dcheng@: What could cause PostCrossThreadTask to not post the given callback to the given task runner, and instead destroy it synchronously?

### [Deleted User] (2023-10-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7fab014dd5dcbab6771179592b0e9951b3ffebdb

commit 7fab014dd5dcbab6771179592b0e9951b3ffebdb
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Oct 25 07:19:29 2023

[ImageCapture] Ensure promise callback always runs on main thread

In some cases, the SingleShotFrameHandler destructor can run on the IO thread.
Since the callback executes JS, always post to the main thread to run it.

Bug: 1494573
Change-Id: Ib7cb5ac7989ebcdc265a749ea87037a7b54d8c16
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4968839
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1214675}

[modify] https://crrev.com/7fab014dd5dcbab6771179592b0e9951b3ffebdb/third_party/blink/renderer/modules/imagecapture/image_capture_frame_grabber.cc


### gu...@chromium.org (2023-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-25)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-10-26)

adding some Blink scheduling folks

Is there anything we can do to make it harder to write this kind of bug? I think what's happening is we were trying to post a task to the scheduler for a detached frame (based on an inspection of the repro + the call stack from guidou). IIRC we used to run tasks, even for detached frames, but maybe we stopped at some point?

maybe we should be redirecting them to the main thread task runner in that case?

[Monorail components: Blink>Scheduling]

### dc...@chromium.org (2023-10-26)

Or maybe we could make PostCrossThreadTask() return a nodiscard value. It's tricky to make that work well here though, since most people post once callbacks. So I guess the return value would have to optionally return the original callback.

### da...@chromium.org (2023-10-26)

Yeah the problem here is a destructor running JS, I think. I don't know if that can be fixed, but destructors doing complex or thread-specific stuff bound into a callback owning them explodes in ways like this.

Even if PostCrossThreadTask returned the callback, you need to not destroy it, or post it somewhere else, but during shutdown you can't do that.

### dc...@chromium.org (2023-10-26)

Frame scheduler exposes this problem much more often though, since frames can be detached without the entire renderer shutting down.

### sh...@chromium.org (2023-10-26)

We still run tasks for detached frames, but only until they become empty. Once that happens, they're shut down and task runners associated with the queue stop accepting tasks (resulting in callbacks being destroyed). (This logic moved from sequence manager to blink recently; see MainThreadSchedulerImpl::ShutdownEmptyDetachedTaskQueues).

There was a similar problem with DeleteSoon (https://crbug.com/chromium/1376851), where the object would leak if the frame/worker queue was shut down. For that, we now automatically delete the object on the thread's (longer-lived) default task queue, but only if the target thread is still alive. We could do something similar here (i.e. redirect, like you mention), but not sure if that's what we want in general.

I guess we could also rethink frame scheduler task queue lifetime (e.g. tie it to task runners) so they continue to accept tasks until thread shutdown -- although per spec tasks associated with non-fully active documents aren't supposed to run, which makes me wonder in this case if the task should just be dropped (and running JS decoupled from the destructor).

### re...@chromium.org (2023-10-26)

It would be nice if we had a version of WTF::CrossThreadBindOnce() which included base::BindPostTask() to bind the callback to the current thread's task runner, but also synchronously invoked the callback if invoked on the correct thread so that there's no overhead in the normal case. This is why the fix CL doesn't use base::BindPostTask(). In the normal case control returns to the correct thread before the callback is invoked so using base::BindPostTask() would introduce an unnecessary PostTask() call.

### [Deleted User] (2023-10-31)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-02)

Congratulations! The Chrome VRP Panel has decided to award you $7,000 for this report of memory corruption in the renderer process + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-10)

Not requesting merge to beta (M120) because latest trunk commit (1214675) appears to be prior to beta branch point (1217362). If this is incorrect, please replace the Merge-NA-120 label with Merge-Request-120. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge review required: M120 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [120].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-10)

https://crrev.com/c/4968839 landed on 120, so 120 merge is not needed here

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-31)

This issue was migrated from crbug.com/chromium/1494573?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>ImageCapture, Blink>Scheduling]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40075363)*
