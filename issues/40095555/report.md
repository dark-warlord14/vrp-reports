# Security: PDFium (XFA) Use-after-free in CXFA_FFDocView::GetPageView

| Field | Value |
|-------|-------|
| **Issue ID** | [40095555](https://issues.chromium.org/issues/40095555) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-07-01 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use-after-free CXFA\_FFPageView object in function CXFA\_FFDocView::GetPageView

**VERSION**  

Operating System: Windows 10 64bit  

Chrome with enabled XFA PDFium

**REPRODUCTION CASE**  

Open file `poc.pdf` in chrome.exe with PageHeap is enabled  

Scroll to the second page, click to edit box and press `Tab` key (MUST `Tab` key) to trigger crash

CRASH INFORMATION

This exception may be expected and handled.  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\pdfium.dll  

eax=464a8ff4 ebx=24b0cfd8 ecx=464a8ff4 edx=00000000 esi=444ccff0 edi=dac0e126  

eip=7787a72f esp=00afbe28 ebp=00afbe2c iopl=0 nv up ei pl nz ac po nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010212  

pdfium!std::\_\_1::unique\_ptr >::get+0xf:  

7787a72f 8b00 mov eax,dword ptr [eax] ds:002b:464a8ff4=????????

3:025> kp

# ChildEBP RetAddr

00 00afbe2c 77878634 pdfium!std::\_\_1::unique\_ptr<CXFA\_FFPageView,std::\_\_1::default\_delete<CXFA\_FFPageView> >::get(void)+0xf [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\buildtools\third\_party\libc++\trunk\include\memory @ 2624]  

01 00afbe38 778785fd pdfium!CXFA\_ViewLayoutItem::GetPageView(void)+0x14 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_viewlayoutitem.h @ 22]  

02 00afbe60 778642ee pdfium!CXFA\_FFDocView::GetPageView(int nIndex = 0n0)+0x6d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp @ 204]  

03 00afbe7c 7785ce03 pdfium!CPDFXFA\_Page::GetXFAPageView(void)+0x3e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_page.cpp @ 53]  

04 00afbec8 778612ec pdfium!CPDFXFA\_Context::GetXFAPage(class CXFA\_FFPageView \* pPage = 0x444ccff0)+0x123 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_context.cpp @ 184]  

05 00afbf04 77889128 pdfium!CPDFXFA\_DocEnvironment::WidgetPreRemove(class CXFA\_FFWidget \* hWidget = 0x3ea5cfa8)+0x8c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\fpdfxfa\cpdfxfa\_docenvironment.cpp @ 337]  

06 00afbf30 77d0b304 pdfium!CXFA\_FFNotify::OnLayoutItemRemoving(class CXFA\_LayoutProcessor \* pLayout = 0x4065cfd8, class CXFA\_LayoutItem \* pSender = 0x3ea62fb8)+0x98 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffnotify.cpp @ 491]  

07 00afbf64 77d0b2b9 pdfium!XFA\_ReleaseLayoutItem(class CXFA\_LayoutItem \* pLayoutItem = 0x3ea62fb8)+0x84 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_layoutitem.cpp @ 28]  

08 00afbf98 77d0b2b9 pdfium!XFA\_ReleaseLayoutItem(class CXFA\_LayoutItem \* pLayoutItem = 0x3ef2efb8)+0x39 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_layoutitem.cpp @ 23]  

09 00afbfcc 77d0b2b9 pdfium!XFA\_ReleaseLayoutItem(class CXFA\_LayoutItem \* pLayoutItem = 0x3edc0fd0)+0x39 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_layoutitem.cpp @ 23]  

0a 00afc000 77d0b2b9 pdfium!XFA\_ReleaseLayoutItem(class CXFA\_LayoutItem \* pLayoutItem = 0x464d6fd0)+0x39 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_layoutitem.cpp @ 23]  

0b 00afc034 77d0c1aa pdfium!XFA\_ReleaseLayoutItem(class CXFA\_LayoutItem \* pLayoutItem = 0x4649efd0)+0x39 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_layoutitem.cpp @ 23]  

0c 00afc06c 77d0ba0a pdfium!CXFA\_LayoutPageMgr::PrepareLayout(void)+0xba [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_layoutpagemgr.cpp @ 1914]  

0d 00afc164 77d1817e pdfium!CXFA\_LayoutPageMgr::InitLayoutPage(class CXFA\_Node \* pFormNode = 0x32a52f80)+0x2a [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_layoutpagemgr.cpp @ 370]  

