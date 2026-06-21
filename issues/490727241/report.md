# Use-after-poison in InspectorMediaEventHandler::SendQueuedMediaEvents via canvas.captureStream() (zero interaction)

| Field | Value |
|-------|-------|
| **Issue ID** | [490727241](https://issues.chromium.org/issues/490727241) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | hu...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2026-03-08 |
| **Bounty** | $7,000.00 |

## Description

# Use-after-poison in InspectorMediaEventHandler::SendQueuedMediaEvents via canvas.captureStream() (zero interaction)

## Security Bug

---

## VULNERABILITY DETAILS

A dangling `raw_ptr<blink::MediaInspectorContext, DanglingUntriaged>` in `InspectorMediaEventHandler` (line 30 of `content/renderer/media/inspector_media_event_handler.h`) is dereferenced after the Oilpan garbage collector has swept the underlying `MediaInspectorContextImpl` object. This results in a use-after-poison crash in the renderer process — triggerable with **zero user interaction and zero permissions** via `canvas.captureStream()`.

### Root Cause

`InspectorMediaEventHandler` holds a non-owning `raw_ptr` to a `blink::MediaInspectorContext` (implemented by `MediaInspectorContextImpl`, a `GarbageCollected` Oilpan object). When a MediaStream-backed `<video>` element is rapidly created and destroyed, the following race occurs:

1. JavaScript destroys the `<video>` element (`video.srcObject = null; video.load(); video.remove()`)
2. A `DOMTimer` fires `HTMLMediaElement::ClearMediaPlayerAndAudioSourceProviderClientWithoutLocking()`
3. This posts a **deferred** `DeleteHelper` task for `WebMediaPlayerMS`
4. Between posting and execution, **Oilpan GC runs** and sweeps `MediaInspectorContextImpl` (marks memory as poisoned, shadow byte `f7`)
5. `DeleteHelper` executes → `~WebMediaPlayerMS()` → `~BatchingMediaLog()` → `SendQueuedMediaEvents()`
6. `inspector_context_->NotifyPlayerEvents(...)` **dereferences poisoned/freed memory** → **CRASH**

The existing `video_player_destroyed_` guard (line 114 in `inspector_media_event_handler.cc`) does not protect against this race because the GC can sweep the context object **before** `OnWebMediaPlayerDestroyed()` is called.

### Security Impact

- **Type**: Use-After-Poison (CWE-416)
- **Severity**: Medium — renderer process crash, potential memory corruption
- **Attack surface**: Zero-interaction, zero-permission. Triggerable via `canvas.captureStream()` — no camera/microphone permission needed
- **Exploitability**: The dangling pointer is used in a virtual method call on the `MediaInspectorContext` interface, meaning the crash dereferences a vtable pointer. In a non-ASan build, this constitutes a use-after-free on an Oilpan-managed object — the freed memory region could potentially be reclaimed by other Oilpan allocations.
- **User interaction**: None required. A malicious page can trigger this automatically on page load.

The crash occurs on a standard ASan dev build without any dangling pointer detection flags (`enable_dangling_raw_ptr_checks`, `use_raw_ptr_asan_unowned_impl`, `PartitionAllocDanglingPtr` are all off). Since `MediaInspectorContextImpl` is an Oilpan `GarbageCollected` object, MiraclePtr / BackupRefPtr does not cover this pointer.

### Partial Fix (Incomplete)

Commit `42cc923a4b6e4` (Dec 9, 2025, Bug: 463465461) — "[Media DevTools] Send queued events before destroying the player" — attempted to fix a related issue by flushing queued events in `OnWebMediaPlayerDestroyedLocked()`. However, this fix:

- Only modified `batching_media_log.cc` — did **NOT** touch `inspector_media_event_handler.cc/h`
- Does **NOT** null out `inspector_context_` after use
- Does **NOT** protect against the GC race (Oilpan can sweep the context between the DOMTimer and the deferred DeleteHelper task)
- The `DanglingUntriaged` annotation on `inspector_context_` **remains unfixed** as of Chromium 147.0.7724.0

---

## VERSION

Chrome Version: 147.0.7724.0 (Dev channel, ASan build, arm64)
Operating System: macOS 15.x (Apple Silicon / arm64)
Release channels impacted: Stable, Beta, Dev — the vulnerable code (`inspector_media_event_handler.cc/h`) has been present since Aug 2019 and the `DanglingUntriaged` annotation was added in Oct 2023.

Note: The bug is platform-independent — the affected code path is cross-platform renderer code.

---

## REPRODUCTION CASE

The attached `poc.html` uses `canvas.captureStream()` to create MediaStream-backed `<video>` elements — **no camera or microphone permissions required**. It runs rapid create/destroy cycles with forced GC. The ASan Chromium renderer typically crashes within 1-3 seconds.

### Steps to Reproduce

```
# 1. Launch ASan Chromium
#    --no-sandbox and --disable-gpu-sandbox are needed only for ASan to write
#    log files to disk. The bug also crashes WITH sandbox enabled (Error 6 / sad tab),
#    but without these flags the ASan log cannot be captured.
ASAN_OPTIONS="detect_leaks=0:halt_on_error=0:log_path=/tmp/asan-poc" \
./Chromium --no-sandbox --disable-gpu-sandbox \
  --js-flags="--expose-gc" \
  --user-data-dir=/tmp/poc-profile \
  --autoplay-policy=no-user-gesture-required \
  "file:///path/to/poc.html"

# 2. Wait ~1-3 seconds. The renderer will crash.

# 3. Check ASan log
cat /tmp/asan-poc.*

```

The primary `poc.html` uses `--expose-gc` to trigger GC at precise moments, making the race window reliable. An additional `poc_no_expose_gc.html` reproduces the same crash **without `--expose-gc`** — it uses ArrayBuffer allocation pressure (~512MB) to force V8 major GC, which triggers Oilpan sweep via the unified heap. See `asan-no-expose-gc.37470` for the crash log — identical stack trace, zero `--js-flags` in the renderer command line.

Steps to reproduce without `--expose-gc`:

```
ASAN_OPTIONS="detect_leaks=0:halt_on_error=0:log_path=/tmp/asan-poc" \
./Chromium --no-sandbox --disable-gpu-sandbox \
  --user-data-dir=/tmp/poc-profile \
  --autoplay-policy=no-user-gesture-required \
  "file:///path/to/poc_no_expose_gc.html"

```
### Expected Result

No crash — media events should be safely dropped if the inspector context has been garbage collected.

### Actual Result

ASan renderer crash: `use-after-poison` on `inspector_context_` vtable dereference.

---

## FOR CRASHES

Type of crash: tab (renderer process crash / sad tab)

Crash State (symbolized ASan stack trace from attached `asan-vrp-retest.36210`):

```
==36210==ERROR: AddressSanitizer: use-after-poison on address 0x7ea400545a48
  at pc 0x000365aa1978 bp 0x00016ee1d110 sp 0x00016ee1d108
READ of size 8 at 0x7ea400545a48 thread T0

    #0 content::InspectorMediaEventHandler::SendQueuedMediaEvents(
         std::vector<media::MediaLogRecord>)+0x11a0
    #1 content::BatchingMediaLog::SendQueuedMediaEvents_Locked()+0x664
    #2 content::BatchingMediaLog::~BatchingMediaLog()+0xa8
    #3 content::BatchingMediaLog::~BatchingMediaLog()+0x8
    #4 blink::WebMediaPlayerMS::~WebMediaPlayerMS()+0x590
    #5 non-virtual thunk to blink::WebMediaPlayerMS::~WebMediaPlayerMS()+0xc
    #6 blink::scheduler::(anonymous namespace)::DeleteHelper::Delete()+0x6c
    #7 base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*)+0x11c
    #8 base::TaskAnnotator::RunTaskImpl(base::PendingTask&)+0x348

Address 0x7ea400545a48 is a wild pointer inside of access range of size 0x8.
SUMMARY: AddressSanitizer: use-after-poison in
  content::InspectorMediaEventHandler::SendQueuedMediaEvents()+0x11a0

Shadow bytes around the buggy address:
  0x7ea400545900: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
  0x7ea400545980: f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7 f7
=>0x7ea400545a00: f7 f7 f7 f7 f7 f7 f7 f7 f7[f7]f7 f7 f7 f7 f7 f7

Task trace (what triggered the crash):
    #0 blink::HTMLMediaElement::ClearMediaPlayerAndAudioSourceProviderClientWithoutLocking()+0x1d0
    #1 blink::DOMTimer::DOMTimer()+0x5c4

```

---

## BISECT INFORMATION

The dangling pointer has existed since the original code was written. Key commits:

| Date | Commit | Description |
| --- | --- | --- |
| **Aug 13, 2019** | `cda47a0e8d542` | Original creation — raw `blink::MediaInspectorContext*` pointer (Bug: 794255) |
| Nov 1, 2019 | `257b682aed319` | Added `video_player_destroyed_` guard (partial fix for Bug: 1014433) |
| **Oct 1, 2023** | `bc3754aeb164b` | MiraclePtr rewrite — converted to `raw_ptr<T, ExperimentalRenderer>` (Bug: 1444624) |
| **Oct 3, 2023** | `d0bb793c40aeb` | Annotated as `DanglingUntriaged` — **acknowledging the dangling pointer** (Bug: 144624) |
| Dec 9, 2025 | `42cc923a4b6e4` | Partial fix — flush events before destroy, but did NOT null out `inspector_context_` (Bug: 463465461) |

**The bug was introduced in**: `cda47a0e8d542` (Aug 13, 2019) — the raw pointer was never lifetime-safe.

**The bug was acknowledged but not fixed in**: `d0bb793c40aeb` (Oct 3, 2023) — the `DanglingUntriaged` annotation explicitly marks this pointer as known-dangling.

---

## PROPOSED PATCH

The attached `fix-inspector-context-uap.patch` is a directional proposal illustrating one approach to the lifetime mismatch. It adds a null-check guard and nulls out `inspector_context_` on player destruction. A more robust production fix would likely involve preventing the raw pointer from outliving the GC-managed object entirely (e.g., via Oilpan `WeakMember` or moving the flush earlier in the destruction sequence).

Summary of proposed changes:

**`content/renderer/media/inspector_media_event_handler.h`**:

- Remove `DanglingUntriaged` annotation from `inspector_context_`

**`content/renderer/media/inspector_media_event_handler.cc`**:

- `SendQueuedMediaEvents()`: Add null-check for `inspector_context_` alongside existing `video_player_destroyed_` guard
- `OnWebMediaPlayerDestroyed()`: Null out `inspector_context_` after `DestroyPlayer()` call

---

## CREDIT INFORMATION

Reporter credit: Hubert Pietrusiak

---

## ATTACHED FILES

Attached files:

| # | File | Description |
| --- | --- | --- |
| 1 | `poc.html` | Zero-interaction PoC — uses canvas.captureStream(), no permissions needed |
| 2 | `poc_no_expose_gc.html` | Same PoC but crashes **without `--expose-gc`** (ArrayBuffer allocation pressure) |
| 3 | `fix-inspector-context-uap.patch` | Proposed fix (unified diff format) |
| 4 | `asan-vrp-retest.36210` | ASan crash log (March 8, 2026, Chromium 147.0.7724.0) |
| 5 | `asan-no-expose-gc.37470` | ASan crash log from `poc_no_expose_gc.html` — **no `--expose-gc`, no `--js-flags`** |
| 6 | `recording.mov` | Screen recording of the crash reproduction |

## Attachments

- [asan-no-expose-gc.37470](attachments/asan-no-expose-gc.37470) (application/octet-stream, 10.4 KB)
- [poc_no_expose_gc.html](attachments/poc_no_expose_gc.html) (text/html, 8.1 KB)
- [fix-inspector-context-uap.patch](attachments/fix-inspector-context-uap.patch) (text/x-diff, 1.8 KB)
- [asan-vrp-retest.36210](attachments/asan-vrp-retest.36210) (application/octet-stream, 10.5 KB)
- [poc.html](attachments/poc.html) (text/html, 7.7 KB)
- [recording.mov](attachments/recording.mov) (video/quicktime, 774.7 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5446573857112064.

### 24...@project.gserviceaccount.com (2026-03-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-03-10)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/2f6df874594524706ee2d13883ff889b4c9cd1d8 (Always post destruction of WebMediaPlayer instances

There are lots of ways that re-entrant destruction of players can
happen. Fixing them all piecemeal is fragile and making WMP garbage
collected is difficult since it's a blink/public interface. For now
just add a Shutdown mechanism and post destruction such that we
never have re-entrant destruction.

Bug: 482958590, 459524033
Change-Id: I9ccdaeed448850a5133deb464dcaeafa7447fe94
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7609443
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Frank Liberato <liberato@chromium.org>
Auto-Submit: Dale Curtis <dalecurtis@chromium.org>
Commit-Queue: Dale Curtis <dalecurtis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1595039}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2026-03-10)

