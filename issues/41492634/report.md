# UAF in gpu::GpuChannelHost

| Field | Value |
|-------|-------|
| **Issue ID** | [41492634](https://issues.chromium.org/issues/41492634) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>GPU |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2024-01-18 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

tested chrome version:  

Chromium 122.0.6238.2  

Chromium 122.0.6257.0

repro steps:  

1 git apply sleep.patch  

2 build chrome with asan:  

args.gn is as follows:  

is\_asan = true  

is\_debug = false  

enable\_nacl = false  

treat\_warnings\_as\_errors = false  

is\_component\_build=false  

dcheck\_always\_on = false  

3 run chrome with the following command:

./chrome --enable-features=SharedBitmapToSharedImage --disable-gpu --user-data-dir=/tmp/xx <http://localhost:8000/crash.html>

note:

- Latest beta version does not require SharedBitmapToSharedImage
- The patch code is only for the convenience of reproduction and should not have an impact on the vulnerability itself.

**Problem Description:**  

bisect:  

<https://chromium-review.googlesource.com/c/chromium/src/+/5092990>

==225252==ERROR: AddressSanitizer: heap-use-after-free on address 0x51b000029ef8 at pc 0x562b79484c2d bp 0x7f6686190570 sp 0x7f6686190568  

READ of size 1 at 0x51b000029ef8 thread T10 (ThreadPoolForeg)  

#0 0x562b79484c2c in has\_value ./../../third\_party/libc++/src/include/optional:359:82  

#1 0x562b79484c2c in operator bool ./../../third\_party/libc++/src/include/optional:820:84  

#2 0x562b79484c2c in gpu::GpuChannelHost::EnqueuePendingOrderingBarrier() ./../../gpu/ipc/client/gpu\_channel\_host.cc:128:8  

#3 0x562b794858b7 in InternalFlush ./../../gpu/ipc/client/gpu\_channel\_host.cc:151:3  

#4 0x562b794858b7 in gpu::GpuChannelHost::VerifyFlush(unsigned int) ./../../gpu/ipc/client/gpu\_channel\_host.cc:117:3  

#5 0x562b7949932c in gpu::SharedImageInterfaceProxy::GenVerifiedSyncToken() ./../../gpu/ipc/client/shared\_image\_interface\_proxy.cc:419:10  

#6 0x562b79467e0f in gpu::ClientSharedImageInterface::GenVerifiedSyncToken() ./../../gpu/ipc/client/client\_shared\_image\_interface.cc:71:18  

#7 0x562b8e679e61 in cc::(anonymous namespace)::BitmapRasterBufferImpl::Playback(cc::RasterSource const\*, gfx::Rect const&, gfx::Rect const&, unsigned long, gfx::AxisTransform2d const&, cc::RasterSource::PlaybackSettings const&, GURL const&) ./../../cc/raster/bitmap\_raster\_buffer\_provider.cc:107:35  

#8 0x562b8e3daea0 in cc::(anonymous namespace)::RasterTaskImpl::RunOnWorkerThread() ./../../cc/tiles/tile\_manager.cc:146:21  

#9 0x562b9a1d7e83 in cc::CategorizedWorkerPoolJob::Run(base::span<cc::TaskCategory const, 18446744073709551615ul, cc::TaskCategory const\*>, base::JobDelegate\*) ./../../cc/raster/categorized\_worker\_pool.cc:550:29  

#10 0x562b9a1e172c in Invoke<void (cc::CategorizedWorkerPoolJob::\*)(base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory \*>, base::JobDelegate \*), cc::CategorizedWorkerPoolJob \*, const base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory \*> &, base::JobDelegate \*> ./../../base/functional/bind\_internal.h:710:12  

#11 0x562b9a1e172c in MakeItSo<void (cc::CategorizedWorkerPoolJob::\*const &)(base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory \*>, base::JobDelegate \*), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<cc::CategorizedWorkerPoolJob, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory \*> > &, base::JobDelegate \*> ./../../base/functional/bind\_internal.h:860:12  

#12 0x562b9a1e172c in RunImpl<void (cc::CategorizedWorkerPoolJob::\*const &)(base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory \*>, base::JobDelegate \*), const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<cc::CategorizedWorkerPoolJob, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::span<const cc::TaskCategory, 18446744073709551615UL, const cc::TaskCategory \*> > &, 0UL, 1UL> ./../../base/functional/bind\_internal.h:991:14  

#13 0x562b9a1e172c in base::internal::Invoker<base::internal::BindState<void (cc::CategorizedWorkerPoolJob::\*)(base::span<cc::TaskCategory const, 18446744073709551615ul, cc::TaskCategory const\*>, base::JobDelegate\*), base::internal::UnretainedWrapper<cc::CategorizedWorkerPoolJob, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0>, base::span<cc::TaskCategory const, 18446744073709551615ul, cc::TaskCategory const\*>>, void (base::JobDelegate\*)>::Run(base::internal::BindStateBase\*, base::JobDelegate\*) ./../../base/functional/bind\_internal.h:911:12  

#14 0x562b88d8c845 in base::RepeatingCallback<void (base::JobDelegate\*)>::Run(base::JobDelegate\*) const & ./../../base/functional/callback.h:344:12  

#15 0x562b88d90c84 in operator() ./../../base/task/thread\_pool/job\_task\_source\_old.cc:104:32  

#16 0x562b88d90c84 in Invoke<const (lambda at ../../base/task/thread\_pool/job\_task\_source\_old.cc:100:11) &, base::internal::JobTaskSourceOld \*> ./../../base/functional/bind\_internal.h:626:12  

#17 0x562b88d90c84 in MakeItSo<const (lambda at ../../base/task/thread\_pool/job\_task\_source\_old.cc:100:11) &, const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<base::internal::JobTaskSourceOld, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> > &> ./../../base/functional/bind\_internal.h:860:12  

#18 0x562b88d90c84 in RunImpl<const (lambda at ../../base/task/thread\_pool/job\_task\_source\_old.cc:100:11) &, const std::\_\_Cr::tuple<base::internal::UnretainedWrapper<base::internal::JobTaskSourceOld, base::unretained\_traits::MayNotDangle, (partition\_alloc::internal::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind\_internal.h:991:14  

#19 0x562b88d90c84 in base::internal::Invoker<base::internal::BindState<base::internal::JobTaskSourceOld::JobTaskSourceOld(base::Location const&, base::Task

**Additional Comments:**

\*\*Chrome version: \*\* 122.0.6257.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 236 B)
- [sleep.patch](attachments/sleep.patch) (text/plain, 1.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 33.2 KB)
- [asan-new.log](attachments/asan-new.log) (text/plain, 34.4 KB)
- [asan-old.log](attachments/asan-old.log) (text/plain, 22.7 KB)
- [asan-1519655.txt](attachments/asan-1519655.txt) (text/plain, 25.9 KB)

