# Security:  heap-use-after-free in blink::InvalidatableInterpolation::MaybeConvertPairwise

| Field | Value |
|-------|-------|
| **Issue ID** | [40055312](https://issues.chromium.org/issues/40055312) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Animation, Blink>CSS |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | fu...@chromium.org |
| **Created** | 2021-03-24 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap-use-after-free in blink::InvalidatableInterpolation::MaybeConvertPairwise

**VERSION**  

Chrome Version: Chromium Dev(asan-win32-release\_x64-865999)  

Operating System: Windows 20H2

**REPRODUCTION CASE**  

Open the poc.html in the latest chromium.  

C:\chromium\_asan\asan-win32-release\_x64-865999>chrome.exe --no-sandbox --user-data-dir=c:/tmp/crash poc.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]

Crash log

# C:\chromium\_asan\asan-win32-release\_x64-865999>chrome.exe --no-sandbox --user-data-dir=c:/tmp/ppc

==10256==ERROR: AddressSanitizer: heap-use-after-free on address 0x1276ade8a450 at pc 0x7ffc8edc1c95 bp 0x00b12c5fd4e0 sp 0x00b12c5fd528  

READ of size 8 at 0x1276ade8a450 thread T0  

==10256==WARNING: Failed to use and restart external symbolizer!  

==10256==\*\*\* WARNING: Failed to initialize DbgHelp! \*\*\*  

==10256==\*\*\* Most likely this means that the app is already \*\*\*  

==10256==\*\*\* using DbgHelp, possibly with incompatible flags. \*\*\*  

==10256==\*\*\* Due to technical reasons, symbolization might crash \*\*\*  

==10256==\*\*\* or produce wrong results. \*\*\*  

#0 0x7ffc8edc1c94 in blink::InvalidatableInterpolation::MaybeConvertPairwise C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\invalidatable\_interpolation.cc:36  

#1 0x7ffc8edc3791 in blink::InvalidatableInterpolation::EnsureValidConversion C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\invalidatable\_interpolation.cc:165  

#2 0x7ffc8edc4b92 in blink::InvalidatableInterpolation::ApplyStack C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\invalidatable\_interpolation.cc:242  

#3 0x7ffc9285b2e1 in blink::StyleCascade::ApplyInterpolation C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:469  

#4 0x7ffc9285aa5c in blink::StyleCascade::ApplyInterpolationMap C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:453  

#5 0x7ffc92855915 in blink::StyleCascade::ApplyInterpolations C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:426  

#6 0x7ffc928534d4 in blink::StyleCascade::Apply C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:191  

#7 0x7ffc8ee717f3 in blink::StyleResolver::ApplyAnimatedStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:1268  

#8 0x7ffc8ee6efd2 in blink::StyleResolver::ResolveStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:761  

#9 0x7ffc8c3c6c89 in blink::Element::StyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2830  

#10 0x7ffc8c3c9d64 in blink::Element::RecalcOwnStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3026  

#11 0x7ffc8c3c7afb in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2874  

#12 0x7ffc8c674431 in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2055  

#13 0x7ffc8c675e76 in blink::StyleEngine::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2139  

#14 0x7ffc8c0e9ff4 in blink::Document::UpdateStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2425  

#15 0x7ffc8c0e8779 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2378  

#16 0x7ffc8c01ef45 in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3350  

#17 0x7ffc8c01f935 in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:3399  

#18 0x7ffc8c01acc7 in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2718  

#19 0x7ffc8c0194e8 in blink::LocalFrameView::UpdateLifecyclePhasesInternal C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2570  

#20 0x7ffc8c016b45 in blink::LocalFrameView::UpdateLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2515  

#21 0x7ffc8c01651e in blink::LocalFrameView::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\local\_frame\_view.cc:2255  

#22 0x7ffc8efd2ff8 in blink::PageAnimator::UpdateAllLifecyclePhases C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\page\page\_animator.cc:140  

#23 0x7ffc8bfcb87a in blink::WebFrameWidgetImpl::UpdateLifecycle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:1264  

#24 0x7ffc8f0b2c23 in blink::WidgetBase::UpdateVisualState C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\widget\_base.cc:782  

#25 0x7ffc89d7d4d9 in cc::LayerTreeHost::RequestMainFrameUpdate C:\b\s\w\ir\cache\builder\src\cc\trees\layer\_tree\_host.cc:307  

#26 0x7ffc8cc4c168 in cc::ProxyMain::BeginMainFrame C:\b\s\w\ir\cache\builder\src\cc\trees\proxy\_main.cc:261  

#27 0x7ffc90aad9d2 in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::\*)(std::unique\_ptr<cc::BeginMainFrameAndCommitState,std::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) >),base::WeakPtr[cc::ProxyMain](javascript:void(0);),std::unique\_ptr<cc::BeginMainFrameAndCommitState,std::default\_delete[cc::BeginMainFrameAndCommitState](javascript:void(0);) > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:690  

