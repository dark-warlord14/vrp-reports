# Security: Browser crash document.createEvent("MouseEvents").initMouseEvent in background tab

| Field | Value |
|-------|-------|
| **Issue ID** | [40057698](https://issues.chromium.org/issues/40057698) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI |
| **Platforms** | Linux |
| **Reporter** | mi...@gmail.com |
| **Assignee** | de...@chromium.org |
| **Created** | 2012-05-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

What steps will reproduce the problem?

1. Create a page which causes the crash. I've attached one with further explenation in the code. (cause-crash.html)
2. Open a page with a HTML link to the crash causing page. (Attached link.html and link-iframe.html)
3. Open the link in a new tab, stay on the current page (link.html or link-iframe.html) and wait until the crash causing page was loaded.

What is the expected result?  

The tab in the background should load normaly.

What happens instead?  

If the current page has got any iframe in it (ex. link-iframe.html)  

- The browser will crash directly.  

If the current page has not got any iframe in it (ex. link.html)  

- The user has to selects on of the options from the select element which is now shown on the active page by the page in the background.  

If the current page has not got an iframe in it but the browser crashs directly then  

- The page had an iframe in it before and the chache wasn't cleared. (Important even if you can't find the iframe by using inspect element this will be the reason)

**VERSION**  

Chrome Version: 18.0.1025.168 stable  

Operating System: Linux Ubuntu 12.04 stable

**REPRODUCTION CASE**  

Attached:

- crash-causing.html
- link.html
- link-iframe.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: unknown  

I use google chrome  

dpkg -l | grep chromium-  

has got no output so chromium-browser doesn't exists  

no explenation was given for Linux in this case on <http://www.chromium.org/for-testers/bug-reporting-guidelines/reporting-crash-bug>  

Client ID (if relevant): 9c0b285a82df862c

## Attachments

- [link.html](attachments/link.html) (text/plain; charset=us-ascii, 52 B)
- [crash-causing.html](attachments/crash-causing.html) (text/html; charset=us-ascii, 1.5 KB)
- [link-iframe.html](attachments/link-iframe.html) (text/plain; charset=us-ascii, 69 B)
- [crash-causing.html](attachments/crash-causing_53003922.html) (text/html; charset=us-ascii, 1.5 KB)

## Timeline

### mi...@gmail.com (2012-05-04)

Important! This might be not clear enough. To make the issue work you should open the links to crash-causing.html by clicking on them with the mouse wheel not by right-click and open in a new tab!

### [Deleted User] (2012-05-04)

I haven't been able to reproduce this anywhere yet. I did see strange behavior once with the select box but no crash. Could you please provide the crash id for the crashes you are seeing.

Go to chrome://crashes and post the ID listed, hopefully this will give us a bit more context.

### mi...@gmail.com (2012-05-04)

I've provided one already. However here are another two:
Produced by active page without iframe: 930bad06065bd840
Produced by active page with iframe: 982bd042b4b2286e

### [Deleted User] (2012-05-07)

Looks like a bad cast. It is dying with the GLib error 
[23582:23582:2143878931188:FATAL:browser_main_loop.cc(154)] GLib-GObject: invalid cast from `GtkFloatingContainer' to `GtkWindow'

Here is the backtrace

#0  base::debug::BreakDebugger () at base/debug/debugger_posix.cc:218
#1  0x00007ffff0d0141a in logging::LogMessage::~LogMessage (this=0x7fffffffae20, __in_chrg=<optimized out>) at base/logging.cc:648
#2  0x00007ffff34de9b4 in (anonymous namespace)::GLibLogHandler(const gchar *, <anonymous enum>, const gchar *, gpointer) (
    log_domain=0x7fffed80f7f2 "GLib-GObject", log_level=G_LOG_LEVEL_WARNING, message=0x7fffda6805b0 "invalid cast from `GtkFloatingContainer' to `GtkWindow'", 
    userdata=0x0) at content/browser/browser_main_loop.cc:154
#3  0x00007fffed340fb9 in IA__g_logv (log_domain=<optimized out>, log_level=<optimized out>, format=<optimized out>, args1=0x7fffffffbda0)
    at /tmp/glib2.0.0xzuTt/glib2.0-2.24.1/glib/gmessages.c:519
