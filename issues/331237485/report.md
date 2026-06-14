# OOB Access in mojo SkBitmap StructTraits

| Field | Value |
|-------|-------|
| **Issue ID** | [331237485](https://issues.chromium.org/issues/331237485) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Services>Viz |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | vu...@darknavy.com |
| **Assignee** | ky...@chromium.org |
| **Created** | 2024-03-26 |
| **Bounty** | $21,000.00 |

## Description

### VULNERABILITY DETAILS

When the browser process receives a mojo param containing BitmapInSharedMemory [0], it will call a handwritten deserialization function `StructTraits<viz::mojom::BitmapInSharedMemoryDataView, SkBitmap>::Read` [1]

```
  if (!sk_bitmap->installPixels(image_info, mapping_ptr->memory(),
                                data.row_bytes(), &DeleteSharedMemoryMapping,
                                mapping_ptr.get())) {

```

The shared memory is used as the actual data of the bitmap by calling `sk_bitmap->installPixels`. However, only the data pointer of the shared memory is passed into the function at this point, and the size of the shared memory is ignored. The image size stored in `image_info` may not be consistent with the memory size contained in `mapping_ptr`. Therefore, when the image sizes in `image_info` is larger than the actual size of the shared memory, an out-of-bounds memory issue will occur here.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:services/viz/public/mojom/compositing/bitmap_in_shared_memory.mojom;drc=098756533733ea50b2dcb1c40d9a9e18d49febbe;l=14>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:services/viz/public/cpp/compositing/bitmap_in_shared_memory_mojom_traits.cc;drc=098756533733ea50b2dcb1c40d9a9e18d49febbe;l=108>

### BISECT

Introduced by <https://chromium.googlesource.com/chromium/src/+/cfa7e4010dd5eafaf1e37853262ccf8af407fa61>
which is the first commit of `BitmapInSharedMemory` mojo traits.

### VERSION

Chrome Version: stable
Operating System: All

### REPRODUCTION CASE

1. Apply the poc.diff and rebuild.
2. Repeatedly opening new tabs will constantly trigger the vulnerable code.

Note:

- We did not investigate which operations would trigger the sending of this structure. We found that opening a new tab would trigger it, so used this hastily.
- Since the OOB occurs in shared memory, what the subsequent memory is and how large it is depends on the situation and can vary greatly under different OSes and environments.

### CRASH INFORMATION

Type of crash: browser
Crash log:

```
[479959:480050:0325/193946.058039:ERROR:bitmap_in_shared_memory_mojom_traits.cc(40)] In process: gpu-process
[479959:480050:0325/193946.058418:ERROR:bitmap_in_shared_memory_mojom_traits.cc(66)] Set bad shared memory size from 623616 to 4096
[0325/193946.084987:ERROR:elf_dynamic_array_reader.h(64)] tag not found
Received signal 11 SEGV_MAPERR 75a2c9707000
#0 0x5f1cd3123782 base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1039:7]
#1 0x5f1cd3111442 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:229:20]
#2 0x5f1cd31231a1 base::debug::(anonymous namespace)::StackDumpSignalHandler() [../../base/debug/stack_trace_posix.cc:457:3]
#3 0x75a2d8c42520 (/usr/lib/x86_64-linux-gnu/libc.so.6+0x4251f)
#4 0x5f1cd3ae4c59 (/root/chromium/src/out/debug/chrome+0x9276c58)
  r8: 0000000000000001  r9: 00005f1cd3ae4b60 r10: 0000000000000180 r11: 000075a2cd1edac8
 r12: 00001d1c04968110 r13: 0000000000000000 r14: 0000000000000001 r15: 0000000000000008
  di: 00001d1c04c230a0  si: 000075a2c9707000  bp: 000075a2cd1ed860  bx: 00001d1c056a6c60
  dx: 00001d1c056a6fa0  ax: 0000000000000001  cx: 0000000000000080  sp: 000075a2cd1ed708
  ip: 00005f1cd3ae4c59 efl: 0000000000010206 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 000075a2c9707000
[end of stack trace]

```
### CREDIT INFORMATION

Reporter credit: DARKNAVY

## Attachments

- [poc.diff](attachments/poc.diff) (text/x-diff, 1.4 KB)

## Timeline

### pa...@chromium.org (2024-03-26)

[security shepherd] Thanks for this report.

I have been investigating the code that you are referring to, but it seems to me that it is the patch that is actually creating this this issue. For instance, we are not supposed to have a size that isn't enough to contain the image, so I cannot see how "The image size stored in image\_info may not be consistent with the memory size contained in mapping\_ptr" is possible. Would you have a PoC that triggers this without the patch?

### vu...@darknavy.com (2024-03-26)

To clarify: the scenario here is that we assume the GPU process is under the attacker's control, so the GPU process can send malformed mojo data to the browser process. A similar issue can be found here: <https://issues.chromium.org/issues/40063362> . The difference is that in the previous issue, it's the renderer process that's causing trouble.

### pe...@google.com (2024-03-26)

Thank you for providing more feedback. Adding the requester to the CC list.

### pa...@chromium.org (2024-03-26)

[security shepherd] This seems legit to me. If `byte_size` can be attacker controlled, we seem to be indeed missing some validation on the browser process side. Given inputs from adetaylor@, setting S1 and assigning to kylechar@.

### ky...@chromium.org (2024-03-26)

Yes, I agree this is a real issue. The traits verify that `data.row_bytes` is long enough for `image_info` minimum row\_bytes but doesn't do the same for `mapping_ptr->size()`.

### pe...@google.com (2024-03-26)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-03-26)

Project: chromium/src
Branch: main

commit 1a19ff70bd54847d818566bd7a1e7c384c419746
Author: kylechar <kylechar@chromium.org>
Date:   Tue Mar 26 17:24:40 2024

    Validate buffer length
    
    The BitmapInSharedMemory mojo traits were only validating row length and
    not total buffer length.
    
    Bug: 331237485
    Change-Id: Ia2318899c44e9e7ac72fc7183954e6ce2c702179
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5396796
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
    Reviewed-by: danakj <danakj@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1278417}

