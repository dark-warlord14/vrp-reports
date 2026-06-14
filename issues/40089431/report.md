# Security: OOB Read in BlobStorageContext::BlobFlattener::BlobFlattener

| Field | Value |
|-------|-------|
| **Issue ID** | [40089431](https://issues.chromium.org/issues/40089431) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2017-10-28 |
| **Bounty** | $2,500.00 |

## Description

VULNERABILITY DETAILS
In storage/browser/blob/blob_storage_context.cc,
BlobStorageContext::BlobFlattener::BlobFlattener
is used to flatten blob slices.

The renderer supplied bounds for the slice are validated as follows:
```
// Validate our reference has good offset & length.
if (input_element.offset() + length > ref_entry->total_size()) {
  status = BlobStatus::ERR_INVALID_CONSTRUCTION_ARGUMENTS;
  return;
}
```

But offset + length itself is not checked for overflow, so a small
negative number can be provided for the offset and the attacker can
read arbitrarily many bytes before the start of the blob in the
browser.

When combined with crbug.com/777728, a full sandbox escape can be achieved.

VERSION
Chrome Version: 62 Stable
Operating System: All

REPRODUCTION CASE
Apply renderer.patch and open index.html in Chrome. A unit test and fix are attached.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: Browser
Crash State: See asan.log.


## Attachments

- [fix.patch](attachments/fix.patch) (application/octet-stream, 1.8 KB)
- [asan.log](attachments/asan.log) (text/plain, 31.9 KB)
- [renderer.patch](attachments/renderer.patch) (application/octet-stream, 676 B)
- [index.html](attachments/index.html) (text/plain, 167 B)

## Timeline

### el...@chromium.org (2017-10-28)

Thanks for the bug and patch!

[Monorail components: Blink>Storage]

### mb...@chromium.org (2017-10-30)

dmurph: Would you mind taking a look?

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/11bd4bc92f3fe704631e3e6ad1dd1a4351641f7c

commit 11bd4bc92f3fe704631e3e6ad1dd1a4351641f7c
Author: Daniel Murphy <dmurph@chromium.org>
Date: Tue Oct 31 22:21:31 2017

[BlobStorage] Fixing potential overflow

Bug: 779314
Change-Id: I74612639d20544e4c12230569c7b88fbe669ec03
Reviewed-on: https://chromium-review.googlesource.com/747725
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/heads/master@{#512977}
[modify] https://crrev.com/11bd4bc92f3fe704631e3e6ad1dd1a4351641f7c/storage/browser/blob/blob_storage_context.cc
[modify] https://crrev.com/11bd4bc92f3fe704631e3e6ad1dd1a4351641f7c/storage/browser/blob/blob_storage_context_unittest.cc


### dm...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### dm...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-10-31)

Can you please mark which OS this impacts?

### dm...@chromium.org (2017-10-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-31)

This bug requires manual review: M63 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-11-01)

+awhalley@ for merge review

### sh...@chromium.org (2017-11-01)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-11-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-03)

@govind - good for M63.

### go...@chromium.org (2017-11-03)

Approving merge to M63 branch 3239 based on https://crbug.com/chromium/779314#c13. Please merge ASAP. Thank you.

### go...@chromium.org (2017-11-03)

Please merge your change M63 branch 3239 by 4:00 PM PT Monday (11/06/17) so we can take it for next week Beta release. Thank you.

### bu...@chromium.org (2017-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fbf7d5393b3765c03348ce466c7ad935eeb887f0

commit fbf7d5393b3765c03348ce466c7ad935eeb887f0
Author: Daniel Murphy <dmurph@chromium.org>
Date: Fri Nov 03 18:38:29 2017

[BlobStorage] Fixing potential overflow

Bug: 779314
Change-Id: I74612639d20544e4c12230569c7b88fbe669ec03
Reviewed-on: https://chromium-review.googlesource.com/747725
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#512977}(cherry picked from commit 11bd4bc92f3fe704631e3e6ad1dd1a4351641f7c)
Reviewed-on: https://chromium-review.googlesource.com/754084
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/3239@{#367}
Cr-Branched-From: adb61db19020ed8ecee5e91b1a0ea4c924ae2988-refs/heads/master@{#508578}
[modify] https://crrev.com/fbf7d5393b3765c03348ce466c7ad935eeb887f0/storage/browser/blob/blob_storage_context.cc
[modify] https://crrev.com/fbf7d5393b3765c03348ce466c7ad935eeb887f0/storage/browser/blob/blob_storage_context_unittest.cc


### mm...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-11-09)

Nice one! $2,500 for this report - cheers!

### aw...@chromium.org (2017-11-10)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/779314?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089431)*