#4  0x00007fffed3413d3 in IA__g_log (log_domain=0x7fffffffa320 "P\243\377\377\377\177", log_level=78, format=0x0)
    at /tmp/glib2.0.0xzuTt/glib2.0-2.24.1/glib/gmessages.c:569
#5  0x00007fffed8071d2 in IA__g_type_check_instance_cast (type_instance=0x7fffd727d1b0, iface_type=<optimized out>)
    at /tmp/glib2.0.0xzuTt/glib2.0-2.24.1/gobject/gtype.c:3978
#6  0x00007ffff3615205 in RenderWidgetHostViewGtk::InitAsPopup (this=0x7fffd2512200, parent_host_view=0x7fffd2513a00, pos=...)
    at content/browser/renderer_host/render_widget_host_view_gtk.cc:597
#7  0x00007ffff367a008 in WebContentsViewHelper::ShowCreatedWidget (this=0x7fffd3232c70, web_contents=0x7fffd903dc00, route_id=2, is_fullscreen=false, 
    initial_pos=...) at content/browser/web_contents/web_contents_view_helper.cc:215
#8  0x00007ffff3678548 in content::WebContentsViewGtk::ShowCreatedWidget (this=0x7fffd3232c60, route_id=2, initial_pos=...)
    at content/browser/web_contents/web_contents_view_gtk.cc:352
#9  0x00007ffff35ef29a in content::RenderViewHostImpl::OnMsgShowWidget (this=0x7fffd7245300, route_id=2, initial_pos=...)
    at content/browser/renderer_host/render_view_host_impl.cc:1041
#10 0x00007ffff35f6932 in DispatchToMethod<content::RenderViewHostImpl, void (content::RenderViewHostImpl::*)(int, gfx::Rect const&), int, gfx::Rect> (
    obj=0x7fffd7245300, method=
    (void (content::RenderViewHostImpl::*)(content::RenderViewHostImpl * const, int, const gfx::Rect &)) 0x7ffff35ef222 <content::RenderViewHostImpl::OnMsgShowWidget(int, gfx::Rect const&)>, arg=...) at ./base/tuple.h:554
#11 0x00007ffff35f4941 in ViewHostMsg_ShowWidget::Dispatch<content::RenderViewHostImpl, content::RenderViewHostImpl, void (content::RenderViewHostImpl::*)(int, gfx::Rect const&)> (msg=0x7fffd720e328, obj=0x7fffd7245300, sender=0x7fffd7245300, func=
    (void (content::RenderViewHostImpl::*)(content::RenderViewHostImpl * const, int, const gfx::Rect &)) 0x7ffff35ef222 <content::RenderViewHostImpl::OnMsgShowWidget(int, gfx::Rect const&)>) at ./content/common/view_messages.h:1255
#12 0x00007ffff35ed295 in content::RenderViewHostImpl::OnMessageReceived (this=0x7fffd7245300, msg=...)
    at content/browser/renderer_host/render_view_host_impl.cc:903
#13 0x00007ffff35dc2a9 in RenderProcessHostImpl::OnMessageReceived (this=0x7fffd299afc0, msg=...)
    at content/browser/renderer_host/render_process_host_impl.cc:939
#14 0x00007ffff0dbe68a in IPC::ChannelProxy::Context::OnDispatchMessage (this=0x7fffd2302160, message=...) at ipc/ipc_channel_proxy.cc:247
#15 0x00007ffff0dc1bc3 in base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>::Run (this=0x7fffffffd130, 
    object=0x7fffd2302160, a1=...) at ./base/bind_internal.h:188
