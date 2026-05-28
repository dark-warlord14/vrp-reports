# UAF in WallpaperSearch

| Field | Value |
|-------|-------|
| **Issue ID** | [40942837](https://issues.chromium.org/issues/40942837) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | rt...@google.com |
| **Created** | 2023-11-15 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description


UAF in WallpaperSearch


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

# Details

When the local wallpaper is selected in customize-chrome, ｜WallpaperSearchHandler::SetBackgroundToWallpaperSearchResult｜calls |WallpaperSearchBackgroundManager::SelectLocalBackgroundImage| in [1]. 


[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/side_panel/customize_chrome/wallpaper_search/wallpaper_search_handler.cc;l=201;drc=42f0b9c4f60f67676d9096b3e94df9fd47f568f4

```
void WallpaperSearchHandler::SetBackgroundToWallpaperSearchResult(
    const base::Token& result_id) {
  CHECK(base::Contains(wallpaper_search_results_, result_id));
  wallpaper_search_background_manager_->SelectLocalBackgroundImage( // [1]
      result_id, wallpaper_search_results_[result_id]);
}
```

In |SelectLocalBackgroundImage|, if the image is decoded successfully, it post the |NtpCustomBackgroundService::SetBackgroundToLocalResourceWithId| to the thread pool [2], bound with the raw ntp_custom_background_service_ pointer. However, |ntp_custom_background_service_| is bound with the profile lifetime, this service could be freed if the current profile is closed. Hence this is problematic since there's no mechanism to cancel the task when WallpaperSearchBackgroundManager is destoryed.

This results the UAF write in [3], when SetBackgroundToLocalResourceWithId runs on the freed ntp_custom_background_service_, after the |WriteFileToPath| is finished. 

[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.cc;l=95-119;drc=73cea2b959efeacaeef680b11dd8bb74c16f4740

```
void WallpaperSearchBackgroundManager::SelectLocalBackgroundImage(
    const base::Token& id,
    const SkBitmap& bitmap) {
  if (ntp_custom_background_service_->IsCustomBackgroundDisabledByPolicy()) {
    return;
  }

  std::vector<unsigned char> encoded;
  const bool success = gfx::PNGCodec::EncodeBGRASkBitmap(
      bitmap, /*discard_transparency=*/false, &encoded);
  if (success) {
    base::ThreadPool::PostTaskAndReply(
        FROM_HERE, {base::TaskPriority::USER_VISIBLE, base::MayBlock()},
        base::BindOnce(
            &WriteFileToPath, std::string(encoded.begin(), encoded.end()),
            profile_->GetPath().AppendASCII(
                id.ToString() +
                chrome::kChromeUIUntrustedNewTabPageBackgroundFilename)),
        base::BindOnce(
            &NtpCustomBackgroundService::SetBackgroundToLocalResourceWithId,
            base::Unretained(ntp_custom_background_service_), id)); // ------- [2] 
    ntp_custom_background_service_->UpdateCustomLocalBackgroundColorAsync(
        gfx::Image::CreateFrom1xBitmap(bitmap));
  }
}
```


[3] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/search/background/ntp_custom_background_service.cc;l=610;drc=42f0b9c4f60f67676d9096b3e94df9fd47f568f4
```
void NtpCustomBackgroundService::SetBackgroundToLocalResourceWithId(
    const base::Token& id) {
  background_updated_timestamp_ = base::TimeTicks::Now(); // ------ [3] UAF write
  // Remove the last local background if it exists. This is
  // temporary until multiple local images is supported.
  RemoveLocalBackgroundImageCopy(
      profile_,
      pref_service_->GetString(prefs::kNtpCustomBackgroundLocalToDeviceId));
  pref_service_->SetBoolean(prefs::kNtpCustomBackgroundLocalToDevice, true);
  pref_service_->SetString(prefs::kNtpCustomBackgroundLocalToDeviceId,
                           id.ToString());
  NotifyAboutBackgrounds();
}
```

# Reproduction

Since there exists an network problem in my local environment to access the wallpaper json result, I slightly modify the wallpaper selection logic, while it does't change the UAF semantic. Please see patch for detail.

To reproduce:
1. Apply the patch `reproduce.patch`
2. Run chrome with --enable-features=CustomizeChromeWallpaperSearch,OptimizationGuideModelExecution, open the side panel with customized-chrome, or visit chrome://customize-chrome-side-panel.top-chrome. Then close the web page. UAF happens.

# Bisect 

This issue is introduced in the commit https://chromium-review.googlesource.com/c/chromium/src/+/4996421

It affects the canary/dev chrome starts with the following version:

Canary: 121.0.6106.0
Dev: 121.0.6115.2

# Patch suggestion

We could use the weak pointer of WallpaperSearchBackgroundManager to ensure the callback won't be executed if it is destructed. 

I've create an possible patch to fix it, see fix.patch for detail:


```
diff --git a/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.cc b/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.cc
index 15644a1064677..68c3bed2ab6c6 100644
--- a/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.cc
+++ b/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.cc
@@ -58,9 +58,13 @@ void WallpaperSearchBackgroundManager::SelectLocalBackgroundImage(
                 id.ToString() +
                 chrome::kChromeUIUntrustedNewTabPageBackgroundFilename)),
         base::BindOnce(
-            &NtpCustomBackgroundService::SetBackgroundToLocalResourceWithId,
-            base::Unretained(ntp_custom_background_service_), id));
+            &WallpaperSearchBackgroundManager::SetBackgroundToLocalResourceWithId,
+            weak_factory_.GetWeakPtr(), id));
     ntp_custom_background_service_->UpdateCustomLocalBackgroundColorAsync(
         gfx::Image::CreateFrom1xBitmap(bitmap));
   }
 }
+
+void WallpaperSearchBackgroundManager::SetBackgroundToLocalResourceWithId(const base::Token& id) {
+  ntp_custom_background_service_->SetBackgroundToLocalResourceWithId(id);
+}
diff --git a/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.h b/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.h
index f1413e1292a7e..041251c9105d1 100644
--- a/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.h
+++ b/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.h
@@ -25,9 +25,13 @@ class WallpaperSearchBackgroundManager {
   virtual void SelectLocalBackgroundImage(const base::Token& id,
                                           const SkBitmap& bitmap);
 
+  virtual void SetBackgroundToLocalResourceWithId(const base::Token& id);
+
  private:
   raw_ptr<NtpCustomBackgroundService> ntp_custom_background_service_;
   raw_ptr<Profile> profile_;
+
+  base::WeakPtrFactory<WallpaperSearchBackgroundManager> weak_factory_{this};
 };
 
 #endif  // CHROME_BROWSER_SEARCH_BACKGROUND_WALLPAPER_SEARCH_WALLPAPER_SEARCH_BACKGROUND_MANAGER_H_

```



#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

browser UAF write


---

### The cause


#### What version of Chrome have you found the security issue in?

121.0.6106.0[Canary]  121.0.6115.2[Dev]


#### Is the security issue related to a crash?

Yes


#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)




## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 26.5 KB)
- [fix.patch](attachments/fix.patch) (text/plain, 2.2 KB)
- [reproduce.patch](attachments/reproduce.patch) (text/plain, 2.9 KB)

## Timeline

### he...@gmail.com (2023-11-15)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2023-11-15)

[Empty comment from Monorail migration]

### ar...@google.com (2023-11-15)

(current security shepherd)

Thanks!
Very nicely written report!


Severity:
---------

A UAF in the browser process is normally critical.
One mitigating factor: it requires profile destruction, which does lower it to "High".

The repro steps have to insert a "sleep(5)" to ease reproducing it, because the Profile must be destroyed within a very specific timing. I will ask others if this change anything.

Impact:
-------

This is behind the feature CustomizeChromeWallpaperSearch.
So, the impact is "None" at the moment, because it is not enabled yet.

The bug was introduced during the current dev version (121)
See: https://chromiumdash.appspot.com/commit/0254d4aea0057afb3cdf3aaf2be6155afb41da2b
but this was only about moving code around. So I suspect it was a pre-existing bug.

Owner:
------

rtatum@, could you please take a look?

Could you also update the "OS" field. Presumably, the feature is not (or not going) to be enabled on every OSes.


[Monorail components: UI>Browser>NewTabPage]

### he...@gmail.com (2023-11-15)

From the bisect commit https://chromium-review.googlesource.com/c/chromium/src/+/4996421, the original code isn't problematic since it uses weak pointer in `NtpCustomBackgroundService::SelectLocalBackgroundImage` of the old `chrome/browser/search/background/ntp_custom_background_service.cc`

```
  if (success) {
    base::ThreadPool::PostTaskAndReply(
        FROM_HERE, {base::TaskPriority::USER_VISIBLE, base::MayBlock()},
        base::BindOnce(
            &WriteFileToPath, std::string(encoded.begin(), encoded.end()),
            profile_->GetPath().AppendASCII(
                id.ToString() +
                chrome::kChromeUIUntrustedNewTabPageBackgroundFilename)),
        base::BindOnce(&NtpCustomBackgroundService::
                           SetBackgroundToLocalResourceAndExtractColor,
                       weak_ptr_factory_.GetWeakPtr(), id, bitmap)); // correct usage
  }
```

Hence it might not be a pre-existing bug. Thank you.

### rt...@google.com (2023-11-20)

Thanks for catching this!

### rt...@google.com (2023-11-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/76328efb7a68718d075db7fdc0fb73d5b4f888db

commit 76328efb7a68718d075db7fdc0fb73d5b4f888db
Author: Riley Tatum <rtatum@google.com>
Date: Tue Nov 21 17:49:50 2023

fix UAF issue in WallpaperSearchBackgroundManager

A bug was filed about a UAF incident that occurs if the side panel is
closed between a user selecting an image and the image being set, if
the user closes the side panel. To handle this, it is safer if we attach
the bind to the background manager itself instead of
ntp_custom_background_service.

Bug: 1502472
Change-Id: I21dc6b09f823300b121e3327e89ffdb7fbc4e2ef
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5046632
Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
Commit-Queue: Riley Tatum <rtatum@google.com>
Reviewed-by: Paul Adedeji <pauladedeji@google.com>
Cr-Commit-Position: refs/heads/main@{#1227453}

[modify] https://crrev.com/76328efb7a68718d075db7fdc0fb73d5b4f888db/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.cc
[modify] https://crrev.com/76328efb7a68718d075db7fdc0fb73d5b4f888db/chrome/browser/search/background/wallpaper_search/wallpaper_search_background_manager.h


### rt...@google.com (2023-11-21)

I had issues reproducing it locally, but I went with your fix, since it made sense and doesn't hurt anything. @hedonistsmith, could you test it out and let me know if you still see the issue?

### he...@gmail.com (2023-11-22)

Hello, I've tested and verified again and could confirm this UAF doesn't exist in the ToT chromium after the patch.

Thank you very much.

### rt...@google.com (2023-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-23)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-30)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report of a significantly mitigated (mitigated by BRP protection and preconditions of user interaction, and profile destruction) security bug. Thank you for your efforts and reporting this issue to us. 

### he...@gmail.com (2023-11-30)

Hello, does bisect and the patch reward take into consideration?

### am...@chromium.org (2023-11-30)

Hi, it doesn't appear the bisect was accurate. However, we did not take the patch into consideration. We'll re-assess at the next VRP Panel for a potential patch reward. 

### am...@google.com (2023-11-30)

[Empty comment from Monorail migration]

### he...@gmail.com (2023-12-01)

Hello, the bisect is correct since the original code before  https://chromium-review.googlesource.com/c/chromium/src/+/4996421 doesn’t problematic, it uses weak pointer. It is this commit that introduce the UAF as I explain it again in the https://crbug.com/chromium/1502472#c4, I.e., the refactor self introduce the UAF. The commit is not “only about moving code around”, rather changes the weak pointer to the raw pointer. So the bisect should be correct.

### am...@chromium.org (2023-12-07)

Hello, in reviewing the patch and bisect the VRP Panel has decided to award you an additional $1000 for patch and bisect bonus combined -- $500 patch bonus based on the simplicity of the patch and it was not novel in terms of saving engineering effort and overall based on the impact of the bug itself. 

### am...@google.com (2023-12-08)

[Empty comment from Monorail migration]

### is...@google.com (2023-12-08)

This issue was migrated from crbug.com/chromium/1502472?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40942837)*
