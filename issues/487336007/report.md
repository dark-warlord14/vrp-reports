# Detached ArrayBuffer UAF after AB view tracking was enabled

| Field | Value |
|-------|-------|
| **Issue ID** | [487336007](https://issues.chromium.org/issues/487336007) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 147.0.7703.0 |
| **Reporter** | er...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2026-02-25 |
| **Bounty** | $8,000.00 |

## Description

##### VULNERABILITY DETAILS

`track_array_buffer_views` was an experimental feature which was enabled in the bisected commit, due to this feature not correctly invalidating ArrayBuffers detaching protectors, an
optimized typed element access can skip detach checks and operate on the stale array, resulting in a UAF on backing store memory.

##### VERSION

V8 Git Commit: `8ac940a79a3b6daebaa76dc3d2f8da12f7c19445`

##### REPRODUCTION CASE

The first poc shows the UAF behaviour by using the detached dangling typed array to modify a separate typed array's elements.

`d8 --allow-natives-syntax --expose-gc poc.js`

```
UAF in round 1
100 should have been 50

```

The second poc attempts to produce a SIGSEGV by making the allocator map the freed backing-store as PROT\_NONE prior to the access (May not be 100% reliable).

`d8 --allow-natives-syntax --expose-gc poc_crash.js`

```
progress 0 probe undefined
progress 16 probe undefined
progress 32 probe undefined
progress 48 probe undefined
progress 64 probe undefined
progress 80 probe undefined
Received signal 11 SEGV_ACCERR 7eaf00200000

==== C stack trace ===============================

./d8(___interceptor_backtrace+0x46)[0x5ab1e36919f6]
./d8(+0x64277c0)[0x5ab1e86e97c0]
/lib/x86_64-linux-gnu/libc.so.6(+0x45330)[0x7d1868c45330]
[0x5ab1ba200a62]
[end of stack trace]
Segmentation fault

```
##### Bisect

```
commit f9ed920568c5c91d33692998ec52387b7cb7361f
Author: Olivier Flückiger <olivf@chromium.org>
Date:   Mon Feb 23 15:48:08 2026 +0100

    [array-buffer] Enable AB view tracking
    
    Bug: 467645277
    Change-Id: I15d457da120d528449c65935d2c641b2c8f2eef3
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7600434
    Reviewed-by: Marja Hölttä <marja@chromium.org>
    Commit-Queue: Marja Hölttä <marja@chromium.org>
    Auto-Submit: Olivier Flückiger <olivf@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#105400}

```
##### CREDIT INFORMATION

Reporter credit: Erge

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 789 B)
- [poc_crash.js](attachments/poc_crash.js) (text/javascript, 733 B)
- [reliable_crash.js](attachments/reliable_crash.js) (text/javascript, 556 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5325523106332672.

### aj...@google.com (2026-02-25)

poc\_crash indeed crashes. Sending to the v8 rotation for further analysis.

```
D:\chromium\src\out\asan [(2914485...)]> .\d8.exe --allow-natives-syntax --expose-gc D:\pocs\everything-487336007\poc_crash.js
progress 0 probe undefined
progress 16 probe undefined
progress 32 probe undefined
=================================================================
==34348==ERROR: AddressSanitizer: access-violation on unknown address 0x136400200000 (pc 0x7ff6e00414f2 bp 0x00fc033fef50 sp 0x00fc033feea0 T0)
==34348==The signal is caused by a WRITE memory access.
==34348==*** WARNING: Failed to initialize DbgHelp!              ***
==34348==*** Most likely this means that the app is already      ***
==34348==*** using DbgHelp, possibly with incompatible flags.    ***
==34348==*** Due to technical reasons, symbolization might crash ***
==34348==*** or produce wrong results.                           ***
    #0 0x7ff6e00414f1  (<unknown module>)
    #1 0x7ff685701b5b in Builtins_JSEntryTrampoline (D:\chromium\src\out\asan\d8.exe+0x146b21b5b)
    #2 0x7ff6857016be in Builtins_JSEntry (D:\chromium\src\out\asan\d8.exe+0x146b216be)
    #3 0x7ff67f5ddc35 in v8::internal::`anonymous namespace'::Invoke D:\chromium\src\v8\src\execution\execution.cc:442:22
    #4 0x7ff67f5e1291 in v8::internal::Execution::CallScript(class v8::internal::Isolate *, class v8::internal::DirectHandle<class v8::internal::JSFunction>, class v8::internal::DirectHandle<class v8::internal::Object>, class v8::internal::DirectHandle<class v8::internal::Object>) D:\chromium\src\v8\src\execution\execution.cc:542:10
    #5 0x7ff67ef83044 in v8::Script::Run(class v8::Local<class v8::Context>, class v8::Local<class v8::Data>) D:\chromium\src\v8\src\api\api.cc:2031:7
    #6 0x7ff67ec2e085 in v8::Shell::ExecuteString(class v8::Isolate *, class v8::Local<class v8::String>, class v8::Local<class v8::String>, enum v8::Shell::ReportExceptions, class v8::Global<class v8::Value> *) D:\chromium\src\v8\src\d8\d8.cc:1039:44
    #7 0x7ff67ec89ecf in v8::SourceGroup::Execute(class v8::Isolate *) D:\chromium\src\v8\src\d8\d8.cc:5661:10
    #8 0x7ff67ec995e8 in v8::Shell::RunMainIsolate(class v8::Isolate *, bool) D:\chromium\src\v8\src\d8\d8.cc:6680:37
    #9 0x7ff67ec9877c in v8::Shell::RunMain(class v8::Isolate *, bool) D:\chromium\src\v8\src\d8\d8.cc:6588:18
    #10 0x7ff67ec9db95 in v8::Shell::Main(int, char **const) D:\chromium\src\v8\src\d8\d8.cc:7502:18
    #11 0x7ff68590427f in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #12 0x7ffb0c52e8d6  (C:\WINDOWS\System32\KERNEL32.DLL+0x18002e8d6)
    #13 0x7ffb0c92c40b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18008c40b)

==34348==Register values:
rax = 136100000011  rbx = 13610101d2c9  rcx = 3e299df8fb96  rdx = 1361010800ad
rdi = 3c  rsi = 136101004609  rbp = fc033fef50  rsp = fc033feea0
r8  = 0  r9  = 100d1bd  r10 = 7ffb09cb0000  r11 = 0
r12 = 136400200000  r13 = 1339293a1080  r14 = 136100000000  r15 = 0
AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: access-violation (<unknown module>)
==34348==ABORTING

```

Tentatively setting severity High.

Note that <https://chromiumdash.appspot.com/commit/f9ed920568c5c91d33692998ec52387b7cb7361f> only landed recently and we discourage hunting for bugs on HEAD to allow our fuzzers time to find issues.

### 24...@project.gserviceaccount.com (2026-02-25)

Detailed Report: https://clusterfuzz.com/testcase?key=5325523106332672

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7eae00200041
Crash State:
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  v8::internal::Invoke
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=105399:105400

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5325523106332672

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### er...@gmail.com (2026-02-25)

> Note that <https://chromiumdash.appspot.com/commit/f9ed920568c5c91d33692998ec52387b7cb7361f> only landed recently and we discourage hunting for bugs on HEAD to allow our fuzzers time to find issues.

My bad, I was under the impression that relatively older experimental features getting "released" on HEAD were eligible for reports.

For what it's worth I minimized the crashing poc, it should be reliable now.

### ch...@google.com (2026-02-25)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2026-02-25)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ol...@chromium.org (2026-02-26)

Thanks for the report. That was actually my fault for not correctly going through the correct stages for the flag.

### ol...@chromium.org (2026-02-26)

reverted in <https://chromiumdash.appspot.com/commit/a5fa6213e8e7733b283fa14f7c602abb3ea6d572>

### 24...@project.gserviceaccount.com (2026-02-27)

ClusterFuzz testcase 5325523106332672 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=105464:105465

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### dx...@google.com (2026-03-09)

Project: v8/v8  

Branch:  main  

Author:  Olivier Flückiger [olivf@chromium.org](mailto:olivf@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7613531>

[array-buffer] Fix AB view tracking issues

---


Expand for full commit details
```
     
    * Set both length fields to 0 
    * Handle view proto with monkey-patched length property 
    * Support build length on detached buffers (avoids dcheck on races) 
     
    Fixed: 487336007 
    Fixed: 487468464 
    Change-Id: Ic81e8527cd7a6197ffacc60952d713cb9a2580f4 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7613531 
    Reviewed-by: Darius Mercadier <dmercadier@chromium.org> 
    Commit-Queue: Olivier Flückiger <olivf@chromium.org> 
    Auto-Submit: Olivier Flückiger <olivf@chromium.org> 
    Reviewed-by: Marja Hölttä <marja@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105663}

```

---

Files:

- M `src/builtins/builtins-array-gen.cc`
- M `src/compiler/heap-refs.cc`
- M `src/objects/js-array-buffer.cc`
- A `test/mjsunit/regress/regress-487468464.js`
- A `test/mjsunit/regress/regress-487857171.js`

---

Hash: [64e4086db066df99332c34332aa7fa5684e1a93f](https://chromiumdash.appspot.com/commit/64e4086db066df99332c34332aa7fa5684e1a93f)  

Date: Thu Feb 26 20:13:40 2026


---

### ch...@google.com (2026-03-11)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
**Merge approved:** your change passed merge requirements and is auto-approved for M147. Please go ahead and merge the CL to branch 7727 (refs/branch-heads/7727) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [147].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ol...@chromium.org (2026-03-11)

No merge needed. The feature is disabled in 147.

### ch...@google.com (2026-03-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2026-03-19)

Please merge your change to M147 by 2:00 PM PT today so we can take it in for tomorrow's M147 beta release. Thank you.

### ch...@google.com (2026-03-21)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2026-03-31)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Baseline. Memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487336007)*
