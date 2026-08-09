# Non trivial number of AutoCloseableRouter finalizer exceptions

| Field | Value |
|-------|-------|
| **Issue ID** | [496266444](https://issues.chromium.org/issues/496266444) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | Internals>Mojo>Bindings |
| **Platforms** | Android |
| **Reporter** | ds...@chromium.org |
| **Assignee** | dc...@chromium.org |
| **Created** | 2026-03-26 |
| **Bounty** | Confirmed (amount unknown) |

## Description

# Steps to reproduce the problem

gn args:

```
android_static_analysis = "off"
debuggable_apks = true
enable_android_secondary_abi = true
dcheck_always_on=false
is_debug=false
ffmpeg_branding = "Chrome"
is_component_build = false
proprietary_codecs = true
symbol_level = 2
target_cpu = "arm64"
target_os = "android"
use_reclient = false
use_siso = true
use_full_mte=true

```

apply patch.diff
enable mte on device

```
python3 -m http.server
adb reverse tcp:8000 tcp:8000

```

open <http://localhost:8000/poc.html>

observe crash on adb logcat

The uaf/double-free triggers around 50% of the time on my device
tested on commit 1fa21d15780b5f89014de6a7a27ada0b49fb4693

# Problem Description

With ipcz mojo handle ids are are normal pointers, meaning that any code that incorrectly closes mojo handles now
triggers a use-after-free / double free.

In the java code for ShareServiceImpl some handles are [handed to a background thread](https://source.chromium.org/chromium/chromium/src/+/main:components/browser_ui/webshare/android/java/src/org/chromium/components/browser_ui/webshare/ShareServiceImpl.java;drc=4bff3a323a0bc83feeb942f7a8233aba26ef4a1c;l=209) for processing. These handles can be closed by the renderer so that by the time the background thread processes them either the backing objects are used after being freed or freed again.

# Summary

Mojo handle double-close / use after close leads to uaf/double free

# Custom Questions

#### Type of crash:

browser crash

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.html](attachments/poc.html) (text/html, 184 B)
- [patch.diff](attachments/patch.diff) (text/x-diff, 4.4 KB)
- [trace.txt](attachments/trace.txt) (text/plain, 19.4 KB)
- [MojoWriteIpcz.txt](attachments/MojoWriteIpcz.txt) (text/plain, 15.3 KB)
- [updated_patch.diff](attachments/updated_patch.diff) (text/x-diff, 4.4 KB)

## Timeline

### da...@gmail.com (2026-03-28)

Okay, I looked a bit further into this, and while I don't really understand what is going on inside the trace I initially attached to be honest, one of the other crashes I observed are actually the ones I was aiming for :D.
What I think is happening inside the trace I attached:

- Mojo java code extracts id integer from java handle object and passes it through jni to ipcz
- UI thread closes the java handle object and thus also frees the c++ object
- Background task dereferences dangling pointer inside ipcz code

### dc...@chromium.org (2026-04-08)

I'll be honest; I don't quite know what's going on either. But seems legitimate enough and I'll triage it as such.

### dc...@chromium.org (2026-04-08)

(I'm assuming this requires a compromised renderer; if that assessment is wrong, please let me know)

### ch...@google.com (2026-04-08)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-08)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### da...@gmail.com (2026-04-08)

Hi, yes this requires a compromised renderer.
couple things:

1: I noticed a bug in my initial patch. The delay time passed from the js part of the poc is currently being ignored and the static delay part is always 15ms. I attached a fixed version. That being said, all the traces I attached before were generated with the buggy patch and it doesn't really seem to make a difference in terms of relieability on my phone.

2: Some of the crashes I observed seem to happen because a miracleptr protected object is being dereferenced,
but as far as I can tell at least the object that's being dereferenced in the trace I sent in #2 is not protected.

3. I unfortunately currently don't have a lot of free time to spend on this. I'll do more digging thursday next week if it's still useful by then.

### dm...@google.com (2026-04-17)

triaged, marking as available this sprint

### ar...@google.com (2026-04-20)

Vulnerability needs assignee

### di...@google.com (2026-04-21)

Taking a look at this.

### di...@google.com (2026-04-21)

My hunch is that this is happening somewhere [around here](https://source.chromium.org/chromium/chromium/src/+/main:components/browser_ui/webshare/android/java/src/org/chromium/components/browser_ui/webshare/ShareServiceImpl.java;l=276;drc=4bff3a323a0bc83feeb942f7a8233aba26ef4a1c).

`files[index].blob.blob` is a Mojo interface proxy (`org.chromium.blink.mojom.Blob.Proxy`), and calling `readAll()` on it in the background thread might be what is causing this crash. [Mojo proxies in Java are not thread safe by default](https://chromium.googlesource.com/chromium/src/+/HEAD/mojo/public/java/bindings/README.md#threading), so if the handle is closed or modified on the main thread simultaneously, it results in a use-after-free or invalid memory access.

### di...@google.com (2026-04-21)

I was able to make something work that doesn't crash Chrome, by making sure that the `ShareServiceImpl` runs [this code](https://source.chromium.org/chromium/chromium/src/+/main:components/browser_ui/webshare/android/java/src/org/chromium/components/browser_ui/webshare/ShareServiceImpl.java;l=276;drc=4bff3a323a0bc83feeb942f7a8233aba26ef4a1c) on the main thread, and then pass the output to the background thread. However, since `BlobReceiver` needs to do blocking file I/O, and `AsyncTask` doesn't have Android message loops, we need to make `BlobReceiver` support I/O operations for this to work. I got it to work using some form of a polling mechanism (waiting to get the reply back from the I/O thread), but that feels super hacky.

I'm also lowering the severity here, because I don't think this is a huge blocker. We should fix it for sure, but as seen from the provided diff patch, it needs a compromised renderer for this to happen.

Edit: The deprecated AsyncTask is a Java thingy, and not Chromium's AsyncTask.

### di...@google.com (2026-04-22)

Forgot to leave it here yesterday, but after trying out a few more fixes like using [`threadSafeProxy`](https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/java/bindings/src/org/chromium/mojo/bindings/Interface.java;l=404;bpv=1;bpt=1?q=buildThreadSafeProxy), I saw a couple of errors like the following:

```
04-22 20:10:02.066  9359  9376 E System  : java.lang.IllegalStateException: Warning: Router objects should be explicitly closed when no longer required otherwise you may leak handles.
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.AutoCloseableRouter.finalize(AutoCloseableRouter.java:113)
04-22 20:10:02.066  9359  9376 E System  : at java.lang.Daemons$FinalizerDaemon.doFinalize(Daemons.java:319)
04-22 20:10:02.066  9359  9376 E System  : at java.lang.Daemons$FinalizerDaemon.runInternal(Daemons.java:306)
04-22 20:10:02.066  9359  9376 E System  : at java.lang.Daemons$Daemon.run(Daemons.java:140)
04-22 20:10:02.066  9359  9376 E System  : at java.lang.Thread.run(Thread.java:1012)
04-22 20:10:02.066  9359  9376 E System  : Caused by: java.lang.Exception: AutocloseableRouter allocated at:
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.AutoCloseableRouter.<init>(AutoCloseableRouter.java:40)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.Interface$Manager.attachProxy(Interface.java:441)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.Interface$Manager.attachProxy(Interface.java:373)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.Decoder.readServiceInterface(Decoder.java:629)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.blink.mojom.SerializedBlob.decode(SerializedBlob.java:80)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.webshare.mojom.SharedFile.decode(SharedFile.java:72)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.webshare.mojom.ShareService_Internal$ShareServiceShareParams.decode(ShareService_Internal.java:259)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.webshare.mojom.ShareService_Internal$ShareServiceShareParams.deserialize(ShareService_Internal.java:213)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.webshare.mojom.ShareService_Internal$ShareServiceStub.acceptWithResponder(ShareService_Internal.java:175)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.RouterImpl.dispatchMessage(RouterImpl.java:269)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.RouterImpl.dispatchMessages(RouterImpl.java:237)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.RouterImpl.handleIncomingMessage(RouterImpl.java:222)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.RouterImpl$HandleIncomingMessageThunk.accept(RouterImpl.java:38)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.Connector.readAndDispatchMessage(Connector.java:197)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.Connector.readOutstandingMessages(Connector.java:162)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.Connector.onWatcherResult(Connector.java:140)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.bindings.Connector$WatcherCallback.onResult(Connector.java:131)
04-22 20:10:02.066  9359  9376 E System  : at org.chromium.mojo.system.impl.WatcherImpl.onHandleReady(WatcherImpl.java:65)
04-22 20:10:02.066  9359  9376 E System  : at android.os.MessageQueue.nativePollOnce(Native Method)
04-22 20:10:02.066  9359  9376 E System  : at android.os.MessageQueue.next(MessageQueue.java:335)
04-22 20:10:02.066  9359  9376 E System  : at android.os.Looper.loopOnce(Looper.java:161)
04-22 20:10:02.066  9359  9376 E System  : at android.os.Looper.loop(Looper.java:288)
04-22 20:10:02.066  9359  9376 E System  : at android.app.ActivityThread.main(ActivityThread.java:7872)
04-22 20:10:02.066  9359  9376 E System  : at java.lang.reflect.Method.invoke(Native Method)
04-22 20:10:02.066  9359  9376 E System  : at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:548)
04-22 20:10:02.066  9359  9376 E System  : at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:936)
04-22 20:10:02.066  9359  9376 E System  : Uncaught exception thrown by finalizer

```

which leads me to [b/40522265](https://issues.chromium.org/issues/40522265). I'll continue investigating) but I'm well out of my depth at this point. It seems more like a Mojo problem here.

### di...@google.com (2026-04-22)

I tried a bunch of things, and couldn't figure out exactly where the router objects should be closed, as all of these happen in the mojo layer. I'm going to route this to the mojo folks for debugging and seeing if there is a way we can fix this.

### dc...@chromium.org (2026-04-22)

I think the exception means that there's a Mojo endpoint that Java didn't explicitly close.

A `SerializedBlob` has an embedded remote to help keep the blob alive as long as its needed: <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/blob/serialized_blob.mojom;l=17;drc=047c7dc4ee1ce908d7fea38ca063fa2f80f92c77>

So after WebShare is done with the blob, it probably needs to clean it up explicitly. Presumably it's using the `Blob` interface somewhere to actually read the data. Unfortunately the Java parlance is all different, but I'm guessing it's `close()` on the proxy: <https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/java/bindings/src/org/chromium/mojo/bindings/Interface.java;l=152;drc=c04b8552deeef94794cf9ac76db0e8891a2d7b6a>

### dx...@google.com (2026-04-24)

Project: chromium/src  

Branch:  main  

Author:  Dibyajyoti Pal [dibyapal@google.com](mailto:dibyapal@google.com)  

Link:    <https://chromium-review.googlesource.com/7788291>

[WebShare] Explicitly close Finalizer objects after WebShare completes

---


Expand for full commit details
```
     
    This CL explicitly closes the router objects (mBlob and mConsumerHandle) 
    after WebShare is done with its work, preventing AutoCloseableRouter 
    finalizer exceptions from crashing Chromium. Doing this helps debug 
    "the" root cause of the stack trace on Chromium, which still occurs with 
    this change [1]. 
     
    [1] https://paste.googleplex.com/5945165350043648 
     
    Bug: 496266444 
    Change-Id: I52da2292e9b76d402eea4291c270cd65cb4a81a7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7788291 
    Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1619947}

```

---

Files:

- M `components/browser_ui/webshare/android/java/src/org/chromium/components/browser_ui/webshare/BlobReceiver.java`

---

Hash: [76185f621437fb01b9e98287e440b3fb766ea2e4](https://chromiumdash.appspot.com/commit/76185f621437fb01b9e98287e440b3fb766ea2e4)  

Date: Fri Apr 24 03:33:07 2026


---

### dx...@google.com (2026-04-25)

Project: chromium/src  

Branch:  main  

Author:  Dibyajyoti Pal [dibyapal@google.com](mailto:dibyapal@google.com)  

Link:    <https://chromium-review.googlesource.com/7791704>

[WebShare] Fix threading violations and race conditions in Android

---


Expand for full commit details
```
     
    This commit addresses several critical stability issues identified 
    in the Android WebShare file transfer implementation: 
     
    1. Fixes sequence affinity violations by moving the creation and 
       starting of the Mojo Watcher from the background thread pool to 
       the Main (UI) thread in ShareServiceImpl by utilizing 
       onPostExecute of the AsyncTask. 
    2. Decouples Mojo events from blocking file I/O in BlobReceiver by 
       posting the read operations to the USER_BLOCKING background 
       sequence. 
    3. Prevents use-after-free crashes and heap corruption by adding 
       state checks (mIsClosed) at callback entry points in 
       BlobReceiver, and reordering destruction in reportError to close 
       handles before executing callbacks. 
     
    Verified that this no longer causes Android chrome to crash or OOM 
    with the compromised poc and the renderer changes. Also verified 
    that "normal" share flow hasn't changed manually. 
     
    Fixed: 496266444 
    Change-Id: I6bcd235826fdfb1ece82bd0b8b25cc30d4a0d4fa 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7791704 
    Reviewed-by: Adriana Ixba <aixba@chromium.org> 
    Commit-Queue: Dibyajyoti Pal <dibyapal@chromium.org> 
    Reviewed-by: Daniel Murphy <dmurph@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1620567}

```

---

Files:

- M `components/browser_ui/webshare/android/java/src/org/chromium/components/browser_ui/webshare/BlobReceiver.java`
- M `components/browser_ui/webshare/android/java/src/org/chromium/components/browser_ui/webshare/ShareServiceImpl.java`

---

Hash: [5678c0f8a561cd9f93bd0f58a9352b314160e2cf](https://chromiumdash.appspot.com/commit/5678c0f8a561cd9f93bd0f58a9352b314160e2cf)  

Date: Sat Apr 25 00:03:40 2026


---

### ch...@google.com (2026-04-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-06-22)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

No evidence of UAF.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### da...@gmail.com (2026-06-22)

I don't quite understand the reasoning.  

I mean yes that's a pretty small race window to actually replace the object on the UI thread but the UAF itself was clearly there?  

The router object dereferenced in the trace from [comment #2](https://issues.chromium.org/issues/496266444#comment2) is the blob remote sent by the renderer to the browser process, so it's [allocated here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/ipcz/src/ipcz/router.cc;drc=d7643f2b864f3ed9bbd5b6f5f8b73ea1b7623374;l=747) with a MakeRefCounted<Router> which is not protected by miracleptr.  

How is an MTE report not evidence of a UAF here?

### aj...@google.com (2026-07-13)

Panel: see comment 20

### ch...@google.com (2026-07-14)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### sp...@google.com (2026-07-28)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided to issue a reward of
**$5000.00** for your report. Congratulations!

Rationale for this decision:

Mildly mitigated browser memory corruption. Mitigated browser crash by race.

Important payment guidance:

- **Legacy**: If you aren't already registered with Google as a supplier,
  [p2p-vrp@google.com](mailto:p2p-vrp@google.com) will reach out to you. If you have registered in the
  past, no need to repeat the process – you can sit back and relax, and we
  will process the payment soon.
  
  If you have any payment related requests, please direct them to
  [p2p-vrp@google.com](mailto:p2p-vrp@google.com). Please remember to include the subject of this email and
  the email address that the report was sent from.

Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot

P.S. One other thing we'd like to mention:

- Please do NOT publicly disclose details until a fix has been released to all
  our users. Early public disclosure may cancel the provisional reward. Also,
  please be considerate about disclosure when the bug affects a core library
  that may be used by other products. Please do NOT share this information
  with third parties who are not directly involved in fixing the bug. Doing so
  may cancel the provisional reward. Please be honest if you have already
  disclosed anything publicly or to third parties. Lastly, we understand that
  some of you are not interested in money. We offer the option to donate your
  reward to an eligible charity. Any rewards that are unclaimed after 12
  months will be donated to a charity of our choosing.

Please contact [security-vrp@chromium.org](mailto:security-vrp@chromium.org) with any questions.

### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Mildly mitigated browser memory corruption. Mitigated browser crash by race. 
> 
> 
> 
> 
> 
> 
> 
>   
>     
>   
> 
> 
> Important payment guidance:
> 
> 
> *   **Legacy**: If you aren't already registered with Google as a supplier,
>     p2p-vrp@google.com will reach out to you. If you have registered in the
>     past, no need to repeat the process – you can sit back and relax, and we
>     will process the payment soon.
> 
>     If you have any payment related requests, please direct them to
>     p2p-vrp@google.com. Please remember

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496266444)*
