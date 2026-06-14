# Site Isolation: Attacker-controlled data URLs end up in wrong process after tab restore

| Field | Value |
|-------|-------|
| **Issue ID** | [40091919](https://issues.chromium.org/issues/40091919) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Sandbox>SiteIsolation |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | s....@gmail.com |
| **Assignee** | cr...@chromium.org |
| **Created** | 2018-07-12 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

When cross-site document redirects to Data URL inside iframe, it's still being isolated by Site Isolation. But when same page is loaded from local cache (I will investigate if there is more easy way to exploit this), Data URL iframe is now committed to same process instead of being cross processed.

**VERSION**  

Chrome Version: 67.0.3396.99 stable  

Operating System: Windows 10 RS4

**REPRODUCTION CASE**

1. Go to <https://shhnjk.azurewebsites.net/IsolateMe.html>
2. Observe that Data URL iframe redirected from <https://vuln.shhnjk.com> is in cross-process
3. Open new tab, type chrome://restart and hit enter
4. Observe that Data URL iframe now lives in the same process as <https://shhnjk.azurewebsites.net/IsolateMe.html>

## Timeline

### es...@chromium.org (2018-07-12)

Another one for you to triage please, Charlie.

[Monorail components: Internals>Sandbox>SiteIsolation]

### cr...@chromium.org (2018-07-13)

Thanks for the report!  We don't preserve SiteInstances across different Chrome sessions, so we don't remember that the data URL was in a different process after a full restart.  Apparently this affects even tab restore as well (where I wasn't sure if we keep SiteInstances or not), though not back/forward.

Other repro steps:
1) Visit http://csreis.github.io/tests/cross-site-iframe.html
2) Click "Go cross-site (simple page)"
3) Open DevTools, inspect the subframe, and enter this into the console:
location.href = "data:text/html,attacker content"
4) Verify there's still a subframe process for the data URL.
5) Open another tab and close the first tab, then use Ctrl+Shift+T to restore it.

The data URL will now be in the parent frame's process.

nick@ had a suspicion this would be possible with data URLs.  Doesn't happen for back/forward navigations, and I think the requirement of restore is a big mitigating factor that means the page has to be open and survive a restart or restored tab (requiring behavior from the user).  Still, it's something we should fix.

Tracking SiteInstances across restore is a super old problem we could try to take the time to fix (https://crbug.com/chromium/14987), but I think it might be more expedient to put data URLs in their own process if we don't know which SiteInstance created them.  That shouldn't break anything since they run in a unique origin.

Note that the process sharing behavior affects about:blank URLs as well, but those don't retain their content after a restore, so it shouldn't be a risk for attacks.

### cr...@chromium.org (2018-07-18)

Alex and I were chatting about this in the context of https://crbug.com/chromium/863623, and we realized one thing we'll need to be careful about-- if we don't use the parent's SiteInstance for a data URL during tab restore, then the default is to currently put it into a "data:" site URL, which will end up sharing a process with all other data URLs.  That wouldn't be good either.

The test for this would be a page like a(b,c), where b and c both navigate to data URLs.  After restore, we currently put both data URLs into a's process.  A simple fix that changes RenderFrameHostManager::CanSubframeSwapProcess to not return false when the source_instance is missing would cause us to put the data URLs in a different process from the main frame but the same process as each other.  A more correct fix would also change SiteInstanceImpl::GetSiteForURL to return something like the full data URL for the site URL, such that two data URLs will only share a process (after restore, or after a browser-initiated navigation) if they're identical to each other.

We'll probably do a similar change to the site URL for blob URLs, file URLs, etc (for unique origin cases).  I'll coordinate with Alex, since this will be related to the fix for https://crbug.com/chromium/863623.

### sh...@chromium.org (2018-07-25)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-07-25)

CL in progress:
https://chromium-review.googlesource.com/c/chromium/src/+/1150767

### cr...@chromium.org (2018-08-02)

Update: There's some test issues in the CL due to layout test problems with OOPIFs and some unexpected failures on Android, and I'm trying to work through them.

### bu...@chromium.org (2018-08-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca

commit 0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca
Author: Charlie Reis <creis@chromium.org>
Date: Mon Aug 06 22:46:01 2018

Use unique processes for data URLs on restore.

Data URLs are usually put into the process that created them, but this
info is not tracked after a tab restore.  Ensure that they do not end up
in the parent frame's process (or each other's process), in case they
are malicious.

BUG=863069

Change-Id: Ib391f90c7bdf28a0a9c057c5cc7918c10aed968b
Reviewed-on: https://chromium-review.googlesource.com/1150767
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#581023}
[modify] https://crrev.com/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca/chrome/browser/renderer_host/render_process_host_chrome_browsertest.cc
[modify] https://crrev.com/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca/content/browser/frame_host/render_frame_host_manager.h
[modify] https://crrev.com/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca/content/browser/site_instance_impl.cc
[modify] https://crrev.com/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca/content/browser/site_instance_impl_unittest.cc
[modify] https://crrev.com/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca/content/browser/site_per_process_browsertest.cc
[add] https://crrev.com/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca/third_party/WebKit/LayoutTests/fast/frames/resources/frame-navigation-child-1.html
[add] https://crrev.com/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca/third_party/WebKit/LayoutTests/fast/frames/resources/frame-navigation-child-2.html
[modify] https://crrev.com/0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca/third_party/WebKit/LayoutTests/fast/frames/resources/frame-navigation-child.html


