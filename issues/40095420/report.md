# More stale styles in listmarkers

| Field | Value |
|-------|-------|
| **Issue ID** | [40095420](https://issues.chromium.org/issues/40095420) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | in...@chromium.org |
| **Assignee** | in...@chromium.org |
| **Created** | 2011-09-22 |
| **Bounty** | $1,000.00 |

## Description

credit: miaubiz

<style>
li:before {
    content: "B";
}

@font-face { font-family: "A"; src: url(); }
body { font-family: A; }
</style>
  <li>C
  <ul> 
  </ul>
<script>
document.body.offsetTop;
document.body.style.color = "blue";
</script>

## Attachments

- [27b.html](attachments/27b.html) (text/html; charset=us-ascii, 536 B)
- [19b.html](attachments/19b.html) (text/plain; charset=us-ascii, 416 B)
- [first-letter.html](attachments/first-letter.html) (text/plain; charset=us-ascii, 150 B)
- [crashing-sep29.html](attachments/crashing-sep29.html) (text/html; charset=us-ascii, 609 B)
- [asan.txt](attachments/asan.txt) (text/x-c; charset=us-ascii, 12.3 KB)
- [asan1165.txt](attachments/asan1165.txt) (text/x-c; charset=us-ascii, 11.3 KB)
- [1165.html](attachments/1165.html) (text/html; charset=us-ascii, 412 B)

## Timeline

### in...@chromium.org (2011-09-22)

Upstreamed
https://bugs.webkit.org/show_bug.cgi?id=68624

### mi...@gmail.com (2011-09-23)

I think these are the same, but just in case :D

### mi...@gmail.com (2011-09-25)

first-letter instead of before. same thing.

### in...@chromium.org (2011-09-26)

Thanks a lot Miaubiz for the additional testcases.


### in...@chromium.org (2011-09-26)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-09-29)

Reopening since generic fix is not enough. There are certain cases where we can't delay font retirement, so like we need to fix these security bugs alongwith functional issue.

https://crbug.com/chromium/97599#c9 From mitz@webkit.org 2011-09-28 13:26:48 PST (-) [reply] 
I can see a reclacStyle(Force) taking place, with a brand new FontSelector, after the old FontSelector’s document is cleared. So the issue remains that style recalc is not updating all renderers as it should. I can’t think of a reasonable way to defer the font deletion in cases like this. We should just fix the style recalc bugs.

### mi...@gmail.com (2011-09-29)

putting this repro here where I think it belongs

### sc...@gmail.com (2011-10-03)

@miaubiz: thanks for uncovering these list marker issues! $1000 for this one too.

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

### mi...@gmail.com (2011-10-03)

but it's not even fixed yet :|

### sc...@gmail.com (2011-10-04)

Oh balls. Looks like a mix up between myself and Inferno. Still, seems like it'll be good for the reward once we fix it :)

### mi...@gmail.com (2011-10-04)

with vertical text orientation the stack changes

==4561== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffe38d050d at pc 0x7ffff3580ea2 bp 0x7fffffff69d0 sp 0x7fffffff68e0
READ of size 1 at 0x7fffe38d050d thread T0
    #0 0x7ffff3580ea2 in WebCore::InlineFlowBox::requiresIdeographicBaseline(WTF::HashMap<WebCore::InlineTextBox const*, std::pair<WTF::Vector<WebCore::SimpleFontData const*, 0ul>, WebCore::GlyphOverflow>, WTF::PtrHash<WebCore::InlineTextBox const*>, WTF::HashTraits<WebCore::InlineTextBox const*>, WTF::HashTraits<std::pair<WTF::Vector<WebCore::SimpleFontData const*, 0ul>, WebCore::GlyphOverflow> > > const&) const ???:0

<html>
  <head>
    <style>
      li:before {
        content: "B";
      }
      @font-face { font-family:"A"; src: url(); }
      li { font-family: A;
        -webkit-writing-mode:vertical-lr;
      }
    </style>
    C
    <style></style>
  </head>
  <body><li><ul></ul></li></body>
</html>
<script>
  document.designMode='on';
  document.execCommand('selectall');
  document.execCommand('italic');
</script>



### in...@chromium.org (2011-10-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-10-10)

http://trac.webkit.org/changeset/97075

### in...@chromium.org (2011-10-10)

merged to m15 in r97086

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/97599?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095420)*
