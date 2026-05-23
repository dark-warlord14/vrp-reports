# Security: www.google.fr marked as "secure" with a Microsoft SSL certificate

| Field | Value |
|-------|-------|
| **Issue ID** | [40086717](https://issues.chromium.org/issues/40086717) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Omnibox>SecurityIndicators |
| **Platforms** | Mac, Windows |
| **Reporter** | er...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2017-02-03 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Happened after a redirect to [www.google.fr](http://www.google.fr) from <https://imagine.microsoft.com/fr-FR> (which occured instantly when prompted the first page). The browser declared the page as "secure" although the certificate used was issued to gateway.login.live.com (a Microsoft service).  

If needed, i can send the aformentioned certificate.

**VERSION**  

Chrome Version: Version 56.0.2924.76 (64-bit) stable  

Operating System: Linux 4.9.6-1-ARCH

**REPRODUCTION CASE**  

Extremely rare (occured twice in 2 days of testing) and conditions are still unknown.  

Go to <https://imagine.microsoft.com/fr-FR> and pray for a redirection to google.com or google.fr.

## Attachments

- [chrome_bug_report.png](attachments/chrome_bug_report.png) (image/png, 92.7 KB)
- [net-internals-log (1).json](attachments/net-internals-log (1).json) (text/plain, 1.6 MB)
- [mslog.json](attachments/mslog.json) (text/plain, 1.6 MB)

## Timeline

### es...@chromium.org (2017-02-03)

Thanks for the report. We've received one other report of the same issue but weren't able to get any more information from the reporter.

If you are able to reproduce this, it would be extremely helpful to get a net-internals log as described at https://dev.chromium.org/for-testers/providing-network-details. (I know that may be impossible to get since you can't reproduce on demand, though.)

I'm cc'ing jam and clamy because this feels similar to https://crbug.com/chromium/662267, which I highly suspect was introduced by jam's refactor to move SSLStatus to NavigationHandleImpl and which clamy incidentally fixed (I suspect) in https://codereview.chromium.org/2475693002/.

Maybe there's some path through which a redirected navigation request preserves the SSLStatus from the first hop of the redirect?

[Monorail components: UI>Browser>Omnibox>SecurityIndicators]

### me...@chromium.org (2017-02-07)

[Empty comment from Monorail migration]

### er...@gmail.com (2017-02-07)

I've tried to reproduce the bug unsuccessfully for the past two days.
I am currently trying to get directly in touch with the Microsoft Team to determine what could trigger that redirection.

I'll get back to you as soon as they reply.

### es...@chromium.org (2017-02-10)

We're investigating this but haven't had any luck reproducing yet. OP, do you know how you ended up on www.google.fr from the Microsoft page? Did you click on a link which redirected to Google, or did the page just spontaneously redirect to google, or something else?

### er...@gmail.com (2017-02-10)

It just spontaneously redirected me to google. However i do have some news to this.

1°) You'll find below the answer Microsoft Security Team gave me when i asked for insights about that redirection.
----
Thank you for contacting the Microsoft Security Response Center (MSRC).  Unfortunately, we were unable to reproduce your findings. As such, we have determined that this is not a valid vulnerability. As far we are aware, there are no open redirect issues on this domain. Therefore, this could potentially be an issue with your browser or a malicious attacker.
----
I find the "malicious attacker" issue to be unlikely since it happened on two different PCs with two different OSes (ArchLinux and Windows10) and on different networks.

2°) It seems that waiting a day or two without navigating to imagine.microsoft.com drastically increases chances of that redirection happening.

3°) Thanks to that new info and less than 10 secondes before receiving your email, i managed to capture the net-internals logs. I hope you'll find something useful.

CHROME VERSION  56.0.2924.76  on 4.9.8-1-ARCH

### el...@chromium.org (2017-02-10)

Did you edit that log file using some other tool? It has a bunch of 0x0A octets embedded in it that prevented reloading the file.

A fixed version is attached.

The server definitely appears to be sending the redirect @592077

POST /en-US/Account/FinishSignInUsingRPS?RedirectionToURL=https%3a%2f%2fwww.google.fr%2f&attempt=0&wa=wsignin1.0 HTTP/1.1
Host: imagine.microsoft.com