Detailed Report: https://clusterfuzz.com/testcase?key=5446573857112064

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ecc00495d88
Crash State:
  content::InspectorMediaEventHandler::SendQueuedMediaEvents
  content::BatchingMediaLog::SendQueuedMediaEvents_Locked
  content::BatchingMediaLog::~BatchingMediaLog
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1595038:1595043

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5446573857112064

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### el...@chromium.org (2026-03-10)

Kicking Pri to 0 to match Sev-0 for now.

### da...@chromium.org (2026-03-10)

CF seems to think this was only exploitable after the commit in [comment#4](https://issues.chromium.org/issues/490727241#comment4) which should be 147+. Reporter, are you able to demonstrate an attack against < 147?

### el...@chromium.org (2026-03-10)

This is also a renderer bug apparently, so it's Sev-1.

### hu...@gmail.com (2026-03-10)

I wasn't able to reproduce the crash on a pre-commit build (mac-arm64 ASan 146).

My original root cause analysis traced the issue too far back. The dangling pointer has been present since 2019, but the actual exploitable crash path was likely introduced by the commit above.

So: no, I'm not able to demonstrate the attack against < 147.

### da...@chromium.org (2026-03-10)

I don't think the proposed patch resolves the issue. The key thing is that we call `MediaLog::OnWebMediaPlayerDestroyed` during `WebMediaPlayerMS::Shutdown()` like `WebMediaPlayerImpl` does. We can't use a WeakPersistent for the context because it's a non-GC type (even though it's backed by an object tied to the ExecutionContext).

