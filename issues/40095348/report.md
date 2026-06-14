# Security: Multiple vulnerabilities in chromeos-disk-firmware.sh

| Field | Value |
|-------|-------|
| **Issue ID** | [40095348](https://issues.chromium.org/issues/40095348) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | tm...@gmail.com |
| **Assignee** | gw...@chromium.org |
| **Created** | 2019-06-10 |
| **Bounty** | $1,000.00 |

## Description

The chromeos-disk-firmware-update.sh[1] script is called at boot from chromeos-disk-firmware-update.conf[2] during init. It is used to check for updates in the root disk firmware.

To actually exploit these issues, an attacker requires the following:
1) Deleting the /mnt/stateful_partition/unencrypted/cache/.disk_firmware_upgrade_completed file. (See [2] line 23). This will guarantee the script runs at boot
2) The attacker must know the location of the FLAGS_tmp_dir to know where to write their malicious files

If an attacker can fulfill the above two requirements, I believe they would be able to persist Guest-to-Guest, and potentially even after updates and upgrades have been performed. 

Vulnerability #1
The first vulnerability lies in the disk_mmc_upgrade function, where on line 468 the ${option} parameter is unquoted[3], allowing for expansions to take place. To note, this vulnerability has the additional requirement of the presence of a MMC disk.

The reading of the rules file takes place in disk_fw_select[4], which takes values from the disk_rules file. The disk_rules file is created in main, by sed'ing the contents of disk_rules_raw[5] (a passed in value, at boot time this resides at /opt/google/disk/firmware/rules, declared in the above .conf script). 

The ${option} parameter is effectively the 4th word on each line. Words are space delimited, however before the options are passed to the mmc binary, they are passed through a sed command[6] which will replace all commas with a " -k <word>", allowing an attacker to add multiple key-value pairs to the command. This key must always be ffu_arg, or else mmc will exit early.

Without any other vulnerabilities, this would only allow an attacker to prevent the device from being updated by supplying a file that has the fourth word containing two commas next to each other (The line would read: 1 2 3 ,, 5), as that will force the mmc binary to exit early ([8] is where said exit takes place). 

The attached patches together should prevent this from being exploited.

Vulnerability #2
In disk_upgrade_devices[7], a bzcat command is run in the event that the ${disk_fw_file} file is missing. 

An attacker can simply replace this file after extraction to get their malicious firmware update installed. I assume there are lower level checks being ran before the firmware is installed, but I couldn't find any when reading through the MMC code. (If there are checks that I missed I would appreciate them being pointed out to me).

While I did provide a patch that mostly removes the use of the FLAGS_tmp_dir variable, this vulnerability would still exist after the attached patches. I'm not sure the best way to approach patching this issue, as extraction is likely always going to be a requirement. While the race is a bit tighter now, it's likely to almost always exist. Checksums could potentially work (likely to be extremely hard to manage due to the sheer number of firmwares needed), but this could fall into the "we should rewrite this as a C++ utility" type of fix that chromium has done in the past. 

[Potential] Vulnerability #3
This vulnerability might not actually exist, but it appears that the mmc-utils is taking the values passed in through this script with little validation[8]. mmc-utils eventually calls MMC_FF_INVOKE_OP[9]. This method grabs the potentially malicious value[10], and then passes it eventually to mmc_prepare_mrq[11]. From here, different implementations do vastly different things. From reading the MMCI implementation[12], my best guess is that this value is being passed as is directly to the underlying firmware to perform the command (in this case, a write). Unfortunately from here I'm not completely sure where to continue looking for how this argument is eventually consumed by the firmware. 


Patches:
chromeos-disk-firmware-update.patch - patch for quoting lots of unquoted variables 
chromeos-disk-firmware-update-remove-tmpdir-usage.patch - patch to limit the use of the FLAGS_tmp_dir (almost complete removal of this variable). This patch is based on the script being patched by chromeos-disk-firmware-update.patch first.

