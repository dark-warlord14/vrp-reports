# Insufficient fix for Cross-Origin (Partial) Status Code leak (XS-Leak)

| Field | Value |
|-------|-------|
| **Issue ID** | [40062152](https://issues.chromium.org/issues/40062152) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>CORS |
| **Platforms** | Mac |
| **Reporter** | ku...@googlemail.com |
| **Assignee** | nr...@chromium.org |
| **Created** | 2022-12-09 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

1. start php server to run h.php `php -S 127.0.0.1 8000`
2. open poc.html
3. Press Check1 with the provided testcases:  
   
   [http://127.0.0.1:8000/h.php?h[X-Frame-Options]=DENY&h[Content-Security-Policy]=frame-ancestors%20%27none%27&statuscode=200](http://127.0.0.1:8000/h.php?h%5BX-Frame-Options%5D=DENY&h%5BContent-Security-Policy%5D=frame-ancestors%20%27none%27&statuscode=200)  
   
   [http://127.0.0.1:8000/h.php?h[X-Frame-Options]=DENY&h[Content-Security-Policy]=frame-ancestors%20%27none%27&statuscode=403](http://127.0.0.1:8000/h.php?h%5BX-Frame-Options%5D=DENY&h%5BContent-Security-Policy%5D=frame-ancestors%20%27none%27&statuscode=403)  
   
   and observe the results.

Results:  

XFO + CSP frame-ancestors + Status Code 200 => no Performance entry  

XFO + CSP frame-ancestors + Status Code 403 => 1 Performance entry

Status Code 200 => 1 Performance entry  

Status Code 403 => 1 Performance entry

**Problem Description:**  

In <https://crbug.com/chromium/1038036> a bug was reported that allows an attacker to differentiate between response status codes Error (= 40x or 50x) and Success (= 20x or 30x) by counting performance entries.

This issue was previously fixed by making sure that subresource requests that get a failing status code still get their resource-timing entries reported: <https://chromium-review.googlesource.com/c/chromium/src/+/1796544>

However, this fix does not work when embedding is not allowed (XFO or CSP frame-ancestors). This is especially problematic because these headers are supposed to protect the resource.

For example, this bug can be used to identify if the user visiting the attack's page is the owner of a specific Youtube channel:

<https://studio.youtube.com/channel/><correct channel id> => XFO and 200  

<https://studio.youtube.com/channel/><wrong channel id> => XFO and 403

See poc.html for details on this attack.

Note 1: Status codes can also be detected with stylesheets and script tags by listing for onload and onerror. (poc.html Check2). However, CORP would block this attack, but not the one described above. Fetch metadata are also different.

Note 2: Detecting XFO or CSP frame-ancestors is also possible with this leak:

XFO or/and CSP frame-ancestors + Status Code 200 => no Performance entry  

Status Code 200 => 1 Performance entry

**Additional Comments:**

\*\*Chrome version: \*\* 108.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [h.php](attachments/h.php) (text/plain, 337 B)
- [object-performanceapi-poc.html](attachments/object-performanceapi-poc.html) (text/plain, 4.6 KB)

## Timeline

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-12)

I can reproduce this as described on asan-linux-release-1058931 (equivalent to 108)

### [Deleted User] (2022-12-12)

[Empty comment from Monorail migration]

### aj...@google.com (2022-12-13)

-> yoavweiss based on https://crbug.com/chromium/1038036 - is this the same thing?


[Monorail components: Blink>SecurityFeature>CORS]

### yo...@chromium.org (2022-12-13)

Superficially, this seems like very similar indeed..

### yo...@chromium.org (2022-12-13)

https://chromium-review.googlesource.com/c/chromium/src/+/4100609 adds tests that should fail based on this bug report, yet don't.

Maybe there's something else that causes the issue, beyond X-frame-options?

### [Deleted User] (2022-12-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yo...@chromium.org (2022-12-14)

Re #6, there was an issue in the test. I'm now able to reproduce the issue.

### yo...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### yo...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-09)

nrosenthal: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-24)

nrosenthal: Uh oh! This issue still open and hasn't been updated in the last 45 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nr...@chromium.org (2023-01-25)

[Empty comment from Monorail migration]

### nr...@chromium.org (2023-01-25)

This happens because we don't report fallback timing in the case of plugin error events. Fixing.

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### ad...@google.com (2023-02-16)

(auto-cc on security bug)

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb

commit 5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb
Author: Noam Rosenthal <nrosenthal@chromium.org>
Date: Mon Feb 27 17:54:10 2023

Consolidate iframe & object resource timing code paths

So far some of the logic  in resource timing for subframe navigations
iframe/object/embed) was duplicated, e.g. both in blink and in content.

