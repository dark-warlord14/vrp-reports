# Security: use-after-poison in blink::FileReaderLoader::OnReceivedData

| Field | Value |
|-------|-------|
| **Issue ID** | [40053717](https://issues.chromium.org/issues/40053717) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DataTransfer, Blink>Storage>FileAPI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wo...@gmail.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2020-10-26 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The renderer process of chromium with ASAN crash when following testcase executed.  

Also I confirmed that crash can be reproduced even linux stable, windows stable, MS Edge.  

The PoC is unstable. (in my environment, the crash reproduced after reloading a few times)  

I used the option (--single-process) to get a complete ASAN report. (ASAN.log)

**VERSION**  

Chrome Version: 88.0.4294.0 (Canary ASAN Build: asan-linux-release-817421)  

Operating System: Linux (Ubuntu 18.04 LTS)

**REPRODUCTION CASE**

1. Download and extract asan-linux-release-817421.zip from (<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-817421.zip?generation=1602754092776757&alt=media>)
2. cd path/to/poc.html dir/
3. python3 -m http.server 8090
4. ./chrome <http://localhost:8090/poc.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: attached ASAN log

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.4 KB)
- [ASAN.log](attachments/ASAN.log) (text/plain, 12.7 KB)

## Timeline

### cl...@chromium.org (2020-10-26)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5671176066367488.

### cl...@chromium.org (2020-10-26)

ClusterFuzz testcase 5671176066367488 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-10-26)

Detailed Report: https://clusterfuzz.com/testcase?key=5671176066367488

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000030
Crash State:
  blink::ClipboardHtmlWriter::StartWrite
  blink::ClipboardWriter::DidFinishLoading
  blink::mojom::blink::BlobReaderClientStubDispatch::Accept
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=820672

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5671176066367488

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5671176066367488 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### oc...@google.com (2020-10-27)

Unable to reproduce this at all on CF (apart from the flaky null deref above). 

+mek (an OWNER of third_party/blink/renderer/core/fileapi). Could you please see if you can reproduce this or if there's anything obvious from the stacktrace provided in the original report?

assigning some initial security labels under the assumption that this reproduces.

[Monorail components: Blink>Storage>FileAPI]

### me...@chromium.org (2020-10-27)

Yeah, that code looks buggy. https://chromium-review.googlesource.com/c/chromium/src/+/1877532 made ClipboardWriter garbage collected, but failed to reset the FileReaderLoader when the ClipboardWriter gets finalized. Either with a pre-finalizer or some more explicit abort hook for ClipboardWriter.