M       services/viz/public/cpp/compositing/bitmap_in_shared_memory_mojom_traits.cc

https://chromium-review.googlesource.com/5396796


### pe...@google.com (2024-03-26)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### pe...@google.com (2024-03-27)

The Found In field may only contain numeric values.
Some values couldn't be corrected but were removed, please verify that any important data wasn't lost.
You can see the changes by toggling full history on the issue.

### pe...@google.com (2024-03-27)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

### pe...@google.com (2024-03-28)

Requesting merge to extended stable (M122) because latest trunk commit (1278417) appears to be after extended stable branch point (1250580).
Requesting merge to stable (M123) because latest trunk commit (1278417) appears to be after stable branch point (1262506).
Requesting merge to beta (M124) because latest trunk commit (1278417) appears to be after beta branch point (1274542).
Merge review required: M122 is already shipping to stable.


Merge review required: M123 is already shipping to stable.


Merge review required: M124 is already shipping to beta.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [122, 123, 124].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ky...@chromium.org (2024-04-02)

1. <https://crrev.com/c/5396796>
2. Yes.
3. No.
4. No.
5. No.

### go...@google.com (2024-04-03)

Please apply the appropriate OSs label.

### am...@chromium.org (2024-04-03)

<https://crrev.com/c/5396796> approved for merge M124 beta/ branch 6367 and M123 Stable/ branch 6312
There are no further planned releases of M122 Extended Stable
Please merge to the respective branches by EOD tomorrow / Thursday, so this fix can be included in the next M123 Stable update and impending M124 Stable cut -- thank you

### ap...@google.com (2024-04-04)

Project: chromium/src
Branch: refs/branch-heads/6367

