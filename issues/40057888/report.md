# Security: Use after free in WebApkIconHasher

| Field | Value |
|-------|-------|
| **Issue ID** | [40057888](https://issues.chromium.org/issues/40057888) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Mobile>WebAPKs |
| **Platforms** | Android |
| **Reporter** | ra...@gmail.com |
| **Assignee** | fb...@chromium.org |
| **Created** | 2021-11-11 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

this bug is introduced on this commit : <https://chromium-review.googlesource.com/c/chromium/src/+/3173211>

```
void WebApkIconHasher::OnSimpleLoaderComplete(  
    base::WeakPtr<content::WebContents> web_contents,  
    int timeout_ms,  
    std::unique_ptr<std::string> response_body) {  
  ....  
  if (simple_url_loader->ResponseInfo() &&  
      simple_url_loader->ResponseInfo()->mime_type == "image/svg+xml") {  
    if (!web_contents) {  
      RunCallback({});  
      return;  
    }  
  
    download_timeout_timer_.Start(  
        FROM_HERE, base::Milliseconds(timeout_ms),  
        base::BindOnce(&WebApkIconHasher::OnDownloadTimedOut,  
                       base::Unretained(this)));  
  
    web_contents->DownloadImage(  
        simple_url_loader->GetFinalURL(),  
        false,        // is_favicon  
        gfx::Size(),  // no preferred size  
        0,            // no max size  
        false,        // normal cache policy  
        base::BindOnce(&WebApkIconHasher::OnImageDownloaded,  
                       base::Unretained(this), std::move(response_body))); //[0]  
    return;  
  }  
  ....  

```

when installing webapk, chrome download icon. if webapk's icon is svg file, it call DownloadImage mojo ipc[0]  

then callback function that include `base::Unretained(this)`.

unfortunately, mojo response callback can delay as much as user want.

```
void WebApkIconHasher::OnDownloadTimedOut() {  
  simple_url_loader_.reset();  
  
  RunCallback({});  
}  
  
void WebApkIconHasher::RunCallback(Icon icon) {  
  std::move(callback_).Run(std::move(icon));  
  delete this;  
}  

```

so if wating untill timeout, we can call `OnDownloadTimedOut`that delete this before mojo response callback.

as result, it cause use-after-free

**VERSION**  

Chrome Version: chromium master  

Operating System: android

**REPRODUCTION CASE**

```
diff --git a/third_party/blink/renderer/modules/image_downloader/image_downloader_impl.cc b/third_party/blink/renderer/modules/image_downloader/image_downloader_impl.cc  
index db9b9d38bfe0f..0c6c08b3dc6f4 100644  
--- a/third_party/blink/renderer/modules/image_downloader/image_downloader_impl.cc  
+++ b/third_party/blink/renderer/modules/image_downloader/image_downloader_impl.cc  
@@ -162,7 +162,7 @@ void ImageDownloaderImpl::CreateMojoService(  
   receiver_.set_disconnect_handler(  
       WTF::Bind(&ImageDownloaderImpl::Dispose, WrapWeakPersistent(this)));  
 }  
-  
+static int fuck = 0;  
 // ImageDownloader methods:  
 void ImageDownloaderImpl::DownloadImage(const KURL& image_url,  
                                         bool is_favicon,  
@@ -170,8 +170,20 @@ void ImageDownloaderImpl::DownloadImage(const KURL& image_url,  
                                         uint32_t max_bitmap_size,  
                                         bool bypass_cache,  
                                         DownloadImageCallback callback) {  
+  LOG(INFO) << "ImageDownloaderImpl::DownloadImage = "<<image_url;  
   // Constrain the preferred size by the max bitmap size. This will prevent  
   // resizing of the resulting image if the preferred size is used.  
+  
+  KURL victim_url("http://localhost:8000/icon/icon.svg");  
+  if(image_url == victim_url && fuck++ == 1){  
+    LOG(INFO) << "Sleep for trigger bug";  
+    sleep(66);  
+      WTF::Vector<SkBitmap> result_images;  
+    WTF::Vector<gfx::Size> result_original_image_sizes;  
+    std::move(callback).Run(202, result_images,  
+                            result_original_image_sizes);  
+  }  
+  
   gfx::Size constrained_preferred_size(preferred_size);  
   uint32_t max_preferred_dimension =  
       std::max(preferred_size.width(), preferred_size.height());  
@@ -179,7 +191,7 @@ void ImageDownloaderImpl::DownloadImage(const KURL& image_url,  
     float scale = float(max_bitmap_size) / max_preferred_dimension;  
     constrained_preferred_size = gfx::ScaleToFlooredSize(preferred_size, scale);  
   }  
-  
+    
   auto download_callback =  
       WTF::Bind(&ImageDownloaderImpl::DidDownloadImage, WrapPersistent(this),  
                 max_bitmap_size, std::move(callback));  

```

run server.py on a2hs.  

in developer build, should have --webapk-server-url=<http://localhost:8000> flag  

because there is no webapk-server-url in public chromium

and then visit <http://localhost:8000> and install webapk  

i don't know why remove the server URL from public chromium  

<https://chromium-review.googlesource.com/c/chromium/src/+/2126929>  

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Woojin Oh(@pwn\_expoit) of STEALIEN

## Attachments

- [a2hs.zip](attachments/a2hs.zip) (application/octet-stream, 145.3 KB)

## Timeline

### ra...@gmail.com (2021-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-11)

Setting found in 97 based on branch position of ref'd cl.

### ts...@chromium.org (2021-11-11)

Reporter: we're not unzipping anything nowadays. Can you attach the files individually?

### [Deleted User] (2021-11-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-11)

CL author is a gmail address, assigning to reviewer of suspect CL.

[Monorail components: Mobile>WebAPKs]

### yf...@chromium.org (2021-11-11)

Looks like Rayan is out until Dec 1.

### ra...@gmail.com (2021-11-11)

zip file is just pwa example. 

### ha...@chromium.org (2021-11-12)

Assigning back to CL author's @chromium.org account

### [Deleted User] (2021-11-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-12)

[Empty comment from Monorail migration]

### be...@gmail.com (2021-11-15)

Thanks for raising this issue. I'll have a look now.

### be...@gmail.com (2021-11-15)

Here's my WIP CL attempt to fix this issue: https://chromium-review.googlesource.com/c/chromium/src/+/3280083

### ha...@chromium.org (2021-11-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/56f1a674bf89f2bced1a80974bf564fe883eb4c1

commit 56f1a674bf89f2bced1a80974bf564fe883eb4c1
Author: Francois Beaufort <beaufort.francois@gmail.com>
Date: Mon Nov 15 22:21:31 2021

Fix use-after-free security error in WebApkIconHasher

This CL makes sure that the WebApkIconHasher::OnImageDownloaded callback
is not called when WebApkIconHasher::OnDownloadTimedOut is called as
it deletes WebApkIconHasher instance.

Bug: 1269307
Change-Id: If1204434052959c1ec6bfee2501e186f9b32eee5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3280083
Commit-Queue: Glenn Hartmann <hartmanng@chromium.org>
Auto-Submit: François Beaufort <beaufort.francois@gmail.com>
Reviewed-by: Glenn Hartmann <hartmanng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#941853}

[modify] https://crrev.com/56f1a674bf89f2bced1a80974bf564fe883eb4c1/components/webapps/browser/android/webapk/webapk_icon_hasher.h
[modify] https://crrev.com/56f1a674bf89f2bced1a80974bf564fe883eb4c1/components/webapps/browser/android/webapk/webapk_icon_hasher.cc


### be...@gmail.com (2021-11-16)

harmanng@ What are the next steps? Shall I mark this as fixed or shall we ask for merge?
https://chromiumdash.appspot.com/commit/56f1a674bf89f2bced1a80974bf564fe883eb4c1 indicates it landed in Chrome 98.0.4708.0

### ha...@chromium.org (2021-11-16)

It's marked as ReleaseBlock-Stable for m97, which has already branched (https://chromiumdash.appspot.com/schedule). I think we'll end up needing to merge into the m97 beta branch, which I believe is 4692.

Having said that... It looks like security issues get special treatment, and Sheriffbot will handle this for us if we just mark this bug as fixed (https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md#security-merge-triage).

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-16)

Requesting merge to dev M97 because latest trunk commit (941853) appears to be after dev branch point (938553).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-16)

