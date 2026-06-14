# Security: PDFium Uninitialized Memory Read in CXFA_LayoutPageMgr::GetAvailHeight

| Field | Value |
|-------|-------|
| **Issue ID** | [40093877](https://issues.chromium.org/issues/40093877) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux |
| **Reporter** | st...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-01-28 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

This issue affects the lastest version of PDFium ( <https://pdfium.googlesource.com/pdfium/+/refs/heads/master> ). When enabling XFA and ASAN, pdfium\_test.exe shows the following log.

# Rendering PDF file C:\poc.pdf. Document has invalid cross reference table

==19532==ERROR: AddressSanitizer: access-violation on unknown address 0xbebebec6 (pc 0x027fcf29 bp 0x0442ebb8 sp 0x0442eb00 T0)  

==19532==The signal is caused by a READ memory access.  

#0 0x27fcf28 in CXFA\_LayoutPageMgr::GetAvailHeight C:\pdfium\xfa\fxfa\parser\cxfa\_layoutpagemgr.cpp:494  

#1 0x2808591 in CXFA\_LayoutProcessor::DoLayout C:\pdfium\xfa\fxfa\parser\cxfa\_layoutprocessor.cpp:73  

#2 0x28a2164 in CXFA\_FFDocView::DoLayout C:\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp:94  

#3 0x2917124 in CPDFXFA\_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp:136  

#4 0x2930c1b in FPDF\_LoadXFA C:\pdfium\fpdfsdk\fpdf\_view.cpp:255  

#5 0x14b15 in main C:\pdfium\samples\pdfium\_test.cc:1005  

#6 0x2dc67aa in \_\_scrt\_common\_main\_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#7 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)  

#8 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)  

#9 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation C:\pdfium\xfa\fxfa\parser\cxfa\_layoutpagemgr.cpp:494 in CXFA\_LayoutPageMgr::GetAvailHeight  

==19532==ABORTING

According to 0xbebebec6, which is near 0xbebebebe, it's obvious that it's an uninitialized memory access issue ( <https://github.com/google/sanitizers/wiki/AddressSanitizer#faq> ).

When ASAN was not enabled and page heap option for pdfium\_test.exe was enabled, the value will be 0xc0c0c0c0, which also indicates that the memory was not initialized.

**VERSION**  

Chrome Version: pdfium master  

Operating System: All

**REPRODUCTION CASE**  

A minimized POC was attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.1 KB)

## Timeline

### st...@gmail.com (2019-01-28)

Root cause analysis.

1. When testing under the debug verion of pdfium_test.exe, an assertion will be triggered at line 1330 of cxfa_layoutpagemgr.cpp.
==========================

CXFA_Node* CXFA_LayoutPageMgr::GetNextAvailPageArea(
    CXFA_Node* pTargetPageArea,
    CXFA_Node* pTargetContentArea,
    bool bNewPage,
    bool bQuery) {
  if (!m_pCurPageArea) {
    FindPageAreaFromPageSet(m_pTemplatePageSetRoot, nullptr, pTargetPageArea,
                            pTargetContentArea, bNewPage, bQuery);
    ASSERT(m_pCurPageArea);            // -----------------------------------> ASSERT failed!!!
    return m_pCurPageArea;
  }

  if (!pTargetPageArea || pTargetPageArea == m_pCurPageArea) {
    if (!bNewPage && GetNextContentArea(pTargetContentArea))
      return m_pCurPageArea;
  // ......
}

2.Now it will return to function CXFA_LayoutPageMgr::RunBreak. And RunBreak will return false. 
==========================

bool CXFA_LayoutPageMgr::RunBreak(XFA_Element eBreakType,
                                  XFA_AttributeValue eTargetType,
                                  CXFA_Node* pTarget,
                                  bool bStartNew) {
  bool bRet = false;
  switch (eTargetType) {
    case XFA_AttributeValue::ContentArea:
      if (pTarget && pTarget->GetElementType() != XFA_Element::ContentArea)
        pTarget = nullptr;
      if (!pTarget ||
          m_CurrentContainerRecordIter == m_ProposedContainerRecords.end() ||
          pTarget !=
              GetCurrentContainerRecord()->pCurContentArea->GetFormNode() ||
          bStartNew) {
        CXFA_Node* pPageArea = nullptr;
        if (pTarget)
          pPageArea = pTarget->GetParent();

        pPageArea = GetNextAvailPageArea(pPageArea, pTarget, false, false);
        bRet = !!pPageArea;
      }
      break;
    case XFA_AttributeValue::PageArea:
      if (pTarget && pTarget->GetElementType() != XFA_Element::PageArea)
        pTarget = nullptr;
      if (!pTarget ||
          m_CurrentContainerRecordIter == m_ProposedContainerRecords.end() ||
          pTarget != GetCurrentContainerRecord()->pCurPageArea->GetFormNode() ||
          bStartNew) {
        CXFA_Node* pPageArea =
            GetNextAvailPageArea(pTarget, nullptr, true, false);
        bRet = !!pPageArea;            // -----------------------------------> return to here, bRet = false
      }
      break;
    case XFA_AttributeValue::PageOdd:
      if (pTarget && pTarget->GetElementType() != XFA_Element::PageArea)
        pTarget = nullptr;
      break;
    case XFA_AttributeValue::PageEven:
      if (pTarget && pTarget->GetElementType() != XFA_Element::PageArea)
        pTarget = nullptr;
      break;
    case XFA_AttributeValue::Auto:
    default:
      break;
  }
  return bRet;
}

3.Now it will return to function CXFA_LayoutPageMgr::ExecuteBreakBeforeOrAfter. And ExecuteBreakBeforeOrAfter will return false.
==========================

bool CXFA_LayoutPageMgr::ExecuteBreakBeforeOrAfter(
    CXFA_Node* pCurNode,
    bool bBefore,
    CXFA_Node*& pBreakLeaderTemplate,
    CXFA_Node*& pBreakTrailerTemplate) {
  XFA_Element eType = pCurNode->GetElementType();
  switch (eType) {
    case XFA_Element::BreakBefore:
    case XFA_Element::BreakAfter: {
      WideString wsBreakLeader;
      WideString wsBreakTrailer;
      CXFA_Node* pFormNode = pCurNode->GetContainerParent();
      CXFA_Node* pContainer = pFormNode->GetTemplateNodeIfExists();
      bool bStartNew =
          pCurNode->JSObject()->GetInteger(XFA_Attribute::StartNew) != 0;
      CXFA_Script* pScript =
          pCurNode->GetFirstChildByClass<CXFA_Script>(XFA_Element::Script);
      if (pScript && !RunBreakTestScript(pScript))
        return false;

      WideString wsTarget =
          pCurNode->JSObject()->GetCData(XFA_Attribute::Target);
      CXFA_Node* pTarget =
          ResolveBreakTarget(m_pTemplatePageSetRoot, true, wsTarget);
      wsBreakTrailer = pCurNode->JSObject()->GetCData(XFA_Attribute::Trailer);
      wsBreakLeader = pCurNode->JSObject()->GetCData(XFA_Attribute::Leader);
      pBreakLeaderTemplate =
          ResolveBreakTarget(pContainer, true, wsBreakLeader);
      pBreakTrailerTemplate =
          ResolveBreakTarget(pContainer, true, wsBreakTrailer);
      if (RunBreak(eType,
                   pCurNode->JSObject()->GetEnum(XFA_Attribute::TargetType),
                   pTarget, bStartNew)) {    // -----------------------------------> RunBreak returned false here
        return true;
      }
  // ......
}

4.Now it will return to function CXFA_LayoutPageMgr::PrepareFirstPage. The root cause of this issue was within this function. PrepareFirstPage should return false but it returned true instead.
==========================

bool CXFA_LayoutPageMgr::PrepareFirstPage(CXFA_Node* pRootSubform) {
  bool bProBreakBefore = false;
  CXFA_Node* pBreakBeforeNode = nullptr;
  while (pRootSubform) {
    for (CXFA_Node* pBreakNode = pRootSubform->GetFirstChild(); pBreakNode;
         pBreakNode = pBreakNode->GetNextSibling()) {
      XFA_Element eType = pBreakNode->GetElementType();
      if (eType == XFA_Element::BreakBefore ||
          (eType == XFA_Element::Break &&
           pBreakNode->JSObject()->GetEnum(XFA_Attribute::Before) !=
               XFA_AttributeValue::Auto)) {
        bProBreakBefore = true;
        pBreakBeforeNode = pBreakNode;
        break;
      }
    }
    if (bProBreakBefore)
      break;

    bProBreakBefore = true;
    pRootSubform =
        pRootSubform->GetFirstChildByClass<CXFA_Subform>(XFA_Element::Subform);
    while (pRootSubform && !pRootSubform->PresenceRequiresSpace()) {
      pRootSubform = pRootSubform->GetNextSameClassSibling<CXFA_Subform>(
          XFA_Element::Subform);
    }
  }
  CXFA_Node* pLeader;
  CXFA_Node* pTrailer;
  if (pBreakBeforeNode &&
      ExecuteBreakBeforeOrAfter(pBreakBeforeNode, true, pLeader, pTrailer)) { // -----------------------------------> returned false
    m_CurrentContainerRecordIter = m_ProposedContainerRecords.begin();
    return true;
  }
  return AppendNewPage(true);  // -----------------------------------> but this line still got chance to execute and returned true
}

4.Correct code logic should be written as follows.
==========================

bool CXFA_LayoutPageMgr::PrepareFirstPage(CXFA_Node* pRootSubform) {
  // ......
  if (pBreakBeforeNode) {
    if (ExecuteBreakBeforeOrAfter(pBreakBeforeNode, true, pLeader, pTrailer)) {
      m_CurrentContainerRecordIter = m_ProposedContainerRecords.begin();
      return true;
    }
    return false;
  }
  return AppendNewPage(true);
}

### st...@gmail.com (2019-01-28)

I upload a patch for this issue at https://pdfium-review.googlesource.com/c/pdfium/+/49150

### st...@gmail.com (2019-01-28)

My patch could fix this issue properly. However, after patching this issue. Another UAF issue will be exposed (not introduced by my patch). The ASAN log shows that it's caused by function ProbeForLowSeverityLifetimeIssue() in UnownedPtr. That's a low severity issue.


Rendering PDF file C:\poc.pdf.
Document has invalid cross reference table
=================================================================
==21916==ERROR: AddressSanitizer: heap-use-after-free on address 0x0cd009e0 at pc 0x03bacc67 bp 0x0032eb10 sp 0x0032eb04
READ of size 1 at 0x0cd009e0 thread T0
    #0 0x3bacc66 in CXFA_FFPageView::~CXFA_FFPageView C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:116
    #1 0x3ae8858 in XFA_ReleaseLayoutItem C:\pdfium\xfa\fxfa\parser\cxfa_layoutitem.cpp:34
    #2 0x3ae878d in XFA_ReleaseLayoutItem C:\pdfium\xfa\fxfa\parser\cxfa_layoutitem.cpp:26
    #3 0x3ae99d9 in CXFA_LayoutPageMgr::~CXFA_LayoutPageMgr C:\pdfium\xfa\fxfa\parser\cxfa_layoutpagemgr.cpp:288
    #4 0x3af8073 in std::unique_ptr<CXFA_LayoutPageMgr,std::default_delete<CXFA_LayoutPageMgr> >::~unique_ptr C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.16.27023\include\memory:2296
    #5 0x3af7fc1 in CXFA_LayoutProcessor::~CXFA_LayoutProcessor C:\pdfium\xfa\fxfa\parser\cxfa_layoutprocessor.cpp:26
    #6 0x3a9ee77 in std::unique_ptr<CXFA_LayoutProcessor,std::default_delete<CXFA_LayoutProcessor> >::reset C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.16.27023\include\memory:2333
    #7 0x3a9e8f8 in CXFA_Document::ClearLayoutData C:\pdfium\xfa\fxfa\parser\cxfa_document.cpp:1296
    #8 0x3b8aa4b in CXFA_FFDoc::CloseDoc C:\pdfium\xfa\fxfa\cxfa_ffdoc.cpp:173
    #9 0x3c06a51 in CPDFXFA_Context::CloseXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp:80
    #10 0x3c0717c in CPDFXFA_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp:131
    #11 0x3c20c27 in FPDF_LoadXFA C:\pdfium\fpdfsdk\fpdf_view.cpp:255
    #12 0x1304b15 in main C:\pdfium\samples\pdfium_test.cc:1005
    #13 0x40b67ba in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #14 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)
    #15 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)
    #16 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

0x0cd009e0 is located 0 bytes inside of 104-byte region [0x0cd009e0,0x0cd00a48)
freed by thread T0 here:
    #0 0x40a0118 in free c:\b\rr\tmpoxo5hi\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:53
    #1 0x3b8c009 in std::unique_ptr<CXFA_FFDocView,std::default_delete<CXFA_FFDocView> >::reset C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Tools\MSVC\14.16.27023\include\memory:2333
    #2 0x3b8aa2a in CXFA_FFDoc::CloseDoc C:\pdfium\xfa\fxfa\cxfa_ffdoc.cpp:170
    #3 0x3c06a51 in CPDFXFA_Context::CloseXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp:80
    #4 0x3c0717c in CPDFXFA_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp:131
    #5 0x3c20c27 in FPDF_LoadXFA C:\pdfium\fpdfsdk\fpdf_view.cpp:255
    #6 0x1304b15 in main C:\pdfium\samples\pdfium_test.cc:1005
    #7 0x40b67ba in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #8 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)
    #9 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)
    #10 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

previously allocated by thread T0 here:
    #0 0x40a021c in malloc c:\b\rr\tmpoxo5hi\w\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:69
    #1 0x40b3774 in operator new d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x3b8b806 in CXFA_FFDoc::CreateDocView C:\pdfium\xfa\fxfa\cxfa_ffdoc.cpp:92
    #3 0x3c070c9 in CPDFXFA_Context::LoadXFADoc C:\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_context.cpp:129
    #4 0x3c20c27 in FPDF_LoadXFA C:\pdfium\fpdfsdk\fpdf_view.cpp:255
    #5 0x1304b15 in main C:\pdfium\samples\pdfium_test.cc:1005
    #6 0x40b67ba in __scrt_common_main_seh d:\agent\_work\2\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #7 0x7730343c in BaseThreadInitThunk+0x11 (C:\Windows\syswow64\kernel32.dll+0x7dd7343c)
    #8 0x77a69801 in RtlInitializeExceptionChain+0x62 (C:\Windows\SysWOW64\ntdll.dll+0x7dea9801)
    #9 0x77a697d4 in RtlInitializeExceptionChain+0x35 (C:\Windows\SysWOW64\ntdll.dll+0x7dea97d4)

SUMMARY: AddressSanitizer: heap-use-after-free C:\pdfium\xfa\fxfa\cxfa_ffpageview.cpp:116 in CXFA_FFPageView::~CXFA_FFPageView
Shadow bytes around the buggy address:
  0x319a00e0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x319a00f0: fd fa fa fa fa fa fa fa fa fa fd fd fd fd fd fd
  0x319a0100: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x319a0110: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa
  0x319a0120: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd
=>0x319a0130: fd fd fd fd fa fa fa fa fa fa fa fa[fd]fd fd fd
  0x319a0140: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x319a0150: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x319a0160: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x319a0170: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fd fd
  0x319a0180: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
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
==21916==ABORTING


### st...@gmail.com (2019-01-28)

Root cause analysis of the exposed UAF issue.

1. The issue was caused in CXFA_FFPageView's destructor. Since this class has an member UnownedPtr<CXFA_FFDocView>, when ASAN was enabled, UnownedPtr will call ProbeForLowSeverityLifetimeIssue() to check whether the actual data it points to has been freed or not.
==========================

class CXFA_FFPageView final : public CXFA_ContainerLayoutItem {
 public:
  CXFA_FFPageView(CXFA_FFDocView* pDocView, CXFA_Node* pPageArea);
  ~CXFA_FFPageView() override;

  CXFA_FFDocView* GetDocView() const;
  CFX_RectF GetPageViewRect() const;
  CFX_Matrix GetDisplayMatrix(const FX_RECT& rtDisp, int32_t iRotate) const;
  std::unique_ptr<IXFA_WidgetIterator> CreateWidgetIterator(
      uint32_t dwTraverseWay,
      uint32_t dwWidgetFilter);

 private:
  UnownedPtr<CXFA_FFDocView> const m_pDocView;  // ----------------> UnownedPtr<CXFA_FFDocView>
};


2. But m_pDocView has been freed already in CXFA_FFDoc::CloseDoc(). Here CXFA_FFDoc::m_DocView points to the same object with CXFA_FFPageView::m_pDocView.
==========================

void CXFA_FFDoc::CloseDoc() {
  if (m_DocView) {
    m_DocView->RunDocClose();
    m_DocView.reset();        // ----------------> this will free m_DocView
  }
  if (m_pDocument)
    m_pDocument->ClearLayoutData();   // --------------> will call CXFA_FFPageView::~CXFA_FFPageView()

  m_pDocument.reset();
  m_pXMLDoc.reset();
  m_pNotify.reset();
  m_pPDFFontMgr.reset();
  m_HashToDibDpiMap.clear();
  m_pApp->ClearEventTargets();
}


Patch suggestions.
==========================
Maybe m_pDocument->ClearLayoutData() should be executed before m_DocView.reset().

### st...@gmail.com (2019-01-28)

The UAF issue was a little complicated for me to fix :(
There's too much cross reference for each object.

### li...@chromium.org (2019-01-28)

Thanks for reporting and taking a look! thestig@, would you be able to help out?

Tentatively setting some labels. Severity medium because this is an uninitialized memory read.

[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2019-01-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-29)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-01-29)

XFA = not shipped.

### st...@gmail.com (2019-08-14)

hello, any plan for this case?

### ts...@chromium.org (2019-08-15)

No longer reproduces for me. I've recently landed a number of changes affecting CXFA_FF* layout items.  Please double-check against a ToT (Tip of Tree)  build.

### ts...@chromium.org (2019-08-15)

Feel free to re-open if you can reproduce

### ts...@chromium.org (2019-08-15)

... and I ran the wrong test cast. Yes, this still reproduces.  Having made the aforementioned changes, we can now look at this as a special case.

### ts...@chromium.org (2019-08-15)

Currently reproduces as a NULL deref segv.  Can you still get control of the address?
   
==116773==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000011 (pc 0x5566e02109bf bp 0x7ffef409fdd0 sp 0x7ffef409fda0 T0)
==116773==The signal is caused by a READ memory access.
==116773==Hint: address points to the zero page.
    #0 0x5566e02109be in get ./../../buildtools/third_party/libc++/trunk/include/memory:2624:19
    #1 0x5566e02109be in Get ./../../core/fxcrt/retain_ptr.h:54:0
    #2 0x5566e02109be in RetainPtr ./../../core/fxcrt/retain_ptr.h:33:0
    #3 0x5566e02109be in CXFA_ViewLayoutProcessor::GetAvailHeight() ./../../xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp:562:0
    #4 0x5566e020a9c5 in CXFA_LayoutProcessor::DoLayout() ./../../xfa/fxfa/layout/cxfa_layoutprocessor.cpp:78:50
    #5 0x5566e00bba14 in CXFA_FFDocView::DoLayout() ./../../xfa/fxfa/cxfa_ffdocview.cpp:98:30
    #6 0x5566e031e4bb in CPDFXFA_Context::LoadXFADoc() ./../../fpdfsdk/fpdfxfa/cpdfxfa_context.cpp:129:18
    #7 0x5566dd7d9f86 in FPDF_LoadXFA ./../../fpdfsdk/fpdf_view.cpp:260:32
    #8 0x5566dd751c73 in RenderPdf ./../../samples/pdfium_test.cc:841:12
    #9 0x5566dd751c73 in main ./../../samples/pdfium_test.cc:1068:0


### st...@gmail.com (2019-08-15)

I'm getting the same NULL deref now. I'll see if I have other samples that could reproduce non-NULL crashes.

### th...@chromium.org (2019-08-16)

I picked a mid-January CL, https://pdfium.googlesource.com/pdfium/+/a9a733294487f1589f3b93240df9a5907986c8d7, and it also only NULL derefs with poc.pdf.

### th...@chromium.org (2019-08-16)

But in any case, thanks for the remainder. I'll try to get to this bug sooner than later.

### th...@chromium.org (2019-08-16)

https://pdfium-review.googlesource.com/59571

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-16)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/97a972a50c3519e1080d470770b6915477816e20

commit 97a972a50c3519e1080d470770b6915477816e20
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Aug 16 21:43:38 2019

Avoid some crashes in CXFA_ViewLayoutProcessor.

Also remove an assertion that can fail.

Bug: chromium:925791
Change-Id: Ib7bf24ba0e8290ac9abaa3e56a875a2f87834a9b
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/59571
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/97a972a50c3519e1080d470770b6915477816e20/xfa/fxfa/layout/cxfa_viewlayoutprocessor.cpp


### th...@chromium.org (2019-08-16)

I think this is fixed. Please let me know if you have additional test cases that still fail in similar ways.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1f00476c49876f3410d173e6ff9b301cae723606

commit 1f00476c49876f3410d173e6ff9b301cae723606
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Aug 17 00:23:24 2019

Roll src/third_party/pdfium 5b3e4c0776c3..c0ccf6d0da8e (4 commits)

https://pdfium.googlesource.com/pdfium.git/+log/5b3e4c0776c3..c0ccf6d0da8e

git log 5b3e4c0776c3..c0ccf6d0da8e --date=short --no-merges --format='%ad %ae %s'
2019-08-16 tsepez@chromium.org CPDFSDK_InteractiveForm::m_XFAMap is useless.
2019-08-16 tsepez@chromium.org Move two files from top-level fpdfsdk/ directory.
2019-08-16 thestig@chromium.org Avoid some crashes in CXFA_ViewLayoutProcessor.
2019-08-16 thestig@chromium.org Make CXFA_ViewRecord private within CXFA_ViewLayoutProcessor.

Created with:
  gclient setdep -r src/third_party/pdfium@c0ccf6d0da8e

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:925791
Change-Id: Ib1784407a424ea3a12b6ac4357f0bd54d5b36314
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1759289
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#687900}

[modify] https://crrev.com/1f00476c49876f3410d173e6ff9b301cae723606/DEPS


### sh...@chromium.org (2019-08-17)

[Empty comment from Monorail migration]

### st...@gmail.com (2019-08-19)

https://crbug.com/chromium/925791#c20
Hello, I've tested my other samples and all of them resulted in nullptr crashes. Thanks for your patch.

https://crbug.com/chromium/925791#c16
Not sure why it cannot be reproduced. I remember that I can reproduce definitely at that time.

### na...@google.com (2019-08-19)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-21)

Congrats! The Panel decided to reward $1,000 for this report!

### na...@google.com (2019-08-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/925791?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093877)*
