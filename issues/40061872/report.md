# Security: heap-use-after-free on chromeOS using PhoneHub + Screensharing

| Field | Value |
|-------|-------|
| **Issue ID** | [40061872](https://issues.chromium.org/issues/40061872) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Shell |
| **Platforms** | ChromeOS |
| **Reporter** | vi...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2022-11-22 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

Consistent heap-use-after-free on chromeOS while using PhoneHub + Screensharing

**VERSION**  

ChromeOS Version: 1074406  

Operating System: ChromeOS

**REPRODUCTION CASE**

1. Open ChromeOS ./asan-linux-release-1074406/chrome
2. Menu > Screen capture > Change to Screen Record and Partial Screen > Gear Icon > Select Folder
3. Exit (Esc, right-click, right-click, esc)
4. Click on Phone Hub, waits 1 second (which keeps trying to connect)
5. Menu > Screen capture > Change to Screen Record and Partial Screen > Gear Icon > Select Folder
6. Wait a few seconds (about 15 seconds) and it breaks ( sometimes need to do the steps above the third time )

**CREDIT INFORMATION**  

Reporter credit: Vitor Torres (github.com/vtorres)

REQUEST FOR CC:  

[alesandro@alesandroortiz.com](mailto:alesandro@alesandroortiz.com)

## Attachments

- [heapuserafterfreechromeos.txt](attachments/heapuserafterfreechromeos.txt) (text/plain, 11.7 KB)
- [heap-user-after-free-chromeos.mp4](attachments/heap-user-after-free-chromeos.mp4) (video/mp4, 5.4 MB)
- [fewsteps.mp4](attachments/fewsteps.mp4) (video/mp4, 5.3 MB)
- [crash.txt](attachments/crash.txt) (text/plain, 29.0 KB)
- [easysteps.mp4](attachments/easysteps.mp4) (video/mp4, 5.0 MB)

## Timeline

### [Deleted User] (2022-11-22)

[Empty comment from Monorail migration]

### vi...@gmail.com (2022-11-22)

Another way with fewer steps:

1. Click on the PhoneHub, wait for a second
2. Menu > Screen capture > Gear Icon > Select Folder
3. Wait 50-60 seconds, it automatically happens


### vi...@gmail.com (2022-11-22)

btw, I'm running it on 
Operating System: Ubuntu 20.04 inside the WSL

### vi...@gmail.com (2022-11-22)

Symbolized crash

### vi...@gmail.com (2022-11-22)

Easier steps after took a better look at what was happening
1. Click Phone Hub > Gear Icon
2. Disable Phone Hub

### vi...@gmail.com (2022-11-22)

I think the UAF was probably added relatively recently: https://source.chromium.org/chromium/chromium/src/+/5416138368b983c79b1928943dd664961f0ddbf3

The call to UpdateHeaderVisibility() in line 157 was added in that CL from Nov 17:
https://source.chromium.org/chromium/chromium/src/+/main:ash/system/phonehub/phone_hub_tray.cc;l=157;drc=7473aada23e43186bbbd4491f8f7f5630e34e109

I don't know for sure, gonna wait for your analysis

### ct...@chromium.org (2022-11-22)

Thanks for your report and your additional investigation! Passing to the ChromeOS sheriff triage as this appears to be specific to ChromeOS system components, and cc'ing the owner of the linked CL.

### vi...@gmail.com (2022-11-23)

[Comment Deleted]

### vi...@gmail.com (2022-11-23)

Ty cthomp@, could you CC alesandro@alesandroortiz.com?

Ah, another detail, the person you cc'ed last visited 46 days ago here with a clock icon, i don't know if worths to mention

### al...@google.com (2022-11-29)

[Empty comment from Monorail migration]

[Monorail components: UI>Shell]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### vi...@gmail.com (2022-11-29)

allenwebb@: Easier steps to repro that I found are mentioned in https://crbug.com/chromium/1392721#c5.

### al...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-29)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-29)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@google.com (2022-11-29)

Tracking the fix in b/260274639

### al...@google.com (2022-11-29)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/260274639]

### na...@google.com (2022-11-29)

Sorry for the late action on this. I am new to Chrome development and did not paid close attention here. We are going to fix the issue ASAP.

### na...@google.com (2022-11-29)

BTW, the new code is guarded by a flag that is off by default: features::IsEcheLauncherEnabled() So, the risk of this is very limited. We will add the fix before M110 cut and hence the flag will be turned on for a larger population only with the fix submitted.

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4868047f97f0c8d4435d70dc902af72212447264

commit 4868047f97f0c8d4435d70dc902af72212447264
Author: Abbas Nayebi <nayebi@google.com>
Date: Fri Dec 02 01:47:55 2022

[eche] Fixing a use-after-free issue with PhoneStatusView.

Change-Id: Ie9d80a83259ee331f068c993ef47a43245b5bf5e
Bug:1392721 b/260274639

Test=As you see in https://screenshot.googleplex.com/47EX3jiSA8BpZh9 commenting the newly added behavior resulted in a use-after-free error in the newly added test that was caught by ASAN.

Change-Id: Ie9d80a83259ee331f068c993ef47a43245b5bf5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4062014
Auto-Submit: Abbas Nayebi <nayebi@google.com>
Reviewed-by: Jon Mann <jonmann@chromium.org>
Commit-Queue: Abbas Nayebi <nayebi@google.com>
Cr-Commit-Position: refs/heads/main@{#1078407}

[modify] https://crrev.com/4868047f97f0c8d4435d70dc902af72212447264/ash/system/phonehub/phone_hub_tray_unittest.cc
[modify] https://crrev.com/4868047f97f0c8d4435d70dc902af72212447264/ash/system/phonehub/phone_hub_tray.cc
[modify] https://crrev.com/4868047f97f0c8d4435d70dc902af72212447264/ash/system/phonehub/phone_hub_tray.h


### na...@google.com (2022-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-02)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations, Vitor! The VRP Panel has decided to award you $2,000 for this report of a highly mitigated security bug. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-17)

Not requesting merge to dev (M110) because latest trunk commit (1078407) appears to be prior to dev branch point (1084008). If this is incorrect, please replace the Merge-NA-110 label with Merge-Request-110. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge review required: M110 is already shipping to stable.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ce...@google.com (2023-01-03)

@nayebi - Could you confirm the comment posted by the automation in #29 is correct? 

If so, we can go ahead and remove the Merge-Review labels.

Thanks!


### na...@google.com (2023-01-03)

We do not need to merge as the failing code had been moved behind a flag even before we fix it (at https://chromium-review.googlesource.com/c/chromium/src/+/4043682/6/ash/system/phonehub/phone_hub_tray.cc) and we are not going to enable the flag until we have the changes.

### ce...@google.com (2023-01-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1392721?no_tracker_redirect=1

[Monorail blocked-on: b/260274639]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061872)*
