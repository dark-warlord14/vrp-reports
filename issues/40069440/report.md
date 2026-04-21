# Use-After-Free in MediaStreamDeviceObserver::OnDeviceStopped

| Field | Value |
|-------|-------|
| **Issue ID** | [40069440](https://issues.chromium.org/issues/40069440) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>MediaStream |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | fw...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2023-08-12 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. chrome.exe --no-sandbox <http://localhost:8001/test.html>
2. Click the Allow Microphone Permissions button
3. Disabling microphone access after page load

**Problem Description:**  

[0] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/user_media_processor.cc;l=1594>  

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/mediastream/media_stream_device_observer.cc;l=79>  

[2] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/modules/mediastream/media_stream_track_impl.cc;l=817>

- Call AddStreams by calling navigator.mediaDevices.getUserMedia[0]
- Calling UserMeidaProcessor::OnDeviceChanged with [0] as the argument when the button to deny access to the microphone is pressed
- Call on\_device\_stopped\_cb in MediaStreamDeviceObserver::OnDeviceStopped Call user event function by calling [2] inside that function
- A use-after-free vulnerability occurs through access to the label\_stream\_map\_ member variable when detaching and releasing an iframe that manages the MediaStreamDevicesObserver life in an event.

**Additional Comments:**

\*\*Chrome version: \*\* 118.0.5939.0 \*\*Channel: \*\* Dev

**OS:** Windows

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 688 B)
- [asan_.log](attachments/asan_.log) (text/plain, 18.8 KB)
- [access.png](attachments/access.png) (image/png, 5.2 KB)
- [blocked.png](attachments/blocked.png) (image/png, 18.3 KB)

## Timeline

### [Deleted User] (2023-08-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-14)

Thanks for the report!

I am unable to reproduce this on a Linux - I assume in step 1 the test.html is the provided poc.html but I was unable to get the microphone permissions dialog to pop up to proceed with steps 2 and 3.
Can you provide clarification on the repro steps?


### fw...@gmail.com (2023-08-15)

- The button mentioned in step 2 corresponds to the corresponding access.png file.
- The action related to the microphone block mentioned in step 3 requires user interaction corresponding to blocked.png

If the button corresponding to access.png does not appear, isn't it possible that the microphone-related system settings are turned off?

### pg...@google.com (2023-08-15)

Thanks for the additional info, reporter!

Setting foundIn to the current stable but provisionally as the linked lines in code have been there for a while
gidou@ - assigning to you based on component history; can you take a look and reroute if necessary?

[Monorail components: Blink>MediaStream]

### [Deleted User] (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### gu...@chromium.org (2023-08-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7337133682ab0404b753c563dde2ae2b1dc13171

commit 7337133682ab0404b753c563dde2ae2b1dc13171
Author: Guido Urdaneta <guidou@chromium.org>
Date: Tue Aug 22 12:53:11 2023

Handle object destruction in MediaStreamDeviceObserver

MSDO executes some callbacks that can result in the destruction of
MSDO upon an external event such as removing a media device or the
user revoking permission.
This CL adds code to detect this condition and prevent further
processing that would result in UAF. It also removes some invalid
DCHECKs.

Drive-by: minor style fixes

Bug: 1472492, b/296997707
Change-Id: I76f019bb110e7d9cca276444bc23a7e43114d2cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4798398
Reviewed-by: Palak Agarwal <agpalak@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1186452}

[modify] https://crrev.com/7337133682ab0404b753c563dde2ae2b1dc13171/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.h
[modify] https://crrev.com/7337133682ab0404b753c563dde2ae2b1dc13171/third_party/blink/renderer/platform/exported/mediastream/web_platform_media_stream_source.cc
[modify] https://crrev.com/7337133682ab0404b753c563dde2ae2b1dc13171/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.cc


### gu...@chromium.org (2023-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-23)

Requesting merge to stable M116 because latest trunk commit (1186452) appears to be after stable branch point (1160321).

Requesting merge to beta M117 because latest trunk commit (1186452) appears to be after beta branch point (1181205).

