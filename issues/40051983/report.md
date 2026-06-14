# Security: PDFium (XFA) Use-after-free in function CPDFXFA_Page::GetFirstOrLastXFAAnnot

| Field | Value |
|-------|-------|
| **Issue ID** | [40051983](https://issues.chromium.org/issues/40051983) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-04-10 |
| **Bounty** | $5,000.00 |

## Description

PDFium (XFA) Use-after-free in function CPDFXFA\_Page::GetFirstOrLastXFAAnnot

**VERSION**

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**

Open file `poc.pdf` in chrome.exe  

Click on a blank space of the first page and press Shift-Tab

**VULNERABILITY DETAILS**

The bug is in function CPDFXFA\_Page::GetFirstOrLastXFAAnnot()

```
CPDFSDK_Annot\* CPDFXFA_Page::GetFirstOrLastXFAAnnot(CPDFSDK_PageView\* page_view,  
                                                    bool last) const {  
  CXFA_FFPageView\* xfa_page_view = GetXFAPageView();  
  if (!xfa_page_view)  
    return nullptr;  
  std::unique_ptr<IXFA_WidgetIterator> it =  
      xfa_page_view->CreateTraverseWidgetIterator(XFA_WidgetStatus_Visible |    // ==> trigger JS callback => free |page_view|   
                                                  XFA_WidgetStatus_Viewable |  
                                                  XFA_WidgetStatus_Focused);  
  
  return page_view->GetAnnotByXFAWidget(last ? it->MoveToLast()                 // ==> use again |page_view|  
                                             : it->MoveToFirst());  
}  

```

Function CreateTraverseWidgetIterator() can trigger JS callback => we can free CPDFSDK\_PageView object. After that, the  

freed object is used in calling function page\_view->GetAnnotByXFAWidget().

Crash log:

eax=00b7da14 ebx=fbbe7ba3 ecx=47932fdc edx=00b7da14 esi=ffffffff edi=47932fb0  

eip=3cc66da2 esp=00b7d9d0 ebp=00b7d9e4 iopl=0 nv up ei pl nz na po nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010202  

pdfium!std::\_\_1::vector<CPDFSDK\_Annot \*,std::\_\_1::allocator<CPDFSDK\_Annot \*> >::begin+0x12:  

3cc66da2 8b31 mov esi,dword ptr [ecx] ds:002b:47932fdc=????????

3:022> kp

# ChildEBP RetAddr

00 00b7d9e4 3cc9a6ba pdfium!std::**1::vector<CPDFSDK\_Annot \*,std::1::allocator<CPDFSDK\_Annot \*> >::begin(void)+0x12 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\buildtools\third\_party\libc++\trunk\include\vector @ 1516]  

01 00b7da1c 3ce52830 pdfium!CPDFSDK\_PageView::GetAnnotByXFAWidget(class CXFA\_FFWidget \* pWidget = 0x4fd6af98)+0x5a [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_pageview.cpp @ 190]  

02 00b7da60 3cc653e9 pdfium!CPDFXFA\_Page::GetFirstOrLastXFAAnnot(class CPDFSDK\_PageView \* page\_view = 0x47932fb0, bool last = true)+0xc0 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\third\_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_page.cpp @ 215]  

03 00b7dacc 3cc650ed pdfium!CPDFSDK\_AnnotHandlerMgr::GetFirstOrLastFocusableAnnot(class CPDFSDK\_PageView \* page\_view = 0x47932fb0, bool last = true)+0x89 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 360]  

04 00b7db38 3cc9c0b6 pdfium!CPDFSDK\_AnnotHandlerMgr::Annot\_OnKeyDown(class CPDFSDK\_PageView \* pPageView = 0x47932fb0, class CPDFSDK\_Annot \* pAnnot = 0x00000000, int nKeyCode = 0n9, int nFlag = 0n1025)+0xad [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 247]  

05 00b7db74 3ccc69c9 pdfium!CPDFSDK\_PageView::OnKeyDown(int nKeyCode = 0n9, int nFlag = 0n1025)+0x76 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_pageview.cpp @ 472]  

06 00b7dba8 1acf116d pdfium!FORM\_OnKeyDown(struct fpdf\_form\_handle\_t \* hHandle = 0x4ef7afa8, struct fpdf\_page\_t** \* page = 0x16358fe8, int nKeyCode = 0n9, int modifier = 0n1025)+0x69 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\third\_party\pdfium\fpdfsdk\fpdf\_formfill.cpp @ 476]  

07 00b7dc60 1acf0110 chrome!chrome\_pdf::PDFiumEngine::OnKeyDown(class pp::KeyboardInputEvent \* event = 0x00b7dd98)+0xbd [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\pdf\pdfium\pdfium\_engine.cc @ 1497]  

