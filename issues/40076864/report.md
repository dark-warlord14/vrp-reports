# Security: UAF in WebCore::SecurityOrigin::databaseIdentifier()

| Field | Value |
|-------|-------|
| **Issue ID** | [40076864](https://issues.chromium.org/issues/40076864) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2013-01-24 |
| **Bounty** | $1,500.00 |

## Description

**VULNERABILITY DETAILS**  

This is not a bug found by be.  

What I found is a reason why webkit <https://crbug.com/chromium/79013> occur.  

<https://bugs.webkit.org/show_bug.cgi?id=79013>

This webkit bug reports a flaky layout test case (http/tests/workers/terminate-during-sync-operation.html) happening from februay, 2012.

This bug occurs because a use after free.  

I Think this use after free occurs because different threads modify the reference count of m\_protocol variable in SecurityOrigin class.

**VERSION**  

Chrome Version:  

[26.0.1394.0 (178560)] + [trunk build] crashes rarely  

[24.0.1312.52] + [stable] crashes everytime. But not sure whether it is due to the use after free mentioned in this report.

Operating System: [Ubuntu 12.04 LTS]

**REPRODUCTION CASE**  

http/tests/workers/terminate-during-sync-operation.html test does not crash everytime. So I add a location.reload() at the end of the test case to refresh it after executing.  

And then ran it on chrome.(Serve layout test from a web server)  

Sometimes it takes hours to reproduce this crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State: [Address sanitizer]

==15107== ERROR: AddressSanitizer: heap-use-after-free on address 0x7f2bc19dcd40 at pc 0x7f2cb8b13c24 bp 0x7f2c917faf20 sp 0x7f2c917faf18  

READ of size 4 at 0x7f2bc19dcd40 thread T1372  

#0 0x7f2cb8b13c23 in WTF::StringImpl::ref() out/Release/../../third\_party/WebKit/Source/WTF/wtf/text/StringImpl.h:581  

#1 0x7f2cb8c03959 in WTF::StringAppend<WTF::String, WTF::String> WTF::operator+[WTF::String](javascript:void(0);)(WTF::String const&, WTF::String) out/Release/../../third\_party/WebKit/Source/WTF/wtf/text/StringOperators.h:139  

#2 0x7f2cbab1febd in WebCore::SecurityOrigin::databaseIdentifier() const out/Release/../../third\_party/WebKit/Source/WebCore/page/SecurityOrigin.cpp:542  

#3 0x7f2cba5424c2 in WebCore::DatabaseTracker::addOpenDatabase(WebCore::AbstractDatabase\*) out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/chromium/DatabaseTrackerChromium.cpp:81  

#4 0x7f2cbac292ba in AbstractDatabase out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/AbstractDatabase.cpp:211  

#5 0x7f2cba53e234 in DatabaseSync out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/DatabaseSync.cpp:53  

#6 0x7f2cba53d24c in WebCore::DatabaseManager::openDatabaseSync(WebCore::ScriptExecutionContext\*, WTF::String const&, WTF::String const&, WTF::String const&, unsigned long, WTF::PassRefPtr[WebCore::DatabaseCallback](javascript:void(0);), int&) out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/DatabaseManager.cpp:167  

#7 0x7f2cbe06dabb in WebCore::WorkerContextWebDatabase::openDatabaseSync(WebCore::WorkerContext\*, WTF::String const&, WTF::String const&, WTF::String const&, unsigned long, WTF::PassRefPtr[WebCore::DatabaseCallback](javascript:void(0);), int&) out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/WorkerContextWebDatabase.cpp:62  

#8 0x7f2cbb843686 in WebCore::WorkerContextV8Internal::openDatabaseSyncCallback(v8::Arguments const&) out/Release/gen/webcore/bindings/V8WorkerContext.cpp:331  

#9 0x7f2cbcb0d351 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1350  

#10 0xb6efe20654d in  

#11 0xb6efe22ee98 in  

#12 0xb6efe225766 in  

#13 0xb6efe211ff6 in  

#14 0x7f2cbcb5bd98 in v8::internal::Invoke(bool, v8::internal::Handle[v8::internal::JSFunction](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), int, v8::internal::Handle[v8::internal::Object](javascript:void(0);)\*, bool\*) out/Release/../../v8/src/execution.cc:118  

#15 0x7f2cbcad16a8 in v8::Function::Call(v8::Handle[v8::Object](javascript:void(0);), int, v8::Handle[v8::Value](javascript:void(0);)\*) out/Release/../../v8/src/api.cc:3783  

#16 0x7f2cbac7f650 in WebCore::V8WorkerContextEventListener::callListenerFunction(WebCore::ScriptExecutionContext\*, v8::Handle[v8::Value](javascript:void(0);), WebCore::Event\*) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/V8WorkerContextEventListener.cpp:106  

#17 0x7f2cbac7d4cf in WebCore::V8AbstractEventListener::invokeEventHandler(WebCore::ScriptExecutionContext\*, WebCore::Event\*, v8::Handle[v8::Value](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/V8AbstractEventListener.cpp:142  

#18 0x7f2cbac7f36a in WebCore::V8WorkerContextEventListener::handleEvent(WebCore::ScriptExecutionContext\*, WebCore::Event\*) out/Release/../../third\_party/WebKit/Source/WebCore/bindings/v8/V8WorkerContextEventListener.cpp:80  

#19 0x7f2cbb11d254 in WebCore::EventTarget::fireEventListeners(WebCore::Event\*, WebCore::EventTargetData\*, WTF::Vector<WebCore::RegisteredEventListener, 1ul>&) out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:256  

#20 0x7f2cbb11cbae in WebCore::EventTarget::fireEventListeners(WebCore::Event\*) out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:203  

#21 0x7f2cbb11ca18 in WebCore::EventTarget::dispatchEvent(WTF::PassRefPtr[WebCore::Event](javascript:void(0);)) out/Release/../../third\_party/WebKit/Source/WebCore/dom/EventTarget.cpp:155  

#22 0x7f2cbec0f8a8 in WebCore::MessageWorkerContextTask::performTask(WebCore::ScriptExecutionContext\*) out/Release/../../third\_party/WebKit/Source/WebCore/workers/WorkerMessagingProxy.cpp:74  

#23 0x7f2cbab9340a in WebCore::WorkerRunLoop::runInMode(WebCore::WorkerContext\*, WebCore::ModePredicate const&, WebCore::WorkerRunLoop::WaitMode) out/Release/../../third\_party/WebKit/Source/WebCore/workers/WorkerRunLoop.cpp:167  

#24 0x7f2cbab931ff in WebCore::WorkerRunLoop::run(WebCore::WorkerContext\*) out/Release/../../third\_party/WebKit/Source/WebCore/workers/WorkerRunLoop.cpp:135  

#25 0x7f2cbe0bfcee in WebCore::WorkerThread::workerThread() out/Release/../../third\_party/WebKit/Source/WebCore/workers/WorkerThread.cpp:178  

#26 0x7f2cbd4b6bde in WTF::threadEntryPoint(void\*) out/Release/../../third\_party/WebKit/Source/WTF/wtf/Threading.cpp:69  

#27 0x7f2cbd4b7141 in WTF::wtfThreadEntryPoint(void\*) out/Release/../../third\_party/WebKit/Source/WTF/wtf/ThreadingPthreads.cpp:196  

#28 0x7f2cb7442aca in \_\_asan::AsanThread::ThreadStart() ??:0  

0x7f2bc19dcd40 is located 0 bytes inside of 36-byte region [0x7f2bc19dcd40,0x7f2bc19dcd64)  

freed by thread T1372 here:  

#0 0x7f2cb743ec02 in free ??:0  

#1 0x7f2cbab20047 in WebCore::SecurityOrigin::databaseIdentifier() const out/Release/../../third\_party/WebKit/Source/WebCore/page/SecurityOrigin.cpp:542  

#2 0x7f2cba541d40 in WebCore::DatabaseTracker::fullPathForDatabase(WebCore::SecurityOrigin\*, WTF::String const&, bool) out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/chromium/DatabaseTrackerChromium.cpp:71  

#3 0x7f2cba53f550 in WebCore::DBBackend::Server::fullPathForDatabase(WebCore::SecurityOrigin\*, WTF::String const&, bool) out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/DBBackendServer.cpp:73  

#4 0x7f2cba53d6cd in WebCore::DatabaseManager::fullPathForDatabase(WebCore::SecurityOrigin\*, WTF::String const&, bool) out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/DatabaseManager.cpp:203  

#5 0x7f2cbac2926e in AbstractDatabase out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/AbstractDatabase.cpp:210  

#6 0x7f2cba53e234 in DatabaseSync out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/DatabaseSync.cpp:53  

#7 0x7f2cba53d24c in WebCore::DatabaseManager::openDatabaseSync(WebCore::ScriptExecutionContext\*, WTF::String const&, WTF::String const&, WTF::String const&, unsigned long, WTF::PassRefPtr[WebCore::DatabaseCallback](javascript:void(0);), int&) out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/DatabaseManager.cpp:167  

#8 0x7f2cbe06dabb in WebCore::WorkerContextWebDatabase::openDatabaseSync(WebCore::WorkerContext\*, WTF::String const&, WTF::String const&, WTF::String const&, unsigned long, WTF::PassRefPtr[WebCore::DatabaseCallback](javascript:void(0);), int&) out/Release/../../third\_party/WebKit/Source/WebCore/Modules/webdatabase/WorkerContextWebDatabase.cpp:62  

#9 0x7f2cbb843686 in WebCore::WorkerContextV8Internal::openDatabaseSyncCallback(v8::Arguments const&) out/Release/gen/webcore/bindings/V8WorkerContext.cpp:331  

#10 0x7f2cbcb0d351 in v8::internal::MaybeObject\* v8::internal::HandleApiCallHelper<false>(v8::internal::(anonymous namespace)::BuiltinArguments<(v8::internal::BuiltinExtraArguments)1>, v8::internal::Isolate\*) out/Release/../../v8/src/builtins.cc:1350  

#11 0xb6efe20654d in  

#12 0xb6efe22ee98 in  

#13 0xb6efe225766 in  

previously allocated by thread T1372 here:  

#0 0x7f2cb743ece2 in malloc ??:0  

#1 0x7f2cbd4b36b8 in WTF::fastMalloc(unsigned long) out/Release/../../third\_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:274  

#2 0x7f2cbd4d6a52 in WTF::StringImpl::createUninitialized(unsigned int, unsigned char\*&) out/Release/../../third\_party/WebKit/Source/WTF/wtf/text/StringImpl.cpp:180  

#3 0x7f2cbd4d71c7 in WTF::StringImpl::create(unsigned char const\*, unsigned int) out/Release/../../third\_party/WebKit/Source/WTF/wtf/text/StringImpl.cpp:266  

#4 0x7f2cbd4d7b16 in WTF::StringImpl::substring(unsigned int, unsigned int) out/Release/../../third\_party/WebKit/Source/WTF/wtf/text/StringImpl.cpp:369  

#5 0x7f2cbd4ead98 in WTF::String::substring(unsigned int, unsigned int) const out/Release/../../third\_party/WebKit/Source/WTF/wtf/text/WTFString.cpp:319  

#6 0x7f2cbc7ef434 in WebCore::KURLGooglePrivate::componentString(url\_parse::Component const&) const out/Release/../../third\_party/WebKit/Source/WebCore/platform/KURLGoogle.cpp:359  

#7 0x7f2cbc7f0211 in WebCore::KURL::protocol() const out/Release/../../third\_party/WebKit/Source/WebCore/platform/KURLGoogle.cpp:526  

#8 0x7f2cbab1ce30 in SecurityOrigin out/Release/../../third\_party/WebKit/Source/WebCore/page/SecurityOrigin.cpp:119  

Thread T1372 created by T0 (chrome) here:  

#0 0x7f2cb743ac64 in pthread\_create ??:0  

#1 0x7f2cbd4b6fb5 in WTF::createThreadInternal(void (\*)(void\*), void\*, char const\*) out/Release/../../third\_party/WebKit/Source/WTF/wtf/ThreadingPthreads.cpp:204  

#2 0x7f2cbd4b6a7f in WTF::createThread(void (\*)(void\*), void\*, char const\*) out/Release/../../third\_party/WebKit/Source/WTF/wtf/Threading.cpp:86  

#3 0x7f2cbe0bf7ff in WebCore::WorkerThread::start() out/Release/../../third\_party/WebKit/Source/WebCore/workers/WorkerThread.cpp:140  

#4 0x7f2cbec0a7ba in WebCore::WorkerMessagingProxy::startWorkerContext(WebCore::KURL const&, WTF::String const&, WTF::String const&, WebCore::WorkerThreadStartMode) out/Release/../../third\_party/WebKit/Source/WebCore/workers/WorkerMessagingProxy.cpp:287  

#5 0x7f2cbe0bdfda in WebCore::Worker::notifyFinished() out/Release/../../third\_party/WebKit/Source/WebCore/workers/Worker.cpp:154  

#6 0x7f2cbab97597 in WebCore::WorkerScriptLoader::didFinishLoading(unsigned long, double) out/Release/../../third\_party/WebKit/Source/WebCore/workers/WorkerScriptLoader.cpp:162  

#7 0x7f2cbaa1d379 in WebCore::CachedResource::didAddClient(WebCore::CachedResourceClient\*) out/Release/../../third\_party/WebKit/Source/WebCore/loader/cache/CachedResource.cpp:482  

#8 0x7f2cbaa18e61 in WebCore::CachedRawResource::didAddClient(WebCore::CachedResourceClient\*) out/Release/../../third\_party/WebKit/Source/WebCore/loader/cache/CachedRawResource.cpp:97  

#9 0x7f2cbc821e72 in WebCore::ThreadTimers::sharedTimerFiredInternal() out/Release/../../third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:116  

#10 0x7f2cbd415aad in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void (webkit\_glue::WebKitPlatformSupportImpl\*)>::MakeItSo(base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, webkit\_glue::WebKitPlatformSupportImpl\*) out/Release/../../base/bind\_internal.h:871  

#11 0x7f2cbd4158a0 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (webkit\_glue::WebKitPlatformSupportImpl::\*)()>, void (webkit\_glue::WebKitPlatformSupportImpl\*), void (base::internal::UnretainedWrapper<webkit\_glue::WebKitPlatformSupportImpl>)>, void (webkit\_glue::WebKitPlatformSupportImpl\*)>::Run(base::internal::BindStateBase\*) out/Release/../../base/bind\_internal.h:1173  

#12 0x7f2cb91512a5 in base::Timer::RunScheduledTask() out/Release/../../base/timer.cc:181  

#13 0x7f2cb91518fd in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void (base::BaseTimerTaskInternal\*)>::MakeItSo(base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, base::BaseTimerTaskInternal\*) out/Release/../../base/bind\_internal.h:871  

#14 0x7f2cb91517a2 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base::BaseTimerTaskInternal::\*)()>, void (base::BaseTimerTaskInternal\*), void (base::internal::OwnedWrapper[base::BaseTimerTaskInternal](javascript:void(0);))>, void (base::BaseTimerTaskInternal\*)>::Run(base::internal::BindStateBase\*) out/Release/../../base/bind\_internal.h:1173  

#15 0x7f2cb90c3ad5 in MessageLoop::RunTask(base::PendingTask const&) out/Release/../../base/message\_loop.cc:473  

#16 0x7f2cb90c43dc in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) out/Release/../../base/message\_loop.cc:485  

#17 0x7f2cb90c4601 in MessageLoop::DoWork() out/Release/../../base/message\_loop.cc:668  

#18 0x7f2cb90d0f5c in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) out/Release/../../base/message\_pump\_default.cc:29  

#19 0x7f2cb90c3194 in MessageLoop::RunInternal() out/Release/../../base/message\_loop.cc:430  

#20 0x7f2cb90ff0c2 in base::RunLoop::Run() out/Release/../../base/run\_loop.cc:45  

#21 0x7f2cb90c1e67 in MessageLoop::Run() out/Release/../../base/message\_loop.cc:310  

#22 0x7f2cbbe68818 in content::RendererMain(content::MainFunctionParams const&) out/Release/../../content/renderer/renderer\_main.cc:223  

#23 0x7f2cbbdbeb0b in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate\*) out/Release/../../content/app/content\_main\_runner.cc:402  

#24 0x7f2cbbdbf4a9 in content::RunNamedProcessTypeMain(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate\*) out/Release/../../content/app/content\_main\_runner.cc:458  

#25 0x7f2cbbdc0219 in content::ContentMainRunnerImpl::Run() out/Release/../../content/app/content\_main\_runner.cc:754  

#26 0x7f2cbbdbe211 in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) out/Release/../../content/app/content\_main.cc:35  

#27 0x7f2cb7447b10 in ChromeMain out/Release/../../chrome/app/chrome\_main.cc:32  

#28 0x7f2cb7447a6a in main out/Release/../../chrome/app/chrome\_exe\_main\_gtk.cc:31  

#29 0x7f2cafe9376c in \_\_libc\_start\_main /build/buildd/eglibc-2.15/csu/libc-start.c:226

## Timeline

### ch...@gmail.com (2013-01-24)

Suggested  fix:
Change this line of the constructor of AbstractDatabase.cpp.

m_contextThreadSecurityOrigin = m_scriptExecutionContext->securityOrigin();
to
m_contextThreadSecurityOrigin = m_scriptExecutionContext->securityOrigin()->isolatedCopy();

If this fix is ok I like to submit a patch.

### in...@chromium.org (2013-01-24)

Dave wrote this in http://trac.webkit.org/changeset/104113. Can you please take a look.

### le...@chromium.org (2013-01-24)

+abarth due to his involvement with https://bugs.webkit.org/show_bug.cgi?id=107784

### le...@chromium.org (2013-01-24)

btw "Dave wrote this in http://trac.webkit.org/changeset/104113" means the test that is exposing the issue. :)

