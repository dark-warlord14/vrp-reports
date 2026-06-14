# Global-buffer-overflow in SkGradientShaderBase::SkGradientShaderBase

| Field | Value |
|-------|-------|
| **Issue ID** | [40081093](https://issues.chromium.org/issues/40081093) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2015-01-01 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

This bug exists in the deserialisation routines for SKImageFilter, which can be triggered on the host process from a renderer through IPC (For example as part of an SwapCompositorFrame message). The filter\_fuzz\_stub binary can be used to reproduce the crash using the attached testcase (repro.fil).

The index into the global array gTileProcs is not properly verified when retrieving a function pointer from this array, this could potentially result in code execution in the host process. An attacker could also use this to get around ASLR by using relative indexing into the binary which also contains the gTileProcs array. VTables stored in this binary should provide plenty function pointers to choose from.

ASAN output:

# [0101/131758:INFO:filter\_fuzz\_stub.cc(59)] Test case: submission1/repro.fil

==10654==ERROR: AddressSanitizer: global-buffer-overflow on address 0x087ed0e0 at pc 0x085a965e bp 0xffdd8b78 sp 0xffdd8b70  

READ of size 4 at 0x087ed0e0 thread T0  

#0 0x85a965d in SkGradientShaderBase::SkGradientShaderBase(SkGradientShaderBase::Descriptor const&, SkMatrix const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkGradientShader.cpp:82  

#1 0x85b4644 in SkLinearGradient::SkLinearGradient(SkPoint const\*, SkGradientShaderBase::Descriptor const&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkLinearGradient.cpp:60  

#2 0x85aed5f in SkGradientShader::CreateLinear(SkPoint const\*, unsigned int const\*, float const\*, int, SkShader::TileMode, unsigned int, SkMatrix const\*) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkGradientShader.cpp:774  

#3 0x85b4eb8 in SkLinearGradient::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/gradients/SkLinearGradient.cpp:71  

#4 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#5 0x81e83d3 in SkShader\* SkReadBuffer::readFlattenable<SkShader>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#6 0x81e533b in SkReadBuffer::readShader() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:133  

#7 0x859e58c in SkRectShaderImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkRectShaderImageFilter.cpp:39  

#8 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#9 0x81c8763 in SkImageFilter\* SkReadBuffer::readFlattenable<SkImageFilter>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#10 0x81bf3cb in SkReadBuffer::readImageFilter() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:129  

#11 0x81bee2a in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:89  

#12 0x85691dc in (anonymous namespace)::SkSpecularLightingImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkLightingImageFilter.cpp:1088 (discriminator 1)  

#13 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#14 0x81c8763 in SkImageFilter\* SkReadBuffer::readFlattenable<SkImageFilter>() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:125  

#15 0x81bf3cb in SkReadBuffer::readImageFilter() /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkReadBuffer.h:129  

#16 0x81bee2a in SkImageFilter::Common::unflatten(SkReadBuffer&, int) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkImageFilter.cpp:89  

#17 0x852d003 in SkBlurImageFilter::CreateProc(SkReadBuffer&) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/effects/SkBlurImageFilter.cpp:43 (discriminator 1)  

#18 0x82945ca in SkValidatingReadBuffer::readFlattenable(SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkValidatingReadBuffer.cpp:247  

#19 0x81b9986 in SkValidatingDeserializeFlattenable(void const\*, unsigned int, SkFlattenable::Type) /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../third\_party/skia/src/core/SkFlattenableSerialization.cpp:26  

#20 0x80f173f in RunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:30  

#21 0x80f1131 in ReadAndRunTestCase /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:65  

#22 0x80f0cb4 in main /mnt/data/b/build/slave/ASan\_Release\_\_32-bit\_x86\_with\_V8-ARM\_\_symbolized\_/build/src/out/Release/../../skia/tools/filter\_fuzz\_stub/filter\_fuzz\_stub.cc:81  

#23 0xf6dc5a82 in \_\_libc\_start\_main ??:?

0x087ed0e0 is located 32 bytes to the left of global variable 'vtable for SkImageFilter' defined in '../../third\_party/skia/src/core/SkImageFilter.cpp' (0x87ed100) of size 60  

0x087ed0e0 is located 20 bytes to the right of global variable 'vtable for SkDrawLooper' defined in '../../third\_party/skia/src/core/SkDrawLooper.cpp' (0x87ed0a0) of size 44  

SUMMARY: AddressSanitizer: global-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x210fd9c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x210fd9d0: 00 00 00 00 00 00 00 00 f9 f9 f9 f9 00 00 00 00  

0x210fd9e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x210fd9f0: 00 00 00 f9 f9 f9 f9 f9 00 00 00 00 00 04 f9 f9  

0x210fda00: f9 f9 f9 f9 00 00 00 00 00 00 00 00 04 f9 f9 f9  

=>0x210fda10: f9 f9 f9 f9 00 00 00 00 00 04 f9 f9[f9]f9 f9 f9  

0x210fda20: 00 00 00 00 00 00 00 04 f9 f9 f9 f9 00 00 00 00  

0x210fda30: 00 00 00 00 00 00 00 00 00 00 00 00 f9 f9 f9 f9  

0x210fda40: 00 00 00 00 00 00 00 00 00 04 f9 f9 f9 f9 f9 f9  

0x210fda50: 00 00 00 04 f9 f9 f9 f9 00 00 00 00 00 00 00 00  

0x210fda60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==10654==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-v8-arm-linux-release-309788

**REPRODUCTION CASE**  

Attached as repro.fil. Use 32-bit build of filter\_fuzz\_stub to reproduce.

## Attachments

- [repro.fil](attachments/repro.fil) (application/octet-stream, 268 B)

## Timeline

### in...@chromium.org (2015-01-01)

Wow! Super nice knockout CloudFuzzer@. We were missing fuzzing the 32-bit filter fuzz binary. Starting fuzzing now, but you probably did it nicely already :)

