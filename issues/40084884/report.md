# <Unloaded_S.DLL>+0x42cd17f crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40084884](https://issues.chromium.org/issues/40084884) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | ku...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-11-12 |
| **Bounty** | $1,000.00 |

## Description

Test chrome 9.0.576.0 dev windows xp sp3

test.php
====
<?
sleep(3);
?>

1,Open a new tab
2,Press CTRL+SHIFT+J open devtools
3,Enter x = open("http://127.0.0.1/test.php");x = open("view-source:http://127.0.0.1/test.php"); press enter
4,At the same time repeat step #3 see crash

I can't make it auto by javascript 


## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ku...@gmail.com (2010-11-12)

[Comment Deleted]

### ku...@gmail.com (2010-11-12)

[Comment Deleted]

### ku...@gmail.com (2010-11-12)

[Comment Deleted]

### ku...@gmail.com (2010-11-12)

[Comment Deleted]

### ku...@gmail.com (2010-11-12)

[Comment Deleted]

### ku...@gmail.com (2010-11-12)

[Comment Deleted]

### in...@chromium.org (2010-11-12)

might be a intermediatary regression with devtools. cannot reproduce anymore with 9.0.581.0 (65936). tried with my test.php at infernohacks.com/t/test.php and also with, without view-source calls in url x = open("view-source:http://infernohacks.com/t/test.php");x = open("view-source:http://infernohacks.com/t/test.php");. it you can still reproduce, please reproduce with more clear steps to reproduce on trunk.

### ku...@gmail.com (2010-11-13)

[Comment Deleted]

### in...@chromium.org (2010-11-13)

Thanks Kuzzcc, will check it out.

### in...@chromium.org (2010-11-16)

Yury, can you please help with a owner here. the crash looks serious as an exec on an non null address. reasons for lower secseverity since it does not look to be possible using automation.

This is reproducing outside of single process easily. Steps to reproduce::

1. Go to google.com
2. Open devtools using Ctrl+Shift+J
3. Type x = open("http://infernohacks.com/t/test.php");x = open("view-source:http://infernohacks.com/t/test.php"); and press enter.
4. Redo Step 3.
5. You will crash on a check in Debug build.
6. For release build crash, type console.log(document.domain). press enter and press enter again. Wait for the crash.

### pf...@chromium.org (2010-11-16)

@inferno: Is test.php supposed to lag and return 0 result?

### in...@chromium.org (2010-11-16)

Pavel, test.php is just a lag of 30 sec and does not return anything :)

<?
sleep(30);
?>

### pf...@chromium.org (2010-11-16)

Yeah, thanks. I started reading from the bottom of the log. Anyways, here is what I get:

