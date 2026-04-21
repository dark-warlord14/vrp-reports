# Security: heap-use-after-free on chrome/browser/ui/views/tabs/tab_strip.cc:220:5

| Field | Value |
|-------|-------|
| **Issue ID** | [40065546](https://issues.chromium.org/issues/40065546) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux |
| **Reporter** | rh...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2023-06-09 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**  

Tested on Linux, chromiumos and lacros

1. Build under Asan and host the poc and lunch chromium with gesture.
2. Wait until page has fully loaded and pick one tab, grab one out and hold the pointer.
3. After first tab closes, release the pointer.

# **Problem Description:**

==105693==ERROR: AddressSanitizer: heap-use-after-free on address 0x51900080fa88 at pc 0x5620e78dfb99 bp 0x7ffcbc391010 sp 0x7ffcbc391008  

READ of size 8 at 0x51900080fa88 thread T0 (chrome)  

#0 0x5620e78dfb98 in GetForDereference base/allocator/partition\_allocator/pointers/raw\_ptr.h:1038:48  

#1 0x5620e78dfb98 in operator-> base/allocator/partition\_allocator/pointers/raw\_ptr.h:806:12  

#2 0x5620e78dfb98 in TabStrip::TabDragContextImpl::OnGestureEvent(ui::GestureEvent\*) chrome/browser/ui/views/tabs/tab\_strip.cc:220:5  

#3 0x5620d3ffa064 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:187:12  

#4 0x5620d3ff8bfa in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:136:5  

#5 0x5620d3ff8253 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:82:14  

#6 0x5620d3ff7d8c in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:54:15  

#7 0x5620d84dfff0 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:72:19  

#8 0x5620d8504c23 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#9 0x5620d8504870 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:143:12  

#10 0x5620dcc231a7 in views::DesktopNativeWidgetAura::OnGestureEvent(ui::GestureEvent\*) ui/views/widget/desktop\_aura/desktop\_native\_widget\_aura.cc:1326:30  

#11 0x5620d3ffa064 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ui/events/event\_dispatcher.cc:187:12  

#12 0x5620d3ff8bfa in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:136:5  

#13 0x5620d3ff8253 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:82:14  

#14 0x5620d3ff7d8c in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:54:15  

#15 0x5620d84cf19b in aura::WindowEventDispatcher::ProcessGestures(aura::Window\*, std::\_\_Cr::vector<std::\_\_Cr::unique\_ptr<ui::GestureEvent, std::\_\_Cr::default\_delete[ui::GestureEvent](javascript:void(0);)>, std::\_\_Cr::allocator<std::\_\_Cr::unique\_ptr<ui::GestureEvent, std::\_\_Cr::default\_delete[ui::GestureEvent](javascript:void(0);)>>>) ui/aura/window\_event\_dispatcher.cc:351:15  

#16 0x5620d84d6d4d in aura::WindowEventDispatcher::PostDispatchEvent(ui::EventTarget\*, ui::Event const&) ui/aura/window\_event\_dispatcher.cc:601:19  

#17 0x5620d3ff7de4 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ui/events/event\_dispatcher.cc:58:15  

#18 0x5620d84dfff0 in ui::EventProcessor::OnEventFromSource(ui::Event\*) ui/events/event\_processor.cc:72:19  

#19 0x5620d8504c23 in ui::EventSource::DeliverEventToSink(ui::Event\*) ui/events/event\_source.cc:118:16  

#20 0x5620d8504870 in ui::EventSource::SendEventToSinkFromRewriter(ui::Event const\*, ui::EventRewriter const\*) ui/events/event\_source.cc:143:12  

#21 0x5620dcc0e465 in aura::WindowTreeHostPlatform::DispatchEvent(ui::Event\*) ui/aura/window\_tree\_host\_platform.cc:236:38  

#22 0x5620dcc34ac4 in views::DesktopWindowTreeHostLinux::DispatchEvent(ui::Event\*) ui/views/widget/desktop\_aura/desktop\_window\_tree\_host\_linux.cc:219:29  

#23 0x5620c2261042 in Invoke<void (ui::PlatformWindowDelegate::\*)(ui::Event \*), ui::PlatformWindowDelegate \*, ui::Event \*> base/functional/bind\_internal.h:746:12  

#24 0x5620c2261042 in MakeItSo<void (ui::PlatformWindowDelegate::\*)(ui::Event \*), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> >, ui::Event \*> base/functional/bind\_internal.h:925:12  

#25 0x5620c2261042 in RunImpl<void (ui::PlatformWindowDelegate::\*)(ui::Event \*), std::\_\_Cr::tuple<base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0> >, 0UL> base/functional/bind\_internal.h:1025:12  

#26 0x5620c2261042 in base::internal::Invoker<base::internal::BindState<void (ui::PlatformWindowDelegate::\*)(ui::Event\*), base::internal::UnretainedWrapper<ui::PlatformWindowDelegate, base::unretained\_traits::MayNotDangle, (base::RawPtrTraits)0>>, void (ui::Event\*)>::RunOnce(base::internal::BindStateBase\*, ui::Event\*) base/functional/bind\_internal.h:976:12  

#27 0x5620d4008ef2 in Run base/functional/callback.h:152:12  

#28 0x5620d4008ef2 in ui::DispatchEventFromNativeUiEvent(ui::Event\* const&, base::OnceCallback<void (ui::Event\*)>) ui/events/ozone/events\_ozone.cc:41:25  

#29 0x5620c232dae3 in ui::X11Window::DispatchUiEvent(ui::Event\*, x11::Event const&) ui/ozone/platform/x11/x11\_window.cc:1387:3  

#30 0x5620c232d12f in ui::X11Window::DispatchEvent(ui::Event\* const&) ui/ozone/platform/x11/x11\_window.c

**Additional Comments:**  

bisect on linux: <https://chromium.googlesource.com/chromium/src/+log/f104ad2af3e5df75c86f9401a51b6eb52e9006ce..66d6e7cb4ff352758a0bb5500e54895732feba2d>  

bisect on cros:  

<https://chromium.googlesource.com/chromium/src/+log/5ddda8a483c5a4abf1d0f8fca51b637c57d5dd5b..4b1c308a1fc5e7d63663059107d69e044cfa30a2>

maybe the culprit: <https://chromium-review.googlesource.com/c/chromium/src/+/3577457>

screencast linux: <https://drive.google.com/file/d/1a5u2ZrBwSPDnVMgA3YMUBcSVA3NGiTpj/view?usp=sharing>  

screencast cros: <https://drive.google.com/file/d/194YrAR6LiCDPXC1-t-4iUcAhlTotGrG8/view?usp=sharing>

\*\*Chrome version: \*\* 116.0.5821.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [tab-poc.html](attachments/tab-poc.html) (text/plain, 490 B)
- [asan.log](attachments/asan.log) (text/plain, 20.7 KB)
- [test-2023-06-09_11.10.54.mp4](attachments/test-2023-06-09_11.10.54.mp4) (video/mp4, 616.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 527 B)
- [poc.html](attachments/poc.html) (text/plain, 479 B)

## Timeline

### rh...@gmail.com (2023-06-09)

uploading asan.log

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-06-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5940601479168000.

### ar...@google.com (2023-06-09)

Thanks for the bug report!

- Security_Severity-High: For me this is "Memory corruption in the browser process that requires specific user interaction"
- Foundin-105: assuming this was caused by https://chromium-review.googlesource.com/c/chromium/src/+/3577457


Note: This might likely be protected by MiraclePtr starting from M115
https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-miracleptr
I would need to learn how to check for this, and reassess severity. However, the bug started affecting users in M115

[Monorail components: UI>Browser>TopChrome>TabStrip>TabGroups]

### ar...@google.com (2023-06-09)

Sorry typo in the previous message. I meant: "..started affecting users in M105"
https://chromiumdash.appspot.com/commit/4b1c308a1fc5e7d63663059107d69e044cfa30a2

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### ar...@google.com (2023-06-09)

Note: I wasn't able to reproduce 116.0.5817.0 ASAN build.

Did I miss something?

### rh...@gmail.com (2023-06-09)

Hi,

Sorry if you weren't able to repro this bug. On my environment:

running on linux: asan-linux-release-1155224$ ASAN_OPTIONS="external_symbolizer_path=/home/dadang/chromium/src/third_party/llvm-build/Release+Asserts/bin/llvm-symbolizer:symbolize=1" ./chrome --user-data-dir=/tmp/pre-chrome-linux2 --touch-devices=9 --disable-popup-blocking http://localhost:8000/tab-poc.html

running on cros prebuilt asan:  $cros/asan-linux-release-1155151$ ./chrome --user-data-dir=/tmp/pre-chrome --bwsi --incognito --login-user='$guest' --login-profile=user --touch-devices=9 --force-show-cursor --disable-popup-blocking --ash-host-window-bounds=1920x1080*1.25  http://localhost:8000/tab-poc.html

download cros-prebuilt-asan with: gsutil cp gs://chromium-browser-asan/linux-release-chromeos/asan-linux-release-1155151.zip $folder

so both repro step is required to use gesture(not mouseEvent) and running from command line, on my test above was "--touch-devices=9",  and you can find on your device with `$xinput` and use the mouse ID pointer for --touch-devices=ID

hope this helps


### [Deleted User] (2023-06-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-09)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-06-09)

(I am a bot: this is an auto-cc on a security bug)

### es...@google.com (2023-06-13)

Taylor/David, handing off my bug triage rotation to Mickey. But wanted to surface this P1 bug which requires some investigation. Thanks.

### [Deleted User] (2023-06-23)

tbergquist: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tb...@chromium.org (2023-06-26)

Okay, can I double check the repro instructions with you?

I'm reading them as:
1. Start with one tab: poc
2. Wait for poc to create tab 1 and tab 2
3. touch and hold tab 1, drag it out into another window
4. Wait for poc tab to close
5. lift finger off tab 1 (this ends the drag session)
6. Wait for tab 1 and tab 2 to close
7. Observe a UAF when tab 1 closes

Is that right? In particular it isn't clear to me when to release the drag - after just the poc tab closes or after one of the created tabs closes. I.e. do I have steps 5 and 6 reversed?

The UAF appears to happen when TabDragContextImpl handles a gesture event after its associated tab_strip_ has already been destroyed (in step 6). It's not clear to me what that gesture event even is, since the drag is already over by the time any browsers are destroyed, which is why I think I might have the repro wrong.

Please clarify the repro steps for me - in the meantime, I'll set up my linux cloudtop with an ASAN build to test this myself.

### rh...@gmail.com (2023-06-27)

Hi Taylor,

The steps you provided is correct. Were you able to repro this bug?

>>Is that right? In particular it isn't clear to me when to release the drag - after just the poc tab closes or after one of the created tabs closes. I.e. do I have steps 5 and 6 reversed?

let say, the poc spawned 2 tabs at that time, and we drag the second tab and wait the first tab closes.

Sorry, I can't retest this bug at this moment. I'm just taking off work and will be back after mid July. I have only mac on handy.


### rh...@gmail.com (2023-06-27)

Sorry I didn't read carefully. This is for the update.

On my screen cast on https://crbug.com/chromium/1453465#c0:1. Start with one tab: poc
2. Wait for poc to create tab 1 and tab 2
>>3. touch and hold tab 1 , drag it out into another window
3. Touch and hold tab 2, drag it out into another window

4. Wait for poc tab to close
>>5. lift finger off tab 1 (this ends the drag session)
5. Wait for tab 1 and other tabs to close

>>6. Wait for tab 1 and tab 2 to close
6. lift finger off tab 2 (this ends the drag session)
7. Observe a UAF when tab 1 closes

That's mean your statement "I.e. do I have steps 5 and 6 reversed?" Is correct.

I also would like to confirm, on the poc spawns 5 tabs. Anyway thank you for looking this issue.




### tb...@chromium.org (2023-06-27)

Okay, I managed to reproduce with this reduced repro:


- Touch and hold tab 2
- Drag tab 2 into another window
- Wait for tab 1 to close
- Release tab 2
- Wait for tab 2 to close (observe in the meantime that you are still dragging the window!)
- Observe UAF

### tb...@chromium.org (2023-06-28)

The UAF happens when the TabDragContext is asked to handle an event after it has been destroyed.

I'm starting to assemble a picture of what might be happening here. Context on tab dragging:
- Tab dragging captures input events and forwards them to the current TabDragContext - this could very plausibly send events to a dead TabDragContext if the capturing is done incorrectly
- Capturing is different on linux/chrome os than on Mac and Windows
- Capturing is different with touch than non-touch
- SetCapture and ReleaseCapture happen in multiple places, for complex, platform-dependent reasons, in TabDragController
- There are no universal structural guarantees that capture will be released, once taken. The closest thing is, in TabDragController's destructor, capture is released if the input method is touch.

The fact that releasing the mouse doesn't end the drag suggests that perhaps capture is not transferred correctly as part of the drag out of window operation - then the end gesture event would get sent to the wrong place, and the drag would not end.

Even if that is the issue, fixing it would still leave us with this underlying risk of dangling capture. We would still need some more robust method for tracking capture set and release, something that gives us stronger guarantees and is easy to understand. That's a challenging change - replacing the current morass of set/release calls will require a deep understanding of capture behavior across every platform and input method.

A middle ground might be unconditionally releasing capture on TabDragContext destruction - it leaves us with the morass, but it does at least ensure that a dead TabDragContext won't have capture.




I'll test some of these things out on my cloudtop and figure out where to go next.

### tb...@chromium.org (2023-06-28)

Okay, scratch most of the above - releasing capture when a TabDragContext is removed from a widget does not affect the crash, the events still get sent to the freed drag context even if capture was released for that context's widget first.

I've trimmed the repro down a bit further, at least - now just one new tab is opened. Simply grab the new tab, drag it into another window, and drop it right away to trigger the bug.

### tb...@chromium.org (2023-06-29)

Okay okay okay, root cause is get!

Here's what is happening:
- Drag tab out of tabstrip
- this calls OnGestureEvent with an ET_GESTURE_SCROLL_UPDATE, which calls ContinueDrag, which ends up entering a nested event loop
- during the nested event loop, the poc tab is closed, which destroys the first window (the one in the parent event loop)
- << this part is still a bit of a mystery to me >>
- at some point after closing the last tab, we pop back out of the nested event loop back into the parent event loop
- now the TabDragContextImpl and TabStrip in the parent loop stack frame are no longer alive

So it's only the one case - ET_GESTURE_SCROLL_UPDATE leading to ContinueDrag - where such a UAF is possible. Easy and correct fix is to just handle the case where ContinueDrag() destroys the tabstrip with an early return. Probably some other code health-y changes will make sense here to make this mistake harder to make in the future.

### tb...@chromium.org (2023-06-29)

Fix is out for review, adding Darryl to CC

### gi...@appspot.gserviceaccount.com (2023-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/63d6b8ba8126b16215d33670df8c67dcbc6c9bef

commit 63d6b8ba8126b16215d33670df8c67dcbc6c9bef
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Fri Jun 30 00:49:39 2023

Fix UAF when exiting a nested run loop in TabDragContextImpl::OnGestureEvent.

OnGestureEvent may call ContinueDrag, which may run a nested run loop. After the nested run loop returns, multiple seconds of time may have passed, and the world may be in a very different state; in particular, the window that contains this TabDragContext may have closed.

This CL checks if this has happened, and returns early in that case.

Bug: 1453465
Change-Id: I6095c0afeb5aa5f422717f1bbd93b96175e52afa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4657527
Reviewed-by: Darryl James <dljames@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1164449}

