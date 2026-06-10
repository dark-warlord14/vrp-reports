# Incomplete Fix for Issue 361782106

| Field | Value |
|-------|-------|
| **Issue ID** | [374310077](https://issues.chromium.org/issues/374310077) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | or...@chromium.org |
| **Created** | 2024-10-18 |
| **Bounty** | $11,000.00 |

## Description

tested OS: Ubuntu & MacOS

tested chrome version:

- Chromium 132.0.6785.0
- Chromium 130.0.6699.3

**Reproduction Steps:**

```
./chrome --user-data-dir=/tmp/xx2 http://localhost:8880/crash.html

```

The issue should reproduce in approximately **30 seconds**.

---

**Note:**

Two months ago, I submitted a WebRTC-related issue ([issue 361782106](https://bugs.chromium.org/p/chromium/issues/detail?id=361782106)). At that time, the CL was implemented as follows:

```
void RTCDataChannel::send(Blob* data, ExceptionState& exception_state) {
+  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
   is_transferable_ = false;

-  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
+  if (state_ != webrtc::DataChannelInterface::kOpen) {
+    ThrowNotOpenException(&exception_state);
+    return;
+  }
+

```

[Reference CL](https://chromium-review.googlesource.com/c/chromium/src/+/5844814)

After this CL was applied, I tested the fix and confirmed that the issue no longer occurred. However, upon modifying the POC today, I found that the issue can still be reproduced in the latest version.

**Differences from the Previous PoC:**

- **Previous PoC:** Forcefully and continuously sent Blob-type data over the data channel.
- **Current PoC:** Establishes a normal data channel connection before sending Blob-type data.

**Suspected Cause:**

I suspect that the previous fix only partially addressed the underlying problem, which allows the new PoC to trigger the issue again. It appears that sending Blob-type data over an established data channel still leads to the same crash.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 6.9 KB)
- [fix.diff](attachments/fix.diff) (text/x-diff, 3.2 KB)

## Timeline

### em...@gmail.com (2024-10-20)

Here's an update on the analysis progress.

In [Chromium code review 3110559](https://chromium-review.googlesource.com/c/chromium/src/+/3110559), the `FileReaderLoader` object is used to support the Blob type. However, this object might be unexpectedly garbage collected when `RTCDataChannel::OnStateChange()` is repeatedly called with the state `webrtc::DataChannelInterface::kClosed`.

```
diff --git a/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc b/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc
index 8afa09e..841e6c2 100644
--- a/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc
+++ b/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc
...
+RTCDataChannel::BlobReader::BlobReader(ExecutionContext* context,
+                                       RTCDataChannel* data_channel,
+                                       PendingMessage* message)
+    : ExecutionContextLifecycleObserver(context),
+      loader_(MakeGarbageCollected<FileReaderLoader>(         // ---> [0]
+          this,
+          GetExecutionContext()->GetTaskRunner(TaskType::kFileReading))),
+      data_channel_(data_channel),
+      message_(message) {}
...

```

Here is the suggested fix:

```
diff --git a/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc b/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc
index 3eeec56af8389..edf40636baa81 100644
--- a/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc
+++ b/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc
@@ -869,6 +869,7 @@ void RTCDataChannel::BlobReader::DidFinishLoading(FileReaderData data) {
   message_->buffer_ = webrtc::DataBuffer(buffer, true);
   message_->type_ = RTCDataChannel::PendingMessage::Type::kBufferReady;
   data_channel_->ProcessSendQueue();
+  Dispose();
 }

 void RTCDataChannel::BlobReader::DidFail(FileErrorCode error) {
@@ -879,6 +880,7 @@ void RTCDataChannel::BlobReader::DidFail(FileErrorCode error) {
       "Couldn't read Blob content, skipping message."));
   message_->type_ = RTCDataChannel::PendingMessage::Type::kBlobFailure;
   data_channel_->ProcessSendQueue();
+  Dispose();
 }

 RTCDataChannel::BlobReader::BlobReader(ExecutionContext* context,
@@ -889,10 +891,10 @@ RTCDataChannel::BlobReader::BlobReader(ExecutionContext* context,
             this,
             GetExecutionContext()->GetTaskRunner(TaskType::kFileReading))),
         data_channel_(data_channel),
-        message_(message) {}
+        message_(message),
+        keep_alive_(this) {}

 RTCDataChannel::BlobReader::~BlobReader() = default;

 void RTCDataChannel::BlobReader::Start(Blob* blob) {
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
   loader_->Start(blob->GetBlobDataHandle());
@@ -910,7 +912,10 @@ bool RTCDataChannel::BlobReader::HasFinishedLoading() const {
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
   return loader_->HasFinishedLoading();
 }

+void RTCDataChannel::BlobReader::Dispose() {
+  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
+  keep_alive_.Clear();
+}
 void RTCDataChannel::BlobReader::ContextDestroyed() {
   DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);
   loader_->Cancel();
diff --git a/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h b/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h
index 9a0879b81399a..465286ae9c9f6 100644
--- a/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h
+++ b/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h
@@ -45,7 +45,7 @@
 #include "third_party/blink/renderer/platform/timer.h"
 #include "third_party/webrtc/api/data_channel_interface.h"
 #include "third_party/webrtc/api/peer_connection_interface.h"
+#include "third_party/blink/renderer/platform/heap/self_keep_alive.h"

 namespace blink {

@@ -239,7 +239,8 @@ class MODULES_EXPORT RTCDataChannel final

     void Start(Blob* blob);
     bool HasFinishedLoading() const;

+    void Dispose();
     // FileReaderAccumulator
     void DidFinishLoading(FileReaderData data) override;
     void DidFail(FileErrorCode error) override;
@@ -251,10 +252,11 @@ class MODULES_EXPORT RTCDataChannel final
     void Trace(Visitor*) const override;

    private:

     Member<FileReaderLoader> loader_;
     Member<RTCDataChannel> data_channel_;
     Member<PendingMessage> message_;

+    SelfKeepAlive<BlobReader> keep_alive_;
     SEQUENCE_CHECKER(sequence_checker_);
   };

```

By applying these changes, we can prevent the `BlobReader` object from being prematurely garbage collected during asynchronous operations.

### ps...@google.com (2024-10-20)

Thank you for the report, I was able to reproduce on linux 130.0.6723.58. Assigning to orphis@chromium.org as they handled the initial fix. 

- govind@google.com: FYI

### pe...@google.com (2024-10-21)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-10-22)

Project: chromium/src  

Branch: main  

Author: Florent Castelli <[orphis@chromium.org](mailto:orphis@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5952972>

datachannel: Keep the BlobReader alive until the FileReaderLoader resolves

---


Expand for full commit details
```
datachannel: Keep the BlobReader alive until the FileReaderLoader resolves

Bug: 374310077
Change-Id: Ic6882d57c465d0e8b64327595213fa881b150181
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5952972
Reviewed-by: Harald Alvestrand <hta@chromium.org>
Commit-Queue: Florent Castelli <orphis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1371980}

```

---

Files:

- M `third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc`
- M `third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h`

---

Hash: 6e4bc681b82bd11f8259c5a8f51593cb6ab444fe  

Date:  Tue Oct 22 13:01:49 2024


---

### or...@chromium.org (2024-10-22)

A fix with your suggested changes has landed. Can you test Canary again when the change has been integrated?

You can check which version it lands in in this page: https://chromiumdash.appspot.com/commit/6e4bc681b82bd11f8259c5a8f51593cb6ab444fe

I'll then merge this in previous versions.

### pe...@google.com (2024-10-22)

Security Merge Request Consideration: Requesting merge to stable (M130) because latest trunk commit (1371980) appears to be after stable branch point (1356013).
Security Merge Request Consideration: Requesting merge to beta (M131) because latest trunk commit (1371980) appears to be after beta branch point (1368529).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### em...@gmail.com (2024-10-22)

I have tested the latest version (gs://chromium-browser-asan/linux-release/asan-linux-release-1372040.zip) and can confirm that the issue has not been reproduced.

### pe...@google.com (2024-10-23)

Merge review required: M131 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)

### pe...@google.com (2024-10-23)

Merge review required: M130 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), gmpritchard (ChromeOS), danielyip (Desktop)

### pg...@google.com (2024-10-24)

Reviewing canary and dev (where available) I do not see any relevant crash/stability impacts. The change looks straight forward from the last time this was attempted to be fixed!

Merge approved for M130 - please merge to branch 6723 by tomorrow Friday Oct 25 by 10AM MTV time to get this change into the next stable release!  

Merge approved for M131 - please merge to branch 6778 at your earliest convenience to get this change into the next beta release!

### ap...@google.com (2024-10-25)

Project: chromium/src  

Branch: refs/branch-heads/6778  

Author: Florent Castelli <[orphis@chromium.org](mailto:orphis@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5963959>

[M131] datachannel: Keep the BlobReader alive until the FileReaderLoader resolves

---


Expand for full commit details
```
[M131] datachannel: Keep the BlobReader alive until the FileReaderLoader resolves 
 
(cherry picked from commit 6e4bc681b82bd11f8259c5a8f51593cb6ab444fe) 
 
Bug: 374310077 
Change-Id: Ic6882d57c465d0e8b64327595213fa881b150181 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5952972 
Reviewed-by: Harald Alvestrand <hta@chromium.org> 
Commit-Queue: Florent Castelli <orphis@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1371980} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5963959 
Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
Auto-Submit: Florent Castelli <orphis@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6778@{#851} 
Cr-Branched-From: b21671ca172dcfd1566d41a770b2808e7fa7cd88-refs/heads/main@{#1368529}

```

---

Files:

- M `third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc`
- M `third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h`

---

Hash: 0ec5c4e7ea11f6433a963a4f24dd76eee3d7c77a  

Date:  Fri Oct 25 13:48:44 2024


---

### pe...@google.com (2024-10-25)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ap...@google.com (2024-10-25)

Project: chromium/src  

Branch: refs/branch-heads/6723  

Author: Florent Castelli <[orphis@chromium.org](mailto:orphis@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5965137>

[M130] datachannel: Keep the BlobReader alive until the FileReaderLoader resolves

---


Expand for full commit details
```
[M130] datachannel: Keep the BlobReader alive until the FileReaderLoader resolves 
 
(cherry picked from commit 6e4bc681b82bd11f8259c5a8f51593cb6ab444fe) 
 
Bug: 374310077 
Change-Id: Ic6882d57c465d0e8b64327595213fa881b150181 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5952972 
Reviewed-by: Harald Alvestrand <hta@chromium.org> 
Commit-Queue: Florent Castelli <orphis@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1371980} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5965137 
Auto-Submit: Florent Castelli <orphis@chromium.org> 
Reviewed-by: Guido Urdaneta <guidou@chromium.org> 
Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6723@{#1492} 
Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

```

---

Files:

- M `third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc`
- M `third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h`

---

Hash: 70783c4250f7c9f7fce3a0f178f7f3576e709e89  

Date:  Fri Oct 25 15:31:02 2024


---

### qk...@google.com (2024-10-28)

Labeling as LTS-NotApplicable-126 because the suspected CL[1] was not merged to M126 LTS. So it looks like we don't need to merge the fix to M126 LTS.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/3110559

### pg...@google.com (2024-10-29)

(Removing ios from the OS fields, as Blink does not impact iOS)

### sp...@google.com (2024-11-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of demonstrated memory corruption in a sandboxed process / the renderer + $1,000 patch bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-08)

Congratulations Cassidy Kim! Thank you for your efforts and your high quality reporting of this issue to us -- nice work!

### pe...@google.com (2025-01-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/374310077)*
