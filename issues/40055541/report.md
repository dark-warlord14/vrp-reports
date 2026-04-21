# Security: Range miscalculation for nodes of type SpeculativeSafeIntegerAdd in v8's TurboFan

| Field | Value |
|-------|-------|
| **Issue ID** | [40055541](https://issues.chromium.org/issues/40055541) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2021-04-13 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

In the TruboFan compiler of v8, a range miscalculation bug in the typer can be triggered due to an off-by-one involving type bounds of "kAdditiveSafeInteger".  

This can be used to crash v8 (via triggering a Throw-node) - and thus the browser tab of Chrome - , however due to the specifics of the bug I am not certain whether it can be leveraged into an out-of-bounds access or a fake object construction.

In v8's TurboFan compiler, during the type-hint lowering step, an addition with type hint "kSignedSmall" or "kSigned32" will be compiled to a "SpeculativeSafeIntegerAdd" node (see SpeculativeNumberOp() in v8/src/compiler/js-type-hint-lowering.cc). (Everything stated here simliarly applies to subtraction, which will generate a "SpeculativeSafeIntegerSubtract" node.)

During the typer stage, the `SpeculativeSafeIntegerAdd` node is typed to `kSafeIntegerOrMinusZero` (in v8/src/compiler/operation-typer.cc):  

Type OperationTyper::SpeculativeSafeIntegerAdd(Type lhs, Type rhs) {  

Type result = SpeculativeNumberAdd(lhs, rhs);  

// If we have a Smi or Int32 feedback, the representation selection will  

// either truncate or it will check the inputs (i.e., deopt if not int32).  

// In either case the result will be in the safe integer range, so we  

// can bake in the type here. This needs to be in sync with  

// SimplifiedLowering::VisitSpeculativeAdditiveOp.  

return Type::Intersect(result, cache\_->kSafeIntegerOrMinusZero, zone());  

}

During the simplified lowering stage, the node will be handled by `VisitSpeculativeIntegerAdditiveOp` (in v8/src/compiler/simplified-lowering.cc):

void VisitSpeculativeIntegerAdditiveOp(Node\* node, Truncation truncation,  

SimplifiedLowering\* lowering) {  

Type left\_upper = GetUpperBound(node->InputAt(0));  

Type right\_upper = GetUpperBound(node->InputAt(1));

```
if (left_upper.Is(type_cache_->kAdditiveSafeIntegerOrMinusZero) &&  
    right_upper.Is(type_cache_->kAdditiveSafeIntegerOrMinusZero)) {  
  // Only eliminate the node if its typing rule can be satisfied, namely  
  // that a safe integer is produced.  
  if (truncation.IsUnused()) return VisitUnused<T>(node);  

  // If we know how to interpret the result or if the users only care  
  // about the low 32-bits, we can truncate to Word32 do a wrapping  
  // addition.  
  if (GetUpperBound(node).Is(Type::Signed32()) ||  
      GetUpperBound(node).Is(Type::Unsigned32()) ||  
      truncation.IsUsedAsWord32()) {  
    // => Int32Add/Sub  
    VisitWord32TruncatingBinop<T>(node);  
    if (lower<T>()) ChangeToPureOp(node, Int32Op(node));  
    return;  
  }  
}  
...  

```

}

In particular, the node is changed to a pure (unchecked) Int32-addition, if both of the following conditions are met:

- Both inputs are guaranteed to be in the `kAdditiveSafeIntegerOrMinusZero` type
- Either the output is guaranteed to be in the (Un)Signed32 type, or the output's truncation type is set to Word32 (when the output is only ever used after truncating it to an Int32)

However, the type kAdditiveSafeIntegerOrMinusZero is defined as follows (in v8/src/compiler/type-cache.h):  

Type const kAdditiveSafeInteger =  

CreateRange(-4503599627370496.0, 4503599627370496.0);  

Type const kAdditiveSafeIntegerOrMinusZero =  

Type::Union(kAdditiveSafeInteger, Type::MinusZero(), zone());  

While kSafeInteger is defined as `CreateRange(-kMaxSafeInteger, kMaxSafeInteger)` where `kMaxSafeInteger` equals 9007199254740991.  

Note that 4503599627370496+4503599627370496 equals 9007199254740992, which exceeds the kSafeInteger type; so if both inputs equal 4503599627370496 (or both -4503599627370496), the output's type constraint is violated.

To trigger the bug, the following conditions need to be met:

1. We need an integer addition with type hint kSignedSmall or kSigned32
2. The input types need to be constrained to kAdditiveSafeIntegerOrMinusZero
3. The output needs to be truncated to a 32-bit word  
   
   The first condition guarantees that a `SpeculativeSafeIntegerAdd` is generated, while conditions 2 and 3 guarantee the conversion to an unconditional Int32Add (we can not allow the operation to be converted to a checked Int32 addition, as this would result in a deoptimization as soon as the inputs actually are 4503599627370496).  
   
   This results in a `SpeculativeSafeIntegerAdd` node that is typed to output a maximum of 9007199254740991, but that still accepts both inputs to be 4503599627370496.

To trigger the bug in a potentially more useful way, we want to have a (true) lower bound on the output as well that is not much lower than 9007199254740991.  

This at first seems contradictory to condition 1, as we need an addition that is assigned a small type hint, but which is actually guaranteed a lower bound much higher than 2^32 = 4294967296.  

However, this goal can be accomplished using inlining: We can first "train" one method, which contains an addition (as well as the necessary code to guarantee its inputs to have type kAdditiveSafeIntegerOrMinusZero, and a bitwise operation which forces the addition's truncation type to Word32) using small operands; and then, after it has been compiled by TurboFan, call this method from a second method with parameters now constrained to be nearly 4503599627370496.  

This will let the `SpeculativeSafeIntegerAdd` node (that has already been generated) be inlined into the second function, where the new bounds are propagated during the typer stage.

In particular, if the second method constrains its operands to just `Range(4503599627370496, 4503599627370496)`, this will result in a crash: The typer phase will simultaneously reason the result to be at least 2\*4503599627370496=9007199254740992, but also at most 9007199254740991, resulting in the type to be reduced to the `None` type.  

During Dead Code Elimination, this node will be marked as Unreachable, resulting in a `Throw` node.

Even though this range miscalculation is a violation of potentially security-relevant assumptions, I did not manage to exploit it further.  

While the primitive can be used to construct a node of type `Range(a, 9007199254740991)` with an arbitrary `a` that in reality contains the value `9007199254740992`, recall that one of the conditions it that the node's truncation type is Word32.  

However, all operations (that I could find) that intrinsically truncate to Word32 use typing logic similar to the following from `v8/src/compiler/operation-typer.cc`:

Type OperationTyper::NumberToInt32(Type type) {  

DCHECK(type.Is(Type::Number()));

```
if (type.Is(Type::Signed32())) return type;  
if (type.Is(cache_->kZeroish)) return cache_->kSingletonZero;  
if (type.Is(signed32ish_)) {  
  return Type::Intersect(Type::Union(type, cache_->kSingletonZero, zone()),  
                       Type::Signed32(), zone());  
}  
return Type::Signed32();  

```

}

While those operations could use information from a range with both bounds being 32-bit values, they cannot infer from an input range of the form `Range(a\*2^32+b,a\*2^32+c)` with `0<=b<c<2^32` and `a>0` that the output will be in `Range(b,c)` - instead they simply set the output to an unconstrained `Signed32` (or `Unsigned32`) type.

Also, we cannot subtract any fixed value to "shift" the range inside the 32-bit range; recall that one of the conditions for the generation of an (unchecked) Int32 addition is that both inputs are in the `kAdditiveSafeIntegerOrMinusZero` type - this clearly can not be the case for our range, which always contains `9007199254740991` (if it isn't empty); thus any following addition or subtraction won't propagate the Word32-truncation to the output of our original addition.

**VERSION**

The crash has been tested on a debug build of the current master branch of v8 (as of 2020-04-13), as well as in browser version Chromium 89.0.4389.114 on Arch Linux.

**REPRODUCTION CASE**

A proof of concept that crashes v8 is attached as `bug.js` (run as `d8 bug.js --allow-natives-syntax`), a version that crashes the chromium tab is attached as `bug.html`.

**CREDIT INFORMATION**

Reporter credit: Manfred Paul

## Attachments

- [bug.js](attachments/bug.js) (text/plain, 1.0 KB)
- [bug.html](attachments/bug.html) (text/plain, 448 B)

## Timeline

### [Deleted User] (2021-04-13)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-04-15)

mvstanton/neis, PTAL?

[Monorail components: Blink>JavaScript>Compiler]

### ne...@google.com (2021-04-15)

Great find and report, thank you!

### ne...@google.com (2021-04-15)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-19)

I agree with the analysis that it seems impossible to exploit this, but I wouldn't bet my life on it. I'm keeping it as a Bug-Security and setting Medium severity ("not harmful on their own but potentially harmful when combined with other bugs"). +adetaylor, please let me know if this classification seems off.

### gi...@appspot.gserviceaccount.com (2021-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/798fbcb0a3e5a292fb775c37c19d9fe73bbac17c

commit 798fbcb0a3e5a292fb775c37c19d9fe73bbac17c
Author: Georg Neis <neis@chromium.org>
Date: Mon Apr 19 11:12:46 2021

[compiler] Fix off-by-one error in kAdditiveSafeInteger

Bug: chromium:1198705
Change-Id: I6b3ad82754e1ca72701ce57f16c4f085f8c87f77
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2835705
Auto-Submit: Georg Neis <neis@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/master@{#74033}

[modify] https://crrev.com/798fbcb0a3e5a292fb775c37c19d9fe73bbac17c/src/compiler/type-cache.h


### ne...@chromium.org (2021-04-19)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-04-19)

neis@ thanks, that sounds like a good compromise.

### [Deleted User] (2021-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-19)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-19)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M90. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to future beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M91. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-19)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-04-19)

Approving merge to M91. Please wait for this to have 24 hours in Canary first.

### ad...@google.com (2021-04-20)

Approving merge to M90 as well.

### sr...@google.com (2021-04-20)

Please complete your merges before thursday EOD PST, so these security fixes can go out in next M90 respin

### gi...@appspot.gserviceaccount.com (2021-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/eecbaafdbe8dcd8aa49028fca049d4b27f0065df

commit eecbaafdbe8dcd8aa49028fca049d4b27f0065df
Author: Georg Neis <neis@chromium.org>
Date: Thu Apr 22 06:43:35 2021

Merged: [compiler] Fix off-by-one error in kAdditiveSafeInteger

Revision: 798fbcb0a3e5a292fb775c37c19d9fe73bbac17c

BUG=chromium:1198705
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
TBR=nicohartmann@chromium.org

Change-Id: I0f0c2e6e605fae6f0a840c03b9209714f23c7aa7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2844653
Reviewed-by: Georg Neis <neis@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.1@{#30}
Cr-Branched-From: 0e4ac64a8cf298b14034a22f9fe7b085d2cb238d-refs/heads/9.1.269@{#1}
Cr-Branched-From: f565e72d5ba88daae35a59d0f978643e2343e912-refs/heads/master@{#73847}

[modify] https://crrev.com/eecbaafdbe8dcd8aa49028fca049d4b27f0065df/src/compiler/type-cache.h


### gi...@appspot.gserviceaccount.com (2021-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/7c299aede5b26ef13c9404f265f30e7b4a2035e2

commit 7c299aede5b26ef13c9404f265f30e7b4a2035e2
Author: Georg Neis <neis@chromium.org>
Date: Thu Apr 22 06:50:06 2021

Merged: [compiler] Fix off-by-one error in kAdditiveSafeInteger

Revision: 798fbcb0a3e5a292fb775c37c19d9fe73bbac17c

BUG=chromium:1198705
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
TBR=nicohartmann@chromium.org

Change-Id: Ifc210e7932f43088e858f6bdac6d9bcdec6e63f5
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2844654
Reviewed-by: Georg Neis <neis@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.0@{#43}
Cr-Branched-From: bd0108b4c88e0d6f2350cb79b5f363fbd02f3eb7-refs/heads/9.0.257@{#1}
Cr-Branched-From: 349bcc6a075411f1a7ce2d866c3dfeefc2efa39d-refs/heads/master@{#73001}

[modify] https://crrev.com/7c299aede5b26ef13c9404f265f30e7b4a2035e2/src/compiler/type-cache.h


### ne...@chromium.org (2021-04-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-23)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-26)

[Empty comment from Monorail migration]

### gi...@google.com (2021-04-27)

[Empty comment from Monorail migration]

### as...@google.com (2021-04-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/00245033cf756f86cef7e830661810777aaf3476

commit 00245033cf756f86cef7e830661810777aaf3476
Author: Georg Neis <neis@chromium.org>
Date: Mon Apr 19 11:12:46 2021

M86-LTS: [compiler] Fix off-by-one error in kAdditiveSafeInteger

(cherry picked from commit 798fbcb0a3e5a292fb775c37c19d9fe73bbac17c)

No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Bug: chromium:1198705
Change-Id: I6b3ad82754e1ca72701ce57f16c4f085f8c87f77
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2835705
Auto-Submit: Georg Neis <neis@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#74033}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2850708
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/8.6@{#87}
Cr-Branched-From: a64aed2333abf49e494d2a5ce24bbd14fff19f60-refs/heads/8.6.395@{#1}
Cr-Branched-From: a626bc036236c9bf92ac7b87dc40c9e538b087e3-refs/heads/master@{#69472}

[modify] https://crrev.com/00245033cf756f86cef7e830661810777aaf3476/src/compiler/type-cache.h


### am...@google.com (2021-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-29)

Congratulations, Manfred! The VRP Panel has decided to award you $7500 for this report. A member of our finance team will be in touch soon to arrange payment. Nice work and thank you for your work in reporting this issue!  

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/928da8091fc9612a22f64015938f692a2bae8bb7

commit 928da8091fc9612a22f64015938f692a2bae8bb7
Author: Georg Neis <neis@chromium.org>
Date: Fri Jun 04 07:49:34 2021

[compiler] Add a few regression tests

Tbr: nicohartmann@chromium.org
Bug: chromium:1198705, chromium:1199345, chromium:1200490
Change-Id: I4a486df636e084279423e6cd3b867137bfe3fd6f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2939984
Reviewed-by: Georg Neis <neis@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#74945}

[add] https://crrev.com/928da8091fc9612a22f64015938f692a2bae8bb7/test/mjsunit/compiler/regress-1198705.js
[add] https://crrev.com/928da8091fc9612a22f64015938f692a2bae8bb7/test/mjsunit/compiler/regress-1199345.js
[add] https://crrev.com/928da8091fc9612a22f64015938f692a2bae8bb7/test/mjsunit/compiler/regress-1200490.js


### [Deleted User] (2021-08-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1198705?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055541)*
