# UaF in PDF accessibility due to relayout

| Field | Value |
|-------|-------|
| **Issue ID** | [40057482](https://issues.chromium.org/issues/40057482) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF, UI>Accessibility |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2021-10-02 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36

Steps to reproduce the problem:
tested chromium version:
	Version 96.0.4655.0 (Developer Build) (64-bit)  build with ASAN
	Chromium 96.0.4660.0 gs://chromium-browser-asan/linux-release/asan-linux-release-927474.zip
os version:
	Ubuntu20.04
1 ./chrome --force-renderer-accessibility http://localhost:8000/crash.html
2 The print dialog will pop up.
3 Manually click refresh, and the crash will repro immediately.

What is the expected behavior?

What went wrong?
==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x61900005b628 at pc 0x558f517e57a1 bp 0x7ffcf87a6e30 sp 0x7ffcf87a6e28
READ of size 8 at 0x61900005b628 thread T0 (chrome)
    #0 0x558f517e57a0 in pdf::PdfAccessibilityTree::SetAccessibilityViewportInfo(chrome_pdf::AccessibilityViewportInfo const&) ./../../buildtools/third_party/libc++/trunk/include/__hash_table:969
    #1 0x558f517e57a0 in size ./../../buildtools/third_party/libc++/trunk/include/unordered_map:1080
    #2 0x558f517e57a0 in size ./../../ui/accessibility/ax_tree.h:169
    #3 0x558f517e57a0 in SetAccessibilityViewportInfo ./../../components/pdf/renderer/pdf_accessibility_tree.cc:1309
    #4 0x558f517e57a0 in ?? ??:0
    #5 0x558f517e089e in base::internal::Invoker<base::internal::BindState<void (chrome_pdf::PdfViewWebPlugin::*)(chrome_pdf::AccessibilityViewportInfo const&), base::WeakPtr<chrome_pdf::PdfViewWebPlugin>, chrome_pdf::AccessibilityViewportInfo>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/bind_internal.h:509
    #6 0x558f517e089e in MakeItSo<void (chrome_pdf::PdfViewWebPlugin::*)(const chrome_pdf::AccessibilityViewportInfo &), base::WeakPtr<chrome_pdf::PdfViewWebPlugin>, chrome_pdf::AccessibilityViewportInfo> ./../../base/bind_internal.h:668
    #7 0x558f517e089e in RunImpl<void (chrome_pdf::PdfViewWebPlugin::*)(const chrome_pdf::AccessibilityViewportInfo &), std::__1::tuple<base::WeakPtr<chrome_pdf::PdfViewWebPlugin>, chrome_pdf::AccessibilityViewportInfo>, 0UL, 1UL> ./../../base/bind_internal.h:721
    #8 0x558f517e089e in RunOnce ./../../base/bind_internal.h:690
    #9 0x558f517e089e in ?? ??:0
    #10 0x558f3d4ae5f3 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) ./../../base/callback.h:99
    #11 0x558f3d4ae5f3 in RunTask ./../../base/task/common/task_annotator.cc:178
    #12 0x558f3d4ae5f3 in ?? ??:0
    #13 0x558f3d4e5b51 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:357
    #14 0x558f3d4e5b51 in ?? ??:0
    #15 0x558f3d4e53a3 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:260
    #16 0x558f3d4e53a3 in ?? ??:0
    #17 0x558f3d4e64c1 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:?
    #18 0x558f3d4e64c1 in ?? ??:0
    #19 0x558f3d3a75ad in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:38
    #20 0x558f3d3a75ad in ?? ??:0
    #21 0x558f3d4e6b8c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:462
    #22 0x558f3d4e6b8c in ?? ??:0
    #23 0x558f3d42a201 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:134
    #24 0x558f3d42a201 in ?? ??:0
    #25 0x558f5150ebc3 in content::RendererMain(content::MainFunctionParams const&) ./../../content/renderer/renderer_main.cc:265
    #26 0x558f5150ebc3 in ?? ??:0
    #27 0x558f3c284823 in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:583
    #28 0x558f3c284823 in ?? ??:0
    #29 0x558f3c2888df in content::ContentMainRunnerImpl::Run(bool) ./../../content/app/content_main_runner_impl.cc:974
    #30 0x558f3c2888df in ?? ??:0
    #31 0x558f3c281e7a in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) ./../../content/app/content_main.cc:390
    #32 0x558f3c281e7a in ?? ??:0
    #33 0x558f3c283a54 in content::ContentMain(content::ContentMainParams const&) ./../../content/app/content_main.cc:418
    #34 0x558f3c283a54 in ?? ??:0
    #35 0x558f2f481fd1 in ChromeMain ./../../chrome/app/chrome_main.cc:172
    #36 0x558f2f481fd1 in ?? ??:0
    #37 0x7fbf3f94b0b2 in __libc_start_main ??:?
    #38 0x7fbf3f94b0b2 in ?? ??:0

0x61900005b628 is located 424 bytes inside of 1080-byte region [0x61900005b480,0x61900005b8b8)
freed by thread T0 (chrome) here:
    #0 0x558f2f47ffcd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152
    #1 0x558f2f47ffcd in ?? ??:0
    #2 0x558f517d2f4c in chrome_pdf::PdfViewWebPlugin::~PdfViewWebPlugin() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54
    #3 0x558f517d2f4c in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315
    #4 0x558f517d2f4c in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269
    #5 0x558f517d2f4c in ~PdfViewWebPlugin ./../../pdf/pdf_view_web_plugin.cc:254
    #6 0x558f517d2f4c in ?? ??:0
    #7 0x558f517d4517 in chrome_pdf::PdfViewWebPlugin::Destroy() ./../../pdf/pdf_view_web_plugin.cc:331
    #8 0x558f517d4517 in ?? ??:0
    #9 0x558f4da9e5ea in blink::WebPluginContainerImpl::Dispose() ./../../third_party/blink/renderer/core/exported/web_plugin_container_impl.cc:790
    #10 0x558f4da9e5ea in ?? ??:0
    #11 0x558f4a9bf7f6 in blink::HTMLFrameOwnerElement::PluginDisposeSuspendScope::PerformDeferredPluginDispose() ./../../third_party/blink/renderer/core/html/html_frame_owner_element.cc:243
    #12 0x558f4a9bf7f6 in ?? ??:0
    #13 0x558f4aa12ace in blink::HTMLPlugInElement::AttachLayoutTree(blink::Node::AttachContext&) ./../../third_party/blink/renderer/core/html/html_frame_owner_element.h:88
    #14 0x558f4aa12ace in AttachLayoutTree ./../../third_party/blink/renderer/core/html/html_plugin_element.cc:208
    #15 0x558f4aa12ace in ?? ??:0
    #16 0x558f49850026 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) ./../../third_party/blink/renderer/core/dom/container_node.cc:1054
    #17 0x558f49850026 in ?? ??:0
    #18 0x558f497e730e in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) ./../../third_party/blink/renderer/core/dom/element.cc:2767
    #19 0x558f497e730e in ?? ??:0
    #20 0x558f49850026 in blink::ContainerNode::AttachLayoutTree(blink::Node::AttachContext&) ./../../third_party/blink/renderer/core/dom/container_node.cc:1054
    #21 0x558f49850026 in ?? ??:0
    #22 0x558f497e730e in blink::Element::AttachLayoutTree(blink::Node::AttachContext&) ./../../third_party/blink/renderer/core/dom/element.cc:2767
    #23 0x558f497e730e in ?? ??:0
    #24 0x558f4978c750 in blink::Node::ReattachLayoutTree(blink::Node::AttachContext&) ./../../third_party/blink/renderer/core/dom/node.cc:1580
    #25 0x558f4978c750 in ?? ??:0
    #26 0x558f497f621f in blink::Element::RebuildLayoutTree(blink::WhitespaceAttacher&) ./../../third_party/blink/renderer/core/dom/element.cc:3365
    #27 0x558f497f621f in ?? ??:0
    #28 0x558f4989ff94 in blink::StyleEngine::RebuildLayoutTree() ./../../third_party/blink/renderer/core/css/style_engine.cc:2246
    #29 0x558f4989ff94 in ?? ??:0
    #30 0x558f498a15f0 in blink::StyleEngine::UpdateStyleAndLayoutTree() ./../../third_party/blink/renderer/core/css/style_engine.cc:2287
    #31 0x558f498a15f0 in ?? ??:0
    #32 0x558f49633a7b in blink::Document::UpdateStyle() ./../../third_party/blink/renderer/core/dom/document.cc:2174
    #33 0x558f49633a7b in ?? ??:0
    #34 0x558f496322b9 in blink::Document::UpdateStyleAndLayoutTreeForThisDocument() ./../../third_party/blink/renderer/core/dom/document.cc:2121
    #35 0x558f496322b9 in ?? ??:0
    #36 0x558f49e6b12f in blink::LocalFrameView::UpdateStyleAndLayoutInternal() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3369
    #37 0x558f49e6b12f in ?? ??:0
    #38 0x558f49e4ff7b in blink::LocalFrameView::UpdateStyleAndLayout() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3323
    #39 0x558f49e4ff7b in ?? ??:0
    #40 0x558f49e5e65e in blink::LocalFrameView::UpdateStyleAndLayoutIfNeededRecursive() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:3243
    #41 0x558f49e5e65e in ?? ??:0
    #42 0x558f49e5ac3c in blink::LocalFrameView::RunStyleAndLayoutLifecyclePhases(blink::DocumentLifecycle::LifecycleState) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2598
    #43 0x558f49e5ac3c in ?? ??:0
    #44 0x558f49e59a6e in blink::LocalFrameView::UpdateLifecyclePhasesInternal(blink::DocumentLifecycle::LifecycleState) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2450
    #45 0x558f49e59a6e in ?? ??:0
    #46 0x558f49e57453 in blink::LocalFrameView::UpdateLifecyclePhases(blink::DocumentLifecycle::LifecycleState, blink::DocumentUpdateReason) ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:2391
    #47 0x558f49e57453 in ?? ??:0
    #48 0x558f4db274e3 in blink::WebAXObject::MaybeUpdateLayoutAndCheckValidity(blink::WebDocument const&) ./../../third_party/blink/renderer/modules/exported/web_ax_object.cc:1399
    #49 0x558f4db274e3 in ?? ??:0
    #50 0x558f4db36617 in blink::WebAXObject::FromWebDocument(blink::WebDocument const&) ./../../third_party/blink/renderer/modules/exported/web_ax_object.cc:1345
    #51 0x558f4db36617 in ?? ??:0
    #52 0x558f4e0bb9f8 in content::BlinkAXTreeSource::ComputeRoot() const ./../../content/renderer/accessibility/blink_ax_tree_source.cc:869
    #53 0x558f4e0bb9f8 in ?? ??:0
    #54 0x558f4e0bf7b5 in content::BlinkAXTreeSource::GetRoot() const ./../../content/renderer/accessibility/blink_ax_tree_source.cc:393
    #55 0x558f4e0bf7b5 in ?? ??:0
    #56 0x558f4e0a5300 in content::RenderAccessibilityImpl::GenerateAXID() ./../../content/renderer/accessibility/render_accessibility_impl.cc:733
    #57 0x558f4e0a5300 in ?? ??:0
    #58 0x558f517e52e6 in pdf::PdfAccessibilityTree::SetAccessibilityViewportInfo(chrome_pdf::AccessibilityViewportInfo const&) ./../../components/pdf/renderer/pdf_accessibility_tree.cc:1512
    #59 0x558f517e52e6 in SetAccessibilityViewportInfo ./../../components/pdf/renderer/pdf_accessibility_tree.cc:1308
    #60 0x558f517e52e6 in ?? ??:0
    #61 0x558f517e089e in Invoke<void (chrome_pdf::PdfViewWebPlugin::*)(const chrome_pdf::AccessibilityViewportInfo &), base::WeakPtr<chrome_pdf::PdfViewWebPlugin>, chrome_pdf::AccessibilityViewportInfo> ./../../base/bind_internal.h:509
    #62 0x558f517e089e in MakeItSo<void (chrome_pdf::PdfViewWebPlugin::*)(const chrome_pdf::AccessibilityViewportInfo &), base::WeakPtr<chrome_pdf::PdfViewWebPlugin>, chrome_pdf::AccessibilityViewportInfo> ./../../base/bind_internal.h:668
    #63 0x558f517e089e in RunImpl<void (chrome_pdf::PdfViewWebPlugin::*)(const chrome_pdf::AccessibilityViewportInfo &), std::__1::tuple<base::WeakPtr<chrome_pdf::PdfViewWebPlugin>, chrome_pdf::AccessibilityViewportInfo>, 0UL, 1UL> ./../../base/bind_internal.h:721
    #64 0x558f517e089e in RunOnce ./../../base/bind_internal.h:690
    #65 0x558f517e089e in ?? ??:0
    #66 0x558f3d4ae5f3 in Run ./../../base/callback.h:99
    #67 0x558f3d4ae5f3 in RunTask ./../../base/task/common/task_annotator.cc:178
    #68 0x558f3d4ae5f3 in ?? ??:0

previously allocated by thread T0 (chrome) here:
    #0 0x558f2f47f76d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95
    #1 0x558f2f47f76d in ?? ??:0
    #2 0x558f517e38fd in pdf::PdfViewWebPluginClient::CreateAccessibilityDataHandler(chrome_pdf::PdfAccessibilityActionHandler*) ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725
    #3 0x558f517e38fd in CreateAccessibilityDataHandler ./../../components/pdf/renderer/pdf_view_web_plugin_client.cc:42
    #4 0x558f517e38fd in ?? ??:0
    #5 0x558f517d2bc4 in chrome_pdf::PdfViewWebPlugin::PdfViewWebPlugin(std::__1::unique_ptr<chrome_pdf::PdfViewWebPlugin::Client, std::__1::default_delete<chrome_pdf::PdfViewWebPlugin::Client> >, mojo::AssociatedRemote<pdf::mojom::PdfService>, blink::WebPluginParams const&) ./../../pdf/pdf_view_web_plugin.cc:252
    #6 0x558f517d2bc4 in ?? ??:0
    #7 0x558f517d19c0 in pdf::CreateInternalPlugin(content::WebPluginInfo const&, blink::WebPluginParams, content::RenderFrame*, std::__1::unique_ptr<pdf::PdfInternalPluginDelegate, std::__1::default_delete<pdf::PdfInternalPluginDelegate> >) ./../../components/pdf/renderer/internal_plugin_renderer_helpers.cc:55
    #8 0x558f517d19c0 in ?? ??:0
    #9 0x558f4de77a16 in ChromeContentRendererClient::CreatePlugin(content::RenderFrame*, blink::WebPluginParams const&, chrome::mojom::PluginInfo const&) ./../../chrome/renderer/chrome_content_renderer_client.cc:1081
    #10 0x558f4de77a16 in ?? ??:0
    #11 0x558f4de74473 in ChromeContentRendererClient::OverrideCreatePlugin(content::RenderFrame*, blink::WebPluginParams const&, blink::WebPlugin**) ./../../chrome/renderer/chrome_content_renderer_client.cc:824
    #12 0x558f4de74473 in ?? ??:0
    #13 0x558f4e03aaac in content::RenderFrameImpl::CreatePlugin(blink::WebPluginParams const&) ./../../content/renderer/render_frame_impl.cc:3301
    #14 0x558f4e03aaac in ?? ??:0
    #15 0x558f4a6e18f0 in blink::LocalFrameClientImpl::CreatePlugin(blink::HTMLPlugInElement&, blink::KURL const&, WTF::Vector<WTF::String, 0u, WTF::PartitionAllocator> const&, WTF::Vector<WTF::String, 0u, WTF::PartitionAllocator> const&, WTF::String const&, bool) ./../../third_party/blink/renderer/core/frame/local_frame_client_impl.cc:870
    #16 0x558f4a6e18f0 in ?? ??:0
    #17 0x558f4aa18c08 in blink::HTMLPlugInElement::LoadPlugin(blink::KURL const&, WTF::String const&, blink::PluginParameters const&, bool) ./../../third_party/blink/renderer/core/html/html_plugin_element.cc:679
    #18 0x558f4aa18c08 in ?? ??:0
    #19 0x558f4aa1721a in blink::HTMLPlugInElement::RequestObject(blink::PluginParameters const&) ./../../third_party/blink/renderer/core/html/html_plugin_element.cc:649
    #20 0x558f4aa1721a in ?? ??:0
    #21 0x558f4a9b8a80 in blink::HTMLEmbedElement::UpdatePluginInternal() ./../../third_party/blink/renderer/core/html/html_embed_element.cc:178
    #22 0x558f4a9b8a80 in ?? ??:0
    #23 0x558f4aa13cfd in blink::HTMLPlugInElement::UpdatePlugin() ./../../third_party/blink/renderer/core/html/html_plugin_element.cc:262
    #24 0x558f4aa13cfd in ?? ??:0
    #25 0x558f49e54490 in blink::LocalFrameView::UpdatePlugins() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:1889
    #26 0x558f49e54490 in ?? ??:0
    #27 0x558f49e547ac in blink::LocalFrameView::FlushAnyPendingPostLayoutTasks() ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:1904
    #28 0x558f49e547ac in FlushAnyPendingPostLayoutTasks ./../../third_party/blink/renderer/core/frame/local_frame_view.cc:1913
    #29 0x558f49e547ac in ?? ??:0
    #30 0x558f4aa15e61 in blink::HTMLPlugInElement::LayoutEmbeddedContentForJSBindings() const ./../../third_party/blink/renderer/core/html/html_plugin_element.cc:489
    #31 0x558f4aa15e61 in ?? ??:0
    #32 0x558f4aa152e3 in blink::HTMLPlugInElement::PluginWrapper() ./../../third_party/blink/renderer/core/html/html_plugin_element.cc:412
    #33 0x558f4aa152e3 in PluginWrapper ./../../third_party/blink/renderer/core/html/html_plugin_element.cc:390
    #34 0x558f4aa152e3 in ?? ??:0
    #35 0x558f4d35febb in blink::V8HTMLEmbedElement::NamedPropertyGetterCustom(WTF::AtomicString const&, v8::PropertyCallbackInfo<v8::Value> const&) ./../../third_party/blink/renderer/bindings/core/v8/custom/v8_html_plugin_element_custom.cc:64
    #36 0x558f4d35febb in NamedPropertyGetterCustom ./../../third_party/blink/renderer/bindings/core/v8/custom/v8_html_plugin_element_custom.cc:135
    #37 0x558f4d35febb in ?? ??:0
    #38 0x558f4d359eb4 in blink::V8HTMLEmbedElement::NamedPropertyGetterCallback(v8::Local<v8::Name>, v8::PropertyCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_html_embed_element.cc:84
    #39 0x558f4d359eb4 in ?? ??:0
    #40 0x558f382391be in v8::internal::PropertyCallbackArguments::CallNamedGetter(v8::internal::Handle<v8::internal::InterceptorInfo>, v8::internal::Handle<v8::internal::Name>) ./../../v8/src/api/api-arguments-inl.h:204
    #41 0x558f382391be in CallNamedGetter ./../../v8/src/api/api-arguments-inl.h:181
    #42 0x558f382391be in ?? ??:0
    #43 0x558f386e4eb2 in v8::internal::(anonymous namespace)::GetPropertyWithInterceptorInternal(v8::internal::LookupIterator*, v8::internal::Handle<v8::internal::InterceptorInfo>, bool*) ./../../v8/src/objects/js-objects.cc:1121
    #44 0x558f386e4eb2 in ?? ??:0
    #45 0x558f387cb1d1 in v8::internal::Object::GetProperty(v8::internal::LookupIterator*, bool) ./../../v8/src/objects/objects.cc:1159
    #46 0x558f387cb1d1 in ?? ??:0
    #47 0x558f381f3775 in v8::internal::LoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>, bool, v8::internal::Handle<v8::internal::Object>) ./../../v8/src/ic/ic.cc:497
    #48 0x558f381f3775 in ?? ??:0
    #49 0x558f38214f52 in v8::internal::Runtime_LoadNoFeedbackIC_Miss(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/ic/ic.cc:2555
    #50 0x558f38214f52 in Runtime_LoadNoFeedbackIC_Miss ./../../v8/src/ic/ic.cc:2540
    #51 0x558f38214f52 in ?? ??:0
    #52 0x558f39ed79f7 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit setup-isolate-deserialize.cc:?
    #53 0x558f39ed79f7 in ?? ??:0
    #54 0x558f39f6566a in Builtins_LdaNamedPropertyHandler setup-isolate-deserialize.cc:?
    #55 0x558f39f6566a in ?? ??:0
    #56 0x558f39e63460 in Builtins_InterpreterEntryTrampoline setup-isolate-deserialize.cc:?
    #57 0x558f39e63460 in ?? ??:0
    #58 0x558f39e97591 in Builtins_GeneratorPrototypeNext setup-isolate-deserialize.cc:?
    #59 0x558f39e97591 in ?? ??:0
    #60 0x558f39e6145b in Builtins_JSEntryTrampoline setup-isolate-deserialize.cc:?
    #61 0x558f39e6145b in ?? ??:0
    #62 0x558f39e61186 in Builtins_JSEntry setup-isolate-deserialize.cc:?
    #63 0x558f39e61186 in ?? ??:0
    #64 0x558f37e7053b in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&) ./../../v8/src/execution/simulator.h:152
    #65 0x558f37e7053b in Invoke ./../../v8/src/execution/execution.cc:383
    #66 0x558f37e7053b in ?? ??:0

SUMMARY: AddressSanitizer: heap-use-after-free (/home/test/asan-linux-release/chrome+0x2ca837a0)
Shadow bytes around the buggy address:
  0x0c3280003670: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3280003680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c3280003690: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800036a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800036b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x0c32800036c0: fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd
  0x0c32800036d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800036e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c32800036f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3280003700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c3280003710: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==1==ABORTING

Did this work before? N/A 

Chrome version: 96.0.4655.0  Channel: n/a
OS Version: 20.04

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 160 B)
- [test.pdf](attachments/test.pdf) (application/pdf, 176 B)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 4.2 MB)

