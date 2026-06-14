# pdfium: global-buffer-overflow in CFX_BidiLine::ResolveImplicit

| Field | Value |
|-------|-------|
| **Issue ID** | [40091293](https://issues.chromium.org/issues/40091293) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | pd...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2018-05-04 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.70 Safari/537.36

Steps to reproduce the problem:
(This is in pdfium XFA, for which I noticed Google is also giving security rewards.)

==7507==ERROR: AddressSanitizer: global-buffer-overflow on address 0x0000003750b0 at pc 0x00000119aed9 bp 0x7ffd3f90efe0 sp 0x7ffd3f90efd8
READ of size 4 at 0x0000003750b0 thread T0
SCARINESS: 27 (4-byte-read-global-buffer-overflow-far-from-bounds)
    #0 0x119aed8 in (anonymous namespace)::CFX_BidiLine::ResolveImplicit(std::__1::vector<CFX_Char, std::__1::allocator<CFX_Char> >*, unsigned long) ../../core/fxcrt/fx_bidi.cpp:451:17
    #1 0x1179a63 in (anonymous namespace)::CFX_BidiLine::BidiLine(std::__1::vector<CFX_Char, std::__1::allocator<CFX_Char> >*, unsigned long) ../../core/fxcrt/fx_bidi.cpp:244:5
    #2 0x1ac9b8a in CFX_TxtBreak::EndBreak_BidiLine(std::__1::deque<FX_TPO, std::__1::allocator<FX_TPO> >*, CFX_BreakType) ../../xfa/fgas/layout/cfx_txtbreak.cpp:309:5
    #3 0x1ac688d in CFX_TxtBreak::EndBreak(CFX_BreakType) ../../xfa/fgas/layout/cfx_txtbreak.cpp:499:5
    #4 0x1a77792 in CFDE_TextOut::CalcLogicSize(fxcrt::WideString const&, CFX_RectF&) ../../xfa/fde/cfde_textout.cpp:235:32
    #5 0x1a819d1 in CFDE_TextOut::CalcLogicSize(fxcrt::WideString const&, CFX_STemplate<float>&) ../../xfa/fde/cfde_textout.cpp:199:3
    #6 0x1c596b6 in CXFA_Node::CalculateTextContentSize(CXFA_FFDoc*, CFX_STemplate<float>&) ../../xfa/fxfa/parser/cxfa_node.cpp:2846:27
    #7 0x1c59ef0 in CXFA_Node::CalculateTextEditAutoSize(CXFA_FFDoc*, CFX_STemplate<float>&) ../../xfa/fxfa/parser/cxfa_node.cpp:2898:3
    #8 0x1c5dff5 in CXFA_Node::CalculateAccWidthAndHeight(CXFA_FFDoc*, float&, float&) ../../xfa/fxfa/parser/cxfa_node.cpp:3114:7
    #9 0x1c5d3a1 in CXFA_Node::StartWidgetLayout(CXFA_FFDoc*, float&, float&) ../../xfa/fxfa/parser/cxfa_node.cpp:3084:7
    #10 0x1c268a2 in CXFA_ItemLayoutProcessor::DoLayoutField() ../../xfa/fxfa/parser/cxfa_itemlayoutprocessor.cpp:2197:12
    #11 0x1c10896 in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) ../../xfa/fxfa/parser/cxfa_itemlayoutprocessor.cpp:2242:7
    #12 0x1c214b7 in CXFA_ItemLayoutProcessor::InsertFlowedItem(CXFA_ItemLayoutProcessor*, bool, bool, float, XFA_AttributeEnum, unsigned char*, std::__1::vector<CXFA_ContentLayoutItem*, std::__1::allocator<CXFA_ContentLayoutItem*> > (&) [3], bool, float, float, float, float*, float*, float*, bool*, bool*, CXFA_LayoutContext*, bool) ../../xfa/fxfa/parser/cxfa_itemlayoutprocessor.cpp:2524:29
    #13 0x1c1dd4b in CXFA_ItemLayoutProcessor::DoLayoutFlowedContainer(bool, XFA_AttributeEnum, float, float, CXFA_LayoutContext*, bool) ../../xfa/fxfa/parser/cxfa_itemlayoutprocessor.cpp:1958:46
    #14 0x1c10a2a in CXFA_ItemLayoutProcessor::DoLayout(bool, float, float, CXFA_LayoutContext*) ../../xfa/fxfa/parser/cxfa_itemlayoutprocessor.cpp:2224:18
    #15 0x1c367b7 in CXFA_LayoutProcessor::DoLayout() ../../xfa/fxfa/parser/cxfa_layoutprocessor.cpp:74:43
    #16 0x1b4846d in CXFA_FFDocView::DoLayout() ../../xfa/fxfa/cxfa_ffdocview.cpp:94:30
    #17 0x179d507 in CPDFXFA_Context::LoadXFADoc() ../../fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:113:18
    #18 0x11285dc in FPDF_LoadXFA ../../fpdfsdk/fpdf_view.cpp:251:63

0x0000003750b0 is located 16 bytes to the left of global variable 'prefix' defined in '../../core/fxcrt/fx_string.cpp:40:28' (0x3750c0) of size 5
0x0000003750b0 is located 16 bytes to the right of global variable '(anonymous namespace)::gc_FX_BidiAddLevel' defined in '../../core/fxcrt/fx_bidi.cpp:228:15' (0x375080) of size 32

The actual bug is elsewhere, with its effect noted by UBSAN in an earlier function.

../../core/fxcrt/fx_bidi.cpp:370:17: runtime error: index 13 out of bounds for type 'const int32_t [10]'
    #0 0x1357511 in (anonymous namespace)::CFX_BidiLine::ResolveWeak(std::__1::vector<CFX_Char, std::__1::allocator<CFX_Char> >*, unsigned long) ../../core/fxcrt/fx_bidi.cpp:370:17
    #1 0x1356983 in (anonymous namespace)::CFX_BidiLine::BidiLine(std::__1::vector<CFX_Char, std::__1::allocator<CFX_Char> >*, unsigned long) ../../core/fxcrt/fx_bidi.cpp:242:5
    #2 0x13568dc in FX_BidiLine(std::__1::vector<CFX_Char, std::__1::allocator<CFX_Char> >*, unsigned long) ../../core/fxcrt/fx_bidi.cpp:617:7

The order of events in CFX_BidiLine::BidiLine is as follows.

    Classify(chars, iCount, false); // <- sets m_iBidiClass on chars[1]
    ResolveExplicit(chars, iCount);
    ResolveWeak(chars, iCount); // <-- UBSAN report
    ResolveNeutrals(chars, iCount);
    ResolveImplicit(chars, iCount); // <-- ASAN report

What is the expected behavior?

What went wrong?
^

Did this work before? N/A 

Chrome version: 66.0.3359.70  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [chromium-839695.pdf](attachments/chromium-839695.pdf) (application/pdf, 310 B)
- [chromium-839695-1.pdf](attachments/chromium-839695-1.pdf) (application/pdf, 310 B)

## Timeline

### pd...@gmail.com (2018-05-04)

[Empty comment from Monorail migration]

### pd...@gmail.com (2018-05-04)

There is also an unrelated UBSAN report for the same PDF, which I think is bogus.

../../core/fxcrt/fx_arabic.cpp:143:32: runtime error: index 1602 out of bounds for type 'const (anonymous namespace)::FX_ARBFORMTABLE [180]'
    #0 0x1a7dd47 in (anonymous namespace)::GetArabicFormTable(wchar_t) ../../core/fxcrt/fx_arabic.cpp:143:32

This fixes the report.

-  return g_FX_ArabicFormTables + unicode - 0x622;
+  return g_FX_ArabicFormTables + (unicode - 0x622);

### ts...@chromium.org (2018-05-04)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2018-05-04)

In debug builds, it's failing the "iClsCur <= FX_BIDICLASS_BN" assertion.

### th...@chromium.org (2018-05-04)

If the code actually checks the value instead of doing an assert, then it needs to do the same in ResolveNeutrals() and ResolveImplicit() for the given test case. Not sure if that's the right answer or if the code should do something different in Classify() in the first place.

We should add unit tests for FX_BidiLine(), and maybe even a fuzzer.

### pd...@gmail.com (2018-05-05)

I don't know what the bug is exactly, or rather how it should be fixed, but I can explain where the bug is.

There are three characters in the string. In Classify, each is assigned m_BidiClass (later referred to by iCls*) with the following operation.

(cur.char_props() & FX_BIDICLASSBITSMASK) >> FX_BIDICLASSBITS

https://cs.chromium.org/chromium/src/third_party/pdfium/core/fxcrt/fx_bidi.cpp?l=315&rcl=36b3d19281e2911a97d6ce84538a3ae575ac38a7

And char_props() is read in earlier as dwProps in AppendChar. FX_GetUnicodeProperties just looks up the value in a large table.

uint32_t dwProps = FX_GetUnicodeProperties(wch);

https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fgas/layout/cfx_txtbreak.cpp?l=228&rcl=36b3d19281e2911a97d6ce84538a3ae575ac38a7

And the second character, \x1D returns char_props() that results in m_BidiClass == 13, which is outside of the asserted range of 0-10 (and 1-5 later).

Now the interesting part is why three characters are necessary to trigger the bug, rather than just that character.

The first character gets into the code path that calls FX_BidiLine in EndBreak_BidiLine.

https://cs.chromium.org/chromium/src/third_party/pdfium/xfa/fgas/layout/cfx_txtbreak.cpp?l=320&rcl=36b3d19281e2911a97d6ce84538a3ae575ac38a7

The second character is explained above, but what about the third? In EndBreak_BidiLine, the following code.

    size_t iBidiNum = 0;
    for (size_t i = 0; i < static_cast<size_t>(iCount); ++i) {
      pTC = &chars[i];
      pTC->m_iBidiPos = static_cast<int32_t>(i);
      if (pTC->GetCharType() != FX_CHARTYPE_Control)
        iBidiNum = i;
      if (i == 0)
        pTC->m_iBidiLevel = 1;
    }
    FX_BidiLine(&chars, iBidiNum + 1); // <-- iBidiNum + 1 == count of chars FX_BidiLine processes

The effect of the above loop is that if the last character of the line is of type FX_CHARTYPE_Control (which \x1D is), then it is not processed by FX_BidiLine. So an additional non-FX_CHARTYPE_Control character is necessary.

I don't know why it's only ignored when it's last, or if that's the bug.

### pd...@gmail.com (2018-05-05)

Minor addition: multiple FX_CHARTYPE_Control characters in last position are also ignored.

### pd...@gmail.com (2018-05-05)

[Comment Deleted]

### pd...@gmail.com (2018-05-07)

Using different characters triggers a similar ASAN report in CFX_BidiLine::ResolveNeutrals.

==646==ERROR: AddressSanitizer: global-buffer-overflow on address 0x00000035bd04 at pc 0x000000b306f2 bp 0x7ffd6e5117a0 sp 0x7ffd6e511798
READ of size 4 at 0x00000035bd04 thread T0
SCARINESS: 27 (4-byte-read-global-buffer-overflow-far-from-bounds)
    #0 0xb306f1 in (anonymous namespace)::CFX_BidiLine::ResolveNeutrals(std::__1::vector<CFX_Char, std::__1::allocator<CFX_Char> >*, unsigned long) ../../core/fxcrt/fx_bidi.cpp:418:17
...
0x00000035bd04 is located 28 bytes to the left of global variable '(anonymous namespace)::gc_FX_BidiNeutralStates' defined in '../../core/fxcrt/fx_bidi.cpp:211:15' (0x35bd20) of size 120
0x00000035bd04 is located 12 bytes to the right of global variable '(anonymous namespace)::gc_FX_BidiNeutralActions' defined in '../../core/fxcrt/fx_bidi.cpp:219:15' (0x35bc80) of size 120


### ds...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### pd...@gmail.com (2018-05-08)

I propose the following patch.

--- a/xfa/fgas/layout/cfx_txtbreak.cpp
+++ b/xfa/fgas/layout/cfx_txtbreak.cpp
@@ -110,6 +110,10 @@ CFX_BreakType CFX_TxtBreak::AppendChar_Control(CFX_Char* pCurChar) {
       case L'\f':
         dwRet = CFX_BreakType::Page;
         break;
+      case 0x1C:
+      case 0x1D:
+      case 0x1E:
+      case 0x85:
       case 0x2029:
         dwRet = CFX_BreakType::Paragraph;
         break;

There are 7 unicode characters with Bidi_Class Paragraph Separator. (B in 5th column.) pdfium refers to them as FX_BIDICLASS_B (13).

ftp://ftp.unicode.org/Public/UNIDATA/UnicodeData.txt

https://cs.chromium.org/chromium/src/third_party/pdfium/core/fxcrt/fx_bidi.cpp?l=34&rcl=967aa0793c0b0cf2722ec8720e9d797266a9fde7

pdfium currently handles 0x2029, 0x0A and 0x0D (the latter two are m_wParagraphBreakChar in the above switch) which all cause the layout code to break after those characters. And then the loop mentioned in the previous post causes those pending characters to not be processed by FX_BidiLine. The other 4 characters are not handled, don't break, are processed, and then cause the bug (or hit the assert).

Note that 0x85 doesn't actually trigger the bug with the above PDFs. It makes it not even reach any of this code. I assume it causes an earlier parser to fail somewhere.

### pd...@gmail.com (2018-05-08)

PS. The same code is in CFX_RTFBreak::AppendChar_Control.

### ds...@chromium.org (2018-05-08)

[Empty comment from Monorail migration]

### ds...@chromium.org (2018-05-09)

I wasn't able to repro the issue with the provided files but making a fuzzer found the assert pretty quickly. I added a test case which also triggers in:

https://pdfium-review.googlesource.com/c/pdfium/+/32191

### pd...@gmail.com (2018-05-09)

Unfortunately my patch doesn't quite fix the actual bug. It works for the attached PDFs, but there are other cases for which it doesn't. I didn't notice that m_wParagraphBreakChar is either 0x0A or 0x0D (set to 0x0A by default, and then changed to the first encountered in the string), so the other isn't matched.

--- a/xfa/fgas/layout/cfx_txtbreak.cpp
+++ b/xfa/fgas/layout/cfx_txtbreak.cpp
@@ -110,6 +110,12 @@ CFX_BreakType CFX_TxtBreak::AppendChar_Control(CFX_Char* pCurChar) {
       case L'\f':
         dwRet = CFX_BreakType::Page;
         break;
+      case 0x0A:
+      case 0x0D:
+      case 0x1C:
+      case 0x1D:
+      case 0x1E:
+      case 0x85:
       case 0x2029:
         dwRet = CFX_BreakType::Paragraph;
         break;

The purpose of m_wParagraphBreakChar is not clear to me. With the above patch, it appears useless.

### pd...@gmail.com (2018-05-09)

Have you tried a build with XFA enabled? I can reproduce with the above files and pdfium_test.

### ds...@chromium.org (2018-05-09)

Yes, I tried with XFA enabled.

### bu...@chromium.org (2018-05-10)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/5e0b271b69355b5692b6afd1cd2c04d08c3b380c

commit 5e0b271b69355b5692b6afd1cd2c04d08c3b380c
Author: Dan Sinclair <dsinclair@chromium.org>
Date: Thu May 10 21:21:05 2018

Fixup ASSERT in Bidi handling; Add bidi fuzzer.

This CL converts several asserts in the FX_Bidi code to continue instead
of asserting in the face of unexpected input.

A BIDI fuzzer has been added as well.

Bug: chromium:839695
Change-Id: If61f822bde7442c008d50be58f7cecffb6e5d658
Reviewed-on: https://pdfium-review.googlesource.com/32191
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: dsinclair <dsinclair@chromium.org>

[modify] https://crrev.com/5e0b271b69355b5692b6afd1cd2c04d08c3b380c/testing/libfuzzer/BUILD.gn
[add] https://crrev.com/5e0b271b69355b5692b6afd1cd2c04d08c3b380c/xfa/fgas/layout/cfx_txtbreak_unittest.cpp
[modify] https://crrev.com/5e0b271b69355b5692b6afd1cd2c04d08c3b380c/core/fxcrt/fx_bidi.cpp
[modify] https://crrev.com/5e0b271b69355b5692b6afd1cd2c04d08c3b380c/xfa/fgas/layout/cfx_break.h
[modify] https://crrev.com/5e0b271b69355b5692b6afd1cd2c04d08c3b380c/xfa/fgas/layout/cfx_rtfbreak_unittest.cpp
[modify] https://crrev.com/5e0b271b69355b5692b6afd1cd2c04d08c3b380c/xfa/fgas/layout/cfx_rtfbreak.h
[modify] https://crrev.com/5e0b271b69355b5692b6afd1cd2c04d08c3b380c/BUILD.gn
[add] https://crrev.com/5e0b271b69355b5692b6afd1cd2c04d08c3b380c/testing/libfuzzer/pdf_bidi_fuzzer.cc


### bu...@chromium.org (2018-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/777a737b6e980720bebdb535c7da9c5788999551

commit 777a737b6e980720bebdb535c7da9c5788999551
Author: pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Fri May 11 03:27:10 2018

Roll src/third_party/pdfium/ 5ad45e2f6..5e0b271b6 (1 commit)

https://pdfium.googlesource.com/pdfium.git/+log/5ad45e2f68bb..5e0b271b6935

$ git log 5ad45e2f6..5e0b271b6 --date=short --no-merges --format='%ad %ae %s'
2018-05-10 dsinclair Fixup ASSERT in Bidi handling; Add bidi fuzzer.

Created with:
  roll-dep src/third_party/pdfium
BUG=chromium:839695


The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=dsinclair@chromium.org

Change-Id: I8dd271c6d77f96e369f68a2be87e978a7211f9c4
Reviewed-on: https://chromium-review.googlesource.com/1054623
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#557777}
[modify] https://crrev.com/777a737b6e980720bebdb535c7da9c5788999551/DEPS


### ds...@chromium.org (2018-05-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-05-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b997d59c3a690405703ac5a4e69503d5325381f9

commit b997d59c3a690405703ac5a4e69503d5325381f9
Author: Dan Sinclair <dsinclair@chromium.org>
Date: Mon May 14 14:53:47 2018

Add pdf_bidi_fuzzer build

Bug: chromium:839695
Change-Id: I062d9a97559a4d26062e8a4932527765f06025a4
Reviewed-on: https://chromium-review.googlesource.com/1050584
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/heads/master@{#558306}
[modify] https://crrev.com/b997d59c3a690405703ac5a4e69503d5325381f9/pdf/pdfium/fuzzers/BUILD.gn


### sh...@chromium.org (2018-08-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-11-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-11-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-11-12)

Hi pdknsk@, the Chrome VRP panel decided this should be tracked as Medium severity, and awarded $1,000 for this report. Thanks!

### aw...@google.com (2018-11-12)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-12)

This issue was migrated from crbug.com/chromium/839695?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091293)*
