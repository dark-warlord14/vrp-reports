# Chromium allows to open popup window from Flash object without user gesture or blocking

| Field | Value |
|-------|-------|
| **Issue ID** | [40083539](https://issues.chromium.org/issues/40083539) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Permissions, Internals>Plugins>Flash |
| **Platforms** | Mac |
| **Reporter** | an...@gmail.com |
| **Assignee** | sp...@chromium.org |
| **Created** | 2016-01-21 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 YaBrowser/16.2.0.2567 (beta) Safari/537.36

Steps to reproduce the problem:
1. Create  a web page with flash object. See code of web page and code in attached index.html and code of swf in attached Main.as. I also attached compiled swf.
2. Upload this web page and swf to web server, it won't be work if it is opened as local file.
3. Go to this web server by Chrome/ Chromium.
4. Click anywhere on page.

What is the expected behavior?
Chromium blocks popup with message

What went wrong?
Popup window opens and in OX gets focus.

Did this work before? N/A 

Chrome version: 47.0.2526.73  Channel: stable
OS Version: OS X 10.11.2
Flash Version: Shockwave Flash 20.0 r0

I deploy PoC in http://jabbos.org/swf_test/. Please, check it.

## Attachments

- [newsecuritytest.swf](attachments/newsecuritytest.swf) (application/octet-stream, 824 B)
- [Main.as](attachments/Main.as) (application/octet-stream, 931 B)
- [swfobject.js](attachments/swfobject.js) (text/javascript, 10.0 KB)
- [swf_test.zip](attachments/swf_test.zip) (application/zip, 7.5 KB)
- [index.html](attachments/index.html) (text/html, 1.2 KB)
- [stable.png](attachments/stable.png) (image/png, 279.8 KB)
- [Screenshot from 2016-01-26 14_15_46 (1).png](attachments/Screenshot from 2016-01-26 14_15_46 (1).png) (image/png, 316.9 KB)
- [new_index.html](attachments/new_index.html) (text/html, 1.4 KB)

## Timeline

### lg...@chromium.org (2016-01-21)

I've confirmed that on OSX it opens up a new tab.

On stable (47), the tab maximizes.
On Beta (48), it actually goes fullscreen and 1) moving your cursor to the top of the screen shows the menu bar but not the omnibox and tab strip, and 2) *you can't use Esc to escape* (Cmd-Ctrl-F works, though).

Marking this as high severity based on [1]. We should consider fixing this in the pre-stable branch (48) before it goes full-stable next week.

[1] http://www.chromium.org/developers/severity-guidelines

mgiuca@, are you the right person to take this?

### cl...@chromium.org (2016-01-21)

[Empty comment from Monorail migration]

### lg...@chromium.org (2016-01-21)

[Empty comment from Monorail migration]

### mg...@chromium.org (2016-01-21)

Sorry, I don't think I'm the right person. I don't do Mac and I haven't had anything to do with the actual fullscreen mode, just the presentation of the permission prompt.

+spqchan who has been looking at this stuff on Mac.

### sp...@chromium.org (2016-01-21)

The hidden omnibox and tabstrip is intentional for media in fullscreen.
I'm 90% sure that ESC key issue is the same one that I've been working on, in which pressing ESC won't let you exit fullscreen if you entered it via extensions.


### mg...@chromium.org (2016-01-21)

On Linux (49.0.2623.13), the new window is opened *behind* the current browser window, but has keyboard focus. So I'm considering this a Linux bug too.

On Chrome OS (49.0.2618.9), the new window is in the foreground, so not really a security bug. On Windows (49.0.2618.0), the new window is in the background and without focus, so also not really a security bug, but the popup could still be blocked in both those cases.

### sp...@chromium.org (2016-01-21)

I'm trying to figure out what we want to do for this. 

I *might* be able to fix the ESC key issue for this, but I'm not too sure because looking into this a bit more carefully, the fullscreen is in a strange state. I'm can't tell if the fullscreen is for "tab content" or for "browser". I'm leaning towards browser because I noticed that you don't exit fullscreen when you switch tabs (which should be the case for "tab content" fullscreen) and there's a lack of permission bubbles.

- If it's a browser fullscreen, then you're not supposed to use ESC to escape. However, the tab and omnibox should be there.

- If it's "tab content", ESC key should work, but there should be a permission bubble

- The extension fullscreen issue I mentioned also don't match it. The tabs and omnibox still appears for extensions, and we should at least see a permission bubble.

I'm not sure what the expected behavior should be for this. From what I gathered...it shouldn't open a new tab, let alone enter fullscreen in the first place. In that case, I don't think I'm the right person for this

Can you please clarify?

### sp...@chromium.org (2016-01-22)

+ihf who has been working on Flash stuff

### ti...@google.com (2016-01-22)

