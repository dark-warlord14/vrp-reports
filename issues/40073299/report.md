# potentional UAF 

| Field | Value |
|-------|-------|
| **Issue ID** | [40073299](https://issues.chromium.org/issues/40073299) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Logging |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | li...@gmail.com |
| **Assignee** | bi...@chromium.org |
| **Created** | 2023-09-25 |
| **Bounty** | Confirmed (amount unknown) |

## Description

**Steps to reproduce the problem:**  

1.  

2.  

3.0

**Problem Description:**  

found by code audit,so if i was wrong ,please ingore it ,thanks.

[0] pass Unretained(this) to OnStartNetLogBoundedScratchDirectoryCreated , then post the task to ThreadPool. so if we destruct the NetworkService ,it will accur uaf.

```
void NetworkService::StartNetLogBounded(base::File file,  
                                        uint64_t max_total_size,  
                                        net::NetLogCaptureMode capture_mode,  
                                        base::Value::Dict client_constants) {  
  base::Value::Dict constants = net::GetNetConstants();  
  constants.Merge(std::move(client_constants));  
  
  base::ThreadPool::PostTaskAndReplyWithResult( <---- post to ThreadPool  
      FROM_HERE,  
      {base::MayBlock(), base::TaskShutdownBehavior::SKIP_ON_SHUTDOWN},  
      base::BindOnce(&NetLogExporter::CreateScratchDirForNetworkService,  
                     base::PassKey<NetworkService>()),  
  
      base::BindOnce(  
          &NetworkService::OnStartNetLogBoundedScratchDirectoryCreated,  
          base::Unretained(this), std::move(file), max_total_size, capture_mode,  <---- [0]   
          std::move(constants)));  
}  

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:services/network/network_service.cc;l=1030;drc=5a2e12875a8fe207bfe6f0febc782b6297788b6d;bpv=1;bpt=1>

**Additional Comments:**

\*\*Chrome version: \*\* lastest \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Timeline

### li...@gmail.com (2023-09-25)

potential UAF in NetworkService::StartNetLogBounded

### [Deleted User] (2023-09-25)

[Empty comment from Monorail migration]

### li...@gmail.com (2023-09-25)

FIX
change the Unretained(this) to WeakPtr.

### do...@chromium.org (2023-09-26)

Thanks for the report. I agree that this does seem to be a potential UaF on shutdown. +bingler and cc reviewers of https://chromium-review.googlesource.com/c/chromium/src/+/4706170 where this was added.

Setting a Medium severity as it's a network service UaF, and mitigated by being isolated to the net-export page and potentially only on shutdown.

[Monorail components: Internals>Network>Logging]

### [Deleted User] (2023-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bi...@chromium.org (2023-09-26)

I'm working on this now.

The bug is thankfully hard to hit as this code path is only reached during the creation of the network service which is unlikely to occur during shutdown. Maybe a crash of the service could trigger it?

### ad...@google.com (2023-09-26)

(I am a bot: this is an auto-cc on a security bug)

### gi...@appspot.gserviceaccount.com (2023-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b348ed9f06e4209e8150eb695b724d7401d83854

commit b348ed9f06e4209e8150eb695b724d7401d83854
Author: sbingler <bingler@chromium.org>
Date: Wed Sep 27 00:07:20 2023

Use WeakPtr in StartNetLogBounded

Replace the base::Unretained with WeakPtr to improve memory safety.

Bug: 1486439
Change-Id: Ia93d24d63e176b992c6ef52e1ec06e646bfa15ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4894827
Commit-Queue: Matt Menke <mmenke@chromium.org>
Commit-Queue: Steven Bingler <bingler@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1201891}

[modify] https://crrev.com/b348ed9f06e4209e8150eb695b724d7401d83854/services/network/network_service.h
[modify] https://crrev.com/b348ed9f06e4209e8150eb695b724d7401d83854/services/network/network_service.cc


### bi...@chromium.org (2023-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-01)

Requesting merge to beta M118 because latest trunk commit (1201891) appears to be after beta branch point (1192594).

Merge review required: M118 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@gmail.com (2023-10-02)

[Comment Deleted]

### li...@gmail.com (2023-10-02)

[Comment Deleted]

### am...@chromium.org (2023-10-03)

This issue appears to be significantly mitigated so I agree with Medium severity here for a potential network process UAF. 
M118 Stable RC is being cut tomorrow (Tuesday), so timing wise this ordinarily wouldn't be great, but this fix was landed six days ago and is a pretty safe fix, thus approving merge for https://crrev.com/c/4894827 for M118 before 10am tomorrow if possible, so this fix can be included in M118 Stable RC. TY

### da...@google.com (2023-10-03)

To ensure there is sufficient time to go through CQ and ready for Early Stable cut tonight, I have CP the CL.

### gi...@appspot.gserviceaccount.com (2023-10-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/68161e020eddbe202f8efa1d607f8a7724e53a81

commit 68161e020eddbe202f8efa1d607f8a7724e53a81
Author: sbingler <bingler@chromium.org>
Date: Tue Oct 03 11:14:12 2023

Use WeakPtr in StartNetLogBounded

Replace the base::Unretained with WeakPtr to improve memory safety.

(cherry picked from commit b348ed9f06e4209e8150eb695b724d7401d83854)

Bug: 1486439
Change-Id: Ia93d24d63e176b992c6ef52e1ec06e646bfa15ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4894827
Commit-Queue: Matt Menke <mmenke@chromium.org>
Commit-Queue: Steven Bingler <bingler@chromium.org>
Reviewed-by: Matt Menke <mmenke@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1201891}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4905817
Auto-Submit: Daniel Yip <danielyip@google.com>
Owners-Override: Daniel Yip <danielyip@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Daniel Yip <danielyip@google.com>
Cr-Commit-Position: refs/branch-heads/5993@{#1086}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/68161e020eddbe202f8efa1d607f8a7724e53a81/services/network/network_service.h
[modify] https://crrev.com/68161e020eddbe202f8efa1d607f8a7724e53a81/services/network/network_service.cc


### [Deleted User] (2023-10-03)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-10-04)

Introduced in M117 so not applicable to LTS.

### am...@chromium.org (2023-10-05)

Thank you for this report. The VRP Panel has decided to decline a reward for this report due to it only presenting a speculative / theoretical vulnerability, with no evidence of exploitability, reachability, or process impact. Additionally, based on our assessment, this issue is significantly mitigated by race condition, shutdown / network service restart, and precondition of the kLogNetLog flag. 


### li...@gmail.com (2023-10-05)

hi, can this report have eligible to get a cve number?

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-10)

regarding #23, we can only issue CVE numbers for security issues / issue that can demonstrably be exploited, therefore, we are unfortunately unable to issue a CVE for this issue 

### pg...@google.com (2023-10-10)

Removing incorrectly added label

### [Deleted User] (2024-01-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1486439?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073299)*
