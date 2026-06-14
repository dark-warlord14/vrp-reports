# UrlRequestContext can be deleted while a live SocketStream has a pointer to it (vtable UAF)

| Field | Value |
|-------|-------|
| **Issue ID** | [40077608](https://issues.chromium.org/issues/40077608) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>Network>WebSockets, Blink>Workers |
| **Reporter** | ri...@chromium.org |
| **Assignee** | yh...@chromium.org |
| **Created** | 2013-05-29 |
| **Bounty** | $3,133.00 |

## Description

When SocketStream::Connect() is called, it defers most of the work to DoBeforeConnect(), which is called via a task posted to the MessageLoop. However, the UrlRequestContext object used by DoBeforeConnect() can be deleted (via destruction of ProfileIOData) in-between these two calls.

## Attachments

- [asan-log.txt](attachments/asan-log.txt) (text/plain; charset=us-ascii, 8.7 KB)
- [shorter.html](attachments/shorter.html) (text/plain; charset=us-ascii, 344 B)

## Timeline

### ri...@chromium.org (2013-05-29)

[Empty comment from Monorail migration]

### ri...@chromium.org (2013-05-30)

Progress report: modifying SocketStream::DetachDelegate() so that it prevents SocketStream::DoBeforeConnect()	from being run does not fix the problem.

Adding logging has demonstrated that the WebWorker thread continues to create new WebSocket connections long after the incognito window has closed (see the 242762_WebSocket_browser_crash_repro.html file from https://crbug.com/chromium/242762). When the incognito profile is eventually deleted, many SocketStream objects still exist with a pointer to the dead UrlRequestContext.

If the SocketStreamHostDispatcher object for the WebWorker was destroyed before OffTheRecordProfileData then the crash could be averted, but I have not found a way to do that yet.

### me...@chromium.org (2013-05-30)

I think this will result in use-after-frees and not directly to code execution, so we can assign this high severity rather than critical per severity guidelines: https://sites.google.com/a/chromium.org/dev/developers/severity-guidelines

### ri...@chromium.org (2013-05-30)

The use-after-free is happening in a vtable look up, so while it's not direct code execution it's only a step or two removed. If I had a way of heap-spraying the browser I could probably exploit it a lot easier than I can fix it.

### ri...@chromium.org (2013-05-31)

Added Cr-Blink-Workers as this seems to be caused by a WebWorker outliving its renderer.

### ri...@chromium.org (2013-05-31)

After trying three different naive approaches, none of which fixed the problem, yhirano@chromium.org provided the insight needed to use weak pointers to prevent the use-after-free. The critical insight being that I could just move the weak pointer functionality from ChromeUrlRequestContext up to the base class UrlRequestContext.

So, this works. With this patch applied, you get a probably-harmless zero-page SEGV in the Worker process rather than a UAF in the browser process. Like all the best security patches, it changes a major API and touches files all over the tree.

https://codereview.chromium.org/15736021/

I am going on holiday for a week, so if you decide to actually pursue this approach, I suggest you work on a clone of that CL.

My recommendation would still be to track down someone with a deep understanding of WebWorker lifecycles and force them to fix the underlying problem.

### jl...@chromium.org (2013-05-31)

Adam, thanks a lot for your hard work on this issue!

I'll see if I can find a Blink expert to take a look.

### jl...@chromium.org (2013-05-31)

Dmitry, you have been denounced as the WebWorker expert. Would you mind taking a look at this "High" security bug?

### me...@google.com (2013-06-04)

This is in the browser process so it's in fact critical then? Sorry for setting "high severity" for this Adam, you were right!

### jl...@chromium.org (2013-06-04)

tyoshino@ or yhirano@: could you take Adam's CL over, so that we can quickly commit a fix, even if it isn't the best long-term one ?

Dmitry: could you take a look at the WebWorker lifecycle concern?

### yh...@chromium.org (2013-06-04)

I have copied the CL to https://codereview.chromium.org/16136006/ .


### cb...@chromium.org (2013-06-04)

Is this actually exploitable?

Does the UAF in the browser process require the user to take action to delete an URLRequestContext?

Thanks for looking at this.

### in...@chromium.org (2013-06-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-06-04)

Please note that critical severity security bug needs immediate attention, can any of the cced folks take ownership of this.

### in...@chromium.org (2013-06-04)

[Empty comment from Monorail migration]

### jl...@chromium.org (2013-06-04)

Will: do you think we could land the existing WeakPtr-using fix as a temporary workaround, with a clear TODO to remove it ?

Unless someone has an idea of how to fix this bug without deep changes to workers?

### wi...@chromium.org (2013-06-04)

Adding mmenke@ as I'm mostly trying to hand over ownership of that code and just advise as needed. Matt, please make the call, here's my advice though.

Security trumps maintainability here, and if the security folks say this is a serious bug and if this WeakPtr workaround will fix it, I encourage you to approve the changelist.

jln: as a clarification, this only happens on URLRequestContext deletion where WebSockets are exposed. We don't delete normal profiles unless process shutdown. I'm unclear how much that affects the severity, since once you're executing arbitrary code, it could obviously be very dangerous. Incognito profiles on the other hand will be deleted when all referencing incognito windows have gone away, and that could result in URLRequestContext deletion and a UAF. My hunch is that this should lower the severity somewhat, but I am no expert on security policy, so I defer to you experts here.

I would have to read the change in more detail to figure out if the WeakPtr workaround would truly patch the security hole or just defer it to a different location.

### yh...@chromium.org (2013-06-05)

I spent today for the investigation and I note what I understand here.
The UAF occurs in the browser shutdown process.

The shutdown procedure BrowserMainLoop::ShutdownThreadsAndCleanup works as follows.

 1. parts->PostMainMessageLoopRun() (destroys profiles and URL request contexts)
 2. resource_dispacher_host_.get()->Shutdown() (cancels pending requests)
 3. stop threads

Thread::Stop works asynchronously. It pushes a task which really stops the thread at the last of the thread message queue. It means that already queued task is not canceled.
Hence SocketStream instances run after the request context destruction and it causes the UAF. Maybe we should implement SocketStreamDispatcherHost::Shutdown and call it in BrowserMainLoop::ShutdownThreadsAndCleanup.


### cb...@chromium.org (2013-06-05)

Could you do SocketStream::set_context(NULL) on all active socket streams when the URLRequestContext goes out of scope? A cursory look at socket stream shows that it _mostly_ handles empty context. One exception seems to be if there is a cert issue.

### yh...@chromium.org (2013-06-05)

> Thread::Stop works asynchronously. It pushes a task which really stops the thread at the last of the thread message queue.
I found it is not correct. But the conclusion does not change.


### cb...@chromium.org (2013-06-05)

I was also concerned that there may be a UAF on the SocketStream::Delegate (since the SocketStream's are RefCounted and may outlive the SocketStreamDispatcherHost) - but it looks like cases are handled. It may not hurt to put a defensive check in SocketStream::DoResolveProtocol, but it looks like that will only be called when delegate_ is non-NULL.

### cb...@chromium.org (2013-06-05)

Actually: at the time we call DetachDelegate() in ~SocketStreamHost couldn't we also call set_context(NULL)? This would be a pretty trivial patch.

Are there any times that the URLRequestContext goes out of scope prior to the SocketStreamHost's destructor? It looks like the lifetime of SocketStreamHost is tied to that of SocketStreamDispatcherHost - which in turn looks like it is tied to the lifetime of a RenderProcessHost. 

### cb...@chromium.org (2013-06-05)

Ah: We'd need to add a method to SocketStreamJob for SetContext() to pass down into the SocketStream - but the general idea still exists. 

### ty...@chromium.org (2013-06-05)

> DoResolveProtocol

Yes. I made a change (not committed yet) to make it clear that DoResolveProtocol is called only when delegate_ is non null.

> URLRequestContext goes out of scope ...

yhirano checked that it's possible SocketStreamDispatcherHost outlives URLRequestContext. I also saw that ChannelProxy delays deletion of filters. Still investigating.

> set_context(NULL)

set_context itself is also problematic. We need to call CancelPacRequest if resolver is alive but we don't know that.

### ty...@chromium.org (2013-06-05)

We're trying to do something like resource_dispatcher_host_.get()->Shutdown() in BrowserMainLoop::ShutdownThreadsAndCleanUp() for SocketStream.

### ty...@chromium.org (2013-06-05)

[Empty comment from Monorail migration]

### cb...@chromium.org (2013-06-05)

#25: Thanks. I definitely want an expedient fix but would prefer one which is localized to SocketStream as much as possible - sounds like you are heading in that direction.

### yh...@chromium.org (2013-06-05)

I wrote another fix without WeakPtr.
https://codereview.chromium.org/16439006/
cbentzel@, mmenke@, can you take a look at it?

### mm...@chromium.org (2013-06-05)

When this problem occur, is anything holding onto a reference to the SocketStream other than the callback?  We may just be able to fix this by having the SocketStream pass a weak pointer to itself to the async call.

### cb...@chromium.org (2013-06-05)

SocketStream is refcounted. Not sure if we want to change to a
non-ref-counted with WeakPtr model right now.

### mm...@chromium.org (2013-06-05)

I was suggesting refcounted *and* WeakPtr.  The WeakPtr would be private, and just for that one callback.

### yh...@chromium.org (2013-06-06)

[Comment Deleted]

### yh...@chromium.org (2013-06-06)

The root cause seems to be a delayed destruction of WorkerProcessHost. Since the destruction is delayed, the destruction of the SocketStreamDispatcherHost attached to the process misses the deadline, the destruction of the profile.
RenderProcessHost seems not to have the same issue. See comments in RenderProcessHostImpl::Cleanup.

I am writing yet another CL fixing it.


### yh...@chromium.org (2013-06-06)

> When this problem occur, is anything holding onto a reference to the SocketStream other than the callback?  We may just be able to fix this by having the SocketStream pass a weak pointer to itself to the async call.
I don't think it does fix the problem.
The UAF occurs because a SocketStream touches an invalid URLRequestContext. So we should prolong the the life of URLRequestContext or kill the SocketStream more rapidly.

### cb...@chromium.org (2013-06-06)

Matt's suggestion was to kill the SocketStream more quickly. He was
concerned that the only reference keeping the SocketStream alive was
the callback. If this used a WeakPtr rather than a refCounted pointer,
it would not keep the SocketStream alive. However - there are other
places that maintain references to SocketStream (SocketStreamJob, I
think it internally calls AddRef) - and these may keep the count above
1.

### yh...@chromium.org (2013-06-06)

As in #33, SocketStreamDispatcherHost instances for workers lives when a profile is destroyed and SocketStreamDispathcher holds SocketStream indirectly.
So,
> that the only reference keeping the SocketStream alive was the callback
is not true.


### cb...@chromium.org (2013-06-06)

#36 makes sense, solution to #33 sounds like it is tackling root cause. However, I do worry that the context will be 

I'll talk to TPM about stable refresh timing. Now I think we want to accept the initial "Add WeakPtr to URLRequestContext" as a temporary bandaid - but we still need to tackle the real solution so that can be undone.

### yh...@chromium.org (2013-06-06)

Yet another CL: https://codereview.chromium.org/16034010/

### mm...@chromium.org (2013-06-06)

The concern about StreamSocketJob and WebSocketJob adding references may not matter - at least on trunk, it looks like neither class is being used.  At least I can't find any constructor calls or storage of them in scoped_refptrs, and running sample pages that use StreamSockets does not result in them being instantiated, though I don't have any tests that use WebSockets from a WebWorker.

The fact that WorkerProcessHosts outlive their profiles definitely seems like a bug, and on sooner rather than later, I think we should use my weak pointer suggestion and fix that lifetime issue.   We should also either get rid of refcounting SocketStreams or just get rid of SocketStreams all together.

As an immediate bug fix, we may have to go with the weak_ptr solution, but we should make sure we pretty heavily unit test it, to make sure all paths are protected.

### mm...@chromium.org (2013-06-06)

Also, could someone give me access to 242762?  I'd like that repro.  I'm also unsure if it's a duplicate of this bug, or just related, or what.

### in...@chromium.org (2013-06-06)

done! cced you on 242762

### xh...@chromium.org (2013-06-06)

[Empty comment from Monorail migration]

### mm...@chromium.org (2013-06-06)

I was wrong about not using the StreamSocketJobs - forgot to include the net:: prefix on my search.  I'll go ahead and review the WeakPtr fix.

### yh...@chromium.org (2013-06-07)

[Empty comment from Monorail migration]

### ri...@chromium.org (2013-06-10)

I have attached a slightly reduced reproduction case. Still requires the user to load it in an incognito window to get a browser UAF (otherwise you just get a zero-page pointer dereference in the Worker process).

It appears the problem does not reproduce with Worker, only with SharedWorker.

### at...@chromium.org (2013-06-10)

Yes, Workers are now implemented as a thread within the renderer process -- only SharedWorkers currently have their own process.

### yh...@chromium.org (2013-06-10)

I landed the workaround patch as https://src.chromium.org/viewvc/chrome?revision=205158&view=revision .
Can you verify it?


### in...@chromium.org (2013-06-10)

I don't see any testcase here to verify, will let Ricea@ to confirm.

### th...@gmail.com (2013-06-10)

I cannot repro the original crash anymore (Tested on Windows 7 with 205184). It still crashes, but those crashes are familiar ones, or null (class) pointers.

I've tested this with the original script: https://code.google.com/p/chromium/issues/detail?id=242762#c5.

and with the optimized one: c#46 (without an extra webworker).


### ri...@chromium.org (2013-06-11)

Confirmed. The Worker process still crashes frequently, but with a NULL pointer dereference that is probably not exploitable.

### at...@chromium.org (2013-06-11)

yhirano: can you explain your comment here: "RenderProcessHost seems not to have the same issue. See comments in RenderProcessHostImpl::Cleanup."

I don't see any useful comments in RenderProcessHostImpl::Cleanup() - the only comment I see is about setting the ThreadWasQuitProperly() flag, and I don't understand how that relates to why RenderProcessHostImpl doesn't have the same problems as shared workers. Can someone who understands this mechanism please explain it a bit more clearly?

+mad - looks like you've had your fingers in ProfileDestroyer. Can you shed some light on this issue? To whit: ProfileDestroyer is only hanging around waiting for RenderProcessHosts to exit, but it sounds like Profiles should really hang around waiting for WorkerProcessHosts to exit as well. From looking at the code in ProfileDestroyer, it sounds like there are cases where we free an incognito profile before all of its RPHs have exited - why doesn't that cause problems/crashes? It seems really bad to have an RPH or WPH outlive its parent BrowserContext, so I'm assuming we have some kind of mechanism in place to deal with this?

### yh...@chromium.org (2013-06-11)

    // It's important not to wait for the DeleteTask to delete the channel
    // proxy. Kill it off now. That way, in case the profile is going away, the
    // rest of the objects attached to this RenderProcessHost start going
    // away first, since deleting the channel proxy will post a
    // OnChannelClosed() to IPC::ChannelProxy::Context on the IO thread.

At least, RenderProcessHostImpl recognizes that the profile may go away if the destruction delays.

In fact, RenderProcessHostImpl::Cleanup is called before Profile is destructed. It destroyes channel_ (IPC::ChannelProxy instance) and the ChannelProxy destroys its ChannelProxy::Context instance asynchronously. The ChannelProxy::Context deletes all filters (including a SocketStreamDispatcherHost) on destruction.

On the other hand, URLRequestContext is included in ProfileIOData in Profile.
Since Profile is valid at the call of RenderProcessHostImpl and both ProfileIOData and ChannelProxy::Context will be destroyed on the same thread (IO thread), the URLRequestContext destruction cannot be precede the SocketStreamDispatcherHost destruction.

RenderProcessHostImpl has a WorkerMessageFilter as a filter. Once it detects the channel closing (at the same timing of the ChannelProxy::Context destruction above), it calls WorkerProcessHost::FilterShutdown indirectly, synchronously.
At this point, URLRequestContext is alive. So the CL try to make the SocketStreamDispatcher inactive in FilterShutdown.
At some point after that, WorkerProcessHost will detect that its own IPC channel is closed and will delete all filters (including the SocketStreamDispatcherHost), but URLRequestContext will be already destroyed at the time.



### at...@chromium.org (2013-06-11)

Ah, thanks. I stupidly just searched for "cleanup" in that file and was unintentionally reading the useless comments in RendererMainThread::CleanUp()

### ma...@chromium.org (2013-06-11)

To answer comment @51, the profile destroy is kind of back to work around a sync destruction issues. The reason for not waiting before deleting incognito, is to avoid privacy issues...

Also, we don't wait forever, we just add a slight delay for a sync issues, if a rvh lives longer (e.g. leaks) there will be a echeck and the real source of the problem must be fixed.

I hope this helps, at least a bit. ;-)

### sc...@gmail.com (2013-06-21)

@yhirano: sorry to be a pain but would you mind merging this to M28 for us? The deadline for the final M28 build is Tuesday.

I'd normally do it myself but there's a non-trivial merge conflict and I don't want to go in and wreck the net code ;-)

### yh...@chromium.org (2013-06-21)

I commited https://src.chromium.org/viewvc/chrome?view=rev&revision=207765 .
Sorry, I failed at r207763 and reverted it at r207764.


### yh...@chromium.org (2013-06-21)

I commited https://src.chromium.org/viewvc/chrome?view=rev&revision=207765 .
Sorry, I failed at r207763 and reverted it at r207764.


### sc...@gmail.com (2013-06-21)

Thanks so much!

### sc...@gmail.com (2013-06-25)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-27)

$3133.7 for this one. Thanks again!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### th...@gmail.com (2013-06-27)

Thanks!

### yh...@chromium.org (2013-07-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-07-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### tk...@chromium.org (2015-11-27)

[Empty comment from Monorail migration]

### tk...@chromium.org (2015-11-27)

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

This issue was migrated from crbug.com/chromium/244746?no_tracker_redirect=1

[Multiple monorail components: Blink>Network>WebSockets, Blink>Workers]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077608)*
