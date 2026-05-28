# Security: SEGV_ACCERR in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40063542](https://issues.chromium.org/issues/40063542) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ki...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2023-03-11 |
| **Bounty** | $21,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that commit https://crrev.com/a92801661d3b26c1745da087db2f0abfb621b9b8 caused this problem.

- 85841 will not trigger crash: 
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-85841.zip?generation=1676473223418611&alt=media
- And 85842 will cause crash:
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-85842.zip?generation=1676473379968038&alt=media

commit	a92801661d3b26c1745da087db2f0abfb621b9b8	[log] [tgz]
author	Darius M <dmercadier@chromium.org>	Wed Feb 15 10:58:31 2023
committer	V8 LUCI CQ <v8-scoped@luci-project-accounts.iam.gserviceaccount.com>	Wed Feb 15 14:58:50 2023
tree	bd0804b07fd89983e446f8054e8350ebec52996e
parent	06d0fde1fe66bb9a11454d852733a8676b44e83f [diff]

[maglev] Support untagged Phis

Design doc: https://docs.google.com/document/d/1DSetLAdTIKp6DZebFw25YNqOzE-U6QWPTZFlORzbk_4/edit?usp=sharing

Bug: v8:7700
Change-Id: Ie9c62876c0d9c352f1b02c3a9dd942c1350d8551
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4233560
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85842}

## CRASH LOG
- Debug output
```
> d8-linux-debug-v8-component-86359/d8 --future --expose-gc /tmp/poc.js
...
Received signal 11 SEGV_ACCERR 0785beac0008

==== C stack trace ===============================

 [0x7f7afb3a2f33]
 [0x7f7afb3a2e72]
 [0x7f7af6e42520]
 [0x7f7af9457941]
 [0x7f7af9e5560c]
 [0x7f7af9d355b0]
 [0x7f7af89c14ee]
[end of stack trace]
[1]    23863 segmentation fault (core dumped)  /tmp/d8-linux-debug-v8-component-86359/d8-linux-debug-v8-component-86359/d8
```


## Other
If you want to use clusterfuzz for classification, please note to include the flags:  `--future --expose-gc`

VERSION
Tested on v8 version: 11.3.0

REPRODUCTION CASE
1. Download debug v8 from: https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-86359.zip?generation=1678507383289660&alt=media
2. Run: `d8-linux-debug-v8-component-86359/d8 --future --expose-gc poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 525 B)
- [poc.js](attachments/poc.js) (text/plain, 525 B)
- [poc1.js](attachments/poc1.js) (text/plain, 296 B)
- [oob-exp.js](attachments/oob-exp.js) (text/plain, 1.7 KB)
- [rce-exp.js](attachments/rce-exp.js) (text/plain, 3.5 KB)
- [repo.mp4](attachments/repo.mp4) (video/mp4, 1.1 MB)

## Timeline

### [Deleted User] (2023-03-11)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-03-11)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that commit https://crrev.com/a92801661d3b26c1745da087db2f0abfb621b9b8 caused this problem.

- 85841 will not trigger crash: 
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-85841.zip?generation=1676473223418611&alt=media
- And 85842 will cause crash:
https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-85842.zip?generation=1676473379968038&alt=media

commit	a92801661d3b26c1745da087db2f0abfb621b9b8	[log] [tgz]
author	Darius M <dmercadier@chromium.org>	Wed Feb 15 10:58:31 2023
committer	V8 LUCI CQ <v8-scoped@luci-project-accounts.iam.gserviceaccount.com>	Wed Feb 15 14:58:50 2023
tree	bd0804b07fd89983e446f8054e8350ebec52996e
parent	06d0fde1fe66bb9a11454d852733a8676b44e83f [diff]

[maglev] Support untagged Phis

Design doc: https://docs.google.com/document/d/1DSetLAdTIKp6DZebFw25YNqOzE-U6QWPTZFlORzbk_4/edit?usp=sharing

Bug: v8:7700
Change-Id: Ie9c62876c0d9c352f1b02c3a9dd942c1350d8551
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4233560
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85842}

## CRASH LOG
- Debug output
```
> d8-linux-debug-v8-component-86359/d8 --future --expose-gc /tmp/poc.js
...
Received signal 11 SEGV_ACCERR 0785beac0008

