# Memory corruption with crash in RenderObject::containingBlock()

| Field | Value |
|-------|-------|
| **Issue ID** | [40081897](https://issues.chromium.org/issues/40081897) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ja...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2010-06-29 |
| **Bounty** | $500.00 |

## Description

I found a new bug, probably different to previous reports because I deleted of my fuzzer: keygen html tag, border-radius (and their variants) and counter-increment, etc (you know, other issues).

I had problems to reproduce the issue and I didn't reduce it (I will try it with next comments)...

I've attached two different stacktraces and files (logs from my fuzzer)

Steps to reproduce (strange? I know):

First method (long and more likely)
------------------------------------

1.- Open Browser (tested on Google Chrome 5.0.375.86)
2.- Add to browser the file: fuzz-11...
3.- Add to browser the file: fuzz-10...
4.- Add to browser the file: fuzz-9...
5.- Add to browser the file: fuzz-x...
...
6.- Finally, add to browser the file: fuzz-3 and Crash!

Second method (short and less likely)
------------------------------------

I've reduced the root cause to files: fuzz-7 and fuzz-3:

1.- Open Browser (tested on Google Chrome 5.0.375.86)
3.- Add to browser the file: fuzz-7
4.- Add to browser the file: fuzz-3
5.- Repeat 3 and 4 steps (until crash)

Maybe this second method doesn't crash the browser, so try it again (fuzz-7 -> fuzz-3, fuzz-7 -> fuzz-3, fuzz-7 -> fuzz-3, ...)

In summary, issue are fuzz-7 and fuzz-3

I will try to reduce the problem in future comments ;)

Final note: I've already tested on 6.0.447.0 dev and it works (second method)




## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [crash.zip](attachments/crash.zip) (application/zip, 1.1 KB)
- [crash_containingBlock.html](attachments/crash_containingBlock.html) (text/html, 581 B)
- [1.html](attachments/1.html) (text/plain; charset=us-ascii, 87 B)
- [2.html](attachments/2.html) (text/plain; charset=us-ascii, 94 B)

## Timeline

### js...@chromium.org (2010-06-29)

@javg0x83 - I suggest that you look at the information here on configuring your debugger:
http://dev.chromium.org/developers/how-tos/debugging

Specifically, you should configure your debugger to use Chrome's symbol server. It would make your stack traces mush more useful.


### ja...@gmail.com (2010-06-29)

Oops! I've been worried to get the repro-files method and I don't notice that first stack-trace has not symbols. I'm not using debugger, it's only copied from Dr. Watson report. @jsc...: I read it ;)

### js...@chromium.org (2010-06-29)

This is a real quick hack and slash, but I've reduced to two smaller files that trigger the corruption. I'm typically getting a NULL deref crash with the following stack on trunk. However, I'm also getting numerous bad pointers in referenced objects and one run overwrote ESP. So, there's definitely memory corruption here.

WebCore::RenderObject::containingBlock()  Line 597
WebCore::RenderBlock::paintContinuationOutlines()  Line 2344
WebCore::RenderBlock::paintObject()  Line 2232
WebCore::RenderBlock::paint()  Line 1980
WebCore::RenderLayer::paintLayer()  Line 2447
WebCore::RenderLayer::paintList()  Line 2499
WebCore::RenderLayer::paintLayer()  Line 2468
WebCore::RenderLayer::paint()  Line 2252
WebCore::FrameView::paintContents()  Line 1943
WebCore::ScrollView::paint()  Line 797
WebCore::RenderWidget::paint()  Line 281
WebCore::InlineBox::paint()  Line 180
WebCore::InlineFlowBox::paint()  Line 682
WebCore::RootInlineBox::paint()  Line 167
WebCore::RenderLineBoxList::paint()  Line 219
WebCore::RenderBlock::paintContents()  Line 2090
WebCore::RenderBlock::paintObject()  Line 2199
WebCore::RenderBlock::paint()  Line 1980
WebCore::RenderBlock::paintChildren()  Line 2127
WebCore::RenderBlock::paintContents()  Line 2092
WebCore::RenderBlock::paintObject()  Line 2199
WebCore::RenderBlock::paint()  Line 1980
WebCore::RenderLayer::paintLayer()  Line 2445
WebCore::RenderLayer::paintList()  Line 2499
WebCore::RenderLayer::paintLayer()  Line 2468
WebCore::RenderLayer::paint()  Line 2252
WebCore::FrameView::paintContents()  Line 1943
WebCore::ScrollView::paint()  Line 797
WebKit::WebFrameImpl::paintWithContext()  Line 1795
WebKit::WebFrameImpl::paint()  Line 1818
WebKit::WebViewImpl::paint()  Line 979
RenderWidget::PaintRect()  Line 390
RenderWidget::DoDeferredUpdate()  Line 501
RenderWidget::CallDoDeferredUpdate()  Line 428


### js...@chromium.org (2010-06-29)

I've trimmed down the repro to the following HTML:

