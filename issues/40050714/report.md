# use-after-poison in base::internal::WeakReferenceOwner::Invalidate()

| Field | Value |
|-------|-------|
| **Issue ID** | [40050714](https://issues.chromium.org/issues/40050714) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>Network>WebSockets |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2019-11-16 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36

Steps to reproduce the problem:
1 Build chrome with asan(Chromium 80.0.3965.0).
2 Start node server.
	-	node node_websocket.js
3 Start python server.
	-	 python standalone.py -p 8880 -w server
4 ./chrome http://127.0.0.1:8605/poc.html
5 Get Use-Ater-Poison crash.

What is the expected behavior?

What went wrong?
==17331==ERROR: AddressSanitizer: use-after-poison on address 0x7ee693c54450 at pc 0x5631a95ac395 bp 0x7fffb9d50650 sp 0x7fffb9d50648
READ of size 8 at 0x7ee693c54450 thread T0 (chrome)
    #0 0x5631a95ac394 in operator-> base/memory/scoped_refptr.h:236:12
    #1 0x5631a95ac394 in base::internal::WeakReferenceOwner::Invalidate() base/memory/weak_ptr.cc:77:3
    #2 0x5631b370bca3 in blink::TimerBase::RunInternal() third_party/blink/renderer/platform/timer.cc:135:21
    #3 0x5631a966728e in Run base/callback.h:98:12
    #4 0x5631a966728e in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:142:33
    #5 0x5631a96a1839 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*, bool*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:365:23
    #6 0x5631a96a11b2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:219:7
    #7 0x5631a95ae0b0 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_default.cc:39:55
    #8 0x5631a96a3664 in Run base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #9 0x5631a96a3664 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #10 0x5631a961608d in base::RunLoop::Run() base/run_loop.cc:156:14
    #11 0x5631ba6229bb in content::RendererMain(content::MainFunctionParams const&) content/renderer/renderer_main.cc:213:16
    #12 0x5631a8622796 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:871:10
    #13 0x5631a87ca10f in service_manager::Main(service_manager::MainParams const&) services/service_manager/embedder/main.cc:423:29
    #14 0x5631a861dad6 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:19:10
    #15 0x56319f9e5e54 in ChromeMain chrome/app/chrome_main.cc:110:12
    #16 0x7facb1e95b96 in __libc_start_main /build/glibc-OTsEL5/glibc-2.27/csu/../csu/libc-start.c:310

Address 0x7ee693c54450 is a wild pointer.
SUMMARY: AddressSanitizer: use-after-poison base/memory/scoped_refptr.h:236:12 in operator->
Shadow bytes around the buggy address:
  0x0fdd52782830: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 06
  0x0fdd52782840: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd52782850: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd52782860: f7 f7 f7 06 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd52782870: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x0fdd52782880: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7
  0x0fdd52782890: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd527828a0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd527828b0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 06 f7 f7 f7 f7 f7
  0x0fdd527828c0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x0fdd527828d0: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
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
==17331==ABORTING

Did this work before? N/A 

Chrome version: 80.0.3965.0  Channel: n/a
OS Version: 18.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### cd...@gmail.com (2019-11-16)

Sorry,
Sorry, I missed one step.
First  need to install pywebsocket(https://github.com/google/pywebsocket).



### do...@chromium.org (2019-11-17)

+network and WebSocket folks. The traceback isn't particularly illuminating, but the PoC suggests something in WebSocket code is triggering a WeakPtr deference on a WeakPtr that is already dead.

[Monorail components: Blink>Network>WebSockets]

### mm...@chromium.org (2019-11-17)

Network stack team doesn't own the WebSocket code, or any code in the renderer process in general (well, aside from the error page code, I suppose).

### yh...@chromium.org (2019-11-17)

I'll be OOO/biztrip next week. Adam, can you take a look?

### sh...@chromium.org (2019-11-17)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2019-11-19)

It's some kind of timer garbage collection race condition. It looks like the destructor for WebSocketMessageChunkAccumulator::timer_ sometimes runs after the destructor for WebSocketChannelImpl. Because WebSocketMessageChunkAccumulator is not itself garbage collected, it doesn't get the garbage-collection aware version of TaskRunnerTimer.

Incidentally, it's not necessary to have a separate installation of pywebsocket to reproduce this. Using third_party/blink/tools/run_blink_websocketserver.py is sufficient.

I can only reproduce the crash with ASAN but that doesn't mean that non-ASAN builds aren't vulnerable.

[Monorail components: Blink>MemoryAllocator>GarbageCollection]

### ri...@chromium.org (2019-11-19)

First vulnerable version is 78.0.3891.0.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dbd38b349c143b1199d5419de252fbc9abd9b1cf

commit dbd38b349c143b1199d5419de252fbc9abd9b1cf
Author: Adam Rice <ricea@chromium.org>
Date: Wed Nov 20 02:42:04 2019

Reset the timer for WebSocketMessageChunkAccumulator

Stop the WebSocketMessageChunkAccumulator timer in
WebSocketChannelImpl::Dispose(), avoiding destruction order issues.

BUG=1025489

Change-Id: I0bc986ec81ede448dc0d96162ca1c15f8b184fef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1923777
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/master@{#716852}

[modify] https://crrev.com/dbd38b349c143b1199d5419de252fbc9abd9b1cf/third_party/blink/renderer/modules/websockets/websocket_channel_impl.cc
[modify] https://crrev.com/dbd38b349c143b1199d5419de252fbc9abd9b1cf/third_party/blink/renderer/modules/websockets/websocket_message_chunk_accumulator.cc
[modify] https://crrev.com/dbd38b349c143b1199d5419de252fbc9abd9b1cf/third_party/blink/renderer/modules/websockets/websocket_message_chunk_accumulator.h


### ri...@chromium.org (2019-11-20)

I'd like to merge this to M79 but I don't know how to write a robust test for it.

### ri...@chromium.org (2019-11-29)

This is a small fix for a potentially serious bug that should be safe to merge to M79.

### sh...@chromium.org (2019-11-29)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2019-11-29)

> 1. Does your merge fit within the Merge Decision Guidelines?
> - Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
> - Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

Mostly. Security consultation in progress. I don't know how to write an automated test for this; I've only tested it manually.

> 2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/1923777

> 3. Has the change landed and been verified on master/ToT?

Yes.

> 4. Why are these changes required in this milestone after branch?

High severity security issue.

> 5. Is this a new feature?

No.

> 6. If it is a new feature, is it behind a flag using finch?

N/A.

### ad...@google.com (2019-11-29)

Adjusting impact to "stable" per https://crbug.com/chromium/1025489#c8.

Yes, we should definitely merge to M79.

### ad...@google.com (2019-11-29)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-29)

Approving merge to M79 branch 3945 per comments #11, #13  and #14. Please merge ASAP. 

### ri...@chromium.org (2019-11-29)

Merged at https://chromium.googlesource.com/chromium/src/+/d8bcf9219cc07f6edbba36126089bab4271a2f7c.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d8bcf9219cc07f6edbba36126089bab4271a2f7c

commit d8bcf9219cc07f6edbba36126089bab4271a2f7c
Author: Adam Rice <ricea@chromium.org>
Date: Fri Nov 29 07:20:01 2019

Reset the timer for WebSocketMessageChunkAccumulator

Stop the WebSocketMessageChunkAccumulator timer in
WebSocketChannelImpl::Dispose(), avoiding destruction order issues.

BUG=1025489

(cherry picked from commit dbd38b349c143b1199d5419de252fbc9abd9b1cf)

Change-Id: I0bc986ec81ede448dc0d96162ca1c15f8b184fef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1923777
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#716852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1943629
Reviewed-by: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/branch-heads/3945@{#821}
Cr-Branched-From: e4635fff7defbae0f9c29e798349f6fc0cce4b1b-refs/heads/master@{#706915}

[modify] https://crrev.com/d8bcf9219cc07f6edbba36126089bab4271a2f7c/third_party/blink/renderer/modules/websockets/websocket_channel_impl.cc
[modify] https://crrev.com/d8bcf9219cc07f6edbba36126089bab4271a2f7c/third_party/blink/renderer/modules/websockets/websocket_message_chunk_accumulator.cc
[modify] https://crrev.com/d8bcf9219cc07f6edbba36126089bab4271a2f7c/third_party/blink/renderer/modules/websockets/websocket_message_chunk_accumulator.h


### sh...@chromium.org (2019-11-29)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-30)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-02)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $5,000 for this report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-05)

ricea@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-01-07)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1025489?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Blink>Network>WebSockets]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050714)*
