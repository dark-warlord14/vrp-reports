# Use-after-Free on BuildWebAppInternalsJson

| Field | Value |
|-------|-------|
| **Issue ID** | [40059505](https://issues.chromium.org/issues/40059505) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebAppInstalls |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gr...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2022-04-28 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. Apply the patch in [2]
2. python3 -m http.server 8000
3. out/asan/chrome --user-data-dir=/tmp/xxxx --load-extension=<path-to-the-extracted-poc-files>/extension "<http://localhost:8000/poc.html>"

**Problem Description:**

# Use-after-Free on BuildWebAppInternalsJson

## VULNERABILITY DETAILS

[0] The `profile` is posted to a separate sequence

[1] `profile` may be destroyed in UI, causing a UAF in BuildWebAppDiskStateJson callback.

```
void BuildWebAppInternalsJson(  
    Profile\* profile,  
    base::OnceCallback<void(base::Value root)> callback) {  
  auto\* provider = web_app::WebAppProvider::GetForLocalAppsUnchecked(profile);  
  base::Value root(base::Value::Type::LIST);  
  root.Append(BuildIndexJson());  
  root.Append(BuildInstalledWebAppsJson(\*provider));  
  root.Append(BuildPreinstalledWebAppConfigsJson(\*provider));  
  root.Append(BuildExternallyManagedWebAppPrefsJson(profile));  
  root.Append(BuildIconErrorLogJson(\*provider));  
  root.Append(BuildInstallProcessErrorLogJson(\*provider));  
#if BUILDFLAG(IS_MAC)  
  root.Append(BuildAppShimRegistryLocalStorageJson());  
#endif  
  base::ThreadPool::PostTaskAndReplyWithResult(  
      FROM_HERE, {base::TaskPriority::USER_VISIBLE, base::MayBlock()},  
      base::BindOnce(&BuildWebAppDiskStateJson, profile, std::move(root)), //---->[0] posttask to ThreadPool  
      std::move(callback));  
}  

```
```
base::Value BuildWebAppDiskStateJson(Profile\* profile, base::Value root) {  
  base::Value file_list(base::Value::Type::LIST);  
  base::FileEnumerator files(web_app::GetWebAppsRootDirectory(profile), true,  
                             base::FileEnumerator::FILES);  
  for (base::FilePath current = files.Next(); !current.empty();  
       current = files.Next()) {  
    file_list.Append(current.AsUTF8Unsafe());  
  }  
  base::Value section(base::Value::Type::DICTIONARY);  
  section.SetKey(kWebAppDirectoryDiskState, std::move(file_list));  
  root.Append(std::move(section));  
  return root;  
}  
  
base::FilePath GetWebAppsRootDirectory(Profile\* profile) {  
  return profile->GetPath().Append(chrome::kWebAppDirname); //---->[1] use here!!  
}  

```

[2] Because it needs to compete with the ui thread so I wrote a patch to help trigger this vulnerability easily

```
base::Value BuildWebAppDiskStateJson(Profile\* profile, base::Value root) {  
+ LOG(ERROR)<<"BuildWebAppDiskStateJson START!!";  
+ sleep(5);  
+ LOG(ERROR)<<"BuildWebAppDiskStateJson END!!";  
  base::Value file_list(base::Value::Type::LIST);  
  base::FileEnumerator files(web_app::GetWebAppsRootDirectory(profile), true,  
                             base::FileEnumerator::FILES);  
  for (base::FilePath current = files.Next(); !current.empty();  
       current = files.Next()) {  
    file_list.Append(current.AsUTF8Unsafe());  
  }  
  base::Value section(base::Value::Type::DICTIONARY);  
  section.SetKey(kWebAppDirectoryDiskState, std::move(file_list));  
  root.Append(std::move(section));  
  return root;  
}  

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/web_app_internals/web_app_internals_source.cc;l=267;drc=1d8b1965b96c021ee069a3ebda38be7aaf8a5786>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/web_app_internals/web_app_internals_source.cc;drc=1d8b1965b96c021ee069a3ebda38be7aaf8a5786;l=235>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/web_applications/web_app_utils.cc;drc=1d8b1965b96c021ee069a3ebda38be7aaf8a5786;l=201>

## Reproduce

1. Apply the patch in [2]
2. python3 -m http.server 8000
3. out/asan/chrome --user-data-dir=/tmp/xxxx --load-extension=<path-to-the-extracted-poc-files>/extension "<http://localhost:8000/poc.html>"

## Credit

Yuntao You (@GraVity0) of Bytedance Wuheng Lab

**Additional Comments:**

\*\*Chrome version: \*\* 100.0.4896.127 \*\*Channel: \*\* Stable

**OS:** Linux

## Attachments

- [asan](attachments/asan) (text/plain, 46.2 KB)
- [extension.zip](attachments/extension.zip) (application/octet-stream, 2.7 KB)
- [poc.html](attachments/poc.html) (text/plain, 38 B)
- [uaf.webm](attachments/uaf.webm) (video/webm, 3.1 MB)
- [new-extension.zip](attachments/new-extension.zip) (application/octet-stream, 1.5 KB)

## Timeline

### dt...@chromium.org (2022-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-28)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-29)

Thanks for the report. +dmurph who added this in https://chromium-review.googlesource.com/c/chromium/src/+/3154686

Setting Medium severity as this is reasonably tricky to trigger, but otherwise is a UaF in the browser process.

[Monorail components: UI>Browser>WebAppInstalls]

### [Deleted User] (2022-04-29)

[Empty comment from Monorail migration]

### gr...@gmail.com (2022-04-29)

I'm sorry to not add  video yesterday in time.
could you please raise the level to high？because once you install a malicious plugin for chrome it triggers UAF.
You can use this new plugin to quickly trigger uaf, and if you have problems reproducing you can ask me.

### do...@chromium.org (2022-04-29)

Reassigning to dmurph.

Our severity guidelines give an example of memory corruption that needs an extension to be installed as being Medium severity[1]. That coupled with needing to be on a chrome:// page warrants Medium I think.

1. https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-medium-severity

### gr...@gmail.com (2022-04-29)

Thanks for your reply, please help to fix this bug

### [Deleted User] (2022-04-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a325c6cb4b612611239143f80067782589632676

commit a325c6cb4b612611239143f80067782589632676
Author: Daniel Murphy <dmurph@google.com>
Date: Thu May 05 20:09:17 2022

[dPWA] Update internals page to have better display format

Screenshot:
https://screenshot.googleplex.com/4duw3zSrRsqYSXS.png

Bug: 1320624
Change-Id: Ifde8a2d1bade9f0f8fc674b5d4487754c8a00c91
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3626492
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Phillis Tang <phillis@chromium.org>
Auto-Submit: Daniel Murphy <dmurph@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1000056}

[modify] https://crrev.com/a325c6cb4b612611239143f80067782589632676/chrome/browser/ui/webui/web_app_internals/web_app_internals_source.cc


### dm...@chromium.org (2022-05-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

Requesting merge to beta M102 because latest trunk commit (1000056) appears to be after beta branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-11)

Merge review required: M102 is already shipping to beta.

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

### am...@chromium.org (2022-05-14)

As this fix has over a week of canary coverage and no issues seem to be exhibiting during that time, approving for M102 merge; please ensure there are no issues or concerns with backmerging this fix to M102 and merge to branch 5005 nlt EOD Monday 16 May so this fix can be included in the M102 stable cut --thank you! 

### sr...@google.com (2022-05-16)

Please complete your merge to M102 ASAP, M102 RC cut is tomorrow  ( May 17) if you want your change to be part of the M102 stable promotion pls complete merges before EOD today PST ( May 16)

### gi...@appspot.gserviceaccount.com (2022-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5c2ca1e929c7b33f152b28b42ddb9b40fe69ba05

commit 5c2ca1e929c7b33f152b28b42ddb9b40fe69ba05
Author: Daniel Murphy <dmurph@google.com>
Date: Mon May 16 18:26:10 2022

[dPWA] Update internals page to have better display format

Screenshot:
https://screenshot.googleplex.com/4duw3zSrRsqYSXS.png

(cherry picked from commit a325c6cb4b612611239143f80067782589632676)

Bug: 1320624
Change-Id: Ifde8a2d1bade9f0f8fc674b5d4487754c8a00c91
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3626492
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Phillis Tang <phillis@chromium.org>
Auto-Submit: Daniel Murphy <dmurph@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1000056}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3648910
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#761}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/5c2ca1e929c7b33f152b28b42ddb9b40fe69ba05/chrome/browser/ui/webui/web_app_internals/web_app_internals_source.cc


### am...@google.com (2022-05-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-24)

Congratulations, Yuntao You! The VRP Panel has decided to award you $5,000 for this report, due to the malicious extension required and this issue's reliance on profile destruction. A member of our finance team will reach out to you to begin payment systems enrollment and arrange for payment. Thank you for your efforts and reporting this issue to us! 

### am...@chromium.org (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@google.com (2022-05-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1320624?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059505)*
