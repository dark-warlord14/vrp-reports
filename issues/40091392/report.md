# use-after-free in svg fontfacelement

| Field | Value |
|-------|-------|
| **Issue ID** | [40091392](https://issues.chromium.org/issues/40091392) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-05-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in svg fontfaceelement,

n.b. I can only reproduce this 2 ways:

1. in linux when I disable tcmalloc with:  
   
   build/gyp\_chromium -Dlinux\_use\_tcmalloc=0
2. in valgrind, where it affects also google chrome stable version.

valgrind gives the same results on non-tcmalloc chromium trunk, google chrome 11 stable, and regular tcm ubuntu chromium daily

**VERSION**  

Chrome Version: trunk with tcmalloc turned off :D  

Operating System: Linux 2.6.38-9-generic #43-Ubuntu SMP Thu Apr 28 15:23:06 UTC 2011 x86\_64

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

Address 0x36bad2b8 is 88 bytes inside a block of size 1,424 free'd  

Address 0x7d7d7d7d7d7d7d41 is not stack'd, malloc'd or (recently) free'd  

at 0x125C916: WebCore::CSSStyleSelector::popParent(WebCore::Element\*)

## Attachments

- [svgf.html](attachments/svgf.html) (text/plain; charset=us-ascii, 311 B)
- [vg-84355-chrome-stable.txt](attachments/vg-84355-chrome-stable.txt) (text/plain; charset=us-ascii, 11.0 KB)
- [vg-84355-chromium.txt](attachments/vg-84355-chromium.txt) (text/x-c; charset=us-ascii, 22.3 KB)

## Timeline

### mi...@gmail.com (2011-05-29)

vg logs for chromium daily and google chrome stable

### in...@chromium.org (2011-05-29)

Thanks miaubiz for continued awesomeness.

### in...@chromium.org (2011-05-30)

filed https://bugs.webkit.org/show_bug.cgi?id=61737. This bug got introduced in http://trac.webkit.org/changeset/77740, so affects our stable channels too.

### in...@chromium.org (2011-06-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-01)

Fixed in http://trac.webkit.org/changeset/87827

### sc...@gmail.com (2011-06-14)

Merged to M12: http://trac.webkit.org/changeset/88758
Merged to M13: http://trac.webkit.org/changeset/88759

### sc...@gmail.com (2011-06-16)

@miaubiz: thanks, $1000 for this one, nice report.

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

### sc...@gmail.com (2011-07-03)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.
(Paid out all the other bugs present in the Chrome 12 security patch too, I will only send the one e-mail).

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

This issue was migrated from crbug.com/chromium/84355?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091392)*