## Timeline

### [Deleted User] (2021-10-02)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-10-02)

thestig: Could you take a look at this?

I'm still working on the repro, but the source analysis seems to support that we have a situation where the following call results in a free of `this`, thus leading to the UAF:

https://source.chromium.org/chromium/chromium/src/+/main:components/pdf/renderer/pdf_accessibility_tree.cc;l=1308-1309;drc=9f667c3873e085c1b822d74e94898165ead512d0

Namely, the call GenerateAXID in https://source.chromium.org/chromium/chromium/src/+/main:components/pdf/renderer/pdf_accessibility_tree.cc;l=1512;drc=63880c90b90f8fd41191afd0c43f50b4f9a39734 causes a relayout, resulting in the current PdfViewWebPlugin being destroyed, which invalidates the current accessibility tree. When we then use the results of that, it's a UAF.

I'll work on further triaging this Monday on affected platform and OSes, but this appears legit.

One thing is the existence of " --force-renderer-accessibility" /may/ mitigate this a severity level if this is a non-standard flag here. I was hoping you may know more on this context, otherwise, I may need to talk to some of the accessibility folks to get a sense on whether this is non-standard, or if this simply makes the repro easier.

[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2021-10-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2021-10-04)

Just noting: I've been unable to reproduce the indicated stack trace.

