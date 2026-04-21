# Google Chrome Console WebUI Heap-Overflow Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40062510](https://issues.chromium.org/issues/40062510) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>WebUI |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | no...@ssd-disclosure.com |
| **Assignee** | du...@chromium.org |
| **Created** | 2023-01-05 |
| **Bounty** | $2,000.00 |

## Description

\*\*Crashed report ID: \*\* 762519778119f868

\*\*How much crashed? \*\* The whole browser

\*\*Is it a problem with a plugin? \*\* No - It's the browser itself

**Steps to reproduce the problem:**

## Title

- Google Chrome WebUI Heap-Overflow Vulnerability

## Summary

- A Heap-Overflow vulnerability exists in the WebUI processing

## Test environment

- Product : Google Chrome Stable 110.0.5459.0
- OS : Windows, Ubuntu, macOS

## Root Cause Analysis

- Heap overflow occurs when the value of "preference\_to\_datatatype" is different from the value of "pref\_name" when calling the find function[1].
- If the values are different, iter values is iter->end(), but iter->end() check is dcheck[2].

```
BrowsingDataType GetDataTypeFromDeletionPreference(  
    const std::string& pref_name) {  
  using DataTypeMap = base::flat_map<std::string, BrowsingDataType>;  
  static base::NoDestructor<DataTypeMap> preference_to_datatype(  
      std::initializer_list<DataTypeMap::value_type>{  
          {prefs::kDeleteBrowsingHistory, BrowsingDataType::HISTORY},  
          {prefs::kDeleteBrowsingHistoryBasic, BrowsingDataType::HISTORY},  
          {prefs::kDeleteCache, BrowsingDataType::CACHE},  
          {prefs::kDeleteCacheBasic, BrowsingDataType::CACHE},  
          {prefs::kDeleteCookies, BrowsingDataType::COOKIES},  
          {prefs::kDeleteCookiesBasic, BrowsingDataType::COOKIES},  
          {prefs::kDeletePasswords, BrowsingDataType::PASSWORDS},  
          {prefs::kDeleteFormData, BrowsingDataType::FORM_DATA},  
          {prefs::kDeleteSiteSettings, BrowsingDataType::SITE_SETTINGS},  
          {prefs::kDeleteDownloadHistory, BrowsingDataType::DOWNLOADS},  
          {prefs::kDeleteHostedAppsData, BrowsingDataType::HOSTED_APPS_DATA},  
      });  

  auto iter = preference_to_datatype->find(pref_name);    //[1]  
  DCHECK(iter != preference_to_datatype->end());          //[2]  
  return iter->second;  
}  

```
## Patch

```
- DCHECK(iter != preference_to_datatype->end());          //[2]  
+ CHECK(iter != preference_to_datatype->end());  

```

**Problem Description:**

## Proof-of-Concept



chrome.send("clearBrowsingData", ["A", [“AAAA”], 0, []]);

```

## REPRODUCTION CASE  
- browsing "chrome://settings" and open devtools  
- excute 'chrome.send("clearBrowsingData", ["A", ["AAAA"], 0, []]);' in console  

**Additional Comments:**   


**Chrome version: ** 108.0.0.0 **Channel: ** Stable  

**OS:** Linux

```

## Timeline

### [Deleted User] (2023-01-05)

^ SecurityTeam

Please add the Bug-Security Label to this report!

### [Deleted User] (2023-01-05)

^ amyressler@google.com

### dt...@chromium.org (2023-01-05)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>WebUI]

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-01-13)

We should not be assuming that the potentially untrustworthy data from the renderer always refers to a pref name. Medium because even though this is a memory unsafely issue, it needs to be combined with a UXSS to a Chrome:// page.

### [Deleted User] (2023-01-13)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-01-13)

Also, on newer versions of Chrome, the repro command is:
chrome.send("clearBrowsingData", ["A", ["AAAA"], 0]);

Since the last argument was removed.

### [Deleted User] (2023-01-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### du...@chromium.org (2023-01-16)

Created a CL: crrev.com/c/4166946

As already mentioned, this heap overflow can only be triggered if the user manually pastes code into devtools. Is this considered a security issue? 
A website can't even navigate a user to chrome://settings or open devtools itself so it requires quite significant manual interaction. You could probably also ask users to just paste stuff into a terminal at this point.


### gi...@appspot.gserviceaccount.com (2023-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/41aeccaca92846875fc393196906a803d2391e33