#28 0x7ffc876e5e77 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:173  

#29 0x7ffc89e6bce7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#30 0x7ffc89e6b3c9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:264  

#31 0x7ffc89e33e23 in base::MessagePumpDefault::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39  

#32 0x7ffc89e6d2df in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:460  

#33 0x7ffc8766be33 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:133  

#34 0x7ffc89c4eef3 in content::RendererMain C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:264  

#35 0x7ffc8741fb58 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:947  

#36 0x7ffc8741ce5a in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372  

#37 0x7ffc8741d444 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#38 0x7ffc7d66145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:141  

#39 0x7ff68b1b5bd5 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#40 0x7ff68b1b2bf9 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:369  

#41 0x7ff68b595e5f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#42 0x7ffd0d467033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#43 0x7ffd0da82650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x1276ade8a450 is located 0 bytes inside of 16-byte region [0x1276ade8a450,0x1276ade8a460)  

freed by thread T0 here:  

#0 0x7ff68b2527fb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffc935ba283 in WTF::HashTable<blink::PropertyHandle,WTF::KeyValuePair<blink::PropertyHandle,std::unique\_ptr<const WTF::Vector<std::unique\_ptr<const blink::InterpolationType,std::default\_delete<const blink::InterpolationType> >,0,WTF::PartitionAllocator>,std::default\_delete<const WTF::Vector<std::unique\_ptr<const blink::InterpolationType,std::default\_delete<const blink::InterpolationType> >,0,WTF::PartitionAllocator> > > >,WTF::KeyValuePairKeyExtractor,WTF::DefaultHash[blink::PropertyHandle](javascript:void(0);)::Hash,WTF::HashMapValueTraits<WTF::HashTraits[blink::PropertyHandle](javascript:void(0);),WTF::HashTraits<std::unique\_ptr<const WTF::Vector<std::unique\_ptr<const blink::InterpolationType,std::default\_delete<const blink::InterpolationType> >,0,WTF::PartitionAllocator>,std::default\_delete<const WTF::Vector<std::unique\_ptr<const blink::InterpolationType,std::default\_delete<const blink::InterpolationType> >,0,WTF::PartitionAllocator> > > > >,WTF::HashTraits[blink::PropertyHandle](javascript:void(0);),WTF::PartitionAllocator>::DeleteBucket C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\hash\_table.h:927  

#2 0x7ffc935a5d01 in blink::CSSInterpolationTypesMap::Get C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\css\_interpolation\_types\_map.cc:100  

#3 0x7ffc8edc4a39 in blink::InvalidatableInterpolation::ApplyStack C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\invalidatable\_interpolation.cc:236  

#4 0x7ffc9285b2e1 in blink::StyleCascade::ApplyInterpolation C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:469  

#5 0x7ffc9285aa5c in blink::StyleCascade::ApplyInterpolationMap C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:453  

#6 0x7ffc92855915 in blink::StyleCascade::ApplyInterpolations C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:426  

#7 0x7ffc928534d4 in blink::StyleCascade::Apply C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:191  

#8 0x7ffc8ee717f3 in blink::StyleResolver::ApplyAnimatedStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:1268  

#9 0x7ffc8ee6efd2 in blink::StyleResolver::ResolveStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:761  

#10 0x7ffc8c3c6c89 in blink::Element::StyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2830  

#11 0x7ffc8c3c9d64 in blink::Element::RecalcOwnStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3026  

#12 0x7ffc8c3c7afb in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2874  

#13 0x7ffc8c78cae9 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1361  

#14 0x7ffc8c3c8290 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2941  

#15 0x7ffc8c78cae9 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1361  

#16 0x7ffc8c3c8290 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2941  

#17 0x7ffc8c674431 in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2055  

#18 0x7ffc8c675e76 in blink::StyleEngine::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2139  

#19 0x7ffc8c0e9ff4 in blink::Document::UpdateStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2425  

#20 0x7ffc8c0e8779 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2378  

#21 0x7ffc8c0d6bad in blink::Document::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2298  

#22 0x7ffc8c12bc09 in blink::Document::FinishedParsing C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:6904  

#23 0x7ffc8f64e033 in blink::HTMLDocumentParser::end C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:1355  

#24 0x7ffc8f63b74c in blink::HTMLDocumentParser::PrepareToStopParsing C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:556  

#25 0x7ffc8f63ea3c in blink::HTMLDocumentParser::AttemptToEnd C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:1392  

#26 0x7ffc8f63bc62 in blink::HTMLDocumentParser::PumpTokenizerIfPossible C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:613  

#27 0x7ffc8f63c174 in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:589  

#28 0x7ffc876e5e77 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:173

previously allocated by thread T0 here:  

