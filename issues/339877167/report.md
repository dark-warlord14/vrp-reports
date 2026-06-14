# Memory corruption in ReadableByteStreamController::FillPullIntoDescriptorFromQueue

| Field | Value |
|-------|-------|
| **Issue ID** | [339877167](https://issues.chromium.org/issues/339877167) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>StreamsAPI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2024-05-11 |
| **Bounty** | $11,000.00 |

## Description

VULNERABILITY DETAILS
When js api ReadableByteStreamController.enqueue is called, it may go with `ReadableByteStreamController::enqueue -> Enqueue -> ProcessPullIntoDescriptorsUsingQueue`. In this function there is a while loop to fill pull into descriptor, if the chunk is ready, it uses Promise.Resolve to fullfill the request and return the buffer to user [1]. However, fullfill the request may trigger an user-defined js function and one can detach the buffer which already queued in the next descriptor by accessing `readcontroller.byobRequest`. This will result in memory corruption when executing memcpy at line[2], which has the ability to write an arbitrary value to memory range starting from 0 to maxArrayBufferLength.

```
void ReadableByteStreamController::ProcessPullIntoDescriptorsUsingQueue(
    ScriptState* script_state,
    ReadableByteStreamController* controller,
    ExceptionState& exception_state) {
    // skip
    if (FillPullIntoDescriptorFromQueue(controller, pull_into_descriptor)) {
      //     i. Perform !
      //     ReadableByteStreamControllerShiftPendingPullInto(controller).
      ShiftPendingPullInto(controller);
      //     ii. Perform ! ReadableByteStreamControllerCommitPullIntoDescriptor(
      //     controller.[[stream]], pullIntoDescriptor).
      CommitPullIntoDescriptor(script_state,                                 // ======> [1]
                               controller->controlled_readable_stream_,
                               pull_into_descriptor, exception_state);
      DCHECK(!exception_state.HadException());
    }
  }
}

bool ReadableByteStreamController::FillPullIntoDescriptorFromQueue(
    ReadableByteStreamController* controller,
    PullIntoDescriptor* pull_into_descriptor) {
  // skip
  while (total_bytes_to_copy_remaining > 0) {
    // a. Let headOfQueue be queue[0].
    QueueEntry* head_of_queue = queue[0];
    // b. Let bytesToCopy be min(totalBytesToCopyRemaining,
    // headOfQueue’s byte length).
    size_t bytes_to_copy =
        std::min(total_bytes_to_copy_remaining, head_of_queue->byte_length);
    // c. Let destStart be pullIntoDescriptor’s byte offset +
    // pullIntoDescriptor’s bytes filled.
    // This addition will not overflow because byte offset and bytes filled
    // refer to actually allocated memory, so together they cannot exceed
    // size_t.
    size_t dest_start =
        pull_into_descriptor->byte_offset + pull_into_descriptor->bytes_filled;
    // d. Perform ! CopyDataBlockBytes(pullIntoDescriptor’s
    // buffer.[[ArrayBufferData]], destStart, headOfQueue’s
    // buffer.[[ArrayBufferData]], headOfQueue’s byte offset, bytesToCopy).
    memcpy(                                                                         // ======> [2]
        static_cast<char*>(pull_into_descriptor->buffer->Data()) + dest_start,
        static_cast<char*>(head_of_queue->buffer->Data()) +
            head_of_queue->byte_offset,
        bytes_to_copy);
```
[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc;l=503;drc=ffa073e3fa09b2be387adb32663a3ca9e93e61e9
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc;l=1055;drc=ffa073e3fa09b2be387adb32663a3ca9e93e61e9


VERSION
Chrome Version: stable + dev


REPRODUCTION CASE
Tested on: Chrome 126.0.6470.1 asan build 64-bit on Linux
1. Setup http server
   python3 -m http.server
2. Launch chrome and navigate to http://localhost:8000/poc.html
   out/Asan/chrome http://localhost:8000/poc.html
The render would crash when accessing a specific address 0x000042424238


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: renderer
Crash State: see crash.log for details


== Bisection ==
This bug exists for a long time which was introduced in Dec, 2020 (https://chromium.googlesource.com/chromium/src/+/c85fa18ea9fd78fb9c992ac3dca9ae41d2f0a2a3)

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.1 KB)
- [crash.log](attachments/crash.log) (text/plain, 2.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-05-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5350388329807872.

### ad...@google.com (2024-05-12)

Reporter, ClusterFuzz was unable to reproduce this. I'll try locally next week, but if you can spot any ways to make this more readily reproducible, please let me know.

### ad...@google.com (2024-05-13)

Reproduced locally with ASAN 1299854.

### ad...@google.com (2024-05-13)

I can also reproduce locally with ASAN 1274542, corresponding to M124.

### ad...@google.com (2024-05-13)

The ASAN stack trace from Canary:

```
Received signal 11 SEGV_MAPERR 000042424238
    #0 0x5583c8df58a6 in ___interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4364:13
    #1 0x5583db41c388 in base::debug::CollectStackTrace(void const**, unsigned long) ./../../base/debug/stack_trace_posix.cc:1043:7
    #2 0x5583db3e40e7 in StackTrace ./../../base/debug/stack_trace.cc:241:20
    #3 0x5583db3e40e7 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:236:28
    #4 0x5583db41b676 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:462:3
    #5 0x7f695b642520 in __sigaction ??:?
    #6 0x7f695b6c49e8 in memcpy ??:?
    #7 0x5583c8e4a2fc in __asan_memcpy _asan_rtl_:3
    #8 0x5583e9bbf05c in blink::ReadableByteStreamController::FillPullIntoDescriptorFromQueue(blink::ReadableByteStreamController*, blink::ReadableByteStreamController::PullIntoDescriptor*) ./../../third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc:1055:5
    #9 0x5583e9bbdee6 in blink::ReadableByteStreamController::ProcessPullIntoDescriptorsUsingQueue(blink::ScriptState*, blink::ReadableByteStreamController*, blink::ExceptionState&) ./../../third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc:497:9
    #10 0x5583e9bbbf77 in blink::ReadableByteStreamController::Enqueue(blink::ScriptState*, blink::ReadableByteStreamController*, blink::NotShared<blink::DOMArrayBufferView>, blink::ExceptionState&) ./../../third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc:402:5
    #11 0x5583ebcbc7ef in blink::(anonymous namespace)::v8_readable_byte_stream_controller::EnqueueOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/core/v8/v8_readable_byte_stream_controller.cc:158:17
    #12 0x5583d205144f in Builtins_CallApiCallbackGeneric setup-isolate-deserialize.cc:0:0

```

This is a renderer write with a controllable address (within some bounds) so is clear RCE - nice discovery! S1.

### cl...@appspot.gserviceaccount.com (2024-05-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5099811186343936.

### cl...@appspot.gserviceaccount.com (2024-05-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6269448315928576.

### ad...@google.com (2024-05-13)

I filed [this bug for the fact ClusterFuzz was unable to reproduce this](https://issues.chromium.org/issues/340201616).

### pe...@google.com (2024-05-13)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-05-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2024-05-15)

Testcase 6269448315928576 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6269448315928576.

### cl...@appspot.gserviceaccount.com (2024-05-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6085483172921344.

### ni...@chromium.org (2024-05-21)

Thank you for reporting the bug!
It appears that this happens because the pull-into descriptor stores the byte length separately from the array buffer, but when the buffer is detached (when postMessage() is called), the computation for how many bytes to copy is out of sync with the array buffer.

We can check to see if the buffer is detached and throw a TypeError before we try to fill the "non-existent" buffer with the memcpy, similar to other places in the spec where we throw a TypeError when the buffer is detached. I'll upload a fix soon.

### ap...@google.com (2024-05-21)

Project: chromium/src
Branch: main

commit cd405492789ec4bc6ecd598754154c527ff60e95
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date:   Tue May 21 07:07:52 2024

    Streams: Check if buffer is detached when filling pull-into descriptor
    
    The pull-into descriptor can become out-of-sync with the array buffer
    when the buffer is detached. This CL adds a check to see if the buffer
    is detached before trying to fill it.
    
    Bug: 339877167
    Change-Id: I17d98416a746a5ade24308ef332cba829933d7de
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5553232
    Reviewed-by: Domenic Denicola <domenic@chromium.org>
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1303628}

M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc
M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.h

https://chromium-review.googlesource.com/5553232


### pe...@google.com (2024-05-21)

Requesting merge to extended stable (M124) because latest trunk commit (1303628) appears to be after extended stable branch point (1274542).
Requesting merge to stable (M125) because latest trunk commit (1303628) appears to be after stable branch point (1287751).
Requesting merge to beta (M126) because latest trunk commit (1303628) appears to be after beta branch point (1300313).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ni...@chromium.org (2024-05-22)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/5553232

2. Has this fix been verified on Canary to not pose any stability regressions?
Yes, there are no regressions on Canary.

3. Does this fix pose any potential non-verifiable stability risks?
No.

4. Does this fix pose any known compatibility risks?
No.

5. Does it require manual verification by the test team? If so, please describe required testing.
No.

### pe...@google.com (2024-05-22)

Merge review required: M126 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-05-22)

Merge review required: M125 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-05-22)

Merge review required: M124 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

### ni...@chromium.org (2024-05-22)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
This is a security fix for a renderer RCE.

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/5553232

3. Have the changes been released and tested on canary?
Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No, readable byte streams is not a new feature. It has been in Chrome for 4 years now.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No, I locally tested with the PoC and checked that the change fixes the issue.

### am...@chromium.org (2024-05-23)

Thanks for filling out the merge questionnaire. This will be reviewed for merge tomorrow since by then minimal Canary bake time will have been achieved.
M126 Beta update released today was cut yesterday and next M125 update will be cut on Tuesday, so we have some time here.

### am...@chromium.org (2024-05-23)

<https://chromium-review.googlesource.com/c/chromium/src/+/5553232> approved for merges

please merge this fix to M126 beta / branch 6478, M125 Stable / branch 6422, and M124 Extended Stable / branch 6367 as soon as possible, before EOD Monday, 27 May so this fix can be included in next weeks respective updates -- thank you!

### ap...@google.com (2024-05-24)

Project: chromium/src
Branch: refs/branch-heads/6367

commit 24329fe5c4d01390a9be6e130f31a9a5597fddb1
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date:   Fri May 24 01:26:02 2024

    [Merge to M124] Streams: Check if buffer is detached when filling pull-into descriptor
    
    The pull-into descriptor can become out-of-sync with the array buffer
    when the buffer is detached. This CL adds a check to see if the buffer
    is detached before trying to fill it.
    
    (cherry picked from commit cd405492789ec4bc6ecd598754154c527ff60e95)
    
    Bug: 339877167
    Change-Id: Ibf46a75e36dc739910db07f2e88ff9998c21e8a8
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5553232
    Reviewed-by: Domenic Denicola <domenic@chromium.org>
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1303628}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5553411
    Cr-Commit-Position: refs/branch-heads/6367@{#1228}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc
M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.h

https://chromium-review.googlesource.com/5553411


### pe...@google.com (2024-05-24)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### ap...@google.com (2024-05-24)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 64c6a5481065557447586d56f7ce020419d34515
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date:   Fri May 24 01:51:06 2024

    [Merge to M126] Streams: Check if buffer is detached when filling pull-into descriptor
    
    The pull-into descriptor can become out-of-sync with the array buffer
    when the buffer is detached. This CL adds a check to see if the buffer
    is detached before trying to fill it.
    
    (cherry picked from commit cd405492789ec4bc6ecd598754154c527ff60e95)
    
    Bug: 339877167
    Change-Id: I325dff05af97c359bc8e53fd197eb0e4e0955c00
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5553232
    Reviewed-by: Domenic Denicola <domenic@chromium.org>
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1303628}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5553000
    Cr-Commit-Position: refs/branch-heads/6478@{#524}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc
M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.h

https://chromium-review.googlesource.com/5553000


### ni...@chromium.org (2024-05-24)

1. Was this issue a regression for the milestone it was found in?
No, this regression existed since 89.0.4346.0 (https://chromiumdash.appspot.com/commit/c85fa18ea9fd78fb9c992ac3dca9ae41d2f0a2a3).

2. Is this issue related to a change or feature merged after the latest LTS Milestone?
No, readable byte streams is not a new feature. It has been in Chrome for 4 years now.

### ap...@google.com (2024-05-24)

Project: chromium/src
Branch: refs/branch-heads/6422

commit 0c4d74372db1b67c84d6a086737278fbf62eed68
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date:   Fri May 24 04:36:45 2024

    [Merge to M125] Streams: Check if buffer is detached when filling pull-into descriptor
    
    The pull-into descriptor can become out-of-sync with the array buffer
    when the buffer is detached. This CL adds a check to see if the buffer
    is detached before trying to fill it.
    
    (cherry picked from commit cd405492789ec4bc6ecd598754154c527ff60e95)
    
    Bug: 339877167
    Change-Id: I8d78356d1fed8b1977edf341e6178d5c69ec9a26
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5553232
    Reviewed-by: Domenic Denicola <domenic@chromium.org>
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1303628}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5553364
    Cr-Commit-Position: refs/branch-heads/6422@{#1140}
    Cr-Branched-From: 9012208d0ce02e0cf0adb9b62558627c356f3278-refs/heads/main@{#1287751}

M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc
M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.h

https://chromium-review.googlesource.com/5553364


### rz...@google.com (2024-05-28)

Adding the answers to the LTS merge questionnaire because the automation isn't adding it:

1. <https://crrev.com/c/5573750>
2. Low, no conflicts
3. 124, 125, 126
4. Yes

### pe...@google.com (2024-05-28)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-05-28)

re [comment #30](https://issues.chromium.org/issues/339877167#comment30): See [comment #29](https://issues.chromium.org/issues/339877167#comment29)

### ap...@google.com (2024-05-30)

Project: chromium/src
Branch: refs/branch-heads/6099

commit f65adad8e38776128ae878df3774a37bb9e8914c
Author: Nidhi Jaju <nidhijaju@chromium.org>
Date:   Thu May 30 08:28:53 2024

    [M120-LTS] Streams: Check if buffer is detached when filling pull-into descriptor
    
    The pull-into descriptor can become out-of-sync with the array buffer
    when the buffer is detached. This CL adds a check to see if the buffer
    is detached before trying to fill it.
    
    (cherry picked from commit cd405492789ec4bc6ecd598754154c527ff60e95)
    
    Bug: 339877167
    Change-Id: I17d98416a746a5ade24308ef332cba829933d7de
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5553232
    Commit-Queue: Nidhi Jaju <nidhijaju@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1303628}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5573750
    Reviewed-by: Artem Sumaneev <asumaneev@google.com>
    Reviewed-by: Nidhi Jaju <nidhijaju@chromium.org>
    Commit-Queue: Zakhar Voit <voit@google.com>
    Owners-Override: Artem Sumaneev <asumaneev@google.com>
    Cr-Commit-Position: refs/branch-heads/6099@{#2030}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.cc
M       third_party/blink/renderer/core/streams/readable_byte_stream_controller.h

https://chromium-review.googlesource.com/5573750


### sp...@google.com (2024-06-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of memory corruption / RCE in sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-05)

Congratulations, Rong! Nice to see a report from you -- nice finding and great report. Thank you so much for your efforts in discovering and reporting this issue to us -- great work!

### pe...@google.com (2024-08-28)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339877167)*
