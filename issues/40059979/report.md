# Security: Misuse of CanCover

| Field | Value |
|-------|-------|
| **Issue ID** | [40059979](https://issues.chromium.org/issues/40059979) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ss...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2022-06-16 |
| **Bounty** | $7,500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

## VULNERABILITY DETAILS

As mentioned in instruction-selector.h [1], `CanCover` is not transitive. The counter example are Nodes A,B,C such that CanCover(A, B) and CanCover(B, C) and B is pure: The the effect level of A and B might differ. `CanCoverTransitively` does the additional checks.  

But in some places, `Cancover` has been continuously used without additional checks, rather than using `CanCoverTransitively`.  

For example, in function VisitWordCompareZero [2].

```
// Shared routine for word comparison against zero.  
void InstructionSelector::VisitWordCompareZero(Node\* user, Node\* value,  
                                               FlagsContinuation\* cont) {  
  // Try to combine with comparisons against 0 by simply inverting the branch.  
  while (value->opcode() == IrOpcode::kWord32Equal && CanCover(user, value)) {  
    Int32BinopMatcher m(value);  
    if (!m.right().Is(0)) break;  
  
    user = value;  
    value = m.left().node();  
    cont->Negate();  
  }  
  
  if (CanCover(user, value)) {                     <------------------- first CanCover  
    switch (value->opcode()) {  
      case IrOpcode::kWord32Equal:  
        cont->OverwriteAndNegateIfEqual(kEqual);  
        return VisitWord32EqualImpl(this, value, cont);  
      case IrOpcode::kInt32LessThan:  
      ...  

```

It use `CanCover` to reduce the kWord32Equal, when its right input is 0. Then, VisitWord32EqualImpl -> VisitWordCompare -> CanBeMemoryOperand [3], in function CanBeMemoryOperand, it only checks whether CanCover(node, input) holds and whether their effect level are equal.

```
  bool CanBeMemoryOperand(InstructionCode opcode, Node\* node, Node\* input,  
                          int effect_level) {  
    if ((input->opcode() != IrOpcode::kLoad &&  
         input->opcode() != IrOpcode::kLoadImmutable) ||  
        !selector()->CanCover(node, input)) {           <------------------- second CanCover  
      return false;  
    }  
    if (effect_level != selector()->GetEffectLevel(input)) {  
      return false;  
    ...  

```

It doesn't use CanCoverTransitively which will cause nodes that should not have been fused to be fused.  

It is hard to construct the POC, but it can be done. Here is an example.

```
let c0 = 0;  
  
function foo(a, b) {  
    function bar1() {  
        b--;  
        return a;  
    }  
    let x = a == 0xdead;  
  
    function bar2() {}  
    bar2 >>>= 1;  
  
    let res = b !== x;  
    b = x;  
    let y = a > c0;  
    res += c0;  
    return res;  
}  
  
let r1 = foo(2n,6);  
console.log(r1);  
%PrepareFunctionForOptimization(foo);  
let r2 = foo(2n,6);  
%OptimizeFunctionOnNextCall(foo);  
let r3 = foo(2n,6);  
console.log(r3);  

```

We can see the graph after Schedule, in B7

```
  ...  
  34: Load[kRepCompressed|kTypeAny](236, 241, 32, 32)  
  127: Int32Constant[0]  
  38: Word32Equal(34, 25)  
  40: Store[kRepTagged, NoWriteBarrier](236, 241, 25, 34, 32)  
  39: Word32Equal(38, 127)  
  ...  

```

Corresponding to JS:

```
let res = b !== x;  
b = x;  

```

`x` corresponds to Node 25. `!==` is lowered to two `Word32Equal` nodes. `b = x` corresponds to the Store node. This Store node is scheduled between two `Word32Equal` nodes. It is ok to schedule this Store node between these two `Word32Equal` nodes. But in InstructionSelector, Node 39 CanCover Node 38, Node 38 CanCover Node 34, and Node 38 has same effect level with Node 34. So these three nodes are fused, and the Load Node is moved after the Store Node. So the result of Node 39 should be true, and it actually becomes false.  

We can confirm it in next two phases:

```
      60: gap ([rdi|R|t] = [stack:6|t]; [r8|R|t] = [stack:5|t]) ()  
          X64MovqCompressTagged : MRI [r8|R|t] #15 [rdi|R|t]  
      61: gap () ()  
          [rdi|R|w64] = X64Cmp32 : MRI && set if not equal [r8|R|t] #15 [rdi|R|t]  

```

This issue might be the real root cause of <https://crbug.com/chromium/1303458>, but it has existed for a long time. The commit 3d5d99ffd9bd0dd433cfdf8ba9b207648ff51ea9 just made it easier to trigger and exploit. We construct mis-typed values at commit 3d5d99ffd9bd0dd433cfdf8ba9b207648ff51ea9, and achieve arbitrary code execution in the context of v8/Chrome's Renderer process using a typer hardening bypass.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/instruction-selector.h;l=415;drc=c673ac8876330a42eed34e298ff585636af113bc;bpv=0;bpt=1>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/x64/instruction-selector-x64.cc;l=2512?q=visitcomparezero&ss=chromium%2Fchromium%2Fsrc>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:v8/src/compiler/backend/x64/instruction-selector-x64.cc;drc=c673ac8876330a42eed34e298ff585636af113bc;bpv=1;bpt=1;l=68?q=visitcomparezero&ss=chromium%2Fchromium%2Fsrc>

## VERSION

d8 Version: Test on stable(10.2.154.8) and main(21fe5e0fef941e3210c622724b6ee9079668ce29)  

Operating System: Test on Ubuntu 18.04, should exist in all platform

## REPRODUCTION CASE

```
let c0 = 0;  
  
function foo(a, b) {  
    function bar1() {  
        b--;  
        return a;  
    }  
    let x = a == 0xdead;  
  
    function bar2() {}  
    bar2 >>>= 1;  
  
    let res = b !== x;  
    b = x;  
    let y = a > c0;  
    res += c0;  
    return res;  
}  
  
let r1 = foo(2n,6);  
console.log(r1);  
%PrepareFunctionForOptimization(foo);  
let r2 = foo(2n,6);  
%OptimizeFunctionOnNextCall(foo);  
let r3 = foo(2n,6);  
console.log(r3);  

```

`./d8 --allow-natives-syntax poc.js`  

The expected behavior would be to print "1" twice; instead "1" and "0" are printed.  

`type-mismatch.js` can be tested at commit 3d5d99ffd9bd0dd433cfdf8ba9b207648ff51ea9.

## Fix

Before call VisitCompareWithMemoryOperand in VisitWordCompare, check whether CanCoverTransitively holds.

## CREDIT INFORMATION

Reporter credit: srodulv and ZNMchtss at S.S.L Team

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 414 B)
- [type-mismatch.js](attachments/type-mismatch.js) (text/plain, 503 B)

