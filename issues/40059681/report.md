# Security: Use-after-free in WebGPU

| Field | Value |
|-------|-------|
| **Issue ID** | [40059681](https://issues.chromium.org/issues/40059681) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2017-15399 |
| **Reporter** | da...@davidmanouchehri.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2022-05-16 |
| **Bounty** | $10,000.00 |

## Description

Reserved.

## Attachments

- [index.js](attachments/index.js) (text/plain, 1.9 KB)

## Timeline

### da...@davidmanouchehri.com (2022-05-16)

VULNERABILITY DETAILS
If GPUMappedDOMArrayBuffer::DetachContents is attempted on a buffer that cannot be detached, WebGPU releases the handle anyway and causes a UAF. This is a variant of https://crbug.com/chromium/776677 and https://crbug.com/chromium/1040325. 


bool DetachContents(v8::Isolate* isolate) {
    // Detach the array buffer by transferring the contents out and dropping
    // them.
    ArrayBufferContents contents;
    return DOMArrayBuffer::Transfer(isolate, contents); // <--- This doesn't actually detach non-detachable buffers
}
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webgpu/gpu_buffer.cc;l=103-108;drc=a086cb36eac298b4c94ed557a772d50e81f5b800;bpv=1;bpt=1


bool DOMArrayBuffer::Transfer(v8::Isolate* isolate,
                              ArrayBufferContents& result) {
  DOMArrayBuffer* to_transfer = this;
  if (!IsDetachable(isolate)) {
    to_transfer = DOMArrayBuffer::Create(Content()->Data(), ByteLength()); // <--- This doesn't detach anything
  }

  return to_transfer->TransferDetachable(isolate, result);
}
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/typed_arrays/dom_array_buffer.cc;l=70-78;drc=a086cb36eac298b4c94ed557a772d50e81f5b800



VERSION
Chrome Version: 101.0.4951.64 + dev
Operating System: All (I think)

REPRODUCTION CASE
See attached. For us Linux users, you'll need to run with this flag:

--enable-features=Vulkan,UseSkiaRenderer

This gives us exactly the same primitive as CVE-2017-15399 (two different ABs looking into the same backing_store). The linearly allocated backing_store nicely bypasses any need for brute forcing ASLR as seen below:

DebugPrint: 0x7d9b0064d9d9: [JSArrayBuffer] <------------------------------- This is AB #1
 - map: 0x7d9b0024d439 <Map(HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x7d9b005b691d <Object map = 0x7d9b002458f1>
 - elements: 0x7d9b00002269 <FixedArray[0]> [HOLEY_ELEMENTS]
 - embedder fields: 2
 - backing_store: 0x7f73578fd000 <------------------------------------ UAF, backing_store is reused
 - byte_length: 4096
 - max_byte_length: 4096
 - properties: 0x7d9b0064dab9 <PropertyArray[3]>
 - All own properties (excluding elements): {
    0x7d9b00005b61 <Symbol: (array_buffer_wasm_memory_symbol)>: 0x7d9b002176d9 <Memory map = 0x7d9b0024c999> (const data field 0), location: properties[0]
 }
 - embedder fields = {
    276830848, aligned pointer: 0x55c521003500
    1910648, aligned pointer: 0x7ea3003a4ef0
 }
...
DebugPrint: 0x7d9b0064e311: [JSArrayBuffer]<------------------------------- This is AB #2
 - map: 0x7d9b002458c9 <Map(HOLEY_ELEMENTS)> [FastProperties]
 - prototype: 0x7d9b005b691d <Object map = 0x7d9b002458f1>
 - elements: 0x7d9b00002269 <FixedArray[0]> [HOLEY_ELEMENTS]
 - embedder fields: 2
 - backing_store: 0x7f73578fd000 <------------------------------------ UAF, backing_store is reused
 - byte_length: 4096
 - max_byte_length: 4096
 - detachable
 - properties: 0x7d9b00002269 <FixedArray[0]>
 - All own properties (excluding elements): {}
 - embedder fields = {
    276830848, aligned pointer: 0x55c521003500
    1911968, aligned pointer: 0x7ea3003a5940
 }


CREDIT INFORMATION
Reporter credit: David Manouchehri

### da...@davidmanouchehri.com (2022-05-16)

PoC attached.

### [Deleted User] (2022-05-16)

[Empty comment from Monorail migration]

### da...@davidmanouchehri.com (2022-05-17)

[Comment Deleted]

### ke...@chromium.org (2022-05-17)

Thank you for the report and the analysis.

enga@: This security issue appears to be a regression from r976959. PTAL?

[Monorail components: Blink>WebGPU]

### [Deleted User] (2022-05-17)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-05-17)

I didn't know array buffers could be made non-detachable by doing this.
I'll add a CHECK for now to crash the renderer process to avoid exposing this use-after-free - until we figure out how to mitigate.

### en...@chromium.org (2022-05-17)

ajgo@ see https://crbug.com/chromium/1326210#c7 - is this a workable mitigation for now?

### aj...@chromium.org (2022-05-17)

It sounds like the issue is in the renderer so yes crashing in the renderer will be a good workaround pending a complete fix.

### da...@davidmanouchehri.com (2022-05-17)

[Comment Deleted]

### en...@chromium.org (2022-05-17)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-05-17)

ulan@ - it looks like using the array buffer to create an asm.js module is causing it to become not detachable.
V8 turns it into a WasmMemoryObject and sets is_asmjs_module to true, and is_detachable to false.
This seems different from actual WASM modules which *do* have detachable memories since they can grow their backing heap.

Why must this asm.js memory not be detached? Could we make it detchable, or could we make it so that asm.js module creation fails if it points to a GPUBuffer-backed ArrayBuffer?

We would really like it so that we are always able to detach mapped memory backing the GPUBuffer. Not being able to detach will lead to complexity in our shared memory allocators if we can't reliably revoke access to the memory. And, eventually it will prevent us from making optimizations which would allow this memory to be directly visible to the GPU. If we can't revoke access, then JavaScript can create tons of races with the privileged GPU process.


### gi...@appspot.gserviceaccount.com (2022-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/15ddcb7754327abd7bf26a714fa6c39cfdde87c0

commit 15ddcb7754327abd7bf26a714fa6c39cfdde87c0
Author: Austin Eng <enga@chromium.org>
Date: Tue May 17 22:20:37 2022

CHECK that detaching a mapped GPUBuffer was successful

Some ArrayBuffers are not detachable meaning failure to detach can
result in JavaScript being able to create array buffers pointing to the same memory.
Add a CHECK to crash the page to prevent this use-after-free until we
figure out a better mitigation.

Bug: 1326210
Change-Id: Ie3c559049693cda0d7813eb48fa8c15f205eaf2a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3652474
Commit-Queue: Austin Eng <enga@chromium.org>
Reviewed-by: Alex Gough <ajgo@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1004483}

[modify] https://crrev.com/15ddcb7754327abd7bf26a714fa6c39cfdde87c0/third_party/blink/renderer/modules/webgpu/gpu_buffer.cc


### en...@chromium.org (2022-05-17)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-05-17)

Closing for tracking purposes - will open a new bug to discuss+track a more permanent fix.

### en...@chromium.org (2022-05-17)

[Empty comment from Monorail migration]

### da...@davidmanouchehri.com (2022-05-17)

[Comment Deleted]

### dc...@chromium.org (2022-05-17)

> (I know the WebGPU team already knows this, this comment is mostly for the security teams who might not be as familiar with what has already shipped.)

If we're not sure, we generally talk with the feature team in question to make sure the scope is well understood :) Nonetheless, thanks for the additional context.

### [Deleted User] (2022-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-18)

[Empty comment from Monorail migration]

### en...@chromium.org (2022-05-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-23)

Merge approved: your change passed merge requirements and is auto-approved for M103. Please go ahead and merge the CL to branch 5060 (refs/branch-heads/5060) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-23)

