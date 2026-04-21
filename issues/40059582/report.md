# Security: UAF in UserEducationInternalsPageHandlerImpl::GetFeaturePromos

| Field | Value |
|-------|-------|
| **Issue ID** | [40059582](https://issues.chromium.org/issues/40059582) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>UserEducation |
| **Platforms** | Linux |
| **Reporter** | et...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2022-05-06 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

Refer to <https://bugs.chromium.org/p/chromium/issues/detail?id=1323236> for reproduction steps

**Problem Description:**  

\*\*VULNERABILITY DETAILS\*\*

UserEducationInternalsPageHandlerImpl holds a raw pointer to `raw_ptr<Profile> profile_` [1].

UserEducationInternalsPageHandlerImpl can continue receiving Mojo calls after `Profile`is freed, resulting in a use after free on [2].

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/internals/user_education/user_education_internals_page_handler_impl.h;drc=07c2037cd88e792e7d3d7ab03d98100d98d19b1d;bpv=1;bpt=1;l=52>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/internals/user_education/user_education_internals_page_handler_impl.cc;l=57;drc=1d3aebb90c0e8a3b791fa309633de1308d0cc48f;bpv=1;bpt=1>

\*\*This bug is similar to [https://bugs.chromium.org/p/chromium/issues/detail?id=1197904\\*\](https://bugs.chromium.org/p/chromium/issues/detail?id=1197904%5C*%5C)\*

**Additional Comments:**

\*\*Chrome version: \*\* 101.0.4951.54 \*\*Channel: \*\* Stable

**OS:** Linux

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 21.5 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 21.5 KB)

## Timeline

### dt...@chromium.org (2022-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-06)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-05-06)

[Comment Deleted]

### me...@google.com (2022-05-06)

Thanks for the report. Assigning high severity since profile destruction is a mitigation factor for severity.

dfried, could you PTAL? Thanks.

[Monorail components: UI>Browser>UserEducation]

### [Deleted User] (2022-05-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-07)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-05-10)

```
void UserEducationInternalsPageHandlerImpl::GetFeaturePromos(
    GetFeaturePromosCallback callback) {
  ...
  const auto& feature_promo_specifications =
      UserEducationServiceFactory::GetForProfile(profile_) // use here!
          ->feature_promo_registry()
          .GetRegisteredFeaturePromoSpecifications();
```


### et...@gmail.com (2022-05-10)

By clicking the show button and closing the page with the plugin, the webui's UAF can be triggered without the need for incognito mode(not the profile's uaf).
But the timing is hard to control, I tried for a long time and only succeeded once, so I can't attach the video, but I attached my asan log, please check it out.

void UserEducationInternalsPageHandlerImpl::ShowFeaturePromo(
    const std::string& title,
    ShowFeaturePromoCallback callback) {
  UserEducationService* user_education_service =
      UserEducationServiceFactory::GetForProfile(profile_);

  const auto& feature_promo_specifications =
      user_education_service->feature_promo_registry()
          .GetRegisteredFeaturePromoSpecifications();

  const base::Feature* feature = nullptr;

  for (const auto& [key, value] : feature_promo_specifications) {
    if (title == GetTitleFromFeaturePromoData(key, value)) {
      feature = key;
      break;
    }
  }

  if (!feature) {
    std::move(callback).Run(std::string("Can not find IPH"));
    return;
  }
  LOG(ERROR) << "sakura in UserEducationInternalsPageHandlerImpl::ShowFeaturePromo" << std::endl;
  FeaturePromoController* feature_promo_controller =
      chrome::FindBrowserWithWebContents(web_ui_->GetWebContents()) // use here!!!!!!!!!
          ->window()
          ->GetFeaturePromoController();


Let me know if you need more feedback, thanks :)


### ts...@chromium.org (2022-05-10)

I can take this on, since I was already planning on changing this after fixing the similar https://crbug.com/chromium/1323236

### ts...@chromium.org (2022-05-11)

I was able to repro the WebUI UAF described in https://crbug.com/chromium/1323239#c9:

1. Open a new tab and navigate to chrome://internals/user-education
2. Click one of the IPH_* buttons
3. At basically the same time, press ctrl-w to close the tab
4. If no crash happened, press ctrl-shift-t and retry