==== C stack trace ===============================

 [0x7f7afb3a2f33]
 [0x7f7afb3a2e72]
 [0x7f7af6e42520]
 [0x7f7af9457941]
 [0x7f7af9e5560c]
 [0x7f7af9d355b0]
 [0x7f7af89c14ee]
[end of stack trace]
[1]    23863 segmentation fault (core dumped)  /tmp/d8-linux-debug-v8-component-86359/d8-linux-debug-v8-component-86359/d8
```


## Other
If you want to use clusterfuzz for classification, please note to include the flags:  `--future --expose-gc`

VERSION
Tested on v8 version: 11.3.0

REPRODUCTION CASE
1. Download debug v8 from: https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-86359.zip?generation=1678507383289660&alt=media
2. Run: `d8-linux-debug-v8-component-86359/d8 --future --expose-gc poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

### ma...@chromium.org (2023-03-13)

Assigning per reported bisect
Cc per maglev triage
Impact-none per --future / maglev

[Monorail components: Blink>JavaScript>Compiler>Maglev]

### ma...@chromium.org (2023-03-13)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-03-15)

Hello, is there still active? Thanks!

### dm...@chromium.org (2023-03-16)

We were missing a write barrier, which means that we could have old->new pointers that weren't in the remembered set, which would then create dangling pointers when the young object was removed but the old->new pointer wasn't updated --> Security_Severity-High

(fix incoming)

### ki...@gmail.com (2023-03-16)

[Comment Deleted]

### ki...@gmail.com (2023-03-16)

I modified the poc, the new poc will be more suitable to be set up as a regression test.
Since we are missing a write barrier setting, `Array.prototype.toString` is stored directly in `Array.prototype` without any write barriers.
Because the `Array.prototype` object is in old-space, the `Array.prototype.toString` HeapNumber allocated in NewSpace, and a minor GC happens this leads to `Array.prototype.toString` being a dangling pointer and pointing to arbitrary objects in NewSpace.

- some debug log
```
        ...
        %DebugPrint(Array.prototype.toString); // before gc, is 0.0( a heap number)
        gc();
        %DebugPrint(Array.prototype.toString); // now  pointing to other object!
        print(Array.prototype.toString);
        ...
```

DebugPrint: 0.0
0x320200000345: [Map] in ReadOnlySpace
 - type: HEAP_NUMBER_TYPE
 - instance size: 12
 - elements kind: HOLEY_ELEMENTS
 - unused property fields: 0
 - enum length: invalid
 - stable_map
 - back pointer: 0x320200000251 <undefined>
 - prototype_validity cell: 0
 - instance descriptors (own) #0: 0x320200000295 <DescriptorArray[0]>
 - prototype: 0x320200000235 <null>
 - constructor: 0x320200000235 <null>
 - dependent code: 0x320200000229 <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0

DebugPrint: 0x3202000421c5: [String]: u#
Smi: 0x50b3f (330559)


### gi...@appspot.gserviceaccount.com (2023-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/09dd673aa7e115b9e72fd4da27d9048d2375281b

commit 09dd673aa7e115b9e72fd4da27d9048d2375281b
Author: Darius M <dmercadier@chromium.org>
Date: Thu Mar 16 16:16:25 2023

[maglev] Insert missing writer barrier after some phi untagging

When the graph builder creates a StoreTaggedField, it drops the write
barrier when it knows that the value being stored is a Smi (typically
because there was a CheckedSmiUntag or CheckSmi earlier), and
generates a StoreTaggedFieldNoWriteBarrier.

However, after phi untagging, if the value was a Smi, we could have
decided to untag it to a Float64 representation rather than to Int32
(or, even if we untagged it to Int32, it could overflow the Smi range,
and, when retagging it, we might need to box it). In such cases, the
value that we're storing is going to be a heap object rather than a
Smi, which means that the stores requires a writer barrier; we thus
change the StoreTaggedFieldNoWriteBarrier into a
StoreTaggedFieldWithWriteBarrier.

Fixed: chromium:1423610
Bug: v8:7700
Change-Id: Ic819e3bbd7c0bd165e8582126716b6d57950c852
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4341659
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#86507}

[modify] https://crrev.com/09dd673aa7e115b9e72fd4da27d9048d2375281b/src/maglev/maglev-phi-representation-selector.cc
[add] https://crrev.com/09dd673aa7e115b9e72fd4da27d9048d2375281b/test/mjsunit/maglev/regress/regress-crbug-1423610.js
[modify] https://crrev.com/09dd673aa7e115b9e72fd4da27d9048d2375281b/src/maglev/maglev-ir.h
[modify] https://crrev.com/09dd673aa7e115b9e72fd4da27d9048d2375281b/src/maglev/maglev-phi-representation-selector.h
[modify] https://crrev.com/09dd673aa7e115b9e72fd4da27d9048d2375281b/src/maglev/maglev-ir.cc


