# Security: Heap-use-after-free in InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed

| Field | Value |
|-------|-------|
| **Issue ID** | [40061095](https://issues.chromium.org/issues/40061095) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Payments |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2022-09-22 |
| **Bounty** | $30,000.00 |

## Description

**Steps to reproduce the problem:**  

repro:

1. download asan-linux-release-1048965.zip and unzip
2. start a server at the folder of poc.html and test.html: `python -m SimpleHTTPServer 8605`
3. run `./chrome --incognito http://127.0.0.1:8605/test.html`  
   
   If you cannot reproduce it, please refresh test.html to try again.

**Problem Description:**  

This is introduced by this commit 21ae413b543e464de8646164d05325f2f86656f7

Note that this UAF doesn't need any flag or user interactions, so I think it should be a critical issue.

**Additional Comments:**

1. Analysis

In this commit 21ae413b543e464de8646164d05325f2f86656f7, a new check is added to function `PaymentManifestDownloader::InitiateDownload(`[1], the `csp_checker_`(1). If this `csp_checker_` is null, then it will call `RespondWithError`[2], this will run callback directly.

```
void PaymentManifestDownloader::InitiateDownload(  
    const url::Origin& request_initiator,  
    const GURL& url,  
    const GURL& url_before_redirects,  
    bool did_follow_redirect,  
    Download::Type download_type,  
    int allowed_number_of_redirects,  
    PaymentManifestDownloadCallback callback) {  
  DCHECK(UrlUtil::IsValidManifestUrl(url));  
  
[...]  
  auto download = std::make_unique<Download>();  
  download->request_initiator = request_initiator;  
  download->type = download_type;  
  download->original_url = url;  
  download->url_before_redirects = url_before_redirects;  
  download->did_follow_redirect = did_follow_redirect;  
  download->loader = std::move(loader);  
  download->callback = std::move(callback);  
  download->allowed_number_of_redirects = allowed_number_of_redirects;  
  
  if (!csp_checker_) {  // Can be null when the webpage closes.  
    RespondWithError(errors::kPaymentManifestDownloadFailed,  // (1) if csp_checker_ is null, `download->callback` will run immediately.  
                     download->original_url, \*log_,  
                     std::move(download->callback));  
    return;  
  }  
  
  csp_checker_->AllowConnectToSource(  
      url, url_before_redirects, did_follow_redirect,  
      base::BindOnce(&PaymentManifestDownloader::OnCSPCheck,  
                     weak_ptr_factory_.GetWeakPtr(), std::move(download)));  
}  

```
```
void RespondWithError(const base::StringPiece& error_format,  
                      const GURL& final_url,  
                      const ErrorLogger& log,  
                      PaymentManifestDownloadCallback callback) {  
  std::string error_message = base::ReplaceStringPlaceholders(  
      error_format, {final_url.spec()}, nullptr);  
  log.Error(error_message);  
  std::move(callback).Run(final_url, std::string(), error_message); // (5) this will run callback with empty `content`  
}  

```

For this issue, when we call function `InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed`[3], it will call `DownloadWebAppManifest`(2), and pass the callback `OnPaymentWebAppManifestDownloaded`(3). `DownloadWebAppManifest` will call `PaymentManifestDownloader::InitiateDownload`[1], so if `csp_checker_` is null, `OnPaymentWebAppManifestDownloaded` will run immediately.

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
  
  for (const auto& web_app_manifest_url : default_applications) {  
[...]  
    downloader_->DownloadWebAppManifest(   // (2) this will call `PaymentManifestDownloader::InitiateDownload` AND reset `this`  
        url::Origin::Create(method_manifest_url_after_redirects),  
        web_app_manifest_url,  
        base::BindOnce(  
            &InstallablePaymentAppCrawler::OnPaymentWebAppManifestDownloaded,  //(3) if csp_checker_ is null, this callback will run immediately  
            weak_ptr_factory_.GetWeakPtr(), method_manifest_url,  
            web_app_manifest_url));  
  }  
  FinishCrawlingPaymentAppsIfReady();  // (6)  `this` may has been reset before here.  
}  
  

