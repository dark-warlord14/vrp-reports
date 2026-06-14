# V8 Sandbox Bypass: Incomplete hardening of the experimental regex engine

| Field | Value |
|-------|-------|
| **Issue ID** | [343801366](https://issues.chromium.org/issues/343801366) |
| **Status** | Verified |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Unknown |
| **Reporter** | as...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2024-05-31 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

The experimental regex engine is still not fully guarded against V8 sandbox escapes.
In regexp/experimental/experimental-interpreter.cc [1], the `SET_REGISTER_TO_CP` and `CLEAR_REGISTER` instructions allow OOB on the OS heap where the register array is stored since there are no bounds check that would protect against V8 heap corruption.

```
void RunActiveThread(InterpreterThread t) {
...
    case RegExpInstruction::SET_REGISTER_TO_CP:
      GetRegisterArray(t)[inst.payload.register_index] = input_index_;
      ++t.pc;
      break;
    case RegExpInstruction::CLEAR_REGISTER:
      GetRegisterArray(t)[inst.payload.register_index] =
          kUndefinedRegisterValue;
...

```

The compiled regex bytecode resides on the V8 heap and can be arbitrarily modified by an attacker with arbitrary read/write on the V8 heap.
By overwriting this bytecode you can get an OOB on the OS heap which I then turn into an `*(arb_ptr) = 0` and write to the sandbox target page to demonstrate a bypass.
This exploit consists of the following steps:

- Overwrite the bytecode of a regex object (on the V8 heap) that was compiled with the experimental engine with the following:

```
BEGIN_LOOP, 0x0, CONSUME_RANGE, 0x610061, SET_REGISTER_TO_CP, <OOB_OFFSET>, ASSERTION, ASSERTION_NON_BOUNDARY, END_LOOP, 0x0, JMP, 0x0

```

- Spray (resizable) ArrayBuffer objects in JS that will be allocated on the OS heap
- Execute the regex with the following string: `re.exec("a".repeat(OOB_VALUE) + "b");`. This will lead to the value `OOB_VALUE` being written OOB on the OS heap with offset `OOB_OFFSET` (treated as an int so OOB is possible in both directions). Concretely, I use this to overwrite the backing\_store of a sprayed resizable ArrayBuffer and point it inside the V8 heap.
- Inside the V8 heap, setup a valid backing\_store structure with `backing_store()->buffer_start_ == arb_ptr` (e.g. Sandbox.targetPage)
- Trigger a resize(0) on the ArrayBuffer which will lead to 0 being written to arb\_ptr [2].

To reproduce this, use the attached expl.js below. This relies on heap offsets, so you might need to replicate my setup or adjust those offsets to make it work on other distros.
I developed the repro on commit V8 `58a82800c63473ea7056478188ab491f5021f7dd` and used the following docker image `archlinux:base-20240101.0.204074` .

Note that since there has been an attempt to harden the experimental regex engine against sandbox escapes with commit (a0ee8d65eadb6a9a3ad391b7346db0f9f443adab), this bypass now needs the flag `--enable-experimental-regexp-engine` to work.
However, the root cause of this issue still exists and only the access to the experimental regex engine is not possible anymore.
I believe that since there has been an attempt at hardening the experimental regex engine that this deserves fixing as well.
I am aware that this is not a bypass as by the official rules.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/regexp/experimental/experimental-interpreter.cc;l=475>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/backing-store.cc;l=612>

**VERSION**
Tested on d8 stable (12.5.227.13)

Operating system: Arch Linux

FIX

Inserts SBXCHECKs to guard those two instructions, similar to the checks for `WRITE_LOOKBEHIND_TABLE` and `READ_LOOKBEHIND_TABLE` instructions.

## Attachments

- [expl.js](attachments/expl.js) (text/javascript, 4.3 KB)

## Timeline

### za...@google.com (2024-05-31)

Passing this v8 sandbox bypass bug to the v8 team. Thank you! 

### cl...@appspot.gserviceaccount.com (2024-06-04)

Detailed Report: https://clusterfuzz.com/testcase?key=6292297674063872

Fuzzer: None
Job Type: linux_d8_sandbox_testing
Platform Id: linux

Crash Type: V8 sandbox violation
Crash Address: 
Crash State:
  NULL
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&revision=94221

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6292297674063872

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sa...@google.com (2024-06-04)

Thanks for this report! It reproduces on Clusterfuzz with `--enable-experimental-regexp-engine`. Patrick, could you take a look? I guess since we added the other set of SBXCHECKs into the experimental engine, it makes sense to also add these here?

### pt...@chromium.org (2024-06-04)

Yes definitely makes sense to add SBXCHECKs to the experimental engine, eventhough it is currently unused.
Will prepare a CL.

### ap...@google.com (2024-06-04)

Project: v8/v8
Branch: main

commit b9ed2ba62aa8dd364cf91ddc691e2113636f603f
Author: pthier <pthier@chromium.org>
Date:   Tue Jun 04 11:29:31 2024

    [regexp] Check bounds on register access in experimental engine
    
    Registers in the experimental engine are stored on the stack/heap
    outside the sandbox.
    The register index is stored in the bytecode, which cannot be trusted.
    
    Fixed: 343801366
    Bug: 42204606
    Change-Id: Ia3a297dc0ba071d98d0468218bf304ac3808b07f
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5594090
    Reviewed-by: Camillo Bruni <cbruni@chromium.org>
    Commit-Queue: Patrick Thier <pthier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94228}

M       src/regexp/experimental/experimental-interpreter.cc

https://chromium-review.googlesource.com/5594090


### 24...@project.gserviceaccount.com (2024-06-04)

ClusterFuzz testcase 6292297674063872 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_sandbox_testing&range=94227:94228

If this is incorrect, please add the hotlistid:5432646 and re-open the issue.

### sp...@google.com (2024-07-17)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
reduced V8 heap sandbox bypass reward; reduced reward due to precondition of custom flag


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-17)

Thank you for your efforts and reporting this V8 sandbox bypass to us -- nice work!

### pe...@google.com (2024-09-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/343801366)*
