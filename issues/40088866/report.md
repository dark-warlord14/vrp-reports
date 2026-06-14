# Issuing multiple redirects hangs any subsequent navigation. This allows URL Spoofing and also a crash.

| Field | Value |
|-------|-------|
| **Issue ID** | [40088866](https://issues.chromium.org/issues/40088866) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2017-08-29 |
| **Bounty** | $500.00 |

## Description

Redirecting the user multiple times in a loop causes any subsequent navigation to hang (in the PoC I used a website that returns a 204 status response code, but I think an arbitrary website can also be used to achieve the same purpose). This allows the URL to be spoofed. I also noted that the same PoC triggers a crash if the user tries to interact with the console while the URL is hanging.

VERSION
I tested on:
61.0.3163.59
62.0.3199.0

REPRODUCTION CASE
1. Access https://lbherrera.github.io/lab/204spoof.html
2. Navigate to any website using the omnibox.
3. Restart the browser.
4. Access https://lbherrera.github.io/lab/204spoof.html
5. Navigate to any website using the omnibox.

* Steps 1 to 3 should only be needed one time. After this, any attempt to spoof the omnibox should work by just following steps 4 and 5.

If you want to crash the browser, you must:
1. Access https://lbherrera.github.io/lab/204spoof.html
2. Open the console.
3. Navigate to any website using the omnibox.
4. Type anything in the console.

Here is a video demonstrating the attack and the crash:
https://www.youtube.com/watch?v=y5xwMnWWxTQ

## Attachments

- [Screen Shot 2017-08-29 at 16.11.45.png](attachments/Screen Shot 2017-08-29 at 16.11.45.png) (image/png, 149.8 KB)

## Timeline

### do...@chromium.org (2017-08-29)

Thanks for the report. The navigation is clearly still in progress (as indicated by the spinning tab indicator that the user can see). As per https://dev.chromium.org/Home/chromium-security/security-faq#TOC-Where-are-the-security-indicators-located-in-the-browser-window- , we don't guarantee the omnibox as a security indicator until navigation is fully complete. So this isn't quite a URL spoof.

+cc avi who is working on beforeunload handlers in general. This might be a duplicate of https://crbug.com/chromium/756803?

[Monorail components: UI>Browser>Navigation]

### do...@chromium.org (2017-08-29)

I'll also note that I don't see the spoof on Mac Canary - it briefly flashes the typed in address before reverting back to the origin address (see screenshot with the spinning tab indicator showing the loading).

My Canary has BrowserSideNavigation enabled which might play a factor in eliminating the spoof entirely. +clamy for thoughts.

### cr...@chromium.org (2017-08-30)

I was able to repro the spoof on Windows with BrowserSideNavigation:Enabled (with just steps 1 and 2), so PlzNavigate doesn't seem to prevent it.  That's surprising to me-- PlzNavigate is not supposed to let a renderer-initiated navigation (like the generate_204 one here) cancel a browser-initiated navigation.  Also, the spoofed URL goes away if you switch to another tab and come back, which means we're actually canceling the navigation but not updating the address bar (which is a problem in itself).

clamy@, could this be an issue with your recent r495139 CL from https://crbug.com/chromium/755507?  That was meant to allow cancellation of renderer-initiated navigations (even those with a user gesture), but not browser-initiated ones.

For context, the spoof itself has overlap with https://crbug.com/chromium/719856 (WontFix), where the user's navigation never completes due to actions from the underlying page, and we leave a user-typed URL in the address bar.  This bug may be slightly worse in that it's interrupting the user's self-chosen navigation and not requiring a weird port to be slow, but it's still mitigated by the spinner and lack of green lock icon.  I also think we should be able to fix it in PlzNavigate, if my guess above is correct.

As for the crash, here's an example report: a98dd07bb865adac.  That's content::RenderFrameDevToolsAgentHost::DidFinishNavigation, so it might be something dgozman@ can help triage.  (Maybe it has some similarity to 580e9a98ff27e38e from https://crbug.com/chromium/756120?)


Summary:
1) PlzNavigate should probably prevent the 204 navigation from canceling the user's navigation.
2) We should probably update the omnibox in cases like this where the cancellation does occur.
3) There's a DevTools crash to fix.

[Monorail components: Platform>Apps>DevTools]

### do...@chromium.org (2017-08-30)

creis@: Thanks for the investigation! I'm assigning this a Medium severity for now based on the mitigating factors and the presence of the devtools crash.

### sh...@chromium.org (2017-08-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-09-08)

