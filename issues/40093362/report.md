# Heap-use-after-free in CPDF_ShadingPattern::Load()

| Field | Value |
|-------|-------|
| **Issue ID** | [40093362](https://issues.chromium.org/issues/40093362) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2018-12-10 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This is same bug as 901654. Only free stack is different.  

<https://crbug.com/chromium/901654> had this fix, which handled all similar cases like this new bug.  

<https://pdfium.googlesource.com/pdfium/+/1399a22912fa38b0d5af2532cd0b37b0b3951d50>

But that fix was reverted under this revision.  

<https://pdfium.googlesource.com/pdfium/+/3abd19f69ea7c319a3316268ebcf1bb0192f7dbf>

**VERSION**  

Chrome Version: [71.0.3578.80] + [stable]  

[73.0.3635.0] + [trunk build]  

Operating System: [Ubuntu 18.04, Windows 10]

**REPRODUCTION CASE**

1. Download pattern3.html and pattern3.pdf files to same folder.
2. Open chrome and open pattern3.html file.
3. If above step did not crash PDF Plugin Process, Please wait 20 seconds.  
   
   pattern3.html will resize PDF embed tag and cause a repaint.  
   
   PDF plugin process will crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [PDF Plugin Proces]  

Crash State: [Address Sanitizer Output]

==3757==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060000517a0 at pc 0x55f5c526f88f bp 0x7ffeea051570 sp 0x7ffeea051568  

READ of size 8 at 0x6060000517a0 thread T0 (chrome)  

#0 0x55f5c526f88e in CPDF\_ShadingPattern::Load() /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_shadingpattern.cpp:67:38  

#1 0x55f5c53844d4 in CPDF\_RenderStatus::DrawShadingPattern(CPDF\_ShadingPattern\*, CPDF\_PageObject const\*, CFX\_Matrix const&, bool) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:2114:17  

#2 0x55f5c53891f6 in CPDF\_RenderStatus::DrawPathWithPattern(CPDF\_PathObject\*, CFX\_Matrix const&, CPDF\_Color const\*, bool) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:2345:5  

#3 0x55f5c5369c40 in CPDF\_RenderStatus::ProcessPathPattern(CPDF\_PathObject\*, CFX\_Matrix const&, int\*, bool\*) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:2358:7  

#4 0x55f5c5367e93 in CPDF\_RenderStatus::ProcessPath(CPDF\_PathObject\*, CFX\_Matrix const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1249:3  

#5 0x55f5c5365160 in CPDF\_RenderStatus::ProcessObjectNoClip(CPDF\_PageObject\*, CFX\_Matrix const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1142:14  

#6 0x55f5c53618d3 in CPDF\_RenderStatus::RenderSingleObject(CPDF\_PageObject\*, CFX\_Matrix const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1078:3  

#7 0x55f5c5378b34 in CPDF\_RenderStatus::DrawTextPathWithPattern(CPDF\_TextObject const\*, CFX\_Matrix const&, CPDF\_Font\*, float, CFX\_Matrix const\*, bool, bool) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1979:5  

#8 0x55f5c536746e in CPDF\_RenderStatus::ProcessText(CPDF\_TextObject\*, CFX\_Matrix const&, CFX\_PathData\*) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1746:5  

#9 0x55f5c53650e4 in CPDF\_RenderStatus::ProcessObjectNoClip(CPDF\_PageObject\*, CFX\_Matrix const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1139:14  

#10 0x55f5c5365919 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject\*, CFX\_Matrix const&, PauseIndicatorIface\*) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_renderstatus.cpp:1108:5  

#11 0x55f5c5356920 in CPDF\_ProgressiveRenderer::Continue(PauseIndicatorIface\*) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_progressiverenderer.cpp:95:30  

#12 0x55f5c5354783 in CPDF\_ProgressiveRenderer::Start(PauseIndicatorIface\*) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/render/cpdf\_progressiverenderer.cpp:44:3  

#13 0x55f5d765d05e in (anonymous namespace)::RenderPageImpl(CPDF\_PageRenderContext\*, CPDF\_Page\*, CFX\_Matrix const&, FX\_RECT const&, int, bool, IPDFSDK\_PauseAdapter\*) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:120:26  

#14 0x55f5d7659497 in RenderPageWithContext(CPDF\_PageRenderContext\*, fpdf\_page\_t\_\_\*, int, int, int, int, int, int, bool, IPDFSDK\_PauseAdapter\*) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:900:3  

#15 0x55f5d7643b2e in FPDF\_RenderPageBitmap\_Start /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_progressive.cpp:59:3  

#16 0x55f5d74c67f0 in chrome\_pdf::PDFiumEngine::ContinuePaint(int, pp::ImageData\*) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2996:10  

#17 0x55f5d74c4278 in chrome\_pdf::PDFiumEngine::Paint(pp::Rect const&, pp::ImageData\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:840:11  

#18 0x55f5d7456fac in chrome\_pdf::OutOfProcessInstance::OnPaint(std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) > const&, std::\_\_1::vector<PaintManager::ReadyRect, std::\_\_1::allocator[PaintManager::ReadyRect](javascript:void(0);) >\*, std::\_\_1::vector<pp::Rect, std::\_\_1::allocator[pp::Rect](javascript:void(0);) >\*) /chromium/src/out/asan/../../pdf/out\_of\_process\_instance.cc:1196:16  

#19 0x55f5d748dd8a in PaintManager::DoPaint() /chromium/src/out/asan/../../pdf/paint\_manager.cc:235:12  

...

0x6060000517a0 is located 0 bytes inside of 56-byte region [0x6060000517a0,0x6060000517d8)  

freed by thread T0 (chrome) here:  

#0 0x55f5bd48e2d2 in operator delete(void\*) *asan\_rtl*:3  

#1 0x55f5c4c67141 in CPDF\_Dictionary::~CPDF\_Dictionary() /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:32:37  

#2 0x55f5c4c73e9f in std::\_\_1::default\_delete<CPDF\_Object>::operator()(CPDF\_Object\*) const /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:2325:5  

#3 0x55f5c4c73e9f in std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >::reset(CPDF\_Object\*) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:2638:0  

#4 0x55f5c4c73e9f in std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >::~unique\_ptr() /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:2592:0  

#5 0x55f5c4c73e9f in std::\_\_1::pair<fxcrt::ByteString const, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >::~~pair() /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/utility:315:0  

#6 0x55f5c4c73c3c in void std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> > >::\_\_destroy<std::\_\_1::pair<fxcrt::ByteString const, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > >(std::\_\_1::integral\_constant<bool, false>, std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> >&, std::\_\_1::pair<fxcrt::ByteString const, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >\*) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1734:23  

#7 0x55f5c4c73c3c in void std::\_\_1::allocator\_traits<std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> > >::destroy<std::\_\_1::pair<fxcrt::ByteString const, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > >(std::\_\_1::allocator<std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*> >&, std::\_\_1::pair<fxcrt::ByteString const, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >\*) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:1597:0  

#8 0x55f5c4c73c3c in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1863:0  

#9 0x55f5c4c73b92 in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::destroy(std::\_\_1::\_\_tree\_node<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, void\*>\*) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1861:9  

#10 0x55f5c4c73a0b in std::\_\_1::\_\_tree<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::\_\_map\_value\_compare<fxcrt::ByteString, std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), true>, std::\_\_1::allocator<std::\_\_1::\_\_value\_type<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::~~\_\_tree() /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/\_\_tree:1851:3  

#11 0x55f5c4c72074 in std::\_\_1::map<fxcrt::ByteString, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >, std::\_\_1::less[fxcrt::ByteString](javascript:void(0);), std::\_\_1::allocator<std::\_\_1::pair<fxcrt::ByteString const, std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> > > > >::~map() /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/map:873:28  

#12 0x55f5c4c67049 in CPDF\_Dictionary::~CPDF\_Dictionary() /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:40:1  

#13 0x55f5c4c67138 in CPDF\_Dictionary::~CPDF\_Dictionary() /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:32:37  

#14 0x55f5c4c6d234 in std::\_\_1::default\_delete<CPDF\_Object>::operator()(CPDF\_Object\*) const /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:2325:5  

#15 0x55f5c4c6d234 in std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >::reset(CPDF\_Object\*) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:2638:0  

#16 0x55f5c4c6d234 in std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >::operator=(std::\_\_1::unique\_ptr<CPDF\_Object, std::\_\_1::default\_delete<CPDF\_Object> >&&) /chromium/src/out/asan/../../buildtools/third\_party/libc++/trunk/include/memory:2504:0  

#17 0x55f5c4c6d234 in CPDF\_Dictionary::SetFor(fxcrt::ByteString const&, std::\_\_1::unique\_ptr<CPDF\_Object, std::**1::default\_delete<CPDF\_Object> >) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:216:0  

#18 0x55f5c58af2cf in std::1::enable\_if<CanInternStrings<CPDF\_String>::value, CPDF\_String\*>::type CPDF\_Dictionary::SetNewFor<CPDF\_String, char const (&) [5], bool>(fxcrt::ByteString const&, char const (&) [5], bool&&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.h:93:28  

#19 0x55f5c5874f30 in CPWL\_AppStream::SetAsPushButton() /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/pwl/cpwl\_appstream.cpp:1218:21  

#20 0x55f5c5512131 in CPDFSDK\_Widget::ResetAppearance(pdfium::Optional[fxcrt::WideString](javascript:void(0);), bool) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widget.cpp:605:17  

#21 0x55f5c5518494 in CPDFSDK\_WidgetHandler::OnLoad(CPDFSDK\_Annot\*) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_widgethandler.cpp:206:14  

#22 0x55f5c54911c2 in CPDFSDK\_AnnotHandlerMgr::Annot\_OnLoad(CPDFSDK\_Annot\*) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_annothandlermgr.cpp:67:28  

#23 0x55f5c550c09a in CPDFSDK\_PageView::LoadFXAnnots() /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_pageview.cpp:514:23  

#24 0x55f5c54e2e7d in CPDFSDK\_FormFillEnvironment::GetPageView(IPDF\_Page\*, bool) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/cpdfsdk\_formfillenvironment.cpp:541:14  

#25 0x55f5d7623755 in (anonymous namespace)::FormHandleToPageView(fpdf\_form\_handle\_t\*, fpdf\_page\_t**\*) /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_formfill.cpp:176:39  

#26 0x55f5d76259ec in FORM\_OnAfterLoadPage /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_formfill.cpp:642:37  

#27 0x55f5d75b4f38 in chrome\_pdf::PDFiumPage::GetPage() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_page.cc:131:7  

#28 0x55f5d75bf39a in chrome\_pdf::PDFiumPage::GetPageFeatures() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_page.cc:574:20  

#29 0x55f5d74bf7e1 in chrome\_pdf::PDFiumEngine::CalculateVisiblePages() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2868:55  

#30 0x55f5d74bca12 in chrome\_pdf::PDFiumEngine::PluginSizeUpdated(pp::Size const&) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:756:3  

#31 0x55f5d744d196 in chrome\_pdf::OutOfProcessInstance::OnGeometryChanged(double, float) /chromium/src/out/asan/../../pdf/out\_of\_process\_instance.cc:1877:12  

#32 0x55f5d745d913 in chrome\_pdf::OutOfProcessInstance::DocumentSizeUpdated(pp::Size const&) /chromium/src/out/asan/../../pdf/out\_of\_process\_instance.cc:1321:3  

#33 0x55f5d74d1b99 in chrome\_pdf::PDFiumEngine::LoadPageInfo(bool) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2788:14  

#34 0x55f5d7513192 in chrome\_pdf::PDFiumEngine::LoadPages() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2816:5  

#35 0x55f5d74d544d in chrome\_pdf::PDFiumEngine::LoadBody() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2805:3  

#36 0x55f5d7511401 in chrome\_pdf::PDFiumEngine::ContinueLoadingDocument(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2703:3  

#37 0x55f5d74d4ca7 in chrome\_pdf::PDFiumEngine::LoadDocument() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2622:5

previously allocated by thread T0 (chrome) here:  

#0 0x55f5bd48d692 in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55f5c483e64f in pdfium::internal::MakeUniqueResult<CPDF\_Dictionary>::Scalar pdfium::MakeUnique<CPDF\_Dictionary, fxcrt::WeakPtr<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);), std::\_\_1::default\_delete<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);) > >&>(fxcrt::WeakPtr<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);), std::\_\_1::default\_delete<fxcrt::StringPoolTemplate[fxcrt::ByteString](javascript:void(0);) > >&) /chromium/src/out/asan/../../third\_party/pdfium/third\_party/base/ptr\_util.h:56:29  

#2 0x55f5c4d78a2a in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:484:9  

#3 0x55f5c4d78dd6 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:506:11  

#4 0x55f5c4d78dd6 in CPDF\_SyntaxParser::GetObjectBodyInternal(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:506:11  

#5 0x55f5c4d7da70 in CPDF\_SyntaxParser::GetIndirectObject(CPDF\_IndirectObjectHolder\*, CPDF\_SyntaxParser::ParseType) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_syntax\_parser.cpp:559:7  

#6 0x55f5c4d243a9 in CPDF\_Parser::ParseIndirectObjectAt(long, unsigned int) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:921:28  

#7 0x55f5c4d26844 in CPDF\_Parser::ParseIndirectObject(unsigned int) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_parser.cpp:870:12  

#8 0x55f5c4c7c88e in CPDF\_Document::ParseIndirectObject(unsigned int) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_document.cpp:194:33  

#9 0x55f5c4cc0757 in CPDF\_IndirectObjectHolder::GetOrParseIndirectObject(unsigned int) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_indirect\_object\_holder.cpp:50:42  

#10 0x55f5c4d4a971 in CPDF\_Reference::GetDirect() const /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_reference.cpp:98:35  

#11 0x55f5c4c6ad4d in CPDF\_Dictionary::GetDirectObjectFor(fxcrt::ByteString const&) const /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:99:17  

#12 0x55f5c4c6b2ec in CPDF\_Dictionary::GetDictFor(fxcrt::ByteString const&) const /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:148:26  

#13 0x55f5c4c6b48c in CPDF\_Dictionary::GetDictFor(fxcrt::ByteString const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/parser/cpdf\_dictionary.cpp:160:50  

#14 0x55f5c529ae94 in CPDF\_StreamContentParser::FindResourceHolder(fxcrt::ByteString const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1141:42  

#15 0x55f5c529d4c0 in CPDF\_StreamContentParser::FindResourceObj(fxcrt::ByteString const&, fxcrt::ByteString const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1153:30  

#16 0x55f5c52a46a2 in CPDF\_StreamContentParser::FindPattern(fxcrt::ByteString const&, bool) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1204:7  

#17 0x55f5c52955d8 in CPDF\_StreamContentParser::Handle\_SetColorPS\_Fill() /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1063:28  

#18 0x55f5c52979fb in CPDF\_StreamContentParser::OnOperator(fxcrt::StringViewTemplate<char> const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:571:5  

#19 0x55f5c52a8c26 in CPDF\_StreamContentParser::Parse(unsigned char const\*, unsigned int, unsigned int, unsigned int, std::\_\_1::vector<unsigned int, std::\_\_1::allocator<unsigned int> > const&) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_streamcontentparser.cpp:1534:9  

#20 0x55f5c51ab4f7 in CPDF\_ContentParser::Parse() /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_contentparser.cpp:211:33  

#21 0x55f5c51a7586 in CPDF\_ContentParser::Continue(PauseIndicatorIface\*) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_contentparser.cpp:133:22  

#22 0x55f5c522ebee in CPDF\_PageObjectHolder::ContinueParse(PauseIndicatorIface\*) /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_pageobjectholder.cpp:60:18  

#23 0x55f5c522a465 in CPDF\_Page::ParseContent() /chromium/src/out/asan/../../third\_party/pdfium/core/fpdfapi/page/cpdf\_page.cpp:110:3  

#24 0x55f5d765848f in FPDF\_LoadPage /chromium/src/out/asan/../../third\_party/pdfium/fpdfsdk/fpdf\_view.cpp:339:10  

#25 0x55f5d75b4d64 in chrome\_pdf::PDFiumPage::GetPage() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_page.cc:129:17  

#26 0x55f5d75bf39a in chrome\_pdf::PDFiumPage::GetPageFeatures() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_page.cc:574:20  

#27 0x55f5d74bf7e1 in chrome\_pdf::PDFiumEngine::CalculateVisiblePages() /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:2868:55  

#28 0x55f5d74bca12 in chrome\_pdf::PDFiumEngine::PluginSizeUpdated(pp::Size const&) /chromium/src/out/asan/../../pdf/pdfium/pdfium\_engine.cc:756:3  

#29 0x55f5d744d196 in chrome\_pdf::OutOfProcessInstance::OnGeometryChanged(double, float) /chromium/src/out/asan/../../pdf/out\_of\_process\_instance.cc:1877:12

**CREDIT INFORMATION**  

Reporter credit: [Uncredited]

## Attachments

- [pattern3.html](attachments/pattern3.html) (text/plain, 169 B)
- [pattern3.pdf](attachments/pattern3.pdf) (application/pdf, 1.1 KB)

## Timeline

### cl...@chromium.org (2018-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5632479786172416.

### mm...@chromium.org (2018-12-10)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### cl...@chromium.org (2018-12-10)

Detailed report: https://clusterfuzz.com/testcase?key=5632479786172416

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c0000d5380
Crash State:
  CPDF_ShadingPattern::Load
  CPDF_RenderStatus::DrawShadingPattern
  CPDF_RenderStatus::ProcessPathPattern
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5632479786172416

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### mm...@chromium.org (2018-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-24)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-07)

tsepez: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2019-01-07)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-01-30)

