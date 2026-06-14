# A GPU crash (or anything that causes loss of GPU support for Chrome) will create framebuffer ghosting with ImageBitmap

| Field | Value |
|-------|-------|
| **Issue ID** | [40058375](https://issues.chromium.org/issues/40058375) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Canvas, Blink>WebGPU |
| **Platforms** | Windows |
| **Reporter** | jo...@gmail.com |
| **Assignee** | ju...@chromium.org |
| **Created** | 2021-12-30 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version : 96.0.4664.110 (Official Build) (64-bit) (cohort: Stable)  

**URLs (if applicable) :** <https://www.planetminecraft.com> - currently reproduceable in our dynamic header (the top ~120 pixels at the top that show a rotating planet, if your browser has WebGL support). On Chrome, this currently uses a SharedWorker, and that SharedWorker creates a WebGL context which passes back ImageBitmaps to the main thread.  

**Other browsers tested:**  

Add OK or FAIL, along with the version, after other browsers where you  

**have tested this issue:**  

Safari: ???  

Firefox: ???  

Edge: ???

**What steps will reproduce the problem?**  

**(1)** Load a page that uses a WebGL context + ImageBitmap transfer to render an image to a canvas. This may also require a SharedWorker/Worker backing, but I have not tested that this is required yet.  

**(2)** Forcefully kill your GPU drivers (either by forcing a crash, or for instance updating your GPU drivers; only tested with an nVidia RTX 3090). This will force Chrome to fall back to software rendering.  

**(3)** Observe that the ImageBitmap's show a seemingly random portion of GPU memory. This will leak data into the canvas from other processes, tabs, etc. For instance, switching tabs will show this: <https://i.imgur.com/VIgPun9.png>

**What is the expected result?**  

Graceful fallback to software rendering

**What happens instead?**  

ImageBitmap still appears to be referring to a portion of GPU memory, causing framebuffer leaks.

Note that the WebGL canvas itself shows the correct data if you pull the data out of it via getImageData or converting the canvas to a blob and then that blob to a data URI. This issue only affects the bitmap output from `transferToImageBitmap`, which appears to contain raw GPU memory.

## Attachments

- [1283434.mp4](attachments/1283434.mp4) (video/mp4, 1.8 MB)
- [1283434-M97.mp4](attachments/1283434-M97.mp4) (video/mp4, 2.0 MB)
- [GPU.txt](attachments/GPU.txt) (text/plain, 23.3 KB)
- [index.html](attachments/index.html) (text/plain, 150 B)
- [main.js](attachments/main.js) (text/plain, 343 B)
- [worker.js](attachments/worker.js) (text/plain, 464 B)

## Timeline

### jo...@gmail.com (2021-12-30)

Note also that this issue did not affect Chrome until a version or two ago. I don't have the exact data on when this issue began happening. Some users experience this issue with no additional steps required; killing GPU drivers was the only way I could reproduce it locally. Perhaps this issue relates to a specific GPU function that ImageBitmap relies on being disabled or broken during Software rendering?

Here's my about:gpu *after* a forced driver crash, in order to reproduce the bug:

Graphics Feature Status
Canvas: Software only, hardware acceleration unavailable
Canvas out-of-process rasterization: Disabled
Compositing: Software only. Hardware acceleration disabled
Multiple Raster Threads: Enabled
Out-of-process Rasterization: Disabled
OpenGL: Disabled
Rasterization: Software only. Hardware acceleration disabled
Raw Draw: Disabled
Skia Renderer: Enabled
Video Decode: Software only. Hardware acceleration disabled
Vulkan: Disabled
WebGL: Software only, hardware acceleration unavailable
WebGL2: Software only, hardware acceleration unavailable
Problems Detected
Gpu compositing has been disabled, either via blocklist, about:flags or the command line. The browser will fall back to software compositing and hardware acceleration will be unavailable.
Disabled Features: gpu_compositing

Graphics Feature Status for Hardware GPU
Canvas: Hardware accelerated
Canvas out-of-process rasterization: Enabled
Compositing: Hardware accelerated
Multiple Raster Threads: Enabled
Out-of-process Rasterization: Hardware accelerated
OpenGL: Enabled
Rasterization: Hardware accelerated
Raw Draw: Disabled
Skia Renderer: Enabled
Video Decode: Hardware accelerated
Vulkan: Disabled
WebGL: Hardware accelerated
WebGL2: Hardware accelerated

### jo...@gmail.com (2021-12-30)

As an addendum, this issue only seems to show up if you render the final canvas over a `bitmaprenderer`. It may be that the BitmapRenderer context is doing something weird, and that the ImageBitmap itself is fine.

### ve...@chromium.org (2021-12-31)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-12-31)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGPU]

### va...@chromium.org (2022-01-03)

Tried the issue on reported chrome version  #96.0.4664.110 using Win 10 as per https://crbug.com/chromium/1283434#c0.
Steps
=====
1. Open testURL "https://www.planetminecraft.com/"
2. Open the Task Manager and kill the GPU process.

Observed Image Bitmap of the Dynamic header in the site appears without any glitches and Observed the same on Latest M97 #97.0.4692.71.

Attached GPU details and Screencast for reference

Reporter@ Could you please review the attached screencast and let us know if anything being missed here.

### jo...@gmail.com (2022-01-03)

@vamsipriyan@chromium.org - I had to patch the issue on our site on Jan 1st as it was causing some concern with people seeing various non-site-data appearing inside of our website. Since we're pretty high traffic I didn't want to leave the bug up for too long.

I will attempt to write a minimal repro of the bug this morning and get back to you.

### [Deleted User] (2022-01-03)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@gmail.com (2022-01-03)

Okay, so I was able to reproduce the software fallbacks not working properly; this only seems to be a problem when you are relying on ImageBitmap's transferred to a BitmapRenderer. The end result is that after hardware acceleration is disabled, the main JS no longer receives valid data from the ImageBitmap. On my end, it only appears white, but as I was able to repro with our old Active Header code, it can show other raw GPU data if certain conditions are correct... I don't know what those conditions are yet, though. The main transfer->receive loop is identical to what I have on our Active Header.

I'm going to upload a version of our Active Header that can "enable" the bug via the Query URI so you can reproduce the originally-reported bug without us exposing regular users. Until then, though, here's the files required to reproduce the less-dangerous bug.

Note that because it's a (Shared)Worker, these will need to be run on a proper web server (nginx/apache/node server) since workers don't run properly if you just open the index.html in the browser.

### jo...@gmail.com (2022-01-03)

Okay, I had a chance to allow the bug to be repro' on our main site again. Please use this URL: https://www.planetminecraft.com/#chromeBug
This will allow the SharedWorker bitmapped backend to be used.

Here's a video link which shows the behavior with GPU acceleration, then me disabling hardware accel and showing the canvas now leaking data from the GPU. I stopped it too early, but, if I perform anything GPU-oriented on my PC it may leak that data into the canvas.

https://streamable.com/o591th

### pu...@chromium.org (2022-01-04)

Able to reproduce the issue on chrome version #96.0.4664.110 using Windows 10 as per https://crbug.com/chromium/1283434#c0 and https://crbug.com/chromium/1283434#c9
Note: Not able see any canvas data leaking from the GPU in Mac 12.0.1

Reproducible on
==============
99.0.4806.0 - Canary
98.0.4758.9 - Dev 
97.0.4692.71 - Beta  
96.0.4664.110  - Stable

Bisect Information:
----------------------------
Good Build: 95.0.4637.2
Bad Build: 95.0.4638.0

Bisect Script: python bisect-builds.py -a win64 -g 95.0.4637.2 -b 95.0.4638.0 --use-local-cache
Change log: https://chromium.googlesource.com/chromium/src/+log/b8fdc1366570017be8e6dfa58f70d99569362a2a..fdcb0119fb753b386ef9d868e8f00f9ab814f59c
Suspect CL : https://chromium.googlesource.com/chromium/src/+/1f31e17abe6fa73c7b9fef908efa4f88d83152c1

Justin Novosad@ Please help us in re-assigning if this is not related to your change.

Thanks..!!

### ju...@chromium.org (2022-01-12)

I am classifying this as a security bug since it could potentially be exploited to exfiltrate private data.

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### ju...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### ju...@chromium.org (2022-01-12)

@#8: With this example, I see a blank canvas after triggering a gpu crash (by navigating to chrome://gpucrash in another window).  This is the correct behavior in that case because the WebGL context is not being restored in the worker, i.e. it is not handling context loss events.  Therefore, it is normal for the worker to be emitting blank ImageBitmaps at that point.

I think the sample code attached to https://crbug.com/chromium/1283434#c8 does not reproduce the bug.

### ju...@chromium.org (2022-01-12)

Okay, I was able to make some progress. I created a 2d canvas next to the bitmap renderer canvas and on the main thread, I  do a drawImage to the 2d canvas and then transfer to the bitmap renderer.  This makes it clear that there are situations where the the ImageBitmap is valid because it can be drawn to the 2D canvas, but the bitmap renderer displays a blank frame.  This is definitely fishy. After three consecutive GPU crashes, Chrome disables many GPU features permanently (the three strikes rule).  At that point, the bitmap renderer continues to show a blank frame even after a page reload.  That's really weird.

I don't think the suspected CL is the right one. There are several graphics related-CLs in that range, so  I am going to do a finer grained bisect.

[Monorail components: Blink>Canvas]

### ju...@chromium.org (2022-01-12)

Also, I am noticing a lot of these error in the stderr output:

[201004:201004:0112/143403.719959:ERROR:gl_utils.cc(314)] [.RendererMainThread-0x71e00cbea00] GL_INVALID_OPERATION: invalid mailbox name.
[201004:201004:0112/143403.720075:ERROR:gl_utils.cc(314)] [.RendererMainThread-0x71e00cbea00] GL_INVALID_OPERATION: texture is not a shared image


### ju...@chromium.org (2022-01-13)

What I have found is that the GPU crash does not only cause WebGL to fallback to the software, but also the compositor, and it is BitmapRenderingContext's interaction with the software compositor that was causing problems.  In some cases an unnecessary early exit condition is being triggered, causing the canvas to go blank, in other cases the pixel buffer format was not being handles correctly.  Using the wrong buffer format can lead to buffer overruns, which is probably what was causing the content leak that was observed by the reporter, but I was not able to come up with a repro case for that exact symptom, I suspect it might only happen with displays where swiftshader chooses to render at 16 bits per pixel. 

I am surprised this bug has not been caught before and that our existing tests did not detect it.  As far as I can tell this code path was never implemented correctly, though the exact manifestations of the bug may have varied over time.

Thanks a lot for finding and reporting this. jonno.5000

### jo...@gmail.com (2022-01-14)

No problem! Technically we have the users of PlanetMinecraft to thank, they first noticed this. For users that were stuck on software rendering, they would see this leakage all the time, and it was quite concerning to me when I realized it could copy over data from other tabs.

### gi...@appspot.gserviceaccount.com (2022-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eb967bf2110884ddde91aea6ba1696ae6b56f892

commit eb967bf2110884ddde91aea6ba1696ae6b56f892
Author: Justin Novosad <junov@chromium.org>
Date: Fri Jan 14 15:26:55 2022

Fix ImageBitmapRenderingContext interaction with software compositor.

Before this CL, there was an early exit condition that prevented
texture-backed resources from being presented to the software compositor
even when the texture backing is swiftshader. This meant that in some
cases, ImageBitmaps that were created by webGL contexts would fail to
render.  Once the early exit removed, there were other bugs due to the
fact that bitmaps were not being converted to N32 format before being
dispatched to the software compositor.  This could cause several types
of rendering artifacts, including leaking bitmap data between contexts.

BUG=1283434

Change-Id: I6f353bc6301b79d7a4124445c85956125135f539
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3387268
Reviewed-by: Juanmi Huertas <juanmihd@chromium.org>
Commit-Queue: Justin Novosad <junov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#959192}

[add] https://crrev.com/eb967bf2110884ddde91aea6ba1696ae6b56f892/third_party/blink/web_tests/fast/canvas/bug1283434-expected.html
[add] https://crrev.com/eb967bf2110884ddde91aea6ba1696ae6b56f892/third_party/blink/web_tests/fast/canvas/bug1283434.html
[modify] https://crrev.com/eb967bf2110884ddde91aea6ba1696ae6b56f892/third_party/blink/renderer/platform/graphics/gpu/image_layer_bridge.cc


### ju...@chromium.org (2022-01-14)

Here is my assessment regarding the data security and privacy impact of this issue.

The data leak happens in the compositor, not in blink. Therefore the leak probably cannot be exploited covertly.  AFAIK, the only Web API that reads composited output is the screen capture API (WebRTC), which cannot be engaged without user consent via the screen/tab/window sharing dialog.  Therefore, for a remote attacker to exploit this leak to exfiltrate cross-origin data, they would need to co-opt the user into sharing their screen via WebRTC.  Due to this bug, a user who screen shares only a specific tab could potentially leak data from an unshared browser tab to a remote attacker. Private data could also be accidentally leaked to peers (not necessarily attackers) when using the screen sharing functionality of a video conferencing app, which could be embarrassing to users. 

### ju...@chromium.org (2022-01-14)

@jonno.5000: I realize that you submitted this bug report using a standard bug templates (not the security template).  I converted this to a security bug a couple days ago by adding security flags to this issue.

There are a few thing you should know about security bugs:

Security bugs are not publicly visible.  However, as the reporter of this issue you continue to have access to it. We ask that you please keep information about this bug private until a fix has been widely deployed.  For example, please don't share the contents of this thread with your users.

For more information see: https://bughunters.google.com/

### jo...@gmail.com (2022-01-15)

Oh, thank you for the note. I wasn't sure at first how bad this bug really was, and I think the assessment above that it's not really abusable unless a very specific set of circumstances is met is accurate. I don't even think I was prompted with the ability to change to a security issue when I first posted this, but I don't recall the process I went through. Noted for the future though!

### ju...@chromium.org (2022-01-18)

@jonno.5000:  The fix is in the latest Canary release of Chrome.  Would you mind installing Chrome Canary to confirm that the bug is adequately fixed?
https://www.google.com/chrome/canary/

Thank you.

### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

Not requesting merge to dev (M99) because latest trunk commit (959192) appears to be prior to dev branch point (961656). If this is incorrect, please replace the Merge-NA-99 label with Merge-Request-99. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-11)

Hi Jonno! Thank you reporting this issue. As your bug report also allowed us to land a mitigation that would fix an issues for users, it also allowed for a mitigation of a potential for memory corruption. The VRP Panel would like to extend to you a $1,000 reward as a thank you for your report and your assistance as it led to a fix. A member of our finance team will reach out to you soon to arrange payment. In the meantime, please let us know the name/identifier you would like us to use to acknowledge you for this report. 

### am...@google.com (2022-02-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### jo...@gmail.com (2022-03-01)

amyressler@chromium.org Hey, sorry for the late reply - name for acknowledgement can just be Paril, that works for me. Thank you for the reward, I'm glad to have helped Chromium!

### am...@chromium.org (2022-03-01)

No worries at all. I've updated today's M99 release notes to reflect your acknowledgement as Paril as requested. [1]
Thanks again for your report and help in capturing this issue along the way. 

[1] https://chromereleases.googleblog.com/2022/03/stable-channel-update-for-desktop.html

### [Deleted User] (2022-04-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1283434?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Canvas, Blink>WebGPU]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058375)*
