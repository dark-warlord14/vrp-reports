# Security: Use after free with mouse lock and window.open

| Field | Value |
|-------|-------|
| **Issue ID** | [40060233](https://issues.chromium.org/issues/40060233) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2012-06-24 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome tab crashes due to use after free when window.open is called after mouse is locked.

**VERSION**  

Chrome Version: [22.0.1185.0 (143805)] + [dev]  

Operating System: [Ubuntu 12.04 LTS 64 bit]

**REPRODUCTION CASE**

1. Download mlock.html.
2. Open chrome and load mlock.html.
3. Click on crash button.
4. Wait 3 seconds.  
   
   Chrome will display sad tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State:

## Asan output

==18459== ERROR: AddressSanitizer heap-use-after-free on address 0x7fe8d1f9daa4 at pc 0x7fe8e78802e8 bp 0x7fffc160b6f0 sp 0x7fffc160b6e8  

READ of size 4 at 0x7fe8d1f9daa4 thread T0  

#0 0x7fe8e78802e8 in \_ZN6WebKit11WebViewImpl17currentInputEventEv /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:279  

#1 0x7fe8e787fc66 in \_ZN6WebKit16ChromeClientImpl12createWindowEPN7WebCore5FrameERKNS1\_16FrameLoadRequestERKNS1\_14WindowFeaturesERKNS1\_16NavigationActionE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:252  

#2 0x7fe8e8cdeca1 in \_ZNK7WebCore6Chrome12createWindowEPNS\_5FrameERKNS\_16FrameLoadRequestERKNS\_14WindowFeaturesERKNS\_16NavigationActionE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/page/Chrome.cpp:189  

#3 0x7fe8e8c44c57 in \_ZN7WebCore12createWindowEPNS\_5FrameES1\_RKNS\_16FrameLoadRequestERKNS\_14WindowFeaturesERb /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:3236  

#4 0x7fe8e8d2a574 in *ZN7WebCore9DOMWindow12createWindowERKN3WTF6StringERKNS1\_12AtomicStringERKNS\_14WindowFeaturesEPS0\_PNS\_5FrameESD\_PFvSB\_PvESE* /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1817  

#5 0x7fe8e8d2b886 in *ZN7WebCore9DOMWindow4openERKN3WTF6StringERKNS1\_12AtomicStringES4\_PS0\_S8* /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1904  

#6 0x7fe8e8692ce6 in \_ZN7WebCore11V8DOMWindow12openCallbackERKN2v89ArgumentsE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8DOMWindowCustom.cpp:468  

#7 0x7fe8e67ba76f in \_ZN2v88internalL19HandleApiCallHelperILb0EEEPNS0\_11MaybeObjectENS0\_12\_GLOBAL\_\_N\_116BuiltinArgumentsILNS0\_21BuiltinExtraArgumentsE1EEEPNS0\_7IsolateE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/v8/src/builtins.cc:1145  

addr2line: '': No such file  

#8 0xcc57600618e in  

#9 0xcc576046174 in  

#10 0xcc576046087 in  

#11 0xcc576024967 in  

#12 0xcc576011417 in  

#13 0x7fe8e6831de5 in \_ZN2v88internalL6InvokeEbNS0\_6HandleINS0\_10JSFunctionEEENS1\_INS0\_6ObjectEEEiPS5\_Pb /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/v8/src/execution.cc:118  

#14 0x7fe8e6753786 in \_ZN2v86Script3RunEv /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/v8/src/api.cc:1612  

#15 0x7fe8e867a303 in \_ZN7WebCore7V8Proxy9runScriptEN2v86HandleINS1\_6ScriptEEE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:365  

#16 0x7fe8e86796fc in \_ZN7WebCore7V8Proxy8evaluateERKNS\_16ScriptSourceCodeEPNS\_4NodeE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:336  

#17 0x7fe8e8f87341 in ~Scope /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/v8/include/v8.h:3625  

#18 0x7fe8e8d14a02 in \_ZN7WebCore24InspectorInstrumentation12hasFrontendsEv /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:252  

#19 0x7fe8e8279a48 in \_ZN7WebCore12ThreadTimers24sharedTimerFiredInternalEv /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#20 0x7fe8e5d89276 in ~Callback /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:243  

#21 0x7fe8e5cfc8c5 in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:272  

#22 0x7fe8e5cfd00e in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:467  

#23 0x7fe8e5cff0bb in \_ZN11MessageLoop13DoDelayedWorkEPN4base9TimeTicksE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:681  

#24 0x7fe8e5d08468 in \_ZN4base18MessagePumpDefault3RunEPNS\_11MessagePump8DelegateE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_default.cc:33  

#25 0x7fe8e5cfb4e2 in \_ZN11MessageLoop11RunInternalEv /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:415  

#26 0x7fe8e5cf96ce in ~AutoRunState /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:728  

#27 0x7fe8eb8242d8 in \_Z12RendererMainRKN7content18MainFunctionParamsE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/content/renderer/renderer\_main.cc:270  

#28 0x7fe8e5ba2e8b in \_ZN7content9RunZygoteERKNS\_18MainFunctionParamsEPNS\_19ContentMainDelegateE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main\_runner.cc:327  

#29 0x7fe8e5ba4357 in \_ZN7content23RunNamedProcessTypeMainERKSsRKNS\_18MainFunctionParamsEPNS\_19ContentMainDelegateE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main\_runner.cc:380  

#30 0x7fe8e5ba5a64 in \_ZN7content21ContentMainRunnerImpl3RunEv /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main\_runner.cc:627  

#31 0x7fe8e5ba2575 in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:35  

#32 0x7fe8e45d90e7 in ChromeMain /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#33 0x7fe8e45d904b in main /home/chamal/programs/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#34 0x7fe8dd87276d in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:258  

0x7fe8d1f9daa4 is located 36 bytes inside of 128-byte region [0x7fe8d1f9da80,0x7fe8d1f9db00)  

freed by thread T0 here:  

#0 0x7fe8eccc04f2 in  

#1 0x7fe8e5e3585a in  

#2 0x7fe8e5d287b2 in  

#3 0x7fe8e5cfe930 in  

#4 0x7fe8e5d08407 in  

#5 0x7fe8e5cfb4e2 in  

#6 0x7fe8e5cf96ce in  

#7 0x7fe8eb8242d8 in  

#8 0x7fe8e5ba2e8b in  

#9 0x7fe8e5ba4357 in  

#10 0x7fe8e5ba5a64 in  

#11 0x7fe8e5ba2575 in  

#12 0x7fe8e45d90e7 in  

#13 0x7fe8e45d904b in  

#14 0x7fe8dd87276d in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:258  

previously allocated by thread T1 here:  

#0 0x7fe8eccc06d7 in  

#1 0x7fe8e5d29cdc in  

#2 0x7fe8e5d2a487 in  

#3 0x7fe8e5e36996 in  

#4 0x7fe8e5e30457 in  

#5 0x7fe8e5e3ea72 in  

#6 0x7fe8e5e36293 in  

#7 0x7fe8e5e35ed2 in  

#8 0x7fe8e5e2ac98 in  

#9 0x7fe8e5c9153c in  

#10 0x7fe8e5de4d45 in  

#11 0x7fe8e5c91b67 in  

#12 0x7fe8e5cfb4e2 in  

#13 0x7fe8e5cf96ce in  

#14 0x7fe8e5d8179d in  

#15 0x7fe8e5d7683c in  

#16 0x7fe8eccc38fc in  

Thread T1 created by T0 here:  

#0 0x7fe8eccbc085 in  

#1 0x7fe8e5d763fc in  

#2 0x7fe8e5d762dd in  

#3 0x7fe8e5d80fe4 in  

#4 0x7fe8e71e199f in  

#5 0x7fe8eb78b0dc in  

#6 0x7fe8eb82419f in  

#7 0x7fe8e5ba2e8b in  

#8 0x7fe8e5ba4357 in  

#9 0x7fe8e5ba5a64 in  

#10 0x7fe8e5ba2575 in  

#11 0x7fe8e45d90e7 in  

#12 0x7fe8e45d904b in  

#13 0x7fe8dd87276d in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:258  

==18459== ABORTING  

Stats: 40M malloced (34M for red zones) by 84071 calls  

Stats: 0M realloced by 691 calls  

Stats: 38M freed by 74018 calls  

Stats: 0M really freed by 0 calls  

Stats: 104M (26640 full pages) mmaped in 26 calls  

mmaps by size class: 8:49149; 9:40955; 10:4095; 11:2047; 12:1024; 13:1024; 14:256; 15:128; 16:64; 17:128; 18:16; 19:8; 20:4; 22:3;  

mallocs by size class: 8:46030; 9:33129; 10:3206; 11:594; 12:171; 13:661; 14:44; 15:41; 16:62; 17:122; 18:4; 19:1; 20:3; 22:3;  

frees by size class: 8:37151; 9:32494; 10:2975; 11:403; 12:106; 13:637; 14:34; 15:36; 16:55; 17:116; 18:4; 19:1; 20:3; 22:3;  

rfrees by size class:  

Stats: malloc large: 133 small slow: 361  

Shadow byte and word:  

0x1ffd1a3f3b54: fd  

0x1ffd1a3f3b50: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ffd1a3f3b30: fd fd fd fd fd fd fd fd  

0x1ffd1a3f3b38: fd fd fd fd fd fd fd fd  

0x1ffd1a3f3b40: fa fa fa fa fa fa fa fa  

0x1ffd1a3f3b48: fa fa fa fa fa fa fa fa  

=>0x1ffd1a3f3b50: fd fd fd fd fd fd fd fd  

0x1ffd1a3f3b58: fd fd fd fd fd fd fd fd  

0x1ffd1a3f3b60: fa fa fa fa fa fa fa fa  

0x1ffd1a3f3b68: fa fa fa fa fa fa fa fa  

0x1ffd1a3f3b70: fd fd fd fd fd fd fd fd

## Attachments

- [mlock.html](attachments/mlock.html) (text/plain; charset=us-ascii, 292 B)
- [asan.txt](attachments/asan.txt) (text/x-c; charset=us-ascii, 15.0 KB)

## Timeline

### in...@chromium.org (2012-06-24)

Looks like introduced recently in http://trac.webkit.org/changeset/120486

Chamal, please do pass the stacktrace through c++filt for final cleanedup version.

### in...@chromium.org (2012-06-24)

[Empty comment from Monorail migration]

### ch...@gmail.com (2012-06-24)

This is Asan output taken with c++filt.

==3038== ERROR: AddressSanitizer heap-use-after-free on address 0x7f0ef908dca4 at pc 0x7f0f10b842e8 bp 0x7ffff5e4a310 sp 0x7ffff5e4a308
READ of size 4 at 0x7f0ef908dca4 thread T0
    #0 0x7f0f10b842e8 in WebKit::WebViewImpl::currentInputEvent() /third_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:279
    #1 0x7f0f10b83c66 in WebKit::ChromeClientImpl::createWindow(WebCore::Frame*, WebCore::FrameLoadRequest const&, WebCore::WindowFeatures const&, WebCore::NavigationAction const&) /third_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:252
    #2 0x7f0f11fe2ca1 in WebCore::Chrome::createWindow(WebCore::Frame*, WebCore::FrameLoadRequest const&, WebCore::WindowFeatures const&, WebCore::NavigationAction const&) const /third_party/WebKit/Source/WebCore/page/Chrome.cpp:189
    #3 0x7f0f11f48c57 in WebCore::createWindow(WebCore::Frame*, WebCore::Frame*, WebCore::FrameLoadRequest const&, WebCore::WindowFeatures const&, bool&) /third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:3236
    #4 0x7f0f1202e574 in WebCore::DOMWindow::createWindow(WTF::String const&, WTF::AtomicString const&, WebCore::WindowFeatures const&, WebCore::DOMWindow*, WebCore::Frame*, WebCore::Frame*, void (*)(WebCore::DOMWindow*, void*), void*) /third_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1817
    #5 0x7f0f1202f886 in WebCore::DOMWindow::open(WTF::String const&, WTF::AtomicString const&, WTF::String const&, WebCore::DOMWindow*, WebCore::DOMWindow*) /third_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1904
    #6 0x7f0f11996ce6 in WebCore::V8DOMWindow::openCallback(v8::Arguments const&) /third_party/WebKit/Source/WebCore/bindings/v8/custom/V8DOMWindowCustom.cpp:468
    #7 0x7f0f0fabe76f in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) /v8/src/builtins.cc:1145
    #8 0x2efa7b40618e in  
    #9 0x2efa7b446174 in  
    #10 0x2efa7b446087 in  
    #11 0x2efa7b424967 in  
    #12 0x2efa7b411417 in  
    #13 0x7f0f0fb35de5 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) /v8/src/execution.cc:118
    #14 0x7f0f0fa57786 in v8::Script::Run() /v8/src/api.cc:1612
    #15 0x7f0f1197e303 in WebCore::V8Proxy::runScript(v8::Handle<v8::Script>) /third_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:365
    #16 0x7f0f1197d6fc in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node*) /third_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:336
    #17 0x7f0f1228b341 in ~Scope /v8/include/v8.h:3625
    #18 0x7f0f12018a02 in WebCore::InspectorInstrumentation::hasFrontends() /third_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:252
    #19 0x7f0f1157da48 in WebCore::ThreadTimers::sharedTimerFiredInternal() /third_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118
    #20 0x7f0f0f08d276 in ~Callback /./base/callback.h:243
    #21 0x7f0f0f0008c5 in base::Callback<void ()>::Run() const /./base/callback.h:272
    #22 0x7f0f0f00100e in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /base/message_loop.cc:467
    #23 0x7f0f0f0030bb in MessageLoop::DoDelayedWork(base::TimeTicks*) /base/message_loop.cc:681
    #24 0x7f0f0f00c468 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /base/message_pump_default.cc:33
    #25 0x7f0f0efff4e2 in MessageLoop::RunInternal() /base/message_loop.cc:415
    #26 0x7f0f0effd6ce in ~AutoRunState /base/message_loop.cc:728
    #27 0x7f0f14b282d8 in RendererMain(content::MainFunctionParams const&) /content/renderer/renderer_main.cc:270
    #28 0x7f0f0eea6e8b in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) /content/app/content_main_runner.cc:327
    #29 0x7f0f0eea8357 in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) /content/app/content_main_runner.cc:380
    #30 0x7f0f0eea9a64 in content::ContentMainRunnerImpl::Run() /content/app/content_main_runner.cc:627
    #31 0x7f0f0eea6575 in content::ContentMain(int, char const**, content::ContentMainDelegate*) /content/app/content_main.cc:35
    #32 0x7f0f0d8dd0e7 in ChromeMain /chrome/app/chrome_main.cc:32
    #33 0x7f0f0d8dd04b in main /chrome/app/chrome_exe_main_gtk.cc:18
    #34 0x7f0f06b7676d in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:258
0x7f0ef908dca4 is located 36 bytes inside of 128-byte region [0x7f0ef908dc80,0x7f0ef908dd00)
freed by thread T0 here:
    #0 0x7f0f15fc44f2 in  
    #1 0x7f0f0f13985a in  
    #2 0x7f0f0f02c7b2 in  
    #3 0x7f0f0f002930 in  
    #4 0x7f0f0f00c407 in  
    #5 0x7f0f0efff4e2 in  
    #6 0x7f0f0effd6ce in  
    #7 0x7f0f14b282d8 in  
    #8 0x7f0f0eea6e8b in  
    #9 0x7f0f0eea8357 in  
    #10 0x7f0f0eea9a64 in  
    #11 0x7f0f0eea6575 in  
    #12 0x7f0f0d8dd0e7 in  
    #13 0x7f0f0d8dd04b in  
    #14 0x7f0f06b7676d in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:258
previously allocated by thread T1 here:
    #0 0x7f0f15fc46d7 in  
    #1 0x7f0f0f02dcdc in  
    #2 0x7f0f0f02e487 in  
    #3 0x7f0f0f13a996 in  
    #4 0x7f0f0f134457 in  
    #5 0x7f0f0f142a72 in  
    #6 0x7f0f0f13a293 in  
    #7 0x7f0f0f139ed2 in  
    #8 0x7f0f0f12ec98 in  
    #9 0x7f0f0ef9553c in  
    #10 0x7f0f0f0e8d45 in  
    #11 0x7f0f0ef95b67 in  
    #12 0x7f0f0efff4e2 in  
    #13 0x7f0f0effd6ce in  
    #14 0x7f0f0f08579d in  
    #15 0x7f0f0f07a83c in  
    #16 0x7f0f15fc78fc in  
Thread T1 created by T0 here:
    #0 0x7f0f15fc0085 in  
    #1 0x7f0f0f07a3fc in  
    #2 0x7f0f0f07a2dd in  
    #3 0x7f0f0f084fe4 in  
    #4 0x7f0f104e599f in  
    #5 0x7f0f14a8f0dc in  
    #6 0x7f0f14b2819f in  
    #7 0x7f0f0eea6e8b in  
    #8 0x7f0f0eea8357 in  
    #9 0x7f0f0eea9a64 in  
    #10 0x7f0f0eea6575 in  
    #11 0x7f0f0d8dd0e7 in  
    #12 0x7f0f0d8dd04b in  
    #13 0x7f0f06b7676d in __libc_start_main /build/buildd/eglibc-2.15/csu/libc-start.c:258


### ch...@gmail.com (2012-06-24)

This issue reproduces only when Enable Pointer Lock flag is enabled.

### sc...@chromium.org (2012-06-25)

M21 -> M22, as it is behind a flag for 21 and is not for 22.

### sc...@chromium.org (2012-06-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-06-29)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-06-29)

D'oh. Still impacts-none if it's m22. Sorry for the noise.

### sc...@chromium.org (2012-07-02)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-07-02)

Symbols for all sections: 


=================================================================
==527== ERROR: AddressSanitizer heap-use-after-free on address 0x7fcef7b613a4 at pc 0x7fcf0d930d98 bp 0x7fff9616f150 sp 0x7fff9616f148
READ of size 4 at 0x7fcef7b613a4 thread T0
    #0 0x7fcf0d930d98 in WebKit::WebViewImpl::currentInputEvent() /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:279
    #1 0x7fcf0d930716 in WebKit::ChromeClientImpl::createWindow(WebCore::Frame*, WebCore::FrameLoadRequest const&, WebCore::WindowFeatures const&, WebCore::NavigationAction const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:252
    #2 0x7fcf1155ef81 in WebCore::Chrome::createWindow(WebCore::Frame*, WebCore::FrameLoadRequest const&, WebCore::WindowFeatures const&, WebCore::NavigationAction const&) const /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebCore/page/Chrome.cpp:189
    #3 0x7fcf114b1fa7 in WebCore::createWindow(WebCore::Frame*, WebCore::Frame*, WebCore::FrameLoadRequest const&, WebCore::WindowFeatures const&, bool&) /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:3255
    #4 0x7fcf115aa404 in WebCore::DOMWindow::createWindow(WTF::String const&, WTF::AtomicString const&, WebCore::WindowFeatures const&, WebCore::DOMWindow*, WebCore::Frame*, WebCore::Frame*, void (*)(WebCore::DOMWindow*, void*), void*) /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1817
    #5 0x7fcf115ab716 in WebCore::DOMWindow::open(WTF::String const&, WTF::AtomicString const&, WTF::String const&, WebCore::DOMWindow*, WebCore::DOMWindow*) /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1904
    #6 0x7fcf10c0bbe6 in WebCore::V8DOMWindow::openCallback(v8::Arguments const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/custom/V8DOMWindowCustom.cpp:468
    #7 0x7fcf16796a6f in v8::internal::MaybeObject* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../v8/src/builtins.cc:1145
    #8 0xce44130618e in  
    #9 0xce44133e274 in  
    #10 0xce44133ee07 in  
    #11 0xce441323be7 in  
    #12 0xce441311377 in  
    #13 0x7fcf16823c35 in v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) /usr/local/google/home/scheib/chromium/src/out/Release/../../v8/src/execution.cc:118
    #14 0x7fcf16703c76 in v8::Script::Run() /usr/local/google/home/scheib/chromium/src/out/Release/../../v8/src/api.cc:1612
    #15 0x7fcf10bdf4e3 in WebCore::V8Proxy::runScript(v8::Handle<v8::Script>) /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:365
    #16 0x7fcf10bde8dc in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node*) /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:336
    #17 0x7fcf10b6b7b1 in ~Scope /usr/local/google/home/scheib/chromium/src/out/Release/../../v8/include/v8.h:3631
    #18 0x7fcf11594be2 in WebCore::InspectorInstrumentation::hasFrontends() /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebCore/inspector/InspectorInstrumentation.h:252
    #19 0x7fcf10678b18 in WebCore::ThreadTimers::sharedTimerFiredInternal() /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118
    #20 0x7fcf14de6fa6 in ~Callback /usr/local/google/home/scheib/chromium/src/out/Release/../../base/callback.h:243
    #21 0x7fcf14d35472 in base::Callback<void ()()>::Run() const /usr/local/google/home/scheib/chromium/src/out/Release/../../base/callback.h:272
    #22 0x7fcf14d35c02 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_loop.cc:467
    #23 0x7fcf14d3807b in MessageLoop::DoDelayedWork(base::TimeTicks*) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_loop.cc:681
    #24 0x7fcf14d42068 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_pump_default.cc:33
    #25 0x7fcf14d340b7 in MessageLoop::RunInternal() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_loop.cc:415
    #26 0x7fcf14d8b302 in base::RunLoop::AfterRun() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/run_loop.cc:84
    #27 0x7fcf14d32527 in MessageLoop::Run() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_loop.cc:299
    #28 0x7fcf0b648048 in RendererMain(content::MainFunctionParams const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/renderer/renderer_main.cc:270
    #29 0x7fcf0ad914db in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main_runner.cc:327
    #30 0x7fcf0ad92955 in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main_runner.cc:380
    #31 0x7fcf0ad94005 in content::ContentMainRunnerImpl::Run() /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main_runner.cc:627
    #32 0x7fcf0ad90bf5 in content::ContentMain(int, char const**, content::ContentMainDelegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main.cc:35
    #33 0x7fcf17b41d67 in ChromeMain /usr/local/google/home/scheib/chromium/src/out/Release/../../chrome/app/chrome_main.cc:32
    #34 0x7fcf17b41ccb in main /usr/local/google/home/scheib/chromium/src/out/Release/../../chrome/app/chrome_exe_main_gtk.cc:18
    #35 0x7fcf065c1c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
0x7fcef7b613a4 is located 36 bytes inside of 128-byte region [0x7fcef7b61380,0x7fcef7b61400)
freed by thread T0 here:
    #0 0x7fcf1a64b952 in free ??:0
    #1 0x7fcf174d9cea in ~RefCountedThreadSafe /usr/local/google/home/scheib/chromium/src/out/Release/../../base/memory/ref_counted.h:151
    #2 0x7fcf14d694f2 in base::PendingTask::~PendingTask() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/pending_task.cc:32
    #3 0x7fcf14d378f0 in MessageLoop::DoWork() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_loop.cc:646
    #4 0x7fcf14d42007 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_pump_default.cc:28
    #5 0x7fcf14d340b7 in MessageLoop::RunInternal() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_loop.cc:415
    #6 0x7fcf14d8b302 in base::RunLoop::AfterRun() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/run_loop.cc:84
    #7 0x7fcf14d32527 in MessageLoop::Run() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_loop.cc:299
    #8 0x7fcf0b648048 in RendererMain(content::MainFunctionParams const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/renderer/renderer_main.cc:270
    #9 0x7fcf0ad914db in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main_runner.cc:327
    #10 0x7fcf0ad92955 in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main_runner.cc:380
    #11 0x7fcf0ad94005 in content::ContentMainRunnerImpl::Run() /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main_runner.cc:627
    #12 0x7fcf0ad90bf5 in content::ContentMain(int, char const**, content::ContentMainDelegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main.cc:35
    #13 0x7fcf17b41d67 in ChromeMain /usr/local/google/home/scheib/chromium/src/out/Release/../../chrome/app/chrome_main.cc:32
    #14 0x7fcf17b41ccb in main /usr/local/google/home/scheib/chromium/src/out/Release/../../chrome/app/chrome_exe_main_gtk.cc:18
    #15 0x7fcf065c1c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
previously allocated by thread T1 here:
    #0 0x7fcf1a64bb37 in realloc ??:0
    #1 0x7fcf14d6aa2c in Pickle::Resize(unsigned long) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/pickle.cc:331
    #2 0x7fcf14d6b1ab in Pickle::Pickle(Pickle const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/pickle.cc:194
    #3 0x7fcf174db9c6 in IPC::Message::Message(IPC::Message const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../ipc/ipc_message.cc:47
    #4 0x7fcf174d4617 in BindState /usr/local/google/home/scheib/chromium/src/out/Release/../../base/bind_internal.h:2588
    #5 0x7fcf174e9f83 in IPC::SyncChannel::SyncContext::OnMessageReceived(IPC::Message const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../ipc/ipc_sync_channel.cc:337
    #6 0x7fcf174da6e8 in IPC::internal::ChannelReader::DispatchInputData(char const*, int) /usr/local/google/home/scheib/chromium/src/out/Release/../../ipc/ipc_channel_reader.cc:75
    #7 0x7fcf174da389 in IPC::internal::ChannelReader::ProcessIncomingMessages() /usr/local/google/home/scheib/chromium/src/out/Release/../../ipc/ipc_channel_reader.cc:28
    #8 0x7fcf174cc8be in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) /usr/local/google/home/scheib/chromium/src/out/Release/../../ipc/ipc_channel_posix.cc:796
    #9 0x7fcf14c91a2a in base::MessagePumpLibevent::FileDescriptorWatcher::OnFileCanReadWithoutBlocking(int, base::MessagePumpLibevent*) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_pump_libevent.cc:107
    #10 0x7fcf14e34bc5 in event_process_active /usr/local/google/home/scheib/chromium/src/out/Release/../../third_party/libevent/event.c:386
    #11 0x7fcf14c92397 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_pump_libevent.cc:266
    #12 0x7fcf14d340b7 in MessageLoop::RunInternal() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_loop.cc:415
    #13 0x7fcf14d8b302 in base::RunLoop::AfterRun() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/run_loop.cc:84
    #14 0x7fcf14d32527 in MessageLoop::Run() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/message_loop.cc:299
    #15 0x7fcf14dde1ea in base::Thread::ThreadMain() /usr/local/google/home/scheib/chromium/src/out/Release/../../base/threading/thread.cc:169
    #16 0x7fcf14dcda68 in base::(anonymous namespace)::ThreadFunc(void*) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/threading/platform_thread_posix.cc:65
    #17 0x7fcf1a64ed5c in __asan::AsanThread::ThreadStart() ??:0
Thread T1 created by T0 here:
    #0 0x7fcf1a6474e5 in pthread_create ??:0
    #1 0x7fcf14dcd65c in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*, base::ThreadPriority) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/threading/platform_thread_posix.cc:127
    #2 0x7fcf14dcd53d in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/threading/platform_thread_posix.cc:245
    #3 0x7fcf14ddda7a in base::Thread::StartWithOptions(base::Thread::Options const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../base/threading/thread.cc:74
    #4 0x7fcf0b24438f in ChildProcess::ChildProcess() /usr/local/google/home/scheib/chromium/src/out/Release/../../content/common/child_process.cc:36
    #5 0x7fcf0b5a6c9c in RenderProcessImpl::RenderProcessImpl() /usr/local/google/home/scheib/chromium/src/out/Release/../../content/renderer/render_process_impl.cc:42
    #6 0x7fcf0b647f0f in RendererMain(content::MainFunctionParams const&) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/renderer/renderer_main.cc:252
    #7 0x7fcf0ad914db in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main_runner.cc:327
    #8 0x7fcf0ad92955 in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main_runner.cc:380
    #9 0x7fcf0ad94005 in content::ContentMainRunnerImpl::Run() /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main_runner.cc:627
    #10 0x7fcf0ad90bf5 in content::ContentMain(int, char const**, content::ContentMainDelegate*) /usr/local/google/home/scheib/chromium/src/out/Release/../../content/app/content_main.cc:35
    #11 0x7fcf17b41d67 in ChromeMain /usr/local/google/home/scheib/chromium/src/out/Release/../../chrome/app/chrome_main.cc:32
    #12 0x7fcf17b41ccb in main /usr/local/google/home/scheib/chromium/src/out/Release/../../chrome/app/chrome_exe_main_gtk.cc:18
    #13 0x7fcf065c1c4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
==527== ABORTING
Stats: 23M malloced (20M for red zones) by 42895 calls
Stats: 0M realloced by 92 calls
Stats: 21M freed by 23439 calls
Stats: 0M really freed by 0 calls
Stats: 80M (20492 full pages) mmaped in 18 calls
  mmaps   by size class: 8:49149; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:128; 17:32; 18:16; 19:8; 20:4; 23:2;
  mallocs by size class: 8:36588; 9:3061; 10:2387; 11:320; 12:125; 13:154; 14:125; 15:42; 16:72; 17:12; 18:4; 19:1; 20:2; 23:2;
  frees   by size class: 8:18967; 9:1572; 10:2260; 11:189; 12:84; 13:135; 14:113; 15:35; 16:67; 17:9; 18:3; 19:1; 20:2; 23:2;
  rfrees  by size class:
Stats: malloc large: 21 small slow: 196
Shadow byte and word:
  0x1ff9def6c274: fd
  0x1ff9def6c270: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1ff9def6c250: fd fd fd fd fd fd fd fd
  0x1ff9def6c258: fd fd fd fd fd fd fd fd
  0x1ff9def6c260: fa fa fa fa fa fa fa fa
  0x1ff9def6c268: fa fa fa fa fa fa fa fa
=>0x1ff9def6c270: fd fd fd fd fd fd fd fd
  0x1ff9def6c278: fd fd fd fd fd fd fd fd
  0x1ff9def6c280: fa fa fa fa fa fa fa fa
  0x1ff9def6c288: fa fa fa fa fa fa fa fa
  0x1ff9def6c290: fd fd fd fd fd fd fd fd


### sc...@chromium.org (2012-07-02)

[Empty comment from Monorail migration]

### sc...@chromium.org (2012-07-02)

In gdb asan breaks here on the error:

#0  0x00007ffff7078020 in __asan_report_error ()
#1  0x00007ffff7078437 in __asan_report_load4 ()
#2  0x00007fffea35bd98 in currentInputEvent (inputEvent=<optimized out>) at ../../third_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:272
#3  WebKit::ChromeClientImpl::getNavigationPolicy (this=<optimized out>) at ../../third_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:317
#4  0x00007fffea35b716 in WebKit::ChromeClientImpl::createWindow (this=<optimized out>, frame=<optimized out>, r=..., features=..., action=...) at ../../third_party/WebKit/Source/WebKit/chromium/src/ChromeClientImpl.cpp:252
#5  0x00007fffedf89f81 in WebCore::Chrome::createWindow (this=<optimized out>, frame=<optimized out>, request=..., features=..., action=...) at ../../third_party/WebKit/Source/WebCore/page/Chrome.cpp:189
#6  0x00007fffededcfa7 in WebCore::createWindow (openerFrame=<optimized out>, lookupFrame=<optimized out>, request=..., features=..., created=<error reading variable: Unhandled dwarf expression opcode 0x0>) at ../../third_party/WebKit/Source/WebCore/loader/FrameLoader.cpp:3255
#7  0x00007fffedfd5404 in WebCore::DOMWindow::createWindow (urlString=..., frameName=..., windowFeatures=..., activeWindow=<optimized out>, firstFrame=<optimized out>, openerFrame=<optimized out>, function=<optimized out>, functionContext=<optimized out>) at ../../third_party/WebKit/Source/WebCore/pa
ge/DOMWindow.cpp:1817
#8  0x00007fffedfd6716 in WebCore::DOMWindow::open (this=<error reading variable: Unhandled dwarf expression opcode 0x0>, urlString=..., frameName=<error reading variable: DWARF-2 expression error: DW_OP_reg operations must be used either alone or in conjunction with DW_OP_piece or DW_OP_bit_piece.>,
 windowFeaturesString=..., activeWindow=<optimized out>, firstWindow=<optimized out>) at ../../third_party/WebKit/Source/WebCore/page/DOMWindow.cpp:1904
#9  0x00007fffed636be6 in WebCore::V8DOMWindow::openCallback (args=...) at ../../third_party/WebKit/Source/WebCore/bindings/v8/custom/V8DOMWindowCustom.cpp:468


### sc...@chromium.org (2012-07-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-02)

upstream - https://bugs.webkit.org/show_bug.cgi?id=90391

### ch...@gmail.com (2012-07-03)

Can I get access to view webkit bug please? My webkit bugzilla user name is chamalsl@yahoo.com.

### in...@chromium.org (2012-07-05)

http://trac.webkit.org/changeset/121909

### in...@chromium.org (2012-07-09)

[Empty comment from Monorail migration]

### ch...@gmail.com (2012-08-06)

Is this issue eligible for a reward?

### sc...@gmail.com (2012-08-20)

Thanks for finding this Chamal. Although this feature was behind a flag, it was "almost ready" so we'll reward at the full $1000 level. Thanks!

### ch...@gmail.com (2012-08-21)

Thank you very much for the reward :)

### sc...@gmail.com (2012-09-12)

Paid as part of $1000 batch

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/134325?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/136140]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060233)*
