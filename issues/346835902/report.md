# Debug check failed: Object::FitsRepresentation(*object, representation). in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [346835902](https://issues.chromium.org/issues/346835902) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-06-13 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 94239
    - link: https://crrev.com/d8bc0da831599b038cabab63b45b63cc28db2687 
- Commit Message

```
commit d8bc0da831599b038cabab63b45b63cc28db2687
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Tue Jun 4 15:06:24 2024 +0200

    [ic] Ensure clone IC respects field type
    
    We can only use a clone IC if a field type change in the target map
    cannot produce a field type that is invalid with respect to entries that
    are created by the clone IC.
    
    Drive-By: Also exclude the int->double case that was accidentally
              allowed.
    
    Fixed: 344638604
    Fixed: 344669837
    Change-Id: Id92f57cf0eadb5d155e268ca2315b3a74644febc
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5595017
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Reviewed-by: Igor Sheludko <ishell@chromium.org>
    Commit-Queue: Igor Sheludko <ishell@chromium.org>
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94239}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-94416/d8 --jit-fuzzing poc.js
# OUTPUT ==============================================================


#
# Fatal error in ../../src/objects/objects.cc, line 255
# Debug check failed: Object::FitsRepresentation(*object, representation).
#
#
#
#FailureMessage Object: 0x7fffb82bd4d0
==== C stack trace ===============================

    /tmp/d8-linux-debug-v8-component-94416/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f8cc1bf4f03]
    /tmp/d8-linux-debug-v8-component-94416/libv8_libplatform.so(+0x18e3d) [0x7f8cc70d2e3d]
    /tmp/d8-linux-debug-v8-component-94416/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f8cc1bd60e4]
    /tmp/d8-linux-debug-v8-component-94416/libv8_libbase.so(+0x2bb05) [0x7f8cc1bd5b05]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>> v8::internal::Object::WrapForRead<(v8::internal::AllocationType)0, v8::internal::Isolate>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNumber, v8::internal::BigInt, v8::internal::String, v8::internal::Symbol, v8::internal::Boolean, v8::internal::Null, v8::internal::Undefined, v8::internal::JSReceiver>>, v8::internal::Representation)+0x24c) [0x7f8cc50149fc]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::JSObject::FastPropertyAt(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSObject>, v8::internal::Representation, v8::internal::FieldIndex)+0xa0) [0x7f8cc4e903b0]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::LookupIterator::FetchValue(v8::internal::AllocationPolicy) const+0x717) [0x7f8cc4fc4747]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::Object::GetProperty(v8::internal::LookupIterator*, bool)+0x8f) [0x7f8cc507742f]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::JSReceiver::GetOwnPropertyDescriptor(v8::internal::LookupIterator*, v8::internal::PropertyDescriptor*)+0xae8) [0x7f8cc4e85118]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::JSReceiver::OrdinaryDefineOwnProperty(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSObject>, v8::internal::PropertyKey const&, v8::internal::PropertyDescriptor*, v8::Maybe<v8::internal::ShouldThrow>)+0x146) [0x7f8cc4e843c6]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::JSReceiver::OrdinaryDefineOwnProperty(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSObject>, v8::internal::Handle<v8::internal::Object>, v8::internal::PropertyDescriptor*, v8::Maybe<v8::internal::ShouldThrow>)+0x1a5) [0x7f8cc4e84195]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::JSReceiver::DefineOwnProperty(v8::internal::Isolate*, v8::internal::Handle<v8::internal::JSReceiver>, v8::internal::Handle<v8::internal::Object>, v8::internal::PropertyDescriptor*, v8::Maybe<v8::internal::ShouldThrow>)+0x560) [0x7f8cc4e83210]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::JSReceiver::DefineProperty(v8::internal::Isolate*, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>)+0x16a) [0x7f8cc4e829fa]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(+0x277bc8d) [0x7f8cc437bc8d]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(v8::internal::Builtin_ObjectDefineProperty(int, unsigned long*, v8::internal::Isolate*)+0x7d) [0x7f8cc437b94d]
    /tmp/d8-linux-debug-v8-component-94416/libv8.so(+0x1dee3bd) [0x7f8cc39ee3bd]

```

