# Use after free in counters in :before, :after content

| Field | Value |
|-------|-------|
| **Issue ID** | [40095423](https://issues.chromium.org/issues/40095423) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | mo...@google.com |
| **Created** | 2011-09-22 |
| **Bounty** | $500.00 |

## Description

credit: miaubiz

This looks like a RenderCounter issue.

<style>
  :before {
    display: table-row-group;
    content: "A";
  }
    @font-face { font-family: "A"; src: url(); }
    body { width: 2ex; }
  div::after {
    content:counter(ctr) url(-);

  }
  .table-row::after { display:table-row; }
  </style>                              
</html>
<style>
</style>

<div class="table-row">A</div>

## Attachments

- [nextBreak.txt](attachments/nextBreak.txt) (text/x-c; charset=us-ascii, 11.8 KB)
- [nextBreak.html](attachments/nextBreak.html) (text/plain; charset=us-ascii, 198 B)
- [jump-to-0.html](attachments/jump-to-0.html) (text/plain; charset=us-ascii, 303 B)
- [vg-jump-to-0.txt](attachments/vg-jump-to-0.txt) (text/plain; charset=us-ascii, 3.6 KB)
- [jump-to-0.txt](attachments/jump-to-0.txt) (text/x-c; charset=us-ascii, 2.5 KB)
- [nextBreak-sep29.html](attachments/nextBreak-sep29.html) (text/html; charset=us-ascii, 357 B)
- [asan.txt](attachments/asan.txt) (text/x-c; charset=us-ascii, 11.8 KB)
- [after-first-letter.html](attachments/after-first-letter.html) (text/html; charset=us-ascii, 374 B)
- [after-first-letter.txt](attachments/after-first-letter.txt) (text/x-c; charset=us-ascii, 12.2 KB)
- [49_inside_136.txt](attachments/49_inside_136.txt) (text/x-c; charset=us-ascii, 8.6 KB)
- [0_inside_96.txt](attachments/0_inside_96.txt) (text/x-c; charset=us-ascii, 7.7 KB)
- [0_inside_208.html](attachments/0_inside_208.html) (text/html; charset=us-ascii, 501 B)
- [0_inside_96.html](attachments/0_inside_96.html) (text/html; charset=us-ascii, 502 B)
- [0_inside_104.html](attachments/0_inside_104.html) (text/html; charset=us-ascii, 467 B)
- [0_inside_208.txt](attachments/0_inside_208.txt) (text/x-c; charset=us-ascii, 8.3 KB)
- [0_inside_104.txt](attachments/0_inside_104.txt) (text/x-c; charset=us-ascii, 8.8 KB)
- [49_inside_136.html](attachments/49_inside_136.html) (text/html; charset=us-ascii, 558 B)
- deleted (application/octet-stream, 0 B)
- [104_inside_1208.txt](attachments/104_inside_1208.txt) (text/x-c; charset=us-ascii, 10.5 KB)
- [104_inside_1208.html](attachments/104_inside_1208.html) (text/html; charset=us-ascii, 507 B)
- [16_inside_1208.txt](attachments/16_inside_1208.txt) (text/x-c; charset=us-ascii, 10.3 KB)
- [16_inside_1208.html](attachments/16_inside_1208.html) (text/html; charset=us-ascii, 471 B)

## Timeline

### mi...@gmail.com (2011-09-25)

another similar

==28916== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffdf5279a0 at pc 0x7ffff391e4b2 bp 0x7fffffff5950 sp 0x7fffffff58e0
READ of size 2 at 0x7fffdf5279a0 thread T0
    #0 0x7ffff391e4b2 in WebCore::nextBreakablePosition(WebCore::LazyLineBreakIterator&, int, bool) ???:0
    #1 0x7ffff36b8c30 in WebCore::RenderBlock::LineBreaker::nextLineBreak(WebCore::BidiResolver<WebCore::InlineIterator, WebCore::BidiRun>&, WebCore::LineInfo&, std::pair<WebCore::RenderText*, WebCore::LazyLineBreakIterator>&, WebCore::RenderBlock::FloatingObject*, unsigned int) ???:0

0x7fffdf5279a0 is located 32 bytes inside of 34-byte region [0x7fffdf527980,0x7fffdf5279a2)
freed by thread T0 here:
    #0 0x7ffff5e296ba in free _asan_rtl_
    #1 0x7ffff38bc06f in WebCore::RenderText::setTextInternal(WTF::PassRefPtr<WTF::StringImpl>) ???:0
    #2 0x7ffff3962807 in WebCore::RenderCounter::computePreferredLogicalWidths(float) ???:0
    #3 0x7ffff38be7c2 in WebCore::RenderText::width(unsigned int, unsigned int, WebCore::Font const&, float, WTF::HashSet<WebCore::SimpleFontData const*, 

### mi...@gmail.com (2011-09-25)

putting this here, no use-after-free, just jump to 0..

==14234== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc (nil) sp 0x7fffffff9ab8 bp 0x7fffffff9f50 ax 0x7fffe07f5930 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x7ffff5e29d08 in ASAN_OnSIGSEGV _asan_rtl_
    #1 0x7fffeab30c60 in __restore_rt ??:0
    #2 0x7ffff362be8e in WebCore::RenderBlock::styleDidChange(WebCore::StyleDifference, WebCore::RenderStyle const*) ???:0





### in...@chromium.org (2011-09-26)

Thanks a lot Miaubiz for the additional testcases.

### in...@chromium.org (2011-09-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-29)

Reopening since generic fix is not enough. There are certain cases where we can't delay font retirement, so like we need to fix these security bugs alongwith functional issue.

https://crbug.com/chromium/97608#c9 From mitz@webkit.org 2011-09-28 13:26:48 PST (-) [reply] 
I can see a reclacStyle(Force) taking place, with a brand new FontSelector, after the old FontSelector’s document is cleared. So the issue remains that style recalc is not updating all renderers as it should. I can’t think of a reasonable way to defer the font deletion in cases like this. We should just fix the style recalc bugs.

### mi...@gmail.com (2011-09-29)

[Comment Deleted]

### in...@chromium.org (2011-09-29)

miaubiz: we need the counter repro in this one.

### mi...@gmail.com (2011-09-29)

right ;D 

sorry.



### in...@chromium.org (2011-09-30)

this might get fixed in mitz's fix in http://code.google.com/p/chromium/issues/detail?id=98556, https://bugs.webkit.org/show_bug.cgi?id=69088

### mi...@gmail.com (2011-10-05)

after, first-letter, p tag, no counter, no lists

### mi...@gmail.com (2011-10-06)

c#0 doesnt repro for me. nextBreak is still there.  should I put c#10 as different bug?

### mi...@gmail.com (2011-10-06)

I put c#10 in http://code.google.com/p/chromium/issues/detail?id=99294

### mi...@gmail.com (2011-10-06)

and I put nextbreakable in: 

http://code.google.com/p/chromium/issues/detail?id=99296



### in...@chromium.org (2011-10-06)

Your repro in https://crbug.com/chromium/99296 is already posted upstream, we know that generic fix fixes c#0 testcase. So, we will use this bug for reference.

### in...@chromium.org (2011-10-06)

[Empty comment from Monorail migration]

### mi...@gmail.com (2011-10-10)

some alternate stacks...



### mi...@gmail.com (2011-10-10)

49_inside_136.html has counters.  the others don't.

### mi...@gmail.com (2011-10-11)

the others got killed since yesterday, maybe by the first-letter/table fix.

### in...@chromium.org (2011-10-11)

We have massacred many :before, :after bugs in the last couple of days. Can you please refresh to trunk and tell which counter specific ones are remaining with their minimized counterparts.

### mi...@gmail.com (2011-10-11)

atleast:
<html>
  <head>
    <style>
      @font-face { 
        font-family: A; 
        src: url();
      }

      div#inner {
        font-family: A;
        display: table-row;
      }

      div#inner:before {
        content: ""; 
      }

      div#inner:after {
        content:"";
      }

      div#outer {
        display: table;
      }

      div#outer:before {
        content: counter(c); 
        display: table-row;
      }
    </style>
  </head>        
  <body>
    <div id="outer">
      <div id="inner">
      </div>
    </div>
  </body>