## Timeline

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-06-16)

Thanks for the report. +tebbi@, could you take a look? Thanks!

Also cc the current V8 sheriff clemensb@

[Monorail components: Blink>JavaScript>Compiler]

### [Deleted User] (2022-06-16)

[Empty comment from Monorail migration]

### te...@chromium.org (2022-06-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6048f754931e0971cab58fb0de785482d175175b

commit 6048f754931e0971cab58fb0de785482d175175b
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Fri Jun 17 10:14:44 2022

[compiler] make CanCover() transitive

In addition to checking that a node is owned, CanCover() also needs to
check if there are any side-effects in between the current node and
the merged node. When merging inputs of inputs, this check was done
with the wrong side-effect level of the in-between node.
We partially fixed this before with `CanCoverTransitively`.
This CL addresses the issue by always comparing to the side-effect
level of the node from which we started, making `CanCoverTransitively`
superfluous.

Bug: chromium:1336869
Change-Id: I78479b32461ede81138f8b5d48d60058cfb5fa0a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3707277
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#81217}

[modify] https://crrev.com/6048f754931e0971cab58fb0de785482d175175b/src/compiler/backend/loong64/instruction-selector-loong64.cc
[modify] https://crrev.com/6048f754931e0971cab58fb0de785482d175175b/src/compiler/backend/mips64/instruction-selector-mips64.cc
[modify] https://crrev.com/6048f754931e0971cab58fb0de785482d175175b/src/compiler/backend/instruction-selector.cc
[modify] https://crrev.com/6048f754931e0971cab58fb0de785482d175175b/src/compiler/backend/x64/instruction-selector-x64.cc
[modify] https://crrev.com/6048f754931e0971cab58fb0de785482d175175b/src/compiler/backend/riscv64/instruction-selector-riscv64.cc
[modify] https://crrev.com/6048f754931e0971cab58fb0de785482d175175b/src/compiler/backend/instruction-selector.h