[1] - https://chromium.googlesource.com/chromiumos/platform2/+/master/disk_updater/scripts/chromeos-disk-firmware-update.sh
[2] - https://chromium.googlesource.com/chromiumos/platform2/+/master/disk_updater/scripts/chromeos-disk-firmware-update.conf
[3] - https://chromium.googlesource.com/chromiumos/platform2/+/master/disk_updater/scripts/chromeos-disk-firmware-update.sh#468
[4] - https://chromium.googlesource.com/chromiumos/platform2/+/master/disk_updater/scripts/chromeos-disk-firmware-update.sh#70
[5] - https://chromium.googlesource.com/chromiumos/platform2/+/master/disk_updater/scripts/chromeos-disk-firmware-update.sh#758 
[6] - https://chromium.googlesource.com/chromiumos/platform2/+/master/disk_updater/scripts/chromeos-disk-firmware-update.sh#465
[7] - https://chromium.googlesource.com/chromiumos/platform2/+/master/disk_updater/scripts/chromeos-disk-firmware-update.sh#683
[8] - https://chromium.googlesource.com/chromiumos/third_party/mmc-utils/+/refs/heads/master/mmc_cmds.c#2215
[9] - https://chromium.googlesource.com/chromiumos/third_party/kernel/+/refs/heads/chromeos-4.4/drivers/mmc/core/ffu.c#315
[10] - https://chromium.googlesource.com/chromiumos/third_party/kernel/+/refs/heads/chromeos-4.4/drivers/mmc/core/ffu.c#62
[11] - https://chromium.googlesource.com/chromiumos/third_party/kernel/+/refs/heads/chromeos-4.4/drivers/mmc/core/core.c#2909
[12] - https://chromium.googlesource.com/chromiumos/third_party/kernel/+/refs/heads/chromeos-4.4/drivers/mmc/host/mmci.c#904

## Attachments

- [chromeos-disk-firmware-update.patch](attachments/chromeos-disk-firmware-update.patch) (application/octet-stream, 6.4 KB)
- [chromeos-disk-firmware-update-remove-tmpdir-usage.patch](attachments/chromeos-disk-firmware-update-remove-tmpdir-usage.patch) (application/octet-stream, 3.8 KB)

## Timeline

### wf...@chromium.org (2019-06-10)

[Empty comment from Monorail migration]

### jo...@chromium.org (2019-06-11)

Thanks for the report! Over to Gwendal who wrote the script for the immediate fixes, we'll file a separate bug for possible script improvements (maybe keeping an FD around to avoid TOCTOU problems?).

Severity is at least High (could be persuaded of Critical given that this bypasses verified boot.)

[Monorail components: OS>Systems]

### tm...@gmail.com (2019-06-11)

> Severity is at least High (could be persuaded of Critical given that this bypasses verified boot.)

Not sure if this is intended for me to comment on or not. I would personally keep it as a High unless one of the following occurs:

1) Firmware images don't need to be signed, and therefore #2 works as described above
2) Vulnerability #3 is what I believe it to be, and an attacker can indeed write arbitrary values to the firmware. 