</html>

aka 49_inside_136.html is live with trunk.

have to check about others

### in...@chromium.org (2011-10-11)

by trunk you mean >=webkit r97124. by this exercise, i seem to find/fix counter specific bugs. 

### mi...@gmail.com (2011-10-11)

I'm on 97126 yeah ;)

### mi...@gmail.com (2011-10-11)

and of course nextBreak.html 

### mi...@gmail.com (2011-10-11)

here's a 104 inside 1208 with counters..



### mi...@gmail.com (2011-10-11)

that had two extra colons

### mi...@gmail.com (2011-10-11)

here's the counterless counterpart

### in...@chromium.org (2011-10-11)

c#26 is fixed by http://code.google.com/p/chromium/issues/detail?id=99880.

### in...@chromium.org (2011-10-13)

This has some testcases different from stale font bugs. These will still reproduce after 100059. We need to fix counter rendering logic issues.

### in...@chromium.org (2011-10-20)

Now fixed with http://trac.webkit.org/changeset/97927

### in...@chromium.org (2011-10-20)

[Empty comment from Monorail migration]

### ke...@google.com (2011-10-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-25)

@miaubiz: sifting through this one, it turns out that one of the repros provided was very useful in fixing an existing bug we were tracking. Hence, a $500 reward!

### sc...@gmail.com (2012-02-15)

[Empty comment from Monorail migration]

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/97608?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/98672, crbug.com/chromium/99296]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095423)*
