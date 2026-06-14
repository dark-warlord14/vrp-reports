# Debug check failed JSFunction::GetDerivedMap

| Field | Value |
|-------|-------|
| **Issue ID** | [40093162](https://issues.chromium.org/issues/40093162) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2018-11-22 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36

Steps to reproduce the problem:
Poc:
a = function(){ return {}; };
b = function(){ return {}; }; 
c = Proxy; 
foo = function(){  Reflect.construct(a,b,c); }; 
foo()

What is the expected behavior?

What went wrong?
#
# Fatal error in ../../src/objects/js-objects-inl.h, line 570
# Debug check failed: has_prototype_slot().
#
#
#
#FailureMessage Object: 0xffda3500
==== C stack trace ===============================

    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x31) [0xf4a64311]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8_libplatform.so(+0x2203c) [0xf4a0203c]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x13a) [0xf4a438aa]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8_libbase.so(+0x262a6) [0xf4a432a6]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x4f) [0xf4a439cf]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(v8::internal::JSFunction::has_initial_map()+0x68) [0xf53b4ce8]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(+0x19b8d5a) [0xf642cd5a]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(v8::internal::JSFunction::GetDerivedMap(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::JSReceiver>)+0x1d0) [0xf63c93b0]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(v8::internal::JSObject::New(v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::JSReceiver>, v8::internal::Handle<v8::internal::AllocationSite>)+0x21a) [0xf63c8faa]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(+0x1d34fbf) [0xf67a8fbf]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(v8::internal::Runtime_NewObject(int, unsigned int*, v8::internal::Isolate*)+0x17c) [0xf67a8a3c]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(+0x265e0b0) [0xf70d20b0]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(+0x233a9e2) [0xf6dae9e2]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(+0x234e2c2) [0xf6dc22c2]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(+0x234e2c2) [0xf6dc22c2]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(+0x2344d61) [0xf6db8d61]
    [0x544020fc]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(v8::internal::GeneratedCode<v8::internal::Object*, v8::internal::Object*, v8::internal::Object*, v8::internal::Object*, int, v8::internal::Object***>::Call(v8::internal::Object*, v8::internal::Object*, v8::internal::Object*, int, v8::internal::Object***)+0x8f) [0xf5fa5f0f]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(+0x152f230) [0xf5fa3230]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(+0x152e643) [0xf5fa2643]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(v8::internal::Execution::Call(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*)+0x95) [0xf5fa2485]
    /home/ubuntu/v8/v8/out.gn/ia32.debug/./libv8.so(v8::Script::Run(v8::Local<v8::Context>)+0x416) [0xf53da436]
    ./d8(v8::Shell::ExecuteString(v8::Isolate*, v8::Local<v8::String>, v8::Local<v8::Value>, v8::Shell::PrintResult, v8::Shell::ReportExceptions, v8::Shell::ProcessMessageQueue)+0x984) [0x56627094]
    ./d8(v8::SourceGroup::Execute(v8::Isolate*)+0x50e) [0x5663cbce]
    ./d8(v8::Shell::RunMain(v8::Isolate*, int, char**, bool)+0x1d1) [0x56641061]
    ./d8(v8::Shell::Main(int, char**)+0x1d74) [0x56643724]
    ./d8(main+0x3c) [0x56643d1c]
    /lib/i386-linux-gnu/libc.so.6(__libc_start_main+0xf7) [0xf4602637]
Received signal 4 ILL_ILLOPN 0000f4a60af1

Reporter: cyrilliu in Tencent Zhanlu Lab

Did this work before? N/A 

Chrome version: 70.0.3538.110  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### do...@chromium.org (2018-11-22)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2018-11-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4820958042652672.

### cl...@chromium.org (2018-11-26)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/4ef4deae6eb3277b0ce63908661bac9f64eea386 ([runtime] Change the default values of Proxy.prototype to undefined from null).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2018-11-26)

Detailed report: https://clusterfuzz.com/testcase?key=4820958042652672

Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  has_prototype_slot() in js-objects-inl.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=54744:54745

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4820958042652672

See https://github.com/google/clusterfuzz-tools for more information.

### mb...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### ve...@chromium.org (2018-11-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-11-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/7a3cb59fadb6e8fcdc00b25e31ee21adf07538d5

commit 7a3cb59fadb6e8fcdc00b25e31ee21adf07538d5
Author: Camillo Bruni <cbruni@chromium.org>
Date: Tue Nov 27 11:52:41 2018

Fix Reflect.construct with constructors without a prototype slot

Bug: chromium:907714
Change-Id: Ie8eacff1b12ec74faa392a1d2c8545f873ab13a1
Reviewed-on: https://chromium-review.googlesource.com/c/1351023
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#57866}
[modify] https://crrev.com/7a3cb59fadb6e8fcdc00b25e31ee21adf07538d5/src/objects.cc
[add] https://crrev.com/7a3cb59fadb6e8fcdc00b25e31ee21adf07538d5/test/mjsunit/regress/regress-crbug-90771.js


