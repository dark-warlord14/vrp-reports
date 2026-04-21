# Security: UAF in AcquireFileAccessPermissionDoneForScheduleDownload

| Field | Value |
|-------|-------|
| **Issue ID** | [40064789](https://issues.chromium.org/issues/40064789) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Network, UI>Browser>Offline |
| **Platforms** | Android |
| **Reporter** | ss...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2023-05-24 |
| **Bounty** | $30,000.00 |

## Description

redacted

## Attachments

- [crashlog](attachments/crashlog) (text/plain, 18.3 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 11.1 KB)
- [server.py](attachments/server.py) (text/plain, 667 B)
- [poc.html](attachments/poc.html) (text/plain, 214 B)
- [vuln.html](attachments/vuln.html) (text/plain, 506 B)
- [crash.log](attachments/crash.log) (text/plain, 20.2 KB)

## Timeline

### [Deleted User] (2023-05-24)

[Empty comment from Monorail migration]

### wf...@chromium.org (2023-05-24)

Hi thanks for your bug, it looks like an interesting find. This requires enable_offline_pages which is Android only, it seems.

I'm curious about the BrowserPrioritizeNativeWork feature, does having this feature off make the bug unexploitable, or just make the race easier to happen?

Further triage will happen shortly.

[Monorail components: UI>Browser>Offline]

### wf...@chromium.org (2023-05-24)

it appears from code inspection that AcquireFileAccessPermissionDoneForScheduleDownload would return early without hitting the UAF in this case (in the production code) are you able to repro this or hit an asan check without the browser patch (but with feature enabled) on e.g. an asan build?

### wf...@chromium.org (2023-05-24)

This is old code - setting milestone 105, if true this is a High sev since it requires a compromised renderer. I am still assessing whether this affects the production version of Chrome (answers from the reporter will help)

### [Deleted User] (2023-05-24)

[Empty comment from Monorail migration]

### wf...@chromium.org (2023-05-24)

I can't use your poc because it has blink reaching into chrome/common/net/net_error_page_support.mojom.h and I get a link error, as there's no gn dep. I need answers to my questions in #2 and #3 to make further progress triaging this issue.

### ss...@gmail.com (2023-05-25)

Re #2:
The BrowserPrioritizeNativeWork feature just makes the race easier to happen. When the feature is enabled, even a click on the empty area in browser will prioritize the native task.
As for this issue, the dtor of WebContents is a native task and the AcquireFileAccessPermissionDoneForScheduleDownload is a Chromium task. Without this feature, the native task will not be scheduled until the chromium tasks are fully processed.

Re #3: 
I'm working on an ASAN/HWASAN build on Android 114.0.5735.53 but can't launch Chromium successfully, seems like there is an UAF in the ASAN-related library which causes the Chromium startup phase to fail :(
I'll continue to work on the ASAN log and I attach the `carsh.log` with symbolized stack backtrace, hope this can help to triage.

To clarify, the first check[1] will not lead to a `return` according to my local testing. There is a READ operation on WebContents at `OfflinePageTabHelper::FromWebContents(web_contents);` which should be caught by the ASAN build.

```
void AcquireFileAccessPermissionDoneForScheduleDownload(
    content::WebContents* web_contents,
    const std::string& name_space,
    const GURL& url,
    OfflinePageUtils::DownloadUIActionFlags ui_action,
    const std::string& request_origin,
    bool granted) {
  if (!granted) // [1]
    return;
  OfflinePageTabHelper* tab_helper =
      OfflinePageTabHelper::FromWebContents(web_contents); // will call to [1]
  if (!tab_helper)
    return;
  tab_helper->ScheduleDownloadHelper(web_contents, name_space, url, ui_action,
                                     request_origin);
}
```

[1] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:base/supports_user_data.cc;drc=4ff9fcc5abab42ce586d3637b5a3a75288dd620f;l=29

### ss...@gmail.com (2023-05-25)

Re #6:
The poc works fine on 616c4423ccf20df85b6d314f244b202c5a925105.
Does the `is_component_build` lead to the link error?
Here is my `args.gn` :
```
target_os = "android"
target_cpu = "arm64"
is_asan = false
is_debug = false
dcheck_always_on = false
symbol_level = 2
is_component_build = false
```


### [Deleted User] (2023-05-26)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### xi...@chromium.org (2023-06-03)

Thanks for the detailed report! I found an old crash bug https://crbug.com/847919 that has the exact signature and there are still occasional crashes recently, so I think this UaF can indeed be triggered in the wild. +jianli@ based on the git history. Thanks!

### xi...@chromium.org (2023-06-03)

[Empty comment from Monorail migration]

### ji...@chromium.org (2023-06-05)

We're not working on offline_pages. Robert, could you please help find out who is the right person to look into this? Thanks.

### ro...@chromium.org (2023-06-05)

over to Tarun for triage and assignment

### [Deleted User] (2023-06-07)

tbansal: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tb...@chromium.org (2023-06-14)

[Empty comment from Monorail migration]

### tb...@chromium.org (2023-06-16)

I was discussing this with the offline team (dimich@, carlosk@) and it was not clear to us if it should be fixed in the navigation stack or the offline stack? The rationale for the former is that it seems there is some fundamental 500ms gap between the browser classifying the page as error and renderer actually updating.

Also cc'ing navigation experts: creis@, dcheng@


### an...@chromium.org (2023-06-30)

creis@, dcheng@ - polling for your thoughts regarding c#17. Thanks! - secondary shepherd

### cr...@chromium.org (2023-06-30)

Sorry for missing this-- in the future, please reach out to us directly if you have a question blocking a security fix, especially if we don't respond promptly to a question on the bug.

Looking at the report, it seems there are several issues needing fixes, but I don't think any of them are in the navigation code.  On the navigation side, it's fundamental that a WebContents may have multiple renderer processes sending IPC messages to the browser process, including the previous page during its pending delete phase.  This means you cannot safely assume that an IPC message comes from the current main frame RenderFrameHost.

The issues I noticed that probably require fixes:

1)  OfflinePageUtils::ScheduleDownload passes a WebContents raw pointer to a callback, with no guarantee it is valid when the callback runs.  This causes the UAF in  AcquireFileAccessPermissionDoneForScheduleDownload.  Could a WebContentsGetter be passed instead, similar to the DownloadControllerBase::AcquireFileAccessPermission call in  OfflinePageUtils::AcquireFileAccessPermission (https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:chrome/browser/offline_pages/offline_page_utils.cc;drc=b73134cfcce34a13f25202d077c0aa9dc03b662e;l=375)?

2)  NetErrorTabHelper::DownloadPageLater() assumes the IPC comes from the renderer process for the last committed NavigationEntry, but there is no guarantee for that.  Instead, NetErrorTabHelper probably needs to keep track of which RenderFrameHost is sending the IPC.  I'm not familiar with that code or who works on it, but it appears to be binding the interface to multiple RenderFrameHosts (e.g., NetErrorTabHelper::BindNetErrorPageSupport).  It should be able to keep track of the RFH and tell whether RenderFrameHost::IsErrorDocument() or not (rather than asking about the last committed NavigationEntry).