Proposed fix here: <https://chromium-review.git.corp.google.com/c/chromium/src/+/7653369>

I'll be OOO until Monday, so if any merges are needed before that someone else will need to handle them.

### da...@chromium.org (2026-03-10)

Reporter, let me know if the new proposed fix resolves the issue for you.

### dx...@google.com (2026-03-11)

Project: chromium/src  

Branch:  main  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7653369>

Ensure inspector media context is released during WMP shutdown

---


Expand for full commit details
```
     
    This resolves two related issues: 
    * A DanglingPointer annotation due to destruction order issues with 
    the WebMediaPlayer implementations. 
    * A failure to call OnWebMediaPlayerDestroyed() from WebMediaPlayerMS. 
     
    Fixed: 490727241 
    Change-Id: I32c5867b519af2e9e7486d8c6c9db75727c8a6f2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7653369 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1597432}

```

---

Files:

- M `content/renderer/media/inspector_media_event_handler.cc`
- M `content/renderer/media/inspector_media_event_handler.h`
- M `content/renderer/media/inspector_media_event_handler_unittest.cc`
- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`

---

Hash: [703e4caaf112e65d5097a7ab231ef063ef075b63](https://chromiumdash.appspot.com/commit/703e4caaf112e65d5097a7ab231ef063ef075b63)  

Date: Wed Mar 11 00:38:45 2026


---

### hu...@gmail.com (2026-03-11)

The fix works. I can't reproduce that anymore.

### 24...@project.gserviceaccount.com (2026-03-11)

ClusterFuzz testcase 5446573857112064 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1597431:1597434

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-03-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-11)

Security Merge Request Consideration: Requesting merge to dev (M147) because latest trunk commit (1597432) appears to be after dev branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-03-12)

**Merge approved:** your change passed merge requirements and is auto-approved for M147. Please go ahead and merge the CL to branch 7727 (refs/branch-heads/7727) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Dale Curtis [dalecurtis@chromium.org](mailto:dalecurtis@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7670122>

[M147] Ensure inspector media context is released during WMP shutdown

---


Expand for full commit details
```
     
    This resolves two related issues: 
    * A DanglingPointer annotation due to destruction order issues with 
    the WebMediaPlayer implementations. 
    * A failure to call OnWebMediaPlayerDestroyed() from WebMediaPlayerMS. 
     
    (cherry picked from commit 703e4caaf112e65d5097a7ab231ef063ef075b63) 
     
    Fixed: 490727241 
    Change-Id: I32c5867b519af2e9e7486d8c6c9db75727c8a6f2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7653369 
    Commit-Queue: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    Auto-Submit: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1597432} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670122 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#564} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `content/renderer/media/inspector_media_event_handler.cc`
