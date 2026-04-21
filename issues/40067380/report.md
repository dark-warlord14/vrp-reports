# Security: UAF in VisualSearchClassifierHost::StartClassificationWithModel

| Field | Value |
|-------|-------|
| **Issue ID** | [40067380](https://issues.chromium.org/issues/40067380) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | UI>Browser |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ps...@google.com |
| **Created** | 2023-07-13 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

Bitset: <https://chromium-review.googlesource.com/c/chromium/src/+/4638949>

When VisualSearchSuggestions is enabled, VisualSearchSuggestionsService will listen on the event of  

visual search classification model loaded. Before the model file is ready, it will store the callback  

in the |model\_callbacks\_| if |SetModelUpdateCallback| is called. [0]

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/companion/visual_search/visual_search_suggestions_service.cc;l=122-130;drc=7d46a1cd36ecd315f69cd8dd17cd4bf4b86bc5dc>

```
void VisualSearchSuggestionsService::SetModelUpdateCallback(  
    ModelUpdateCallback callback) {  
  if (model_file_) {  
    std::move(callback).Run(model_file_->Duplicate(),  
                            GetModelSpec(model_metadata_));  
    return;  
  }  
  model_callbacks_.emplace_back(std::move(callback)); // <--- [0]  
}  

```

In the VisualSearchClassifierHost, the |render\_frame\_host| raw pointer is bound to the callback. [1]  

So if the render\_frame\_host is freed, when target model file is loaded, line [3] in function  

|StartClassificationWithModel| will cause UAF.

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/companion/visual_search/visual_search_classifier_host.cc;l=98-101;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188>

```
void VisualSearchClassifierHost::StartClassification(  
    content::RenderFrameHost\* render_frame_host,  
    const GURL& validated_url,  
    ResultCallback callback) {  
  if (!render_frame_host) {  
    LOCAL_HISTOGRAM_BOOLEAN("Companion.VisualSearch.EmptyRenderFrame", true);  
    return;  
  }  
  
  if (validated_url == current_url_) {   // <--- [2]  
    LOCAL_HISTOGRAM_BOOLEAN(  
        "Companion.VisualSearch.ClassificationAlreadyStarted", true);  
    return;  
  }  
  
  current_url_ = validated_url;  
  visual_search_service_->SetModelUpdateCallback(  
      base::BindOnce(&VisualSearchClassifierHost::StartClassificationWithModel,  
                     weak_ptr_factory_.GetWeakPtr(), render_frame_host,  
                     validated_url, std::move(callback))); // <--- [1]  
  
  LOCAL_HISTOGRAM_BOOLEAN("Companion.VisualSearch.StartClassificationBegin",  
                          true);  
}  

```

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/companion/visual_search/visual_search_classifier_host.cc;l=136;drc=1b9ee37d9e583adb8b4f492115bdb8fd268e8188>

```
void VisualSearchClassifierHost::StartClassificationWithModel(  
    content::RenderFrameHost\* render_frame_host,  
    const GURL validated_url,  
    ResultCallback callback,  
    base::File model,  
    std::string base64_config) {  
  // ...  
  render_frame_host->GetRemoteAssociatedInterfaces()->GetInterface(  
      &visual_search);  // <---- [3] UAF if render_frame_host was freed.  
  
  // ...  
}  

```

There is a lot of check like: if (validated\_url == current\_url\_) [2], this could be bypassed in  

following steps:

1. Visit first website, like google.com. RenderFrameHost A, validated\_url: "<https://google.com/>" was stored in the model\_callbacks\_.
2. Redirect to second website, for example: example.com, currently A maybe freed.
3. Go back to the first website, google.com, current\_url\_ will be "<https://google.com/>". And then the stored model\_callbacks\_ run, validated\_url == current\_url\_ is true.

**VERSION**  

Chrome Version: commit at c5dd506edb56a0c12f58381e19d11e063a0e7fd6  

Operating System: desktop platforms

NOTE: I found that in lacros, MiraclePtr is disabled by default. And VisualSearchSuggestions feature can be enabled in lacros.  

See: <https://chromium-review.googlesource.com/c/chromium/src/+/4478673/5/base/allocator/partition_alloc_features.cc#110>

I can reproduced this problem with lacros.

**REPRODUCTION CASE**  

I'm testing on linux-chromeos-ash, but I expect it to be compatible with other desktop platforms as well.  

0. touch /tmp/fake-model and git apply uaf-vsss.patch

1. Run ./out/chromeos/chrome --use-system-clipboard --login-manager --enable-features=VisualSearchSuggestions
2. Go to <http://a.zhchbin.live> and open search companion side panel, wait for uaf
3. If it didn't work, please restart chromeos and try again.

NOTE: a.zhchbin.live will redirect to b.zhchbin.xyz/redirect\_back, and then redirect back to a.zhchbin.live

uaf-vsss.patch explanation  

I'm currently unable to determine how to trigger |VisualSearchSuggestionsService::OnModelUpdated| in my environment.  

Based on the relevant code, it seems that Chrome may retrieve the model with a delay of several seconds before  

triggering this method. To facilitate testing, I've simulated this behavior by adding a task to the background  

runner and including a sleep(30) in the task.

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/optimization_guide/core/prediction_manager.cc;l=1030-1049;drc=9d4eb7ed25296abba8fd525a6bdd0fdbf4bcdd9f>  

<https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/optimization_guide/core/optimization_guide_features.cc;l=457-475;drc=9d4eb7ed25296abba8fd525a6bdd0fdbf4bcdd9f>

In case it's necessary, I've created a video demonstration as well:

In ChromeOS-Ash  

<https://drive.google.com/file/d/12RM7lq6Ztouo6P5Fua83jWXjSXnbqA31/view?usp=sharing>

With lacros  

<https://drive.google.com/file/d/1hZoz1D4rMrnQsYKgumY3UAPHadqi1_0T/view?usp=sharing>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see uaf-vsch.asan

Fix Suggestion:  

Pass the render\_frame\_host global id instead of raw pointer.  

See fix-uaf-vsch.patch.

## Attachments

- [uaf-vsss.patch](attachments/uaf-vsss.patch) (text/plain, 2.0 KB)
- [fix-uaf-vsch.patch](attachments/fix-uaf-vsch.patch) (text/plain, 2.5 KB)
- [uaf-vsch.asan](attachments/uaf-vsch.asan) (text/plain, 29.8 KB)

## Timeline

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-07-13)

