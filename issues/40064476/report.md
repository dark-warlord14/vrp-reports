# Security: UAF in CommitErrorPage

| Field | Value |
|-------|-------|
| **Issue ID** | [40064476](https://issues.chromium.org/issues/40064476) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2023-05-10 |
| **Bounty** | $30,000.00 |

## Description

When the renderFrameHost commits to an error page[1], if the renderFrameHost is not live[2], the NavigationRequest will be destroyed.  

Then the UAF will be triggered when returning to call the function PopulateDocumentTokenForCrossDocumentNavigation[3] and access the member variables.

```
void NavigationRequest::CommitErrorPage(  
    const absl::optional<std::string>& error_page_content) {  
    [...]  
    ReadyToCommitNavigation(true /\* is_error \*/);    <-------- [1]  
  
    PopulateDocumentTokenForCrossDocumentNavigation();    <-------- [3]  
    [...]  
}  
  
void NavigationRequest::ReadyToCommitNavigation(bool is_error) {  
    [...]  
    if (!GetRenderFrameHost()->IsRenderFrameLive()) {    <-------- [2]  
      OnNavigationClientDisconnected(0, "");  
      // DO NOT ADD CODE AFTER THIS, as the NavigationHandle has been deleted  
      // by the previous call.  
      return;  
    }  
    [...]  
}  

```

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=5582;drc=77ae2b0fa84ba68418d58af091745e49f7e8c512>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/renderer_host/navigation_request.cc;l=7250;drc=77ae2b0fa84ba68418d58af091745e49f7e8c512>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=5584;drc=77ae2b0fa84ba68418d58af091745e49f7e8c512>

In POC, I used the ssl error handler as the error page. And set the renderFrameHost to not live state by sending an error mojo message[4] before ShowSSLInterstitial[5]. You can also try to trigger it in other ways.

```
void RenderFrameHostImpl::UpdateTitle(  
  [...]  
  if (received_title.length() > blink::mojom::kMaxTitleChars) {  
    mojo::ReportBadMessage("Renderer sent too many characters in title.");    <-------- [4]  
    return;  
  }  
  [...]  
}  

```
```
void SSLErrorHandler::StartHandlingError() {  
  [...]  
  if (IsCaptivePortalInterstitialEnabled() && !is_captive_portal_login_tab) {  
    delegate_->CheckForCaptivePortal();  
    timer_.Start(FROM_HERE, g_config.Pointer()->interstitial_delay(), this,  
                 &SSLErrorHandler::ShowSSLInterstitial);       <-------- [5]  
    if (g_config.Pointer()->timer_started_callback())  
      g_config.Pointer()->timer_started_callback()->Run(web_contents());  
    return;  
  }  
  [...]  
}  

```

[4]. <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:content/browser/renderer_host/render_frame_host_impl.cc;l=6315;drc=fa20eae012f6180ac08242b7823e27f5fbd9122a;bpv=0;bpt=0>  

[5]. <https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:components/security_interstitials/content/ssl_error_handler.cc;l=802;drc=12be03159fe22cd4ef291e9561762531c2589539>

**VERSION**  

Chrome Version: M113 stable  

Operating System: test in win

Bisect:  

<https://source.chromium.org/chromium/chromium/src/+/79bd493f8f229ef060e2dd2eb91612032bf84440>

**REPRODUCTION CASE**

Apply poc.diff  

$ python3 server.py  

$ out/asan/chrome.exe --user-data-dir=xxxx "<https://localhost:8000/poc.html>" --no-first-run

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: browser  

Crash State: asan file

## Attachments

- [server.py](attachments/server.py) (text/plain, 1.5 KB)
- [poc.diff](attachments/poc.diff) (text/plain, 785 B)
- [asan](attachments/asan) (text/plain, 27.5 KB)
- [https_svr_key.pem](attachments/https_svr_key.pem) (application/octet-stream, 3.0 KB)

## Timeline

### [Deleted User] (2023-05-10)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-05-11)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2023-05-11)

Thanks for the report!

rakina@: Can you take a look at this one, as a similar "use NavigationRequest after it's deleted" case as https://crbug.com/chromium/1417133 and https://crbug.com/chromium/1417122?

Tentatively rating Critical and Pri-0, similar to those issues, but I haven't tried to confirm the bug or check if there are any mitigating factors.

### cr...@chromium.org (2023-05-11)

It looks like the poc.html file mentioned in the repro steps wasn't uploaded with the report.  Could you upload that as well?  Thanks!

### me...@chromium.org (2023-05-11)

[Empty comment from Monorail migration]

### me...@chromium.org (2023-05-11)

creis: I don't think there is an actual poc.html. Instead, server.py handles the path "/poc.html" and returns an empty 200 response.

### me...@chromium.org (2023-05-12)

FWIW, I'm unable to trigger a UAF in M112 or M113. The renderer gets killed due to the patch poc.diff but ASAN doesn't report anything otherwise.

### hi...@gmail.com (2023-05-12)

I can reproduce it  stably,  I reproduce it on the Window platform.

### ra...@chromium.org (2023-05-12)

Thanks for the report! I've made a fix CL with a regression test at crrev.com/c/4520493. I think this needs the error page navigation to use an existing RenderFrameHost instead of creating a speculative RFH, because in the latter case the navigation will get cancelled earlier if the process crashed. So this means it can only happen on same-RenderFrameHost navigations, and for main frame navigations that means navigating from an error page to an error page again due to error page isolation (for subframe navs error pages are not isolated, so same-RFH navigations can happen even if the previous page is not an error page). Not sure if that means the severity can be marked as lower.

### gi...@appspot.gserviceaccount.com (2023-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/42db806805ef2be64ee92803d3a784631b2a7df0

commit 42db806805ef2be64ee92803d3a784631b2a7df0
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Fri May 12 16:09:05 2023

Return after ReadyCommitNavigation call in CommitErrorPage if it deletes NavigationRequest

NavigationRequest::ReadyToCommitNavigation() can cause deletion of the
NavigationRequest, so callers should check for that possibility after
calling the function. A caller in CommitErrorPage is missing that
check, which this CL adds, along with a regression test.

Bug: 1444360
Change-Id: I3964da4909a6709b7730d25d6497b19c098f4f21
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4520493
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1143298}

