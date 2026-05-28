# Security: Heap-use-after-free in BrowsingTopicsServiceImpl::GetBrowsingTopicsStateForWebUi

| Field | Value |
|-------|-------|
| **Issue ID** | [40067522](https://issues.chromium.org/issues/40067522) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>TopicsAPI |
| **Platforms** | Mac |
| **Reporter** | me...@gmail.com |
| **Assignee** | ab...@chromium.org |
| **Created** | 2023-07-17 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply the patch to Chromium and compile Chromium with ASAN enabled
2. run `./Chromium --user-data-dir=./noexist`  and open `chrome://topics-internals`
3. close the browser  
   
   Note: I repro this on MAC

**Problem Description:**

1. Analysis

`GetBrowsingTopicsStateForWebUi` passes a callback with `Unretained(this)`[1] to `GetContextDomainsFromHashedContextDomains`[2]. `GetContextDomainsFromHashedContextDomains` will `AsyncCall` some other function and then call the callback. Because that `AsyncCall` will run on a ThreadPool, we could free `BrowsingTopicsServiceImpl` during the ThreadPool, just before the callback is invoked => UAF occurs.  

To trigger this easily, I add a sleep to the ThreadPool.

```
void BrowsingTopicsServiceImpl::GetBrowsingTopicsStateForWebUi(  
    bool calculate_now,  
    mojom::PageHandler::GetBrowsingTopicsStateCallback callback) {  
  if (!browsing_topics_state_loaded_) {  
    std::move(callback).Run(  
        mojom::WebUIGetBrowsingTopicsStateResult::NewOverrideStatusMessage(  
            "State loading hasn't finished. Please retry shortly."));  
    return;  
  }  
  
  // If a calculation is already in progress, get the webui topics state after  
  // the calculation is done. Do this regardless of whether `calculate_now` is  
  // true, i.e. if `calculate_now` is true, this request is effectively merged  
  // with the in progress calculation.  
  if (topics_calculator_) {  
    get_state_for_webui_callbacks_.push_back(std::move(callback));  
    return;  
  }  
  
  DCHECK(schedule_calculate_timer_.IsRunning());  
  
  if (calculate_now) {  
    get_state_for_webui_callbacks_.push_back(std::move(callback));  
    schedule_calculate_timer_.AbandonAndStop();  
    CalculateBrowsingTopics(/\*is_manually_triggered=\*/true);  
    return;  
  }  
  
  site_data_manager_->GetContextDomainsFromHashedContextDomains(  
      GetAllObservingDomains(browsing_topics_state_),  
      base::BindOnce(  
          &BrowsingTopicsServiceImpl::GetBrowsingTopicsStateForWebUiHelper,  
          base::Unretained(this), std::move(callback)));  
}  

```
```
void BrowsingTopicsSiteDataManagerImpl::  
    GetContextDomainsFromHashedContextDomains(  
        const std::set<browsing_topics::HashedDomain>& hashed_context_domains,  
        BrowsingTopicsSiteDataManager::  
            GetContextDomainsFromHashedContextDomainsCallback callback) {  
  storage_  
      .AsyncCall(&BrowsingTopicsSiteDataStorage::  
                     GetContextDomainsFromHashedContextDomains)  
      .WithArgs(hashed_context_domains)  
      .Then(std::move(callback));  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/browsing_topics/browsing_topics_service_impl.cc;l=548;bpv=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/browsing_topics/browsing_topics_site_data_manager_impl.cc;l=77>

Please note that function `BrowsingTopicsServiceImpl::OnCalculateBrowsingTopicsCompleted` passes an `Unretained(this)` to the callback, the callback is also invoked by `GetContextDomainsFromHashedContextDomains`. This `Unretained(this)` will also result in UAF as I mentioned above. Considering that they are introduced by the same commit, I didn't submit a new issue.

[3] <https://source.chromium.org/chromium/chromium/src/+/main:components/browsing_topics/browsing_topics_service_impl.cc;l=705;bpv=0>

2. Bisect

This problem is introduced by this commit: 9243f6ac4417e4480e575f42a1a45e56fa336243  

<https://chromium-review.googlesource.com/c/chromium/src/+/4670036>

3. Suggested Patch  
   
   Use WeakPtr instead of Unretained.

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [change.txt](attachments/change.txt) (text/plain, 768 B)
- [asan.txt](attachments/asan.txt) (text/plain, 32.2 KB)
- [video.mov](attachments/video.mov) (video/quicktime, 7.4 MB)

## Timeline

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### bo...@google.com (2023-07-17)

Thanks for the report. 

Setting FoundIn-117 based on the referenced commit, which landed in M117. 

This report starts at Severity High (memory corruption in browser process assuming compromise of renderer process), but -1 severity due to requirement for user interaction with UI elements. 

@yaoxia, I was unable to reproduce this crash on Windows and I lack the means to test on a Mac, so I'm trusting the reporter's assessment since they have a very long history of valid reports. Another shepherd from Chrome Security may be able to help test reproducibility before you get to this, but in the interest of getting plausibly valid reports in front of an owner quickly, please accept my apologies for routing without confirming reproducibility. 

[Monorail components: Blink>TopicsAPI]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### ya...@chromium.org (2023-07-17)

abigailkatcoff@: PTAL. It seems instead of passing `base::Unretained(this)`, we should be passing `weak_ptr_factory_.GetWeakPtr()`.

### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7dda1e504e249317070fd8d1a89526eba07e6b49

commit 7dda1e504e249317070fd8d1a89526eba07e6b49
Author: Abigail Katcoff <abigailkatcoff@chromium.org>
Date: Tue Jul 18 15:39:35 2023

Topics API: Fix use after free in GetBrowsingTopicsStateForWebUi

Replace usages of Unretained(this) with WeakPtr.

Bug: 1465293
Change-Id: Ie391cae0534f513142057182c21ba999d7583498
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4695135
Reviewed-by: Yao Xiao <yaoxia@chromium.org>
Commit-Queue: Yao Xiao <yaoxia@chromium.org>
Commit-Queue: Abigail Katcoff <abigailkatcoff@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1171765}

[modify] https://crrev.com/7dda1e504e249317070fd8d1a89526eba07e6b49/components/browsing_topics/browsing_topics_service_impl.cc


### [Deleted User] (2023-07-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2023-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-28)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-08-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-03)

Congratulations, Krace! The VRP Panel has decided to award you $1,000 for this report of a significantly mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us. 

### am...@chromium.org (2023-08-03)

I meant to add above that the reward amount was based this bug being "significantly mitigated" by user gesture, browser shutdown (limiting the exploitability), and MiraclePtr protection. 

### am...@google.com (2023-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-10)

Not requesting merge to dev (M117) because latest trunk commit (1171765) appears to be prior to dev branch point (1181205). If this is incorrect, please replace the Merge-NA-117 label with Merge-Request-117. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M117. Please go ahead and merge the CL to branch 5938 (refs/branch-heads/5938) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2023-08-14)

Your Cl has been already approved for M117 Branch and we are cutting M117 Beta RC tomorrow i.e., Aug-15th, so request  you to get the CL's cherry pick before Noon tomorrow so that we get maximum Beta coverage for the CL please.



### am...@chromium.org (2023-08-16)

fix landed on 117, no merge needed

### [Deleted User] (2023-10-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1465293?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067522)*
