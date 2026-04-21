# Security: Bypass the Protection of input fields cache (Autofill) 1108181

| Field | Value |
|-------|-------|
| **Issue ID** | [40060742](https://issues.chromium.org/issues/40060742) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Autofill |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **CVE IDs** | CVE-2022-44688 |
| **Reporter** | el...@gmail.com |
| **Assignee** | vi...@google.com |
| **Created** | 2022-08-31 |
| **Bounty** | $5,000.00 |

## Description

## **VULNERABILITY DETAILS** this is a report to a security vulnerability in google chrome/chromium browser as high-quality report with functional exploit. this vulnerability allows attackers to steal thecache of input fields like usernames, e-mail adresses, telephone numbers from any site like twitter, google and any others (Chrome Autofill Saved Data).

## **VERSION** Exploit tested with the following properties: Google Chrome (windows 10) Version 105.0.5195.54 (Official Build) (64-bit)

**REPRODUCTION CASE**

the exploit use a vulnerability in showing of cache of input fields. your browser suggests the saved entries of input fields like saved user logins (username, email, phone number...) or cached search word any similar entered things.

nobody will send critical information to unknown sites. but this can be hide by full bypassing the visibility of all fields and suggests. in this case nobody are able to notice that they are sending their data to unknown attackers.

## REPRODUCTION STEPS

(Play a little jump and run game (Dino) to get hijacked any cached input of fieldname "username",email,telphone,address,cardnumber,.....)

\*\*Before Repro you can add some data under chrome://settings/addresses and add some records

1-visit <https://vrphunt.com/chrome/canvasautofillwindows.html> in (Close and open page again If Start Button not correctly Shown/disabled)

2- Double click the button to start Game

3-Press Arrow UP/Down then Enter

Autofill data Will be shown in the Green Box

---

**CREDIT INFORMATION**  

Reporter credit: Ahmed ElMasry

---

Thank you for your attention. with kind Regards

## Attachments

- [AUTOFILL-POC-FILES.rar](attachments/AUTOFILL-POC-FILES.rar) (application/octet-stream, 4.4 KB)
- [Autofill-POC.mp4](attachments/Autofill-POC.mp4) (video/mp4, 1.4 MB)
- [canvasautofillwindows.html](attachments/canvasautofillwindows.html) (text/plain, 6.8 KB)
- [maincanvasjs.js](attachments/maincanvasjs.js) (text/plain, 3.6 KB)
- [spoofautofillpop.html](attachments/spoofautofillpop.html) (text/plain, 2.8 KB)
- [stylecanvas.css](attachments/stylecanvas.css) (text/plain, 372 B)
- [POC-WINDOWS- 2022-09-05 00-21-19-907.mp4](attachments/POC-WINDOWS- 2022-09-05 00-21-19-907.mp4) (video/mp4, 6.9 MB)
- [Linux-POC-2022-09-05_00-34-20.mkv](attachments/Linux-POC-2022-09-05_00-34-20.mkv) (application/octet-stream, 2.5 MB)
- [Linux-POC-2022-09-05_00-34-20.mp4](attachments/Linux-POC-2022-09-05_00-34-20.mp4) (video/mp4, 1.2 MB)
- [Screenshot_20230116-155939.png](attachments/Screenshot_20230116-155939.png) (image/png, 267.3 KB)
- [Screenshot_20230116-160756.png](attachments/Screenshot_20230116-160756.png) (image/png, 305.4 KB)

## Timeline

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-08-31)

Thanks for the report. I'm redirecting to the AutoFill folks because I don't properly understand their threat model. 

There was a bug in the POC such that the contents of spoofautofillpop.html were visible, which was actually instructive for understanding how the attack works. Namely it attempts to trick the user to interact with a hidden form, luring key presses to cycle through auto-complete values. 

Note: I'm attaching the individual files from the archive in https://crbug.com/chromium/1358647#c1 so others can avoid RAR extraction. 

[Monorail components: UI>Browser>Autofill]

### bo...@chromium.org (2022-08-31)

[Empty comment from Monorail migration]

