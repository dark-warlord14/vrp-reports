# Heap-use-after-free in WebCore::Reverb::latencyFrames

| Field | Value |
|-------|-------|
| **Issue ID** | [40077300](https://issues.chromium.org/issues/40077300) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Blink>Media>Audio |
| **Reporter** | in...@chromium.org |
| **Assignee** | ha...@chromium.org |
| **Created** | 2013-03-26 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=174623476

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x601600198e18
Crash State:
  - crash stack -
  WebCore::Reverb::latencyFrames
  WebCore::ConvolverNode::latencyTime
  - free stack -
  WebCore::ConvolverNode::setBuffer
  v8::internal::StoreCallbackProperty
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv963UOGM6m7-Ikip6VCdsBOhx1nkgvx4UVN73ewy8ukHON0gh-xQdAsQ_iiizQFppjfZhSico0zcttMSEKMVo9qIkNk_4qhXuAUn6ztyFmMNjhZPZNFosJaHk5BWYWA5P2YOL9c6GiJXrrnTMN46ixeAgR7NAmRkcbC6KmCc4U9oCNOK-ac

Additional requirements: Requires Interaction Gestures

## Attachments

- [races](attachments/races) (text/plain; charset=us-ascii, 599.9 KB)

## Timeline

### in...@chromium.org (2013-03-26)

Unreliable testcase, but free stack can give an idea on the bug.

### in...@chromium.org (2013-03-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-03-26)

See the thread numbers, freed in one thread and used in another.

READ of size 8 at 0x601600198e18 thread T7 (AudioOutputDevi)
    #0 0x7fc729aedfe9 in WebCore::Reverb::latencyFrames() const third_party/WebKit/Source/WTF/wtf/Vector.h:547
    #1 0x7fc72557971f in WebCore::ConvolverNode::latencyTime() const 
0x601600198e18 is located 8 bytes inside of 40-byte region [0x601600198e10,0x601600198e38)
freed by thread T0 (chrome) here:
    #0 0x7fc720c6ceb2 in operator delete(void*)
    #1 0x7fc72557926d in WebCore::ConvolverNode::setBuffer(WebCore::AudioBuffer*) third_party/WebKit/Source/WTF/wtf/OwnPtr.h:141
    #2 0x7fc724160c25 in v8::internal::StoreCallbackProperty(v8::internal::Arguments, v8::internal::Isolate*) v8/src/stub-cache.cc:1048

### kc...@chromium.org (2013-03-27)

can we try this with tsan v2? 

### gl...@chromium.org (2013-03-27)

There's a whole bunch of TSan v2 races, some include WebCore::Reverb and other media-related code. Will take a look.

### in...@chromium.org (2013-03-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=175159532

Fuzzer: Attekett_webaudio_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x600a000c0af8
Crash State:
  - crash stack -
  WebCore::Reverb::latencyFrames
  WebCore::ConvolverNode::latencyTime
  - free stack -
  WebCore::ConvolverNode::setBuffer
  v8::internal::JSObject::SetPropertyWithCallback
  


Additional requirements: Requires Interaction Gestures

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-16)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-16)

James, do you plan to contribute to Blink? If not we will need to find new owners for these security bugs.

Thanks!

### [Deleted User] (2013-04-17)

 will investigate this issue after this patch landed: https://codereview.chromium.org/14042005/

### in...@chromium.org (2013-04-25)

Don't see this anymore. We won't have a way to verify this one-time-crasher as duplicate, unless it hits again. Closing.

### sc...@gmail.com (2013-05-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-03)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6724805919244288

Fuzzer: Attekett_webaudio_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x611000c9e394
Crash State:
  - crash stack -
  WebCore::Reverb::latencyFrames
  WebCore::ConvolverNode::latencyTime
  - free stack -
  WebCore::ConvolverNode::setBuffer
  WebCore::ConvolverNodeV8Internal::bufferAttributeSetterCallback
  


Unreliable crash found using linux_tsan_chrome_mp job type (history_size=6).
Additional requirements: Requires Interaction Gestures



### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-09-03)

Fixing severity based on the fact, that all of these are race conditions (free, crash on different threads). No reliable reproducer.

### gr...@chromium.org (2013-09-03)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-09-04)

The culprit would be that we don't protect the access to m_reverb with MutexLock.

double ConvolverNode::latencyTime() const
{
    // MutexLocker is missing. Thus thread conflicts.
    return m_reverb ? m_reverb->latencyFrames() / static_cast<double>(sampleRate()) : 0;
}

I'll write a CL soon.

### ha...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### ha...@chromium.org (2013-09-04)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-09-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157245

------------------------------------------------------------------------
r157245 | haraken@chromium.org | 2013-09-04T21:23:14.917120Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/ConvolverNode.cpp?r1=157245&r2=157244&pathrev=157245

Fix threading races on ConvolverNode::m_reverb in ConvolverNode::latencyFrames()

According to the crash report (https://cluster-fuzz.appspot.com/testcase?key=6515787040817152),
ConvolverNode::m_reverb races between ConvolverNode::latencyFrames() and ConvolverNode::setBuffer().
This CL adds a proper lock for ConvolverNode::m_reverb.

BUG=223962
No tests because the crash depends on threading races and thus not reproducible.

Review URL: https://chromiumcodereview.appspot.com/23514037
------------------------------------------------------------------------

### in...@chromium.org (2013-09-05)

I will keep monitoring the CF for this webaudio crash once this blink change rolls into chromium. 

### in...@chromium.org (2013-09-12)

Please merge your change to the m30 branch (1599) by early next week [using drover]. We have m30 beta coming next week and we want all the security changes in by that time. 

### bu...@chromium.org (2013-09-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=157690

------------------------------------------------------------------------
r157690 | haraken@chromium.org | 2013-09-12T19:21:20.634216Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1599/Source/modules/webaudio/ConvolverNode.cpp?r1=157690&r2=157689&pathrev=157690

Merge 157245 "Fix threading races on ConvolverNode::m_reverb in ..."

> Fix threading races on ConvolverNode::m_reverb in ConvolverNode::latencyFrames()
> 
> According to the crash report (https://cluster-fuzz.appspot.com/testcase?key=6515787040817152),
> ConvolverNode::m_reverb races between ConvolverNode::latencyFrames() and ConvolverNode::setBuffer().
> This CL adds a proper lock for ConvolverNode::m_reverb.
> 
> BUG=223962
> No tests because the crash depends on threading races and thus not reproducible.
> 
> Review URL: https://chromiumcodereview.appspot.com/23514037

TBR=haraken@chromium.org

Review URL: https://codereview.chromium.org/24123002
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

@attekett: thanks, we'll be tagging most of these racy bugs at $500. If ever you were able to get the repro deterministic and demonstrate a controllable corruption, there's the liklihood that the new reward rules would enable a higher reward.

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

This issue was migrated from crbug.com/chromium/223962?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Media>Audio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077300)*