Without the above occurring, I believe a High is the most appropriate choice of Severity, as then this bug more falls in line with other bugs (such as https://bugs.chromium.org/p/chromium/issues/detail?id=955949 which I reported back in April).

### sh...@chromium.org (2019-06-12)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-12)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gw...@chromium.org (2019-06-15)

[Empty comment from Monorail migration]

### gw...@chromium.org (2019-06-15)

Thanks a lot for your analysis and the patches.

-  """An attacker can simply replace this file after extraction to get their malicious firmware update installed. I assume there are lower level checks being ran before the firmware is installed, but I couldn't find any when reading through the MMC code. (If there are checks that I missed I would appreciate them being pointed out to me)."""
disk firmware utilities - mmc, hdparm and nvme for eMMC, SATA and NVMe devices respectively - do not check for firmware image validity and will send it to the block device. The only exception is the "old" mmc method ["old_ffu" at https://chromium.googlesource.com/chromiumos/third_party/mmc-utils/+/refs/heads/master/mmc.c#244,  which ends up calling mmc_ffu_invoke at https://chromium.googlesource.com/chromiumos/third_party/kernel/+/refs/heads/chromeos-4.4/drivers/mmc/core/ffu.c#315]: the kernel code requires the firmware to be in the root image (/lib/firmware) so no malicious firmware can be installed.

The burden to reject malicious firmware is in the device itself: SSD vendors sign their production firmware images and implemented anti-rollback mechanism. A production firmware is not able to install a test firmware image. Furthermore, the SSD is not trusted, we don't rely on any provided security features: we come with our own with verified boot, block and file encryption.

- The intent of FLAGS_tmp_dir is testing: It is not specified when chromeos-disk-firmware-update.sh is invoked on device, just in unit tests:
https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/master/disk_updater/tests/chromeos-disk-firmware-mmc-test.sh#21
I will see how to still test the code without using FLAGS_tmp_dir
Patch chromeos-disk-firmware-update-remove-tmpdir-usage.patch does not completely remove the threat, but limit its scope to function disk_upgrade_devices(), which is where the script spent much of its time. I will remove the use of bzcat for newer firmware packages.

Now if an attacker has intimate knowledge of the SSD, access to the SSD manufacturer signer, she could build a malicious firmware image, and you have found a way to download that image without the attacker having root access to run the normal utilities.

Until the issue is resolved, disk-firmware-update package is removed from images where it was used:
- eve [nvme + emmc]
- falco [sata[
- other board for tests.

*1392478
*1392807
*1392479
*1392357
*1392480
*222325


### tm...@gmail.com (2019-06-15)

Thanks for the pointer to where the firmware verification is. 

> The intent of FLAGS_tmp_dir is testing [...]
This makes a lot of sense. Would it be better for chromium if instead of using the chromeos-disk-firmware-update-remove-tmpdir-usage.patch patch, writing one that checks for testing mode before trying to use tmp_dir? I'll happily give a shot at writing that patch if you think it could be a better solution, as I imagine it would require a lot less rewriting of unit tests, and likely have the same (or better) outcome.

### gw...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### ge...@google.com (2019-06-18)

Approved for ChromeOS M75

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-20)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chromeos/overlays/overlay-eve-private/+/efb39e03ecdd11cf2816f1cd999b2d4d643a9683

commit efb39e03ecdd11cf2816f1cd999b2d4d643a9683
Author: Gwendal Grignou <gwendal@chromium.org>
Date: Thu Jun 20 01:04:37 2019


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-20)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chromeos/overlays/overlay-falco-private/+/618418857223476f964cf80ed8d6e2d57ebb749c

commit 618418857223476f964cf80ed8d6e2d57ebb749c
Author: Gwendal Grignou <gwendal@chromium.org>
Date: Thu Jun 20 01:04:34 2019


### gw...@chromium.org (2019-06-23)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-23)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chromeos/overlays/overlay-falco-private/+/38fa97ad4cad8027c823b4e2cd5b48f5c115caf8

commit 38fa97ad4cad8027c823b4e2cd5b48f5c115caf8
Author: Gwendal Grignou <gwendal@chromium.org>
Date: Sun Jun 23 05:44:42 2019


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-23)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chromeos/overlays/overlay-falco-private/+/12f5c470ae2979fc5bd89e98b009de330e7f6306

commit 12f5c470ae2979fc5bd89e98b009de330e7f6306
Author: Gwendal Grignou <gwendal@chromium.org>
Date: Sun Jun 23 05:45:12 2019


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-23)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chromeos/overlays/overlay-eve-private/+/15d663a4b4f63a419445ec48c17df8ee86de258c

commit 15d663a4b4f63a419445ec48c17df8ee86de258c
Author: Gwendal Grignou <gwendal@chromium.org>
Date: Sun Jun 23 05:47:02 2019


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-06-23)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chromeos/overlays/overlay-eve-private/+/2afa370a16ed7bf1d8c26218294fc09b455cfd54

commit 2afa370a16ed7bf1d8c26218294fc09b455cfd54
Author: Gwendal Grignou <gwendal@chromium.org>
Date: Sun Jun 23 05:47:22 2019


### gw...@chromium.org (2019-06-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-23)

This bug requires manual review: M76 has already been promoted to the beta branch, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), cindyb@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gw...@chromium.org (2019-06-25)

