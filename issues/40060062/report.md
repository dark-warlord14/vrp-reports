# Security: container-overflow in TabStripModel::AddToNewGroupImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40060062](https://issues.chromium.org/issues/40060062) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Journeys |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | mf...@google.com |
| **Created** | 2022-06-24 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**  

commit 7cfb85cef096c94f4d4255a712b05a53f87333f9

1. run `./out/ui/chrome --enable-features=UnifiedSidePanel,SidePanelJourneys --user-data-dir=/path/to/your/exist/profile`
2. open sidepanel and choose `Journeys`, then choose `Open all in new tab group`  
   
   Note that you need a old profle to have some journeys data.

**Problem Description:**  

You can see the video for more info.

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 11.9 KB)
- [video.webm](attachments/video.webm) (video/webm, 614.3 KB)

## Timeline

### [Deleted User] (2022-06-24)

[Empty comment from Monorail migration]

### me...@gmail.com (2022-06-24)

In function `HistoryClustersHandler::OpenVisitUrlsInTabGroup`[1],  it only insure that the size of visits is less than 32, but do not check whether it is 0, if we pass a visits with 0 element, overflow occurs.


[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/history_clusters/history_clusters_handler.cc;l=310;drc=a6f42f19fb2e519fe887ed47ba3c1775f1aa7cb8;bpv=1;bpt=1

patch suggestion:

diff --git a/chrome/browser/ui/webui/history_clusters/history_clusters_handler.cc b/chrome/browser/ui/webui/history_clusters/history_clusters_handler.cc
index 1d5cb9b5e07d..e528e81239b4 100644
--- a/chrome/browser/ui/webui/history_clusters/history_clusters_handler.cc
+++ b/chrome/browser/ui/webui/history_clusters/history_clusters_handler.cc
@@ -308,6 +308,9 @@ void HistoryClustersHandler::RemoveVisits(
 
 void HistoryClustersHandler::OpenVisitUrlsInTabGroup(
     std::vector<mojom::URLVisitPtr> visits) {
+  if (visits.empty()) {
+    return;
+  }
   const auto* browser = chrome::FindTabbedBrowser(profile_, false);
   if (!browser) {
     return;

### aj...@google.com (2022-06-24)

please take a look at this security report - I was not able to repro on a slightly older commit as the journeys panel didn't show me anything - I believe this is work in progress - if the flag isn't enabled for any users, please set Security_Impact-None to avoid unnecessary merger.

[Monorail components: UI>Browser>Journeys]

### [Deleted User] (2022-06-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-24)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-24)

[Empty comment from Monorail migration]

### mf...@chromium.org (2022-06-25)

This is a WIP. So not a security risk.

### mf...@chromium.org (2022-06-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-25)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mf...@chromium.org (2022-06-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-26)

[Empty comment from Monorail migration]

### aj...@google.com (2022-06-27)

mfacey - Severity is still Medium - the flag being disabled allows us to mark this as Impact-None. Thanks for working on a fix!

### gi...@appspot.gserviceaccount.com (2022-07-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0bad3b32fc165e80277cd4154ed31173996feeb4

commit 0bad3b32fc165e80277cd4154ed31173996feeb4
Author: Marlon Facey <mfacey@chromium.org>
Date: Mon Jul 11 22:21:59 2022

[journeys] Check for 0 visits when opening visits in tab group

When there is a zero length array passed into the OpenVisitUrlsInTabGroup there is an overflow error.

Bug: 1339140
Change-Id: Ib7ff0078adcbd4ec07c3b4f583422d45a5329ceb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3751720
Commit-Queue: Marlon Facey <mfacey@chromium.org>
Reviewed-by: Tommy Li <tommycli@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1022932}

[modify] https://crrev.com/0bad3b32fc165e80277cd4154ed31173996feeb4/chrome/browser/ui/webui/history_clusters/history_clusters_handler.cc


### mf...@chromium.org (2022-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-14)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-08-04)

Congratulations! The VRP Panel has decided to award you $2,000 for this report. The reward amount was decided upon based on this issue being significantly mitigated by not being remote exploitable and requiring significant user interaction. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1339140?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060062)*