[modify] https://crrev.com/42db806805ef2be64ee92803d3a784631b2a7df0/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/42db806805ef2be64ee92803d3a784631b2a7df0/content/browser/renderer_host/navigation_request_browsertest.cc


### cr...@chromium.org (2023-05-12)

Thanks for the quick investigation!

I suspect the repro case gets into the "navigate from a [non-live] error page to an error page" case because of the modification to DispatchDidReceiveTitle, which would cause all renderer processes to be killed.  That's unrealistic in practice, since no untrustworthy code should be running in the error page process.  If that were the only way to repro the bug, it would lower the severity.

However, I suspect this is still exploitable because subframe error pages do not use the error page process.  That means you could commit an error page in a subframe of your own origin, then cause the renderer process to exit (which would likely be easier via OOM than a compromise), then attempt to load the error page in the subframe again.  This would be possible if the main frame is in a different origin, on a page like A(B1, B2), where B1 shows the error pages and B2 causes the OOM.

I took a quick look to see if there are other risky callsites for functions with "DO NOT ADD CODE after this" in NavigationRequest and didn't see any at first glance, but I only went one level deep.  There's a lot of code of this form in NavigationRequest, unfortunately.  Rakina, is there a issue filed for continuing the audit to make sure we avoid other bugs of this form?

### cr...@chromium.org (2023-05-12)

Should be fixed by r1143298, so we can see how it does on Canary before considering merges.

Marking FoundIn-113, but the bug goes back further than that, so feel free to adjust that label if needed.

### [Deleted User] (2023-05-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-13)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-13)

Requesting merge to stable M113 because latest trunk commit (1143298) appears to be after stable branch point (1121455).

Requesting merge to beta M114 because latest trunk commit (1143298) appears to be after beta branch point (1135570).

Merge review required: M113 is already shipping to stable.

Merge review required: M114 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-05-14)

Adjusting this to FoundIn-112 since this issue goes back farther than 112 and M112 is currently Extended Stable. 
Also, as this is a Critical severity issue, it will eventually need to be evaluated for M109 backport as M109 is the release channel for Enterprise extended support for Windows 2012 

### am...@chromium.org (2023-05-14)

Thank you for the quick response to this rakina@. 
In checking Canary since this fix was landed, not seeing any issues that would prevent backmerge. 
M114 merge approved, please merge this fix to branch 5735
M113 and M112 merges approved, please merge this fix to branches 5672 and 5616 respectively before 10am Pacific Monday, 15 May so this fix can be included in the M113/Stable and M112/Extended Stable RCs for the next respin being, scheduled to be released Tuesday, 16 May. 
 

### [Deleted User] (2023-05-14)

Requesting merge to stable M113 because latest trunk commit (1143298) appears to be after stable branch point (1121455).

Requesting merge to beta M114 because latest trunk commit (1143298) appears to be after beta branch point (1135570).

Merge review required: M113 is already shipping to stable.

Merge review required: M114 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [113, 114].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2023-05-15)

Based on https://crbug.com/chromium/1444360#c18 and offline chat with Amy the CL's are approved hence I am labeling them accordingly.

### gi...@appspot.gserviceaccount.com (2023-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6755626950491fac28d6631b19e16a5733435070

commit 6755626950491fac28d6631b19e16a5733435070
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Mon May 15 03:21:49 2023

[M114] Return after ReadyCommitNavigation call in CommitErrorPage if it deletes NavigationRequest

NavigationRequest::ReadyToCommitNavigation() can cause deletion of the
NavigationRequest, so callers should check for that possibility after
calling the function. A caller in CommitErrorPage is missing that
check, which this CL adds, along with a regression test.

(cherry picked from commit 42db806805ef2be64ee92803d3a784631b2a7df0)