0e 00afc1bc 77d186e8 pdfium!CXFA\_LayoutProcessor::StartLayout(bool bForceRestart = true)+0x13e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_layoutprocessor.cpp @ 55]  

0f 00afc1d8 77877c3e pdfium!CXFA\_LayoutProcessor::IncrementLayout(void)+0x28 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\layout\cxfa\_layoutprocessor.cpp @ 107]  

10 00afc204 77878155 pdfium!CXFA\_FFDocView::RunLayout(void)+0x2e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp @ 447]  

11 00afc23c 77888520 pdfium!CXFA\_FFDocView::UpdateDocView(void)+0xf5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp @ 188]  

12 00afc258 7782f2b5 pdfium!CXFA\_FFNotify::OpenDropDownList(class CXFA\_FFWidget \* hWidget = 0x42d33fa8)+0x70 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffnotify.cpp @ 262]  

13 00afc320 7782dcbe pdfium!CJX\_HostPseudoModel::openList(class CFX\_V8 \* runtime = 0x3770af98, class std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);),std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > \* params = 0x00afc438 { size=1 })+0x445 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cjx\_hostpseudomodel.cpp @ 316]  

14 00afc358 7783d5d3 pdfium!CJX\_HostPseudoModel::openList\_static(class CJX\_Object \* node = 0x24b0cfd8, class CFX\_V8 \* runtime = 0x3770af98, class std::\_\_1::vector<v8::Local[v8::Value](javascript:void(0);),std::\_\_1::allocator<v8::Local[v8::Value](javascript:void(0);) > > \* params = 0x00afc438 { size=1 })+0x7e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cjx\_hostpseudomodel.h @ 33]  

15 00afc3b0 777e79bc pdfium!CJX\_Object::RunMethod(class fxcrt::WideString \* func = 0x00afc584, class std::**1::vector<v8::Local[v8::Value](javascript:void(0);),std::1::allocator<v8::Local[v8::Value](javascript:void(0);) > > \* params = 0x00afc438 { size=1 })+0x103 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cjx\_object.cpp @ 179]  

16 00afc458 777e1b72 pdfium!CFXJSE\_Engine::NormalMethodCall(class v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) \* info = 0x00afc5f0, class fxcrt::WideString \* functionName = 0x00afc584)+0x1fc [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cfxjse\_engine.cpp @ 459]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\v8.dll  

17 00afc5d4 50c6d5f1 pdfium!`anonymous namespace'::DynPropGetterAdapter_MethodCallback(class v8::FunctionCallbackInfo<v8::Value> \* info = 0x00afc5f0)+0x382 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\third_party\pdfium\fxjs\xfa\cfxjse_class.cpp @ 111] 18 00afc648 50c6c056 v8!v8::internal::FunctionCallbackArguments::Call(class v8::internal::CallHandlerInfo handler = class v8::internal::CallHandlerInfo)+0x251 [C:\Users\huyna_dev\Desktop\chromium\chromium_pdfium_XFA\src\v8\src\api\api-arguments-inl.h @ 158] 19 00afc6b4 50c6a72f v8!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(class v8::internal::Isolate \* isolate = <Value unavailable error>, class v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);) function = class v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), class v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);) new\_target = class v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), class v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);) fun\_data = class v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), class v8::internal::Handle[v8::internal::Object](javascript:void(0);) receiver = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments)+0x316 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\v8\src\builtins\builtins-api.cc @ 113]  

1a 00afc708 50c6a2d2 v8!v8::internal::Builtin\_Impl\_HandleApiCall(class v8::internal::BuiltinArguments args = class v8::internal::BuiltinArguments, class v8::internal::Isolate \* isolate = 0x42cf2b58)+0x18f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\v8\src\builtins\builtins-api.cc @ 141]  

1b 00afc780 519f5fc3 v8!v8::internal::Builtin\_HandleApiCall(int args\_length = 0n6, unsigned int \* args\_object = 0x00afc7bc, class v8::internal::Isolate \* isolate = 0x42cf2b58)+0x72 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\v8\src\builtins\builtins-api.cc @ 129]  

1c 00afc7a0 517e7c1c v8!Builtins\_CEntry\_Return1\_DontSaveFPRegs\_ArgvOnStack\_BuiltinExit+0x43  

1d 00afc7e8 517d481c v8!Builtins\_InterpreterEntryTrampoline+0x31c  

1e 00afc804 517e7c1c v8!Builtins\_ArgumentsAdaptorTrampoline+0xbc  

1f 00afc84c 517d481c v8!Builtins\_InterpreterEntryTrampoline+0x31c  

20 00afc868 517e7c1c v8!Builtins\_ArgumentsAdaptorTrampoline+0xbc  

21 00afc8b0 517d481c v8!Builtins\_InterpreterEntryTrampoline+0x31c  

22 00afc8cc 517dff3f v8!Builtins\_ArgumentsAdaptorTrampoline+0xbc  

23 00afc8e4 517dfd5b v8!Builtins\_JSEntryTrampoline+0x5f  

24 00afc910 50da3795 v8!Builtins\_JSEntry+0x5b  

25 (Inline) -------- v8!v8::internal::GeneratedCode<unsigned int,unsigned int,unsigned int,unsigned int,unsigned int,int,unsigned int \*\*>::Call+0xf [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\v8\src\execution\simulator.h @ 138]  

26 00afc9cc 50da2eae v8!v8::internal::`anonymous namespace'::Invoke(class v8::internal::Isolate \* isolate = <Value unavailable error>, struct v8::internal::`anonymous namespace'::InvokeParams \* params = 0x00afc9d8)+0x8d5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\v8\src\execution\execution.cc @ 264]  

