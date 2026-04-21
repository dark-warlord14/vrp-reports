# Security: heap-use-after-free in network::NetworkContext::DestroyURLLoaderFactory

| Field | Value |
|-------|-------|
| **Issue ID** | [40067612](https://issues.chromium.org/issues/40067612) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Loader, Blink>SecurityFeature>CORS, Internals>Network |
| **Platforms** | Linux |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2023-07-18 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

In the process of NetworkContext destruction, CorsURLLoaderFactorys (owned by the NetworkContext) would be destroyed, which would abort all undergoing URLRequests processed by the URLLoaders. The following stack trace shows the key functions involved:

```
#1 net::URLRequest::~URLRequest
#2 network::URLLoader::~URLLoader
#3 network::cors::CorsURLLoaderFactory::~CorsURLLoaderFactory
#4 ~set
#5 network::NetworkContext::~NetworkContext
```

If there were active URLRequestHttpJob in the URLRequest and enqueued HttpTransaction in disk cache ActiveEntry, the dtor of URLRequest would also try to stop the job and delete the queued transactions. The problem is that the destruction of HttpTransaction could synchronously notify the corresponding URLLoader its completion (note that the URLLoader does not have to be the same with the one currently being destroyed), and further call URLLoader::DeleteSelf. If the URLLoader was the last one owned by CorsURLLoaderFactory, the CorsURLLoaderFactory would also delete itself by calling CorsURLLoaderFactory::DeleteIfNeeded. Key stack trace here:

```
#1  network::NetworkContext::DestroyURLLoaderFactory
#2  network::cors::CorsURLLoaderFactory::DeleteIfNeeded
#3  network::URLLoader::DeleteSelf
#4  network::URLLoader::NotifyCompleted
#5  network::URLLoader::OnResponseStarted
#6  net::URLRequestHttpJob::OnStartCompleted
#7  net::HttpCache::ProcessEntryFailure
#8  net::HttpCache::WritersDoneWritingToEntry
#9  net::HttpCache::DoneWithEntry
#10 net::HttpCache::Transaction::DoneWithEntry
#11 net::HttpCache::Transaction::~Transaction
#12 net::URLRequestHttpJob::DestroyTransaction
#13 net::URLRequestHttpJob::Kill
#14 net::URLRequest::DoCancel
#15 net::URLRequest::~URLRequest
```

This may lead to UAF when invoking std::set::find on `url_loader_factories_` which was currently being destroyed, because find could access the already deleted (but has not been cleared by std::set) DestroyURLLoaderFactory object stored in the container.

**VERSION**
Chrome Version: stable + dev

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**
Type of crash: network
Crash State: see asan report below

## Attachments

- [asan](attachments/asan) (text/plain, 54.8 KB)

## Timeline

### [Deleted User] (2023-07-18)

[Empty comment from Monorail migration]

### hi...@gmail.com (2023-07-18)

appen the asan log as a file because it's too long

### hi...@gmail.com (2023-07-18)

BTW， I do not have a replicable environment. I just encountered this issue incidentally and performed some analysis on the ASAN log

### rs...@chromium.org (2023-07-19)

Without more details or reproduction steps, this cannot be fully triaged. However, the ASan stack and explanation seem plausible.

horo: Could you reason through the code to see if there is a bug here?

[Monorail components: Blink>Loader Blink>SecurityFeature>CORS Internals>Network]

### [Deleted User] (2023-07-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2023-07-20)

[Blink>SecurityFeature triage] Setting status to Assigned as this already has an owner.

### ad...@google.com (2023-07-20)

(I am a bot: this is an auto-cc on a security bug)

### ri...@chromium.org (2023-07-21)

I think resolving https://crbug.com/chromium/1432903 should also fix this, but I don't know if we want to wait for that.

### vi...@google.com (2023-07-21)

Waiting for https://crbug.com/chromium/1432903 would make this P1 be blocked on lower priority bug, so I'd say we cannot wait, unless this issue is considered to be security severity Medium. 

### ho...@chromium.org (2023-07-24)

Sorry, I'm not familiar with the state management of HttpCache::Transaction.

ricea@
Could you please handle this?

### ri...@chromium.org (2023-07-28)

I'm not sure how to reproduce it but I know how to fix it.

### ri...@chromium.org (2023-07-31)

A rough sketch of a repro would be:

1. Create a NetworkContext
2. Create two CorsURLLoaderFactory's with this NetworkContext and the same NIK.
3. Create a URL request with the first factory and run it forward until it is waiting for the response headers.
4. Create a URL request with the second factory and run it forward until it is waiting on the cache lock.
5. Run the first request forward until it receives the response headers.
6. Destroy the NetworkContext.

It seems like the timing has to be very precise, but maybe I am missing some factor that makes it more likely to reproduce.

### gi...@appspot.gserviceaccount.com (2023-08-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e579b20308290df03f045c5d0ccb852d96b24ce3

commit e579b20308290df03f045c5d0ccb852d96b24ce3
Author: Adam Rice <ricea@chromium.org>
Date: Tue Aug 01 07:34:05 2023

NetworkContext: Don't access url_loader_factories_ during destruction

Move the contents of `url_loader_factories_` to a temporary variable in
the destructor of network::NetworkContext so that re-entrant calls to
DestroyURLLoaderFactory() don't happen after it has started being
destroyed.

BUG=1465833

Change-Id: I476f0865256bdcba4ec934688597e69991968f84
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4733351
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1177648}