Now we have close the issue the battle plan is:
- apply chromeos-disk-firmware-update.patch  (vulnerability #1)
- store firmware image as-is, not compressed (need to check the impact on rootfs) (vulnerability #2)
- still use temporary directory
- check hdparm/mmc/nvme cli tool they use the last argument for the firmware image, no other image can be inserted in between (vulnerability #1).

In parallel, check if disk_updater still makes sense, given fwudpater project is underway. [https://fwupd.org]

### sh...@chromium.org (2019-06-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dg...@google.com (2019-07-02)

Merge approved for M76

### mn...@chromium.org (2019-07-23)

I believe the CLs that landed per comments 11-17 have closed the vulnerability. Gwendal, can you confirm?

If so, I suggest we close this security bug and file a separate one to track the work to re-enable disk firmware updating.

### jo...@chromium.org (2019-07-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/e82d37f2a7f476a7c2e23d0f1517acaa6a75a6e0

commit e82d37f2a7f476a7c2e23d0f1517acaa6a75a6e0
Author: Gwendal Grignou <gwendal@chromium.org>
Date: Sun Jul 28 07:39:08 2019

disk_updater: Add quotes around variables

Add missing quotes around variables:
2 expections:
- mmc options call, where several quirks can be defined
- disk selection, in case more than one disk is present.

BUG=chromium:972463
TEST=Unit test.

Change-Id: I99af7c61c41bbdc6cb75d0596615cfd8dd8a6363
Reviewed-on: https://chromium-review.googlesource.com/1697046
Tested-by: Gwendal Grignou <gwendal@chromium.org>
Commit-Ready: Gwendal Grignou <gwendal@chromium.org>
Legacy-Commit-Queue: Commit Bot <commit-bot@chromium.org>
Reviewed-by: Mike Frysinger <vapier@chromium.org>

[modify] https://crrev.com/e82d37f2a7f476a7c2e23d0f1517acaa6a75a6e0/disk_updater/scripts/chromeos-disk-firmware-update.sh


### jo...@chromium.org (2019-07-29)

Time to mark this fixed?

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-09)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tm...@gmail.com (2019-08-15)

Any updates or something I can help with?

### gw...@chromium.org (2019-08-28)

I did not commit the other changes, at tmpdir can be guess even if not formally specified and attacker that can inject file can update the firmware directly.
(see 
https://chromium-review.googlesource.com/c/chromiumos/platform2/+/1708004
https://chromium-review.googlesource.com/c/chromiumos/platform2/+/1697047)
We assume the SSD will reject incorrect firmware.

### sh...@chromium.org (2019-08-29)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-03)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-10-16)

Hi - do any of those overlays CLs need to be reverted now this issue is fixed?

### mn...@chromium.org (2019-10-17)

This came bug in a recent discussion and we did take a closer look at exploitability.

We realized that the input data for vuln #1 sits on the rootfs, which isn't writeable. So the hurdle is really high to place something malicous at the correct path. The only plausible way would seem to mount something over the file. An attacker with an arbitrary mount primitive has many ways to gain full control over the system already, so the quoting bug in the script is of little value.

For vuln #2, the attacker would require an arbitrary file write primitive to the tmpdir. That directory is only accessible to root, so there the attacker would first have to gain privileges.

Given these additional mitgating circumstances, I'll downgrade severity to Low.

### sh...@chromium.org (2019-10-18)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2019-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-18)

Congrats! The Panel decided to reward $1,000 for this report

### na...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### tm...@gmail.com (2019-10-18)

Awesome thanks a lot!

### tm...@gmail.com (2019-10-19)

Per #36, I have a few questions on exploitability. Pretty sure these would be considered out of scope, but: Wouldn't an attacker be able to abuse vulnerability #2 to install a known vulnerable firmware version to then exploit as a boot persistence mechanism? Or they could have also exploited #1 to prevent the update then persist via vulnerable firmware. While root is definitely required, if we're talking about attacking persistence at boot time root is likely a requirement already. 

### sh...@chromium.org (2019-12-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-17)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/972463?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/464496]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095348)*