[modify] https://crrev.com/63d6b8ba8126b16215d33670df8c67dcbc6c9bef/chrome/browser/ui/views/tabs/tab_strip.cc
[modify] https://crrev.com/63d6b8ba8126b16215d33670df8c67dcbc6c9bef/chrome/browser/ui/views/tabs/tab_slot_controller.h
[modify] https://crrev.com/63d6b8ba8126b16215d33670df8c67dcbc6c9bef/chrome/browser/ui/views/tabs/fake_tab_slot_controller.cc
[modify] https://crrev.com/63d6b8ba8126b16215d33670df8c67dcbc6c9bef/chrome/browser/ui/views/tabs/fake_tab_slot_controller.h
[modify] https://crrev.com/63d6b8ba8126b16215d33670df8c67dcbc6c9bef/chrome/browser/ui/views/tabs/tab_strip.h


### rh...@gmail.com (2023-06-30)

Taylor,

Thank you very much for fixing this bug. I Appreciate much!

### tb...@chromium.org (2023-07-05)

[Empty comment from Monorail migration]

### tb...@chromium.org (2023-07-05)

Thanks for the repro! It was a bit of a tricky one, nice repro helped. :)

### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-06)

Requesting merge to stable M114 because latest trunk commit (1164449) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1164449) appears to be after beta branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1164449) appears to be after dev branch point (1160321).

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

