# RenderViewHostImpl::OnMessageReceived

| Field | Value |
|-------|-------|
| **Issue ID** | [40076979](https://issues.chromium.org/issues/40076979) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, UI>Browser>Navigation |
| **Reporter** | ch...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2013-02-14 |
| **Bounty** | $1,000.00 |

## Description

Google Chrome	24.0.1312.57 (Official Build 178923) m
OS	Windows XP & 7

1. Open 
data:text/html,<button onclick="test()">clickme</button><script>delay_url = 'http://www.google.co.ma/';function test(){w = open();w.opener = null;setTimeout(function(){w.document.write(1);w.location = delay_url;setTimeout(function(){w.location.reload();}, 0);}, 0)}</script>

2. click on button and you can see there is new page on this there is same button but after two seconds it's loading google.com website so click faster on the button before loading of google then also you can get same thing in next step, you should do that three times at least and after you can see on the browser our url(data:text/html,...) and pages of google after loading.

3. Close each page of google.

the problem is our url is open google.com but not directly after reload of our page (data:text/html,...) with location.reload() method so when we click on button before loading of google.com and we get also another page and we close theme the browser is crashed.


 # ChildEBP RetAddr  
00 0012f928 02175e73 chrome_1c30000!content::RenderViewHostImpl::OnMessageReceived+0xc5 [c:\b\build\slave\win\build\src\content\browser\renderer_host\render_view_host_impl.cc @ 959]
01 0012fadc 01c61204 chrome_1c30000!content::RenderProcessHostImpl::ProcessDied+0x111 [c:\b\build\slave\win\build\src\content\browser\renderer_host\render_process_host_impl.cc @ 1430]
02 0012fb38 01c60f26 chrome_1c30000!MessageLoop::RunTask+0x1eb [c:\b\build\slave\win\build\src\base\message_loop.cc @ 472]
03 0012fc88 01e56084 chrome_1c30000!MessageLoop::DoWork+0x2ec [c:\b\build\slave\win\build\src\base\message_loop.cc @ 666]
04 0012fcb8 01c60ab4 chrome_1c30000!base::MessagePumpForUI::DoRunLoop+0x5b [c:\b\build\slave\win\build\src\base\message_pump_win.cc @ 241]
05 0012fcd8 01c609a8 chrome_1c30000!MessageLoop::RunInternal+0x5f [c:\b\build\slave\win\build\src\base\message_loop.cc @ 422]
06 0012fce8 02106774 chrome_1c30000!base::RunLoop::Run+0x59 [c:\b\build\slave\win\build\src\base\run_loop.cc @ 46]
07 0012fd4c 021066ad chrome_1c30000!ChromeBrowserMainParts::MainMessageLoopRun+0xaa [c:\b\build\slave\win\build\src\chrome\browser\chrome_browser_main.cc @ 1547]
08 0012fd60 02106677 chrome_1c30000!content::BrowserMainLoop::RunMainMessageLoopParts+0x2d [c:\b\build\slave\win\build\src\content\browser\browser_main_loop.cc @ 483]
09 0012fd70 01cabf43 chrome_1c30000!content::BrowserMainRunnerImpl::Run+0x13 [c:\b\build\slave\win\build\src\content\browser\browser_main_runner.cc @ 129]
0a 0012fd84 01c48af7 chrome_1c30000!content::BrowserMain+0x3c [c:\b\build\slave\win\build\src\content\browser\browser_main.cc @ 22]
0b 0012fd98 01c48a7e chrome_1c30000!content::RunNamedProcessTypeMain+0x58 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 448]
0c 0012fe04 01c3a8fb chrome_1c30000!content::ContentMainRunnerImpl::Run+0x85 [c:\b\build\slave\win\build\src\content\app\content_main_runner.cc @ 741]
0d 0012fe14 01c3a5ed chrome_1c30000!content::ContentMain+0x29 [c:\b\build\slave\win\build\src\content\app\content_main.cc @ 35]
0e 0012fe4c 00423f9b chrome_1c30000!ChromeMain+0x1e [c:\b\build\slave\win\build\src\chrome\app\chrome_main.cc @ 28]
0f 0012fec4 00426ad4 chrome!MainDllLoader::Launch+0xe9 [c:\b\build\slave\win\build\src\chrome\app\client_util.cc @ 441]
10 0012fee8 00426b3f chrome!RunChrome+0x4d [c:\b\build\slave\win\build\src\chrome\app\chrome_exe_main_win.cc @ 32]
11 0012ff30 0047f62d chrome!wWinMain+0x50 [c:\b\build\slave\win\build\src\chrome\app\chrome_exe_main_win.cc @ 47]
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\WINDOWS\system32\kernel32.dll - 
12 0012ffc0 7c817067 chrome!__tmainCRTStartup+0x11a [f:\dd\vctools\crt_bld\self_x86\crt\src\crt0.c @ 275]
WARNING: Stack unwind information not available. Following frames may be wrong.
13 0012fff0 00000000 kernel32!RegisterWaitForInputIdle+0x49



