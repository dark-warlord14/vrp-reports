# Security: PDFium (XFA) Use-after-free in function CXFA_FFWidgetHandler::OnRButtonDown

| Field | Value |
|-------|-------|
| **Issue ID** | [40051986](https://issues.chromium.org/issues/40051986) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-04-10 |
| **Bounty** | $7,500.00 |

## Description

**VERSION**

Operating System: Windows 10 64bit  

PDFium + enabled XFA (built from 8cc69b1037252e46883624efe239017dfdca5676)

**REPRODUCTION CASE**

Run pdfium\_test.exe with input file poc.pdf + poc.evt

pdfium\_test.exe --send-events poc.pdf

**VULNERABILITY DETAILS**

The bug is in function CXFA\_FFWidgetHandler::OnRButtonDown()

```
bool CXFA_FFWidgetHandler::OnRButtonDown(CXFA_FFWidget\* hWidget,  
                                         uint32_t dwFlags,  
                                         const CFX_PointF& point) {  
  bool bRet =  
      hWidget->AcceptsFocusOnButtonDown(dwFlags, hWidget->Rotate2Normal(point),  
                                        FWL_MouseCommand::RightButtonDown);  
  if (bRet) {  
    if (m_pDocView->SetFocus(hWidget)) {                           => trigger JS function in 'enter' event => free |hWidget|  
      m_pDocView->GetDoc()->GetDocEnvironment()->SetFocusWidget(  
          m_pDocView->GetDoc(), hWidget);  
    }  
    bRet = hWidget->OnRButtonDown(dwFlags, hWidget->Rotate2Normal(point));  => |hWidget| is used after freed!!!  
  }  
  return bRet;  
}  

```

Function SetFocus() can trigger JS callback => we can free |hWidget| pointer. After that, the  

freed object is used in calling function hWidget->Rotate2Normal(point).

Crash log:

eax=1f538f98 ebx=0355efa4 ecx=00000000 edx=ffffffff esi=0355f144 edi=02f9e2e4  

eip=02627f91 esp=0355ef64 ebp=0355efcc iopl=0 nv up ei pl zr na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010246  

pdfium\_test\_exe!CXFA\_FFWidget::Rotate2Normal+0x51:  

02627f91 8b08 mov ecx,dword ptr [eax] ds:002b:1f538f98=????????

0:000> kp

# ChildEBP RetAddr

00 0355efcc 0262916d pdfium\_test\_exe!CXFA\_FFWidget::Rotate2Normal(class CFX\_PTemplate<float> \* point = 0x0355f144)+0x51 [C:\Users\huyna\_dev\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffwidget.cpp @ 550]  

01 0355f030 027f4add pdfium\_test\_exe!CXFA\_FFWidgetHandler::OnRButtonDown(class CXFA\_FFWidget \* hWidget = 0x1f538f98, unsigned int dwFlags = 0, class CFX\_PTemplate<float> \* point = 0x0355f144)+0x10d [C:\Users\huyna\_dev\Desktop\chromium\pdfium\_newest\pdfium\xfa\fxfa\cxfa\_ffwidgethandler.cpp @ 109]  

02 0355f06c 00b240ba pdfium\_test\_exe!CPDFXFA\_WidgetHandler::OnRButtonDown(class CPDFSDK\_PageView \* pPageView = 0x1f5d2fb0, class fxcrt::ObservedPtr<CPDFSDK\_Annot> \* pAnnot = 0x0355f0ec, unsigned int nFlags = 0, class CFX\_PTemplate<float> \* point = 0x0355f144)+0xbd [C:\Users\huyna\_dev\Desktop\chromium\pdfium\_newest\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_widgethandler.cpp @ 485]  

03 0355f0ac 00b6a07f pdfium\_test\_exe!CPDFSDK\_AnnotHandlerMgr::Annot\_OnRButtonDown(class CPDFSDK\_PageView \* pPageView = 0x1f5d2fb0, class fxcrt::ObservedPtr<CPDFSDK\_Annot> \* pAnnot = 0x0355f0ec, unsigned int nFlags = 0, class CFX\_PTemplate<float> \* point = 0x0355f144)+0x9a [C:\Users\huyna\_dev\Desktop\chromium\pdfium\_newest\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 198]  

04 0355f100 00ba2311 pdfium\_test\_exe!CPDFSDK\_PageView::OnRButtonDown(class CFX\_PTemplate<float> \* point = 0x0355f144, unsigned int nFlag = 0)+0xbf [C:\Users\huyna\_dev\Desktop\chromium\pdfium\_newest\pdfium\fpdfsdk\cpdfsdk\_pageview.cpp @ 338]  

05 0355f15c 00b1458d pdfium\_test\_exe!FORM\_OnRButtonDown(struct fpdf\_form\_handle\_t\_\_ \* hHandle = 0x1a288fa8, struct fpdf\_page\_t\_\_ \* page = 0x1f5e4fe8, int modifier = 0n0, double page\_x = 200, double page\_y = 200)+0xd1 [C:\Users\huyna\_dev\Desktop\chromium\pdfium\_newest\pdfium\fpdfsdk\fpdf\_formfill.cpp @ 451]  

06 0355f1b8 00b13f08 pdfium\_test\_exe!`anonymous namespace'::SendMouseDownEvent(struct fpdf_form_handle_t__ \* form = 0x1a288fa8, struct fpdf_page_t__ \* page = 0x1f5e4fe8, class std::__1::vector<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> >,std::__1::allocator<std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > > > \* tokens = 0x0355f210 { size=4 })+0x22d [C:\Users\huyna_dev\Desktop\chromium\pdfium_newest\pdfium\samples\pdfium_test_event_helper.cc @ 69] 07 0355f248 00b0c240 pdfium_test_exe!SendPageEvents(struct fpdf_form_handle_t__ \* form = 0x1a288fa8, struct fpdf_page_t__ \* page = 0x1f5e4fe8, class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* events = 0x0355f73c "mousedown,right,200,200")+0x278 [C:\Users\huyna_dev\Desktop\chromium\pdfium_newest\pdfium\samples\pdfium_test_event_helper.cc @ 153] 08 0355f4a0 00b04687 pdfium_test_exe!`anonymous namespace'::RenderPage(class std::\_\_1::basic\_string<char,std::**1::char\_traits<char>,std::1::allocator<char> > \* name = 0x1801eff0 "C:\Users\huyna\_dev\OneDrive\pdfium\_issues\pdfium\_41\pdfium\_16\41.debug.TheOtherField\_Acro81.pdf", struct fpdf\_document\_t \* doc = 0x1a1f7f90, struct fpdf\_form\_handle\_t** \* form = 0x1a288fa8, struct `anonymous namespace'::FPDF_FORMFILLINFO_PDFiumTest \* form_fill_info = 0x0355f588, int page_index = 0n0, struct` anonymous namespace'::Options \* options = 0x0355f7a0, class std::\_\_1::basic\_string<char,std::\_\_1::char\_traits<char>,std::\_\_1::allocator<char> > \* events = 0x0355f73c "mousedown,right,200,200")+0xf0 [C:\Users\huyna\_dev\Desktop\chromium\pdfium\_newest\pdfium\samples\pdfium\_test.cc @ 708]  

09 0355f690 00b0182d pdfium\_test\_exe!`anonymous namespace'::RenderPdf(class std::__1::basic_string<char,std::__1::char_traits<char>,std::__1::allocator<char> > \* name = 0x1801eff0 "C:\Users\huyna_dev\OneDrive\pdfium_issues\pdfium_41\pdfium_16\41.debug.TheOtherField_Acro81.pdf", char \* buf = 0x1a10a838 "%PDF-1.3.%???", unsigned int len = 0x17be, struct` anonymous namespace'::Options \* options = 0x0355f7a0, class std::\_\_1::basic\_string<char,std::\_\_1::char\_traits<char>,std::\_\_1::allocator<char> > \* events = 0x0355f73c "mousedown,right,200,200")+0xa37 [C:\Users\huyna\_dev\Desktop\chromium\pdfium\_newest\pdfium\samples\pdfium\_test.cc @ 974]  

