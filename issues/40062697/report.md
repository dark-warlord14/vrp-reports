# UAF in blink::VideoFrameSubmitter::OnContextLost

| Field | Value |
|-------|-------|
| **Issue ID** | [40062697](https://issues.chromium.org/issues/40062697) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>Video |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2023-01-16 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:ubuntu22.04  

chromium version:  

Chromium 111.0.5523.0( gs://chromium-browser-asan/linux-release/asan-linux-release-1091147.zip)  

Chromium 110.0.5481.24(custom asan build)  

repro steps:

1. setup simple http server:  
   
   python -m SimpleHTTPServer 8000
2. patch chromium source.  
   
   diff --git a/third\_party/blink/renderer/platform/graphics/video\_frame\_submitter.cc b/third\_party/blink/renderer/platform/graphics/video\_frame\_submitter.cc  
   
   index 92d678f772fd1..d6c0e1ded9963 100644  
   
   --- a/third\_party/blink/renderer/platform/graphics/video\_frame\_submitter.cc  
   
   +++ b/third\_party/blink/renderer/platform/graphics/video\_frame\_submitter.cc  
   
   @@ -184,8 +184,14 @@ VideoFrameSubmitter::VideoFrameSubmitter(

VideoFrameSubmitter::~VideoFrameSubmitter() {  

DCHECK\_CALLED\_ON\_VALID\_THREAD(thread\_checker\_);  

if (context\_provider\_){

- ```
   LOG(ERROR)<<"[0]sleep start...";  
  
  ```
- ```
   sleep(10);  
  
  ```
- ```
   LOG(ERROR)<<"[1]sleep end...";  
  
  ```
  
  context\_provider\_->RemoveObserver(this);
- }
  
  // Release VideoFrameResourceProvider early since its destruction will make  
  
  // calls back into this class via the viz::SharedBitmapReporter interface.

3. run chromium with command:  
   
   ./chrome --use-fake-device-for-media-stream --use-fake-ui-for-media-stream <http://localhost:8605/crash2/> --incognito --user-data-dir=/tmp/xx6 --no-sandbox  
   
   4.Close the browser as soon as the "[1] sleep end..." message appears in the console. After waiting for a few seconds, the use-after-free issue will repro.  
   
   Additional repro information:
   - This issue is related to race, and maybe it is difficult to reproduce without patching.
   - The |context\_provider\_|[0] holds a reference to the object of the class RasterContextProvider.So if you repro in a virtual machine, you should need to install a virtual graphics card.  
     
     [0]<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/graphics/video_frame_submitter.h;drc=503535015a7b373cc6185c69c991e01fda5da571;l=148>

**Problem Description:**  

analysis:  

The VideoFrameSubmitter class contains a raw pointer, video\_frame\_provider\_[1], which points to an object of type cc::VideoFrameProvider,and is initialized in the WebMediaPlayerMSCompositor::InitializeSubmitter(), and is not released in the destructor of the VideoFrameSubmitter class.  

void WebMediaPlayerMSCompositor::InitializeSubmitter() {  

DCHECK(video\_frame\_compositor\_task\_runner\_->BelongsToCurrentThread());  

submitter\_->Initialize(this, /\* is\_media\_stream = \*/ true);  

}

Under normal circumstances, the release process of video\_frame\_provider\_ is as follows:  

(a)WebMediaPlayerMSCompositorTraits::Destruct()[3]  

(b)delete compositor;[3]  

(c)WebMediaPlayerMSCompositor::~WebMediaPlayerMSCompositor()[4]  

(d)video\_frame\_compositor\_task\_runner\_->DeleteSoon(FROM\_HERE,std::move(submitter\_))[4]  

(e)VideoFrameSubmitter::~VideoFrameSubmitter() [5]  

(f)context\_provider\_->RemoveObserver(this);[5]  

The problem is that in (d),schedules the submitter\_ object for deletion on video\_frame\_compositor\_task\_runner\_.  

So it does not guarantee that the object will be deleted immediately after it is called. It's possible that the deletion will be delayed if the task runner is busy with other tasks. If submitter\_ is not called, (f) will not be executed. If `observer.OnContextLost()`(6) is triggered at this point in time, it will eventually lead to uaf(7).

```
// static  
void WebMediaPlayerMSCompositorTraits::Destruct(           ------->(a)    
    const WebMediaPlayerMSCompositor\* compositor) {  
  if (!compositor->video_frame_compositor_task_runner_  
           ->BelongsToCurrentThread()) {  
    PostCrossThreadTask(  
        \*compositor->video_frame_compositor_task_runner_, FROM_HERE,  
        CrossThreadBindOnce(&WebMediaPlayerMSCompositorTraits::Destruct,  
                            CrossThreadUnretained(compositor)));  
    return;  
  }  
  delete compositor;   ------->(b)  
}  

```
```
WebMediaPlayerMSCompositor::~WebMediaPlayerMSCompositor() {       ---->(c)  
  // Ensured by destructor traits.  
  DCHECK(video_frame_compositor_task_runner_->BelongsToCurrentThread());  
  
  if (submitter_) {  
    video_frame_compositor_task_runner_->DeleteSoon(FROM_HERE,  
                                                    std::move(submitter_)); ---->(d)  
  } else {  
    DCHECK(!video_frame_provider_client_)  
        << "Must call StopUsingProvider() before dtor!";  
  }  
}  

```
```
VideoFrameSubmitter::~VideoFrameSubmitter() {     ---->(e)  
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);  
  if (context_provider_)  
    context_provider_->RemoveObserver(this);   ---->(f)  
  
  // Release VideoFrameResourceProvider early since its destruction will make  
  // calls back into this class via the viz::SharedBitmapReporter interface.  
  resource_provider_.reset();  
}  

```

Here is the log I added.  

pwn11@pwn11:~/www/crash2$ /home/pwn11/chromium/src/out/test/chrome --use-fake-device-for-media-stream --use-fake-ui-for-media-stream <http://localhost:8000/crash2/> --incognito --user-data-dir=/tmp/xx6 --no-sandbox  

[750486:750693:0116/233549.497833:ERROR:webmediaplayer\_ms\_compositor.cc(269)] [\*CREATE\*]WebMediaPlayerMSCompositor::InitializeSubmitter()-this=0x6140000e7c40,submitter\_=0x618000040480  

//\*video\_frame\_provider\_ initilized\*  

[750486:750693:0116/233549.514648:ERROR:webmediaplayer\_ms\_compositor.cc(269)] [\*CREATE\*]WebMediaPlayerMSCompositor::InitializeSubmitter()-this=0x6140000e8840,submitter\_=0x618000040880  

[750486:750693:0116/233549.519640:ERROR:webmediaplayer\_ms\_compositor.cc(243)] [\*FREE\*][0]~WebMediaPlayerMSCompositorthis=0x6140000e7c40,submitter\_=0x618000040480  

//\*The desctruction of a video\_frame\_provider\_ completed successfully\*  

[750486:750693:0116/233549.519750:ERROR:video\_frame\_submitter.cc(189)] [\*FREE\*][1]~~VideoFrameSubmitter()=>RemoveObserver()=>this = 0x618000040480, context\_provider\_ = 0x6150000ae190, video\_frame\_provider\_ = 0x6140000e7c40  

[750486:750693:0116/233549.519813:ERROR:video\_frame\_submitter.cc(190)] [0]sleep start...  

\*close browser here\*  

[750486:750688:0116/233551.695206:ERROR:context\_provider\_command\_buffer.cc(493)] [\*USE\*][0]ContextProviderCommandBuffer::OnLostContext  

[750486:750500:0116/233551.695301:ERROR:context\_provider\_command\_buffer.cc(493)] [\*USE\*][0]ContextProviderCommandBuffer::OnLostContext  

[750486:750500:0116/233551.695675:ERROR:context\_provider\_command\_buffer.cc(493)] [\*USE\*][0]ContextProviderCommandBuffer::OnLostContext  

pwn11@pwn11:~~/www/crash2$ [750486:750693:0100/000000.519964:ERROR:video\_frame\_submitter.cc(192)] [1]sleep end...  

[750486:750693:0100/000000.520295:ERROR:webmediaplayer\_ms\_compositor.cc(269)] [\*CREATE\*]WebMediaPlayerMSCompositor::InitializeSubmitter()-this=0x6140000e9840,submitter\_=0x618000041080  

//\*video\_frame\_provider\_ deleted\*  

[750486:750693:0100/000000.520390:ERROR:webmediaplayer\_ms\_compositor.cc(243)] [\*FREE\*][0]~WebMediaPlayerMSCompositorthis=0x6140000e8840,submitter\_=0x618000040880

```
//\*trigger observer callback\*  
[750486:750693:0100/000000.532193:ERROR:context_provider_com  
  
**Additional Comments:**   
  
  
**Chrome version: ** 110.0.5481.24 **Channel: ** Not sure  
  
**OS:** Linux

```

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.0 KB)
- [test.png](attachments/test.png) (image/png, 376 B)
- [asan.log](attachments/asan.log) (text/plain, 35.9 KB)
- [repro.mov](attachments/repro.mov) (video/quicktime, 6.3 MB)
- deleted (application/octet-stream, 0 B)
- [crash3.html](attachments/crash3.html) (text/plain, 1.8 KB)
- [check.log](attachments/check.log) (text/plain, 12.5 KB)
- [crash4.html](attachments/crash4.html) (text/plain, 1.2 KB)
- [gpu_oom.html](attachments/gpu_oom.html) (text/plain, 427 B)

## Timeline

### [Deleted User] (2023-01-16)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-01-16)

Sorry,there is error by my autofill extention.please ignore this sentence.
*, and is not released in the destructor of the VideoFrameSubmitter class.*

### em...@gmail.com (2023-01-16)

[Empty comment from Monorail migration]

### bo...@google.com (2023-01-17)

Thanks for the report. 

I'm unable to reproduce, but it's possibly related to timing. Is it feasible to make the POC trigger reliably? I'm testing the POC on a fast machine with a GPU (no VM) and each attempt is taking minutes without printing the sleep messages from the patch. How long does the POC typically take to trigger in your testing? 

### em...@gmail.com (2023-01-17)

"[0]sleep start..." will show very quickly, and the repro is almost 100%. I'm temporarily not sure why it could'nt repro for a few minutes in your pc.
I  uploaded a repro video here to see if it can help you locate the repro problem.

### em...@gmail.com (2023-01-17)

Could you please check if the value of context_provider_ is empty?
VideoFrameSubmitter::~VideoFrameSubmitter() {
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);
  + LOG(ERROR)<<"context_provider_"<<context_provider_;

### em...@gmail.com (2023-01-17)

I modified the poc. Please try this one.

### em...@gmail.com (2023-01-17)

[Empty comment from Monorail migration]

### em...@gmail.com (2023-01-17)

[Empty comment from Monorail migration]

### bo...@google.com (2023-01-18)

I've spent a couple hours trying to repro the various POCs and I've been unable to do so on a Linux workstation with NVIDIA GPU. 

An unreliable POC is not a deal breaker, but it seriously hampers our ability to do root cause analysis. However, since the report includes a suggested root cause that looks plausible enough, I'm going to invite an owner of the code to take a look. 

I will hold off on setting the usual security triage flags until we get input from an owner. 

Owner(s) - Apologies for looping you in without being able to repro first as we would normal prefer. Please treat this as a tentatively valid security bug that would give an attacker remote code execution in the renderer sandbox, which we'd regard as a high severity bug. We need your help to work out whether this bug is valid, and if so, how to fix. I'll keep an eye on your feedback and set the security flags accordingly. Thank you!

[Monorail components: Blink>Media>Video]

### da...@chromium.org (2023-01-18)

video_frame_provider_ should only be used when surface layer is disabled -- which is only used on WebView IIRC. We also call StopUsingProvider() which should null it out before starting the destruction process.

I'm not clear on exactly what variable is supposedly used after free? Sorry if I'm misreading.

### em...@gmail.com (2023-01-18)

[Comment Deleted]

### em...@gmail.com (2023-01-18)

Sorry, some content in the previous report did not go into detail.
`video_frame_provider_` can be initialized from `WebMediaPlayerMSCompositor`[0] or `VideoFrameCompositor`[1].
There are two branches in the `MediaFactory::CreateMediaPlayer()` function that will call `VideoFrameSubmitter::Initialize()`[3]. If
`source.IsMediaStream()`[2] is true, `WebMediaPlayerMSCompositor` will be created and `video_frame_provider_` will be initialized from `WebMediaPlayerMSCompositor`. If source.IsMediaStream() is false, `VideoFrameCompositor` will be created and `video_frame_provider_` will be initialized from `VideoFrameCompositor`.
If `video_frame_provider_` initialized from  VideoFrameCompositor, StopUsingProvider() will be called in the destructor [4] of VideoFrameCompositor, and video_frame_provider_ will also be set to nullptr. But if video_frame_provider_ is initialized from WebMediaPlayerMSCompositor, there is no similar cleanup code in WebMediaPlayerMSCompositor's destructor[5].


[0]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc;drc=3ec715d325b2cac20ff4987f46e238a4b19cc131;l=268
[1]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/media/video_frame_compositor.cc;drc=3ec715d325b2cac20ff4987f46e238a4b19cc131;l=76
[2]https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/media/media_factory.cc;drc=adac219925ef5d9c9a954d189c2e4b8852a4bbed;l=379
[3]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/graphics/video_frame_submitter.cc;drc=aff3b5b1f9a377ec59b599200d2fbe6611941361;l=243
[4]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/media/video_frame_compositor.cc;drc=3ec715d325b2cac20ff4987f46e238a4b19cc131;l=81
[5]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc;drc=3ec715d325b2cac20ff4987f46e238a4b19cc131;l=239

### da...@chromium.org (2023-01-18)

We seem to call WMPMS::StopUsingProvider here?
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc;l=417;drc=aff3b5b1f9a377ec59b599200d2fbe6611941361

The WMPMSC destructor has a DCHECK that StopUsingProvider has already been called. WMPSC ref counted traits always posts to that thread too, so it seems like that should be called.

### em...@gmail.com (2023-01-19)

I just tested it. `compositor_->StopUsingProvider()` will indeed be called. But `video_frame_provider_client_`[0] is always empty, so `video_frame_provider_client_->StopUsingProvider()` will not be called. There are two places, WebMediaPlayerMSCompositor::EnableSubmission[1] and WebMediaPlayerMSCompositor::SetVideoFrameProviderClient[2] will assign to video_frame_provider_client_. But the two places are not called, and I haven't found the reason yet.
BTW, I can reproduce this uaf without patch. The result is the same as that reproduced after patch. So this uaf and patch are irrelevant.

[0] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc;drc=3ec715d325b2cac20ff4987f46e238a4b19cc131;l=879
[1]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc;drc=3ec715d325b2cac20ff4987f46e238a4b19cc131;l=297
[2]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc;drc=3ec715d325b2cac20ff4987f46e238a4b19cc131;l=354

### da...@chromium.org (2023-01-19)

Wasn't able to to reproduce on Windows FWIW.

### em...@gmail.com (2023-01-19)

I don't have windows, so I haven't tested it, but I tested it on a mac, and I couldn't reproduce it. I can only reproduce it stably in linux (with patching).

### em...@gmail.com (2023-01-19)

I probably found why video_frame_provider_client_ is empty when ~WebMediaPlayerMSCompositor() call.
The `video_frame_provider_client_` assignment call chain  is as follows:
void WebMediaPlayerMSCompositor::EnableSubmission
void WebMediaPlayerMS::ActivateSurfaceLayerForVideo
void WebMediaPlayerMS::OnFirstFrameReceived

but`~VideoFrameSubmitter()` sometimes executes earlier than OnFirstFrameReceived, causing `video_frame_provider_client_` to be empty, eventually triggering use-after-free.

### da...@chromium.org (2023-01-19)

Those all queue tasks on video_frame_compositor_task_runner_ though, the same task runner that StopUsingProviderInternal is queued on. So if ~WMPMS has run, it seems it can't be possible that StopUsingProviderInternal sees a nullptr for video_frame_provider_client_. 

I've been home sick so haven't been able to try on Linux this week.

### em...@gmail.com (2023-01-20)

I am here just to record and sync my progress of analysis. You can check it again after you fully recover next week. :)
After the WMPMS is created, it can be quickly deleted from the entry 'ClearMediaPlayerAndAudioSourceProviderClientWithoutLocking()' before the 'OnFirstFrameReceived' is called to initialize the 'video_frame_provider_client_'. I only added a 'CHECK(video_frame_provider_client_);' in the original chromium source code 'StopUsingProviderInternal()' (without adding the 'sleep' function in the original report), and it will trigger this error soon. I have uploaded the attachment.
```
void HTMLMediaElement::ResetMediaPlayerAndMediaSource() {
  CloseMediaSource();

  {
    AudioSourceProviderClientLockScope scope(*this);
    ClearMediaPlayerAndAudioSourceProviderClientWithoutLocking();
  }

  if (audio_source_node_)
    GetAudioSourceProvider().SetClient(audio_source_node_);
}
```
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/media/html_media_element.cc;drc=45d49ba699e90c06a2c9c454d1c317784980cac9;l=4364

tested chrome version: Chromium 110.0.5481.24
Command to run:
./chrome --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --incognito --user-data-dir=/tmp/xx6 --no-sandbox http://localhost:8000/crash3.html

### he...@google.com (2023-01-23)

Are you ok to own this, Dale? I've not get my head around the lifecycles just yet so don't have any suggestions.

### da...@chromium.org (2023-01-23)

Can take a look tomorrow when I'm back in the office.

### da...@chromium.org (2023-01-25)

I wasn't able to reproduce either. Emily, were you ever able to reproduce w/o closing the browser / tab? I'm wondering if we're in a situation where a PostTask/DeleteSoon is dropped because the main thread task runner is being shut down.

### em...@gmail.com (2023-01-25)

Manually closing will immediately trigger 'mojo::InterfaceEndpointClient::NotifyError' (to be precise, gpu.mojom.CommandBufferClient), which ultimately calls 'VideoFrameSubmitter::OnContextLost()' in this stack. 
So this issue can be reproduced  w/o closing the browser, as long as 'gpu::CommandBuffer ProxyImpl::OnDisconnect()' is called, uaf will be triggered.
I have two methods of reproducing this. 
Method 1: 
1. First, open the browser. 
./chrome --use-fake-device-for-media-stream --use-fake-ui-for-media-stream http://localhost:8000 --incognito --user-data-dir=/tmp/xx6 --no-sandbox 
2. Click on crash4.html in the page list.
3. Confirm the GPU process PID and kill it. 
ps -aux|grep type=gpu 
kill -9 pid. Method 
Method 2: 
Through the HTML code, trigger the GPU process OOM to trigger uaf. 
1. First, open the browser. 
./chrome --use-fake-device-for-media-stream --use-fake-ui-for-media-stream http://localhost:8000 --incognito --user-data-dir=/tmp/xx6 --no-sandbox 
2. Open two pages, the first page click crash4.html, the second page click gpu_oom.html. Wait for a while here, and it will reproduce UAF. Note: the above two methods are tested with the patch (sleep(10) in the original report).

tested version(Chromium 111.0.5545.6)
is_asan = true
is_debug = false
enable_nacl = false
treat_warnings_as_errors = false
is_component_build=false
dcheck_always_on = false

### em...@gmail.com (2023-01-25)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-25)

Okay, GPU crash shouldn't trigger task runner tear down, so that would mean it can reproduce normally. Will take a look when I'm back on Linux tomorrow.

### da...@chromium.org (2023-01-26)

I was able to get a reproduction. I think Emily is right that EnableSubmission is delayed and thus the client is not set and thus StopUsingProvider isn't called.

The fix seems like it would be to set client when Submitter::Initialize() is called, but need to make sure that doesn't explode anything.

### da...@chromium.org (2023-01-26)

Here's my speculative fix: https://chromium-review.googlesource.com/c/chromium/src/+/4195824

I wasn't able to reproduce reliably, so can you test that patch and see if it still reproduces for you Emily?

### em...@gmail.com (2023-01-27)

Confirmed.
I tested in 3 ways, and the issue did not repro after patching.
(1)Fix
(2)Fix + sleep(10)(from original report),
(3)Fix + CHECK(video_frame_provider_client_)(from #20);

### da...@chromium.org (2023-01-27)

Great, thanks for checking! Looks like it blows up a few things, so will try to sort those out today.

### da...@chromium.org (2023-01-27)

I realize the cause might be simpler. Can you try the latest patch set on https://chromium-review.googlesource.com/c/chromium/src/+/4195824 again Emily? 

### em...@gmail.com (2023-01-28)

Confirmed.
After many tests, the issue has not been reproduced.
I think this fix is ​​very clear (consistent with the destructor logic of VideoFrameCompositor).
Thanks.

### da...@chromium.org (2023-01-28)

Great thanks for confirming!

### gi...@appspot.gserviceaccount.com (2023-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cbd238e85903b7d94910bd2c6362ff9abf9908cc

commit cbd238e85903b7d94910bd2c6362ff9abf9908cc
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Mon Jan 30 10:14:12 2023

Simplify WebMediaPlayerMSCompositor destruction.

The code was only sometimes calling StopUsingProvider() and posted
the submitter destruction unnecessarily.

Destruction now works the same as in VideoFrameCompositor, where the
class itself is responsible for calling StopUsingProvider() during
its own destruction.

Fixed: 1407701
Change-Id: Ia649cb5532519468eea34e12745ed9c990580d82
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4195824
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Reviewed-by: Frank Liberato <liberato@chromium.org>
Reviewed-by: Tony Herre <toprice@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1098505}

[modify] https://crrev.com/cbd238e85903b7d94910bd2c6362ff9abf9908cc/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc
[modify] https://crrev.com/cbd238e85903b7d94910bd2c6362ff9abf9908cc/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.h
[modify] https://crrev.com/cbd238e85903b7d94910bd2c6362ff9abf9908cc/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc


### [Deleted User] (2023-01-30)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2023-01-30)

Defer to bookholt@ for severity labels. It looks like it has existed since the launch of SurfaceLayer in 2018.

### bo...@google.com (2023-01-30)

Thanks everyone for your help with triage and diagnosis. 

Setting security bits as follows:
- FoundIn-108 because this issue predates all our current supported releases, so 108 is the farthest back we'll go. 
- Severity High because UAF in renderer sandbox
- Priority 1 (due to High severity) - although this is a NOOP since the bug is now fixed.
- All Blink platforms, i.e. everything except iOS. 

### [Deleted User] (2023-01-30)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-31)

Looks like my "fix" is causing a similar crash to show up in the wild now. Will take a look today.

### [Deleted User] (2023-01-31)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2023-01-31)

https://chromium-review.googlesource.com/c/chromium/src/+/4210508

### gi...@appspot.gserviceaccount.com (2023-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1622bffc6534a0cc4f53d07c43e0cd8f49975d10

commit 1622bffc6534a0cc4f53d07c43e0cd8f49975d10
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Wed Feb 01 09:36:42 2023

Further simplify WebMediaPlayerMSCompositor lifetime.

Due to the raw pointer held by VideoFrameSubmitter, there may be
tasks pending on the compositor task runner after the RefCounted
traits have "destructed" WebMediaPlayerMSCompositor. Through this
raw pointer VFS was invoking OnContextLost which attempts to use
the zero ref count compositor.

The solution here is again similar to VideoFrameCompositor, its
destruction should be explicit instead of a tangle of RefCounted
owners.

Fixed: 1407701, 1411601
Change-Id: Ic77294d1113d54ab83bc0f5b625a997edf57bf7c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4210508
Reviewed-by: Tony Herre <toprice@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1099726}

[modify] https://crrev.com/1622bffc6534a0cc4f53d07c43e0cd8f49975d10/third_party/blink/public/web/modules/mediastream/webmediaplayer_ms.h
[modify] https://crrev.com/1622bffc6534a0cc4f53d07c43e0cd8f49975d10/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc
[modify] https://crrev.com/1622bffc6534a0cc4f53d07c43e0cd8f49975d10/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.h
[modify] https://crrev.com/1622bffc6534a0cc4f53d07c43e0cd8f49975d10/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc


### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

Requesting merge to extended stable M108 because latest trunk commit (1099726) appears to be after extended stable branch point (1058933).

Requesting merge to stable M109 because latest trunk commit (1099726) appears to be after stable branch point (1070088).

Requesting merge to beta M110 because latest trunk commit (1099726) appears to be after beta branch point (1084008).

Requesting merge to dev M111 because latest trunk commit (1099726) appears to be after dev branch point (1097615).

Merge review required: M108 is already shipping to stable.

Merge review required: M110 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [108, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2023-02-01)

1. https://chromium-review.googlesource.com/c/chromium/src/+/4195824 and https://chromium-review.googlesource.com/c/chromium/src/+/4210508
2. Yes
3. Should probably soak a few more days.
4. No.
5. No.

### [Deleted User] (2023-02-02)

Merge approved: your change passed merge requirements and is auto-approved for M111. Please go ahead and merge the CL to branch 5563 (refs/branch-heads/5563) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-02)

