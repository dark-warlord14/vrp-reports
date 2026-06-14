# Security: Possible to retrieve cross-origin image data from canvas

| Field | Value |
|-------|-------|
| **Issue ID** | [40093139](https://issues.chromium.org/issues/40093139) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Canvas, Blink>ServiceWorker |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | de...@gmail.com |
| **Assignee** | fa...@chromium.org |
| **Created** | 2018-11-20 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

The canvas element allows cross-origin images to be drawn within it, but will prevent the image data from being read back out. Internally, the canvas caches the list of URLs it's seen before and whether or not they tainted the canvas. That way, when an image is drawn, the cached result can be re-used, rather than performing the tainted check again.

While this works in most cases, it doesn't work too well when service workers are used. A site can use a service worker to return a custom response for a cross-origin image. This image would be drawn on the canvas and the result of the tainted check would be stored internally by the canvas (as the image was not actually retrieved from a different origin, the canvas would not be considered tainted).

Then, the site could retrieve the image again, though this time from the actual origin. This image would taint the canvas, but it doesn't, because the original tainted result is used instead. The site can then read the data from the canvas using one if its export methods.

It's also possible to use this general idea to retrieve frames from a cross-origin video.

**VERSION**  

Chrome Version: Tested on 70.0.3538.110 (stable) and 72.0.3616.0 (canary)  

Operating System: Windows 10 Pro, version 1803

**REPRODUCTION CASE**

1. The attached files form a simple website. To begin with, download each of the files and place them in a directory.
2. In the directory you downloaded the files to, run the following command in a terminal:

python3 -m http.server 8080

This will start a simple web server that can be used to serve the files in the directory.  

3. In the browser, navigate to the following location:

<http://localhost:8080/index.html>

4. This page will create an image element and load a cross-origin image into it (in this case <https://en.wikipedia.org/static/images/project-logos/enwiki.png>).
5. The page will then install a service worker (service\_worker.js).
6. Once the service worker is active, the page will create another image element with the same source. This time, however, the service worker will intercept the request and return a local image from the site instead (local.png, which is simply a 1x1 transparent pixel).
7. The page will draw this image onto a canvas. The canvas will check whether the image would taint the canvas (which it won't, as the response wasn't actually cross-origin) and it will then cache the result of the check for this source URL.
8. The page will then draw the original cross-origin image (obtained in step 4) onto the canvas. This should result in the canvas being tainted, however, that doesn't happen as the tainted result obtained and cached in step 7 is re-used.
9. The canvas will then be exported using the following call:

canvas.toDataURL();

This data will then be assigned to the source of an image displayed under the "Output image" section of the page.  

10. The service worker will then be unregistered. This is done simply so that the page works in the same way each time it's loaded.

As mentioned in the summary, it's also possible to retrieve frames from a cross-origin video using this technique. The CanvasRenderingContext2D.drawImage() function can accept a video element as its first parameter. Therefore, by going through the steps above (except with a video), you can draw video frames on the canvas then extract them using the toDataURL() method.

The function that caches the result of the tainted check can be found at the following location:

<https://cs.chromium.org/chromium/src/third_party/blink/renderer/core/html/canvas/canvas_rendering_context.cc?l=166&rcl=13204491b69908ea885e7e2e125df59884803d22>

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [index.html](attachments/index.html) (text/plain, 266 B)
- [local.png](attachments/local.png) (image/png, 156 B)
- [main.js](attachments/main.js) (text/plain, 1.6 KB)
- [service_worker.js](attachments/service_worker.js) (text/plain, 343 B)
- [index.html](attachments/index_53093312.html) (text/plain, 266 B)
- [local.png](attachments/local_53093313.png) (image/png, 156 B)
- [main.js](attachments/main_53093314.js) (text/plain, 1.6 KB)
- [service_worker.js](attachments/service_worker_53093315.js) (text/plain, 341 B)

## Timeline

### de...@gmail.com (2018-11-20)

One thing to note is that while the image used in the demonstration has an "access-control-allow-origin: *" header present (meaning the image could be read anyway), this has no bearing on the example. Any image could be used and works equally well. I've attached a second example here that uses a different image (https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png), one that doesn't have the header set.

### mb...@chromium.org (2018-11-21)

falken: Are you the right owner for this, or do you happen to know who might be? Feel free to assign it back to me for re-triage if not.

[Monorail components: Blink>Canvas Blink>ServiceWorker]

### fa...@chromium.org (2018-11-21)

Thanks, looks similar to https://crbug.com/chromium/780435.

### fa...@chromium.org (2018-11-21)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-11-21)

I can reproduce this with the wikipedia image, but as noted it has opted into CORS so that seems WAI.

I can't reproduce this with the google.com image. It says:
main.js:24 Uncaught (in promise) DOMException: Failed to execute 'toDataURL' on 'HTMLCanvasElement': Tainted canvases may not be exported.
    at HTMLDocument.loadAndDrawImages

Tested on 70.0.3538.102 and  72.0.3610.2.

Can you recheck it's exportable with a non-CORS image?

### de...@gmail.com (2018-11-21)

I've tried with a few different cross-origin images, as well as a cross-origin video, none of which have the "access-control-allow-origin" header set, and can reproduce the issue in each case.

How are you performing the test with the google.com image? If it's by updating the URL in main.js, note that you'll also need to update the URL path in service_worker.js. It's also possible that the browser may have cached one of the files, so it might be worth double checking that. Finally, you might want to verify that the updated version of the service worker is what's being used. I've also seen issues when having multiple tabs open to http://localhost:8080/index.html causes issues, perhaps because it interferes with the service worker unregistration.

I had actually confirmed the bug with the google.com image to begin with, but thought I'd use another image for the demo and didn't realise it had the "access-control-allow-origin" header set until after I created the issue.

### fa...@chromium.org (2018-11-21)

You're right, I was only updating the path in one file. I'll try again after working on https://crbug.com/chromium/904219.

### sh...@chromium.org (2018-11-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-21)

[Empty comment from Monorail migration]

### fa...@chromium.org (2018-11-22)

+shimazu for context for the CL

### fa...@chromium.org (2018-11-22)

+fserb for context for the CL

### bu...@chromium.org (2018-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/48d01db7e4858ad06cebaea89aa55575ee1bdd42

commit 48d01db7e4858ad06cebaea89aa55575ee1bdd42
Author: Matt Falkenhagen <falken@chromium.org>
Date: Thu Nov 22 09:51:36 2018

WPT: service worker: canvas tainting with two images from the same URL

This adds a test that does the following:
- Writes to a canvas with a cors same-origin image
- Writes to a canvas with a cors cross-origin image from the same URL
- Tests that the canvas is tainted after the second step.

Bug: 907047
Change-Id: Ie231b442eb9b55c642b3957c065555e6f4997a83
Reviewed-on: https://chromium-review.googlesource.com/c/1347952
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Makoto Shimazu <shimazu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#610356}
[add] https://crrev.com/48d01db7e4858ad06cebaea89aa55575ee1bdd42/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-double-write.https-expected.txt
[add] https://crrev.com/48d01db7e4858ad06cebaea89aa55575ee1bdd42/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-double-write.https.html
[add] https://crrev.com/48d01db7e4858ad06cebaea89aa55575ee1bdd42/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/resources/fetch-canvas-tainting-double-write-worker.js


### bu...@chromium.org (2018-11-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/889ddafc7932e318d1f213bb4e0926e71cb94657

commit 889ddafc7932e318d1f213bb4e0926e71cb94657
Author: Matt Falkenhagen <falken@chromium.org>
Date: Thu Nov 22 22:47:18 2018

Remove caching of CORS info from CanvasRenderingContext.

Before this CL, CanvasRenderingContext remembered which request URLs
were CORS same-origin and which were CORS cross-origin. This worked
relatively well in a pre-service-worker world. But with service workers,
the same request URL can have different response URLs. Also, even if two
things have have the same response URL, they could differ in whether
they were CORS approved or not.

The solution is to remove the caching entirely. This causes more calls
to CanvasImageSource::WouldTaintOrigin(), but the implementations of
those look relatively lightweight so I don't expect performance to be
worse than tracking URLs in two HashSets.

Test: fetch-canvas-tainting-double-write.https.html added in
https://chromium-review.googlesource.com/c/chromium/src/+/1347952.

Bug: 907047
Change-Id: I4cf6289174935dee40ccad0364eb425d717b9f7f
Reviewed-on: https://chromium-review.googlesource.com/c/1347953
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Reviewed-by: Makoto Shimazu <shimazu@chromium.org>
Commit-Queue: Matt Falkenhagen <falken@chromium.org>
Cr-Commit-Position: refs/heads/master@{#610498}
[delete] https://crrev.com/e373f9b913736c34dcee1994120e08d0641da586/third_party/WebKit/LayoutTests/external/wpt/service-workers/service-worker/fetch-canvas-tainting-double-write.https-expected.txt
[modify] https://crrev.com/889ddafc7932e318d1f213bb4e0926e71cb94657/third_party/blink/renderer/core/html/canvas/canvas_rendering_context.cc
[modify] https://crrev.com/889ddafc7932e318d1f213bb4e0926e71cb94657/third_party/blink/renderer/core/html/canvas/canvas_rendering_context.h


### fa...@chromium.org (2018-11-26)

This is fixed. Should I merge to 71?

### fa...@chromium.org (2018-11-26)

BTW I did some archaeology about this caching and found it a bit interesting. WebKit removed the cache also, in: http://trac.webkit.org/changeset/167741. And it was originally introduced in: https://trac.webkit.org/changeset/61877.

### sh...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-03)

Hi derceg86@ - the VRP panel decided to award $4,000 for this report, many thanks! A member of our finance team will be in touch to arrange payments.

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### de...@gmail.com (2018-12-04)

Thanks!

### sh...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-12-14)

Already in 72

### kb...@chromium.org (2019-01-02)

[Empty comment from Monorail migration]

### fa...@chromium.org (2019-01-08)

Adding people from https://crbug.com/chromium/918460 who might want context.

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/907047?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Blink>ServiceWorker]
[Monorail blocking: crbug.com/chromium/918460]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093139)*
