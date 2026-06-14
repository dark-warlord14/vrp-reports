# Use-of-uninitialized-value in blink::PropertyHandle::operator==

| Field | Value |
|-------|-------|
| **Issue ID** | [40085579](https://issues.chromium.org/issues/40085579) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Animation |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2016-10-03 |
| **Bounty** | $2,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6656629452046336

Fuzzer: attekett_dom_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::PropertyHandle::operator==
  std::__1::pair<WTF::KeyValuePair<blink::PropertyHandle, std::__1::unique_ptr<WTF
  blink::PropertyInterpolationTypesMapping::get
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=421807:422067

Minimized Testcase (0.84 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95xNAB75BRYMmj4hN3hjUQtPBIYCDOwzVKF6ZuS3vXksePNTk7qxc-fqMUlADR1XYYosAnEX4jVoHtWdLOcWDR54oChguXWXv0gygc3fvXpMDUXIV7FOLzpRKk021Iz5aahGZ2dDuIz3WpgsknTYVSpDmUaRQ?testcase_id=6656629452046336

Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2016-10-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-03)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-03)

[Empty comment from Monorail migration]

### ke...@chromium.org (2016-10-03)

Suspecting: https://chromium.googlesource.com/chromium/src/+/294c014b805fae756af944846f9ef21a85a71d49

alancutter: Can you please take a look? If your CL isn't the cause then can you suggest a better owner?

[Monorail components: Blink>Animation]

### al...@chromium.org (2016-10-04)

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x60300002f268 at pc 0x7f4f67a96736 bp 0x7ffcd8832ab0 sp 0x7ffcd8832aa8
READ of size 4 at 0x60300002f268 thread T0 (content_shell)
    #0 0x7f4f67a96735 in existingHash ./out/asan/../../third_party/WebKit/Source/wtf/text/StringImpl.h:274:12
    #1 0x7f4f67a96735 in hash ./out/asan/../../third_party/WebKit/Source/core/animation/PropertyHandle.cpp:31:0
    #2 0x7f4f67aaac21 in hash ./out/asan/../../third_party/WebKit/Source/core/animation/PropertyHandle.h:118:21
    #3 0x7f4f67aaac21 in hash<blink::PropertyHandle> ./out/asan/../../third_party/WebKit/Source/wtf/HashTable.h:464:0
    #4 0x7f4f67aaac21 in lookupForWriting<WTF::IdentityHashTranslator<WTF::DefaultHash<blink::PropertyHandle>::Hash>, blink::PropertyHandle> ./out/asan/../../third_party/WebKit/Source/wtf/HashTable.h:1046:0
    #5 0x7f4f67aaa473 in lookupForWriting ./out/asan/../../third_party/WebKit/Source/wtf/HashTable.h:779:12
    #6 0x7f4f67aaa473 in reinsert ./out/asan/../../third_party/WebKit/Source/wtf/HashTable.h:1339:0
    #7 0x7f4f67aaa473 in rehashTo ./out/asan/../../third_party/WebKit/Source/wtf/HashTable.h:1687:0
    #8 0x7f4f67aaa473 in rehash ./out/asan/../../third_party/WebKit/Source/wtf/HashTable.h:1733:0
    #9 0x7f4f67aa9e2c in expand ./out/asan/../../third_party/WebKit/Source/wtf/HashTable.h:1591:10
    #10 0x7f4f67aa9ac5 in add<WTF::HashMapTranslator<WTF::HashMapValueTraits<WTF::HashTraits<blink::PropertyHandle>, WTF::HashTraits<std::__1::unique_ptr<const WTF::Vector<std::__1::unique_ptr<const blink::InterpolationType, std::__1::default_delete<const blink::InterpolationType> >, 0, WTF::PartitionAllocator>, std::__1::default_delete<const WTF::Vector<std::__1::unique_ptr<const blink::InterpolationType, std::__1::default_delete<const blink::InterpolationType> >, 0, WTF::PartitionAllocator> > > > >, WTF::DefaultHash<blink::PropertyHandle>::Hash>, const blink::PropertyHandle &, std::__1::unique_ptr<WTF::Vector<std::__1::unique_ptr<const blink::InterpolationType, std::__1::default_delete<const blink::InterpolationType> >, 0, WTF::PartitionAllocator>, std::__1::default_delete<WTF::Vector<std::__1::unique_ptr<const blink::InterpolationType, std::__1::default_delete<const blink::InterpolationType> >, 0, WTF::PartitionAllocator> > > > ./out/asan/../../third_party/WebKit/Source/wtf/HashTable.h:1248:13
    #11 0x7f4f67a9cf29 in inlineAdd<const blink::PropertyHandle &, std::__1::unique_ptr<WTF::Vector<std::__1::unique_ptr<const blink::InterpolationType, std::__1::default_delete<const blink::InterpolationType> >, 0, WTF::PartitionAllocator>, std::__1::default_delete<WTF::Vector<std::__1::unique_ptr<const blink::InterpolationType, std::__1::default_delete<const blink::InterpolationType> >, 0, WTF::PartitionAllocator> > > > ./out/asan/../../third_party/WebKit/Source/wtf/HashMap.h:480:26
    #12 0x7f4f67a9cf29 in add<const blink::PropertyHandle &, std::__1::unique_ptr<WTF::Vector<std::__1::unique_ptr<const blink::InterpolationType, std::__1::default_delete<const blink::InterpolationType> >, 0, WTF::PartitionAllocator>, std::__1::default_delete<WTF::Vector<std::__1::unique_ptr<const blink::InterpolationType, std::__1::default_delete<const blink::InterpolationType> >, 0, WTF::PartitionAllocator> > > > ./out/asan/../../third_party/WebKit/Source/wtf/HashMap.h:536:0
    #13 0x7f4f67a9cf29 in get ./out/asan/../../third_party/WebKit/Source/core/animation/PropertyInterpolationTypesMapping.cpp:425:0
    #14 0x7f4f67a5f8f4 in createInterpolation ./out/asan/../../third_party/WebKit/Source/core/animation/Keyframe.cpp:18:23
    #15 0x7f4f67a565c3 in addInterpolationsFromKeyframes ./out/asan/../../third_party/WebKit/Source/core/animation/InterpolationEffect.cpp:44:30
    #16 0x7f4f67a6b52e in ensureInterpolationEffectPopulated ./out/asan/../../third_party/WebKit/Source/core/animation/KeyframeEffectModel.cpp:242:31