Merge review required: M109 is already shipping to stable.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2023-02-02)

1. Security fix.
2. https://chromium-review.googlesource.com/c/chromium/src/+/4195824 and https://chromium-review.googlesource.com/c/chromium/src/+/4210508
3. Should soak until tomorrow.
4. No
5. n/a
6. n/a

### da...@chromium.org (2023-02-03)

No new crashes or issues on canary/dev so will start merging now.

### am...@chromium.org (2023-02-03)

there are no further planned releases of M108/Extended or M109/Stable, removing labels accordingly
Please hold off merging to M110 just yet, purposely have left this in the merge review queue as M110/Stable RC has been cut for release on Tuesday and want to make sure we aren't adding fixes if a recut is needed for any platform before Tuesday's release -- thank you! 
Merging to M111 is a-okay right now though! 

### da...@chromium.org (2023-02-03)

Yes, sorry to be clear I was only going to merge to the approved branches.

### am...@chromium.org (2023-02-03)

ah awesome, tysm! 

### da...@chromium.org (2023-02-04)

M111 merge is here: https://chromium-review.googlesource.com/c/chromium/src/+/4220900

### gi...@appspot.gserviceaccount.com (2023-02-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f3141b1661d35ce366368da970b40108e23517b0

commit f3141b1661d35ce366368da970b40108e23517b0
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Mon Feb 06 15:58:57 2023