For example, attempting with the version specified, I trigger stack traces on RenderAccessibilityManager::FatalError ( https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/accessibility/render_accessibility_manager.cc;l=71;drc=021686d6b49506d4e5c51cb6b9c7cb61b8e4b6ec ) due to an invalid Mojo message

I've tried with this exact release indicated in https://crbug.com/chromium/1255332#c0, but still to no avail. That said, the backtrace itself looks legitimate, which is why I'm curious to keep looking. That's both with dismissing the print dialog and refreshing, or refreshing while the print dialog is still open, as well as refreshing while the dialog is still loading.

### em...@gmail.com (2021-10-05)

I sometimes get 'RenderAccessibilityManager::FatalErro' too.
I uploaded a simple reproduction video, hope it helps.

tested version:
Version 96.0.4661.0 (Developer Build) (64-bit) gsutil cp gs://chromium-browser-asan/linux-release/asan-linux-release-928008.zip .


### th...@chromium.org (2021-10-05)

I tried a build with DCHECKs turned on, and got a DCHECK() failure at the start of RenderFrameImpl::Unload(). Commenting that out, I get the next one in RenderFrameImpl::SwapOutAndDeleteThis(). Getting past these 2, the page will load and open Print Preview.

Pressing reload triggers the Paused() DCHECK() in DocumentLoader::BodyDataReceived(). Next NOTREACHED() failure is LocalFrameView::updateLifecyclePhasesInternal() reentrance. in LocalFrameView::UpdateLifecyclePhases().