### ct...@chromium.org (2018-11-27)

Security sheriff here: Tentatively labeling this Severity-Medium per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md -- my cursory look at the DCHECK and the code after makes it seem like reaching this code in non-debug builds could potentially trigger an out-of-bounds read (looking https://cs.chromium.org/chromium/src/v8/src/objects/js-objects-inl.h?sq=package:chromium&g=0&l=561). If that is incorrect, please let me know and we can re-label.

### cl...@chromium.org (2018-11-28)

ClusterFuzz has detected this issue as fixed in range 57865:57866.

Detailed report: https://clusterfuzz.com/testcase?key=4820958042652672

Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  has_prototype_slot() in js-objects-inl.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=54744:54745
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=57865:57866

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4820958042652672

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-11-28)

ClusterFuzz testcase 4820958042652672 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### cb...@chromium.org (2018-11-28)

In response to https://crbug.com/chromium/907714#c8:

Yes, there will be an OOB read since kPrototypeOrInitialMapOffset is used in JSFunction::has_initial_map() and JSFunction::initial_map(). 

However, even in release mode there are a few checks in place which most likely will result in a SEGFAULT or slightly incorrect language semantics (wrong constructor).


FastInitializeDerivedMap (https://cs.chromium.org/chromium/src/v8/src/objects.cc?type=cs&q=FastInitializeDerivedMap&g=0&l=13382) does several dynamic checks:
- has_initial_map does a IsMap() check which quite likely will succed if the there is an object right after the new_target in memory (the first word of any object is the map pointer). In the other case 

- new_target->initial_map()->GetConstructor() will most likely succe for any Map object, but since there is a explicit raw pointer comparison against the existing constructor the returned value is most likely irrelevant and might just fail.

- As a result we most likely end up creating a new Map and the size calculated in JSFunction::CalculateInstanceSizeForDerivedClass is some arbitrary number, however, this is going to be in sync with the newly created Map. Hence there is no OOB read or write  possible trough the newly created object.

Worst case scenario: You can read the Map of the object following right after the new_target object in memory. This might be from a dead or live Object or a filler Map used by the GC.

### cb...@chromium.org (2018-11-28)

Asking for a merge request back to M71 since this is a very simple fix.

### sh...@chromium.org (2018-11-28)

This bug requires manual review: Less than 2 days to go before AppStore submit on M71
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-11-28)

[Empty comment from Monorail migration]

### go...@chromium.org (2018-11-28)

+hablich@ & awhalley@ for M71 merge review.

### ha...@chromium.org (2018-11-28)

[Empty comment from Monorail migration]

### ct...@chromium.org (2018-11-28)

Minor fix to OS labels: This does not affect iOS since we do not ship Blink/V8 there.

### aw...@chromium.org (2018-11-28)

[Empty comment from Monorail migration]

### cb...@chromium.org (2018-11-29)

Backmerging tomorrow after enough canary coverage, so far 72.0.3625.0 looks good.

### go...@chromium.org (2018-11-29)

Pls merge tomorrow morning PT if change continue to look good in canary, we're planning to cut M71 stable RC @ 11:00 AM PT tomorrow. Thank you.

### bu...@chromium.org (2018-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c261e8393cefe522562c99c00ab8703f68fee594

commit c261e8393cefe522562c99c00ab8703f68fee594
Author: Camillo Bruni <cbruni@chromium.org>
Date: Fri Nov 30 13:06:30 2018

Merged: Fix Reflect.construct with constructors without a prototype slot

Revision: 7a3cb59fadb6e8fcdc00b25e31ee21adf07538d5

BUG=chromium:907714
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=verwaest@chromium.org

Change-Id: I66a75cd7dd4884eb640236e602ac059c7b280528
Reviewed-on: https://chromium-review.googlesource.com/c/1356513
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/branch-heads/7.1@{#57}
Cr-Branched-From: f70aaa8ab2e8815505a6145c745e50d8328cd28c-refs/heads/7.1.302@{#1}
Cr-Branched-From: 1dbcc78efa17a9047f7e923958087ef9eec43066-refs/heads/master@{#56462}
[modify] https://crrev.com/c261e8393cefe522562c99c00ab8703f68fee594/src/objects.cc
[add] https://crrev.com/c261e8393cefe522562c99c00ab8703f68fee594/test/mjsunit/regress/regress-crbug-90771.js


### go...@chromium.org (2018-11-30)

Removing "Merge-Approved-71" label as this is already merged to M71 at #22.

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-12-07)

Hi! The Chrome VRP panel decided to award $1,000 for this bug - many thanks! A member of our finance team will be in touch to arrange payment details.

### aw...@google.com (2018-12-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-03-06)

This issue was migrated from crbug.com/chromium/907714?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093162)*