This needs an as-yet unshipped feature: --enable-features=VisualSearchSuggestions

[Monorail components: UI>Browser]

### da...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### mc...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### ps...@google.com (2023-07-13)

Thanks for reporting this bug, currently working on fix.

### gi...@appspot.gserviceaccount.com (2023-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/94e7b9e682093d43919744687c1741809818648c

commit 94e7b9e682093d43919744687c1741809818648c
Author: Pierre St Juste <pstjuste@google.com>
Date: Sat Jul 15 06:37:06 2023

Bug fix for UAF bug in VisualSearchClassifierHost.

This cl removes the current_url checks and does not pass around the callback storing the RFH that is the culprit of the UAF bug.

Bug: 1464636
Change-Id: I091635d1a81ca9a9fac61f98fedc386ad4450158
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4680465
Commit-Queue: Pierre St Juste <pstjuste@google.com>
Reviewed-by: Michael Crouse <mcrouse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1170854}

[modify] https://crrev.com/94e7b9e682093d43919744687c1741809818648c/chrome/browser/companion/visual_search/visual_search_classifier_host_unittest.cc
[modify] https://crrev.com/94e7b9e682093d43919744687c1741809818648c/chrome/browser/companion/visual_search/visual_search_classifier_host.h
[modify] https://crrev.com/94e7b9e682093d43919744687c1741809818648c/chrome/browser/ui/views/side_panel/search_companion/companion_page_browsertest.cc
[modify] https://crrev.com/94e7b9e682093d43919744687c1741809818648c/chrome/browser/companion/visual_search/visual_search_classifier_host.cc


