# Use after free in FocusController::advanceFocusInDocumentOrder

| Field | Value |
|-------|-------|
| **Issue ID** | [40094108](https://issues.chromium.org/issues/40094108) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-08-18 |
| **Bounty** | $1,000.00 |

## Description

!!!  

you have to press a key when the page loads up  

!!!

**VULNERABILITY DETAILS**  

use-after-free

**VERSION**  

Chrome Version: stable + trunk  

Operating System: linux 64bit

**REPRODUCTION CASE**  

attached

you have to press a key in the focused text field!

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan/vg  

Crash State:

==28518== ERROR: AddressSanitizer crashed on address 0x00007fffe50d10f8 at pc 0x7ffff49e319e bp 0x7fffffff6220 sp 0x7fffffff5f20  

READ of size 8 at 0x00007fffe50d10f8 thread T0  

#0 0x7ffff49e319e in WebCore::FocusController::advanceFocusInDocumentOrder(WebCore::FocusDirection, WebCore::KeyboardEvent\*, bool) ???:0

0x00007fffe50d10f8 is located 120 bytes inside of 240-byte region [0x00007fffe50d1080,0x00007fffe50d1170)  

freed by thread T0 here:  

#0 0x7ffff6c8ef82 in operator delete(void\*) *asan\_rtl*  

#1 0x7ffff3bef8d9 in WebCore::ContainerNode::removeChildren() ???:0

previously allocated by thread T0 here:  

#0 0x7ffff6c8f34a in operator new(unsigned long) *asan\_rtl*  

#1 0x7ffff68ee09e in WebCore::HTMLIFrameElement::create(WebCore::QualifiedName const&, WebCore::Document\*) ???:0

## Attachments

- [valgrind.txt](attachments/valgrind.txt) (text/plain; charset=us-ascii, 16.6 KB)
- [asan-symbols.txt](attachments/asan-symbols.txt) (text/plain; charset=us-ascii, 8.8 KB)
- [120_24o.html](attachments/120_24o.html) (text/plain; charset=us-ascii, 412 B)

## Timeline

### kc...@chromium.org (2011-08-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-08-22)

Awesome bug. One keypress is not that hard to get.

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=66678

### in...@chromium.org (2011-08-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-08-22)

http://trac.webkit.org/changeset/93514

### sc...@gmail.com (2011-08-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-24)

Merged to M14: http://trac.webkit.org/changeset/93694

### sc...@gmail.com (2011-08-24)

@miaubiz: nice bug. Good for a $1000 reward.

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

### sc...@gmail.com (2011-08-24)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/93420?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094108)*
