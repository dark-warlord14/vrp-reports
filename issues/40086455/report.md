# Security: Use after free in PDFium's Annot::name

| Field | Value |
|-------|-------|
| **Issue ID** | [40086455](https://issues.chromium.org/issues/40086455) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | [Deleted User] |
| **Assignee** | ts...@chromium.org |
| **Created** | 2017-01-10 |
| **Bounty** | $3,500.00 |

## Description

*No description available.*

## Timeline

### ts...@chromium.org (2017-01-12)

Requires XFA as in https://crbug.com/chromium/679642, so shipping chromium not affected.

### ts...@chromium.org (2017-01-12)

https://pdfium.googlesource.com/pdfium/+/192497124e7cde747ade7bf89028586eea293be5

### ts...@chromium.org (2017-01-12)

VRP: same caveats as in 679642, impact none only since we don't ship XFA.

### bu...@chromium.org (2017-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/34ff66f6a7ed64c19c9494b0327a7a4037b7b2ff

commit 34ff66f6a7ed64c19c9494b0327a7a4037b7b2ff
Author: pdfium-deps-roller <pdfium-deps-roller@chromium.org>
Date: Thu Jan 12 22:28:15 2017

Roll src/third_party/pdfium/ db7647083..98d00b230 (4 commits).

https://pdfium.googlesource.com/pdfium.git/+log/db7647083d0a..98d00b230aa1

$ git log db7647083..98d00b230 --date=short --no-merges --format='%ad %ae %s'
2017-01-12 dsinclair Remove used items from the CSS code.
2017-01-12 tsepez Don't put timers with ID == 0 into the global timer map.
2017-01-12 tsepez Custom toString() methods may delete annots.
2017-01-12 npm Fix leak in OJPEGReadHeaderInfoSecTablesAcTable when read fails.

BUG=679649,679643,680520

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls

TBR=dsinclair@chromium.org

Review-Url: https://codereview.chromium.org/2627073004
Cr-Commit-Position: refs/heads/master@{#443386}

[modify] https://crrev.com/34ff66f6a7ed64c19c9494b0327a7a4037b7b2ff/DEPS


### sh...@chromium.org (2017-01-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-23)

The panel awarded $3,500 for this one!  Thanks!

### th...@chromium.org (2017-02-24)

Should we add reward-3500 and other rewards related labels?

[Monorail components: Internals>Plugins>PDF]

### aw...@chromium.org (2017-03-13)

Added! Note that the reward amount the panel decided upon was $3,000, but VRP error in your favour...!

### sh...@chromium.org (2017-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-10-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### is...@google.com (2017-10-06)

This issue was migrated from crbug.com/chromium/679643?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086455)*
