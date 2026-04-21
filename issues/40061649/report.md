# UAF in ScreenAIService

| Field | Value |
|-------|-------|
| **Issue ID** | [40061649](https://issues.chromium.org/issues/40061649) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Accessibility |
| **Platforms** | Mac |
| **Reporter** | ha...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2022-11-08 |
| **Bounty** | $1,500.00 |

## Description

**Steps to reproduce the problem:**  

Will attach details soon.

**Problem Description:**  

browser UAF

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.5407.0 \*\*Channel: \*\* Canary

**OS:** Mac OS

## Attachments

- [asan1.txt](attachments/asan1.txt) (text/plain, 24.5 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 24.5 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 767 B)
- [poc1.html](attachments/poc1.html) (text/plain, 190 B)
- [fake.pdf](attachments/fake.pdf) (application/pdf, 1 B)
- [1382369_1.webm](attachments/1382369_1.webm) (video/webm, 2.1 MB)
- [1382369_2.webm](attachments/1382369_2.webm) (video/webm, 2.1 MB)
- [non_patch_asan.txt](attachments/non_patch_asan.txt) (text/plain, 25.0 KB)
- [main.js](attachments/main.js) (text/plain, 124 B)
- [manifest.json](attachments/manifest.json) (text/plain, 176 B)

## Timeline

### ha...@gmail.com (2022-11-08)

[Comment Deleted]

### ha...@gmail.com (2022-11-08)

# Details 

The lifetime of the `ScreenAIService` is bound with the `ScreenAIServiceRouter` through mojo pipe. `ScreenAIServiceRouter` is a keyed service, i.e., the lifetime of `ScreenAIService` is roughly similar with the keyed service.

When the `ScreenAIServiceRouter` is launched through `ScreenAIServiceRouter::LaunchIfNotRunning()`, it will create/bind `ScreenAIService`, and call `ScreenAIService::LoadLibrary` through mojo. 

In `ScreenAIService::LoadLibrary`, if the service haven't been loaded yet, it will post `ScreenAIService::LoadLibraryInternal` function to the background thread. 


This is problematic and leads to two UAFs here:

1. There's no mechanism to guarantee the `ScreenAIService` isn't destroyed during the `ScreenAIService::LoadLibraryInternal` execution. 
2. Since `ScreenAIService::LoadLibraryInternal` is bound with the raw this pointer by `unretained(this)`, it won't be canceled even after the `ScreenAIService` is destroyed.

When the profile is shutdown, the `ScreenAIService` will be destroyed. However, the `ScreenAIService::LoadLibraryInternal` running on the background thread will still be executed, and access the freed `library_` and `library_functions_` member variable in [4]. 

Moreover, there are multiple places to access (both reading & writing) the freed member variable in `ScreenAIService::LoadLibraryInternal` function, i.e., the `library_`, `library_functions_`, the `CallInitVisualAnnotationsFunction` function which also access the freed `library_functions_`, `CallEnableDebugMode` function which access the freed `library_functions_`. Those access places increase the UAF window to acceptable/practical degree between the profile shutdown and the `ScreenAIService::LoadLibraryInternal` execution in another thread, make it easier to expolit.


Additionally, the comment of `unretained(this)` usage in `ScreenAIService::LoadLibrary` function says

// This object gets destroyed only when service is shutting down, so unless
// the service would be destroyed immediately after LoadLibrary request is
// triggered, using 'this' unretained is safe.

This is not true actually, since even if we still need to destroy the service after the `LoadLibrary`, we don't require the `immediately` time. Ideally, since the background thread could be blocked (which could done easily by a compromised renderer), combing the aforementioned multiple UAF places, the racing window for the UAF is large enough to be practical.


[1]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/cpp/screen_ai_service_router.cc;l=58-62;drc=38bff96f36fb3980fef273c1066ba65a7b32da7c

  content::ServiceProcessHost::Launch(
      screen_ai_service_.BindNewPipeAndPassReceiver(),
      content::ServiceProcessHost::Options()
          .WithDisplayName("Screen AI Service")
          .Pass());

[2]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/cpp/screen_ai_service_router_factory.cc;l=34-37;drc=38bff96f36fb3980fef273c1066ba65a7b32da7c

[3]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/cpp/screen_ai_service_router.cc;l=70-72;drc=38bff96f36fb3980fef273c1066ba65a7b32da7c

    screen_ai_service_->LoadLibrary(
        std::move(model_files->screen2x_model_config_),
        std::move(model_files->screen2x_model_), library_path);

[4]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/screen_ai_service_impl.cc;l=115-145;drc=55fdf4da7255536a8c69911ec73e176b039615a1

void ScreenAIService::LoadLibraryInternal(base::File model_config,
                                          base::File model_tflite,
                                          const base::FilePath& library_path) {
  DCHECK(!content::BrowserThread::CurrentlyOn(content::BrowserThread::UI));
  library_ = base::ScopedNativeLibrary(library_path);  // [4] access the freed `library_`
  library_functions_.LoadFunctions(library_);  // [4] access the freed `library_functions_`
  if (features::IsScreenAIDebugModeEnabled())  
    CallEnableDebugMode();
  bool init_ok = true;
#if !BUILDFLAG(IS_WIN)
  if (features::IsPdfOcrEnabled() ||
      features::IsScreenAIVisualAnnotationsEnabled()) {
    if (!CallInitVisualAnnotationsFunction(library_path.DirName())) {   // [4] the CallInitVisualAnnotationsFunction function will still access the freed `library_functions_`
      init_ok = false;
      // TODO(https://crbug.com/1278249): Add UMA metrics to monitor failures.
    }
  }
#endif

  if (init_ok && features::IsReadAnythingWithScreen2xEnabled()) {
    if (!CallInitMainContentExtractionFunction(model_config, model_tflite)) {
      // TODO(https://crbug.com/1278249): Add UMA metrics to monitor failures.
      init_ok = false;
    }
  }

  if (!init_ok) {
    VLOG(0) << "Screen AI library initialization failed.";
    base::Process::TerminateCurrentProcessImmediately(-1);
  }
}

# bisect

This UAF is introduced in the commit https://chromium-review.googlesource.com/c/chromium/src/+/3975612. 
The impacted chromium version ranging from 109.0.5407.0 to the latest 109.0.5408.2

# Patch suggestion

We'd better rewrite the `LoadLibraryInternal` function to the static one, and get the loaded `library_`/`library_functions_` from the post task result, which could avoid the UAFs here.

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-08)

