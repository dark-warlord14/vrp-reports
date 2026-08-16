# Potential UAF write in GPU process via glBufferData OOM on Android

| Field | Value |
|-------|-------|
| **Issue ID** | [507707838](https://issues.chromium.org/issues/507707838) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vm...@google.com |
| **Assignee** | sh...@google.com |
| **Created** | 2026-04-29 |
| **Bounty** | $25,000.00 |

## Description

---

### Report description

GPU passthrough decoder UAF: DoBufferData GL error path skips mapped\_buffer\_map.erase()

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

### Vulnerability Description

GLES2DecoderPassthroughImpl::DoBufferData in the GPU passthrough decoder does not clean up the mapped\_buffer\_map entry when glBufferData returns a GL error. The result is that DoUnmapBuffer later finds a stale entry with map\_ptr pointing to freed driver memory and writes renderer-controlled data into it.

The relevant code in gles2\_cmd\_decoder\_passthrough\_doers.cc (current HEAD, ~line 618):

```
  CheckErrorCallbackState();
  api()->glBufferDataFn(target, size, data, usage);
  if (CheckErrorCallbackState()) {
    return error::kNoError;   // early return, no erase
  }
  resources_->mapped_buffer_map.erase(bound_buffers_[target]);  // not reached on error

```

CheckErrorCallbackState() works through the KHR\_debug callback (PassthroughGLDebugMessageCallback -> OnDebugMessage -> had\_error\_callback\_ = true). Any GL error from glBufferDataFn causes the early return. The most impactful case is GL\_OUT\_OF\_MEMORY, where the driver frees the old backing store and the map\_ptr in the remaining mapped\_buffer\_map entry now points to freed memory.

The same vulnerability was fixed in the validating decoder in commit daeb9ba8d7ce
([Bug 498715368](https://issues.chromium.org/issues/498715368)) with this comment in buffer\_manager.cc:

```
  // SECURITY: ... Clear it here so that UnmapBufferHelper does not memcpy
  // renderer-controlled SHM into freed driver memory.
  buffer->ClearMapping();

```

The passthrough decoder was not included in that fix.

### Attack Preconditions

Attacker has a compromised renderer process (standard precondition for GPU process bugs). The GPU passthrough decoder must be active, which is the case by default on Windows, macOS, and Linux: ui/gl/features.gni sets enable\_validating\_command\_decoder = is\_android, so on desktop builds UsePassthroughCommandDecoder() in gl\_utils.cc returns true unconditionally.

### Reproduction Steps / POC

I added a regression test to the existing passthrough decoder test suite:
gpu/command\_buffer/service/gles2\_cmd\_decoder\_passthrough\_unittest\_buffers.cc

Test name: GLES3DecoderPassthroughTest.BufferDataGLErrorLeavesStaleMapEntry

Steps the test performs:

1. Create and bind a buffer, map it with GL\_MAP\_WRITE\_BIT. Confirms the entry is added to mapped\_buffer\_map.
2. Submit a BufferData command with size=-1. This triggers GL\_INVALID\_VALUE, which fires the KHR\_debug callback and causes DoBufferData to take the early-return path. Functionally the same as GL\_OUT\_OF\_MEMORY for this code path.
3. Assert that the mapped\_buffer\_map entry is still present (bug confirmed).

Output from the ASAN build (out/asan/gpu\_unittests, macOS arm64, ANGLE null backend):

```
  [ RUN      ] GLES3DecoderPassthroughTest.BufferDataGLErrorLeavesStaleMapEntry
  [ERROR] GL_INVALID_VALUE: glBufferData: Negative size.
  [       OK ] GLES3DecoderPassthroughTest.BufferDataGLErrorLeavesStaleMapEntry (3584 ms)

```

The EXPECT\_NE assertion passes, confirming the stale entry is present after the GL error. On real hardware with GL\_OUT\_OF\_MEMORY the map\_ptr would point to freed driver memory, and a subsequent glUnmapBuffer call from the renderer would trigger:

```
memcpy(map_info.map_ptr, renderer_shm, map_info.size)

```

That memcpy is a heap-use-after-free write in the GPU process with renderer-controlled content and size.

Fix: add the erase before the early return in DoBufferData:

```
  if (CheckErrorCallbackState()) {
      resources_->mapped_buffer_map.erase(bound_buffers_[target]);
      return error::kNoError;
  }

```
#### Impact analysis

A compromised renderer can trigger this by mapping a GPU buffer, then calling glBufferData with a large enough size to cause GL\_OUT\_OF\_MEMORY. The GPU driver frees the old backing store. DoBufferData returns early without erasing the mapped\_buffer\_map entry. The renderer then calls glUnmapBuffer, which causes the GPU process to write attacker-controlled data into freed driver memory.

This gives an attacker a heap-use-after-free write primitive in the GPU process, with control over the write destination (via timing/heap grooming), the content (shared memory), and the size. The GPU process is a sandboxed process separate from the renderer. Exploiting this primitive to achieve GPU process code execution would constitute a sandbox escape from a compromised renderer.

The bug affects all desktop Chrome users on Windows, macOS, and Linux, since the passthrough decoder is enabled by default on those platforms.

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7815.0 (dev/canary) - confirmed on HEAD commit fc933fae76 (2026-04-28) 147.0.7727.138 (stable) - affected, bug predates current HEAD

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

tohafrit

## Attachments

- [gpu_passthrough_uaf_bufferdata.md](attachments/gpu_passthrough_uaf_bufferdata.md) (text/markdown, 6.5 KB)
- [gpu_passthrough_uaf_test.patch](attachments/gpu_passthrough_uaf_test.patch) (application/octet-stream, 3.3 KB)
- [gpu_passthrough_uaf_test_output.txt](attachments/gpu_passthrough_uaf_test_output.txt) (text/plain, 1.1 KB)

## Timeline

### ka...@google.com (2026-04-30)

Unsandboxed GPU process UAF, requires a renderer process compromise. S1

Assigning to Shrek who worked on the cited similar [bug 498715368](https://issues.chromium.org/issues/498715368) in the validating command decoder: <https://crrev.com/c/7727794>

### ch...@google.com (2026-05-01)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-05-04)

Project: chromium/src  

Branch:  main  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7808748>

gpu: Fix UAF in passthrough decoder DoBufferData

---


Expand for full commit details
```
     
    GLES2DecoderPassthroughImpl::DoBufferData does not clean up the 
    mapped_buffer_map entry when glBufferData returns a GL error. 
    The result is that DoUnmapBuffer later finds a stale entry with 
    map_ptr pointing to freed driver memory and writes renderer-controlled 
    data into it. 
     
    This CL fixes the issue by erasing the entry from mapped_buffer_map 
    even if glBufferData returns an error, preventing the potential 
    heap-use-after-free write. 
     
    Bug: 507707838 
    Change-Id: I51d7eb959a8f11077e05b73e86d16d9fae850047 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7808748 
    Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    Commit-Queue: Shrek Shao <shrekshao@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1624914}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_unittest_buffers.cc`

---

Hash: [13532776ca8af93b5254efd1ac3cd4db62bddd6c](https://chromiumdash.appspot.com/commit/13532776ca8af93b5254efd1ac3cd4db62bddd6c)  

Date: Mon May 4 20:58:01 2026


---

### sp...@google.com (2026-05-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Baseline. Memory corruption in a highly privileged process (e.g. GPU, network processes) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 149.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514926300](https://crbug.com/514926300) to have this merge reviewed.**

### dx...@google.com (2026-05-21)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7864747>

[M148] gpu: Fix UAF in passthrough decoder DoBufferData

---


Expand for full commit details
```
     
    Original change's description: 
    > gpu: Fix UAF in passthrough decoder DoBufferData 
    > 
    > GLES2DecoderPassthroughImpl::DoBufferData does not clean up the 
    > mapped_buffer_map entry when glBufferData returns a GL error. 
    > The result is that DoUnmapBuffer later finds a stale entry with 
    > map_ptr pointing to freed driver memory and writes renderer-controlled 
    > data into it. 
    > 
    > This CL fixes the issue by erasing the entry from mapped_buffer_map 
    > even if glBufferData returns an error, preventing the potential 
    > heap-use-after-free write. 
    > 
    > Bug: 507707838 
    > Change-Id: I51d7eb959a8f11077e05b73e86d16d9fae850047 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7808748 
    > Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    > Commit-Queue: Shrek Shao <shrekshao@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1624914} 
     
    (cherry picked from commit 13532776ca8af93b5254efd1ac3cd4db62bddd6c) 
     
    Bug: 514926300,507707838 
    Change-Id: I51d7eb959a8f11077e05b73e86d16d9fae850047 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7864747 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Reviewed-by: Kai Ninomiya <kainino@chromium.org> 
    Commit-Queue: Shrek Shao <shrekshao@google.com> 
    Reviewed-by: Shrek Shao <shrekshao@google.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3419} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_unittest_buffers.cc`

---

Hash: [cab2a7414afc2d2fb618b0e99c40d8cff0f08c96](https://chromiumdash.appspot.com/commit/cab2a7414afc2d2fb618b0e99c40d8cff0f08c96)  

Date: Thu May 21 19:37:42 2026


---

### pe...@google.com (2026-05-21)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### sh...@google.com (2026-05-21)

1. no
2. no

### pe...@google.com (2026-05-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-27)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7874065>
2. Low - There was no conflict.
3. 148
4. Yes.

### dx...@google.com (2026-05-29)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Shrek Shao [shrekshao@google.com](mailto:shrekshao@google.com)  

Link:    <https://chromium-review.googlesource.com/7874065>

[M144-LTS] gpu: Fix UAF in passthrough decoder DoBufferData

---


Expand for full commit details
```
     
    GLES2DecoderPassthroughImpl::DoBufferData does not clean up the 
    mapped_buffer_map entry when glBufferData returns a GL error. 
    The result is that DoUnmapBuffer later finds a stale entry with 
    map_ptr pointing to freed driver memory and writes renderer-controlled 
    data into it. 
     
    This CL fixes the issue by erasing the entry from mapped_buffer_map 
    even if glBufferData returns an error, preventing the potential 
    heap-use-after-free write. 
     
    (cherry picked from commit 13532776ca8af93b5254efd1ac3cd4db62bddd6c) 
     
    Bug: 507707838 
    Change-Id: I51d7eb959a8f11077e05b73e86d16d9fae850047 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7808748 
    Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    Commit-Queue: Shrek Shao <shrekshao@google.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1624914} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7874065 
    Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
    Reviewed-by: Shrek Shao <shrekshao@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4913} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough_unittest_buffers.cc`

---

Hash: [316e5d06b649a4abbd02c5718c0963ae18d6c09a](https://chromiumdash.appspot.com/commit/316e5d06b649a4abbd02c5718c0963ae18d6c09a)  

Date: Fri May 29 04:23:08 2026


---

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. Memory corruption in a highly privileged process (e.g. GPU, network processes)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/507707838)*
