# Security: UNKNOWN in RenderFrameImpl::OnMessageReceived 

| Field | Value |
|-------|-------|
| **Issue ID** | [40081488](https://issues.chromium.org/issues/40081488) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Reporter** | ch...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2015-02-24 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 43.0.2313.0 canary  

Operating System: Windows 7

**REPRODUCTION CASE**  

Actually this issue needs several attempts for repro the crash, I uploaded a video for see how I repro it  

but I'm looking for another way to repro it easily.

Crash ID: a20a8abec387eccc  

206d3cf668db709e  

c7967da3ee8b4998

eax=88ef4125 ebx=0890b400 ecx=2541e630 edx=001cf5a4 esi=0738eb50 edi=0890b400  

eip=0f458e67 esp=001cf2e0 ebp=001cf62c iopl=0 nv up ei ng nz na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010286  

chrome\_child!content::RenderFrameImpl::OnMessageReceived+0x27:  

0f458e67 ff5064 call dword ptr [eax+64h] ds:0023:88ef4189=????????  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it  

ChildEBP RetAddr  

001cf62c 0f414a39 chrome\_child!content::RenderFrameImpl::OnMessageReceived+0x27 [c:\b\build\slave\win\build\src\content\renderer\render\_frame\_impl.cc @ 950]  

001cf63c 0f414a11 chrome\_child!content::MessageRouter::RouteMessage+0x24 [c:\b\build\slave\win\build\src\content\common\message\_router.cc @ 55]  

001cf648 0f3870a6 chrome\_child!content::MessageRouter::OnMessageReceived+0x1d [c:\b\build\slave\win\build\src\content\common\message\_router.cc @ 47]  

001cf6d8 0f386fe3 chrome\_child!content::ChildThreadImpl::OnMessageReceived+0xa3 [c:\b\build\slave\win\build\src\content\child\child\_thread\_impl.cc @ 545]  

001cf70c 0f386f48 chrome\_child!IPC::ChannelProxy::Context::OnDispatchMessage+0x98 [c:\b\build\slave\win\build\src\ipc\ipc\_channel\_proxy.cc @ 283]  

001cf71c 0f385a56 chrome\_child!base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall content::InputEventFilter::\*)(IPC::Message const &)>,void \_\_cdecl(content::InputEventFilter \*,IPC::Message const &),base::internal::TypeList<content::InputEventFilter \*,IPC::Message> >,base::internal::TypeList<base::internal::UnwrapTraits<content::InputEventFilter \*>,base::internal::UnwrapTraits[IPC::Message](javascript:void(0);) >,base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (\_\_thiscall content::InputEventFilter::\*)(IPC::Message const &)>,base::internal::TypeList<content::InputEventFilter \* const &,IPC::Message const &> >,void \_\_cdecl(void)>::Run+0x20 [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 346]  

001cf794 0f3f29fe chrome\_child!base::debug::TaskAnnotator::RunTask+0x1b7 [c:\b\build\slave\win\build\src\base\debug\task\_annotator.cc @ 63]  

001cf7e0 0f3f2554 chrome\_child!content::TaskQueueManager::ProcessTaskFromWorkQueue+0x4c [c:\b\build\slave\win\build\src\content\renderer\scheduler\task\_queue\_manager.cc @ 419]  

001cf804 0f3f24c2 chrome\_child!content::TaskQueueManager::DoWork+0x8e [c:\b\build\slave\win\build\src\content\renderer\scheduler\task\_queue\_manager.cc @ 389]  

001cf818 0f3f2483 chrome\_child!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (\_\_thiscall content::TaskQueueManager::\*)(bool)>,base::internal::TypeList<base::WeakPtr[content::TaskQueueManager](javascript:void(0);) const &,bool const &> >::MakeItSo+0x3a [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 303]  