#0 0x7ff68b2528fb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffc88b87215 in WTF::Partitions::FastMalloc C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\wtf\allocator\partitions.cc:265  

#2 0x7ffc935a5e5a in blink::CSSInterpolationTypesMap::Get C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\css\_interpolation\_types\_map.cc:111  

#3 0x7ffc8edc4a39 in blink::InvalidatableInterpolation::ApplyStack C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\invalidatable\_interpolation.cc:236  

#4 0x7ffc9285b2e1 in blink::StyleCascade::ApplyInterpolation C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:469  

#5 0x7ffc9285aa5c in blink::StyleCascade::ApplyInterpolationMap C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:453  

#6 0x7ffc92855915 in blink::StyleCascade::ApplyInterpolations C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:426  

#7 0x7ffc928534d4 in blink::StyleCascade::Apply C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:191  

#8 0x7ffc8ee717f3 in blink::StyleResolver::ApplyAnimatedStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:1268  

#9 0x7ffc8ee6efd2 in blink::StyleResolver::ResolveStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:761  

#10 0x7ffc8c3c6c89 in blink::Element::StyleForLayoutObject C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2830  

#11 0x7ffc8c3c9d64 in blink::Element::RecalcOwnStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:3026  

#12 0x7ffc8c3c7afb in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2874  

#13 0x7ffc8c78cae9 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1361  

#14 0x7ffc8c3c8290 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2941  

#15 0x7ffc8c78cae9 in blink::ContainerNode::RecalcDescendantStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\container\_node.cc:1361  

#16 0x7ffc8c3c8290 in blink::Element::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\element.cc:2941  

#17 0x7ffc8c674431 in blink::StyleEngine::RecalcStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2055  

#18 0x7ffc8c675e76 in blink::StyleEngine::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\style\_engine.cc:2139  

#19 0x7ffc8c0e9ff4 in blink::Document::UpdateStyle C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2425  

#20 0x7ffc8c0e8779 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2378  

#21 0x7ffc8c0d6bad in blink::Document::UpdateStyleAndLayoutTree C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:2298  

#22 0x7ffc8c12bc09 in blink::Document::FinishedParsing C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\dom\document.cc:6904  

#23 0x7ffc8f64e033 in blink::HTMLDocumentParser::end C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:1355  

#24 0x7ffc8f63b74c in blink::HTMLDocumentParser::PrepareToStopParsing C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:556  

#25 0x7ffc8f63ea3c in blink::HTMLDocumentParser::AttemptToEnd C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:1392  

#26 0x7ffc8f63bc62 in blink::HTMLDocumentParser::PumpTokenizerIfPossible C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:613  

#27 0x7ffc8f63c174 in blink::HTMLDocumentParser::DeferredPumpTokenizerIfPossible C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\html\parser\html\_document\_parser.cc:589  

#28 0x7ffc876e5e77 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:173

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\invalidatable\_interpolation.cc:36 in blink::InvalidatableInterpolation::MaybeConvertPairwise  

Shadow bytes around the buggy address:  

0x04c1839d1430: fa fa fd fd fa fa fd fa fa fa fd fd fa fa 00 00  

0x04c1839d1440: fa fa fd fd fa fa fd fa fa fa fd fa fa fa fd fa  

0x04c1839d1450: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x04c1839d1460: fa fa fd fa fa fa fd fa fa fa 00 fa fa fa 00 fa  

0x04c1839d1470: fa fa 00 fa fa fa 00 fa fa fa 04 fa fa fa 04 fa  

=>0x04c1839d1480: fa fa 04 fa fa fa 00 fa fa fa[fd]fd fa fa fd fa  

0x04c1839d1490: fa fa fd fa fa fa fd fa fa fa fd fa fa fa 04 fa  

0x04c1839d14a0: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd  

0x04c1839d14b0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x04c1839d14c0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x04c1839d14d0: fa fa 00 fa fa fa 00 fa fa fa fd fd fa fa fd fa  

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

==10256==ABORTING

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 19.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)

## Timeline

### [Deleted User] (2021-03-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-03-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5721553292296192.

### cl...@chromium.org (2021-03-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-03-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-03-25)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Animation Blink>CSS]

### ke...@chromium.org (2021-03-25)

Thanks for the report.

futhark@: Can you please have a look at this or else find another owner? I would assign to andruud@ but he appears to be unavailable.

This regression appears when @property was enabled last year (r769658) and I don't know if it is related to https://crbug.com/chromium/1185524 which andruud@ recently fixed.

### cl...@chromium.org (2021-03-25)

Detailed Report: https://clusterfuzz.com/testcase?key=5721553292296192

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6090002cdfe0
Crash State:
  blink::InvalidatableInterpolation::MaybeConvertPairwise
  blink::InvalidatableInterpolation::EnsureValidConversion
  blink::InvalidatableInterpolation::ApplyStack
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=769657:769660

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5721553292296192

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5721553292296192 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2021-03-27)