Ok so on trunk on Linux, I can't reproduce the URL with or without PlzNavigate. The difference is without PlzNavigate the browser-initiated nav completes whereas with PlzNavigate it doesn't - which is clearly not what we want. I will investigate some more.

### cl...@chromium.org (2017-09-08)

Ok so the issue on PlzNavigate is not related to r495139 but to the short amount of time we need to commit the browser-initiated nav. What happens is the following:
- we start a browser-initiated nav.
- while it's ongoing on the browser process the renderer-initiated non user-initiated navs cannot cancel it and cannot start.
- it reaches the point where it's ready to commit and it is sent to the speculative RFH for commit.
- a non-user initiated nav arrives. Since we no longer have a NavigationRequest it can start. At that point we clean up the speculative RFH which has not committed yet.
- the browser-initiated nav is cancelled.

To solve the issue, I can two options:
1) don't clean up a speculative RFH that is about to commit when the new navigation is not user-initiated.
2) when checking if a non-user initiated navigation can start, also check if we don't have a Navigationhandle for a browser initiated nav in the current and speculative RFHs and don't start in that case.

Personally, I'd be more in favor of two, since it doesn't require fiddling with the RFH clean up. Wdyt?

### sh...@chromium.org (2017-09-23)

clamy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-10-07)

clamy: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2017-10-09)

creis: Is there anything we can do to move this forward while clamy@ is away?

dgozman: can you comment on the devtools crash?

### dg...@chromium.org (2017-10-09)

I suspect the devtools-related crash to be the same as https://crbug.com/chromium/742955. Does it repro on ToT?

### sh...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-10-24)

I can't get the crash to repro on ToT, so it looks like that is sorted now.

creis/clamy: friendly ping on this one. I don't have a windows machine handy to see if the original spoof problem still exists.

### cl...@chromium.org (2017-10-24)

I don't have a windows machine either so I can't comment on the spoof. The race condition that leads to the non-user initiated navigation not being cancelled is something we're looking to fix along with other races happening during navigation.

### mm...@chromium.org (2017-11-14)

Ping from security sheriff. Any update here?

Do we still need to test this on Windows?

### pa...@chromium.org (2017-12-04)

Per https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md#High-severity, this is a High ("Complete control over the apparent origin in the omnibox").

It is not limited to Windows; I reproduced the spoof on Linux just now. It does not repro on iOS though.

I can't reproduce the browser crash by typing into the console, though.

### pa...@chromium.org (2017-12-04)

This also means that we have exceeded our 60-day fix promise.

### pa...@chromium.org (2017-12-04)

awhalley has confirmed the spoof on macOS on Canary, btw.

### pa...@chromium.org (2017-12-04)

And on Android on Canary (but not Beta or Stable; the Omnibox shows the attack page URL on those versions).

### cl...@chromium.org (2017-12-05)

I can reproduce in a flaky manner on Linux. I'm looking at it.

### sh...@chromium.org (2017-12-05)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2017-12-05)

I have a browser test for the issue at https://chromium-review.googlesource.com/c/chromium/src/+/808924. I think I have the gist of it. For this to happen, a renderer process needs to do constant location.assign to cross-document URL (and they shouldn't actually succeed). This will eventually allow the spoof of a browser-intiated cross-site nav in the following manner:
1) While the cross-site navigation is ongoing, the renderer-initiated navs are dropped (since they're not user-initiated).
2) Once the browser-initiated nav is ready to commit, we send it to the speculative RFH for commit.
3) A renderer-initiated nav comes in. It is now accepted, and the speculative RFH gets deleted. This should update the visible URL, but it doesn't. -> This is the issue in this sequence.
4) The renderer must continue issuing renderer-initiated navs that never succeeds. Otherwise we do update the visible URL properly (see in the test, the last EXPECT for the Visible URL is true).

So the problem here is we don't update the visible URL when a speculative RFH that is pending commit gets deleted. I suspect we should check if it has a NavigationHandle, and if so, delete the pending NavigationEntry that corresponds to it.

### cl...@chromium.org (2017-12-05)

So that was indeed the issue. I have a fix for it at https://chromium-review.googlesource.com/c/chromium/src/+/808924.

### cr...@chromium.org (2017-12-06)

palmer@: I'm unclear why this was changed to High severity in https://crbug.com/chromium/760342#c16.  That would be true for an unrestricted URL spoof, but this has several mitigating factors mentioned in comments 1 and 3:

1) The attacker can't choose the victim URL.  The user has to type a new URL themselves, which means the attacker has a harder time showing a convincing spoof, and that user interaction is required.

