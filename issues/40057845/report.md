# Security: heap-use-after-free in content::WebContentsObserver::web_contents

| Field | Value |
|-------|-------|
| **Issue ID** | [40057845](https://issues.chromium.org/issues/40057845) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | yu...@gmail.com |
| **Assignee** | cm...@chromium.org |
| **Created** | 2021-11-07 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

I thought it is inappropriate implementation in WebAppInstallTask. Actually, it is a use after free in WebAppInstallTask.

There are a few problems here:

1. WebAppInstallTask extends WebContentsObserver and observer a local variable webcontents. When shutdown the keyed service, it will cause a callchain like this.  
   
   WebAppInstallManager::Shutdown -> ~WebAppInstallTask -> ~install\_callback\_ -> ~WebContentsImpl -> WebContentsDestroyed -> CallInstallCallback -> ~install\_callback\_  
   
   It will cause a DCHECK fail in ref\_counted.h.
2. It it a use after free problem. LoaderTask is also a WebContentsObserver and observer the webcontents in problem 1. When LoaderTask::LoadUrl call, it wrapper a callback bind with WebAppInstallTask raw pointer and save as |callback\_|. After the webcontents destroyed, it will post the |callback\_| task to main thread in WebContentsDestroyed and cause a Uaf when the callback run.  
   
   WebAppInstallManager::Shutdown -> ~WebAppInstallTask -> ~install\_callback\_ -> ~WebContentsImpl -> LoaderTask::WebContentsDestroyed -> LoaderTask::PostResultTask  
   
   UaF triggered when WebAppInstallTask::OnWebAppUrlLoadedGetWebApplicationInfo callback run on main thread.
3. Callback in problem 2 hold a raw pointer to the webcontents and also possiable cause a UaF when WebAppInstallTask::OnWebAppUrlLoadedGetWebApplicationInfo callback run.

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/web_applications/web_app_install_task.cc;drc=2be2d6b317c391d34a77bed0c8836058ae180c93;l=147>  

void WebAppInstallTask::LoadWebAppAndCheckManifest(  

...  

content::WebContents\* web\_contents\_ptr = web\_contents.get();

Observe(web\_contents.get()); // obsever a local variable web\_contents[1]  

background\_installation\_ = false;  

install\_callback\_ =  

base::BindOnce(std::move(callback), std::move(web\_contents)); // move webcontents unique\_ptr to install\_callback\_[1]  

install\_source\_ = install\_source;  

url\_loader->LoadUrl(  

url, web\_contents\_ptr,  

WebAppUrlLoader::UrlComparison::kIgnoreQueryParamsAndRef,  

base::BindOnce( // this callback will be wrapper in another callback and saved in LoaderTask and it use base::Unretained(this)[2]  

&WebAppInstallTask::OnWebAppUrlLoadedCheckAndRetrieveManifest,  

base::Unretained(this), url, web\_contents\_ptr)); // web\_contents\_ptr will be use in OnWebAppUrlLoadedGetWebApplicationInfo callback after webcontents freed[3]  

}  

void WebAppInstallTask::WebContentsDestroyed() {  

CallInstallCallback(AppId(), InstallResultCode::kWebContentsDestroyed); // call when web contents destroyed[1]  

}  

void WebAppInstallTask::CallInstallCallback(const AppId& app\_id,  

InstallResultCode code) {  

...  

DCHECK(install\_callback\_);  

std::move(install\_callback\_).Run(app\_id, code); // will try deconstruct install\_callback\_ again because of std::move[1]  

}

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/web_applications/web_app_url_loader.cc;drc=917a2b5c9c82f96f685692202fd44725b02f6e98;l=128>  

void WebAppUrlLoader::LoadUrl(const GURL& url,  

content::WebContents\* web\_contents,  

UrlComparison url\_comparison,  

ResultCallback callback) {  

auto loader\_task = std::make\_unique<LoaderTask>();  

auto\* loader\_task\_ptr = loader\_task.get();  

loader\_task\_ptr->LoadUrl( // wrapper a callback and call LoaderTask::LoadUrl[2]  

url, web\_contents, url\_comparison,  

base::BindOnce(  

[](ResultCallback callback, std::unique\_ptr<LoaderTask> task,  

Result result) {  

std::move(callback).Run(result);  

task.reset();  

},  

std::move(callback), std::move(loader\_task)));  

}  

class LoaderTask : public content::WebContentsObserver {  

///  

void WebContentsDestroyed() override { // call when web contents destroyed[2]  

timer\_.Stop();  

PostResultTask(WebAppUrlLoader::Result::kFailedWebContentsDestroyed);  

}  

void PostResultTask(WebAppUrlLoader::Result result) {  

Observe(nullptr);  

// Post a task to avoid reentrancy issues e.g. adding a WebContentsObserver  

// while a previous observer call is being executed.  

base::ThreadTaskRunnerHandle::Get()->PostTask(  

FROM\_HERE, base::BindOnce(std::move(callback\_), result)); // task will be post to UI Thread and run after WebAppInstallTask freed[2]  

}  

...  

}

**VERSION**  

Chrome Version: stable (according to source code)  

Operating System: all (according to source code)

**REPRODUCTION CASE**

1. Apply patch and rebuild chrome (this patch force bypass some WebApp check and DCHECK error in problem 1)
2. Launch chrome and install the attach extentsion (call chrome.management.installReplacementWebApp)
3. Close chrome (shutdown keyed service)

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

Reporter credit: Wei Yuan of MoyunSec VLab

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 14.7 KB)
- [background.js](attachments/background.js) (text/plain, 101 B)
- [manifest.json](attachments/manifest.json) (text/plain, 244 B)
- [record.mov](attachments/record.mov) (video/quicktime, 7.9 MB)
- [patch.txt](attachments/patch.txt) (text/plain, 7.0 KB)