commit 41aeccaca92846875fc393196906a803d2391e33
Author: Christian Dullweber <dullweber@chromium.org>
Date: Tue Jan 17 20:34:36 2023

ClearBrowsingData: Prevent heap overflow with false data type

Users can call ClearBrowsingDataHandler::HandleClearBrowsingData with
false arguments through devtools. This usually results in a clean crash.
Passing an invalid data type results in a heap overflow. This is turned
into a clean crash by changing a DCHECK into a CHECK.

Bug: 1405123
Change-Id: I00c7d7aefcd8b1d68a285fce62edf8ebdf2e3b4b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4166946
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Commit-Queue: Demetrios Papadopoulos <dpapad@chromium.org>
Auto-Submit: Christian Dullweber <dullweber@chromium.org>
Reviewed-by: Martin Šrámek <msramek@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1093506}

[modify] https://crrev.com/41aeccaca92846875fc393196906a803d2391e33/components/browsing_data/core/browsing_data_utils.h
[modify] https://crrev.com/41aeccaca92846875fc393196906a803d2391e33/components/browsing_data/core/browsing_data_utils.cc
[modify] https://crrev.com/41aeccaca92846875fc393196906a803d2391e33/chrome/browser/ui/webui/settings/settings_clear_browsing_data_handler.cc


### du...@chromium.org (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

Requesting merge to beta M110 because latest trunk commit (1093506) appears to be after beta branch point (1084008).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-18)

Merge review required: M110 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-19)

M110 merge approved, please merge this fix to branch 5481 at your earliest convenience. I agree with the bot's labeling on this one. This doesn't not appear to be a sufficient severe issue to backmerge farther than 110 due to the level of mitigation and user interaction required. 

### du...@google.com (2023-01-20)

Created merge cl: https://crrev.com/c/4183162

### gi...@appspot.gserviceaccount.com (2023-01-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4f8124e01158772f904356e706972d29bb2a4fa3

commit 4f8124e01158772f904356e706972d29bb2a4fa3
Author: Christian Dullweber <dullweber@chromium.org>
Date: Fri Jan 20 09:01:39 2023

ClearBrowsingData: Prevent heap overflow with false data type

Users can call ClearBrowsingDataHandler::HandleClearBrowsingData with
false arguments through devtools. This usually results in a clean crash.
Passing an invalid data type results in a heap overflow. This is turned
into a clean crash by changing a DCHECK into a CHECK.

(cherry picked from commit 41aeccaca92846875fc393196906a803d2391e33)

Bug: 1405123
Change-Id: I00c7d7aefcd8b1d68a285fce62edf8ebdf2e3b4b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4166946
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Commit-Queue: Demetrios Papadopoulos <dpapad@chromium.org>
Auto-Submit: Christian Dullweber <dullweber@chromium.org>
Reviewed-by: Martin Šrámek <msramek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1093506}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4183162
Reviewed-by: John Lee <johntlee@chromium.org>
Commit-Queue: Christian Dullweber <dullweber@chromium.org>
Commit-Queue: John Lee <johntlee@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#487}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/4f8124e01158772f904356e706972d29bb2a4fa3/components/browsing_data/core/browsing_data_utils.h
[modify] https://crrev.com/4f8124e01158772f904356e706972d29bb2a4fa3/components/browsing_data/core/browsing_data_utils.cc
[modify] https://crrev.com/4f8124e01158772f904356e706972d29bb2a4fa3/chrome/browser/ui/webui/settings/settings_clear_browsing_data_handler.cc


### dc...@chromium.org (2023-01-20)

> As already mentioned, this heap overflow can only be triggered if the user manually pastes code into devtools. Is this considered a security issue? 
> A website can't even navigate a user to chrome://settings or open devtools itself so it requires quite significant manual interaction. You could probably also ask users to just paste stuff into a terminal at this point.

To be clear, the immediate bug here (browser trusting renderer data) is a security issue because:
- historically there have been bugs which allowed an attacker-controlled page to UXSS a chrome:// page (and open other chrome:// pages)
- triggering the bug itself does not require devtools; devtools is just the avenue by which this bug is being demonstrated.

Normally this would be a critical severity bug as a browser process memory safety issue; however, due to the mitigating factors (and hopefully stronger UXSS protection), it is only medium severity.

### dc...@chromium.org (2023-01-20)

(maybe not critical; iirc, this might "just" be a read not a write; nonetheless, it's still a security bug)

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### no...@ssd-disclosure.com (2023-02-02)

Please credit it to:
Sumin Hwang of SSD Labs

### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1405123?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062510)*