08 00b7de70 1ad1c396 chrome!chrome\_pdf::PDFiumEngine::HandleEvent(class pp::InputEvent \* event = 0x00b7dfe0)+0x250 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\pdf\pdfium\pdfium\_engine.cc @ 791]  

09 00b7dff8 195391f6 chrome!chrome\_pdf::OutOfProcessInstance::HandleInputEvent(class pp::InputEvent \* event = 0x00b7e028)+0x6e6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\pdf\out\_of\_process\_instance.cc @ 871]  

0a 00b7e038 3b867361 chrome!pp::InputEvent\_HandleEvent(int pp\_instance = 0n-412024135, int resource = 0n230)+0xa6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\ppapi\cpp\module.cc @ 53]  

0b 00b7e06c 3b8672e3 ppapi\_proxy!ppapi::CallWhileUnlocked<PP\_Bool,int,int,int,int>(<function> \* function = 0x19539150, int \* p1 = 0x00b7e0c0, int \* p2 = 0x00b7e0a4)+0x51 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\ppapi\shared\_impl\proxy\_lock.h @ 136]  

0c 00b7e0b8 3b867e2e ppapi\_proxy!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMsgHandleFilteredInputEvent(int instance = 0n-412024135, struct ppapi::InputEventData \* data = 0x00b7e290, <unnamed-tag> \* result = 0x00b7e1dc)+0xb3 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 107]  

0d 00b7e0fc 3b867d58 ppapi\_proxy!base::DispatchToMethodImpl<ppapi::proxy::PPP\_InputEvent\_Proxy \*,void (class ppapi::proxy::PPP\_InputEvent\_Proxy \*\* obj = 0x00b7e368, <function> \* method = 0x3b867230, class std::\_\_1::tuple<int,ppapi::InputEventData> \* in = 0x00b7e288, class std::\_\_1::tuple<PP\_Bool> \* out = 0x00b7e1dc)+0x8e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\tuple.h @ 96]  

0e 00b7e160 3b86719b ppapi\_proxy!base::DispatchToMethod<ppapi::proxy::PPP\_InputEvent\_Proxy \*,void (class ppapi::proxy::PPP\_InputEvent\_Proxy \*\* obj = 0x00b7e368, <function> \* method = 0x3b867230, class std::\_\_1::tuple<int,ppapi::InputEventData> \* in = 0x00b7e288, class std::\_\_1::tuple<PP\_Bool> \* out = 0x00b7e1dc)+0x98 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\tuple.h @ 105]  

0f 00b7e35c 3b866a59 ppapi\_proxy!IPC::MessageT<PpapiMsg\_PPPInputEvent\_HandleFilteredInputEvent\_Meta,std::\_\_1::tuple<int,ppapi::InputEventData>,std::\_\_1::tuple<PP\_Bool> >::Dispatch<ppapi::proxy::PPP\_InputEvent\_Proxy,ppapi::proxy::PPP\_InputEvent\_Proxy,void,void (class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\out\chromium\_pdfium\_xfa\message\_support.dll  

msg = 0x4aeb4fb8 {size = 0x90}, class ppapi::proxy::PPP\_InputEvent\_Proxy \* obj = 0x400bcfe8, class ppapi::proxy::PPP\_InputEvent\_Proxy \* sender = 0x400bcfe8, <function> \* func = 0x3b867230)+0x35b [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\ipc\ipc\_message\_templates.h @ 198]  

10 00b7e3d4 3b79a5e2 ppapi\_proxy!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMessageReceived(class IPC::Message \* msg = 0x4aeb4fb8 {size = 0x90})+0x179 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 85]  

11 00b7e4b4 3b7fa1ff ppapi\_proxy!ppapi::proxy::Dispatcher::OnMessageReceived(class IPC::Message \* msg = 0x4aeb4fb8 {size = 0x90})+0x132 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\ppapi\proxy\dispatcher.cc @ 70]  

12 00b7e588 20372197 ppapi\_proxy!ppapi::proxy::PluginDispatcher::OnMessageReceived(class IPC::Message \* msg = 0x4aeb4fb8 {size = 0x90})+0x35f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\ppapi\proxy\plugin\_dispatcher.cc @ 273]  

13 00b7e5a8 2037854f ipc!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message \* message = 0x4aeb4fb8 {size = 0x90})+0x97 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\ipc\ipc\_channel\_proxy.cc @ 327]  

