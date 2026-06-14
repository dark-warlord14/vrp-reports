# Security: Heap-use-after-free in RuntimeCustomBindings::GetExtensionViews

| Field | Value |
|-------|-------|
| **Issue ID** | [40084207](https://issues.chromium.org/issues/40084207) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-04-29 |
| **Bounty** | $1,500.00 |

## Description

Chrome version: 50.0.2661.75

RuntimeCustomBindings::GetExtensionViews retrieves a vector of RenderFrame*s of the current extension, and stores each item in a v8::Array. But the extension can intercept the setter for a numeric index (e.g. 0), destroy the RenderFrame and cause a UAF. Oops.

To reproduce, just load the attached extension (manifest.json & background.js).
The extension does not need any permissions.

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 162 B)
- [background.js](attachments/background.js) (text/plain, 1.7 KB)
- [asan-uaf-getViews-50.0.2661.75.log](attachments/asan-uaf-getViews-50.0.2661.75.log) (text/plain, 27.7 KB)

## Timeline

### ro...@robwu.nl (2016-04-30)

Patch: https://codereview.chromium.org/1935953002/ (locally verified)

### rs...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-05-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/aa7a889002dd7a1288cc5e962086e517131fb01e

commit aa7a889002dd7a1288cc5e962086e517131fb01e
Author: rob <rob@robwu.nl>
Date: Mon May 02 16:18:37 2016

Create array of extension views without side effects

BUG=608104

Review-Url: https://codereview.chromium.org/1935953002
Cr-Commit-Position: refs/heads/master@{#390961}

[modify] https://crrev.com/aa7a889002dd7a1288cc5e962086e517131fb01e/extensions/renderer/runtime_custom_bindings.cc


### ro...@robwu.nl (2016-05-03)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-03)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### go...@chromium.org (2016-05-03)

Please merge your change to M51 branch 2704 by 4:00 PM PST today so we can take it for this week beta release tomorrow.Thank you.

### cl...@chromium.org (2016-05-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-05-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3d0effb3db93713cafeea3bc81231403b5cba018

commit 3d0effb3db93713cafeea3bc81231403b5cba018
Author: Rob Wu <rob@robwu.nl>
Date: Tue May 03 21:23:08 2016

Create array of extension views without side effects

BUG=608104

Review-Url: https://codereview.chromium.org/1935953002
Cr-Commit-Position: refs/heads/master@{#390961}
(cherry picked from commit aa7a889002dd7a1288cc5e962086e517131fb01e)

Review URL: https://codereview.chromium.org/1948773002 .

Cr-Commit-Position: refs/branch-heads/2704@{#362}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/3d0effb3db93713cafeea3bc81231403b5cba018/extensions/renderer/runtime_custom_bindings.cc


### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-05-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-31)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-06)

Updating severity.

### ti...@google.com (2016-06-06)

$1,500 here Rob ($1000 for the report, +$500 for the patch). Cheers as always!

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/608104?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084207)*
