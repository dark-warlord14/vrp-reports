# Security: ResourceTiming entries are not generated for responses with 204, 205 status codes when loaded in a iframe

| Field | Value |
|-------|-------|
| **Issue ID** | [40060392](https://issues.chromium.org/issues/40060392) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>PerformanceAPIs>ResourceTiming |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | da...@gmail.com |
| **Created** | 2022-07-24 |
| **Bounty** | $2,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

ResourceTiming entries are not generated for responses with 204, 205 status codes when loaded in a iframe. This allows  

malicious sites to infer whether or not a particular site responded with a 204, 205 status code by loading the  

victim site in a iframe.

**VERSION**  

Chrome Version: 105 (latest git commit)  

Chrome Version: 103 [stable]  

Operating System: Manjaro Linux, kernel: 5.17.15

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

1. Download attached app.py and index.html files
2. Run a python HTTP server by running `python -m http.server` in the same directory as the index.html file.
3. Install flask (`pip3 install flask`) and run the app.py file (using `python3 app.py`) in a terminal.
4. Open <http://localhost:8000/index.html> in Chrome
5. Open DevTools Console
6. <http://localhost:5000/content> should be correctly identified as having a not responding with a  
   
   204, 205 response status code, whereas <http://localhost:5000/reset-content>,  
   
   <http://localhost:5000/no-content> should be correctly identified as having a 204, 205 response status code

NOTES/PRELIMINARY INVESTIGATION

This issue appears to be present in versions of Chromium earlier than 103 based off the following comment in  

`third_party/blink/renderer/core/loader/document_loader.cc`.  

(<https://chromium-review.googlesource.com/c/chromium/src/+/1396690/5/third_party/blink/renderer/core/loader/document_loader.cc#427>)

Additionally there are wpt tests for this specific issue (which is how I came across this) under  

<https://wpt.fyi/results/resource-timing/iframe-failed-commit.html?label=experimental&label=master&aligned>  

however, the failures related to this issue are not publicly recorded due to a harness error that prevents  

these tests from being run.

**CREDIT INFORMATION**

This bug was found as part of the recent Web performance spec alignment GSoC project that  

I am working on (ccing yoav and ian who are my mentors).

## Attachments

- [app.py](attachments/app.py) (text/plain, 316 B)
- [index.html](attachments/index.html) (text/plain, 861 B)

## Timeline

### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-07-25)

Thanks for the report, I can also reproduce this in M103. Normally limited information disclosure vulnerabilities are Sev-Medium, but because this is only restricted to determining if the HTTP status code is 204 or 205, I think this is Sev-Low.

### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-02)

[Empty comment from Monorail migration]

### hi...@chromium.org (2022-08-03)

This is currently assigned to me as a reviewer/approver of https://chromium-review.googlesource.com/c/chromium/src/+/1396690/5/third_party/blink/renderer/core/loader/document_loader.cc#427 but I don't have additional context about the added comment, and I suspect the behavior has even existed before the CL 1396690 (M-73), but not sure about this.

### yo...@chromium.org (2022-08-05)

Talked to dattasohom1@ about this yesterday and they'd be taking this on.

### gi...@appspot.gserviceaccount.com (2022-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/43e57ae44aa74f979f6c206f480f04fb2bf93ea7

commit 43e57ae44aa74f979f6c206f480f04fb2bf93ea7
Author: Sohom <sohom.datta@learner.manipal.edu>
Date: Sun Nov 13 08:19:49 2022

Fix WPT test /wpt/resource-timing/iframe-failed-commit.html

- Fix harness error that caused the tests to fail regardless of pass status
- Make sure the 204/205 responses are evaluated as
empty responses with a zero body size.
- Improved reliability by providing timeouts
- Handle cases where no load events are fired

Bug: 1346924
Change-Id: I990cac59c40f2781d30d36adb8a7b91705d207eb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4005398
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Commit-Queue: Sohom Datta <dattasohom1@gmail.com>
Cr-Commit-Position: refs/heads/main@{#1070752}

[modify] https://crrev.com/43e57ae44aa74f979f6c206f480f04fb2bf93ea7/third_party/blink/web_tests/external/wpt/resource-timing/resources/entry-invariants.js
[modify] https://crrev.com/43e57ae44aa74f979f6c206f480f04fb2bf93ea7/third_party/blink/web_tests/external/wpt/resource-timing/iframe-failed-commit.html
[modify] https://crrev.com/43e57ae44aa74f979f6c206f480f04fb2bf93ea7/third_party/blink/web_tests/external/wpt/resource-timing/iframe-failed-commit-expected.txt
[modify] https://crrev.com/43e57ae44aa74f979f6c206f480f04fb2bf93ea7/third_party/blink/web_tests/external/wpt/resource-timing/resources/resource-loaders.js


### da...@gmail.com (2022-11-13)

Once https://chromium-review.googlesource.com/c/chromium/src/+/3976688 gets merged, this should be fixed. The patch above just fixes/unbreaks the tests related to the underlying issue.

### gi...@appspot.gserviceaccount.com (2022-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/588a52a6f503ca2da1c4bbc79ce790df5de3b899

commit 588a52a6f503ca2da1c4bbc79ce790df5de3b899
Author: Nancy Wang <nancylingwang@chromium.org>
Date: Mon Nov 14 02:19:07 2022

Revert "Fix WPT test /wpt/resource-timing/iframe-failed-commit.html"

This reverts commit 43e57ae44aa74f979f6c206f480f04fb2bf93ea7.

Reason for revert:
Tests are broken:
https://ci.chromium.org/p/chromium/builders/ci/Linux%20Tests/122189
https://ci.chromium.org/p/chromium/builders/ci/mac12-arm64-rel-tests
https://ci.chromium.org/p/chromium/builders/ci/Mac12%20Tests
https://ci.chromium.org/p/chromium/builders/ci/Mac10.15%20Tests
https://ci.chromium.org/p/chromium/builders/ci/Mac10.14%20Tests
https://ci.chromium.org/p/chromium/builders/ci/Mac11%20Tests
https://ci.chromium.org/p/chromium/builders/ci/Mac10.13%20Tests

Original change's description:
> Fix WPT test /wpt/resource-timing/iframe-failed-commit.html
>
> - Fix harness error that caused the tests to fail regardless of pass status
> - Make sure the 204/205 responses are evaluated as
> empty responses with a zero body size.
> - Improved reliability by providing timeouts
> - Handle cases where no load events are fired
>
> Bug: 1346924
> Change-Id: I990cac59c40f2781d30d36adb8a7b91705d207eb
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4005398
> Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
> Commit-Queue: Sohom Datta <dattasohom1@gmail.com>
> Cr-Commit-Position: refs/heads/main@{#1070752}

Bug: 1346924
Change-Id: I710074a9baa420ba4cd1540b3b06e02e9840cf1a
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4021868
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Nancy Wang <nancylingwang@chromium.org>
Auto-Submit: Nancy Wang <nancylingwang@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Nancy Wang <nancylingwang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1070838}

[modify] https://crrev.com/588a52a6f503ca2da1c4bbc79ce790df5de3b899/third_party/blink/web_tests/external/wpt/resource-timing/resources/entry-invariants.js
[modify] https://crrev.com/588a52a6f503ca2da1c4bbc79ce790df5de3b899/third_party/blink/web_tests/external/wpt/resource-timing/iframe-failed-commit.html
[modify] https://crrev.com/588a52a6f503ca2da1c4bbc79ce790df5de3b899/third_party/blink/web_tests/external/wpt/resource-timing/iframe-failed-commit-expected.txt
[modify] https://crrev.com/588a52a6f503ca2da1c4bbc79ce790df5de3b899/third_party/blink/web_tests/external/wpt/resource-timing/resources/resource-loaders.js


### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/002a658b1f77c47fb47c53ad0af8ee6346bacae5

commit 002a658b1f77c47fb47c53ad0af8ee6346bacae5
Author: Sohom <dattasohom1@gmail.com>
Date: Thu Jan 12 19:20:46 2023

Fix WPT test /wpt/resource-timing/iframe-failed-commit.html

- Fix harness error that caused the tests to fail regardless of pass status
- Make sure the 204/205 responses are evaluated as
empty responses with a zero body size.

Bug: 1346924
Change-Id: I825017fb90b1899cb1284b07f8ff887f61f41af7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4158291
Commit-Queue: Sohom Datta <dattasohom1@gmail.com>
Reviewed-by: Yoav Weiss <yoavweiss@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1091978}

[modify] https://crrev.com/002a658b1f77c47fb47c53ad0af8ee6346bacae5/third_party/blink/web_tests/external/wpt/resource-timing/resources/entry-invariants.js
[modify] https://crrev.com/002a658b1f77c47fb47c53ad0af8ee6346bacae5/third_party/blink/web_tests/external/wpt/resource-timing/iframe-failed-commit.html
[modify] https://crrev.com/002a658b1f77c47fb47c53ad0af8ee6346bacae5/third_party/blink/web_tests/external/wpt/resource-timing/iframe-failed-commit-expected.txt
[modify] https://crrev.com/002a658b1f77c47fb47c53ad0af8ee6346bacae5/third_party/blink/web_tests/external/wpt/resource-timing/resources/resource-loaders.js


### yo...@chromium.org (2023-01-16)

Looks like we're still seeing flakes: https://ci.chromium.org/ui/p/chromium/builders/ci/linux-wpt-content-shell-asan-fyi-rel/583/test-results?sortby=&groupby=

### gi...@appspot.gserviceaccount.com (2023-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7299b22d624a5325955149cd48f07d82bf2a0039

commit 7299b22d624a5325955149cd48f07d82bf2a0039
Author: Sohom <dattasohom1@gmail.com>
Date: Fri Jan 20 15:20:52 2023

Report ResourceTiming entries for 204/205 status codes even when not
navigating

Bug: 1346924
Change-Id: I368885b3dfaa5647795f08213d410861114c1dfa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3976688
Reviewed-by: Emily Stark <estark@chromium.org>
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Commit-Queue: Sohom Datta <dattasohom1@gmail.com>
Cr-Commit-Position: refs/heads/main@{#1095047}

[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/browser/BUILD.gn
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/renderer/core/frame/local_frame_mojo_handler.h
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/public/common/content_features.h
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/public/common/BUILD.gn
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/public/mojom/frame/frame.mojom
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/web_tests/TestExpectations
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/public/test/fake_local_frame.cc
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/public/test/fake_local_frame.h
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/browser/renderer_host/navigation_request.h
[add] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/browser/loader/resource_timing_utils.cc
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/public/common/content_features.cc
[delete] https://crrev.com/d2da1ebba819a75ab04e1f46b6fe2b992c850725/third_party/blink/web_tests/external/wpt/resource-timing/iframe-failed-commit-expected.txt
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/renderer/core/frame/local_frame_mojo_handler.cc
[add] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/browser/loader/resource_timing_utils.h
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/browser/loader/object_navigation_fallback_body_loader.cc
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/renderer/core/frame/local_frame.h
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/public/mojom/BUILD.gn
[add] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/public/common/frame/frame_owner_element_type_mojom_traits.h
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/common/BUILD.gn
[modify] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/renderer/core/frame/local_frame.cc
[add] https://crrev.com/7299b22d624a5325955149cd48f07d82bf2a0039/third_party/blink/common/frame/frame_owner_element_type_mojom_traits.cc


### da...@gmail.com (2023-01-20)

Issue should be fixed in the latest commit :)

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-27)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. A member of our finance team will reach out to you soon to arrange payment. Please let us know what name/tag/handle/other identifier you would like us to use in acknowledging you for this issue. Thank you for your efforts on this -- great work!  

### da...@gmail.com (2023-01-27)

Thanks a lot. Wrt to tag/handle something along the lines of "Sohom Datta, Manipal Institute of Technology" should be fine :)

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-03)

Latest commit resolving this issue landed on M111, so this is not considered as fix shipping in M110 as the automation is conjecturing. This fix will ship in milestone release in M111. 

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-04-28)

This issue was migrated from crbug.com/chromium/1346924?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060392)*
