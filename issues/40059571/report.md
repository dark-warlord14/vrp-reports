# Security DCHECK(TypeConfuse) failed: IsA<Derived>(from) in blink::VisualViewport::StartTrackingPinch

| Field | Value |
|-------|-------|
| **Issue ID** | [40059571](https://issues.chromium.org/issues/40059571) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Input |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | bo...@chromium.org |
| **Created** | 2022-05-05 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

#TestOn  

asan-win32-release\_x64-998137

#Reproduce  

This problem was found in the fuzzer environment, but could not be reproduced.  

I provided a sample that I think may be related to the trigger.  

The sample will continuously open new pages through the form tag. My fuzzer log indicates that the sample triggers the problem.

**Problem Description:**  

Type of crash  

render tab

[8800:8796:0505/104019.390:FATAL:casting.h(126)] Security DCHECK failed: IsA<Derived>(from).  

Backtrace:  

base::debug::CollectStackTrace [0x00007FFEA3646E62+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace\_win.cc:305)  

base::debug::StackTrace::StackTrace [0x00007FFEA606EADA+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace.cc:218)  

logging::LogMessage::~LogMessage [0x00007FFEA348D9AA+762] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:601)  

blink::VisualViewport::StartTrackingPinchStats [0x00007FFEA8B6DA72+482] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\visual\_viewport.cc:1040)  

blink::WebFrameWidgetImpl::HandleInputEvent [0x00007FFEA8697EDC+588] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\frame\web\_frame\_widget\_impl.cc:2457)  

blink::WidgetBaseInputHandler::HandleInputEvent [0x00007FFEAB8AE4CA+2938] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\widget\_base\_input\_handler.cc:435)  

blink::WidgetInputHandlerManager::HandleInputEvent [0x00007FFEAB8506C1+625] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\widget\_input\_handler\_manager.cc:305)  

blink::MainThreadEventQueue::HandleEventOnMainThread [0x00007FFEAB899E36+534] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:685)  

blink::QueuedWebInputEvent::Dispatch [0x00007FFEAB89AD26+550] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:156)  

blink::MainThreadEventQueue::DispatchEvents [0x00007FFEAB8982B4+1700] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:462)  

base::TaskAnnotator::RunTaskImpl [0x00007FFEA35AA4B5+933] (C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl [0x00007FFEA6473756+1206] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:385)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork [0x00007FFEA6472D67+407] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:290)  

base::MessagePumpDefault::Run [0x00007FFEA644FE4B+379] (C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_default.cc:39)  

base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run [0x00007FFEA6474F11+753] (C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:497)  

base::RunLoop::Run [0x00007FFEA351CA98+1304] (C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:143)  

content::RendererMain [0x00007FFEA5F3AF67+2723] (C:\b\s\w\ir\cache\builder\src\content\renderer\renderer\_main.cc:290)  

content::RunOtherNamedProcessTypeMain [0x00007FFEA314704C+1273] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:701)  

content::ContentMainRunnerImpl::Run [0x00007FFEA3148C88+1148] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1040)  

content::RunContentProcess [0x00007FFEA314567C+3403] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:407)  

content::ContentMain [0x00007FFEA3145E05+407] (C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:435)  

ChromeMain [0x00007FFE97FF14CC+968] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177)  

MainDllLoader::Launch [0x00007FF7D5BA5B17+945] (C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:167)  

main [0x00007FF7D5BA2B60+6898] (C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382)  

\_\_scrt\_common\_main\_seh [0x00007FF7D5F9FE9C+268] (d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288)  

BaseThreadInitThunk [0x00007FFF2EB97034+20]  

RtlUserThreadStart [0x00007FFF309C2651+33]  

Task trace:  

Backtrace:  

blink::MainThreadEventQueue::QueueEvent [0x00007FFEAB89674C+1484] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\main\_thread\_event\_queue.cc:624)  

mojo::Connector::PostDispatchNextMessageFromPipe [0x00007FFEA38A0264+390] (C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:581)  

mojo::SimpleWatcher::ArmOrNotify [0x00007FFEA38F3010+664] (C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:238)  

