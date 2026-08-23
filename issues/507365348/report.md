# SpdyStream Use-After-Free in QueueNextDataFrame via PrefacePing drain

| Field | Value |
|-------|-------|
| **Issue ID** | [507365348](https://issues.chromium.org/issues/507365348) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Network>HTTP2 |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ci...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2026-04-28 |
| **Bounty** | $43,000.00 |

## Description

---

### Report description

SpdyStream Use-After-Free in QueueNextDataFrame via PrefacePing drain

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:net/spdy/spdy_stream.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

SpdyStream::QueueNextDataFrame() calls SpdySession::CreateDataBuffer() with pending\_send\_data\_.get(). For non-empty DATA frames, CreateDataBuffer() calls MaybeSendPrefacePing(). If that PING enqueue sees more than session\_max\_queued\_capped\_frames queued capped frames (default 10000), EnqueueSessionWrite() synchronously calls DoDrainSession().

The drain destroys the calling SpdyStream, including its pending\_send\_data\_ DrainableIOBuffer. Control then returns to CreateDataBuffer(), which continues with the stale data pointer and calls data->data() while constructing the DATA frame.

The attached PoC is tuned to avoid the previous reproduction race. It uses one HTTPS/HTTP2 origin, no mixed-content control plane, no manual pause/start endpoints, and an automatic server-side read pause after all flow streams and the bulk POST headers are observed.

Default PoC math:  

streams=240  

full cycles=41  

final partial cycle streams=119  

stream WINDOW\_UPDATE frames = 41 \* 240 + 119 = 9959  

connection WINDOW\_UPDATE frames = 41 full cycles + 1 partial cycle = 42  

total capped frames queued before trigger = 9959 + 42 = 10001

After the 10001 capped frames are queued client-side, the page waits 11500ms to satisfy the PrefacePing idle gate, then sends 1024 bytes on the trigger POST body. That body enters QueueNextDataFrame(), reaches CreateDataBuffer(), attempts to enqueue PrefacePing, drains the session, destroys the calling SpdyStream, and crashes when CreateDataBuffer() resumes with the stale data pointer.

### Steps to Reproduce

1. Save poc.html and server.py in the same folder
2. `pip3 install h2`
3. `python3 server.py`
4. Launch Chromium directly to the server URL (<https://localhost:8443/poc.html>). Do not open poc.html as a file:// URL. Accept the self-signed HTTPS certificate.

```
~/chromium/src/out/ASan/Chromium.app/Contents/MacOS/Chromium https://localhost:8443/poc.html

```

5. Wait approximately **4 minutes** then ASan reports:

```
==80749==ERROR: AddressSanitizer: heap-use-after-free on address 0x60400069a460 at pc 0x0003793905e0 bp 0x00016fbb5490 sp 0x00016fbb5488
READ of size 8 at 0x60400069a460 thread T9
    #0 net::SpdySession::CreateDataBuffer(...)
    #1 net::SpdyStream::QueueNextDataFrame()
    #2 net::SpdyStream::SendData(...)
[...]
MiraclePtr Status: NOT PROTECTED

```
#### Crash Evidence

**Chromium 149.0.7813.0 (Developer Build, ASan) (arm64) - macOS 15 (Apple M5)**

- Attached `asan_symbolized.txt`

**Chrome Stable 147.0.7727.101 - Android 16 (Pixel 10, arm64)**

- Attached `android_tombstone.txt` showing NetworkService SIGTRAP and chrome://crashes ID `056da228154b34fe`

**Chrome Dev 149.0.7806.0 - Android 16 (Pixel 10, arm64)**

- chrome://crashes ID `21e0879a6b27018d`

### Proposed Fix

Do not call MaybeSendPrefacePing() from inside SpdySession::CreateDataBuffer() while CreateDataBuffer() holds raw pointers into the calling SpdyStream. Move the PrefacePing enqueue to a point where the caller can guard SpdyStream lifetime with a WeakPtr before passing pending\_send\_data\_.get(), or otherwise make CreateDataBuffer() verify stream/data lifetime after MaybeSendPrefacePing() before dereferencing data. A post-call guard in QueueNextDataFrame() alone is insufficient because the stale data pointer is dereferenced inside CreateDataBuffer().

### Bisect

Introduced by commit 410676ab9660a (HTTP2 DoS Mitigations, 2019-08-13), which added the synchronous drain in EnqueueSessionWrite() when the capped-frame queue exceeds the configured limit.

#### Impact analysis

- Web-reachable, no compromised renderer required.
- Heap use-after-free in the network service process.
- Default HTTP/2 configuration; no special feature flags required.

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7813.0 (Developer Build) (arm64)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

cinzinga

## Attachments

- [server.py](attachments/server.py) (text/x-python-script, 14.4 KB)
- [android_tombstone.txt](attachments/android_tombstone.txt) (text/plain, 865.2 KB)
- [poc.html](attachments/poc.html) (text/html, 5.8 KB)
- [asan_symbolized.txt](attachments/asan_symbolized.txt) (text/plain, 42.3 KB)
- [asan_out.txt](attachments/asan_out.txt) (text/plain, 41.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 36.0 KB)

## Timeline

### ci...@gmail.com (2026-04-28)

Confirming the attached POC+server downloaded from this submission works on Chromium 149.0.7787.0 (Developer Build) (x86\_64) - macOS 15 (Intel).

### ct...@chromium.org (2026-04-28)

Thanks for the updated POC! I have been able to reproduce on macOS M149 ASAN. Full confirmation ASAN log attached, excerpt below:

```
=================================================================
==92228==ERROR: AddressSanitizer: heap-use-after-free on address 0x6040005887a0 at pc 0x000314fd5174 bp 0x0001712ed630 sp 0x0001712ed628
READ of size 8 at 0x6040005887a0 thread T9
==92228==WARNING: invalid path to external symbolizer!
==92228==WARNING: Failed to use and restart external symbolizer!
    #0 0x000314fd5170 in net::SpdySession::CreateDataBuffer(unsigned int, net::IOBuffer*, int, spdy::SpdyDataFlags, int*, bool*)+0xa58 (/Users/cthomp/scratch/asan-canary/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7811.0/Chromium Framework:arm64+0x14fd5170)
    #1 0x00031501aa10 in net::SpdyStream::QueueNextDataFrame()+0x2c0 (/Users/cthomp/scratch/asan-canary/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7811.0/Chromium Framework:arm64+0x1501aa10)
    #2 0x00031501c39c in net::SpdyStream::SendData(net::IOBuffer*, int, net::SpdySendStatus)+0x22c (/Users/cthomp/scratch/asan-canary/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7811.0/Chromium Framework:arm64+0x1501c39c)
    #3 0x000314fa9ee8 in net::SpdyHttpStream::OnRequestBodyReadCompleted(int)+0x3e0 (/Users/cthomp/scratch/asan-canary/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7811.0/Chromium Framework:arm64+0x14fa9ee8)
    #4 0x000314fac2f0 in base::internal::Invoker<base::internal::FunctorTraits<void (net::SpdyHttpStream::*&&)(int), base::WeakPtr<net::SpdyHttpStream>&&>, base::internal::BindState<true, true, false, void (net::SpdyHttpStream::*)(int), base::WeakPtr<net::SpdyHttpStream>>, void (int)>::RunOnce(base::internal::BindStateBase*, int)+0x168 (/Users/cthomp/scratch/asan-canary/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7811.0/Chromium Framework:arm64+0x14fac2f0)
    #5 0x000314a154a4 in net::UploadDataStream::OnReadCompleted(int)+0x200 (/Users/cthomp/scratch/asan-canary/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7811.0/Chromium Framework:arm64+0x14a154a4)
    #6 0x0003182576ac in network::ChunkedDataPipeUploadDataStream::OnHandleReadable(unsigned int)+0x224 (/Users/cthomp/scratch/asan-canary/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/149.0.7811.0/Chromium Framework:arm64+0x182576ac)

```

Setting some security labels:

- FoundIn-146: this also repro'd for me on Linux M146 ASAN (extended stable)
- OS: All desktop + android
- Sev-Crit (S0): this is memory corruption in a privileged and unsandboxed process

Passing this to rch@ for net/spdy/OWNERS. Also cc'ing dschinazi@ from the original CL [crrev.com/c/1752387](https://crrev.com/c/1752387).

### ch...@google.com (2026-04-29)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-29)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### mm...@chromium.org (2026-05-06)

DoDrainSession() in the SPDY code is just so dangerous - this is the third issue we've run into with it that I'm aware of, and I would not be surprised if there are more. I think we may want to make it always async, but my current project is just not leaving me with time to do a deep dive into the code here, and I'm far from an expert on SPDY.

### ba...@chromium.org (2026-05-07)

> I think we may want to make it always async

I agree, but unfortunately I don't have the time to look into the sync drain problem in depth either.

I have uploaded a fix that drains session asynchronously in SpdySession::EnqueueSessionWrite().
<https://crrev.com/c/7825349>

### dx...@google.com (2026-05-11)

Project: chromium/src  

Branch:  main  

Author:  Kenichi Ishibashi [bashi@chromium.org](mailto:bashi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7825349>

Fix potential crash in SpdyStream::QueueNextDataFrame via PrefacePing drain

---


Expand for full commit details
```
     
    This CL fixes a potential crash in SpdyStream caused by accessing a 
    destroyed object when a session drain is triggered by a Preface Ping 
    hitting the capped frames limit. 
     
    SpdyStream::QueueNextDataFrame calls SpdySession::CreateDataBuffer, 
    which synchronously invokes MaybeSendPrefacePing if the connection has 
    been idle. If the number of queued capped frames already exceeds the max 
    allowed limit, EnqueueSessionWrite historically called DoDrainSession 
    synchronously. 
     
    DoDrainSession immediately destroys all active streams. Because this 
    happened synchronously inside the CreateDataBuffer call stack, the 
    stream's data buffer reference was dropped, causing subsequent data 
    frame serialization to access invalid memory, resulting in a crash. 
     
    This CL changes the synchronous DoDrainSession to DoDrainSessionAsync in 
    EnqueueSessionWrite when the cap is hit. This ensures the session is 
    marked unavailable immediately, but the actual stream destruction is 
    deferred to the next message loop tick, allowing the call stack to 
    unwind safely. 
     
    Bug: 507365348 
    Test: SpdySessionTest.SendDataExceedsCappedFramesLimitViaPrefacePing 
    Change-Id: I25b82c06a7218514ea664bd43767edf2ead9bcdc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7825349 
    Reviewed-by: mmenke <mmenke@chromium.org> 
    Commit-Queue: Kenichi Ishibashi <bashi@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1628325}

```

---

Files:

- M `net/spdy/spdy_session.cc`
- M `net/spdy/spdy_session.h`
- M `net/spdy/spdy_session_unittest.cc`

---

Hash: [eb721a86c032d2f945afb73fe45b3c101c4366d6](https://chromiumdash.appspot.com/commit/eb721a86c032d2f945afb73fe45b3c101c4366d6)  

Date: Mon May 11 01:54:31 2026


---

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $43000.00 for this report.

Rationale for this decision:
High quality with bisect. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925667](https://crbug.com/514925667) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514927846](https://crbug.com/514927846) to have this merge reviewed.**

### dx...@google.com (2026-05-21)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Kenichi Ishibashi [bashi@chromium.org](mailto:bashi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7862508>

[M149] Fix potential crash in SpdyStream::QueueNextDataFrame via PrefacePing drain

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix potential crash in SpdyStream::QueueNextDataFrame via PrefacePing drain 
    > 
    > This CL fixes a potential crash in SpdyStream caused by accessing a 
    > destroyed object when a session drain is triggered by a Preface Ping 
    > hitting the capped frames limit. 
    > 
    > SpdyStream::QueueNextDataFrame calls SpdySession::CreateDataBuffer, 
    > which synchronously invokes MaybeSendPrefacePing if the connection has 
    > been idle. If the number of queued capped frames already exceeds the max 
    > allowed limit, EnqueueSessionWrite historically called DoDrainSession 
    > synchronously. 
    > 
    > DoDrainSession immediately destroys all active streams. Because this 
    > happened synchronously inside the CreateDataBuffer call stack, the 
    > stream's data buffer reference was dropped, causing subsequent data 
    > frame serialization to access invalid memory, resulting in a crash. 
    > 
    > This CL changes the synchronous DoDrainSession to DoDrainSessionAsync in 
    > EnqueueSessionWrite when the cap is hit. This ensures the session is 
    > marked unavailable immediately, but the actual stream destruction is 
    > deferred to the next message loop tick, allowing the call stack to 
    > unwind safely. 
    > 
    > Bug: 507365348 
    > Test: SpdySessionTest.SendDataExceedsCappedFramesLimitViaPrefacePing 
    > Change-Id: I25b82c06a7218514ea664bd43767edf2ead9bcdc 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7825349 
    > Reviewed-by: mmenke <mmenke@chromium.org> 
    > Commit-Queue: Kenichi Ishibashi <bashi@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1628325} 
     
    (cherry picked from commit eb721a86c032d2f945afb73fe45b3c101c4366d6) 
     
    Bug: 514927846,507365348 
    Change-Id: I25b82c06a7218514ea664bd43767edf2ead9bcdc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7862508 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7827@{#1332} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `net/spdy/spdy_session.cc`
- M `net/spdy/spdy_session.h`
- M `net/spdy/spdy_session_unittest.cc`

---

Hash: [ab1d24f7a81fe622b58ddcb36e0dc7df0ecd8fe6](https://chromiumdash.appspot.com/commit/ab1d24f7a81fe622b58ddcb36e0dc7df0ecd8fe6)  

Date: Thu May 21 01:59:59 2026


---

### pe...@google.com (2026-05-21)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dx...@google.com (2026-05-21)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Kenichi Ishibashi [bashi@chromium.org](mailto:bashi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7865646>

[M148] Fix potential crash in SpdyStream::QueueNextDataFrame via PrefacePing drain

---


Expand for full commit details
```
     
    Original change's description: 
    > Fix potential crash in SpdyStream::QueueNextDataFrame via PrefacePing drain 
    > 
    > This CL fixes a potential crash in SpdyStream caused by accessing a 
    > destroyed object when a session drain is triggered by a Preface Ping 
    > hitting the capped frames limit. 
    > 
    > SpdyStream::QueueNextDataFrame calls SpdySession::CreateDataBuffer, 
    > which synchronously invokes MaybeSendPrefacePing if the connection has 
    > been idle. If the number of queued capped frames already exceeds the max 
    > allowed limit, EnqueueSessionWrite historically called DoDrainSession 
    > synchronously. 
    > 
    > DoDrainSession immediately destroys all active streams. Because this 
    > happened synchronously inside the CreateDataBuffer call stack, the 
    > stream's data buffer reference was dropped, causing subsequent data 
    > frame serialization to access invalid memory, resulting in a crash. 
    > 
    > This CL changes the synchronous DoDrainSession to DoDrainSessionAsync in 
    > EnqueueSessionWrite when the cap is hit. This ensures the session is 
    > marked unavailable immediately, but the actual stream destruction is 
    > deferred to the next message loop tick, allowing the call stack to 
    > unwind safely. 
    > 
    > Bug: 507365348 
    > Test: SpdySessionTest.SendDataExceedsCappedFramesLimitViaPrefacePing 
    > Change-Id: I25b82c06a7218514ea664bd43767edf2ead9bcdc 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7825349 
    > Reviewed-by: mmenke <mmenke@chromium.org> 
    > Commit-Queue: Kenichi Ishibashi <bashi@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1628325} 
     
    (cherry picked from commit eb721a86c032d2f945afb73fe45b3c101c4366d6) 
     
    Bug: 514925667,507365348 
    Change-Id: I25b82c06a7218514ea664bd43767edf2ead9bcdc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7865646 
    Commit-Queue: Kenichi Ishibashi <bashi@chromium.org> 
    Reviewed-by: mmenke <mmenke@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3356} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `net/spdy/spdy_session.cc`
- M `net/spdy/spdy_session.h`
- M `net/spdy/spdy_session_unittest.cc`

---

Hash: [f2c7cf1df943370540e9eb35caecf022429dd6a7](https://chromiumdash.appspot.com/commit/f2c7cf1df943370540e9eb35caecf022429dd6a7)  

Date: Thu May 21 02:34:34 2026


---

### pe...@google.com (2026-05-21)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-21)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7866603>
2. Low - There was a small conflict.
3. 149
4. Yes, the bug was introduced in 2019.

### dx...@google.com (2026-05-25)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Kenichi Ishibashi [bashi@chromium.org](mailto:bashi@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7866603>

[M144-LTS] Fix potential crash in SpdyStream::QueueNextDataFrame via PrefacePing drain

---


Expand for full commit details
```
     
    This CL fixes a potential crash in SpdyStream caused by accessing a 
    destroyed object when a session drain is triggered by a Preface Ping 
    hitting the capped frames limit. 
     
    SpdyStream::QueueNextDataFrame calls SpdySession::CreateDataBuffer, 
    which synchronously invokes MaybeSendPrefacePing if the connection has 
    been idle. If the number of queued capped frames already exceeds the max 
    allowed limit, EnqueueSessionWrite historically called DoDrainSession 
    synchronously. 
     
    DoDrainSession immediately destroys all active streams. Because this 
    happened synchronously inside the CreateDataBuffer call stack, the 
    stream's data buffer reference was dropped, causing subsequent data 
    frame serialization to access invalid memory, resulting in a crash. 
     
    This CL changes the synchronous DoDrainSession to DoDrainSessionAsync in 
    EnqueueSessionWrite when the cap is hit. This ensures the session is 
    marked unavailable immediately, but the actual stream destruction is 
    deferred to the next message loop tick, allowing the call stack to 
    unwind safely. 
     
    (cherry picked from commit eb721a86c032d2f945afb73fe45b3c101c4366d6) 
     
    Bug: 507365348 
    Test: SpdySessionTest.SendDataExceedsCappedFramesLimitViaPrefacePing 
    Change-Id: I25b82c06a7218514ea664bd43767edf2ead9bcdc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7825349 
    Reviewed-by: mmenke <mmenke@chromium.org> 
    Commit-Queue: Kenichi Ishibashi <bashi@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1628325} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7866603 
    Reviewed-by: Kenichi Ishibashi <bashi@chromium.org> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4887} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `net/spdy/spdy_session.cc`
- M `net/spdy/spdy_session.h`
- M `net/spdy/spdy_session_unittest.cc`

---

Hash: [f07bf251b47b4bae6a5c2b06475352c7159a44a4](https://chromiumdash.appspot.com/commit/f07bf251b47b4bae6a5c2b06475352c7159a44a4)  

Date: Mon May 25 16:36:57 2026


---

### ch...@google.com (2026-08-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/507365348)*
