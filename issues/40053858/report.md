# Double free/UAF in RegionDataLoaderImpl::DeleteThis

| Field | Value |
|-------|-------|
| **Issue ID** | [40053858](https://issues.chromium.org/issues/40053858) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | ko...@google.com |
| **Created** | 2020-11-13 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36

Steps to reproduce the problem:
1. python copy_mojo_js_bindings.py path/to/ASAN/gen/
2. python -m SimpleHTTPServer 8605
3. ASAN/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/noexit http://127.0.0.1:8605/uaf.html
4. wait for a moment

What is the expected behavior?

What went wrong?
In file components/autofill/core/browser/geo/region_data_loader_impl.cc
 function OnRegionDataLoaded of class RegionDataLoaderImpl will be called when construct a  RegionDataLoaderImpl, it will set PostTask to call DeleteThis at line 64,
 which will delete this pointer.

 46 void RegionDataLoaderImpl::OnRegionDataLoaded(bool success,
 47                                               const std::string& country_code,
 48                                               int unused_rule_count) {
 49   timer_.Stop();
 50   if (!callback_.is_null()) {
 51     if (success) {
 52       std::string best_region_tree_language_tag;
 53       ::i18n::addressinput::RegionDataBuilder builder(&region_data_supplier_);
 54       callback_.Run(
 55           builder
 56               .Build(country_code, app_locale_, &best_region_tree_language_tag)
 57               .sub_regions());
 58     } else {
 59       callback_.Run(std::vector<const ::i18n::addressinput::RegionData*>());
 60     }
 61   }
 62   // The deletion must be asynchronous since the caller is not quite done with
 63   // the preload supplier.
 64   base::ThreadTaskRunnerHandle::Get()->PostTask(
 65       FROM_HERE, base::BindOnce(&RegionDataLoaderImpl::DeleteThis,
 66                                 base::Unretained(this)));
 67 }
 68 
 69 void RegionDataLoaderImpl::DeleteThis() {
 70   delete this;
 71 }

However, when construct many RegionDataLoaderImpl at a time, the same PostTask maybe called twice, and this will be freed twice. ==> double free.
ASAN log shows that this is an UAF, because the `this` pointer is used again before freed, I think:) 

Did this work before? N/A 

Chrome version: 86.0.4240.75  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)
- [uaf.html](attachments/uaf.html) (text/plain, 5.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 12.3 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2020-11-13)

[Empty comment from Monorail migration]

### me...@gmail.com (2020-11-16)

[Comment Deleted]

### dr...@chromium.org (2020-11-16)

Thanks for the report! A UAF in the browser process is usually critical severity, but since this seems to require a compromised renderer, marking High instead.

estade@ - can you take a look?

[Monorail components: UI>Browser>Autofill]

### es...@chromium.org (2020-11-16)

over to autofill owner

### [Deleted User] (2020-11-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2020-11-17)

Here is some analysis, hope it is helpful to you.

### ba...@chromium.org (2020-11-17)

Thanks for the report! We will take a look.

### [Deleted User] (2020-11-17)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6468cd76f009cfa86a55d214393dc0fbef31b7b5

commit 6468cd76f009cfa86a55d214393dc0fbef31b7b5
Author: Matthias Körber <koerber@google.com>
Date: Wed Nov 18 08:45:01 2020

[Autofill] Exchange bare pointer with weak pointer for callbacks.