Merge review required: M114 is already shipping to stable.

Merge review required: M115 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-10)

[Comment Deleted]

### am...@chromium.org (2023-07-10)

116 merge approved, please merge this fix to branch 5845 by EOD Wednesday, 12 July so this fix can be included in the next M116 dev on Thursday 

due to Stable RC deadlines and the impending Extended Stable cut + given that this is not a remove exploitable security bug and is mitigated by user interaction, I'd like to hold off merge approval to M115 and M114 until next week; re-adding merge review labels so this can return to the queue but not be approved until next week 

### am...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/52a4a302b67a13863a11dbf7868b219ba1ccbb31

commit 52a4a302b67a13863a11dbf7868b219ba1ccbb31
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue Jul 11 00:36:09 2023

Fix UAF when exiting a nested run loop in TabDragContextImpl::OnGestureEvent.

OnGestureEvent may call ContinueDrag, which may run a nested run loop. After the nested run loop returns, multiple seconds of time may have passed, and the world may be in a very different state; in particular, the window that contains this TabDragContext may have closed.

This CL checks if this has happened, and returns early in that case.

(cherry picked from commit 63d6b8ba8126b16215d33670df8c67dcbc6c9bef)

Bug: 1453465
Change-Id: I6095c0afeb5aa5f422717f1bbd93b96175e52afa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4657527
Reviewed-by: Darryl James <dljames@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/heads/main@{#1164449}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4676144
Reviewed-by: Shibalik Mohapatra <shibalik@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1448}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/52a4a302b67a13863a11dbf7868b219ba1ccbb31/chrome/browser/ui/views/tabs/tab_strip.cc
[modify] https://crrev.com/52a4a302b67a13863a11dbf7868b219ba1ccbb31/chrome/browser/ui/views/tabs/tab_slot_controller.h
[modify] https://crrev.com/52a4a302b67a13863a11dbf7868b219ba1ccbb31/chrome/browser/ui/views/tabs/fake_tab_slot_controller.cc
[modify] https://crrev.com/52a4a302b67a13863a11dbf7868b219ba1ccbb31/chrome/browser/ui/views/tabs/fake_tab_slot_controller.h
[modify] https://crrev.com/52a4a302b67a13863a11dbf7868b219ba1ccbb31/chrome/browser/ui/views/tabs/tab_strip.h


