# Security: global-buffer-overflow in SkBitmap IPC Deserialization

| Field | Value |
|-------|-------|
| **Issue ID** | [40089439](https://issues.chromium.org/issues/40089439) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Core, Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2017-10-30 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS
ParamTraits<SkBitmap>::Read in gfx_skia_param_traits.cc handles
deserialization of SkBitmap parameters for old-style IPC messages.
When a compromised renderer sends a message with an oversized
color type, an (arbitrary) out of bounds read occurs.

The problem is here:
```
bool SK_WARN_UNUSED_RESULT tryAllocPixels(const SkImageInfo& info) {
    return this->tryAllocPixels(info, info.minRowBytes());
}
```

The real `this->tryAllocPixels` does validation on the color and alpha
types, but the call `info.minRowBytes()` leads to a call to
`this->bytesPerPixel` which indexes into a global buffer using the
renderer-provided value.

A full patch should fix this at both the Skia layer and the Chromium
layer, but for simplicity the attached patch only adds validation at
the IPC deserialization level in Chromium code.

VERSION
Chrome Version: 62 Stable
Operating System: All

REPRODUCTION CASE
Apply renderer.patch and open Chrome.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Browser
Crash State: See crash.log


## Attachments

- [crash.log](attachments/crash.log) (text/plain, 7.7 KB)
- [fix.patch](attachments/fix.patch) (application/octet-stream, 1.7 KB)
- [renderer.patch](attachments/renderer.patch) (application/octet-stream, 1.7 KB)

## Timeline

### ne...@gmail.com (2017-10-30)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-10-30)

[Empty comment from Monorail migration]

[Monorail components: Internals>Core Internals>Skia]

### hc...@chromium.org (2017-10-30)

[Empty comment from Monorail migration]

### mb...@chromium.org (2017-10-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-11-02)

reed@ -- please help triage and find the right owner for this issue. thanks.

### sh...@chromium.org (2017-11-13)

reed: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@google.com (2017-11-16)

Funny there is a patch, but not a CL.

Having glanced at the patch, I'm not sure if this is the best approach. We seems to be validating the data coming from SkBitmap, but not validating it when it came directly out of deserialization... If this patch fixes things, how did the SkBitmap get passed bad values?

### sh...@chromium.org (2017-11-28)

markdittmer: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2017-11-28)

Does this line not prevent the aforementioned bad indexing?

https://cs.chromium.org/chromium/src/third_party/skia/include/core/SkImageInfo.h?gsn=SkBitmap&l=103

### re...@google.com (2017-11-28)

SkASSERT only fires in debug builds. I think the gfx code that has decided to deserialize a bitmap needs to validate its parameters before creating the skia object.

### ne...@gmail.com (2017-11-28)

re https://crbug.com/chromium/779428#c9: This patch addresses the bug at the IPC deserialization layer, making sure the input data is well-formed before passing it to Skia. Is there another patch you had in mind here? Also I didn't know how to CL before, but I've since made one. I can open a CL if that's easier for you.

### ma...@chromium.org (2017-11-29)

nedwilliamson@gmail.com a CL would be great!

My only feedback on the code as-is would be this: could the unit test be based on serializing then attempting to deserialize an actual SkBitmap instance that is otherwise well formed, but has only the color or alpha perturbed? Two cases (one for each of alpha and color) would also be ideal.

I'm happy to review the CL, but I don't have the OWNERS power to give final approval.

Thanks for catching and suggesting a fix for this!

### ne...@gmail.com (2017-12-05)

CL is up at https://chromium-review.googlesource.com/c/chromium/src/+/809294

Thanks for the suggestions!

### rs...@chromium.org (2018-01-22)

Friendly ping on this. Mark: how does the CL look at this point?

### sh...@chromium.org (2018-01-25)

[Empty comment from Monorail migration]

### ne...@gmail.com (2018-01-25)

Hey guys, it seems Mark hasn't visited in a couple weeks and we're approaching Google's own 90 day deadline for security bugs. Should I reassign to another owner? The CL has been open for a couple months now and it's important that we get this fixed since it crosses the sandbox boundary.