- M `content/renderer/media/inspector_media_event_handler.h`
- M `content/renderer/media/inspector_media_event_handler_unittest.cc`
- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`

---

Hash: [1181a96c5d6a0278e9afd202e9cd731e91de610a](https://chromiumdash.appspot.com/commit/1181a96c5d6a0278e9afd202e9cd731e91de610a)  

Date: Tue Mar 17 07:47:21 2026


---

### pe...@google.com (2026-03-17)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### da...@chromium.org (2026-03-17)

Per [comment#9](https://issues.chromium.org/issues/490727241#comment9) this only affects 147+, so no more merges are needed.

### pe...@google.com (2026-03-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-19)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7683671
2. Low - There was no conflict.
3. 147
4. Yes, according to the BISECT INFORMATION section in the description, the dangling pointer has existed since Aug 2019, and it was not fixed fully until Oct 2023. Thus, M138 also needs to have the patch.

### pe...@google.com (2026-03-19)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-19)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7683730
2. Low - There was no conflict.
3. 147
4. Yes, according to the BISECT INFORMATION section in the description, the dangling pointer has existed since Aug 2019, and it was not fixed fully until Oct 2023. Thus, M144 also needs to have the patch.

### hu...@gmail.com (2026-03-19)

Please take a look at comment [#comment9](https://issues.chromium.org/issues/490727241#comment9) and [#comment4](https://issues.chromium.org/issues/490727241#comment4) (the actual attack vector was unlocked in commit <https://chromium.googlesource.com/chromium/src/+/2f6df874594524706ee2d13883ff889b4c9cd1d8>)

### an...@google.com (2026-03-30)

Delayed until M147 hits Stable

### sp...@google.com (2026-04-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process. Incorrect bisect.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490727241)*
