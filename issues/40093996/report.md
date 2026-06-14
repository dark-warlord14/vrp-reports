# Security: CORS policy not applied for bitmap canvases loaded without CORS support

| Field | Value |
|-------|-------|
| **Issue ID** | [40093996](https://issues.chromium.org/issues/40093996) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Canvas, Blink>SecurityFeature>CORS |
| **Platforms** | Mac |
| **Reporter** | aa...@gmail.com |
| **Assignee** | aa...@chromium.org |
| **Created** | 2019-02-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The Cross-origin resource sharing (CORS) policy does not apply to bitmap  

canvases if no crossorigin attribute is specified for the image being rendered.  

Images on external domains protected by cookies or IP whitelisting can  

therefore be stolen using Cross-site Request Forgery even if the target server  

does not give CORS access to other domains.

**VERSION**  

Chrome Version: 72.0.3626.96 stable  

Operating System: macOS Mojave 10.14.1 (18B75)

**REPRODUCTION CASE**  

A tiny proof of concept is shown below.

<html><body>
<script charset="utf-8">
function getData() {
createImageBitmap(this, 0, 0, this.naturalWidth,
this.naturalHeight).then(function(bmap) {
var can = document.createElement('canvas');
var ctx = can.getContext('bitmaprenderer');
ctx.transferFromImageBitmap(bmap);
document.getElementById('result').textContent = can.toDataURL();
}); }
</script>
<!-- this image does is not served with any CORS headers (no Access-Control-Allow-Origin) -->
<img src="https://www.google.com/logos/doodles/2019/friedlieb-ferdinand-runges-225th-birthday-4887536710189056-law.gif" onload="getData.call(this)"/>
<br/><textarea readonly style="width:100%;height:10em" id="result"></textarea>
</body></html>

The image, which should not be accessible to JavaScript from origins other than  

<https://www.google.com> is in fact rendered in the canvas and its base64-encoded  

contents are displayed. Note that due to <https://crbug.com/chromium/838108> (<https://bugs.chromium.org/p/chromium/issues/detail?id=838108>)  

the transformed image is actually transparent. However it is clear that the  

CORS policy has not been applied when it should have been.

--- Detailed Proof of Concept ---  

A more detailed proof of concept is attached (requires python3):

- secret.png: a dummy image
- simple.py: will serve the current working directory over HTTP on port 58080;  
  
  it will set a cookie (foo=bar) and require this cookie for access  
  
  to secret.png
- poc.html: will embed secret.png as <img> twice: once with the  
  
  crossorigin="use-credentials" attribure and once without it;  
  
  then it will render each of the <img> elements in a 2D canvas and  
  
  in a bitmap canvas and display the result  
  
  Place all files in a single directory, then run "python3 simple.py". Follow the  
  
  instructions it shows. The result should be that only rendering the image  
  
  without the crossorigin attribute in a bitmap canvas is "stolen".

--- Discussion: impact and recommendation ---  

Websites commonly rely on the browser's same-origin policy to prevent  

cross-site request forgery and prevent read access to authenticated user's data.  

If a server does not explicitly allow a domain to access data from the page  

(using Access-Control-Allow-Origin) then the browser is supposed to deny  

JavaScript access to it. Chrome applies policy is applied to iframes, images,  

objects and scripts alike. The one exception being access via a bitmap canvas  

to images not loaded explicitly for crossorigin access.  

A suitable fix would apply the same check that is done when rendering in a 2D  

canvas and that results in the following error:  

Failed to execute 'toDataURL' on 'HTMLCanvasElement': Tainted canvases may not be exported.

--- Affected versions ---  

I believe all version which support Bitmap canvases are vulnerable. I tested:

- Chromium 64.0.3279.0 dev: no support for bitmap canvas; 2D canvas can read tainted canvases
- Chromium 67.0.3387.0 dev: both 2D and bitmap canvases can read tainted canvases  
  
  The bug for 2D canvases has been fixed some time between version 67.0.3387.0 and 71.0.3578.98

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: (twitter) @AaylaSecura1138, github.com/aayla-secura

## Attachments

- [simple.py](attachments/simple.py) (text/plain, 1.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 3.0 KB)
- [secret.png](attachments/secret.png) (image/png, 5.2 KB)
- [poc_hardcoded_target.html](attachments/poc_hardcoded_target.html) (text/plain, 2.7 KB)
- [diff-origin.png](attachments/diff-origin.png) (image/png, 613.6 KB)
- [same-origin.png](attachments/same-origin.png) (image/png, 604.7 KB)
- [current_93083a26ba0a1f79049b91af7aeced1afe0d91b8.png](attachments/current_93083a26ba0a1f79049b91af7aeced1afe0d91b8.png) (image/png, 68.2 KB)
- [revert_02c469f444a7e6a69e82d4301a0272435ce6be1a.png](attachments/revert_02c469f444a7e6a69e82d4301a0272435ce6be1a.png) (image/png, 631.0 KB)

## Timeline

### aa...@gmail.com (2019-02-08)

Apologies, the title is not quite accurate: the CORS policy kick in if the crossorigin attribute IS given. The issue here is for tainted canvases, i.e. where the image is not loaded with CORS support.

### mm...@chromium.org (2019-02-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>Canvas Blink>SecurityFeature>CORS]

### mm...@chromium.org (2019-02-08)

Thanks for your report and a great reproducer. Unfortunately, I'm getting an empty image 300x150 on Linux. Is this Mac specific?

### aa...@gmail.com (2019-02-08)

Hi, yes as I mentioned, this is a separate bug in Chrome, which renders the transformed Bitmap canvases transparent: https://crbug.com/chromium/838108 (https://bugs.chromium.org/p/chromium/issues/detail?id=838108)

However, the underlying same-origin policy violation is there: with 2D tainted canvases I get a security error, with Bitmap tainted canvases I get an image.

### sh...@chromium.org (2019-02-08)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-02-09)

[Empty comment from Monorail migration]

### fs...@chromium.org (2019-02-11)

[Empty comment from Monorail migration]

### fs...@chromium.org (2019-02-11)

[Empty comment from Monorail migration]

### aa...@chromium.org (2019-02-12)

In your tiny reproduce case the string resulting from `canvas.toDataURL();` is not a transparent version of the image, it's actually just a fully black transparent image. 

Taking that base64 string and re-rendering it shows that there's no data:

<html><body>
  <script charset="utf-8">
    function getData() {
      createImageBitmap(this, 0, 0, this.naturalWidth,
        this.naturalHeight).then(function(bmap) {

        // Original tiny bug
        var can = document.createElement('canvas');
        document.body.appendChild(can);
        var ctx = can.getContext('bitmaprenderer');
        ctx.transferFromImageBitmap(bmap);
        tainedImageData = can.toDataURL();
        document.getElementById('result').textContent = tainedImageData;

        // Create an image with the "tainted" data
        // And draw it to a 2D canvas
        var taintedImage = new Image(100, 100);
        taintedImage.src = tainedImageData;
        var canvas2d = document.createElement('canvas');
        document.body.appendChild(canvas2d);
        var ctx = canvas2d.getContext('2d');
        ctx.drawImage(taintedImage, 0, 0, can.width, can.height);

        // What are the actual pixel values of this image?
        var pixels = ctx.getImageData(0, 0, can.width, can.height).data;
        var allZeros = true;
        for (p in pixels) {
          if (pixels[p] != 0) {
            allZeros = false
          }
        }
        if (allZeros) {
          console.log("Leaked image is entirely black");
        } else {
          console.log("Leaked image has colored pixels");
        }
      }); }
  </script>
  <!-- this image does is not served with any CORS headers (no Access-Control-Allow-Origin) -->
  <img src="https://www.google.com/logos/doodles/2019/friedlieb-ferdinand-runges-225th-birthday-4887536710189056-law.gif" onload="getData.call(this)"/>
  <br/><textarea readonly style="width:100%;height:10em" id="result"></textarea>
</body></html>

So, it looks like this is a bug in ImageBitmapRenderingContext.toDataURL() and is not a security issue.


### aa...@gmail.com (2019-02-12)

The bug which causes a transparent bitmap image is completely separate and manifests itself even when the image is loaded from the SAME origin. I attach a slightly modified poc.html which loads secret.png from http://127.0.0.1:58080 (run previously attached simple.py or your own http server).

1) I open poc.html from http://127.0.0.1:58080 (same origin) and the transparent generic image is shown. The 2D canvas correctly shows secret.png
2) I open poc.html from http://localhost:58080 (different origin) and the transparent generic image is exactly the same as in 1). The 2D canvas now displays a clear security error.

