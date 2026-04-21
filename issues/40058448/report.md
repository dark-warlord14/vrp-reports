# Security: double-free in content::RenderFrameHostImpl::ResetNavigationRequests

| Field | Value |
|-------|-------|
| **Issue ID** | [40058448](https://issues.chromium.org/issues/40058448) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Core, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation, UI>Browser>TopChrome>TabStrip |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | yu...@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2022-01-10 |
| **Bounty** | $5,000.00 |

## Description

double-free in content::RenderFrameHostImpl::ResetNavigationRequests

**VULNERABILITY DETAILS**  

This crash found in my fuzz system and I am still investigating it. I will submit PoC or crash analysis as soon as possible.

Since it is found in dev version, please let me know if there has any more info about this (such as it is duplicated...)

**VERSION**  

Chrome Version: asan-win32-release\_x64-950368  

Operating System: windows 10 21H2

**REPRODUCTION CASE**  

Asan log attached and more info is analyzing.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser

**CREDIT INFORMATION**  

Reporter credit: Wei Yuan(@vo\_sec) of MoyunSec VLab

## Attachments

- [double-free.txt](attachments/double-free.txt) (text/plain, 20.1 KB)
- [double-free-956935.txt](attachments/double-free-956935.txt) (text/plain, 14.5 KB)

## Timeline

### [Deleted User] (2022-01-10)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-01-10)

Please provide a PoC when you can, as well as details of the Chrome build it reproduces on. Were you fuzzing with local or instrumented builds? Does it reproduce on the official Chrome stable?

### yu...@gmail.com (2022-01-11)

Re #2, this crash was found by fuzzing the offical build asan-win32-release_x64-950368 downloaded from storage.googleapis.com with just a extension.

The issue maybe introduced by https://chromium-review.googlesource.com/c/chromium/src/+/3254542.

A RenderProcessHostImpl::ProcessDied call add here cause a recursive RenderFrameHostImpl::ResetNavigationRequests call and ASAN report it as double-free.
https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_process_host_impl.cc;drc=83fd7137dcf236a57a447904c082db821ce98779;l=3926

According to the analysis of asan stack and source code, when a special Mojo call recived to close last tab and window, a callchain like this triggered:
navigation_requests_.clear();                                  <=  free NavigationRequest
content::RenderFrameHostImpl::ResetNavigationRequests
content::RenderFrameHostImpl::RenderProcessGone
content::SiteInstanceImpl::RenderProcessExited 
content::RenderProcessHostImpl::ProcessDied      <= this call added recently
content::RenderProcessHostImpl::Cleanup
content::SiteInstanceImpl::~SiteInstanceImpl
content::NavigationRequest::~NavigationRequest
navigation_requests_.clear();                                   <=  double-free report here
content::RenderFrameHostImpl::ResetNavigationRequests
content::FrameTree::Shutdown
content::WebContentsImpl::~WebContentsImpl
TabStripModel::SendDetachWebContentsNotifications
TabStripModel::CloseTabs
TabStripModel::CloseAllTabs
BrowserView::OnWindowCloseRequested
views::Widget::CloseWithReason
extensions::WindowsRemoveFunction::Run
ExtensionFunction::RunWithValidation
extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal
extensions::ExtensionFunctionDispatcher::Dispatch
extensions::ExtensionFrameHost::Request
extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder
extensions::mojom::LocalFrameHostStub >::AcceptWithResponder
mojo::InterfaceEndpointClient::HandleValidatedMessage
mojo::MessageDispatcher::Accept

### [Deleted User] (2022-01-11)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@gmail.com (2022-01-11)

[Comment Deleted]

### ct...@chromium.org (2022-01-13)

> Re #2, this crash was found by fuzzing the offical build asan-win32-release_x64-950368 downloaded from storage.googleapis.com with just a extension.

Could you upload the extension you used to trigger this crash and give reproduction steps? Thanks. It's difficult for us to act on this report without being able to reproduce it.

### yu...@gmail.com (2022-01-17)

RE #6, The extension is a fuzzer with lots of code and can not be minimized because the crash can't reproduce. So, it is useless for reproduce or fix.

This one discovered accidentally and still not reproduce in few days,  the competition conditions are a bit harsh. Maybe code owner could help triage it.

It is happened when extension call |chrome.windows.remove| to close a window, if a relative RenderProcessHost has only inactive render frames but still have navigation requests pending in |rfh->navigation_requests_|. The callchain in #3 could happen and trigger double-free.

### [Deleted User] (2022-01-17)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@google.com (2022-01-18)

sending to erikchen to take a look based on blame around the site of the double-free. please take a look at this report.

yuanvi.cn: it would be great to see a reproduction case.

Tentatively setting sev=high as this is a browser RCE with complex steps and FoundIn-97.

[Monorail components: UI>Browser>TopChrome>TabStrip]

### er...@chromium.org (2022-01-18)

I haven't looked at this code in years. I think you maybe wanted creis from https://chromium-review.googlesource.com/c/chromium/src/+/3254542 ?

### [Deleted User] (2022-01-18)

[Empty comment from Monorail migration]

### cr...@chromium.org (2022-01-18)

Thanks for the report!  My guess is that this might repro if one of the NavigationRequests in a tab being closed happens to share a process with a non-live RenderFrameHost (and nothing else).  That might cause the pending process to go away using the new leak cleanup logic, in a way that appears to cause a re-entrant call to ResetNavigationRequests.  I haven't been able to trigger it just yet, but I'll look again after my meetings to confirm it.

Also, I think the FoundIn-97 label might be wrong?  r940033 landed in 98.0.4697.0 and wasn't merged, IIUC.  ajgo@: Correct me if there's a reason to consider M97 affected.

[Monorail components: Internals>Core Internals>Sandbox>SiteIsolation UI>Browser>Navigation]

### cr...@chromium.org (2022-01-18)

[Empty comment from Monorail migration]

### cr...@chromium.org (2022-01-19)

This seems plausible, but I haven't been able to find steps to reproduce it in a test yet.

The stack in https://crbug.com/chromium/1285759#c3 suggests the following:

* We're closing a tab while the main frame RFH owns one or more NavigationRequests.  This means those NavigationRequests have reached OnResponseStarted (and have a response from the network) but we're still waiting for the renderer process to commit the navigation.  (Before OnResponseStarted, the NavigationRequest is owned by the FrameTreeNode rather than the RenderFrameHost.  After the commit, the NavigationRequest no longer exists.)

* We then get to the first ResetNavigationRequests call from FrameTree::Shutdown.

* We're deleting a SiteInstance as part of deleting one of the NavigationRequests.  This can't be the dest_site_instance_ because that's also referenced by the RenderFrameHost and wouldn't go away yet (thanks to the second scoped_refptr reference).  I'll guess that it's the starting_site_instance_, which suggests that a redirect or COOP navigation forced a SiteInstance swap.  Let's call the deleted one SiteInstance A, with the commit happening in a RenderFrameHost for SiteInstance B.

* When SiteInstance A is deleted, it removes itself as an observer from RenderProcessHost 1 and calls Cleanup.  There's at least one other non-live RFH and no live RFHs in RenderProcessHost 1, causing RPHI::Cleanup to call RPHI::ProcessDied, thanks to my process leak cleanup code from r940033.

* Some other SiteInstance (B or C) that is also sharing RenderProcessHost 1 listens to RenderProcessExited and calls RenderFrameHost::RenderProcessGone on its RFHs.  Suppose this is SiteInstance B notifying the main frame RFH which is being closed.  (If so, we somehow need the SiteInstance swap from A to B to reuse the same RenderProcessHost.  That's tricky, but maybe it's possible with COOP if we're over the process limit.)

* That RenderProcessGone call then re-entrantly calls ResetNavigationRequests.  I think the first NavigationRequest is gone from the navigation_requests_ list at that point, but there could be more than one in the list if a second NavigationRequest was also waiting to commit.  If we delete a second NavigationRequest here, then I think we'll try to double free it when the stack unwinds and we get back to the first ResetNavigationRequests call from FrameTree::Shutdown (since that iterator is stale at that point).

The catch here is that I *think* this would require the main frame RenderFrameHost for SiteInstance B to be considered live (since the navigation is waiting to commit), and thus the RPHI::ProcessDied call wouldn't happen from RPHI::Cleanup (which can't happen with live RFHs).  I can't think of any other way for the nested ResetNavigationRequests call to operate on the same RenderFrameHost, though, so maybe it's possible?  For example, maybe the renderer process crashed after OnResponseStarted but before closing the tab?  (Not sure if that would clear out the NavigationRequests on its own, though.)

I'll try to explore that possibility in my test, but any additional info about the fuzzer's repro case would be very helpful.  Thanks!

### yu...@gmail.com (2022-01-19)

Another same crash found in offical build version 'asan-win32-release_x64-956935', it looks like a bit difference. Hope it is helpful.

### [Deleted User] (2022-01-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2022-01-19)

https://crbug.com/chromium/1285759#c15: Thanks, though that looks pretty much the same as the original report from the WebContents destructor on, and still doesn't shed light on how we got into the state.  If you can share anything about the navigations that are in progress at the time of the crash (e.g., what URLs are in RenderFrameHostImpl::navigation_requests_ at the time of FrameTree::Shutdown), that would help.

Given the urgency here for M98 (assuming this is reachable based on the fuzzer's output), I've put together a speculative fix in https://chromium-review.googlesource.com/c/chromium/src/+/3401801 and I can look into a test separately.

### gi...@appspot.gserviceaccount.com (2022-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5791f62b21d2ded8e3e3fecd79e053f3d6614d2

commit f5791f62b21d2ded8e3e3fecd79e053f3d6614d2
Author: Charlie Reis <creis@chromium.org>
Date: Thu Jan 20 03:30:05 2022

Swap maps in ResetNavigationRequests.

Bug: 1285759
Change-Id: I6cacd311107570cec7fd678ec8c5e5265bf893be
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3401801
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Charles Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/main@{#961301}

[modify] https://crrev.com/f5791f62b21d2ded8e3e3fecd79e053f3d6614d2/content/browser/renderer_host/render_frame_host_impl.cc


### cr...@chromium.org (2022-01-20)

r961301 should prevent the double-free, I think, though I haven't been able to repro the bug myself.  I'll try to put a little more time into getting a test to work, and any input regarding https://crbug.com/chromium/1285759#c18 is still welcome.

If you're able to re-run your fuzzer to confirm that r961301 fixes it, that would also be appreciated.  Thanks!

### yu...@gmail.com (2022-01-20)

I will run my fuzzer on this reversion soon, but this crash was found accidentally (just twice) in my fuzzing system, so maybe I just can confirm it not reproduce in a period of time or report it if reproduced.

### cr...@chromium.org (2022-01-20)

srinivassista@ / govind@ / amyressler@: r961301 is a low-risk CL that should avoid the browser-process memory bug reported here, which was introduced in M98.  I'd like to get some Canary coverage for it (since it isn't in a Canary yet), but I wanted to check on the deadline for requesting a M98 merge for it.

For context, we haven't found a way to repro this (outside of some accidental hits in an external fuzzer), so we don't know if there are mitigating factors that would make it lower than High severity.  I'm guessing it's just a matter of closing a tab while the right network requests are in progress, though, so it's probably exploitable if you can get the timing right.

### [Deleted User] (2022-01-20)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-20)

Hi creis@, stable cut for M98 is next Tuesday, 25 January, so you have a few days to get some solid canary coverage for this fix. 

While the result of this issue is a double-free in the browser process, and is a high severity given the complex steps to reproduce, given that this is also flaky and not readily reproducible and also seems to require a small timing window to exploit, giving an attacker very limited control, it seem that this could be lowered to a Medium. I'd like other sheriffs to confirm my assessment before I can it. But given all these conditions at exist at present, I'm fairly certain this should potentially be reduced to medium severity. 

### [Deleted User] (2022-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-20)

Requesting merge to beta M98 because latest trunk commit (961301) appears to be after beta branch point (950365).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-21)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2022-01-21)

