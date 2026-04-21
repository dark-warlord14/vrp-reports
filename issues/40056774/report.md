# AddressSanitizer: heap-buffer-overflow mojo::internal::Serializer<BigBufferDataView,BigBufferView>::Serialize

| Field | Value |
|-------|-------|
| **Issue ID** | [40056774](https://issues.chromium.org/issues/40056774) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>ShapeDetection, Internals>Core, Internals>Mojo>Bindings |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2021-08-04 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4582.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
Windows NT 10.0; Win64; x64
gs://chromium-browser-asan/win32-release_x64/asan-win32-release_x64-906640.zip

#Reproduce
1. chrome.exe --no-sandbox --js-flags='--expose_gc' --enable-blink-test-features --user-data-dir=0727 mini_poc.html

What is the expected behavior?

What went wrong?

Type of crash
render tab

#Analysis
1. AT[1] If condition is true, the memory allocation logic will be skipped
2. The code "var v0299 = new OffscreenCanvas(0x80CB, 0x8F9B);" will make condition satisfied(0x80CB*0x8F9B>kMaxNumElements)
3. In the debug version this DCHECK[2] will be triggered(FATAL:message_fragment.h(140)] Check failed: !is_null(). )

```

mojo/public/cpp/bindings/lib/message_fragment.h:148

Array_Data<T>* data() {
DCHECK(!is_null());	[2]
return message_.payload_buffer()->template Get<Array_Data<T>>(index_);
}

// Allocates and claims enough memory for `num_elements` elements of type `T`,
// plus an array header, and initializes a new `Array_Data<T>` in place.
void AllocateArrayData(size_t num_elements) {
static_assert(
	std::numeric_limits<uint32_t>::max() > Traits::kMaxNumElements,
	"Max num elements castable to 32bit");
if (num_elements > Traits::kMaxNumElements)		<<[1]
  return;

const uint32_t num_bytes =
	Traits::GetStorageSize(static_cast<uint32_t>(num_elements));
index_ = message_.payload_buffer()->Allocate(num_bytes);
new (data()) Array_Data<T>(num_bytes, static_cast<uint32_t>(num_elements));
}
```

