# Memory Corruption with invalid svg rendering

| Field | Value |
|-------|-------|
| **Issue ID** | [40081292](https://issues.chromium.org/issues/40081292) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ao...@gmail.com |
| **Created** | 2010-05-28 |
| **Bounty** | $500.00 |

## Description

A segmentation fault occurs in 32-bit Chromium (6.0.416.0 (Developer Build
48240) Ubuntu) on Ubuntu 10.04 when a malformed SVG file is opened. To
reproduce:

 $ echo '<g xmlns="http://www.w3.org/2000/svg"><text>a' > test.svg
 $ chromium-browser test.svg

The issue does not affect Google Chrome (5.0.375.55 (Official Build 47796))
on the same machine. Not tested 64-bit platforms or Windows.

Backtrace begins:

#0  0x00000000 in ?? ()
#1  0x09011e5d in WebCore::RenderInline::createAndAppendInlineFlowBox (
    this=0xa547198)
    at third_party/WebKit/WebCore/rendering/RenderInline.cpp:850
#2  0x08fe1b83 in createInlineBoxForRenderer (this=0xa5474f0, obj=0xa547198, 
    firstLine=true)
    at third_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:191
#3  WebCore::RenderBlock::createLineBoxes (this=0xa5474f0, obj=0xa547198, 
    firstLine=true)
    at third_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:227
#4  0x08fe1d6f in WebCore::RenderBlock::constructLine (this=0xa5474f0, 
    runCount=1, firstRun=0xa547820, lastRun=0xa547820, firstLine=true, 
    lastLine=true, endObject=0x0)
    at third_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:280
#5  0x08fe9d99 in WebCore::RenderBlock::layoutInlineChildren (this=0xa5474f0, 
    relayoutChildren=true, repaintTop=@0xbfffd82c, repaintBottom=@0xbfffd828)
    at third_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:740
#6  0x08fdf098 in WebCore::RenderBlock::layoutBlock (this=0xa5474f0, 
    relayoutChildren=true)
    at third_party/WebKit/WebCore/rendering/RenderBlock.cpp:746
#7  0x08fce348 in WebCore::RenderBlock::layout (this=0xa5474f0)
    at third_party/WebKit/WebCore/rendering/RenderBlock.cpp:670
[...]


## Attachments

- [bug45331.svg](attachments/bug45331.svg) (text/plain; charset=us-ascii, 47 B)
- deleted (application/octet-stream, 0 B)
- [segv-getBorderPaddingMargin.svg](attachments/segv-getBorderPaddingMargin.svg) (text/plain; charset=us-ascii, 47 B)

## Timeline

### js...@chromium.org (2010-05-28)

Doesn't crash the Windows trunk for me. Crashes 64-bit version of 6.0.408.1.

### js...@chromium.org (2010-05-28)

That last comment should have read: Crashes 64-bit Linux (Ubuntu 8.04) version of 
6.0.408.1.

### in...@chromium.org (2010-06-04)

I can reproduce this on both linux and windows with latest trunk. Need to add a
newline for crash to happen. also hunting regression. it happened between 58209-58231.

### in...@chromium.org (2010-06-04)

Filed webkit bug.
https://bugs.webkit.org/show_bug.cgi?id=40173

### [Deleted User] (2010-06-07)

[Empty comment from Monorail migration]

### ao...@gmail.com (2010-06-13)

I just noticed that some other segfaults from the test run crashed at ip 0, but with slightly different backtrace and input. Could you check whether this issue is also handled by the webkit fix?

Tested with Chromiums 6.0.434.0 (Developer Build 49638) Ubuntu 10.04/x86, and 49488 on x86_64. Backtrace starts:
Program received signal SIGSEGV, Segmentation fault.
0x00000000 in ?? ()
(gdb) bt
#0  0x00000000 in ?? ()
#1  0x0900aefb in getBorderPaddingMargin (child=0xa564398, endOfInline=true)
    at third_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:55
#2  0x0900af78 in inlineWidth (child=0xa564594, start=<value optimized out>, 
    end=true)
    at third_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:66
#3  0x09011c5b in WebCore::RenderBlock::findNextLineBreak (this=0xa5646c0, 
    resolver=..., firstLine=true, isLineEmpty=@0xbfffd17c, 
    previousLineBrokeCleanly=@0xbfffd17d, clear=0xbfffd164)
    at third_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:1510
#4  0x09014ea4 in WebCore::RenderBlock::layoutInlineChildren (this=0xa5646c0, 
    relayoutChildren=true, repaintTop=@0xbfffd26c, repaintBottom=@0xbfffd268)
    at third_party/WebKit/WebCore/rendering/RenderBlockLineLayout.cpp:675
#5  0x0900a9c8 in WebCore::RenderBlock::layoutBlock (this=0xa5646c0, 
    relayoutChildren=true)
    at third_party/WebKit/WebCore/rendering/RenderBlock.cpp:1187
#6  0x08ff7eb8 in WebCore::RenderBlock::layout (this=0xa5646c0)
    at third_party/WebKit/WebCore/rendering/RenderBlock.cpp:1111
#7  0x09009cf3 in WebCore::RenderBlock::layoutBlockChild (this=0xa564520, 
    child=0xa5646c0, marginInfo=..., previousFloatBottom=@0xbfffd36c, 
    maxFloatBottom=@0xbfffd454)
    at third_party/WebKit/WebCore/rendering/RenderBlock.cpp:1804
[...]

### ao...@gmail.com (2010-06-13)

Less wrong file:

### sc...@gmail.com (2010-06-14)

Thanks Aki! This qualifies for one of our $500 rewards.
We likely won't get to it right away since it doesn't affect our stable version. But we're very happy that your report will mean we can make sure it won't affect the next stable version :)

### in...@chromium.org (2010-06-15)

I have a fix that fixes both of the above two testcases and looks to fix 43488, 46360 as well in a generic way. I am able to get clean results from run-webkit-tests as well. the fix is done in a generic way so that memory corruption does not happen inside constructline function. (we want this pattern of similar bugs to end now ..). still testing the fix.

### in...@chromium.org (2010-06-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-06-21)

The fix in https://crbug.com/chromium/45331#c9 is just a mitigation strategy. We should not traveling that code path for svg rendering, so the problem is happening somewhere else. Removing myself as owner for now.

### js...@chromium.org (2010-06-22)

Turns out this has the same root cause (and fix) as https://crbug.com/chromium/43488. Neither is the most accurate description, but I'm merging into the oldest one.


### sc...@gmail.com (2010-06-26)

[Empty comment from Monorail migration]

### ao...@gmail.com (2010-06-28)

When you get around to it, and if it still applies this being a duplicate issue, I'd like to forward the reward to Red Cross.

### sc...@gmail.com (2010-07-08)

Hello Aki! It is indeed a duplicate. We've upped the reward to $1337 and donated it to Red Cross as requested.

### ao...@gmail.com (2010-07-09)

Excellent :)

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/45331?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/43488]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081292)*
