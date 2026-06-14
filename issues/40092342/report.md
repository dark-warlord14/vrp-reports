# Canceling a browser-initiated navigation by using the history.back function

| Field | Value |
|-------|-------|
| **Issue ID** | [40092342](https://issues.chromium.org/issues/40092342) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2018-09-03 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

By calling history.back after the onbeforeunload event it's possible to cancel a browser-initiated navigation and trick the user into thinking the navigation happened and that they are in the page they intended to access.

While it's not possible to know which website the user was trying to access, the attacker can use a fake Google Search page hoping the user was trying to search for something using the omnibox or maybe mislead the user into thinking that somehow the URL that they typed was interpreted as a search.

**VERSION**  

Chrome 68.0.3440.106 (Official Build) stable (64-bit)  

Chrome 70.0.3538.5 (Official Build) canary (64-bit)

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/history/index.html>
2. Try to search for anything using the omnibox.

## Timeline

### ts...@chromium.org (2018-09-04)

See https://chromium.googlesource.com/chromium/src/+/master/docs/security/faq.md

> Furthermore, Chrome can only guarantee that it is correctly representing
> URLs and their origins at the end of all navigation. Quirks of URL parsing,
> HTTP redirection, and so on are not security concerns unless Chrome is
> misrepresenting a URL or origin after navigation has completed.

### he...@gmail.com (2018-09-04)

tsepez@: Please take a look again, this bug is about an attacker being able to cancel a browser-initiated navigation, which surely shouldn't be possible.

### ts...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### mp...@google.com (2018-09-04)

This seems like an issue to me. As per the FAQ, users don't (or shouldn't) expect links on web pages to take them to trusted locations. But, users certainly trust the Omnibox to take them to trusted locations.

Seems to be an issue with a long history: https://bugs.chromium.org/p/chromium/issues/detail?id=756803.

And https://bugs.chromium.org/p/chromium/issues/detail?id=660716 and perhaps https://bugs.chromium.org/p/chromium/issues/detail?id=634108.

CC'ing @dcheng because he seems to be involved in all these issues.

### he...@gmail.com (2018-09-04)

Guess this is a rediscovery of an issue I had reported in 2015: https://bugs.chromium.org/p/chromium/issues/detail?id=537629#c4.
I had forgotten about it.

### mp...@google.com (2018-09-05)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### na...@chromium.org (2018-09-05)

Adding a some other folks that know navigation code.

### he...@gmail.com (2018-09-05)

By the way, after reading the severity guidelines, wouldn't this fall under the medium severity (A bug that allows web content to tamper with trusted browser UI)?

### ar...@chromium.org (2018-09-05)

The history navigation deletes the omnibox navigation with this stack trace:
---------------------------------------------------------------------------------------
#3 0x7f4fdd2d77f9 content::NavigationRequest::~NavigationRequest()
#4 0x7f4fdd27b352 content::FrameTreeNode::ResetNavigationRequest()
#5 0x7f4fdd27ad32 content::FrameTreeNode::CreatedNavigationRequest()
#6 0x7f4fdd2ec754 content::NavigatorImpl::Navigate()
#7 0x7f4fdd292294 content::NavigationControllerImpl::NavigateToExistingPendingEntry()
#8 0x7f4fdd294049 content::NavigationControllerImpl::GoToIndex()
#9 0x7f4fdd29417b content::NavigationControllerImpl::GoToOffset()
#10 0x7f4fddc64af5 content::WebContentsImpl::OnGoToEntryAtOffset()
??? IPC = ViewHostMsg_GoToEntryAtOffset
---------------------------------------------------------------------------------------

Renderer initiated navigation are ignored if there is an ongoing browser initiated navigation in:
NavigatorImpl::OnBeginNavigation(), but it is never touched.

Renderer initiated backforward navigation is using a different IPC. The 'normal' path is the one with BeginNavigation.

I guess we need to merge the two path or make a similar check on the second path.

### cr...@chromium.org (2018-09-05)

https://crbug.com/chromium/879965#c8: Thanks for the report.  That said, the trusted browser UI (the omnibox) is accurately showing the user where they ended up in this case, so it's not being tampered with.  It's more of an unexpected navigation at an unfortunate time, which I agree is low severity but worth fixing.

https://crbug.com/chromium/879965#c9: Thanks for spotting that!  Would you be up for adding the relevant check?

### he...@gmail.com (2018-09-05)

#10, Well, it's true that the browser UI is accurately showing where the user ended at, but from my understanding, the ability of the user to use the omnibox to go where they want has been tampered. How's the user supposed to know that it wasn't "google.com" that redirected them to, for example, "apps-google.com" and instead, was the attacker?

### cr...@chromium.org (2018-09-05)

