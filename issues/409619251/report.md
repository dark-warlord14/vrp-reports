# Buffer Overflow (GPU process) in Chrome Windows Media Foundation Encode Accelerator

| Field | Value |
|-------|-------|
| **Issue ID** | [409619251](https://issues.chromium.org/issues/409619251) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Windows |
| **Reporter** | el...@cryptosearch.tools |
| **Assignee** | eu...@chromium.org |
| **Created** | 2025-04-09 |
| **Bounty** | $15,000.00 |

## Description

---

### Report description

Buffer Overflow (GPU process) in Chrome Windows Media Foundation Encode Accelerator

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://www.google.com/chrome/>

---

### The problem

#### Please describe the technical details of the vulnerability

### Summary

There is a Buffer Overflow 0-day in Google Chrome on Windows. The Windows Media Foundation Video Encode Accelerator (which is used by default for H.264 encoding) estimates the buffer size required for encoded frames, and never explicitly checks for each encoded frame whether it actually fits in the provided buffer. This allows an attacker who can lure a victim using Windows to his HTML/JS page to trigger a buffer overflow in the highly privileged GPU process by calling the `VideoEncoder` in javascript using specific settings and high-entropy input data that will result in large encoded frame sizes. The buffer overflow is happening in the shared memory region in the virtual address space that used for inter-process communication.

### Vulnerable Code

The vulnerable calls are `memcpy` here:
<https://source.chromium.org/chromium/chromium/src/+/main:media/gpu/windows/media_foundation_video_encode_accelerator_win.cc;drc=34737a18832c71452ad1fdb4ca9970439daefcf4;l=2446>
<https://source.chromium.org/chromium/chromium/src/+/main:media/gpu/windows/media_foundation_video_encode_accelerator_win.cc;drc=34737a18832c71452ad1fdb4ca9970439daefcf4;l=797>

The buffer size estimation happens here:
<https://source.chromium.org/chromium/chromium/src/+/main:media/video/video_encode_accelerator.cc;drc=1e05ab5d3b3951f622ec8f64f326310aa47fc3c5;l=274>

While this estimate is sufficient for most cases, an attacker can specifically craft video data that will result in larger frames. The assumption that the encoded frame can never be larger than the input data plus headers is wrong, and the second limit based on the bitrate can be bypassed by using a large constant bitrate. However, in my opinion, the root issue is not the insufficient buffer size estimate, but the fact that an estimate is used at all without a rigid security check for each frame.

### Proof of Concept

In our PoC, we need to make the encoder generate at least one oversized frame. I have appended two scripts: `video13_configurable.html` allows the user to set parameters for video encoding and will trigger on the click of a button. It will automatically and randomly generate high-entropy data to attempt the generation of an oversized frame. It also computes the buffer size using the methods from the source code ("Raw" and "Expected", and "Final" is the maximum of those two that is used as the actual buffer size). `video15_autoload.html` will run without user interaction with the right settings (those that triggered the vulnerability on my machine) and a fixed seed for all random calls.

The exact parameters may depend on the browser version used as well as the Windows version, GPU and GPU driver version (everything that could affect how the Windows Media Foundation H.264 encoder is behaving). I executed my PoC on a GPU VPS (Basic GPU VPS - P600) from the hosting provider Database Mart LLC: <https://www.vps-mart.com/gpu-server>
The GPU used is NVIDIA Quadro P600. The driver version (according to `nvidia-smi`) is 556.39.

The Windows specifications are as follows:

```
Edition	Windows 10 Pro
Version	22H2
Installed on	‎3/‎6/‎2025
OS build	19045.5608
Experience	Windows Feature Experience Pack 1000.19061.1000.0

```

The Chrome version is the latest on the Stable Channel, at the time of writing:

```
135.0.7049.85 (Official Build) (64-bit) (cohort: 135.0.7049.84 Rollout) 

```

Important note: I was unable to trigger the vulnerability on the exact same version of the Chromium ASAN build - not because it seems fixed (according to the source code, it is not), but because - according to the data of my exploit script - I failed to find parameters that make the encoder exceed the estimated frame size for this version. Apparently, Chromium and Chrome use different code somewhere in the H.264 encoding process, and Chromium generates smaller frames. I was able to generate larger frames in an older ASAN build of Chromium (111.0.5554.0). It should be noted that no ASAN stack trace was generated by this build when the vulnerability was triggered - which is not surprising as the buffer overflow occurs in the shared memory region, where ASAN is not designed to detect buffer overflows, to my knowledge.

Chrome should be started with the following command:

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --enable-logging=stderr --v=1  

```

Use the following settings in the HTML page:

```
Width: 3400
Height: 100
Bitrate: 800
Framerate: 62
Bitrate Mode: Constant (CBR)
AVC Profile: High Profile (level 5.0)

```

The pattern settings can be left at default.

Once the vulnerability is triggered you will see a black-white flash covering the whole Chrome window and something like the following output in the command line:

```
[6824:7236:0409/152447.039:ERROR:gpu_process_host.cc(954)] GPU process exited unexpectedly: exit_code=-1073741819                                       [6824:7236:0409/152447.039:WARNING:gpu_process_host.cc(1395)] The GPU process has crashed 1 time(s)        
[6824:7236:0409/152447.480:WARNING:gpu_process_host.cc(976)] Reinitialized the GPU process after a crash. The reported initialization time was 349 ms     

```

I have appended a video that shows that the crash happens indeed exactly when we are expecting it according to our buffer size calculations, and otherwise the encoding functions normally.

### Potential for ACE Exploitation

This buffer overflow may be exploitable for ACE, which could be very dangerous as it happens in a highly privileged process (GPU process). Furthermore, the buffer overflow happens inside the shared memory region for inter-process communication. This could allow an attacker to tamper with memory sections that are relevant for communicating with the main process, even if it is not possible to gain ACE in the GPU process.

Writing arbitrary data is only constrained by what the H.264 algorithms can produce. I do not expect this to be the major challenge here, but it certainly an additional barrier for an attacker that the submitted data goes through a mathematical transformation first. Furthermore, guard areas, ASLR and other protections might make exploitation hard or impossible. I will investigate this further in the coming weeks and follow up here if successful to (hopefully) receive an increased bounty. I decided to submit this initial report right now in order to allow you immediate mitigation, given the severity of this bug (and to reduce the risk of someone else having submitted this issue first).

### Suggested Patch

Check whether the encoder output size is smaller or equal than `bitstream_buffer_size_` before calling `memcpy`.

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

This vulnerability allows an attacker to trigger a buffer overflow in the highly privileged Chrome GPU process on Windows, which might in the worst case result in Arbitrary Code Execution in the security context of the GPU process. The only user interaction required is visiting a HTML/JS website.

---

### The cause

#### What version of Chrome have you found the security issue in?

135.0.7049.85 [stable]

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Elias Hohl

## Attachments

- [video13_configurable.html](attachments/video13_configurable.html) (text/html, 48.3 KB)
- [gpu_process_crash.png](attachments/gpu_process_crash.png) (image/png, 149.1 KB)
- [video15_autoload.html](attachments/video15_autoload.html) (text/html, 42.8 KB)
- [chromium-exploit-video.mp4](attachments/chromium-exploit-video.mp4) (video/mp4, 27.6 MB)
- [video15_autoload.html](attachments/video15_autoload.html) (text/html, 42.8 KB)
- [chrome-video-callstack-2.png](attachments/chrome-video-callstack-2.png) (image/png, 325.1 KB)

## Timeline

### ma...@google.com (2025-04-10)

(Speculatively triaging for now.)

dalecurtis@ could you PTAL?

### ch...@google.com (2025-04-10)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### da...@chromium.org (2025-04-10)

Thanks for the report! You're right it's missing a size check. We should also spanify all this code to harden it further.

### ma...@google.com (2025-04-10)

It sounds like this issue might lead to RCE in the GPU process directly from the web, so changing severity to Critical/S0. dalecurtis@ (or eugene@), do you agree with that assessment?

### da...@chromium.org (2025-04-10)

Seems reasonable. The buffer is being overwritten with encoded data that isn't easily controllable, but is predictable to an extent. I could imagine that a specific family of hardware encoders could be predicted well enough to write a controlled stream of bytes.

### el...@cryptosearch.tools (2025-04-11)

Thanks for quickly addressing this report. I am additionally appending a screenshot of the Call Stack from Visual Studio Debugger as a further confirmation that my previously submitted root cause analysis was correct. The memcpy call causing the buffer overflow in this case was https://source.chromium.org/chromium/chromium/src/+/refs/tags/135.0.7049.85:media/gpu/windows/media_foundation_video_encode_accelerator_win.cc;drc=4e5c5443939dbcdac3c976a2e1805cc548a34783;l=2402

Regarding controllability of the encoded data - indeed the hardware encoders might not be 100% deterministic, but if it is possible to overcome other security mitigations that might be more effective (it could be impossible to reach relevant memory locations with the buffer overflow), then I think writing a controlled stream would likely not be the problem because
1. It might not be necessary to precisely control all output data that is written, precisely controlling a part of the stream may be sufficient
2. We have full control over the video input data
3. Only a few frames are required to trigger the vulnerability. Encoders probably behave more deterministically with a small number of frames, or at least there is a very limited amount of choices that can be made in terms of scheduling and parallelization
4. It seems like the GPU process is auto-restarting and we can keep the renderer alive, meaning we can attempt multiple times to exploit the vulnerability when the victim visits our HTML/JS page (so we could test exploits for different hardware / software / driver versions)

I will investigate further whether I can demonstrate RCE

In case you need anything else, feel free to let me know.

### dx...@google.com (2025-04-11)

Project: chromium/src  

Branch: main  

Author: Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6448912>

media: Spanify MediaFoundationVideoEncodeAccelerator

---


Expand for full commit details
```
     
    Bug: 409619251, 40285824, 338570700 
    Change-Id: Icbe9b7deb2d485f11327d1e233b5629480b40aad 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6448912 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Mustafa Emre Acer <meacer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1445651}