### [Deleted User] (2023-03-16)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-03-17)

Hello! This is undoubtedly a vulnerability that can cause an RCE, and I am working on an exploit for this vulnerability for further reference in v8 reward.
Now I can fake an object to cause out-of-bound read&write with attached POC, and the full exploit will be available soon :)

Exploit commit: 3eeca75f1c5ae67026a8fa440d490424ecd8c3e5 (HEAD, tag: 11.3.148-pgo, tag: 11.3.148, origin/11.3.148) (#86362)
OOB exploit output:

```
> v8 git:(11.3.148)  out/x64.release/d8 --allow-natives-syntax --future /tmp/exp.js
DebugPrint: 0x340d00042165: [JSArray]
 - map: 0x340d0018e979 <Map[16](PACKED_DOUBLE_ELEMENTS)> [FastProperties]
 - prototype: 0x340d0018e399 <JSArray[0]>
 - elements: 0x340d00042149 <FixedDoubleArray[5]> [PACKED_DOUBLE_ELEMENTS]
 - length: 196608
 - properties: 0x340d00000219 <FixedArray[0]>
 - All own properties (excluding elements): {
    0x340d00000e19: [String] in ReadOnlySpace: #length: 0x340d0014428d <AccessorInfo name= 0x340d00000e19 <String[6]: #length>, data= 0x340d00000251 <undefined>> (const accessor descriptor), location: descriptor
 }
 - elements: 0x340d00042149 <FixedDoubleArray[5]> {
         0-1: 0
           2: 3.46444e-308
           3: 5.7435e-309
           4: 8.34403e-309
 }
0x340d0018e979: [Map] in OldSpace
 - type: JS_ARRAY_TYPE
 - instance size: 16
 - inobject properties: 0
 - elements kind: PACKED_DOUBLE_ELEMENTS
 - unused property fields: 0
 - enum length: invalid
 - back pointer: 0x340d0018e939 <Map[16](HOLEY_SMI_ELEMENTS)>
 - prototype_validity cell: 0x340d00000ac5 <Cell value= 1>
 - instance descriptors #1: 0x340d0018e905 <DescriptorArray[1]>
 - transitions #1: 0x340d0018e9a1 <TransitionArray[4]>Transition array #1:
     0x340d00000edd <Symbol: (elements_transition_symbol)>: (transition to HOLEY_DOUBLE_ELEMENTS) -> 0x340d0018e9b9 <Map[16](HOLEY_DOUBLE_ELEMENTS)>

 - prototype: 0x340d0018e399 <JSArray[0]>
 - constructor: 0x340d0018e0c1 <JSFunction Array (sfi = 0x340d00157ec1)>
 - dependent code: 0x340d00000229 <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0

[+] fake_array.length:  196608
[+] oob fake_array[200]:  1.2583435043077e-311
```

### ki...@gmail.com (2023-03-17)

Full exploit is available now!  The shellcode used here will open a shell locally.

To reproduce the exploit, simply run the following commands:

```bash
➜  v8 git:(11.3.148) git checkout 11.3.148
HEAD 目前位于 3eeca75f1c Version 11.3.148
➜  v8 git:(11.3.148) git status
头指针分离于 11.3.148
无文件要提交，干净的工作区
➜  v8 git:(11.3.148) tools/dev/gm.py x64.release
# autoninja -C out/x64.release d8
ninja: Entering directory `out/x64.release'
ninja: no work to do.
Done! - V8 compilation finished successfully.
➜  v8 git:(11.3.148) out/x64.release/d8 --allow-natives-syntax --future /tmp/exp.js
$ whoami
kiprey
$ uname -a
Linux  5.19.0-32-generic #33~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Jan 30 17:03:34 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
$ exit
```

### [Deleted User] (2023-03-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-22)

Congratulations, Kipreyyy! The VRP Panel has decided to award you $20,000 for this report and V8 exploit + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- excellent work! 

### am...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-24)

[Description Changed]

### is...@google.com (2023-07-24)

This issue was migrated from crbug.com/chromium/1423610?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1423616]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063542)*