https://crbug.com/chromium/1285759#c24: Thanks!  Looks like r961301 is now in 99.0.4844.0, and the initial stability data from the first 11 hours looks good (i.e., I don't see related crash signatures):
https://crash.corp.google.com/browse?q=product_name%3D%27Chrome%27&compProp=product.Version&v1=99.0.4840.0&v2=99.0.4844.0
https://crash.corp.google.com/browse?q=product.version%3E%3D%2799.0.4844.0%27+AND+expanded_custom_data.ChromeCrashProto.channel%3D%27canary%27+AND+expanded_custom_data.ChromeCrashProto.ptype%3D%27browser%27

We still don't have a repro or a way to verify the fix, but r961301 has a very high chance of fixing it and is low risk.  I'm happy to wait until later today or early Monday to land the merge if you'd like, to have more bake time for the Canary.

Despite the lack of repro, I think it might make sense to keep this as High severity.  The difficulty in this one lies more in finding the right conditions to write the test or exploit, and not in running the exploit once you have it written.  At most there's a timing race you need to win, but I think repeat attempts would be possible.

https://crbug.com/chromium/1285759#c27:
1) It's a security fix for a browser process memory bug, which could allow sandbox escape.
2) r961301 (https://chromium-review.googlesource.com/c/chromium/src/+/3401801)
3) Yes, it has been on Canary for half a day so far
4) No, not a new feature
5) N/A
6) No verification possible without repro steps.