### te...@chromium.org (2022-06-17)

[Empty comment from Monorail migration]

### te...@chromium.org (2022-06-17)

[Empty comment from Monorail migration]

### te...@chromium.org (2022-06-17)

Thanks a lot to the reporters for finding this issue!

This bug demonstrates that the current code does lead to miscompilation, moving a load after a store in very carefully crafted situations. While it doesn't demonstrate this to be exploitable, it is plausible that this can be exploited in some way if a repro is found where the typer predicts a precise type or a repro where the functional error corrupts memory. Therefore, I do consider this a serious issue, despite there being no proof for this being exploitable in any shipping configuration, as 3d5d99ffd9bd0dd433cfdf8ba9b207648ff51ea9 has never reached the stable channel.

My fix should be fairly safe to back-merge and cover all possible variants of the root cause.

### [Deleted User] (2022-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-17)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M102. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M103. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M104. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-18)

Merge approved: your change passed merge requirements and is auto-approved for M104. Please go ahead and merge the CL to branch 5112 (refs/branch-heads/5112) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-18)

Merge review required: M103 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-18)

Merge review required: M102 is already shipping to stable.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-20)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1336869&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Compiler&entry.975983575=tebbi@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2022-06-20)

1. Why does your merge fit within the merge criteria for these milestones?

It's a potentially explitable security issue with a simple fix in very stable code, I'm confident there will be no issues in back-merging this.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/v8/v8/+/3707277

3. Have the changes been released and tested on canary?

Released in canary 105.0.5127.0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

no

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

no

### gi...@appspot.gserviceaccount.com (2022-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/518d38c1eb4ea5d8c3fbe89fe48c8cd462f8dabc

commit 518d38c1eb4ea5d8c3fbe89fe48c8cd462f8dabc
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Fri Jun 17 10:14:44 2022

Merged: [compiler] make CanCover() transitive

In addition to checking that a node is owned, CanCover() also needs to
check if there are any side-effects in between the current node and
the merged node. When merging inputs of inputs, this check was done
with the wrong side-effect level of the in-between node.
We partially fixed this before with `CanCoverTransitively`.
This CL addresses the issue by always comparing to the side-effect
level of the node from which we started, making `CanCoverTransitively`
superfluous.

Bug: chromium:1336869
(cherry picked from commit 6048f754931e0971cab58fb0de785482d175175b)

