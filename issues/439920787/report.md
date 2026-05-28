# Controlled memory corruption leading to segmentation fault in V8 locale validation due to argument mismatch in blink caller

| Field | Value |
|-------|-------|
| **Issue ID** | [439920787](https://issues.chromium.org/issues/439920787) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2025-08-19 |
| **Bounty** | Confirmed (amount unknown) |

## Description

---

### Report description

Controlled memory corruption leading to segmentation fault in V8 locale validation due to argument mismatch in blink caller

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

local

---

### The problem

#### Please describe the technical details of the vulnerability

I am uploading LLDB debug results and the Javascript to trigger the bug below, I might be wrong in pinpointing the exact cause of the bug I tried my best:

There is a bug in the function blink::ValidateAndCanonicalizeBCP47Languages (or its caller). This function is responsible for preparing arguments to call the V8 API function v8::Isolate::ValidateAndCanonicalizeUnicodeLocaleId :

-A segmentation fault occurs during the validation of BCP47 language tags in Blink, specifically when blink::ValidateAndCanonicalizeBCP47Languages calls v8::Isolate::ValidateAndCanonicalizeUnicodeLocaleId. The arguments are swapped in the call site, leading to invalid memory accesses.

-In frame 2 (blink::ValidateAndCanonicalizeBCP47Languages at +285), the loop (starting at +217) prepares arguments for the call but swaps them:%rdi is set to a stack address,
%rsi is set to the Isolate\* from %rbx in frame 2.

The call invokes frame 1 v8::Isolate::ValidateAndCanonicalizeUnicodeLocaleId :

on frame 1 :
-%rdi (stack address) is stored in %rbx (invalid for isolate\*).

-%rsi (actual isolate\*) is treated as the string\_view.data(), but the assembly incorrectly accesses isolate offsets on %rsi (e.g., 0x230(%rsi), 0x238(%rsi), 0x240(%rsi)).

-this mismatches the expected behavior: the assembly appears to treat %rsi as the Isolate\* (setting up CallDepthScope), while %rdi is ignored for that purpose.

*The expected convention is %rdi = isolate*, %rsi = string data pointer, %rdx = string length. Instead, %rsi = isolate\*, %rdx = string data, and %rdi is left as -0x70(%rbp) (a stack address). This swaps the this pointer and string data, passing a stack address as the "isolate" and the isolate\* as the "string data".

Later on frame 0 :

The corruption happens in earlier frames and remains dormant until it manifests in the destructor of the v8::CallDepthScope object :

-The destructor reads a pointer from the corrupted Isolate memory at a fixed offset (isolate+0x150).

-This pointer, now overwritten with data from our crafted string (e.g., 0x41414141), is dereferenced at an offset (0x4bb) to load a value.

-This value is used as an index (shrl $0x6, %ecx) and combined with another corrupted pointer from isolate+0x268 to calculate a read address: movq (%rdx,%rcx,8), %rcx.

-This calculated address can be invalid and unmapped if the string data used results in a high offset, causing a segmentation fault. Or, it can be a valid, mapped address which would very likely result in a ud2 intentional crash from chrome because the valid address would not contain the necessary bit check value chrome expects. A third alternative is if a potential malicious actor controls the value of where chrome would read and place the exact bit value chrome is expecting, then, he would achieve a much severe impact than what I am currently demonstrating.

Some notes :

-our controlled string value, lets say "A" is 41 in ASCII, so in frame 0 when you check RCX you will see rcx = 0x0000000001050505 this is what we currently control at this state, this comes from <+27>: shrl $0x6, %ecx so 0x41414141 >> 6 = 0x1050505, the string length determines how much of our own value will be written and used beyond the index offset at frame 0 so with an ASLR bypass this becomes a critical vulnerability

-\*\*\*the bug is only present on (x86\_64) systems ( mac and windows ), not on ARM systems

-based on the assemble, if I am not wrong, if an attacker can place the necessary bit check value from where the attacker makes chrome read, he would have additional primitives that would potentially allow him to write on native C++ layer which would grant him extensive control on native layer potentially leading to code execution.

I have uploaded to different Javascript, one uses the translator, the other uses the summarizer API as both have access to the necessary code paths; just run the html and it will crash.

Furthermore I have attached two LLDB debugs, one shows a huge index which causes segfault and invalid memory read, and one is with an acceptable value that yields an index/offset that would read from a valid memory ( but still yield a ud2 crash due to the missing bit check ).

I also want to note that if you attach LLDB or alike on a live renderer you will see that on frame 7 JIT is involved, I am not sure but it might have an effect on the bug.

I hope the details above have been helpful, if you need anything else from let me know.

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

This can be deployed via HTML on an attacker controlled website - anyone who visits the page will be affected , currently controlled memory corruption leading to guaranteed DoS, if paired with an ASLR bypass then it would very likely lead to remote code execution

---

### The cause

#### What version of Chrome have you found the security issue in?

Version 139.0.7258.128 (Official Build) (x86\_64)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

iGnosis

## Attachments

- [Large Offset_EXC_BAD_ACCESS.txt](attachments/Large Offset_EXC_BAD_ACCESS.txt) (text/plain, 11.7 KB)
- [Valid Offset_EXC_BREAKPOINT.txt](attachments/Valid Offset_EXC_BREAKPOINT.txt) (text/plain, 12.1 KB)
- [summarizer.html](attachments/summarizer.html) (text/html, 476 B)
- [translator.html](attachments/translator.html) (text/html, 475 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-08-19)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4563782516801536.

### 24...@project.gserviceaccount.com (2025-08-20)

Detailed Report: https://clusterfuzz.com/testcase?key=4563782516801536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x78cdb9d4e820
Crash State:
  v8::Isolate::ValidateAndCanonicalizeUnicodeLocaleId
  blink::ValidateAndCanonicalizeSourceAndTargetLanguages
  blink::Translator::create
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1503674

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4563782516801536

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ch...@google.com (2025-08-20)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@chromium.org (2025-08-20)

I would have ordinarily assigned this to syg@ on the V8 side, but since he's no longer here assigning to clemensb@

### am...@chromium.org (2025-08-20)

also cc'ing btriebw@ and memmott@ based on recent work with language tags

### bt...@chromium.org (2025-08-20)

Assigning to myself to investigate and fix

### am...@chromium.org (2025-08-20)

Setting speculative found-in to current extended stable as I'm not seeing any more recent code changes that might have resulted in this issue; please update found-in if this is incorrect

### me...@gmail.com (2025-08-20)

hi again, i have experimented with the bug to explore its exploitability further,

i have only managed to trigger the bug with a race condition combined with destruction, without the destruction and without the race i am not yet able to reproduce the bug. Nevertheless it is consistently reproducible via the HTML's/Javascript(s) I provided.

furthermore, an attacker can exploit the string in a controlled way; for example : the length will determine how much of our custom values will be potentially written and used on native layer, and the string content ( aka our controlled writes ) can be multi layered ( ie custom value + custom value + custom value........... )

best regards,

iG

### bt...@chromium.org (2025-08-20)

Re assigning to clemensb. I'm able to reproduce this, but I don't see anything wrong in `ValidateAndCanonicalizeBCP47Languages` specifically. Since the crash seems related to `EnterV8NoScriptScope` it seems like a potential V8 bug.

### ch...@google.com (2025-08-21)

Setting milestone because of s0/s1 severity.

### cl...@chromium.org (2025-08-25)

I am just returning from vacation, and still have plenty of other stuff to look into. I am not sure why this was assigned to me.
Assigning to the current sheriff. Please assign back if this has any relation to any of my projects or CLs.

### me...@gmail.com (2025-08-26)

am I allowed to exploit this further? 


### 24...@project.gserviceaccount.com (2025-08-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2025-08-26)

Detailed Report: https://clusterfuzz.com/testcase?key=4563782516801536

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x78cdb9d4e820
Crash State:
  v8::Isolate::ValidateAndCanonicalizeUnicodeLocaleId
  blink::ValidateAndCanonicalizeSourceAndTargetLanguages
  blink::Translator::create
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1472012:1472029

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4563782516801536

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### is...@chromium.org (2025-08-26)

Thank you for the report! Nice catch!

The fix is on the way.

### is...@chromium.org (2025-08-27)

**TL;DR;**: The POC demonstrates type confusion between `NativeContext` and `ModuleContext` when loading a `MicrotaskQueue` pointer which is not a security issue because

1. V8 Sandbox guarantees that the pointer is either valid `MicrotaskQueue` pointer (but potentially belonging to some other `NativeContext`) or it'd cause a SEGFAULT on dereference or it'd crash during reading the value from the external pointer table,
2. the `MicrotaskQueue` pointer is not actually used on the code path in question.

# Details

The type confusion happens [here](https://source.chromium.org/chromium/chromium/src/+/2978d7757169ad7f72c90c8d9b25336423e4afdf:v8/src/api/api-inl.h;l=171?q=%22i::Cast%3Ci::NativeContext%3E(isolate_-%3Econtext())%22&ss=chromium) when V8 loads microtask queue pointer from current context which happens to be `ModuleContext` instead of `NativeContext` as expected.

This happens when a module calls an Api function which in turn calls `v8::Isolate::ValidateAndCanonicalizeUnicodeLocaleId()` and the Api call is compiled with Maglev.

The reasons are

1. When generating call to Api function Maglev passes current context (`ModuleContext`) instead of `NativeContext`,
2. `Isolate::ValidateAndCanonicalizeUnicodeLocaleId()` uses `EnterV8NoScriptScope<> api_scope` which doesn't re-set the context to the current `NativeContext` and the current context still contains `ModuleContext`.

# Why not a security issue?

1. Although POC allows to fake external pointer handle representing `NativeContext`'s `MicrotaskQueue` pointer, the V8 Sandbox guarantees that
   
   either
   
   a) there would be a SEGFAULT when reading from external pointer table using invalid handle,
   
   or
   
   b) the external pointer read from the external pointer table is a pointer to a valid `MicrotaskQueue` object (potentially belonging to some other `NativeContext`),
   
   or
   
   c) the external pointer read from the external pointer table is an invalid pointer which will cause a SEGFAULT on dereference.
