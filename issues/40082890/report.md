# Geolocation use after free

| Field | Value |
|-------|-------|
| **Issue ID** | [40082890](https://issues.chromium.org/issues/40082890) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Geolocation |
| **Reporter** | in...@chromium.org |
| **Assignee** | jo...@chromium.org |
| **Created** | 2010-08-26 |
| **Bounty** | $500.00 |

## Description

credit: kuzzcc

Kuzzcc emailed me on this again. Looked like a dup of previous bugs. But then I synced to latest trunk 7.0.506.0 (57453) and can reproduce the use after free.

There is clear memory corruption in m_service..

line 257: m_lastPosition = m_service->lastPosition();
Stacktrace::
 	632e656c()	
>name=WebCore::Geolocation::lastPosition()  Line 257 + 0x20 bytesname=
 name=WebCore::Geolocation::setIsAllowed(bool allowed=true)  Line 450 + 0x8 bytesname=
 name=WebCore::GeolocationServiceChromium::setIsAllowed(bool allowed=true)  Line 49name=
 name=WebKit::WebGeolocationServiceBridgeImpl::setIsAllowed(bool allowed=true)  Line 156name=
 name=GeolocationDispatcher::OnGeolocationPermissionSet(int bridge_id=2, bool allowed=true)  Line 86 + 0x13 bytesname=
 name=DispatchToMethod<GeolocationDispatcher,void (__thiscall GeolocationDispatcher::*)(int,bool),int,bool>(GeolocationDispatcher * obj=0x07e05690, void (int, bool)* method=0x50661220, const Tuple2<int,bool> & arg={...})  Line 554 + 0x16 bytesname=
 name=IPC::MessageWithTuple<Tuple2<int,bool> >::Dispatch<GeolocationDispatcher,void (__thiscall GeolocationDispatcher::*)(int,bool)>(const IPC::Message * msg=class=16, index=167, GeolocationDispatcher * obj=0x07e05690, void (int, bool)* func=0x50661220)  Line 944 + 0x11 bytesname=
 name=GeolocationDispatcher::OnMessageReceived(const IPC::Message & message=class=16, index=167)  Line 31 + 0x12 bytesname=
 name=RenderView::OnMessageReceived(const IPC::Message & message=class=16, index=167)  Line 673 + 0x2b bytesname=
 name=MessageRouter::RouteMessage(const IPC::Message & msg=class=16, index=167)  Line 40 + 0x13 bytesname=
 name=MessageRouter::OnMessageReceived(const IPC::Message & msg=class=16, index=167)  Line 31 + 0x13 bytesname=
 name=ChildThread::OnMessageReceived(const IPC::Message & msg=class=16, index=167)  Line 163 + 0x17 bytesname=
 name=IPC::ChannelProxy::Context::OnDispatchMessage(const IPC::Message & message=class=16, index=167)  Line 206 + 0x19 bytesname=
 name=DispatchToMethod<IPC::ChannelProxy::Context,void (__thiscall IPC::ChannelProxy::Context::*)(IPC::Message const &),IPC::Message>(IPC::ChannelProxy::Context * obj=0x04b58180, void (const IPC::Message &)* method=0x502a6530, const Tuple1<IPC::Message> & arg={...})  Line 547 + 0xf bytesname=
 name=RunnableMethod<IPC::ChannelProxy::Context,void (__thiscall IPC::ChannelProxy::Context::*)(IPC::Message const &),Tuple1<IPC::Message> >::Run()  Line 327 + 0x1e bytesname=
 name=MessageLoop::RunTask(Task * task=0x05775d00)  Line 408 + 0xf bytesname=
 name=MessageLoop::DeferOrRunPendingTask(const MessageLoop::PendingTask & pending_task={...})  Line 420name=
 name=MessageLoop::DoWork()  Line 524 + 0xc bytesname=
 name=base::MessagePumpForUI::DoRunLoop()  Line 202 + 0x1d bytesname=
 name=base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate=0x050cfb64, base::MessagePumpWin::Dispatcher * dispatcher=0x00000000)  Line 51 + 0xf bytesname=
 name=base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate=0x050cfb64)  Line 80 + 0x1c bytesname=
 name=MessageLoop::RunInternal()  Line 256 + 0x2a bytesname=
 name=MessageLoop::RunHandler()  Line 229name=
 name=MessageLoop::Run()  Line 207name=
 name=base::Thread::Run(MessageLoop * message_loop=0x050cfb64)  Line 141name=
 name=base::Thread::ThreadMain()  Line 164 + 0x16 bytesname=
 name=`anonymous namespace'::ThreadFunc(void * closure=0x00e09d20)  Line 26 + 0xf bytesname=
 	kernel32.dll!@BaseThreadInitThunk@12()  + 0xe bytes	
 	ntdll.dll!___RtlUserThreadStart@8()  + 0x23 bytes	
 	ntdll.dll!__RtlUserThreadStart@8()  + 0x1b bytes	

Will take a closer look tmrw. testcase enclosed.
can launch testcase from http://www/~aarya/no_crawl/index.htm (note that this would go away sooner or later)

## Attachments

- [geo.htm](attachments/geo.htm) (text/plain; charset=us-ascii, 186 B)
- [index.htm](attachments/index.htm) (text/plain; charset=us-ascii, 119 B)
- [tmpdiff](attachments/tmpdiff) (text/x-diff; charset=us-ascii, 1.7 KB)

## Timeline

### in...@chromium.org (2010-08-26)

ignore the name= junk in stacktrace. looks like i messed up when clearing some stuff.

### in...@chromium.org (2010-08-26)

Taking an active look at it, i have some idea of where the problem can be fixed. Just a fyi, another crash stacktrace is

  if (bridge) {
    bridge->setIsAllowed(allowed);
  }
 	07ff03f0()	
>GeolocationDispatcher::OnGeolocationPermissionSet(int bridge_id=2, bool allowed=true)  Line 86 + 0x13 bytes
 DispatchToMethod<GeolocationDispatcher,void (__thiscall GeolocationDispatcher::*)(int,bool),int,bool>(GeolocationDispatcher * obj=0x08352af0, void (int, bool)* method=0x50661220, const Tuple2<int,bool> & arg={...})  Line 554 + 0x16 bytes
 IPC::MessageWithTuple<Tuple2<int,bool> >::Dispatch<GeolocationDispatcher,void (__thiscall GeolocationDispatcher::*)(int,bool)>(const IPC::Message * msg=class=16, index=167, GeolocationDispatcher * obj=0x08352af0, void (int, bool)* func=0x50661220)  Line 944 + 0x11 bytes
 GeolocationDispatcher::OnMessageReceived(const IPC::Message & message=class=16, index=167)  Line 31 + 0x12 bytes
 RenderView::OnMessageReceived(const IPC::Message & message=class=16, index=167)  Line 673 + 0x2b bytes
 MessageRouter::RouteMessage(const IPC::Message & msg=class=16, index=167)  Line 40 + 0x13 bytes
 MessageRouter::OnMessageReceived(const IPC::Message & msg=class=16, index=167)  Line 31 + 0x13 bytes
 ChildThread::OnMessageReceived(const IPC::Message & msg=class=16, index=167)  Line 163 + 0x17 bytes
 IPC::ChannelProxy::Context::OnDispatchMessage(const IPC::Message & message=class=16, index=167)  Line 206 + 0x19 bytes
 DispatchToMethod<IPC::ChannelProxy::Context,void (__thiscall IPC::ChannelProxy::Context::*)(IPC::Message const &),IPC::Message>(IPC::ChannelProxy::Context * obj=0x05028180, void (const IPC::Message &)* method=0x502a6530, const Tuple1<IPC::Message> & arg={...})  Line 547 + 0xf bytes
 RunnableMethod<IPC::ChannelProxy::Context,void (__thiscall IPC::ChannelProxy::Context::*)(IPC::Message const &),Tuple1<IPC::Message> >::Run()  Line 327 + 0x1e bytes
 MessageLoop::RunTask(Task * task=0x07fe3a80)  Line 408 + 0xf bytes
 MessageLoop::DeferOrRunPendingTask(const MessageLoop::PendingTask & pending_task={...})  Line 420
 MessageLoop::DoWork()  Line 524 + 0xc bytes
 base::MessagePumpForUI::DoRunLoop()  Line 202 + 0x1d bytes
 base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate=0x0550f688, base::MessagePumpWin::Dispatcher * dispatcher=0x00000000)  Line 51 + 0xf bytes
 base::MessagePumpWin::Run(base::MessagePump::Delegate * delegate=0x0550f688)  Line 80 + 0x1c bytes
 MessageLoop::RunInternal()  Line 256 + 0x2a bytes
 MessageLoop::RunHandler()  Line 229
 MessageLoop::Run()  Line 207
 base::Thread::Run(MessageLoop * message_loop=0x0550f688)  Line 141
 base::Thread::ThreadMain()  Line 164 + 0x16 bytes
 `anonymous namespace'::ThreadFunc(void * closure=0x028cba80)  Line 26 + 0xf bytes
 	kernel32.dll!@BaseThreadInitThunk@12()  + 0xe bytes	
 	ntdll.dll!___RtlUserThreadStart@8()  + 0x23 bytes	
 	ntdll.dll!__RtlUserThreadStart@8()  + 0x1b bytes	