Thank you for your report. I'm unsure how an attacker would make use of this issue to put our users at risk? It seems this requires the profile to shut down before the initial load of the library to complete? Do you know how an attacker might accomplish this?

[Monorail components: UI>Accessibility]

### wf...@chromium.org (2022-11-08)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-09)

Thanks for the quick reply. There are many ways to reproduce this UAF and is web-accessible.

Note that the initial load of the ScreenAI library is not related with the profile initialization. Moreover, the library initialization could be trigger by many ways, one of the web-accessiable ways is to embed an pdf file in the html, trigger the PdfOcr component to indirectly start the ScreenAI service, and finally trigger the ScreenAI library initialization.

I will explain some reproduction ways on MacOS:

[1] The web-accessible method:

1. host the attached `fake.pdf`, `poc1.html`
2. apply the `patch.diff` patch, the patch simulate the possible thread blocking on the background thread, which make it more easy to reproduce. Please note that this patch could be achieve easily by a compromise renderer to block/stuck the victim's threads/cpus by OOM request, etc
3. Visit the poc1.html by:

./Chromium.app/Contents/MacOS/Chromium  --enable-features=ScreenAI,PdfOcr http://localhost:8000/poc1.html

the UAF stack is attached as `asan1.txt`.

Additional analysis about this method:

Note that on MacOS, even if the user has only one profile, we could still leverage this UAF to achieve more exploit. Since closing the only window of the only profile, the browser instance itself doesn't destroyed, hence this web-accessible method doesn't much migrated by the profile shutdown. 

On other platform, since the PdfOcr detection, (i.e., the ScreenAI library loading stage) could be controlled by the web page, by the time the attacker want to close the page, it could leverage OOM or other recourses-exhaust request to block/stuck the host cpu, combining the aforementioned multiple UAFs access places and the uncancelable `LoadLibraryInternal` binding, making this UAF much practical to expolit. Since all of the UAF condition could be controlled by the remote attacker, the mitigation seems negligible.


[2] Leverage ReadAnything to trigger the ScreenAI service:

1. Also please apply the `patch.diff`.
2. run chromium:

./Chromium.app/Contents/MacOS/Chromium  --enable-features=ScreenAI,ReadAnything,ReadAnythingWithScreen2x

3. Open side panel, visit Read anything, and close the current window. (Note that this is not close the browser, since we only need to shutdown the current service instance.)

the UAF stack of this method is attached as `asan2.txt`


### ha...@gmail.com (2022-11-09)

Attached two reproduction video corresponding to the above two methods.

### ha...@gmail.com (2022-11-09)

Demonstration on the the above reproduction methods:

### For the web-accessible method (no user-interaction required)

