# Security: An <option> with a long label causes browser crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40056127](https://issues.chromium.org/issues/40056127) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Forms>Select, Internals>GPU |
| **Platforms** | Linux |
| **Reporter** | ba...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2021-06-06 |
| **Bounty** | $6,000.00 |

## Description

**VULNERABILITY DETAILS**

As an R&D team in securityforeveryone.com, we found a crash bug in Chrome's latest version.

While developing our project, we accidentally use a debug output in the option part of a select form.

Then we realize that each time we select that option, our chrome process and our operating system have crashed.

We are not sure, but we think that this bug may lead to RCE.

We are adding only one HTML page to reproduce this bug.

Also, we tried for both Windows, Linux, and OS X. It seems only the Linux version is affected.

**VERSION**  

Chrome Version: [91.0.4472.77] + [stable] (Official Build) (64-bit)  

Operating System: [Kali GNU/Linux version 2020.1, Ubuntu version 20.04.2 LTS, Ubuntu version 20.04.1 LTS]

**REPRODUCTION CASE**  

Open poc-exploit.html in the related environment.  

Click the selective box (a bunch of AAAA.)  

Wait  

OS and Browser Process should be freeze and crash.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Browser and OS  

No crash ID is available, also no crash dump files in our env.

**CREDIT INFORMATION**  

