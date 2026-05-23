# Security: UAF after use clicks help link in accessibility labels dialog

| Field | Value |
|-------|-------|
| **Issue ID** | [40055975](https://issues.chromium.org/issues/40055975) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | UI>Accessibility |
| **Platforms** | Linux, Windows |
| **Reporter** | de...@gmail.com |
| **Assignee** | ka...@chromium.org |
| **Created** | 2021-05-23 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

The accessibility labels dialog includes a help link in the bottom left. That link is opened via the WebContents used to show the dialog. If that WebContents has been destroyed (e.g. because the tab has been closed) and the user clicks the help link, a UAF will occur in the browser process.

Overall, this issue is very similar to <https://crbug.com/chromium/1212498>.

**VERSION**  

Chrome Version: Tested on 93.0.4520.0 (latest asan build)  

Operating System: Windows 10, version 20H2

**REPRODUCTION CASE**

1. Navigate to chrome://accessibility/ and enable the "Web accessibility" and "Screen reader support" modes.
2. Install the attached extension.
3. Once installed, the extension will open page.html in a new tab.
4. Right-click anywhere on the page, then select one of the options under the "Get image descriptions from Google" submenu.
5. page.html will wait for the contextmenu event, followed by a blur event (which will be triggered when the accessibility labels dialog is opened). Once it detects those events, it will send a message to the background page requesting it to close the tab.
6. Once the tab has been closed, click the help link shown in the dialog. That will result in a UAF in the browser process. You can verify that by going through these steps in an asan build.

**CREDIT INFORMATION**  

Reporter credit: David Erceg

## Attachments

- [asan_output_885837.txt](attachments/asan_output_885837.txt) (text/plain, 17.7 KB)
- [background.js](attachments/background.js) (text/plain, 228 B)
- [manifest.json](attachments/manifest.json) (text/plain, 169 B)
- [page.html](attachments/page.html) (text/plain, 98 B)
- [page.js](attachments/page.js) (text/plain, 710 B)
- [asan_output_779982.txt](attachments/asan_output_779982.txt) (text/plain, 17.3 KB)

## Timeline

### [Deleted User] (2021-05-23)

[Empty comment from Monorail migration]

### de...@gmail.com (2021-05-23)

The AccessibilityLabelsBubbleModel class holds a pointer to the WebContents that was used to host the context menu:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.h;l=41;drc=dec9912407fc5946125799ec62b996a04d08c4f0

When the help page link is clicked, the stored WebContents will be used to open the help page:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.cc;l=99;drc=dec9912407fc5946125799ec62b996a04d08c4f0

If the WebContents has been destroyed since the menu was shown, that will result in a UAF.

The accessibility labels dialog can also be invoked via chrome://settings/accessibility:

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/settings/accessibility_main_handler.cc;l=71;drc=d6a9b7daec08caaa914942f6be2c864e54904d70

So this issue is present there as well.

### va...@chromium.org (2021-05-25)

Unable to repro this on 90.0.4430.0 (Chromium)

### va...@chromium.org (2021-05-25)

[Empty comment from Monorail migration]

[Monorail components: UI>Accessibility]

### va...@chromium.org (2021-05-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-25)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2021-05-25)

Thanks. I think we can fix this by using BrowserList::GetInstance()->GetLastActive() to open the URL instead of a saved WebContents? I'll send that out for review.

### va...@chromium.org (2021-05-25)

Unable to reproduce this on 91.0.4472.0 either.

### va...@chromium.org (2021-05-25)

Unable to reproduce this on 92.0.4512.4.

katie@ -- are you able to reproduce this on ToT or elsewhere?

### ka...@chromium.org (2021-05-25)

I didn't try with an ASAN build, but I was able to follow the steps outlined to get the tab to close behind the dialog. It seems like something worthwhile to tidy up even if it's not reproducing the ASAN error? But I can also try with ASAN build if that's helpful.

Here's a change to fix it: https://chromium-review.googlesource.com/c/chromium/src/+/2917795

### ka...@chromium.org (2021-05-25)

Reproduced. Tried with ASAN build from this morning's tip-of-tree and got a crash from a use-after-free with the webcontents. With my fix, no ASAN build crash and same user facing behavior.

### de...@gmail.com (2021-05-25)

For what it's worth, this reproduces for me on the current version of each release channel (stable, beta, dev and canary). Also, it doesn't look like there have been any relevant changes to the AccessibilityLabelsBubbleModel recently:

https://chromium.googlesource.com/chromium/src/+log/main/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.cc

So it appears this issue may have been around for some time. Testing on an older asan build (85.0.4177.0, from about a year ago) also shows the same use-after-free (I've attached the asan log for that build here).

vakh@ Does the tab the extension creates close after you select one of the options under the accessibility menu? The extension will only close the tab if the time between opening the context menu and showing the dialog is less than 10 seconds.

### av...@chromium.org (2021-05-25)

Re https://crbug.com/chromium/1212500#c7, does it matter that BrowserList::GetInstance()->GetLastActive() might return a different profile than the one used to pull up the dialog? I’m working on related https://crbug.com/chromium/1212498 and I think I might have to just close the dialog if the page closes out from underneath it.

### ka...@chromium.org (2021-05-25)

Per lazyboy@'s comment in my change, I'm going to try using ScopedTabbedBrowserDisplayer to get the browser to use to open the URL, via chrome::ScopedTabbedBrowserDisplayer(profile_).browser(); I think this should fix the concern with the different profile, @avi?

### av...@chromium.org (2021-05-25)

Are we sure the profile will still be valid, too? This might have been the last window that had the profile open, and I know there are efforts to close out profiles when they’re done being used.

Given that both of our bugs involve subclasses of ConfirmBubbleModel, maybe we can add something to that superclass to watch the WebContents that it’s on, and close itself if the WebContents goes away.

### av...@chromium.org (2021-05-25)

Hmmm... ok, ConfirmBubbleModel is a UI thing, so it doesn’t know about that at all. ConfirmBubbleViews does indeed go away if the owning Browser window goes away, so my scenario can’t happen. Lemme take a look at your CL; I might follow suit.

### ka...@chromium.org (2021-05-25)

Closing ConfirmBubbleModel after the WebContents goes away SGTM.

I can't see crbug.com/1212498.

### ka...@chromium.org (2021-05-25)

Offline, @avi and I couldn't find an easy way to close ConfirmBubbleModel because it has no insight into what Widget / Dialog it belongs to. Therefore we are proceeding with my change and will probably apply the same fix to crbug.com/1212498 pending review.

### va...@chromium.org (2021-05-26)

I was able to reproduce this on Stable so marking it as such.

### va...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### va...@chromium.org (2021-05-26)

go/kroma for all crashes

### [Deleted User] (2021-05-26)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/427728383657e6ccb06dbfcce0c5118bb557c0af

commit 427728383657e6ccb06dbfcce0c5118bb557c0af
Author: Katie Dektar <katie@chromium.org>
Date: Wed May 26 19:47:15 2021

Check saved web contents before using to open new tab.

This means if the web contents were invalidated or missing, we can
still open the help page for the dialog about showing image
descriptions for unlabeled images, but without using invalid memory.

Also removes outdated TODO and adds a test for
AccessibilityLabelsBubbleModel.

Bug: 1212500
Change-Id: I17f0fa6c8a387ff3342c1d95deae5ee991583f5c
AX-Relnotes: N/A
Test: Dialog still opens help menu, even after closing the webcontents that launched the dialog, and new browsertests.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2917795
Commit-Queue: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#886863}

[modify] https://crrev.com/427728383657e6ccb06dbfcce0c5118bb557c0af/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.cc
[modify] https://crrev.com/427728383657e6ccb06dbfcce0c5118bb557c0af/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.h
[add] https://crrev.com/427728383657e6ccb06dbfcce0c5118bb557c0af/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model_browsertest.cc
[modify] https://crrev.com/427728383657e6ccb06dbfcce0c5118bb557c0af/chrome/test/BUILD.gn


### ka...@chromium.org (2021-05-26)

[Empty comment from Monorail migration]

### ka...@chromium.org (2021-05-26)

Do we want to try to merge to M92?

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-27)

Requesting merge to stable M91 because latest trunk commit (886863) appears to be after stable branch point (870763).

Requesting merge to beta M91 because latest trunk commit (886863) appears to be after beta branch point (870763).

Requesting merge to future beta M92 because latest trunk commit (886863) appears to be after future beta branch point (56).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-27)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ka...@chromium.org (2021-05-27)

