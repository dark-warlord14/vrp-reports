# heap-use-after-free in PriceTrackingEmailDialogCoordinator::Show

| Field | Value |
|-------|-------|
| **Issue ID** | [329965696](https://issues.chromium.org/issues/329965696) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Shopping>PriceTracking |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | un...@gmail.com |
| **Assignee** | md...@chromium.org |
| **Created** | 2024-03-17 |
| **Bounty** | $3,000.00 |

## Description

Chrome Version: 124.0.6363.0 (Developer Build)
OS: Win10

Steps to reproduce the problem: 
(1) apply repro.patch and compile chrome in asan version, download the extension file attached. 
(2) run chrome.exe --load-extension=path_to_extension 
(3) navigate to an website that can trigger the price_tracking service.
 eg: https://issues.chromium.org/issues?q=type:vulnerability%20-status:obsolete 
(4) click the icon in the navigation bar to add this website as a bookmark. 
(5) crash occurs.

Problem Description: In CreatePriceTrackingEmailCallback, it binds a callback with raw pointer of web_contents [1]:

base::OnceCallback<void()> CreatePriceTrackingEmailCallback(
    Profile* profile,
    views::View* anchor_view,
    content::WebContents* web_contents,
    const bookmarks::BookmarkNode* bookmark) {
......
  base::OnceCallback<void()> show_dialog_callback = base::BindOnce(
      [](content::WebContents* web_contents, Profile* profile,
         views::View* anchor) {
        if (!web_contents || !profile || !anchor) {
          return;
        }
        PriceTrackingEmailDialogCoordinator(anchor).Show(web_contents, profile,
                                                         base::DoNothing());
      },
      // TODO(crbug.com/1380714): Remove `UnsafeDanglingUntriaged`
      base::UnsafeDanglingUntriaged(web_contents), profile, anchor_view);           // [1]

  return base::BindOnce(
      [](Profile* profile, const bookmarks::BookmarkNode* node,
         base::OnceCallback<void()> show_dialog) {
        commerce::IsBookmarkPriceTracked(
            commerce::ShoppingServiceFactory::GetForBrowserContext(profile),
            BookmarkModelFactory::GetForBrowserContext(profile), node,
            base::BindOnce(
                [](base::OnceCallback<void()> show_dialog, bool is_tracked) {
                  if (is_tracked) {
                    std::move(show_dialog).Run();                                             // [2]                                  
                  }
                },
                std::move(show_dialog)));
      },
      profile, bookmark, std::move(show_dialog_callback));
}

And the callback will be posted to an task and finally runs in [2]. Before the callback runs, we can free the web_contents by close the tab with extension.

The repro.patch file is just to make it easier for us to reproduce this issue.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/bookmark_bubble_view.cc;l=151
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/bookmarks/bookmark_bubble_view.cc;l=162

## Attachments

- [repro.patch](attachments/repro.patch) (text/x-diff, 1.3 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 13.8 KB)
- [background.js](attachments/background.js) (text/javascript, 308 B)
- [manifest.json](attachments/manifest.json) (application/json, 313 B)

## Timeline

### me...@chromium.org (2024-03-18)

Thanks for the report.

arthursonzogni: Could you please take a look?

### me...@chromium.org (2024-03-18)

Ah, sorry, I went by the owner of bug 1380714. 

mdjones: Could you PTAL instead? 

### me...@chromium.org (2024-03-18)

Assigning high severity since this requires an extension to time the closing of the tab.

### me...@chromium.org (2024-03-19)

This code has been around for a long time, assuming it impacts M122.

### ap...@google.com (2024-03-19)

Project: chromium/src
Branch: main

commit 0764f1e9bee0df31a7dc4f3d8cbe3c574994b191
Author: Matt Jones <mdjones@chromium.org>
Date:   Tue Mar 19 13:29:11 2024

    Fix UAF related to price tracking in bookmark save flow
    
    This patch updates the WebContents pointer passed to the callback that
    creates the price tracking email dialog to use a weak pointer. While
    dialogs are closed as a result of the WebContents being destroyed, the
    callback still references the raw pointer prior to creating the new
    dialog. If the user manages to close the tab (manually or by extension)
    in this short window, a UAF results.
    
    Bug: b:329965696
    Change-Id: Ic78adecf1e7af19992326b843186fea21531b3fa
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5378438
    Reviewed-by: Scott Violet <sky@chromium.org>
    Commit-Queue: Matthew Jones <mdjones@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1274868}

M       chrome/browser/ui/views/bookmarks/bookmark_bubble_view.cc

https://chromium-review.googlesource.com/5378438


### pe...@google.com (2024-03-19)

Setting milestone because of s0/s1 severity.

### aj...@google.com (2024-03-19)

Can this be marked as Fixed?

### md...@chromium.org (2024-03-19)

Yes, I'm not sure if this requires merge though - it's been around for a few milestones.

### pe...@google.com (2024-03-20)

Requesting merge to extended stable (M122) because latest trunk commit (1274868) appears to be after extended stable branch point (1250580).
Requesting merge to stable (M123) because latest trunk commit (1274868) appears to be after stable branch point (1262506).
Requesting merge to dev (M124) because latest trunk commit (1274868) appears to be after dev branch point (1274542).
Merge review required: M122 is already shipping to stable.


Merge review required: M123 is already shipping to stable.


Merge approved: your change passed merge requirements and is auto-approved for M124. Please go ahead and merge the CL to branch 6367 (refs/branch-heads/6367) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [122, 123, 124].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


### ap...@google.com (2024-03-20)

