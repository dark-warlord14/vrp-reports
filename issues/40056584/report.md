# Security: heap-use-after-free in WebDataRequestManager::RequestCompletedOnThread

| Field | Value |
|-------|-------|
| **Issue ID** | [40056584](https://issues.chromium.org/issues/40056584) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | yu...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2021-07-19 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

The AutocompleteHistoryManager class extends WebDataServiceConsumer.  

<https://source.chromium.org/chromium/chromium/src/+/main:components/autofill/core/browser/autocomplete_history_manager.h;l=30>

And the instance is holded as a raw pointer in WebDataRequest.  

<https://source.chromium.org/chromium/chromium/src/+/main:components/webdata/common/web_data_request_manager.h;l=80>

When close chrome, the keyed\_service component will destroy all keyed services, include a AutocompleteHistoryManager instance.  

<https://source.chromium.org/chromium/chromium/src/+/main:components/keyed_service/core/dependency_manager.cc;l=148>

If a request completed after the AutocompleteHistoryManager instance destroied, uaf triggered in WebDataRequestManager::RequestCompletedOnThread.  

<https://source.chromium.org/chromium/chromium/src/+/main:components/webdata/common/web_data_request_manager.cc;l=139>

**VERSION**  

Chrome Version: asan-linux-release-900758,93.0.4574.0,dev  

Operating System: Linux

**REPRODUCTION CASE**  

Asan log attached. I am still investigating this issue, and will submit POC files soon.

**CREDIT INFORMATION**  

Reporter credit: Wei Yuan of MoyunSec VLab

## Attachments

- [uaf_asan.txt](attachments/uaf_asan.txt) (text/plain, 22.0 KB)
- [patch.txt](attachments/patch.txt) (text/plain, 2.7 KB)
- [record.mov](attachments/record.mov) (video/quicktime, 23.7 MB)

## Timeline

### [Deleted User] (2021-07-19)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-07-19)

Thanks for your report. Chrome uses quite a few raw pointers, so a PoC would certainly help us assess the viability of this issue.

### yu...@gmail.com (2021-07-20)

Yes, maybe a request completed after all keyed services destroied is the root cause. It is a classical muti-thread problem.
I found this crash in my fuzz system without any patch and manual operators, so this bug can be triggered in official build version and the patch file is just for PoC and stable reproduce. 

Reproduce steps:
1. apply patch file and rebuild chrome
2. delete userdata directory to bypass the "if (CHROME_VERSION_MAJOR > last_cleaned_version)" check. (like chrome first startup)
3. open chrome,  click close button.

After investigate the source code, maybe this problem exists long time. Following is my simple analysis, FYI.

1、When chrome start, the AutocompleteHistoryManager::Init called and instance registered in keyed services. RemoveExpiredAutocompleteEntries call in this method will post a task witch will be executed in ThreadPoolSingleThreadSharedForegroundBlocking thread.  Additionally,  chrome main window was created here and can receive a CLOSE message.
https://source.chromium.org/chromium/chromium/src/+/main:components/autofill/core/browser/autocomplete_history_manager.cc;l=153
```
    if (CHROME_VERSION_MAJOR > last_cleaned_version) {
      // Trigger the cleanup.
      profile_database_->RemoveExpiredAutocompleteEntries(this);
    }
```
https://source.chromium.org/chromium/chromium/src/+/main:components/webdata/common/web_database_service.cc;l=104;drc=34da4407648871eca12e13e607545c0a64a83c1c
```
  std::unique_ptr<WebDataRequest> request =
      web_db_backend_->request_manager()->NewRequest(consumer);      //   consumer is a AutocompleteHistoryManager instance
  WebDataServiceBase::Handle handle = request->GetHandle();
  db_task_runner_->PostTask(
      from_here,
      BindOnce(&WebDatabaseBackend::DBReadTaskWrapper, web_db_backend_,
               std::move(task), std::move(request)));
```

2、When close chrome, ScopedProfileKeepAlive::RemoveKeepAliveOnUIThread will be called destroy all keyed_services. If the task in step 1 completed in ThreadPoolSingleThreadSharedForegroundBlocking and post a RequestCompleted task to main thread exactly, the RequestCompleted task will be executed before break task loop.
https://source.chromium.org/chromium/chromium/src/+/main:components/webdata/common/web_data_request_manager.cc;l=111

3、UaF triggered in WebDataRequestManager::RequestCompletedOnThread when it called in main thread.
https://source.chromium.org/chromium/chromium/src/+/main:components/webdata/common/web_data_request_manager.cc;l=139

### [Deleted User] (2021-07-20)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### do...@chromium.org (2021-07-21)

+battre +schwering, can you please follow up on this? I'm setting a Low severity as this would only trigger on shutdown and it's likely existed since at least https://chromium-review.googlesource.com/c/chromium/src/+/1351434 in 2018 which made this object a KeyedService.

[Monorail components: UI>Browser>Autofill]

### do...@chromium.org (2021-07-21)

(This bug is a lot older than M91 but I think I'm meant to set the latest stable as the oldest milestone for FoundIn)

### [Deleted User] (2021-07-21)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2021-07-21)

ACK. Will look into this. Thanks for the report.

### ba...@chromium.org (2021-07-22)

CL is out for review here: https://chromium-review.googlesource.com/c/chromium/src/+/3043648/

### gi...@appspot.gserviceaccount.com (2021-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f15e0e905b169e2f6a09443db0888f418159572f

commit f15e0e905b169e2f6a09443db0888f418159572f
Author: Dominic Battre <battre@chromium.org>
Date: Thu Jul 22 17:05:46 2021

Make WebDataServiceConsumer support WeakPtrs

The WebDataServiceBase is ref counted (with destruction on a specific
sequence). As the WebDataService owns a refcounted WebDataService, the
destruction is a bit unpredictable.

This CL adds a WeakPtrFactory to WebDataServiceConsumer so that we don't
have to guarantee that WebDataServiceConsumers need to outlive the
WebDataService.

Bug: 1230513
Change-Id: I91a27d7d4ecca4ee9685aabae306437b6fe0cc54
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3043648
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Olivier Robin <olivierrobin@chromium.org>
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Commit-Position: refs/heads/master@{#904371}

[modify] https://crrev.com/f15e0e905b169e2f6a09443db0888f418159572f/components/webdata/common/BUILD.gn
[modify] https://crrev.com/f15e0e905b169e2f6a09443db0888f418159572f/components/webdata/common/web_data_request_manager.cc
[modify] https://crrev.com/f15e0e905b169e2f6a09443db0888f418159572f/components/webdata/common/web_data_request_manager.h
[add] https://crrev.com/f15e0e905b169e2f6a09443db0888f418159572f/components/webdata/common/web_data_service_consumer.cc
[modify] https://crrev.com/f15e0e905b169e2f6a09443db0888f418159572f/components/webdata/common/web_data_service_consumer.h
[modify] https://crrev.com/f15e0e905b169e2f6a09443db0888f418159572f/components/webdata/common/web_database_service.h
[modify] https://crrev.com/f15e0e905b169e2f6a09443db0888f418159572f/ios/chrome/browser/autofill/autofill_controller_unittest.mm


### ba...@chromium.org (2021-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-23)

[Empty comment from Monorail migration]

### ba...@chromium.org (2021-07-27)

[Empty comment from Monorail migration]

### ba...@chromium.org (2021-08-02)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-02)

This bug requires manual review: M93's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2021-08-02)

1. I am not sure whether this problem happens anywhere in the wild but it is possible. As it has been on Dev/Canary for some time now, I feel that we can mergen.

2. https://chromium-review.googlesource.com/c/chromium/src/+/3043648

3. Yes

4. Unless the security folks ask, I would limit this to M93 for now.

5. Possible security vulnerability.

6. No

### am...@chromium.org (2021-08-02)

Hi battre@, you don't need to manually request merge for security bugs now; once you update a security bug status to Fixed, we (with the 'bot) will take care of the rest. I'll go ahead and approve this to merge to M93. Please merge this to branch 4577 before 2pm PDT tomorrow (Tuesday, 3 August) so it can be a part of this week's beta release. Thank you!

### sr...@google.com (2021-08-03)

Please complete your merges to M93 today asap. I am cutting beta RC today at 3pm PST, so please help complete merges so we can include in this weeks beta release

### gi...@appspot.gserviceaccount.com (2021-08-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/df1ed39e67a804a5fabb1477b32e619fa4eef886

commit df1ed39e67a804a5fabb1477b32e619fa4eef886
Author: Dominic Battre <battre@chromium.org>
Date: Wed Aug 04 21:24:40 2021

[M93] Make WebDataServiceConsumer support WeakPtrs

The WebDataServiceBase is ref counted (with destruction on a specific
sequence). As the WebDataService owns a refcounted WebDataService, the
destruction is a bit unpredictable.

This CL adds a WeakPtrFactory to WebDataServiceConsumer so that we don't
have to guarantee that WebDataServiceConsumers need to outlive the
WebDataService.

(cherry picked from commit f15e0e905b169e2f6a09443db0888f418159572f)

Bug: 1230513
Change-Id: I91a27d7d4ecca4ee9685aabae306437b6fe0cc54
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3043648
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Reviewed-by: Olivier Robin <olivierrobin@chromium.org>
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#904371}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3067346
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Dominic Battré <battre@chromium.org>
Commit-Queue: Olivier Robin <olivierrobin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#450}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/df1ed39e67a804a5fabb1477b32e619fa4eef886/components/webdata/common/BUILD.gn
[modify] https://crrev.com/df1ed39e67a804a5fabb1477b32e619fa4eef886/components/webdata/common/web_data_request_manager.cc
[modify] https://crrev.com/df1ed39e67a804a5fabb1477b32e619fa4eef886/components/webdata/common/web_data_request_manager.h
[add] https://crrev.com/df1ed39e67a804a5fabb1477b32e619fa4eef886/components/webdata/common/web_data_service_consumer.cc
[modify] https://crrev.com/df1ed39e67a804a5fabb1477b32e619fa4eef886/components/webdata/common/web_data_service_consumer.h
[modify] https://crrev.com/df1ed39e67a804a5fabb1477b32e619fa4eef886/components/webdata/common/web_database_service.h
[modify] https://crrev.com/df1ed39e67a804a5fabb1477b32e619fa4eef886/ios/chrome/browser/autofill/autofill_controller_unittest.mm


### am...@chromium.org (2021-08-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-28)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. Thank you for your report as well as your patience while we resolved and rewarded this issue. 



### am...@chromium.org (2021-09-28)

for posterity sake/security sheriff templating, updating security severity from Low to Medium. Even though this issue is seemingly difficult to trigger and requires profile destruction, it does result in a UAF in the browser process. 

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### vo...@google.com (2021-10-04)

[Empty comment from Monorail migration]

### gi...@google.com (2021-10-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/903cf32bda772f3e11334814d8ca0096822dfcfc

commit 903cf32bda772f3e11334814d8ca0096822dfcfc
Author: Zakhar Voit <voit@google.com>
Date: Thu Oct 07 11:14:31 2021

[M90-LTS] Make WebDataServiceConsumer support WeakPtrs

M90 merge conflicts: used UTF-16 string instead of UTF-8 because the
code hasn't yet transitioned to UTF-8 in M90.

The WebDataServiceBase is ref counted (with destruction on a specific
sequence). As the WebDataService owns a refcounted WebDataService, the
destruction is a bit unpredictable.

This CL adds a WeakPtrFactory to WebDataServiceConsumer so that we don't
have to guarantee that WebDataServiceConsumers need to outlive the
WebDataService.

(cherry picked from commit f15e0e905b169e2f6a09443db0888f418159572f)

Bug: 1230513
Change-Id: I91a27d7d4ecca4ee9685aabae306437b6fe0cc54
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3043648
Commit-Queue: Dominic Battré <battre@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#904371}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3201971
Reviewed-by: Jana Grill <janagrill@google.com>
Reviewed-by: Dominic Battré <battre@chromium.org>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1639}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[add] https://crrev.com/903cf32bda772f3e11334814d8ca0096822dfcfc/components/webdata/common/web_data_service_consumer.cc
[modify] https://crrev.com/903cf32bda772f3e11334814d8ca0096822dfcfc/components/webdata/common/web_data_request_manager.cc
[modify] https://crrev.com/903cf32bda772f3e11334814d8ca0096822dfcfc/ios/chrome/browser/autofill/autofill_controller_unittest.mm
[modify] https://crrev.com/903cf32bda772f3e11334814d8ca0096822dfcfc/components/webdata/common/web_database_service.h
[modify] https://crrev.com/903cf32bda772f3e11334814d8ca0096822dfcfc/components/webdata/common/web_data_service_consumer.h
[modify] https://crrev.com/903cf32bda772f3e11334814d8ca0096822dfcfc/components/webdata/common/web_data_request_manager.h
[modify] https://crrev.com/903cf32bda772f3e11334814d8ca0096822dfcfc/components/webdata/common/BUILD.gn


### vo...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1230513?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056584)*
