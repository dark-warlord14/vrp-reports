# Fatal error in ../../src/heap/mark-compact.cc, line 3665

| Field | Value |
|-------|-------|
| **Issue ID** | [350256147](https://issues.chromium.org/issues/350256147) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>GarbageCollection |
| **Platforms** | Linux |
| **Reporter** | da...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2024-07-01 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS

## INTRODUCE

After bisect, it was determined that following commit caused this problem.

- Commit Info
  - Version: 94662
  - link: <https://crrev.com/739f6d2b1f3350033c24a118b8d98ba6b8bec9a9>
- Commit Message

```
commit 739f6d2b1f3350033c24a118b8d98ba6b8bec9a9
Author: Nikolaos Papaspyrou <nikolaos@chromium.org>
Date:   Wed Jun 26 18:14:44 2024 +0200

    [heap] Parallelize trivial clearing of weakrefs
    
    Clearing weak references accounts for a large portion of GC's atomic
    pause. A large fraction of this time is spent clearing weak references
    that were recorded during marking, after we re-check that the referenced
    objects have not been marked.
    
    With this CL, weak references that are candidates for clearing are
    distinguished in two categories: trivial and non-trivial. Trivial
    weak references can be cleared in parallel, thus shortening the total
    length of the atomic pause. Non-trivial weak references (that cannot be
    cleared in parallel) are maps whose clearing involves custom weakness
    logic.
    
    Bug: 348181803
    Change-Id: I72f338b48dc9691f77d2adeb7658dc6ab2989e71
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5648710
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Nikolaos Papaspyrou <nikolaos@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94662}


```
## CRASH LOG

- Debug output

```
# CMD: /tmp/d8-linux-debug-v8-component-94724/d8 --jit-fuzzing --stress-incremental-marking poc.js
# OUTPUT ==============================================================
test/mjsunit/wasm/wasm-module-builder.js:1099: TypeError: Cannot read properties of undefined (reading 'opcode')
      this.emit_u8(type.opcode);
                        ^
TypeError: Cannot read properties of undefined (reading 'opcode')
    at Binary.emit_type (test/mjsunit/wasm/wasm-module-builder.js:1099:25)
    at test/mjsunit/wasm/wasm-module-builder.js:1852:19
    at Binary.emit_section (test/mjsunit/wasm/wasm-module-builder.js:1121:5)
    at WasmModuleBuilder.toBuffer (test/mjsunit/wasm/wasm-module-builder.js:1845:14)
    at WasmModuleBuilder.toModule (test/mjsunit/wasm/wasm-module-builder.js:2189:40)
    at WasmModuleBuilder.instantiate (test/mjsunit/wasm/wasm-module-builder.js:2178:23)
    at ./output_poc.js:17:11



#
# Fatal error in ../../src/heap/mark-compact.cc, line 3665
# Debug check failed: !InReadOnlySpace(value).
#
#
#
#FailureMessage Object: 0x7ffe9fa3c990
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-94724/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f2eea7f5113]
    /tmp/d8-linux-debug-v8-component-94724/libv8_libplatform.so(+0x190ad) [0x7f2eefe8c0ad]
    /tmp/d8-linux-debug-v8-component-94724/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f2eea7d6224]
    /tmp/d8-linux-debug-v8-component-94724/libv8_libbase.so(+0x2bc45) [0x7f2eea7d5c45]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::MarkCompactCollector::ClearNonTrivialWeakReferences()+0x4e3) [0x7f2eed5bba73]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::MarkCompactCollector::ClearNonLiveReferences()+0x18a3) [0x7f2eed5ab9f3]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::MarkCompactCollector::CollectGarbage()+0xa4) [0x7f2eed5a8354]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::Heap::MarkCompact()+0x109) [0x7f2eed5603e9]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*)+0x5e4) [0x7f2eed55f674]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(+0x2d8caee) [0x7f2eed58caee]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(+0x2d8c59f) [0x7f2eed58c59f]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(+0x43c650b) [0x7f2eeebc650b]


```
## Other

Please note to include the flags `--jit-fuzzing --stress-incremental-marking` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.8.0 - 12.8.0

REPRODUCTION CASE

1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-94724.zip
2. Run: `d8 --jit-fuzzing --stress-incremental-marking poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [mini-poc.js](attachments/mini-poc.js) (text/javascript, 718 B)
- [poc_for_clusterfuzz.js](attachments/poc_for_clusterfuzz.js) (text/javascript, 74.6 KB)
- [poc_with_ismap_dcheck.js](attachments/poc_with_ismap_dcheck.js) (text/javascript, 766 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-07-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6238542404452352.

### cl...@appspot.gserviceaccount.com (2024-07-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6248087569760256.

### ah...@google.com (2024-07-01)

[primary security shepherd]
Setting a provisional severity of High (S1)
Setting a provisional Found In of the current Extended Stable.
Assign it to the current V8 Sheriff: ishell@google.com

### ki...@gmail.com (2024-07-02)

This additional POC displays another DCHECK message, which may indicate that the current issue should be a security issue.

> Note: This POC needs to be run multiple times to trigger DCHECK.

```
$ /tmp/d8-linux-debug-v8-component-94724/d8 --jit-fuzzing --stress-incremental-marking ./output_poc.js 


#
# Fatal error in ../../src/heap/mark-compact.cc, line 3666
# Debug check failed: IsMap(value).
#
#
#
#FailureMessage Object: 0x7ffd861f3280
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-94724/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f87eda42113]
    /tmp/d8-linux-debug-v8-component-94724/libv8_libplatform.so(+0x190ad) [0x7f87ed9eb0ad]
    /tmp/d8-linux-debug-v8-component-94724/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f87eda23224]
    /tmp/d8-linux-debug-v8-component-94724/libv8_libbase.so(+0x2bc45) [0x7f87eda22c45]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::MarkCompactCollector::ClearNonTrivialWeakReferences()+0x50e) [0x7f87eafbba9e]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::MarkCompactCollector::ClearNonLiveReferences()+0x18a3) [0x7f87eafab9f3]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::MarkCompactCollector::CollectGarbage()+0xa4) [0x7f87eafa8354]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::Heap::MarkCompact()+0x109) [0x7f87eaf603e9]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GarbageCollectionReason, char const*)+0x5e4) [0x7f87eaf5f674]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(+0x2d8caee) [0x7f87eaf8caee]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(+0x2d8c59f) [0x7f87eaf8c59f]
    /tmp/d8-linux-debug-v8-component-94724/libv8.so(+0x43c650b) [0x7f87ec5c650b]
