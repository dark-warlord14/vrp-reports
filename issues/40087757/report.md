# Crash in ContainerNodeAlgorithms.h with outdated ice-tea plugin

| Field | Value |
|-------|-------|
| **Issue ID** | [40087757](https://issues.chromium.org/issues/40087757) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals, Internals>Plugins |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2011-02-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Crashes at  

third\_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h  

-> removeAllChildrenInContainer(GenericNodeContainer\* container)

while executing this line.  

delete n;

**VERSION**  

Chrome Version: [11.0.665.0 (74248)] + [dev (Release/Debug)]  

Operating System: [Ubuntu ,10.04, 32 bit]

**REPRODUCTION CASE**

1. Install out-dated ice-tea java plugin.
2. Open attached crash.html.  
   
   crash.html contains a applet.  
   
   Chrome will show a info bar saying ice-tea java plugin is out-dated.
3. Move the mouse over java applet (Applet is not loaded at this moment, since plugin is outdated).
4. Wait about 3 seconds. crash.html will refresh itself.  
   
   Once the page is refreshed chrome will display a sad tab.

It may be possible to reproduce this with other out-dated plugins as well. I ll post on this issue if I can.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Crash State:

stack trace

#0 0x00000000 in ?? ()  

#1 0x0a013e63 in WebCore::removeAllChildrenInContainer<WebCore::Node, WebCore::ContainerNode> (container=0xc799000)  

at third\_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h:64  

#2 0x0a00fa73 in WebCore::ContainerNode::removeAllChildren (this=0xc799000)  

at third\_party/WebKit/Source/WebCore/dom/ContainerNode.cpp:72  

#3 0x0a01ec3f in WebCore::Document::removedLastRef (this=0xc799000)  

at third\_party/WebKit/Source/WebCore/dom/Document.cpp:534  

#4 0x09ac6185 in WebCore::TreeShared[WebCore::ContainerNode](javascript:void(0);)::deref (  

this=0xc799004)  

at third\_party/WebKit/Source/WebCore/platform/TreeShared.h:79  

#5 0x0a4104e0 in WebCore::DOMDataStore::weakNodeCallback (value=...,  

domObject=0xc799000)  

at third\_party/WebKit/Source/WebCore/bindings/v8/DOMDataStore.cpp:165  

#6 0x092525ef in v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing (this=0xc601284) at v8/src/global-handles.cc:182  

#7 0x092517a8 in v8::internal::GlobalHandles::PostGarbageCollectionProcessing  

() at v8/src/global-handles.cc:387  

#8 0x0925da84 in v8::internal::Heap::PerformGarbageCollection (  

collector=v8::internal::MARK\_COMPACTOR, tracer=0xbfffe068)  

at v8/src/heap.cc:778  

#9 0x0925d2a5 in v8::internal::Heap::CollectGarbage (  

space=v8::internal::OLD\_POINTER\_SPACE,  

#10 0x09217d5a in v8::internal::Heap::CollectGarbage (  

space=v8::internal::OLD\_POINTER\_SPACE) at v8/src/heap-inl.h:412  

#11 0x0925d198 in v8::internal::Heap::CollectAllGarbage (  

force\_compaction=false) at v8/src/heap.cc:451  

#12 0x09264c85 in v8::internal::Heap::IdleNotification ()  

at v8/src/heap.cc:3838  

#13 0x093d8bfb in v8::internal::V8::IdleNotification () at v8/src/v8.cc:240  

#14 0x091ef565 in v8::V8::IdleNotification () at v8/src/api.cc:3340  

#15 0x09f58989 in WebCore::V8GCForContextDispose::pseudoIdleTimerFired (  

this=0xc69f270)  

at third\_party/WebKit/Source/WebCore/bindings/v8/V8GCForContextDispose.cpp:69  

#16 0x09f58a74 in WebCore::Timer[WebCore::V8GCForContextDispose](javascript:void(0);)::fired (  

this=0xc69f270) at third\_party/WebKit/Source/WebCore/platform/Timer.h:99  

#17 0x09eb2d26 in WebCore::ThreadTimers::sharedTimerFiredInternal (  

this=0xc686fe0)  

at third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:112  

#18 0x09eb2c73 in WebCore::ThreadTimers::sharedTimerFired ()  

at third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:90  

#19 0x09764648 in webkit\_glue::WebKitClientImpl::DoTimeout (this=0xc5f5a50)  

at ./webkit/glue/webkitclient\_impl.h:82  

#20 0x09764943 in DispatchToMethod<webkit\_glue::WebKitClientImpl, void (webkit\_glue::WebKitClientImpl::\*)()> (obj=0xc5f5a50,  

method=0x9764626 <webkit\_glue::WebKitClientImpl::DoTimeout()>, arg=...)  

at ./base/tuple.h:541  

#21 0x097648d1 in base::BaseTimer<webkit\_glue::WebKitClientImpl, false>::TimerTask::Run (this=0xc69f480) at ./base/timer.h:160  

