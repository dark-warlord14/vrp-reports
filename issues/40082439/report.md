# Use after free with SVG use referencing svg style element

| Field | Value |
|-------|-------|
| **Issue ID** | [40082439](https://issues.chromium.org/issues/40082439) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2010-07-30 |
| **Bounty** | $1,000.00 |

## Description

with chrome it sees always comes to 00000000 
but chromium not
it does not crash safari


chromium 6.0.477.0 (53603)
chrome 5.0.375.125

1.svg
=============================
<?xml version="1.0" standalone="no"?>
<svg width="100%" height="100%"  version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">  
<style id="crash">
	<ff/>
</style>	
	<use xlink:href="#crash" /> 
 <k>
</svg>

## Attachments

- [1.txt](attachments/1.txt) (text/x-c++; charset=us-ascii, 5.1 KB)

## Timeline

### js...@chromium.org (2010-07-30)

Confirmed on trunk and stable. Looks like another use-after-free with the SVG use element. Taking a closer look at it now.


### js...@chromium.org (2010-07-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-07-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-07-30)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-07-30)

Here's the explanation. The SVGStyleElement instance is getting prematurely deleted along with the shadow tree for the use element. I've reduced the testcase a bit more just to keep the stack smaller and destructions easy to follow. Filed upstream here:
https://bugs.webkit.org/show_bug.cgi?id=43260

I'm not getting a crash in Safari, but it is knocking out WebKit trunk.


### js...@chromium.org (2010-07-31)

I confirmed on Friday that this is a general destruction ordering issue with use elements. I may have a fix, and will circle back on Monday.

### js...@chromium.org (2010-08-02)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-08-05)

https://crbug.com/chromium/51252 may be a duplicate, but needs further investigation.

### js...@chromium.org (2010-08-05)

[Comment Deleted]

### in...@chromium.org (2010-08-26)

[Empty comment from Monorail migration]

### ch...@gmail.com (2010-09-01)

[Empty comment from Monorail migration]

### ch...@gmail.com (2010-09-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-09-04)

Fix landed upstream as http://trac.webkit.org/changeset/66795
It should be an easy, low risk merge to stable.

### sc...@gmail.com (2010-09-08)

@kuzzcc: congratulations! This report provisionally qualifies for a $1000 Chromium Security Reward! We are increasing this reward beyond the base level because:
- The initial comment contains a very simple repro.
- The initial comment includes a nice crash log which shows a crash trying to write to a register which has 16-bit Unicode ASCII text in it :)
(We are willing to overlook the duplicate bug(s) here on account of the good quality of the repro and crash record)

### in...@chromium.org (2010-09-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-09-08)

Broke the compile, fixing.
3>d:\chrome\472\src\third_party\webkit\webcore\svg\SVGUseElement.cpp(127) : error C2248: 'WebCore::XMLDocumentParser::wellFormed' : cannot access private member declared in class 'WebCore::XMLDocumentParser'
3>        d:\chrome\472\src\third_party\WebKit\WebCore\dom\XMLDocumentParser.h(103) : see declaration of 'WebCore::XMLDocumentParser::wellFormed'
3>        d:\chrome\472\src\third_party\WebKit\WebCore\dom\XMLDocumentParser.h(73) : see declaration of 'WebCore::XMLDocumentParser'

### in...@chromium.org (2010-09-08)

compile fixed, looks like some other change did made this function public, so i did the same :)

### bu...@gmail.com (2010-09-08)

------------------------------------------------------------------------
r58828 | inferno@chromium.org | Wed Sep 08 08:57:40 PDT 2010
Changed paths:
 M /branches/WebKit/472/WebCore/svg/SVGUseElement.cpp
 A /branches/WebKit/472/LayoutTests/svg/custom/use-invalid-style-expected.txt
 A /branches/WebKit/472/LayoutTests/svg/custom/use-invalid-style.svg
Merge 66795 - 2010-09-04  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Nikolas Zimmermann.

        Prevent premature deletion of svg use shadow tree
        https://bugs.webkit.org/show_bug.cgi?id=43260

        Test: svg/custom/use-invalid-style.svg

        * svg/SVGUseElement.cpp:
        (WebCore::SVGUseElement::insertedIntoDocument):
        (WebCore::SVGUseElement::removedFromDocument):
        (WebCore::SVGUseElement::detach):
2010-09-04  Justin Schuh  <jschuh@chromium.org>

        Reviewed by Nikolas Zimmermann.

        Check for premature deletion of svg use shadow style element
        https://bugs.webkit.org/show_bug.cgi?id=43260

        * svg/custom/use-invalid-style-expected.txt: Added.
        * svg/custom/use-invalid-style.svg: Added.


BUG=50712

Review URL: http://codereview.chromium.org/3364011
------------------------------------------------------------------------

### bu...@gmail.com (2010-09-08)

------------------------------------------------------------------------
r58841 | inferno@chromium.org | Wed Sep 08 09:56:31 PDT 2010
Changed paths:
 M /branches/WebKit/472/WebCore/dom/XMLDocumentParser.h
Fix SVG Compile.

BUG=50712

------------------------------------------------------------------------

### sc...@gmail.com (2010-09-22)

Payment is in the electronic system.

### js...@chromium.org (2011-01-05)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

This issue was migrated from crbug.com/chromium/50712?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/50713, crbug.com/chromium/66763]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082439)*
