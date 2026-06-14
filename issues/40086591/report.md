# Aw snap on github.com with voice search extension installed

| Field | Value |
|-------|-------|
| **Issue ID** | [40086591](https://issues.chromium.org/issues/40086591) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | te...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-12-31 |
| **Bounty** | $500.00 |

## Description

Affected version: 9.0.601.0 (68003) / 10.0.625.0 (70283) - Windows  

Last known working Version: 9.0.595.0 (67491)

**What steps will reproduce the problem?**

1. Install voice search <https://chrome.google.com/webstore/detail/hhfkcobomkalfdlmkongnhnhahkmnaad>
2. Log in to github.com and go to github.com  
   
   **3.**

**What is the expected output? What do you see instead?**  

Happy pages. Sad face.

**Please use labels and text to provide additional information.**

Stack trace:

> chrome.dll!WebCore::InlineFlowBox::addToLine(WebCore::InlineBox \* child) Line 82 + 0x3 bytes C++  
> 
> chrome.dll!WebCore::RenderBlock::constructLine(unsigned int runCount, WebCore::BidiRun \* firstRun, WebCore::BidiRun \* lastRun, bool firstLine, bool lastLine, WebCore::RenderObject \* endObject) Line 271 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren, int & repaintLogicalTop, int & repaintLogicalBottom) Line 736 + 0x40 bytes C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1207 C++  
> 
> chrome.dll!WebCore::RenderTextControlSingleLine::layout() Line 270 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren, int & repaintLogicalTop, int & repaintLogicalBottom) Line 573 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1207 C++  
> 
> chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox \* child, WebCore::RenderBlock::MarginInfo & marginInfo, int & previousFloatLogicalBottom, int & maxFloatLogicalBottom) Line 1938 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlockChildren(bool relayoutChildren, int & maxFloatLogicalBottom) Line 1850 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1211 C++  
> 
> chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox \* child, WebCore::RenderBlock::MarginInfo & marginInfo, int & previousFloatLogicalBottom, int & maxFloatLogicalBottom) Line 1938 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlockChildren(bool relayoutChildren, int & maxFloatLogicalBottom) Line 1850 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1211 C++  
> 
> chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  
> 
> chrome.dll!WebCore::RenderBlock::insertFloatingObject(WebCore::RenderBox \* o) Line 3045 C++  
> 
> chrome.dll!WebCore::RenderBlock::skipLeadingWhitespace(WebCore::BidiResolver[WebCore::InlineIterator,WebCore::BidiRun](javascript:void(0);) & resolver, bool firstLine, bool isLineEmpty, bool previousLineBrokeCleanly, WebCore::RenderBlock::FloatingObject \* lastFloatFromPreviousLine) Line 1309 + 0xd bytes C++  
> 
> chrome.dll!WebCore::RenderBlock::findNextLineBreak(WebCore::BidiResolver[WebCore::InlineIterator,WebCore::BidiRun](javascript:void(0);) & resolver, bool firstLine, bool & isLineEmpty, bool & previousLineBrokeCleanly, bool & hyphenated, WebCore::EClear \* clear, WebCore::RenderBlock::FloatingObject \* lastFloatFromPreviousLine) Line 1428 + 0x4f bytes C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren, int & repaintLogicalTop, int & repaintLogicalBottom) Line 667 + 0x38 bytes C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1207 C++  
> 
> chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  
> 
> chrome.dll!WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox \* child, WebCore::RenderBlock::MarginInfo & marginInfo, int & previousFloatLogicalBottom, int & maxFloatLogicalBottom) Line 1938 C++

## Timeline

### [Deleted User] (2011-01-05)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-01-05)

Sunand, the layout bugs are deceptively similar and it does not look this might be dup. The crash stack looks security since i have fixed several layout bugs. Can you please confirm it does not reproduce on trunk (m10).

### te...@gmail.com (2011-01-05)

10.0.628.0 (70457) crashes with the same stack trace.

### in...@chromium.org (2011-01-05)

temp01irc, i did suspect that this is a different bug. we have some other layout bgus at this time and this might be a dup of one of those. also, this would need reduction before we can quickly fix it.

### er...@chromium.org (2011-01-11)

This is the top renderer crash on the dev channel as well.
It reproduces very easily so long as you have googlevoice extension installed.

Another easy site to repro on is http://www.artlebedev.ru/.


(1) Install: https://chrome.google.com/webstore/detail/hhfkcobomkalfdlmkongnhnhahkmnaad#

(2) Load: http://www.artlebedev.ru/

