# Spanify AudioBus and AudioBuffer

| Field | Value |
|-------|-------|
| **Issue ID** | [482828615](https://issues.chromium.org/issues/482828615) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P4 |
| **Component** | Internals>Media>Audio |
| **Reporter** | tg...@google.com |
| **Assignee** | tg...@chromium.org |
| **Created** | 2026-02-09 |
| **Bounty** | $36,000.00 |

## Description

Summary

SpeechRecognizerImpl fails to validate that the size of the data array in the AudioDataS16 Mojo struct matches the declared channel\_count \* frame\_count. This allows a compromised renderer to trigger a heap out-of-bounds read in the Browser Process.

VULNERABILITY DETAILS

Heap-buffer-overflow (OOB read) in the browser process via `SpeechRecognizerImpl::AddAudioFromRenderer()`. A compromised renderer can read attacker-controlled amounts of browser-process heap memory through the `media.mojom.SpeechRecognitionAudioForwarder` Mojo interface. No permissions are required, the audio forwarder path bypasses the microphone permission check.

The per-packet `AudioDataS16` Mojo struct has independent `channel_count`, `frame_count`, and `data` fields with no validation that `data.size() >= channel_count * frame_count`. The deprecated raw-pointer `FromInterleaved()` overload at `speech_recognizer_impl.cc:341` reads `channel_count * frame_count` int16 values from the undersized data buffer, causing an OOB heap read. The read size is `(channel_count * frame_count - data.size()) * 2` bytes, fully attacker-controlled per packet.

There is also a secondary integer overflow at line 345 where `channel_count * frame_count * 16 / 8` is computed in int32 this can undersize the AudioChunk allocation, but requires a 1GB+ AudioBus to trigger so it's only DoS.

The OOB-read data is converted to float, written to an AudioChunk, then FLAC-encoded (level 0, lossless) and uploaded to Google's speech API. The int16→float32→int16→FLAC pipeline is bit-for-bit lossless (float32 mantissa exceeds int16 precision), so the heap bytes survive encoding intact.

Introduced in commit 881ab7a9d5 ("Add MediaStreamTrack support to the Web Speech API", Evan Liu, 2024-08-01, <https://chromium-review.googlesource.com/c/chromium/src/+/5631655>).

VERSION
Chrome Version: 146.0.7673.0 (trunk) affected since Chrome 129 (Aug 2024)
Operating System: Ubuntu 22.04 / WSL2

REPRODUCTION CASE

Attached: `poc-speech-oob-read.html` (primary), `poc-variable-read-sizes.html` (shows 100/1024/4096/65536-byte reads)

The PoCs use MojoJS to simulate a compromised renderer crafting raw Mojo messages. A real attacker with renderer RCE would construct identical messages directly.

cd chromium/src
ASAN\_OPTIONS=detect\_odr\_violation=0 ./out/asan-debug/chrome   

--no-sandbox --enable-blink-features=MojoJS,MojoJSTest --disable-gpu   

file:///path/to/poc-speech-oob-read.html 2>&1 | tee /tmp/asan.log

Build: `is_debug=true is_asan=true is_lsan=true is_component_build=true`
`--no-sandbox` is a WSL2 requirement; the bug is in the browser-process Mojo handler and is hit regardless of sandbox state.
`detect_odr_violation=0` is needed for ASan component builds (expected cppgc ODR violation).

The PoC binds `media.mojom.SpeechRecognizer`, sends `Start()` with an `audio_forwarder` receiver (bypasses mic permission), waits for the session to initialize, then sends `AddAudioFromRenderer` with `channel_count=2, frame_count=1024, data=[10 values]` reads 4076 bytes past the 20-byte allocation.

In release builds the OOB read is silent with no crash.

FOR CRASHES
Type of crash: browser process (Chrome\_IOThread)
Crash State (full ASan log attached)

==35997==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x717bf9f18bf4 at pc 0x754d48186b8b bp 0x714be7753730 sp 0x714be7753728
READ of size 2 at 0x717bf9f18bf4 thread T8 (Chrome\_IOThread)
#0 0x754d48186b8a in void media::AudioBus::CopyConvertFromInterleavedSourceToAudioBus<media::FixedSampleTypeTraits<short>>(...) media/base/audio\_bus.h:494:27
#1 0x754d481869ce in void media::AudioBus::FromInterleavedPartial<media::FixedSampleTypeTraits<short>>(...) media/base/audio\_bus.h:422:3
#2 0x754d4817f758 in void media::AudioBus::FromInterleaved<media::FixedSampleTypeTraits<short>>(...) media/base/audio\_bus.h:390:3
#3 0x754d48173ecc in content::SpeechRecognizerImpl::AddAudioFromRenderer(...) content/browser/speech/speech\_recognizer\_impl.cc:341:9
#4 0x754d3e126c20 in media::mojom::SpeechRecognitionAudioForwarderStubDispatch::Accept(...) gen/media/mojo/mojom/speech\_recognition\_audio\_forwarder.mojom.cc:192:13

0x717bf9f18bf4 is located 0 bytes after 20-byte region [0x717bf9f18be0,0x717bf9f18bf4)
allocated by thread T8 (Chrome\_IOThread) here:
#0 0x5db19b595a5d in operator new(unsigned long)
...
#8 0x754d3e03269f in mojo::ArrayTraits<std::vector<short>>::Resize(...) mojo/public/cpp/bindings/array\_traits.h:149:17

SUMMARY: AddressSanitizer: heap-buffer-overflow media/base/audio\_bus.h:494:27 in void media::AudioBus::CopyConvertFromInterleavedSourceToAudioBus<...>(...)

SUGGESTED FIX

Attached: `suggested-fix.patch`

Validate `data.size() == channel_count * frame_count` (with `base::CheckMul` for overflow) before the `FromInterleaved` call, and switch to the span-based `FromInterleaved` overload which has `CHECK_LE`. The speech service at `chrome/services/speech/` already does this validation. The browser-process `SpeechRecognizerImpl` just lacks it.

CREDIT INFORMATION

Reporter credit: Grischa Hauser

## Attachments

- [asan-speech-oob-report.log](attachments/asan-speech-oob-report.log) (text/plain, 30.7 KB)
- [suggested-fix.patch](attachments/suggested-fix.patch) (text/x-diff, 2.2 KB)
- [poc-variable-read-sizes.html](attachments/poc-variable-read-sizes.html) (text/html, 4.4 KB)
- [poc-speech-oob-read.html](attachments/poc-speech-oob-read.html) (text/html, 4.5 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5270757089148928.

### gr...@gmail.com (2026-02-10)

Thanks for spinning up the ClusterFuzz. Quick question on process:
I'm working on a few ideas to extend this further. if I find larger attack chains that build on this same root cause, should I add them as comments here, or file separate reports for each? Thanks!

### ts...@google.com (2026-02-10)

CF repro'd but failed to update this bug.  Looks like it is still trying to determine how far back in time the issue occurs.

### ts...@google.com (2026-02-10)

reporter - same root cause should be tracked as a single issue.  In particular, if you are able to extend the PoC to perform more powerful actions, that should go here.

### gr...@gmail.com (2026-02-10)

Thanks for the clarification.

### ts...@google.com (2026-02-10)

Assigning per recent activity in audio_bus.h, feel free to re-assign as appropriate.

### 24...@project.gserviceaccount.com (2026-02-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-10)

Detailed Report: https://clusterfuzz.com/testcase?key=5270757089148928

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7b94e4af0134
Crash State:
  void media::AudioBus::CopyConvertFromInterleavedSourceToAudioBus<media::FixedSam
  content::SpeechRecognizerImpl::AddAudioFromRenderer
  media::mojom::SpeechRecognitionAudioForwarderStubDispatch::Accept
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1397672:1397675

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5270757089148928

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### gr...@gmail.com (2026-02-11)

Status update: I am still working on extraction of overflow-read information.

Current result: I have a working oracle-based canary readback that can recover synthetic bytes (controlled payload) in
renderer context. This indicates practical data leakage is feasible, though reliability tuning is still in progress.

I can upload the current extension PoC and run artifacts if useful for triage. Please let me know if you want the full package attached to this report. (it's not very clean yet, but a basic demonstration that there are ways to use the bytes read by the oob)

Question for Assignee/Verifier: would an additional end-to-end extraction demonstration materially affect severity assessment, or is the current proof sufficient?
thanks!

### ch...@google.com (2026-02-11)

Setting milestone because of s0/s1 severity.

### tg...@google.com (2026-02-12)

Thank you for the report. It turns out that the `FromInterleaved/ToInterleaved` calls there are unnecessary here, and I've uploaded a CL removing them, along with the suggested mojo message verifications.

CL: <https://chromium-review.googlesource.com/c/chromium/src/+/7573019>

FWIW, I was actively in the process of spanifying all of the `{From,To}Interleaved` calls (tracked [here](https://g-issues.chromium.org/issues/373960632#comment57)), but I might have missed the opportunity to verify the Mojo message as part of that work. This is now a better result, since the bad mojo message should crash the offending renderer instead of running into CHECKs.

I've purposely kept the CL title mundane, as to not draw too much attention to this bug.

### tg...@google.com (2026-02-12)

Adding nasko@ to this bug, for context of the review in [comment#12](https://issues.chromium.org/issues/482828615#comment12)

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  Thomas Guilbert [tguilbert@chromium.org](mailto:tguilbert@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7573019>

[CodeHealth] Spanify (de)interleaving in SpeechRecognizerImpl

---


Expand for full commit details
```
     
    This CL updates an instance of `AudioBus::ToInterleaved()` to use its 
    safer, spanified counterpart. 
     
    It also removes one round trip of deinterleaving/interleaving + copy 
    converting to/from float, which saves one memory copy. This extra round 
    trip might have had the intention of clipping/sanitizing incoming data, 
    which is only useful for `float`, not `int16_t`. 
     
    Finally, this CL also hardens by rejecting potentially bad messages 
    coming from the renderer, and using checked math when calculating 
    memory allocation sizes. 
     
    See linked bugs for additional details. 
     
    Bug: 373960632, 482828615 
    Change-Id: I03c0e3342651bc6b55aa3505206e54c1c56bac5e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7573019 
    Reviewed-by: Frank Liberato <liberato@chromium.org> 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    Commit-Queue: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1586654}

```

---

Files:

- M `content/browser/speech/speech_recognizer_impl.cc`
- M `content/browser/speech/speech_recognizer_impl.h`

---

Hash: [88a0535d5bab4c1e7e97af17882a3c00d021fba9](https://chromiumdash.appspot.com/commit/88a0535d5bab4c1e7e97af17882a3c00d021fba9)  

Date: Wed Feb 18 21:08:43 2026


---

### tg...@google.com (2026-02-18)

This issue should be fixed. I will update this bug with the first Canary version number once it is released.

### gr...@gmail.com (2026-02-18)

Cool, thanks for the quick fix! I'm already working on the next one (different root cause). Since this was my first Chromium report: was the style okay? I want to keep reports as minimal as possible while still including enough information. Any suggestions for improvement for future reports are very welcome. Thanks

### tg...@google.com (2026-02-18)

I don't have any specific feedback on the style, it was more than good enough! A high quality repro case and a stack trace is the most important part. Your suggested fix was also nice, since in this case it showed from just code inspection that there was an issue; after reading the suggested fix, that was enough for me, and I didn't have to read the other details of the bug.

### 24...@project.gserviceaccount.com (2026-02-19)

ClusterFuzz testcase 5270757089148928 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1586639:1586656

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-02-20)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1586654) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1586654) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1586654) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: M144 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M145 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M146 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-02-21)

No crashes in Canary. Approved to merge to all three channels.

### tg...@google.com (2026-02-23)

Re-adding original reporter, after accidental un-cc'ing.

### tg...@google.com (2026-02-23)

> Which CLs should be backmerged? (Please include Gerrit links.)

3 CLs:

- <https://chromium-review.googlesource.com/c/chromium/src/+/7563266> - Necessary refactor
- <https://chromium-review.googlesource.com/c/chromium/src/+/7588685> - Follow-up fix to the refactor
- <https://chromium-review.googlesource.com/c/chromium/src/+/7573019> - The mojom fix

> Has this fix been verified on Canary to not pose any stability regressions?

Confirmed in [comment#20](https://issues.chromium.org/issues/482828615#comment20)

> Does this fix pose any potential non-verifiable stability risks?

Extra crashes instead of security issues.

> Does this fix pose any known compatibility risks?

No

> Does it require manual verification by the test team? If so, please describe required testing.

No

drubery@, considering there are 3 CLs to merge and potential conflicts, should I still proceed to merge back to 3 previous milestones?

### tg...@google.com (2026-02-23)

Adding srinivassista@ as milestone owner. PTAL at [comment#22](https://issues.chromium.org/issues/482828615#comment22)

### sr...@chromium.org (2026-02-24)

thanks i will reach out to securiy team to chime in

### sr...@chromium.org (2026-02-24)

I am cutting stable RC #1 for early stable release tomorrow for 146 today around 2pm PST, please help complete all your merges before that time to be included in tomorrow release, if this is critcal and missing that timeline, please reach out to me asap

### dr...@chromium.org (2026-02-24)

An OOB read of browser process memory is quite a powerful primitive for an attacker. I would still recommend merging. I've done a more thorough stability check. brhttp://shortn/\_FEaEiwO47z shows no relevant crashes in all of //components/speech. <http://shortn/_zkhs9lmSHx> shows no relevant crashes in all of //content/browser/speech. (Relevant in both cases being after those CLs landed). We've had 5 days of data at this point, so it's unlikely users will hit a new crash frequently.

If you run into significant merge conflicts that you think introduce new stability risk, let me know.

### tg...@google.com (2026-02-24)

I have started merging back branches, but it is a convoluted process (3 dependent CLs).

There are conflicts on M145, M144.

The only OWNER of these files is OOO, so getting approval from "content/ + component/" OWNERS is tricky. I've talked to drubery@ offline about this, but if there was some OWNERS override to expedite the approvals that would be great.

### sr...@chromium.org (2026-02-24)

For merge conflict CL, please get another engineer to help +1 the CL and then reach out to us for OO , we can do that once some one reviewed the merge conflicts are resolved properly

### tg...@google.com (2026-02-24)

Could I get OO on the M146 (1 of 3) CL without merge conflicts? <https://chromium-review.googlesource.com/c/chromium/src/+/7603118>

### sr...@chromium.org (2026-02-24)

since these are dependent CL's will there be issues if we land this one and not land the other two in RC build ? if so lets wait for them to be ready and together ?

### tg...@google.com (2026-02-24)

Seems good. Sorry, it took forever for git fetch to complete (following [these instructions](https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md#using-git)).

All 3 M146 cherry-picked without issue and are ready for OO:

- <https://chromium-review.googlesource.com/c/chromium/src/+/7603118/3>
- <https://chromium-review.googlesource.com/c/chromium/src/+/7604815/1>
- <https://chromium-review.googlesource.com/c/chromium/src/+/7602968/1>

### dr...@google.com (2026-02-24)

The conflicts on M145 mean that we'd be rewriting some of this patch and introducing untested code directly to Stable. Given there's only one more release of M145 anyways, I no longer think we should merge to M145. Let's just get this into M146.

### tg...@google.com (2026-02-24)

For M145, the conflicts are due to this missing CL:

<https://chromium-review.googlesource.com/c/chromium/src/+/7455508>

Merging that one back might cause stability issues (I don't know if other bugs came up after that one landed and were cleaned up in M146).

I could only take the relevant parts from the missing CL, or only merge back the portion of [the "3rd of 3" CL](https://chromium-review.googlesource.com/c/chromium/src/+/7573019) which validates the mojom messages (without spanification).

I think only addressing the bad mojom messages would mitigate the issues outlined in this bug without causing too much code churn.

### tg...@google.com (2026-02-24)

Thanks! I was typing out [comment#33](https://issues.chromium.org/issues/482828615#comment33) before I saw [comment#32](https://issues.chromium.org/issues/482828615#comment32). Only merging for M146 SGTM

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Thomas Guilbert [tguilbert@chromium.org](mailto:tguilbert@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7603118>

[M146][CodeHealth] Spanify AudioChunk and AudioBuffer

---


Expand for full commit details
```
     
    This CL spanifies the speech service's `AudioChunk` and `AudioBuffer`. 
    Doing so fixes some undefined behavior when it came to using 
    reinterpret_cast() on some potentially unaligned memory. 
     
    Additionally, some code which used to rely on passing 
    `const std::string&` has been updated to take a `std::string_view` 
    instead, to defer copying data out of `AudioChunk` until necessary. 
     
    (cherry picked from commit 9e5e194f78a8d6b5e178571356fa2dc66ad5605f) 
     
    Change-Id: Iad2751c0258700f62ae5a1b2906e407a39c0aec8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7563266 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    Reviewed-by: Tommy Nyquist <nyquist@chromium.org> 
    Commit-Queue: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1586237} 
    Bug: 482828615 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7603118 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Thomas Guilbert <tguilbert@chromium.org> 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1283} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `components/speech/BUILD.gn`
- M `components/speech/audio_buffer.cc`
- M `components/speech/audio_buffer.h`
- A `components/speech/audio_buffer_unittest.cc`
- M `components/speech/upstream_loader.cc`
- M `components/speech/upstream_loader.h`
- M `content/browser/speech/audio_encoder_fuzzer.cc`
- M `content/browser/speech/network_speech_recognition_engine_impl.cc`
- M `content/browser/speech/network_speech_recognition_engine_impl.h`
- M `content/browser/speech/on_device_speech_recognition_engine_impl.cc`
- M `content/browser/speech/soda_speech_recognition_engine_impl.cc`
- M `content/browser/speech/speech_recognizer_impl.cc`

---

Hash: [908f10d39220c86f5450a0f5c6926e3d4ceca8d1](https://chromiumdash.appspot.com/commit/908f10d39220c86f5450a0f5c6926e3d4ceca8d1)  

Date: Tue Feb 24 23:42:23 2026


---

### tg...@google.com (2026-02-24)

I've received the OWNERS approvals I needed, I am submitting the CL chain to M146 CQ

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Thomas Guilbert [tguilbert@chromium.org](mailto:tguilbert@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7604815>

[M146] Guard against 0 length in AudioChunk ctor

---


Expand for full commit details
```
     
    Recent changes spanified some aspect of `AudioChunk`, and changed the 
    backing memory from `std::string` to `base::AlignedHeapArray`. 
     
    This CL prevents CHECKs in `base::AlignedUninit` when the `length` 
    passed to `AudioChunk`'s ctor is 0 
     
    (cherry picked from commit f8c6b74e04907b7202193dcbe572793e15129184) 
     
    Bug: 485569900, 482828615 
    Change-Id: I0271fdd45310306aa35e29e1728630b7ee0a899c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7588685 
    Reviewed-by: Tommy Nyquist <nyquist@chromium.org> 
    Commit-Queue: Thomas Guilbert <tguilbert@chromium.org> 
    Auto-Submit: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1587492} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7604815 
    Cr-Commit-Position: refs/branch-heads/7680@{#1286} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `components/speech/audio_buffer.cc`
- M `components/speech/audio_buffer_unittest.cc`

---

Hash: [bce758a5d3563e317e92bc4561798c424a7f21eb](https://chromiumdash.appspot.com/commit/bce758a5d3563e317e92bc4561798c424a7f21eb)  

Date: Wed Feb 25 00:21:02 2026


---

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Thomas Guilbert [tguilbert@chromium.org](mailto:tguilbert@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7602968>

[M146] [CodeHealth] Spanify (de)interleaving in SpeechRecognizerImpl

---


Expand for full commit details
```
     
    This CL updates an instance of `AudioBus::ToInterleaved()` to use its 
    safer, spanified counterpart. 
     
    It also removes one round trip of deinterleaving/interleaving + copy 
    converting to/from float, which saves one memory copy. This extra round 
    trip might have had the intention of clipping/sanitizing incoming data, 
    which is only useful for `float`, not `int16_t`. 
     
    Finally, this CL also hardens by rejecting potentially bad messages 
    coming from the renderer, and using checked math when calculating 
    memory allocation sizes. 
     
    See linked bugs for additional details. 
     
    (cherry picked from commit 88a0535d5bab4c1e7e97af17882a3c00d021fba9) 
     
    Bug: 373960632, 482828615 
    Change-Id: I03c0e3342651bc6b55aa3505206e54c1c56bac5e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7573019 
    Reviewed-by: Frank Liberato <liberato@chromium.org> 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    Commit-Queue: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1586654} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7602968 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Auto-Submit: Thomas Guilbert <tguilbert@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1287} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `content/browser/speech/speech_recognizer_impl.cc`
- M `content/browser/speech/speech_recognizer_impl.h`

---

Hash: [7ba017ee52ade3b69894721a024af52b1f86bb0b](https://chromiumdash.appspot.com/commit/7ba017ee52ade3b69894721a024af52b1f86bb0b)  

Date: Wed Feb 25 00:21:19 2026


---

### tg...@google.com (2026-02-25)

The merge to M146 is complete.

### ch...@google.com (2026-02-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2026-02-25)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sp...@google.com (2026-03-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

Rationale for this decision:
High Quality with Bisect. Sandbox escape / Memory corruption in a non-sandboxed process.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### gr...@gmail.com (2026-03-05)

Thanks a lot! And also thanks for the quick fix and valuable feedback

### vi...@google.com (2026-03-10)

Similar to the conclusion reached in #33, I labeled the issue as 'LTS-NotApplicable-138' because backporting the fix to M138 is overly complicated due to the convoluted process involving multiple dependent CLs

### vi...@google.com (2026-04-09)

Answering the two questions from [#comment41](https://issues.chromium.org/issues/482828615#comment41):

1. no
2. no

this security issue was introduced in 129 in <https://crrev.com/c/5631655>

### pe...@google.com (2026-04-09)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### vi...@google.com (2026-04-10)

1. a total of 6 CLs - in this order:
   - <https://chromium-review.git.corp.google.com/c/chromium/src/+/7747068>
   - <https://chromium-review.git.corp.google.com/c/chromium/src/+/7749404> (this one contains some simple conflicts in the unittests)
   - <https://chromium-review.git.corp.google.com/c/chromium/src/+/7738240>
   - <https://chromium-review.git.corp.google.com/c/chromium/src/+/7744796> (actual bug fix)
   - <https://chromium-review.git.corp.google.com/c/chromium/src/+/7744897> (actual bug fix)
   - <https://chromium-review.git.corp.google.com/c/chromium/src/+/7744898> (actual bug fix)
2. Medium - as mentioned, the 3 CLs bringing the actual fixes were convoluted and required 3 other CLs, one of them with a simple conflict to be fixed
3. 146
4. borderline Yes

### dx...@google.com (2026-05-07)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7738240>

[M144-LTS] spanification: automatically spanify .../speech/endpointer/endpointer\_unittest.cc etc.

---


Expand for full commit details
```
     
    In M144, different to the original, there were two changes commented by 
    developers during the review: 
      - components/speech/audio_buffer.cc: In function AudioChunk::GetSample16, it was removed a DCHECK, because a check is already made by the span returned from SamplesData16AsSpan. 
      - components/speech/endpointer/energy_endpointer.cc: In function RMS, line `ssq_int64 += sample * sample` was mentioned as a potential overflow, so it was properly cast to int64_t. 
     
    Original change's description: 
    > spanification: automatically spanify .../speech/endpointer/endpointer_unittest.cc etc. 
    > 
    > This is the result of running the automatic spanification on linux and 
    > updating code to use and pass spans where size is known. 
    > 
    > The original patch was fully automated using script: 
    > //tools/clang/spanify/rewrite-multiple-platforms.sh -platforms=linux 
    > Then refined with gemini-cli 
    > 
    > gemini-run/batch-run-1761614304/group_188 
    > 
    > BUG=439964610 
    > BUG=431824301 
    > 
    > Change-Id: I33b627b0ba4dc40e3f6dd3c69d3c80752ac33550 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7455508 
    > Commit-Queue: Bryan Enrique Gonzalez <bryanenriquegv@google.com> 
    > Reviewed-by: Evan Liu <evliu@google.com> 
    > Reviewed-by: Stephen Nusko <nuskos@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1569858} 
     
    Bug: 482828615 
    Change-Id: I33b627b0ba4dc40e3f6dd3c69d3c80752ac33550 
    Fuchsia-Binary-Size: Cherry-pick the CL to M144. 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7738240 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Evan Liu <evliu@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4857} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `chrome/services/speech/soda_speech_recognizer_impl.cc`
- M `components/speech/audio_buffer.cc`
- M `components/speech/audio_buffer.h`
- M `components/speech/endpointer/endpointer.cc`
- M `components/speech/endpointer/endpointer.h`
- M `components/speech/endpointer/endpointer_unittest.cc`
- M `components/speech/endpointer/energy_endpointer.cc`
- M `components/speech/endpointer/energy_endpointer.h`
- M `content/browser/speech/speech_recognizer_impl.cc`

---

Hash: [731e1c3c97fc5b253ca07a59d56d8089a27c9812](https://chromiumdash.appspot.com/commit/731e1c3c97fc5b253ca07a59d56d8089a27c9812)  

Date: Thu May 7 20:32:17 2026


---

### dx...@google.com (2026-05-15)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7744796>

[M144-LTS] [CodeHealth] Spanify AudioChunk and AudioBuffer

---


Expand for full commit details
```
     
    Original change's description: 
    > [CodeHealth] Spanify AudioChunk and AudioBuffer 
    > 
    > This CL spanifies the speech service's `AudioChunk` and `AudioBuffer`. 
    > Doing so fixes some undefined behavior when it came to using 
    > reinterpret_cast() on some potentially unaligned memory. 
    > 
    > Additionally, some code which used to rely on passing 
    > `const std::string&` has been updated to take a `std::string_view` 
    > instead, to defer copying data out of `AudioChunk` until necessary. 
    > 
    > Change-Id: Iad2751c0258700f62ae5a1b2906e407a39c0aec8 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7563266 
    > Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    > Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    > Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    > Reviewed-by: Tommy Nyquist <nyquist@chromium.org> 
    > Commit-Queue: Thomas Guilbert <tguilbert@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1586237} 
     
    Bug: 482828615 
    Change-Id: Iad2751c0258700f62ae5a1b2906e407a39c0aec8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7744796 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Reviewed-by: Evan Liu <evliu@google.com> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4862} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `components/speech/BUILD.gn`
- M `components/speech/audio_buffer.cc`
- M `components/speech/audio_buffer.h`
- A `components/speech/audio_buffer_unittest.cc`
- M `components/speech/upstream_loader.cc`
- M `components/speech/upstream_loader.h`
- M `content/browser/speech/audio_encoder_fuzzer.cc`
- M `content/browser/speech/network_speech_recognition_engine_impl.cc`
- M `content/browser/speech/network_speech_recognition_engine_impl.h`
- M `content/browser/speech/on_device_speech_recognition_engine_impl.cc`
- M `content/browser/speech/soda_speech_recognition_engine_impl.cc`
- M `content/browser/speech/speech_recognizer_impl.cc`

---

Hash: [720638c72d896752a7e78900769c2da0b2e1bbd5](https://chromiumdash.appspot.com/commit/720638c72d896752a7e78900769c2da0b2e1bbd5)  

Date: Fri May 15 20:50:53 2026


---

### dx...@google.com (2026-05-18)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7744897>

[M144-LTS] [CodeHealth] Spanify (de)interleaving in SpeechRecognizerImpl

---


Expand for full commit details
```
     
    Original change's description: 
    > [CodeHealth] Spanify (de)interleaving in SpeechRecognizerImpl 
    > 
    > This CL updates an instance of `AudioBus::ToInterleaved()` to use its 
    > safer, spanified counterpart. 
    > 
    > It also removes one round trip of deinterleaving/interleaving + copy 
    > converting to/from float, which saves one memory copy. This extra round 
    > trip might have had the intention of clipping/sanitizing incoming data, 
    > which is only useful for `float`, not `int16_t`. 
    > 
    > Finally, this CL also hardens by rejecting potentially bad messages 
    > coming from the renderer, and using checked math when calculating 
    > memory allocation sizes. 
    > 
    > See linked bugs for additional details. 
    > 
    > Bug: 373960632, 482828615 
    > Change-Id: I03c0e3342651bc6b55aa3505206e54c1c56bac5e 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7573019 
    > Reviewed-by: Frank Liberato <liberato@chromium.org> 
    > Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    > Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    > Commit-Queue: Thomas Guilbert <tguilbert@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1586654} 
     
    Bug: 482828615 
    Change-Id: I03c0e3342651bc6b55aa3505206e54c1c56bac5e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7744897 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4869} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `content/browser/speech/speech_recognizer_impl.cc`
- M `content/browser/speech/speech_recognizer_impl.h`

---

Hash: [9142fa065c82837a8376932b2080494615352c5c](https://chromiumdash.appspot.com/commit/9142fa065c82837a8376932b2080494615352c5c)  

Date: Mon May 18 15:40:07 2026


---

### dx...@google.com (2026-05-19)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Tiago Vignatti [vignatti@google.com](mailto:vignatti@google.com)  

Link:    <https://chromium-review.googlesource.com/7744898>

[M144-LTS] Guard against 0 length in AudioChunk ctor

---


Expand for full commit details
```
     
    Original change's description: 
    > Guard against 0 length in AudioChunk ctor 
    > 
    > Recent changes spanified some aspect of `AudioChunk`, and changed the 
    > backing memory from `std::string` to `base::AlignedHeapArray`. 
    > 
    > This CL prevents CHECKs in `base::AlignedUninit` when the `length` 
    > passed to `AudioChunk`'s ctor is 0 
    > 
    > Bug: 485569900 
    > Change-Id: I0271fdd45310306aa35e29e1728630b7ee0a899c 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7588685 
    > Reviewed-by: Tommy Nyquist <nyquist@chromium.org> 
    > Commit-Queue: Thomas Guilbert <tguilbert@chromium.org> 
    > Auto-Submit: Thomas Guilbert <tguilbert@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1587492} 
     
    Bug: 482828615 
    Change-Id: I0271fdd45310306aa35e29e1728630b7ee0a899c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7744898 
    Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
    Commit-Queue: Tiago Vignatti (xWF) <vignatti@google.com> 
    Reviewed-by: Tommy Nyquist <nyquist@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4871} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `components/speech/audio_buffer.cc`
- M `components/speech/audio_buffer_unittest.cc`

---

Hash: [ab234fd84cd9d6801469fee29d7a2ea25a450e78](https://chromiumdash.appspot.com/commit/ab234fd84cd9d6801469fee29d7a2ea25a450e78)  

Date: Tue May 19 21:29:49 2026


---

### ch...@google.com (2026-05-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High Quality with Bisect. Sandbox escape / Memory corruption in a non-sandboxed process.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/482828615)*
