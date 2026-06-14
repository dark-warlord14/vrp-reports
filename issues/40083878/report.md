# Use after free when encountering history.back() call during Page::goToItem execution

| Field | Value |
|-------|-------|
| **Issue ID** | [40083878](https://issues.chromium.org/issues/40083878) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ge...@gmail.com |
| **Assignee** | mi...@chromium.org |
| **Created** | 2010-10-18 |
| **Bounty** | $500.00 |

## Description

Chrome Version : 8.0.558.0 (Developer Build 62906), WinXP  

URLs (if applicable) : <http://www.volkswagen.de/vwcms/master_public/virtualmaster/de3/modelle/passat.html>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 4:**  

**Firefox 3.x:**  

**IE 7:**  

**IE 8:**

**What steps will reproduce the problem?**

1. go to the url
2. click "Konfigurator Passat Variant"
3. in the new window click "comfort"
4. do a history back (with the back key on your keyboard)

**What is the expected result?**  

goes back

**What happens instead?**  

AW, snap! on the popup and normal window

## Timeline

### th...@chromium.org (2010-10-19)

Can you reproduce this? Care to run windbg and get a backtrace?

### tk...@chromium.org (2010-10-19)

I reproduced this with today's chromium Mac Debug.

0x0130d897 in url_canon::(anonymous namespace)::DoRemoveURLWhitespace<unsigned short> (input=0x0, input_len=8, buffer=0xb5628d7c, output_len=0xb5629598) at /Volumes/d2/chromesvn/src/build/temp_gyp/../../googleurl/src/url_canon_etc.cc:59
59          if (!IsRemovableURLWhitespace(input[i]))
(gdb) 
Current language:  auto; currently c++
(gdb) bt
#0  0x0130d897 in url_canon::(anonymous namespace)::DoRemoveURLWhitespace<unsigned short> (input=0x0, input_len=8, buffer=0xb5628d7c, output_len=0xb5629598) at /Volumes/d2/chromesvn/src/build/temp_gyp/../../googleurl/src/url_canon_etc.cc:59
#1  0x0130d969 in url_canon::RemoveURLWhitespace (input=0x0, input_len=8, buffer=0xb5628d7c, output_len=0xb5629598) at /Volumes/d2/chromesvn/src/build/temp_gyp/../../googleurl/src/url_canon_etc.cc:312
#2  0x0131d182 in url_util::(anonymous namespace)::DoResolveRelative<unsigned short> (base_spec=0x0, base_spec_len=0, base_parsed=@0xb5629ab4, in_relative=0x0, in_relative_length=8, charset_converter=0x0, output=0xb562963c, output_parsed=0xb5629b60) at /Volumes/d2/chromesvn/src/build/temp_gyp/../../googleurl/src/url_util.cc:228
#3  0x0131d348 in url_util::ResolveRelative (base_spec=0x0, base_spec_len=0, base_parsed=@0xb5629ab4, relative=0x0, relative_length=8, charset_converter=0x0, output=0xb562963c, output_parsed=0xb5629b60) at /Volumes/d2/chromesvn/src/build/temp_gyp/../../googleurl/src/url_util.cc:454
#4  0x021624e2 in WebCore::KURLGooglePrivate::init (this=0xb5629b5c, base=@0xb5629ab0, rel=0x0, relLength=8, queryEncoding=0x0) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../platform/KURLGoogle.cpp:255
#5  0x021626be in WebCore::KURLGooglePrivate::init (this=0xb5629b5c, base=@0xb5629ab0, relative=@0x15a69e68, queryEncoding=0x0) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../platform/KURLGoogle.cpp:194
#6  0x021627f3 in WebCore::KURL::KURL (this=0xb5629b5c, url=@0x15a69e68) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../platform/KURLGoogle.cpp:373
#7  0x0245db7e in WebCore::HistoryItem::url (this=0x15a69e60) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../history/HistoryItem.cpp:197
#8  0x01cd4ca2 in WebKit::FrameLoaderClientImpl::shouldGoToHistoryItem (this=0x1581c85c, item=0x15a69e60) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebKit/chromium/src/FrameLoaderClientImpl.cpp:1108
#9  0x0252c843 in WebCore::HistoryController::goToItem (this=0xa087774, targetItem=0x15a69e60, type=WebCore::FrameLoadTypeIndexedBackForward) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../loader/HistoryController.cpp:227
#10 0x025bd182 in WebCore::Page::goToItem (this=0x1580d210, item=0x15a69e60, type=WebCore::FrameLoadTypeIndexedBackForward) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../page/Page.cpp:369
#11 0x025bd2c4 in WebCore::Page::goBackOrForward (this=0x1580d210, distance=1) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../page/Page.cpp:343
#12 0x02539305 in WebCore::ScheduledHistoryNavigation::fire (this=0x15a7efd0, frame=0x170b3400) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../loader/NavigationScheduler.cpp:180
#13 0x02537e0a in WebCore::NavigationScheduler::timerFired (this=0x170b3758) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../loader/NavigationScheduler.cpp:373
#14 0x0253905f in WebCore::Timer<WebCore::NavigationScheduler>::fired (this=0x170b375c) at Timer.h:98
#15 0x0217635b in WebCore::ThreadTimers::sharedTimerFiredInternal (this=0x938ad90) at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../platform/ThreadTimers.cpp:112
#16 0x021764fd in WebCore::ThreadTimers::sharedTimerFired () at /Volumes/d2/chromesvn/src/third_party/WebKit/WebCore/WebCore.gyp/../platform/ThreadTimers.cpp:90
#17 0x0189b22e in webkit_glue::WebKitClientImpl::DoTimeout (this=0x936ec30) at webkitclient_impl.h:68
#18 0x0189b2e6 in DispatchToMethod<webkit_glue::WebKitClientImpl, void (webkit_glue::WebKitClientImpl::*)()> (obj=0x936ec30, method={__pfn = 0x189b20c <webkit_glue::WebKitClientImpl::DoTimeout()>, __delta = 0}, arg=@0xb5629e6f) at tuple.h:537
#19 0x0189b329 in base::BaseTimer<webkit_glue::WebKitClientImpl, false>::TimerTask::Run (this=0x15a70b10) at timer.h:160
#20 0x00c7baff in MessageLoop::RunTask (this=0xb562ae48, task=0x15a70b10) at /Volumes/d2/chromesvn/src/base/message_loop.cc:410
#21 0x00c7bbaf in MessageLoop::DeferOrRunPendingTask (this=0xb562ae48, pending_task=@0xb5629fec) at /Volumes/d2/chromesvn/src/base/message_loop.cc:419
#22 0x00c7be3f in MessageLoop::DoWork (this=0xb562ae48) at /Volumes/d2/chromesvn/src/base/message_loop.cc:526
#23 0x00ce9a0a in base::MessagePumpCFRunLoopBase::RunWork (this=0x952a380) at /Volumes/d2/chromesvn/src/base/message_pump_mac.mm:291
#24 0x00ce9a4f in base::MessagePumpCFRunLoopBase::RunWorkSource (info=0x952a380) at /Volumes/d2/chromesvn/src/base/message_pump_mac.mm:269
#25 0x97e64f91 in __CFRunLoopDoSources0 ()
#26 0x97e62bbf in __CFRunLoopRun ()
#27 0x97e62094 in CFRunLoopRunSpecific ()
#28 0x97e61ec1 in CFRunLoopRunInMode ()
#29 0x91103378 in -[NSRunLoop(NSRunLoop) runMode:beforeDate:] ()
#30 0x00ce969c in base::MessagePumpNSRunLoop::DoRun (this=0x952a380, delegate=0xb562ae48) at /Volumes/d2/chromesvn/src/base/message_pump_mac.mm:650
#31 0x00ce9b3b in base::MessagePumpCFRunLoopBase::Run (this=0x952a380, delegate=0xb562ae48) at /Volumes/d2/chromesvn/src/base/message_pump_mac.mm:213
#32 0x00c7c6cc in MessageLoop::RunInternal (this=0xb562ae48) at /Volumes/d2/chromesvn/src/base/message_loop.cc:258
#33 0x00c7c6e7 in MessageLoop::RunHandler (this=0xb562ae48) at /Volumes/d2/chromesvn/src/base/message_loop.cc:230
#34 0x00c7c74b in MessageLoop::Run (this=0xb562ae48) at /Volumes/d2/chromesvn/src/base/message_loop.cc:208
#35 0x00cb9e4d in base::Thread::Run (this=0x936ad50, message_loop=0xb562ae48) at /Volumes/d2/chromesvn/src/base/thread.cc:140
#36 0x00cba321 in base::Thread::ThreadMain (this=0x936ad50) at /Volumes/d2/chromesvn/src/base/thread.cc:164
#37 0x00c98be8 in ThreadFunc (closure=0x936ad50) at /Volumes/d2/chromesvn/src/base/platform_thread_posix.cc:35
#38 0x9243281d in _pthread_start ()
#39 0x924326a2 in thread_start ()

(gdb) p i
$1 = 0
(gdb) p input
$2 = (const char16 *) 0x0
(gdb) p input_len
$3 = 8


### ge...@gmail.com (2010-10-19)

thx tkent, no more work for me :)!

