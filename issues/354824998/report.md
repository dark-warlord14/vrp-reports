# heap-use-after-free on content::OverlayStateObserverImpl::Create

| Field | Value |
|-------|-------|
| **Issue ID** | [354824998](https://issues.chromium.org/issues/354824998) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Platforms** | Windows |
| **Reporter** | ki...@gmail.com |
| **Assignee** | fr...@microsoft.com |
| **Created** | 2024-07-23 |
| **Bounty** | $2,000.00 |

## Description

deleted

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [uaf-asan.log](attachments/uaf-asan.log) (text/plain, 28.5 KB)

## Timeline

### ki...@gmail.com (2024-07-23)

deleted

### ki...@gmail.com (2024-07-23)

Hello, I have analyzed the RCA, however the time is now too late for me to write it. Please don't assign this issue for now.

### ma...@chromium.org (2024-07-23)

[security shepherd]

Thanks for the report! I look forward to the root cause analysis. Have you had any luck in simplifying the proof-of-concept? It's very complex at the moment.

### ki...@gmail.com (2024-07-24)

## VULNERABILITY DETAILS

heap-use-after-free on content::OverlayStateObserverImpl::Create

## BISECTION

a28a7b4f4d86192a04281fc6f952c38d0eede0bd

```
MF Frame Server Mode: Part 5: Promotion Hint Service

This change introduces the underpinnings for an Overlay State Service
on Windows. This service will live in the GPU process where it will
track the overlay state of opted in textures.

In the initial implementation the DC Overlay Processor provides state
information during texture processing, a future update will likely
also incorporate state information like video capture.

The service is exposed to renderer clients via GPU channel and the
service allows the client to subscribe for notifications based on the
mailbox of the associated texture.

A basic promotion state service & aggregator are introduced to track
observers & current state. A future update will likely introduce
additional logic into the aggregator to help minimize IPC.

Bug: 1258887
Change-Id: I1b69155079bce6f4d22e1e33626ceadc0c2aa325
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3403933
Reviewed-by: Xiaohan Wang <xhwang@chromium.org>
Reviewed-by: Sunny Sachanandani <sunnyps@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: William Carr <wicarr@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#995427}

```
## Root Cause Analysis

0. Bind `OverlayStateServiceProvider` to `UnsafeDanglingUntriaged`
   
   ```
   media::ObserveOverlayStateCB observe_overlay_state_cb = base::BindRepeating(
       &OverlayStateObserverImpl::Create,
       base::UnsafeDanglingUntriaged(
           render_thread->GetOverlayStateServiceProvider())); // BIND HERE
   
   ```
1. Execution path
   
   ```
   void MediaFoundationRendererClient::InitializeFramePool(
       mojom::FramePoolInitializationParametersPtr pool_info) {
     DCHECK_GT(pool_info->frame_textures.size(), static_cast<size_t>(0));
   
     // Release our references to the video pool so that once the
     // rendering is complete the memory will be freed.
     video_frame_pool_.clear();
   
     for (const auto& frame_info : pool_info->frame_textures) {
       dcomp_texture_wrapper_->CreateVideoFrame(
           pool_info->texture_size, std::move(frame_info->texture_handle),
           base::BindOnce(
               &MediaFoundationRendererClient::OnFramePoolVideoFrameCreated,
               weak_factory_.GetWeakPtr(), frame_info->token));
     }
   }
   
   ```
2. The callback `create_video_frame_cb` will run in `media_task_runner_`, that means `MediaFoundationRendererClient::OnFramePoolVideoFrameCreated` will also be executed in `media_task_runner_`.
   
   ```
   void DCOMPTextureWrapperImpl::CreateVideoFrame(
       const gfx::Size& natural_size,
       gfx::GpuMemoryBufferHandle dx_handle,
       CreateDXVideoFrameCB create_video_frame_cb) {
     DCHECK(media_task_runner_->RunsTasksInCurrentSequence());
   [...]
   
     std::move(create_video_frame_cb).Run(video_frame_texture, mailbox);
   }
   
   ```
3. Finnally `OverlayStateObserverImpl::Create` will be executed in `media_task_runner_` too.
   
   ```
   MediaFoundationRendererClient::ObserveMailboxForOverlayState(
       const gpu::Mailbox& mailbox) {
     std::unique_ptr<OverlayStateObserverSubscription> observer_subscription;
   
     // If the rendering strategy is dynamic then setup an OverlayStateObserver to
     // respond to promotion changes. If the rendering strategy is Direct
     // Composition or Frame Server then we do not need to listen & respond to
     // overlay state changes.
     if (rendering_strategy_ == MediaFoundationClearRenderingStrategy::kDynamic) {
       // 'observe_overlay_state_cb_' creates a content::OverlayStateObserver to
       // subscribe to overlay state information for the given 'mailbox' from the
       // Viz layer in the GPU process. We hold an OverlayStateObserverSubscription
       // since a direct dependency on a content object is not allowed. Once the
       // OverlayStateObserverSubscription is destroyed the OnOverlayStateChanged
       // callback will no longer be invoked, so base::Unretained(this) is safe to
       // use.
       observer_subscription = observe_overlay_state_cb_.Run( //called 
           mailbox, base::BindRepeating(
                       &MediaFoundationRendererClient::OnOverlayStateChanged,
                       base::Unretained(this), mailbox));
       DCHECK(observer_subscription);
     }
   
     return observer_subscription;
   }
   
   ```
4. As the backtrace demonstrates, if the `overlay_state_service_provider_->IsLost()` condition is true, the `overlay_state_service_provider_` is released and recreated, this step will result in a UAF.
   
   This part of the operation will be performed on the main thread.
   
   ```
   OverlayStateServiceProvider*
   RenderThreadImpl::GetOverlayStateServiceProvider() {
     DCHECK(IsMainThread());
     // Only set 'overlay_state_service_provider_' if Media Foundation for clear
     // is enabled.
     if (media::SupportMediaFoundationClearPlayback()) {
       if (!overlay_state_service_provider_ ||
           overlay_state_service_provider_->IsLost()) {
         scoped_refptr<gpu::GpuChannelHost> channel = EstablishGpuChannelSync();
         if (!channel) {
           overlay_state_service_provider_ = nullptr;
           return nullptr;
         }
         overlay_state_service_provider_ =
             std::make_unique<OverlayStateServiceProviderImpl>(std::move(channel));
       }
     }
   
     return overlay_state_service_provider_.get();
   }
   
   ```

## VERSION

Chrome Version: tested in chromium head: c1bb405c44f662afcd8b3cae8dc0135518d1d5ba

Operating System: tested in Windows

## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: tab

Crash State: see asan log

## CREDIT INFORMATION

Reporter credit: Nan Wang(@eternalsakura13) and Zhenghang Xiao(@Kipreyyy) of 360 Vulnerability Research Institute

### pe...@google.com (2024-07-24)

Thank you for providing more feedback. Adding the requester to the CC list.

### ma...@chromium.org (2024-07-24)

[security shepherd]
Thanks for that detailed analysis. Do you have a proof of concept you can share? It can help us to understand the conditions necessary to trigger the bug from web content and which platforms it affects.

### ki...@gmail.com (2024-07-24)

This vulnerability likely does not require user interaction, but it does require a race condition, making a stable proof of concept difficult.

However, the problem is evident from the RCA. Additionally, since the vulnerable function only affects Windows, I believe it does not impact other platforms.

### ki...@gmail.com (2024-07-24)

There are some errors and inconvenient information in the initial report [comment#1](https://issues.chromium.org/issues/354824998#comment1) and [comment#2](https://issues.chromium.org/issues/354824998#comment2); please do not restore it. Additionally, you can assign an appropriate owner to review it according to this link: <https://chromium.googlesource.com/chromium/src/+/a28a7b4f4d86192a04281fc6f952c38d0eede0bd>.
For example, CC it to the owner of the Overlay component.

### pe...@google.com (2024-07-24)

The NextAction date has arrived: 2024-07-24
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ma...@chromium.org (2024-07-24)

[security shepherd]

Assigning to mfoltz@ based on content/renderer/media/OWNERS. If there is a better assignee, please feel free to reassign.

mfoltz@, the Security Team is unable to reproduce this issue based on information provided. If you can diagnose and fix the issue based on the ASan report and analysis provided by the reporter, please proceed accordingly.

### pe...@google.com (2024-07-25)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-25)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@chromium.org (2024-07-25)

updating component and other Media owners for visibility; also cc'ing wicarr@ of MSFT since it appears they have done some *relatively* recent work in this area

### da...@chromium.org (2024-07-26)

wicarr@ has left Microsoft, so please cc frankli@ instead for new MSFT issues.

### ki...@gmail.com (2024-08-01)

Hello, is there any update? Thanks!

### ar...@chromium.org (2024-08-07)

(secondary security shepherd)

**TLDR:**

- The bug is likely [(Protected by MiraclePtr)](https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#toc-miracleptr), however the fact we have two threads: one releasing the memory, and one holding a ~dangling raw\_ptr<T> make it so that I can't be 100% affirmative.
- Assignee: mfoltz as OWNER, as @frankli isn't responding.

---

Thanks for the detailed instruction!

This is a callback invoked with a dangling pointer, causing a UAF.

The dangling pointer reported here was found in March 2024 (+CC @paulsemel) using some MiraclePtr extension for callbacks.
<https://chromium-review.googlesource.com/c/chromium/src/+/5355853>

Paul linked a real some reports that this bugs occurs in practise.

Since then, MiraclePtr has been enabled in non-renderer processes across all Chrome platforms and release channels since M118, we are no longer considering BRP-protected UAFs as security issues as of M128. This has been updated in the [severity guidelines](https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#toc-miracleptr).

The ASAN reports says:

```
MiraclePtr Status: MANUAL ANALYSIS REQUIRED
This crash occurred inside a callback where a raw_ptr<T> pointing to the same region was bound to one of the arguments.
The "use" and "free" threads don't match. This crash is likely to have been caused by a race condition that is mislabeled as a use-after-free. Make sure that the "free" is sequenced after the "use" (e.g. both are on the same sequence, or the "free" is in a task posted after the "use"). Otherwise, the crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

```

Here, we indeed have two threads. One releasing the memory, and the other dereferencing the dangling pointers. It might exist to some tiny time interval on some platforms where this could result in memory corruptions. Otherwise, it would be purely a stability bug.

It seems @fr...@microsoft.com Dale assigned is not responding.
Assigning to mfoltz@ based on content/renderer/media/OWNERS. If there is a better assignee, please feel free to reassign.

### mf...@chromium.org (2024-08-12)

This looks like code to support media foundation rendering which I unfortunately know little about.
From my perspective there are a few options here:

1. Bind a weak pointer to `OverlayStateServiceProviderImpl` to prevent UAF
2. Delete the old subscription and create a new one with the new `OverlayStateServiceProviderImpl`
3. Switch to reference counting this object; but that might keep the old one alive after IsLost
4. Don't handle the IsLost() case and give up

I don't really know this code well enough to say ... maybe someone who did reviews for it could chime in ...

### pe...@google.com (2024-08-27)

mfoltz: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### xh...@chromium.org (2024-08-28)

I suppose this path is only executed when `SupportMediaFoundationClearPlayback()` is true, which is behind a feature flag `kMediaFoundationClearPlayback` that's disabled by default.

AFAIK Edge was experimenting with this feature enabled, and since they contributed the code initially as well, I'll assign to Microsoft owners to take a look.

### mf...@chromium.org (2024-08-29)

Is this still P1/S1 if it is behind a flag?

I also want to point out there is no repro or PoC for this.

### fr...@microsoft.com (2024-08-29)

Changed it to P3/S2.

### ki...@gmail.com (2024-09-11)

Hello, is there any update? Thanks!

### fr...@microsoft.com (2024-09-11)

We are pending on the decision with removal Media Foundation for Clear (MFClear) Frame Server mode or fix the issue with information provided here.
Best Regards.

### pe...@google.com (2024-09-26)

frankli: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fr...@microsoft.com (2024-10-01)

I was on vacation. I will take a look ASAP,
Best Regards,

### ap...@google.com (2024-10-14)

Project: chromium/src  

Branch: main  

Author: Frank Li <[frankli@microsoft.com](mailto:frankli@microsoft.com)>  

Link:      <https://chromium-review.googlesource.com/5910432>

[media] avoid heap-use-after-free in OverlayStateObserverImpl::Create

---


Expand for full commit details
```
[media] avoid heap-use-after-free in OverlayStateObserverImpl::Create

In PS38 of
https://chromium-review.googlesource.com/c/chromium/src/+/3403933/37..38,
`scoped_refptr<OverlayStateServiceProvider>` parameter of
`OverlayStateObserverImpl::Create()' was changed into
`OverlayStateServiceProvider*`. This causes the heap-use-after-free
issue described in https://issuetracker.google.com/issues/354824998.

This CL is to follow existing code pattern of producing `scoped_refptr`
in `RenderThreadImpl::GetStreamTextureFactory()`/
`RenderThreadImpl::GetDCOMPTextureFactor()` instead of returning a raw
pointer in `RenderThreadImpl::GetOverlayStateServiceProvider()`.

Bug: 354824998
Change-Id: Ic188bf18b28a5f024488bd92fb11f6fca6c5d05a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5910432
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Frank Li <frankli@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#1368423}

```

---

Files:

- M `content/renderer/media/media_factory.cc`
- M `content/renderer/media/win/overlay_state_observer_impl.cc`
- M `content/renderer/media/win/overlay_state_observer_impl_unittest.cc`
- M `content/renderer/media/win/overlay_state_service_provider.h`
- M `content/renderer/render_thread_impl.cc`
- M `content/renderer/render_thread_impl.h`

---

Hash: 486a40271e7b2f538e8f2c6140735566bd70426d  

Date:  Mon Oct 14 21:00:53 2024


---

### pg...@google.com (2024-11-11)

Frank, it looks like this bug can be marked as fixed given the change <https://chromium-review.googlesource.com/5910432> from [comment #27](https://issues.chromium.org/issues/354824998#comment27) - is that right?

### fr...@microsoft.com (2024-11-11)

Thanks for the reminder. I have changed the "Status" to "Fixed".

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$1,000 for heavily mitigated memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Congratulations Nan and Zhenghang! Thank you for your efforts and reporting this issue to us.

### ph...@google.com (2025-02-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/354824998)*
