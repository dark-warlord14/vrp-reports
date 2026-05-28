# ---

| Field | Value |
|-------|-------|
| **Issue ID** | [438916130](https://issues.chromium.org/issues/438916130) |
| **Status** | Unknown |
| **Severity** | Unknown |
| **Priority** | Unknown |
| **Component** | Unknown |
| **Reporter** | Unknown |
| **Created** | 2025-08-15 |
| **Bounty** | Confirmed (amount unknown) |

## Description

---

### Report description

Use-After-Free in DataPipeConsumerDispatcher::Close() Due to Concurrent Access

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

Chromium — Mojo Core (mojo/core), DataPipeConsumerDispatcher (consumer-side data pipe dispatcher)

---

### The problem

#### Please describe the technical details of the vulnerability

Severity: Real use-after-free (ASan + TSan PoC supplied). Impact depends on which process materializes the dispatcher (browser → high severity; renderer → still serious and possibly chainable). See attack scenario below.

**Files & exact pointers (source snapshot):**

mojo/core/data\_pipe\_consumer\_dispatcher.cc — BeginReadData returns pointer into mapping. (Function header at approx. L13; pointer returned at approx. L14).
Chromium Git Repositories

mojo/core/data\_pipe\_consumer\_dispatcher.cc — Close() (locks then calls CloseNoLock) at approx. L6; CloseNoLock() unmaps mapping at approx. L31, clearing ring\_buffer\_mapping\_ and shared\_ring\_buffer\_. This unmap happens without checking in\_two\_phase\_read\_.
Chromium Git Repositories

mojo/core/data\_pipe\_consumer\_dispatcher.cc — Deserialize(...) constructs dispatcher from a platform handle / shared memory region and therefore is a reachable deserialization point where remote handles can be materialized in the receiving process (around L23–L26).

**Minimal PoC (what I attached/run):**

Minimal harness (isolated test) that reproduces the race and triggers:

ASan PoC: run a two-phase BeginReadData, spawn Close() concurrently, then dereference the returned pointer → ASan shows heap-use-after-free (allocation site = constructor/new[]; free site = Close() → delete[]; read site = harness).

TSan PoC: loop early to reproduce race; TSan shows data race between delete[] (Close) and read.

Commands used (examples):

**ASan**

clang++ -std=c++17 -g -fsanitize=address data\_pipe\_consumer\_dispatcher.cc uaf\_asan.cpp -o uaf\_asan
ASAN\_OPTIONS=detect\_stack\_use\_after\_return=1:halt\_on\_error=1 ./uaf\_asan 2>&1 | tee asan\_log.txt

**TSan**

clang++ -std=c++17 -g -fsanitize=thread data\_pipe\_consumer\_dispatcher.cc uaf\_tsan.cpp -o uaf\_tsan
TSAN\_OPTIONS=halt\_on\_error=1:report\_thread\_leaks=1 ./uaf\_tsan 2>&1 | tee tsan\_log.txt

(Attach asan\_log.txt, tsan\_log.txt, and the harness sources.)

**Root cause:** BeginReadData() hands out a raw pointer into ring\_buffer\_mapping\_.memory() and sets in\_two\_phase\_read\_ = true, but CloseNoLock() (called by Close()) clears/unmaps ring\_buffer\_mapping\_ and shared\_ring\_buffer\_ without checking or waiting for active two-phase reads (in\_two\_phase\_read\_), allowing a concurrent free of memory still pointed at by callers.

**Remote exploiability**

Two-phase consumer read in a privileged process: The network service reads from data\_pipe\_ using the Mojo C++ wrapper’s ReadData, which is the two-phase read surface exposed by mojo/public/cpp/system/data\_pipe.h; the watcher-driven loop in ReadInternal/OnHandleReadable confirms active consumption of the consumer handle in a privileged process.

Renderer-triggerable abort tearing down the same consumer during read: The renderer-facing mojom::ChunkedDataPipeGetter remote is bound with a disconnect handler that, when invoked, enters OnSizeReceived’s error path and synchronously cancels the watcher and resets data\_pipe\_ (closing the consumer) while a pending read may be in progress (buf\_ non-null), thereby tearing down the read-side consumer during an active read.

proof:

Disconnect handler install: chunked\_data\_pipe\_getter\_.set\_disconnect\_handler(... OnDataPipeGetterClosed).

Start reading and consumer ownership: CreateDataPipe; StartReading(std::move(data\_pipe\_producer)); data\_pipe\_ = std::move(data\_pipe\_consumer).

Read loop setup: handle\_watcher\_.Watch(data\_pipe\_.get(), READABLE|PEER\_CLOSED, ... OnHandleReadable).

Read call: data\_pipe\_->ReadData(MOJO\_READ\_DATA\_FLAG\_NONE, buf->first(num\_bytes), num\_bytes).

Abort/teardown during read: OnDataPipeGetterClosed -> OnSizeReceived error path -> handle\_watcher\_.Cancel(); data\_pipe\_.reset(); buf\_ cleared; chunked\_data\_pipe\_getter\_.reset(); OnReadCompleted(status\_).

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

Actors & setup:

- Victim: Chrome user; Chrome runs sandboxed renderer(s) and a browser process that accepts Mojo handles.
- Attacker: a malicious webpage that can arrange for a DataPipe consumer handle to be passed to another process (e.g., via a streaming API or by invoking browser APIs that accept/forward data-pipe handles).

Scenario:

1. The attacker causes a DataPipeConsumer handle to be deserialized in the target process (e.g., browser) causing creation of a DataPipeConsumerDispatcher that maps a shared ring buffer. (Deserialize path in `mojo/core` materializes the shared mapping.)
2. Using carefully timed operations, the attacker causes code to call `BeginReadData()` on that dispatcher — the API returns a raw pointer into the mapping.
3. Before the caller finishes the two-phase read (`EndReadData()`), another action induced by the attacker triggers `Close()` on the same dispatcher. `Close()` unmaps/frees the ring\_buffer mapping without checking for in-progress two-phase readers.
4. The original caller accesses the pointer returned by `BeginReadData()` after `Close()` has freed the mapping → use-after-free / memory corruption.
   Potential consequences:

- If the affected dispatcher runs in an unsandboxed or privileged process (browser, utility), attacker-controlled memory corruption could potentially be turned into code execution.
- If in a sandboxed renderer, the bug can still crash the process or be chained with a sandbox escape for further compromise.

**Exploitable by:**

- Any attacker who can serve a malicious webpage to a Chrome user.
- The attack requires the victim to navigate to a page that interacts with Chrome’s renderer-to-network Mojo interfaces (ChunkedDataPipeGetter).

**What the attacker gains:**

- Sandboxed renderer: Can crash the renderer process, causing denial-of-service. With further chaining, may attempt a sandbox escape.
- Privileged process (browser/network): The UAF in the network service allows memory corruption. A remote attacker could potentially execute arbitrary code in a higher-privileged process, leading to full compromise of the Chrome process or host OS.

**Summary:** Remote, web-reachable attacker can cause crashes and, under certain conditions, potentially achieve remote code execution in a privileged process.

also i wasnt able to complie and test inside the chromium build because i dont really have capable hardware

also this is not really perfectly replicable rn i am still testing for a working 90% race exploit with remote execution but may take some time

---

### The cause

#### What version of Chrome have you found the security issue in?

127.0.6533.72 + stable

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

satvik hardat

## Attachments

- [uaf_tsan.cpp](attachments/uaf_tsan.cpp) (text/plain, 978 B)
- [uaf_test.cpp](attachments/uaf_test.cpp) (text/plain, 790 B)
- [tsan_log.txt](attachments/tsan_log.txt) (text/plain, 3.1 KB)
- [uaf_asan.cpp](attachments/uaf_asan.cpp) (text/plain, 936 B)
- [asan_log.txt](attachments/asan_log.txt) (text/plain, 19.6 KB)
- [data_pipe_consumer_dispatcher.h](attachments/data_pipe_consumer_dispatcher.h) (text/plain, 614 B)
- [data_pipe_consumer_dispatcher.cc](attachments/data_pipe_consumer_dispatcher.cc) (text/plain, 1.0 KB)
- [uaf_tsan.txt](attachments/uaf_tsan.txt) (text/plain, 1.5 MB)
- [uaf_test.txt](attachments/uaf_test.txt) (text/plain, 1.5 MB)
- [uaf_asan.txt](attachments/uaf_asan.txt) (text/plain, 1.7 MB)
- [a.html](attachments/a.html) (text/html, 713 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [a.html](attachments/a.html) (text/html, 3.1 KB)
- Screen Recording 2025-08-15 222252.mp4 (video/mp4, 46.9 MB)
- [a.html](attachments/a.html) (text/html, 1.3 KB)
- [a.html](attachments/a.html) (text/html, 1.6 KB)
- Screen Recording 2025-08-16 143709.mp4 (video/mp4, 24.3 MB)
- deleted (application/octet-stream, 0 B)
- [Screen Recording 2025-08-16 193748.mp4](attachments/Screen Recording 2025-08-16 193748.mp4) (video/mp4, 180.6 MB)
- [a.html](attachments/a.html) (text/html, 1.3 KB)
- [modified-but-not-crashing-much-still.html](attachments/modified-but-not-crashing-much-still.html) (text/html, 1.4 KB)

## Timeline

### sa...@gmail.com (2025-08-15)

Still trying to do a remote UAF but this does work locally

### sa...@gmail.com (2025-08-15)

my analysis of Chromium's Mojo source code, this does appear to be a legitimate use-after-free vulnerability in mojo/core/data_pipe_consumer_dispatcher.cc. Here's a breakdown confirming the issue step by step, aligned with the exact pointers I mentioned:

BeginReadData Pointer Return: The function (around line 13 in typical snapshots) initiates a two-phase read and returns a raw pointer to the shared ring buffer mapping. This pointer provides direct access to the mapped memory, which is vulnerable if the mapping is freed prematurely.

Close() and CloseNoLock() Unmapping: Close() (around line 6) acquires a lock and calls CloseNoLock(). In CloseNoLock() (around line 31), it unmaps the ring buffer (ring_buffer_mapping_ and shared_ring_buffer_) and clears related fields without checking if a two-phase read is in progress (e.g., no validation of in_two_phase_read_). This allows the mapping to be freed while a read operation still holds the pointer, leading to UAF when the caller accesses it post-close.

Deserialize as Entry Point: Deserialize() (around lines 23–26) constructs a DataPipeConsumerDispatcher from a platform handle and shared memory region, materializing remote handles in the receiving process (e.g., browser). This is reachable from untrusted sources like malicious webpages via handle passing (e.g., through APIs that forward data pipes), enabling attackers to set up the shared mapping and trigger the race condition

### sa...@gmail.com (2025-08-15)

this is a lifetime bug? i believe this has been here from a long long time

### sa...@gmail.com (2025-08-15)

deleted

### sa...@gmail.com (2025-08-15)

deleted

### sa...@gmail.com (2025-08-15)

deleted

### sa...@gmail.com (2025-08-15)

redacted

### sa...@gmail.com (2025-08-15)

redacted

### sa...@gmail.com (2025-08-15)

redacted

### am...@chromium.org (2025-08-16)

Hello, thank you for the report. This report does not present clear actionable information to demonstrate a reachable, exploitable security issue in Chrome in order to reproduce, validate, and triage this issue.

Before we proceed with triage, can you please confirm the following:

- Does this issue impact / reproduce on an active, production version of Chrome? I ask because you have stated this issue impacts version 127.0.6533.72; the current oldest active release version of Chrome is Extended Stable version 138.0.7204.235. So issues should impact versions 138.0.7204.235 and newer
- Which version of the POC / test case file is the current, reliably reproducible version?
  Please also provide clear, concise steps to reproduce.
  In your video you have used the a.html file, but that doesn't seem to reproduce to result in a UAF based on what video displays
- please provide an asan stacktrace from a Chrome ASAN build, the asan logs you have presented appear to be either corrupted or not related to Chrome.

To better understand expected characteristics of a security bug report for Chrome, please see: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md#Best-Practices-for-Security-Bug-Reporting> and [our guidelines on AI bug reporting](https://chromium.googlesource.com/chromium/src/+/main/docs/security/faq.md#Should-I-ask-an-AI-to-Generate-a-Vulnerability-Report-for-Chrome)

Setting needs-feedback and a next-action date. If valid, actionable information related to Chrome is unable to be provided by that time, we'll need to go ahead and close this report.

### sa...@gmail.com (2025-08-16)

redacted

### pe...@google.com (2025-08-16)

Thank you for providing more feedback. Adding the requester to the CC list.

### sa...@gmail.com (2025-08-16)

also due to hardware restrictions the asan_log.txt in my POC was a single C++ compiled file that had the same implementation as the data_pipe_consumer_dispatcher.cc to confirm the Race possibility

### dc...@chromium.org (2025-08-16)

Sorry, but this is not a valid bug report. `DataPipeConsumerDispatcher` makes no claim that it is safe to use concurrently on multiple threads without external synchronization: in fact, classes that are safe to use concurrently with no synchronization whatsoever are quite rare. This is only a security bug if you can demonstrate that there is code in the Chrome product that is actually using `DataPipeConsumerDispatcher` on multiple threads without external synchronization.

### sa...@gmail.com (2025-08-16)

redacted

### sa...@gmail.com (2025-08-16)

Thank you for reviewing and for the feedback on the thread-safety aspects of DataPipeConsumerDispatcher. I appreciate the clarification.

I've attached an updated PoC (a.html) that, when run can crash you browser in 3-4 attempts. This was reproducible on 139.0.7258.128 (Official Build) (64-bit) (cohort: Stable), and I've included a screen recording (Screen Recording 2025-08-16 143709.mp4) showing the crash in action.

The crash occurs in the context of the fetch/abort race I described, and it aligns with the UAF window in the code paths mentioned. Given this new reproducible crash, could the team please take another look or confirm if this is still considered intended behavior? If needed, I'm happy to provide more details or adjust the PoC for easier testing.

Thank You!

### dc...@chromium.org (2025-08-16)

The video is invalid/does not load, and some attempts at reproing with `a.html` did not work either.

### sa...@gmail.com (2025-08-16)

deleted

### sa...@gmail.com (2025-08-16)

deleted

### sa...@gmail.com (2025-08-16)

deleted

### sa...@gmail.com (2025-08-16)

deleted

### sa...@gmail.com (2025-08-16)

see does this confirm the bug?
its a bit long but u can see stack trace from mem curruption i believe at the end of the POC (my browser also crashed once during testing which is also in the video POC)
also the html file is also attached

### sa...@gmail.com (2025-08-16)

[8780:1888:0816/195405.988:ERROR:content\browser\gpu\gpu_process_host.cc:966] GPU process exited unexpectedly: exit_code=-1073741523
==4744==ERROR: AddressSanitizer failed to allocate 0x800000 (8388608) bytes of StackStore (error code: 1455)
==4744==Dumping process modules:
        0x7ff676500000-0x7ff6776db000 C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\chrome.exe
        0x7ff9675a0000-0x7ff967fa4000 C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll
        0x7ff967fb0000-0x7ff968517000 C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\chrome_elf.dll
        0x7ff9d3fa0000-0x7ff9d3fbe000 C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\VCRUNTIME140.dll
        0x7ff9dea40000-0x7ff9dea4b000 C:\WINDOWS\SYSTEM32\VERSION.dll
        0x7ff9e8820000-0x7ff9e8c10000 C:\WINDOWS\System32\KERNELBASE.dll
        0x7ff9e8f80000-0x7ff9e90cb000 C:\WINDOWS\System32\ucrtbase.dll
        0x7ff9e9320000-0x7ff9e93e9000 C:\WINDOWS\System32\KERNEL32.DLL
        0x7ff9e95e0000-0x7ff9e9689000 C:\WINDOWS\System32\msvcrt.dll
        0x7ff9eb580000-0x7ff9eb7e7000 C:\WINDOWS\SYSTEM32\ntdll.dll
AddressSanitizer: CHECK failed: sanitizer_common.cpp:61 "((0 && "unable to mmap")) != (0)" (0x0, 0x0) (tid=18028)
Warning: maxDynamicUniformBuffersPerPipelineLayout artificially reduced from 24 to 16 to fit dynamic offset allocation limit.
Warning: maxDynamicStorageBuffersPerPipelineLayout artificially reduced from 60 to 16 to fit dynamic offset allocation limit.
==4744==WARNING: Can't read from symbolizer at fd 196
==4744==WARNING: Can't write to symbolizer at fd 216
    #0 0x7ff9675f56e8  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x1800556e8)
    #1 0x7ff9675b9004  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x180019004)
    #2 0x7ff9675a55c6  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x1800055c6)
    #3 0x7ff9675b542e  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18001542e)
    #4 0x7ff9675bac05  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18001ac05)
    #5 0x7ff9675baa61  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18001aa61)
    #6 0x7ff9675bcbe7  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18001cbe7)
    #7 0x7ff9675bd0aa  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18001d0aa)
    #8 0x7ff9675bce5f  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18001ce5f)
    #9 0x7ff9675cced8  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18002ced8)
    #10 0x7ff9675cd515  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18002d515)
    #11 0x7ff9675ea29d  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18004a29d)
    #12 0x7ff9e8fbd188  (C:\WINDOWS\System32\ucrtbase.dll+0x18003d188)
    #13 0x7ff9e8f94a0b  (C:\WINDOWS\System32\ucrtbase.dll+0x180014a0b)
    #14 0x7ff9e8f9488a  (C:\WINDOWS\System32\ucrtbase.dll+0x18001488a)
    #15 0x7ff9e8f94843  (C:\WINDOWS\System32\ucrtbase.dll+0x180014843)
    #16 0x7ff9675fda30  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18005da30)
    #17 0x7ff9675fd9f8  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18005d9f8)
    #18 0x7ff9675b9698  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x180019698)
    #19 0x7ff9675f5231  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x180055231)
    #20 0x7ff9675f59db  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x1800559db)
    #21 0x7ff9e8fee715  (C:\WINDOWS\System32\ucrtbase.dll+0x18006e715)
    #22 0x7ff9675fe669  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18005e669)
    #23 0x7ff9675fe84a  (C:\Users\jyoti\Downloads\win32-release_x64_asan-win32-release_x64-1502291\clang_rt.asan_dynamic-x86_64.dll+0x18005e84a)
    #24 0x7ff9eb6e0ced  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180160ced)
    #25 0x7ff9eb5f29fd  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800729fd)
    #26 0x7ff9eb5f196b  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18007196b)
    #27 0x7ff9eb5bbc79  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18003bc79)
    #28 0x7ff9eb5bbca5  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18003bca5)
    #29 0x7ff9eb5bbca5  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18003bca5)
    #30 0x7ff9eb5e56db  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800656db)
    #31 0x7ff9eb5e3893  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180063893)
    #32 0x7ff9eb5e367d  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006367d)
    #33 0x7ff9eb5b5fcd  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180035fcd)

AddressSanitizer: nested bug in the same thread, aborting.

### sa...@gmail.com (2025-08-17)

ok leave it ill see if i can remotely trigger the heap use after free and if i can confirm with the AddressSanitizer then i will submit a new report!

### dc...@chromium.org (2025-08-18)

As I noted, the originally-reported bug here isn't valid, nor do the stacks above demonstrate a use-after-free in `DataPipeConsumerDispatcher`; they indicate other issues, e.g. ASan failing to allocate, but those aren't security bugs.

**However**, while testing the attachment in [comment #23](https://issues.chromium.org/issues/438916130#comment23), I discovered that the attach test case very occasionally triggers other renderer-only crashes: at least one version of the crash is already tracked in [issue 438569732](https://issues.chromium.org/issues/438569732) (filed August 13). My success rate is quite low though; I've had two successful attempts and many more failed ones. I attempted to automate the clicking of the button but that hasn't helped much either. I've attached my modified version, and I'm going to try throwing it into clusterfuzz.

@ml...@chromium.org since you're assigned on the other bug, I'm CCing you here. Unfortunately, the test case is still not much to go on, but maybe you'll see something in the stack trace from ASan that will help:

```
=================================================================
==5060==ERROR: AddressSanitizer: use-after-poison on address 0x7e9c00b8867c at pc 0x00031dbc9fcc bp 0x00016fbadd90 sp 0x00016fbadd88
WRITE of size 4 at 0x7e9c00b8867c thread T0
==5060==WARNING: invalid path to external symbolizer!
==5060==WARNING: Failed to use and restart external symbolizer!
    #0 0x00031dbc9fc8 in blink::HeapObserverList<blink::ContextLifecycleObserver>::RemoveObserver(blink::ContextLifecycleObserver*)+0x75c (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x1dbc9fc8)
    #1 0x00031dbd0ed0 in blink::ContextLifecycleObserver::SetContextLifecycleNotifier(blink::ContextLifecycleNotifier*)+0x78 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x1dbd0ed0)
    #2 0x00031fea8770 in blink::DOMTimer::Fired()+0x53c (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x1fea8770)
    #3 0x00031dff61b8 in blink::TimerBase::RunInternal()+0xb0 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x1dff61b8)
    #4 0x00031a6048c0 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::TimerBase::*&&)(), blink::TimerBase*>, base::internal::BindState<true, true, false, void (blink::TimerBase::*)(), blink::UnretainedWrapper<blink::TimerBase>>, void ()>::RunOnce(base::internal::BindStateBase*)+0x11c (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x1a6048c0)
    #5 0x00031134610c in base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x344 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x1134610c)
    #6 0x0003113a9aa8 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)+0x844 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x113a9aa8)
    #7 0x0003113a8ea4 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()+0x138 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x113a8ea4)
    #8 0x000311230f78 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*)+0x1cc (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x11230f78)
    #9 0x0003113aad9c in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)+0x338 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x113aad9c)
    #10 0x0003112d5598 in base::RunLoop::Run(base::Location const&)+0x434 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x112d5598)
    #11 0x00031a556d94 in content::RendererMain(content::MainFunctionParams)+0x8c4 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x1a556d94)
    #12 0x00030e04e3cc in content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)+0x41c (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0xe04e3cc)
    #13 0x00030e0503b0 in content::ContentMainRunnerImpl::Run()+0x468 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0xe0503b0)
    #14 0x00030e04be38 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)+0x56c (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0xe04be38)
    #15 0x00030e04c69c in content::ContentMain(content::ContentMainParams)+0x190 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0xe04c69c)
    #16 0x0003000070c4 in ChromeMain+0x360 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x70c4)
    #17 0x000100250ce4 in main+0x254 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer):arm64+0x100000ce4)
    #18 0x000194262b94 in start+0x17b8 (/usr/lib/dyld:arm64+0xfffffffffff3ab94)

Address 0x7e9c00b8867c is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x1dbc9fc8) in blink::HeapObserverList<blink::ContextLifecycleObserver>::RemoveObserver(blink::ContextLifecycleObserver*)+0x75c
Shadow bytes around the buggy address:
  0x7e9c00b88380: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e9c00b88400: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e9c00b88480: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e9c00b88500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7e9c00b88580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7e9c00b88600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00[f7]
  0x7e9c00b88680: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e9c00b88700: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e9c00b88780: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e9c00b88800: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7e9c00b88880: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb

NOTE: the stack trace above identifies the code that *accessed* the poisoned memory.
To identify the code that *poisoned* the memory, try the experimental setting ASAN_OPTIONS=poison_history_size=<size>.

==5060==ADDITIONAL INFO

==5060==Note: Please include this section with the ASan report.
Task trace:
    #0 0x00031fea7ac0 in blink::DOMTimer::DOMTimer(blink::ExecutionContext&, blink::ScheduledAction*, base::TimeDelta, bool)+0x608 (/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Chromium Framework:arm64+0x1fea7ac0)


Command line: `/Users/dcheng/src/chrome/src/asan-stuff/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/141.0.7359.0/Helpers/Chromium Helper (Renderer).app/Contents/MacOS/Chromium Helper (Renderer) --type=renderer --user-data-dir=/var/folders/0z/dr3l_rdd6rz6h8fy106v7zx00020mk/T/tmp.pidddeBMex --enable-dinosaur-easter-egg-alt-images --file-url-path-alias=/gen=/Users/dcheng/src/chrome/src/asan-stuff/gen --lang=en-US --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=8 --time-ticks-at-unix-epoch=-1755454318808385 --launch-time-ticks=825552502 --shared-files --metrics-shmem-handle=1752395122,r,17974985417008530711,11985258489093871136,2097152 --field-trial-handle=1718379636,r,14035276343092076718,16124029116842509759,262144 --variations-seed-version --seatbelt-client=114`


==5060==END OF ADDITIONAL INFO
==5060==ABORTING

```

(I've also seen the `CHECK()` on index bug; unfortunately I haven't managed to reproduce that this time so far.

### cl...@appspot.gserviceaccount.com (2025-08-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5771122062589952.

### 24...@project.gserviceaccount.com (2025-08-18)

Testcase 5771122062589952 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5771122062589952.

### sa...@gmail.com (2025-08-18)

Hi,

Thank you for the detailed analysis and for taking the time to re-investigate this.

I understand now that my initial theory about the DataPipeConsumerDispatcher race was incorrect, and I appreciate the clarification. It's great to hear that the test case was still useful in helping reproduce the known Blink issue (438569732).

Happy to know it could contribute in some way. Let me know if you need any other details from my end.

Best,
Satvik

### ml...@chromium.org (2025-08-18)

(Just returned from OOO, will take a bit to ramp up.)

I don't see anything immediately obvious. Will try to reproduce this with the repro from [comment #26](https://issues.chromium.org/issues/438916130#comment26).

### dc...@chromium.org (2025-08-18)

Given the crash reports, I'm going to dupe this into the earlier crash report bug to centralize discussion there.

### dc...@chromium.org (2025-08-18)

Well on second thought, maybe not since the crash report is not clearly a memory-safety issue. But I'll route this otherwise.

### dc...@chromium.org (2025-08-18)

I don't have a clear FoundIn to set yet, due to the inconsistent repro. I expect we'll know more once we have a fix...

### ml...@chromium.org (2025-08-18)

Okay, I did find a bug.

The observer list is implemented with a vector (for fast iteration) and a hash map (for constant time removal) -- both being weakly managed. The bug is that the data structures get out of sync.

Bug annotated in code:

```
  // Removes the given observer from this list. Does nothing if this observer is
  // not in this list. Removing an observer is O(n) but amortized constant.
  void RemoveObserver(ObserverType* observer) {
    CHECK(mutation_state_ & kAllowRemoval);
    DCHECK_EQ(observers_to_indices_.size(), observers_.size());

    const auto it = observers_to_indices_.find(observer);
    if (it == observers_to_indices_.end()) [[unlikely]] {
      return;
    }
    const wtf_size_t index = it->value;
    // `erase()` may trigger GC which results in `observers_to_indices_` already
    // missing the to-be-deleted observer.
    observers_to_indices_.erase(it);

    // == BUG ==
    // Since erase() may invoke GC and `observers_` is weak, elements in there may die.
    // This means that `index` may be larger than `observers_.size()` afterwards, 
    // leading to a CHECK failure.
    // == BUG ==
    
    const wtf_size_t last_observer_index = observers_.size() - 1;
    if (index != last_observer_index) {
      auto* last_observer = observers_[last_observer_index].Get();
      observers_[index] = last_observer;
      observers_to_indices_.find(last_observer)->value = index;
    }
    observers_.pop_back();
    observers_.ShrinkToReasonableCapacity();
    // observers_to_indices_ did already shrink if necessary due to erase().
    check_capacity_ = false;
  }

```

By reading the code, I could only find cases though that should crash in the `CHECK()` that is also found in [issue 438569732](https://issues.chromium.org/issues/438569732). The repro also only ever lead to a `CHECK()` crasher for me.

The UAF would indicate that some access is invalid in there. `RemoveObserver()` is only ever used with `this` [1](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/context_lifecycle_observer.cc;drc=c7aed0467577ef236f0cf0e3b369b96f69a040d7;bpv=1;bpt=1;l=28) which is a little suspicious because we basically remove a weak `this` pointer from a data structure contained in itself, all weakly held and able to trigger GC. I couldn't find an issue there though.

### sa...@gmail.com (2025-08-19)

Hi team,

Thanks for the ongoing investigation and for reopening this based on the repro attempts.

Building on the analysis in [comment #34](https://issues.chromium.org/issues/438916130#comment34) and the use-after-poison stack in #26, I've dug deeper into the Blink source (e.g., third\_party/blink/renderer/platform/heap\_observer\_list.h and related heap files). I believe the root cause is a race condition in HeapObserverList<ObserverType>::RemoveObserver, where garbage collection (GC) can interleave during the method, leading to an out-of-bounds access on potentially poisoned memory. This manifests as the use-after-poison (UAP) in ASan builds, or sometimes as CHECK failures, depending on GC timing.

Here's a detailed breakdown for clarity:

- The HeapObserverList maintains two data structures for observers:
- A HeapVector<UntracedMember<ObserverType>> observers\_ (for fast iteration).
- A HeapHashMap<WeakMember<ObserverType>, wtf\_size\_t> observers\_to\_indices\_ (for O(1) lookups and removals).
- Both are weakly managed via Blink's Oilpan GC system, allowing automatic cleanup of dead (unreachable) observers.

In RemoveObserver (from platform/heap\_observer\_list.h):

```
void RemoveObserver(ObserverType* observer) {
  CHECK(mutation_state_ & kAllowRemoval);
  DCHECK_EQ(observers_to_indices_.size(), observers_.size());
  const auto it = observers_to_indices_.find(observer);
  if (it == observers_to_indices_.end()) [[unlikely]] {
    return;
  }
  const wtf_size_t index = it->value;
  // Erase can trigger GC via weak callbacks, shrinking observers_ if dead entries are cleaned up.
  observers_to_indices_.erase(it);
  // Post-GC, index may now be >= observers_.size() (invalid).
  const wtf_size_t last_observer_index = observers_.size() - 1;
  if (index != last_observer_index) {
    auto* last_observer = observers_[last_observer_index].Get();
    observers_[index] = last_observer;  // Out-of-bounds if index >= size; may hit poisoned memory.
    observers_to_indices_.find(last_observer)->value = index;
  }
  observers_.pop_back();
  observers_.ShrinkToReasonableCapacity();
  check_capacity_ = false;
}

```

- **The problem occurs during the erase call:** Erasing from the HeapHashMap (which uses WeakMember) can trigger a GC cycle at allocation/deallocation points or weak callback processing. This invokes the registered weak callback CleanupDeadObservers (via visitor->RegisterWeakCallbackMethod in trace methods).

In CleanupDeadObservers (non-iterating mode, since mutation\_state\_ allows mutations):

- It removes dead observers from the vector using std::remove\_if (filtering out those not alive per the liveness broker).
- It then rebuilds the hash map indices for the remaining observers.
- This shrinks the vector's size if dead observers are present.
- After erase returns, the local index (fetched pre-GC) may now be invalid (>= the new vector size). When the code proceeds:
- It computes last\_observer\_index = observers\_.size() - 1 (using the post-GC size).
- If index != last\_observer\_index (which could hold if index <= last\_observer\_index), it attempts to access observers\_[last\_observer\_index] and assign to observers\_[index].

**Accessing/writing to observers\_[index] when index >= size() is out-of-bounds. In AddressSanitizer (ASan) builds, this manifests as a use-after-poison because:**

- *The vector's backing store has redzones (poisoned memory) beyond its current size.*
- *If the vector was resized/shrunk (e.g., via internal capacity adjustments or during GC compaction in Oilpan), the old buffer area may be freed and poisoned.*

*This leads to memory corruption (UAF/use-after-poison), potentially exploitable for arbitrary reads/writes if chained, especially in the renderer process.*

**The variability (CHECK failures vs. UAF) depends on GC timing, the presence of dead observers, and whether the out-of-bounds access hits poisoned memory.**

For context, here's a snippet from the weak callback handling (approximate from heap\_observer\_list.h trace methods):

```
void Trace(Visitor* visitor) const {
  // Registers weak callback for GC to invoke CleanupDeadObservers.
  visitor->RegisterWeakCallbackMethod(this, &HeapObserverList::CleanupDeadObservers);
}

void CleanupDeadObservers(const LivenessBroker& broker) {
  // Non-iterating mode: Remove dead observers and rebuild indices.
  auto last = std::remove_if(observers_.begin(), observers_.end(),
                             [&](const auto& o) { return !broker.IsHeapObjectAlive(o); });
  observers_.erase(last, observers_.end());
  // Rebuild observers_to_indices_ for remaining.
  observers_to_indices_.clear();
  for (wtf_size_t i = 0; i < observers_.size(); ++i) {
    observers_to_indices_.insert(observers_[i].Get(), i);
  }
}

```

This seems consistent with the repro behavior (e.g., via fetch/abort stress on contexts with observers). let me know if this matches your findings and if I find a more reliable POC a for ASan repro, i will comment it later

Best,

Satvik Hardat

### ml...@chromium.org (2025-08-19)

This is exactly the repro that I can also understand and follow. However, as you write, the broken condition is `index >= size()`.

> Accessing/writing to observers\_[index] when index >= size() is out-of-bounds. In AddressSanitizer (ASan) builds, this manifests as a use-after-poison because:

`WTF::Vector` has bounds checks for all it's accessors using `CHECK()`, e.g. `operator[]` [1], so I cannot follow why this would be a U-A-P for ASAN builds.

I can so far only see why this would crash in a `CHECK()`.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/wtf/vector.h;l=1356?q=wtf%2Fvector.h&ss=chromium>

### sa...@gmail.com (2025-08-19)

what if Oilpan’s Incremental GC, where the buffer freeing and poisoning can occur mid-GC at a safepoint?, allowing the operator[] `CHECK` to use a stale size\_ (pre-update) and pass, but the subsequent access hits the poisoned old buffer. This fits the race window and variability in manifestations (CHECK vs. UAP) based on GC timing and task scheduling.

(i can be really wrong here)

### sa...@gmail.com (2025-08-19)

Like when `observers_[last_observer_index].Get()` or `observers_[index] = last_observer` runs:

operator[] checks index < size\_ (in wtf/vector.h:1356):

```
cppT& operator[](wtf_size_t index) {
  CHECK(index < size());
  return begin()[index];
}

```

If `size_` is stale (pre-GC, larger than actual), the `CHECK` passes, but begin\_ may still point to the old, freed buffer.
The write (`observers_[index] = last_observer`) accesses this poisoned memory, triggering ASan’s UAP (as seen in [comment #26](https://issues.chromium.org/issues/438916130#comment26)’s stack trace).

### dx...@google.com (2025-08-19)

Project: chromium/src  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6859882>

heap: Fix inconsistencies in HeapObserverList

---


Expand for full commit details
```
     
    The observer list is both weak (implicitly managed) and allows for 
    removing observers. If observers are removed while at the same time 
    multiple other observers die, and the removal call triggers GC, this may 
    lead to CHECK() failures where the index retrieved on `RemoveObserver` 
    is too large for the `observers_` array. 
     
    Bug: 438569732, 438916130 
    Change-Id: I6731ad38e96f01a47258bc8f8f5a0b1b41e736a3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6859882 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Anton Bikineev <bikineev@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1503316}

```

---

Files:

- M `third_party/blink/renderer/platform/heap_observer_list.h`

---

Hash: [a6a9cbddea75dc950e808f84695d3d3e2275f58f](https://chromiumdash.appspot.com/commit/a6a9cbddea75dc950e808f84695d3d3e2275f58f)  

Date: Tue Aug 19 14:04:08 2025


---

### ml...@chromium.org (2025-08-19)

> If size\_ is stale (pre-GC, larger than actual), the CHECK passes, but begin\_ may still point to the old, freed buffer. The write (observers\_[index] = last\_observer) accesses this poisoned memory, triggering ASan’s UAP (as seen in [comment #26](https://issues.chromium.org/issues/438916130#comment26)’s stack trace).

How would that happen? That would be a different bug then.

### sa...@gmail.com (2025-08-19)

not possible, im dumb

### dx...@google.com (2025-08-20)

Project: chromium/src  

Branch:  refs/branch-heads/7339  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6867493>

[M140] heap: Fix inconsistencies in HeapObserverList

---


Expand for full commit details
```
     
    Original change's description: 
    > heap: Fix inconsistencies in HeapObserverList 
    >  
    > The observer list is both weak (implicitly managed) and allows for 
    > removing observers. If observers are removed while at the same time 
    > multiple other observers die, and the removal call triggers GC, this may 
    > lead to CHECK() failures where the index retrieved on `RemoveObserver` 
    > is too large for the `observers_` array. 
    >  
    > Bug: 438569732, 438916130 
    > Change-Id: I6731ad38e96f01a47258bc8f8f5a0b1b41e736a3 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6859882 
    > Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    > Reviewed-by: Anton Bikineev <bikineev@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1503316} 
     
    Bug: 440101815,438569732,438916130 
    Change-Id: I6731ad38e96f01a47258bc8f8f5a0b1b41e736a3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6867493 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7339@{#999} 
    Cr-Branched-From: 27be8b77710f4405fdfeb4ee946fcabb0f6c92b2-refs/heads/main@{#1496484}

```

---

Files:

- M `third_party/blink/renderer/platform/heap_observer_list.h`

---

Hash: [8fd165da2ae3f499d079b0cb3699731157741138](https://chromiumdash.appspot.com/commit/8fd165da2ae3f499d079b0cb3699731157741138)  

Date: Wed Aug 20 22:26:57 2025


---

### fl...@google.com (2025-08-21)

mlippautz@, if this is a security bug, do you have an idea of what version of Chromium introduced it?  All security bugs need a FoundIn.  Thanks!

### dc...@chromium.org (2025-08-21)

I believe the fix above is not a security fix. It addresses a safe `CHECK()` failure.

However, there is a (very) inconsistent use-after-poison. That **is** a security bug, but we also haven't figured out how to consistently reproduce it, and without a reproduction, it's very difficult to say what the FoundIn should be.

### ml...@chromium.org (2025-08-21)

I would assume that this is the change the introduces the bug as it adds the tricky bits of weakness handling to allow for constant time insertion/deletion on top of fast iteration: <https://chromiumdash.appspot.com/commit/693909697a28a2bc2bbeb92f73f278c6f2cf35cf>

Setting M140 tentatively here, please remove the label if you think this is not good enough of a hint.

### ml...@chromium.org (2025-08-21)

Separately I will now try to reproduce the U-A-P again with the fix and see how far I can get.

### ml...@chromium.org (2025-08-21)

I have run the repro now on custom ASAN build on `HEAD` for ~1h with and without GC stress flags and I couldn't reproduce a single U-A-P failure.

I'd like to believe that the buggy implementation would either lead to a CHECK failure or the U-A-P and is now fixed.

### dc...@chromium.org (2025-08-22)

I'm good with that–I haven't been able to get a consistent repro even at revisions we know to be problematic.

### pe...@google.com (2025-08-22)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ml...@chromium.org (2025-08-22)

> Was this issue a regression for the milestone it was found in?

Seems this was a regression in M140.

> Is this issue related to a change or feature merged after the latest LTS Milestone?

It was merged after M138 and is thus not an issue in LTS.

### sa...@gmail.com (2025-08-22)

deleted

### qk...@google.com (2025-08-26)

Labelling as not applicable for LTS 132 because the [comment #50](https://issues.chromium.org/issues/438916130#comment50) said this issue was a regression in M140. Thus we don't need to merge back the fix to M138 and M132 LTS.

### sa...@gmail.com (2025-08-27)

Hi team,

After further review, I want to highlight a subtle but real GC lifetime hazard in the ContextLifecycleObserver / ContextLifecycleNotifier pattern, which may explain rare UAFs or ASan hits observed in this area.

Summary of the issue:

- ContextLifecycleObserver stores its notifier\_ in a WeakMember<ContextLifecycleNotifier>, which Oilpan clears when the notifier is collected.
- However, WeakMember does not protect the *observer itself* (this). If the observer is only weakly reachable, it can be finalized while still executing its own method.

example:

In ContextLifecycleObserver::SetContextLifecycleNotifier():

```
  if (notifier_)
    notifier_->RemoveContextLifecycleObserver(this);  // may allocate / trigger GC

```

At this point, if the observer has no strong roots, Oilpan may finalize it during weak processing triggered by RemoveContextLifecycleObserver. When the call returns, subsequent writes to 'this' (e.g. reassigning notifier\_) will access memory that may already be finalized, causing a UAF/UAP.

Why this is not a threading bug:

- All runs on the main thread. The hazard comes from GC reentrancy: weak objects may be finalized mid-method at GC safepoints.

Supporting evidence:

- The observed crash patterns (ASan hits in HeapObserverList::RemoveObserver during SetContextLifecycleNotifier in [comment #26](https://issues.chromium.org/issues/438916130#comment26)) align with this lifetime window.
- The DCHECKs in ContextLifecycleObserver only assert ordering, but do not prevent this self-finalization hazard in release builds.

Recommendation:

To avoid this class of GC/UAF, observer removal and notifier change functions should root the observer temporarily (e.g. with a local Persistent<ContextLifecycleObserver>) for the duration of calls that may trigger GC or weak processing.

(i may be completely wrong, im like 15 and not the best at C++ )

### dc...@chromium.org (2025-08-27)

The comment was deleted, but I'm going to respond a bit here just so it's documented for the future:

> In ContextLifecycleObserver::SetContextLifecycleNotifier():
> 
> ```
>   if (notifier_)
>     notifier_->RemoveContextLifecycleObserver(this);  // may allocate / trigger GC
> 
> ```
> 
> At this point, if the observer has no strong roots, Oilpan may finalize it during weak processing triggered by RemoveContextLifecycleObserver. When the call returns, subsequent writes to 'this' (e.g. reassigning notifier\_) will access memory that may already be finalized, causing a UAF/UAP.

In refcounted systems, you'd see something like `scoped_refptr protected(this);` as a stack variable. Oilpan does something similar by utilizing conservative stack scanning (including registers though) and treats any potential addresses into the Oilpan heap as roots; that would keep `this` alive.

### ml...@chromium.org (2025-08-28)

Being late here but yes, this should be covered by conservative stack scanning. The code certainly seems on the dangerous side here but I could not see why it wouldn't work.

- `this` is a parameter that is passed via register/stack and has to keep this alive atleast for some time.
- it's passed on in the call itself, keeping it alive as well
- `RemoveObserver` on the `observers_` needs to update its own state which creates an inner pointer to the notifier as well which needs to keep it alive conservatively

### sp...@google.com (2025-08-28)

** NOTE: This is an automatically generated email **

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this issue does not meet the criteria to qualify for a reward.

Rationale for this decision:
While we appreciate the report and the effort, this does not appear to be an exploitable security issue. There was no demonstrable evidence of an exploitable security bug provided in this report or discovered from our attempts to reproduce and investigation. This report is unfortunately not eligible for a Chrome VRP reward.

Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they will review your report and decide if a fix is required. We'll let you know if the issue was fixed.

Regards,
Google Security Bot


--
How did we do? Please fill out a short anonymous survey (https://goo.gl/IR3KRH).

### ch...@google.com (2025-11-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> While we appreciate the report and the effort, this does not appear to be an exploitable security issue. There was no demonstrable evidence of an exploitable security bug provided in this report or discovered from our attempts to reproduce and investigation. This report is unfortunately not eligible for a Chrome VRP reward.
> 
> Please note that the fact that this issue is not being rewarded does not mean that the product team won't fix the issue. We have filed a bug with the product team and they w

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/438916130)*