freed by thread T0 (content_shell) here:
    #0 0x525b2b in __interceptor_free ??:?
    #1 0x7f4f6ddc15a6 in finalize ./out/asan/../../third_party/WebKit/Source/platform/heap/HeapPage.cpp:104:5
    #2 0x7f4f6ddc8bed in sweep ./out/asan/../../third_party/WebKit/Source/platform/heap/HeapPage.cpp:1216:15
    #3 0x7f4f6ddc3a70 in sweepUnsweptPage ./out/asan/../../third_party/WebKit/Source/platform/heap/HeapPage.cpp:296:11
    #4 0x7f4f6ddc3a70 in completeSweep ./out/asan/../../third_party/WebKit/Source/platform/heap/HeapPage.cpp:349:0
    #5 0x7f4f6ddd0fc4 in completeSweep ./out/asan/../../third_party/WebKit/Source/platform/heap/ThreadState.cpp:1202:20
    #6 0x7f4f6ddd66e6 in leaveSafePoint ./out/asan/../../third_party/WebKit/Source/platform/heap/ThreadState.cpp:1378:3
    #7 0x7f4f6ddd66e6 in ~SafePointScope ./out/asan/../../third_party/WebKit/Source/platform/heap/SafePoint.h:29:0
    #8 0x7f4f6ddd66e6 in collectGarbage ./out/asan/../../third_party/WebKit/Source/platform/heap/ThreadState.cpp:1777:0
    #9 0x7f4f6ddd9e50 in collectAllGarbage ./out/asan/../../third_party/WebKit/Source/platform/heap/ThreadState.cpp:1822:5
    #10 0x7f4f6ddd9e50 in runScheduledGC ./out/asan/../../third_party/WebKit/Source/platform/heap/ThreadState.cpp:1020:0




