# TOCTOU in PersistentHistogramAllocator::GetHistogram

| Field | Value |
|-------|-------|
| **Issue ID** | [378623799](https://issues.chromium.org/issues/378623799) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Metrics |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 131.0.6778.20 |
| **Reporter** | bl...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2024-11-12 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Apply the patch\_renderer.diff with `--ignore-whitespace` argument.
2. Build the release version of Chrome and start it.
3. Open a new tab and visit any URL.
4. Close the tab. If the issue does not trigger, repeat the process of opening a new tab, visiting a URL, and closing the tab.
5. Since ASAN on Windows cannot detect this vulnerability, You can use WinDbg to attach to the broker process and then perform the above operations to capture the exception.

# Problem Description

This vulnerability can be triggered through process such as render, GPU, and utility to cause a crash in the broker processes. The current demonstration shows that in the render process, it requires opening a new page to visit a website and then closing the page to have a chance of triggering it, as this is a TOCTOU bug.

base/metrics/persistent\_histogram\_allocator.cc

```
std::unique_ptr<HistogramBase> PersistentHistogramAllocator::GetHistogram(
    Reference ref) {
  PersistentHistogramData* data =
      memory_allocator_->GetAsObject<PersistentHistogramData>(ref);[1]
  const size_t length = memory_allocator_->GetAllocSize(ref);[2]

  if (!data || data->name[0] == '\0' ||
      reinterpret_cast<char*>(data)[length - 1] != '\0' ||
      data->samples_metadata.id == 0 || data->logged_metadata.id == 0 ||
      (data->logged_metadata.id != data->samples_metadata.id &&
       data->logged_metadata.id != data->samples_metadata.id + 1) ||
      [3]HashMetricName(data->name) != data->samples_metadata.id) {
    return nullptr;
  }
  return CreateHistogram(data);
}

```

When the function reaches point **[1]**, the [subsequently called function](https://source.chromium.org/chromium/chromium/src/+/main:base/metrics/persistent_memory_allocator.cc;drc=a45502c46d75f210c783e07384138379ea1e46e4;l=939) checks whether `block->size` is greater than or equal to `0x68`.If it is, it will return `data`, which is a pointer to shared memory. The value of `data` is `shared_memory_base + [shared_memory_base + 0x3c] + 0x10`. This shared memory is also mapped in other processes, and is categorized based on metrics and types, such as render, GPU, utility, etc.

However, at point **[2]**, when actually obtaining `length`, it only checks whether `block->size` is greater than `0x10`.

Since this operation involves shared memory, there exists a TOCTOU (Time-of-Check to Time-of-Use) bug here.

If a child process modifies the value of `size` between points **[1]** and **[2]**, it can bypass the subsequent check `reinterpret_cast<char*>(data)[length - 1] != '\0'`. This check is used to ensure that `data->name` is a null-terminated string.

Before entering function **[3]**, the code calls `strlen` to get the length of `data->name`. If `data->name` is very long and reaches the end of the shared memory, the `strlen` function will read out-of-bounds into the next heap block to check for a null terminator.

There are three possible scenarios:

1. The beginning of the next memory region happens to be `0`. In this case, the out-of-bounds access does not have much impact.
2. The next memory region is not yet allocated. An out-of-bounds access by `strlen` will cause an exception.
3. The beginning of the next memory region is not `0`. In this case, `strlen` will return a value larger than the actual length of `data->name`.

In the third scenario, at point **[3]**, the code will call `OPENSSL_memcpy(data + n, in, len)`, which will lead to an out-of-bounds read.

HashMetricName(std::string\_view name) --> MD5Sum(as\_byte\_span(name), &digest) --> MD5(data.data(), data.size(), digest->a.data()) --> MD5\_Update --> [crypto\_md32\_update](https://source.chromium.org/chromium/chromium/src/+/main:third_party/boringssl/src/crypto/fipsmodule/digest/md32_common.h;drc=a45502c46d75f210c783e07384138379ea1e46e4;l=127)

For this vulnerability patch, I recommend checking if the `length` is larger 0x68 after obtaining it. The code is as follows:

```
--- a/base/metrics/persistent_histogram_allocator.cc
+++ b/base/metrics/persistent_histogram_allocator.cc
@@ -328,7 +328,7 @@ std::unique_ptr<HistogramBase> PersistentHistogramAllocator::GetHistogram(
   // Check that metadata is reasonable: name is null-terminated and non-empty,
   // ID fields have been loaded with a hash of the name (0 is considered
   // unset/invalid).
-  if (!data || data->name[0] == '\0' ||
+  if (length < 0x58 || !data || data->name[0] == '\0' ||
       reinterpret_cast<char*>(data)[length - 1] != '\0' ||
       data->samples_metadata.id == 0 || data->logged_metadata.id == 0 ||
       // Note: Sparse histograms use |id + 1| in |logged_metadata|.

```
# Additional Comments

Chrome Version: Version 131.0.6778.20 (Developer Build) (64-bit) commit 5b1aa5623a75aec826e1c812228173345a5065c3 (HEAD -> beta, origin/branch-heads/6778)
Operating System: windows10

# Summary

TOCTOU in PersistentHistogramAllocator::GetHistogram

# Custom Questions

#### Type of crash:

browser

#### Crash state:

```
0:010> p
chrome!std::__Cr::__constexpr_strlen [inlined in chrome!base::PersistentHistogramAllocator::GetHistogram+0xad]:
00007ffc`1e43fc3d e8aebb3b09      call    chrome!strlen (00007ffc`277fb7f0)
0:010> db 000001B1AD9300C0
000001b1`ad9300c0  61 61 61 61 61 61 61 61-61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000001b1`ad9300d0  61 61 61 61 61 61 61 61-61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000001b1`ad9300e0  61 61 61 61 61 61 61 61-61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000001b1`ad9300f0  61 61 61 61 61 61 61 61-61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000001b1`ad930100  61 61 61 61 61 61 61 61-61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000001b1`ad930110  61 61 61 61 61 61 61 61-61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000001b1`ad930120  61 61 61 61 61 61 61 61-61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
000001b1`ad930130  61 61 61 61 61 61 61 61-61 61 61 61 61 61 61 61  aaaaaaaaaaaaaaaa
0:010> p
(3300.167c): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome!strlen+0x31:
00007ffc`277fb821 488b10          mov     rdx,qword ptr [rax] ds:000001b1`adb30000=????????????????
0:010> db 000001B1ADB30000
000001b1`adb30000  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
000001b1`adb30010  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
000001b1`adb30020  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
000001b1`adb30030  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
000001b1`adb30040  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
000001b1`adb30050  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
000001b1`adb30060  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
000001b1`adb30070  ?? ?? ?? ?? ?? ?? ?? ??-?? ?? ?? ?? ?? ?? ?? ??  ????????????????
0:010> k
 # Child-SP          RetAddr               Call Site
00 00000036`d25fd0b8 00007ffc`1e43fc42     chrome!strlen+0x31 [C:\chromium\src\out\release\minkernel\crts\ucrt\src\appcrt\string\amd64\strlen.asm @ 70] 
01 (Inline Function) --------`--------     chrome!std::__Cr::__constexpr_strlen+0x5 [C:\chromium\src\third_party\libc++\src\include\__string\constexpr_c_functions.h @ 66] 
02 (Inline Function) --------`--------     chrome!std::__Cr::char_traits<char>::length+0x5 [C:\chromium\src\third_party\libc++\src\include\__string\char_traits.h @ 130] 
03 (Inline Function) --------`--------     chrome!std::__Cr::__char_traits_length_checked+0x5 [C:\chromium\src\third_party\libc++\src\include\string_view @ 269] 
04 (Inline Function) --------`--------     chrome!std::__Cr::basic_string_view<char,std::__Cr::char_traits<char> >::basic_string_view+0xa [C:\chromium\src\third_party\libc++\src\include\string_view @ 347] 
05 00000036`d25fd0c0 00007ffc`1e43fb3d     chrome!base::PersistentHistogramAllocator::GetHistogram+0xb2 [C:\chromium\src\base\metrics\persistent_histogram_allocator.cc @ 340] 
06 00000036`d25fd120 00007ffc`2052ed7b     chrome!base::PersistentHistogramAllocator::Iterator::GetNextWithIgnore+0xed [C:\chromium\src\base\metrics\persistent_histogram_allocator.cc @ 314] 
07 (Inline Function) --------`--------     chrome!base::PersistentHistogramAllocator::Iterator::GetNext+0xb [C:\chromium\src\base\metrics\persistent_histogram_allocator.h @ 198] 
08 00000036`d25fd2c0 00007ffc`16da3e98     chrome!metrics::SubprocessMetricsProvider::MergeHistogramDeltasFromAllocator+0x7b [C:\chromium\src\components\metrics\content\subprocess_metrics_provider.cc @ 268] 
09 00000036`d25fd4d0 00007ffc`1e3dfe32     chrome!base::OnceCallback<void ()>::Run+0x58 [C:\chromium\src\base\functional\callback.h @ 156] 
0a 00000036`d25fd550 00007ffc`1e3e0006     chrome!base::internal::PostTaskAndReplyRelay::RunTaskAndPostReply+0x32 [C:\chromium\src\base\threading\post_task_and_reply_impl.h @ 49] 
0b (Inline Function) --------`--------     chrome!base::internal::DecayedFunctorTraits<void (*)(base::internal::PostTaskAndReplyRelay),base::internal::PostTaskAndReplyRelay &&>::Invoke+0x21 [C:\chromium\src\base\functional\bind_internal.h @ 671] 
0c (Inline Function) --------`--------     chrome!base::internal::InvokeHelper<0,base::internal::FunctorTraits<void (*&&)(base::internal::PostTaskAndReplyRelay),base::internal::PostTaskAndReplyRelay &&>,void,0>::MakeItSo+0x21 [C:\chromium\src\base\functional\bind_internal.h @ 930] 
0d (Inline Function) --------`--------     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(base::internal::PostTaskAndReplyRelay),base::internal::PostTaskAndReplyRelay &&>,base::internal::BindState<0,1,0,void (*)(base::internal::PostTaskAndReplyRelay),base::internal::PostTaskAndReplyRelay>,void ()>::RunImpl+0x21 [C:\chromium\src\base\functional\bind_internal.h @ 1067] 
0e 00000036`d25fd5e0 00007ffc`16da3e98     chrome!base::internal::Invoker<base::internal::FunctorTraits<void (*&&)(base::internal::PostTaskAndReplyRelay),base::internal::PostTaskAndReplyRelay &&>,base::internal::BindState<0,1,0,void (*)(base::internal::PostTaskAndReplyRelay),base::internal::PostTaskAndReplyRelay>,void ()>::RunOnce+0x36 [C:\chromium\src\base\functional\bind_internal.h @ 980] 
0f 00000036`d25fd660 00007ffc`1e3f7194     chrome!base::OnceCallback<void ()>::Run+0x58 [C:\chromium\src\base\functional\callback.h @ 156] 
10 00000036`d25fd6e0 00007ffc`224e2173     chrome!base::TaskAnnotator::RunTaskImpl+0x154 [C:\chromium\src\base\task\common\task_annotator.cc @ 203] 
11 (Inline Function) --------`--------     chrome!base::TaskAnnotator::RunTask+0x54 [C:\chromium\src\base\task\common\task_annotator.h @ 98] 
12 (Inline Function) --------`--------     chrome!base::internal::TaskTracker::RunTaskImpl+0x78 [C:\chromium\src\base\task\thread_pool\task_tracker.cc @ 677] 
13 00000036`d25fd780 00007ffc`224e14b6     chrome!base::internal::TaskTracker::RunBlockShutdown+0xc3 [C:\chromium\src\base\task\thread_pool\task_tracker.cc @ 670] 
14 (Inline Function) --------`--------     chrome!base::internal::TaskTracker::RunTaskWithShutdownBehavior+0x5b [C:\chromium\src\base\task\thread_pool\task_tracker.cc @ 695] 
15 00000036`d25fd840 00007ffc`224e0c91     chrome!base::internal::TaskTracker::RunTask+0x426 [C:\chromium\src\base\task\thread_pool\task_tracker.cc @ 524] 
16 00000036`d25ff1e0 00007ffc`243741cc     chrome!base::internal::TaskTracker::RunAndPopNextTask+0x2d1 [C:\chromium\src\base\task\thread_pool\task_tracker.cc @ 417] 
17 00000036`d25ff490 00007ffc`24373a28     chrome!base::internal::WorkerThread::RunWorker+0x49c [C:\chromium\src\base\task\thread_pool\worker_thread.cc @ 493] 
18 00000036`d25ff730 00007ffc`1e3864a4     chrome!base::internal::WorkerThread::RunBackgroundPooledWorker+0x18 [C:\chromium\src\base\task\thread_pool\worker_thread.cc @ 385] 
19 00000036`d25ff770 00007ffc`8a387374     chrome!base::`anonymous namespace'::ThreadFunc+0x164 [C:\chromium\src\base\threading\platform_thread_win.cc @ 124] 
1a 00000036`d25ff940 00007ffc`8acbcc91     KERNEL32!BaseThreadInitThunk+0x14
1b 00000036`d25ff970 00000000`00000000     ntdll!RtlUserThreadStart+0x21

```
#### Reporter credit:

Xiantong Hou and Pisanbao of Wuheng Lab

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: N/A

## Attachments

- [patch_renderer.diff](attachments/patch_renderer.diff) (text/x-diff, 3.5 KB)

## Timeline

### ch...@chromium.org (2024-11-13)

Thanks for your detailed report.

I tried to apply your patch and reproduce on a Linux asan build, but it always would hit:

`ERROR:persistent_memory_allocator.cc(878)] Corruption detected in shared-memory segment.`

I can try again on Windows later/tomorrow. (I think there may be some differences in how shared memory is handled on Windows.)

Based on your description and analysis, I'm assigning provisional severity as High based on an out-of-bounds read in the browser process requiring a compromised renderer.

asvitkine: Could you please take a look and if possible, provide a comment explaining whether you believe this condition can be achieved in a production version of Chrome? If you can diagnose and fix the issue based on information provided, please proceed accordingly. Please provide a comment about when this issue may have been introduced or which active release branches of Chrome may be impacted.

### [Deleted User] (2024-11-20)

Roger: I'm going to tentatively set the FoundIn to extended stable (under the assumption that this issue has been around for a while), but once you know what the fix looks like, can you comment on whether the issue was introduced more recently than M130?

### pe...@google.com (2024-11-21)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-11-29)

rogerm: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ro...@chromium.org (2024-11-29)

CL in flight
https://chromium-review.googlesource.com/6025612

### ro...@chromium.org (2024-11-29)

This is a long-standing issue, going back to at least M51 (at which point the code was refactored into its current location). I believe it existed well before that. Do you need me to go back further in history?

### ap...@google.com (2024-12-10)

Project: chromium/src  

Branch: main  

Author: Roger McFarlane <[rogerm@chromium.org](mailto:rogerm@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6025612>

Remove PersistentMemoryAllocator::GetAllocSize()

---


Expand for full commit details
```
Remove PersistentMemoryAllocator::GetAllocSize() 
 
This CL removes PersistentMemoryAllocator::GetAllocSize() in favor 
of allowing various other API entry points to return the alloc size. 
This mitigates potential TOCTOU errors where the size of an alloc 
is validated by one API then separately fetched in another call. The 
size could otherwise be manipulated in between initial validation and 
the subsequent fetch. 
 
Bug: 378623799 
Change-Id: I8021cf4c07f1a96172deb2a252326e9ffa525798 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6025612 
Reviewed-by: Alexei Svitkine <asvitkine@chromium.org> 
Commit-Queue: Roger McFarlane <rogerm@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1394492}

```

---

Files:

- M `base/metrics/field_trial.cc`
- M `base/metrics/persistent_histogram_allocator.cc`
- M `base/metrics/persistent_histogram_allocator.h`
- M `base/metrics/persistent_memory_allocator.cc`
- M `base/metrics/persistent_memory_allocator.h`
- M `base/metrics/persistent_memory_allocator_unittest.cc`
- M `components/metrics/persistent_system_profile.cc`

---

Hash: 23479ae0d3332f5525cfd9491137fc6c0ffcb46a  

Date:  Tue Dec 10 20:31:23 2024


---

### th...@chromium.org (2024-12-11)

[secondary shepherd] Thanks for the CL rogerm@. If this issue is resolved, could you please mark it as fixed?

Re [#comment7](https://issues.chromium.org/issues/378623799#comment7): nope, it just matters which active branch it was introduced in. So if it's older than current extended stable M130, we can keep "Found In" at 130.

### ro...@chromium.org (2024-12-11)

Done.

### pe...@google.com (2024-12-12)

Security Merge Request Consideration: Requesting merge to extended stable (M130) because latest trunk commit (1394492) appears to be after extended stable branch point (1356013).
Security Merge Request Consideration: Requesting merge to stable (M131) because latest trunk commit (1394492) appears to be after stable branch point (1368529).
Security Merge Request Consideration: Requesting merge to beta (M132) because latest trunk commit (1394492) appears to be after beta branch point (1381561).
Security Merge Request - Manual Review: Merge review required: M130 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M131 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M132 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [130, 131, 132].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ro...@chromium.org (2024-12-12)

1. Which CLs should be backmerged? (Please include Gerrit links.)
   
   <https://chromium-review.googlesource.com/6025612>
   
   RE: Severity and required merges
   
   - This issue could allow a compromised child process to crash the
     browser with a out-of-bounds read; it would not allow for data
     exfiltration or privilige escalation.
   - I'm not sure that a merge to M121 Stable is required, if this is
     the only fix going into the respin.
   - I would suggest merging to M132 BETA.
   - The fix should be safe to merge to both branches; so I defer to
     the release manager's final decision.
2. Has this fix been verified on Canary to not pose any stability regressions?
   
   In-progress. As of this writing the fix has been landed for under 48 hours.
3. Does this fix pose any potential non-verifiable stability risks?
   
   There are no stability risks anticipated.
4. Does this fix pose any known compatibility risks?
   
   There are no known compatibility risks.
5. Does it require manual verification by the test team? If so, please describe required testing.
   
   No.
   
   Per review of the code, the issue has been fixed. That said, it might be helpful to ask
   the original reporter to validate that they also can non longer reproduce. In testing the
   fix, I haven't seen any repros of the crash. However, in testing without the fix, the
   repro steps did not reliably produce the crash in our dev environment.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!
   
   All except for iOS

### am...@chromium.org (2024-12-16)

merge to M132 approved for https://crrev.com/c/6025612
Security fixes go through security merge approval rather than release managers. From a security perspective, and especially given that we're about to go into holiday release freeze, I concur with not merging to Stable and Extended Stable. 
Looking at canary and dev data, I don't see any issue with this fix, please merge to branch 6834 at your earliest convenience so that this fix can be included in this week's M132 Beta update before release freeze starting on Friday, 20 December.

### ro...@chromium.org (2024-12-17)

Merge is in-flight

- <https://chromium-review.googlesource.com/c/chromium/src/+/6098919>

### ap...@google.com (2024-12-17)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Roger McFarlane <[rogerm@chromium.org](mailto:rogerm@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6098919>

Remove PersistentMemoryAllocator::GetAllocSize()

---


Expand for full commit details
```
Remove PersistentMemoryAllocator::GetAllocSize() 
 
This CL removes PersistentMemoryAllocator::GetAllocSize() in favor 
of allowing various other API entry points to return the alloc size. 
This mitigates potential TOCTOU errors where the size of an alloc 
is validated by one API then separately fetched in another call. The 
size could otherwise be manipulated in between initial validation and 
the subsequent fetch. 
 
(cherry picked from commit 23479ae0d3332f5525cfd9491137fc6c0ffcb46a) 
 
Bug: 378623799 
Change-Id: I8021cf4c07f1a96172deb2a252326e9ffa525798 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6025612 
Reviewed-by: Alexei Svitkine <asvitkine@chromium.org> 
Commit-Queue: Roger McFarlane <rogerm@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1394492} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6098919 
Auto-Submit: Roger McFarlane <rogerm@chromium.org> 
Commit-Queue: Luc Nguyen <lucnguyen@google.com> 
Reviewed-by: Luc Nguyen <lucnguyen@google.com> 
Cr-Commit-Position: refs/branch-heads/6834@{#2335} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `base/metrics/field_trial.cc`
- M `base/metrics/persistent_histogram_allocator.cc`
- M `base/metrics/persistent_histogram_allocator.h`
- M `base/metrics/persistent_memory_allocator.cc`
- M `base/metrics/persistent_memory_allocator.h`
- M `base/metrics/persistent_memory_allocator_unittest.cc`
- M `components/metrics/persistent_system_profile.cc`

---

Hash: 35f86d6a0a03295e4da9dff23eddfe4032350db3  

Date:  Tue Dec 17 12:20:05 2024


---

### pe...@google.com (2024-12-17)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2024-12-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-12-18)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6096434
2. Medium - There were 2 conflicts.
3. 132
4. Yes. According to comment #7, this issue has been around for a long time.


### gm...@google.com (2024-12-18)

Delaying approval until 132 goes out in stable channel.

### sp...@google.com (2024-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
highly mitigated security bug in a non-sandboxed process, mitigated by race and access to a primitive that does not provide attacker utility in a way likely to result in user harm


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-12-19)

Congratulations! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2025-01-02)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### pe...@google.com (2025-01-02)

rogerm: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2025-01-28)

Project: chromium/src  

Branch: refs/branch-heads/6478  

Author: Gyuyoung Kim <[qkim@google.com](mailto:qkim@google.com)>  

Link:      <https://chromium-review.googlesource.com/6096434>

[M126-LTS] Remove PersistentMemoryAllocator::GetAllocSize()

---


Expand for full commit details
```
[M126-LTS] Remove PersistentMemoryAllocator::GetAllocSize() 
 
This CL removes PersistentMemoryAllocator::GetAllocSize() in favor 
of allowing various other API entry points to return the alloc size. 
This mitigates potential TOCTOU errors where the size of an alloc 
is validated by one API then separately fetched in another call. The 
size could otherwise be manipulated in between initial validation and 
the subsequent fetch. 
 
(cherry picked from commit 23479ae0d3332f5525cfd9491137fc6c0ffcb46a) 
 
Bug: 378623799 
Change-Id: I8021cf4c07f1a96172deb2a252326e9ffa525798 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6025612 
Reviewed-by: Alexei Svitkine <asvitkine@chromium.org> 
Commit-Queue: Roger McFarlane <rogerm@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1394492} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6096434 
Reviewed-by: Fahad Mansoor <fahadmansoor@google.com> 
Commit-Queue: Alexei Svitkine <asvitkine@chromium.org> 
Reviewed-by: Roger McFarlane <rogerm@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6478@{#2023} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `base/metrics/field_trial.cc`
- M `base/metrics/persistent_histogram_allocator.cc`
- M `base/metrics/persistent_histogram_allocator.h`
- M `base/metrics/persistent_memory_allocator.cc`
- M `base/metrics/persistent_memory_allocator.h`
- M `base/metrics/persistent_memory_allocator_unittest.cc`
- M `components/metrics/persistent_system_profile.cc`

---

Hash: 11e21b28672aeccd6a45712b0539ca6e104ff48a  

Date:  Tue Jan 28 08:34:44 2025


---

### ch...@google.com (2025-04-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/378623799)*
