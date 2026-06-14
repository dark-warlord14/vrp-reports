# Use-after-free when font is missing

| Field | Value |
|-------|-------|
| **Issue ID** | [40095584](https://issues.chromium.org/issues/40095584) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2011-09-26 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

continued

**VERSION**  

Chrome Version:  

Chromium 16.0.893.0 (Developer Build 102749)  

OS Linux  

WebKit 535.5 (trunk@95959)

Operating System: 64bit linux

**REPRODUCTION CASE**  

attached

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==25708== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe39b3890 at pc 0x7ffff378700a bp 0x7fffffff5490 sp 0x7fffffff5460  

READ of size 4 at 0x7fffe39b3890 thread T0  

#0 0x7ffff378700a in WebCore::RenderInline::baselinePosition(WebCore::FontBaseline, bool, WebCore::LineDirectionMode, WebCore::LinePositionMode) const ???:0  

#1 0x7ffff3913c16 in WebCore::RootInlineBox::ascentAndDescentForBox(WebCore::InlineBox\*, WTF::HashMap<WebCore::InlineTextBox const\*, std::pair<WTF::Vector<WebCore::SimpleFontData const\*, 0ul>, WebCore::GlyphOverflow>, WTF::PtrHash<WebCore::InlineTextBox const\*>, WTF::HashTraits<WebCore::InlineTextBox const\*>, WTF::HashTraits<std::pair<WTF::Vector<WebCore::SimpleFontData const\*, 0ul>, WebCore::GlyphOverflow> > >&, int&, int&, bool&, bool&) const ???:0

0x7fffe39b3890 is located 16 bytes inside of 1208-byte region [0x7fffe39b3880,0x7fffe39b3d38)  

freed by thread T0 here:  

#0 0x7ffff5e2749a in free *asan\_rtl*  

#1 0x7ffff359f4ed in WebCore::CSSFontFaceSource::pruneTable() ???:0  

#2 0x7ffff359f731 in WebCore::CSSFontFaceSource::fontLoaded(WebCore::CachedFont\*) ???:0

## Attachments

- [stil26.txt](attachments/stil26.txt) (text/x-c; charset=us-ascii, 12.9 KB)
- [still26.html](attachments/still26.html) (text/plain; charset=us-ascii, 282 B)
- [jump-to-0.txt](attachments/jump-to-0.txt) (text/x-c; charset=us-ascii, 2.5 KB)
- [vg-jump-to-0.txt](attachments/vg-jump-to-0.txt) (text/plain; charset=us-ascii, 3.6 KB)
- [jump-to-0.html](attachments/jump-to-0.html) (text/plain; charset=us-ascii, 303 B)
- [crashing-sep29.html](attachments/crashing-sep29.html) (text/html; charset=us-ascii, 609 B)
- [asan.txt](attachments/asan.txt) (text/x-c; charset=us-ascii, 12.3 KB)

## Timeline

### mi...@gmail.com (2011-09-26)

jump to 0

==25941== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc (nil) sp 0x7fffffff9ab8 bp 0x7fffffff9f50 ax 0x7fffe07f0930 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x7ffff5e27ae8 in ASAN_OnSIGSEGV _asan_rtl_
    #1 0x7fffeab2bc60 in __restore_rt ??:0
    #2 0x7ffff362810e in WebCore::RenderBlock::styleDidChange(WebCore::StyleDifference, WebCore::RenderStyle const*) ???:0
    #3 0x7ffff386c1b2 in WebCore::RenderTable::styleDidChange(WebCore::StyleDifference, WebCore::RenderStyle const*) ???:0
    #4 0x7ffff383eb4e in WebCore::RenderObject::setStyle(WTF::PassRefPtr<WebCore::RenderStyle>) ???:0


### in...@chromium.org (2011-09-26)

If you see the stack, you will realize, we need to fix this in Mitz' patch - http://trac.webkit.org/changeset/94508. the crash stack hasn't changed after my fix http://trac.webkit.org/changeset/95959 because the underlying r94508 wasn't able to delay the font retirement.

### in...@chromium.org (2011-09-27)

Upstreamed - https://bugs.webkit.org/show_bug.cgi?id=68929

### in...@chromium.org (2011-09-29)

This is again a specific fix and not a generic one.
http://trac.webkit.org/changeset/96294

### mi...@gmail.com (2011-09-29)

here's the repro that is still crashing

### mi...@gmail.com (2011-09-29)

asan log for that 

### in...@chromium.org (2011-09-29)

merged to m15 in r96369

### in...@chromium.org (2011-09-29)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-19)

Thanks for all these stale style bugs, miaubiz. We think we've got a good defense now to making these stale style bugs unexploitable, but we'll pay $1000 per well-reported bug up until that point. $1000 for this one. Forgive the brevity on upcoming rewards :)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/98064?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095584)*
