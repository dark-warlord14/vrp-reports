# crash in Builtins_StaCurrentContextSlotHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40053031](https://issues.chromium.org/issues/40053031) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | fb...@chromium.org |
| **Created** | 2020-08-08 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36

Steps to reproduce the problem:
chrome version:Chromium 86.0.4222.(https://commondatastorage.googleapis.com/chromium-browser-asan/index.html )
1.download or build latest chrome.
2.python3.6m -m http.server 8000
3../chrome  --use-fake-ui-for-media-stream --js-flags=--expose-gc --user-dir=/tmp/888 --incognito http://127.0.0.1:8000/poc.html

What is the expected behavior?

What went wrong?
Received signal 11 SEGV_ACCERR 7e9a0bac0008
    #0 0x560a2efc725b in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4176:13
    #1 0x560a3a06f639 in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:840:39
    #2 0x560a39e7ea73 in StackTrace ./../../base/debug/stack_trace.cc:206:12
    #3 0x560a39e7ea73 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:203:28
    #4 0x560a3a06e22e in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345:3
    #5 0x7f6f3ba418a0 in __funlockfile ??:?
    #6 0x7f6f3ba418a0 in ?? ??:0
    #7 0x560a37cdec39 in Builtins_StaCurrentContextSlotHandler ??:0:0
  r8: 00007ffe87345190  r9: 0000000000000142 r10: 00007e9a08042381 r11: 00007e9a08d60021
 r12: 0000000000000142 r13: 00007e9a00000000 r14: 00007e9a08d60021 r15: 0000623000003910
  di: 00007e9a000033c8  si: 00007e9a0bac0000  bp: 00007ffe87345190  bx: 00007e9a08d28c31
  dx: 000000000000002b  ax: 00007e9a0baffedf  cx: 0000560a37cdebe0  sp: 00007ffe87345110
  ip: 0000560a37cdec39 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00007e9a0bac0008
[end of stack trace]
Calling _exit(1). Core file will not be generated.
Builtins_StaCurrentContextSlotHandler

Did this work before? N/A 

Chrome version: Builtins_StaCurrentContextSlotHandle  Channel: n/a
OS Version: 20.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### xi...@chromium.org (2020-08-10)

Thanks for the report. I am not able to reproduce it on my latest asan build. Is it possible to provide more details on this crash, like the full stack trace? That may help us triage the issue. Thanks!

### em...@gmail.com (2020-08-11)

Chromium 86.0.4230.0(gsutil cp gs://chromium-browser-asan/linux-release/asan-linux-release-796639.zip)
I can still reproduce it with the new version.And the above is all the stack trace information.  I will continue to analyze.


### [Deleted User] (2020-08-11)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2020-08-11)

Can you add one more parameter and try again?
"--use-fake-device-for-media-stream"

### va...@chromium.org (2020-08-12)

I couldn't reproduce with that flag either:

$ asan-linux-debug-768962/chrome --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --js-flags=--expose-gc --user-dir=/tmp/888 --incognito http://127.0.0.1:8000/poc.html

And I only got a bunch of error messages on the command line:

[3845563:78:0812/022251.115092:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 305ms; render delay: 0ms
[3845563:78:0812/022251.133796:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 314ms; render delay: 0ms
[3845563:78:0812/022251.148721:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 319ms; render delay: 0ms
[3845563:78:0812/022251.165601:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 326ms; render delay: 0ms
[3845563:78:0812/022251.179182:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 329ms; render delay: 0ms
[3845563:78:0812/022251.193144:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 333ms; render delay: 0ms
[3845563:78:0812/022251.207770:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 338ms; render delay: 0ms
[3845563:78:0812/022251.220988:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 341ms; render delay: 0ms
[3845563:78:0812/022251.234285:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 344ms; render delay: 0ms
[3845563:78:0812/022251.247606:WARNING:media_stream_audio_processor.cc(707)] Large audio delay, capture delay: 348ms; render delay: 0ms
[3845979:3845986:0812/022251.443975:WARNING:sync_reader.cc(170)] ASR: No room in socket buffer.: Broken pipe (32)


### va...@chromium.org (2020-08-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### va...@chromium.org (2020-08-12)

Oh, I just realized that I was using an older version in https://crbug.com/chromium/1114398#c5. Trying out a more recent version now (797157).


### va...@chromium.org (2020-08-12)

Repros with this:
$ 797157/asan-linux-debug-797157/asan-linux-debug-797157/chrome --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --js-flags=--expose-gc --user-dir=/tmp/888 --incognito http://127.0.0.1:8000/poc/poc.html 2>&1 | $SRC/tools/valgrind/asan/asan_symbolize.py

[3856528:3856528:0812/024003.467531:INFO:content_main_runner_impl.cc(993)] Chrome is running in full browser mode.
[3856528:3856528:0812/024006.284861:WARNING:account_consistency_mode_manager.cc(196)] Desktop Identity Consistency cannot be enabled as no OAuth client ID and client secret have been configured.
[3856528:3856628:0812/024006.468937:ERROR:bus.cc(393)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[3856528:3856628:0812/024006.469460:ERROR:bus.cc(393)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[3856528:3856628:0812/024006.998491:ERROR:bus.cc(393)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[3856528:3856628:0812/024006.999273:ERROR:bus.cc(393)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[3856627:3856627:0812/024007.136461:ERROR:sandbox_linux.cc(374)] InitializeSandbox() called with multiple threads in process gpu-process.
[3856630:3856692:0812/024008.486489:WARNING:http_cache_transaction.cc(1181)] Unable to open or create cache entry
Received signal 11 <unknown> 000000000000
    #0 0x55aab178474b in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4176:13
    #1 0x7f661099b44f in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:840:39
    #2 0x7f66102d5309 in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace.cc:206:12
    #3 0x7f66102d5168 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:203:28
    #4 0x7f66109999dd in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:345:3
    #5 0x7f657af0a110 in __funlockfile :?
    #6 0x7f657af0a110 in ?? ??:0
    #7 0x7f658ee48386 in Builtins_CallApiCallback ??:0:0
  r8: 00000000000003a4  r9: 00000000000003a0 r10: 00007efb08042381 r11: 1baddead0baddeaf
 r12: 00007efb084c2d99 r13: 00007efb00000000 r14: 0000625000039bd0 r15: 00007efb0000a750
  di: 00007efb000033b0  si: 00007efb08303d21  bp: 00007ffdeb0ef5a8  bx: 0000000000000038
  dx: 00000c1c00008c7b  ax: 1baffed00baffedf  cx: 00000c4a0000771a  sp: 00007ffdeb0ef4e0
  ip: 00007f658ee48386 efl: 0000000000010202 cgf: 002b000000000033 erf: 0000000000000000
 trp: 000000000000000d msk: 0000000000000000 cr2: 0000000000000000
[end of stack trace]
Calling _exit(1). Core file will not be generated.


### va...@chromium.org (2020-08-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-08-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5661024845365248.

### jg...@chromium.org (2020-08-12)

Waiting for CF results.

### cl...@chromium.org (2020-08-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5722434287763456.

### cl...@chromium.org (2020-08-12)

https://clusterfuzz.com/testcase?key=5722434287763456 reproduced the crash.

### cl...@chromium.org (2020-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-08-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5722434287763456

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7e9c0bac0008
Crash State:
  Builtins_StaCurrentContextSlotHandler
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=783845:783847

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5722434287763456

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5722434287763456 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### jg...@chromium.org (2020-08-13)

Bisected to

f891859 Shows error dialog when MGS provisioning fails in ARC++ by GioVAX · 6 weeks ago
8049b14 [PTZ] Resolve getUserMedia when ImageCapture has been initialized by Francois Beaufort · 6 weeks ago

Suspecting the latter. Adding reviewers since the CL author is external, ptal.

Going by the trace in #8 which contains Builtins_CallApiCallback, it looks like the crash is happening in an embedder (= blink) function. 

The originally reported trace looks a bit different and has Builtins_StaCurrentContextSlotHandler on top, possibly it also goes through Builtins_CallApiCallback but it's just not part of the trace? Not sure.

### re...@chromium.org (2020-08-13)

CL author isn't actually external.

### fb...@chromium.org (2020-08-13)

I'll have a look

### fb...@chromium.org (2020-08-13)

I can reproduce locally.

### fb...@chromium.org (2020-08-13)

I just noticed the crash does not happen when using `navigator.mediaDevices.getUserMedia` instead of `navigator.webkitGetUserMedia` or `navigator.getUserMedia`.

### fb...@chromium.org (2020-08-13)

Disregard https://crbug.com/chromium/1114398#c21. I can reproduce with `navigator.mediaDevices.getUserMedia` as well.

### cl...@chromium.org (2020-08-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5722434287763456

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7e9c0bac0008
Crash State:
  Builtins_StaCurrentContextSlotHandler
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=783845:783847

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5722434287763456

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5722434287763456 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### gu...@chromium.org (2020-08-13)

[Empty comment from Monorail migration]

### fb...@chromium.org (2020-08-13)

WIP CL is in review at https://chromium-review.googlesource.com/c/chromium/src/+/2352800

### fb...@chromium.org (2020-08-13)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/420456578b90c05228cc8310678c6edd6088b17b

commit 420456578b90c05228cc8310678c6edd6088b17b
Author: Francois Beaufort <beaufort.francois@gmail.com>
Date: Thu Aug 13 13:32:15 2020

Post callback asynchronously from the MediaStream constructor

This CL makes sure initialized callback from the MediaStream constructor
is called asynchronously as it was causing a JavaScript crash
potentially caused by the fact that the MediaStream was not completely
registered with oilpan.

Bug: 1114398
Change-Id: If6058b183bdd07fa747d810efe0f6abed4914e49
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2352800
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: François Beaufort <beaufort.francois@gmail.com>
Cr-Commit-Position: refs/heads/master@{#797649}

[modify] https://crrev.com/420456578b90c05228cc8310678c6edd6088b17b/third_party/blink/renderer/modules/mediastream/media_stream.cc
[modify] https://crrev.com/420456578b90c05228cc8310678c6edd6088b17b/third_party/blink/renderer/modules/mediastream/media_stream_track.cc


### cl...@chromium.org (2020-08-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5722434287763456

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7e9c0bac0008
Crash State:
  Builtins_StaCurrentContextSlotHandler
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=783845:783847

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5722434287763456

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5722434287763456 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### [Deleted User] (2020-08-13)

This issue is marked as a release blocker with no milestone associated. Please add an appropriate milestone.

All release blocking issues should have milestones associated to it, so that the issue can tracked and the fixes can be pushed promptly.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2020-08-13)

The culprit CL landed in M-86 so no merges should be necessary.

### cl...@chromium.org (2020-08-13)

ClusterFuzz testcase 5722434287763456 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=797641:797649

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-08-14)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-17)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-19)

VRP panel increasing this to High in case there's an effective use-after-free here.

### ad...@google.com (2020-08-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-19)

Thanks for the report! The VRP panel has decided to award $5000 for this bug. Someone from our finance team will be in touch.

### ad...@google.com (2020-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-11-21)

This issue was migrated from crbug.com/chromium/1114398?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053031)*