### th...@chromium.org (2010-10-19)

There hasn't been a googleurl update in a month. Probably a bug in webkit. There were some recent change to KURLGoogle.cpp.

### [Deleted User] (2010-10-21)

Mihai, any chance you can help figure out whats going on here?

### [Deleted User] (2010-10-21)

Mihai, any chance you can help figure out whats going on here?

### mi...@chromium.org (2010-10-22)

Will try to reduce.

### mi...@chromium.org (2010-10-26)

I don't think a GoogleURL or KURL change is to blame. By the time we get to HistoryController::goToItem, the HistoryItem that is passed in has been dereferenced one too many times (m_deletionHasBegun is true) and had its destructor called. This clears out its m_urlString member, and GoogleURL doesn't like the empty string that's passed to it. 

So the problem lies before the given stack trace. As far as I can tell, in Page::goToItem, the stopAllLoaders() call can occasionally cause the passed in HistoryItem*'s ref count to decrease, and thus for it to be deleted by the time we get to the HistoryController::goToItem call at the end. A protector RefPtr<HistoryItem> would work around this, but I'd like to understand why stopAllLoaders is causing its ref count to go down in the first place (partly so I can make a reduction, since I haven't had much luck with the mess of iframes and event handlers that is the configuration UI on volkswagen.de).

### mi...@chromium.org (2010-10-26)

This is how we end up destroying the current HistoryItem:

#0  WebCore::HistoryItem::~HistoryItem (this=0x40408940) at src/third_party/WebKit/WebCore/WebCore.gyp/../history/HistoryItem.cpp:117
#1  0x02606aef in WTF::RefCounted<WebCore::HistoryItem>::deref (this=0x40408940) at RefCounted.h:139
#2  0x02606b1b in WTF::derefIfNotNull<WebCore::HistoryItem> (ptr=0x40408940) at PassRefPtr.h:59
#3  0x01d3cfed in WTF::RefPtr<WebCore::HistoryItem>::operator= (this=0x14d2c030, o=@0xb50e40e0) at RefPtr.h:140
#4  0x01ce8931 in WebKit::BackForwardListClientImpl::itemAtIndex (this=0x14d2c020, index=1) at src/third_party/WebKit/WebKit/chromium/src/BackForwardListClientImpl.cpp:117
#5  0x0249b5bd in WebCore::BackForwardListImpl::itemAtIndex (this=0x14d32430, index=1) at src/third_party/WebKit/WebCore/WebCore.gyp/../history/BackForwardListChromium.cpp:121
#6  0x02579ff5 in WebCore::NavigationScheduler::scheduleHistoryNavigation (this=0xa8d7db0, steps=1) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/NavigationScheduler.cpp:355
#7  0x025fa7fe in WebCore::History::forward (this=0x40470d20) at src/third_party/WebKit/WebCore/WebCore.gyp/../page/History.cpp:73
#8  0x01fb0741 in WebCore::HistoryInternal::forwardCallback (args=@0xb50e41d8) at V8History.cpp:78
#9  0x0140f1b3 in v8::internal::HandleApiCallHelper<false> (args={<v8::internal::Arguments> = {<v8::internal::Embedded> = {<No data fields>}, length_ = 2, arguments_ = 0xb50e42c0}, <No data fields>}) at src/v8/tools/gyp/../../src/builtins.cc:983
#10 0x0140f257 in v8::internal::Builtin_Impl_HandleApiCall (args={<v8::internal::Arguments> = {<v8::internal::Embedded> = {<No data fields>}, length_ = 2, arguments_ = 0xb50e42c0}, <No data fields>}) at src/v8/tools/gyp/../../src/builtins.cc:1000
#11 0x0140f27c in v8::internal::Builtin_HandleApiCall (args={<v8::internal::Arguments> = {<v8::internal::Embedded> = {<No data fields>}, length_ = 2, arguments_ = 0xb50e42c0}, <No data fields>}) at src/v8/tools/gyp/../../src/builtins.cc:999
#12 0x1b96c1ee in ?? ()
#13 0x1dfe9d5c in ?? ()
#14 0x1b96e09f in ?? ()
#15 0x1b97d151 in ?? ()
#16 0x1b96d442 in ?? ()
#17 0x014428c5 in v8::internal::Invoke (construct=false, func={location_ = 0xb03be64}, receiver={location_ = 0xb03be74}, argc=1, args=0xb50e4530, has_pending_exception=0xb50e447f) at src/v8/tools/gyp/../../src/execution.cc:94
#18 0x01442dd1 in v8::internal::Execution::Call (func={location_ = 0xb03be64}, receiver={location_ = 0xb03be74}, argc=1, args=0xb50e4530, pending_exception=0xb50e447f) at src/v8/tools/gyp/../../src/execution.cc:121
#19 0x013ed08f in v8::Function::Call (this=0xb03be64, recv={val_ = 0xb03be74}, argc=1, argv=0xb50e4530) at src/v8/tools/gyp/../../src/api.cc:2840
#20 0x0225c92d in WebCore::V8Proxy::callFunction (this=0x1638b130, function={val_ = 0xb03be64}, receiver={val_ = 0xb03be74}, argc=1, args=0xb50e4530) at src/third_party/WebKit/WebCore/WebCore.gyp/../bindings/v8/V8Proxy.cpp:513
#21 0x02201ec9 in WebCore::V8EventListener::callListenerFunction (this=0x40441010, context=0x980a038, jsEvent={val_ = 0xb03be48}, event=0x404089e0) at src/third_party/WebKit/WebCore/WebCore.gyp/../bindings/v8/custom/V8CustomEventListener.cpp:75
#22 0x02241010 in WebCore::V8AbstractEventListener::invokeEventHandler (this=0x40441010, context=0x980a038, event=0x404089e0, jsEvent={val_ = 0xb03be48}) at src/third_party/WebKit/WebCore/WebCore.gyp/../bindings/v8/V8AbstractEventListener.cpp:151
#23 0x02241527 in WebCore::V8AbstractEventListener::handleEvent (this=0x40441010, context=0x980a038, event=0x404089e0) at src/third_party/WebKit/WebCore/WebCore.gyp/../bindings/v8/V8AbstractEventListener.cpp:94
#24 0x023a2660 in WebCore::EventTarget::fireEventListeners (this=0x944df00, event=0x404089e0, d=0x944dfb4, entry=@0x4043d1d0) at src/third_party/WebKit/WebCore/WebCore.gyp/../dom/EventTarget.cpp:335
#25 0x023a2d5c in WebCore::EventTarget::fireEventListeners (this=0x944df00, event=0x404089e0) at src/third_party/WebKit/WebCore/WebCore.gyp/../dom/EventTarget.cpp:304
#26 0x025b869e in WebCore::DOMWindow::dispatchEvent (this=0x944df00, prpEvent=@0xb50e4798, prpTarget=@0xb50e4794) at src/third_party/WebKit/WebCore/WebCore.gyp/../page/DOMWindow.cpp:1536
#27 0x025b9777 in WebCore::DOMWindow::dispatchLoadEvent (this=0x944df00) at src/third_party/WebKit/WebCore/WebCore.gyp/../page/DOMWindow.cpp:1502
#28 0x02363fc7 in WebCore::Document::dispatchWindowLoadEvent (this=0x980a000) at src/third_party/WebKit/WebCore/WebCore.gyp/../dom/Document.cpp:3387
#29 0x02366746 in WebCore::Document::implicitClose (this=0x980a000) at src/third_party/WebKit/WebCore/WebCore.gyp/../dom/Document.cpp:2021
#30 0x0255acd3 in WebCore::FrameLoader::checkCallImplicitClose (this=0xa8d7a2c) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:902
#31 0x0255db59 in WebCore::FrameLoader::checkCompleted (this=0xa8d7a2c) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:850
#32 0x0255dc57 in WebCore::FrameLoader::completed (this=0x993c02c) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:1200
#33 0x0255db79 in WebCore::FrameLoader::checkCompleted (this=0x993c02c) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:854
#34 0x0255f0de in WebCore::FrameLoader::mainReceivedCompleteError (this=0x993c02c, loader=0x9941600) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:3260
#35 0x02544d21 in WebCore::DocumentLoader::mainReceivedError (this=0x9941600, error=@0xb50e4a2c, isComplete=true) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/DocumentLoader.cpp:197
#36 0x0255c724 in WebCore::FrameLoader::receivedMainResourceError (this=0x993c02c, error=@0xb50e4a2c, isComplete=true) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:2817
#37 0x02573355 in WebCore::MainResourceLoader::didCancel (this=0x9997c00, error=@0xb50e4a2c) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/MainResourceLoader.cpp:107
#38 0x0257c8ba in WebCore::ResourceLoader::cancel (this=0x9997c00, error=@0xb50e4a6c) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/ResourceLoader.cpp:364
#39 0x0257c507 in WebCore::ResourceLoader::cancel (this=0x9997c00) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/ResourceLoader.cpp:354
#40 0x02544e55 in WebCore::DocumentLoader::stopLoading (this=0x9941600, databasePolicy=WebCore::DatabasePolicyStop) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/DocumentLoader.cpp:240
#41 0x02559921 in WebCore::FrameLoader::stopAllLoaders (this=0x993c02c, databasePolicy=WebCore::DatabasePolicyStop) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:1700
#42 0x02559a11 in WebCore::FrameLoader::stopLoadingSubframes (this=0xa8d7a2c) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:1681
#43 0x025598e6 in WebCore::FrameLoader::stopAllLoaders (this=0xa8d7a2c, databasePolicy=WebCore::DatabasePolicyStop) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:1698
#44 0x02559a11 in WebCore::FrameLoader::stopLoadingSubframes (this=0x15840c2c) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:1681
#45 0x025598e6 in WebCore::FrameLoader::stopAllLoaders (this=0x15840c2c, databasePolicy=WebCore::DatabasePolicyStop) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/FrameLoader.cpp:1698
#46 0x025ff0ec in WebCore::Page::goToItem (this=0x14d4b560, item=0x40408940, type=WebCore::FrameLoadTypeIndexedBackForward) at src/third_party/WebKit/WebCore/WebCore.gyp/../page/Page.cpp:378
#47 0x025ff3a1 in WebCore::Page::goBackOrForward (this=0x14d4b560, distance=1) at src/third_party/WebKit/WebCore/WebCore.gyp/../page/Page.cpp:346
#48 0x0257b18d in WebCore::ScheduledHistoryNavigation::fire (this=0x163f56d0, frame=0x9968000) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/NavigationScheduler.cpp:180
#49 0x02579c92 in WebCore::NavigationScheduler::timerFired (this=0x99683b0) at src/third_party/WebKit/WebCore/WebCore.gyp/../loader/NavigationScheduler.cpp:373
#50 0x0257aee7 in WebCore::Timer<WebCore::NavigationScheduler>::fired (this=0x99683b4) at Timer.h:98
...

As part of going forward (stack frame #47), we stop all current loads (stack frame #45). We have three nested FrameLoaders (0x15840c2c -> 0xa8d7a2c -> 0x993c02c) so we end up triggering the onload handler of the middle one (stack frame #30-#27). The onload handler also calls history.forward, which ends up in NavigationScheduler::scheduleHistoryNavigation (stack frame #6), which calls BackForwardListImpl::itemAtIndex (stack frame #5) to make sure that we have an item to navigate to. The Chromium implementation of itemAtIndex has side effects (it saves the item in m_pendingHistoryItem, since we're about to navigate to it), and since m_pendingHistoryItem was the only reference to the history item that we were navigating to in the first place (0x40408940 is the item on both stack frame #46 and #2), we end up destroying it even though Page::goToItem isn't done with it.

Possible fixes:
1. Add a protector RefPtr<HistoryItem> protector(item) in Page::goToItem
2. Change NavigationScheduler::scheduleHistoryNavigation to not call BackForwardListImpl::itemAtIndex. It doesn't actually care the item that's returned, it just wants to check whether we can navigate by that amount, so we can use backListCount() and forwardListCount().
3. Change FrameLoader so that we don't invoke onload handlers when stopping loads

I think 3 would be too broad of a change, so I'm leaning towards doing both 1 and 2.

### mi...@chromium.org (2010-10-27)

Finally have a reduction: http://persistent.info/webkit/test-cases/crbug-59554/outer-pre.html

The flow is:
1. outer-pre.html goes to outer.html (after onload, to create a history entry). 
2. outer.html has an iframe that points to middle.html.
3. middle.html has an iframe that points to hung-page.php
4. hung-page.php never loads (it just has a sleep statement), which means that its load is never committed.
5. outer.html calls history.back()
6. We end up in Page::goToItem, which calls FrameLoader::stopAllLoaders
7. We recurse through the nested frame loaders, and once we stop the load of hung-page.php, we end up triggering the onload handler of outer.html (due to FrameLoader::complete calling checkComplete in the parent)
8. The onload handler of outer.html has a history.back() call
9. We call BackForwardListImpl::itemAtIndex to see if we can still go back.

That recreates the stack trace from https://crbug.com/chromium/59554#c9, where we end up deref()-ing to 0 the HistoryItem that's on the stack (in the Page::goToItem frame).

### mi...@chromium.org (2010-10-27)

Fix will be upstream, filed http://webkit.org/b/48477.

### js...@chromium.org (2010-11-01)

Flagging as security. We'll merge to beta (and stable if we have another refresh).

### in...@chromium.org (2010-11-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-11-02)

Fixed in http://trac.webkit.org/changeset/71170. Needs to be merged to 552.

### mi...@chromium.org (2010-11-02)

Abhishek, were you going to merge this, or should I?

### in...@chromium.org (2010-11-02)

Mihai, i will merge this to 552 once the bots are green. Seems a low risk merge.

### in...@chromium.org (2010-11-02)

merged to 552 in r71176.

### in...@chromium.org (2010-11-03)

Mihai, i totally forgot to check the compile after this merge. And broke the beta 552 build. can you please do a hand merge of this after the beta goes out.

third_party/WebKit/WebCore/loader/NavigationScheduler.cpp: In member function â€˜void WebCore::NavigationScheduler::scheduleHistoryNavigation(int)â€™:
third_party/WebKit/WebCore/loader/NavigationScheduler.cpp:344: error: â€˜class WebCore::Pageâ€™ has no member named â€˜backForwardâ€™
third_party/WebKit/WebCore/loader/NavigationScheduler.cpp:345: error: invalid use of incomplete type â€˜struct WebCore::BackForwardControllerâ€™
third_party/WebKit/WebCore/page/Page.h:41: error: forward declaration of â€˜struct WebCore::BackForwardControllerâ€™
third_party/WebKit/WebCore/loader/NavigationScheduler.cpp:345: error: invalid use of incomplete type â€˜struct WebCore::BackForwardControllerâ€™
third_party/WebKit/WebCore/page/Page.h:41: error: forward declaration of â€˜struct WebCore::BackForwardControllerâ€™

### mi...@chromium.org (2010-11-05)

Merged to 552 with http://trac.webkit.org/changeset/71368, I believe this should build cleanly (where do I check that, http://chrome-master.mtv:8010/console?)

### in...@chromium.org (2010-11-05)

Mihai, Waterfall is at http://chrome-master.mtv:8010/waterfall, please look at the beta ones for all platforms.

### mi...@chromium.org (2010-11-05)

Thanks (things appear to be building).

### js...@chromium.org (2010-11-05)

Excellent. I was worried this would get bumped to m9. Thanks for taking care of it @mihaip.

### sc...@gmail.com (2010-11-29)

@geki007: with what name might we credit you in our release notes?

### sc...@gmail.com (2010-11-29)

@geki007: thanks very much for your help with filing this bug!

Although not filed originally as a security issue, we investigated and found it to have security impact. Therefore, we found this report very useful :)

We'd like to offer you a $500 Chromium Security Reward for your help. Congratulations!
To get further rewards in the future:
- Be sure to file possible security issues (such as tab crashes) under the security bug template.
- Have a look at our help on reporting crash bugs: http://www.chromium.org/for-testers/bug-reporting-guidelines/reporting-crash-bug
(Details from here help determine whether something is a security bug or in fact harmless)
- We often pay bigger rewards for a simple, reduced piece of HTML as a test case.

Good luck :)

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ge...@gmail.com (2010-11-29)

