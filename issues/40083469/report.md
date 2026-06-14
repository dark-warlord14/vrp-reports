# Security: PureCall on CPWL_Edit::OnKillFocus

| Field | Value |
|-------|-------|
| **Issue ID** | [40083469](https://issues.chromium.org/issues/40083469) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **CVE IDs** | CVE-2016-1613 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2015-12-29 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Bug reported in <https://crbug.com/chromium/537173> reproduces again.  

Attached test case crashes with a PureCall.  

Please open test.pdf file in a PDF editor to see JavaScript code which triggers pureCall. JavaScript is available in Document Will Close Action.

**VERSION**  

Chrome Version: [49.0.2606.0] + [TOT debug build]  

Operating System: [Windows 10]

**REPRODUCTION CASE**

1. Build chrome debug build.  
   
   ninja -C out\Debug chrome
2. Run chrome debug build
3. Open test.pdf in chrome
4. Attach visual studio debugger to chrome PDF process.
5. Press reload button in chrome.
6. The debugger will fail with PureCall debug break.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF plugin process.]  

Crash State:  

base.dll!`anonymous namespace'::PureCall() Line 26  

[External Code]  

[Frames below may be incorrect and/or missing, no symbols loaded for msvcr120d.dll]  

chrome.dll!CPWL\_Edit::OnKillFocus() Line 696  

chrome.dll!CPWL\_MsgControl::KillFocus() Line 157  

chrome.dll!CPWL\_Wnd::KillFocus() Line 720  

chrome.dll!CPWL\_Wnd::Destroy() Line 248  

chrome.dll!CFFL\_FormFiller::~CFFL\_FormFiller() Line 29  

chrome.dll!CFFL\_TextField::~CFFL\_TextField() Line 20  

[External Code]  

chrome.dll!CFFL\_IFormFiller::UnRegisterFormFiller(CPDFSDK\_Annot \* pAnnot) Line 554  

chrome.dll!CFFL\_IFormFiller::OnDelete(CPDFSDK\_Annot \* pAnnot) Line 119  

chrome.dll!CPDFSDK\_BFAnnotHandler::ReleaseAnnot(CPDFSDK\_Annot \* pAnnot) Line 358  

chrome.dll!CPDFSDK\_AnnotHandlerMgr::ReleaseAnnot(CPDFSDK\_Annot \* pAnnot) Line 67  

chrome.dll!CPDFSDK\_PageView::~CPDFSDK\_PageView() Line 612  

[External Code]  

chrome.dll!CPDFSDK\_Document::~CPDFSDK\_Document() Line 396  

[External Code]  

chrome.dll!FPDFDOC\_ExitFormFillEnvironment(void \* hHandle) Line 105  

chrome.dll!chrome\_pdf::PDFiumEngine::~PDFiumEngine() Line 617

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 1.9 KB)

## Timeline

### cl...@chromium.org (2015-12-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5194496305790976

### cl...@chromium.org (2015-12-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6315043341205504

### th...@chromium.org (2015-12-30)

[Empty comment from Monorail migration]

### th...@chromium.org (2015-12-31)

I can't reproduce this on Linux near r367110. The calls happen in a sane order here:

CPWL_Edit ctor
CPWL_MsgControl ctor
CPWL_MsgControl::KillFocus
CPWL_Edit::OnKillFocus
CPWL_MsgControl dtor
CPWL_Edit dtor


### ch...@gmail.com (2016-01-01)

I can still reproduce on windows debug build (version:49.0.2609.0).
But I am unable to test on Linux, since there are some issues with my Linux machine.

### mb...@chromium.org (2016-01-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-04)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-01-05)

I ran the test case as a pdfium embedder test on linux.
  a). Did not reproduce when pdfium is built with clang.
  b). Reproduced when pdfium is build without clang.
      GYP_DEFINES=clang=0 build/gyp_pdfium
I was unable to build chromium and test without clang on linux so far.

### np...@chromium.org (2016-01-06)

ochang -- Can you try repro'ing this on windows?

### ch...@gmail.com (2016-01-06)

This is the back-trace I get from gdb when test case is run as pdfium_embeddertest on Linux. Pdfium_embeddertest should be built without clang with below mentioned steps. 
1. GYP_DEFINES=clang=0 build/gyp_pdfium.
2. ninja -C out/Debug pdfium_embeddertests

#0  0x00007ffff695ecc9 in __GI_raise (sig=sig@entry=6)
    at ../nptl/sysdeps/unix/sysv/linux/raise.c:56
#1  0x00007ffff69620d8 in __GI_abort () at abort.c:89
#2  0x00007ffff7487535 in __gnu_cxx::__verbose_terminate_handler() ()
   from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
#3  0x00007ffff74856d6 in ?? () from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
#4  0x00007ffff7485703 in std::terminate() ()
   from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
#5  0x00007ffff74861bf in __cxa_pure_virtual ()
   from /usr/lib/x86_64-linux-gnu/libstdc++.so.6
#6  0x0000000001188a7b in CPWL_Edit::OnKillFocus (this=0x267eee0)
    at ../../fpdfsdk/src/pdfwindow/PWL_Edit.cpp:695
#7  0x00000000011ade98 in CPWL_MsgControl::KillFocus (this=0x267f2a0)
    at ../../fpdfsdk/src/pdfwindow/PWL_Wnd.cpp:152
#8  0x00000000011b174d in CPWL_Wnd::KillFocus (this=0x267eee0)
    at ../../fpdfsdk/src/pdfwindow/PWL_Wnd.cpp:703
#9  0x00000000011ae421 in CPWL_Wnd::Destroy (this=0x267eee0)
    at ../../fpdfsdk/src/pdfwindow/PWL_Wnd.cpp:241
#10 0x0000000000596af5 in CFFL_FormFiller::~CFFL_FormFiller (this=0x26c33b0, 
    __in_chrg=<optimized out>)
    at ../../fpdfsdk/src/formfiller/FFL_FormFiller.cpp:30
#11 0x00000000005a0ad2 in CFFL_TextField::~CFFL_TextField (this=0x26c33b0, 
    __in_chrg=<optimized out>)
---Type <return> to continue, or q <return> to quit---
    at ../../fpdfsdk/src/formfiller/FFL_TextField.cpp:18
#12 0x00000000005a0b1c in CFFL_TextField::~CFFL_TextField (this=0x26c33b0, 
    __in_chrg=<optimized out>)
    at ../../fpdfsdk/src/formfiller/FFL_TextField.cpp:20
#13 0x000000000059c456 in CFFL_IFormFiller::UnRegisterFormFiller (
    this=0x26c32c0, pAnnot=0x26c3310)
    at ../../fpdfsdk/src/formfiller/FFL_IFormFiller.cpp:557
#14 0x000000000059af7a in CFFL_IFormFiller::OnDelete (this=0x26c32c0, 
    pAnnot=0x26c3310) at ../../fpdfsdk/src/formfiller/FFL_IFormFiller.cpp:121
#15 0x00000000004a0e0b in CPDFSDK_BFAnnotHandler::ReleaseAnnot (
    this=0x26c2630, pAnnot=0x26c3310)
    at ../../fpdfsdk/src/fsdk_annothandler.cpp:358
#16 0x00000000004a0072 in CPDFSDK_AnnotHandlerMgr::ReleaseAnnot (
    this=0x26c3260, pAnnot=0x26c3310)
    at ../../fpdfsdk/src/fsdk_annothandler.cpp:67
#17 0x000000000049a19e in CPDFSDK_PageView::~CPDFSDK_PageView (this=0x26c2540, 
    __in_chrg=<optimized out>) at ../../fpdfsdk/src/fsdk_mgr.cpp:612
#18 0x0000000000499634 in CPDFSDK_Document::~CPDFSDK_Document (this=0x26b1150, 
    __in_chrg=<optimized out>) at ../../fpdfsdk/src/fsdk_mgr.cpp:396
#19 0x0000000000475c36 in FPDFDOC_ExitFormFillEnvironment (hHandle=0x26adbe0)
    at ../../fpdfsdk/src/fpdfformfill.cpp:105
#20 0x0000000000437ccb in EmbedderTest::TearDown (this=0x26594f0)
    at ../../testing/embedder_test.cpp:81




### th...@chromium.org (2016-01-06)

Yes I can repro with gcc. Fix: https://codereview.chromium.org/1564773003

### cl...@chromium.org (2016-01-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/806bd1cae5a92505ca052bb1406b2dd60ce06b41

commit 806bd1cae5a92505ca052bb1406b2dd60ce06b41
Author: thestig <thestig@chromium.org>
Date: Thu Jan 07 09:50:40 2016

Roll PDFium 03f5040..0213958

https://pdfium.googlesource.com/pdfium.git/+log/03f5040..0213958

BUG=572871
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1563203002

Cr-Commit-Position: refs/heads/master@{#368045}

[modify] http://crrev.com/806bd1cae5a92505ca052bb1406b2dd60ce06b41/DEPS


### th...@chromium.org (2016-01-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-07)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-08)

thestig / tsepez: can you please add a severity and a desired milestone for this bug?

### ti...@google.com (2016-01-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2016-01-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### th...@chromium.org (2016-01-12)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-12)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ti...@google.com (2016-01-12)

Merge approved for M48 (branch 2564). Pls go ahead merge.

A friendly reminder that M48 Stable is launching very soon! Pls make sure to get it merged into release branch by Jan-12. All changes MUST be merged into the release branch by 5pm on Jan-14 to make into the Stable final build cut. Thanks!

### bu...@chromium.org (2016-01-12)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=82801

------------------------------------------------------------------
r82801 | thestig@google.com | 2016-01-12T20:19:57.302122Z

-----------------------------------------------------------------

### ti...@google.com (2016-01-19)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

Congratulations - $3000 for this report. I'll start payment shortly.

### ti...@google.com (2016-01-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-20)

CVE-2016-1613

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-14)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

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

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/572871?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083469)*
