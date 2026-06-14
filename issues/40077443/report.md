# ASSERTION FAILED: run.charactersLength() >= run.length(), Heap-buffer-overflow in WebCore::Font::characterRangeCodePath

| Field | Value |
|-------|-------|
| **Issue ID** | [40077443](https://issues.chromium.org/issues/40077443) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | aa...@google.com |
| **Assignee** | sc...@chromium.org |
| **Created** | 2013-04-20 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=179368951

Fuzzer: Miaubiz_svg_fuzzer

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x600800117bf4
Crash State:
  - crash stack -
  WebCore::Font::characterRangeCodePath
  WebCore::Font::drawText
  WebCore::SVGInlineTextBox::paintTextWithShadows
  

Minimized Testcase (9.60 Kb): https://cluster-fuzz.appspot.com/download/AMIfv947xLyZEJ_4hM7siGmxQipj5Vulne79FxkGujpHBd4IuWoDRXQpoQ7NW7rtgQBlQQV53p8S_SM3A3weIaCk2HN8ZGL1qsFXScc9I7zefiHkePJFItwB0lJmp5AoAEHJNVPWwgpCJhZeA0xG-jRyTjv_9cRMmBKWyvFBIaL11hD61BRI41M

## Attachments

- [cr233848-minimized.html](attachments/cr233848-minimized.html) (text/html; charset=us-ascii, 916 B)

## Timeline

### in...@chromium.org (2013-04-20)

[Empty comment from Monorail migration]

### sc...@chromium.org (2013-04-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-04-21)

[Comment Deleted]

### in...@chromium.org (2013-04-21)

Ignore the last ClusterFuzz which says fixed in range "195296:195394". Looks like a bad build sneeked in [clang roll] and ASAN stopped working. Things look fine on trunk, so i clicked redo on ClusterFuzz reports.

### cl...@chromium.org (2013-04-21)

[Comment Deleted]

### sc...@chromium.org (2013-04-22)

That's least minimized minimization possible. :-(

Debug assertion hits. Not surprising that it's a buffer read overflow.

ASSERTION FAILED: run.charactersLength() >= run.length()
../../third_party/WebKit/Source/core/rendering/svg/SVGInlineTextBox.cpp(450) : WebCore::TextRun WebCore::SVGInlineTextBox::constructTextRun(WebCore::RenderStyle *, const WebCore::SVGTextFragment &) const

Now I'll try to really minimize it.

### sc...@chromium.org (2013-04-22)

Discovered during minimization: This will hit different asserts depending on which lines are added/removed. There may be more than one problem here.

### sc...@chromium.org (2013-04-22)

This is another instance of two SVG roots in a single page, with a text-related element in the first root using a filter from the second, and layout leaving the first SVG root marked as needing layout but not laid out.

That is, https://code.google.com/p/chromium/issues/detail?id=231618

I suspect that the fix there does not fix things here do to the unicode characters in the text path.

### in...@chromium.org (2013-04-28)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=180641586

Fuzzer: Miaubiz_svg_fuzzer

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x6050002e4a9a
Crash State:
  - crash stack -
  WebCore::Font::characterRangeCodePath
  WebCore::Font::selectionRectForText
  WebCore::SVGInlineTextBox::selectionRectForTextFragment
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=116390:116434

Minimized Testcase (8.62 Kb): https://cluster-fuzz.appspot.com/download/AMIfv960yWT48cx_p8JD01fu7Nj7Ti-cinzfRPHltqKsV77o0p73bebpjphGuaq0QNAoWo24myUnsKCFDJdRowCdKtdg7Wa9EQ-hxvWmR8qci1YFuOmVNITajR8lsWK0R2kbeSC64xdWouQBh98xOm62V9EK7aiN97kTyzMthnzbHan94x-Fuo4

### in...@chromium.org (2013-05-02)

Please do read Mark's email titled "Calling a Code 28 for Security Bugs" on chrome-team mailing list.

### pa...@chromium.org (2013-05-09)

Hey Stephen, are you still OK to own this one (in addition to https://code.google.com/p/chromium/issues/detail?id=231618) too?

### sc...@chromium.org (2013-05-09)

I think I should still own it. I don't know who else would be willing to deal with it. I'm finishing up another task and then it's on to this.

### sc...@chromium.org (2013-05-14)

Patch up: https://codereview.chromium.org/15183002/

I am not sure that this fixes every issue with the "minimized" not so minimized test. Various attempts to minimize it led to different assertions and maybe some of those are still problems.

### in...@chromium.org (2013-05-15)

https://src.chromium.org/viewvc/blink?view=rev&revision=150456

### bu...@chromium.org (2013-05-15)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/blink?view=rev&rev=150456

------------------------------------------------------------------------
r150456 | schenney@chromium.org | 2013-05-15T22:41:19.026846Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/SVGInlineTextBox.cpp?r1=150456&r2=150455&pathrev=150456
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/SVGRootInlineBox.h?r1=150456&r2=150455&pathrev=150456
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/unicode-in-tspan-multi-svg-crash-expected.txt?r1=150456&r2=150455&pathrev=150456
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/rendering/svg/SVGInlineTextBox.h?r1=150456&r2=150455&pathrev=150456
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/svg/custom/unicode-in-tspan-multi-svg-crash.html?r1=150456&r2=150455&pathrev=150456

Clear SVGInlineTextBox fragments when the text changes.

This patch modifies SVGInlineTextBox::dirtyLineBoxes to clear all
following text boxes when invoked. Typically this method is called
when the underlying text string changes, and that change needs to
be propagated to all the boxes that use the text beyond the point
where the text is first modified.

Also cleans up virtual, OVERRIDE and FINAL for SVGRootInlineBox, which was all messed up.

R=inferno@chromium.org,leviw@chromium.org
BUG=233848

Review URL: https://chromiumcodereview.appspot.com/15183002
------------------------------------------------------------------------

### sc...@gmail.com (2013-05-28)

Since this is Medium, we can let it hit M28.
M28: r151288

### pa...@chromium.org (2013-06-27)

$500 for this one!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### pa...@chromium.org (2013-06-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-07-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-07-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/233848?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077443)*