Merge review required: M116 is already shipping to stable.

Merge review required: M117 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [116, 117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@chromium.org (2023-08-23)


1. Which CLs should be backmerged? (Please include Gerrit links.)
r1186452

2. Has this fix been tested on Canary?
Yes.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
No stability regressions or risks.

4. Does this fix pose any known compatibility risks?
No.

5. Does it require manual verification by the test team? If so, please describe required testing.
Not required, but feel free to try the repro page supplied in the description.



### pg...@google.com (2023-08-24)

Merge approved for M116 - please merge to branch 5845 by EOD Mountain View time Thursday Aug 24th to get this in the next stable respin
Merge approved for M117 - please merge to branch 5938 at your earliest convenience to get this fix into M117 beta

### gi...@appspot.gserviceaccount.com (2023-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8b7d02f3330376e8dc701db18f07786b3cca1536

commit 8b7d02f3330376e8dc701db18f07786b3cca1536
Author: Guido Urdaneta <guidou@chromium.org>
Date: Thu Aug 24 09:58:38 2023

Handle object destruction in MediaStreamDeviceObserver

MSDO executes some callbacks that can result in the destruction of
MSDO upon an external event such as removing a media device or the
user revoking permission.
This CL adds code to detect this condition and prevent further
processing that would result in UAF. It also removes some invalid
DCHECKs.

Drive-by: minor style fixes

(cherry picked from commit 7337133682ab0404b753c563dde2ae2b1dc13171)

Bug: 1472492, b/296997707
Change-Id: I76f019bb110e7d9cca276444bc23a7e43114d2cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4798398
Reviewed-by: Palak Agarwal <agpalak@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1186452}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4807726
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5938@{#502}
Cr-Branched-From: 2b50cb4bcc2318034581a816714d9535dc38966d-refs/heads/main@{#1181205}

[modify] https://crrev.com/8b7d02f3330376e8dc701db18f07786b3cca1536/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.h
[modify] https://crrev.com/8b7d02f3330376e8dc701db18f07786b3cca1536/third_party/blink/renderer/platform/exported/mediastream/web_platform_media_stream_source.cc
[modify] https://crrev.com/8b7d02f3330376e8dc701db18f07786b3cca1536/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.cc


### [Deleted User] (2023-08-24)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@chromium.org (2023-08-24)


1. Was this issue a regression for the milestone it was found in?
No. But the bug is present in M114.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?
No. It is an older bug.

### gi...@appspot.gserviceaccount.com (2023-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/35c06406a658e424a27f59e7a3910f29c5c1122a

commit 35c06406a658e424a27f59e7a3910f29c5c1122a
Author: Guido Urdaneta <guidou@chromium.org>
Date: Thu Aug 24 11:12:43 2023

Handle object destruction in MediaStreamDeviceObserver

MSDO executes some callbacks that can result in the destruction of
MSDO upon an external event such as removing a media device or the
user revoking permission.
This CL adds code to detect this condition and prevent further
processing that would result in UAF. It also removes some invalid
DCHECKs.

Drive-by: minor style fixes

(cherry picked from commit 7337133682ab0404b753c563dde2ae2b1dc13171)

Bug: 1472492, b/296997707
Change-Id: I76f019bb110e7d9cca276444bc23a7e43114d2cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4798398
Reviewed-by: Palak Agarwal <agpalak@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1186452}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4810035
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5845@{#1586}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/35c06406a658e424a27f59e7a3910f29c5c1122a/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.h
[modify] https://crrev.com/35c06406a658e424a27f59e7a3910f29c5c1122a/third_party/blink/renderer/platform/exported/mediastream/web_platform_media_stream_source.cc
[modify] https://crrev.com/35c06406a658e424a27f59e7a3910f29c5c1122a/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.cc


### pg...@google.com (2023-08-24)

The initial commit landed in M118

### pg...@google.com (2023-08-25)

Adding additional OSes liberally - guidou,  please feel free to remove the OSes that are not impacted.

### rz...@google.com (2023-08-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-28)

@reporter, how would you like to be credited?

### rz...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-08-29)

1. https://crrev.com/c/4814875
2. Low, no conflicts
3. 116
4. Low, no conflicts

### fw...@gmail.com (2023-08-29)

fwnfwn(@_fwnfwn)

### pg...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-30)

[Empty comment from Monorail migration]

### rz...@google.com (2023-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-31)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-08-31)

1. https://crrev.com/c/4822913
2. Low, no conflicts
3. 116
4. Yes

### gm...@google.com (2023-09-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-07)

Congratulations! The VRP Panel has decided to award you $3,000 for this report of a mildly mitigated security bug, mitigated by user interaction, in the renderer process. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### gm...@google.com (2023-09-08)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1d40d64e1494de7dff27e34379208f37ef40ce3e

commit 1d40d64e1494de7dff27e34379208f37ef40ce3e
Author: Guido Urdaneta <guidou@chromium.org>
Date: Fri Sep 08 12:47:38 2023

[M114-LTS] Handle object destruction in MediaStreamDeviceObserver

MSDO executes some callbacks that can result in the destruction of
MSDO upon an external event such as removing a media device or the
user revoking permission.
This CL adds code to detect this condition and prevent further
processing that would result in UAF. It also removes some invalid
DCHECKs.

Drive-by: minor style fixes

(cherry picked from commit 7337133682ab0404b753c563dde2ae2b1dc13171)

Bug: 1472492, b/296997707
Change-Id: I76f019bb110e7d9cca276444bc23a7e43114d2cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4798398
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1186452}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4814875
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1593}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/1d40d64e1494de7dff27e34379208f37ef40ce3e/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.h
[modify] https://crrev.com/1d40d64e1494de7dff27e34379208f37ef40ce3e/third_party/blink/renderer/platform/exported/mediastream/web_platform_media_stream_source.cc
[modify] https://crrev.com/1d40d64e1494de7dff27e34379208f37ef40ce3e/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.cc


