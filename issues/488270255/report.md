# css.ResolveValues() does not check validity of reserved values

| Field | Value |
|-------|-------|
| **Issue ID** | [488270255](https://issues.chromium.org/issues/488270255) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>CSS |
| **Reporter** | he...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | $2,000.00 |

## Description

NOTE: The text below is for another bug. This bug was repurposed to deal with the issue of invalid env() or attr() inside CSS.resolveValues (from Devtools).

### Summary

`CSS.setScopeText` (via [`InspectorCSSAgent::setScopeText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_css_agent.cc;l=3092)) desynchronizes nested `@scope` wrappers: [`CSSScopeRule::SetPreludeText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_scope_rule.cc;l=69) mutates only wrapper-local `group_rule_`, and later index-based reattach calls [`CSSGroupingRule::Reattach`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_grouping_rule.cc;l=363) with a non-group `StyleRule*`, leading to type confusion and the memory corruption.

### Details

`CSS.setScopeText` edits the prelude of an existing `@scope` rule by calling [`InspectorStyleSheet::SetScopeRuleText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_style_sheet.cc;l=1532), which locates the existing `CSSScopeRule` wrapper and invokes `CSSScopeRule::SetPreludeText`.

The key problem is that `CSSScopeRule::SetPreludeText` replaces the wrapper’s internal `group_rule_` pointer with a newly allocated `StyleRuleScope`, but does not replace the corresponding `StyleRuleScope` inside the stylesheet’s rule graph. This means the wrapper becomes detached from the real sheet contents, yet still participates in subsequent CSSOM calls and later `Reattach()` cascades (which assume wrapper/rule index+type stability).

In [`CSSScopeRule::SetPreludeText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_scope_rule.cc;l=69), the mutation ends by assigning a new rule object only to the wrapper field:

```
  HeapVector<Member<StyleRuleBase>> new_child_rules;
  new_child_rules.ReserveInitialCapacity(
      GetStyleRuleScope().ChildRules().size());
  for (StyleRuleBase* child_rule : GetStyleRuleScope().ChildRules()) {
    new_child_rules.push_back(
        child_rule->Clone(new_style_scope->RuleForNesting(),
                          /*mixin_parameter_bindings=*/nullptr));
  }
  group_rule_ = MakeGarbageCollected<StyleRuleScope>(
      *new_style_scope, std::move(new_child_rules));

```

After this, page JS can mutate the stale `CSSScopeRule` wrapper (e.g. `deleteRule()` then `insertRule('@media all {}', 0)`) such that the wrapper’s `child_rule_cssom_wrappers_` at index 0 becomes a `CSSMediaRule`, while the stylesheet-backed `@scope` still has a style rule at index 0.

Later, a parent rule mutation that performs a replacement+reattach (e.g. [`CSSStyleRule::setSelectorText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_style_rule.cc;l=87)) reattaches nested wrappers by index. During that reattach, the stale scope wrapper forwards `ChildRules()[0]` (a `StyleRule*`) into the `CSSMediaRule` wrapper’s `Reattach()`. `CSSMediaRule` inherits `CSSGroupingRule::Reattach`, which performs an unchecked cast:

In [`CSSGroupingRule::Reattach`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_grouping_rule.cc;l=363), the downcast is a `static_cast` without runtime validation:

```
void CSSGroupingRule::Reattach(StyleRuleBase* rule) {
  DCHECK(rule);
  group_rule_ = static_cast<StyleRuleGroup*>(rule);
  for (unsigned i = 0; i < child_rule_cssom_wrappers_.size(); ++i) {
    if (child_rule_cssom_wrappers_[i]) {
      child_rule_cssom_wrappers_[i]->Reattach(
          group_rule_->ChildRules()[i].Get());
    }
  }
}

```

Once the wrapper’s `group_rule_` is miscast to a `StyleRuleGroup*`, subsequent CSSOM operations on that wrapper (notably `insertRule`) can write through the misinterpreted layout, corrupting the real `StyleRule` object fields. A reliable symptom is that later style resolution (RuleSet construction) crashes in `RuleSet::AddStyleRule`/`AddChildRules` while iterating nested rules, consistent with a corrupted `StyleRule::ChildRules()` pointer.

### Bisection

This issue is introduced by the commit: `ed46557e198a8fce6c1ef52b38e5c17734c99ba9` [css-nesting] Implement CSSScopeRule::SetPreludeText by rule replacement.

### Reproduction

Download the chrome from `https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1591355.zip`

To make the reproduction more conveniently, we leverage a nodejs script to setup CDP and reproduce it automatically. You may need to firstly modify the `CHROME`, `HTML` to the actual file path in the mjs, and then:

```
node run_poc.mjs

```

After several iteration, it would catch the ASAn-crash shown in the `asan.txt`

### Suggested Fix

Harden `CSSGroupingRule::Reattach` against type mismatches by validating `rule` is a `StyleRuleGroup` before assigning it to `group_rule_` (e.g. `DynamicTo<StyleRuleGroup>`).

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 13.7 KB)
- [run_poc.mjs](attachments/run_poc.mjs) (text/javascript, 4.0 KB)
- [poc.html](attachments/poc.html) (text/html, 176 B)
- [background.js](attachments/background.js) (text/javascript, 3.3 KB)
- [manifest.json](attachments/manifest.json) (application/json, 215 B)
- [poc.html](attachments/poc_74019024.html) (text/html, 252 B)
- [resolve_values_asan.txt](attachments/resolve_values_asan.txt) (text/plain, 8.7 KB)

## Timeline

### aj...@google.com (2026-02-28)

Hello - please upload a poc that is just an html file, we cannot feed node servers into our reproduction infrastructure.

### he...@gmail.com (2026-02-28)

Hi, I've attached the poc.html which I forget to upload during the submission. However, since this issue exists in the inspector, i.e., triggered by the Chrome Devtool Protocol, it is not reachable by purely HTML loading. Instead, it requires enabling the CDP in the chrome, and the issue occurs when the remote/local CDP message triggers specific Inspector functions. Therefore, you may need to manual reproduce it since IIUC cluster fuzz doesn't support such CDP reproduction.

The previous attached `run_poc.mjs` is not a HTML server, it is a automation script which launch the chrome with CDP enabled, load the poc.html, send the specific CDP message, and cause the memory corruption in the renderer. The threat model here is that CDP have the ability to execute arbitrary **JS code** in the renderer, but it cannot execute arbitrary **code** in the renderer / cannot compromise the renderer, thus the memory corruption issue triggered by CDP can have security impact.

Also, I recall that history memory corruption issues in CDP are treated as the security issues, hence I report it. Feel free to correct me if you think the memory corruption in CDP is ineligible.

Many thanks.

### pe...@google.com (2026-02-28)

Thank you for providing more feedback. Adding the requester to the CC list.

### cl...@appspot.gserviceaccount.com (2026-03-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6273381972246528.

### mp...@google.com (2026-03-04)

I think extensions with the debugger permission can access DevTools protocol? Can you show that an extension with this (rather powerful) permission can trigger this UAF?

### mp...@google.com (2026-03-04)

Low severity for now given its highly mitigated nature.

### an...@chromium.org (2026-03-04)

sesse@ volunteered to take a look a this. (Thanks!)

### se...@chromium.org (2026-03-04)

In the process of trying to reproduce this, I got this DCHECK crash:

```
[2201261:2201261:0304/120530.814871:FATAL:third_party/blink/renderer/core/css/resolver/style_cascade.cc:88] DCHECK failed: ident_token.GetType() == kIdentToken (7 vs. 0).
    #0 0x55704456b3c6 in ___interceptor_backtrace ??:0:0
    #1 0x7fe5cff81ccb in base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) ./../../base/debug/stack_trace_posix.cc:1048:7
    #2 0x7fe5cfea2ffd in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace.cc:280:20
    #3 0x7fe5cfea2e05 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:275:28
    #4 0x7fe5cf66450a in logging::LogMessage::Flush() ./../../base/logging.cc:706:29
    #5 0x7fe5cf664121 in logging::LogMessage::~LogMessage() ./../../base/logging.cc:695:3
    #6 0x7fe5cf58c155 in logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage() ./../../base/check.cc:181:3
    #7 0x7fe5cf58c179 in logging::(anonymous namespace)::DCheckLogMessage::~DCheckLogMessage() ./../../base/check.cc:177:32
    #8 0x7fe5cf58d497 in std::__Cr::default_delete<logging::LogMessage>::operator()(logging::LogMessage*) const ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #9 0x7fe5cf58c5e6 in std::__Cr::unique_ptr<logging::LogMessage, std::__Cr::default_delete<logging::LogMessage> >::reset(logging::LogMessage*) ./gen/third_party/libc++/src/include/__memory/unique_ptr.h:288:7
    #10 0x7fe5cf58b369 in logging::CheckError::~CheckError() ./../../base/check.cc:348:16
    #11 0x7fe4dcecb879 in blink::(anonymous namespace)::ConsumeVariableName(blink::CSSParserTokenStream&) ./../../third_party/blink/renderer/core/css/resolver/style_cascade.cc:88:3
    #12 0x7fe4dcec1d6e in blink::StyleCascade::ResolveEnvInto(blink::CSSParserTokenStream&, blink::TreeScope const*, blink::CascadeResolver&, blink::CSSParserContext const&, blink::StyleCascade::TokenSequence&) ./../../third_party/blink/renderer/core/css/resolver/style_cascade.cc:2303:32
    #13 0x7fe4dceaf22a in blink::StyleCascade::ResolveTokensInto(blink::CSSParserTokenStream&, blink::TreeScope const*, blink::CascadeResolver&, blink::CSSParserContext const&, blink::StyleCascade::FunctionContext*, blink::CSSParserTokenType, blink::StyleCascade::TokenSequence&) ./../../third_party/blink/renderer/core/css/resolver/style_cascade.cc:1656:18
    #14 0x7fe4dceaeb48 in blink::StyleCascade::ResolveSubstitutions(blink::StyleResolverState&, blink::CSSUnparsedDeclarationValue const&, blink::TreeScope const*, blink::MixinParameterBindings const*) ./../../third_party/blink/renderer/core/css/resolver/style_cascade.cc:437:16
    #15 0x7fe4e1000965 in blink::InspectorCSSAgent::resolveValues(std::__Cr::unique_ptr<std::__Cr::vector<blink::String, std::__Cr::allocator<blink::String> >, std::__Cr::default_delete<std::__Cr::vector<blink::String, std::__Cr::allocator<blink::String> > > >, int, std::__Cr::optional<blink::String>, std::__Cr::optional<blink::String>, std::__Cr::optional<blink::String>, std::__Cr::unique_ptr<std::__Cr::vector<blink::String, std::__Cr::allocator<blink::String> >, std::__Cr::default_delete<std::__Cr::vector<blink::String, std::__Cr::allocator<blink::String> > > >*) ./../../third_party/blink/renderer/core/inspector/inspector_css_agent.cc:2500:9
    #16 0x7fe4e1001730 in non-virtual thunk to blink::InspectorCSSAgent::resolveValues(std::__Cr::unique_ptr<std::__Cr::vector<blink::String, std::__Cr::allocator<blink::String> >, std::__Cr::default_delete<std::__Cr::vector<blink::String, std::__Cr::allocator<blink::String> > > >, int, std::__Cr::optional<blink::String>, std::__Cr::optional<blink::String>, std::__Cr::optional<blink::String>, std::__Cr::unique_ptr<std::__Cr::vector<blink::String, std::__Cr::allocator<blink::String> >, std::__Cr::default_delete<std::__Cr::vector<blink::String, std::__Cr::allocator<blink::String> > > >*) ./../../third_party/blink/renderer/core/inspector/inspector_css_agent.cc:0:0
    #17 0x7fe4eb10e15a in blink::protocol::CSS::DomainDispatcherImpl::resolveValues(crdtp::Dispatchable const&) ./gen/third_party/blink/renderer/core/inspector/protocol/css.cc:1397:44
    #18 0x7fe4eb11f115 in blink::protocol::CSS::DomainDispatcherImpl::Dispatch(std::__Cr::span<unsigned char const, 18446744073709551615ul>)::$_0::operator()(crdtp::Dispatchable const&) const ./gen/third_party/blink/renderer/core/inspector/protocol/css.cc:991:5
    #19 0x7fe4eb11f03d in std::__Cr::__invoke_result_impl<void, blink::protocol::CSS::DomainDispatcherImpl::Dispatch(std::__Cr::span<unsigned char const, 18446744073709551615ul>)::$_0&, crdtp::Dispatchable const&>::type std::__Cr::__invoke<blink::protocol::CSS::DomainDispatcherImpl::Dispatch(std::__Cr::span<unsigned char const, 18446744073709551615ul>)::$_0&, crdtp::Dispatchable const&>(blink::protocol::CSS::DomainDispatcherImpl::Dispatch(std::__Cr::span<unsigned char const, 18446744073709551615ul>)::$_0&, crdtp::Dispatchable const&) ./gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
    #20 0x7fe4eb11f00d in void std::__Cr::__invoke_void_return_wrapper<void, true>::__call<blink::protocol::CSS::DomainDispatcherImpl::Dispatch(std::__Cr::span<unsigned char const, 18446744073709551615ul>)::$_0&, crdtp::Dispatchable const&>(blink::protocol::CSS::DomainDispatcherImpl::Dispatch(std::__Cr::span<unsigned char const, 18446744073709551615ul>)::$_0&, crdtp::Dispatchable const&) ./gen/third_party/libc++/src/include/__type_traits/invoke.h:350:5
    #21 0x7fe4eb11efdd in void std::__Cr::__invoke_r<void, blink::protocol::CSS::DomainDispatcherImpl::Dispatch(std::__Cr::span<unsigned char const, 18446744073709551615ul>)::$_0&, crdtp::Dispatchable const&>(blink::protocol::CSS::DomainDispatcherImpl::Dispatch(std::__Cr::span<unsigned char const, 18446744073709551615ul>)::$_0&, crdtp::Dispatchable const&) ./gen/third_party/libc++/src/include/__type_traits/invoke.h:356:10
    #22 0x7fe4eb11efa6 in void std::__Cr::__function::__policy_func<void (crdtp::Dispatchable const&)>::__call_func<blink::protocol::CSS::DomainDispatcherImpl::Dispatch(std::__Cr::span<unsigned char const, 18446744073709551615ul>)::$_0>(std::__Cr::__function::__policy_storage const*, crdtp::Dispatchable const&) ./gen/third_party/libc++/src/include/__functional/function.h:443:12
    #23 0x7fe542fbc0e7 in std::__Cr::__function::__policy_func<void (crdtp::Dispatchable const&)>::operator()(crdtp::Dispatchable const&) const ./gen/third_party/libc++/src/include/__functional/function.h:502:12
    #24 0x7fe542fbc08d in std::__Cr::function<void (crdtp::Dispatchable const&)>::operator()(crdtp::Dispatchable const&) const ./gen/third_party/libc++/src/include/__functional/function.h:754:10
    #25 0x7fe542fa837c in crdtp::UberDispatcher::Dispatch(crdtp::Dispatchable const&) const::$_0::operator()() const ./../../third_party/inspector_protocol/crdtp/dispatch.cc:544:15
    #26 0x7fe542fa8355 in std::__Cr::__invoke_result_impl<void, crdtp::UberDispatcher::Dispatch(crdtp::Dispatchable const&) const::$_0&>::type std::__Cr::__invoke<crdtp::UberDispatcher::Dispatch(crdtp::Dispatchable const&) const::$_0&>(crdtp::UberDispatcher::Dispatch(crdtp::Dispatchable const&) const::$_0&) ./gen/third_party/libc++/src/include/__type_traits/invoke.h:90:27
    #27 0x7fe542fa8335 in void std::__Cr::__invoke_void_return_wrapper<void, true>::__call<crdtp::UberDispatcher::Dispatch(crdtp::Dispatchable const&) const::$_0&>(crdtp::UberDispatcher::Dispatch(crdtp::Dispatchable const&) const::$_0&) ./gen/third_party/libc++/src/include/__type_traits/invoke.h:350:5
    #28 0x7fe542fa8315 in void std::__Cr::__invoke_r<void, crdtp::UberDispatcher::Dispatch(crdtp::Dispatchable const&) const::$_0&>(crdtp::UberDispatcher::Dispatch(crdtp::Dispatchable const&) const::$_0&) ./gen/third_party/libc++/src/include/__type_traits/invoke.h:356:10
    #29 0x7fe542fa828e in void std::__Cr::__function::__policy_func<void ()>::__call_func<crdtp::UberDispatcher::Dispatch(crdtp::Dispatchable const&) const::$_0>(std::__Cr::__function::__policy_storage const*) ./gen/third_party/libc++/src/include/__functional/function.h:443:12
    #30 0x7fe542fba83f in std::__Cr::__function::__policy_func<void ()>::operator()() const ./gen/third_party/libc++/src/include/__functional/function.h:502:12
    #31 0x7fe542fa9cd5 in std::__Cr::function<void ()>::operator()() const ./gen/third_party/libc++/src/include/__functional/function.h:754:10
    #32 0x7fe542fa5040 in crdtp::UberDispatcher::DispatchResult::Run() ./../../third_party/inspector_protocol/crdtp/dispatch.cc:509:3
    #33 0x7fe4e0e1408d in blink::DevToolsSession::DispatchProtocolCommandImpl(int, blink::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:278:59
    #34 0x7fe4e0e129f0 in blink::DevToolsSession::DispatchProtocolCommand(int, blink::String const&, base::span<unsigned char const, 18446744073709551615ul, unsigned char const*>) ./../../third_party/blink/renderer/core/inspector/devtools_session.cc:243:10
    #35 0x7fe4c9723603 in blink::mojom::blink::DevToolsSessionStubDispatch::Accept(blink::mojom::blink::DevToolsSession*, mojo::Message*) ./gen/third_party/blink/public/mojom/devtools/devtools_agent.mojom-blink.cc:1542:13
    #36 0x7fe4e0e29757 in blink::mojom::blink::DevToolsSessionStub<mojo::RawPtrImplRefTraits<blink::mojom::blink::DevToolsSession> >::Accept(mojo::Message*) ./gen/third_party/blink/public/mojom/devtools/devtools_agent.mojom-blink.h:451:12
    #37 0x7fe5d0f2e4af in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:1085:54
    #38 0x7fe5d0f2d292 in mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:383:18
    #39 0x7fe5d0f6b989 in mojo::MessageDispatcher::Accept(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/message_dispatcher.cc:44:19
    #40 0x7fe5d0f34251 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) ./../../mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:747:20
    #41 0x7fe59f58f2cf in IPC::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification) ./../../ipc/ipc_mojo_bootstrap.cc:1199:24
    #42 0x7fe59f592670 in void base::internal::DecayedFunctorTraits<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>::Invoke<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>(void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&) ./../../base/functional/bind_internal.h:740:12
    #43 0x7fe59f59246a in void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, void, 0ul, 1ul, 2ul>::MakeItSo<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>>(void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>&&) ./../../base/functional/bind_internal.h:932:12
    #44 0x7fe59f592237 in void base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunImpl<void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, 0ul, 1ul, 2ul>(void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), std::__Cr::tuple<scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>) ./../../base/functional/bind_internal.h:1069:14
    #45 0x7fe59f592089 in base::internal::Invoker<base::internal::FunctorTraits<void (IPC::ChannelAssociatedGroupController::*&&)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), IPC::ChannelAssociatedGroupController*&&, mojo::Message&&, IPC::(anonymous namespace)::ScopedUrgentMessageNotification&&>, base::internal::BindState<true, true, false, void (IPC::ChannelAssociatedGroupController::*)(mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification), scoped_refptr<IPC::ChannelAssociatedGroupController>, mojo::Message, IPC::(anonymous namespace)::ScopedUrgentMessageNotification>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:982:12
    #46 0x7fe5cf563e03 in base::OnceCallback<void ()>::Run() && ./../../base/functional/callback.h:155:12
    #47 0x7fe5cfa902cf in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:229:34
    #48 0x7fe5cfbc0b28 in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_4&&) ./../../base/task/common/task_annotator.h:112:5
    #49 0x7fe5cfbbfb1f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
    #50 0x7fe5cfbbe89b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    #51 0x7fe5cfbbfff3 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:0:0
    #52 0x7fe5cf6df56b in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:42:55
    #53 0x7fe5cfbc1c93 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    #54 0x7fe5cf9182b8 in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:135:14
    #55 0x7fe5b7b9e8d6 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer_main.cc:332:16
    #56 0x7fe5b86890fb in content::RunZygote(content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:664:14
    #57 0x7fe5b868a92d in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> > const&, content::MainFunctionParams, content::ContentMainDelegate*) ./../../content/app/content_main_runner_impl.cc:771:12
    #58 0x7fe5b868e127 in content::ContentMainRunnerImpl::Run() ./../../content/app/content_main_runner_impl.cc:1152:10
    #59 0x7fe5b8683fb0 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) ./../../content/app/content_main.cc:358:36
    #60 0x7fe5b8684df6 in content::ContentMain(content::ContentMainParams) ./../../content/app/content_main.cc:371:10
    #61 0x557044608481 in ChromeMain ./../../chrome/app/chrome_main.cc:191:12
    #62 0x557044607ce2 in main ./../../chrome/app/chrome_exe_main_aura.cc:17:10
    #63 0x7fe48e833ca8 in __libc_start_call_main ./csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #64 0x7fe48e833d65 in __libc_start_main ./csu/../csu/libc-start.c:360:3
    #65 0x557044521cea in _start ??:0:0
Task trace:
    #0 0x7fe59f5c3177 in IPC::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:1138:13
Crash keys:
  "devtools_present" = "true"
  "view-count" = "2"
  "loaded-origin-0" = "null"
  "web-frame-count" = "1"
  "renderer_foreground" = "true"
  "v8_ro_space_firstpage_address" = "0x7a9300000000"
  "v8_isolate_address" = "0x7ef464a45000"
  "reentry_guard_tls_slot" = "unused"
  "switch-19" = "--trace-process-track-uuid=1090478943850377728"
  "switch-18" = "--pseudonymization-salt-handle=7,i,11926260313882726901,12767309"
  "switch-17" = "--variations-seed-version"
  "switch-16" = "--field-trial-handle=3,i,1405170713663509779,1267813519547597058"
  "switch-15" = "--metrics-shmem-handle=4,i,5614766757032133176,22323829499055042"
  "switch-14" = "--shared-files=v8_context_snapshot_data:100"
  "switch-13" = "--launch-time-ticks=182339189094"
  "switch-12" = "--time-ticks-at-unix-epoch=-1772439975035805"
  "switch-11" = "--renderer-client-id=5"
  "switch-10" = "--enable-main-frame-before-activation"
  "switch-9" = "--num-raster-threads=4"
  "switch-8" = "--lang=en-GB"
  "switch-7" = "--ozone-platform=x11"
  "switch-6" = "--remote-debugging-pipe"
  "osarch" = "x86_64"
  "pid" = "2201261"
  "ptype" = "renderer"
  "switch-5" = "--no-sandbox"
  "switch-4" = "--change-stack-guard-on-fork=enable"
  "switch-3" = "--user-data-dir=/tmp/any/profile-1772622304085-2201062-a1"
  "switch-2" = "--enable-crash-reporter=,"
  "switch-1" = "--crashpad-handler-pid=2201085"
  "num-switches" = "20"

```

I'm trying to see if it's related or an independent issue.

### se...@chromium.org (2026-03-04)

Seemingly it comes from this in the PoC:

```
    const race = await Promise.race([
      send("CSS.resolveValues", { nodeId, values: ["env(1)", "attr(1)"] }, sessionId).then(
        () => "resolved",
      ),
      sleep(5000).then(() => "timeout"),
    ]);

```

env(1) isn't a valid declaration value, and we seemingly don't check for those when they come in from Devtools' CSS.resolveValues().

After changing the PoC to use var(--foo) instead, I don't get a crash. I don't read your description as this actually being directly related, though. Can you confirm that the bug should be reproducible even without feeding in the invalid env()?

I'm going to send out the env() fix and a To<> hardening shortly, but I don't believe it will fix the actual underlying bug.

### se...@chromium.org (2026-03-04)

I think maybe just the wrong PoC (run\_poc.mjs) was attached. This one doesn't seem to do any CSSOM manipulation at all.

### ch...@google.com (2026-03-04)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must exceed severity.

### dx...@google.com (2026-03-04)

Project: chromium/src  

Branch:  main  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7627756>

Make InspectorCSSAgent::resolveValues() check for invalid syntax.

---


Expand for full commit details
```
     
    This is similar to fixes we did for Typed OM; ResolveSubstitutions() 
    assumes that the grammar is valid and will DCHECK if not, so we need 
    to check this up-front. 
     
    Bug: 488270255 
    Change-Id: I4909305f6551c4bfc09b48932f102de7e813136e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7627756 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1593954}

```

---

Files:

- M `third_party/blink/renderer/core/inspector/inspector_css_agent.cc`
- M `third_party/blink/web_tests/inspector-protocol/css/css-resolve-values-expected.txt`
- M `third_party/blink/web_tests/inspector-protocol/css/css-resolve-values.js`

---

Hash: [413ddd0099e56ada6e88c43814f1ee135b8d9c08](https://chromiumdash.appspot.com/commit/413ddd0099e56ada6e88c43814f1ee135b8d9c08)  

Date: Wed Mar 4 15:45:53 2026


---

### dx...@google.com (2026-03-05)

Project: chromium/src  

Branch:  main  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7627755>

Harden cast in CSSGroupingRule::Reattach().

---


Expand for full commit details
```
     
    Bug: 488270255 
    Change-Id: I87548f6057ed2a7633f8e0e807347bd1ff92f752 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7627755 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1594622}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_grouping_rule.cc`
- M `third_party/blink/renderer/core/css/style_rule.h`

---

Hash: [0e7b7e97d89f8c796c3b74aba171c862c8a986f0](https://chromiumdash.appspot.com/commit/0e7b7e97d89f8c796c3b74aba171c862c8a986f0)  

Date: Thu Mar 5 13:46:26 2026


---

### he...@gmail.com (2026-03-05)

Yes, I think the core of this issue is `"env(1)", "attr(1)"`, this is a variant of my recent reports 484751092, but this one is inside the devtools.

### se...@chromium.org (2026-03-05)

So @scope, and setScopeText, has nothing to do with the bug?

### he...@gmail.com (2026-03-05)

Oh sorry for that. There should be two bugs that I need to report.

The first one is indeed the setScopeText as this report demonstrated, but I attach the wrong POC. Actually the wrong POC demonstrate my another **should have been report** OOB issue inside the DevTools `CSS.resolveValues`. I somehow mix them up during my submission time and cause that this report contains the RCA with the first issue, and the POC of the second (non-reported) issue.

Deeply sorry for that. I'll update the POC for this first issue ASAP. And will fill up another issue which uses `env(1)`. Thank you so much for taking time looking at this, and I deeply appreciate that. (I might be trapped by the CSS implementation recently)

Many thanks!

### se...@chromium.org (2026-03-05)

Perhaps we should do the opposite? Re-target this bug to be about env(1), since we've now fixed that issue, and then file a new one for setScopeText?

### he...@gmail.com (2026-03-05)

Good idea, I'll do that. Thank you very much!

### se...@chromium.org (2026-03-05)

Note to security: <https://chromium-review.googlesource.com/c/chromium/src/+/7627755> is not relevant to this bug; it is for the type confusion bug, which will be re-submitted under another number.

### he...@gmail.com (2026-03-05)

### Summary

`InspectorCSSAgent::resolveValues` (DevTools protocol `CSS.resolveValues`) creates a `CSSVariableData` directly from an arbitrary string with `needs_variable_resolution=true`, then calls `StyleCascade::ResolveSubstitutions` to resolve substitution functions like `env()`/`attr()`. In this path, `StyleCascade::ConsumeVariableName()` assumes that the first argument token is an identifier and unconditionally calls `CSSParserToken::Value().ToAtomicString()`. When the first token is actually a non-string-backed token such as a `kNumberToken`, `Value()` produces an invalid `StringView` and hashing it triggers the OOB read in `AtomicStringTable::Add`.

### Details

DevTools `CSS.resolveValues` resolves attacker-controlled strings in the context of an element. The implementation in [`InspectorCSSAgent::resolveValues`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_css_agent.cc;l=2443) wraps each input string into `CSSVariableData` and then asks the style cascade to resolve substitutions:

[`InspectorCSSAgent::resolveValues`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_css_agent.cc;l=2474):

```
CSSVariableData* data =
    CSSVariableData::Create(value, /* is_animation_tainted= */ false,
                            /* is_attr_tainted= */ false,
                            /*needs_variable_resolution=*/true);
...
const CSSUnparsedDeclarationValue* unparsed =
    MakeGarbageCollected<CSSUnparsedDeclarationValue>(data, parser_context);
...
const CSSUnparsedDeclarationValue* substituted =
    StyleCascade::ResolveSubstitutions(state, *unparsed, &document,
                                       /*env_bindings=*/nullptr);

```

During substitution resolution, `env()` and `attr()` are handled in [`StyleCascade::ResolveEnvInto`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/style_cascade.cc;l=2297) / `ResolveAttrInto`, both of which call a helper that consumes the variable name token. That helper only enforces the token type with a `DCHECK` and then calls `Value()` unconditionally:

[`ConsumeVariableName`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/style_cascade.cc;l=85):

```
AtomicString ConsumeVariableName(CSSParserTokenStream& stream) {
  stream.ConsumeWhitespace();
  CSSParserToken ident_token = stream.ConsumeIncludingWhitespaceRaw();
  DCHECK_EQ(ident_token.GetType(), kIdentToken);
  return ident_token.Value().ToAtomicString();
}

```

For malformed strings like `env(1)` / `attr(1)`, the first token inside the function is a `kNumberToken`, not an ident. Finally, the resulting invalid `StringView` is then converted to `AtomicString`, which hashes over the bogus span and produces an OOB.

### Bisection

This issue is introduce by the commit <https://chromium-review.googlesource.com/c/chromium/src/+/6734447>

### Reproduction

Download the chrome from <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1591355.zip>

Launch the chrome with the poc.html and the extension:

```
./chrome --load-extension=/path/to/ext --no-sandbox poc.html

```

You would observer the OOB crash in `resolve_values_asan.txt`

### he...@gmail.com (2026-03-05)

Hi, I've fill the `setScopeText` issue as the new one in 490023239.

Many thanks!

### se...@chromium.org (2026-03-05)

Thanks. You will need to Cc me on the bug if I am to do anything about it (security bugs have limited visibility until they have been fixed).

### ch...@google.com (2026-04-07)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline with bisect. Heavily mitigated (sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488270255)*