```

In function `InstallablePaymentAppCrawler::OnPaymentWebAppManifestDownloaded`[4], if the `content`(4) is empty(`RespondWithError` will run ``InstallablePaymentAppCrawler::OnPaymentWebAppManifestDownloaded`with an empty`content`(5)), `FinishCrawlingPaymentAppsIfReady()` will be called, which will run `finished\_using\_resources\_` callback.

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
  if (content.empty()) {   // (4) if this function is called by `RespondWithError`, `content` will be empty.  
    SetFirstError(error_message);  
    FinishCrawlingPaymentAppsIfReady();  
    return;  
  }  
[...]  

```

`finished_using_resources_` callback is initialized in function `OnPaymentAppsVerified`[5]. The `finished_using_resources_` is assigned as `&SelfDeletingServiceWorkerPaymentAppFinder::OnPaymentAppsCrawlerFinishedUsingResources`[6].  

And `SelfDeletingServiceWorkerPaymentAppFinder::OnPaymentAppsCrawlerFinishedUsingResources` will reset the `crawler_` directly! This `crawler_` is the class where we run `InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed`[3]. So when the code continue running, it will use the freed memory(6).

```
    if ((installed_apps_.empty() ||  
         !method_manifest_urls_for_icon_refetch.empty()) &&  
        crawler_ != nullptr) {  
      // Crawls installable web payment apps if no web payment apps have been  
      // installed or when an installed app is missing an icon.  
      is_payment_app_crawler_finished_using_resources_ = false;  
      crawler_->Start(  
          requested_method_data_,  
          std::move(method_manifest_urls_for_icon_refetch),  
          base::BindOnce(  
              &SelfDeletingServiceWorkerPaymentAppFinder::OnPaymentAppsCrawled,  
              weak_ptr_factory_.GetWeakPtr()),  
          base::BindOnce(&SelfDeletingServiceWorkerPaymentAppFinder::  
                             OnPaymentAppsCrawlerFinishedUsingResources,  // `finished_using_resources_` is assigned here  
                         weak_ptr_factory_.GetWeakPtr()));  
      return;  
    }  

```
```
  void OnPaymentAppsCrawlerFinishedUsingResources() {  
    crawler_.reset();  
  
    is_payment_app_crawler_finished_using_resources_ = true;  
    FinishUsingResourcesIfReady();  
  }  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/core/payment_manifest_downloader.cc;l=387;drc=21ae413b543e464de8646164d05325f2f86656f7;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/core/payment_manifest_downloader.cc;l=46;bpv=1;bpt=0;drc=21ae413b543e464de8646164d05325f2f86656f7>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/installable_payment_app_crawler.cc;l=208;bpv=1;bpt=0;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/installable_payment_app_crawler.cc;l=237;bpv=1;bpt=0;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd>  

[5] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/service_worker_payment_app_finder.cc;l=229;drc=21ae413b543e464de8646164d05325f2f86656f7;bpv=0;bpt=0>  

[6] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/service_worker_payment_app_finder.cc;l=309;drc=5e23336d543816202a70de6dc6cdf721350adf22;bpv=0;bpt=0>

2. POC  
   
   `csp_checker_` is weakPtr in `PaymentManifestDownloader`, and is owned by `ServiceWorkerPaymentAppFinder`, `ServiceWorkerPaymentAppFinder` is bound to `content::DocumentUserData`, so we can refresh the frame to free it. You can see the poc.html and test.html for more info.

```
class ServiceWorkerPaymentAppFinder  
    : public content::DocumentUserData<ServiceWorkerPaymentAppFinder> {  

```

[7] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/service_worker_payment_app_finder.h;l=41;bpv=1;bpt=0;drc=21ae413b543e464de8646164d05325f2f86656f7>

