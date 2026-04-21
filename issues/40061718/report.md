# Security: UAF in lens::LensStaticPageController::LoadChromeLens

| Field | Value |
|-------|-------|
| **Issue ID** | [40061718](https://issues.chromium.org/issues/40061718) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | ju...@google.com |
| **Created** | 2022-11-13 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This UAF was introduced in recent commit: <https://source.chromium.org/chromium/chromium/src/+/9b85c864a06815cab2bd9495c3b93a779b7153ef> .

1. In LensStaticPageController::OpenStaticPage[0](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/lens/lens_static_page_controller.cc;l=43-47;drc=9b85c864a06815cab2bd9495c3b93a779b7153ef), load\_url\_callback is bind with this pointer and pass to ui::GrabWindowSnapshotAsync
2. The callback is passed through [1](https://source.chromium.org/chromium/chromium/src/+/main:ui/snapshot/snapshot_aura.cc;l=126;drc=5a691c7c1c46421b2fa7ff3cd3b5f79470ed3808): ui::GrabWindowSnapshotAsync → GrabWindowSnapshotAsyncAura → MakeInitialAsyncCopyRequest → MakeAsyncCopyRequest
3. In function MakeAsyncCopyRequest[2](https://source.chromium.org/chromium/chromium/src/+/main:ui/snapshot/snapshot_aura.cc;l=31-44;drc=5a691c7c1c46421b2fa7ff3cd3b5f79470ed3808), an instance of viz::CopyOutputRequest is created and the callback is stored result\_callback\_[3](https://source.chromium.org/chromium/chromium/src/+/main:components/viz/common/frame_sinks/copy_output_request.h;l=170;drc=5a691c7c1c46421b2fa7ff3cd3b5f79470ed3808)
4. When copy output request is done, SendResult[4](https://source.chromium.org/chromium/chromium/src/+/main:components/viz/common/frame_sinks/copy_output_request.cc;l=143-158;drc=5a691c7c1c46421b2fa7ff3cd3b5f79470ed3808) will be called. In this function, the result\_callback\_ will be posted to the result task runner |base::SequencedTaskRunnerHandle::Get()| and then executed asynchronously.
5. Let’s go back to the callback function LensStaticPageController::LoadChromeLens [5](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/lens/lens_static_page_controller.cc;l=55;drc=9b85c864a06815cab2bd9495c3b93a779b7153ef), in line 55 raw pointer browser\_ is accessed. However, this browser\_ cloud be freed when the callback executing. UAF here.

**VERSION**

Chrome Version: 9b85c864a06815cab2bd9495c3b93a779b7153ef  

Operating System: Linux, Windows using Aura, ChromeOS

**REPRODUCTION CASE**  

Note: is\_chrome\_branded = true is required. This setting is meant for building Google Chrome and not Chromium and it depends on some closed source code. So I couldn’t reproduce it directly, sorry for that.

However, I think the following steps cloud be work.

1. apply the patch: copy\_output\_request.cc.patch for easy reproduction.
2. Run chrome with flag: ./out/Default/chrome --enable-features=LensRegionSearchStaticPage
3. Open two browser window.
4. In one of the browser window, right click and trigger context menu item with commit id: IDC\_CONTENT\_CONTEXT\_LENS\_REGION\_SEARCH or IDC\_CONTENT\_CONTEXT\_WEB\_REGION\_SEARCH, ExecRegionSearch will be called. Now close this window.
5. Wait for the UAF

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

Reporter credit: Chaobin Zhang

## Attachments

- [copy_output_request.cc.patch](attachments/copy_output_request.cc.patch) (text/plain, 1.7 KB)
- [asan.log](attachments/asan.log) (text/plain, 26.8 KB)

## Timeline

### [Deleted User] (2022-11-13)

[Empty comment from Monorail migration]

### zh...@gmail.com (2022-11-13)

I also create a possible fix for this problem: https://chromium-review.googlesource.com/c/chromium/src/+/4025044

By the way, in the reproduction step 4, trigger ExecRegionSearch and close should quicker than the callback is executed. The patch in step 1 post a sleep task to the runner, which can help us win this race easily.

### wf...@chromium.org (2022-11-14)

analysis looks reasonable but I haven't yet reproduced. Also the bisect is reasonable.

I'm assigning to juanmojica to take a look at. Please consider reverting https://chromium-review.googlesource.com/c/chromium/src/+/4018087 if this issue cannot be quickly fixed.

Please create a component for Lens in monorail so this bug and others can be more effectively triaged.



[Monorail components: UI>Browser]

### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1bc4718f746cfa3bcdc30d4b8f188d92ca10edcd

commit 1bc4718f746cfa3bcdc30d4b8f188d92ca10edcd
Author: Juan Mojica <juanmojica@google.com>
Date: Mon Nov 14 20:30:54 2022

Use weak ptr to prevent running callback if browser is freed.

Bug: 1383791
Change-Id: I4c471a29708c87cdbf0a4faa5c735dbdd870bb9e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4026587
Reviewed-by: Anudeep Palanki <apalanki@google.com>
Commit-Queue: Juan Mojica <juanmojica@google.com>
Cr-Commit-Position: refs/heads/main@{#1071189}

[modify] https://crrev.com/1bc4718f746cfa3bcdc30d4b8f188d92ca10edcd/chrome/browser/ui/views/lens/lens_static_page_controller.h
[modify] https://crrev.com/1bc4718f746cfa3bcdc30d4b8f188d92ca10edcd/chrome/browser/ui/views/lens/lens_static_page_controller.cc


### ju...@google.com (2022-11-14)

Was able to reproduce and check a fix in. Thanks!

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-15)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations, Chaobin Zhang! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### zh...@gmail.com (2022-12-02)

Thank you very much!

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-02-21)

This issue was migrated from crbug.com/chromium/1383791?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061718)*
