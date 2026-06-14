# Integer overflow in style elements

| Field | Value |
|-------|-------|
| **Issue ID** | [40088764](https://issues.chromium.org/issues/40088764) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-03-11 |
| **Bounty** | $1,337.00 |

## Description

https://bugs.webkit.org/show_bug.cgi?id=56150

## Attachments

- [cr.html](attachments/cr.html) (text/html; charset=us-ascii, 1.1 KB)

## Timeline

### sc...@gmail.com (2011-03-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-11)

[Empty comment from Monorail migration]

### ke...@google.com (2011-03-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-11)

committed - http://trac.webkit.org/changeset/80787
m10 merge - http://trac.webkit.org/changeset/80788
m11 merge - http://trac.webkit.org/changeset/80790

### sc...@gmail.com (2011-03-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-11)

Testcase.

### in...@chromium.org (2011-03-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-03-11)

Confirmed fixed. I downloaded google-chrome-stable-10.0.648.133-77742.i386.rpm from the build output, ran the exploit, and I get a clean CRASH()-based sad-tab:


Program received signal SIGSEGV, Segmentation fault.
0x09c8f2d1 in ?? ()

(gdb) disass $eip,$eip+20
Dump of assembler code from 0x9c8f2d1 to 0x9c8f2e5:
=> 0x09c8f2d1:	movl   $0x0,0xbbadbeef
   0x09c8f2db:	call   *%eax

(gdb) i r
eax            0x0	0


### [Deleted User] (2011-03-11)

We are not crashing in memcpy anymore. We are deliberately crashing the renderer in WebCore::StyleElement::process(WebCore::Element *)

Stack Trace
-----------
Thread 0 *CRASHED* ( EXCEPTION_BREAKPOINT @ 0x6b369942 )

0x6b369942	 [chrome.dll	 - styleelement.cpp:107]	WebCore::StyleElement::process(WebCore::Element *)
0x6b369887	 [chrome.dll	 - styleelement.cpp:61]	WebCore::StyleElement::insertedIntoDocument(WebCore::Document *,WebCore::Element *)
0x6af7e410	 [chrome.dll	 - htmlstyleelement.cpp:75]	WebCore::HTMLStyleElement::insertedIntoDocument()
0x6acc8396	 [chrome.dll	 - containernode.cpp:1019]	WebCore::notifyChildInserted
0x6acc7875	 [chrome.dll	 - containernode.cpp:608]	WebCore::ContainerNode::appendChild(WTF::PassRefPtr<WebCore::Node>,int &,bool)
0x6ac648b8	 [chrome.dll	 - node.cpp:591]	WebCore::Node::appendChild(WTF::PassRefPtr<WebCore::Node>,int &,bool)
0x6add278e	 [chrome.dll	 - v8nodecustom.cpp:123]	WebCore::V8Node::appendChildCallback(v8::Arguments const &)
0x6b497df9	 [chrome.dll	 - builtins.cc:1065]	v8::internal::HandleApiCallHelper<0>
0x6b49812f	 [chrome.dll	 + 0x00d8812f]	
0x2f807112			
0x2f801238			
0x2f7f2a01			
0x6b466948	 [chrome.dll	 - execution.cc:97]	v8::internal::Invoke
0x6b466a04	 [chrome.dll	 - execution.cc:123]	v8::internal::Execution::Call(v8::internal::Handle<v8::internal::JSFunction>,v8::internal::Handle<v8::internal::Object>,int,v8::internal::Object * * *,bool *)
0x6b418e27	 [chrome.dll	 - api.cc:1314]	v8::Script::Run()
0x6ac45e90	 [chrome.dll	 - frame.cpp:577]	WebCore::Frame::keepAlive()
0x6ad3733c	 [chrome.dll	 - v8proxy.cpp:371]	WebCore::V8Proxy::evaluate(WebCore::ScriptSourceCode const &,WebCore::Node *)
0x6ac6373b	 [chrome.dll	 - scriptcontroller.cpp:242]	WebCore::ScriptController::evaluate(WebCore::ScriptSourceCode const &,WebCore::ShouldAllowXSS)
0x6acc1d5e	 [chrome.dll	 - scriptcontrollerbase.cpp:60]	WebCore::ScriptController::executeScript(WebCore::ScriptSourceCode const &,WebCore::ShouldAllowXSS)
0x6add5baa	 [chrome.dll	 - scriptelement.cpp:216]	WebCore::ScriptElement::executeScript(WebCore::ScriptSourceCode const &)
0x6af924e4	 [chrome.dll	 - htmlscriptrunner.cpp:316]	WebCore::HTMLScriptRunner::runScript(WebCore::Element *,WTF::TextPosition<WTF::OneBasedNumber> const &)
0x6af6cbd5	 [chrome.dll	 - htmldocumentparser.cpp:244]	WebCore::HTMLDocumentParser::pumpTokenizer(WebCore::HTMLDocumentParser::SynchronousMode)
0x6af6ca28	 [chrome.dll	 - htmldocumentparser.cpp:169]	WebCore::HTMLDocumentParser::pumpTokenizerIfPossible(WebCore::HTMLDocumentParser::SynchronousMode)
0x6af6ce11	 [chrome.dll	 - htmldocumentparser.cpp:325]	WebCore::HTMLDocumentParser::append(WebCore::SegmentedString const &)
0x6add84a6	 [chrome.dll	 - decodeddatadocumentparser.cpp:54]	WebCore::DecodedDataDocumentParser::appendBytes(WebCore::DocumentWriter *,char const *,int,bool)
0x6acc40ca	 [chrome.dll	 - documentwriter.cpp:200]	WebCore::DocumentWriter::addData(char const *,int,bool)
0x6acc0bed	 [chrome.dll	 - documentloader.cpp:310]	WebCore::DocumentLoader::commitData(char const *,int)
0x6afa09f3	 [chrome.dll	 - webframeimpl.cpp:1040]	WebKit::WebFrameImpl::commitDocumentData(char const *,unsigned int)
0x6afb84c9	 [chrome.dll	 - frameloaderclientimpl.cpp:1066]	WebKit::FrameLoaderClientImpl::committedLoad(WebCore::DocumentLoader *,char const *,int)
0x6acc0b6e	 [chrome.dll	 - documentloader.cpp:295]	WebCore::DocumentLoader::commitLoad(char const *,int)
...... (6 stack frames dropped.)
0x6ab9f626	 [chrome.dll	 - resource_dispatcher.cc:372]	ResourceDispatcher::OnReceivedData(IPC::Message const &,int,void *,int)
0x6ab9fbcf	 [chrome.dll	 - resource_dispatcher.cc:528]	ResourceDispatcher::DispatchMessageW(IPC::Message const &)
0x6ab9f428	 [chrome.dll	 - resource_dispatcher.cc:297]	ResourceDispatcher::OnMessageReceived(IPC::Message const &)
0x6ab8f71f	 [chrome.dll	 - child_thread.cc:144]	ChildThread::OnMessageReceived(IPC::Message const &)
0x6a9bebde	 [chrome.dll	 - task.h:331]	RunnableMethod<cloud_print::PrintSystemWin::PrinterCapsHandler,void ( cloud_print::PrintSystemWin::PrinterCapsHandler::*)(scoped_refptr<base::MessageLoopProxy> const &),Tuple1<scoped_refptr<base::MessageLoopProxy> > >::Run()
0x6a7dfdf3	 [chrome.dll	 - message_loop.cc:356]	MessageLoop::RunTask(Task *)
0x6a7dfe7a	 [chrome.dll	 - message_loop.cc:365]	MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const &)
0x6a7e022c	 [chrome.dll	 - message_loop.cc:558]	MessageLoop::DoWork()
0x6a7f7026	 [chrome.dll	 - message_pump_default.cc:50]	base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x6a7dfd74	 [chrome.dll	 - message_loop.cc:331]	MessageLoop::RunInternal()
0x6a7dfcf9	 [chrome.dll	 - message_loop.cc:304]	MessageLoop::RunHandler()
0x6a7dfbed	 [chrome.dll	 - message_loop.cc:234]	MessageLoop::Run()
0x6a80dff4	 [chrome.dll	 - renderer_main.cc:300]	RendererMain(MainFunctionParams const &)
0x6a713fb8	 [chrome.dll	 - chrome_main.cc:925]	ChromeMain
0x013e3dd4	 [chrome.exe	 - client_util.cc:280]	MainDllLoader::Launch(HINSTANCE__ *,sandbox::SandboxInterfaceInfo *)
0x013e419e	 [chrome.exe	 - chrome_exe_main_win.cc:46]	wWinMain
0x01429bec	 [chrome.exe	 - crt0.c:263]	__tmainCRTStartup
0x75663676	 [kernel32.dll	 + 0x00013676]	BaseThreadInitThunk
0x779b9f01	 [ntdll.dll	 + 0x00039f01]	__RtlUserThreadStart
0x779b9ed4	 [ntdll.dll	 + 0x00039ed4]	_RtlUserThreadStart

