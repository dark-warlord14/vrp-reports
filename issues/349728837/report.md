# UAF in URLDownloader::DeleteCompletionHandler

| Field | Value |
|-------|-------|
| **Issue ID** | [349728837](https://issues.chromium.org/issues/349728837) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | iOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-06-27 |
| **Bounty** | $1,000.00 |

## Description


RLDownloader::DeleteCompletionHandler bind as unretained,and RLDownloader owned by ReadingListDownloadService

same as https://chromium-review.googlesource.com/c/chromium/src/+/5654812

void URLDownloader::HandleNextTask() {
  if (working_ || tasks_.empty()) {
    return;
  }
  working_ = true;

  Task task = tasks_.front();
  tasks_.pop_front();
  GURL url = task.second;
  base::FilePath directory_path =
      reading_list::OfflineURLDirectoryAbsolutePath(base_directory_, url);

  if (task.first == DELETE) {
    task_tracker_.PostTaskAndReplyWithResult(
        task_runner_.get(), FROM_HERE,
        base::BindOnce(&base::DeletePathRecursively, directory_path),
        base::BindOnce(&URLDownloader::DeleteCompletionHandler,
                       base::Unretained(this), url));
  } else if (task.first == DOWNLOAD) {
    DCHECK(!distiller_);
    OfflinePathExists(directory_path,
                      base::BindOnce(&URLDownloader::DownloadURL,
                                     base::Unretained(this), url));
  }
}


void URLDownloader::OnURLLoadComplete(const GURL& original_url,
                                      base::FilePath response_path) {
  // At the moment, only pdf files are downloaded using URLFetcher.
  DCHECK(mime_type_ == "application/pdf");
  base::FilePath path = reading_list::OfflinePagePath(
      original_url_, reading_list::OFFLINE_TYPE_PDF);
  std::string mime_type;
  if (url_loader_->ResponseInfo()) {
    mime_type = url_loader_->ResponseInfo()->mime_type;
  }
  if (response_path.empty() || mime_type != mime_type_) {
    return DownloadCompletionHandler(original_url_, "", path, ERROR);
  }

  task_tracker_.PostTaskAndReplyWithResult(
      task_runner_.get(), FROM_HERE,
      base::BindOnce(&URLDownloader::SavePDFFile, base::Unretained(this),
                     response_path),
      base::BindOnce(&URLDownloader::DownloadCompletionHandler,
                     base::Unretained(this), original_url, "", path));

  url_loader_.reset();
}


fix  

use weakptr replace unretained




## Timeline

### el...@chromium.org (2024-06-27)

Security shepherd: thanks for the report; I confirmed the bug by code inspection. Over to you, olivierrobin@ :)

### ha...@gmail.com (2024-06-28)

bisect <https://codereview.chromium.org/2204083003>

### ap...@google.com (2024-06-28)

Project: chromium/src
Branch: main

commit 37505e874977ddd0270d3258887c827222abe5d9
Author: Olivier Robin <olivierrobin@google.com>
Date:   Fri Jun 28 10:25:09 2024

    Fix potential UAF in ios/ReadingList
    
    Move all off-main-thread function out of the object to avoid
    concurrent access or usage after deletion.
    Guard all reply to main thread with WeakPtr.
    
    Fixed: 349728837
    Change-Id: I6e20501f393cc51c5e71cacfb92066b7bc07e45f
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5663355
    Reviewed-by: Quentin Pubert <qpubert@google.com>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Commit-Queue: Olivier Robin <olivierrobin@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1320859}

M       ios/chrome/browser/dom_distiller/model/distiller_viewer.cc
M       ios/chrome/browser/dom_distiller/model/distiller_viewer.h
M       ios/chrome/browser/reading_list/model/offline_page_tab_helper.h
M       ios/chrome/browser/reading_list/model/offline_page_tab_helper.mm
M       ios/chrome/browser/reading_list/model/reading_list_web_state_observer.h
M       ios/chrome/browser/reading_list/model/reading_list_web_state_observer.mm
M       ios/chrome/browser/reading_list/model/url_downloader.h
M       ios/chrome/browser/reading_list/model/url_downloader.mm
M       ios/chrome/browser/reading_list/model/url_downloader_unittest.mm

https://chromium-review.googlesource.com/5663355


### pe...@google.com (2024-06-28)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-28)

Requesting merge to stable (M126) because latest trunk commit (1320859) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1320859) appears to be after beta branch point (1313161).
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### ol...@chromium.org (2024-06-28)

Discussed with ellyjones, and we thought that merging in 127 only was probably best.

Which CLs should be backmerged? (Please include Gerrit links.)
 https://chromium-review.googlesource.com/c/chromium/src/+/5663355

Has this fix been verified on Canary to not pose any stability regressions?
tested on trunk. Will test on canary on Monday. Note that there is no POC for crashing.

Does this fix pose any potential non-verifiable stability risks?
The CL refactors a lot of code, so there is a risk in CPing it to stable

Does this fix pose any known compatibility risks?
No

Does it require manual verification by the test team? If so, please describe required testing.
Yes, Test Reading list

### pe...@google.com (2024-06-29)

Merge review required: M127 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), alonbajayo (ChromeOS), danielyip (Desktop)

### pe...@google.com (2024-06-29)

Merge review required: M126 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), ceb (ChromeOS), srinivassista (Desktop)

### ol...@chromium.org (2024-07-01)

Why does your merge fit within the merge criteria for these milestones?
This is potentially a security issue, need to CP the fix

What changes specifically would you like to merge? Please link to Gerrit.
 https://chromium-review.googlesource.com/c/chromium/src/+/5663355

Have the changes been released and tested on canary?
Yes

Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No

If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
May be useful to test reading list again (note that EG tests should already cover it)

### am...@chromium.org (2024-07-01)

This is a speculative issue, based on this code, it seems doubtful this issue would be remotely exploitable and would require a fair amount of user interaction and potentially shutdown to trigger. Based on this and that M127 Stable RC is being cut week after next following release freeze, given the size of this change, I don't presently concur with backmerging this fix to M127. 
We are presently in release freeze until this week and next, so there's not an opportunity to get this fix on early beta to see how performance, stability, or usability may be affected.
Since this is iOS, we don't have canary data either, so there's not time -- in terms of more bake time-- that would provide data to support backmerging. 

Therefore, at this time, I'm going to decline backmerge to M126 and M127 for this issue and we can plan on shipping this fix in M128 for now.
Please let me know if you have any issues with this decision. 

### sp...@google.com (2024-07-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
speculative report of highly mitigated memory corruption in a non-sandboxed process 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-03)

Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2024-10-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/349728837)*
