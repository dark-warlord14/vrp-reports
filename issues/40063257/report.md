# Security: web HID memory corruption bug

| Field | Value |
|-------|-------|
| **Issue ID** | [40063257](https://issues.chromium.org/issues/40063257) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HID |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | mo...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2023-02-26 |
| **Bounty** | $8,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

I am reporting an issue with web HID. While using the platform, I wrote a code that simulated the transfer of data from an HID device to Google Meet, which caused Chrome to crash.

Although it is unlikely that an actual device is causing this problem, it is possible for someone with malicious intent to exploit this vulnerability by designing a malicious HID device to cause Chrome to crash.

**VERSION**  

Chrome Version: [75.0.3763.0] + [stable, beta, dev]  

Operating System: [Chrome OS, 12106.0.0]

**REPRODUCTION CASE**

1. Compile uhid-example.c (attach file) and scp it to a Chromebook.
2. Open Chrome browser and access Google Meet.
3. Start a new video conference.
4. Connect to the Chromebook via ssh.
5. Execute the uhid-example binary.
6. In Google Meet settings -> Audio -> Call Controls -> Connect a device -> select test-uhid-device.
7. Input "1" into uhid-example.
8. Chrome crashes.

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]  

Crash State: [no stack trace because I already have found the root cause of the bug.]  

Client ID (if relevant): [N/A]

---

Here is the root cause:

commit:  

<https://chromium-review.googlesource.com/c/chromium/src/+/1521966>

When HID device send a input report, there is only a report\_id available, which results in an out-of-bounds memory error in buffer->data()[1].  

<https://source.chromium.org/chromium/chromium/src/+/main:services/device/hid/hid_connection_impl.cc;l=58?q=HidConnectionImpl::OnInputReport&ss=chromium%2Fchromium%2Fsrc>

The attach patch can fix this bug.

---

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: [yes, public]

## Attachments

- [patch.diff](attachments/patch.diff) (text/plain, 882 B)
- [uhid-example.c](attachments/uhid-example.c) (text/plain, 6.9 KB)

## Timeline

### [Deleted User] (2023-02-26)

[Empty comment from Monorail migration]

### sr...@google.com (2023-02-27)

[Empty comment from Monorail migration]

### ha...@google.com (2023-02-27)

 Thanks for the report. I see the you mention that it Chrome [75.0.3763.0] + [stable, beta, dev] is affected. 

Does that mean any version past that or you found this on M75 only? 

### mo...@gmail.com (2023-02-27)

I found this bug on the latest chrome OS version [15365.0.0]. But the root cause patch is merged on M75.

### ha...@google.com (2023-02-28)



Thanks for the clarification. Routing this as appropriate


It is a UAF -- marking it as medium sev. 


Matt, could you please take a look, try to reproduce and land a potential fix?


cc'ing Aashay. Incoming sheriff

[Monorail components: Blink>HID]

### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### mo...@gmail.com (2023-02-28)

Hi~
I already have a patch (patch.diff) in the attach file (in the original report) for fixing the issue, maybe you can take a look first for saving your time.
Thanks.

### ma...@google.com (2023-03-02)

> It is a UAF -- marking it as medium sev.

I don't see how this is UAF. This appears to be out-of-bounds array access when initializing the vector with begin == end.

std::vector<uint8_t> data(begin, end);

### gi...@appspot.gserviceaccount.com (2023-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c9d77da78bc66c135520ac77873d67b89cdcaee6

commit c9d77da78bc66c135520ac77873d67b89cdcaee6
Author: Matt Reynolds <mattreynolds@google.com>
Date: Thu Mar 02 02:29:24 2023

hid: Handle empty input reports

It's possible for a HID device to define its report descriptor such that
one or more reports have no data fields within the report. When receiving these reports, the report buffer should contain only the
report ID byte and no other data.

Ensure that we do not read past the end of the buffer when handling
zero-length input reports.

Bug: 1419718
Change-Id: I51d32c20f6b16f0d2b0172e0a165469b6b79748c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296562
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1112009}

[modify] https://crrev.com/c9d77da78bc66c135520ac77873d67b89cdcaee6/services/device/hid/hid_connection_impl.cc
[modify] https://crrev.com/c9d77da78bc66c135520ac77873d67b89cdcaee6/services/device/hid/hid_connection_impl_unittest.cc


### ma...@google.com (2023-03-02)

I confirmed this on a local developer build (ToT) using the userspace HID example provided above.