Merge approved: your change passed merge requirements and is auto-approved for M97. Please go ahead and merge the CL to branch 4692 (refs/branch-heads/4692) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8973db70ef8b5602756c5255688b3c5b673fe97b

commit 8973db70ef8b5602756c5255688b3c5b673fe97b
Author: Francois Beaufort <beaufort.francois@gmail.com>
Date: Wed Nov 17 15:18:40 2021

Fix use-after-free security error in WebApkIconHasher

This CL makes sure that the WebApkIconHasher::OnImageDownloaded callback
is not called when WebApkIconHasher::OnDownloadTimedOut is called as
it deletes WebApkIconHasher instance.

(cherry picked from commit 56f1a674bf89f2bced1a80974bf564fe883eb4c1)

Bug: 1269307
Change-Id: If1204434052959c1ec6bfee2501e186f9b32eee5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3280083
Commit-Queue: Glenn Hartmann <hartmanng@chromium.org>
Auto-Submit: François Beaufort <beaufort.francois@gmail.com>
Reviewed-by: Glenn Hartmann <hartmanng@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#941853}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3289343
Reviewed-by: François Beaufort <beaufort.francois@gmail.com>
Cr-Commit-Position: refs/branch-heads/4692@{#239}
Cr-Branched-From: 038cd96142d384c0d2238973f1cb277725a62eba-refs/heads/main@{#938553}

[modify] https://crrev.com/8973db70ef8b5602756c5255688b3c5b673fe97b/components/webapps/browser/android/webapk/webapk_icon_hasher.h
[modify] https://crrev.com/8973db70ef8b5602756c5255688b3c5b673fe97b/components/webapps/browser/android/webapk/webapk_icon_hasher.cc


### am...@google.com (2021-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-17)

Congratulations -- the VRP Panel has decided to award you $20000 for this report. Thanks for reporting this finding to us and nice work!! 

### am...@google.com (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1269307?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057888)*