2) Chrome is still showing that the page hasn't committed, since the spinner is still going and the lock icon isn't displayed.

I would normally treat those as sufficient mitigations to consider this a Medium.  Is that incorrect?

### bu...@chromium.org (2017-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/372343377dfdc9736630ba80887bab27e047f4e6

commit 372343377dfdc9736630ba80887bab27e047f4e6
Author: clamy <clamy@chromium.org>
Date: Wed Dec 06 22:45:07 2017

Fix for URL spoof caused by deletion of speculative RFH

This CL fixes a security issue where a website could succeed in spoofing the
URL of a cross-process navigation by issuing an endless loop of JavaScript
navigations. When the cross-site navigation was ready to commit, a
renderer-initiated navigation would start, causing the deletion of the
speculative RenderFrameHost. However, we would not update the visible URL for
the tab, even though the load of the cross-site navigation had stopped (due to
the deletion of the speculative RFH). This CL ensures that the pending
NavigationEntry is deleted in that case.

BUG=760342

Change-Id: Ie24beda484ebd6daca5feb17f74da921eac80ce9
Reviewed-on: https://chromium-review.googlesource.com/808924
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#522231}
[modify] https://crrev.com/372343377dfdc9736630ba80887bab27e047f4e6/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/372343377dfdc9736630ba80887bab27e047f4e6/content/browser/frame_host/render_frame_host_manager_browsertest.cc


### do...@chromium.org (2017-12-06)

+cc palmer for visibility: just reiterating the question in c#24 for the escalation in severity. When this bug was initially triaged the mitigating factors reduced the severity. Was there a change in the factors?

### pa...@chromium.org (2017-12-06)

Hmm, yeah, I think #24 is right. Sorry about that, everyone.

And thanks clamy! :)

### cl...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-07)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-14)

Thanks for the report! The VRP panel looked at this and decided to award $500, a lower amount due to the amount of user interaction required. Cheers!

### aw...@chromium.org (2017-12-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

This bug requires manual review: M64 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-12-18)

abdulsyed@ - good for M64

### ab...@chromium.org (2017-12-19)

Approving merge for M64. Branch:3282

### cl...@chromium.org (2017-12-19)

I would prefer if we waited before merging this. It might be related to crashes on M65, so we should investigate the crashes first.

### ab...@google.com (2018-01-03)

sounds good. Can you please confirm if crashes are related?

### cl...@chromium.org (2018-01-03)

Yes they are. I'm looking at a fix for the issue.

### cm...@chromium.org (2018-01-05)

Please merge the approved cl(s) to M64 release branch 3282 as soon as possible.

### cm...@google.com (2018-01-10)

Another ping!

### bu...@chromium.org (2018-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5cd363bc34f508c63b66e653bc41bd1783a4b711

commit 5cd363bc34f508c63b66e653bc41bd1783a4b711
Author: clamy <clamy@chromium.org>
Date: Thu Jan 11 13:12:44 2018

Fix issue with pending NavigationEntry being discarded incorrectly

This CL fixes an issue where we would attempt to discard a pending
NavigationEntry when a cross-process navigation to this NavigationEntry
is interrupted by another navigation to the same NavigationEntry.

BUG=760342,797656,796135

Change-Id: I204deff1efd4d572dd2e0b20e492592d48d787d9
Reviewed-on: https://chromium-review.googlesource.com/850877
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Camille Lamy <clamy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#528611}
[modify] https://crrev.com/5cd363bc34f508c63b66e653bc41bd1783a4b711/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/5cd363bc34f508c63b66e653bc41bd1783a4b711/content/browser/frame_host/render_frame_host_manager_browsertest.cc


### cl...@chromium.org (2018-01-11)

@cmasso: I was waiting for the CL at 43 to land since it fixes a crash that can occur because of CL 25. I can't merge CL 25 without the second CL. Should I wait for the second CL to have at least a day on Canary?

### cm...@google.com (2018-01-11)

Yes please.

### cm...@google.com (2018-01-12)

Please verify

### cl...@chromium.org (2018-01-15)

There's still a crash following the fix (https://crash.corp.google.com/browse?q=custom_data.ChromeCrashProto.magic_signature_1.name%3D%27content%3A%3ANavigationControllerImpl%3A%3ADiscardPendingEntry%27%20AND%20product.name%3D%27Chrome%27%20AND%20product.Version%3D%2765.0.3321.0%27&sql_dialect=googlesql&ignore_case=false&enable_rewrite=true&omit_field_name=&omit_field_value=&omit_field_opt=%3D&stbtiq=&reportid=&index=0#4). I see why it's happening, will work on another fix.

