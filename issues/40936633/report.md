# Security: Heap-use-after-free in ReadAnythingUntrustedPageHandler::LogTextStyle

| Field | Value |
|-------|-------|
| **Issue ID** | [40936633](https://issues.chromium.org/issues/40936633) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>SidePanel |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | me...@gmail.com |
| **Assignee** | kr...@google.com |
| **Created** | 2023-10-17 |
| **Bounty** | $2,000.00 |

## Description

**Steps to reproduce the problem:**

1. Start a server at the folder of poc.html
2. `./Chromium --user-data-dir=./tmp http://127.0.0.1:8605/poc.html about:blank`
3. Open the `SidePanel`, choose `ReadAnything`, then drag and merge the poc.html, close the `SidePanel`

**Problem Description:**

1. Analysis

There is a `raw_ptr<Browser> browser_` in `ReadAnythingUntrustedPageHandler`[1], it could be deleted before the `ReadAnythingUntrustedPageHandler` was destructed, UAF occurs when accessing this freed `browser_`[2].

Note that there are many other codes that use `browser_`, not only the `LogTextStyle`.

```
  const raw_ptr<Browser> browser_;  

```
```
void ReadAnythingUntrustedPageHandler::LogTextStyle() {  
  if (!browser_ || !browser_->profile()->GetPrefs()) {  
    return;  
  }  
  
  // This is called when the side panel closes, so retrieving the values from  
  // preferences won't happen very often.  
  PrefService\* prefs = browser_->profile()->GetPrefs();  
  int maximum_font_scale_logging =  
      GetNormalizedFontScale(kReadAnythingMaximumFontScale);  
  double font_scale =  
      prefs->GetDouble(prefs::kAccessibilityReadAnythingFontScale);  
  base::UmaHistogramExactLinear(string_constants::kFontScaleHistogramName,  
                                GetNormalizedFontScale(font_scale),  
                                maximum_font_scale_logging + 1);  
  std::string font_name =  
      prefs->GetString(prefs::kAccessibilityReadAnythingFontName);  
  if (font_map_.find(font_name) != font_map_.end()) {  
    ReadAnythingFont font = font_map_.at(font_name);  
    base::UmaHistogramEnumeration(string_constants::kFontNameHistogramName,  
                                  font);  
  }  
  read_anything::mojom::Colors color =  
      static_cast<read_anything::mojom::Colors>(  
          prefs->GetInteger(prefs::kAccessibilityReadAnythingColorInfo));  
  base::UmaHistogramEnumeration(string_constants::kColorHistogramName, color);  
  read_anything::mojom::LineSpacing line_spacing =  
      static_cast<read_anything::mojom::LineSpacing>(  
          prefs->GetInteger(prefs::kAccessibilityReadAnythingLineSpacing));  
  base::UmaHistogramEnumeration(string_constants::kLineSpacingHistogramName,  
                                line_spacing);  
  read_anything::mojom::LetterSpacing letter_spacing =  
      static_cast<read_anything::mojom::LetterSpacing>(  
          prefs->GetInteger(prefs::kAccessibilityReadAnythingLetterSpacing));  
  base::UmaHistogramEnumeration(string_constants::kLetterSpacingHistogramName,  
                                letter_spacing);  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/side_panel/read_anything/read_anything_untrusted_page_handler.h;l=128>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/side_panel/read_anything/read_anything_untrusted_page_handler.cc;l=368>

2. Bisect

This `browser_` is introduced in <https://chromium-review.googlesource.com/c/chromium/src/+/3585558> since Stable 103.0.5060.53, and it's a normal pointer and is changed to a `raw_ptr` in <https://chromium-review.googlesource.com/c/chromium/src/+/3682900> Chrome Stable 104.0.5112.79

3. Suggested Patch  
   
   Use a weakPtr to observe the lifetime of `browser_`.

**Additional Comments:**

\*\*Chrome version: \*\* 117.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 60 B)
- [asan.txt](attachments/asan.txt) (text/plain, 22.3 KB)
- [poc.mov](attachments/poc.mov) (video/quicktime, 4.8 MB)

## Timeline

### [Deleted User] (2023-10-17)

[Empty comment from Monorail migration]

### ca...@chromium.org (2023-10-18)

Thanks for the report, I was able to reproduce this in current stable 118. Setting severity to high isnce this is memory corruption in the browser process, but requires significant user interaction.

corising and kristislee: Can you help further triage this (and reassign as appropriate)? Thanks

[Monorail components: UI>Browser>TopChrome>SidePanel]

### [Deleted User] (2023-10-18)

[Empty comment from Monorail migration]

### co...@chromium.org (2023-10-18)

Passing to the read anything team

### ab...@google.com (2023-10-18)

Kristi--Looks like we're still getting reports of this. Might we need to merge the fix into an older version?

### kr...@google.com (2023-10-18)

Maybe. I'm not sure how to do that. Though the fix suggested here is different than the one I did. I'm not sure if my fix fixes the problem as I'm still not super familiar with pointers. 

My fix is here: https://chromium-review.googlesource.com/c/chromium/src/+/4857382 and is in M119.

### ad...@google.com (2023-10-18)

(I am a bot: this is an auto-cc on a security bug)

### ab...@google.com (2023-10-18)

I think we should do the suggested fix here and cherry-pick into 118 and 119, and also cherry-pick your original fix into 118. Here are the merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md. Let me know if you have any questions.

### [Deleted User] (2023-10-19)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@google.com (2023-10-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1d1db68e593863446a45a8b388046ad927eb0a46

commit 1d1db68e593863446a45a8b388046ad927eb0a46
Author: Kristi Saney <kristislee@google.com>
Date: Sat Oct 21 00:03:06 2023

Make ReadAnythingUntrustedPageHandler.browser_ a weak ptr

Bug: 1493380
Change-Id: Id178b9dbd879ea28476adb58e6e18fd6fe2082d6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4953624
Reviewed-by: Jocelyn Tran <jocelyntran@google.com>
Commit-Queue: Kristi Saney <kristislee@google.com>
Cr-Commit-Position: refs/heads/main@{#1213016}

[modify] https://crrev.com/1d1db68e593863446a45a8b388046ad927eb0a46/chrome/browser/ui/webui/side_panel/read_anything/read_anything_untrusted_page_handler.h
[modify] https://crrev.com/1d1db68e593863446a45a8b388046ad927eb0a46/chrome/browser/ui/webui/side_panel/read_anything/read_anything_untrusted_page_handler.cc


### [Deleted User] (2023-10-21)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@google.com (2023-10-23)

Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?
Security severity is high

What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/4953624

Have the changes been released and tested on canary?
Yes

Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
no

If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
no

### [Deleted User] (2023-10-23)

Merge review required: M119 is already shipping to beta.

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
Owners: eakpobaro (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-23)

Merge review required: M118 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@google.com (2023-10-23)

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
it's a security fix of high severity

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/chromium/src/+/4953624

3. Have the changes been released and tested on canary?
yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
no

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
this is not for chromeOS

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
no 

### am...@chromium.org (2023-10-23)

Thank you for fixing this issue. As per https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#security-merge-triage, please update security issues to Fixed status as soon as the final fix CL is landed. This allows the bot to update with the merge reviews based on severity and impact. 
Since this is a bit of larger than standard change for a weak_ptr change, please confirm this fix has been tested and there are no potential stability or other potential issues with backmerging this fix. 
119 is current beta but next release on Wednesday will go out as Early Stable, so we need to be sure there are no potential issues. Thank you! 



### am...@chromium.org (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-24)

Reducing the severity of this issue to medium severity; while this results in memory corruption in the browse process reflected in the initial triage this issue involves significant user interaction to trigger, but this pointer is also BRP protected 

### kr...@google.com (2023-10-24)

Confirming that this fix has been tested and I'm not seeing any issues.

### [Deleted User] (2023-10-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-24)

thank you for confirming!
119 and 118 merges approved for https://crrev.com/c/4953624, please merge this fix to 119 / branch 6045 by EOD today so this fix can be included in the last 119 Beta (and 119 Early Stable) 

please merge this fix to 118 / branch 5993 at your convenience (by EOD Friday, 27 October) so this fix can be included in the first 118 Extended Stable release 

### gi...@appspot.gserviceaccount.com (2023-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9081c90e76cb6c3176a6fb3662bd4a0e6083167a

commit 9081c90e76cb6c3176a6fb3662bd4a0e6083167a
Author: Kristi Saney <kristislee@google.com>
Date: Tue Oct 24 20:23:55 2023

[Merge M119] Make ReadAnythingUntrustedPageHandler.browser_ a weak ptr

(cherry picked from commit 1d1db68e593863446a45a8b388046ad927eb0a46)

Bug: 1493380
Change-Id: Id178b9dbd879ea28476adb58e6e18fd6fe2082d6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4953624
Reviewed-by: Jocelyn Tran <jocelyntran@google.com>
Commit-Queue: Kristi Saney <kristislee@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1213016}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4973676
Commit-Queue: Jocelyn Tran <jocelyntran@google.com>
Auto-Submit: Kristi Saney <kristislee@google.com>
Cr-Commit-Position: refs/branch-heads/6045@{#909}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/9081c90e76cb6c3176a6fb3662bd4a0e6083167a/chrome/browser/ui/webui/side_panel/read_anything/read_anything_untrusted_page_handler.h
[modify] https://crrev.com/9081c90e76cb6c3176a6fb3662bd4a0e6083167a/chrome/browser/ui/webui/side_panel/read_anything/read_anything_untrusted_page_handler.cc


### [Deleted User] (2023-10-24)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/10838444f95177dc6165a2fc8cbfd425dcf69cf2

commit 10838444f95177dc6165a2fc8cbfd425dcf69cf2
Author: Kristi Saney <kristislee@google.com>
Date: Tue Oct 24 21:24:59 2023

[Merge M118] Make ReadAnythingUntrustedPageHandler.browser_ a weak ptr

(cherry picked from commit 1d1db68e593863446a45a8b388046ad927eb0a46)

Bug: 1493380
Change-Id: Id178b9dbd879ea28476adb58e6e18fd6fe2082d6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4953624
Reviewed-by: Jocelyn Tran <jocelyntran@google.com>
Commit-Queue: Kristi Saney <kristislee@google.com>
Cr-Original-Commit-Position: refs/heads/main@{#1213016}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4974036
Auto-Submit: Kristi Saney <kristislee@google.com>
Cr-Commit-Position: refs/branch-heads/5993@{#1421}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/10838444f95177dc6165a2fc8cbfd425dcf69cf2/chrome/browser/ui/webui/side_panel/read_anything/read_anything_untrusted_page_handler.h
[modify] https://crrev.com/10838444f95177dc6165a2fc8cbfd425dcf69cf2/chrome/browser/ui/webui/side_panel/read_anything/read_anything_untrusted_page_handler.cc


### kr...@google.com (2023-10-25)

1. yes
2. the feature was merged in Desktop M115. I'm not sure if that corresponds to the same milestone on ChromeOS LTS

### ab...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### rz...@google.com (2023-10-27)

Most of the changed code isn't present in 114

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-02)

Congratulations Krace! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug, mitigated by BRP protection and the precondition of user gestures. Thank you for your effort and reporting this issue to us! 

### am...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-09)

https://crbug.com/chromium/1494436 has been un-merged from this issue.


### gi...@appspot.gserviceaccount.com (2023-11-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-30)

This issue was migrated from crbug.com/chromium/1493380?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40936633)*
