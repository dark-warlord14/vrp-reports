# Use after free due to refcounting issue in MediaQueryMatcher::prepareEvaluator

| Field | Value |
|-------|-------|
| **Issue ID** | [40092133](https://issues.chromium.org/issues/40092133) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-06-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

not sure if this is a real bug but reporting anyhow, as per twitter w/ @scarybeasts

use-after-free + invalid read. doesn't crash the regular browser, just valgrind and ASan

**VERSION**  

Chrome Version: stable, trunk.  

Operating System: linux

**REPRODUCTION CASE**

<iframe id="i"></iframe>
<script type="application/javascript">
var iframe = document.getElementById("i");
var obj = iframe.contentWindow.matchMedia("(min-width: 0em)");
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer with asan or vg  

Crash State:  

==20062== ERROR: AddressSanitizer crashed on address 0x000000000bc811c8 at pc 0x4e7643b bp 0x7ffffdddf3b0 sp 0x7ffffdddf390  

READ of size 8 at 0x000000000bc811c8 thread T0  

#0 0x4e7643b in WebCore::CSSPrimitiveValue::computeLengthDouble /home/user/asan/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:60  

#1 0x4e7610c in WebCore::CSSPrimitiveValue::computeLength<int> /home/user/asan/src/third\_party/WebKit/Source/WebCore/css/

## Attachments

- [css.html](attachments/css.html) (text/plain; charset=us-ascii, 186 B)
- [vg.txt](attachments/vg.txt) (text/plain; charset=us-ascii, 17.0 KB)
- [vg-google-chrome-stable.txt](attachments/vg-google-chrome-stable.txt) (text/plain; charset=us-ascii, 7.1 KB)
- [asan.txt](attachments/asan.txt) (text/plain; charset=us-ascii, 5.7 KB)

## Timeline

### in...@chromium.org (2011-06-23)

Awesome miaubiz. Seeing the ASAN stacktrace looks pretty legit use after free. Also it crashes my windows debug without any problem :)

### in...@chromium.org (2011-06-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-23)

filed webkit bug - https://bugs.webkit.org/show_bug.cgi?id=63264 and have fix ready.

### in...@chromium.org (2011-06-23)

http://trac.webkit.org/changeset/89595

### sc...@gmail.com (2011-06-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-06-28)

Merged to M13: http://trac.webkit.org/changeset/89898

### sc...@gmail.com (2011-07-20)

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

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/87227?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092133)*