[1]    3915796 trace trap  /tmp/d8-linux-debug-v8-component-94724/d8 --jit-fuzzing  ./output_poc.js

```

### is...@chromium.org (2024-07-02)

Thank you for the report!

The `!InReadOnlySpace(value)` is a duplicate of [issue 349788229](https://issues.chromium.org/issues/349788229). Checking the `IsMap(value)` one.

### is...@chromium.org (2024-07-02)

The `value` at [this point](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/heap/mark-compact.cc;l=3666?q=%22DCHECK(!InReadOnlySpace(value));%22&ss=chromium) happened to be a `PropertyCell`.

### pe...@google.com (2024-07-02)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-07-02)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@chromium.org (2024-07-03)

This issue was reported three days after crbug/349788229, which was merged in the wrong direction as a duplicated of this report. 
Since draft fixes are already associated with this issue, I can't merge this issue into the other one at this time, so noting this here in general and for VRP consideration.
Marking this issue as a blocker for the resolution of the other report. 

### ap...@google.com (2024-07-04)

Project: v8/v8
Branch: main

commit 088eb75d704954dba497279d7ed27673fd84a2d4
Author: Nikolaos Papaspyrou <nikolaos@chromium.org>
Date:   Wed Jul 03 17:28:05 2024

    [heap] Fix DCHECK in clearing of weakrefs
    
    A number of DCHECKs introduced by https://crrev.com/c/5648710, and
    in particular the DCHECK enforcing that the value of a weak reference
    to be cleared would not be in the RO space, was wrong. It could be
    falsified in case the value of the weak reference changed between
    marking and clearing. This CL fixes the issue.
    
    Bug: 348181803
    Bug: 350256147
    Change-Id: Id4582b1992606ed5974e71731fc51dedc9b9ffe5
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5676327
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
    Commit-Queue: Nikolaos Papaspyrou <nikolaos@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94818}

M       src/heap/mark-compact.cc

https://chromium-review.googlesource.com/5676327


### ki...@gmail.com (2024-07-04)

Hi, is this report considered as duplication? Thanks!

### am...@chromium.org (2024-07-15)

re c#12 -- yes, this is considered a duplicate of [crbug.com/349788229](https://crbug.com/349788229) which was reported three days prior to this report

As such, this issue is unfortunately not eligible for a Chrome VRP reward.

### pe...@google.com (2024-08-26)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M128 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M129 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pg...@google.com (2024-08-26)

The fix for this already landed on M128 - removing merge request 128 label

### pe...@google.com (2024-10-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/350256147)*
