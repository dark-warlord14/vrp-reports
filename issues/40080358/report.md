# UNKNOWN in v8::internal::JSFunction::context

| Field | Value |
|-------|-------|
| **Issue ID** | [40080358](https://issues.chromium.org/issues/40080358) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ja...@chromium.org |
| **Created** | 2014-09-03 |
| **Bounty** | $3,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5842195568394240

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8

Crash Type: UNKNOWN
Crash Address: 0x00000020042e
Crash State:
  v8::internal::JSFunction::context
  v8::internal::Context::native_context
  v8::internal::Object::GetRootMap
  
Regressed: V8: r23571:23613

Minimized Testcase (11.31 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94U0Wyh4-m4RniV6l78VVWTZMjcmLBkT5T8fFOscsLAZuyzn-z6u3ImPBXvaRf87xxkuDEETManrdlJ-zxZ59zV04cbC9XNexHxiE0Mp0ynVP2WOPdiH5JnGIw7717cAi5ivbBfnCjlNuj0UWgvchV0vu1sFA

Filer: mbarbella

## Timeline

### in...@chromium.org (2014-09-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-03)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-09-03)

It seems like there are no unsafe runtime functions being called here, so this looks promising. I'm working on getting a repro for this now.

### cl...@chromium.org (2014-09-03)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6695940778885120

### cl...@chromium.org (2014-09-04)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6695940778885120

Uploader: mbarbella@google.com
Job Type: Linux_asan_chrome_v8

Crash Type: UNKNOWN
Crash Address: 0x00000020042e
Crash State:
  v8::internal::JSFunction::context
  v8::internal::Context::native_context
  v8::internal::Object::GetRootMap
  
Regressed: V8: r23571:23613

Minimized Testcase (2.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv964Nh1nheic8r9ZTM23Zd_0OHC4k8moLUQCuE57de0MfZHETwSzwD6IZ0swsIedKY69Jdrbz7B2ib97ur4Ldm46ERE6O-d-FknY5JQ05vU7mYblVrxOuNuckyY7E_AyDWvDYGaQNfpWzJwPOLlHGgn3Wu0_hw



### cl...@chromium.org (2014-09-04)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ja...@chromium.org (2014-09-04)

Fixed in V8 bleeding edge r23699.

### cl...@chromium.org (2014-09-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-05)

ClusterFuzz has detected this issue as fixed in range 23682:23706.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5842195568394240

Fuzzer: Decoder_langfuzz
Job Type: Linux_asan_d8

Crash Type: UNKNOWN
Crash Address: 0x00000020042e
Crash State:
  v8::internal::JSFunction::context
  v8::internal::Context::native_context
  v8::internal::Object::GetRootMap
  
Regressed: V8: r23571:23613
Fixed: V8: r23682:23706

Minimized Testcase (11.31 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94U0Wyh4-m4RniV6l78VVWTZMjcmLBkT5T8fFOscsLAZuyzn-z6u3ImPBXvaRf87xxkuDEETManrdlJ-zxZ59zV04cbC9XNexHxiE0Mp0ynVP2WOPdiH5JnGIw7717cAi5ivbBfnCjlNuj0UWgvchV0vu1sFA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-09-06)

ClusterFuzz has detected this issue as fixed in range 23682:23706.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6695940778885120

Uploader: mbarbella@google.com
Job Type: Linux_asan_chrome_v8

Crash Type: UNKNOWN
Crash Address: 0x00000020042e
Crash State:
  v8::internal::JSFunction::context
  v8::internal::Context::native_context
  v8::internal::Object::GetRootMap
  
Regressed: V8: r23571:23613
Fixed: V8: r23682:23706

Minimized Testcase (2.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv964Nh1nheic8r9ZTM23Zd_0OHC4k8moLUQCuE57de0MfZHETwSzwD6IZ0swsIedKY69Jdrbz7B2ib97ur4Ldm46ERE6O-d-FknY5JQ05vU7mYblVrxOuNuckyY7E_AyDWvDYGaQNfpWzJwPOLlHGgn3Wu0_hw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### mb...@chromium.org (2014-11-17)

Thanks again for the fuzzer contribution! This one qualified for a $3000 reward.

### ti...@google.com (2014-12-09)

Reward payment in process

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-11)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/410556?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080358)*
