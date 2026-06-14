# Crash when closing chrome - BalloonViewImpl::DelayedClose

| Field | Value |
|-------|-------|
| **Issue ID** | [40082405](https://issues.chromium.org/issues/40082405) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | do...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-07-28 |
| **Bounty** | $1,337.00 |

## Description

Chrome Version : 6.0.472.0 (Official Build 53024) dev

**What steps will reproduce the problem?**

1. Close Chrome

**What is the expected result?**  

It should not crash

**What happens instead?**  

It crash

**Please provide any additional information below. Attach a screenshot if**  

**possible.**  

Crash id: 14d45f6a91589d25

## Timeline

### th...@chromium.org (2010-07-28)

There's no stack trace in the crash dump, unfortunately. Can you reproduce this every time?

### do...@gmail.com (2010-07-29)

it occured again just now. crash id: 23aaef67ab57da3b

it's not happens every time. it happens sometimes. before i reported, it was occured a few more times at different times.

### [Deleted User] (2010-07-29)

Thanks for the report. If you could find repro steps, that would be great. What exactly were you doing before closing Chrome? Post your comments in https://crbug.com/chromium/46018.

### js...@chromium.org (2010-08-03)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2010-08-03)

This is not a duplicate.  This is a crash at browser shutdown, which is a different path than the other bug.

### [Deleted User] (2010-08-03)

[Empty comment from Monorail migration]

### do...@gmail.com (2010-08-03)

new crash id: b200a9209eb9ba43

### hu...@chromium.org (2010-08-03)

23aaef67ab57da3b and b200a9209eb9ba43 are the crash on BalloonViewImpl::DelayedClose. updated title.

### js...@chromium.org (2010-08-03)

Marking as critical severity because this could be used fo code execution outside the sandbox. The reproduction from https://crbug.com/chromium/50386 is as follows:

javascript:webkitNotifications.createNotification().show();close();

@johnnyg - you mentioned that you think you have this bug worked out?


### js...@chromium.org (2010-08-03)

Updating priority and milestone to reflect severity.


### [Deleted User] (2010-08-03)

all these new crash ids being attached to the bug have nothing to do with browser shutdown.  There is a real crash at browser shutdown, with this stack

0019f21c 63ac9ba5 0019f250 01449550 00000000 chrome_63550000!MessageLoop::PostTask_Helper+0xd8 (FPO: [5,44,0]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\base\message_loop.cc @ 350]
0019f234 63f3cae9 0019f250 01449550 01450240 chrome_63550000!MessageLoop::PostTask+0x15 (FPO: [2,0,0]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\base\message_loop.cc @ 300]
0019f258 63f3ba12 01450240 01450240 00000000 chrome_63550000!IPC::ChannelProxy::Send+0x69 (FPO: [1,3,4]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\ipc\ipc_channel_proxy.cc @ 282]
0019f308 63f3992e 01450240 ffffffff 6376244e chrome_63550000!IPC::SyncChannel::SendWithTimeout+0x32 (FPO: [2,40,0]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\ipc\ipc_sync_channel.cc @ 386]
0019f314 6376244e 01450240 037b7244 05fc3b60 chrome_63550000!IPC::SyncChannel::Send+0xe (FPO: [1,0,0]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\ipc\ipc_sync_channel.cc @ 382]
0019f3b8 63957581 05fc3b60 6395807c 037b7240 chrome_63550000!RenderWidgetHost::Shutdown+0x5e (FPO: [0,36,4]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\chrome\browser\renderer_host\render_widget_host.cc @ 128]
0019f3c0 6395807c 037b7240 63877ceb 00000001 chrome_63550000!BalloonHost::Shutdown+0x11 (FPO: [0,0,4]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\chrome\browser\notifications\balloon_host.cc @ 45]
0019f3c8 63877ceb 00000001 00000001 037b7240 chrome_63550000!BalloonViewHost::`scalar deleting destructor'+0x1c (FPO: [1,0,4]) (CONV: thiscall)
0019f3dc 63878048 05efc640 638777b8 00000001 chrome_63550000!BalloonViewImpl::~BalloonViewImpl+0xab (FPO: [0,0,4]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\chrome\browser\views\notifications\balloon_view.cc @ 114]
0019f3e4 638777b8 00000001 02a524bc 646885a1 chrome_63550000!BalloonViewImpl::`scalar deleting destructor'+0x8 (FPO: [1,0,4]) (CONV: thiscall)
0019f3f0 646885a1 00000001 02aae570 00000000 chrome_63550000!Balloon::`scalar deleting destructor'+0x18 (FPO: [1,0,4]) (CONV: thiscall)
0019f400 638791a5 02aae570 00000001 02aae570 chrome_63550000!STLDeleteContainerPointers<std::_Deque_iterator<CallbackRunner<Tuple1<media::Buffer *> > *,std::allocator<CallbackRunner<Tuple1<media::Buffer *> > *>,1> >+0x71 (FPO: [4,2,0]) (CONV: cdecl) [c:\b\slave\chromium-rel-xp\build\src\base\stl_util-inl.h @ 65]
0019f42c 63879278 0144be78 6361750b 00000001 chrome_63550000!BalloonCollectionImpl::~BalloonCollectionImpl+0x55 (FPO: [0,2,0]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\chrome\browser\notifications\balloon_collection.cc @ 48]
0019f434 6361750b 00000001 0144be70 00000000 chrome_63550000!BalloonCollectionImpl::`scalar deleting destructor'+0x8 (FPO: [1,0,4]) (CONV: thiscall)
0019f44c 63617698 01400280 6357eada 00000001 chrome_63550000!NotificationUIManager::~NotificationUIManager+0x7b (FPO: [0,2,0]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\chrome\browser\notifications\notification_ui_manager.cc @ 45]
0019f454 6357eada 00000001 02a35000 01400280 chrome_63550000!NotificationUIManager::`scalar deleting destructor'+0x8 (FPO: [1,0,4]) (CONV: thiscall)
0019f490 6357f168 013f8150 63592168 00000001 chrome_63550000!BrowserProcessImpl::~BrowserProcessImpl+0x36a (FPO: [0,10,4]) (CONV: thiscall) [c:\b\slave\chromium-rel-xp\build\src\chrome\browser\browser_process_impl.cc @ 210]
0019f498 63592168 00000001 0019fa01 013f8230 chrome_63550000!BrowserProcessImpl::`scalar deleting destructor'+0x8 (FPO: [1,0,4]) (CONV: thiscall)
0019f5c8 63574264 013fb440 ffffffff 00000000 chrome_63550000!browser_shutdown::Shutdown+0x198 (FPO: [0,70,0]) (CONV: cdecl) [c:\b\slave\chromium-rel-xp\build\src\chrome\browser\browser_shutdown.cc @ 150]
0019fa6c 6355910b 0019fab4 63558620 015317c8 chrome_63550000!BrowserMain+0x1ab4 (FPO: [1,292,0]) (CONV: cdecl) [c:\b\slave\chromium-rel-xp\build\src\chrome\browser\browser_main.cc @ 1312]

and it is fixed by http://src.chromium.org/viewvc/chrome?view=rev&revision=54713

https://crbug.com/chromium/50386 that repros on closing a notification, and the crash on BalloonViewImpl::DelayedClose are different bugs which I am still investigating.

### bu...@gmail.com (2010-08-04)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=54713 

------------------------------------------------------------------------
r54713 | johnnyg@chromium.org | 2010-08-03 00:04:07 -0700 (Tue, 03 Aug 2010) | 6 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/browser_process_impl.cc?r1=54713&r2=54712

Shutdown the notification UI manager before the notifications service, as the former's shutdown logic depends on the latter.

BUG=50553
TEST=see bug

Review URL: http://codereview.chromium.org/3051029
------------------------------------------------------------------------


### in...@chromium.org (2010-08-04)

Needs to be merged to 375 and 472.

### js...@chromium.org (2010-08-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-04)

Still getting a crash with the javascript URL above. The MessageLoop this pointer at the top of the stack appears to be stale:

base::TimeTicks::is_null()  Line 464
MessageLoop::PostTask_Helper(const tracked_objects::Location & from_here={...}, Task * task=0x04ea4e40, __int64 delay_ms=0, bool nestable=true)  Line 350
MessageLoop::PostTask(const tracked_objects::Location & from_here={...}, Task * task=0x04ea4e40)  Line 300
IPC::ChannelProxy::Send(IPC::Message * message=class=16, index=7)  Line 283
IPC::SyncChannel::SendWithTimeout(IPC::Message * message=class=16, index=7, int timeout_ms=-1)  Line 387
IPC::SyncChannel::Send(IPC::Message * message=class=16, index=7)  Line 381
BrowserRenderProcessHost::Send(IPC::Message * msg=class=16, index=7)  Line 796
RenderWidgetHost::Send(IPC::Message * msg=class=16, index=7)  Line 188
RenderWidgetHost::Shutdown()  Line 128
RenderViewHost::Shutdown()  Line 866
BalloonHost::Shutdown()  Line 44
BalloonViewHost::~BalloonViewHost()  Line 22
BalloonViewHost::`scalar deleting destructor'() 
scoped_ptr<BalloonViewHost>::~scoped_ptr<BalloonViewHost>()  Line 75
BalloonViewImpl::~BalloonViewImpl()  Line 114
BalloonViewImpl::`scalar deleting destructor'() 
scoped_ptr<BalloonView>::~scoped_ptr<BalloonView>()  Line 75
Balloon::~Balloon()  Line 21
Balloon::`scalar deleting destructor'() 
STLDeleteContainerPointers<std::_Deque_iterator<Balloon *,std::allocator<Balloon *>,1> >(std::_Deque_iterator<Balloon *,std::allocator<Balloon *>,1> begin=<end>, std::_Deque_iterator<Balloon *,std::allocator<Balloon *>,1> end=<end>)  Line 65
STLDeleteElements<std::deque<Balloon *,std::allocator<Balloon *> > >(std::deque<Balloon *,std::allocator<Balloon *> > * container=[1](0x04d2f500 {profile_=0x00f5d000 notification_={origin_url_={...} content_url_={...} display_source_="" ...} collection_=0x04cb6aa0 ...}))  Line 231
BalloonCollectionImpl::~BalloonCollectionImpl()  Line 48
BalloonCollectionImpl::`scalar deleting destructor'() 
scoped_ptr<BalloonCollection>::~scoped_ptr<BalloonCollection>()  Line 75
NotificationUIManager::~NotificationUIManager()  Line 45
NotificationUIManager::`scalar deleting destructor'() 
scoped_ptr<NotificationUIManager>::reset(NotificationUIManager * p=0x00000000)  Line 84


### js...@chromium.org (2010-08-04)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-08-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55016 

------------------------------------------------------------------------
r55016 | johnnyg@chromium.org | 2010-08-04 19:04:13 -0700 (Wed, 04 Aug 2010) | 5 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/browser_process_impl.cc?r1=55016&r2=55015

Reset the notification ui manager even earlier, before the IO thread goes away.

BUG=50553
TEST=see bug
Review URL: http://codereview.chromium.org/2819092
------------------------------------------------------------------------


### js...@chromium.org (2010-08-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-06)

NOTE - this bug is being used to track a critical issue that was first reported to us by Serg Glazunov in 50386. Any reward nominations tagged on this bug apply to Serg's discovery in 50386.

### sc...@gmail.com (2010-08-06)

@Serg.Glazunov: congrats! We've decided to reward the browser crash at the $1337 level. We were prevented from going higher by the user interaction element as well as the challenge of preparing browser address space for an event at shutdown.

### bu...@gmail.com (2010-08-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55423 

------------------------------------------------------------------------
r55423 | inferno@chromium.org | 2010-08-09 11:19:15 -0700 (Mon, 09 Aug 2010) | 8 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/472/src/chrome/browser/browser_process_impl.cc?r1=55423&r2=55422

Merge 54713 - Shutdown the notification UI manager before the notifications service, as the former's shutdown logic depends on the latter.

BUG=50553
TEST=see bug

Review URL: http://codereview.chromium.org/3051029

Review URL: http://codereview.chromium.org/3091018
------------------------------------------------------------------------


### bu...@gmail.com (2010-08-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55424 

------------------------------------------------------------------------
r55424 | inferno@chromium.org | 2010-08-09 11:20:46 -0700 (Mon, 09 Aug 2010) | 7 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/472/src/chrome/browser/browser_process_impl.cc?r1=55424&r2=55423

Merge 55016 - Reset the notification ui manager even earlier, before the IO thread goes away.

BUG=50553
TEST=see bug
Review URL: http://codereview.chromium.org/2819092

Review URL: http://codereview.chromium.org/3028052
------------------------------------------------------------------------


### bu...@gmail.com (2010-08-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55469 

------------------------------------------------------------------------
r55469 | cdn@chromium.org | 2010-08-09 13:58:35 -0700 (Mon, 09 Aug 2010) | 8 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/375/src/chrome/browser/browser_process_impl.cc?r1=55469&r2=55468

Merge 54713 - Shutdown the notification UI manager before the notifications service, as the former's shutdown logic depends on the latter.

BUG=50553
TEST=see bug

Review URL: http://codereview.chromium.org/3051029

Review URL: http://codereview.chromium.org/3112001
------------------------------------------------------------------------


### bu...@gmail.com (2010-08-09)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55470 

------------------------------------------------------------------------
r55470 | cdn@chromium.org | 2010-08-09 14:01:04 -0700 (Mon, 09 Aug 2010) | 7 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/375/src/chrome/browser/browser_process_impl.cc?r1=55470&r2=55469

Merge 55016 - Reset the notification ui manager even earlier, before the IO thread goes away.

BUG=50553
TEST=see bug
Review URL: http://codereview.chromium.org/2819092

Review URL: http://codereview.chromium.org/3114001
------------------------------------------------------------------------


### ch...@gmail.com (2010-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2010-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2010-08-18)

Works fine with Google Chrome 5.0.375.127 (Official Build 55887) on Win XP and Linux Ubuntu9.04

### [Deleted User] (2010-08-18)

Works fine on mac.
5.0.375.127

### sc...@gmail.com (2010-08-25)

Payment is in the electronic system.

### do...@gmail.com (2010-09-13)

https://crbug.com/chromium/55415

### la...@chromium.org (2011-03-19)

Chrome Version : 6.0.472.0 (Official Build 53024) dev

**What steps will reproduce the problem?**

1. Close Chrome

**What is the expected result?**  

It should not crash

**What happens instead?**  

It crash

**Please provide any additional information below. Attach a screenshot if**  

**possible.**  

Crash id: 14d45f6a91589d25

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### [Deleted User] (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-11-03)

This issue was migrated from crbug.com/chromium/50553?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082405)*