27 00afca10 50bc53d5 v8!v8::internal::Execution::Call(class v8::internal::Isolate \* isolate = 0x42cf2b58, class v8::internal::Handle[v8::internal::Object](javascript:void(0);) callable = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), class v8::internal::Handle[v8::internal::Object](javascript:void(0);) receiver = class v8::internal::Handle[v8::internal::Object](javascript:void(0);), int argc = 0n1, class v8::internal::Handle[v8::internal::Object](javascript:void(0);) \* argv = 0x00afcddc)+0x6e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\v8\src\execution\execution.cc @ 356]  

28 00afcac8 777e42d0 v8!v8::Function::Call(class v8::Local[v8::Context](javascript:void(0);) context = class v8::Local[v8::Context](javascript:void(0);), class v8::Local[v8::Value](javascript:void(0);) recv = class v8::Local[v8::Value](javascript:void(0);), int argc = 0n1, class v8::Local[v8::Value](javascript:void(0);) \* argv = 0x00afcddc)+0x2f5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\v8\src\api\api.cc @ 4793]  

29 00afcdf0 777e9679 pdfium!CFXJSE\_Context::ExecuteScript(char \* szScript = 0x5a0f001c "eval('try { if (aaaa == 1) {xfa.host.setFocus(field\_DropDownList1);xfa.template.remerge();xfa.host.openList(field\_DropDownList1);} } catch(e){xfa.host.beep(2);}') == 0", class CFXJSE\_Value \* lpRetValue = 0x248d0ff0, class CFXJSE\_Value \* lpNewThisObject = 0x3e516ff0)+0x9b0 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cfxjse\_context.cpp @ 300]  

2a 00afced0 7781e7c2 pdfium!CFXJSE\_Engine::RunScript(CXFA\_Script::Type eScriptType = Javascript (0n1), class fxcrt::StringViewTemplate<wchar\_t> wsScript = class fxcrt::StringViewTemplate<wchar\_t>, class CFXJSE\_Value \* hRetValue = 0x248d0ff0, class CXFA\_Object \* pThisObject = 0x4061cf80)+0x349 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cfxjse\_engine.cpp @ 153]  

