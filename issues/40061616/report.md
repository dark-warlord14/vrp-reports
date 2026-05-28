# Memory corruption in PresentationRequest

| Field | Value |
|-------|-------|
| **Issue ID** | [40061616](https://issues.chromium.org/issues/40061616) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>PresentationAPI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | mf...@chromium.org |
| **Created** | 2022-11-06 |
| **Bounty** | $8,500.00 |

## Description

**Steps to reproduce the problem:**  

visist the atached PoC, reproduced with 109.0.5405.0 Chromium.

**Problem Description:**  

memory corruption in blink

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.5405.0 \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 3.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 130 B)
- [poc.html](attachments/poc.html) (text/plain, 90 B)
- [asan2.txt](attachments/asan2.txt) (text/plain, 4.1 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 92 B)
- [suggestion_patch.diff](attachments/suggestion_patch.diff) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2022-11-06)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-06)

[Comment Deleted]

### ha...@gmail.com (2022-11-06)

tested on Windows 109.0.5405.0 Chromium:

out/asan/chrome.exe --no-sandbox  --enable-experimental-web-platform-features poc.html


### ha...@gmail.com (2022-11-06)

updated poc.html is attached

### ke...@chromium.org (2022-11-08)

Thanks for the report. This reproduces for me on Linux.

Security_Impact-None because of needing the experimental web platform features flag.

mfoltz@: PTAL?

[Monorail components: Blink>PresentationAPI]

### mf...@chromium.org (2022-11-08)

Looks like an issue with site initiated mirroring => takumif@
Missing a null-check on audioPlayback?


### ha...@gmail.com (2022-11-10)

After digging it, I found that the root cause is clear, i.e., type confusion in PresentationRequest.

When PresentationRequest is constructed, `PresentationRequest::Create` is called. If the source is `PresentationSource` type, it calls `CreateUrlFromSource` [1] to create the KURL. 

In `CreateUrlFromSource`, it only checks whether it has AudioPlayback [2]. However, since `PresentationSource` is a DictionaryBase type, and the field of `audioPlayback` could be null but still exists, `hasAudioPlayback` is insufficient if the `audioPlayback` is a null value. Then it will cast the nullable `audioPlayback` value to the Enum type by `AsEnum()`, leading to the type confusion.