## Attachments

- [exe.png](attachments/exe.png) (image/png; charset=binary, 28.2 KB)

## Timeline

### jl...@chromium.org (2013-02-15)

Looks legitimate. Reproduced on Windows and Linux.

Still trying to figure it out. Here are a couple of crash IDs:

Crash ID bbeee2fbf72e79b0
Crash ID 506f79ef3837eb2b
Crash ID 47ceadced188c520

### jl...@chromium.org (2013-02-15)

On a debug build this can fail an assert in a renderer:

ASSERTION FAILED: m_currentItem
../../third_party/WebKit/Source/WebCore/loader/HistoryController.cpp(123) : void WebCore::HistoryController::restoreScrollPositionAndViewState()

Received signal 11 SEGV_MAPERR 0000bbadbeef
 [0x7f2dedc12f4e] base::debug::StackTrace::StackTrace()
 [0x7f2dedc12a85] base::debug::(anonymous namespace)::StackDumpSignalHandler()
 [0x7f2de6c1acb0] <unknown>
 [0x7f2def0c8cee] WebCore::HistoryController::restoreScrollPositionAndViewState()
 [0x7f2def0ba139] WebCore::FrameLoader::checkLoadCompleteForThisFrame()
 [0x7f2def0b2d9d] WebCore::FrameLoader::checkLoadComplete()
 [0x7f2def08d443] WebCore::DocumentLoader::finishedLoading()
 [0x7f2def0d2dd0] WebCore::MainResourceLoader::didFinishLoading()
 [0x7f2def0d3c06] WebCore::MainResourceLoader::notifyFinished()
 [0x7f2def10b73d] WebCore::CachedResource::checkNotify()
 [0x7f2def10b7a5] WebCore::CachedResource::data()
 [0x7f2def10774b] WebCore::CachedRawResource::data()
 [0x7f2def0e91fa] WebCore::SubresourceLoader::didFinishLoading()
 [0x7f2def0e38f5] WebCore::ResourceLoader::didFinishLoading()
 [0x7f2df0c98da4] WebCore::ResourceHandleInternal::didFinishLoading()
 [0x7f2df16b1e64] webkit_glue::WebURLLoaderImpl::Context::OnCompletedRequest()
 [0x7f2df16affd2] webkit_glue::WebURLLoaderImpl::Context::HandleDataURL()
 [0x7f2df16b3332] base::internal::RunnableAdapter<>::Run()
 [0x7f2df16b32a9] base::internal::InvokeHelper<>::MakeItSo()
 [0x7f2df16b3265] base::internal::Invoker<>::Run()
 [0x7f2dec75181e] base::Callback<>::Run()
 [0x7f2dedc4958e] MessageLoop::RunTask()
 [0x7f2dedc4992b] MessageLoop::DeferOrRunPendingTask()
 [0x7f2dedc49ad5] MessageLoop::DoWork()
 [0x7f2dedc530c8] base::MessagePumpDefault::Run()
 [0x7f2dedc49006] MessageLoop::RunInternal()
 [0x7f2dedc48eb5] MessageLoop::RunHandler()
 [0x7f2dedc79c62] base::RunLoop::Run()
 [0x7f2dedc48751] MessageLoop::Run()
 [0x7f2df0301872] content::RendererMain()
 [0x7f2df02886ca] content::RunZygote()
 [0x7f2df02889d4] content::RunNamedProcessTypeMain()
 [0x7f2df028991d] content::ContentMainRunnerImpl::Run()
 [0x7f2df0287e14] content::ContentMain()
 [0x7f2dec6b41be] ChromeMain
 [0x7f2dec6b4172] main

