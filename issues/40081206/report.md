# Security: Heap-use-after-free SpeechRecognitionDispatcher

| Field | Value |
|-------|-------|
| **Issue ID** | [40081206](https://issues.chromium.org/issues/40081206) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>Speech |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ml...@chromium.org |
| **Created** | 2015-01-17 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 42.0.2278.0 canary and Chromium 42.0.2277.0 (Developer Build) (32-bit)  

Operating System: Win7

What steps will reproduce the problem?

1. Start chrome
2. Open <http://jsfiddle.net/5xBpW/show> in chrome and allow the micro request and click on Result

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Client ID (if relevant): 832ee1f4ae0dec75

eax=05609938 ebx=00000001 ecx=0560993c edx=0022eb30 esi=0485ceb0 edi=0485ce90  

eip=0486f9c0 esp=0022eb20 ebp=0022eb34 iopl=0 nv up ei pl zr na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010246  

0486f9c0 100deb51e840 adc byte ptr ds:[40E851EBh],cl ds:0023:40e851eb=??  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it  

ChildEBP RetAddr  

WARNING: Frame IP not in any known module. Following frames may be wrong.  

0022eb1c 516c11bb 0x486f9c0  

0022eb34 50637131 chrome\_child!content::SpeechRecognitionDispatcher::OnRecognitionEnded+0x53 [c:\b\build\slave\win\build\src\content\renderer\speech\_recognition\_dispatcher.cc @ 216]  

0022eb44 5069e4b7 chrome\_child!MidiMsg\_AcknowledgeSentData::Dispatch<content::MidiMessageFilter,content::MidiMessageFilter,void,void (\_\_thiscall content::MidiMessageFilter::\*)(unsigned int)>+0x22 [c:\b\build\slave\win\build\src\content\common\media\midi\_messages.h @ 58]  

0022ec18 5069d023 chrome\_child!content::SpeechRecognitionDispatcher::OnMessageReceived+0x1dc [c:\b\build\slave\win\build\src\content\renderer\speech\_recognition\_dispatcher.cc @ 56]  

0022f030 5064bd33 chrome\_child!content::RenderViewImpl::OnMessageReceived+0xc0 [c:\b\build\slave\win\build\src\content\renderer\render\_view\_impl.cc @ 1277]  

0022f040 5064bd0b chrome\_child!content::MessageRouter::RouteMessage+0x24 [c:\b\build\slave\win\build\src\content\common\message\_router.cc @ 55]  

0022f04c 505c4925 chrome\_child!content::MessageRouter::OnMessageReceived+0x1d [c:\b\build\slave\win\build\src\content\common\message\_router.cc @ 47]  

0022f0c8 505c486a chrome\_child!content::ChildThread::OnMessageReceived+0x9b [c:\b\build\slave\win\build\src\content\child\child\_thread.cc @ 512]  

0022f0fc 505c47cf chrome\_child!IPC::ChannelProxy::Context::OnDispatchMessage+0x98 [c:\b\build\slave\win\build\src\ipc\ipc\_channel\_proxy.cc @ 283]  

0022f10c 505c3aa7 chrome\_child!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<bool (\_\_thiscall content::ChildMessageFilter::\*)(IPC::Message const &)>,void \_\_cdecl(content::ChildMessageFilter \*,IPC::Message const &),void \_\_cdecl(scoped\_refptr[content::ChildMessageFilter](javascript:void(0);),IPC::Message)>,void \_\_cdecl(content::ChildMessageFilter \*,IPC::Message const &)>::Run+0x16 [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 562]  

0022f1bc 50635601 chrome\_child!base::debug::TaskAnnotator::RunTask+0x2ce [c:\b\build\slave\win\build\src\base\debug\task\_annotator.cc @ 63]  

0022f204 506351dd chrome\_child!content::TaskQueueManager::ProcessTaskFromWorkQueue+0x48 [c:\b\build\slave\win\build\src\content\renderer\scheduler\task\_queue\_manager.cc @ 371]  

0022f214 506351a1 chrome\_child!content::TaskQueueManager::DoWork+0x38 [c:\b\build\slave\win\build\src\content\renderer\scheduler\task\_queue\_manager.cc @ 342]  

0022f228 50635162 chrome\_child!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (\_\_thiscall content::TaskQueueManager::\*)(bool)>,void \_\_cdecl(base::WeakPtr[content::TaskQueueManager](javascript:void(0);) const &,bool const &)>::MakeItSo+0x3a [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 391]  

0022f23c 505c3aa7 chrome\_child!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall content::TaskQueueManager::\*)(bool)>,void \_\_cdecl(content::TaskQueueManager \*,bool),void \_\_cdecl(base::WeakPtr[content::TaskQueueManager](javascript:void(0);),bool)>,void \_\_cdecl(content::TaskQueueManager \*,bool)>::Run+0x16 [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 562]  

