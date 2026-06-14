# Size calculation overflow can lead to heap buffer overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40094038](https://issues.chromium.org/issues/40094038) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2019-02-14 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36

Steps to reproduce the problem:
poc:
new BigInt64Array(1073741823);

What is the expected behavior?

What went wrong?
abort: CSA_ASSERT failed: Torque assert 'byteLength >>> this.sizeLog2 == length' failed [../../src/builtins/typed-array.tq:13]

==== JS stack trace =========================================

    0: ExitFrame [pc: 0xf6fedc70]
    1: StubFrame [pc: 0xf70ca3a9]
Security context: 0x5430d705 <JSObject>#0#
    2: new BigInt64Array(aka BigInt64Array) [0x54307659](this=0x51f80305 <the_hole>,1073741823)
    3: ConstructFrame [pc: 0xf6cd7b50]
    4: StubFrame [pc: 0xf714e298]
    5: /* anonymous */ [0x5430fe29] [(d8):1] [bytecode=0x5430fddd offset=16](this=0x51680bbd <JSGlobal Object>#1#)
    6: InternalFrame [pc: 0xf6ce0801]
    7: EntryFrame [pc: 0xf6ce05c9]

==== Details ================================================

[0]: ExitFrame [pc: 0xf6fedc70]
[1]: StubFrame [pc: 0xf70ca3a9]
[2]: new BigInt64Array(aka BigInt64Array) [0x54307659](this=0x51f80305 <the_hole>,1073741823) {
// optimized frame
--------- s o u r c e   c o d e ---------
<No Source>
-----------------------------------------
}
[3]: ConstructFrame [pc: 0xf6cd7b50]
[4]: StubFrame [pc: 0xf714e298]
[5]: /* anonymous */ [0x5430fe29] [(d8):1] [bytecode=0x5430fddd offset=16](this=0x51680bbd <JSGlobal Object>#1#) {
  // expression stack (top to bottom)
  [02] : 1073741823
  [01] : 0x54307659 <JSFunction BigInt64Array (sfi = 0x26b0ad19)>#2#
  [00] : 0x51f80289 <undefined>
--------- s o u r c e   c o d e ---------
new BigInt64Array(1073741823)
-----------------------------------------
}

[6]: InternalFrame [pc: 0xf6ce0801]
[7]: EntryFrame [pc: 0xf6ce05c9]
==== Key         ============================================

 #0# 0x5430d705: 0x5430d705 <JSObject>
 #1# 0x51680bbd: 0x51680bbd <JSGlobal Object>
 #2# 0x54307659: 0x54307659 <JSFunction BigInt64Array (sfi = 0x26b0ad19)>
 BYTES_PER_ELEMENT: 8
=====================

Received signal 4 ILL_ILLOPN 0000f4a5a781

==== C stack trace ===============================

 [0x0000f4a5d451]
 [0x0000f4a5d356]
 [0x0000f77d3bd0]
 [0x0000f4a5a781]
 [0x0000f67d2626]
 [0x0000f67d20f2]
 [0x0000f6fedc70]
 [0x0000f70ca3a9]
 [0x0000f6f986d8]
 [0x0000f6cd7b50]
 [0x0000f714e298]
 [0x0000f6ce92a0]
 [0x0000f6ce0801]
 [0x0000f6ce05c9]
 [0x0000f5f83ad2]
 [0x0000f5f80b6f]
 [0x0000f5f7ff51]
 [0x0000f56119c6]
 [0x0000565f3248]
 [0x000056602107]
 [0x000056606af6]
 [0x000056606f2c]
 [0x0000f464e637]
[end of stack trace]

Did this work before? N/A 

Chrome version: 73.0.3679.0  Channel: n/a
OS Version: 10.0
Flash Version:

## Attachments

- [Screen Shot 2019-02-18 at 11.10.41 AM.png](attachments/Screen Shot 2019-02-18 at 11.10.41 AM.png) (image/png, 641.1 KB)
- [expd8.js](attachments/expd8.js) (text/plain, 5.4 KB)
- [exploit.png](attachments/exploit.png) (image/png, 98.5 KB)
- [leak.png](attachments/leak.png) (image/png, 19.7 KB)

## Timeline

### me...@google.com (2019-02-14)

jgruber: Can you please take a look? Does this crash have any security implications?

[Monorail components: Blink>JavaScript]

### jg...@chromium.org (2019-02-18)

Peter W ptal, the failing assert was added in 

commit c9ef0405c786c86f5ad9755b9b3573d2a43d9757
Author: peterwmwong <peter.wm.wong@gmail.com>
Reviewed-on: https://chromium-review.googlesource.com/c/1456299

Let's revert & reland with a fix.

### jg...@chromium.org (2019-02-18)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ced2e4eec541b04908ea73755e9129ea2167fea4

commit ced2e4eec541b04908ea73755e9129ea2167fea4
Author: Jakob Gruber <jgruber@chromium.org>
Date: Mon Feb 18 08:57:43 2019

Revert "[builtins]: Optimize CreateTypedArray to use element size log 2 for calculations."

This reverts commit c9ef0405c786c86f5ad9755b9b3573d2a43d9757.

Reason for revert: https://crbug.com/932034

Original change's description:
> [builtins]: Optimize CreateTypedArray to use element size log 2 for calculations.
>
> TypedArrayElementsInfo now represents an element's size as a log 2 and typed as
> uintptr.  This simplifies and speeds up (avoids possible HeapNumber allocations) a
> number of calculations:
>
>   - Number of Elements (length) -> Byte Length - is now a WordShl
>   - Byte Length -> Number of Elements (length) - is now a WordShr
>   - Testing alignment (byte offset or length)  - is now a WordAnd
>
> These element/byte length related calculations are encapsulated in
> TypedArrayElementsInfo as struct methods.
>
> This reduces the size of CreateTypedArray by 2.125 KB (24%) on Mac x64.release:
>   - Before: 9,088
>   - After:  6,896
>
> This improves the performance of the following microbencmarks
>   - TypedArrays-ConstructWithBuffer: ~87%
>   - TypedArrays-SubarrayNoSpecies:   ~28%
>
> Bug: v8:7161
> Change-Id: I2239fd0e0af9d3ad55cd52318088d3c7c913ae44
> Reviewed-on: https://chromium-review.googlesource.com/c/1456299
> Commit-Queue: Peter Wong <peter.wm.wong@gmail.com>
> Reviewed-by: Jakob Gruber <jgruber@chromium.org>
> Reviewed-by: Simon Zünd <szuend@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#59531}

TBR=peter.wm.wong@gmail.com,jgruber@chromium.org,petermarshall@chromium.org,szuend@chromium.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: v8:7161, chromium:932034
Change-Id: I3da95447ce34f84d01629d2791868f3adcdfb387
Reviewed-on: https://chromium-review.googlesource.com/c/1475764
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#59645}
[modify] https://crrev.com/ced2e4eec541b04908ea73755e9129ea2167fea4/src/builtins/base.tq
[modify] https://crrev.com/ced2e4eec541b04908ea73755e9129ea2167fea4/src/builtins/builtins-typed-array-gen.cc
[modify] https://crrev.com/ced2e4eec541b04908ea73755e9129ea2167fea4/src/builtins/builtins-typed-array-gen.h
[modify] https://crrev.com/ced2e4eec541b04908ea73755e9129ea2167fea4/src/builtins/typed-array-createtypedarray.tq
[modify] https://crrev.com/ced2e4eec541b04908ea73755e9129ea2167fea4/src/builtins/typed-array.tq
[modify] https://crrev.com/ced2e4eec541b04908ea73755e9129ea2167fea4/src/code-stub-assembler.cc
[modify] https://crrev.com/ced2e4eec541b04908ea73755e9129ea2167fea4/src/code-stub-assembler.h
[modify] https://crrev.com/ced2e4eec541b04908ea73755e9129ea2167fea4/src/external-reference.cc
[modify] https://crrev.com/ced2e4eec541b04908ea73755e9129ea2167fea4/src/external-reference.h


### pe...@gmail.com (2019-02-18)

Jakob/meacer, I'm a bit a confused by this.

1) The reported version is "73.0.3679.0", but the size log 2 optimization (merged 6 days ago) didn't/shouldn't have made it into the V8 7.3 release branch.

