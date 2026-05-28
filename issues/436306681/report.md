# [V8] Received signal 11 SEGV_ACCERR 794bb021ffe0

| Field | Value |
|-------|-------|
| **Issue ID** | [436306681](https://issues.chromium.org/issues/436306681) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Blink>JavaScript>Regexp, Blink>JavaScript>Runtime |
| **Platforms** | Linux, Mac |
| **Reporter** | rh...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2025-08-05 |
| **Bounty** | Confirmed (amount unknown) |

## Description

```
Received signal 11 SEGV_MAPERR 7ffcdfd3df00

==== C stack trace ===============================

../v8/v8/out/x64.build/d8(__interceptor_backtrace+0x46)[0x55b20ef35286]
/home/user/v8/v8/out/x64.build/libv8_libbase.so(_ZN2v84base5debug10StackTraceC2Ev+0x13)[0x7fb50020c0b3]
/home/user/v8/v8/out/x64.build/libv8_libbase.so(+0x94ebd)[0x7fb50020bebd]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x7fb4fe7b9330]
../v8/v8/out/x64.build/d8(__asan_poison_memory_region+0xd1)[0x55b20ef916e1]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal4Zone7AsanNewEm+0x121)[0x7fb5081f7381]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x4f4)[0x7fb507c2f8c4]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEiibPNS0_10RegExpTreeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeEb+0x7de)[0x7fb507c2fbae]
/home/user/v8/v8/out/x64.build/libv8.so(_ZN2v88internal16RegExpQuantifier6ToNodeEPNS0_14RegExpCompilerEPNS0_10RegExpNodeE+0x84)[0x7fb507c2f374]
[end of stack trace]
Segmentation fault

```
#### TESTCASE

```
let nested = "a";
for (let i = 0; i < 40000; i++) {
    nested = "(?:" + nested + ")+";
}

let regex = new RegExp(nested);
let result = regex.test("aaaaaaaaaa");

```
#### VERSION

V8 version 13.9.0 (candidate)

#### REPRODUCTION CASE

Build: `python3 tools/dev/gm.py x64.debug`

Run: `./d8 poc.js`

---

Reporter credit: Shaheen Fazim

## Timeline

### cl...@appspot.gserviceaccount.com (2025-08-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4505169446240256.

### 24...@project.gserviceaccount.com (2025-08-05)

ClusterFuzz testcase 4505169446240256 appears to be flaky, updating reproducibility hotlist.

### 24...@project.gserviceaccount.com (2025-08-05)

Detailed Report: https://clusterfuzz.com/testcase?key=4505169446240256

Fuzzer: None
Job Type: linux_asan_d8_v8_arm64_dbg
Platform Id: linux

Crash Type: Stack-overflow
Crash Address: 0x7ffd16b10f40
Crash State:
  v8::internal::RegExpQuantifier::ToNode
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_d8_v8_arm64_dbg&revision=101766

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4505169446240256

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### za...@google.com (2025-08-05)

Hi ishell@ can you please take a look at this v8 bug and triage? Tried to reproduce on clusterfuzzer but it couldn't reproduce it. Thanks.

### is...@chromium.org (2025-08-06)

Thank you for the report!

This is a stack overflow while computing `RegExpGroup::CaptureRegisters()` for a deeply recursed `RegEx`. It would be nice to fail gracefully instead of crashing.

This doesn't look like a security issue to me - either we manage to execute the call or we crash with a SEGFAULT.

### jg...@chromium.org (2025-08-08)

Given the regexp compiler's recursive implementation and that overflow protection is cobbled onto it, many such paths exist. Here's another recent example: [b/432385241](https://issues.chromium.org/issues/432385241).

While we still use this recursive compiler: I don't think it makes senses to sprinkle overflow checks around. We should either accept that such paths exist and will not cause problems in the real world since "real" patterns are not this large or deeply nested.

Or alternatively, add the stack check to every ToNode method.

### dx...@google.com (2025-08-18)

Project: v8/v8  

Branch:  main  

Author:  Jakob Linke [jgruber@chromium.org](mailto:jgruber@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6830053>

[regexp] Centralize stack overflow check in RegExp compiler

---


Expand for full commit details
```
     
    Previously, stack overflow checks were scattered in the RegExp compiler, 
    making it hard to ensure all paths were covered. 
     
    This CL centralizes the stack overflow check into a single chokepoint 
    in `RegExpTree::ToNode`. All `ToNode` methods with virtual dispatch are 
    renamed to `ToNodeImpl` and are called from `ToNode`. This ensures that 
    all paths are checked for stack overflows. 
     
    Bug: 436306681 
    Change-Id: I6d9b5260bd3856c72fbebfaf8cbed568d7824b22 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6830053 
    Auto-Submit: Jakob Linke <jgruber@chromium.org> 
    Commit-Queue: Patrick Thier <pthier@chromium.org> 
    Reviewed-by: Patrick Thier <pthier@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#101915}

```

---

Files:

- M `src/regexp/regexp-ast.h`
- M `src/regexp/regexp-compiler-tonode.cc`
- M `src/regexp/regexp-compiler.h`

---

Hash: [7ed79e45e7ad9dfdbfff87c46ca8b46fb52d03ad](https://chromiumdash.appspot.com/commit/7ed79e45e7ad9dfdbfff87c46ca8b46fb52d03ad)  

Date: Fri Aug 8 09:41:41 2025


---

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. As this appears to be a report of a functional issue, rather than a security issue, this report is unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-11-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. As this appears to be a report of a functional issue, rather than a security issue, this report is unfortunately not eligible for a Chrome VRP reward.
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.
> 
> Regards,
> Google Security Bot
> 
> 
> --
> How did we do? 

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/436306681)*