0022f2ec 505c358b chrome\_child!base::debug::TaskAnnotator::RunTask+0x2ce [c:\b\build\slave\win\build\src\base\debug\task\_annotator.cc @ 63]  

0022f324 505c340d chrome\_child!base::MessageLoop::RunTask+0xed [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 439]  

0022f430 505c524d chrome\_child!base::MessageLoop::DoWork+0x2c1 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 555]  

0022f45c 505c3092 chrome\_child!base::MessagePumpDefault::Run+0xc8 [c:\b\build\slave\win\build\src\base\message\_loop\message\_pump\_default.cc @ 33]  

0022f480 505c2f9a chrome\_child!base::MessageLoop::RunHandler+0x65 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 406]

## Attachments

- [repro.mp4](attachments/repro.mp4) (application/octet-stream, 283.1 KB)

## Timeline

### mb...@chromium.org (2015-01-18)

This seems to be consistently reproducible.

### mb...@chromium.org (2015-01-18)

tommi, could you take a look at this one as well or help find another owner?

### cl...@chromium.org (2015-01-18)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-01-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-20)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### to...@chromium.org (2015-01-20)

[Empty comment from Monorail migration]

### pe...@chromium.org (2015-01-21)

[Empty comment from Monorail migration]

### pe...@chromium.org (2015-01-21)

Bisecting this points to https://chromium.googlesource.com/chromium/blink/+log/8c3b8de..1d9bab3

and especially https://chromium.googlesource.com/chromium/blink/+/c8895b668d6ef8a9bed07bfd4b7b656550b38872. 
It looks like the refactoring is half done in M41? 

### tn...@chromium.org (2015-01-21)

[Empty comment from Monorail migration]

### ml...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-01-23)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=188868

------------------------------------------------------------------
r188868 | mlamouri@chromium.org | 2015-01-23T09:35:45.585332Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechRecognition.cpp?r1=188868&r2=188867&pathrev=188868
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebViewImpl.cpp?r1=188868&r2=188867&pathrev=188868
   M http://src.chromium.org/viewvc/blink/trunk/public/web/WebFrameClient.h?r1=188868&r2=188867&pathrev=188868
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechRecognitionController.cpp?r1=188868&r2=188867&pathrev=188868
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/speech/SpeechRecognitionController.h?r1=188868&r2=188867&pathrev=188868
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/WebLocalFrameImpl.cpp?r1=188868&r2=188867&pathrev=188868

