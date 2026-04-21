# Security: Heap-use-after-free in InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed

| Field | Value |
|-------|-------|
| **Issue ID** | [40061467](https://issues.chromium.org/issues/40061467) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Payments |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | sm...@chromium.org |
| **Created** | 2022-10-25 |
| **Bounty** | $30,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1062625.zip and unzip
2. put poc.html, test.html, pay and web\_manifest.json together and start a HTTPS server
3. run `./chrome --incognito http://localhost/test.html`

**Problem Description:**  

This is caused by the incomplete fix of <https://crbug.com/chromium/1366806>.  

This is the commit that fix <https://crbug.com/chromium/1366806>: <https://chromium-review.googlesource.com/c/chromium/src/+/3920030>  

This problem is introduced in this commit: 21ae413b543e464de8646164d05325f2f86656f7

Now, the dev channel is updated to 108.0.5359.10, so this vulnerability affect the dev channel of chrome. And I've verified that in dev.webm, if you want to verify that, please use test\_dev.html, it refreshes more frequently.  

The Beta channel is updated to 107.0.5304.62, so it is not affected by this vulnerability.

**Additional Comments:**

1. Analysis

As mentioned in <https://crbug.com/chromium/1366806>, `downloader_->DownloadWebAppManifest`[1] can call `PaymentManifestDownloader::InitiateDownload` and reset `this`. And the patch assume that "only the last iteration of the loop can result in a deletion, as `number_of_web_app_manifest_to_download_` must be zero"(1). If the assume is correct, `this` can only be deleted after loop, everything will be OK.

However, I find the implement of this logic is not correct. `number_of_web_app_manifest_to_download_` is added just before `downloader_->DownloadWebAppManifest`. Considering there are two elements in this loop, for the first one, when the code run into `downloader_->DownloadWebAppManifest`, the `number_of_web_app_manifest_to_download_` will be ONE(2), and `number_of_web_app_manifest_to_download_` will be decrease by ONE in `OnPaymentWebAppManifestDownloaded`[2] immediately! If the `content` is empty, `FinishCrawlingPaymentAppsIfReady` will delete `this` because the `number_of_web_app_manifest_to_download_` is already be ZERO(3).  

So, if the `OnPaymentWebAppManifestDownloaded` is executed before traversing the second element, `this` will be deleted and continue running will cause UAF.

```
void InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed(  
    const GURL& method_manifest_url,  
    const GURL& method_manifest_url_after_redirects,  
    const std::string& content,  
    const std::vector<GURL>& default_applications,  
    const std::vector<url::Origin>& supported_origins) {  
  number_of_payment_method_manifest_to_parse_--;  
  
  auto\* rfh = content::RenderFrameHost::FromID(initiator_frame_routing_id_);  
  if (!rfh)  
    return;  
  
  content::PermissionController\* permission_controller =  
      rfh->GetBrowserContext()->GetPermissionController();  
  DCHECK(permission_controller);  
  
  // If there are no valid entries in default_applications, this task will  
  // finish the crawling.  
  PostTaskToFinishCrawlingPaymentAppsIfReady();  
  
  // The `DownloadWebAppManifest()` method may synchronously call  
  // `OnPaymentWebAppManifestDownloaded()`, e.g., if the owning page has gone  
  // away already. This may result in this InstallablePaymentAppCrawler object  
  // to be deleted, so no code should be run after this loop.  
  //  
  // Note that only the last iteration of the loop can result in a deletion, as  
  // `number_of_web_app_manifest_to_download_` must be zero.  
  for (const auto& web_app_manifest_url : default_applications) {   // (1)   
    if (downloaded_web_app_manifests_.find(web_app_manifest_url) !=  
        downloaded_web_app_manifests_.end()) {  
      // Do not download the same web app manifest again since a web app could  
      // be the default application of multiple payment methods.  
      continue;  
    }  
  
    if (!IsSameOriginWith(method_manifest_url_after_redirects,  
                          web_app_manifest_url)) {  
      std::string error_message = base::ReplaceStringPlaceholders(  
          errors::kCrossOriginWebAppManifestNotAllowed,  
          {web_app_manifest_url.spec(),  
           method_manifest_url_after_redirects.spec()},  
          nullptr);  
      SetFirstError(error_message);  
      continue;  
    }  
  
    if (permission_controller  
            ->GetPermissionResultForOriginWithoutContext(  
                blink::PermissionType::PAYMENT_HANDLER,  
                url::Origin::Create(web_app_manifest_url))  
            .status != blink::mojom::PermissionStatus::GRANTED) {  
      // Do not download the web app manifest if it is blocked.  
      continue;  
    }  
  
    number_of_web_app_manifest_to_download_++;   // (2) number_of_web_app_manifest_to_download_ is increased by one   
    downloaded_web_app_manifests_.insert(web_app_manifest_url);  
  
    if (method_manifest_url_after_redirects == web_app_manifest_url) {  
      OnPaymentWebAppManifestDownloaded(  
          method_manifest_url, web_app_manifest_url, web_app_manifest_url,  
          content, /\*error_message=\*/"");  
      continue;  
    }  
  
    // May cause this InstallablePaymentAppCrawler object to be synchronously  
    // deleted.  
    downloader_->DownloadWebAppManifest(  
        url::Origin::Create(method_manifest_url_after_redirects),  
        web_app_manifest_url,  
        base::BindOnce(  
            &InstallablePaymentAppCrawler::OnPaymentWebAppManifestDownloaded,  
            weak_ptr_factory_.GetWeakPtr(), method_manifest_url,  
            web_app_manifest_url));  
  }  
}  

```
```
void InstallablePaymentAppCrawler::OnPaymentWebAppManifestDownloaded(  
    const GURL& method_manifest_url,  
    const GURL& web_app_manifest_url,  
    const GURL& web_app_manifest_url_after_redirects,  
    const std::string& content,  
    const std::string& error_message) {  
#if DCHECK_IS_ON()  
  GURL::Replacements replacements;  
  if (ignore_port_in_origin_comparison_for_testing_)  
    replacements.ClearPort();  
  
  // Enforced in PaymentManifestDownloader.  
  DCHECK_EQ(  
      web_app_manifest_url.ReplaceComponents(replacements),  
      web_app_manifest_url_after_redirects.ReplaceComponents(replacements));  
#endif  // DCHECK_IS_ON()  
  
  number_of_web_app_manifest_to_download_--;  
  if (content.empty()) {  
    SetFirstError(error_message);  
    FinishCrawlingPaymentAppsIfReady(); //(3) FinishCrawlingPaymentAppsIfReady will delete this  
    return;  
  }  
[...]  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/installable_payment_app_crawler.cc;l=217;drc=7f00d813a79f51a6c77797cdaa33b56cce340a33;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/installable_payment_app_crawler.cc;l=244;drc=7f00d813a79f51a6c77797cdaa33b56cce340a33;bpv=0;bpt=0>

2. POC  
   
   To get more than one element in `default_applications`, I use my onw `pay` and `web_manifest.json` file. You can see that in file `pay`, there are many `default_applications`.
3. Patch  
   
   I think `number_of_web_app_manifest_to_download_` should be assigned the size of `default_applications`, and decrease it in `OnPaymentWebAppManifestDownloaded` or when the loop continue.

```
diff --git a/components/payments/content/installable_payment_app_crawler.cc b/components/payments/content/installable_payment_app_crawler.cc  
index 8d629a8a04220..dc11de3ad6f10 100644  
--- a/components/payments/content/installable_payment_app_crawler.cc  
+++ b/components/payments/content/installable_payment_app_crawler.cc  
@@ -174,11 +174,13 @@ void InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed(  
   //  
   // Note that only the last iteration of the loop can result in a deletion, as  
   // `number_of_web_app_manifest_to_download_` must be zero.  
+  number_of_web_app_manifest_to_download_ = default_applications.size();  
   for (const auto& web_app_manifest_url : default_applications) {  
     if (downloaded_web_app_manifests_.find(web_app_manifest_url) !=  
         downloaded_web_app_manifests_.end()) {  
       // Do not download the same web app manifest again since a web app could  
       // be the default application of multiple payment methods.  
+      number_of_web_app_manifest_to_download_--;    
       continue;  
     }  
   
@@ -190,6 +192,7 @@ void InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed(  
            method_manifest_url_after_redirects.spec()},  
           nullptr);  
       SetFirstError(error_message);  
+      number_of_web_app_manifest_to_download_--;    
       continue;  
     }  
   
@@ -199,16 +202,17 @@ void InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed(  
                 url::Origin::Create(web_app_manifest_url))  
             .status != blink::mojom::PermissionStatus::GRANTED) {  
       // Do not download the web app manifest if it is blocked.  
+      number_of_web_app_manifest_to_download_--;    
       continue;  
     }  
   