This has led to race conditions, inconsistencies and sometimes
XSS leaks.

This patch attempts to improve the situation by consolidating the code
paths:

- NavigationRequest receives is_container_initiated, which ensures only
  container-initiated navigations are reported to the parent. This
  is a clarification of something that was ambiguous in the spec
  previously (https://github.com/whatwg/html/issues/8846).
  It later uses ParentResourceTimingAccess to decide if a navigation
  should report to its parent with/without response details
  (status code and mime-type), or not report at all (TAO-fail, not
  an iframe, not container-initiated).

- Both object fallbacks and cancelled navigations (204/205) report
  to the parent via RenderFrameImpl, and blink converts that to a
  ResourceTimingInfo object. This allows us to remove the duplicated
  resource timing creation code in //content.

- We report fallback resource timing also for plugin error events and
  not only for load events.

Bug: 1399862
Bug: 1410705
Change-Id: Id37d23cd02eee9e38f812e6f3da99caedafdee3d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4214695
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Noam Rosenthal <nrosenthal@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1110433}

[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/frame.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/public/web/web_navigation_params.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/navigator.h
[delete] https://crrev.com/5981fcb6e1fecfd7de85d69c5d42f37eb79ba86f/content/browser/loader/resource_timing_utils.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/loader/frame_load_request.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/loader/object_navigation_fallback_body_loader.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/navigator.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/loader/object_navigation_fallback_body_loader.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/local_frame_client_impl.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/ipc_utils.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/frame.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/web_tests/external/wpt/resource-timing/iframe-sequence-of-events.html
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/test/navigation_simulator_impl.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/local_frame_mojo_handler.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/remote_frame.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/public/test/fake_local_frame.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/local_frame_client_impl.cc
[delete] https://crrev.com/5981fcb6e1fecfd7de85d69c5d42f37eb79ba86f/content/browser/loader/resource_timing_utils.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/html/html_plugin_element.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/render_frame_proxy_host.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/loader/navigation_url_loader_unittest.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/timing/performance.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/local_frame_client.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/common/frame.mojom
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/DEPS
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/public/test/fake_local_frame.h
[add] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/web_tests/external/wpt/resource-timing/entries-for-object-frame-options-deny.html
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/public/mojom/navigation/navigation_params.mojom
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/loader/empty_clients.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/html/html_frame_owner_element.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/html/html_frame_owner_element.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/test/test_render_frame_host.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/loader/empty_clients.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/navigation_controller_impl.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/web_tests/external/wpt/resource-timing/resources/frame-timing.js
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/public/web/web_navigation_timings.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/BUILD.gn
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/remote_frame.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/public/mojom/frame/frame.mojom
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/navigation_controller_impl.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/loader/navigation_url_loader_impl_unittest.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/local_frame.h
[add] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/web_tests/external/wpt/resource-timing/resources/object-frame-options-200.asis
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/html/html_frame_element_base.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/public/mojom/frame/remote_frame.mojom
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/public/test/fake_remote_frame.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/timing/performance.h
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/renderer/render_frame_impl.cc
[add] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/web_tests/external/wpt/resource-timing/resources/object-frame-options-403.asis
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/third_party/blink/renderer/core/frame/local_frame.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/public/test/fake_remote_frame.cc
[modify] https://crrev.com/5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb/content/browser/security_exploit_browsertest.cc


### nr...@chromium.org (2023-02-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/103c852b146f0ee1f7fe2693f92f17523fd1a305

commit 103c852b146f0ee1f7fe2693f92f17523fd1a305
Author: Dan H <harringtond@chromium.org>
Date: Mon Feb 27 22:56:43 2023

Revert "Consolidate iframe & object resource timing code paths"

This reverts commit 5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb.

Reason for revert: MSan failures crbug.com/1420057

Original change's description:
> Consolidate iframe & object resource timing code paths
>
> So far some of the logic  in resource timing for subframe navigations
> iframe/object/embed) was duplicated, e.g. both in blink and in content.
>
> This has led to race conditions, inconsistencies and sometimes
> XSS leaks.
>
> This patch attempts to improve the situation by consolidating the code
> paths:
>
> - NavigationRequest receives is_container_initiated, which ensures only
>   container-initiated navigations are reported to the parent. This
>   is a clarification of something that was ambiguous in the spec
>   previously (https://github.com/whatwg/html/issues/8846).
>   It later uses ParentResourceTimingAccess to decide if a navigation
>   should report to its parent with/without response details
>   (status code and mime-type), or not report at all (TAO-fail, not
>   an iframe, not container-initiated).
>
> - Both object fallbacks and cancelled navigations (204/205) report
>   to the parent via RenderFrameImpl, and blink converts that to a
>   ResourceTimingInfo object. This allows us to remove the duplicated
>   resource timing creation code in //content.
>
> - We report fallback resource timing also for plugin error events and
>   not only for load events.
>
> Bug: 1399862
> Bug: 1410705
> Change-Id: Id37d23cd02eee9e38f812e6f3da99caedafdee3d
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4214695
> Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
> Reviewed-by: Daniel Cheng <dcheng@chromium.org>
> Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
> Commit-Queue: Noam Rosenthal <nrosenthal@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1110433}