#Patch
diff --git a/mojo/public/cpp/bindings/lib/message_fragment.h b/mojo/public/cpp/bindings/lib/message_fragment.h
index e466d62250e..9583e53307b 100644
--- a/mojo/public/cpp/bindings/lib/message_fragment.h
+++ b/mojo/public/cpp/bindings/lib/message_fragment.h
@@ -149,8 +149,8 @@ class MessageFragment<Array_Data<T>> {
     static_assert(
         std::numeric_limits<uint32_t>::max() > Traits::kMaxNumElements,
         "Max num elements castable to 32bit");
-    if (num_elements > Traits::kMaxNumElements)
-      return;
+    
+    CHECK_LE(num_elements,Traits::kMaxNumElements);

     const uint32_t num_bytes =
         Traits::GetStorageSize(static_cast<uint32_t>(num_elements));

#asan

==9332==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x126f603e3ad8 at pc 0x7ff602ba5b37 bp 0x00e9807fc700 sp 0x00e9807fc748
WRITE of size 4848451492 at 0x126f603e3ad8 thread T0
==9332==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff602ba5b36 in __asan_memcpy C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:22
    #1 0x7ffa46a6ecc4 in mojo::internal::Serializer<mojo::ArrayDataView<unsigned char>,base::span<const unsigned char,18446744073709551615> >::Serialize C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\array_serialization.h:475
    #2 0x7ffa46ae9cc5 in mojo::internal::Serializer<mojo_base::mojom::BigBufferDataView,mojo_base::BigBufferView>::Serialize C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\mojo\public\mojom\base\big_buffer.mojom-shared.h:231
    #3 0x7ffa4790c596 in mojo::internal::Serializer<skia::mojom::BitmapN32DataView,const SkBitmap>::Serialize C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\skia\public\mojom\bitmap.mojom-shared.h:284
    #4 0x7ffa4e42aa61 in shape_detection::mojom::blink::FaceDetectionProxy::Detect C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\services\shape_detection\public\mojom\facedetection.mojom-blink.cc:217
    #5 0x7ffa60b216a3 in blink::FaceDetector::DoDetect C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\shapedetection\face_detector.cc:64
    #6 0x7ffa60aaa634 in blink::ShapeDetector::detect C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\shapedetection\shape_detector.cc:115
    #7 0x7ffa5ff2c2ac in blink::`anonymous namespace'::v8_face_detector::DetectOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_face_detector.cc:183
    #8 0x7ffa4b5bf01a in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:155
    #9 0x7ffa4b5bc0dd in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #10 0x7ffa4b5b9513 in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
    #11 0x7ffa4b5b883e in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #12 0x7e92000be07b  (<unknown module>)

0x126f603e3ad8 is located 0 bytes to the right of 280-byte region [0x126f603e39c0,0x126f603e3ad8)
allocated by thread T0 here:
    #0 0x7ff602ba60ab in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffa4856b4f4 in mojo::core::`anonymous namespace'::ComplexMessage::ComplexMessage C:\b\s\w\ir\cache\builder\src\mojo\core\channel.cc:471
    #2 0x7ffa4856d124 in mojo::core::Channel::Message::ExtendPayload C:\b\s\w\ir\cache\builder\src\mojo\core\channel.cc:371
    #3 0x7ffa485d7c39 in mojo::core::UserMessageImpl::AppendData C:\b\s\w\ir\cache\builder\src\mojo\core\user_message_impl.cc:514
    #4 0x7ffa48577ee9 in mojo::core::Core::AppendMessageData C:\b\s\w\ir\cache\builder\src\mojo\core\core.cc:391
    #5 0x7ffa485928d7 in MojoAppendMessageDataImpl C:\b\s\w\ir\cache\builder\src\mojo\core\entrypoints.cc:93
    #6 0x7ffa4f9d3071 in mojo::internal::Buffer::Allocate C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\buffer.cc:69
    #7 0x7ffa4790cf0e in mojo::internal::Serializer<skia::mojom::BitmapN32ImageInfoDataView,const SkImageInfo>::Serialize C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\skia\public\mojom\image_info.mojom-shared.h:421
    #8 0x7ffa4790c40d in mojo::internal::Serializer<skia::mojom::BitmapN32DataView,const SkBitmap>::Serialize C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\skia\public\mojom\bitmap.mojom-shared.h:272
    #9 0x7ffa4e42aa61 in shape_detection::mojom::blink::FaceDetectionProxy::Detect C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\services\shape_detection\public\mojom\facedetection.mojom-blink.cc:217
    #10 0x7ffa60b216a3 in blink::FaceDetector::DoDetect C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\shapedetection\face_detector.cc:64
    #11 0x7ffa60aaa634 in blink::ShapeDetector::detect C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\shapedetection\shape_detector.cc:115
    #12 0x7ffa5ff2c2ac in blink::`anonymous namespace'::v8_face_detector::DetectOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_face_detector.cc:183
    #13 0x7ffa4b5bf01a in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:155
    #14 0x7ffa4b5bc0dd in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112
    #15 0x7ffa4b5b9513 in v8::internal::Builtin_Impl_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142
    #16 0x7ffa4b5b883e in v8::internal::Builtin_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130
    #17 0x7e92000be07b  (<unknown module>)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:22 in __asan_memcpy
Shadow bytes around the buggy address:
  0x04994c3fc700: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x04994c3fc710: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x04994c3fc720: 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fa
  0x04994c3fc730: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x04994c3fc740: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x04994c3fc750: 00 00 00 00 00 00 00 00 00 00 00[fa]fa fa fa fa
  0x04994c3fc760: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x04994c3fc770: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04994c3fc780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x04994c3fc790: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x04994c3fc7a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==9332==ABORTING

Did this work before? N/A 

Chrome version: 94.0.4582.0  Channel: n/a
OS Version: 10.0

## Attachments

- [mini_poc.html](attachments/mini_poc.html) (text/plain, 1.0 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 684 B)
- [asan.txt](attachments/asan.txt) (text/plain, 6.6 KB)

## Timeline

### [Deleted User] (2021-08-04)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-08-04)

Thanks for the report.

rockot@: PTAL?

The reporter is suggesting a hard CHECK in MessageFragment::AllocateArrayData(), rather than returning nullptr for a too-large allocation request.

[Monorail components: Internals>Mojo>Bindings]

### [Deleted User] (2021-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2021-08-06)

https://crbug.com/chromium/1236318#c2 The better approach is to prevent the crash, but it seems that a lot of code needs to be modified.

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-18)