### cl...@chromium.org (2018-01-16)

I have a fix for it at https://chromium-review.googlesource.com/c/chromium/src/+/867030.

### cm...@chromium.org (2018-01-17)

Please land the new fix and verify in the next canary

### cl...@chromium.org (2018-01-18)

The fix landed in https://crbug.com/chromium/796135.

### cm...@chromium.org (2018-01-18)

The merge was approved already. Are you planning to merge this?

### cl...@chromium.org (2018-01-19)

Yes, I've confirmed that we are not seeing any crashes in the last canary.

### bu...@chromium.org (2018-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9efc6345d59766bd88e72123b12dd154e051161e

commit 9efc6345d59766bd88e72123b12dd154e051161e
Author: clamy <clamy@chromium.org>
Date: Fri Jan 19 15:43:34 2018

Fix for URL spoof caused by deletion of speculative RFH

This CL fixes a security issue where a website could succeed in spoofing the
URL of a cross-process navigation by issuing an endless loop of JavaScript
navigations. When the cross-site navigation was ready to commit, a
renderer-initiated navigation would start, causing the deletion of the
speculative RenderFrameHost. However, we would not update the visible URL for
the tab, even though the load of the cross-site navigation had stopped (due to
the deletion of the speculative RFH). This CL ensures that the pending
NavigationEntry is deleted in that case.

BUG=760342

Change-Id: Ie24beda484ebd6daca5feb17f74da921eac80ce9
Reviewed-on: https://chromium-review.googlesource.com/808924
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#522231}(cherry picked from commit 372343377dfdc9736630ba80887bab27e047f4e6)
Reviewed-on: https://chromium-review.googlesource.com/876342
Reviewed-by: Camille Lamy <clamy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3282@{#547}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/9efc6345d59766bd88e72123b12dd154e051161e/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/9efc6345d59766bd88e72123b12dd154e051161e/content/browser/frame_host/render_frame_host_manager_browsertest.cc


### bu...@chromium.org (2018-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a75ca76a3d13ba91d94a73bbf7fc04ffdd722a8c

commit a75ca76a3d13ba91d94a73bbf7fc04ffdd722a8c
Author: clamy <clamy@chromium.org>
Date: Fri Jan 19 15:46:20 2018

Fix issue with pending NavigationEntry being discarded incorrectly

This CL fixes an issue where we would attempt to discard a pending
NavigationEntry when a cross-process navigation to this NavigationEntry
is interrupted by another navigation to the same NavigationEntry.

BUG=760342,797656,796135

Change-Id: I204deff1efd4d572dd2e0b20e492592d48d787d9
Reviewed-on: https://chromium-review.googlesource.com/850877
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Camille Lamy <clamy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#528611}(cherry picked from commit 5cd363bc34f508c63b66e653bc41bd1783a4b711)
Reviewed-on: https://chromium-review.googlesource.com/875944
Reviewed-by: Camille Lamy <clamy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3282@{#548}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/a75ca76a3d13ba91d94a73bbf7fc04ffdd722a8c/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/a75ca76a3d13ba91d94a73bbf7fc04ffdd722a8c/content/browser/frame_host/render_frame_host_manager_browsertest.cc


### bu...@chromium.org (2018-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5fbda71f8804ad8abbc0da3112b77eadf16be944

commit 5fbda71f8804ad8abbc0da3112b77eadf16be944
Author: clamy <clamy@chromium.org>
Date: Fri Jan 19 15:49:16 2018

Fix issue with pending NavigationEntry being wrongly deleted

This CL makes sure we don't delete the pending NavigationEntry when
RenderFrameHostManager::GetFrameHostForNavigation is called following a
call to NavigationController::NavigateToEntry.

BUG=796135,760342

Change-Id: I492d7a74f9eec8d81fd6cbac6dca6d61fe1dcc81
Reviewed-on: https://chromium-review.googlesource.com/867030
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#529954}(cherry picked from commit 4820ab1967e126c20c98e00606ee4648f071f62f)
Reviewed-on: https://chromium-review.googlesource.com/876362
Reviewed-by: Camille Lamy <clamy@chromium.org>
Cr-Commit-Position: refs/branch-heads/3282@{#549}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/5fbda71f8804ad8abbc0da3112b77eadf16be944/content/browser/frame_host/render_frame_host_manager.cc


### cl...@chromium.org (2018-01-19)

All CLs have been merged to 64, this should be good.

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/760342?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088866)*
