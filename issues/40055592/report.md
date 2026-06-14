# Heap-use-after-free in WebCore::ContainerNode::resumePostAttachCallbacks

| Field | Value |
|-------|-------|
| **Issue ID** | [40055592](https://issues.chromium.org/issues/40055592) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-03-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free with input that overwrites document element contents during focus

**VERSION**  

Chrome Version: stable, beta, dev

Chromium 19.0.1081.0 (Developer Build 128813)  

OS Linux  

WebKit 536.4 (@111994)

Operating System: 64 bit linux

**REPRODUCTION CASE**

<html>
<body>
<object data="a">
<input autofocus="" onfocus="document.documentElement.textContent = 'A'"/>
</object>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==22166== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffecaac8a8 at pc 0x555559231f56 bp 0x7fffffff9930 sp 0x7fffffff9928  

READ of size 8 at 0x7fffecaac8a8 thread T0  

#0 0x555559231f56 in WebCore::ContainerNode::resumePostAttachCallbacks() ???:0  

#1 0x5555592c11a4 in WebCore::Element::attach() ???:0  

#2 0x55555a44d40d in WebCore::FrameLoader::receivedMainResourceError(WebCore::ResourceError const&, bool) ???:0

0x7fffecaac8a8 is located 40 bytes inside of 224-byte region [0x7fffecaac880,0x7fffecaac960)  

freed by thread T0 here:  

#0 0x55555de945f2 in operator delete(void\*) ??:0  

#1 0x555559235f7d in WTF::Vector<std::pair<void (\*)(WebCore::Node\*, unsigned int), std::pair<WTF::RefPtr[WebCore::Node](javascript:void(0);), unsigned int> >, 0ul>::shrinkCapacity(unsigned long) ???:0  

#2 0x555559231e3b in WebCore::ContainerNode::resumePostAttachCallbacks() ???:0

## Attachments

- [stable-40224.txt](attachments/stable-40224.txt) (text/x-c; charset=us-ascii, 9.5 KB)
- [beta-40224.txt](attachments/beta-40224.txt) (text/x-c; charset=us-ascii, 10.1 KB)
- [40224.html](attachments/40224.html) (text/html; charset=us-ascii, 152 B)
- 40224.html (text/html; charset=us-ascii, 152 B)

## Timeline

### in...@chromium.org (2012-03-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=30309630

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7fdc0dfca4a8
Crash State:
  - crash stack -
  WebCore::ContainerNode::resumePostAttachCallbacks
  WebCore::Element::attach
  - free stack -
  WTF::Vector<std::pair<void 
  WebCore::ContainerNode::resumePostAttachCallbacks
  

Minimized Testcase (0.10 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94qPqi-K0aAgt2GZVmiBoCHgwriEyh6xub3FTfntVZ8dwa4Qj8DtdbL5Fb5lZBUFekKBbqUbt1cOLLWC1Mu7CQt7oVGaCsKP3VSx2W-SUnF8SXbBRCB2MggH1OFyL2-ig1Ol54JOzFNVCfDOgOJITrCzGBTrg
<object data="a">
      <input autofocus="" onfocus="document.documentElement.textContent = 'A'"/</object>

### in...@chromium.org (2012-03-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-26)

tracking webkit bug - https://bugs.webkit.org/show_bug.cgi?id=82159

### in...@chromium.org (2012-03-26)

[Empty comment from Monorail migration]

### ke...@chromium.org (2012-03-26)

Relevant changeset: http://trac.webkit.org/changeset/112051

### cl...@chromium.org (2012-03-26)

ClusterFuzz has detected this issue as fixed in range 128808:128813.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=30309630

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f5886cc42a8
Crash State:
  - crash stack -
  WebCore::ContainerNode::resumePostAttachCallbacks
  WebCore::Element::attach
  - free stack -
  WTF::Vector<std::pair<void 
  WebCore::ContainerNode::resumePostAttachCallbacks
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=128808:128813

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97CzzgNNMKrB2jm4nDeyxtzGHrs--HR8sweSBJtuLZLHTex35yar7JtPxVNeRXJCdclcjV-KNzirZbewzpFl8Ui_YoM8Dy-qOXZPKjMnid-zvWEglclFujD5dyn2LhZX8I1V3HmusS7B_jcsFX2wNna_1RUAA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### cl...@chromium.org (2012-03-26)

ClusterFuzz has detected this issue as fixed in range 128813:128890.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=30309630

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f5886cc42a8
Crash State:
  - crash stack -
  WebCore::ContainerNode::resumePostAttachCallbacks
  WebCore::Element::attach
  - free stack -
  WTF::Vector<std::pair<void 
  WebCore::ContainerNode::resumePostAttachCallbacks
  
Fixed: https://cluster-fuzz.appspot.com/revisions?range=128813:128890

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97CzzgNNMKrB2jm4nDeyxtzGHrs--HR8sweSBJtuLZLHTex35yar7JtPxVNeRXJCdclcjV-KNzirZbewzpFl8Ui_YoM8Dy-qOXZPKjMnid-zvWEglclFujD5dyn2LhZX8I1V3HmusS7B_jcsFX2wNna_1RUAA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-04-02)

M18: http://trac.webkit.org/changeset/112907

### sc...@gmail.com (2012-04-04)

$1000 encore

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

This issue was migrated from crbug.com/chromium/120037?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055592)*