## Timeline

### [Deleted User] (2021-11-07)

[Empty comment from Monorail migration]

### yu...@gmail.com (2021-11-07)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-11-08)

dominickn@/ericwilligers@/dmurph@ -- could one of you please take a look at this and help triage it? Thanks.

### va...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>WebAppInstalls]

### va...@chromium.org (2021-11-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-09)

Security bugs should have owners, picking one from C3, feel free to re-assign as appropriate. Thanks!

### do...@chromium.org (2021-11-09)

Over to cmp@ as I believe dmurph is OOO.

### cm...@chromium.org (2021-11-10)

[Empty comment from Monorail migration]

### co...@google.com (2021-11-10)

[Empty comment from Monorail migration]

### cm...@chromium.org (2021-11-11)

FYI to phillis and estade

### cm...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### yu...@gmail.com (2021-11-12)

The callback trigger UaF is WebAppInstallTask::OnWebAppUrlLoadedCheckAndRetrieveManifest, not WebAppInstallTask::OnWebAppUrlLoadedGetWebApplicationInfo.

Sorry for my very careless mistake and please let me know if have any questions.

### er...@chromium.org (2021-11-12)

WebAppInstallManager and WebAppInstallTask each own a WeakPtrFactory. There is no need for these classes to use base::Unretained(this)

   https://chromium-review.googlesource.com/c/chromium/src/+/3275867

### es...@chromium.org (2021-11-12)

[Empty comment from Monorail migration]

### cm...@chromium.org (2021-11-12)

Hey Eric, thank you for your eagerness to fix this issue!  TL;DR I've +1'd your https://crrev.com/c/3275867 and am taking this bug back.

More info: I've been investigating this while dmurph@ is OOO and have a WIP CL to address it at https://crrev.com/c/3277123.  My CL includes the WeakPtr change to the affected area (and others) along with the fix to the WebContents ownership issue to avoid the refcheck issue.  Let's just get your change in, then I'll rebase on top of it and fix the remaining issue.

### gi...@appspot.gserviceaccount.com (2021-11-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/25030ef24ece304403cc88cb4fc8c5e8936e0098

commit 25030ef24ece304403cc88cb4fc8c5e8936e0098
Author: Eric Willigers <ericwilligers@chromium.org>
Date: Fri Nov 12 18:54:23 2021