2) I'm unable to reproduce the CSA_ASSERT crash in Dev (74) or Beta (73).  I get the expected "Uncaught RangeError: Array buffer allocation failed".  I double checked with WIndows 10 and Chrome Beta 73 on SauceLabs and also couldn't reproduce (see screenshot).



### hi...@gmail.com (2019-02-19)

[Comment Deleted]

### hi...@gmail.com (2019-02-19)

Sorry , the UserAgent is wrong 

### pa...@chromium.org (2019-02-19)

This bug does/would apply to all platforms with V8.

I'm not sure I see any security implications. Allocation failure with a throw (in Release builds; maybe asserts in Debug) is expected, good behavior in this case, right?

Any objections to me taking this out of the security queue?

### jg...@chromium.org (2019-02-20)

Ah sorry, just realized I didn't answer the q in #1. I think there may be security implications: the (debug) assert was guarding an overflow in when calculating the byte length of the typed array backing store. I can imagine a scenario where we overflow, allocate a typed array backing store that is too small, and later access OOB. 

I didn't verify in detail whether this is possible though. Peter, do you know more?

### pe...@gmail.com (2019-02-20)

Jakob,

Yes, that scenario (overflow causes a smaller backing and OOB access later) is possible given the right length passed to TypedArray constructor.


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24