For M91 merge request:
1. I'm not sure, since this has already gone to stable cut AFAIK. Maybe the security team can chime in here? + pbommana@ also?
  * The change has fully automated unit test coverage
  * The change has not been in Canary 24 hours yet
  * I am confident that this is a safe merge and it's low complexity
2. https://chromium-review.googlesource.com/c/chromium/src/+/2917795
3. Yes
4. Yes, M+1 (M92)
5. Security fix
6. No
7. N/A

### ad...@google.com (2021-05-27)

Approving merge to M92, branch 4515. We'll handle M91 approvals at a later stage.

### gi...@appspot.gserviceaccount.com (2021-05-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2d3f7840d4e01d00b354187834595fdc442fcac9

commit 2d3f7840d4e01d00b354187834595fdc442fcac9
Author: Katie Dektar <katie@chromium.org>
Date: Thu May 27 21:59:00 2021

[Merge to M92] Check saved web contents before using to open new tab.

This means if the web contents were invalidated or missing, we can
still open the help page for the dialog about showing image
descriptions for unlabeled images, but without using invalid memory.

Also removes outdated TODO and adds a test for
AccessibilityLabelsBubbleModel.

(cherry picked from commit 427728383657e6ccb06dbfcce0c5118bb557c0af)

Bug: 1212500
Change-Id: I17f0fa6c8a387ff3342c1d95deae5ee991583f5c
AX-Relnotes: N/A
Test: Dialog still opens help menu, even after closing the webcontents that launched the dialog, and new browsertests.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2917795
Commit-Queue: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#886863}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2923115
Commit-Queue: Avi Drissman <avi@chromium.org>
Auto-Submit: Katie Dektar <katie@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#132}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/2d3f7840d4e01d00b354187834595fdc442fcac9/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.cc
[modify] https://crrev.com/2d3f7840d4e01d00b354187834595fdc442fcac9/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.h
[add] https://crrev.com/2d3f7840d4e01d00b354187834595fdc442fcac9/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model_browsertest.cc
[modify] https://crrev.com/2d3f7840d4e01d00b354187834595fdc442fcac9/chrome/test/BUILD.gn


