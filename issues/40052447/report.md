# Security: drawImage timing depends on alpha-channel value, allowing to read cross-origin images

| Field | Value |
|-------|-------|
| **Issue ID** | [40052447](https://issues.chromium.org/issues/40052447) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Canvas, Internals>GPU, Internals>Skia |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@popovs.lv |
| **Assignee** | mt...@google.com |
| **Created** | 2020-05-30 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The function CanvasRenderingContext2D.drawImage takes a different amount of time to draw pixels depending on their alpha value: fully opaque pixels (A=255) are drawn about an order of magnitude faster than fully transparent ones (A=0), and fully transparent ones are about an order of magnitude faster than partially transparent ones (1<=A<=255). Because drawImage can crop and resize images, given a cross-origin image img, we can do drawImage(img, x, y, 1, 1, 0, 0, 1024, 1024) many times in a loop to draw 1024^2 copies of the pixel at (x, y) in img, making it possible to observe the timing difference.

This timing difference can be very reliably observed when hardware canvas acceleration is disabled (flag #disable-accelerated-2d-canvas on chrome://flags). With acceleration enabled, I've had some intermittent luck observing the same effects with a higher iteration count, but calling drawImage in a loop would also cause my whole system to slow down, and eventually the GPU process would crash and Chrome would fall back to software rendering, so it seems that crashing the GPU might sometimes be a viable way of exploiting this in the default configuration.

**VERSION**  

Chrome Version: Chromium 83.0.4103.61 (Official Build) Arch Linux (64-bit)  

Operating System: Linux 5.6.14-arch1-1 x86\_64, using X11  

CPU: Intel(R) Core(TM) i3-6100U CPU @ 2.30GHz  

GPU: VENDOR= 0x8086 [Intel], DEVICE=0x1916 [Mesa Intel(R) HD Graphics 520 (SKL GT2)] \*ACTIVE\*

**REPRODUCTION CASE**  

I am attaching two PoCs:

- benchmark.html measures the performance of running drawImage 1000 times with differently-colored 1x1 images, and outputs a CSV report. benchmark\_nogpu.png is a plot of the results obtained when running with acceleration disabled, clearly showing the three different performance levels.
- exploit.html uses this timing side channel to reconstruct a 5x5 cross-origin image. Notice that opening it will make a request to a remote server. I'm also attaching target\_xsmall.png, the image on the remote server.

**CREDIT INFORMATION**  

Reporter credit: Aleksejs Popovs

As a heads up, I have also reported a similar bug in Firefox.

## Attachments

- [benchmark.html](attachments/benchmark.html) (text/plain, 3.8 KB)
- [exploit.html](attachments/exploit.html) (text/plain, 2.4 KB)
- [target_xsmall.png](attachments/target_xsmall.png) (image/png, 593 B)
- [benchmark_nogpu.png](attachments/benchmark_nogpu.png) (image/png, 43.4 KB)

## Timeline

### dr...@chromium.org (2020-06-01)

Marking as low severity since it can only read alpha channel, and triaging to Blink>Paint OWNERs (feel free to re-assign if I've guessed the wrong component)

[Monorail components: Blink>Paint]

### en...@chromium.org (2020-06-01)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Paint Blink>Canvas]

### fs...@chromium.org (2020-06-01)

Moving to the triage queue.

### [Deleted User] (2020-06-01)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fs...@chromium.org (2020-06-09)

I'm adding some components here, because as much as I recognize the issue here, I have no idea what to do about it.

[Monorail components: Internals>GPU Internals>Skia]

### fs...@chromium.org (2020-06-09)

[Empty comment from Monorail migration]

### fs...@chromium.org (2020-06-30)

[Empty comment from Monorail migration]

### re...@google.com (2020-06-30)

[Empty comment from Monorail migration]

### mt...@google.com (2020-06-30)

Probably all the short-circuiting optimizations in blit_row_s32a_opaque()?

### al...@popovs.lv (2020-07-02)

I think that those optimizations are part of the story here, but not all of it. Reading blit_row_s32a_opaque, you'd expect that drawing fully transparent pixels should be fastest (that's the first short-circuiting condition in the function, and the only one that doesn't require doing anything at all), but in the benchmark I posted it's the fully opaque pixels that are fastest.

I thought about why drawing solid pixels could ever be faster than drawing transparent ones (≈ doing nothing) and imagined there might be an optimization somewhere higher up in the stack for the case “we are drawing a fully solid image *that also covers the whole destination*”, and does this even faster with a single memcpy/pointer swap/whatever.

The original benchmark scaled the source pixel up to 1024×1024 and drew it onto a 1024×1024 canvas, so it would hit that hypothetical optimization. I changed it to instead scale it up to 1024×1024 but draw into the middle of a 2048×2048 canvas, and now I was indeed getting results that are consistent with the optimizations in blit_row_s32a_opaque:

Alpha | Time to draw onto 1024 canvas | Time to draw onto 2048 canvas
000 |  65 |  65
128 | 392 | 478
255 |   9 | 302

With the bigger canvas, fully solid pixels are drawn way slower, and now fully transparent ones are indeed the fastest, so I think my hypothesis about this extra optimization contributing to this side channel sounds plausible. Does this sound right?

### mt...@google.com (2020-07-06)

Yep, sounds pretty plausible.

### al...@popovs.lv (2020-07-20)

I think I found the optimization I was talking about: the macro DRAW_BEGIN_CHECK_COMPLETE_OVERWRITE (used in SkCanvas::onDrawImageRect) passes the flag auxOpaque (which says whether the image drawn is fully opaque) into SkCanvas::predrawNotify, which uses it to determine whether to discard the surface.

So it looks like at least this and the short-circuiting in blit_row_s32a_opaque would have to be disabled somehow when drawing cross-origin images or tainted canvases.

Do you have any updates about bounty eligibility, by any chance?

### ts...@chromium.org (2020-08-25)

mtklein - looks like you've optimized this code in the past, perhaps you could take a look and/or re-assign as appropriate?  Thanks.

### mt...@google.com (2020-08-27)

I've been able to reproduce this locally, and then stifle my local repro by removing the branching on source image data in the few-pixel scalar part of blit_row_s32a_opaque():

diff --git a/src/opts/SkBlitRow_opts.h b/src/opts/SkBlitRow_opts.h
index 1e64498abe..b7a72e9214 100644
--- a/src/opts/SkBlitRow_opts.h
+++ b/src/opts/SkBlitRow_opts.h
@@ -441,13 +441,7 @@ void blit_row_s32a_opaque(SkPMColor* dst, const SkPMColor* src, int len, U8CPU a
 #endif

     while (len-- > 0) {
-        // This 0xFF000000 is not semantically necessary, but for compatibility
-        // with chromium:611002 we need to keep it until we figure out where
-        // the non-premultiplied src values (like 0x00FFFFFF) are coming from.
-        // TODO(mtklein): sort this out and assert *src is premul here.
-        if (*src & 0xFF000000) {
-            *dst = (*src >= 0xFF000000) ? *src : SkPMSrcOver(*src, *dst);
-        }
+        *dst = SkPMSrcOver(*src, *dst);
         src++;
         dst++;
     }

That's not the only branching based on source data in this code, just an exemplar.  The other branching is on larger chunks of pixels (8,16,32, or 64 at a time) that I imagine would be harder to time.  But blit_row_s32a_opaque() kind of exists exactly for this leaky transparent/opaque/general-case branching, so it might be the deeper fix for this would effectively be to delete the whole function.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-28)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/5c612ade3b8d913242e07ef16fea5cc7e8fb8823

commit 5c612ade3b8d913242e07ef16fea5cc7e8fb8823
Author: Mike Klein <mtklein@google.com>
Date: Fri Aug 28 16:17:39 2020

create a sample to demonstrate a timing attack

This sample attempts to re-create an image's alpha channel by drawing it
one pixel at a time and timing how long each pixel takes to draw.

The "abc" text should appear twice normally, and the third and fourth
versions are reconstructed from timing, one by timing 1:1 pixel draws,
the other by timing 1x1:1024x1024 upscale into an offscreen.  It's not
meant to be an exact reconstruction, but you can easily see the shapes,
particularly at -O0, -O1, and -Os.  Auto-vectorization from -O2/-O3 do
a good amount to cover up the problem.

The legacy CPU backend is the main place to look.  I haven't been able
to reconstruct any images using SkRasterPipelineBlitter or SkVMBlitter,
and while on the GPU I do see non-random patterns in the timing, it
appears to be the same single pattern across devices, OSes, GPUs, GPU
APIs and content... I assume it's something like our resource caching
policy.

This can't really be a GM, given how it draws non-deterministically.

Bug: chromium:1088224
Change-Id: I2ec79c8dd407ecb104fd9bf0c8039cb6dd1fe436
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/313466
Commit-Queue: Mike Klein <mtklein@google.com>
Commit-Queue: Mike Reed <reed@google.com>
Reviewed-by: Mike Reed <reed@google.com>

[add] https://crrev.com/5c612ade3b8d913242e07ef16fea5cc7e8fb8823/samplecode/SampleTiming.cpp
[modify] https://crrev.com/5c612ade3b8d913242e07ef16fea5cc7e8fb8823/gn/samples.gni


### mt...@google.com (2020-08-28)

So far as I can tell, this does all come down to blit_row_s32a_opaque().

The auxOpaque-related idea in https://crbug.com/chromium/1088224#c12 did look promising to me, but as far as I can tell, image subsets inherit alpha type from their parent, and we don't peek at 1x1 images to see if they're actually opaque.  This is a complicated area with a lot of interactions, so it's certainly possible I've overlooked something; I just don't think it's that at the moment.  I was able to reconstruct a source image by timing two ways, one of which I think mimics the repro case here, and both are fixed by removing pixel-based branching from blit_row_s32a_opaque().  (Not yet landed.)

### al...@popovs.lv (2020-08-28)

I'm pretty sure you're right about https://crbug.com/chromium/1088224#c12! I couldn't find where in the code the inheritance happens, but I ran some further experiments and empirically found that cropping an opaque pixel out of an image that also has non-opaque ones doesn't seem to trigger that optimization. Sorry I forgot to report back about this.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9d302ba8d05f3ee2a93717f14337babc30ce373b

commit 9d302ba8d05f3ee2a93717f14337babc30ce373b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Aug 28 21:13:52 2020

Roll Skia from fc1eb95f39a3 to 1e87a9ab4a13 (5 revisions)

https://skia.googlesource.com/skia.git/+log/fc1eb95f39a3..1e87a9ab4a13

2020-08-28 mtklein@google.com second guess swizzler avx-512 opts
2020-08-28 reed@google.com Only expose isConvex on path publicly.
2020-08-28 johnstiles@google.com Remove fProgram member from ProgramVisitor.
2020-08-28 mtklein@google.com create a sample to demonstrate a timing attack
2020-08-28 johnstiles@google.com Add helper function for making temp variables in inlineCall.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC mtklein@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Cq-Do-Not-Cancel-Tryjobs: true
Bug: chromium:1088224
Tbr: mtklein@google.com
Change-Id: I8ab94e27350db84183dd65880d88837598f7487f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2381945
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#802791}

[modify] https://crrev.com/9d302ba8d05f3ee2a93717f14337babc30ce373b/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-29)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/5d3314c53ce5c966591f0b02349103f51f986e6e

commit 5d3314c53ce5c966591f0b02349103f51f986e6e
Author: Mike Klein <mtklein@google.com>
Date: Sat Aug 29 13:04:30 2020

overhaul blit_row_s32a_opaque()

  - Remove branching on source alpha, which
    makes Skia susceptible to timing attacks.

  - Remove SSE4.1 variant, which is nearly identical
    to the SSE2 code once branching's removed.

  - Reroll SIMD loops back to their native vector
    size, leaving unrolling to the compiler.

  - Allow wider SIMD sets to cascade down into the
    narrower ones for the last few pixels instead of
    always hitting the scalar fallback.

  - Move code around, rewrite, refactor, etc. so it
    all reads more consistently.

  blit_row_color32() has not changed at all here,
  just moved to the bottom of the file to prevent
  it from interrupting blit_row_s32a_opaque().

  This prevents me from seeing the timing reconstructions
  on the Timing sample everywhere I've tested.

Charts to watch (ARMv7, ARMv8 AVX2, AVX512 geometric mean of SKP rendering):

    https://perf.skia.org/e/?formulas=geo(filter(%22config%3D8888%26cpu_or_gpu_value%3DAVX2%26extra_config%3D!Fast%26extra_config%3D!SK_FORCE_RASTER_PIPELINE_BLITTER%26source_type%3Dskp%26sub_result%3Dmin_ms%22))&formulas=geo(filter(%22config%3D8888%26cpu_or_gpu_value%3DAVX512%26source_type%3Dskp%26sub_result%3Dmin_ms%22))&formulas=geo(filter(%22arch%3Darm64%26config%3D8888%26source_type%3Dskp%26sub_result%3Dmin_ms%22))&formulas=geo(filter(%22arch%3Darm%26config%3D8888%26source_type%3Dskp%26sub_result%3Dmin_ms%22))

Bug: chromium:1088224
Change-Id: I4baf2ccd58ac3129ef01c2cf79c3826c9c0d389e
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/313716
Commit-Queue: Mike Klein <mtklein@google.com>
Reviewed-by: Mike Reed <reed@google.com>
Reviewed-by: Herb Derby <herb@google.com>

[modify] https://crrev.com/5d3314c53ce5c966591f0b02349103f51f986e6e/src/opts/SkBlitRow_opts.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c000744b0540f5a5617f8c986fac70d026e03008

commit c000744b0540f5a5617f8c986fac70d026e03008
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Aug 29 14:53:28 2020

Roll Skia from 6fd391a016f3 to 5d3314c53ce5 (1 revision)

https://skia.googlesource.com/skia.git/+log/6fd391a016f3..5d3314c53ce5

2020-08-29 mtklein@google.com overhaul blit_row_s32a_opaque()

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC mtklein@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Cq-Do-Not-Cancel-Tryjobs: true
Bug: chromium:1088224
Tbr: mtklein@google.com
Change-Id: Icc5df01f2d6679dccab7cd3a44b81258db3f4e77
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2383611
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#802908}

[modify] https://crrev.com/c000744b0540f5a5617f8c986fac70d026e03008/DEPS


### al...@popovs.lv (2020-08-29)

Looks like this worked. I tried a build of revision 4788efad44d0e759d1ff6f038104781f1bc91d48 and the exploit attached to this issue no longer works, plus the benchmark doesn't seem to show any useful difference in performance.

### mt...@google.com (2020-08-29)

Good!  That matches my local testing, which has so far shown no macro-level performance change.

### al...@popovs.lv (2020-08-29)

Can I share a link to the Skia patch with the Firefox folks?

Also, any updates on whether this is eligible for the bounty and/or when you'd be okay with disclosing this?

### mt...@google.com (2020-08-29)

Sure, yeah, https://chromium.googlesource.com/skia/+/5d3314c53ce5c966591f0b02349103f51f986e6e is publicly visible.  Feel free to share it with Firefox.

(I'm not part of deciding any of the rest.  I guess I'll mark this as Fixed and see what happens.)

### [Deleted User] (2020-08-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-31)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-31)

aleksejs@popovs.lv thanks for the report. This will go to the VRP panel this week who will decide on bounties. We'll likely allocate a CVE when this is released, which at the moment looks like it will be Chrome 87 in November. As for disclosure, we normally open things up to the public 14 weeks after the fix date, in order to give plenty of time for the fix to roll out to nearly 100% of users. If you have a pressing need to disclose earlier please let us know.

Meanwhile - please feel free to cc the relevant Firefox folk on this bug (or if you don't have permission to do that, let me know who and I can do so). That way they'll be able to see all this discussion prior to public disclosure, and that's fine.

### al...@popovs.lv (2020-08-31)

Thank you!

It looks like I don't have permission to cc, could you add lsalzman@mozilla.com?

### ad...@chromium.org (2020-08-31)

Done!

### ad...@google.com (2020-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-09)

Congratulations! The VRP panel has decided to award $5,000 for this bug. It's an interesting one! Someone from our finance team will get in touch with you.

### al...@popovs.lv (2020-09-10)

Woah awesome, thank you!

### ad...@google.com (2020-09-10)

[Empty comment from Monorail migration]

### mt...@google.com (2020-09-11)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### is...@google.com (2021-01-07)

This issue was migrated from crbug.com/chromium/1088224?no_tracker_redirect=1

[Multiple monorail components: Blink>Canvas, Internals>GPU, Internals>Skia]
[Monorail mergedwith: crbug.com/chromium/1123393]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052447)*