### ba...@chromium.org (2022-09-01)

Thank you very much for the report. We will look into this.

### el...@gmail.com (2022-09-03)

bookholt@
Sorry to forget file (spoofautofillpop.html) but you got it from live POC, Thx


>>There was a bug in the POC such that the contents of spoofautofillpop.html were visible

in the POC Video attached. I meant to show you the PopUp behind the canvas pip at sec 29 of video to the end , as the whole page is black, to show you how the attack actually works, I can call window.close to close  the PopUp if the PiP has been existed, but this is OK to help you in seeing what actually happens, Thanks for your response, Hope this fixed as soon as possible. 

### el...@gmail.com (2022-09-04)

Hello
bookholt@ ,mlerman@ , after Checking The poc after you mentioned that there is a bug in the POC i've found that i forget to Comment some lines of code  not needed which break the code ,this happen after i sent you the report ,

So Now all Things is Clear and working fine  and i have Refined the code more and removed not needed functions , als i have done some tests on Chrome WIndows Version ,Edge Windows Version ,and Linux Chrome and Edge too, so Please you can Remove the attachment Files on Previous Comments  to Avoid Confusion while testing

I Confirmed That the Live POC Working Fine Both Linux and Windows Version 

what i have tested
-------------------------- 
Windows 10 Enterprise 2H1 Build (19043.1826)

Chrome (105.0.5195.102) official Build 64 Bit Both Normal mode and Incognito Mode

Edge (105.0.1343.27) Official Build 64 Bit Both Normal mode and Incognito Mode

-----------
POC Live URL :

This POC Refined to work Both Windows and Linux

https://vrphunt.com/chrome/canvasautofill.html

POC-Windows Video with name (POC-WINDOWS- 2022-09-05 00-21-19-907.mp4)
POC-Linux Video with name (Linux-POC-2022-09-05_00-34-20.mkv)

========================
Second :

I've also Refined the Mentioned URL POC Code that was Buggy by mistake at main Ticket Comment

https://vrphunt.com/chrome/canvasautofillwindows.html

this Works for Windows Only Not Refined for Linux 

=========
Live POC are Clean and Become Direct to Test. You Can Try Dual Working POC URL 

Thanks 

### el...@gmail.com (2022-09-04)

[Empty comment from Monorail migration]

### ml...@chromium.org (2022-09-05)

[Empty comment from Monorail migration]

### ml...@chromium.org (2022-09-05)

[Empty comment from Monorail migration]

### ml...@chromium.org (2022-09-06)

Thanks for providing the additional details. I'm working to see who's best to assign this to.

### [Deleted User] (2022-09-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2022-09-08)

[Empty comment from Monorail migration]

### vi...@google.com (2022-09-08)

[Empty comment from Monorail migration]

### el...@gmail.com (2022-09-12)

Hi 
vidhanj@
mlerman@ any updates? I didn't see any activity on this? It's two weeks from submission and no Open CL yet 

Thanks all for your time 

### vi...@google.com (2022-09-13)

Hi 

I haven't made enough progress on this yet. I'll update here once I have a CL.

Thanks!

### vi...@google.com (2022-09-22)

[Empty comment from Monorail migration]

### vi...@google.com (2022-09-26)

CC'ing Picture-in-Picture folks

### vi...@google.com (2022-10-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/87cf1589bb30dde902d74657840c8486b605a9b1

commit 87cf1589bb30dde902d74657840c8486b605a9b1
Author: Vidhan <vidhanj@google.com>
Date: Mon Oct 17 13:14:18 2022

Add GetWindowBounds for PictureInPicture

The window bounds would be used to check for any overlaps with the
Autofill popup in the next CLs.

Bug: 1358647
Change-Id: Ie564d1cdf26532a30b796eff15c402c5879332d0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3921456
Reviewed-by: Fr <beaufort.francois@gmail.com>
Commit-Queue: Vidhan Jain <vidhanj@google.com>
Reviewed-by: Kazuki Takise <takise@chromium.org>
Reviewed-by: Eliot Courtney <edcourtney@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1059914}

