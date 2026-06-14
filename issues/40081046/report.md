# security:chrome_1c30000!WebCore::InlineBox::paint+0x70

| Field | Value |
|-------|-------|
| **Issue ID** | [40081046](https://issues.chromium.org/issues/40081046) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | wo...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2010-05-18 |
| **Bounty** | $500.00 |

## Description

test it on 4.1.249.1064 (45376)
the stack is like this:
ChildEBP RetAddr  Args to Child              
0012edfc 023bbc32 0012ee30 00000000 000000a9
chrome_1f30000!WebCore::InlineBox::paint+0x70 (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlinebox.cpp
@ 173]
0012ee5c 023bbc32 0012ee90 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012eebc 023bbc32 0012eef0 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012ef1c 023bbc32 0012ef50 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012ef7c 023bbc32 0012efb0 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012efdc 023bbc32 0012f010 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012f03c 023bbc32 0012f070 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012f09c 023bbc32 0012f0d0 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012f0fc 023bbc32 0012f130 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012f15c 023bbc32 0012f190 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012f1bc 023b9d13 0012f248 00000000 000000a9
chrome_1f30000!WebCore::InlineFlowBox::paint+0x1be (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\inlineflowbox.cpp
@ 674]
0012f1d4 023e2987 0012f248 00000000 000000a9
chrome_1f30000!WebCore::RootInlineBox::paint+0x14 (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\rootinlinebox.cpp
@ 166]
001

unpack the webkit21.rar and got the 1.xhtml and frame.jsp , copy frame.jsp
and 1.xhtml files to tomcat webapp dir.use safari to visit frame.jsp, 
chrome will crash. And sometimes maybe you need move mouse in the window.

I used a 12 inch laptop , windows xp sp3 version.





## Attachments

- [webkit21.rar](attachments/webkit21.rar) (application/x-rar, 1.1 KB)
- [1.xhtml](attachments/1.xhtml) (text/plain; charset=utf-8, 4.3 KB)
- [frame.html](attachments/frame.html) (text/plain; charset=us-ascii, 215 B)

## Timeline

### in...@chromium.org (2010-05-18)

v6 trunk Release: crashes almost instantly.
on Debug build: I get an arbitary memory read at this ASSERT
inline RenderBoxModelObject* toRenderBoxModelObject(RenderObject* object)
{ 
    ASSERT(!object || object->isBoxModelObject());

### sk...@chromium.org (2010-05-18)

This crash is easier to reproduce with the attached files (1.xhtml is unchanged from 
the original).

I think it may be caused by text wrapping (which is why I added the random width of the 
IFRAME in my repro) but I'm still investigating.

### in...@chromium.org (2010-05-18)

Filed WebKit Bug.
https://bugs.webkit.org/show_bug.cgi?id=39305

However, since ASSERT don't hit in release version, it is most likely causing memory
corruption because of an invalid cast.
inline RenderBoxModelObject* toRenderBoxModelObject(RenderObject* object)
{ 
    ASSERT(!object || object->isBoxModelObject());
    return static_cast<RenderBoxModelObject*>(object);
}

Thanks Skylined for working on the reduced testcase.

### js...@chromium.org (2010-05-20)

We should try to get this fixed for the security rollup patch following the v5 
release.

### in...@chromium.org (2010-05-20)

Thanks Justin. i have added couple of guys from apple side (mitz, hyatt) who i think
know this code best. i will track this on my radar.

### js...@chromium.org (2010-06-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-06-14)

copy-paste from my webkit comments.

Here is a reduced testcase which does not require any page refreshes, and crashes both safari and chrome. (Note that there is a space in the first \*\*\*\* line between the two 64 = blocks).

<html>
\*\*================================================================ ================================================================\*\*
<b>================================================================
</b>
<b dir='ltr'>-===============================================================
<object data='anyURI'></object>
</b>
</html>

The problem can be seen with even a more reduced version below. As you will see, the +== line is created twice. The one created to the end of -=== line is invalid. The resolver looks to be getting messed up in RenderBlock::layoutInlineChildren.

<html>
\*\*-=================================================================\*\*
<b dir='ltr'>+==============================================================
</b>
</html>

I am trying to see what is happening wrong here, but any pointers will be very helpful. A somewhat related bug to this is a another memory corruption bug (<https://bugs.webkit.org/show_bug.cgi?id=38977>) where resolver position gets past the text length (in RenderBlock::determineStartPosition).

### sk...@chromium.org (2010-06-18)

While trying to reduce the original, I found that the size at which page is rendered plays a role; my repro loads the xhtml in an IFRAME with random width over and over until it crashes. This could indeed indicate that positioning, word-breaking and/or line-wrapping may have something to do with this, but I'm not sure exactly what.

### sk...@chromium.org (2010-06-18)

Sorry, I already mentioned that in https://crbug.com/chromium/44424#c2 :S.

Either way, I can only reproduce a NULL pointer, so it does not appear exploitable at this point.

### in...@chromium.org (2010-06-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-06-23)

James, can you please help to check what is happening wrong with layout and bidi resolver in this bug. Please see the reduced testcase in #7.

### in...@chromium.org (2010-06-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-06-26)

Fixed in <http://trac.webkit.org/projects/webkit/changeset/61921>.

### in...@chromium.org (2010-06-28)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-06-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=51012 

------------------------------------------------------------------------
r51012 | inferno@chromium.org | 2010-06-28 12:10:32 -0700 (Mon, 28 Jun 2010) | 23 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/bidi-explicit-embedding-past-end-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/bidi-explicit-embedding-past-end-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/bidi-explicit-embedding-past-end-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/bidi-explicit-embedding-past-end.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/platform/text/BidiResolver.h?r1=51012&r2=51011

Merge 61921 - <rdar://problem/8000667> Certain text is repeated before and after a line break

Reviewed by Sam Weinig.

WebCore: 

Test: fast/text/bidi-explicit-embedding-past-end.html

* platform/text/BidiResolver.h:
(WebCore::::createBidiRunsForLine): Committing explicit embedding past the end of the range
creates BidiRuns up to the end of the range, so at that point, we can stop iterating.

LayoutTests: 

* fast/text/bidi-explicit-embedding-past-end-expected.checksum: Added.
* fast/text/bidi-explicit-embedding-past-end-expected.png: Added.
* fast/text/bidi-explicit-embedding-past-end-expected.txt: Added.
* fast/text/bidi-explicit-embedding-past-end.html: Added.


BUG=44424
TBR=mitz@apple.com
Review URL: http://codereview.chromium.org/2843028
------------------------------------------------------------------------


### sc...@gmail.com (2010-07-01)

Another reward for wushi! :D

### sc...@gmail.com (2010-07-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-12)

Payment on its way.

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

This issue was migrated from crbug.com/chromium/44424?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081046)*
