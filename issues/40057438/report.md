# Primitive type confusion in ia32 AssembleCodePhase

| Field | Value |
|-------|-------|
| **Issue ID** | [40057438](https://issues.chromium.org/issues/40057438) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Linux, ChromeOS |
| **Reporter** | fz...@gmail.com |
| **Assignee** | ni...@chromium.org |
| **Created** | 2021-09-29 |
| **Bounty** | $7,500.00 |

## Description

redacted

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 911 B)

## Timeline

### [Deleted User] (2021-09-29)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-09-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler]

### cl...@chromium.org (2021-09-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5749979341455360.

### ve...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### ve...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### vi...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-09-30)

Setting some flags; talking with victor this sounds limited to ia32, which means I don't believe it affects Windows/Android, but happy to adjust there. This sounds like a High, in the context of ACE in the renderer. I'll work on repro'ing this further to set up FoundIn, although victor, feel free to set it if you've already root caused :)

### rs...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/b65e72c68eaf48640679dc1e7b379e81f999a8f1

commit b65e72c68eaf48640679dc1e7b379e81f999a8f1
Author: Victor Gomes <victorgomes@chromium.org>
Date: Thu Sep 30 17:22:31 2021

[TurboFan] Change representation of NumberConstant in 32-bit arch

Smi constants in 32 bit machines are guaranteed to be 31 bits.

Bug: chromium:1254189
Change-Id: I4ea296a7212c5e6ea14119fbd71cfb5789762b55
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3195874
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77185}

[modify] https://crrev.com/b65e72c68eaf48640679dc1e7b379e81f999a8f1/src/compiler/effect-control-linearizer.cc


### vi...@chromium.org (2021-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-01)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/131c0055c9a5e039185d19584b3c95edc3164bee

commit 131c0055c9a5e039185d19584b3c95edc3164bee
Author: Victor Gomes <victorgomes@chromium.org>
Date: Mon Oct 04 08:29:09 2021

Revert "[TurboFan] Change representation of NumberConstant in 32-bit arch"

This reverts commit b65e72c68eaf48640679dc1e7b379e81f999a8f1.

Reason for revert: CFs issues

Original change's description:
> [TurboFan] Change representation of NumberConstant in 32-bit arch
>
> Smi constants in 32 bit machines are guaranteed to be 31 bits.
>
> Bug: chromium:1254189
> Change-Id: I4ea296a7212c5e6ea14119fbd71cfb5789762b55
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3195874
> Commit-Queue: Victor Gomes <victorgomes@chromium.org>
> Reviewed-by: Maya Lekova <mslekova@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#77185}

Bug: chromium:1254189, chromium:1255213, chromium:1255330
Change-Id: Idd9a6e76a44612d1ab9aada0d8ee093b9aab34a0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3200079
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77210}

[modify] https://crrev.com/131c0055c9a5e039185d19584b3c95edc3164bee/src/compiler/effect-control-linearizer.cc


### vi...@chromium.org (2021-10-04)

I've got some CFs issues, so I reverted the fix and I am investigating it again.

### vi...@chromium.org (2021-10-04)

This is exploitable since M84.

### rs...@chromium.org (2021-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@google.com (2021-10-15)

any updates on this one?

### fz...@gmail.com (2021-10-15)

A suggested patch is attached as `patch.diff`.

### vi...@chromium.org (2021-10-19)

Nico, can you have a better look? This is outside of my comfort zone.

### gi...@appspot.gserviceaccount.com (2021-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/bdf31d5883607db4377b519d7308fb1e639a0448

commit bdf31d5883607db4377b519d7308fb1e639a0448
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Mon Oct 25 08:58:59 2021

[TurboFan] Do not use NumberConstant as immediate in x86

Bug: chromium:1254189
Change-Id: I77854c767cf5c5748999fdd40a4a42e25dff3f79
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3236989
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Reviewed-by: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77516}

[modify] https://crrev.com/bdf31d5883607db4377b519d7308fb1e639a0448/src/compiler/backend/ia32/instruction-selector-ia32.cc


### ni...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-08)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M94. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M95. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M96. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M97. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-08)

Merge approved: your change passed merge requirements and is auto-approved for M97. Please go ahead and merge the CL to branch 4692 (refs/branch-heads/4692) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-08)

Merge review required: M96 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-08)

Merge review required: M95 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-08)

Merge review required: M94 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-11-08)

approving merge to M96; once a more recent Canary verification has been completed (since this CL landed 14 days ago, but was marked fixed today) please go ahead and merge to the appropriate branch for M96 in the V8 repo. Please merge by EOD, Tuesday 9 November so this fix can be included in the M96 stable channel release next week. Thank you! 

no backmerge to M95 or M94 required; there are no more planned releases for 94/Extended or 95/Stable

### gi...@appspot.gserviceaccount.com (2021-11-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/5d2b5e7c006c8af13b2d467ce2a38877bad300dc

commit 5d2b5e7c006c8af13b2d467ce2a38877bad300dc
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Mon Oct 25 08:58:59 2021