HTTP_TRANSACTION_READ_RESPONSE_HEADERS
HTTP/1.1 302 Found
Location: https://www.google.fr/


### er...@gmail.com (2017-02-10)

Not at all, but the text editor i used warned me about the file being too large. Maybe it got corrupted when i saved it. Sorry about that.

Nice to learn. If i can be of any more help, i'll be glad to.

### es...@chromium.org (2017-02-10)

Thanks for the log! This is very interesting.

I'm not sure how/why that request to the open redirector https://imagine.microsoft.com/en-US/Account/FinishSignInUsingRPS?RedirectionToURL=https%3a%2f%2fwww.google.fr%2f... is happening, but something funky looks to be happening when following it. We process the 302 redirect, but the request is cancelled before following the redirect. Maybe the Adblock Plus extension is cancelling it. And then another request to https://www.google.fr happens right afterwards, which might be the navigation request that ends up committing. I'm not sure what might be initiating that separate https://www.google.fr request; maybe an extension or maybe there's a retry somewhere that gets triggered when the initial request is cancelled.

In any case, I bet there is a navigation path that gets the two requests mixed up (the cancelled redirect and the separate https://www.google.fr).

I'll try reproducing in a fresh profile with Adblock Plus installed.

### es...@chromium.org (2017-02-11)

OP, would you be willing to share a list of extensions that you have installed?

Braindump since I have to head out in a few minutes:

I can almost sort of kind of reproduce the sequence of events in the netlog by modifying ResourceLoader::FollowDeferredRedirectInternal to call CancelRequest() and return when the redirect URL is https://www.google.com, and then following these steps:

1. When *not* logged into Microsoft, visit https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1486764847&rver=6.6.6577.0&wp=MBI_SSL&wreply=https:%2F%2Fimagine.microsoft.com%2Fen-US%2FAccount%2FFinishSignInUsingRPS%3FRedirectionToURL%3Dhttps%253a%252f%252fwww.google.fr%252f%26attempt%3D0&id=294732

2. Open chrome://net-internals in another tab

3. In the first tab, open DevTools and run the following JS:
f=document.createElement("form"); f.action="https://imagine.microsoft.com/en-US/Account/FinishSignInUsingRPS?RedirectionToURL=https%3a%2f%2fwww.google.com%2f&attempt=0&wa=wsignin1.0"; f.method="POST"; document.body.appendChild(f); f.submit();

The resulting netlog matches the events in https://crbug.com/chromium/688425#c5. Notably, the imagine.microsoft.com request redirects to www.google.com but the request is cancelled before following the redirect, and a subsequent www.google.com request happens afterwards, which looks like it has something to do with a Service Worker (the URL_REQUEST netlog entry contains SERVICE_WORKER_START_REQUEST). But, the certificate behavior doesn't repro -- I'm still ending up on www.google.com with the proper cert -- so there must be some race somewhere that I'm still not hitting.

### ja...@chromium.org (2017-02-12)

Nice debugging. Emily also mentioned in person she suspecteted the bug is with RenderFrameHostImpl::TakeNavigationHandleForCommit. I originally thought it was a bug in NavigationController since I caused several bugs there, but I looked at those codepaths and I don't think they're to blame. So maybe the race is that the old NavigationHandle is still alive when TakeNavigationHandleForCommit is called and it incorrectly uses it. Somehow the old SSLStatus is used.

### er...@gmail.com (2017-02-12)

For my active chrome extensions :

1 - Adblock Plus 1.12.4           (id: cfhdojbkjhnklbpkdaibdccddilifddb)
2 - Ember inspector  2.0.4      (id: bmdblncegkenkacieihfhpjfppoconhi)
3 - Momentum 0.92.2             (id: laookkfknpbbblfpciffpaejjkokdgca)

### es...@chromium.org (2017-02-13)

Addendum to my "repro" in https://crbug.com/chromium/688425#c9: it seems like you have to log in and then log out of login.live.com first for those instructions to work to reproduce the sequence of events in the OP's net log.

(But, I'm not sure this is all that useful, anyway -- I've tried a gazillion ways and can't repro the actual bug using this sequence of steps.)

### ji...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-14)

[Empty comment from Monorail migration]

### es...@chromium.org (2017-02-16)

OP, if you see this happen again, could you please take a screenshot that includes the tab title? Or do you happen to remember if the tab title and favicon was for Google or for Microsoft?

That would help us narrow down what might be going on. Thanks!

### bu...@chromium.org (2017-02-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c32cd2069ae8062b52e5b7b1faf5936bd71a583a

commit c32cd2069ae8062b52e5b7b1faf5936bd71a583a
Author: estark <estark@chromium.org>
Date: Thu Feb 16 08:37:31 2017

Add DumpWithoutCrashing in RendererDidNavigateToExistingPage

This is intended to be reverted after investigating the linked bug.

BUG=688425
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2701523004
Cr-Commit-Position: refs/heads/master@{#450900}

[modify] https://crrev.com/c32cd2069ae8062b52e5b7b1faf5936bd71a583a/content/browser/frame_host/navigation_controller_impl.cc


### er...@gmail.com (2017-02-16)

@est...@chromium.org, related to https://crbug.com/chromium/688425#c16, i can confirm that the favicon and tab title are both correct (favicon is current google logo, and title is 'Google').
The page is totally functional aswell.

The only Microsoft related thing is the certificate as far as i can tell.

### sh...@chromium.org (2017-02-17)

Users experienced this crash on the following builds:

Mac Canary 58.0.3015.0 -  5.11 CPM, 3 reports, 3 clients (signature [Dump without crash] content::`anonymous namespace'::MaybeDumpCopiedNonSameOriginEntry)

If this update was incorrect, please add "Fracas-Wrong" label to prevent future updates.

- Go/Fracas

### sh...@chromium.org (2017-02-17)

Users experienced this crash on the following builds:

Win Canary 58.0.3015.0 -  8.83 CPM, 32 reports, 32 clients (signature [Dump without crash] content::`anonymous namespace'::MaybeDumpCopiedNonSameOriginEntry)
Mac Canary 58.0.3015.0 -  6.59 CPM, 7 reports, 7 clients (signature [Dump without crash] content::`anonymous namespace'::MaybeDumpCopiedNonSameOriginEntry)

If this update was incorrect, please add "Fracas-Wrong" label to prevent future updates.

- Go/Fracas

### sh...@chromium.org (2017-02-18)

This crash has high impact on Chrome's stability.
Signature: [Dump without crash] content::`anonymous namespace'::MaybeDumpCopiedNonSameOriginEntry.
Channel: canary. Platform: win.
Labeling https://crbug.com/chromium/688425 with ReleaseBlock-Dev.


If this update was incorrect, please add "Fracas-Wrong" label to prevent future updates.

- Go/Fracas

### es...@chromium.org (2017-02-18)

Removing ReleaseBlock label, the crash is a DumpWithoutCrashing that we added to gather more data.

### bu...@chromium.org (2017-02-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b1730dabdf125160dc23db993e08f453fc648fc8

commit b1730dabdf125160dc23db993e08f453fc648fc8
Author: estark <estark@chromium.org>
Date: Sun Feb 19 00:06:26 2017

Use ScopedCrashKey for RendererDidNavigate crash dumps

This will make the crash reports easier to view.

BUG=688425
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2696193006
Cr-Commit-Position: refs/heads/master@{#451501}

[modify] https://crrev.com/b1730dabdf125160dc23db993e08f453fc648fc8/chrome/app/chrome_crash_reporter_client_win.cc
[modify] https://crrev.com/b1730dabdf125160dc23db993e08f453fc648fc8/chrome/common/crash_keys.cc
[modify] https://crrev.com/b1730dabdf125160dc23db993e08f453fc648fc8/content/browser/frame_host/navigation_controller_impl.cc


### ja...@chromium.org (2017-02-19)

@erasmus425: can you try using Canary channel to reproduce this? And please enable crash/error reporting. @estark added logging and it would be great if we can confirm where the error is. Thanks.

### er...@gmail.com (2017-02-20)

I might be mistaken, but i'm reading everywhere that the canary version isn't available to the Linux platform. Do you have any solution ?

Since my main computer is on Linux, it might take a while before i can reproduce this bug in a Windows environment.

### es...@chromium.org (2017-02-21)

[Empty comment from Monorail migration]

### ja...@chromium.org (2017-02-21)

@eramus425: ah you're right, I didn't notice you're on Linux.

Regardless, Emily seems to have tracked this down to the code path.

For Googlers reading this, per Maria here's a convenient link to look at all the crash reports that came with the debugging info Emily added:
https://crash.corp.google.com/dremel_query_ui?q=select%20reportid%2C%20productdata.key%2C%20productdata.value%0AFROM%20crash.prod.latest%0AWHERE%20product.name%3D%27Chrome%27%20AND%20ProductData.key%20LIKE%20%27navigation_controller_impl_renderer_did_navigate-%25%27%0AORDER%20BY%201%2C%202

This shows all the crash keys in one table. The main takeways are:
-RendererDidNavigateToNewPage is not involved
-all of the reports are from RendererDidNavigateToExistingPage
-there are no in_page hits

### bu...@chromium.org (2017-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7e735c119621aadf893858adb6c37b58325d5e94

commit 7e735c119621aadf893858adb6c37b58325d5e94
Author: jam <jam@chromium.org>
Date: Tue Feb 21 21:18:54 2017

Revert of Use ScopedCrashKey for RendererDidNavigate crash dumps (patchset #4 id:60001 of https://codereview.chromium.org/2696193006/ )

Reason for revert:
We got the data we wanted.

Original issue's description:
> Use ScopedCrashKey for RendererDidNavigate crash dumps
>
> This will make the crash reports easier to view.
>
> BUG=688425
> CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation
>
> Review-Url: https://codereview.chromium.org/2696193006
> Cr-Commit-Position: refs/heads/master@{#451501}
> Committed: https://chromium.googlesource.com/chromium/src/+/b1730dabdf125160dc23db993e08f453fc648fc8

TBR=creis@chromium.org,rsesek@chromium.org,ananta@chromium.org,estark@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=688425

Review-Url: https://codereview.chromium.org/2705303002
Cr-Commit-Position: refs/heads/master@{#451834}

[modify] https://crrev.com/7e735c119621aadf893858adb6c37b58325d5e94/chrome/app/chrome_crash_reporter_client_win.cc
[modify] https://crrev.com/7e735c119621aadf893858adb6c37b58325d5e94/chrome/common/crash_keys.cc
[modify] https://crrev.com/7e735c119621aadf893858adb6c37b58325d5e94/content/browser/frame_host/navigation_controller_impl.cc


### ke...@chromium.org (2017-02-21)

It seems like estark@ is making good progress on this, please re-assign if you aren't the right owner.

### es...@chromium.org (2017-02-21)

jam@'s got a fix coming soon.

### bu...@chromium.org (2017-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c5608a34fd0112511e9165179a91cdd9277518b2

commit c5608a34fd0112511e9165179a91cdd9277518b2
Author: jam <jam@chromium.org>
Date: Wed Feb 22 09:49:13 2017

Revert of Add DumpWithoutCrashing in RendererDidNavigateToExistingPage (patchset #3 id:40001 of https://codereview.chromium.org/2701523004/ )

Reason for revert:
We got the data we wanted.

Original issue's description:
> Add DumpWithoutCrashing in RendererDidNavigateToExistingPage
>
> This is intended to be reverted after investigating the linked bug.
>
> BUG=688425
> CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation
>
> Review-Url: https://codereview.chromium.org/2701523004
> Cr-Commit-Position: refs/heads/master@{#450900}
> Committed: https://chromium.googlesource.com/chromium/src/+/c32cd2069ae8062b52e5b7b1faf5936bd71a583a

TBR=nasko@chromium.org,estark@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=688425

Review-Url: https://codereview.chromium.org/2711533002
Cr-Commit-Position: refs/heads/master@{#451960}

[modify] https://crrev.com/c5608a34fd0112511e9165179a91cdd9277518b2/content/browser/frame_host/navigation_controller_impl.cc


### bu...@chromium.org (2017-02-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a78746ec1a1bfa668f5bcb01d2b2665d2c514369

commit a78746ec1a1bfa668f5bcb01d2b2665d2c514369
Author: jam <jam@chromium.org>
Date: Wed Feb 22 17:21:57 2017

Fix SSL certificate being wrong in the intended_as_new_entry fase of NAVIGATION_TYPE_EXISTING_PAGE.

It turns out that in some rare race conditions, this section of the code could get reached with a different origin for the committed page and the NavigationEntry that was reused. In that case, make sure to use the SSL certificate from the NavigationHandle instead of resusing the old one.

BUG=688425
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2707133003
Cr-Commit-Position: refs/heads/master@{#452106}

[modify] https://crrev.com/a78746ec1a1bfa668f5bcb01d2b2665d2c514369/content/browser/frame_host/navigation_controller_impl.cc


### ja...@chromium.org (2017-02-22)

Tomorrow I can merge 452106 to 57 

### sh...@chromium.org (2017-02-23)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-02-23)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-02-23)

+awhalley@ for M57 merge review.

### aw...@chromium.org (2017-02-23)

govind@ - this will be good for M57 tomorrow after some more time in canary.

jam@ - thanks for the investigation and fix!

### go...@chromium.org (2017-02-23)

Thank you  awhalley@. Please update after Canary baking. If all looks good, I will approve the merge. Thank you.

### ja...@chromium.org (2017-02-23)

Thanks, will check in tomorrow.

Emily tracked this down; the fix is trivial after she localized it :)

### sh...@chromium.org (2017-02-24)

[Empty comment from Monorail migration]

### ja...@chromium.org (2017-02-24)

@awhalley @govind
ok to merge?

### go...@chromium.org (2017-02-24)

Approving merge to M57 branch 2987 after discussing with awhalley@. Please merge ASAP. Thank you.

### bu...@chromium.org (2017-02-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d37f8f3c85e4c2f6c5d040478f5067969f278650

commit d37f8f3c85e4c2f6c5d040478f5067969f278650
Author: John Abd-El-Malek <jam@chromium.org>
Date: Fri Feb 24 19:20:11 2017

Fix SSL certificate being wrong in the intended_as_new_entry case of NAVIGATION_TYPE_EXISTING_PAGE.

It turns out that in some rare race conditions, this section of the code could get reached with a different origin for the committed page and the NavigationEntry that was reused. In that case, make sure to use the SSL certificate from the NavigationHandle instead of resusing the old one.

BUG=688425
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2707133003
Cr-Commit-Position: refs/heads/master@{#452106}
(cherry picked from commit a78746ec1a1bfa668f5bcb01d2b2665d2c514369)

Review-Url: https://codereview.chromium.org/2719573002 .
Cr-Commit-Position: refs/branch-heads/2987@{#680}
Cr-Branched-From: ad51088c0e8776e8dcd963dbe752c4035ba6dab6-refs/heads/master@{#444943}

[modify] https://crrev.com/d37f8f3c85e4c2f6c5d040478f5067969f278650/content/browser/frame_host/navigation_controller_impl.cc


### aw...@chromium.org (2017-02-28)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/43f7ab4d121be7ad05f31728ccc130d500232031

commit 43f7ab4d121be7ad05f31728ccc130d500232031
Author: nasko <nasko@chromium.org>
Date: Wed Mar 01 21:47:48 2017

Change CHECK into DCHECK.

Code in the browser process should not be doing a CHECK based on data
coming from the renderer process, as this allows a compromised renderer
to trivially kill the whole browser.

BUG=688425
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation

Review-Url: https://codereview.chromium.org/2721393002
Cr-Commit-Position: refs/heads/master@{#454047}

[modify] https://crrev.com/43f7ab4d121be7ad05f31728ccc130d500232031/content/browser/frame_host/navigation_controller_impl.cc


### bu...@chromium.org (2017-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/494a3b618ecf62e96f14c195a0d2234b20db785c

commit 494a3b618ecf62e96f14c195a0d2234b20db785c
Author: jam <jam@chromium.org>
Date: Wed Mar 01 22:07:16 2017

Revert of Change CHECK into DCHECK. (patchset #1 id:1 of https://codereview.chromium.org/2721393002/ )

Reason for revert:
(per discussion, I was using this to get a signal. I'll send a cl to fix)

Original issue's description:
> Change CHECK into DCHECK.
>
> Code in the browser process should not be doing a CHECK based on data
> coming from the renderer process, as this allows a compromised renderer
> to trivially kill the whole browser.
>
> BUG=688425
> CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation
>
> Review-Url: https://codereview.chromium.org/2721393002
> Cr-Commit-Position: refs/heads/master@{#454047}
> Committed: https://chromium.googlesource.com/chromium/src/+/43f7ab4d121be7ad05f31728ccc130d500232031

TBR=creis@chromium.org,nasko@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=688425

Review-Url: https://codereview.chromium.org/2729613003
Cr-Commit-Position: refs/heads/master@{#454058}

[modify] https://crrev.com/494a3b618ecf62e96f14c195a0d2234b20db785c/content/browser/frame_host/navigation_controller_impl.cc


### bu...@chromium.org (2017-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/494a3b618ecf62e96f14c195a0d2234b20db785c

commit 494a3b618ecf62e96f14c195a0d2234b20db785c
Author: jam <jam@chromium.org>
Date: Wed Mar 01 22:07:16 2017

Revert of Change CHECK into DCHECK. (patchset #1 id:1 of https://codereview.chromium.org/2721393002/ )

Reason for revert:
(per discussion, I was using this to get a signal. I'll send a cl to fix)

Original issue's description:
> Change CHECK into DCHECK.
>
> Code in the browser process should not be doing a CHECK based on data
> coming from the renderer process, as this allows a compromised renderer
> to trivially kill the whole browser.
>
> BUG=688425
> CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation
>
> Review-Url: https://codereview.chromium.org/2721393002
> Cr-Commit-Position: refs/heads/master@{#454047}
> Committed: https://chromium.googlesource.com/chromium/src/+/43f7ab4d121be7ad05f31728ccc130d500232031

TBR=creis@chromium.org,nasko@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=688425

Review-Url: https://codereview.chromium.org/2729613003
Cr-Commit-Position: refs/heads/master@{#454058}

[modify] https://crrev.com/494a3b618ecf62e96f14c195a0d2234b20db785c/content/browser/frame_host/navigation_controller_impl.cc


### bu...@chromium.org (2017-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/494a3b618ecf62e96f14c195a0d2234b20db785c

commit 494a3b618ecf62e96f14c195a0d2234b20db785c
Author: jam <jam@chromium.org>
Date: Wed Mar 01 22:07:16 2017

Revert of Change CHECK into DCHECK. (patchset #1 id:1 of https://codereview.chromium.org/2721393002/ )

Reason for revert:
(per discussion, I was using this to get a signal. I'll send a cl to fix)

Original issue's description:
> Change CHECK into DCHECK.
>
> Code in the browser process should not be doing a CHECK based on data
> coming from the renderer process, as this allows a compromised renderer
> to trivially kill the whole browser.
>
> BUG=688425
> CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_site_isolation
>
> Review-Url: https://codereview.chromium.org/2721393002
> Cr-Commit-Position: refs/heads/master@{#454047}
> Committed: https://chromium.googlesource.com/chromium/src/+/43f7ab4d121be7ad05f31728ccc130d500232031

TBR=creis@chromium.org,nasko@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=688425

Review-Url: https://codereview.chromium.org/2729613003
Cr-Commit-Position: refs/heads/master@{#454058}

[modify] https://crrev.com/494a3b618ecf62e96f14c195a0d2234b20db785c/content/browser/frame_host/navigation_controller_impl.cc


### aw...@chromium.org (2017-03-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-05)

Congratulations! The panel decided to award $3,000 for this!  A member of our finance team will be in touch to arrange payment.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### er...@gmail.com (2017-03-13)

I did not know that would fit in the Google reward Bounty program, that's awesome !
Would it be possible to give a part to charity ?
To whom shall i address for it ?

### aw...@chromium.org (2017-03-13)

erasmus425@ - great to hear!  I've followed up in email.

### sh...@chromium.org (2017-06-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-06-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/688425?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/694184]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086717)*
