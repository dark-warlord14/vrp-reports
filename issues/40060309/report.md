# wild read in DrawCall::run

| Field | Value |
|-------|-------|
| **Issue ID** | [40060309](https://issues.chromium.org/issues/40060309) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE, Internals>GPU>SwiftShader |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | em...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-07-16 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

1.google-chrome --disable-gpu --user-data-dir=/tmp/xx <http://localhost:8001/crash.html>

**Problem Description:**  

testedOS:  

macOS,Ubuntu22.04  

Chrome Version:  

Version 105.0.5148.2 (Official Build) dev (64-bit) ubuntu  

Chromium 105.0.5127.0 (MacOS)

src/third\_party/swiftshader/src/Device/Renderer.cpp  

...  

{  

auto batch = draw->batchDataPool->borrow();  

batch->id = batchId;  

batch->firstPrimitive = batch->id \* numPrimitivesPerBatch;  

batch->numPrimitives = std::min(batch->firstPrimitive + numPrimitivesPerBatch, numPrimitives) - batch->firstPrimitive;

```
	for(int cluster = 0; cluster < MaxClusterCount; cluster++)  
	{  
		batch->clusterTickets[cluster] = std::move(clusterQueues[cluster].take());  
	}  

	marl::schedule([device, draw, batch, finally] {  
		processVertices(device, draw.get(), batch.get());   ==>Thread<00> (5): EXC_BAD_ACCESS (code=1, address=0x2dfff4814)   

		if(!draw->setupState.rasterizerDiscard)  
		{  
			processPrimitives(device, draw.get(), batch.get());  

			if(batch->numVisible > 0)  
			{  
				processPixels(device, draw, batch, finally);  
				return;  
			}  
		}  

```

Because I cannot be repro this issue in the debug build with symbole, more detailed information cannot be provided for the time being.

**Additional Comments:**

\*\*Chrome version: \*\* Version 105.0.5148.2 (Official Build) dev (64-bit) \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 2.5 KB)
- [crash.html](attachments/crash.html) (text/plain, 2.4 KB)
- [webgl-test-utils2.js](attachments/webgl-test-utils2.js) (text/plain, 112.4 KB)
- [crash2.html](attachments/crash2.html) (text/plain, 2.5 KB)

## Timeline

### em...@gmail.com (2022-07-16)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-07-16)

My mistake,upload poc again.

### [Deleted User] (2022-07-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-07-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5641191639154688.

### dc...@chromium.org (2022-07-19)

Can you please provide a copy of webgl-test-utils2.js as well?

### em...@gmail.com (2022-07-19)

Ok, but this issue doesn't depend on  webgl-test-utils2.js file. 
In my local test, the debug version cannot   repro, but the release version and asan version can  repro. 
I slightly modified crash2.html. Please try again, thanks.

### dc...@chromium.org (2022-07-19)

I'm not sure why clusterfuzz cannot repro. I think I am able to repro a little, but the stacks are completely useless and I'm not sure why.

### dc...@chromium.org (2022-07-19)

+hans@ as FYI for stack issues, though I'm not actually able to get a useful stack out of gdb for this one, so maybe it's unrelated to the other issue.

I was able to repro this in asan-linux-release-1002910, so I'm tagging this as FoundIn-103, but we're still missing a lot of information we need to actually narrow down what's going on here.

For lack of a better idea, I'm randomly assigning to an OWNER from //third_party/blink/renderer/modules/webgl. I'm not sure what severity to mark this as without a bit more information on what's actually triggering the crash.

[Monorail components: Blink>WebGL]

### [Deleted User] (2022-07-19)

[Empty comment from Monorail migration]

### kb...@chromium.org (2022-07-20)

While this POC is triggered via WebGL, the out of range read seems to be coming from SwiftShader. Alexei, Nicolas, could one of you please try to triage this?

Upon initial investigation it doesn't look like the test case is running a very long shader, or submitting an enormous amount of geometry.


[Monorail components: Internals>GPU>SwiftShader]

### rs...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-07-21)

> the out of range read seems to be coming from SwiftShader

It appears to be a use-after-free, which could be an ANGLE bug. There's a storage buffer which gets written to (likely to emulate transform feedback) during a first draw call. Then the buffer gets deleted, but a subsequent draw call attempts to write to it as well.

Jamie can you please take a look?

[Monorail components: Internals>GPU>ANGLE]

### dc...@chromium.org (2022-07-21)

Do you know why this isn't being detected as a standard use-after-free? Is there a custom allocator involved?

### kb...@chromium.org (2022-07-21)

Jamie's OOO - Geoff, any chance someone else from the ANGLE team could investigate?


### [Deleted User] (2022-07-21)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-07-21)

(auto-cc on security bug)

### sy...@chromium.org (2022-07-22)

I can take a look at this on Monday.

### gi...@appspot.gserviceaccount.com (2022-07-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/80022b96c6eda4dab1d342a11d7aef8b72ed420b

commit 80022b96c6eda4dab1d342a11d7aef8b72ed420b
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Jul 27 01:07:04 2022

Vulkan: Fix xfb buffer redefine to smaller size

In 89e11878b275b15735eaf273ababfa6fd43a2e3d, a use-after-free bug was
fixed where glBufferData redefined a buffer, leading to a change in
storage.  This was only tested for the case where the new buffer was
larger than the old buffer.

When the new buffer is smaller however, another issue remains where the
buffer size as cached by the transform feedback object used the old
object's size.  This is worked around in this change, with a fix for the
real issue (that the buffer state is updated after calling into the
backend instead of before) coming up.

Bug: chromium:1345042
Change-Id: I6c9e9344705fefe49926a14cf6ce73ce84305872
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3788308
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>
Auto-Submit: Shahbaz Youssefi <syoussefi@chromium.org>
Reviewed-by: Charlie Lao <cclao@google.com>
Commit-Queue: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/80022b96c6eda4dab1d342a11d7aef8b72ed420b/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/80022b96c6eda4dab1d342a11d7aef8b72ed420b/src/libANGLE/renderer/vulkan/TransformFeedbackVk.cpp
[modify] https://crrev.com/80022b96c6eda4dab1d342a11d7aef8b72ed420b/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/80022b96c6eda4dab1d342a11d7aef8b72ed420b/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/80022b96c6eda4dab1d342a11d7aef8b72ed420b/src/libANGLE/renderer/vulkan/BufferVk.cpp


### ni...@google.com (2022-07-27)

> Do you know why this isn't being detected as a standard use-after-free?

Yes, the crash happens in JIT-compiled code, which isn't instrumented. I'll look into supporting it: b/240465596.

### sy...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-28)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M104. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M105. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-28)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-28)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/41df4dedd0d03da5bcf740ccc2e01c089503acc9

commit 41df4dedd0d03da5bcf740ccc2e01c089503acc9
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jul 28 19:18:22 2022

Roll ANGLE from 0dc29af95a66 to c48cfa02e3e6 (11 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/0dc29af95a66..c48cfa02e3e6

2022-07-28 jmadill@chromium.org Revert "Disable share context lock for Chromium"
2022-07-28 jmadill@chromium.org Test Runner: Disable --bot-mode on Fuchsia.
2022-07-28 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 7158d6e8eaad to d28e244d3e12 (3 revisions)
2022-07-28 angle-autoroll@skia-public.iam.gserviceaccount.com Roll SwiftShader from 1739966fee2a to e8c074d7684b (4 revisions)
2022-07-28 angle-autoroll@skia-public.iam.gserviceaccount.com Roll Chromium from 85c57e6023c8 to e810ac85e1c8 (442 revisions)
2022-07-27 steven@valvesoftware.com d3d11: allow selecting render device by PCI vendor/device ID
2022-07-27 penghuang@chromium.org Remove WARN() in getPixelFormatInfo()
2022-07-27 syoussefi@chromium.org Vulkan: Fix xfb buffer redefine to smaller size
2022-07-27 ynovikov@chromium.org Roll chromium_revision 1201dfbc62..85c57e6023 (1027387:1028671)
2022-07-27 steven@valvesoftware.com Vulkan: allow selecting render device by PCI device/vendor IDs
2022-07-27 penghuang@chromium.org Disable share context lock for Chromium

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC yuxinhu@google.com,jmadill@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1336126,chromium:1345042,chromium:1347817
Tbr: yuxinhu@google.com,jmadill@google.com
Change-Id: Ia4e673d9ae034f66fc3843de55a2a243248929b8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3792226
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1029400}

[modify] https://crrev.com/41df4dedd0d03da5bcf740ccc2e01c089503acc9/DEPS


### sy...@chromium.org (2022-07-28)

1. UAF security fix
2. https://chromium-review.googlesource.com/c/angle/angle/+/3788308
3. Merged to Chromium just today, needs a few days to be tested on Canary
4. No
5. N/A
6. N/A


### am...@chromium.org (2022-08-01)

Thank you for this fix and the responses in #27., syoussefi@! 
We are temporarily pausing merges to M104, so leaving this in the m104 merge review queue for now.

M105 merge approved, please merge this fix to branch 5195 at your earliest availability 

### gi...@appspot.gserviceaccount.com (2022-08-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/647273af89deaa2f016452a8d562ce7c44e04720

commit 647273af89deaa2f016452a8d562ce7c44e04720
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Jul 27 01:07:04 2022

M105: Vulkan: Fix xfb buffer redefine to smaller size

In 89e11878b275b15735eaf273ababfa6fd43a2e3d, a use-after-free bug was
fixed where glBufferData redefined a buffer, leading to a change in
storage.  This was only tested for the case where the new buffer was
larger than the old buffer.

When the new buffer is smaller however, another issue remains where the
buffer size as cached by the transform feedback object used the old
object's size.  This is worked around in this change, with a fix for the
real issue (that the buffer state is updated after calling into the
backend instead of before) coming up.

Bug: chromium:1345042
Change-Id: Ib370539bfffe1033c443572e3265062261be8dfe
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3807061
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/647273af89deaa2f016452a8d562ce7c44e04720/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/647273af89deaa2f016452a8d562ce7c44e04720/src/libANGLE/renderer/vulkan/TransformFeedbackVk.cpp
[modify] https://crrev.com/647273af89deaa2f016452a8d562ce7c44e04720/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/647273af89deaa2f016452a8d562ce7c44e04720/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/647273af89deaa2f016452a8d562ce7c44e04720/src/libANGLE/renderer/vulkan/BufferVk.cpp


### am...@chromium.org (2022-08-04)

Adjusting to high severity based on https://crbug.com/chromium/1345042#c19 as this is a uaf in the gpu process 

### am...@chromium.org (2022-08-04)

M104 merge approved, please go ahead and merge this fix to branch 5112 at your earliest convenience. Thank you! 

### gi...@appspot.gserviceaccount.com (2022-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/1121a459f094cd85e8b1b4dff0adcac5ccf0a5d2

commit 1121a459f094cd85e8b1b4dff0adcac5ccf0a5d2
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Wed Jul 27 01:07:04 2022

M104: Vulkan: Fix xfb buffer redefine to smaller size

In 89e11878b275b15735eaf273ababfa6fd43a2e3d, a use-after-free bug was
fixed where glBufferData redefined a buffer, leading to a change in
storage.  This was only tested for the case where the new buffer was
larger than the old buffer.

When the new buffer is smaller however, another issue remains where the
buffer size as cached by the transform feedback object used the old
object's size.  This is worked around in this change, with a fix for the
real issue (that the buffer state is updated after calling into the
backend instead of before) coming up.

Bug: chromium:1345042
Change-Id: I7bafd51b6203a419e5ef123da26b9e1eaf079bf1
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3812556
Reviewed-by: Ian Elliott <ianelliott@google.com>

[modify] https://crrev.com/1121a459f094cd85e8b1b4dff0adcac5ccf0a5d2/src/tests/gl_tests/TransformFeedbackTest.cpp
[modify] https://crrev.com/1121a459f094cd85e8b1b4dff0adcac5ccf0a5d2/src/libANGLE/renderer/vulkan/TransformFeedbackVk.cpp
[modify] https://crrev.com/1121a459f094cd85e8b1b4dff0adcac5ccf0a5d2/src/tests/angle_end2end_tests_expectations.txt
[modify] https://crrev.com/1121a459f094cd85e8b1b4dff0adcac5ccf0a5d2/src/libANGLE/renderer/vulkan/ContextVk.cpp
[modify] https://crrev.com/1121a459f094cd85e8b1b4dff0adcac5ccf0a5d2/src/libANGLE/renderer/vulkan/BufferVk.cpp


### sy...@chromium.org (2022-08-05)

Done

### am...@google.com (2022-08-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-11)

Congratulations on another on, Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts in discovering and reporting these GPU bugs to us -- nice work! 

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-16)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1345042?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE, Internals>GPU>SwiftShader]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060309)*
