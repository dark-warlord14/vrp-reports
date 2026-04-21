# Security: ChromeOS On halt/reboot root file overwrite

| Field | Value |
|-------|-------|
| **Issue ID** | [40062106](https://issues.chromium.org/issues/40062106) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | al...@google.com |
| **Created** | 2022-12-07 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

chromeos\_shutdown calls bootstat\_archive with a chronos-controlled target directory, which is used to copy a set of files from /tmp. Chronos can set up this target directory before bootstat\_archive is executed to cause bootstat\_archive to write arbitrary file contents through a symbolic link.

**VERSION**  

Google Chrome 107.0.5304.110 (Official Build) (64-bit)  

Revision 2a558545ab7e6fb8177002bf44d4fc1717cb2998-refs/branch-heads/5304@{#1202}  

Platform 15117.112.0 (Official Build) stable-channel eve  

Firmware Version Google\_Eve.9584.230.0

**REPRODUCTION CASE**  

Execute the following shell script, which will trigger a reboot.

echo EXPLOIT > /tmp/disk-messages

for offset in `seq 0 60`; do  

TGT=/var/log/metrics/shutdown.$(date --date="+$offset sec" '+%Y%m%d%H%M%S')  

mkdir ${TGT}  

ln -s /var/log/messages ${TGT}/disk-messages  

done

dbus-send --print-reply --system --dest=org.chromium.PowerManager /org/chromium/PowerManager org.chromium.PowerManager.RequestRestart uint32:0 string:

Post-reboot, observe that the contents of /var/log/messages have been overwritten with the controlled ‘EXPLOIT’ value (later values are added as part of normal bootup, but the ‘EXPLOIT’ value should be the first line)

DETAILS  

As part of shutdown, chromeos\_shutdown will call bootstat\_archive [1] with a parent directory of /var/log/metrics/. This directory is owned by chronos. The chronos user can set up directories matching the timestamp “/var/log/metrics/shutdown.$(date '+%Y%m%d%H%M%S')” which contain symbolic links. When bootstat\_archive is then run as part of shutdown it will perform an unsafe copy from /tmp into this directory [2]. A controlled /tmp/disk-\* file will be copied to /var/log/metrics/shutdown.[timestamp]/disk-\* as root. This can result in arbitrary file writes as root during shutdown.

The above proof of concept will create 60 timestamped directories to allow for a slower shutdown (i.e the next minute of bootstat\_archive runs). A file is created at /tmp/disk-messages (an unused disk- filename) and a symlink at /var/log/metrics/shutdown.[timestamp]/disk-messages to control both the contents and the targeted file of the file write.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/init/chromeos_shutdown#129>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/bootstat/bootstat_archive#26>

Requirements

- None

Impact

- Arbitrary file overwrite as root. Due to the late stage of this execution during system shutdown, this cannot be reasonably used as part of the current boot and therefore can only target files on disk (not, for example, files in /proc).

Recommendation

- Add --remove-destination to cp or change the target directory to one that cannot be controlled by chronos

## Timeline

### [Deleted User] (2022-12-07)

[Empty comment from Monorail migration]

### ad...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-09)

Hi Allen, I saw you touched chromeos_shutdown at some point, can you help me to route this bug?

[Monorail components: Security]

### le...@google.com (2022-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### le...@google.com (2022-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-22)

allenwebb: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@google.com (2022-12-22)

I think the fix for this is to update bootstat to accept the destination path as a command line switch so there is no need to copy the results. We can then use SafeFD to validate the paths.

### br...@chromium.org (2022-12-22)

> I think the fix for this is to update bootstat to accept the destination path as a command line switch so there is no need to copy the results.

There are various non-root callers of `boostat` (or its equivalent library functions; and even a separate implementation in Chrome...). So you'd have to open up the permissions of the target directory too, which probably defeats the purpose.

I think you either need to harden the copy (in `bootstat_archive`), like suggest in the OP, or else add some privilege delegation, so that we don't need such wide permissions for the file locations. The latter would be complex, since some of the bootstat entries need to be generated rather early, probably before we're running most D-Bus services.

### al...@google.com (2022-12-22)

I wasn't aware of the non-root callers, so that makes sense.

Adding "--remove-destination" is fine for solving symlink issues with the last path component of the copy operation, but we also need to take the mkdir into account. I think a tmpfiles.d rule for the parent path, plus some checks might do a reasonable job.

### al...@google.com (2022-12-22)

`/var/log/metrics` is already covered by tmpfiles.d. There is also code in chromeos_shutdown that handles creating ${PRESERVE_DIR}/log (but not the metrics sub directory).

### gi...@appspot.gserviceaccount.com (2023-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/e5a45a77fc5a37622cb250ec257c727244f8a0c5

commit e5a45a77fc5a37622cb250ec257c727244f8a0c5
Author: Allen Webb <allenwebb@google.com>
Date: Thu Dec 22 21:42:19 2022

bootstat: Make bootstat_archive symlink resistant.

This makes it harder to use symlinks to confuse bootstat_archive.

BUG=chromium:1398989
TEST=bootstat_archive <path with symlink> &&
  bootstat_archive <path without symlink>

Change-Id: I4437978de7e98398d28c4c5fdce24c73013456d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4122219
Tested-by: Allen Webb <allenwebb@google.com>
Reviewed-by: Brian Norris <briannorris@chromium.org>
Reviewed-by: Hidehiko Abe <hidehiko@chromium.org>
Commit-Queue: Allen Webb <allenwebb@google.com>

[modify] https://crrev.com/e5a45a77fc5a37622cb250ec257c727244f8a0c5/bootstat/bootstat_archive


### al...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### al...@google.com (2023-01-06)

After this is on top-of-tree for a week or so we can probably consider cherry-picking it to 109.

### [Deleted User] (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-06)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M109. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-07)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M109. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-08)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M109. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ce...@google.com (2023-01-09)

Not sure why sheriffbot is posting so many questionnaires.

Please complete the questionnaire ASAP and prep the cherry-picks. All channels are being promoted this week and this could delay release qualification.

Thanks!

Cole

### [Deleted User] (2023-01-09)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M109. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@google.com (2023-01-10)

> 1. Which CLs should be backmerged? (Please include Gerrit links.)
https://crrev.com/c/4122219


> 2. Has this fix been tested on Canary?

The fix landed in 15306.0.0 (1/7) and was included in a Canary build.

> 3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

None are anticipated and so far there hasn't been evidence of a stability regression.

> 4. Does this fix pose any known compatibility risks?

No

> 5. Does it require manual verification by the test team? If so, please describe required testing.

No


### [Deleted User] (2023-01-10)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M109. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [109, 110].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ce...@google.com (2023-01-10)

Merge approved for M-110.

Merge Category: Security issue.

### ma...@google.com (2023-01-12)

Approved, M109.

Category: Security fix

### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations, Rory! The VRP Panel has decided to award you $20,000 for this report - or 0.667 Rory. :) Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### ro...@rorym.cnamara.com (2023-01-12)

Thank you!

### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/682dc8b9ce288f097aedce5a5b2f3023dee17eb4

commit 682dc8b9ce288f097aedce5a5b2f3023dee17eb4
Author: Allen Webb <allenwebb@google.com>
Date: Thu Dec 22 21:42:19 2022

bootstat: Make bootstat_archive symlink resistant.

This makes it harder to use symlinks to confuse bootstat_archive.

BUG=chromium:1398989
TEST=bootstat_archive <path with symlink> &&
  bootstat_archive <path without symlink>

Change-Id: I4437978de7e98398d28c4c5fdce24c73013456d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4122219
Tested-by: Allen Webb <allenwebb@google.com>
Reviewed-by: Brian Norris <briannorris@chromium.org>
Reviewed-by: Hidehiko Abe <hidehiko@chromium.org>
Commit-Queue: Allen Webb <allenwebb@google.com>
(cherry picked from commit e5a45a77fc5a37622cb250ec257c727244f8a0c5)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4162964
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Allen Webb <allenwebb@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/682dc8b9ce288f097aedce5a5b2f3023dee17eb4/bootstat/bootstat_archive


### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/789f9907d43f1365016216146f0683443e6e7f2d

commit 789f9907d43f1365016216146f0683443e6e7f2d
Author: Allen Webb <allenwebb@google.com>
Date: Thu Dec 22 21:42:19 2022

bootstat: Make bootstat_archive symlink resistant.

This makes it harder to use symlinks to confuse bootstat_archive.

BUG=chromium:1398989
TEST=bootstat_archive <path with symlink> &&
  bootstat_archive <path without symlink>

Change-Id: I4437978de7e98398d28c4c5fdce24c73013456d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4122219
Tested-by: Allen Webb <allenwebb@google.com>
Reviewed-by: Brian Norris <briannorris@chromium.org>
Reviewed-by: Hidehiko Abe <hidehiko@chromium.org>
Commit-Queue: Allen Webb <allenwebb@google.com>
(cherry picked from commit e5a45a77fc5a37622cb250ec257c727244f8a0c5)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4162965
Auto-Submit: Allen Webb <allenwebb@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/789f9907d43f1365016216146f0683443e6e7f2d/bootstat/bootstat_archive


### gi...@appspot.gserviceaccount.com (2023-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/682dc8b9ce288f097aedce5a5b2f3023dee17eb4

commit 682dc8b9ce288f097aedce5a5b2f3023dee17eb4
Author: Allen Webb <allenwebb@google.com>
Date: Thu Dec 22 21:42:19 2022

bootstat: Make bootstat_archive symlink resistant.

This makes it harder to use symlinks to confuse bootstat_archive.

BUG=chromium:1398989
TEST=bootstat_archive <path with symlink> &&
  bootstat_archive <path without symlink>

Change-Id: I4437978de7e98398d28c4c5fdce24c73013456d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4122219
Tested-by: Allen Webb <allenwebb@google.com>
Reviewed-by: Brian Norris <briannorris@chromium.org>
Reviewed-by: Hidehiko Abe <hidehiko@chromium.org>
Commit-Queue: Allen Webb <allenwebb@google.com>
(cherry picked from commit e5a45a77fc5a37622cb250ec257c727244f8a0c5)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4162964
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Auto-Submit: Allen Webb <allenwebb@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>

[modify] https://crrev.com/682dc8b9ce288f097aedce5a5b2f3023dee17eb4/bootstat/bootstat_archive


### al...@google.com (2023-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1398989?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062106)*