[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/chrome/browser/picture_in_picture/document_picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/content/browser/picture_in_picture/video_picture_in_picture_window_controller_impl.h
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/content/public/browser/picture_in_picture_window_controller.h
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/content/browser/picture_in_picture/video_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.h
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/content/browser/picture_in_picture/video_picture_in_picture_content_browsertest.cc
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/chrome/browser/picture_in_picture/video_picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/chrome/browser/ash/arc/pip/arc_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/chrome/browser/ui/views/overlay/document_overlay_window_views_unittest.cc
[modify] https://crrev.com/87cf1589bb30dde902d74657840c8486b605a9b1/chrome/browser/ash/arc/pip/arc_picture_in_picture_window_controller_impl.h


### vi...@google.com (2022-10-17)

Tentative fix: https://chromium-review.googlesource.com/c/chromium/src/+/3959939

### [Deleted User] (2022-10-31)

vidhanj: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@gmail.com (2022-11-01)

Thanks ,vidhanj@ and François  and all for working on fixing this issue.

please mark this as fixed so that sheriffbot can add reward label to it .

well, but my most intention to report bugs to google is the bug bounty program and their rewards (especially in the Bad economic conditions as a result of the Ukrainian war in conjunction with the repercussions of Covid-19).

when and where can i find out how my fully detailed "High-quality Report with multi Functional Exploits PoCs" is rewarded?
Referring to 
https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules

Thanks all

### vi...@google.com (2022-11-01)

https://chromium-review.googlesource.com/c/chromium/src/+/3959939 still needs to get merged to mark it as fixed.

### gi...@appspot.gserviceaccount.com (2022-11-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ff1874e9b31c51520032643e4ce3101a42743dee

commit ff1874e9b31c51520032643e4ce3101a42743dee
Author: Vidhan <vidhanj@google.com>
Date: Mon Nov 07 16:39:21 2022

Hide Autofill popup if it overlaps with picture-in-picture window

This CL introduces BoundsOverlapWithPictureInPictureWindow used in
autofill_popup_view_native_views.cc to determine whether there is an
overlap between the picture-in-picture window and the autofill popup.
If it does, it hides the autofill popup.

Bug: 1358647
Change-Id: Icea36db627ed0e4bb0d910cab692711f886814ec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3959939
Reviewed-by: Fr <beaufort.francois@gmail.com>
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Commit-Queue: Vidhan Jain <vidhanj@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/heads/main@{#1068138}

[modify] https://crrev.com/ff1874e9b31c51520032643e4ce3101a42743dee/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/ff1874e9b31c51520032643e4ce3101a42743dee/chrome/browser/ui/views/autofill/autofill_popup_base_view.cc
[modify] https://crrev.com/ff1874e9b31c51520032643e4ce3101a42743dee/chrome/browser/ui/views/autofill/autofill_popup_view_utils.h
[modify] https://crrev.com/ff1874e9b31c51520032643e4ce3101a42743dee/components/autofill/core/browser/ui/popup_types.h
[modify] https://crrev.com/ff1874e9b31c51520032643e4ce3101a42743dee/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/ff1874e9b31c51520032643e4ce3101a42743dee/chrome/browser/ui/views/autofill/autofill_popup_view_utils.cc
[modify] https://crrev.com/ff1874e9b31c51520032643e4ce3101a42743dee/chrome/browser/picture_in_picture/picture_in_picture_window_manager.h
[modify] https://crrev.com/ff1874e9b31c51520032643e4ce3101a42743dee/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/ff1874e9b31c51520032643e4ce3101a42743dee/chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc


### am...@chromium.org (2022-11-08)

In reference to https://crbug.com/chromium/1358647#c25, security bugs should get updated as Fixed as soon as the resolving CL is landed. [1]
Sheriffbot will update the issue with the appropriate merge request/review labels based on security severity and security impact; and put the issue into the security merge review accordingly. 

Updating as Fixed accordingly so that merge request/review process can be initiated. 

[1]  https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#security-merge-triage 

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-08)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-14)