### cr...@chromium.org (2018-08-06)

This should be resolved in r581023, which causes restored data URLs to go into processes locked to the whole data URL, instead of "data:".  We still keep navigations to data URLs in the process of the creator, to keep process count low (though we're discussing that in https://crbug.com/chromium/863073).

We should let this bake for a few days and consider whether it's safe to merge to M69.

### sh...@chromium.org (2018-08-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-08-08)

[Empty comment from Monorail migration]

### cr...@chromium.org (2018-08-08)

r581023 landed in 70.0.3515.0, and I don't see any crashes as a result.  The initial UMA data (admittedly only from a few days) doesn't seem to show a large increase in the process count, which would only happen if users had a lot of data URL subframes and restarted their browser.

Seems like this should be a safe merge to M69.  (It depends on r576318 from https://crbug.com/chromium/863623, but that's already in M69.)  The merge may be worthwhile to avoid cases where an attacker can navigate to a data URL in a subframe of a victim site, then end up in the victim's process after a restart.  The merge is clean, and I'm checking out a branch to verify it locally.

### sh...@chromium.org (2018-08-08)

This bug requires manual review: M69 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-08-08)

Approving merge to M69 branch 3497 based on https://crbug.com/chromium/863069#c11. Please merge now. Thank you.

### bu...@chromium.org (2018-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d8474edf8dc7e6f479937bb67fd191366493315b

commit d8474edf8dc7e6f479937bb67fd191366493315b
Author: Charlie Reis <creis@chromium.org>
Date: Wed Aug 08 21:45:12 2018

[Merge to M69] Use unique processes for data URLs on restore.

Data URLs are usually put into the process that created them, but this
info is not tracked after a tab restore.  Ensure that they do not end up
in the parent frame's process (or each other's process), in case they
are malicious.

BUG=863069

Change-Id: Ib391f90c7bdf28a0a9c057c5cc7918c10aed968b
Reviewed-on: https://chromium-review.googlesource.com/1150767
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Lei Zhang <thestig@chromium.org>
Commit-Queue: Charlie Reis <creis@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#581023}(cherry picked from commit 0bb3f5c715eb66bb5c1fb05fd81d902ca57f33ca)
Reviewed-on: https://chromium-review.googlesource.com/1167771
Reviewed-by: Charlie Reis <creis@chromium.org>
Cr-Commit-Position: refs/branch-heads/3497@{#511}
Cr-Branched-From: 271eaf50594eb818c9295dc78d364aea18c82ea8-refs/heads/master@{#576753}
[modify] https://crrev.com/d8474edf8dc7e6f479937bb67fd191366493315b/chrome/browser/renderer_host/render_process_host_chrome_browsertest.cc
[modify] https://crrev.com/d8474edf8dc7e6f479937bb67fd191366493315b/content/browser/frame_host/render_frame_host_manager.cc
[modify] https://crrev.com/d8474edf8dc7e6f479937bb67fd191366493315b/content/browser/frame_host/render_frame_host_manager.h
[modify] https://crrev.com/d8474edf8dc7e6f479937bb67fd191366493315b/content/browser/site_instance_impl.cc
[modify] https://crrev.com/d8474edf8dc7e6f479937bb67fd191366493315b/content/browser/site_instance_impl_unittest.cc
[modify] https://crrev.com/d8474edf8dc7e6f479937bb67fd191366493315b/content/browser/site_per_process_browsertest.cc
[add] https://crrev.com/d8474edf8dc7e6f479937bb67fd191366493315b/third_party/WebKit/LayoutTests/fast/frames/resources/frame-navigation-child-1.html
[add] https://crrev.com/d8474edf8dc7e6f479937bb67fd191366493315b/third_party/WebKit/LayoutTests/fast/frames/resources/frame-navigation-child-2.html
[modify] https://crrev.com/d8474edf8dc7e6f479937bb67fd191366493315b/third_party/WebKit/LayoutTests/fast/frames/resources/frame-navigation-child.html


### cr...@chromium.org (2018-08-08)

For the record, I was able to verify the fix in a local M69 build as well, using the steps in https://crbug.com/chromium/863069#c2 and running the new tests.

### go...@chromium.org (2018-08-08)

Thank you creis@.

### aw...@chromium.org (2018-08-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-08-16)

Hi s.h.h.n.j.k@ - thanks taking a look at Site Isolation! Though the need to restore is a significant mitigation, this qualifies for the Chrome New Feature Special Rewards, so the VRP panel decided to award $3,000. Cheers!

### s....@gmail.com (2018-08-16)

Thanks!

### aw...@chromium.org (2018-08-16)

[Empty comment from Monorail migration]

### aw...@google.com (2018-08-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-09-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-11-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### Ju...@microsoft.com (2019-08-20)

This bug is linked in Severity Guidelines as High severity example. Changing the severity to avoid confusions in the future. 
https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/863069?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091919)*
