# Chrome_Mac: Crash Report -         Stack Signature: CompositorOutputSurface::OnMessageReceived-...

| Field | Value |
|-------|-------|
| **Issue ID** | [40076359](https://issues.chromium.org/issues/40076359) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | dh...@google.com |
| **Assignee** | nd...@chromium.org |
| **Created** | 2012-09-26 |
| **Bounty** | $500.00 |

## Description

Product: Chrome_Mac
Stack Signature: CompositorOutputSurface::OnMessageReceived-2B4E1D3
New Signature Label: CompositorOutputSurface::OnMessageReceived
New Signature Hash: 3da6e7dd_72586abe_4b6e4984_a08d6dce_bb253a37

Report link: http://go/crash/reportdetail?reportid=b1d9b0d95bc386c7

Meta information:
Product Name: Chrome_Mac
Product Version: 24.0.1277.0
Report ID: b1d9b0d95bc386c7
Report Time: 2012/09/26 17:13:20, Wed
Uptime: 65995 sec
Cumulative Uptime: 0 sec
OS Name: Mac OS X
OS Version: 10.8.2 12C54
CPU Architecture: x86
CPU Info: GenuineIntel family 6 model 58 stepping 9
ptype: renderer

Thread 0 *CRASHED* ( EXC_BAD_ACCESS / KERN_INVALID_ADDRESS @ 0xffffffff83e58955 )

0x003de515	 [Google Chrome Framework]	 - compositor_output_surface.cc:111]	CompositorOutputSurface::OnMessageReceived
0x003de5e8	 [Google Chrome Framework]	 - ../base/bind_internal.h:190 (cs|src|ann)]	base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (CompositorOutputSurface::*)(const IPC::Message &)>, void (CompositorOutputSurface *, const IPC::Message &), void (base::internal::UnretainedWrapper<CompositorOutputSurface>)>, void (CompositorOutputSurface *, const IPC::Message &)>::Run
0x00df7018	 [Google Chrome Framework]	 - ../base/callback.h:429 (cs|src|ann)]	base::internal::Invoker<1, base::internal::BindState<base::Callback<void (const IPC::Message &)>, void (const IPC::Message &), void (IPC::Message)>, void (const IPC::Message &)>::Run
0x00af7942	 [Google Chrome Framework]	 - ../base/callback.h:389 (cs|src|ann)]	MessageLoop::RunTask
0x00af7d7c	 [Google Chrome Framework]	 - message_loop.cc:482]	MessageLoop::DoWork
0x00acb314	 [Google Chrome Framework]	 - message_pump_mac.mm:250]	base::MessagePumpCFRunLoopBase::RunWork
0x96e1166e	 [CoreFoundation]	 + 0x0001266e]	__CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__
0x96e11098	 [CoreFoundation]	 + 0x00012098]	__CFRunLoopDoSources0
0x96e36e45	 [CoreFoundation]	 + 0x00037e45]	__CFRunLoopRun
0x96e36639	 [CoreFoundation]	 + 0x00037639]	CFRunLoopRunSpecific
0x96e364aa	 [CoreFoundation]	 + 0x000374aa]	CFRunLoopRunInMode
0x96a73159	 [HIToolbox]	 + 0x00058159]	RunCurrentEventLoopInMode
0x96a72ec8	 [HIToolbox]	 + 0x00057ec8]	ReceiveNextEventCommon
0x96a72d43	 [HIToolbox]	 + 0x00057d43]	BlockUntilNextEventMatchingListInMode
0x9399aa39	 [AppKit]	 + 0x00163a39]	_DPSNextEvent
0x9399a26b	 [AppKit]	 + 0x0016326b]	-[NSApplication nextEventMatchingMask:untilDate:inMode:dequeue:]
0x939906cb	 [AppKit]	 + 0x001596cb]	-[NSApplication run]
0x00acb6d0	 [Google Chrome Framework]	 - message_pump_mac.mm:574]	base::MessagePumpNSApplication::DoRun
0x00acb20b	 [Google Chrome Framework]	 - message_pump_mac.mm:169]	base::MessagePumpCFRunLoopBase::Run
0x00af73bf	 [Google Chrome Framework]	 - message_loop.cc:427]	MessageLoop::RunHandler
0x00b09470	 [Google Chrome Framework]	 - run_loop.cc:45]	base::RunLoop::Run
0x00af7139	 [Google Chrome Framework]	 - message_loop.cc:307]	MessageLoop::Run
0x004eb931	 [Google Chrome Framework]	 - renderer_main.cc:239]	RendererMain
0x00a5f29a	 [Google Chrome Framework]	 - content_main_runner.cc:437]	content::ContentMainRunnerImpl::Run
0x00a5e5af	 [Google Chrome Framework]	 - content_main.cc:35]	content::ContentMain
0x00013148	 [Google Chrome Framework]	 - chrome_main.cc:32]	ChromeMain
0x0000af77	 [Google Chrome Helper]	 - chrome_exe_main_mac.cc:16]	main
0x0000af54	 [Google Chrome Helper]	 + 0x00000f54]	start
0x00000007	

