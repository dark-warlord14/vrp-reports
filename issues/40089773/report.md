# Security: Integer overflow in FastArraySliceCodeStubAssembler::HandleFastSlice

| Field | Value |
|-------|-------|
| **Issue ID** | [40089773](https://issues.chromium.org/issues/40089773) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2017-12-03 |
| **Bounty** | $5,500.00 |

## Description

**VULNERABILITY DETAILS**  

<https://cs.chromium.org/chromium/src/v8/src/builtins/builtins-array-gen.cc?rcl=fc33dfbebfb1cb800d490af97bf1019e9d66be33&l=1114>  

Node\* HandleFastSlice(Node\* context, Node\* array, Node\* from, Node\* count,  

Label\* slow) {  

VARIABLE(result, MachineRepresentation::kTagged);  

Label done(this);

```
GotoIf(TaggedIsNotSmi(from), slow);  
GotoIf(TaggedIsNotSmi(count), slow);  

[...]  

int max_fast_elements =  
    (kMaxRegularHeapObjectSize - FixedArray::kHeaderSize - JSArray::kSize -  
     AllocationMemento::kSize) /  
    kPointerSize;  
GotoIf(SmiAboveOrEqual(count, SmiConstant(max_fast_elements)),  
       &try_simple_slice);  

GotoIf(SmiLessThan(from, SmiConstant(0)), slow);  

Node\* end = SmiAdd(from, count); //\*\*\*1\*\*\*  

Node\* unmapped_elements = LoadFixedArrayElement(  
    sloppy_elements, SloppyArgumentsElements::kArgumentsIndex);  
Node\* unmapped_elements_length =  
    LoadFixedArrayBaseLength(unmapped_elements);  

GotoIf(SmiGreaterThan(end, unmapped_elements_length), slow); //\*\*\*2\*\*\*  

Node\* array_map = LoadJSArrayElementsMap(HOLEY_ELEMENTS, native_context);  
result.Bind(AllocateJSArray(HOLEY_ELEMENTS, array_map, count, count,  
                            nullptr, SMI_PARAMETERS));  

index_out.Bind(IntPtrConstant(0));  
Node\* result_elements = LoadElements(result.value());  
Node\* from_mapped = SmiMin(parameter_map_length, from);  
Node\* to = SmiMin(parameter_map_length, end); //\*\*\*3\*\*\*  
Node\* arguments_context = LoadFixedArrayElement(  
    sloppy_elements, SloppyArgumentsElements::kContextIndex);  
VariableList var_list({&index_out}, zone());  
BuildFastLoop(  
    var_list, from_mapped, to,  
    [this, result_elements, arguments_context, sloppy_elements,  
     unmapped_elements, &index_out](Node\* current) {  
      Node\* context_index = LoadFixedArrayElement(  
          sloppy_elements, current,  
          kPointerSize \* SloppyArgumentsElements::kParameterMapStart,  
          SMI_PARAMETERS); //\*\*\*4\*\*\*  
      Label is_the_hole(this), done(this);  
      GotoIf(IsTheHole(context_index), &is_the_hole);  
      Node\* mapped_argument =  
          LoadContextElement(arguments_context, SmiUntag(context_index));  
      StoreFixedArrayElement(result_elements, index_out.value(),  
                             mapped_argument, SKIP_WRITE_BARRIER); //\*\*\*5\*\*\*  

```

[...]

An integer overflow can occur in (1), and |end| can end up being a negative number.  

Since the sanity checks in (2) and (3) are implemented using signed integer arithmetic,  

a negative |end| passes both checks leading to out-of-bounds access later in (4) and (5).

Replacing |SmiGreaterThan()| with |SmiAbove()| should be enough to fix the issue.

**VERSION**  

Google Chrome 64.0.3278.0 (Official Build) dev (64-bit)  

Google Chrome 64.0.3282.3 (Official Build) canary (32-bit)  

The stable and beta branches are not affected.

**REPRODUCTION CASE**

<script>
(function(a) {
var len = navigator.userAgent.includes("x64") ? 0x80000000 : 0x40000000;
arguments.length = len;
Array.prototype.slice.call(arguments, len - 1, len);
}('a'))
</script>

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 9.5 KB)

## Timeline

### el...@chromium.org (2017-12-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### el...@chromium.org (2017-12-03)

+V8 Sheriff

### ha...@chromium.org (2017-12-03)

[Empty comment from Monorail migration]

### ra...@chromium.org (2017-12-03)

[Empty comment from Monorail migration]

### bm...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-12-04)

awhalley for further impact triage.

### da...@chromium.org (2017-12-04)

Good catch, taking a look.

### aw...@google.com (2017-12-04)

+raymes, current Chrome Security Sheriff

### pa...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-12-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/6f6ca7301abc5e0bf1745ba7e99c2676e9cfa0f9

commit 6f6ca7301abc5e0bf1745ba7e99c2676e9cfa0f9
Author: Daniel Clifford <danno@chromium.org>
Date: Tue Dec 05 14:34:17 2017

Fix OOB access in Array.prototype.slice

Bug: chromium:791345
Change-Id: I81e5e23e2ddfc5e78a4ca922ceffda28516277c3
Reviewed-on: https://chromium-review.googlesource.com/806097
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Daniel Clifford <danno@chromium.org>
Cr-Commit-Position: refs/heads/master@{#49871}
[modify] https://crrev.com/6f6ca7301abc5e0bf1745ba7e99c2676e9cfa0f9/src/builtins/builtins-array-gen.cc
[add] https://crrev.com/6f6ca7301abc5e0bf1745ba7e99c2676e9cfa0f9/test/mjsunit/regress/regress-791345.js


### da...@chromium.org (2017-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-06)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-06)

Your change meets the bar and is auto-approved for M64. Please go ahead and merge the CL to branch 3282 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-11)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-12-11)