Chrome stable version 72 was released yesterday.
But this bug is still present.
I tested on my local build.
Chrome version: 74.0.3687.0 (Developer Build) (64-bit)

Does this bug reproduce for you?

### ts...@chromium.org (2019-01-30)

Yes, this is still open. I've not come up with a good solution, yet.

### sh...@chromium.org (2019-02-08)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2019-02-14)

Will this bug be fixed in chrome 73?

### ts...@chromium.org (2019-02-16)

No, not 73.  This is an unusual situation as I've been struggling in my attempts to find the correct solution, so the reporter hasn't been paid despite reporting a quality bug some time ago. I'm flipping this over to the panel even though the bug is not fixed to see if they have a policy for this situation.


### ts...@chromium.org (2019-03-04)

https://pdfium-review.googlesource.com/c/pdfium/+/51451 whacks this particular mole, but short of ref-counting all these objects, I expect the reporter will find similar examples lurking.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-04)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/9384947f47f28811e7b15b0c267e89a277d24880

commit 9384947f47f28811e7b15b0c267e89a277d24880
Author: Tom Sepez <tsepez@chromium.org>
Date: Mon Mar 04 22:21:11 2019

Do not replace existing objects in CPWL_AppStream::SetAsPushButton

An empty string is no assurance of a key not being set.

