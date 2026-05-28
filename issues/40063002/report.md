# Security: ChromeOS root privilege escalation (mount-passthrough-jailed)

| Field | Value |
|-------|-------|
| **Issue ID** | [40063002](https://issues.chromium.org/issues/40063002) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ro...@rorym.cnamara.com |
| **Assignee** | mo...@google.com |
| **Created** | 2023-02-09 |
| **Bounty** | $31,000.00 |

## Description

**VULNERABILITY DETAILS**  

Mount-passthrough-jailed uses shflags and therefore will use eval over the passed arguments. These arguments can be controlled via chronos. This results in arbitrary command execution as root.

**VERSION**  

Google Chrome 111.0.5544.0 (Official Build) dev (64-bit)  

Revision 14a1ac2acbb26d770b097909126a2dd2cf9dfa71-refs/branch-heads/5544@{#1}  

Platform 15320.0.0 (Official Build) dev-channel eve  

Firmware Version Google\_Eve.9584.230.0

(I hope you like dev channel privescs as much as stable channel)

**REPRODUCTION CASE**  

Execute privesc.sh attached as follows:

sh <(cat privesc.sh)

The script should immediately return with a root shell.

DETAILS  

Mount-passthrough-jailed uses eval during argument parsing [1]. The arcvm-mount-removable-media.conf upstart script passes fuse\_uid [2] imported [3] from arcvm-media-sharing-services.conf [4] which is startable by chronos [5].

An appropriate payload (e.g ';$(id>/tmp/pwned);') in the MEDIA\_PROVIDER\_UID argument to the arcvm-media-sharing-services upstart job will break out of the quoting and execute an arbitrary command. The attached script runs sshd.

[1] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/main/arc/mount-passthrough/mount-passthrough-jailed#33>  

[2] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/main/arc/vm/scripts/init/mount-media-dirs/arcvm-mount-removable-media.conf#40>  

[3] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/main/arc/vm/scripts/init/mount-media-dirs/arcvm-mount-removable-media.conf#18>  

[4] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/main/arc/vm/scripts/init/arcvm-media-sharing-services.conf#20>  

[5] <https://chromium.googlesource.com/chromiumos/platform2/+/refs/heads/main/arc/vm/scripts/init/dbus-1/ArcVmScripts.conf#17>

## Attachments

- [privesc.sh](attachments/privesc.sh) (text/plain, 672 B)

## Timeline

### [Deleted User] (2023-02-09)

[Empty comment from Monorail migration]

### ma...@google.com (2023-02-09)

Over to CrOS security bug triage

### ro...@rorym.cnamara.com (2023-02-09)

Quick addition: This was added in https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4113640

### lz...@google.com (2023-02-09)

Let me rope in Momoko to see if we can stop command injection via `eval`.

### lz...@google.com (2023-02-09)

[Empty comment from Monorail migration]

### mo...@chromium.org (2023-02-10)

[Empty comment from Monorail migration]

### yo...@chromium.org (2023-02-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/92d04ce33f087bf49002088105c02441751fb77a

commit 92d04ce33f087bf49002088105c02441751fb77a
Author: Momoko Hattori <momohatt@google.com>
Date: Fri Feb 10 04:26:00 2023

arc: Verify input string from chronos to arcvm-media-sharing-services

BUG=chromium:1414511, b:268542674
TEST=Check that chromium:1414511 is fixed
TEST=(arcvm-media-sharing-services fails to start).
TEST=tast run <DUT> arc.MyFiles.vm arc.RemovableMedia.vm

Change-Id: Id8557b23b4b92e61f52588ff6bcbe6c0c4195ea3
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4235401
Reviewed-by: Ryo Hashimoto <hashimoto@chromium.org>
Reviewed-by: Youkichi Hosoi <youkichihosoi@chromium.org>
Reviewed-by: Hidehiko Abe <hidehiko@chromium.org>
Tested-by: Momoko Hattori <momohatt@chromium.org>
Commit-Queue: Momoko Hattori <momohatt@chromium.org>

[modify] https://crrev.com/92d04ce33f087bf49002088105c02441751fb77a/arc/vm/scripts/init/arcvm-media-sharing-services.conf


### lz...@google.com (2023-02-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-02-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/3bf0979709a854c1061bb4639b37e25bffdbebd6

commit 3bf0979709a854c1061bb4639b37e25bffdbebd6
Author: Momoko Hattori <momohatt@google.com>
Date: Fri Feb 10 04:26:00 2023

arc: Verify input string from chronos to arcvm-media-sharing-services

BUG=chromium:1414511, b:268542674
TEST=Check that chromium:1414511 is fixed
TEST=(arcvm-media-sharing-services fails to start).
TEST=tast run <DUT> arc.MyFiles.vm arc.RemovableMedia.vm

Change-Id: Id8557b23b4b92e61f52588ff6bcbe6c0c4195ea3
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4235401
Reviewed-by: Ryo Hashimoto <hashimoto@chromium.org>
Reviewed-by: Youkichi Hosoi <youkichihosoi@chromium.org>
Reviewed-by: Hidehiko Abe <hidehiko@chromium.org>
Tested-by: Momoko Hattori <momohatt@chromium.org>
Commit-Queue: Momoko Hattori <momohatt@chromium.org>
(cherry picked from commit 92d04ce33f087bf49002088105c02441751fb77a)
Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/platform2/+/4248158

[modify] https://crrev.com/3bf0979709a854c1061bb4639b37e25bffdbebd6/arc/vm/scripts/init/arcvm-media-sharing-services.conf


### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations, Rory! The VRP Panel has decided to award you $30,000 for this report + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### ro...@rorym.cnamara.com (2023-02-17)

Thank you!

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1414511?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063002)*