14 00b7e5d0 2037842c ipc!base::internal::FunctorTraits<void (<function> \* method = 0x20372100, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* receiver\_ptr = 0x4aeb4fb0 [0x203cfc20] 0x1370af00 {...}, class IPC::Message \* args = 0x4aeb4fb8 {size = 0x90})+0x4f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\bind\_internal.h @ 499]  

15 00b7e610 2037835f ipc!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x4aeb4fa8, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* args = 0x4aeb4fb0 [0x203cfc20] 0x1370af00 {...}, class IPC::Message \* args = 0x4aeb4fb8 {size = 0x90})+0x7c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\bind\_internal.h @ 599]  

16 00b7e634 203782dc ipc!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x4aeb4fa8, class std::**1::tuple<scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);),IPC::Message> \* bound = 0x4aeb4fb0)+0x6f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\bind\_internal.h @ 672]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\out\chromium\_pdfium\_xfa\base.dll  

17 00b7e65c 50c023f1 ipc!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x4aeb4f90)+0x5c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\bind\_internal.h @ 641]  

18 00b7e680 50dd60ab base!base::OnceCallback<void (void)+0x61 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\callback.h @ 99]  

19 00b7e910 50e24667 base!base::TaskAnnotator::RunTask(char \* trace\_event\_name = 0x5102288e "SequenceManager RunTask", struct base::PendingTask \* pending\_task = 0x4cd64a08)+0x6eb [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\task\common\task\_annotator.cc @ 144]  

1a 00b7ec70 50e23bac base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \* continuation\_lazy\_now = 0x00b7ed10, bool \* ran\_task = 0x00b7ed2f)+0x807 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 408]  

1b 00b7ed40 50cb076d base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0x11c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 247]  

1c 00b7eda8 50e25bf4 base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x4cd28efc)+0x9d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\message\_loop\message\_pump\_default.cc @ 39]  

1d 00b7f044 50d682b4 base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application\_tasks\_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x394 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 513]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\out\chromium\_pdfium\_xfa\content.dll  

1e 00b7f1a8 204b821d base!base::RunLoop::Run(void)+0x2f4 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\base\run\_loop.cc @ 124]  

1f 00b7f3cc 241cec24 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x00b7f444)+0x60d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\content\ppapi\_plugin\ppapi\_plugin\_main.cc @ 168]  

20 00b7f3f8 241cff29 content!content::RunOtherNamedProcessTypeMain(class std::1::basic\_string<char,std::1::char\_traits<char>,std::1::allocator<char> > \* process\_type = 0x00b7f460 "ppapi", struct content::MainFunctionParams \* main\_function\_params = 0x00b7f444, class content::ContentMainDelegate \* delegate = 0x00b7fa70)+0xb4 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\content\app\content\_main\_runner\_impl.cc @ 554]  

21 00b7f5c0 241cb2e0 content!content::ContentMainRunnerImpl::Run(bool start\_service\_manager\_only = false)+0x319 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\content\app\content\_main\_runner\_impl.cc @ 881]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\out\chromium\_pdfium\_xfa\embedder.dll  

22 00b7f5d8 7b4423b8 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\content\app\content\_service\_manager\_main\_delegate.cc @ 52]  

23 00b7f97c 241cea30 embedder!service\_manager::Main(struct service\_manager::MainParams \* params = 0x00b7f9a8)+0x7a8 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\services\service\_manager\embedder\main.cc @ 423]  

24 00b7f9d4 16b61376 content!content::ContentMain(struct content::ContentMainParams \* params = 0x00b7fa50)+0x80 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\content\app\content\_main.cc @ 20]  

\*\*\* WARNING: Unable to verify checksum for chrome.exe  

25 00b7fac8 004e56bd chrome!ChromeMain(struct HINSTANCE \* instance = 0x004e0000, struct sandbox::SandboxInterfaceInfo \* sandbox\_info = 0x00b7fb34, int64 exe\_entry\_point\_ticks = 0n2021579595359)+0x246 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\chrome\app\chrome\_main.cc @ 110]  

26 00b7fb6c 004e1826 chrome\_exe!MainDllLoader::Launch(struct HINSTANCE \* instance = 0x004e0000, class base::TimeTicks exe\_entry\_point\_ticks = class base::TimeTicks)+0x25d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\chrome\app\main\_dll\_loader\_win.cc @ 177]  

27 00b7fef0 006dba3e chrome\_exe!wWinMain(struct HINSTANCE \* instance = 0x004e0000, struct HINSTANCE** \* prev = 0x00000000)+0x826 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_03\_2020\src\chrome\app\chrome\_exe\_main\_win.cc @ 271]  

28 00b7ff08 006dbb91 chrome\_exe!invoke\_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 123]  

