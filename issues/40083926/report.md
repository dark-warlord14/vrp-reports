# Security: URL spoof + iframe spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40083926](https://issues.chromium.org/issues/40083926) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Linux, Windows |
| **CVE IDs** | CVE-2016-1664 |
| **Reporter** | wa...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2016-03-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

Iframes history navigation causing URL spoof and iframe spoof (iframes replaced by malicious ones)

**VERSION**  

Chrome Version: 49.0.2623.87 m stable  

Operating System: Windows, 7, service pack 1

**REPRODUCTION CASE**

Steps to follow:

1- Open the attached file <http://localhost/attack.html>  

2- Click on the "iframe2" button  

3- Click on the "go to youtube" link  

4- Navigate back to the first page (2 backs)  

5- Click on the "Start Attack" button

Iframe Spoof:  

You will see that the iframe of youtube has been replaced by the iframe containing wikipedia.  

URL Spoof:  

From the page containing the spoofed iframe, if you go back one page, you will spoof the domain "localhost" by displaying in its content the content of youtube.

## Attachments

- [attack.html](attachments/attack.html) (text/plain, 415 B)
- [iframespoof.png](attachments/iframespoof.png) (image/png, 264.5 KB)
- [urlspoof.png](attachments/urlspoof.png) (image/png, 266.5 KB)
- [attack.html](attachments/attack_53418874.html) (text/plain, 501 B)
- [attack2.html](attachments/attack2.html) (text/plain, 622 B)
- [frozen_spoof.html](attachments/frozen_spoof.html) (text/plain, 176 B)

## Timeline

### wf...@chromium.org (2016-03-23)

I can't reproduce this either with stable 49.0.2623.87 or canary 51.0.2686.0 on Windows.

Can you confirm what I am meant to see after step 5? Can you enclose a screenshot of what you see?

### wf...@chromium.org (2016-03-23)

[Empty comment from Monorail migration]

### wa...@gmail.com (2016-03-24)

Try with the new attached "attack.html" and replace step 2 by:
'2- Click on the "iframe1" button then on the "iframe2" button'.

This attack is very reliable on my system.

### wf...@chromium.org (2016-03-24)

I still can't seem to be able to reproduce this. I've tried both on a webserver from http://localhost and also remotely e.g. http://myserver.mydomain.com/

All I get when I click the "Start Attack" button is that youtube loads correctly with no evidence of any other frame.

It looks like from your screenshots that the iframe is appearing maybe where youtube's flash object appears?

What is the iframe in the youtube site that you expect to be replaced?

### wa...@gmail.com (2016-03-24)

the iframe that is replaced in youtube is the advertising iframe. 
It works on other websites than youtube (as long as they contain iframes).

### wf...@chromium.org (2016-03-24)

are you sure this isn't aggressive caching by your network? Can you try on another network or with a fresh profile?

### wa...@gmail.com (2016-03-24)

I tried from different networks and after deleting the cache, and it works.

By experimenting with delays inside the "attack()" function by adding setTimeout(), the attack fails. This tells me that if the reload of the iframes occurs when we navigate forward in the history and if this reload is too fast, the attack will fail.

Your network connection is too fast, maybe that's the cause.
For the iframe spoof attack, since the localhost domain is attacker controlled, the attacker could force the load of its iframes to be slow.

Maybe you should try with slow loading iframes when you test the attack.
For me it works every time.

### sh...@chromium.org (2016-03-24)

Thank you for providing more feedback. Assigning to requester "wfh@chromium.org" for another review.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2016-03-24)

adding some navigation experts. I'll have to find some slow loading iframes or a way to try and reproduce this to try and get an idea of the impact.

[Monorail components: UI>Browser>Navigation]

### na...@chromium.org (2016-03-24)

I have a page that simulates a slow response. Feel free to use it: http://tests.netsekure.org/slow.php?seconds=5

### cr...@chromium.org (2016-03-25)

I was able to repro the URL spoof portion of it (not yet the wrong iframe portion), using DevTools.  You can open the Network conditions tab (under "More Tools" in the menu), then set Network Throttling to Regular 3G.

Note that I'm not seeing it with the new navigation stack in --isolate-extensions, so it might not repro if you're in the SiteIsolationExtensions field trial (on Canary or Dev channel).  You can avoid that by passing --force-fieldtrials=SiteIsolationExtensions/Control at the command line.

Anyway, looks like we might be getting something wrong when updating PageState on the NavigationEntry.  Not sure about the implications so far, given how much user interaction is required.  I'll take a look to see what's going on.

### wf...@chromium.org (2016-03-25)