### zh...@gmail.com (2023-07-15)

[Comment Deleted]

### zh...@gmail.com (2023-07-15)

https://source.chromium.org/chromium/chromium/src/+/main:base/allocator/partition_alloc_features.cc;l=104-114;drc=2e824dc95e28bbafac53944f5eea1dd2b1ed14fc

```
BASE_FEATURE(kPartitionAllocBackupRefPtr,
             "PartitionAllocBackupRefPtr",
#if BUILDFLAG(IS_ANDROID) || BUILDFLAG(IS_WIN) || BUILDFLAG(IS_MAC) || \
    BUILDFLAG(IS_CHROMEOS_ASH) ||                                      \
    (BUILDFLAG(IS_LINUX) && !BUILDFLAG(IS_CASTOS)) ||                  \
    BUILDFLAG(ENABLE_BACKUP_REF_PTR_FEATURE_FLAG) ||                   \
    (BUILDFLAG(USE_ASAN_BACKUP_REF_PTR) && BUILDFLAG(IS_LINUX))
             FEATURE_ENABLED_BY_DEFAULT
#else
             FEATURE_DISABLED_BY_DEFAULT
#endif
```

In my local build of chrome ash, PartitionAllocBackupRefPtr is enabled by default, while build of lacros is disabled by default.

### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7e32c359eb9eb81fb8d08c77ff6f3cf019c41753

commit 7e32c359eb9eb81fb8d08c77ff6f3cf019c41753
Author: Pierre St Juste <pstjuste@google.com>
Date: Tue Jul 18 16:35:23 2023

[M116] Bug fix for UAF bug in VisualSearchClassifierHost.

This cl removes the current_url checks and does not pass around the callback storing the RFH that is the culprit of the UAF bug.

(cherry picked from commit 94e7b9e682093d43919744687c1741809818648c)

Bug: 1449021, 1464636
Change-Id: I091635d1a81ca9a9fac61f98fedc386ad4450158
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4680465
Commit-Queue: Pierre St Juste <pstjuste@google.com>
Reviewed-by: Michael Crouse <mcrouse@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1170854}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4690895
Cr-Commit-Position: refs/branch-heads/5845@{#572}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/7e32c359eb9eb81fb8d08c77ff6f3cf019c41753/chrome/browser/companion/visual_search/visual_search_classifier_host_unittest.cc
[modify] https://crrev.com/7e32c359eb9eb81fb8d08c77ff6f3cf019c41753/chrome/browser/companion/visual_search/visual_search_classifier_host.h
[modify] https://crrev.com/7e32c359eb9eb81fb8d08c77ff6f3cf019c41753/chrome/browser/ui/views/side_panel/search_companion/companion_page_browsertest.cc
[modify] https://crrev.com/7e32c359eb9eb81fb8d08c77ff6f3cf019c41753/chrome/browser/companion/visual_search/visual_search_classifier_host.cc


### zh...@gmail.com (2023-07-21)

Maybe we can mark this issue as fixed? 

### ps...@google.com (2023-07-21)

[Comment Deleted]

### zh...@gmail.com (2023-07-22)

Certainly. I've tested the issue in both Lacros and ChromeOS-Ash and can confirm that the fix is solid.

### ps...@google.com (2023-07-23)

Wonderful, closing out bug now, thank you.

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-10)

Congratulations Chaobin Zhang! The VRP Panel has decided to award you $2,000 for this report of a significantly mitigated security bug, mitigated by a fairly constrained race condition and user interaction, + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us. 

### zh...@gmail.com (2023-08-10)

Thank you very much! 

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-10-30)

This issue was migrated from crbug.com/chromium/1464636?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067380)*
