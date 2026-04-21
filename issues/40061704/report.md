# Security: Heap-buffer-overflow in CommerceHintAgent::DidFinishLoadCallback 

| Field | Value |
|-------|-------|
| **Issue ID** | [40061704](https://issues.chromium.org/issues/40061704) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Shopping |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2022-11-11 |
| **Bounty** | $2,500.00 |

## Description

**Steps to reproduce the problem:**

1. apply the change.diff and compile Chromium with ASAN
2. put navigation.html, nav1.html together and start a server. Note that this needs a non-IP address domain, I use "mytest.com" here.
3. run `./chrome --user-data-dir=/tmp/noexist --enable-features=NtpChromeCartModule,ContextMenuPerformanceInfoAndRemoteHintFetching --disable-popup-blocking --no-sandbox http://mytest.com:8605/navigation.html`

This is a render crash, so we need `--no-sandbox` to get the symbols.

**Problem Description:**

1. Analysis

In function `CommerceHintAgent::DidCommitProvisionalLoad`[1], it will pass a callback `CommerceHintAgent::DidCommitProvisionalLoadCallback` to `OnNavigation`(1). And we can call `CommerceHintAgent::DidCommitProvisionalLoad` more than once, so, in one `CommerceHintAgent`, there could be more than one callback `CommerceHintAgent::DidCommitProvisionalLoadCallback` waiting for run.

```
void CommerceHintAgent::DidCommitProvisionalLoad(  
    ui::PageTransition transition) {  
  if (!starting_url_.is_valid())  
    return;  
  DCHECK(starting_url_.SchemeIsHTTPOrHTTPS());  
  should_use_dom_heuristics_.reset();  
  mojo::Remote<mojom::CommerceHintObserver> observer =  
      GetObserver(render_frame());  
  if (!commerce::kOptimizeRendererSignal.Get()) {  
    DidCommitProvisionalLoadCallback(starting_url_, std::move(observer), false,  
                                     mojom::Heuristics::New());  
    return;  
  }  
  auto\* observer_ptr = observer.get();  
  observer_ptr->OnNavigation(  
      starting_url_, CommerceHeuristicsData::GetInstance().GetVersion(),  
      base::BindOnce(&CommerceHintAgent::DidCommitProvisionalLoadCallback, // (1) callback is passed   
                     weak_factory_.GetWeakPtr(), starting_url_,  
                     std::move(observer)));  
}  

```

In callback `CommerceHintAgent::DidCommitProvisionalLoadCallback`, the `starting_url_` will be set to a null GURL() [2]. Therefore, if there are two `CommerceHintAgent::DidCommitProvisionalLoadCallback` executing consecutively, the latter will use a null `starting_url_`, but there is no check. This `starting_url_.PathForRequestPiece()`(2) will return a string of length -1, but this will be covert to an unsigned integer 0xffffffffffffffff. The use of any element of this string will cause an overflow.

```
void CommerceHintAgent::DidCommitProvisionalLoadCallback(  
    const GURL& url,  
    mojo::Remote<mojom::CommerceHintObserver> observer,  
    bool should_skip,  
    mojom::HeuristicsPtr heuristics) {  
  should_skip_ = should_skip;  
  if (should_skip)  
    return;  
  if (!heuristics->version_number.empty() &&  
      heuristics->version_number !=  
          CommerceHeuristicsData::GetInstance().GetVersion()) {  
    bool is_populated =  
        CommerceHeuristicsData::GetInstance().PopulateDataFromComponent(  
            heuristics->hint_json_data, heuristics->global_json_data,  
            /\*product_id_json_data\*/ "", /\*cart_extraction_script\*/ "");  
    DCHECK(is_populated);  
    CommerceHeuristicsData::GetInstance().UpdateVersion(  
        base::Version(heuristics->version_number));  
  }  
  if (IsAddToCart(starting_url_.PathForRequestPiece())) { // (2) null GURL().PathForRequestPiece will return a string of length -1  
    RecordCommerceEvent(CommerceEvent::kAddToCartByURL);  
    OnAddToCart(render_frame());  
  }  
  if (!IsVisitCart(starting_url_) && IsVisitCheckout(starting_url_)) {  
    RecordCommerceEvent(CommerceEvent::kVisitCheckout);  
    OnVisitCheckout(render_frame());  
  }  
  if (IsPurchase(starting_url_)) {  
    RecordCommerceEvent(CommerceEvent::kPurchaseByURL);  
    OnPurchase(render_frame());  
  }  
  
  starting_url_ = GURL(); //  starting_url_ will be set to null GURL  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/cart/commerce_hint_agent.cc;l=1059;drc=5e3ca35bda50d49a27f05a1111c95dc0aea39c2f;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/renderer/cart/commerce_hint_agent.cc;l=1085;drc=5e3ca35bda50d49a27f05a1111c95dc0aea39c2f;bpv=0;bpt=0>

**Additional Comments:**  

2. Affected versions

This problem is introduced in this commit: 8694e1c99e688be202e3118727b8978ec173babe  

Because this commit add the callback `CommerceHintAgent::DidCommitProvisionalLoadCallback`

The Dev channel is updated to 109.0.5396.2, and it is affected by this vulnerability.  

The Beta channel is updated to 108.0.5359.30, and it is affected by this vulnerability.

The Stable channel is updated to 107.0.5304.87, which doesn't have the callback, so it is not affected by this vulnerability

3. POC  
   
   In my poc, you need to patch the logic of browser to simulate a signed-in user with more than one profiles:

```
// On Android, commerce hint observer is enabled for all users with the feature  
// enabled since the observer is only used for collecting metrics for now, and  
// we want to maximize the user population exposed; on Desktop, ChromeCart is  
// not available for non-signin single-profile users and therefore neither does  
// commerce hint observer.  
#if !BUILDFLAG(IS_ANDROID)  
  Profile\* profile = Profile::FromBrowserContext(  
      frame_host->GetProcess()->GetBrowserContext());  
  auto\* identity_manager = IdentityManagerFactory::GetForProfile(profile);  
  ProfileManager\* profile_manager = g_browser_process->profile_manager();  
  if (!identity_manager || !profile_manager)  
    return;  
  if (!identity_manager->HasPrimaryAccount(signin::ConsentLevel::kSignin) &&  
      profile_manager->GetNumberOfProfiles() <= 1)  
    return;  
#endif  

```

Also note that flag `ContextMenuPerformanceInfoAndRemoteHintFetching` is not necessary, it is just used to pass this check `IsUserPermittedToFetchFromRemoteOptimizationGuide`[4]. You could let the `IsUserConsentedToAnonymousDataCollectionAndAllowedToFetchFromRemoteService` return true to pass this check.

```
bool IsUserPermittedToFetchFromRemoteOptimizationGuide(  
    bool is_off_the_record,  
    PrefService\* pref_service) {  
  if (is_off_the_record)  
    return false;  
  
  if (switches::ShouldOverrideCheckingUserPermissionsToFetchHintsForTesting()) {  
    return true;  
  }  
  
  if (!features::IsRemoteFetchingEnabled())  
    return false;  
  
  if (features::IsRemoteFetchingExplicitlyAllowedForPerformanceInfo())  
    return true;  
  
  return IsUserConsentedToAnonymousDataCollectionAndAllowedToFetchFromRemoteService(  
      pref_service);  
}  

```

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_browser_interface_binders.cc;l=429;bpv=1;bpt=0;drc=16071723febba2f1b9e92c72836395065d5d9442>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:components/optimization_guide/core/optimization_guide_permissions_util.cc;l=46;drc=a0dedabb214a245c792009e64baf333c7e8d7357;bpv=0;bpt=1>

4. Patch  
   
   I think you should check the `starting_url_` in function `CommerceHintAgent::DidCommitProvisionalLoadCallback` too.  
   
   Please see the attached patch.diff.

\*\*Chrome version: \*\* \*\*Channel: \*\* Beta

**OS:** Linux

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-11)

ty for your report. I am triaging this now. I'm curious about the browser patch in particular, can you explain why this is needed, and how I might trigger this vuln without it?

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-11)

This bug seems legitimate to me. What I haven't determined is the set of circumstances for this to happen in practice, which makes gauging the risk to users harder. I'm triaging as High for now, but I might lower this depending on my further analysis.

I note also that the feature seems to be enabled by default https://source.chromium.org/chromium/chromium/src/+/main:components/search/ntp_features.cc;l=80

[Monorail components: UI>Browser>NewTabPage UI>Browser>Shopping]

### yu...@chromium.org (2022-11-11)

Thanks for the filing! This looks legit to me as well, we didn't realize that DidCommitProvisionalLoad could be called for multiple times in one navigation. The original post was correct, this change has not reached Stable channel yet. I'll come up with a fix and see if we can merge it to M108; if not, I'll revert the culprit CL that introduces the code path.

### [Deleted User] (2022-11-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e97b7b9aa77f21a1d7959446069f69e540016833

commit e97b7b9aa77f21a1d7959446069f69e540016833
Author: Yue Zhang <yuezhanggg@chromium.org>
Date: Mon Nov 14 07:19:37 2022

[ChromeCart] Add a missed URL check

https://crrev.com/c/3924102 missed the fact that
DidCommitProvisionalLoad could be called for multiple times in one
navigation, which would make the starting_url_ invalid for later
DidCommitProvisionalLoadCallback when trying to access. This CL fixes
this issue by adding the missed check of starting_url_.

Bug: 1383422
Change-Id: I179b243643481e7b04071af72233d4ba3d9afd80
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4023354
Commit-Queue: Wei-Yin Chen <wychen@chromium.org>
Auto-Submit: Yue Zhang <yuezhanggg@chromium.org>
Reviewed-by: Wei-Yin Chen <wychen@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1070888}

[modify] https://crrev.com/e97b7b9aa77f21a1d7959446069f69e540016833/chrome/renderer/cart/commerce_hint_agent.cc


### am...@chromium.org (2022-11-14)

This does indeed to appear to be a stable release blocker, so this fix would need to be merged to branch 5359/M108 before Stable Cut for M108, scheduled for tomorrow 

### [Deleted User] (2022-11-14)

Requesting merge to beta M108 because latest trunk commit (1070888) appears to be after beta branch point (1058933).

Requesting merge to dev M109 because latest trunk commit (1070888) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@chromium.org (2022-11-14)

Flipping status to assigned. Will mark this as fixed once the merging process if finished.

### am...@chromium.org (2022-11-15)

Hi yuezhanggg@, apologies if this mucks with your workflow, however, security merge review and release process are reliant on bugs being marked Fixed. This allows the bot to update the issue with the appropriate merge request labels (as you can see in https://crbug.com/chromium/1383422#c10) and get it into our security merge review queue. 
Please refer to https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#Security-merge-triage

In the future, please update all fixed security bugs as Fixed once the resolving CL is landed to ensure we can review and approve security fixes for merge review as soon as possible. This is a necessity to keep our patch gap as small as possible and help protect our users from n-day exploitation of from unshipped security fixes. Thank you! :)

Updating issue as Fixed accordingly. 

### yu...@chromium.org (2022-11-15)

Oh I'm so sorry I didn't know this difference, thanks for the context! Let me know if there is anything I could help with the security merge review process.

### am...@chromium.org (2022-11-15)

Merges to M109 and M108 approved; please merge this fix to branches 5414 and 5359. Please prioritize the merge of this fix to branch 5359/m108 to be completed at soonest (by 10am Pacific Tuesday 15 November) so this fix can be included in the M108/Stable cut. 

### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/76feaab5e7581089481fe0dad968167207d465e1

commit 76feaab5e7581089481fe0dad968167207d465e1
Author: Yue Zhang <yuezhanggg@chromium.org>
Date: Tue Nov 15 01:59:18 2022

[M109][ChromeCart] Add a missed URL check

https://crrev.com/c/3924102 missed the fact that
DidCommitProvisionalLoad could be called for multiple times in one
navigation, which would make the starting_url_ invalid for later
DidCommitProvisionalLoadCallback when trying to access. This CL fixes
this issue by adding the missed check of starting_url_.

(cherry picked from commit e97b7b9aa77f21a1d7959446069f69e540016833)

Bug: 1383422
Change-Id: I179b243643481e7b04071af72233d4ba3d9afd80
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4023354
Commit-Queue: Wei-Yin Chen <wychen@chromium.org>
Auto-Submit: Yue Zhang <yuezhanggg@chromium.org>
Reviewed-by: Wei-Yin Chen <wychen@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1070888}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4027027
Commit-Queue: Yue Zhang <yuezhanggg@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#39}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/76feaab5e7581089481fe0dad968167207d465e1/chrome/renderer/cart/commerce_hint_agent.cc


### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5f68aadf00e1ac7b501935d11721b4258e51599

commit f5f68aadf00e1ac7b501935d11721b4258e51599
Author: Yue Zhang <yuezhanggg@chromium.org>
Date: Tue Nov 15 01:59:10 2022

[M108][ChromeCart] Add a missed URL check

https://crrev.com/c/3924102 missed the fact that
DidCommitProvisionalLoad could be called for multiple times in one
navigation, which would make the starting_url_ invalid for later
DidCommitProvisionalLoadCallback when trying to access. This CL fixes
this issue by adding the missed check of starting_url_.

(cherry picked from commit e97b7b9aa77f21a1d7959446069f69e540016833)

Bug: 1383422
Change-Id: I179b243643481e7b04071af72233d4ba3d9afd80
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4023354
Commit-Queue: Wei-Yin Chen <wychen@chromium.org>
Auto-Submit: Yue Zhang <yuezhanggg@chromium.org>
Reviewed-by: Wei-Yin Chen <wychen@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1070888}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4026942
Reviewed-by: Will Harris <wfh@chromium.org>
Commit-Queue: Yue Zhang <yuezhanggg@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#834}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/f5f68aadf00e1ac7b501935d11721b4258e51599/chrome/renderer/cart/commerce_hint_agent.cc


### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/76feaab5e7581089481fe0dad968167207d465e1

commit 76feaab5e7581089481fe0dad968167207d465e1
Author: Yue Zhang <yuezhanggg@chromium.org>
Date: Tue Nov 15 01:59:18 2022

[M109][ChromeCart] Add a missed URL check

https://crrev.com/c/3924102 missed the fact that
DidCommitProvisionalLoad could be called for multiple times in one
navigation, which would make the starting_url_ invalid for later
DidCommitProvisionalLoadCallback when trying to access. This CL fixes
this issue by adding the missed check of starting_url_.

(cherry picked from commit e97b7b9aa77f21a1d7959446069f69e540016833)

Bug: 1383422
Change-Id: I179b243643481e7b04071af72233d4ba3d9afd80
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4023354
Commit-Queue: Wei-Yin Chen <wychen@chromium.org>
Auto-Submit: Yue Zhang <yuezhanggg@chromium.org>
Reviewed-by: Wei-Yin Chen <wychen@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1070888}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4027027
Commit-Queue: Yue Zhang <yuezhanggg@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#39}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/76feaab5e7581089481fe0dad968167207d465e1/chrome/renderer/cart/commerce_hint_agent.cc


### [Deleted User] (2022-11-15)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-15)

[Empty comment from Monorail migration]

### vo...@google.com (2022-11-17)

The problem was introduced in 8694e1c99e688be202e3118727b8978ec173babe, DidCommitProvisionalLoadCallback is not presentin M102. Marking as not applicable for LTS.

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations, Krace! The VRP Panel has decided to award you $2,500 for this report of a moderately mitigated security bug + bisect bonus. Thank you for your efforts and reporting this issue to us! 

### me...@gmail.com (2022-12-02)

Hi amyressler@, thank you for your explanation.
But this issue only needs to login in a Google Accout, so I have to patch the browser code. According to the rules:
'Moderately mitigated: Security bug with multiple mitigations; e.g. a malicious extension and two or fewer user interactions or winning a race condition'
As I said in https://crbug.com/chromium/1383422#c1, 
'you need to patch the logic of browser to simulate a signed-in user with more than one profiles'
Therefore, log in an google account and have more than one profiles is also considered as Moderately mitigated?
Thank you again.

### am...@chromium.org (2022-12-02)

Hi Krace, the mitigation here is not that the user is login to a google account or even more than one profile, that is very standard and expected behavior that we would consider very much within a standard threat model. The mitigation that resulted in this bug being rated and rewarded as moderately mitigated here is that there is a race condition, one that is very visible to the user.

I hope that explanation helps! 

### me...@gmail.com (2022-12-02)

Got it, thank you:)

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1383422?no_tracker_redirect=1

[Multiple monorail components: UI>Browser>NewTabPage, UI>Browser>Shopping]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061704)*