rockot: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-01)

rockot: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-09-02)

[Security marshall] I don't know if this is a mojo issue. Isn't this an issue where the offscreen canvas is asking for something that's too big and failing the preconditions the mojo type has?

+reillyg as the stacktrace goes through face detection.

[Monorail components: -Internals>Mojo>Bindings Blink>ShapeDetection]

### ke...@chromium.org (2021-09-02)

That is a problem yes but separate from the issue that asking mojo to serialize a large array will cause a buffer overflow. Possibly this could be split into two bugs, but I'd consider the mojo problem to be the more important for a proper security fix.

[Monorail components: Internals>Mojo>Bindings]

### re...@chromium.org (2021-09-02)

Adding rockot@ back to this issue. It really seems like a Mojo bug.

### re...@chromium.org (2021-09-02)

Adding the recommended CHECK in https://chromium-review.googlesource.com/c/chromium/src/+/3139712.

It would be nice to fix the surrounding code but the way we get into this situation is when BigBuffer has already failed to allocate a shared memory region and so it falling back to trying to pass the data directly in the Mojo message. The CHECK is important for defense-in-depth for this kind of situation as the only other solution is to implement an arbitrary limit on the size of an image source which can be passed to methods like detect() as there's no back-pressure signal Mojo can provide for serialization failures.

rockot@, what do you think about closing the Mojo pipe on the sending side when there is a serialization failure?

### ro...@google.com (2021-09-02)

That's a pretty big change, but it sounds reasonable in theory. To be clear you would actually want to not just close the pipe, but also swap it out for a new disconnected pipe: you don't want to silently pull the Remote out from under someone such that operator-> starts crashing.

The biggest risk here would be significant code size increase from making serialization able to fail gracefully due to potentially many new branches in generated/template code.

### re...@chromium.org (2021-09-02)

Agreed, it should swap out the pipe for a new disconnected one and fire the disconnection handler. Basically the same behavior as you get on deserialization failure.

### gi...@appspot.gserviceaccount.com (2021-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/588cb74f661269a5b2b69f52619c0f7a09867d6f

commit 588cb74f661269a5b2b69f52619c0f7a09867d6f
Author: Reilly Grant <reillyg@chromium.org>
Date: Fri Sep 03 00:49:59 2021

mojo: CHECK when array has too many elements to serialize

This change turns an early return into a CHECK because the surrounding
code expects memory allocation to succeed.