https://crbug.com/chromium/879965#c11: Yes, but that's different from what you mentioned in https://crbug.com/chromium/879965#c8-- we're talking about how the user knows they ended up in the wrong place, and Chrome is providing that information in the omnibox.  It's closer to bugs that deny the user from navigating away from the page, and it's also partly mitigated by the fact that the page they end up on isn't related to what they typed-- the attacker can't predict where the user is going.

I certainly agree this is a bug and we should fix it.  I just don't see it as medium severity, given the mitigating factors (omnibox is correct, page isn't related to what user typed).

### cl...@chromium.org (2018-09-06)

This is not a URL spoof. I think we could end up with a case where the page prevents the user from navigating away by constantly requesting a back/forward that result in a 204.

As Arthur points out, we have a check against this kind of bad behavior in OnBeginNavigation which is not used for history navigations. For history navigations, I think we use the OpenURL path instead? If that's the case, it might be a bit hard to add the same kind of checks: we can't prevent a OpenURL from going through if there's a navigation ongoing in the frame until we know for sure that the frame will be used to navigate to the opened URL. I guess we could rely on the WindowDisposition param to provide this for us, but I think the content embedder is still allowed to decide it wants to open the URL somewhere else than described in the window disposition passed to it. So I don't think we can put it at the OpenURL level.

The alternative then is to put it in NavigationController. However, right now the only cases where NavigationController won't start the navigation it's being asked to start is when it can't (eg you're asking for a back navigation when there's no previous NavigationEntry). Adding a new cases where navigation don't start might have unexpected side effects.

Also adding the usual warning about modifying the conditions when navigations are allowed to start or not: it's quite possible that we will find that some websites actually rely on this behavior to work. It's often been the case in the past.

### ar...@chromium.org (2018-09-06)

#13: In this case, this is not about FrameHostMsg_OpenURL, but ViewHostMsg_GoToEntryAtOffset

Maybe there is a similar issue with openURL.

### ar...@chromium.org (2018-09-06)

Okay, I started working on it:
https://chromium-review.googlesource.com/c/chromium/src/+/1209744

For the moment, I added one test and I still need to work a bit on the fix.

Note: Funnily, it has the side effect to also fix: https://bugs.chromium.org/p/chromium/issues/detail?id=869710
It fixes the bug, but for wrong reasons. The path ViewHostMsg_GoToEntryAtOffset classified the navigation as 'browser-initiated', which is wrong. But it means the second history.back() is now canceled, because the first history.back() is in progress.

### na...@chromium.org (2018-09-06)

Shouldn't the second history.back() cancel the first one? This is how usually things work when we allow navigations to be cancelled.

### ar...@chromium.org (2018-09-07)

Nasko: In https://bugs.chromium.org/p/chromium/issues/detail?id=869710,
I guess what happens is the second navigation cancels the first one.
The first navigation with history.back() never happens, but it created a pending_entry in the NavigationController. pending_entry_index_ = (current - 1).

Then when the second navigation is created, GetCurrentEntryIndex() returns (current - 1) instead of current. So history.back() navigate to (current-2).
-----------
int NavigationControllerImpl::GetCurrentEntryIndex() const {
  if (transient_entry_index_ != -1)
    return transient_entry_index_;
  if (pending_entry_index_ != -1)
    return pending_entry_index_;          <----- Why are we doing this?
  return last_committed_entry_index_;
}
-----------



### cr...@chromium.org (2018-09-13)

#17: Just to post the reply here as well, you're correct in https://bugs.chromium.org/p/chromium/issues/detail?id=869710#c12 that it's because of the back/forward buttons.  We want the user to be able to click those buttons repeatedly (or use keyboard shortcuts) to go multiple entries back and forward without having to wait for each one to commit.  We should preserve that when fixing the history API behavior (as discussed in https://chromium-review.googlesource.com/c/chromium/src/+/1209744).

(Sorry for missing that there's an update on that CL-- I'll take a look.)

### bu...@chromium.org (2018-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a7d715ae5b654d1f98669fd979a00282a7229044

commit a7d715ae5b654d1f98669fd979a00282a7229044
Author: Arthur Sonzogni <arthursonzogni@chromium.org>
Date: Thu Sep 20 16:11:13 2018

Prevent renderer initiated back navigation to cancel a browser one.

Renderer initiated back/forward navigations must not be able to cancel ongoing
browser initiated navigation if they are not user initiated.

Note: 'normal' renderer initiated navigation uses the
FrameHost::BeginNavigation() path. A code similar to this patch is done
in NavigatorImpl::OnBeginNavigation().

Test:
-----

Added: NavigationBrowserTest.
 * HistoryBackInBeforeUnload
 * HistoryBackInBeforeUnloadAfterSetTimeout
 * HistoryBackCancelPendingNavigationNoUserGesture
 * HistoryBackCancelPendingNavigationUserGesture