[Empty comment from Monorail migration]

### ca...@chromium.org (2017-12-11)

danno@, reminder to please merge change to 3282 branch soon.

### bu...@chromium.org (2017-12-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/72223a655e6c94f51a681cd6a397d56191b7b95c

commit 72223a655e6c94f51a681cd6a397d56191b7b95c
Author: Daniel Clifford <danno@chromium.org>
Date: Mon Dec 11 22:16:46 2017

Merged: Fix OOB access in Array.prototype.slice

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Bug: chromium:791345
Change-Id: I81e5e23e2ddfc5e78a4ca922ceffda28516277c3
Reviewed-on: https://chromium-review.googlesource.com/806097
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Daniel Clifford <danno@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#49871}(cherry picked from commit 6f6ca7301abc5e0bf1745ba7e99c2676e9cfa0f9)
Reviewed-on: https://chromium-review.googlesource.com/820730
Cr-Commit-Position: refs/branch-heads/6.4@{#10}
Cr-Branched-From: 0407506af3d9d7e2718be1d8759296165b218fcf-refs/heads/6.4.388@{#1}
Cr-Branched-From: a5fc4e085ee543cb608eb11034bc8f147ba388e1-refs/heads/master@{#49724}
[modify] https://crrev.com/72223a655e6c94f51a681cd6a397d56191b7b95c/src/builtins/builtins-array-gen.cc
[add] https://crrev.com/72223a655e6c94f51a681cd6a397d56191b7b95c/test/mjsunit/regress/regress-791345.js


### cm...@chromium.org (2017-12-13)

Please merge this issue to M64 branch 3282 if it has been verified in canary. The sooner the better. Thanks!

### ha...@google.com (2017-12-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-14)

Thanks as ever! The VRP panel decided to award $5,000 for this, and $500 for supplying the fix we used.

### aw...@chromium.org (2017-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-31)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-06-26)

This issue was migrated from crbug.com/chromium/791345?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089773)*
