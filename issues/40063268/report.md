# Security: Heap-use-after-free in UserNotesPageHandler::GetNoteOverviews

| Field | Value |
|-------|-------|
| **Issue ID** | [40063268](https://issues.chromium.org/issues/40063268) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>SidePanel |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2023-02-27 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**  

commit at 6f19cbe2d8ad1fe1564b518ddfb4e55d9342ba25

1. apply change.txt and compile chromium with ASAN
2. start a server at the folder of poc.html
3. ./chrome --enable-features=UserNotes --user-data-dir=/tmp/noexist <http://127.0.0.1:8605/poc.html>
4. add a new note, then choose 'All notes'

**Problem Description:**  

##Analysis  

In function `UserNotesPageHandler::GetNoteOverviews`, a raw\_ptr `bookmark_model_` is passed into the callback directly. If we could free `bookmark_model_` before callback is invoked, UAF occurs.

```
void UserNotesPageHandler::GetNoteOverviews(const std::string& user_input,  
                                            GetNoteOverviewsCallback callback) {  
  service_->GetPowerOverviewsForType(  
      sync_pb::PowerBookmarkSpecifics::POWER_TYPE_NOTE,  
      base::BindOnce(  
          [](GetNoteOverviewsCallback callback, const GURL& current_tab_url,  
             bookmarks::BookmarkModel\* bookmark_model,  
             std::vector<std::unique_ptr<power_bookmarks::PowerOverview>>  
                 power_overviews) {  
            std::vector<side_panel::mojom::NoteOverviewPtr> results;  
            for (auto& power_overview : power_overviews) {  
              results.push_back(PowerOverviewToMojo(  
                  \*power_overview, current_tab_url, bookmark_model));  
            }  
            std::move(callback).Run(std::move(results));  
          },  
          std::move(callback), current_tab_url_, bookmark_model_));  
}  

```

Due to that the callback is invoked after `PostTaskAndReplyWithResult`, and the task is running on a threadpool, we could sleep the threadpoll and free the `bookmark_model_`, when callback invoking, UAF occurs.

```
void PowerBookmarkService::GetPowerOverviewsForType(  
    const sync_pb::PowerBookmarkSpecifics::PowerType& power_type,  
    PowerOverviewsCallback callback) {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  backend_task_runner_->PostTaskAndReplyWithResult(  
      FROM_HERE,  
      base::BindOnce(&PowerBookmarkBackend::GetPowerOverviewsForType,  
                     base::Unretained(backend_.get()), power_type),  
      std::move(callback));  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/side_panel/user_notes/user_notes_page_handler.cc;l=170;drc=0fd896e9b3aed71a39951d3c98fab6a5df6b55b0;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/power_bookmarks/core/power_bookmark_service.cc;l=76;drc=140889335cedb1fd7b08f99c85190e0bfcf2951e;bpv=1;bpt=0>

## Bisect

This UAF is introduced in this commit:  

<https://chromium-review.googlesource.com/c/chromium/src/+/4265690>

## Suggested patch

Please use a WeakPtr to pass the `bookmark_model_`.

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-02-27)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-02-27)

[Comment Deleted]

### sr...@google.com (2023-02-27)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>TopChrome>SidePanel]

### ad...@google.com (2023-02-27)

(I am a bot: this is an auto-cc on a security bug)

### ro...@chromium.org (2023-02-27)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/40f19a91100191e0d9cba8450b12729c9cd737ad

commit 40f19a91100191e0d9cba8450b12729c9cd737ad
Author: Yuheng Huang <yuhengh@chromium.org>
Date: Wed Mar 01 07:48:08 2023

Notes: fix uaf in UserNotesPageHandler

Use a weak pointer to bookmark model in UserNotesPageHandler since it
may outlive the callback in GetNoteOverviews().

Change-Id: Ifcba21eba4de52aeb5bf26489b1ba23d4e6d16d9
Bug: 1419773
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296975
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Commit-Queue: Yuheng Huang <yuhengh@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1111463}

[modify] https://crrev.com/40f19a91100191e0d9cba8450b12729c9cd737ad/chrome/browser/ui/webui/side_panel/user_notes/user_notes_page_handler.cc
[modify] https://crrev.com/40f19a91100191e0d9cba8450b12729c9cd737ad/chrome/browser/ui/webui/side_panel/user_notes/user_notes_page_handler.h


### yu...@chromium.org (2023-03-01)

@merc.ouc Thanks for the report. Could you verify if the above CL fixed the issue?

### [Deleted User] (2023-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-01)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-03-02)

I have verified that this CL fixed the issue, thanks for the quick fix :)

### am...@google.com (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Congratulations on another one, Weipeng! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-09)

This issue was migrated from crbug.com/chromium/1419773?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063268)*
