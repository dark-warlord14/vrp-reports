# UNKNOWN in Read_CVT

| Field | Value |
|-------|-------|
| **Issue ID** | [40081113](https://issues.chromium.org/issues/40081113) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2015-01-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

# ASAN:SIGSEGV

==14904==ERROR: AddressSanitizer: SEGV on unknown address 0x123a8000c510 (pc 0x0000008ed05c bp 0x7fffaab61d80 sp 0x7fffaab61d70 T0)  

#0 0x8ed05b in Read\_CVT /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/fx\_freetype/src/../fxft2.5.01/src/truetype/ttinterp.c:1615  

#1 0x8f833b in Ins\_MIRP /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/fx\_freetype/src/../fxft2.5.01/src/truetype/ttinterp.c:6582  

#2 0x8e9783 in FPDFAPI\_TT\_RunIns /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/fx\_freetype/src/../fxft2.5.01/src/truetype/ttinterp.c:8819  

#3 0x908a7d in tt\_size\_run\_prep /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/fx\_freetype/src/../fxft2.5.01/src/truetype/ttobjs.c:886  

#4 0x907d33 in tt\_size\_ready\_bytecode /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/fx\_freetype/src/../fxft2.5.01/src/truetype/ttobjs.c:1098  

#5 0x9019ef in tt\_loader\_init /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/fx\_freetype/src/../fxft2.5.01/src/truetype/ttgload.c:1990  

#6 0x9012ec in TT\_Load\_Glyph /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/fx\_freetype/src/../fxft2.5.01/src/truetype/ttgload.c:2258  

#7 0x85eb8c in FPDFAPI\_FT\_Load\_Glyph /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/fx\_freetype/src/../fxft2.5.01/src/base/ftobjs.c:721  

#8 0x89aebd in CFX\_FaceCache::RenderGlyph(CFX\_Font\*, unsigned int, int, CFX\_Matrix const\*, int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/ge/fx\_ge\_text.cpp:1338  

#9 0x89a8a6 in CFX\_FaceCache::LookUpGlyphBitmap(CFX\_Font\*, CFX\_Matrix const\*, CFX\_ByteStringC&, unsigned int, int, int, int) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/ge/fx\_ge\_text.cpp:1094  

#10 0x899012 in CFX\_FaceCache::LoadGlyphBitmap(CFX\_Font\*, unsigned int, int, CFX\_Matrix const\*, int, int, int&) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/ge/fx\_ge\_text.cpp:1137  

#11 0x88e698 in CFX\_RenderDevice::DrawNormalText(int, FXTEXT\_CHARPOS const\*, CFX\_Font\*, CFX\_FontCache\*, float, CFX\_Matrix const\*, unsigned int, unsigned int, int, void\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fxge/ge/fx\_ge\_text.cpp:235  

#12 0x5ecbb3 in CPDF\_TextRenderer::DrawNormalText(CFX\_RenderDevice\*, int, unsigned int\*, float\*, CPDF\_Font\*, float, CFX\_Matrix const\*, unsigned int, CPDF\_RenderOptions const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_text.cpp:684  

#13 0x5e9c1e in CPDF\_RenderStatus::ProcessText(CPDF\_TextObject const\*, CFX\_Matrix const\*, CFX\_PathData\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_text.cpp:288  

#14 0x5b4ae2 in CPDF\_RenderStatus::ProcessObjectNoClip(CPDF\_PageObject const\*, CFX\_Matrix const\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:399  

#15 0x5b4f0c in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:344  

#16 0x5bb415 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1133  

#17 0x4a8d86 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:726  

#18 0x4a9130 in FPDF\_RenderPageBitmap /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:524  

#19 0x4a3ab9 in RenderPdf /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:426  

#20 0x4a4724 in main /mnt/data/b/build/slave/ASAN\_Release\_\_symbolized\_/build/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:512  

#21 0x7f4cb66f5ec4 in \_\_libc\_start\_main /build/buildd/eglibc-2.19/csu/libc-start.c:287

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV ??:0 ??  

==14904==ABORTING

**VERSION**  

Chrome Version: asan-symbolized-linux-release-309428

**REPRODUCTION CASE**  

Attached as repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 525.6 KB)

## Timeline

### cl...@chromium.org (2015-01-04)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4854469152997376

### in...@chromium.org (2015-01-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-04)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4854469152997376

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: UNKNOWN
Crash Address: 0x123a8000c510
Crash State:
  Read_CVT
  FPDFAPI_TT_RunIns
  tt_size_run_prep
  

Minimized Testcase (525.61 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97bdoZyAazncDoxzOCk62ynrgBYjUBBuKCRTA4nRPhS098609zdCWqZvOk685iagCmTH5xtiRD-mL83LxcWqDLaBYfrh6fP2NcKjyCHRahWwXEexuTNaCx9TuWbXTUTJMghrrX1MnKl-MWT8amGiPlLn7QAf5CwxXlAhzGGJaQHLHDtMQM



### cl...@chromium.org (2015-01-04)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-01-04)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2015-01-05)

freetype has been updated in https://pdfium.googlesource.com/pdfium/+/b3a323016ab64d3f3ff044a5d7084c272327692e but not rolled to chromium yet.

### bo...@foxitsoftware.com (2015-01-05)

The commit in #6 is wrong, see this one https://pdfium.googlesource.com/pdfium/+/e4fc5ced45c8fcfbe2487ec64eab036bc7d57602

### in...@chromium.org (2015-01-05)

please mark as status=Fixed once pdfium roll happens and freetype is updated.

### th...@chromium.org (2015-01-06)

tsepez is doing the roll: https://codereview.chromium.org/789613007/

### aa...@google.com (2015-01-06)

Thanks Tom - https://crrev.com/6ae67338f424ae28d3cd1344282dfb7391ad3025

### cl...@chromium.org (2015-01-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### th...@chromium.org (2015-01-07)

Isn't this the same as https://crbug.com/chromium/387964?

### cl...@chromium.org (2015-01-07)

ClusterFuzz has detected this issue as fixed in range 310098:310217.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4854469152997376

Uploader: aarya@google.com
Job Type: Linux_asan_pdfium

Crash Type: UNKNOWN
Crash Address: 0x123a8000c510
Crash State:
  Read_CVT
  FPDFAPI_TT_RunIns
  tt_size_run_prep
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=310098:310217

Minimized Testcase (525.61 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97bdoZyAazncDoxzOCk62ynrgBYjUBBuKCRTA4nRPhS098609zdCWqZvOk685iagCmTH5xtiRD-mL83LxcWqDLaBYfrh6fP2NcKjyCHRahWwXEexuTNaCx9TuWbXTUTJMghrrX1MnKl-MWT8amGiPlLn7QAf5CwxXlAhzGGJaQHLHDtMQM

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2015-01-07)

387964 was a null pointer crash, and this one is security related, stack looks similar. no idea if the same. but these look like all old freetype bugs that got nuked with update.

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-27)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Updating severity

### ti...@google.com (2015-03-03)

Congrats - $1000 for this report.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-07)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-04-14)

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

This issue was migrated from crbug.com/chromium/446033?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081113)*
