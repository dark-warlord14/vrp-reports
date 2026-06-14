# Security: heap-use-after-free in CPDF_AnnotList::CPDF_AnnotList

| Field | Value |
|-------|-------|
| **Issue ID** | [40050414](https://issues.chromium.org/issues/40050414) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ba...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2019-10-12 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

While rendering the pdf page, Appearance of annotations is processed by GenerateAP function [1]

// pdfium/core/fpdfdoc/cpdf\_annotlist.cpp:173  

// <https://cs.chromium.org/chromium/src/third_party/pdfium/core/fpdfdoc/cpdf_annotlist.cpp?l=173>  

CPDF\_AnnotList::CPDF\_AnnotList(CPDF\_Page\* pPage)  

: m\_pDocument(pPage->GetDocument()) {  

CPDF\_Array\* pAnnots = pPage->GetDict()->GetArrayFor("Annots"); // \*\*\* 2 \*\*\*  

[...]  

const CPDF\_Dictionary\* pRoot = m\_pDocument->GetRoot();  

const CPDF\_Dictionary\* pAcroForm = pRoot->GetDictFor("AcroForm");  

bool bRegenerateAP =  

pAcroForm && pAcroForm->GetBooleanFor("NeedAppearances", false);  

for (size\_t i = 0; i < pAnnots->size(); ++i) { // \*\*\* 9 \*\*\*  

CPDF\_Dictionary\* pDict = ToDictionary(pAnnots->GetDirectObjectAt(i));  

if (!pDict)  

continue;  

const ByteString subtype =  

pDict->GetStringFor(pdfium::annotation::kSubtype);  

if (subtype == "Popup") {  

// Skip creating Popup annotations in the PDF document since PDFium  

// provides its own Popup annotations.  

continue;  

}  

pAnnots->ConvertToIndirectObjectAt(i, m\_pDocument.Get());  

m\_AnnotList.push\_back(  

pdfium::MakeUnique<CPDF\_Annot>(pDict, m\_pDocument.Get()));  

if (bRegenerateAP && subtype == "Widget" &&  

CPDF\_InteractiveForm::IsUpdateAPEnabled() &&  

!pDict->GetDictFor(pdfium::annotation::kAP)) {

```
  GenerateAP(m_pDocument.Get(), pDict);              // \*\*\* 1 \*\*\*  
}  

```

}  

[...]

GenerateAP function calls CPVT\_GenerateAP::GenerateFormAP function [3]

// pdfium/core/fpdfdoc/cpdf\_annotlist.cpp:125  

// <https://cs.chromium.org/chromium/src/third_party/pdfium/core/fpdfdoc/cpdf_annotlist.cpp?l=125>  

void GenerateAP(CPDF\_Document\* pDoc, CPDF\_Dictionary\* pAnnotDict) {  

if (!pAnnotDict ||  

pAnnotDict->GetStringFor(pdfium::annotation::kSubtype) != "Widget") {  

return;  

}

CPDF\_Object\* pFieldTypeObj =  

FPDF\_GetFieldAttr(pAnnotDict, pdfium::form\_fields::kFT);  

if (!pFieldTypeObj)  

return;

ByteString field\_type = pFieldTypeObj->GetString();  

if (field\_type == pdfium::form\_fields::kTx) {  

CPVT\_GenerateAP::GenerateFormAP(pDoc, pAnnotDict, // \*\*\* 3 \*\*\*  

CPVT\_GenerateAP::kTextField);  

return;  

}

CPVT\_GenerateAP::GenerateFormAP function handles lot CPDF\_Object objects.

// pdfium/core/fpdfdoc/cpvt\_generateap.cpp:915  

// <https://cs.chromium.org/chromium/src/third_party/pdfium/core/fpdfdoc/cpvt_generateap.cpp?l=915>  

void CPVT\_GenerateAP::GenerateFormAP(CPDF\_Document\* pDoc,  

CPDF\_Dictionary\* pAnnotDict,  

FormType type) {  

CPDF\_Dictionary\* pRootDict = pDoc->GetRoot();  

if (!pRootDict)  

return;

CPDF\_Dictionary\* pFormDict = pRootDict->GetDictFor("AcroForm");  

if (!pFormDict)  

return;

ByteString DA;  

if (CPDF\_Object\* pDAObj = FPDF\_GetFieldAttr(pAnnotDict, "DA")) // \*\*\* 4 \*\*\*  

DA = pDAObj->GetString();  

if (DA.IsEmpty())  

DA = pFormDict->GetStringFor("DA");  

if (DA.IsEmpty())  

return;

CPDF\_DefaultAppearance appearance(DA);

float fFontSize = 0;  

Optional<ByteString> font = appearance.GetFont(&fFontSize);  

if (!font)  

return;

ByteString font\_name = \*font; // \*\*\* 5 \*\*\*  

CFX\_Color crText = fpdfdoc::CFXColorFromString(DA);  

CPDF\_Dictionary\* pDRDict = pFormDict->GetDictFor("DR");  

if (!pDRDict)  

return;

CPDF\_Dictionary\* pDRFontDict = pDRDict->GetDictFor("Font"); // \*\*\* 6 \*\*\*  

if (!pDRFontDict)  

return;

CPDF\_Dictionary\* pFontDict = pDRFontDict->GetDictFor(font\_name); // \*\*\* 7 \*\*\*  

if (!pFontDict) {  

pFontDict = pDoc->NewIndirect<CPDF\_Dictionary>();  

pFontDict->SetNewFor<CPDF\_Name>("Type", "Font");  

pFontDict->SetNewFor<CPDF\_Name>("Subtype", "Type1");  

pFontDict->SetNewFor<CPDF\_Name>("BaseFont", CFX\_Font::kDefaultAnsiFontName);  

pFontDict->SetNewFor<CPDF\_Name>("Encoding", "WinAnsiEncoding");  

pDRFontDict->SetNewFor<CPDF\_Reference>(font\_name, pDoc,  

pFontDict->GetObjNum()); // \*\*\* 8 \*\*\*  

}  

[...]

This function loads string from key "DA" in [4] and later retrieves font name from that string [5].  

It loads font dictionry [7] and loads value for font-name key [6][7]. If loaded value doesn't exist or type of loaded value isn't dictionary, It create new dictionary-typed value for font-name key.

Primitive 1. retrieved font dictionary could be other object [6].  

Primitive 2. font-name can be any string(controlled by value of 'DR' key) and value for font-name key could be removed if type of value isn't dictionary. [7][8]

With above two primitives, arbitrary key of which value type isn't dictionary could be removed in other dictionary object at [8]. The value get freed when the matched key is removed.  

In the attached poc, value for 'Annots' key [2] is freed by [8] and dangled object is used at [9], Use-after-free occured.

**VERSION**  

Chrome Version: Mozilla/5.0 (X11; Linux x86\_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.0 Safari/537.36  

Operating System: All

**REPRODUCTION CASE**

1. Build pdfium\_test or chromium with ASAN
2. Load the attached poc pdf file with pdfium\_test or chromium
3. Crash occured

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: PDF plugin process  

Crash State: Address Sanitizer output

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060000675a0 at pc 0x55607a41ffb4 bp 0x7ffdaf53fcf0 sp 0x7ffdaf53fce8  

READ of size 8 at 0x6060000675a0 thread T0 (chrome)  

==1==WARNING: invalid path to external symbolizer!  

==1==WARNING: Failed to use and restart external symbolizer!  

#0 0x55607a41ffb3 in size ./../../buildtools/third\_party/libc++/trunk/include/vector:656:46  

#1 0x55607a41ffb3 in size ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_array.h:38:0  

#2 0x55607a41ffb3 in CPDF\_AnnotList::CPDF\_AnnotList(CPDF\_Page\*) ./../../third\_party/pdfium/core/fpdfdoc/cpdf\_annotlist.cpp:186:0  

#3 0x55607a4cf928 in MakeUnique<CPDF\_AnnotList, CPDF\_Page \*&> ./../../third\_party/pdfium/third\_party/base/ptr\_util.h:56:33  

#4 0x55607a4cf928 in (anonymous namespace)::RenderPageImpl(CPDF\_PageRenderContext\*, CPDF\_Page\*, CFX\_Matrix const&, FX\_RECT const&, int, bool, IPDFSDK\_PauseAdapter\*) ./../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:126:0  

#5 0x55607a4cf40a in RenderPageWithContext(CPDF\_PageRenderContext\*, fpdf\_page\_t\_\_\*, int, int, int, int, int, int, bool, IPDFSDK\_PauseAdapter\*) ./../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:926:3  

#6 0x55607a4c7995 in FPDF\_RenderPageBitmap\_Start ./../../third\_party/pdfium/fpdfsdk/fpdf\_progressive.cpp:59:3  

#7 0x55608c174869 in chrome\_pdf::PDFiumEngine::ContinuePaint(int, pp::ImageData\*) ./../../pdf/pdfium/pdfium\_engine.cc:2923:10  

#8 0x55608c173745 in chrome\_pdf::PDFiumEngine::Paint(pp::Rect const&, pp::ImageData\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*) ./../../pdf/pdfium/pdfium\_engine.cc:719:11  

#9 0x55608c14dae3 in chrome\_pdf::OutOfProcessInstance::OnPaint(std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) > const&, std::\_\_1::vector<PaintManager::ReadyRect, std::\_\_1::allocator[PaintManager::ReadyRect](javascript:void(0);) >\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*) ./../../pdf/out\_of\_process\_instance.cc:1167:16  

#10 0x55608c166c41 in PaintManager::DoPaint() ./../../pdf/paint\_manager.cc:235:12  

#11 0x55608c168f9c in PaintManager::OnFlushComplete(int) ./../../pdf/paint\_manager.cc:328:5  

#12 0x55608c1690db in operator() ./../../ppapi/utility/completion\_callback\_factory.h:607:9  

#13 0x55608c1690db in pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::\*)(int)> >::Thunk(void\*, int) ./../../ppapi/utility/completion\_callback\_factory.h:584:0  

#14 0x556080a65941 in PP\_RunCompletionCallback ./../../ppapi/c/pp\_completion\_callback.h:240:3  

#15 0x556080a65941 in CallWhileUnlocked<void, PP\_CompletionCallback \*, int, PP\_CompletionCallback \*, int> ./../../ppapi/shared\_impl/proxy\_lock.h:135:0  

#16 0x556080a65941 in ppapi::TrackedCallback::Run(int) ./../../ppapi/shared\_impl/tracked\_callback.cc:141:0  

#17 0x55608999f769 in DispatchResourceReplyOrDefaultParams<IPC::MessageT<PpapiPluginMsg\_Graphics2D\_FlushAck\_Meta>, base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)> &> ./../../base/callback\_internal.h:0:25  

#18 0x55608999f769 in ppapi::proxy::PluginResourceCallback<IPC::MessageT<PpapiPluginMsg\_Graphics2D\_FlushAck\_Meta, std::\_\_1::tuple<>, void>, base::RepeatingCallback<void (ppapi::proxy::ResourceMessageReplyParams const&)> >::Run(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) ./../../ppapi/proxy/plugin\_resource\_callback.h:39:0  

#19 0x5560898ef0c1 in ppapi::proxy::PluginResource::OnReplyReceived(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) ./../../ppapi/proxy/plugin\_resource.cc:62:15  

#20 0x5560898ed84d in ppapi::proxy::PluginMessageFilter::DispatchResourceReply(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) ./../../ppapi/proxy/plugin\_message\_filter.cc:116:13  

#21 0x55607b6a2482 in Run ./../../base/callback.h:98:12  

#22 0x55607b6a2482 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:142:0  

#23 0x55607b6db706 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#24 0x55607b6dac97 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#25 0x55607b5e6ee0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#26 0x55607b6dd75e in Run ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#27 0x55607b6dd75e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#28 0x55607b65441c in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run\_loop.cc:157:14  

#29 0x556079cc694d in content::PpapiPluginMain(content::MainFunctionParams const&) ./../../content/ppapi\_plugin/ppapi\_plugin\_main.cc:157:12  

#30 0x55607a67e9f0 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:518:14  

#31 0x55607a68209b in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:871:10  

#32 0x55607a81fb1b in service\_manager::Main(service\_manager::MainParams const&) ./../../services/service\_manager/embedder/main.cc:422:29  

#33 0x55607a67cf44 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:19:10  

#34 0x556071bb0ddd in ChromeMain ./../../chrome/app/chrome\_main.cc:110:12  

#35 0x7fc92239682f in \_\_libc\_start\_main /build/glibc-LK5gWL/glibc-2.23/csu/../csu/libc-start.c:291:0

0x6060000675a0 is located 32 bytes inside of 64-byte region [0x606000067580,0x6060000675c0)  

freed by thread T0 (chrome) here:  

#0 0x556071baebbd in operator delete(void\*) *asan\_rtl*:3  

#1 0x55607a2a6fa5 in Release ./../../third\_party/pdfium/core/fxcrt/retain\_ptr.h:122:7  

#2 0x55607a2a6fa5 in operator() ./../../third\_party/pdfium/core/fxcrt/retain\_ptr.h:20:0  

#3 0x55607a2a6fa5 in reset ./../../buildtools/third\_party/libc++/trunk/include/memory:2651:0  

#4 0x55607a2a6fa5 in operator= ./../../third\_party/pdfium/core/fxcrt/retain\_ptr.h:69:0  

#5 0x55607a2a6fa5 in CPDF\_Dictionary::SetFor(fxcrt::ByteString const&, fxcrt::RetainPtr<CPDF\_Object>) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:216:0  

#6 0x55607a442429 in std::**1::enable\_if<!(CanInternStrings<CPDF\_Reference>::value), CPDF\_Reference\*>::type CPDF\_Dictionary::SetNewFor<CPDF\_Reference, CPDF\_Document\*&, unsigned int>(fxcrt::ByteString const&, CPDF\_Document\*&, unsigned int&&) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.h:83:9  

#7 0x55607a4587a7 in CPVT\_GenerateAP::GenerateFormAP(CPDF\_Document\*, CPDF\_Dictionary\*, CPVT\_GenerateAP::FormType) ./../../third\_party/pdfium/core/fpdfdoc/cpvt\_generateap.cpp:955:18  

#8 0x55607a41ee20 in GenerateAP ./../../third\_party/pdfium/core/fpdfdoc/cpdf\_annotlist.cpp:138:5  

#9 0x55607a41ee20 in CPDF\_AnnotList::CPDF\_AnnotList(CPDF\_Page\*) ./../../third\_party/pdfium/core/fpdfdoc/cpdf\_annotlist.cpp:203:0  

#10 0x55607a4cf928 in MakeUnique<CPDF\_AnnotList, CPDF\_Page \*&> ./../../third\_party/pdfium/third\_party/base/ptr\_util.h:56:33  

#11 0x55607a4cf928 in (anonymous namespace)::RenderPageImpl(CPDF\_PageRenderContext\*, CPDF\_Page\*, CFX\_Matrix const&, FX\_RECT const&, int, bool, IPDFSDK\_PauseAdapter\*) ./../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:126:0  

#12 0x55607a4cf40a in RenderPageWithContext(CPDF\_PageRenderContext\*, fpdf\_page\_t**\*, int, int, int, int, int, int, bool, IPDFSDK\_PauseAdapter\*) ./../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:926:3  

#13 0x55607a4c7995 in FPDF\_RenderPageBitmap\_Start ./../../third\_party/pdfium/fpdfsdk/fpdf\_progressive.cpp:59:3  

#14 0x55608c174869 in chrome\_pdf::PDFiumEngine::ContinuePaint(int, pp::ImageData\*) ./../../pdf/pdfium/pdfium\_engine.cc:2923:10  

#15 0x55608c173745 in chrome\_pdf::PDFiumEngine::Paint(pp::Rect const&, pp::ImageData\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*) ./../../pdf/pdfium/pdfium\_engine.cc:719:11  

#16 0x55608c14dae3 in chrome\_pdf::OutOfProcessInstance::OnPaint(std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) > const&, std::\_\_1::vector<PaintManager::ReadyRect, std::\_\_1::allocator[PaintManager::ReadyRect](javascript:void(0);) >\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*) ./../../pdf/out\_of\_process\_instance.cc:1167:16  

#17 0x55608c166c41 in PaintManager::DoPaint() ./../../pdf/paint\_manager.cc:235:12  

#18 0x55608c168f9c in PaintManager::OnFlushComplete(int) ./../../pdf/paint\_manager.cc:328:5  

#19 0x55608c1690db in operator() ./../../ppapi/utility/completion\_callback\_factory.h:607:9  

#20 0x55608c1690db in pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::\*)(int)> >::Thunk(void\*, int) ./../../ppapi/utility/completion\_callback\_factory.h:584:0  

#21 0x556080a65941 in PP\_RunCompletionCallback ./../../ppapi/c/pp\_completion\_callback.h:240:3  

#22 0x556080a65941 in CallWhileUnlocked<void, PP\_CompletionCallback \*, int, PP\_CompletionCallback \*, int> ./../../ppapi/shared\_impl/proxy\_lock.h:135:0  

#23 0x556080a65941 in ppapi::TrackedCallback::Run(int) ./../../ppapi/shared\_impl/tracked\_callback.cc:141:0  

#24 0x55608999f769 in DispatchResourceReplyOrDefaultParams<IPC::MessageT<PpapiPluginMsg\_Graphics2D\_FlushAck\_Meta>, base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)> &> ./../../base/callback\_internal.h:0:25  

#25 0x55608999f769 in ppapi::proxy::PluginResourceCallback<IPC::MessageT<PpapiPluginMsg\_Graphics2D\_FlushAck\_Meta, std::\_\_1::tuple<>, void>, base::RepeatingCallback<void (ppapi::proxy::ResourceMessageReplyParams const&)> >::Run(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) ./../../ppapi/proxy/plugin\_resource\_callback.h:39:0  

#26 0x5560898ef0c1 in ppapi::proxy::PluginResource::OnReplyReceived(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) ./../../ppapi/proxy/plugin\_resource.cc:62:15  

#27 0x5560898ed84d in ppapi::proxy::PluginMessageFilter::DispatchResourceReply(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) ./../../ppapi/proxy/plugin\_message\_filter.cc:116:13  

#28 0x55607b6a2482 in Run ./../../base/callback.h:98:12  

#29 0x55607b6a2482 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:142:0  

#30 0x55607b6db706 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#31 0x55607b6dac97 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#32 0x55607b5e6ee0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#33 0x55607b6dd75e in Run ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#34 0x55607b6dd75e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#35 0x55607b65441c in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run\_loop.cc:157:14  

#36 0x556079cc694d in content::PpapiPluginMain(content::MainFunctionParams const&) ./../../content/ppapi\_plugin/ppapi\_plugin\_main.cc:157:12  

#37 0x55607a67e9f0 in content::RunZygote(content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:518:14  

#38 0x55607a68209b in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content\_main\_runner\_impl.cc:871:10  

#39 0x55607a81fb1b in service\_manager::Main(service\_manager::MainParams const&) ./../../services/service\_manager/embedder/main.cc:422:29  

#40 0x55607a67cf44 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content\_main.cc:19:10  

#41 0x556071bb0ddd in ChromeMain ./../../chrome/app/chrome\_main.cc:110:12

previously allocated by thread T0 (chrome) here:  

#0 0x556071bae35d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55607a2f5d07 in MakeRetain<CPDF\_Array> ./../../third\_party/pdfium/core/fxcrt/retain\_ptr.h:142:23  

#2 0x55607a2f5d07 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:469:0  

#3 0x55607a2f6747 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:507:11  

#4 0x55607a2f91f5 in CPDF\_SyntaxParser::GetIndirectObject(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:559:33  

#5 0x55607a2d9bc2 in CPDF\_Parser::ParseIndirectObjectAt(long, unsigned int) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:916:28  

#6 0x55607a2daad4 in CPDF\_Parser::ParseIndirectObject(unsigned int) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:865:12  

#7 0x55607a2ab03c in CPDF\_Document::ParseIndirectObject(unsigned int) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:76:33  

#8 0x55607a2ba3d2 in CPDF\_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_indirect\_object\_holder.cpp:50:36  

#9 0x55607a280695 in GetDirectObjectAt ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_array.cpp:105:24  

#10 0x55607a280695 in CPDF\_Array::GetDictAt(unsigned long) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_array.cpp:139:0  

#11 0x55607a2ac259 in CPDF\_Document::TraversePDFPages(int, int\*, unsigned long) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:147:39  

#12 0x55607a2ad002 in CPDF\_Document::GetPageDictionary(int) ./../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:238:28  

#13 0x55607a4d1177 in FPDF\_GetPageSizeByIndex ./../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:957:34  

#14 0x55608c177aaa in GetPageSize ./../../pdf/pdfium/pdfium\_engine.cc:2821:12  

#15 0x55608c177aaa in chrome\_pdf::PDFiumEngine::LoadPageInfo(bool) ./../../pdf/pdfium/pdfium\_engine.cc:2640:0  

#16 0x55608c19458b in chrome\_pdf::PDFiumEngine::ContinueLoadingDocument(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) ./../../pdf/pdfium/pdfium\_engine.cc:2578:3  

#17 0x55608c179969 in chrome\_pdf::PDFiumEngine::LoadDocument() ./../../pdf/pdfium/pdfium\_engine.cc:2501:5  

#18 0x55608c1a6844 in chrome\_pdf::DocumentLoaderImpl::ReadComplete() ./../../pdf/document\_loader\_impl.cc:0:0  

#19 0x55608c1a6c8c in chrome\_pdf::DocumentLoaderImpl::DidRead(int) ./../../pdf/document\_loader\_impl.cc:0:0  

#20 0x55608c1a7d8b in operator() ./../../ppapi/utility/completion\_callback\_factory.h:607:9  

#21 0x55608c1a7d8b in pp::CompletionCallbackFactory<chrome\_pdf::DocumentLoaderImpl, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome\_pdf::DocumentLoaderImpl, pp::ThreadSafeThreadTraits>::Dispatcher0<void (chrome\_pdf::DocumentLoaderImpl::\*)(int)> >::Thunk(void\*, int) ./../../ppapi/utility/completion\_callback\_factory.h:584:0  

#22 0x55608c1aee08 in chrome\_pdf::URLLoaderWrapperImpl::DidRead(int) ./../../pdf/url\_loader\_wrapper\_impl.cc:0:0  

#23 0x55608c1b6ebb in operator() ./../../ppapi/utility/completion\_callback\_factory.h:607:9  

#24 0x55608c1b6ebb in pp::CompletionCallbackFactory<chrome\_pdf::URLLoaderWrapperImpl, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<chrome\_pdf::URLLoaderWrapperImpl, pp::ThreadSafeThreadTraits>::Dispatcher0<void (chrome\_pdf::URLLoaderWrapperImpl::\*)(int)> >::Thunk(void\*, int) ./../../ppapi/utility/completion\_callback\_factory.h:584:0  

#25 0x556080a65941 in PP\_RunCompletionCallback ./../../ppapi/c/pp\_completion\_callback.h:240:3  

#26 0x556080a65941 in CallWhileUnlocked<void, PP\_CompletionCallback \*, int, PP\_CompletionCallback \*, int> ./../../ppapi/shared\_impl/proxy\_lock.h:135:0  

#27 0x556080a65941 in ppapi::TrackedCallback::Run(int) ./../../ppapi/shared\_impl/tracked\_callback.cc:141:0  

#28 0x5560899f7133 in RunCallback ./../../ppapi/proxy/url\_loader\_resource.cc:336:22  

#29 0x5560899f7133 in OnPluginMsgFinishedLoading ./../../ppapi/proxy/url\_loader\_resource.cc:282:0  

#30 0x5560899f7133 in DispatchResourceReplyImpl<ppapi::proxy::URLLoaderResource, void (ppapi::proxy::URLLoaderResource::\*)(const ppapi::proxy::ResourceMessageReplyParams &, int), std::\_\_1::tuple<int> &, 0> ./../../ppapi/proxy/dispatch\_reply\_message.h:32:0  

#31 0x5560899f7133 in DispatchResourceReply<ppapi::proxy::URLLoaderResource, void (ppapi::proxy::URLLoaderResource::\*)(const ppapi::proxy::ResourceMessageReplyParams &, int), std::\_\_1::tuple<int> &> ./../../ppapi/proxy/dispatch\_reply\_message.h:46:0  

#32 0x5560899f7133 in ppapi::proxy::URLLoaderResource::OnReplyReceived(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) ./../../ppapi/proxy/url\_loader\_resource.cc:220:0  

#33 0x5560898ed84d in ppapi::proxy::PluginMessageFilter::DispatchResourceReply(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) ./../../ppapi/proxy/plugin\_message\_filter.cc:116:13  

#34 0x55607b6a2482 in Run ./../../base/callback.h:98:12  

#35 0x55607b6a2482 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:142:0  

#36 0x55607b6db706 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#37 0x55607b6dac97 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#38 0x55607b5e6ee0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#39 0x55607b6dd75e in Run ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#40 0x55607b6dd75e in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#41 0x55607b65441c in base::RunLoop::RunWithTimeout(base::TimeDelta) ./../../base/run\_loop.cc:157:14  

#42 0x556079cc694d in content::PpapiPluginMain(content::MainFunctionParams const&) ./../../content/ppapi\_plugin/ppapi\_plugin\_main.cc:157:12

SUMMARY: AddressSanitizer: heap-use-after-free (/home/banananapenguin/asan-linux-release-681094/chrome+0x11503fb3)  

Shadow bytes around the buggy address:  

0x0c0c80004e60: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c0c80004e70: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa  

0x0c0c80004e80: 00 00 00 00 00 00 00 00 fa fa fa fa 00 00 00 00  

0x0c0c80004e90: 00 00 00 00 fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c0c80004ea0: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa  

=>0x0c0c80004eb0: fd fd fd fd[fd]fd fd fd fa fa fa fa fd fd fd fd  

0x0c0c80004ec0: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0c80004ed0: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c0c80004ee0: fd fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x0c0c80004ef0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0c80004f00: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

Shadow gap: cc  

==1==ABORTING

**CREDIT INFORMATION**  

Reporter credit: banananapenguin

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### aj...@google.com (2019-10-14)

Thanks for the report. I will confirm tomorrow.

[Monorail components: Internals>Plugins>PDF]

### aj...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-10-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6249479941259264.

### aj...@google.com (2019-10-14)

Confirmed read of -1 on Windows HEAD(ish):

9:160> .exr -1
ExceptionAddress: 00007ffc520da1d3 (pdfium!std::__1::unique_ptr<CPDF_Object,fxcrt::ReleaseDeleter<CPDF_Object> >::get+0x0000000000000013)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 0000000000000000
   Parameter[1]: ffffffffffffffff
Attempt to read from address ffffffffffffffff

9:160> k
 # Child-SP          RetAddr           Call Site
00 00000001`40dfa660 00007ffc`52161403 pdfium!std::__1::unique_ptr<CPDF_Object,fxcrt::ReleaseDeleter<CPDF_Object> >::get+0x13 [C:\src\chromium\src\buildtools\third_party\libc++\trunk\include\memory @ 2624] 
01 00000001`40dfa690 00007ffc`52186680 pdfium!fxcrt::RetainPtr<CPDF_Object>::operator->+0x13 [C:\src\chromium\src\third_party\pdfium\core\fxcrt\retain_ptr.h @ 95] 
02 00000001`40dfa6c0 00007ffc`52209373 pdfium!CPDF_Array::GetDirectObjectAt+0x70 [C:\src\chromium\src\third_party\pdfium\core\fpdfapi\parser\cpdf_array.cpp @ 106] 
03 00000001`40dfa720 00007ffc`5238f5f7 pdfium!CPDF_AnnotList::CPDF_AnnotList+0x2e3 [C:\src\chromium\src\third_party\pdfium\core\fpdfdoc\cpdf_annotlist.cpp @ 184] 
04 00000001`40dfa8e0 00007ffc`523cc9b9 pdfium!pdfium::MakeUnique<CPDF_AnnotList,CPDF_Page *&>+0x47 [C:\src\chromium\src\third_party\pdfium\third_party\base\ptr_util.h @ 56] 
05 00000001`40dfa940 00007ffc`523cb518 pdfium!`anonymous namespace'::RenderPageImpl+0x419 [C:\src\chromium\src\third_party\pdfium\fpdfsdk\fpdf_view.cpp @ 116] 
06 00000001`40dfaab0 00007ffc`523c0832 pdfium!RenderPageWithContext+0x198 [C:\src\chromium\src\third_party\pdfium\fpdfsdk\fpdf_view.cpp @ 915] 
07 00000001`40dfabb0 00007ffc`7839b10b pdfium!FPDF_RenderPageBitmap_Start+0x2c2 [C:\src\chromium\src\third_party\pdfium\fpdfsdk\fpdf_progressive.cpp @ 66] 
08 00000001`40dfad00 00007ffc`7839a7c9 chrome!chrome_pdf::PDFiumEngine::ContinuePaint+0x61b [C:\src\chromium\src\pdf\pdfium\pdfium_engine.cc @ 2823] 
09 00000001`40dfb380 00007ffc`783cae7e chrome!chrome_pdf::PDFiumEngine::Paint+0x719 [C:\src\chromium\src\pdf\pdfium\pdfium_engine.cc @ 541] 
0a 00000001`40dfbae0 00007ffc`796135c9 chrome!chrome_pdf::OutOfProcessInstance::OnPaint+0x4de [C:\src\chromium\src\pdf\out_of_process_instance.cc @ 1195] 
0b 00000001`40dfc010 00007ffc`796145c4 chrome!PaintManager::DoPaint+0x389 [C:\src\chromium\src\pdf\paint_manager.cc @ 237] 
0c 00000001`40dfc410 00007ffc`79614b2b chrome!PaintManager::OnFlushComplete+0xe4 [C:\src\chromium\src\pdf\paint_manager.cc @ 331] 
0d 00000001`40dfc5a0 00007ffc`79614a51 chrome!pp::CompletionCallbackFactory<PaintManager,pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::*)(int)>::operator()+0x4b [C:\src\chromium\src\ppapi\utility\completion_callback_factory.h @ 608] 
0e 00000001`40dfc5f0 00007ffc`56be9234 chrome!pp::CompletionCallbackFactory<PaintManager,pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<PaintManager,pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::*)(int)> >::Thunk+0x41 [C:\src\chromium\src\ppapi\utility\completion_callback_factory.h @ 586] 
0f 00000001`40dfc640 00007ffc`56be91e5 ppapi_shared!PP_RunCompletionCallback+0x24 [C:\src\chromium\src\ppapi\c\pp_completion_callback.h @ 241] 
10 00000001`40dfc680 00007ffc`56be879f ppapi_shared!ppapi::CallWhileUnlocked<void,PP_CompletionCallback *,int,PP_CompletionCallback *,int>+0x55 [C:\src\chromium\src\ppapi\shared_impl\proxy_lock.h @ 136] 
11 00000001`40dfc6e0 00007ffc`66a32dcd ppapi_shared!ppapi::TrackedCallback::Run+0x20f [C:\src\chromium\src\ppapi\shared_impl\tracked_callback.cc @ 141] 
12 00000001`40dfc790 00007ffc`66a3367f ppapi_proxy!ppapi::proxy::Graphics2DResource::OnPluginMsgFlushACK+0x3d [C:\src\chromium\src\ppapi\proxy\graphics_2d_resource.cc @ 161] 
13 00000001`40dfc7d0 00007ffc`66a3358f ppapi_proxy!base::internal::FunctorTraits<void (ppapi::proxy::Graphics2DResource::*)(const ppapi::proxy::ResourceMessageReplyParams &),void>::Invoke<void (ppapi::proxy::Graphics2DResource::*)(const ppapi::proxy::ResourceMessageReplyParams &),const scoped_refptr<ppapi::proxy::Graphics2DResource> &,const ppapi::proxy::ResourceMessageReplyParams &>+0x5f [C:\src\chromium\src\base\bind_internal.h @ 498] 
14 00000001`40dfc830 00007ffc`66a33512 ppapi_proxy!base::internal::InvokeHelper<0,void>::MakeItSo<void (ppapi::proxy::Graphics2DResource::*const &)(const ppapi::proxy::ResourceMessageReplyParams &),const scoped_refptr<ppapi::proxy::Graphics2DResource> &,const ppapi::proxy::ResourceMessageReplyParams &>+0x6f [C:\src\chromium\src\base\bind_internal.h @ 598] 
15 00000001`40dfc8a0 00007ffc`66a33424 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (ppapi::proxy::Graphics2DResource::*)(const ppapi::proxy::ResourceMessageReplyParams &),scoped_refptr<ppapi::proxy::Graphics2DResource> >,void (const ppapi::proxy::ResourceMessageReplyParams &)>::RunImpl<void (ppapi::proxy::Graphics2DResource::*const &)(const ppapi::proxy::ResourceMessageReplyParams &),const std::__1::tuple<scoped_refptr<ppapi::proxy::Graphics2DResource> > &,0>+0x62 [C:\src\chromium\src\base\bind_internal.h @ 671] 
16 00000001`40dfc900 00007ffc`669f87f7 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (ppapi::proxy::Graphics2DResource::*)(const ppapi::proxy::ResourceMessageReplyParams &),scoped_refptr<ppapi::proxy::Graphics2DResource> >,void (const ppapi::proxy::ResourceMessageReplyParams &)>::Run+0x54 [C:\src\chromium\src\base\bind_internal.h @ 653] 
17 00000001`40dfc950 00007ffc`669f877f ppapi_proxy!base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)>::Run+0x57 [C:\src\chromium\src\base\callback.h @ 132] 
18 00000001`40dfc9b0 00007ffc`669f86d6 ppapi_proxy!ppapi::proxy::DispatchResourceReplyImpl<base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)> &,std::__1::tuple<> &>+0x2f [C:\src\chromium\src\ppapi\proxy\dispatch_reply_message.h @ 58] 
19 00000001`40dfca00 00007ffc`66a34854 ppapi_proxy!ppapi::proxy::DispatchResourceReply<base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)> &,std::__1::tuple<> &>+0x56 [C:\src\chromium\src\ppapi\proxy\dispatch_reply_message.h @ 72] 
1a 00000001`40dfca60 00007ffc`66a346a0 ppapi_proxy!ppapi::proxy::DispatchResourceReplyOrDefaultParams<IPC::MessageT<PpapiPluginMsg_Graphics2D_FlushAck_Meta>,base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)> &>+0x144 [C:\src\chromium\src\ppapi\proxy\dispatch_reply_message.h @ 143] 
1b 00000001`40dfcc20 00007ffc`66a72a9a ppapi_proxy!ppapi::proxy::PluginResourceCallback<IPC::MessageT<PpapiPluginMsg_Graphics2D_FlushAck_Meta>,base::RepeatingCallback<void (const ppapi::proxy::ResourceMessageReplyParams &)> >::Run+0x30 [C:\src\chromium\src\ppapi\proxy\plugin_resource_callback.h @ 41] 
1c 00000001`40dfcc60 00007ffc`66a6f782 ppapi_proxy!ppapi::proxy::PluginResource::OnReplyReceived+0x35a [C:\src\chromium\src\ppapi\proxy\plugin_resource.cc @ 63] 
1d 00000001`40dfcec0 00007ffc`66a71b9d ppapi_proxy!ppapi::proxy::PluginMessageFilter::DispatchResourceReply+0x152 [C:\src\chromium\src\ppapi\proxy\plugin_message_filter.cc @ 117] 
1e 00000001`40dfd080 00007ffc`66a71add ppapi_proxy!base::internal::FunctorTraits<void (*)(const ppapi::proxy::ResourceMessageReplyParams &, const IPC::Message &),void>::Invoke<void (*)(const ppapi::proxy::ResourceMessageReplyParams &, const IPC::Message &),ppapi::proxy::ResourceMessageReplyParams,IPC::Message>+0x4d [C:\src\chromium\src\base\bind_internal.h @ 398] 
1f 00000001`40dfd0d0 00007ffc`66a71a6d ppapi_proxy!base::internal::InvokeHelper<0,void>::MakeItSo<void (*)(const ppapi::proxy::ResourceMessageReplyParams &, const IPC::Message &),ppapi::proxy::ResourceMessageReplyParams,IPC::Message>+0x4d [C:\src\chromium\src\base\bind_internal.h @ 598] 
20 00000001`40dfd120 00007ffc`66a7194e ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (*)(const ppapi::proxy::ResourceMessageReplyParams &, const IPC::Message &),ppapi::proxy::ResourceMessageReplyParams,IPC::Message>,void ()>::RunImpl<void (*)(const ppapi::proxy::ResourceMessageReplyParams &, const IPC::Message &),std::__1::tuple<ppapi::proxy::ResourceMessageReplyParams,IPC::Message>,0,1>+0x6d [C:\src\chromium\src\base\bind_internal.h @ 671] 
21 00000001`40dfd170 00007ffc`82e121b1 ppapi_proxy!base::internal::Invoker<base::internal::BindState<void (*)(const ppapi::proxy::ResourceMessageReplyParams &, const IPC::Message &),ppapi::proxy::ResourceMessageReplyParams,IPC::Message>,void ()>::RunOnce+0x4e [C:\src\chromium\src\base\bind_internal.h @ 640] 
22 00000001`40dfd1c0 00007ffc`830077b2 base!base::OnceCallback<void ()>::Run+0x61 [C:\src\chromium\src\base\callback.h @ 99] 
23 00000001`40dfd220 00007ffc`8306487d base!base::TaskAnnotator::RunTask+0x622 [C:\src\chromium\src\base\task\common\task_annotator.cc @ 144] 
24 00000001`40dfd6a0 00007ffc`83063f23 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x6dd [C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 366] 
25 00000001`40dfdc80 00007ffc`82edcad4 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork+0xb3 [C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 221] 
26 00000001`40dfdd80 00007ffc`83065c57 base!base::MessagePumpDefault::Run+0x74 [C:\src\chromium\src\base\message_loop\message_pump_default.cc @ 40] 
27 00000001`40dfde20 00007ffc`82f8f745 base!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x367 [C:\src\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 467] 
28 00000001`40dfe2c0 00007ffc`6e29545a base!base::RunLoop::Run+0x385 [C:\src\chromium\src\base\run_loop.cc @ 156] 
29 00000001`40dfe660 00007ffc`72253059 content!content::PpapiPluginMain+0x52a [C:\src\chromium\src\content\ppapi_plugin\ppapi_plugin_main.cc @ 159] 
2a 00000001`40dfea20 00007ffc`722541b1 content!content::RunOtherNamedProcessTypeMain+0xc9 [C:\src\chromium\src\content\app\content_main_runner_impl.cc @ 570] 
2b 00000001`40dfea90 00007ffc`7224f497 content!content::ContentMainRunnerImpl::Run+0x291 [C:\src\chromium\src\content\app\content_main_runner_impl.cc @ 889] 
2c 00000001`40dfede0 00007ffc`4b412325 content!content::ContentServiceManagerMainDelegate::RunEmbedderProcess+0x37 [C:\src\chromium\src\content\app\content_service_manager_main_delegate.cc @ 52] 
2d 00000001`40dfee20 00007ffc`72252e1f embedder!service_manager::Main+0x6c5 [C:\src\chromium\src\services\service_manager\embedder\main.cc @ 423] 
2e 00000001`40dff4d0 00007ffc`740c12ff content!content::ContentMain+0x5f [C:\src\chromium\src\content\app\content_main.cc @ 20] 
2f 00000001`40dff570 00007ff7`a8b19335 chrome!ChromeMain+0x1cf [C:\src\chromium\src\chrome\app\chrome_main.cc @ 110] 
30 00000001`40dff6e0 00007ff7`a8b11471 chrome_exe!MainDllLoader::Launch+0x475 [C:\src\chromium\src\chrome\app\main_dll_loader_win.cc @ 203] 
31 00000001`40dff890 00007ff7`a8d75622 chrome_exe!wWinMain+0x471 [C:\src\chromium\src\chrome\app\chrome_exe_main_win.cc @ 234] 
32 00000001`40dffdc0 00007ff7`a8d7575e chrome_exe!invoke_main+0x32 [d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 123] 
33 00000001`40dffe00 00007ff7`a8d757de chrome_exe!__scrt_common_main_seh+0x12e [d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
34 00000001`40dffe70 00007ff7`a8d757f9 chrome_exe!__scrt_common_main+0xe [d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 331] 
35 00000001`40dffea0 00007ffc`f5357974 chrome_exe!wWinMainCRTStartup+0x9 [d:\agent\_work\3\s\src\vctools\crt\vcstartup\src\startup\exe_wwinmain.cpp @ 17] 
36 00000001`40dffed0 00007ffc`f761a271 KERNEL32!BaseThreadInitThunk+0x14
37 00000001`40dfff00 00000000`00000000 ntdll!RtlUserThreadStart+0x21


### aj...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-10-15)

Detailed Report: https://clusterfuzz.com/testcase?key=6249479941259264

Fuzzer: 
Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c000004f60
Crash State:
  RenderPageImpl
  RenderPageWithContext
  FPDF_RenderPageBitmap_Start
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=569055:569062

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6249479941259264

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6249479941259264 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sh...@chromium.org (2019-10-15)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-10-15)

Will take a look, though we are probably not going to have time to fix this in M77.

### th...@chromium.org (2019-10-15)

I thought of a couple potential ways to work on this bug, that can be combined:
a. Turn this into a non-security crash by using CPDF_ArrayLocker in CPDF_AnnotList::CPDF_AnnotList().
b. Verify object types in CPVT_GenerateAP::GenerateFormAP(), though that's not foolproof because objects can also just omit their /Type.

Following up on (b), we may want to try maintaining a map of all objects and their (deduced) types. If we first saw object X 0 as a page dictionary, we shouldn't also treat it as another type of dictionary. This object confusion/reuse is most commonly used for security exploits. We'll have to assess how many real world PDFs would ever do this.

There may be more we can do, I'll see what comes to mind.

### th...@chromium.org (2019-10-16)

Hmm, can't actually do (a) because CPDF_ArrayLocker wants a const pointer and hands out const iterators. Maybe we need to be more careful in CPVT_GenerateAP::GenerateFormAP().

### th...@chromium.org (2019-10-16)

(b) will work in this case, because font dictionaries must have a /Type /Font entry per PDF spec. It's cannot be omitted like some other dictionary /Type entries. So we can validate that in CPVT_GenerateAP::GenerateFormAP() and prevent this bug.

### th...@chromium.org (2019-10-16)

Nope, we are back to (b) being not foolproof because I was looking at the font dictionary, but /DR's /Font entry is a dictionary of font dictionaries, with no /Type at all.

Maybe we should check if the resource dictionary does not have a /Type then? Or check to make sure all of its entries are fonts? I might try the latter and see if anything breaks.

### th...@chromium.org (2019-10-16)

https://pdfium-review.googlesource.com/61450 verifies font resource dictionaries.



### th...@chromium.org (2019-10-16)

Another approach to fixing this is to avoid modifying existing dictionaries. Clone them instead. As an optimization to avoid excessive cloning, we would keep track of the cloned dictionaries and their purpose, so we can look that up to avoid cloning again on future modifications.

### sh...@chromium.org (2019-10-16)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-10-17)

Well, I'll just go with https://pdfium-review.googlesource.com/61450 for now.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-17)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/94e600d98301661502135a89db1fb0cc7caae5e9

commit 94e600d98301661502135a89db1fb0cc7caae5e9
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Oct 17 17:29:01 2019

Verify font resource dictionaries.

Font dictionaries are required to have a /Type /Font entry, and font
resource dictionaries should be made up of valid font dictionaries.
Verify this in places that use font resource dictionaries, to prevent
accidentally treating other objects as font resource dictionaries.

Add ValidateDictType() and ValidateResourceDict() helper functions, with
unit tests, to do this validation.

Bug: chromium:1013868
Change-Id: I6ae2b60d35ea396f47cd5a9c80e8f138ef9d264b
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/61450
Commit-Queue: Lei Zhang <thestig@chromium.org>
Commit-Queue: dsinclair <dsinclair@chromium.org>
Reviewed-by: dsinclair <dsinclair@chromium.org>
Reviewed-by: Chris Palmer <palmer@chromium.org>

[modify] https://pdfium.googlesource.com/pdfium/+/94e600d98301661502135a89db1fb0cc7caae5e9/core/fpdfdoc/cpdf_formfield.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/94e600d98301661502135a89db1fb0cc7caae5e9/core/fpdfapi/parser/fpdf_parser_utility_unittest.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/94e600d98301661502135a89db1fb0cc7caae5e9/core/fpdfdoc/cpvt_generateap.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/94e600d98301661502135a89db1fb0cc7caae5e9/core/fpdfapi/parser/fpdf_parser_utility.h
[modify] https://pdfium.googlesource.com/pdfium/+/94e600d98301661502135a89db1fb0cc7caae5e9/core/fpdfdoc/cpvt_fontmap.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/94e600d98301661502135a89db1fb0cc7caae5e9/core/fpdfdoc/cpdf_formcontrol.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/94e600d98301661502135a89db1fb0cc7caae5e9/core/fpdfdoc/cpdf_interactiveform.cpp
[modify] https://pdfium.googlesource.com/pdfium/+/94e600d98301661502135a89db1fb0cc7caae5e9/core/fpdfapi/parser/fpdf_parser_utility.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/777c570b1042e3e2554a7a57e7fe9431c5d44415

commit 777c570b1042e3e2554a7a57e7fe9431c5d44415
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Oct 17 20:29:48 2019

Roll src/third_party/pdfium 1f088ab877cb..94e600d98301 (2 commits)

https://pdfium.googlesource.com/pdfium.git/+log/1f088ab877cb..94e600d98301

git log 1f088ab877cb..94e600d98301 --date=short --no-merges --format='%ad %ae %s'
2019-10-17 thestig@chromium.org Verify font resource dictionaries.
2019-10-17 thestig@chromium.org Add a JavaScript test for AFDate_FormatEx().

Created with:
  gclient setdep -r src/third_party/pdfium@94e600d98301

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

Bug: chromium:1013868,chromium:572901
Change-Id: I7c900f247a67da175eabf06115ad04fe1f9d3f11
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1867029
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#707062}

[modify] https://crrev.com/777c570b1042e3e2554a7a57e7fe9431c5d44415/DEPS


### cl...@chromium.org (2019-10-18)

ClusterFuzz testcase 6249479941259264 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_pdfium&range=707014:707072

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### th...@chromium.org (2019-10-18)

Thanks ClusterFuzz. I still have more work to do on this bug to merge to various branches.

### th...@chromium.org (2019-10-18)

Missed the M79 branch cut, so first order of business is to merge to M79.

### sh...@chromium.org (2019-10-18)

This bug requires manual review: We don't branch M79 until 2019-10-17.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-10-18)

1. Yes
2. https://pdfium-review.googlesource.com/c/pdfium/+/61450
3. Yes, see https://crbug.com/chromium/1013868#c21.
4. Because it's a security bug.
5. No.
6. N/A.

### sh...@chromium.org (2019-10-19)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-10-21)

Approving merge to M79 branch 3945 per https://crbug.com/chromium/1013868#c25, please merge ASAP. Thank you.

+adetaylor@ & +pbommana@ as FYI

### na...@google.com (2019-10-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-10-21)

Please merge your change to M79 branch 3945 ASAP so we can take it in for this week Dev release of M79 branch. Thank you.

### go...@chromium.org (2019-10-22)

Please merge your change to M79 branch 3945 now so we can pick it up for tomorrow's M79 Dev Release. Thank you.

### th...@chromium.org (2019-10-22)

Merged here: https://pdfium-review.googlesource.com/c/pdfium/+/61630 - not sure why Bugdroid didn't pick it up.

### th...@chromium.org (2019-10-23)

The M79 merge is now on Dev Channel. I'll let that bake for a few days and request the M78 merge first thing next week.

### na...@google.com (2019-10-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-10-23)

Congrats! The Panel decided to award $2,000 for this report :) 

### ba...@gmail.com (2019-10-24)

natashapabrai@ Thanks for notification. Which award was decided for this report? 7500(https://crbug.com/chromium/1013868#c33) or 2000(https://crbug.com/chromium/1013868#c34)?

### na...@google.com (2019-10-24)

Whoops sorry my mistake it should be $7,500 :) 

### na...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### th...@chromium.org (2019-10-29)

Hmm, NextAction didn't fire, but I remembered anyway. We should merge to M78.

### sh...@chromium.org (2019-10-29)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-10-29)

re: https://crbug.com/chromium/1013868#c39 - see https://crbug.com/chromium/1013868#c25.

### sr...@google.com (2019-10-29)

Merge approved for M78 branch:3904, 

### th...@chromium.org (2019-10-29)

Merged to branch 3904: https://pdfium.googlesource.com/pdfium/+/61d5b39075761403ae37242780f0365136deef4d

### th...@chromium.org (2019-10-29)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-31)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-31)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1013868?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050414)*