## Timeline

### [Deleted User] (2024-01-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4856798755880960.

### za...@google.com (2024-01-18)

ccameron@ Can you please take a look at this gpu related bug? Thanks !

[Monorail components: Internals>GPU]

### [Deleted User] (2024-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2024-01-20)

Sorry, after multiple tests, it has been found that the free stack in the ASan log can sometimes differ, and the GpuChannelHost is not always released through cc::LayerTreeFrameSink::OnGpuChannelLost before the UAF occurs. Moreover, it can be reproduced in older versions as well, hence the above bisect result is not accurate. These tests were conducted without applying any patches. 
In the new version, reproduction is very difficult. it was reproduced more than 10 times overnight (MiraclePtr Status: NOT PROTECTED). In the old version, it is easy to reproduce(MiraclePtr Status: PROTECTED).

### ha...@google.com (2024-01-20)

[Empty comment from Monorail migration]

### em...@gmail.com (2024-01-24)

I forgot to mention the chromium version I was testing on.
latest version:Chromium 123.0.6262.0
old version: Chromium 119.0.6041.0 

### [Deleted User] (2024-01-24)

[Empty comment from Monorail migration]

### th...@chromium.org (2024-01-30)

[secondary shepherd] Hi emilykim8708@, just for clarification:

1. Are you saying that the bug is reproducible on current Stable (M120)? If so, is the appropriate run command to do so still `./chrome --enable-features=SharedBitmapToSharedImage --disable-gpu --user-data-dir=/tmp/xx http://localhost:8000/crash.html`? Meaning it requires the feature SharedBitmapToSharedImage to be enabled.
2. For your note "Latest beta version does not require SharedBitmapToSharedImage" -- which milestone versions is this referring to?

