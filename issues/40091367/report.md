# Security: Uninitialized Memory Read in CXFA_LayoutPageMgr::GetAvailHeight

| Field | Value |
|-------|-------|
| **Issue ID** | [40091367](https://issues.chromium.org/issues/40091367) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | hn...@chromium.org |
| **Created** | 2018-05-13 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

An out-of-bounds-read (uninitialized-memory-read) issue was found in PDFium. Following log was produced by AddressSanitizer.

=================================================================  

==9584==ERROR: AddressSanitizer: access-violation on unknown address 0xbebebec6 (pc 0x037419e3 bp 0x002deb18 sp 0x002dea60 T0)  

#0 0x37419e2 in CXFA\_LayoutPageMgr::GetAvailHeight C:\pdfium\xfa\fxfa\parser\cxfa\_layoutpagemgr.cpp:489  

#1 0x3714d67 in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:73  

#2 0x36577ba in CXFA\_FFDocView::DoLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:94  

#3 0x362e0bf in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:118  

#4 0x2c14ffa in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:265  

#5 0x1054269 in main C:\pdfium\samples\pdfium\_test.cc:911  

#6 0x3c5b90a in \_\_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:283  

#7 0x7677343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#8 0x77569831 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9831)  

#9 0x77569804 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9804)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation C:\pdfium\xfa\fxfa\parser\cxfa\_layoutpagemgr.cpp:489 in CXFA\_LayoutPageMgr::GetAvailHeight  

==9584==ABORTING

If we compile a normal version of pdfium (with is\_asan=false and is\_debug=false), and enable pageheap option for pdfium\_test.exe, we'll get the following information. Here the value of eax was 0xc0c0c0c0 (read from a 12-bytes heap) which indicates that the value was not initialized.

=================================================================  

(2c60.499c): Access violation - code c0000005 (!!! second chance !!!)  

eax=c0c0c0c0 ebx=0aed0f90 ecx=0af76fc0 edx=0031f394 esi=0af76fc0 edi=0031f3bc  

eip=01b19473 esp=0031f378 ebp=0031f3a0 iopl=0 nv up ei pl nz na po nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010202  

pdfium\_test!CXFA\_LayoutPageMgr::GetAvailHeight+0x1d:  

01b19473 8b4008 mov eax,dword ptr [eax+8] ds:002b:c0c0c0c8=????????

0:000> r eax  

eax=c0c0c0c0

0:000> ub eip  

pdfium\_test!CXFA\_LayoutPageMgr::GetAvailHeight+0x5  

[C:\pdfium\xfa\fxfa\parser\cxfa\_layoutpagemgr.cpp @ 487]:  

01b1945b 83ec20 sub esp,20h  

01b1945e a1b09bf801 mov eax,dword ptr [pdfium\_test!\_\_security\_cookie (01f89bb0)]  

01b19463 89ce mov esi,ecx  

01b19465 0f57c0 xorps xmm0,xmm0  

01b19468 31e8 xor eax,ebp  

01b1946a 8945f4 mov dword ptr [ebp-0Ch],eax  

01b1946d 8b4118 mov eax,dword ptr [ecx+18h]  

01b19470 8b4008 mov eax,dword ptr [eax+8]

0:000> dd ecx+18 L1  

0af76fd8 0af78ff0

0:000> dd 0af78ff0  

0af78ff0 0af78ff0 0af78ff0 c0c0c0c0 d0d0d0d0  

0af79000 ???????? ???????? ???????? ????????

0:000> !heap -p -a 0af78ff0  

address 0af78ff0 found in  

\_DPH\_HEAP\_ROOT @ 321000  

in busy allocation ( DPH\_HEAP\_BLOCK: UserAddr UserSize - VirtAddr VirtSize)  

af80068: af78ff0 c - af78000 2000  

66248e89 verifier!AVrfDebugPageHeapAllocate+0x00000229  

7760103e ntdll!RtlDebugAllocateHeap+0x00000030  

775babe2 ntdll!RtlpAllocateHeap+0x000000c4  

775634a1 ntdll!RtlAllocateHeap+0x0000023a  

01c521e5 pdfium\_test!\_malloc\_base+0x00000038 [minkernel\crts\ucrt\src\appcrt\heap\malloc\_base.cpp @ 34]  

01c2dbea pdfium\_test!operator new+0x0000001a [f:\dd\vctools\crt\vcstartup\src\heap\new\_scalar.cpp @ 34]  

01b187c8 pdfium\_test!CXFA\_LayoutPageMgr::CXFA\_LayoutPageMgr+0x00000028 [C:\pdfium\xfa\fxfa\parser\cxfa\_layoutpagemgr.cpp @ 275]  

01b0f9d4 pdfium\_test!CXFA\_LayoutProcessor::StartLayout+0x00000086 [C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp @ 49]  

01aed438 pdfium\_test!CXFA\_FFDocView::StartLayout+0x0000003c [C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp @ 74]  

01ae5057 pdfium\_test!CPDFXFA\_Context::LoadXFADoc+0x000000a7 [C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp @ 112]  

018943ee pdfium\_test!FPDF\_LoadXFA+0x00000022 [C:\pdfium\fpdfsdk\fpdf\_view.cpp @ 265]  

012f1edb pdfium\_test!main+0x00000edb [C:\pdfium\samples\pdfium\_test.cc @ 911]  

01c2e61b pdfium\_test!\_\_scrt\_common\_main\_seh+0x000000f9 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 283]  

