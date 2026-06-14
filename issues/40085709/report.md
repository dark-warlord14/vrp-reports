# Security: Omnibox scrolls RTL domains off-screen (spoofing)

| Field | Value |
|-------|-------|
| **Issue ID** | [40085709](https://issues.chromium.org/issues/40085709) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | ja...@gmail.com |
| **Assignee** | mg...@chromium.org |
| **Created** | 2016-10-16 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: 56.0.2891.0  

Operating System: Windows

**REPRODUCTION CASE**  

Open <http://xn--nebl.xn--9dbq2a/%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20https://www.google.com/search?q=khalil&biw=1360&bih=700&source=lnms&tbm=isch&sa=X&ved=0ahUKEwig9dC0rd7PAhUFshQKHU0JAngQ_AUIBigB=mobile%20%20%20%20%20%20%20%20%20%20%20%20%20>

## Attachments

- deleted (application/octet-stream, 0 B)
- [screenshot.png](attachments/screenshot.png) (image/png, 70.1 KB)
- [Link.txt](attachments/Link.txt) (text/plain, 263 B)
- [rtl-url-scroll.png](attachments/rtl-url-scroll.png) (image/png, 6.6 KB)
- [omnibox-scrolled-correctly.png](attachments/omnibox-scrolled-correctly.png) (image/png, 9.1 KB)
- [url-middle-out-origin.png](attachments/url-middle-out-origin.png) (image/png, 6.3 KB)
- [Spoofable RTL URLs.png](attachments/Spoofable RTL URLs.png) (image/png, 212.5 KB)
- [Screenshot_20161206-115024.png](attachments/Screenshot_20161206-115024.png) (image/png, 73.1 KB)
- [IMG_3682.jpg](attachments/IMG_3682.jpg) (image/jpeg, 66.3 KB)
- [Screen Shot 2016-12-06 at 14.06.39.png](attachments/Screen Shot 2016-12-06 at 14.06.39.png) (image/png, 156.4 KB)

## Timeline

### ja...@gmail.com (2016-10-16)

[Empty comment from Monorail migration]

### ja...@gmail.com (2016-10-16)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-10-17)

Thanks for your report.

mgiuca@, could you please take a look and help to triage this? I've seen that you were an owner for similar issues in the past (https://crbug.com/chromium/630481, https://crbug.com/chromium/624213, https://crbug.com/chromium/499933).

I'm setting Medium severity for now (as Medium has been assigned to the previous reports).

[Monorail components: Security>UX UI>Browser>Omnibox]

### mm...@chromium.org (2016-10-17)

[Empty comment from Monorail migration]

### mg...@chromium.org (2016-10-18)

I was able to reproduce in certain cases (not exactly sure yet what the trigger is). But more information would be helpful.

In particular, I'm unclear on why this bug is titled "U+FE70". The repro case has nothing to do with U+FE70 ARABIC FATHATAN ISOLATED FORM from what I can tell; I've gone through to make sure and it doesn't look like that character appears anywhere in the URL in encoded or decoded form.

I can repro on Linux and Windows, but not on a 1920x1080 display. By making the window smaller, it becomes reproducible (note that the above screenshot is 906x512). Or by adding a bunch more %20s onto the end, it can be reproduced at 1920 width.

What's actually happening is that the text field is being scrolled horizontally such that "https://www.google.com..." is exactly aligned along the left edge, and the real domain is not visible. Note that it isn't simply being right-aligned. It's explicitly aligning the LTR part of the URL to the left edge. I can't explain why that will happen but I will investigate.

### mg...@chromium.org (2016-10-18)

Bit of a simpler repro case:

http://xn--nebl.xn--9dbq2a/0abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz

(Works on 1920 width; keep adding letters to the end until it overflows the width on your monitor.)

### mg...@chromium.org (2016-10-18)

This only happens after you select the text and hit Enter (not upon first navigation). Here's the stack trace that causes the weird display offset in RenderText:

#1 0x7f954d253d0f gfx::RenderText::SetDisplayOffset()
#2 0x7f954d253ba5 gfx::RenderText::GetUpdatedCursorBounds()
#3 0x7f9549b5e636 views::Textfield::UpdateAfterChange()
#4 0x7f9550132db5 OmniboxViewViews::OnBlur()
#5 0x7f9549b6fd0a views::FocusManager::SetFocusedViewWithReason()
#6 0x7f954c450b74 content::WebContentsImpl::NotifyWebContentsFocused()
#7 0x7f954c351b1e content::RenderWidgetHostImpl::GotFocus()
#8 0x7f954c3604f8 content::RenderWidgetHostViewAura::OnWindowFocused()
#9 0x7f9549970760 wm::FocusController::SetFocusedWindow()
#10 0x7f9549970227 wm::FocusController::FocusAndActivateWindow()
#11 0x7f9549c3b449 aura::Window::Focus()
#12 0x7f9550087637 chrome::Navigate()
#13 0x7f955008070f chrome::OpenCurrentURL()
#14 0x7f955007f0b6 chrome::BrowserCommandController::ExecuteCommandWithDisposition()
#15 0x7f955075c6e2 CommandUpdater::ExecuteCommand()
#16 0x7f95501ea7d5 ChromeOmniboxEditController::OnAutocompleteAccept()
#17 0x7f9550a40de1 OmniboxEditModel::OpenMatch()
#18 0x7f9550a43f47 OmniboxView::OpenMatch()
#19 0x7f9550a402e1 OmniboxEditModel::AcceptInput()
#20 0x7f95501334f6 OmniboxViewViews::HandleKeyEvent()
#21 0x7f9549b601a1 views::Textfield::OnKeyPressed()
#22 0x7f9549b7fb50 views::View::OnKeyEvent()

Investigating...

### mg...@chromium.org (2016-10-18)

There are a few hidden steps of the stack trace due to inlining. Here is the full stack trace up to OnBlur:

#1 gfx::RenderText::SetDisplayOffset()
#2 gfx::RenderText::UpdateCachedBoundsAndOffset()
#3 gfx::RenderText::GetUpdatedCursorBounds()
#4 views::Textfield::RepaintCursor()
#5 views::Textfield::UpdateAfterChange()
#6 views::Textfield::SelectRange()
#7 OmniboxViewViews::OnBlur()

Firstly, I think it's disgusting that this offset update happens as part of a deliberate side-effect of GetUpdatedCursorBounds(), which happens as a deliberate side-effect of RepaintCursor(). That's insanely hard to follow.

OK so here's what's happening (see attachment for illustration):

The algorithm for deciding on the default horizontal scroll for the Omnibox after hitting Enter is:
1. Scroll all the way to the right (for some reason I haven't gotten into). This happens before OnBlur.
2. Text field loses focus.
3. OmniboxViewViews::OnBlur: Position the cursor at column 0, explicitly to "make sure the beginning of the text is visible."
4. RenderText::UpdateCachedBoundsAndOffset: Scrolls the textfield horizontally such that the cursor is visible.

Every piece works as intended, but the overall effect is not what we want: when bidirectional text is involved, column 0 is *not necessarily* the leftmost thing. See the image: here column 0 is to the right of the domain and to the left of the path. When we scroll the textfield from the rightmost part to *just* get the cursor on-screen, we end up aligning column 0 (the dotted red line in my image) with the left edge, pushing the domain fully off-screen.

Note that we can't guarantee the domain will be on the left side either, so just making sure the leftmost part is visible is not the right answer. Perhaps the right fix here is to simply select the *entire* domain, rather than just placing the cursor at the beginning of the domain. I think then RenderText::UpdateCachedBoundsAndOffset will do the Right Thing.

+pkasting, jshin

### mg...@chromium.org (2016-10-18)

Yes, doing that fixes it (see image of the original repro case). I had to do a weird two-step hack:
1. First select the domain. This ensures that the domain is on-screen.
2. Place the cursor at the start of the domain with an empty selection. This means there is no text selected afterwards (otherwise there is weird behaviour when you click the domain).

So this is a bit of a hack.

### sh...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-18)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@gmail.com (2016-10-18)

Can someone please Cc Khalil Zhani "chromium.khalil@gmail.com" (my partner).


### aw...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### pk...@chromium.org (2016-10-18)

Would any of this be less nasty in a future world where we addressed the "how should BiDi URLs be physically displayed" issues, so that we knew e.g. that the domain was actually the leftmost thing?  It seems like the screenshot in https://crbug.com/chromium/656417#c8 is all kinds of bad from a usability perspective, and while we can try to work around this for now, anything we do is going to be imperfect.

My inclination is to try and ask the textfield to scroll the "leading edge" of the text into view, wherever that maps to logically, because that will avoid putting the physical middle of the string at the start of the control.  But perhaps this is also problematic if someone can place arbitrary amounts of text on each physical side of the domain.

If indeed this doesn't work, then the hack you suggest is the right thing for now.

### mg...@chromium.org (2016-10-18)

> Would any of this be less nasty in a future world where we addressed the "how should BiDi URLs be physically displayed" issues, so that we knew e.g. that the domain was actually the leftmost thing?

Yes. My fix for https://crbug.com/chromium/351639 would mean the origin is always on the left. That wouldn't implicitly fix this issue, but it would mean that simply scrolling all the way to the left would be fine.

> But perhaps this is also problematic if someone can place arbitrary amounts of text on each physical side of the domain.

Yes that's a good point. The repro case for this is:
http://xn--nebl.xn--9dbq2a/0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz

The origin gets placed in between the numbers and the letters (see screenshot). However, scrolling all the way to the left in this case would be *okay* for spoofing because you can't put any RTL characters to the left of the domain (as soon as an RTL character is encountered, it moves to the right of the domain). So all you could spoof is numbers and fully Arabic/Hebrew URLs.

It isn't clear what "leading edge" means in this case. Do you mean if the origin is RTL, go right, if it's LTR, go left? That won't work because the physical position of the origin depends upon the other characters in the string. If there are LTR characters in the path, the origin appears on the left. If not, it appears on the right. So I think my hack is the best we can do unless we fix the display of the URL itself.

I'm also curious how the offset is determined when you left-click a link and the Omnibox changes without user focus. That already works exactly right. It's like we have two separate pieces of code for this (one when the Omnibox changes itself, another when the focus blurs) and the former already does what we want. I'll try to dig it out and maybe we can just reuse it for blur.

### mg...@chromium.org (2016-10-18)

Note: This same issue was reported (by a different user) 1 day before this bug was filed, on a public bug:
https://bugs.chromium.org/p/chromium/issues/detail?id=351639#c164
Quoting and attaching screenshot.

"""
Interesting.
Enter the following URL in the address bar:


http://xn--ngbrx4e.xn--mgbaam7a8h/%D8%A3%D8%B3%D8%A6%D9%84%D8%A9-%D9%85%D8%AA%D9%83%D8%B1%D8%B1%D8%A9?%20%20%20%20%20%20%20https://developers.google.com/speed/pagespeed/insights/?url=http%3A%2F%2Fwww.finanser.es%3Fm%3D1&hl=es&priorityGroup=usability&utm_source=wmx&utm_campaign=wmx_mobilepsi&tab=mobile%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20#
"""

### pk...@chromium.org (2016-10-19)

[Empty comment from Monorail migration]

### pk...@chromium.org (2016-10-19)

I commented on https://crbug.com/chromium/351639.  The very short summary is, let's just fix this, and let's not do a user study, get more buy-in, wait on other vendors, etc.  The fix for "backspace goes back" has inspired me; we should do more of what I used to do in the early days of the omnibox, and Just Fix It when something is wrong.

I consider this bug to be an artifact of that one, so if we think this is a security P1, to me that makes the other at least a P2 if not a P1 itself.

### mg...@chromium.org (2016-10-19)

Cool, I replied on the other bug.

Regarding priority, though, I'm going to reduce this actually, given that:
1. it's been around ~forever, and
2. it only happens when you enter or edit the URL manually, not when you arrive somewhere by clicking on a link.

Given #2, I think the risk of spoofing is actually quite low, so I am removing RBS and lowering the pri. I'm still happy to fix it in the M56 timeframe though.

### mg...@chromium.org (2016-10-19)

It gets worse. I did find a way to have this bug trigger on navigation (rather than from explicitly editing the textfield): if your language is set to RTL.

1. Run LANGUAGE=he chrome (i.e., set your language to Hebrew).
2. Make a small website with an <a href="..."> (the above URL). Doesn't work from crbug because for some reason it doesn't recognise these as clickable URLs.
3. Click the link.

Unfortunately, the origin will be off-screen, due to the very thing that makes this *not* an issue in LTR languages.

The logic for navigation is:
1. Set display origin to 0. (For left-aligned text, this scrolls all the way left. For right-aligned text, this scrolls all the way right.)
2. Scroll so that the cursor position *before* the first character of the URL is visible.

There are four cases:

If it's an LTR language -- the text is left-aligned {
  Scroll all the way *left*
  If the origin is LTR (CASE 1) {
    Origin is on the left.
    Scroll until the *left* edge of the origin is visible.
    (This is a no-op because it will be visible by definition.) ✓
  } Else the origin is RTL (CASE 2) {
    Origin is potentially anywhere.
    Scroll until the *right* edge of the origin is visible.
    Now the origin is on screen. ✓
  }
} Else it's an RTL language -- the text is right-aligned {
  Scroll all the way *right*
  If the origin is LTR (CASE 3) {
    Origin is on the left.
    Scroll until the *left* edge of the origin is visible.
    Now the origin is on screen. ✓
  } Else the origin is RTL (CASE 4) {
    Origin is potentially anywhere.
    Scroll until the *right* edge of the origin is visible.
    If the origin was offscreen, it will still be offscreen. ✗
  }
}