[M111] Combined WebMediaPlayerCompositor cleanups.

Simplify WebMediaPlayerMSCompositor destruction:
cbd238e85903b7d94910bd2c6362ff9abf9908cc

The code was only sometimes calling StopUsingProvider() and posted
the submitter destruction unnecessarily.

Destruction now works the same as in VideoFrameCompositor, where the
class itself is responsible for calling StopUsingProvider() during
its own destruction.

Further simplify WebMediaPlayerMSCompositor lifetime:
1622bffc6534a0cc4f53d07c43e0cd8f49975d10

Due to the raw pointer held by VideoFrameSubmitter, there may be
tasks pending on the compositor task runner after the RefCounted
traits have "destructed" WebMediaPlayerMSCompositor. Through this
raw pointer VFS was invoking OnContextLost which attempts to use
the zero ref count compositor.

The solution here is again similar to VideoFrameCompositor, its
destruction should be explicit instead of a tangle of RefCounted
owners.

R=toprice

Fixed: 1407701, 1411601
Change-Id: Ib6e67fb802b7f8f33e7a290f10de9bc282a55368
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4220900
Commit-Queue: Tony Herre <toprice@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Tony Herre <toprice@chromium.org>
Cr-Commit-Position: refs/branch-heads/5563@{#191}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/f3141b1661d35ce366368da970b40108e23517b0/third_party/blink/public/web/modules/mediastream/webmediaplayer_ms.h
[modify] https://crrev.com/f3141b1661d35ce366368da970b40108e23517b0/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc
[modify] https://crrev.com/f3141b1661d35ce366368da970b40108e23517b0/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.h
[modify] https://crrev.com/f3141b1661d35ce366368da970b40108e23517b0/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc


### [Deleted User] (2023-02-06)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### rz...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-09)

Congratulations on another one, Cassidy Kim! The VRP panel has decided to award you $3,000 for this report of a moderately mitigated bug, including bonus as we found your additional analysis and continued communication with the developer to be especially beneficial and helpful. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@chromium.org (2023-02-10)

M110 merge approved, please merge to branch 5481 at your earliest convenience -- ty! 

### da...@chromium.org (2023-02-10)

110 merge here https://chromium-review.googlesource.com/c/chromium/src/+/4237939

### gi...@appspot.gserviceaccount.com (2023-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5b049614dbf51b35c61b6cacd7f63e472ca92ab6

commit 5b049614dbf51b35c61b6cacd7f63e472ca92ab6
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Fri Feb 10 07:08:06 2023

[M110] Combined WebMediaPlayerCompositor cleanups.

Simplify WebMediaPlayerMSCompositor destruction:
cbd238e85903b7d94910bd2c6362ff9abf9908cc

The code was only sometimes calling StopUsingProvider() and posted
the submitter destruction unnecessarily.

Destruction now works the same as in VideoFrameCompositor, where the
class itself is responsible for calling StopUsingProvider() during
its own destruction.

Further simplify WebMediaPlayerMSCompositor lifetime:
1622bffc6534a0cc4f53d07c43e0cd8f49975d10

Due to the raw pointer held by VideoFrameSubmitter, there may be
tasks pending on the compositor task runner after the RefCounted
traits have "destructed" WebMediaPlayerMSCompositor. Through this
raw pointer VFS was invoking OnContextLost which attempts to use
the zero ref count compositor.

The solution here is again similar to VideoFrameCompositor, its
destruction should be explicit instead of a tangle of RefCounted
owners.

R=​toprice

(cherry picked from commit f3141b1661d35ce366368da970b40108e23517b0)

Fixed: 1407701, 1411601
Change-Id: Ib6e67fb802b7f8f33e7a290f10de9bc282a55368
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4220900
Commit-Queue: Tony Herre <toprice@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5563@{#191}
Cr-Original-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4237939
Cr-Commit-Position: refs/branch-heads/5481@{#1072}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/5b049614dbf51b35c61b6cacd7f63e472ca92ab6/third_party/blink/public/web/modules/mediastream/webmediaplayer_ms.h
[modify] https://crrev.com/5b049614dbf51b35c61b6cacd7f63e472ca92ab6/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc
[modify] https://crrev.com/5b049614dbf51b35c61b6cacd7f63e472ca92ab6/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.h
[modify] https://crrev.com/5b049614dbf51b35c61b6cacd7f63e472ca92ab6/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc


### rz...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-10)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-02-10)

1. 2 CLs https://chromium-review.googlesource.com/q/topic:%225359_1407701%22
2. Low, one simple naming conflict in one of the CLs
3. 112
4. Yes

### gm...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### gm...@google.com (2023-02-13)

Merged to 110. Approving for 108.

### rz...@google.com (2023-02-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-02-16)

1. 2 CLs https://chromium-review.googlesource.com/q/topic:%225005_1407701%22
2. Low, simple naming and parameter conflicts in one of the CLs
3. 110
4. Yes

### gm...@google.com (2023-02-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/999cc7185e93efb4a8d79e94887043adfd05ec88

commit 999cc7185e93efb4a8d79e94887043adfd05ec88
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Mon Feb 20 10:08:49 2023

[M108-LTS] Simplify WebMediaPlayerMSCompositor destruction.

The code was only sometimes calling StopUsingProvider() and posted
the submitter destruction unnecessarily.

Destruction now works the same as in VideoFrameCompositor, where the
class itself is responsible for calling StopUsingProvider() during
its own destruction.

(cherry picked from commit cbd238e85903b7d94910bd2c6362ff9abf9908cc)

Fixed: 1407701
Disallow-Recycled-Builds: test-failures
Change-Id: Ia649cb5532519468eea34e12745ed9c990580d82
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4195824
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1098505}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4225498
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1391}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/999cc7185e93efb4a8d79e94887043adfd05ec88/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc
[modify] https://crrev.com/999cc7185e93efb4a8d79e94887043adfd05ec88/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.h
[modify] https://crrev.com/999cc7185e93efb4a8d79e94887043adfd05ec88/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc


### gi...@appspot.gserviceaccount.com (2023-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f0b3a54c53c9aa6fc60220ac15fb36fe2e56eff

commit 0f0b3a54c53c9aa6fc60220ac15fb36fe2e56eff
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Mon Feb 20 13:16:32 2023

[M108-LTS] Further simplify WebMediaPlayerMSCompositor lifetime.

M108 merge issues:
  third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc:
    - video_task_runner_ is named io_task_runner_ in 108

  third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc:
    - video_task_runner_ is named io_task_runner_ in 108 (conflict in ReplaceCurrentFrameWithACopy)

Due to the raw pointer held by VideoFrameSubmitter, there may be
tasks pending on the compositor task runner after the RefCounted
traits have "destructed" WebMediaPlayerMSCompositor. Through this
raw pointer VFS was invoking OnContextLost which attempts to use
the zero ref count compositor.

The solution here is again similar to VideoFrameCompositor, its
destruction should be explicit instead of a tangle of RefCounted
owners.

(cherry picked from commit 1622bffc6534a0cc4f53d07c43e0cd8f49975d10)

Fixed: 1407701, 1411601
Change-Id: Ic77294d1113d54ab83bc0f5b625a997edf57bf7c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4210508
Commit-Queue: Tony Herre <toprice@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1099726}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4225393
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1392}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/0f0b3a54c53c9aa6fc60220ac15fb36fe2e56eff/third_party/blink/public/web/modules/mediastream/webmediaplayer_ms.h
[modify] https://crrev.com/0f0b3a54c53c9aa6fc60220ac15fb36fe2e56eff/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc
[modify] https://crrev.com/0f0b3a54c53c9aa6fc60220ac15fb36fe2e56eff/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.h
[modify] https://crrev.com/0f0b3a54c53c9aa6fc60220ac15fb36fe2e56eff/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc


### gi...@appspot.gserviceaccount.com (2023-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca8d6a6ea67531cdab278e3c5648227ecff00271

commit ca8d6a6ea67531cdab278e3c5648227ecff00271
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Mon Feb 20 13:36:56 2023

[M102-LTS] Simplify WebMediaPlayerMSCompositor destruction.

The code was only sometimes calling StopUsingProvider() and posted
the submitter destruction unnecessarily.

Destruction now works the same as in VideoFrameCompositor, where the
class itself is responsible for calling StopUsingProvider() during
its own destruction.

(cherry picked from commit cbd238e85903b7d94910bd2c6362ff9abf9908cc)

Fixed: 1407701
Change-Id: Ia649cb5532519468eea34e12745ed9c990580d82
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4195824
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Tony Herre <toprice@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1098505}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4227731
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1435}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/ca8d6a6ea67531cdab278e3c5648227ecff00271/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc
[modify] https://crrev.com/ca8d6a6ea67531cdab278e3c5648227ecff00271/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.h
[modify] https://crrev.com/ca8d6a6ea67531cdab278e3c5648227ecff00271/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc


### gi...@appspot.gserviceaccount.com (2023-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bd19ef529fc969ee83d77a1522ad2eb7bdf04ac0

commit bd19ef529fc969ee83d77a1522ad2eb7bdf04ac0
Author: Dale Curtis <dalecurtis@chromium.org>
Date: Mon Feb 20 15:23:51 2023