If we can't get this fixed (I'm willing to help over the weekend if necessary) by 90 days I will have to publicly disclose it: https://googleprojectzero.blogspot.com/2015/02/feedback-and-data-driven-updates-to.html

### da...@chromium.org (2018-01-25)

sky could review the paramtraits stuff

### ne...@gmail.com (2018-01-25)

Thanks for reassigning. Sky's suggested fix sounds much better than the existing one. I can try to attempt a fix over the weekend, and I can bump the disclosure 14 days as long as we keep moving forward :)

### da...@chromium.org (2018-01-25)

For the future, you can find a reviewer by looking at OWNERS files in the source tree, by walking up the tree from the modified files.

### pa...@chromium.org (2018-01-26)

This should affect Fuchsia too, right? https://skia.org/dev/flutter

### dc...@chromium.org (2018-01-29)

Fuschia would be affected, yes.

nedwilliamson: are you still planning on updating the CL for this? Otherwise, I'll adopt it. I'd like to get this fixed for M64.

### ne...@gmail.com (2018-01-29)

dcheng: feel free to start from my initial CL or start a new one. I think rewriting the serialization field-by-field is the way to go here, as was noted on the CL. I agree we want to get this fixed and unfortunately I work full time somewhere else. ;)

### dc...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

### dc...@chromium.org (2018-02-02)

https://skia-review.googlesource.com/c/skia/+/99781 appears to have fixed this already, by getting rid of the table and using a switch. So we could merge that patch...

(Normally using memcpy like this is also an info leak. I think we lucked here, in that the struct happens to have no padding)

For now, I'll request that this be merged into M-65. If someone from Skia can help with the merge if it's approved, that'd be appreciated.

### bu...@chromium.org (2018-02-03)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/528018f579c3647a5acd6a27e83c47192ea65baf

commit 528018f579c3647a5acd6a27e83c47192ea65baf
Author: Brian Salomon <bsalomon@google.com>
Date: Sat Feb 03 00:24:40 2018

Add kRGBX_8888, kRGBA_1010102, and kRGBX_1010102 color types. Unused for now.

BUG= skia:7533

Cherry pick to M65
BUG = chromium:779428

No-Tree-Checks: true
No-Try: true
No-Presubmit: true
Change-Id: I4b3f6b827fd833ba2d07895884d2abc9a3132366
Reviewed-On: https://skia-review.googlesource.com/99781
Reviewed-By: Mike Klein <mtklein@chromium.org>
Commit-Queue: Brian Salomon <bsalomon@google.com>
Reviewed-on: https://skia-review.googlesource.com/103200
Reviewed-by: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/528018f579c3647a5acd6a27e83c47192ea65baf/src/image/SkImage_Lazy.cpp
[modify] https://crrev.com/528018f579c3647a5acd6a27e83c47192ea65baf/tools/debugger/SkObjectParser.cpp
[modify] https://crrev.com/528018f579c3647a5acd6a27e83c47192ea65baf/src/core/SkImageInfo.cpp
[modify] https://crrev.com/528018f579c3647a5acd6a27e83c47192ea65baf/src/gpu/gl/GrGLCaps.cpp
[modify] https://crrev.com/528018f579c3647a5acd6a27e83c47192ea65baf/src/gpu/SkGr.cpp
[modify] https://crrev.com/528018f579c3647a5acd6a27e83c47192ea65baf/src/codec/SkWebpCodec.cpp
[modify] https://crrev.com/528018f579c3647a5acd6a27e83c47192ea65baf/gm/bitmapcopy.cpp
[modify] https://crrev.com/528018f579c3647a5acd6a27e83c47192ea65baf/include/core/SkImageInfo.h
[modify] https://crrev.com/528018f579c3647a5acd6a27e83c47192ea65baf/src/gpu/vk/GrVkCaps.cpp


### ne...@gmail.com (2018-02-03)

Awesome! A fix at the Skia layer is much better since it protects future clients.

### go...@chromium.org (2018-02-03)

Cl listed #27 got merged to M65 without approval and it is breaking M65 builds (Pls see https://crbug.com/chromium/808763 for more details). Next time, pls wait for approval. Thank you.

