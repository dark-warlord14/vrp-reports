# Residual UAF in token fetcher code

| Field | Value |
|-------|-------|
| **Issue ID** | [40058730](https://issues.chromium.org/issues/40058730) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>WebLayer |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | bl...@chromium.org |
| **Created** | 2022-02-09 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36

Steps to reproduce the problem:
There's an insufficient fix to the patch https://chromium-review.googlesource.com/c/chromium/src/+/3306578

The patch fixes the SafeBrowsingPrimaryAccountTokenFetcher usage in [1], but still leaving the possible UAF issue [2] in the related code of  weblayer.

1. https://source.chromium.org/chromium/chromium/src/+/main:components/safe_browsing/core/browser/sync/safe_browsing_primary_account_token_fetcher.cc;l=37-40;drc=c458116b70c1498f5858e7c09d0e2445b72e3009

const int request_id = token_fetch_tracker_.StartTrackingTokenFetch(
    std::move(callback),
    base::BindOnce(&SafeBrowsingPrimaryAccountTokenFetcher::OnTokenTimeout,
                    weak_ptr_factory_.GetWeakPtr())); // [1]

2. https://source.chromium.org/chromium/chromium/src/+/main:weblayer/browser/safe_browsing/safe_browsing_token_fetcher_impl.cc;l=31-34;drc=664bd2172f4e0b03959f227bd572ba352afe8d66

  const int request_id = token_fetch_tracker_.StartTrackingTokenFetch(
      std::move(callback),
      base::BindOnce(&SafeBrowsingTokenFetcherImpl::OnTokenTimeout,
                     base::Unretained(this))); // [2]

What is the expected behavior?

What went wrong?
Above all.

Did this work before? N/A 

Chrome version: 97.0.4692.99  Channel: n/a
OS Version:

## Timeline

### [Deleted User] (2022-02-09)

[Empty comment from Monorail migration]

### ad...@google.com (2022-02-09)

Thanks, good spot.

blundell@, over to you as the fixer or https://crbug.com/chromium/1271747. I haven't verified the WebLayer code pattern above is equally vulnerable but it does look plausible to me.

Labelling as FoundIn-98 as the oldest currently relevant branch. Copying Medium severity from https://crbug.com/chromium/1271747 although also discussing rationale for that severity with mpdenton@ so this might get adjusted. (Colin, do you know what sort of UI interaction is required to trigger these types of bug? That would affect our severity rating)

[Monorail components: Internals>WebLayer Services>Safebrowsing]

### [Deleted User] (2022-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-09)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-02-09)

I understand from mpdenton that the rationale for medium severity on the original bug is because it was triggered by a failed network request to a Google service, which may limit exploitability.

### dr...@chromium.org (2022-02-09)

(Triaging SB bugs with owners)

### bl...@chromium.org (2022-02-10)

Thanks for the report! I do indeed need to make this fix, and I'll do so shortly.

FYI, there is no UAF currently:

- The only way that SafeBrowsingTokenFetcherImpl is instantiated at the current time is for ClientSideDetectionHost [1]
- ClientSideDetectionHost doesn't destroy its SafeBrowsingTokenFetcher instance in its token fetched callback [2]

[1] https://source.chromium.org/chromium/chromium/src/+/main:weblayer/browser/safe_browsing/weblayer_safe_browsing_tab_observer_delegate.cc;l=31;drc=2efae6f74f98ae428f6339635beaa13e6a084add;bpv=1;bpt=1
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/safe_browsing/content/browser/client_side_detection_host.cc;l=632;bpv=1;bpt=1?q=ClientSideDetectionHost::OnGot&sq=&ss=chromium

### bl...@chromium.org (2022-02-10)

[Empty comment from Monorail migration]

### bl...@chromium.org (2022-02-11)

Fix out for review here:

https://chromium-review.googlesource.com/c/chromium/src/+/3455623

### xi...@chromium.org (2022-02-11)

Thanks Colin! Adding the security impact none label since the UAF cannot be triggered in production.

### ha...@gmail.com (2022-02-13)

[Comment Deleted]

### ha...@gmail.com (2022-02-13)

Thanks for the work.

I think there's another place that SafeBrowsingTokenFetcherImpl is instantiated, in RealTimeUrlLookupServiceFactory [1]

[1] https://source.chromium.org/chromium/chromium/src/+/main:weblayer/browser/safe_browsing/real_time_url_lookup_service_factory.cc;l=58-60;drc=d2a29692aa123852430813986e64d2ced2d10bc6

### gi...@appspot.gserviceaccount.com (2022-02-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2c43bd58fde81673db05e6ad448bd0e6dd7b7040

commit 2c43bd58fde81673db05e6ad448bd0e6dd7b7040
Author: Colin Blundell <blundell@chromium.org>
Date: Mon Feb 14 08:51:28 2022

[WebLayer] Harden SafeBrowsingTokenFetcherImpl against UAF

https://chromium-review.googlesource.com/c/chromium/src/+/3306578 fixed
flows that could result in UAF's in
SafeBrowsingPrimaryAccountTokenFetcher. //weblayer's
SafeBrowsingTokenFetcherImpl has similar issues due to its analogous
usage of SafeBrowsingTokenFetchTracker. These issues are not currently
hit in production (see explanation in [1]), but obviously they should
be fixed. This CL does so in a manner similar to that of the CL
referenced above.

[1] https://bugs.chromium.org/p/chromium/issues/detail?id=1295699#c7

Bug: 1295699
Change-Id: I095472514fd78e0d6b3cf2dfd201f1eefbb31609
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3455623
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Commit-Queue: Colin Blundell <blundell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#970532}

[modify] https://crrev.com/2c43bd58fde81673db05e6ad448bd0e6dd7b7040/weblayer/browser/safe_browsing/safe_browsing_token_fetcher_impl.cc
[modify] https://crrev.com/2c43bd58fde81673db05e6ad448bd0e6dd7b7040/weblayer/browser/safe_browsing/safe_browsing_token_fetcher_impl_unittest.cc


### bl...@chromium.org (2022-02-14)

happyercat@: Thanks for the report and the analysis! You are correct that that is another instantiation site. However, RealTimeLookupServiceFactory currently configures RealTimeUrlLookupService such that it never performs access token fetches in production [1]; hence the fetcher created there isn't actually used in production at this time.

[1] https://source.chromium.org/chromium/chromium/src/+/main:weblayer/browser/safe_browsing/real_time_url_lookup_service_factory.cc;l=63

### bl...@chromium.org (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-11)

Thank you for this report! The VRP Panel has decided to award you $1,000 for this report as a thank you as this issue appears to have a limited potential exploitability and this issue does not currently exist in production code, so it does not affect users at this time. We greatly appreciate your efforts, however, and reporting this issue to us! 

### am...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1295699?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>WebLayer, Services>Safebrowsing]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058730)*