0a 0355f828 02bbeafe pdfium\_test\_exe!main(int argc = 0n3, char \*\* argv = 0x17f7af20)+0x82d [C:\Users\huyna\_dev\Desktop\chromium\pdfium\_newest\pdfium\samples\pdfium\_test.cc @ 1191]  

0b 0355f83c 02bbec61 pdfium\_test\_exe!invoke\_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 78]  

0c 0355f894 02bbed2d pdfium\_test\_exe!\_\_scrt\_common\_main\_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 283]  

0d 0355f89c 02bbed38 pdfium\_test\_exe!\_\_scrt\_common\_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 326]  

0e 0355f8a4 74936359 pdfium\_test\_exe!mainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_main.cpp @ 17]  

0f 0355f8b4 77197b74 KERNEL32!BaseThreadInitThunk+0x19  

10 0355f910 77197b44 ntdll!\_\_RtlUserThreadStart+0x2f  

11 0355f920 00000000 ntdll!\_RtlUserThreadStart+0x1b

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 5.9 KB)
- [poc.evt](attachments/poc.evt) (application/octet-stream, 23 B)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 10.9 KB)

## Timeline

### xi...@chromium.org (2020-04-10)

Setting Sev-High for UAF but Impact-None since we don't ship XFA by default.

tsepez@ could you also take a look at this one? Thanks!

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2020-04-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/9af75ef959336c26dc7b66652605a1b3ed807227

