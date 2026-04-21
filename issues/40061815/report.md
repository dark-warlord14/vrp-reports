# Security: Unretained() can be used for objects on the Oilpan heap

| Field | Value |
|-------|-------|
| **Issue ID** | [40061815](https://issues.chromium.org/issues/40061815) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vm...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2022-11-18 |
| **Bounty** | $3,000.00 |

## Description

I found several non-test instances.

https://chromium-review.googlesource.com/c/chromium/src/+/4038606 is the CL.

MemoryCache is created as a global Persistent singleton, so it should be OK: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/memory_cache.h;l=72;drc=199e0841b322540bf17a776cf432efd02ed22861

ResourceLoader::CodeCacheRequest holds own, but ResourceLoader::code_cache_request_ is cleared by a prefinalizer, so it should be safe: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/resource_loader.cc;l=1478;drc=d4ee6330e0d68e0752af9cdd9b6e17b4e8e925fb

WorkerMainScriptLoader also has two instances. I cannot determine if these are safe or not.
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/url_loader/worker_main_script_loader.cc;l=205;drc=bfb8c49dbe07823ef4ebf1a857be9a4d288d1120 creates a mojo::SimpleWatcher. This does not appear to be cleared by prefinalizers, so could theoretically fire when the loader is unreachable but not yet finalized.
Something similar applies to the other usage here: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/loader/fetch/url_loader/worker_main_script_loader.cc;l=105;drc=bfb8c49dbe07823ef4ebf1a857be9a4d288d1120

## Timeline

### dc...@chromium.org (2022-11-18)

I've reached out to the loading/worker teams to try to understand if the last two uses are safe because WorkerMainScriptLoader is always protected via some other means or not. It is not clear to me if worker main script loading can somehow be cancelled and the resulting WorkerMainScriptLoader marked as unreachable.

### dr...@chromium.org (2022-11-19)

dcheng@ - I don't know enough about the context you filed this to add triage labels. Is it safe to assume that these lead to renderer memory corruption in the worst case?

### dc...@chromium.org (2022-11-19)

In the worst case, this could be what is essentially a use-after-free in the renderer.

I am pretty sure the first two uses cannot be use-after-frees. I am not sure about the WorkerMainScriptLoader cases, and I am hoping someone from the worker or loading teams can help clarify the situation.

### dc...@chromium.org (2022-11-21)

nhiroki@, do you know who can help us figure out if the Unretained() usage in WorkerMainScriptLoader can possibly lead to use-after-poison?

### nh...@chromium.org (2022-11-21)

[Empty comment from Monorail migration]

### nh...@chromium.org (2022-11-21)

Hmm, probably https://crbug.com/chromium/1258567 is an instance of this issue. I'll work on this...

### nh...@chromium.org (2022-11-21)

I tried to reproduce crashes using unit tests but failed. Anyway, I think it's safe to explicitly cancel ongoing requests in the prefinalizer.

### nh...@chromium.org (2022-11-21)

cc: hiroshige@ for code review

https://chromium-review.googlesource.com/c/chromium/src/+/4041904

### dc...@chromium.org (2022-11-22)

I also have https://chromium-review.googlesource.com/c/chromium/src/+/4038606 to use WeakPersistent for the callbacks.

### nh...@chromium.org (2022-11-22)

dcheng@: Thanks! Feel free to land it. +1 to using WeakPersistent as default if it's ok in terms of the perf :)

### gi...@appspot.gserviceaccount.com (2022-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bfc0869a5b5f508a4c263fe546f4c42bb174c183

commit bfc0869a5b5f508a4c263fe546f4c42bb174c183
Author: Daniel Cheng <dcheng@chromium.org>
Date: Tue Nov 22 07:49:23 2022

Consistently wrap Oilpan objects with a persistent wrapper in callbacks.

All fixes migrated to use WrapWeakPersistent; while some of these
probably could use a strong persistent, using weak persistent seems like
a safer default to avoid accidentally introducing strong reference
cycles.

Also migrates base::Bind{Once,Repeating} calls to use the WTF version.
since the WTF version is stricter about requiring WTF::Unretained() when
binding raw pointers, also add WTF::Unretained() wrappers as needed.

Bug: 1258806, 1386249
Change-Id: I76c31ddef15187ad04511b143bdb40aa9d05bfe9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4038606
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1074494}