previously allocated by thread T0 (content_shell) here:
    #0 0x525e7c in __interceptor_malloc ??:?
    #1 0x7f4f6c21e6f9 in partitionAllocGenericFlags ./out/asan/../../third_party/WebKit/Source/wtf/allocator/PartitionAlloc.h:821:18
    #2 0x7f4f6c21e6f9 in partitionAllocGeneric ./out/asan/../../third_party/WebKit/Source/wtf/allocator/PartitionAlloc.h:851:0
    #3 0x7f4f6c21e6f9 in bufferMalloc ./out/asan/../../third_party/WebKit/Source/wtf/allocator/Partitions.h:91:0
    #4 0x7f4f6c21e6f9 in createUninitialized ./out/asan/../../third_party/WebKit/Source/wtf/text/StringImpl.cpp:333:0
    #5 0x7f4f67868560 in createUninitialized ./out/asan/../../third_party/WebKit/Source/wtf/text/WTFString.h:310:12
    #6 0x7f4f67868560 in fromV8String<blink::V8StringOneByteTrait> ./out/asan/../../third_party/WebKit/Source/bindings/core/v8/V8StringResource.cpp:81:0
    #7 0x7f4f67868560 in v8StringToWebCoreString<WTF::String> ./out/asan/../../third_party/WebKit/Source/bindings/core/v8/V8StringResource.cpp:127:0
    #8 0x7f4f67761a59 in toString<WTF::String> ./out/asan/../../third_party/WebKit/Source/bindings/core/v8/V8StringResource.h:254:14
    #9 0x7f4f67761a59 in operator String ./out/asan/../../third_party/WebKit/Source/bindings/core/v8/V8StringResource.h:218:0
    #10 0x7f4f67761a59 in appendSlowCase<blink::V8StringResource<blink::V8StringResourceMode::DefaultMode> &> ./out/asan/../../third_party/WebKit/Source/wtf/Vector.h:1418:0
    #11 0x7f4f6775fb77 in append<blink::V8StringResource<blink::V8StringResourceMode::DefaultMode> &> ./out/asan/../../third_party/WebKit/Source/wtf/Vector.h:1388:3
    #12 0x7f4f6775fb77 in getPropertyNames ./out/asan/../../third_party/WebKit/Source/bindings/core/v8/Dictionary.cpp:164:0
    #13 0x7f4f67a3e6ee in convertArrayForm ./out/asan/../../third_party/WebKit/Source/core/animation/EffectInput.cpp:234:24
    #14 0x7f4f67a3d714 in convert ./out/asan/../../third_party/WebKit/Source/core/animation/EffectInput.cpp:174:12
    #15 0x7f4f69baaa61 in animate ./out/asan/../../third_party/WebKit/Source/core/animation/ElementAnimation.h:76:27
    #16 0x7f4f69ba64e9 in animate2Method ./out/asan/gen/blink/bindings/core/v8/V8Element.cpp:2529:25
    #17 0x7f4f69ba64e9 in animateMethod ./out/asan/gen/blink/bindings/core/v8/V8Element.cpp:2555:0
    #18 0x7f4f69ba64e9 in animateMethodCallback ./out/asan/gen/blink/bindings/core/v8/V8Element.cpp:2581:0

### bu...@chromium.org (2016-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/71dd575dd664dcfa639dab8e9a1e469084df2d40

commit 71dd575dd664dcfa639dab8e9a1e469084df2d40
Author: alancutter <alancutter@chromium.org>
Date: Tue Oct 04 07:46:40 2016

Use AtomicString instead of StringImpl* in PropertyHandle

This patch avoids using raw pointers to AtomicString contents for
animation PropertyHandles. By making the AtomicString class a member
all the necessary reference counting occurs.

BUG=652127

Review-Url: https://codereview.chromium.org/2390203002
Cr-Commit-Position: refs/heads/master@{#422731}

[add] https://crrev.com/71dd575dd664dcfa639dab8e9a1e469084df2d40/third_party/WebKit/LayoutTests/animations/custom-property-animation-crash.html
[modify] https://crrev.com/71dd575dd664dcfa639dab8e9a1e469084df2d40/third_party/WebKit/Source/core/animation/PropertyHandle.cpp
[modify] https://crrev.com/71dd575dd664dcfa639dab8e9a1e469084df2d40/third_party/WebKit/Source/core/animation/PropertyHandle.h


### al...@chromium.org (2016-10-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-10-05)

ClusterFuzz has detected this issue as fixed in range 422674:422794.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6656629452046336

Fuzzer: attekett_dom_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  blink::PropertyHandle::operator==
  std::__1::pair<WTF::KeyValuePair<blink::PropertyHandle, std::__1::unique_ptr<WTF
  blink::PropertyInterpolationTypesMapping::get
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=421807:422067
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=422674:422794

Minimized Testcase (0.84 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95xNAB75BRYMmj4hN3hjUQtPBIYCDOwzVKF6ZuS3vXksePNTk7qxc-fqMUlADR1XYYosAnEX4jVoHtWdLOcWDR54oChguXWXv0gygc3fvXpMDUXIV7FOLzpRKk021Iz5aahGZ2dDuIz3WpgsknTYVSpDmUaRQ?testcase_id=6656629452046336

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2016-10-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

And $2,500 for this one!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-01-10)

This issue was migrated from crbug.com/chromium/652127?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085579)*
