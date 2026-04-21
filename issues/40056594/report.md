# Google Chrome WebRTC addIceCandidate use after free vulnerability (TALOS-2021-1348)

| Field | Value |
|-------|-------|
| **Issue ID** | [40056594](https://issues.chromium.org/issues/40056594) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ht...@chromium.org |
| **Created** | 2021-07-19 |
| **Bounty** | $22,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15

Steps to reproduce the problem:
While executing the attached PoC testcase on Windows 10 x64 machine with ASAN enabled, Chrome crashes inside TrackAddIceCandidate from PeerConnectionTracker. Snippet of this function is as follows:

     1:      void PeerConnectionTracker::TrackAddIceCandidate(
     2:          RTCPeerConnectionHandler* pc_handler,
     3:          RTCIceCandidatePlatform* candidate,
     4:          Source source,
     5:          bool succeeded) {
     6:      DCHECK_CALLED_ON_VALID_THREAD(main_thread_);
     7:      int id = GetLocalIDForHandler(pc_handler);
     8:      if (id == -1)
     9:          return;
    10:      String value =
    11:          "sdpMid: " + String(candidate->SdpMid()) + ", " + "sdpMLineIndex: " +
    12:          (candidate->SdpMLineIndex() ? String::Number(*candidate->SdpMLineIndex())
    13:                                      : "null") +
    14:          ", " + "candidate: " + String(candidate->Candidate());

When setting up an WebRTC session ,function, `AddIceCandidate` is used to add Interactive Connection Establishment candidates, recieved from the remote peer over signaling channle, to browser's ICE agent. 

In the supplied PoC , before adding an ICE candidate, garbage collection is forced to mark objects which can later be used because of active Promise that was called before garbage collection.
In between triggering garbage collection and function causing the reuse, allocated memory is accessed thanks to Promise using function `setLocalDescription`.
Function `setLocalDescription`  changes the local description associated with the connection which marks parts of the memory to be collected by garbage collector. Same marked memory is accessed during execution of `AddIceCandidate` which constitutes a use after free vulnerability.

With proper manipulation of Promise that is responsible for setting description `setLocalDescription` this vulnerability could lead to control over freed memory and ultimately arbitrary code execution.

### Crash Information

Command line :
    chrome.exe --js-flags=" --expose-gc"  --no-sandbox poc.html
ASAN information Windows 10 x64

    =================================================================
    ==26232==ERROR: AddressSanitizer: use-after-poison on address 0x7ef84e666428 at pc 0x7ff654dd0a45 bp 0x0003385fea80 sp 0x0003385feac8
    READ of size 8 at 0x7ef84e666428 thread T27
    ==26232==WARNING: Failed to use and restart external symbolizer!
        #0 0x7ff654dd0a44 in blink::PeerConnectionTracker::TrackAddIceCandidate C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\peer_connection_tracker.cc:987
        #1 0x7ff6516d1f5b in base::internal::Invoker<base::internal::BindState<lambda at ../../third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc:1590:7',base::WeakPtr<blink::RTCPeerConnectionHandler>,blink::CrossThreadWeakPersistent<blink::PeerConnectionTracker>,std::unique_ptr<webrtc::SessionDescriptionInterface,std::default_delete<webrtc::SessionDescriptionInterface> >,std::unique_ptr<webrtc::SessionDescriptionInterface,std::default_delete<webrtc::SessionDescriptionInterface> >,std::unique_ptr<webrtc::SessionDescriptionInterface,std::default_delete<webrtc::SessionDescriptionInterface> >,std::unique_ptr<webrtc::SessionDescriptionInterface,std::default_delete<webrtc::SessionDescriptionInterface> >,blink::CrossThreadPersistent<blink::RTCIceCandidatePlatform>,webrtc::RTCError,blink::CrossThreadPersistent<blink::RTCVoidRequest> >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:690
        #2 0x7ff64f507137 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:173
        #3 0x7ff651bcadcf in base::sequence_manager::internal::ThreadControllerImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_impl.cc:199
        #4 0x7ff651bcd953 in base::internal::Invoker<base::internal::BindState<void (base::sequence_manager::internal::ThreadControllerImpl::*)(base::sequence_manager::internal::ThreadControllerImpl::WorkType),base::WeakPtr<base::sequence_manager::internal::ThreadControllerImpl>,base::sequence_manager::internal::ThreadControllerImpl::WorkType>,void ()>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:703
        #5 0x7ff64f507137 in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:173
        #6 0x7ff651bcfb24 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:351
        #7 0x7ff651bcf1e9 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:264
        #8 0x7ff64f5a31a0 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:220
        #9 0x7ff64f5a1388 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
        #10 0x7ff651bd10c4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:460
        #11 0x7ff64f4a3833 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:133
        #12 0x7ff64f54c779 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:312
        #13 0x7ff64f54cc8e in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:383
        #14 0x7ff64f5bf66f in base::anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:111
        #15 0x7ff64f3cd7c7 in asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:279
        #16 0x7ff93f947033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
        #17 0x7ff9405a2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

    Address 0x7ef84e666428 is a wild pointer inside of access range of size 0x000000000008.
    SUMMARY: AddressSanitizer: use-after-poison C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\peerconnection\peer_connection_tracker.cc:987 in blink::PeerConnectionTracker::TrackAddIceCandidate
    Shadow bytes around the buggy address:
      0x1114c634cc30: 00 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7
      0x1114c634cc40: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00
      0x1114c634cc50: 00 00 00 00 00 00 00 00 00 f7 f7 f7 f7 f7 f7 f7
      0x1114c634cc60: f7 f7 f7 f7 f7 f7 f7 f7 f7 00 00 00 00 00 00 00
      0x1114c634cc70: 00 00 00 00 00 00 f7 00 00 00 00 00 00 00 00 00
    =>0x1114c634cc80: 00 00 00 00 f7[f7]f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
      0x1114c634cc90: f7 f7 f7 f7 f7 00 00 00 00 00 00 00 00 00 00 00
      0x1114c634cca0: 00 00 f7 00 00 00 00 00 00 00 00 f7 00 00 00 00
      0x1114c634ccb0: 00 00 00 00 00 00 f7 00 00 00 00 00 00 00 00 00
      0x1114c634ccc0: 00 00 00 00 f7 00 00 00 00 00 00 00 00 00 00 00
      0x1114c634ccd0: 00 00 00 00 f7 00 00 00 00 00 00 00 00 00 f7 00
    Shadow byte legend (one shadow byte represents 8 application bytes):
      Addressable:           00
      Partially addressable: 01 02 03 04 05 06 07
      Heap left redzone:       fa
      Freed heap region:       fd
      Stack left redzone:      f1
      Stack mid redzone:       f2
      Stack right redzone:     f3
      Stack after return:      f5
      Stack use after scope:   f8
      Global redzone:          f9
      Global init order:       f6
      Poisoned by user:        f7
      Container overflow:      fc
      Array cookie:            ac
      Intra object redzone:    bb
      ASan internal:           fe
      Left alloca redzone:     ca
      Right alloca redzone:    cb
      Shadow gap:              cc
    Thread T27 created by T0 here:
        #0 0x7ff64f3ce2b2 in asan_wrap_CreateThread C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_win.cpp:146
        #1 0x7ff64f5bea6e in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:171
        #2 0x7ff64f54ba4a in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:187
        #3 0x7ff64e3a0548 in content::RenderProcessHostImpl::Init C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_process_host_impl.cc:1831
        #4 0x7ff64e384308 in content::RenderFrameHostManager::InitRenderView C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:2807
        #5 0x7ff64e37badd in content::RenderFrameHostManager::ReinitializeMainRenderFrame C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:3033
        #6 0x7ff64e37988e in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:1057
        #7 0x7ff64e378522 in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_manager.cc:810
        #8 0x7ff64e109166 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\frame_tree_node.cc:538
        #9 0x7ff64e2bcd27 in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigator.cc:578
        #10 0x7ff64e231b74 in content::NavigationControllerImpl::NavigateWithoutEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:3280
        #11 0x7ff64e230d63 in content::NavigationControllerImpl::LoadURLWithParams C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\navigation_controller_impl.cc:1116
        #12 0x7ff65532b6dc in content::Shell::LoadURLForFrame C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell.cc:251
        #13 0x7ff65532b388 in content::Shell::LoadURL C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell.cc:239
        #14 0x7ff65532b08c in content::Shell::CreateNewWindow C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell.cc:229
        #15 0x7ff655372b3a in content::ShellBrowserMainParts::InitializeMessageLoopContext C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell_browser_main_parts.cc:161
        #16 0x7ff655373114 in content::ShellBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\shell\browser\shell_browser_main_parts.cc:213
        #17 0x7ff64d91ab56 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:959
        #18 0x7ff64e64a9f7 in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup_task_runner.cc:41
        #19 0x7ff64d91a060 in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:867
        #20 0x7ff64d921976 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:131
        #21 0x7ff64d916698 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:43
        #22 0x7ff64a5a0b8c in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:598
        #23 0x7ff64a5a35a9 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1081
        #24 0x7ff64a5a27b1 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:956
        #25 0x7ff64a59f9e7 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:372
        #26 0x7ff64a59ffe6 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:398
        #27 0x7ff6476011d2 in main C:\b\s\w\ir\cache\builder\src\content\shell\app\shell_main.cc:33
        #28 0x7ff65cb54863 in scrt_common_main_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
        #29 0x7ff93f947033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)
        #30 0x7ff9405a2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

    ==26232==ABORTING

What is the expected behavior?

What went wrong?
### Summary

A use after free vulnerability exists in the WebRTC functionality of Google Chrome 91.0.4472.114 (Stable) and 93.0.4575.0 (Canary). A specially crafted web page can trigger reuse of previously freed memory which can lead to arbitrary code execution. Victim would need to visit a malicious website to trigger this vulnerability.

Did this work before? N/A 

Chrome version: <Copy from: 'about:version'>  Channel: n/a
OS Version: OS X 10.14.6

## Attachments

- [TALOS-2021-1348 - Google_Chrome_WebRTC_addIceCandidate_use_after_free_vulnerability.txt](attachments/TALOS-2021-1348 - Google_Chrome_WebRTC_addIceCandidate_use_after_free_vulnerability.txt) (text/plain, 13.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 896 B)
- [poc-4.html](attachments/poc-4.html) (text/plain, 9.0 KB)

## Timeline

### [Deleted User] (2021-07-19)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-07-19)

I'm personally unable to repro this right now due to my own Windows env's issue, so I'm just assuming this works.

I think this is a UaF in the renderer [1], so treating it as such. If this is in the browser, this will need to jump up to Security_Severity-Critical.

tommi@: can you please take a look at this? Thanks!

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/peer_connection_tracker.h;l=40

[Monorail components: Blink>WebRTC]

### [Deleted User] (2021-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@chromium.org (2021-07-23)

tommi is out for a bit, it seems.

### gu...@chromium.org (2021-07-24)

[Empty comment from Monorail migration]

### ht...@chromium.org (2021-07-28)

Unable to reproduce on win-asan bot on ToT - see https://chromium-review.googlesource.com/c/chromium/src/+/3057049


### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2021-08-06)

Label: reward_to-marcin.towalski_at_gmail.com

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2021-08-09)

Attaching an updated POC which should make it easier to reproduce. It's a little larger than the original one (that one is minimized) but that's to make it more easily reproducible. 

### ht...@chromium.org (2021-08-09)

Asking for more information on the repro:

- Does this repro on any other platform than Windows 10? (We have a scarcity of Windows machines available for testing)
- Does the repro expose the bug every time for you, or is it flaky?

Needed to figure out more on how to proceed.

### vu...@sourcefire.com (2021-08-09)

- It was mostly tested on Windows but also reproduces on Linux
- It does not reproduce every time, but the latest POC we uploaded should increase success rates

### ht...@chromium.org (2021-08-10)

Thank you very much!
Able to reproduce on tip-of-tree on Linux with:

- args.gn:

is_asan = true
is_debug = false

- command line

out/asan/chrome --js-flags="--expose-gc" --no-sandbox



### gi...@appspot.gserviceaccount.com (2021-08-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/654536e793760b23679131e9f8db45620e5636c7

commit 654536e793760b23679131e9f8db45620e5636c7
Author: Harald Alvestrand <hta@chromium.org>
Date: Tue Aug 10 10:49:27 2021

Protect candidate better from garbage collection during negotiation.

Includes a test that was reliably observed to produce an UAF on Linux
when compiled with ASAN before the fix.

Bug: chromium:1230767
Change-Id: I02dd29332a6d00790dcace41b6584b96413ef6f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057049
Reviewed-by: Florent Castelli <orphis@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/heads/master@{#910244}

[modify] https://crrev.com/654536e793760b23679131e9f8db45620e5636c7/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[add] https://crrev.com/654536e793760b23679131e9f8db45620e5636c7/third_party/blink/web_tests/fast/peerconnection/poc-123067.html


### ht...@chromium.org (2021-08-10)

This CL seems to have fixed the issue. Ran web test and poc-4.html in browser without failure.


### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-10)

Requesting merge to stable M92 because latest trunk commit (910244) appears to be after stable branch point (885287).

Requesting merge to beta M93 because latest trunk commit (910244) appears to be after beta branch point (902210).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-08-10)

hta@ since this fix just landed earlier today I'm going to decline merge approval to M93 to allow for some bake time for this fix on canary, especially as there will be 93 beta release tomorrow. Please let me know if there are any issues with this. Thanks! 

### am...@google.com (2021-08-10)

adding reward-to label based on vulndiscovery@ researcher attribution in comment above (in comment # 13) 

### ht...@chromium.org (2021-08-10)

amyressler@ my reading is that this is going into 94, hasn't made it to a canary release yet, and that we'll ask for a downmerge to 93 in a day or two.
Do you want to decline both merges now and ask me to re-add the merge request labels on Thursday, or should we just leave them dangling?

I don't see it as being extremely urgent, so we'll just roll it when it's ripe.



### ht...@chromium.org (2021-08-11)

94.0.4604.0 is the first Canary version with the fix.

### [Deleted User] (2021-08-11)

This bug requires manual review: M93's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@chromium.org (2021-08-11)

1. Yes.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3057049
3. Yes.
4. Yes. Merge to M-92 is desirable.
5. This is a fix for an UAF, which may be a security vulnerability.
6. No.
7. N/A


### am...@chromium.org (2021-08-12)

hta@ sorry I didn't see your response on Tuesday, but yes, my plan was to leave the merge labels dangling and circle back around. Which is what I'm doing now. :)  Approving merge to M93 and since this is a fix for high-severity UAF, going to go ahead and approve this for merge to M92 so this can be included in next week's table channel release. Please merge to M93, branch 4577, and M92, branch 4515, asap. Sorry for getting back around so late today!

### ht...@chromium.org (2021-08-13)

I have prepared the merge CLs. Who's supposed to change the label from Merge-Request / Merge-Review to Merge-Approved?


### gi...@appspot.gserviceaccount.com (2021-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e02776661c73ce26d04b70ca969063c9e7050e7

commit 4e02776661c73ce26d04b70ca969063c9e7050e7
Author: Harald Alvestrand <hta@chromium.org>
Date: Fri Aug 13 10:02:27 2021

[Merge 92] Protect candidate better from garbage collection during negotiation.

Includes a test that was reliably observed to produce an UAF on Linux
when compiled with ASAN before the fix.

(cherry picked from commit 654536e793760b23679131e9f8db45620e5636c7)

Bug: chromium:1230767
Change-Id: I02dd29332a6d00790dcace41b6584b96413ef6f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057049
Reviewed-by: Florent Castelli <orphis@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#910244}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3094046
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#2046}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/4e02776661c73ce26d04b70ca969063c9e7050e7/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[add] https://crrev.com/4e02776661c73ce26d04b70ca969063c9e7050e7/third_party/blink/web_tests/fast/peerconnection/poc-123067.html


### gi...@appspot.gserviceaccount.com (2021-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/19fd0487f0d178112985b5bc1572c5cf71fda890

commit 19fd0487f0d178112985b5bc1572c5cf71fda890
Author: Harald Alvestrand <hta@chromium.org>
Date: Fri Aug 13 10:03:33 2021

[Merge to 93] Protect candidate better from garbage collection during negotiation.

Includes a test that was reliably observed to produce an UAF on Linux
when compiled with ASAN before the fix.

(cherry picked from commit 654536e793760b23679131e9f8db45620e5636c7)

Bug: chromium:1230767
Change-Id: I02dd29332a6d00790dcace41b6584b96413ef6f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057049
Reviewed-by: Florent Castelli <orphis@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#910244}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3093586
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#779}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/19fd0487f0d178112985b5bc1572c5cf71fda890/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[add] https://crrev.com/19fd0487f0d178112985b5bc1572c5cf71fda890/third_party/blink/web_tests/fast/peerconnection/poc-123067.html


### ht...@chromium.org (2021-08-13)

Merges done, deleting obsolete labels. Adding sheriff to CC in case I missed something.



### am...@google.com (2021-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-16)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-20)

[Empty comment from Monorail migration]

### ht...@chromium.org (2021-08-20)

Now we have merges to 93 and 92, and approval for a merge to 90. Is there reason to ask for a merge to 91?


### am...@chromium.org (2021-08-20)

I don't know about LTS, but for general release channel branches, there is no need to merge to 91. Originally 91 was going to be the first Extended Stable channel release, but that is no longer the case. 

### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/010a318d585ca40546c29263579999aebaf92ee7

commit 010a318d585ca40546c29263579999aebaf92ee7
Author: Harald Alvestrand <hta@chromium.org>
Date: Fri Aug 20 17:27:48 2021

[M90-LTS] Protect candidate better from garbage collection during negotiation.

Includes a test that was reliably observed to produce an UAF on Linux
when compiled with ASAN before the fix.

(cherry picked from commit 654536e793760b23679131e9f8db45620e5636c7)

Bug: chromium:1230767
Change-Id: I02dd29332a6d00790dcace41b6584b96413ef6f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057049
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#910244}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3102948
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1570}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/010a318d585ca40546c29263579999aebaf92ee7/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[add] https://crrev.com/010a318d585ca40546c29263579999aebaf92ee7/third_party/blink/web_tests/fast/peerconnection/poc-123067.html


