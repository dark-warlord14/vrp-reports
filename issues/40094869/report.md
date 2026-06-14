# Multiple file download protection bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [40094869](https://issues.chromium.org/issues/40094869) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Loader, UI>Browser>Downloads, UI>Browser>Navigation |
| **Platforms** | Windows |
| **Reporter** | Ju...@microsoft.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2019-05-05 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome has multiple file download protection. But download request followed by cross-origin redirect can cause multiple download if final end point after redirect results in download.

**VERSION**  

Chrome Version:74 stable  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Go to <https://shhnjk.azurewebsites.net/autodownload.html>

## Timeline

### ad...@google.com (2019-05-05)

Thanks for the report!

I can confirm that this site downloads multiple files without choosing 'allow' on the prompt, so this sounds valid to me.

qinmin@, you seem to have looked after lots of download issues lately so sending this your way (even though your profile says you work on Clank only.) Hope that's right - otherwise please pass on.

### sh...@chromium.org (2019-05-06)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2019-05-06)

[Empty comment from Monorail migration]

[Monorail components: Blink>Loader]

### qi...@chromium.org (2019-05-06)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### qi...@chromium.org (2019-05-06)

I saw that all the DownloadManager::DownloadUrl() calls are blocked if we don't allow the origin to issue multiple downloads. However, downloads that are caused by the navigation to the URL is not blocked. I am wondering why we issue both a navigation request and a DownloadUrl() request in this case.

yaoxia@, you worked on download attribute recently, can you check why a separate navigation request is issued along with downloadUrl() call?

### ya...@chromium.org (2019-05-07)

After looking at DownloadRequestLimiter:

For <a download> download, it updates the state of DownloadRequestLimiter before knowing whether it's going to redirect. A X-origin redirection will count as a browser initiated navigation that will resets the state of DownloadRequestLimiter, and therefore the following downloads will still succeed.

For this specific test in the bug, the reason you see both prompt and downloads is that it gets triggered so fast, so the 1st download succeeds, the 2nd-Nth downloads triggers the prompt, but when the navigation caused by the 1st redirection is observed, the state is reset, and the whole process will go over again. This is a site that triggers multiple download without a prompt: https://cr.kungfoo.net/yao/downloads/multiple

I believe there was a reason for treating this kind of download as a navigation in the first place, but I'm not exactly sure, maybe for security? Add @jochen for more comment who added DownloadCrossOriginRedirects::kNavigate/kFollow and also redirection mechanism (https://chromium-review.googlesource.com/c/chromium/src/+/1138081/)

My initial thought on the solution is 1) we shouldn't let the navigation caused by this type of redirection reset the states of DownloadRequestLimiter, and 2) in DownloadRequestLimiter::CanDownload(), when it encounters a download which is resulted from a redirection triggered also from here previously, it should keep using the previous policy, rather than using the most up-to-date policy.

I would like to own this bug but it might take a while for me to understand the infrastructure around here. Feel free to assign to someone who's more familiar with this multiple downloads intervention, otherwise I can slowly look into it.


### sh...@chromium.org (2019-05-22)

yaoxia: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dc5ed1036ef464b0bbc6575c9ac518e3997808ea

commit dc5ed1036ef464b0bbc6575c9ac518e3997808ea
Author: Yao Xiao <yaoxia@chromium.org>
Date: Tue Jun 04 19:19:09 2019

Fix multiple download protection for <a download> x-origin redirect

The bug: multiple downloads protection is bypassed when there are multiple
<a download> download attempts and they end up triggering a x-origin redirect
to another download.

The cause: Each x-origin redirect following the <a download> is being treated as
a navigation. (See DownloadManagerImpl::InterceptDownload() (NetworkService
enabled), DownloadResourceHandler::OnRequestRedirected() (NetworkService
disabled)). The navigation will hit
DownloadRequestLimiter::TabDownloadState::DidStartNavigation that resets some
state of the limiter, and future downloads won't be prevented.

The solution: plumb |from_download_cross_origin_redirect| to NavigationRequest,
and skip resetting the limiter state when the flag is true.

Bug: 959640
Change-Id: I7d8aca09670be5258e149e34e3e6f2f3107442ff
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1627209
Reviewed-by: Jochen Eisinger <jochen@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Yao Xiao <yaoxia@chromium.org>
Cr-Commit-Position: refs/heads/master@{#665973}

[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/chrome/browser/download/download_browsertest.cc
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/chrome/browser/download/download_request_limiter.cc
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/chrome/browser/download/download_request_limiter.h
[add] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/chrome/test/data/downloads/multiple_a_download_x_origin_redirect_to_download.html
[add] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/chrome/test/data/downloads/redirect_x_origin_download.html
[add] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/chrome/test/data/downloads/redirect_x_origin_download.html.mock-http-headers
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/browser/download/download_manager_impl.cc
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/browser/download/download_resource_handler.cc
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/browser/frame_host/navigation_controller_impl.cc
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/browser/frame_host/navigation_handle_impl.cc
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/browser/frame_host/navigation_handle_impl.h
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/browser/frame_host/navigation_request.h
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/public/browser/navigation_controller.cc
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/public/browser/navigation_controller.h
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/public/browser/navigation_handle.h
[modify] https://crrev.com/dc5ed1036ef464b0bbc6575c9ac518e3997808ea/content/public/test/mock_navigation_handle.h


### sh...@chromium.org (2019-06-05)

yaoxia: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-11)

Requesting merge to M75 because latest trunk commit (665973) appears to be after beta branch point (652427).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-11)

This bug requires manual review: Request affecting a post-stable build
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
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-06-11)

adetaylor@ yaoxia@ for M75 we are at 25% stable and this has been there since M74, so i am rejecting the merge for M75 and targeting the fix to M76, Pls re-apply the merge-request label if you think this warrants a merge to M75 now.

### ad...@chromium.org (2019-06-11)

OK, agreed.

### Ju...@microsoft.com (2019-06-13)

PoC source:
<a href="/location.php?url=https://www.google.com/complete/search?q=a%26cp%3D1%26client%3Dpsy-ab%26xssi%3Dt%26gs_ri%3Dgws-wiz%26hl%3Den%26authuser%3D0%26psi%3D492jXIbRLYmt-gTrjK7QCg.1554243044952%26ei%3D492jXIbRLYmt-gTrjK7QCg" download="test.txt">go</a>

<script>
setInterval(()=>{document.querySelector("a").click();},1);
</script>

### na...@google.com (2019-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-06-13)

Congrats! The Panel decided to reward $500 for this report!

### ad...@google.com (2019-09-09)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-09-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-20)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/959640?no_tracker_redirect=1

[Multiple monorail components: Blink>Loader, UI>Browser>Downloads, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094869)*
