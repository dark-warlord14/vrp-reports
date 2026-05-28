# Debug check failed: isolate()->CurrentLocalHeap()->IsRunning()

| Field | Value |
|-------|-------|
| **Issue ID** | [441427753](https://issues.chromium.org/issues/441427753) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2025-08-27 |
| **Bounty** | $3,000.00 |

## Description

```
#
# Fatal error in ../../src/heap/heap.cc, line 7095
# Debug check failed: isolate()->CurrentLocalHeap()->IsRunning().
#
#
#
#FailureMessage Object: 0x7b8393119c60
==== C stack trace ===============================

    ../v8/v8/out/x64.build/d8(__interceptor_backtrace+0x46) [0x55665cbdb286]
    /home/user/v8/v8/out/x64.build/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f83c02460b3]
    /home/user/v8/v8/out/x64.build/libv8_libplatform.so(+0x392ea) [0x7f83c01912ea]
    /home/user/v8/v8/out/x64.build/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x2a0) [0x7f83c020c7f0]
    /home/user/v8/v8/out/x64.build/libv8_libbase.so(+0x5a7ef) [0x7f83c020b7ef]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::Heap::UnregisterStrongRoots(v8::internal::StrongRootsEntry*)+0x14f) [0x7f83c65779cf]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::IdentityMapBase::Clear()+0xac) [0x7f83c822374c]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::IdentityMap<unsigned long*, v8::internal::ZoneAllocationPolicy>::~IdentityMap()+0x2f) [0x7f83c5b5798f]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevCompilationInfo::~MaglevCompilationInfo()+0xb9) [0x7f83c86b74f9]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevCompilationJob::~MaglevCompilationJob()+0x74) [0x7f83c8843a84]
    /home/user/v8/v8/out/x64.build/libv8.so(v8::internal::maglev::MaglevConcurrentDispatcher::JobTask::Run(v8::JobDelegate*)+0xd2e) [0x7f83c884964e]
    /home/user/v8/v8/out/x64.build/libv8_libplatform.so(v8::platform::DefaultJobWorker::Run()+0x2e6) [0x7f83c018e746]
    /home/user/v8/v8/out/x64.build/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0x1f1) [0x7f83c0195941]
    /home/user/v8/v8/out/x64.build/libv8_libbase.so(+0x91b2e) [0x7f83c0242b2e]
    ../v8/v8/out/x64.build/d8(+0x1999b7) [0x55665cc329b7]
    /lib/x86_64-linux-gnu/libc.so.6(+0x9caa4) [0x7f83be84aaa4]
    /lib/x86_64-linux-gnu/libc.so.6(+0x129c3c) [0x7f83be8d7c3c]
Received signal 6
Aborted

```
#### VERSION

V8 version 14.1.0 (candidate)

#### REPRODUCTION CASE

Build: `python3 tools/dev/gm.py x64.release`

Run: `./d8 poc.js`

---

Reporter credit: Shaheen Fazim

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 537 B)

## Timeline

### fa...@gmail.com (2025-08-27)

Correction: `Debug build: python3 tools/dev/gm.py x64.debug`

### cl...@appspot.gserviceaccount.com (2025-08-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6313094087114752.

### 24...@project.gserviceaccount.com (2025-08-27)

Testcase 6313094087114752 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6313094087114752.

### ct...@chromium.org (2025-08-27)

Clusterfuzz is having trouble reproducing (using a linux debug d8 job). Building debug d8 locally and trying I can reproduce but I have to let it sit a while. I'll start a new clusterfuzz job with a longer timeout.

```
$ time out/Debug/d8 ~/scratch/crbug441427753.js 


#
# Fatal error in ../../v8/src/heap/heap.cc, line 7088
# Debug check failed: LocalHeap::Current()->IsRunning().
#
#
#
#FailureMessage Object: 0x7f14e37fcfe0
==== C stack trace ===============================

    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7f1524008ce3]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8_libplatform.so(+0x16afd) [0x7f1523fb7afd]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x7f1523fe9f24]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8_libbase.so(+0x288f5) [0x7f1523fe98f5]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8.so(+0x21eab29) [0x7f15211eab29]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8.so(v8::internal::IdentityMapBase::Clear()+0x28) [0x7f1521c76128]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8.so(+0x1e14728) [0x7f1520e14728]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8.so(+0x2e4103a) [0x7f1521e4103a]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8.so(+0x2ff0d2e) [0x7f1521ff0d2e]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8_libplatform.so(+0x15873) [0x7f1523fb6873]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8_libplatform.so(v8::platform::DefaultWorkerThreadsTaskRunner::WorkerThread::Run()+0xcc) [0x7f1523fb8e5c]
    /usr/local/google/home/cthomp/chromium2/src/out/Debug/libv8_libbase.so(+0x4648f) [0x7f152400748f]
    /lib/x86_64-linux-gnu/libc.so.6(+0x92b7b) [0x7f151dec8b7b]
    /lib/x86_64-linux-gnu/libc.so.6(+0x1107b8) [0x7f151df467b8]
Trace/breakpoint trap (core dumped)

real	1m0.390s
user	0m57.864s
sys	0m1.375s

```

### cl...@appspot.gserviceaccount.com (2025-08-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4784419965435904.

### ct...@chromium.org (2025-08-27)

Clusterfuzz continues to have trouble reproducing this, so I'm going to pass this to the V8 shepherd for further triage. ishell@ could you PTAL?

- Setting a provision severity of High (S1). V8 folks please help assess if this debug check has actual security ramifications or not.
- Setting a provisional FoundIn of Extended Stable (M138)

### is...@chromium.org (2025-08-28)

Thank you for the report! The fix is on the way.

### dx...@google.com (2025-08-28)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6895240>

[maglev] Properly destroy failed compilation jobs

---


Expand for full commit details
```
     
    Fixed: 441427753 
    Change-Id: I93cf8848ec770a9a375f5b7521d7d847f01f7288 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/6895240 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#102098}

```

---

Files:

- M `src/maglev/maglev-concurrent-dispatcher.cc`

---

Hash: [a6578fa58cc5862e9fd340326dbc7492904426ca](https://chromiumdash.appspot.com/commit/a6578fa58cc5862e9fd340326dbc7492904426ca)  

Date: Thu Aug 28 11:46:42 2025


---

### ch...@google.com (2025-08-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-08-28)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-08-28)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139, 140].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### is...@chromium.org (2025-08-28)

This is a security issue. There's a short time window when a GC might be [iterating over the strong roots region list](https://source.chromium.org/chromium/chromium/src/+/8b9ad85423ee41ac181d3507019e61bd19dc3310:v8/src/heap/heap.cc;l=4949) and looking at the entry while it's [being removed from the list](https://source.chromium.org/chromium/chromium/src/+/8b9ad85423ee41ac181d3507019e61bd19dc3310:v8/src/heap/heap.cc;l=7085) by background compilation thread.

Given that the time window is expected to be quite short, I think it's hardly exploitable in practice - thus lowering the severity.

### sp...@google.com (2025-09-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Report of mildly mitigated memory corruption in a sandboxed process / the renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### fa...@gmail.com (2025-09-26)

Hi, can I get a CVE and credit for this issue? Thank you.

### ch...@google.com (2025-12-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2025-12-05)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/441427753)*
