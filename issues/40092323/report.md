# Use after free in range extract contents

| Field | Value |
|-------|-------|
| **Issue ID** | [40092323](https://issues.chromium.org/issues/40092323) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-06-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free

**VERSION**  

Chrome Version: stable + trunk  

Operating System: linux 64bit

vg/asan seems to be required

wouldn't crash on canary on windows :(

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan/vg  

Crash State:  

Address 0xf4b6e30 is 48 bytes inside a block of size 120 free'd  

Address 0x4141414141414171 is not stack'd, malloc'd or (recently) free'd  

at 0x1952070: WebCore::Node::nodeIndex() const (Node.cpp:2844)

0x00007fffbeafe748 is located 72 bytes inside of 120-byte region [0x00007fffbeafe700,0x00007fffbeafe778)

I couldn't get asan to show symbols even though the binary takes 3 gigs and ASAN\_OPTIONS is unset. sorry.

## Attachments

- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 12.5 KB)
- [nodeIndex72inside120.html](attachments/nodeIndex72inside120.html) (text/html; charset=us-ascii, 423 B)
- [asan.txt](attachments/asan.txt) (text/plain; charset=us-ascii, 3.8 KB)

## Timeline

### [Deleted User] (2011-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2011-06-29)

Filed upstream at https://bugs.webkit.org/show_bug.cgi?id=63650

### in...@chromium.org (2011-06-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-29)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-30)

http://trac.webkit.org/changeset/90130

### sc...@gmail.com (2011-06-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-07-12)

Merged to M13: http://trac.webkit.org/changeset/90845

### sc...@gmail.com (2011-07-20)

$1000

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-09)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/87925?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092323)*
