# use-after-free on  ReadingListDownloadService::DownloadUnprocessedEntries

| Field | Value |
|-------|-------|
| **Issue ID** | [349251460](https://issues.chromium.org/issues/349251460) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | UI>Browser>Mobile>ReadingList |
| **Platforms** | iOS |
| **Chrome Version** | 126.0.0.0 |
| **Reporter** | li...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-06-25 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. code audit
2. maybe poc upload soon.

# Problem Description

1. Classic mode, `ThreadPool` and `base::Unretained(this)`, if `ReadingListDownloadService` is destroyed before running `ReadingListDownloadService::DownloadUnprocessedEntries`, there is a possibility of UAF.

```
void ReadingListDownloadService::SyncWithModel() {
[...]
    base::ThreadPool::PostTaskAndReply(
        FROM_HERE,
        {base::MayBlock(), base::TaskPriority::USER_VISIBLE,
         base::TaskShutdownBehavior::SKIP_ON_SHUTDOWN},
        base::BindOnce(&::CleanUpFiles, OfflineRoot(), processed_directories),
        base::BindOnce(&ReadingListDownloadService::DownloadUnprocessedEntries,
                       base::Unretained(this), unprocessed_entries)); //
  }

```

2. `ReadingListDownloadService` inherits from `KeyedService`, so when the browser is closed, it will be UAF.

```
class ReadingListDownloadService
    : public KeyedService,
      public ReadingListModelObserver,
      public network::NetworkConnectionTracker::NetworkConnectionObserver {
 public:

```

3.`DownloadUnprocessedEntries` uses `this`

```
void ReadingListDownloadService::DownloadUnprocessedEntries(
    const std::set<GURL>& unprocessed_entries) {
  for (const GURL& url : unprocessed_entries) {
    this->ScheduleDownloadEntry(url);
  }
}

```

[0]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/reading_list/model/reading_list_download_service.mm;l=177>
[1]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/reading_list/model/reading_list_download_service.h;l=33;drc=90cac1911508d3d682a67c97aa62483eb712f69a>
[2]. <https://source.chromium.org/chromium/chromium/src/+/main:ios/chrome/browser/reading_list/model/reading_list_download_service.mm;l=184;drc=90cac1911508d3d682a67c97aa62483eb712f69a>

bitset:
<https://source.chromium.org/chromium/chromium/src/+/a859436434e4b45c9dacc9e5f0bd56c8616dba9e>

I can't see the earlier commit, so I point to the last commit that fixed it

# Summary

use-after-free on ReadingListDownloadService::DownloadUnprocessedEntries

# Custom Questions

#### Type of crash:

browser

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [fix5.patch](attachments/fix5.patch) (text/x-diff, 831 B)

## Timeline

### el...@chromium.org (2024-06-25)

I agree from code inspection that there is a UaF here. -> olivierrobin@ from //ios/chrome/browser/reading\_list/model/OWNERS, Pri-1 Sev-1 for now because it's a browser crash.

### ap...@google.com (2024-06-25)

Project: chromium/src
Branch: main

commit 8fc5f56c5eca90cd7a923d0f8144092144849692
Author: Olivier Robin <olivierrobin@google.com>
Date:   Tue Jun 25 19:58:49 2024

    Fix uaf in ReadingListDownloadService
    
    Fixed: 349251460
    Change-Id: I1030759eab496d9746e285b220881b597aa7c227
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5654812
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Elly FJ <ellyjones@chromium.org>
    Commit-Queue: Olivier Robin <olivierrobin@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1319334}

M       ios/chrome/browser/reading_list/model/reading_list_download_service.mm

https://chromium-review.googlesource.com/5654812


### li...@gmail.com (2024-06-26)

Notice:
IOS does not enable MiraclePtr, so this Unretained (this) is not protected by MiraclePtr/BackupRefPtr

### pe...@google.com (2024-06-26)

Setting milestone because of s0/s1 severity.

### li...@gmail.com (2024-06-27)

Hi,please update the credit to : lime(@limeSec\_) From TIANGONG Team of Legendsec at QI-ANXIN Group, thanks. :)

### ol...@chromium.org (2024-06-28)

Which CLs should be backmerged? (Please include Gerrit links.)
https://chromium-review.googlesource.com/c/chromium/src/+/5654812

Has this fix been verified on Canary to not pose any stability regressions?
Yes

Does this fix pose any potential non-verifiable stability risks?
No

Does this fix pose any known compatibility risks?
No

Does it require manual verification by the test team? If so, please describe required testing.
No

### am...@chromium.org (2024-07-01)

Please refrain from manually entering merge requests and reviews. The bot will do this, which is why it's important for security issues to be closed as fixed when the resolving CL lands. 
This merge request was improperly formatting and was not trigging an entry in the security queue. 
Because there has been human intervention, the bot will not respond so I'm manually updating the merge tags. 

### am...@chromium.org (2024-07-01)

While this is a browser UAF, it's also speculative as presented. Walking through the code, triggering this issue does not appear to be remote exploitable and would require a fair amount of user interaction. There is also a precondition of shutdown, providing lesser attacker control. 
Given that we are in a release freeze & that there is no Canary data for iOS, I'm wary to backmerge. Looking at this fix, however, I'm less worried about risk. However, given the limitations here, and that M127 Stable RC is being cut directly following release freeze, I'm approving backmerge only to M127.
Please merge this fix to branch 6533 before EOD Monday, 15 July, so this fix an be included in M127 Stable RC for release on 23 July. 

### ap...@google.com (2024-07-02)

Project: chromium/src
Branch: refs/branch-heads/6533

commit 27a5d6c34a5288199e3bd1c3290e2c659724ed9d
Author: Olivier Robin <olivierrobin@google.com>
Date:   Tue Jul 02 17:58:56 2024

    [127] Fix uaf in ReadingListDownloadService
    
    (cherry picked from commit 8fc5f56c5eca90cd7a923d0f8144092144849692)
    
    Fixed: 349251460
    Change-Id: I1030759eab496d9746e285b220881b597aa7c227
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5654812
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Reviewed-by: Elly FJ <ellyjones@chromium.org>
    Commit-Queue: Olivier Robin <olivierrobin@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1319334}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5672183
    Auto-Submit: Olivier Robin <olivierrobin@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6533@{#959}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       ios/chrome/browser/reading_list/model/reading_list_download_service.mm

https://chromium-review.googlesource.com/5672183


### sp...@google.com (2024-07-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of highly mitigated memory corruption in a non-sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-03)

Thank you for this report, lime. This issue was determined to be highly mitigated, as noted in c#9, this is a report of a speculative issue that does not appear to be remote exploitable and would require a fair amount of user interaction. There is also a precondition of shutdown, providing lesser attacker control. Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-10-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349251460)*
