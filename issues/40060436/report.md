# Security: container-overflow in HistoryClustersHandler::OpenVisitUrlsInTabGroup

| Field | Value |
|-------|-------|
| **Issue ID** | [40060436](https://issues.chromium.org/issues/40060436) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Journeys |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | mf...@google.com |
| **Created** | 2022-07-29 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. download asan-linux-release-1029554.zip and unzip
2. run `./chrome --enable-features=SidePanelJourneys,UnifiedSidePanel --user-data-dir=//path/to/your/exist/profile`
3. open sidepanel and choose `Journeys`, then choose `Open all in new tab group`  
   
   Note that you need a old profle to have some journeys data.

**Problem Description:**  

This is similar to 1339140, but with different cause.

In Function `OpenVisitUrlsInTabGroup`[1], `tab_indices`(1) that passed into function `AddToNewGroup` could be empty even if `visits`(2) is not empty, because only the tab that can actually opened in this browser can be added into the `tab_indices`(3), if there are no tabs could meet this condition, then `tab_indices` is empty, causing overflow.

```
void HistoryClustersHandler::OpenVisitUrlsInTabGroup(  
    std::vector<mojom::URLVisitPtr> visits) {  
  // Sometimes WebUI passes an empty vector, and TabStripModel::AddToNewGroup  
  // requires a non-empty vector (Fixes https://crbug.com/1339140)  
  if (visits.empty()) {  // ==>(2)  
    return;  
  }  
  const auto\* browser = chrome::FindTabbedBrowser(profile_, false);  
  if (!browser) {  
    return;  
  }  
  
  // Hard cap the number of opened visits in a tab group to 32. It's a  
  // relatively high cap chosen fairly arbitrarily, because the user took an  
  // affirmative action to open this many tabs. And hidden visits aren't opened.  
  constexpr size_t kMaxVisitsToOpenInTabGroup = 32;  
  if (visits.size() > kMaxVisitsToOpenInTabGroup) {  
    visits.resize(kMaxVisitsToOpenInTabGroup);  
  }  
  
  auto\* model = browser->tab_strip_model();  
  std::vector<int> tab_indices;  
  tab_indices.reserve(visits.size());  
  auto\* opener = web_contents_.get();  
  for (const auto& visit_ptr : visits) {  
    auto\* opened_web_contents = opener->OpenURL(  
        content::OpenURLParams(visit_ptr->normalized_url, content::Referrer(),  
                               WindowOpenDisposition::NEW_BACKGROUND_TAB,  
                               ui::PAGE_TRANSITION_AUTO_BOOKMARK, false));  
  
    // The url may have opened a new window or clobbered the current one.  
    // Replace `opener` to be sure. `opened_web_contents` may be null in tests.  
    if (opened_web_contents) {  
      opener = opened_web_contents;  
    }  
  
    // Only add those tabs to a new group that actually opened in this browser.  
    const int tab_index = model->GetIndexOfWebContents(opened_web_contents);  
    if (tab_index != TabStripModel::kNoTab) { // ==>(3)  
      tab_indices.push_back(tab_index);  
    }  
  }  
  model->AddToNewGroup(tab_indices);  // ==>(1)  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/history_clusters/history_clusters_handler.cc;l=398>

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 11.9 KB)
- [poc.webm](attachments/poc.webm) (video/webm, 518.5 KB)

## Timeline

### [Deleted User] (2022-07-29)

[Empty comment from Monorail migration]

### bh...@google.com (2022-07-30)

Able to replicate in debug build, where the code hits the Dcheck. Please take a look.

[Monorail components: UI>Browser>Journeys]

### mf...@google.com (2022-08-01)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-08-30)

friendly ping~

### to...@chromium.org (2022-09-06)

[Empty comment from Monorail migration]

### mf...@google.com (2022-09-08)

Getting to this shortly @merc.ouc. 

### mf...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3556fdb66853c7b2b00ec458ab7217e789a0a7d7

commit 3556fdb66853c7b2b00ec458ab7217e789a0a7d7
Author: Marlon Facey <mfacey@chromium.org>
Date: Thu Sep 15 01:28:35 2022

[journeys] Check if tab_indices are empty

The indices passed to AddToNewGroup could still be empty even if there
are no visits. Instead I added the check to the AddToNewGroups function.

Bug: 1348464
Change-Id: I49a7d9d4dc37b25bbf96ba3c3e7d3fc2ff80c334
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3800492
Commit-Queue: Marlon Facey <mfacey@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1047247}

[modify] https://crrev.com/3556fdb66853c7b2b00ec458ab7217e789a0a7d7/chrome/browser/ui/webui/history_clusters/history_clusters_handler.cc


### mf...@google.com (2022-09-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-16)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-16)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-07)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of this heavily mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2022-12-23)

This issue was migrated from crbug.com/chromium/1348464?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1357462]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060436)*