### bu...@chromium.org (2018-02-03)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/73137ff6ba51b3f329d0da9e50a312c4cedee32c

commit 73137ff6ba51b3f329d0da9e50a312c4cedee32c
Author: Brian Salomon <bsalomon@google.com>
Date: Sat Feb 03 16:36:11 2018

Revert "Add kRGBX_8888, kRGBA_1010102, and kRGBX_1010102 color types. Unused for now."

This reverts commit 528018f579c3647a5acd6a27e83c47192ea65baf.

Reason for revert: Breaks branch build w/out corresponding Chrome change.

Original change's description:
> Add kRGBX_8888, kRGBA_1010102, and kRGBX_1010102 color types. Unused for now.
> 
> BUG= skia:7533
> 
> Cherry pick to M65
> BUG = chromium:779428
> 
> No-Tree-Checks: true
> No-Try: true
> No-Presubmit: true
> Change-Id: I4b3f6b827fd833ba2d07895884d2abc9a3132366
> Reviewed-On: https://skia-review.googlesource.com/99781
> Reviewed-By: Mike Klein <mtklein@chromium.org>
> Commit-Queue: Brian Salomon <bsalomon@google.com>
> Reviewed-on: https://skia-review.googlesource.com/103200
> Reviewed-by: Brian Salomon <bsalomon@google.com>

TBR=mtklein@chromium.org,bsalomon@google.com

Change-Id: I3a8fc24ae48519b1da21e54c5e85899e8577f288
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: skia:7533
Reviewed-on: https://skia-review.googlesource.com/103300
Reviewed-by: Brian Salomon <bsalomon@google.com>
Commit-Queue: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/73137ff6ba51b3f329d0da9e50a312c4cedee32c/src/image/SkImage_Lazy.cpp
[modify] https://crrev.com/73137ff6ba51b3f329d0da9e50a312c4cedee32c/tools/debugger/SkObjectParser.cpp
[modify] https://crrev.com/73137ff6ba51b3f329d0da9e50a312c4cedee32c/src/core/SkImageInfo.cpp
[modify] https://crrev.com/73137ff6ba51b3f329d0da9e50a312c4cedee32c/src/gpu/gl/GrGLCaps.cpp
[modify] https://crrev.com/73137ff6ba51b3f329d0da9e50a312c4cedee32c/src/gpu/SkGr.cpp
[modify] https://crrev.com/73137ff6ba51b3f329d0da9e50a312c4cedee32c/src/codec/SkWebpCodec.cpp
[modify] https://crrev.com/73137ff6ba51b3f329d0da9e50a312c4cedee32c/gm/bitmapcopy.cpp
[modify] https://crrev.com/73137ff6ba51b3f329d0da9e50a312c4cedee32c/include/core/SkImageInfo.h
[modify] https://crrev.com/73137ff6ba51b3f329d0da9e50a312c4cedee32c/src/gpu/vk/GrVkCaps.cpp


### go...@chromium.org (2018-02-03)

Removing "merge-merged-m65" label as CL got reverted from M65 at #30.

### sh...@chromium.org (2018-02-03)

Your change meets the bar and is auto-approved for M65. Please go ahead and merge the CL to branch 3325 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-04)

[Comment Deleted]

### bu...@chromium.org (2018-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/247c9292e111304b0bf92a507744bce42356ab68

commit 247c9292e111304b0bf92a507744bce42356ab68
Author: Brian Salomon <bsalomon@google.com>
Date: Mon Feb 05 13:40:51 2018

Prepare mojom for new Skia color types.

