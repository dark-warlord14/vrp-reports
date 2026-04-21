# Security: chrome url spoofing 

| Field | Value |
|-------|-------|
| **Issue ID** | [40081917](https://issues.chromium.org/issues/40081917) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Loader, UI>Browser>Navigation |
| **Reporter** | wa...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2015-04-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

URL spoofing triggered by race condition.

**VERSION**

Chrome Version: [41.0.2272.118 m] + [stable]  

Operating System: [Windows, 7, service pack 1]

**REPRODUCTION CASE**

open 'Read me.txt' and follow instructions.

## Attachments

- [chrome attack POC.zip](attachments/chrome attack POC.zip) (application/zip, 13.6 KB)
- [chrome attack POC 2.zip](attachments/chrome attack POC 2.zip) (application/zip, 12.1 KB)

## Timeline

### mb...@chromium.org (2015-04-23)

I haven't been able to reproduce this locally (tried with a few different timeout values). Tentatively setting severity to medium and stable impact.

wadih.matar: Thanks for the report. If you're able to provide a more reliable reproduction case, it would help us a lot with fixing the issue and when determining if it qualifies for a reward.

creis: Any idea what might be going on here?


### cl...@chromium.org (2015-04-23)

[Empty comment from Monorail migration]

### wa...@gmail.com (2015-04-24)


What might be going on:
______________________


On the spoofed page, executing the javascript function history.replaceState() crashes the renderer process.
After some analysis, i think that the browser is killing the renderer, and it happens in AreURLsInPageNavigation() of /src/content/browser/frame_host/navigation_controller_impl.cc.

In this function bad_message::ReceivedBadMessage() is processed if is_same_origin (of the new and existing urls) is false. This suggests that one "part" of chrome thinks that the existing url is youtube.com and another "part" thinks that the existing url is localhost. I think that the browser process thinks (in navigationentries?) the existing url is youtube.com and the renderer process thinks that the existing url is
localhost.
This also suggests that the bug is not a display bug. It seems that one of the browser or renderer is updated incorrectly or not updated (concerning
the information of the current url).


 
Concerning the exploit:
___________________________


I get a reasonable amount of success (displays the spoofed page) from the attack (around 30% on average).
I just tested it on chrome 41 and windows 7.


There can be 4 possible outcomes from the attack:


1- the attack doesn't reach lastpage.html and youtube.com opens (the real one). The attack fails.

2-the attack reaches laspage.html. When lastpage.html starts doing back(), youtube opens. The attack fails.

3-the attack reaches laspage.html. When lastpage.html starts doing back(), youtube doesn't open at all. The attack fails.

4-the attack reaches laspage.html. When lastpage.html starts doing back(), youtube.com shows up in the url but the backs continue. The attack created a spoofed page in the chain. Now it's a matter of finding it in the chain (fwdcounter is trying to guess its position). 



I will think about how to make the exploit more reliable.


### cr...@chromium.org (2015-04-24)

Thanks for the explanation.  I'm definitely interested in tracking down cases that AreURLsInPageNavigation is killing the renderer process, and I agree that the confusion about the current URL between the browser process and renderer process is concerning.

I'm still trying to get your example to succeed.  One thing I noticed: the code in the file you attached doesn't use replaceState at all, though the readme file claims that it does.  Did you upload the right version?  Where is the replaceState call taking place?

### cr...@chromium.org (2015-04-24)

I've taken a closer look at AreURLsInPageNavigation, and there is indeed a bug in one of the call sites.  Specifically, ClassifyNavigation is passing the existing entry's URL rather than the last committed entry's URL.  |existing_entry| is supposed to have the same URL as params.url, so comparing it against params.url is kind of a no-op.

However, it would only kill the renderer process if you did a replaceState *after* another bug put the wrong (cross-origin) URL into an existing NavigationEntry.  In other words, seeing that crash means you've likely already achieved the spoof and this is just a side effect.

That means we're looking for another bug that would lead us to put the wrong URL into an existing entry.  I'm eager to track it down, but I may need a more reliable proof of concept to be able to diagnose it.

### wa...@gmail.com (2015-04-24)

I managed to get a more reliable exploit. 
I tested it on 41.0.2272.118 m and 42.0.2311.90 m. 
It worked and the success rate is much higher now (the spoofed page is created more oftently and its position is more predictable).

Main change: adding a sleep function at the begining of the fastbacks function.

Start the attack and wait for the message "the attack is finished. If you can see youtube.com in the url it means it succeeded." to be displayed.


N.B: in the read me.txt i was describing another exploit idea using replaceState and the renderer crash to determine more precisely the position of the spoofed page. The code i uploaded before did not use this technique.

### cr...@chromium.org (2015-04-25)

That makes sense about replaceState, given https://crbug.com/chromium/480201#c5.  Your attack likely wouldn't depend on it.

Thanks for the new file; I'll give it a try.  I also tried removing the forward operations in the previous approach so that I could just click back/forward myself.  It already shows "I am iframe 2" inside an iframe of youtube.com, which is bad on its own.

This likely indicates a race or a bug in UpdateState, which explains how we would get into a spoofable state.  I'll take a closer look.

### cr...@chromium.org (2015-04-25)

CC'ing avi@, since this may be relevant to the confusing UpdateState cases we've seen in the past.

### wa...@gmail.com (2015-04-25)

Regarding the replacement of the iframe of youtube.com by iframe2.html, i already did the following test:

Execute from youtube.com :

//(the id of the iframe of youtube.com was "ad_creative_iframe_1")
var iframeWin = document.getElementById("ad_creative_iframe_1").contentWindow;
iframeWin.postMessage("secretmessage", "*");


The listener of iframe2.html got the message. This could be a dangerous attack.

### mb...@chromium.org (2015-04-25)

[Empty comment from Monorail migration]

### cr...@chromium.org (2015-04-27)

Thanks for the new version.  It's still pretty unreliable for me, but I was able to repro the whole spoof at least once.

The bug is actually deeper than UpdateState, and I may need japhet@'s help.  The key piece seems to be that HistoryController's current_entry_ is not getting updated when we go from attack.html to youtube.com.  Blink is showing youtube.com, and the browser process is notified via DidCommit that we're on youtube.com, but HistoryController's current entry is still attack.html.

Because the back/forward history is filled with manual subframe navigations, going back *should* schedule a navigation in the main frame (from youtube.com back to attack.html), but HistoryController thinks we're already on attack.html so it only schedules a navigation in the first subframe.  That's how I ended up with iframe2.html inside YouTube in https://crbug.com/chromium/480201#c7, and I suspect it's a building block for the rest of the spoof.

japhet@: The reason HistoryController gets confused is that FrameLoader is calling UpdateForCommit with WebHistoryInertFrame, even though it's a navigation from attack.html to youtube.com.  This happens during a call from FrameLoader::receivedFirstData(), where m_loadType is FrameLoadTypeRedirectWithLockedBackForwardList.  I dug a little further and found that m_loadType was set to that value by FrameLoader::determineFrameLoadType, because request.lockBackForwardList() was true.

It starts to go over my head at this point, deep in the Blink loader logic.  Why would Blink classify a navigation from attack.html to youtube.com as a redirect with a locked back/forward list?  (Note that the relevant navigation is the parent.location = "https://www.youtube.com"; call in iframeattack.html, and it's likely racing with other subframe navigations.)

### ja...@chromium.org (2015-04-28)

The reason for the FrameLoadTypeRedirectWithLockedBackForwardList is in NavigationScheduler::mustLockBackForwardList. The first clause causes script-initiated navigations before the load event to lock the back forward list, and that appears to be what's happening here.

I'm suspicious that HistoryController's state is somehow getting out of sync with blink state, and that's the real bug. In the inert commit case, blink sets all of the relevant state on FrameLoader::m_currentItem (see FrameLoader::setHistoryItemStateForCommit), which is *supposed* to be the same underlying object as HistoryController::current_entry_->GetItemForFrame(frame) (one's a WebHitoryItem and the other is a HistoryItem, of course). The failure mode you're describing implies that it's not, in fact, the same memory under the hood.

We could presumably fix this by adding the following to HistoryController::UpdateForCommit() for the inert case:

if (HistoryEntry::HistoryNode* node =
        current_entry_->GetHistoryNodeForFrame(frame)) {
  node->set_item(item);
}

...though I'm not sure whether there's some other case that'll break. There shouldn't be, but you never know with this stuff.

### cr...@chromium.org (2015-04-28)

Thanks, that sounds like a good lead.  I'll see if I can confirm it this afternoon.

### cr...@chromium.org (2015-04-29)

Ok, it took some effort but I've finally got a more minimal, reliable repro:

1) Visit page A with a frame A1.
2) Go to page A2 in the frame.
3) Go back, then go forward.
4) Do a location.replace(B).
(Corruption happens here.  Current entry is still A, but page is B.)
5) Go back.  Viewing A, with A in address bar.
6) Go forward.  Viewing A, but B in address bar.  Spoof!

