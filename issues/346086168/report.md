# Turbofan incorrectly optimizes 64 bit bigint shifts.

| Field | Value |
|-------|-------|
| **Issue ID** | [346086168](https://issues.chromium.org/issues/346086168) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler>Turbofan |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | in...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2024-06-10 |
| **Bounty** | $11,000.00 |

## Description

VULNERABILITY DETAILS

Debug check failed: shift\_amount >= 0 (-9223372036854775808 vs. 0).

In src/compiler/simplified-lowering.cc "VisitNode(Node\* node, Truncation truncation, SimplifiedLowering\* lowering)" we try to optimize bigint (left and right) shifts:

```
      case IrOpcode::kSpeculativeBigIntShiftLeft:
      case IrOpcode::kSpeculativeBigIntShiftRight: {
        if (truncation.IsUnused() && BothInputsAre(node, Type::BigInt())) {
          VisitUnused<T>(node);
          return;
        }
        if (truncation.IsUsedAsWord64()) { // #1
          Type input_type = GetUpperBound(node->InputAt(0));
          Type shift_amount_type = GetUpperBound(node->InputAt(1));

          if (shift_amount_type.IsHeapConstant()) { // #2
            HeapObjectRef ref = shift_amount_type.AsHeapConstant()->Ref();
            if (ref.IsBigInt()) { // #3

```

We first check if the result is truncated to a word64 (#1), the shift amount is a heap constant (#2) and if it is a BigInt (#3). If all of these conditions are met, we continue with the optimization:

```
              BigIntRef bigint = ref.AsBigInt();
              bool lossless = false;
              int64_t shift_amount = bigint.AsInt64(&lossless); // #4

              // Canonicalize {shift_amount}.
              bool is_shift_left =
                  node->opcode() == IrOpcode::kSpeculativeBigIntShiftLeft;
              if (shift_amount < 0) { // #5
                is_shift_left = !is_shift_left;
                shift_amount = -shift_amount;
              }
              DCHECK_GE(shift_amount, 0);

```

We convert the BigInt to an int64\_t (#4) and check if the shift amount is negative. If it is, we negate it and invert the shift op (#5).

**This negation can fail** if the shift amount is -9223372036854775808 (0x8000000000000000). This is because the negation of this value is the same value, which is not representable in a signed int64\_t.

IMPACT
After commenting the DCHECK*s* out we get a mismatch between interpreter and turbofan.
Interpreter (`0`) is correct, turbofan (`-1`) is wrong.

EXPLOITABILITY
It's unclear whether this is exploitable to me. In contrast to <https://issues.chromium.org/issues/345960102> we don't replace the node with a constant node.
There have been similiar issues in SimplifiedLowering in the past [0], [1], but again it's probably not exploitable as is and would require another bug.

REFERENCES
[0] <https://faraz.faith/2021-01-07-cve-2020-16040-analysis/>
[1] <https://www.thezdi.com/blog/2021/12/8/understanding-the-root-cause-of-cve-2021-21220-a-chrome-bug-from-pwn2own-2021>

VERSION

V8 Version: 258701f221f3966f70abb74ddc88925b9772cc62

Operating System: Linux debian 6.1.0-21-amd64 #1 SMP PREEMPT\_DYNAMIC Debian 6.1.90-1 (2024-05-03) x86\_64 GNU/Linux

REPRODUCTION CASE

1. run poc.js with `d8 --jit-fuzzing --allow-natives-syntax poc.js`

CREDIT INFORMATION
The writeup has been written by Simon Gerst (intrigus-lgtm) after investigating a testcase originally found by Liam Wachter & Julian Gremminger and making a few modifications.

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 317 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-06-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6017133828833280.

### is...@chromium.org (2024-06-10)

dmercadier@, PTAL

### in...@gmail.com (2024-06-11)

"BISECT":
All the relevant code has been introduced in <https://chromium.googlesource.com/v8/v8.git/+/2690e2e3a39f6c1325dae0743682c714cbbc98db> so, nothing to really bisect :)

### pe...@google.com (2024-06-12)

Setting milestone because of s2 severity.

### ni...@chromium.org (2024-06-13)

I agree that this is most likely not exploitable. We do not refine the BigInt type in any of the truncated shift cases and we do not compute ranges for BigInt types, which would lead to type confusion. So this is (to my best guess) a correctness issue.

Fix incoming.

### ap...@google.com (2024-06-13)

Project: v8/v8
Branch: main

commit fd6ff721dc05000ca8b38893bf987711651db383
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Thu Jun 13 14:56:47 2024

    [turbofan] Fix overflow in BigInt64 shift optimization
    
    Bug: chromium:346086168
    Change-Id: I41e3ca5e096d845cb3baffe0b0c5083388ca1a0d
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5626030
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94439}

M       src/compiler/simplified-lowering.cc
A       test/mjsunit/regress/regress-346086168.js

https://chromium-review.googlesource.com/5626030


### am...@chromium.org (2024-06-17)

Thank you for the report. As per c#6 this does not appear to be an exploitable security issue, therefore, this report is unfortunately not eligible for a Chrome VRP reward.

### pe...@google.com (2024-09-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/346086168)*
