# Security: Cross-Origin information leak in GetDeveloperIdsTask

| Field | Value |
|-------|-------|
| **Issue ID** | [40057025](https://issues.chromium.org/issues/40057025) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>BackgroundFetch |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2021-08-26 |
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

There is a mojo interface in BackgroundFetchService::GetDeveloperIds. The main code of  

this interface is in file |get\_developer\_ids\_task.cc|. But there is NO origin check after it got the information from database and return to renderer process:

"""  

void GetDeveloperIdsTask::Start() {  

service\_worker\_context()->GetRegistrationUserKeysAndDataByKeyPrefix(  

service\_worker\_registration\_id\_, {kActiveRegistrationUniqueIdKeyPrefix},  

base::BindOnce(&GetDeveloperIdsTask::DidGetUniqueIds,  

weak\_factory\_.GetWeakPtr()));  

}

void GetDeveloperIdsTask::DidGetUniqueIds(  

blink::ServiceWorkerStatusCode status,  

const base::flat\_map<std::string, std::string>& data\_map) {  

switch (ToDatabaseStatus(status)) {  

case DatabaseStatus::kNotFound:  

FinishWithError(blink::mojom::BackgroundFetchError::NONE);  

break;  

case DatabaseStatus::kOk: {  

developer\_ids\_.reserve(data\_map.size());  

for (const auto& pair : data\_map)  

developer\_ids\_.push\_back(pair.first);  

FinishWithError(blink::mojom::BackgroundFetchError::NONE);  

break;  

}  

case DatabaseStatus::kFailed:  

SetStorageErrorAndFinish(  

BackgroundFetchStorageError::kServiceWorkerStorageError);  

break;  

}  

}  

"""

The other similar interface GetRegistration has orgin check:  

"""  

void GetMetadataTask::ProcessMetadata(const std::string& metadata) {  

metadata\_proto\_ = std::make\_unique[proto::BackgroundFetchMetadata](javascript:void(0);)();  

if (!metadata\_proto\_->ParseFromString(metadata)) {  

FinishWithError(blink::mojom::BackgroundFetchError::STORAGE\_ERROR);  

return;  

}

const auto& registration\_proto = metadata\_proto\_->registration();  

// TODO(<https://crbug.com/1199077>): Check that the storage key matches once we  

// can get it from `metadata_proto_`.  

if (registration\_proto.developer\_id() != developer\_id\_ ||  

!storage\_key\_.origin().IsSameOriginWith(  

url::Origin::Create(GURL(metadata\_proto\_->origin())))) {  

FinishWithError(blink::mojom::BackgroundFetchError::STORAGE\_ERROR);  

return;  

}

FinishWithError(blink::mojom::BackgroundFetchError::NONE);  

}  

"""

It seems like Fetch interface checked it too, but I am not sure.

From a compromised renderer process, the attacker can easy guest the |service\_worker\_registration\_id|(as it starts from 0) and enum it from 0 to 1000 etc...

After got the user's other origin developerIds, the attacker can know what websites have user visited which belongs to sensitive information. As browsing history is useful for pre attack probe and user identification etc...

how to reproduce:  

$python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/Debug/gen  

$out/Debug/chrome --enable-blink-features=MojoJS '<http://localhost:8000/victim.html>'  

$out/Debug/chrome --enable-blink-features=MojoJS '<http://localhost:8001/attacker.html>'

port 8000/victim.html is used for set a developerId in database.  

port 8001/attacker.html is used for stole the other origin developerIds.

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: SorryMybad(@S0rryMybad) of Kunlun Lab

## Attachments

- [PoC.zip](attachments/PoC.zip) (application/octet-stream, 1.9 KB)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 513 B)

## Timeline

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-26)

This seems to reproduce as claimed, though I'm not super familiar with the BackgroundFetchService. Assigning Medium severity since this is an information leak, and triaging to an owner for the code. peter@, nator@ - can you take a look?

I've attached copy_mojo_js_bindings.py, to help reproduce.

[Monorail components: Blink>BackgroundFetch]

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2021-08-30)

+Rayan, mind taking a look?

### ra...@chromium.org (2021-09-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d97b8b86be732448cbc57b47f6b46547c9866df3

commit d97b8b86be732448cbc57b47f6b46547c9866df3
Author: Rayan Kanso <rayankans@google.com>
Date: Wed Sep 01 18:12:45 2021