[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_test.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/core/frame/local_frame_back_forward_cache_test.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/platform/loader/fetch/url_loader/worker_main_script_loader.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/platform/loader/fetch/memory_cache.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/modules/mediastream/user_media_client_test.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/platform/loader/fetch/resource_loader.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/core/loader/resource_load_observer_for_frame_test.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/core/frame/root_frame_viewport_test.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/core/layout/svg/svg_hit_test_perftest.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/core/frame/frame_test_helpers.cc
[modify] https://crrev.com/bfc0869a5b5f508a4c263fe546f4c42bb174c183/third_party/blink/renderer/platform/heap/test/incremental_marking_test.cc


### dc...@chromium.org (2022-11-22)

Given the use-after-poison bug linked in https://crbug.com/chromium/1386249#c6, I am going to consider this a memory corruption and triage it as such. This was introduced by https://chromium-review.googlesource.com/c/chromium/src/+/1916682; I am not sure if that CL precisely made this reachable or not, but I think we've being using this loading path for quite some time, so I will consider this as affecting extended stable as well.

(For the VRP panel, I am referring to https://crbug.com/chromium/1258567 which was not reported as a security bug, but appears to directly related)

### dc...@chromium.org (2022-11-22)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-11-22)

CCing vmth4869@gmail.com here who was the original reporter for https://crbug.com/chromium/1258567.

### nh...@chromium.org (2022-11-22)

dcheng@: Thanks for proceeding with the process.

### ad...@google.com (2022-11-22)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-11-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b83b97d8c6e3b9344db91ad818658203d0b4ea2e

commit b83b97d8c6e3b9344db91ad818658203d0b4ea2e
Author: Daniel Cheng <dcheng@chromium.org>
Date: Wed Nov 23 22:28:04 2022

Ban GarbageCollected<T> from being Unretained in Chrome callbacks.

This is not a perfect solution:

- The trait implementation does not force T to be fully-defined. A
  forward-declared type can always be used as Unretained(). This is
  tracked as https://crbug.com/1392872.
- The Blink traits themselves are reliant on the marker types in v8
  always evaluating to void if present. Attempting to use std::void_t<>
  as part of the specialization causes the compiler complain that the
  template specialization is redefined.

Bug: 1386249
Change-Id: I2b0c2282a11ccea1e8925e5014901925088e699d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4049894
Commit-Queue: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1075352}

[modify] https://crrev.com/b83b97d8c6e3b9344db91ad818658203d0b4ea2e/third_party/blink/renderer/platform/BUILD.gn
[modify] https://crrev.com/b83b97d8c6e3b9344db91ad818658203d0b4ea2e/third_party/blink/renderer/platform/heap/DEPS
[add] https://crrev.com/b83b97d8c6e3b9344db91ad818658203d0b4ea2e/third_party/blink/renderer/platform/wtf/functional_test.nc
[modify] https://crrev.com/b83b97d8c6e3b9344db91ad818658203d0b4ea2e/third_party/blink/renderer/platform/heap/garbage_collected.h


### dc...@chromium.org (2022-11-23)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/08fa43f15f0c53b584caf4f403141c5c524ce9a0

commit 08fa43f15f0c53b584caf4f403141c5c524ce9a0
Author: Daniel Cheng <dcheng@chromium.org>
Date: Thu Nov 24 15:19:09 2022

Fix instances of base::Unretained() with incomplete types on Linux.

This CL fixes all existing non-test instances on a non-official Linux
build. The followup CL enforces this for non-test code on non-official
Linux builds.

Bug: 1386249
Change-Id: I92d35b1505e388096e4ab1a64525d83aa8210a05
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4053980
Reviewed-by: danakj <danakj@chromium.org>
Owners-Override: danakj <danakj@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Commit-Queue: danakj <danakj@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1075569}

[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/extensions/browser/extensions_browser_interface_binders.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/chrome/browser/policy/chrome_browser_cloud_management_controller_desktop.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/chrome/browser/ui/views/bookmarks/bookmark_editor_view.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/chrome/browser/net/nss_service.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/services/network/proxy_service_mojo.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/components/autofill/core/browser/form_parsing/credit_card_field.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/chrome/browser/safe_browsing/chrome_client_side_detection_host_delegate.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/chrome/browser/invalidation/profile_invalidation_provider_factory.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/content/browser/network/network_errors_listing_ui.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/content/browser/aggregation_service/aggregation_service_test_utils.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/media/filters/offloading_video_decoder.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/content/gpu/gpu_service_factory.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/content/browser/browser_interface_binders.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/chrome/browser/ui/views/toolbar/chrome_labs_view_controller.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/components/enterprise/browser/controller/chrome_browser_cloud_management_controller.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/chrome/browser/platform_util_linux.cc
[modify] https://crrev.com/08fa43f15f0c53b584caf4f403141c5c524ce9a0/content/browser/media/capture/web_contents_video_capture_device.cc


### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### ad...@google.com (2023-01-31)

VRP panel: this bug is in a bit of an odd state but, based on the comments on https://crbug.com/chromium/1258567, it probably should have been marked type=Bug-Security.

### [Deleted User] (2023-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-31)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-09)

Congratulations! The VRP Panel has decided to award you $3,000 for your report of https://crbug.com/chromium/1258567, a mildly mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-02)

This issue was migrated from crbug.com/chromium/1386249?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1258567]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061815)*