### in...@chromium.org (2010-08-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-08-26)

basically the fix of https://crbug.com/chromium/51670 didn't fix the real issue and kuzzcc came up with same bug but in  a different location

i looked at it and understand the issue, so want to discuss how to best fix it::

basically, the bridge map are stored on chromium side

void GeolocationDispatcher::OnGeolocationPermissionSet(int bridge_id,
bool allowed) {
WebKit::WebGeolocationServiceBridge* bridge = bridges_map_.Lookup(bridge_id);
if (bridge) {
bridge->setIsAllowed(allowed);
}
}

when Geolocation::disconnectFrame() is called, then it tries to clear these bridges in stopUpdating() call.
void WebGeolocationServiceBridgeImpl::stopUpdating()
{
    WebViewClient* webViewClient = getWebViewClient();
    if (m_bridgeId && webViewClient) {
        WebGeolocationService* geolocationService = webViewClient->geolocationService();
        geolocationService->stopUpdating(m_bridgeId);
        geolocationService->detachBridge(m_bridgeId);
    }
    m_bridgeId = 0;
}

but since page is gone (i think location.reload causes it to become zero), 
getWebViewClient returns zero

WebViewClient* WebGeolocationServiceBridgeImpl::getWebViewClient()
{
Frame* frame = m_GeolocationServiceChromium->frame();
if (!frame || !frame->page())
return 0;
WebKit::ChromeClientImpl* chromeClientImpl = static_cast<WebKit::ChromeClientImpl*>(frame->page()->chrome()->client());
WebKit::WebViewClient* webViewClient = chromeClientImpl->webView()->client();
return webViewClient;
}

