# Security: Hide real extension of file by many white spaces via suggestedName parameter - showSaveFilePicker

| Field | Value |
|-------|-------|
| **Issue ID** | [40060615](https://issues.chromium.org/issues/40060615) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Storage>FileSystem |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2022-08-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1140403> can be bypassed by using suggestedName parameter in showSaveFilePicker

**VERSION**  

Chrome Version: 104.0.5112.101 (Official Build) (64-bit) (cohort: 104\_stable\_101\_rampup)  

Operating System: Windows 10 Version 21H2 (Build 19044.1889)

**REPRODUCTION CASE**

1. See the attached HTML, click on download button.
2. notmalicious.txt file is downloaded but the real extension is .bat. The real extension is hidden via many many many, whitespaces in suggestedName parameter.
3. Clicking on it will launch calc.exe

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [poc.png](attachments/poc.png) (image/png, 3.1 KB)
- [filepicker-poc.html](attachments/filepicker-poc.html) (text/plain, 1.5 KB)
- [unfixed-poc.png](attachments/unfixed-poc.png) (image/png, 7.7 KB)

## Timeline

### [Deleted User] (2022-08-19)

[Empty comment from Monorail migration]

### sr...@google.com (2022-08-19)

Thanks for the report. I'll use the same severity as crbug.com/1140403.
asully@, since you fixed the other bug, could you take a look at this one too?

[Monorail components: Blink>Storage>FileSystem]

### as...@chromium.org (2022-08-19)

Thanks for the report! I've got a fix up that should land shortly https://crrev.com/c/3841864

### as...@chromium.org (2022-08-19)

mek: is this something that should be added to the spec? We are explicit about only allowing extensions of up to 16 code points in FilePickerOptions, but we're more vague about the sanitization done for the extension for suggestedName https://wicg.github.io/file-system-access/#:~:text=If%20the%20suggestedName%20is%20deemed%20too%20dangerous%2C%20user%20agents%20should%20ignore%20or%20sanitize%20the%20suggested%20file%20name%2C%20similar%20to%20the%20sanitization%20done%20when%20fetching%20something%20as%20a%20download.

### me...@chromium.org (2022-08-19)

Not adding it to the spec makes it easier to tweak the logic, although if there are particular constraints we place it might make sense to add them anyway. Extension validation is in the spec because it throws, while filename sanitization/validation doesn't have website visible consequences; all it can break is user/developer expectations (although it does have user visible consequences, so developers probably still want to know about it).

### gi...@appspot.gserviceaccount.com (2022-08-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/028168a938a7af57b6886a5611478692cd7e2cd7

commit 028168a938a7af57b6886a5611478692cd7e2cd7
Author: Austin Sullivan <asully@chromium.org>
Date: Mon Aug 22 17:36:05 2022

FSA: Restrict suggestedName extensions to 16 characters

Matches the extension length restriction for FilePickerOptions

Bug: 1354505
Change-Id: I37d61aed0bcebbdf05d131a33cc0f14b117f04e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3841864
Commit-Queue: Daseul Lee <dslee@chromium.org>
Reviewed-by: Daseul Lee <dslee@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1037829}

[modify] https://crrev.com/028168a938a7af57b6886a5611478692cd7e2cd7/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/028168a938a7af57b6886a5611478692cd7e2cd7/content/browser/file_system_access/file_system_chooser_browsertest.cc


### as...@chromium.org (2022-08-22)

Makes sense! I might add a hint in the suggestedName portion of the spec that the restrictions on extensions should be the same as for FilePickerOptions

### [Deleted User] (2022-08-22)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-08-22)

[Empty comment from Monorail migration]

### sr...@google.com (2022-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-23)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

Requesting merge to beta M105 because latest trunk commit (1037829) appears to be after beta branch point (1027018).

Requesting merge to dev M106 because latest trunk commit (1037829) appears to be after dev branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

Merge approved: your change passed merge requirements and is auto-approved for M106. Please go ahead and merge the CL to branch 5249 (refs/branch-heads/5249) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

Merge review required: M105 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-08-23)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches

Yes, medium severity security bug

2. What changes specifically would you like to merge? Please link to Gerrit.

https://crrev.com/c/3851961 (cherry-pick of https://crrev.com/c/3841864)

3. Have the changes been released and tested on canary?

Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No

### sr...@google.com (2022-08-24)

Please help complete your merge to M106 branch asap today before 3pm PST. Dev RC build will be cut today evening for release tomorrow.

### gi...@appspot.gserviceaccount.com (2022-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fab3720aa1197cf847d165fc334d00c00a871d21

commit fab3720aa1197cf847d165fc334d00c00a871d21
Author: Austin Sullivan <asully@chromium.org>
Date: Wed Aug 24 20:05:38 2022

[M106] FSA: Restrict suggestedName extensions to 16 characters