We'll do a M48 stable refresh early next week and can take this if the fix can be landed this week and merge by next Mon. Thanks.

### ti...@google.com (2016-01-22)

[Empty comment from Monorail migration]

### an...@gmail.com (2016-01-22)

[Comment Deleted]

### an...@gmail.com (2016-01-22)

Hello, could you please provide me information, whether it falls under: https://www.google.ru/about/appsecurity/chrome-rewards/ or not?

### sp...@chromium.org (2016-01-22)

[Empty comment from Monorail migration]

### lg...@chromium.org (2016-01-22)

Re #12: Yes, if you do not disclose it via other channels until the fix has reached most users, this qualifies for consideration under the VRP. I'm adding `reward-topanel` to make sure it reaches the panel.

mgiuca: I thought even Flash fullscreen was supposed to show a "You've gone fullscreen" prompt?

### lg...@chromium.org (2016-01-22)

[Empty comment from Monorail migration]

### ih...@chromium.org (2016-01-22)

[Empty comment from Monorail migration]

### ih...@chromium.org (2016-01-22)

[Empty comment from Monorail migration]

### mg...@chromium.org (2016-01-22)

#14 Flash does its own "Press ESC to exit fullscreen" prompt. We don't interfere or add our own prompt. But I'm not sure how this is relevant since the bug seems to be too go fullscreen and immediately exit. (The prompt is probably shown but only for a fraction of a second.)

### go...@chromium.org (2016-01-25)

Please fix and request a merge to M48 (branch: 2564) before 5:00 PM PST today, If you would like to make it to this this week stable refresh.

### na...@google.com (2016-01-25)

[Empty comment from Monorail migration]

### ih...@chromium.org (2016-01-26)

Sorry, I have no plans to look at this.

### ti...@google.com (2016-01-26)

+ Tim. With no progress in the fix so far, most likely this will miss this week's M48 stable refresh.

### la...@google.com (2016-01-26)

Hey Justin, what are your thoughts on this?

### lg...@chromium.org (2016-01-26)

Based on talking with Justin, this is more of a medium severity. It also only works on OSX.

I've attached a screenshot of what it looks like on Linux (after an initial fullscreen flash): basically a pop-under.

It seems that this goes fullscreen with Flash; going back to Javascript then inherits the fullscreen permission from the Flash gesture. I'm still not completely certain if the `fullscreen` attribute [1] in `openGoogle()` is what does it, but that seems to be the case.

spqchan@: You know more about Mac fullscreen than any of use at this point, I think.
Could you investigate why the `window.open()` receives permission to be fullscreen, and whether Chrome attempts to show a prompt at all?

[1] https://developer.mozilla.org/en-US/docs/Web/API/Window/open

### mg...@chromium.org (2016-01-26)

> I've attached a screenshot of what it looks like on Linux
> (after an initial fullscreen flash): basically a pop-under.

Except that, as per #6, the pop-under has keyboard focus so it can intercept your keystrokes. I think this qualifies as broken on Linux.

### sp...@chromium.org (2016-01-26)

I've been mainly working with the UI work for fullscreen so looking into Web APIs and fullscreen permission is something new for me.

If there are no takers with more experience, I'm willing to investigate this.

### lg...@chromium.org (2016-01-27)

Also removing ReleaseBlock-Stable. I added it at the beginning in the hope that we might be able to target the regular stable release without any additional release or delays, but `ReleaseBlock-Stable` probably wasn't appropriate even if this was high severity.

### an...@gmail.com (2016-01-27)

I have remark, that the problem is not only focused fullscreen on OS X, but also in popup-blocking differences from Flash and from pure javascript. I've deployed http://jabbos.org/swf_test2/, where you can find button, that fires openGoogle, and Flash with the same functionality. 

Take a look at function openGoogle(), I added cycle before window.open. If you click button, only one window will appear and popup blocker will tell about popup windows, but if you click on flash - 4 windows will appear and only after it popup blocker would work. Seems, that behavior might be similar.

### an...@gmail.com (2016-01-27)

In WIndows everything is ok - Flash and javascript allow only one window.

### an...@gmail.com (2016-01-27)

If the user continue to click on page after getting message about popub blocking - new windows will also appear. Possible it is normal behavior.

### an...@gmail.com (2016-02-10)

Hi, any news here? 


### sp...@chromium.org (2016-02-11)

I'm still investigating this.
Unfortunately, progress was going slow since I had several high priority Release-Blocks on my stack and this is something I'm not familiar with.
 
Anyway, I've just fixed all of my Release-Block issues so I can focus more on this.

### sp...@chromium.org (2016-02-23)

I found the reason why it enters fullscreen and opens a new tab.
I'm currently working on a fix that will open a new pop up instead of a new tab.

### an...@gmail.com (2016-02-24)

I also made my own little investigation of this bug. 
In addition to the "new tab problem", I think there is another problem.  