commit 8dc9843f379fae7fb72db73cb3cd603d2d9fe8ac
Author: kylechar <kylechar@chromium.org>
Date:   Thu Apr 04 13:24:44 2024

    Validate buffer length
    
    The BitmapInSharedMemory mojo traits were only validating row length and
    not total buffer length.
    
    (cherry picked from commit 1a19ff70bd54847d818566bd7a1e7c384c419746)
    
    Bug: 331237485
    Change-Id: Ia2318899c44e9e7ac72fc7183954e6ce2c702179
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5396796
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
    Reviewed-by: danakj <danakj@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1278417}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5421550
    Commit-Queue: danakj <danakj@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6367@{#547}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       services/viz/public/cpp/compositing/bitmap_in_shared_memory_mojom_traits.cc

https://chromium-review.googlesource.com/5421550


### ap...@google.com (2024-04-04)

Project: chromium/src
Branch: refs/branch-heads/6312

commit f15315f1cb7897e208947a40d538aac693283d7f
Author: kylechar <kylechar@chromium.org>
Date:   Thu Apr 04 13:24:06 2024

    Validate buffer length
    
    The BitmapInSharedMemory mojo traits were only validating row length and
    not total buffer length.
    
    (cherry picked from commit 1a19ff70bd54847d818566bd7a1e7c384c419746)
    
    Bug: 331237485
    Change-Id: Ia2318899c44e9e7ac72fc7183954e6ce2c702179
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5396796
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
    Reviewed-by: danakj <danakj@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1278417}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5420432
    Commit-Queue: danakj <danakj@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6312@{#786}
    Cr-Branched-From: 6711dcdae48edaf98cbc6964f90fac85b7d9986e-refs/heads/main@{#1262506}

M       services/viz/public/cpp/compositing/bitmap_in_shared_memory_mojom_traits.cc

https://chromium-review.googlesource.com/5420432


### ap...@google.com (2024-04-04)

Project: chromium/src
Branch: refs/branch-heads/6367

commit 8dc9843f379fae7fb72db73cb3cd603d2d9fe8ac
Author: kylechar <kylechar@chromium.org>
Date:   Thu Apr 04 13:24:44 2024

    Validate buffer length
    
    The BitmapInSharedMemory mojo traits were only validating row length and
    not total buffer length.
    
    (cherry picked from commit 1a19ff70bd54847d818566bd7a1e7c384c419746)
    
    Bug: 331237485
    Change-Id: Ia2318899c44e9e7ac72fc7183954e6ce2c702179
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5396796
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
    Reviewed-by: danakj <danakj@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1278417}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5421550
    Commit-Queue: danakj <danakj@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6367@{#547}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       services/viz/public/cpp/compositing/bitmap_in_shared_memory_mojom_traits.cc

https://chromium-review.googlesource.com/5421550


### pe...@google.com (2024-04-04)

LTS Milestone M120

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



### am...@google.com (2024-04-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-04-04)

Congratulations DarkNavy! The Chrome VRP Panel has decided to award you $20,000 for this report of OOB write that could potentially result in a sandbox escape with the precondition of a compromised GPU process + $1,000 bisect bonus.
Had you been able to provide a POC and/or demonstrate an arbitrary write or attacker control outside of the sandbox, we would have assessed this for a potentially considerably higher reward. Thank you for your efforts in discovering and reporting this issue to use -- nice work.

### pe...@google.com (2024-04-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### vo...@google.com (2024-04-08)

1. One <https://crrev.com/c/5433678>
2. Low - simple change, no conflicts
3. M123, M124
4. Yes

### ap...@google.com (2024-04-09)

Project: chromium/src
Branch: refs/branch-heads/6099

commit 1b1f34234346db1df8751e51c7a26c533b308fb4
Author: kylechar <kylechar@chromium.org>
Date:   Tue Apr 09 17:14:26 2024

    [M120-LTS] Validate buffer length
    
    The BitmapInSharedMemory mojo traits were only validating row length and
    not total buffer length.
    
    (cherry picked from commit 1a19ff70bd54847d818566bd7a1e7c384c419746)
    
    (cherry picked from commit f15315f1cb7897e208947a40d538aac693283d7f)
    
    Bug: 331237485
    Change-Id: Ia2318899c44e9e7ac72fc7183954e6ce2c702179
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5396796
    Commit-Queue: Kyle Charbonneau <kylechar@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1278417}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5420432
    Commit-Queue: danakj <danakj@chromium.org>
    Cr-Original-Commit-Position: refs/branch-heads/6312@{#786}
    Cr-Original-Branched-From: 6711dcdae48edaf98cbc6964f90fac85b7d9986e-refs/heads/main@{#1262506}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5433678
    Reviewed-by: danakj <danakj@chromium.org>
    Reviewed-by: Kyle Charbonneau <kylechar@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#2003}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       services/viz/public/cpp/compositing/bitmap_in_shared_memory_mojom_traits.cc

https://chromium-review.googlesource.com/5433678


### pe...@google.com (2024-07-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/331237485)*
