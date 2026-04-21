# Security: Information Leak in Array indexOf

| Field | Value |
|-------|-------|
| **Issue ID** | [40086773](https://issues.chromium.org/issues/40086773) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Runtime |
| **Reporter** | cw...@gmail.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2017-02-12 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

This vulnerability occurs in the following two functions:

- Array.prototype.indexOf(arr, elem, from\_index);
- Array.prototype.includes(arr, elem, from\_index);

I'll describe only indexOf since two vulnerabilities occurs in the similar process.

Summary: In the process of Array.indexOf, properties of arr can be changed.

In runtime-array.cc,

1. it checks the length of the target array first (<https://chromium.googlesource.com/v8/v8/+/5.6.326.50/src/runtime/runtime-array.cc#574>).
2. from\_index is converted to integer by calling Object::ToInteger (<https://chromium.googlesource.com/v8/v8/+/5.6.326.50/src/runtime/runtime-array.cc#586>).
3. Iterate elements using the length calculated in 1.

In the step 2, the length of the target array can be changed (or any properties can be changed). If we pass a typed array to the `arr`, and if we neuter arr.buffer in the step 2. Then, step 3 search in freed elements.

**VERSION**  

v8 5.6.326.50 32bit version  

I tested it in Ubuntu 14.04.3 64bit, and compiled v8 to ia32.release.

**REPRODUCTION CASE**

For simplicity, I used ArrayBufferNeuter native function.

================ test.js ==================  

// flags: --allow-natives-syntax  

var buf = new ArrayBuffer(0x10000);  

var arr2 = new Uint8Array(buf).fill(55);  

var tmp = {};  

tmp[Symbol.toPrimitive] = function () {  

%ArrayBufferNeuter(arr2.buffer)  

var arr3 = new Uint8Array(0x800).fill(0xfc);  

return 0;  

};

# print(Array.prototype.indexOf.call(arr2, 0x00, tmp));

$ ./out/ia32.release/d8 --allow-natives-syntax ./test\_arrindex.js  

10

Since we filled the typedarray to 55, it has to print -1. But, in my machine, it prints 10 as an output. It searched freed elements, and found the position of null! If we use Uint8Array for brute-force, we can easily guess values in memories.

## Timeline

### ji...@chromium.org (2017-02-12)

[Empty comment from Monorail migration]

[Monorail components: Infra>Client>V8]

### ji...@chromium.org (2017-02-13)

+yangguo@, could you help triage this issue? Feel free to re-assign owner

### ya...@chromium.org (2017-02-13)

Seems rather serious at first glance.

### bm...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

[Monorail components: -Infra>Client>V8 Blink>JavaScript>Runtime]

### ya...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### bm...@chromium.org (2017-02-13)

Assigning to cbruni@ for investigation: It seems that the IndexOfValueImpl for TypedArrays is missing a neutering check.

### ha...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### ji...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### ji...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### cb...@chromium.org (2017-02-20)

[elements] Check if the backing store has been neutered for indexOf

BUG=691323

Change-Id: I84f2c90355982567c421639e115745eadd5fcb21
Reviewed-on: https://chromium-review.googlesource.com/441964
Reviewed-by: Caitlin Potter <caitp@igalia.com>
Reviewed-by: Camillo Bruni <cbruni@chromium.org>
Commit-Queue: Camillo Bruni <cbruni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#43279}

### cb...@chromium.org (2017-02-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-02-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-02-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-02-21)

If possible, Please merge your change to M57 branch 2987 by 5:00 PM PT today, Tuesday (02/21) so we can pick it up for this week beta release. Thank you.

### mb...@chromium.org (2017-02-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2017-02-24)

Merged to v8 5.7 branch as https://crrev.com/9dae47c8dade7216f624ab4487e610faf90c2237

### aw...@chromium.org (2017-02-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-28)

Congratulations! The panel decided to award $2,000 for this bug!

### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-03-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/691323?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086773)*