I mean using blink::WebUserGestureIndicator::isProcessingUserGesture(), that returns true after click on page and it's enough for getting full screen from Flash and also running window.open. Seems that, after one action, that required user action (flash full screen, for example),   blink::WebUserGestureIndicator::isProcessingUserGesture() could return false to the next real user action. 

Maybe I'm wrong, please, check it=)

### an...@gmail.com (2016-02-24)

And I also have one more question. Will this bug got CVE id or not?

### an...@gmail.com (2016-02-24)

[Comment Deleted]

### sp...@chromium.org (2016-02-24)

No, you're not wrong. That's actually another part of the problem I've been investigating, and it's most likely why the popup blocker doesn't trigger. 
I'm tackling the "new tab" issue first before I move into that.

As for the CVE id question, I don't know the answer and will leave it to the other devs to answer. 

### sp...@chromium.org (2016-02-26)

+pinkerton so that he can gives us his thoughts on the popup behavior.

I dug around the codebase and it looks like on OSX, we are actively converting popups into new tabs if we're in System Fullscreen. The reason why is because since System Fullscreen occupies its own space on OSX Lion, so the popups would be unaccessible until you exit fullscreen. Here's the issue that's associated with this: https://bugs.chromium.org/p/chromium/issues/detail?id=92570

The reason why the permission bubble never appeared is because when the browser switched to the new tab created by openWindow(...), the tab that contains the flash widget loses "exclusive access". By losing "exclusive access", the flash widget exits fullscreen and the permission bubble is dismissed. This will then leave us in "browser fullscreen" for the new tab.

For a solution, I want to do add an exception for tab content fullscreen, so that the popups will not be converted into new tabs. The "unaccessible popup" problem in https://crbug.com/chromium/92570 should now be fixed in OSX 10.10, so we shouldn't have a problem with opening a popup. What will happen is that the popup will be opened and left behind in the previous Space.

pinkterton, There are a few things I want to address for the behavior:
- Should we focus on the new popup? There's no indication that we opened one (other the popup blocker once we get it to work). If we focus on it, we'll have to switch to the Space the popup occupies in.
- Now that "unaccessible popup" problem is fixed in OSX 10.10, should we only open popups for tab content fullscreen or for System fullscreen on 10.10+? I don't think there were any complaints about the converting it into a new tab so we can probably just do it for tab content fullscreen (Note: Safari converts everything into a new tab if it's in fullscreen. I didn't check what it does for this scenario yet though) 

Aside from opening a popup instead of a new tab, I'm also investigating why the popup blocker isn't working. I have a few ideas why it might be happening, but I will need to go through the codebase a bit more.

### pi...@chromium.org (2016-03-01)

What about 10.9 and the "unaccessible popup" problem? 

### sp...@chromium.org (2016-03-01)