### jl...@chromium.org (2013-02-15)

[Empty comment from Monorail migration]

### le...@chromium.org (2013-02-15)

Also from another machine at 05b38f8ac93c9c6c and 2032d6ad8ecc7981

### le...@chromium.org (2013-02-15)

I can't manage to repro the Browser crash in 25.0.1364.68 beta


### jl...@chromium.org (2013-02-15)

I can reproduce on Windows as well, but I can't get a crash report. On Linux here's the crash dump for the browser process:

Thread 0 *CRASHED* ( SIGSEGV @ 0x6014ffaa8024 )

0x7fc3fd308e90	 [chrome]	 - content/browser/renderer_host/render_view_host_impl.cc:959]	content::RenderViewHostImpl::OnMessageReceived(IPC::Message const&)
0x7fc3fd2f9d86	 [chrome]	 - content/browser/renderer_host/render_process_host_impl.cc:1430]	content::RenderProcessHostImpl::ProcessDied()
0x7fc3fb89bca3	 [chrome]	 - ./base/callback.h:391]	MessageLoop::RunTask(base::PendingTask const&)
0x7fc3fb89c5da	 [chrome]	 - base/message_loop.cc:482]	MessageLoop::DeferOrRunPendingTask(base::PendingTask const&)
0x7fc3fb89cbe7	 [chrome]	 - base/message_loop.cc:665]	MessageLoop::DoWork()
0x7fc3fb8d5e94	 [chrome]	 - base/message_pump_glib.cc:203]	base::MessagePumpGlib::RunWithDispatcher(base::MessagePump::Delegate*, base::MessagePumpDispatcher*)
0x7fc3fb8ada61	 [chrome]	 - base/run_loop.cc:45]	base::RunLoop::Run()
0x7fc3fb5caedb	 [chrome]	 - chrome/browser/chrome_browser_main.cc:1545]	ChromeBrowserMainParts::MainMessageLoopRun(int*)
0x7fc3fd279950	 [chrome]	 - content/browser/browser_main_loop.cc:481]	content::BrowserMainLoop::RunMainMessageLoopParts()
0x7fc3fd27b44c	 [chrome]	 - content/browser/browser_main_runner.cc:128]	content::BrowserMainRunnerImpl::Run()
0x7fc3fd279628	 [chrome]	 - content/browser/browser_main.cc:22]	content::BrowserMain(content::MainFunctionParams const&)
0x7fc3fb8222c2	 [chrome]	 - content/app/content_main_runner.cc:741]	content::ContentMainRunnerImpl::Run()
0x7fc3fb820a10	 [chrome]	 - content/app/content_main.cc:35]	content::ContentMain(int, char const**, content::ContentMainDelegate*)
0x7fc3fb2fcf1c	 [chrome]	 - chrome/app/chrome_main.cc:32]	ChromeMain
0x7fc3fb2fced5	 [chrome]	 - chrome/app/chrome_exe_main_gtk.cc:31]	main

### jl...@chromium.org (2013-02-15)

Adding a few security minded people who have touched around that area, in case they want to help.

### jl...@chromium.org (2013-02-15)

The Webkit assert appears to be a red herring in this case. And I can't reproduce the browser crash on tip of tree.