When the PdfOcr feature is enabled, and if a loaded web page contains pdf frame, the `PdfAccessibilityTree` will be built, and it creates the `PdfOcrService`[1]. `PdfOcrService` will bind the `ScreenAIAnnotator` [2] and eventually initialize/use the `ScreenAIService`, triggers the UAF-problematic `ScreenAIService::LoadLibrary` function.

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/pdf/renderer/pdf_accessibility_tree.cc;l=1228-1232;drc=fb406c65738a42757aed8c7702906f258e303867

    content::RenderAccessibility* render_accessibility =
        GetRenderAccessibilityIfEnabled();
    DCHECK(render_accessibility);
    ocr_service_ = std::make_unique<PdfOcrService>(       // [1]
        render_accessibility->GetTreeIDForPluginHost(), *render_frame);

[2]https://source.chromium.org/chromium/chromium/src/+/main:components/pdf/renderer/pdf_accessibility_tree.cc;l=58-61;drc=fb406c65738a42757aed8c7702906f258e303867

  PdfOcrService(const ui::AXTreeID& parent_tree_id,
                content::RenderFrame& render_frame)
      : parent_tree_id_(parent_tree_id) {
    if (features::IsPdfOcrEnabled()) {
      render_frame.GetBrowserInterfaceBroker()->GetInterface(
          screen_ai_annotator_.BindNewPipeAndPassReceiver()); // [2]
    }
  }

### For the ReadAnything method (user-interaction needed)

When ReadAnythingWithScreen2x feature is enabled, `AXTreeDistiller` will bind & launch the ScreenAIService [3] through `BindMainContentExtractor` mojo pipe [4] by the `ScreenAIServiceRouter`, in `LaunchIfNotRunning` function [5]. `LaunchIfNotRunning` will eventually triggers the UAF-problematic `ScreenAIService::LoadLibrary` function in [6].

[3]https://source.chromium.org/chromium/chromium/src/+/main:content/renderer/accessibility/ax_tree_distiller.cc;l=87-90;drc=dee3baf387b5a58fced7eced99464829c7ef8a24

[4]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/mojom/screen_ai_service.mojom;l=78-79;drc=dee3baf387b5a58fced7eced99464829c7ef8a24

[5]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/cpp/screen_ai_service_router.cc;l=75-81;drc=dee3baf387b5a58fced7eced99464829c7ef8a24

void ScreenAIServiceRouter::BindMainContentExtractor(
    mojo::PendingReceiver<mojom::Screen2xMainContentExtractor> receiver) {
  LaunchIfNotRunning();  // [5]

  if (screen_ai_service_.is_bound())
    screen_ai_service_->BindMainContentExtractor(std::move(receiver));
}


[6]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/cpp/screen_ai_service_router.cc;l=112-115;drc=dee3baf387b5a58fced7eced99464829c7ef8a24


All in all, when one of the ReadAnythingWithScreen2x, ScreenAI, PdfOcr features is enabled, the ScreenAIService become available [7].

[7]https://source.chromium.org/chromium/chromium/src/+/main:ui/accessibility/accessibility_features.cc;l=313-316;drc=38bff96f36fb3980fef273c1066ba65a7b32da7c

bool IsScreenAIServiceNeeded() {
  return IsPdfOcrEnabled() || IsScreenAIVisualAnnotationsEnabled() ||
         IsReadAnythingWithScreen2xEnabled();
}

### ha...@gmail.com (2022-11-09)

Since the `ScreenAIService::LoadLibrary` originates from another background thread's result schedule [1], the window is large enough for web-accessible method to expolit. Hence the previous mentioned `patch.diff` is not required. That's to say, without any patch, we could achieve the UAF easily by the web-accessible method. I've succeed it and attached its asan stack as `non_patch_asan.txt`/

Moreover, I found the third UAF in [1], i.e., the usage of the PostTaskAndReplyWithResult is also problematic since it incorrectly bind the unretained raw this pointer, which could be freed after the profile shutdown. The reproduce method for this third UAF is similar with this issue. However, since the root cause and the UAF place is different with this issue (that happens in ScreenAIServiceRouter, while this issue focus on ScreenAIService), I'll open an new issue to report it.

[1]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/cpp/screen_ai_service_router.cc;l=112-115;drc=dee3baf387b5a58fced7eced99464829c7ef8a24

  base::ThreadPool::PostTaskAndReplyWithResult(
      FROM_HERE,
      {base::MayBlock(), base::TaskShutdownBehavior::SKIP_ON_SHUTDOWN},
      base::BindOnce(&ComponentModelFiles::LoadComponentFiles),
      base::BindOnce(
          [](ScreenAIServiceRouter* service_router,
             std::unique_ptr<ComponentModelFiles> model_files) {
            service_router->screen_ai_service_->LoadLibrary(    // [1]
                std::move(model_files->screen2x_model_config_),
                std::move(model_files->screen2x_model_),
                model_files->library_binary_path_);
          },
          base::Unretained(this)));

### ha...@gmail.com (2022-11-09)