```

---

Files:

- M `gpu/ipc/common/dxgi_helpers.cc`
- M `gpu/ipc/common/dxgi_helpers.h`
- M `media/base/video_frame.cc`
- M `media/base/video_frame.h`
- M `media/base/win/mf_helpers.cc`
- M `media/base/win/mf_helpers.h`
- M `media/gpu/windows/media_foundation_video_encode_accelerator_win.cc`
- M `media/gpu/windows/mf_video_processor_accelerator_unittest.cc`
- M `media/gpu/windows/video_rate_control_wrapper.h`

---

Hash: b094accf6189985f07e7bfe576c6a11001099896  

Date:  Fri Apr 11 02:59:52 2025


---

### ch...@google.com (2025-04-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-04-11)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M134. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [134, 135, 136].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### eu...@chromium.org (2025-04-11)

1. https://chromium-review.googlesource.com/6448912
2. we don't have a reliable repro. so we can't really validate the fix.
3. no
4. no
5. no

### pg...@google.com (2025-04-14)

Linux doesnt have much canary data but the other platforms dont seem to have any relevant looking crashes in canary

Windows has [one](https://crash.corp.google.com/browse?q=product_name%3D%27Chrome%27+AND+product.version%3D%27137.0.7122.0%27+AND+STRPOS%28expanded_custom_data.ChromeCrashProto.magic_signature_1.name%2C+%27DXGI%27%29+%3E+0+AND+expanded_custom_data.ChromeCrashProto.magic_signature_1.name%3D%27%5BDump+without+crash%5D+gpu%3A%3A%60anonymous+namespace%5C%27%3A%3ADumpWithoutCrashingOnDXGIError%27) potentially but it doesnt appear to be caused by this CL. Please take another look at canary to ensure that this security fix will not be introducing any stability risks -

Merge approving, though not the usual merge cycle, given the severity of this bug and spanification not needing to jostle too much logic afaict:

merge approved for M135 - please merge ASAP to get this merged to the next stable respin!  

merge approved for M134 - please merge ASAP to get this merge into the next extended respin!  

merge approved for M136 - please merge this by Friday EOD MTC time to get this fix into the next stable release!

### el...@cryptosearch.tools (2025-04-14)

I have tested Windows Media Foundation video encoding on Chrome Canary 137.0.7123.0 (Offizieller Build) canary (64-Bit) (cohort: Clang-64) on two systems now: a) The one I described at the beginning of this report, and b) a different Windows machine with a different GPU and driver.

On both systems, video encoding with normal dimensions seems to work as usual, and the vulnerability seems fixed. When running my autoload exploit, no GPU process crash happens. The error that was shown in chrome://media-internals when the encoded frame exceeds the buffer size is "VEA adapter error. Code: 17. Message: Failed to copy bitstream media buffer.", which is consistent with the error code raised by your patch. 
In vulnerable Chrome versions, the error is "VEA adapter error. Code: 9. Message: Mojo is disconnected".

### eu...@chromium.org (2025-04-14)

This morning I was able to reproduce the GPU crash on stable 135.0.7049.85 and also verified the fix in canary.

### el...@cryptosearch.tools (2025-04-14)

I now looked deeper into where this bug was introduced, and it seems like this is very old code. The file containing the vulnerability was added in 2016:

```
commit e75bb4429ddcf2e79ae678a544064069718ee7a0
Author: emircan <emircan@chromium.org>
Date:   Thu Jul 21 09:51:28 2016 -0700

    H264 HW encode using MediaFoundation
    
    This CL adds MediaFoundationVideoEncodeAccelerator which enables H264 encode support
    using MediaFoundation on Windows 8.1+. Also, it includes a refactor of common
    MediaFoundation classes under mf_helpers.*.
    
    Note that, this is the first CL and H264 codec is still behind a flag.
    
    Design Doc(with perf measurements): http://goo.gl/UCnwyA
    
    BUG=590060
    TEST= Tested AppRTC loopback with Chrome flag "--enable-webrtc-hw-h264-encoding" and
    "--enable-mf-h264-encoding" on https://apprtc.appspot.com/?debug=loopback&vsc=h264
    Also, added WIN specific sections at vea_unittests.
    
    Review-Url: https://codereview.chromium.org/2058413003
    Cr-Commit-Position: refs/heads/master@{#406876}

```

It already contained all three `memcpy` statements (from which two are vulnerable, the third just copies to the temporary buffer initialized with the correct size). The calculation of `bitstream_buffer_size_` was done differently back then: Instead of `EstimateBitstreamBufferSize`, a much simpler approach was used - the size of the buffer was chosen to be simply the area of the input data - width times height in pixels. The current estimate is always larger (at least by a factor 1.5, from my understanding), so it should have been even easier to exploit the old one.

### dx...@google.com (2025-04-14)

Project: chromium/src  

Branch: refs/branch-heads/6998  

Author: Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6453840>

[M134] media: Spanify MediaFoundationVideoEncodeAccelerator

---


Expand for full commit details
```
     
    (cherry picked from commit b094accf6189985f07e7bfe576c6a11001099896) 
     
    Bug: 409619251, 40285824, 338570700 
    Change-Id: Icbe9b7deb2d485f11327d1e233b5629480b40aad 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6448912 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Mustafa Emre Acer <meacer@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1445651} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6453840 
    Reviewed-by: Prudhvikumar Bommana <pbommana@google.com> 
    Owners-Override: Prudhvikumar Bommana <pbommana@google.com> 
    Cr-Commit-Position: refs/branch-heads/6998@{#3332} 
    Cr-Branched-From: de9c6fafd8ae5c6ea0438764076ca7d04a0b165d-refs/heads/main@{#1415337}

```

---

Files:

- M `gpu/ipc/common/dxgi_helpers.cc`
- M `gpu/ipc/common/dxgi_helpers.h`
- M `media/base/video_frame.cc`
- M `media/base/video_frame.h`
- M `media/base/win/mf_helpers.cc`
- M `media/base/win/mf_helpers.h`
- M `media/gpu/windows/media_foundation_video_encode_accelerator_win.cc`
- M `media/gpu/windows/mf_video_processor_accelerator_unittest.cc`
- M `media/gpu/windows/video_rate_control_wrapper.h`

---

Hash: a47a6387b3c6d2be359e4de5a273cf28aba3daa4  

Date:  Mon Apr 14 21:06:05 2025


---

### dx...@google.com (2025-04-14)

Project: chromium/src  

Branch: refs/branch-heads/7049  

Author: Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6454954>

[M135] media: Spanify MediaFoundationVideoEncodeAccelerator

---


Expand for full commit details
```
     
    (cherry picked from commit b094accf6189985f07e7bfe576c6a11001099896) 
     
    Bug: 409619251, 40285824, 338570700 
    Change-Id: Icbe9b7deb2d485f11327d1e233b5629480b40aad 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6448912 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Mustafa Emre Acer <meacer@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1445651} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6454954 
    Owners-Override: Prudhvikumar Bommana <pbommana@google.com> 
    Reviewed-by: Prudhvikumar Bommana <pbommana@google.com> 
    Commit-Queue: Prudhvikumar Bommana <pbommana@google.com> 
    Cr-Commit-Position: refs/branch-heads/7049@{#1834} 
    Cr-Branched-From: 2dab7846d0951a552bdc4f350dad497f986e6fed-refs/heads/main@{#1427262}

```

---

Files:

- M `gpu/ipc/common/dxgi_helpers.cc`
- M `gpu/ipc/common/dxgi_helpers.h`
- M `media/base/video_frame.cc`
- M `media/base/video_frame.h`
- M `media/base/win/mf_helpers.cc`
- M `media/base/win/mf_helpers.h`
- M `media/gpu/windows/media_foundation_video_encode_accelerator_win.cc`
- M `media/gpu/windows/mf_video_processor_accelerator_unittest.cc`
- M `media/gpu/windows/video_rate_control_wrapper.h`

---

Hash: 5b308896c5e4f4810a5cc52d263dfd628a25cc3e  

Date:  Mon Apr 14 21:06:35 2025


---

### dx...@google.com (2025-04-14)

Project: chromium/src  

Branch: refs/branch-heads/7103  

Author: Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6455365>

[M136] media: Spanify MediaFoundationVideoEncodeAccelerator

---


Expand for full commit details
```
     
    (cherry picked from commit b094accf6189985f07e7bfe576c6a11001099896) 
     
    Bug: 409619251, 40285824, 338570700 
    Change-Id: Icbe9b7deb2d485f11327d1e233b5629480b40aad 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6448912 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Reviewed-by: Mustafa Emre Acer <meacer@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1445651} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6455365 
    Commit-Queue: Prudhvikumar Bommana <pbommana@google.com> 
    Owners-Override: Prudhvikumar Bommana <pbommana@google.com> 
    Reviewed-by: Prudhvikumar Bommana <pbommana@google.com> 
    Cr-Commit-Position: refs/branch-heads/7103@{#890} 
    Cr-Branched-From: e09430c64983fc906f37a9f7e6806275c9b67b86-refs/heads/main@{#1440670}

```

---

Files:

- M `gpu/ipc/common/dxgi_helpers.cc`
- M `gpu/ipc/common/dxgi_helpers.h`
- M `media/base/video_frame.cc`
- M `media/base/video_frame.h`
- M `media/base/win/mf_helpers.cc`
- M `media/base/win/mf_helpers.h`
- M `media/gpu/windows/media_foundation_video_encode_accelerator_win.cc`
- M `media/gpu/windows/mf_video_processor_accelerator_unittest.cc`
- M `media/gpu/windows/video_rate_control_wrapper.h`

---

Hash: ce0ed020f12bbc1878536846a134f64f11fa0582  

Date:  Mon Apr 14 21:25:32 2025


---

### am...@chromium.org (2025-04-16)

Converting this to S1 / high severity since the GPU process on Windows is sandboxed.

### el...@cryptosearch.tools (2025-04-16)

Dear Chrome team, wasn't S0 initially justified because the GPU process, although sandboxed, is a "highly privileged process", according to the Chrome VRP website? From my understanding, it has more privileges than the renderer processes and could also - in contrast to a compromised renderer - affect other Chrome tabs than the attacker's page itself (visual spoofing / stealing confidential data)

### sp...@google.com (2025-04-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
high-quality report of memory corruption in a highly privileged process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-18)

Congratulations Elias! Thank you for your efforts and your high-quality reporting this issue to us -- great work!

### aj...@chromium.org (2025-06-02)

Regarding comment 20 - we believe the GPU process to be reasonably sandboxed on Windows (<https://source.chromium.org/chromium/chromium/src/+/main:docs/security/process-sandboxes-by-platform.md>) so the severity rating follows our guidelines.

### ch...@google.com (2025-07-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### el...@cryptosearch.tools (2025-08-07)

Thank you for the reward and sorry for my late response! I have researched this further, I built a C++ application that uses the Media Foundation Video Encode Accelerator with the same settings as Chrome, and investigated the behavior of the encoder. I managed to simplify the video data triggering the bug, confirmed the encoder is fully deterministic (at least on the system I used), that it is possible to configure and reset the encoder in a way that every second frame will be encoded to the same data as if it was a single-frame video, that its length is quite well controllable, and that a large variety of controlled data could be written. I am not sure whether it is possible to mathematically "invert" the encoder with the constraints present, so I investigated using a brute-force approach. It helps that the bitstream buffers are reused, so we can write bytes one by one (triggering overflow with length L, then L - 1, L - 2, etc. to write the desired sequence). The output distribution of the last byte is very interesting. Although there are only a few specifically forbidden (control) sequences at the end of the frame, some bytes occur commonly, and others almost never (or maybe really never). To conclude what is really not possible / write almost all bytes, one would need to bruteforce the encoder longer, or use a better GPU. Unfortunately, once I had arrived at this point, the (already extended) deadline was already near, so I did not continue researching the heap layout in Chrome. What I figured out is dimensions and settings to use that the shared memory buffer gets allocated exactly into a 64KiB VirtualAlloc region, without any nonaccessible 4KiB in the way to the next VirtualAlloc region. It might be hard to achieve RCE because to write into an adjacent heap region, one needs to smash through the metadata, so the heap region will be fragile afterwards. And PartitionAlloc objects cannot be used at all because they are protected by guard pages.

If you are interested in my code that I used to analyze the encoder behavior, feel free to let me know, I can upload it here.

Regarding the bounty - I understand that the GPU process is sandboxed on Windows, which means - according to my understanding - it falls in the middle of the three categories in the table (privileged process, where the GPU process is specifically mentioned. I conclude this refers to a sandboxed GPU process, because the unsandboxed Android GPU process is specified in the high category), which assigns $15000 bounty for a high-quality memory corruption report. If the GPU process was unsandboxed on Windows, I think it would fall into the high category (where the Android GPU process is specifically mentioned because it is unsandboxed). However, that's not the case and that's not what I was referring to - I was referring to the footnote [2] "Amounts are based on the precondition of a compromised renderer, otherwise the equivalent renderer reward will also be added.", which is present for both the middle and high categories. That's how I understood it, but maybe I am just reading it the wrong way. In any case, thanks a lot for the bounty that I already received!

## Bounty Award

> high-quality report of memory corruption in a highly privileged process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/409619251)*