#16 0x00007ffff0dc168b in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) (runnable=..., a1=@0x7fffd720e320: 0x7fffd2302160, a2=...) at ./base/bind_internal.h:896
#17 0x00007ffff0dc0f7a in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context*, IPC::Message const&), void (IPC::ChannelProxy::Context*, IPC::Message)>, void (IPC::ChannelProxy::Context*, IPC::Message const&)>::Run(base::internal::BindStateBase*) (base=0x7fffd720e300) at ./base/bind_internal.h:1254
#18 0x00007ffff01b1f03 in base::Callback<void ()>::Run() const (this=0x7fffffffd488) at ./base/callback.h:272
#19 0x00007ffff0d0630c in MessageLoop::RunTask (this=0x7fffe242c400, pending_task=...) at base/message_loop.cc:458
#20 0x00007ffff0d06423 in MessageLoop::DeferOrRunPendingTask (this=0x7fffe242c400, pending_task=...) at base/message_loop.cc:470
#21 0x00007ffff0d06c17 in MessageLoop::DoWork (this=0x7fffe242c400) at base/message_loop.cc:647
#22 0x00007ffff0d7ff23 in base::MessagePumpGlib::HandleDispatch (this=0x7fffeececd20) at base/message_pump_glib.cc:275
#23 0x00007ffff0d7f46f in (anonymous namespace)::WorkSourceDispatch (source=0x7fffeececd90, unused_func=0, unused_data=0x0) at base/message_pump_glib.cc:105
#24 0x00007fffed3368c2 in g_main_dispatch (context=<optimized out>) at /tmp/glib2.0.0xzuTt/glib2.0-2.24.1/glib/gmain.c:1960
#25 IA__g_main_context_dispatch (context=0x7fffeeca1c40) at /tmp/glib2.0.0xzuTt/glib2.0-2.24.1/glib/gmain.c:2513
#26 0x00007fffed33a748 in g_main_context_iterate (context=0x7fffeeca1c40, block=<optimized out>, dispatch=<optimized out>, self=<optimized out>)
    at /tmp/glib2.0.0xzuTt/glib2.0-2.24.1/glib/gmain.c:2591
#27 0x00007fffed33a8fc in IA__g_main_context_iteration (context=0x7fffeeca1c40, may_block=1) at /tmp/glib2.0.0xzuTt/glib2.0-2.24.1/glib/gmain.c:2654
#28 0x00007ffff0d7fbd2 in base::MessagePumpGlib::RunWithDispatcher (this=0x7fffeececd20, delegate=0x7fffe242c400, dispatcher=0x0)
    at base/message_pump_glib.cc:206
#29 0x00007ffff0d80000 in base::MessagePumpGlib::Run (this=0x7fffeececd20, delegate=0x7fffe242c400) at base/message_pump_glib.cc:298
#30 0x00007ffff0d05fd3 in MessageLoop::RunInternal (this=0x7fffe242c400) at base/message_loop.cc:417
#31 0x00007ffff0d05e8a in MessageLoop::RunHandler (this=0x7fffe242c400) at base/message_loop.cc:390
#32 0x00007ffff0d07158 in MessageLoopForUI::RunWithDispatcher (this=0x7fffe242c400, dispatcher=0x0) at base/message_loop.cc:763
#33 0x00007ffff09660bf in ChromeBrowserMainParts::MainMessageLoopRun (this=0x7fffeebfce00, result_code=0x7fffeebfbd28)
    at chrome/browser/chrome_browser_main.cc:1916
#34 0x00007ffff34e018d in content::BrowserMainLoop::RunMainMessageLoopParts (this=0x7fffeebfbd10) at content/browser/browser_main_loop.cc:453
#35 0x00007ffff34e1ad2 in (anonymous namespace)::BrowserMainRunnerImpl::Run (this=0x7fffeec33d80) at content/browser/browser_main_runner.cc:98
#36 0x00007ffff34de150 in BrowserMain (parameters=...) at content/browser/browser_main.cc:21
#37 0x00007ffff0c389bf in (anonymous namespace)::RunNamedProcessTypeMain (process_type="", main_function_params=..., delegate=0x7fffffffe440)
    at content/app/content_main_runner.cc:290
#38 0x00007ffff0c3942c in (anonymous namespace)::ContentMainRunnerImpl::Run (this=0x7fffeec04f30) at content/app/content_main_runner.cc:548
#39 0x00007ffff0c380b5 in content::ContentMain (argc=2, argv=0x7fffffffe5a8, delegate=0x7fffffffe440) at content/app/content_main.cc:35
#40 0x00007fffefe5340d in ChromeMain (argc=2, argv=0x7fffffffe5a8) at chrome/app/chrome_main.cc:32
#41 0x00007fffefe533cc in main (argc=2, argv=0x7fffffffe5a8) at chrome/app/chrome_exe_main_gtk.cc:18


I don't think this is a security issue as GLib should always perform this check and crash us but I'll leave the flags up until someone can verify that I am reading this correctly.