Matches the extension length restriction for FilePickerOptions

(cherry picked from commit 028168a938a7af57b6886a5611478692cd7e2cd7)

Bug: 1354505
Change-Id: I37d61aed0bcebbdf05d131a33cc0f14b117f04e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3841864
Commit-Queue: Daseul Lee <dslee@chromium.org>
Reviewed-by: Daseul Lee <dslee@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1037829}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3851062
Cr-Commit-Position: refs/branch-heads/5249@{#80}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/fab3720aa1197cf847d165fc334d00c00a871d21/content/browser/file_system_access/file_system_chooser.cc
[modify] https://crrev.com/fab3720aa1197cf847d165fc334d00c00a871d21/content/browser/file_system_access/file_system_chooser_browsertest.cc


### [Deleted User] (2022-08-24)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-08-24)

1. Was this issue a regression for the milestone it was found in?

No

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No. The suggestedName option was introduced in M91

### as...@chromium.org (2022-08-24)

Spec PR created: https://github.com/WICG/file-system-access/pull/384

### rz...@google.com (2022-08-25)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-25)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-25)

1. Just https://crrev.com/c/3856176
2. Low, simple conflict in the unit tests
3. 105, 106
4. Yes

### as...@chromium.org (2022-08-26)

Just to clarify https://crbug.com/chromium/1354505#c25: this hasn't yet been merged to 105 (merge review is still pending)

### ha...@gmail.com (2022-08-30)

Hi asully@, I am not sure how this has been fixed, but I can still insert many whitespaces in Chrome Canary,

In addition, the prompt activates on Chrome canary, but the many whitespaces will elide the actual extension. (See the picture I just attached) [Should I open a separate bug for this?]

The other many whitespaces variant in getFileHandle() bug I submitted - https://bugs.chromium.org/p/chromium/issues/detail?id=1354850, is also unfixed on Canary. No "dangerous file" prompt will activate there as well. I think it should be reopened

### as...@chromium.org (2022-08-30)

Apologies, I had misinterpreted this bug. The character limit only applies to the trailing extension, which in this case is hidden by the spaces

It seems like there's two things going on here.

(1) It's not really the extension that needs to be sanitized, but the filename itself... which is tricky, since generally we generally prefer algorithmic approaches of sanitizing filenames (such as restricting specific characters or extensions) as opposed to heuristics which may violate develop expectations. But limiting use of spaces (" ") or periods (".") in filenames is not reasonable (for example, a file name like "1.1 Introduction.pptx" should be completely valid.

Perhaps collapsing repeated spaces would work?
Before: notmalicious.txt                .exe
After: notmalicious.txt .exe

(2) In the image above, there's no indication that the file name is overflowing the dialog box. 

+pbos how do prompts typically deal with overflow? Is there a way to configure the prompt to show something like "notmalicious.txt       ...  .exe"?

### [Deleted User] (2022-08-30)

[Empty comment from Monorail migration]

### pb...@chromium.org (2022-08-30)

+cc pkasting@ do we have any canonical suggestions here? I don't know that I've hit this before.

### pb...@chromium.org (2022-08-30)

Maybe this means the title needs to be ...-elided, or maybe that the filename needs to go in the dialog where it can be unelided.

### as...@chromium.org (2022-08-30)

https://crrev.com/c/3866652 should fix (1). Which makes (2) less pressing, though not NOT relevant because if the file name is long enough the extension will still be hidden

This doesn't address https://crbug.com/chromium/1354850, though (creating a file in a directory you already have write permission to via getFileHandle). But I'm not sure if it should? +sroettger do you have thoughts here?

### pk...@chromium.org (2022-08-31)

I think we should not try and "sanitize" the file name, but rather should elide the filename for display rather than clipping it.  ui/gfx/text_elider.h has a method called ElideFilename() that does what you want here (prioritizes the file extension), and I see it's being called from chrome/browser/ui/views/web_apps/file_handler_launch_dialog_view.cc, so maybe there's something there you can crib from.

### ha...@gmail.com (2022-09-01)

Maybe collapsing whitespaces after a preceding '.' may be better?

### gm...@google.com (2022-09-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-08)

while this issue has been reopened for ongoing work, please merge the original fix to M105 (https://crrev.com/c/3841864) to branch 5195 ASAP (NLT tomorrow/Friday, 9 September) so this fix can be included in the next stable security respin --- thanks, Austin! 

### pb...@google.com (2022-09-08)

This merge has been approved for M105, please help complete your merges asap (before 4pm PST) today, so the change can be included in next weeks RC build for Stable releases.

### am...@chromium.org (2022-09-09)

spoke to Austin off bug, a new fix CL will be landed to fully resolve this issue targeted for M106; removing 105 merge approval label as merge of https://crrev.com/c/3841864 is no longer necessary 

### gm...@google.com (2022-09-12)

@rzanoni, please review https://crbug.com/chromium/1354505#c38 and assess merge request for LTS-102 

### gm...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### gm...@google.com (2022-09-13)

@rzanoni, Please submit a merge request once fixed and merged to 106

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### gm...@google.com (2022-10-13)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-10-14)

Apologies, this bug fell through the cracks. I just put up a CL to actually fix this now https://crrev.com/c/3955966

### ha...@gmail.com (2022-11-18)

Hi, any updates here? The CL https://crrev.com/c/3955966 seems to have been stale.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### as...@chromium.org (2023-01-05)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-01-19)

Hi any updates here? Perhaps you could show first N characters and then ... and then the file extension?

Or you can collapse the whitespaces in the filename shown in the prompt only but not the actual filename.

### as...@chromium.org (2023-01-31)

Hi OP, sorry for the delays here. gfx::ElideFilename() is great (thanks for the pointer, @pkasting) but unfortunately this is still quite tricky to fix since the filename elision is dependent on the size of the dialog, while the elided text is needed to construct said dialog... It's a bit of a mess. I revived the CL the other day, but it's still WIP

### gi...@appspot.gserviceaccount.com (2023-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cd19df2323dd3c7598201b7436181a267d0c952f

commit cd19df2323dd3c7598201b7436181a267d0c952f
Author: Austin Sullivan <asully@chromium.org>
Date: Tue Jan 31 16:52:42 2023

FSA: Elide filenames in permission prompt titles

This prioritizes showing the file extension for files with long names
that would otherwise overflow the dialog box.

Screenshots (Googler-only, sorry): go/fsa-filename-elision

Bug: 1354505
Change-Id: I1c6c72c6b19c36c712080c8bdbc0a541a5ecf89c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3955966
Reviewed-by: Daseul Lee <dslee@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Reviewed-by: Allen Bauer <kylixrd@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1099285}

[modify] https://crrev.com/cd19df2323dd3c7598201b7436181a267d0c952f/chrome/browser/ui/views/file_system_access/file_system_access_dangerous_file_dialog.cc
[modify] https://crrev.com/cd19df2323dd3c7598201b7436181a267d0c952f/chrome/browser/ui/views/file_system_access/file_system_access_usage_bubble_view.cc
[modify] https://crrev.com/cd19df2323dd3c7598201b7436181a267d0c952f/chrome/browser/ui/views/file_system_access/file_system_access_ui_helpers_unittest.cc
[modify] https://crrev.com/cd19df2323dd3c7598201b7436181a267d0c952f/chrome/browser/ui/views/file_system_access/file_system_access_ui_helpers.cc
[modify] https://crrev.com/cd19df2323dd3c7598201b7436181a267d0c952f/chrome/browser/ui/views/file_system_access/file_system_access_permission_dialog.cc
[modify] https://crrev.com/cd19df2323dd3c7598201b7436181a267d0c952f/chrome/browser/ui/views/file_system_access/file_system_access_ui_helpers.h


### as...@chromium.org (2023-01-31)

I'm not super happy with how this was fixed (https://crbug.com/chromium/1411723 tracks making the implementation better), but the security issue is at least fixed

### as...@chromium.org (2023-02-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-10)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-06)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1354505?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1354850, crbug.com/chromium/1405195]
[Monorail components added to Component Tags custom field.]

### dx...@google.com (2025-06-19)

Project: chromium/src  

Branch: main  

Author: Mingyu Lei [leimy@chromium.org](mailto:leimy@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6654447>

FSA: make the file name elision result shorter to fit in the dialog

---


Expand for full commit details
```
     
    Previously, even if the file name is elided with the real extension 
    type, it could be still too long to fit in the dialog title, so the 
    extension now could be clipped again and lead to the same issue 
    discussed in the original bug. This may be caused by recent UI revamp or 
    it could be device specific. 
     
    While we still need 40254943 to be fixed, this CL serves as a quick 
    mitigation to shorten the file name, making the extension visible in a 
    small dialog. 
     
    Comparison of dialog UI before and after the change: 
    https://docs.google.com/document/d/1MZSvmtIyC44qMF6H76t74F9ydXwdmOA-OElYGE8Zuuo 
     
    Bug: 40060615, 421950224 
    Change-Id: I54dca0594ea22a15edb9758fdc2cb0606ee0eb9c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6654447 
    Reviewed-by: Ming-Ying Chung <mych@chromium.org> 
    Commit-Queue: Mingyu Lei <leimy@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1476166}

```

---

Files:

- M `chrome/browser/ui/file_system_access/file_system_access_ui_helpers.cc`
- M `chrome/browser/ui/file_system_access/file_system_access_ui_helpers_unittest.cc`

---

Hash: 4c368edb4f76d794c80a1971f1a36f6c417c2186  

Date:  Thu Jun 19 15:07:13 2025


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060615)*
