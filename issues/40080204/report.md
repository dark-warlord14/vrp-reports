# Use-after-free in speech - saying "Hello" during the incognito window has closed

| Field | Value |
|-------|-------|
| **Issue ID** | [40080204](https://issues.chromium.org/issues/40080204) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2014-08-12 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

**VERSION**  

Chrome Version: Stable 36.0.1985.125 m  

Operating System: Win7

**REPRODUCTION CASE**

1. Launch Chrome
2. Launch Incognito window, Ctrl+N
3. Open Index.html on Incognito window as a fresh page as on Screen-shot.png and keep clicking on the button "Click here" then the page will close (which is on Incognito window)
4. "Whoa! Google Chrome has crashed."

"If my explanation was unclear please watch the video on Youtube to how to repro the crash: <http://youtu.be/8vvE-Tse6n4> "

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

eax=f813e16e ebx=00000000 ecx=0bf900a0 edx=00000002 esi=0bf900a0 edi=070101e0  

eip=5f73f7b1 esp=002fe878 ebp=002fe978 iopl=0 nv up ei pl zr na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010246  

chrome\_5e6a0000!GetExtensionVoices+0x2d:  

5f73f7b1 ff5070 call dword ptr [eax+70h] ds:0023:f813e1de=????????  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it  

ChildEBP RetAddr  

002fe978 5ee3eac9 chrome\_5e6a0000!GetExtensionVoices+0x2d [c:\b\build\slave\win\build\src\chrome\browser\speech\extension\_api\tts\_engine\_extension\_api.cc @ 64]  

002fe98c 5ee3ece2 chrome\_5e6a0000!TtsController::GetVoices+0x17 [c:\b\build\slave\win\build\src\chrome\browser\speech\tts\_controller.cc @ 302]  

002fea60 5ee3ec90 chrome\_5e6a0000!TtsController::SpeakNow+0x49 [c:\b\build\slave\win\build\src\chrome\browser\speech\tts\_controller.cc @ 157]  

002fea74 5ee3eb6f chrome\_5e6a0000!TtsController::SpeakNextUtterance+0x36 [c:\b\build\slave\win\build\src\chrome\browser\speech\tts\_controller.cc @ 330]  

002fea80 5f73fec7 chrome\_5e6a0000!TtsController::OnTtsEvent+0x3d [c:\b\build\slave\win\build\src\chrome\browser\speech\tts\_controller.cc @ 294]  

002feb04 5ea4151d chrome\_5e6a0000!ExtensionTtsEngineSendTtsEventFunction::RunSync+0x343 [c:\b\build\slave\win\build\src\chrome\browser\speech\extension\_api\tts\_engine\_extension\_api.cc @ 271]  

002feb2c 5ea34df1 chrome\_5e6a0000!SyncExtensionFunction::Run+0x15 [c:\b\build\slave\win\build\src\extensions\browser\extension\_function.cc @ 387]  

002feba4 5ea34aba chrome\_5e6a0000!extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal+0x204 [c:\b\build\slave\win\build\src\extensions\browser\extension\_function\_dispatcher.cc @ 385]  

002febd8 5ea34a19 chrome\_5e6a0000!extensions::ExtensionFunctionDispatcher::Dispatch+0x9d [c:\b\build\slave\win\build\src\extensions\browser\extension\_function\_dispatcher.cc @ 309]  

002febe8 5ea34717 chrome\_5e6a0000!extensions::ExtensionHost::OnRequest+0x14 [c:\b\build\slave\win\build\src\extensions\browser\extension\_host.cc @ 342]  

002fecb8 5ea11649 chrome\_5e6a0000!ExtensionHostMsg\_Request::Dispatch<extensions::TabHelper,extensions::TabHelper,void (\_\_thiscall extensions::TabHelper::\*)(ExtensionHostMsg\_Request\_Params const &)>+0x4a [c:\b\build\slave\win\build\src\extensions\common\extension\_messages.h @ 460]  

002fed28 5ea095b0 chrome\_5e6a0000!extensions::ExtensionHost::OnMessageReceived+0x106 [c:\b\build\slave\win\build\src\extensions\browser\extension\_host.cc @ 329]  

002fef08 5ea0955d chrome\_5e6a0000!content::WebContentsImpl::OnMessageReceived+0x4f [c:\b\build\slave\win\build\src\content\browser\web\_contents\web\_contents\_impl.cc @ 482]  

002fef1c 5ea0898c chrome\_5e6a0000!content::WebContentsImpl::OnMessageReceived+0x13 [c:\b\build\slave\win\build\src\content\browser\web\_contents\web\_contents\_impl.cc @ 468]  

002ff164 5ea088f2 chrome\_5e6a0000!content::RenderViewHostImpl::OnMessageReceived+0x8d [c:\b\build\slave\win\build\src\content\browser\renderer\_host\render\_view\_host\_impl.cc @ 982]  

002ff298 5ea0860f chrome\_5e6a0000!content::RenderProcessHostImpl::OnMessageReceived+0x2d2 [c:\b\build\slave\win\build\src\content\browser\renderer\_host\render\_process\_host\_impl.cc @ 1383]  

002ff2cc 5e753ae7 chrome\_5e6a0000!IPC::ChannelProxy::Context::OnDispatchMessage+0x98 [c:\b\build\slave\win\build\src\ipc\ipc\_channel\_proxy.cc @ 275]  

002ff2dc 5e709f7c chrome\_5e6a0000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall extensions::CountingPolicy::\*)(std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const &)>,void \_\_cdecl(extensions::CountingPolicy \*,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const &),void \_\_cdecl(base::internal::UnretainedWrapper[extensions::CountingPolicy](javascript:void(0);),std::basic\_string<char,std::char\_traits<char>,std::allocator<char> >)>,void \_\_cdecl(extensions::CountingPolicy \*,std::basic\_string<char,std::char\_traits<char>,std::allocator<char> > const &)>::Run+0x16 [c:\b\build\slave\win\build\src\base\bind\_internal.h @ 1253]  

