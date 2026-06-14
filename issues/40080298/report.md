# Global-buffer-overflow in CFX_Font::LoadGlyphPath

| Field | Value |
|-------|-------|
| **Issue ID** | [40080298](https://issues.chromium.org/issues/40080298) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | at...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-08-26 |
| **Bounty** | $1,000.00 |

## Description


Tested on: 

Os: Ubuntu 12.04

Chromium: 39.0.2136.0 (Developer Build e6f6b730e646) 

ASAN-trace:

==419==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7fc0f5c824ed at pc 0x7fc0f4dd610c bp 0x7fffac1235b0 sp 0x7fffac1235a8
READ of size 1 at 0x7fc0f5c824ed thread T0 (chrome)
    #0 0x7fc0f4dd610b in CFX_Font::LoadGlyphPath(unsigned int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/ge/fx_ge_text.cpp:1662
    #1 0x7fc0f4dd213d in CFX_FaceCache::LoadGlyphPath(CFX_Font*, unsigned int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/ge/fx_ge_text.cpp:1522
    #2 0x7fc0f4dd13b4 in CFX_RenderDevice::DrawTextPath(int, FXTEXT_CHARPOS const*, CFX_Font*, CFX_FontCache*, float, CFX_Matrix const*, CFX_Matrix const*, CFX_GraphStateData const*, unsigned int, unsigned int, CFX_PathData*, int, int, void*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/ge/fx_ge_text.cpp:941
    #3 0x7fc0f4b23234 in CPDF_TextRenderer::DrawTextPath(CFX_RenderDevice*, int, unsigned int*, float*, CPDF_Font*, float, CFX_Matrix const*, CFX_Matrix const*, CFX_GraphStateData const*, unsigned int, unsigned int, CFX_PathData*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_text.cpp:600
    #4 0x7fc0f4b20745 in CPDF_RenderStatus::ProcessText(CPDF_TextObject const*, CFX_Matrix const*, CFX_PathData*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_text.cpp:296
    #5 0x7fc0f4aed511 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject const*, CFX_Matrix const*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render.cpp:420
    #6 0x7fc0f4aed923 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject const*, CFX_Matrix const*, IFX_Pause*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render.cpp:365
.
.
.


## Attachments

- [chrome-global-buffer-overflow-CFXFontLoadGlyphPath9.pdf](attachments/chrome-global-buffer-overflow-CFXFontLoadGlyphPath9.pdf) (application/pdf, 19.4 KB)
- [chrome-SEGV-CFXFontLoadGlyphPath9.pdf](attachments/chrome-SEGV-CFXFontLoadGlyphPath9.pdf) (application/pdf, 46.9 KB)

## Timeline

### in...@chromium.org (2014-08-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-26)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5950946103263232

### at...@gmail.com (2014-08-26)

Here is another repro-file causing SEGV with nearly identical stack( frame #3 is different and #4 is new.) I think this is the same issue triggered with slightly different repro-file.

ASAN-trace:

==2279==ERROR: AddressSanitizer: SEGV on unknown address 0x7f463959807c (pc 0x7f46314e09e2 bp 0x7fff9b482890 sp 0x7fff9b482700 T0)
    #0 0x7f46314e09e1 in CFX_Font::LoadGlyphPath(unsigned int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/ge/fx_ge_text.cpp:1662
    #1 0x7f46314dd13d in CFX_FaceCache::LoadGlyphPath(CFX_Font*, unsigned int, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/ge/fx_ge_text.cpp:1522
    #2 0x7f46314dc3b4 in CFX_RenderDevice::DrawTextPath(int, FXTEXT_CHARPOS const*, CFX_Font*, CFX_FontCache*, float, CFX_Matrix const*, CFX_Matrix const*, CFX_GraphStateData const*, unsigned int, unsigned int, CFX_PathData*, int, int, void*, int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/ge/fx_ge_text.cpp:941
    #3 0x7f46314d2eeb in CFX_RenderDevice::DrawNormalText(int, FXTEXT_CHARPOS const*, CFX_Font*, CFX_FontCache*, float, CFX_Matrix const*, unsigned int, unsigned int, int, void*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fxge/ge/fx_ge_text.cpp:172
    #4 0x7f463122e4e8 in CPDF_TextRenderer::DrawNormalText(CFX_RenderDevice*, int, unsigned int*, float*, CPDF_Font*, float, CFX_Matrix const*, unsigned int, CPDF_RenderOptions const*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_text.cpp:696
    #5 0x7f463122b807 in CPDF_RenderStatus::ProcessText(CPDF_TextObject const*, CFX_Matrix const*, CFX_PathData*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_text.cpp:300
    #6 0x7f46311f8511 in CPDF_RenderStatus::ProcessObjectNoClip(CPDF_PageObject const*, CFX_Matrix const*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render.cpp:420
.
.
.
 


### cl...@chromium.org (2014-08-26)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5693285076041728

### bo...@foxitsoftware.com (2014-08-26)

Can not reproduce this one. Can not see crash stack on clusterfuzz report either.

### at...@gmail.com (2014-08-26)

Did you try with both repro-files?

### cl...@chromium.org (2014-08-26)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5711322529398784

### bo...@foxitsoftware.com (2014-08-26)

Yes, I did. This seems related to https://pdfium.googlesource.com/pdfium/+/02132dcdf97674c223d9a3566c89df9f57029d5c. I checkout one commit ahead but can not repro either. 

### at...@gmail.com (2014-08-26)

Hmmm... It seems that it doesn't reproduce on pdfium_test binary, but reproduces clean with ASAN chrome from https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-symbolized-linux-release-291876.zip?generation=1409067028780000&alt=media

### at...@gmail.com (2014-08-26)

So most probably also ClusterFuzz could reproduce it with ASAN Chrome.

### in...@chromium.org (2014-08-26)

Does not reproduce on CF either. cmd line i am using - /mnt/scratch0/clusterfuzz/slave-bot/builds/chromium-browser-asan_linux-release/revisions/asan-linux-release-291876/chrome --allow-file-access-from-files --disable-click-to-play --disable-hang-monitor --disable-metrics --disable-popup-blocking --disable-prompt-on-repost --enable-experimental-extension-apis --enable-extension-apps --enable-extension-timeline-api --enable-nacl --enable-search-provider-api-v2 --enable-video-track --js-flags="--expose-gc --verify-heap" --new-window --no-default-browser-check --no-first-run --no-process-singleton-dialog --enable-shadow-dom --enable-media-stream --use-gl=osmesa --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --user-data-dir=/mnt/scratch0/clusterfuzz/slave-bot/inputs/user-profile-dirs/user_profile_0 --log-net-log=/mnt/scratch0/tmp/net_log_0 /mnt/scratch0/clusterfuzz/slave-bot/inputs/fuzzer-testcases/chrome-SEGV-CFXFontLoadGlyphPath9.pdf



### at...@gmail.com (2014-08-26)

$: ./chrome/chrome --no-sandbox chrome-SEGV-CFXFontLoadGlyphPath9.pdf 
[7592:7592:0826/220641:ERROR:browser_main_loop.cc(162)] Running without the SUID sandbox! See https://code.google.com/p/chromium/wiki/LinuxSUIDSandboxDevelopment for more information on developing with the sandbox on.
ATTENTION: default value of option force_s3tc_enable overridden by environment.
[7657:7657:0826/220642:ERROR:renderer_main.cc(204)] Running without renderer sandbox
[7666:7666:0826/220642:ERROR:renderer_main.cc(204)] Running without renderer sandbox
ASAN:SIGSEGV
=================================================================
==7657==ERROR: AddressSanitizer: SEGV on unknown address 0x7fc68ca3f3bc (pc 0x7fc684980302 bp 0x7fffd66edb90 sp 0x7fffd66eda00 T0)
    #0 0x7fc684980301 (/home/attekett/Downloads/chrome/libpdf.so+0x86b301)
    #1 0x7fc68497ca5d (/home/attekett/Downloads/chrome/libpdf.so+0x867a5d)


### in...@chromium.org (2014-08-26)

Tom, does this look like the same bug. Please see c#8.

### bo...@foxitsoftware.com (2014-08-26)

This is fixed in https://pdfium.googlesource.com/pdfium/+/02132dcdf97674c223d9a3566c89df9f57029d5c. c#8 was based on pdfium. But the crash can only be repro on chrome.

### cl...@chromium.org (2014-08-26)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-09-23)

From my reading here, this looks like it only impacted Dev and didn't make it into Beta/Stable. Marking as Merge-NA and Security_Impact-Head based on that understanding.

### cl...@chromium.org (2014-12-03)

Bulk update: removing view restriction from closed bugs.

### in...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

$1000 for this report.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/407488?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080298)*