I'm tentatively giving this a medium if you can spoof in this way. creis do you think that's about right here?

### cl...@chromium.org (2016-03-26)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-03-28)

wfh@: It depends on whether it requires the user to go back or not.  I'll know more once I get a minimized repro case.

To follow up, I'm able to repro both the URL spoof and the wrong iframe issue in a debug build.  We hit a NOTREACHED in NavigationControllerImpl::RendererDidNavigateAutoSubframe, which means this is related to https://crbug.com/chromium/486916.  (Hopefully the fix for this will let us turn that NOTREACHED into a renderer kill, as I'd hoped.)

I'm doing some debugging to find out where we're going wrong.  It's likely in HistoryController / HistoryEntry in the renderer process, perhaps in a way that doesn't apply to the new session history logic in --isolate-extensions and other OOPIF-enabled modes (as mentioned above).  I haven't had luck using simpler pages yet, so I'll have to keep debugging with the large sites for now.  I'm guessing we're committing some subframe to the wrong HistoryEntry.

### wa...@gmail.com (2016-03-29)

Here is another attack that spoofs URLs.

Steps to follow:

1- Open http://localhost/attack2.html
2- Load iframe1 
3- Load iframe2
4- Open Youtube link
5- Go Back 2 times
6- Execute attack2 
7- Go Forward 1 time

This will spoof the URL https://www.youtube.com, although it still requires the victim to press back in step 3.



### mb...@chromium.org (2016-03-29)

[Empty comment from Monorail migration]

### cr...@chromium.org (2016-03-30)

Looks like one of the bugs is in HistoryController::UpdateForCommit.  When it sees a back/forward commit for a frame, it assumes it must match any existing provisional HistoryEntry and thus makes it the current entry.  In this case, the commit is for Wikipedia in the attack page's iframe, but the provisional entry is already YouTube.  Thus, we end up putting a Wikipedia HistoryItem on the YouTube HistoryEntry.

When we later commit the YouTube page in the main frame, we see the Wikipedia HistoryItem in the HistoryEntry and load Wikipedia within YouTube, which explains the iframe spoof.

When we go back from there, the second bug is that we've somehow ended up with YouTube in the PageState of the NavigationEntry.  The NavigationEntry's URL is correct (i.e., the attack page), but the HistoryEntry tells us to go to YouTube instead.  (It's bad that the NavigationEntry's URL and the PageState's URL don't match.)

The outcome is that HistoryController thinks the main frame doesn't need to change (since it's already on YouTube), and it navigates one of the subframes to about:blank instead.  That's an AUTO_SUBFRAME navigation, which hits the NOTREACHED I mentioned in https://crbug.com/chromium/597322#c14 in debug builds.  In release builds, we just commit that back NavigationEntry and show the attack page's URL over the YouTube content.

I'll try to track down how to avoid committing the provisional entry and how to avoid corrupting the PageState.

### cr...@chromium.org (2016-03-31)

Ah, and the PageState corruption makes sense here, since the renderer process thinks the current entry is YouTube while we're still on the attack page (due to the first bug), so when we do actually go to YouTube, the UpdateState message we send uses that incorrect HistoryEntry.  Maybe we can start catching that in the browser process with a sanity check.

### cr...@chromium.org (2016-04-01)

A proposed fix is up for review at https://codereview.chromium.org/1848103004/, and the test is in a separate CL at https://codereview.chromium.org/1848813005/.  (I had to do the test separately because it relies on a test utility class that hasn't quite landed yet.  Separating them will also make the fix easier to merge.)

### bu...@chromium.org (2016-04-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bb3548ef2fcdb58f9bc638bb5a3c379320fdd0e0

commit bb3548ef2fcdb58f9bc638bb5a3c379320fdd0e0
Author: creis <creis@chromium.org>
Date: Fri Apr 01 19:21:08 2016

Fix HistoryEntry corruption when commit isn't for provisional entry.

BUG=597322
TEST=See bug for repro steps.

Review URL: https://codereview.chromium.org/1848103004

