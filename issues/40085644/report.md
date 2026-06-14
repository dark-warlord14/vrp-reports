# Security: PDFs can navigate to file:-URLs

| Field | Value |
|-------|-------|
| **Issue ID** | [40085644](https://issues.chromium.org/issues/40085644) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | ro...@robwu.nl |
| **Created** | 2016-10-09 |
| **Bounty** | $1,000.00 |

## Description

Chrome version: 53.0.2785.116 (stable) and latest (56.0.2886.0).

1. Open attached PDF.
2. Ctrl-click on the PDF file (middle-mouse and shift also work in Chrome 54 onwards thanks to https://crbug.com/chromium/630075).
3. Observe that file:///tmp/ is being opened (as an example).

This is like https://crbug.com/chromium/533520, except with key modifiers.

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 638 B)

## Timeline

### ro...@robwu.nl (2016-10-09)

Patch: https://codereview.chromium.org/2402873002

### ts...@chromium.org (2016-10-10)

Severity medium per previous bug with these consequences.

### th...@chromium.org (2016-10-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/374249e767a68d8da073a4ed3a4f29236451174c

commit 374249e767a68d8da073a4ed3a4f29236451174c
Author: rob <rob@robwu.nl>
Date: Fri Oct 14 10:13:14 2016

Add check for file:-navigations from PDFs

BUG=654279
TEST=./browser_tests --gtest_filter=PDFExtensionTest.Navigator
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2402873002
Cr-Commit-Position: refs/heads/master@{#425287}

[modify] https://crrev.com/374249e767a68d8da073a4ed3a4f29236451174c/chrome/browser/resources/pdf/navigator.js
[modify] https://crrev.com/374249e767a68d8da073a4ed3a4f29236451174c/chrome/browser/resources/pdf/pdf.js
[modify] https://crrev.com/374249e767a68d8da073a4ed3a4f29236451174c/chrome/test/data/pdf/navigator_test.js


### th...@chromium.org (2016-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-15)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-10-17)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-10-17)

Your change meets the bar and is auto-approved for M55 (branch: 2883)

### bu...@chromium.org (2016-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c337558010508f6e27594e2683ddcf2f8813fc89

commit c337558010508f6e27594e2683ddcf2f8813fc89
Author: Rob Wu <rob@robwu.nl>
Date: Mon Oct 17 11:54:00 2016

Add check for file:-navigations from PDFs

BUG=654279
TEST=./browser_tests --gtest_filter=PDFExtensionTest.Navigator
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2402873002
Cr-Commit-Position: refs/heads/master@{#425287}
(cherry picked from commit 374249e767a68d8da073a4ed3a4f29236451174c)

Review URL: https://codereview.chromium.org/2424783002 .

Cr-Commit-Position: refs/branch-heads/2883@{#146}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/c337558010508f6e27594e2683ddcf2f8813fc89/chrome/browser/resources/pdf/navigator.js
[modify] https://crrev.com/c337558010508f6e27594e2683ddcf2f8813fc89/chrome/browser/resources/pdf/pdf.js
[modify] https://crrev.com/c337558010508f6e27594e2683ddcf2f8813fc89/chrome/test/data/pdf/navigator_test.js


### aw...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-27)

$1,000 for this report - many thanks!

### bu...@chromium.org (2016-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c337558010508f6e27594e2683ddcf2f8813fc89

commit c337558010508f6e27594e2683ddcf2f8813fc89
Author: Rob Wu <rob@robwu.nl>
Date: Mon Oct 17 11:54:00 2016

Add check for file:-navigations from PDFs

BUG=654279
TEST=./browser_tests --gtest_filter=PDFExtensionTest.Navigator
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2402873002
Cr-Commit-Position: refs/heads/master@{#425287}
(cherry picked from commit 374249e767a68d8da073a4ed3a4f29236451174c)

Review URL: https://codereview.chromium.org/2424783002 .

Cr-Commit-Position: refs/branch-heads/2883@{#146}
Cr-Branched-From: 614d31daee2f61b0180df403a8ad43f20b9f6dd7-refs/heads/master@{#423768}

[modify] https://crrev.com/c337558010508f6e27594e2683ddcf2f8813fc89/chrome/browser/resources/pdf/navigator.js
[modify] https://crrev.com/c337558010508f6e27594e2683ddcf2f8813fc89/chrome/browser/resources/pdf/pdf.js
[modify] https://crrev.com/c337558010508f6e27594e2683ddcf2f8813fc89/chrome/test/data/pdf/navigator_test.js


### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-11-01)

(not merged, budroid comment is wrong - https://groups.google.com/a/chromium.org/d/msg/chromium-dev/sJ7gZLqyJ-g/k-CbRUrnBwAJ)

### aw...@chromium.org (2016-11-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-11-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/654279?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085644)*