After getting past all those, I got RenderAccessibilityManager::FatalError() every time. The way to avoid this and to trigger the ASAN UAF is to muck with RenderFrameHostImpl::AccessibilityFatalError() and just call AccessibilityReset() rather than going through the FatalError() path. So now I think I have a reliable repro. I'll try to take a look.

+nektar@ from the a11y side FYI.

[Monorail components: UI>Accessibility]

### th...@chromium.org (2021-10-05)

For some of the DCHECK(), https://crbug.com/chromium/773177 and https://crbug.com/chromium/1251760 are related. So I won't file new bugs.

### th...@chromium.org (2021-10-05)

https://chromium-review.googlesource.com/3206106

### th...@chromium.org (2021-10-06)

[Empty comment from Monorail migration]

### th...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/994ecbfe6e5448e2ed8d41002d7508bb09f606f1

commit 994ecbfe6e5448e2ed8d41002d7508bb09f606f1
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Oct 07 19:32:19 2021

Observe for self deletions in PdfAccessibilityTree.

PdfAccessibilityTree::GetRenderAccessibilityIfEnabled() can cause itself
to get deleted. Watch out for this case and return nullptr, which in
turn causes callers to abort whatever they are doing.

Bug: 1255332
Change-Id: I34321bf9a9809f1795e6c6049832e7915f9677b2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3206106
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Ryan Sleevi <rsleevi@chromium.org>
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Cr-Commit-Position: refs/heads/main@{#929343}

[modify] https://crrev.com/994ecbfe6e5448e2ed8d41002d7508bb09f606f1/components/pdf/renderer/pdf_accessibility_tree.h
[modify] https://crrev.com/994ecbfe6e5448e2ed8d41002d7508bb09f606f1/components/pdf/renderer/pdf_accessibility_tree.cc


### th...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-07)

[Empty comment from Monorail migration]

### th...@chromium.org (2021-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-09)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-09)

Requesting merge to beta M95 because latest trunk commit (929343) appears to be after beta branch point (920003).

Not requesting merge to dev (M96) because latest trunk commit (929343) appears to be prior to dev branch point (929512). If this is incorrect, please replace the Merge-NA-96 label with Merge-Request-96. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-09)