What you are telling me, that the bitmap canvas displays a transparent image instead of an error is the intended behaviour to prevent cross-origin access, does not seem logical and contradicts case 1.

I also attach screenshots.

### aa...@chromium.org (2019-02-12)

[Comment Deleted]

### aa...@chromium.org (2019-02-12)

Yeah, I was only pointing out that the image is not only transparent, it's also totally black, so data is not being leaked. There's still definitely a bug, but things aren't as urgent as we may have imagined.

### aa...@gmail.com (2019-02-12)

Of course, it's up to you (the security team) to decide on the urgency. But it IS a *security* issue, which should be eligible for a bounty. And should be fixed before fixing https://crbug.com/chromium/838108 (transparent image from bitmap transform).

I'm keen to look through the code and provide a patch when I have more time, if a patch has not been issued by then.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/02c469f444a7e6a69e82d4301a0272435ce6be1a

commit 02c469f444a7e6a69e82d4301a0272435ce6be1a
Author: Aaron Krajeski <aaronhk@google.com>
Date: Mon Feb 25 17:50:42 2019

CORS errors are broken for ImageBitmapRenderingContext

ImageBitmapRenderingContext.toDataURL() does not throw CORS errors
when reading from a tainted canvas. It is not super urgent right now
as the entire functionality is broken, it simply returns black pixels,
so there is no security vulnerability RIGHT now. Regardless
once https://bugs.chromium.org/p/chromium/issues/detail?id=838108 is
fixed, it will expose a problem.