3) I'm surprised a normal renderer process is allowed to use the DownloadPageLater Mojo interface at all, if it's only meant for error pages in an error page specific process.  Do we grant it to normal renderer processes because of subframe error pages?  Maybe we can avoid that once https://crbug.com/chromium/1092524 is fixed?  Adding nasko@ for FYI.

At any rate, the highest priority fix is the raw pointer in the callback, but the NetErrorTabHelper fix seems worthwhile as well.

[Monorail components: Internals>Network]

### an...@chromium.org (2023-06-30)

Thanks for your analysis creis@! 
tbansal@, jianli@: can one of you take a look at fixing item 1 in c#19?
cc'ing ricea@, bashi@ for item 2 (as owners) - please redirect if necessary.   

### ad...@google.com (2023-06-30)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-07-01)

tbansal: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-11)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2023-07-12)

Adding CCs. bengr - is there someone who might have cycles to take a look at this? Thanks.

### [Deleted User] (2023-07-23)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9475c8dfe501a4893e727486c69810e6f5fd27f7

commit 9475c8dfe501a4893e727486c69810e6f5fd27f7
Author: Tarun Bansal <tbansal@google.com>
Date: Fri Jul 28 17:52:17 2023

[Offline] Pass WebContentsGetter instead of WebContents

OfflinePageUtils::ScheduleDownload passes a WebContents
raw pointer to a callback, with no guarantee it is valid
when the callback runs. This CL changes the logic to pass a
WebContentsGetter instead of WebContents.

