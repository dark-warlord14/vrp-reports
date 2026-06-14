# UAP in blink::FileReaderLoader::OnStartLoading

| Field | Value |
|-------|-------|
| **Issue ID** | [40093382](https://issues.chromium.org/issues/40093382) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileAPI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cd...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2018-12-11 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36

Steps to reproduce the problem:
1. Install Node.js include npm and express(cuz there is a node webserver)
2. Make a dirctory named "htm" in the same dir with sw.js and put crash.html and other resource files into the "htm" dir.
3. Run node ws.js and,if every thing setting up correctly,nothing will echo from console.
4.Download latest chromium asan build. asan-linux-release-613801 tested to be fine.
5.Run ./chrome http://127.0.0.1:8605/crash.html

What is the expected behavior?

What went wrong?
Can stably get UAP crash.Sees in asan.log

Did this work before? N/A 

Chrome version: 73.0.3631.0  Channel: n/a
OS Version: 16.04
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### ca...@chromium.org (2018-12-11)

Thanks for the report, marking as high severity since this looks like memory corruption in the renderer process.

mek: Assigning to you from the owners' file, and from (relatively) recent activity, can you please take a look (and reassign if appropriate?). Thanks.

[Monorail components: Blink>Storage>FileAPI]

### me...@chromium.org (2018-12-12)

https://chromium-review.googlesource.com/c/chromium/src/+/1374511

### bu...@chromium.org (2018-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/419c4bfbfb94849ed30dcab7c3aaf67afe238b27

commit 419c4bfbfb94849ed30dcab7c3aaf67afe238b27
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Thu Dec 13 17:09:55 2018

Fix UAP in ImageBitmapLoader/FileReaderLoader

FileReaderLoader stores its client as a raw pointer, so in cases like
ImageBitmapLoader where the FileReaderLoaderClient really is garbage
collected we have to make sure to destroy the FileReaderLoader when
the ExecutionContext that owns it is destroyed.

Bug: 913970
Change-Id: I40b02115367cf7bf5bbbbb8e9b57874d2510f861
Reviewed-on: https://chromium-review.googlesource.com/c/1374511
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#616342}
[modify] https://crrev.com/419c4bfbfb94849ed30dcab7c3aaf67afe238b27/third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.cc
[modify] https://crrev.com/419c4bfbfb94849ed30dcab7c3aaf67afe238b27/third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.h


### me...@chromium.org (2018-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-14)

This bug requires manual review: M72 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-12-14)

@govind - good for 72

### go...@chromium.org (2018-12-14)

Approving merge to M72 branch 3626 based on https://crbug.com/chromium/913970#c6. Please merge ASAP. Thank you.

### bu...@chromium.org (2018-12-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2cc08a407575bc8f4854db61cf1eae60ee7f6456

commit 2cc08a407575bc8f4854db61cf1eae60ee7f6456
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Fri Dec 14 21:59:33 2018

Fix UAP in ImageBitmapLoader/FileReaderLoader

FileReaderLoader stores its client as a raw pointer, so in cases like
ImageBitmapLoader where the FileReaderLoaderClient really is garbage
collected we have to make sure to destroy the FileReaderLoader when
the ExecutionContext that owns it is destroyed.

TBR=mek@chromium.org

(cherry picked from commit 419c4bfbfb94849ed30dcab7c3aaf67afe238b27)

Bug: 913970
Change-Id: I40b02115367cf7bf5bbbbb8e9b57874d2510f861
Reviewed-on: https://chromium-review.googlesource.com/c/1374511
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#616342}
Reviewed-on: https://chromium-review.googlesource.com/c/1379106
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#368}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}
[modify] https://crrev.com/2cc08a407575bc8f4854db61cf1eae60ee7f6456/third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.cc
[modify] https://crrev.com/2cc08a407575bc8f4854db61cf1eae60ee7f6456/third_party/blink/renderer/core/imagebitmap/image_bitmap_factories.h


### sh...@chromium.org (2018-12-15)

[Empty comment from Monorail migration]

### na...@google.com (2018-12-17)

[Empty comment from Monorail migration]

### cr...@appspot.gserviceaccount.com (2018-12-19)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/2cc08a407575bc8f4854db61cf1eae60ee7f6456

Commit: 2cc08a407575bc8f4854db61cf1eae60ee7f6456
Author: mek@chromium.org
Commiter: mek@chromium.org
Date: 2018-12-14 21:59:33 +0000 UTC

Fix UAP in ImageBitmapLoader/FileReaderLoader

FileReaderLoader stores its client as a raw pointer, so in cases like
ImageBitmapLoader where the FileReaderLoaderClient really is garbage
collected we have to make sure to destroy the FileReaderLoader when
the ExecutionContext that owns it is destroyed.

TBR=mek@chromium.org

(cherry picked from commit 419c4bfbfb94849ed30dcab7c3aaf67afe238b27)

Bug: 913970
Change-Id: I40b02115367cf7bf5bbbbb8e9b57874d2510f861
Reviewed-on: https://chromium-review.googlesource.com/c/1374511
Reviewed-by: Jeremy Roman <jbroman@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#616342}
Reviewed-on: https://chromium-review.googlesource.com/c/1379106
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/3626@{#368}
Cr-Branched-From: d897fb137fbaaa9355c0c93124cc048824eb1e65-refs/heads/master@{#612437}

### na...@google.com (2018-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2018-12-20)

Thanks for your report. The panel has decided to reward $3,000 :) 

### cd...@gmail.com (2018-12-20)

Thanks a lot for the reward!

### na...@google.com (2018-12-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-01-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-10-30)

[Empty comment from Monorail migration]

### is...@google.com (2020-10-30)

This issue was migrated from crbug.com/chromium/913970?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1144264]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093382)*
