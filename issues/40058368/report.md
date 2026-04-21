# Security: UAF in ChromeContentBrowserClient::CreateURLLoaderThrottles

| Field | Value |
|-------|-------|
| **Issue ID** | [40058368](https://issues.chromium.org/issues/40058368) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader>WebPackaging, Internals>Network |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | cd...@chromium.org |
| **Created** | 2021-12-30 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

PrefetchURLLoaderService is responsible for handling prefetch requests from renderer including something like '<link rel="prefetch">'. PrefetchURLLoaderService::CreateLoaderAndStart will be invoked which creates a PrefetchURLLoader instance to load the resource. The PrefetchURLLoader is self-owned so it would be freed only when the client disconnects or the request is completed [1]. Meanwhile, PrefetchURLLoader's constructor takes a RepeatingCallback as a parameter which binds to PrefetchURLLoaderService::CreateURLLoaderThrottles [2]. Given that PrefetchURLLoaderService is a Refcounted object, this will add a reference to the service instance so that it will not be freed earlier than PrefetchURLLoader.

PrefetchURLLoaderService::CreateURLLoaderThrottles will finally be invoked if the PrefetchURLLoader finds prefetching resource is served as a Signed Exchange then starting to read body through SignedExchangeLoader [3].

In PrefetchURLLoaderService::CreateURLLoaderThrottles, it passes a member variable `browser_context_` as a parameter to another function CreateContentBrowserURLLoaderThrottles [4]. The `browser_context_` is a raw pointer to BrowserContext that could have been freed at an earlier time, thus causing UAF at [5].

To conclude, PrefetchURLLoader is self-owned and doesn't associates itself with BrowserContext, but its code may access the raw pointer stored in PrefetchURLLoaderService after the context is gone.

```
mojo::MakeSelfOwnedReceiver(              // ===> [1]  
    std::make_unique<PrefetchURLLoader>(  
        // skip  
        base::BindRepeating(  
            &PrefetchURLLoaderService::CreateURLLoaderThrottles, this,  // ===> [2]  
            resource_request, current_context.frame_tree_node_id),  
        browser_context_, signed_exchange_prefetch_metric_recorder_,  
        std::move(prefetched_signed_exchange_cache), accept_langs_,  
        base::BindOnce(  
            &PrefetchURLLoaderService::GenerateRecursivePrefetchToken, this,  
            current_context.weak_ptr_factory.GetWeakPtr())),  
    std::move(receiver));  
  
void SignedExchangeLoader::StartReadingBody() {  
  // skip  
  if (!(outer_request_.load_flags & net::LOAD_PREFETCH) &&  
      base::FeatureList::IsEnabled(features::kSignedHTTPExchangePingValidity) &&  
      !validity_pinger_) {  
    validity_pinger_ = SignedExchangeValidityPinger::CreateAndStart(  
        \*inner_request_url_, url_loader_factory_,  
        url_loader_throttles_getter_.Run(),        // ===> [3]  
        outer_request_.throttling_profile_id,  
        base::BindOnce(&SignedExchangeLoader::StartReadingBody,  
                       weak_factory_.GetWeakPtr()));  
    DCHECK(validity_pinger_);  
    return;  
  }  
  
PrefetchURLLoaderService::CreateURLLoaderThrottles(  
    const network::ResourceRequest& request,  
    int frame_tree_node_id) {  
  return CreateContentBrowserURLLoaderThrottles(  
      request, browser_context_,                  // ===> [4]  
  
ChromeContentBrowserClient::CreateURLLoaderThrottles(  
    const network::ResourceRequest& request,  
    content::BrowserContext\* browser_context,  
    const base::RepeatingCallback<content::WebContents\*()>& wc_getter,  
    content::NavigationUIData\* navigation_ui_data,  
    int frame_tree_node_id) {  
  // skip  
  Profile\* profile = Profile::FromBrowserContext(browser_context);  
  // skip  
  bool matches_enterprise_allowlist = safe_browsing::IsURLAllowlistedByPolicy(  
      request.url, \*profile->GetPrefs());        // ===> [5]  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/prefetch_url_loader_service.cc;l=209;drc=6c9a8e348eadc7cb14ce09204b0cb0211769c0ac>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/prefetch_url_loader_service.cc;l=220;drc=6c9a8e348eadc7cb14ce09204b0cb0211769c0ac>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_package/signed_exchange_loader.cc;l=353;drc=6c9a8e348eadc7cb14ce09204b0cb0211769c0ac>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/loader/prefetch_url_loader_service.cc;l=358;drc=6c9a8e348eadc7cb14ce09204b0cb0211769c0ac>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/chrome_content_browser_client.cc;l=4595;drc=6c9a8e348eadc7cb14ce09204b0cb0211769c0ac>

**VERSION**  

Chrome Version: stable (96.0.4664.110) + dev

**REPRODUCTION CASE**

1. Unzip the attached poc.zip
2. Setup a HTTP server using nodejs  
   
   node ./server.js
3. Run following command, the browser should crash in a few seconds  
   
   out/Asan/chrome --user-data-dir=/tmp/xxx/ --ignore-certificate-errors <https://localhost:8000/poc.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log for details

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 4.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 22.7 KB)

## Timeline

### [Deleted User] (2021-12-30)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-01-04)

The PoC doesn't quite work, since window.close() will refuse to close a window not opened by a script. But if you close the browser manually, you do see the promised crash. This is memory corruption in the browser process. I don't think closing a tab is unusual enough to downgrade the severity, so setting severity Critical.

mmenke@, toyoshim@ - can you take a look?

[Monorail components: Internals>Network]

### [Deleted User] (2022-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-04)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-01-04)

adetaylor@ pointed out that we're considering profile destruction bugs in general as a mitigating factor for severity purposes, bringing this down to High.

### mm...@chromium.org (2022-01-04)

Passing the buck - completely unfamiliar with this code.  Looks like Kinuko wrote a lot of it, with horo@ reviewing at least some of it?

### ho...@chromium.org (2022-01-05)

This issue is related to Signed Exchange prefetching which is a part of Web Packaging project.

But sorry, I'm no longer working on Web Packaging project.


> @hayato, @ksakamoto, @myrzakereyms

Does anyone in Web Packaging team can handle this issue?

Thank you.

[Monorail components: Blink>Loader>WebPackaging]

### ha...@chromium.org (2022-01-05)

@ksakamoto.

Could you take a look at it? This is related to Signed Exchange.

@horo
Thanks for notifying us. If ksakamoto@ needs a help, we'd appreciate your help!
 

### ks...@chromium.org (2022-01-05)

PrefetchURLLoaderService::CreateURLLoaderThrottles is invoked not by [3] but by SignedExchangeCertFetcherFactoryImpl::CreateFetcherAndStart [6], but otherwise the reporter's analysis looks accurate.

The raw pointer `browser_context_` member in PrefetchUrlLoaderService was introduced in this CL:
https://chromium-review.googlesource.com/c/chromium/src/+/1707249/

And in the past we had a similar issue regarding the lifetime of BrowserContext and PrefetchURLLoader:
https://chromium-review.googlesource.com/c/chromium/src/+/1881379/

cduvall@: Could you take a look based on the above? I'm not sure what's the right way to fix this.

[6] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_package/signed_exchange_cert_fetcher_factory.cc;l=54;drc=13a62b6d89315e5a90deb712b0c1e47c72100f6c


### [Deleted User] (2022-01-05)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-05)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cd...@chromium.org (2022-01-05)

I'm not super familiar with signed exchange requirements, but I sent out a CL which fixes the lifetime issue in local testing: https://chromium-review.googlesource.com/c/chromium/src/+/3361198

### gi...@appspot.gserviceaccount.com (2022-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/223e1a1752f3513c4b250bc6b8246256febfe121

commit 223e1a1752f3513c4b250bc6b8246256febfe121
Author: Clark DuVall <cduvall@chromium.org>
Date: Thu Jan 06 01:21:21 2022

Fix lifetime bug in PrefetchURLLoader

PrefetchURLLoader is now owned by PrefetchURLLoaderService, which is no
longer refcounted. This makes the lifetime much easier to reason about.

Bug: 1283371
Change-Id: Iaa58c1f44cc9f066459ce344012f57faca533197
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3361198
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Reviewed-by: Kunihiko Sakamoto <ksakamoto@chromium.org>
Commit-Queue: Clark DuVall <cduvall@chromium.org>
Cr-Commit-Position: refs/heads/main@{#955986}

[modify] https://crrev.com/223e1a1752f3513c4b250bc6b8246256febfe121/content/browser/loader/prefetch_url_loader_service.cc
[modify] https://crrev.com/223e1a1752f3513c4b250bc6b8246256febfe121/content/browser/storage_partition_impl.h
[modify] https://crrev.com/223e1a1752f3513c4b250bc6b8246256febfe121/content/browser/loader/prefetch_url_loader_service.h
[modify] https://crrev.com/223e1a1752f3513c4b250bc6b8246256febfe121/content/browser/storage_partition_impl.cc


### cd...@chromium.org (2022-01-06)

This has been fixed. Should this be merged into M98/M97?

### cd...@chromium.org (2022-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

Requesting merge to extended stable M96 because latest trunk commit (955986) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (955986) appears to be after stable branch point (938553).

Requesting merge to dev M98 because latest trunk commit (955986) appears to be after dev branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-07)

Merge review required: M98 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-07)

Merge review required: M97 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-07)

Merge review required: M96 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2022-01-10)

pls answer https://crbug.com/chromium/1283371#c21 for merge review

### cd...@chromium.org (2022-01-10)

1. This is a high severity security fix
2. https://chromium-review.googlesource.com/c/chromium/src/+/3361198
3. Yes
4. No
5. N/A
6. Yes, repro instructions are in description

### am...@chromium.org (2022-01-10)

Merge approved to M98, please merge to branch 4758 before noon PST Tuesday, 11 Jan so this fix can be included in tomorrow's beta cut. Thank you! 

### gi...@appspot.gserviceaccount.com (2022-01-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/940e7df2de6847400f26f59080f4f2ed66535e00

commit 940e7df2de6847400f26f59080f4f2ed66535e00
Author: Clark DuVall <cduvall@chromium.org>
Date: Mon Jan 10 19:38:51 2022

[Merge M98] Fix lifetime bug in PrefetchURLLoader

PrefetchURLLoader is now owned by PrefetchURLLoaderService, which is no
longer refcounted. This makes the lifetime much easier to reason about.

(cherry picked from commit 223e1a1752f3513c4b250bc6b8246256febfe121)

Bug: 1283371
Change-Id: Iaa58c1f44cc9f066459ce344012f57faca533197
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3361198
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Reviewed-by: Kunihiko Sakamoto <ksakamoto@chromium.org>
Commit-Queue: Clark DuVall <cduvall@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#955986}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3378043
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Clark DuVall <cduvall@chromium.org>
Commit-Queue: John Abd-El-Malek <jam@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#473}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/940e7df2de6847400f26f59080f4f2ed66535e00/content/browser/loader/prefetch_url_loader_service.cc
[modify] https://crrev.com/940e7df2de6847400f26f59080f4f2ed66535e00/content/browser/storage_partition_impl.h
[modify] https://crrev.com/940e7df2de6847400f26f59080f4f2ed66535e00/content/browser/loader/prefetch_url_loader_service.h
[modify] https://crrev.com/940e7df2de6847400f26f59080f4f2ed66535e00/content/browser/storage_partition_impl.cc


### am...@chromium.org (2022-01-12)

merge approved for M96 and M97; please merge to branches 4664 and 4692 respectively, before 11am PST, Friday, 14 January, so this fix can be included in the next Extended and Stable security respins - thanks 

### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b70c72fb95dab9d262f37477a7657e7642f16849

commit b70c72fb95dab9d262f37477a7657e7642f16849
Author: Clark DuVall <cduvall@chromium.org>
Date: Thu Jan 13 02:39:02 2022

[Merge M97] Fix lifetime bug in PrefetchURLLoader

PrefetchURLLoader is now owned by PrefetchURLLoaderService, which is no
longer refcounted. This makes the lifetime much easier to reason about.

(cherry picked from commit 223e1a1752f3513c4b250bc6b8246256febfe121)

Bug: 1283371
Change-Id: Iaa58c1f44cc9f066459ce344012f57faca533197
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3361198
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Reviewed-by: Kunihiko Sakamoto <ksakamoto@chromium.org>
Commit-Queue: Clark DuVall <cduvall@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#955986}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3384721
Auto-Submit: Clark DuVall <cduvall@chromium.org>
Commit-Queue: John Abd-El-Malek <jam@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#1426}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/b70c72fb95dab9d262f37477a7657e7642f16849/content/browser/loader/prefetch_url_loader_service.cc
[modify] https://crrev.com/b70c72fb95dab9d262f37477a7657e7642f16849/content/browser/storage_partition_impl.h
[modify] https://crrev.com/b70c72fb95dab9d262f37477a7657e7642f16849/content/browser/loader/prefetch_url_loader_service.h
[modify] https://crrev.com/b70c72fb95dab9d262f37477a7657e7642f16849/content/browser/storage_partition_impl.cc


### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a1f95e4f705d6718fce869eaa9a0879dfd09ef89

commit a1f95e4f705d6718fce869eaa9a0879dfd09ef89
Author: Clark DuVall <cduvall@chromium.org>
Date: Thu Jan 13 04:52:23 2022

[Merge M96] Fix lifetime bug in PrefetchURLLoader

PrefetchURLLoader is now owned by PrefetchURLLoaderService, which is no
longer refcounted. This makes the lifetime much easier to reason about.

(cherry picked from commit 223e1a1752f3513c4b250bc6b8246256febfe121)

Bug: 1283371
Change-Id: Iaa58c1f44cc9f066459ce344012f57faca533197
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3361198
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Reviewed-by: Kunihiko Sakamoto <ksakamoto@chromium.org>
Commit-Queue: Clark DuVall <cduvall@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#955986}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3384742
Auto-Submit: Clark DuVall <cduvall@chromium.org>
Commit-Queue: John Abd-El-Malek <jam@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1397}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/a1f95e4f705d6718fce869eaa9a0879dfd09ef89/content/browser/loader/prefetch_url_loader_service.cc
[modify] https://crrev.com/a1f95e4f705d6718fce869eaa9a0879dfd09ef89/content/browser/storage_partition_impl.h
[modify] https://crrev.com/a1f95e4f705d6718fce869eaa9a0879dfd09ef89/content/browser/loader/prefetch_url_loader_service.h
[modify] https://crrev.com/a1f95e4f705d6718fce869eaa9a0879dfd09ef89/content/browser/storage_partition_impl.cc


### am...@google.com (2022-01-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-14)

Congratulations on another one! The VRP Panel has decided to award you $15,000 for this report. Thank you for your report and great work! 

### am...@google.com (2022-01-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1283371?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader>WebPackaging, Internals>Network]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058368)*
