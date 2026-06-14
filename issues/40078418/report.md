# Heap-use-after-free in WebCore::V8SVGStringList::resolveWrapperReachability

| Field | Value |
|-------|-------|
| **Issue ID** | [40078418](https://issues.chromium.org/issues/40078418) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SVG |
| **Reporter** | cl...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2013-11-19 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes chrome's ASAN build.

**VERSION**  

Chrome Version: asan-symbolized-linux-release-235520  

Operating System: Linux 64 bit

**REPRODUCTION CASE**

<script>
try{o568;}catch(e){}
o568=document.createElementNS('http://www.w3.org/2000/svg', 'g');
o569=o568.systemLanguage;
o568=null;
window.location.reload(true);
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: ASAN output attached in stack.txt

## Attachments

- [stack.txt](attachments/stack.txt) (text/plain, 13.5 KB)

## Timeline

### in...@chromium.org (2013-11-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-19)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=6458041524289536

### in...@chromium.org (2013-11-19)

This is similar to https://code.google.com/p/chromium/issues/detail?id=318577. This code is in active churn and we have crash stacks already on CF. Some got fixed, and we are filing bugs as they are getting fixed. Filing the new ones here.

### cl...@chromium.org (2013-11-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5876164614684672

Fuzzer: Inferno_twister_custom_bundle
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000008a48
Crash State:
  - crash stack -
  WebCore::V8SVGStringList::resolveWrapperReachability
  WebCore::MajorGCWrapperVisitor::VisitPersistentHandle
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=234486:234493

Minimized Testcase (6.92 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96itWpqy_YvN1_xzIllWk9vBWMHJgKJ100YnGtzrqn1oWHRadKL0d5TrLWfFCN-jl3scKSEd-Qwu0sDyqEIjroCAfHVizscs3jUqFLodhUEq0Xhm-l0X01YEZ183bCefB_VCxZP76GHPXrVsetSA7BUHAabnQ



### in...@chromium.org (2013-11-19)

another regression from http://src.chromium.org/viewvc/blink?view=rev&revision=161752

### cl...@chromium.org (2013-11-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5417571763355648

Fuzzer: Ifratric-browserfuzzer-v3
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x07f6377f
Crash State:
  - crash stack -
  WebCore::DOMDataStore::containsWrapper<WebCore::V8SVGElement,WebCore::SVGElement>
  WebCore::V8SVGStringList::resolveWrapperReachability
  - free stack -
  WebCore::SVGForeignObjectElement::`scalar deleting destructor'
  WebCore::Node::removedLastRef
  




### cl...@chromium.org (2013-11-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5672712190033920

Fuzzer: Ifratric-browserfuzzer-v3
Job Type: Windows_syzyasan_chrome

Crash Type: Use-after-free READ 4
Crash Address: 0x07e52357
Crash State:
  - crash stack -
  WebCore::DOMDataStore::containsWrapper<WebCore::V8SVGElement,WebCore::SVGPathElement>
  WebCore::V8SVGStringList::resolveWrapperReachability
  - free stack -
  WebCore::SVGEllipseElement::`scalar deleting destructor'
  WebCore::Node::removedLastRef
  


Additional requirements: Requires Interaction Gestures



### cl...@chromium.org (2013-11-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6643784431435776

Fuzzer: Inferno_layout_test_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000008c48
Crash State:
  - crash stack -
  WebCore::V8SVGStringList::resolveWrapperReachability
  WebCore::MajorGCWrapperVisitor::VisitPersistentHandle
  - free stack -
  void WebCore::removeDetachedChildrenInContainer<WebCore::Node, WebCore::ContainerNode>
  WebCore::ContainerNode::~ContainerNode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=234486:234493

Minimized Testcase (0.78 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94Oep59QQQJgglmMQDbwI0HqlGVWIWfbAxQVm8ChNkxEs9GryQjvbFDs1q6y38TRuGJPZz-_AnY5cTf_LWIhKVUnuVeLT2PosAmnYwkgBmGnihrBzneYI6moSSHs7E8CHkHE-NlPMA6g9ol023xu1lUOajjxw



### ko...@chromium.org (2013-11-19)

This should be already fixed in https://src.chromium.org/viewvc/blink?revision=162274&view=revision

### cl...@chromium.org (2013-11-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6458041524289536

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61400006f088
Crash State:
  - crash stack -
  WebCore::V8SVGStringList::resolveWrapperReachability
  WebCore::MajorGCWrapperVisitor::VisitPersistentHandle
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=234486:234493

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94Juya2fE85MKtcD77OPAAdL6xS2ZhbWHDAdyvrfijkKry9d1R8fR55ylvN3y8q0eU4gi1x7-dvNZJTEmTiIDqFXgeL0FcArWfQY1c9YFniDGkgJKdFIHKq7VZZjaBxPRkyyvPgUnxYPHQWHvANL6WYTqAkGA



### ko...@chromium.org (2013-11-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-19)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

Adding ReleaseBlock-Stable label.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-11-19)

Kouhei's lets come back after a day or two and make sure all the repros are fixed. I mean just check CF notifications for each of these testcase entries.

### cl...@chromium.org (2013-11-20)

ClusterFuzz has detected this issue as fixed in range 236036:236160.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6458041524289536

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x61400006f088
Crash State:
  - crash stack -
  WebCore::V8SVGStringList::resolveWrapperReachability
  WebCore::MajorGCWrapperVisitor::VisitPersistentHandle
  - free stack -
  v8::internal::GlobalHandles::Node::PostGarbageCollectionProcessing
  v8::internal::GlobalHandles::PostGarbageCollectionProcessing
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=234486:234493
Fixed: https://cluster-fuzz.appspot.com/revisions?range=236036:236160

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94Juya2fE85MKtcD77OPAAdL6xS2ZhbWHDAdyvrfijkKry9d1R8fR55ylvN3y8q0eU4gi1x7-dvNZJTEmTiIDqFXgeL0FcArWfQY1c9YFniDGkgJKdFIHKq7VZZjaBxPRkyyvPgUnxYPHQWHvANL6WYTqAkGA

Unreliable crash found using linux_tsan_chrome_mp job type (history_size=6).

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-11-20)

ClusterFuzz has detected this issue as fixed in range 236036:236160.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6643784431435776

Fuzzer: Inferno_layout_test_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x614000008c48
Crash State:
  - crash stack -
  WebCore::V8SVGStringList::resolveWrapperReachability
  WebCore::MajorGCWrapperVisitor::VisitPersistentHandle
  - free stack -
  void WebCore::removeDetachedChildrenInContainer<WebCore::Node, WebCore::ContainerNode>
  WebCore::ContainerNode::~ContainerNode
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=234486:234493
Fixed: https://cluster-fuzz.appspot.com/revisions?range=236036:236160

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94Oep59QQQJgglmMQDbwI0HqlGVWIWfbAxQVm8ChNkxEs9GryQjvbFDs1q6y38TRuGJPZz-_AnY5cTf_LWIhKVUnuVeLT2PosAmnYwkgBmGnihrBzneYI6moSSHs7E8CHkHE-NlPMA6g9ol023xu1lUOajjxw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### ko...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-12-10)

Thanks for the report. This one qualifies for a $500 reward. Though we were hitting this bug in our fuzzing, the test case you provided was helpful in getting the bug fixed.

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-28)

Bulk update: removing view restriction from closed bugs.

### gl...@chromium.org (2015-06-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/321037?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078418)*
