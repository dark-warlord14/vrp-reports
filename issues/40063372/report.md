# Crash in Builtins_StoreTypedElementJSAny_Int16Elements_0

| Field | Value |
|-------|-------|
| **Issue ID** | [40063372](https://issues.chromium.org/issues/40063372) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | wh...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-03-04 |
| **Bounty** | $7,000.00 |

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

**VULNERABILITY DETAILS**  

SEGV\_ACCERR OOB Write

**VERSION**  

v8

**REPRODUCTION CASE**

using default d8 or from <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-86236.zip?generation=1677865234314716&alt=media> (latest commit at current time)  

run "./d8 poc.js"

PoC  

function main() {  

const v2 = {"maxByteLength":14990892};  

const v3 = new ArrayBuffer(14990892,v2);  

const v5 = new Int16Array(v3);  

const v7 = new Int32Array();  

function v8(v9) {  

const v10 = v3.resize();  

return v10;  

}  

const v11 = [v7];  

const v12 = v11;  

const v13 = v5;  

const v15 = Float64Array.from;  

function v16(v17) {  

return v13;  

}  

const v18 = v15.call(v16,v12,v8);  

}  

main();

RAX 0x0  

\*RBX 0x260b00000000 ◂— 0x0  

RCX 0x0  

RDX 0x0  

\*RDI 0x7fff17736640 —▸ 0x26080010c589 ◂— 0xa9000022a90024ba  

\*RSI 0x260800020485 ◂— 0x8e50431cae00002f /\* '/' \*/  

R8 0x0  

\*R9 0x6  

\*R10 0xffffffff  

\*R11 0x7fff177367c0 —▸ 0x26080010c5c9 ◂— 0xa1000022a90024ea  

\*R12 0x26080025ae01 ◂— 0xf100000020000032 /\* '2' \*/  

\*R13 0x5598af926af0 —▸ 0x260800000000 ◂— 0x40000  

\*R14 0x260800000000 ◂— 0x40000  

\*R15 0x5598af959ef0 —▸ 0x7f47dfdb7f00 ◂— lea rbx, [rip - 7]  

\*RBP 0x7fff177367d8 —▸ 0x7fff17736868 —▸ 0x7fff17736930 —▸ 0x7fff17736988 —▸ 0x7fff177369b8 ◂— ...  

\*RSP 0x7fff177367a0 —▸ 0x260800002231 ◂— 0x8322000007000021 /\* '!' \*/  

\*RIP 0x7f47dfdb3664 ◂— mov word ptr [rbx + rcx\*2], r8w  

──────────────────────────────────────[ DISASM / x86-64 / set emulate on ]───────────────────────────────────────  

► 0x7f47dfdb3664 mov word ptr [rbx + rcx\*2], r8w  

0x7f47dfdb3669 xor eax, eax  

0x7f47dfdb366b mov rsp, rbp  

0x7f47dfdb366e pop rbp  

0x7f47dfdb366f ret  

↓  

0x7f47dfd33b75 mov r8d, eax  

0x7f47dfd33b78 mov r10d, 0xffffffff  

0x7f47dfd33b7e cmp r8, r10  

0x7f47dfd33b81 jbe 0x7f47dfd33b90 <0x7f47dfd33b90>  

↓  

0x7f47dfd33b90 mov r10, rsp  

0x7f47dfd33b93 sub rsp, 8

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [stable_repro.mp4](attachments/stable_repro.mp4) (video/mp4, 652.0 KB)

## Timeline

### [Deleted User] (2023-03-04)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-03-04)

bisect

commit that introduced the bug is 0863bcdf712131b67c2474da60daddff8b844d92 (v8 repo) [1]
active release branch: M112/dev M111/beta  and note that stable version 111.0.5563.50 ( seems will released in Mar 7,2023)

[1] https://chromiumdash.appspot.com/commit/0863bcdf712131b67c2474da60daddff8b844d92



### wh...@gmail.com (2023-03-04)

bisect

commit that introduced the bug is 0863bcdf712131b67c2474da60daddff8b844d92 (This CL ships --harmony-rab-gsab) [1]  
                                               and 9b4a0b9b9f8a9bbe3e2a27c78b8636849ab963f8  (the commit seems not related this bug, but I tested at this commit and previous commit 7586dc7910e66f2a2d45721f685980535f961645 with add argument "--harmony-rab-gsab" . From commit 9b4a0b9b9f8a9bbe3e2a27c78b8636849ab963f8 is affected.  
You can tested previous commit using https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-81999.zip?generation=1658924774764589&alt=media
introduced commit: https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-82000.zip?generation=1658925621743067&alt=media


active release branch: M112/dev M111/beta  and stable version 111.0.5563.50 ( seems will released in Mar 7,2023)

[1] https://chromiumdash.appspot.com/commit/0863bcdf712131b67c2474da60daddff8b844d92

### wh...@gmail.com (2023-03-04)

this bug is similar to https://crbug.com/chromium/1393375

details

typed array buffer can be resized during TypedArrayFrome [1]
while typed array buffer become 
DebugPrint: 0x1fec00000251: [Oddball] in ReadOnlySpace: #undefined
0x1fec00000151: [Map] in ReadOnlySpace
 - type: ODDBALL_TYPE
 - instance size: 28
 - elements kind: HOLEY_ELEMENTS
 - unused property fields: 0
 - enum length: invalid
 - stable_map
 - undetectable
 - non-extensible
 - back pointer: 0x1fec00000251 <undefined>
 - prototype_validity cell: 0
 - instance descriptors (own) #0: 0x1fec00000295 <DescriptorArray[0]>
 - prototype: 0x1fec00000235 <null>
 - constructor: 0x1fec00000235 <null>
 - dependent code: 0x1fec00000229 <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0

but access it [2]

```

    const mapfn: Callable = Cast<Callable>(mapfnObj) otherwise unreachable;   
    const accessor: TypedArrayAccessor =
        GetTypedArrayAccessor(targetObj.elements_kind);
    // 6d-6e and 11-12.
    // 11. Let k be 0.
    // 12. Repeat, while k < len
    for (let k: uintptr = 0; k < finalLength; k++) {
      // 12a. Let Pk be ! ToString(k).
      const kNum = Convert<Number>(k);
      // 12b. Let kValue be ? Get(arrayLike, Pk).
      const kValue: JSAny = GetProperty(finalSource, kNum);
      let mappedValue: JSAny;
      // 12c. If mapping is true, then
      if (mapping) {
        // i. Let mappedValue be ? Call(mapfn, T, « kValue, k »).
        mappedValue = Call(context, mapfn, thisArg, kValue, kNum);
      } else {
        // 12d. Else, let mappedValue be kValue.
        mappedValue = kValue;
      }
      // 12e. Perform ? Set(targetObj, Pk, mappedValue, true).
      // Buffer may be detached during executing ToNumber/ToBigInt.
      accessor.StoreJSAny(context, targetObj, k, mappedValue)
          otherwise IfDetached;
      // 12f. Set k to k + 1. (done by the loop).
    }
```

[1] https://chromium.googlesource.com/v8/v8/+/refs/heads/main/src/builtins/typed-array-from.tq#193
[2] https://chromium.googlesource.com/v8/v8/+/refs/heads/main/src/builtins/typed-array-from.tq#201

fix: 
when storejsany, try to check it 
```
      if (typed_array_length == 0) {
        return Just<int64_t>(-1);
      }
``` 




### cl...@chromium.org (2023-03-06)

Detailed Report: https://clusterfuzz.com/testcase?key=4880213381677056

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7e8f00000000
Crash State:
  Builtins_StoreTypedElementJSAny_Int16Elements_0
  Builtins_TypedArrayFrom
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8&revision=86265

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4880213381677056

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-06)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>API Blink>JavaScript>Runtime]