I don't have an easy way to confirm this on Windows or macOS since I don't have a device with the necessary behavior.

### [Deleted User] (2023-03-02)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2023-03-03)

I understand from the above comments that this is an old bug (introduced in M75), please correct me if I'm wrong.

I'm not sure how to rate severity. I'm going to tentatively mark as High severity under the grounds that connecting a malicious HID is a "specific user interaction". https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#toc-high-severity

### [Deleted User] (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-03)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

Requesting merge to extended stable M110 because latest trunk commit (1112009) appears to be after extended stable branch point (1084008).

Requesting merge to stable M111 because latest trunk commit (1112009) appears to be after stable branch point (1097615).

Requesting merge to dev M112 because latest trunk commit (1112009) appears to be after dev branch point (1109224).

Merge approved: your change passed merge requirements and is auto-approved for M112. Please go ahead and merge the CL to branch 5615 (refs/branch-heads/5615) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

Merge review required: M110 is already shipping to stable.

Merge review required: M111 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2023-03-03)

Created cherry-pick to refs/branch-heads/5615 (M112): https://crrev.com/c/4308533

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)

https://crrev.com/c/4296562

2. Has this fix been tested on Canary?

No, this bug requires a specific virtualized "device" which we don't have available on platforms with Canary builds. I've tested it with a ToT Linux build using the provided uhid-example.c.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

The fix only adds a buffer size check and should not cause any regressions.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

No.

### [Deleted User] (2023-03-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2023-03-07)

This bug has been approved for Merge to M112 , please help complete the merges asap so the change can get into the next M112 weekly beta release. ( M112 beta promotion is this thursday and weekly beta happens every wednesday after that) [Bulk Edit message]

### am...@chromium.org (2023-03-07)

M112 auto-approved (thanks for creating that CP already) so please merge to branch 5615 ASAP/ at soonest so this fix can be included in tomorrow's M112 last dev/first beta 

I feel conflicted on severity (and backmerge here); this feels closer to a medium severity issue given the preconditions and impact (not a UAF and without a stack trace I cannot ascertain the process impact). 

Given the relative safety/trivial nature of this fix, going to err on the side of caution and approve for backmerge to M111 and M110.
M111 merge approved, please merge this fix to branch 5563 
M110 merge approved, please merge this fix to branch 5481 

Please complete these merges at your earliest convenience so this fix can be included in the first M111/Stable and M110/Extended respins. TY! 

### am...@chromium.org (2023-03-07)

Hi OP, thank you for the report. 

>>>[no stack trace because I already have found the root cause of the bug.]

Please note, that is expected that reports of memory corruption bugs / crashes from triggering a security issue include an ASAN stack trace to be considered as a baseline quality report [1]. 
While identifying root cause and bisects are always greatly appreciated (and are part of our report quality and bonus structure for VRP rewards), and it was great this issue could be resolved in the absence of, they are an essential part of the security bug analysis and triage process. 
Please be sure to include a symbolized stack trace in all future reports of these types of bugs. Both triage and VRP reward potential can be impacted due to lack of stack trace. 

[1] https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#report-quality

### am...@chromium.org (2023-03-07)

oh yeah, it helps if I update the labels (also removing mattreynolds@ from accidental cc, they are already the owner here) 

### gi...@appspot.gserviceaccount.com (2023-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d4c564dbff808f00ec50026af55bbe0212e4d619

commit d4c564dbff808f00ec50026af55bbe0212e4d619
Author: Matt Reynolds <mattreynolds@google.com>
Date: Wed Mar 08 00:29:49 2023

hid: Handle empty input reports

It's possible for a HID device to define its report descriptor such that
one or more reports have no data fields within the report. When receiving these reports, the report buffer should contain only the
report ID byte and no other data.

Ensure that we do not read past the end of the buffer when handling
zero-length input reports.

(cherry picked from commit c9d77da78bc66c135520ac77873d67b89cdcaee6)