So the case of an RTL origin in an RTL language setting is bad. The reason for the asymmetry is that URLs have an inherent base direction of LTR, which means an LTR origin will always appear on the left, whereas an RTL origin will *not* necessarily appear on the right.

The solution to this is to fix Step 1: instead of setting display origin to 0, we should always scroll all the way left. This affects Cases 3 and 4. Case 3 won't change the outcome because it will always scroll all the way left anyway. So it just fixes Case 4 to be the same as Case 2.

### mg...@chromium.org (2016-11-16)

At least some of these bugs also appear on Android (different implementation, slightly different results but same issue). We should also test Mac and iOS; I would not be surprised if they had similar issues.

### mg...@chromium.org (2016-11-16)

Reported in https://crbug.com/chromium/665358 using NBSP to make the right side of the Omnibox appear blank, with the string:

'http://xn--ggbla1c4e.xn--ngbc5azd/?'+Array(0x50).join("%C2%A0")+'127.0.0.1'

### ra...@chromium.org (2016-11-30)

[Empty comment from Monorail migration]

[Monorail components: -Security>UX]

### mg...@chromium.org (2016-12-06)

Note: I haven't forgotten about this bug. I have a fix on Views but I think we need to fix on all four platforms at the same time (or at least within the same milestone) so I am holding off on landing it.