3. Supplement  
   
   Besides, `InstallablePaymentAppCrawler::OnPaymentMethodManifestDownloaded`[8] has a similar logic with `InstallablePaymentAppCrawler::OnPaymentWebAppManifestDownloaded`[4], which could also call `FinishCrawlingPaymentAppsIfReady()`. So it could also be used to trigger this UAF.

[8] <https://source.chromium.org/chromium/chromium/src/+/main:components/payments/content/installable_payment_app_crawler.cc;l=139;drc=8ba1bad80dc22235693a0dd41fe55c0fd2dbdabd;bpv=0;bpt=0>

\*\*Chrome version: \*\* 108 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [test.html](attachments/test.html) (text/plain, 750 B)
- [poc.html](attachments/poc.html) (text/plain, 723 B)
- [poc.webm](attachments/poc.webm) (video/webm, 557.9 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 55.9 KB)
- [asan-error.txt](attachments/asan-error.txt) (text/plain, 56.0 KB)

## Timeline

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-23)

I am not able to repro with these instructions, but as there's a mention of a specific CL, bringing the CL author in to take a look.

rouslan@, can you take a quick look?

[Monorail components: Blink>Payments]

### [Deleted User] (2022-09-23)

[Empty comment from Monorail migration]

### ro...@google.com (2022-09-23)

Will work on a fix.

### hc...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-09-24)

Hi hchao@ and rouslan@, if you cannot repro this UAF, please consider that:
1. Your computer should be able to access the 'https://google.com/pay', because you need to download the manifest file from it.
2. Considering that your different download speed, the timeout in `test.html` maybe need to be adjust. Here I use 2.5s-3.4s, perhaps you could adjust the timeout from 1.0s-2.0s or 2s-3s or 3s-4s to see if you can repro it.

BTW, this browser UAF doesn't need a compromised render or any user interactions, could you please set it's Severity to Critical according to the rules[1]?
Thank you!

[1] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#TOC-Critical-severity

### [Deleted User] (2022-09-24)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-24)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-24)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2022-09-26)

CC-ing for visibility.

### ro...@google.com (2022-09-26)

Reproduced in developer build with the reporter's provided test.html and poc.html after 3 refreshes. Had to reduce their timeout value by 1 second as the reporter recommended.

GN args:
  is_debug = false
  use_goma = true
  is_asan = true
  is_component_build = true

Server start command: `python -m http.server 8605`
Chrome command: `out/asan/chrome --incognito http://127.0.0.1:8605/test.html`

### ro...@google.com (2022-09-26)

==1050265==ERROR: AddressSanitizer: heap-use-after-free on address 0x6130003cc2d8 at pc 0x55968d9b3fbf bp 0x7ffce71d37d0 sp 0x7ffce71d37c8
READ of size 8 at 0x6130003cc2d8 thread T0 (chrome)
    #0 0x55968d9b3fbe in payments::InstallablePaymentAppCrawler::FinishCrawlingPaymentAppsIfReady() components/payments/content/installable_payment_app_crawler.cc:522:7

Code at this line:

void InstallablePaymentAppCrawler::FinishCrawlingPaymentAppsIfReady() {          
  if (number_of_payment_method_manifest_to_download_ != 0 ||                     
      number_of_payment_method_manifest_to_parse_ != 0 ||                        
      number_of_web_app_manifest_to_download_ != 0 ||                            
      number_of_web_app_manifest_to_parse_ != 0 ||                               
      number_of_web_app_icons_to_download_and_decode_ != 0) {                    
    return;                                                                      
  } 

If the line # is accurate, 522:7 is reading of member variable `number_of_payment_method_manifest_to_download_`, which would indicate that InstallablePaymentAppCrawler has been already deleted.

### ro...@google.com (2022-09-26)

0x6130003cc2d8 is located 152 bytes inside of 336-byte region [0x6130003cc240,0x6130003cc390)
freed by thread T0 (chrome) here:
    #0 0x55968483a3cd in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x55968d99645c in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:49:5
    #2 0x55968d99645c in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:281:7
    #3 0x55968d99645c in payments::(anonymous namespace)::SelfDeletingServiceWorkerPaymentAppFinder::OnPaymentAppsCrawlerFinishedUsingResources() components/payments/content/service_worker_payment_app_finder.cc:309:14

Code at service_worker_payment_app_finder.cc:309:

  void OnPaymentAppsCrawlerFinishedUsingResources() {                            
    crawler_.reset(); 

Indeed, it is the `crawler_` (an instance of InstallablePaymentAppCrawler) that has been deleted.

### ro...@google.com (2022-09-26)

Allocation stack trace, truncated for clarity:

previously allocated by thread T0 (chrome) here:
    ...
    #1 0x55968d98fc0b in make_unique<payments::InstallablePaymentAppCrawler>
    #2 0x55968d98fc0b in GetAllPaymentApps components/payments/content/service_worker_payment_app_finder.cc:121:18
    #3 0x55968d98fc0b in payments::ServiceWorkerPaymentAppFinder::GetAllPaymentApps() components/payments/content/service_worker_payment_app_finder.cc:418:24
    #4 0x55968d930bd4 in payments::ServiceWorkerPaymentAppFactory::Create() components/payments/content/service_worker_payment_app_factory.cc:190:9
    #5 0x55968d92f2f0 in payments::PaymentAppService::Create() components/payments/content/payment_app_service.cc:52:14
    #6 0x55968d911c89 in payments::PaymentRequestState::PaymentRequestState() components/payments/content/payment_request_state.cc:91:12
    #7 0x55968d8b12fb in std::Cr::__unique_if<payments::PaymentRequestState> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:670:30
    #8 0x55968d8ae960 in payments::PaymentRequest::Init()

### me...@gmail.com (2022-09-26)

Hi rouslan@, since you can repro this issue, could you please consider the severity I mentioned in https://crbug.com/chromium/1366806#c6?  
Thank you.

### ro...@google.com (2022-09-26)

[Comment Deleted]

### ro...@google.com (2022-09-26)

UAF explanation, to the best of my understanding:

1) InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed() calls
                       PaymentManifestDownloader::DownloadWebAppManifest()

    1.1) PaymentManifestDoandlower::DownloadWebAppManifest() immediately calls back into
                       InstallablePaymentAppCrawler::OnPaymentWebAppManifestDownloaded()
                       with empty contents because of null `csp_checker_`.

    1.2) InstallablePaymentAppCrawler::OnPaymentWebAppManifestDownloaded() calls into
                       InstallablePaymentAppCrawler::FinishCrawlingPaymentAppsIfReady()
                       because of the empty `contents`.

    1.3) InstallablePaymentAppCrawler::FinishCrawlingPaymentAppsIfReady() invokes
                       the `finished_using_resouces_` callback.

    1.4) The `callback_` is  SelfDeletingServiceWorkerPaymentAppFinder::
                       OnPaymentAppsCrawlerFinishedUsingResources().

    1.5) SelfDeletingServiceWorkerPaymentAppFinder::
                      OnPaymentAppsCrawlerFinishedUsingResources,() DELETES
                      the InstallablePaymentAppCrawler via `crawler_.reset()` statement.

2) InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed() calls
                     InstallablePaymentAppCrawler::FinishCrawlingPaymentAppsIfReady(),
                     which accesses its member variables on `this`, which is a UAF.

(Reposted with better formatting.)

### ro...@google.com (2022-09-26)

> Hi rouslan@, since you can repro this issue, could you please consider the severity I mentioned in https://crbug.com/chromium/1366806#c6?  

Let's let the security team (e.g.,  hchao@) consider the severity level, if you don't mind? :-D

### me...@gmail.com (2022-09-26)

[Comment Deleted]

### sm...@chromium.org (2022-09-26)