Change-Id: I59ec8bdf9699052ea7a2302d16854991f8ec45ff
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3714243
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.4@{#13}
Cr-Branched-From: b1413ed7c71ababe05d590de4b5c4ed97b68693e-refs/heads/10.4.132@{#1}
Cr-Branched-From: 9d0a09368569234a1d1094975e2e92591922cd08-refs/heads/main@{#80972}

[modify] https://crrev.com/518d38c1eb4ea5d8c3fbe89fe48c8cd462f8dabc/src/compiler/backend/mips64/instruction-selector-mips64.cc
[modify] https://crrev.com/518d38c1eb4ea5d8c3fbe89fe48c8cd462f8dabc/src/compiler/backend/loong64/instruction-selector-loong64.cc
[modify] https://crrev.com/518d38c1eb4ea5d8c3fbe89fe48c8cd462f8dabc/src/compiler/backend/instruction-selector.cc
[modify] https://crrev.com/518d38c1eb4ea5d8c3fbe89fe48c8cd462f8dabc/src/compiler/backend/x64/instruction-selector-x64.cc
[modify] https://crrev.com/518d38c1eb4ea5d8c3fbe89fe48c8cd462f8dabc/src/compiler/backend/riscv64/instruction-selector-riscv64.cc
[modify] https://crrev.com/518d38c1eb4ea5d8c3fbe89fe48c8cd462f8dabc/src/compiler/backend/instruction-selector.h


### [Deleted User] (2022-06-20)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-21)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2022-06-23)

Merged to Chrome 104.0.5112.20

### te...@chromium.org (2022-06-23)

I'm still waiting for merge review M102/M103.

### va...@chromium.org (2022-06-23)

pbommana@ and srinivassista@ IMO we should back merge the security issue ASAP. PTAL

### am...@chromium.org (2022-06-23)

Hi vahl@ and tebbi@-  this was actually my responsibility to review. :) 
Apologize for not prioritizing sooner, as while I concur this should be certainly merged back, I saw this CL when it landed after the three days after stable cut for M103 stable and M102 ES, which was 14 June and released this past Tuesday, 21 June.

I've now approved for merge- please merge to the relevant V8 branches for M102 and M103 at your earliest convenience and this fix will be included in the next security respins for Stable and ES. Thank you! 

### am...@google.com (2022-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-24)

Congratulations, srodulv and ZNMchtss! The VRP Panel has decided to award you $7,500 for this report. Thank you for your efforts in discovering and reporting this issue to us! Great work! 

### gi...@appspot.gserviceaccount.com (2022-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/512940e0a39b198ce86bacdad8f4089e5b60dbdd

commit 512940e0a39b198ce86bacdad8f4089e5b60dbdd
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Fri Jun 17 10:14:44 2022

Merged: [compiler] make CanCover() transitive

In addition to checking that a node is owned, CanCover() also needs to
check if there are any side-effects in between the current node and
the merged node. When merging inputs of inputs, this check was done
with the wrong side-effect level of the in-between node.
We partially fixed this before with `CanCoverTransitively`.
This CL addresses the issue by always comparing to the side-effect
level of the node from which we started, making `CanCoverTransitively`
superfluous.

Bug: chromium:1336869
(cherry picked from commit 6048f754931e0971cab58fb0de785482d175175b)

Change-Id: Ic731d663e311f613e3edd8c653f913b22d53fe6f
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3721818
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.3@{#25}
Cr-Branched-From: 1a8f4cab47232e7861928945eeee1c40fe7f7c08-refs/heads/10.3.174@{#1}
Cr-Branched-From: 8fbefa47971832fc5afaffb913ae9689f0cc9f9e-refs/heads/main@{#80471}

[modify] https://crrev.com/512940e0a39b198ce86bacdad8f4089e5b60dbdd/src/compiler/backend/mips64/instruction-selector-mips64.cc
[modify] https://crrev.com/512940e0a39b198ce86bacdad8f4089e5b60dbdd/src/compiler/backend/loong64/instruction-selector-loong64.cc
[modify] https://crrev.com/512940e0a39b198ce86bacdad8f4089e5b60dbdd/src/compiler/backend/instruction-selector.cc
[modify] https://crrev.com/512940e0a39b198ce86bacdad8f4089e5b60dbdd/src/compiler/backend/x64/instruction-selector-x64.cc
[modify] https://crrev.com/512940e0a39b198ce86bacdad8f4089e5b60dbdd/src/compiler/backend/riscv64/instruction-selector-riscv64.cc
[modify] https://crrev.com/512940e0a39b198ce86bacdad8f4089e5b60dbdd/src/compiler/backend/instruction-selector.h


### gi...@appspot.gserviceaccount.com (2022-06-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/13ffdf63a471dda4cd9369a55e6df539a79369dd

commit 13ffdf63a471dda4cd9369a55e6df539a79369dd
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Fri Jun 17 10:14:44 2022

Merged: [compiler] make CanCover() transitive

In addition to checking that a node is owned, CanCover() also needs to
check if there are any side-effects in between the current node and
the merged node. When merging inputs of inputs, this check was done
with the wrong side-effect level of the in-between node.
We partially fixed this before with `CanCoverTransitively`.
This CL addresses the issue by always comparing to the side-effect
level of the node from which we started, making `CanCoverTransitively`
superfluous.

Bug: chromium:1336869
(cherry picked from commit 6048f754931e0971cab58fb0de785482d175175b)

Change-Id: I63cf6bfdd40c2c55921db4a2ac737612bb7da4e4
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3722095
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.2@{#19}
Cr-Branched-From: 374091f382e88095694c1283cbdc2acddc1b1417-refs/heads/10.2.154@{#1}
Cr-Branched-From: f0c353f6315eeb2212ba52478983a3b3af07b5b1-refs/heads/main@{#79976}

[modify] https://crrev.com/13ffdf63a471dda4cd9369a55e6df539a79369dd/src/compiler/backend/loong64/instruction-selector-loong64.cc
[modify] https://crrev.com/13ffdf63a471dda4cd9369a55e6df539a79369dd/src/compiler/backend/mips64/instruction-selector-mips64.cc
[modify] https://crrev.com/13ffdf63a471dda4cd9369a55e6df539a79369dd/src/compiler/backend/instruction-selector.cc
[modify] https://crrev.com/13ffdf63a471dda4cd9369a55e6df539a79369dd/src/compiler/backend/x64/instruction-selector-x64.cc
[modify] https://crrev.com/13ffdf63a471dda4cd9369a55e6df539a79369dd/src/compiler/backend/riscv64/instruction-selector-riscv64.cc
[modify] https://crrev.com/13ffdf63a471dda4cd9369a55e6df539a79369dd/src/compiler/backend/instruction-selector.h


### te...@chromium.org (2022-06-24)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-06-27)

1. Just https://crrev.com/c/3726007
2. Low, no conflicts
3. 102, 103
4. Yes

### gm...@google.com (2022-06-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6d3075a34fd3ef5ec6e6bd2e87b42c68a6935745

commit 6d3075a34fd3ef5ec6e6bd2e87b42c68a6935745
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Fri Jun 17 10:14:44 2022

[M96-LTS][compiler] make CanCover() transitive

In addition to checking that a node is owned, CanCover() also needs to
check if there are any side-effects in between the current node and
the merged node. When merging inputs of inputs, this check was done
with the wrong side-effect level of the in-between node.
We partially fixed this before with `CanCoverTransitively`.
This CL addresses the issue by always comparing to the side-effect
level of the node from which we started, making `CanCoverTransitively`
superfluous.

(cherry picked from commit 6048f754931e0971cab58fb0de785482d175175b)

Bug: chromium:1336869
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: I78479b32461ede81138f8b5d48d60058cfb5fa0a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3707277
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#81217}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3726007
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Owners-Override: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.6@{#70}
Cr-Branched-From: 0b7bda016178bf438f09b3c93da572ae3663a1f7-refs/heads/9.6.180@{#1}
Cr-Branched-From: 41a5a247d9430b953e38631e88d17790306f7a4c-refs/heads/main@{#77244}

[modify] https://crrev.com/6d3075a34fd3ef5ec6e6bd2e87b42c68a6935745/src/compiler/backend/loong64/instruction-selector-loong64.cc
[modify] https://crrev.com/6d3075a34fd3ef5ec6e6bd2e87b42c68a6935745/src/compiler/backend/mips64/instruction-selector-mips64.cc
[modify] https://crrev.com/6d3075a34fd3ef5ec6e6bd2e87b42c68a6935745/src/compiler/backend/instruction-selector.cc
[modify] https://crrev.com/6d3075a34fd3ef5ec6e6bd2e87b42c68a6935745/src/compiler/backend/x64/instruction-selector-x64.cc
[modify] https://crrev.com/6d3075a34fd3ef5ec6e6bd2e87b42c68a6935745/src/compiler/backend/riscv64/instruction-selector-riscv64.cc
[modify] https://crrev.com/6d3075a34fd3ef5ec6e6bd2e87b42c68a6935745/src/compiler/backend/instruction-selector.h


### rz...@google.com (2022-06-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-03)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-03)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1336869?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059979)*
