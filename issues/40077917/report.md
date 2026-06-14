# Heap-use-after-free in WebCore::AudioDSPKernelProcessor::reset

| Field | Value |
|-------|-------|
| **Issue ID** | [40077917](https://issues.chromium.org/issues/40077917) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ha...@chromium.org |
| **Created** | 2013-08-10 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6662160935550976

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x050a47c3
Crash State:
  - crash stack -
  WebCore::AudioDSPKernelProcessor::reset
  WebCore::BiquadProcessor::setType
  - free stack -
  WebCore::BiquadDSPKernel::`scalar deleting destructor'
  WTF::Vector<WTF::OwnPtr<WebCore::FrameAction>,0>::shrink
  

Minimized Testcase (74.37 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96VVe5qRsF1_53yM1BQ2rSbqz3CXIz8rmMDJfH5ShR4-6svRxbt0IxBiQYamp88hAjOaiOlmG6Qs111CYf5ZRfSVm2cxrkzPnE66H7QGVwRmSzdq9tTekQyEXIGV0A_ain7Yr-t5zNnzhm_ExYMDLcNqZf1_9rG-KeIAWhWApmZyObQno8

## Attachments

- [C--clusterfuzz-slave-bot-inputs-fuzzer-testcases-fuzz-8.html](attachments/C--clusterfuzz-slave-bot-inputs-fuzzer-testcases-fuzz-8.html) (text/html; charset=us-ascii, 74.4 KB)
- [C--clusterfuzz-slave-bot-inputs-fuzzer-testcases-fuzz-8 (1).html](attachments/C--clusterfuzz-slave-bot-inputs-fuzzer-testcases-fuzz-8 (1).html) (text/plain; charset=us-ascii, 6.6 KB)

## Timeline

### in...@chromium.org (2013-08-10)

Xingnan@, can you please help to take a look.

### in...@chromium.org (2013-08-10)

CF windows bots are constantly trying to reduce it more since it is not a reliable crasher. way more reduced testcase enclosed.

### in...@chromium.org (2013-08-15)

Chris not longer works here. Assigning to Ray for triage. This only reproduced on windows syzyasan bots. so, no regression range.

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

Fixing severity based on the fact, that all of these are race conditions (free, crash on different threads). No reliable reproducer.

### gr...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-04)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6737468556574720

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fb30480008c
Crash State:
  - crash stack -
  WebCore::AudioDSPKernelProcessor::reset
  WebCore::BiquadFilterNode::setType
  - free stack -
  WebCore::DOMWindowV8Internal::btoaMethodCallback
  v8::internal::FunctionCallbackArguments::Call
  




### ha...@chromium.org (2013-09-04)

This would be due to threading races on AudioDSPKernelProcessor::m_kernels. I'll upload a CL soon.

### ha...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157256

------------------------------------------------------------------------
r157256 | haraken@chromium.org | 2013-09-05T01:24:48.627268Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioDSPKernelProcessor.h?r1=157256&r2=157255&pathrev=157256
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioDSPKernelProcessor.cpp?r1=157256&r2=157255&pathrev=157256

Fix threading races on AudioDSPKernelProcessor::m_kernels

AudioDSPKernelProcessor::m_kernels is accessed by the main thread and
the Audio Device thread, and thus should be protected by mutex.

This mutex implementation is consistent with that of ConvolverNode::m_reverb.

See the crash report for more details: https://cluster-fuzz.appspot.com/testcase?key=6662160935550976

BUG=271161
No tests because the crash depends on threading races and thus not reproducible.

Review URL: https://chromiumcodereview.appspot.com/23931002
------------------------------------------------------------------------

### ha...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### bu...@chromium.org (2013-09-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157692

------------------------------------------------------------------------
r157692 | haraken@chromium.org | 2013-09-12T19:23:46.009249Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/platform/audio/AudioDSPKernelProcessor.cpp?r1=157692&r2=157691&pathrev=157692
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/core/platform/audio/AudioDSPKernelProcessor.h?r1=157692&r2=157691&pathrev=157692

Merge 157256 "Fix threading races on AudioDSPKernelProcessor::m_..."

> Fix threading races on AudioDSPKernelProcessor::m_kernels
> 
> AudioDSPKernelProcessor::m_kernels is accessed by the main thread and
> the Audio Device thread, and thus should be protected by mutex.
> 
> This mutex implementation is consistent with that of ConvolverNode::m_reverb.
> 
> See the crash report for more details: https://cluster-fuzz.appspot.com/testcase?key=6662160935550976
> 
> BUG=271161
> No tests because the crash depends on threading races and thus not reproducible.
> 
> Review URL: https://chromiumcodereview.appspot.com/23931002

TBR=haraken@chromium.org

Review URL: https://codereview.chromium.org/23619043
------------------------------------------------------------------------

### ha...@chromium.org (2013-09-12)

Merged into M30.

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### la...@google.com (2013-09-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

$500

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-21)

Renaming Blink>Audio to Blink>Media>Audio for better characterization

[Monorail components: -Blink>Audio Blink>Media>Audio]

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

This issue was migrated from crbug.com/chromium/271161?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077917)*