### gi...@appspot.gserviceaccount.com (2023-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4322aa806c3e0ef8dcced08064e473f95625ab67

commit 4322aa806c3e0ef8dcced08064e473f95625ab67
Author: Guido Urdaneta <guidou@chromium.org>
Date: Fri Sep 08 15:11:02 2023

[M108-LTS] Handle object destruction in MediaStreamDeviceObserver

MSDO executes some callbacks that can result in the destruction of
MSDO upon an external event such as removing a media device or the
user revoking permission.
This CL adds code to detect this condition and prevent further
processing that would result in UAF. It also removes some invalid
DCHECKs.

Drive-by: minor style fixes

(cherry picked from commit 7337133682ab0404b753c563dde2ae2b1dc13171)

Bug: 1472492, b/296997707
Change-Id: I76f019bb110e7d9cca276444bc23a7e43114d2cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4798398
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1186452}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4822913
Reviewed-by: Tony Herre <toprice@chromium.org>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1514}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/4322aa806c3e0ef8dcced08064e473f95625ab67/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.h
[modify] https://crrev.com/4322aa806c3e0ef8dcced08064e473f95625ab67/third_party/blink/renderer/platform/exported/mediastream/web_platform_media_stream_source.cc
[modify] https://crrev.com/4322aa806c3e0ef8dcced08064e473f95625ab67/third_party/blink/renderer/modules/mediastream/media_stream_device_observer.cc


### am...@google.com (2023-09-09)

[Empty comment from Monorail migration]

### rz...@google.com (2023-09-11)

[Empty comment from Monorail migration]

### rz...@google.com (2023-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### da...@davidmanouchehri.com (2023-11-29)

Could you undelete the PoC?

### am...@chromium.org (2023-11-30)

Hi David, thanks for reaching out. 

Also hello fwnfwn, we consider attachments/POCs and all analysis included with reports to be an integral part of the report (https://g.co/chrome/vrp/#investigating-and-reporting-bugs), even when included in comments, so I have undeleted them. Thanks! 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1472492?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069440)*
