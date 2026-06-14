# Security: Crash in CPDF_Dictionary::GetObjectBy

| Field | Value |
|-------|-------|
| **Issue ID** | [40085057](https://issues.chromium.org/issues/40085057) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2016-08-09 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 54.0.2823.0  

Operating System: Windows 7

**REPRODUCTION CASE**

1. Open the test case
2. Scroll down and click on "Reset" (red button)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

rax=00000000002fcf98 rbx=00000000021b0fe1 rcx=00000000021b0fe1  

rdx=00000000002fcfd0 rsi=00000007fecdd92c rdi=00000007fecdd92c  

rip=000007fecd0d5ce1 rsp=00000000002fcf70 rbp=00000000002fd080  

r8=00000000002fd080 r9=000007fecaa00000 r10=000007fecdd916d0  

r11=0000000002682e80 r12=0000000000000000 r13=0000000000000000  

r14=00000000002fcfd0 r15=00000000002fd2b0  

iopl=0 nv up ei pl nz na pe nc  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00010202  

\*\*\* WARNING: Unable to verify checksum for chrome\_child.dll  

chrome\_child!std::\_Tree<std::\_Tmap\_traits<CFX\_ByteString,CFX\_FontFaceInfo \* \_\_ptr64,std::less<CFX\_ByteString>,std::allocator<std::pair<CFX\_ByteString const ,CFX\_FontFaceInfo \* \_\_ptr64> >,0> >::find+0x25:  

000007fe`cd0d5ce1 488b5e08 mov rbx,qword ptr [rsi+8] ds:00000007`fecdd934=????????????????  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it  

Child-SP RetAddr Call Site  

00000000`002fcf70 000007fe`ccfe362e chrome\_child!std::\_Tree<std::\_Tmap\_traits<CFX\_ByteString,CFX\_FontFaceInfo \* \_\_ptr64,std::less<CFX\_ByteString>,std::allocator<std::pair<CFX\_ByteString const ,CFX\_FontFaceInfo \* \_\_ptr64> >,0> >::find+0x25 [c:\b\depot\_tools\win\_toolchain\vs\_files\95ddda401ec5678f15eeed01d2bee08fcbc5ee97\vc\include\xtree @ 1488]  

00000000`002fcfa0 000007fe`ccfe343b chrome\_child!CPDF\_Dictionary::GetObjectBy+0x1a [c:\b\build\slave\win64\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_parser\cpdf\_dictionary.cpp @ 56]  

00000000`002fcfd0 000007fe`ccfe3668 chrome\_child!CPDF\_Dictionary::GetArrayBy+0xb [c:\b\build\slave\win64\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_parser\cpdf\_dictionary.cpp @ 117]  

00000000`002fd000 000007fe`cd03e155 chrome\_child!CPDF\_Dictionary::GetRectBy+0x20 [c:\b\build\slave\win64\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_parser\cpdf\_dictionary.cpp @ 127]  

00000000`002fd040 000007fe`ccfd8317 chrome\_child!CPDF\_Annot::GetRect+0x39 [c:\b\build\slave\win64\build\src\third\_party\pdfium\core\fpdfdoc\cpdf\_annot.cpp @ 48]  

00000000`002fd080 000007fe`ccfe01c6 chrome\_child!CPDFSDK\_BAAnnot::GetRect+0x1b [c:\b\build\slave\win64\build\src\third\_party\pdfium\fpdfsdk\fsdk\_baseannot.cpp @ 522]  

00000000`002fd0b0 000007fe`ccfde1c9 chrome\_child!CFFL\_Button::OnLButtonDown+0x26 [c:\b\build\slave\win64\build\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_formfiller.cpp @ 648]  

00000000`002fd110 000007fe`ccfdb6be chrome\_child!CFFL\_IFormFiller::OnLButtonDown+0x189 [c:\b\build\slave\win64\build\src\third\_party\pdfium\fpdfsdk\formfiller\cffl\_iformfiller.cpp @ 235]  

00000000`002fd1c0 000007fe`ccfdac45 chrome\_child!CPDFSDK\_BFAnnotHandler::OnLButtonDown+0x66 [c:\b\build\slave\win64\build\src\third\_party\pdfium\fpdfsdk\fsdk\_annothandler.cpp @ 524]  

00000000`002fd210 000007fe`ccfd76ab chrome\_child!CPDFSDK\_AnnotHandlerMgr::Annot\_OnLButtonDown+0x45 [c:\b\build\slave\win64\build\src\third\_party\pdfium\fpdfsdk\fsdk\_annothandler.cpp @ 162]  

00000000`002fd250 000007fe`ccfc6e00 chrome\_child!CPDFSDK\_PageView::OnLButtonDown+0x6f [c:\b\build\slave\win64\build\src\third\_party\pdfium\fpdfsdk\fsdk\_mgr.cpp @ 776]  

00000000`002fd290 000007fe`cc2cb093 chrome\_child!FORM\_OnLButtonDown+0x48 [c:\b\build\slave\win64\build\src\third\_party\pdfium\fpdfsdk\fpdfformfill.cpp @ 302]  

00000000`002fd2e0 000007fe`cc2ca02f chrome\_child!chrome\_pdf::PDFiumEngine::OnMouseDown+0x2b3 [c:\b\build\slave\win64\build\src\pdf\pdfium\pdfium\_engine.cc @ 1569]  

00000000`002fd3e0 000007fe`cc2d20a7 chrome\_child!chrome\_pdf::PDFiumEngine::HandleEvent+0xff [c:\b\build\slave\win64\build\src\pdf\pdfium\pdfium\_engine.cc @ 1183]  

00000000`002fd430 000007fe`cc2651be chrome\_child!chrome\_pdf::OutOfProcessInstance::HandleInputEvent+0x263 [c:\b\build\slave\win64\build\src\pdf\out\_of\_process\_instance.cc @ 525]  

00000000`002fd530 000007fe`cc828cb7 chrome\_child!pp::InputEvent\_HandleEvent+0x52 [c:\b\build\slave\win64\build\src\ppapi\cpp\module.cc @ 53]  

00000000`002fd570 000007fe`cc829211 chrome\_child!ppapi::CallWhileUnlocked<enum PP\_Bool,int,int,int,int>+0x23 [c:\b\build\slave\win64\build\src\ppapi\shared\_impl\proxy\_lock.h @ 135]  

00000000`002fd5a0 000007fe`cc828f23 chrome\_child!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMsgHandleFilteredInputEvent+0x69 [c:\b\build\slave\win64\build\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 107]  

00000000`002fd5e0 000007fe`cc829112 chrome\_child!IPC::MessageT<PpapiMsg\_PPPInputEvent\_HandleFilteredInputEvent\_Meta,std::tuple<int,ppapi::InputEventData>,std::tuple<enum PP\_Bool> >::Dispatch<ppapi::proxy::PPP\_InputEvent\_Proxy,ppapi::proxy::PPP\_InputEvent\_Proxy,void,void (\_\_cdecl ppapi::proxy::PPP\_InputEvent\_Proxy::\*)(int,ppapi::InputEventData const & \_\_ptr64,enum PP\_Bool \* \_\_ptr64) \_\_ptr64>+0x107 [c:\b\build\slave\win64\build\src\ipc\ipc\_message\_templates.h @ 174]  

00000000`002fd7a0 000007fe`cc7fddd2 chrome\_child!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMessageReceived+0xba [c:\b\build\slave\win64\build\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 85]

## Attachments

- [testcase.pdf](attachments/testcase.pdf) (application/pdf, 139.6 KB)
- [EHC_E_Fillable.pdf](attachments/EHC_E_Fillable.pdf) (application/pdf, 405.9 KB)

## Timeline

### oc...@chromium.org (2016-08-09)

weili, could you please take a look? looks like this might've been introduced in https://pdfium.googlesource.com/pdfium.git/+/5a6c1398d0e559fb6a048cb0dca46ba9f9309a77%5E%21/#F13:

   const auto& annots = m_pAnnotList->All();
-  return pdfium::ContainsValue(annots, p);
+  std::unique_ptr<const CPDF_Annot> annot(p);
+  return pdfium::ContainsValue(annots, annot);
 }