Bug: 1419718
Change-Id: I51d32c20f6b16f0d2b0172e0a165469b6b79748c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296562
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1112009}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4308533
Auto-Submit: Matt Reynolds <mattreynolds@chromium.org>
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/5615@{#279}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/d4c564dbff808f00ec50026af55bbe0212e4d619/services/device/hid/hid_connection_impl.cc
[modify] https://crrev.com/d4c564dbff808f00ec50026af55bbe0212e4d619/services/device/hid/hid_connection_impl_unittest.cc


### [Deleted User] (2023-03-08)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@google.com (2023-03-08)

> 1. Was this issue a regression for the milestone it was found in?

No, the regression was introduced in Chrome 75 and was found in a recent release (probably 111)

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No, the relevant feature is WebHID which shipped in Chrome 89.

### ma...@google.com (2023-03-08)

M110: https://crrev.com/c/4320692
M111: https://crrev.com/c/4320871

### gi...@appspot.gserviceaccount.com (2023-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5d38dd1ad5842a20186195b225e65a4a1efbb342

commit 5d38dd1ad5842a20186195b225e65a4a1efbb342
Author: Matt Reynolds <mattreynolds@google.com>
Date: Wed Mar 08 23:22:22 2023

[M-111] hid: Handle empty input reports

It's possible for a HID device to define its report descriptor
such that one or more reports have no data fields within the
report. When receiving these reports, the report buffer should
contain only the report ID byte and no other data.

Ensure that we do not read past the end of the buffer when
handling zero-length input reports.

(cherry picked from commit c9d77da78bc66c135520ac77873d67b89cdcaee6)

Bug: 1419718
Change-Id: I51d32c20f6b16f0d2b0172e0a165469b6b79748c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296562
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1112009}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4320871
Cr-Commit-Position: refs/branch-heads/5563@{#1105}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/5d38dd1ad5842a20186195b225e65a4a1efbb342/services/device/hid/hid_connection_impl.cc
[modify] https://crrev.com/5d38dd1ad5842a20186195b225e65a4a1efbb342/services/device/hid/hid_connection_impl_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b041159d06adbf7487639bd33a261cc0270d7a34

commit b041159d06adbf7487639bd33a261cc0270d7a34
Author: Matt Reynolds <mattreynolds@google.com>
Date: Wed Mar 08 23:55:10 2023

[M-110] hid: Handle empty input reports

It's possible for a HID device to define its report descriptor such that
one or more reports have no data fields within the report. When receiving these reports, the report buffer should contain only the
report ID byte and no other data.

Ensure that we do not read past the end of the buffer when handling
zero-length input reports.

(cherry picked from commit c9d77da78bc66c135520ac77873d67b89cdcaee6)

Bug: 1419718
Change-Id: I51d32c20f6b16f0d2b0172e0a165469b6b79748c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296562
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1112009}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4320692
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Auto-Submit: Matt Reynolds <mattreynolds@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#1341}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/b041159d06adbf7487639bd33a261cc0270d7a34/services/device/hid/hid_connection_impl.cc
[modify] https://crrev.com/b041159d06adbf7487639bd33a261cc0270d7a34/services/device/hid/hid_connection_impl_unittest.cc


### am...@google.com (2023-03-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-09)

Congratulations! The VRP Panel has decided to award you $8,000 for this report. A member of our finance team will reach out to you to arrange payment. In the meantime, please let us know what name/tag/handle or other identifier you would like us to use in acknowledging you for this finding. 
Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2023-03-11)

[Empty comment from Monorail migration]

### vo...@google.com (2023-03-14)

[Empty comment from Monorail migration]

### vo...@google.com (2023-03-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-14)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-03-15)

1. Just one https://crrev.com/c/4336541
2. Low - no conflicts
3. Merged to M110
4. Yes

### gm...@google.com (2023-03-16)

LTS: I don't think this made it out on 110 ChromeOS. Delaying.

### gm...@google.com (2023-03-16)

[Empty comment from Monorail migration]

### mo...@gmail.com (2023-03-17)

Hi Amyressler,

In the bug description, I have not yet received the following two rewards:

Bisect Bonus 
$2,000: For identifying the specific commit that introduced the bug and verifying which active release branches (dev/beta/stable) are impacted at the time of reporting. (In the report discription)

Patch Bonus 
$500-$2000: For providing a patch in the attachment.

Could you please check if there is any issue with the reward calculation?

Thank you.

### am...@chromium.org (2023-03-17)

Hello, thanks for reaching out. The reward calculation is correct. My apologies for not breaking that out for you in my https://crbug.com/chromium/1419718#c31. 

The reward amount was the combined reward for the report and bisect bonus $1000, since you just provided the commit that introduced this issue and did not include all the current / active release channels of Chrome browser impacted by the bug being reported (which would equate to a $2,000 bisect bonus, as per bisect bonus reward policies [1]) and absence of a stack trace displaying the specific memory corruption.)