Bug: 1236318
Change-Id: Ib11e0564fb0fa653cb50c82e1973c76ec0c9c725
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3139712
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/heads/main@{#917908}

[modify] https://crrev.com/588cb74f661269a5b2b69f52619c0f7a09867d6f/mojo/public/cpp/bindings/lib/message_fragment.h


### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### re...@chromium.org (2021-09-24)

[Empty comment from Monorail migration]

### re...@chromium.org (2021-09-24)

This is "Fixed" but we're still going to hit the CHECK as is seen in https://crbug.com/chromium/1250769. The right solution is surfacing the serialization failure in a way which can be safely caught and turned into a Javascript error rather than crashing the renderer. Ken, do you think that's something you want to track on a separate bug?

### cl...@chromium.org (2021-09-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-03)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2021-10-04)

I've filed https://crbug.com/chromium/1255667 for the follow up work so this security bug can be closed. The security fix landed over a month ago and we missed the chance to merge to m94 stable.

### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-04)

Requesting merge to stable M94 because latest trunk commit (917908) appears to be after stable branch point (911515).

Not requesting merge to beta (M95) because latest trunk commit (917908) appears to be prior to beta branch point (920003). If this is incorrect, please replace the Merge-NA-95 label with Merge-Request-95. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-04)

Merge review required: M94 is already shipping to stable.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2021-10-04)

I've created a draft merge[1] and it appears to apply cleanly. I'll defer to Ken on whether he considers this to be a safe change to make late in the stable release cycle.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/3202713 

### am...@google.com (2021-10-04)

Merge approved to M94, please merge to branch 4606 by EOD tomorrow, 5 October, so this fix can be included in the next Stable channel refresh on Thursday. 

### gi...@appspot.gserviceaccount.com (2021-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b2c4e4dc21e509207bfa4cfc6a32bd24fa3423d9

commit b2c4e4dc21e509207bfa4cfc6a32bd24fa3423d9
Author: Reilly Grant <reillyg@chromium.org>
Date: Mon Oct 04 23:02:19 2021

[Merge M-94] mojo: CHECK when array has too many elements to serialize

This change turns an early return into a CHECK because the surrounding
code expects memory allocation to succeed.

(cherry picked from commit 588cb74f661269a5b2b69f52619c0f7a09867d6f)

Bug: 1236318
Change-Id: Ib11e0564fb0fa653cb50c82e1973c76ec0c9c725
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3139712
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Ken Rockot <rockot@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#917908}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3203131
Cr-Commit-Position: refs/branch-heads/4606@{#1301}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/b2c4e4dc21e509207bfa4cfc6a32bd24fa3423d9/mojo/public/cpp/bindings/lib/message_fragment.h


### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations, the VRP Panel has decided to award you $7500 for this report. Thank you for this report and nice work! 

### am...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-10-11)

ClusterFuzz testcase 5639033806716928 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### re...@chromium.org (2021-10-11)

kenrb@, is there a way to tell Clusterfuzz that this crash is expected or get it to start tracking https://crbug.com/chromium/1255667 instead?

### rz...@google.com (2021-10-12)

[Empty comment from Monorail migration]

### ke...@chromium.org (2021-10-12)

Re https://crbug.com/chromium/1236318#c36: There doesn't seem to be a way to change the bug that a CF report is associated with. Probably best just to flag ClusterFuzz-Ignore to prevent any further nags.

### gi...@google.com (2021-10-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7f0f370265cbf03329c7a2e22a12be0b3157047c

commit 7f0f370265cbf03329c7a2e22a12be0b3157047c
Author: Reilly Grant <reillyg@chromium.org>
Date: Tue Oct 19 08:35:51 2021

[M90-LTS] mojo: CHECK when array has too many elements to serialize

This change turns an early return into a CHECK because the surrounding
code expects memory allocation to succeed.

(cherry picked from commit 588cb74f661269a5b2b69f52619c0f7a09867d6f)

Bug: 1236318
Change-Id: Ib11e0564fb0fa653cb50c82e1973c76ec0c9c725
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3139712
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Auto-Submit: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917908}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3217108
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1641}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/7f0f370265cbf03329c7a2e22a12be0b3157047c/mojo/public/cpp/bindings/lib/message_fragment.h


### rz...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### re...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-10-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1236318?no_tracker_redirect=1

[Multiple monorail components: Blink>ShapeDetection, Internals>Core, Internals>Mojo>Bindings]
[Monorail mergedwith: crbug.com/chromium/1250769, crbug.com/chromium/1261624]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056774)*