### le...@chromium.org (2013-01-24)

chamal.desilva that seems like a fine fix.

Thank you!

### ab...@chromium.org (2013-01-25)

Dave, I can take this bug off your hands if you like.  :)

### bu...@chromium.org (2013-01-25)

https://bugs.webkit.org/show_bug.cgi?id=79013


### bu...@chromium.org (2013-01-29)

https://bugs.webkit.org/show_bug.cgi?id=79013
http://trac.webkit.org/changeset/141057


### ab...@chromium.org (2013-01-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-01-29)

Need to consider Chamal for higher reward, since he supplied the patch. Just a fyi for the panel.

### sc...@gmail.com (2013-01-29)

M25: http://trac.webkit.org/changeset/141155

### sc...@gmail.com (2013-02-11)

@chamal: nice idea to look for flaky tests that fail with an actual crash :)
$1000 for the bug and $500 bonus for the fix, which it seems like we took verbatim.
Total $1500

### ch...@gmail.com (2013-02-11)

Thank you very much for the reward :)

### pa...@chromium.org (2013-02-14)

Hey Chamal,

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### pa...@chromium.org (2013-02-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-24)

[Empty comment from Monorail migration]

### ch...@gmail.com (2013-02-27)

What is the status of the reward. Reward-inprocess flag is removed. Does it mean it is paid?

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-13)

Hey Chamal,

By now, you should have received payment. Let me know if that's not the case, and I'll investigate.

### ch...@gmail.com (2013-03-14)

I received the payment. Thanks a lot :)

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/171951?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076864)*
