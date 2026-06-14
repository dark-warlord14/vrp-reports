# Use-after-poison in blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,

| Field | Value |
|-------|-------|
| **Issue ID** | [40084711](https://issues.chromium.org/issues/40084711) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GarbageCollection, Blink>Workers |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | th...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2016-06-28 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5286150310985728

Fuzzer: therealholden_worker
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x574e97d0
Crash State:
  blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,
  blink::ThreadState::threadLocalWeakProcessing
  blink::ThreadState::preSweep
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=401864:401888

Minimized Testcase (2.52 Kb): https://cluster-fuzz.appspot.com/download/AMIfv957vJImnbvGf5iAzRCA6-tuR_28YYx3VbgL1ET1db6EZOlv6AeZXPgU9p3e04-JM_beiKnOrLNgic7HiMVucZ47R_ykLIdPyNCzkgExrz0UGw4wckhy7o8iZci7AnyqQA--IprPG6QwHeXSKokAXiMWnYOJ5Q?testcase_id=5286150310985728

Additional requirements: Requires HTTP

Filer: tanin

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### cl...@chromium.org (2016-06-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6139727615098880

Fuzzer: therealholden_worker
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Use-after-poison READ 4
Crash Address: 0x0ee286a4
Crash State:
  blink::PersistentBase<class blink::WorkerWebSocketChannel::Bridge,1,1>::handleWe
  blink::ThreadState::threadLocalWeakProcessing
  blink::ThreadState::preSweep
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome_no_sandbox&range=401970:402059

Minimized Testcase (2.89 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96oUds_1H5jK2crga5nbCtK5Z_aT6qxPDXnEuP_GGQ_NbaP0JWYledglmacK9jqvHP2Kuu6Be8C5rKTYE1P62xsjrRMiy7Fd-bmklj7eCPlpVpTPrlhpxFslI906gyHjXO32WjET5YXQpC7muARrAgqdR1bag?testcase_id=6139727615098880

Additional requirements: Requires HTTP

Filer: tanin

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-06-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5836974430879744

Fuzzer: inferno_layout_test_unmodified
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7eb96d6bc960
Crash State:
  blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,
  blink::ThreadState::threadLocalWeakProcessing
  blink::ThreadState::preSweep
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=401864:401888

Minimized Testcase (3.24 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97Yfzga9SHwsJJMPDEH6xK8KBxaK-o7CYEPXN6d4f0TfgwrowS3GzoJtYZHWg5GNPQsMy_4Yo-WL6Jh3UYslL9cg-5LgKdWA8i94s1cNXvNlGl5x4u2cMR_bmTg3GdDn2NJZrHfIRyMFlNylMzdBwKA75j6IQ?testcase_id=5836974430879744

Additional requirements: Requires HTTP

Filer: tanin

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-06-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5093201266606080

Fuzzer: therealholden_worker
Job Type: linux_debug_chrome
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ead9ada6e98
Crash State:
  blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,
  blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,
  blink::CallbackStack::Item::call
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_debug_chrome&range=401864:401888

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95RPHkudRike5zeLdojSXlIOPOMDPX5WzrorL-k56mZRajvsULWnml82sGI8hz99mHAWAVgVFC0hOwRwOwbLDVFWTEhD0z6s-YdHw3Cm8Zg7uNMP3FlmKABrrcR-6Id4NS_D5Oy7-uqWFukVikeVzcoaYo8dQ?testcase_id=5093201266606080


Additional requirements: Requires HTTP

Filer: tanin

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### pa...@chromium.org (2016-06-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-06-28)

[Empty comment from Monorail migration]

[Monorail components: Blink>Workers]

### [Deleted User] (2016-06-28)

Handling weak persistents during thread-local weak processing is not going to work for CrossThreadWeakPersistent<>s residing on other heap objects, and pointing to objects on another thread's heap. Like what WorkerWebSocketChannel::Peer::m_bridge is doing.

### [Deleted User] (2016-06-28)

https://codereview.chromium.org/2106863003/ addresses.

### bu...@chromium.org (2016-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a71167e5645142b200f917bf26b7a546e36a3574

commit a71167e5645142b200f917bf26b7a546e36a3574
Author: sigbjornf <sigbjornf@opera.com>
Date: Wed Jun 29 05:21:13 2016

Handle cross-thread weak persistents during global weak processing.

r401880 changed the handling of weak persistents, clearing
and releasing their underlying PersistentNodes once their
weak references point to otherwise unreferenced objects.

However, performing that weak processing step cannot reliably
be done as part of thread-local weak processing if the
weak persistent is a CrossThreadWeakPersistent<T> (CTWP) as the
object it refers to may reside on a different thread's heap than
where the CTWP resides. If both locations need to be accessed,
doing that as part of thread-local weak processing is too
late and unsafe.

Instead we process the cross-thread weak persistents along with the
'weak cells' during global weak processing. WeakPersistent<>s are
still handled during thread-local weak processing.

R=
BUG=623985

Review-Url: https://codereview.chromium.org/2106863003
Cr-Commit-Position: refs/heads/master@{#402734}

[modify] https://crrev.com/a71167e5645142b200f917bf26b7a546e36a3574/third_party/WebKit/Source/platform/heap/MarkingVisitor.h
[modify] https://crrev.com/a71167e5645142b200f917bf26b7a546e36a3574/third_party/WebKit/Source/platform/heap/MarkingVisitorImpl.h
[modify] https://crrev.com/a71167e5645142b200f917bf26b7a546e36a3574/third_party/WebKit/Source/platform/heap/Persistent.h
[modify] https://crrev.com/a71167e5645142b200f917bf26b7a546e36a3574/third_party/WebKit/Source/platform/heap/Visitor.h


### [Deleted User] (2016-06-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>MemoryAllocator>GarbageCollection]

### sh...@chromium.org (2016-06-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-29)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5836974430879744

Fuzzer: inferno_layout_test_unmodified
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7eb96d6bc960
Crash State:
  blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,
  blink::ThreadState::threadLocalWeakProcessing
  blink::ThreadState::preSweep
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=401864:401888

Minimized Testcase (3.24 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97Yfzga9SHwsJJMPDEH6xK8KBxaK-o7CYEPXN6d4f0TfgwrowS3GzoJtYZHWg5GNPQsMy_4Yo-WL6Jh3UYslL9cg-5LgKdWA8i94s1cNXvNlGl5x4u2cMR_bmTg3GdDn2NJZrHfIRyMFlNylMzdBwKA75j6IQ?testcase_id=5836974430879744

Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-06-30)

ClusterFuzz has detected this issue as fixed in range 402484:402485.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5093201266606080

Fuzzer: therealholden_worker
Job Type: linux_debug_chrome
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ead9ada6e98
Crash State:
  blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,
  blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,
  blink::CallbackStack::Item::call
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_debug_chrome&range=401864:401888
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_debug_chrome&range=402484:402485

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95RPHkudRike5zeLdojSXlIOPOMDPX5WzrorL-k56mZRajvsULWnml82sGI8hz99mHAWAVgVFC0hOwRwOwbLDVFWTEhD0z6s-YdHw3Cm8Zg7uNMP3FlmKABrrcR-6Id4NS_D5Oy7-uqWFukVikeVzcoaYo8dQ?testcase_id=5093201266606080


Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-06-30)

ClusterFuzz has detected this issue as fixed in range 402485:402737.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5286150310985728

Fuzzer: therealholden_worker
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Use-after-poison READ 4
Crash Address: 0x574e97d0
Crash State:
  blink::PersistentBase<blink::WorkerWebSocketChannel::Bridge,
  blink::ThreadState::threadLocalWeakProcessing
  blink::ThreadState::preSweep
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=401864:401888
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=402485:402737

Minimized Testcase (2.52 Kb): https://cluster-fuzz.appspot.com/download/AMIfv957vJImnbvGf5iAzRCA6-tuR_28YYx3VbgL1ET1db6EZOlv6AeZXPgU9p3e04-JM_beiKnOrLNgic7HiMVucZ47R_ykLIdPyNCzkgExrz0UGw4wckhy7o8iZci7AnyqQA--IprPG6QwHeXSKokAXiMWnYOJ5Q?testcase_id=5286150310985728

Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-06-30)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6139727615098880

Fuzzer: therealholden_worker
Job Type: windows_asan_chrome_no_sandbox
Platform Id: windows

Crash Type: Use-after-poison READ 4
Crash Address: 0x0ee286a4
Crash State:
  blink::PersistentBase<class blink::WorkerWebSocketChannel::Bridge,1,1>::handleWe
  blink::ThreadState::threadLocalWeakProcessing
  blink::ThreadState::preSweep
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_asan_chrome_no_sandbox&range=401970:402059

Minimized Testcase (2.89 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96oUds_1H5jK2crga5nbCtK5Z_aT6qxPDXnEuP_GGQ_NbaP0JWYledglmacK9jqvHP2Kuu6Be8C5rKTYE1P62xsjrRMiy7Fd-bmklj7eCPlpVpTPrlhpxFslI906gyHjXO32WjET5YXQpC7muARrAgqdR1bag?testcase_id=6139727615098880

Additional requirements: Requires HTTP

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

$3,500 for this one!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-09-16)

[Empty comment from Monorail migration]

[Monorail components: -Blink>MemoryAllocator>GarbageCollection Blink>GarbageCollection]

### is...@google.com (2021-09-16)

This issue was migrated from crbug.com/chromium/623985?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>GarbageCollection, Blink>Workers]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084711)*