29 00b7ff60 006dbc5d chrome\_exe!\_\_scrt\_common\_main\_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 283]  

2a 00b7ff68 006dbc68 chrome\_exe!\_\_scrt\_common\_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 326]  

2b 00b7ff70 74936359 chrome\_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_wwinmain.cpp @ 17]  

2c 00b7ff80 77197b74 KERNEL32!BaseThreadInitThunk+0x19  

2d 00b7ffdc 77197b44 ntdll!\_\_RtlUserThreadStart+0x2f  

2e 00b7ffec 00000000 ntdll!\_RtlUserThreadStart+0x1b

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 9.5 KB)
- [log_crash.txt](attachments/log_crash.txt) (text/plain, 18.1 KB)

## Timeline

### xi...@chromium.org (2020-04-10)

Setting Sev-High for UAF but Impact-None since we don't ship XFA by default.

tsepez@ could you take a look at this one? Thanks!

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2020-04-10)

From https://pdfium-review.googlesource.com/65810

### th...@chromium.org (2020-04-10)

Add an ObservedPtr<CPDFSDK_PageView>?

### ts...@chromium.org (2020-04-13)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-04-13)

CL at https://pdfium-review.googlesource.com/c/pdfium/+/68710

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-13)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/fe0cadf616ef87ca894bf4cd7cd645981cbef9f7

commit fe0cadf616ef87ca894bf4cd7cd645981cbef9f7
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Apr 13 22:18:14 2020

Observe pagview across JS invocation in cpdfxfa_page.cpp

Bug: chromium:1069700
Change-Id: I68db0b17dc8cc7146a18d7caf88334f75b3d31fc
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/68710
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[add] https://pdfium.googlesource.com/pdfium/+/fe0cadf616ef87ca894bf4cd7cd645981cbef9f7/testing/resources/javascript/xfa_specific/bug_1069700.evt
[modify] https://pdfium.googlesource.com/pdfium/+/fe0cadf616ef87ca894bf4cd7cd645981cbef9f7/fpdfsdk/fpdfxfa/cpdfxfa_page.cpp
[add] https://pdfium.googlesource.com/pdfium/+/fe0cadf616ef87ca894bf4cd7cd645981cbef9f7/testing/resources/javascript/xfa_specific/bug_1069700.in


### ts...@google.com (2020-04-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9c28c972d82158adf8f7727567f016a73e8d8b61

commit 9c28c972d82158adf8f7727567f016a73e8d8b61
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Apr 14 03:14:31 2020

Roll src/third_party/pdfium e6e9fec904b8..5bc1f981df4d (7 commits)

https://pdfium.googlesource.com/pdfium.git/+log/e6e9fec904b8..5bc1f981df4d

git log e6e9fec904b8..5bc1f981df4d --date=short --first-parent --format='%ad %ae %s'
2020-04-14 dhoss@chromium.org Add a helper to copy a ByteString to a buffer
2020-04-13 thestig@chromium.org Remove third_party/yasm from DEPS.
2020-04-13 thestig@chromium.org Roll third_party/libjpeg_turbo/ ce0e57e8e..7e3ad7980 (4 commits)
2020-04-13 thestig@chromium.org Add third_party/nasm to DEPS.
2020-04-13 thestig@chromium.org Fix nits in the DEPS file.
2020-04-13 tsepez@chromium.org Remove some needless locals from cxfa_ffwidgethandler.cpp
2020-04-13 tsepez@chromium.org Observe pagview across JS invocation in cpdfxfa_page.cpp

Created with:
  gclient setdep -r src/third_party/pdfium@5bc1f981df4d

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1069700,chromium:766721
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I2ec868838e528a83adbec69b7b1f1e00448e91eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2148166
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#758703}

[modify] https://crrev.com/9c28c972d82158adf8f7727567f016a73e8d8b61/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/74d34da5afcb06f4642f7f9c9afc671e94a769bb

commit 74d34da5afcb06f4642f7f9c9afc671e94a769bb
Author: Tom Sepez <tsepez@chromium.org>
Date: Tue Apr 14 16:40:03 2020

Add missing brace to bug_1069700.in

Although this prevented proper replacement in the generated PDF file,
the missing section did not affect the correctness of the test.

Bug: chromium:1069700
Change-Id: Ia3dc81f4633be97de9f6b90380e02623afe28eee
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/68750
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Auto-Submit: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/74d34da5afcb06f4642f7f9c9afc671e94a769bb/testing/resources/javascript/xfa_specific/bug_1069700.in


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

Congrats the Panel decided to award $5,000 for this report!

### na...@google.com (2020-04-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-07-21)

This issue was migrated from crbug.com/chromium/1069700?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051983)*