## Other
Please note to include the flags `--jit-fuzzing` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.7.0 - 12.8.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-94416.zip
2. Run: `d8 --jit-fuzzing poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)    


## Attachments

- [output_poc.js](attachments/output_poc.js) (text/javascript, 1.2 KB)
- [poc.js](attachments/poc.js) (text/javascript, 456 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-06-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6690426898546688.

### ki...@gmail.com (2024-06-13)

Mini poc is attached below.

### pg...@google.com (2024-06-13)

Clusterfuzz is still working on getting the remaining fields, but over to the V8 sheriff for the full triage!

### 24...@project.gserviceaccount.com (2024-06-13)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-06-13)

Detailed Report: https://clusterfuzz.com/testcase?key=6690426898546688

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  Object::FitsRepresentation(*object, representation) in objects.cc
  v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNu
  v8::internal::JSObject::FastPropertyAt
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=94238:94239

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6690426898546688

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ol...@chromium.org (2024-06-13)

yay @kipreyxx, brilliant find again. thanks! While the other one was benign, this one isn't!

### ol...@chromium.org (2024-06-13)

ok, this was one issue too many, let's disable this on 127. @pgrace I would like to merge https://chromium-review.googlesource.com/c/v8/v8/+/5625901 to 127.

### ap...@google.com (2024-06-13)

Project: v8/v8
Branch: main

commit 6e8923c8232c723f8c4bca0b8e7900696e8c5792
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Thu Jun 13 09:41:45 2024

    [ic] Move side-step transitions behind future for now
    
    Needs some more time to iron out issues.
    
    Bug: 346835902
    Bug: 346386746
    Change-Id: I199bc6da9d4c7c2e5fe4cabee349c7599ce93478
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5625901
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Reviewed-by: Igor Sheludko <ishell@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Commit-Queue: Igor Sheludko <ishell@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94420}

M       src/flags/flag-definitions.h

https://chromium-review.googlesource.com/5625901


### ap...@google.com (2024-06-13)

Project: v8/v8
Branch: main

commit 98eb9e2fb0b17373a3726a0f4d56fed3eb63f88f
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Thu Jun 13 11:14:25 2024

    [ic] Fix representation confusion in clone IC
    
    By deprecating the target map of a clone IC it can be tricked into
    creating objects with type confused contents. This works as follows:
    
    1. Setup IC copying smi -> smi
    2. Deprecate the target map
    3. Create another clone IC, which overrides the deprecated side-step
    4. Transition the source to tagged -- doesn't update deprecated target
    5. Original IC now clones from tagged -> smi (deprecated)
    
    Fixed: 346835902
    Change-Id: I94180af1047daee202a691d04836047b09c16ebe
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5625902
    Reviewed-by: Igor Sheludko <ishell@chromium.org>
    Commit-Queue: Igor Sheludko <ishell@chromium.org>
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94428}

M       src/ic/accessor-assembler.cc

https://chromium-review.googlesource.com/5625902


### pe...@google.com (2024-06-13)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-06-13)

Project: v8/v8
Branch: chromium/6535

commit ca0b5c331967a72c127041bc08cc515d86d78557
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Thu Jun 13 09:41:45 2024

    Merged: [ic] Move side-step transitions behind future for now
    
    Needs some more time to iron out issues.
    
    Bug: 346835902
    Bug: 346386746
    (cherry picked from commit 6e8923c8232c723f8c4bca0b8e7900696e8c5792)
    
    Change-Id: I33cc73959a859df508673271e90b95b23be14a5b
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5630498
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>

M       src/flags/flag-definitions.h

https://chromium-review.googlesource.com/5630498


### 24...@project.gserviceaccount.com (2024-06-14)

ClusterFuzz testcase 6690426898546688 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=94419:94420

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### ap...@google.com (2024-06-14)

Project: v8/v8
Branch: refs/branch-heads/12.7

commit 7fc0a4cbab1fca823ebedb0970934346a35b2ccf
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Thu Jun 13 09:41:45 2024

    Merged: [ic] Move side-step transitions behind future for now
    
    Needs some more time to iron out issues.
    
    Bug: 346835902
    Bug: 346386746
    (cherry picked from commit 6e8923c8232c723f8c4bca0b8e7900696e8c5792)
    
    Change-Id: I7950b628dfe547115adf611bb53196874fbba518
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5633594
    Reviewed-by: Olivier Flückiger <olivf@chromium.org>
    Commit-Queue: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/branch-heads/12.7@{#8}
    Cr-Branched-From: 35cc908918d3f8083955ed8328506f964e17ae40-refs/heads/12.7.224@{#1}
    Cr-Branched-From: 6d60e6734b32211215c8410db6fe2b84b13abe0e-refs/heads/main@{#94324}

M       src/flags/flag-definitions.h

https://chromium-review.googlesource.com/5633594


### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Congratulations, Zhenghang! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-09-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/346835902)*