## Timeline

### nd...@chromium.org (2012-09-26)

[Empty comment from Monorail migration]

### nd...@chromium.org (2012-10-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-02)

[Empty comment from Monorail migration]

### nd...@chromium.org (2012-10-02)

[Empty comment from Monorail migration]

### nd...@chromium.org (2012-10-03)

[Empty comment from Monorail migration]

### nd...@chromium.org (2012-10-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-03)

Adding reward-topanel since attekett repro was useful to reproduce this. Otherwise, we just had a crash stack as per https://crbug.com/chromium/152569#c0.

### bu...@chromium.org (2012-10-03)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=159853

------------------------------------------------------------------------
r159853 | nduca@chromium.org | 2012-10-03T06:03:39.094364Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/gpu/compositor_output_surface.h?r1=159853&r2=159852&pathrev=159853
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/gpu/compositor_output_surface.cc?r1=159853&r2=159852&pathrev=159853

Dont let messages hit CompositorOutputSurface after it is destroyed.

BUG=152569


Review URL: https://chromiumcodereview.appspot.com/11044008
------------------------------------------------------------------------

### nd...@chromium.org (2012-10-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-03)

Does this affect m22 as well ?

### nd...@chromium.org (2012-10-03)

The code landed in r151387, so its in the branch. However, we dont send any vsync messages in 22. So, I think we're ok with 22. I'm going to let this cook on tomorrow's canary before I drover, though, to double check that I got this right.

### in...@chromium.org (2012-10-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-04)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=160189

------------------------------------------------------------------------
r160189 | nduca@chromium.org | 2012-10-04T19:18:24.583032Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/content/renderer/gpu/compositor_output_surface.cc?r1=160189&r2=160188&pathrev=160189
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/content/renderer/gpu/compositor_output_surface.h?r1=160189&r2=160188&pathrev=160189

Merge 159853 - Dont let messages hit CompositorOutputSurface after it is destroyed.

BUG=152569


Review URL: https://chromiumcodereview.appspot.com/11044008

TBR=nduca@chromium.org
Review URL: https://codereview.chromium.org/11039043
------------------------------------------------------------------------

### jb...@chromium.org (2012-10-05)

I don't really understand the threading here, so forgive me if this is a dumb question, but is it possible for it to be in CompositorOutputSurface::OnUpdateVSyncParameters while (and after) the destructor is being called?

### nd...@chromium.org (2012-10-05)

You mean OnUpdateVSyncParams causing a ~CompositorOutputSurface?

### in...@chromium.org (2012-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-29)

@attekett: we already had this bug on file when your report came in, but your report greatly helped us reproduce the issue properly, hence a $500 bonus!

### sc...@gmail.com (2012-12-14)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/152569?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/153189]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076359)*
