# Use after free in SVGUseElement::buildShadowTree

| Field | Value |
|-------|-------|
| **Issue ID** | [40091635](https://issues.chromium.org/issues/40091635) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-06-07 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: stable, & daily  

Operating System: osx, linux

**REPRODUCTION CASE**  

<svg>  

<g>  

<use xlink:href="#g"/>  

</g>  

<g id="g">

<script>
document.body.innerText = "";
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

Address 0xf4ecb38 is 40 bytes inside a block of size 384 free'd  

Address 0x4141414141414571 is not stack'd, malloc'd or (recently) free'd  

at 0x183B1B0: WebCore::Node::dispatchSubtreeModifiedEvent() (Document.h:886)  

by 0x17F3B5D: WebCore::ContainerNode::appendChild

## Attachments

- [svgx.html](attachments/svgx.html) (text/plain; charset=us-ascii, 98 B)
- [vg-google-chrome.txt](attachments/vg-google-chrome.txt) (text/plain; charset=us-ascii, 7.2 KB)
- [vg-chromium-nightly.txt](attachments/vg-chromium-nightly.txt) (text/plain; charset=us-ascii, 19.8 KB)

## Timeline

### mi...@gmail.com (2011-06-07)

vg logs

### in...@chromium.org (2011-06-07)

Awesome bug miaubiz.

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=62225

Slightly more clear testcase::
<svg>
    <g>
        <use xlink:href="#test"/>
    </g>
    <rect id="test">
        <script>
            document.body.innerHTML = "PASS";
        </script>
    </rect>
</svg>

### in...@chromium.org (2011-06-07)

trying out a fix.

### in...@chromium.org (2011-06-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-10)

Committed r88549: <http://trac.webkit.org/changeset/88549>

We will merge to m12, m13 branches.

### in...@chromium.org (2011-06-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-11)

We should be uptaking fix from https://bugs.webkit.org/show_bug.cgi?id=62412 after the c#6 fix. This is a more proper fix as per Eric's comments.

### in...@chromium.org (2011-06-11)

lets just pick 88549 for now. the comprehensive fix in https://crbug.com/chromium/62412 has brought some crashes. http://build.webkit.org/results/SnowLeopard%20Intel%20Debug%20(Tests)/r88585%20(583)/results.html

### sc...@gmail.com (2011-06-14)

Merged 88549 to M12: http://trac.webkit.org/changeset/88836
and M13: http://trac.webkit.org/changeset/88837

### sc...@gmail.com (2011-06-16)

@miaubiz: Interesting bug. Seems almost too simple :P Nice small repro, clear $1000 reward case.

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

### mi...@gmail.com (2011-06-16)

@scarybeasts: I had this as a nullpointer and infinite recursion since december. but now it had become exploitable.  delightfully simple yes :)

### sc...@gmail.com (2011-07-03)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

### js...@chromium.org (2011-10-05)

Batch update.

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

This issue was migrated from crbug.com/chromium/85211?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091635)*