Bug: skia:7533
Change-Id: If19339a4a0aaa8ea655184db054058ea2697c6f3
Reviewed-on: https://chromium-review.googlesource.com/887381
Commit-Queue: Brian Salomon <bsalomon@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Florin Malita <fmalita@chromium.org>
Reviewed-by: Mike Klein <mtklein@chromium.org>
Cr-Commit-Position: refs/heads/master@{#532698}
(cherry picked from commit 8ae77702133e0921f9a6491eb3b6c5f1db67c885)

TBR=bsalomon@google.com

Bug: 779428
Change-Id: Iaa32246899f64fb4704fa6c7d17ffb1528667cce
Reviewed-on: https://chromium-review.googlesource.com/901366
Reviewed-by: Brian Salomon <bsalomon@chromium.org>
Cr-Commit-Position: refs/branch-heads/3325@{#296}
Cr-Branched-From: bc084a8b5afa3744a74927344e304c02ae54189f-refs/heads/master@{#530369}
[modify] https://crrev.com/247c9292e111304b0bf92a507744bce42356ab68/skia/public/interfaces/bitmap_skbitmap_struct_traits.cc


### bu...@chromium.org (2018-02-05)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/7f321dad5c6d767f031c41d966f3bbded165b6c4

commit 7f321dad5c6d767f031c41d966f3bbded165b6c4
Author: Brian Salomon <bsalomon@google.com>
Date: Mon Feb 05 14:07:37 2018

Revert "Revert "Add kRGBX_8888, kRGBA_1010102, and kRGBX_1010102 color types. Unused for now.""

This reverts commit 73137ff6ba51b3f329d0da9e50a312c4cedee32c.

No-Tree-Checks: true
No-Try: true
No-Presubmit: true
Bug: chromium:779428
Change-Id: I33ab6e3d5be79f3f97e14c50bfb632ca5126756e
Reviewed-on: https://skia-review.googlesource.com/103441
Reviewed-by: Brian Salomon <bsalomon@google.com>
Commit-Queue: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/7f321dad5c6d767f031c41d966f3bbded165b6c4/src/image/SkImage_Lazy.cpp
[modify] https://crrev.com/7f321dad5c6d767f031c41d966f3bbded165b6c4/tools/debugger/SkObjectParser.cpp
[modify] https://crrev.com/7f321dad5c6d767f031c41d966f3bbded165b6c4/src/core/SkImageInfo.cpp
[modify] https://crrev.com/7f321dad5c6d767f031c41d966f3bbded165b6c4/src/gpu/gl/GrGLCaps.cpp
[modify] https://crrev.com/7f321dad5c6d767f031c41d966f3bbded165b6c4/src/gpu/SkGr.cpp
[modify] https://crrev.com/7f321dad5c6d767f031c41d966f3bbded165b6c4/src/codec/SkWebpCodec.cpp
[modify] https://crrev.com/7f321dad5c6d767f031c41d966f3bbded165b6c4/gm/bitmapcopy.cpp
[modify] https://crrev.com/7f321dad5c6d767f031c41d966f3bbded165b6c4/include/core/SkImageInfo.h
[modify] https://crrev.com/7f321dad5c6d767f031c41d966f3bbded165b6c4/src/gpu/vk/GrVkCaps.cpp


### bu...@chromium.org (2018-02-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9fe6e9f89a1c78b8b38e806d35651a15858b053b

commit 9fe6e9f89a1c78b8b38e806d35651a15858b053b
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Feb 06 01:02:04 2018

Update IPC ParamTraits for SkBitmap to follow best practices.

Using memcpy() to serialize a POD struct is highly discouraged. Just use
the standard IPC param traits macros for doing it.

Bug: 779428
Change-Id: I48f52c1f5c245ba274d595829ed92e8b3cb41334
Reviewed-on: https://chromium-review.googlesource.com/899649
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/master@{#534562}
[modify] https://crrev.com/9fe6e9f89a1c78b8b38e806d35651a15858b053b/ui/gfx/ipc/skia/gfx_skia_param_traits.cc
[modify] https://crrev.com/9fe6e9f89a1c78b8b38e806d35651a15858b053b/ui/gfx/ipc/skia/gfx_skia_param_traits.h
[add] https://crrev.com/9fe6e9f89a1c78b8b38e806d35651a15858b053b/ui/gfx/ipc/skia/gfx_skia_param_traits_macros.h


### aw...@google.com (2018-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-09)

Nice one nedwilliamson@! The VRP panel decided to award $2,000 for this bug, and also wish to thank you for the help on the bug and code review :-)

### aw...@google.com (2018-02-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/779428?no_tracker_redirect=1

[Multiple monorail components: Internals>Core, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089439)*
