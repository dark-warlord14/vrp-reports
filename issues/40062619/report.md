# Security: Forced user interaction for permission prompts by closing a popup window

| Field | Value |
|-------|-------|
| **Issue ID** | [40062619](https://issues.chromium.org/issues/40062619) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Permissions>Indicators |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | re...@gmail.com |
| **Assignee** | tu...@chromium.org |
| **Created** | 2023-01-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

It is possible to trick a user into accepting a permission prompt (eg microphone/webcam) by tricking them into clicking rapidly in a popup window, then closing the popup while a permission prompt is already open in a different window.

The permission prompt has a cooldown to prevent similar clickjacking attacks, but this cooldown does not apply across different windows.

**VERSION**  

Chrome Version: Stable, Dev (110.0.5481.30)  

Operating System: Windows, macOS, Linux

**REPRODUCTION CASE**  

The included PoC only works on Windows, but could be made to work cross-platform (like in <https://crbug.com/chromium/1371207>).

1. Open the attached `poc.html` file from a secure context.
2. Click on "Start Game".
3. Rapidly click the cookie.
4. The window will close and make you accept the microphone permission with an additional click.

This reproduction case can also be seen in the `demo.mp4` file.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Jasper Rebane (popstonia)

## Attachments

- [demo.mp4](attachments/demo.mp4) (video/mp4, 456.2 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### bo...@google.com (2023-01-17)

Thanks for the report. I'm not familiar enough with our Permissions threat model to say for sure whether this behavior is working as intended or something to try to mitigate. 

Assigning Medium severity due to mitigating factors such as assumptions about window placement that break the POC when not satisfied. However I'm relying on Permissions folks to adjust severity based on norms that I may not be familiar with. 

Joe, apologies if you're not the right person for subsequent triage. Monorail listed raymes@ as the component owner, but they're no longer with Google and there was some overlap with your ownership roles in related components. Feel free to punt back to me if you're not the right person and don't know who is. 

[Monorail components: UI>Browser>Permissions>Indicators]

### [Deleted User] (2023-01-17)

[Empty comment from Monorail migration]

### re...@gmail.com (2023-01-17)

Thank you for the triage!

I agree with the severity assigned, but I just wanted to note that the PoC is not mitigated by the window placement or size, as it uses the parent window's screenX/screenY properties and the popup's moveTo method to always place the dialog window in the right spot (on Windows, for this PoC specifically). 

### [Deleted User] (2023-01-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-27)

jdeblasio: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jd...@chromium.org (2023-01-30)

[Comment Deleted]

### jd...@chromium.org (2023-01-30)

fjacky@: I think that https://crbug.com/chromium/1407511 is a duplicate of this one, but assigning to you just in case.

If they are indeed duplicates, please dupe the other one into this one -- this report was submitted first, so is the one that ought to qualify for a VRP reward.

Thanks!


### jd...@chromium.org (2023-01-30)

[Empty comment from Monorail migration]

### fj...@chromium.org (2023-02-01)

[Empty comment from Monorail migration]

### fj...@chromium.org (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-11)

tungnh: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2023-02-11)

[Empty comment from Monorail migration]

### sr...@google.com (2023-02-25)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-03-06)

Given that there're several similar reports and attacks focusing on overlay windows clickjacking, I think it would be better to come up with general mitigation.
One interesting point, all the attacks are triggered from window.open and that would be a good start for us.
FYI, finally I have time on this and I start writing down one pager potential mitigation (not completed):
https://docs.google.com/document/d/1gyTYJGgXRMh_eYXmCD86I44-kQOqlVb4VUwnyc_qXhg/edit#heading=h.634dhc2cz9rm

### tu...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### re...@gmail.com (2023-03-06)

I'd be interested in the mitigation docs, would it be possible to get view access or is it too confidential to share?

### tu...@chromium.org (2023-03-06)

I think the document's for internal only, at this time being

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### tu...@chromium.org (2023-05-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c5119cd03d4078afaa280d2398d7faf3157db980

commit c5119cd03d4078afaa280d2398d7faf3157db980
Author: Thomas Nguyen <tungnh@google.com>
Date: Fri May 26 14:14:00 2023

Ignore user input events shortly after moving overlay windows

This is implementation of
https://docs.google.com/document/d/1gyTYJGgXRMh_eYXmCD86I44-kQOqlVb4VUwnyc_qXhg/edit#

Bug: 1406922
Change-Id: If9e4f085d95cd8e2bb0eacc8d66e48f88886e9fb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4476695
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Commit-Queue: Thomas Nguyen <tungnh@chromium.org>
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1149704}

[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/widget/native_widget_mac_unittest.mm
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/window/dialog_client_view.h
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/bubble/bubble_frame_view.cc
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/window/dialog_client_view.cc
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/BUILD.gn
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/widget/native_widget_mac.mm
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/window/dialog_delegate.cc
[add] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/windows_stationarity_monitor.h
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/input_event_activation_protector.h
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/input_event_activation_protector.cc
[add] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/windows_stationarity_monitor_aura.cc
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/test/widget_test.h
[add] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/windows_stationarity_monitor.cc
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/components/ui_devtools/views/dom_agent_mac.h
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/chrome/browser/ui/views/permissions/chip_controller.cc
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/chrome/browser/ui/views/permissions/permission_prompt_bubble.cc
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/window/dialog_client_view_unittest.cc
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/widget/native_widget_mac.h
[add] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/windows_stationarity_monitor_mac.mm
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/window/dialog_delegate.h
[modify] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/components/ui_devtools/views/dom_agent_mac.mm
[add] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/windows_stationarity_monitor_aura.h
[add] https://crrev.com/c5119cd03d4078afaa280d2398d7faf3157db980/ui/views/windows_stationarity_monitor_mac.h


### tu...@chromium.org (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-30)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations, Jasper! The VRP Panel has decided to award you $1,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### en...@chromium.org (2023-06-14)

Thomas, can you please update the milestones on this one? It looks like we are targeting a fix later than M112 here.

### tu...@chromium.org (2023-06-15)

[Empty comment from Monorail migration]

### en...@chromium.org (2023-06-15)

Did we verify this fix on Canary already? We might need to force-disable the one-time permission experiment (chrome://flags/#one-time-permission), so that we get the old UI that this bug talks about. Work on the new UI is tracked in a separate bug.

### en...@chromium.org (2023-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

Not requesting merge to dev (M116) because latest trunk commit (1149704) appears to be prior to dev branch point (1160321). If this is incorrect, please replace the Merge-NA-116 label with Merge-Request-116. If other changes are required to fix this bug completely, please request a merge if necessary.

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

### fj...@chromium.org (2023-06-29)

[Empty comment from Monorail migration]

### da...@google.com (2023-07-12)

Removing merge-approved as it seems to be added by sheriffbot by mistake.

### am...@chromium.org (2023-08-11)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1406922?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1407511, crbug.com/chromium/1414896, crbug.com/chromium/1418749, crbug.com/chromium/1453929, crbug.com/chromium/1458739]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062619)*
