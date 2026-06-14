# Stack-use-after-return in v8::internal::HandleBase::IsDereferenceAllowed

| Field | Value |
|-------|-------|
| **Issue ID** | [40084668](https://issues.chromium.org/issues/40084668) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2016-06-23 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6008956061483008

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_dbg
Platform Id: linux

Crash Type: Stack-use-after-return READ 8
Crash Address: 0x7f6eaf8b5110
Crash State:
  v8::internal::HandleBase::IsDereferenceAllowed
  v8::internal::Builtin_Impl_ArrayPop
  v8::internal::Builtin_ArrayPop
  
Regressed: V8: r37179:37180

Minimized Testcase (9.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95yvMxZAaH3w2lwOgIRc8dPYadetH3pAVfnCpBW4uxa_RTf7_1eDcUF5YZWEBDMWcgHGb8z2vDEmQTUQm9J8sp1C1UJCwQS0TrshCVAr16mUTyhnyyxcAmJAX6LwVUOTcoy55r5tHIcgA8SYJCB309wGbNcUA?testcase_id=6008956061483008

Filer: rossberg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### ro...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6204317413670912

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_v8_arm_dbg
Platform Id: linux

Crash Type: Stack-use-after-return READ 4
Crash Address: 0xd4c86e78
Crash State:
  v8::internal::HandleBase::IsDereferenceAllowed
  v8::internal::ArrayConcatVisitor::visit
  v8::internal::IterateElementsSlow
  
Regressed: V8: r37179:37180

Minimized Testcase (7.06 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97hiFYngfI8zG6Wn7HHcZVMSNzl-cQtxVcExSj29m327ylmQKgTX6VqLajfjtEYrFCHL4rPDMBaHtYXhLRIAfd4cVaAYbhF1kLKUMXpN5da12HM0fOBTH3X4c9IfJ3tHmz_VIQ3Ck8RieWK-JyFXjm9aOir5g?testcase_id=6204317413670912

Filer: rossberg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-06-23)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6294138870038528

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_v8_arm_dbg
Platform Id: linux

Crash Type: Stack-use-after-return READ 4
Crash Address: 0xf5e53a78
Crash State:
  v8::internal::HandleBase::IsDereferenceAllowed
  v8::internal::JSReceiver::OrdinaryToPrimitive
  v8::internal::JSReceiver::ToPrimitive
  
Regressed: V8: r37179:37180

Minimized Testcase (8.50 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96ZrXX41XrzUphfgZRXoajFs3AP4XjQcgagdE3_dH9ZefxLR1VANbvfBgTKjegATvQN4PUMFKdr7Hytj4GLEHji3C0qZvoRu6xSvcZ847zK94qpXwrv8IOQf6SVjACm2y9MaZ2m0fOHQgK3nIndgTyc1pdp3w?testcase_id=6294138870038528

Additional requirements: Requires Gestures

Filer: rossberg

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### ve...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### do...@chromium.org (2016-06-24)

Tentatively assigning impact on tip of tree.

### sh...@chromium.org (2016-06-24)

The older reward-topanel https://crbug.com/chromium/622348 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### sh...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-24)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ve...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-24)

ClusterFuzz has detected this issue as fixed in range 37253:37254.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6008956061483008

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_dbg
Platform Id: linux

Crash Type: Stack-use-after-return READ 8
Crash Address: 0x7f6eaf8b5110
Crash State:
  v8::internal::HandleBase::IsDereferenceAllowed
  v8::internal::Builtin_Impl_ArrayPop
  v8::internal::Builtin_ArrayPop
  
Regressed: V8: r37179:37180
Fixed: V8: r37253:37254

Minimized Testcase (9.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95yvMxZAaH3w2lwOgIRc8dPYadetH3pAVfnCpBW4uxa_RTf7_1eDcUF5YZWEBDMWcgHGb8z2vDEmQTUQm9J8sp1C1UJCwQS0TrshCVAr16mUTyhnyyxcAmJAX6LwVUOTcoy55r5tHIcgA8SYJCB309wGbNcUA?testcase_id=6008956061483008

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-06-24)

ClusterFuzz has detected this issue as fixed in range 37253:37254.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6294138870038528

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_v8_arm_dbg
Platform Id: linux

Crash Type: Stack-use-after-return READ 4
Crash Address: 0xf5e53a78
Crash State:
  v8::internal::HandleBase::IsDereferenceAllowed
  v8::internal::JSReceiver::OrdinaryToPrimitive
  v8::internal::JSReceiver::ToPrimitive
  
Regressed: V8: r37179:37180
Fixed: V8: r37253:37254

Minimized Testcase (8.50 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96ZrXX41XrzUphfgZRXoajFs3AP4XjQcgagdE3_dH9ZefxLR1VANbvfBgTKjegATvQN4PUMFKdr7Hytj4GLEHji3C0qZvoRu6xSvcZ847zK94qpXwrv8IOQf6SVjACm2y9MaZ2m0fOHQgK3nIndgTyc1pdp3w?testcase_id=6294138870038528

Additional requirements: Requires Gestures

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-25)

ClusterFuzz has detected this issue as fixed in range 37253:37254.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6204317413670912

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_ignition_v8_arm_dbg
Platform Id: linux

Crash Type: Stack-use-after-return READ 4
Crash Address: 0xd4c86e78
Crash State:
  v8::internal::HandleBase::IsDereferenceAllowed
  v8::internal::ArrayConcatVisitor::visit
  v8::internal::IterateElementsSlow
  
Regressed: V8: r37179:37180
Fixed: V8: r37253:37254

Minimized Testcase (7.06 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97hiFYngfI8zG6Wn7HHcZVMSNzl-cQtxVcExSj29m327ylmQKgTX6VqLajfjtEYrFCHL4rPDMBaHtYXhLRIAfd4cVaAYbhF1kLKUMXpN5da12HM0fOBTH3X4c9IfJ3tHmz_VIQ3Ck8RieWK-JyFXjm9aOir5g?testcase_id=6204317413670912

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2016-06-25)

The older reward-topanel https://crbug.com/chromium/622659 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### sh...@chromium.org (2016-06-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-27)

The older reward-topanel https://crbug.com/chromium/622346 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### ha...@chromium.org (2016-07-05)

Is this also affecting M52?

### ve...@chromium.org (2016-07-05)

This doesn't affect anything. It was a bug in ToT for 3 days or so.

### aw...@chromium.org (2016-07-26)

Removing ReleaseBlock-Beta per #19

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-10)

Nice one - $3,500 for this.

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-11)

This issue was migrated from crbug.com/chromium/622664?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/622341, crbug.com/chromium/622346, crbug.com/chromium/622348, crbug.com/chromium/622659, crbug.com/chromium/622665, crbug.com/chromium/622666, crbug.com/chromium/622667, crbug.com/chromium/623023, crbug.com/chromium/623024, crbug.com/chromium/623184, crbug.com/chromium/623191, crbug.com/chromium/623192]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084668)*
