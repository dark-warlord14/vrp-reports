# Debug check failed: has_latin1_bytecode().

| Field | Value |
|-------|-------|
| **Issue ID** | [447613219](https://issues.chromium.org/issues/447613219) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | pt...@chromium.org |
| **Created** | 2025-09-27 |
| **Bounty** | $7,000.00 |

## Description

COMMIT INFORMATION:

- Version: 102131
- Commit: 5652827a6073536b38e55c5cd52a6b25355c22d6
- Link: <https://crrev.com/5652827a6073536b38e55c5cd52a6b25355c22d6>

COMMIT MESSAGE:

```
commit 5652827a6073536b38e55c5cd52a6b25355c22d6
Author: pthier <pthier@chromium.org>
Date: Fri Aug 29 14:09:47 2025 +0200

[regexp] Assemble from BC: Check for exceptions

While assembling from bytecode itself doesn't throw exceptions,
compiling from source which might be called if we eagerly tiered-up can
throw. To prevent a double throw, check for exceptions when
CompileIrregexpFromBytecode returns false.

Bug: 437003349
Change-Id: I97d052e327c4b26748d40f8f6fb9efaa570069ce
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6891271
Reviewed-by: Jakob Linke <jgruber@chromium.org>
Commit-Queue: Patrick Thier <pthier@chromium.org>
Cr-Commit-Position: refs/heads/main@{#102131}


```

REPRODUCTION:

1. Download: `gs://v8-asan/linux-debug/d8-linux-debug-v8-component-102800.zip`
2. Run: `d8 --allow-natives-syntax --regexp-assemble-from-bytecode --fuzzing poc.js`

CRASH OUTPUT:

```
----------------------------------------


#
# Fatal error in ../../src/objects/js-regexp-inl.h, line 120
# Debug check failed: has_latin1_bytecode().
#
#
#
#FailureMessage Object: 0x7fffb6ef8980
==== C stack trace ===============================

/path/to/d8-linux-debug-v8-component-102800/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f87209f4bb3]
/path/to/d8-linux-debug-v8-component-102800/libv8_libplatform.so(+0x1b4ed) [0x7f872099b4ed]
/path/to/d8-linux-debug-v8-component-102800/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f87209d5a84]
/path/to/d8-linux-debug-v8-component-102800/libv8_libbase.so(+0x2d445) [0x7f87209d5445]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(v8::internal::IrRegExpData::bytecode(bool) const+0x170) [0x7f872574cee0]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(v8::internal::IrregexpInterpreter::Match(v8::internal::Isolate*, v8::internal::Tagged<v8::internal::IrRegExpData>, v8::internal::Tagged<v8::internal::String>, int*, int, int, v8::internal::RegExp::CallOrigin)+0x13c) [0x7f872574cb1c]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(v8::internal::IrregexpInterpreter::MatchForCallFromRuntime(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::IrRegExpData>, v8::internal::DirectHandle<v8::internal::String>, int*, int, int)+0xaf) [0x7f87257691ff]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(v8::internal::RegExpImpl::IrregexpExecRaw(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::IrRegExpData>, v8::internal::DirectHandle<v8::internal::String>, int, int*, int)+0xae6) [0x7f87257956d6]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(v8::internal::RegExpImpl::IrregexpExec(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::IrRegExpData>, v8::internal::DirectHandle<v8::internal::String>, int, int*, unsigned int)+0x535) [0x7f872578eb05]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(v8::internal::RegExp::Exec(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSRegExp>, v8::internal::DirectHandle<v8::internal::String>, int, int*, unsigned int)+0x23f) [0x7f872578e22f]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(v8::internal::RegExp::Exec_Single(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSRegExp>, v8::internal::DirectHandle<v8::internal::String>, int, v8::internal::DirectHandle<v8::internal::RegExpMatchInfo>)+0x254) [0x7f872578eff4]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(+0x4e9dd29) [0x7f872589dd29]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(+0x4e92118) [0x7f8725892118]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(v8::internal::Runtime_RegExpReplaceRT(int, unsigned long*, v8::internal::Isolate*)+0x84) [0x7f87258918a4]
/path/to/d8-linux-debug-v8-component-102800/libv8.so(+0x2b8e5bd) [0x7f872358e5bd]
Received signal 6

----------------------------------------

```

PoC:

```
function id(x) { return x; }

function main() {
  try { var s = id(""); } catch (e) {}
  try { s.replace(/bar\d\d/); } catch (e) {}
  try { main(); } catch (e) {}
  try { /bar\d\d/g; } catch (e) {}
  try { helper(); } catch (e) {}
}

function helper() {
  try { var s = id(""); } catch (e) {}
  try { var r = /bar\d\d/; } catch (e) {}
  try { s.replace(r, id("--$&--")); } catch (e) {}
  try { s += "\u1200"; } catch (e) {}
  try { s.replace(r); } catch (e) {}
}

try { main(); } catch (e) {}
// Flags: --allow-natives-syntax --regexp-assemble-from-bytecode --fuzzing

```

## Timeline

### je...@gmail.com (2025-09-27)

SEGV in Release, so it should be S1.

```
/home/sakura/v8/v8/out/x64.release/d8 --allow-natives-syntax --regexp-assemble-from-bytecode --fuzzing poc.js

Received signal 11 SEGV_ACCERR 2f0300000007

==== C stack trace ===============================

/home/sakura/v8/v8/out/x64.release/d8(_ZN2v84base5debug10StackTraceC1Ev+0x13)[0x5634e778d6b3]
/home/sakura/v8/v8/out/x64.release/d8(+0x2d5060f)[0x5634e778d60f]
/lib/x86_64-linux-gnu/libc.so.6(+0x42520)[0x7fdf2a842520]
/home/sakura/v8/v8/out/x64.release/d8(+0x1c61585)[0x5634e669e585]
/home/sakura/v8/v8/out/x64.release/d8(_ZN2v88internal19IrregexpInterpreter13MatchInternalEPNS0_7IsolateEPNS0_6TaggedINS0_16TrustedByteArrayEEEPNS4_INS0_6StringEEEPiiiiNS0_6RegExp10CallOriginEj+0x27f)[0x5634e669e43f]
/home/sakura/v8/v8/out/x64.release/d8(_ZN2v88internal19IrregexpInterpreter5MatchEPNS0_7IsolateENS0_6TaggedINS0_12IrRegExpDataEEENS4_INS0_6StringEEEPiiiNS0_6RegExp10CallOriginE+0x124)[0x5634e669e154]
/home/sakura/v8/v8/out/x64.release/d8(_ZN2v88internal19IrregexpInterpreter23MatchForCallFromRuntimeEPNS0_7IsolateENS0_12DirectHandleINS0_12IrRegExpDataEEENS4_INS0_6StringEEEPiii+0x1a)[0x5634e66a222a]
/home/sakura/v8/v8/out/x64.release/d8(_ZN2v88internal10RegExpImpl15IrregexpExecRawEPNS0_7IsolateENS0_12DirectHandleINS0_12IrRegExpDataEEENS4_INS0_6StringEEEiPii+0xbb)[0x5634e66bdadb]
/home/sakura/v8/v8/out/x64.release/d8(_ZN2v88internal10RegExpImpl12IrregexpExecEPNS0_7IsolateENS0_12DirectHandleINS0_12IrRegExpDataEEENS4_INS0_6StringEEEiPij+0x17c)[0x5634e66bb05c]
/home/sakura/v8/v8/out/x64.release/d8(_ZN2v88internal6RegExp4ExecEPNS0_7IsolateENS0_12DirectHandleINS0_8JSRegExpEEENS4_INS0_6StringEEEiPij+0xa0)[0x5634e66bae70]
/home/sakura/v8/v8/out/x64.release/d8(_ZN2v88internal6RegExp11Exec_SingleEPNS0_7IsolateENS0_12DirectHandleINS0_8JSRegExpEEENS4_INS0_6StringEEEiNS4_INS0_15RegExpMatchInfoEEE+0xb8)[0x5634e66bb288]
/home/sakura/v8/v8/out/x64.release/d8(+0x1ce2f2d)[0x5634e671ff2d]
/home/sakura/v8/v8/out/x64.release/d8(_ZN2v88internal23Runtime_RegExpReplaceRTEiPmPNS0_7IsolateE+0xd6)[0x5634e671a056]
/home/sakura/v8/v8/out/x64.release/d8(+0x2bf1ef6)[0x5634e762eef6]
[end of stack trace]
[1]    2412763 segmentation fault  /home/sakura/v8/v8/out/x64.release/d8 --allow-natives-syntax  --fuzzing 


```

### aj...@google.com (2025-09-29)

Hello - please provide symbolized stacks (ideally asan traces) with your reports - this makes triage much easier!

### aj...@google.com (2025-09-29)

Note - you have provided an experimental feature flag please include all d8 output in your reports!

```
D:\chromium\src [(9d5a15a...)]> .\out\asan\d8.exe --allow-natives-syntax --regexp-assemble-from-bytecode --fuzzing D:\pocs\jlulu-447613219\poc.js
V8 is running with experimental features enabled. Stability and security will suffer.
=================================================================
==21412==ERROR: AddressSanitizer: access-violation on unknown address 0x015b00000007 (pc 0x7ff620e5e08f bp 0x00204910f2e0 sp 0x00204910f260 T0)
==21412==The signal is caused by a READ memory access.
==21412==*** WARNING: Failed to initialize DbgHelp!              ***
==21412==*** Most likely this means that the app is already      ***
==21412==*** using DbgHelp, possibly with incompatible flags.    ***
==21412==*** Due to technical reasons, symbolization might crash ***
==21412==*** or produce wrong results.                           ***
    #0 0x7ff620e5e08e in v8::internal::`anonymous namespace'::RawMatch<unsigned char> D:\chromium\src\v8\src\regexp\regexp-interpreter.cc:476:5
    #1 0x7ff620e5d886 in v8::internal::IrregexpInterpreter::MatchInternal(class v8::internal::Isolate *, class v8::internal::Tagged<class v8::internal::TrustedByteArray> *, class v8::internal::Tagged<class v8::internal::String> *, int *, int, int, int, enum v8::internal::RegExp::CallOrigin, unsigned int) D:\chromium\src\v8\src\regexp\regexp-interpreter.cc:1210:12
    #2 0x7ff620e5cd8c in v8::internal::IrregexpInterpreter::Match(class v8::internal::Isolate *, class v8::internal::Tagged<class v8::internal::IrRegExpData>, class v8::internal::Tagged<class v8::internal::String>, int *, int, int, enum v8::internal::RegExp::CallOrigin) D:\chromium\src\v8\src\regexp\regexp-interpreter.cc:1146:27
    #3 0x7ff620e70601 in v8::internal::IrregexpInterpreter::MatchForCallFromRuntime(class v8::internal::Isolate *, class v8::internal::DirectHandle<class v8::internal::IrRegExpData>, class v8::internal::DirectHandle<class v8::internal::String>, int *, int, int) D:\chromium\src\v8\src\regexp\regexp-interpreter.cc:1270:10
    #4 0x7ff620f023f0 in v8::internal::RegExpImpl::IrregexpExecRaw(class v8::internal::Isolate *, class v8::internal::DirectHandle<class v8::internal::IrRegExpData>, class v8::internal::DirectHandle<class v8::internal::String>, int, int *, int) D:\chromium\src\v8\src\regexp\regexp.cc:979:20
    #5 0x7ff620ef54a9 in v8::internal::RegExpImpl::IrregexpExec(class v8::internal::Isolate *, class v8::internal::DirectHandle<class v8::internal::IrRegExpData>, class v8::internal::DirectHandle<class v8::internal::String>, int, int *, unsigned int) D:\chromium\src\v8\src\regexp\regexp.cc:1068:13
    #6 0x7ff620ef4e49 in v8::internal::RegExp::Exec(class v8::internal::Isolate *, class v8::internal::DirectHandle<class v8::internal::JSRegExp>, class v8::internal::DirectHandle<class v8::internal::String>, int, int *, unsigned int) D:\chromium\src\v8\src\regexp\regexp.cc:357:14
    #7 0x7ff620ef61bb in v8::internal::RegExp::Exec_Single(class v8::internal::Isolate *, class v8::internal::DirectHandle<class v8::internal::JSRegExp>, class v8::internal::DirectHandle<class v8::internal::String>, int, class v8::internal::DirectHandle<class v8::internal::RegExpMatchInfo>) D:\chromium\src\v8\src\regexp\regexp.cc:384:7
    #8 0x7ff62107f9d2 in v8::internal::`anonymous namespace'::RegExpReplace D:\chromium\src\v8\src\runtime\runtime-regexp.cc:1475:7
    #9 0x7ff621069912 in v8::internal::Runtime_RegExpReplaceRT(int, unsigned __int64 *, class v8::internal::Isolate *) D:\chromium\src\v8\src\runtime\runtime-regexp.cc:1910:1

```

### aj...@google.com (2025-09-29)

tentatively setting labels - v8 folks please add to None hotlist or turn into a bug if the flags above are not currently in scope

### je...@gmail.com (2025-09-29)

My fuzz won't fuzz experimental flags. It hasn't been experimental since last week. Please update your local v8.

```
[regexp] Mark --regexp-assemble-from-bytecode non-experimental

Assembling RegExp from bytecode is now feature complete, so it is not
considered experimental anymore.

```

<https://source.chromium.org/chromium/_/chromium/v8/v8/+/78867e361f3495857778f7e063181f9e3c6cc1e0>
<https://source.chromium.org/chromium/chromium/src/+/main:v8/src/flags/flag-definitions.h;l=3088>

### je...@gmail.com (2025-09-29)

Additionally, this is a release segv, and it should be S1

### je...@gmail.com (2025-09-30)

Hi, team, can you upload it to clusterfuzzer? It should be able to automatically assign it to the appropriate owner.

### cl...@appspot.gserviceaccount.com (2025-09-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6432128904396800.

### 24...@project.gserviceaccount.com (2025-09-30)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-09-30)

Detailed Report: https://clusterfuzz.com/testcase?key=6432128904396800

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  has_latin1_bytecode() in js-regexp-inl.h
  v8::internal::IrRegExpData::bytecode
  v8::internal::IrregexpInterpreter::Match
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=102130:102131

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6432128904396800

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ch...@google.com (2025-09-30)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-09-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-09-30)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ta...@google.com (2025-09-30)

Hi pthier@, could you please take a look at this DCHECK failure?

### pt...@chromium.org (2025-09-30)

This is behind an off-by-default flag and should therefore be marked as `SecurityImpact_None` and `ReleaseBlock` removed.

tacet@ Can you please update the hotlist?

### dx...@google.com (2025-10-02)

Project: v8/v8  

Branch:  main  

Author:  pthier [pthier@chromium.org](mailto:pthier@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6999673>

[regexp] Pass compilation target as argument to CompileFromSource

---


Expand for full commit details
```
     
    For assembling JIT-code from bytecode we might need to force bytecode 
    compilation, if we forcefully tier-up (e.g. for global RegExp or long 
    subject strings we don't want to run the interpreter). 
    Previously we reset the tier-up ticks to force bytecode compilation, but 
    this is brittle in case of errors during compilation. 
     
    Fixed: 447613219 
    Bug: 437003349 
    Change-Id: Idf96ef84706ad40e5d97b639e68188aae63f0151 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6999673 
    Reviewed-by: Jakob Linke <jgruber@chromium.org> 
    Auto-Submit: Patrick Thier <pthier@chromium.org> 
    Commit-Queue: Jakob Linke <jgruber@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102883}

```

---

Files:

- M `src/regexp/regexp.cc`
- A `test/mjsunit/regress/regress-447613219.js`

---

Hash: [c8b2aeec5dfe2c1d579ec612a82518a704f559a6](https://chromiumdash.appspot.com/commit/c8b2aeec5dfe2c1d579ec612a82518a704f559a6)  

Date: Wed Oct 1 07:51:52 2025


---

### 24...@project.gserviceaccount.com (2025-10-03)

ClusterFuzz testcase 6432128904396800 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=102887:102888

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### sp...@google.com (2025-10-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Baseline renderer memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-01-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline renderer memory corruption in a sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/447613219)*