-    number_of_web_app_manifest_to_download_++;  
     downloaded_web_app_manifests_.insert(web_app_manifest_url);  
   
     if (method_manifest_url_after_redirects == web_app_manifest_url) {  
       OnPaymentWebAppManifestDownloaded(  
           method_manifest_url, web_app_manifest_url, web_app_manifest_url,  
           content, /\*error_message=\*/"");  
+      number_of_web_app_manifest_to_download_--;    
       continue;  
     }  
  

```

\*\*Chrome version: \*\* 108.0.5359.10 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 722 B)
- [test.html](attachments/test.html) (text/plain, 276 B)
- [pay](attachments/pay) (text/plain, 6.8 KB)
- [web_manifest.json](attachments/web_manifest.json) (text/plain, 326 B)
- [test_dev.html](attachments/test_dev.html) (text/plain, 275 B)
- [asan.webm](attachments/asan.webm) (video/webm, 244.9 KB)
- [dev.webm](attachments/dev.webm) (video/webm, 675.2 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 56.8 KB)

## Timeline

### [Deleted User] (2022-10-25)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-10-25)

Rouslan, could you PTAL? Thanks.

[Monorail components: Blink>Payments]

### [Deleted User] (2022-10-25)

[Empty comment from Monorail migration]

### ro...@google.com (2022-10-25)

+cc for visibility

### ro...@google.com (2022-10-25)

M108 beta promotion is scheduled for this week.

### sm...@google.com (2022-10-25)

[Empty comment from Monorail migration]

### sm...@google.com (2022-10-25)

[Empty comment from Monorail migration]

### sm...@chromium.org (2022-10-26)

Thanks OP for the report, and for continuing to dig at this troublesome area of code!

Rouslan and I will be working to confirm and then address this today. If confirmed, I believe this will need to block M108 beta, so cc release TPMs for 108. srinivassista@, govind@, please confirm I have the right labels applied for that (I added M-108, ReleaseBlock-Beta, and ReleaseBlock-Stable just to be safe - though we are weeks away from M108 stable).

### sm...@chromium.org (2022-10-26)

We believe we have confirmed the report and reproduced the UAF, and are working on a fix and accompanying tests. 

### go...@chromium.org (2022-10-26)

For Android, we already cut M108 Beta RC for release tomorrow. Is this bug applicable to Android and other OSs or just Linux?

+Amy (Security TPM)

### sm...@chromium.org (2022-10-26)

Apologies, fixed the OS list. This bug affects all OSes except iOS.

### sm...@chromium.org (2022-10-26)

WIP CL: https://chromium-review.googlesource.com/c/chromium/src/+/3983012

### am...@chromium.org (2022-10-26)

re: https://crbug.com/chromium/1378286#c8 and https://crbug.com/chromium/1378286#c10, yes, unfortunately all points point to this being a critical severity issue introduced in 108, and as a high+ severity security regression, all points point to this being a release blocker for 108 beta 

### sr...@google.com (2022-10-26)

rouslan@ can you help get the CL landed on trunk asap ( https://crbug.com/chromium/1378286#c12) and ping us so we can merge to latest canary branch and trigger a new canary build. Once we verify this change is working on canary , we will merge to M108 asap so we can recut beta build for M108, since this is a critical regression we are postponing beta promotion for all platforms by a day., so can you help get the reviews and land the CL asap to trunk

### ro...@google.com (2022-10-26)

> rouslan@ can you help 

OK.

### sm...@chromium.org (2022-10-26)

CL has CR+2 and is dry-running currently. I plan to land it once the dry-run completes.

### [Deleted User] (2022-10-26)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c5c1f9cf8c9a715c481ece9fdf87efb7b2c149cc

commit c5c1f9cf8c9a715c481ece9fdf87efb7b2c149cc
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Wed Oct 26 17:14:35 2022

[Web Payments] Avoid early deletion of crawler for 2+ web app manifests

The previous fix[0] overlooked that
number_of_payment_method_manifest_to_download_ could be synchronously
reduced to 0 during the loop, as opposed to only in the last iteration.
This CL corrects that, by pre-allocating
number_of_payment_method_manifest_to_download_ ahead of the loop and
decrementing it every loop iteration. As such, only the last iteration
should be able to have it reduced to zero.

[0]: https://chromium-review.googlesource.com/c/chromium/src/+/3920030

Bug: 1378286
Change-Id: Ia2857a0775dc12aca1a83b3f3087836c9caad168
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3983012
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1063872}

[modify] https://crrev.com/c5c1f9cf8c9a715c481ece9fdf87efb7b2c149cc/components/payments/content/installable_payment_app_crawler.cc
[modify] https://crrev.com/c5c1f9cf8c9a715c481ece9fdf87efb7b2c149cc/chrome/browser/payments/service_worker_payment_app_finder_browsertest.cc


### sm...@chromium.org (2022-10-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/be6a50c2c03fec04bf04682b0f4509a1ac335f10

commit be6a50c2c03fec04bf04682b0f4509a1ac335f10
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Wed Oct 26 17:27:14 2022

[Web Payments] Avoid early deletion of crawler for 2+ web app manifests

The previous fix[0] overlooked that
number_of_payment_method_manifest_to_download_ could be synchronously
reduced to 0 during the loop, as opposed to only in the last iteration.
This CL corrects that, by pre-allocating
number_of_payment_method_manifest_to_download_ ahead of the loop and
decrementing it every loop iteration. As such, only the last iteration
should be able to have it reduced to zero.

[0]: https://chromium-review.googlesource.com/c/chromium/src/+/3920030

(cherry picked from commit c5c1f9cf8c9a715c481ece9fdf87efb7b2c149cc)

Bug: 1378286
Change-Id: Ia2857a0775dc12aca1a83b3f3087836c9caad168
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3983012
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1063872}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3982794
Reviewed-by: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5383@{#4}
Cr-Branched-From: 43400687887852cce02f5cccc703d60844f60398-refs/heads/main@{#1063734}

[modify] https://crrev.com/be6a50c2c03fec04bf04682b0f4509a1ac335f10/components/payments/content/installable_payment_app_crawler.cc
[modify] https://crrev.com/be6a50c2c03fec04bf04682b0f4509a1ac335f10/chrome/browser/payments/service_worker_payment_app_finder_browsertest.cc


### go...@chromium.org (2022-10-26)

Merged the fix to canary branch 5383 (https://chromium-review.googlesource.com/c/chromium/src/+/3982794) and triggered a new canary #109.0.5383.3 (currently building) for Android and Desktop.

M108 branch 5359 merge in CQ dry run (https://chromium-review.googlesource.com/c/chromium/src/+/3983496).

Requesting a postmortem for this as this  requires to recut M108 Beta RC and blocking beta promotion tomorrow. 

### sm...@chromium.org (2022-10-26)

Thanks govind@

> Requesting a postmortem for this as this  requires to recut M108 Beta RC and blocking beta promotion tomorrow.

Absolutely, we had already planned this on our side. Can you confirm if we should be using go/chrome-postmortem-template (given 'use this template if you’re writing a postmortem for a security-releated incident') or the newer process described at go/chrome-postmortem ?

### go...@chromium.org (2022-10-26)

Thank you, smcgrer@.  
Please follow the newer process described at go/chrome-postmortem. But would like amyressler@ to chime in if there is a separate process for security postmortem.

### go...@chromium.org (2022-10-26)

Previous canary failed to trigger so please verify this change on canary version 109.0.5383.4+. 


### ro...@google.com (2022-10-26)

My Canary is on 109.0.5382.1. Is there an ETA for when 109.0.5383.4+ is out?

### go...@chromium.org (2022-10-26)

Re #25,  ETA for Desktop canary ~5 hrs, Android canary ~8 hrs. 

### sr...@google.com (2022-10-26)

desktop should be out well before the 5hrs, usually takes 2-3 hrs for windows or mac, build has been going for an hour already, so expect it to be available by 2:30 pm PST

### sm...@chromium.org (2022-10-27)

Starting verification. Plan will be to verify that general PaymentHandler functionality still appears correct on Chrome Canary (MacOS, Android as available test platforms for me), and to verify that ASAN builds from https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1064254.zip?generation=1666869782418260&alt=media before/after the fix do/don't reproduce the UAF.

### sm...@chromium.org (2022-10-27)

Chrome MacOS 109.0.5383.4 (Official Build) canary (x86_64) 

- Cleared all browser data, to (I believe) uninstall any existing service worker PaymentHandlers
- Visited https://accounts.google.com, logged into Google accouunt
- Visited https://developers.google.com/pay/api/web/guides/resources/demos and tried Google Pay flow - success (appeared to install Google Pay payment handler)
- Visited https://rsolomakhin.github.io/pr/payjs/ and tried Google Pay flow - success
- Visited https://rsolomakhin.github.io/pr/bob/ and tried Bob Pay flow - success

Chrome MacOS general PaymentHandler functionality looks correct, at least in 'good' cases.

### sm...@chromium.org (2022-10-27)

Chrome Android 109.0.5383.4 (Official Build) canary (64-bit)

- Cleared all app data, to (I believe) uninstall any existing service worker PaymentHandlers
- Opened Canary, did initial setup flow (turn on sync, etc)
- Visited https://developers.google.com/pay/api/web/guides/resources/demos and tried Google Pay flow - success (showed GMSCore overlay)
- Visited https://rsolomakhin.github.io/pr/payjs/ and tried Google Pay flow - success
- Visited https://rsolomakhin.github.io/pr/bob/ and tried Bob Pay flow - success (appeared to install BobPay web payment handler)

Unable to test BobPay native PaymentHandler from https://bobbucks.dev/ as phone doesn't allow direct apk install - rouslan@ can you test this?

Chrome Android general PaymentHandler functionality looks correct, at least in 'good' cases.

### sm...@chromium.org (2022-10-27)

ASAN Reproduction: So far unable to reproduce with a hosted version of the OP's repro. (Temporarily hosted at https://rsolomakhin.github.io/pr/1378286/test_dev.html). This is likely due to timing issues, as we were able to reproduce the UAF via C++ browser tests and believe that a website *could* trigger it if the timing was right, but does mean its hard to verify the fix outside of the C++ browser tests.

We are continuing to work on trying to reproduce:

~/Downloads/asan-linux-release-1062625/chrome https://rsolomakhin.github.io/pr/1378286/test_dev.html

(And once we do, will then verify that a newer asan release with the fix **doesn't** reproduce)

### sm...@chromium.org (2022-10-27)

We continue to be unable to reproduce this using web-platform means (i.e. the reporters original repro html) unfortunately. As noted above however, we are reasonably confident that:

- A UAF existed (confirmed via code analysis and new browser tests)
- It should be fixed (confirmed via same browser tests)
- It would have been possible to trigger via a website navigating an iframe (though the timing seems very tight)

We are also fairly confident that the fix hasn't broken PaymentHandler either, based on smoke tests on Canary builds.

As such, marking Fixed. We should merge to M108 imo (govind@ - will you take lead on this?), and start on the postmortem on our side.

### sm...@chromium.org (2022-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-27)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@chromium.org (2022-10-27)

https://crbug.com/chromium/1378286#c34 looks to me like sheriffbot is confusing M102 (the current LTS release) and M108 (the upcoming LTS channel).

I don't *think* a specific merge to LTS will be required, because this should merge into M108 before LTS is cut I assume?

### go...@chromium.org (2022-10-27)

Re #32, sure i can submit M108 merge - https://chromium-review.googlesource.com/c/chromium/src/+/3983496 after amyressler@ (Security TPM) review and approval. Thank you. 

### [Deleted User] (2022-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-27)

Merge review required: M108 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2022-10-27)

> 1. Why does your merge fit within the merge criteria for these milestones?

Security bug fix.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

https://crrev.com/c5c1f9cf8c9a715c481ece9fdf87efb7b2c149cc

> 3. Have the changes been released and tested on canary?

Yes and yes.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

Not a new feature.

> 5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

N/A

### [Deleted User] (2022-10-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-27)

Thank you for prompt attention and the fast fix, Stephen and your very thorough analysis and follow up displayed in comments # 30-21. 
M108 merge approved, please go ahead and merge this fix to branch 5359 as soon as possible. Thank you! 

### go...@chromium.org (2022-10-27)

Thank you Stephen and Amy.

M108 branch 5359 merge in CQ: https://chromium-review.googlesource.com/c/chromium/src/+/3983496

### gi...@appspot.gserviceaccount.com (2022-10-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca1ff978f0bdeeedc883f293afa7ce443e9c1eb4

commit ca1ff978f0bdeeedc883f293afa7ce443e9c1eb4
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Thu Oct 27 20:22:17 2022

[Web Payments] Avoid early deletion of crawler for 2+ web app manifests

The previous fix[0] overlooked that
number_of_payment_method_manifest_to_download_ could be synchronously
reduced to 0 during the loop, as opposed to only in the last iteration.
This CL corrects that, by pre-allocating
number_of_payment_method_manifest_to_download_ ahead of the loop and
decrementing it every loop iteration. As such, only the last iteration
should be able to have it reduced to zero.

[0]: https://chromium-review.googlesource.com/c/chromium/src/+/3920030

(cherry picked from commit c5c1f9cf8c9a715c481ece9fdf87efb7b2c149cc)

(cherry picked from commit c8cf0673b7740f637ccbabb69e19cd7a413f6055)

Bug: 1378286
Change-Id: Ia2857a0775dc12aca1a83b3f3087836c9caad168
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3983012
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1063872}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3982794
Reviewed-by: Krishna Govind <govind@chromium.org>
Owners-Override: Krishna Govind <govind@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Original-Commit-Position: refs/branch-heads/5383@{#4}
Cr-Original-Branched-From: 43400687887852cce02f5cccc703d60844f60398-refs/heads/main@{#1063734}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3983496
Commit-Queue: Krishna Govind <govind@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#364}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/ca1ff978f0bdeeedc883f293afa7ce443e9c1eb4/components/payments/content/installable_payment_app_crawler.cc
[modify] https://crrev.com/ca1ff978f0bdeeedc883f293afa7ce443e9c1eb4/chrome/browser/payments/service_worker_payment_app_finder_browsertest.cc


### rz...@google.com (2022-10-28)

[Empty comment from Monorail migration]

### rz...@google.com (2022-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-28)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-10-28)

1. https://crrev.com/c/3990825
2. Low, minor conflicts with a function and a test class not present in M102
3. 108, 109
4. Yes

### sm...@chromium.org (2022-10-28)

I'm not sure a merge to LTS 102 is needed or wise here. The commit that introduced the UAF in the first place - https://chromium.googlesource.com/chromium/src/+/21ae413b543e464de8646164d05325f2f86656f7 - should not be present in M102 afaik, and so applying a merge fix seems unnecessary (and thus risky) to me? The proposed merge also skips the previous (partial) fix - https://chromium-review.googlesource.com/c/chromium/src/+/3920030 - which is part of why it doesn't apply cleanly.

### gm...@google.com (2022-10-28)

Per https://crbug.com/chromium/1378286#c35 and https://crbug.com/chromium/1378286#c48, tagging this as not Applicable for LTS-102.

### ro...@google.com (2022-10-31)

The post-mortem is at http://irm/i_ofbkcu5f1DMuaa7EiTNQ.

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations, Krace! Nice Finding! The VRP Panel has decided to award you $30,000 for this report + $2,000 bisect bonus for a total VRP reward of $32,000. Thank you for you efforts in discovering and reporting this issue to us. Excellent work! 

### me...@gmail.com (2022-11-03)

[Comment Deleted]

### am...@chromium.org (2022-11-03)

Hi Weipeng Jiang! Thanks for calling our attention to that and apologies we missed that the first time around. Your new reward amount is $39,000 ($30,000 + $7,000 RCE bonus + $2,000 bisect bonus)! 

### me...@gmail.com (2022-11-03)

Thank you:)

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@google.com (2023-03-29)

[Empty comment from Monorail migration]

### is...@google.com (2023-03-29)

This issue was migrated from crbug.com/chromium/1378286?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061467)*