ASan stacktrace:

==4534==ERROR: AddressSanitizer: heap-use-after-free on address 0x604000234210 at pc 0x7f49f2b4560d bp 0x7ffee600f090 sp 0x7ffee600f088
READ of size 8 at 0x604000234210 thread T0 (chrome)
    #0 0x7f49f2b4560c in CPDF_Annot::GetRect(CFX_FloatRect&) const third_party/pdfium/core/fpdfdoc/cpdf_annot.cpp:46:8
    #1 0x7f49f29493e3 in CPDFSDK_BAAnnot::GetRect() const third_party/pdfium/fpdfsdk/fsdk_baseannot.cpp:521:13
    #2 0x7f49f296db7d in CFFL_Button::OnLButtonDown(CPDFSDK_PageView*, CPDFSDK_Annot*, unsigned int, CFX_FloatPoint const&) third_party/pdfium/fpdfsdk/formfiller/cffl_formfiller.cpp:647:35
    #3 0x7f49f2952b55 in CFFL_IFormFiller::OnLButtonDown(CPDFSDK_PageView*, CPDFSDK_Annot*, unsigned int, CFX_FloatPoint const&) third_party/pdfium/fpdfsdk/formfiller/cffl_iformfiller.cpp:232:25
    #4 0x7f49f293cc98 in CPDFSDK_BFAnnotHandler::OnLButtonDown(CPDFSDK_PageView*, CPDFSDK_Annot*, unsigned int, CFX_FloatPoint const&) third_party/pdfium/fpdfsdk/fsdk_annothandler.cpp:524:29
    #5 0x7f49f2938e8e in CPDFSDK_AnnotHandlerMgr::Annot_OnLButtonDown(CPDFSDK_PageView*, CPDFSDK_Annot*, unsigned int, CFX_FloatPoint const&) third_party/pdfium/fpdfsdk/fsdk_annothandler.cpp:159:27
    #6 0x7f49f2935531 in CPDFSDK_PageView::OnLButtonDown(CFX_FloatPoint const&, unsigned int) third_party/pdfium/fpdfsdk/fsdk_mgr.cpp:776:25
    #7 0x7f49f28eb476 in FORM_OnLButtonDown third_party/pdfium/fpdfsdk/fpdfformfill.cpp:301:21
    #8 0x7f49e3abadcc in chrome_pdf::PDFiumEngine::OnMouseDown(pp::MouseInputEvent const&) pdf/pdfium/pdfium_engine.cc:1568:5
    #9 0x7f49e3ab9ad2 in chrome_pdf::PDFiumEngine::HandleEvent(pp::InputEvent const&) pdf/pdfium/pdfium_engine.cc:1183:12
    #10 0x7f49e3b123ff in chrome_pdf::OutOfProcessInstance::HandleInputEvent(pp::InputEvent const&) pdf/out_of_process_instance.cc:525:16
    #11 0x7f49e38c99e9 in pp::InputEvent_HandleEvent(int, int) ppapi/cpp/module.cc:53:32
    #12 0x7f49e990c95a in CallWhileUnlocked<PP_Bool, int, int, int, int> ppapi/shared_impl/proxy_lock.h:135:10
    #13 0x7f49e990c95a in ppapi::proxy::PPP_InputEvent_Proxy::OnMsgHandleFilteredInputEvent(int, ppapi::InputEventData const&, PP_Bool*) ppapi/proxy/ppp_input_event_proxy.cc:107
    #14 0x7f49e990c3d9 in DispatchToMethodImpl<ppapi::proxy::PPP_InputEvent_Proxy *, void (ppapi::proxy::PPP_InputEvent_Proxy::*)(int, const ppapi::InputEventData &, PP_Bool *), int, ppapi::InputEventData, PP_Bool, 0, 1, 0> base/tuple.h:179:3
    #15 0x7f49e990c3d9 in DispatchToMethod<ppapi::proxy::PPP_InputEvent_Proxy *, void (ppapi::proxy::PPP_InputEvent_Proxy::*)(int, const ppapi::InputEventData &, PP_Bool *), int, ppapi::InputEventData, PP_Bool> base/tuple.h:188
    #16 0x7f49e990c3d9 in bool IPC::MessageT<PpapiMsg_PPPInputEvent_HandleFilteredInputEvent_Meta, std::__1::tuple<int, ppapi::InputEventData>, std::__1::tuple<PP_Bool> >::Dispatch<ppapi::proxy::PPP_InputEvent_Proxy, ppapi::proxy::PPP_InputEvent_Proxy, void, void (ppapi::proxy::PPP_InputEvent_Proxy::*)(int, ppapi::InputEventData const&, PP_Bool*)>(IPC::Message const*, ppapi::proxy::PPP_InputEvent_Proxy*, ppapi::proxy::PPP_InputEvent_Proxy*, void*, void (ppapi::proxy::PPP_InputEvent_Proxy::*)(int, ppapi::InputEventData const&, PP_Bool*)) ipc/ipc_message_templates.h:173
    #17 0x7f49e990b64a in ppapi::proxy::PPP_InputEvent_Proxy::OnMessageReceived(IPC::Message const&) ppapi/proxy/ppp_input_event_proxy.cc:85:5
    #18 0x7f49e9879803 in ppapi::proxy::Dispatcher::OnMessageReceived(IPC::Message const&) ppapi/proxy/dispatcher.cc:70:17
    #19 0x7f49e9885bc9 in ppapi::proxy::PluginDispatcher::OnMessageReceived(IPC::Message const&) ppapi/proxy/plugin_dispatcher.cc:252:22
    #20 0x7f49e8825a6a in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:314:14
    #21 0x7f49e4c44b95 in Run base/callback.h:389:12
    #22 0x7f49e4c44b95 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) base/debug/task_annotator.cc:54
    #23 0x7f49e4a70c25 in base::MessageLoop::RunTask(base::PendingTask const&) base/message_loop/message_loop.cc:496:19
    #24 0x7f49e4a71a1f in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask) base/message_loop/message_loop.cc:505:5
    #25 0x7f49e4a7305a in base::MessageLoop::DoWork() base/message_loop/message_loop.cc:629:13
    #26 0x7f49e4a7d9cd in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:35:31
    #27 0x7f49e4afdd59 in base::RunLoop::Run() base/run_loop.cc:35:10
    #28 0x7f49e384c1d0 in content::PpapiPluginMain(content::MainFunctionParams const&) content/ppapi_plugin/ppapi_plugin_main.cc:146:19
    #29 0x7f49e3aa2627 in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:343:14
    #30 0x7f49e3aa6e05 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:785:12
    #31 0x7f49e3aa13bd in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:20:28
    #32 0x7f49ddd5e5b5 in ChromeMain chrome/app/chrome_main.cc:85:12
    #33 0x7f49d2fd7f44 in __libc_start_main /build/eglibc-oGUzwX/eglibc-2.19/csu/libc-start.c:287


