# Uninitialized alpha-plane padding in VP9-with-alpha external frame buffer decode causes renderer heap data disclosure via WebCodecs VideoFrame.copyTo(codedRect)

| Field | Value |
|-------|-------|
| **Issue ID** | [486506202](https://issues.chromium.org/issues/486506202) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gi...@octane.security |
| **Assignee** | eu...@chromium.org |
| **Created** | 2026-02-22 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Uninitialized alpha-plane padding in VP9-with-alpha external frame buffer decode causes renderer heap data disclosure via WebCodecs VideoFrame.copyTo(codedRect)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://github.com/chromium/chromium>

---

### The problem

#### Please describe the technical details of the vulnerability

When decoding WebM **VP9** content with alpha enabled, Chromium allocates an **uninitialized** alpha-plane buffer and fills only the **visible-width** alpha pixels. If the decoded frame's **coded width is greater than its visible width** (e.g. due to stride alignment), the **per-row padding bytes** in the alpha plane are never written and remain uninitialized. WebCodecs `VideoFrame.copyTo()` allows JavaScript to request a copy using a rectangle bounded by the frame's **coded size**. For CPU-backed (mappable) frames, the Blink copy path copies **`src_rect.width()` bytes per row** from each plane and does **not** clamp to the visible rect. By calling `copyTo()` with a rect that spans the full coded width and height, an attacker can copy and then read the uninitialized alpha-plane padding bytes from JavaScript, resulting in **renderer heap information disclosure**.

**Root cause chain**

1. **WebM / demuxer:** When the track has `AlphaMode` = 1 and a block has block-additional data whose **first 8 bytes** (BlockAddID, big endian) equal **1**, the remainder is stored in `DecoderBuffer::side_data()->alpha_data` (see `media/formats/webm/webm_cluster_parser.cc` and `webm_video_client.cc`).
2. **Decoder:** In `VpxVideoDecoder`, the VP9 external frame buffer path allocates the alpha plane in `FrameBufferPool::AllocateAlphaPlaneForFrameBuffer()` (`media/base/frame_buffer_pool.cc`), which uses `base::UncheckedMalloc()` and **does not initialize** the memory (comment: *"the new array is purposely not initialized"*). The alpha plane is then filled via `libyuv::CopyPlane()` with **width = `vpx_image_alpha->d_w`** (visible width) and height = `d_h`. The allocation size is **stride × height** (e.g. `vpx_image_alpha->stride[VPX_PLANE_Y] * d_h`). When stride (coded width) > `d_w`, the bytes at the end of each row are never written.
3. **VideoFrame:** The resulting `VideoFrame` has `coded_size()` from `(vpx_image->w, vpx_image->d_h)` and `visible_rect()` from `(d_w, d_h)`. So `coded_size.width()` can exceed `visible_rect().width()`.
4. **WebCodecs:** In Blink, `VideoFrame.copyTo(options)` validates the source rect against the frame's **coded size** (`ParseCopyToOptions` → `ToGfxRect(..., frame.coded_size(), ...)`). For mappable frames, `CopyMappablePlanes()` copies `PlaneSize(src_rect.width(), ...)` bytes per row from each plane (`third_party/blink/renderer/modules/webcodecs/video_frame.cc`). No clamping to the visible rect is applied, so a rect covering the full coded size causes the uninitialized padding to be copied into the destination buffer and exposed to script.

**Precondition:** The decoded frame has **coded width > visible width** (e.g. odd or non-aligned width such as 9 or 17). When this holds, the read is deterministic; the **content** of the leaked bytes depends on allocator state (prior heap usage).

#### Impact analysis

**Who can exploit it**

Any **attacker who can run JavaScript in the renderer** can exploit this, for example by hosting a page that the victim visits (e.g. via link, ad, or compromised site), or by utilizing an XSS primitive or other bug that allows execution of script in a Chrome tab. No special permissions or user interaction beyond loading the page are required.

**What they gain**

The attacker gains **read access to uninitialized renderer heap memory** (the alpha-plane padding). That can include pointers (e.g. heap addresses), which can support ASLR bypass or heap layout inference, leftover data from previous allocations (strings, structures, etc.), and stable information disclosure when the same allocation patterns are repeated (e.g. repeated decoding with the same or similar frame sizes). By itself, it does not escape the renderer sandbox or escalate privileges, but it turns an information-disclosure primitive into javascript-readable data that can support further exploitation (e.g. heap grooming, pointer leaks for a separate bug).

**Severity Analysis**

Given the Severity Guidelines for Security Issues, a [medium severity](https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#toc-medium-severity) classification is well-supported for this finding.

---

### The cause

#### What version of Chrome have you found the security issue in?

Current Live Stable Release: 145.0.7632.110 and 145.0.7632.103

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Information Leak

#### How would you like to be publicly acknowledged for your report?

Identified by the Octane Security Team: Giovanni Vignone, Paolo Gentry, Robert van Eijk

## Attachments

- [report.md](attachments/report.md) (application/octet-stream, 5.3 KB)
- [exploit_poc.html](attachments/exploit_poc.html) (text/html, 4.2 KB)
- [heap_ptr_leak.html](attachments/heap_ptr_leak.html) (text/html, 2.4 KB)
- [vp9_17x17.webm](attachments/vp9_17x17.webm) (video/webm, 996 B)
- [2026-02-24 00-04-14.mp4](attachments/2026-02-24 00-04-14.mp4) (video/mp4, 28.8 MB)
- [heap_ptr_leak.html](attachments/heap_ptr_leak_73806579.html) (text/html, 3.9 KB)
- [exploit_poc.html](attachments/exploit_poc_73806557.html) (text/html, 5.8 KB)

## Timeline

### gi...@octane.security (2026-02-22)

Hi this issue was categorized incorrectly because I believe we selected the wrong issue category "Information Leak" instead of "Memory Corruption (in a sandboxed process)", it should be a P1 not a P4 as it is a memory corruption issue that could be useful in potential memory corruption exploits, or exposure of sensitive user information that an attacker can exfiltrate

### an...@chromium.org (2026-02-23)

Hello, please provide detailed reproduction steps. The attached video file doesn't play for me - so please provided an updated one. Thanks!

### gi...@octane.security (2026-02-23)

Please inspect the contents of "report.md" for the full report with detailed reproduction steps

the .webm in the attachment is a specific file required to trigger the vulnerability and is not meant as intructional materials but rather as part of the Proof-of-Concept.

the included .html files as well as the .webm are to be placed inside the webroot of a webserver such as through the following python3 command:

---
python3 -m http.server 8000
---

then navigate to:
http://127.0.0.1:8000/exploit_poc.html

Observe the hexdump of a leaked uninitialized heap chunk being displayed


navigate to:
http://127.0.0.1:8000/heap_ptr_leak.html

observe a heap pointer being extracted from the leak

please refer to the report.md file for a full detailed writeup on the cause of the vulnerability as well as the detailed reproduction steps

### pe...@google.com (2026-02-23)

Thank you for providing more feedback. Adding the requester to the CC list.

### gi...@octane.security (2026-02-23)

Absolutely, no problem! Happy to help. Please let me know if there's anything else I can provide

### li...@chromium.org (2026-02-25)

@da...@chromium.org - do you mind taking a look or reassigning as necessary?

### da...@chromium.org (2026-02-26)

Eugene, can you take a look? It seems like another oversight in copyTo bounds.

### da...@chromium.org (2026-02-26)

There's no reason to allow copying from the coded rect, but it might be too late to change, in which case we may need to zero the initial allocations. UncheckedCalloc may not cost much more here.

### ch...@google.com (2026-02-26)

Setting milestone because of s2 severity.

### eu...@chromium.org (2026-02-27)

alleged leak comes from VpxVideoDecoder

### eu...@chromium.org (2026-02-27)

well need to use `FrameBufferPool` with `zero_initialize_memory = true` everywhere like we already do for ffmpeg

### eu...@chromium.org (2026-02-27)

one file with standalone repro

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  main  

Author:  Eugene Zemtsov [eugene@chromium.org](mailto:eugene@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7616614>

media: Zero-initialize frames in software decoders to prevent info leaks

---


Expand for full commit details
```
     
    Pass `zero_initialize_memory=true` when creating FrameBufferPools for 
    libvpx and dav1d decoders. Also update AllocateAlphaPlaneForFrameBuffer 
    to respect this flag. This prevents potential heap information 
    disclosure from uninitialized padding bytes. 
     
    We already do it for ffmpeg decoder. 
     
    Bug: 486506202 
    Change-Id: I5e88f827f7043cfebef140524092e5543d7d03a3 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7616614 
    Reviewed-by: Dale Curtis <dalecurtis@chromium.org> 
    Commit-Queue: Eugene Zemtsov <eugene@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1592929}

```

---

Files:

- M `media/base/frame_buffer_pool.cc`
- M `media/base/frame_buffer_pool_unittest.cc`
- M `media/filters/dav1d_video_decoder.cc`
- M `media/filters/vpx_video_decoder.cc`

---

Hash: [c0244cac701a5bfadcd275dc10ee3d12ef593908](https://chromiumdash.appspot.com/commit/c0244cac701a5bfadcd275dc10ee3d12ef593908)  

Date: Tue Mar 3 03:16:41 2026


---

### gi...@octane.security (2026-03-03)

Hi Eugene, thank you for the quick investigation and fix — really appreciate the turnaround.

Now that the issue has been marked as fixed, could you please confirm:

1. The final severity classification for this issue
2. The expected VRP payout range and payout timeline

Also confirming that the preferred public credit is:

Identified by Octane Security's AI with collaboration from:
Giovanni Vignone, Paolo Gentry, Robert van Eijk

Please let me know if any additional information is needed from our side.

Thanks again for addressing this so quickly

### eu...@chromium.org (2026-03-04)

it's not up to me to decide

### gi...@octane.security (2026-03-04)

Understood, and thank you a lot for the fast reply. Would you mind looping in the right person to handle the above?

### gi...@octane.security (2026-03-11)

Hi all, is there any update on the following...

1. The final severity classification for this issue
2. The expected VRP payout range and payout timeline

Thank you in advance!

### gi...@octane.security (2026-03-16)

Hi following up on the above here!

### gi...@octane.security (2026-03-25)

Hi please provide an update here

### dr...@chromium.org (2026-03-25)

Your bug is in the VRP reward queue (hotlist reward-topanel). Final severity and payout will be determined when it gets through the queue. We can't provide any evaluation in advance.

### gi...@octane.security (2026-04-08)

Hi any update from the panel?

### gi...@octane.security (2026-05-25)

Hi there, can someone please provide an update, it's been 3 months from submission

### ch...@google.com (2026-06-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486506202)*