7677343d kernel32!BaseThreadInitThunk+0x0000000e  

77569832 ntdll!\_\_RtlUserThreadStart+0x00000070  

77569805 ntdll!\_RtlUserThreadStart+0x0000001b

Here the size of the heap buffer was 12 bytes. Actually, that's `CXFA_LayoutPageMgr::m_CurrentContainerRecordIter`。

pdfium\_test.exe crashed when calling `GetCurrentContainerRecord()` in `CXFA_LayoutPageMgr::GetAvailHeight()`.

```
float CXFA_LayoutPageMgr::GetAvailHeight() {  
  CXFA_ContainerLayoutItem\* pLayoutItem =  
      GetCurrentContainerRecord()->pCurContentArea;     // ----> crashed!!!  
  if (!pLayoutItem || !pLayoutItem->m_pFormNode)  
    return 0.0f;  
  
  float fAvailHeight = pLayoutItem->m_pFormNode->JSObject()  
                           ->GetMeasure(XFA_Attribute::H)  
                           .ToUnit(XFA_Unit::Pt);  
  if (fAvailHeight >= XFA_LAYOUT_FLOAT_PERCISION)  
    return fAvailHeight;  
  if (m_CurrentContainerRecordIter == m_ProposedContainerRecords.begin())  
    return 0.0f;  
  return FLT_MAX;  
}  
  
  CXFA_ContainerRecord\* /\* CXFA_LayoutPageMgr:: \*/ GetCurrentContainerRecord() {  
    return \*m_CurrentContainerRecordIter;               // ----> crashed!!!  
  }  

```

This vulnerability is more likely exploitable since the value of `pLayoutItem` may be controlled by attacker.

```
  float fAvailHeight = pLayoutItem->m_pFormNode->JSObject()  
                           ->GetMeasure(XFA_Attribute::H)  
                           .ToUnit(XFA_Unit::Pt);  

```

**VERSION**  

Chrome Version: pdfium with XFA enabled  

Operating System: Windows

**REPRODUCTION CASE**  

A minimized proof-of-concept file will be attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### st...@gmail.com (2018-05-13)

Please note it only affects XFA enabled PDFium. Some of the build arguments:

```
pdf_enable_xfa = true
pdf_enable_v8 = true
is_asan=true
```

### st...@gmail.com (2018-05-13)

I'm sorry for forgetting add PDFium in title. Please help add the following label,
thank you very much.

Components: Internals>Plugins>PDF

### cl...@chromium.org (2018-05-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4899555070705664.

### cl...@chromium.org (2018-05-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4826538613407744.

### rs...@chromium.org (2018-05-13)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### ds...@chromium.org (2018-05-14)

[Empty comment from Monorail migration]

### hn...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### hn...@chromium.org (2018-06-27)

[Empty comment from Monorail migration]

### hn...@chromium.org (2018-06-27)

Tom, Dan, I need some input here. The root of this bug is this block in the POC: 

    <subform layout="tb">
        <event activity="initialize">
            <submit/>
        </event>
    </subform>

"initialize" triggers when the document is loaded, and a submit is immediately performed. Putting aside the security considerations of the uninitialized memory access for a moment, I don't think that's a thing we want to ever do. Do we even want to support Submit at all?

### ts...@chromium.org (2018-06-28)

No idea, Dan?

### ds...@chromium.org (2018-07-09)

At least for MVP, I think we can put Submit off the table. I'd hope the initialize would fire after the subform is initialized? So, hopefully we can fixup anything uninitialized?

### hn...@chromium.org (2018-07-12)

It triggers during the initialization. The relevant call tree:
 
CXFA_FFDocView::StartLayout() begins
  CXFA_LayoutProcessor::StartLayout() begins
    -> CXFA_LayoutPageMgr::AppendNewPage() fills m_ProposedContainerRecords
  CXFA_LayoutProcessor::StartLayout() ends
  CXFA_FFDocView::InitLayout() begins
    CPDFXFA_DocEnvironment::OnBeforeNotifySubmit() begins
      CXFA_LayoutProcessor::StartLayout() begins
        -> CXFA_LayoutPageMgr::ClearData() clears m_ProposedContainerRecords
        -> CXFA_LayoutPageMgr::AppendNewPage() fills m_ProposedContainerRecords
      CXFA_LayoutProcessor::StartLayout() ends
      CXFA_LayoutProcessor::DoLayout() begins
        -> CXFA_LayoutPageMgr::GetAvailHeight() accesses m_ProposedContainerRecords
        -> CXFA_LayoutPageMgr::ClearData() clears m_ProposedContainerRecords
      CXFA_LayoutProcessor::DoLayout() ends
    CPDFXFA_DocEnvironment::OnBeforeNotifySubmit() ends
  CXFA_FFDocView::InitLayout() ends