Cr-Commit-Position: refs/heads/master@{#384659}

[modify] https://crrev.com/bb3548ef2fcdb58f9bc638bb5a3c379320fdd0e0/content/renderer/history_controller.cc


### cr...@chromium.org (2016-04-01)

This should be fixed now in r384659.  We'll see how that does over the weekend before merging to M50 or M49.  mbarbella@, any reason this was labeled M50 rather than M49?  I think it affects both.

I like the new example in https://crbug.com/chromium/597322#c15-- it shows how this bug can be used to put the victim's URL over the attacker's content (as needed for a useful attack), rather than the attacher's URL over the victim's content (as in the original steps).

I'll also note that steps 2, 3, 4, 6, and even 7 from https://crbug.com/chromium/597322#c15 can all be done by the attacker.  However, I haven't been able to think of a way for the attacker to do step 5 (go back from the victim page to the attacker's page).  You can't do a back navigation on a cross-origin window.

I think requiring user interaction counts as a mitigating factor, so that would keep this as medium severity rather than high (for "control over the apparent origin of the omnibox").  If you find a way to do it without any user interaction in step 5, let us know.

Thanks for the nice report!  I'll try to follow up with some extra lines of defense once this is landed (e.g., upgrading the NOTREACHED from https://crbug.com/chromium/486916 to a renderer kill).

### mb...@chromium.org (2016-04-01)

Merging it back to M-49 sounds good to me. For medium severity we choose between beta and stable on a case-by-case basis, but if it seems like a straightforward merge there's no reason not to request it here.

### cl...@chromium.org (2016-04-01)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### wa...@gmail.com (2016-04-04)

It is possible to do the URL spoof using other techniques, but the attacker's page will be frozen. See attached file for an example.

I don't think there is a way to do step 5 (go back from the victim page to the attacker's page) of the attack described in https://crbug.com/chromium/597322#c15 without user interaction. 

However, the attacker may increase the probability of the victim pressing on the back button (without social engineering).
He can open 2 tabs (in the same renderer process), one of them navigates to youtube (the URL to spoof) and the other, after waiting a while for youtube to finish displaying, crashes the renderer process by making the browser process kill it. 
This can be done by displaying, for example, some malformed pdf file.
Once the renderer process has crashed, the victim has now 2 choices: "go back" or "refresh" (50-50 chances of "go back" since the refresh button from the crash page has disappeared). 
If the victim goes back, the URL spoof attack will succeed. 

### cr...@chromium.org (2016-04-04)

Looks like my fix led to some crashes if there was no current entry and the provisional entry didn't match (see https://crbug.com/chromium/600238).  I'll revert and land an updated fix.

### bu...@chromium.org (2016-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/413fc09a3fa2e915410d39034d78661837468633

commit 413fc09a3fa2e915410d39034d78661837468633
Author: creis <creis@chromium.org>
Date: Mon Apr 04 17:43:40 2016

Revert of Fix HistoryEntry corruption when commit isn't for provisional entry. (patchset #2 id:20001 of https://codereview.chromium.org/1848103004/ )

Reason for revert:
This led to crashes in HistoryController::UpdateForCommit if there is no current entry and the provisional entry doesn't match the commit.  See https://crbug.com/600238.  I'll land an updated fix.

Original issue's description:
> Fix HistoryEntry corruption when commit isn't for provisional entry.
>
> BUG=597322
> TEST=See bug for repro steps.
>
> Committed: https://crrev.com/bb3548ef2fcdb58f9bc638bb5a3c379320fdd0e0
> Cr-Commit-Position: refs/heads/master@{#384659}

TBR=japhet@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=597322

Review URL: https://codereview.chromium.org/1859593003

Cr-Commit-Position: refs/heads/master@{#384938}

[modify] https://crrev.com/413fc09a3fa2e915410d39034d78661837468633/content/renderer/history_controller.cc


### cl...@chromium.org (2016-04-05)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### cr...@chromium.org (2016-04-05)

Guess the merge label threw ClusterFuzz off.  It's not fixed, due to the revert in https://crbug.com/chromium/597322#c26.

### cr...@chromium.org (2016-04-05)

That said, I have repro steps for the crash in https://crbug.com/chromium/600238, so I should be able to update the fix and re-land it.  It happens when you get a redirect when navigating back/forward in a newly created tab (e.g., Ctrl+click back/forward).

1) Sign into Gmail.
2) Click into a message.
3) Go back.
4) In a new tab, sign out of Google.
5) In the Gmail tab, Ctrl+Click Forward.

In this case, the item sequence number will be different even though the provisional entry should be committed in HistoryController.  We should probably verify the frame's ancestors match the provisional entry instead.

### cr...@chromium.org (2016-04-11)

I have an updated fix up for review here:
https://codereview.chromium.org/1848813005/

### bu...@chromium.org (2016-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/82500315884357312b3caafb49d347ef011c296f

commit 82500315884357312b3caafb49d347ef011c296f
Author: creis <creis@chromium.org>
Date: Tue Apr 12 19:56:03 2016

Fix HistoryEntry corruption when commit isn't for provisional entry (try #2).

BUG=597322, 600238
TEST=See bug for repro steps.
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review URL: https://codereview.chromium.org/1848813005