Merged: [TurboFan] Do not use NumberConstant as immediate in x86

Bug: chromium:1254189
(cherry picked from commit bdf31d5883607db4377b519d7308fb1e639a0448)

Change-Id: I1d4426fee8392c7a680ad67af4bf2745d04b2e52
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3268905
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.6@{#22}
Cr-Branched-From: 0b7bda016178bf438f09b3c93da572ae3663a1f7-refs/heads/9.6.180@{#1}
Cr-Branched-From: 41a5a247d9430b953e38631e88d17790306f7a4c-refs/heads/main@{#77244}

[modify] https://crrev.com/5d2b5e7c006c8af13b2d467ce2a38877bad300dc/src/compiler/backend/ia32/instruction-selector-ia32.cc


### sr...@google.com (2021-11-09)

removing merge-approved as this is merged to M96 per comment above

### am...@google.com (2021-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-11)

Congratulations! The VRP Panel has decided to award you $7500 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and nice work! 

### pb...@google.com (2021-11-11)

Your change has been approved for M97 Branch 4692,please go ahead and merge the CL manually asap so that it would be part of this week’s Dev/Beta release.

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-11-15)

Your change has been approved for M97 Branch 4692. Please go ahead and get the change merged to Branch 4692 manually asap so that it would be part of tomorrow's Dev and this week's first M97 Beta release.

### ni...@chromium.org (2021-11-16)

This should be in M97 for quite a while already. This is the roll that merged it: https://chromiumdash.appspot.com/commit/3e7b25d8bb53f7cc0bc983eaa3146d0061bb2eac

### ni...@chromium.org (2021-11-16)

[Empty comment from Monorail migration]

### va...@google.com (2021-11-16)

Removing Merge-Approved-97 as the initial CL landed already in 9.7: https://chromiumdash.appspot.com/commit/bdf31d5883607db4377b519d7308fb1e639a0448

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-12-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8212f0fb2878e9ec16422eb609a65891606bca91

commit 8212f0fb2878e9ec16422eb609a65891606bca91
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Mon Oct 25 08:58:59 2021

Merged: [TurboFan] Do not use NumberConstant as immediate in x86

Bug: chromium:1254189
(cherry picked from commit bdf31d5883607db4377b519d7308fb1e639a0448)

(cherry picked from commit 5d2b5e7c006c8af13b2d467ce2a38877bad300dc)

Change-Id: I1d4426fee8392c7a680ad67af4bf2745d04b2e52
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3268905
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Reviewed-by: Maya Lekova <mslekova@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/9.6@{#22}
Cr-Original-Branched-From: 0b7bda016178bf438f09b3c93da572ae3663a1f7-refs/heads/9.6.180@{#1}
Cr-Original-Branched-From: 41a5a247d9430b953e38631e88d17790306f7a4c-refs/heads/main@{#77244}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3330865
Reviewed-by: Adam Klein <adamk@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.4@{#54}
Cr-Branched-From: 3b51863bc25492549a8bf96ff67ce481b1a3337b-refs/heads/9.4.146@{#1}
Cr-Branched-From: 2890419fc8fb9bdb507fdd801d76fa7dd9f022b5-refs/heads/master@{#76233}

[modify] https://crrev.com/8212f0fb2878e9ec16422eb609a65891606bca91/src/compiler/backend/ia32/instruction-selector-ia32.cc


### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1254189?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-12-19)

original POC from the restricted content of original description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10\_15\_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15

Steps to reproduce the problem:

```
function foo() {
    let x = 1337;
    x /= true;
    let y = x || NaN;
    y <<= 1;
    let z = 2 >> y;
    return z;
}
console.log(foo());
%PrepareFunctionForOptimization(foo);
foo();
%OptimizeFunctionOnNextCall(foo);
console.log(foo());

```
```
➜  ./d8 --allow-natives-syntax poc.js
0
2

```

What is the expected behavior?

What went wrong?
In ia32, when visit shift

```
static inline void VisitShift(InstructionSelector* selector, Node* node,
                              ArchOpcode opcode) {
  IA32OperandGenerator g(selector);
  Node* left = node->InputAt(0);
  Node* right = node->InputAt(1);

  if (g.CanBeImmediate(right)) {
    selector->Emit(opcode, g.DefineSameAsFirst(node), g.UseRegister(left),
                   g.UseImmediate(right));
  } else {
    selector->Emit(opcode, g.DefineSameAsFirst(node), g.UseRegister(left),
                   g.UseFixed(right, ecx));
  }
}


```

If the right node is `NumberConstant`. In `CanBeImmediate`, `NumberConstant` is considered an immediate.

```
bool CanBeImmediate(Node* node) {
    switch (node->opcode()) {
      case IrOpcode::kInt32Constant:
      case IrOpcode::kNumberConstant:
      case IrOpcode::kExternalConstant:
      case IrOpcode::kRelocatableInt32Constant:
      case IrOpcode::kRelocatableInt64Constant:
        return true;
           ...
    }
  }

```

So it will call `UseImmediate`.

```
InstructionOperand UseImmediate(Node* node) {
    return sequence()->AddImmediate(ToConstant(node));
}

```

In `ToConstant`, `NumberConstant` will be stored in the `Constant` class as a double. And it will be added to `immediates_` in `AddImmediate`.

```
  static Constant ToConstant(const Node* node) {
    switch (node->opcode()) {
      ...
      case IrOpcode::kFloat64Constant:
      case IrOpcode::kNumberConstant:
        return Constant(OpParameter<double>(node->op()));
      ...
      }
      default:
        break;
    }
    UNREACHABLE();
  }


```

In AssembleCodePhase, in `CodeGenerator::AssembleArchInstruction`, If the current instruction is `kIA32Shr` and the second operand is an immediate value, it will call `InputInt5` to get the immediate value.

```
CodeGenerator::CodeGenResult CodeGenerator::AssembleArchInstruction(
    Instruction* instr) {
    ...
    case kIA32Shl:
      if (HasImmediateInput(instr, 1)) {
        __ shl(i.OutputOperand(), i.InputInt5(1));
      } else {
        __ shl_cl(i.OutputOperand());
      }
      break;
    case kIA32Shr:
      if (HasImmediateInput(instr, 1)) {
        __ shr(i.OutputOperand(), i.InputInt5(1));
      } else {
        __ shr_cl(i.OutputOperand());
      }
      break;
    ...
}

```

`InputInt5->InputInt32->ToInt32` . In the Debug version, it will fail in DCHECK because it's type is `float64` . And in the release version, there will be a type confusion.

```
  bool FitsInInt32() const {
    if (type() == kInt32) return true;
    DCHECK(type() == kInt64);
    return value_ >= std::numeric_limits<int32_t>::min() &&
           value_ <= std::numeric_limits<int32_t>::max();
  }

  int32_t ToInt32() const {
    DCHECK(FitsInInt32());
    const int32_t value = static_cast<int32_t>(value_);
    DCHECK_EQ(value_, static_cast<int64_t>(value));
    return value;
  }

```

To trigger this bug, we need to construct a right shift operation where the second operand is a `NumberConstant`.

We can use `ChangeFloat64ToTagged` node to generate `NumberConstant` node in EarlyOptimization. `CheckedTaggedSignedToInt32` node will be lowed to `WordSarShiftOutZeros` node in EffectControlLinearizer. So we can combine `CheckedTaggedSignedToInt32` node and `Word32Shl` node, and use the following optimization in the MachineOperatorReducer to to put NumberConstant on the second operand of `Word32Sar` node.

```

Reduction MachineOperatorReducer::ReduceWord32Shl(Node* node) {
  DCHECK_EQ(IrOpcode::kWord32Shl, node->opcode());
  Int32BinopMatcher m(node);
  if (m.right().Is(0)) return Replace(m.left().node());  // x << 0 => x
  if (m.IsFoldable()) {  // K << K => K  (K stands for arbitrary constants)
    return ReplaceInt32(base::ShlWithWraparound(m.left().ResolvedValue(),
                                                m.right().ResolvedValue()));
  }
  if (m.right().IsInRange(1, 31)) {
    if (m.left().IsWord32Sar() || m.left().IsWord32Shr()) {
      Int32BinopMatcher mleft(m.left().node());

      // If x >> K only shifted out zeros:
      // (x >> K) << L => x           if K == L
      // (x >> K) << L => x >> (K-L) if K > L
      // (x >> K) << L => x << (L-K)  if K < L
      // Since this is used for Smi untagging, we currently only need it for
      // signed shifts.
      if (mleft.op() == machine()->Word32SarShiftOutZeros() &&
          mleft.right().IsInRange(1, 31)) {
        Node* x = mleft.left().node();
        int k = mleft.right().ResolvedValue();
        int l = m.right().ResolvedValue();
        if (k == l) {
          return Replace(x);
        } else if (k > l) {
          node->ReplaceInput(0, x);
          node->ReplaceInput(1, Uint32Constant(k - l));
          NodeProperties::ChangeOp(node, machine()->Word32Sar());
          return Changed(node).FollowedBy(ReduceWord32Sar(node));
        } else {
          DCHECK(k < l);
          node->ReplaceInput(0, x);
          node->ReplaceInput(1, Uint32Constant(l - k));
          return Changed(node);
        }
      }

      // (x >>> K) << K => x & ~(2^K - 1)
      // (x >> K) << K => x & ~(2^K - 1)
      if (mleft.right().Is(m.right().ResolvedValue())) {
        node->ReplaceInput(0, mleft.left().node());
        node->ReplaceInput(1,
                           Uint32Constant(std::numeric_limits<uint32_t>::max()
                                          << m.right().ResolvedValue()));
        NodeProperties::ChangeOp(node, machine()->Word32And());
        return Changed(node).FollowedBy(ReduceWord32And(node));
      }
    }
  }
  return ReduceWord32Shifts(node);
}

```

Did this work before? N/A

Chrome version: 94.0.4606.61 Channel: stable
OS Version: OS X 10.15.7

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057438)*