(Looping in magchen@ into cc as well from the bisect CL, though https://crbug.com/chromium/1519655#c7 notes that the bisect result is not accurate.)

### ma...@chromium.org (2024-01-30)

The implementation for SharedBitmapToSharedImage is not completed in M120. Please do not enable it when the feature is not ready. That's why it's disabled by default because it's under development.

SharedBitmapToSharedImage is enabled by default in M123. Could you re-run your test with the latest version. If you still see an issue, please open a new bug with the info on the latest version.

Since this bug is open for M122, I am going to merge it into an old bug.

### ma...@chromium.org (2024-01-31)

More info on SharedBitmapToSharedImage. It's disabled in M122 and all previous versions. For M120 and M121, some specific codes are even removed so they cannot be enabled by the flag, because people tried to enable it and run (asan) test on it when the feature is still under development.
SharedBitmapToSharedImage is enabled in M123.

### th...@chromium.org (2024-01-31)

Thank you magchen@ for the comment and for identifying this is a duplicate! emilykim8708@, please do file a new issue if you are able to reproduce on the latest Chrome version.

One note: security bugs in unlaunched features (in code behind a flag not enabled by default) are still eligible for the Chrome Vulnerability Reward Program[1], so filing security bugs for unlaunched features is not discouraged.

[1]: https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules

### em...@gmail.com (2024-01-31)

I previously mentioned（#https://crbug.com/chromium/1519655#c9） that this issue could be reproduced in version 123.0.6262.0, and I have just tested it in the updated version（Chromium 123.0.6273.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1254377.zip)）, where the issue still persists.
In my fuzzer, running for several minutes usually reproduces the issue once. To reproduce it quickly, applying the sleep.patch is necessary.
Do I need to create a new issue report?

### th...@chromium.org (2024-01-31)

Thank you for the speedy response. No you do not need to create a new issue.

I'm able to reproduce this on gLinux with the patch on head. I do not need any flags on the machine I'm reproducing on (neither of these: --enable-features=SharedBitmapToSharedImage --disable-gpu), so not setting the label Security_Impact-None. It is a UAF in the browser process, the MiraclePtr Status is NOT PROTECTED, and there are no user interactions needed, so I'm raising the severity to Critical. For now, I'm setting the FoundIn to M123 to match the lack of Security_Impact-None label, since that is where the flag has been enabled by default. Note: I'm actually seeing a slightly different stack trace using the provided POC and am attaching it.

FWIW -- without the patch, I have not been able to reproduce it. I let it run for a bit over an hour.

magchen@: could you PTAL?

### [Deleted User] (2024-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-31)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2024-01-31)

Hi.
Before I saw your reply, I had already submited a new issue. There are info to quickly repro without using patches, and you can merge the issues together or close 1523688(https://bugs.chromium.org/p/chromium/issues/detail?id=1523688).
Thanks.

### th...@chromium.org (2024-01-31)

Thank you for the heads up on that. I'll close it as a duplicate and will give the the owner + cc access to that closed bug for reference.

### th...@chromium.org (2024-01-31)

[Empty comment from Monorail migration]

### ma...@chromium.org (2024-01-31)

I am taking a look.

### ma...@chromium.org (2024-01-31)

By the way, this is only part of the whole ShareBitmapToShareImage conversion and the feature is still in progress. I will just disable the feature for now and reenable it later when the more conversion is done and we can run tests thoroughly on the whole feature. (I am going OOO for weeks.)

### ma...@chromium.org (2024-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3662d42594a1def49e6fab1c8e58f51a1b71bfe9

commit 3662d42594a1def49e6fab1c8e58f51a1b71bfe9
Author: Maggie Chen <magchen@chromium.org>
Date: Wed Jan 31 19:04:51 2024

Temporarily disable kSharedBitmapToSharedImage

Bug: 1434885
Change-Id: I7da3e99d26830e232a91732247e7ce688e66a7c0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5252845
Commit-Queue: Maggie Chen <magchen@chromium.org>
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1254654}

[modify] https://crrev.com/3662d42594a1def49e6fab1c8e58f51a1b71bfe9/components/viz/common/features.cc


### ma...@chromium.org (2024-01-31)

Hi thefrog@, I have already disabled the feature. I am not sure if you can reproduce the crash without the patch. But for the test with the patch, you can verify it with the latest code. Thanks.

### th...@chromium.org (2024-01-31)

Great, thanks for the quick action on this. I can no longer reproduce this without setting the renamed extra flag. I'm adding the Security_Impact-None label now to reflect that. I'm marking this as a blocking bug for crbug.com/1434885 for tracking purposes.

I'm also setting the FoundIn to 122, since I was able to reproduce on there with the patch and the extra flags. I was not able to reproduce on 121, presumably because of the extra codes described in https://crbug.com/chromium/1519655#c13 preventing the feature from running on 121 and 120. I did not try reproducing on 120 after that.

magchen@: Can you confirm that this feature has not been toggled on with a field trial configuration?

### ma...@chromium.org (2024-01-31)

No, it's not in the field trial configuration. No finch experiment either.

### th...@chromium.org (2024-01-31)

Great. Then the Security_Impact-None label makes sense. For now, we should leave this ticket open until the root cause is resolved, and then this ticket can be marked as Fixed.

### ma...@chromium.org (2024-01-31)

Should we lower the priority?

### th...@chromium.org (2024-01-31)

[Empty comment from Monorail migration]

### th...@chromium.org (2024-01-31)

Yes we should.

### am...@chromium.org (2024-01-31)

as SI-None this is also not a release blocker, so I'm removing the RBS label 

### be...@google.com (2024-02-01)

Adding Hotlist-RBS-Removed for tracking purposes.

### ma...@chromium.org (2024-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fcb0e4fbfdd8afbc2a0ce07c90de1e9d6b292110

commit fcb0e4fbfdd8afbc2a0ce07c90de1e9d6b292110
Author: Maggie Chen <magchen@chromium.org>
Date: Thu Feb 01 16:41:57 2024

Use scoped_refptr for shared_image_interface() in LayerTreeFrameSink

Now that ClientSharedImageInterface is ref counted, switch to
scoped_refptr for shared_image_interface().

Bug: 1434885
Change-Id: Ic4eebc905f3cc6179721434a37c20614b7665354
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5255057
Commit-Queue: Maggie Chen <magchen@chromium.org>
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1255080}