blink::WidgetInputHandlerManager::AddInterface [0x00007FFEAB84FB08+1320] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\platform\widget\input\widget\_input\_handler\_manager.cc:273)  

IPC::`anonymous namespace'::ChannelAssociatedGroupController::Accept [0x00007FFEA41C19C9+2731] (C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:952)

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 8.8 KB)
- [fuzz-00003.html](attachments/fuzz-00003.html) (text/plain, 3.6 KB)

## Timeline

### dt...@chromium.org (2022-05-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>Input]

### am...@chromium.org (2022-06-14)

Due to an issue with the monorail wizard workflow, this issue was not originally labeled as a security bug and, therefore, this issue did not make it to the security team bug queue for triage. This wizard workflow issue was just discovered today, updating accordingly now. 

Setting FoundIn-102 as reported above, but is also now the oldest active release channel so no need to set back further. 

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5135144004550656.

### cl...@chromium.org (2022-06-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6202194974146560.

### xi...@chromium.org (2022-06-16)

I'm not able to reproduce this crash. +bokan@, could you check if this is already fixed in https://crbug.com/1316535? Marking the severity as low, but it can be marked as non-security bug if this doesn't have security implication.

### bo...@chromium.org (2022-06-21)

Hmm, https://crbug.com/chromium/1316535 would indeed have produced this stack. OTOH, I believe that would have required the test case to have a <fencedframe> or <portal> element in it and, if the original report is accurate, the included test case doesn't have either. Certainly, my fix in 1316535 would only affect fencedframes. Is it possible the test case there isn't the right one?

The only other possibility is if the Widget's main frame is speculative (but then we shouldn't get an input event for it? Could that happen?) or if the main frame has been swapped out (but I believe we delete it immediately in that case so it shouldn't get a chance to process any queued input).

+dtapuska@ who has a better understanding of widget/frame lifetimes to double-check my reasoning.

### dt...@chromium.org (2022-06-21)

This smells very similiar to https://crbug.com/chromium/1139104 where we had a speculative frame get compositing events before it swapped. I'd expect the browser wouldn't be injecting input, but wonder if perhaps some synthetic input on the renderer side causes it to trip up. Unfortunately we never fixed 1139104 because the feature that triggered it was disabled.

What feature flags is this fuzzer running with? 

### bo...@chromium.org (2022-07-18)

> What feature flags is this fuzzer running with?

  "switch-30" = "--disable-features=Translate"
  "switch-29" = "--enable-features=BlockInsecurePrivateNetworkRequests,BlockInsec"
  "switch-28" = "--field-trial-handle=1864,i,13716202190706430380,395537856116238"
  "switch-27" = "--mojo-platform-channel-handle=3652"
  "switch-26" = "--launch-time-ticks=479065011426"
  "switch-25" = "--renderer-client-id=17"
  "switch-24" = "--enable-main-frame-before-activation"
  "switch-23" = "--num-raster-threads=4"
  "switch-22" = "--device-scale-factor=1"
  "switch-21" = "--lang=en-US"
  "switch-20" = "--video-capture-use-gpu-memory-buffer"
  "switch-19" = "--enable-blink-features=IdleDetection,MojoJS,MojoJSTest"
  "switch-18" = "--disable-gpu-compositing"
  "switch-17" = "--js-flags=--expose-gc --allow-natives-syntax"
  "switch-16" = "--use-fake-ui-for-media-stream"
  "switch-15" = "--remote-debugging-port=0"
  "switch-14" = "--force-color-profile=srgb"
  "switch-13" = "--file-url-path-alias=/gen=D:\chrome_asan\asan-win32-release_x64"
  "switch-12" = "--enable-blink-test-features"
  "switch-11" = "--enable-experimental-web-platform-features"
  "switch-10" = "--enable-automation"
  "switch-9" = "--disable-breakpad"
  "switch-8" = "--disable-background-timer-throttling"
  "switch-7" = "--autoplay-policy=no-user-gesture-required"
  "switch-6" = "--no-sandbox"
  "switch-5" = "--disable-in-process-stack-traces"
  "switch-4" = "--enable-experimental-extension-apis"
  "switch-3" = "--display-capture-permissions-policy-allowed"
  "switch-2" = "--disable-client-side-phishing-detection"
  "switch-1" = "--user-data-dir=TMP/auto_test_task_6"

Dave: It looks like the task runner and queue for a widget are destroyed in WidgetSchedulerImpl::Shutdown[1] which is posted asynchronously from WidgetBase::Shutdown[2]. [2]  happens when we detach the frame during a Swap. Is there anything that prevents running input tasks (e.g. flush the main thread event queue) between [2] and [1]? There's some comments above [2] that imply that we might still be posting tasks to the input queue after shutdown...

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/scheduler/main_thread/widget_scheduler_impl.cc;l=40;drc=97f94c6631e327c2c1a9891774b44fbba9e8e3bf
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/widget/widget_base.cc;l=295;drc=97f94c6631e327c2c1a9891774b44fbba9e8e3bf



### dt...@chromium.org (2022-07-18)

ClearClient gets call synchronously, so the input event queue can't call back to the widget:

https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/widget/input/main_thread_event_queue.cc;drc=97f94c6631e327c2c1a9891774b44fbba9e8e3bf;l=719

### bo...@chromium.org (2022-07-21)

Ah, thanks - yeah, I think that rules out post shutdown input.

Taking a look at the report, it looks like we have a stack for where the task was queued:

	blink::MainThreadEventQueue::QueueEvent
	mojo::Connector::PostDispatchNextMessageFromPipe
	mojo::SimpleWatcher::ArmOrNotify
	blink::WidgetInputHandlerManager::AddInterface

AddInterface is called via Mojo from RenderFrameCreated so IIUC the widget can be connected for a provisional frame? This means if at input were to be queued by the browser it would get dispatched while the frame was provisional (the frame exits the provisional state at navigation commit). From local testing I can reproduce the widget being initialized and AddInterface called while the frame is provisional

I guess the only question is whether the browser would route input to the new widget. I would assume the widget can't be targeted until it produces a frame but the targeting logic is rather complex so I wouldn't be surprised if there's a path to queuing input on a speculative widget. I wonder if we should just avoid dispatching events in the renderer while the frame's widget is provisional?



### bo...@chromium.org (2022-07-28)

https://crbug.com/chromium/1347644 has a repro I was able to look at - it does seem like the browser can sometimes dispatch events to a provisional frame; that seems problematic.

I think it'd make sense to just drop events dispatched to a provisional frame but it'd be useful to also have a DCHECK on the browser side to prevent browser code from doing that since I think this is a bug.

IIUC, a provisional frame is created for a speculative RenderFrameHost...can we tell from a RenderWidgetHost that its owning RenderFrameHost is speculative? It seems we don't have a reference to the RenderFrameHost...

### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/05a0d99c971514184d92dd261304cf8c4fe98cac

commit 05a0d99c971514184d92dd261304cf8c4fe98cac
Author: David Bokan <bokan@chromium.org>
Date: Thu Jul 28 18:09:13 2022

Prevent handling input for provisional frames

Bug: 1347644,1322812
Change-Id: Ifd60f6aa593ce23ca6cbb65552fc9fb8f8690035
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3791883
Commit-Queue: David Bokan <bokan@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1029361}

[modify] https://crrev.com/05a0d99c971514184d92dd261304cf8c4fe98cac/third_party/blink/renderer/core/frame/web_frame_widget_impl.cc


### bo...@chromium.org (2022-07-28)

#14 will prevent execution from getting to the bad cast in production so we can close this. There's probably bugs on the browser side if we're dispatching events to an uncommitted frame but we'll track that separately in https://crbug.com/chromium/1347644.

Thanks for the report!

### [Deleted User] (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-17)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. Thank you for reporting this issue to us -- nice work! 

### am...@google.com (2022-08-19)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-27)

elevated to medium severity; there also seem to be many flags that must be enabled to trigger this issue, so potentially this should have been SI-None, that is inconsequential at this point. 

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-11-04)

This issue was migrated from crbug.com/chromium/1322812?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059571)*
