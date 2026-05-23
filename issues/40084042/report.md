# Security: PDFium Out-of-Bounds Read in CFX_FaceCache::RenderGlyph

| Field | Value |
|-------|-------|
| **Issue ID** | [40084042](https://issues.chromium.org/issues/40084042) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **CVE IDs** | CVE-2016-1685 |
| **Reporter** | st...@gmail.com |
| **Assignee** | oc...@chromium.org |
| **Created** | 2016-04-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The attached proof-of-concept file could crash the latest build of pdfium\_test.  

This is an Out-Of-Bounds Read issue.  

The exception information is presented as follows.

---

## Exception Information

(14e4.2bac): Access violation - code c0000005 (!!! second chance !!!)  

eax=80fcb76f ebx=0816afe8 ecx=80000001 edx=00002c13 esi=07f37f78 edi=07dd7fd8  

eip=00e2933c esp=003cf4cc ebp=003cf52c iopl=0 ov up ei ng nz ac pe cy  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010a97  

pdfium\_test!CFX\_FaceCache::RenderGlyph+0xec:  

00e2933c 0fbe08 movsx ecx,byte ptr [eax] ds:002b:80fcb76f=??

Here we can see that the process tried to read data from 0x80fcb76f. It's known to all that an user mode application cannot access memory address which is greater than 0x80000000.

---

## Stack Trace Information

0:000> k  

ChildEBP RetAddr  

003cf52c 00e291c6 pdfium\_test!CFX\_FaceCache::RenderGlyph+0xec [pdfium\core\fxge\ge\fx\_ge\_text.cpp @ 1571]  

003cf560 00e28d7b pdfium\_test!CFX\_FaceCache::LookUpGlyphBitmap+0xd6 [pdfium\core\fxge\ge\fx\_ge\_text.cpp @ 1306]  

003cf62c 00e25fd1 pdfium\_test!CFX\_FaceCache::LoadGlyphBitmap+0x14b [pdfium\core\fxge\ge\fx\_ge\_text.cpp @ 1407]  

003cf794 00d5faf8 pdfium\_test!CFX\_RenderDevice::DrawNormalText+0x521 [pdfium\core\fxge\ge\fx\_ge\_text.cpp @ 307]  

003cf7d8 00d6078b pdfium\_test!CPDF\_TextRenderer::DrawNormalText+0xc8 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_text.cpp @ 727]  

003cf870 00d46c64 pdfium\_test!CPDF\_RenderStatus::ProcessText+0x1eb [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_text.cpp @ 319]  

003cf890 00d451fc pdfium\_test!CPDF\_RenderStatus::ProcessObjectNoClip+0x34 [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 397]  

003cf8ac 00d44fee pdfium\_test!CPDF\_RenderStatus::ContinueSingleObject+0xec [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 339]  

003cf900 00d194f1 pdfium\_test!CPDF\_ProgressiveRenderer::Continue+0x2de [pdfium\core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 1103]  

003cf93c 00d19d99 pdfium\_test!FPDF\_RenderPage\_Retail+0x221 [pdfium\fpdfsdk\fpdfview.cpp @ 936]  

003cf978 00d13168 pdfium\_test!FPDF\_RenderPageBitmap+0x99 [pdfium\fpdfsdk\fpdfview.cpp @ 668]  

003cfa94 00d1355f pdfium\_test!RenderPage+0x1b8 [pdfium\samples\pdfium\_test.cc @ 452]  

003cfb6c 00d18696 pdfium\_test!RenderPdf+0x2ef [pdfium\samples\pdfium\_test.cc @ 628]  

003cfc50 00e5478d pdfium\_test!main+0x2e6 [pdfium\samples\pdfium\_test.cc @ 877]  

(Inline) -------- pdfium\_test!invoke\_main+0x1d [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 74]  

003cfc9c 7647338a pdfium\_test!\_\_scrt\_common\_main\_seh+0xff [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 264]  

003cfca8 76ef9a02 kernel32!BaseThreadInitThunk+0xe  

003cfce8 76ef99d5 ntdll!\_\_RtlUserThreadStart+0x70  

003cfd00 00000000 ntdll!\_RtlUserThreadStart+0x1b

The topmost stack frame is located at function CFX\_FaceCache::RenderGlyph().

---

## Source Code Analysis

