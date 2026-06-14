# Debug check failed: mutable_double_address_ == reinterpret_cast<Address>(raw_bytes_->end()) (23179938834648 vs. 23179938834660)

| Field | Value |
|-------|-------|
| **Issue ID** | [324342761](https://issues.chromium.org/issues/324342761) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux, Mac |
| **Reporter** | wh...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2024-02-08 |
| **Bounty** | $8,000.00 |

## Description

Security Bug

This template is ONLY for reporting security bugs. If you are reporting a Download Protection Bypass bug, please use the ""Security -Download Protection"" template. For all other reports, please use a different template.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: http://g.co/ChromeBugRewards

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

# Fatal error in ../../src/json/json-parser.cc, line 1030
# Debug check failed: mutable_double_address_ == reinterpret_cast<Address>(raw_bytes_->end()) (29807073380136 vs. 29807073380148).
#
#FailureMessage Object: 0x7ffdab9f6340
==== C stack trace ===============================

    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f61761b8a83]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8_libplatform.so(+0x18e5d) [0x7f6176161e5d]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x17e) [0x7f6176199c4e]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8_libbase.so(+0x2b695) [0x7f6176199695]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8.so(v8::internal::FoldedMutableHeapNumberAllocator::~FoldedMutableHeapNumberAllocator()+0x1ee) [0x7f6178e224de]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8.so(v8::internal::JsonParser<unsigned char>::BuildJsonObject(v8::internal::JsonParser<unsigned char>::JsonContinuation const&, v8::base::SmallVector<v8::internal::JsonProperty, 16ul, std::__Cr::allocator<v8::internal::JsonProperty>> const&, v8::internal::Handle<v8::internal::Map>)+0xe0d) [0x7f6178e2028d]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8.so(v8::internal::MaybeHandle<v8::internal::Object> v8::internal::JsonParser<unsigned char>::ParseJsonValue<false>(v8::internal::Handle<v8::internal::Object>)+0xb65) [0x7f6178e1bac5]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8.so(v8::internal::JsonParser<unsigned char>::ParseJson(v8::internal::Handle<v8::internal::Object>)+0x96) [0x7f6178e18266]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8.so(v8::internal::JsonParser<unsigned char>::Parse(v8::internal::Isolate*, v8::internal::Handle<v8::internal::String>, v8::internal::Handle<v8::internal::Object>)+0x79) [0x7f6178e17fa9]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8.so(+0x2526277) [0x7f61786ea277]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8.so(v8::internal::Builtin_JsonParse(int, unsigned long*, v8::internal::Isolate*)+0x7f) [0x7f61786e9d0f]
    /mnt/asan/d8_debug_zip/d8-linux-debug-v8-component-91999/libv8.so(+0x1b9d5bd) [0x7f6177d615bd]

### Bisect 
[maglev] Extend CSE

Also let non-value Nodes participate in CSE and allow merging of
instructions with equivalent but not identical immediate arguments.

Drive-By: To enable the latter a refactoring to use full equality checks
          over immediate arguments.

Bug: v8:7700
Change-Id: I5eeba26e6b7fd176574ba8523a4ab2c009339a2b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5215746
Commit-Queue: Olivier Flückiger <olivf@chromium.org>
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Auto-Submit: Olivier Flückiger <olivf@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91995}

VERSION
Chrome Version: [x.x.x.x] + [stable, beta, or dev]
Operating System: [Please indicate OS, version, and service pack level]

REPRODUCTION CASE
run d8 --expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing 

I'll upload poc later.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Timeline

### wh...@gmail.com (2024-02-08)

PoC

function f6(a7, a8) {
    const v10 = "randomKey" + a8;
    const o11 = {
        "foo": a8,
        [v10]: 'A',
    };
    return o11;
}
const v14 = Array(1600);
const v16 = v14.fill().map(f6);
v16[0]['foo'] = 4294967297;
JSON.parse(JSON.stringify(v16));


### wh...@gmail.com (2024-02-08)

Oh, sorry for Comment1 Bisect is wrong. 

here is right Bisect. 

[object] Add fast path map creation

Allow the JSDataObjectBuilder to create maps, rather than bailing out if
a transition isn't found, to stay on the fast path (with fast object
initialisation) a bit more often.

Change-Id: I7e6845232e485532755e37f3df6912a165615a81
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5228677
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91998}

### wh...@gmail.com (2024-02-08)

active channel: dev/123

### da...@chromium.org (2024-02-08)

Provisionally setting S1/High and FoundIn 120, these may need to be updated after triage.

### cl...@appspot.gserviceaccount.com (2024-02-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5159945839771648.

### 24...@project.gserviceaccount.com (2024-02-08)

Detailed Report: https://clusterfuzz.com/testcase?key=5159945839771648

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  mutable_double_address_ == reinterpret_cast<Address>(raw_bytes_->end()) in json-
  v8::internal::FoldedMutableHeapNumberAllocator::~FoldedMutableHeapNumberAllocato
  v8::internal::Handle<v8::internal::JSObject> v8::internal::JSDataObjectBuilder::
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91997:91998

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5159945839771648

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pg...@google.com (2024-02-09)

Removing provisional FoundIn set as clusterfuzz bisected the source to be in M123

### cf...@google.com (2024-02-09)

Leszek, as this bisects to [[object] Add fast path map creation](https://chromium.googlesource.com/v8/v8/+/549cc2e1a5fb385fb514c79568abc57ecc82578e), could you PTAL?

### wh...@gmail.com (2024-02-09)

### details

`RegisterFieldNeedsFreshHeapNumber` expect to allocate HeapNumbers for double representation, but descriptor's representation is changed from kDouble to kTagged.

```
    // Initialize the in-object properties up to the last added property.
    int current_property_offset = raw_object->GetInObjectPropertyOffset(0);
    for (int i = 0; i < current_property_index_; ++i, ++value_it) {
      InternalIndex descriptor_index(i);
      Tagged<Object> value = **value_it;

      // See comment in RegisterFieldNeedsFreshHeapNumber, we need to allocate
      // HeapNumbers for double representation fields when we can't make
      // existing HeapNumbers mutable, or when we only have a Smi value.
      if (heap_number_mode_ != kHeapNumbersGuaranteedUniquelyOwned ||
          IsSmi(value)) {
        PropertyDetails details = descriptors->GetDetails(descriptor_index);
        if (details.representation().IsDouble()) {
          value = hn_allocator.AllocateNext(
              roots, Float64(static_cast<double>(Smi::cast(value).value())));
        }
      }

```

[1]<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/json/json-parser.cc;l=882?q=json-parser.cc>

### pe...@google.com (2024-02-09)

Setting milestone because of s0/s1 severity.

### 24...@project.gserviceaccount.com (2024-02-10)

ClusterFuzz testcase 5159945839771648 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=92253:92254

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### am...@google.com (2024-02-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-02-14)

Congratulations Ganjiang Zhou! The Chrome VRP Panel has decided to award you $7,000 for this report of a renderer / sandboxed process memory corruption bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-02-21)

This is sufficiently serious that it should be merged to dev. But I can't  see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M123. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [123].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### am...@chromium.org (2024-02-21)

fix (<https://crrev.com/c/5279593>) landed on M123, no merge necessary

### pe...@google.com (2024-05-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/324342761)*
