# Heap-buffer-overflow in void SkMatrixConvolutionImageFilter::filterPixels<ClampPixelFetcher, false>

| Field | Value |
|-------|-------|
| **Issue ID** | [40080540](https://issues.chromium.org/issues/40080540) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2014-09-26 |
| **Bounty** | $2,000.00 |

## Description



Tested on:

OS: Ubuntu 12.04

Chromium	39.0.2170.0 (Developer Build) 
Revision	6128c200e138d3d7c52aae5e01d0af36a48b1706-refs/heads/master@{#296715}


The repro-file is inside tar.gz package because Chrome crashes every time I try to attach the file. Also Ubuntu nautilus will crash with a null-pointer crash if you try to access the folder where the file is. 

ASAN-report:

==6564==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000093af0 at pc 0x7fb8ead1e16d bp 0x7fb8aecfb530 sp 0x7fb8aecfb528
READ of size 4 at 0x602000093af0 thread T7 (CompositorRaste)
    #0 0x7fb8ead1e16c in void SkMatrixConvolutionImageFilter::filterPixels<ClampPixelFetcher, false>(SkBitmap const&, SkBitmap*, SkIRect const&, SkIRect const&) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/effects/SkMatrixConvolutionImageFilter.cpp:197
    #1 0x7fb8ead1a1e4 in SkMatrixConvolutionImageFilter::onFilterImage(SkImageFilter::Proxy*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap*, SkIPoint*) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/effects/SkMatrixConvolutionImageFilter.cpp:328
    #2 0x7fb8ea9b8720 in SkImageFilter::filterImage(SkImageFilter::Proxy*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap*, SkIPoint*) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkImageFilter.cpp:186
    #3 0x7fb8eace0e6e in SkColorFilterImageFilter::onFilterImage(SkImageFilter::Proxy*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap*, SkIPoint*) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/effects/SkColorFilterImageFilter.cpp:114
    #4 0x7fb8ea9b8720 in SkImageFilter::filterImage(SkImageFilter::Proxy*, SkBitmap const&, SkImageFilter::Context const&, SkBitmap*, SkIPoint*) const /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkImageFilter.cpp:186
    #5 0x7fb8ea9866a5 in SkCanvas::internalDrawDevice(SkBaseDevice*, int, int, SkPaint const*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkCanvas.cpp:1227
    #6 0x7fb8ea982fdb in SkCanvas::internalRestore() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkCanvas.cpp:1009
    #7 0x7fb8ea985f27 in SkCanvas::restore() /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/core/SkCanvas.cpp:979
.
.
.
0x602000093af1 is located 0 bytes to the right of 1-byte region [0x602000093af0,0x602000093af1)
allocated by thread T0 (chrome) here:
    #0 0x7fb8e8b10c6b in operator new[](unsigned long) ??:0
    #1 0x7fb8ead181ad in SkMatrixConvolutionImageFilter::SkMatrixConvolutionImageFilter(SkTSize<int> const&, float const*, float, float, SkIPoint const&, SkMatrixConvolutionImageFilter::TileMode, bool, SkImageFilter*, SkImageFilter::CropRect const*, unsigned int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/src/effects/SkMatrixConvolutionImageFilter.cpp:39
    #2 0x7fb8ead192ac in SkMatrixConvolutionImageFilter::Create(SkTSize<int> const&, float const*, float, float, SkIPoint const&, SkMatrixConvolutionImageFilter::TileMode, bool, SkImageFilter*, SkImageFilter::CropRect const*, unsigned int) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/skia/include/effects/SkMatrixConvolutionImageFilter.h:65
    #3 0x7fb8f3bc4498 in blink::FEConvolveMatrix::createImageFilter(blink::SkiaImageFilterBuilder*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/filters/FEConvolveMatrix.cpp:534
    #4 0x7fb8ebd3037e in blink::FilterEffect::createImageFilterWithoutValidation(blink::SkiaImageFilterBuilder*) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/filters/FilterEffect.cpp:548
    #5 0x7fb8ebd057c9 in blink::SkiaImageFilterBuilder::build(blink::FilterEffect*, blink::ColorSpace, bool) /b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/filters/SkiaImageFilterBuilder.cpp:71
.
.
.



## Attachments

- [repro-file.tar.gz](attachments/repro-file.tar.gz) (application/x-gzip, 16.0 KB)

## Timeline

### in...@chromium.org (2014-09-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-26)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6708652560875520

### at...@gmail.com (2014-09-26)

Btw, if this is figured to be a skia issue in chrome, I want to report this separately to whoever is responsible for Ubuntu nautilus.

### cl...@chromium.org (2014-09-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6708652560875520

Uploader: rsesek@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60900018bb70
Crash State:
  void SkMatrixConvolutionImageFilter::filterPixels<ClampPixelFetcher, false>
  SkMatrixConvolutionImageFilter::onFilterImage
  SkImageFilter::filterImage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291444:291576

Minimized Testcase (0.85 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94V9L2OH6IIfonVTVA2rG_KAlDtRnN5UijJF-sRoBcEOFvEjcGF1yb_TCA2q7Frk7ML3DAQl_EyzyvJsuRz21KQCYxsXRBIQrziAlJWgpgyt8Pf5JrhaTuFeWPIXl25e8gSja_7K4tAC6lCglAUu9AWO0OiCg



### rs...@chromium.org (2014-09-26)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-09-26)

attekett: This issue does appear limited to Skia. Unless Nautilus also uses Skia internally, it would appear to be a separate bug for that product.

### [Deleted User] (2014-09-26)

[Empty comment from Monorail migration]

### se...@chromium.org (2014-09-26)

[Empty comment from Monorail migration]

### at...@gmail.com (2014-09-26)

Let me know when I can report this to guys from Ubuntu. I hate it when my whole file manager crashes for a file. :)

### cl...@chromium.org (2014-09-26)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### se...@chromium.org (2014-09-26)

Skia patch up at https://codereview.chromium.org/610723002/.

### in...@chromium.org (2014-09-27)

Stephen, does this impact Stable ? Is yes change Security_Impact-Head to Security_Impact-Stable.

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### se...@chromium.org (2014-09-29)

inferno: Yes, it does affect Stable (m37).

### am...@chromium.org (2014-09-30)

We need all beta blockers closed by Friday at the latest.  Mike, will that be viable?

### se...@chromium.org (2014-09-30)

The fix landed in Skia at https://chromium.googlesource.com/skia/+/3a49520696b2eca69e57884657d23fd2402ccfd1 and rolled into Chrome at r297189. I was just waiting on some bake time before requesting merge.

### am...@google.com (2014-09-30)

Is there a merge required here?

### cl...@chromium.org (2014-09-30)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-30)

ClusterFuzz has detected this issue as fixed in range 296715:297214.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6708652560875520

Uploader: rsesek@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60900018bb70
Crash State:
  void SkMatrixConvolutionImageFilter::filterPixels<ClampPixelFetcher, false>
  SkMatrixConvolutionImageFilter::onFilterImage
  SkImageFilter::filterImage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=291444:291576
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=296715:297214

Minimized Testcase (0.85 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94V9L2OH6IIfonVTVA2rG_KAlDtRnN5UijJF-sRoBcEOFvEjcGF1yb_TCA2q7Frk7ML3DAQl_EyzyvJsuRz21KQCYxsXRBIQrziAlJWgpgyt8Pf5JrhaTuFeWPIXl25e8gSja_7K4tAC6lCglAUu9AWO0OiCg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### se...@chromium.org (2014-09-30)

Requesting merge to M38.

### se...@chromium.org (2014-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2014-09-30)

Approved for 38.

### se...@chromium.org (2014-09-30)

Landed on Skia's chrome/m38_2125 branch as https://skia.googlesource.com/skia/+/f14866df6ca3ecce221916fa0c061af49385a863.

### se...@chromium.org (2014-09-30)

Requesting merge to M39.

### am...@chromium.org (2014-10-01)

merge approved for m39 branch 2171

### se...@chromium.org (2014-10-01)

Merge to Skia's chrome/m39 branch as https://skia.googlesource.com/skia/+/aafcb54f27d30c63602a0a0232f0b9fc8b310d19.

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-11-15)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks for the report! This one qualified for a $2000 reward.

### si...@gmail.com (2014-11-20)

attekett,
Was this reported to ubuntu? I see it crashes nautilus in fedora as well.

### at...@gmail.com (2014-11-20)


Not this one yet. I have tried to report bundle of security bugs from librsvg to gnome3 bugzilla. Those reports have been inactive for almost two months. If they don't even respond to security bugs, I would guess reporting null-pointers would be useless. :(

### si...@gmail.com (2014-11-20)

I can chase upstream if you want, let me know if there is an upstream bug. My gnome bz address is huzaifas@redhat.com

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-06)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/418161?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080540)*