Nate's fix looks good, so I'm trying it out on the try bots (https://codereview.chromium.org/1112823005/).  I'm also adding a second line of defense in the browser process that can kill the renderer if we get a subframe commit that unexpectedly changes the main frame URL.  We'll see if the try bots are happy with that one.

I'll try to distill the new repro steps into a test case.

### wa...@gmail.com (2015-04-30)

After step 4 we land on the B page.
B is the website to spoof. The attacker has no control on its JS and therefore cannot do a window.history.back(). The back must be done manually.

The unreliability of the old exploit comes from the fact that it tries to open B while keeping control on the navigation with JS.

### cr...@chromium.org (2015-04-30)

history.back() used to be supported from a cross-origin window, so controlling it from a popup might be one option.  But a quick test of that showed that history.back() was generating a security error, so maybe that has changed.  For now, we should still consider the exploit somewhat unreliable, but it can be effective.

### bu...@chromium.org (2015-04-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/da5ec7010ba73b2b343dacd0c6d302b90b1ea7ae

commit da5ec7010ba73b2b343dacd0c6d302b90b1ea7ae
Author: creis <creis@chromium.org>
Date: Thu Apr 30 21:59:56 2015

Ensure that HistoryController's current entry is updated on inert commits.

BUG=480201
TEST=See bug for repro steps.

Review URL: https://codereview.chromium.org/1112823005

Cr-Commit-Position: refs/heads/master@{#327806}

[modify] http://crrev.com/da5ec7010ba73b2b343dacd0c6d302b90b1ea7ae/content/browser/bad_message.h
[modify] http://crrev.com/da5ec7010ba73b2b343dacd0c6d302b90b1ea7ae/content/browser/frame_host/navigation_controller_impl.cc
[modify] http://crrev.com/da5ec7010ba73b2b343dacd0c6d302b90b1ea7ae/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] http://crrev.com/da5ec7010ba73b2b343dacd0c6d302b90b1ea7ae/content/renderer/history_controller.cc
[add] http://crrev.com/da5ec7010ba73b2b343dacd0c6d302b90b1ea7ae/content/test/data/navigation_controller/page_with_data_iframe.html


### cr...@chromium.org (2015-05-01)

Fixed (with an extra line of defense) in r327806.  Verified in Mac Canary 44.0.2388.0.

### cl...@chromium.org (2015-05-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cr...@chromium.org (2015-05-01)

I'll be out next week.  Nasko, would you be able to merge mid-next week if it looks good on Canary?  I can do it when I get back if not, since I think this should definitely go to at least M43 given the history corruption.  Probably M42 as well.

The bad_message.h and navigation_controller_impl.cc merge might be tricky, since that's fairly new code and the enum values matter for histogram reporting.  It's not strictly necessary for M42 and M43, since it's just a second line of defense.  Only the history_controller.cc change is needed to fix the bug.

### na...@chromium.org (2015-05-01)

Yes, I'll keep an eye on Canary and merge mid-next week.

### na...@chromium.org (2015-05-07)

The CL looks clean on canary, shall we merge into M43 first?

### la...@google.com (2015-05-07)

[Automated comment] Request affecting a post-stable build (M42), manual review required.

### la...@google.com (2015-05-07)

[Automated comment] Less than 2 weeks to go before stable on M43, manual review required.

### la...@google.com (2015-05-08)

Given the timing this is not going to M42.

Approved for M43 (2357).

### am...@chromium.org (2015-05-11)

Not happening for 42.

### bu...@chromium.org (2015-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f1e479334250fd53ddeb8ef9614a77e0a538b6cb

commit f1e479334250fd53ddeb8ef9614a77e0a538b6cb
Author: creis <creis@chromium.org>
Date: Mon May 11 21:11:55 2015

Ensure that HistoryController's current entry is updated on inert commits.

BUG=480201
TEST=See bug for repro steps.
TBR=avi
NOTRY=true
NOPRESUBMIT=true

Review URL: https://codereview.chromium.org/1112823005

Cr-Commit-Position: refs/heads/master@{#327806}
(cherry picked from commit da5ec7010ba73b2b343dacd0c6d302b90b1ea7ae)

Review URL: https://codereview.chromium.org/1128903007

Cr-Commit-Position: refs/branch-heads/2357@{#355}
Cr-Branched-From: 59d4494849b405682265ed5d3f5164573b9a939b-refs/heads/master@{#323860}

[modify] http://crrev.com/f1e479334250fd53ddeb8ef9614a77e0a538b6cb/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] http://crrev.com/f1e479334250fd53ddeb8ef9614a77e0a538b6cb/content/renderer/history_controller.cc
[add] http://crrev.com/f1e479334250fd53ddeb8ef9614a77e0a538b6cb/content/test/data/navigation_controller/page_with_data_iframe.html


### bu...@chromium.org (2015-05-11)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/f1e479334250fd53ddeb8ef9614a77e0a538b6cb

commit f1e479334250fd53ddeb8ef9614a77e0a538b6cb
Author: creis <creis@chromium.org>
Date: Mon May 11 21:11:55 2015


### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-07)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-28)

We found some old bugs that weren't voted on and took them to the reward panel last week. This was one of them.

Our reward panel decided to award you $1,000 for this report. 

Panel notes: Good spoof by race condition, though looks unreliable due to race condition prerequisite. 

Our finance team should be in touch within 7 days. If that doesn't happen, please contact me directly at timwillis@

Thanks for your report!

### aw...@chromium.org (2016-07-01)

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

This issue was migrated from crbug.com/chromium/480201?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081917)*
