# Memory corruption (read random system memory) or crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40080724](https://issues.chromium.org/issues/40080724) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | [Deleted User] |
| **Assignee** | mo...@google.com |
| **Created** | 2010-04-28 |
| **Bounty** | $500.00 |

## Description

It is possible to crash browser or read some memory using special page.
Check details (in attach). HTML file (+js) and instructions in it.

Thanks a lot.


4.1.249.1064 (45376), Windows XP 32 bit, SP3

## Attachments

- [google_bug.zip](attachments/google_bug.zip) (application/zip, 204.9 KB)
- [highlight.html](attachments/highlight.html) (text/html, 3.2 KB)

## Timeline

### sc...@gmail.com (2010-04-28)

Sounds interesting!
Looks OK on my Linux dev channel build.

Justin or Abhishek - do you happen to have a Windows stable version around to check 
this on?

### in...@chromium.org (2010-04-28)

trying to reproduce bug on my windows.

### sc...@gmail.com (2010-04-28)

Actually, this sounds like it needs a server running? Clicking on 1 or 2 seem to hit 
http://localhost. Do you have a self-contained version that runs only on the 
filesystem?

### [Deleted User] (2010-04-28)

No, you not need a server.
I'll create HTML with crash - one minute.

### [Deleted User] (2010-04-28)

Also, checked on 2 computers - reproduces.

### in...@chromium.org (2010-04-28)

I can replicate the crash 5.0.388.0 (45605) windows. investigating more (my debugger
is giving some weird issues, fixing it first to analyze furthur).
http://infernohacks.com/t/a/Syntax%20analyzer%20demo.htm


### in...@chromium.org (2010-04-28)

This is not a browser crash, but a renderer crash. I will post more analysis soon.

### js...@chromium.org (2010-04-28)

There's definitely an OOB read. I got a sad tab outside of the debugger, but not 
inside. However, running a debug build hits the following ASSERT in 
WebCore::getFallbackFamily() from FontUtilsChromiumWin.cpp:

    ASSERT(characters && characters[0] && length > 0);

The ASSERT is triggered because characters[0] == 0 in my testing. Here's part of the 
stack:

WebCore::getFallbackFamily(const wchar_t * characters=0x175cb8fe, int length=1, 
WebCore::FontDescription::GenericFamilyType generic=StandardFamily, int * 
charChecked=0x00000000, UScriptCode * scriptChecked=0x00000000)  Line 247 + 0x32 
bytes	C++
WebCore::UniscribeHelper::shape(const wchar_t * input=0x175cb8fe, int itemLength=1, 
int numGlyphs=32, tag_SCRIPT_ITEM & run={...}, WebCore::UniscribeHelper::Shaping & 
shaping={...})  Line 633 + 0x13 bytes	C++
WebCore::UniscribeHelper::fillShapes()  Line 728 + 0x34 bytes	C++
WebCore::UniscribeHelper::initWithOptionalLengthProtection(bool 
lengthProtection=true)  Line 145	C++
WebCore::UniscribeHelper::init()  Line 165	C++
WebCore::UniscribeHelperTextRun::UniscribeHelperTextRun(const WebCore::TextRun & 
run={...}, const WebCore::Font & font={...})  Line 59	C++
WebCore::Font::floatWidthForComplexText(const WebCore::TextRun & run={...}, 
WTF::HashSet<WebCore::SimpleFontData const *,WTF::PtrHash<WebCore::SimpleFontData 
const *>,WTF::HashTraits<WebCore::SimpleFontData const *> > * __formal=0x00000000, 
WTF::HashSet<WebCore::SimpleFontData const *,WTF::PtrHash<WebCore::SimpleFontData 
const *>,WTF::HashTraits<WebCore::SimpleFontData const *> > * __formal=0x00000000)  
Line 509	C++
WebCore::Font::floatWidth(const WebCore::TextRun & run={...}, 
WTF::HashSet<WebCore::SimpleFontData const *,WTF::PtrHash<WebCore::SimpleFontData 
const *>,WTF::HashTraits<WebCore::SimpleFontData const *> > * 
fallbackFonts=0x00000000, WebCore::GlyphOverflow * glyphOverflow=0x00000000)  Line 
202	C++
WebCore::Font::width(const WebCore::TextRun & run={...}, 
WTF::HashSet<WebCore::SimpleFontData const *,WTF::PtrHash<WebCore::SimpleFontData 
const *>,WTF::HashTraits<WebCore::SimpleFontData const *> > * 
fallbackFonts=0x00000000, WebCore::GlyphOverflow * glyphOverflow=0x00000000)  Line 97 
+ 0x22 bytes	C++
WebCore::textWidth(WebCore::RenderText * text=0x0086cd8c, unsigned int from=443, 
unsigned int len=325, const WebCore::Font & font={...}, int xPos=0, bool 
isFixedPitch=false, bool collapseWhiteSpace=true)  Line 1302	C++
WebCore::RenderBlock::findNextLineBreak(WebCore::BidiResolver<WebCore::InlineIterator
,WebCore::BidiRun> & resolver={...}, bool firstLine=false, bool & isLineEmpty=false, 
bool & previousLineBrokeCleanly=false, WebCore::EClear * clear=0x0636cd30)  Line 1625 
+ 0x3b bytes	C++
WebCore::RenderBlock::layoutInlineChildren(bool relayoutChildren=false, int & 
repaintTop=114, int & repaintBottom=263)  Line 671 + 0x33 bytes	C++
WebCore::RenderBlock::layoutBlock(bool relayoutChildren=false)  Line 745	C++
WebCore::RenderBlock::layout()  Line 670 + 0x14 bytes	C++


