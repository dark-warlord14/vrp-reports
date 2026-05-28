# Use-After-Free in MediaStreamDescriptor

| Field | Value |
|-------|-------|
| **Issue ID** | [440737137](https://issues.chromium.org/issues/440737137) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 137.0.0.0 |
| **Reporter** | ss...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2025-08-23 |
| **Bounty** | $10,000.00 |

## Description

# Steps to reproduce the problem

1. chrome.exe --js-flags="--stress-incremental-marking --expose-gc" --no-sandbox

# Problem Description

```
void MediaStreamDescriptor::AddComponent(MediaStreamComponent* component) {
  '''
  '''
  // Iterate over a copy of |observers_| to avoid re-entrancy issues.
  Vector<WebMediaStreamObserver*> observers = observers_;
  for (auto*& observer : observers)
    observer->TrackAdded(WebString(component->Id()));
}

```

  

A vulnerability occurs when the garbage collector runs while maintaining GC objects on the stack using a Vector.\

```
SpaceSplitString::Data* SpaceSplitString::Data::Create(
    const AtomicString& string) {
  auto result = SharedDataMap().insert(string, nullptr);
  SpaceSplitString::Data* data = result.stored_value->value;
  if (result.is_new_entry) {
    data = MakeGarbageCollected<SpaceSplitString::Data>(string);
    result.stored_value->value = data;
  }
  return data;
}
```\
As shown in the asan.log file, the MakeGarbageCollected function can be called from the SpaceSplitString function and several other functions within the TrackAdded function.\
```c++
void CppHeap::ReportBufferedAllocationSizeIfPossible() {
    '''
    '''
    used_size_.fetch_add(static_cast<size_t>(bytes_to_report),
                         std::memory_order_relaxed);
    allocated_size_ += bytes_to_report;

    if (v8_flags.incremental_marking) {
      if (allocated_size_ > allocated_size_limit_for_check_) {
        Heap* heap = isolate_->heap();
        heap->StartIncrementalMarkingIfAllocationLimitIsReached(
            heap->main_thread_local_heap(),
            heap->GCFlagsForIncrementalMarking(),
            kGCCallbackScheduleIdleGarbageCollection);
        if (heap->incremental_marking()->IsMajorMarking()) {
          if (heap->AllocationLimitOvershotByLargeMargin()) {
            heap->FinalizeIncrementalMarkingAtomically(
                i::GarbageCollectionReason::kExternalFinalize);
          } else {
            heap->incremental_marking()->AdvanceOnAllocation();
          }
        }
        allocated_size_limit_for_check_ =
            allocated_size_ + kIncrementalMarkingCheckInterval;
      }
    }
  }
}
```\
If there is a lot of memory allocated so far inside the MakeGarbageCollected function, you can call FinalizeIncrementalMarkingAtomically through the ReportBufferedAllocationSizeIfPossible function to execute Full GarbageCollect.\
The probability of the conditions for executing the above GarbageCollect is very low and can change a lot depending on the version, environment, etc., so the probability can be adjusted by taking actions such as setting the ArrayBuffer allocation size and loop count to different values.

# Summary
Use-After-Free in MediaStreamDescriptor

# Custom Questions
#### Type of crash: 
Renderer

#### Crash state: 
Crash referencing vftable

#### Reporter credit: 
sherkito

# Additional Data
Category: Security \
Chrome Channel: Not sure \
Regression: N/A \

```

## Attachments

- [test0.html](attachments/test0.html) (text/html, 2.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 18.0 KB)
- [poc.html](attachments/poc.html) (text/html, 2.3 KB)
- [pocv2.html](attachments/pocv2.html) (text/html, 2.8 KB)

## Timeline

### ss...@gmail.com (2025-08-24)

# Steps to reproduce the problem

1. chrome.exe --js-flags="--stress-incremental-marking --expose-gc" --no-sandbox
2. button click

# Problem Description

```
void MediaStreamDescriptor::AddComponent(MediaStreamComponent* component) {
  '''
  '''
  // Iterate over a copy of |observers_| to avoid re-entrancy issues.
  Vector<WebMediaStreamObserver*> observers = observers_;
  for (auto*& observer : observers)
    observer->TrackAdded(WebString(component->Id()));
}

```

A vulnerability occurs when the garbage collector runs while maintaining GC objects on the stack using a Vector.

```
SpaceSplitString::Data* SpaceSplitString::Data::Create(
    const AtomicString& string) {
  auto result = SharedDataMap().insert(string, nullptr);
  SpaceSplitString::Data* data = result.stored_value->value;
  if (result.is_new_entry) {
    data = MakeGarbageCollected<SpaceSplitString::Data>(string);
    result.stored_value->value = data;
  }
  return data;
}

```

As you can see in the asan.log file, the MakeGarbageCollected function can be called from multiple places due to the difference in triggering methods within the SpaceSplitString and TrackAdded functions, and I will omit the attachments for other calling locations.

```
void CppHeap::ReportBufferedAllocationSizeIfPossible() {
    '''
    '''
    used_size_.fetch_add(static_cast<size_t>(bytes_to_report),
                         std::memory_order_relaxed);
    allocated_size_ += bytes_to_report;

    if (v8_flags.incremental_marking) {
      if (allocated_size_ > allocated_size_limit_for_check_) {
        Heap* heap = isolate_->heap();
        heap->StartIncrementalMarkingIfAllocationLimitIsReached(
            heap->main_thread_local_heap(),
            heap->GCFlagsForIncrementalMarking(),
            kGCCallbackScheduleIdleGarbageCollection);
        if (heap->incremental_marking()->IsMajorMarking()) {
          if (heap->AllocationLimitOvershotByLargeMargin()) {
            heap->FinalizeIncrementalMarkingAtomically(
                i::GarbageCollectionReason::kExternalFinalize);
          } else {
            heap->incremental_marking()->AdvanceOnAllocation();
          }
        }
        allocated_size_limit_for_check_ =
            allocated_size_ + kIncrementalMarkingCheckInterval;
      }
    }
  }
}

