# Heap-use-after-free in blink::Node::recalcDistribution

| Field | Value |
|-------|-------|
| **Issue ID** | [40081631](https://issues.chromium.org/issues/40081631) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Reporter** | at...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2015-03-16 |
| **Bounty** | $2,000.00 |

## Description


Tested on:

OS: Ubuntu 14.04

Chromium: linux-release-asan-symbolized-linux-release-320284

ASAN-trace:

==1067==ERROR: AddressSanitizer: heap-use-after-free on address 0x60b000010dd8 at pc 0x7f73659c911c bp 0x7fff47e8bbb0 sp 0x7fff47e8bba8
READ of size 4 at 0x60b000010dd8 thread T0 (chrome)
    #0 0x7f73659c911b in blink::Node::getFlag(blink::Node::NodeFlags) const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.h:735:49
    #1 0x7f7366590bda in blink::Node::youngestShadowRoot() const /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/shadow/ElementShadow.h:114:10
    #2 0x7f736670d91b in blink::Node::recalcDistribution() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:686:29
    #3 0x7f736670c42a in blink::Node::updateDistribution() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:671:9
    #4 0x7f7367866a86 in blink::KeyframeEffectModelBase::forceConversionsToAnimatableValues(blink::Element&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/animation/KeyframeEffectModel.cpp:71:5
    #5 0x7f7367861a41 in blink::EffectInput::convert(blink::Element*, WTF::Vector<blink::Dictionary, 0ul, WTF::DefaultAllocator> const&, blink::ExceptionState&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/animation/EffectInput.cpp:119:5
    #6 0x7f736786272c in blink::EffectInput::convert(blink::Element*, blink::AnimationEffectOrDictionarySequence const&, blink::ExceptionState&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/animation/EffectInput.cpp:129:16
.
.
.
0x60b000010dd8 is located 24 bytes inside of 112-byte region [0x60b000010dc0,0x60b000010e30)
freed by thread T0 (chrome) here:
    #0 0x7f7360a4bd9b in __interceptor_free ??:0:0
    #1 0x7f73667215c4 in blink::Node::removedLastRef() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/Node.cpp:2266:5
    #2 0x7f73659cac43 in blink::TreeShared<blink::Node>::deref() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/TreeShared.h:82:13
    #3 0x7f736659b96b in derefIfNotNull<blink::Node> /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/PassRefPtr.h:57:13
    #4 0x7f736659b96b in ~RefPtr /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:55:0
    #5 0x7f736659b96b in WTF::VectorDestructor<true, WTF::RefPtr<blink::Node> >::destruct(WTF::RefPtr<blink::Node>*, WTF::RefPtr<blink::Node>*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Vector.h:72:0
    #6 0x7f736659b52a in WTF::Vector<WTF::RefPtr<blink::Node>, 0ul, WTF::DefaultAllocator>::finalize() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Vector.h:667:17
    #7 0x7f736682b10b in blink::DistributionPool::distributeTo(blink::InsertionPoint*, blink::ElementShadow*) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/dom/shadow/ElementShadow.cpp:110:1
.
.
.

## Attachments

- [chrome-heap-use-after-free-blinkNodegetFlag10-min.html](attachments/chrome-heap-use-after-free-blinkNodegetFlag10-min.html) (text/html, 4.4 KB)

## Timeline

### cl...@chromium.org (2015-03-16)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5737541207064576

### in...@chromium.org (2015-03-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5737541207064576

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f0000135f8
Crash State:
  blink::Node::recalcDistribution
  blink::Node::updateDistribution
  blink::KeyframeEffectModelBase::forceConversionsToAnimatableValues
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=318001:318044

Minimized Testcase (1.88 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94SLzGB8BjPegAEdmYsvE5W6A3mF7sjKYoPTRnKYztM9_kzLyGNMITdKhbDb1dfaItDq8oCvZDGeZFbCI-Tnq-EgtsjhDZzCclnraYM9vSJw11fQnA9WsrwccYEeZCoBgABqdR0TBcVZrCHwBo2ZAvaiiaDdg



### wf...@chromium.org (2015-03-16)

[Empty comment from Monorail migration]

### wf...@chromium.org (2015-03-16)

Kojii - can you take a look at this regression please?

### cl...@chromium.org (2015-03-16)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ko...@chromium.org (2015-03-17)

alancutter@, any ideas? I don't think reverting my CL would help.

### al...@chromium.org (2015-03-19)

I've minified the test case to the following:
<div id="outer">
  <summary id="summary">
    <div>
      <div id="appender"></div>
    </div>
  </summary>
</div>
<script>
var summary = document.getElementById("summary");
var appender = document.getElementById("appender");
outer.innerHTML = '';
summary.animate([]);
summary.innerHTML = '';
appender.appendChild(summary);
summary.animate([]);
</script>

Removing the call to element.updateDistribution() from forceConversionsToAnimatableValues() (called by animate([])) fixes the UAF.
Doing this is effectively reverting: https://codereview.chromium.org/956493002
This will reintroduce an ASSERT failure (crbug.com/427398) but it doesn't crash release ASAN so that's preferable to a UAF.

If you add "void updateDistribution();" to Node.idl and call that instead of animate([]) the UAF still occurs.
I'm not familiar with node distributions or why this is causing a UAF. +hayato for advice.


### bu...@chromium.org (2015-03-20)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=192147

------------------------------------------------------------------
r192147 | alancutter@chromium.org | 2015-03-19T09:58:37.317317Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/animation/KeyframeEffectModel.cpp?r1=192147&r2=192146&pathrev=192147
   D http://src.chromium.org/viewvc/blink/trunk/LayoutTests/animations/animation-shadow-element-crash.html?r1=192147&r2=192146&pathrev=192147

Remove bad call to element.updateDistribution()

This change avoids a call to element.updateDistribution() from
element.animate() due to corner case conditions causing chaos.
This is only a hot fix and does not resolve the root problem
uncovered by calling element.updateDistribution().

BUG=467452,427398

Review URL: https://codereview.chromium.org/1021683002
-----------------------------------------------------------------

### al...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-03-20)

ClusterFuzz has detected this issue as fixed in range 321145:321437.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5737541207064576

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x60f0000135f8
Crash State:
  blink::Node::recalcDistribution
  blink::Node::updateDistribution
  blink::KeyframeEffectModelBase::forceConversionsToAnimatableValues
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=318001:318044
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=321145:321437

Minimized Testcase (1.88 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94SLzGB8BjPegAEdmYsvE5W6A3mF7sjKYoPTRnKYztM9_kzLyGNMITdKhbDb1dfaItDq8oCvZDGeZFbCI-Tnq-EgtsjhDZzCclnraYM9vSJw11fQnA9WsrwccYEeZCoBgABqdR0TBcVZrCHwBo2ZAvaiiaDdg

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ti...@google.com (2015-06-14)

Congrats - $2,000 for this report

FYI - this one will also go through the new payment process.

### ti...@google.com (2015-06-25)

Processing rewards - should be paid in approximately 2 weeks.

### cl...@chromium.org (2015-06-26)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/467452?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081631)*