The bot did not label this one (adding to ongoing bug about this), putting into 108 merge review queue (heads up that merge will need to be done by 10am Pacific time tomorrow/Tuesday to ensure this fix goes into 108/stable release cut) 

### [Deleted User] (2022-11-14)

Merge review required: M108 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-15)

M108 merge approved, please merge this fix to branch 5359 at soonest (by tomorrow/Tuesday 10am Pacific) so this fix can be included in M108 Stable cut -- thank you

### sr...@google.com (2022-11-15)

I have CP'ed CL to M108 here -https://chromium-review.googlesource.com/c/chromium/src/+/4027141

### am...@google.com (2022-11-15)

Since both CLs would need to be backmerged to M108 (https://ccrev.com/c/3921456 and https://ccrev.com/c/4027141) and RC for M108 stable is being cut today, we'll need to defer merge until tomorrow (wednesday) at the earliest and these fixes can be included in M108/Stable respin. 

### sc...@google.com (2022-11-15)

I'm on it, sorry for the delay.

### sr...@google.com (2022-11-15)

per offline chat with schwering, in order to not delay the RC cut further, we can let this fix land later and be included in the next re-spin. 

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-18)

Congratulations, Ahmed! The VRP Panel has decided to award you $5,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### el...@gmail.com (2022-11-18)

[Comment Deleted]

### [Deleted User] (2022-11-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-11-18)

Hi Ahmed, CVEs are issued when the fix is shipped in a Stable channel release and will be updated directly here at that time. 
I've also confirmed that emiliapaz@ should have access to https://crbug.com/chromium/1369103 and have added a comment to request her evaluate if your report is a duplicate of 1331162. 

vidhanj@ - please let me know if you would like access to 1369103 and have time to take a look. 


### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### sr...@google.com (2022-11-22)

pls complete the merges asap to M108, we have to recut M108 RC for a security zero day, so i will like to include this merge to M108,.
Please complete the merges asap by EOD today 

### ba...@chromium.org (2022-11-23)

Srinivas I found two CLs that are currently waiting for your LGTM:
https://chromium-review.googlesource.com/c/chromium/src/+/4028799
https://chromium-review.googlesource.com/c/chromium/src/+/4027141

### gi...@appspot.gserviceaccount.com (2022-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/010dbbd3762c1a96a990cb41ddb0d3e92258cd82

commit 010dbbd3762c1a96a990cb41ddb0d3e92258cd82
Author: Vidhan <vidhanj@google.com>
Date: Wed Nov 23 18:53:56 2022

Add GetWindowBounds for PictureInPicture

The window bounds would be used to check for any overlaps with the
Autofill popup in the next CLs.

(cherry picked from commit 87cf1589bb30dde902d74657840c8486b605a9b1)

Bug: 1358647
Change-Id: Ie564d1cdf26532a30b796eff15c402c5879332d0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3921456
Reviewed-by: Fr <beaufort.francois@gmail.com>
Commit-Queue: Vidhan Jain <vidhanj@google.com>
Reviewed-by: Kazuki Takise <takise@chromium.org>
Reviewed-by: Eliot Courtney <edcourtney@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1059914}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4028799
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Auto-Submit: Christoph Schwering <schwering@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#934}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/chrome/browser/picture_in_picture/document_picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/content/browser/picture_in_picture/video_picture_in_picture_window_controller_impl.h
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/content/public/browser/picture_in_picture_window_controller.h
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/content/browser/picture_in_picture/video_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/chrome/browser/ui/views/overlay/video_overlay_window_views_unittest.cc
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.h
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/content/browser/picture_in_picture/video_picture_in_picture_content_browsertest.cc
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/content/browser/picture_in_picture/document_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/chrome/browser/picture_in_picture/video_picture_in_picture_window_controller_browsertest.cc
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/chrome/browser/ash/arc/pip/arc_picture_in_picture_window_controller_impl.cc
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/chrome/browser/ui/views/overlay/document_overlay_window_views_unittest.cc
[modify] https://crrev.com/010dbbd3762c1a96a990cb41ddb0d3e92258cd82/chrome/browser/ash/arc/pip/arc_picture_in_picture_window_controller_impl.h