WebAppInstallTask: Use weak pointers

We replace calls to base::Unretained(this) with GetWeakPtr() in
WebAppInstallTask and WebAppInstallManager.

Bug: 1267661
Change-Id: I1ac0d79657d8980e8edf7cc3a2db5f8ece9c9b58
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3275867
Auto-Submit: Eric Willigers <ericwilligers@chromium.org>
Commit-Queue: Chase Phillips <cmp@chromium.org>
Reviewed-by: Chase Phillips <cmp@chromium.org>
Cr-Commit-Position: refs/heads/main@{#941240}

[modify] https://crrev.com/25030ef24ece304403cc88cb4fc8c5e8936e0098/chrome/browser/web_applications/web_app_install_task.cc
[modify] https://crrev.com/25030ef24ece304403cc88cb4fc8c5e8936e0098/chrome/browser/web_applications/web_app_install_manager.h
[modify] https://crrev.com/25030ef24ece304403cc88cb4fc8c5e8936e0098/chrome/browser/web_applications/web_app_install_manager.cc


### cm...@chromium.org (2021-11-12)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-15)

Setting sev based upon memory corruption in browser process. 

### gi...@appspot.gserviceaccount.com (2021-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fc26857104f0bc5ec024941ae39a8236d73057a6

commit fc26857104f0bc5ec024941ae39a8236d73057a6
Author: Chase Phillips <cmp@chromium.org>
Date: Mon Nov 15 23:18:04 2021

dpwa: Ensure callbacks are run on install task destruction

If install task `task` is destroyed, `task` destruction will destroy
`install_callback_`.  In some cases, `install_callback_` may hold a
WebContents and destroying that can lead to triggering a call back onto
`task`'s WebContentsDestroyed().  In other cases, if a callback is
present when `task` is destroyed, we may fail to signal to callers the
new state of the install request and inadvertently drop the callback on
the floor.

At destruction, call any pending callback as long as `task` is still
observing a WebContents.  CallInstallCallback() will trigger any pending
callback, but before doing so, will update `task` to stop observing
WebContents with a call to Observe(nullptr).

Bug: 1267661
Change-Id: Iecea0e91ff49b302e449b7dbc7767b363b769aa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3277123
Commit-Queue: Chase Phillips <cmp@chromium.org>
Auto-Submit: Chase Phillips <cmp@chromium.org>
Reviewed-by: Phillis Tang <phillis@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/main@{#941907}

[modify] https://crrev.com/fc26857104f0bc5ec024941ae39a8236d73057a6/chrome/browser/web_applications/web_app_constants.cc
[modify] https://crrev.com/fc26857104f0bc5ec024941ae39a8236d73057a6/chrome/browser/web_applications/web_app_install_task.cc
[modify] https://crrev.com/fc26857104f0bc5ec024941ae39a8236d73057a6/chrome/browser/web_applications/web_app_install_task_unittest.cc
[modify] https://crrev.com/fc26857104f0bc5ec024941ae39a8236d73057a6/chrome/browser/web_applications/web_app_install_manager.cc
[modify] https://crrev.com/fc26857104f0bc5ec024941ae39a8236d73057a6/chrome/browser/web_applications/web_app_constants.h


### cm...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cm...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### cm...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-15)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-11-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-18)

Requesting merge to stable M96 because latest trunk commit (941907) appears to be after stable branch point (929512).

Requesting merge to dev M97 because latest trunk commit (941907) appears to be after dev branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-18)

Merge review required: M97 is already shipping to beta.

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

### [Deleted User] (2021-11-18)

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

### am...@chromium.org (2021-11-19)

Merge approved to M96 and M97, please merge to branches 4664 and 4692 respectively at your earliest convenience.

### cm...@chromium.org (2021-11-20)

Thanks Amy.  This is on my list of things to do early next week for https://crrev.com/c/3275867 and likely also https://crrev.com/c/3277123.

(FYI to ericwilligers@ that I'll take a look at getting both of these CLs to 96 and 97)

### [Deleted User] (2021-11-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-11-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-24)

Congratulations -- the VRP Panel has decided to award you $15,000 for this report. Thank you for this report and nice work!

### am...@google.com (2021-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-11-29)

Your change has been approved for M97 branch,please go ahead and merge the CL's to M97 branch:4692 manually asap so that they would be part of this week's first M97 Beta release.

### am...@chromium.org (2021-11-29)

hi cmp@ -- please merge to branch 4692 ASAP so this can be included in beta cut tomorrow; for M96 merge, please merge to branch 4664 by EOD Friday so this fix can be included in next week's stable respin -- thank you! 

### cm...@chromium.org (2021-11-30)

Hi, all 4 CLs have been posted and are CR+1.  Landing them through CQ now.

4664 (96):
  Task weak ptr fix: https://crrev.com/c/3307742
  Callback fix: https://crrev.com/c/3307644

4692 (97):
  Task weak ptr fix: https://crrev.com/c/3308212
  Callback fix: https://crrev.com/c/3308213

### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/62fd7d67b813b1bbb9253408558df7c2d0f75fc3

commit 62fd7d67b813b1bbb9253408558df7c2d0f75fc3
Author: Chase Phillips <cmp@chromium.org>
Date: Tue Nov 30 01:26:16 2021

WebAppInstallTask: Use weak pointers

We replace calls to base::Unretained(this) with GetWeakPtr() in
WebAppInstallTask and WebAppInstallManager.

(cherry picked from commit 25030ef24ece304403cc88cb4fc8c5e8936e0098)

Bug: 1267661
Change-Id: I1ac0d79657d8980e8edf7cc3a2db5f8ece9c9b58
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3275867
Auto-Submit: Eric Willigers <ericwilligers@chromium.org>
Commit-Queue: Chase Phillips <cmp@chromium.org>
Reviewed-by: Chase Phillips <cmp@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#941240}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3307742
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Auto-Submit: Chase Phillips <cmp@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1181}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/62fd7d67b813b1bbb9253408558df7c2d0f75fc3/chrome/browser/web_applications/web_app_install_task.cc
[modify] https://crrev.com/62fd7d67b813b1bbb9253408558df7c2d0f75fc3/chrome/browser/web_applications/web_app_install_manager.h
[modify] https://crrev.com/62fd7d67b813b1bbb9253408558df7c2d0f75fc3/chrome/browser/web_applications/web_app_install_manager.cc


### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e1ed13a08e46f5703705f298edd9e6059c3e87a4

commit e1ed13a08e46f5703705f298edd9e6059c3e87a4
Author: Chase Phillips <cmp@chromium.org>
Date: Tue Nov 30 01:51:48 2021

WebAppInstallTask: Use weak pointers

We replace calls to base::Unretained(this) with GetWeakPtr() in
WebAppInstallTask and WebAppInstallManager.

(cherry picked from commit 25030ef24ece304403cc88cb4fc8c5e8936e0098)

Bug: 1267661
Change-Id: I1ac0d79657d8980e8edf7cc3a2db5f8ece9c9b58
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3275867
Auto-Submit: Eric Willigers <ericwilligers@chromium.org>
Commit-Queue: Chase Phillips <cmp@chromium.org>
Reviewed-by: Chase Phillips <cmp@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#941240}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3308212
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Auto-Submit: Chase Phillips <cmp@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#555}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/e1ed13a08e46f5703705f298edd9e6059c3e87a4/chrome/browser/web_applications/web_app_install_task.cc
[modify] https://crrev.com/e1ed13a08e46f5703705f298edd9e6059c3e87a4/chrome/browser/web_applications/web_app_install_manager.h
[modify] https://crrev.com/e1ed13a08e46f5703705f298edd9e6059c3e87a4/chrome/browser/web_applications/web_app_install_manager.cc


### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/30835f861d5cd78b309225a4faab70cd011c8be6

commit 30835f861d5cd78b309225a4faab70cd011c8be6
Author: Chase Phillips <cmp@chromium.org>
Date: Tue Nov 30 02:08:27 2021

dpwa: Ensure callbacks are run on install task destruction

If install task `task` is destroyed, `task` destruction will destroy
`install_callback_`.  In some cases, `install_callback_` may hold a
WebContents and destroying that can lead to triggering a call back onto
`task`'s WebContentsDestroyed().  In other cases, if a callback is
present when `task` is destroyed, we may fail to signal to callers the
new state of the install request and inadvertently drop the callback on
the floor.

At destruction, call any pending callback as long as `task` is still
observing a WebContents.  CallInstallCallback() will trigger any pending
callback, but before doing so, will update `task` to stop observing
WebContents with a call to Observe(nullptr).

(cherry picked from commit fc26857104f0bc5ec024941ae39a8236d73057a6)

Bug: 1267661
Change-Id: Iecea0e91ff49b302e449b7dbc7767b363b769aa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3277123
Commit-Queue: Chase Phillips <cmp@chromium.org>
Auto-Submit: Chase Phillips <cmp@chromium.org>
Reviewed-by: Phillis Tang <phillis@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#941907}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3307644
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/4664@{#1182}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/30835f861d5cd78b309225a4faab70cd011c8be6/chrome/browser/web_applications/web_app_install_task.cc
[modify] https://crrev.com/30835f861d5cd78b309225a4faab70cd011c8be6/chrome/browser/web_applications/web_app_constants.cc
[modify] https://crrev.com/30835f861d5cd78b309225a4faab70cd011c8be6/chrome/browser/web_applications/web_app_install_task_unittest.cc
[modify] https://crrev.com/30835f861d5cd78b309225a4faab70cd011c8be6/chrome/browser/web_applications/web_app_install_manager.cc
[modify] https://crrev.com/30835f861d5cd78b309225a4faab70cd011c8be6/chrome/browser/web_applications/web_app_constants.h


### gi...@appspot.gserviceaccount.com (2021-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3adb8f7e7dc78e4aa23544b312328647e618643b

commit 3adb8f7e7dc78e4aa23544b312328647e618643b
Author: Chase Phillips <cmp@chromium.org>
Date: Tue Nov 30 02:09:48 2021

dpwa: Ensure callbacks are run on install task destruction

If install task `task` is destroyed, `task` destruction will destroy
`install_callback_`.  In some cases, `install_callback_` may hold a
WebContents and destroying that can lead to triggering a call back onto
`task`'s WebContentsDestroyed().  In other cases, if a callback is
present when `task` is destroyed, we may fail to signal to callers the
new state of the install request and inadvertently drop the callback on
the floor.

At destruction, call any pending callback as long as `task` is still
observing a WebContents.  CallInstallCallback() will trigger any pending
callback, but before doing so, will update `task` to stop observing
WebContents with a call to Observe(nullptr).

(cherry picked from commit fc26857104f0bc5ec024941ae39a8236d73057a6)

Bug: 1267661
Change-Id: Iecea0e91ff49b302e449b7dbc7767b363b769aa6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3277123
Commit-Queue: Chase Phillips <cmp@chromium.org>
Auto-Submit: Chase Phillips <cmp@chromium.org>
Reviewed-by: Phillis Tang <phillis@chromium.org>
Reviewed-by: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#941907}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3308213
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/branch-heads/4692@{#556}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/3adb8f7e7dc78e4aa23544b312328647e618643b/chrome/browser/web_applications/web_app_install_task.cc
[modify] https://crrev.com/3adb8f7e7dc78e4aa23544b312328647e618643b/chrome/browser/web_applications/web_app_constants.cc
[modify] https://crrev.com/3adb8f7e7dc78e4aa23544b312328647e618643b/chrome/browser/web_applications/web_app_install_task_unittest.cc
[modify] https://crrev.com/3adb8f7e7dc78e4aa23544b312328647e618643b/chrome/browser/web_applications/web_app_install_manager.cc
[modify] https://crrev.com/3adb8f7e7dc78e4aa23544b312328647e618643b/chrome/browser/web_applications/web_app_constants.h


### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-03)

We believe this probably requires an extension, and is also a profile destruction bug; these are sufficient mitigations to downgrade this from Critical to High.

### [Deleted User] (2021-12-04)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@chromium.org (2021-12-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1267661?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057845)*