so then none of the bridge are removed in 
geolocationService->detachBridge(m_bridgeId);.

we have frame at the point of disconnectframe, but we dont have a page. so stopupdating does nothing. 

When we later get to this call, we are working on a stale bridge from the bridge map which causes crashes either in bridge pointer or m_Service stale pointer.

It is not good to store bridge map outside of webcore since they dont get hooked to the proper page/frame/document destructor and hence stale pointers are left in map.

@joth, @bulach - can you please chat with me at aarya@google and discuss more on this.




### in...@chromium.org (2010-08-27)

@joth: the fix needs to be in chrome side code and probably needs to be moved to webcore. can you please take a look. since this is secseverity-high, we want to target v6 first patch.

### jo...@chromium.org (2010-08-31)

I started investigating and now understand inferno's comments. The attached patch appears to make the symptoms go away in a very simplistic manner. I now need to go away and learn what is wrong with this patch.

### er...@chromium.org (2010-08-31)

BTW this is the top renderer crash in 7.0.503.0 as well.

(Crashes in GeolocationDispatcher::OnMessageReceived).

Sample reports:

http://crash/reportdetail?reportid=010889b77315d97b
http://crash/reportdetail?reportid=019d0c7534b5811d
http://crash/reportdetail?reportid=019d0c7534b58feb
http://crash/reportdetail?reportid=01b1bc76410f97dc
http://crash/reportdetail?reportid=01b1bc76410f9a8b
http://crash/reportdetail?reportid=01fe14ae6c3fa801
http://crash/reportdetail?reportid=02cf92f20a9857ff


### bu...@gmail.com (2010-09-07)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=58687 

------------------------------------------------------------------------
r58687 | joth@chromium.org | 2010-09-07 03:42:41 -0700 (Tue, 07 Sep 2010) | 10 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/geolocation_dispatcher.cc?r1=58687&r2=58686
   M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/tools/test_shell/test_geolocation_service.cc?r1=58687&r2=58686

Make calls to onWebGeolocationServiceDestroyed
Needed by patch https://bugs.webkit.org/show_bug.cgi?id=45112