```

If there is a lot of memory allocated so far inside the MakeGarbageCollected function, you can call FinalizeIncrementalMarkingAtomically through the ReportBufferedAllocationSizeIfPossible function to execute Full GarbageCollect.  

The probability of the conditions for executing the above GarbageCollect is very low and can change a lot depending on the version, environment, etc., so the probability can be adjusted by taking actions such as setting the ArrayBuffer allocation size and loop count to different values.  

Add the modified version code related to probability and the commit version.

```
commit version: 06773e4fd40f4b8ad8a3c94a86ff14613b626c8e

```

I'm re-attaching this to the comments because I think the Markdown typo in the above descriptor is making it less readable.

### cl...@appspot.gserviceaccount.com (2025-08-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6541335527882752.

### cl...@appspot.gserviceaccount.com (2025-08-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6256909841530880.

### an...@chromium.org (2025-08-25)

I wasn't able to get clusterfuzz to repro this but forwarding to guidou@ (based on similar triage for <https://issues.chromium.org/40083666>) since the reporter included an ASAN trace. @guidou, if you are not the right assignee, please feel free to re-route as necessary. Thanks!

### ch...@google.com (2025-08-26)

Setting milestone because of s2 severity.

### ch...@google.com (2025-08-26)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ss...@gmail.com (2025-08-27)

I've attached the code I modified after removing the button click issue and confirming that the issue still occurs in ASAN Chromium.

### dx...@google.com (2025-09-04)

Project: chromium/src  

Branch:  main  

Author:  Guido Urdaneta [guidou@chromium.org](mailto:guidou@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6912084>

[MediaStream] Use weak ptrs to track observers in MediaStreamDescriptor

---


Expand for full commit details
```
     
    Prior to this CL, we were using raw pointers. 
    This was problematic for several reasons, including that one of the observer classes is GCed. 
    The GCed case (MediaRecorderHandler) is handled by using composition 
    instead of inheriting directly from the WebMediaStreamObserver interface. 
     
    Bug: 440737137 
    Change-Id: Ibebb8145b3d190b39f04424f4e14cb9020855038 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6912084 
    Reviewed-by: Tony Herre <toprice@chromium.org> 
    Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1510795}

