# Security: race condition lead to many fatal Error D in WebAssembly.validate

| Field | Value |
|-------|-------|
| **Issue ID** | [40089891](https://issues.chromium.org/issues/40089891) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2017-12-12 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**  

<https://bugs.chromium.org/p/chromium/issues/detail?id=759624>

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

## Attachments

- [worker.js](attachments/worker.js) (text/plain, 796 B)
- [stack.wasm](attachments/stack.wasm) (application/octet-stream, 335 B)

## Timeline

### hi...@gmail.com (2017-12-12)

Security: race condition lead to many fatal Errors in WebAssembly.validate

VULNERABILITY DETAILS
this is a similar issue as https://bugs.chromium.org/p/chromium/issues/detail?id=759624, https://crbug.com/chromium/759624 fixed WebAssembly.Module but missed WebAssembly.validate

VERSION
Chrome Version: [63.0.3239.84] + [stable]
Operating System: [all]

REPRODUCTION CASE
a poc is attached, just run "./d8 ./worker.js" to reproduce the crash. The d8 should be a debug version.

here is some crashes
crash 1:
#
# Fatal error in ../../v8/src/wasm/function-body-decoder-impl.h, line 290
# Debug check failed: kExprBrTable == decoder->read_u8<validate>(pc, "opcode") (14 vs. '54').
#

==== C stack trace ===============================

    /path/chromium/src/out/Debug/./libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fa83255b693]
    /path/chromium/src/out/Debug/./libv8_libplatform.so(+0xdc1b) [0x7fa832536c1b]
    /path/chromium/src/out/Debug/./libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xdc) [0x7fa832554c6c]
    /path/chromium/src/out/Debug/./libv8_libbase.so(+0x14a45) [0x7fa832554a45]
    /path/chromium/src/out/Debug/./libv8.so(+0xc94786) [0x7fa831f52786]
    /path/chromium/src/out/Debug/./libv8.so(+0xc9f7c0) [0x7fa831f5d7c0]
    /path/chromium/src/out/Debug/./libv8.so(+0xc99cca) [0x7fa831f57cca]
    /path/chromium/src/out/Debug/./libv8.so(v8::internal::wasm::VerifyWasmCode(v8::internal::AccountingAllocator*, v8::internal::wasm::WasmModule const*, v8::internal::wasm::FunctionBody&)+0x109) [0x7fa831f579d9]
    /path/chromium/src/out/Debug/./libv8.so(+0xc9a020) [0x7fa831f58020]
    /path/chromium/src/out/Debug/./libv8.so(+0xcdb4c9) [0x7fa831f994c9]
    /path/chromium/src/out/Debug/./libv8.so(+0xcd7370) [0x7fa831f95370]
    /path/chromium/src/out/Debug/./libv8.so(+0xcd2184) [0x7fa831f90184]
    /path/chromium/src/out/Debug/./libv8.so(+0xcd1714) [0x7fa831f8f714]
    /path/chromium/src/out/Debug/./libv8.so(+0xcd1338) [0x7fa831f8f338]
    /path/chromium/src/out/Debug/./libv8.so(v8::internal::wasm::SyncDecodeWasmModule(v8::internal::Isolate*, unsigned char const*, unsigned char const*, bool, v8::internal::wasm::ModuleOrigin)+0x47) [0x7fa831f906e7]
    /path/chromium/src/out/Debug/./libv8.so(v8::internal::wasm::SyncValidate(v8::internal::Isolate*, v8::internal::wasm::ModuleWireBytes const&)+0x4f) [0x7fa831f7520f]
    /path/chromium/src/out/Debug/./libv8.so(+0xd09034) [0x7fa831fc7034]
    /path/chromium/src/out/Debug/./libv8.so(+0x33d282) [0x7fa8315fb282]
    /path/chromium/src/out/Debug/./libv8.so(+0x43a115) [0x7fa8316f8115]
    /path/chromium/src/out/Debug/./libv8.so(+0x438209) [0x7fa8316f6209]
    /path/chromium/src/out/Debug/./libv8.so(+0x437c4d) [0x7fa8316f5c4d]
    [0x223aa4004384]
Received signal 4 ILL_ILLOPN 7fa832559ab2
Illegal instruction


crash 2:
#
# Fatal error in ../../v8/src/wasm/module-decoder.cc, line 650
# Debug check failed: !cmp_less(*it, *last).
#

==== C stack trace ===============================

    /path/chromium/src/out/Debug/./libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fa6038b4693]
    /path/chromium/src/out/Debug/./libv8_libplatform.so(+0xdc1b) [0x7fa60388fc1b]
    /path/chromium/src/out/Debug/./libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0xdc) [0x7fa6038adc6c]
    /path/chromium/src/out/Debug/./libv8_libbase.so(+0x14a45) [0x7fa6038ada45]
    /path/chromium/src/out/Debug/./libv8.so(+0xcd6dd1) [0x7fa6032eddd1]
    /path/chromium/src/out/Debug/./libv8.so(+0xcd212b) [0x7fa6032e912b]
    /path/chromium/src/out/Debug/./libv8.so(+0xcd1714) [0x7fa6032e8714]
    /path/chromium/src/out/Debug/./libv8.so(+0xcd1338) [0x7fa6032e8338]
    /path/chromium/src/out/Debug/./libv8.so(v8::internal::wasm::SyncDecodeWasmModule(v8::internal::Isolate*, unsigned char const*, unsigned char const*, bool, v8::internal::wasm::ModuleOrigin)+0x47) [0x7fa6032e96e7]
    /path/chromium/src/out/Debug/./libv8.so(v8::internal::wasm::SyncValidate(v8::internal::Isolate*, v8::internal::wasm::ModuleWireBytes const&)+0x4f) [0x7fa6032ce20f]
    /path/chromium/src/out/Debug/./libv8.so(+0xd09034) [0x7fa603320034]
    /path/chromium/src/out/Debug/./libv8.so(+0x33d282) [0x7fa602954282]
    /path/chromium/src/out/Debug/./libv8.so(+0x43a115) [0x7fa602a51115]
    /path/chromium/src/out/Debug/./libv8.so(+0x438209) [0x7fa602a4f209]
    /path/chromium/src/out/Debug/./libv8.so(+0x437c4d) [0x7fa602a4ec4d]
    [0x37c2b5d84384]
