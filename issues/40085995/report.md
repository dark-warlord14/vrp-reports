# Onbeforeunload use after free

| Field | Value |
|-------|-------|
| **Issue ID** | [40085995](https://issues.chromium.org/issues/40085995) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Windows |
| **Reporter** | wa...@gmail.com |
| **Assignee** | lf...@chromium.org |
| **Created** | 2016-11-18 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36

Steps to reproduce the problem:
1- open http://localhost/testcase.html
2- click "click here" then "then here" buttons
3- write something in the URL bar (of the tab containing testcase.html) then press enter. If the navigation occurs, go to step 4. If the print dialog is displayed, go to step 1
4- close the tab that has just navigated (this step isn't necessary but increases the likelihood of seeing a crash)
5- close the tab containing "helper2.html" or wait for it to close by itself
6- the renderer process hosting "helper2.html" crashes sometimes (see crash example.txt)

What is the expected behavior?
No crashes should occur.

What went wrong?
On closing helper2.html, content::RenderFrameImpl::OnBeforeUnload is executed even though it shouldn't. 
It seems like this function is using freed memory.

Did this work before? N/A 

Chrome version: 54.0.2840.59  Channel: n/a
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 23.0 r0

This poc can be done with less user interaction.

## Attachments

- [testcase.zip](attachments/testcase.zip) (application/octet-stream, 4.8 KB)
- [UAF-onbeforeunload.zip](attachments/UAF-onbeforeunload.zip) (application/octet-stream, 2.7 KB)

## Timeline

### me...@chromium.org (2016-11-18)

Thanks for the report. Do you have a stack trace that you can attach to the bug?

### wa...@gmail.com (2016-11-18)

Hi, there is a stack trace in crash example.txt

### me...@chromium.org (2016-11-18)

Sorry, I missed it.

changwan: Could you please take a look or reassign as appropriate? Thanks.

[Monorail components: UI>Browser>Navigation]

### sh...@chromium.org (2016-11-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-19)

[Empty comment from Monorail migration]

### ch...@chromium.org (2016-11-21)

Sorry, unassigning myself as I'm not an expert in this domain. I have no idea how OnBeforeUnload can be called after the object (could it be frame_?) gets freed. Could be related to the recent refactoring around frame detachment, but not sure. cc'ing nasko@ just in case.

### ke...@chromium.org (2016-11-21)

I see creis@ in a TODO in the function. creis@ can you own this or do you know who it can be assigned to? Thanks.

### cr...@chromium.org (2016-11-21)

+lfg, dcheng for frame detach knowledge.

We'll need to catch this in a debugger to see what's being used after free in RenderFrameImpl::OnBeforeUnload.  I agree that frame_ seems like the likely candidate.  It would be concerning if we're routing IPCs to a RenderFrameImpl after the underlying frame_ has been deleted.

I likely won't have time to debug this until tomorrow, so others are free to grab it first.  If not, I'll look when I get a moment.

### lf...@chromium.org (2016-11-21)

I'll take a look.

### lf...@chromium.org (2016-11-21)

I've reproed on canary, crash id 10476d6f00000000.

Looking at the crash dump, it seems that the RenderFrameImpl itself is deleted while executing the unload callback. I'll confirm and send a patch to fix the UaF.


### lf...@chromium.org (2016-11-21)

What happens is that there is a window.print() in the beforeunload handler, which causes a sync IPC to be sent and it runs a nested message loop while waiting. The frame is then detached in this nested message loop, and when coming back to OnBeforeUnload it is already destroyed.

Adding thestig@ for printing.

I can easily fix this specific UaF by not doing a virtual call in OnBeforeUnload, but I'm wondering if there are other implications that could come out of the nested message loop in the print preview.

Here's the callstack for the frame destruction:

>	chrome_child.dll!content::RenderFrameImpl::frameDetached(blink::WebLocalFrame * frame, blink::WebFrameClient::DetachType type) Line 3014	C++
 	chrome_child.dll!blink::FrameLoaderClientImpl::detached(blink::FrameDetachType type) Line 355	C++
 	chrome_child.dll!blink::Frame::detach(blink::FrameDetachType type) Line 77	C++
 	chrome_child.dll!blink::LocalFrame::detach(blink::FrameDetachType type) Line 445	C++
 	chrome_child.dll!blink::WebFrame::swap(blink::WebFrame * frame) Line 86	C++
 	chrome_child.dll!content::RenderFrameImpl::OnSwapOut(int proxy_routing_id, bool is_loading, const content::FrameReplicationState & replicated_frame_state) Line 1720	C++
 	chrome_child.dll!IPC::MessageT<FrameMsg_SwapOut_Meta,std::tuple<int,bool,content::FrameReplicationState>,void>::Dispatch<content::RenderFrameImpl,content::RenderFrameImpl,void,void (__cdecl content::RenderFrameImpl::*)(int,bool,content::FrameReplicationState const & __ptr64) __ptr64>(const IPC::Message * msg, content::RenderFrameImpl * obj, content::RenderFrameImpl * func, void *) Line 121	C++
 	chrome_child.dll!content::RenderFrameImpl::OnMessageReceived(const IPC::Message & msg) Line 1496	C++
 	chrome_child.dll!IPC::MessageRouter::RouteMessage(const IPC::Message & msg) Line 57	C++
 	chrome_child.dll!content::ChildThreadImpl::OnMessageReceived(const IPC::Message & msg) Line 796	C++
 	chrome_child.dll!IPC::ChannelProxy::Context::OnDispatchMessage(const IPC::Message & message) Line 341	C++
 	chrome_child.dll!base::debug::TaskAnnotator::RunTask(const char * queue_function, base::PendingTask * pending_task) Line 52	C++
 	chrome_child.dll!blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue(blink::scheduler::internal::WorkQueue * work_queue) Line 361	C++
 	chrome_child.dll!blink::scheduler::TaskQueueManager::DoWork(base::TimeTicks run_time, bool from_main_thread) Line 250	C++
 	chrome_child.dll!base::internal::Invoker<base::internal::BindState<void (__cdecl blink::scheduler::TaskQueueManager::*)(base::TimeTicks,bool) __ptr64,base::WeakPtr<blink::scheduler::TaskQueueManager>,base::TimeTicks,bool>,void __cdecl(void)>::Run(base::internal::BindStateBase * base) Line 343	C++
 	chrome_child.dll!base::debug::TaskAnnotator::RunTask(const char * queue_function, base::PendingTask * pending_task) Line 52	C++
 	chrome_child.dll!base::MessageLoop::RunTask(base::PendingTask * pending_task) Line 414	C++
 	chrome_child.dll!base::MessageLoop::DoWork() Line 515	C++
 	chrome_child.dll!base::MessagePumpDefault::Run(base::MessagePump::Delegate * delegate) Line 36	C++
 	chrome_child.dll!base::RunLoop::Run() Line 36	C++
 	chrome_child.dll!IPC::SyncChannel::WaitForReplyWithNestedMessageLoop(IPC::SyncChannel::SyncContext * context) Line 673	C++
 	chrome_child.dll!IPC::SyncChannel::WaitForReply(mojo::SyncHandleRegistry * registry, IPC::SyncChannel::SyncContext * context, bool pump_messages) Line 638	C++
 	chrome_child.dll!IPC::SyncChannel::Send(IPC::Message * message) Line 586	C++
 	chrome_child.dll!content::RenderThreadImpl::Send(IPC::Message * msg) Line 1058	C++
 	chrome_child.dll!printing::PrintWebViewHelper::RequestPrintPreview(printing::PrintWebViewHelper::PrintPreviewRequestType type) Line 1950	C++
 	chrome_child.dll!printing::PrintWebViewHelper::ScriptedPrint(bool user_initiated) Line 968	C++
 	chrome_child.dll!content::RenderViewImpl::printPage(blink::WebLocalFrame * frame) Line 1507	C++
 	chrome_child.dll!blink::ChromeClientImpl::printDelegate(blink::LocalFrame * frame) Line 685	C++
 	chrome_child.dll!blink::ChromeClient::print(blink::LocalFrame * frame) Line 218	C++
 	chrome_child.dll!blink::LocalDOMWindow::print(blink::ScriptState * scriptState) Line 724	C++
 	chrome_child.dll!blink::DOMWindowV8Internal::printMethod(const v8::FunctionCallbackInfo<v8::Value> & info) Line 4351	C++
 	chrome_child.dll!v8::internal::FunctionCallbackArguments::Call(void(*)(const v8::FunctionCallbackInfo<v8::Value> &) f) Line 20	C++
 	chrome_child.dll!v8::internal::`anonymous namespace'::HandleApiCallHelper<0>(v8::internal::Isolate * isolate, v8::internal::Handle<v8::internal::HeapObject> function, v8::internal::Handle<v8::internal::HeapObject> new_target, v8::internal::Handle<v8::internal::FunctionTemplateInfo> fun_data, v8::internal::Handle<v8::internal::Object> receiver, v8::internal::BuiltinArguments args) Line 108	C++
 	chrome_child.dll!v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments args, v8::internal::Isolate * isolate) Line 135	C++
 	chrome_child.dll!v8::internal::Builtin_HandleApiCall(int args_length, v8::internal::Object * * args_object, v8::internal::Isolate * isolate) Line 123	C++


### cr...@chromium.org (2016-11-21)

Thanks for starting the fix!  (https://codereview.chromium.org/2514323003/)

We'll probably want to land that, though I wonder if we should be preventing print() during beforeunload/unload the way we do for navigations.  Nested message loops seem like they could really mess things up in those cases, and it's not clear that we should be printing there.

Quite interestingly, we already don't seem to support print() during unload for same-process navigations, though we do try to do it for cross-process navigations (in which case the print dialog is displayed over the *new* page after commit, and it never finds anything to print).  I'm not sure why we would allow it for cross-process but not same-process.

### th...@chromium.org (2016-11-21)

BTW, is https://crbug.com/chromium/666616 the same problem? The stack traces look similar.

### cr...@chromium.org (2016-11-22)

thestig: Yes, that looks very similar, but I don't think lfg's proposed fix will handle that.  That one is a UaF in PrintWebViewHelper (setting  is_scripted_preview_delayed_ to false after the frame and helper are deleted during the nested message loop) rather than in RenderFrameImpl.  Not sure why we didn't hit that one in these repro steps.

thestig/lfg: Do either of you see a way to avoid that UaF without the bigger change of disallowing print during beforeunload/unload?

### lf...@chromium.org (2016-11-22)

The UaF in https://crbug.com/chromium/666616 does not involve the unload/beforeunload handlers, so disallowing print during those won't fix it.

How complicated would it be to redesign the print dialog so it doesn't need a nested message loop?


### th...@chromium.org (2016-11-22)

The nested message loops is only for window.print(). We discussed duplicating the frame in https://crbug.com/chromium/21555 but at the time decided it was too hard to do. There's also https://crbug.com/chromium/629432 on this topic.

### bu...@chromium.org (2016-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0dd441a0007aa46917779e782ee9094f111a02b3

commit 0dd441a0007aa46917779e782ee9094f111a02b3
Author: lfg <lfg@chromium.org>
Date: Wed Nov 23 19:43:40 2016

Fix UaF in RenderFrameImpl::OnBeforeUnload.

BUG=666714

Review-Url: https://codereview.chromium.org/2514323003
Cr-Commit-Position: refs/heads/master@{#434226}

[modify] https://crrev.com/0dd441a0007aa46917779e782ee9094f111a02b3/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/0dd441a0007aa46917779e782ee9094f111a02b3/content/renderer/render_view_browsertest.cc


### lf...@chromium.org (2016-11-30)

Confirmed this is fixed on the latest canary, requesting merge.

### lf...@chromium.org (2016-11-30)

Also requesting merge to M55.

### di...@chromium.org (2016-11-30)

[Automated comment] Less than 2 weeks to go before stable on M55, manual review required.

### di...@chromium.org (2016-11-30)

Your change meets the bar and is auto-approved for M56 (branch: 2924)

### sh...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/638b5943f7d8c4b64e38c6f65796d7c4d77ee1db

commit 638b5943f7d8c4b64e38c6f65796d7c4d77ee1db
Author: lfg <lfg@chromium.org>
Date: Wed Nov 30 16:52:25 2016

Fix UaF in RenderFrameImpl::OnBeforeUnload.

BUG=666714

Review-Url: https://codereview.chromium.org/2514323003
Cr-Commit-Position: refs/heads/master@{#434226}
(cherry picked from commit 0dd441a0007aa46917779e782ee9094f111a02b3)

TBR=creis@chromium.org,thestig@chromium.org
NOTRY=true
NOPRESUBMIT=true

Review-Url: https://codereview.chromium.org/2541073002
Cr-Commit-Position: refs/branch-heads/2924@{#187}
Cr-Branched-From: 3a87aecc31cd1ffe751dd72c04e5a96a1fc8108a-refs/heads/master@{#433059}

[modify] https://crrev.com/638b5943f7d8c4b64e38c6f65796d7c4d77ee1db/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/638b5943f7d8c4b64e38c6f65796d7c4d77ee1db/content/renderer/render_view_browsertest.cc


### lf...@chromium.org (2016-11-30)

+awhalley@

Merged to M56, waiting on review for M55 merge.


### aw...@chromium.org (2016-11-30)

This has just missed early stable, but we should take this for the main stable release next week, which will also give it some more time to bake in dev.

### aw...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

I'm afraid the panel declined to reward for this bug, given the difficulty of exploitation and the amount of user interaction involved.

### wa...@gmail.com (2016-12-02)

The only user interaction needed by the user is writing anything in the URL in step 3.
As for the exploitation part, helper2.html has the possibility of spraying the heap as much as it wants after the free, before triggering the use.

### wa...@gmail.com (2016-12-03)

Step 3 doesn't even need user interaction:

It is possible to do a cross process navigation automatically using Javascript navigation to "https://chrome.google.com/webstore/category/extensions?hl=fr" (location="https://chrome.google.com/webstore/category/extensions?hl=fr")

### wa...@gmail.com (2016-12-09)

Hi,this is a way to reduce most user interactions:

1-Open http://localhost/UAF.html
2-click "click here" then "then here" buttons (this step is to bypass the popup blocker)
3-click "OK" in the alert box
4-wait for all localhost pages to close (the wait can be made as short as the attacker wants)


The process hosting http://localhost will trigger a Use After Free (in content::RenderFrameImpl::OnBeforeUnload).

Given that user interaction is now minimal, maybe this bug will get a higher security severity?


### aw...@chromium.org (2017-01-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-12)

Congratulations! The panel decided to reward $2,000 for this bug!

### aw...@chromium.org (2017-01-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/666714?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/674938]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085995)*