### jl...@chromium.org (2013-02-15)

Finally managed to build a version that crashes locally. It crashes at:

content/browser/renderer_host/render_view_host_impl.cc:959, which is in RenderViewHostImpl::OnMessageReceived():

  if (delegate_->OnMessageReceived(this, msg))
    return true;

Looks like the delegate may be destroyed before we hit this.

I wonder if it could be similar to crbug.com/82827

John, do you want to take a look ?

Symbolized ASAN dump:

=================================================================
==19167== ERROR: AddressSanitizer heap-use-after-free on address 0x7f3376a22890 at pc 0x7f338e084ef1 bp 0x7fffd12a5270 sp 0x7fffd12a5268
READ of size 8 at 0x7f3376a22890 thread T0
    #0 0x7f338e084ef0 in _ZN7content18RenderViewHostImpl17OnMessageReceivedERKN3IPC7MessageE /home/julien/sources/chrome/src/out/Release/../../content/browser/renderer_host/render_view_host_impl.cc:959
    #1 0x7f338e08d22c in _ZThn8_N7content18RenderViewHostImpl17OnMessageReceivedERKN3IPC7MessageE ???:0
    #2 0x7f338e05f963 in _ZN7content21RenderProcessHostImpl11ProcessDiedEv /home/julien/sources/chrome/src/out/Release/../../content/browser/renderer_host/render_process_host_impl.cc:1461
    #3 0x7f338fe9dfe7 in _ZNK4base8CallbackIFvvEE3RunEv /home/julien/sources/chrome/src/out/Release/../../base/callback.h:391
    #4 0x7f338fe9e5c1 in _ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/julien/sources/chrome/src/out/Release/../../base/message_loop.cc:482
    #5 0x7f338fe9f37d in _ZN11MessageLoop6DoWorkEv /home/julien/sources/chrome/src/out/Release/../../base/message_loop.cc:665
    #6 0x7f338ff6c478 in _ZN4base15MessagePumpGlib14HandleDispatchEv /home/julien/sources/chrome/src/out/Release/../../base/message_pump_glib.cc:268
    #7 0x7f3389200d52 in g_main_dispatch /build/buildd/glib2.0-2.32.3/./glib/gmain.c:2539
0x7f3376a22890 is located 80 bytes inside of 1136-byte region [0x7f3376a22840,0x7f3376a22cb0)
freed by thread T0 here:
    #0 0x7f3394993e50 in _ZdlPv ??:0
    #1 0x7f338e5bc4a9 in ~scoped_ptr /home/julien/sources/chrome/src/out/Release/../../base/memory/scoped_ptr.h:163
    #2 0x7f338e5d0294 in _ZN13TabStripModel16InternalCloseTabEP11TabContentsib /home/julien/sources/chrome/src/out/Release/../../chrome/browser/ui/tabs/tab_strip_model.cc:1179
    #3 0x7f338e5c80ba in _ZN13TabStripModel17InternalCloseTabsERKSt6vectorIiSaIiEEj /home/julien/sources/chrome/src/out/Release/../../chrome/browser/ui/tabs/tab_strip_model.cc:1159
    #4 0x7f338e5c849e in _ZN13TabStripModel18CloseTabContentsAtEij /home/julien/sources/chrome/src/out/Release/../../chrome/browser/ui/tabs/tab_strip_model.cc:396
    #5 0x7f338e51211f in _ZN11TabStripGtk8CloseTabEP6TabGtk /home/julien/sources/chrome/src/out/Release/../../chrome/browser/ui/gtk/tabs/tab_strip_gtk.cc:1232
    #6 0x7f338e86d893 in _ZN6TabGtk20OnButtonReleaseEventEP10_GtkWidgetP15_GdkEventButton /home/julien/sources/chrome/src/out/Release/../../chrome/browser/ui/gtk/tabs/tab_gtk.cc:181
    #7 0x7f338e86c5a7 in _ZN6TabGtk25OnButtonReleaseEventThunkEP10_GtkWidgetP15_GdkEventButtonPv /home/julien/sources/chrome/src/out/Release/../../chrome/browser/ui/gtk/tabs/tab_gtk.h:138
    #8 0x7f3388cb5dd7 in _gtk_marshal_BOOLEAN__BOXED /build/buildd/gtk+2.0-2.24.10/gtk/gtkmarshalers.c:86
