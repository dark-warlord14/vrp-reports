# Security: Incorrect Handling of XFrameOptions with mailMsg in the PDF Viewer

| Field | Value |
|-------|-------|
| **Issue ID** | [40053488](https://issues.chromium.org/issues/40053488) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature, Internals>Plugins>PDF |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2020-10-01 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

This bug reproduces only when Gmail is set as default mail handler for chrome.  

It is possible to open compose window of default Email client with Javascript embedded in a PDF file.

ex:  

app.mailMsg(true,"[test@testemail.com](mailto:test@testemail.com)","","","heading","body");

Gmail compose window is loaded inside HTML embed element used by PDF file, when above Javascript is executed.  

This behavior cause two problems.

1. Chrome address bar keeps displaying URL of PDF file.  
   
   Does not change to a Gmail URL.  
   
   If user is not careful, user may not notice that she's sending this message from Gmail.
2. This test case loads a Gmail URL inside HTML embed element.  
   
   This is not allowed by Gmail X-Frame-Options.
   
   If I try to load a Gmail URL directly in HTML embed element like below:  
   
   <embed src="https://mail.google.com/"></embed>
   
   Then chrome displays this error message in console window.  
   
   Refused to display '<https://mail.google.com/mail/u/0/>' in a frame because it set 'X-Frame-Options' to 'sameorigin'.

**VERSION**  

Chrome Version: [85.0.4183.121] + [stable]  

[87.0.4279.0] + [Trunk build]

Operating System: [Windows 10, Ubuntu 18.04]

**REPRODUCTION CASE**

1. Set Gmail as default email handler for chrome.  
   
   Please follow the instruction in this page.  
   
   <https://support.google.com/a/users/answer/9308783?hl=en>
2. Open attached mailto.pdf file with Chrome.
3. Click "Send Message" button.
4. Gmail compose window will load inside HTML embed element used by PDF file.  
   
   Address bar will remain same as of mailto.pdf file.

**CREDIT INFORMATION**  

Reporter credit: [Uncredited]

## Attachments

- [mailto.pdf](attachments/mailto.pdf) (application/pdf, 3.0 KB)
- [screenshot_1.png](attachments/screenshot_1.png) (image/png, 27.3 KB)
- [extension.zip](attachments/extension.zip) (application/octet-stream, 3.0 KB)

## Timeline

### do...@chromium.org (2020-10-02)

Reporter - do you mind adding a screenshot of what you see?

+PDF folks, +CSP folks, and +security UX.

[Monorail components: Blink>SecurityFeature Internals>Plugins>PDF]

### ch...@gmail.com (2020-10-02)

Attached a screenshot as requested in https://crbug.com/chromium/1134338#c1.

### do...@chromium.org (2020-10-02)

#2 - thanks. It literally is just the compose window... that is quite curious.

### ts...@chromium.org (2020-10-02)

This would be in the extension itself, above the PDFium layer. Lei, could someone on your team take a look at this?
Setting serverity medium as we are inserting an iframe into the extension renderer (would be sev-high if one can demonstrate access via javascript to the extension page itself).

### [Deleted User] (2020-10-02)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2020-10-05)

"Mailto:" links in PDF files function properly.

PDF extension calls below function  when a user clicks on a "mailto:" link.
   chrome.tabs.update(this.tabId_, {url: url});
   This is inside "navigateInCurrentTab(url)" method of chrome/browser/resources/pdf/navigator.js file.

PDF extension calls below code when "app.mailMsg" function is used.

  case 'email':
        const emailData = /** @type {!EmailMessageData} */ (messageData);
        const href = 'mailto:' + emailData.to + '?cc=' + emailData.cc +
            '&bcc=' + emailData.bcc + '&subject=' + emailData.subject +
            '&body=' + emailData.body;
        window.location.href = href;

  This is inside "handlePluginMessage_(messageEvent)" of chrome/browser/resources/pdf/controller.js file.

It seems PDF extension redirects to new URL inside the extension page, when "window.location.href " method is used.


### ch...@gmail.com (2020-10-06)

It is possible to load a normal web link such as http://www.google.com inside an EMBED tag, if PDF file is loaded inside an extension.

Steps
--------
1. Download and extract extensions.zip
2. Open chrome and visit "chrome://extensions/".
3. Click "Load Unpacked" button.
4. Navigate to extracted extension folder.
    Click "Select Folder" button.
5. Click on "Extensions Icon" next to address bar.
6. Click on "Test PDF" icon.
7. Chrome will display a popup page.
    This page will load a PDF file inside an EMBED tag.
8. Click on "Google" link inside PDF file.
9. http://www.google.com will be loaded inside embed tag.
   
   I think this should not happen because 'X-Frame-Options' is set to 'sameorigin' by google.com.
   But I am not that sure whether this behavior is allowed inside an extension.

### th...@chromium.org (2020-10-07)

+rdevlin re: https://crbug.com/chromium/1134338#c8. Not sure what to make of that.
+rbpotter FYI.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c7ada1b86a5d7edf4c873e44a4f79c278af10c97

commit c7ada1b86a5d7edf4c873e44a4f79c278af10c97
Author: Lei Zhang <thestig@chromium.org>
Date: Wed Oct 07 22:01:55 2020

Handle mailto links consistently in the PDF Viewer.

Bug: 1134338
Change-Id: I17c4512511911db84d4485fff143cd0d570d57e7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2454797
Reviewed-by: Rebekah Potter <rbpotter@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/heads/master@{#814896}

[modify] https://crrev.com/c7ada1b86a5d7edf4c873e44a4f79c278af10c97/chrome/browser/resources/pdf/controller.js
[modify] https://crrev.com/c7ada1b86a5d7edf4c873e44a4f79c278af10c97/chrome/browser/resources/pdf/pdf_viewer.js


### th...@chromium.org (2020-10-09)

Should we split https://crbug.com/chromium/1134338#c8 into a separate bug?

### rd...@chromium.org (2020-10-09)

I think maybe https://crbug.com/chromium/1134338#c8 is tracked by https://crbug.com/chromium/1115590.  (Thanks, karandeepb@, for the link!)

### ad...@google.com (2020-10-12)

thestig@ is https://crbug.com/chromium/1134338#c10 a complete fix here? If so please could you mark this as Fixed. (Assuming that https://crbug.com/chromium/1134338#c8 really is tracked by https://crbug.com/chromium/1115590.)

### th...@chromium.org (2020-10-12)

Since https://crbug.com/chromium/1134338#c8 has been split out into https://crbug.com/chromium/1115590, I believe r814896 covers the bug.

### [Deleted User] (2020-10-14)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-19)

Requesting merge to beta M87 because latest trunk commit (814896) appears to be after beta branch point (812852).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-10-19)

This bug requires manual review: M87's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: benmason@(Android), bindusuvarna @(iOS), cindyb@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2020-10-20)

thestig@ - please respond to the merge questionnaire in c#18 to consider the M87 merge

### th...@chromium.org (2020-10-20)

I defer to adetaylor@ on question 1, w.r.t. criticality.

2. https://chromium-review.googlesource.com/c/chromium/src/+/2454797
3. Landed - yes. Verified - will double check.
4. Maybe M86?
5. Bug was filed on M87 branch cut day.
6. No
7. N/A

### ad...@google.com (2020-10-20)

Yes, our normal guidelines say we should merge medium severity fixes back to the current beta channel and I see no reason why this would be an exception. Unless you have stability concerns, please merge to M87, branch 4280.

### ad...@google.com (2020-10-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-10-21)

Congratulations, the VRP panel has awarded $3000 for this bug report. Thanks!

### th...@chromium.org (2020-10-22)

Verified with .88.0.4292.2. Merging.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7413302849fa43aacf18ba0f2a65bfffacf8ca2c

commit 7413302849fa43aacf18ba0f2a65bfffacf8ca2c
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Oct 22 10:19:24 2020

M87: Handle mailto links consistently in the PDF Viewer.

(cherry picked from commit c7ada1b86a5d7edf4c873e44a4f79c278af10c97)

Tbr: rbpotter@chromium.org
Bug: 1134338
Change-Id: I17c4512511911db84d4485fff143cd0d570d57e7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2454797
Reviewed-by: Rebekah Potter <rbpotter@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#814896}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2490207
Reviewed-by: Lei Zhang <thestig@chromium.org>
Cr-Commit-Position: refs/branch-heads/4280@{#622}
Cr-Branched-From: ea420fb963f9658c9969b6513c56b8f47efa1a2a-refs/heads/master@{#812852}

[modify] https://crrev.com/7413302849fa43aacf18ba0f2a65bfffacf8ca2c/chrome/browser/resources/pdf/controller.js
[modify] https://crrev.com/7413302849fa43aacf18ba0f2a65bfffacf8ca2c/chrome/browser/resources/pdf/pdf_viewer.js


### ad...@google.com (2020-10-22)

[Empty comment from Monorail migration]

### ch...@gmail.com (2020-11-16)

thestig@ I can still reproduce test case mentioned in https://crbug.com/chromium/1134338#c8 on chrome dev version.
Version: 88.0.4315.5 (Official Build) dev (64-bit)
              88.0.4321.0 (Developer Build) (32-bit)  (Local build)

That test case was split into https://crbug.com/chromium/1115590. Is that bug still open?

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-16)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### vs...@google.com (2020-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-10)

[Empty comment from Monorail migration]

### ke...@google.com (2020-12-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3017fbed7b3f5e2eb66a5614967c05c6f4c36c7d

commit 3017fbed7b3f5e2eb66a5614967c05c6f4c36c7d
Author: Lei Zhang <thestig@chromium.org>
Date: Thu Jan 07 11:09:03 2021

Handle mailto links consistently in the PDF Viewer.

(cherry picked from commit c7ada1b86a5d7edf4c873e44a4f79c278af10c97)

Bug: 1134338
Change-Id: I17c4512511911db84d4485fff143cd0d570d57e7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2454797
Reviewed-by: Rebekah Potter <rbpotter@chromium.org>
Commit-Queue: Lei Zhang <thestig@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#814896}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2584931
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1497}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/3017fbed7b3f5e2eb66a5614967c05c6f4c36c7d/chrome/browser/resources/pdf/controller.js
[modify] https://crrev.com/3017fbed7b3f5e2eb66a5614967c05c6f4c36c7d/chrome/browser/resources/pdf/pdf_viewer.js


### ad...@google.com (2021-01-07)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1134338?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature, Internals>Plugins>PDF]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053488)*