Attaching screenshots on Android and iOS for the same bug. It will probably be a bug in Mac too but I haven't been able to test yet.

This is going to take me a little while to go through and do it on all the platforms since I don't do Mac or iOS development (and I will have to find someone on the iOS team because I have no local equipment or knowledge on that platform).

### mg...@chromium.org (2016-12-06)

Shortened URL for testing on other devices: https://goo.gl/gfEaLi

### lg...@chromium.org (2016-12-06)

[Empty comment from Monorail migration]

[Monorail components: UI>Security>UrlFormatting]

### mg...@chromium.org (2016-12-06)

Ah it seems to not be an issue on Mac because it will always show the domain with an ellipsis.

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-05-02)

I did end up forgetting about this. :(

+groby, +jdonelly, +tommycli from Omnibox: we have had this outstanding issue for awhile. Yet another RTL issue one where I have a fix on Views but we need to port out the change on Android and iOS as well. Can anybody help?

Note: In https://crbug.com/chromium/656417#c24 above, I claim to have a Views fix but there's no CL attached. Possibly it's on my hard drive. I'll check when I'm at my desk.

### mg...@chromium.org (2017-05-02)

Huh, I never uploaded this CL before. Well here it is now:
https://codereview.chromium.org/2855793003

Can we replicate this change in iOS and Android?

### jd...@chromium.org (2017-05-03)

We can try to take this on sometime in the next few weeks. Would that be sufficient?

### mg...@chromium.org (2017-05-04)

Yeah. In the mean time I'm going to try and land this Views change (but it turns out there were unresolved bugs which is why it didn't get mailed out last time).

