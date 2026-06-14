# Security: scrollbar-corner can be drawn outside the containing frame, allowing redress of parent frame.

| Field | Value |
|-------|-------|
| **Issue ID** | [40078612](https://issues.chromium.org/issues/40078612) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | jo...@saynotolinux.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2013-12-31 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

Scrollbar corner rects are not constrained to the owning viewport, allowing child documents to draw over their parents by specifying overly large dimensions for ::webkit-scrollbar pseudo-elements.

An attacker may then selectively overlay their own content using a semi-transparent background-image for ::-webkit-scrollbar-corner, so long as it is above or to the left of the frame. Content may also be drawn below and to the right of the frame using box-shadow sprites.

This may be used to spoof content (as the location bar will remain the same, and any indicators RE: untrusted content being framed may be drawn over,) as well as to clickjack the parent frame via UI redress.

The attached patch fixes the issue in ScrollView::scrollCornerRect() by clamping the corner's rect to the viewport.

**VERSION**  

Chrome Version: 31.0.1650.63 stable  

Operating System: Ubuntu 13.04

**REPRODUCTION CASE**

A trivial example:

```
<html>  
<body>  
Hi <iframe width="1" height="1" srcdoc='  
<html><head><style>  
html,body { width:99999999px; height:9999999px;}  
::-webkit-scrollbar { height: 999999px; width: 999999px; }  
::-webkit-scrollbar-corner { background-color: red; box-shadow: 7px 7px green; }  
</style></head></html>  
'></iframe>  
</body>  
</html>  

```

`cr_scroll_content_spoofing.html` in the attached archive is an example of how this may be used to trick users on pages that frame semi/untrusted content.

An animated semi-transparent GIF is used for the corner's background-image so that it will be repainted every frame, to cover any repaints in the parent frame. The areas we want the user to use are made transparent so the usual caret and focus indicators will be show through the overlay, and users may click and enter text into them as usual. It also demonstrates that the framed document still receives click events as usual.

## Attachments

- [cr_scroll_content_spoofing.tar.gz](attachments/cr_scroll_content_spoofing.tar.gz) (application/x-gzip, 33.2 KB)
- [Clamp-scrollCornerRect-to-the-view-s-frameRect.patch](attachments/Clamp-scrollCornerRect-to-the-view-s-frameRect.patch) (application/octet-stream, 801 B)
- [scroll-corner-overflow.html](attachments/scroll-corner-overflow.html) (text/html, 384 B)
- [v2-Clip-FrameView-scrollbar-and-scrollcorner-paints-to-.patch](attachments/v2-Clip-FrameView-scrollbar-and-scrollcorner-paints-to-.patch) (application/octet-stream, 1.9 KB)
- [cr_active_content_spoofing.tar.gz](attachments/cr_active_content_spoofing.tar.gz) (application/x-gzip, 25.6 KB)

## Timeline

### mb...@chromium.org (2013-12-31)

Thanks for the report. Does anyone know who a good owner for this might be or want to take a look at the provided patch?

### [Deleted User] (2013-12-31)

[Empty comment from Monorail migration]

### [Deleted User] (2013-12-31)

Don't iframes already clip themselves always?  I would have expected them to. We'd have to look at how the layers for this attack are generated.

### [Deleted User] (2013-12-31)

I think the attached patch is fine.  But I also think that we want a stronger guarantee that x-origin iframes can't paint outside their designated region.

### [Deleted User] (2013-12-31)

Does the compositor have any notion of origins?  Presumably it will for OOPI?  Or should it always be blink's job to enforce that origin's don't create content outside of their designated content region?

### [Deleted User] (2013-12-31)

This also reproduces in Safari.

### [Deleted User] (2013-12-31)

I've turned your small test into a layout test (just shows green/red for pass/fail).  I haven't figured out how to get rid of the small black box in the lower right, it's one of the scroll pieces...

I don't think the proposed patch is quite right.  I think we should probably fix this by making FrameViews always clip all their children instead.

### jo...@saynotolinux.com (2013-12-31)

>I don't think the proposed patch is quite right.

I forgot about how I originally discovered it, a second testcase shows that the patch is insufficient:

    <html>
    <body>
        <iframe srcdoc="
            <html>
            <head><style>
            html{ height: 9999999px; width:999999px; }
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
                box-shadow: 20px 20px red;
            }
            ::-webkit-scrollbar-track { box-shadow:30px 30px blue; }
            ::-webkit-scrollbar-corner { box-shadow: 40px 40px red; }
            ::-webkit-scrollbar-button { box-shadow: 50px 50px orange; }
            ::-webkit-scrollbar-thumb { box-shadow: 60px 60px purple; }
            </style></head>
            </html>
        " width="100" height="100"></iframe>
    </body>
    </html>

> I think we should probably fix this by making FrameViews always clip all their children instead.

Mmm, there's no security implications re: overflow divs drawing outside their rect, and a patch in ScrollView would mess with them. I'll take a look at how to do this properly with FrameView. 

I think the scrollbar styling is a bit of a special case though, since the scoll pieces are considered part of the parent document but the framed content is allowed to style them. In most other cases content should be clipped correctly. Are there any other cases where elements in the parent may be styled from the child?

### jo...@saynotolinux.com (2014-01-01)

>I haven't figured out how to get rid of the small black box in the lower right, it's one of the scroll pieces...

I'm not sure which box you mean, the frame's border?