1545 CFX\_GlyphBitmap\* CFX\_FaceCache::RenderGlyph(CFX\_Font\* pFont,  

1546 uint32\_t glyph\_index,  

1547 FX\_BOOL bFontStyle,  

1548 const CFX\_Matrix\* pMatrix,  

1549 int dest\_width,  

1550 int anti\_alias) {  

1551 if (!m\_Face) {  

1552 return NULL;  

1553 }  

1554 FXFT\_Matrix ft\_matrix;  

1555 ft\_matrix.xx = (signed long)(pMatrix->GetA() / 64 \* 65536);  

1556 ft\_matrix.xy = (signed long)(pMatrix->GetC() / 64 \* 65536);  

1557 ft\_matrix.yx = (signed long)(pMatrix->GetB() / 64 \* 65536);  

1558 ft\_matrix.yy = (signed long)(pMatrix->GetD() / 64 \* 65536);  

1559 FX\_BOOL bUseCJKSubFont = FALSE;  

1560 const CFX\_SubstFont\* pSubstFont = pFont->GetSubstFont();  

1561 if (pSubstFont) {  

1562 bUseCJKSubFont = pSubstFont->m\_bSubstOfCJK && bFontStyle;  

1563 int skew = 0;  

1564 if (bUseCJKSubFont) {  

1565 skew = pSubstFont->m\_bItlicCJK ? -15 : 0;  

1566 } else {  

1567 skew = pSubstFont->m\_ItalicAngle;  

1568 }  

1569 if (skew) {  

1570 // skew is nonpositive so -skew is used as the index.  

1571 skew = -skew <= static\_cast<int>(ANGLESKEW\_ARRAY\_SIZE) // Crashed at this line!  

1572 ? -58 // Crashed at this line!  

1573 : -g\_AngleSkew[-skew]; // Crashed at this line!  

1574 if (pFont->IsVertical())  

1575 ft\_matrix.yx += ft\_matrix.yy \* skew / 100;  

1576 else  

1577 ft\_matrix.xy += -ft\_matrix.xx \* skew / 100;  

1578 }  

1579 if (pSubstFont->m\_SubstFlags & FXFONT\_SUBST\_MM) {  

1580 pFont->AdjustMMParams(glyph\_index, dest\_width,  

1581 pFont->GetSubstFont()->m\_Weight);  

1582 }  

1583 }

0:000> dv  

this = 0x0816afe8  

pFont = 0x07f37f78  

glyph\_index = 0  

bFontStyle = 0n0  

pMatrix = 0x003cf6b0  

dest\_width = 0n615  

anti\_alias = 0n3  

bUseCJKSubFont = 0n0  

scoped\_transform = class `anonymous-namespace'::ScopedFontTransform  

load\_flags = <value unavailable>  

pDestBuf = <value unavailable>  

dest\_pitch = <value unavailable>  

pGlyphBitmap = <value unavailable>  

src\_pitch = <value unavailable>  

ft\_matrix = struct FT\_Matrix\_  

weight = <value unavailable>  

bmwidth = <value unavailable>  

error = <value unavailable>  

bmheight = <value unavailable>  

pSubstFont = 0x07dd7fd8  

pSrcBuf = <value unavailable>  

skew = 0n-2147483647 <- (ecx, 0x80000001)  

index = <value unavailable>  

level = <value unavailable>  

bytes = <value unavailable>  

n = <value unavailable>  

rowbytes = <value unavailable>

---

## Vulnerability Analysis

0:000> ub eip  

pdfium\_test!CFX\_FaceCache::RenderGlyph+0xd5 [pdfium\core\fxge\ge\fx\_ge\_text.cpp @ 1571]:  

00e29325 8bc1 mov eax,ecx  

00e29327 f7d8 neg eax  

00e29329 83f81e cmp eax,1Eh  

00e2932c 7f07 jg pdfium\_test!CFX\_FaceCache::RenderGlyph+0xe5 (00e29335)  

00e2932e b9c6ffffff mov ecx,0FFFFFFC6h  

00e29333 eb0c jmp pdfium\_test!CFX\_FaceCache::RenderGlyph+0xf1 (00e29341)  

00e29335 b870b7fc00 mov eax,offset pdfium\_test!g\_AngleSkew (00fcb770)  

00e2933a 2bc1 sub eax,ecx

0:000> db 00fcb770  

00fcb770 00 02 03 05 07 09 0b 0c-0e 10 12 13 15 17 19 1b ................  

00fcb780 1d 1f 20 22 24 26 28 2a-2d 2f 31 33 35 37 00 00 .. "$&(\*-/1357..  

00fcb790 00 03 06 07 08 09 0b 0c-0e 0f 10 11 12 13 14 15 ................  

00fcb7a0 16 17 18 19 1a 1b 1c 1d-1e 1f 20 21 22 23 23 24 .......... !"##$  

00fcb7b0 24 25 25 25 26 26 26 27-27 27 28 28 28 29 29 29 $%%%&&&'''((()))  

00fcb7c0 2a 2a 2a 2a 2b 2b 2b 2c-2c 2c 2c 2d 2d 2d 2d 2e \*\*\*\*+++,,,,----.  

00fcb7d0 2e 2e 2e 2f 2f 2f 2f 30-30 30 30 30 31 31 31 31 ...////000001111  

00fcb7e0 32 32 32 32 32 33 33 33-33 33 34 34 34 34 34 35 2222233333444445

Function CFX\_FaceCache::RenderGlyph starts from the 1545th line of file pdfium\core\fxge\ge\fx\_ge\_text.cpp. We can see that the type of skew is int and the value is -2147483647 (ecx, 0x80000001). It's no doublt that the expression g\_AngleSkew[-skew] will cause an Out-of-Bounds Read issue.

The value of g\_AngleSkew is 00fcb770. The value of skew can be controlled by the attacker! In the attached proof-of-concept file, the /ItalicAngle property of the 9th object was set to 2147483649 (0x80000001). You can change this value to anything you like. It seems that we can read data from arbitrary memory address.

9 0 obj  

<<  

/Type /FontDescriptor  

/FontName /GMTXSU+Calibri  

/FontBBox [0 -177 770 680]  

/Flags 4  

/Ascent 680  

/CapHeight 680  

/Descent -177  

/ItalicAngle 2147483649  

/StemV 115  

/MissingWidth 506  

/FontFile2 12 0 R

endobj

The /FontFile2 property of the 9th object is 12 0 R. The 12th object uses the /FlateDecode filter.

12 0 obj  

<<  

/Filter /FlateDecode  

/Length1 26888  

/Length 10903

To trigger this vulnerability, we should mutate the value of the compressed content. Here the 110th byte of the compressed content was changed from 0x37 to 0x39. The mutated compressed content cannot be decompressed normally (tested with zlib library delivered with python).I'm not sure how PDFium handle this situation.

stream  

78 9C ED 7D 09 7C 54 D5 D9 F7 39 F7 CE BE 64 F6  

C9 24 93 64 66 32 C9 24 61 B2 90 7D 21 24 43 36  

48 42 08 21 19 48 80 40 42 C2 AA 6C 01 64 11 14  

C1 35 8A BB 56 D4 BA B4 2A 56 14 26 C3 16 C4 56  

6C 51 5B 5B D4 BA B7 2E C5 B6 56 A4 62 B1 AD 2B  

26 F9 9E 73 9F 7B 30 F0 AA 5F DF 7E FD 7E 7D FB  

7D CC CD FF FE FF E7 39 CB DC FB 9C ED B9 [39] // 0x37 -> 0x39  

......  

endstream

---

## Patch Suggestion

Maybe we should check if the value of /ItalicAngle is valid or not.

---

## Credit

This vulnerability was discovered by Ke Liu of Tencent's Xuanwu LAB (<http://www.tencent.com/>).

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

PDFium Version: latest version built with Visual Studio 2015, both xfa and javascript were disabled.  

Operating System: [Windows 7 SP1]

**REPRODUCTION CASE**  

Both of the original normal pdf document and the mutated pdf document were attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

See at section VULNERABILITY DETAILS.

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### st...@gmail.com (2016-04-07)

Function CFX_Font::LoadGlyphPath() at line 1827 may also be vulnerable to issue.

### ke...@chromium.org (2016-04-08)

Thanks for the report.

ochang@: Are you available to look into this?

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2016-04-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5760321024688128

### cl...@chromium.org (2016-04-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6474405881839616

Fuzzer: ifratric_pdf_generic
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x0000907ca194
Crash State:
  CFX_FaceCache::RenderGlyph
  CFX_FaceCache::LookUpGlyphBitmap
  CFX_FaceCache::LoadGlyphBitmap
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=383194:384397

Minimized Testcase (215.17 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95ORS_teR00RaT7d7NdLBcg1xoin-8uBFAkvngjaVxdvi_DtSB6xeB_0h2KEfz4kJCitTrh7AzhQ-AD50zJgcsu35yW6TNVJ01pwLrtO9KpyYcAc-76Yrej-BSI45llt3WJ132AaplQuPPJ7CW_PV8c20TdM19rXcAJlVk6VlcfsE_0qpM

Filer: ochang

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### oc...@chromium.org (2016-04-08)

Looks like this was found by an internal fuzzer on April 1.

### oc...@chromium.org (2016-04-08)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-04-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5760321024688128

Uploader: ochang@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x0000907ca793
Crash State:
  CFX_FaceCache::RenderGlyph
  CFX_FaceCache::LookUpGlyphBitmap
  CFX_FaceCache::LoadGlyphBitmap
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=383194:384397

Minimized Testcase (13.98 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95gdtM9jVTcegWHIyCSiaXObmF0IrjvxGrxMyr1sKYp6D9Pc-sCErlD6zD19-vzKlbOmPMKFiZMp7_WIKtKKBVgLxWfPj9DCFgZgo_Al7H0kqs9sxjfrutKQoTXofVUWgF8edB0xfE0mkjcfu2Dzahf6uKzrw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2016-04-08)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-04-08)

Fixing impact/milestone.

### oc...@chromium.org (2016-04-11)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-04-11)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-04-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-11)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/b8627c9d13884d48943d8a7a5381eaf0bb2c08d9

commit b8627c9d13884d48943d8a7a5381eaf0bb2c08d9
Author: ochang <ochang@chromium.org>
Date: Mon Apr 11 20:47:41 2016

Fix integer issues leading to out of bounds access in fx_ge_text.cpp.

- Using |-skew| to get positive index, which doesn't work when skew is
  INT_MIN
- Incorrect logic when determining when to use |-skew| as an index.

R=tsepez@chromium.org,weili@chromium.org
BUG=chromium:601362

Review URL: https://codereview.chromium.org/1875673004

[modify] https://crrev.com/b8627c9d13884d48943d8a7a5381eaf0bb2c08d9/BUILD.gn
[modify] https://crrev.com/b8627c9d13884d48943d8a7a5381eaf0bb2c08d9/core/fxge/ge/fx_ge_text.cpp
[add] https://crrev.com/b8627c9d13884d48943d8a7a5381eaf0bb2c08d9/core/fxge/ge/fx_ge_text_embeddertest.cpp
[modify] https://crrev.com/b8627c9d13884d48943d8a7a5381eaf0bb2c08d9/pdfium.gyp
[add] https://crrev.com/b8627c9d13884d48943d8a7a5381eaf0bb2c08d9/testing/resources/bug_601362.pdf


### bu...@chromium.org (2016-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/96b1d62776fbe12940581493cb8537f2ba926bec

commit 96b1d62776fbe12940581493cb8537f2ba926bec
Author: ochang <ochang@chromium.org>
Date: Tue Apr 12 23:12:38 2016

Roll PDFium e5984e9..461129e

https://pdfium.googlesource.com/pdfium.git/+log/e5984e9..461129e

BUG=401189, 601362, 602046
TBR=tsepez@chromium.org

Review URL: https://codereview.chromium.org/1878943005

Cr-Commit-Position: refs/heads/master@{#386844}

[modify] https://crrev.com/96b1d62776fbe12940581493cb8537f2ba926bec/DEPS


### oc...@chromium.org (2016-04-12)

Requesting merge to 51 since this didn't make the cut.

### ti...@google.com (2016-04-12)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### cl...@chromium.org (2016-04-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-13)

ClusterFuzz has detected this issue as fixed in range 386714:386879.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5760321024688128

Uploader: ochang@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x0000907ca793
Crash State:
  CFX_FaceCache::RenderGlyph
  CFX_FaceCache::LookUpGlyphBitmap
  CFX_FaceCache::LoadGlyphBitmap
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=383194:384397
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=386714:386879

Minimized Testcase (13.98 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95gdtM9jVTcegWHIyCSiaXObmF0IrjvxGrxMyr1sKYp6D9Pc-sCErlD6zD19-vzKlbOmPMKFiZMp7_WIKtKKBVgLxWfPj9DCFgZgo_Al7H0kqs9sxjfrutKQoTXofVUWgF8edB0xfE0mkjcfu2Dzahf6uKzrw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-04-13)

ClusterFuzz has detected this issue as fixed in range 386714:386879.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6474405881839616

Fuzzer: ifratric_pdf_generic
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x0000907ca194
Crash State:
  CFX_FaceCache::RenderGlyph
  CFX_FaceCache::LookUpGlyphBitmap
  CFX_FaceCache::LoadGlyphBitmap
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=383194:384397
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=386714:386879

Minimized Testcase (215.17 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95ORS_teR00RaT7d7NdLBcg1xoin-8uBFAkvngjaVxdvi_DtSB6xeB_0h2KEfz4kJCitTrh7AzhQ-AD50zJgcsu35yW6TNVJ01pwLrtO9KpyYcAc-76Yrej-BSI45llt3WJ132AaplQuPPJ7CW_PV8c20TdM19rXcAJlVk6VlcfsE_0qpM

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-04-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5760321024688128

Uploader: ochang@google.com
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x0000907ca793
Crash State:
  CFX_FaceCache::RenderGlyph
  CFX_FaceCache::LookUpGlyphBitmap
  CFX_FaceCache::LoadGlyphBitmap
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=383194:384397
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=386714:386879

Minimized Testcase (13.98 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95gdtM9jVTcegWHIyCSiaXObmF0IrjvxGrxMyr1sKYp6D9Pc-sCErlD6zD19-vzKlbOmPMKFiZMp7_WIKtKKBVgLxWfPj9DCFgZgo_Al7H0kqs9sxjfrutKQoTXofVUWgF8edB0xfE0mkjcfu2Dzahf6uKzrw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ss...@google.com (2016-04-18)

Merge approved for M51 (branch 2704)

### go...@chromium.org (2016-04-18)

Please merge your change to M51 branch 2704 ASAP (before 6:00 PM PST, today) so we can take it in for M51 last Dev release tomorrow.

### bu...@chromium.org (2016-04-18)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=86732

------------------------------------------------------------------
r86732 | ochang@google.com | 2016-04-18T19:53:43.499907Z

-----------------------------------------------------------------

### ti...@google.com (2016-05-24)

Updating labels based on #22/#23

### ti...@google.com (2016-05-25)

Thanks for reporting this issue. Our reward panel decided to award you $1,000 for this report. Congratulations!

We've credited you in our release notes as "Ke Liu of Tencent's Xuanwu LAB": https://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html

Someone from our finance team will be in contact to collect details for payment within 7 days. If that doesn't happen, please either update this bug or contact me at timwillis@.

The CVE-ID for this issue is CVE-2016-1685. Usual boilerplate text below - let me know if you have any questions.

Thanks again for the report!


*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

### st...@gmail.com (2016-06-02)

Hi Timwillis, no one has contacted me so far.

### ti...@google.com (2016-06-02)

Thanks for letting me know - I'll chase today along with https://crbug.com/chromium/603518.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-20)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-04)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/a6b07058f9525c42b021f6f01d5e0da3215f46ed

commit a6b07058f9525c42b021f6f01d5e0da3215f46ed
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Sep 04 18:06:56 2019

Add a test for glyph path rendering.

Use it to also test a fixed bug in that code, where the original test
PDF no longer triggers the function that had the bug.

Bug: chromium:601362
Change-Id: I251b59ba5c55752a46bfaa680ef78a037d877283
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/60052
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/a6b07058f9525c42b021f6f01d5e0da3215f46ed/testing/resources/pixel/bug_601362.in
[add] https://pdfium.googlesource.com/pdfium/+/a6b07058f9525c42b021f6f01d5e0da3215f46ed/testing/resources/pixel/bug_601362_expected.pdf.0.png


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0cec9dcb0f83536a041d4db4bd741ccd43100fa8

commit 0cec9dcb0f83536a041d4db4bd741ccd43100fa8
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Sep 04 21:57:34 2019

Roll src/third_party/pdfium aea4bca2621b..a6b07058f952 (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/aea4bca2621b..a6b07058f952

git log aea4bca2621b..a6b07058f952 --date=short --no-merges --format='%ad %ae %s'
2019-09-04 thestig@chromium.org Add a test for glyph path rendering.
2019-09-04 thestig@chromium.org Add a pixel test for a fixed JBIG2 bug.
2019-09-04 thestig@chromium.org Remove CRLF line endings from link_annots.in.
2019-09-03 thestig@chromium.org Roll third_party/freetype/src/ 9adc3b35f..543a3b939 (31 commits)
2019-08-28 gourabk@microsoft.com Add embedder tests for progressive render public APIs

Created with:
  gclient setdep -r src/third_party/pdfium@a6b07058f952

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

Bug: chromium:601362,chromium:963885
Change-Id: Ib95fe39d0b40e4f159dd0dd4493b6bc4070d53d6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1783561
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#693391}

[modify] https://crrev.com/0cec9dcb0f83536a041d4db4bd741ccd43100fa8/DEPS


### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

The recent code change here looks like test code only, so I'm not going to mention this in the M78 release notes.

### th...@chromium.org (2019-10-18)

Correct. Just a follow up CL to add test coverage.

### is...@google.com (2019-10-18)

This issue was migrated from crbug.com/chromium/601362?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/602117, crbug.com/chromium/602129]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084042)*