Bug: 1399862
Bug: 1410705
Bug: 1420057
Change-Id: Icfc5b6ca7ebd718b2fff58e3f5c7765c53ee93f9
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4295881
Owners-Override: Dan H <harringtond@chromium.org>
Reviewed-by: Dan H <harringtond@chromium.org>
Commit-Queue: Dan H <harringtond@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1110619}

[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/frame.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/public/web/web_navigation_params.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/navigator.h
[add] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/loader/resource_timing_utils.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/loader/frame_load_request.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/loader/object_navigation_fallback_body_loader.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/loader/object_navigation_fallback_body_loader.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/navigator.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/local_frame_client_impl.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/ipc_utils.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/frame.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/web_tests/external/wpt/resource-timing/iframe-sequence-of-events.html
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/test/navigation_simulator_impl.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/local_frame_mojo_handler.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/remote_frame.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/public/test/fake_local_frame.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/local_frame_client_impl.cc
[add] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/loader/resource_timing_utils.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/html/html_plugin_element.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/render_frame_proxy_host.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/loader/navigation_url_loader_unittest.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/timing/performance.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/local_frame_client.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/common/frame.mojom
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/DEPS
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/public/test/fake_local_frame.h
[delete] https://crrev.com/faee629e20dd36f843ea6df900f2fd4b382dab78/third_party/blink/web_tests/external/wpt/resource-timing/entries-for-object-frame-options-deny.html
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/public/mojom/navigation/navigation_params.mojom
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/loader/empty_clients.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/html/html_frame_owner_element.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/html/html_frame_owner_element.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/test/test_render_frame_host.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/loader/empty_clients.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/navigation_controller_impl.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/web_tests/external/wpt/resource-timing/resources/frame-timing.js
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/public/web/web_navigation_timings.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/BUILD.gn
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/remote_frame.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/public/mojom/frame/frame.mojom
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/renderer_host/navigation_controller_impl.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/loader/navigation_url_loader_impl_unittest.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/local_frame.h
[delete] https://crrev.com/faee629e20dd36f843ea6df900f2fd4b382dab78/third_party/blink/web_tests/external/wpt/resource-timing/resources/object-frame-options-200.asis
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/html/html_frame_element_base.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/public/mojom/frame/remote_frame.mojom
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/public/test/fake_remote_frame.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/timing/performance.h
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/renderer/render_frame_impl.cc
[delete] https://crrev.com/faee629e20dd36f843ea6df900f2fd4b382dab78/third_party/blink/web_tests/external/wpt/resource-timing/resources/object-frame-options-403.asis
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/public/test/fake_remote_frame.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/third_party/blink/renderer/core/frame/local_frame.cc
[modify] https://crrev.com/103c852b146f0ee1f7fe2693f92f17523fd1a305/content/browser/security_exploit_browsertest.cc


### gi...@appspot.gserviceaccount.com (2023-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c8d82e52681f338bc4671df333a2bc9d6c93a32c

commit c8d82e52681f338bc4671df333a2bc9d6c93a32c
Author: Noam Rosenthal <nrosenthal@chromium.org>
Date: Tue Feb 28 10:46:20 2023

Reland "Consolidate iframe & object resource timing code paths"

This is a reland of commit 5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb

(Reland change: initializing
WebNavigationTimings::parent_resource_timing_access, caught by MSAN)
Original change's description:
> Consolidate iframe & object resource timing code paths
>
> So far some of the logic  in resource timing for subframe navigations
> iframe/object/embed) was duplicated, e.g. both in blink and in content.
>
> This has led to race conditions, inconsistencies and sometimes
> XSS leaks.
>
> This patch attempts to improve the situation by consolidating the code
> paths:
>
> - NavigationRequest receives is_container_initiated, which ensures only
>   container-initiated navigations are reported to the parent. This
>   is a clarification of something that was ambiguous in the spec
>   previously (https://github.com/whatwg/html/issues/8846).
>   It later uses ParentResourceTimingAccess to decide if a navigation
>   should report to its parent with/without response details
>   (status code and mime-type), or not report at all (TAO-fail, not
>   an iframe, not container-initiated).
>
> - Both object fallbacks and cancelled navigations (204/205) report
>   to the parent via RenderFrameImpl, and blink converts that to a
>   ResourceTimingInfo object. This allows us to remove the duplicated
>   resource timing creation code in //content.
>
> - We report fallback resource timing also for plugin error events and
>   not only for load events.
>
> Bug: 1399862
> Bug: 1410705
> Change-Id: Id37d23cd02eee9e38f812e6f3da99caedafdee3d
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4214695
> Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
> Reviewed-by: Daniel Cheng <dcheng@chromium.org>
> Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
> Commit-Queue: Noam Rosenthal <nrosenthal@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1110433}