CXFA_FFDocView::StartLayout() ends
CXFA_LayoutProcessor::DoLayout() begins
  -> CXFA_LayoutPageMgr::GetAvailHeight() accesses m_ProposedContainerRecords, crashes

The submit operation inside CXFA_FFDocView::StartLayout() causes m_ProposedContainerRecords to be cleared, while there is an assumption that it would be valid after CXFA_FFDocView::StartLayout() returns.

### hn...@chromium.org (2018-07-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-25)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/1b54bc1474af7923f6b82496924978cb87844ff0

commit 1b54bc1474af7923f6b82496924978cb87844ff0
Author: Henrique Nakashima <hnakashima@chromium.org>
Date: Wed Jul 25 17:26:28 2018

Disable submit in XFA forms.

Bug: chromium:842503
Change-Id: If411815d8324929f482e3cad0fda54f24d370c2a
Reviewed-on: https://pdfium-review.googlesource.com/37830
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Henrique Nakashima <hnakashima@chromium.org>

[modify] https://crrev.com/1b54bc1474af7923f6b82496924978cb87844ff0/xfa/fxfa/parser/cxfa_event.h
[modify] https://crrev.com/1b54bc1474af7923f6b82496924978cb87844ff0/xfa/fxfa/parser/cxfa_event.cpp
[modify] https://crrev.com/1b54bc1474af7923f6b82496924978cb87844ff0/xfa/fxfa/fxfa.h
[modify] https://crrev.com/1b54bc1474af7923f6b82496924978cb87844ff0/xfa/fxfa/parser/cxfa_node.cpp
[modify] https://crrev.com/1b54bc1474af7923f6b82496924978cb87844ff0/fpdfsdk/fpdfxfa/cpdfxfa_docenvironment.cpp
[modify] https://crrev.com/1b54bc1474af7923f6b82496924978cb87844ff0/fpdfsdk/fpdfxfa/cpdfxfa_docenvironment.h


### hn...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-07-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/033de4c4fc396ff11ae80766cf7d00d86f4afc62

commit 033de4c4fc396ff11ae80766cf7d00d86f4afc62
Author: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Wed Jul 25 23:20:07 2018

Roll src/third_party/pdfium 1f7db295b1de..a5d2bf1131fe (8 commits)

https://pdfium.googlesource.com/pdfium.git/+log/1f7db295b1de..a5d2bf1131fe


git log 1f7db295b1de..a5d2bf1131fe --date=short --no-merges --format='%ad %ae %s'
2018-07-25 thestig@chromium.org Remove CFX_MemoryStream uses in tests.
2018-07-25 tsepez@chromium.org Use struct {Single,Range}Cmap in FPDFAPI_CIDFromCharCode().
2018-07-25 hinoka@google.com README.md: Update waterfall location
2018-07-25 thestig@chromium.org Change CFX_BufferSeekableReadStream to take a span.
2018-07-25 thestig@chromium.org Only build cfx_fileaccess_windows.cpp on Windows.
2018-07-25 thestig@chromium.org Move CPDF_SyntaxParser init methods into ctor.
2018-07-25 hnakashima@chromium.org Disable submit in XFA forms.
2018-07-25 tsepez@chromium.org Introduce ToXMLElement() checked downcast helper function


Created with:
  gclient setdep -r src/third_party/pdfium@a5d2bf1131fe

The AutoRoll server is located here: https://pdfium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:860896,chromium:842503
TBR=dsinclair@chromium.org

Change-Id: If7bcdd2cc19be54976a33cb521e5fe2717fae483
Reviewed-on: https://chromium-review.googlesource.com/1150362
Reviewed-by: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Commit-Queue: pdfium-chromium-autoroll <pdfium-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#578120}
[modify] https://crrev.com/033de4c4fc396ff11ae80766cf7d00d86f4afc62/DEPS


### sh...@chromium.org (2018-07-26)

[Empty comment from Monorail migration]

### aw...@google.com (2018-09-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-09-26)

hnakashima@ - thanks for the fix. Might it be worth adding a test case for this in case submit is re-enabled in the future without the root cause having been addressed?

### aw...@chromium.org (2018-09-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-28)

And $3,000 for this one :-)

### aw...@google.com (2018-09-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-11-01)

This issue was migrated from crbug.com/chromium/842503?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/62400]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091367)*