### ad...@google.com (2021-06-03)

Approving merge to M91. Please merge to branch 4472.

### pb...@google.com (2021-06-03)

Your change has been approved for M91. Please go ahead and merge the CL to M91 branch : 4472 (refs/branch-heads/4472) manually asap.

### gi...@appspot.gserviceaccount.com (2021-06-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ac8ca2ab03c64ac1bb06860d9a4d649c043680ad

commit ac8ca2ab03c64ac1bb06860d9a4d649c043680ad
Author: Katie Dektar <katie@chromium.org>
Date: Thu Jun 03 23:25:28 2021

[Merge to M91] Check saved web contents before using to open new tab.

This means if the web contents were invalidated or missing, we can
still open the help page for the dialog about showing image
descriptions for unlabeled images, but without using invalid memory.

Also removes outdated TODO and adds a test for
AccessibilityLabelsBubbleModel.

(cherry picked from commit 427728383657e6ccb06dbfcce0c5118bb557c0af)

Bug: 1212500
Change-Id: I17f0fa6c8a387ff3342c1d95deae5ee991583f5c
AX-Relnotes: N/A
Test: Dialog still opens help menu, even after closing the webcontents that launched the dialog, and new browsertests.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2917795
Commit-Queue: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#886863}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2936918
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1421}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/ac8ca2ab03c64ac1bb06860d9a4d649c043680ad/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.cc
[modify] https://crrev.com/ac8ca2ab03c64ac1bb06860d9a4d649c043680ad/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.h
[add] https://crrev.com/ac8ca2ab03c64ac1bb06860d9a4d649c043680ad/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model_browsertest.cc
[modify] https://crrev.com/ac8ca2ab03c64ac1bb06860d9a4d649c043680ad/chrome/test/BUILD.gn