2b 00afcf90 7781b508 pdfium!`anonymous namespace'::DoPredicateFilter(class fxcrt::WideString wsCondition = class fxcrt::WideString, unsigned int iFoundCount = 1, class CFXJSE\_ResolveNodeData \* pRnd = 0x00afd290)+0x2e2 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cfxjse\_resolveprocessor.cpp @ 47]  

2c 00afd034 7781a836 pdfium!CFXJSE\_ResolveProcessor::FilterCondition(class fxcrt::WideString wsCondition = class fxcrt::WideString, class CFXJSE\_ResolveNodeData \* pRnd = 0x00afd290)+0x398 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cfxjse\_resolveprocessor.cpp @ 697]  

2d 00afd0b8 77819d61 pdfium!CFXJSE\_ResolveProcessor::ResolveDollar(class CFXJSE\_ResolveNodeData \* rnd = 0x00afd290)+0x1f6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cfxjse\_resolveprocessor.cpp @ 174]  

2e 00afd13c 777ea2e5 pdfium!CFXJSE\_ResolveProcessor::Resolve(class CFXJSE\_ResolveNodeData \* rnd = 0x00afd290)+0x161 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cfxjse\_resolveprocessor.cpp @ 80]  

2f 00afd2d8 778792b0 pdfium!CFXJSE\_Engine::ResolveObjects(class CXFA\_Object \* refObject = 0x3dfd8f80, class fxcrt::StringViewTemplate<wchar\_t> wsExpression = class fxcrt::StringViewTemplate<wchar\_t>, struct XFA\_RESOLVENODE\_RS \* resolveNodeRS = 0x00afd340, unsigned int dwStyles = 0x69, class CXFA\_Node \* bindNode = 0x00000000)+0x615 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fxjs\xfa\cfxjse\_engine.cpp @ 661]  

30 00afd36c 77890657 pdfium!CXFA\_FFDocView::GetWidgetByName(class fxcrt::WideString \* wsName = 0x00afd3d0, class CXFA\_FFWidget \* pRefWidget = 0x3ea5cfa8)+0x120 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffdocview.cpp @ 420]  

31 00afd38c 778904f0 pdfium!CXFA\_FFTabOrderPageWidgetIterator::FindWidgetByName(class fxcrt::WideString \* wsWidgetName = 0x00afd3d0, class CXFA\_FFWidget \* pRefWidget = 0x3ea5cfa8)+0x37 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 335]  

32 00afd3d8 7788fbd5 pdfium!CXFA\_FFTabOrderPageWidgetIterator::GetTraverseWidget(class CXFA\_FFWidget \* pWidget = 0x3ea5cfa8)+0xf0 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 327]  

33 00afd460 7788f916 pdfium!CXFA\_FFTabOrderPageWidgetIterator::CreateTabOrderWidgetArray(void)+0x235 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 370]  

34 00afd470 7788f8b6 pdfium!CXFA\_FFTabOrderPageWidgetIterator::Reset(void)+0x16 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 247]  

35 00afd4a0 7788e6dc pdfium!CXFA\_FFTabOrderPageWidgetIterator::CXFA\_FFTabOrderPageWidgetIterator(class CXFA\_FFPageView \* pPageView = 0x444ccff0, unsigned int dwFilter = 0x188)+0xa6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 241]  

36 00afd4d4 7788e5e2 pdfium!pdfium::MakeUnique<CXFA\_FFTabOrderPageWidgetIterator,CXFA\_FFPageView \*,unsigned int &>(class CXFA\_FFPageView \*\* args = 0x00afd510, unsigned int \* args = 0x00afd538)+0x5c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\third\_party\base\ptr\_util.h @ 56]  

37 00afd528 776b6269 pdfium!CXFA\_FFPageView::CreateWidgetIterator(unsigned int dwTraverseWay = 1, unsigned int dwWidgetFilter = 0x188)+0x72 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\xfa\fxfa\cxfa\_ffpageview.cpp @ 137]  

38 00afd5ac 776b6107 pdfium!CPDFSDK\_AnnotHandlerMgr::GetNextAnnot(class CPDFSDK\_Annot \* pSDKAnnot = 0x46a44fe0, bool bNext = true)+0x79 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 317]  

39 00afd608 776d72f1 pdfium!CPDFSDK\_AnnotHandlerMgr::Annot\_OnKeyDown(class CPDFSDK\_Annot \* pAnnot = 0x46a44fe0, int nKeyCode = 0n9, int nFlag = 0n1024)+0xe7 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_annothandlermgr.cpp @ 236]  

3a 00afd63c 776fbf31 pdfium!CPDFSDK\_PageView::OnKeyDown(int nKeyCode = 0n9, int nFlag = 0n1024)+0x61 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\cpdfsdk\_pageview.cpp @ 482]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\chrome.dll  

3b 00afd670 1a36de18 pdfium!FORM\_OnKeyDown(struct fpdf\_form\_handle\_t \* hHandle = 0x407cafb8, struct fpdf\_page\_t** \* page = 0x3feacfe8, int nKeyCode = 0n9, int modifier = 0n1024)+0x61 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\third\_party\pdfium\fpdfsdk\fpdf\_formfill.cpp @ 479]  

3c 00afd728 1a36cd99 chrome!chrome\_pdf::PDFiumEngine::OnKeyDown(class pp::KeyboardInputEvent \* event = 0x00afd85c)+0xb8 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\pdf\pdfium\pdfium\_engine.cc @ 1662]  

3d 00afd930 1a390f1d chrome!chrome\_pdf::PDFiumEngine::HandleEvent(class pp::InputEvent \* event = 0x00afdaa0)+0x249 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\pdf\pdfium\pdfium\_engine.cc @ 962]  

3e 00afdab4 18b2ebf6 chrome!chrome\_pdf::OutOfProcessInstance::HandleInputEvent(class pp::InputEvent \* event = 0x00afdae4)+0x60d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\pdf\out\_of\_process\_instance.cc @ 846]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\ppapi\_proxy.dll  

3f 00afdaf4 507fa767 chrome!pp::InputEvent\_HandleEvent(int pp\_instance = 0n-775059439, int resource = 0n702)+0x96 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\cpp\module.cc @ 53]  

40 00afdb24 507fa6fa ppapi\_proxy!ppapi::CallWhileUnlocked<PP\_Bool,int,int,int,int>(<function> \* function = 0x18b2eb60, int \* p1 = 0x00afdb78, int \* p2 = 0x00afdb5c)+0x47 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\shared\_impl\proxy\_lock.h @ 136]  

41 00afdb70 507fb09e ppapi\_proxy!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMsgHandleFilteredInputEvent(int instance = 0n-775059439, struct ppapi::InputEventData \* data = 0x00afdd48, <unnamed-tag> \* result = 0x00afdc98)+0xaa [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 107]  

42 00afdbb4 507fafc8 ppapi\_proxy!base::DispatchToMethodImpl<ppapi::proxy::PPP\_InputEvent\_Proxy \*,void (class ppapi::proxy::PPP\_InputEvent\_Proxy \*\* obj = 0x00afde1c, <function> \* method = 0x507fa650, class std::\_\_1::tuple<int,ppapi::InputEventData> \* in = 0x00afdd40, class std::\_\_1::tuple<PP\_Bool> \* out = 0x00afdc98)+0x8e [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\tuple.h @ 96]  

43 00afdc18 507fa5bc ppapi\_proxy!base::DispatchToMethod<ppapi::proxy::PPP\_InputEvent\_Proxy \*,void (class ppapi::proxy::PPP\_InputEvent\_Proxy \*\* obj = 0x00afde1c, <function> \* method = 0x507fa650, class std::\_\_1::tuple<int,ppapi::InputEventData> \* in = 0x00afdd40, class std::\_\_1::tuple<PP\_Bool> \* out = 0x00afdc98)+0x98 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\tuple.h @ 105]  

44 00afde10 507f9f8d ppapi\_proxy!IPC::MessageT<PpapiMsg\_PPPInputEvent\_HandleFilteredInputEvent\_Meta,std::\_\_1::tuple<int,ppapi::InputEventData>,std::\_\_1::tuple<PP\_Bool> >::Dispatch<ppapi::proxy::PPP\_InputEvent\_Proxy,ppapi::proxy::PPP\_InputEvent\_Proxy,void,void (class IPC::Message \* \*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\message\_support.dll  

msg = 0x247fafb8 {size = 0x90}, class ppapi::proxy::PPP\_InputEvent\_Proxy \* obj = 0x40e2afe8, class ppapi::proxy::PPP\_InputEvent\_Proxy \* sender = 0x40e2afe8, <function> \* func = 0x507fa650)+0x2cc [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ipc\ipc\_message\_templates.h @ 205]  

45 00afde88 507397a7 ppapi\_proxy!ppapi::proxy::PPP\_InputEvent\_Proxy::OnMessageReceived(class IPC::Message \* msg = 0x247fafb8 {size = 0x90})+0x14d [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\ppp\_input\_event\_proxy.cc @ 85]  

46 00afdf64 50795c75 ppapi\_proxy!ppapi::proxy::Dispatcher::OnMessageReceived(class IPC::Message \* msg = 0x247fafb8 {size = 0x90})+0x127 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\dispatcher.cc @ 70]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\ipc.dll  

47 00afe038 633288df ppapi\_proxy!ppapi::proxy::PluginDispatcher::OnMessageReceived(class IPC::Message \* msg = 0x247fafb8 {size = 0x90})+0x2f5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ppapi\proxy\plugin\_dispatcher.cc @ 273]  

48 00afe058 6332ebff ipc!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message \* message = 0x247fafb8 {size = 0x90})+0x8f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\ipc\ipc\_channel\_proxy.cc @ 326]  

49 00afe080 6332eadc ipc!base::internal::FunctorTraits<void (<function> \* method = 0x63328850, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* receiver\_ptr = 0x247fafb0 [0x63381340] 0x42626f10 {...}, class IPC::Message \* args = 0x247fafb8 {size = 0x90})+0x4f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 499]  

4a 00afe0c0 6332ea0f ipc!base::internal::InvokeHelper<0,void>::MakeItSo<void (<function> \*\* functor = 0x247fafa8, class scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) \* args = 0x247fafb0 [0x63381340] 0x42626f10 {...}, class IPC::Message \* args = 0x247fafb8 {size = 0x90})+0x7c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 599]  

4b 00afe0e4 6332e8c4 ipc!base::internal::Invoker<base::internal::BindState<void (<function> \*\* functor = 0x247fafa8, class std::**1::tuple<scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);),IPC::Message> \* bound = 0x247fafb0)+0x6f [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 672]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\base.dll  

4c 00afe10c 68311bb0 ipc!base::internal::Invoker<base::internal::BindState<void (class base::internal::BindStateBase \* base = 0x247faf90)+0x54 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\bind\_internal.h @ 641]  

4d 00afe130 684e7d73 base!base::OnceCallback<void (void)+0x50 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\callback.h @ 98]  

4e 00afe3b8 6853d457 base!base::TaskAnnotator::RunTask(char \* trace\_event\_name = 0x686ca607 "ThreadController::Task", struct base::PendingTask \* pending\_task = 0x00afe700)+0x5b3 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\common\task\_annotator.cc @ 144]  

4f 00afe770 6853ca81 base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(class base::sequence\_manager::LazyNow \* continuation\_lazy\_now = 0x00afe810, bool \* ran\_task = 0x00afe82b)+0x737 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 368]  

50 00afe838 683d1ea0 base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork(void)+0xb1 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 218]  

51 00afe898 6853e85c base!base::MessagePumpDefault::Run(class base::MessagePump::Delegate \* delegate = 0x3ea96f2c)+0x60 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\message\_loop\message\_pump\_default.cc @ 39]  

52 00afeb2c 68479d6b base!base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool application\_tasks\_allowed = true, class base::TimeDelta timeout = 9223372036854775807)+0x34c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc @ 466]  

53 00afede0 68479a05 base!base::RunLoop::RunWithTimeout(class base::TimeDelta timeout = 9223372036854775807)+0x34b [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\run\_loop.cc @ 163]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\content.dll  

54 00afee08 1ece7315 base!base::RunLoop::Run(void)+0x45 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\base\run\_loop.cc @ 131]  

55 00afeff0 22adfc26 content!content::PpapiPluginMain(struct content::MainFunctionParams \* parameters = 0x00aff064)+0x5c5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\ppapi\_plugin\ppapi\_plugin\_main.cc @ 160]  

56 00aff01c 22ae0c75 content!content::RunOtherNamedProcessTypeMain(class std::1::basic\_string<char,std::1::char\_traits<char>,std::1::allocator<char> > \* process\_type = 0x00aff080 "ppapi", struct content::MainFunctionParams \* main\_function\_params = 0x00aff064, class content::ContentMainDelegate \* delegate = 0x00aff650)+0xa6 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_main\_runner\_impl.cc @ 579]  

57 00aff1d8 22adc500 content!content::ContentMainRunnerImpl::Run(bool start\_service\_manager\_only = false)+0x2c5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_main\_runner\_impl.cc @ 876]  

\*\*\* WARNING: Unable to verify checksum for C:\Users\huyna\_dev\Desktop\chromium\out\chromium\_pdfium\_xfa\embedder.dll  

58 00aff1f0 355722e1 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess(void)+0x30 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_service\_manager\_main\_delegate.cc @ 52]  

59 00aff570 22adfa4c embedder!service\_manager::Main(struct service\_manager::MainParams \* params = 0x00aff594)+0x6d1 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\services\service\_manager\embedder\main.cc @ 422]  

5a 00aff5bc 16521315 content!content::ContentMain(struct content::ContentMainParams \* params = 0x00aff634)+0x5c [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\content\app\content\_main.cc @ 20]  

\*\*\* WARNING: Unable to verify checksum for chrome.exe  

5b 00aff698 003a8e33 chrome!ChromeMain(struct HINSTANCE \* instance = 0x003a0000, struct sandbox::SandboxInterfaceInfo \* sandbox\_info = 0x00aff72c, int64 exe\_entry\_point\_ticks = 0n71623879408)+0x1f5 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\chrome\app\chrome\_main.cc @ 110]  

5c 00aff790 003a1479 chrome\_exe!MainDllLoader::Launch(struct HINSTANCE \* instance = 0x003a0000, class base::TimeTicks exe\_entry\_point\_ticks = class base::TimeTicks)+0x453 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\chrome\app\main\_dll\_loader\_win.cc @ 202]  

5d 00affa74 005ddd8e chrome\_exe!wWinMain(struct HINSTANCE \* instance = 0x003a0000, struct HINSTANCE** \* prev = 0x00000000)+0x479 [C:\Users\huyna\_dev\Desktop\chromium\chromium\_pdfium\_XFA\src\chrome\app\chrome\_exe\_main\_win.cc @ 229]  

5e 00affa8c 005ddee1 chrome\_exe!invoke\_main(void)+0x1e [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 123]  

5f 00affae4 005ddfad chrome\_exe!\_\_scrt\_common\_main\_seh(void)+0x151 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 283]  

60 00affaec 005ddfb8 chrome\_exe!\_\_scrt\_common\_main(void)+0xd [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 326]  

61 00affaf4 75f80419 chrome\_exe!wWinMainCRTStartup(void)+0x8 [f:\dd\vctools\crt\vcstartup\src\startup\exe\_wwinmain.cpp @ 17]  

62 00affb04 7706662d KERNEL32!BaseThreadInitThunk+0x19  

63 00affb60 770665fd ntdll!\_\_RtlUserThreadStart+0x2f  

64 00affb70 00000000 ntdll!\_RtlUserThreadStart+0x1b

## Attachments

- [crash_info.txt](attachments/crash_info.txt) (text/plain, 30.9 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 9.4 KB)

## Timeline

### cl...@chromium.org (2019-07-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5653748768964608.

### cl...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-07-01)

Testcase 5653748768964608 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5653748768964608.

### jd...@chromium.org (2019-07-01)

tsepez@: You're a lot better equipped to judge these than I am. Can you take a look at this and re-route if needed? Thanks a ton.

(that said, I don't even see a second page to the PDF, so I can't repro)

[Monorail components: Internals>Plugins>PDF]

### jd...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-07-01)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-07-02)

Probably stale ptr from CXFA_LayoutPageMgr::m_PageArray.  Refcounting the layoutiems would avoid this.

### cl...@chromium.org (2019-07-12)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-07-30)

https://pdfium-review.googlesource.com/c/pdfium/+/54190 avoids this UAF, but now triggers an unowned ptr low severity trace.

### ts...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### hu...@gmail.com (2020-01-10)

Hi all, 

Can you take a look to this issue? I check it and maybe it's patched by this patch https://pdfium-review.googlesource.com/c/pdfium/+/54190. There is no UAF crash. 

### th...@chromium.org (2020-02-20)

We are just down to ProbeForLowSeverityLifetimeIssue() failures now. I took care of the first one in a local build, but then we get another... In particular, CXFA_FFTabOrderPageWidgetIterator has a std::vector of UnownedPtrs.

### hu...@gmail.com (2020-06-02)

thestig@ tsepez@ 

can you take a look to this issue to finish it plz? :D 


### th...@chromium.org (2020-06-02)

Thanks for the remainder. Maybe this will be an XFA security bug fix week?

### th...@chromium.org (2020-06-02)

Actually, I think I just fixed the remaining ProbeForLowSeverityLifetimeIssue() issue I referred to in https://crbug.com/chromium/980172#c12. The PoC from https://crbug.com/chromium/980161 exhibits the same issue, and I took care of that. So to summarize:

https://pdfium-review.googlesource.com/54190 took care of the initial issue.
https://pdfium-review.googlesource.com/70252 took care of the secondary issue.

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

Congrats! The Panel decided to award $2,000 for this report! 

### na...@google.com (2020-06-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-09-08)

This issue was migrated from crbug.com/chromium/980172?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095555)*