### mg...@chromium.org (2017-05-12)

Just an update on this: I am still working on it.

It turns out this is super complex; I'm having to deep-dive into the RTL layout and elision algorithm in RenderTextHarfbuzz (to understand how it truncates the bidi string). My tests are all failing, but the Omnibox seems to behave properly. I'm trying to figure out whether it's just something wrong with the text or whether the fix should actually be in the elision algorithm.

### mg...@chromium.org (2017-05-12)

Yikes, I just discovered an even more extreme case:

http://xn--nebl.xn--9dbq2a/012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz

The Omnibox (on Views) is COMPLETELY BLANK when not editing the text field. My above CL does fix this behaviour, but I'm struggling to understand why.

(My fix performs scroll operations, it's kind of a hack. Now I've learned that the textfield performs elision when the text is not editable, so I don't know why scrolling has any effect.)

### mg...@chromium.org (2017-05-12)

OK this is a Monday job. But I think I fully understand it now.

The URL is being 1. elided to fit in the text box, then 2. scrolled horizontally.

The eliding is perfectly good for RTL text. For example, if you write (ASCII-hack-RTL) "ABC.COM/0123abcd", it will elide to "ABC.COM/012…" which renders as "…012/MOC.CBA". That's good.

There is no need to scroll horizontally (due to the eliding): it should *always* be at offset 0. Otherwise you just end up with whitespace on either side, which in the worst case scrolls the origin entirely off-screen and leaves the text field blank.

The current implementation is designed for all-LTR-URLs; it removes any horizontal offset (post-elision) by calling:
SelectRange(gfx::Range(0));
that is equivalent to reset-horizontal-scroll-to-0 for all-LTR text, but doesn't do that at all in bidi land. I think we just need to replace SelectRange(gfx::Range(0)) with a scroll all the way left.

But there are lots of cases to consider:
- RTL UI mode.
- The THREE different ways you can get into non-editing Omnibox mode (navigation from clicking a link, pasting the URL into the Omnibox and hitting Enter, and blurring the text field). All three of these give different results so I suspect they have different code paths.

Have to figure out unit testing.

And then, of course, have to debug and solve the same problem on Mac, Android and iOS. Yay.

### to...@chromium.org (2017-05-16)

[Empty comment from Monorail migration]

### to...@chromium.org (2017-05-16)

Hey Matt, since you sent that shoutout, I'm going to investigate the Android fix. I'll add Android specific discussion there to keep this bug more clear.

### to...@chromium.org (2017-05-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c603f3c7e6a01188ba81015e5354e4797a017f45

commit c603f3c7e6a01188ba81015e5354e4797a017f45
Author: mgiuca <mgiuca@chromium.org>
Date: Tue May 23 07:37:02 2017

Fix RTL URL rendering in Omnibox (domain off screen on long URL).

BUG=656417

Review-Url: https://codereview.chromium.org/2855793003
Cr-Commit-Position: refs/heads/master@{#473830}

[modify] https://crrev.com/c603f3c7e6a01188ba81015e5354e4797a017f45/chrome/browser/ui/omnibox/omnibox_view_browsertest.cc
[modify] https://crrev.com/c603f3c7e6a01188ba81015e5354e4797a017f45/chrome/browser/ui/views/omnibox/omnibox_view_views.cc
[modify] https://crrev.com/c603f3c7e6a01188ba81015e5354e4797a017f45/chrome/browser/ui/views/omnibox/omnibox_view_views.h
[modify] https://crrev.com/c603f3c7e6a01188ba81015e5354e4797a017f45/chrome/browser/ui/views/omnibox/omnibox_view_views_browsertest.cc
[modify] https://crrev.com/c603f3c7e6a01188ba81015e5354e4797a017f45/chrome/browser/ui/views/omnibox/omnibox_view_views_unittest.cc


### mg...@chromium.org (2017-05-23)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-05-23)

OK this should be completely fixed on Views now. Android fix has landed today as well (thanks Tommy!). I just filed https://crbug.com/chromium/725400 for iOS (the last remaining platform) so we can close this one out.

### sh...@chromium.org (2017-05-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-25)

[Empty comment from Monorail migration]

### ch...@gmail.com (2017-05-25)

Happy for that!

- Can you please make this reward to me? also, Please don't forget to credit me as "Khalil Zhani" :-) - Thanks Andrew, as always!

### aw...@chromium.org (2017-05-25)

Thanks Khalil. jackwillzac@gmail.com - could you confirm here or to me in email that's you agree with #46?

### ja...@gmail.com (2017-05-25)

Yeah sure!

### aw...@chromium.org (2017-05-26)

[Empty comment from Monorail migration]

### mg...@chromium.org (2017-08-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-09-05)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/656417?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Omnibox, UI>Security>UrlFormatting]
[Monorail blocked-on: crbug.com/chromium/351639, crbug.com/chromium/723100]
[Monorail blocking: crbug.com/chromium/725400, crbug.com/chromium/757150]
[Monorail mergedwith: crbug.com/chromium/665358]
[Monorail components added to Component Tags custom field.]

### ti...@gmail.com (2024-09-16)

deleted

### ti...@gmail.com (2024-09-16)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085709)*
