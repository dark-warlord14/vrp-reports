# Security: UAF in DumpDatabaseHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [40059248](https://issues.chromium.org/issues/40059248) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2022-03-30 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**

Message `getDatabaseDump`[1] will bind the task `DidGetDatabaseDump`[2] with `base::Unretained(this)` as a callback into the SyncFileSystemService. And if the `sync_worker` is turned on, the task will be posted into a new sequence[3]. It will cause the UAF if `DumpDatabaseHandler` gets destroyed before the task run.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/sync_file_system_internals/dump_database.js;l=17;drc=04131fcab06ff84254133e7f7f38dd6c48cb0c13;bpv=0;bpt=0>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/sync_file_system_internals/dump_database_handler.cc;l=35;drc=354945de1fb564ef04c07cf8bfedf434d2d81747>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/sync_file_system/drive_backend/sync_engine.cc;l=565;bpv=1;bpt=0;drc=646a03e971cc83d5e9751aefa67abd39fe842f67>

Fix suggestion:

Use `weak_ptr_factory_.GetWeakPtr()` or `CancelableTask`.

**VERSION**  

Chrome Version: stable  

Operating System: test in linux & win & chromeos

**REPRODUCTION CASE**

1. Make sure the browser has an account that has turned on sync.  
   
   Or apply this patch to turn on the SyncEngine.

diff --git a/chrome/browser/sync\_file\_system/drive\_backend/sync\_engine.cc b/chrome/browser/sync\_file\_system/drive\_backend/sync\_engine.cc  

index b7b315093f257..584bafc84fad1 100644  

--- a/chrome/browser/sync\_file\_system/drive\_backend/sync\_engine.cc  

+++ b/chrome/browser/sync\_file\_system/drive\_backend/sync\_engine.cc  

