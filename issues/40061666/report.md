# UAF in ScreenAIServiceRouter

| Field | Value |
|-------|-------|
| **Issue ID** | [40061666](https://issues.chromium.org/issues/40061666) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Accessibility |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2022-11-09 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**  

Will attach details soon.

**Problem Description:**  

browser UAF

**Additional Comments:**

\*\*Chrome version: \*\* 109.0.5407.0 \*\*Channel: \*\* Canary

**OS:** Mac OS

## Attachments

- [asan1.txt](attachments/asan1.txt) (text/plain, 29.8 KB)
- [asan2.txt](attachments/asan2.txt) (text/plain, 29.7 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 719 B)
- [fake1.pdf](attachments/fake1.pdf) (application/pdf, 8 B)
- [poc1.html](attachments/poc1.html) (text/plain, 186 B)
- [1382690_read_anything.webm](attachments/1382690_read_anything.webm) (video/webm, 3.5 MB)
- [1382690_web.webm](attachments/1382690_web.webm) (video/webm, 3.8 MB)
- [main.js](attachments/main.js) (text/plain, 124 B)
- [manifest.json](attachments/manifest.json) (text/plain, 176 B)
- [1382690_with_ext.webm](attachments/1382690_with_ext.webm) (video/webm, 2.8 MB)

## Timeline

### [Deleted User] (2022-11-09)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-11-09)

[Comment Deleted]

### ha...@gmail.com (2022-11-09)

# Details 

This issue is similar with the previous reported https://crbug.com/chromium/1382369, however, the root cause is different and it happened on the different places. Hence I report it with a new issue.

`ScreenAIServiceRouter` is a keyed service [1]. When the `ScreenAIServiceRouter` tries to launch ScreenAIService in `ScreenAIServiceRouter::LaunchIfNotRunning()` according to the source component (including ScreenAIAnnotator, MainContentExtractor), it will post a task to the background thread and bind the lamnbda function with the raw this pointer in [2]. 

The `Unretained(this)` usage here is problematic because the `ScreenAIServiceRouter` (i.e., the `service_router` argument in the lambda function) could be freed before the lambda function is executed. Moreover, the lambda function can't be canceled, which increase the racing window to achieve UAF by blocking the background thread.

Then in the lambda function, it will access the freed `screen_ai_service_` member variable of the freed `service_router` and calls the mojo pipe function with the freed object, resulting in the UAF in [2]. 

[1]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/cpp/screen_ai_service_router_factory.cc;l=34-37;drc=dee3baf387b5a58fced7eced99464829c7ef8a24

[2]https://source.chromium.org/chromium/chromium/src/+/main:components/services/screen_ai/public/cpp/screen_ai_service_router.cc;l=105-117;drc=dee3baf387b5a58fced7eced99464829c7ef8a24

  base::ThreadPool::PostTaskAndReplyWithResult(
      FROM_HERE,
      {base::MayBlock(), base::TaskShutdownBehavior::SKIP_ON_SHUTDOWN},
      base::BindOnce(&ComponentModelFiles::LoadComponentFiles),
      base::BindOnce(
          [](ScreenAIServiceRouter* service_router,
             std::unique_ptr<ComponentModelFiles> model_files) {
            service_router->screen_ai_service_->LoadLibrary(    // [2] the service_router could be freed, causing UAF here
                std::move(model_files->screen2x_model_config_),
                std::move(model_files->screen2x_model_),
                model_files->library_binary_path_);
          },
          base::Unretained(this))); // [2] bound the raw pointer of this KeyedService to the uncancelable lambda function


# Bisect

This UAF is introduced in the commit https://chromium-review.googlesource.com/c/chromium/src/+/3975612. 

The impacted chromium version ranging from 109.0.5407.0 to the latest 109.0.5408.2


# Reproduction

The reproduction method is similar with the previous https://crbug.com/chromium/1382369. However, the racing window for this UAF is slightly narrow than the previous issue. We could still enlarge the racing window by the OOM or other recourses-exhaust request in renderer to block/stuck the host cpu, since the task is posted to the background thread, which could easily be blocked.

I will explain some reproduction ways on MacOS:

[1] The web-accessible method:

1. host the attached fake.pdf, poc1.html
2. apply the `patch.diff` patch, the patch simulate the possible thread blocking on the background thread, which make it more easy to reproduce. Please note that this patch could be achieve easily by a compromise renderer to block/stuck the victim's threads/cpus by OOM request, etc.
3. Visit the poc1.html by:

./Chromium.app/Contents/MacOS/Chromium  --enable-features=ScreenAI,PdfOcr --force-renderer-accessibility http://localhost:8000/poc1.html

the UAF stack is attached as `asan1.txt`.

Since the PdfOcr detection, (i.e., the ScreenAI library loading stage) could be controlled by the web page, by the time the attacker want to close the page, it could leverage OOM or other recourses-exhaust request to block/stuck the host cpu, combining the aforementioned multiple UAFs access places and the uncancelable lambda function [2], making this UAF much practical to expolit. Since all of the UAF condition could be controlled by the remote attacker, the mitigation seems negligible.


[2] Leverage ReadAnything to trigger the ScreenAI service:

1. Also please apply the `patch.diff`.
2. run chromium:

./Chromium.app/Contents/MacOS/Chromium  --enable-features=ScreenAI,ReadAnything,ReadAnythingWithScreen2x --force-renderer-accessibility

3. Open side panel, visit Read anything, and close the current window. (Note that this is not close the browser, since we only need to shutdown the current service instance.)

the UAF stack of this method is attached as `asan2.txt`

### ha...@gmail.com (2022-11-09)

Attached two reproduction video corresponding to the above two methods.


### ha...@gmail.com (2022-11-09)

Since ScreenAIServiceRouter is available in the incognito mode, we could also leverage an extension to achieve this UAF, hence profile shutdown is not required.

i.e., the extension could create an incognito window, which visit the aforementioned web page poc and close it, and doesn't require profile shutdown anymore.

I reproduced with the attached extension on 109.0.5409.0 chromium as well.

./Chromium.app/Contents/MacOS/Chromium -enable-features=ReadAnything,ReadAnythingWithScreen2x,ScreenAI,PdfOcr --force-renderer-accessibility --load-extension=/path/to/ext

### ha...@gmail.com (2022-11-09)

# Patch suggestion

We'd better pass the weak pointer of the `ScreenAIServiceRouter` to the lambda function, and check its validation before usage. Or we could rewrite this lambda function to a member function, and bound with the weak pointer of the `ScreenAIServiceRouter` in PostTaskAndReplyWithResult. 
In this way, we would no longer access the freed ScreenAIServiceRouter.

Also note that this UAF affects all desktop platform since the ScreenAIService/ScreenAIServiceRouter is enabled on all desktop platform. And the reproduction methods is available to other desktop platform as well.

### wf...@chromium.org (2022-11-09)

[Empty comment from Monorail migration]

### rh...@chromium.org (2022-11-09)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-09)

ty for taking this bug, rhalavati.

[Monorail components: UI>Accessibility]

### wf...@chromium.org (2022-11-09)

this bug requires ability for attacker to destroy profile which either means supply poc on command line (as reporter does) or gestures, so it's downgraded from critical to high.

### [Deleted User] (2022-11-09)

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

[Comment Deleted]

### am...@chromium.org (2022-11-18)

Congratulations on yet another this week, Chaoyuan Peng! The VRP Panel has decided to award you $4,000 for this report of a moderately mitigated security bug (this one being in the browser process) + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us!

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1382690?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ni...@google.com (2024-06-12)

marking verrified per comment 14.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061666)*
