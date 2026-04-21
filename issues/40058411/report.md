# Security:  UAF in DistilledPagePrefs::SetFontScaling

| Field | Value |
|-------|-------|
| **Issue ID** | [40058411](https://issues.chromium.org/issues/40058411) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>ReaderMode |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | md...@chromium.org |
| **Created** | 2022-01-06 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a raw pointer `distilled_page_prefs_` stored as member variable in class DistillerJavaScriptServiceImpl. And the lifetime of DistillerJavaScriptServiceImpl binds to a self-owned receiver [1], which means it will stay alive as long as the underlying message pipe stays connected.

`distilled_page_prefs_` comes from DomDistillerContextKeyedService (derived from KeyedSerive) and will be a dangling pointer after the Profile is gone.

Because DistillerJavaScriptServiceImpl can continue receiving mojo calls after the Profile is freed, a UAF would occur when function like DistillerJavaScriptServiceImpl::HandleStoreFontScalingPref being invoked and accessing the raw pointer again [2].

```
void CreateDistillerJavaScriptService(  
    DistillerUIHandle\* distiller_ui_handle,  
    DistilledPagePrefs\* distilled_page_prefs,  
    mojo::PendingReceiver<mojom::DistillerJavaScriptService> receiver) {  
  mojo::MakeSelfOwnedReceiver(std::make_unique<DistillerJavaScriptServiceImpl>(  // ===> [1]  
                                  distiller_ui_handle, distilled_page_prefs),  
                              std::move(receiver));  
}  
  
void DistillerJavaScriptServiceImpl::HandleStoreFontScalingPref(  
    float font_scale) {  
  distilled_page_prefs_->SetFontScaling(font_scale);   // ===> [2]  
}  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/dom_distiller/content/browser/distiller_javascript_service_impl.cc;l=45;drc=73a504d9c4206b06598fc62da68407a4a6b703b4>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:components/dom_distiller/content/browser/distiller_javascript_service_impl.cc;l=38;drc=73a504d9c4206b06598fc62da68407a4a6b703b4>

**VERSION**  

Chrome Version: 97.0.4692.71 (stable) + dev

**REPRODUCTION CASE**

1. copy js mojo binding files to working dir  
   
   python3 ./copy\_mojo\_bindings.py /path/to/chrome/.../out/Asan/gen
2. setup a HTTP server  
   
   python3 -m http.server 8000
3. run out/asan/chrome --user-data-dir=/tmp/xxx/ --enable-blink-features=MojoJS <http://localhost:8000/poc.html>
4. close the tab immediately and the browser should crash in a few seconds

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan.log for details

## Attachments

- [copy_mojo_bindings.py](attachments/copy_mojo_bindings.py) (text/plain, 637 B)
- [poc.html](attachments/poc.html) (text/plain, 626 B)
- [asan.log](attachments/asan.log) (text/plain, 33.7 KB)

## Timeline

### [Deleted User] (2022-01-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-01-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5737565271162880.

### cl...@chromium.org (2022-01-07)

ClusterFuzz testcase 5737565271162880 is closed as invalid, so closing issue.

### cl...@chromium.org (2022-01-07)

Testcase 5737565271162880 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5737565271162880.

### dr...@chromium.org (2022-01-07)

I'm not sure why ClusterFuzz closed this just because it didn't reproduce. I'll take a look.

### dr...@chromium.org (2022-01-07)

ClusterFuzz failed to reproduce the crash because it couldn't find distiller_javascript_service.mojom.js. My local build also doesn't have it. Did you do something special to generate those bindings?

### jt...@gmail.com (2022-01-10)

Re #6:
Run "ninja -C out/<asan_build> components/dom_distiller/core/mojom:mojom_js" if there were no js binding files  : )

### [Deleted User] (2022-01-10)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-01-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5185971351781376.

### dr...@chromium.org (2022-01-10)

I'm still having trouble reproducing this, but I now suspect that my setup is the problem, so triaging to some owners for dom_distiller, who can probably do a better job reproducing this.



[Monorail components: UI>Browser>ReaderMode]

### [Deleted User] (2022-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### md...@chromium.org (2022-01-14)

I haven't been able to repro either, but it should be relatively easy to remove the possibility of this.

### jt...@gmail.com (2022-01-15)

This could be reproduced in another way with an extension installed, just like crbug.com/1197904. Please let me know if you need more info about it.

### gi...@appspot.gserviceaccount.com (2022-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ee3c9dfc50f9330c8205cd7eff97dd18774573c3

commit ee3c9dfc50f9330c8205cd7eff97dd18774573c3
Author: Matt Jones <mdjones@chromium.org>
Date: Tue Jan 18 19:03:59 2022

Fix possible UAF in DistillerJavascriptServiceImpl

This patch moves away from using raw pointers in the distiller
javascript service, instead using a weak pointer to the main distiller
service. Methods that call into the distiller service now check the
weak pointer to make sure it is still alive, removing the potential
for a use-after-free bug.

Bug: 1284916
Change-Id: I6d2348ec4c12b4c068f5ae2efc1bd97a49e6fe3a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389816
Reviewed-by: Filip Gorski <fgorski@chromium.org>
Reviewed-by: Alex Gough <ajgo@chromium.org>
Commit-Queue: Matthew Jones <mdjones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#960510}

[modify] https://crrev.com/ee3c9dfc50f9330c8205cd7eff97dd18774573c3/components/dom_distiller/content/browser/distiller_javascript_service_impl.cc
[modify] https://crrev.com/ee3c9dfc50f9330c8205cd7eff97dd18774573c3/components/dom_distiller/core/dom_distiller_service.h
[modify] https://crrev.com/ee3c9dfc50f9330c8205cd7eff97dd18774573c3/chrome/browser/chrome_browser_interface_binders.cc
[modify] https://crrev.com/ee3c9dfc50f9330c8205cd7eff97dd18774573c3/components/dom_distiller/core/dom_distiller_service.cc
[modify] https://crrev.com/ee3c9dfc50f9330c8205cd7eff97dd18774573c3/components/dom_distiller/content/browser/distiller_javascript_service_impl.h


### md...@chromium.org (2022-01-18)

Marking as fixed, not sure if this needs to be merged back to M97 and M98.

### md...@chromium.org (2022-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-19)

Merge review required: M98 is already shipping to beta.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-19)

Merge review required: M97 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### md...@chromium.org (2022-01-19)

1. This is a security fix
2. https://chromium-review.googlesource.com/c/chromium/src/+/3389816
3. Yes
4. No
5. N/A
6. No

### am...@chromium.org (2022-01-21)

Hi mdjones@, thank you for fixing this issue. In the future, one the CLs resolving a security bug are landed, please update the bug to Fixed immediately. This way the bug can make appropriate decisions and labeling based on branch points and severity and you no longer have to manually request merges. :) 

### am...@chromium.org (2022-01-21)

merge approved to M98, please merge this fix to branch 4758 at your earliest convenience before 11am PST, Tuesday, 25 January 2021 so this fix can be included in the stable cut for M98 -- thank you! 

### md...@chromium.org (2022-01-21)

My mistake, I'll remember that for the future. Merge in progress here: https://chromium-review.googlesource.com/c/chromium/src/+/3408015

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

[Empty comment from Monorail migration]

### sr...@google.com (2022-01-24)

https://chromium-review.googlesource.com/c/chromium/src/+/3408015 has merged to M98.

### [Deleted User] (2022-01-24)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### md...@chromium.org (2022-01-24)

1. No, it is a long-standing issue likely for the lifetime of the feature (much farther back than M90)
2. No

### rz...@google.com (2022-01-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-01-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-01-28)

Congratulations! The VRP Panel has decided to award you $20,000 for this report. Thank you for your efforts and great work!! 

### am...@google.com (2022-01-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-01-31)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-02-04)

1. Number of CLs needed for this fix and links to them.
1 CL, https://crrev.com/c/3417138

2. Level of complexity (High, Medium, Low - Explain)
Low, includes and member data type declaration conflicts

3. Has this been merged to a stable release? beta release?
98

4. Overall Recommendation (Yes, No)
Yes

### gm...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/917f042f6707fac7c578254584689a62feaa695b

commit 917f042f6707fac7c578254584689a62feaa695b
Author: Matt Jones <mdjones@chromium.org>
Date: Mon Feb 07 18:13:19 2022

[M96-LTS] Fix possible UAF in DistillerJavascriptServiceImpl

M96 merge issues:
  distiller_javascript_service_impl.h:
    - distiller_ui_handle_, distilled_page_prefs_ declared as
    simple raw pointers instead of raw_ptr<>
    - conflicting includes
  dom_distiller_service.h:
    - conflicting includes

This patch moves away from using raw pointers in the distiller
javascript service, instead using a weak pointer to the main distiller
service. Methods that call into the distiller service now check the
weak pointer to make sure it is still alive, removing the potential
for a use-after-free bug.

(cherry picked from commit ee3c9dfc50f9330c8205cd7eff97dd18774573c3)

Bug: 1284916
Change-Id: I6d2348ec4c12b4c068f5ae2efc1bd97a49e6fe3a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3389816
Reviewed-by: Filip Gorski <fgorski@chromium.org>
Reviewed-by: Alex Gough <ajgo@chromium.org>
Commit-Queue: Matthew Jones <mdjones@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#960510}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3417138
Reviewed-by: Matthew Jones <mdjones@chromium.org>
Reviewed-by: Jana Grill <janagrill@google.com>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1460}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/917f042f6707fac7c578254584689a62feaa695b/chrome/browser/chrome_browser_interface_binders.cc
[modify] https://crrev.com/917f042f6707fac7c578254584689a62feaa695b/components/dom_distiller/content/browser/distiller_javascript_service_impl.cc
[modify] https://crrev.com/917f042f6707fac7c578254584689a62feaa695b/components/dom_distiller/core/dom_distiller_service.h
[modify] https://crrev.com/917f042f6707fac7c578254584689a62feaa695b/components/dom_distiller/core/dom_distiller_service.cc
[modify] https://crrev.com/917f042f6707fac7c578254584689a62feaa695b/components/dom_distiller/content/browser/distiller_javascript_service_impl.h


### rz...@google.com (2022-02-07)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1284916?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058411)*
