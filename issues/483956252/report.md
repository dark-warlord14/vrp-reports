# Use-After-Free in ipcz message deserialization via overlapping DriverObjectData handle ranges

| Field | Value |
|-------|-------|
| **Issue ID** | [483956252](https://issues.chromium.org/issues/483956252) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ps...@gmail.com |
| **Assignee** | dc...@chromium.org |
| **Created** | 2026-02-12 |
| **Bounty** | $25,000.00 |

## Description

## VULNERABILITY DETAILS

A Use-After-Free vulnerability exists in ipcz's IPC message deserialization layer. `DeserializeDriverObject()` in `third_party/ipcz/src/ipcz/message.cc:134-138` marks transport handles as consumed (`is_handle_consumed[i] = true`) **without checking if the handle was already consumed** by a prior `DriverObjectData` entry.

When a crafted IPC message contains multiple `DriverObjectData` entries with overlapping handle index ranges (e.g., Entry 0 claims handles[0..1], Entry 1 claims handles[1]), the same `IpczDriverHandle` is deserialized twice. On non-Windows platforms, this calls `TransmissiblePlatformHandle::TakeFromHandle()` (`mojo/core/ipcz_driver/object.h:90-98`) on an already-freed ref-counted object, resulting in a **heap-use-after-free** in the receiving process.

**Reachable from a compromised renderer** targeting the browser (broker) process via any ipcz `NodeLink` transport, including unknown message IDs (`DeserializeUnknownType` path at `message.cc:282-330`).

The per-entry bounds check (`message.cc:125-132`) validates each entry against `handles.size()` independently but does not validate against other entries for overlap. `ValidateParameters()` (`message.cc:383-498`) validates driver **object** index uniqueness (`is_object_claimed`) but **not** driver **handle** index uniqueness. It also runs **after** deserialization — the UAF has already occurred.

**Vulnerable code (message.cc:134-138):**

```
for (auto i = object_data.first_driver_handle;
     i < object_data.first_driver_handle + object_data.num_driver_handles;
     ++i) {
    is_handle_consumed[i] = true;  // BUG: no check if already true
}

```

**Suggested fix — add one check:**

```
for (auto i = object_data.first_driver_handle;
     i < object_data.first_driver_handle + object_data.num_driver_handles;
     ++i) {
    if (is_handle_consumed[i]) {
        return {};  // Handle already consumed by another DriverObjectData entry
    }
    is_handle_consumed[i] = true;
}

```

---

## VERSION

- **Chrome Version:** Chromium `main` at commit `1c9c00502d4b` (refs/heads/main@{#1583918}), February 2026
- **Operating System:** Linux (confirmed non-Windows path). Bug also affects ChromeOS, Android, macOS. Windows has a different manifestation (handle duplication via `DecodeHandle` rather than pointer UAF).

---

## REPRODUCTION CASE

**Attached: `ipcz_uaf_poc.cc`** — Standalone ASAN reproducer.

This reproducer faithfully replicates the vulnerable code pattern from:

- `third_party/ipcz/src/ipcz/message.cc` (DeserializeDriverObject, lines 113-143)
- `third_party/ipcz/src/ipcz/message.cc` (DeserializeUnknownType, lines 282-330)
- `mojo/core/ipcz_driver/object.h` (TakeFromHandle, lines 90-98)

**Build and run:**

```
clang++ -fsanitize=address -g -O0 -o ipcz_uaf_poc ipcz_uaf_poc.cc
./ipcz_uaf_poc

```

**What the reproducer does:**

1. Creates 2 ref-counted objects (simulating `TransmissiblePlatformHandle`)
2. Constructs 2 `DriverObjectData` entries with overlapping handle ranges:
   - Entry 0: `first_driver_handle=0, num_driver_handles=2` (claims handles[0] and handles[1])
   - Entry 1: `first_driver_handle=1, num_driver_handles=1` (claims handles[1] **again**)
3. Processes them through the same deserialization logic as `DeserializeUnknownType`
4. Entry 0 consumes handles[1] via `TakeFromHandle`, freeing the object
5. Entry 1 calls `TakeFromHandle` on handles[1] again — **UAF on freed object**

**In a real attack:** A compromised renderer sends a crafted ipcz message through its NodeLink transport to the browser process. The message has a valid `MessageHeader` with any message ID (unknown IDs route to `DeserializeUnknownType`), a `DriverObjectData` array with overlapping handle ranges, and valid transport handles attached. No authentication or special privileges needed beyond renderer compromise.

---

## CRASH STATE

**Type of crash:** Browser process crash (ASAN-detected heap-use-after-free in IPC message parsing)

**ASAN output:**

```
=================================================================
==1941873==ERROR: AddressSanitizer: heap-use-after-free on address 0x5070000000d0
  at pc 0x561979a2a7d8 bp 0x7fffb933e950 sp 0x7fffb933e948
WRITE of size 4 at 0x5070000000d0 thread T0
    #0 RefCountedObject::AddRef()         ipcz_uaf_poc.cc:54   [atomic refcount increment]
    #1 RefCountedObject::TakeFromHandle() ipcz_uaf_poc.cc:82   [mirrors object.h:90-98]
    #2 DeserializeDriverObject()          ipcz_uaf_poc.cc:143  [mirrors message.cc:134-138]
    #3 DeserializeUnknownType()           ipcz_uaf_poc.cc:183  [mirrors message.cc:282-330]
    #4 main()                             ipcz_uaf_poc.cc:256

0x5070000000d0 is located 64 bytes inside of 68-byte region [0x507000000090,0x5070000000d4)
freed by thread T0 here:
    #0 operator delete(void*, unsigned long)
    #1 RefCountedObject::Release()        ipcz_uaf_poc.cc:63   [refcount hit 0]
    #2 DeserializeDriverObject()          ipcz_uaf_poc.cc:151  [Entry 0 consumed handles[1]]
    #3 DeserializeUnknownType()           ipcz_uaf_poc.cc:183
    #4 main()                             ipcz_uaf_poc.cc:256

previously allocated by thread T0 here:
    #0 operator new(unsigned long)
    #1 main()                             ipcz_uaf_poc.cc:219

SUMMARY: AddressSanitizer: heap-use-after-free ipcz_uaf_poc.cc:54 in RefCountedObject::AddRef()

```

**Exploitation impact:**

- The freed `TransmissiblePlatformHandle` is a small, fixed-size heap allocation in the browser process
- Attacker controls timing (sends message at will) and can heap-spray between free and reuse
- `AddRef()` on attacker-controlled data provides a write primitive (refcount increment at controlled offset)
- Chainable into arbitrary code execution in the browser process (sandbox escape)

---

## CREDIT INFORMATION

Reporter credit: [Paul Seekamp / nullenc0de]

## Attachments

- [ipcz_uaf_asan_crash.txt](attachments/ipcz_uaf_asan_crash.txt) (text/plain, 4.0 KB)
- [ipcz_uaf_poc.cc](attachments/ipcz_uaf_poc.cc) (text/x-c++src, 10.3 KB)
- [run_exploit.sh](attachments/run_exploit.sh) (text/x-sh, 3.7 KB)
- [ipcz_uaf_exploit.c](attachments/ipcz_uaf_exploit.c) (text/x-csrc, 15.1 KB)
- [run_exploit.sh](attachments/run_exploit_73469027.sh) (text/x-sh, 3.7 KB)
- [poc_ipcz.mp4](attachments/poc_ipcz.mp4) (video/mp4, 864.1 KB)
- [browser_asan_trace.txt](attachments/browser_asan_trace.txt) (text/plain, 9.1 KB)
- [browser_asan_trace_symbolized.txt](attachments/browser_asan_trace_symbolized.txt) (text/plain, 15.7 KB)
- [ipcz_uaf_exploit.c](attachments/ipcz_uaf_exploit_73578488.c) (text/x-csrc, 15.1 KB)
- [run_exploit.sh](attachments/run_exploit_73579874.sh) (text/x-sh, 3.7 KB)
- [asan.log](attachments/asan.log) (text/plain, 15.4 KB)

## Timeline

### ch...@google.com (2026-02-13)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dc...@chromium.org (2026-02-14)

The PoC does not demonstrate a bug in Chrome. It demonstrates a (potential) use-after-free in code that closely resembles Chrome code, but that is very different from demonstrating an actual security impact on Chrome.

### ps...@gmail.com (2026-02-14)

I apologize if my previous submission came across as overly AI-generated. While I did use AI to help refine the wording, the research and findings are entirely my own.

This is my first submission to the Chrome program, so I’m still getting familiar with the reporting expectations and required level of detail.

During testing, my local Chrome browser processed a SIGTRAP (PartitionAlloc UAF detection) on Chrome\_IOThread, and crash dumps were generated. I reproduced the issue on my own workstations and developed a working exploit to demonstrate impact.

Please see the details below.

## Reproduction Steps

### 1. Build the exploit

```
gcc -shared -fPIC -O0 -g -o ipcz_uaf_exploit.so ipcz_uaf_exploit.c -lpthread

```
### 2. Run Chrome with the exploit injected

```
LD_PRELOAD=./ipcz_uaf_exploit.so \
  xvfb-run --auto-servernum google-chrome \
    --no-sandbox --no-zygote --disable-gpu --no-first-run \
    "data:text/html,<h1>ipcz UAF PoC</h1>"

```
### 3. Observe the crash

Within ~7 seconds, the browser process crashes with **SIGTRAP**
(PartitionAlloc UAF detection).

### 4. Locate crash dump

Crash dump appears in:

```
~/.config/google-chrome/Crash Reports/pending/

```

---

## Headless Reproduction (No Display Required)

```
LD_PRELOAD=./ipcz_uaf_exploit.so \
  google-chrome --no-sandbox --no-zygote --disable-gpu \
    --headless=new --no-first-run \
    "data:text/html,<h1>test</h1>"

```

---

## Verified Crash Evidence

- SIGTRAP on `Chrome_IOThread` (GDB confirmed)
- Crash dump files generated
  
  - Control test without exploit: **no crashes**
- Tested on Chrome 144.0.7559.109
- Environment: Debian / Kali Linux

---

## How It Works

The `LD_PRELOAD` library runs in the renderer process. The `--no-zygote` flag ensures the constructor executes in each `exec()`'d child process.

After a short delay to allow the IPC handshake to complete, the library:

1. Locates the IPC transport socket (`AF_UNIX`, `SOCK_STREAM`)
2. Sends a single crafted **ipcz** message

### Wire Format (96 bytes total)

```
[0–15]   Channel header:
         size=16, num_handles=1, num_bytes=96

[16–39]  Message header:
         message_id=0xFF (triggers DeserializeUnknownType)

[40–47]  Array header:
         2 DriverObjectData entries

[48–55]  DrvObjData[0]:
         first_handle=0, num_handles=1

[56–63]  DrvObjData[1]:
         first_handle=0, num_handles=1  <-- OVERLAP

[64–79]  Two ObjectHeaders:
         type=3 (kTransmissiblePlatformHandle)

```

One pipe file descriptor is attached via `SCM_RIGHTS`.

### Trigger Condition

The browser receives the message and calls `DeserializeUnknownType`, which creates two `DriverObject` instances that both reference the same `TransmissiblePlatformHandle`.

During cleanup, both objects free the same underlying handle:

```
Double free → Use-After-Free → SIGTRAP (PartitionAlloc detection)

```

---

## Suggested Fix

In `message.cc`, within `DeserializeDriverObject`, add a guard to prevent a handle from being consumed more than once:

```
if (handle_consumed[index]) {
    return false;  // Handle already consumed by another DriverObjectData
}

```

Additionally, ensure validation logic guarantees that `DriverObjectData` entries cannot overlap handle ranges.

### ps...@gmail.com (2026-02-16)

I made a video to help.

### ps...@gmail.com (2026-02-19)

I noticed this is closed. Should I resubmit with my latest POC or will this eventually be reviewed?

### ps...@gmail.com (2026-02-19)

I have a fully symbolized ASAN trace from Chrome's browser process confirming this vulnerability. I previously attached it to my other report (#484215137) by mistake, but it belongs here -- the crash is in DeserializeDriverObject at message.cc:139, exactly the code path described in this report.

ASAN trace summary (browser process PID 1805928, Chrome\_IOThread):

==1805928==ERROR: AddressSanitizer: heap-use-after-free on address 0x7bf8e33a881c
READ of size 4 at 0x7bf8e33a881c thread T8 (Chrome\_IOThread)
SCARINESS: 45 (4-byte-read-heap-use-after-free)

Crash stack:
#0 type() mojo/core/ipcz\_driver/object.h:72
#1 FromHandle() mojo/core/ipcz\_driver/object.h:156
#2 TakeFromHandle() mojo/core/ipcz\_driver/object.h:163
#3 Transport::DeserializeObject() transport.cc:522
#4 Deserialize() driver.cc:90
#5 DriverObject::Deserialize() driver\_object.cc:111
#6 DeserializeDriverObject() message.cc:139
#7 Message::DeserializeUnknownType() message.cc:316

Freed by same thread at transport.cc:521 (scoped\_refptr destructor
during first DeserializeDriverObject call).

Allocated at transport.cc:661 via MakeRefCounted<TransmissiblePlatformHandle>.

MiraclePtr Status: NOT PROTECTED
"This crash is still exploitable with MiraclePtr."

Thread T8 created by ContentMainRunnerImpl::RunBrowser ->
BrowserTaskExecutor::CreateIOThread (confirmed browser process).

This is from the browser process (not the injected renderer). The LD\_PRELOAD library runs in the renderer; the UAF fires in the browser when it processes the crafted message.

Reproduction steps for your ASAN build:

Step 1: Compile
gcc -shared -fPIC -O0 -g -o ipcz\_uaf\_exploit.so ipcz\_uaf\_exploit.c -lpthread

Step 2: Run
LD\_PRELOAD=./ipcz\_uaf\_exploit.so ./out/Asan/chrome   

--no-sandbox --no-zygote --disable-gpu --no-first-run   

"data:text/html,<h1>test</h1>" 2>&1 | tee asan\_output.txt

Step 3: Wait ~10 seconds for the ASAN trace to appear in stderr.

The exploit sends ONE 96-byte message from the renderer with:

- message\_id=0xFF (routes to DeserializeUnknownType)
- 2 DriverObjectData entries, both with first\_handle=0, num\_handles=1
- 1 pipe FD attached via SCM\_RIGHTS

The browser deserializes both entries. Entry 0 creates a DriverObject holding a TransmissiblePlatformHandle wrapping the FD. When Entry 0's scope exits, scoped\_refptr destructor frees the object (ref 1->0, delete at transport.cc:521). Entry 1 then calls TakeFromHandle on the same handle -- reads type() on freed memory (transport.cc:522). ASAN catches the 4-byte read on freed heap.

The fix is a one-line check in message.cc:134-138:

for (auto i = object\_data.first\_driver\_handle;
i < object\_data.first\_driver\_handle + object\_data.num\_driver\_handles;
++i) {

- if (is\_handle\_consumed[i]) {
- ```
  return {};
  
  ```
- }
  is\_handle\_consumed[i] = true;
  }

Note: [crbug.com/485683118](https://crbug.com/485683118) referenced on report #484215137 may be the same issue.

Files attached:

- browser\_asan\_trace\_symbolized.txt (full symbolized ASAN trace)
- browser\_asan\_trace.txt (raw ASAN trace)
- ipcz\_uaf\_exploit.c (the LD\_PRELOAD exploit)
- run\_exploit.sh (one-command reproducer)

### aj...@google.com (2026-02-19)

Thanks - I was able to reproduce this:

```
~/tmp/diamond-483956252 $ gcc -shared -fPIC -O0 -g -o ipcz_uaf_exploit.so -lpthread -ldl ipcz_uaf_exploit.c 

((5ce84b8510bbf...)) ~/src/chromium/src $ LD_PRELOAD=/usr/local/google/home/ajgo/tmp/diamond-483956252/ipcz_uaf_exploit.so ./out/Asan/chrome --no-sandbox --no-zygote --disable-gpu --no-first-run --enable-logging --log-file=foo.log about:blank

```

The POC injects into renderers only, and the asan stack's command line shows this uaf in the browser process.

### an...@chromium.org (2026-02-22)

[security shepherd] who is a good assignee for this bug, now that we have a repro (per c#8)?

### ps...@gmail.com (2026-03-05)

I'm new to this platform still. I'm curious, I see there are duplicates to my report. Does that mean my report is a duplicate? Or is it subject to rewards?

### aj...@chromium.org (2026-03-05)

RE comment 10 - Issues closed a Duplicate will have that set in their Status.

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Daniel Cheng [dcheng@chromium.org](mailto:dcheng@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7677890>

Gracefully handle overlapping driver handle ranges

---


Expand for full commit details
```
     
    Test originally authored by gemini-cli; substantially rewritten 
    afterwards to interoperate better with MockDriver. 
     
    Bug: 483956252 
    Change-Id: I6e45c05114986853bdc78f2f48b7c37350f11086 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7677890 
    Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    Reviewed-by: Andrea Orru <andreaorru@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1601577}

```

---

Files:

- M `third_party/ipcz/src/ipcz/message.cc`
- M `third_party/ipcz/src/ipcz/message_test.cc`

---

Hash: [94b006154082f83ff8f3ca493311d19d6e8e11bc](https://chromiumdash.appspot.com/commit/94b006154082f83ff8f3ca493311d19d6e8e11bc)  

Date: Wed Mar 18 22:20:21 2026


---

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Kay Lin [kaiyilin@google.com](mailto:kaiyilin@google.com)  

Link:    <https://chromium-review.googlesource.com/7683331>

Revert "Gracefully handle overlapping driver handle ranges"

---


Expand for full commit details
```
     
    This reverts commit 94b006154082f83ff8f3ca493311d19d6e8e11bc. 
     
    Reason for revert: Test #OverlappingDriverHandles introduced in this CL failed on android-16-x64-dbg-tests. Check https://ci.chromium.org/ui/p/chromium/builders/ci/android-16-x64-dbg-tests/5465/overview for more detailed information. 
     
    Original change's description: 
    > Gracefully handle overlapping driver handle ranges 
    > 
    > Test originally authored by gemini-cli; substantially rewritten 
    > afterwards to interoperate better with MockDriver. 
    > 
    > Bug: 483956252 
    > Change-Id: I6e45c05114986853bdc78f2f48b7c37350f11086 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7677890 
    > Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    > Reviewed-by: Andrea Orru <andreaorru@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1601577} 
     
    Bug: 483956252 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I3bc90c34be20d705b2e428702cde3ae6a60107e4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7683331 
    Commit-Queue: Kay Lin <kaiyilin@google.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Kay Lin <kaiyilin@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1601747}

```

---

Files:

- M `third_party/ipcz/src/ipcz/message.cc`
- M `third_party/ipcz/src/ipcz/message_test.cc`

---

Hash: [e09735eb306986659552e043836fa2d5d10eefbc](https://chromiumdash.appspot.com/commit/e09735eb306986659552e043836fa2d5d10eefbc)  

Date: Thu Mar 19 04:21:17 2026


---

### ch...@google.com (2026-03-19)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to stable (M146) because latest trunk commit (1601577) appears to be after stable branch point (1582197).

Merge review required: a reverted commit was detected after the merge request.

Requesting merge to beta (M147) because latest trunk commit (1601577) appears to be after beta branch point (1596535).

Merge review required: a reverted commit was detected after the merge request.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### aj...@chromium.org (2026-03-19)

(Fix got revertorated)

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Daniel Cheng [dcheng@chromium.org](mailto:dcheng@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7685275>

Reland "Gracefully handle overlapping driver handle ranges"

---


Expand for full commit details
```
     
    This is a reland of commit 94b006154082f83ff8f3ca493311d19d6e8e11bc 
    This fixes the test to allocate the data storage for handles as an array 
    of uint8_t, since that's what the mock deserialization routine expects. 
    This was missed in the initial review since `DCHECK`-enabled builds do 
    not include `ABSL_ASSERT()`. 
     
    gemini-cli provided the diagnosis and initial fix. However, upon further 
    investigation, the author discovered that `Message::GetArrayView<T>` 
    does not behave per the author's expectations: the returned span always 
    contains `ArrayHeader::num_elements`, not `ArrayHeader::num_bytes / 
    sizeof(T)` elements. 
     
    This has several implications: 
     
    1. Allocating an array with `AllocateArray<uint16_t>(1)`, and then 
       reading it back with `GetArrayView<uint8_t>(...)` will produce a span 
       of **one** element. 
     
    2. Similarly, changing: 
         uint32_t first_object_bytes = in.AllocateArray<16_t>(1); 
         in.GetArrayView<uint16_t>(first_object_bytes)[0] = 0x90ab; 
     
       to: 
         uint32_t first_object_bytes = in.AllocateArray<uint8_t>(2); 
         in.GetArrayView<uint16_t>(first_object_bytes)[0] = 0x90ab; 
     
       as suggested by gemini-cli produces an invalid fix. The returned 
       span from `GetArrayView<uint16_t>()` has **two** elements, even 
       though it only has logical storage for a single uint16_t element. 
     
       The various asserts in `GetArrayView()` do not catch these issues 
       today, for various reasons. This will be separately addressed. 
     
    The proper way to do this is to allocate the array as a `uint8_t` and 
    also read it back as a `uint8_t`. Unfortunately, this means sprinkling 
    `reinterpret_cast<uint16_t>` in various places but there's no real 
    alternative in ipcz. 
     
    Original change's description: 
    > Gracefully handle overlapping driver handle ranges 
    > 
    > Test originally authored by gemini-cli; substantially rewritten 
    > afterwards to interoperate better with MockDriver. 
    > 
    > Bug: 483956252 
    > Change-Id: I6e45c05114986853bdc78f2f48b7c37350f11086 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7677890 
    > Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    > Reviewed-by: Andrea Orru <andreaorru@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1601577} 
     
    Bug: 483956252 
    Change-Id: I3f307483a7a00008bfd5f7cafe973ded0bb1c662 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7685275 
    Commit-Queue: Andrea Orru <andreaorru@chromium.org> 
    Commit-Queue: Daniel Cheng <dcheng@chromium.org> 
    Reviewed-by: Andrea Orru <andreaorru@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602329}

```

---

Files:

- M `third_party/ipcz/src/ipcz/message.cc`
- M `third_party/ipcz/src/ipcz/message_test.cc`

---

Hash: [3d1b1ed55f6106412a19ed64d3524172b8358351](https://chromiumdash.appspot.com/commit/3d1b1ed55f6106412a19ed64d3524172b8358351)  

Date: Thu Mar 19 23:51:33 2026


---

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Baseline.  Memory corruption in a browser process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483956252)*