Bug: 1448548
Change-Id: Ibaefdae8eae61139dcb6eae8365e9d3ce1c32f9c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4709689
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Tarun Bansal <tbansal@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1176718}

[modify] https://crrev.com/9475c8dfe501a4893e727486c69810e6f5fd27f7/chrome/browser/offline_pages/offline_page_utils.cc


### tb...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

Merge review required: M116 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-08-03)

Thank you for landing the fix for this high-severity issue. In the future, please close security bugs as fixed once the resolving CL has landed. This allows the bot to put the appropriate labels and get added to the security merge review queue more immediately. 

116 merge approved for https://crrev.com/c/4709689 -- please merge this fix to branch 5845 at your earliest convenience / before EOD Monday, 7 August so this fix can be included in M116 Stable cut -- thank you 

### [Deleted User] (2023-08-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-08-07)

Hi robertogden@ -- I see that tbansal@ is currently out, would you be able to backmerge this fix in their absence? 
Or dcheng@ would you be able to since you reviewed this fix? 
It should be backmerged by EOD today so this fix can be included in the M116 Stable RC being cut tomorrow -- thank you! 

### ro...@chromium.org (2023-08-07)

on it!

### ro...@chromium.org (2023-08-07)

in the cq now - https://crrev.com/c/4755652

### gi...@appspot.gserviceaccount.com (2023-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dd1d15391999ee8b4f212866652b16c7b6be7fee

commit dd1d15391999ee8b4f212866652b16c7b6be7fee
Author: Tarun Bansal <tbansal@google.com>
Date: Mon Aug 07 19:06:59 2023

[Offline] Pass WebContentsGetter instead of WebContents

OfflinePageUtils::ScheduleDownload passes a WebContents
raw pointer to a callback, with no guarantee it is valid
when the callback runs. This CL changes the logic to pass a
WebContentsGetter instead of WebContents.

(cherry picked from commit 9475c8dfe501a4893e727486c69810e6f5fd27f7)

Bug: 1448548
Change-Id: Ibaefdae8eae61139dcb6eae8365e9d3ce1c32f9c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4709689
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Commit-Queue: Tarun Bansal <tbansal@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1176718}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4755652
Commit-Queue: Robert Ogden <robertogden@chromium.org>
Commit-Queue: Sophie Chang <sophiechang@chromium.org>
Reviewed-by: Sophie Chang <sophiechang@chromium.org>
Auto-Submit: Robert Ogden <robertogden@chromium.org>
Cr-Commit-Position: refs/branch-heads/5845@{#1232}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/dd1d15391999ee8b4f212866652b16c7b6be7fee/chrome/browser/offline_pages/offline_page_utils.cc


### am...@google.com (2023-08-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-08-09)

Congratulations avaue! The Chrome VRP Panel has decided to award you $30,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1448548?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Internals>Network, UI>Browser>Offline]
[Monorail mergedwith: crbug.com/chromium/847919]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064789)*
