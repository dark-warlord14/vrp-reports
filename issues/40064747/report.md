# Security: Heap Buffer Overflow and Security DCHECK failed: IsA<Derived>(from) in MediaStreamTrackImpl::stopTrack

| Field | Value |
|-------|-------|
| **Issue ID** | [40064747](https://issues.chromium.org/issues/40064747) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2023-05-23 |
| **Bounty** | $10,000.00 |

## Description

## Bitset and Test version

TestOn: Version 115.0.5788.0 (Developer Build) (64-bit)

Based on the analysis with bitset, it was determined that the vulnerability was introduced by this commit: https://chromium.googlesource.com/chromium/src/+/3da6e612d7b1ab789f018db887334391a47504de

## RCA

Due to an unsafe conversion from `blink::ExecutionContext` to `blink::LocalDOMWindow` in the `stopTrack` [0] function, a heap overflow occurs when attempting to find `UserMediaClient::kSupplementName`.

In the ASAN release version, this issue triggers a SECURITY DCHECK directly. However, after commenting it out, the heap overflow can be observed. Please refer to the attached video for a demonstration of the issue.

```
void MediaStreamTrackImpl::stopTrack(ExecutionContext* execution_context) {
  ...
  UserMediaClient* user_media_client =
      UserMediaClient::From(To<LocalDOMWindow>(execution_context));
  ...
}

template <typename Derived, typename Base>
Derived& To(Base& from) {
  SECURITY_DCHECK(IsA<Derived>(from));
  return static_cast<Derived&>(from);
}
template <typename Derived, typename Base>
Derived* To(Base* from) {
  return from ? &To<Derived>(*from) : nullptr;
}

UserMediaClient* UserMediaClient::From(LocalDOMWindow* window) {
	...
  auto* client = Supplement<LocalDOMWindow>::From<UserMediaClient>(window);

template <typename SupplementType>
  static SupplementType* From(const Supplementable<T>& supplementable) {
    return supplementable.template RequireSupplement<SupplementType>();
  }

template <typename SupplementType>
  SupplementType* RequireSupplement() const {
		...
    const auto it = this->supplements_.find(SupplementType::kSupplementName);
    ...
  }
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/media_stream_track_impl.cc;l=429

## Reproduce
Download Asan Release Chromium: `wget https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1147620.zip?generation=1684811282171770&alt=media`

Run: `/tmp/asan-linux-release-1147620/chrome --incognito --enable-blink-features=VideoTrackGeneratorInWorker,VideoTrackGenerator poc.html`

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 199 B)
- [security_dcheck.log](attachments/security_dcheck.log) (text/plain, 7.1 KB)
- [heap_buffer_overflow.log](attachments/heap_buffer_overflow.log) (text/plain, 29.2 KB)
- [reproduce.mp4](attachments/reproduce.mp4) (video/mp4, 3.5 MB)
- deleted (application/octet-stream, 0 B)
- [heap_buffer_overflow.log](attachments/heap_buffer_overflow.log) (text/plain, 29.2 KB)
- [security_dcheck.log](attachments/security_dcheck.log) (text/plain, 7.1 KB)
- [poc.html](attachments/poc.html) (text/plain, 199 B)

## Timeline

### [Deleted User] (2023-05-23)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-05-23)

## Bitset and Test version

TestOn: Version 115.0.5788.0 (Developer Build) (64-bit)

Based on the analysis with bitset, it was determined that the vulnerability was introduced by this commit: https://chromium.googlesource.com/chromium/src/+/3da6e612d7b1ab789f018db887334391a47504de

## RCA

Due to an unsafe conversion from `blink::ExecutionContext` to `blink::LocalDOMWindow` in the `stopTrack` [0] function, a heap overflow occurs when attempting to find `UserMediaClient::kSupplementName`.

In the ASAN release version, this issue triggers a SECURITY DCHECK directly. However, after commenting it out, the heap overflow can be observed. Please refer to the attached video for a demonstration of the issue.

```
void MediaStreamTrackImpl::stopTrack(ExecutionContext* execution_context) {
  ...
  UserMediaClient* user_media_client =
      UserMediaClient::From(To<LocalDOMWindow>(execution_context));
  ...
}

template <typename Derived, typename Base>
Derived& To(Base& from) {
  SECURITY_DCHECK(IsA<Derived>(from));
  return static_cast<Derived&>(from);
}
template <typename Derived, typename Base>
Derived* To(Base* from) {
  return from ? &To<Derived>(*from) : nullptr;
}

UserMediaClient* UserMediaClient::From(LocalDOMWindow* window) {
	...
  auto* client = Supplement<LocalDOMWindow>::From<UserMediaClient>(window);

template <typename SupplementType>
  static SupplementType* From(const Supplementable<T>& supplementable) {
    return supplementable.template RequireSupplement<SupplementType>();
  }

template <typename SupplementType>
  SupplementType* RequireSupplement() const {
		...
    const auto it = this->supplements_.find(SupplementType::kSupplementName);
    ...
  }
```

[0] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/media_stream_track_impl.cc;l=429

## Reproduce
Download Asan Release Chromium: `wget https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1147620.zip?generation=1684811282171770&alt=media`

Run: `/tmp/asan-linux-release-1147620/chrome --incognito --enable-blink-features=VideoTrackGeneratorInWorker,VideoTrackGenerator poc.html`

### wf...@chromium.org (2023-05-23)

Thank you for your report. Some initial triage. Will work on reproduction steps.

[Monorail components: Blink>MediaStream]

### cl...@chromium.org (2023-05-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6233569377320960.

### wf...@chromium.org (2023-05-23)

VideoTrackGeneratorInWorker is behind a flag so impact-none. memory corruption in the renderer process is high sev.

### ht...@chromium.org (2023-05-23)

VideoTrackGeneratorInWorker is an unfinished project; it has no status in runtime_enabled_features.json5, and is known not to work.

Should we add a NOTIMPLEMENTED() call in the constructor to avoid reports like this until the project is resumed?



### cl...@chromium.org (2023-05-23)

ClusterFuzz testcase 6233569377320960 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-05-23)

Detailed Report: https://clusterfuzz.com/testcase?key=6233569377320960

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::MediaStreamTrackImpl::stopTrack
  v8::internal::FunctionCallbackArguments::Call
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1148003

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6233569377320960

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### je...@gmail.com (2023-05-23)

[Comment Deleted]

### je...@gmail.com (2023-05-23)

[Comment Deleted]

### ht...@chromium.org (2023-05-24)

[Empty comment from Monorail migration]

### je...@gmail.com (2023-05-25)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2023-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/09b8ac2476d2db757605ec76026be76db8887c1f

commit 09b8ac2476d2db757605ec76026be76db8887c1f
Author: Harald Alvestrand <hta@chromium.org>
Date: Thu May 25 10:25:41 2023

Disallow VideoTrackGenerator in worker for now

The current implementation is not safe for use, and people are testing
with flags enabled even if they are in test-only state.

Disable in worker for now.

Bug: chromium:1448032
Change-Id: I700aff5160acc46c3c78f767ab8dd31b8a57bd7d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4558545
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Reviewed-by: Tony Herre <toprice@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1149003}

[modify] https://crrev.com/09b8ac2476d2db757605ec76026be76db8887c1f/third_party/blink/renderer/modules/breakout_box/video_track_generator.cc
[modify] https://crrev.com/09b8ac2476d2db757605ec76026be76db8887c1f/third_party/blink/renderer/modules/breakout_box/video_track_generator.idl


### je...@gmail.com (2023-05-25)

[Comment Deleted]

### ht...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-01)

Congratulations! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. A member of our finance team will reach out to you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-02)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-24)

[Description Changed]

### [Deleted User] (2023-09-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-01)

This issue was migrated from crbug.com/chromium/1448032?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1300528]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064747)*