<dialog style='position:relative'>
  <h style='outline-style:auto'>X<div></div></h>
</dialog>

I'm getting it to trigger by alternating between setting an iframe body to the above and then clearing it. The second file in the original repro was unnecessary; it looks like it just needed a navigation to trigger a repaint. It triggers in both Safari 5 and WebKit Nightly. Filed upstream as:
https://bugs.webkit.org/show_bug.cgi?id=41373

@jamesr - mind taking a look at this?


### ja...@gmail.com (2010-06-30)

@jsc...: I've got symbols for windbg :)
Btw: Great reduction

just my repro-method

1.- Google Chrome -> Automatic (take several seconds): Open file 1.html
2.- Safari -> Open file 1.html and then twice Ctrl+T 

Note: 1.html contains an iframe with meta tag redirection. 2.html just contains #4


### ja...@gmail.com (2010-07-03)

I've checked this bug and it's alive with new stable release: 5.0.375.99. (I thought that issue may had been left for get fixed...) 

### ja...@gmail.com (2010-07-08)

[Comment Deleted]

### in...@chromium.org (2010-07-08)

I am working on the fix. Jose, this bug is already marked SecSeverity-High because of the memory corruption involved. We are looking to see if this is eligible for the reward.

### in...@chromium.org (2010-07-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-08)

Yep, this provisionally qualifies for a reward - congrats! We're working on the fix, and rewards are typically issued after we release the fix to users.

### ja...@gmail.com (2010-07-08)

Thanks for quick response

### in...@chromium.org (2010-07-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-07-09)

Switching the owner back to security@, because Mitz is looking at this upstream.

### in...@chromium.org (2010-07-10)

Fixed in <http://trac.webkit.org/changeset/63048>.

### in...@chromium.org (2010-07-14)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-07-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=52365 

------------------------------------------------------------------------
r52365 | inferno@chromium.org | 2010-07-14 11:53:02 -0700 (Wed, 14 Jul 2010) | 33 lines
Changed paths:
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/fast/inline/continuation-outlines-with-layers-2.html
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/platform/mac/fast/inline/continuation-outlines-with-layers-2-expected.checksum
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/platform/mac/fast/inline/continuation-outlines-with-layers-2-expected.png
   A http://src.chromium.org/viewvc/chrome/branches/WebKit/375/LayoutTests/platform/mac/fast/inline/continuation-outlines-with-layers-2-expected.txt
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/rendering/InlineFlowBox.cpp?r1=52365&r2=52364
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/rendering/RenderBlock.cpp?r1=52365&r2=52364
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/rendering/RenderObject.cpp?r1=52365&r2=52364
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/rendering/RenderObject.h?r1=52365&r2=52364

Merge 63048 - <rdar://problem/8153214> Continuation outlines in layers do not paint correctly

Reviewed by Anders Carlsson.

WebCore: 

Test: fast/inline/continuation-outlines-with-layers-2.html

Continuation outlines are normally painted by the containing block. However, when the
block and the inline are not enclosed by the same self-painting layer, the inline has to
paint its own outlines. This was handled correctly only for the case where the inline had
its own self-painting layer, but now when an ancestor inline had the self-painting layer.

* rendering/InlineFlowBox.cpp:
(WebCore::InlineFlowBox::paint): Instead of testing for having a self-painting layer, test
whether any intermediate box between the inline and the containing block has a self-painting
layer.
* rendering/RenderBlock.cpp:
(WebCore::RenderBlock::paintObject): Ditto.
* rendering/RenderObject.cpp:
(WebCore::RenderObject::enclosingBoxModelObject): Added this utility method.
* rendering/RenderObject.h:

LayoutTests: 

* fast/inline/continuation-outlines-with-layers-2.html: Added.
* platform/mac/fast/inline/continuation-outlines-with-layers-2-expected.checksum: Added.
* platform/mac/fast/inline/continuation-outlines-with-layers-2-expected.png: Added.
* platform/mac/fast/inline/continuation-outlines-with-layers-2-expected.txt: Added.

BUG=47866

Review URL: http://codereview.chromium.org/2975015
------------------------------------------------------------------------


### bu...@gmail.com (2010-07-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=52374 

------------------------------------------------------------------------
r52374 | inferno@chromium.org | 2010-07-14 12:39:47 -0700 (Wed, 14 Jul 2010) | 4 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/WebKit/375/WebCore/rendering/InlineFlowBox.cpp?r1=52374&r2=52373

Fix Build

BUG=47866

------------------------------------------------------------------------


### [Deleted User] (2010-07-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2010-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2010-07-21)

[Comment Deleted]

### [Deleted User] (2010-07-21)

[Comment Deleted]

### sc...@gmail.com (2010-08-03)

@javg0x83: please e-mail me at cevans@chromium.org for steps on collecting your reward :)

### sc...@gmail.com (2010-08-10)

Reward should be on its way. Thanks @javg0x83

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

This issue was migrated from crbug.com/chromium/47866?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081897)*
