# Security: Out of bounds memory access in BigInt

| Field | Value |
|-------|-------|
| **Issue ID** | [40056682](https://issues.chromium.org/issues/40056682) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | p4...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2021-07-27 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

when dealing with divide operation in bigint, it calculates the result length in `DivideResultLength`[1], and use the length to alloc a bigint object [2].

```
MaybeHandle<BigInt> BigInt::Divide(Isolate\* isolate, Handle<BigInt> x,  
                                   Handle<BigInt> y) {  
  // 1. If y is 0n, throw a RangeError exception.  
  if (y->is_zero()) {  
    THROW_NEW_ERROR(isolate, NewRangeError(MessageTemplate::kBigIntDivZero),  
                    BigInt);  
  }  
  // 2. Let quotient be the mathematical value of x divided by y.  
  // 3. Return a BigInt representing quotient rounded towards 0 to the next  
  //    integral value.  
  if (bigint::Compare(GetDigits(x), GetDigits(y)) < 0) {  
    return Zero(isolate);  
  }  
  bool result_sign = x->sign() != y->sign();  
  if (y->length() == 1 && y->digit(0) == 1) {  
    return result_sign == x->sign() ? x : UnaryMinus(isolate, x);  
  }  
  Handle<MutableBigInt> quotient;  
 [1] int result_length = bigint::DivideResultLength(GetDigits(x), GetDigits(y));  
 [2] if (!MutableBigInt::New(isolate, result_length).ToHandle(&quotient)) {  
    return {};  
  }  
  DisallowGarbageCollection no_gc;  
  bigint::Status status = isolate->bigint_processor()->Divide(  
      GetRWDigits(quotient), GetDigits(x), GetDigits(y));  
  if (status == bigint::Status::kInterrupted) {  
    AllowGarbageCollection terminating_anyway;  
    isolate->TerminateExecution();  
    return {};  
  }  
  quotient->set_sign(result_sign);  
  return MutableBigInt::MakeImmutable(quotient);  
}  

```

the length is `A.len() - B.len() + 1 + 0`

```
inline int DivideResultLength(Digits A, Digits B) {  
#if V8_ADVANCED_BIGINT_ALGORITHMS  
  // The Barrett division algorithm needs one extra digit for temporary use.  
  int kBarrettExtraScratch = B.len() >= kBarrettThreshold ? 1 : 0;  
#else  
  constexpr int kBarrettExtraScratch = 0;  
#endif  
  return A.len() - B.len() + 1 + kBarrettExtraScratch;  
}  

```

But the length of A and B can be modified at following function. In `ProcessorImpl::DivideBarrett`, it will generate a `ShiftedDigits` variable ([2][1]) and use them to call `DivideBarrett`[3].

```
void ProcessorImpl::DivideBarrett(RWDigits Q, RWDigits R, Digits A, Digits B) {  
  DCHECK(Q.len() > A.len() - B.len());  
  DCHECK(R.len() >= B.len());  
  DCHECK(A.len() > B.len());  // Careful: This is \*not\* '>=' !  
  DCHECK(B.len() > 0);        // NOLINT(readability/check)  
  
  // Normalize B, and shift A by the same amount.  
[1]  ShiftedDigits b_normalized(B);  
[2]  ShiftedDigits a_normalized(A, b_normalized.shift());  
  // Keep the code below more concise.  
  B = b_normalized;  
  A = a_normalized;  
  
// [...]  
  } else {  
  [3]  DivideBarrett(Q, R, A, B, I, scratch);  
    if (should_terminate()) return;  
    RightShift(R, R, b_normalized.shift());  
  }  
}  

```

when generating `ShiftedDigits`, the A's length will increase when `shift > leading_zeros`, it does not match the memory previously allocted.

```
  explicit ShiftedDigits(Digits& original, int shift = -1,  
                         bool allow_inplace = false)  
      : Digits(original.digits_, original.len_) {  
    int leading_zeros = CountLeadingZeros(original.msd());  
    if (shift < 0) {  
      shift = leading_zeros;  
    } else if (shift > leading_zeros) {  
      allow_inplace = false;  
 [\*]     len_++;  
    }  
    shift_ = shift;  
    if (shift == 0) {  
      inplace_ = true;  
      return;  
    }  
    inplace_ = allow_inplace;  
    if (!inplace_) {  
      digit_t\* digits = new digit_t[len_];  
      storage_.reset(digits);  
      digits_ = digits;  
    }  
    RWDigits rw_view(digits_, len_);  
    LeftShift(rw_view, original, shift_);  
  }  

```

It will fail at DCHECK[1] for 'Q.len() == A.len() - B.len()' in `ProcessorImpl::DivideBarrett`. It will modify the Q's length as `I.len() + 1`, meaning that the value of len\_ is greater than the momory allocted at `MutableBigInt::New`. when calling `Add`[3] or `Multiply`[4], there will be an oob memory access.

```
void ProcessorImpl::DivideBarrett(RWDigits Q, RWDigits R, Digits A, Digits B,  
                                  Digits I, RWDigits scratch) {  
 [1] DCHECK(Q.len() > A.len() - B.len());  
  DCHECK(R.len() >= B.len());  
  DCHECK(A.len() > B.len());  // Careful: This is \*not\* '>=' !  
  DCHECK(A.len() <= 2 \* B.len());  
  DCHECK(B.len() > 0);  // NOLINT(readability/check)  
  DCHECK(IsBitNormalized(B));  
  DCHECK(I.len() == A.len() - B.len());  
  DCHECK(scratch.len() >= DivideBarrettScratchSpace(A.len()));  
  
  int orig_q_len = Q.len();  
  
  // (1): A1 = A with B.len fewer digits.  
  Digits A1 = A + B.len();  
  DCHECK(A1.len() == I.len());  
  
  // (2): Q = A1\*I with I.len fewer digits.  
  // {I} has an implicit high digit with value 1, so we add {A1} to the high  
  // part of the multiplication result.  
  RWDigits K(scratch, 0, 2 \* I.len());  
  Multiply(K, A1, I);  
  if (should_terminate()) return;  
  [2]Q.set_len(I.len() + 1);  
  [3]Add(Q, K + I.len(), A1);  
  // K is no longer used, can re-use {scratch} for P.  
  
  // (3): R = A - B\*Q (approximate remainder).  
  RWDigits P(scratch, 0, A.len() + 1);  
  [4]Multiply(P, B, Q);  
  if (should_terminate()) return;  
  digit_t borrow = SubtractAndReturnBorrow(R, A, Digits(P, 0, B.len()));  
  // R may be allocated wider than B, zero out any extra digits if so.  
  for (int i = B.len(); i < R.len(); i++) R[i] = 0;  
  digit_t r_high = A[B.len()] - P[B.len()] - borrow;  
  
  // Adjust R and Q so that they become the correct remainder and quotient.  
  // The number of iterations is guaranteed to be at most some very small  
  // constant, unless the caller gave us a bad approximate quotient.  
  if (r_high >> (kDigitBits - 1) == 1) {  
    // (5b): R < 0, so R += B  
    digit_t q_sub = 0;  
    do {  
      r_high += AddAndReturnCarry(R, R, B);  
      q_sub++;  
      DCHECK(q_sub <= 5);  // NOLINT(readability/check)  
    } while (r_high != 0);  
    Subtract(Q, q_sub);  
  } else {  
    digit_t q_add = 0;  
    while (r_high != 0 || GreaterThanOrEqual(R, B)) {  
      // (5c): R >= B, so R -= B  
      r_high -= SubtractAndReturnBorrow(R, R, B);  
      q_add++;  
      DCHECK(q_add <= 5);  // NOLINT(readability/check)  
    }  
    Add(Q, q_add);  
  }  
  // (5a): Return.  
  int final_q_len = Q.len();  
  Q.set_len(orig_q_len);  
  for (int i = final_q_len; i < orig_q_len; i++) Q[i] = 0;  
}  

```

**VERSION**  

v8 Version: commit ec7171608b49e16ba7231d298af3f08ac55163d3  

Operating System: Ubuntu 16.04

**REPRODUCTION CASE**  

run the attach file in DEBUG version of v8, it will crash at DECHECK:  

// ../../src/bigint/div-barrett.cc:229: Assertion failed: Q.len() > A.len() - B.len()  

// Received signal 6  

// ==== C stack trace ===============================  

// [0x55c51532d910]  

// [0x7fa2832a33c0]  

// [0x7fa282f6d18b]  

// [0x7fa282f4c859]  

// [0x55c5167ca47b]  

// [0x55c5167cabba]  

// [0x55c5167be529]  

// [0x55c5167bee08]  

// [0x55c515aa63e5]  

// [0x55c5160bac7a]  

// [0x09a80008f178]  

// [end of stack trace]

## Attachments

- [test.js](attachments/test.js) (text/plain, 78 B)

## Timeline

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### va...@google.com (2021-07-27)

PTAL

[Monorail components: Blink>JavaScript>Compiler]

### ne...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript>Compiler]

### cl...@chromium.org (2021-07-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5211543057530880.

### cl...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### p4...@gmail.com (2021-07-27)

Addition, In release version, it can oob write at V8 heap memory, because RWDigits Q points to a v8::bigint's Digits.
```c++
bigint::RWDigits GetRWDigits(MutableBigInt bigint) {
  return bigint::RWDigits(
      reinterpret_cast<bigint::digit_t*>(
          bigint.ptr() + BigIntBase::kDigitsOffset - kHeapObjectTag),
      bigint.length());
}
```




### cl...@chromium.org (2021-07-27)

Detailed Report: https://clusterfuzz.com/testcase?key=5211543057530880

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  Q.len() > A.len() - B.len()
  v8::bigint::ProcessorImpl::DivideBarrett
  v8::bigint::ProcessorImpl::Divide
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=75742:75743

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5211543057530880

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5211543057530880 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### jk...@chromium.org (2021-07-27)

Good catch!

This is unexpected because `bigint::DivideResultLength` explicitly avoids this problem by allocating an extra digit when Barrett division will be used. The problem is that this logic (along with the rest of Barrett division) requires V8_ADVANCED_BIGINT_ALGORITHMS to be defined, and while we set that preprocessor define for src/bigint/*, we forgot to pass it to src/objects/bigint.cc, which includes bigint.h with the `DivideResultLength` definition.

Fix coming up: https://chromium-review.googlesource.com/c/v8/v8/+/3056452

### gi...@appspot.gserviceaccount.com (2021-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8c057f17366669abf025d9d033e9390d99af85fd

commit 8c057f17366669abf025d9d033e9390d99af85fd
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Tue Jul 27 14:33:16 2021

[bigint] Define V8_ADVANCED_BIGINT_ALGORITHMS everywhere

It was previously only passed to compilation units in src/bigint/,
but inconsistencies arise when it's not passed to other compilation
units that #include src/bigint/bigint.h.

Fixed: chromium:1233397
Change-Id: Idb310d8c13bad12766699086574aa2c3869eb56c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3056452
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/master@{#75941}

[modify] https://crrev.com/8c057f17366669abf025d9d033e9390d99af85fd/BUILD.gn
[modify] https://crrev.com/8c057f17366669abf025d9d033e9390d99af85fd/src/bigint/bigint-internal.cc
[modify] https://crrev.com/8c057f17366669abf025d9d033e9390d99af85fd/src/bigint/bigint.h
[modify] https://crrev.com/8c057f17366669abf025d9d033e9390d99af85fd/test/bigint/BUILD.gn
[add] https://crrev.com/8c057f17366669abf025d9d033e9390d99af85fd/test/mjsunit/harmony/bigint/div-special-cases.js


### [Deleted User] (2021-07-27)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2021-07-27)

ClusterFuzz testcase 5211543057530880 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=75940:75941

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-27)

[Empty comment from Monorail migration]

### jk...@chromium.org (2021-07-27)

#10: My best guess for severity is Medium: it's an OOB write by one word. I can't rule out that it could be used as a stepping stone to getting a full r/w gadget for the renderer's memory, but I don't see an obvious way how to do that either.
No merges required, as M93 is definitely not affected.

### p4...@gmail.com (2021-07-28)

[Comment Deleted]

### [Deleted User] (2021-07-28)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### p4...@gmail.com (2021-07-30)

[Comment Deleted]

### jk...@chromium.org (2021-08-02)

#18: Maybe, I haven't tried it. I agree that 8 bytes is two compressed fields. Since you can't specifically write only one of these fields (only overwrite both at once), you may need to find some additional bug that lets you read a valid Map pointer to write into the first of those two fields (when the second is a length value you want to modify), unless you find a code path that reads that modified length without first reading the Map preceding it. An additional challenge is that the BigInt in question is allocated and then written into (including the OOB write) immediately afterwards, without any user code getting executed in between; so if you wanted that OOB write to affect another object, you'd have to find a way to make the BigInt allocation pick a memory location right before a previously-existing object (and I'm not sure if that's feasible, especially in new-space).

So I don't really have anything to add to my https://crbug.com/chromium/1233397#c14: "I can't rule out that this bug could be used as a stepping stone, but I don't see an obvious way". Which doesn't mean that there isn't a way I'm not seeing.

### p4...@gmail.com (2021-08-03)

Thank you for shareing your views. 

It's indeed a challenge since no chance to execute user js code between allocation and oob write, maybe can Take advantage of the fromSpace and toSpace feature in new-space, but it needs some effort to research that.  I understand your conclusion.

### am...@google.com (2021-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-04)

Congratulations - the VRP Panel has decided to award you $15,000 for this report of this V8 memory corruption issue! Nice work! 

### am...@google.com (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-14)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M94. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-15)

Your change meets the bar and is auto-approved for M94. Please go ahead and merge the CL to branch 4606 (refs/branch-heads/4606) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jk...@chromium.org (2021-08-15)

#24/#25: Go home, sheriffbot, you're drunk. The fix has landed long before the M94 branch point, and M93 is not affected. There are no merges required here.

### [Deleted User] (2021-11-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1233397?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056682)*
