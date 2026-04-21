# Security:  UAF in UnblockPendingSubframeNavigationRequestsIfNeeded

| Field | Value |
|-------|-------|
| **Issue ID** | [40070041](https://issues.chromium.org/issues/40070041) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>History |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | yq...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2023-08-20 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The function `UnblockPendingSubframeNavigationRequestsIfNeeded`` calls` Resume`at line [1]. Calling`Resume` may delete NavigationRequest synchronously [2], which result in UAF write at line [3].

This issue is similar to [crbug.com/1417122](https://crbug.com/1417122),1417133,1444360.it's just a potential UAF but I will construct PoC later.

```
void NavigationRequest::UnblockPendingSubframeNavigationRequestsIfNeeded() {  
  // After a main frame same-document history navigation completes successfully,  
  // we can resume any corresponding subframe history navigations that were  
  // blocked on it.  
  for (auto& throttle : subframe_history_navigation_throttles_) {  
    if (throttle) {  
      throttle->Resume();  //   [1]  
    }  
  }  
  subframe_history_navigation_throttles_.clear(); //  [3]  
}  
  
  
void NavigationRequest::Resume(NavigationThrottle\* resuming_throttle) {  
  DCHECK(resuming_throttle);  
  CHECK(!is_resuming_) << "This call does not support re-entrancy.";  
  EnterChildTraceEvent("Resume", this);  
  is_resuming_ = true;  
  
  // Stop watching for response body changes to ensure that the response body  
  // callback isn't called later in the throttle's lifetime with a response body  
  // that is not relevant to the throttle.  
  if (response_body_watcher_) {  
    CHECK(response_body_callback_);  
    response_body_watcher_.reset();  
    std::move(response_body_callback_).Run(std::string());  
  }  
  
  is_resuming_ = false;  
  throttle_runner_->ResumeProcessingNavigationEvent(resuming_throttle);   //[2]  
  // DO NOT ADD CODE AFTER THIS, as the NavigationHandle might have been deleted  
  // by the previous call.  
}  
  
  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;drc=48290eaa6a80203b317bff0b5e6cf91005602c41;bpv=1;bpt=1;l=9205>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=6660;drc=48290eaa6a80203b317bff0b5e6cf91005602c41>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;drc=48290eaa6a80203b317bff0b5e6cf91005602c41;bpv=1;bpt=1;l=9208>

**VERSION**  

Chrome Version: stable

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

## Timeline

### [Deleted User] (2023-08-20)

[Empty comment from Monorail migration]

### jd...@chromium.org (2023-08-21)

japhet@: this is your code, can you take a look?

I'm tentatively setting Sev-High, but it could be Sev-Critical, or if it's inaccessible, it might not even be a security bug. The code here is complicated enough that I can't easily tell if this is actually exploitable or not. 

reporter: Providing a PoC would go a long way to ensuring that this bug is prioritized appropriately. Quoting from our VRP rules [1], "All reports ... must provide a convincing explanation or evidence of exploitability (such as through a POC), and/or numbered reproduction steps rather than simply consisting of static analysis of code." Thanks!

[1] https://www.google.com/about/appsecurity/chrome-rewards/

[Monorail components: Blink>History]

### [Deleted User] (2023-08-21)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-08-21)

I'm not familiar enough with the cases in which NavigationThrottle::Resume() can lead to deletion to know whether that's a realistic concern in this situation.

That said, this should be extremely simple to defend against if we want to just go ahead with it (checking a self-WeakPtr after each Resume() call).

### jd...@chromium.org (2023-08-21)

Thanks Nate! If you're willing to fix it, please do so, especially since it's straightforward. We can treat it as Sev-High out of an abundance of caution and then if the reporter isn't able to actually demonstrate exploitability, the VRP will take that into separate consideration.

### ja...@chromium.org (2023-08-21)

Proposed fix: https://chromium-review.googlesource.com/c/chromium/src/+/4799935

### [Deleted User] (2023-08-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@chromium.org (2023-08-23)

It is not clear to me that this UaF can happen. I agree with japhet@ that trying to be proactively defensive is a good idea, but without a PoC I don't think we can reason whether the bug is possible or not.

### gi...@appspot.gserviceaccount.com (2023-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/418de85d4ae13cd902a154ac94976c2d6a836268

commit 418de85d4ae13cd902a154ac94976c2d6a836268
Author: Nate Chapin <japhet@chromium.org>
Date: Wed Aug 23 18:22:04 2023

Guard against NavigationThrottle::Resume misbehavior in NavigationRequest:: UnblockPendingSubframeNavigationRequestsIfNeeded

Bug: 1474253
Change-Id: I7b4dafdda90e3d71e4d2313ea718590c27014866
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4799935
Reviewed-by: Nasko Oskov <nasko@chromium.org>
Commit-Queue: Nate Chapin <japhet@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1187391}

[modify] https://crrev.com/418de85d4ae13cd902a154ac94976c2d6a836268/content/browser/renderer_host/navigation_request.cc


### [Deleted User] (2023-09-05)

japhet: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-05)

It appears this issue is speculative and the CL in https://crbug.com/chromium/1474253#c9 would resolve this issue based on the information provided. Closed as fixed, reduced severity to medium since this appears to be speculative and potentially not exploitable. 

### [Deleted User] (2023-09-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations! The Chrome VRP Panel has decided to award you $1,000 for this report. The reward amount was decided based on the report quality, and that no evidence of vulnerability was provided, and no exploitability or security consequences were demonstrated. Since we were able to make a security relevant change, we did want to reward you for this discovery. Thank you for your efforts and reporting this finding to us. 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1474253?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ar...@chromium.org (2024-03-08)

NavigationRequest is uniquely owned by `std::unique_ptr<T>`.

Given the libc++ implementation of [`std::unique_ptr<T>::reset`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libc++/src/include/__memory/unique_ptr.h;l=275-280;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090).

```
  _LIBCPP_HIDE_FROM_ABI _LIBCPP_CONSTEXPR_SINCE_CXX23 void reset(pointer __p = pointer()) _NOEXCEPT {
    pointer __tmp  = __ptr_.first();
    __ptr_.first() = __p;
    if (__tmp)
      __ptr_.second()(__tmp);
  }

```

The address is moved to the stack first, before calling the destructor.
It means a re-entrant `.reset()` won't call the destructor twice.

Since this potential bug was in the NavigationRequest destructor, we can prove this is **never problematic**.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070041)*
