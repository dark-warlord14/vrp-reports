# Security: access-violation src\v8\src\api\api.cc:5809 in v8::String::WriteOneByte

| Field | Value |
|-------|-------|
| **Issue ID** | [40061335](https://issues.chromium.org/issues/40061335) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bindings, Blink>ImageCapture, Blink>JavaScript>API |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | be...@google.com |
| **Created** | 2022-10-13 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

access-violation src\v8\src\api\api.cc:5809 in v8::String::WriteOneByte

**VERSION**  

WIN10 X64  

asan-win32-release\_x64-1057463

**REPRODUCTION CASE**  

Coming soon

Type of crash: [tab]

RCA  

Coming soon

ASAN

=================================================================  

==9272==ERROR: AddressSanitizer: access-violation on unknown address 0x000000004858 (pc 0x7ffa6b2f892c bp 0x009e237fdec0 sp 0x009e237fde40 T11)  

==9272==The signal is caused by a READ memory access.  

==9272==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffa6b2f892b in v8::String::WriteOneByte C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:5809  

#1 0x7ffa794d1e3f in blink::ToBlinkString[WTF::String](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\bindings\string\_resource.cc:201  

#2 0x7ffa7ccd8cfa in blink::PromiseRejectHandler C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\v8\_initializer.cc:300  

#3 0x7ffa7ccd4e51 in blink::PromiseRejectHandlerInMainThread C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\v8\_initializer.cc:343  

#4 0x7ffa6b94691c in v8::internal::Isolate::ReportPromiseReject C:\b\s\w\ir\cache\builder\src\v8\src\execution\isolate.cc:5465  

#5 0x7ffa6c541657 in v8::internal::JSPromise::Reject C:\b\s\w\ir\cache\builder\src\v8\src\objects\objects.cc:5541  

#6 0x7ffa6b319c2d in v8::Promise::Resolver::Reject C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:7828  

#7 0x7ffa7ca5be97 in blink::ScriptPromise::InternalResolver::Reject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\script\_promise.cc:205  

#8 0x7ffa7ca59862 in blink::ScriptPromiseResolver::ResolveOrRejectImmediately C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\script\_promise\_resolver.cc:147  

#9 0x7ffa78fb9b57 in blink::ScriptPromiseResolver::ResolveOrReject[blink::ToV8UndefinedGenerator](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\bindings\core\v8\script\_promise\_resolver.h:202  

#10 0x7ffa87c1ea01 in blink::`anonymous namespace'::OnError C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\imagecapture\image_capture_frame_grabber.cc:52 #11 0x7ffa87c20a88 in base::internal::Invoker<base::internal::BindState<void (\*)(std::Cr::unique_ptr<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap,void>,std::Cr::default_delete<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap,void> > >)>,void (std::Cr::unique_ptr<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap,void>,std::Cr::default_delete<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap,void> > >)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:871 #12 0x7ffa87c20c54 in base::OnceCallback<void (std::Cr::unique_ptr<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap,void>,std::Cr::default_delete<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap,void> > >)>::Run C:\b\s\w\ir\cache\builder\src\base\functional\callback.h:145 #13 0x7ffa87c1f80a in blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap,void> >::~ScopedWebCallbacks C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\imagecapture\image_capture_frame_grabber.h:91 #14 0x7ffa87c205ce in base::internal::BindState<void (blink::ImageCaptureFrameGrabber::\*)(blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap,void> >, sk_sp<SkImage>),base::WeakPtr<blink::ImageCaptureFrameGrabber>,blink::ScopedWebCallbacks<blink::internal::CallbackPromiseAdapterInternal::CallbackPromiseAdapter<blink::ImageBitmap,void> > >::Destroy C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1121 #15 0x7ffa87c2068b in base::RefCountedThreadSafe<blink::ImageCaptureFrameGrabber::SingleShotFrameHandler,WTF::DefaultThreadSafeRefCountedTraits<blink::ImageCaptureFrameGrabber::SingleShotFrameHandler> >::Release C:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h:416 #16 0x7ffa87c200d1 in base::internal::BindState<void (blink::ImageCaptureFrameGrabber::SingleShotFrameHandler::\*)(scoped_refptr<base::SingleThreadTaskRunner>, scoped_refptr<media::VideoFrame>, std::Cr::vector<scoped_refptr<media::VideoFrame>,std::Cr::allocator<scoped_refptr<media::VideoFrame> > >, base::TimeTicks),scoped_refptr<blink::ImageCaptureFrameGrabber::SingleShotFrameHandler>,scoped_refptr<base::SingleThreadTaskRunner> >::Destroy C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1121 #17 0x7ffa6e750b72 in base::internal::BindState<void (\*)(base::OnceCallback<void (base::OnceCallback<void (blink::ServiceWorkerStatusCode)>)>, base::OnceCallback<void (blink::ServiceWorkerStatusCode)>, blink::ServiceWorkerStatusCode),base::OnceCallback<void (base::OnceCallback<void (blink::ServiceWorkerStatusCode)>)>,base::OnceCallback<void (blink::ServiceWorkerStatusCode)> >::Destroy C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:1121 #18 0x7ffa7400ce58 in base::sequence_manager::internal::TaskQueueImpl::GuardedTaskPoster::PostTask C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\task_queue_impl.cc:110 #19 0x7ffa7400d7da in base::sequence_manager::internal::TaskQueueImpl::TaskRunner::PostDelayedTask C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\task_queue_impl.cc:144 #20 0x7ffa7402ad3f in base::TaskRunner::PostTask C:\b\s\w\ir\cache\builder\src\base\task\task_runner.cc:47 #21 0x7ffa86378e82 in blink::MediaStreamVideoTrack::FrameDeliverer::RemoveCallbackOnIO C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\mediastream\media_stream_video_track.cc:331 #22 0x7ffa86387437 in base::internal::Invoker<base::internal::BindState<void (blink::MediaStreamVideoTrack::FrameDeliverer::\*)(blink::WebMediaStreamSink \*, const scoped_refptr<base::SingleThreadTaskRunner> &),scoped_refptr<blink::MediaStreamVideoTrack::FrameDeliverer>,WTF::CrossThreadUnretainedWrapper<blink::WebMediaStreamSink>,scoped_refptr<base::SingleThreadTaskRunner> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind_internal.h:871 #23 0x7ffa73feec69 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:133 #24 0x7ffa76f1da88 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:441 #25 0x7ffa76f1c8b2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:297 #26 0x7ffa7409f009 in base::MessagePumpForIO::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:710 #27 0x7ffa74098f50 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78 #28 0x7ffa76f1fd8d in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:600 #29 0x7ffa73f87ece in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141 #30 0x7ffa7403ec7d in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:338 #31 0x7ffa6e83aa21 in content::BrowserProcessIOThread::IOThreadRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_process_io_thread.cc:119 #32 0x7ffa7403f095 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:408 #33 0x7ffa740bb001 in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:134  

#34 0x7ff62a2ceeb3 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:277  

#35 0x7ffaef647033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#36 0x7ffaf07626a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

==9272==First 16 instruction bytes at pc: 45 8b 8d 58 48 00 00 41 c7 85 58 48 00 00 05 00  

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation C:\b\s\w\ir\cache\builder\src\v8\src\api\api.cc:5809 in v8::String::WriteOneByte  

Thread T11 created by T0 here:  

#0 0x7ff62a2cf942 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffa740ba0ae in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:199  

#2 0x7ffa7403dec4 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:211  

#3 0x7ffa6f6e0557 in content::BrowserTaskExecutor::CreateIOThread C:\b\s\w\ir\cache\builder\src\content\browser\scheduler\browser\_task\_executor.cc:382  

#4 0x7ffa73b16df5 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1215  

#5 0x7ffa73b15ee7 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1103  

#6 0x7ffa73b11e00 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:342  

#7 0x7ffa73b124d2 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:370  

#8 0x7ffa676214af in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:175  

#9 0x7ff62a215a20 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#10 0x7ff62a212a4c in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:391  

#11 0x7ff62a6325cf in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#12 0x7ffaef647033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#13 0x7ffaf07626a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

==9272==ABORTING

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 9.9 KB)
- [dcheck.txt](attachments/dcheck.txt) (text/plain, 16.8 KB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [help.js](attachments/help.js) (text/plain, 827 B)
- [poc2.html](attachments/poc2.html) (text/plain, 1.5 KB)
- [asan_with_log.txt](attachments/asan_with_log.txt) (text/plain, 20.2 KB)
- [index.html](attachments/index.html) (text/plain, 284 B)

## Timeline

### [Deleted User] (2022-10-13)

[Empty comment from Monorail migration]

### jd...@chromium.org (2022-10-13)

Adding the Needs-Feedback label until a PoC is available.

### m....@gmail.com (2022-10-13)

REPRODUCTION CASE
install node
install puppeteer-core
unzip poc.zip;python -m http.server 1337; 
node ch.test.js chrome_bin_path http://localhost:1337/poc.html

NOTE:1337 is hardcode in poc.html,can't change.
ch.test will cycle the test 30 times to ensure that the crash occurs stably


### [Deleted User] (2022-10-13)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-10-13)

The current analysis believes that the problem is that the code executed on the main thread is wrongly executed on the IO thread(blink::PromiseRejectHandlerInMainThread).

The address of the out-of-bounds read seems to be related to the content pointed to by the PC register.

access-violation on unknown address 0x00000000   48 58
==9272==First 16 instruction bytes at pc: 45 8b 8d 58 48 00 00 41 c7 85 58 48 00 00 05 00 
access-violation on unknown address 0x00000000     dc 70
==14024==First 16 instruction bytes at pc: 49 83 bd 70 dc 00 00 00 0f 95 c0 48 83 ec 40 89 

### jd...@chromium.org (2022-10-14)

Wow, that's quite the PoC... Can you help us by reducing the size of the PoC a bit? It's quite hard to interpret in its current form.

### m....@gmail.com (2022-10-17)

Because it cannot be reproduced stably, the minimum sample has not yet been produced, and I am still trying.

### [Deleted User] (2022-10-17)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-10-17)

RCA
I don't know what the consequences of executing script code in the IO thread using the main thread context will be, but it seems very serious

1. The scoped_callbacks[1] object is constructed using MakeScopedWebCallbacks in the ImageCaptureFrameGrabber::GrabFrame function, and OnError is used as the construction_callback
2. scoped_callbacks will transfer ownership to SingleShotFrameHandler[2]
3. ConvertToBaseRepeatingCallback will encapsulate all into callback_A[3]
4. ConnectToTrack adds the callback_A to the callbacks_[4,5,6] list of the MediaStreamVideoTrack object by AddSink->AddCallback->AddcallbackOnIO
5. callbacks_ will destroys on IO thread by blink::MediaStreamVideoTrack::FrameDeliverer::RemoveCallback[7]
6. scoped_callbacks is destroyed in the IO thread, construction_callback is called, finally the IO thread accesses the script execution context of the main thread[8]

```
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/imagecapture/image_capture_frame_grabber.cc;drc=aaea55c708c63d53a89fb525484aa94747599714;l=313
void ImageCaptureFrameGrabber::GrabFrame(
    MediaStreamComponent* component,
    std::unique_ptr<ImageCaptureGrabFrameCallbacks> callbacks,
    scoped_refptr<base::SingleThreadTaskRunner> task_runner) {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);

  if (frame_grab_in_progress_) {
    // Reject grabFrame()s too close back to back.
    callbacks->OnError();
    return;
  }

  auto scoped_callbacks =
      MakeScopedWebCallbacks(std::move(callbacks), WTF::BindOnce(&OnError));			<<[1]

  // A SingleShotFrameHandler is bound and given to the Track to guarantee that
  // only one VideoFrame is converted and delivered to OnSkImage(), otherwise
  // SKImages might be sent to resolved |callbacks| while DisconnectFromTrack()
  // is being processed, which might be further held up if UI is busy, see
  // https://crbug.com/623042.
  frame_grab_in_progress_ = true;
  MediaStreamVideoSink::ConnectToTrack(													<<[4]
      WebMediaStreamTrack(component),
      ConvertToBaseRepeatingCallback(CrossThreadBindRepeating(							<<[3]
          &SingleShotFrameHandler::OnVideoFrameOnIOThread,
          base::MakeRefCounted<SingleShotFrameHandler>(CrossThreadBindOnce(
              &ImageCaptureFrameGrabber::OnSkImage, weak_factory_.GetWeakPtr(),
              std::move(scoped_callbacks))),											<<[2]
          std::move(task_runner))),
      MediaStreamVideoSink::IsSecure::kNo,
      MediaStreamVideoSink::UsesAlpha::kDefault);
}

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediarecorder/video_track_recorder.cc;drc=aaea55c708c63d53a89fb525484aa94747599714;l=815
void VideoTrackRecorderImpl::ConnectToTrack(
    const VideoCaptureDeliverFrameCB& callback) {
  track_->AddSink(this, callback, MediaStreamVideoSink::IsSecure::kNo,					<<[5]
                  MediaStreamVideoSink::UsesAlpha::kDefault);
}

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/media_stream_video_track.cc;drc=aaea55c708c63d53a89fb525484aa94747599714;l=261
void MediaStreamVideoTrack::FrameDeliverer::AddCallbackOnIO(
    VideoSinkId id,
    VideoCaptureDeliverFrameInternalCallback callback) {
  DCHECK(io_task_runner_->BelongsToCurrentThread());
  callbacks_.push_back(VideoIdCallbacks{id, std::move(callback),						<<[6]
                                        CrossThreadBindRepeating([] {})});
}

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/media_stream_video_track.cc;drc=aaea55c708c63d53a89fb525484aa94747599714;l=317
void MediaStreamVideoTrack::FrameDeliverer::RemoveCallback(VideoSinkId id) {
  DCHECK_CALLED_ON_VALID_THREAD(main_render_thread_checker_);
  PostCrossThreadTask(
      *io_task_runner_, FROM_HERE,
      CrossThreadBindOnce(&FrameDeliverer::RemoveCallbackOnIO,							<<[7]
                          WrapRefCounted(this), WTF::CrossThreadUnretained(id),
                          main_render_task_runner_));
}

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/imagecapture/image_capture.cc;drc=aaea55c708c63d53a89fb525484aa94747599714;l=368

ScriptPromise ImageCapture::grabFrame(ScriptState* script_state) {
  auto* resolver = MakeGarbageCollected<ScriptPromiseResolver>(script_state);
  ScriptPromise promise = resolver->Promise();

...CUT...

  auto resolver_callback_adapter =
      std::make_unique<CallbackPromiseAdapter<ImageBitmap, void>>(resolver);			<<[8]
  frame_grabber_->GrabFrame(stream_track_->Component(),
                            std::move(resolver_callback_adapter),
                            ExecutionContext::From(script_state)
                                ->GetTaskRunner(TaskType::kDOMManipulation));

  return promise;
}
```

### jd...@chromium.org (2022-10-18)

I can't reproduce this, and I'm not sure of the consequences either. If we can't narrow this down a bit, this may become a WontFix.

eladalon@: would you mind taking a look at this and see if you can see what's going on? It seems likely you'll be somewhat more comfortable in this part of the code than I am. Feel free to re-assign if you think there'd be someone better. Thank you!

[Monorail components: Blink>ImageCapture]

### m....@gmail.com (2022-10-18)

By analyzing the log of dcheck, I manually constructed a sample, which can be reproduced stably locally.

#REPRODUCE
1. python -m http.server 1337; 
2. chrome --js-flags="--expose-gc --allow-natives-syntax" --no-sandbox --disable-extensions --user-data-dir=test --enable-logging=stderr http://localhost/fuzz1/poc2.html
3. Click havtest button,wait 10 sec
4. Reload page try again

### m....@gmail.com (2022-10-18)

Clean up irrelevant code
NOTE:
If not reproduce try again from step 2

```
<script src="help.js"></script>
<body>
<button id="button_fuzz" onclick="trigger1()">HavTest</button>
<iframe id="target" width=48 height=32></iframe>
<script>
async function trigger1() {
var v0789 = help_tag2id("IFrame",394);
var v0801 = new v0789.contentWindow.MediaStreamTrackGenerator("video");
var v0840 = new ImageCapture(v0801);
try{v0840.grabFrame()}catch(e){}

v0801=null
v0789.remove()
v0789 = null
gc();
setTimeout(function(){trigger1();},8000);
}
</script>
</body>
```

### m....@gmail.com (2022-10-18)

Fix error in reproduction description
chrome --js-flags="--expose-gc --allow-natives-syntax" --no-sandbox --disable-extensions --user-data-dir=test --enable-logging=stderr http://localhost:1337/poc2.html

### el...@chromium.org (2022-10-19)

The use of MediaStreamTrackGenerator in the PoC suggest Ben as the best owner for this.
(Please bounce back if incorrectly routed.)

### be...@chromium.org (2022-10-19)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-10-20)

Also found a case with my fuzzer running on CF
https://clusterfuzz.com/testcase-detail/5074303642173440


### be...@google.com (2022-10-20)

m.cooolie@gmail.com, could you please associate https://clusterfuzz.com/testcase-detail/5074303642173440 with this bug in order to grant access?

### m....@gmail.com (2022-10-20)

I don't have that permission, it needs to be set by the security team, CC amyressler@chromium.org.

### bo...@google.com (2022-10-20)

Thanks for the tidy POC! 

Confirming successful reproduction on Linux based on POC in https://crbug.com/chromium/1374294#c11 and https://crbug.com/chromium/1374294#c12. 

Repro on 108/Dev @ 1058931
Did not repro on 107/Beta @ 1047724
Did not repro on 106/Stable @ 1036826

Assigning Severity High per memory corruption in renderer process. 

### [Deleted User] (2022-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@google.com (2022-10-24)

The minimal repro seems to be

```
  let iframe = document.createElement('iframe');
  document.body.appendChild(iframe);
  let generator = new iframe.contentWindow.MediaStreamTrackGenerator({kind: 'video'});
  const capture = new ImageCapture(generator);
  capture.grabFrame();
```

I believe garbage collection triggers the codepath that results in the crash, and it depends on which object is destructed first.


### be...@google.com (2022-10-25)

If I understand the issue correctly, the following leads to the crash:
1. When the MediaStreamTrackGenerator is created, it takes its task runner from the iframe's context. [1]
2. grabFrame uses ScopedWebCallbacks to ensure that the promise is rejected if there's no explicit call to Resolve or Reject. The destructor callback is not bound to any task runner, which I believe is the bug. [2]
3. grabFrame also adds a sink to the MediaStreamTrackGenerator, which is a callback that transitively references the ScopedWebCallbacks.
4. When the iframe is removed, its task runner is stopped.
5. When the ImageCaptureFrameGrabber is garbage collected, its destructor calls DisconnectFromTrack. [3]
6. DisconnectFromTrack eventually ends up calling MediaStreamVideoTrack::FrameDeliverer::RemoveCallbackOnIO on the IO thread, which posts a task to its task runner. [4]
7. However, per step 4 above, the task runner is stopped. Thus the callback is destroyed without being run. [5] This triggers the destructor for ScopedWebCallbacks, which calls the destructor callback mentioned in step 2 above. This entire call chain is executed on the IO thread.
8. In an ASAN build, we get an access-violation because we are modifying memory belonging to the main thread on the IO thread. In a debug build, we get a DCHECK from ThreadCheckingCallbackWrapper. [6]

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/breakout_box/media_stream_track_generator.cc;l=90;drc=327a3573ed3d1ee29d433ee215e50947f1b94170
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/imagecapture/image_capture_frame_grabber.cc;l=312;drc=327a3573ed3d1ee29d433ee215e50947f1b94170
[3] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/media_stream_video_sink.cc;l=42;drc=327a3573ed3d1ee29d433ee215e50947f1b94170
[4] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/media_stream_video_track.cc;l=332;drc=327a3573ed3d1ee29d433ee215e50947f1b94170
[5] https://source.chromium.org/chromium/chromium/src/+/main:base/task/sequence_manager/task_queue_impl.cc;l=105;drc=327a3573ed3d1ee29d433ee215e50947f1b94170
[6] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/wtf/functional.h;l=225;drc=327a3573ed3d1ee29d433ee215e50947f1b94170

### gi...@appspot.gserviceaccount.com (2022-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/371321be741a021ca6800e8a96370dfa79f33545

commit 371321be741a021ca6800e8a96370dfa79f33545
Author: Ben Wagner <benjaminwagner@google.com>
Date: Wed Oct 26 14:51:46 2022

Bind a task runner to destructor callback for MakeScopedWebCallbacks

Bug: 1374294
Change-Id: I310ecbcff440f3e781133869beea7ebe212cb8f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3973075
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Auto-Submit: Ben Wagner <benjaminwagner@google.com>
Commit-Queue: Ben Wagner <benjaminwagner@google.com>
Cr-Commit-Position: refs/heads/main@{#1063795}

[modify] https://crrev.com/371321be741a021ca6800e8a96370dfa79f33545/third_party/blink/renderer/modules/imagecapture/image_capture_frame_grabber.cc
[add] https://crrev.com/371321be741a021ca6800e8a96370dfa79f33545/third_party/blink/web_tests/external/wpt/mediacapture-image/ImageCapture-grabFrame-crash.html


### be...@google.com (2022-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-26)

Requesting merge to dev M108 because latest trunk commit (1063795) appears to be after dev branch point (1058933).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@google.com (2022-10-26)

I didn't read https://crbug.com/chromium/1374294#c19 carefully enough earlier. I did a bisect gave a blamelist of https://chromium.googlesource.com/chromium/src/+log/636064b0f30c5df814cfb14d0cf9a26bd3478d2c..128b904d20ca2084d98bc6472620df0ee178b6c5. These two CLs seem very relevant:
 - https://chromium-review.googlesource.com/c/chromium/src/+/3901097
 - https://chromium-review.googlesource.com/c/chromium/src/+/3893052


### [Deleted User] (2022-10-27)

Merge review required: M108 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@google.com (2022-10-27)

1. Why does your merge fit within the merge criteria for these milestones?
Marked ReleaseBlock-Stable
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3982117
3. Have the changes been released and tested on canary?
No canary on Linux, and I don't have access to another device right now. First included in 109.0.5384.0.
4. Is this a new feature?
No
5. N/A
6. N/A


### be...@google.com (2022-10-28)

I got access to a Mac to test. Reproducible on 108.0.5359.19 (Official Build) dev (x86_64), not reproducible on 109.0.5386.0 (Official Build) canary (x86_64) .

### be...@google.com (2022-10-28)

1. Why does your merge fit within the merge criteria for these milestones?
Marked ReleaseBlock-Stable
2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/3982117
3. Have the changes been released and tested on canary?
Yes
4. Is this a new feature?
No
5. N/A
6. N/A

### be...@google.com (2022-10-31)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-31)

108 merge approved, please merge to branch 5359 at your earliest convenience -- thank you! 

### gi...@appspot.gserviceaccount.com (2022-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/333bf72b1f6b82d7d66b96fc89436df6b115e289

commit 333bf72b1f6b82d7d66b96fc89436df6b115e289
Author: Ben Wagner <benjaminwagner@google.com>
Date: Tue Nov 01 08:47:03 2022

[M108] Bind a task runner to destructor callback for MakeScopedWebCallbacks

(cherry picked from commit 371321be741a021ca6800e8a96370dfa79f33545)

Bug: 1374294
Change-Id: I310ecbcff440f3e781133869beea7ebe212cb8f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3973075
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Auto-Submit: Ben Wagner <benjaminwagner@google.com>
Commit-Queue: Ben Wagner <benjaminwagner@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1063795}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3982117
Commit-Queue: Kentaro Hara <haraken@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#468}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/333bf72b1f6b82d7d66b96fc89436df6b115e289/third_party/blink/renderer/modules/imagecapture/image_capture_frame_grabber.cc
[add] https://crrev.com/333bf72b1f6b82d7d66b96fc89436df6b115e289/third_party/blink/web_tests/external/wpt/mediacapture-image/ImageCapture-grabFrame-crash.html


### am...@chromium.org (2022-11-02)

my review during merge wasn't thorough enough at the time to catch that this issue is limited to a read; since it in the renderer process, reducing severity to medium 

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations on another one this week! The VRP Panel has decided to award you $5,000 for this report. Thank you for your efforts in discovering and reporting this issue to us! 

### be...@google.com (2022-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-03)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Bindings Blink>JavaScript>API]

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1374294?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Bindings, Blink>ImageCapture, Blink>JavaScript>API]
[Monorail mergedwith: crbug.com/chromium/1376922]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061335)*