[M102-LTS] Further simplify WebMediaPlayerMSCompositor lifetime.

M102 merge issues:
  third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc:
    - video_task_runner_ is named io_task_runner_ in 102
    - Conflicting arguments for CrossThreadBindOnce in ActivateSurfaceLayerForVideo()

  third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc:
    - The use_surface_layer check is different in 102
    - video_task_runner_ is named io_task_runner_ in 102 (conflict in
      ReplaceCurrentFrameWithACopy)

Due to the raw pointer held by VideoFrameSubmitter, there may be
tasks pending on the compositor task runner after the RefCounted
traits have "destructed" WebMediaPlayerMSCompositor. Through this
raw pointer VFS was invoking OnContextLost which attempts to use
the zero ref count compositor.

The solution here is again similar to VideoFrameCompositor, its
destruction should be explicit instead of a tangle of RefCounted
owners.

(cherry picked from commit 1622bffc6534a0cc4f53d07c43e0cd8f49975d10)

Fixed: 1407701, 1411601
Change-Id: Ic77294d1113d54ab83bc0f5b625a997edf57bf7c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4210508
Commit-Queue: Tony Herre <toprice@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1099726}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4225497
Reviewed-by: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1436}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/bd19ef529fc969ee83d77a1522ad2eb7bdf04ac0/third_party/blink/public/web/modules/mediastream/webmediaplayer_ms.h
[modify] https://crrev.com/bd19ef529fc969ee83d77a1522ad2eb7bdf04ac0/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.cc
[modify] https://crrev.com/bd19ef529fc969ee83d77a1522ad2eb7bdf04ac0/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms_compositor.h
[modify] https://crrev.com/bd19ef529fc969ee83d77a1522ad2eb7bdf04ac0/third_party/blink/renderer/modules/mediastream/webmediaplayer_ms.cc


### rz...@google.com (2023-02-20)

[Empty comment from Monorail migration]

### rz...@google.com (2023-02-20)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-20)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1407701?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1411601]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062697)*