I was able to get it to happen after about 20-30 attempts.

### gi...@appspot.gserviceaccount.com (2022-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f009a6ae002cb1e85720bd009cf3a711d3028139

commit f009a6ae002cb1e85720bd009cf3a711d3028139
Author: Tim Sergeant <tsergeant@chromium.org>
Date: Wed May 11 08:37:28 2022

Do not use a self-owned receiver on chrome://internals/user-education

Using a self-owned receiver means that the
UserEducationInternalsPageHandler can live longer than the
WebUIController. If the handler receives a mojo message with the right
timing, it is possible to trigger a UAF on either the Profile or WebUI.

This CL changes the Handler so that it is owned by the WebUIController
directly, which addresses this issue and matches the pattern used by
other WebUI pages.

Bug: 1323239
Change-Id: Id2127380c398f5a5805001555141afc2f5d57a2b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3640103
Reviewed-by: Christopher Lam <calamity@chromium.org>
Auto-Submit: Tim Sergeant <tsergeant@chromium.org>
Commit-Queue: Tim Sergeant <tsergeant@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1001968}

[modify] https://crrev.com/f009a6ae002cb1e85720bd009cf3a711d3028139/chrome/browser/ui/webui/internals/internals_ui.h
[modify] https://crrev.com/f009a6ae002cb1e85720bd009cf3a711d3028139/chrome/browser/ui/webui/internals/user_education/user_education_internals_page_handler_impl.cc
[modify] https://crrev.com/f009a6ae002cb1e85720bd009cf3a711d3028139/chrome/browser/ui/webui/internals/internals_ui.cc
[modify] https://crrev.com/f009a6ae002cb1e85720bd009cf3a711d3028139/chrome/browser/ui/webui/internals/user_education/user_education_internals_page_handler_impl.h


### et...@gmail.com (2022-05-11)

Thanks for your fix, good job :)

### ts...@chromium.org (2022-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-12)

Requesting merge to stable M101 because latest trunk commit (1001968) appears to be after stable branch point (982481).

Requesting merge to beta M102 because latest trunk commit (1001968) appears to be after beta branch point (992738).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-12)

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

### [Deleted User] (2022-05-12)

Merge review required: M101 is already shipping to stable.

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
Owners: benmason (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2022-05-13)

1. Yes, it's a security fix. Security sheriff can weigh in for certain on whether this meets the bar for a stable merge.

2. https://crrev.com/c/3640103

3. Yes, verified on a new ASAN build.

4. No

5. NA

6. NA

### am...@chromium.org (2022-05-14)

Thanks for this fix! There appear to be no stability risks or concerns with this fix; as long as you concur, please go ahead and merge this fix to branch 5005 NLT EOD Monday, 16 May so this fix can be included in the M102 stable cut; 
101 merge-na, ordinarily this fix would warrant stable merge; however there are no further planned releases of M101 stable/M100 extended and M102 will be the next planned stable release on 24 May. 

### ts...@chromium.org (2022-05-16)

Merge CL is here: https://crrev.com/c/3649920. It's currently blocked on an infra issue (https://crbug.com/chromium/1325711). If that isn't fixed by EOD Monday MTV time, I can force-submit the CL.

### sr...@google.com (2022-05-16)

Please complete your merge to M102 ASAP, M102 RC cut is tomorrow  ( May 17) if you want your change to be part of the M102 stable promotion pls complete merges before EOD today PST ( May 16)

### gi...@appspot.gserviceaccount.com (2022-05-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a802d278c9bbfb5971eba79276bc1ff7296126c1

commit a802d278c9bbfb5971eba79276bc1ff7296126c1
Author: Tim Sergeant <tsergeant@chromium.org>
Date: Mon May 16 18:31:45 2022

[102] Do not use a self-owned receiver on chrome://internals/user-education

Using a self-owned receiver means that the
UserEducationInternalsPageHandler can live longer than the
WebUIController. If the handler receives a mojo message with the right
timing, it is possible to trigger a UAF on either the Profile or WebUI.

This CL changes the Handler so that it is owned by the WebUIController
directly, which addresses this issue and matches the pattern used by
other WebUI pages.