Bug: chromium:913320
Change-Id: Ia06d0cbe0fa7c2ee662c8fb3d0d537878e80a1ed
Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/51451
Commit-Queue: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/9384947f47f28811e7b15b0c267e89a277d24880/fpdfsdk/pwl/cpwl_appstream.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d8b4303ff94dfe0e1ba7bc38ab2521fe87c7d323

commit d8b4303ff94dfe0e1ba7bc38ab2521fe87c7d323
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Mar 04 23:51:19 2019

Roll src/third_party/pdfium 9bbc2313bfd2..9384947f47f2 (1 commits)

https://pdfium.googlesource.com/pdfium.git/+log/9bbc2313bfd2..9384947f47f2


git log 9bbc2313bfd2..9384947f47f2 --date=short --no-merges --format='%ad %ae %s'
2019-03-04 tsepez@chromium.org Do not replace existing objects in CPWL_AppStream::SetAsPushButton


Created with:
  gclient setdep -r src/third_party/pdfium@9384947f47f2

The AutoRoll server is located here: https://autoroll.skia.org/r/pdfium-autoroll

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.



BUG=chromium:913320
TBR=dsinclair@chromium.org

Change-Id: Ie074e2f575c0cd5b6fc497d08bd6f79eca3e6f83
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1501033
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#637485}
[modify] https://crrev.com/d8b4303ff94dfe0e1ba7bc38ab2521fe87c7d323/DEPS


### ts...@chromium.org (2019-03-05)

[Empty comment from Monorail migration]

### aw...@google.com (2019-03-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-03-05)

ClusterFuzz has detected this issue as fixed in range 637484:637490.

Detailed report: https://clusterfuzz.com/testcase?key=5632479786172416

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60c0000d5380
Crash State:
  CPDF_ShadingPattern::Load
  CPDF_RenderStatus::DrawShadingPattern
  CPDF_RenderStatus::ProcessPathPattern
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=637484:637490

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5632479786172416

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2019-03-05)

ClusterFuzz testcase 5632479786172416 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### na...@google.com (2019-03-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-03-14)

Congrats! The Panel decided to reward $3,000 for this report :) 

### aw...@google.com (2019-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This bug requires manual review: M74 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-03-26)

Discussing with abdulsyed@ - this landed before the M74 branch so no need for special merge.

### aw...@google.com (2019-04-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/913320?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093362)*