Change-Id: I9b1467d5f34d9381c8f944009b8f7511063fa30e
Bug: 1150004, 1148749
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544706
Commit-Queue: Matthias Körber <koerber@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/master@{#828642}

[modify] https://crrev.com/6468cd76f009cfa86a55d214393dc0fbef31b7b5/components/autofill/core/browser/ui/region_combobox_model.cc
[modify] https://crrev.com/6468cd76f009cfa86a55d214393dc0fbef31b7b5/components/autofill/core/browser/ui/region_combobox_model.h


### me...@gmail.com (2020-11-18)

Hi, I test the poc with asan-linux-release-828648, it seems that the crash can still repo? 
Maybe the function `LoadRegionData` should also be modified in components/autofill/core/browser/geo/region_data_loader_impl.cc?

### ba...@chromium.org (2020-11-18)

This is not the full fix, which consists of two parts.

### me...@gmail.com (2020-11-18)

[Comment Deleted]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a0baadbb6d48171540c24be7c74608b57f4cdc3b

commit a0baadbb6d48171540c24be7c74608b57f4cdc3b
Author: Matthias Körber <koerber@google.com>
Date: Fri Nov 20 12:34:55 2020

[Autofill] Remove self-destruct on timeout for RegionDataLoaderImpl

The self-destruction timer is not necessary because the RegionDataLoader
is guaranteed to be destructed once the query to libaddressinput
terminates.

Change-Id: Iac364183aa9d456b91ddc4d5f6f29b4c0ffe816d
Bug: 1148749
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544945
Reviewed-by: Dominic Battré <battre@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Christoph Schwering <schwering@google.com>
Commit-Queue: Matthias Körber <koerber@google.com>
Cr-Commit-Position: refs/heads/master@{#829628}

[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/chrome/browser/ui/views/payments/shipping_address_editor_view_controller.cc
[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/components/autofill/core/browser/geo/region_data_loader.h
[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/components/autofill/core/browser/geo/region_data_loader_impl.cc
[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/components/autofill/core/browser/geo/region_data_loader_impl.h
[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/components/autofill/core/browser/geo/test_region_data_loader.cc
[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/components/autofill/core/browser/geo/test_region_data_loader.h
[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/components/autofill/core/browser/ui/region_combobox_model.cc
[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/components/autofill/core/browser/ui/region_combobox_model.h
[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/components/autofill/core/browser/ui/region_combobox_model_unittest.cc
[modify] https://crrev.com/a0baadbb6d48171540c24be7c74608b57f4cdc3b/third_party/libaddressinput/chromium/chrome_metadata_source.cc


### ko...@google.com (2020-11-20)

Now, with this second patch, the UAF should be hopefully fixed.

### ko...@google.com (2020-11-20)

Our interpretation of the origin of the double free is actually a bit different. We do not see the problem in having multiple instances of RegionDataLoaderImpl, but that there are two mechanisms that lead to a self-destruct of a given instance.

a) The timeout timer.
b) region_data_supplier_.LoadRules(country_code, *region_data_supplier_callback_) terminates and calls the callback.

If a) happens before b) we end up in a double free. If b) happens before a), the timer is canceled.

To mitigate, we removed the timer and added a timeout to the network request instantiated by LoadRules making sure the instance is destructed eventually.
We also added a weak pointer for the callback to the UI to mitigate, the the UI may have already been destructed.

### me...@gmail.com (2020-11-23)

You are right, I believe that the UAF has been fixed :)

### ko...@google.com (2020-11-23)

That is good news, thank you for testing.

### ko...@google.com (2020-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-23)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@google.com (2020-11-23)

1. 
Yes - it is a fix to a UAF bug.

2.
https://chromium-review.googlesource.com/c/chromium/src/+/2544945
https://chromium-review.googlesource.com/c/chromium/src/+/2544706

3.
Changes landed, reporter confirmed that the changes fix the issue.

4.
The cause for the UAF is not due to a recent change, but already exists for some time.
Merging to M87 will roll out the fix to most users. 
If rejected, the fixes should at least be merged to M88.

5.
The changes will fix a use after free bug that can be triggered by a delayed server response.

6.
No

7.
NA


### la...@google.com (2020-11-23)

I am going to reject this for M87 given the fact this is a pre-existing issue and we are only taking critical fixes for M87 which is in Stable now. Please raise an M88 merge request.

### ko...@google.com (2020-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-24)

Your change meets the bar and is auto-approved for M88. Please go ahead and merge the CL to branch 4324 (refs/branch-heads/4324) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2024e6801fd2323f3b65b44672dbf75d2f2b5f75

commit 2024e6801fd2323f3b65b44672dbf75d2f2b5f75
Author: Matthias Körber <koerber@google.com>
Date: Thu Nov 26 13:59:14 2020

[Autofill] Exchange bare pointer with weak pointer for callbacks.

(cherry picked from commit 6468cd76f009cfa86a55d214393dc0fbef31b7b5)

Change-Id: I9b1467d5f34d9381c8f944009b8f7511063fa30e
Bug: 1150004, 1148749
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544706
Commit-Queue: Matthias Körber <koerber@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#828642}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2562140
Reviewed-by: Matthias Körber <koerber@google.com>
Cr-Commit-Position: refs/branch-heads/4324@{#379}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/2024e6801fd2323f3b65b44672dbf75d2f2b5f75/components/autofill/core/browser/ui/region_combobox_model.cc
[modify] https://crrev.com/2024e6801fd2323f3b65b44672dbf75d2f2b5f75/components/autofill/core/browser/ui/region_combobox_model.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-11-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3cb8d76b7ae399600055082698c5a65dde6576fe

commit 3cb8d76b7ae399600055082698c5a65dde6576fe
Author: Matthias Körber <koerber@google.com>
Date: Thu Nov 26 15:13:14 2020

[Autofill] Remove self-destruct on timeout for RegionDataLoaderImpl

The self-destruction timer is not necessary because the RegionDataLoader
is guaranteed to be destructed once the query to libaddressinput
terminates.

(cherry picked from commit a0baadbb6d48171540c24be7c74608b57f4cdc3b)

Change-Id: Iac364183aa9d456b91ddc4d5f6f29b4c0ffe816d
Bug: 1148749
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544945
Reviewed-by: Dominic Battré <battre@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Christoph Schwering <schwering@google.com>
Commit-Queue: Matthias Körber <koerber@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#829628}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2562142
Reviewed-by: Matthias Körber <koerber@google.com>
Cr-Commit-Position: refs/branch-heads/4324@{#380}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/chrome/browser/ui/views/payments/shipping_address_editor_view_controller.cc
[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/components/autofill/core/browser/geo/region_data_loader.h
[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/components/autofill/core/browser/geo/region_data_loader_impl.cc
[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/components/autofill/core/browser/geo/region_data_loader_impl.h
[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/components/autofill/core/browser/geo/test_region_data_loader.cc
[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/components/autofill/core/browser/geo/test_region_data_loader.h
[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/components/autofill/core/browser/ui/region_combobox_model.cc
[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/components/autofill/core/browser/ui/region_combobox_model.h
[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/components/autofill/core/browser/ui/region_combobox_model_unittest.cc
[modify] https://crrev.com/3cb8d76b7ae399600055082698c5a65dde6576fe/third_party/libaddressinput/chromium/chrome_metadata_source.cc


### me...@gmail.com (2020-12-04)

[Comment Deleted]

### ba...@chromium.org (2020-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-08)

koerber: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@chromium.org (2020-12-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-12)

[Empty comment from Monorail migration]

### ad...@google.com (2020-12-14)

I'm adding M87 merge request because this is a security bug, and I assume lakpamarthy@ didn't spot that when he added https://crbug.com/chromium/1148749#c22. I will discuss with lakpamarthy@ next time I do a round of M87 merge approvals.

Re https://crbug.com/chromium/1148749#c27, this will be considered by the panel, and it will be likely allocated a CVE when we release the fix. Thanks for the report.

### ad...@google.com (2020-12-15)

Approving merge to M87, branch 4280. This has been in canary for 20+ days and is a sandbox escape, so is at the upper end of high severity.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/de8d766436ddcf5dc69690ab8100e736ff0e1f9d

commit de8d766436ddcf5dc69690ab8100e736ff0e1f9d
Author: Matthias Körber <koerber@google.com>
Date: Tue Dec 15 22:17:16 2020

[Autofill] Exchange bare pointer with weak pointer for callbacks.

(cherry picked from commit 6468cd76f009cfa86a55d214393dc0fbef31b7b5)

Change-Id: I9b1467d5f34d9381c8f944009b8f7511063fa30e
Bug: 1150004, 1148749
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544706
Commit-Queue: Matthias Körber <koerber@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#828642}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2592799
Reviewed-by: Matthias Körber <koerber@google.com>
Cr-Commit-Position: refs/branch-heads/4280@{#1885}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/de8d766436ddcf5dc69690ab8100e736ff0e1f9d/components/autofill/core/browser/ui/region_combobox_model.h
[modify] https://crrev.com/de8d766436ddcf5dc69690ab8100e736ff0e1f9d/components/autofill/core/browser/ui/region_combobox_model.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-12-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/75ab68d1276fbdc5805e0194fc9e628a8e796f03

commit 75ab68d1276fbdc5805e0194fc9e628a8e796f03
Author: Matthias Körber <koerber@google.com>
Date: Wed Dec 16 00:33:27 2020

[Autofill] Remove self-destruct on timeout for RegionDataLoaderImpl

The self-destruction timer is not necessary because the RegionDataLoader
is guaranteed to be destructed once the query to libaddressinput
terminates.

(cherry picked from commit a0baadbb6d48171540c24be7c74608b57f4cdc3b)

Change-Id: Iac364183aa9d456b91ddc4d5f6f29b4c0ffe816d
Bug: 1148749
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544945
Reviewed-by: Dominic Battré <battre@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Christoph Schwering <schwering@google.com>
Commit-Queue: Matthias Körber <koerber@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#829628}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2593004
Reviewed-by: Matthias Körber <koerber@google.com>
Cr-Commit-Position: refs/branch-heads/4280@{#1887}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/components/autofill/core/browser/geo/test_region_data_loader.h
[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/components/autofill/core/browser/ui/region_combobox_model.cc
[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/components/autofill/core/browser/geo/region_data_loader_impl.cc
[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/components/autofill/core/browser/geo/region_data_loader_impl.h
[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/components/autofill/core/browser/ui/region_combobox_model_unittest.cc
[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/third_party/libaddressinput/chromium/chrome_metadata_source.cc
[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/components/autofill/core/browser/geo/test_region_data_loader.cc
[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/components/autofill/core/browser/ui/region_combobox_model.h
[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/chrome/browser/ui/views/payments/shipping_address_editor_view_controller.cc
[modify] https://crrev.com/75ab68d1276fbdc5805e0194fc9e628a8e796f03/components/autofill/core/browser/geo/region_data_loader.h


### ko...@google.com (2020-12-16)

Thanks Adrian, the merge is done. 

### ad...@google.com (2020-12-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-12-17)

Congratulations! The VRP panel has decided to award $20,000 for this bug.

### ad...@google.com (2020-12-17)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-05)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-06)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### ke...@google.com (2021-01-08)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2323a55fb313de52fe85a05f5e2aa6a4e7251e25

commit 2323a55fb313de52fe85a05f5e2aa6a4e7251e25
Author: Matthias Körber <koerber@google.com>
Date: Sat Jan 09 20:50:54 2021

[Autofill] Exchange bare pointer with weak pointer for callbacks.

(cherry picked from commit 6468cd76f009cfa86a55d214393dc0fbef31b7b5)

(cherry picked from commit de8d766436ddcf5dc69690ab8100e736ff0e1f9d)

Change-Id: I9b1467d5f34d9381c8f944009b8f7511063fa30e
Bug: 1150004, 1148749
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544706
Commit-Queue: Matthias Körber <koerber@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Original-Original-Commit-Position: refs/heads/master@{#828642}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2592799
Reviewed-by: Matthias Körber <koerber@google.com>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#1885}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617104
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1509}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/2323a55fb313de52fe85a05f5e2aa6a4e7251e25/components/autofill/core/browser/ui/region_combobox_model.h
[modify] https://crrev.com/2323a55fb313de52fe85a05f5e2aa6a4e7251e25/components/autofill/core/browser/ui/region_combobox_model.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/82c477be5e8e9bbfe70849437a20cfc76022894e

commit 82c477be5e8e9bbfe70849437a20cfc76022894e
Author: Matthias Körber <koerber@google.com>
Date: Mon Jan 11 17:40:41 2021

[Autofill] Remove self-destruct on timeout for RegionDataLoaderImpl

The self-destruction timer is not necessary because the RegionDataLoader
is guaranteed to be destructed once the query to libaddressinput
terminates.

(cherry picked from commit a0baadbb6d48171540c24be7c74608b57f4cdc3b)

(cherry picked from commit 75ab68d1276fbdc5805e0194fc9e628a8e796f03)

Change-Id: Iac364183aa9d456b91ddc4d5f6f29b4c0ffe816d
Bug: 1148749
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2544945
Reviewed-by: Dominic Battré <battre@chromium.org>
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Christoph Schwering <schwering@google.com>
Commit-Queue: Matthias Körber <koerber@google.com>
Cr-Original-Original-Commit-Position: refs/heads/master@{#829628}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2593004
Reviewed-by: Matthias Körber <koerber@google.com>
Cr-Original-Commit-Position: refs/branch-heads/4280@{#1887}
Cr-Original-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2617102
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1512}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/components/autofill/core/browser/geo/test_region_data_loader.h
[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/components/autofill/core/browser/ui/region_combobox_model.cc
[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/components/autofill/core/browser/geo/region_data_loader_impl.cc
[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/components/autofill/core/browser/geo/region_data_loader_impl.h
[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/components/autofill/core/browser/ui/region_combobox_model_unittest.cc
[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/third_party/libaddressinput/chromium/chrome_metadata_source.cc
[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/components/autofill/core/browser/geo/test_region_data_loader.cc
[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/components/autofill/core/browser/ui/region_combobox_model.h
[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/chrome/browser/ui/views/payments/shipping_address_editor_view_controller.cc
[modify] https://crrev.com/82c477be5e8e9bbfe70849437a20cfc76022894e/components/autofill/core/browser/geo/region_data_loader.h


### [Deleted User] (2021-01-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-03-29)

Hi, @merc.ouc - we consider attachments/pocs included with reports to be an integral part of the report, so I've un-deleted them. Thanks!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1148749?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053858)*
