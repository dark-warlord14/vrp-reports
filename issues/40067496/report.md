# Security: Memory corruption due to HeapVector iterator invalidation

| Field | Value |
|-------|-------|
| **Issue ID** | [40067496](https://issues.chromium.org/issues/40067496) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Fuchsia, Linux, Mac, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | dt...@chromium.org |
| **Created** | 2023-07-16 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: stable + dev

**REPRODUCTION CASE**

1. chrome poc.html
2. open devtools and click Event Listeners

#RCA  

Same as <https://bugs.chromium.org/p/chromium/issues/detail?id=1429201>

In function InspectorDOMDebuggerAgent::CollectEventListeners, it iterates all registered fetch event listeners and calls JSEventListener::GetEffectiveFunction to get the listener function [1]. JSEventListener::GetEffectiveFunction may calls v8::Object::Get to retrieve the "handleEvent" property of the listener object [2], which may executes user defined JS code and invalidates the iterator by removing fetch event listeners.

```
void InspectorDOMDebuggerAgent::CollectEventListeners(  
    v8::Isolate\* isolate,  
    EventTarget\* target,  
    v8::Local<v8::Value> target_wrapper,  
    Node\* target_node,  
    bool report_for_all_contexts,  
    V8EventListenerInfoList\* event_information) {  
  if (!target->GetExecutionContext())  
    return;  
//CUT  
  Vector<AtomicString> event_types = target->EventTypes();  
  for (AtomicString& type : event_types) {  
    EventListenerVector\* listeners = target->GetEventListeners(type);  
    if (!listeners)  
      continue;  
    for (auto& registered_event_listener : \*listeners) {  
      EventListener\* event_listener = registered_event_listener->Callback();  
  
      v8::Local<v8::Value> effective_function =  
          v8_event_listener->GetEffectiveFunction(\*target); [1]  
            
v8::Local<v8::Value> JSEventListener::GetEffectiveFunction(  
    EventTarget& target) {  
  // skip  
    if (v8_listener.As<v8::Object>()  
            ->Get(isolate->GetCurrentContext(),  
                  V8AtomicString(isolate, "handleEvent"))    // ===> [2]  
            .ToLocal(&property) &&  
        property->IsFunction()) {  
      return GetBoundFunction(property.As<v8::Function>());  
    }  
  }            

```

[1]  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/core/inspector/inspector_dom_debugger_agent.cc;drc=54f2184c5bf221c0efaabdbe549f938066aab00f;l=129>  

[2]  

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/core/v8/js_event_listener.cc;drc=047c7dc4ee1ce908d7fea38ca063fa2f80f92c77;l=33>

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 566 B)
- [asan.txt](attachments/asan.txt) (text/plain, 5.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 661 B)
- [asan2.txt](attachments/asan2.txt) (text/plain, 6.8 KB)

## Timeline

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-07-16)