Verified with Google Chrome 10.0.648.133 (Official Build 77742) on Win7.

### [Deleted User] (2011-03-11)

Verified with Google Chrome 10.0.648.133 (Official Build 77742) on Mac.

Stack Trace
------------
Thread 0 *CRASHED* ( EXC_BAD_ACCESS / KERN_INVALID_ADDRESS @ 0xffffffffbbadbeef )

0x04fe4ad7	 [Google Chrome Framework	 - StyleElement.cpp:107]	WebCore::StyleElement::process
0x04a4feb7	 [Google Chrome Framework	 - HTMLStyleElement.cpp:75]	WebCore::HTMLStyleElement::insertedIntoDocument
0x04f731da	 [Google Chrome Framework	 - ContainerNode.cpp:1019]	WebCore::notifyChildInserted
0x04f75140	 [Google Chrome Framework	 - ContainerNode.cpp:608]	WebCore::ContainerNode::appendChild
0x04fbc7c7	 [Google Chrome Framework	 - Node.cpp:591]	WebCore::Node::appendChild
0x04e92954	 [Google Chrome Framework	 - V8NodeCustom.cpp:123]	WebCore::V8Node::appendChildCallback
0x042799cc	 [Google Chrome Framework	 - builtins.cc:1065]	v8::internal::Builtin_HandleApiCall
0x006b22ad			
0x006c8bd2			
0x006c3818			
0x006b4a01			
0x0429ae3c	 [Google Chrome Framework	 - execution.cc:96]	v8::internal::Invoke
0x0429b356	 [Google Chrome Framework	 - execution.cc:123]	v8::internal::Execution::Call
0x0426409b	 [Google Chrome Framework	 - api.cc:1314]	v8::Script::Run
0x04eba96b	 [Google Chrome Framework	 - V8Proxy.cpp:415]	WebCore::V8Proxy::runScript
0x04ebacd0	 [Google Chrome Framework	 - V8Proxy.cpp:371]	WebCore::V8Proxy::evaluate
0x04ea2229	 [Google Chrome Framework	 - ScriptController.cpp:242]	WebCore::ScriptController::evaluate
0x04e6fbd0	 [Google Chrome Framework	 - ScriptControllerBase.cpp:60]	WebCore::ScriptController::executeScript
0x04fd9347	 [Google Chrome Framework	 - ScriptElement.cpp:216]	WebCore::ScriptElement::executeScript
0x04aa321d	 [Google Chrome Framework	 - HTMLScriptRunner.cpp:316]	WebCore::HTMLScriptRunner::runScript
0x04aa3931	 [Google Chrome Framework	 - HTMLScriptRunner.cpp:173]	WebCore::HTMLScriptRunner::execute
0x04a97795	 [Google Chrome Framework	 - HTMLDocumentParser.cpp:199]	WebCore::HTMLDocumentParser::runScriptsForPausedTreeBuilder
0x04a98db8	 [Google Chrome Framework	 - HTMLDocumentParser.cpp:244]	WebCore::HTMLDocumentParser::pumpTokenizer
0x04a99426	 [Google Chrome Framework	 - HTMLDocumentParser.cpp:169]	WebCore::HTMLDocumentParser::append
0x04f79ce9	 [Google Chrome Framework	 - DecodedDataDocumentParser.cpp:54]	WebCore::DecodedDataDocumentParser::appendBytes
0x05136300	 [Google Chrome Framework	 - DocumentWriter.cpp:200]	WebCore::DocumentWriter::addData
0x0512be3b	 [Google Chrome Framework	 - DocumentLoader.cpp:310]	WebCore::DocumentLoader::commitData
0x0498d781	 [Google Chrome Framework	 - FrameLoaderClientImpl.cpp:1066]	WebKit::FrameLoaderClientImpl::committedLoad
0x0512b9ef	 [Google Chrome Framework	 - DocumentLoader.cpp:295]	WebCore::DocumentLoader::commitLoad
0x0516a3c2	 [Google Chrome Framework	 - ResourceLoader.cpp:277]	WebCore::ResourceLoader::didReceiveData
...... (9 stack frames dropped.)
0x03ce348b	 [Google Chrome Framework	 - message_loop.cc:356]	MessageLoop::RunTask
0x03ce363d	 [Google Chrome Framework	 - message_loop.cc:365]	MessageLoop::DeferOrRunPendingTask
0x03ce427a	 [Google Chrome Framework	 - message_loop.cc:558]	MessageLoop::DoWork
0x03cbb953	 [Google Chrome Framework	 - message_pump_mac.mm:296]	base::MessagePumpCFRunLoopBase::RunWorkSource
0x932f43c4	 [CoreFoundation	 + 0x000733c4]	CFRunLoopRunSpecific
0x932f4aa7	 [CoreFoundation	 + 0x00073aa7]	CFRunLoopRunInMode
0x900332ab	 [HIToolbox	 + 0x000302ab]	RunCurrentEventLoopInMode
0x900330c4	 [HIToolbox	 + 0x000300c4]	ReceiveNextEventCommon
0x90032f38	 [HIToolbox	 + 0x0002ff38]	BlockUntilNextEventMatchingListInMode
0x954216d4	 [AppKit	 + 0x000406d4]	_DPSNextEvent
0x95420f87	 [AppKit	 + 0x0003ff87]	-[NSApplication nextEventMatchingMask:untilDate:inMode:dequeue:]
0x95419f9e	 [AppKit	 + 0x00038f9e]	-[NSApplication run]
0x03cbb6d4	 [Google Chrome Framework	 - message_pump_mac.mm:678]	base::MessagePumpNSApplication::DoRun
0x03cbab89	 [Google Chrome Framework	 - message_pump_mac.mm:212]	base::MessagePumpCFRunLoopBase::Run
0x03ce4123	 [Google Chrome Framework	 - message_loop.cc:331]	MessageLoop::Run
0x03c49b00	 [Google Chrome Framework	 - renderer_main.cc:300]	RendererMain
0x033e7cae	 [Google Chrome Framework	 - chrome_main.cc:598]	ChromeMain
0x00001f57	 [Google Chrome Helper	 - chrome_exe_main_mac.mm:16]	main
0x00001f15	 [Google Chrome Helper	 + 0x00000f15]

Mac report @ http://crash/reportdetail?reportid=a403ebe4652736fb

Win report @ http://crash/reportdetail?reportid=298a8b3080ac6dd3

### sc...@gmail.com (2011-03-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2012-01-31)

Payment in progress... better late than never

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/75712?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088764)*
