# UAF in content::protocol::InputHandler::InputInjector::InjectMouseEvent through DevTools

| Field | Value |
|-------|-------|
| **Issue ID** | [430635213](https://issues.chromium.org/issues/430635213) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Android |
| **Reporter** | xu...@gmail.com |
| **Assignee** | pf...@google.com |
| **Created** | 2025-07-10 |
| **Bounty** | $1,000.00 |

## Description

# VULNERABILITY DETAILS

This vulnerability occurs in the Chrome DevTools protocol input handling mechanism, specifically within the InputInjector class that manages mouse event injection for automation and debugging purposes.

The vulnerability stems from a race condition in the asynchronous callback mechanism between mouse event processing and the InputInjector object's lifecycle management:

1.Open pages within the DevTools interface will create the InputInjector object.

2.Plug/unplug the USB cable will trigger the disconnection and reconnection of devtools, which calls the destruction fuction of InputInjector object

3.However, the InjectMouseEvent function may still hold references to the object's member variables or attempt to access the InputInjector object after the asynchronous callback has already destroyed it, which causes use-after-free vulnerability and a crash in the browser process.

We have identified this issue in Chrome Android, however, other platform implementations of DevTools may also be affected by this problem.

# VERSION

Chrome Version: [140.0.7283.0] + [canary]

Operating System: [Android]

# REPRODUCTION CASE

1. Connect to ADB
2. open DevTools
3. randomly access(click/drag) pages
4. plug/unplug the USB cable, and click the mouse multiple times in pages opened within the DevTools interface to trigger the issue.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [browser]

# Crash State

```
07-09 23:43:51.333  1181  1181 I app_process64: ==1181==ERROR: HWAddressSanitizer: tag-mismatch on address 0x0039862dbca0 at pc 0x006caee73e54
07-09 23:43:51.334  1181  1181 I app_process64: READ of size 1 at 0x0039862dbca0 tags: cd/10 (ptr/mem) in thread T0
07-09 23:43:51.364  1181  1181 I app_process64:     #0 0x6caee73e54  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6873e54) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::InputInjector::InjectMouseEvent(blink::WebMouseEvent const&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >) at ./../../content/browser/devtools/protocol/input_handler.cc:695
07-09 23:43:51.364  1181  1181 I app_process64:     #1 0x6caee6d598  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x686d598) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::OnWidgetForDispatchMouseEvent(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>) at ./../../content/browser/devtools/protocol/input_handler.cc:1576 (discriminator 6)
07-09 23:43:51.364  1181  1181 I app_process64:     #2 0x6caee82c34  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6882c34) (BuildId: f70b4ed1a4f72e94) -> void base::internal::DecayedFunctorTraits<void (content::protocol::InputHandler::*)(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>), base::WeakPtr<content::protocol::InputHandler>&&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >&&, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >&&>::Invoke<void (content::protocol::InputHandler::*)(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>), base::WeakPtr<content::protocol::InputHandler> const&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF> >(void (content::protocol::InputHandler::*)(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>), base::WeakPtr<content::protocol::InputHandler> const&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >&&, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >&&, base::WeakPtr<content::RenderWidgetHostViewBase>&&, std::__Cr::optional<gfx::PointF>&&) at ./../../base/functional/bind_internal.h:731 (discriminator 12)
07-09 23:43:51.364  1181  1181 I app_process64:     #3 0x6cafbd2310  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x75d2310) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>::Run(base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.364  1181  1181 I app_process64:     #4 0x6cafc184a4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x76184a4) (BuildId: f70b4ed1a4f72e94) -> void base::internal::DecayedFunctorTraits<void (*)(base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>), base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>&&>::Invoke<void (*)(base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>), base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF> >(void (*&&)(base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>), base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>&&, base::WeakPtr<input::RenderWidgetHostViewInput>&&, std::__Cr::optional<gfx::PointF>&&) at ./../../base/functional/bind_internal.h:664 (discriminator 4)
07-09 23:43:51.364  1181  1181 I app_process64:     #5 0x6cb7653ac0  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf053ac0) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>)>::Run(base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.364  1181  1181 I app_process64:     #6 0x6cb7655674  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf055674) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetTargeter::FoundTarget(input::RenderWidgetHostViewInput*, std::__Cr::optional<gfx::PointF> const&, input::RenderWidgetTargeter::TargetingRequest*) at ./../../components/input/render_widget_targeter.cc:401
07-09 23:43:51.364  1181  1181 I app_process64:     #7 0x6cb765463c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf05463c) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetTargeter::ResolveTargetingRequest(input::RenderWidgetTargeter::TargetingRequest) at ./../../components/input/render_widget_targeter.cc:231
07-09 23:43:51.364  1181  1181 I app_process64:     #8 0x6cb765494c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf05494c) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetTargeter::FindTargetAndCallback(input::RenderWidgetHostViewInput*, gfx::PointF const&, base::OnceCallback<void (base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>)>) at ./../../components/input/render_widget_targeter.cc:179 (discriminator 2)
07-09 23:43:51.364  1181  1181 I app_process64:     #9 0x6cb7646410  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf046410) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetHostInputEventRouter::GetRenderWidgetHostAtPointAsynchronously(input::RenderWidgetHostViewInput*, gfx::PointF const&, base::OnceCallback<void (base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>)>) at ./../../components/input/render_widget_host_input_event_router.cc:1582 (discriminator 4)
07-09 23:43:51.365  1181  1181 I app_process64:     #10 0x6cafbd2500  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x75d2500) (BuildId: f70b4ed1a4f72e94) -> content::WebContentsImpl::GetRenderWidgetHostAtPointAsynchronously(content::RenderWidgetHostViewBase*, gfx::PointF const&, base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>) at ./../../content/browser/web_contents/web_contents_impl.cc:4471 (discriminator 2)
07-09 23:43:51.365  1181  1181 I app_process64:     #11 0x6caee82920  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6882920) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::HandleMouseEvent(std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >)::$_0::operator()(base::WeakPtr<content::protocol::InputHandler>, base::WeakPtr<content::RenderWidgetHostImpl>, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, bool) const at ./../../content/browser/devtools/protocol/input_handler.cc:1345
07-09 23:43:51.365  1181  1181 I app_process64:     #12 0x6caee6cd7c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x686cd7c) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (bool)>::Run(bool) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.365  1181  1181 I app_process64:     #13 0x6caee70bd4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6870bd4) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::DispatchMouseEvent(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, double, double, std::__Cr::optional<int>, std::__Cr::optional<double>, std::__Cr::optional<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >, std::__Cr::optional<int>, std::__Cr::optional<int>, std::__Cr::optional<double>, std::__Cr::optional<double>, std::__Cr::optional<double>, std::__Cr::optional<double>, std::__Cr::optional<int>, std::__Cr::optional<double>, std::__Cr::optional<double>, std::__Cr::optional<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >) at ./../../content/browser/devtools/protocol/input_handler.cc:1318 (discriminator 6)
07-09 23:43:51.365  1181  1181 I app_process64:     #14 0x6cae9b73b4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x63b73b4) (BuildId: f70b4ed1a4f72e94) -> content::protocol::Input::DomainDispatcherImpl::dispatchMouseEvent(crdtp::Dispatchable const&) at ./gen/content/browser/devtools/protocol/input.cc:607 (discriminator 14)
07-09 23:43:51.365  1181  1181 I app_process64:     #15 0x6cb7f697c4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf9697c4) (BuildId: f70b4ed1a4f72e94) -> std::__Cr::__function::__policy_func<void ()>::operator()() const at ./../../third_party/libc++/src/include/__functional/function.h:722
07-09 23:43:51.365  1181  1181 I app_process64:     #16 0x6caee08270  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6808270) (BuildId: f70b4ed1a4f72e94) -> content::DevToolsSession::HandleCommandInternal(crdtp::Dispatchable, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) at ./../../content/browser/devtools/devtools_session.cc:381
07-09 23:43:51.365  1181  1181 I app_process64:     #17 0x6caee080c4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x68080c4) (BuildId: f70b4ed1a4f72e94) -> content::DevToolsSession::HandleCommand(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) at ./../../content/browser/devtools/devtools_session.cc:367 (discriminator 4)
07-09 23:43:51.365  1181  1181 I app_process64:     #18 0x6cb958be80  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x10f8be80) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>)>::Run(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.365  1181  1181 I app_process64:     #19 0x6cb430b19c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xbd0b19c) (BuildId: f70b4ed1a4f72e94) -> DevToolsManagerDelegateAndroid::HandleCommand(content::DevToolsAgentHostClientChannel*, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>, base::OnceCallback<void (base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>)>) at ./../../chrome/browser/android/devtools_manager_delegate_android.cc:293 (discriminator 6)
07-09 23:43:51.365  1181  1181 I app_process64:     #20 0x6caee07f40  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6807f40) (BuildId: f70b4ed1a4f72e94) -> content::DevToolsSession::DispatchProtocolMessageInternal(crdtp::Dispatchable, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) at ./../../content/browser/devtools/devtools_session.cc:358
07-09 23:43:51.365  1181  1181 I app_process64:     #21 0x6caee076f0  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x68076f0) (BuildId: f70b4ed1a4f72e94) -> content::DevToolsSession::DispatchProtocolMessage(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) at ./../../content/browser/devtools/devtools_session.cc:336
07-09 23:43:51.365  1181  1181 I app_process64:     #22 0x6caee07268  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6807268) (BuildId: f70b4ed1a4f72e94) -> content::DevToolsSession::DispatchProtocolMessage(base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) at ./../../content/browser/devtools/devtools_session.cc:273 (discriminator 2)
07-09 23:43:51.365  1181  1181 I app_process64:     #23 0x6caeddff24  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x67dff24) (BuildId: f70b4ed1a4f72e94) -> void base::internal::DecayedFunctorTraits<void (content::DevToolsHttpHandler::*)(int, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >), base::WeakPtr<content::DevToolsHttpHandler>&&, int&&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >&&>::Invoke<void (content::DevToolsHttpHandler::*)(int, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >), base::WeakPtr<content::DevToolsHttpHandler> const&, int, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >(void (content::DevToolsHttpHandler::*)(int, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >), base::WeakPtr<content::DevToolsHttpHandler> const&, int&&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >&&) at ./../../base/functional/bind_internal.h:731 (discriminator 8)
07-09 23:43:51.365  1181  1181 I app_process64:     #24 0x6cb386565c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xb26565c) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void ()>::Run() && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.365  1181  1181 I app_process64:     #25 0x6cb38a02b4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xb2a02b4) (BuildId: f70b4ed1a4f72e94) -> void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&) at ./../../base/task/common/task_annotator.h:104
07-09 23:43:51.365  1181  1181 I app_process64:     #26 0x6cb389f8cc  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xb29f8cc) (BuildId: f70b4ed1a4f72e94) -> base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() at ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:330
07-09 23:43:51.365  1181  1181 I app_process64:     #27 0x6cb393490c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xb33490c) (BuildId: f70b4ed1a4f72e94) -> base::MessagePumpAndroid::DoNonDelayedLooperWork(bool) at ./../../base/message_loop/message_pump_android.cc:458 (discriminator 2)
07-09 23:43:51.365  1181  1181 I app_process64:     #28 0x6cb39347e8  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xb3347e8) (BuildId: f70b4ed1a4f72e94) -> base::MessagePumpAndroid::OnNonDelayedLooperCallback() at ./../../base/message_loop/message_pump_android.cc:443
07-09 23:43:51.365  1181  1181 I app_process64:     #29 0x6cb3934184  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xb334184) (BuildId: f70b4ed1a4f72e94) -> base::(anonymous namespace)::NonDelayedLooperCallback(int, int, void*) at ./../../base/message_loop/message_pump_android.cc:67
07-09 23:43:51.365  1181  1181 I app_process64:     #30 0x76f8c67608  (/system/lib64/libutils.so+0x14608) (BuildId: 48b3487cb5d47b9b2933b384c748a420)
07-09 23:43:51.365  1181  1181 I app_process64:     #31 0x76f371a058  (/system/lib64/libandroid_runtime.so+0x296058) (BuildId: b0323c59b626c024b60bf427ae199f09)
07-09 23:43:51.365  1181  1181 I app_process64:
07-09 23:43:51.365  1181  1181 I app_process64: [0x0039862dbc80,0x0039862dbd00) is a small unallocated heap chunk; size: 128 offset: 32
07-09 23:43:51.365  1181  1181 I app_process64:
07-09 23:43:51.365  1181  1181 I app_process64: Cause: use-after-free
07-09 23:43:51.365  1181  1181 I app_process64: 0x0039862dbca0 is located 32 bytes inside a 120-byte region [0x0039862dbc80,0x0039862dbcf8)
07-09 23:43:51.365  1181  1181 I app_process64: freed by thread T0 here:
07-09 23:43:51.366  1181  1181 I app_process64:     #0 0x76ddcdc27c  (/apex/com.android.runtime/lib64/bionic/libclang_rt.hwasan-aarch64-android.so+0x2927c) (BuildId: c4d7dd325a00ab29431622590de702c37735af2f)
07-09 23:43:51.366  1181  1181 I app_process64:     #1 0x6caee82328  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6882328) (BuildId: f70b4ed1a4f72e94) -> std::__Cr::default_delete<content::protocol::InputHandler::InputInjector>::operator()(content::protocol::InputHandler::InputInjector*) const at ./../../third_party/libc++/src/include/__memory/unique_ptr.h:77 (discriminator 2)
07-09 23:43:51.366  1181  1181 I app_process64:     #2 0x6caee8b2c8  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x688b2c8) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::InputInjector::OnInputEventAck(content::RenderWidgetHost const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState, blink::WebInputEvent const&) at ./../../content/browser/devtools/protocol/input_handler.cc:794
07-09 23:43:51.366  1181  1181 I app_process64:     #3 0x6caf8a0da8  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x72a0da8) (BuildId: f70b4ed1a4f72e94) -> content::RenderWidgetHostImpl::NotifyObserversOfInputEventAcks(blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState, blink::WebInputEvent const&) at ./../../content/browser/renderer_host/render_widget_host_impl.cc:2668
07-09 23:43:51.366  1181  1181 I app_process64:     #4 0x6caf89ed10  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x729ed10) (BuildId: f70b4ed1a4f72e94) -> content::RenderWidgetHostImpl::OnMouseEventAck(input::EventWithLatencyInfo<blink::WebMouseEvent> const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState) at ./../../content/browser/renderer_host/render_widget_host_impl.cc:2375
07-09 23:43:51.366  1181  1181 I app_process64:     #5 0x6cb7622b28  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf022b28) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (input::EventWithLatencyInfo<blink::WebMouseEvent> const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState)>::Run(input::EventWithLatencyInfo<blink::WebMouseEvent> const&, blink::mojom::InputEventResultSource, blink::mojom::InputEventResultState) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.366  1181  1181 I app_process64:     #6 0x6caf89629c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x729629c) (BuildId: f70b4ed1a4f72e94) -> content::RenderWidgetHostImpl::ForwardMouseEventWithLatencyInfo(blink::WebMouseEvent const&, ui::LatencyInfo const&) at ./../../content/browser/renderer_host/render_widget_host_impl.cc:1608 (discriminator 2)
07-09 23:43:51.366  1181  1181 I app_process64:     #7 0x6caf895cc4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x7295cc4) (BuildId: f70b4ed1a4f72e94) -> content::RenderWidgetHostImpl::ForwardMouseEvent(blink::WebMouseEvent const&) at ./../../content/browser/renderer_host/render_widget_host_impl.cc:1565 (discriminator 2)
07-09 23:43:51.366  1181  1181 I app_process64:     #8 0x6caee73e4c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6873e4c) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::InputInjector::InjectMouseEvent(blink::WebMouseEvent const&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >) at ./../../content/browser/devtools/protocol/input_handler.cc:694 (discriminator 2)
07-09 23:43:51.366  1181  1181 I app_process64:     #9 0x6caee6d598  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x686d598) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::OnWidgetForDispatchMouseEvent(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>) at ./../../content/browser/devtools/protocol/input_handler.cc:1576 (discriminator 6)
07-09 23:43:51.366  1181  1181 I app_process64:     #10 0x6caee82c34  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6882c34) (BuildId: f70b4ed1a4f72e94) -> void base::internal::DecayedFunctorTraits<void (content::protocol::InputHandler::*)(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>), base::WeakPtr<content::protocol::InputHandler>&&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >&&, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >&&>::Invoke<void (content::protocol::InputHandler::*)(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>), base::WeakPtr<content::protocol::InputHandler> const&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF> >(void (content::protocol::InputHandler::*)(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>), base::WeakPtr<content::protocol::InputHandler> const&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >&&, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >&&, base::WeakPtr<content::RenderWidgetHostViewBase>&&, std::__Cr::optional<gfx::PointF>&&) at ./../../base/functional/bind_internal.h:731 (discriminator 12)
07-09 23:43:51.366  1181  1181 I app_process64:     #11 0x6cafbd2310  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x75d2310) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>::Run(base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.366  1181  1181 I app_process64:     #12 0x6cafc184a4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x76184a4) (BuildId: f70b4ed1a4f72e94) -> void base::internal::DecayedFunctorTraits<void (*)(base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>), base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>&&>::Invoke<void (*)(base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>), base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF> >(void (*&&)(base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>), base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>&&, base::WeakPtr<input::RenderWidgetHostViewInput>&&, std::__Cr::optional<gfx::PointF>&&) at ./../../base/functional/bind_internal.h:664 (discriminator 4)
07-09 23:43:51.366  1181  1181 I app_process64:     #13 0x6cb7653ac0  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf053ac0) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>)>::Run(base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.366  1181  1181 I app_process64:     #14 0x6cb7655674  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf055674) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetTargeter::FoundTarget(input::RenderWidgetHostViewInput*, std::__Cr::optional<gfx::PointF> const&, input::RenderWidgetTargeter::TargetingRequest*) at ./../../components/input/render_widget_targeter.cc:401
07-09 23:43:51.366  1181  1181 I app_process64:     #15 0x6cb765463c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf05463c) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetTargeter::ResolveTargetingRequest(input::RenderWidgetTargeter::TargetingRequest) at ./../../components/input/render_widget_targeter.cc:231
07-09 23:43:51.366  1181  1181 I app_process64:     #16 0x6cb765494c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf05494c) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetTargeter::FindTargetAndCallback(input::RenderWidgetHostViewInput*, gfx::PointF const&, base::OnceCallback<void (base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>)>) at ./../../components/input/render_widget_targeter.cc:179 (discriminator 2)
07-09 23:43:51.366  1181  1181 I app_process64:     #17 0x6cb7646410  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf046410) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetHostInputEventRouter::GetRenderWidgetHostAtPointAsynchronously(input::RenderWidgetHostViewInput*, gfx::PointF const&, base::OnceCallback<void (base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>)>) at ./../../components/input/render_widget_host_input_event_router.cc:1582 (discriminator 4)
07-09 23:43:51.366  1181  1181 I app_process64:     #18 0x6cafbd2500  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x75d2500) (BuildId: f70b4ed1a4f72e94) -> content::WebContentsImpl::GetRenderWidgetHostAtPointAsynchronously(content::RenderWidgetHostViewBase*, gfx::PointF const&, base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>) at ./../../content/browser/web_contents/web_contents_impl.cc:4471 (discriminator 2)
07-09 23:43:51.366  1181  1181 I app_process64:     #19 0x6caee82920  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6882920) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::HandleMouseEvent(std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >)::$_0::operator()(base::WeakPtr<content::protocol::InputHandler>, base::WeakPtr<content::RenderWidgetHostImpl>, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, bool) const at ./../../content/browser/devtools/protocol/input_handler.cc:1345
07-09 23:43:51.366  1181  1181 I app_process64:
07-09 23:43:51.366  1181  1181 I app_process64: previously allocated by thread T0 here:
07-09 23:43:51.367  1181  1181 I app_process64:     #0 0x76ddcdc8d8  (/apex/com.android.runtime/lib64/bionic/libclang_rt.hwasan-aarch64-android.so+0x298d8) (BuildId: c4d7dd325a00ab29431622590de702c37735af2f)
07-09 23:43:51.367  1181  1181 I app_process64:     #1 0x77160575dc  (/apex/com.android.runtime/lib64/bionic/hwasan/libc.so+0x515dc) (BuildId: 035b6fecf053f871f58e141e9c628c8a)
07-09 23:43:51.367  1181  1181 I app_process64:     #2 0x6cbe7cd6d4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x161cd6d4) (BuildId: f70b4ed1a4f72e94) -> operator_new_impl(unsigned long) at ./../../third_party/libc++/src/src/new.cpp:34 (discriminator 2)
07-09 23:43:51.367  1181  1181 I app_process64:     #3 0x6caee6f16c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x686f16c) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::EnsureInjector(content::RenderWidgetHostImpl*) at ./../../content/browser/devtools/protocol/input_handler.cc:2237
07-09 23:43:51.367  1181  1181 I app_process64:     #4 0x6caee6d51c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x686d51c) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::OnWidgetForDispatchMouseEvent(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>) at input_handler.cc:?
07-09 23:43:51.367  1181  1181 I app_process64:     #5 0x6caee82c34  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6882c34) (BuildId: f70b4ed1a4f72e94) -> void base::internal::DecayedFunctorTraits<void (content::protocol::InputHandler::*)(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>), base::WeakPtr<content::protocol::InputHandler>&&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >&&, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >&&>::Invoke<void (content::protocol::InputHandler::*)(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>), base::WeakPtr<content::protocol::InputHandler> const&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF> >(void (content::protocol::InputHandler::*)(std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>), base::WeakPtr<content::protocol::InputHandler> const&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >&&, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >&&, base::WeakPtr<content::RenderWidgetHostViewBase>&&, std::__Cr::optional<gfx::PointF>&&) at ./../../base/functional/bind_internal.h:731 (discriminator 12)
07-09 23:43:51.367  1181  1181 I app_process64:     #6 0x6cafbd2310  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x75d2310) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>::Run(base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.367  1181  1181 I app_process64:     #7 0x6cafc184a4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x76184a4) (BuildId: f70b4ed1a4f72e94) -> void base::internal::DecayedFunctorTraits<void (*)(base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>), base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>&&>::Invoke<void (*)(base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>), base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF> >(void (*&&)(base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>, base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>), base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>&&, base::WeakPtr<input::RenderWidgetHostViewInput>&&, std::__Cr::optional<gfx::PointF>&&) at ./../../base/functional/bind_internal.h:664 (discriminator 4)
07-09 23:43:51.367  1181  1181 I app_process64:     #8 0x6cb7653ac0  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf053ac0) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>)>::Run(base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.367  1181  1181 I app_process64:     #9 0x6cb7655674  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf055674) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetTargeter::FoundTarget(input::RenderWidgetHostViewInput*, std::__Cr::optional<gfx::PointF> const&, input::RenderWidgetTargeter::TargetingRequest*) at ./../../components/input/render_widget_targeter.cc:401
07-09 23:43:51.367  1181  1181 I app_process64:     #10 0x6cb765463c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf05463c) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetTargeter::ResolveTargetingRequest(input::RenderWidgetTargeter::TargetingRequest) at ./../../components/input/render_widget_targeter.cc:231
07-09 23:43:51.367  1181  1181 I app_process64:     #11 0x6cb765494c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf05494c) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetTargeter::FindTargetAndCallback(input::RenderWidgetHostViewInput*, gfx::PointF const&, base::OnceCallback<void (base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>)>) at ./../../components/input/render_widget_targeter.cc:179 (discriminator 2)
07-09 23:43:51.367  1181  1181 I app_process64:     #12 0x6cb7646410  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf046410) (BuildId: f70b4ed1a4f72e94) -> input::RenderWidgetHostInputEventRouter::GetRenderWidgetHostAtPointAsynchronously(input::RenderWidgetHostViewInput*, gfx::PointF const&, base::OnceCallback<void (base::WeakPtr<input::RenderWidgetHostViewInput>, std::__Cr::optional<gfx::PointF>)>) at ./../../components/input/render_widget_host_input_event_router.cc:1582 (discriminator 4)
07-09 23:43:51.367  1181  1181 I app_process64:     #13 0x6cafbd2500  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x75d2500) (BuildId: f70b4ed1a4f72e94) -> content::WebContentsImpl::GetRenderWidgetHostAtPointAsynchronously(content::RenderWidgetHostViewBase*, gfx::PointF const&, base::OnceCallback<void (base::WeakPtr<content::RenderWidgetHostViewBase>, std::__Cr::optional<gfx::PointF>)>) at ./../../content/browser/web_contents/web_contents_impl.cc:4471 (discriminator 2)
07-09 23:43:51.367  1181  1181 I app_process64:     #14 0x6caee82920  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6882920) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::HandleMouseEvent(std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >)::$_0::operator()(base::WeakPtr<content::protocol::InputHandler>, base::WeakPtr<content::RenderWidgetHostImpl>, std::__Cr::unique_ptr<blink::WebMouseEvent, std::__Cr::default_delete<blink::WebMouseEvent> >, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >, bool) const at ./../../content/browser/devtools/protocol/input_handler.cc:1345
07-09 23:43:51.367  1181  1181 I app_process64:     #15 0x6caee6cd7c  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x686cd7c) (BuildId: f70b4ed1a4f72e94) -> base::OnceCallback<void (bool)>::Run(bool) && at ./../../base/functional/callback.h:156 (discriminator 4)
07-09 23:43:51.367  1181  1181 I app_process64:     #16 0x6caee70bd4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6870bd4) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::DispatchMouseEvent(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, double, double, std::__Cr::optional<int>, std::__Cr::optional<double>, std::__Cr::optional<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >, std::__Cr::optional<int>, std::__Cr::optional<int>, std::__Cr::optional<double>, std::__Cr::optional<double>, std::__Cr::optional<double>, std::__Cr::optional<double>, std::__Cr::optional<int>, std::__Cr::optional<double>, std::__Cr::optional<double>, std::__Cr::optional<std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > >, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >) at ./../../content/browser/devtools/protocol/input_handler.cc:1318 (discriminator 6)
07-09 23:43:51.367  1181  1181 I app_process64:     #17 0x6cae9b73b4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x63b73b4) (BuildId: f70b4ed1a4f72e94) -> content::protocol::Input::DomainDispatcherImpl::dispatchMouseEvent(crdtp::Dispatchable const&) at ./gen/content/browser/devtools/protocol/input.cc:607 (discriminator 14)
07-09 23:43:51.367  1181  1181 I app_process64:     #18 0x6cb7f697c4  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0xf9697c4) (BuildId: f70b4ed1a4f72e94) -> std::__Cr::__function::__policy_func<void ()>::operator()() const at ./../../third_party/libc++/src/include/__functional/function.h:722
07-09 23:43:51.367  1181  1181 I app_process64:     #19 0x6caee08270  (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6808270) (BuildId: f70b4ed1a4f72e94) -> content::DevToolsSession::HandleCommandInternal(crdtp::Dispatchable, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) at ./../../content/browser/devtools/devtools_session.cc:381
07-09 23:43:51.367  1181  1181 I app_process64:
07-09 23:43:51.367  1181  1181 I app_process64: hwasan_dev_note_heap_rb_distance: 5 1023
07-09 23:43:51.367  1181  1181 I app_process64: hwasan_dev_note_num_matching_addrs: 0
07-09 23:43:51.367  1181  1181 I app_process64: hwasan_dev_note_num_matching_addrs_4b: 0
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T0 0x006d00002000 stack: [0x007fcf9ab000,0x007fd01ab000) sz: 8388608 tls: [0x00771bcfda00,0x00771bd01000)
07-09 23:43:51.367  1181  1181 I app_process64:
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T1 0x006d00006000 stack: [0x0076a639e000,0x0076a649f6c0) sz: 1054400 tls: [0x0076a649fa00,0x0076a64a3000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T2 0x006d0000a000 stack: [0x0076a52a0000,0x0076a53996c0) sz: 1021632 tls: [0x0076a5399a00,0x0076a539d000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T3 0x006d0000e000 stack: [0x0076a18ae000,0x0076a19b76c0) sz: 1087168 tls: [0x0076a19b7a00,0x0076a19bb000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T4 0x006d00012000 stack: [0x0076a17a0000,0x0076a18a96c0) sz: 1087168 tls: [0x0076a18a9a00,0x0076a18ad000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T5 0x006d00016000 stack: [0x0076a19bc000,0x0076a1ab56c0) sz: 1021632 tls: [0x0076a1ab5a00,0x0076a1ab9000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T6 0x006d0001a000 stack: [0x0076a1692000,0x0076a179b6c0) sz: 1087168 tls: [0x0076a179ba00,0x0076a179f000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T7 0x006d0001e000 stack: [0x0076a0584000,0x0076a068d6c0) sz: 1087168 tls: [0x0076a068da00,0x0076a0691000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T8 0x006d00022000 stack: [0x00769c388000,0x00769c4816c0) sz: 1021632 tls: [0x00769c481a00,0x00769c485000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T9 0x006d00026000 stack: [0x00769b28a000,0x00769b3836c0) sz: 1021632 tls: [0x00769b383a00,0x00769b387000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T10 0x006d0002a000 stack: [0x00768ca71000,0x00768cb6a6c0) sz: 1021632 tls: [0x00768cb6aa00,0x00768cb6e000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T11 0x006d0002e000 stack: [0x00768b0d5000,0x00768b1ce6c0) sz: 1021632 tls: [0x00768b1cea00,0x00768b1d2000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T67 0x006d000f6000 stack: [0x0076cc045000,0x0076cc13e6c0) sz: 1021632 tls: [0x0076cc13ea00,0x0076cc142000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T13 0x006d00036000 stack: [0x0076d1a03000,0x0076d1b0c6c0) sz: 1087168 tls: [0x0076d1b0ca00,0x0076d1b10000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T65 0x006d000ee000 stack: [0x0076cfe1e000,0x0076cff176c0) sz: 1021632 tls: [0x0076cff17a00,0x0076cff1b000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T66 0x006d000f2000 stack: [0x0076cfd20000,0x0076cfe196c0) sz: 1021632 tls: [0x0076cfe19a00,0x0076cfe1d000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T18 0x006d00042000 stack: [0x007683dd1000,0x007683eda6c0) sz: 1087168 tls: [0x007683edaa00,0x007683ede000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T19 0x006d00046000 stack: [0x007682cc3000,0x007682dcc6c0) sz: 1087168 tls: [0x007682dcca00,0x007682dd0000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T20 0x006d0004a000 stack: [0x007681bb5000,0x007681cbe6c0) sz: 1087168 tls: [0x007681cbea00,0x007681cc2000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T21 0x006d0004e000 stack: [0x007680aa7000,0x007680bb06c0) sz: 1087168 tls: [0x007680bb0a00,0x007680bb4000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T24 0x006d00052000 stack: [0x007680999000,0x007680aa26c0) sz: 1087168 tls: [0x007680aa2a00,0x007680aa6000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T26 0x006d00056000 stack: [0x00768088b000,0x0076809946c0) sz: 1087168 tls: [0x007680994a00,0x007680998000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T27 0x006d0005a000 stack: [0x006ca5502000,0x006ca55fb6c0) sz: 1021632 tls: [0x006ca55fba00,0x006ca55ff000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T28 0x006d0005e000 stack: [0x006ca4404000,0x006ca44fd6c0) sz: 1021632 tls: [0x006ca44fda00,0x006ca4501000)
07-09 23:43:51.367  1181  1181 I app_process64: Thread: T29 0x006d00062000 stack: [0x006ca32f6000,0x006ca33ff6c0) sz: 1087168 tls: [0x006ca33ffa00,0x006ca3403000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T30 0x006d00066000 stack: [0x006ca1e00000,0x006ca1ef96c0) sz: 1021632 tls: [0x006ca1ef9a00,0x006ca1efd000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T31 0x006d0006a000 stack: [0x006ca1efe000,0x006ca1ff76c0) sz: 1021632 tls: [0x006ca1ff7a00,0x006ca1ffb000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T32 0x006d0006e000 stack: [0x006ca21f8000,0x006ca22f16c0) sz: 1021632 tls: [0x006ca22f1a00,0x006ca22f5000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T33 0x006d00072000 stack: [0x006ca1ffc000,0x006ca20f56c0) sz: 1021632 tls: [0x006ca20f5a00,0x006ca20f9000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T34 0x006d00076000 stack: [0x006ca20fa000,0x006ca21f36c0) sz: 1021632 tls: [0x006ca21f3a00,0x006ca21f7000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T35 0x006d0007a000 stack: [0x006ca1d02000,0x006ca1dfb6c0) sz: 1021632 tls: [0x006ca1dfba00,0x006ca1dff000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T36 0x006d0007e000 stack: [0x006c9b6d9000,0x006c9b7d26c0) sz: 1021632 tls: [0x006c9b7d2a00,0x006c9b7d6000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T37 0x006d00082000 stack: [0x006c9a5db000,0x006c9a6d46c0) sz: 1021632 tls: [0x006c9a6d4a00,0x006c9a6d8000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T38 0x006d00086000 stack: [0x006c9a4dd000,0x006c9a5d66c0) sz: 1021632 tls: [0x006c9a5d6a00,0x006c9a5da000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T39 0x006d0008a000 stack: [0x006c982e1000,0x006c983da6c0) sz: 1021632 tls: [0x006c983daa00,0x006c983de000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T40 0x006d0008e000 stack: [0x006c970e5000,0x006c971de6c0) sz: 1021632 tls: [0x006c971dea00,0x006c971e2000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T41 0x006d00092000 stack: [0x006c971e3000,0x006c972dc6c0) sz: 1021632 tls: [0x006c972dca00,0x006c972e0000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T42 0x006d00096000 stack: [0x006c983df000,0x006c984d86c0) sz: 1021632 tls: [0x006c984d8a00,0x006c984dc000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T43 0x006d0009a000 stack: [0x006c96fe7000,0x006c970e06c0) sz: 1021632 tls: [0x006c970e0a00,0x006c970e4000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T44 0x006d0009e000 stack: [0x006c92ee9000,0x006c92fe26c0) sz: 1021632 tls: [0x006c92fe2a00,0x006c92fe6000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T45 0x006d000a2000 stack: [0x006c91deb000,0x006c91ee46c0) sz: 1021632 tls: [0x006c91ee4a00,0x006c91ee8000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T46 0x006d000a6000 stack: [0x006c90ced000,0x006c90de66c0) sz: 1021632 tls: [0x006c90de6a00,0x006c90dea000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T47 0x006d000aa000 stack: [0x006c90bef000,0x006c90ce86c0) sz: 1021632 tls: [0x006c90ce8a00,0x006c90cec000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T48 0x006d000ae000 stack: [0x006c8eaf1000,0x006c8ebea6c0) sz: 1021632 tls: [0x006c8ebeaa00,0x006c8ebee000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T49 0x006d000b2000 stack: [0x006c8e9f3000,0x006c8eaec6c0) sz: 1021632 tls: [0x006c8eaeca00,0x006c8eaf0000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T50 0x006d000b6000 stack: [0x006c8bff5000,0x006c8c0ee6c0) sz: 1021632 tls: [0x006c8c0eea00,0x006c8c0f2000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T51 0x006d000ba000 stack: [0x006c8aee7000,0x006c8aff06c0) sz: 1087168 tls: [0x006c8aff0a00,0x006c8aff4000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T52 0x006d000be000 stack: [0x006c8add9000,0x006c8aee26c0) sz: 1087168 tls: [0x006c8aee2a00,0x006c8aee6000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T53 0x006d000c2000 stack: [0x006c88cdb000,0x006c88dd46c0) sz: 1021632 tls: [0x006c88dd4a00,0x006c88dd8000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T54 0x006d000c6000 stack: [0x006c87bcd000,0x006c87cd66c0) sz: 1087168 tls: [0x006c87cd6a00,0x006c87cda000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T55 0x006d000ca000 stack: [0x006c868cf000,0x006c869c86c0) sz: 1021632 tls: [0x006c869c8a00,0x006c869cc000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T56 0x006d000ce000 stack: [0x006c857c1000,0x006c858ca6c0) sz: 1087168 tls: [0x006c858caa00,0x006c858ce000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T57 0x006d000d2000 stack: [0x006c856b3000,0x006c857bc6c0) sz: 1087168 tls: [0x006c857bca00,0x006c857c0000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T58 0x006d000d6000 stack: [0x006c86abf000,0x006c86bc86c0) sz: 1087168 tls: [0x006c86bc8a00,0x006c86bcc000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T59 0x006d000da000 stack: [0x006c812a5000,0x006c813ae6c0) sz: 1087168 tls: [0x006c813aea00,0x006c813b2000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T61 0x006d000de000 stack: [0x006c80099000,0x006c801a26c0) sz: 1087168 tls: [0x006c801a2a00,0x006c801a6000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T63 0x006d000e2000 stack: [0x006c7ee9d000,0x006c7ef966c0) sz: 1021632 tls: [0x006c7ef96a00,0x006c7ef9a000)
07-09 23:43:51.368  1181  1181 I app_process64: Thread: T62 0x006d000e6000 stack: [0x006c7ef9b000,0x006c7f0946c0) sz: 1021632 tls: [0x006c7f094a00,0x006c7f098000)
07-09 23:43:51.369  1181  1181 I app_process64:
07-09 23:43:51.369  1181  1181 I app_process64: Memory tags around the buggy address (one tag corresponds to 16 bytes):
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862db400: 73  73  73  73  73  73  73  00  79  79  79  79  79  79  79  79
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862db500: 19  19  19  19  19  19  08  3f  9b  9b  9b  9b  9b  9b  08  8c
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862db600: 66  66  66  66  66  66  66  8b  12  12  12  12  12  12  12  00
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862db700: 62  62  62  62  62  62  62  17  38  38  38  38  38  38  38  08
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862db800: 67  67  67  67  67  67  67  08  06  06  06  06  06  06  06  06
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862db900: 83  83  83  83  83  83  83  08  8d  8d  8d  8d  8d  8d  8d  8d
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dba00: 57  57  57  57  57  57  57  60  71  71  71  71  71  71  0c  c5
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dbb00: 6f  6f  6f  6f  6f  6f  6f  18  3d  3d  3d  3d  3d  3d  08  51
07-09 23:43:51.369  1181  1181 I app_process64: =>0x0039862dbc00: 09  09  09  09  09  09  08  ab  10  10 [10] 10  10  10  10  10
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dbd00: fc  fc  fc  fc  fc  fc  fc  fc  8f  8f  8f  8f  8f  8f  8f  8f
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dbe00: 31  31  31  31  31  31  0c  bf  4d  4d  4d  4d  4d  4d  4d  5d
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dbf00: d4  d4  d4  d4  d4  d4  d4  d4  a9  a9  a9  a9  a9  a9  a9  c7
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dc000: 95  95  95  95  95  95  95  36  be  be  be  be  be  be  be  c5
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dc100: ef  ef  ef  ef  ef  ef  ef  ef  66  66  66  66  66  66  66  66
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dc200: 3a  3a  3a  3a  3a  3a  3a  3a  09  09  09  09  09  09  09  09
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dc300: 6f  6f  6f  6f  6f  6f  6f  00  67  67  67  67  67  67  67  f4
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dc400: bc  bc  bc  bc  bc  bc  bc  6a  d4  d4  d4  d4  d4  d4  d4  d4
07-09 23:43:51.369  1181  1181 I app_process64: Tags for short granules around the buggy address (one tag corresponds to 16 bytes):
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dbb00: ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  3d  ..
07-09 23:43:51.369  1181  1181 I app_process64: =>0x0039862dbc00: 6d  e2  0b  00  00  f1  09  ..  f8  62 [00] 00  ea  00  8e  cd
07-09 23:43:51.369  1181  1181 I app_process64:   0x0039862dbd00: ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..  ..
07-09 23:43:51.369  1181  1181 I app_process64: See https://clang.llvm.org/docs/HardwareAssistedAddressSanitizerDesign.html#short-granules for a description of short granule tags
07-09 23:43:51.369  1181  1181 I app_process64:
07-09 23:43:51.369  1181  1181 I app_process64: Registers where the failure occurred (pc 0x006caee73e54):
07-09 23:43:51.369  1181  1181 I app_process64:     x0  5800003f862888c8  x1  1700003a86286ac0  x2  0000000000000001  x3  0000003686300880
07-09 23:43:51.369  1181  1181 I app_process64:     x4  0000000000000020  x5  0000000000000014  x6  0000007fcf9ab000  x7  0000000000000001
07-09 23:43:51.369  1181  1181 I app_process64:     x8  4937a1e4dd9b1c74  x9  0200006e00000000  x10 0000006cbec5cf14  x11 000000771bbad680
07-09 23:43:51.369  1181  1181 I app_process64:     x12 000000000003b627  x13 0000000000000014  x14 0000000000000000  x15 00003b537fff49c0
07-09 23:43:51.369  1181  1181 I app_process64:     x16 0000000000000010  x17 0000000000000001  x18 000000771c644000  x19 0200006e00000000
07-09 23:43:51.369  1181  1181 I app_process64:     x20 cd000039862dbc80  x21 1700003a86286ac0  x22 000000771bcfda40  x23 0000007fd01a3650
07-09 23:43:51.369  1181  1181 I app_process64:     x24 0040000da000037e  x25 0000000000000000  x26 cd000039862dbc98  x27 cd000039862dbca0
07-09 23:43:51.369  1181  1181 I app_process64:     x28 00000007fd01a365  x29 0000007fd01a3680  x30 0000006caee73e58   sp 0000007fd01a3630
07-09 23:43:51.369  1181  1181 I app_process64: Learn more about HWASan reports: https://source.android.com/docs/security/test/memory-safety/hwasan-reports
07-09 23:43:51.370  1181  1181 I app_process64: SUMMARY: HWAddressSanitizer: tag-mismatch (/data/app/~~47cxnQp1PLqI56lgYho12g==/org.chromium.chrome-BkkkBaeMyLMy4SzvxB-_kg==/lib/arm64/libchrome.so+0x6873e54) (BuildId: f70b4ed1a4f72e94) -> content::protocol::InputHandler::InputInjector::InjectMouseEvent(blink::WebMouseEvent const&, std::__Cr::unique_ptr<content::protocol::Input::Backend::DispatchMouseEventCallback, std::__Cr::default_delete<content::protocol::Input::Backend::DispatchMouseEventCallback> >) at ./../../content/browser/devtools/protocol/input_handler.cc:695

```
# CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [xuanocto]

## Attachments

- android_crash.hwasan.log (text/plain, 59.5 KB)
- 2025-07-13 06-09-57.mkv (video/x-matroska, 12.5 MB)
- win_crash.mkv (video/x-matroska, 15.1 MB)
- win_crash.asan.log (text/plain, 91.3 KB)

## Timeline

### li...@chromium.org (2025-07-10)

I can't quite get this to reproduce, reporter were you able to get this to reproduce reliably? Since there's a race condition involved I might just not be hitting the race. If you can give some more specific instructions on how you clicked around to get the race that could be helpful.

The InputInjector is allocated in InputHandler::EnsureInjector

```
InputHandler::InputInjector* InputHandler::EnsureInjector(
    RenderWidgetHostImpl* widget_host) {
  for (auto& it : injectors_) {
    if (it->HasWidgetHost(widget_host))
      return it.get();
  }
  InputInjector* injector = new InputInjector(this, widget_host); <----
  injectors_.emplace(injector);
  return injector;
}

```

It's later freed in OnInputAck when MaybeSelfDestruct() is called. I noticed that the callback that is popped here only gets sendSuccess() called if it meets certain conditions, instead of unconditionally like in other parts of the code that pop the callbacks from the queue.

```
if ((blink::WebInputEvent::IsMouseEventType(event.GetType()) ||
         event.GetType() == blink::WebInputEvent::Type::kMouseWheel) &&
        !pending_mouse_callbacks_.empty()) {
      auto callback = std::move(pending_mouse_callbacks_.front());
      pending_mouse_callbacks_.pop_front();
      // We need to handle the event in the drag controller in case drag was
      // initiated at some point between dispatch and now because the event will
      // have been ignored during dispatch in this case.
      //
      // Note this also applies to the mouse move that triggers the drag, so
      // HandleMouseEvent has special logic to handle this specific case.
      if (!widget_host_ ||
          !owner_->drag_controller_.HandleMouseEvent(
              *widget_host_, static_cast<const blink::WebMouseEvent&>(event),
              callback)) {
        callback->sendSuccess();
      }
      MaybeSelfDestruct(); <---
      return;
    }

```
```
void MaybeSelfDestruct() {
    if (!pending_key_callbacks_.empty() || !pending_mouse_callbacks_.empty())
      return;
    if (widget_host_)
      widget_host_->RemoveInputEventObserver(this);
    owner_->injectors_.erase(this); <---
  }

```

Eventually there's some type of race where InjectMouseEvent is called and a crash happens. I'm a bit confused by this code snippet in InjectMouseEvent, though, ebecause input\_queued\_ is set to false, so the conditional is always hit, and pending\_mouse\_callbacks\_ pushes a callback to its queue then immediately pops it, so it seems a little redundant.

```
input_queued_ = false;
    pending_mouse_callbacks_.push_back(std::move(callback));
    widget_host_->ForwardMouseEvent(mouse_event);
    if (!input_queued_) {
      pending_mouse_callbacks_.back()->sendSuccess();
      pending_mouse_callbacks_.pop_back();
      MaybeSelfDestruct();
    }
  }

```

It looks like the most relevant possible owners no longer work on chromium, assigning to a devtools owner to take a look. Could you please reassign if necessary? I'm gonna mark this down as a high severity because even though devtools is in the browser the difficulty in trying to meet this race condition presents a significant hurdle for an attacker. Tentatively marking FoundIn as 140 since I couldn't get it to repro anywhere, so I can't confidently say this is repro-able in earlier versions of Chrome.

### ch...@google.com (2025-07-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-07-11)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-07-11)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### xu...@gmail.com (2025-07-13)

Hi, after some tests, I've succesfully reproduced this bug on 139.0.7219.0(Chrome Android Dev 139.0.7219.0), it includes a video below,
the trigger is not very stable but can be triggered certainly. The operation is:

1. open google.com in devtools
2. click the switch buttons behind the omnibox, you can choose mouse/click randomly
3. click random button on google.com page, chrome crashes
4. if not reproduced, try step 1-3 several times, chrome will crash.

If it's not reproduced, please check it several times, hopefully you can reproduce this issue on Latest Dev channel version.

There are other simpler trigger we tried, yet not stable as well

### xu...@gmail.com (2025-07-13)

We have also conducted some tests on the Windows desktop version of Chromium and found that this issue should not be unique to Android. The test version used was chromium-1478942-win64-asan (140.0.7262.0), and the reproduction steps were similar to those mentioned above. We have also attached a video below. Similar problems may exist in Chrome implementations across other platforms (Linux,Mac ...).

### xu...@gmail.com (2025-07-13)

Through the debugger, we roughly analyzed the cause. Here, the isActive condition, the mouse click that triggered the crash went into this if statement, while the normal mouse click events did not enter. This should be the judgment of whether the page rendered by devtools is still valid. If it is found to be invalid, the callback will be executed directly, and then the InputInjector object will be destroyed.

```
content::RenderWidgetHostImpl::ForwardMouseEventWithLatencyInfo will call input::InputRouterImpl::SendMouseEvent

components/input/input_router_impl.cc   (This is a generic implementation and does not represent code specific to any particular platform)
void InputRouterImpl::SendMouseEvent(
    const MouseEventWithLatencyInfo& mouse_event,
    MouseEventCallback event_result_callback,
    DispatchToRendererCallback& dispatch_callback) {
  if ((!IsActive() &&                                         
       base::FeatureList::IsEnabled(
           blink::features::kDropInputEventsWhilePaintHolding)) ||
      (mouse_event.event.GetType() == WebInputEvent::Type::kMouseDown &&
       gesture_event_queue_.GetTouchpadTapSuppressionController()
           ->ShouldSuppressMouseDown(mouse_event)) ||
      (mouse_event.event.GetType() == WebInputEvent::Type::kMouseUp &&
       gesture_event_queue_.GetTouchpadTapSuppressionController()
           ->ShouldSuppressMouseUp())) {
    // Run DispatchToRendererCallback before the event ack callback since
    // RenderWidgetHostImpl input observers would generally expect to see an
    // event before they see an ack for the event.
    std::move(dispatch_callback)
        .Run(mouse_event.event, DispatchToRendererResult::kNotDispatched);

    std::move(event_result_callback)
        .Run(mouse_event, blink::mojom::InputEventResultSource::kBrowser,
             blink::mojom::InputEventResultState::kIgnored);                 <-  trigger content::protocol::InputHandler::InputInjector::MaybeSelfDestruct
    return;
  }

  SendMouseEventImmediately(mouse_event, std::move(event_result_callback),
                            dispatch_callback);
}

```

It feels like OnInputEventAck should originally be an asynchronous callback, and it should be executed after the mouse event is processed, because the function to destroy the InputInjector object will be executed in it. The general process is as follows in the attached diagram.

```
Browser Process                 Renderer Process
     |                                 |
     | ForwardMouseEvent               |
     |-------------------------------->|
     | (Immediate return)              | Process Event...
     |                                 | (Takes time)
     |                                 |
     | OnInputEventAck                 |
     |<--------------------------------|
     | (asynchronous callback)         |

```

However, after sending ForwardMouseEvent, if it is judged that the page rendered by devtools is invalid, for example, due to some unexpected factors, it will directly synchronously call OnMouseEventAck to destroy the InputInjector object, and then after InjectMouseEvent sends ForwardMouseEvent, it still needs to use the input\_queued\_ member of the InputInjector object.

I'm not very sure if this is the cause of the UAF issue. I hope my analysis can be helpful to you.

### pf...@google.com (2025-07-16)

The analysis in the comments above is spot-on, great work! We trigger the UAF because InputRouterImpl has this path that [drops events](https://source.chromium.org/chromium/chromium/src/+/main:components/input/input_router_impl.cc;drc=b861b40f7b2e4987f54f5ce496416512035711b5;l=109) in a few conditions, which gets ack'ed to InputHandler which then [destroys itself](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/protocol/input_handler.cc;drc=95685daa270ab4081139f1a7471e5077010bf757;l=794), even though it's still further up on the call stack. This doesn't strictly require android & remote debugging, but it's easier to trigger there, since InputRouterImpl will drop the events when in a fling tap suppression downtime. It will also drop while the router is not active, which [happens](https://source.chromium.org/chromium/chromium/src/+/main:components/input/input_router.h;drc=b861b40f7b2e4987f54f5ce496416512035711b5;l=41) in the short period of time before the renderer has produced the first content. It's possible to trigger the issue via that path as well, which interestingly was reported and fixed for keyboard inputs in the past (<https://crbug.com/40055273>).

I'll apply the same fix as for the keyboard inputs to the rest of the protocol handler.

### dx...@google.com (2025-07-16)

Project: chromium/src  

Branch:  main  

Author:  Philip Pfaffe [pfaffe@chromium.org](mailto:pfaffe@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6760050>

Fix UAF in InputInjector

---


Expand for full commit details
```
     
    Fixed: 430635213 
    Change-Id: Id076fa79d74fca61354e1cbe78c741ef26ec2fba 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6760050 
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org> 
    Auto-Submit: Philip Pfaffe <pfaffe@chromium.org> 
    Reviewed-by: Alex Rudenko <alexrudenko@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1487530}

```

---

Files:

- M `content/browser/devtools/protocol/input_handler.cc`

---

Hash: [54788bf20c04579648d93dfbe0deb1840fb819ca](http://crrev.com/54788bf20c04579648d93dfbe0deb1840fb819ca)  

Date: Wed Jul 16 11:17:01 2025


---

### am...@chromium.org (2025-07-24)

This issue has pretty significant preconditions to successfully exploit. Downgrading to S2 / medium severity.

### sp...@google.com (2025-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of heavily mitigated memory corruption in a non-sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-08-06)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-08-06)

Fix landed in 140; no merge needed

### ch...@google.com (2025-10-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### x4...@gmail.com (2025-10-25)

Hey xuanocto, can you please help me with the steps to building hwasan for android? I tried building it, it was successful but chromium crashes as soon as I start the app. I would appreciate your help, you can email me at [x4nd3r.h1.dump@gmail.com](mailto:x4nd3r.h1.dump@gmail.com)

## Bounty Award

> report of heavily mitigated memory corruption in a non-sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/430635213)*
