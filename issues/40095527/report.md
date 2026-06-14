# Security: URL bar spoofing via download redirect

| Field | Value |
|-------|-------|
| **Issue ID** | [40095527](https://issues.chromium.org/issues/40095527) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Downloads, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2019-06-28 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 77.0.3836.3 canary  

Operating System: Android

**REPRODUCTION CASE**

1. Go to <https://shhnjk.azurewebsites.net/download_redirector.php?url=https://www.google.com:1234>

Observed Results: Observe that google.com:1234 displayed but the content area still shows <https://shhnjk.azurewebsites.net/> contents.

- The content area is interactive, so the user can enter enter data.

## Attachments

- [976549F7-B41B-4D28-B841-462FC3D5D14C.MP4](attachments/976549F7-B41B-4D28-B841-462FC3D5D14C.MP4) (video/mp4, 1.4 MB)

## Timeline

### ch...@gmail.com (2019-06-28)

[Empty comment from Monorail migration]

### jd...@chromium.org (2019-06-28)

Thanks for the report!

tommycli@: can you take a look at this? This can repro on Desktop too, if you load the page and then open devtools. Feel free to re-assign to someone you think is more appropriate, especially if it's better for the navigation folks.

(I'm giving this severity-high because it's arbitrary domain in omnibox, and I don't consider the port number to be very mitigating.)

[Monorail components: UI>Browser>Omnibox]

### ch...@gmail.com (2019-06-28)

To repro on Desktop:

1. Go to https://shhnjk.azurewebsites.net/download_redirector.php?url=https://www.google.com:1234
2. Double-click on the URL (https://shhnjk.az….) 

or

2. Open devtools

- google.com:1234 loads after a few minutes, but on Android, when I tapped on “WhoIam” link, google.com:1234 is in URL forever. It never finished loading even after waiting for like more than 5mins.



### ch...@gmail.com (2019-07-02)

Can someone please Cc ahemery@ per https://bugs.chromium.org/p/chromium/issues/detail?id=979441#c2

### sh...@chromium.org (2019-07-12)

tommycli: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2019-07-23)

Friendly ping - any update on this bug? Thanks!

### sh...@chromium.org (2019-07-27)

tommycli: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2019-07-29)

jochen: I just bisected this and landed on this CL: https://chromium-review.googlesource.com/c/chromium/src/+/1138081

Does this look right?

It seems like when the page starts a download that times out, the URL returned by NavigationController::GetVisibleEntry() is updated to the cross-origin download URL.

I'm compiling locally to try to confirm my suspicions above, but please take a look too.

### to...@chromium.org (2019-07-29)

I was able to confirm (by adding a printf to ChromeLocationBarModelDelegate::GetURL), than NavigationController::GetVisibleEntry() returns the DOWNLOAD URL instead of the page content URL while the download is starting up in the above linked example.

NavigationController::GetVisibleEntry() should always return the URL corresponding to the page content to avoid spoofing.

Sending this off to the Download / Navigation owners.

dtrainor: Do you mind assigning this to someone, since jochen@chromium.org is OOO?

[Monorail components: -UI>Browser>Omnibox UI>Browser>Downloads UI>Browser>Navigation]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-08-07)

dtrainor@ Friendly ping.

### jd...@chromium.org (2019-08-19)

dtrainor@: can you help us route this?

I'm also adding qinmin@ for visibility.

### dt...@chromium.org (2019-08-19)

Min can you take a look?  Thank you for the pings!

### qi...@chromium.org (2019-08-19)

When the page loads, the javascript automatically clicks on the download link to perform a redirect.  And that should change the url of the location bar.
However, because the response doesn't came, chrome will still display the current page content even though the NavigationController::GetVisibleEntry() has already changed.
On desktop, the location bar seems only get updated once the response comes back. As a result, although the visible entry points to the "google.com:1234" URL, but the location bar is not updated.
On Android, however, the location bar is immediately updated once the loading starts. As a result, the URL is changed to "google.com:1234".

The issue seems to be related to navigation and UI.
1. If navigation is underway and response hasn't come back, we probably shounldn't update the visible entry.
2. Or once visible entry changes, we should immediately change the location bar and clear up the frame content so that user will not see the original content

This issue is not related to download though. As we can always call NavigationController::LoadURLWithParams() and passing in a url that will time out. And android will always show the new URL in location bar although the page content is stale.

creis@, would you please help triaging this?

[Monorail components: -UI>Browser>Downloads]

### es...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### cr...@chromium.org (2019-08-22)

https://crbug.com/chromium/979443#c14: Sorry for missing this; it came in while I was OOO.

> When the page loads, the javascript automatically clicks on the download link to perform a redirect.  And that should change the url of the location bar.

That's not correct.  Renderer-initiated navigations should *not* update the location bar (because that makes this kind of spoof possible), and they should not be returned via GetVisibleEntry().  That is, NavigationControllerImpl::GetVisibleEntry() doesn't return the pending entry if is_renderer_initiated() is true.