002ff374 5e7097fd chrome\_5e6a0000!base::MessageLoop::RunTask+0x2a5 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 452]  

002ff4b8 5e786328 chrome\_5e6a0000!base::MessageLoop::DoWork+0x367 [c:\b\build\slave\win\build\src\base\message\_loop\message\_loop.cc @ 577]

## Attachments

- [Index.html](attachments/Index.html) (text/html, 110 B)
- [Screen-shot.png](attachments/Screen-shot.png) (image/png, 385.4 KB)
- [repro.html](attachments/repro.html) (text/html, 204 B)
- [Chrome-last.dmp](attachments/Chrome-last.dmp) (application/octet-stream, 324.9 KB)

## Timeline

### ch...@gmail.com (2014-08-12)

[Empty comment from Monorail migration]

### ke...@chromium.org (2014-08-12)

dmazzoni: Can you please take a look at this? It is a browser process use-after-free bug, so pretty nasty. I have only tried it in Windows but might affect other platforms also.

Crash ID: d874b06efeb1811a

### cl...@chromium.org (2014-08-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-20)

dmazzoni@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-27)

dmazzoni@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ch...@gmail.com (2014-08-27)

dmazzoni@: Could you please take a look or find someone else to own it.


### wf...@chromium.org (2014-08-27)

dtseng@ can you take a look at this high priority security issue as soon as possible, please.

### cl...@chromium.org (2014-09-04)

dtseng@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-11)

dtseng@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ch...@gmail.com (2014-09-11)

dtseng@: Can you please take a look at this issue or find someone else to own it.


### dm...@chromium.org (2014-09-11)

I'll take this one as soon as I have a chance.


### cl...@chromium.org (2014-09-19)

dmazzoni@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-26)

dmazzoni@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-04)

dmazzoni@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-14)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### ch...@gmail.com (2014-10-14)

dmazzoni@ Could you please take a look at this issue or find someone to own it.


### ch...@gmail.com (2014-10-21)

[Comment Deleted]

### ch...@gmail.com (2014-10-24)

The original dump actually looks like a use-after-free. 
It crashes here:

The vtable pointer of result_voice is invalid address.

result_voice->SetString(constants::kLangKey, voice.lang);

When a tab is closed while the result is performing 
speech utterance, the speech must be cancelled.


### dm...@chromium.org (2014-10-31)

I agree that speech must be cancelled. I can repro the crash in Chrome 39 but not Chrome 40. I'm possibly suspecting this helped: https://codereview.chromium.org/625503002


### in...@chromium.org (2014-10-31)

chromium.khalil@, can you try this on latest canary. If this is fixed with https://codereview.chromium.org/625503002, we need to mark this as Fixes and merge-request to M-39 asap.

### ch...@gmail.com (2014-10-31)

I am still able to repro this crash on latest canary.

### dm...@chromium.org (2014-10-31)

https://codereview.chromium.org/692203002/

### dm...@chromium.org (2014-11-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-11-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8880b279a491ca69db564a975cce3bbfd8f5c3e3

commit 8880b279a491ca69db564a975cce3bbfd8f5c3e3
Author: dmazzoni <dmazzoni@chromium.org>
Date: Thu Nov 06 08:44:55 2014

Stop utterances from a tab when that tab is closed.

BUG=402957,418806

Review URL: https://codereview.chromium.org/692203002

Cr-Commit-Position: refs/heads/master@{#302987}

[modify] https://chromium.googlesource.com/chromium/src.git/+/8880b279a491ca69db564a975cce3bbfd8f5c3e3/chrome/browser/speech/extension_api/tts_extension_api.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/8880b279a491ca69db564a975cce3bbfd8f5c3e3/chrome/browser/speech/tts_controller.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/8880b279a491ca69db564a975cce3bbfd8f5c3e3/chrome/browser/speech/tts_controller_impl.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/8880b279a491ca69db564a975cce3bbfd8f5c3e3/chrome/browser/speech/tts_controller_impl.h
[modify] https://chromium.googlesource.com/chromium/src.git/+/8880b279a491ca69db564a975cce3bbfd8f5c3e3/chrome/browser/speech/tts_message_filter.cc
[modify] https://chromium.googlesource.com/chromium/src.git/+/8880b279a491ca69db564a975cce3bbfd8f5c3e3/chrome/browser/speech/tts_message_filter.h


### in...@chromium.org (2014-11-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

Your fix is very close to the branch point. After the branch happens, please make sure to check if your fix is in.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### dm...@chromium.org (2014-12-22)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congratulations - $2000 for this report! Reward panel notes: "It's a browser use-after-free, but it requires two gestures to trigger".

### cl...@chromium.org (2015-02-12)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/402957?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080204)*