[1]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/presentation/presentation_request.cc;l=114-123;drc=5a5b814da59edeb575b2c1fd49f66f7f7f6aade5

  for (const auto& source : sources) {
    if (source->IsPresentationSource()) {
      if (!RuntimeEnabledFeatures::SiteInitiatedMirroringEnabled()) {
        exception_state.ThrowDOMException(
            DOMExceptionCode::kNotSupportedError,
            "You must pass in valid URL strings.");
        return nullptr;
      }
      const KURL source_url = CreateUrlFromSource(
          *execution_context, *source->GetAsPresentationSource());


[2]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/presentation/presentation_request.cc;l=55-59;drc=5a5b814da59edeb575b2c1fd49f66f7f7f6aade5

  int capture_audio = !source.hasAudioPlayback() ||      // [2] source could has the audioPlayback member with a null value.
                              (source.audioPlayback()->AsEnum() ==  // [2] type confusion of the audioPlayback value
                               V8AudioPlaybackDestination::Enum::kReceiver)
                          ? 1
                          : 0;

### another type confusion

Moreover, after checking `PresentationSource`, I found that there exists another similar type confusions for the `CaptureLatency` field in `PresentationSource`. 

The type confusion of `CaptureLatency` is in `GetPlayoutDelay` function [3]. The checks in the [3], i.e., `source.hasLatencyHint()` is insufficient, since the `latencyHint` could be null (see poc2.html for detail) and bypass this check. Hence casting `source.latencyHint()` by `AsEnum()` causes the type confusion.

I've attached `poc2.html` to trigger this and the asan stack log as `asan2.txt`, reproduced on the 109.0.5409.0 chromium.

[3]https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/presentation/presentation_request.cc;l=41-51;drc=5a5b814da59edeb575b2c1fd49f66f7f7f6aade5

int GetPlayoutDelay(const PresentationSource& source) {
  if (!source.hasLatencyHint()) { // [3]  insufficient nullable check
    return 400;
  }
  switch (source.latencyHint()->AsEnum()) { // [3] type confusion here
    case V8CaptureLatency::Enum::kLow:
      return 200;
    case V8CaptureLatency::Enum::kDefault:
      return 400;
    case V8CaptureLatency::Enum::kHigh:
      return 800;
  }
}

### patch suggestion

We should check whether `source.audioPlayback()` or `source.latencyHint()` is `absl::nullopt` before casting it by the `AsEnum`. 

I've create an possible patch to fix it and attached it as suggestion_patch.diff:

diff --git a/third_party/blink/renderer/modules/presentation/presentation_request.cc b/third_party/blink/renderer/modules/presentation/presentation_request.cc
index cd9462a848ab9..df16f1eab407c 100644
--- a/third_party/blink/renderer/modules/presentation/presentation_request.cc
+++ b/third_party/blink/renderer/modules/presentation/presentation_request.cc
@@ -38,7 +38,7 @@ bool IsKnownProtocolForPresentationUrl(const KURL& url) {
 }

 int GetPlayoutDelay(const PresentationSource& source) {
-  if (!source.hasLatencyHint()) {
+  if (!source.hasLatencyHint() || source.latencyHint() == absl::nullopt) {
     return 400;
   }
   switch (source.latencyHint()->AsEnum()) {
@@ -53,7 +53,7 @@ int GetPlayoutDelay(const PresentationSource& source) {

 KURL CreateMirroringUrl(const PresentationSource& source) {
   int capture_audio = !source.hasAudioPlayback() ||
-                              (source.audioPlayback()->AsEnum() ==
+                              (source.audioPlayback() != absl::nullopt && source.audioPlayback()->AsEnum() ==
                                V8AudioPlaybackDestination::Enum::kReceiver)
                           ? 1
                           : 0;

### ha...@gmail.com (2022-11-10)

Moreover, I think it is introduced by the commit https://chromium-review.googlesource.com/c/chromium/src/+/3868662

Hence it affects stable channel, from 108.0.5316.0 to 108.0.5359.9 and from 109.0.5360.0 to 109.0.5412.1 chromium

### ha...@gmail.com (2022-11-15)

[Comment Deleted]

### mf...@chromium.org (2022-11-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2cb6033d3ae64c8a6cb1366cb2179c7b611b73d4

commit 2cb6033d3ae64c8a6cb1366cb2179c7b611b73d4
Author: mark a. foltz <mfoltz@chromium.org>
Date: Wed Nov 16 02:54:16 2022

[Presentation API] Null check PresentationSource parameters.

Adds a null check for properties of the PresentationSource.

Bug: 1381849
Change-Id: Iedf01625ab61d14c3afb462280f6a2ada4739a24
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4029402
Reviewed-by: Takumi Fujimoto <takumif@chromium.org>
Commit-Queue: Takumi Fujimoto <takumif@chromium.org>
Auto-Submit: Mark Foltz <mfoltz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1072010}

[modify] https://crrev.com/2cb6033d3ae64c8a6cb1366cb2179c7b611b73d4/third_party/blink/renderer/modules/presentation/presentation_request.cc


### mf...@chromium.org (2022-11-16)

happyercat@, thank you for the POC and suggested patch.  Please verify the fix on the next canary.


### ha...@gmail.com (2022-11-16)

Thanks for the quick fix. I could verify that the two type confusions are not reproducible on the latest canary 110.0.5422.0 chromium, i.e., the patch has fixed this issue.

### [Deleted User] (2022-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations, Chaoyuan Peng! The VRP Panel has decided to award you $7000 for this mildly mitigated security bug + $1000 bisect bonus + $500 patch bonus for a $8500 total VRP reward. Thank you for your efforts and reporting this issue to us. Nice work! 

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-02-22)

This issue was migrated from crbug.com/chromium/1381849?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061616)*