### am...@chromium.org (2022-01-21)

Thanks for all this! Yes, I conferred with the other sheriffs and also concur with leaving this at high severity. Since M98 stable cut is Tuesday and even though this is a low risk fix, let's revisit on Monday. The odds have not been in my favor this week, so I'm happy to err on the side of caution since we have a little buffer that allows a little extra Canary bake time. 

### cr...@chromium.org (2022-01-24)

https://crbug.com/chromium/1285759#c29: Thanks!  I've checked the crash links in https://crbug.com/chromium/1285759#c28 again, and it still looks safe to me.  (No new crash signatures related to this change, as far as I can tell.)  With the extra bake time over the weekend, it's probably safe to merge to M98.

As a side note, Nasko and I tried to work on a local repro a little more but still got stuck at the same catch from https://crbug.com/chromium/1285759#c14, where the RenderFrameHost needs to be considered live to have navigation_requests_ but non-live for the leak cleanup to apply.  We haven't found the steps needed to repro it, so I don't have a test.

### am...@chromium.org (2022-01-24)

Thanks for the update including about repro attempts and test. 
merge approved to M98, please merge to branch 4758 at your earliest convenience (and before 11am PST tomorrow/Tuesday, 25 January) -- thanks! 

### sr...@google.com (2022-01-24)