previously allocated by thread T0 here:
    #0 0x7f3394993cd0 in _Znwm ??:0
    #1 0x7f338e179e2a in _ZN7content15WebContentsImpl15CreateNewWindowEiRK31ViewHostMsg_CreateWindow_ParamsPNS_23SessionStorageNamespaceE /home/julien/sources/chrome/src/out/Release/../../content/browser/web_contents/web_contents_impl.cc:1283
    #2 0x7f338fe9dfe7 in _ZNK4base8CallbackIFvvEE3RunEv /home/julien/sources/chrome/src/out/Release/../../base/callback.h:391
    #3 0x7f338fe9e5c1 in _ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/julien/sources/chrome/src/out/Release/../../base/message_loop.cc:482
    #4 0x7f338fe9f37d in _ZN11MessageLoop6DoWorkEv /home/julien/sources/chrome/src/out/Release/../../base/message_loop.cc:665
    #5 0x7f338ff6c478 in _ZN4base15MessagePumpGlib14HandleDispatchEv /home/julien/sources/chrome/src/out/Release/../../base/message_pump_glib.cc:268
    #6 0x7f3389200d52 in g_main_dispatch /build/buildd/glib2.0-2.32.3/./glib/gmain.c:2539
Shadow byte and word:
  0x1fe66ed44512: fd
  0x1fe66ed44510: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1fe66ed444f0: fa fa fa fa fa fa fa fa
  0x1fe66ed444f8: fa fa fa fa fa fa fa fa
  0x1fe66ed44500: fa fa fa fa fa fa fa fa
  0x1fe66ed44508: fd fd fd fd fd fd fd fd
=>0x1fe66ed44510: fd fd fd fd fd fd fd fd
  0x1fe66ed44518: fd fd fd fd fd fd fd fd
  0x1fe66ed44520: fd fd fd fd fd fd fd fd
  0x1fe66ed44528: fd fd fd fd fd fd fd fd
  0x1fe66ed44530: fd fd fd fd fd fd fd fd
Stats: 154M malloced (156M for red zones) by 912502 calls
Stats: 14M realloced by 59780 calls
Stats: 140M freed by 816764 calls
Stats: 105M really freed by 547399 calls
Stats: 171M (43900 full pages) mmaped in 324 calls
  mmaps   by size class: 7:335790; 8:45034; 9:11253; 10:38325; 11:2550; 12:2176; 13:768; 14:704; 15:160; 16:176; 17:64; 18:30; 19:4; 20:4; 22:2;
  mallocs by size class: 7:733931; 8:88719; 9:20714; 10:56245; 11:4529; 12:4457; 13:1456; 14:1669; 15:274; 16:328; 17:115; 18:54; 19:5; 20:4; 22:2;
  frees   by size class: 7:655964; 8:76802; 9:18904; 10:55195; 11:3090; 12:3382; 13:1166; 14:1586; 15:219; 16:291; 17:105; 18:50; 19:5; 20:3; 22:2;
  rfrees  by size class: 7:428013; 8:50836; 9:12114; 10:49280; 11:2288; 12:2470; 13:827; 14:1061; 15:154; 16:232; 17:78; 18:36; 19:5; 20:3; 22:2;
Stats: malloc large: 783 small slow: 7770
==19167== ABORTING

### jl...@chromium.org (2013-02-15)

[Comment Deleted]

### ch...@gmail.com (2013-02-15)

i was wondering is that use-after-free vulnerability 

### cr...@chromium.org (2013-02-16)

