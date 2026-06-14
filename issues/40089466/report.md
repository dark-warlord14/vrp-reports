# Read cross-origin video using Canvas and Service Worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40089466](https://issues.chromium.org/issues/40089466) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>SameOriginPolicy, Blink>ServiceWorker, Internals>Media>Network |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2017-11-01 |
| **Bounty** | $4,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36

Steps to reproduce the problem:
1. Go to https://attack.shhnjk.com/steal_svg.html
2. Reload the page.
3. Click on get image button.

What is the expected behavior?
canvas.toDataURL() is blocked for cross-origin image or video. 

What went wrong?
Back in 2014, Chrome fixed a canvas bug[1] which allowed attacker to steal image cross-origin. This attack used cache to bypass cross-origin check.

Time goes on, and now we have Service Worker. Chrome had a bug in SW[2] which allowed attacker to treat cross-origin CSS file as same origin by intercepting same-origin request and responding with cross-origin resource. 

We can use these tricks combined to steal cross-origin image/video again!

[1]: https://bugs.chromium.org/p/chromium/issues/detail?id=380885
[2]: https://bugs.chromium.org/p/chromium/issues/detail?id=598077

Did this work before? N/A 

Chrome version: 62.0.3202.75  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### el...@chromium.org (2017-11-01)

Great find! 

Also repros in 64.0.3254.0, which is after the fix for https://crbug.com/chromium/761622 landed, so this is a new issue.

[Monorail components: Blink>Canvas Blink>SecurityFeature>SameOriginPolicy Blink>ServiceWorker]

### el...@chromium.org (2017-11-01)

Removing Blink>Canvas, which apparently leaks all bugs to a public mailing list.

[Monorail components: -Blink>Canvas]

### el...@chromium.org (2017-11-01)

This does seem to be limited to cross-origin video, right? Trying to use the same trick to launder the origin of an image doesn't appear to be effective.

### el...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### el...@chromium.org (2017-11-01)

Inside ImageResource::IsAccessAllowed, we have an explicit check to see whether the data is kServiceWorkerOpaque

  if (GetCORSStatus() == CORSStatus::kServiceWorkerOpaque)
    return false;

HTMLMediaElement::IsMediaDataCORSSameOrigin does not seem to have the same type of check. Maybe it needs one?

### s....@gmail.com (2017-11-01)