[Monorail components: Internals>Plugins>PDF]

### oc...@chromium.org (2016-08-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-10)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-08-10)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-08-11)

[Comment Deleted]

### ch...@gmail.com (2016-08-12)

I can repro this crash again with another PoC when I try to fill "date (yyyy-mm-dd)" option.

Almost every time when I open some PDF file contains "Rest or Print or Clear..." button and I click on some of them I get the crash. This should be fixed as soon as possible. Thanks!

### bu...@chromium.org (2016-08-16)

Any updates? M54 branch point is coming up and this is a Beta blocker.

### th...@chromium.org (2016-08-16)

It should be easy to fix. What ochang@ pointed is clearly wrong.

### th...@chromium.org (2016-08-16)

https://codereview.chromium.org/2242213004

### bu...@chromium.org (2016-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c0c3b125a5c48bae6486bbc8ab4c630c571e3afe

commit c0c3b125a5c48bae6486bbc8ab4c630c571e3afe
Author: thestig <thestig@chromium.org>
Date: Wed Aug 17 02:23:26 2016

Roll PDFium b469424..4674d95

https://pdfium.googlesource.com/pdfium.git/+log/b469424..4674d95

BUG=62625,635848
TBR=ochang@chromium.org

Review-Url: https://codereview.chromium.org/2245063005
Cr-Commit-Position: refs/heads/master@{#412427}

[modify] https://crrev.com/c0c3b125a5c48bae6486bbc8ab4c630c571e3afe/DEPS


### th...@chromium.org (2016-08-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-17)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-08-23)

Is this report qualified for a chromium security reward?


### mb...@chromium.org (2016-08-23)

I don't see any specific reason why it wouldn't be, but it's up to the reward panel to decide.

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

And indeed, the panel awarded $1,000 for this!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-11-23)

This issue was migrated from crbug.com/chromium/635848?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085057)*