Bug: 1444360
Change-Id: I3964da4909a6709b7730d25d6497b19c098f4f21
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4520493
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1143298}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4531446
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Rakina Zata Amni <rakina@chromium.org>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#607}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/6755626950491fac28d6631b19e16a5733435070/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/6755626950491fac28d6631b19e16a5733435070/content/browser/renderer_host/navigation_request_browsertest.cc


### ra...@chromium.org (2023-05-15)

Thanks creis@! Merges are in-flight, and I've filed a bug about the NavigationRequest UaF here: crbug.com/1445554 (thanks for the reminder!)

### gi...@appspot.gserviceaccount.com (2023-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/780c88666facea7123f724c8e8b4667108ddcb29

commit 780c88666facea7123f724c8e8b4667108ddcb29
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Mon May 15 15:16:21 2023

[M113] Return after ReadyCommitNavigation call in CommitErrorPage if it deletes NavigationRequest

NavigationRequest::ReadyToCommitNavigation() can cause deletion of the
NavigationRequest, so callers should check for that possibility after
calling the function. A caller in CommitErrorPage is missing that
check, which this CL adds, along with a regression test.

(cherry picked from commit 42db806805ef2be64ee92803d3a784631b2a7df0)

Bug: 1444360
Change-Id: I3964da4909a6709b7730d25d6497b19c098f4f21
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4520493
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1143298}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4531445
Auto-Submit: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/branch-heads/5672@{#1199}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/780c88666facea7123f724c8e8b4667108ddcb29/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/780c88666facea7123f724c8e8b4667108ddcb29/content/browser/renderer_host/navigation_request_browsertest.cc


### gi...@appspot.gserviceaccount.com (2023-05-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c82190c97f9dba375f4814d9fb0e725b7a4e9622

commit c82190c97f9dba375f4814d9fb0e725b7a4e9622
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Mon May 15 15:19:31 2023

[M112] Return after ReadyCommitNavigation call in CommitErrorPage if it deletes NavigationRequest

NavigationRequest::ReadyToCommitNavigation() can cause deletion of the
NavigationRequest, so callers should check for that possibility after
calling the function. A caller in CommitErrorPage is missing that
check, which this CL adds, along with a regression test.

(cherry picked from commit 42db806805ef2be64ee92803d3a784631b2a7df0)

Bug: 1444360
Change-Id: I3964da4909a6709b7730d25d6497b19c098f4f21
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4520493
Commit-Queue: Charlie Reis <creis@chromium.org>
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1143298}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4528897
Auto-Submit: Rakina Zata Amni <rakina@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#1426}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/c82190c97f9dba375f4814d9fb0e725b7a4e9622/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/c82190c97f9dba375f4814d9fb0e725b7a4e9622/content/browser/renderer_host/navigation_request_browsertest.cc


### am...@chromium.org (2023-05-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-16)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-05-16)

the well-meaning bot removed release label due to this issue not having a SI label; updating as SI-Extended and re-adding release label accordingly 

### pg...@google.com (2023-05-16)

[Empty comment from Monorail migration]

### hi...@gmail.com (2023-05-17)

credit info: 360VRI

### am...@google.com (2023-05-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-18)

Congratulations! The VRP Panel has decided to award you $30,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- excellent work! 

### am...@google.com (2023-05-19)

[Empty comment from Monorail migration]

### gm...@google.com (2023-05-25)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-26)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-26)

[Empty comment from Monorail migration]

### rz...@google.com (2023-05-26)

1. Just https://crrev.com/c/4567848
2. 112, 113, 114
3. Low, only a few type conflicts, and with code around the changes that wasn't present in 108
4. Yes

### gm...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### gm...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9964ff18eadab4a95c23a055adee862077b63590

commit 9964ff18eadab4a95c23a055adee862077b63590
Author: Rakina Zata Amni <rakina@chromium.org>
Date: Tue May 30 16:24:26 2023

[M108-LTS] Return after ReadyCommitNavigation call in CommitErrorPage if it deletes NavigationRequest

M108 merge issue:
  content/browser/renderer_host/navigation_request.cc:
    topics_eligible_ isn't present in M108

NavigationRequest::ReadyToCommitNavigation() can cause deletion of the
NavigationRequest, so callers should check for that possibility after
calling the function. A caller in CommitErrorPage is missing that
check, which this CL adds, along with a regression test.

(cherry picked from commit 42db806805ef2be64ee92803d3a784631b2a7df0)

Bug: 1444360
Change-Id: I3964da4909a6709b7730d25d6497b19c098f4f21
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4520493
Commit-Queue: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1143298}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4567848
Reviewed-by: Rakina Zata Amni <rakina@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1460}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/9964ff18eadab4a95c23a055adee862077b63590/content/browser/renderer_host/navigation_request.cc
[modify] https://crrev.com/9964ff18eadab4a95c23a055adee862077b63590/content/browser/renderer_host/navigation_request_browsertest.cc


### rz...@google.com (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1444360?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064476)*