#22 0x08caeb37 in MessageLoop::RunTask (this=0xbfffe8b4, task=0xc69f480)  

at base/message\_loop.cc:362  

#23 0x08caebef in MessageLoop::DeferOrRunPendingTask (this=0xbfffe8b4,  

pending\_task=...) at base/message\_loop.cc:371  

#24 0x08caf62b in MessageLoop::DoDelayedWork (this=0xbfffe8b4,  

next\_delayed\_work\_time=0xc62f050) at base/message\_loop.cc:602  

#25 0x08cb540d in base::MessagePumpDefault::Run (this=0xc62f040,  

delegate=0xbfffe8b4) at base/message\_pump\_default.cc:27  

#26 0x08cae9a5 in MessageLoop::RunInternal (this=0xbfffe8b4)  

at base/message\_loop.cc:337  

#27 0x08cae88f in MessageLoop::RunHandler (this=0xbfffe8b4)  

at base/message\_loop.cc:310  

#28 0x08cae353 in MessageLoop::Run (this=0xbfffe8b4)  

at base/message\_loop.cc:234  

#29 0x08b558db in RendererMain (parameters=...)  

at chrome/renderer/renderer\_main.cc:300  

#30 0x08072b37 in RunNamedProcessTypeMain (process\_type=...,  

main\_function\_params=...) at chrome/app/chrome\_main.cc:649  

#31 0x08073538 in ChromeMain (argc=6, argv=0xbffff0a4)  

at chrome/app/chrome\_main.cc:977  

#32 0x0807370d in main (argc=6, argv=0xbffff0a4)  

at chrome/app/chrome\_exe\_main\_gtk.cc:49

registers

eax 0xc7482a0 208962208  

ecx 0x3aa8 15016  

edx 0x0 0  

ebx 0x1 1  

esp 0xbfffdeac 0xbfffdeac  

ebp 0xbfffded8 0xbfffded8  

esi 0x0 0  

edi 0x1 1  

eip 0x0 0  

