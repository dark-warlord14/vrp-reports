# Turbofan incorrectly optimizes 64 bit bigint shifts.

| Field | Value |
|-------|-------|
| **Issue ID** | [345960102](https://issues.chromium.org/issues/345960102) |
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

Turbofan incorrectly optimizes 64 bit bigint shifts.

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

We convert the BigInt to an int64\_t (#4) and check if the shift amount is negative. If it is, we negate it and invert the shift op (#5). When converting the BigInt to an int64\_t, we can lose information. `lossless` is `true` if the value represented by the bigint fits into an int64\_t, i.e., is not too big and the `sign` of the bigint and the int64\_t are the same.

A bigint is basically a number of digits that are stored effectively as one's complement with the sign stored separately.
When negating a bigint, we can therefore just negate the sign and leave the digits as they are.
However, the spec [0] also says this:

> For binary operations, BigInts act as two's complement binary strings, with negative numbers treated as having bits set infinitely to the left.

With this out of the way, let's explain where the issue is.
For this we have this poc:

```
y = BigInt("0xffffffffffffffff") // #6
function b() {
    let x = BigInt.asIntN(64, -1n);
    console.log("x: ", x);
    console.log("y: ", y);
    let lol = x >> (y);
    return BigInt.asIntN(64, lol); // #7
}

console.log("lol: ", b());
console.log("lol: ", b());
% OptimizeFunctionOnNextCall(b)
console.log("lol: ", b());

```

We create a bigint `y` (#6) and a function `b` that shifts `-1n` right by `y`. We then call `b` three times. The first two calls print `lol: -1`, but the third call prints `lol: 0`.

We pass (#1), because (#7) truncated the result to a word64. We pass (#2) because `y` is a heap constant. We pass (#3) because `y` is a BigInt. We then convert `y` to an int64\_t (#4). The value of `shift_amount` is `-1`. We therefore negate it and change the opcode to a left shift. `lossless` is false, because `y` is **signed** and `0xffffffffffffffff` does **not** fit into an int64\_t without changing the sign.

```

              // If the operation is a *real* left shift, propagate truncation.
              // If it is a *real* right shift, the output representation is
              // word64 only if we know the input type is BigInt64.
              // Otherwise, fall through to using BigIntOperationHint.
              if (is_shift_left) {
                VisitBinop<T>(
                    node,
                    UseInfo::CheckedBigIntTruncatingWord64(FeedbackSource{}),
                    UseInfo::Any(), MachineRepresentation::kWord64);
                if (lower<T>()) {
                  if (!lossless || shift_amount > 63) {
                    DeferReplacement(node, jsgraph_->Int64Constant(0)); // #8
                  } else if (shift_amount == 0) {
                    DeferReplacement(node, node->InputAt(0));
                  } else {
                    DCHECK_GE(shift_amount, 1);
                    DCHECK_LE(shift_amount, 63);
                    ReplaceWithPureNode(
                        node,
                        graph()->NewNode(
                            lowering->machine()->Word64Shl(), node->InputAt(0),
                            jsgraph_->Int64Constant(shift_amount)));
                  }
                }
                return;

```

After some iterations of the fix-point iteration, we reach (#8), because `lossless` is false and `shift_amount` is `1`. We replace the node with a constant 0.
**This is wrong**.
Why is this wrong?
Our code is:

```
-1n >> 0xffffffffffffffffn

```

and the result should be `-1n` [1].
But V8 treats it as if `-1n` was not a negative number where bits are treated as being set infinitely to the left.
I.e. V8 treats `-1n` as a 64-bit number, where this optimization would be correct.
I believe, the optimization at hand is only correct for positive numbers.

I guess that the thinking is that we can convert all right shift operations to left shift operations, if the right shift amount is negative. The developers probably correctly realized, that the shift amount can **appear** to be negative if the value is too big to fit into an int64\_t. In this case, they concluded that all such spurious left shifts are actually right shifts where the shift amount is actually a very, very big number. For `0n >> very_big_number` the result is `0`, but not for `-1n >> very_big_number`.

IMPACT
Mismatch between interpreter and turbofan.
Interpreter (`-1`. Can be converted to very big value, by using `BigInt.asUintN()`) is correct, turbofan (`0`) is wrong.

EXPLOITABILITY
It's unclear whether this is exploitable to me. Always getting a constant 0 appears to not be very helpful.
There have been similiar issues in SimplifiedLowering in the past [2], [3], but again it's probably not exploitable as is and would require another bug.

REFERENCES
[0] <https://tc39.es/ecma262/multipage/ecmascript-data-types-and-values.html#sec-ecmascript-language-types-bigint-type>
[1] <https://tc39.es/ecma262/multipage/ecmascript-data-types-and-values.html#sec-numeric-types-bigint-signedRightShift>
[2] <https://faraz.faith/2021-01-07-cve-2020-16040-analysis/>
[3] <https://www.thezdi.com/blog/2021/12/8/understanding-the-root-cause-of-cve-2021-21220-a-chrome-bug-from-pwn2own-2021>

VERSION

V8 Version: 258701f221f3966f70abb74ddc88925b9772cc62

Operating System: Linux debian 6.1.0-21-amd64 #1 SMP PREEMPT\_DYNAMIC Debian 6.1.90-1 (2024-05-03) x86\_64 GNU/Linux

REPRODUCTION CASE

1. run poc.js with `d8 --jit-fuzzing --allow-natives-syntax poc.js`

CREDIT INFORMATION
The writeup has been written by Simon Gerst (intrigus-lgtm) based on a testcase originally found by Liam Wachter & Julian Gremminger.

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 325 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-06-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6413282888843264.

### li...@chromium.org (2024-06-10)

Over to v8 sheriff. Going to mark this as medium for now since exploitability isn't clear.

### is...@chromium.org (2024-06-10)

dmercadier@, PTAL.

### dm...@chromium.org (2024-06-11)

That's more Nico's area. He is on vacation today (I think), but should come back tomorrow; given that this doesn't seem easily exploitable, waiting one more day for a fix should be ok :)

(nice writeup Simon btw, very clear and precise, thanks! :) )

### pe...@google.com (2024-06-11)

Setting milestone because of s2 severity.

### in...@gmail.com (2024-06-11)

"BISECT":
All the relevant code has been introduced in <https://chromium.googlesource.com/v8/v8.git/+/2690e2e3a39f6c1325dae0743682c714cbbc98db> so, nothing to really bisect :)

### in...@gmail.com (2024-06-14)

Curious, why is this a duplicate?

### ni...@chromium.org (2024-06-14)

Looked like the same root cause to me at first glance. Taking a more detailed look (thanks for the great analysis) it might indeed by a different problem. I'll take reopen for now and will investigate again next week. Thanks

### ap...@google.com (2024-06-26)

Project: v8/v8
Branch: main

commit 1b85c84da74a325826f4e940d1affee9d94c8beb
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Wed Jun 26 10:48:08 2024

    [turbofan] Skip 64 bit BigInt shift optimizations if not precise
    
    Bug: chromium:345960102
    Change-Id: Id48340944d7fc44cd9314b0b134bd8754c7ea218
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5656773
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#94644}

M       src/compiler/simplified-lowering.cc
M       test/mjsunit/compiler/bigint-shift-left.js
A       test/mjsunit/regress/regress-345960102.js

https://chromium-review.googlesource.com/5656773


### pe...@google.com (2024-06-29)

nicohartmann: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2024-07-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of memory corruption in a non-sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-03)

Congratulations Simon! Thank you for your efforts and reporting this issue to us -- nice work!

### qk...@google.com (2024-09-10)

https://crrev.com/c/5656773 is not applicable to LTS M120 branch because M120 LTS branch doesn't implement `TryOptimizeBigInt64Shift` method.(For your information, the method was implemented by https://chromium-review.googlesource.com/c/v8/v8/+/5626030 on Jun 13, 2024)
So I'm not sure if M120 LTS version was affected by this bug. So I add "LTS-NonApplicable-120" label to this bug.

### qk...@google.com (2024-09-19)

Labeling as LTS-NotApplicable-126 because of the same reason for M120 above.

### pe...@google.com (2024-10-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### am...@chromium.org (2025-08-15)

Hi Simon, p2p-vrp has reached out to convey that they have not received a response to the enrollment request in the past year-plus necessary to process the reward for this issue to you. In accordance with our policies, it will be donated to a charitable organization soon if you do not complete that process to receive it.

### in...@gmail.com (2025-08-16)

Hi Amy,
I assume getting paid via Bugcrowd is not possible when p2p-vrp has already been involved?
Anyway, working on getting this done.

## Bounty Award

> $10,000 for high quality report of memory corruption in a non-sandboxed process + $1,000 bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/345960102)*
