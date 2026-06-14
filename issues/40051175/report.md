# CHECK failure: *old_buffer != memory_object->array_buffer() in wasm-objects.cc

| Field | Value |
|-------|-------|
| **Issue ID** | [40051175](https://issues.chromium.org/issues/40051175) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2017-15399 |
| **Reporter** | da...@davidmanouchehri.com |
| **Assignee** | gd...@chromium.org |
| **Created** | 2020-01-09 |
| **Bounty** | $2,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5945746400542720

Fuzzer: ochang_js_fuzzer
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  *old_buffer != memory_object->array_buffer() in wasm-objects.cc
  v8::internal::WasmMemoryObject::Grow
  v8::WebAssemblyMemoryGrow
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=65645:65646

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5945746400542720

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5945746400542720 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### cl...@chromium.org (2020-01-09)

First error after staging atomics (growing shared memory).
Deepti, can you take a look?

[Monorail components: -Blink>JavaScript Blink>JavaScript>WebAssembly]

### sh...@chromium.org (2020-01-09)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8d511cbd209e90448f3f9197b2ac49757cd32ca5

commit 8d511cbd209e90448f3f9197b2ac49757cd32ca5
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Tue Jan 14 01:35:06 2020

[wasm] Growing memory should always allocate a new JS buffer

The UpdateSharedWasmMemoryObjects function only creates a new
JSArrayBuffer when the the legths of old/new ArrayBuffer objects
are unequal, but the CHECK in the Grow() funciton assumes that a new
object is always created. Fix so that a new ArrayBuffer is always
allocated.

Bug: v8:10044, chromium:1040325
Change-Id: I66912bdc091e65a57e5b50f4ed63b0da5492dcc4
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1999603
Reviewed-by: Ben Smith <binji@chromium.org>
Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65742}

[modify] https://crrev.com/8d511cbd209e90448f3f9197b2ac49757cd32ca5/src/objects/backing-store.cc
[modify] https://crrev.com/8d511cbd209e90448f3f9197b2ac49757cd32ca5/test/mjsunit/wasm/grow-shared-memory.js


### cl...@chromium.org (2020-01-14)

ClusterFuzz testcase 5945746400542720 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=65741:65742

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2020-01-15)

[Empty comment from Monorail migration]

### el...@chromium.org (2020-01-22)

curious: Is this related to https://crbug.com/chromium/1010272? especially c35 on that bug

### gd...@chromium.org (2020-01-22)

Hi, yes it is - previously all the cases for growing by 0 were handled together so this behaved the same way for both shared/unshared memory. After a refactoring change, the shared memory case was split out, but we didn't test for grow(0), and shared memory separately. We now have a unit test for this specific case, and better fuzzer coverage so we catch cases like this earlier. 

### ad...@chromium.org (2020-02-13)

Adding David Manouchehri who provided the test case in https://bugs.chromium.org/p/chromium/issues/detail?id=1010272#c35, as they've asked about this bug.

### ad...@chromium.org (2020-02-13)

VRP panel, please see https://crbug.com/chromium/1040325#c7 and https://crbug.com/chromium/1040325#c8 which suggests that https://bugs.chromium.org/p/chromium/issues/detail?id=1010272#c35 was helpful in discovering this.

### da...@davidmanouchehri.com (2020-02-13)

Thanks for adding me to the ticket, cool to see that ClusterFuzz caught it. I was convinced this ticket was owned by glazunov. =P 

I found this bug through variant analysis of https://bugs.chromium.org/p/chromium/issues/detail?id=776677 / CVE-2017-15399 if anyone is curious.

Exploitation of this one is more difficult than CVE-2017-15399 as you'd need to win the race between BroadcastSharedWasmMemoryGrow and the CHECK_NE. 

int32_t WasmMemoryObject::Grow(Isolate* isolate,
                               Handle<WasmMemoryObject> memory_object,
                               uint32_t pages) {
...
  // Try to handle shared memory first.
  if (old_buffer->is_shared()) {
    if (FLAG_wasm_grow_shared_memory) {
      // Shared memories can only be grown in place; no copying.
      if (backing_store->GrowWasmMemoryInPlace(isolate, pages, maximum_pages)) {
        BackingStore::BroadcastSharedWasmMemoryGrow(isolate, backing_store,
                                                    new_pages);
        // <----------------------------------- Must win a race before this line
        CHECK_NE(*old_buffer, memory_object->array_buffer());
...
      }
    }
    return -1;
  }
...
}

I didn't submit a report as I wasn't able to provide a PoC that could reliably win such a race. In hindsight I should have committed my test case and sent it off to Gerrit, which would have helped spot and fix this much soon. Lesson learned!

### na...@google.com (2020-02-20)

Unfortunately the Panel declined to reward this report as it was found by another fuzzer. 

### da...@davidmanouchehri.com (2020-02-20)

No worries. To clarify/confirm, when was it found by another fuzzer? My test case was provided on Nov 11, 2019, which was much earlier than ochang_js_fuzzer (Jan 8, 2020 according to this ticket).

### ad...@chromium.org (2020-02-25)

Allocating CVE because the first mention of this was external in https://bugs.chromium.org/p/chromium/issues/detail?id=1010272#c35, AIUI.

### ad...@google.com (2020-02-26)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-27)

Congrats! The Panel re-visited this report and decided to award $2,000! Nice one! 

### da...@davidmanouchehri.com (2020-02-27)

Thanks, that was quite a genuine gesture; you folks are all awesome!

I promise this will be my last and only poorly reported security bug. =P 

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-06-01)

Hmmm. I'm trying to work out if I should have allocated a CVE here (I'll need to submit details to MITRE, but I can only allocate one if it affected a shipping product i.e. stable).

As far as I can tell, here's the timeline.
1. this bug was introduced prior to November but was only triggered using the  --experimental-wasm-threads flag
2. that flag was sometimes enabled on desktop Chrome (according to https://chromium.googlesource.com/v8/v8/+log/7d420621887c9ceaef827db99ef2e627bc023d22..6e2e31e5fb21085e4f041d952e023b308a61e90a?pretty=fuller&n=10000, both the commit comment and code comments)
3. that commit (which is the regression range for this bug) enabled the flag by default, which is what caused the fuzzer to find it
4. the fix was 8d511cbd209e90448f3f9197b2ac49757cd32ca5 which went into M81 initial release.

As such I believe that Security_Impact-Head is effectively wrong, and this did impact some production stable configurations. Therefore it does deserve a CVE, as well as a mention in the M81 release notes, which I will edit in due course. Adjusting labels to that effect.

### ad...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1040325?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051175)*
