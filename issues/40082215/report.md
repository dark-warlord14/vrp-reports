# Security issue in SVGUseElement::buildShadowTree

| Field | Value |
|-------|-------|
| **Issue ID** | [40082215](https://issues.chromium.org/issues/40082215) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | wo...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2010-07-20 |
| **Bounty** | $500.00 |

## Description

Hi, these two I sent them to ZDI severval months ago , but ZDI refused, so I sent them to google. I tested , it works on newest chrome stable version.

wushi




## Attachments

- [45.rar](attachments/45.rar) (application/x-rar, 3.3 KB)
- [47.rar](attachments/47.rar) (application/x-rar, 2.7 KB)
- [1.xhtml](attachments/1.xhtml) (text/html; charset=us-ascii, 5.3 KB)
- [svg_use.xhtml](attachments/svg_use.xhtml) (text/html, 334 B)

## Timeline

### in...@chromium.org (2010-07-20)

Lets use it to track 47.rar attachments. Other attachment is handled in 49628. Need to do more analysis on this.

Breaks at
    shadowRoot->appendChild(newChild.release(), ec);
    wheree newChild is NULL.
 	00000002()	
>WebCore::SVGUseElement::buildShadowTree(WebCore::SVGShadowTreeRootElement * shadowRoot=0x088ab780, WebCore::SVGElement * target=0x0886fe00, WebCore::SVGElementInstance * targetInstance=0x0b0b7f80)  Line 776 + 0x2b bytes	C++
 WebCore::SVGUseElement::buildShadowAndInstanceTree(WebCore::SVGShadowTreeRootElement * shadowRoot=0x088ab780)  Line 538	C++
 WebCore::RenderSVGShadowTreeRootContainer::updateFromElement()  Line 80	C++
 WebCore::updateFromElementCallback(WebCore::Node * node=0x04edaa00)  Line 601 + 0x12 bytes	C++
 WebCore::ContainerNode::dispatchPostAttachCallbacks()  Line 630 + 0x9 bytes	C++
 WebCore::ContainerNode::resumePostAttachCallbacks()  Line 598	C++
 WebCore::Element::attach()  Line 828	C++
 WebCore::ContainerNode::insertBefore(WTF::PassRefPtr<WebCore::Node> newChild={m_document=0x0b7cb000 m_previous=0x00000000 m_next=0x0b3e2c80 ...}, WebCore::Node * refChild=0x0b3e2c80, int & ec=0, bool shouldLazyAttach=false)  Line 167 + 0x12 bytes	C++
 WebCore::XMLDocumentParser::insertErrorMessageBlock()  Line 314	C++
 WebCore::XMLDocumentParser::end()  Line 224	C++
 WebCore::XMLDocumentParser::finish()  Line 240	C++
 WebCore::Document::finishParsing()  Line 2055 + 0x20 bytes	C++
 WebCore::DocumentWriter::endIfNotLoadingMainResource()  Line 222	C++
 WebCore::DocumentWriter::end()  Line 207	C++
 WebCore::DocumentLoader::finishedLoading()  Line 270	C++
 WebCore::FrameLoader::finishedLoading()  Line 2223	C++
 WebCore::MainResourceLoader::didFinishLoading()  Line 435	C++
 WebCore::ResourceLoader::didFinishLoading(WebCore::ResourceHandle * __formal=0x082ed030)  Line 443 + 0xf bytes	C++
 WebCore::ResourceHandleInternal::didFinishLoading(WebKit::WebURLLoader * __formal=0x082f6718)  Line 191 + 0x25 bytes	C++
 webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest(const URLRequestStatus & status={...}, const std::basic_string<char,std::char_traits<char>,std::allocator<char> > & security_info="")  Line 604 + 0x1e bytes	C++
 ResourceDispatcher::OnRequestComplete(int request_id=34, const URLRequestStatus & status={...}, const std::basic_string<char,std::char_traits<char>,std::allocator<char> > & security_info="")  Line 467 + 0x17 bytes	C++
 DispatchToMethod<ResourceDispatcher,void (__thiscall ResourceDispatcher::*)(int,URLRequestStatus const &,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &),int,URLRequestStatus,std::basic_string<char,std::char_traits<char>,std::allocator<char> > >(ResourceDispatcher * obj=0x00bb5320, void (int, const URLRequestStatus &, const std::basic_string<char,std::char_traits<char>,std::allocator<char> > &)* method=0x54fd4340, const Tuple3<int,URLRequestStatus,std::basic_string<char,std::char_traits<char>,std::allocator<char> > > & arg={...})  Line 435 + 0x1c bytes	C++
 IPC::MessageWithTuple<Tuple3<int,URLRequestStatus,std::basic_string<char,std::char_traits<char>,std::allocator<char> > > >::Dispatch<ResourceDispatcher,void (__thiscall ResourceDispatcher::*)(int,URLRequestStatus const &,std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &)>(const IPC::Message * msg=class=16, index=54, ResourceDispatcher * obj=0x00bb5320, void (int, const URLRequestStatus &, const std::basic_string<char,std::char_traits<char>,std::allocator<char> > &)* func=0x54fd4340)  Line 1043 + 0x11 bytes	C++
 ResourceDispatcher::DispatchMessageW(const IPC::Message & message=class=16, index=54)  Line 536 + 0x12 bytes	C++
 ResourceDispatcher::OnMessageReceived(const IPC::Message & message=class=16, index=54)  Line 303	C++
 ChildThread::OnMessageReceived(const IPC::Message & msg=class=16, index=54)  Line 124 + 0x19 bytes	C++
 IPC::ChannelProxy::Context::OnDispatchMessage(const IPC::Message & message=class=16, index=54)  Line 206 + 0x19 bytes	C++
 DispatchToMethod<IPC::ChannelProxy::Context,void (__thiscall IPC::ChannelProxy::Context::*)(IPC::Message const &),IPC::Message>(IPC::ChannelProxy::Context * obj=0x00c5d900, void (const IPC::Message &)* method=0x53eddae0, const Tuple1<IPC::Message> & arg={...})  Line 422 + 0xf bytes	C++
 RunnableMethod<IPC::ChannelProxy::Context,void (__thiscall IPC::ChannelProxy::Context::*)(IPC::Message const &),Tuple1<IPC::Message> >::Run()  Line 326 + 0x1e bytes	C++
 MessageLoop::RunTask(Task * task=0x0b36e980)  Line 409 + 0xf bytes	C++
 MessageLoop::DeferOrRunPendingTask(const MessageLoop::PendingTask & pending_task={...})  Line 421	C++
 MessageLoop::DoWork()  Line 525 + 0xc bytes	C++
 base::MessagePumpForUI::DoRunLoop()  Line 203 + 0x1d bytes	C++
 base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate=0x0521faa0, base::MessagePumpWin::Dispatcher * dispatcher=0x00000000)  Line 52 + 0xf bytes	C++
 base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate=0x0521faa0)  Line 79 + 0x1c bytes	C++
 MessageLoop::RunInternal()  Line 257 + 0x2a bytes	C++
 MessageLoop::RunHandler()  Line 230	C++
 MessageLoop::Run()  Line 208	C++
 base::Thread::Run(MessageLoop * message_loop=0x0521faa0)  Line 137	C++
 base::Thread::ThreadMain()  Line 160 + 0x16 bytes	C++
 `anonymous namespace'::ThreadFunc(void * closure=0x00c6f780)  Line 26 + 0xf bytes	C++
 	kernel32.dll!@BaseThreadInitThunk@12()  + 0xe bytes	
 	ntdll.dll!___RtlUserThreadStart@8()  + 0x23 bytes	
 	ntdll.dll!__RtlUserThreadStart@8()  + 0x1b bytes	


### js...@chromium.org (2010-07-20)

Here's a reduction. It's another SVG USE element bug. The crash is an exec NULL, so it might an arbitrary exec (or harmless). I should know better shortly.


### js...@chromium.org (2010-07-20)

Looks like a stale pointer. I have to dig a bit more, but a style recalculation triggers an early deletion of the SVGGElement exposed by the SVGShadowTreeRootElement.

I've filed upstream with more details: 
https://bugs.webkit.org/show_bug.cgi?id=42659


### sc...@gmail.com (2010-07-22)

Thank you wushi! We have fixed both of these already. We'll get the fixes out to users in the next release after this week's release.

This qualifies for a $500 reward (as does the other one, which I'll tag separately).

One comment: we're now looking at rewarding $1000 for bugs like this, if the bug report quality is high. If you had taken the big HTML demo file and reduced it to the simplest test case, it would have likely been worth $1000.

### js...@chromium.org (2010-07-22)

Landed as: http://trac.webkit.org/changeset/63865


### js...@chromium.org (2010-07-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-07-26)

merged to 472. forgot the bug no, so adding the commit info..

Merge 63865 - 2010-07-21 Justin Schuh <jschuh@chromium.org>

Reviewed by Oliver Hunt.

Prevent DeleteButtonController enable state from changing when not editing
https://bugs.webkit.org/show_bug.cgi?id=42659

Test: svg/custom/use-invalid-html.xhtml

* dom/ContainerNode.cpp:
(WebCore::ContainerNode::cloneChildNodes):
2010-07-21 Justin Schuh <jschuh@chromium.org>

Reviewed by Oliver Hunt.

Prevent DeleteButtonController enable state from changing when not editing
https://bugs.webkit.org/show_bug.cgi?id=42659

* svg/custom/use-invalid-html-expected.txt: Added.
* svg/custom/use-invalid-html.xhtml: Added.


TBR=jschuh@chromium.org

Committed: http://src.chromium.org/viewvc/chrome?view=rev&revision=53682

### ch...@gmail.com (2010-08-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-17)

We did merge this to 375:

Merge 63865 - 2010-07-21  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Oliver Hunt.

        Prevent DeleteButtonController enable state from changing when not editing
        https://bugs.webkit.org/show_bug.cgi?id=42659

        Test: svg/custom/use-invalid-html.xhtml

        * dom/ContainerNode.cpp:
        (WebCore::ContainerNode::cloneChildNodes):
2010-07-21  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Oliver Hunt.

        Prevent DeleteButtonController enable state from changing when not editing
        https://bugs.webkit.org/show_bug.cgi?id=42659

        * svg/custom/use-invalid-html-expected.txt: Added.
        * svg/custom/use-invalid-html.xhtml: Added.


Review URL: http://codereview.chromium.org/3007044

### [Deleted User] (2010-08-18)

[Empty comment from Monorail migration]

### ro...@chromium.org (2010-08-18)

Works fine on Mac 5.0.375.127 (Official Build 55887).
Browser doesn't crash.

### [Deleted User] (2010-08-18)

Works fine with Google Chrome 5.0.375.127 (Official Build 55887) on Windows.

On Linux Ubuntu 9.04 with Google Chrome 5.0.375.127 (Official Build 55887),
renderer crashes with 1.xhtml from https://crbug.com/chromium/49596#c1 but doesn't crash with svg_use.xhtml from https://crbug.com/chromium/49596#c2

Crash reports haven't got uploaded yet but you can find them @ 
http://crash/reportdetail?reportid=4d0e41ca16494e63
http://crash/reportdetail?reportid=ecea9e26556d6dbc

### [Deleted User] (2010-08-18)

I don't see the crashed thread in the reports. But it should be fairly easy to repro.

### js...@chromium.org (2010-08-18)

@sunandt, so far I can't get a repro with either of the 1.xhtml files on 5.0.375.127 on Windows. And the linked crash reports are from renderer startup/shutdown hangs, which really doesn't make sense for this bug. 

Specifically which of the files are you referring to, and can you provide anymore detail?


### [Deleted User] (2010-08-18)

jschuh, this works fine on Windows. Renderer crash can be seen on Linux. Please see https://crbug.com/chromium/49596#c12. I'm not sure why the stack trace doesn't show up in crash/.

### js...@chromium.org (2010-08-18)

@sunandt - Please tell me which file you are testing. There are two archives and both have a 1.xhtml file. There's no useful crash data and we need something to work from.


### js...@chromium.org (2010-08-18)

Nevermind. I see it's the file from https://crbug.com/chromium/49596#c1, not from the original archive. Sorry for the confusion.

### js...@chromium.org (2010-08-18)

It looks like there's an entirely different bug hidden in all the fuzzer junk. It doesn't show up on Windows or Mac without several minutes of automatic reloading. I'll try to isolate it and open another bug.


### js...@chromium.org (2010-08-19)

After a lot of poking around I found that the original repro can very infrequently trigger https://crbug.com/chromium/51252. I'll leave a note in that bug to verify against the repro here after we get a fix in for https://crbug.com/chromium/51252.

Do not make this visible until https://crbug.com/chromium/51252 is patched.


### sc...@gmail.com (2010-08-25)

Payment in the electronic system.

Hey @wooshi, we should not have actually paid out on this one. We require reports to be sent to us and only us. Your first comment mentions offering the bug first to ZDI.

However the mistake is ours so we did of course still pay.

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

This issue was migrated from crbug.com/chromium/49596?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082215)*
