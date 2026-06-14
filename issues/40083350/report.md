# Security: URL Spoofing with HTTPS lock

| Field | Value |
|-------|-------|
| **Issue ID** | [40083350](https://issues.chromium.org/issues/40083350) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox |
| **Reporter** | he...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2015-12-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability makes it possible to display arbitrary content under any URL and with the HTTPS lock spoofed.

**VERSION**  

Chrome Version: I tested on 48.0.2564.22 and 49.0.2584.0 (canary).

**REPRODUCTION CASE**

1. Access <http://lbherrera.me/spoofpopup.html>
2. Click on the link.
3. A popup should appear asking for your credentials under the <https://accounts.google.com> URL.

\* I suspect this happens because setting the opener to null causes the omnibox to be focused, and then if you redirect the website while it is focused, the URL (if it is large) won't be displayed from the start (as it is when the omnibox isn't focused).

## Attachments

- [spoof.png](attachments/spoof.png) (image/png, 89.8 KB)
- [no-spoof.png](attachments/no-spoof.png) (image/png, 51.9 KB)
- [crbug567445.png](attachments/crbug567445.png) (image/png, 80.2 KB)

## Timeline

### me...@chromium.org (2015-12-08)

Looks like omnibox eliding/alignment in popup windows isn't correct.

palmer: As lord of the origins, can you assign a severity label? (I'm torn between low and medium)

### me...@chromium.org (2015-12-08)

[Empty comment from Monorail migration]

### pa...@chromium.org (2015-12-08)

It doesn't seem to work for me.

### me...@chromium.org (2015-12-08)

I get this on M47 on Goobuntu (popup width is a bit off, but good enough).

### he...@gmail.com (2015-12-08)

I tested on Windows 7, on 3 different computers. Perhaps it only works on Windows.

### me...@chromium.org (2015-12-08)

Ah, interesting. I had JS disabled on the popup page in the above screenshot. If I enable JS on that origin, it doesn't repro for me either. 

### me...@chromium.org (2015-12-08)

luan.herrera@hotmail.com: Can you try removing the alert box from the popup window? That seems to reposition the omnibox text.

### he...@gmail.com (2015-12-08)

Done, meacer. The one without the alert won't have the https lock because it's hosted on my server and not on my friend's sever (who has https).

On windows, after the spoof, if you click somewhere the URL will be alignment to the start. That's why I use the alert.

### he...@gmail.com (2015-12-08)

[Comment Deleted]

### he...@gmail.com (2015-12-08)

aligned*

And on windows, the prompt doesn't remove the focus from the omnibox, thus keeping the URL spoofed. Don't know about others OS.

### me...@chromium.org (2015-12-08)

palmer: Can you repro with the new POC at the same link?

### pa...@chromium.org (2015-12-08)

Yes, I now see what you see in #4.

### cl...@chromium.org (2015-12-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-12-10)

palmer@ - As someone who clearly cares (enough to mark the bug medium severity) I leave it to you to find an owner. Also, I genuinely don't have a clue who should own it, and that context seems much more up enamel's alley.

### pa...@chromium.org (2015-12-10)

[Empty comment from Monorail migration]

### fe...@chromium.org (2015-12-11)

egm@, you've been working with the omnibox team right? Is there anyone who would be a good owner for this?

### eg...@chromium.org (2015-12-12)

+groby, is there anyone on your team who might be able to pick this up? 

### gr...@chromium.org (2015-12-14)

FWIW, does not repro on OSX 49.0.2586.0

Might be because the Password Alert extension interferes :)

To answer egm@: I don't really have anybody with spare time on their hands right now. Since it seems to be Windows only, maybe pkasting@?

### pk...@chromium.org (2015-12-14)

For clarity, the issue here seems to be that focus is getting placed in the omnibox to begin with, and specifically that the cursor position in that case is at the end of the text (instead of e.g. the whole URL being selected).

Once those things are true, the rest of the behavior here naturally falls out, since the omnibox on views at least needs to keep the text scrolled such that the cursor is visible.

I don't know why the omnibox is getting focus here.  According to https://crbug.com/chromium/567445#c0, this is due to setting the opener to null.  I don't see a reason why that should focus the omnibox, though.  The next step here would be to step through to understand the call chain that does that.

There probably isn't any really great person to own this.  Plausible candidates include me, creis, msw, sky, and ben, but pretty much all of us are busy.

### cl...@chromium.org (2016-01-05)

palmer@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-26)

palmer@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### pa...@chromium.org (2016-02-09)

As surprising as it is, I have confirmed that not setting window.opener to null causes the omnibox to not be focused and the cursor not to go to the end. When window.opener is null, BrowserView::SetFocusToLocationBar is called, which then:

1103   LocationBarView* location_bar = GetLocationBarView();                                                                      
1104 base::debug::StackTrace().OutputToStream(&std::cerr);                                                                        
1105   if (location_bar->omnibox_view()->IsFocusable()) {                                                                         
1106     // Location bar got focus.                                                                                               
1107     location_bar->FocusLocation(select_all);                                                                                 
1108   } else {

Line 1107 is the thing that does it.

### pa...@chromium.org (2016-02-09)

It looks like when window.opener is null, web_contents_->FocusLocationBarByDefault() returns true, which causes a call to web_contents_->GetDelegate()->SetFocusToLocationBar(false);. (The false means "do not select all text".)

CL on the way.

### pa...@chromium.org (2016-02-09)

https://codereview.chromium.org/1678233003/ for anyone interested.

### cr...@chromium.org (2016-02-10)

Hmm, let's try to understand a little more of the connection.  Note that setting window.opener to null and navigating the popup to a cross-site URL is a way to force a cross-process navigation.  That may explain part of the behavior here.

### cr...@chromium.org (2016-02-10)

Ok, I found a few interesting things after looking closer.

1) This general "focus the omnibox for about:blank" behavior was added in https://codereview.chromium.org/141028 for https://crbug.com/chromium/9966, and was meant for cases where the user starts Chrome at about:blank.  Amusingly, this case is fairly broken today, since it gives the omnibox focus but puts the cursor before "about:blank" and doesn't select the text.  Thus, any typing will keep "about:blank" as a suffix.  This suggests that we should either remove that logic entirely (killing this spoof) or select the text as well as focus it.