We really should make FileReaderLoader (or at least FileReaderLoaderClient) be garbage collected to avoid these bugs (I think I've fixed this exact issue at least twice before for other FileReaderLoaderClient implementations in the past; at the time I verified all other existing usage didn't have this problem, but that doesn't stop new problems from sneaking in).

+huangdarwin since the issue in this case is in the clipboard code

[Monorail components: Blink>DataTransfer]

### [Deleted User] (2020-10-27)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-27)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2020-10-28)

Re: https://crbug.com/chromium/1142331#c5: In the meantime, if making FileReaderLoader GC'ed might be complex, we could first fix the Clipboard implementation.

Could I see how you fixed this issue in the past? I see that the file_reader_ is reset() during DidFinishLoading()[1], but assume we're missing another reset, at least in DidFail(). Also, did you mean by "when the ClipboardWriter gets finalized"?

[1]: https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/modules/clipboard/clipboard_writer.cc;l=354;drc=c752526e8a29339257cbf2dd580218cb5e8cceab

### me...@chromium.org (2020-10-28)

https://chromium-review.googlesource.com/c/chromium/src/+/1374511 is one of these fixes I've done in the past. PS1 has the approach of using a pre-finalizer, and then I switched to instead clearing the loader when the ExecutionContext is destroyed. Not sure what the best option would be for ClipboardWriter. It seems ClipboardWriter is always owned by ClipboardPromise, but not clear to me what keeps ClipboardPromise alive while ClipboardWriter is reading the blob.
Adding a pre-finalizer would definitely fix the UAP, but there might be better options depending on how lifetime of a ClipboardPromise is defined (afaict nothing keeps the ClipboardPromise alive, but I might be missing something).

### hu...@chromium.org (2020-10-30)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0f6df4faf919a4c688803e727cb12f0bacea72e4

commit 0f6df4faf919a4c688803e727cb12f0bacea72e4
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Fri Nov 13 20:02:02 2020

Clipboard: Fix UaP in ClipboardWriter/FileReaderLoader.

Make ClipboardWriter keep FileReaderLoader alive until it's done reading
a Blob, by using SelfKeepAlive<T>.

Previously, ClipboardWriter could be garbage collected unexpectedly
(ex. when the frame detaches). This could cause a use after poison
in the FileReaderLoader, where:
(1) A ClipboardWriter's FileReaderLoader starts reading the input blob
    as an async task.
(2) The ClipboardWriter is destroyed (garbage collected).
(3) The FileReaderLoader completes its async task of reading the input
    blob, and calls ClipboardWriter::StartWrite on the destroyed, owning
    ClipboardWriter.

Additionally, add a "context destroyed" error message when a context
detaches.

Bug: 1142331
Change-Id: I427cd6dc02e773b2d235d45bd9ad8935b575ff71
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2509033
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#827371}

[modify] https://crrev.com/0f6df4faf919a4c688803e727cb12f0bacea72e4/third_party/blink/renderer/modules/clipboard/clipboard_promise.cc
[modify] https://crrev.com/0f6df4faf919a4c688803e727cb12f0bacea72e4/third_party/blink/renderer/modules/clipboard/clipboard_promise.h
[modify] https://crrev.com/0f6df4faf919a4c688803e727cb12f0bacea72e4/third_party/blink/renderer/modules/clipboard/clipboard_writer.cc
[modify] https://crrev.com/0f6df4faf919a4c688803e727cb12f0bacea72e4/third_party/blink/renderer/modules/clipboard/clipboard_writer.h
[add] https://crrev.com/0f6df4faf919a4c688803e727cb12f0bacea72e4/third_party/blink/web_tests/clipboard/async-clipboard/clipboard-garbage-collection-race-condition.html


### hu...@chromium.org (2020-11-13)

I guess Security_Severity-High implies we should merge-back. I'll ask for M87 mergeback but not M86 because I believe the final M86 branch has already happened (though I could certainly be wrong if yet another one comes up).

### [Deleted User] (2020-11-13)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2020-11-13)

1. Probably? This is a Security_Severity-High bug, and I suspect the change shouldn't be too risky and isn't too large, but 3 days from stable is a bit close. I can defer to security on this.
2. https://crrev.com/c/2536946
3. The change has landed, but we should wait "a few" days to make sure this is safe on canary. If we merge this, I think merging on Monday (the stable branch date) could be good, to have 2 days of canary data over the weekend.
4. No.
5. Security bug discovered after branch (from late 2019/early 2020).
6. No.
7. N/A

### [Deleted User] (2020-11-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-14)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-11-16)

Probably already be too late for M87 merge, but +adetaylor@ for heads up just in case this should still be merged.

### ad...@chromium.org (2020-11-16)

huangdarwin@ thanks. This is marked as Security_Impact-Head which means the problem didn't exist before M88. Is that wrong; is this a problem in M87?

### hu...@chromium.org (2020-11-17)

Per https://crbug.com/chromium/1142331#c5, this has existed since this CL[1][2], which was first merged in M81. Therefore, this should affect all milestones after M81 (except ToT which was just patched).

Thank you, I think I didn't consider the Security_Impact-Head label. I've relabelled this as Security_Impact-Stable. I've also updated the bug to add Target-87 and M-87 labels. Please let me know if this doesn't seem right.

[1]: https://crrev.com/c/1877532
[2]: https://chromiumdash.appspot.com/commit/1e1812f85d8cd9f6a19c6039aafe482e2bd3d967

### ad...@chromium.org (2020-11-17)

OK sounds good! In which case yes, we should merge this to one of the scheduled M87 security refreshes (we just missed initial release). I'll be approving merges in a day or two once the dust has settled on the initial release, and this should appear on my filters.

### ad...@google.com (2020-11-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-11-18)

Congratulations, the VRP panel has decided to award $5,000 for this bug. Someone from our finance team will get in touch.

How would you like to be credited in the Chrome release notes?



### wo...@gmail.com (2020-11-19)

Thank you for the reward.

> How would you like to be credited in the Chrome release notes?
Credit: Ryoya Tsukasaki


### ad...@chromium.org (2020-11-19)

Thank you!

### ad...@google.com (2020-11-19)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-19)

Approving merge to M87, branch 4280, assuming things are looking good in Canary.

### hu...@chromium.org (2020-11-19)

Thanks. Seems things are looking good in canary. (I haven't heard of any new crashes, and don't see any new clipboard bugs since this merged into ToT).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2412ef46369528a15cc7acc1b4fe9aa7d6915384

commit 2412ef46369528a15cc7acc1b4fe9aa7d6915384
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Fri Nov 20 04:31:58 2020

Clipboard: Fix UaP in ClipboardWriter/FileReaderLoader (M87).

Make ClipboardWriter keep FileReaderLoader alive until it's done reading
a Blob, by using SelfKeepAlive<T>.

Previously, ClipboardWriter could be garbage collected unexpectedly
(ex. when the frame detaches). This could cause a use after poison
in the FileReaderLoader, where:
(1) A ClipboardWriter's FileReaderLoader starts reading the input blob
    as an async task.
(2) The ClipboardWriter is destroyed (garbage collected).
(3) The FileReaderLoader completes its async task of reading the input
    blob, and calls ClipboardWriter::StartWrite on the destroyed, owning
    ClipboardWriter.

Additionally, add a "context destroyed" error message when a context
detaches.

TBR=mek@chromium.org
(cherry picked from commit 0f6df4faf919a4c688803e727cb12f0bacea72e4)

Bug: 1142331
Change-Id: I427cd6dc02e773b2d235d45bd9ad8935b575ff71
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2509033
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#827371}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2536946
Cr-Commit-Position: refs/branch-heads/4280@{#1475}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/2412ef46369528a15cc7acc1b4fe9aa7d6915384/third_party/blink/renderer/modules/clipboard/clipboard_promise.cc
[modify] https://crrev.com/2412ef46369528a15cc7acc1b4fe9aa7d6915384/third_party/blink/renderer/modules/clipboard/clipboard_promise.h
[modify] https://crrev.com/2412ef46369528a15cc7acc1b4fe9aa7d6915384/third_party/blink/renderer/modules/clipboard/clipboard_writer.cc
[modify] https://crrev.com/2412ef46369528a15cc7acc1b4fe9aa7d6915384/third_party/blink/renderer/modules/clipboard/clipboard_writer.h
[add] https://crrev.com/2412ef46369528a15cc7acc1b4fe9aa7d6915384/third_party/blink/web_tests/clipboard/async-clipboard/clipboard-garbage-collection-race-condition.html


### hu...@chromium.org (2020-11-20)

Oops, I just realized the ToT CL first hit M89, per https://chromiumdash.appspot.com/commit/0f6df4faf919a4c688803e727cb12f0bacea72e4

Therefore, requesting mergeback to M88 (we currently have this CL in M87 and M89, but not M88). This CL should be safe, per M88 merge review in https://crbug.com/chromium/1142331#c16.

### hu...@chromium.org (2020-11-20)

(requesting merge for https://crrev.com/c/2552756)

### ad...@chromium.org (2020-11-20)

Approving merge to M88, branch 4324. Good spot.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/eaf87a99b25e2f33d71a9422eb0517c9b72029bf

commit eaf87a99b25e2f33d71a9422eb0517c9b72029bf
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Fri Nov 20 22:07:11 2020

Clipboard: Fix UaP in ClipboardWriter/FileReaderLoader (M88).

Make ClipboardWriter keep FileReaderLoader alive until it's done reading
a Blob, by using SelfKeepAlive<T>.

Previously, ClipboardWriter could be garbage collected unexpectedly
(ex. when the frame detaches). This could cause a use after poison
in the FileReaderLoader, where:
(1) A ClipboardWriter's FileReaderLoader starts reading the input blob
    as an async task.
(2) The ClipboardWriter is destroyed (garbage collected).
(3) The FileReaderLoader completes its async task of reading the input
    blob, and calls ClipboardWriter::StartWrite on the destroyed, owning
    ClipboardWriter.

Additionally, add a "context destroyed" error message when a context
detaches.

TBR=mek@chromium.org
(cherry picked from commit 0f6df4faf919a4c688803e727cb12f0bacea72e4)

Bug: 1142331
Change-Id: I427cd6dc02e773b2d235d45bd9ad8935b575ff71
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2509033
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#827371}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2552756
Reviewed-by: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#209}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/eaf87a99b25e2f33d71a9422eb0517c9b72029bf/third_party/blink/renderer/modules/clipboard/clipboard_promise.cc
[modify] https://crrev.com/eaf87a99b25e2f33d71a9422eb0517c9b72029bf/third_party/blink/renderer/modules/clipboard/clipboard_promise.h
[modify] https://crrev.com/eaf87a99b25e2f33d71a9422eb0517c9b72029bf/third_party/blink/renderer/modules/clipboard/clipboard_writer.cc
[modify] https://crrev.com/eaf87a99b25e2f33d71a9422eb0517c9b72029bf/third_party/blink/renderer/modules/clipboard/clipboard_writer.h
[add] https://crrev.com/eaf87a99b25e2f33d71a9422eb0517c9b72029bf/third_party/blink/web_tests/clipboard/async-clipboard/clipboard-garbage-collection-race-condition.html


### ad...@google.com (2020-12-02)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-02)

[Empty comment from Monorail migration]

### as...@google.com (2020-12-08)

ketakid@, could you please take a look at the merge to LTS?

### ke...@google.com (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/75021a87d975b9b0d0bbe1cb7679c11c3de27388

commit 75021a87d975b9b0d0bbe1cb7679c11c3de27388
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Wed Dec 16 18:42:11 2020

Clipboard: Fix UaP in ClipboardWriter/FileReaderLoader.

Make ClipboardWriter keep FileReaderLoader alive until it's done reading
a Blob, by using SelfKeepAlive<T>.

Previously, ClipboardWriter could be garbage collected unexpectedly
(ex. when the frame detaches). This could cause a use after poison
in the FileReaderLoader, where:
(1) A ClipboardWriter's FileReaderLoader starts reading the input blob
    as an async task.
(2) The ClipboardWriter is destroyed (garbage collected).
(3) The FileReaderLoader completes its async task of reading the input
    blob, and calls ClipboardWriter::StartWrite on the destroyed, owning
    ClipboardWriter.

Additionally, add a "context destroyed" error message when a context
detaches.

(cherry picked from commit 0f6df4faf919a4c688803e727cb12f0bacea72e4)

Bug: 1142331
Change-Id: I427cd6dc02e773b2d235d45bd9ad8935b575ff71
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2509033
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#827371}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2587155
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1489}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/75021a87d975b9b0d0bbe1cb7679c11c3de27388/third_party/blink/renderer/modules/clipboard/clipboard_writer.cc
[modify] https://crrev.com/75021a87d975b9b0d0bbe1cb7679c11c3de27388/third_party/blink/renderer/modules/clipboard/clipboard_promise.cc
[modify] https://crrev.com/75021a87d975b9b0d0bbe1cb7679c11c3de27388/third_party/blink/renderer/modules/clipboard/clipboard_promise.h
[modify] https://crrev.com/75021a87d975b9b0d0bbe1cb7679c11c3de27388/third_party/blink/renderer/modules/clipboard/clipboard_writer.h
[add] https://crrev.com/75021a87d975b9b0d0bbe1cb7679c11c3de27388/third_party/blink/web_tests/clipboard/async-clipboard/clipboard-garbage-collection-race-condition.html


### [Deleted User] (2020-12-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-03-29)

work38thaxus@ - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1142331?no_tracker_redirect=1

[Multiple monorail components: Blink>DataTransfer, Blink>Storage>FileAPI]
[Monorail blocking: crbug.com/chromium/1144264]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053717)*
