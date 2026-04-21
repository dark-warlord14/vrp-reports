# Security: UAF in extensions::SupervisedUserExtensionsDelegateImpl::ShowParentPermissionDialogForExtension

| Field | Value |
|-------|-------|
| **Issue ID** | [40063759](https://issues.chromium.org/issues/40063759) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2023-03-25 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

When loading extension icon in SupervisedUserExtensionsDelegateImpl::RequestToEnableExtensionOrShowError,  

the web content will be bound into function `OnExtensionDataLoaded` as a callback [0](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_extensions_delegate_impl.cc;l=111-116;drc=ff8be0d73bf2c6c504fc73b3377c5c8b2fd140ce).

```
void SupervisedUserExtensionsDelegateImpl::RequestToEnableExtensionOrShowError(  
    const extensions::Extension& extension,  
    content::BrowserContext\* browser_context,  
    content::WebContents\* web_contents,  
    ExtensionApprovalDoneCallback extension_approval_callback) {  
  // ...  
  
  if (CanInstallExtensions(browser_context)) {  
    auto icon_callback = base::BindOnce(  
        &SupervisedUserExtensionsDelegateImpl::OnExtensionDataLoaded,  
        base::Unretained(this), std::cref(extension), browser_context,  
        web_contents);  // <---[0]  
    icon_loader_ = std::make_unique<ExtensionIconLoader>();  
    icon_loader_->Load(extension, browser_context, std::move(icon_callback));  
    return;  
  }  
  
  // ...  
}  

```

This callback will run asynchronously after the icon loaded in thread pool [1](https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/image_loader.cc;l=262-273;drc=7575b86db3973aeec227c8427a1d40e968089145).

ExtensionIconLoader::Load -> ImageLoader::LoadImageAtEveryScaleFactorAsync -> ImageLoader::LoadImagesAsync

```
void ImageLoader::LoadImagesAsync(  
    const Extension\* extension,  
    const std::vector<ImageRepresentation>& info_list,  
    ImageLoaderImageCallback callback) {  
  DCHECK_CURRENTLY_ON(BrowserThread::UI);  
  base::ThreadPool::PostTaskAndReplyWithResult(       // <--- [1] load icon in thread pool  
      FROM_HERE, {base::MayBlock(), base::TaskPriority::USER_VISIBLE},  
      base::BindOnce(LoadImagesBlocking, info_list,  
                     LoadResourceBitmaps(extension, info_list)),  
      base::BindOnce(&ImageLoader::ReplyBack, weak_ptr_factory_.GetWeakPtr(),  
                     std::move(callback)));  
}  

```

In the callback, the web content pointer will be used to call |GetTopLevelNativeWindow|[2](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_extensions_delegate_impl.cc;l=142;drc=ff8be0d73bf2c6c504fc73b3377c5c8b2fd140ce).

```
void SupervisedUserExtensionsDelegateImpl::  
    ShowParentPermissionDialogForExtension(  
        const extensions::Extension& extension,  
        content::BrowserContext\* context,  
        content::WebContents\* contents,  
        const gfx::ImageSkia& icon) {  
  // ...  
  gfx::NativeWindow parent_window =  
      contents ? contents->GetTopLevelNativeWindow() : nullptr;  // <--- [2]  
  // ...  
}  

```

If the web content is destroyed before the `ShowParentPermissionDialogForExtension` gets executed, [2](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/supervised_user/supervised_user_extensions_delegate_impl.cc;l=142;drc=ff8be0d73bf2c6c504fc73b3377c5c8b2fd140ce) will trigger UAF.

**VERSION**  

Chrome Version: dev 113.0.5651.0 <https://chromiumdash.appspot.com/commit/ff8be0d73bf2c6c504fc73b3377c5c8b2fd140ce>  

Operating System: Linux-ChromeOS  

Bitset: <https://chromium-review.googlesource.com/c/chromium/src/+/4300092>

**REPRODUCTION CASE**

I'm struggling to create a supervised child account in Linux-ChromeOS, as a workaround, I patch the  

ManagementSetEnabledFunction to simplify the process of reproducing it.

1. apply the supervised\_user\_load\_icon\_uaf.patch
2. download the extension and run ./out/chromeos/chrome --use-system-clipboard --login-manager --load-extension=/path/to/ext
3. click the extension action icon
4. wait for UAF.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see supervised\_user\_load\_icon\_uaf.asan file.

**CREDIT INFORMATION**  

Reporter credit: Chaobin Zhang

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 334 B)
- [popup.html](attachments/popup.html) (text/plain, 78 B)
- [popup.js](attachments/popup.js) (text/plain, 372 B)
- [icon.png](attachments/icon.png) (image/png, 4.3 KB)
- [supervised_user_load_icon_uaf.patch](attachments/supervised_user_load_icon_uaf.patch) (text/plain, 2.4 KB)
- [supervised_user_load_icon_uaf.asan](attachments/supervised_user_load_icon_uaf.asan) (text/plain, 24.2 KB)
- [supervised_user_load_icon_uaf_poc.mp4](attachments/supervised_user_load_icon_uaf_poc.mp4) (video/mp4, 6.7 MB)

