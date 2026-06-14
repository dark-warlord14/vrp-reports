# pdfium: stack-buffer-overflow in IntersectSides

| Field | Value |
|-------|-------|
| **Issue ID** | [40091180](https://issues.chromium.org/issues/40091180) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF, Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2018-04-22 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.70 Safari/537.36

Steps to reproduce the problem:
I'm not sure what to do with this report. This is in code that's not shipped in Chromium today. I don't know if custom pdfium implementations use it. You have to build pdfium with pdf_use_skia_paths enabled. I only do so because that code tends to be faster than agg. And you get bonus skia paths coverage.

From what I've gathered, the intention is still to ship this in Chromium, so it could be enabled tomorrow. It already was, only to be reverted.

https://chromium.googlesource.com/chromium/src/+/1545ba94087279c773705760d51b728d709fd72d

Anyway, here is the ASAN report.

==15308==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fa784e1fa48 at pc 0x000000d2c576 bp 0x7ffe76f73180 sp 0x7ffe76f73178
READ of size 4 at 0x7fa784e1fa48 thread T0
    #0 0xd2c575 in operator-(SkPoint const&, SkPoint const&) third_party/skia/include/core/SkPoint.h:494:26
    #1 0xd2c840 in (anonymous namespace)::IntersectSides(SkPoint const&, SkPoint const&, SkPoint const&) core/fxge/skia/fx_skia_device.cpp:463:29
    #2 0xd2330c in (anonymous namespace)::ClipAngledGradient(SkPoint const*, SkPoint*, bool, bool, SkPath*) core/fxge/skia/fx_skia_device.cpp:537:16
    #3 0xd20799 in CFX_SkiaDeviceDriver::DrawShading(CPDF_ShadingPattern const*, CFX_Matrix const*, FX_RECT const&, int, bool) core/fxge/skia/fx_skia_device.cpp:2075:9
    #4 0xb69f81 in CPDF_RenderStatus::DrawShading(CPDF_ShadingPattern const*, CFX_Matrix*, FX_RECT const&, int, bool) core/fpdfapi/render/cpdf_renderstatus.cpp:2091:37
    #5 0xb60110 in CPDF_RenderStatus::ProcessShading(CPDF_ShadingObject const*, CFX_Matrix const*) core/fpdfapi/render/cpdf_renderstatus.cpp:2193:3
    #6 0xb5a642 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const*, PauseIndicatorIface*) core/fpdfapi/render/cpdf_renderstatus.cpp:1173:5
    #7 0xb59048 in CPDF_ProgressiveRenderer::Continue(PauseIndicatorIface*) core/fpdfapi/render/cpdf_progressiverenderer.cpp:93:30
    #8 0x93c199 in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IPDFSDK_PauseAdapter*) fpdfsdk/fpdf_view.cpp:124:26
    #9 0x92ff7e in FPDF_RenderPage_Retail(CPDF_PageRenderContext*, void*, int, int, int, int, int, int, bool, IPDFSDK_PauseAdapter*) fpdfsdk/fpdf_view.cpp:905:3
    #10 0x93ae45 in FPDF_RenderPageBitmap fpdfsdk/fpdf_view.cpp:631:3

Address 0x7fa784e1fa48 is located in stack of thread T0 at offset 584 in frame
    #0 0xd1f3df in CFX_SkiaDeviceDriver::DrawShading(CPDF_ShadingPattern const*, CFX_Matrix const*, FX_RECT const&, int, bool) core/fxge/skia/fx_skia_device.cpp:1982

  This frame has 24 object(s):
    [32, 40) 'ref.tmp' (line 1999)
    [64, 80) 'skColors' (line 2004)
    [96, 112) 'skPos' (line 2005)
    [128, 132) 'ref.tmp49' (line 2020)
    [144, 148) 'ref.tmp50' (line 2021)
    [160, 168) 'ref.tmp73' (line 2029)
    [192, 193) 'clipStart' (line 2030)
    [208, 209) 'clipEnd' (line 2031)
    [224, 312) 'paint' (line 2032)
    [352, 392) 'skMatrix' (line 2035)
    [432, 448) 'skRect' (line 2036)
    [464, 480) 'skClip' (line 2038)
    [496, 512) 'skPath' (line 2039)
    [528, 544) 'pts' (line 2045)
    [560, 568) 'agg.tmp'
    [592, 624) 'rectPts' (line 2071) <== Memory access at offset 584 underflows this variable
    [656, 672) 'pts209' (line 2087)
    [688, 696) 'agg.tmp216'
    [720, 760) 'inverse' (line 2101)
    [800, 952) 'stream' (line 2111)
    [1024, 1120) 'cubics' (line 2115)
    [1152, 1168) 'colors' (line 2116)
    [1184, 1216) 'tempCubics' (line 2126)
    [1248, 1256) 'point' (line 2136)

What is the expected behavior?

What went wrong?
^

Did this work before? No 

Chrome version: 66.0.3359.70  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-835667.pdf](attachments/chromium-835667.pdf) (application/pdf, 268 B)