Cr-Commit-Position: refs/heads/master@{#386785}

[modify] https://crrev.com/82500315884357312b3caafb49d347ef011c296f/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/82500315884357312b3caafb49d347ef011c296f/content/renderer/history_controller.cc


### cr...@chromium.org (2016-04-12)

Should be fixed again in r386785.  If it looks good on tomorrow's canary, we can start the merge process.

### cr...@chromium.org (2016-04-14)

The fix has been present since 52.0.2707.0, and there don't appear to be any crashes this time.

Ok if I start by merging to M51?

### ti...@google.com (2016-04-14)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### bu...@chromium.org (2016-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f2fe508569075c99b5a4566d9aaaa280e3c229e9

commit f2fe508569075c99b5a4566d9aaaa280e3c229e9
Author: creis <creis@chromium.org>
Date: Thu Apr 14 20:16:14 2016

Fix HistoryEntry corruption when commit isn't for provisional entry (try #2).

BUG=597322, 600238
TEST=See bug for repro steps.
TBR=japhet,alexmos
NOTRY=true
NOPRESUBMIT=true

Review URL: https://codereview.chromium.org/1848813005

Cr-Commit-Position: refs/heads/master@{#386785}
(cherry picked from commit 82500315884357312b3caafb49d347ef011c296f)

Review URL: https://codereview.chromium.org/1892593002

Cr-Commit-Position: refs/branch-heads/2704@{#60}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/f2fe508569075c99b5a4566d9aaaa280e3c229e9/content/browser/frame_host/navigation_controller_impl_browsertest.cc
[modify] https://crrev.com/f2fe508569075c99b5a4566d9aaaa280e3c229e9/content/renderer/history_controller.cc


### cr...@chromium.org (2016-04-14)

tinazh: Should I merge to M50 as well?  I'll need to land just the fix and not the test, since the test relies on a utility class added in M51.  The fix should be safe, though.

### sh...@chromium.org (2016-04-15)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-15)

[Automated comment] Less than 2 weeks to go before stable on M50, manual review required.

### go...@chromium.org (2016-04-15)

Reply to https://crbug.com/chromium/597322#c36, without the test, can your fix pass through the unit test?

### cr...@chromium.org (2016-04-15)

Yes, it will pass all the existing tests.  I just can't easily merge the new test to the M50 branch.

### go...@chromium.org (2016-04-15)

OK, thank you. Approving merge to M50 branch 2661. Please merge ASAP. Thank you.

### bu...@chromium.org (2016-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1c6963d11c9f7deb4e88b8b0a555e73719da2056

commit 1c6963d11c9f7deb4e88b8b0a555e73719da2056
Author: creis <creis@chromium.org>
Date: Fri Apr 15 22:24:33 2016

Fix HistoryEntry corruption when commit isn't for provisional entry (try #2).

(Omit the newly added tests, which won't compile on M50 branch.)

BUG=597322, 600238
TEST=See bug for repro steps.
TBR=japhet,alexmos
NOTRY=true
NOPRESUBMIT=true

Review URL: https://codereview.chromium.org/1848813005

Cr-Commit-Position: refs/heads/master@{#386785}
(cherry picked from commit 82500315884357312b3caafb49d347ef011c296f)

Review URL: https://codereview.chromium.org/1892273003

Cr-Commit-Position: refs/branch-heads/2661@{#592}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/1c6963d11c9f7deb4e88b8b0a555e73719da2056/content/renderer/history_controller.cc


### cr...@chromium.org (2016-04-18)

Too late to merge to M49.  Looks like this is done.

### ti...@google.com (2016-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-02)

Congratulations again - $1000 for this report. I'll add it to your payment for https://crbug.com/chromium/601629 (and see that bug for info on payment details).

The CVE-ID for this vulnerability is CVE-2016-1664

Thanks again!

### ti...@google.com (2016-05-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-05-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fb6eeb6dde866fbe9b48b62311eb6cc48771fc70

commit fb6eeb6dde866fbe9b48b62311eb6cc48771fc70
Author: creis <creis@chromium.org>
Date: Tue May 10 19:01:51 2016

Kill renderer if it changes the main frame's origin on subframe commits.

This is hopefully safe after the fix for 597322.  It's a useful second
line of defense against URL spoofs.

BUG=486916, 597322
TEST=No NC_AUTO_SUBFRAME kills
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/1960983002
Cr-Commit-Position: refs/heads/master@{#392666}

[modify] https://crrev.com/fb6eeb6dde866fbe9b48b62311eb6cc48771fc70/content/browser/frame_host/navigation_controller_impl.cc


### sh...@chromium.org (2016-07-20)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/597322?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083926)*
