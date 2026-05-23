# SUMMARY: AddressSanitizer: heap-use-after-free (Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1958102f) in blink::ComputedAccessibleNode::checked()

| Field | Value |
|-------|-------|
| **Issue ID** | [40055854](https://issues.chromium.org/issues/40055854) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | dm...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2021-05-14 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0

Steps to reproduce the problem:
1. Download file "heap-uaf-in-aom.html"
2. Open Chromium 92.0.4491.0 (Developer Build) (x86_64)
3. Enable Chromium flag: chrome://flags/#enable-experimental-web-platform-features
4. Relaunch Chromium and open downloaded file "heap-uaf-in-aom.html".
5. Click link "Click me"
6. Wait ~1s until new window will be closed and browser will be crashed with UaF.

What is the expected behavior?
No crash with heap-uaf. Validation if tree exists.

What went wrong?
Short description: 
I use following scenario: Open new window via click -> Get ComputedAccessibleNode of new DOM element -> Wait until window closed and DOM tree destroyed -> Access property of ComputedAccessibleNode, which call method on non-existent "tree_".

Looks like this issue triggered because code doesn't validate if tree_ exists and is available.

ASAN Report:
==42409==ERROR: AddressSanitizer: heap-use-after-free on address 0x616000057980 at pc 0x00012b363d85 bp 0x7ffee830b5f0 sp 0x7ffee830b5e8
READ of size 8 at 0x616000057980 thread T0
==42409==WARNING: failed to spawn external symbolizer (errno: 9)
==42409==WARNING: failed to spawn external symbolizer (errno: 9)
==42409==WARNING: failed to spawn external symbolizer (errno: 9)
==42409==WARNING: failed to spawn external symbolizer (errno: 9)
==42409==WARNING: failed to spawn external symbolizer (errno: 9)
==42409==WARNING: Failed to use and restart external symbolizer!
    #0 0x12b363d84 in blink::ComputedAccessibleNode::parent() const+0x214 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x19581d84)
    #1 0x12f36bf69 in blink::(anonymous namespace)::v8_computed_accessible_node::ParentAttributeGetCallback(v8::FunctionCallbackInfo<v8::Value> const&)+0x109 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1d589f69)
    #2 0x7ee30004b84d  (<unknown module>)
    #3 0x7ee300052b23  (<unknown module>)
    #4 0x7ee30013a7fd  (<unknown module>)
    #5 0x7ee300049640  (<unknown module>)
    #6 0x7ee3000476fa  (<unknown module>)
    #7 0x7ee300047482  (<unknown module>)
    #8 0x119cae19c in v8::internal::(anonymous namespace)::Invoke(v8::internal::Isolate*, v8::internal::(anonymous namespace)::InvokeParams const&)+0xdcc (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x7ecc19c)
    #9 0x119cad15a in v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*)+0x35a (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x7ecb15a)
    #10 0x119907a90 in v8::Function::Call(v8::Local<v8::Context>, v8::Local<v8::Value>, int, v8::Local<v8::Value>*)+0x4c0 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x7b25a90)
    #11 0x12e53f104 in blink::V8ScriptRunner::CallFunction(v8::Local<v8::Function>, blink::ExecutionContext*, v8::Local<v8::Value>, int, v8::Local<v8::Value>*, v8::Isolate*)+0x764 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1c75d104)
    #12 0x12e44587a in blink::bindings::CallbackInvokeHelper<blink::CallbackFunctionBase, (blink::bindings::CallbackInvokeHelperMode)0>::Call(int, v8::Local<v8::Value>*)+0xda (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1c66387a)
    #13 0x12f2de34c in blink::V8Function::Invoke(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&)+0x49c (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1d4fc34c)
    #14 0x12f2ded05 in blink::V8Function::InvokeAndReportException(blink::bindings::V8ValueOrScriptWrappableAdapter, blink::HeapVector<blink::ScriptValue, 0u> const&)+0x155 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1d4fcd05)
    #15 0x12e49c8e8 in blink::ScheduledAction::Execute(blink::ExecutionContext*)+0x328 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1c6ba8e8)
    #16 0x12c251796 in blink::DOMTimer::Fired()+0x496 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1a46f796)
    #17 0x12ed929e2 in blink::TimerBase::RunInternal()+0xa2 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1cfb09e2)
    #18 0x12dfb359f in base::internal::Invoker<base::internal::BindState<void (blink::TimerBase::*)(), base::WeakPtr<blink::TimerBase> >, void ()>::RunOnce(base::internal::BindStateBase*)+0x1df (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1c1d159f)
    #19 0x11dd35df9 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*)+0x3e9 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf53df9)
    #20 0x11dd74042 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)+0x502 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf92042)
    #21 0x11dd73827 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x1f7 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf91827)
    #22 0x11de631b8 in invocation function for block in base::MessagePumpCFRunLoopBase::RunDelayedWorkTimer(__CFRunLoopTimer*, void*)+0xe8 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc0811b8)
    #23 0x11de50289 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc06e289)
    #24 0x11de61975 in base::MessagePumpCFRunLoopBase::RunDelayedWorkTimer(__CFRunLoopTimer*, void*)+0x175 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc07f975)
    #25 0x7fff204c090c in __CFRUNLOOP_IS_CALLING_OUT_TO_A_TIMER_CALLBACK_FUNCTION__+0x13 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x9a90c)
    #26 0x7fff204c03e7 in __CFRunLoopDoTimer+0x399 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x9a3e7)
    #27 0x7fff204bff41 in __CFRunLoopDoTimers+0x132 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x99f41)
    #28 0x7fff204a657e in __CFRunLoopRun+0x7d7 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x8057e)
    #29 0x7fff204a56cd in CFRunLoopRunSpecific+0x232 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7f6cd)
    #30 0x7fff21232fa0 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd3 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:x86_64+0x5ffa0)
    #31 0x11de647d0 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0x100 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc0827d0)
    #32 0x11de609d8 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x208 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc07e9d8)
    #33 0x11dd752a5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x2a5 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf932a5)
    #34 0x11dcb2aee in base::RunLoop::Run(base::Location const&)+0x46e (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbed0aee)
    #35 0x1324b5370 in content::RendererMain(content::MainFunctionParams const&)+0x9e0 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x206d3370)
    #36 0x11da873cd in content::ContentMainRunnerImpl::Run(bool)+0x3fd (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbca53cd)
    #37 0x11da84716 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*)+0x15f6 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbca2716)
    #38 0x11da84d2c in content::ContentMain(content::ContentMainParams const&)+0x1c (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbca2d2c)
    #39 0x111dea075 in ChromeMain+0x225 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x8075)
    #40 0x1078f0b78 in main+0x2b8 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):x86_64+0x100002b78)
    #41 0x7fff203ca620 in start+0x0 (/usr/lib/system/libdyld.dylib:x86_64+0x15620)

0x616000057980 is located 0 bytes inside of 600-byte region [0x616000057980,0x616000057bd8)
freed by thread T0 here:
    #0 0x107b2d0d9 in __asan_memmove+0x1d19 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x450d9)
    #1 0x132411186 in content::RenderFrameImpl::~RenderFrameImpl()+0x1076 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x2062f186)
    #2 0x13241266d in content::RenderFrameImpl::~RenderFrameImpl()+0xd (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x2063066d)
    #3 0x132438a4c in content::RenderFrameImpl::FrameDetached()+0x6cc (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x20656a4c)
    #4 0x12c4910df in blink::LocalFrameClientImpl::Detached(blink::FrameDetachType)+0x1cf (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1a6af0df)
    #5 0x12c27c2a4 in blink::Frame::Detach(blink::FrameDetachType)+0x384 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1a49a2a4)
    #6 0x12db2194f in blink::Page::WillBeDestroyed()+0xdf (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1bd3f94f)
    #7 0x12fcfc941 in blink::WebViewImpl::Close()+0x281 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1df1a941)
    #8 0x1324a5e02 in content::RenderViewImpl::Destroy()+0x82 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x206c3e02)
    #9 0x11f4f45a3 in base::internal::Invoker<base::internal::BindState<base::internal::ThenHelper<base::OnceCallback<void ()>, base::OnceCallback<void ()> >::CreateTrampoline()::'lambda'(base::OnceCallback<void ()>, base::OnceCallback<void ()>), base::OnceCallback<void ()>, base::OnceCallback<void ()> >, void ()>::RunOnce(base::internal::BindStateBase*)+0x193 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xd7125a3)
    #10 0x11dd35df9 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*)+0x3e9 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf53df9)
    #11 0x11dd74042 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)+0x502 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf92042)
    #12 0x11dd73827 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x1f7 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf91827)
    #13 0x11de63408 in invocation function for block in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe8 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc081408)
    #14 0x11de50289 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc06e289)
    #15 0x11de61bb5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x175 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc07fbb5)
    #16 0x7fff204a7a0b in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x10 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x81a0b)
    #17 0x7fff204a7973 in __CFRunLoopDoSource0+0xb3 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x81973)
    #18 0x7fff204a76ee in __CFRunLoopDoSources0+0xf7 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x816ee)
    #19 0x7fff204a6120 in __CFRunLoopRun+0x379 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x80120)
    #20 0x7fff204a56cd in CFRunLoopRunSpecific+0x232 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7f6cd)
    #21 0x7fff21232fa0 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd3 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:x86_64+0x5ffa0)
    #22 0x11de647d0 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0x100 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc0827d0)
    #23 0x11de609d8 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x208 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc07e9d8)
    #24 0x11dd752a5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x2a5 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf932a5)
    #25 0x11dcb2aee in base::RunLoop::Run(base::Location const&)+0x46e (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbed0aee)
    #26 0x1324b5370 in content::RendererMain(content::MainFunctionParams const&)+0x9e0 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x206d3370)
    #27 0x11da873cd in content::ContentMainRunnerImpl::Run(bool)+0x3fd (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbca53cd)
    #28 0x11da84716 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*)+0x15f6 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbca2716)
    #29 0x11da84d2c in content::ContentMain(content::ContentMainParams const&)+0x1c (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbca2d2c)

previously allocated by thread T0 here:
    #0 0x107b2cf90 in __asan_memmove+0x1bd0 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/libclang_rt.asan_osx_dynamic.dylib:x86_64+0x44f90)
    #1 0x11dbb0d27 in operator new(unsigned long)+0x27 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbdced27)
    #2 0x13246f634 in non-virtual thunk to content::RenderFrameImpl::GetOrCreateWebComputedAXTree()+0x44 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x2068d634)
    #3 0x12b35f9ae in blink::ComputedAccessibleNodePromiseResolver::UpdateTreeAndResolve()+0x9e (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1957d9ae)
    #4 0x12bc69931 in blink::FrameRequestCallbackCollection::ExecuteFrameCallbacks(double, double)+0x571 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x19e87931)
    #5 0x12bd376b2 in blink::ScriptedAnimationController::ServiceScriptedAnimations(base::TimeTicks)+0x902 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x19f556b2)
    #6 0x12bb2a1de in blink::Document::ServiceScriptedAnimations(base::TimeTicks)+0x4e (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x19d481de)
    #7 0x12c3969ad in blink::LocalFrameView::ServiceScriptedAnimations(base::TimeTicks)+0x39d (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1a5b49ad)
    #8 0x12db2f5bb in blink::PageAnimator::ServiceScriptedAnimations(base::TimeTicks)+0x2db (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1bd4d5bb)
    #9 0x12db3bd14 in blink::PageWidgetDelegate::Animate(blink::Page&, base::TimeTicks)+0x54 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1bd59d14)
    #10 0x12c4b5c86 in blink::WebFrameWidgetImpl::BeginMainFrame(base::TimeTicks)+0x386 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x1a6d3c86)
    #11 0x124006447 in cc::ProxyMain::BeginMainFrame(std::__1::unique_ptr<cc::BeginMainFrameAndCommitState, std::__1::default_delete<cc::BeginMainFrameAndCommitState> >)+0xa37 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x12224447)
    #12 0x124004504 in base::internal::Invoker<base::internal::BindState<void (cc::ProxyMain::*)(std::__1::unique_ptr<cc::BeginMainFrameAndCommitState, std::__1::default_delete<cc::BeginMainFrameAndCommitState> >), base::WeakPtr<cc::ProxyMain>, std::__1::unique_ptr<cc::BeginMainFrameAndCommitState, std::__1::default_delete<cc::BeginMainFrameAndCommitState> > >, void ()>::RunOnce(base::internal::BindStateBase*)+0x1f4 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x12222504)
    #13 0x11dd35df9 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*)+0x3e9 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf53df9)
    #14 0x11dd74042 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*)+0x502 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf92042)
    #15 0x11dd73827 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x1f7 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf91827)
    #16 0x11de63408 in invocation function for block in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0xe8 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc081408)
    #17 0x11de50289 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc06e289)
    #18 0x11de61bb5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*)+0x175 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc07fbb5)
    #19 0x7fff204a7a0b in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x10 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x81a0b)
    #20 0x7fff204a7973 in __CFRunLoopDoSource0+0xb3 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x81973)
    #21 0x7fff204a76ee in __CFRunLoopDoSources0+0xf7 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x816ee)
    #22 0x7fff204a6120 in __CFRunLoopRun+0x379 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x80120)
    #23 0x7fff204a56cd in CFRunLoopRunSpecific+0x232 (/System/Library/Frameworks/CoreFoundation.framework/Versions/A/CoreFoundation:x86_64h+0x7f6cd)
    #24 0x7fff21232fa0 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:]+0xd3 (/System/Library/Frameworks/Foundation.framework/Versions/C/Foundation:x86_64+0x5ffa0)
    #25 0x11de647d0 in base::MessagePumpNSRunLoop::DoRun(base::MessagePump::Delegate*)+0x100 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc0827d0)
    #26 0x11de609d8 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*)+0x208 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xc07e9d8)
    #27 0x11dd752a5 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x2a5 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbf932a5)
    #28 0x11dcb2aee in base::RunLoop::Run(base::Location const&)+0x46e (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0xbed0aee)
    #29 0x1324b5370 in content::RendererMain(content::MainFunctionParams const&)+0x9e0 (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x206d3370)

SUMMARY: AddressSanitizer: heap-use-after-free (/Users/ddv_ua/InfoSec/Apps/Chromium/asan-mac-release-876501/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/92.0.4491.0/Chromium Framework:x86_64+0x19581d84) in blink::ComputedAccessibleNode::parent() const+0x214
Shadow bytes around the buggy address:
  0x1c2c0000aee0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0000aef0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0000af00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0000af10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0000af20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x1c2c0000af30:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0000af40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0000af50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0000af60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c2c0000af70: fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa
  0x1c2c0000af80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
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
  Shadow gap:              cc
==42409==ABORTING
Received signal 6
 [0x00011de28939]
 [0x00011dbd8593]
 [0x00011de2859b]
 [0x7fff203f3d7d]
 [0x7ffee830b5e8]
 [0x7fff20302720]
 [0x000107b4ca26]
 [0x000107b4c154]
 [0x000107b336a4]
 [0x000107b32f7a]
 [0x000107b33b78]
 [0x00012b363d85]
 [0x00012f36bf6a]
 [0x7ee30004b84e]
 [0x7ee300052b24]
[end of stack trace]
[0514/103050.490215:WARNING:process_memory_mac.cc(93)] mach_vm_read(0x7ffee8311000, 0x2000): (os/kern) invalid address (1)

Did this work before? N/A 

Chrome version: 92.0.4491.0 (Developer Build) (x86_64)  Channel: n/a
OS Version: OS X 10.15
Flash Version: Shockwave Flash 30.0 r0

## Attachments

- [heap-uaf-in-aom.html](attachments/heap-uaf-in-aom.html) (text/plain, 987 B)
- [heap-uaf-in-aom-iframe.html](attachments/heap-uaf-in-aom-iframe.html) (text/plain, 770 B)

## Timeline

### [Deleted User] (2021-05-14)

[Empty comment from Monorail migration]

### dm...@gmail.com (2021-05-14)

Sorry, in title and PoC I reference "checked" property, but in ASAN report reference property "parent".

This occurred because issue is also applicable for another properties and when I validated this, I missed that last report was for property "parent" instead of property "checked".

### dm...@gmail.com (2021-05-14)

To simplify exploitation attacker can use "iframe" instead "window.open". I attach another PoC via iframe.

Steps to reproduce the problem:
1. Download file "heap-uaf-in-aom-iframe.html"
2. Open Chromium 92.0.4491.0 (Developer Build) (x86_64)
3. Enable Chromium flag: chrome://flags/#enable-experimental-web-platform-features
4. Relaunch Chromium and open downloaded file "heap-uaf-in-aom-iframe.html".
5. Wait ~1s until browser will be crashed with UaF.

### cl...@chromium.org (2021-05-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6287421629857792.

### xi...@chromium.org (2021-05-17)

Looks like CF cannot reproduce. +aleventhal@, could you take a look? Thanks!

Tentatively setting impact to None since it requires the #enable-experimental-web-platform-features flag to be enabled (assuming this flag is disabled by default).

[Monorail components: Blink>Accessibility]

### al...@chromium.org (2021-05-18)

Correct, it requires --enable-experimental-web-platform-features
I can repro locally.

### gi...@appspot.gserviceaccount.com (2021-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f12af1dba9ab5ca8b96a41bcfcad6c9ffc1f253b

commit f12af1dba9ab5ca8b96a41bcfcad6c9ffc1f253b
Author: Aaron Leventhal <aleventhal@google.com>
Date: Wed May 19 20:12:24 2021

Avoid potential dangling pointer access in computed accessible nodes

Remove raw pointer and use an accessor instead. This will prevent
use-after-free in a robust way. It's impossible for any new getters
to do anything worse than a null pointer reference.

Bug: 1209118
Change-Id: Ied410c54f35e0d99f5d7a14bac9fd7563e9e87d5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2903506
Commit-Queue: Aaron Leventhal <aleventhal@chromium.org>
Auto-Submit: Aaron Leventhal <aleventhal@chromium.org>
Reviewed-by: Stephen McGruer <smcgruer@chromium.org>
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Reviewed-by: Mason Freed <masonf@chromium.org>
Cr-Commit-Position: refs/heads/master@{#884650}

[modify] https://crrev.com/f12af1dba9ab5ca8b96a41bcfcad6c9ffc1f253b/third_party/blink/renderer/core/aom/computed_accessible_node.cc
[modify] https://crrev.com/f12af1dba9ab5ca8b96a41bcfcad6c9ffc1f253b/third_party/blink/renderer/core/aom/computed_accessible_node.h
[modify] https://crrev.com/f12af1dba9ab5ca8b96a41bcfcad6c9ffc1f253b/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/f12af1dba9ab5ca8b96a41bcfcad6c9ffc1f253b/third_party/blink/renderer/core/dom/document.h
[add] https://crrev.com/f12af1dba9ab5ca8b96a41bcfcad6c9ffc1f253b/third_party/blink/web_tests/external/wpt/accessibility/crashtests/aom-in-destroyed-iframe.html


### al...@chromium.org (2021-05-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Nice work!

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-08-26)

This issue was migrated from crbug.com/chromium/1209118?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055854)*