derat, looks like you changed this code most recently. Can you take a look and let me know if this can ever get past the check and end up as a bad cast? 


### de...@chromium.org (2012-05-07)

Looking...

### de...@chromium.org (2012-05-07)

It looks like this came from http://crrev.com/21207 / http://codereview.chromium.org/159147, way back in 2009.

 589   // The underlying X window needs to be created and mapped by the above code
 590   // before we can grab the input devices.
 591   if (NeedsInputGrab()) {
 592     // Grab all input for the app. If a click lands outside the bounds of the
 593     // popup, WebKit will notice and destroy us. Before doing this we need
 594     // to ensure that the the popup is added to the browser's window group,
 595     // to allow for the grabs to work correctly.
 596     gtk_window_group_add_window(gtk_window_get_group(
 597         GTK_WINDOW(gtk_widget_get_toplevel(parent_))), window);
 598     gtk_grab_add(view_.get());

http://www.gtk.org/api/2.6/gtk/GtkWidget.html#gtk-widget-get-toplevel says, "This function returns the topmost widget in the container hierarchy widget is a part of. If widget has no parent widgets, it will be returned as the topmost widget. ... To reliably find the toplevel GtkWindow, use gtk_widget_get_toplevel() and check if the TOPLEVEL flags is set on the result."

Speculating recklessly: perhaps the parent widget hasn't been parented inside of a window in some cases when this is called.  We should probably perform the toplevel check described in the documentation and just avoid the gtk_window_group_add_window() call if we don't get back a window.  I can do this if it sounds reasonable.

I think that this is unlikely to be a security issue.

### es...@chromium.org (2012-05-07)

sounds like that would fix the crash, but wouldn't that leave the select dropdown open with no easy way to close it (I can't remember the exact purpose of the window grouping)? if there's no toplevel window, perhaps we should close the select.

### [Deleted User] (2012-05-07)

Actually I just verified that on a release build the error isn't fatal. This will result in a cast to a GtkWindow. This bad GtkWindow is then passed into gtk_window_group_add_window() where it seems like all manner of badness can happen. It seems like it is probably possible to get more than a read off of this though.

I think I'm going to mark this high severity given that it requires a ctrl-click to trigger. 

estade, derat, if in your investigation you come up with a way to trigger this without the ctrl-click let me know.

### de...@chromium.org (2012-05-07)

Middle-click works too.  I don't have numbers on how frequently users open links in new tabs, but I bet it's frequent.

### de...@chromium.org (2012-05-07)

Working on a fix.

### de...@chromium.org (2012-05-07)

I'll check in a quick fix for the crash (not doing the grab in this case) now, but it seems pretty weird to me that we'll display menus for inactive tabs.  The user still gets a menu popping up over the toolbar.

### de...@chromium.org (2012-05-09)

https://chromiumcodereview.appspot.com/10380044/ committed as http://crrev.com/135966.  I take it this needs to be merged to 19 and (if it doesn't make the branch) 20, right?

### bu...@chromium.org (2012-05-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=135966

------------------------------------------------------------------------
r135966 | derat@chromium.org | Tue May 08 18:24:24 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_widget_host_view_gtk.cc?r1=135966&r2=135965&pathrev=135966

linux: Fix grabs for popups belonging to inactive tabs.

When displaying a popup for an inactive tab, grab input on
behalf of the popup's window rather than its parent window.

Also removes window-group code that doesn't make sense to me
here (the popup wants all input rather than just input for a
subset of browser windows, as shown by the way that it's
doing X grabs).

BUG=126296
TEST=manual

Review URL: https://chromiumcodereview.appspot.com/10380044
------------------------------------------------------------------------

### in...@chromium.org (2012-05-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-05-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=136173

------------------------------------------------------------------------
r136173 | derat@chromium.org | Wed May 09 16:44:38 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/content/browser/renderer_host/render_widget_host_view_gtk.cc?r1=136173&r2=136172&pathrev=136173

Merge 135966 - linux: Fix grabs for popups belonging to inactive tabs.

When displaying a popup for an inactive tab, grab input on
behalf of the popup's window rather than its parent window.

Also removes window-group code that doesn't make sense to me
here (the popup wants all input rather than just input for a
subset of browser windows, as shown by the way that it's
doing X grabs).