## Timeline

### pd...@gmail.com (2018-04-22)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-04-22)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF Internals>Skia]

### va...@chromium.org (2018-04-22)

I'm unable to reproduce it with the standard ASAN builds since it requires building with pdf_use_skia_paths enabled.

### va...@chromium.org (2018-04-22)

[Empty comment from Monorail migration]

### pd...@gmail.com (2018-04-22)

You can reproduce it with an ASAN build from the week this was enabled by default. I reproduced it with asan-linux-release-482029.zip from below.

https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=linux-release/

### pd...@gmail.com (2018-04-22)

(The above stack is from current pdfium, not from the Chromium build.)

### ds...@chromium.org (2018-04-23)

We currently have no plans to ship the Skia Paths code. There are known security issues and I believe some performance issues which need to be addressed.

### in...@chromium.org (2018-08-24)

[Empty comment from Monorail migration]

### ds...@chromium.org (2018-09-04)

Setting PDF bugs assigned to me back to untriaged so they can get re-assigned as needed.

### hn...@chromium.org (2018-09-05)

Lowering priority as this only affects Skia.

### th...@chromium.org (2018-09-11)

Will take a look. We definitely appreciate your interest with pdf_use_skia_paths and this bug report.

### th...@chromium.org (2018-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-12)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/987416db22712d0b5c666be08a148946ce4b9bdb

commit 987416db22712d0b5c666be08a148946ce4b9bdb
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Sep 12 17:21:11 2018

Avoid out of bound access in ClipAngledGradient().

BUG=chromium:835667

Change-Id: I3b9fd04d26f1baa30d48f938616b187410134b5f
Reviewed-on: https://pdfium-review.googlesource.com/42311
Reviewed-by: Cary Clark <caryclark@google.com>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/987416db22712d0b5c666be08a148946ce4b9bdb/core/fxge/skia/fx_skia_device.cpp


### th...@chromium.org (2018-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/410476c8c458115643d1b9f1302521004bfc5b3b

commit 410476c8c458115643d1b9f1302521004bfc5b3b
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Wed Sep 12 19:57:16 2018

Roll src/third_party/pdfium b4c1b016c9d3..987416db2271 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/b4c1b016c9d3..987416db2271


git log b4c1b016c9d3..987416db2271 --date=short --no-merges --format='%ad %ae %s'
2018-09-12 thestig@chromium.org Avoid out of bound access in ClipAngledGradient().


Created with:
  gclient setdep -r src/third_party/pdfium@987416db2271

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:835667
TBR=dsinclair@chromium.org

Change-Id: I4c76309c519bc31801abc08d86efd3e2152b3b88
Reviewed-on: https://chromium-review.googlesource.com/1222208
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#590797}
[modify] https://crrev.com/410476c8c458115643d1b9f1302521004bfc5b3b/DEPS


### sh...@chromium.org (2018-09-13)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

Thanks for the report, pdknsk@. The Chrome VRP panel decided to award $500 for this, noting that this code path is very unlikely to ship to users.

### aw...@google.com (2018-11-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-12-20)

This issue was migrated from crbug.com/chromium/835667?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, Internals>Skia]
[Monorail blocking: crbug.com/pdfium/11]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091180)*