Since the `ScreenAIService::LoadLibrary` originates from another background thread's result schedule [1], the window is large enough for web-accessible method to expolit. Hence the previous mentioned `patch.diff` is not required. That's to say, without any patch, we could achieve the UAF easily by the web-accessible method. I've succeed it and attached its asan stack as `non_patch_asan.txt`.

Moreover, I found the third UAF in [1], i.e., the usage of the PostTaskAndReplyWithResult is also problematic since it incorrectly bind the unretained raw this pointer, which could be freed after the profile shutdown. The reproduce method for this third UAF is similar with this issue. However, since the root cause and the UAF place is different with this issue (that happens in ScreenAIServiceRouter, while this issue focus on ScreenAIService), I'll open an new issue to report it.

[1]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/cpp/screen_ai_service_router.cc;l=112-115;drc=dee3baf387b5a58fced7eced99464829c7ef8a24

  base::ThreadPool::PostTaskAndReplyWithResult(
      FROM_HERE,
      {base::MayBlock(), base::TaskShutdownBehavior::SKIP_ON_SHUTDOWN},
      base::BindOnce(&ComponentModelFiles::LoadComponentFiles),
      base::BindOnce(
          [](ScreenAIServiceRouter* service_router,
             std::unique_ptr<ComponentModelFiles> model_files) {
            service_router->screen_ai_service_->LoadLibrary(    // [1]
                std::move(model_files->screen2x_model_config_),
                std::move(model_files->screen2x_model_),
                model_files->library_binary_path_);
          },
          base::Unretained(this)));

### ha...@gmail.com (2022-11-09)

Moreover, since ScreenAIService is available in the incognito mode, we could also leverage an extension to achieve this UAF, hence profile shutdown is not required.

i.e., the extension could create an incognito window, which visit the aforementioned web page poc and close it, and doesn't require profile shutdown anymore.

I reproduced with the attached extension on 109.0.5409.0 chromium as well.

./Chromium.app/Contents/MacOS/Chromium -enable-features=ReadAnything,ReadAnythingWithScreen2x,ScreenAI,PdfOcr --force-renderer-accessibility --load-extension=/path/to/ext

### rh...@chromium.org (2022-11-09)

Thank you for reporting the issue.

I leave severity assessment of the issue to security reviewers, I have  a CL to fix it: crrev.com/c/4016407

### ha...@gmail.com (2022-11-09)

Thank you very much for the quick candidate fix. 

As for https://crbug.com/chromium/1382369#c10, the UAF in ScreenAIServiceRouter I report previously in detail is https://crbug.com/chromium/1382690, maybe we could add bug: 1382690 in the candidate fix if possible, since this fix also related with the ScreenAIServiceRouter. Moreover, the candidate fix LGTM.

### rh...@chromium.org (2022-11-09)

I don't have access to https://crbug.com/chromium/1382690, can someone give me permission?

### wf...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/26ae6b74f6e2323266ac6f7e49fbe5fa50b46bf3

commit 26ae6b74f6e2323266ac6f7e49fbe5fa50b46bf3
Author: Ramin Halavati <rhalavati@chromium.org>
Date: Thu Nov 10 06:45:05 2022

Fix possible UAFs on ScreenAI service.

ScreenAI service router and implementation are updated to remove the
possibility of UAF when profiles are closing.

Bug: 1382369, 1382690, 1278249
Change-Id: Ia3d21464daddb81ec93bcef828b3a4f2a15dc118
Ax-Relnotes: n/a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4016407
Reviewed-by: David Tseng <dtseng@chromium.org>
Commit-Queue: Ramin Halavati <rhalavati@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1069623}

[modify] https://crrev.com/26ae6b74f6e2323266ac6f7e49fbe5fa50b46bf3/components/services/screen_ai/public/cpp/screen_ai_service_router.h
[modify] https://crrev.com/26ae6b74f6e2323266ac6f7e49fbe5fa50b46bf3/components/services/screen_ai/screen_ai_service_impl.cc
[modify] https://crrev.com/26ae6b74f6e2323266ac6f7e49fbe5fa50b46bf3/components/services/screen_ai/public/cpp/screen_ai_service_router.cc
[modify] https://crrev.com/26ae6b74f6e2323266ac6f7e49fbe5fa50b46bf3/components/services/screen_ai/screen_ai_service_impl.h


### rh...@chromium.org (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-10)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-10)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-12)

Not requesting merge to dev (M109) because latest trunk commit (1069623) appears to be prior to dev branch point (1070088). If this is incorrect, please replace the Merge-NA-109 label with Merge-Request-109. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-18)

Congratulations! The VRP Panel has decided to award you $1,500 for this report of a moderately mitigated bug in a sandboxed process + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-17)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1382369?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### ni...@google.com (2024-06-18)

marking verified per comment 19

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061649)*