[BackgroundFetch] Check whether the SW ID is valid for GetIds().

Bug: 1243622
Change-Id: I93a40db0e71c7a087d279653e741800015232d7f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3135479
Reviewed-by: Richard Knoll <knollr@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Commit-Position: refs/heads/main@{#917314}

[modify] https://crrev.com/d97b8b86be732448cbc57b47f6b46547c9866df3/content/browser/background_fetch/background_fetch_service_unittest.cc
[modify] https://crrev.com/d97b8b86be732448cbc57b47f6b46547c9866df3/content/browser/background_fetch/storage/get_developer_ids_task.cc
[modify] https://crrev.com/d97b8b86be732448cbc57b47f6b46547c9866df3/content/browser/background_fetch/storage/get_developer_ids_task.h


### ra...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

Requesting merge to beta M94 because latest trunk commit (917314) appears to be after beta branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-04)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2021-09-06)

1. Does your merge fit within the Merge Decision Guidelines?
Yes

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/3135479

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
No

5. Why are these changes required in this milestone after branch?
Security issue

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
N/A

### sr...@google.com (2021-09-07)

Merge approved for M94 branch:4606 please merge before 3pm PST today so this can go out in tomorrow beta release

### go...@chromium.org (2021-09-07)

Please merge your change to M94 branch 4606 ASAP so we can take it in for tomorrow's beta release. Beta RC cut @ 2:00 PM PT today, 09/07. Thank you.

### gi...@appspot.gserviceaccount.com (2021-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f2fd53c6d70614bdf1f38d7ff22a0299535dfed3

commit f2fd53c6d70614bdf1f38d7ff22a0299535dfed3
Author: Rayan Kanso <rayankans@google.com>
Date: Tue Sep 07 19:35:02 2021

[BackgroundFetch] Check whether the SW ID is valid for GetIds().

(cherry picked from commit d97b8b86be732448cbc57b47f6b46547c9866df3)

Bug: 1243622
Change-Id: I93a40db0e71c7a087d279653e741800015232d7f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3135479
Reviewed-by: Richard Knoll <knollr@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917314}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3143705
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Commit-Queue: Richard Knoll <knollr@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#828}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/f2fd53c6d70614bdf1f38d7ff22a0299535dfed3/content/browser/background_fetch/background_fetch_service_unittest.cc
[modify] https://crrev.com/f2fd53c6d70614bdf1f38d7ff22a0299535dfed3/content/browser/background_fetch/storage/get_developer_ids_task.cc
[modify] https://crrev.com/f2fd53c6d70614bdf1f38d7ff22a0299535dfed3/content/browser/background_fetch/storage/get_developer_ids_task.h


### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-28)

[Empty comment from Monorail migration]

### gi...@google.com (2021-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/efd8e01ac1a6e8686cbf03f4f8e6d5a9a7160df6

commit efd8e01ac1a6e8686cbf03f4f8e6d5a9a7160df6
Author: Zakhar Voit <voit@google.com>
Date: Wed Sep 29 14:24:18 2021

[M90-LTS][BackgroundFetch] Check whether the SW ID is valid for GetIds().

M90-LTS merge conflicts solved by using origin instead of storage key
because the storage key migration happened after M90.

(cherry picked from commit d97b8b86be732448cbc57b47f6b46547c9866df3)

Bug: 1243622
Change-Id: I93a40db0e71c7a087d279653e741800015232d7f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3135479
Reviewed-by: Richard Knoll <knollr@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917314}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3190253
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1627}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/efd8e01ac1a6e8686cbf03f4f8e6d5a9a7160df6/content/browser/background_fetch/background_fetch_service_unittest.cc
[modify] https://crrev.com/efd8e01ac1a6e8686cbf03f4f8e6d5a9a7160df6/content/browser/background_fetch/storage/get_developer_ids_task.h
[modify] https://crrev.com/efd8e01ac1a6e8686cbf03f4f8e6d5a9a7160df6/content/browser/background_fetch/storage/get_developer_ids_task.cc


### so...@gmail.com (2021-10-06)

Hi, any update of bounty?

### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations, the VRP Panel has decided to award you $2,000 for this report. Thank you for your report! 

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1243622?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057025)*
