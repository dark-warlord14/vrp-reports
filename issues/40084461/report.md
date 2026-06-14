# Security: access-violation in blink::ScriptState::from

| Field | Value |
|-------|-------|
| **Issue ID** | [40084461](https://issues.chromium.org/issues/40084461) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Bindings, Blink>Loader |
| **Reporter** | fi...@gmail.com |
| **Assignee** | ik...@chromium.org |
| **Created** | 2016-06-03 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

==164==ERROR: AddressSanitizer: access-violation on unknown address 0x410b1081 (pc 0x11d328c6 bp 0x0039b6b4 sp 0x0039b460 T0)  

#0 0x11d328c5 in blink::ScriptState::from C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\bindings\core\v8\ScriptState.h:77  

#1 0x153c7a68 in blink::messageHandlerInMainThread C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\bindings\core\v8\V8Initializer.cpp:115  

#2 0x1b778f6b in v8::internal::MessageHandler::ReportMessage C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\messages.cc:142  

#3 0x1acb2c25 in v8::internal::Isolate::ReportPendingMessages C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\isolate.cc:1592  

#4 0x11bbf04f in v8::internal::ApiNatives::InstantiateObject C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\api-natives.cc:477  

#5 0x1bae44db in v8::internal::Genesis::ConfigureGlobalObjects C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\bootstrapper.cc:3455  

#6 0x1ba84c63 in v8::internal::Genesis::Genesis C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\bootstrapper.cc:3730  

#7 0x1ba83635 in v8::internal::Bootstrapper::CreateEnvironment C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\bootstrapper.cc:328  

#8 0x11b00b18 in v8::CreateEnvironment C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\api.cc:5588 #9 0x11a98a96 in v8::Context::New C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\api.cc:5616 #10 0x15dc14b1 in blink::WindowProxy::createContext C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\bindings\core\v8\WindowProxy.cpp:324  

#11 0x15dbf74e in blink::WindowProxy::initialize C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\bindings\core\v8\WindowProxy.cpp:235  

#12 0x15dbf439 in blink::WindowProxy::initializeIfNeeded C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\bindings\core\v8\WindowProxy.cpp:222  

#13 0x153a0bed in blink::ScriptController::windowProxy C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\bindings\core\v8\ScriptController.cpp:186  

#14 0x153a278e in blink::ScriptController::updateDocument C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\bindings\core\v8\ScriptController.cpp:281  

#15 0x13be3124 in blink::LocalDOMWindow::installNewDocument C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\frame\LocalDOMWindow.cpp:368  

#16 0x13bd76d8 in blink::DocumentLoader::createWriterFor C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\loader\DocumentLoader.cpp:657  

#17 0x13bd7312 in blink::DocumentLoader::ensureWriter C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\loader\DocumentLoader.cpp:453  

#18 0x13bd2bce in blink::DocumentLoader::commitData C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\loader\DocumentLoader.cpp:461  

#19 0x13bd7b8e in blink::DocumentLoader::processData C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\loader\DocumentLoader.cpp:520  

#20 0x13bd786e in blink::DocumentLoader::dataReceived C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\loader\DocumentLoader.cpp:495  

#21 0x143985da in blink::RawResource::appendData C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\fetch\RawResource.cpp:100  

#22 0x1442598e in blink::ResourceLoader::didReceiveData C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\fetch\ResourceLoader.cpp:199  

#23 0x1cb0fb5c in content::WebURLLoaderImpl::Context::OnReceivedData C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\web\_url\_loader\_impl.cc:716  

#24 0x1cb11bcc in content::WebURLLoaderImpl::RequestPeerImpl::OnReceivedData C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\web\_url\_loader\_impl.cc:893  

#25 0x1628da1e in content::ResourceDispatcher::OnReceivedData C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\resource\_dispatcher.cc:284  

#26 0x16298da1 in IPC::MessageT<ResourceMsg\_DataReceived\_Meta,std::tuple<int,int,int,int>,void>::Dispatch C:\b\build\slave\Win\_ASan\_Release\build\src\ipc\ipc\_message\_templates.h:120  

#27 0x162881f2 in content::ResourceDispatcher::DispatchMessageW C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\resource\_dispatcher.cc:508  

#28 0x1628635a in content::ResourceDispatcher::OnMessageReceived C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\resource\_dispatcher.cc:126  

#29 0x16304c8e in content::`anonymous namespace'::DispatchMessageTask::run C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\resource\_scheduling\_filter.cc:31  

#30 0x1cbbb50e in scheduler::WebTaskRunnerImpl::runTask C:\b\build\slave\Win\_ASan\_Release\build\src\components\scheduler\child\web\_task\_runner\_impl.cc:70  

#31 0xfff4bd1 in base::internal::RunnableAdapter<void (\*)(std::unique\_ptr<base::trace\_event::MemoryDumpManager::ProcessMemoryDumpAsyncState,std::default\_delete[base::trace\_event::MemoryDumpManager::ProcessMemoryDumpAsyncState](javascript:void(0);) >)>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:159  

#32 0x1cbbc22d in base::internal::Invoker<base::IndexSequence<0>,base::internal::BindState<base::internal::RunnableAdapter<void (\*)(std::unique\_ptr<blink::WebTaskRunner::Task,std::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >)>,void (std::unique\_ptr<blink::WebTaskRunner::Task,std::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) >),base::internal::PassedWrapper<std::unique\_ptr<blink::WebTaskRunner::Task,std::default\_delete[blink::WebTaskRunner::Task](javascript:void(0);) > > >,0,void ()>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:364  

#33 0x10021cc1 in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\debug\task\_annotator.cc:49  

#34 0x1cbe56b2 in scheduler::TaskQueueManager::ProcessTaskFromWorkQueue C:\b\build\slave\Win\_ASan\_Release\build\src\components\scheduler\base\task\_queue\_manager.cc:289  

#35 0x1cbdfe0b in scheduler::TaskQueueManager::DoWork C:\b\build\slave\Win\_ASan\_Release\build\src\components\scheduler\base\task\_queue\_manager.cc:201  

#36 0x1cbea00f in base::internal::Invoker<base::IndexSequence<0,1,2>,base::internal::BindState<base::internal::RunnableAdapter<void (scheduler::TaskQueueManager::\*)(base::TimeTicks, bool) **attribute**((thiscall))>,void (scheduler::TaskQueueManager \*, base::TimeTicks, bool),base::WeakPtr[scheduler::TaskQueueManager](javascript:void(0);),base::TimeTicks,bool>,1,void ()>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:358  

#37 0x10021cc1 in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\debug\task\_annotator.cc:49  

#38 0xff24c92 in base::MessageLoop::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:475  

#39 0xff267ba in base::MessageLoop::DoWork C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:599  

#40 0x10028ae4 in base::MessagePumpDefault::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_pump\_default.cc:33  

#41 0xff24008 in base::MessageLoop::RunHandler C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:439  

#42 0x100290d0 in base::RunLoop::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\run\_loop.cc:35  

#43 0xff2312f in base::MessageLoop::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:294  

#44 0x165a2337 in content::RendererMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\renderer\_main.cc:199  

#45 0xfe19220 in content::RunNamedProcessTypeMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:420  

#46 0xfe1b239 in content::ContentMainRunnerImpl::Run C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:787  

#47 0xfe18a74 in content::ContentMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main.cc:20  

#48 0xfaa1122 in ChromeMain C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_main.cc:84  

#49 0xc3a7e6 in MainDllLoader::Launch C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\main\_dll\_loader\_win.cc:185  

#50 0xc325a6 in main C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_exe\_main\_win.cc:263  

#51 0x184a24c in \_\_scrt\_common\_main\_seh f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl:255  

#52 0x76404197 in BaseThreadInitThunk+0x27 (C:\Windows\system32\KERNEL32.DLL+0x68904197)  

#53 0x773c2cb0 in LdrRemoveLoadAsDataTable+0x190 (C:\Windows\SYSTEM32\ntdll.dll+0x6a252cb0)  

#54 0x773c2c7e in LdrRemoveLoadAsDataTable+0x15e (C:\Windows\SYSTEM32\ntdll.dll+0x6a252c7e)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\bindings\core\v8\ScriptState.h:77 in blink::ScriptState::from

**VERSION**  

Chrome Version: asan-win32-release-397536  

Chrome Version: 53.0.2756.0 dev-m

Operating System: Windows 32bit

**REPRODUCTION CASE**

<script>
function crash() {
img = document.createElement('img')
img.src='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"><foreignObject><body xmlns="http://www.w3.org/1999/xhtml"><marquee></marquee></body></foreignObject></svg>'
document.body.appendChild(img)
window.location.reload()
}
</script>
<body onload='crash()'>

## Timeline

### cl...@chromium.org (2016-06-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5103661730758656

### fe...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>Workers]

### fe...@chromium.org (2016-06-03)

nhiroki@, would you be a good person to take a look at this one?

### cl...@chromium.org (2016-06-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5103661730758656

Uploader: felt@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000000000000
Crash State:
  blink::ScriptState::from
  blink::messageHandlerInMainThread
  v8::internal::MessageHandler::ReportMessage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=172836:173286

Minimized Testcase (0.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94Jy7gax7dwADF73_PZAI08-sJ4SQXiLJu4UWTTX_jiuc1Xc6Ut2DLAEWSBHjDBgg6svBcqdIcBj6PLU1ygAkRU7hQr-HbvT0uFqV_46LhZjwK-40gjEIWRq_GNhCs3m2uzx959EWctwELbddatFunXrV6R8A

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-06-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-04)

[Empty comment from Monorail migration]

### fe...@chromium.org (2016-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-05)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### nh...@chromium.org (2016-06-05)

Regarding to the minimized test case and the stack trace, this might be a loader related issue.

[Monorail components: -Blink>Workers Blink>Loader]

### nh...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### ki...@chromium.org (2016-06-06)

+yhirano, +japhet-- does the stack trace ring any bells for you?  I don't have time to investigate this right away.

### yh...@chromium.org (2016-06-06)

It looks there is an error while initializing a V8 context (blink::MessageHandler::ReportMessage is called in v8::Context::New). ScriptState::from needs a proper V8 context which I guess doesn't exist. The check after getting ScriptState is too late.

https://codereview.chromium.org/1885833002 is suspicious.

[Monorail components: Blink>Bindings]

### ik...@chromium.org (2016-06-06)

Have fix in https://codereview.chromium.org/2039333002/ which fixes crash.

https://codereview.chromium.org/1885833002 was root cause.

### bu...@chromium.org (2016-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2deeee5b5604eb997fa053a1b6ab4268c662596f

commit 2deeee5b5604eb997fa053a1b6ab4268c662596f
Author: ikilpatrick <ikilpatrick@chromium.org>
Date: Tue Jun 07 16:04:13 2016

Fixes ASan crash for an embedded Blink-in-JS component.

In the test case (in this patch) it appears the Blink-in-JS component tries to run JS during document creation.
However there is a ScriptForbidden scope which throws a "Uncaught Error: Script execution is forbidden." (probably because it is being created in this weird place?)

This patch re-adds the simple check that was removed in https://codereview.chromium.org/1885833002 which checked if the toDOMWindow(isolate->GetEnteredContext()) was null.
(now the check is just isolate->GetEnteredContext()->IsEmpty()).

BUG=617104

Review-Url: https://codereview.chromium.org/2039333002
Cr-Commit-Position: refs/heads/master@{#398310}

[add] https://crrev.com/2deeee5b5604eb997fa053a1b6ab4268c662596f/third_party/WebKit/LayoutTests/bindings/blink-in-js-asan-crash-expected.txt
[add] https://crrev.com/2deeee5b5604eb997fa053a1b6ab4268c662596f/third_party/WebKit/LayoutTests/bindings/blink-in-js-asan-crash.html
[modify] https://crrev.com/2deeee5b5604eb997fa053a1b6ab4268c662596f/third_party/WebKit/Source/bindings/core/v8/V8Initializer.cpp


### ik...@chromium.org (2016-06-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### ik...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

Your change meets the bar and is auto-approved for M52 (branch: 2743)

### cl...@chromium.org (2016-06-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5103661730758656

Uploader: felt@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000000000000
Crash State:
  blink::ScriptState::from
  blink::messageHandlerInMainThread
  v8::internal::MessageHandler::ReportMessage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=172836:173286

Minimized Testcase (0.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv960n0j6LGDAEfVNLVMbMMWMtDgiMiG_cYKCT3Hfaw3g5ZAGJnFXAJ_0sYnr9qgw2vnzz_ShRLvXxHP540JZ5xTMTI7x1AdyEywsbZi6Epai1EPG9QzIJ-axzdQAum0g-nPcV8xLmF6BBDkKWOCXb8bxpequdA

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### bu...@chromium.org (2016-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d

commit 0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d
Author: Ian Kilpatrick <ikilpatrick@chromium.org>
Date: Wed Jun 08 19:31:49 2016

Fixes ASan crash for an embedded Blink-in-JS component.

In the test case (in this patch) it appears the Blink-in-JS component tries to run JS during document creation.
However there is a ScriptForbidden scope which throws a "Uncaught Error: Script execution is forbidden." (probably because it is being created in this weird place?)

This patch re-adds the simple check that was removed in https://codereview.chromium.org/1885833002 which checked if the toDOMWindow(isolate->GetEnteredContext()) was null.
(now the check is just isolate->GetEnteredContext()->IsEmpty()).

BUG=617104

Review-Url: https://codereview.chromium.org/2039333002
Cr-Commit-Position: refs/heads/master@{#398310}
(cherry picked from commit 2deeee5b5604eb997fa053a1b6ab4268c662596f)

Review URL: https://codereview.chromium.org/2049163003 .

Cr-Commit-Position: refs/branch-heads/2743@{#283}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[add] https://crrev.com/0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d/third_party/WebKit/LayoutTests/bindings/blink-in-js-asan-crash-expected.txt
[add] https://crrev.com/0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d/third_party/WebKit/LayoutTests/bindings/blink-in-js-asan-crash.html
[modify] https://crrev.com/0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d/third_party/WebKit/Source/bindings/core/v8/V8Initializer.cpp


### cl...@chromium.org (2016-06-08)

ClusterFuzz has detected this issue as fixed in range 398017:398351.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5103661730758656

Uploader: felt@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x000000000000
Crash State:
  blink::ScriptState::from
  blink::messageHandlerInMainThread
  v8::internal::MessageHandler::ReportMessage
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=172836:173286
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=398017:398351

Minimized Testcase (0.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv960n0j6LGDAEfVNLVMbMMWMtDgiMiG_cYKCT3Hfaw3g5ZAGJnFXAJ_0sYnr9qgw2vnzz_ShRLvXxHP540JZ5xTMTI7x1AdyEywsbZi6Epai1EPG9QzIJ-axzdQAum0g-nPcV8xLmF6BBDkKWOCXb8bxpequdA

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### bu...@chromium.org (2016-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d

commit 0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d
Author: Ian Kilpatrick <ikilpatrick@chromium.org>
Date: Wed Jun 08 19:31:49 2016

Fixes ASan crash for an embedded Blink-in-JS component.

In the test case (in this patch) it appears the Blink-in-JS component tries to run JS during document creation.
However there is a ScriptForbidden scope which throws a "Uncaught Error: Script execution is forbidden." (probably because it is being created in this weird place?)

This patch re-adds the simple check that was removed in https://codereview.chromium.org/1885833002 which checked if the toDOMWindow(isolate->GetEnteredContext()) was null.
(now the check is just isolate->GetEnteredContext()->IsEmpty()).

BUG=617104

Review-Url: https://codereview.chromium.org/2039333002
Cr-Commit-Position: refs/heads/master@{#398310}
(cherry picked from commit 2deeee5b5604eb997fa053a1b6ab4268c662596f)

Review URL: https://codereview.chromium.org/2049163003 .

Cr-Commit-Position: refs/branch-heads/2743@{#283}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[add] https://crrev.com/0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d/third_party/WebKit/LayoutTests/bindings/blink-in-js-asan-crash-expected.txt
[add] https://crrev.com/0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d/third_party/WebKit/LayoutTests/bindings/blink-in-js-asan-crash.html
[modify] https://crrev.com/0dccfd08b8278a4ac6e3c3ad0698a4e45f3efc0d/third_party/WebKit/Source/bindings/core/v8/V8Initializer.cpp


### aw...@chromium.org (2016-07-26)

Fix already in M53, removing ReleaseBlock-Beta.

### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

Congratulations, the panel awarded $1,000 for this bug.

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-11)

This issue was migrated from crbug.com/chromium/617104?no_tracker_redirect=1

[Multiple monorail components: Blink>Bindings, Blink>Loader]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084461)*