Bug: 1399862
Bug: 1410705
Change-Id: Ica01bcc861ffd60909e9adad79ef2f71ab23f98e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296794
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Noam Rosenthal <nrosenthal@chromium.org>
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1110858}

[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/frame.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/public/web/web_navigation_params.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/navigator.h
[delete] https://crrev.com/67e938017f886bc2a044f2384a85f877d8f0bca7/content/browser/loader/resource_timing_utils.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/loader/frame_load_request.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/loader/object_navigation_fallback_body_loader.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/navigator.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/loader/object_navigation_fallback_body_loader.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/local_frame_client_impl.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/ipc_utils.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/web_tests/external/wpt/resource-timing/iframe-sequence-of-events.html
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/frame.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/test/navigation_simulator_impl.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/local_frame_mojo_handler.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/remote_frame.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/public/test/fake_local_frame.cc
[delete] https://crrev.com/67e938017f886bc2a044f2384a85f877d8f0bca7/content/browser/loader/resource_timing_utils.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/local_frame_client_impl.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/html/html_plugin_element.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/render_frame_proxy_host.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/loader/navigation_url_loader_unittest.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/timing/performance.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/local_frame_client.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/common/frame.mojom
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/DEPS
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/public/test/fake_local_frame.h
[add] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/web_tests/external/wpt/resource-timing/entries-for-object-frame-options-deny.html
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/public/mojom/navigation/navigation_params.mojom
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/loader/empty_clients.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/html/html_frame_owner_element.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/html/html_frame_owner_element.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/loader/empty_clients.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/test/test_render_frame_host.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/navigation_controller_impl.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/web_tests/external/wpt/resource-timing/resources/frame-timing.js
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/public/web/web_navigation_timings.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/BUILD.gn
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/remote_frame.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/public/mojom/frame/frame.mojom
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/renderer_host/navigation_controller_impl.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/loader/navigation_url_loader_impl_unittest.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/local_frame.h
[add] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/web_tests/external/wpt/resource-timing/resources/object-frame-options-200.asis
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/html/html_frame_element_base.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/public/mojom/frame/remote_frame.mojom
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/public/test/fake_remote_frame.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/timing/performance.h
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/renderer/render_frame_impl.cc
[add] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/web_tests/external/wpt/resource-timing/resources/object-frame-options-403.asis
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/public/test/fake_remote_frame.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/third_party/blink/renderer/core/frame/local_frame.cc
[modify] https://crrev.com/c8d82e52681f338bc4671df333a2bc9d6c93a32c/content/browser/security_exploit_browsertest.cc


### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d1b49ff4d15bc538c4feddff9f81253bba6abd9d

commit d1b49ff4d15bc538c4feddff9f81253bba6abd9d
Author: Sergey Poromov <poromov@chromium.org>
Date: Wed Mar 01 10:25:38 2023

Revert "Reland "Consolidate iframe & object resource timing code paths""

This reverts commit c8d82e52681f338bc4671df333a2bc9d6c93a32c.

Reason for revert: Unblocking revert at https://crrev.com/c/4295184

Original change's description:
> Reland "Consolidate iframe & object resource timing code paths"
>
> This is a reland of commit 5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb
>
> (Reland change: initializing
> WebNavigationTimings::parent_resource_timing_access, caught by MSAN)
> Original change's description:
> > Consolidate iframe & object resource timing code paths
> >
> > So far some of the logic  in resource timing for subframe navigations
> > iframe/object/embed) was duplicated, e.g. both in blink and in content.
> >
> > This has led to race conditions, inconsistencies and sometimes
> > XSS leaks.
> >
> > This patch attempts to improve the situation by consolidating the code
> > paths:
> >
> > - NavigationRequest receives is_container_initiated, which ensures only
> >   container-initiated navigations are reported to the parent. This
> >   is a clarification of something that was ambiguous in the spec
> >   previously (https://github.com/whatwg/html/issues/8846).
> >   It later uses ParentResourceTimingAccess to decide if a navigation
> >   should report to its parent with/without response details
> >   (status code and mime-type), or not report at all (TAO-fail, not
> >   an iframe, not container-initiated).
> >
> > - Both object fallbacks and cancelled navigations (204/205) report
> >   to the parent via RenderFrameImpl, and blink converts that to a
> >   ResourceTimingInfo object. This allows us to remove the duplicated
> >   resource timing creation code in //content.
> >
> > - We report fallback resource timing also for plugin error events and
> >   not only for load events.
> >
> > Bug: 1399862
> > Bug: 1410705
> > Change-Id: Id37d23cd02eee9e38f812e6f3da99caedafdee3d
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4214695
> > Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
> > Reviewed-by: Daniel Cheng <dcheng@chromium.org>
> > Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
> > Commit-Queue: Noam Rosenthal <nrosenthal@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#1110433}
>
> Bug: 1399862
> Bug: 1410705
> Change-Id: Ica01bcc861ffd60909e9adad79ef2f71ab23f98e
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296794
> Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
> Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
> Commit-Queue: Noam Rosenthal <nrosenthal@chromium.org>
> Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
> Reviewed-by: Daniel Cheng <dcheng@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1110858}