It looks like the box-shadow issues are going to be harder to fix, since they can be drawn outside an element's rect. The rect that FrameView::paintScrollbar passes to ScrollView::paintScrollbar is correct, but ScrollView::paintScrollbar calls ScrollbarTheme::paint which will paint outside the provided rect... There's similar issues with FrameView::paintScrollCorner.

Is there any way to make the scrollbar a child of the frame rather than a component of it, so any of its paints get clipped to the viewport?

### jo...@saynotolinux.com (2014-01-03)

patch v2, clips FrameView scrollbar / scrollCorner paints to the FrameView's rect per #7 .

### in...@chromium.org (2014-01-07)

[Empty comment from Monorail migration]

### jl...@chromium.org (2014-01-08)

eseidel@chromium.org: would you mind owning this bug?

### jl...@chromium.org (2014-01-10)

Julien, I hear you may be a good owner for this, so assigning to you. Feel free to re-assign of course.

### fe...@chromium.org (2014-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-19)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### jo...@saynotolinux.com (2014-01-25)

I initially thought that the frame couldn't receive input focus or display dynamic content while the scrollcorner was larger than its bounds, but that doesn't seem to be the case. We can paint onto a -webkit-canvas scrollcorner backgound and force repaints, and we can force the input focus to an element on the attacker's page.

Attached is an example of a spoofed login form that receives mouse and keyboard events in the framed document, and covers the framing document.

### cl...@chromium.org (2014-01-27)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-05)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### fe...@chromium.org (2014-02-05)

jchaffraix@, if you aren't the right owner, could you please suggest one? This is a medium-severity bug.

### cl...@chromium.org (2014-02-13)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-02-21)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-02)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### pa...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-03-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-11)

jchaffraix@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### jc...@chromium.org (2014-03-19)

Good owners are any rendering people (eseidel, leviw, eae, ...) as we don't have people who know the scrollbar code specifically.

I don't have any bandwidth for bugs that are not blocking a release.

### pa...@chromium.org (2014-03-19)

Hi Levi, here is a special fun present for you. :)

### cl...@chromium.org (2014-03-28)

leviw@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-03-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-02)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=170625

------------------------------------------------------------------
r170625 | leviw@chromium.org | 2014-04-02T02:15:16.043417Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/scrollbars/custom-scrollbars-paint-outside-iframe-expected.html?r1=170625&r2=170624&pathrev=170625
   A http://src.chromium.org/viewvc/blink/trunk/LayoutTests/scrollbars/custom-scrollbars-paint-outside-iframe.html?r1=170625&r2=170624&pathrev=170625
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollView.cpp?r1=170625&r2=170624&pathrev=170625

Clip Scrollbar painting like contents painting in ScrollView

Previously, it was possible to paint a scroll corner that was larger
than the iframe it was attached to, effectively enabling it to paint
over parts of the parent frame. This change clips scrollbar painting
the same way we clip contents.

BUG=331168

Review URL: https://codereview.chromium.org/220243010
-----------------------------------------------------------------

### le...@chromium.org (2014-04-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-04-02)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-17)

This can wait for M35 - merge requested.

### ka...@google.com (2014-04-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-04-21)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=172057

------------------------------------------------------------------
r172057 | leviw@chromium.org | 2014-04-21T18:33:41.981056Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/scrollbars/custom-scrollbars-paint-outside-iframe-expected.html?r1=172057&r2=172056&pathrev=172057
   A http://src.chromium.org/viewvc/blink/branches/chromium/1916/LayoutTests/scrollbars/custom-scrollbars-paint-outside-iframe.html?r1=172057&r2=172056&pathrev=172057
   M http://src.chromium.org/viewvc/blink/branches/chromium/1916/Source/platform/scroll/ScrollView.cpp?r1=172057&r2=172056&pathrev=172057

Merge 170625 "Clip Scrollbar painting like contents painting in ..."

> Clip Scrollbar painting like contents painting in ScrollView
> 
> Previously, it was possible to paint a scroll corner that was larger
> than the iframe it was attached to, effectively enabling it to paint
> over parts of the parent frame. This change clips scrollbar painting
> the same way we clip contents.
> 
> BUG=331168
> 
> Review URL: https://codereview.chromium.org/220243010

TBR=leviw@chromium.org

Review URL: https://codereview.chromium.org/245543002
-----------------------------------------------------------------

### ti...@chromium.org (2014-04-23)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-19)

Congratulations - $500 for this report! The release notes for v35 should be released tomorrow and we'll credit you as "Jordan Milne". A member of the Google finance team will be in contact in the next week or two to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### jo...@saynotolinux.com (2014-05-20)

#6 mentioned that WebKit was affected as well, are they planning to incorporate this patch?

### le...@chromium.org (2014-05-20)

They should. I'm traveling until next week. If someone else doesn't submit the patch before then, I'm happy to see about submitting it myself to WebKit sometime next week.

### dd...@apple.com (2014-05-20)

WebKit security bug:  <https://bugs.webkit.org/show_bug.cgi?id=133131>

Email me if you need access.


### le...@chromium.org (2014-05-27)

Hi ddkilzer. I don't necessarily need access, but are y'all taking care of porting it? If so I'm content :)

### dd...@apple.com (2014-05-27)

The WebKit bug is not actively being worked on at this time.  I've added you in case you want to work on it.


### cl...@chromium.org (2014-07-09)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

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

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/331168?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078612)*
