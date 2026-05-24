# V8 sandbox bypass: reuse `protected_uses` of `WasmDispatchTable` after grow

| Field | Value |
|-------|-------|
| **Issue ID** | [483220222](https://issues.chromium.org/issues/483220222) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox, Blink>JavaScript>WebAssembly |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pv...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2026-02-10 |
| **Bounty** | $20,000.00 |

## Description

## Detail

- Every `WasmDispatchTable` has `protected_uses` array which contains all `WasmTrustedInstanceData` using that table, so that when this table grows it will update table stored in those instances

```
void WasmDispatchTable::AddUse(Isolate* isolate,
                               DirectHandle<WasmDispatchTable> dispatch_table,
                               DirectHandle<WasmTrustedInstanceData> instance,
                               int table_index) {
  Tagged<ProtectedWeakFixedArray> uses =
      MaybeGrowUsesList(isolate, dispatch_table);
  int cursor = GetUsedLength(uses);
  // {MaybeGrowUsesList} ensures that we have enough capacity.
  SetEntry(uses, cursor, *instance, table_index);
  SetUsedLength(uses, cursor + 2);
}

```

- But on table grow it get the `protected_uses` from the old table and not remove that from old table

```
DirectHandle<WasmDispatchTable> WasmDispatchTable::Grow(
    Isolate* isolate, DirectHandle<WasmDispatchTable> old_table,
    uint32_t new_length) {
...
// Update users.             old table still contains protected_uses
  Tagged<ProtectedWeakFixedArray> uses = old_table->protected_uses(); 
  new_table->set_protected_uses(uses);
 ...

```

- This will cause when old\_table grows again it can update entry in instances that use `new_table`. With this we can "shrink" table in instance by growing `old_table` -> lead to oob read on dispatch table that can be exploitable just like this [issue](https://issues.chromium.org/issues/433407763)
- The exploit is: creaing table with minimum and maxium(1, 0x1000), we call it `table1`, grow it to `0x500` (`table2`), create an instance that imports that module with size(0x501, 0x501), grow `table1` by `1` -> update entry in the instance to `table3`(size 2) -> oob

## Reproduce

- Run `.\d8.exe --expose-memory-corruption-api shrink_table.js`, it will try to write 0xdeadbeef to 0x4141414141414141

## Crash

```
RAX: 414141414141413A   RBX: 0000000000000001   RCX: 0000026E615B0000   
RDX: 00000000DEADBEEF   RSI: 0000026E0100ADD5   RDI: 000002415B1C19C8   
RIP: 000002415B1C19D9   RSP: 000000DD431FE940   RBP: 000000DD431FE960   
R8:  0000027801080000   R9:  0000000000000001   R10: 0000027801040000   
R11: 0000000000000000   R12: 0000000000000000   R13: 0000409400E68080   
R14: 0000027800000000   R15: 0000027801044AFD   
EFLAGS: 00010202 CF=0 PF=0 AF=0 ZF=0 SF=0 TF=0 IF=1 DF=0 OF=0

```
```
(9bac.7c5c): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
00000241`5b1c19d9 48894207        mov     qword ptr [rdx+7],rax ds:00000000`deadbef6=????????????????


```
```
# Child-SP          RetAddr               Call Site
00 000000dd`431fe940 00000241`5b1b1a48     0x00000241`5b1c19d9
01 000000dd`431fe970 00007ff7`7db01fc9     0x00000241`5b1b1a48
02 000000dd`431fe9c0 00007ff7`7dbe6f1c     d8!Builtins_JSToWasmWrapperAsm+0x89
03 000000dd`431fe9f8 00007ff7`7da5a0bc     d8!Builtins_JSToWasmWrapper+0xc5c
04 000000dd`431febf0 00007ff7`7da56e5c     d8!Builtins_InterpreterEntryTrampoline+0x13c
05 000000dd`431fec90 00007ff7`7da569bf     d8!Builtins_JSEntryTrampoline+0x5c
06 000000dd`431fecb8 00007ff7`7c3a6d3e     d8!Builtins_JSEntry+0xff
07 (Inline Function) --------`--------     d8!v8::internal::GeneratedCode<unsigned long long,unsigned long long,unsigned long long,unsigned long long,unsigned long long,long long,unsigned long long **>::Call+0x12 [D:\8_2_2026\v8\src\execution\simulator.h @ 216] 
08 000000dd`431fede0 00007ff7`7c3a71fb     d8!v8::internal::`anonymous namespace'::Invoke+0xe9e [D:\8_2_2026\v8\src\execution\execution.cc @ 441] 
09 000000dd`431fefd0 00007ff7`7c1f31f3     d8!v8::internal::Execution::CallScript+0xdb [D:\8_2_2026\v8\src\execution\execution.cc @ 542] 
0a 000000dd`431ff060 00007ff7`7c15704c     d8!v8::Script::Run+0x2b3 [D:\8_2_2026\v8\src\api\api.cc @ 2028] 
0b 000000dd`431ff1a0 00007ff7`7c176a4e     d8!v8::Shell::ExecuteString+0x78c [D:\8_2_2026\v8\src\d8\d8.cc @ 1039] 
0c 000000dd`431ff440 00007ff7`7c17b1a0     d8!v8::SourceGroup::Execute+0x30e [D:\8_2_2026\v8\src\d8\d8.cc @ 5614] 
0d 000000dd`431ff4f0 00007ff7`7c17adf9     d8!v8::Shell::RunMainIsolate+0x190 [D:\8_2_2026\v8\src\d8\d8.cc @ 6633] 
0e 000000dd`431ff5a0 00007ff7`7c17cdc8     d8!v8::Shell::RunMain+0x129 [D:\8_2_2026\v8\src\d8\d8.cc @ 6541] 
0f 000000dd`431ff630 00007ff7`7dc59688     d8!v8::Shell::Main+0x11d8 [D:\8_2_2026\v8\src\d8\d8.cc @ 7452] 
10 (Inline Function) --------`--------     d8!invoke_main+0x22 [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 78] 
11 000000dd`431ffb90 00007ffd`5aeb259d     d8!__scrt_common_main_seh+0x10c [D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
12 000000dd`431ffbd0 00007ffd`5c42af78     KERNEL32!BaseThreadInitThunk+0x1d
13 000000dd`431ffc00 00000000`00000000     ntdll!RtlUserThreadStart+0x28


```
## Credit

- Nao(@natsumikyouno\_\_)

## Attachments

- [shrink_table.js](attachments/shrink_table.js) (text/javascript, 3.4 KB)

## Timeline

### pv...@gmail.com (2026-02-10)

Oh i should call `callIndirect(0xdeadbeefn, 0x4141414141414141n - 7n)`. The state above shows that it's trying to write to 0xdeadbeef+7

### ts...@google.com (2026-02-10)

Repro'd locally on V8 version 14.6.195 / Linux /Asan after inserting wasm-module-builder.js to make standalone.
Oddly, did not get the sandbox bypass message, just an accv at deadbef6. So left wondering if the issue is in the memory corruption framework rather than V8 itself (e.g. we give you memory corruption, so corrupting memory in and of itself may not be enough.  Except that deadbef6 is out of sandbox?


### ts...@google.com (2026-02-10)

Upoading to CF.

### cl...@appspot.gserviceaccount.com (2026-02-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4780129989361664.

### pv...@gmail.com (2026-02-11)

i can get the sandbox message by modifying the call to `callIndirect(0xdeadbeefn, 0x414141414141n - 7n)`

```
./d8 --sandbox-testing shrink_table.js 
Sandbox testing mode is enabled. Only sandbox violations will be reported, all other crashes will be ignored.
Sandbox bounds: [0x70c700000000,0x71c700000000)
old_table_ptr: 407800
Reuse old table

## V8 sandbox violation detected!

Received signal 11 SEGV_MAPERR 414141414141

==== C stack trace ===============================

./d8(___interceptor_backtrace+0x46)[0x5ac96b573b66]
./d8(+0x6eaf049)[0x5ac970f06049]
./d8(+0x3162413)[0x5ac96d1b9413]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7608e6042520]
[0x7e8c375189d9]
[end of stack trace]
Segmentation fault


```

### cl...@appspot.gserviceaccount.com (2026-02-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4703290407190528.

### el...@chromium.org (2026-02-11)

FoundIn = speculatively extended stable per usual v8 triage guidelines.

### cl...@appspot.gserviceaccount.com (2026-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5352409551273984.

### ch...@google.com (2026-02-12)

Setting milestone because of s2 severity.

### cl...@appspot.gserviceaccount.com (2026-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5345270376103936.

### cl...@appspot.gserviceaccount.com (2026-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5046092685049856.

### cl...@appspot.gserviceaccount.com (2026-02-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4555410790875136.

### om...@chromium.org (2026-02-12)

Also reproduces on V8 ToT (52df14de5bead2d45590c2f90a3cf10d14ff2b73).

Jakob can you take a look?

### jk...@chromium.org (2026-02-13)

Excellent report, thanks! Fix is in flight: <https://chromium-review.googlesource.com/c/v8/v8/+/7575933>

### dx...@google.com (2026-02-13)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7575933>

[sandbox][wasm] Zap WasmDispatchTable::protected\_uses after growth

---


Expand for full commit details
```
     
    Preventing abuse of the old/unused object. 
     
    Fixed: 483220222 
    Change-Id: I19b71a7408ddb11587c801624d92ea4a6f6c4eb3 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7575933 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Omer Katz <omerkatz@chromium.org> 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105269}

```

---

Files:

- M `src/wasm/wasm-objects.cc`

---

Hash: [dc31719c947c12a0d7121978c136a006ba4e29c0](https://chromiumdash.appspot.com/commit/dc31719c947c12a0d7121978c136a006ba4e29c0)  

Date: Fri Feb 13 16:42:43 2026


---

### sa...@google.com (2026-02-17)

As the fix seems pretty trivial, we think it would be worth backmerging it as the bug allows breaking out of the V8 Sandbox.

### ch...@google.com (2026-02-17)

Merge review required: M146 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-17)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### jk...@chromium.org (2026-02-17)

#18/#19:

1. The patch improves security hardening, see [comment #17](https://issues.chromium.org/issues/483220222#comment17).
2. <https://chromium-review.googlesource.com/7575933>
3. Yes, 147.0.7687.0
4. No, old feature
5. N/A
6. No manual testing needed

### dr...@chromium.org (2026-02-19)

No crashes in Canary yet, merge approved to 145 and 146

### dx...@google.com (2026-02-19)

Project: v8/v8  

Branch:  refs/branch-heads/14.5  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7592747>

Merged: [sandbox][wasm] Zap WasmDispatchTable::protected\_uses after growth

---


Expand for full commit details
```
     
    Preventing abuse of the old/unused object. 
     
    Fixed: 483220222 
    (cherry picked from commit dc31719c947c12a0d7121978c136a006ba4e29c0) 
     
    Change-Id: I5c2f5b6ca4c9b9c4f316831c0d23b5acfe6f29e4 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7592747 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.5@{#20} 
    Cr-Branched-From: f09d67c66114951c0ea3dc9d4b025461670a9557-refs/heads/14.5.201@{#2} 
    Cr-Branched-From: 3f006438f768659ed9776359a421dc432edce53f-refs/heads/main@{#104623}

```

---

Files:

- M `src/wasm/wasm-objects.cc`

---

Hash: [08f049aa86deb98efa928999a50c4ed45d9db23e](https://chromiumdash.appspot.com/commit/08f049aa86deb98efa928999a50c4ed45d9db23e)  

Date: Fri Feb 13 16:42:43 2026


---

### dx...@google.com (2026-02-19)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7593037>

Merged: [sandbox][wasm] Zap WasmDispatchTable::protected\_uses after growth

---


Expand for full commit details
```
     
    Preventing abuse of the old/unused object. 
     
    Fixed: 483220222 
    (cherry picked from commit dc31719c947c12a0d7121978c136a006ba4e29c0) 
     
    Change-Id: Ib9416026ba67f28621f9c6dbaf45df8cf4f07ec3 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7593037 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Matthias Liedtke <mliedtke@chromium.org> 
    Reviewed-by: Matthias Liedtke <mliedtke@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#5} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/wasm/wasm-objects.cc`

---

Hash: [3ae89fe3ba4a152374856bbee76de5c8520c25c7](https://chromiumdash.appspot.com/commit/3ae89fe3ba4a152374856bbee76de5c8520c25c7)  

Date: Fri Feb 13 16:42:43 2026


---

### pe...@google.com (2026-02-19)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### jk...@chromium.org (2026-02-19)

#24: old bug in an old feature, probably worth merging to M144. Note that this is "only" a sandbox escape, i.e. an additional layer of security. It's not exploitable (or crashing, etc) on its own, but makes it easier to turn *other* bugs into security exploits.

### qk...@google.com (2026-02-20)

Added `Not-Applicable-138` label because the fix required the CL[1], but M138 didn't have it.

[1] <https://chromium-review.googlesource.com/c/v8/v8/+/6972023>

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $20000.00 for this report.

Rationale for this decision:
Controlled write outside the V8 sandbox


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-04-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-04-09)

1. https://chromium-review.git.corp.google.com/c/v8/v8/+/7734227
2. Low - There was no conflict.
3. 145 and 146
4. Yes, this is an old bug.

### an...@google.com (2026-04-10)

Merge approved for LTS-144.

### dx...@google.com (2026-04-16)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7734227>

[M144-LTS][sandbox][wasm] Zap WasmDispatchTable::protected\_uses after growth

---


Expand for full commit details
```
     
    Preventing abuse of the old/unused object. 
     
    (cherry picked from commit dc31719c947c12a0d7121978c136a006ba4e29c0) 
     
    Fixed: 483220222 
    Change-Id: I19b71a7408ddb11587c801624d92ea4a6f6c4eb3 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7575933 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Commit-Queue: Omer Katz <omerkatz@chromium.org> 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Clemens Backes <clemensb@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#105269} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7734227 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#69} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/wasm/wasm-objects.cc`

---

Hash: [a650c8e7ec321191cc7ef8b4931b2377d97718ee](https://chromiumdash.appspot.com/commit/a650c8e7ec321191cc7ef8b4931b2377d97718ee)  

Date: Fri Feb 13 16:42:43 2026


---

### ch...@google.com (2026-05-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Controlled write outside the V8 sandbox

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483220222)*
