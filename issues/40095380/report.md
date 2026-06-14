# Use-after-free in WasmMemoryObject::Grow

| Field | Value |
|-------|-------|
| **Issue ID** | [40095380](https://issues.chromium.org/issues/40095380) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Linux |
| **Reporter** | jt...@gmail.com |
| **Assignee** | gd...@chromium.org |
| **Created** | 2019-06-12 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36

Steps to reproduce the problem:
1. Download the poc.html
2. Run chrome --js-flags="--wasm-grow-shared-memory" poc.html

What is the expected behavior?
Not crash.

What went wrong?
WasmMemoryTracker uses isolates_per_buffer_ to map each buffer to the isolates that share the backing store.

When using postMessage to share a WasmMemoryObject, it will call RegisterWasmMemoryAsShared, which insert current isolate to |isolates_per_buffer_[backing_store]|.

From https://cs.chromium.org/chromium/src/v8/src/wasm/wasm-memory.cc?l=281&rcl=0460fcded75a3fecb8375d55feeaf8d0d402c5cb
```
void WasmMemoryTracker::RegisterWasmMemoryAsShared(
    Handle<WasmMemoryObject> object, Isolate* isolate) {
  [...]
  if (!IsWasmMemory(backing_store)) return;
  {
    base::MutexGuard scope_lock(&mutex_);
    // Register as shared allocation when it is post messaged. This happens only
    // the first time a buffer is shared over Postmessage, and track all the
    // memory objects that are associated with this backing store.
    RegisterSharedWasmMemory_Locked(object, isolate);
    // Add isolate to backing store mapping.
    isolates_per_buffer_[backing_store].emplace(isolate);
  }
}
```

RegisterWasmMemoryAsShared will be called both serialize and deserialize. However, we can interrupt serialization by throwing an exception after the WasmMemoryObject getting serialized, and |isolates_per_buffer_[backing_store]| will only contain one isolate.

After calling WasmMemoryObject::Grow, gc should decide whether the backing store will be freed or not.

From https://cs.chromium.org/chromium/src/v8/src/wasm/wasm-memory.cc?l=455&rcl=0c53fce086cb01d4070013c3139f846d2477b3cc
```
void WasmMemoryTracker::FreeMemoryIfNotShared_Locked(
    Isolate* isolate, const void* backing_store) {
  RemoveSharedBufferState_Locked(isolate, backing_store); // ** 1 **
  if (CanFreeSharedMemory_Locked(backing_store)) {
    const AllocationData allocation =
        ReleaseAllocation_Locked(isolate, backing_store);
    CHECK(FreePages(GetPlatformPageAllocator(), allocation.allocation_base,
                    allocation.allocation_length));
  }
}

bool WasmMemoryTracker::CanFreeSharedMemory_Locked(const void* backing_store) {
  const auto& value = isolates_per_buffer_.find(backing_store);  
  // If no isolates share this buffer, backing store can be freed.
  // Erase the buffer entry.
  if (value == isolates_per_buffer_.end() || value->second.empty() /* ** 2 ** */) return true;  
  return false;
}
```
[1] will remove |isolate| in unordered_set isolates_per_buffer_[backing_store], because there are only one isolate in the set before [1], [2] will be true and backing store will be freed.

We still keep a reference to the freed memory region and UAF occured.

Note:
This looks very similar to https://bugs.chromium.org/p/project-zero/issues/detail?id=1819, but with different code path. In this case, SharedArrayBuffer in WasmMemoryObject gets externalized and Blink's GC takes responsible for managing the memory.

Did this work before? N/A 

Chrome version: 75.0.3770.80  Channel: stable
OS Version: 
Flash Version:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)

## Timeline

### cl...@chromium.org (2019-06-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6283043546988544.

### me...@chromium.org (2019-06-13)

mstarzinger: Can you PTAL?

[Monorail components: Blink>JavaScript>WebAssembly]

### me...@chromium.org (2019-06-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-06-14)

Detailed report: https://clusterfuzz.com/testcase?key=6283043546988544

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7eec24b80000
Crash State:
  Builtins_DataViewPrototypeSetUint8
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=638468:638469

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6283043546988544

Additional requirements: Requires HTTP

See https://github.com/google/clusterfuzz-tools for instructions to reproduce this bug locally.

### me...@chromium.org (2019-06-14)

The regression range above contains this CL: https://chromium.googlesource.com/v8/v8/+/365b637cc0fb57fd25008b5f3b0aac90b934b6e2

gdeepti: Assigning to you, PTAL?

### sh...@chromium.org (2019-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-14)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-26)

gdeepti: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-10)

gdeepti: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-07-23)

ClusterFuzz testcase 6283043546988544 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=679558:679561

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-07-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-24)

Requesting merge to beta M76 even though there is no obvious Chromium repository trunk commit here. Perhaps it was fixed in another ticket; please investigate.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-07-24)

This bug requires manual review: We are only 5 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2019-07-24)

No clear CL, and we're less than a week away from stable. 

### na...@google.com (2019-07-24)

[Empty comment from Monorail migration]

### gd...@chromium.org (2019-07-24)

There's an ongoing effort to refactor ArrayBuffer backing stores that was landed in the V8 range rolled into Chromium, but was reverted soon after. (https://chromium.googlesource.com/v8/v8/+log/5578fd9f5f5f37c133bfb93871f21e294c99e198..6459bca2413ebac5c1d8b11b52ea4fb504d6dba0?pretty=fuller&n=10000

So clusterfuzz detected this as fixed for now, but will mark this as not fixed as the next version of V8 rolls in. 

It is correct that there is nothing to merge here, as this was behind a flag and never on by default. Re-opening this bug, and adding the tracking bug for the backing store refactor as a dependency. 

### gd...@chromium.org (2019-07-24)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-24)

Setting Security_Impact-None per https://crbug.com/chromium/973360#c16 - gdeepti@ please correct me if I'm wrong.

### gd...@chromium.org (2019-07-24)

Thanks for updating, verifying that the labels are correct. 

### sh...@chromium.org (2019-07-25)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-08-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-08-01)

Congrats! The Panel decided to reward you $5,000 for this report! 

### na...@google.com (2019-08-01)

[Empty comment from Monorail migration]

### pa...@chromium.org (2019-08-01)

jtrrodant@gmail.com - please let me know how you would like to be credited in our release notes. 

### jt...@gmail.com (2019-08-02)

Thank You :)
Credit info: Rong Jian and Guang Gong of Alpha Team, Qihoo 360.
Will this receive a CVE id?

### jt...@gmail.com (2019-09-11)

[Comment Deleted]

### sh...@chromium.org (2019-11-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-01)

This issue was migrated from crbug.com/chromium/973360?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/v8/9380]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095380)*