Project: chromium/src
Branch: refs/branch-heads/6367

commit 50cba44fa54b9c026de88a81b9f04882243d3dd9
Author: Matt Jones <mdjones@chromium.org>
Date:   Wed Mar 20 17:47:10 2024

    [M124] Fix UAF related to price tracking in bookmark save flow
    
    This patch updates the WebContents pointer passed to the callback that
    creates the price tracking email dialog to use a weak pointer. While
    dialogs are closed as a result of the WebContents being destroyed, the
    callback still references the raw pointer prior to creating the new
    dialog. If the user manages to close the tab (manually or by extension)
    in this short window, a UAF results.
    
    (cherry picked from commit 0764f1e9bee0df31a7dc4f3d8cbe3c574994b191)
    
    Bug: b:329965696
    Change-Id: Ic78adecf1e7af19992326b843186fea21531b3fa
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5378438
    Reviewed-by: Scott Violet <sky@chromium.org>
    Commit-Queue: Matthew Jones <mdjones@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1274868}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5381778
    Commit-Queue: Scott Violet <sky@chromium.org>
    Auto-Submit: Matthew Jones <mdjones@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6367@{#39}
    Cr-Branched-From: d158c6dc6e3604e6f899041972edf26087a49740-refs/heads/main@{#1274542}

M       chrome/browser/ui/views/bookmarks/bookmark_bubble_view.cc

https://chromium-review.googlesource.com/5381778


### un...@gmail.com (2024-03-26)

Hi, can I get bug bounty for this bug report? 

### am...@chromium.org (2024-03-26)

Now that this issue has been closed as fixed, it will be reviewed for a potential VRP reward at an upcoming VRP Panel session and has been labeled as such (see reward-topanel tag in c#10).

### am...@google.com (2024-03-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-03-27)

Congratuations! The Chrome VRP Panel has decided to award you $3,000 for this report of moderately mitigated memory corruption, mitigated by precondition to install a malicious extension, race condition, and user interaction. A member of the Google p2p-vrp finance team will reach out to you soon to initiate the payment process. In the meantime, please let us know what name or handle/tag you would like us to use in acknowledging you for this finding.

Thank you for your efforts and reporting this issue to us!

### am...@chromium.org (2024-03-27)

Merges approved for <https://crrev.com/c/5378438>, please merge this fix to M123 Stable (branch 6312) and M122 Extended (branch 6261) by EOD tomorrow, 28 March, so this fix can be included in the next security updates

### un...@gmail.com (2024-03-28)

Thank you very much. Just use undoingfish is fine.

### pe...@google.com (2024-04-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-04-01)

Project: chromium/src
Branch: refs/branch-heads/6312

commit 03fbddf498224f2bcca36d06c44df0d5f625067e
Author: Matt Jones <mdjones@chromium.org>
Date:   Mon Apr 01 17:10:26 2024

    [M123] Fix UAF related to price tracking in bookmark save flow
    
    This patch updates the WebContents pointer passed to the callback that
    creates the price tracking email dialog to use a weak pointer. While
    dialogs are closed as a result of the WebContents being destroyed, the
    callback still references the raw pointer prior to creating the new
    dialog. If the user manages to close the tab (manually or by extension)
    in this short window, a UAF results.
    
    (cherry picked from commit 0764f1e9bee0df31a7dc4f3d8cbe3c574994b191)
    
    Bug: b:329965696
    Change-Id: Ic78adecf1e7af19992326b843186fea21531b3fa
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5378438
    Reviewed-by: Scott Violet <sky@chromium.org>
    Commit-Queue: Matthew Jones <mdjones@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1274868}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5409909
    Cr-Commit-Position: refs/branch-heads/6312@{#754}
    Cr-Branched-From: 6711dcdae48edaf98cbc6964f90fac85b7d9986e-refs/heads/main@{#1262506}

M       chrome/browser/ui/views/bookmarks/bookmark_bubble_view.cc

https://chromium-review.googlesource.com/5409909


### sr...@google.com (2024-04-01)

Merges completed for m123 , so updating labels

### ap...@google.com (2024-04-01)

Project: chromium/src
Branch: refs/branch-heads/6261

commit f1a45d7ded05d64ca8136cc142ddc0c271b1dd43
Author: Matt Jones <mdjones@chromium.org>
Date:   Mon Apr 01 17:15:10 2024

    [M122] Fix UAF related to price tracking in bookmark save flow
    
    This patch updates the WebContents pointer passed to the callback that
    creates the price tracking email dialog to use a weak pointer. While
    dialogs are closed as a result of the WebContents being destroyed, the
    callback still references the raw pointer prior to creating the new
    dialog. If the user manages to close the tab (manually or by extension)
    in this short window, a UAF results.
    
    (cherry picked from commit 0764f1e9bee0df31a7dc4f3d8cbe3c574994b191)
    
    Bug: b:329965696
    Change-Id: Ic78adecf1e7af19992326b843186fea21531b3fa
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5378438
    Reviewed-by: Scott Violet <sky@chromium.org>
    Commit-Queue: Matthew Jones <mdjones@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1274868}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5410351
    Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
    Cr-Commit-Position: refs/branch-heads/6261@{#1153}
    Cr-Branched-From: 9755d9d81e4a8cb5b4f76b23b761457479dbb06b-refs/heads/main@{#1250580}

M       chrome/browser/ui/views/bookmarks/bookmark_bubble_view.cc

https://chromium-review.googlesource.com/5410351


### pe...@google.com (2024-06-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/329965696)*