"Adjust the Poc code implementation to make the security issue more obvious (NullDef->UAF)."
```
=================================================================
==26316==ERROR: AddressSanitizer: use-after-poison on address 0x7ef9001d2b48 at pc 0x7fff50979b0c bp 0x00c2ab5f9820 sp 0x00c2ab5f9868
READ of size 4 at 0x7ef9001d2b48 thread T0
==26316==*** WARNING: Failed to initialize DbgHelp!              ***
==26316==*** Most likely this means that the app is already      ***
==26316==*** using DbgHelp, possibly with incompatible flags.    ***
==26316==*** Due to technical reasons, symbolization might crash ***
==26316==*** or produce wrong results.                           ***
    #0 0x7fff50979b0b in blink::InspectorDOMDebuggerAgent::CollectEventListeners D:\chromium\src\third_party\blink\renderer\core\inspector\inspector_dom_debugger_agent.cc:142
    #1 0x7fff5097a16d in blink::InspectorDOMDebuggerAgent::EventListenersInfoForTarget D:\chromium\src\third_party\blink\renderer\core\inspector\inspector_dom_debugger_agent.cc:194
    #2 0x7fff50989ac9 in blink::InspectorDOMDebuggerAgent::getEventListeners D:\chromium\src\third_party\blink\renderer\core\inspector\inspector_dom_debugger_agent.cc:464
    #3 0x7fff5493b92e in blink::protocol::DOMDebugger::DomainDispatcherImpl::getEventListeners D:\chromium\src\out\use\gen\third_party\blink\renderer\core\inspector\protocol\dom_debugger.cc:205
    #4 0x7fff60efdbb9 in crdtp::UberDispatcher::DispatchResult::Run D:\chromium\src\third_party\inspector_protocol\crdtp\dispatch.cc:511
    #5 0x7fff507e601a in blink::DevToolsSession::DispatchProtocolCommandImpl D:\chromium\src\third_party\blink\renderer\core\inspector\devtools_session.cc:263
    #6 0x7fff507e5759 in blink::DevToolsSession::DispatchProtocolCommand D:\chromium\src\third_party\blink\renderer\core\inspector\devtools_session.cc:228
    #7 0x7fff4c1bf179 in blink::mojom::blink::DevToolsSessionStubDispatch::Accept D:\chromium\src\out\use\gen\third_party\blink\public\mojom\devtools\devtools_agent.mojom-blink.cc:1321
    #8 0x7fffcb7b61db in mojo::InterfaceEndpointClient::HandleValidatedMessage D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:1016
    #9 0x7fffcb7cc786 in mojo::MessageDispatcher::Accept D:\chromium\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43
    #10 0x7fffcb7bbe74 in mojo::InterfaceEndpointClient::HandleIncomingMessage D:\chromium\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:701
    #11 0x7fff9b571f61 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread D:\chromium\src\ipc\ipc_mojo_bootstrap.cc:1075
    #12 0x7fff9b567fd0 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce D:\chromium\src\base\functional\bind_internal.h:944
    #13 0x7fff943b5081 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:201
    #14 0x7fff94421086 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:480
    #15 0x7fff9441fe2f in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:345
    #16 0x7fff9424c7f3 in base::MessagePumpDefault::Run D:\chromium\src\base\message_loop\message_pump_default.cc:40
    #17 0x7fff944238d5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:645
    #18 0x7fff9431b317 in base::RunLoop::Run D:\chromium\src\base\run_loop.cc:134
    #19 0x7fff7b808c01 in content::RendererMain D:\chromium\src\content\renderer\renderer_main.cc:339
    #20 0x7fff7bdfadc9 in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content_main_runner_impl.cc:745
    #21 0x7fff7bdfde47 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content_main_runner_impl.cc:1118
    #22 0x7fff7bdf8471 in content::RunContentProcess D:\chromium\src\content\app\content_main.cc:326
    #23 0x7fff7bdf909e in content::ContentMain D:\chromium\src\content\app\content_main.cc:343
    #24 0x7fff81141738 in ChromeMain D:\chromium\src\chrome\app\chrome_main.cc:187
    #25 0x7ff692dc5a25 in MainDllLoader::Launch D:\chromium\src\chrome\app\main_dll_loader_win.cc:166
    #26 0x7ff692dc28ee in main D:\chromium\src\chrome\app\chrome_exe_main_win.cc:390
    #27 0x7ff692f86ef3 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #28 0x7ffff2c826ac in BaseThreadInitThunk+0x1c (C:\Windows\System32\KERNEL32.DLL+0x1800126ac)
    #29 0x7ffff350a9f7 in RtlUserThreadStart+0x27 (C:\Windows\SYSTEM32\ntdll.dll+0x18005a9f7)

Address 0x7ef9001d2b48 is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison D:\chromium\src\third_party\blink\renderer\core\inspector\inspector_dom_debugger_agent.cc:142 in blink::InspectorDOMDebuggerAgent::CollectEventListeners
Shadow bytes around the buggy address:
  0x7ef9001d2880: f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00 00 00
  0x7ef9001d2900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ef9001d2980: 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7
  0x7ef9001d2a00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef9001d2a80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x7ef9001d2b00: f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7
  0x7ef9001d2b80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef9001d2c00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef9001d2c80: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef9001d2d00: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ef9001d2d80: f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00
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

==26316==ADDITIONAL INFO

==26316==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7fff9b5661fc in IPC::`anonymous namespace'::ChannelAssociatedGroupController::Accept D:\chromium\src\ipc\ipc_mojo_bootstrap.cc:1017


