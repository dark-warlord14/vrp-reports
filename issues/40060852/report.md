# Security: heap-use-after-free in the Metal features in the GPU process

| Field | Value |
|-------|-------|
| **Issue ID** | [40060852](https://issues.chromium.org/issues/40060852) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Mac |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | cc...@google.com |
| **Created** | 2022-09-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap-use-after-free in the Metal features in the GPU process

**VERSION**  

Chrome Version: 107.0.5287.0 (Developer Build) (arm64)  

Operating System: MacOS Monterey Version 12.5.1  

Revision 66a7dac93d21894a8a58de4c3ac9e7ad6080c514-refs/heads/main@{#1043835}

**REPRODUCTION CASE**

1. get the source code(66a7dac93d21894a8a58de4c3ac9e7ad6080c514-refs/heads/main@{#1043835}) and build the asan version

```
is_asan = true  
is_debug = false  

```

2. run the command:  
   
   ./AsanBuild/Chromium.app/Contents/MacOS/Chromium --user-data-dir=/tmp/any --no-sandbox --enable-features=Metal

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [Gpu browser]  

Asan log:  

See the asan.log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 44.1 KB)
- [1360743-asan.log](attachments/1360743-asan.log) (text/plain, 152.7 KB)

## Timeline

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-09-07)

Repros for me with asan build 107.0.5286.0.

The asan.log attached above doesn't have the asan traces for some reason, so attaching my log.

ccameron: It appears this feature is disabled by default and is not in use by any current finch trials, is that correct?
Tentatively setting impact none since this appears to be non-launched code.
Setting severity high based on UAF in GPU.



[Monorail components: Internals>GPU>Rasterization]

### cc...@chromium.org (2022-09-08)

This is in non-launched code. This is code in the Skia/Metal backend, which is still quite a ways out. (For reference, the ANGLE/Metal backend is something that is shipping soon).

[Monorail components: -Internals>GPU>Rasterization Internals>Skia]

### cc...@chromium.org (2022-09-09)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2022-09-09)

Hi,why this issue is set as WontFix.

### ma...@chromium.org (2022-09-09)

Even if this is non-launched it still looks like a valid bug and we should track that it is fixed before launching.

### cc...@chromium.org (2022-09-12)

->jvanverth for Skia/Metal issues.

### jv...@google.com (2022-09-12)

This may be related to https://skia-review.googlesource.com/c/skia/+/575516.

Looks like the char array in the std::string created for the shader source is wrapped in an NSString and then the original std::string goes out of scope before GrCompileMtlShaderLibrary returns, which doesn't make much sense based on the code flow. The error "malloc: nano zone abandoned due to inability to preallocate reserved vm space." seems related to this: https://stackoverflow.com/questions/64126942/malloc-nano-zone-abandoned-due-to-inability-to-preallocate-reserved-vm-space. I'll dig further when I have a chance, but it looks like to me that ASAN is interfering with malloc and throwing things out of whack.

In addition, it is highly likely that Chrome would not be using this code for Metal, but instead the new Graphite backend. Due to this, and as this is non-launched, dropping the priority.

### jv...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### jv...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-23)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/5e7523fc99f336df984c9f665fc59407d9d943e8

commit 5e7523fc99f336df984c9f665fc59407d9d943e8
Author: Jim Van Verth <jvanverth@google.com>
Date: Fri Sep 23 20:25:33 2022

[metal] Copy shader string into NSString to avoid invalid access.

It appears that when Metal caches shaders, it takes a ref to the
NSString passed in, rather than a copy. This means that when our
std::string goes out of scope they're referring an NSString with
deleted data. Copying it should fix this.

Bug: 1360743
Change-Id: Ia33bfd2ebfa273c3295a0693613eef4b5e5f19f2
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/584456
Reviewed-by: John Stiles <johnstiles@google.com>
Commit-Queue: Jim Van Verth <jvanverth@google.com>

[modify] https://crrev.com/5e7523fc99f336df984c9f665fc59407d9d943e8/src/gpu/ganesh/mtl/GrMtlUtil.mm
[modify] https://crrev.com/5e7523fc99f336df984c9f665fc59407d9d943e8/src/gpu/graphite/mtl/MtlUtils.mm


### jv...@google.com (2022-09-28)

Not sure why it's not showing up here, but this CL has rolled into Chrome (https://chromium-review.googlesource.com/c/chromium/src/+/3916870). Marking fixed.

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-06)

Thank you for this report. The VRP Panel has decided to award you $1,000 for this report as a show of appreciation for this mitigated issue in very new/ work in progress code in head. We generally discourage hunting in head given that that code is likely to change dramatically with trunk churn and testing. Since we did make a security relevant change associated with this report, we did want to extend a thank you reward for that. 

Thank you for your efforts and reporting this issue to us.  

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### jo...@google.com (2022-10-24)

Apple responded and informed me that they do not own `MTLDeviceProxy`, we do. Sure enough, they were right. I found it here: 

https://osscs.corp.google.com/chromium/chromium/src/+/main:components/viz/common/gpu/metal_api_proxy.mm;l=181;drc=48558f8dbe66e6aea5ce16d0f66d739e08dd96aa

ccameron@, do you still own this code? Who can I talk with about getting in a fix? I think there's a subtle retain-versus-copy issue going on here.

### cc...@chromium.org (2022-10-24)

The cache that we have there is due to crbug.com/974219, which I think has been addressed at a different level. At this point I'd suggest deleting MTLDeviceProxy entirely, and re-introducing it if we find that it's needed.

### jo...@google.com (2022-10-24)

It's been addressed by Apple in 10.15+, but it's still a real issue in earlier OSes. Skia has a "workaround" where we drop the draw entirely if shader compilation takes longer than 1 second; we don't make any effort to retry the paint, though:

https://osscs.corp.google.com/skia/skia/+/main:src/gpu/ganesh/mtl/GrMtlUtil.mm;l=175;drc=928dfc8c94ca4b583e8ba3fdde9b014df85d3432

How far back do we want Metal support to go?

### jv...@google.com (2022-10-24)

We've removed our timeout on shader builds in Graphite and haven't noticed any issues with using the non-async library builder directly so far. It's looking likely that we won't need any mitigation at all in the future unless we want to support older OSes.

### cc...@chromium.org (2022-10-24)

My sense is that these Chrome-side mitigations that I added in the distant past have bitrotted to the point that they're more of a liability than anything else. If we want to look into addressing this in 10.14- then I think we're better off doing it with fresh eyes.

### jo...@google.com (2022-10-24)

FYI: another thing we noticed while reviewing this code was that we are defining our own Objective-C classes with a MTL prefix. This is dangerous; if Apple decides to create a `MTLDeviceProxy` or `MTLLibraryCache` class, their classes will clash with ours. We should always avoid using Apple-claimed prefixes. Of course, if we remove the code, this is a non-issue, but if there are other places where we have used MTL in an Objective-C class name, we should fix those as well.

### [Deleted User] (2022-10-26)

[Empty comment from Monorail migration]

### jo...@google.com (2022-10-27)

Chris, should I file a separate bug that Chromium is adding Objective-C classes with the MTL prefix? You suggested that you might just delete this code, but I think there might be other examples of this pattern in the code as well, and it's not safe.

### cc...@chromium.org (2022-10-27)

If there are other examples, then we should file a bug on them (if it's just this, we should file a bug on deleting it ... we should file a bug on deleting it anyway).

### jo...@google.com (2022-10-28)

I didn't realize you wanted separate bugs cut.
PTAL http://go/crb/1379359 for the MTLDeviceProxy improper-retain issue (with a suggested quick fix)

### jo...@google.com (2022-10-28)

PTAL http://go/crb/1379367 for the class-name prefix issue.

### jo...@google.com (2022-10-28)

Closing this bug in lieu of the two new bugs just cut.

### ma...@chromium.org (2022-10-28)

It looks like the problem has not been solved yet so this should not be closed, we need to track the actual state of the security fix.

### jo...@google.com (2022-10-28)

The security fix concern should be covered by http://go/crb/1379359 , this bug feels like a dupe of that bug now to me.

### gi...@appspot.gserviceaccount.com (2022-11-10)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/300b14cf5d5325d9b0e3bf019e14f01385c0e939

commit 300b14cf5d5325d9b0e3bf019e14f01385c0e939
Author: Jim Van Verth <jvanverth@google.com>
Date: Thu Nov 10 15:04:50 2022

Revert "[metal] Copy shader string into NSString to avoid invalid access."

This reverts commit 5e7523fc99f336df984c9f665fc59407d9d943e8.

Reason for revert: Chrome has removed MTLDeviceProxy so this is no
longer needed.

Original change's description:
> [metal] Copy shader string into NSString to avoid invalid access.
>
> It appears that when Metal caches shaders, it takes a ref to the
> NSString passed in, rather than a copy. This means that when our
> std::string goes out of scope they're referring an NSString with
> deleted data. Copying it should fix this.
>
> Bug: 1360743
> Change-Id: Ia33bfd2ebfa273c3295a0693613eef4b5e5f19f2
> Reviewed-on: https://skia-review.googlesource.com/c/skia/+/584456
> Reviewed-by: John Stiles <johnstiles@google.com>
> Commit-Queue: Jim Van Verth <jvanverth@google.com>

Bug: 1360743
Change-Id: Ib2bf75b98a959b8f3ec9252094fe91ac1db4dab5
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/603119
Commit-Queue: Jim Van Verth <jvanverth@google.com>
Reviewed-by: John Stiles <johnstiles@google.com>

[modify] https://crrev.com/300b14cf5d5325d9b0e3bf019e14f01385c0e939/src/gpu/ganesh/mtl/GrMtlUtil.mm
[modify] https://crrev.com/300b14cf5d5325d9b0e3bf019e14f01385c0e939/src/gpu/graphite/mtl/MtlUtils.mm


### am...@chromium.org (2022-11-17)

Closing as fixed based on https://crbug.com/chromium/1360743#c31 and status/ code removal work in https://crbug.com/chromium/1379359

### am...@chromium.org (2022-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-02-25)

This issue was migrated from crbug.com/chromium/1360743?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1366723]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060852)*