[Empty comment from Monorail migration]

### fu...@chromium.org (2021-03-29)

[Empty comment from Monorail migration]

### fu...@chromium.org (2021-03-29)

This should be reproducible with the javascript api as well, and the bug was probably introduced here: https://codereview.chromium.org/2618673003/

### fu...@chromium.org (2021-03-30)

https://chromium-review.googlesource.com/c/chromium/src/+/2792423

### gi...@appspot.gserviceaccount.com (2021-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ea0f74c3dfef5f864aba149ae33e4ea6360e9abb

commit ea0f74c3dfef5f864aba149ae33e4ea6360e9abb
Author: Rune Lillesveen <futhark@chromium.org>
Date: Tue Mar 30 18:36:59 2021

Don't erase InterpolationTypes used by other documents

A registered custom property in one document caused the entry for the
same custom property (unregistered) used in another document to be
deleted, which caused a use-after-free.

Only store the CSSDefaultInterpolationType for unregistered custom
properties and never store registered properties in the map. They may
have different types in different documents when registered.

Bug: 1192054
Change-Id: I1af03d0a298795db99acc9c62f0d0fff8a5e801d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2792423
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Robert Flack <flackr@chromium.org>
Cr-Commit-Position: refs/heads/master@{#867692}

[modify] https://crrev.com/ea0f74c3dfef5f864aba149ae33e4ea6360e9abb/third_party/blink/renderer/core/animation/build.gni
[modify] https://crrev.com/ea0f74c3dfef5f864aba149ae33e4ea6360e9abb/third_party/blink/renderer/core/animation/css_interpolation_types_map.cc
[add] https://crrev.com/ea0f74c3dfef5f864aba149ae33e4ea6360e9abb/third_party/blink/renderer/core/animation/css_interpolation_types_map_test.cc


### fu...@chromium.org (2021-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-31)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fu...@chromium.org (2021-03-31)

I added this request early. I have sent a mail to chrome-security@ for evaluation.

1. Requesting evaluation of whether this should be merged because it is tagged as Security_Severity-High based on an external report
2. https://chromium-review.googlesource.com/c/chromium/src/+/2792423
3. No, not in Canary yet
4. Don't think so
5. Fix for use-after-free security issue reported externally
6. No
7. N/A


### ad...@google.com (2021-03-31)

Thanks for the fix - if this is complete, please mark it as Fixed and Sheriffbot will take care of initiating the correct merges.
https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#TOC-Merge-labels
I think in practice we'll aim to merge this back to M90, so any comments on stability concerns or risks are much appreciated.

### fu...@chromium.org (2021-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### fu...@chromium.org (2021-03-31)

Risk should be low. Adding flackr@ who reviewed the CL for a second opinion.


### fl...@chromium.org (2021-03-31)

I agree, the risk should be low.

### [Deleted User] (2021-03-31)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-31)

OK, in that case approving merge to M90; please merge to branch 4430. Thanks.

### gi...@appspot.gserviceaccount.com (2021-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/af77c20371d1418300cefbc5fa6779067b7792cf

commit af77c20371d1418300cefbc5fa6779067b7792cf
Author: Rune Lillesveen <futhark@chromium.org>
Date: Wed Mar 31 22:48:56 2021

Don't erase InterpolationTypes used by other documents

A registered custom property in one document caused the entry for the
same custom property (unregistered) used in another document to be
deleted, which caused a use-after-free.

Only store the CSSDefaultInterpolationType for unregistered custom
properties and never store registered properties in the map. They may
have different types in different documents when registered.

(cherry picked from commit ea0f74c3dfef5f864aba149ae33e4ea6360e9abb)

Bug: 1192054
Change-Id: I1af03d0a298795db99acc9c62f0d0fff8a5e801d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2792423
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Reviewed-by: Robert Flack <flackr@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#867692}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2797576
Auto-Submit: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#962}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/af77c20371d1418300cefbc5fa6779067b7792cf/third_party/blink/renderer/core/animation/build.gni
[modify] https://crrev.com/af77c20371d1418300cefbc5fa6779067b7792cf/third_party/blink/renderer/core/animation/css_interpolation_types_map.cc
[add] https://crrev.com/af77c20371d1418300cefbc5fa6779067b7792cf/third_party/blink/renderer/core/animation/css_interpolation_types_map_test.cc


### cl...@chromium.org (2021-04-01)

ClusterFuzz testcase 5721553292296192 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=867685:867695

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ad...@google.com (2021-04-07)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-07)

Congratulations, 0xasnine@! The VRP Panel has decided to award you $5000 for this report. Nice work!

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ja...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### ad...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-22)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-07-08)

This issue was migrated from crbug.com/chromium/1192054?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Animation, Blink>CSS]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055312)*
