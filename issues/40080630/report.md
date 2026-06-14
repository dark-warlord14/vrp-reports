# WebCore::FontFallbackList::determinePitch memory corruption (0b4c05aab686a31bc4954a5bd6bae27b)

| Field | Value |
|-------|-------|
| **Issue ID** | [40080630](https://issues.chromium.org/issues/40080630) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Fonts |
| **Reporter** | wo...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2010-04-22 |
| **Bounty** | $500.00 |

## Description

unpack the webkit30.rar and got the 2.xhtml and frame.jsp , copy frame.jsp
and 2.xhtml files to tomcat webapp dir.use chrome to visit frame.jsp. 

the crash will like this:

(128.17b4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=017f01b0 ebx=04e8e0b0 ecx=01af03f0 edx=0012f1a4 esi=01af03f0 edi=01af9db8
eip=017f01c0 esp=0012eea4 ebp=0012f00c iopl=0         nv up ei ng nz ac pe cy
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010297
017f01c0 c0017f          rol     byte ptr [ecx],7Fh         ds:0023:01af03f0=b0
1:019> kv
ChildEBP RetAddr  Args to Child              
WARNING: Frame IP not in any known module. Following frames may be wrong.
0012eea0 023a1871 04e8e4bc 04e9ca98 022ce67c 0x17f01c0
0012eeac 022ce67c 01b16c34 00000001 023ff9e7
chrome_1f30000!WebCore::FontFallbackList::determinePitch+0x17 (FPO:
[1,1,1]) (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\platform\graphics\fontfallbacklist.cpp
@ 77]
0012eeb8 023ff9e7 0012f0a0 0012f104 04e8e4bc
chrome_1f30000!WebCore::Font::isFixedPitch+0x10 (FPO: [0,0,1]) (CONV:
thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\platform\graphics\font.cpp
@ 160]
0012f00c 023fe014 04e8e4bc 0012f048 0012f0f4
chrome_1f30000!WebCore::RenderBlock::findNextLineBreak+0x595 (CONV:
thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblocklinelayout.cpp
@ 1800]
0012f1c8 0236823f 04e8e4bc 00000001 0012f1f4
chrome_1f30000!WebCore::RenderBlock::layoutInlineChildren+0x632 (CONV:
thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblocklinelayout.cpp
@ 960]
0012f254 0236807a 00000001 0012f2e0 0236936a
chrome_1f30000!WebCore::RenderBlock::layoutBlock+0x1a7 (CONV: thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp
@ 734]
0012f260 0236936a 0012f2c8 04e8e4bc 04e8df14
chrome_1f30000!WebCore::RenderBlock::layout+0x17 (FPO: [0,0,1]) (CONV:
thiscall)
[c:\b\slave\chrome-official\build\src\third_party\webkit\webcore\rendering\renderblock.cpp
@ 663]



## Attachments

- [webkit30.rar](attachments/webkit30.rar) (application/x-rar, 2.6 KB)
- [WebCore..FontFallbackList..determinePitch ReadAV@NULL (0b4c05aab686a31bc4954a5bd6bae27b).html](attachments/WebCore..FontFallbackList..determinePitch ReadAV@NULL (0b4c05aab686a31bc4954a5bd6bae27b).html) (exported SGML document text, 803.1 KB)
- [repro.xhtml](attachments/repro.xhtml) (text/html, 442 B)
- [WebCore..FontFallbackList..determinePitch ExecAV@Arbitrary (0b4c05aab686a31bc4954a5bd6bae27b).html](attachments/WebCore..FontFallbackList..determinePitch ExecAV@Arbitrary (0b4c05aab686a31bc4954a5bd6bae27b).html) (exported SGML document text, 964.5 KB)

## Timeline

### sk...@chromium.org (2010-04-22)

I've simplified the repro to the attached xhtml file. I've also attached details for a NULL ptr crash and an arbitrary code execution crash.

id:             WebCore::FontFallbackList::determinePitch ReadAV@NULL (0b4c05aab686a31bc4954a5bd6bae27b)
description:    Attempt to read from NULL pointer (+0x15) in WebCore::FontFallbackList::determinePitch
stack:          WebCore::FontFallbackList::determinePitch
                WebCore::Font::isFixedPitch
                WebCore::RenderBlock::findNextLineBreak
                WebCore::RenderBlock::layoutInlineChildren
                WebCore::RenderBlock::layoutBlock
                WebCore::RenderBlock::layout
                WebCore::RenderBlock::layoutBlockChild
                WebCore::RenderBlock::layoutBlockChildren
                WebCore::RenderBlock::layoutBlock
                WebCore::RenderBlock::layout
                WebCore::RenderBlock::layoutBlockChild
                WebCore::RenderBlock::layoutBlockChildren
                WebCore::RenderBlock::layoutBlock
                WebCore::RenderBlock::layout
                WebCore::RenderBlock::layoutBlockChild
                WebCore::RenderBlock::layoutBlockChildren
                WebCore::RenderBlock::layoutBlock
                WebCore::RenderBlock::layout
                WebCore::RenderView::layout
                WebCore::FrameView::layout
                WebCore::FrameView::layoutIfNeededRecursive
<snip>

The problem seems to be caused by an unavailable font file loaded through css and specific xhtml content.

Source:
http://svn.webkit.org/repository/webkit/trunk/WebCore/platform/graphics/FontFallbackList.cpp
void FontFallbackList::determinePitch(const Font* font) const
{
    const FontData* fontData = primaryFontData(font);
    if (!fontData->isSegmented())                                                  // *** kaB00m!! (Apparently fontData can get corrupted)
        m_pitch = static_cast<const SimpleFontData*>(fontData)->pitch();
    else {
        const SegmentedFontData* segmentedFontData = static_cast<const SegmentedFontData*>(fontData);
        unsigned numRanges = segmentedFontData->numRanges();
        if (numRanges == 1)
            m_pitch = segmentedFontData->rangeAt(0).fontData()->pitch();
        else
            m_pitch = VariablePitch;
    }
}

Apparently, this happens in the wild too:
http://crash/search?query=stack_signature.contains:%22WebCore::FontFallbackList::determinePitch%22+stack_signature.contains:%22160602C%22

### sc...@gmail.com (2010-04-22)

GREAT bug @wushi!

I concur with SkyLined that this condition isn't just a security concern, but is also 
a stability concern. It's one of our top crashers:
http://crash/stackview?product=Chrome&version=4.1.249.1059&num=50
http://crash/reportview?
product=Chrome&version=4.1.249.1059&date=&signature=WebCore::FontFallbackList::determ
inePitch(WebCore::Font+const+*)-1606028&newsig=
http://crash/reportview?
product=Chrome&version=4.1.249.1059&date=&signature=WebCore::FontFallbackList::determ
inePitch(WebCore::Font+const+*)-134E8B3&newsig=

(The sum of those two distinct stack signals equates to one of the top crashers -- 
after discounting Flash plugin crashes)

### in...@chromium.org (2010-04-22)

putting this in my queue. will fix sometime next week, too much busy right now with
other webkit patches. marking milestone 5. 

### in...@chromium.org (2010-04-22)

filed bug in webkit. also affects safari

### in...@chromium.org (2010-04-22)

[Empty comment from Monorail migration]

### ma...@google.com (2010-04-23)

[Empty comment from Monorail migration]

### da...@chromium.org (2010-04-23)

[Empty comment from Monorail migration]

### dg...@chromium.org (2010-04-23)

[Empty comment from Monorail migration]

### dg...@chromium.org (2010-04-23)

What's the WebKit bug URL? Can you cc me there?

### dg...@chromium.org (2010-04-23)

Sato-san, can you look into this?

### in...@chromium.org (2010-04-23)

the webkit bug is https://bugs.webkit.org/show_bug.cgi?id=38001. i have cced Dimitri
and Yusuke.

### sc...@gmail.com (2010-04-23)

Since it's such a significant bug (in terms of the long-running stability impact), I 
also pinged a few Apple contacts. Hopefully someone will jump on it soon :)

### in...@chromium.org (2010-04-24)

this is now fixed in http://trac.webkit.org/changeset/58201.
i will merge this to 375 alongwith with other pending  merges.

### wo...@gmail.com (2010-04-24)

You guys are awesome! Analyze & Patching speed is so quickly.

### ma...@google.com (2010-04-26)

+cc anantha for testing

### an...@chromium.org (2010-04-26)

Sunand and Michael, We should verify this on tot and 375 after it gets patched.

### in...@chromium.org (2010-04-26)

This is now merged to both 249 and 375.
249:
http://src.chromium.org/viewvc/chrome?view=rev&revision=45544
375:
http://src.chromium.org/viewvc/chrome?view=rev&revision=45594

### sc...@gmail.com (2010-04-27)

Thanks, Wushi! This qualifies for an award.

### sc...@gmail.com (2010-04-29)

The security bug no longer reproduces in v4.1.249.1064 (yay!)
However, the stability-related crashes are still there :( e.g. 
http://crash/reportdetail?reportid=7f58c8a1caaf5938

Looks like there's a second condition in that same code whereby the font is simply 
NULL. Not a security condition, but irritating.

### sc...@gmail.com (2010-05-19)

(Not yet releasing - Safari not yet fixed, best I know)

### dg...@chromium.org (2010-05-28)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-06-13)

Releasing - Safari 5 is based on a recent WebKit revision so should have this fixed.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/42294?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Fonts]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080630)*