A patch bonus was not extended since we did not end up using the patch you provided. [2]

[1] https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#bisect-bonus
[2] https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#patch-bonus


### mo...@gmail.com (2023-03-18)

Hi Amyressler,

In my previous comment (https://crbug.com/chromium/1419718#c4), I reported a bug I found in the latest version of Chrome. Since then, I discovered that the root cause patch was merged on M75. Therefore, I believe that this matches the criteria for the bisect bonus of $2000, due to the bug affecting the current release channels of Chrome browser.

Thank you.

### am...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-21)

Thank you for that information. There was no information (such as build / version numbers) or other details that clearly conveyed you tested that the issue presents in current dev, beta, or stable versions of Chrome, and since "Chrome Version: [x.x.x.x] + [stable, beta, dev]" are part of the bug reporting template.

We are happy to reassess at a future VRP Panel session. Any decision or change will be communicated here after that occurs. 
In the future, please do also include the symbolized stack trace as part of the report as that is part of the contributing characteristics expected for a baseline quality report. 

### pg...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-29)

Hello, the VRP Panel has reviewed the reward amount and more specifically the bisect bonus and we feel that the current reward amount and bisect bonus of $1,000 is sufficient for the information provide in the report and bisect. There was no analysis or other information provided to demonstrate or explain that this issue was reproducible in all the current active release channels and seems to be simply based on the commit and when the commit was introduced, which was already rewarded and covered by the $1,000 bisect bonus. 

The level of effort for the $2,000 bisect bonus - which is double for bisecting to the commit introducing the issue - is expected to provide that level of value to result in more effective triage and root cause analysis, such as demonstrating or providing output from testing to show that the issue reproduces in active release channels or providing explicit reproduction steps or analysis to show how the bug effects the different versions in particular, if necessary and applicable. 

### gm...@google.com (2023-03-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e8018f2187c8dc35123691a367d2555a1bf8a736

commit e8018f2187c8dc35123691a367d2555a1bf8a736
Author: Matt Reynolds <mattreynolds@google.com>
Date: Thu Mar 30 16:37:57 2023

[M108-LTS] hid: Handle empty input reports

It's possible for a HID device to define its report descriptor such that
one or more reports have no data fields within the report. When receiving these reports, the report buffer should contain only the
report ID byte and no other data.

Ensure that we do not read past the end of the buffer when handling
zero-length input reports.

(cherry picked from commit c9d77da78bc66c135520ac77873d67b89cdcaee6)

(cherry picked from commit b041159d06adbf7487639bd33a261cc0270d7a34)

Bug: 1419718
Change-Id: I51d32c20f6b16f0d2b0172e0a165469b6b79748c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4296562
Commit-Queue: Matt Reynolds <mattreynolds@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1112009}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4320692
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Auto-Submit: Matt Reynolds <mattreynolds@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/5481@{#1341}
Cr-Original-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4336541
Reviewed-by: Michael Ershov <miersh@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1422}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/e8018f2187c8dc35123691a367d2555a1bf8a736/services/device/hid/hid_connection_impl.cc
[modify] https://crrev.com/e8018f2187c8dc35123691a367d2555a1bf8a736/services/device/hid/hid_connection_impl_unittest.cc


### vo...@google.com (2023-03-30)

[Empty comment from Monorail migration]

### mo...@gmail.com (2023-04-05)

Hi Amyressler,

I am writing to express my gratitude for the generous bisect bonus of $1000. Your kindness and thoughtfulness are greatly appreciated.

Please let me know if there are any specific action items or tasks that I need to complete in response to this bonus. I am eager to fulfill any requirements or expectations that may accompany it.

Thank you again for your generosity.

### am...@chromium.org (2023-04-05)

[Comment Deleted]

### am...@chromium.org (2023-04-05)

Hello, there is no action or tasks you need to complete here to receive you reward. The bisect bonus of $1,000 was included in the original reward amount of $8000 ($7,000 for bug report + $1,000 bisect bonus) and that information was sent over the the finance team for payment processing on 10 March. As mentioned in https://crbug.com/chromium/1419718#c31, a member of the finance team should have been in touch with you. The p2p-vrp finance team has confirmed they reached out to you on 13 March. Please be sure to respond to their emails and fill out the appropriate forms so that you can be enrolled in the Google payment system in order to receive your reward payment.

### [Deleted User] (2023-06-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1419718?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063257)*