NOTE Depends on webkit r66837: (http://trac.webkit.org/changeset/66837)
 (will land once that is rolled in)

BUG=53394
TEST=fast/dom/Geolocation/*

Review URL: http://codereview.chromium.org/3338008
------------------------------------------------------------------------


### js...@chromium.org (2010-09-07)

Need to look at the complexity of this one to see if we should target m6. Flagging as WillMerge for the moment.

### jo...@chromium.org (2010-09-07)

To summarize, merge will involve applying three patches to the branch:

WebKit
http://trac.webkit.org/changeset/66837
http://trac.webkit.org/changeset/66886
Chrome:
http://src.chromium.org/viewvc/chrome?view=rev&revision=58687


### in...@chromium.org (2010-09-08)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-09-08)

------------------------------------------------------------------------
r58834 | inferno@chromium.org | Wed Sep 08 09:23:47 PDT 2010
Changed paths:
 M /branches/WebKit/472/WebKit/chromium/public/WebGeolocationServiceBridge.h
 M /branches/WebKit/472/WebKit/chromium/src/WebGeolocationServiceBridgeImpl.cpp
Merge 66837 - 2010-09-06  Jonathan Dixon  <joth@chromium.org>

        Reviewed by Jeremy Orlow.

        Add new interface and empty impl. as precursor to https://crbug.com/chromium/45112
        https://bugs.webkit.org/show_bug.cgi?id=45257

        * public/WebGeolocationServiceBridge.h:
        (WebKit::WebGeolocationServiceBridge::~WebGeolocationServiceBridge):
        * src/WebGeolocationServiceBridgeImpl.cpp:
        (WebKit::WebGeolocationServiceBridgeImpl::onWebGeolocationServiceDestroyed):

BUG=53394

Review URL: http://codereview.chromium.org/3340018
------------------------------------------------------------------------

### sc...@gmail.com (2010-09-09)

Bugdroid died...

Also 

http://src.chromium.org/viewvc/chrome?view=rev&revision=58835
for
http://trac.webkit.org/changeset/66886

and
http://src.chromium.org/viewvc/chrome?view=rev&revision=58836
for
http://src.chromium.org/viewvc/chrome?view=rev&revision=58687


### jo...@chromium.org (2010-09-09)

Branch 517 was cut just hours before this fix landed, so we'll need to merge these into there for M7 too.
Let me know if you'd like me to handle that

### in...@chromium.org (2010-09-09)

Yes Jonathan, please go ahead and merge these to 517. Marking WIllMerge till then.

### in...@chromium.org (2010-09-09)

Merged to 517.

### bu...@gmail.com (2010-09-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=58961

------------------------------------------------------------------------
r58961 | inferno@chromium.org | Thu Sep 09 10:54:56 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/517/src/chrome/renderer/geolocation_dispatcher.cc?r1=58961&r2=58960&pathrev=58961
 M http://src.chromium.org/viewvc/chrome/branches/517/src/webkit/tools/test_shell/test_geolocation_service.cc?r1=58961&r2=58960&pathrev=58961

Merge 58687 - Make calls to onWebGeolocationServiceDestroyed
Needed by patch https://bugs.webkit.org/show_bug.cgi?id=45112

NOTE Depends on webkit r66837: (http://trac.webkit.org/changeset/66837)
 (will land once that is rolled in)

BUG=53394
TEST=fast/dom/Geolocation/*

Review URL: http://codereview.chromium.org/3338008

TBR=joth@chromium.org
Review URL: http://codereview.chromium.org/3294019
------------------------------------------------------------------------

### sc...@gmail.com (2010-09-09)

@kuzzcc: thanks for noticing that the fix for the previous Geolocation bug was not complete. This was a very useful catch for us. Therefore: congratulations! You have provisionally qualified for an additional $500 Chromium Security Reward :)

### jo...@chromium.org (2010-09-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2010-09-13)

Fix merged into branch 517 for M7 :-

http://trac.webkit.org/changeset/67097/branches/chromium/517/WebCore/platform
http://src.chromium.org/viewvc/chrome?view=rev&revision=58961
http://trac.webkit.org/changeset/67097/branches/chromium/517/WebKit

### jo...@chromium.org (2010-09-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-09-22)

Payment is in the electronic system.

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

### be...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>Geolocation]

### be...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Location]

### is...@google.com (2017-09-22)

This issue was migrated from crbug.com/chromium/53394?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Geolocation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082890)*