BUG=126296
TEST=manual

Review URL: https://chromiumcodereview.appspot.com/10380044

TBR=derat@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10378081
------------------------------------------------------------------------

### de...@chromium.org (2012-05-10)

I'll leave this open until we know whether it made the cut for 20 or not.

### sc...@gmail.com (2012-05-10)

The merge to M19 probably won't make M19 final? cc: @laforge to see when the final build is / was.

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### de...@chromium.org (2012-05-10)

My fix got reverted: https://chromiumcodereview.appspot.com/10378088/

I'll spend more time on this today.

### [Deleted User] (2012-05-10)

bumping the status back after this got reverted.

### [Deleted User] (2012-05-10)

For Mstone-19: r136173 will be in 19.0.1084.47 (build pending).

### bu...@chromium.org (2012-05-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=136451

------------------------------------------------------------------------
r136451 | derat@chromium.org | Thu May 10 16:43:32 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/renderer_host/render_widget_host_view_gtk.cc?r1=136451&r2=136450&pathrev=136451

Reland "linux: Fix grabs for popups belonging to ..."

This relands r135966, which was reverted by r136293.  By
adding the popup to its parent's window group, the DevTools
profiler heap snapshot combobox receives mouse input again.
I'm still not sure why this is necessary.

Original description:

When displaying a popup for an inactive tab, grab input on
behalf of the popup's window rather than its parent window.

[snip obsolete, now-removed window group change]

BUG=126296
TEST=manual: original test case is still fine; dev tool regression described in r136293 is gone


Review URL: https://chromiumcodereview.appspot.com/10389080
------------------------------------------------------------------------

### in...@chromium.org (2012-05-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-05-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=136648

------------------------------------------------------------------------
r136648 | derat@chromium.org | Fri May 11 13:23:14 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1084/src/content/browser/renderer_host/render_widget_host_view_gtk.cc?r1=136648&r2=136647&pathrev=136648

Merge 136451 - Reland "linux: Fix grabs for popups belonging to ..."

This relands r135966, which was reverted by r136293.  By
adding the popup to its parent's window group, the DevTools
profiler heap snapshot combobox receives mouse input again.
I'm still not sure why this is necessary.

Original description:

When displaying a popup for an inactive tab, grab input on
behalf of the popup's window rather than its parent window.

[snip obsolete, now-removed window group change]

BUG=126296
TEST=manual: original test case is still fine; dev tool regression described in r136293 is gone


Review URL: https://chromiumcodereview.appspot.com/10389080

TBR=derat@chromium.org
Review URL: https://chromiumcodereview.appspot.com/10381117
------------------------------------------------------------------------

### bu...@chromium.org (2012-05-11)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=136650

------------------------------------------------------------------------
r136650 | derat@chromium.org | Fri May 11 13:29:24 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/1132/src/content/browser/renderer_host/render_widget_host_view_gtk.cc?r1=136650&r2=136649&pathrev=136650

Merge 136451 - Reland "linux: Fix grabs for popups belonging to ..."

This relands r135966, which was reverted by r136293.  By
adding the popup to its parent's window group, the DevTools
profiler heap snapshot combobox receives mouse input again.
I'm still not sure why this is necessary.

Original description:

When displaying a popup for an inactive tab, grab input on
behalf of the popup's window rather than its parent window.

[snip obsolete, now-removed window group change]

BUG=126296
TEST=manual: original test case is still fine; dev tool regression described in r136293 is gone


Review URL: https://chromiumcodereview.appspot.com/10389080

TBR=derat@chromium.org
------------------------------------------------------------------------

### de...@chromium.org (2012-05-11)

The fix has been merged to 1084 as http://crrev.com/136648 and to 1132 as http://crrev.com/136650.

### sc...@gmail.com (2012-05-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-23)

@michabartholome: thanks for reporting this! It qualifies for a $1000 Chromium Security Reward :D

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

### sc...@gmail.com (2012-05-23)

BTW, not sure I'll be able to get it in on time, but let us know if there's some particular name you'd like us to credit in our release notes.

### an...@chromium.org (2012-05-23)

[Empty comment from Monorail migration]

### [Deleted User] (2012-06-15)

+erg

### sc...@gmail.com (2012-08-03)

Payment in system.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/126296?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057698)*