commit 02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24
Author: peterwmwong <peter.wm.wong@gmail.com>
Date: Wed Feb 20 12:06:53 2019

Reland "[builtins]: Optimize CreateTypedArray to use element size log 2 for calculations."

This is a reland of c9ef0405c786c86f5ad9755b9b3573d2a43d9757

Original change's description:
> [builtins]: Optimize CreateTypedArray to use element size log 2 for calculations.
>
> TypedArrayElementsInfo now represents an element's size as a log 2 and typed as
> uintptr.  This simplifies and speeds up (avoids possible HeapNumber allocations) a
> number of calculations:
>
>   - Number of Elements (length) -> Byte Length - is now a WordShl
>   - Byte Length -> Number of Elements (length) - is now a WordShr
>   - Testing alignment (byte offset or length)  - is now a WordAnd
>
> These element/byte length related calculations are encapsulated in
> TypedArrayElementsInfo as struct methods.
>
> This reduces the size of CreateTypedArray by 2.125 KB (24%) on Mac x64.release:
>   - Before: 9,088
>   - After:  6,896
>
> This improves the performance of the following microbencmarks
>   - TypedArrays-ConstructWithBuffer: ~87%
>   - TypedArrays-SubarrayNoSpecies:   ~28%
>
> Bug: v8:7161
> Change-Id: I2239fd0e0af9d3ad55cd52318088d3c7c913ae44
> Reviewed-on: https://chromium-review.googlesource.com/c/1456299
> Commit-Queue: Peter Wong <peter.wm.wong@gmail.com>
> Reviewed-by: Jakob Gruber <jgruber@chromium.org>
> Reviewed-by: Simon Zünd <szuend@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#59531}

Bug: v8:7161, chromium:932034
Change-Id: I5c3dc34c549234417f95b404e7d49b2fd496fa69
Reviewed-on: https://chromium-review.googlesource.com/c/1476306
Commit-Queue: Peter Wong <peter.wm.wong@gmail.com>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Simon Zünd <szuend@chromium.org>
Cr-Commit-Position: refs/heads/master@{#59728}
[modify] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/src/builtins/base.tq
[modify] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/src/builtins/builtins-typed-array-gen.cc
[modify] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/src/builtins/builtins-typed-array-gen.h
[modify] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/src/builtins/typed-array-createtypedarray.tq
[modify] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/src/builtins/typed-array.tq
[modify] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/src/code-stub-assembler.cc
[modify] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/src/code-stub-assembler.h
[modify] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/src/external-reference.cc
[modify] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/src/external-reference.h
[add] https://crrev.com/02b9847f4e09c1765ba6d4b71b7ce75f19bf7d24/test/mjsunit/regress/regress-crbug-932034.js


### pe...@chromium.org (2019-02-20)

re #9: Yes I think it's a security issue, I agree with Peter W in #10.

### hi...@gmail.com (2019-02-20)

[Comment Deleted]

### hi...@gmail.com (2019-02-20)

Yes, this is a security issue, Please focus on my another https://crbug.com/chromium/933664.
An out-of-bounds read and write can be caused.

### pa...@chromium.org (2019-02-20)

Ahh, thank you.

### pe...@gmail.com (2019-02-20)

Just to be clear, this does not apply to 73.
As clarified in https://crbug.com/chromium/932034#c7, the original reported UA version was incorrect.

### va...@chromium.org (2019-02-21)

So per #16, can this be marked as fixed then?

### va...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### jg...@chromium.org (2019-02-21)

Yes, fixed as of the revert in #11.

### sh...@chromium.org (2019-02-21)

[Empty comment from Monorail migration]

### hi...@gmail.com (2019-02-22)

an exploit for d8 ia32.release is attatched

### hi...@gmail.com (2019-02-25)

Can I get a reward with this?   awhalley@google.com@

### na...@google.com (2019-02-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-28)

Congrats! The Panel decided to reward $5,000 for this report :) 

### hi...@gmail.com (2019-03-03)

thanks (^-^)

### aw...@google.com (2019-03-04)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-05-30)

This issue was migrated from crbug.com/chromium/932034?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094038)*