### [Deleted User] (2010-04-28)


                        var last = 1;
                        function doCrash() {
                            if (last == 1) {
                                var a = (Math.random() * 31) + 2;
                                a = a - (a % 1);
                                eval("markInText" + a +"()");
                                last = 0;
                            } else {
                                markInText1();
                                last = 1;
                            }
                            return 0;
                        }
                        function crash() {
                            doCrash();
                            setTimeout("crash()", 100);                            
                        }


You can execute add it in page to crash browser in fast way. Run crash() - wait for 10 sec. If there 
is no crash - reload page and try again.

### in...@chromium.org (2010-04-28)

Jungshik, can you take a look at this one ?

### sc...@gmail.com (2010-04-28)

Great bug. Since the OOB memory is retrieveable via 
document.getElementById('text').innerText[0...100] then this is at least a 
SecSeverity-Medium

### in...@chromium.org (2010-04-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-05-03)

Jungshik, did you get a chance to look at it ? Or, can you please advise a suitable
owner for this bug.

### js...@chromium.org (2010-05-03)

[Comment Deleted]

### js...@chromium.org (2010-05-03)

I'm sorry I mised this. I'll take a look. 

BTW,  have an unrelated CL pending review touching the same file. 



### in...@chromium.org (2010-05-03)

Thanks Jungshik for helping with this. 

### js...@chromium.org (2010-05-11)

Jshin, any progress on this? It's currently flagged m5 and the window is about to 
close.


### js...@chromium.org (2010-05-12)

Sorry. I'm hard time reproducing it. I'll try more and come up with a fix tonight. 


### js...@chromium.org (2010-05-12)

The buffer appears to be corrupted well before it reaches the complex script 
measuring code (Uniscribe). As early as WebCore::RenderBlock::findNextLineBreak (if 
not earlier), the buffer is 'corrupt'. 

In that frame, both |o| (RenderObject pointer) and |t| (RenderText pointer) points to 
"<14 SP's>Window Vi渀گH" (26 chars long). "Windows Vista" is replaced by "Window Vi
渀گH". 

In the previous frame(RenderBlock::layoutInlineChildren), |resolver| appears to be 
init'd with a corrupt value. Perhaps, the actual corruption happens much earlier. 
|resolver|'s position is much larger than the length of the buffer. As a result, 
|len| in the following code in the next frame is set to a huge value (because strlen 
<< pos)

           int strlen = t->textLength();
           int len = strlen - pos;
           const UChar* str = t->characters();


I can put on wall-paper in the measuring/drawing code, but it's not a real fix. 

I've just reproduced the problem with Chrome *and* Safari on Mac and Chrome on Linux 
(the text in the gray box gets corrupted the same way as on Windows if I press box #1 
and box #2 and box #1 again). 

Obviously, wall-papering in the measuring/drawing code of Windows doesn't do any good 
for Mac/Linux. This is clearly a Webkit bug (I was afraid it might be a V8 issue, but 
it's not). 

We need a reduced test to expedite the diagnosis. 

I'm really sorry that I didn't get to this much sooner. I'll report this to the 
upstream. 


### js...@chromium.org (2010-05-12)

set to a huge value ==> set to a negative value. |len| is a 'loop variable' in a while 
loop coming later. So, depending on what happens inside the loop, the renderer may not 
crash despite a random memory access. 


### js...@chromium.org (2010-05-12)

Filed a webkit bug ( https://bugs.webkit.org/show_bug.cgi?id=38977 ). I cc'd everyone 
whose email here whose email address I know. 


### js...@chromium.org (2010-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2010-05-26)

[Comment Deleted]

### [Deleted User] (2010-05-26)

http://lists.macosforge.org/pipermail/webkit-unassigned/2006-July/016004.html

Look like it the same issue.

Here you can test:
https://bug-28245-attachments.webkit.org/attachment.cgi?id=34714

Also, looks like it is from 2006))

### js...@chromium.org (2010-05-26)

The test case doesn't reproduce, and looking at the changeset for the original bug it 
doesn't appear to me that it's the same issue: 
http://trac.webkit.org/changeset?old_path=/&old=17696&new_path=/&new=17697

We've reported the problem upstream to WebKit, and if no one else gets to it soon one 
of the Chrome devs will have another look at it.


### in...@chromium.org (2010-05-26)

I look to have found out the problem. Analyzing more and testing fix.

### ch...@gmail.com (2010-06-23)

+cdn

### ch...@gmail.com (2010-06-25)

I've got the repro down to 70 or so fairly understandable lines. Strangely though, notice on line 11 inside the load event handler that you have to throw exactly that type of exception.

### ch...@gmail.com (2010-06-25)

Forgot to mention the repro involves the following:

1) Splitting text nodes and replacing the split nodes with span element wrapping clones of the split nodes. 
2) Removing the wrapper nodes and replacing them with the wrapped text nodes.
3) Normalizing all the text to coalesce adjoining text nodes.
4) Repeating step one with a larger number of different (non-overlapping) nodes

