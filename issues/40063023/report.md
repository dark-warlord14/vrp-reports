# Security: Document PIP origin spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [40063023](https://issues.chromium.org/issues/40063023) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture, UI>Browser>Navigation |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-02-11 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Repeatedly opening a Document Picture-in-Picture window (PIP2) while navigating the opener page can result in the PIP window showing wrong security origin UI.

A similar issue regarding iframes [0](https://chromium-review.googlesource.com/c/chromium/src/+/4112814), "main frame origin is displayed in pip window when it is opened from third-party iframe", has been fixed by making sure "the pip window would never outlive its opener".  

However, currently there is a race when:

- opener document is navigated away
- PIP window is opened and navigated

Opening a PIP window and navigating it to a URL while the document is unloading will cause the opened PIP window frame UI to use the new document's origin.

Note that navigating the PIP window should not be possible. [1](https://chromium-review.googlesource.com/c/chromium/src/+/3553772)

Following code is used for acessing the opener web contents:

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc;l=90>

```
void PictureInPictureWindowManager::EnterDocumentPictureInPicture(  
    content::WebContents\* parent_web_contents,  
    content::WebContents\* child_web_contents) {  
  // If there was already a controller, close the existing window before  
  // creating the next one. This needs to happen before creating the new  
  // controller so that its precondition (no child_web_contents_) remains  
  // valid.  
  if (pip_window_controller_)  
    CloseWindowInternal();  
  
  // Start observing the parent web contents.  
  document_web_contents_observer_ =  
      std::make_unique<DocumentWebContentsObserver>(this, parent_web_contents);  
  
  auto\* controller = content::PictureInPictureWindowController::  
      GetOrCreateDocumentPictureInPictureController(parent_web_contents);  
  
  controller->SetChildWebContents(child_web_contents);  
  
  // Show the new window. As a side effect, this also first closes any  
  // pre-existing PictureInPictureWindowController's window (if any).  
  EnterPictureInPictureWithController(controller);  
}  

```

**VERSION**  

Chrome Version: 112.0.5589.0 + beta  

Operating System: Windows 11

**REPRODUCTION CASE**

chrome://flags/#document-picture-in-picture-api

1. Open poc.html
2. Hold Enter

With manual testing I could repro the POC on almost every time. Sometimes more than one PIP window opens, one of them "RESULT\_CODE\_KILLED". The timing might need to be adjusted for different systems.

Note: PIP2 is under an origin trial [2](https://developer.chrome.com/origintrials/#/view_trial/1885882343961395201), therefore it could be reached without the flag. This does not affect stable, but does affects beta and newer branches.

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 501 B)
- [poc.webm](attachments/poc.webm) (video/webm, 1.3 MB)

## Timeline

### [Deleted User] (2023-02-11)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-11)

Thanks for the report!

Sev-Medium for UI spoof with some mitigation/difficulty. Not setting Impact-None, because there is an ongoing origin trial.

liberato@, could you take on this issue or route it to an appropriate owner? Thanks!



[Monorail components: Blink>Media>PictureInPicture]

### [Deleted User] (2023-02-11)

[Empty comment from Monorail migration]

### li...@google.com (2023-02-11)

=> steimel@, who is looking at some similar issues.

### li...@google.com (2023-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2023-02-13)

[BULK EDIT] Reminder: We have 2 more beta releases before Stable Cut on Feb 28. Please help resolve this RBS and request a merge as soon as possible.

### li...@google.com (2023-02-13)

i've tried this with and without [1] applied locally, which fixes it.  in particular, the repro happens when:

 - navigation is noticed by document pip window controller
 - starts close
 - RFHI::ClosePage posts to close after a delay (IsPrimaryMainFrame is true at this point)
 - (later) RFHI::ClosePageIgnoring... runs, and !IsPrimarymainFrame is false => leave pip window open.

[1] fixes this.  i verified that, even with the patch applied, my repro attempts would have taken the bad branch in ClosePageIgnoring if the patch didn't add the extra check to prevent it.  in other words, i didn't accidentally break the timing in the repro+patch attempts.  failed almost every time without the patch, succeeded 4/4 with the patch.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/4242019

### li...@google.com (2023-02-13)

whoops -- in the above, the last '-' should say "IsPrimarymainFrame is false" not "!IsPrimary...".  it's not the primary main frame any more, and it exits early in the repro case is what i was trying to say.

### cr...@chromium.org (2023-02-17)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Navigation]

### gi...@appspot.gserviceaccount.com (2023-02-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5f49142eb086b425f52bb63592ea0a1540e5b2ac

commit 5f49142eb086b425f52bb63592ea0a1540e5b2ac
Author: Tommy Steimel <steimel@chromium.org>
Date: Tue Feb 21 12:51:37 2023

PiP 2.0: Ensure subsequent about:blank loads close the PiP window

Document PiP windows should always close if navigated from the initial
about:blank document. However, the logic allowed for about:blank
navigations to allow the initial navigation to succeed. This opens up a
couple of issues:

1) Refreshing the PiP document breaks but does not close the document

2) Setting the location of the PiP window to about:blank in JS would
disconnect the PiP document from the original window and render it
unusable.

