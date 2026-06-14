# Table layout crash bug from wushi

| Field | Value |
|-------|-------|
| **Issue ID** | [40080718](https://issues.chromium.org/issues/40080718) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sc...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2010-04-28 |
| **Bounty** | $500.00 |

## Description

Reproduces for me with attached repro.

Analysis
--------

WebKit/WebCore/rendering/FixedTableLayout.cpp

                int usedSpan = 0;
                int i = 0;
                while (usedSpan < span) {
                    //ASSERT(cCol + i < nEffCols);
                    int eSpan = m_table->spanOfEffCol(cCol + i);
                    // Only set if no col element has already set it.
                    if (m_width[cCol + i].isAuto() && w.type() != Auto) {
                        m_width[cCol + i].setRawValue(w.type(), 
w.rawValue() * eSpan / span);
                        usedWidth += effWidth * eSpan / span;
                    }
                    usedSpan += eSpan;
                    i++;
                }

The repro causes "i" to go large and out-of-bounds.
A debug build will crash on the ASSERT() that I commented out.
An optimized build will typically crash due to an out-of-bounds array read 
due to the large "i" value.

Note that isAuto() and setRawValue() are non-virtual, otherwise this would 
be clearly exploitable due to using an out-of-bounds vtable.

setRawValue() is under some conditions writing out-of-bounds to an array so 
this is still likely exploitable. Assigning SecSeverity-High out of an 
abundance of caution.


## Attachments

- [test0.xhtml](attachments/test0.xhtml) (text/html, 526 B)

## Timeline

### sc...@gmail.com (2010-04-28)

WebKit bug https://bugs.webkit.org/show_bug.cgi?id=38261

### in...@chromium.org (2010-04-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-05-14)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-05-14)

Committed r59495: <http://trac.webkit.org/changeset/59495>

Let it bake on dev channel for a week before merging to v5 stable. will probably go
in the first v5 patch.


### sc...@gmail.com (2010-05-21)

Another reward for Wushi :)

### in...@chromium.org (2010-05-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-05-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-05-24)

Bugdroid will be started soon by Mark (it was down), till then i have manually put
the comments here.

Merge 59495 - 20100514 Abhishek Arya <inferno@chromium.org>

Reviewed by David Hyatt.

Tests that large colspan in a fixed table layout does not result in crash.
https://bugs.webkit.org/show_bug.cgi?id=38261

* fast/table/fixedtablelayoutlargecolspancrashexpected.txt: Added.
* fast/table/fixedtablelayoutlargecolspancrash.html: Added.
20100514 Abhishek Arya <inferno@chromium.org>

Reviewed by David Hyatt.

Move the m_width(Length) and m_columns(RenderTable::ColumnStruct)
vector outofbounds check out of the ASSERT into the main code.
https://bugs.webkit.org/show_bug.cgi?id=38261

Test: fast/table/fixedtablelayoutlargecolspancrash.html

* rendering/FixedTableLayout.cpp:
(WebCore::FixedTableLayout::calcWidthArray):

BUG=42723
TBR=eric@webkit.org

Committed: http://src.chromium.org/viewvc/chrome?view=rev&revision=48059

### bu...@gmail.com (2010-05-24)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=48059 

------------------------------------------------------------------------
r48059 | inferno@chromium.org | 2010-05-24 11:26:34 -0700 (Mon, 24 May 2010) | 25 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/ChangeLog?r1=48059&r2=48058
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/table/fixed-table-layout-large-colspan-crash-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/table/fixed-table-layout-large-colspan-crash.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/ChangeLog?r1=48059&r2=48058
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/rendering/FixedTableLayout.cpp?r1=48059&r2=48058

Merge 59495 - 20100514  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Tests that large colspan in a fixed table layout does not result in crash.
        https://bugs.webkit.org/show_bug.cgi?id=38261

        * fast/table/fixedtablelayoutlargecolspancrashexpected.txt: Added.
        * fast/table/fixedtablelayoutlargecolspancrash.html: Added.
20100514  Abhishek Arya  <inferno@chromium.org>

        Reviewed by David Hyatt.

        Move the m_width(Length) and m_columns(RenderTable::ColumnStruct)
        vector outofbounds check out of the ASSERT into the main code.
        https://bugs.webkit.org/show_bug.cgi?id=38261

        Test: fast/table/fixedtablelayoutlargecolspancrash.html

        * rendering/FixedTableLayout.cpp:
        (WebCore::FixedTableLayout::calcWidthArray):

BUG=42723
TBR=eric@webkit.org
Review URL: http://codereview.chromium.org/2171002
------------------------------------------------------------------------


### sc...@gmail.com (2010-06-11)

Fixed in 5.0.375.70

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/42723?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080718)*