```

---

Files:

- M `third_party/blink/public/platform/modules/mediastream/web_media_stream.h`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.cc`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.h`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl_test.cc`
- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`
- M `third_party/blink/renderer/platform/exported/mediastream/web_media_stream.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.h`

---

Hash: [4e6f77f4984209726c6d33475bc4afb13f0e2955](https://chromiumdash.appspot.com/commit/4e6f77f4984209726c6d33475bc4afb13f0e2955)  

Date: Thu Sep 4 09:43:02 2025


---

### ch...@google.com (2025-09-11)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### gu...@google.com (2025-09-11)

1. Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/6912084

2. Has this fix been verified on Canary to not pose any stability regressions?
No issues so far.

3. Does this fix pose any potential non-verifiable stability risks?
No known risks.

4. Does this fix pose any known compatibility risks?
No.

5. Does it require manual verification by the test team? If so, please describe required testing.
Not required. 

### ts...@google.com (2025-09-11)

Please merge to  M-140 (7339) by EOD Friday and M-141 (7390) 

### sp...@google.com (2025-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
a high quality memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2025-09-11)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  Guido Urdaneta [guidou@chromium.org](mailto:guidou@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6940103>

[MediaStream] Use weak ptrs to track observers in MediaStreamDescriptor

---


Expand for full commit details
```
     
    Prior to this CL, we were using raw pointers. 
    This was problematic for several reasons, including that one of the observer classes is GCed. 
    The GCed case (MediaRecorderHandler) is handled by using composition 
    instead of inheriting directly from the WebMediaStreamObserver interface. 
     
    (cherry picked from commit 4e6f77f4984209726c6d33475bc4afb13f0e2955) 
     
    Bug: 440737137 
    Change-Id: Ibebb8145b3d190b39f04424f4e14cb9020855038 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6912084 
    Reviewed-by: Tony Herre <toprice@chromium.org> 
    Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1510795} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6940103 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7390@{#697} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `third_party/blink/public/platform/modules/mediastream/web_media_stream.h`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.cc`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.h`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl_test.cc`
- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`
- M `third_party/blink/renderer/platform/exported/mediastream/web_media_stream.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.h`

---

Hash: [4b1e10d97a73c99d84dd13ddd802dc81f2065b5d](https://chromiumdash.appspot.com/commit/4b1e10d97a73c99d84dd13ddd802dc81f2065b5d)  

Date: Thu Sep 11 21:55:45 2025


---

### pe...@google.com (2025-09-11)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### gu...@google.com (2025-09-11)

1. Was this issue a regression for the milestone it was found in?
No

2. Is this issue related to a change or feature merged after the latest LTS Milestone
No

### dx...@google.com (2025-09-11)

Project: chromium/src  

Branch:  refs/branch-heads/7339  

Author:  Guido Urdaneta [guidou@chromium.org](mailto:guidou@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6939758>

[M140][MediaStream] Use weak ptrs to track observers in MediaStreamDescriptor

---


Expand for full commit details
```
     
    Prior to this CL, we were using raw pointers. 
    This was problematic for several reasons, including that one of the observer classes is GCed. 
    The GCed case (MediaRecorderHandler) is handled by using composition 
    instead of inheriting directly from the WebMediaStreamObserver interface. 
     
    (cherry picked from commit 4e6f77f4984209726c6d33475bc4afb13f0e2955) 
     
    Bug: 440737137 
    Change-Id: Ibebb8145b3d190b39f04424f4e14cb9020855038 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6912084 
    Reviewed-by: Tony Herre <toprice@chromium.org> 
    Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1510795} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6939758 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7339@{#1891} 
    Cr-Branched-From: 27be8b77710f4405fdfeb4ee946fcabb0f6c92b2-refs/heads/main@{#1496484}

```

---

Files:

- M `third_party/blink/public/platform/modules/mediastream/web_media_stream.h`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.cc`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.h`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl_test.cc`
- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`
- M `third_party/blink/renderer/platform/exported/mediastream/web_media_stream.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.h`

---

Hash: [7f8d86bc1b1c01685e62ef879a91391c0f6fe042](https://chromiumdash.appspot.com/commit/7f8d86bc1b1c01685e62ef879a91391c0f6fe042)  

Date: Thu Sep 11 22:30:08 2025


---

### pe...@google.com (2025-09-15)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-15)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6942295
2. Low - There was no conflict.
3. 140 and 141
4. Yes, this issue has been around for a long time.

### pe...@google.com (2025-09-16)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-09-16)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6939069
2. Medium - There were some conflicts.
3. 140 and 141
4. Yes, this issue has been around M132. But there are some conflicts in the test and MediaStreamDescriptor class, it's still worth to merge the fix to M132. 

### dx...@google.com (2025-09-27)

Project: chromium/src  

Branch:  refs/branch-heads/6834  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://chromium-review.googlesource.com/6939069>

[M132-LTS][MediaStream] Use weak ptrs to track observers in MediaStreamDescriptor

---


Expand for full commit details
```
     
    Prior to this CL, we were using raw pointers. 
    This was problematic for several reasons, including that one of the observer classes is GCed. 
    The GCed case (MediaRecorderHandler) is handled by using composition 
    instead of inheriting directly from the WebMediaStreamObserver interface. 
     
    (cherry picked from commit 4e6f77f4984209726c6d33475bc4afb13f0e2955) 
     
    Bug: 440737137 
    Change-Id: Ibebb8145b3d190b39f04424f4e14cb9020855038 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6912084 
    Reviewed-by: Tony Herre <toprice@chromium.org> 
    Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1510795} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6939069 
    Owners-Override: Michael Ershov <miersh@google.com> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/6834@{#5649} 
    Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `third_party/blink/public/platform/modules/mediastream/web_media_stream.h`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.cc`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.h`
- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`
- M `third_party/blink/renderer/platform/exported/mediastream/web_media_stream.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.h`

---

Hash: [6edf44d54c5a0a0eff489c1047cb993e058e03f6](https://chromiumdash.appspot.com/commit/6edf44d54c5a0a0eff489c1047cb993e058e03f6)  

Date: Sat Sep 27 04:46:54 2025


---

### dx...@google.com (2025-09-27)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Guido Urdaneta [guidou@chromium.org](mailto:guidou@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6942295>

[M138-LTS][MediaStream] Use weak ptrs to track observers in MediaStreamDescriptor

---


Expand for full commit details
```
     
    Prior to this CL, we were using raw pointers. 
    This was problematic for several reasons, including that one of the observer classes is GCed. 
    The GCed case (MediaRecorderHandler) is handled by using composition 
    instead of inheriting directly from the WebMediaStreamObserver interface. 
     
    (cherry picked from commit 4e6f77f4984209726c6d33475bc4afb13f0e2955) 
     
    Bug: 440737137 
    Change-Id: Ibebb8145b3d190b39f04424f4e14cb9020855038 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6912084 
    Reviewed-by: Tony Herre <toprice@chromium.org> 
    Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1510795} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6942295 
    Reviewed-by: Michael Ershov <miersh@google.com> 
    Owners-Override: Michael Ershov <miersh@google.com> 
    Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3418} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/public/platform/modules/mediastream/web_media_stream.h`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.cc`
- M `third_party/blink/renderer/modules/mediarecorder/media_recorder_handler.h`
- M `third_party/blink/renderer/modules/mediastream/media_stream_track_impl_test.cc`
- M `third_party/blink/renderer/modules/mediastream/web_media_player_ms.cc`
- M `third_party/blink/renderer/platform/exported/mediastream/web_media_stream.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.cc`
- M `third_party/blink/renderer/platform/mediastream/media_stream_descriptor.h`

---

Hash: [a0a7f722388642a904dd21fa13ec63f5ed439e3c](https://chromiumdash.appspot.com/commit/a0a7f722388642a904dd21fa13ec63f5ed439e3c)  

Date: Sat Sep 27 04:51:42 2025


---

### ch...@google.com (2025-12-12)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/440737137)*