>	chrome.dll!base::debug::BreakDebugger()  Line 108	C++
 	chrome.dll!logging::LogMessage::~LogMessage()  Line 670	C++
 	chrome.dll!IDMap<IPC::Channel::Listener,0>::AddWithID(IPC::Channel::Listener * data=0x0bebc600, int id=2)  Line 66 + 0xc0 bytes	C++
 	chrome.dll!RenderProcessHost::Attach(IPC::Channel::Listener * listener=0x0bebc600, int routing_id=2)  Line 116	C++
 	chrome.dll!RenderWidgetHost::RenderWidgetHost(RenderProcessHost * process=0x0868e160, int routing_id=2)  Line 100	C++
 	chrome.dll!RenderViewHost::RenderViewHost(SiteInstance * instance=0x082bdbb0, RenderViewHostDelegate * delegate=0x094d4b88, int routing_id=2, SessionStorageNamespace * session_storage=0x06582420)  Line 136 + 0x40 bytes	C++
 	chrome.dll!RenderViewHostFactory::Create(SiteInstance * instance=0x082bdbb0, RenderViewHostDelegate * delegate=0x094d4b88, int routing_id=2, SessionStorageNamespace * session_storage_namespace=0x06582420)  Line 24 + 0x2e bytes	C++
 	chrome.dll!RenderViewHostManager::Init(Profile * profile=0x00967000, SiteInstance * site_instance=0x082bdbb0, int routing_id=2)  Line 62 + 0x38 bytes	C++
 	chrome.dll!TabContents::TabContents(Profile * profile=0x00967000, SiteInstance * site_instance=0x082bdbb0, int routing_id=2, const TabContents * base_tab_contents=0x0098db00, SessionStorageNamespace * session_storage_namespace=0x00000000)  Line 400	C++
 	chrome.dll!RenderViewHostDelegateViewHelper::CreateNewWindow(int route_id=2, Profile * profile=0x00967000, SiteInstance * site=0x082bdbb0, void * domui_type=0x00000000, RenderViewHostDelegate * opener=0x0098db08, WindowContainerType window_container_type=WINDOW_CONTAINER_TYPE_NORMAL, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > & frame_name="_blank")  Line 102 + 0x43 bytes	C++
 	chrome.dll!TabContentsView::CreateNewWindow(int route_id=2, WindowContainerType window_container_type=WINDOW_CONTAINER_TYPE_NORMAL, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > & frame_name="_blank")  Line 43 + 0xa2 bytes	C++
 	chrome.dll!RenderViewHost::CreateNewWindow(int route_id=2, WindowContainerType window_container_type=WINDOW_CONTAINER_TYPE_NORMAL, const std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > & frame_name="_blank")  Line 940 + 0x1a bytes	C++
 	chrome.dll!RenderWidgetHelper::OnCreateWindowOnUI(int opener_id=1, int route_id=2, WindowContainerType window_container_type=WINDOW_CONTAINER_TYPE_NORMAL, std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > frame_name="_blank")  Line 234	C++
 	chrome.dll!DispatchToMethod<RenderWidgetHelper,void (__thiscall RenderWidgetHelper::*)(int,int,enum WindowContainerType,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >),int,int,enum WindowContainerType,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > >(RenderWidgetHelper * obj=0x0662a880, void (int, int, WindowContainerType, std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >)* method=0x6070eca0, const Tuple4<int,int,enum WindowContainerType,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > > & arg={...})  Line 574	C++
 	chrome.dll!RunnableMethod<RenderWidgetHelper,void (__thiscall RenderWidgetHelper::*)(int,int,enum WindowContainerType,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> >),Tuple4<int,int,enum WindowContainerType,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > > >::Run()  Line 330 + 0x1a bytes	C++
 	chrome.dll!MessageLoop::RunTask(Task * task=0x0bec35a0)  Line 418 + 0xf bytes	C++
 	chrome.dll!MessageLoop::DeferOrRunPendingTask(const MessageLoop::PendingTask & pending_task={...})  Line 430	C++
 	chrome.dll!MessageLoop::DoWork()  Line 534 + 0xc bytes	C++
 	chrome.dll!base::MessagePumpForUI::DoRunLoop()  Line 201 + 0x1d bytes	C++
 	chrome.dll!base::MessagePumpWin::RunWithDispatcher(base::MessagePump::Delegate * delegate=0x00930000, base::MessagePumpWin::Dispatcher * dispatcher=0x0021e298)  Line 49 + 0xf bytes	C++
 	chrome.dll!MessageLoop::RunInternal()  Line 262	C++
 	chrome.dll!MessageLoop::RunHandler()  Line 239	C++
 	chrome.dll!MessageLoopForUI::Run(base::MessagePumpWin::Dispatcher * dispatcher=0x0021e298)  Line 677	C++
 	chrome.dll!`anonymous namespace'::RunUIMessageLoop(BrowserProcess * browser_process=0x00932000)  Line 513	C++
 	chrome.dll!BrowserMain(const MainFunctionParams & parameters={...})  Line 1611 + 0xe bytes	C++
 	chrome.dll!ChromeMain(HINSTANCE__ * instance=0x00ef0000, sandbox::SandboxInterfaceInfo * sandbox_info=0x0021f86c, wchar_t * command_line=0x00481c6a)  Line 838 + 0xc bytes	C++


### in...@chromium.org (2010-11-23)

Pavel, Yury: ping, did you get a chance to take a look ?

### in...@chromium.org (2010-12-01)

Pavel, Yury, can you please take a look. the crash is still reproducing in canary 9.0.597.0 canary build.

### js...@chromium.org (2011-01-08)

I was unable to repro this on a recent dev channel. Was it fixed, and any clue as to when?

### pf...@chromium.org (2011-01-10)

I could repro it on ToT with the same stack. It does not seem to be devtools-specific, RenderProcessHost::Attach is being called with the same id twice. Adding Darin to help triaging.

### sc...@gmail.com (2011-01-22)

Can we get an owner for this one? Looking at the stack trace, it appears to be a whole-browser crash? That makes me nervous.

### pf...@chromium.org (2011-01-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-02-01)

@yurys : ping !, can you please take a look.

### yu...@chromium.org (2011-02-02)

I agree with Pavel that it doesn't look like a DevTools-specific problem. Can we have someone who works on IPC look at this issue? I'm pretty sure that DevTools is not the only example where this issue can be reproduced.

### js...@chromium.org (2011-03-07)

This seems seems to have slipped off the radar. If it's not a devtools-specific problem then it's a generic sandbox escalation issue (and thus a higher severity). Any idea who should be looking at this?

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-04-07)

Kuzzcc, this does not reproduce anymore on trunk or m10 stable. can you please try again to see if the bug still reproduce for you ??

### ku...@gmail.com (2011-04-08)

1, open data:text/html,<a href="http://www.google.cn">somewhere</a>
2, shift+ctrl+j open devtools
3, devtools open("view-source:http://infernohacks.com/t/test.php");
4, click "somewhere"
5, wait for seconds click history back
6, devtools open("view-source:http://infernohacks.com/t/test.php");
7, devtools open("view-source:http://infernohacks.com/t/test.php");
8, devtools open("view-source:http://infernohacks.com/t/test.php");
9, devtools open("view-source:http://infernohacks.com/t/test.php");
10, devtools open("view-source:http://infernohacks.com/t/test.php");
11, devtools open("view-source:http://infernohacks.com/t/test.php");
12, devtools open("view-source:http://infernohacks.com/t/test.php");
13, devtools open("view-source:http://infernohacks.com/t/test.php");
14,click stop button
15,close it

### ku...@gmail.com (2011-04-08)

[Comment Deleted]

### ku...@gmail.com (2011-04-08)

[Comment Deleted]

### js...@chromium.org (2011-04-12)

@darin - Any chance you can take a look at this or direct it to someone who knows the majority of the moving parts?

### da...@chromium.org (2011-04-19)

Based on https://crbug.com/chromium/62925#c13, I'm guessing that we are tripping on this assertion:

  DCHECK(data_.find(id) == data_.end()) << "Inserting duplicate item";

I'm not sure how to explain that.

### in...@chromium.org (2011-05-26)

Mass update to M12.

### sc...@gmail.com (2011-06-09)

@kuzzcc: does this still hit in Chrome 12? Sorry that this bug is dragging on.

### ku...@gmail.com (2011-06-09)

Yes,  hit Chrome 13.0.782.13

(470.508): Access violation - code c0000005 (!!! second chance !!!)
eax=04beb580 ebx=00000001 ecx=04beb6e0 edx=0113005c esi=04979300 edi=0496b240
eip=00000000 esp=0012fff8 ebp=00000000 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00200246
Missing image name, possible paged-out or corrupt data.
Missing image name, possible paged-out or corrupt data.
Missing image name, possible paged-out or corrupt data.
00000000 ??              ???
0:000> .exr -1
ExceptionAddress: 00000000
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 00000000
Attempt to execute non-executable address 00000000



### sc...@gmail.com (2011-06-10)

@darin: any idea who would be the best person to fix this bug? Seems like it's getting a little old for a possible security issue.

### ku...@gmail.com (2011-06-10)

1, Open data:text/html,<a href="http://www.google.cn">somewhere</a>
2, Devtools open("view-source:http://infernohacks.com/t/test.php");
3, Devtools open("view-source:http://infernohacks.com/t/test.php");
4, Close it

### in...@chromium.org (2011-07-06)

Moving all M12 bugs to M13. We won't have another M12 patch.

### in...@chromium.org (2011-07-07)

[Empty comment from Monorail migration]

### [Deleted User] (2011-07-13)

I have been digging into this bug and I have a couple of notes:

- To more consistently trigger the bug, clear the browsing data before trying to trigger again

-What I am seeing is that there there can be multiple RenderWidgetHost instances with the same (RenderProcessHost *)process_ attribute.

This is what triggers the bug:
Each RenderWidgetHelper triggers a RenderWidgetHelper::OnCreateWindowOnUI call where route_id is set.  When the RenderWidgetHelper instances are distinct, two different RenderWidgetHelpers may end up with the same route_id to use when calling CreateNewWindow(). 

Inside the CreateNewWindow() call, RenderWidgetHost calls process_->Attach(this,routing_id_), and what ends up happening is  process_ tries to add that routing_id_ to its listeners_, but it appears to already be there because some other RenderWidgetHost with the same routing_id_ beat it to the punch.

Given that I am not particularly familiar with the code base yet, I am unsure as to what the correct behavior/fix should be.  If we want to allow multiple RenderWidgetHost instances to register routing_ids they generated with the same RenderProcessHost, then we need to use different keys for the IDMap... otherwise I would have to dig deeper to think up a fix.

### sc...@gmail.com (2011-07-13)

@darin: any hints for Bex to continue with a fix?

### br...@chromium.org (2011-07-13)

The route ID generation should be "quite unique" for each RenderProcessHost. This implies to me that we're getting confused with different processes.

The RenderProcessHost for the created window must match the one the original RenderView that created the rout ID was in. The create function does this using the site instance. This implies to me that the site instance we're getting in RenderViewHostDelegateViewHelper doesn't match the one belonging to the original render view.

(I think the code has changed a bit since the above stack was captured.)

But anyway, I think this can happen if a RenderViewHost from a process that's not foreground is sending the original create window message. We'd then end up with the site instance from the foreground one in a different process, using the route ID from another process. Somebody with the repro should double-check this theory in the debugger when the assert happens.

I suspect we should be sending the SiteInstance along with the route ID "up" the stack so we can't get confused with this kind of thing.

It might be the right thing to check in the TabContents layer that the RVH is the current one and ignore the create window request otherwise. I think this would also independently fix this bug, but I think we should do both. There is also some scary code in the window creation logic to GetWebUITypeForCurrentState which potentially could get confused if background RVH's ever send new window messages, and that could cause its own security problems.

It would be great to hear Charlie's opinion.

### cr...@chromium.org (2011-07-14)

I haven't had a chance to debug this one, but I agree that a route_id collision sounds like route_ids from different processes are getting used, and Brett's description sounds plausible.  Threading the SiteInstance through is similar to what we do in NavigationController when trying to find things by page ID (e.g., GetEntryIndexWithPageID).

I'm surprised that we'd see a route_id from a different RenderProcessHost, but I don't know that code very well, so it's certainly possible.

### ma...@google.com (2011-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2011-07-22)

How does the decide which RenderWidgetHelper handles a given CreateWindow message?  The RWH that is chosen ends up being the object that creates the route ID for the new RenderView. 

Since we have two different RenderWidgetHelpers with different render_process_ids creating routing IDs on behalf of the same RenderView, does that mean there is a problem with the message routing?  My (possibly incorrect) understanding is that there should be a single RenderWidgetHelper handling CreateWindow (etc) messages from the same RenderView. 

The CreateWindow request is initiated by a synchronous message, so it seems like we shouldn't fail when the SiteInstance is wrong if the issue is really just with routing.  (Unless of course it happens to be that the correct RenderWidgetHelper is waiting in line to handle the CreateWindow message and we just haven't reached it yet... )  Although I do agree that threading the SiteInstance through gives us enough information to correctly decide as to whether we should handle the message.

@creis, would you be able to point out where SiteInstance is used to help with with GetEntryIndexWithPageID?

### ma...@google.com (2011-07-28)

I'll handle this one.

### ma...@google.com (2011-07-28)

Er... that was a mistake.

### sc...@gmail.com (2011-07-28)

Sorry, Mark. You're committed now.

### sc...@gmail.com (2011-07-29)

This is now our oldest known crash bug with security consequences :D
Can anyone be bribed to sit down with Bex and debug it a little?

### cr...@chromium.org (2011-07-29)

Sorry to be out of touch on this one.  I'm trying to wrap up some URL spoof bugs today, but I'll set aside some time on Monday to dive into this one a bit and discuss it with Bex.

### cr...@chromium.org (2011-08-01)

Ok, I've looked a little closer and have a few thoughts for what's going on, but I haven't been able to reproduce the crash at all so it's tough to confirm it.

The first thing to note is that the test cases tend to open a window to a view-source: URL, which will eventually live in a different renderer process than the current page.  That page will end up with a different SiteInstance and RenderProcessHost than the original tab.

When the CreateNewWindow call arrives, it's part of the original tab (e.g., google.com in https://crbug.com/chromium/62925#c10).  It goes through all the steps in the stack trace in https://crbug.com/chromium/62925#c13 to create a new TabContents and RenderViewHost, using the same SiteInstance as the parent.  It looks to me like the new tab won't switch its SiteInstance (for the view-source page) until later, when the navigation occurs.  That happens via RenderViewHostManager::CreatePendingRenderView.

This makes the crash seem strange to me-- the stack trace where we're crashing should be using a route_id from the original tab's process, so I expect it to be correct.  Our earlier discussion made me think RenderViewHostDelegateViewHelper::CreateNewWindowFromTabContents might have been the culprit, since it asks for tab_contents->GetSiteInstance(), which might not match the RenderViewHost that called CreateNewWindow.  (For example, tab_contents might have had a pending RenderViewHost.)  However, it doesn't sound like the original tab is navigating, so that might not be the bug.

If something else got there first and incorrectly registered the same route_id (perhaps as part of the navigation from an earlier call to window.open?), then I'd expect the collision when we got there the second time.

Bex, can you post the set of repro steps that work for you?  I tried disabling popup blocking and trying the steps described so far, but I've never seen the crash.  If you can repro it, I'd suggest comparing the SiteInstance at the RenderViewHost constructor (near the top of the call stack) with the one in the RenderViewHost::CreateNewWindow call.  If they don't match, that's probably what we're looking for.

### cr...@chromium.org (2011-08-02)

Several more observations.

1) I was able to reproduce this on a slightly older Mac debug build, using the steps in https://crbug.com/chromium/62925#c10.  My up-to-date Linux build won't repro, and it sounds like Bex might not be able to repro on a new build, so it's possible a recent change has affected this.

2) Does anyone know what the security consequences are?  We're not overwriting arbitrary memory in AddWithID-- we're just replacing an existing entry.  Is it exploitable?

3) By debugging during the crash, I found out that the CreateNewWindow call is coming from the pending RenderViewHost of a TabContents.  That means our guess of RenderViewHostDelegateViewHelper::CreateNewWindowFromTabContents is correct-- it's grabbing the SiteInstance from the current RenderViewHost, rather than the RenderViewHost that sent the message.  We should probably pass in a pointer to the actual RenderViewHost that sent the message, avoiding this issue in the future.

4) There's actually an uglier bug here underneath that.  The TabContents with the pending RVH is actually the *original* TabContents.  There's no reason it should be navigating anywhere-- we're telling a view-source link to open in a new window.  As it turns out, any window.open call that causes a process swap appears to be causing the navigation to occur in the original window.  That's bad.  (You can see it most easily on view-source URLs, but you can also see it if you do a window.open to a URL for an installed hosted app.)

That's the reason we're getting into this unexpected situation in the first place.  We should still fix the issue in bullet (3), but we definitely need to make sure bullet (4) gets fixed.

I can repro it in the 15.0.840.0 Canary, but not on my tip-of-tree Linux build.  Bex and/or I can look more closely to see what's going wrong and whether some other CL has resolved it.

### cr...@chromium.org (2011-08-02)

By setting a breakpoint in RenderViewHostManager::Navigate and running window.open("view-source:http://www.chromium.org"), I'm trying to find the spot that's sending the navigation to the wrong tab.

It looks like the OpenURL message is coming from the renderer process to a TabContents with no state (maybe the newly opened one?), but then BlockedContentContainer::OpenURLFromTab is redirecting the call to the original TabContents (maybe because it has the wrong owner_->tab_contents() value?).  Maybe this is only happening when the popup blocker is enabled, and that call is sending it to the wrong TabContents.

Need to go for now, but that looks like the right place to investigate.

### sc...@gmail.com (2011-08-03)

Thanks Charlie :)

### sc...@gmail.com (2011-08-03)

Upping milestone. Seems like we won't get to this for the M13 patch ;-)

### sc...@gmail.com (2011-08-10)

Thanks all for the various useful comments on this one. Unless there are any objections, or someone chimes in and says they're actively working it, I'll likely tackle this as the next bug on my plate tomorrow.

### [Deleted User] (2011-08-24)

[Comment Deleted]

### [Deleted User] (2011-08-24)

[Comment Deleted]

### [Deleted User] (2011-08-24)

It looks like a lot of refactoring has been done to the code that is involved in this bug, the real question is whether the underlying issues that creis spotted (see https://crbug.com/chromium/62925#c50) have been fixed.  

I would like to figure out which patch smothered this bug and then get the author of the patch to check out this bug report. There are a few promising revisions that I will look at (such as the one that patches https://crbug.com/chromium/87702-- owned by jam).

### sc...@gmail.com (2011-08-28)

@kuzzcc: can you still reproduce it on the latest M15 dev builds? @bxx thinks that it has stop reproducing. Weird.

### cr...@chromium.org (2011-08-30)

The behavior that I described in https://crbug.com/chromium/62925#c50 with cross-process popups navigating their opener is still present in Chrome 15.0.865.0.  It's also been filed as https://crbug.com/chromium/93412 (cc'ing Mihai), so maybe we can pursue it there.

I'm not seeing this crash in that build, for what it's worth.

### ku...@gmail.com (2011-08-30)

Can not reproduce on 15.0.861.0 :)

### in...@chromium.org (2011-08-30)

Kuzzcc has been very useful here. And this was a real bug, so closing in FixUnreleased.

### [Deleted User] (2011-08-30)

Just as an FYI: It looks like this bug stops being reproducible at svn revision 94329 (http://src.chromium.org/viewvc/chrome?view=rev&revision=94329) where webkit is updated.  

### ku...@gmail.com (2011-09-05)

Thank you, securityteam.

### sc...@gmail.com (2011-09-08)

@kuzzcc: definitely an interesting issue, and seems to have some severity, so our pleasure to offer a $1000 Chromium Security Reward :D

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

### js...@chromium.org (2011-10-05)

Batch update: fuzzily determined that this security bug affected a stable release.

### sc...@gmail.com (2011-11-03)

Payment in system. Sorry for the delay on this one.

### ku...@gmail.com (2012-01-08)

Is this bug fixed?
I got new crash chrome 17.0.963.26 dev-m

### ku...@gmail.com (2012-03-16)

location = 'view-source:http://www.google.com:999';location = 'view-source:http://www.google.com:999';alert('now press ok \nthen ctrl+shift+j');setTimeout(function(){location='data:text/html,1'}, 3000)



### ku...@gmail.com (2012-03-16)

Test chrome 19.0.1068.1 dev-m windows xp 

### sc...@gmail.com (2012-03-16)

Does it look like the same crash?

### cr...@chromium.org (2012-03-16)

I can't confirm the crash in Chrome 17 or 19.  I'm trying it out by visiting chrome://history (as shown in the screenshot) and pasting the command from https://crbug.com/chromium/62925#c68 into the web inspector.

### ku...@gmail.com (2012-03-19)

(a10.754): Access violation - code c0000005 (!!! second chance !!!)
eax=69646769 ebx=00000001 ecx=05360320 edx=0527e500 esi=05360320 edi=063d1124
eip=69646769 esp=0012f340 ebp=0012f34c iopl=0         nv up ei pl nz ac pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00200216
Missing image name, possible paged-out or corrupt data.
Missing image name, possible paged-out or corrupt data.
Missing image name, possible paged-out or corrupt data.
69646769 ??              ???
0:000> kp
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0012f33c 01d3bb9b 0x69646769
0012f34c 01d3bca3 chrome_1c30000!content::DevToolsAgentHost::DipatchOnInspectorBackend(class std::basic_string<char,std::char_traits<char>,std::allocator<char> > * message = 0x0012f37c)+0x2b [c:\b\build\slave\win\build\src\content\browser\debugger\devtools_agent_host.cc @ 31]
0012f358 02c0b379 chrome_1c30000!content::DevToolsManagerImpl::DispatchOnInspectorBackend(class content::DevToolsClientHost * from = 0x05f7c740, class std::basic_string<char,std::char_traits<char>,std::allocator<char> > * message = 0x0012f37c)+0x23 [c:\b\build\slave\win\build\src\content\browser\debugger\devtools_manager_impl.cc @ 76]
0012f36c 0277d5a4 chrome_1c30000!content::DevToolsFrontendHost::OnDispatchOnInspectorBackend(class std::basic_string<char,std::char_traits<char>,std::allocator<char> > * message = 0x0012f37c)+0x19 [c:\b\build\slave\win\build\src\content\browser\debugger\devtools_frontend_host.cc @ 88]
0012f39c 02c0b55a chrome_1c30000!AutomationMsg_SetProxyConfig::Dispatch<AutomationProvider,AutomationProvider,void (class IPC::Message * msg = 0x063d1124, class AutomationProvider * obj = 0x05f7c740, class AutomationProvider * sender = 0x05f7c740, <function> * func = 0x02c0b360)+0x44 [c:\b\build\slave\win\build\src\chrome\common\automation_messages_internal.h @ 908]
0012f45c 01cb9d4a chrome_1c30000!content::DevToolsFrontendHost::OnMessageReceived(class IPC::Message * message = 0x063d1124)+0x7a [c:\b\build\slave\win\build\src\content\browser\debugger\devtools_frontend_host.cc @ 68]
0012f788 01c64b33 chrome_1c30000!content::RenderViewHostImpl::OnMessageReceived(class IPC::Message * msg = 0x063d1124)+0xba [c:\b\build\slave\win\build\src\content\browser\renderer_host\render_view_host_impl.cc @ 792]
0012f89c 022249ab chrome_1c30000!RenderProcessHostImpl::OnMessageReceived(class IPC::Message * msg = 0x063d1124)+0x3c3 [c:\b\build\slave\win\build\src\content\browser\renderer_host\render_process_host_impl.cc @ 929]
0012f8d0 02a6ead8 chrome_1c30000!IPC::ChannelProxy::Context::OnDispatchMessage(class IPC::Message * message = 0x063d1124)+0xbb [c:\b\build\slave\win\build\src\ipc\ipc_channel_proxy.cc @ 274]
0012f8e0 023aded1 chrome_1c30000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (class base::internal::BindStateBase * base = 0x063d1110)+0x18 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1254]
0012f9ec 023af7d9 chrome_1c30000!MessageLoop::RunTask(struct base::PendingTask * pending_task = 0x0012fa04)+0x211 [c:\b\build\slave\win\build\src\base\message_loop.cc @ 460]
0012fa40 023e40da chrome_1c30000!MessageLoop::DoWork(void)+0x229 [c:\b\build\slave\win\build\src\base\message_loop.cc @ 661]
0012fa70 023e3090 chrome_1c30000!base::MessagePumpForUI::DoRunLoop(void)+0x5a [c:\b\build\slave\win\build\src\base\message_pump_win.cc @ 204]
0012fa90 023aef3e chrome_1c30000!base::MessagePumpWin::RunWithDispatcher(class base::MessagePump::Delegate * delegate = 0x01081b80, class base::MessagePumpWin::Dispatcher * dispatcher = 0x0012fb68)+0x40 [c:\b\build\slave\win\build\src\base\message_pump_win.cc @ 53]
0012fb40 023afca8 chrome_1c30000!MessageLoop::RunInternal(void)+0x8e [c:\b\build\slave\win\build\src\base\message_loop.cc @ 412]
0012fb5c 024fc191 chrome_1c30000!MessageLoopForUI::RunWithDispatcher(class base::MessagePumpWin::Dispatcher * dispatcher = 0x0012fb68)+0x68 [c:\b\build\slave\win\build\src\base\message_loop.cc @ 777]
0012fb8c 01c9cadb chrome_1c30000!ChromeBrowserMainParts::MainMessageLoopRun(int * result_code = 0x01073d4c)+0x31 [c:\b\build\slave\win\build\src\chrome\browser\chrome_browser_main.cc @ 1853]
0012fb98 01cb01a0 chrome_1c30000!content::BrowserMainLoop::RunMainMessageLoopParts(void)+0x2b [c:\b\build\slave\win\build\src\content\browser\browser_main_loop.cc @ 454]
0012fc40 02c0a0ce chrome_1c30000!`anonymous namespace'::BrowserMainRunnerImpl::Run(void)+0xc0 [c:\b\build\slave\win\build\src\content\browser\browser_main_runner.cc @ 95]
0012fc50 0243044e chrome_1c30000!BrowserMain(struct content::MainFunctionParams * parameters = 0x0012fde4)+0x3e [c:\b\build\slave\win\build\src\content\browser\browser_main.cc @ 21]


### ku...@gmail.com (2012-03-19)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/62925?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084884)*