### cl...@chromium.org (2023-03-06)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/a44a99a24cbcfae1a7843b096f465d0a122ca81a ([ext-code-space] Enable better code range allocation, #2).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### is...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-06)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-03-07)

Smallest repro:

const ab = new ArrayBuffer(1000, {"maxByteLength": 1000});
const ta = new Int16Array(ab);

function evil() {
  ab.resize(0);
}

function evilCtor() {
  return ta;
}

Float64Array.from.call(evilCtor, [0], evil);


### ma...@chromium.org (2023-03-07)

Afaics this is just writing to unmapped memory --> setting severity to low.

Thanks for the bug report, the fix is underway...

### gi...@appspot.gserviceaccount.com (2023-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/af52ed2ed3d56e7009330fa22383682c4fd4b816

commit af52ed2ed3d56e7009330fa22383682c4fd4b816
Author: Marja Hölttä <marja@chromium.org>
Date: Tue Mar 07 12:56:41 2023

[rab/gsab] Fix OOB buffer handling in %TypedArray%.from

Bug: v8:11111,chromium:1421451
Change-Id: I36e2ffcbc36207fda07757b5ed6ebe76e9eab51a
Fixed: chromium:1421451
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4315902
Auto-Submit: Marja Hölttä <marja@chromium.org>
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/main@{#86285}

[modify] https://crrev.com/af52ed2ed3d56e7009330fa22383682c4fd4b816/src/builtins/builtins-typed-array-gen.cc
[modify] https://crrev.com/af52ed2ed3d56e7009330fa22383682c4fd4b816/src/builtins/builtins-typed-array-gen.h
[modify] https://crrev.com/af52ed2ed3d56e7009330fa22383682c4fd4b816/src/builtins/typed-array-from.tq
[add] https://crrev.com/af52ed2ed3d56e7009330fa22383682c4fd4b816/test/mjsunit/regress/regress-crbug-1421451.js
[modify] https://crrev.com/af52ed2ed3d56e7009330fa22383682c4fd4b816/src/builtins/typed-array.tq


### cl...@chromium.org (2023-03-07)

ClusterFuzz testcase 4880213381677056 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=86284:86285

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-07)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-07)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-03-07)