[modify] https://crrev.com/fcb0e4fbfdd8afbc2a0ce07c90de1e9d6b292110/cc/layers/heads_up_display_layer_impl.cc
[modify] https://crrev.com/fcb0e4fbfdd8afbc2a0ce07c90de1e9d6b292110/cc/trees/layer_tree_frame_sink.cc
[modify] https://crrev.com/fcb0e4fbfdd8afbc2a0ce07c90de1e9d6b292110/cc/trees/layer_tree_host_impl.cc
[modify] https://crrev.com/fcb0e4fbfdd8afbc2a0ce07c90de1e9d6b292110/cc/trees/layer_tree_frame_sink.h
[modify] https://crrev.com/fcb0e4fbfdd8afbc2a0ce07c90de1e9d6b292110/cc/raster/bitmap_raster_buffer_provider.cc

### ma...@chromium.org (2024-02-02)

Hi emilykim8708@, are you able to verify if CL5255057 fixes the problem? Thanks.

### em...@gmail.com (2024-02-02)

Thank you for the quick fix. After applying the patch, the UAF was not reproduced again.

### wf...@chromium.org (2024-02-02)

[secondary shepherd} ty for your CL magchen@chromium.org, can this bug be marked fixed now?

### ma...@chromium.org (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1519655?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1434885]
[Monorail mergedwith: crbug.com/chromium/1523688]
[Monorail mergedinto: crbug.com/chromium/1453577]
[Monorail components added to Component Tags custom field.]

### th...@chromium.org (2024-02-05)

Unmarking as duplicate so that the status says Fixed instead of "Duplicate of 40065570". (The issue was closed as a duplicate and then I reopened it in #17, but perhaps I also needed to unlink it from the duplicate bug which I did not do.)

### th...@chromium.org (2024-02-05)

Also changing owner back to magchen@ since that doesn't seem to have carried over into the migrated bug. (Note: I've filed internal bugs about both of these quirks.)

### am...@google.com (2024-02-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-08)

Congratulations Cassidy Kim! The Chrome VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### pe...@google.com (2024-05-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41492634)*