[modify] https://crrev.com/e579b20308290df03f045c5d0ccb852d96b24ce3/services/network/network_context.h
[modify] https://crrev.com/e579b20308290df03f045c5d0ccb852d96b24ce3/services/network/network_context.cc


### ri...@chromium.org (2023-08-02)

CL https://chromium-review.googlesource.com/c/chromium/src/+/4733351 has now shipped in canary. Requesting merge to 116.

### [Deleted User] (2023-08-02)

Merge review required: M116 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2023-08-02)

> 1. Why does your merge fit within the merge criteria for these milestones?
> - Chrome Browser: https://chromiumdash.appspot.com/branches

High severity security fix.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/4733351

> 3. Have the changes been released and tested on canary?

Yes. There are no relevant crash reports in versions that have the fix.

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Manual testing not possible.

### am...@chromium.org (2023-08-02)

Thanks for rooting this out in terms of repro and fix, ricea@. 
Closing this as fixed so this can be included in the security merge review queue. Since the fix landed < 24 hours ago, I'm going to let this get a bit more bake time on Canary before reviewing for merge. 

Since the last scheduled updates of M115/Stable and M114/Extended, there's no necessary considerations for backmerging this further fix beyond M116 at this time. 
It would be helpful to understand, however, when this issue was introduced / how far back this issue has existing, so that we can update the FoundIn- as this affects some of our security<->release automation and processes. Thanks! 


### ri...@chromium.org (2023-08-03)

I don't think this was introduced by a recent change. It has probably been like this since at least 2018, M69.

### am...@chromium.org (2023-08-03)

Thank you! Wow, 2018 -- nice find of an old bug, Guang! The current oldest active release channel is 114/Extended, so updating labels accordingly. There's no need to backdate this as far back as M69. 

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-03)

M116 merge approved for https://crrev.com/c/4733351; please merge this fix to branch 5845 at your earliest convenience, before EOD Monday 7 August so this fix can be included in the M116 Stable cut -- thank you 

### [Deleted User] (2023-08-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4f1e8d9f683faac8acf72ac39eebdaf69c8627f0

commit 4f1e8d9f683faac8acf72ac39eebdaf69c8627f0
Author: Adam Rice <ricea@chromium.org>
Date: Tue Aug 08 08:48:51 2023

NetworkContext: Don't access url_loader_factories_ during destruction

Move the contents of `url_loader_factories_` to a temporary variable in
the destructor of network::NetworkContext so that re-entrant calls to
DestroyURLLoaderFactory() don't happen after it has started being
destroyed.

BUG=1465833

(cherry picked from commit e579b20308290df03f045c5d0ccb852d96b24ce3)

Change-Id: I476f0865256bdcba4ec934688597e69991968f84
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4733351
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1177648}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4756334
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Adam Rice <ricea@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5845@{#1252}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/4f1e8d9f683faac8acf72ac39eebdaf69c8627f0/services/network/network_context.h
[modify] https://crrev.com/4f1e8d9f683faac8acf72ac39eebdaf69c8627f0/services/network/network_context.cc


### ri...@chromium.org (2023-08-08)

Sorry I didn't get this merged yesterday.

### am...@google.com (2023-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-09)

Congratulations! The VRP Panel has decided to award you $2,000 for this report for a significantly mitigated - by tightly timed race condition and shutdown- security bug in a highly privileged (network) process. Thank you for your efforts and reporting this issue this issue to us. 

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1465833?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Loader, Blink>SecurityFeature>CORS, Internals>Network]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067612)*