@scarybeasts:
I reported a lot of bugs and now i get some money, that's like christmas ;)
Thank you, getting money makes bug reporting much more attractive!
Next time i will follow your 3 points to get more money :)

I think you need my realname, respectively it is cooler to see it in your release notes.
My name is: Stefan Troger

And at last the most important question: How i get the money? :)

### js...@chromium.org (2010-11-29)

Just to clarify, the security bug reporting guidelines are located here:
http://www.chromium.org/Home/chromium-security/reporting-security-bugs

When reporting security bugs in the future, be sure to follow these guidelines to improve your chances of a reward.


### ge...@gmail.com (2010-11-29)

thanks for the clarification, didn't know this page

### sc...@gmail.com (2010-11-29)

E-mail cevans@chromium.org to start the process of collecting the reward -- although payment usually occurs once the fix is released. This should occur this week or next.

### sc...@gmail.com (2011-01-10)

Payment is now in the electronic system...

### ge...@gmail.com (2011-01-10)

hope i will get it in a few days :)

### ge...@gmail.com (2011-01-19)

thank's a lot, i got the money :)!


just a hint: shouldn't the Status be Fixed and Released!?

### la...@chromium.org (2011-03-19)

Chrome Version : 8.0.558.0 (Developer Build 62906), WinXP  

URLs (if applicable) : <http://www.volkswagen.de/vwcms/master_public/virtualmaster/de3/modelle/passat.html>  

**Other browsers tested:**  

**Add OK or FAIL after other browsers where you have tested this issue:**  

**Safari 4:**  

**Firefox 3.x:**  

**IE 7:**  

**IE 8:**

**What steps will reproduce the problem?**

1. go to the url
2. click "Konfigurator Passat Variant"
3. in the new window click "comfort"
4. do a history back (with the back key on your keyboard)

**What is the expected result?**  

goes back

**What happens instead?**  

AW, snap! on the popup and normal window

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/59554?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083878)*