Currently toDataURL() in dev builds fails https://cs.chromium.org/chromium/src/third_party/blink/renderer/platform/graphics/unaccelerated_static_bitmap_image.cc?q=unaccelerated_static_bitmap_image&sq=package:chromium&dr=C&l=28
and on https://cs.chromium.org/chromium/src/cc/paint/paint_image_builder.cc?dr=C&q=paint_image_builder&sq=package:chromium&g=0&l=47
not sure when this was introduced, but as of now we have no tests for
toDataURL().

toDataURL() with LOCAL images also appears to be broken for
ImageBitmapRenderingContext, as it just returns empty images.

Will add tests and try to fix those problems in other CLs

Bug: 930057
Change-Id: Id22d22310ae2130472f1a3cbc104cfe632a7129c
Reviewed-on: https://chromium-review.googlesource.com/c/1474546
Reviewed-by: Fernando Serboncini <fserb@chromium.org>
Commit-Queue: Aaron Krajeski <aaronhk@chromium.org>
Cr-Commit-Position: refs/heads/master@{#635149}
[modify] https://crrev.com/02c469f444a7e6a69e82d4301a0272435ce6be1a/third_party/blink/renderer/modules/canvas/imagebitmap/image_bitmap_rendering_context.cc


### sh...@chromium.org (2019-02-27)

aaronhk: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aa...@chromium.org (2019-02-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-28)

[Empty comment from Monorail migration]

### aa...@gmail.com (2019-03-03)

Indeed, it would have exposed an issue. Commit 02c469f444a7e6a69e82d4301a0272435ce6be1a fixed it. The latest version, as of Thu Feb 28 20:11:04 2019 +0000, does not export the cross-origin image (current_93083a26ba0a1f79049b91af7aeced1afe0d91b8.png). I manually reverted commit 02c469f444a7e6a69e82d4301a0272435ce6be1a and recompiled. The cross-origin image is now exported and rendered correctly (since https://crbug.com/chromium/838108 was fixed subsequently), in violation of the same-origin policy (revert_02c469f444a7e6a69e82d4301a0272435ce6be1a.png).

Would this bug be eligible for a bounty?

### na...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-03-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-07)

Congrats! The Panel decided to reward $1,000 for this report! 

A member from finance will be in touch shortly :) 

### aw...@google.com (2019-03-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-03-26)

This landed well before M74 branch point so no need to do special merges into M74.

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/930057?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Blink>SecurityFeature>CORS]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093996)*
