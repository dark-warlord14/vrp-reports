# Cross-Origin image data leak via cache and canvas

| Field | Value |
|-------|-------|
| **Issue ID** | [40090099](https://issues.chromium.org/issues/40090099) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Image, Blink>SecurityFeature>CORS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | hi...@chromium.org |
| **Created** | 2018-01-05 |
| **Bounty** | $4,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3312.0 Safari/537.36

Steps to reproduce the problem:
1. Go to https://vulnerabledoma.in/chrome_cache_image_leak.html . This page has an img tag which loads a same-origin PNG image and an iframe tag which embeds a cross-origin page:

<img src="//vulnerabledoma.in/rgb.png" style="width:300px;height:100px;image-rendering:pixelated">
<iframe src="//l0.cm/chrome_cache_image_leak.html"></iframe>

The `rgb.png` is an image having red, green and blue pixels.

The cross-origin page has the following code which loads the rgb.png on canvas:

<canvas id="canvas"></canvas>
<script>
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var img = new Image();
img.src = '//vulnerabledoma.in/rgb.png';
img.onload=function(){
ctx.drawImage(img, 0, 0);
[...]
}
</script>

In additon, the page has the code which tries to read three pixels:

 console.log(ctx.getImageData(0,0,1,1).data);//red
 console.log(ctx.getImageData(1,0,1,1).data);//green
 console.log(ctx.getImageData(2,0,1,1).data);//blue

2.  See your console. Usually the `getImageData` method call against a cross-origin image is blocked. But if my PoC works well, you can see three pixel data:

Uint8ClampedArray(4) [255, 0, 0, 255] //red
Uint8ClampedArray(4) [0, 255, 0, 255] //green
Uint8ClampedArray(4) [0, 0, 255, 255] //blue

What is the expected behavior?
The following error should be thrown:
Uncaught DOMException: Failed to execute 'getImageData' on 'CanvasRenderingContext2D': The canvas has been tainted by cross-origin data.

What went wrong?
The cross-origin data is leaked via cached data and cross-origin iframe.

Did this work before? N/A 

Chrome version: 65.0.3312.0  Channel: canary
OS Version: 10.0
Flash Version:

## Attachments

- [SOPViolationInCanvasMemoryCache..png](attachments/SOPViolationInCanvasMemoryCache..png) (image/png, 72.6 KB)

## Timeline

### el...@chromium.org (2018-01-05)

Very cool find.

I can reliably reproduce this in 63.0.3239.132 but not 64.0.3282.71 or 65.0.3312.0 (getting the Access Denied script error in both later builds), but it sounds like you're saying that you can reproduce this in Chrome 65?

Could you tweak the POC so that it shows the data in the frame instead of the console, so we can rule out any impact of the Developer Tools being open?

[Monorail components: Blink>Canvas]

### ma...@gmail.com (2018-01-05)

I modified the PoC. It shows the data in the frame now.
If you can't reproduce it, please use "Reload" button in the page instead of a manual reload. I can always reproduce it on 65.0.3312.0 via the button. 

### el...@chromium.org (2018-01-05)

RE #2: Thanks! 

I've reproduced this on Chrome 64.0.3282.71 on a Lenovo T460s, but I haven't yet managed to reproduce in Chrome 65. My guess is that there's a race condition somewhere in the loader/memory cache.



### el...@chromium.org (2018-01-05)

Repros in ToT on the latest Chromium.
Version 65.0.3312.0 (Developer Build) (32-bit)

ImageResource::IsAccessAllowed is returning true from IsSameOriginOrCORSSuccessful().

### el...@chromium.org (2018-01-05)

In the insecure case, the IsSameOriginOrCORSSuccessful function returns true for the resource whose URL is "https://vulnerabledoma.in/rgb.png" because it has cors_status_ == CORSStatus::kSameOrigin.

In the secure case, IsSameOriginOrCORSSuccessful returns false and security_origin->TaintsCanvas(GetResponse().Url()) returns true, leading the canvas to be tainted.

### me...@chromium.org (2018-01-05)

I was also able to reproduce. 

I'll add that when I refresh the page the POC fails and I get the following warning in the console:

chrome_cache_image_leak.html:11 Uncaught DOMException: Failed to execute 'getImageData' on 'CanvasRenderingContext2D': The canvas has been tainted by cross-origin data.
    at Image.img.onload (https://l0.cm/chrome_cache_image_leak.html:11:62)



xlai@ could you take a look at this please?

### el...@chromium.org (2018-01-05)

Returning false from ImageResource::CanReuse makes the bug go away.

My non-expert guess about what happens is that we have two Resource Requests for the image running in parallel, one in the main frame and one in the subframe. If the request in the mainframe is registered first, the second request blocks on the completion of the first Resource and reuses it. Critically, however, the first Resource has a cors_status_ of CORSStatus::kSameOrigin as set by ResourceLoader::DetermineCORSStatus.

When the second context reuses the Resource, calls to ImageResource::IsAccessAllowed see that the Resource has a CORS status of kSameOrigin and does not care that |security_origin| has no relationship to |GetResponse().Url()|.

In contrast, if the timing works out such that the Resource isn't reused, the DetermineCORSStatus function gets called with a |source_origin| from the cross-origin subframe, and the Resource is NOT marked CORSStatus::kSameOrigin and the canvas is properly tainted.


### el...@chromium.org (2018-01-05)

https://chromium.googlesource.com/chromium/src/+/e8de0e46213b60669a73760f30aa59c74f43f1f9 is the Chrome 61 CL that changed ImageResource::IsAccessAllowed to check the cached CORS status set by the ResourceLoader instead of performing an access-control check with the supplied |security_origin|.

### xl...@chromium.org (2018-01-05)

Hmmm. I don't think this issue is in the implementation of canvas2d's GetImageData function. In this example, it reads the image from the ImageElement,
which is one type of CanvasImageSource. The cross-origin detection relies on the
value returns by WouldTaintOrigin(), which is overridden in ImageElementBase; by tracing the code, it is the ImageResourceContent::IsAccessAllowed that decides
the value.

[Monorail components: -Blink>Canvas Blink>Image]

### el...@chromium.org (2018-01-05)

I believe hintzed was an intern who has moved on. 

mkwst tends to be an expert in these sorts of things and may have a good suggestion on who should own.

### sh...@chromium.org (2018-01-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-20)

mkwst: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mk...@chromium.org (2018-01-22)

I believe toyoshim@ picked up the refactoring work hintzed@ started. toyoshim@, would you mind taking a look at this? CCing kinuko@ as well.

[Monorail components: Blink>SecurityFeature>CORS]

### to...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### to...@chromium.org (2018-01-29)

cc: relevant people, probably Something is wrong in DetermineRevalidationPolicy. Let me take a look.

### to...@chromium.org (2018-01-29)

hum... kForceCache was set against the resource for an unknown reason. Let me go deeper.

### to...@chromium.org (2018-01-29)

I'm seeing several related bugs on investigating the issue.

 1. Specifying kForceCache may bypass CORS check in DetermineRevalidationPolicy for image taint tracking.

 2. Memory cache is used for the second image load even DevTools disables the cache (not a security issue, but unexpected)

 3. kFrameLoadTypeBackForward is passed to the iframe for unknown reasons (now I'm investigating this)

3. will be the root cause of this specific bug, but 1. is also still a bad security issue if this is true even when JavaScript calls history.back

I will continue to investigate this tomorrow, but probably Hiroshige-san may have better knowledge on 1 and 2.

### to...@chromium.org (2018-01-29)

Oops, the reason of 3 is just because my Chrome restores the test page on launching. So, related problems are 1 and 2, and the root of this issue is DetermineRevalidationPolicy reaches to the last line that returns kUse.

Hiroshige-san, can you own this bug?

### ma...@gmail.com (2018-01-29)

>1. is also still a bad security issue if this is true even when JavaScript calls history.back
I confirmed this bug works via history.back.
PoC is here: https://l0.cm/chrome_cache_image_leak2_start.html

### el...@chromium.org (2018-01-29)

Re #18, "2. Memory cache is used for the second image load even DevTools disables the cache (not a security issue, but unexpected)". 

I believe that is https://crbug.com/chromium/644828, which was deemed WONTFIX.



### to...@chromium.org (2018-01-30)

I talked with yhirano@.

So, current memory cache design shares the Resource instance over all origins in the same renderer process. But, CORSStatus was evaluated for the first request in ResourceLoader, and stored in the Resource instance. This is wrong, and we need to have the CORSStatus in ResourceClient side rather than Resource.

I think this is not a recent regression, but long living memory cache design issue. Let me check if we can have a fix without a large design change.

Note that this issue does not happen if site isolation is enabled (of course).

### to...@chromium.org (2018-01-30)

Plan A is to move the CORSStatus from Resource to ResourceClient. This is not s simple change.

Plan B is to stop sharing Resource instance among different source origins. Cons of this plan is we may see performance regressions for increased memory cache misses, but still it hits the disk cache. We will see a similar regression when we enable the site isolation. Also, once CORS support is moved out of renderer process, per-origin CORS check will require an IPC call to evaluate the CORSStatus for each origin.

So, at this point, Plan B looks reasonable even if we may see some performance regressions.

### to...@chromium.org (2018-01-30)

CL for the Plan B; https://chromium-review.googlesource.com/c/chromium/src/+/892722

### to...@chromium.org (2018-01-30)

Had a VC with hiroshige.
I completely overlooked the https://crbug.com/chromium/799477#c8, and will explore a CL that virtually reverts that change.

### to...@chromium.org (2018-01-31)

[Empty comment from Monorail migration]

### to...@chromium.org (2018-02-01)

Hi Security Team, should the fix for this be merged to any release branch?

Information for the decision follows.

- This was regressed at m61
- Canvas image taint, and CORS and SRI checks for images and scripts can be bypassed, if it is still on memory cache
- The memory cache is shared among the same renderer process, that says if the site isolation is enabled, the issue should be hidden.

Tentatively reassigned to hiroshige@ who is trying to have the first fix.

### el...@chromium.org (2018-02-01)

Regarding merges: This is currently Severity-Medium, which makes a merge to Stable conditional upon the risk/complexity of the fix.

https://www.chromium.org/developers/severity-guidelines
"If the fix seems too complicated to merge to the current stable milestone, assign it to the next stable milestone."

Having said that, can you please elaborate on 

"SRI checks for images and scripts can be bypassed, if it is still on memory cache"

How is the SRI check for scripts bypassed? That sounds significantly different than the issue with ImageResource::IsAccessAllowed. Is it? Has a bug with a repro for that issue been filed?

### hi...@chromium.org (2018-02-01)

SRI should block (according to [1]) a subresource if CORS check fails OR the integrity check (e.g. hash check) fails.
Currently, e.g. no-cors cross-origin <script> with correct integrity attribute can be executed, while it should be (and had been) blocked due to lack of CORS headers. (I expect the security impact is smaller than the canvas taint check bypassing)

[1] https://codesearch.chromium.org/chromium/src/third_party/WebKit/Source/platform/loader/SubresourceIntegrity.cpp?sq=package:chromium&l=101

### hi...@chromium.org (2018-02-01)

Correction to https://crbug.com/chromium/799477#c29:
In fact, the SRI issue is related to another issue that causes potential SRI bypassing, and probably this issue doesn't cause regression in SRI checks.

### ty...@chromium.org (2018-02-02)

Wrote a patch that implements the approach I suggested in the VC.
https://chromium-review.googlesource.com/c/chromium/src/+/897040
Confirmed that this prevents pixels from being read by the script.

### bu...@chromium.org (2018-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fad67a5b73639d7211b24fd9bdb242e82039b765

commit fad67a5b73639d7211b24fd9bdb242e82039b765
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Wed Feb 07 23:00:05 2018

Check CORS using PassesAccessControlCheck() with supplied SecurityOrigin

Partial revert of https://chromium-review.googlesource.com/535694.

Bug: 799477
Change-Id: I878bb9bcb83afaafe8601293db9aa644fc5929b3
Reviewed-on: https://chromium-review.googlesource.com/898427
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Takeshi Yoshino <tyoshino@chromium.org>
Cr-Commit-Position: refs/heads/master@{#535176}
[add] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/LayoutTests/external/wpt/html/semantics/scripting-1/the-script-element/cacheable-script-throw.py
[add] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/LayoutTests/external/wpt/html/semantics/scripting-1/the-script-element/muted-errors-iframe.html
[add] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/LayoutTests/external/wpt/html/semantics/scripting-1/the-script-element/muted-errors.sub.html
[modify] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/Source/core/loader/modulescript/DocumentModuleScriptFetcher.cpp
[modify] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/Source/core/loader/resource/ImageResource.cpp
[modify] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/Source/core/loader/resource/ScriptResource.cpp
[modify] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/Source/core/loader/resource/ScriptResource.h
[modify] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/Source/core/script/ClassicPendingScript.cpp
[modify] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/Source/platform/loader/fetch/Resource.cpp
[modify] https://crrev.com/fad67a5b73639d7211b24fd9bdb242e82039b765/third_party/WebKit/Source/platform/loader/fetch/Resource.h


### hi...@chromium.org (2018-02-09)

The fix landed on 66.0.3343.0 and stayed on canary for one day. Requesting merge to M-65.

### sh...@chromium.org (2018-02-09)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

+awhalley@ (Security TPM) for M65 merge review.

### sh...@chromium.org (2018-02-09)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-02-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-12)

govind@ - good for 65

### go...@chromium.org (2018-02-12)

Approving merge to M65 branch 3325 based on https://crbug.com/chromium/799477#c38. Please merge ASAP so we can pick it up for this week Beta release. Thank you.

### aw...@google.com (2018-02-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15

commit 8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Mon Feb 12 21:52:23 2018

Check CORS using PassesAccessControlCheck() with supplied SecurityOrigin

Partial revert of https://chromium-review.googlesource.com/535694.

Bug: 799477
Change-Id: I878bb9bcb83afaafe8601293db9aa644fc5929b3
Reviewed-on: https://chromium-review.googlesource.com/898427
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Takeshi Yoshino <tyoshino@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#535176}(cherry picked from commit fad67a5b73639d7211b24fd9bdb242e82039b765)
Reviewed-on: https://chromium-review.googlesource.com/914927
Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Commit-Position: refs/branch-heads/3325@{#434}
Cr-Branched-From: bc084a8b5afa3744a74927344e304c02ae54189f-refs/heads/master@{#530369}
[add] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/LayoutTests/external/wpt/html/semantics/scripting-1/the-script-element/cacheable-script-throw.py
[add] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/LayoutTests/external/wpt/html/semantics/scripting-1/the-script-element/muted-errors-iframe.html
[add] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/LayoutTests/external/wpt/html/semantics/scripting-1/the-script-element/muted-errors.sub.html
[modify] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/Source/core/loader/modulescript/DocumentModuleScriptFetcher.cpp
[modify] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/Source/core/loader/resource/ImageResource.cpp
[modify] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/Source/core/loader/resource/ScriptResource.cpp
[modify] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/Source/core/loader/resource/ScriptResource.h
[modify] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/Source/core/script/ClassicPendingScript.cpp
[modify] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/Source/platform/loader/fetch/Resource.cpp
[modify] https://crrev.com/8f4341f9eb29137d8cc52bdd4d9fcdd2e1328b15/third_party/WebKit/Source/platform/loader/fetch/Resource.h


### ty...@chromium.org (2018-02-13)

Checked the beta builder.

win64%20beta/builds/2707
mac64%20beta/builds/3261
linux64%20beta/builds/3101

were all broken due to compile failure happened before hiroshige@'s patch.

They all passed later.


### bu...@chromium.org (2018-02-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c1df004861ab704945d31a0d207bb7f4c205e60c

commit c1df004861ab704945d31a0d207bb7f4c205e60c
Author: Takeshi Yoshino <tyoshino@chromium.org>
Date: Mon Feb 19 05:25:55 2018

Stop reusing MemoryCache entries for requests with a different source origin.

ResourceFetcher/ResourceLoader now saves the result of the CORS check on
the Resource object. Though the result of the CORS check varies
depending on the source origin, reusing an existing resource fetched by
a different source origin is allowed by mistake.

This patch introduces a logic to prevent MemoryCache entries from being
reused for requests with a different source (requestor) origin by saving
the source origin on the Resource object and comparing that with the new
source origin in Resource::CanReuse(), so that the result of the CORS
check is reused only when the source origin is the same.

An alternative possibly-better approach is to isolate MemoryCache for
different origins by changing the cache identifier to take into account
the source origin of requests. However, to keep the patch small and fix
the issue quickly, this patch just prevents reuse.

Bug: 799477, 809350
Change-Id: Ib96c9e728abe969a53f3d80519118a83392067b4
Reviewed-on: https://chromium-review.googlesource.com/897040
Commit-Queue: Takeshi Yoshino <tyoshino@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#537580}
[add] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/LayoutTests/external/wpt/cors/image-tainting-in-cross-origin-iframe.sub.html
[add] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/LayoutTests/external/wpt/cors/resources/image-tainting-checker.sub.html
[add] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/LayoutTests/external/wpt/images/blue-png-cachable.py
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/core/loader/resource/ImageResource.cpp
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/core/loader/resource/ImageResource.h
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/MemoryCacheCorrectnessTest.cpp
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/RawResource.cpp
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/RawResource.h
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/RawResourceTest.cpp
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/Resource.cpp
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/Resource.h
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/ResourceFetcher.cpp
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/ResourceFetcher.h
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/ResourceFetcherTest.cpp
[modify] https://crrev.com/c1df004861ab704945d31a0d207bb7f4c205e60c/third_party/WebKit/Source/platform/loader/fetch/ResourceRequest.h


### aw...@chromium.org (2018-02-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-19)

Congratulations masatokinugawa@! The VRP panel decided to award $4,000 for this report :-D

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-08-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086

commit c1b6d6a2b7a6e834bdeeca93269cfaffb123a086
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Wed Aug 15 09:19:32 2018

Remove per-client CORS checks

Those are needed because a request could match with another request made
by a foreign origin, but [1] fixed the issue. This is basically reverting
[2]. Two layout tests are added to detect regressions.

This CL changes the behavior a bit. Without this CL,

 - A response with a proper access-control-allow-origin header for a
   cross-origin request with "no-cors" mode is treated as
   non-opaque, and
 - A response without a proper access-control-allow-origin header for a
   same-origin request with "no-cors" mode redirected from a cross-origin
   resource is treated as opaque

while with this CL,

 - A response with a proper access-control-allow-origin header for a
   cross-origin request with "no-cors" mode is treated as opaque, and
 - A response without a proper access-control-allow-origin header for a
   same-origin request with "no-cors" mode redirected from a cross-origin
   resource is treated as non-opaque.

Also, before this CL, CORSStatus is calculated with an opaque origin for
top-level worklet scripts. This CL changes that: now CORSStatus is
calculated with the origin of the parent context, and so it stops muting
error messages in worklets.

1: https://chromium.googlesource.com/chromium/src.git/+/c1df004861ab704945d31a0d207bb7f4c205e60c
2: https://chromium.googlesource.com/chromium/src.git/+/fad67a5b73639d7211b24fd9bdb242e82039b765

Bug: 809350, 799477
Change-Id: If28f59f6e6ac03a4d5992cca85801231748019bd
Reviewed-on: https://chromium-review.googlesource.com/1158165
Commit-Queue: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
Reviewed-by: Fredrik Söderquist <fs@opera.com>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Commit-Position: refs/heads/master@{#583202}
[add] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/WebKit/LayoutTests/http/tests/security/cors-check-for-cached-image.html
[add] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/WebKit/LayoutTests/http/tests/security/cors-check-for-cached-script.html
[add] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/WebKit/LayoutTests/http/tests/security/resources/cors-check-for-cached-image-iframe.html
[add] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/WebKit/LayoutTests/http/tests/security/resources/cors-check-for-cached-script-iframe.html
[add] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/WebKit/LayoutTests/http/tests/security/resources/cors-image.php
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/WebKit/LayoutTests/http/tests/security/resources/cors-script.php
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/blink/renderer/core/loader/modulescript/document_module_script_fetcher.cc
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/blink/renderer/core/loader/modulescript/worker_module_script_fetcher.cc
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/blink/renderer/core/loader/modulescript/worklet_module_script_fetcher.cc
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/blink/renderer/core/loader/resource/image_resource.cc
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/blink/renderer/core/loader/resource/script_resource.cc
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/blink/renderer/core/loader/resource/script_resource.h
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/blink/renderer/core/script/classic_pending_script.cc
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/blink/renderer/platform/loader/fetch/resource.cc
[modify] https://crrev.com/c1b6d6a2b7a6e834bdeeca93269cfaffb123a086/third_party/blink/renderer/platform/loader/fetch/resource.h


### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/799477?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Image, Blink>SecurityFeature>CORS]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090099)*