2. The `MicrotaskQueue` pointer is eagerly computed but it's not used for the `ValidateAndCanonicalizeUnicodeLocaleId()` case (`do_callback` is false [here](https://source.chromium.org/chromium/chromium/src/+/2978d7757169ad7f72c90c8d9b25336423e4afdf:v8/src/api/api-inl.h;l=183?q=%22i::Cast%3Ci::NativeContext%3E(isolate_-%3Econtext())%22&ss=chromium)).
3. And even if the [FireCallCompletedCallback(microtask\_queue);](https://source.chromium.org/chromium/chromium/src/+/2978d7757169ad7f72c90c8d9b25336423e4afdf:v8/src/api/api-inl.h;l=183?q=%22i::Cast%3Ci::NativeContext%3E(isolate_-%3Econtext())%22&ss=chromium) is called for some other `NativeContext`'s microtask queue it would be a correctness issue.

Thus, I'm updating security labels.

# Fix

1. Make sure Maglev always passes NativeContext when generating calls to Api functions (to match Turbofan behaviour).
2. Make `CallDepthScope` class compute microtask queue pointer only when necessary.
3. Make `CallDepthScope` class always compute NativeContext when loading microtask queue.

### me...@gmail.com (2025-08-27)

We can control the index via our Javascript string, in our example rcx = 0x0000000001050505  comes from <+27>: shrl $0x6, %ecx so 0x41414141 >> 6 = 0x1050505. The string from Javascript in the example of summarizer = sourceLanguage: 'A'.repeat(2000), we can customize it and determine the length as we wish, which has impact on the native layer of Chrome as seen in the crash above. This is not enough to deem it exploitable? 

### is...@chromium.org (2025-08-27)

I'm afraid that this particular SEGFAULT is not exploitable.

The assembly code you are referring to comes from [ExternalPointerTable::Get()](https://source.chromium.org/chromium/chromium/src/+/main:v8/src/sandbox/external-pointer-table-inl.h;l=174?q=%22ExternalPointerTable::Get%22&ss=chromium%2Fchromium%2Fsrc). `rcx` value `0x1050505` is the value of the `index` into the external pointer table.

See [this comment](https://source.chromium.org/chromium/chromium/src/+/main:v8/include/v8-internal.h?q=%22%2F%2F%20The%20external%20pointer%20table%20indices%20stored%20in%20HeapObjects%20as%20external%22&ss=chromium%2Fchromium%2Fsrc) explaining how shift amount and external pointer table reservation size guarantees safety.

**TL;DR;**: it's possible to read some value from some other entry via "corrupting" or "constructing" an external pointer handle value but the actual pointer read from external pointer table would either be unusable (causing SEGFAULT on dereference) or it'd be a pointer to another object with the same tag (in our case pointer to another `MicrotaskQueue` object), which in this particular case is fine, see the explanation above.

Please see [the blog post](https://v8.dev/blog/sandbox) explaining how V8 Sandbox works.

### me...@gmail.com (2025-08-27)

Alright, thank you

### dx...@google.com (2025-08-28)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6890032>

[maglev][api] Use NativeContext when calling Api functions

---


Expand for full commit details
```
     
    Drive-by: 
     - make sure that CallDepthScope loads MicrotaskQueue pointer 
       from native context and only when necessary, 
     - remove context argument from CallKnownApiFunction node and 
       use current native context instead (which is guaranteed to match 
       Api function's native context since we don't inline Api calls 
       cross native context), 
     - simplify generation of CallKnownApiFunction nodes by using 
       __ CallBuiltin<Builtin>(...). 
     
    Fixed: 439920787 
    Change-Id: Iea58e378c35de1298bb7c4c1aed22066ff3989bc 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6890032 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102090}

```

---

Files:

- M `src/api/api-inl.h`
- M `src/compiler/turboshaft/turbolev-graph-builder.cc`
- M `src/maglev/maglev-assembler-inl.h`
- M `src/maglev/maglev-graph-builder.cc`
- M `src/maglev/maglev-ir.cc`
- M `src/maglev/maglev-ir.h`

---

Hash: [56a98f13a05706e3e0db5611ed82622d3ede7d5c](https://chromiumdash.appspot.com/commit/56a98f13a05706e3e0db5611ed82622d3ede7d5c)  

Date: Thu Aug 28 08:44:03 2025


---

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
Thank you for the report. As this issue is not an exploitable security issue resulting in security consequences for a user, this issue is unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### 24...@project.gserviceaccount.com (2025-08-29)

ClusterFuzz testcase 4563782516801536 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1507757:1507764

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2025-12-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you for the report. As this issue is not an exploitable security issue resulting in security consequences for a user, this issue is unfortunately not eligible for a Chrome VRP reward.
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.
> 
> Regards,
> Google Security Bot
> 
> 
> --
> Ho

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/439920787)*