Reporter credit: [Security For Everyone Team - https://securityforeveryone.com/]

## Attachments

- [chrome.mp4](attachments/chrome.mp4) (video/mp4, 1.2 MB)
- [poc-exploit.html](attachments/poc-exploit.html) (text/plain, 9.9 KB)
- [crash1.png](attachments/crash1.png) (image/png, 48.6 KB)
- [crash2.png](attachments/crash2.png) (image/png, 161.5 KB)
- [crash3.png](attachments/crash3.png) (image/png, 166.4 KB)
- [st.png](attachments/st.png) (image/png, 59.3 KB)
- [release.png](attachments/release.png) (image/png, 115.7 KB)
- [error.png](attachments/error.png) (image/png, 66.2 KB)
- [console-log.txt](attachments/console-log.txt) (text/plain, 41.7 KB)
- [Chrome_wide_window.mp4](attachments/Chrome_wide_window.mp4) (video/mp4, 9.6 MB)

## Timeline

### [Deleted User] (2021-06-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-06-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5117398366355456.

### bd...@chromium.org (2021-06-07)

I tried it on Linux with Chrome version 91.0.4472.77 (Official Build) (64-bit) using the poc-exploit.html but could not repro it unfortunately. Can you try again and see?

### ba...@gmail.com (2021-06-07)

Hello there,
I tried it in Ubuntu 20.04.1 and got the same result. I am sharing the details of the crash report to help.

### bd...@chromium.org (2021-06-08)

Thanks for the logs! Could you try this with an Asan build? https://commondatastorage.googleapis.com/chromium-browser-asan/index.html

### bd...@chromium.org (2021-06-08)

[Empty comment from Monorail migration]

### ba...@gmail.com (2021-06-08)

[Comment Deleted]

### [Deleted User] (2021-06-08)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ba...@gmail.com (2021-06-08)

We tried exploit in latest Chrome stable version. We still get crash in latest Chrome version. We tried exploit in latest Asan version. We don’t get crash but we get error at console log. We attached related screenshot and console log.

### bd...@chromium.org (2021-06-08)

Thank you for the logs!

@penghuang can you look into this (found you through blame in makecontextcurrent method)

[Monorail components: Internals>GPU]

### [Deleted User] (2021-06-09)

[Empty comment from Monorail migration]

### ba...@gmail.com (2021-06-10)

Hello, any update?

### mp...@chromium.org (2021-06-10)

Also adding weiliangc@ for more eyes. Seems like it's causing a UAF in the GPU process from minimal user interaction (might also be possible via Javascript), so I'll mark this as high severity.

### ba...@gmail.com (2021-06-12)

Hello, any update?

### pe...@chromium.org (2021-06-14)

Just reproduced it. Investigating it now.

### pe...@chromium.org (2021-06-14)

Looks like, when the option is clicked, chrome will create a new popup Window which size is 106733x23. It is too wide. When chrome creates this really wide window and GLSurface it causes the the Xserver hang (my Xserver will start show garbage see the attached video). And I believe the error in https://crbug.com/chromium/1216822#c9 is not related. I think it is better to fix it in blink, probably blink should check screen size, and create the popup window with a proper size.

### pe...@chromium.org (2021-06-14)

BTW, my desktop environment is:
penghuang@penghuang-linux:~/sources/chromium/src/third_party/blink$ neofetch 
       _,met$$$$$gg.          penghuang@penghuang-linux 
    ,g$$$$$$$$$$$$$$$P.       ------------------------- 
  ,g$$P"     """Y$$.".        OS: Debian GNU/Linux rodete x86_64 
 ,$$P'              `$$$.     Host: HP Z840 Workstation 
',$$P       ,ggs.     `$$b:   Kernel: 5.10.28-1rodete1-amd64 
`d$$'     ,$P"'   .    $$$    Uptime: 15 days, 18 hours, 10 mins 
 $$P      d$'     ,    $$P    Packages: 2959 (dpkg) 
 $$:      $$.   -    ,d$$'    Shell: bash 5.1.4 
 $$;      Y$b._   _,d$P'      Resolution: 3840x2160 
 Y$$.    `.`"Y$$$$P"'         DE: GNOME 3.38.4 
 `$$b      "-.__              WM: Mutter 
  `Y$$                        WM Theme: Adwaita 
   `Y$$.                      Theme: Adwaita-dark [GTK2/3] 
     `$$b.                    Icons: Adwaita [GTK2/3] 
       `Y$$b.                 Terminal: gnome-terminal 
          `"Y$b._             CPU: Intel Xeon E5-2690 v4 (28) @ 1.198GHz 
              `"""            GPU: NVIDIA GeForce GTX 745 
                              Memory: 12433MiB / 128823MiB 

                                                      
                                                      


### ba...@gmail.com (2021-06-14)

Hi, all right, what happens now?

### pe...@chromium.org (2021-06-14)

Assign it to tkent@ who modified code related option element.

Hi tkent@ could you please take a look this issue or triage it to someone who can fix the problem in blink? Thanks.

### tk...@chromium.org (2021-06-14)

Mason, would you triage this please?


[Monorail components: Blink>Forms>Select]

### [Deleted User] (2021-06-15)

[Empty comment from Monorail migration]

### ma...@chromium.org (2021-06-16)

Interesting crash! One quick thing to sort out here - the log in https://crbug.com/chromium/1216822#c9 has a UAF that seems repeatable. https://crbug.com/chromium/1216822#c16 has a great analysis of the bug here, and I can take a look at putting a cap on the size of the option. But it also says https://crbug.com/chromium/1216822#c9 is unrelated. Should we open a fresh bug for that (serious, UAF) issue?



### ba...@gmail.com (2021-06-18)

Hello, any update?

### pe...@chromium.org (2021-06-18)

FYI. for the UAF problem. I think the GPU context has been marked lost (probably due to the super wide popup window), and the GPU process should be in the teardown process, and then a new GPU process will be created. I will file a new issue for it.

### gi...@appspot.gserviceaccount.com (2021-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/38b4905f8d877b27bc2d4ccd4cfc0f82b636deea

commit 38b4905f8d877b27bc2d4ccd4cfc0f82b636deea
Author: Peng Huang <penghuang@chromium.org>
Date: Fri Jun 18 21:20:09 2021

Fix UAF problem in SharedImageInterfaceInProcess

Bug: 1216822
Change-Id: I8ae1f7c406e1899e500ee7ddeaaf18230b1cbcb2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2971144
Commit-Queue: Peng Huang <penghuang@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Auto-Submit: Peng Huang <penghuang@chromium.org>
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#893931}

[modify] https://crrev.com/38b4905f8d877b27bc2d4ccd4cfc0f82b636deea/gpu/ipc/shared_image_interface_in_process.cc
[modify] https://crrev.com/38b4905f8d877b27bc2d4ccd4cfc0f82b636deea/gpu/ipc/shared_image_interface_in_process.h


### ma...@chromium.org (2021-06-18)

Ok, had a chance to look at this. So my hypothesis is that this is related to this fix:

  https://chromium-review.googlesource.com/c/chromium/src/+/1455518

I cannot reproduce this anywhere but Linux, and the code [1] should take care of limiting the popup window to the window width, except in the special case added by the CL above.

thomasanderson@ I'm hoping I can assign this over to you to take a look? Not sure what the fix is going to be, if you can't end up getting window dimensions reliably. Perhaps just set a fixed max (10k pixels?) or something?

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/forms/resources/pickerCommon.js;l=180;drc=972aab37ea418c88ab54c752b77b4256e2001441

### [Deleted User] (2021-06-20)

thomasanderson: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### th...@chromium.org (2021-06-21)

I think [1] is no longer necessary and can be reverted.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/1455518

### gi...@appspot.gserviceaccount.com (2021-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8d16f621fa982e656664077cdaa80d09a44de9ce

commit 8d16f621fa982e656664077cdaa80d09a44de9ce
Author: Tom Anderson <thomasanderson@chromium.org>
Date: Tue Jun 22 00:02:35 2021

Revert "Add a fallback path for SELECT window size when there's no available space"

Reason for revert:  The workaround is no longer necessary after [1]

[1] https://chromium-review.googlesource.com/c/chromium/src/+/1457462

> Some buggy window managers on Linux (https://crbug.com/chromium/774232) have an improperly set screen
> workarea that's empty on secondary displays.  This CL adds a fallback path for
> this case to prevent rendering issues on select dropdowns.
>
> BUG=774232
>
> Change-Id: I7188418b2e737478307663652ccaef48594b1696
> Reviewed-on: https://chromium-review.googlesource.com/c/1455518
> Commit-Queue: Kent Tamura <tkent@chromium.org>
> Reviewed-by: Kent Tamura <tkent@chromium.org>
> Auto-Submit: Thomas Anderson <thomasanderson@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#630215}

BUG=1216822
R=tkent

Change-Id: I65208990c7d15d23bdb6c449b91f81abc9b8af87
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2976081
Auto-Submit: Thomas Anderson <thomasanderson@chromium.org>
Commit-Queue: Kent Tamura <tkent@chromium.org>
Reviewed-by: Kent Tamura <tkent@chromium.org>
Cr-Commit-Position: refs/heads/master@{#894465}

[modify] https://crrev.com/8d16f621fa982e656664077cdaa80d09a44de9ce/third_party/blink/renderer/core/html/forms/resources/pickerCommon.js
[modify] https://crrev.com/8d16f621fa982e656664077cdaa80d09a44de9ce/third_party/blink/web_tests/fast/forms/page-popup/page-popup-adjust-rect-expected.txt
[modify] https://crrev.com/8d16f621fa982e656664077cdaa80d09a44de9ce/third_party/blink/web_tests/fast/forms/page-popup/page-popup-adjust-rect.html


### th...@chromium.org (2021-06-22)

reporter: are you able to verify the issue is fixed after 8d16f621fa982e656664077cdaa80d09a44de9ce

### ba...@gmail.com (2021-06-27)

Hi any update?

### th...@chromium.org (2021-06-28)

The CL has already landed.  Please see https://crbug.com/chromium/1216822#c31.  Can you check if the issue still reproduces now?

### ba...@gmail.com (2021-07-01)

The security vulnerability appears to have been fixed.  Can you help with bounty or hall of fame or backlink?

### th...@chromium.org (2021-07-01)

Thanks for verifying.  Bug bounty is up to the security team.

### [Deleted User] (2021-07-01)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and Security_Impact labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues Impact guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-07-01)

based on all the above (and that this appears to be a high severity UAF bug), updating to Security_Impact-Stable/FoundIn-91 so that Sheriffbot can kick off merge requests. thomasanderson@, if you agree with this, please re-update this bug as Fixed. Thank you! 

### th...@chromium.org (2021-07-01)

Reassigning to masonf@ to answer c#36.  I just created the revert; masonf@ will know the details better than I.

### [Deleted User] (2021-07-03)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-07-04)

masonf: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2021-07-07)

This bug has been around since Chromium 74.0.3700.0, and is Linux only. It is really two bugs, one is a UAF and the other is a browser crash. The UAF bug fix should likely be merged, but the browser crash likely doesn't need a merge.

Given the above, I'll add a merge request for https://crbug.com/chromium/1216822#c25 to M92 Beta.

### [Deleted User] (2021-07-07)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-07-07)

Approving merge of https://crbug.com/chromium/1216822#c25 to M92, branch 4515.

Based on https://crbug.com/chromium/1216822#c35 and https://crbug.com/chromium/1216822#c36 I think this is Fixed.

### pb...@google.com (2021-07-07)

Changing the label to Merge-Approved-92 based on https://crbug.com/chromium/1216822#c42. 

### ma...@chromium.org (2021-07-07)

Merge in review: https://chromium-review.googlesource.com/c/chromium/src/+/3011895

### gi...@appspot.gserviceaccount.com (2021-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cd98d7c0dae974428f2b7692b010dd62aba3d3c4

commit cd98d7c0dae974428f2b7692b010dd62aba3d3c4
Author: Peng Huang <penghuang@chromium.org>
Date: Wed Jul 07 20:50:53 2021

Fix UAF problem in SharedImageInterfaceInProcess

(cherry picked from commit 38b4905f8d877b27bc2d4ccd4cfc0f82b636deea)

Bug: 1216822
Change-Id: I8ae1f7c406e1899e500ee7ddeaaf18230b1cbcb2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2971144
Commit-Queue: Peng Huang <penghuang@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Auto-Submit: Peng Huang <penghuang@chromium.org>
Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#893931}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3011895
Auto-Submit: Mason Freed <masonf@chromium.org>
Reviewed-by: Peng Huang <penghuang@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#1369}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/cd98d7c0dae974428f2b7692b010dd62aba3d3c4/gpu/ipc/shared_image_interface_in_process.cc
[modify] https://crrev.com/cd98d7c0dae974428f2b7692b010dd62aba3d3c4/gpu/ipc/shared_image_interface_in_process.h


### ba...@gmail.com (2021-07-08)

hi, any update?

### [Deleted User] (2021-07-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-08)

[Empty comment from Monorail migration]

### ba...@gmail.com (2021-07-13)

Hi any update for bounty?

### tk...@chromium.org (2021-07-13)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-14)

Thank you for this report! The bug report will also be considered and evaluated for a potential bug bounty by the VRP Panel (Vulnerability Rewards Program) within the coming weeks. Once a reward decision has been made, that will be updated here. This tracker system will push an email to you with that update, same as other comments or updates to this report. Thank you for your patience! 

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-22)

Congratulations! The VRP Panel has decided to award you $6,000 for this report. A member of our finance team will be in touch soon to arrange payment. Nice work! 

### am...@google.com (2021-07-23)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### ad...@google.com (2021-08-03)

(this comment is primarily for my own notes because I'm bound to come back to this and be confused!)

I'm digging into the root cause here for some security bug analyses, and I disagree that this CL is the regression which caused this:
https://chromium-review.googlesource.com/c/chromium/src/+/1455518

Even without that CL, a compromised renderer could presumably have caused the GPU process to hit this UaF, so the security risk was pre-existing.

### ba...@gmail.com (2021-08-03)

So what about the bounty process?

### am...@chromium.org (2021-08-03)

Hi bartusarp@, the VRP reward decision was made on 22 July (please see comment # 54 and https://crbug.com/chromium/1216822#c55). According to finance, they reached out with an enrollment invite (sent to the email address you used to report this bug here), on 1 August 2021. You'll need to follow the instructions in that enrollment email from finance so they can arrange for payment. 
Please let me know if you have any specific questions about the VRP process. Thank you. 

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-09)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/186264aa996c8ab8747824e30e1b43d7bb936b4e

commit 186264aa996c8ab8747824e30e1b43d7bb936b4e
Author: Peng Huang <penghuang@chromium.org>
Date: Tue Aug 17 15:59:40 2021

[M90-LTS] Fix UAF problem in SharedImageInterfaceInProcess

(cherry picked from commit 38b4905f8d877b27bc2d4ccd4cfc0f82b636deea)

Bug: 1216822
Change-Id: I8ae1f7c406e1899e500ee7ddeaaf18230b1cbcb2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2971144
Commit-Queue: Peng Huang <penghuang@chromium.org>
Commit-Queue: Vasiliy Telezhnikov <vasilyt@chromium.org>
Auto-Submit: Peng Huang <penghuang@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#893931}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3059449
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1567}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/186264aa996c8ab8747824e30e1b43d7bb936b4e/gpu/ipc/shared_image_interface_in_process.cc
[modify] https://crrev.com/186264aa996c8ab8747824e30e1b43d7bb936b4e/gpu/ipc/shared_image_interface_in_process.h


### rz...@google.com (2021-08-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1216822?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>Select, Internals>GPU]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056127)*