001cf82c 0f385a56 chrome\_child!base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall content::TaskQueueManager::\*)(bool)>,void \_\_cdecl(content::TaskQueueManager \*,bool),base::internal::TypeList<base::WeakPtr[content::TaskQueueManager](javascript:void(0);),bool> >,base::internal::TypeList<base::internal::UnwrapTraits<base::WeakPtr[content::TaskQueueManager](javascript:void(0);) >,base::internal::UnwrapTraits<bool> >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (\_\_thiscall content::TaskQueueManager::\*)(bool)>,base::internal::TypeList<base::WeakPtr[content::TaskQueueManager](javascript:void(0);) const &,bool const &> >,void \_\_cdecl(void)>::Run+0x1e [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 346]  

001cf8a4 0f3856db chrome\_child!base::debug::TaskAnnotator::RunTask+0x1b7 [c:\b\build\slave\win\build\src\base\debug\task\_annotator.cc @ 63]  

001cf8dc 0f38552d chrome\_child!base::MessageLoop::RunTask+0xed [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 451]  

001cf9e8 0f387a06 chrome\_child!base::MessageLoop::DoWork+0x2c1 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 571]  

001cfa14 0f3851b2 chrome\_child!base::MessagePumpDefault::Run+0xc7 [c:\b\build\slave\win\build\src\base\message\_loop\message\_pump\_default.cc @ 33]  

001cfa38 0f3850ba chrome\_child!base::MessageLoop::RunHandler+0x65 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 415]  

001cfa60 0f386624 chrome\_child!base::RunLoop::Run+0x88 [c:\b\build\slave\win\build\src\base\run\_loop.cc @ 56]  

001cfa84 0f3d8e5c chrome\_child!base::MessageLoop::Run+0x16 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 308]  

001cfc24 0f37e265 chrome\_child!content::RendererMain+0x277 [c:\b\build\slave\win\build\src\content\renderer\renderer\_main.cc @ 221]  

001cfc38 0f37e1e1 chrome\_child!content::RunNamedProcessTypeMain+0x61 [c:\b\build\slave\win\build\src\content\app\content\_main\_runner.cc @ 385]

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [Chrome-last.dmp](attachments/Chrome-last.dmp) (application/octet-stream, 284.9 KB)
- [video.mp4](attachments/video.mp4) (application/octet-stream, 489.2 KB)
- [testcase.html](attachments/testcase.html) (text/html, 1.1 KB)
- [1.png](attachments/1.png) (image/png, 41.3 KB)
- [steps.mp4](attachments/steps.mp4) (application/octet-stream, 1.0 MB)
- [testcase.html](attachments/testcase_53017570.html) (text/html, 1.1 KB)
- [screenshot.png](attachments/screenshot.png) (image/png, 52.0 KB)
- [issue 461191.mp4](attachments/issue 461191.mp4) (application/octet-stream, 1.5 MB)

## Timeline

### ch...@gmail.com (2015-02-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-24)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-02-25)

[Comment Deleted]

### cl...@chromium.org (2015-02-27)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-02-28)

Reproduced on stable channel (40.0.2214.115 m).

Still trying to figure it out. Here is crash ID:

Crash ID 684cc87c99c55601



### in...@chromium.org (2015-03-02)

I see navigator.webkitGetUserMedia, and your repro shows camera pop-us. so, something related to webrtc. Assigning to Patrick for help in triage and finding owner.

### ch...@gmail.com (2015-03-02)

I created a new testcase because I couldn't repro this with using that testcase in #1 this crash seems like needs some iframe contains ads for keep pages loading as in screenshot-1.png. I uploaded a video too see how I repro this.

### cl...@chromium.org (2015-03-02)

[Empty comment from Monorail migration]

### ph...@chromium.org (2015-03-03)

chromium.khalil: What is it you're doing in the beginning when you open all those tabs? Are the multiple tabs necessary to repro?

I'll CC in some WebRTC people, but I'm not sure this is a pure WebRTC crash. The problem might be in the borderlands between WebRTC and the rest of the browser. RenderFrameImpl does contain references to web media player which plays back WebRTC video and audio (I think), but it never gets used in this case because we can see in the testcase that we never play the media stream (on gUM success, close the window and throw away the stream).

The crash happens in OnMessage: is this a crash in the IPC framework? Abhishek, can you CC in some IPC people or people working on the general browser to help understand this?

