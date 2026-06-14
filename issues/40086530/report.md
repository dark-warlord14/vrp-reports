# Security: URL Spoofing (with HTTPS lock) by focusing the omnibox while changing the location hash and calling a modal dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40086530](https://issues.chromium.org/issues/40086530) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation, UI>Browser>Omnibox, UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | kr...@chromium.org |
| **Created** | 2017-01-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

By changing the location hash and calling a modal dialog at the same time a user focuses on the omnibox it's possible to spoof the URL and the HTTPS lock.  

After the spoof, if the user tries to interact with the webpage the URL will return to normal, but this can be circumvented by putting the user in fullscreen after his first click.

**VERSION**  

I tested on:  

55.0.2883.87 [Stable].  

56.0.2924.59 [Beta].

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/spoof/spoof.html>
2. Click on the omnibox.
3. An alert should appear saying you are being redirected to <https://www.google.com>
4. A fake page should load under Google's URL.

\* Given that I used several spaces to align the spoofed URL to my display resolution (1280x984), the spoofed URL might be misaligned in your screen, however a dedicated attacker could fix this as he would have access to the users' screen resolution.

Here is a video simulating the attack:  

<https://www.youtube.com/watch?v=kCdDD5i3clM>

## Attachments

- [Screen Shot 2017-01-17 at 16.07.16.png](attachments/Screen Shot 2017-01-17 at 16.07.16.png) (image/png, 55.5 KB)
- [spoof.html](attachments/spoof.html) (text/plain, 1.2 KB)

## Timeline

### do...@chromium.org (2017-01-17)

On Mac, I get the attached screenshot - not ideal, but not quite as bad. I'm guessing that the Views (Win/Linux/ChromeOS) omnibox has the more serious overlapping issue that we see in your PoC.

creis: can you take a look at this? Also cc mgiuca and emilyschechter FYI.

[Monorail components: UI>Browser>Omnibox>SecurityIndicators]

### pk...@chromium.org (2017-01-17)

I get something like the screenshot in https://crbug.com/chromium/681740#c1 on Win dev.

### he...@gmail.com (2017-01-17)

#2, I just tested on canary and if you only click on the omnibox it doesn't seem to work. But if you try to select the current URL (by clicking and dragging the mouse) it works. I assume it must be working the same way in dev.

### sh...@chromium.org (2017-01-17)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-01-17)

Looks like another focus-the-omnibox bug, similar to https://crbug.com/chromium/677716.  I'm not able to repro on Windows Beta (56.0.2924.59), where the focus ends up at the start of the omnibox, showing the origin.  It looks like it does repro on M55 stable, though.

(The original report says it works on 56.0.2924.59, so maybe I'm missing something?)

I'll try to bisect it when I get a chance.

### cr...@chromium.org (2017-01-18)

The bisect for this is proving very difficult, because the behavior seems nondeterministic in some way.  I've seen successful and unsuccessful runs on the same version (on both M57 and M55), even when just limiting to the click approach rather than the drag approach mentioned in https://crbug.com/chromium/681740#c3.  So far, I've seen it often on Windows and never on Linux.

Maybe there's a race involved?  Or some aspect of focus tracking I don't understand?  I'm trying to do the exact same thing across multiple runs (e.g., how and where I click, how I dismiss the alert, etc), and I'm seeing different results across the runs on the same version.

My guess is that this is some issue with how focus is tracked in the omnibox.  When the alert is dismissed and we get the subsequent DidCommit for the fragment URL, focus is sometimes given back to the omnibox, and when that happens, sometimes it's at the start of the omnibox (no spoof) and sometimes it's at the end (working spoof).

nick@ noticed that OmniboxViewViews::OnFocus has a saved_selection_for_focus_change_, which may possibly be related?

pkasting@, do you know that code at all and what might be happening here?  I'll assign this to you for the moment since I don't know how that code works or how the fragment navigation plays into it, but feel free to assign it back if it ends up looking like a navigation issue.

[Monorail components: UI>Browser>Navigation UI>Browser>Omnibox]

### cr...@chromium.org (2017-01-18)

For the record, here's the spoof.html file, in case the link stops working later.

### pk...@chromium.org (2017-01-23)

saved_selection_for_focus_change_ is about restoring the selected text in the address bar when the address bar is refocused.  For example, select some text in the omnibox, then hit tab; this blurs the omnibox and deselects the text (we'd get a grey selection in the omnibox if we failed to deselect).  Now hit shift-tab; the selection should be restored.  I would assume all that functionality is unrelated to this issue.

I haven't reproduced this myself, but if you sometimes can, then it would be useful to start setting breakpoints (which just print the current function and continue) on any functions involved, so you can see whether there's a different sequence of calls in the cases which reproduce and the ones that don't.  I'd suggest specific things to set breakpoints on, but other than OmniboxViewViews::OnFocus()/OnBlur(), I'm not sure what's involved here.

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-01-27)

Sorry, I didn't have a chance to look at this this week, and I'll be at BlinkOn next week followed by vacation.  This is also pretty unfamiliar territory for me, so any assistance from people who know the omnibox is welcome.  Otherwise, I'll take a look when I get back.

Side note: the unreliability of the exploit for me would be a mitigating factor possibly making this medium severity, but I don't want to downgrade it until we know more about why it's unreliable.

### sh...@chromium.org (2017-02-11)

creis: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@chromium.org (2017-02-12)

Adding a a few more enamelites.

### sh...@chromium.org (2017-02-25)

creis: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-03-13)

