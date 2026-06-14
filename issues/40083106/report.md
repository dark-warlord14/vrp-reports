# Security: Permission bubble runs callbacks on cross-origin pages

| Field | Value |
|-------|-------|
| **Issue ID** | [40083106](https://issues.chromium.org/issues/40083106) |
| **Status** | Accepted |
| **Severity** | Unknown |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature |
| **Reporter** | he...@gmail.com |
| **Created** | 2015-10-30 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability makes it possible to display a cross-origin modal dialog. This way it is possible to ask the victim to do some action on behalf of the website.

**VERSION**  

Chrome Version: [46.0.2490.80 m] + [stable].

**REPRODUCTION CASE**

1. Click on the link: <https://www.google.com/url?sa=t&url=%68%74t%70%3A%2F%2F%57w%57%2EF3RR4M3N745%2ECOM%2F&usg=AFQjCNFd9sop1iEz6lV5aUJ6PI9_sXd_wQ>
2. You should be redirected to the attacker's webpage and then quickly redirected to google.com.
3. After the redirect, a modal dialog should appear on google.com asking you to install the "update".

\* Using a redirect from google.com we can send the victim to the attacker's page where the script will be executed (this is only done to give more credibility to attack). I noticed too that the attack sometimes doesn't work. So you may need to click on the link sometimes.

\* This PoC won't initiate the download (my host server doesn't allow upload of .bat and .exe), but if you want I can send you the full PoC.

\* In case the google link isn't working, you can access the attack on: <http://www.f3rr4m3n745.com>

Here is a video simulating the attack:  

<https://www.youtube.com/watch?v=jp8PMQQyiHs>

## Attachments

- [crbug_549724.html](attachments/crbug_549724.html) (text/html, 499 B)

## Timeline

### me...@chromium.org (2015-10-30)

Attaching the POC for convenience and renaming the bug. This is what's happening:

- The page requests notification and geolocation permissions, which triggers a permission bubble.
- It then redirects to google.com
- The redirect closes the permission bubble, ignoring the permission requests. This in turn runs the callbacks for the permissions, even though the page is now navigated to google.com.

The fix seems to be to check the origin when closing the permission bubble in permission_bubble_request_impl.cc, as the bubble could have been closed by a cross origin navigation. Assigning severity medium, as I think a well crafted permission callback code can do more interesting things with this bug.

@felt, can you PTAL or reassign?

### me...@chromium.org (2015-10-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-30)

[Empty comment from Monorail migration]

### me...@chromium.org (2015-11-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-21)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-12-12)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-03)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 63 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-01-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-24)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 85 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-02-15)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 107 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ra...@chromium.org (2016-02-18)

meacer: this no longer seems to reproduce for me. The page does not navigate until the modal has finished executing. Do you agree? If so can we mark as WontFix?

### he...@gmail.com (2016-02-18)

I tested this on canary and after a few tries it worked. I'm using windows 7.

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 128 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### me...@chromium.org (2016-03-16)

felt: Ping, should we find another owner?

### cl...@chromium.org (2016-04-07)

felt@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-21)

felt: Uh oh! This issue still open and hasn't been updated in the last 173 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-04-26)

tsergeant and benwells are currently looking at bubbles bugs.

### be...@chromium.org (2016-04-27)

I've had a look into this a bit and have some findings:

1. I'm not sure if this is a valid attack. Maybe this is just my naievety, but the script can show one prompt, if lucky (i.e. its racy), and then nothing more. Any script put after the confirm will fail to run.

meacer: do you think this is a valid attack?

2. I'm pretty sure this isn't a bubble related bug, but somewhere deep down in either content or blink, and is to do with how the PermissionManager mojo service is implemented.

I think this because I can see that no 'permission set' callbacks up in the UI layer get called in these cases. However mojo callbacks do get called when the request is destroyed (see https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/permissions/permission_service_impl.cc&l=72). The mojo callback always should be called, but the blink layer (or sumthin) should ignore it in this case.



[Monorail components: -Internals>Permissions]

### he...@gmail.com (2016-04-27)

#21, You are right. I just tested and the code below also shows the modal dialog.

window.onload = function() {
  location.href = "https://www.google.com.br";
}

window.onblur = function() {
  alert(1);
}

And in my opinion this should be considered a valid attack, as the attacker is able to display an arbitrary modal dialog on any webpage. This could lead to some types of phishing attacks.

### me...@chromium.org (2016-04-27)

> 1. I'm not sure if this is a valid attack. Maybe this is just my naievety, but the script can show one prompt, if lucky (i.e. its racy), and then nothing more. Any script put after the confirm will fail to run.

I think there is still a phishing risk here: The attacking page could use prompt() instead and ask for user password over google.com. Other than that, if the attacking page can't run any other code on google.com, then it's at most a low severity bug.

### be...@chromium.org (2016-04-28)

OK ... I not sure if prompting for user / password would work, I don't think the site would get to see any response to the prompt. But the site could definitely put up a message like "You're infected, call Google on XXX-XXX-XXX to fix!"

Note that the prompt now says that it is an embedded site making the request, but most users wouldn't know what that means.

I think this has nothing to do with security UX / permission bubbles, it's something to do with how blink dispatches callbacks.

[Monorail components: -Security>UX Blink>SecurityFeature Security]

### he...@gmail.com (2016-04-28)

#24, About the prompt saying it is an embedded site, if the script is executed on a data url, the following will be displayed "An embedded page on this webpage says".

data:text/html,<html><script src="http://lbherrera.me/script.js"></script></html>

### sh...@chromium.org (2016-05-04)

[Empty comment from Monorail migration]

### be...@chromium.org (2016-05-26)

I only just realised this was assigned to me....

jww - do you know a good owner to assign this to? It is a general blink callback dispatch problem.

### sh...@chromium.org (2016-05-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-02-28)

I bisected this, and it looks like the original report that shows the dialog is fixed by avi's change to suppress dialogs from swapped out frames (https://crbug.com/chromium/634108). The bisect range points to https://chromium.googlesource.com/chromium/src/+log/3ab073a707c7287174539c48829dccdecbb62730..4430f9e5f415d06994bc12ba3fe2a8a46ac80482 with avi's commit 1e870b1.

I further checked if the callback is running on the correct origin, and that seems to be the case (console.log prints the correct origin). That means the modal dialog was the only problem here, and it's fixed, so I think we can close this now. 

luan.herrera@: Please let me know if I'm missing anything.

### he...@gmail.com (2017-05-15)

meacer@: Hey, was looking this up and it's indeed fixed. I also looked at https://crbug.com/chromium/634108 and it seems it's fundamentally the same as this one. It's a shame that I had reported this vulnerability and it didn't get fixed until someone else reported it again 9 months later :(

### ra...@chromium.org (2017-05-15)

+cc awhalley. The bugs do seem similar from a cursory look.

### aw...@chromium.org (2017-05-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-05-22)

The VRP panel noted this was the first report of an issue they awarded for  subsequently, and so should match the reward amount.

### aw...@chromium.org (2017-05-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-06-06)

This issue was migrated from crbug.com/chromium/549724?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Security]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083106)*