### in...@chromium.org (2015-03-03)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-03-03)

Patrick, When I open those tabs I wait til see some tabs are ready (are not loading) as in screenshot.png and go to some of them than keep clicking on the page.

### ch...@gmail.com (2015-03-03)

I have made this video I think is more clarity in steps.

### tn...@chromium.org (2015-03-03)

According to the testcase code in #7, each tab that is created includes this onclick handler:

    i.onclick = function() {
      setTimeout(function() {  
                navigator.webkitGetUserMedia({video: true}, function(){window.close()}, function(){window.close()});
                window.close()
           }, 200);

Perhaps because the gUM call is asynchronous, I've only seen the gUM prompt appear once, and I wasn't quick enough to click the infobar. I may also be having problems reproducing this because my setup differs from the originally reported M43 crash reports in these ways:
a) crash reports - from a 32 bit machine, while I was testing with 64 bit binaries
b) uploaded videos indicate use of http server, while I was testing over https. This difference is important because https should remember gUM responses to requests from the same domain.

Even if I get a repro, I'm not clear that WebRTC is the cause. 

chromium.khalil@ - can you see if you can repro with nearly the same testcase code, except swap out the getUserMedia call with something else that triggers an infobar, such as a geolocation request?

### ch...@gmail.com (2015-03-03)

I have tried with using SpeechRecognition API and geolocation but I wasn't able to repro.

### cl...@chromium.org (2015-03-05)

[Empty comment from Monorail migration]

### jl...@chromium.org (2015-03-05)

tnakamura@, assigning to you for better tracking, but re-assign if needed.

### ph...@chromium.org (2015-03-06)

We are unsure on how to proceed. Ted can't repro manually and it's probably at best tangentially related to WebRTC. nasko, creis, do you have any IPC wisdom to impart here? 

Appears the crash is in content/renderer/render_frame_impl.cc. Back at the time for Chrome 43.0.2313.0 (base commit 2b5fc4b664d47828d4e999a0fb17b22038318864) this was the code around line 950:

bool RenderFrameImpl::OnMessageReceived(const IPC::Message& msg) {
  // TODO(kenrb): document() should not be null, but as a transitional step
  // we have RenderFrameProxy 'wrapping' a RenderFrameImpl, passing messages
  // to this method. This happens for a top-level remote frame, where a
  // document-less RenderFrame is replaced by a RenderFrameProxy but kept
  // around and is still able to receive messages.
  if (!frame_->document().isNull())
    GetContentClient()->SetActiveURL(frame_->document().url());

  ObserverListBase<RenderFrameObserver>::Iterator it(observers_);
  RenderFrameObserver* observer;
  while ((observer = it.GetNext()) != NULL) {
    if (observer->OnMessageReceived(msg))
      return true;
  }

This line is the one that blows up:

if (!frame_->document().isNull())

, so I guess either frame_ or frame_->document() is junk.

cc:ing jam and nick who are in the blame list around that area. Can you help us understand how this can happen? What do we need to do to process? This is apparently quite hard to repro.

Also, is it really high priority, impacts stable, security and so on?

### cl...@chromium.org (2015-03-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-03-12)

possible renderframe lifetime issue?  nasko or creis can you take a look at this?

### cr...@chromium.org (2015-03-13)

Taking a quick look to triage this.  The crashes date back to about Chrome 36.

It boils down to a WebLocalFrame getting deleted before RenderFrameImpl.  Daniel (or Lucas): what's the expected order of deletion for WebLocalFrame and RenderFrameImpl?  Is there a way we can at least null out the frame_ pointer in RenderFrameImpl rather than leaving it dangling and leading to this UaF?

Side note: Ken's TODO and the isNull() call (see https://crbug.com/chromium/461191#c17) are stale after my r305276.  I'll remove them, but that will just postpone the UaF to the following line's frame_->document().url() call.

### cr...@chromium.org (2015-03-13)

Yikes.  For main frames, we delete the WebLocalFrameImpl in RenderFrameImpl::frameDetached(), when it calls WebLocalFrame::Close().  But the RenderFrameImpl itself doesn't get deleted until an entirely separate event, via RenderWidget::Release (which deletes both the RenderView and RenderFrame).  In the meantime, RenderFrameImpl::is_detaching_ is true, but we have a dangling frame_ pointer and no one (except Send) checks it.

This means that arbitrary methods can be called when frame_ is bogus.

RenderViewImpl seems to take care of this by nulling out its webview() (actually, RenderWidget does this), and then having null checks everywhere on the accesses to webview().

Unfortunate, but we need to do the same in RenderFrameImpl.  frameDetached should null out frame_ and everyone needs to null check it.

I'll do this first thing on Monday unless someone beats me to it.

### cl...@chromium.org (2015-03-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5761100646187008

Fuzzer: Aohelin_ni
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x611000064040
Crash State:
  content::RenderFrameImpl::OnMessageReceived
  content::MessageRouter::RouteMessage
  content::MessageRouter::OnMessageReceived
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95jojrwBlyTwfqwzEMKg1uZeGVXiNls03N6jsVMcbFvcEF8Gr0fHKCxCra3fOGv78I67m6laz2pC40dC1n91Idv-u_-lIVHpQA5h9_2Q0FgTqEX_3awnJGGMwhmVMnlwGqDFwuzSqZ6JMs_YPxwTA-zZREs7UGHJFytPH1tk-biaK2x360


Filer: inferno

### in...@chromium.org (2015-03-14)

Charlie, i think c#23 is the same bug and we have a nice uaf stack if you need ?

### cr...@chromium.org (2015-03-16)

Thanks.  I've got a fix with test up for review:
https://codereview.chromium.org/1007123003/

### cr...@chromium.org (2015-03-16)

The automated commit email hasn't shown up, but the fix for this landed in r320773.  Should be gone from tomorrow's canary.

Once that has a chance to bake, we can see about merging the fix.

### ch...@gmail.com (2015-03-16)

Thanks Charlie! Tomorrow I will test it on canary.

### cl...@chromium.org (2015-03-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cfaa4468f3394995a9f1565104ee2743a30d58e0

commit cfaa4468f3394995a9f1565104ee2743a30d58e0
Author: creis <creis@chromium.org>
Date: Mon Mar 16 19:27:18 2015

Clear RenderFrameImpl::frame_ pointer after deleting it.

Also avoid dereferencing it in OnMessageReceived after deletion.

BUG=461191
TEST=No more crashes in RenderFrameImpl::OnMessageReceived

Review URL: https://codereview.chromium.org/1007123003

Cr-Commit-Position: refs/heads/master@{#320773}

[modify] http://crrev.com/cfaa4468f3394995a9f1565104ee2743a30d58e0/content/renderer/render_frame_impl.cc
[modify] http://crrev.com/cfaa4468f3394995a9f1565104ee2743a30d58e0/content/renderer/render_frame_impl.h
[modify] http://crrev.com/cfaa4468f3394995a9f1565104ee2743a30d58e0/content/renderer/render_view_browsertest.cc
[modify] http://crrev.com/cfaa4468f3394995a9f1565104ee2743a30d58e0/content/renderer/render_view_impl.h


### cr...@chromium.org (2015-03-18)

It looks like this is doing well.  I don't see any RenderFrameImpl::OnMessageReceived crashes as of 43.0.2335.0.

Shall we merge it to M42 (and later M41)?

### am...@google.com (2015-03-18)

[Automated comment] Request affecting a post-stable build (M41), manual review required.

### am...@google.com (2015-03-18)

Approved for M42 (branch: 2311)

### cr...@chromium.org (2015-03-18)

Great.  I'll do it first thing tomorrow, since I need to head out early today.

### bu...@chromium.org (2015-03-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b92260b108fc4b79361e9ea30ad903fa8359e338

commit b92260b108fc4b79361e9ea30ad903fa8359e338
Author: creis <creis@chromium.org>
Date: Thu Mar 19 16:19:58 2015

Clear RenderFrameImpl::frame_ pointer after deleting it.

Also avoid dereferencing it in OnMessageReceived after deletion.

NOTRY=true
TBR=nasko
BUG=461191
TEST=No more crashes in RenderFrameImpl::OnMessageReceived

Review URL: https://codereview.chromium.org/1007123003

Cr-Commit-Position: refs/heads/master@{#320773}
(cherry picked from commit cfaa4468f3394995a9f1565104ee2743a30d58e0)

Review URL: https://codereview.chromium.org/1002493004

Cr-Commit-Position: refs/branch-heads/2311@{#284}
Cr-Branched-From: 09b7de5dd7254947cd4306de907274fa63373d48-refs/heads/master@{#317474}

[modify] http://crrev.com/b92260b108fc4b79361e9ea30ad903fa8359e338/content/renderer/render_frame_impl.cc
[modify] http://crrev.com/b92260b108fc4b79361e9ea30ad903fa8359e338/content/renderer/render_frame_impl.h
[modify] http://crrev.com/b92260b108fc4b79361e9ea30ad903fa8359e338/content/renderer/render_view_browsertest.cc
[modify] http://crrev.com/b92260b108fc4b79361e9ea30ad903fa8359e338/content/renderer/render_view_impl.h


### cr...@chromium.org (2015-03-19)

Looks like the merge to M42 cleared the beta builders.  Should I merge to M41 as well, or wait for M42 to bake?

### pe...@google.com (2015-03-20)

Merge approved for m41 branch 2272.

### bu...@chromium.org (2015-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e176af4a53e7d4483e5dda125d7f77f2818e697c

commit e176af4a53e7d4483e5dda125d7f77f2818e697c
Author: creis <creis@chromium.org>
Date: Fri Mar 20 16:49:01 2015

Clear RenderFrameImpl::frame_ pointer after deleting it.

Also avoid dereferencing it in OnMessageReceived after deletion.

NOTRY=true
TBR=nasko@chromium.org
BUG=461191
TEST=No more crashes in RenderFrameImpl::OnMessageReceived

Review URL: https://codereview.chromium.org/1007123003

Cr-Commit-Position: refs/heads/master@{#320773}
(cherry picked from commit cfaa4468f3394995a9f1565104ee2743a30d58e0)

Review URL: https://codereview.chromium.org/1021313002

Cr-Commit-Position: refs/branch-heads/2272@{#445}
Cr-Branched-From: 827a380cfdb31aa54c8d56e63ce2c3fd8c3ba4d4-refs/heads/master@{#310958}

[modify] http://crrev.com/e176af4a53e7d4483e5dda125d7f77f2818e697c/content/renderer/render_frame_impl.cc
[modify] http://crrev.com/e176af4a53e7d4483e5dda125d7f77f2818e697c/content/renderer/render_frame_impl.h
[modify] http://crrev.com/e176af4a53e7d4483e5dda125d7f77f2818e697c/content/renderer/render_view_browsertest.cc
[modify] http://crrev.com/e176af4a53e7d4483e5dda125d7f77f2818e697c/content/renderer/render_view_impl.h


### bu...@chromium.org (2015-03-31)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/experimental/chrome-radiance.git/+/cfaa4468f3394995a9f1565104ee2743a30d58e0

commit cfaa4468f3394995a9f1565104ee2743a30d58e0
Author: creis <creis@chromium.org>
Date: Mon Mar 16 19:27:18 2015


### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### tn...@chromium.org (2015-04-09)

chromium.khalil@, have you been able to verify that this is fixed in canary and/or any of the builds where the fix was merged into? It looks like the merges were approved based on the lack of crashes in canary (#30), which is fine, but I also want to make sure the fix looks good to you. :)

### ch...@gmail.com (2015-04-09)

I am unable again to reproduce a crash with 44.0.2362.0 canary.

### ti...@google.com (2015-04-14)

Congratulations - $3000 for this report.

Notes from panel: We're paying a higher amount here because we think that may be scenarios where this could possibly result in a sandbox escape.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-23)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/461191?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/461427]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081488)*
