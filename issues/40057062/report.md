# Security: SameSite Cookie Bypass via BackgroundFetch

| Field | Value |
|-------|-------|
| **Issue ID** | [40057062](https://issues.chromium.org/issues/40057062) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>BackgroundFetch, Internals>Network>Cookies |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | la...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2021-08-28 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

BackgroundFetch sends all cookies ignoring the SameSite attribute.

**VERSION**  

Chrome Version: Version 92.0.4515.159 (Official Build) Arch Linux (64-bit)

**REPRODUCTION CASE**  

Set a cookie with `SameSite=Strict` here: <https://foregoing-sulky-carpenter.glitch.me>

Start a local webserver with `python -m http.server` hosting these files:

test.html

```
<script>  
  const url = "https://foregoing-sulky-carpenter.glitch.me/echo-cookie";  
  
  navigator.serviceWorker.ready.then(async (swReg) => {  
    const request = new Request(url, { credentials: "include" });  
  
    const bgFetch = await swReg.backgroundFetch.fetch("test", [request]);  
  
    const targetPage = await bgFetch.match(url);  
    const response = await targetPage.responseReady;  
    console.log("Background Fetch:", await response.text()); // contains cookie  
  
    const normalFetch = await fetch(request);  
    console.log("Fetch:", await normalFetch.text()); // no cookie  
  });  
  
  navigator.serviceWorker.register("sw.js");  
</script>  

```

sw.js

```
// can be empty  

```

The response of the bgFetch request contains the cookie set with SameSite=Strict.

**CREDIT INFORMATION**  

Maurice Dauer

## Timeline

### [Deleted User] (2021-08-28)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-28)

This does reproduce as claimed. Triaging to a BackgroundFetch owner.

[Monorail components: Blink>BackgroundFetch Internals>Network>Cookies]

### [Deleted User] (2021-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-11)

peter: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-26)

rayankans: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2021-09-27)

Sorry I just saw this.

This has been fixed in the other bug: crbug.com/1239709

### ra...@chromium.org (2021-09-27)

Also the fixes have been merged back to M94

### ra...@chromium.org (2021-09-27)

[Empty comment from Monorail migration]

### la...@gmail.com (2021-09-27)

I'm afraid this bug hasn't been fixed with https://crbug.com/chromium/1239709, it does still reproduce for me on version 94.0.4606.61. The credentials mode is now correctly applied and checked, but the SameSite attribute of cookies is not respected, only cookies with a `SameSite=None` attribute should be sent with CORS requests.
The reproduction case in the initial report demonstrates that the cookie set with a `SameSite=Strict` attribute is included in a BackgroundFetch request, but not in a request made with fetch.

### ra...@chromium.org (2021-09-27)

Re-opening the bug

### ra...@chromium.org (2021-09-27)

cc: xingliu
Xing, any ideas why the Download Service is not respecting the SameSite attribute of cookies?

### la...@gmail.com (2021-09-27)

I may be wrong here since I'm not really familiar with C++ and the codebase, but looking at the code it seems like the setting that is used to check which SameSite cookies should be sent is here[1] and the url value that is used there seems to come from here[2] which is the request url thus causing all SameSite cookies to be sent.

[1] https://source.chromium.org/chromium/chromium/src/+/main:components/download/internal/common/download_utils.cc;drc=cd8e2bf106ae1083d18a0246f644f1623740db26;l=293
[2] https://source.chromium.org/chromium/chromium/src/+/main:components/background_fetch/background_fetch_delegate_base.cc;drc=9834395f60edc393922232e5194b4e299b6174e9;l=97



### ra...@chromium.org (2021-09-27)

Yeah, I think we need to set up the proper isolation info and it should work.

Xing, is this something that can be set internally through the DownloadService, or should it be exposed in download::DownloadParams for clients to pass along?

### xi...@chromium.org (2021-09-27)

per https://crbug.com/chromium/1244289#c15, yeah, I can do the plumbing of isolation info.

The correct isolation info probably needs to pass from the caller to background download service, since the API doesn't know whether the download URL is in a main frame or subframe.

Example:
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_impl.cc;l=4815;drc=9834395f60edc393922232e5194b4e299b6174e9;bpv=1;bpt=1

### xi...@chromium.org (2021-09-27)

[Empty comment from Monorail migration]

### xi...@chromium.org (2021-09-27)

Isolation info can be cached to DownloadItem, but probably doesn't need to be persisted to db, since we won't know which site triggered the fetch api in a new browser session during download resumption.

### gi...@appspot.gserviceaccount.com (2021-09-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/91049ef77f5e1e7faf62ccf5ea059ce950324991

commit 91049ef77f5e1e7faf62ccf5ea059ce950324991
Author: Xing Liu <xingliu@chromium.org>
Date: Tue Sep 28 22:25:59 2021