Thanks Rouslan for the work you're doing here. I suspect this may be the root cause of https://crbug.com/chromium/1366503, but since this is more concrete let us work on it here and fix it, then see if https://crbug.com/chromium/1366503 resolves.

### sm...@chromium.org (2022-09-26)

https://crbug.com/chromium/1366806#c17 makes sense to me. InstallablePaymentAppCrawler::OnPaymentMethodManifestParsed has that call to handle the case where |default_applications| is empty or none of them are valid (e.g., blocked, etc), but it doesn't expect a synchronous deletion of its own object.

The overall lifecycle of SelfDeletingServiceWorkerPaymentAppFinder seems quite dangerous and something we should look at in the future, but hopefully we can get a targeted fix in for this case. 

### ro...@google.com (2022-09-26)

The reason for difficulty to reproduce this bug is due to `PaymentManifestDownloader::csp_checker_` having to be reset to null after PaymentManifestDownloader::DownloaderPaymentMethodManifest(), but before PaymentManifestDownloader::DownloadWebAppManifest(). That is a short period of time.

### ro...@google.com (2022-09-26)

Patch Set #1 @ https://crrev.com/c/3920030 reliably reproduces the UAF in ASAN builds:

1 test crashed:
    Test/ServiceWorkerPaymentAppFinderCSPCheckerBrowserTest.CSPCheckerResetDoestNotCrash/2 (../../chrome/browser/payments/service_worker_payment_app_finder_browsertest.cc:892)

There is no fix in that patch set yet.

### gi...@appspot.gserviceaccount.com (2022-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7f00d813a79f51a6c77797cdaa33b56cce340a33

commit 7f00d813a79f51a6c77797cdaa33b56cce340a33
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Tue Sep 27 23:40:41 2022

[Web Payment] Handle CSP checker going away.

Cq-Include-Trybots: luci.chromium.try:linux_chromium_asan_rel_ng,mac_chromium_asan_rel_ng,win-asan
Bug: 1366806
Change-Id: I3a99800b829dd53d268027d30f52186f730b9e10
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3920030
Reviewed-by: Stephen McGruer <smcgruer@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1052116}

[modify] https://crrev.com/7f00d813a79f51a6c77797cdaa33b56cce340a33/components/payments/core/const_csp_checker.h
[modify] https://crrev.com/7f00d813a79f51a6c77797cdaa33b56cce340a33/components/payments/content/installable_payment_app_crawler.cc
[modify] https://crrev.com/7f00d813a79f51a6c77797cdaa33b56cce340a33/components/payments/content/installable_payment_app_crawler.h
[modify] https://crrev.com/7f00d813a79f51a6c77797cdaa33b56cce340a33/components/payments/core/const_csp_checker.cc
[modify] https://crrev.com/7f00d813a79f51a6c77797cdaa33b56cce340a33/chrome/browser/payments/service_worker_payment_app_finder_browsertest.cc


### sm...@chromium.org (2022-09-28)

The above CL should be available as of 108.0.5327.0, which is now in Canary on Windows, Mac, and Android. 

I believe the latest asan-releases builds should also already have it (52339.zip appears to be https://chromium.googlesource.com/chromium/src/+/d607e010819c36b4060a374bd031d71d56d62b8a which is after the above CL), but have not explicitly confirmed this.

### ro...@google.com (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-10-05)

[vrp panel] Nice Catch! Very cool bug!

### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-07)

Congratulations, Weipeng Jiang! The VRP Panel has decided to award you $30,000 + $7,000 renderer RCE bonus + $1,000 bisect bonus for a total of $38,000 for this report. Really neat bug, great find, and excellent report! Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### me...@gmail.com (2022-10-07)

[Comment Deleted]

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### sm...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-14)

Not requesting merge to dev (M108) because latest trunk commit (1052116) appears to be prior to dev branch point (1058933). If this is incorrect, please replace the Merge-NA-108 label with Merge-Request-108. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1366806?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1366503]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061095)*