Merge review required: M102 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-23)

Merge review required: M101 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-23)

Merge review required: M100 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2022-05-23)

Re https://crbug.com/chromium/1326210#c24, https://crbug.com/chromium/1326210#c25, https://crbug.com/chromium/1326210#c26

1. Why does your merge fit within the merge criteria for these milestones?
Yes, it has high security severity.

2. What changes specifically would you like to merge? Please link to Gerrit.
 https://chromium-review.googlesource.com/c/chromium/src/+/3652474

3. Have the changes been released and tested on canary?
Not yet since it just landed. Status here: https://chromiumdash.appspot.com/commit/15ddcb7754327abd7bf26a714fa6c39cfdde87c0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
Not a new feature

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
Should not require manual testing.


### en...@chromium.org (2022-05-23)

sorry - amend (3) - it has been released on canary for a few days now

### en...@chromium.org (2022-05-23)

Does not need to be merged to M100. The issue was introduced in M101 https://chromiumdash.appspot.com/commit/68365a9dc0a62413d5f2c2a96f926ef540ee6ee2

### gi...@appspot.gserviceaccount.com (2022-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a6a90a050b8194525de0ae6ca1363de10b03f091

commit a6a90a050b8194525de0ae6ca1363de10b03f091
Author: Austin Eng <enga@chromium.org>
Date: Mon May 23 19:53:30 2022