2) This attack is possible because the "w=window.open(); w.opener=null; w.location.href=url" case triggers an OpenURL call so that cross-process navigations are possible.  OpenURL goes through OpenURLFromTab and UpdateUIForNavigationInTab, which calls FocusLocationBarByDefault.

3) The about:blank logic is using the visible entry (after https://codereview.chromium.org/25654005), which seems right at first glance but is actually wrong.  When we get here for OpenURL, the visible entry is about:blank (which is the last committed entry), but the pending entry is the attacker's renderer-initiated URL.

Given all this, if we decide to keep the "focus the omnibox for about:blank" behavior, I'd recommend limiting it to the initial navigation, checking the pending entry rather than the visible one, and verifying that it isn't renderer-initiated.


### cr...@chromium.org (2016-02-10)

I also found https://crbug.com/chromium/567445#c10 intriguing, which is that we somehow keep the focus in the omnibox on Windows when a dialog appears.  This doesn't happen on Linux (as mentioned in https://crbug.com/chromium/567445#c7 and as I verified), which is a nice second line of defense here.  In general, any time the cursor is in the omnibox and a dialog appears, the start of the URL (origin) should become visible.

@pkasting: Does that sound like something we should fix on Windows?

### pk...@chromium.org (2016-02-10)

Huh, at first hearing the Linux behavior actually sounds kinda wrong to me.  Is there a simple way I can test this out locally to see what it feels like?

As for your notes in https://crbug.com/chromium/567445#c26, I'd prefer to keep the fix for starting with about:blank, but make it select all the text (which is what happens when e.g. the user hits ctrl-L or the like -- it would be worth seeing why the codepaths are different enough to result in this behavior difference) and restricting it to the initial navigation.

### cr...@chromium.org (2016-02-10)

https://crbug.com/chromium/567445#c28: I used http://lbherrera.me/spoofpopup.html to see the dialog vs omnibox behavior.  (Disable Safe Browsing in settings and use the second link.)  On Linux, the omnibox loses focus and shows the origin when the prompt dialog appears and takes focus.

### pk...@chromium.org (2016-02-18)

OK, you're right that the Windows behavior is weird.  We should be like Linux there.

We should also do everything in your final paragraph of https://crbug.com/chromium/567445#c26, as well as selecting all the text in the case where we do do this.

### bu...@chromium.org (2016-03-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c70cb1fe9303df33b11187d0f5f60d22938e6e63

commit c70cb1fe9303df33b11187d0f5f60d22938e6e63
Author: palmer <palmer@chromium.org>
Date: Fri Mar 04 23:41:26 2016

Don't focus the location bar in a phishy situation.

There is logic to focus the location bar for editing if the URL is about:blank.
However, if the page transition type is PAGE_TRANSITION_LINK, bypass that logic;
it's not really a blank page. This avoids a phishy edge case with window.open.

BUG=567445

Review URL: https://codereview.chromium.org/1678233003

Cr-Commit-Position: refs/heads/master@{#379396}

[modify] https://crrev.com/c70cb1fe9303df33b11187d0f5f60d22938e6e63/chrome/browser/ui/browser_focus_uitest.cc
[modify] https://crrev.com/c70cb1fe9303df33b11187d0f5f60d22938e6e63/content/browser/web_contents/web_contents_impl.cc


### pa...@chromium.org (2016-03-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-03-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-24)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### go...@chromium.org (2016-03-24)

Please merge your change to M50 branch (2661) by EOD tomorrow, Friday (03/25), so we can take it for next week beta cut. Thank you.

### cr...@chromium.org (2016-03-24)

I think palmer@ is OOO.  I'll try to merge it for him.

### bu...@chromium.org (2016-03-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/67e95d7f6741266391e521e4ced6608ff8af9999

commit 67e95d7f6741266391e521e4ced6608ff8af9999
Author: creis <creis@chromium.org>
Date: Thu Mar 24 23:18:20 2016

Don't focus the location bar in a phishy situation.

There is logic to focus the location bar for editing if the URL is about:blank.
However, if the page transition type is PAGE_TRANSITION_LINK, bypass that logic;
it's not really a blank page. This avoids a phishy edge case with window.open.

TBR=palmer
BUG=567445
NOTRY=true
NOPRESUBMIT=true

Review URL: https://codereview.chromium.org/1678233003

Cr-Commit-Position: refs/heads/master@{#379396}
(cherry picked from commit c70cb1fe9303df33b11187d0f5f60d22938e6e63)

Review URL: https://codereview.chromium.org/1832913003

Cr-Commit-Position: refs/branch-heads/2661@{#386}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/67e95d7f6741266391e521e4ced6608ff8af9999/chrome/browser/ui/browser_focus_uitest.cc
[modify] https://crrev.com/67e95d7f6741266391e521e4ced6608ff8af9999/content/browser/web_contents/web_contents_impl.cc


### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

Thanks for the report. How would you like to be credited when we mention this in Chrome's release notes?

### he...@gmail.com (2016-04-12)

You can credit me as "Luan Herrera", thanks.

### mb...@chromium.org (2016-04-13)

Thanks again for the report! This one qualified for a $1000 reward.

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/567445?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083350)*
