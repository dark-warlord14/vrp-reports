# container-overflow in blink::CloseWatcher::WatcherStack::Signal() close_watcher.cc:170:10

| Field | Value |
|-------|-------|
| **Issue ID** | [409911705](https://issues.chromium.org/issues/409911705) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML, IO>Keyboard |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | do...@chromium.org |
| **Created** | 2025-04-11 |
| **Bounty** | $5,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

# NOTE

The issue was discovered by a fuzzer running on ClusterFuzz.  

It requires user interaction (pressing the Escape key) to trigger,  

which prevented ClusterFuzz from reporting it automatically.  

I have provided a minimal Proof of Concept (PoC) that can trigger the problem.  

Locally, it results in a null pointer, while on ClusterFuzz, it triggers a container overflow.  

The exact cause is still under analysis.

<https://clusterfuzz.com/testcase-detail/5308799824887808>

# Reproduction Steps

- Run: `chrome --no-sandbox --user-data-dir=test --enable-logging=stderr poc.html`
- Press the Escape key to trigger the bug

## Root Cause Analysis (RCA) & Bisect

Coming soon

## Attachments

- poc.html (text/html, 1.4 KB)
- poc.html (text/html, 1.4 KB)
- asan.txt (text/plain, 9.0 KB)
- dbg.patch.diff (text/x-diff, 1.3 KB)
- poc.html (text/html, 1.4 KB)
- Video2.webm (video/webm, 2.2 MB)
- many-watchers-in-cancel-event-crash.html (text/html, 522 B)
- deleted (application/octet-stream, 0 B)
- poc_with_memcontrol.html (text/html, 3.5 KB)
- dbg_print_MEMADDRESS_log.patch (text/x-diff, 4.4 KB)

## Timeline

### m....@gmail.com (2025-04-14)

- Apply `dbg.patch.diff`.
- Using the PoC in the attachment, the use-after-poison issue can be reproduced.

```
[14656:3188:0414/153915.530:ERROR:third_party\blink\renderer\core\html\closewatcher\close_watcher.cc:168] Signalbegin===

[14656:3188:0414/153915.532:ERROR:third_party\blink\renderer\core\html\closewatcher\close_watcher.cc:170] Signal , group 2 tname-> CrRendererMain

[14656:3188:0414/153915.532:ERROR:third_party\blink\renderer\core\html\closewatcher\close_watcher.cc:172] Signal , before RequestClose, group.size-> 2 tname-> CrRendererMain

[9452:10968:0414/153915.534:INFO:CONSOLE:42] "watcher.oncancel", source: poc.html (42)
=================================================================
==14656==ERROR: AddressSanitizer: use-after-poison on address 0x7ebc00470e4c at pc 0x7ffe4d32dffd bp 0x00de0f7f90e0 sp 0x00de0f7f9128
READ of size 4 at 0x7ebc00470e4c thread T0
==14656==*** WARNING: Failed to initialize DbgHelp!              ***
==14656==*** Most likely this means that the app is already      ***
==14656==*** using DbgHelp, possibly with incompatible flags.    ***
==14656==*** Due to technical reasons, symbolization might crash ***
==14656==*** or produce wrong results.                           ***
[9452:10968:0414/153916.038:ERROR:chrome\browser\policy\cloud\fm_registration_token_uploader.cc:179] Client is missing for kUser scope
[9452:10968:0414/153916.039:ERROR:chrome\browser\policy\cloud\fm_registration_token_uploader.cc:179] Client is missing for kUser scope
[9452:7416:0414/153916.265:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
    #0 0x7ffe4d32dffc in blink::CloseWatcher::WatcherStack::Signal D:\chromium\src\third_party\blink\renderer\core\html\closewatcher\close_watcher.cc:176
    #1 0x7ffe4d9456e8 in blink::KeyboardEventManager::DefaultEscapeEventHandler D:\chromium\src\third_party\blink\renderer\core\input\keyboard_event_manager.cc:610
    #2 0x7ffe4d94472d in blink::KeyboardEventManager::DefaultKeyboardEventHandler D:\chromium\src\third_party\blink\renderer\core\input\keyboard_event_manager.cc:426
    #3 0x7ffe4fce79a6 in blink::EventDispatcher::DispatchEventPostProcess D:\chromium\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc:414
    #4 0x7ffe4fce524f in blink::EventDispatcher::Dispatch D:\chromium\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc:275
    #5 0x7ffe4fce33e8 in blink::EventDispatcher::DispatchEvent D:\chromium\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc:81
    #6 0x7ffe4d942890 in blink::KeyboardEventManager::KeyEvent D:\chromium\src\third_party\blink\renderer\core\input\keyboard_event_manager.cc:333
    #7 0x7ffe4d16484c in blink::WebFrameWidgetImpl::HandleKeyEvent D:\chromium\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:955
    #8 0x7ffe4d992f0e in blink::WidgetEventHandler::HandleInputEvent D:\chromium\src\third_party\blink\renderer\core\input\widget_event_handler.cc:114
    #9 0x7ffe4d1809ee in blink::WebFrameWidgetImpl::HandleInputEvent D:\chromium\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:3180
    #10 0x7ffe4670855d in blink::WidgetBaseInputHandler::HandleInputEvent D:\chromium\src\third_party\blink\renderer\platform\widget\input\widget_base_input_handler.cc:417
    #11 0x7ffe46720c36 in blink::WidgetInputHandlerManager::HandleInputEvent D:\chromium\src\third_party\blink\renderer\platform\widget\input\widget_input_handler_manager.cc:423
    #12 0x7ffe466e7791 in blink::MainThreadEventQueue::HandleEventOnMainThread D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:808
    #13 0x7ffe466eb69d in blink::QueuedWebInputEvent::Dispatch D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:194
    #14 0x7ffe466e5633 in blink::MainThreadEventQueue::DispatchEvents D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:571
    #15 0x7ffe466f299c in base::internal::Invoker<base::internal::FunctorTraits<void (MainThreadEventQueue::*&&)(),blink::MainThreadEventQueue *&&>,base::internal::BindState<1,1,0,void (MainThreadEventQueue::*)(),scoped_refptr<blink::MainThreadEventQueue> >,void ()>::RunOnce D:\chromium\src\base\functional\bind_internal.h:973
    #16 0x7fff3174a623 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:209
    #17 0x7fff317d5b19 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:456
    #18 0x7fff317d49bf in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:330
    #19 0x7fff315bc6f7 in base::MessagePumpDefault::Run D:\chromium\src\base\message_loop\message_pump_default.cc:42
    #20 0x7fff317d7891 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run D:\chromium\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:629
    #21 0x7fff316a91ae in base::RunLoop::Run D:\chromium\src\base\run_loop.cc:134
    #22 0x7ffe818938a0 in content::RendererMain D:\chromium\src\content\renderer\renderer_main.cc:369
    #23 0x7ffe81d60766 in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content_main_runner_impl.cc:781
    #24 0x7ffe81d62f9a in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content_main_runner_impl.cc:1155
    #25 0x7ffe81d5652b in content::RunContentProcess D:\chromium\src\content\app\content_main.cc:359
    #26 0x7ffe81d570b0 in content::ContentMain D:\chromium\src\content\app\content_main.cc:372
    #27 0x7ffe895016ba in ChromeMain D:\chromium\src\chrome\app\chrome_main.cc:222
    #28 0x7ff7e20d3de9 in MainDllLoader::Launch D:\chromium\src\chrome\app\main_dll_loader_win.cc:201
    #29 0x7ff7e20d1be9 in main D:\chromium\src\chrome\app\chrome_exe_main_win.cc:352
    #30 0x7ff7e227e3b3 in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #31 0x7fff890ae8d6 in BaseThreadInitThunk+0x16 (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #32 0x7fff8b1dbf6b in RtlUserThreadStart+0x2b (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800bbf6b)

Address 0x7ebc00470e4c is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison D:\chromium\src\third_party\blink\renderer\core\html\closewatcher\close_watcher.cc:176 in blink::CloseWatcher::WatcherStack::Signal
Shadow bytes around the buggy address:
  0x7ebc00470b80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ebc00470c00: 00 00 00 00 00 f7 f7 f7 f7 00 00 00 00 f7 f7 f7
  0x7ebc00470c80: f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00 00 00
  0x7ebc00470d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ebc00470d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7ebc00470e00: 00 00 00 00 00 00 00 00 00[f7]00 00 00 00 00 00
  0x7ebc00470e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ebc00470f00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ebc00470f80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ebc00471000: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7ebc00471080: 00 00 00 f7 f7 00 00 00 00 00 00 00 00 f7 f7 f7
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

==14656==ADDITIONAL INFO

==14656==Note: Please include this section with the ASan report.
Task trace:
    #0 0x7ffe466e34a0 in blink::MainThreadEventQueue::QueueEvent D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:738
    #1 0x7fff62f6e3af in mojo::SimpleWatcher::Context::Notify D:\chromium\src\mojo\public\cpp\system\simple_watcher.cc:102


Command line: `"D:\chromium\src\out\asan\chrome.exe" --type=renderer --user-data-dir=test --no-pre-read-main-dll --no-sandbox --js-flags="-expose-gc --allow-natives-syntax" --video-capture-use-gpu-memory-buffer --lang=en-US --device-scale-factor=2 --num-raster-threads=4 --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1743991026287498 --launch-time-ticks=625327425289 --metrics-shmem-handle=3384,i,13941371420173574604,2756554228562263361,2097152 --field-trial-handle=1880,i,16202755530615160075,16493414734575409601,262144 --variations-seed-version --enable-logging=stderr --mojo-platform-channel-handle=3392 /prefetch:1`


==14656==END OF ADDITIONAL INFO
==14656==ABORTING

```

### m....@gmail.com (2025-04-14)

# RCA

There are two issues with `CloseWatcher::RequestClose`:

1. It can lead to iterator invalidation through the sequence `close->destroy->Remove`.
2. It invokes user-defined `CloseWatcher` callbacks (`oncancel` or `onclose`), where user JavaScript code might create new `CloseWatcher` instances, potentially causing iterator invalidation.

---

Here is the stack trace of `RequestClose` calling user-defined JavaScript:

```
base::debug::CollectStackTrace [0x00007FFF31204DAA+58] (D:\chromium\src\base\debug\stack_trace_win.cc:326)
base::debug::StackTrace::StackTrace [0x00007FFF311B47B6+230] (D:\chromium\src\base\debug\stack_trace.cc:250)
blink::LocalDOMWindow::alert [0x00007FFE4C21457D+717] (D:\chromium\src\third_party\blink\renderer\core\frame\local_dom_window.cc:1415)
blink::`anonymous namespace'::v8_window::AlertOperationCallback [0x00007FFE3E7112DA+2202] (D:\chromium\src\out\asan\gen\third_party\blink\renderer\bindings\modules\v8\v8_window.cc:15202)
Builtins_CallApiCallbackGeneric [0x00007FFE5B3575C5+197]
Builtins_InterpreterEntryTrampoline [0x00007FFE5B3557B5+309]
Builtins_JSEntryTrampoline [0x00007FFE5B35329C+92]
Builtins_JSEntry [0x00007FFE5B352DFF+255]
v8::internal::`anonymous namespace'::Invoke [0x00007FFE569225CD+6013] (D:\chromium\src\v8\src\execution\execution.cc:440)
v8::internal::Execution::Call [0x00007FFE56920D7E+462] (D:\chromium\src\v8\src\execution\execution.cc:530)
v8::Function::Call [0x00007FFE5626628A+1978] (D:\chromium\src\v8\src\api\api.cc:5427)
blink::V8ScriptRunner::CallFunction [0x00007FFE4AAC8C02+1778] (D:\chromium\src\third_party\blink\renderer\bindings\core\v8\v8_script_runner.cc:888)
blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase,2,0>::Call [0x00007FFE4A8D2A79+713] (D:\chromium\src\third_party\blink\renderer\bindings\core\v8\callback_invoke_helper.cc:166)
blink::V8EventHandlerNonNull::InvokeWithoutRunnabilityCheck [0x00007FFE4F61AA44+1380] (D:\chromium\src\out\asan\gen\third_party\blink\renderer\bindings\core\v8\v8_event_handler_non_null.cc:183)
blink::JSEventHandler::InvokeInternal [0x00007FFE4A8FF634+3460] (D:\chromium\src\third_party\blink\renderer\bindings\core\v8\js_event_handler.cc:134)
blink::JSBasedEventListener::Invoke [0x00007FFE4A8FD6B5+1797] (D:\chromium\src\third_party\blink\renderer\bindings\core\v8\js_based_event_listener.cc:160)
blink::EventTarget::FireEventListeners [0x00007FFE4B8D7565+4437] (D:\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc:1088)
blink::EventTarget::FireEventListeners [0x00007FFE4B8D56AD+1357] (D:\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc:1009)
blink::EventTarget::DispatchEventInternal [0x00007FFE4B8D50E0+128] (D:\chromium\src\third_party\blink\renderer\core\dom\events\event_target.cc:905)
blink::CloseWatcher::RequestClose [0x00007FFE4C65EB62+1010] (D:\chromium\src\third_party\blink\renderer\core\html\closewatcher\close_watcher.cc:262)
blink::CloseWatcher::WatcherStack::Signal [0x00007FFE4C65E394+1860] (D:\chromium\src\third_party\blink\renderer\core\html\closewatcher\close_watcher.cc:173)
blink::KeyboardEventManager::DefaultEscapeEventHandler [0x00007FFE4CC75E49+1513] (D:\chromium\src\third_party\blink\renderer\core\input\keyboard_event_manager.cc:610)
blink::KeyboardEventManager::DefaultKeyboardEventHandler [0x00007FFE4CC74E8E+2622] (D:\chromium\src\third_party\blink\renderer\core\input\keyboard_event_manager.cc:432)
blink::EventDispatcher::DispatchEventPostProcess [0x00007FFE4F018107+1639] (D:\chromium\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc:414)
blink::EventDispatcher::Dispatch [0x00007FFE4F0159B0+3280] (D:\chromium\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc:275)
blink::EventDispatcher::DispatchEvent [0x00007FFE4F013B49+489] (D:\chromium\src\third_party\blink\renderer\core\dom\events\event_dispatcher.cc:81)
blink::KeyboardEventManager::KeyEvent [0x00007FFE4CC72FF1+5409] (D:\chromium\src\third_party\blink\renderer\core\input\keyboard_event_manager.cc:333)
blink::WebFrameWidgetImpl::HandleKeyEvent [0x00007FFE4C494CAD+957] (D:\chromium\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:955)
blink::WidgetEventHandler::HandleInputEvent [0x00007FFE4CCC366F+1567] (D:\chromium\src\third_party\blink\renderer\core\input\widget_event_handler.cc:114)
blink::WebFrameWidgetImpl::HandleInputEvent [0x00007FFE4C4B0E4F+2495] (D:\chromium\src\third_party\blink\renderer\core\frame\web_frame_widget_impl.cc:3180)
blink::WidgetBaseInputHandler::HandleInputEvent [0x00007FFE45A3855E+3294] (D:\chromium\src\third_party\blink\renderer\platform\widget\input\widget_base_input_handler.cc:417)
blink::WidgetInputHandlerManager::HandleInputEvent [0x00007FFE45A50C37+567] (D:\chromium\src\third_party\blink\renderer\platform\widget\input\widget_input_handler_manager.cc:423)
blink::MainThreadEventQueue::HandleEventOnMainThread [0x00007FFE45A17792+578] (D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:808)
blink::QueuedWebInputEvent::Dispatch [0x00007FFE45A1B69E+1166] (D:\chromium\src\third_party\blink\renderer\platform\widget\input\main_thread_event_queue.cc:194)

```
# ref

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/closewatcher/close_watcher.cc;drc=5e01cdc5efe08fe9bedf7cc1523b8094b626559d;l=170>

### m....@gmail.com (2025-04-14)

# Bisect

<https://chromium-review.googlesource.com/c/chromium/src/+/5465306>

### m....@gmail.com (2025-04-14)

The attachment includes a PoC (Proof of Concept) that can stably trigger the issue in a precompiled Chromium build, along with a demonstration video.
gs://chromium-browser-asan/win32-release\_x64/asan-win32-release\_x64-1441351.zip

### fl...@google.com (2025-04-14)

This reproduces on my machine. Assigning severity S1 because of use-after-poison in blink.

domenic@, would you mind taking a look, since it looks like it's bisected to a CL you're familiar with? (Feel free to reassign if there's someone better.)

### do...@chromium.org (2025-04-15)

Adding +jarhar who has been more active than me in this code recently. I will still keep it assigned to me though as a backstop and will try to get to it this week if Joey cannot.

### ch...@google.com (2025-04-15)

Setting milestone because of s0/s1 severity.

### do...@chromium.org (2025-04-16)

Tentative conclusion: a quick fix that should work is to clone the group before iterating over it. I'll try patching that in and seeing if it works as expected.

Another fix, which might also help with the simple (sync) part of [issue 363225474](https://issues.chromium.org/issues/363225474), is to change the "establish a close watcher" logic to behave differently while close watcher callbacks are running. E.g., by always grouping. I'm unsure yet if that's better and will investigate a bit more.

### do...@chromium.org (2025-04-16)

I have a draft fix at <https://chromium-review.googlesource.com/c/chromium/src/+/6458381>.

### do...@chromium.org (2025-04-17)

I'm attaching the failing-before, passing-after web platform test that I plan to commit after the CL above has made its way to stable.

### do...@chromium.org (2025-04-21)

This was fixed by <https://chromium-review.googlesource.com/c/chromium/src/+/6458381> . flowerhack@ tells me that the the security team will handle back-merges as necessary. Let me know if there is more for me to do!

### ch...@google.com (2025-04-21)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-04-21)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M134. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [134, 135, 136].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pg...@google.com (2025-04-21)

Fix landed April 17 - I see a few watcher related crashes, but none of their stacktraces nor their crash history appear to make crash relevant to this fix in all canary data available.

Merge approved for M136 - please merge to branch 7103 by 9am MTV time Tuesday April 22!

### sr...@google.com (2025-04-21)

Please complete your merges before EOD today April 21, 2025 PST so they can be part of stable RC build ( i will cutting the RC tomorrow morning PST) 

### do...@chromium.org (2025-04-22)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/6458381>
2. Yes
3. No
4. No
5. No

Who is responsible for this merge? I was told the security rotation team would do it, and I don't want to step on their toes.

### pg...@google.com (2025-04-22)

Hi Domenic! thanks for checking - the merge should be done by the assignee of the bug and the security team comes to do the approvals for backmerging at all (based on severity, impact, scheduling, etc)

### go...@google.com (2025-04-22)

Put M136 merge in CQ - https://chromium-review.googlesource.com/c/chromium/src/+/6478663 as domenic@ is in TOK and we're cutting M136 Early Stable RC today. 

@pg...@google.com & @sr...@google.com as FYI

### go...@google.com (2025-04-22)

M136 merge landed - https://chromium-review.googlesource.com/c/chromium/src/+/6478663

### pe...@google.com (2025-04-22)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### do...@chromium.org (2025-04-23)

Thank you all for taking care of the merge, and sorry for not understanding the procedure.

Regarding [comment #21](https://issues.chromium.org/issues/409911705#comment21):

1. No. This issue was introduced in Chrome 126. (<https://chromiumdash.appspot.com/commit/ea9a37ac43f5ad8a670ed318488b42bdb8fa0d73>)
2. No. This issue is related to a change merged in Chrome 126.

### am...@chromium.org (2025-04-23)

M136 is being promoted to Stable next week, there are no further planned releases of M135 Stable or M134 Extended

### m....@gmail.com (2025-04-25)

The attachment demonstrates using DOMRect object data to forge a CloseWatcher object, but does not implement arbitrary address write.

# Goal

1. Utilize an object of the same type, `HeapVector<Member<T>>`, as a placeholder. The content of `T` should preferably be controllable at the JS level. After occupying the memory, a `T` object can be provided to forge a `CloseWatcher` object for code execution. Alternatively, setting `CloseWatcher`'s `state_ = State::kClosed` can corrupt the `T` object, creating an opportunity for code execution.
2. Use large objects to achieve more stable memory occupation. This is easily achievable by continuously adding enough elements to `HeapVector`, causing its buffer to be allocated in large pages.

# Implementation

- Use `EditContext::characterBounds[1]` to create a `HeapVector<Member<DOMRect>>` of controllable size.
- The content of `DOMRect` is controllable at the JS level.
- Use `watcher->RequestClose` to callback into user JS code, where new `CloseWatcher` objects are added, causing the previous buffer to be freed.
- Calling `characterBounds` to create `HeapVector<Member<DOMRect>>` can stably occupy the memory freed in the previous step.

# Note

This PoC only demonstrates replacing the buffer of a `HeapVector<Member<CloseWatcher>>` object with user-controllable content[2]. Arbitrary write functionality has not yet been implemented.`

```
[1]
const HeapVector<Member<DOMRect>> EditContext::characterBounds() {
  HeapVector<Member<DOMRect>> dom_rects;
  std::ranges::transform(
      character_bounds_, std::back_inserter(dom_rects), [](const auto& bound) {
        return DOMRect::Create(bound.x(), bound.y(), bound.width(),
                               bound.height());
      });
  return dom_rects;
}

```
```
[2]
0:000> dt this
Local var @ 0x401fbfa6d0 Type blink::CloseWatcher*
0x000007bc`022e3c98 
   +0x000 __VFN_table : 0x00007ff9`1e28c170 
   +0x008 wrapper_         : v8::TracedReference<v8::Object>
   =00007ff9`1e58d8d8 wrapper_type_info_ : 0x00007ff9`1e58d8a0 blink::WrapperTypeInfo
   +0x010 data_            : cppgc::internal::BasicMember<blink::EventTargetData,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer>
   +0x018 __VFN_table : 0x41414141`00000000 
   +0x020 execution_context_ : cppgc::internal::BasicMember<blink::ExecutionContext,cppgc::internal::WeakMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer>
   =00007ff9`1e57ce88 wrapper_type_info_ : 0x00007ff9`1e57ce50 blink::WrapperTypeInfo
   +0x028 state_           : 0x80000000 (No matching name)
   +0x02c dispatching_cancel_ : 41
   +0x02d enabled_         : 41
   +0x030 abort_handle_    : cppgc::internal::BasicMember<blink::AbortSignal::AlgorithmHandle,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer>
   +0x034 stack_           : cppgc::internal::BasicMember<blink::CloseWatcher::WatcherStack,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer>
0:000> dd 0x000007bc`022e3c98
000007bc`022e3c98  1e28c170 00007ff9 22b758d8 00000193
000007bc`022e3ca8  00000000 41414141 00000000 41414141
000007bc`022e3cb8  80000000 41414141 80000000 41414141
000007bc`022e3cc8  00000000 000f0271 1e28c170 00007ff9

```

### sp...@google.com (2025-04-25)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$3,000 for report of mildly mitigated memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus + $1,000 good report bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2025-04-28)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-04-28)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6483547
2. Medium - There were a few conflicts.
3. 136
4. Yes, according to the comment #22, this bug was introduced in M126.

### ch...@google.com (2025-07-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> $3,000 for report of mildly mitigated memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus + $1,000 good report bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/409911705)*