### gi...@appspot.gserviceaccount.com (2022-11-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202

commit d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202
Author: Vidhan <vidhanj@google.com>
Date: Wed Nov 23 20:35:44 2022

Hide Autofill popup if it overlaps with picture-in-picture window

This CL introduces BoundsOverlapWithPictureInPictureWindow used in
autofill_popup_view_native_views.cc to determine whether there is an
overlap between the picture-in-picture window and the autofill popup.
If it does, it hides the autofill popup.

(cherry picked from commit ff1874e9b31c51520032643e4ce3101a42743dee)

Bug: 1358647
Change-Id: Icea36db627ed0e4bb0d910cab692711f886814ec
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3959939
Reviewed-by: Fr <beaufort.francois@gmail.com>
Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org>
Commit-Queue: Vidhan Jain <vidhanj@google.com>
Reviewed-by: Christoph Schwering <schwering@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1068138}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4027141
Owners-Override: Srinivas Sista <srinivassista@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#937}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202/chrome/browser/ui/autofill/autofill_popup_controller_impl.cc
[modify] https://crrev.com/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202/chrome/browser/ui/views/autofill/autofill_popup_base_view.cc
[modify] https://crrev.com/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202/chrome/browser/ui/views/autofill/autofill_popup_view_utils.h
[modify] https://crrev.com/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202/components/autofill/core/browser/ui/popup_types.h
[modify] https://crrev.com/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202/chrome/browser/ui/views/autofill/autofill_popup_view_native_views.cc
[modify] https://crrev.com/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202/chrome/browser/ui/views/autofill/autofill_popup_view_utils.cc
[modify] https://crrev.com/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202/chrome/browser/picture_in_picture/picture_in_picture_window_manager.h
[modify] https://crrev.com/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202/tools/metrics/histograms/enums.xml
[modify] https://crrev.com/d2e718e05d222bfb1c7df8e462b0eb7ca4f4c202/chrome/browser/picture_in_picture/picture_in_picture_window_manager.cc


### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### vi...@google.com (2022-11-29)

 amyressler@, I don't have access to crbug,com/1369103


### am...@chromium.org (2022-11-29)

vidhanj@, I've cc'ed you on https://crbug.com/chromium/1369103 - you should have access to it now 

### el...@gmail.com (2022-11-29)

Thanks Amy amyressler@  for your efforts,

I've checked the fix landed here on Chrome DEV 108 and 109 and fix works fine , i have similar bug reported a couple of hours ago,and related to the 1st CL at https://crbug.com/chromium/1358647#c45 

Could you please take a look and CC the same folks here as the fix depends on the Main  CL  landed here and the exploit same way using PIP(picture in picture) 

https://crbug.com/chromium/1394410

Thanks , Appreciate your help and time  in advance 


### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### el...@gmail.com (2022-12-01)

amyressler@

Could You Check The Bypass for that at  Issue:1358647 and Add/Assign same folks to it  if available , for tight fix .?
vidhanj@

Thanks You All 

### el...@gmail.com (2022-12-01)

**sorry Bypass at https://crbug.com/chromium/1395164

### cf...@google.com (2022-12-01)

[Empty comment from Monorail migration]

### el...@gmail.com (2023-01-13)

Hi ..

Action Needed 

VIP  Notes  hope you consider this well and take right action 

1- Please Add Embargo Label / Restrict-View-Google , as it will be public at the Beginning of FEB/2023 ,and it has not been fixed on Microsoft Edge(Chromium) & it may be used to affect innocent people.

2-Could you also add Some Microsoft Folks here , Because after the fix landed and reached to all users ,reported the bug to Microsoft Edge team at Dec 21, 2022, as it becomes related to edge ,Microsoft  case manger replied today (13-JAN-2023) and mentioned
------------
>>
Thank you for taking the time to submit this report. This issue appears to be an upstream issue. 

Please report the issue directly to Google Chrome: https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules

Warm Regards,

