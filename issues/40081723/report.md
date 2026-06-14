# Flash: out-of-bounds write in shader handling

| Field | Value |
|-------|-------|
| **Issue ID** | [40081723](https://issues.chromium.org/issues/40081723) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | sc...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-03-26 |
| **Bounty** | $3,000.00 |

## Description

[Copying from https://code.google.com/p/google-security-research/issues/detail?id=239]

Credit is to "Jihui Lu of KeenTeam (@K33nTeam), working with the Chromium vulnerability reward program"

Flash Player 16.0.0.296 in Chrome 40 Linux x64

Crashes are all over the place, due to heap corruption. Attaching 4 PoCs although I believe they are all the same root cause.

## Attachments

- [PBJ2.swf](attachments/PBJ2.swf) (application/octet-stream, 1.2 KB)
- [PBJ3.swf](attachments/PBJ3.swf) (application/octet-stream, 1.3 KB)
- [PBJ1.swf](attachments/PBJ1.swf) (application/octet-stream, 1.3 KB)
- [PBJ4.swf](attachments/PBJ4.swf) (application/octet-stream, 1.2 KB)

## Timeline

### [Deleted User] (2015-05-01)

Fixed: https://helpx.adobe.com/security/products/flash-player/apsb15-06.html

### [Deleted User] (2015-05-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-04)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sc...@gmail.com (2015-05-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-08)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-17)

Jihui Lu: $3,000 for this report.

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/470753?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081723)*
