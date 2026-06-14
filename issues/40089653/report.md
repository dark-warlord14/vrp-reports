# Cross-origin Shared Worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40089653](https://issues.chromium.org/issues/40089653) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | nh...@chromium.org |
| **Created** | 2017-11-20 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/2.html
2. Open another tab and go to https://vuln.shhnjk.com/2.html
3. Click on stop button on one tab

What is the expected behavior?
other tab keeps counting and does not stop (SharedWorker won't be established between cross-origin)

What went wrong?
In https://html.spec.whatwg.org/multipage/workers.html#sharedworker, step 11.2's note of "When the SharedWorker(scriptURL, options) constructor is invoked:"  says

data: URLs create a worker with an opaque origin. Both the constructor origin and constructor url are compared so the same data: URL can be used within an origin to get to the same SharedWorkerGlobalScope object, but cannot be used to bypass the same origin restriction.

This is not the case in Chrome and cross-origin site can create SharedWorker using data URL SharedWorker script. 

Did this work before? N/A 

Chrome version: 62.0.3202.94  Channel: stable
OS Version: 10.0
Flash Version:

## Timeline

### mm...@chromium.org (2017-11-20)

Hiroki, could you please take a look?

It reproduces on Linux as well.

[Monorail components: Blink>ServiceWorker]

### nh...@chromium.org (2017-11-20)

[Empty comment from Monorail migration]

[Monorail components: -Blink>ServiceWorker Blink>Workers]

### nh...@chromium.org (2017-11-21)

Thank you for reporting this.

Looks like URL matching logic (SharedWorkerInstance::Matches()) is not correct for Data URL. Data URL has an empty origin and can pass the logic. Probably we should compare "constructor origin" set to "outside settings's origin"[1] instead of a given URL's origin.

[1] https://html.spec.whatwg.org/multipage/workers.html#run-a-worker


### nh...@chromium.org (2017-11-21)

Bumping up the priority because this is a security issue to bypass the same origin policy...

### fa...@chromium.org (2017-11-21)

Related to https://crbug.com/chromium/270979 and https://www.chromestatus.com/feature/5633342665916416?

Seems like https://groups.google.com/a/chromium.org/forum/#!msg/blink-dev/6otx9aZlwEo/ddfnO5gTCAAJ had a lot of discussion about the security model.

### nh...@chromium.org (2017-11-21)

falken@: Thank you for sharing information!

WIP CL (I'll add tests):
https://chromium-review.googlesource.com/c/chromium/src/+/781539

### mm...@chromium.org (2017-11-21)

[Empty comment from Monorail migration]

### pa...@chromium.org (2017-11-28)

nhiroki: Friendly ping. :) 

### nh...@chromium.org (2017-11-28)

I'm still working on the CL to fix this in M64:
https://chromium-review.googlesource.com/c/chromium/src/+/781539

### bu...@chromium.org (2017-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/018bb6d300c11acb953d51ef3cbec4cdcaf4a652

commit 018bb6d300c11acb953d51ef3cbec4cdcaf4a652
Author: Hiroki Nakagawa <nhiroki@chromium.org>
Date: Thu Nov 30 03:31:37 2017

SharedWorker: Introduce "constructor origin" concept defined in the spec

This CL introduces the "constructor origin" concept defined in the HTML spec:
https://html.spec.whatwg.org/multipage/workers.html#concept-sharedworkerglobalscope-constructor-origin

Bug: 787103
Change-Id: I273629760bb34e0c24f1c4d023e66e146a476407
Reviewed-on: https://chromium-review.googlesource.com/781539
Reviewed-by: Raymes Khoury <raymes@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Commit-Queue: Hiroki Nakagawa <nhiroki@chromium.org>
Cr-Commit-Position: refs/heads/master@{#520417}
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/browsing_data/browsing_data_shared_worker_helper.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/browsing_data/browsing_data_shared_worker_helper.h
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/browsing_data/browsing_data_shared_worker_helper_unittest.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/browsing_data/cookies_tree_model.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/browsing_data/mock_browsing_data_shared_worker_helper.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/browsing_data/mock_browsing_data_shared_worker_helper.h
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/chrome_content_browser_client.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/chrome_content_browser_client.h
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/content_settings/tab_specific_content_settings.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/chrome/browser/content_settings/tab_specific_content_settings.h
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/browser/devtools/shared_worker_devtools_manager_unittest.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/browser/shared_worker/shared_worker_instance.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/browser/shared_worker/shared_worker_instance.h
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/browser/shared_worker/shared_worker_instance_unittest.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/browser/shared_worker/shared_worker_service_impl.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/browser/shared_worker/shared_worker_service_impl.h
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/browser/shared_worker/shared_worker_service_impl_unittest.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/public/browser/content_browser_client.cc
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/public/browser/content_browser_client.h
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/content/public/browser/shared_worker_service.h
[add] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/third_party/WebKit/LayoutTests/external/wpt/workers/data-url-shared-window.html
[modify] https://crrev.com/018bb6d300c11acb953d51ef3cbec4cdcaf4a652/third_party/WebKit/LayoutTests/external/wpt/workers/data-url-shared.html


### nh...@chromium.org (2017-11-30)

[Empty comment from Monorail migration]

### nh...@chromium.org (2017-11-30)

Android doesn't support SharedWorker.

### sh...@chromium.org (2017-11-30)

[Empty comment from Monorail migration]

### aw...@google.com (2017-12-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-12-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-08)

Nice on s.h.h.n.j.k@! The VRP panel decided to award $2,000 for this report. Cheers!

### aw...@chromium.org (2017-12-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-15)

This bug requires manual review: M64 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-12-18)

abdulsyed@ - good for M64

### ab...@chromium.org (2017-12-18)

nhiroki@ - this seems like a very large change overall and is touching some key directories. Can you please comment on whether this is absolutely needed for M64 vs waiting until M65? How well tested is this? Are we confident it won't break anything?

### ab...@chromium.org (2017-12-18)

On a second look, seems like this is already in M64 and made it before branch. Removing Merge-Request label. 

https://chromium.googlesource.com/chromium/src.git/+/018bb6d300c11acb953d51ef3cbec4cdcaf4a652

### nh...@chromium.org (2017-12-18)

Sorry for the late comment. I didn't notice the automatic merge request. Yes, this should already be in M64.

$ git find-releases 018bb6d300c11acb953d51ef3cbec4cdcaf4a652
commit 018bb6d300c11acb953d51ef3cbec4cdcaf4a652 was:
  initially in 64.0.3282.0

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/787103?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089653)*