==26316==END OF ADDITIONAL INFO
==26316==ABORTING
```

### m....@gmail.com (2023-07-16)

bisect:This was introduced in
https://chromium-review.googlesource.com/c/chromium/src/+/4623037

### bo...@chromium.org (2023-07-16)

Thanks for the report. Confirming I can reproduce on M117. Assigning medium severity due to requirement to trigger via DevTools + detailed user interaction requirement. 

[Monorail components: Platform>DevTools]

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-07-17)

[Comment Deleted]

### m....@gmail.com (2023-07-17)

My fix proposal

Prevent iterator invalidation during user js callback
```
diff --git a/third_party/blink/renderer/core/inspector/inspector_dom_debugger_agent.cc b/third_party/blink/renderer/core/inspector/inspector_dom_debugger_agent.cc
index 1468126c9057..9bb222f1438b 100644
--- a/third_party/blink/renderer/core/inspector/inspector_dom_debugger_agent.cc
+++ b/third_party/blink/renderer/core/inspector/inspector_dom_debugger_agent.cc
@@ -110,7 +110,11 @@ void InspectorDOMDebuggerAgent::CollectEventListeners(
     EventListenerVector* listeners = target->GetEventListeners(type);
     if (!listeners)
       continue;
-    for (auto& registered_event_listener : *listeners) {
+    
+    //GetEffectiveFunction may call user defined js callback cause iterating invaild
+    //make a copy of listeners avoid UAF 
+    EventListenerVector _listeners = *listeners;
+    for (auto& registered_event_listener : _listeners) {
       EventListener* event_listener = registered_event_listener->Callback();
       JSBasedEventListener* v8_event_listener =
           DynamicTo<JSBasedEventListener>(event_listener);
```

### bm...@chromium.org (2023-07-17)

[Empty comment from Monorail migration]

### dt...@chromium.org (2023-07-17)

Fix posted here: https://chromium-review.googlesource.com/c/chromium/src/+/4690243

### [Deleted User] (2023-07-17)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e5befc1404c709ca4dd59830fe8310fb4f05452e

commit e5befc1404c709ca4dd59830fe8310fb4f05452e
Author: Dave Tapuska <dtapuska@chromium.org>
Date: Tue Jul 18 14:19:55 2023

Clone the EventListenerVector before iterating on it

Iterating on a EventListenerVector while calling operations
that can mutate it can invalidate the iterator.

Bug: 1465193
Change-Id: I259a8b4ee5831accbffc12750b91ea36ca250fe6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4690243
Commit-Queue: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1171730}

[modify] https://crrev.com/e5befc1404c709ca4dd59830fe8310fb4f05452e/third_party/blink/renderer/core/inspector/inspector_dom_debugger_agent.cc


### dt...@chromium.org (2023-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-03)

Congratulations! The VRP Panel has decided to award you $3,000 for this report of a mildly mitigated renderer memory corruption + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-11)

Not requesting merge to dev (M117) because latest trunk commit (1171730) appears to be prior to dev branch point (1181205). If this is incorrect, please replace the Merge-NA-117 label with Merge-Request-117. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M117. Please go ahead and merge the CL to branch 5938 (refs/branch-heads/5938) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2023-08-14)

Your Cl has been already approved for M117 Branch and we are cutting M117 Beta RC tomorrow i.e., Aug-15th, so request  you to get the CL's cherry pick before Noon tomorrow so that we get maximum Beta coverage for the CL please.



### [Deleted User] (2023-08-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-08-16)

fix landed in 117, no merge needed 

### [Deleted User] (2023-10-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1465193?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067496)*
