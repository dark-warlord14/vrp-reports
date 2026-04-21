# Security: Privilege escalation via command execution in crosh / top

| Field | Value |
|-------|-------|
| **Issue ID** | [40086377](https://issues.chromium.org/issues/40086377) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | mn...@chromium.org |
| **Assignee** | va...@chromium.org |
| **Created** | 2017-01-03 |
| **Bounty** | $5,000.00 |

## Description

top, which is available via crosh executes arbitrary commands via its configuration file /home/chronos/user/.toprc. The latter is chronos-writable, which allows an attacker with an arbitrary file write vulnerability to gain code execution as chronos.

We should add safeguards that help ensure crosh commands can't be used to spawn shells or other attacker-controlled code. Perhaps we can run crosh commands within a minijail sandbox that doesn't allow exec() or puts stuff into a chroot that doesn't contain executable binaries?

vapier@, what's your take? Also, who's a good owner for this?

(See https://crbug.com/chromium/677817 for background)

## Timeline

### sh...@chromium.org (2017-01-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-03)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-01-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/37b20658f3e9f801604d9d5d41d8e939bf9ce59f

commit 37b20658f3e9f801604d9d5d41d8e939bf9ce59f
Author: Mike Frysinger <vapier@chromium.org>
Date: Tue Jan 03 16:18:58 2017

init: make sure stateful dirs are not symlinks

None of the dirs we create in the stateful should be symlinks.

BUG=chromium:677934
TEST=precq passes
TEST=booted on a system and it didn't recreate paths

Change-Id: I17fec46bc4b44f6fa84057f74baf6430ea14d529
Reviewed-on: https://chromium-review.googlesource.com/422628
Commit-Ready: Mike Frysinger <vapier@chromium.org>
Tested-by: Mike Frysinger <vapier@chromium.org>
Reviewed-by: Mattias Nissler <mnissler@chromium.org>

[modify] https://crrev.com/37b20658f3e9f801604d9d5d41d8e939bf9ce59f/init/chromeos_startup


### bu...@chromium.org (2017-01-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/c446013ceaae05128b1a5abc8d1070ffd826ff95

commit c446013ceaae05128b1a5abc8d1070ffd826ff95
Author: Mike Frysinger <vapier@chromium.org>
Date: Tue Jan 03 16:14:32 2017

crosh: force top to run with empty HOME

BUG=chromium:677934
TEST=ran top and it still worked

Change-Id: Ie1e15428c0b7d6176acad82bf4ae876cf9356fc0
Reviewed-on: https://chromium-review.googlesource.com/424632
Commit-Ready: Mike Frysinger <vapier@chromium.org>
Tested-by: Mike Frysinger <vapier@chromium.org>
Reviewed-by: Mattias Nissler <mnissler@chromium.org>

[modify] https://crrev.com/c446013ceaae05128b1a5abc8d1070ffd826ff95/crosh/crosh


### va...@chromium.org (2017-01-04)

risk should be low, but this could be used to bypass enrollment

### sh...@chromium.org (2017-01-05)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-05)

Your change meets the bar and is auto-approved for M56. Please go ahead and merge the CL manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/b7cf5887f6e9ec08a08397b0aca210fbd041aa2b

commit b7cf5887f6e9ec08a08397b0aca210fbd041aa2b
Author: Mike Frysinger <vapier@chromium.org>
Date: Tue Jan 03 16:18:58 2017

init: make sure stateful dirs are not symlinks

None of the dirs we create in the stateful should be symlinks.

BUG=chromium:677934
TEST=precq passes
TEST=booted on a system and it didn't recreate paths

Change-Id: I17fec46bc4b44f6fa84057f74baf6430ea14d529
(cherry picked from commit 37b20658f3e9f801604d9d5d41d8e939bf9ce59f)
Reviewed-on: https://chromium-review.googlesource.com/425656
Reviewed-by: Mike Frysinger <vapier@chromium.org>
Tested-by: Mike Frysinger <vapier@chromium.org>

[modify] https://crrev.com/b7cf5887f6e9ec08a08397b0aca210fbd041aa2b/init/chromeos_startup


### bu...@chromium.org (2017-01-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/57da9dfe3a043f3e0ceed703441ecacde3c3675c

commit 57da9dfe3a043f3e0ceed703441ecacde3c3675c
Author: Mike Frysinger <vapier@chromium.org>
Date: Tue Jan 03 16:14:32 2017

crosh: force top to run with empty HOME

BUG=chromium:677934
TEST=ran top and it still worked

Change-Id: Ie1e15428c0b7d6176acad82bf4ae876cf9356fc0
(cherry picked from commit c446013ceaae05128b1a5abc8d1070ffd826ff95)
Reviewed-on: https://chromium-review.googlesource.com/425657
Reviewed-by: Mike Frysinger <vapier@chromium.org>
Tested-by: Mike Frysinger <vapier@chromium.org>

[modify] https://crrev.com/57da9dfe3a043f3e0ceed703441ecacde3c3675c/crosh/crosh


### sh...@chromium.org (2017-01-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-09)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2017-01-12)

stupid security bot

### bu...@chromium.org (2017-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/0da769c9440a2834b609a41e2aeed0827d95bf32

commit 0da769c9440a2834b609a41e2aeed0827d95bf32
Author: Mike Frysinger <vapier@chromium.org>
Date: Tue Jan 03 16:27:07 2017

init: make sure /var/empty/ stays empty

Since /var/empty/ is on the stateful partition, there is a chance that
content is added to it.  Mark it immutable using ext4 bits to prevent
that from happening.

BUG=chromium:677934
TEST=precq passes
TEST=reboots on same system still work, and /var/empty is immutable

Change-Id: Id11b88431597f4323a0cb71be8920edf41e30952
Reviewed-on: https://chromium-review.googlesource.com/423409
Commit-Ready: Mike Frysinger <vapier@chromium.org>
Tested-by: Mike Frysinger <vapier@chromium.org>
Reviewed-by: Mattias Nissler <mnissler@chromium.org>

[modify] https://crrev.com/0da769c9440a2834b609a41e2aeed0827d95bf32/init/chromeos_startup


### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-02-01)

the fix is in M56, but apparently no one wants to approve M55 anymore, so assuming we'll leave it vulnerable

### sh...@chromium.org (2017-03-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-06-06)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-06-26)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-18)

Congratulations! The VRP panel decided to award $5,000 for this report!  A member of our finance team will be in touch to arrange for payment.

### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### ro...@rorym.cnamara.com (2017-09-21)

Thanks!

### dc...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-06-21)

[Empty comment from Monorail migration]

### is...@google.com (2018-06-21)

This issue was migrated from crbug.com/chromium/677934?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/677817]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086377)*
