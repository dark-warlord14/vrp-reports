# Security: UAF in SegmentationPlatformServiceImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40059331](https://issues.chromium.org/issues/40059331) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>SegmentationPlatform |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | ss...@chromium.org |
| **Created** | 2022-04-08 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

When the ProfileManager is destructed with flag SegmentationPlatform enabled:

ProfileManager::~ProfileManager()

```
ProfileManager::~ProfileManager() {  
  DCHECK_CALLED_ON_VALID_THREAD(thread_checker_);  
  for (auto& observer : observers_) {  
    observer.OnProfileManagerDestroying();  
  }  
  [...]  
}  

```

observer.OnProfileManagerDestroying();  

=> SegmentationPlatformProfileObserver::OnProfileManagerDestroying  

=> UkmDatabaseClient::GetInstance().ProfileManagerDestroying(); [1]  

=> ukm\_data\_manager\_.reset(); [2]

ProfileManager::~ProfileManager() Done  

=> ~ProfilesInfoMap profiles\_info\_;  

=> ~ProfileImpl  

=> ~SegmentationPlatformServiceImpl [3]

```
SegmentationPlatformServiceImpl::~SegmentationPlatformServiceImpl() {  
  history_service_observer_.reset();  
  ukm_data_manager_->RemoveRef();  <<<======= raw pointer ukm_data_manager_ UAF.  
}  

```

This flag is enabled by default on Android, but since the `profile_manager` on Android won't be destructed, this UAF does not affect Android devices.

[1]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/segmentation_platform/segmentation_platform_profile_observer.cc;l=81;drc=7784e7d23252129e48b15ab13f05ca0cfc9875ca>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/segmentation_platform/ukm_database_client.cc;l=70;drc=5e0e4558498f51aaed966229ea0c61b94e794d4d>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/main:components/segmentation_platform/internal/segmentation_platform_service_impl.cc;l=170;drc=7f85823102456de1df9273d3ab66e742e2c9cf70>

There were some refactorings in this part of the code recently, but it does not affect the triggering of the uaf.  

The owner seems should be [ssid@chromium.org](mailto:ssid@chromium.org)

**VERSION**

Chrome Version: beta with SegmentationPlatform  

Operating System: all except Android

**REPRODUCTION CASE**

$ python -m SimpleHTTPServer 8000  

$ out/asan/chrome --user-data-dir=/tmp/xxxx --enable-features=SegmentationPlatform "<http://localhost:8000/poc.html>"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan](attachments/asan) (text/plain, 17.9 KB)
- [poc.html](attachments/poc.html) (text/plain, 140 B)

## Timeline

### [Deleted User] (2022-04-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-04-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5516058542538752.

### rs...@chromium.org (2022-04-08)

Thanks, I can reproduce this on 101.0.4951.0 and 102.0.4991.0 but not 100.0.4896.0.

ssid: Can you confirm that SegmentationPlatform is not enabled (even via Finch) on any OS besides Android?

[Monorail components: Internals>SegmentationPlatform]

### [Deleted User] (2022-04-08)

[Empty comment from Monorail migration]

### ss...@chromium.org (2022-04-09)

Segmentation is not enabled on any desktop platforms. I had assumed OnProfileManagerDestroying() is called after profile destruction. Will send a fix.

### [Deleted User] (2022-04-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2022-04-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/172877aff7470271185cc1a14227f8645177fd87

commit 172877aff7470271185cc1a14227f8645177fd87
Author: ssid <ssid@chromium.org>
Date: Mon Apr 11 21:28:45 2022

Do not destroy UkmDataManager

Some profiles are kept alive at shutdown, and segmentation platforms of
this profile can still be using the UKM database. So, do not destroy the
data manager during shutdown.

BUG=1314676

Change-Id: I583a45a63933b52575ef8c300cc297f274e7778c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3579779
Reviewed-by: Min Qin <qinmin@chromium.org>
Commit-Queue: Siddhartha S <ssid@chromium.org>
Cr-Commit-Position: refs/heads/main@{#991189}

[modify] https://crrev.com/172877aff7470271185cc1a14227f8645177fd87/chrome/browser/segmentation_platform/ukm_database_client.cc
[modify] https://crrev.com/172877aff7470271185cc1a14227f8645177fd87/chrome/browser/segmentation_platform/ukm_database_client.h
[modify] https://crrev.com/172877aff7470271185cc1a14227f8645177fd87/chrome/browser/segmentation_platform/segmentation_platform_profile_observer.cc


### ss...@chromium.org (2022-04-12)

No need to merge the fix since experiment is not enabled in any channels.

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-22)

Thank you for this report, Leecraso and Guang Gong. The VRP Panel has decided to award you $3,000 for this report as this issue is fairly mitigated given that it is reliant on profile destruction to trigger. Thank you for your efforts and reporting this issue to us!

### le...@gmail.com (2022-04-22)

Appeal reward reason: First of all thanks very much for the bounty. 

Possibly due to the changes in the panel rules, I've noticed that recent bounties are discounted. I think it's normal for some low impactful or hard-to-exploit vulnerabilities to be discounted. But this time the bounty amount shocked me.

1. The reason for giving this bounty amount is: this issue is fairly mitigated given that it is reliant on profile destruction to trigger. But as far as I understand, this type of bug (like crbug.com/1267661 crbug.com/1283371 crbug.com/1248030) will be awarded around $15000 before this, now it's 20% off. I don't know if the panel's decision rules have changed.

2. If the rules change, I think it should be declared ahead of time.

3. Even if the rules change, I don't think a 20% discount seems like an appropriate decision.

