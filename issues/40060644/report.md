# use-after-free in BrowserCrashEventRouter

| Field | Value |
|-------|-------|
| **Issue ID** | [40060644](https://issues.chromium.org/issues/40060644) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>CrashReporting |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | xa...@google.com |
| **Created** | 2022-08-22 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**

## Details

`ConnectorsService` is a KeyedService, when it is created in [1], it creates `BrowserCrashEventRouter`. During the initialization of `BrowserCrashEventRouter`, it will add itself to the observers of ChromeBrowserCloudManagementController (when the `BrowserCrashEventsEnabled` feature is enabled) and store a KeyedService pointer of `RealtimeReportingClient` in [2] as `reporting_client_`.

When the `OnCloudReportingLaunched` callback triggered, it calls [3] and post the KeyedService pointer of `reporting_client_`. However, `UploadToReportingServer` will not be canceled, and when the `GetNewReports` executed and reply to the `UploadToReportingServer` during/after the profile shutdown, `reporting_client_` will be freed, causing UAF in `UploadToReportingServer` [5].

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/connectors_service.cc;l=582-588;drc=91e23cd891fa63eca6d32c16a30a977a87c9f587>

KeyedService\* ConnectorsServiceFactory::BuildServiceInstanceFor(  

content::BrowserContext\* context) const {  

return new ConnectorsService(  

context,  

std::make\_unique<ConnectorsManager>(  

std::make\_unique<BrowserCrashEventRouter>(context), // [1]  

ExtensionInstallEventRouter(context),  

user\_prefs::UserPrefs::Get(context), GetServiceProviderConfig(),  

base::FeatureList::IsEnabled(kEnterpriseConnectorsEnabled)));  

}

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/reporting/browser_crash_event_router.cc;l=206-216;drc=91e23cd891fa63eca6d32c16a30a977a87c9f587>

BrowserCrashEventRouter::BrowserCrashEventRouter(  

content::BrowserContext\* context) {  

reporting\_client\_ = RealtimeReportingClientFactory::GetForProfile(context); //[2]  

if (base::FeatureList::IsEnabled(kBrowserCrashEventsEnabled)) {  

#if !BUILDFLAG(IS\_CHROMEOS\_ASH)  

controller\_ = g\_browser\_process->browser\_policy\_connector()  

->chrome\_browser\_cloud\_management\_controller();  

controller\_->AddObserver(this);  

#endif // !BUILDFLAG(IS\_CHROMEOS\_ASH)  

}  

}

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/reporting/browser_crash_event_router.cc;l=200-203;drc=91e23cd891fa63eca6d32c16a30a977a87c9f587>

void BrowserCrashEventRouter::OnCloudReportingLaunched(  

enterprise\_reporting::ReportScheduler\* report\_scheduler) {  

ReportCrashes(); // [3]  

}

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/reporting/browser_crash_event_router.cc;l=194-197;drc=91e23cd891fa63eca6d32c16a30a977a87c9f587>

void BrowserCrashEventRouter::ReportCrashes() {  

DCHECK(reporting\_client\_);  

const absl::optional<ReportingSettings> settings =  

reporting\_client\_->GetReportingSettings();  

if (!settings.has\_value() ||  

settings->enabled\_event\_names.count(  

ReportingServiceSettings::kBrowserCrashEvent) == 0) {  

return;  

}  

// GetNewReports() may block since it has file I/O operations  

base::ThreadPool::PostTaskAndReplyWithResult(  

FROM\_HERE, {base::MayBlock()}, base::BindOnce(&GetNewReports),  

base::BindOnce(&UploadToReportingServer, reporting\_client\_,  

std::move(\*settings)));  

}

[5] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/connectors/reporting/browser_crash_event_router.cc;l=176;drc=91e23cd891fa63eca6d32c16a30a977a87c9f587>

void UploadToReportingServer(  

RealtimeReportingClient\* reporting\_client,  

ReportingSettings settings,  

std::vector[crashpad::CrashReportDatabase::Report](javascript:void(0);) reports) {  

DCHECK(reporting\_client);  

if (reports.empty()) {  

return;  

}

const std::string version = version\_info::GetVersionNumber();  

const std::string channel =  

version\_info::GetChannelString(chrome::GetChannel());  

const std::string platform = version\_info::GetOSType();

for (const auto& report : reports) {  

base::Value::Dict event;  

event.Set(kKeyChannel, channel);  

event.Set(kKeyVersion, version);  

event.Set(kKeyReportId, report.id);  

event.Set(kKeyPlatform, platform);  

event.Set(kKeyProfileUserName, reporting\_client->GetProfileUserName()); // [5] UAF here  

reporting\_client->ReportRealtimeEvent(  

ReportingServiceSettings::kBrowserCrashEvent, settings,  

std::move(event));  

}  

}

**Problem Description:**  

Browser UAF.

**Additional Comments:**

\*\*Chrome version: \*\* 107.0.5254.1 \*\*Channel: \*\* Canary

**OS:** Windows

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 27.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 62 B)
- [repro.diff](attachments/repro.diff) (text/plain, 3.0 KB)
- [1355252_min.mp4](attachments/1355252_min.mp4) (video/mp4, 8.5 MB)
- [linux_asan.txt](attachments/linux_asan.txt) (text/plain, 35.0 KB)
- [repro_linux.diff](attachments/repro_linux.diff) (text/plain, 4.0 KB)