Sugoi@, I enabled your fuzzer on newly created 32-bit job type linux_asan_filter_fuzz_stub_32bit.

### cl...@chromium.org (2015-01-01)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6291963090305024

### cl...@chromium.org (2015-01-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6291963090305024

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Global-buffer-overflow READ 4
Crash Address: 0x088e5ac0
Crash State:
  SkGradientShaderBase::SkGradientShaderBase
  SkLinearGradient::SkLinearGradient
  SkGradientShader::CreateLinear
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=309756:309788

Minimized Testcase (0.26 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95gyXeA_VVLQfbGEIF9f3U0uuu7EEWPtjb4iU29Zet7aTX78QtcNazALo2_UMMtufghrcWT3i07cwoOo74BIIsnGKHYnZkdNgD-Su_KNZeBPtYCE092TJkv8dxjprHT_RLXFXlkzK9DaaKdoqWwm_r5zciE4Q



### cl...@chromium.org (2015-01-01)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-01-04)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-01-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-04)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### [Deleted User] (2015-01-05)

Here is the offending line (I think) :

SkGradientShaderBase::SkGradientShaderBase(const Descriptor& desc, const SkMatrix& ptsToUnit)
    : INHERITED(desc.fLocalMatrix)
    , fPtsToUnit(ptsToUnit)
{
    fPtsToUnit.getType();  // Precache so reads are threadsafe.
    SkASSERT(desc.fCount > 1);

    fGradFlags = SkToU8(desc.fGradFlags);

    SkASSERT((unsigned)desc.fTileMode < SkShader::kTileModeCount);
    SkASSERT(SkShader::kTileModeCount == SK_ARRAY_COUNT(gTileProcs));
    fTileMode = desc.fTileMode;
    fTileProc = gTileProcs[desc.fTileMode];    <--------------

The factory that calls this constructor should check the range of the enum.



### se...@chromium.org (2015-01-05)

[Empty comment from Monorail migration]

### re...@google.com (2015-01-06)

possible fix : https://codereview.chromium.org/837013002

### cl...@chromium.org (2015-01-06)

ClusterFuzz has detected this issue as fixed in range 309892:309898.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6291963090305024

Uploader: aarya@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Global-buffer-overflow READ 4
Crash Address: 0x088e5ac0
Crash State:
  SkGradientShaderBase::SkGradientShaderBase
  SkLinearGradient::SkLinearGradient
  SkGradientShader::CreateLinear
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=309756:309788
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=309892:309898

Minimized Testcase (0.26 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95gyXeA_VVLQfbGEIF9f3U0uuu7EEWPtjb4iU29Zet7aTX78QtcNazALo2_UMMtufghrcWT3i07cwoOo74BIIsnGKHYnZkdNgD-Su_KNZeBPtYCE092TJkv8dxjprHT_RLXFXlkzK9DaaKdoqWwm_r5zciE4Q

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### aa...@google.com (2015-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### pe...@google.com (2015-01-25)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### dx...@chromium.org (2015-01-30)

not approved for m40.  seems too risky.

### ri...@chromium.org (2015-03-09)

Hey, do we know what code change fixed this bug?

Unless a check was added elsewhere, https://code.google.com/p/chromium/codesearch#chromium/src/third_party/skia/src/effects/gradients/SkGradientShader.cpp&l=82 still shows an unchecked index (the asserts are only enabled on debug builds).

It looks like the index comes from https://code.google.com/p/chromium/codesearch#chromium/src/third_party/skia/src/effects/gradients/SkGradientShader.cpp&l=56, maybe worth adding a check there as well.

### ti...@google.com (2015-04-09)

Congratulations - $5000 for this report.

### cl...@chromium.org (2015-04-14)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

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

### is...@google.com (2018-01-22)

This issue was migrated from crbug.com/chromium/445807?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081093)*