Hmm, seems like video only :( That's sad.

### el...@chromium.org (2017-11-01)

jrummell@: Can you please take a look at this and if needed, suggest a more appropriate owner?

### el...@chromium.org (2017-11-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### jr...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2017-11-02)

We have this test:

https://cs.chromium.org/chromium/src/media/blink/resource_multibuffer_data_provider.cc?l=349

Which is insufficient for some reason. =>hubbe 

### da...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

[Monorail components: Internals>Media>Network]

### s....@gmail.com (2017-11-02)

Hi, does anyone know if creating bitmap image from cross-origin image is allowed? Following test case alerts security error on Firefox but successful on Chrome.

https://attack.shhnjk.com/canvid.html

### el...@chromium.org (2017-11-02)

Re #13: Stealing pixels of images cross domains is forbidden. Loading your attack repro in Chrome 62 and Chrome 64 yields the expected script error:

"Uncaught DOMException: Failed to execute 'toDataURL' on 'HTMLCanvasElement': Tainted canvases may not be exported."

### s....@gmail.com (2017-11-02)

Re #14: Sorry for the confusion. Forget about get image button there. Creating 2nd image (the one at the bottom) using createImageBitmap() is forbidden on Firefox. I guess createImageBitmap doesn't steal pixel though.

### el...@chromium.org (2017-11-02)

Got it. In terms of the standards question, I believe Chrome's behavior is correct, and Firefox's is not. Specifically:

https://html.spec.whatwg.org/multipage/imagebitmap-and-animations.html#dom-createimagebitmap
If the origin of image's image is not the same origin as the origin specified by the entry settings object, then set the origin-clean flag of the ImageBitmap object's bitmap to false.

If you do find a vector by which the image bitmaps pixels can be read, please do file a separate issue. Thanks!

### el...@chromium.org (2017-11-03)

Re #11 - My read of the check mentioned in #11 is that it ensures that we don't mix data from multiple sources in a single data buffer. But in the attack scenario, all of the data is stored from the one fetch done by the service worker. Assuming that the code in that test works right, the buffer's url_data_'s data_origin_ would properly contain the origin of the cross-domain victim site, but nothing looks at it.

Maybe we need something like this code that we have in the redirect handler, which sets single_origin_ to false if there's a redirection?
  if (url_data_->url().GetOrigin() != destination->url().GetOrigin()) {
    single_origin_ = false;
  }

While a serviceworker delivering a cross-origin opaque fetch isn't exactly the same as a redirect, it behaves in a similar manner...

### hu...@chromium.org (2017-11-03)

You mean like this:
https://cs.chromium.org/chromium/src/media/blink/multibuffer_data_source.cc?type=cs&q=single_origin_&sq=package:chromium&l=230

### el...@chromium.org (2017-11-03)

Re #18: Exactly-- We have that code in the redirect handler, but we don't have equivalent (same_origin_ = false) tainting in the case where a ServiceWorker responds to a same-origin fetch by returning an opaque response from a cross-origin fetch.

### es...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### hu...@chromium.org (2017-11-10)

So how/where do we do the tainting for service workers?
Why are service workers allowed to fetch data from one origin and return it in another?


### s....@gmail.com (2017-11-14)

Service Worker is kind of proxy. It can intercept request made by client (of SW, in this case, window) and respond with something else. But cross-origin response remains unreadable unless it satisfies CORS. In this case, SW used mode: 'no-cors', which essentially does request without CORS. 

Seems like this bug is exploitable even after enabling Site Isolation (chrome://flags/#enable-site-per-process). Is it a site isolation bug or it's just out of scope for Site Isolation?

### pa...@chromium.org (2017-11-15)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-11-15)

It seems like some combination of blink::ResourceResponse::UrlListViaServiceWorker and ResourceResponse::ResponseTypeViaServiceWorker() should give you the information you need? Not entirely sure what the correct checks are, but if you do want to support opaque responses but do the correct tainting that should either tell you if the response was opaque, or if the response was fetched cross origin.

### me...@chromium.org (2017-11-15)

And from the spec side, it doesn't seem like it's very well defined what it means for an image to be origin-clean? https://html.spec.whatwg.org/multipage/canvas.html#the-image-argument-is-not-origin-clean doesn't actually say how you're supposed to get the origin of an element (origin of the src attribute? origin of the last redirect? And yeah, the service worker complications. There has been some discussion and back/forth about what the URL for a response from a service worker should be (request URL vs URL of whatever was fetched), but if origin clean doesn't even mention that it should be the origin of the response, that wouldn't help either...

### el...@chromium.org (2017-11-20)

Re #25: While the Canvas spec may not be fully clear, we do know what same-origin-policy forbids (it forbids cross-origin reads) and as a consequence we know what behavior we need. Specifically, we know that using the origin of the SRC attribute isn't sufficient, because if only the initial SRC were checked, that would allow data theft via a cross-origin redirect. So, code that properly taints canvases does so even in the face of such redirect.

The problem in this codepath is that we don't taint if a service worker returns a response which was opaque because it was fetched from a different origin.

### sh...@chromium.org (2017-11-25)

hubbe: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-10)

hubbe: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2017-12-11)