We're still using Immersive Fullscreen for 10.9, so the "unaccessible popup" problem won't happen.
(Note: popup blocker doesn't work on it).

I'm proposing the change for only 10.10+. I think if we're concerned with inconsistency, then perhaps we can stick with opening new tabs for browser fullscreen, and opening popups for tab fullscreen.


### ti...@google.com (2016-03-01)

#35: TL;DR - once the bug is fixed, we'll assess severity and CVE-ID assignment.

Longer version: We only assign CVE-IDs when the reward panel meets, and the reward panel only reviews fixed bugs. 

Once this bug is fixed, it will go to the reward panel. If the panel decides that this bug meets the severity threshold for CVE-ID assignment (on first reading this bug looks like it will, but I'll reserve final comment for the panel), it will be assigned at that point in time (as well as any applicable cash reward based on https://www.google.com/about/appsecurity/chrome-rewards/). There are some exceptions to that process, but they mostly kick in for bugs which aren't fixed within 90 days of reporting or reports involving multiple vendors. 

That said, there's usually no need for a CVE-ID ahead of the publication of our release notes, as the first mention of a Chrome CVE-ID should be our release notes.

### sp...@chromium.org (2016-03-03)

I discussed with pinkerton about the popup today and we decided that for consistency's sake, we'll continue to open the popup as a new tab and feed it to the popup blocker.

### ih...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-31)

spqchan@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### sp...@chromium.org (2016-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### an...@gmail.com (2016-04-21)

Hello! Is there any news here? Can I somehow help in investigations? 

### mm...@chromium.org (2016-05-03)

Any chance to resolve this issue?

### sp...@chromium.org (2016-05-03)

Sorry, I've been OOO and recently got back. Progress is slow, since I have a couple of release blockers to get to first, but I'm currently trying to debug why the behavior is different than Windows

### an...@gmail.com (2016-05-04)

I found one more possible application for this bug in addition to creating fullscreen phishing pages and popunders.  
Because of click it's possible to enter fullscreen and try to install Crhomium extension, for example, openGoogle() look like this: 

function openGoogle() {
		chrome.webstore.install('https://chrome.google.com/webstore/detail/djhgiahomjkabjdodlemhnhbnbfcomam',
        successCallback(), failureCallback());
        }

	function successCallback(){
		alert('ok!');
	}

	function failureCallback(){
		window.onbeforeunload = openGoogle();
	}

And in failure callback it's possible to create fullscreen browlock effect. But it works only in Windows, in OS X I just get hang of Flash plugin. Magic will stop working if user press "ESC", but nobody tells him about that. Please, check this scenario in Windows and OS X.

### sp...@chromium.org (2016-05-24)

Will update the progress on this bug EOD

### sp...@chromium.org (2016-05-25)

Sorry for the late update, I had been swamped. Anyway, I'm able to focus on this again and is debugging the difference in navigation behavior on Windows and OSX 

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### sp...@chromium.org (2016-06-10)

I'm still working on the popup blocker. But in the meantime, I have a fix for the "stuck in fullscreen" behavior in OSX: https://codereview.chromium.org/2053343003/

What was happening was that OSX's fullscreen transition was async, and the call to exit fullscreen after we switched tabs was lost if it occurred during the transition to fullscreen. This puts the browser in an awkward state.

Anyway, once this fix lands, this will behave like Windows.

### bu...@chromium.org (2016-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/104e5ad762f4d2fcf04a33ff8471d77d7b8678bb

commit 104e5ad762f4d2fcf04a33ff8471d77d7b8678bb
Author: spqchan <spqchan@chromium.org>
Date: Mon Jun 13 19:39:06 2016

[Mac] Fix Issue to Exit Fullscreen

Ensure that the browser exits fullscreen if toggleFullscreen was called
during the transition to fullscreen.

BUG=579934

Review-Url: https://codereview.chromium.org/2053343003
Cr-Commit-Position: refs/heads/master@{#399506}

[modify] https://crrev.com/104e5ad762f4d2fcf04a33ff8471d77d7b8678bb/chrome/browser/ui/cocoa/browser_window_controller.h
[modify] https://crrev.com/104e5ad762f4d2fcf04a33ff8471d77d7b8678bb/chrome/browser/ui/cocoa/browser_window_controller_private.mm


### bu...@chromium.org (2016-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/104e5ad762f4d2fcf04a33ff8471d77d7b8678bb

commit 104e5ad762f4d2fcf04a33ff8471d77d7b8678bb
Author: spqchan <spqchan@chromium.org>
Date: Mon Jun 13 19:39:06 2016

[Mac] Fix Issue to Exit Fullscreen

Ensure that the browser exits fullscreen if toggleFullscreen was called
during the transition to fullscreen.

BUG=579934

Review-Url: https://codereview.chromium.org/2053343003
Cr-Commit-Position: refs/heads/master@{#399506}

[modify] https://crrev.com/104e5ad762f4d2fcf04a33ff8471d77d7b8678bb/chrome/browser/ui/cocoa/browser_window_controller.h
[modify] https://crrev.com/104e5ad762f4d2fcf04a33ff8471d77d7b8678bb/chrome/browser/ui/cocoa/browser_window_controller_private.mm


### aw...@chromium.org (2016-07-08)

Hi spqchan@ - what's the ETA on the full fix?  If it's going to be a while migth be worth marking this as fixed so it can start the journey to getting merged and filing a new bug to cover the remaining work?

### sp...@chromium.org (2016-07-08)

Getting the popup blocker to work will take a while. I created https://crbug.com/chromium/626749 to get that part to work and marking this as fixed.

### sh...@chromium.org (2016-07-09)

[Empty comment from Monorail migration]

### an...@gmail.com (2016-07-12)

Hello! 

Glad to know, that bug was fixed!
Any news about CVE for this bug? 

### aw...@chromium.org (2016-07-20)

Congratulations!  The panel has reward $1,000 for this bug.  A member of our finance team will be in touch shortly.

We assign CVEs when release notes go out for the release with this fix, which is likely to be an M52 update.

### an...@gmail.com (2016-07-22)

Hello! Great to know!!! Thank you very much! 

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### an...@gmail.com (2016-09-07)

Hello! 
Any news about CVE-ID? I din't find any information in Google Chrome release notes about this fix. 

### aw...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-09-13)

[Automated comment] Commit may have occurred before M54 branch point (8/25/2016), needs manual review.

### aw...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### bu...@google.com (2016-09-13)

This change was committed long before the M54 branch point on 8/25.  I verified the CL is present in the 2840 branch.  Removing the M54 merge request labels.

### sh...@chromium.org (2016-10-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-02-25)

This issue was migrated from crbug.com/chromium/579934?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Permissions, Internals>Plugins>Flash]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083539)*