Received signal 4 ILL_ILLOPN 7fa6038b2ab2
Illegal instruction

### el...@chromium.org (2017-12-12)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>WebAssembly]

### ha...@chromium.org (2017-12-12)

DCHECKS don't sound that severe. Waiting for security sheriffs to upload it to CF.

### ti...@chromium.org (2017-12-12)

Looks like we are missing a memcpy of the bytes out of the buffer for the SyncValidate() method.

### cl...@chromium.org (2017-12-12)

[Comment Deleted]

### cl...@chromium.org (2017-12-12)

[Comment Deleted]

### cl...@chromium.org (2017-12-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5464777051865088.

### cl...@chromium.org (2017-12-13)

Detailed report: https://clusterfuzz.com/testcase?key=5464777051865088

Job Type: linux_asan_d8_dbg
Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !cmp_less(*it, *last) in module-decoder.cc
  v8::internal::wasm::ModuleDecoderImpl::DecodeExportSection
  v8::internal::wasm::ModuleDecoderImpl::DecodeSection
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=46985:46986

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5464777051865088

See https://github.com/google/clusterfuzz-tools for more information.

### el...@chromium.org (2017-12-13)

Re #3: As I understand it, the problem is that the DCHECK blocks clusterfuzz from knowing what happens in the absence of the DCHECK.

### cl...@chromium.org (2017-12-13)

Detailed report: https://clusterfuzz.com/testcase?key=5464777051865088

Job Type: linux_asan_d8_dbg
Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !cmp_less(*it, *last) in module-decoder.cc
  v8::internal::wasm::ModuleDecoderImpl::DecodeExportSection
  v8::internal::wasm::ModuleDecoderImpl::DecodeSection
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=46985:46986

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5464777051865088

See https://github.com/google/clusterfuzz-tools for more information.

### ct...@chromium.org (2017-12-13)

I think we've treated other DCHECK triggers in d8 as High severity. Without the DCHECK it is possible this could lead to memory corruption in a sandboxed process.

I've also manually checked that the test case crashes builds going back to August.

### ct...@chromium.org (2017-12-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-27)

titzer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f3c67392acb9804598cc23a142b31abdf4aeaac3

commit f3c67392acb9804598cc23a142b31abdf4aeaac3
Author: Ben L. Titzer <titzer@chromium.org>
Date: Wed Jan 10 10:49:10 2018

[wasm] Improve copying behavior for SyncCompile and SyncValidate

This fixes a long-standing TODO to only make a copy of a module's
wire bytes if the input is a SharedArrayBuffer and also fixes the
concurrent-modification bug for synchronous validation.

R=clemensh@chromium.org
BUG=chromium:794091

Cq-Include-Trybots: master.tryserver.chromium.linux:linux_chromium_rel_ng
Change-Id: I8d2f20a9aeedbc306434853f8f6cfc070a24cf97
Reviewed-on: https://chromium-review.googlesource.com/856559
Commit-Queue: Ben Titzer <titzer@chromium.org>
Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#50472}
[modify] https://crrev.com/f3c67392acb9804598cc23a142b31abdf4aeaac3/src/api.cc
[modify] https://crrev.com/f3c67392acb9804598cc23a142b31abdf4aeaac3/src/wasm/module-compiler.cc
[modify] https://crrev.com/f3c67392acb9804598cc23a142b31abdf4aeaac3/src/wasm/module-compiler.h
[modify] https://crrev.com/f3c67392acb9804598cc23a142b31abdf4aeaac3/src/wasm/wasm-js.cc
[modify] https://crrev.com/f3c67392acb9804598cc23a142b31abdf4aeaac3/test/fuzzer/wasm-async.cc


### ti...@chromium.org (2018-01-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-01-11)

ClusterFuzz has detected this issue as fixed in range 50471:50472.

Detailed report: https://clusterfuzz.com/testcase?key=5464777051865088

Job Type: linux_asan_d8_dbg
Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !cmp_less(*it, *last) in module-decoder.cc
  v8::internal::wasm::ModuleDecoderImpl::DecodeExportSection
  v8::internal::wasm::ModuleDecoderImpl::DecodeSection
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=46985:46986
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=50471:50472

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5464777051865088

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-01-11)

ClusterFuzz testcase 5464777051865088 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### aw...@google.com (2018-01-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-22)

Nice one!  The VRP panel decided to award $3,000 for this report :-)

### aw...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-09)

This bug requires manual review: M65 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-09)

[Bulk Edit]

+awhalley@ (Security TPM) for M65 merge review

### aw...@google.com (2018-02-09)

govind@ - good for 65

### go...@chromium.org (2018-02-09)

Approving merge to M65 branch 3325 based on https://crbug.com/chromium/794091#c28. Please merge ASAP so we can pick it up for next week Beta release. Thank you.

### sh...@chromium.org (2018-02-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2018-02-12)

The fix was landed before the M65 branch point. Removing Merge-Approved label.

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/794091?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089891)*
