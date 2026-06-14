# Security: PDFium heap-use-after-free in CFDE_TextEditEngine::ReplaceSelectedText (XFA)

| Field | Value |
|-------|-------|
| **Issue ID** | [40051696](https://issues.chromium.org/issues/40051696) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | my...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2020-03-05 |
| **Bounty** | $5,000.00 |

## Description

PDFium heap-use-after-free in CFDE\_TextEditEngine::ReplaceSelectedText (XFA)

**VULNERABILITY DETAILS**

The bug is in function CFDE\_TextEditEngine::ReplaceSelectedText()

```
void CFDE_TextEditEngine::ReplaceSelectedText(const WideString& requested_rep) {  
...  
  
    delegate_->OnTextWillChange(&change);             // ==> trigger JS function => free object!  
    if (change.cancelled)  
      return;  
  
    rep = change.text;  
    selection_.start_idx = change.selection_start;    // ==> use again!!!   
    selection_.count = change.selection_end - change.selection_start;  
...  

```

**VERSION**  

Build lastest chromium with PDFium XFA is enabled

**REPRODUCTION CASE**

- Open file `test.pdf` in chrome.exe
- Click right mouse button and choose "Select All"
- Click right mouse button again and this time choose "Cut"

Stacktrace

00b7d6f0 26a2931c pdfium!CFDE\_TextEditEngine::ReplaceSelectedText(class fxcrt::WideString \* requested\_rep = 0x00b7d818)+0x140 [C:\Users\minhtt\Desktop\chromium\src\third\_party\pdfium\xfa\fde\cfde\_texteditengine.cpp @ 897]  

00b7d720 265ac6cd pdfium!CFWL\_Edit::Paste(class fxcrt::WideString \* wsPaste = 0x00b7d818)+0x5c [C:\Users\minhtt\Desktop\chromium\src\third\_party\pdfium\xfa\fwl\cfwl\_edit.cpp @ 242]  

00b7d738 265ac67f pdfium!CFWL\_ComboBox::EditPaste(class fxcrt::WideString \* wsPaste = 0x00b7d818)+0x2d [C:\Users\minhtt\Desktop\chromium\src\third\_party\pdfium\xfa\fwl\cfwl\_combobox.h @ 84]  

00b7d758 265e5d37 pdfium!CXFA\_FFComboBox::Paste(class fxcrt::WideString \* wsPaste = 0x00b7d818)+0x5f [C:\Users\minhtt\Desktop\chromium\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffcombobox.cpp @ 274]  

00b7d778 265a2bb5 pdfium!CXFA\_FFWidgetHandler::PasteText(class CXFA\_FFWidget \* widget = 0x39642f98, class fxcrt::WideString \* text = 0x00b7d818)+0x47 [C:\Users\minhtt\Desktop\chromium\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffwidgethandler.cpp @ 166]  

00b7d7ac 263c2b51 pdfium!CPDFXFA\_WidgetHandler::ReplaceSelection(class CPDFSDK\_Annot \* pAnnot = 0x2c724fd8, class fxcrt::WideString \* text = 0x00b7d818)+0x85 [C:\Users\minhtt\Desktop\chromium\src\third\_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_widgethandler.cpp @ 296]  

00b7d7d0 263f7513 pdfium!CPDFSDK\_AnnotHandlerMgr::Annot\_ReplaceSelection(class CPDFSDK\_Annot \* pAnnot = 0x2c724fd8, class fxcrt::WideString \* text = 0x00b7d818)+0x41 [C:\Users\minhtt\Desktop\chromium\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 95]  

00b7d7f4 26421f17 pdfium!CPDFSDK\_PageView::ReplaceSelection(class fxcrt::WideString \* text = 0x00b7d818)+0x63 [C:\Users\minhtt\Desktop\chromium\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_pageview.cpp @ 226]  

00b7d828 5e250935 pdfium!FORM\_ReplaceSelection(struct fpdf\_form\_handle\_t\_\_ \* hHandle = 0x389e2fb0, struct fpdf\_page\_t\_\_ \* page = 0x13b26fe8, unsigned short \* wsText = 0x00b7d868)+0x77 [C:\Users\minhtt\Desktop\chromium\src\third\_party\pdfium\fpdfsdk\fpdf\_formfill.cpp @ 530]  

00b7d924 5e274120 chrome!chrome\_pdf::PDFiumEngine::ReplaceSelection(class std::\_\_1::basic\_string<char,std::\_\_1::char\_traits<char>,std::\_\_1::allocator<char> > \* text = 0x00b7d96c "")+0x1c5 [C:\Users\minhtt\Desktop\chromium\src\pdf\pdfium\pdfium\_engine.cc @ 1984]  

00b7d93c 5e27cf04 chrome!chrome\_pdf::OutOfProcessInstance::ReplaceSelection(class std::\_\_1::basic\_string<char,std::\_\_1::char\_traits<char>,std::\_\_1::allocator<char> > \* text = 0x00b7d96c "")+0x30 [C:\Users\minhtt\Desktop\chromium\src\pdf\out\_of\_process\_instance.cc @ 1090]  

00b7d988 25dc3051 chrome!chrome\_pdf::`anonymous namespace'::ReplaceSelection(int instance = 0n1165093057, char \* text = 0x00b7db04 "")+0xa4 [C:\Users\minhtt\Desktop\chromium\src\pdf\out\_of\_process\_instance.cc @ 308]  

00b7d9b8 25dc1866 ppapi\_proxy!ppapi::CallWhileUnlocked<void,int,const char \*,int,const char \*>(<function> \* function = 0x5e27ce60, int \* p1 = 0x00b7d9e8, char \*\* p2 = 0x00b7d9d4)+0x51 [C:\Users\minhtt\Desktop\chromium\src\ppapi\shared\_impl\proxy\_lock.h @ 136]  

00b7d9e0 25dc5a82 ppapi\_proxy!ppapi::proxy::PPP\_Pdf\_Proxy::OnPluginMsgReplaceSelection(int instance = 0n1165093057, class std::\_\_1::basic\_string<char,std::\_\_1::char\_traits<char>,std::\_\_1::allocator<char> > \* text = 0x00b7db04 "")+0x56 [C:\Users\minhtt\Desktop\chromium\src\ppapi\proxy\ppp\_pdf\_proxy.cc @ 260]  

00b7da14 25dc59f4 ppapi\_proxy!base::DispatchToMethodImpl<ppapi::proxy::PPP\_Pdf\_Proxy \*,void (class ppapi::proxy::PPP\_Pdf\_Proxy \*\* obj = 0x00b7daa4, <function> \* method = 0x25dc1810, class std::\_\_1::tuple<int,std::\_\_1::basic\_string<char,std::\_\_1::char\_traits<char>,std::\_\_1::allocator<char> > > \* args = 0x00b7db00)+0x72 [C:\Users\minhtt\Desktop\chromium\src\base\tuple.h @ 53]  

00b7da5c 25dc596a ppapi\_proxy!base::DispatchToMethod<ppapi::proxy::PPP\_Pdf\_Proxy \*,void (class ppapi::proxy::PPP\_Pdf\_Proxy \*\* obj = 0x00b7daa4, <function> \* method = 0x25dc1810, class std::\_\_1::tuple<int,std::\_\_1::basic\_string<char,std::\_\_1::char\_traits<char>,std::\_\_1::allocator<char> > > \* args = 0x00b7db00)+0x74 [C:\Users\minhtt\Desktop\chromium\src\base\tuple.h @ 60]  

00b7da9c 25dc17bf ppapi\_proxy!IPC::DispatchToMethod<ppapi::proxy::PPP\_Pdf\_Proxy,void (class ppapi::proxy::PPP\_Pdf\_Proxy \* obj = 0x3812afe8, <function> \* method = 0x25dc1810, class std::\_\_1::tuple<int,std::\_\_1::basic\_string<char,std::\_\_1::char\_traits<char>,std::\_\_1::allocator<char> > > \* tuple = 0x00b7db00)+0x6a [C:\Users\minhtt\Desktop\chromium\src\ipc\ipc\_message\_templates.h @ 51]  

00b7db40 25dbf711 ppapi\_proxy!IPC::MessageT<PpapiMsg\_PPPPdf\_ReplaceSelection\_Meta,std::\_\_1::tuple<int,std::\_\_1::basic\_string<char,std::\_\_1::char\_traits<char>,std::\_\_1::allocator<char> > >,void>::Dispatch<ppapi::proxy::PPP\_Pdf\_Proxy,ppapi::proxy::PPP\_Pdf\_Proxy,void,void (class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\minhtt\Desktop\chromium\src\out\chromium\_pdfium\_xfa\message\_support.dll  

msg = 0x39ff0fb8 {size = 0x50}, class ppapi::proxy::PPP\_Pdf\_Proxy \* obj = 0x3812afe8, class ppapi::proxy::PPP\_Pdf\_Proxy \* sender = 0x3812afe8, void \* parameter = 0x00000000, <function> \* func = 0x25dc1810)+0x1ff [C:\Users\minhtt\Desktop\chromium\src\ipc\ipc\_message\_templates.h @ 140]  

00b7dcbc 25cea5e2 ppapi\_proxy!ppapi::proxy::PPP\_Pdf\_Proxy::OnMessageReceived(class IPC::Message \* msg = 0x39ff0fb8 {size = 0x50})+0x5b1 [C:\Users\minhtt\Desktop\chromium\src\ppapi\proxy\ppp\_pdf\_proxy.cc @ 187]  

00b7dd9c 25d49fff ppapi\_proxy!ppapi::proxy::Dispatcher::OnMessageReceived(class IPC::Message \* msg = 0x39ff0fb8 {size = 0x50})+0x132 [C:\Users\minhtt\Desktop\chromium\src\ppapi\proxy\dispatcher.cc @ 70]  

00b7de70 59891f67 ppapi\_proxy!ppapi::proxy::PluginDispatcher::OnMessageReceived(class IPC::Message \* msg = 0x39ff0fb8 {size = 0x50})+0x35f [C:\Users\minhtt\Desktop\chromium\src\ppapi\proxy\plugin\_dispatcher.cc @ 273]  

00b7de90 5989831f ipc!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message \* message = 0x39ff0fb8 {size = 0x50})+0x97 [C:\Users\minhtt\Desktop\chromium\src\ipc\ipc\_channel\_proxy.cc @ 327]  

00b7deb8 598981fc ipc!base::internal::FunctorTraits<void (<function> \* method = 0x59891ed0, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* receiver\_ptr = 0x39ff0fb0 [0x598efc00] 0x39ed2f00 {...}, class IPC::Message \* args = 0x39ff0fb8 {size = 0x50})+0x4f [C:\Users\minhtt\Desktop\chromium\src\base\bind\_internal.h @ 499]  

00b7def8 5989812f ipc!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x39ff0fa8, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* args = 0x39ff0fb0 [0x598efc00] 0x39ed2f00 {...}, class IPC::Message \* args = 0x39ff0fb8 {size = 0x50})+0x7c [C:\Users\minhtt\Desktop\chromium\src\base\bind\_internal.h @ 599]  

00b7df1c 598980ac ipc!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x39ff0fa8, class std::**1::tuple<scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);),IPC::Message> \* bound = 0x39ff0fb0)+0x6f [C:\Users\minhtt\Desktop\chromium\src\base\bind\_internal.h @ 672]  

00b7df44 66a123f1 ipc!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x39ff0f90)+0x5c [C:\Users\minhtt\Desktop\chromium\src\base\bind\_internal.h @ 641]  

00b7df68 66bd740b base!base::OnceCallback<void (void)+0x61 [C:\Users\minhtt\Desktop\chromium\src\base\callback.h @ 99]  

00b7e1f8 66c258c7 base!base::TaskAnnotator::RunTask(char \* trace\_event\_name = 0x66e2229e "SequenceManager RunTask", struct base::PendingTask \* pending\_task = 0x36a5ea08)+0x6eb [C:\Users\minhtt\Desktop\chromium\src\base\task\common\task\_annotator.cc @ 144]  

00b7e558 66c24e17 base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \* continuation\_lazy\_now = 0x00b7e5f8, bool \* ran\_task = 0x00b7e613)+0x807 [C:\Users\minhtt\Desktop\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 365]  

00b7e620 66ac060d base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xf7 [C:\Users\minhtt\Desktop\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 218]  

00b7e688 66c26de4 base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x36a22f2c)+0x9d [C:\Users\minhtt\Desktop\chromium\src\base\message\_loop\message\_pump\_default.cc @ 39]  

00b7e924 66b69674 base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application\_tasks\_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x394 [C:\Users\minhtt\Desktop\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 463]  

00b7ea88 54bf7cbd base!base::RunLoop::Run(void)+0x2f4 [C:\Users\minhtt\Desktop\chromium\src\base\run\_loop.cc @ 124]  

00b7ecac 58882924 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x00b7ed24)+0x60d [C:\Users\minhtt\Desktop\chromium\src\content\ppapi\_plugin\ppapi\_plugin\_main.cc @ 168]  

00b7ecd8 58883b99 content!content::RunOtherNamedProcessTypeMain(class std::1::basic\_string<char,std::1::char\_traits<char>,std::1::allocator<char> > \* process\_type = 0x00b7ed40 "ppapi", struct content::MainFunctionParams \* main\_function\_params = 0x00b7ed24, class content::ContentMainDelegate \* delegate = 0x00b7f350)+0xb4 [C:\Users\minhtt\Desktop\chromium\src\content\app\content\_main\_runner\_impl.cc @ 554]  

00b7eea0 5887efe0 content!content::ContentMainRunnerImpl::Run(bool start\_service\_manager\_only = false)+0x319 [C:\Users\minhtt\Desktop\chromium\src\content\app\content\_main\_runner\_impl.cc @ 880]  

00b7eeb8 2dc223b8 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\minhtt\Desktop\chromium\src\content\app\content\_service\_manager\_main\_delegate.cc @ 52]  

00b7f25c 58882730 embedder!service\_manager::Main(struct service\_manager::MainParams \* params = 0x00b7f288)+0x7a8 [C:\Users\minhtt\Desktop\chromium\src\services\service\_manager\embedder\main.cc @ 423]  

00b7f2b4 5a151376 content!content::ContentMain(struct content::ContentMainParams \* params = 0x00b7f330)+0x80 [C:\Users\minhtt\Desktop\chromium\src\content\app\content\_main.cc @ 20]  

00b7f3a0 0077550d chrome!ChromeMain(struct HINSTANCE \* instance = 0x00770000, struct sandbox::SandboxInterfaceInfo \* sandbox\_info = 0x00b7f40c, int64 exe\_entry\_point\_ticks = 0n231199174304)+0x246 [C:\Users\minhtt\Desktop\chromium\src\chrome\app\chrome\_main.cc @ 110]  

00b7f444 007717dc chrome\_exe!MainDllLoader::Launch(struct HINSTANCE \* instance = 0x00770000, class base::TimeTicks exe\_entry\_point\_ticks = class base::TimeTicks)+0x25d [C:\Users\minhtt\Desktop\chromium\src\chrome\app\main\_dll\_loader\_win.cc @ 177]  

00b7f7c8 0096967e chrome\_exe!wWinMain(struct HINSTANCE \* instance = 0x00770000, struct HINSTANCE** \* prev = 0x00000000)+0x7dc [C:\Users\minhtt\Desktop\chromium\src\chrome\app\chrome\_exe\_main\_win.cc @ 265]  

00b7f7e0 009697d1 chrome\_exe!invoke\_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 123]  

00b7f838 0096989d chrome\_exe!\_\_scrt\_common\_main\_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 283]  

00b7f840 009698a8 chrome\_exe!\_\_scrt\_common\_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 326]  

00b7f848 755e6359 chrome\_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_wwinmain.cpp @ 17]  

00b7f858 77b67b74 KERNEL32!BaseThreadInitThunk+0x19  

00b7f8b4 77b67b44 ntdll\_77b00000!\_\_RtlUserThreadStart+0x2f  

00b7f8c4 00000000 ntdll\_77b00000!\_RtlUserThreadStart+0x1b

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 6.8 KB)

## Timeline

### ts...@chromium.org (2020-03-05)

Gah, I fixed these for one class in https://pdfium-review.googlesource.com/c/pdfium/+/67170, but missed that there were other overrides.

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2020-03-05)

See https://pdfium-review.googlesource.com/c/pdfium/+/67270

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-05)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/8ecb862ae74dda3e98cfe7e027d0b7800514ee0f

commit 8ecb862ae74dda3e98cfe7e027d0b7800514ee0f
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Mar 05 19:56:06 2020

Retain layout item in all CFXA_FF.*::Paste() method overrides.

Covers cases missed by
  https://pdfium-review.googlesource.com/c/pdfium/+/67170

Bug: chromium:1058653
Change-Id: I9ede1c49d26bd0c37b80415b1ef30e5d318f79ca
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/67270
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/8ecb862ae74dda3e98cfe7e027d0b7800514ee0f/fpdfsdk/fpdf_formfill_embeddertest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/8ecb862ae74dda3e98cfe7e027d0b7800514ee0f/xfa/fxfa/cxfa_ffcombobox.h
[add] https://pdfium.googlesource.com/pdfium/+/8ecb862ae74dda3e98cfe7e027d0b7800514ee0f/testing/resources/bug_1058653.pdf
[modify] https://pdfium.googlesource.com/pdfium/+/8ecb862ae74dda3e98cfe7e027d0b7800514ee0f/xfa/fxfa/cxfa_ffdatetimeedit.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/8ecb862ae74dda3e98cfe7e027d0b7800514ee0f/xfa/fxfa/cxfa_ffcombobox.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/8ecb862ae74dda3e98cfe7e027d0b7800514ee0f/xfa/fxfa/cxfa_ffdatetimeedit.h
[add] https://pdfium.googlesource.com/pdfium/+/8ecb862ae74dda3e98cfe7e027d0b7800514ee0f/testing/resources/bug_1058653.in


### ts...@chromium.org (2020-03-05)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dc9689a6738e7dd7e2ee93dad052c1e07abdad48

commit dc9689a6738e7dd7e2ee93dad052c1e07abdad48
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Mar 05 23:04:59 2020

Roll src/third_party/pdfium a40862f237fc..8ecb862ae74d (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/a40862f237fc..8ecb862ae74d

git log a40862f237fc..8ecb862ae74d --date=short --first-parent --format='%ad %ae %s'
2020-03-05 tsepez@chromium.org Retain layout item in all CFXA_FF.*::Paste() method overrides.
2020-03-05 nigi@chromium.org Add FXSYS_IsLowerASCII().
2020-03-05 nigi@chromium.org Add a caller for FXSYS_ToUpperASCII() to simplify code.
2020-03-04 tsepez@chromium.org Retain layout item in a few more places where text changes.
2020-03-04 nigi@chromium.org Add FXSYS_IsUpperASCII().

Created with:
  gclient setdep -r src/third_party/pdfium@8ecb862ae74d

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/pdfium-autoroll
Please CC pdfium-deps-rolls@chromium.org on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

Bug: chromium:1055869,chromium:1058653
Tbr: pdfium-deps-rolls@chromium.org
Change-Id: I221c2f725aa0dce901bf6c3c8f2fd91c0aea28a3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2090223
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#747461}

[modify] https://crrev.com/dc9689a6738e7dd7e2ee93dad052c1e07abdad48/DEPS


### [Deleted User] (2020-03-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-09)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-11)

Congrats! The Panel decided to award $5,000 for this report!

### na...@google.com (2020-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-06-12)

This issue was migrated from crbug.com/chromium/1058653?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051696)*