Fixed:
 * (WPT) .../the-history-interface/traverse_the_history_2.html
 * (WPT) .../the-history-interface/traverse_the_history_3.html
 * (WPT) .../the-history-interface/traverse_the_history_4.html
 * (WPT) .../the-history-interface/traverse_the_history_5.html

Bug: 879965
Change-Id: I1a9bfaaea1ffc219e6c32f6e676b660e746c578c
Reviewed-on: https://chromium-review.googlesource.com/1209744
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Reviewed-by: Camille Lamy <clamy@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#592823}
[modify] https://crrev.com/a7d715ae5b654d1f98669fd979a00282a7229044/content/browser/frame_host/navigation_controller_impl_unittest.cc
[modify] https://crrev.com/a7d715ae5b654d1f98669fd979a00282a7229044/content/browser/navigation_browsertest.cc
[modify] https://crrev.com/a7d715ae5b654d1f98669fd979a00282a7229044/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/a7d715ae5b654d1f98669fd979a00282a7229044/content/browser/web_contents/web_contents_impl.h
[modify] https://crrev.com/a7d715ae5b654d1f98669fd979a00282a7229044/content/common/view_messages.h
[modify] https://crrev.com/a7d715ae5b654d1f98669fd979a00282a7229044/content/renderer/render_view_impl.cc
[modify] https://crrev.com/a7d715ae5b654d1f98669fd979a00282a7229044/content/renderer/render_view_impl.h
[delete] https://crrev.com/96a4668d39b28f933b44801b594aa91cdd32f87b/third_party/WebKit/LayoutTests/external/wpt/html/browsers/history/the-history-interface/traverse_the_history_2-expected.txt
[delete] https://crrev.com/96a4668d39b28f933b44801b594aa91cdd32f87b/third_party/WebKit/LayoutTests/external/wpt/html/browsers/history/the-history-interface/traverse_the_history_3-expected.txt
[delete] https://crrev.com/96a4668d39b28f933b44801b594aa91cdd32f87b/third_party/WebKit/LayoutTests/external/wpt/html/browsers/history/the-history-interface/traverse_the_history_4-expected.txt
[delete] https://crrev.com/96a4668d39b28f933b44801b594aa91cdd32f87b/third_party/WebKit/LayoutTests/external/wpt/html/browsers/history/the-history-interface/traverse_the_history_5-expected.txt
[modify] https://crrev.com/a7d715ae5b654d1f98669fd979a00282a7229044/third_party/blink/public/web/web_view_client.h
[modify] https://crrev.com/a7d715ae5b654d1f98669fd979a00282a7229044/third_party/blink/renderer/core/exported/local_frame_client_impl.cc


### ar...@chromium.org (2018-09-20)

This is now fixed.
This will be part of M71. Do you think it needs to be cherry-picked into M70?

M70 is in beta and Stable cut is in 19 days (Oct 9)
There is a small risk of seeing some websites actually relying on the behavior I removed. On the other side, it will likely prevent bad ones from keeping user blocked, which will be nice.

Let's wait a 5-6 days on canary and then try to cherry-pick this CL into beta?

### ar...@chromium.org (2018-09-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-21)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-09-21)

https://crbug.com/chromium/879965#c20: Thanks!  Sounds like this may benefit from having the full bake time just to make sure there's no regression, so I'd lean towards not merging it and letting the fix go out in M71.  CC'ing awhalley@ in case he'd prefer to request the merge, though.

### aw...@chromium.org (2018-09-21)

Thanks for checking - I'm OK with this going in 71.

### ar...@chromium.org (2018-09-24)

It looks good to me.

### aw...@chromium.org (2018-09-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-09-28)

Thanks for the report luan.herrera@! The VRP panel decided to award $500.

### aw...@chromium.org (2018-09-28)

[Empty comment from Monorail migration]

### aw...@google.com (2018-12-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### Ju...@microsoft.com (2020-04-01)

Just FYI, that check added in the patch trusts `has_user_gesture` passed from a renderer.

### lu...@chromium.org (2020-04-01)

+mustaq@ for any comments on how to improve user gesture checks in the browser process (see https://crbug.com/chromium/879965#c35 above)

### mu...@chromium.org (2020-04-01)

https://crbug.com/chromium/848778 tracks our work on browser-verified user activation.

Ideally |has_user_gesture| bit from renderer shouldn't be needed because browser already has the info in FrameTreeNode.  However, navigation code sometimes check the state after navigation is done, so FTN can't be relied on in all cases.

### is...@google.com (2020-04-01)

This issue was migrated from crbug.com/chromium/879965?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092342)*
