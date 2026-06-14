# pdfium: oob read in PDF_DecodeText

| Field | Value |
|-------|-------|
| **Issue ID** | [40050063](https://issues.chromium.org/issues/40050063) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | pd...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-09-05 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.133 Safari/537.36

Steps to reproduce the problem:
==4947==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000004597
READ of size 1 at 0x602000004597 thread T0
SCARINESS: 12 (1-byte-read-heap-buffer-overflow)
    #0 0x55fa7ee6ed62 in (anonymous namespace)::GetUnicodeFromBigEndianBytes(unsigned char const*) core/fpdfapi/parser/fpdf_parser_decode.cpp:34:26
    #1 0x55fa7ee4cfef in PDF_DecodeText(pdfium::span<unsigned char const>) core/fpdfapi/parser/fpdf_parser_decode.cpp:495:23
    #2 0x55fa7ee64f8f in CPDF_Stream::GetUnicodeText() const core/fpdfapi/parser/cpdf_stream.cpp:178:10
    #3 0x55fa7f11ad14 in CPDF_Action::GetJavaScript() const core/fpdfdoc/cpdf_action.cpp:136:29
    #4 0x55fa7eb317dd in CPDFSDK_ActionHandler::ExecuteDocumentPageAction(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, std::__1::set<CPDF_Dictionary const*, std::__1::less<CPDF_Dictionary const*>, std::__1::allocator<CPDF_Dictionary const*> >*) fpdfsdk/cpdfsdk_actionhandler.cpp:134:32
    #5 0x55fa7eb31611 in CPDFSDK_ActionHandler::DoAction_Page(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*) fpdfsdk/cpdfsdk_actionhandler.cpp:67:10
    #6 0x55fa7eb71b18 in FORM_DoPageAAction fpdfsdk/fpdf_formfill.cpp:703:21
    #7 0x55fa7eb214ff in (anonymous namespace)::GetPageForIndex(_FPDF_FORMFILLINFO*, fpdf_document_t__*, int) samples/pdfium_test.cc:593:3
    #8 0x55fa7eb21899 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:611:20
    #9 0x55fa7eb1b559 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:879:9
    #10 0x55fa7eb18293 in main samples/pdfium_test.cc:1071:5

0x602000004597 is located 0 bytes to the right of 7-byte region [0x602000004590,0x602000004597)
allocated by thread T0 here:
    #0 0x55fa7eaebd82 in calloc /b/swarming/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cc:154:3
    #1 0x55fa7eb83ae8 in PartitionAllocGenericFlags third_party/base/allocator/partition_allocator/partition_alloc.h:397:30
    #2 0x55fa7eb83ae8 in FX_SafeAlloc(unsigned long, unsigned long) core/fxcrt/fx_memory.h:49
    #3 0x55fa7eb6bdda in FX_AllocOrDie(unsigned long, unsigned long) core/fxcrt/fx_memory.h:68:18
    #4 0x55fa7ee6652a in CPDF_StreamAcc::ReadRawStream() const core/fpdfapi/parser/cpdf_stream_acc.cpp:158:7
    #5 0x55fa7ee65cb4 in CPDF_StreamAcc::ProcessRawData() core/fpdfapi/parser/cpdf_stream_acc.cpp:102:51
    #6 0x55fa7ee65b4b in CPDF_StreamAcc::LoadAllData(bool, unsigned int, bool) core/fpdfapi/parser/cpdf_stream_acc.cpp:35:5
    #7 0x55fa7ee471be in CPDF_StreamAcc::LoadAllDataFiltered() core/fpdfapi/parser/cpdf_stream_acc.cpp:41:3
    #8 0x55fa7ee64f53 in CPDF_Stream::GetUnicodeText() const core/fpdfapi/parser/cpdf_stream.cpp:177:9
    #9 0x55fa7f11ad14 in CPDF_Action::GetJavaScript() const core/fpdfdoc/cpdf_action.cpp:136:29
    #10 0x55fa7eb317dd in CPDFSDK_ActionHandler::ExecuteDocumentPageAction(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*, std::__1::set<CPDF_Dictionary const*, std::__1::less<CPDF_Dictionary const*>, std::__1::allocator<CPDF_Dictionary const*> >*) fpdfsdk/cpdfsdk_actionhandler.cpp:134:32
    #11 0x55fa7eb31611 in CPDFSDK_ActionHandler::DoAction_Page(CPDF_Action const&, CPDF_AAction::AActionType, CPDFSDK_FormFillEnvironment*) fpdfsdk/cpdfsdk_actionhandler.cpp:67:10
    #12 0x55fa7eb71b18 in FORM_DoPageAAction fpdfsdk/fpdf_formfill.cpp:703:21
    #13 0x55fa7eb214ff in (anonymous namespace)::GetPageForIndex(_FPDF_FORMFILLINFO*, fpdf_document_t__*, int) samples/pdfium_test.cc:593:3
    #14 0x55fa7eb21899 in (anonymous namespace)::RenderPage(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, fpdf_document_t__*, fpdf_form_handle_t__*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:611:20
    #15 0x55fa7eb1b559 in (anonymous namespace)::RenderPdf(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&) samples/pdfium_test.cc:879:9
    #16 0x55fa7eb18293 in main samples/pdfium_test.cc:1071:5

SUMMARY: AddressSanitizer: heap-buffer-overflow core/fpdfapi/parser/fpdf_parser_decode.cpp:34:26 in (anonymous namespace)::GetUnicodeFromBigEndianBytes(unsigned char const*)
Shadow bytes around the buggy address:
  0x0c047fff8860: fa fa 00 04 fa fa 00 04 fa fa 00 04 fa fa 00 04
  0x0c047fff8870: fa fa 00 04 fa fa fd fa fa fa 04 fa fa fa fd fa
  0x0c047fff8880: fa fa 04 fa fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c047fff8890: fa fa fd fd fa fa 04 fa fa fa 00 fa fa fa 00 00
  0x0c047fff88a0: fa fa 00 fa fa fa 00 fa fa fa fc fc fa fa 01 fa
=>0x0c047fff88b0: fa fa[07]fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff88c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff88d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff88e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff88f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff8900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 76.0.3809.133  Channel: stable
OS Version: 
Flash Version:

## Attachments

- [chromium-1001159.pdf](attachments/chromium-1001159.pdf) (application/pdf, 122 B)

## Timeline

### pd...@gmail.com (2019-09-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-09-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6198144328400896.

### cl...@chromium.org (2019-09-05)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-09-05)

Automatically assigning owner based on suspected regression changelist https://pdfium.googlesource.com/pdfium/+/15f1a88dece664ae7300d9a60fe124cec1f2b9de (Properly handle language markers in decoded text).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-09-05)

Detailed Report: https://clusterfuzz.com/testcase?key=6198144328400896

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x609000056727
Crash State:
  GetUnicodeFromBigEndianBytes
  PDF_DecodeText
  CPDF_Stream::GetUnicodeText
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=585329:585343

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6198144328400896

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### th...@chromium.org (2019-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-09)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/1d3ff52a37c75d29c7d08483a042ef33266a9baf

commit 1d3ff52a37c75d29c7d08483a042ef33266a9baf
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Sep 09 18:37:48 2019

Fix out of bound read in PDF_DecodeText().

Add unit test for PDF_DecodeText() with basic test cases and test cases
for handling escape sequences. Also use size_t consistently.

Bug: chromium:1001159
Change-Id: I6e8750ce90fdd6cf6e5b2eff35bcdc89f28fc6c5
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/60310
Reviewed-by: Chris Palmer <palmer@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/1d3ff52a37c75d29c7d08483a042ef33266a9baf/core/fpdfapi/parser/fpdf_parser_decode.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/1d3ff52a37c75d29c7d08483a042ef33266a9baf/core/fpdfapi/parser/fpdf_parser_decode_unittest.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c5f8cf9eb92c136fe4a57c377ddf73e86d765e5d

commit c5f8cf9eb92c136fe4a57c377ddf73e86d765e5d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Sep 09 20:09:13 2019

Roll src/third_party/pdfium eb590e0e22e9..1d3ff52a37c7 (3 commits)

https://pdfium.googlesource.com/pdfium.git/+log/eb590e0e22e9..1d3ff52a37c7

git log eb590e0e22e9..1d3ff52a37c7 --date=short --no-merges --format='%ad %ae %s'
2019-09-09 thestig@chromium.org Fix out of bound read in PDF_DecodeText().
2019-09-09 bebeaudr@microsoft.com PDF a11y: new API for font-weight
2019-09-07 thestig@chromium.org Simplify CPDF_CMap ctor.

Created with:
  gclient setdep -r src/third_party/pdfium@1d3ff52a37c7

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:1001159,chromium:985604
Change-Id: Ib6fc0b8abd36d50385d4509937a90eb1c28f455f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1793234
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#694882}

[modify] https://crrev.com/c5f8cf9eb92c136fe4a57c377ddf73e86d765e5d/DEPS


### th...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-09-10)

ClusterFuzz testcase 6198144328400896 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=694867:694904

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### th...@chromium.org (2019-09-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-10)

This bug requires manual review: We don't branch M78 until 2019-09-05.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-09-10)

[Empty comment from Monorail migration]

### sr...@google.com (2019-09-10)

Merge approved for M78, branch:3904

### th...@chromium.org (2019-09-10)

M78 merge: https://pdfium.googlesource.com/pdfium/+/b93ec9bf15bbab33c46f7c1296f11965dbb15836

Will request M77 merge soon too.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-10)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/b93ec9bf15bbab33c46f7c1296f11965dbb15836

commit b93ec9bf15bbab33c46f7c1296f11965dbb15836
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Sep 10 20:11:15 2019

M78: Fix out of bound read in PDF_DecodeText().

Add unit test for PDF_DecodeText() with basic test cases and test cases
for handling escape sequences. Also use size_t consistently.

Bug: chromium:1001159
Change-Id: I6e8750ce90fdd6cf6e5b2eff35bcdc89f28fc6c5
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/60310
Reviewed-by: Chris Palmer <palmer@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
(cherry picked from commit 1d3ff52a37c75d29c7d08483a042ef33266a9baf)
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/60434
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/b93ec9bf15bbab33c46f7c1296f11965dbb15836/core/fpdfapi/parser/fpdf_parser_decode.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/b93ec9bf15bbab33c46f7c1296f11965dbb15836/core/fpdfapi/parser/fpdf_parser_decode_unittest.cpp


### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-09-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-12)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-09-16)

+lakpamarthy

This security fix covers a corner case and should have no impact on anything else.

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $2,000 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-27)

We will target this in M78.

### th...@chromium.org (2019-10-08)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-12-18)

This issue was migrated from crbug.com/chromium/1001159?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1011642]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050063)*