commit 9af75ef959336c26dc7b66652605a1b3ed807227
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Apr 14 17:07:33 2020

Retain widgets across SetFocus() calls in CXFA_FFWidgetHandler.

Bug: chromium:1069789
Change-Id: I65e26b8eb1ef6646ffb29a88d84464cd099fe3cd
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/68696
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/9af75ef959336c26dc7b66652605a1b3ed807227/testing/resources/javascript/xfa_specific/bug_1069789.in
[add] https://pdfium.googlesource.com/pdfium/+/9af75ef959336c26dc7b66652605a1b3ed807227/testing/resources/javascript/xfa_specific/bug_1069789.evt
[modify] https://pdfium.googlesource.com/pdfium/+/9af75ef959336c26dc7b66652605a1b3ed807227/xfa/fxfa/cxfa_ffwidgethandler.cpp


### ts...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/65723df7b5562a876ac0cc7f65fc77b967a49f0d

commit 65723df7b5562a876ac0cc7f65fc77b967a49f0d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Apr 14 20:35:26 2020

Roll src/third_party/pdfium 5bc1f981df4d..671aece845dd (8 commits)

https://pdfium.googlesource.com/pdfium.git/+log/5bc1f981df4d..671aece845dd

git log 5bc1f981df4d..671aece845dd --date=short --first-parent --format='%ad %ae %s'
2020-04-14 thestig@chromium.org Add FPDFAnnotEmbedderTest.FocusableAnnotRendering.
2020-04-14 thestig@chromium.org Update .gitignore after moving from YASM to NASM.
2020-04-14 tsepez@chromium.org Retain widgets across SetFocus() calls in CXFA_FFWidgetHandler.
2020-04-14 no-reply@google.com Mark static const class/struct members as constexpr
2020-04-14 tsepez@chromium.org Add missing brace to bug_1069700.in
2020-04-14 thestig@chromium.org Sanitize mouse wheel code.
2020-04-14 thestig@chromium.org Add FORM_OnMouseWheel().
2020-04-14 dhoss@chromium.org Add FPDF_GetFileIdentifier() to public API

Created with:
  gclient setdep -r src/third_party/pdfium@671aece845dd

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1069700,chromium:1069789
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ic36a9ccb58506e566bce820ea6a7b20595f610ad
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2149524
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#758994}

[modify] https://crrev.com/65723df7b5562a876ac0cc7f65fc77b967a49f0d/DEPS


### na...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-23)

Congrats the Panel decided to award $7,500 for this report!

### na...@google.com (2020-04-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-07-21)

This issue was migrated from crbug.com/chromium/1069789?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051986)*