### gi...@appspot.gserviceaccount.com (2023-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/81892592667ab061315fb7ab52981a293c47c2c8

commit 81892592667ab061315fb7ab52981a293c47c2c8
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue Jul 11 01:10:05 2023

Fix UAF when exiting a nested run loop in TabDragContextImpl::OnGestureEvent.

OnGestureEvent may call ContinueDrag, which may run a nested run loop. After the nested run loop returns, multiple seconds of time may have passed, and the world may be in a very different state; in particular, the window that contains this TabDragContext may have closed.

This CL checks if this has happened, and returns early in that case.

(cherry picked from commit 63d6b8ba8126b16215d33670df8c67dcbc6c9bef)

Bug: 1453465
Change-Id: I6095c0afeb5aa5f422717f1bbd93b96175e52afa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4657527
Reviewed-by: Darryl James <dljames@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/heads/main@{#1164449}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4674678
Reviewed-by: Shibalik Mohapatra <shibalik@chromium.org>
Cr-Commit-Position: refs/branch-heads/5790@{#1565}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/81892592667ab061315fb7ab52981a293c47c2c8/chrome/browser/ui/views/tabs/tab_strip.cc
[modify] https://crrev.com/81892592667ab061315fb7ab52981a293c47c2c8/chrome/browser/ui/views/tabs/tab_slot_controller.h
[modify] https://crrev.com/81892592667ab061315fb7ab52981a293c47c2c8/chrome/browser/ui/views/tabs/fake_tab_slot_controller.cc
[modify] https://crrev.com/81892592667ab061315fb7ab52981a293c47c2c8/chrome/browser/ui/views/tabs/fake_tab_slot_controller.h
[modify] https://crrev.com/81892592667ab061315fb7ab52981a293c47c2c8/chrome/browser/ui/views/tabs/tab_strip.h


### gi...@appspot.gserviceaccount.com (2023-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c60a1ab717c77636508995c044a6c0e8086ac011

commit c60a1ab717c77636508995c044a6c0e8086ac011
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue Jul 11 01:32:22 2023

Fix UAF when exiting a nested run loop in TabDragContextImpl::OnGestureEvent.

OnGestureEvent may call ContinueDrag, which may run a nested run loop. After the nested run loop returns, multiple seconds of time may have passed, and the world may be in a very different state; in particular, the window that contains this TabDragContext may have closed.

This CL checks if this has happened, and returns early in that case.

(cherry picked from commit 63d6b8ba8126b16215d33670df8c67dcbc6c9bef)

Bug: 1453465
Change-Id: I6095c0afeb5aa5f422717f1bbd93b96175e52afa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4657527
Reviewed-by: Darryl James <dljames@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/heads/main@{#1164449}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4676126
Reviewed-by: Shibalik Mohapatra <shibalik@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#410}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/c60a1ab717c77636508995c044a6c0e8086ac011/chrome/browser/ui/views/tabs/tab_strip.cc
[modify] https://crrev.com/c60a1ab717c77636508995c044a6c0e8086ac011/chrome/browser/ui/views/tabs/tab_slot_controller.h
[modify] https://crrev.com/c60a1ab717c77636508995c044a6c0e8086ac011/chrome/browser/ui/views/tabs/fake_tab_slot_controller.cc
[modify] https://crrev.com/c60a1ab717c77636508995c044a6c0e8086ac011/chrome/browser/ui/views/tabs/fake_tab_slot_controller.h
[modify] https://crrev.com/c60a1ab717c77636508995c044a6c0e8086ac011/chrome/browser/ui/views/tabs/tab_strip.h


### gi...@appspot.gserviceaccount.com (2023-07-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6ebfa5695a1388ef64f6c2d9c3366e21ad48ce44

commit 6ebfa5695a1388ef64f6c2d9c3366e21ad48ce44
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Wed Jul 12 19:38:29 2023

Revert "Fix UAF when exiting a nested run loop in TabDragContextImpl::OnGestureEvent."

This reverts commit 52a4a302b67a13863a11dbf7868b219ba1ccbb31.

Reason for revert: amyressler@: due to Stable RC deadlines and the impending Extended Stable cut + given that this is not a remove exploitable security bug and is mitigated by user interaction, I'd like to hold off merge approval to M115 and M114 until next week

Original change's description:
> Fix UAF when exiting a nested run loop in TabDragContextImpl::OnGestureEvent.
>
> OnGestureEvent may call ContinueDrag, which may run a nested run loop. After the nested run loop returns, multiple seconds of time may have passed, and the world may be in a very different state; in particular, the window that contains this TabDragContext may have closed.
>
> This CL checks if this has happened, and returns early in that case.
>
> (cherry picked from commit 63d6b8ba8126b16215d33670df8c67dcbc6c9bef)
>
> Bug: 1453465
> Change-Id: I6095c0afeb5aa5f422717f1bbd93b96175e52afa
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4657527
> Reviewed-by: Darryl James <dljames@chromium.org>
> Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
> Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
> Cr-Original-Commit-Position: refs/heads/main@{#1164449}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4676144
> Reviewed-by: Shibalik Mohapatra <shibalik@chromium.org>
> Cr-Commit-Position: refs/branch-heads/5735@{#1448}
> Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

Bug: 1453465
Change-Id: I49d98e9e92c60a0cfbdd31a4f5c87a8dd01b85a2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4681901
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Shibalik Mohapatra <shibalik@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1459}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/6ebfa5695a1388ef64f6c2d9c3366e21ad48ce44/chrome/browser/ui/views/tabs/tab_strip.cc
[modify] https://crrev.com/6ebfa5695a1388ef64f6c2d9c3366e21ad48ce44/chrome/browser/ui/views/tabs/tab_slot_controller.h
[modify] https://crrev.com/6ebfa5695a1388ef64f6c2d9c3366e21ad48ce44/chrome/browser/ui/views/tabs/fake_tab_slot_controller.cc
[modify] https://crrev.com/6ebfa5695a1388ef64f6c2d9c3366e21ad48ce44/chrome/browser/ui/views/tabs/fake_tab_slot_controller.h
[modify] https://crrev.com/6ebfa5695a1388ef64f6c2d9c3366e21ad48ce44/chrome/browser/ui/views/tabs/tab_strip.h


### am...@google.com (2023-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-13)

Congratulations! The VRP Panel has decided to award you $2,000 for this highly mitigated security bug. Thank you for your efforts and reporting this issue to us. 

### rh...@gmail.com (2023-07-14)

Sorry Amy,  is there any bisect bonus for this bug?

### am...@google.com (2023-07-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-14)

Yes, apologies that I did not break that out. This reward amount includes the reward for the bisect you provided. 

### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-19)

Thank you for your revert of the M114 merge last week.
Merge review for M114 approval -- please go ahead and merge this fix to branch 5735 at your earliest convenience. Thank you! 

### am...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/47eca93b238e63460a78d6e13896ae675b628e4f

commit 47eca93b238e63460a78d6e13896ae675b628e4f
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Sat Jul 29 16:37:40 2023

Reland "Fix UAF when exiting a nested run loop in TabDragContextImpl::OnGestureEvent."

This is a reland of commit 52a4a302b67a13863a11dbf7868b219ba1ccbb31

Original change's description:
> Fix UAF when exiting a nested run loop in TabDragContextImpl::OnGestureEvent.
>
> OnGestureEvent may call ContinueDrag, which may run a nested run loop. After the nested run loop returns, multiple seconds of time may have passed, and the world may be in a very different state; in particular, the window that contains this TabDragContext may have closed.
>
> This CL checks if this has happened, and returns early in that case.
>
> (cherry picked from commit 63d6b8ba8126b16215d33670df8c67dcbc6c9bef)
>
> Bug: 1453465
> Change-Id: I6095c0afeb5aa5f422717f1bbd93b96175e52afa
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4657527
> Reviewed-by: Darryl James <dljames@chromium.org>
> Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
> Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
> Cr-Original-Commit-Position: refs/heads/main@{#1164449}
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4676144
> Reviewed-by: Shibalik Mohapatra <shibalik@chromium.org>
> Cr-Commit-Position: refs/branch-heads/5735@{#1448}
> Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

Bug: 1453465
Change-Id: Ic2254a6d9df7c9df0d5ef9195968871590804ecd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4728330
Reviewed-by: David Pennington <dpenning@chromium.org>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1532}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/47eca93b238e63460a78d6e13896ae675b628e4f/chrome/browser/ui/views/tabs/tab_strip.cc
[modify] https://crrev.com/47eca93b238e63460a78d6e13896ae675b628e4f/chrome/browser/ui/views/tabs/tab_slot_controller.h
[modify] https://crrev.com/47eca93b238e63460a78d6e13896ae675b628e4f/chrome/browser/ui/views/tabs/fake_tab_slot_controller.cc
[modify] https://crrev.com/47eca93b238e63460a78d6e13896ae675b628e4f/chrome/browser/ui/views/tabs/fake_tab_slot_controller.h
[modify] https://crrev.com/47eca93b238e63460a78d6e13896ae675b628e4f/chrome/browser/ui/views/tabs/tab_strip.h


### am...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1453465?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065546)*