You're right that we just happen to not be updating the address bar to show the new visible entry on desktop, but that's a fragile state, and we don't want the URL in the visible entry.  As noted earlier, opening DevTools makes it appear, as does switching to another tab and coming back.  It's just a matter of getting the omnibox to refresh.

The bug seems to have been introduced in r576376 (69.0.3497.0) because NavigateOnUIThread in DownloadResourceHandler is treating the redirect as a new browser-initiated navigation with LoadURLWithParams (apparently with no security checks).  I'm very concerned about this code-- it would allow navigations to chrome:// URLs, for example, though we appear to be catching that somewhere else in my quick test of it.

The catch is that I don't know where this code ended up-- the download code seems to have been refactored since this landed, and I don't see it at first glance.  Ah, the bug is also in DownloadManagerImpl::InterceptDownload, which still around.  Not sure if there are more places?

qinmin@ and jochen@: Can you track down all the download cases where this LoadURLWithParams code ended up and ensure it gets treated as a renderer-initiated navigation with appropriate security checks (e.g., FilterURL / CanRequestURL)?  I'm also about go to OOO for another week, but nasko@, alexmos@, or other navigation folks can point you to the right checks to impose.


[Monorail components: UI>Browser>Downloads]

### qi...@chromium.org (2019-08-22)

I think i have a simple fix. If the download is initiated by renderer,  the LoadURLParams  should carry a is_renderer_initiated flag when a cross-origin redirect happens.
That will keep the existing visible entry and not to be replaced by the pending entry.
working on a CL now

### qi...@chromium.org (2019-08-23)

CL is here: https://chromium-review.googlesource.com/c/chromium/src/+/1768825

Per #16, CanRequestURL() is checked during the new renderer-initiated navigation, so I guess we are fine.

### sh...@chromium.org (2019-08-27)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6d7c9ec2923a71d3f9acb7fdd019a5e56f44c09b

commit 6d7c9ec2923a71d3f9acb7fdd019a5e56f44c09b
Author: Min Qin <qinmin@chromium.org>
Date: Tue Aug 27 20:28:53 2019

Pass renderer initiated flag for navigations triggered by cross-origin download

If a navigation is triggered by a cross-origin download initiated by
renderer, the navigation should carry the renderer initiated flag.

BUG=979443

Change-Id: I0716193768a5473f70e909b7efbb5fc74933d89e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1768825
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#690869}

[modify] https://crrev.com/6d7c9ec2923a71d3f9acb7fdd019a5e56f44c09b/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/6d7c9ec2923a71d3f9acb7fdd019a5e56f44c09b/components/download/internal/common/resource_downloader.cc
[modify] https://crrev.com/6d7c9ec2923a71d3f9acb7fdd019a5e56f44c09b/components/download/internal/common/resource_downloader.h
[modify] https://crrev.com/6d7c9ec2923a71d3f9acb7fdd019a5e56f44c09b/components/download/public/common/download_create_info.h
[modify] https://crrev.com/6d7c9ec2923a71d3f9acb7fdd019a5e56f44c09b/content/browser/download/download_browsertest.cc
[modify] https://crrev.com/6d7c9ec2923a71d3f9acb7fdd019a5e56f44c09b/content/browser/download/download_manager_impl.cc


### ch...@gmail.com (2019-08-27)

Verified on Chromium desktop 78.0.3895.0 refs/heads/master@{#690869} this seems like fixed, I will verify it on tomorrow's Canary build on Android and desktop. Thanks for the fix!.

### ch...@gmail.com (2019-08-29)

Verified on Canary 78.0.3895.0 (64-bit). Fixed.

### do...@chromium.org (2019-08-30)

Security marshal - marking as fixed. :)

### sh...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-30)

Requesting merge to stable M76 because latest trunk commit (690869) appears to be after stable branch point (665002).

Requesting merge to beta M77 because latest trunk commit (690869) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-30)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-08-30)

ginmin@ - please respond to C#26 to consider the merge request

### qi...@chromium.org (2019-08-31)

1.yes
2.https://chromium-review.googlesource.com/c/chromium/src/+/1768825
3. yes
4, security fix
5. no


### la...@google.com (2019-09-03)

merge approved for M77 branch 3865

### na...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### sr...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-03)

This request for M77 merge is already approved. Please land your changes into M77 branch (3865) today. We are one week away from Stable and doing the final Beta tomorrow.

### la...@google.com (2019-09-03)

Dropping the Merge-Approved-M77 label as the change has landed into the branch - https://chromium-review.googlesource.com/c/chromium/src/+/1782800


### wf...@chromium.org (2019-09-04)

hello from the VRP panel. Please make sure you attach any POC code to the bug when submitting and do not rely on external websites for demonstration.

### na...@google.com (2019-09-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-05)

Congrats! The Panel decided to reward $2,000 for this report! 

### na...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2019-12-20)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/979443?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>Downloads, UI>Browser>Navigation]
[Monorail mergedwith: crbug.com/chromium/996689]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095527)*