### rz...@google.com (2021-08-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-25)

Congratulations, Marcin! The VRP Panel had decided to award you $22,000 for this report. Thank you for your detailed analysis and reporting +POC of this browser process memory corruption issue in WebRTC. A member of our finance team will be in touch soon to arrange payment. Excellent work and thanks again for this report! 

### am...@google.com (2021-08-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/43c8a5a2bddd7c1bcb3e0ae1d1bb7ad23ee4395b

commit 43c8a5a2bddd7c1bcb3e0ae1d1bb7ad23ee4395b
Author: Harald Alvestrand <hta@chromium.org>
Date: Tue Sep 21 21:41:04 2021

[Merge 92] Protect candidate better from garbage collection during negotiation.

Includes a test that was reliably observed to produce an UAF on Linux
when compiled with ASAN before the fix.

(cherry picked from commit 654536e793760b23679131e9f8db45620e5636c7)

(cherry picked from commit 4e02776661c73ce26d04b70ca969063c9e7050e7)

Bug: chromium:1230767
Change-Id: I02dd29332a6d00790dcace41b6584b96413ef6f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3057049
Reviewed-by: Florent Castelli <orphis@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#910244}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3094046
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4515@{#2046}
Cr-Original-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3168970
Auto-Submit: Joe Tessler <jrt@chromium.org>
Reviewed-by: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515_132@{#8}
Cr-Branched-From: 8e089f9dc0d240f50afd19b527a90447b90ca5bb-refs/branch-heads/4515@{#1934}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[add] https://crrev.com/43c8a5a2bddd7c1bcb3e0ae1d1bb7ad23ee4395b/third_party/blink/web_tests/fast/peerconnection/poc-123067.html
[modify] https://crrev.com/43c8a5a2bddd7c1bcb3e0ae1d1bb7ad23ee4395b/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc


### vu...@sourcefire.com (2021-10-04)

Is there a release date established for this issue? 90 days approaching this month

### am...@chromium.org (2021-10-04)

Hi vulndiscovery@, the fix for this issue was released in the second security refresh of M92 released on 14 August: https://chromereleases.googleblog.com/2021/08/stable-channel-update-for-desktop.html

This issue was updated as Fixed on 10 August which, by my math, means this bug will be made public (updated with the allpublic label) by us on or about 16 November 2021.  

### vu...@sourcefire.com (2021-10-04)

Thanks for the update

### vu...@sourcefire.com (2021-11-16)

[Comment Deleted]

### vu...@sourcefire.com (2021-11-16)

Just following up to see if the all public status will be updated for this issue


### [Deleted User] (2021-11-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1230767?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056594)*