This can probably be reduced more, but what's actually happening seems to be a lot clearer now.


### ch...@gmail.com (2010-06-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-06-25)

This is starting to look like it may be a duplicate of the replaceChild case from https://crbug.com/chromium/35366.


### in...@chromium.org (2010-06-27)

[Empty comment from Monorail migration]

### ch...@gmail.com (2010-06-28)

This was further reduced by mitz upstream

<p id="text" style="width: 200px; outline: solid;">AAAAAAAAsBBBBBBBB AAAAAAAAAA AAAAAAAAAAAAAAA CCC <!-- -->Z</p> 
<script> 
	var paragraph = document.getElementById("text");
    paragraph.removeChild(paragraph.childNodes[1]);
 
    // Force layout
    document.body.offsetTop;
 
    paragraph.normalize();
    paragraph.firstChild.splitText(0);
</script>

### in...@chromium.org (2010-06-29)

Fixed in <http://trac.webkit.org/changeset/62134>.

### in...@chromium.org (2010-06-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-08)

@Michail: congratulations! This bug report provisionally qualifies for a $500 Chromium Security Reward. Although SecSeverity-Medium, we found this to be a particularly interesting bug. We'll ship the fix to users shortly.

### [Deleted User] (2010-07-09)

Wow, thanks!
Waiting for your final decision :)


### bu...@gmail.com (2010-07-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=52369 

------------------------------------------------------------------------
r52369 | cdn@chromium.org | 2010-07-14 12:00:50 -0700 (Wed, 14 Jul 2010) | 30 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/setData-dirty-lines-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/setData-dirty-lines-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/setData-dirty-lines-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/setData-dirty-lines.html
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/splitText-dirty-lines-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/splitText-dirty-lines-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/splitText-dirty-lines-expected.txt
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/text/splitText-dirty-lines.html
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/dom/CharacterData.cpp?r1=52369&r2=52368
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/dom/Text.cpp?r1=52369&r2=52368

Merge 62134 - <rdar://problem/7975842> Certain text is repeated after using splitText()

Reviewed by Darin Adler.

WebCore: 

Tests: fast/text/setData-dirty-lines.html
       fast/text/splitText-dirty-lines.html

* dom/CharacterData.cpp:
(WebCore::CharacterData::setData): Call RenderText::setTextWithOffset() rather than
setText(), because only the former correctly dirties line boxes.
* dom/Text.cpp:
(WebCore::Text::splitText): Ditto.

LayoutTests: 

* fast/text/setData-dirty-lines-expected.checksum: Added.
* fast/text/setData-dirty-lines-expected.png: Added.
* fast/text/setData-dirty-lines-expected.txt: Added.
* fast/text/setData-dirty-lines.html: Added.
* fast/text/splitText-dirty-lines-expected.checksum: Added.
* fast/text/splitText-dirty-lines-expected.png: Added.
* fast/text/splitText-dirty-lines-expected.txt: Added.
* fast/text/splitText-dirty-lines.html: Added.



BUG=42736
Review URL: http://codereview.chromium.org/2927014
------------------------------------------------------------------------


### ch...@gmail.com (2010-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2010-07-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2010-07-21)

Verified on Mac 5.0.375.121 (Official Build 52864) beta


### [Deleted User] (2010-08-02)

Cool,looks fixed on 5.0.375.125 Windows XP.
But why "FixUnreleased"?


### sc...@gmail.com (2010-08-02)

Yeah, the name FixUnreleased is a little strange but it basically means that we haven't yet opened up the bug to public view.
In this case, it's not clear whether Safari has fixed this yet or not. We generally don't want to open up a bug to public view until Safari is safe.

### sc...@gmail.com (2010-08-03)

@Michail: e-mail me at cevans@chromium.org for steps on how to collect your reward.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-05-04)

This reward got old. If you like one option is that we up the reward to $1337 and donate it to charity.

### [Deleted User] (2012-05-09)

Good idea, agreed.

### sc...@gmail.com (2012-09-05)

$1337 paid to Red Cross.

### [Deleted User] (2012-09-05)

Thanks you guys.

### bu...@chromium.org (2012-10-14)

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

This issue was migrated from crbug.com/chromium/42736?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080724)*
