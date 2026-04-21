# Optimization bug in TurboShaft::MachineOptimizationReducer::ReduceSignedDiv

| Field | Value |
|-------|-------|
| **Issue ID** | [40061881](https://issues.chromium.org/issues/40061881) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Linux |
| **Reporter** | kw...@gmail.com |
| **Assignee** | te...@google.com |
| **Created** | 2022-11-23 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

Run the poc.js with the release build of the v8-11.0.67.  

Command: `./d8 --allow-natives-syntax --future ./poc.js`

```
// poc.js  
function opt() {  
  const v11 = BigInt.asUintN(16, 2n);  
  const v12 = -1n / v11;  
  return v12;  
}  
let jit_a0 = opt();  
% PrepareFunctionForOptimization(opt);  
opt();  
% OptimizeFunctionOnNextCall(opt)  
let jit_a2 = opt();  
console.log(jit_a0);  
console.log(jit_a2);  
  
**Problem Description:**   
By running the poc.js, we can observe the below difference:  
0  
-1  
  
I found out that this bug occurs because of the wrong optimization at ReduceSignedDiv @ src/compiler/turboshaft/machine-optimization-reducer.h:  
  
 if (base::bits::IsPowerOfTwo(right)) {  
      uint32_t shift = base::bits::WhichPowerOfTwo(right);  
      DCHECK_GT(shift, 0);  
      if (shift > 1) {  
        quotient =  
            Asm().ShiftRightArithmetic(quotient, rep.bit_width() - 1, rep);  
      }  
      quotient =  
          Asm().ShiftRightArithmetic(quotient, rep.bit_width() - shift, rep); // <= should be ShiftRightLogical  
      quotient = Asm().WordAdd(quotient, left, rep);  
      quotient = Asm().ShiftRightArithmetic(quotient, shift, rep);  
      return quotient;  
    }  
  
TurboShaft optimizes the signed division with the arithmetic right shift if the `right` is a power of two.  
However, this optimization goes wrong because of the first 'ShiftRightArithmetic' operation.   
I think It should be ShiftRightLogical.  
  
**Additional Comments:**   
  
  
**Chrome version: **  **Channel: ** Not sure  
  
**OS:** Linux

```

## Timeline

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-11-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler]

### sr...@google.com (2022-11-24)

This bisects to 0c177366ddda31b0f132b575c50686c6fdc36c28.
Not sure if it's a duplicate of 1392928 or a separate bug.

### pa...@google.com (2022-11-24)

It is a separate bug.

### gi...@appspot.gserviceaccount.com (2022-11-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/0d04ebd575c8ea87309c913e75217b9f68f37991

commit 0d04ebd575c8ea87309c913e75217b9f68f37991
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Thu Nov 24 15:39:02 2022

[turboshaft] fix signed div with power of 2

Bug: chromium:1392953
Change-Id: I392d5e0b12d840e08cd4f97b092a74208b30ac9b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4055862
Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
Auto-Submit: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84467}

[modify] https://crrev.com/0d04ebd575c8ea87309c913e75217b9f68f37991/src/compiler/turboshaft/machine-optimization-reducer.h


### te...@chromium.org (2022-11-24)

[Empty comment from Monorail migration]

### te...@chromium.org (2022-11-24)

Thanks a lot for this report!

### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### kw...@gmail.com (2022-11-24)

Glad it helped!

### [Deleted User] (2022-11-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### kw...@gmail.com (2022-12-02)

Thanks a lot!

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-02)

This issue was migrated from crbug.com/chromium/1392953?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061881)*
