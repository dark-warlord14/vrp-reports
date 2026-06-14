# stale entries in gPercentHeightDescendantsMap

| Field | Value |
|-------|-------|
| **Issue ID** | [40089194](https://issues.chromium.org/issues/40089194) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | wo...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2011-03-23 |
| **Bounty** | $1,000.00 |

## Description

test on stable version 10.0.648.151, stack like this:

eax=007e77f0 ebx=007e76f8 ecx=007e792c edx=01299600 esi=007e792c edi=007e792c
eip=00200815 esp=0013ef94 ebp=0013eff4 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010246
00200815 ??              ???
1:018> k
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0013ef90 58e6879e 0x200815
0013efa0 58f170db WebCore::RenderObject::containingBlock+0xf
0013eff4 58f15e47 WebCore::RenderBlock::layoutBlockChildren+0x56
0013f078 58f15b2d WebCore::RenderBlock::layoutBlock+0x2fc
0013f088 58f174b5 WebCore::RenderBlock::layout+0x19
0013f0cc 58f172e1 WebCore::RenderBlock::layoutBlockChild+0x1b1
0013f134 58f15e47 WebCore::RenderBlock::layoutBlockChildren+0x25c
0013f1b8 58f15b2d WebCore::RenderBlock::layoutBlock+0x2fc
0013f1c8 58f174b5 WebCore::RenderBlock::layout+0x19
0013f20c 58f172e1 WebCore::RenderBlock::layoutBlockChild+0x1b1
0013f274 58f15e47 WebCore::RenderBlock::layoutBlockChildren+0x25c
0013f2f8 58f15b2d WebCore::RenderBlock::layoutBlock+0x2fc
0013f308 58e6ebf0 WebCore::RenderBlock::layout+0x19
0013f370 58e97007 WebCore::RenderView::layout+0x15a
0013f3bc 58e99192 WebCore::FrameView::layout+0x4e8
0013f3e0 58a62683 WebCore::FrameView::updateLayoutAndStyleIfNeededRecursive+0x34
0013f544 58a6260f RenderWidget::DoDeferredUpdate+0x59
0013f550 58a64056 RenderWidget::CallDoDeferredUpdate+0x9
0013f554 58a61bbe IPC::Message::Dispatch<RenderWidget,RenderWidget>+0x16
0013f58c 58a26a0e RenderWidget::OnMessageReceived+0x84

## Attachments

- [test0.html](attachments/test0.html) (text/html; charset=us-ascii, 924 B)

## Timeline

### in...@chromium.org (2011-03-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-23)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-03-23)

webkit bug - 
https://bugs.webkit.org/show_bug.cgi?id=56902

### in...@chromium.org (2011-03-23)

Fixed - http://trac.webkit.org/changeset/81786

### sc...@gmail.com (2011-03-24)

Merged to M11: http://trac.webkit.org/changeset/81885

### sc...@gmail.com (2011-04-14)

@wooshi - thanks, nice use-after-free with good repro, stack and registers. $1000.

### sc...@gmail.com (2011-04-14)

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

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-06)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/77130?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089194)*