## Timeline

### [Deleted User] (2023-03-25)

[Empty comment from Monorail migration]

### zh...@gmail.com (2023-03-25)

Add poc video.

### zh...@gmail.com (2023-03-25)

For a supervised child account, I think we can also reproduce this issue with following steps without extension:
1.  Patch extension image loader with a sleep(3) for easier manual reproduction

diff --git a/extensions/browser/image_loader.cc b/extensions/browser/image_loader.cc
index b8163c786b676..a64940b4875fb 100644
--- a/extensions/browser/image_loader.cc
+++ b/extensions/browser/image_loader.cc
@@ -178,6 +178,9 @@ namespace {
 std::vector<ImageLoader::LoadResult> LoadImagesBlocking(
     const std::vector<ImageLoader::ImageRepresentation>& info_list,
     const std::vector<SkBitmap>& bitmaps) {
+  LOG(ERROR) << "LoadImageBlocking, sleeping";
+  sleep(3);
+
   std::vector<ImageLoader::LoadResult> load_result;
 
   for (size_t i = 0; i < info_list.size(); ++i) {

2. Go to chrome://extensions, try to enable/disable one of the extension.
3. Close the window

### ch...@google.com (2023-03-27)

[Empty comment from Monorail migration]

[Monorail blocking: b/275281500]

### ch...@google.com (2023-03-27)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/275281500). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on.

### [Deleted User] (2023-03-27)

[Empty comment from Monorail migration]

### ch...@google.com (2023-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-06)

[Empty comment from Monorail migration]

### ch...@google.com (2023-04-24)

Marked as fixed.
Cl landed: https://crrev.com/c/4447779



### ch...@google.com (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-24)

[Empty comment from Monorail migration]

### pa...@chromium.org (2023-04-25)

Thanks for this report!

Memory corruption that requires a specific extension to be installed: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#TOC-Medium-severity

But, it also requires user interaction, and for the target to be set up with a supervised child account. Those 2 mitigating factors might make this Low severity, arguably.

[Monorail components: Platform>Extensions]

### [Deleted User] (2023-04-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-05-01)

This code isn't specific to ChromeOS and I'm unsure if the issue is also specific to Chrome OS, therefore adding Linux based platforms. Raising severity for Chrome browser, as this would be a Medium severity issue on the browser side of the house given the mitigations of requiring install of a malicious extension and user interaction. 
Reassigning ownership to agawronska@ (patch author) for potential backmerge to M113. 

### am...@chromium.org (2023-05-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-05-02)

113 merge approved, please merge this fix to branch 5672 at your earliest convenience so this fix can be included in the M113/Stable channel update 

### ag...@chromium.org (2023-05-04)

It's not a clean cherry-pick so I am 'porting' the cl and testing locally. Will upload the cl ASAP.

### gi...@appspot.gserviceaccount.com (2023-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5a47c4799b1d82e8783957180494c36787abfeb2

commit 5a47c4799b1d82e8783957180494c36787abfeb2
Author: Aga Wronska <agawronska@chromium.org>
Date: Thu May 04 23:35:43 2023

[M113] ext approvals: Cancel approval request if requester was deleted

Supervised users require parent approval for an extension installation.
Approval request can originate from the browser tab and the corresponding
web contents is then passed to the request. Showing the approval might
require an async data fetch (extension icon) and the browser tab or
window can be closed meanwhile. This cases UAF for the web contents.

In order to prevent UAF this cl uses weak ptr to the web contents and
cancels the approval if the web contents was deleted during the async
data fetch.

Note: We assume that once the async data fetch is finished the UI is  modal
or system modal and the browser window/tab cannot be closed before the
request is completed.

(cherry picked from commit 51ce31ffb029509615e00e17e9c0af257e945b32)

Bug: 1427804, b:275281500
Change-Id: Ib4203dd6f6aa129e5dfe37c631b95de37d747644
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4447779
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Reviewed-by: Courtney Wong <courtneywong@chromium.org>
Commit-Queue: Aga Wronska <agawronska@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1133455}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4504692
Cr-Commit-Position: refs/branch-heads/5672@{#1099}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/5a47c4799b1d82e8783957180494c36787abfeb2/chrome/browser/supervised_user/supervised_user_extensions_delegate_impl.cc
[modify] https://crrev.com/5a47c4799b1d82e8783957180494c36787abfeb2/chrome/browser/supervised_user/supervised_user_extensions_delegate_impl.h


### am...@google.com (2023-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-12)

Congratulations, ChaobinZhang! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us. 

### zh...@gmail.com (2023-05-12)

Thank you very much! 

### am...@google.com (2023-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1427804?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: b/275281500]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063759)*
