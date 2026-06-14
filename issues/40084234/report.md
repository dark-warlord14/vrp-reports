# Security: heap-buffer-overflow in SkRegion::RunHead::findScanline

| Field | Value |
|-------|-------|
| **Issue ID** | [40084234](https://issues.chromium.org/issues/40084234) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2016-05-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The latest 32-bit asan build of filter\_fuzz\_stub crashes as follows with the attached input:

=================================================================  

==30079==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xf48003b4 at pc 0x082ebb67 bp 0xffa39c38 sp 0xffa39c30  

READ of size 4 at 0xf48003b4 thread T0  

#0 0x82ebb66 in SkRegion::RunHead::findScanline(int) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkRegionPriv.h:156  

#1 0x82eb93f in SkRegion::contains(int, int) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkRegion.cpp:321 (discriminator 1)  

#2 0x88f2ee0 in SkAlphaThresholdFilterImpl::onFilterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:231 (discriminator 2)  

#3 0x823c4d8 in SkImageFilter::filterImage(SkSpecialImage\*, SkImageFilter::Context const&, SkIPoint\*) const /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:212 (discriminator 1)  

#4 0x8208e16 in SkBaseDevice::drawSpriteWithFilter(SkDraw const&, SkBitmap const&, int, int, SkPaint const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkDevice.cpp:426 (discriminator 2)  

#5 0x81e959f in SkCanvas::onDrawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:2370  

#6 0x81e25b6 in SkCanvas::drawBitmap(SkBitmap const&, float, float, SkPaint const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkCanvas.cpp:1968  

#7 0x8124580 in (anonymous namespace)::RunTestCase(std::\_\_1::basic\_string<char, std::\_*1::char\_traits<char>, std::**1::allocator<char> >&, SkBitmap&, SkCanvas\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:47  

#8 0x8123751 in (anonymous namespace)::ReadAndRunTestCase(char const\*, SkBitmap&, SkCanvas\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#9 0x8123266 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:85  

#10 0xf6c5d73d in \_\_libc\_start\_main ??:?

0xf48003b4 is located 0 bytes to the right of 20-byte region [0xf48003a0,0xf48003b4)  

allocated by thread T0 here:  

#0 0x80f90b3 in **interceptor\_malloc ??:?  

#1 0x8b37f5b in sk\_malloc\_throw(unsigned int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/ext/SkMemory\_new\_handler.cpp:58  

#2 0x82ea0a8 in SkRegion::RunHead::Alloc(int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../third\_party/skia/src/core/SkRegionPriv.h:70 (discriminator 1)  

#3 0x82e9ecb in SkRegion::RunHead::Alloc(int, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkRegionPriv.h:83 (discriminator 1)  

#4 0x82e9e4d in SkRegion::allocateRuns(int, int, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkRegion.cpp:103  

#5 0x82ef3e2 in SkRegion::readFromMemory(void const\*, unsigned int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkRegion.cpp:1140  

#6 0x8355aac in SkValidatingReadBuffer::readRegion(SkRegion\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:153 (discriminator 2)  

#7 0x88f1cb6 in SkAlphaThresholdFilterImpl::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkAlphaThresholdFilter.cpp:78  

#8 0x8356b68 in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:275  

#9 0x823231a in SkValidatingDeserializeFlattenable(void const\*, unsigned int, SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#10 0x81243de in (anonymous namespace)::RunTestCase(std::\_\_1::basic\_string<char, std::\_*1::char\_traits<char>, std::**1::allocator<char> >&, SkBitmap&, SkCanvas\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:31 (discriminator 1)  

#11 0x8123751 in (anonymous namespace)::ReadAndRunTestCase(char const\*, SkBitmap&, SkCanvas\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:66  

#12 0x8123266 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized*/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:85  

#13 0xf6c5d73d in \_\_libc\_start\_main ??:?

SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/nils/MonkeyChrome/asan-symbolized-v8-arm-linux-release-391505/filter\_fuzz\_stub+0x82ebb66)  

Shadow bytes around the buggy address:  

0x3e900020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e900030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e900040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e900050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x3e900060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fd fd  

=>0x3e900070: fd fd fa fa 00 00[04]fa fa fa fd fd fd fd fa fa  

0x3e900080: 00 00 00 fa fa fa 00 00 00 00 fa fa 00 00 00 00  

0x3e900090: fa fa 00 00 00 00 fa fa 00 00 00 00 fa fa 00 00  

0x3e9000a0: 00 00 fa fa 00 00 04 fa fa fa 00 00 04 fa fa fa  

0x3e9000b0: 00 00 04 fa fa fa 00 00 04 fa fa fa 00 00 04 fa  

0x3e9000c0: fa fa 00 00 04 fa fa fa 00 00 04 fa fa fa 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==30079==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-v8-arm-linux-release-391505  

Operating System: Linux

**REPRODUCTION CASE**  

Attached as test.fil

## Attachments

- [test.fil](attachments/test.fil) (application/octet-stream, 108 B)

## Timeline

### cl...@chromium.org (2016-05-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4568082806210560

### cl...@chromium.org (2016-05-05)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-05-06)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### fe...@chromium.org (2016-05-06)

senorblanco@, can you please take a look? could this have been caused by https://chromium.googlesource.com/skia.git/+/c41e7e14f4a0076d277870502168ed870e558dfc?

### fe...@chromium.org (2016-05-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-06)

[Empty comment from Monorail migration]

### se...@chromium.org (2016-05-06)

If I were a betting man, I'd put money on that not being my change. But the fix looks simple enough, so I'll give it a shot.

### bu...@chromium.org (2016-05-06)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/675576f023c8fa10cdb0c18bc0a6c214e0bab069