## Timeline

### [Deleted User] (2022-08-22)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-08-22)

## Reproduction

To reproduce the UAF stably, please apply the `repro.diff` patch. The patch enables the `BrowserCrashEventsEnabled` feature and make the UAF reproduced more conveniently. 

Then host and visit the attached `poc.html`:
```
./chrome http://127.0.0.1:8000/poc.html
```

The ASan stack trace is attached as `asan.txt`.

## Bisect

This UAF is introduced by the commit https://chromium-review.googlesource.com/c/chromium/src/+/3814112

I think it impacted varies from version 107.0.5250.0 to the latest version 107.0.5254.1 (and dev channel). Moreover, it affects all platform except FUCHSIA and ChromeOS.

## Patch

There are many ways to avoid using the freed `reporting_client_` pointer:

1. We could make `UploadToReportingServer` function a member function, and use weak pointer when binding it to PostTaskAndReplyWithResult.

2. We could implment `Shutdown` to the `BrowserCrashEventRouter` and clean the `reporting_client_` pointer during shutdown. Then we could check the nullness of `reporting_client_` in UploadToReportingServer before use it. 

### ha...@gmail.com (2022-08-22)

uploaded the reproduction video due to the previous network error.

### sr...@google.com (2022-08-22)

Hmm, it looks legit of course but I fail at reproducing it.
I'm building chrome on linux at tags/107.0.5254.1 with your patch applied.
I'm using the following gn.args:
```
use_goma = true
is_asan = true
is_debug = false
```

And I'm starting at as:
./out/Asan/chrome --user-data-dir=/tmp/chrometmp 'http://localhost:1337/poc.html'

Any idea what could be the issue? Do I need to retry it or does it work 100% for you? (the patch looks like it should always work)

### sr...@google.com (2022-08-22)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-08-22)

[Comment Deleted]

### ha...@gmail.com (2022-08-23)

Reproduction for Linux: (the main reason previous Mac repro doesn't works on Linux is that the `GetNewReports` function returns empty reports from CrashReportDatabase)

1. Apply the attached patch (should works on both Linux and Windows) .
2. Open with two profile, let one of the profile visits poc.html

Tested on Linux with 107.0.5254.1 as well. Moreover, reproduce/exploit it on Mac is the most convenient/likely way.

### sr...@google.com (2022-08-23)

[Empty comment from Monorail migration]

### sr...@google.com (2022-08-23)

wanghaifan@ can you take a look at this?

[Monorail components: Internals>CrashReporting]

### [Deleted User] (2022-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xa...@google.com (2022-08-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4cf37076572ca8b63ed8af63c932276022d9e886

commit 4cf37076572ca8b63ed8af63c932276022d9e886
Author: Shanthanu Bhardwaj <xanth@google.com>
Date: Tue Aug 30 19:14:26 2022

Fix use-after-free bug in BrowserCrashEventRouter

- Make UploadToReportingServer a member function and bind with
  AsWeakPtr() to the BrowserCrashEventRouter.
- This should prevent any attempts to use the reporting_client after
  the reporting_client has been freed
- Move the write to latest_crash_report file from GetReports to
  UploadToReportingServer to ensure only uploaded reports are cleared.

Change-Id: I2357dabeca3cf3c46f9cf0d3f29ba3073c66e978
Bug: 1355252
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3863024
Commit-Queue: Shanthanu Bhardwaj <xanth@google.com>
Commit-Queue: Dominique Fauteux-Chapleau <domfc@chromium.org>
Reviewed-by: Dominique Fauteux-Chapleau <domfc@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1041112}