RenderProcessHostImpl::ProcessDied is just looping through render_widget_hosts_ and calling OnMessageReceived on them.  It looks like a RenderViewHost might have been left in that list despite being deleted.

@jln: If you have a build that repros, perhaps you could verify when the RVH in question gets deleted?

(Sounds like this might not be an issue in M25?  Probably good to understand what the bug was to verify it's fixed, at least.)

### na...@chromium.org (2013-02-16)

I've done some work to find out when the bug showed up and when it was fixed. I've got straight crash introduced in the range of 136162:136190. In the range of 134975:134990 there is no immediate crash, but there is one when the full browser is closed.

The bug is fixed somewhere in the range 171316:171783.

### na...@chromium.org (2013-02-16)

The most likely revision that fixes this issue is http://crrev.com/171384. The test case opens a new window, disowns it (w.opener = null;) and then navigates it cross-site. It is likely that http://crrev.com/134981 introduced the condition, but hasn't surfaced in any test cases. I haven't debugged to verify, just going on by changes to Chrome and the test case provided.

### ts...@chromium.org (2013-02-19)

@nasko - if you're sure of your results, and this is fixed, then this can be closed out.

### cr...@chromium.org (2013-02-19)

Sounds like it's almost certainly resolved by http://crrev.com/171384, and that's in the 25 branch, so this wouldn't repro on Chrome 25.  Before we close this, I'd like to take a closer look to verify what the bug was and that it's actually fixed, and that we haven't just papered over it in a way that leaves the crash possible.  I'll try to verify later today.

### jl...@chromium.org (2013-02-19)

Thanks Chris. As I was telling Nasko last week on IRC, I'm pretty worried about the same thing.

As the very least we may want to NULL out this pointer at delete time or make use of a smart pointers (didn't look enough to know which one).

### ts...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### ts...@chromium.org (2013-02-19)

[Empty comment from Monorail migration]

### cr...@chromium.org (2013-02-20)

And, as it turns out, the underlying bug is still there.  :)  The CL in http://crrev.com/171384 is indeed just papering over these repro steps by changing the behavior for w.opener = null.  However, the bug still exists if you use a different technique to cause a process swap, such as navigating to a hosted app.  (For example, Google Drive is installed as a default hosted app, so you can use https://drive.google.com.)

As a result, I'm able to repro on Chrome 27.0.1417.2 (crash report 6a18452c68f2dfe6), using the URL below:

data:text/html,<button onclick="test()">clickme</button><script>delay_url = 'https://drive.google.com/';function test(){w = open();setTimeout(function(){w.document.write(1);w.location = delay_url;setTimeout(function(){w.location.reload();}, 0);}, 0)}</script>

The actual bug is that we're creating two RenderViewHosts in the Google process for one of the tabs, and we're only cleaning up one of them.  That means it sticks around in the RenderProcessHost's render_widget_hosts_ list, and we try to call a method on it after the tab (i.e., its delegate_) has been deleted.

I'm investigating to find out why the extra RVH is getting created.

### jl...@chromium.org (2013-02-20)

Awesome job, thanks Charlie!

I still don't have a good enough understanding to have a good sense of how exploitable this could be from a compromised renderer to escape to the browser.
But I would tend to think that an exploit is not a stretch, even though the level of control of the browser's address space is pretty low.

### ch...@gmail.com (2013-02-20)

[Comment Deleted]

### ch...@gmail.com (2013-02-20)

Thank you Charlie for explanation 

### cr...@chromium.org (2013-02-20)

Found it.  When we're doing a cross-process navigation, we make sure we have any necessary swapped out RVHs for the opener(s) of the tab, which allows us to do things like window.opener.postMessage.

Obviously, if there's an existing swapped out RVH, we should use it, and only create a new one if necessary.  However, in this case there was a pending RVH that we weren't checking.  If we check for it, we don't create the extra RVH described in https://crbug.com/chromium/176252#c21.

I have a simple CL that fixes the issue, and I'm putting together a test.

### bu...@chromium.org (2013-02-21)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=183730

------------------------------------------------------------------------
r183730 | creis@chromium.org | 2013-02-21T03:25:00.968744Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/web_contents/web_contents_impl_unittest.cc?r1=183730&r2=183729&pathrev=183730
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/web_contents/web_contents_impl.cc?r1=183730&r2=183729&pathrev=183730
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/web_contents/web_contents_impl.h?r1=183730&r2=183729&pathrev=183730

Avoid creating an extra RVH for a tab's opener when one is pending.

This prevents a crash when later deleting the tab.

BUG=176252
TEST=See bug for repro steps.


Review URL: https://chromiumcodereview.appspot.com/12319035
------------------------------------------------------------------------

### cr...@chromium.org (2013-02-21)

The fix for this bug has landed in http://crrev.com/183730.  It didn't quite make it into today's Canary (27.0.1419.0), but it should be in the next one.  Once we verify it, we should merge the fix, probably to both M26 and M25.

### cr...@chromium.org (2013-02-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-21)

I'll do it. Keep an extra careful eye out for problems?

### cr...@chromium.org (2013-02-25)

FYI, I was able to verify the fix for this in Mac Chrome 27.0.1422.0 and I don't see related crashes, so I think it should be good to merge.

### ch...@gmail.com (2013-02-26)

@scarybeasts: is this report qualified for a chromium security reward ?

### sc...@gmail.com (2013-02-26)

@chromium.khalil: thanks for asking!
As you can see, the bug is tagged "reward-topanel" which means we'll cover the case in out rewards nomination process soon! And we'll let you know on this bug.

### sc...@gmail.com (2013-02-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-02-26)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=184722

------------------------------------------------------------------------
r184722 | cevans@chromium.org | 2013-02-26T20:35:13.785530Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1364/src/content/browser/web_contents/web_contents_impl.h?r1=184722&r2=184721&pathrev=184722
   M http://src.chromium.org/viewvc/chrome/branches/1364/src/content/browser/web_contents/web_contents_impl_unittest.cc?r1=184722&r2=184721&pathrev=184722
   M http://src.chromium.org/viewvc/chrome/branches/1364/src/content/browser/web_contents/web_contents_impl.cc?r1=184722&r2=184721&pathrev=184722

Merge 183730
> Avoid creating an extra RVH for a tab's opener when one is pending.
> 
> This prevents a crash when later deleting the tab.
> 
> BUG=176252
> TEST=See bug for repro steps.
> 
> 
> Review URL: https://chromiumcodereview.appspot.com/12319035

TBR=creis@chromium.org
Review URL: https://codereview.chromium.org/12330151
------------------------------------------------------------------------

### bu...@chromium.org (2013-02-26)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=184723

------------------------------------------------------------------------
r184723 | cevans@chromium.org | 2013-02-26T20:38:18.857854Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/content/browser/web_contents/web_contents_impl_unittest.cc?r1=184723&r2=184722&pathrev=184723
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/content/browser/web_contents/web_contents_impl.cc?r1=184723&r2=184722&pathrev=184723
   M http://src.chromium.org/viewvc/chrome/branches/1410/src/content/browser/web_contents/web_contents_impl.h?r1=184723&r2=184722&pathrev=184723

Merge 183730
> Avoid creating an extra RVH for a tab's opener when one is pending.
> 
> This prevents a crash when later deleting the tab.
> 
> BUG=176252
> TEST=See bug for repro steps.
> 
> 
> Review URL: https://chromiumcodereview.appspot.com/12319035

TBR=creis@chromium.org
Review URL: https://codereview.chromium.org/12321144
------------------------------------------------------------------------

### sc...@gmail.com (2013-03-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-02)

@chromium.khalil: thanks for the report! As it happens, this does qualify for a provisional $1000 Chromium Security Reward! :D

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

### ch...@gmail.com (2013-03-02)

@scarybeasts: Thank you so much :)

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/176252?no_tracker_redirect=1

[Multiple monorail components: Internals, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076979)*
