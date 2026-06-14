# UAF in OnTaskFinished

| Field | Value |
|-------|-------|
| **Issue ID** | [341208341](https://issues.chromium.org/issues/341208341) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Mobile>WebAPKs |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ha...@google.com |
| **Created** | 2024-05-17 |
| **Bounty** | $1,000.00 |

## Description


[0] WebApkRestoreManager::OnTaskFinished bind as base::Unretained,and will pass into [1],and finally will be posttask,and WebApkRestoreManager is owned by WebApkSyncService [3].
If before posttask,we close browser,will free WebApkRestoreManager object,the task do not be canceled,then will trigger UAF in WebApkRestoreManager::OnTaskFinished.

See https://issues.chromium.org/issues/40060186

void WebApkRestoreManager::MaybeStartNextTask() {
  if (is_running_) {
    return;
  }

  if (tasks_.empty()) {
    ResetIfNotRunning();
    return;
  }

  is_running_ = true;
  web_contents_manager()->EnsureWebContentsCreated(PassKey());
  restorable_tasks_.at(tasks_.front())
      ->Start(base::BindOnce(&WebApkRestoreManager::OnTaskFinished,
                             base::Unretained(this)));  //[0]
}



void WebApkRestoreTask::Start(CompleteCallback complete_callback) {
  complete_callback_ = std::move(complete_callback);   //[]

  web_contents_manager_->LoadUrl(
      fallback_info_->url, base::BindOnce(&WebApkRestoreTask::OnWebAppUrlLoaded,
                                          weak_factory_.GetWeakPtr()));
}



void WebApkRestoreTask::OnFinishedInstall(bool is_fallback,
                                          webapps::WebApkInstallResult result) {
  base::UmaHistogramEnumeration(
      (is_fallback ? kRestoreInstallFallbackWebApkResultHistogram
                   : kRestoreInstallFetchedWebApkResultHistogram),
      result);

  if (complete_callback_) {
    base::SingleThreadTaskRunner::GetCurrentDefault()->PostTask(
        FROM_HERE,
        base::BindOnce(std::move(complete_callback_), manifest_id(), result));  //[2]
  }
}




WebApkSyncService::WebApkSyncService(Profile* profile) {
  database_factory_ = std::make_unique<WebApkDatabaseFactory>(profile);
  sync_bridge_ = std::make_unique<WebApkSyncBridge>(database_factory_.get(),
                                                    base::DoNothing());
  restore_manager_ = std::make_unique<WebApkRestoreManager>(profile);  //[3]
}


std::unique_ptr<KeyedService>
WebApkSyncServiceFactory::BuildServiceInstanceForBrowserContext(
    content::BrowserContext* context) const {
  Profile* profile = Profile::FromBrowserContext(context);
  return std::make_unique<WebApkSyncService>(profile);
}



reproduce

1.restore an webapk
2. Close the browser when the installation is completed (ASAN can be reproduced by adding the msleep function)
3.UAF trigger

Note: I don’t have Android Chrome to reproduce, but the steps to reproduce should be as above, requiring less user interaction


Fix

  restorable_tasks_.at(tasks_.front())
      ->Start(base::BindOnce(&WebApkRestoreManager::OnTaskFinished,
                              weak_ptr_factory_.GetWeakPtr()));



commit
https://chromium-review.googlesource.com/c/chromium/src/+/5414094

## Timeline

### ph...@chromium.org (2024-05-17)

Hi eirage@, could you look at this UAF bug introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/5414094> please?

### pe...@google.com (2024-05-18)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-18)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ei...@chromium.org (2024-05-18)

I'll be away for the next two weeks. Glenn, can you take over this?
(I believe just changing `base::Unretained(this)` to `weak_factory_.GetWeakPtr()` will fix this)

### ha...@google.com (2024-05-23)

Looking into this. I agree that this is a legitimate issue, and the suggested fix looks right to me. I'm not having any luck in actually reproducing it so far though

### ap...@google.com (2024-05-25)

Project: chromium/src
Branch: main

commit 4d9ff9f55afdba857ec4da3f0489a37a0f9c7337
Author: Glenn Hartmann <hartmanng@chromium.org>
Date:   Sat May 25 01:34:35 2024

    Fix potential use-after-free in WebApkRestoreManager
    
    See bug for details.
    
    Bug: 341208341
    Change-Id: I265aa7fa3813bc288403da6f45ab7e5cf0a759f0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5568930
    Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
    Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
    Auto-Submit: Glenn Hartmann <hartmanng@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1306033}

M       chrome/browser/android/webapk/webapk_restore_manager.cc

https://chromium-review.googlesource.com/5568930


### pe...@google.com (2024-05-27)

Requesting merge to beta (M126) because latest trunk commit (1306033) appears to be after beta branch point (1300313).
Merge review required: M126 is already shipping to beta.


Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ha...@google.com (2024-05-27)

Re: [#comment8](https://issues.chromium.org/issues/341208341#comment8)

> 1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/c/chromium/src/+/5568930> (revision hash `4d9ff9f55afdba857ec4da3f0489a37a0f9c7337`)

> 2. Has this fix been verified on Canary to not pose any stability regressions?

Yes

> 3. Does this fix pose any potential non-verifiable stability risks?

No

> 4. Does this fix pose any known compatibility risks?

No

> 5. Does it require manual verification by the test team? If so, please describe required testing.

No

### am...@chromium.org (2024-05-28)

This is a purely speculative / theoretical security bug; however, given this is an exceptionally low / near zero risk change, I'm going to go ahead and approve for merge to M126
Please merge this fix (<https://crrev.com/c/5568930>) to M126 / branch 6478 by EOD tomorrow (Wednesday, 29 May) so this fix can be included in the next M126 Beta update.
Thank you!

### ap...@google.com (2024-05-29)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 764399daf2cb3405ca514f9e598cc855bbd5696d
Author: Glenn Hartmann <hartmanng@chromium.org>
Date:   Wed May 29 16:05:11 2024

    Fix potential use-after-free in WebApkRestoreManager
    
    See bug for details.
    
    (cherry picked from commit 4d9ff9f55afdba857ec4da3f0489a37a0f9c7337)
    
    Bug: 341208341
    Change-Id: I265aa7fa3813bc288403da6f45ab7e5cf0a759f0
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5568930
    Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
    Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
    Auto-Submit: Glenn Hartmann <hartmanng@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1306033}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5581129
    Commit-Queue: Glenn Hartmann <hartmanng@chromium.org>
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#820}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       chrome/browser/android/webapk/webapk_restore_manager.cc

https://chromium-review.googlesource.com/5581129


### pg...@google.com (2024-06-11)

Removing security release added incorrectly

### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of highly mitigated memory corruption in a non-sandboxed process 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Thank you for this speculative report of highly mitigated memory corruption. As we were able to make a security-relevant change based on the information in your report, we did want to extend a thank you reward that also reflects this as a highly mitigated issue. Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-09-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/341208341)*