[Empty comment from Monorail migration]

### go...@chromium.org (2022-01-24)

Please merge your change to M98 branch 4758 ASAP so we can take it in for M98 Stable RC cut. RC cut tomorrow, Tuesday noon PT. Thank you. 

### gi...@appspot.gserviceaccount.com (2022-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ff85cf2cf2f1f8fb89abd60b5294d0ca0b9baf6a

commit ff85cf2cf2f1f8fb89abd60b5294d0ca0b9baf6a
Author: Charlie Reis <creis@chromium.org>
Date: Mon Jan 24 22:20:46 2022

[M98] Swap maps in ResetNavigationRequests.

(cherry picked from commit f5791f62b21d2ded8e3e3fecd79e053f3d6614d2)

Bug: 1285759
Change-Id: I6cacd311107570cec7fd678ec8c5e5265bf893be
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3401801
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Charles Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#961301}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3412898
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Charles Reis <creis@chromium.org>
Commit-Queue: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/4758@{#877}
Cr-Branched-From: 4a2cf4baf90326df19c3ee70ff987960d59a386e-refs/heads/main@{#950365}

[modify] https://crrev.com/ff85cf2cf2f1f8fb89abd60b5294d0ca0b9baf6a/content/browser/renderer_host/render_frame_host_impl.cc


### [Deleted User] (2022-01-24)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2022-01-24)

https://crbug.com/chromium/1285759#c35: There is no need for an M96 merge, because the bug was introduced in 98.0.4697.0.

### gm...@google.com (2022-01-26)

Thank you @creis. 

### am...@google.com (2022-01-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-28)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Thank you for your report and nice work! 

### yu...@gmail.com (2022-01-28)

Thanks for the award, this issue still not reproduce on r961301 in my fuzz system up to now. The double-free problem should be fixed.  I will improve report quality and see you in next submit.

### am...@google.com (2022-01-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1285759?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Core, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation, UI>Browser>TopChrome>TabStrip]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058448)*