Revert of Make SpeechRecognitionController per frame instead of per page. (patchset #3 id:40001 of https://codereview.chromium.org/636863002/)

Reason for revert:
https://crbug.com/449739

Original issue's description:
> Make SpeechRecognitionController per frame instead of per page.
> 
> This is still using the WebViewClient::speechRecognizer() if
> WebFrameClient::speechRecognizer() returns null. After part 2
> lands, part 3 will remove it.
> 
> Part 1: <this>
> Part 2: https://codereview.chromium.org/636863003/
> Part 3: https://codereview.chromium.org/752303003/
> 
> BUG=390749
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=186174

TBR=dcheng@chromium.org,mkwst@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=390749,449739

Review URL: https://codereview.chromium.org/863213002
-----------------------------------------------------------------

### ml...@chromium.org (2015-01-23)

I will need to merge this to M41. The change has not yet spent 24 hours in dev but I will wait for that before doing the merge. Regarding the risk, it's pretty low. That CL was not meant to have any behavioural change. It was meant to be a first step of a three sided patch that got blocked at the last minute by more urgent projects.

### pe...@google.com (2015-01-23)

[Automated comment] Reverts referenced in bugdroid comments, needs manual review.

### in...@chromium.org (2015-01-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-01-23)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-01-25)

[Comment Deleted]

### ch...@gmail.com (2015-01-25)

[Comment Deleted]

### in...@chromium.org (2015-01-25)

[Empty comment from Monorail migration]

### tn...@chromium.org (2015-01-26)

If it helps with the merge review - I cannot reproduce the originally reported crash with the current canary (42.0.2287.0, which includes Blink @r188902, so it includes the revert mentioned in #12).

### pe...@chromium.org (2015-01-29)

Merge approved for M41 branch 2272.

### ml...@chromium.org (2015-02-04)

Merged: https://codereview.chromium.org/899853002

### bu...@chromium.org (2015-02-04)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=189483

------------------------------------------------------------------
r189483 | mlamouri@chromium.org | 2015-02-04T11:14:47.371529Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/modules/speech/SpeechRecognitionController.h?r1=189483&r2=189482&pathrev=189483
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/web/WebLocalFrameImpl.cpp?r1=189483&r2=189482&pathrev=189483
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/modules/speech/SpeechRecognition.cpp?r1=189483&r2=189482&pathrev=189483
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/web/WebViewImpl.cpp?r1=189483&r2=189482&pathrev=189483
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/public/web/WebFrameClient.h?r1=189483&r2=189482&pathrev=189483
   M http://src.chromium.org/viewvc/blink/branches/chromium/2272/Source/modules/speech/SpeechRecognitionController.cpp?r1=189483&r2=189482&pathrev=189483

Merge 188868 "Revert of Make SpeechRecognitionController per fra..."

> Revert of Make SpeechRecognitionController per frame instead of per page. (patchset #3 id:40001 of https://codereview.chromium.org/636863002/)
> 
> Reason for revert:
> https://crbug.com/449739
> 
> Original issue's description:
> > Make SpeechRecognitionController per frame instead of per page.
> > 
> > This is still using the WebViewClient::speechRecognizer() if
> > WebFrameClient::speechRecognizer() returns null. After part 2
> > lands, part 3 will remove it.
> > 
> > Part 1: <this>
> > Part 2: https://codereview.chromium.org/636863003/
> > Part 3: https://codereview.chromium.org/752303003/
> > 
> > BUG=390749
> > 
> > Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=186174
> 
> TBR=dcheng@chromium.org,mkwst@chromium.org
> NOPRESUBMIT=true
> NOTREECHECKS=true
> NOTRY=true
> BUG=390749,449739
> 
> Review URL: https://codereview.chromium.org/863213002

TBR=mlamouri@chromium.org

Review URL: https://codereview.chromium.org/899853002
-----------------------------------------------------------------

### ri...@chromium.org (2015-02-06)

[Empty comment from Monorail migration]

### ja...@chromium.org (2015-02-10)

I hit a crash in 41.0.2272.43 using the repro steps in the description however the stack trace looks a tad different. I can see that the blink roll has not yet landed in latest available 2272 release. Can anyone confirm that this is the same issue? I will retry in the next beta release which hopefully will have the blink roll in it.

Crash id: f2987d8b2785c704 

### ch...@gmail.com (2015-02-11)

Jansson@ There is no crash in 41.0.2272.53 beta-m.

### tn...@chromium.org (2015-02-26)

I'm unable to reproduce a crash with 42.0.2311.11. Therefore, since both M42 (this comment) and M41 (#26) seem fixed, I'm updating this bug to Verified.

### cl...@chromium.org (2015-05-01)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-16)

No release label required - Beta impact only.

### ti...@google.com (2015-06-12)

Congratulations - $1000 for this report.

Reward panel notes: Bug required significant user interaction, hence the lower payout level.

I'll add the payment to your tab ;)

We'll start payment via our new process (should take 1-2 weeks) from when you see the "reward-inprocess" label on this bug.

### ti...@google.com (2015-06-25)

We'll process this reward via our new payment process which should only take ~1-2 weeks.  

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/449739?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/443840]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081206)*
