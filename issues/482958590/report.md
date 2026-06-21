# Use-After-Free in WMPI

| Field | Value |
|-------|-------|
| **Issue ID** | [482958590](https://issues.chromium.org/issues/482958590) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 144.0.0.0 |
| **Reporter** | ss...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2026-02-09 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. .\chrome.exe --js-flags="--expose-gc"

# Problem Description

Use-After-Free occurs when a parent object is destroyed by GC while accessing a WMPI object.  

GC can be called via the [0] function.  

There are several places where this function can be called, but I chose to use the [1] function.  

To call the [1] function directly without timing it, I called the [2] function.\

[0]`https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/media/web_media_player_impl.cc;l=3334;drc=e63596721df61bbc199c38c4a102597ad81ad154`
[1]`https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/media/web_media_player_impl.cc;l=1860;drc=e63596721df61bbc199c38c4a102597ad81ad154`
[2]`https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/media/renderer_web_media_player_delegate.cc;l=335;drc=e63596721df61bbc199c38c4a102597ad81ad154;bpv=0;bpt=1`

This vulnerability didn't work properly in the ASAN build, so I triggered it using Chromium built using the args.gn below.  

Also, since the crash didn't occur in the release version without spraying, I used poc\_helper.diff for the crash test below, and attached the crash dump log instead of the ASAN log.\

```
is_component_build = false
is_debug = false
dcheck_always_on = false
is_asan = false
enable_nacl = false

```

I believe the vulnerability started with commit `50a635ebbf250f8f35ea060d564b102b804dcea7`.

# Summary

Use-After-Free in WMPI

# Custom Questions

#### Type of crash:

renderer

#### Reporter credit:

sherkito

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [repro.html](attachments/repro.html) (text/html, 2.0 KB)
- [repro.webm](attachments/repro.webm) (video/webm, 38.3 MB)
- [poc_helper.diff](attachments/poc_helper.diff) (text/x-diff, 581 B)
- [crash.log](attachments/crash.log) (text/plain, 7.1 KB)

## Timeline

### ss...@gmail.com (2026-02-09)

The chromium commit that reproduced the trigger is `5a6e2727eb1deb24bbe5451ff26ffbc9d3bbd4e2`.  

need to apply and run poc\_helper.diff in the reproduce step.

### el...@chromium.org (2026-02-11)

Security shepherd: thanks for the report. To be clear, does this actually crash (or otherwise do something) in either an official Chrome build or an ASAN build? Or does it only reproduce in builds with the given patch applied?

### ss...@gmail.com (2026-02-12)

This patch is intended to reference vftable for crash testing purposes in release builds. (If testing is performed without this patch, the freed object simply references `integer` member variables, preventing crashes.)  

Due to the vulnerability's sensitive GC triggering process, ASAN builds failed, so we implemented the patch and reported the issue as described above.  

That is, it is a vulnerability that causes crashes in normal Chrome and Chromium.

### pe...@google.com (2026-02-12)

Thank you for providing more feedback. Adding the requester to the CC list.

### li...@chromium.org (2026-02-12)

This looks v8 related since it requires the `expose-gc` flag so I'm sending it to the v8 sheriff to confirm

### om...@google.com (2026-02-12)

I'm not seeing anything in the repro that would be V8 related. IIUC The call to `gc()` is just a trigger or a way to force a specific timing.   

I believe the issue is likely somewhere in `media::PipelineController` or `media::PipelineImpl`.   

Unassigning myself to get this issue retriaged.

### ss...@gmail.com (2026-02-13)

To be more specific, this vulnerability occurs when the GarbageCollector is triggered by calling the WebMediaPlayerImpl::ReportMemoryUsage function (function [0]) via function [1]. During this process, while accessing the simple MediaPlayerImpl object, the parent GC object, the MediaElement object, is freed, and then the WebMediaPlayerImpl member object is referenced. (Of course, as you can see in the code, the member reference occurs even without applying the patch. I simply called the function that references the vftable for simple testing.)  

The member reference occurs at `https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/media/web_media_player_impl.cc;l=1862;drc=e63596721df61bbc199c38c4a102597ad81ad154`.

The key commits affecting this vulnerability are:  

`https://source.chromium.org/chromium/chromium/src/+/50a635ebbf250f8f35ea060d564b102b804dcea7`   

`https://source.chromium.org/chromium/chromium/src/+/83266c7462e414731592d6e7946de4ccb10f8a5a`  

It's related to these two parts. I hope this helps you identify the appropriate point of contact for this fix.

### ch...@google.com (2026-02-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2026-02-13)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ma...@google.com (2026-02-13)

dalecurtis@, PTAL?

### da...@chromium.org (2026-02-23)

I've been OOO so just seeing this today. Will try to take a look this week, but digging out of OOO and sheriff today. Since I see memory dump mentioned above cc: @jo...@google.com since he was looking at that recently.

### jo...@google.com (2026-02-23)

Dug into this a bit. The `ReportMemoryUsage()` function has nothing to do with this. If the `MediaPlayerImpl` object must already be deleted when `OnPipelineSuspended()` was called. From inside `OnPipelineSuspended()` the `this` pointer on the stack would keep `MediaPlayerImpl` alive even if the owning `MediaElement` is deleted. (I had to double-check on this because I don't usually work in blink: see "Conservative GC" at <https://chromium.googlesource.com/v8/v8/+/main/include/cppgc/README.md#precise-and-conservative-garbage-collection>.)

From the attached crash.log, `OnPipelineSuspended()` is called from here:

```
00 00000028`939fe0d0 00007ff8`8116b2a5     chrome!blink::WebMediaPlayerImpl::OnPipelineSuspended+0x231 
01 00000028`939fe150 00007ff8`81ee53d1     chrome!base::RepeatingCallback<void ()>::Run+0x55 
02 00000028`939fe1a0 00007ff8`81ee61e9     chrome!media::PipelineController::OnPipelineStatus+0xf1 
...
06 00000028`939fe210 00007ff8`8181718b     chrome!base::internal::Invoker<base::internal::FunctorTraits<...,base::WeakPtr<media::PipelineController> &&,...>::RunOnce+0x79 
07 00000028`939fe280 00007ff8`818935ab     chrome!base::OnceCallback<void (media::TypedStatus<media::EncoderStatusTraits>)>::Run+0x4b 
08 00000028`939fe2d0 00007ff8`870d1475     chrome!media::PipelineImpl::OnSuspendDone+0x8b 

```

So `OnSuspendDone()` invokes a callback that's bound to a `WeakPtr`: it will safely do nothing if the `PipelineController` is dead. Then `PipelineController::OnPipelineStatus()` invokes a callback bound to `OnPipelineSuspended`, which must be the problem. That callback should be using a `WeakPtr` or `Persistent` or something to ensure that the `WebMediaPlayerImpl` is still alive when it's invoked.

### jo...@google.com (2026-02-23)

(Removing myself since this doesn't seem to be memory-dump-related.)

### jo...@google.com (2026-02-23)

Ok, one more comment: all the obvious callbacks in `PipelineController` are bound at <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/media/web_media_player_impl.cc;l=524;drc=44c3d61b466d13e43fd307e40b0c64d95be1e793> and use `WeakPtr`, except for `error_cb_` which is:

```
BindRepeating(&media::DemuxerManager::OnPipelineError,
                    Unretained(demuxer_manager_.get())

```

A comment as `demuxer_manager_` outlives the `PipelineController`. Worth double-checking that, but assuming it's correct, `DemuxerManager::OnPipelineError()` immediately starts accessing a `client_` member [which is](https://source.chromium.org/chromium/chromium/src/+/main:media/filters/demuxer_manager.h;l=178;drc=5e79cb4e366b8582752f0a1ca757125a05d905eb):

```
  // This is usually just the WebMediaPlayerImpl.
  raw_ptr<Client, DanglingUntriaged> client_;

```

So I bet the `WebMediaPlayerImpl` can be deleted without clearing that `raw_ptr`.

### ss...@gmail.com (2026-02-24)

The core of this vulnerability is `ReportMemoryUsage`.  

The functions proceed in the following order: `ReportMemoryUsage` -> `RespondToDemuxerMemoryUsageReport` -> `FinishMemoryUsageReport`.

In the `RespondToDemuxerMemoryUsageReport` function, since the current DemuserType object is `DemuxerType::kChunkDemuxer`, the `FinishMemoryUsageReport` function is called synchronously.

```
void WebMediaPlayerImpl::FinishMemoryUsageReport(int64_t demuxer_memory_usage) {
DCHECK(main_task_runner_->BelongsToCurrentThread());

const auto stats = GetPipelineStatistics(); 
const int64_t data_source_memory_usage = 
demuxer_manager_->GetDataSourceMemoryUsage(); 
''' 
''' 
const int64_t video_memory_usage = 
stats.video_memory_usage + 
((pipeline_metadata_.has_video && !stats.video_memory_usage && 
has_first_frame_) 
? media::VideoFrame::AllocationSize(media::PIXEL_FORMAT_I420, 
pipeline_metadata_.natural_size) 
: 0); 

const int64_t current_memory_usage =
stats.audio_memory_usage + video_memory_usage + data_source_memory_usage +
demuxer_memory_usage;

'''
'''
const int64_t delta = current_memory_usage - last_reported_memory_usage_;
last_reported_memory_usage_ = current_memory_usage;
external_memory_accounter_.Update(isolate_.get(), delta);
}

```

The `FinishMemoryUsageReport` function executes code like `external_memory_accounter_.Update`, which calls the `GarbageCollector`, causing the vulnerability.  

The code then accesses the `WebMediaPlayerImpl` object within the `if (pending_suspend_resume_cycle_)` block, but the object is already freed at this point, leading to a Use-After-Free vulnerability. When `poc_helper.diff` is applied, a reference to the object's vftable occurs instead of the aforementioned if statement logic.

```
void Heap::HandleExternalMemoryInterrupt() {
  const GCCallbackFlags kGCCallbackFlagsForExternalMemory =
      static_cast<GCCallbackFlags>(
          kGCCallbackFlagSynchronousPhantomCallbackProcessing |
          kGCCallbackFlagCollectAllExternalMemory);
  uint64_t current = external_memory();
  '''
  '''
  if (current > external_memory_hard_limit()) {
    TRACE_EVENT2("devtools.timeline,v8", "V8.ExternalMemoryPressure",
                 "external_memory_mb", static_cast<int>((current) / MB),
                 "external_memory_hard_limit_mb",
                 static_cast<int>((external_memory_hard_limit()) / MB));
    CollectAllGarbage(
        GCFlag::kReduceMemoryFootprint,
        GarbageCollectionReason::kExternalMemoryPressure,
        static_cast<GCCallbackFlags>(kGCCallbackFlagCollectAllAvailableGarbage |
                                     kGCCallbackFlagsForExternalMemory));
    return;
  }
  '''
  '''
}

```

As you can see from the description, it is a similar vulnerability type to `https://crbug.com/448046109`.

### ss...@gmail.com (2026-02-24)

My personal analysis regarding [Comment #14](https://issues.chromium.org/issues/482958590#comment14) and [Comment #16](https://issues.chromium.org/issues/482958590#comment16) is as follows:  

First, `WebMediaPlayerImpl` is an off-heap object allocated via PartitionAllocator, which means it cannot be marked through stack scanning (this would only be possible if the parent object, `HTMLMediaElement`, were being used as this).  

Furthermore, there is no function between `OnPipelineStatus` and `OnPipelineSuspended` that could trigger the destruction of the object. Of course, the `PipelineController::OnPipelineStatus` task itself cannot proceed if the object has been deleted, thanks to the `WeakPtr` check.

Secondly, Regarding the `media::DemuxerManager::OnPipelineError` function: even if the destruction of `demuxer_manager_` is delayed via an asynchronous `DeleteSoon`, this remains a synchronous call.  

Since it is part of the `PipelineController` task sequence, it cannot be invoked if `WebMediaPlayerImpl` has already been destroyed.  

Additionally, the `WebMediaPlayerImpl` destructor calls `DemuxerManager::StopAndResetClient`, which explicitly overwrites the `raw_` pointer with NULL.

Please let me know if there are any errors in my analysis. Thank you.

### da...@chromium.org (2026-02-24)

Thanks, yeah I was just thinking this sounded like [issue 448046109](https://issues.chromium.org/issues/448046109). I'll see if a similar fix resolve the issue here.

### da...@chromium.org (2026-02-24)

Unfortunately, I've been unable to reproduce this. Will keep poking at it since it does seem like another version of the sam issue.

### ss...@gmail.com (2026-02-25)

If you haven't been able to reproduce the issue yet, please try the following:  

By adjusting the outermost `setTimeout` to `15000` and the `sourcebuffer_array loop count` to `0xa0`, the issue should be consistently reproducible across various systems.  

Properly balancing the timeout and loop count is key to reproducing this behavior.

### da...@chromium.org (2026-03-05)

I was never able to reproduce, but given we know this pattern is problematic, I've switched destruction of the WMP classes to be posted. Let me know if you can still reproduce after <https://crrev.com/c/7609443>

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7609443>

Always post destruction of WebMediaPlayer instances

---


Expand for full commit details
```
     
    There are lots of ways that re-entrant destruction of players can 
    happen. Fixing them all piecemeal is fragile and making WMP garbage 
    collected is difficult since it's a blink/public interface. For now 
    just add a Shutdown mechanism and post destruction such that we 
    never have re-entrant destruction. 
     
    Bug: 482958590, 459524033 
    Change-Id: I9ccdaeed448850a5133deb464dcaeafa7447fe94 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7609443 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Reviewed-by: Frank Liberato <liberato@chromium.org> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1595039}

```

---

Files:

- M `third_party/blink/public/platform/web_media_player.h`
- M `third_party/blink/public/web/modules/mediastream/web_media_player_ms.h`
- M `third_party/blink/renderer/core/exported/web_media_player_impl_unittest.cc`
- M `third_party/blink/renderer/core/html/media/html_media_element.cc`
- M `third_party/blink/renderer/modules/mediacapturefromelement/html_video_element_capturer_source_unittest.cc`
- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`
- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms_test.cc`
- M `third_party/blink/renderer/platform/media/web_media_player_impl.cc`
- M `third_party/blink/renderer/platform/media/web_media_player_impl.h`
- M `third_party/blink/renderer/platform/testing/empty_web_media_player.h`

---

Hash: [2f6df874594524706ee2d13883ff889b4c9cd1d8](https://chromiumdash.appspot.com/commit/2f6df874594524706ee2d13883ff889b4c9cd1d8)  

Date: Fri Mar 6 00:33:22 2026


---

### ss...@gmail.com (2026-03-06)

I've confirmed that the vulnerability is no longer reproducible.

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7644110>

[WMPI] Ensure stats reporters and timers stop before destruction

---


Expand for full commit details
```
     
    R=liberato 
     
    Fixed: 490325378, 490370724, 490381710 
    Bug: 482958590 
    Change-Id: Ibcc765e12c884bfd01bcc2078217cda30924ffbd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644110 
    Reviewed-by: Frank Liberato <liberato@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1595604}

```

---

Files:

- M `third_party/blink/renderer/platform/media/web_media_player_impl.cc`

---

Hash: [4c7280839692f83af68e239667bb9df25825b513](https://chromiumdash.appspot.com/commit/4c7280839692f83af68e239667bb9df25825b513)  

Date: Fri Mar 6 20:12:19 2026


---

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7644708>

[WMP-MS] Ensure timers are stopped during Shutdown.

---


Expand for full commit details
```
     
    R=liberato 
     
    Fixed: 490381614 
    Bug: 482958590 
    Change-Id: I5f754369cd85d52265e606b0b2008bf7623f50b3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7644708 
    Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1595727}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`

---

Hash: [2d6f077745b6fd0d956bf851b2fcf517d99d91a2](https://chromiumdash.appspot.com/commit/2d6f077745b6fd0d956bf851b2fcf517d99d91a2)  

Date: Fri Mar 6 23:03:24 2026


---

### da...@chromium.org (2026-03-10)

This should be fixed, but there may be some fallout from posting that needs further addressing.

### ch...@google.com (2026-03-10)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-03-10)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1595727) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1595727) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1595727) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: M144 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M145 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M146 is already shipping to stable.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### da...@chromium.org (2026-03-10)

I'd avoid merging this back unless we feel we have to, it seems hard to exploit and the fixes may have undiscovered blast radius.

### dr...@chromium.org (2026-03-11)

Sure, given the raciness here lowering the security risk, I'm happy to skip the merge.

### dx...@google.com (2026-03-11)

Project: chromium/src  

Branch:  main  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7655311>

[WMPI] Cancel background video track status updates

---


Expand for full commit details
```
     
    R=liberato 
     
    Fixed: 491576311 
    Bug: 482958590 
    Change-Id: I6a7e797d80f3138622fa4a25fd472f71c2041af9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7655311 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Frank Liberato <liberato@chromium.org> 
    Reviewed-by: Frank Liberato <liberato@chromium.org> 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1597469}

```

---

Files:

- M `third_party/blink/renderer/platform/media/web_media_player_impl.cc`

---

Hash: [6fac5f11ed19049b72953ab2eab4a0dc076a3aba](https://chromiumdash.appspot.com/commit/6fac5f11ed19049b72953ab2eab4a0dc076a3aba)  

Date: Wed Mar 11 01:49:13 2026


---

### dx...@google.com (2026-03-14)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7664367>

[M147] [WMPI] Cancel background video track status updates

---


Expand for full commit details
```
     
    Original change's description: 
    > [WMPI] Cancel background video track status updates 
    > 
    > R=liberato 
    > 
    > Fixed: 491576311 
    > Bug: 482958590 
    > Change-Id: I6a7e797d80f3138622fa4a25fd472f71c2041af9 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7655311 
    > Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    > Commit-Queue: Frank Liberato <liberato@chromium.org> 
    > Reviewed-by: Frank Liberato <liberato@chromium.org> 
    > Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1597469} 
     
    (cherry picked from commit 6fac5f11ed19049b72953ab2eab4a0dc076a3aba) 
     
    Bug: 492633940,491576311,482958590 
    Change-Id: I6a7e797d80f3138622fa4a25fd472f71c2041af9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7664367 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#305} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `third_party/blink/renderer/platform/media/web_media_player_impl.cc`

---

Hash: [1f2f95d8acfa55306ae5574a87755850e2ed6f38](https://chromiumdash.appspot.com/commit/1f2f95d8acfa55306ae5574a87755850e2ed6f38)  

Date: Sat Mar 14 03:44:09 2026


---

### pe...@google.com (2026-03-14)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### da...@chromium.org (2026-03-16)

As noted in [comment#30](https://issues.chromium.org/issues/482958590#comment30) and confirmed in [comment#31](https://issues.chromium.org/issues/482958590#comment31), we shouldn't merge this back.

### vi...@google.com (2026-03-18)

Hi. I've labeled `LTS-NotApplicable-138` and `LTS-NotApplicable-144` because [comment#30](https://issues.chromium.org/issues/482958590#comment30) and [comment#31](https://issues.chromium.org/issues/482958590#comment31) mentioned low exploitability, concern about potential instability from the fixes, and the "raciness" is considered to lower the overall security risk.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure with bisect.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/482958590)*