[modify] https://crrev.com/4cf37076572ca8b63ed8af63c932276022d9e886/chrome/test/BUILD.gn
[modify] https://crrev.com/4cf37076572ca8b63ed8af63c932276022d9e886/chrome/browser/enterprise/connectors/reporting/browser_crash_event_router.h
[modify] https://crrev.com/4cf37076572ca8b63ed8af63c932276022d9e886/chrome/browser/enterprise/connectors/reporting/browser_crash_event_router.cc


### xa...@google.com (2022-08-30)

[Comment Deleted]

### xa...@google.com (2022-08-30)

Issue fixed in main, need merge to 107

### xa...@google.com (2022-08-30)

- Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
  Browser UAF.

- What changes specifically would you like to merge? Please link to Gerrit.
  crrev.com/c/3863024

- Have the changes been released and tested on canary?
  Simple change and the fix has been tested on a local dev build.

- Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
  Yes, and the feature is hidden behind the `BrowserCrashEventsEnabled` feature flag that is not active in any release channel.

- If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
  Has been verified by me in dev and does not require manual verification.

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### xa...@google.com (2022-09-06)

[Empty comment from Monorail migration]

### xa...@google.com (2022-09-06)

Requesting merge to 106 because it is a major security+stability issue

### [Deleted User] (2022-09-06)

Merge review required: M106 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### xa...@google.com (2022-09-07)

1 Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
  Browser UAF will cause a crash.

2 What changes specifically would you like to merge? Please link to Gerrit.
  crrev.com/c/3863024

3 Have the changes been released and tested on canary?
  Simple change and the fix has been tested on a local dev build.

4 Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
  Yes, and the feature is hidden behind the `BrowserCrashEventsEnabled` feature flag that is not active in any release channel.

5 [Not a Chrome OS change]

6 If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
  Has been verified by me in dev and does not require manual verification.

### am...@chromium.org (2022-09-07)

updating as SI-None based on requiring BrowserCrashEventsEnabled flag that is not enabled, does not require merge 

### [Deleted User] (2022-09-08)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-09)

Congratulations! The VRP Panel has decided to award you $4,000 for this report of a moderately mitigated bug + $2,000 bisect bonus. Thank you for your efforts and reporting this issue to us!  

### am...@google.com (2022-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-16)

Merge approved: your change passed merge requirements and is auto-approved for M107. Please go ahead and merge the CL to branch 5304 (refs/branch-heads/5304) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-09-19)

[Bulk edit] This merge has been approved for M107, please help complete your merges asap, so the change can be included in this week's RC build for dev release.

### pb...@google.com (2022-09-20)

[Bulk Edit] This merge has been approved for M107, please help complete your merges asap, so the change can be included in this week's RC build for dev releases.

### [Deleted User] (2022-09-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-09-21)

[Bulk Edit] This merge has been approved for M107, please help complete your merges asap (before 3pm PST) today, so the change can be included in this week's RC build for dev releases.

We would like to get the changes as much Dev time as possible, so please complete your merges asap.


### [Deleted User] (2022-09-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-09-27)

[Bulk Edit] This merge has been approved for M107, please help complete your merges asap (before 3pm PST) today, so the change can be included in this week's RC build for dev/beta releases.

We would like to get the changes as much beta time as possible, so please complete your merges asap to M107 branch(go/chrome-branches).

### pb...@google.com (2022-10-05)

[Bulk Edit] Merge approved for M107 Branch:Refer to go/chrome-branches for branch info, Please goahead and get the changes cherrypick asap.

Note : We are cutting M107 Beta RC today i.e., Oct-05th, Please cherry pick the changes  before 1PM PST or earlier.


### pb...@google.com (2022-10-10)

[Bulk Edit] Your change has been approved for M107 Branch, please help complete your merges asap (before 3pm PST) today, so the change can be included in this week's RC build for beta releases.

We would like to get the changes as much beta time as possible, so please complete your merges asap to M107 branch(go/chrome-branches).


### am...@google.com (2022-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-20)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1355252?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060644)*
