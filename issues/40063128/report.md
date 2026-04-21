# Security: UAF when code runs after NavigationThrottle's Resume() or CancelDeferredNavigation() are called

| Field | Value |
|-------|-------|
| **Issue ID** | [40063128](https://issues.chromium.org/issues/40063128) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Reporter** | jt...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2023-02-17 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

The function `NavigationRequest::RendererCancellationWindowEnded` runs the callback renderer\_cancellation\_window\_ended\_callback\_ at line [1]. And the renderer\_cancellation\_window\_ended\_callback\_ is `RendererCancellationThrottle::NavigationCancellationWindowEnded`, which calls `Resume` at line [2]. Calling `Resume` may delete NavigationRequest synchronously, which result in UAF write at line [3].

This issue is similar to anthter one I reported ([crbug.com/1417122](https://crbug.com/1417122)) -- UAF caused by accessing member variables after calling function `Resume`. According to other callsites of `Resume`, there is code comment saying "Resume() may have deleted `this`." [4], and [crbug.com/1417122](https://crbug.com/1417122) provides a PoC to demonstrate it. I didn't construct the PoC for this issue (sorry about that, time limited), so it's just a potential UAF. Feel free to close it if you believe it not a security issue :)

```
void NavigationRequest::RendererCancellationWindowEnded() {  
  // The renderer had indicated that the navigation cancellation window had  
  // ended, so the navigation can resume if it is currently waiting for this  
  // signal.  
  renderer_cancellation_window_ended_ = true;  
  if (renderer_cancellation_window_ended_callback_) {  
    std::move(renderer_cancellation_window_ended_callback_).Run();  // ===> [1]  
  }  
  renderer_cancellation_listener_.reset();  // ===> [3]  
}  
  
void RendererCancellationThrottle::NavigationCancellationWindowEnded() {  
  CHECK(NavigationRequest::From(navigation_handle())  
            ->renderer_cancellation_window_ended());  
  // Stop the timeout and notify that renderer is responsive if necessary.  
  renderer_cancellation_timeout_timer_.Stop();  
  NavigationRequest\* request = NavigationRequest::From(navigation_handle());  
  request->GetRenderFrameHost()->GetRenderWidgetHost()->RendererIsResponsive();  
  
  Resume();  // ===> [2]  
}  
  
void PrerenderSubframeNavigationThrottle::DidFinishNavigation(  
    NavigationHandle\* nav_handle) {  
  // skip  
  // Resume the subframe navigation.  
  if (!is_deferred_)  
    return;  
  is_deferred_ = false;  
  Resume();  
  // Resume() may have deleted `this`.  // ===> [4]  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=8567;drc=4ced8912f6c8b32715984dd81e3f376a260ebab6>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/renderer_cancellation_throttle.cc;l=87;drc=4ced8912f6c8b32715984dd81e3f376a260ebab6>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=8569;drc=4ced8912f6c8b32715984dd81e3f376a260ebab6>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/preloading/prerender/prerender_subframe_navigation_throttle.cc;l=150;drc=4ced8912f6c8b32715984dd81e3f376a260ebab6>

**VERSION**  

Chrome Version: stable

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

## Timeline

### [Deleted User] (2023-02-17)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-02-17)

Thank you for your report. This report does not contain enough technical information sufficient to be considered to demonstrate exploitability or security consequences. 

Without further actionable information (e.g. POC / reproduction steps / symbolized stack trace), the Chrome Security team is unable to reproduce this bug. We do not have definite evidence that this bug is a reachable, exploitable security bug in Chrome and we need your help to assess.

rakina@, can you briefly review this issue, and if possible, provide a comment explaining whether you believe this condition can be achieved in a production version of Chrome? It would also be helpful to know if you think this is a recent regression or not. If you believe this issue is real, please prioritize a fix.

Note: In case this is a real bug, setting the severity to Critical due to a UAF in the browser process.

[Monorail components: Internals>Sandbox>SiteIsolation]

### [Deleted User] (2023-02-18)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-18)

[Empty comment from Monorail migration]

### ra...@chromium.org (2023-02-21)

Thanks for the report. Yes, I think deletion of the NavigationRequest is possible after we run NavigationThrottle::Resume() if we end up at calling OnRequestFailedInternal() [1] -> MaybeCancelFailedNavigation() [2] which might delete the NavigationRequest, although only in some cases (<object> element and aborted navigations?). There's also NavigationThrottle::CancelDeferredNavigation() which might also result in deletion of the NavigationRequest in the same way.

I audited other usages of Resume() and looks like there are other throttles that still have code after Resume() and CancelDeferredNavigation() calls. I've made crrev.com/c/4273107 to fix them.

Aside from that, I wonder if there's something that we can do to avoid this problem from happening again in the future. We already have comments about the potential deletions caused by calling these functions both in the method and a lot of the callsites, but that seems easy to overlook/forget. Naming the functions more explicitly (e.g. ResumeMayDeleteThrottle()) might make it more noticeable I guess, but I wonder if we can make something like an automatic (compile-time?) check that ensures these functions are the last things called from the callers..

[1]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=4260;drc=d6736f594e04d48d710ef41d24ce85f0e7699335
[2]: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=8228;drc=d6736f594e04d48d710ef41d24ce85f0e7699335

[Monorail components: UI>Browser>Navigation]

### gi...@appspot.gserviceaccount.com (2023-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/483bfa8d8f1483d8c4eb01524730bb52ca861985

commit 483bfa8d8f1483d8c4eb01524730bb52ca861985
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Sun Feb 26 12:58:28 2023

Ensure calls to NavigationThrottle's Resume and CancelDeferredNavigation aren't followed by other code

These functions might result in the deletion of the NavigationRequest
owning the NavigationThrottle, so if there are code that runs in the
NavigationRequest/NavigationThrottle after that, it might result in
a UAF.

This CL moves the code that can run after those calls to run earlier
instead, and adds comments to prevent more code from being added
after the calls.

Bug: 1417133, 1419020
Change-Id: I81e594b33a5731a7e0cf5b8640395c3df137eb10
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4273107
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
Owners-Override: Alex Moshchuk <alexmos@chromium.org>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1110080}

[modify] https://crrev.com/483bfa8d8f1483d8c4eb01524730bb52ca861985/fuchsia_web/webengine/browser/navigation_policy_throttle.cc
[modify] https://crrev.com/483bfa8d8f1483d8c4eb01524730bb52ca861985/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/483bfa8d8f1483d8c4eb01524730bb52ca861985/content/browser/devtools/protocol/target_handler.cc


### ra...@chromium.org (2023-02-27)

So this particular bug (and I think all remaining bugs that goes through a similar path) has been fixed, but I've filed crbug.com/1419020 for the follow-up work on improving this general area as mentioned in https://crbug.com/chromium/1417133#c5.

### [Deleted User] (2023-02-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, Rong! The VRP Panel has decided to award you $10,000 for this issue -- the amount was decided based on this issue not being reproducible or demonstrable as exploitable. If this issue were exploitable or someone determined a way to exploit it, it would be seemingly sufficiently impactful but also potentially mitigated; therefore, since the information you provided allowed us to land a patch to prevent this possibility. Thank you for your efforts and reporting this to us! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1417133?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063128)*