Bug: 1399862
Bug: 1410705
Change-Id: I35e3a03d38be4d2cc42d18ee0ed0296b978da090
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4299069
Auto-Submit: Sergey Poromov <poromov@chromium.org>
Reviewed-by: Sergey Poromov <poromov@chromium.org>
Owners-Override: Sergey Poromov <poromov@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Sergey Poromov <poromov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1111499}

[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/frame.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/public/web/web_navigation_params.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/navigator.h
[add] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/loader/resource_timing_utils.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/loader/frame_load_request.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/loader/object_navigation_fallback_body_loader.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/navigator.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/loader/object_navigation_fallback_body_loader.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/local_frame_client_impl.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/ipc_utils.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/frame.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/test/navigation_simulator_impl.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/local_frame_mojo_handler.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/remote_frame.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/public/test/fake_local_frame.cc
[add] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/loader/resource_timing_utils.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/local_frame_client_impl.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/html/html_plugin_element.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/render_frame_proxy_host.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/loader/navigation_url_loader_unittest.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/timing/performance.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/local_frame_client.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/common/frame.mojom
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/DEPS
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/public/test/fake_local_frame.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/public/mojom/navigation/navigation_params.mojom
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/loader/empty_clients.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/html/html_frame_owner_element.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/html/html_frame_owner_element.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/loader/empty_clients.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/test/test_render_frame_host.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/navigation_controller_impl.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/public/web/web_navigation_timings.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/BUILD.gn
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/remote_frame.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/public/mojom/frame/frame.mojom
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/navigation_controller_impl.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/loader/navigation_url_loader_impl_unittest.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/local_frame.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/html/html_frame_element_base.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/public/mojom/frame/remote_frame.mojom
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/public/test/fake_remote_frame.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/timing/performance.h
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/third_party/blink/renderer/core/frame/local_frame.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/public/test/fake_remote_frame.cc
[modify] https://crrev.com/d1b49ff4d15bc538c4feddff9f81253bba6abd9d/content/browser/security_exploit_browsertest.cc


### gi...@appspot.gserviceaccount.com (2023-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dd557c16af01b29c0263c8108c4893b2ac2ff343

commit dd557c16af01b29c0263c8108c4893b2ac2ff343
Author: Sergey Poromov <poromov@chromium.org>
Date: Wed Mar 01 11:28:45 2023

Reland "Reland "Consolidate iframe & object resource timing code paths""

This reverts commit d1b49ff4d15bc538c4feddff9f81253bba6abd9d.

Reason for revert: The failing tests will be fixed instead of reverting the original CL that caused them.

Original change's description:
> Revert "Reland "Consolidate iframe & object resource timing code paths""
>
> This reverts commit c8d82e52681f338bc4671df333a2bc9d6c93a32c.
>
> Reason for revert: Unblocking revert at https://crrev.com/c/4295184
>
> Original change's description:
> > Reland "Consolidate iframe & object resource timing code paths"
> >
> > This is a reland of commit 5dcb6f7b01d5f51144a9ba847c34bb0cdc344ccb
> >
> > (Reland change: initializing
> > WebNavigationTimings::parent_resource_timing_access, caught by MSAN)
> > Original change's description:
> > > Consolidate iframe & object resource timing code paths
> > >
> > > So far some of the logic  in resource timing for subframe navigations
> > > iframe/object/embed) was duplicated, e.g. both in blink and in content.
> > >
> > > This has led to race conditions, inconsistencies and sometimes
> > > XSS leaks.
> > >
> > > This patch attempts to improve the situation by consolidating the code
> > > paths:
> > >
> > > - NavigationRequest receives is_container_initiated, which ensures only
> > >   container-initiated navigations are reported to the parent. This
> > >   is a clarification of something that was ambiguous in the spec
> > >   previously (https://github.com/whatwg/html/issues/8846).
> > >   It later uses ParentResourceTimingAccess to decide if a navigation
> > >   should report to its parent with/without response details
> > >   (status code and mime-type), or not report at all (TAO-fail, not
> > >   an iframe, not container-initiated).
> > >
> > > - Both object fallbacks and cancelled navigations (204/205) report
> > >   to the parent via RenderFrameImpl, and blink converts that to a
> > >   ResourceTimingInfo object. This allows us to remove the duplicated
> > >   resource timing creation code in //content.
> > >
> > > - We report fallback resource timing also for plugin error events and
> > >   not only for load events.
> > >
> > > Bug: 1399862
> > > Bug: 1410705
> > > Change-Id: Id37d23cd02eee9e38f812e6f3da99caedafdee3d
> > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4214695
> > > Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
> > > Reviewed-by: Daniel Cheng <dcheng@chromium.org>
> > > Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
> > > Commit-Queue: Noam Rosenthal <nrosenthal@chromium.org>
> > > Cr-Commit-Position: refs/heads/main@{#1110433}
> >
> > Bug: 1399862
> > Bug: 1410705
> > Change-Id: Ica01bcc861ffd60909e9adad79ef2f71ab23f98e
> > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296794
> > Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
> > Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
> > Commit-Queue: Noam Rosenthal <nrosenthal@chromium.org>
> > Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
> > Reviewed-by: Daniel Cheng <dcheng@chromium.org>
> > Cr-Commit-Position: refs/heads/main@{#1110858}
>
> Bug: 1399862
> Bug: 1410705
> Change-Id: I35e3a03d38be4d2cc42d18ee0ed0296b978da090
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4299069
> Auto-Submit: Sergey Poromov <poromov@chromium.org>
> Reviewed-by: Sergey Poromov <poromov@chromium.org>
> Owners-Override: Sergey Poromov <poromov@chromium.org>
> Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
> Commit-Queue: Sergey Poromov <poromov@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1111499}

Bug: 1399862
Bug: 1410705
Change-Id: I3458949b0632b266e24a000a10f864189fd8d1db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4299070
Auto-Submit: Sergey Poromov <poromov@chromium.org>
Owners-Override: Sergey Poromov <poromov@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Sergey Poromov <poromov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1111522}

[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/frame.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/public/web/web_navigation_params.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/navigator.h
[delete] https://crrev.com/4fc47f3a7b57ae56e3eb90ea36ecea6b1904f8ef/content/browser/loader/resource_timing_utils.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/loader/frame_load_request.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/loader/frame_loader.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/loader/object_navigation_fallback_body_loader.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/loader/object_navigation_fallback_body_loader.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/navigator.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/local_frame_client_impl.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/ipc_utils.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/frame.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/test/navigation_simulator_impl.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/local_frame_mojo_handler.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/remote_frame.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/public/test/fake_local_frame.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/local_frame_client_impl.cc
[delete] https://crrev.com/4fc47f3a7b57ae56e3eb90ea36ecea6b1904f8ef/content/browser/loader/resource_timing_utils.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/html/html_plugin_element.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/render_frame_proxy_host.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/loader/navigation_url_loader_unittest.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/timing/performance.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/local_frame_client.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/common/frame.mojom
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/DEPS
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/public/test/fake_local_frame.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/loader/document_loader.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/public/mojom/navigation/navigation_params.mojom
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/loader/empty_clients.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/html/html_frame_owner_element.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/html/html_frame_owner_element.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/platform/loader/fetch/resource_timing_utils.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/test/test_render_frame_host.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/loader/empty_clients.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/navigation_controller_impl.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/public/web/web_navigation_timings.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/BUILD.gn
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/remote_frame.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/public/mojom/frame/frame.mojom
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/navigation_controller_impl.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/renderer_host/navigation_request.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/loader/navigation_url_loader_impl_unittest.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/local_frame.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/html/html_frame_element_base.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/public/mojom/frame/remote_frame.mojom
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/public/test/fake_remote_frame.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/loader/document_loader.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/timing/performance.h
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/third_party/blink/renderer/core/frame/local_frame.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/public/test/fake_remote_frame.cc
[modify] https://crrev.com/dd557c16af01b29c0263c8108c4893b2ac2ff343/content/browser/security_exploit_browsertest.cc


### am...@google.com (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Thank you for the report! The VRP Panel has decided to award you $1,000 for this report. If you would like to be acknowledged for this report, please let us know what name/handle/tag we should use in doing so. Thank you for taking the time to report this issue to us! 

### ku...@googlemail.com (2023-03-10)

Thank you very much. Please use @kunte_ctf 

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-02)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1399862?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062152)*
