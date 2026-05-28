# Security: Debug check failed: enum_length == map->NumberOfEnumerableProperties()

| Field | Value |
|-------|-------|
| **Issue ID** | [40061952](https://issues.chromium.org/issues/40061952) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ki...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-11-29 |
| **Bounty** | $11,000.00 |

## Description

**VULNERABILITY DETAILS**

## CRASH LOG

- Debug output

```
#  
# Fatal error in ../../src/objects/keys.cc, line 500  
# Debug check failed: enum_length == map->NumberOfEnumerableProperties() (1 vs. 0).  
#  
#  
#  
#FailureMessage Object: 0x7ffebc769630  
==== C stack trace ===============================  
  
    /usr/class/v8/v8/out/fuzzbuild/d8(+0x6adfd2) [0x556cc7cd1fd2]  
    /usr/class/v8/v8/out/fuzzbuild/d8(+0x6acc57) [0x556cc7cd0c57]  
    /usr/class/v8/v8/out/fuzzbuild/d8(+0x69eafb) [0x556cc7cc2afb]  
    /usr/class/v8/v8/out/fuzzbuild/d8(+0x69e485) [0x556cc7cc2485]  
    /usr/class/v8/v8/out/fuzzbuild/d8(+0x149cf97) [0x556cc8ac0f97]  
    /usr/class/v8/v8/out/fuzzbuild/d8(+0x82b8b6) [0x556cc7e4f8b6]  
    /usr/class/v8/v8/out/fuzzbuild/d8(+0x8299c8) [0x556cc7e4d9c8]  
    [0x556c5feb00b8]  
[2]    3925465 trace trap  /usr/class/v8/v8/out/fuzzbuild/d8 --harmony-struct  

```

**VERSION**  

Tested on v8 version 11.0.0

**REPRODUCTION CASE**

1. Download debug v8 from: <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-84519.zip?generation=1669651182751742&alt=media>
2. Run: ./d8 --harmony-struct poc.js

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

**CREDIT INFORMATION**  

Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 33 B)

## Timeline

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### ki...@gmail.com (2022-11-29)

INTRODUCE

After bisect, it was determined that commit 0dcbdfa0168d061890f8c559f798d7722305653e caused this problem.

- 84046 will not trigger crash
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-84046.zip?generation=1667491214780018&alt=media
- And 84047 will cause crash
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-84047.zip?generation=1667493817644033&alt=media

commit 0dcbdfa0168d061890f8c559f798d7722305653e
Author: Shu-yu Guo <syg@chromium.org>
Date:   Thu Nov 3 08:48:39 2022 -0700

    [shared-struct] Fix for-in enumeration
    
    for-in enumeration creates an EnumCache, which is currently incorrectly
    allocated in the per-thread heap. This CL preallocates the enum cache at
    SharedStructType-creation time.
    
    Also drive-by fixes typos in the enum cache code.
    
    Bug: v8:12547, chromium:1379616
    Change-Id: I1930f88844eca5ccfeebd8dfdcce4ad0bd80ee38
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3997701
    Commit-Queue: Shu-yu Guo <syg@chromium.org>
    Reviewed-by: Camillo Bruni <cbruni@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#84047}

### ki...@gmail.com (2022-11-29)

CRASH ANALYSIS

1. It can be seen from the poc that the num_properties of the constructed SharedStructType is 1.

2. v8 then calls InitializeFastPropertyEnumCache to compute the `for....in...` cache, but it directly passes num_properties as enum_length.

3. Since Symbol is a non-enumerable property, the value calculated by NumberOfEnumerableProperties is 0, resulting in inconsistency between enum_length and map->NumberOfEnumerableProperties(), thus triggering DCHECK.

4. This will eventually lead to inconsistency in enum length and enum cache, and this inconsistency may be a potential problem for JIT optimization. I'm not sure if this is possible to exploit the v8 via JIT optimization or other exploit methods, and I submit it anyway.

### cl...@chromium.org (2022-11-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5089526335864832.

### cl...@chromium.org (2022-11-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-30)

Detailed Report: https://clusterfuzz.com/testcase?key=5089526335864832

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  enum_length == map->NumberOfEnumerableProperties() in keys.cc
  v8::internal::FastKeyAccumulator::InitializeFastPropertyEnumCache
  v8::internal::Builtin_Impl_SharedStructTypeConstructor
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84046:84047

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5089526335864832

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-11-30)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2022-11-30)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/0dcbdfa0168d061890f8c559f798d7722305653e ([shared-struct] Fix for-in enumeration).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### ki...@gmail.com (2022-11-30)

