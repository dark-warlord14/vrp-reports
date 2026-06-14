# Security: UNKOWN in CFX_Edit_Provider::GetCharWidthW

| Field | Value |
|-------|-------|
| **Issue ID** | [40085090](https://issues.chromium.org/issues/40085090) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2016-08-13 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 54.0.2829.0  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Open the test case.
2. Go to the second page (2/4).
3. Select any country in "Country of Last School Attended" option.
4. Scroll down >> Crash!

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

rax=000007fed602ffff rbx=0000000000000064 rcx=00000000023abdb0  

rdx=0000000000000000 rsi=0000000000000000 rdi=0000000000000062  

rip=00000400001e1200 rsp=000000000022dde8 rbp=0000000002ef20e0  

r8=0000000000000062 r9=0000000000000000 r10=0000000000000000  

r11=000000000022defc r12=0000000000000002 r13=0000000000000000  

r14=000000000412e9b0 r15=0000000000000000  

iopl=0 nv up ei pl nz na po nc  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00010206  

00000400`001e1200 ?? ??? 0:000> k \*\*\* Stack trace for last set context - .thread/.cxr resets it \*\*\* WARNING: Unable to verify checksum for chrome_child.dll Child-SP RetAddr Call Site 00000000`0022dde8 000007fe`d5aa797b 0x400`001e1200  

00000000`0022ddf0 000007fe`d5a50536 chrome\_child!CFX\_Edit\_Provider::GetCharWidthW+0x27 [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\fxedit\fxet\_edit.cpp @ 284]  

00000000`0022de20 000007fe`d5a5247b chrome\_child!CPDF\_VariableText::GetWordWidth+0x62 [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\core\fpdfdoc\cpdf\_variabletext.cpp @ 799]  

00000000`0022de80 000007fe`d5a52330 chrome\_child!CSection::SearchWordPlace+0x8f [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\core\fpdfdoc\csection.cpp @ 228]  

00000000`0022ded0 000007fe`d5a51178 chrome\_child!CSection::SearchWordPlace+0x1f0 [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\core\fpdfdoc\csection.cpp @ 179]  

00000000`0022df60 000007fe`d5aa8911 chrome\_child!CPDF\_VariableText::SearchWordPlace+0x1d4 [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\core\fpdfdoc\cpdf\_variabletext.cpp @ 575]  

00000000`0022dfc0 000007fe`d5aa9f90 chrome\_child!CFX\_Edit::GetVisibleWordRange+0x6d [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\fxedit\fxet\_edit.cpp @ 1746]  

00000000`0022e020 000007fe`d5aaa81d chrome\_child!CFX\_Edit::Refresh+0x4c [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\fxedit\fxet\_edit.cpp @ 2038]  

00000000`0022e070 000007fe`d5b1218c chrome\_child!CFX\_Edit::SelectNone+0x3d [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\fxedit\fxet\_edit.cpp @ 1826]  

00000000`0022e0a0 000007fe`d5b13bc8 chrome\_child!CPWL\_Edit::OnKillFocus+0x20 [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\pdfwindow\pwl\_edit.cpp @ 463]  

00000000`0022e0d0 000007fe`d5b13c07 chrome\_child!CPWL\_MsgControl::KillFocus+0x24 [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\pdfwindow\pwl\_wnd.cpp @ 175]  

00000000`0022e100 000007fe`d5b13028 chrome\_child!CPWL\_Wnd::KillFocus+0x27 [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\pdfwindow\pwl\_wnd.cpp @ 702]  

00000000`0022e130 000007fe`d59eb353 chrome\_child!CPWL\_Wnd::Destroy+0x20 [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\pdfwindow\pwl\_wnd.cpp @ 274]  

00000000`0022e170 000007fe`d59e91e0 chrome\_child!CFFL\_FormFiller::~CFFL\_FormFiller+0x5b [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_formfiller.cpp @ 34]  

00000000`0022e1c0 000007fe`d4ce170f chrome\_child!CFFL\_ComboBox::`scalar deleting destructor'+0x14 00000000`0022e1f0 000007fe`d59e7174 chrome_child!std::_Tree<std::_Tmap_traits<void const \* __ptr64,std::unique_ptr<base::SupportsUserData::Data,std::default_delete<base::SupportsUserData::Data> >,std::less<void const \* __ptr64>,std::allocator<std::pair<void const \* __ptr64 const,std::unique_ptr<base::SupportsUserData::Data,std::default_delete<base::SupportsUserData::Data> > > >,0> >::erase+0x2db [c:\b\depot_tools\win_toolchain\vs_files\95ddda401ec5678f15eeed01d2bee08fcbc5ee97\vc\include\xtree @ 1440] 00000000`0022e220 000007fe`d59e4eac chrome_child!CFFL_IFormFiller::OnDelete+0x5c [c:\b\build\slave\win64-pgo\build\src\third_party\pdfium\fpdfsdk\formfiller\cffl_iformfiller.cpp @ 123] 00000000`0022e250 000007fe`d59e4e70 chrome_child!CPDFSDK_BFAnnotHandler::ReleaseAnnot+0x1c [c:\b\build\slave\win64-pgo\build\src\third_party\pdfium\fpdfsdk\fsdk_annothandler.cpp @ 461] 00000000`0022e280 000007fe`d59d940f chrome_child!CPDFSDK_AnnotHandlerMgr::ReleaseAnnot+0x34 [c:\b\build\slave\win64-pgo\build\src\third_party\pdfium\fpdfsdk\fsdk_annothandler.cpp @ 91] 00000000`0022e2b0 000007fe`d59d9522 chrome\_child!CPDFSDK\_PageView::~CPDFSDK\_PageView+0x4b [c:\b\build\slave\win64-pgo\build\src\third\_party\pdfium\fpdfsdk\fsdk\_mgr.cpp @ 505]

## Attachments

- [testcase.pdf](attachments/testcase.pdf) (application/pdf, 1.3 MB)
- [Recording.mp4](attachments/Recording.mp4) (video/mp4, 1.8 MB)
- [ASan-stacktrace.txt](attachments/ASan-stacktrace.txt) (text/plain, 12.1 KB)

## Timeline

### oc...@chromium.org (2016-08-15)

dsinclair, could you please take a look?


[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2016-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-16)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-17)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2016-08-17)

This seems like a use-after-free vulnerability.

### ds...@chromium.org (2016-08-17)

chromium.khalil@ are you sure it's the same stack? On linux I get a UAF but it's on a different stack trace then the above.

### ch...@gmail.com (2016-08-18)

[Comment Deleted]

### ch...@gmail.com (2016-08-18)

When I try to repro this under ASan on Windows, I can t get a symbolized stacktrace.

### ds...@chromium.org (2016-08-18)

I uploaded https://codereview.chromium.org/2259823004/ to fix the UAF caused by this file when running with XFA on Linux. Will see if I can figure out what is causing the reported stack trace.

### ds...@chromium.org (2016-08-18)

I can repro the initial failure in ASan on linux. Tracking down .....

### bu...@chromium.org (2016-08-22)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/28a4a2410f24910c709578d981cae3bb8153fdba

commit 28a4a2410f24910c709578d981cae3bb8153fdba
Author: dsinclair <dsinclair@chromium.org>
Date: Mon Aug 22 20:36:02 2016

Destroy window before cleaning up combobox

Currently, when we destroy a CFFL_ComboBox we'll cleanup the fontmap and then
call the destructor for the parent type. This will case the PWL_Wnd to be
destroyed. In this case, the window is a PWL_Edit. On destruction it will reset
the focus which causes the text selection to change, which asks the font map
for data but we've already destroyed the font map.

This CL forces the destruction of the window earlier in order to have the
fontmap available. A followup bug is filed to correct the location of the
fontmap so we don't have this dependency.

BUG=chromium:637546

Review-Url: https://codereview.chromium.org/2266943002

[modify] https://crrev.com/28a4a2410f24910c709578d981cae3bb8153fdba/fpdfsdk/formfiller/cffl_combobox.cpp
[modify] https://crrev.com/28a4a2410f24910c709578d981cae3bb8153fdba/fpdfsdk/formfiller/cffl_formfiller.cpp
[modify] https://crrev.com/28a4a2410f24910c709578d981cae3bb8153fdba/fpdfsdk/formfiller/cffl_formfiller.h
[modify] https://crrev.com/28a4a2410f24910c709578d981cae3bb8153fdba/fpdfsdk/formfiller/cffl_textfield.cpp


### ds...@chromium.org (2016-08-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4bc6edbaaae5387289d5346424e965bada33a9c7

commit 4bc6edbaaae5387289d5346424e965bada33a9c7
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Tue Aug 23 00:14:53 2016

Roll src/third_party/pdfium/ 8d6c929d2..a73b8fee8 (4 commits).

https://pdfium.googlesource.com/pdfium.git/+log/8d6c929d2605..a73b8fee8751

$ git log 8d6c929d2..a73b8fee8 --date=short --no-merges --format='%ad %ae %s'
2016-08-22 tonikitoo Implement Field::SetHidden using Field::SetDisplay.
2016-08-22 weili Make CFX_Color constructor explicit
2016-08-22 dsinclair Destroy window before cleaning up combobox
2016-08-22 tsepez Add fuzzer for CPDF_StreamParser

BUG=637546

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2268763002
Cr-Commit-Position: refs/heads/master@{#413595}

[modify] https://crrev.com/4bc6edbaaae5387289d5346424e965bada33a9c7/DEPS


### sh...@chromium.org (2016-08-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-23)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/837735660808d52580703183ae24a3c7c7b05c7d

commit 837735660808d52580703183ae24a3c7c7b05c7d
Author: dsinclair <dsinclair@chromium.org>
Date: Tue Aug 23 18:39:23 2016

[XFA] Force destruction order of font managers.

The GEFont points to the font manager which creates it and tries to unregister
itself. Currently the GEFont can be created by the default mapper and then
stored in a different mapper. If the default mapper is destroyed first, when
the second mapper cleans up the font there will be a call to unregister on
the default mapper causing a use-after-free.

The long term fix is to fixup the GEFont so it points to the correct mapper
to unregister from. This CL forces the destruction order in CXFA_FFApp to
cleanup the non-default mapper first.

BUG=chromium:637546

Review-Url: https://codereview.chromium.org/2259823004

[modify] https://crrev.com/837735660808d52580703183ae24a3c7c7b05c7d/xfa/fgas/font/fgas_stdfontmgr.cpp
[modify] https://crrev.com/837735660808d52580703183ae24a3c7c7b05c7d/xfa/fgas/font/fgas_stdfontmgr.h
[modify] https://crrev.com/837735660808d52580703183ae24a3c7c7b05c7d/xfa/fxfa/app/xfa_fontmgr.cpp
[modify] https://crrev.com/837735660808d52580703183ae24a3c7c7b05c7d/xfa/fxfa/include/xfa_ffapp.h


### bu...@chromium.org (2016-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fa5b32badcf084f1120a522d76a8e2cc5638171b

commit fa5b32badcf084f1120a522d76a8e2cc5638171b
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Tue Aug 23 21:10:46 2016

Roll src/third_party/pdfium/ c38de1116..837735660 (1 commit).

https://pdfium.googlesource.com/pdfium.git/+log/c38de1116bbe..837735660808

$ git log c38de1116..837735660 --date=short --no-merges --format='%ad %ae %s'
2016-08-23 dsinclair [XFA] Force destruction order of font managers.

BUG=637546

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2269183002
Cr-Commit-Position: refs/heads/master@{#413833}

[modify] https://crrev.com/fa5b32badcf084f1120a522d76a8e2cc5638171b/DEPS


### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

The panel awarded $1,000 for this.  Thanks!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-11-29)

This issue was migrated from crbug.com/chromium/637546?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085090)*