Download: Add isolation info to background download service.

Background download service now supports to set the isolation info to
control the cookie to set for SameSite response header attribute.

Bug: 1244289
Change-Id: Ifd46ee773d4b58110ad5c12784b9039a54d22519
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3188755
Reviewed-by: Min Qin <qinmin@chromium.org>
Reviewed-by: Ryan Hamilton <rch@chromium.org>
Commit-Queue: Xing Liu <xingliu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#925975}

[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/public/common/download_item.h
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/content/browser/download/download_browsertest.cc
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/public/background_service/DEPS
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/internal/common/download_create_info.cc
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/public/common/download_create_info.h
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/public/common/mock_download_item.h
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/content/public/test/fake_download_item.cc
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/public/background_service/download_params.cc
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/content/public/test/fake_download_item.h
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/public/background_service/download_params.h
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/public/common/download_item_impl.h
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/91049ef77f5e1e7faf62ccf5ea059ce950324991/components/download/internal/background_service/in_memory_download.cc


### xi...@chromium.org (2021-09-28)

Assigning back to rayankans@ for background fetch side change. components/download/public/background_service/download_params.h now can set isolation info.

### gi...@appspot.gserviceaccount.com (2021-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f21e4d56847aecb3af7861b3e4ec9a4aaf47ca7

commit 0f21e4d56847aecb3af7861b3e4ec9a4aaf47ca7
Author: Rayan Kanso <rayankans@google.com>
Date: Wed Oct 06 09:40:39 2021

Add the ability to Serialize/Deserialize net::IsolationInfo

Bug: 1244289
Change-Id: Iff47c77bf8470ad8f96dfd401b2f0587fd23a8da
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3198085
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#928605}

[add] https://crrev.com/0f21e4d56847aecb3af7861b3e4ec9a4aaf47ca7/net/base/isolation_info.proto
[modify] https://crrev.com/0f21e4d56847aecb3af7861b3e4ec9a4aaf47ca7/net/base/isolation_info.cc
[modify] https://crrev.com/0f21e4d56847aecb3af7861b3e4ec9a4aaf47ca7/net/base/isolation_info_unittest.cc
[modify] https://crrev.com/0f21e4d56847aecb3af7861b3e4ec9a4aaf47ca7/net/base/isolation_info.h
[modify] https://crrev.com/0f21e4d56847aecb3af7861b3e4ec9a4aaf47ca7/net/BUILD.gn


### gi...@appspot.gserviceaccount.com (2021-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fd260c29e002327aa30d4ee4c434880e273bd935

commit fd260c29e002327aa30d4ee4c434880e273bd935
Author: Rayan Kanso <rayankans@google.com>
Date: Tue Oct 12 15:05:10 2021

[BackgroundFetch] Pass isolation info to the download service

Bug: 1244289
Change-Id: I79f0f76abc699022d517ef0ee8f422832a94124f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3194254
Reviewed-by: Ken Buchanan <kenrb@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Commit-Position: refs/heads/main@{#930549}

[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_job_controller.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_job_controller.h
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_service_unittest.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/public/browser/background_fetch_description.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_context.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/storage/get_initialization_data_task.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch.proto
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_service_impl.h
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/public/browser/background_fetch_description.h
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_scheduler.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_data_manager.h
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_context.h
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/storage/get_initialization_data_task.h
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_scheduler.h
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/storage/create_metadata_task.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/storage/create_metadata_task.h
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_data_manager_unittest.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_data_manager_observer.h
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_scheduler_unittest.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/browser_interface_binders.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_job_controller_unittest.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_service_impl.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_data_manager.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/components/background_fetch/background_fetch_delegate_base.cc
[modify] https://crrev.com/fd260c29e002327aa30d4ee4c434880e273bd935/content/browser/background_fetch/background_fetch_delegate_proxy_unittest.cc


### ra...@chromium.org (2021-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Congratulations, Maurice! The VRP Panel has decided to award you $3000 for this report. Thank you for reporting this issue to us! 

### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### la...@gmail.com (2021-11-02)

I looked at the fix and it can be bypassed by redirecting from site A to site B, which leads to the request to site B containing all cookies regardless of the SameSite attribute. Should I open a new issue?

### ad...@google.com (2021-11-09)

Thanks, I raised https://crbug.com/chromium/1268580 for the problem you describe in https://crbug.com/chromium/1244289#c29 and cc'd you there.

### ad...@google.com (2021-11-09)

(Sheriffbot didn't ask for merges here. That Sheriffbot bug is tracked as https://crbug.com/chromium/1262390).

### am...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-11-12)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1244289?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>BackgroundFetch, Internals>Network>Cookies]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057062)*