[Comment Deleted]

### wh...@gmail.com (2023-03-10)

Hi, I tested current Stable channel version 

Google Chrome	111.0.5563.65 (Official Build) (64-bit) (cohort: 110_Win_Cotrol) 
Revision	c710e93d5b63b7095afe8c2c17df34408078439d-refs/branch-heads/5563@{#995}
OS	Windows 10 Version 22H2 (Build 19045.2604)
JavaScript	V8 11.1.277.13

v8 11.1.277.13 also impacted.

so, please add 
credit: Ganjiang Zhou(@refrain_areu) of ChaMd5-H1 team

Thanks.


### ma...@chromium.org (2023-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-10)

Merge rejected: M112 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-10)

Merge rejected: M111 is already shipping to stable and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wh...@gmail.com (2023-03-10)

[Empty comment from Monorail migration]

### ma...@chromium.org (2023-03-10)

Yes, this is happening on stable. I'll let the security team take it from here.

### va...@chromium.org (2023-03-13)

pbommana@ to PTAL and confirm that https://crbug.com/chromium/1421451#c24 is correct. Thanks

### am...@chromium.org (2023-03-13)

CF seems to find this only reproducible on head, based on the initial POC. Based on https://crbug.com/chromium/1421451#c26, updating Foundin- and SI-Stable. 
Re-adding merge request labels for 112 and 111. 
OP, it would be helpful to understand if this is still reproducing on M110, since that is current Extended Stable.

### pb...@google.com (2023-03-13)

Thank you Amy for taking a look.

### [Deleted User] (2023-03-13)

Merge rejected: M112 is already shipping to beta and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-13)

Merge rejected: M111 is already shipping to stable and this issue is marked as a Pri-2, Pri-3, or Type-Feature.

Please contact the milestone owner if you have questions.
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2023-03-13)

This won't repro in M110, because resizable arraybuffers are shipping only starting at M111.

### am...@chromium.org (2023-03-13)

sheriffbot is rejecting these merges still, it's because this issue is was originally marked high (OOB write) by CF, but was updated as a low severity issue as marja@. 
I hadn't noticed that when I checked in on this issue earlier. 

This an OOB write in the renderer would generally be considered a high severity, as with V8 there generally exists the possibility that such as issue could be exploited to result in RCE 
regarding https://crbug.com/chromium/1421451#c14,  
>>> Afaics this is just writing to unmapped memory --> setting severity to low
Can you relay how we are sure that this write will not allow for attacker control such as to result in a RCE. 

### ma...@chromium.org (2023-03-13)

In this special case we've unmapped the memory manually: https://source.chromium.org/chromium/chromium/src/+/main:v8/src/objects/backing-store.cc;l=626;bpv=1;bpt=1?q=backing-store.c&ss=chromium

So there's no real security risk here at the moment. I don't have a strong opinion about whether to merge the fix or not. It's more like a crash fix at the moment.

We've agreed to keep these as security bugs though; if we later implement moving the backing pointer of an ArrayBuffer, these bugs potentially turn into a real out of bounds read / write -> we want to catch them early.

### wh...@gmail.com (2023-03-14)

[Comment Deleted]

### wh...@gmail.com (2023-03-14)

[Comment Deleted]

### wh...@gmail.com (2023-03-14)

[Comment Deleted]

### wh...@gmail.com (2023-03-16)

[Comment Deleted]

### am...@chromium.org (2023-03-16)

No, we do not need to backmerge this fix. Based on https://crbug.com/chromium/1421451#c34 there are no current security implications from this issue. We'll leave this as low-severity based on our agreement to keep these as security bugs in light of potential future changes in V8, but we do not backmerge fixes for low severity issues. 

### wh...@gmail.com (2023-03-17)

Ok, thanks for the reply.

### wh...@gmail.com (2023-03-30)

ping, any update about reward?


### am...@google.com (2023-03-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-30)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-04-01)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-04-01)

[Comment Deleted]

### wh...@gmail.com (2023-04-01)

Hi, @amyressler, may I get bisect bonus with https://crbug.com/chromium/1421451#c3, and bisect should be right.

### wh...@gmail.com (2023-04-01)

[Comment Deleted]

### am...@chromium.org (2023-04-05)

Hello, thanks for reaching out about the bisect bonus. We've updated your reward amount with the $2,000 bisect bonus based on the information in https://crbug.com/chromium/1421451#c3 as well as the reproduction to validate the impact to Stable in https://crbug.com/chromium/1421451#c25. Your original $7,000 reward amount was already sent to finance for processing to the bisect bonus will follow as an additional separate payment of $2,000. 

### am...@google.com (2023-04-08)

[Empty comment from Monorail migration]

### wh...@gmail.com (2023-04-13)

Thanks.

### am...@chromium.org (2023-04-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-28)

There are no security implications from this issue as it stands presently or at the time of the report; removing release label.

### [Deleted User] (2023-06-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-13)

This issue was migrated from crbug.com/chromium/1421451?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063372)*
