# Heap-use-after-free in WebCore::ConvolverNode::tailTime

| Field | Value |
|-------|-------|
| **Issue ID** | [40078041](https://issues.chromium.org/issues/40078041) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ha...@chromium.org |
| **Created** | 2013-09-03 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6515787040817152

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60a0002a3c60
Crash State:
  - crash stack -
  WebCore::ConvolverNode::tailTime
  WebCore::AudioNode::propagatesSilence
  - free stack -
  WebCore::ConvolverNode::setBuffer
  WebCore::ConvolverNodeV8Internal::bufferAttributeSetterCallback
  


Fully reproducible crash found using linux_tsan_chrome_mp job type (history_size=6).

## Timeline

### in...@chromium.org (2013-09-03)

Changing severity since free and crash on different threads, does not seem it is reliable to reproduce.

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

Fixing severity based on the fact, that all of these are race conditions (free, crash on different threads). No reliable reproducer.

### gr...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-09-03)

This looks like the same issue as 223962

Freed in one thread and used in another.

READ of size 8 at 0x60a0002a3c60 thread T7 (AudioOutputDevi)
    #0 0x7fe168abd4fa in WebCore::ConvolverNode::tailTime() const src/third_party/WebKit/Source/core/platform/audio/Reverb.h:51
    #1 0x7fe168aa451f in WebCore::AudioNode::propagatesSilence() const src/third_party/WebKit/Source/modules/webaudio/AudioNode.cpp:339
    #2 0x7fe168aa4060 in WebCore::AudioNode::processIfNecessary(unsigned long) src/third_party/WebKit/Source/modules/webaudio/AudioNode.cpp:317
freed by thread T0 (chrome) here:
    #0 0x7fe15ec98134 in operator delete(void*) _asan_rtl_
    #1 0x7fe168abd28c in WebCore::ConvolverNode::setBuffer(WebCore::AudioBuffer*) src/third_party/WebKit/Source/wtf/OwnPtrCommon.h:47


### ha...@chromium.org (2013-09-04)

Sorry, this would be a different issue from 223962.

The culprit is that we don't protect m_reverb with MutexLocker.

double ConvolverNode::tailTime() const
{
    // MutexLocker is missing. Thus m_reverb conflicts between threads.
    return m_reverb ? m_reverb->impulseResponseLength() / static_cast<double>(sampleRate()) : 0;
}


### ha...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157243

------------------------------------------------------------------------
r157243 | haraken@chromium.org | 2013-09-04T20:59:04.151644Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/ConvolverNode.cpp?r1=157243&r2=157242&pathrev=157243

Fix threading races on ConvolverNode::m_reverb in ConvolverNode::tailTime()

According to the crash report (https://cluster-fuzz.appspot.com/testcase?key=6515787040817152),
ConvolverNode::m_reverb races between ConvolverNode::tailTime() and ConvolverNode::setBuffer().
This CL adds a proper lock for ConvolverNode::m_reverb.

BUG=284785
No tests because the crash depends on threading races and thus not reproducible.

Review URL: https://chromiumcodereview.appspot.com/23926002
------------------------------------------------------------------------

### ha...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### bu...@chromium.org (2013-09-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157693

------------------------------------------------------------------------
r157693 | haraken@chromium.org | 2013-09-12T19:24:45.206507Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/modules/webaudio/ConvolverNode.cpp?r1=157693&r2=157692&pathrev=157693

Merge 157243 "Fix threading races on ConvolverNode::m_reverb in ..."

> Fix threading races on ConvolverNode::m_reverb in ConvolverNode::tailTime()
> 
> According to the crash report (https://cluster-fuzz.appspot.com/testcase?key=6515787040817152),
> ConvolverNode::m_reverb races between ConvolverNode::tailTime() and ConvolverNode::setBuffer().
> This CL adds a proper lock for ConvolverNode::m_reverb.
> 
> BUG=284785
> No tests because the crash depends on threading races and thus not reproducible.
> 
> Review URL: https://chromiumcodereview.appspot.com/23926002

TBR=haraken@chromium.org

Review URL: https://codereview.chromium.org/23600046
------------------------------------------------------------------------

### ha...@chromium.org (2013-09-12)

Merged into M30.

### in...@chromium.org (2013-09-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### mb...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-09-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### gl...@chromium.org (2015-06-29)

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

This issue was migrated from crbug.com/chromium/284785?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078041)*