@@ -259,8 +259,7 @@ void SyncEngine::Initialize() {  

DCHECK\_CURRENTLY\_ON(content::BrowserThread::UI);  

Reset();

- if (!identity\_manager\_ ||
- ```
   !identity_manager_->HasPrimaryAccount(signin::ConsentLevel::kSync)) {  
  
  ```

- if (!identity\_manager\_ ) {  
  
  return;  
  
  }

2. Load the attached extension to trigger this uaf:

out/asan/chrome --user-data-dir=/tmp/xxxx --load-extension="/path/to/extension"

Or you can:

browsing `chrome://syncfs-internals` and open devtools  

execute ```  

var w = window.open("chrome://syncfs-internals/");  

setTimeout(()=>{  

with (w) {  

async function cb() {  

}  

cr.webUIResponse = cb;  

for (let index = 0; index < 0x2000; index++) {  

chrome.send("getDatabaseDump",[""]);  

chrome.send("getDatabaseDump",[""]);  

window.close();  

}  

}  

},1000);

```
  
  
**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**   
Type of crash: browser  
Crash State: see asan file  
  
  
**CREDIT INFORMATION**   
Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute  

```

## Attachments

- [asan](attachments/asan) (text/plain, 46.6 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 210 B)
- [background.js](attachments/background.js) (text/plain, 534 B)

## Timeline

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-03-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5086324381777920.

### le...@gmail.com (2022-03-31)

It is a browser crash, ClusterFuzz with v8 doesn't seem reasonable.

### hc...@google.com (2022-03-31)

Yeah good point.

I was able to repro though i haven't gotten around to looking at foundin correctly. Its at least in 99.

@pwnall can you take a look?



[Monorail components: Blink>Storage>FileSystem]

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-03-31)

Per discussions, marking this as critical because it's a browser process UaF and only requires an extension to be installed (with minimal permissions).

The line with base::Unretained() dates back to at least https://source.chromium.org/chromium/chromium/src/+/db3408a9ef16b977be7ab0f5c30a09a57348d62a, and so this is unsafe in extended and beyond.

### dc...@chromium.org (2022-03-31)

I don't /think/ this WebUI page is used on Android, but I don't have a device handy to confirm. Can someone check?

### le...@gmail.com (2022-03-31)

[Comment Deleted]

### le...@gmail.com (2022-03-31)

yes, this webUI page is not used on Android.

### [Deleted User] (2022-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hc...@google.com (2022-04-01)

[Empty comment from Monorail migration]

### me...@chromium.org (2022-04-01)

asully: can you take a look?

### [Deleted User] (2022-04-01)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-04-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6405ab0150f1a98ea7a712cf79047770d54bd854

commit 6405ab0150f1a98ea7a712cf79047770d54bd854
Author: Austin Sullivan <asully@chromium.org>
Date: Mon Apr 04 23:40:56 2022

syncfs_internals: Use WeakPtr for DumpDatabaseHandler

Bug: 1311701
Change-Id: I97044b3622cb78d8d0950ee52ada168c401700b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3570389
Auto-Submit: Austin Sullivan <asully@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#988749}

[modify] https://crrev.com/6405ab0150f1a98ea7a712cf79047770d54bd854/chrome/browser/ui/webui/sync_file_system_internals/dump_database_handler.h
[modify] https://crrev.com/6405ab0150f1a98ea7a712cf79047770d54bd854/chrome/browser/ui/webui/sync_file_system_internals/dump_database_handler.cc


### as...@chromium.org (2022-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-05)

Requesting merge to stable M100 because latest trunk commit (988749) appears to be after stable branch point (972766).

Requesting merge to beta M101 because latest trunk commit (988749) appears to be after beta branch point (982481).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-04-05)

This requires an extension to be installed which mitigates this down from Critical to High. We should accommodate this in the next convenient release vehicle, but this does not require us to inconvenience and cost all Chrome users by issuing an extra Chrome build.

### [Deleted User] (2022-04-05)

Merge review required: M101 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-05)

Merge review required: M100 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-04-06)

1. Why does your merge fit within the merge criteria for these milestones?

High severity security fix

2. What changes specifically would you like to merge? Please link to Gerrit.

M101: https://crrev.com/c/3573889
M100: https://crrev.com/c/3573890

3. Have the changes been released and tested on canary?

Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Yes. See repro case in the initial bug report. The fix works if the browser does not crash

### am...@chromium.org (2022-04-07)

M101 merge approved, please merge to branch 4951 at your earliest convenience 

M100 merge approved, please merge to branch 4896 ASAP so this fix can be included in tomorrow's security refresh for M100 

### gi...@appspot.gserviceaccount.com (2022-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b8d56fab5dde25c988f0ae7acdac37b1fbd26a91

commit b8d56fab5dde25c988f0ae7acdac37b1fbd26a91
Author: Austin Sullivan <asully@chromium.org>
Date: Thu Apr 07 18:07:37 2022

M100: syncfs_internals: Use WeakPtr for DumpDatabaseHandler

(cherry picked from commit 6405ab0150f1a98ea7a712cf79047770d54bd854)

Bug: 1311701
Change-Id: I97044b3622cb78d8d0950ee52ada168c401700b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3570389
Auto-Submit: Austin Sullivan <asully@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#988749}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3573890
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/4896@{#1074}
Cr-Branched-From: 1f63ff4bc27570761b35ffbc7f938f6586f7bee8-refs/heads/main@{#972766}

[modify] https://crrev.com/b8d56fab5dde25c988f0ae7acdac37b1fbd26a91/chrome/browser/ui/webui/sync_file_system_internals/dump_database_handler.h
[modify] https://crrev.com/b8d56fab5dde25c988f0ae7acdac37b1fbd26a91/chrome/browser/ui/webui/sync_file_system_internals/dump_database_handler.cc


### [Deleted User] (2022-04-07)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-04-07)

1. Was this issue a regression for the milestone it was found in?

No

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No

### gi...@appspot.gserviceaccount.com (2022-04-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0221dbed0ca96e011d38b117a04aeac320578f27

commit 0221dbed0ca96e011d38b117a04aeac320578f27
Author: Austin Sullivan <asully@chromium.org>
Date: Thu Apr 07 18:35:05 2022

M101: syncfs_internals: Use WeakPtr for DumpDatabaseHandler

(cherry picked from commit 6405ab0150f1a98ea7a712cf79047770d54bd854)

Bug: 1311701
Change-Id: I97044b3622cb78d8d0950ee52ada168c401700b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3570389
Auto-Submit: Austin Sullivan <asully@chromium.org>
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#988749}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3573889
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/branch-heads/4951@{#551}
Cr-Branched-From: 27de6227ca357da0d57ae2c7b18da170c4651438-refs/heads/main@{#982481}

[modify] https://crrev.com/0221dbed0ca96e011d38b117a04aeac320578f27/chrome/browser/ui/webui/sync_file_system_internals/dump_database_handler.h
[modify] https://crrev.com/0221dbed0ca96e011d38b117a04aeac320578f27/chrome/browser/ui/webui/sync_file_system_internals/dump_database_handler.cc


### rz...@google.com (2022-04-11)

[Empty comment from Monorail migration]

### ad...@google.com (2022-04-11)

[Empty comment from Monorail migration]

### ad...@google.com (2022-04-11)

[Empty comment from Monorail migration]

### rz...@google.com (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-04-12)

1. Just https://crrev.com/c/3581702
2. Low, a few simple conflicts and the fix is a small change
3. 100, 101
4. Yes

### am...@google.com (2022-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-13)

Congratulations, leecraso and Guang Gong! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and great work! 

### am...@google.com (2022-04-16)

[Empty comment from Monorail migration]

### gm...@google.com (2022-04-19)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/794764e9dac65771375b3c3fc1bb73cc4f3a9efe

commit 794764e9dac65771375b3c3fc1bb73cc4f3a9efe
Author: Austin Sullivan <asully@chromium.org>
Date: Tue Apr 19 17:21:58 2022

[M96-LTS] syncfs_internals: Use WeakPtr for DumpDatabaseHandler

M96 merge issues:
  dump_database_handler.h:
  - include conflicts
  - conflicting types for profile_
  dump_database_handler.cc:
  - conflicts on call for getting the callback_id

(cherry picked from commit 6405ab0150f1a98ea7a712cf79047770d54bd854)

Bug: 1311701
Change-Id: I97044b3622cb78d8d0950ee52ada168c401700b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3570389
Auto-Submit: Austin Sullivan <asully@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#988749}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3581702
Reviewed-by: Austin Sullivan <asully@chromium.org>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1596}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/794764e9dac65771375b3c3fc1bb73cc4f3a9efe/chrome/browser/ui/webui/sync_file_system_internals/dump_database_handler.h
[modify] https://crrev.com/794764e9dac65771375b3c3fc1bb73cc4f3a9efe/chrome/browser/ui/webui/sync_file_system_internals/dump_database_handler.cc


### rz...@google.com (2022-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1311701?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059248)*