[Comment Deleted]

### ki...@gmail.com (2022-11-30)

sorry, https://crbug.com/chromium/1394408#c3 code here
```
BUILTIN(SharedStructTypeConstructor) {
  ...
  // Treat field_names_arg as arraylike.
  Handle<Object> raw_length_number;
  ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
      isolate, raw_length_number,
      Object::GetLengthFromArrayLike(isolate, field_names_arg));
  double num_properties_double = raw_length_number->Number();
  if (num_properties_double < 0 || num_properties_double > kMaxJSStructFields) {
    THROW_NEW_ERROR_RETURN_FAILURE(
        isolate, NewRangeError(MessageTemplate::kStructFieldCountOutOfRange));
  }
  int num_properties = static_cast<int>(num_properties_double); // <----------------------- 1 
  ...
  // Pre-create the enum cache in the shared space, as otherwise for-in
  // enumeration will incorrectly create an enum cache in the per-thread heap.
  if (num_properties == 0) {
    instance_map->SetEnumLength(0);
  } else {
    instance_map->InitializeDescriptors(isolate, *maybe_descriptors);
    FastKeyAccumulator::InitializeFastPropertyEnumCache(
        isolate, instance_map, num_properties, AllocationType::kSharedOld);  // <----------------------- 2
    DCHECK_EQ(num_properties, instance_map->EnumLength());
  }

  return *constructor;
}


// static
Handle<FixedArray> FastKeyAccumulator::InitializeFastPropertyEnumCache(
    Isolate* isolate, Handle<Map> map, int enum_length,
    AllocationType allocation) {
  ...
  DCHECK_EQ(enum_length, map->NumberOfEnumerableProperties()); // <----------------------- 3


int Map::NumberOfEnumerableProperties() const {
  int result = 0;
  DescriptorArray descs = instance_descriptors(kRelaxedLoad);
  for (InternalIndex i : IterateOwnDescriptors()) {
    if ((int{descs.GetDetails(i).attributes()} & ONLY_ENUMERABLE) == 0 && // <----------------------- 3
        !descs.GetKey(i).FilterKey(ENUMERABLE_STRINGS)) {
      result++;
    }
  }
  return result;
}
```

### ca...@chromium.org (2022-11-30)

Setting severity high to match other similar bugs

### [Deleted User] (2022-12-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-01)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-12-01)

This is Security_Impact-None as it depends on the experimental flag --harmony-struct, which is off by default. And so it is also not a release blocker. Removing those labels.

### ki...@gmail.com (2022-12-06)

Hello, is there still active?  Thanks!

### sy...@chromium.org (2022-12-06)

Yes, this is still on my plate and will fix this week. Last week I had a conflict and did not have time to work on this.

### ad...@google.com (2022-12-06)

[Empty comment from Monorail migration]

### ki...@gmail.com (2022-12-12)

Hi, If you are free, can you take a look at this issue?
https://bugs.chromium.org/p/chromium/issues/detail?id=1400051
It was introduced by this commit you submitted
https://chromium.googlesource.com/v8/v8/+/31e17fe62d59968f6f89f5c33eaf8fa75d375b77

It needs to call d8's quit() function to trigger, so it is marked as won't fix by clusterfuzz, but this is obviously not the expected situation, which will cause a SEGV_ACCERR on release

Thanks!

### gi...@appspot.gserviceaccount.com (2022-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/d1d100d4ef4aa4299f0b7cef921bf69daaac08c4

commit d1d100d4ef4aa4299f0b7cef921bf69daaac08c4
Author: Shu-yu Guo <syg@chromium.org>
Date: Sat Dec 10 00:07:00 2022

[shared-struct] Disallow Symbol field names

Bug: chromium:1394408, v8:12547
Change-Id: If98e6f0e7048a7d218010eb2859bb986a20917ba
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4094374
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Auto-Submit: Shu-yu Guo <syg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84779}

[modify] https://crrev.com/d1d100d4ef4aa4299f0b7cef921bf69daaac08c4/test/mjsunit/shared-memory/shared-struct-surface.js
[modify] https://crrev.com/d1d100d4ef4aa4299f0b7cef921bf69daaac08c4/src/builtins/builtins-struct.cc


### cl...@chromium.org (2022-12-12)

ClusterFuzz testcase 5089526335864832 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=84778:84779

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-12)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-12-15)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Congratulations, Zhenghang! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1394408?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1384471, crbug.com/chromium/1396184]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061952)*