### am...@chromium.org (2022-04-22)

Hi, leecraso. I appreciate you taking the time to reach out and your feedback. 

>>>1. The reason for giving this bounty amount is: this issue is fairly mitigated given that it is reliant on profile destruction to trigger. But as far as I understand, this type of bug (like crbug.com/1267661 crbug.com/1283371 crbug.com/1248030) will be awarded around $15000 before this, now it's 20% off. I don't know if the panel's decision rules have changed.
--- Yes, you are correct. In 2021 and prior we were rewarding higher for these types of bugs. At the time, however, the trend was that these bugs were fairly even and less prolific than reports of bugs that were remote accessible and/or did not require profile destruction. The trends began to shift and remote accessible bugs became more rare and the more common type of security bugs being reported became ones for bugs requiring UI interaction or profile destruction. After some analysis we decided we did need to shift the reward amounts to encourage reporting of remote accessible and more impactful types of security bugs. 

>>>2. If the rules change, I think it should be declared ahead of time.
----  I guess I am a bit surprised by this comment as this change has been communicated both directly in feedback about other bugs, but also via email to the researcher community. Some examples of the 1:1 bug communications were via reward explanations, such as through: https://crbug.com/chromium/1303615, https://crbug.com/chromium/1303613, https://crbug.com/chromium/1292304, and the communications in https://crbug.com/chromium/1283609. Additionally, a very detailed email communication and explanation was directly to the Chrome VRP researcher community via email on 18 February 2021 (the copy of which I will provide below for transparency and in case you missed this). 
I would appreciate your feedback about how else this could have been conveyed for clarity's sake and for communication of future issues. 

Of course, in tandem to this email, we did also update our VRP rules and policies page with this information. [1]

3. >>>Even if the rules change, I don't think a 20% discount seems like an appropriate decision.
----- We are happy to reassess your report, however, unless other information is provided to demonstrate better attacker control or exploitability, I'm not positive there will be much of a change. We are, however, also happy to take your feedback into consideration.

[1] https://g.co/chrome/vrp

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
copy of 18 February researcher to Chrome VRP community group: 

On Fri, Feb 18, 2022 at 1:30 PM Amy Ressler <amyressler@chromium.org> wrote:
Hello Chrome VRP Researchers, 


We wanted to reach out to make you aware of an update to our Rewards information to our Chrome VRP rules.

Previously, the Chrome VRP Rewards section including stated the following: 

The amounts listed are for good quality reports that don't require complex or unlikely user interaction. Less convincing or more constrained bug submissions will likely qualify for reduced reward amounts, as chosen at the discretion of the reward panel.


We have recently updated the page to include clarifying information to help answer some of the questions you have asked us about particular reward decisions. 


There is a recent trend of reports away from issues triggered by remote content to issues that are strongly or solely dependent on user interaction. While we appreciate your efforts to discover and report these bugs, these issues are not as impactful or exploitable as those that demonstrate exploitability through remote content. 

To reduce ambiguity and to provide more clarification, we have updated our Rewards section on our Rules page:


The amounts listed are for good quality reports that don't require complex or unlikely user interaction. Reports of issues that rely heavily or solely on user interaction, instead of being triggered by remote content, will generally receive significantly reduced rewards. Less convincing or more constrained bug submissions will likely qualify for reduced reward amounts, as chosen at the discretion of the reward panel.


Reports of issues that involve implausible interaction, interactions a user would not be realistically convinced to perform, may not be rewarded. 


As always, we are happy to answer questions and provide clarifying information about reward decisions, but hoping this helps provide some context in advance and help you understand some of the decisions moving forward. 


On behalf of the Chrome VRP, 

Amy 



### le...@gmail.com (2022-04-24)

[Comment Deleted]

### le...@gmail.com (2022-04-24)

Hi Amy, thanks for your patient explanation.

Sorry for any confusion. I had noticed the change in the rule for the issues that require user interaction, and I also pretty much agree with this change.

But https://crbug.com/chromium/1314676#c15 is only for the bug triggered during profile destructuring, it does not require user interaction. I'm shocked that the bounty for this type of bug gets 20% off, which seems to be more heavily discounted than those that require complex or unlikely user interaction. This change hasn't been reflected in the previous notices, and such a severe discount seems somewhat unreasonable.

### le...@gmail.com (2022-04-24)

So from my point of view, there are no indications and claims to reduce the bounty for this type of bug to such a degree. After all, the latest public issue that requires profile destruction and even user interaction can get $20,000: crbug.com/1284584. 

I'm sorry if I offended, and also sorry if pointing to the issue links above made reporters uncomfortable.

### am...@chromium.org (2022-04-29)

Hi Leecraso, thank you for your feedback and providing your point of view. Also, you haven't offended at all. Your discourse and questions have been very respectful. We would always rather these questions being asked. The outcome may not always be exactly as you are hoping, but we will always do our best to provide transparency and clarity about reward decisions or any other issues related to VRP security bug reports. 

At this time, the VRP Panel has decided that the reward amount is sufficient for this report. If you could provide a POC that could trigger this behavior or some other information to amplify the security impact and exploitation potential of this issue we would be happy to reassess for a potential change for reward amount. 

In updating the reward and other process documentation [1] we thought it was implied and clear that bugs that these types of security bugs, such as profile destruction, that have a much lower exploitability potential and do not provide a lot of attacker control were understood to be a part of the policy/reward updates. In reviewing the update and your feedback, it appears some additional clarity can be brought to our rules page and the updated language. Apologies that wasn't clear and thank you for the feedback that will allow us to update the policy language to make that clearer to all. 

[1] https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1314676?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059331)*
