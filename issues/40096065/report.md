# Security: [xfa] pdfium SEGV on RelocateTableRowCells

| Field | Value |
|-------|-------|
| **Issue ID** | [40096065](https://issues.chromium.org/issues/40096065) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | qu...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2019-08-22 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Pdfium Out-Of-Bounds Read on RelocateTableRowCells

**VERSION**  

commit 60044886a39365bbf10be7f8894a71dcd3275794  

Date: Thu Aug 22 10:29:04 UTC 2019

**REPRODUCTION CASE**

The attached proof-of-concept file could crash the latest build of pdfium\_test.  

This is an Out-Of-Bounds Read issue.

- build pdfium\_test with ASAN, XFA is enabled
- Open attached file.

ADDITIONAL INFORMATION

# Rendering PDF file result/crash/RelocateTableRowCells.pdf.

==10497==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000051454 at pc 0x5648c1ada630 bp 0x7fff3b03ec10 sp 0x7fff3b03ec08  

READ of size 4 at 0x602000051454 thread T0  

#0 0x5648c1ada62f in (anonymous namespace)::RelocateTableRowCells(fxcrt::RetainPtr<CXFA\_ContentLayoutItem> const&, std::\_\_1::vector<float, std::\_\_1::allocator<float> > const&, XFA\_AttributeValue) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:231:24  

#1 0x5648c1ad89d4 in CXFA\_ContentLayoutProcessor::DoLayoutTableContainer(CXFA\_Node\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1311:9  

#2 0x5648c1ad606b in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2077:11  

#3 0x5648c1ae5be3 in CXFA\_ContentLayoutProcessor::InsertFlowedItem(CXFA\_ContentLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<fxcrt::RetainPtr<CXFA\_ContentLayoutItem>, std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> > > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_ContentLayoutProcessor::Context\*, bool) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2354:29  

#4 0x5648c1ae2338 in CXFA\_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_ContentLayoutProcessor::Context\*, bool) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1795:23  

#5 0x5648c1ad5fdc in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2066:18  

#6 0x5648c1ad317d in CXFA\_ContentLayoutProcessor::DoLayout(bool, float, float) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2045:10  

#7 0x5648c1b018f0 in CXFA\_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa\_layoutprocessor.cpp:80:36  

#8 0x5648c1878e94 in CXFA\_FFDocView::DoLayout() xfa/fxfa/cxfa\_ffdocview.cpp:98:30  

#9 0x5648c1d0b7e5 in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:129:18  

#10 0x5648bd61eb5c in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:260:32  

#11 0x5648bd480841 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:841:12  

#12 0x5648bd47c119 in main samples/pdfium\_test.cc:1068:5  

#13 0x7fd3b5f3eb96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

0x602000051454 is located 0 bytes to the right of 4-byte region [0x602000051450,0x602000051454)  

allocated by thread T0 here:  

#0 0x5648bd4787bd in operator new(unsigned long) /b/swarming/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cc:99:3  

#1 0x5648bd48aeb8 in std::\_\_1::\_\_libcpp\_allocate(unsigned long, unsigned long) buildtools/third\_party/libc++/trunk/include/new:238:10  

#2 0x5648bd4bad57 in std::\_\_1::allocator<float>::allocate(unsigned long, void const\*) buildtools/third\_party/libc++/trunk/include/memory:1813:37  

#3 0x5648bd4bac20 in std::\_\_1::allocator\_traits<std::\_\_1::allocator<float> >::allocate(std::\_\_1::allocator<float>&, unsigned long) buildtools/third\_party/libc++/trunk/include/memory:1546:21  

#4 0x5648bd4ba34e in std::\_\_1::\_\_split\_buffer<float, std::\_\_1::allocator<float>&>::\_\_split\_buffer(unsigned long, unsigned long, std::\_\_1::allocator<float>&) buildtools/third\_party/libc++/trunk/include/\_\_split\_buffer:311:29  

#5 0x5648bd4b9aa7 in void std::\_\_1::vector<float, std::\_\_1::allocator<float> >::\_\_push\_back\_slow\_path<float>(float&&) buildtools/third\_party/libc++/trunk/include/vector:1622:49  

#6 0x5648bd4b4a22 in std::\_\_1::vector<float, std::\_\_1::allocator<float> >::push\_back(float&&) buildtools/third\_party/libc++/trunk/include/vector:1663:9  

#7 0x5648c1ad73f5 in CXFA\_ContentLayoutProcessor::DoLayoutTableContainer(CXFA\_Node\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1171:33  

#8 0x5648c1ad606b in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2077:11  

#9 0x5648c1ae5be3 in CXFA\_ContentLayoutProcessor::InsertFlowedItem(CXFA\_ContentLayoutProcessor\*, bool, bool, float, XFA\_AttributeValue, unsigned char\*, std::\_\_1::vector<fxcrt::RetainPtr<CXFA\_ContentLayoutItem>, std::\_\_1::allocator<fxcrt::RetainPtr<CXFA\_ContentLayoutItem> > > (&) [3], bool, float, float, float, float\*, float\*, float\*, bool\*, bool\*, CXFA\_ContentLayoutProcessor::Context\*, bool) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2354:29  

#10 0x5648c1ae2338 in CXFA\_ContentLayoutProcessor::DoLayoutFlowedContainer(bool, XFA\_AttributeValue, float, float, CXFA\_ContentLayoutProcessor::Context\*, bool) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:1795:23  

#11 0x5648c1ad5fdc in CXFA\_ContentLayoutProcessor::DoLayoutInternal(bool, float, float, CXFA\_ContentLayoutProcessor::Context\*) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2066:18  

#12 0x5648c1ad317d in CXFA\_ContentLayoutProcessor::DoLayout(bool, float, float) xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:2045:10  

#13 0x5648c1b018f0 in CXFA\_LayoutProcessor::DoLayout() xfa/fxfa/layout/cxfa\_layoutprocessor.cpp:80:36  

#14 0x5648c1878e94 in CXFA\_FFDocView::DoLayout() xfa/fxfa/cxfa\_ffdocview.cpp:98:30  

#15 0x5648c1d0b7e5 in CPDFXFA\_Context::LoadXFADoc() fpdfsdk/fpdfxfa/cpdfxfa\_context.cpp:129:18  

#16 0x5648bd61eb5c in FPDF\_LoadXFA fpdfsdk/fpdf\_view.cpp:260:32  

#17 0x5648bd480841 in (anonymous namespace)::RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, (anonymous namespace)::Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) samples/pdfium\_test.cc:841:12  

#18 0x5648bd47c119 in main samples/pdfium\_test.cc:1068:5  

#19 0x7fd3b5f3eb96 in \_\_libc\_start\_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

SUMMARY: AddressSanitizer: heap-buffer-overflow xfa/fxfa/layout/cxfa\_contentlayoutprocessor.cpp:231:24 in (anonymous namespace)::RelocateTableRowCells(fxcrt::RetainPtr<CXFA\_ContentLayoutItem> const&, std::\_\_1::vector<float, std::\_\_1::allocator<float> > const&, XFA\_AttributeValue)  

Shadow bytes around the buggy address:  

0x0c0480002230: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480002240: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480002250: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480002260: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0c0480002270: fa fa fd fd fa fa 00 00 fa fa 00 fa fa fa 00 fa  

=>0x0c0480002280: fa fa 00 fa fa fa fd fa fa fa[04]fa fa fa 00 00  

0x0c0480002290: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c04800022a0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0c04800022b0: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fa  

0x0c04800022c0: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd  

0x0c04800022d0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

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

Shadow gap: cc  

==10497==ABORTING

**CREDIT INFORMATION**  

Quang Nguyen(@quangnh89) from Viettel Cyber Security

## Attachments

- [RelocateTableRowCells.pdf](attachments/RelocateTableRowCells.pdf) (application/pdf, 1.5 KB)
- [RelocateTableRowCells.patch](attachments/RelocateTableRowCells.patch) (text/plain, 586 B)

## Timeline

### cl...@chromium.org (2019-08-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5740715367071744.

### cl...@chromium.org (2019-08-22)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-08-22)

Detailed Report: https://clusterfuzz.com/testcase?key=5740715367071744

Fuzzing Engine: libFuzzer
Fuzz Target: pdfium_xfa_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x6090000ba264
Crash State:
  RelocateTableRowCells
  CXFA_ContentLayoutProcessor::DoLayoutTableContainer
  CXFA_ContentLayoutProcessor::DoLayoutInternal
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=555504:555559

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5740715367071744

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ts...@chromium.org (2019-08-22)

XFA is not shipped

### qu...@gmail.com (2019-08-23)

[Comment Deleted]

### qu...@gmail.com (2019-08-23)

ADDITIONAL ANALYSIS

File `pdfium\xfa\fxfa\layout\cxfa_contentlayoutprocessor.cpp`
Function: RelocateTableRowCells

`RelocateTableRowCells` reads `nColSpan` value from XFA form (line 216). Notice that, both `nOriginalColSpan` and `nCurrentColIdx` are signed integers (int32_t). When `nCurrentColIdx` is equal to 1 and `nColSpan` is equal to 2147483647, `nCurrentColIdx + nColSpan` == -2147483648, an integer overflow vulnerability. And then, `nColSpan` is used to access elements in `rgSpecifiedColumnWidths`, an Out-Of-Bounds-Access issue will occur.

```
void RelocateTableRowCells(const RetainPtr<CXFA_ContentLayoutItem>& pLayoutRow,
                           const std::vector<float>& rgSpecifiedColumnWidths,
                           XFA_AttributeValue eLayout) {
  /////........

  for (CXFA_LayoutItem* pIter = pLayoutRow->GetFirstChild(); pIter;
       pIter = pIter->GetNextSibling()) {
    CXFA_ContentLayoutItem* pLayoutChild = pIter->AsContentLayoutItem();
    if (!pLayoutChild)
      continue;

	// `nOriginalColSpan` is obtained
    int32_t nOriginalColSpan =
        pLayoutChild->GetFormNode()->JSObject()->GetInteger(
            XFA_Attribute::ColSpan);
    if (nOriginalColSpan <= 0 && nOriginalColSpan != -1)
      continue;

    int32_t nColSpan = nOriginalColSpan;
    float fColSpanWidth = 0;
    if (nColSpan == -1 ||
        nCurrentColIdx + nColSpan >
            pdfium::CollectionSize<int32_t>(rgSpecifiedColumnWidths)) {         // << BUG HERE, integer overflow vulnerability
      nColSpan = pdfium::CollectionSize<int32_t>(rgSpecifiedColumnWidths) -
                 nCurrentColIdx;
    }
	
    for (int32_t i = 0; i < nColSpan; i++)
      fColSpanWidth += rgSpecifiedColumnWidths[nCurrentColIdx + i];

```

### qu...@gmail.com (2019-08-23)

Patch for this issue:

```

--- a/xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp
+++ b/xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp
@@ -222,8 +222,8 @@
     int32_t nColSpan = nOriginalColSpan;
     float fColSpanWidth = 0;
     if (nColSpan == -1 ||
-        nCurrentColIdx + nColSpan >
-            pdfium::CollectionSize<int32_t>(rgSpecifiedColumnWidths)) {
+        (uint32_t)nCurrentColIdx + (uint32_t)nColSpan >
+            pdfium::CollectionSize<uint32_t>(rgSpecifiedColumnWidths)) {
       nColSpan = pdfium::CollectionSize<int32_t>(rgSpecifiedColumnWidths) -
                  nCurrentColIdx;
     }

```

### th...@chromium.org (2019-08-23)

note: We don't take patches on the issue tracker. See https://pdfium.googlesource.com/pdfium/+/master/README.md#contributing-code if you'd like to contribute a patch. Otherwise, let me know and I can fix this.

### th...@chromium.org (2019-08-23)

Putting on my code reviewer hat, I probably won't take that patch as is.

### th...@chromium.org (2019-08-24)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-08-24)

[Empty comment from Monorail migration]

### qu...@gmail.com (2019-09-14)

Hi everyone,
Do you re-check this issue to confirm and review my patch?

### th...@chromium.org (2019-09-18)

re: https://crbug.com/chromium/996770#c12 - Can do. What happened was you uploaded patch set 4, but that did not generate a new email. In this case, the missing step in the CL review workflow is you could have replied to the comment on https://pdfium-review.googlesource.com/c/pdfium/+/59950/3/xfa/fxfa/layout/cxfa_contentlayoutprocessor.cpp#225, which would have generated an email, and the reviewers would have a signal to revisit the CL.

### cl...@chromium.org (2019-10-17)

Automatically adding ccs based on OWNERS file / target commit history.

If this is incorrect, please add the ClusterFuzz-Wrong label.

### qu...@gmail.com (2020-05-08)

Hi everyone,
Do you re-check this issue to confirm and review my patch? Should we close this issue?


### cl...@chromium.org (2020-08-19)

ClusterFuzz testcase 5740715367071744 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=799568:799569

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### th...@chromium.org (2020-08-20)

There's still an out of bound std::vector access.

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### aj...@google.com (2021-02-19)

Is this still Security_Impact-None now that XFA is shipping? Does anyone fancy being assigned?

### aj...@google.com (2021-02-23)

tsepez? https://crbug.com/chromium/996770#c20 ?

### ts...@chromium.org (2021-02-23)

Will become impact_stable as this ships, but I thought this was fixed. No longer reproducing after moving to cppgc it would seem.  But that doesn't square with c17.  

### ts...@chromium.org (2021-02-23)

Probably reappeared as https://crbug.com/1164158

### ts...@chromium.org (2021-02-23)

And confirmed fixed by https://pdfium.googlesource.com/pdfium/+/f3b585e8edf5b271445c1ef7ce07f461e87a038f

### [Deleted User] (2021-02-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-24)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-04)

Congratulations, Quang! The VRP Panel has decided to award you $5,000 for this report. Nice work! 

### qu...@gmail.com (2021-03-04)

Wow! Thank you so much! You just made my day!

### am...@google.com (2021-03-04)

 Hey Quang -- yay! That's super great to hear! Thank you for your work and helping make Chrome more secure for everyone! 

### am...@google.com (2021-03-05)

[Empty comment from Monorail migration]

### qu...@gmail.com (2021-03-12)

[Comment Deleted]

### qu...@gmail.com (2021-03-12)

Hi I want to update credit information:
Reporter credit: Quang Nguyen(@quangnh89) from Viettel Cyber Security and Nguyen Phuong.

Thanks and best regards

### am...@google.com (2021-03-12)

Hello, Quang. I'll update our information so that this full credit will be reflected in the release notes once this fix is included in a release. Thank you and congrats again to you and Nguyen. 

### [Deleted User] (2021-06-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-07-09)

Quang, thanks for getting in touch to ask about CVEs.

CVE rules say we can only allocate CVEs for bugs which affect the shipping product. As XFA is disabled by default, we can't allocate a CVE. Amy is OOO this week and it's possible that there's something special about XFA which I don't understand, so she may contradict me next week - but I doubt it. Sorry about that!

### qu...@gmail.com (2021-07-10)

Many thanks for the prompt reply. Yes, your answer is very clear to me. I don’t have anymore questions.

Best regards


### is...@google.com (2021-07-10)

This issue was migrated from crbug.com/chromium/996770?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40096065)*