(3) Renderer crashes immediately

### te...@gmail.com (2011-01-12)

The following crashes for me:

1) Open data:text/html,<input type="search">
2) Run document.querySelector("input[type='search']").setAttribute('x-webkit-speech', '') using Console.


### in...@chromium.org (2011-01-12)

Thanks a lot temp01irc. you made life a whole lot easier with this minimized repro. i will ask the security panel to consider this for a reward.

I have verified that this results in bad cast in RenderBlock::createLineBoxes and hits my favorite all time assert
ASSERT(obj->isRenderInline() || obj == this);

Satish, can you please take a look.

### in...@chromium.org (2011-01-12)

Satish, this is also the top renderer crash, so it will be great if we can move fast on this.

### in...@chromium.org (2011-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2011-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2011-01-12)

Fix in review - https://bugs.webkit.org/show_bug.cgi?id=52325

### [Deleted User] (2011-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2011-01-14)

The webkit patch was reviewed by jamesr@ and I have addressed all his comments. However looks like he is away until tuesday. If we need to move fast could someone else review and approve the patch?

### in...@chromium.org (2011-01-14)

Satish fixed in http://trac.webkit.org/changeset/75811. will merge to m9.

### [Deleted User] (2011-01-27)

Was this merged and should we close this bug?

### js...@chromium.org (2011-01-27)

The status is WillMerge because it needs to be merged to m9 once the window opens.

### in...@chromium.org (2011-02-01)

speech is m10 and we branched at 76408 which is after fix revision r75811.

### la...@chromium.org (2011-03-18)

Affected version: 9.0.601.0 (68003) / 10.0.625.0 (70283) - Windows  

Last known working Version: 9.0.595.0 (67491)

**What steps will reproduce the problem?**

1. Install voice search <https://chrome.google.com/webstore/detail/hhfkcobomkalfdlmkongnhnhahkmnaad>
2. Log in to github.com and go to github.com  
   
   **3.**

**What is the expected output? What do you see instead?**  

Happy pages. Sad face.

**Please use labels and text to provide additional information.**

Stack trace:

> chrome.dll!WebCore::InlineFlowBox::addToLine(WebCore::InlineBox \* child) Line 82 + 0x3 bytes C++  

chrome.dll!WebCore::RenderBlock::constructLine(unsigned int runCount, WebCore::BidiRun \* firstRun, WebCore::BidiRun \* lastRun, bool firstLine, bool lastLine, WebCore::RenderObject \* endObject) Line 271 C++  

chrome.dll!WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren, int & repaintLogicalTop, int & repaintLogicalBottom) Line 736 + 0x40 bytes C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1207 C++  

chrome.dll!WebCore::RenderTextControlSingleLine::layout() Line 270 C++  

chrome.dll!WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren, int & repaintLogicalTop, int & repaintLogicalBottom) Line 573 C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1207 C++  

chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox \* child, WebCore::RenderBlock::MarginInfo & marginInfo, int & previousFloatLogicalBottom, int & maxFloatLogicalBottom) Line 1938 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChildren(bool relayoutChildren, int & maxFloatLogicalBottom) Line 1850 C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1211 C++  

chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox \* child, WebCore::RenderBlock::MarginInfo & marginInfo, int & previousFloatLogicalBottom, int & maxFloatLogicalBottom) Line 1938 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChildren(bool relayoutChildren, int & maxFloatLogicalBottom) Line 1850 C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1211 C++  

chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  

chrome.dll!WebCore::RenderBlock::insertFloatingObject(WebCore::RenderBox \* o) Line 3045 C++  

chrome.dll!WebCore::RenderBlock::skipLeadingWhitespace(WebCore::BidiResolver<WebCore::InlineIterator,WebCore::BidiRun> & resolver, bool firstLine, bool isLineEmpty, bool previousLineBrokeCleanly, WebCore::RenderBlock::FloatingObject \* lastFloatFromPreviousLine) Line 1309 + 0xd bytes C++  

chrome.dll!WebCore::RenderBlock::findNextLineBreak(WebCore::BidiResolver<WebCore::InlineIterator,WebCore::BidiRun> & resolver, bool firstLine, bool & isLineEmpty, bool & previousLineBrokeCleanly, bool & hyphenated, WebCore::EClear \* clear, WebCore::RenderBlock::FloatingObject \* lastFloatFromPreviousLine) Line 1428 + 0x4f bytes C++  

chrome.dll!WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren, int & repaintLogicalTop, int & repaintLogicalBottom) Line 667 + 0x38 bytes C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1207 C++  

chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox \* child, WebCore::RenderBlock::MarginInfo & marginInfo, int & previousFloatLogicalBottom, int & maxFloatLogicalBottom) Line 1938 C++

### la...@chromium.org (2011-03-19)

Affected version: 9.0.601.0 (68003) / 10.0.625.0 (70283) - Windows  

Last known working Version: 9.0.595.0 (67491)

**What steps will reproduce the problem?**

1. Install voice search <https://chrome.google.com/webstore/detail/hhfkcobomkalfdlmkongnhnhahkmnaad>
2. Log in to github.com and go to github.com  
   
   **3.**

**What is the expected output? What do you see instead?**  

Happy pages. Sad face.

**Please use labels and text to provide additional information.**

Stack trace:

> chrome.dll!WebCore::InlineFlowBox::addToLine(WebCore::InlineBox \* child) Line 82 + 0x3 bytes C++  

chrome.dll!WebCore::RenderBlock::constructLine(unsigned int runCount, WebCore::BidiRun \* firstRun, WebCore::BidiRun \* lastRun, bool firstLine, bool lastLine, WebCore::RenderObject \* endObject) Line 271 C++  

chrome.dll!WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren, int & repaintLogicalTop, int & repaintLogicalBottom) Line 736 + 0x40 bytes C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1207 C++  

chrome.dll!WebCore::RenderTextControlSingleLine::layout() Line 270 C++  

chrome.dll!WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren, int & repaintLogicalTop, int & repaintLogicalBottom) Line 573 C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1207 C++  

chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox \* child, WebCore::RenderBlock::MarginInfo & marginInfo, int & previousFloatLogicalBottom, int & maxFloatLogicalBottom) Line 1938 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChildren(bool relayoutChildren, int & maxFloatLogicalBottom) Line 1850 C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1211 C++  

chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox \* child, WebCore::RenderBlock::MarginInfo & marginInfo, int & previousFloatLogicalBottom, int & maxFloatLogicalBottom) Line 1938 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChildren(bool relayoutChildren, int & maxFloatLogicalBottom) Line 1850 C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1211 C++  

chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  

chrome.dll!WebCore::RenderBlock::insertFloatingObject(WebCore::RenderBox \* o) Line 3045 C++  

chrome.dll!WebCore::RenderBlock::skipLeadingWhitespace(WebCore::BidiResolver<WebCore::InlineIterator,WebCore::BidiRun> & resolver, bool firstLine, bool isLineEmpty, bool previousLineBrokeCleanly, WebCore::RenderBlock::FloatingObject \* lastFloatFromPreviousLine) Line 1309 + 0xd bytes C++  

chrome.dll!WebCore::RenderBlock::findNextLineBreak(WebCore::BidiResolver<WebCore::InlineIterator,WebCore::BidiRun> & resolver, bool firstLine, bool & isLineEmpty, bool & previousLineBrokeCleanly, bool & hyphenated, WebCore::EClear \* clear, WebCore::RenderBlock::FloatingObject \* lastFloatFromPreviousLine) Line 1428 + 0x4f bytes C++  

chrome.dll!WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren, int & repaintLogicalTop, int & repaintLogicalBottom) Line 667 + 0x38 bytes C++  

chrome.dll!WebCore::RenderBlock::layoutBlock(bool relayoutChildren, int pageLogicalHeight) Line 1207 C++  

chrome.dll!WebCore::RenderBlock::layout() Line 1108 C++  

chrome.dll!WebCore::RenderBlock::layoutBlockChild(WebCore::RenderBox \* child, WebCore::RenderBlock::MarginInfo & marginInfo, int & previousFloatLogicalBottom, int & maxFloatLogicalBottom) Line 1938 C++

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

### sc...@gmail.com (2012-11-09)

@temp01irc: are you still paying attention to this bug?

It looks like the rewards panel decided to reward you $500 for this security bug report back in Jan 2011 (oops!)
Obviously, the right thing to do is for us to still pay you if you're interested. Or we could give $1337 to charity.

### ke...@chromium.org (2012-11-09)

It probably makes sense to remove the comment restriction in case temp01irc wants to actually reply.

### te...@gmail.com (2012-11-17)

Hey,

Yeah. I just checked this. Am I still eligible?

### sc...@gmail.com (2012-12-05)

@temp01irc: yippee!! Just noticed you replied :-)

Yes, you're still eligible. Sounds like you're interested so I'll have someone reach out to arrange the reward.

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### as...@chromium.org (2014-06-17)

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

This issue was migrated from crbug.com/chromium/68342?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086591)*
