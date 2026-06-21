# ## V8 Sandbox Bypass: Native stack OOB write in arm64 `Generate_PushBoundArguments`

| Field | Value |
|-------|-------|
| **Issue ID** | [481749436](https://issues.chromium.org/issues/481749436) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Sandbox |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2026-02-05 |
| **Bounty** | $5,000.00 |

## Description

## VULNERABILITY DETAILS

### Summary

A V8 sandbox bypass on **arm64**: the builtin helper `Generate_PushBoundArguments()` reads `JSBoundFunction::[[BoundArguments]]` (a `FixedArray`) and **untags its `length_` as a signed value** without validating it is non-negative. Attacker can set `FixedArray.length_` to a **negative Smi** causes:

- the **stack overflow check to be bypassed**
- an **unbounded copy loop** controlled by a negative counter, and
- **continuous, attacker-influenced stores** to a stack region outside the sandbox until a crash.

### Details

#### The Bug

The arm64 implementation of `Generate_PushBoundArguments()` uses `SmiUntagField` on `FixedArray::length_` (signed) and only checks for zero. A negative value therefore enters the “has bound args” path.

Key behaviors when `bound_argc < 0`:

- **Bypass stack overflow check**: required space is computed as `bound_argc << 3` and compared using a signed branch; negative “required” space trivially passes.
- **Unbounded copy loop**: the loop counter is initialized from `bound_argc` and decremented until it becomes zero. Negative values will never reach zero in practice, so the loop stores indefinitely.
- **Native stack writes**: the loop writes one pointer-sized slot per iteration via `str ..., [copy_to], #8`, walking `copy_to` upwards and smashing stack memory outside the sandbox.

```
void Generate_PushBoundArguments(MacroAssembler* masm) {
  // ----------- S t a t e -------------
  //  -- x0 : the number of arguments
  //  -- x1 : target (checked to be a JSBoundFunction)
  //  -- x3 : new.target (only in case of [[Construct]])
  // -----------------------------------

  Register bound_argc = x4;
  Register bound_argv = x2;

  // Load [[BoundArguments]] into x2 and length of that into x4.
  Label no_bound_arguments;
  __ LoadTaggedField(
      bound_argv, FieldMemOperand(x1, JSBoundFunction::kBoundArgumentsOffset));
  __ SmiUntagField(bound_argc,
                   FieldMemOperand(bound_argv, offsetof(FixedArray, length_)));
  __ Cbz(bound_argc, &no_bound_arguments);
  {
    Register argc = x0;

    // Check for stack overflow.
    {
      Label done;
      __ LoadStackLimit(x10, StackLimitKind::kRealStackLimit);
      __ Sub(x10, sp, x10);
      __ Cmp(x10, Operand(bound_argc, LSL, kSystemPointerSizeLog2));
      __ B(gt, &done);
      __ TailCallRuntime(Runtime::kThrowStackOverflow);
      __ Bind(&done);
    }

    Label copy_bound_args;
    Register total_argc = x15;
    Register slots_to_claim = x12;
    Register scratch = x10;
    Register receiver = x14;

    __ Sub(argc, argc, kJSArgcReceiverSlots);
    __ Add(total_argc, argc, bound_argc);
    __ Peek(receiver, 0);

    // Round up slots_to_claim to an even number if it is odd.
    __ Add(slots_to_claim, bound_argc, 1);
    __ Bic(slots_to_claim, slots_to_claim, 1);
    __ Claim(slots_to_claim, kSystemPointerSize);

    // ... alignment handling omitted ...

    __ Bind(&copy_bound_args);

    // Copy the receiver back.
    __ Poke(receiver, 0);
    // Copy [[BoundArguments]] to the stack (below the receiver).
    {
      Label loop;
      Register counter = bound_argc;
      Register copy_to = x12;
      __ Add(bound_argv, bound_argv,
             OFFSET_OF_DATA_START(FixedArray) - kHeapObjectTag);
      __ SlotAddress(copy_to, 1);
      __ Bind(&loop);
      __ Sub(counter, counter, 1);
      __ LoadTaggedField(scratch,
                         MemOperand(bound_argv, kTaggedSize, PostIndex));
      __ Str(scratch, MemOperand(copy_to, kSystemPointerSize, PostIndex));
      __ Cbnz(counter, &loop);
    }
    // Update argc.
    __ Add(argc, total_argc, kJSArgcReceiverSlots);
  }
  __ Bind(&no_bound_arguments);
}

```
## Validation on x86\_64 host via arm64 simulator

I only have an **x86\_64** machine. To validate an **arm64** builtin bug, I built V8 with `target_cpu="arm64"` and ran `d8` on x86\_64. V8 then executes generated arm64 code through its **arm64 simulator**.

The excerpt below shows the exact repeating instruction sequence:

- `sub x4, x4, #1` where `x4` is a **negative** counter (e.g. `0xfffffffffffffe4b`, `...fe4a`, …),
- `str x10, [x12], #8` performing **8-byte stores**, and
- `x12` increasing monotonically until the crash occurs at `...5007`, consistent with an 8-byte access crossing into an unmapped/guard region.

```
0x00005604f7dc8600  b5ffff84            cbnz x4, #-0x10 (addr 0x5604f7dc85f0)
0x00005604f7dc85f0  d1000484            sub x4, x4, #0x1 (1)
#    x4: 0xfffffffffffffe4b
0x00005604f7dc85f4  b840444a            ldr w10, [x2], #4
0x00005604f7dc85f8  aa0a038a            orr x10, x28, x10
0x00005604f7dc85fc  f800858a            str x10, [x12], #8
#    x12: 0x00001b5401204ef8
...
0x00005604f7dc85fc  f800858a            str x10, [x12], #8
#    x12: 0x00001b5401205000

## V8 sandbox violation detected!
Received signal 11 SEGV_ACCERR 1b5401205007

```

This validates the core bug properties **without native arm64 hardware**: negative counter never reaches zero, and the builtin performs repeated `str` stores to a stack-like region outside the sandbox bounds.

## Issues with Sandbox Crash Filter (simulator “read vs write” confusion)

When running an arm64 target via the simulator, the crash filter may report:

> “The sandbox violation was a *read* access…”

even when the bug’s semantic is a **write**.

This happens because the simulator often uses a probing mechanism (e.g. `ProbeMemory`) that performs a host-side **read** to check address validity before emulating the load/store, so the *faulting host instruction* can be a read. The **`--trace-sim`** arm64 instruction log is therefore the authoritative source to confirm the presence of `str` stores and the write address progression.

## VERSION

14.6.146

## REPRODUCTION CASE

### Build (arm64 target on x86\_64 host, simulator mode)

1. Generate an arm64 GN build directory:

```
tools/dev/v8gen.py arm64.release
# Add v8_enable_memory_corruption_api = true
# Add v8_enable_sandbox = true

```

2. Build `d8`:

```
ninja -C out.gn/arm64.release d8

```
### Run

```
out.gn/arm64.release/d8 --sandbox-testing --trace-sim poc.js

```
## FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

**Type of crash**: v8 sandbox violation

## CREDIT INFORMATION

Reporter credit: Picasso

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 626 B)

## Timeline

### ch...@google.com (2026-02-05)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### xi...@chromium.org (2026-02-05)

Thanks for the report. Assigning to v8 shepherd to triage v8 sandbox bypass issues.

### cl...@appspot.gserviceaccount.com (2026-02-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6322476367675392.

### ta...@google.com (2026-02-06)

Hi Toon, I believe you were working on related code recently. CYPTAL? I have a problem with reproducing, but the description is precise and the reporter has a history of correct reports.

### cl...@appspot.gserviceaccount.com (2026-02-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4769040115367936.

### pi...@gmail.com (2026-03-10)

Hello, is there any update?

### ve...@chromium.org (2026-03-12)

Not yet, sorry, will look tomorrow.

### ve...@chromium.org (2026-03-13)

There was a duplicate report and it's already fixed by <https://chromium-review.git.corp.google.com/c/v8/v8/+/7649110>.

### pi...@gmail.com (2026-05-14)

Hello, any reward update?

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. v8 sandbox


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-20)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/481749436)*