CHECK that detaching a mapped GPUBuffer was successful

Some ArrayBuffers are not detachable meaning failure to detach can
result in JavaScript being able to create array buffers pointing to the same memory.
Add a CHECK to crash the page to prevent this use-after-free until we
figure out a better mitigation.

Bug: 1326210
Change-Id: Ie3c559049693cda0d7813eb48fa8c15f205eaf2a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3651746
Reviewed-by: Kai Ninomiya <kainino@chromium.org>
Commit-Queue: Austin Eng <enga@chromium.org>
Cr-Commit-Position: refs/branch-heads/5060@{#193}
Cr-Branched-From: b83393d0f4038aeaf67f970a024d8101df7348d1-refs/heads/main@{#1002911}

[modify] https://crrev.com/a6a90a050b8194525de0ae6ca1363de10b03f091/third_party/blink/renderer/modules/webgpu/gpu_buffer.cc


### [Deleted User] (2022-05-23)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2022-05-23)

Does not need to be merged to M96 per comment above:

> Does not need to be merged to M100. The issue was introduced in M101 https://chromiumdash.appspot.com/commit/68365a9dc0a62413d5f2c2a96f926ef540ee6ee2


### rz...@google.com (2022-05-25)

Thanks kainino@, labelling as not applicable.

### am...@chromium.org (2022-05-31)

m102 merge approved, please merge this fix to branch 5005 at your earliest convenience so this fix can be included in next week's M102 security refresh 

### gi...@appspot.gserviceaccount.com (2022-06-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9cae1b9b33b10b9b1d661cb291efe5df7ef905e2

commit 9cae1b9b33b10b9b1d661cb291efe5df7ef905e2
Author: Austin Eng <enga@chromium.org>
Date: Wed Jun 01 01:23:55 2022

CHECK that detaching a mapped GPUBuffer was successful

Some ArrayBuffers are not detachable meaning failure to detach can
result in JavaScript being able to create array buffers pointing to the same memory.
Add a CHECK to crash the page to prevent this use-after-free until we
figure out a better mitigation.

Bug: 1326210
Change-Id: Ie3c559049693cda0d7813eb48fa8c15f205eaf2a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3652689
Reviewed-by: Kai Ninomiya <kainino@chromium.org>
Commit-Queue: Austin Eng <enga@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#1076}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/9cae1b9b33b10b9b1d661cb291efe5df7ef905e2/third_party/blink/renderer/modules/webgpu/gpu_buffer.cc


### am...@google.com (2022-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-01)

Congratulations, David! The VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts in reporting this issue to us and great work! 

### am...@google.com (2022-06-05)

[Empty comment from Monorail migration]

### ad...@google.com (2022-06-06)

[Empty comment from Monorail migration]

### ad...@google.com (2022-06-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-06-15)

[Empty comment from Monorail migration]

### aj...@chromium.org (2022-06-20)

reporter: I intend to make the report and poc available again - is there a strong reason for keeping it hidden? It is our policy that bug reports are public.

### da...@davidmanouchehri.com (2022-06-20)

[Comment Deleted]

### aj...@chromium.org (2022-06-20)

Thanks - I'll leave it hidden for now.

### am...@google.com (2022-07-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1326210?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1326691]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059681)*