commit 675576f023c8fa10cdb0c18bc0a6c214e0bab069
Author: senorblanco <senorblanco@chromium.org>
Date: Fri May 06 15:48:57 2016

Detect an invalid intervalCount in SkRegion during deserialiation.

BUG=609260
GOLD_TRYBOT_URL= https://gold.skia.org/search2?unt=true&query=source_type%3Dgm&master=false&issue=1961463003

Review-Url: https://codereview.chromium.org/1961463003

[modify] https://crrev.com/675576f023c8fa10cdb0c18bc0a6c214e0bab069/src/core/SkRegion.cpp


### bu...@chromium.org (2016-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3aac6086196e2dc147a046285caed61c30603a8c

commit 3aac6086196e2dc147a046285caed61c30603a8c
Author: skia-deps-roller <skia-deps-roller@chromium.org>
Date: Fri May 06 16:52:13 2016

Roll src/third_party/skia/ 8ca7da80f..675576f02 (9 commits).

https://chromium.googlesource.com/skia.git/+log/8ca7da80fa32..675576f023c8

$ git log 8ca7da80f..675576f02 --date=short --no-merges --format='%ad %ae %s'
2016-05-06 senorblanco Detect an invalid intervalCount in SkRegion during deserialiation.
2016-05-06 halcanary SkAdvancedTypefaceMetrics: fail cleanly.
2016-05-06 halcanary https://groups.google.com/forum/#!topic/skia-discuss/2F2she2nQMg
2016-05-06 robertphillips Revert of Retract GrRenderTarget a bit within SkGpuDevice (patchset #2 id:20001 of https://codereview.chromium.org/1956473002/ )
2016-05-06 halcanary SkAdvancedTypefaceMetrics: improve robustness
2016-05-06 bsalomon Take SkStrokeRec::InitStyle rather than SkPaint::Style in mask filter and DrawMask GOLD_TRYBOT_URL= https://gold.skia.org/search2?unt=true&query=source_type%3Dgm&master=false&issue=1955633002
2016-05-06 msarett Compile SkForceLinking on CMake
2016-05-06 robertphillips Simplify SkGpuBlurUtils::GaussianBlur method
2016-05-06 robertphillips Revert of Disable layer hoisting for non-8888 canvases (patchset #2 id:20001 of https://codereview.chromium.org/1957433002/ )

BUG=609260,567031,567031

CQ_INCLUDE_TRYBOTS=tryserver.blink:linux_blink_rel
TBR=jvanverth@google.com

Review-Url: https://codereview.chromium.org/1959693002
Cr-Commit-Position: refs/heads/master@{#392077}

[modify] https://crrev.com/3aac6086196e2dc147a046285caed61c30603a8c/DEPS


### cl...@chromium.org (2016-05-08)

ClusterFuzz has detected this issue as fixed in range 392043:392266.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4568082806210560

Uploader: mbarbella@google.com
Job Type: linux_asan_filter_fuzz_stub_32bit
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0xf49001d4
Crash State:
  SkRegion::contains
  SkAlphaThresholdFilterImpl::onFilterImage
  SkImageFilter::filterImage
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=363565:363834
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=392043:392266

Minimized Testcase (0.11 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95TT5EVB4x2fOe489JgHZ5NiaZhOJb62hmTkJ2ja8WxWCAr4MlP20Uo0LfCIg0igQBQT5qTHh9eYHCV49mPiQWUsm8kJKGoBxTuXSHxVWlJqjLa7kI3Sq1nM3d9H0AwLBrt1aoSzge7XhFuAvT8tiHGLcCbkg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### fe...@chromium.org (2016-05-09)

thank you for the quick fix!

### cl...@chromium.org (2016-05-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-05-09)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

Can we land this change to M51 prior to 4pm pacific today? If not, let's consider it for a patch release.

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-05-25)

Is this applicable to any specific OS or All?

Also before we approve merge to M51, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### ti...@google.com (2016-05-27)

Fix has baked since 6 May and was on M52 prior to branch point. This should go with M51.

Krishna - Please approve merge for M51 / 2704.

### go...@chromium.org (2016-05-27)

Approving merge to M51 branch 2704 based on https://crbug.com/chromium/609260#c19. Please merge ASAP (Merge has to be in by 1:00 PM PST on Tuesday, 05/31 in order to make it to next week Stable cut). Thank you.

### sh...@chromium.org (2016-05-31)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2016-05-31)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/e181e8b6235ec8f5d7f1ba49001a534c64f6974a

commit e181e8b6235ec8f5d7f1ba49001a534c64f6974a
Author: senorblanco <senorblanco@chromium.org>
Date: Tue May 31 14:47:50 2016

Detect an invalid intervalCount in SkRegion during deserialiation.

[Cherry-pick from 675576f023c8fa10cdb0c18bc0a6c214e0bab069 to M51 branch.]

TBR=robertphillips@google.com
BUG=609260
GOLD_TRYBOT_URL= https://gold.skia.org/search2?unt=true&query=source_type%3Dgm&master=false&issue=1961463003

Original Review-Url: https://codereview.chromium.org/1961463003
NOTREECHECKS=true
NOTRY=true
NOPRESUBMIT=true

Review-Url: https://codereview.chromium.org/2027643002

[modify] https://crrev.com/e181e8b6235ec8f5d7f1ba49001a534c64f6974a/src/core/SkRegion.cpp


### se...@chromium.org (2016-05-31)

Cherry-picked to Skia's M51 branch as https://skia.googlesource.com/skia/+/e181e8b6235ec8f5d7f1ba49001a534c64f6974a above.

### ti...@google.com (2016-05-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### se...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-06)

$1000 here cloudfuzzer - the panel was unsure how this would be useful this type of info leak would be and if it could lead to a later write. 

I'll punch this into the payment system shortly.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/609260?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084234)*