Ok, I've finally had a chance to look at this in a debugger.  I think I see where the problem is, but I don't yet know the right way to fix it.

(Quick note: I had to append a period after all the spaces in the attack to make it work.  Maybe a recent change trimmed trailing whitespace?  The period isn't that noticeable to the user, but it is another mitigating factor beyond the fact that a drag is required.)

There are two somewhat independent things going on: (1) the fragment navigation commit changes the URL while focus is in the omnibox and scrolls it to the end, and (2) the alert dialog distracts the user and ends any ongoing drag.  We can think about possible fixes for both of these.

Note that we can get a very similar attack (perhaps not quite as robust) by leaving out the alert dialog entirely: just run the following line in DevTools and then put focus in the omnibox and wait for the URL to change after 5 seconds:
setTimeout(function() { location.href="#  http://www.google.com                                                                                                                                                                                                                                                         ."; }, 5000);

As noted in https://crbug.com/chromium/681740#c3, *clicking* in the omnibox doesn't cause a spoof.  If you click and release, all of the text is selected.  When the navigation commits, we end up clearing the selection in OmniboxViewViews::Update (via RevertAll; see below), but we call SelectAll again because was_select_all is true.  That keeps the origin visible.

In contrast, starting a drag does lead to the spoof.  When the navigation commits, the selected range is empty (i.e., a caret at the starting point) instead of having the whole text selected.  You'll see the same thing if you put a caret into the URL while waiting for the timer to fire in my simplified repro, or if you just select part of the URL.

After the navigation commits, we get to OmniboxViewViews::RevertAll, via Update.  (This happens to be via SSLManager and VisibleSecurityStateChanged, but it can happen other ways as well, like via Browser::ActiveTabChanged when switching back to the tab.)  RevertAll calls OmniboxEditModel::Revert, which has this line:
  view_->SetWindowTextAndCaretPos(permanent_text_,
                                  has_focus() ? permanent_text_.length() : 0,
                                  false, true);

Since the omnibox has focus, we're setting the caret position to the end of the text.  I think this is surprising, since the text has just changed to something the page controls.  We scroll to show the end of the new URL and scroll the origin out of view, despite the fact that the user was interacting with a different part of the old URL before the navigation committed.  Seems likely to cause a disruption in any case, not just this spoof.

In the "click on the omnibox" case, we get another call to SelectAll (from Update) afterward, so it doesn't matter that the caret was put at the end.  (SelectAll shows the start of the URL, not the end.)  In the "drag on the omnibox" case, however, there's no SelectAll afterward, so we put the caret at the end and scroll the origin out of view.

As a strawman fix, I tried putting a SelectAll() call in RevertAll().  That prevents the spoof but breaks a bunch of tests (and almost certainly isn't the right thing to do in general):
https://codereview.chromium.org/2747583004
Maybe there's another way to decide that we should call SelectAll in these cases?

We could also look at the dialog half of the problem, where focus is returned to the omnibox after dismissing a dialog, if it had focus when the dialog opened.  On one hand, this is sensible from a focus perspective.  On the other hand, it does mean that the attacker can interrupt the drag and distract the user from what they were doing in the omnibox with something from the page.  Maybe we could consider giving focus to the page after the page puts up a dialog and the user closes it?  (That would be in addition to whatever SelectAll change we consider above, since the dialog isn't necessary for the spoof.)

Anyway, given the fact that this requires both a drag in the omnibox and a trailing non-whitespace character, I'm ok with lowering this to medium severity.

pkasting@: Do you have a sense for what the correct fix(es) should be here?  Should we somehow be doing a SelectAll in this case to avoid letting an attacker scroll the origin out of view with a fragment navigation?  (No objections if you want to take this over-- I imagine you're more familiar with the corner cases in this code than I am.)  :)

### pk...@chromium.org (2017-03-21)

+CC krb, since this is related to some work he is doing with how to muck with selection with reverts and focus changes.

I was going to say: "OmniboxEditModel::Revert() places the caret at the end of the text because it's designed for the case when the user hits <esc> while editing".  But that's a lie; if you hit esc while editing, we select all.

I don't know what case this is actually designed for.  It traces back to before the public launch.  I can't trace further at the moment because my access to the historical pre-launch repo is currently blocked for some reason.

Making OmniboxEditModel::Revert() always select all might be reasonable, but could cause problems given the comments in OmniboxViewViews::Update() about what happens if we think the box was previously select-all.  I wonder if we'd have to fix those issues to consider doing this.

### kr...@chromium.org (2017-03-21)

With ToT, I get a left-shifted highlighted URL. If I then hit right arrow, I get the spoof. This all sounds WAI to me. Perhaps we'd just like to put an ellipsis left of the visible text to indicate that there's more? I rather suspect we should do this anyways, for clarity, and consistency with something going off the right edge.

### cr...@chromium.org (2017-03-21)

https://crbug.com/chromium/681740#c17: As I noted in https://crbug.com/chromium/681740#c15, the spoof seems to work if you put a period at the end of the URL.  Try this in DevTools and then select part of the URL before the 5 second timer fires:

setTimeout(function() { location.href="#  http://www.google.com                                                                                                                                                                                                                                                         ."; }, 5000);

### cr...@chromium.org (2017-03-24)

krb@: Would you be able to take this over?  I'll be OOO for the next week, and I'm not very clear on this omnibox code anyway.  Now that we understand a bit more of why it's happening, I think it's largely a question of how to change it.

(I'm also skeptical that an ellipsis will be enough to make it clear it's a URL spoof and that we'll want to keep the origin in view in this case, but I could be wrong.)

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### kr...@chromium.org (2017-05-03)

I still can't get this to happen with the original spoof, even when I change the href to have a trailing dot, or when I change the code to:

setTimeout(function() { location.href = "# ...

This method appears to remove focus from the Omnibox and simply append the hash.

The only way that I have found to duplicate it is with the dev-tool trick *and* we haven't selected all. This still seems contrived to me.

I tried the change to SetWindowTextAndCaretPos, and it does clobber this one case, but seems to break OmniboxViewTest.BasicTextOperations and OmniboxViewTest.SelectAllStaysAfterUpdate on all the platforms. Presumably they can be changed, but it implies that behavior isn't correct.

### he...@gmail.com (2017-05-03)

#21, I gave a look again at the PoC and is seems that it's not working anymore on M58 (even with the trailing dot). I guess the change that made dialogs tab-modal is preventing it to work.

That being said, I found out that using the onbeforeunload dialog we can 
achieve the same spoof as before and also that there's a way to "bypass" the need for a trailing dot (using a different white space character).

Here's the new PoC:
https://lbherrera.github.io/lab/spoof.html

* After clicking in the omnibox you need to click in the "Leave" button (but it's also possible to make the spoof work even if the user clicks in "Stay").

### kr...@chromium.org (2017-05-04)

[Empty comment from Monorail migration]

### kr...@chromium.org (2017-05-08)

[Empty comment from Monorail migration]

### kr...@chromium.org (2017-05-10)

[Empty comment from Monorail migration]

### kr...@chromium.org (2017-05-11)

I realized why I wasn't seeing exactly what creis@ and others were seeing. A 'is_debug=true' build behaves differently. In this build, the URL is always selected and visible to the left.

But even a non-debug build doesn't always display the issue. However, if I click on the main window before clicking the omnibox, it consistently happens.

I considered creis@s statement, "Since the omnibox has focus, we're setting the caret position to the end of the text.  I think this is surprising, since the text has just changed to something the page controls." It seems to me that we shouldn't scroll if the user wasn't inputting anything.

Changing OmniboxEditModel::Revert() to:

{
  bool user_input_was_in_progress = user_input_in_progress_;
  SetInputInProgress(false);
  ...
  view_->SetWindowTextAndCursor ...
      has_focus() && user_input_was_in_progress ? ...

seems to narrow the cases where we scroll. The only thing I worry about is that the cursor is visible to the left after these pages have settled, but perhaps this is ok.

### bu...@chromium.org (2017-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5a8c1da2cda8f195695bc226dacdd35964df4113

commit 5a8c1da2cda8f195695bc226dacdd35964df4113
Author: krb <krb@chromium.org>
Date: Wed May 17 13:34:02 2017

If text was appended to a URL, the omnibox was shifting it to show the new text. This change makes it such that the text is only shifted if the user is editing. Otherwise, it homes the cursor, showing the origin.

BUG=681740

Review-Url: https://codereview.chromium.org/2860503004
Cr-Commit-Position: refs/heads/master@{#472440}

[modify] https://crrev.com/5a8c1da2cda8f195695bc226dacdd35964df4113/chrome/browser/ui/omnibox/omnibox_view_browsertest.cc
[modify] https://crrev.com/5a8c1da2cda8f195695bc226dacdd35964df4113/components/omnibox/browser/omnibox_edit_model.cc


### kr...@chromium.org (2017-05-18)

[Empty comment from Monorail migration]

### mp...@chromium.org (2017-05-22)

Fixed?

### bu...@chromium.org (2017-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0daf68bf98988529e6fe65c29f3de08a497e5564

commit 0daf68bf98988529e6fe65c29f3de08a497e5564
Author: krb <krb@chromium.org>
Date: Fri May 26 17:31:20 2017

[omnibox] Break out SetCaretPos() method and enhance browser test

Instead of calling SetWindowTextAndCaretPos() twice, add a SetCaretPos()
method so that we can call it instead.

Also, enhance the portable browser tests to make sure the caret
position is restored, but also capped at the text length.

BUG=681740

Review-Url: https://codereview.chromium.org/2891653003
Cr-Commit-Position: refs/heads/master@{#475045}

[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/chrome/browser/ui/cocoa/omnibox/omnibox_view_mac.h
[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/chrome/browser/ui/cocoa/omnibox/omnibox_view_mac.mm
[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/chrome/browser/ui/omnibox/omnibox_view_browsertest.cc
[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/chrome/browser/ui/views/omnibox/omnibox_view_views.cc
[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/chrome/browser/ui/views/omnibox/omnibox_view_views.h
[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/components/omnibox/browser/omnibox_edit_model.cc
[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/components/omnibox/browser/omnibox_edit_unittest.cc
[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/components/omnibox/browser/omnibox_view.h
[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/ios/chrome/browser/ui/omnibox/omnibox_view_ios.h
[modify] https://crrev.com/0daf68bf98988529e6fe65c29f3de08a497e5564/ios/chrome/browser/ui/omnibox/omnibox_view_ios.mm


### kr...@chromium.org (2017-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-27)

[Empty comment from Monorail migration]

### aw...@google.com (2017-05-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-05)

[Comment Deleted]

### aw...@chromium.org (2017-06-05)

Nice one!  The panel decided to award $1,000 for this bug!

### aw...@chromium.org (2017-06-05)

[Empty comment from Monorail migration]

### he...@gmail.com (2017-06-07)

 awhalley@: Will a CVE be assigned to this bug?

### aw...@chromium.org (2017-06-07)

luan.herrera@ - yep, when Chrome 60 goes stable.

### sh...@chromium.org (2017-06-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-09)

Your change meets the bar and is auto-approved for M60. Please go ahead and merge the CL to branch 3112 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-07-10)

Please merge this to M60 ASAP. branch:3112

### kr...@chromium.org (2017-07-10)

Change 5a8c1da2 is already in M60. It contains the bug-fix. Change 0daf68bf is simply clean-up for it, and not urgent.

If you'd still like it, I can merge it but thought you should know about the state.

### kr...@chromium.org (2017-07-10)

[Empty comment from Monorail migration]

### cr...@chromium.org (2017-07-10)

Agreed-- it sounds like r472440 is all we need, and that's already in M60.  Thanks!

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2017-09-02)

Restoring restriction to verify team is ok with it.

### sh...@chromium.org (2017-09-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/681740?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>Navigation, UI>Browser>Omnibox, UI>Browser>Omnibox>SecurityIndicators]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086530)*