MSRC
---------------

MSRC CASE#: VULN-082426

Proof: https://drive.google.com/file/d/1LipaRCNxMX2pjWAUh2_vkHzeUusIWGSf/view?usp=sharing

**Please take the right actions towards the above two points.**

Thanks for All


### am...@chromium.org (2023-01-13)

Hello, thank for your reaching out about this. There is no need for RV-SE or RV-G in this case, and actually these labels would be detrimental in this case as it would prohibit the Edge folk at MSFT and other embedders from accessing this fix. Once this issue was marked as Fixed it provided access to this issue and the fix to be leveraged in Edge and other Chromium based browsers and software at that time. 

### am...@chromium.org (2023-01-13)

I thought it might be helpful to convey this is a standard process, and is exhibited by the Restrict-View-SecurityNotify label that is present on this bug, added just after it was updated as Fixed. This is the process that allows the Chromium embedders, like Edge and other Chromium-based browsers and software, to have access to the issue and see the related fix. MSFT folks and others already have access to this issue so no need to add any here and we certainly do not want to RV access away from them. 

### el...@gmail.com (2023-01-13)

Thanks Amy  amyressler@ for your Quick Response, 

i asked CC for some Microsoft folks here , as the bug closed in MSRC portal and received this reply

>>
Thank you for taking the time to submit this report. This issue appears to be an upstream issue. 

Please report the issue directly to Google Chrome: https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules

Warm Regards,

MSRC
---------------

and i know this isn't upstream from Google side , so i  need to be fired and looked at again before publishing this and some users data could be collected using this bug.

Do you have any explanation why he said it belonged to Google, so i need you clear that point from you side mentioning some folks as it isn't related to upstream.

Thanks 

### am...@chromium.org (2023-01-13)

What MSFT is conveying is correct, because Chromium the upstream project that supports Edge. This issue lives in core Chromium, impacting Chrome and Edge, so the issue is in upstream. Google (Chrome Security team) are the stewards of Chromium security issues so this issue belongs does belong to Google who resolved it (well, specifically vidhanj@ resolved it). 
As we fixed it, the fix is now (has been) available by downstream Chromium-based browsers, like Edge, and other Chromium based produced to be picked up and used in their updates of their products. 
Hope this helps. 

### el...@gmail.com (2023-01-13)

amyressler@ , Fixed in Chrome Browser 108.0.5359.71 ( Mac/linux) and 108.0.5359.71/72( Windows)

and Microsoft downstream the update at

Microsoft Edge Version: 108.0.1462.41	
Date Released    5-DEC-2022	
Based on Chromium Version 108.0.5359.94
--------
and  now it still Reproduce at Edge109.0.1518.49 (Official build) (64-bit) , that should include fix since 5 dec-2022 .and they closed the bug after review today as resolved and it is not , and told me to report to Google, i'am so confused
this video show the proof that this still repro in edge but not in chrome.
https://drive.google.com/file/d/1LipaRCNxMX2pjWAUh2_vkHzeUusIWGSf/view?usp=sharing

What Should i do now..?!, i think you are the right one who can help me for what to do 

should i report to google again ?! 

thanks


### am...@chromium.org (2023-01-13)

No, if it is not reproducing in Chrome and the patch works for this issue, please do not report it back to us again. :) 
If it is still reproducing in Edge, please go back to your report with MSRC and link them to his bug report and convey this has been fixed in Chromium. 
Either, they potentially have not picked up the patch OR there is an Edge-specific issue that is causing this to reproduce in Edge. 

Thanks for including the video, but if this issue is only reproducing in Edge, there's not much else we can do on our side. 


### am...@chromium.org (2023-01-13)

Having watched your video, I could see how if they didn't watch the video to the end and based on the report at a superficial level, they could believe this issue impacts all Chromium browsers. Please simply go back to your report with MSRC and report that this issue was fixed in Chromium and not longer reproduces in Chrome and only reproduces in Chromium. Feel free to link this bug report and also provide them the link to the fix commits to help convey your message: 
https://chromium-review.googlesource.com/c/chromium/src/+/4028799
https://chromium-review.googlesource.com/c/chromium/src/+/4027141