### am...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### vs...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2835c871c02585bba204806b7d5fbe2003d0515e

commit 2835c871c02585bba204806b7d5fbe2003d0515e
Author: Katie Dektar <katie@chromium.org>
Date: Thu Jun 10 07:43:04 2021

[M86-LTS] Check saved web contents before using to open new tab.

This means if the web contents were invalidated or missing, we can
still open the help page for the dialog about showing image
descriptions for unlabeled images, but without using invalid memory.

Also removes outdated TODO and adds a test for
AccessibilityLabelsBubbleModel.

(cherry picked from commit 427728383657e6ccb06dbfcce0c5118bb557c0af)

(cherry picked from commit ac8ca2ab03c64ac1bb06860d9a4d649c043680ad)

Bug: 1212500
Change-Id: I17f0fa6c8a387ff3342c1d95deae5ee991583f5c
AX-Relnotes: N/A
Test: Dialog still opens help menu, even after closing the webcontents that launched the dialog, and new browsertests.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2917795
Commit-Queue: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#886863}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2936918
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1421}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944945
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1666}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/2835c871c02585bba204806b7d5fbe2003d0515e/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.cc
[modify] https://crrev.com/2835c871c02585bba204806b7d5fbe2003d0515e/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.h
[add] https://crrev.com/2835c871c02585bba204806b7d5fbe2003d0515e/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model_browsertest.cc
[modify] https://crrev.com/2835c871c02585bba204806b7d5fbe2003d0515e/chrome/test/BUILD.gn


### gi...@appspot.gserviceaccount.com (2021-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cc4e89eb5a743f24cdc2e4d4b667924ee8323402

commit cc4e89eb5a743f24cdc2e4d4b667924ee8323402
Author: Katie Dektar <katie@chromium.org>
Date: Thu Jun 10 07:45:07 2021

[M90-LTS] Check saved web contents before using to open new tab.

This means if the web contents were invalidated or missing, we can
still open the help page for the dialog about showing image
descriptions for unlabeled images, but without using invalid memory.

Also removes outdated TODO and adds a test for
AccessibilityLabelsBubbleModel.

(cherry picked from commit 427728383657e6ccb06dbfcce0c5118bb557c0af)

(cherry picked from commit ac8ca2ab03c64ac1bb06860d9a4d649c043680ad)

Bug: 1212500
Change-Id: I17f0fa6c8a387ff3342c1d95deae5ee991583f5c
AX-Relnotes: N/A
Test: Dialog still opens help menu, even after closing the webcontents that launched the dialog, and new browsertests.
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2917795
Commit-Queue: Katie Dektar <katie@chromium.org>
Reviewed-by: Istiaque Ahmed <lazyboy@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#886863}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2936918
Reviewed-by: Avi Drissman <avi@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1421}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2947508
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1516}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/cc4e89eb5a743f24cdc2e4d4b667924ee8323402/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.cc
[modify] https://crrev.com/cc4e89eb5a743f24cdc2e4d4b667924ee8323402/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model.h
[add] https://crrev.com/cc4e89eb5a743f24cdc2e4d4b667924ee8323402/chrome/browser/renderer_context_menu/accessibility_labels_bubble_model_browsertest.cc
[modify] https://crrev.com/cc4e89eb5a743f24cdc2e4d4b667924ee8323402/chrome/test/BUILD.gn


### vs...@google.com (2021-06-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

And another one! The VRP Panel had decided to award you $10,000 for this report. Nice work, David. 

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cs...@google.com (2021-10-08)

No crashes have been reported and the code is presumed fixed.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1212500?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055975)*