Merge review required: M95 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2021-10-11)

+amyressler@: Would you be able to help flip the bits? ^

### am...@chromium.org (2021-10-11)

absolutely, merge approved for M95, please go ahead and merge to branch 4638 as soon as possible as M95 stable cut is tomorrow. thanks! 

### gi...@appspot.gserviceaccount.com (2021-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7dce7b3a15b2fa14be933f2a0b8eb93192a1e0b9

commit 7dce7b3a15b2fa14be933f2a0b8eb93192a1e0b9
Author: Lei Zhang <thestig@chromium.org>
Date: Mon Oct 11 20:36:49 2021

M95: Observe for self deletions in PdfAccessibilityTree.

PdfAccessibilityTree::GetRenderAccessibilityIfEnabled() can cause itself
to get deleted. Watch out for this case and return nullptr, which in
turn causes callers to abort whatever they are doing.

(cherry picked from commit 994ecbfe6e5448e2ed8d41002d7508bb09f606f1)

Bug: 1255332
Change-Id: I34321bf9a9809f1795e6c6049832e7915f9677b2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3206106
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Ryan Sleevi <rsleevi@chromium.org>
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#929343}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3218032
Commit-Queue: Ryan Sleevi <rsleevi@chromium.org>
Auto-Submit: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/branch-heads/4638@{#760}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[modify] https://crrev.com/7dce7b3a15b2fa14be933f2a0b8eb93192a1e0b9/components/pdf/renderer/pdf_accessibility_tree.h
[modify] https://crrev.com/7dce7b3a15b2fa14be933f2a0b8eb93192a1e0b9/components/pdf/renderer/pdf_accessibility_tree.cc


### th...@chromium.org (2021-10-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### gi...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/39de6aab386fe810077cd2e2baea74d7058229fb

commit 39de6aab386fe810077cd2e2baea74d7058229fb
Author: Lei Zhang <thestig@chromium.org>
Date: Tue Oct 26 13:04:15 2021

[M90-LTS] Observe for self deletions in PdfAccessibilityTree.

PdfAccessibilityTree::GetRenderAccessibilityIfEnabled() can cause itself
to get deleted. Watch out for this case and return nullptr, which in
turn causes callers to abort whatever they are doing.

M90 merge issues:
  Conflicting includes and
  GetRenderAccessibilityIfEnabled not in M90

(cherry picked from commit 994ecbfe6e5448e2ed8d41002d7508bb09f606f1)

Bug: 1255332
Change-Id: I34321bf9a9809f1795e6c6049832e7915f9677b2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3206106
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#929343}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3234532
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1644}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/39de6aab386fe810077cd2e2baea74d7058229fb/components/pdf/renderer/pdf_accessibility_tree.h
[modify] https://crrev.com/39de6aab386fe810077cd2e2baea74d7058229fb/components/pdf/renderer/pdf_accessibility_tree.cc


### rz...@google.com (2021-10-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-28)

Congratulations Cassidy Kim! The VRP Panel has decided to award you $5000 for this report. Nice work and thank you for your efforts! 

### am...@google.com (2021-10-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-05)

Hello OP/emilykim@, we consider attachments/pocs included with reports to be an integral part of the report (https://bughunters.google.com/about/rules/5745167867576320), so I've undeleted them. Thank you! 

### [Deleted User] (2022-01-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2022-10-06)

Crash no longer being reported, presumed fixed.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1255332?no_tracker_redirect=1

[Multiple monorail components: Internals>Plugins>PDF, UI>Accessibility]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057482)*