This CL changes that logic to only allow the initial synchronous about:blank navigation to succeed. However, this is insufficient for the
second issue, since there was a race where if the navigation succeeded
before the page closed, then the RenderFrameHostImpl would cancel the
closing action. In order to fix this (and other issues with navigations
canceling the close action), this CL also makes close requests from the
browser side always close the page regardless of navigations.

Bug: 1413919, 1406023, 1414124, 1414975
Change-Id: Ib52875be2ad107ce3f33e2682b0b87f2c7bc6cbf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4242019
Reviewed-by: Charlie Reis <creis@chromium.org>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1107695}

[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/chrome/browser/picture_in_picture/document_picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/chrome/test/data/media/picture-in-picture/document-pip.html
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_proxy_host.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_manager.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_impl_unittest.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/site_per_process_browsertest.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/5f49142eb086b425f52bb63592ea0a1540e5b2ac/content/browser/renderer_host/render_frame_host_manager_unittest.cc


### st...@chromium.org (2023-02-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

Merge review required: M111 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@gmail.com (2023-02-22)

I tried this in r1108335 and I am not able to reproduce the issue anymore.

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-22)

[Empty comment from Monorail migration]

### st...@chromium.org (2023-02-22)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

It fixes a release blocker

2. What changes specifically would you like to merge? Please link to Gerrit.

https://crrev.com/c/4242019

3. Have the changes been released and tested on canary?
Yes, see https://crbug.com/chromium/1414975#c16

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

It fixes an issue in a new feature. The new feature is behind an OT and can be turned off

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

It affects Chrome OS but is not Chrome OS-specific, and based on that list I don't *think* it needs to be approved here, but please correct me if I'm wrong

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

N/A since M111 is not stable yet

### am...@chromium.org (2023-02-24)

Since Document PIP going into OT in M111, I concur merge is appropriate here. 
No issues exhibited on Canary thus far; 111 merge approved 
Please merge this fix to branch 5563 by EOD Monday, 27 February so this fix can be included in M111/Stable cut on Tuesday. Ty!  

### li...@google.com (2023-02-24)

steimel@ is ooo, so i started a cherry pick.  there are some conflicts that i need to look at.

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c3a3e0ff3d045805d4a3e15c6877b189a767e05c

commit c3a3e0ff3d045805d4a3e15c6877b189a767e05c
Author: Tommy Steimel <steimel@chromium.org>
Date: Mon Feb 27 19:13:20 2023

[M111] PiP 2.0: Ensure subsequent about:blank loads close the PiP window

This is a cherry-pick onto M111 of https://crrev.com/c/4242019.

Original CL description:

> Document PiP windows should always close if navigated from the initial
> about:blank document. However, the logic allowed for about:blank
> navigations to allow the initial navigation to succeed. This opens up a
> couple of issues:
>
> 1) Refreshing the PiP document breaks but does not close the document
>
> 2) Setting the location of the PiP window to about:blank in JS would
> disconnect the PiP document from the original window and render it
> unusable.
>
> This CL changes that logic to only allow the initial synchronous about:blank navigation to succeed. However, this is insufficient for the
> second issue, since there was a race where if the navigation succeeded
> before the page closed, then the RenderFrameHostImpl would cancel the
> closing action. In order to fix this (and other issues with navigations
> canceling the close action), this CL also makes close requests from the
> browser side always close the page regardless of navigations.
>
> Bug: 1413919, 1406023, 1414124, 1414975
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4242019
> Reviewed-by: Charlie Reis <creis@chromium.org>
> Commit-Queue: Tommy Steimel <steimel@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1107695}
(cherry picked from commit 5f49142eb086b425f52bb63592ea0a1540e5b2ac)

Change-Id: I56332ac46ed37227be8da03118c1fe49b2e5294e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4292137
Reviewed-by: Alex Moshchuk <alexmos@chromium.org>
Reviewed-by: Fr <beaufort.francois@gmail.com>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/branch-heads/5563@{#866}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/chrome/test/data/media/picture-in-picture/document-pip.html
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_proxy_host.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_impl.h
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/chrome/browser/picture_in_picture/document_picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_manager.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_impl_unittest.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_impl.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/site_per_process_browsertest.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/web_contents/web_contents_impl.cc
[modify] https://crrev.com/c3a3e0ff3d045805d4a3e15c6877b189a767e05c/content/browser/renderer_host/render_frame_host_manager_unittest.cc


### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations, Thomas! The VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-07-06)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-14)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-27)

Already in M114.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1414975?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>PictureInPicture, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063023)*
