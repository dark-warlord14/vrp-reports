# Out-of-bounds heap read in VP9 encoder via WebCodecs VideoEncoder dimension reconfiguration

| Field | Value |
|-------|-------|
| **Issue ID** | [489755020](https://issues.chromium.org/issues/489755020) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>WebCodecs |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ca...@gmail.com |
| **Assignee** | jz...@google.com |
| **Created** | 2026-03-04 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

**This is meant to track the merge request for libvpx (VP9) as part of [b/487259772](https://issues.chromium.org/issues/487259772). That bug covers both libvpx and libaom (AV1) and a fix is still pending for AV1.**

Out-of-bounds heap read in VP9 encoder via WebCodecs VideoEncoder dimension reconfiguration

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/+/main/third_party/libvpx/source/libvpx/vp9/encoder/>

---

### The problem

#### Please describe the technical details of the vulnerability

Calling `configure()` with changing dimensions on a WebCodecs `VideoEncoder` (VP9 or AV1), followed by `encode()` without waiting for the previous encode to complete, causes memory corruption in both the VP9 and AV1 encode pipelines. The crash is stochastic and typically fires within 30 to 80 rounds of rapid dimension changes.

Tested on Windows 10 x64, reproduced on both ASAN Chrome 147.0.7696.0 and latest stable Chrome 145.0.7632.110.

The core issue is in Chrome's `OffloadingVideoEncoder`, which dispatches `Encode` and `ChangeOptions` (the internal path for JS `configure()`) onto the encoder's task queue without properly serializing them. When `configure()` arrives while codec-internal row-MT worker threads are still mid-encode, the reconfigure tears down internal state (reference frame buffers, context structures) while those threads still hold live pointers into the old allocations.

The ASAN task traces for both crashes confirm this interleaving:

```
OffloadingVideoEncoder::Encode
OffloadingVideoEncoder::WrapCallback
OffloadingVideoEncoder::ChangeOptions    <- reconfigure while encode in flight
OffloadingVideoEncoder::WrapCallback

```

When the encoder gets reconfigured to different dimensions, internal reference frame buffers from earlier configurations remain in the encoder's buffer pool while the encoder begins operating at the new dimensions. Motion estimation then computes offsets into these undersized reference buffers using the new dimensions, reading past the end of the allocation.

The row-MT worker thread (`enc_row_mt_worker_hook`) continues executing `vp9_pick_inter_mode`, which calls into SAD (sum of absolute differences) functions against a reference frame buffer that's already been freed and reallocated for the new dimensions. The SAD function reads a 64x64 block at a stride (`rdx=0x360`, 864 bytes) calibrated to the old frame width, walking off the end of the new allocation. ASAN catches this as an access-violation READ at a heap address, confirming genuine use-after-free with heap-relative addressing.

By toying with the timing and dimension configurations, we've been able to hit multiple crash sites in the VP9 path. The primary crash is in `vpx_sad64x64_avx2` (sad\_avx2.c:113), but we've also triggered `vpx_sad16x16_sse2` with smaller dimension transitions. The crash site depends on which block partition size the encoder selects for the current superblock, which varies with the dimension mismatch and content. By carefully selecting the dimensions we have some control over the length of the read (64x64, 32x32, 16x16, 8x, 4x), making it a controlled read.

The VP9 path requires `latencyMode: 'realtime'` to force threaded tile encoding (`vp9_encode_tiles_row_mt`), which widens the race window. Rapid dimension changes across superblock/MI allocation boundaries (e.g. 120x120 to 128x128, crossing mi\_cols 15 to 16) maximize the likelihood that the internal reallocation changes buffer sizes and strides. The race is reachable from any origin via the WebCodecs `VideoEncoder` API with no user interaction, permissions, or flags required. Both crashes occur in the renderer process on a thread pool worker thread (T5/T6).

**AV1 (libaom):** The same root cause also affects the AV1 encoder, which is expected given that libaom's buffer pool design and encoder architecture originate from its fork of libvpx. The AV1 variant manifests differently: `av1_encode_tiles_row_mt` calls `memset` on a buffer pointer that the reconfigure has already nulled out, resulting in a WRITE to `0x000000000000` (`rax=0` at crash). Unlike VP9 where libvpx leaves the pointer dangling, libaom's teardown zeroes it, so it surfaces as a null dereference rather than a UAF. AV1 triggers under default encoder settings without needing `latencyMode: 'realtime'`.

Reproducer: open the attached HTML, click VP9 or AV1, wait. It calls `configure()` with random dimensions (1x1 through 800x600) followed by `encode()` in a loop. On the systems I've tested this on the VP9 crash happens roughly after 30 seconds, the AV1 crash is close to instant.

#### Impact analysis

At minimum this is an controlled out-of-bounds heap read in the renderer process, triggerable from any webpage via the WebCodecs API without user interaction. On most heap layouts the read hits unmapped pages and crashes the tab. When adjacent pages happen to be committed, the read crosses into neighboring allocations, which could theoretically be an information disclosure or ASLR bypass vector, with the right heap massaging and finding an read length that ends up in between the padding of the frame and end of mapped heap pages, though we haven't been able to demonstrate that from JavaScript.

Since the underlying issue is the encoder operating in an invalid state (mismatched dimensions between active config and retained reference buffers), it's hard to fully determine the impact. The bug surfaces as an OOB read in VP9 motion estimation, but the same invalid state is present throughout the encode pipeline. We've confirmed multiple crash sites in the VP9 path (`vpx_sad64x64_avx2`, `vpx_sad16x16_sse2`) depending on timing and dimension configuration, which supports this: the stale reference buffers are reachable from various points in the encoder, and which one faults first depends on the specific encode parameters. The AV1 variant crashing as a write to a low constant address rather than a heap read further supports the idea that the consequences depend on which code path encounters the stale buffers first. Other code paths in the encoder that touch reference frames (reconstruction, loop filtering, etc.) could potentially be reached with different exploitation strategies.

---

### The cause

#### What version of Chrome have you found the security issue in?

[147.0.7696.0] + [ASAN], [145.0.7632.110] + [stable]

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Casper Woudenberg

## Timeline

### jz...@google.com (2026-03-04)

See the parent, [b/487259772](https://issues.chromium.org/issues/487259772), for further background. The issue is related to frame offsets that may surface as heap-overflow (read) or use-after-free (read) depending on the input.

### ch...@google.com (2026-03-04)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-04)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### jz...@google.com (2026-03-04)

> 1. Why does your merge fit within the merge criteria for these milestones?
> 
> - Chrome Browser: <https://chromiumdash.appspot.com/branches>
> - Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

Security fix: heap-overflow (read) / use-after-free (read).

> 2. What changes specifically would you like to merge? Please link to Gerrit.

- <https://crrev.com/c/7624803>
- <https://crrev.com/c/7624804>

> 3. Have the changes been released and tested on canary?

Yes. Confirmed in 147.0.7717.0.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>

N/A.

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.

### ch...@google.com (2026-03-04)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### jz...@google.com (2026-03-04)

<https://chromium-review.git.corp.google.com/c/chromium/src/+/7629421> contains the fix.

```
Roll src/third_party/libvpx/source/libvpx/ 4fcebeabe..9a2d3d1f4 (2 commits)

https://chromium.googlesource.com/webm/libvpx.git/+log/4fcebeabe58e..9a2d3d1f46af

$ git log 4fcebeabe..9a2d3d1f4 --date=short --no-merges --format='%ad %ae %s'
2026-03-02 jzern vp9_scale_references: fail if no free buffer is available
2026-03-02 jzern vp9_pick_inter_mode: fix buf offsets w/scaled refs

Created with:
  roll-dep src/third_party/libvpx/source/libvpx

Bug: 487259772, 308446709
Change-Id: I15f4759b1dec9c73042986f1ad6cc161445cb2c3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7629421
Reviewed-by: Wan-Teh Chang <wtc@google.com>
Commit-Queue: James Zern <jzern@google.com>
Cr-Commit-Position: refs/heads/main@{#1593487}

```

### jz...@google.com (2026-03-04)

> If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.

I missed this part:

- <https://crrev.com/c/7624803>
- <https://crrev.com/c/7624804>

### dr...@chromium.org (2026-03-04)

From the security side, I don't think we need to merge anything here. Assuming all of these bugs are just reads of same-process memory, the security impact wouldn't justify the stability risk.

But there's a lot of CLs here. How confident are we that these are all read-only?

### jz...@google.com (2026-03-04)

These are source buffers, so they'll be read to gather statistics, but not written to. Stats output is to a single return value (or a handful). The output buffers are the correct size in this case. The test cases will normally pass without a sanitizer present unless the read is grossly out of range.

### dr...@chromium.org (2026-03-04)

Okay thank you, I think we can remove the merge labels then.

### vi...@google.com (2026-05-12)

Labeling as `LTS-NotApplicable-144` based on [#comment10](https://issues.chromium.org/issues/489755020#comment10) and [#comment11](https://issues.chromium.org/issues/489755020#comment11).

### ch...@google.com (2026-06-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/489755020)*
