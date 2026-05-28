# Security: Heap-use-after-free in UploadToReportingServer

| Field | Value |
|-------|-------|
| **Issue ID** | [40065507](https://issues.chromium.org/issues/40065507) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | me...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2023-06-08 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. apply change.diff and compile Chromium with ASAN enabled
2. run `./chrome --user-data-dir=/tmp/noexist --enable-chrome-browser-cloud-management http://127.0.0.1:8605/poc.html`
3. wait until crash

**Problem Description:**

1. Analysis

In function `ReportCrashes`, there is a raw ptr `reporting_client`[1] that is passed into the Reply Callback directly. If we could free the `reporting_client` before this callback is invoked[2], UAF occurs.

```
void ReportCrashes() {  
  CrashReportingContext\* context = CrashReportingContext::GetInstance();  
  if (!context->HasActiveProfile()) {  
    return;  
  }  
  RealtimeReportingClient\* reporting_client =  
      context->GetCrashReportingClient();  
  VLOG(1) << "enterprise.crash_reporting: crash reporting enabled: "  
          << (reporting_client != nullptr);  
  if (!reporting_client) {  
    g_browser_process->local_state()->ClearPref(kLatestCrashReportCreationTime);  
    return;  
  }  
  VLOG(1) << "enterprise.crash_reporting: checking for unreported crashes";  
  time_t latest_creation_time =  
      GetLatestCrashReportTime(g_browser_process->local_state());  
  if (latest_creation_time == 0) {  
    latest_creation_time = base::Time::Now().ToTimeT();  
    SetLatestCrashReportTime(g_browser_process->local_state(),  
                             latest_creation_time);  
  }  
  base::ThreadPool::PostTaskAndReplyWithResult(  
      FROM_HERE, {base::MayBlock()},  
      base::BindOnce(&GetNewReports, latest_creation_time),  
      base::BindOnce(&UploadToReportingServer, reporting_client,   // `reporting_client` is a raw ptr and passed into callback directly  
                     g_browser_process->local_state()));  
}  

```
```
void UploadToReportingServer(  
    RealtimeReportingClient\* reporting_client,  
    PrefService\* local_state,  
    std::vector<crashpad::CrashReportDatabase::Report> reports) {  
  VLOG(1) << "enterprise.crash_reporting: " << reports.size()  
          << " crashes to report";  
  if (reports.empty()) {  
    return;  
  }  
  absl::optional<ReportingSettings> settings =  
      reporting_client->GetReportingSettings();  // `reporting_client` is used after freed  
  [...]  
}  

```

Because that this Reply Callback is invoked after a ThreadPool Post, we can easily trigger this UAF by slowing the call to function `GetNetReports`[3]. Besides, to simulate a normal return value of `GetNetReports`, I patch the code to return a std::vector[crashpad::CrashReportDatabase::Report](javascript:void(0);), this will not influence the logic of code.

```
std::vector<crashpad::CrashReportDatabase::Report> GetNewReports(  
    time_t latest_creation_time) {  
  auto crashpad_path = crash_reporter::GetCrashpadDatabasePath();  
  if (!crashpad_path) {  
    VLOG(1) << "enterprise.crash_reporting: no valid crashpad path";  
    return {};  
  }  
  std::unique_ptr<crashpad::CrashReportDatabase> database =  
      crashpad::CrashReportDatabase::InitializeWithoutCreating(\*crashpad_path);  
  if (!database) {  
    VLOG(1) << "enterprise.crash_reporting: failed to fetch crashpad db";  
    return {};  
  }  
  return GetNewReportsFromDatabase(latest_creation_time, database.get());  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/reporting/crash_reporting_context.cc;l=94;drc=4928fbb26b8f7e2ecc5f7d83db337f394fa67a48;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/reporting/crash_reporting_context.cc;l=161;drc=4928fbb26b8f7e2ecc5f7d83db337f394fa67a48;bpv=0;bpt=0>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/reporting/crash_reporting_context.cc;l=54;drc=4928fbb26b8f7e2ecc5f7d83db337f394fa67a48;bpv=0;bpt=0>

2. Bisect

This problem is introduced in this commit: 4107741a4a010218f7de76429cba7a43f776b51f  

<https://chromium-review.googlesource.com/c/chromium/src/+/4335176>

According to the chromiumdash, this proble affects DEV version after 116.0.5791.0.

3. Suggested Patch

Use a WeakPtr or a ScopedRefPtr to observe the lifetime of `reporting_client`

**Additional Comments:**  

To get a `reporting_client`, you need to set a preference to pass the check in [4], I also patch this part of code for convenience. This will NOT influence the logic.

```
RealtimeReportingClient\* CrashReportingContext::GetCrashReportingClient()  
    const {  
  for (auto& it : active_profiles_) {  
    Profile\* profile = it.second;  
    RealtimeReportingClient\* reporting_client =  
        RealtimeReportingClientFactory::GetForProfile(profile);  
    if (!reporting_client) {  
      continue;  
    }  
    absl::optional<ReportingSettings> settings =  
        reporting_client->GetReportingSettings();  
    if (settings.has_value() &&  
        settings->enabled_event_names.count(  
            ReportingServiceSettings::kBrowserCrashEvent) != 0 &&  
        !settings->per_profile) {  
      return reporting_client;  
    }  
  }  
  return nullptr;  
}  

```

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/reporting/crash_reporting_context.cc;l=210;drc=4928fbb26b8f7e2ecc5f7d83db337f394fa67a48;bpv=0;bpt=0>

\*\*Chrome version: \*\* 116.0.5791.0 \*\*Channel: \*\* Dev

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 91 B)
- [change.diff](attachments/change.diff) (text/plain, 2.4 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 28.7 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 5.1 MB)

## Timeline

### [Deleted User] (2023-06-08)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-06-08)

I repro this on MAC, note that this also affects Win and Linux.

Upload the asan and video.

### aj...@google.com (2023-06-08)

could you outline how the reporting_client might get free'd in normal operation?

### aj...@google.com (2023-06-08)

[Empty comment from Monorail migration]

[Monorail components: Enterprise]

### [Deleted User] (2023-06-08)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-06-09)

re c#3
You can free it by closing the browser.

### aj...@google.com (2023-06-09)

Thanks - setting a Medium as this is somewhat mitigated by shutdown and a race.

### [Deleted User] (2023-06-09)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@gmail.com (2023-06-14)

Hello, any update?

### al...@chromium.org (2023-06-15)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/770e7fc56b9d9e72e613caf56c3ade6ae316dbd5

commit 770e7fc56b9d9e72e613caf56c3ade6ae316dbd5
Author: Nasser Al-shawwa <alshawwa@chromium.org>
Date: Fri Jun 16 14:35:17 2023

Use WeakPtr to track lifetime of reporting_client

Bug: 1453209
Change-Id: I3ed10356f842b399d8cfbcedd0999cad19370dd0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4615195
Commit-Queue: Nasser Al-shawwa <alshawwa@chromium.org>
Reviewed-by: Dominique Fauteux-Chapleau <domfc@chromium.org>
Code-Coverage: Findit <findit-for-me@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1158819}

[modify] https://crrev.com/770e7fc56b9d9e72e613caf56c3ade6ae316dbd5/chrome/browser/enterprise/connectors/reporting/realtime_reporting_client.cc
[modify] https://crrev.com/770e7fc56b9d9e72e613caf56c3ade6ae316dbd5/chrome/browser/enterprise/connectors/reporting/realtime_reporting_client.h
[modify] https://crrev.com/770e7fc56b9d9e72e613caf56c3ade6ae316dbd5/chrome/browser/enterprise/connectors/reporting/crash_reporting_context.h
[modify] https://crrev.com/770e7fc56b9d9e72e613caf56c3ade6ae316dbd5/chrome/browser/enterprise/connectors/reporting/crash_reporting_context_unittest.cc
[modify] https://crrev.com/770e7fc56b9d9e72e613caf56c3ade6ae316dbd5/chrome/browser/enterprise/connectors/reporting/crash_reporting_context.cc


### al...@chromium.org (2023-06-16)

[Empty comment from Monorail migration]

### al...@chromium.org (2023-06-16)

Issue was fixed by using weakptr to track the lifetime of reporting_client

### [Deleted User] (2023-06-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

Not requesting merge to dev (M116) because latest trunk commit (1158819) appears to be prior to dev branch point (1160321). If this is incorrect, please replace the Merge-NA-116 label with Merge-Request-116. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-06-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-24)

Congratulations, Krace! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-30)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-06)

Thanks for the addressing this issue so quickly, alshawwa@. This issue was introduced in 116 and this fix in C#14 was landed in 116, so no merges are needed here. Removing the merge approval label to stop the nagging from our ever-persistent bot. 

### [Deleted User] (2023-09-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1453209?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065507)*