While this bug is video-specific, it really seems to be caused by service workers. (As in: If there were no service workers, we wouldn't have a problem.) What's more, it's not clear to me what the right fix is. I'm happy to help implement the fix if someone can just tell me what it it is...

Assigning to someone who seems to know more for now.


### el...@chromium.org (2017-12-14)

falken@ -- Can you please help us find an expert on the ServiceWorker team that can help the Media team correctly identify when a given response is a cross-origin opaque response and thus should taint a Canvas that contains data from such a response?

I tried to point in what I hoped was a useful direction in Comments #5 and #17, but I suspect that a ServiceWorker expert will be able to provide more actionable/correct guidance.

Thanks!

### fa...@chromium.org (2017-12-15)

Nice find.

I think this is likely similar to https://crbug.com/chromium/598077 as noted in the original bug report, and likely an extension of https://crbug.com/chromium/553535 or https://crbug.com/chromium/435446.

For this bug we'll want to check the blink::ResourceResponse or content:: WebURLResponse for media content, and check WasFetchedViaServiceWorker() and OriginalURLViaServiceWorker(). That should give you the actual origin the content came from (after redirects). As noted above, we already have this check in https://cs.chromium.org/chromium/src/media/blink/resource_multibuffer_data_provider.cc?l=349:

// This test is vital for security!
const GURL& original_url = response.WasFetchedViaServiceWorker()
                                 ? response.OriginalURLViaServiceWorker()
                                 : response.Url();

So evidently we need to add this check to another place, I guess there is a simple case somewhere when it isn't a "multibuffer" resource?

### fa...@chromium.org (2017-12-15)

I made an official build and ran the test. I confirmed the "vital for security" code path is reached and knows the actual origin of the response:
[1:1:1215/150752.931041:ERROR:resource_multibuffer_data_provider.cc(353)] virtual void media::ResourceMultiBufferDataProvider::DidReceiveResponse(const blink::WebURLResponse &): sw? 1, url = https://www.w3schools.com/html/mov_bbb.mp4

I see now what c#30 means about canvas. When the test does drawImage() to write from the video to the canvas, the canvas should be marked as tainted.

I'm not sure where that code lives.

### fa...@chromium.org (2017-12-15)

We have some related tests here:
https://cs.chromium.org/chromium/src/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting.https.html?q=fetch-canvas-tainting-iframe.html&sq=package:chromium&dr=C&l=36

### fa...@chromium.org (2017-12-15)

I think I see a solution. In ResourceMultiBufferDataProvider::DidReceiveResponse() , we must set |destination_url_data| to the actual response. 

So something like this:

  if (!redirects_to_.is_empty()) {
    destination_url_data =
        url_data_->url_index()->GetByUrl(redirects_to_, cors_mode_);
    redirects_to_ = GURL();
  } else if (response.WasFetchedViaServiceWorker()) {
    const GURL& original_url = response.OriginalURLViaServiceWorker();
    if (!original_url.is_empty()) {
      destination_url_data =
          url_data_->url_index()->GetByUrl(original_url, cors_mode_);
    }
  }

This seems to get the data sourced recognized as cross-origin via
blink::HTMLMediaElement::IsMediaDataCORSSameOrigin() 
media::WebMediaPlayerImpl::DidPassCORSAccessCheck()
MultibufferDataSource::DidPassCORSAccessCheck()
UrlData::cors_mode()



I'm not too sure whether the SW check should come before or after the redirect check. Probably before, as OriginalURLViaServiceWorker() returns the final response after redirects.

### fa...@chromium.org (2017-12-15)

That fix turns out too simplistic because even if the service worker response was same-origin as the request, MultibufferDataSource::DidPassCORSAccessCheck() returns false since cors_mode_ is UNSPECIFIED. I'm not sure why redirects don't have the same issue.

I have a WIP patch here, feel free to comment or take it over:
https://chromium-review.googlesource.com/c/chromium/src/+/828564

### s....@gmail.com (2017-12-16)

I have a better PoC now. I can steal "stream" not just "pixel". And this also works with audio.

1. Go to https://test.shhnjk.com/video_check.html
2. Wait for 11 seconds.

It will record "hidden" and "muted" video for 10 seconds, and then convert blob of that recorded video to data URL. Finally, converted data URL is set to another video tag.



### fa...@chromium.org (2017-12-18)

Some updates:
* As hubbe@ points out on https://chromium-review.googlesource.com/c/chromium/src/+/828564, we don't want to set destination_url_data.
* horo@ points out we should be using WebURLResponse::FetchResponseType (we'll need to add a getter for it), not comparing the URLs directly in order to determine opaqueness. Otherwise we would taint all cross-origin responses, even if the fetch performed a valid CORS request.
* Plumbing FetchResponseType to UrlData and then to MultibufferDataSource::DidPassCORSAccessCheck() seems promising. But I think there is still an escape hatch in that  HTMLMediaElement::IsMediaDataCORSSameOrigin() will ultimately return true: in the SW proxied case, source URL will be same-origin and no redirects will occur, so HasSingleSecurityOrigin() will return true.
* Setting HasSingleSecurityOrigin to false whenever SW proxies the response from cross-origin would probably work, but it will disallow the case where a valid CORS request happened (e.g, to a CDN with Allow-Access-*). Setting to it to false only when the response was opaque seems to make the concept more complex. Hrm.

### fa...@chromium.org (2017-12-19)

Sorry that I won't be able to fix this before vacation.

If anyone wants to take this while I'm away I think the way forward is:
* Expose WebURLResponse::FetchResponseType()
* Teach MultibufferDataSource about the fetch response type.
* Change HTMLMediaElement::IsMediaDataCORSSameOrigin() to something like:

bool HTMLMediaElement::IsMediaDataCORSSameOrigin(
    const SecurityOrigin* origin) const {
  // If a service worker handled the request, we don't know if the origin in the
  // src is the same as the actual response URL so can't rely on URL checks
  // alone. So detect an opaque response via
  // DidGetOpaqueResponseFromServiceWorker().
  if (GetWebMediaPlayer() &&
      GetWebMediaPlayer()->DidGetOpaqueResponseFromServiceWorker()) {
    return false;
  }

  // Otherwise, HasSingleSecurityOrigin() tells us whether the origin in the src
  // is the same as the actual request (i.e. after redirect).
  if (!HasSingleSecurityOrigin())
    return false;

  // DidPassCORSAccessCheck() means it was a successful CORS-enabled fetch
  // (vs. non-CORS-enabled or failed).
  // TaintsCanvas() does CheckAccess() on the URL plus allow data sources,
  // to ensure that it is not a URL that requires CORS (basically same
  // origin).
  return (GetWebMediaPlayer() &&
          GetWebMediaPlayer()->DidPassCORSAccessCheck()) ||
         !origin->TaintsCanvas(currentSrc()));
         !origin->TaintsCanvas(currentSrc());
}
* Do a similar thing for audio elements.
* Expand the WPT fetch-canvas-tainting.html test to also test video and audio.

### s....@gmail.com (2018-01-25)

No activity for a month now. Is anyone working on the fix?

### fa...@chromium.org (2018-01-25)

I've been working on other things since returning from break. I had a local patch and was trying to get tests working. I'll try to resume my work.

### bu...@chromium.org (2018-01-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0595c4d499e667842991af8d879b0e55b4058984

commit 0595c4d499e667842991af8d879b0e55b4058984
Author: Matt Falkenhagen <falken@chromium.org>
Date: Mon Jan 29 07:05:15 2018

service worker: Refactor and comment WPT test fetch-canvas-tainting.

This uses promise_test for each test case instead of an all-or-nothing
result, which makes the test easier to extend and debug. It also
adds more explanatory comments.

R=horo, shimazu

Bug: 780435
Change-Id: I3ac77448cd19e66b9db806e6b8b5530857713c6c
Reviewed-on: https://chromium-review.googlesource.com/890694
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Cr-Commit-Position: refs/heads/master@{#532339}
[modify] https://crrev.com/0595c4d499e667842991af8d879b0e55b4058984/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-cache.https.html
[modify] https://crrev.com/0595c4d499e667842991af8d879b0e55b4058984/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting.https.html
[modify] https://crrev.com/0595c4d499e667842991af8d879b0e55b4058984/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-canvas-tainting-iframe.html
[add] https://crrev.com/0595c4d499e667842991af8d879b0e55b4058984/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-canvas-tainting-tests.js
[modify] https://crrev.com/0595c4d499e667842991af8d879b0e55b4058984/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-rewrite-worker.js


### bu...@chromium.org (2018-01-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b52069772cb2dfc046c92354522e1d9d1f04843b

commit b52069772cb2dfc046c92354522e1d9d1f04843b
Author: Matt Falkenhagen <falken@chromium.org>
Date: Tue Jan 30 08:47:20 2018

service worker: Add tests for canvas tainting from video.

R=horo

Bug: 780435
Change-Id: Ie8ae9cf8dca55f122a7b4a984ca0a96035b0099f
Reviewed-on: https://chromium-review.googlesource.com/892683
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#532814}
[modify] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/TestExpectations
[rename] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-image-cache.https.html
[rename] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-image.https.html
[add] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video-cache.https-expected.txt
[copy] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video-cache.https.html
[add] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video.https-expected.txt
[copy] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video.https.html
[modify] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-access-control.py
[modify] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-canvas-tainting-iframe.html
[modify] https://crrev.com/b52069772cb2dfc046c92354522e1d9d1f04843b/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-canvas-tainting-tests.js


### bu...@chromium.org (2018-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/aae1788f5c1ffc97dc1d7fb409ad97328302ec73

commit aae1788f5c1ffc97dc1d7fb409ad97328302ec73
Author: Matt Falkenhagen <falken@chromium.org>
Date: Fri Feb 02 00:23:51 2018

service worker: Add tests for canvas tainting from a video with range requests.

This tests that a canvas is tainted when the video had multiple responses
from a service worker, if any of the responses were opaque.

Bug: 780435
Change-Id: Ifef394c87921cb646b1728a9079908264673fdd4
Reviewed-on: https://chromium-review.googlesource.com/897165
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#533869}
[add] https://crrev.com/aae1788f5c1ffc97dc1d7fb409ad97328302ec73/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video-with-range-request.https-expected.txt
[add] https://crrev.com/aae1788f5c1ffc97dc1d7fb409ad97328302ec73/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video-with-range-request.https.html
[modify] https://crrev.com/aae1788f5c1ffc97dc1d7fb409ad97328302ec73/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-access-control.py
[add] https://crrev.com/aae1788f5c1ffc97dc1d7fb409ad97328302ec73/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-event-network-fallback-worker.js
[add] https://crrev.com/aae1788f5c1ffc97dc1d7fb409ad97328302ec73/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/range-request-to-different-origins-worker.js
[add] https://crrev.com/aae1788f5c1ffc97dc1d7fb409ad97328302ec73/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/range-request-with-different-cors-modes-worker.js


### bu...@chromium.org (2018-02-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b147c5f0c82332833a763f94f5949eff34f4cfa1

commit b147c5f0c82332833a763f94f5949eff34f4cfa1
Author: Matt Falkenhagen <falken@chromium.org>
Date: Fri Feb 02 03:17:35 2018

Enable <video> to see if a response from a service worker was cross-origin.

Previously, if the <video> src was same-origin as the page, and the
service worker intercepted the request and responded with an opaque
response (by making a cross-origin request without CORS sharing),
the <video> would be considered same-origin data.

The solution is to teach the data backing <video> about FetchResponseType,
which tells us if a response is opaque or non-opaque.

There is some complexity with multiple responses due to range requests/
partial content responses. It's possible that some responses are
opaque and some are non-opaque. Once the opaque bit is set, it shouldn't
be cleared.

This fixes tests added in:
https://chromium-review.googlesource.com/c/chromium/src/+/892683 and
https://chromium-review.googlesource.com/c/chromium/src/+/897165

Bug: 780435
Change-Id: I95f7f088d907f84edd4c2db8b57532e761237465
Reviewed-on: https://chromium-review.googlesource.com/828564
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Reviewed-by: Fredrik Hubinette <hubbe@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#533942}
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/content/renderer/media/webmediaplayer_ms.cc
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/content/renderer/media/webmediaplayer_ms.h
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/content/renderer/media_capture_from_element/html_video_element_capturer_source_unittest.cc
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/media/blink/DEPS
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/media/blink/multibuffer_data_source.cc
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/media/blink/multibuffer_data_source.h
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/media/blink/resource_multibuffer_data_provider.cc
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/media/blink/url_index.cc
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/media/blink/url_index.h
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/media/blink/webmediaplayer_impl.cc
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/media/blink/webmediaplayer_impl.h
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video-cache.https-expected.txt
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video-with-range-request.https-expected.txt
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-video.https-expected.txt
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/third_party/WebKit/Source/core/html/media/HTMLMediaElement.cpp
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/third_party/WebKit/Source/platform/exported/WebURLResponse.cpp
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/third_party/WebKit/Source/platform/testing/EmptyWebMediaPlayer.h
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/third_party/WebKit/public/platform/WebMediaPlayer.h
[modify] https://crrev.com/b147c5f0c82332833a763f94f5949eff34f4cfa1/third_party/WebKit/public/platform/WebURLResponse.h


### fa...@chromium.org (2018-02-02)

c#44 fixed the <video> bug and should be included in the next one or two Canaries and shipped in stable in Chrome 66.

I'm wondering if we need to do anything with <audio>. I guess there is no concept like canvas tainting with audio. On the other hand we have code like  MediaElementAudioSourceHandler::PassesCORSAccessCheck().

I'll open a new bug to track generally auditing service worker interaction with HTML elements like this.

### fa...@chromium.org (2018-02-02)

I filed https://crbug.com/chromium/808334.

### s....@gmail.com (2018-02-02)

Please make sure to fix the audio bug in M66 too. I will disclose this bug once Chrome 66 is released.

### aw...@google.com (2018-02-06)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-02-07)

I've also confirmed that the fix stops the MediaRecorder attack from c#36 via:
Uncaught DOMException: Failed to execute 'captureStream' on 'HTMLMediaElement': Cannot capture from element with cross-origin data

But the tests I've added are only testing <canvas>. It'd be good to add a test for MediaRecorder too.

### s....@gmail.com (2018-02-07)

Hmm, Audio seems fixed too.
1. Go to https://test.shhnjk.com/audio_hack.html
2. Reload the page.

Same error as c#49.


### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

falken@ - how do you feel about the safety of merging this to M65?  Thanks!

### fa...@chromium.org (2018-02-09)

It's a tricky and subtle patch in an area of the codebase I'm unfamiliar with. I would not bet a lot on the safety of it.

### aw...@google.com (2018-02-09)

Thanks falken@, we can wait until 66.

### aw...@chromium.org (2018-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-09)

Congrats! The VRP panel decided to award $4,000 for this report :-)

### aw...@google.com (2018-02-09)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/780435?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>SameOriginPolicy, Blink>ServiceWorker, Internals>Media>Network]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089466)*