eflags 0x210206 [ PF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

## Attachments

- [crash.html](attachments/crash.html) (text/html; charset=us-ascii, 1001 B)

## Timeline

### ch...@gmail.com (2011-02-09)

Also have to mention that debug build fails on these assert conditions.
Need to remove these assert checks to get the above mentioned stack trace.

Assert failiures
================

1. ASSERT(!eventDispatchForbidden()) on
   1.1. third_party/WebKit/Source/WebCore/dom/ContainerNode.cpp 
          -> notifyChildInserted(Node* child)
          -> dispatchChildInsertionEvents(Node* child)
          -> dispatchChildRemovalEvents(Node* child)
   1.2. third_party/WebKit/Source/WebCore/dom/Node.cpp 
          -> dispatchGenericEvent(PassRefPtr<Event> prpEvent)
          -> dispatchSubtreeModifiedEvent()
          -> dispatchUIEvent(const AtomicString& eventType, int detail, PassRefPtr<Event> underlyingEvent)
   1.3. third_party/WebKit/Source/WebCore/dom/Element.cpp 
          -> dispatchAttrRemovalEvent(Attribute*)
   1.4. third_party/WebKit/Source/WebCore/dom/EventTarget.cpp 
          -> fireEventListeners(Event* event)

2. ASSERT(!n->m_deletionHasBegun);
   third_party/WebKit/Source/WebCore/dom/ContainerNodeAlgorithms.h
      -> addChildNodesToDeletionQueue(Event* event)

### js...@chromium.org (2011-02-09)

@bauerb - Seems like you would be the best owner? (Assuming this affects m10 as well).

### ba...@chromium.org (2011-02-09)

Looks like the first ASSERT happens when we try to restore the old tooltip while running the event handler that fired on modifying the tooltip in the first place.

I don't think restoring the old tooltip is even necessary, as this method is only called during destruction of the WebPluginContainer, so it shouldn't need the old tooltip.

### sc...@gmail.com (2011-02-09)

Wow, sorry for sucking, Bernhard.
I think this will affect M9, too :-(

### bu...@chromium.org (2011-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=74428

------------------------------------------------------------------------
r74428 | bauerb@chromium.org | Thu Feb 10 04:32:43 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/npapi/webview_plugin.h?r1=74428&r2=74427&pathrev=74428
 M http://src.chromium.org/viewvc/chrome/trunk/src/webkit/plugins/npapi/webview_plugin.cc?r1=74428&r2=74427&pathrev=74428
 M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/renderer/blocked_plugin.cc?r1=74428&r2=74427&pathrev=74428

Restore old title in WebViewPlugin only when loading the plugin.

BUG=72437
TEST=see bug for manual test

Review URL: http://codereview.chromium.org/6476006
------------------------------------------------------------------------

### ba...@chromium.org (2011-02-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-02-10)

Thanks for mopping up my mess Bernhard!

### bu...@chromium.org (2011-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=74434

------------------------------------------------------------------------
r74434 | bauerb@chromium.org | Thu Feb 10 07:40:32 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/648/src/chrome/renderer/blocked_plugin.cc?r1=74434&r2=74433&pathrev=74434
 M http://src.chromium.org/viewvc/chrome/branches/648/src/webkit/plugins/npapi/webview_plugin.cc?r1=74434&r2=74433&pathrev=74434
 M http://src.chromium.org/viewvc/chrome/branches/648/src/webkit/plugins/npapi/webview_plugin.h?r1=74434&r2=74433&pathrev=74434

Merge 74428 - Restore old title in WebViewPlugin only when loading the plugin.

BUG=72437
TEST=see bug for manual test

Review URL: http://codereview.chromium.org/6476006

TBR=bauerb@chromium.org
Review URL: http://codereview.chromium.org/6483014
------------------------------------------------------------------------

### bu...@chromium.org (2011-02-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=74435

------------------------------------------------------------------------
r74435 | bauerb@chromium.org | Thu Feb 10 07:43:45 PST 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/597/src/webkit/glue/plugins/webview_plugin.cc?r1=74435&r2=74434&pathrev=74435
 M http://src.chromium.org/viewvc/chrome/branches/597/src/webkit/glue/plugins/webview_plugin.h?r1=74435&r2=74434&pathrev=74435
 M http://src.chromium.org/viewvc/chrome/branches/597/src/chrome/renderer/blocked_plugin.cc?r1=74435&r2=74434&pathrev=74435

Merge 74428 - Restore old title in WebViewPlugin only when loading the plugin.

BUG=72437
TEST=see bug for manual test

Original review URL: http://codereview.chromium.org/6476006

Review URL: http://codereview.chromium.org/6480034
------------------------------------------------------------------------

### in...@chromium.org (2011-02-10)

Thanks for merging to 597, 648.

### sc...@gmail.com (2011-02-13)

@chamal.desilva: thanks for finding and reporting this bug!
And congrats -- we'd like to offer you a provisional $1000 Chromium Security Reward.

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

### ch...@gmail.com (2011-02-13)

It is wonderful. Thanks a lot :)

### ba...@chromium.org (2011-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2011-02-17)

I don't see the renderer crash anymore with Google Chrome 10.0.648.82 (Official Build 75062) on windows and linux.

### [Deleted User] (2011-02-18)

With Google Chrome 9.0.597.107 (Official Build 75357) on Windows , I don't see any crash. But on Linux loading the testcase crashes the plugin continuously. It crashes so fast that I don't see the plugin crash infobar.

Stack Trace
------------
Thread 0 *CRASHED* ( SIGABRT @ 0xdf1e00000ce4 )

0x7fd6f2b6aa75	 [libc-2.11.1.so	 - ../nptl/sysdeps/unix/sysv/linux/raise.c:64]	raise
0x7fd6f2b6e5bf	 [libc-2.11.1.so	 - abort.c:92]	abort
0x7fd6f2b63940	 [libc-2.11.1.so	 - assert.c:81]	__assert_fail
0x7fd6f8ef2e76	 [libnpjp2.so	 + 0x00005e76]	
0x7fd6ef74b7ad	 [libavahi-client.so.3.2.5	 + 0x000027ad]	
0x7fd6f8e6495c	 [ld-2.11.1.so	 + 0x0000c95c]	
0x7fd6f8e668c5	 [ld-2.11.1.so	 + 0x0000e8c5]	
0x7fd6f8e6491f	 [ld-2.11.1.so	 + 0x0000c91f]

Full report @ http://crash/reportdetail?reportid=ae1a8b802986aed4

### sc...@gmail.com (2011-02-21)

@sunandt: I don't think the failure to load the plug-in at all is related to this particular fix? i.e. I don't think this fix causes a regression?

FWIW, both the Java and IcedTea plug-ins load OK for me, 64-bit Linux, with a build of 9.0.597.107.

I'm just making sure there's nothing here that might hold up the patch. Please advise.


### [Deleted User] (2011-02-23)

@scarybeasts: I see the same behavior with 9.0.597.98 and 9.0.597.107. When I load the testcase with old Java plugin(1.6.0_16), plugin crashes continuously. But with latest Java plugin(1.6.0_23), we are not crashing. If you think this is a different issue and since we are doing fine with the latest java plugin, we can ignore this unless you want to get that fixed as well. If you want this to be fixed as well, I can log a new bug.

### sc...@gmail.com (2011-02-23)

@sunandt: thanks for the details. This certainly isn't a regression then, so 9.0.597.107 is on track!!

I don't think we need to track the old plug-in version crash. As of Chrome 10 (i.e. very soon), we basically shepherd people towards installing an uptodate and less vulnerable Java. 1.6.0_16 is irrelevant in that world.

### sc...@gmail.com (2011-03-04)

Invoice finalized; payment is in e-payment system.

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/72437?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>Plugins]
[Monorail mergedwith: crbug.com/chromium/72361]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087757)*
