# Regression(82144): OOB InlineIterator read in TrailingObjects::updateMidpointsForTrailingBoxes

| Field | Value |
|-------|-------|
| **Issue ID** | [40092893](https://issues.chromium.org/issues/40092893) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-07-21 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

READ of size 4 at 0x00007fffbea36cf8 thread T0  

#0 0x7ffff515b0a4 in WebCore::TrailingObjects::updateMidpointsForTrailingBoxes(WebCore::MidpointState[WebCore::InlineIterator](javascript:void(0);)&,  

0x00007fffbea36cf8 is located 8 bytes to the left of 384-byte region [0x00007fffbea36d00,0x00007fffbea36e80)

**VERSION**  

Chrome Version: stable + trunk  

Operating System: linux 64bit

**REPRODUCTION CASE**  

attached

## Attachments

- [8totheleft.html](attachments/8totheleft.html) (text/plain; charset=us-ascii, 210 B)
- [asan-symbols.txt](attachments/asan-symbols.txt) (text/plain; charset=us-ascii, 8.1 KB)
- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 6.1 KB)
- [google-chrome-vg.txt](attachments/google-chrome-vg.txt) (text/plain; charset=us-ascii, 3.1 KB)
- [8totheleft720.html](attachments/8totheleft720.html) (text/x-asm; charset=us-ascii, 38.3 KB)
- [asan-symbols-8-to-the-left-720.txt](attachments/asan-symbols-8-to-the-left-720.txt) (text/plain; charset=us-ascii, 9.1 KB)

## Timeline

### mi...@gmail.com (2011-07-22)

here's another, with 8 to the left of 720 byte region.

### kc...@chromium.org (2011-07-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-07-22)

Awesome miaubiz, you are on fire. You can go more creative with bug title :)

### in...@chromium.org (2011-07-25)

https://bugs.webkit.org/show_bug.cgi?id=65137

### in...@chromium.org (2011-07-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-08-01)

http://trac.webkit.org/changeset/92132

### in...@chromium.org (2011-08-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-22)

Merged to M14: http://trac.webkit.org/changeset/93496

### sc...@gmail.com (2011-08-24)

@miaubiz: interesting bug. We don't think the OOB content (off-by-one?) can be recovered by script, but why not pay you a $500 reward out of an abundance of caution? :)

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-23)

Payment in system.

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/89991?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092893)*