(cherry picked from commit f009a6ae002cb1e85720bd009cf3a711d3028139)

Bug: 1323239
Change-Id: Id2127380c398f5a5805001555141afc2f5d57a2b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3640103
Reviewed-by: Christopher Lam <calamity@chromium.org>
Auto-Submit: Tim Sergeant <tsergeant@chromium.org>
Commit-Queue: Tim Sergeant <tsergeant@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1001968}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3649920
Reviewed-by: Giovanni Ortuno Urquidi <ortuno@chromium.org>
Owners-Override: Tim Sergeant <tsergeant@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#764}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/a802d278c9bbfb5971eba79276bc1ff7296126c1/chrome/browser/ui/webui/internals/internals_ui.h
[modify] https://crrev.com/a802d278c9bbfb5971eba79276bc1ff7296126c1/chrome/browser/ui/webui/internals/user_education/user_education_internals_page_handler_impl.cc
[modify] https://crrev.com/a802d278c9bbfb5971eba79276bc1ff7296126c1/chrome/browser/ui/webui/internals/internals_ui.cc
[modify] https://crrev.com/a802d278c9bbfb5971eba79276bc1ff7296126c1/chrome/browser/ui/webui/internals/user_education/user_education_internals_page_handler_impl.h


### am...@google.com (2022-05-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-05-16)

Thank you for your reports. As this issue and the linked https://crbug.com/chromium/1323236 (for reproduction steps) convey, this issue requires an extension and is reliant on profile destruction OR requires substantial user interaction + reliance on profile destruction (as detailed in https://crbug.com/chromium/1323239#c11) and is does not reliantly reproduce, the VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us. 

### et...@gmail.com (2022-05-17)

[Comment Deleted]

### et...@gmail.com (2022-05-17)

re https://crbug.com/chromium/1323239#c26:
hello i want to know "requires substantial user interaction + reliance on profile destruction" meaning of this sentence
Because following this reproduction step in https://crbug.com/chromium/1323239#c11, it will only need to close the tab to release the webui, **no need to close the browser to release the profile.**
thanks :)
And if using a extension, we can trigger profile uaf in https://crbug.com/chromium/1323239#c8 without interaction, just like issue-1323236 and 
 https://bugs.chromium.org/p/chromium/issues/detail?id=1197904

Please help communicate to VRP and hope this reward will be reconsidered, thanks Chrome VRP :), 
of course, If this is your final decision, I will also accept it.

### am...@chromium.org (2022-05-19)

Hello, the VRP has reassessed your issue and we believe the original reward amount is appropriate for this issue. 
I would still like to answer your questions to provide context and transparency: 
>>>hello i want to know "requires substantial user interaction + reliance on profile destruction" meaning of this sentence
The substantial user interaction refers to the amount of user gesture required by us to reliably reproduce this issue as exhibited by https://crbug.com/chromium/1323239#c11. This issue is not remote/web-accessible and requires direct navigation to chrome://internals/user-education followed by user interactions to trigger this issue in the following steps. 

The user interaction not withstanding the profile is freed which happens upon profile destruction resulting in a small window for exploitability and limited attacker control. In February 2022, we updated our policies (and sent an email to the VRP community to communicate this) to reflect lowered reward amounts for bugs with lower exploitability potential, including bugs mitigated by user gesture and profile destruction. 

Additionally, the scripted trigger via the extension without user gesture as explained in https://crbug.com/chromium/1323239#c9 (and compared to https://crbug.com/chromium/1197904, which requires no user interaction but does close the browser) was not reproducible on our end and also not reliably reproducible by you as explained in that comment. 

I hope this helps! Thanks again for your questions and also taking the time to report this issue and provide the additional explanations. 




### et...@gmail.com (2022-05-20)

Thanks for your reply!
I'll look at this question again when I have time, because in fact triggering a profile's UAF via a extension without interaction I think it's possible.
Before this I fully accept with the decision of chrome vrp.

Another thing, please use "Nan Wang (@eternalsakura13) and Guang Gong of 360 Vulnerability Research Institute" as cve credit, thanks :)

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

### am...@chromium.org (2022-07-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1323239?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059582)*