### el...@gmail.com (2023-01-13)

amyressler@ 
>> please do not report it back to us again. :) 
Sure, i know that it's not yours, you fixed this but bypass at  https://crbug.com/chromium/1395164 still not.

>>If it is still reproducing in Edge, please go back to your report with MSRC and link them to his bug report and convey this has been fixed in Chromium.
sure,i did that.

>>Either, they potentially have not picked up the patch OR there is an Edge-specific issue that is causing this to reproduce in Edge. 
the patch merged since 5-DEC-2022 but Microsoft Edge has it's own custom Autofill popup with addtional search feature and copy from clipboard data to autofill rows,i think this breaks your fix.

>> about https://crbug.com/chromium/1358647#c63
i did with exploit additional features related to edge  fully detailed with CLs but it seems like gone to the wrong case manger.
if you could ping  some good one internally to take a look it will be great and helpful.


thanks amy 


### am...@chromium.org (2023-01-14)

Thanks for your efforts on this. I've reached out to someone at MSRC to see if they could look into this. 

### ga...@microsoft.com (2023-01-16)

Thank you both for reaching out, I can confirm that this was resolved in Edge official 109.0.1518.55

### el...@gmail.com (2023-01-16)

Hi
garet...@microsoft

Thanks for your feedback.

>>I can confirm that this was resolved in Edge official 109.0.1518.55

Rep:/ this release still not available to users . Last updated chrome version is Edge109.0.1518.49.


Referring to:
 https://www.microsoft.com/en-us/msrc/bounty-new-edge?rtc=1

As MSRC stated
-------------------
Vulnerability submissions must meet the following criteria to be eligible for bounty awards: 

Identify a previously unreported vulnerability that is unique to Microsoft Edge based on Chromium, in the Dev, Beta, or Stable channels, and which does not reproduce on the equivalent channel of Google Chrome. 
Vulnerabilities must be reproducible on the latest version of Microsoft Edge at the time of submission running on the latest, fully patched version of Windows (including Windows 10, Windows 7 SP1 or Windows 8.1), Linux, MacOS, Android, or iOS. Testing in Windows Insider Preview is not required. 
----------

And the my report qualify this criteria and rules.
------------

How it was closed as resolved at Jan 13, 2023 without being issued a bounty?

How come MSRC sent me Report this back to google and it was fixed here ?!

------------
My report was sent to MSRC at Dec 21, 2022 while it was fixed in chrome upstream, and not fixed in your same chromium based version which is Edge V108.0.1462.41(chromium) based on Chromium 108.0.5359.94 and released in 5-DEC-2022.


As Mentioned in https://crbug.com/chromium/1358647#c61  Referring to my previous CVE 
at this link shows Edge version and based on Chromium version  https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-44688

So please Consider Every note i've stated here and hope you review the case well and consider also bounty Decision?

Isn't this deserve that based on your program rules?

Thanks and Regards.


### el...@gmail.com (2023-01-16)

Hi Amy amyressler@

Thanks for reaching out garet...@microsoft
Could you add him to cc list / send me his mail for direct contact or  confirm that he received my last comment at 67 .

Waiting for your yor response and garet...@


### am...@chromium.org (2023-01-17)

MSFT was just a little late in picking up this fix to include in their update. Per Microsoft, this issue was resolved in Edge v109.0.1518.55. 


### el...@gmail.com (2023-01-17)

Hi ..
Thank you so much Amy for your continued support and help , MSFT reopened the case again  , MSFT released Edge v109.0.1518.55 at 1/15/2023, and i confirmed with Gareth that the bug still works perfectly on that version with providing them POC Videos proof for that version  , they changed the case from resolved to develop state so that they are working on the fix because they realized that this issue specific to Microsoft Edge only ..

So please don't let this bug go public until MSFT fixes this BUG.

Again ,thank you so much for your great help , as expected Google have smart ,talented and helpful people.

### [Deleted User] (2023-02-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1358647?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060742)*
