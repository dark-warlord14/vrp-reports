# Security: Chrome OS: bluez missed patch can cause remotely information leak in function cli_feat_read_cb

| Field | Value |
|-------|-------|
| **Issue ID** | [40067324](https://issues.chromium.org/issues/40067324) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | pi...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-13 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**

According to bluez security advisory <https://github.com/bluez/bluez/security/advisories/GHSA-479m-xcq5-9g2q> , this bug can remotely oob read and return the oob read content to bluetooth endpoint, can bypass ASLR or leak sensitive content:  

It is the out-of-bounds reading problem in cli\_feat\_read\_cb

```
len = sizeof(state->cli_feat)-offset;  
value = len? &state->cli_feat[offset]: NULL;  

Unverified offset can cause the leakage of any address on the heap  

```

And according to above link, the bug in cli\_feat\_read\_cb is fixed siliently, no CVE assigned, so cause chromeos miss the patch to bluez/current branch.  

<https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/bluez/current/src/gatt-database.c;drc=4977dc04f9159c19478c0cc442017cbf7e03920b;l=1086>

I found two patches relates to this bug, I personally think the first patch is suitable to chromeos bluez/current:  

<https://github.com/bluez/bluez/commit/3a40bef49305f8327635b81ac8be52a3ca063d5a>  

<https://github.com/bluez/bluez/commit/6a50b6aeda78a88eafb177718109c256eec077a6>

**VERSION**  

ChromeOS bluez/current

## Timeline

### [Deleted User] (2023-07-13)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-07-13)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-14)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/291158682). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/291158682]

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-01)

Project: chromiumos/third_party/bluez
Branch: release-R115-15474.B-chromeos-5.54

commit 15e3a1bb8d64916c739a932b9f83db4905947d2d
Author: Luiz Augusto von Dentz <luiz.von.dentz@intel.com>
Date:   Tue Jan 05 16:38:03 2021

    UPSTREAM: shared/gatt-db: Introduce gatt_db_attribute_set_fixed_length
   
    This enables user to inform if an attribute has a fixed length so it can
    automatically perform bounds checking.
    (cherry picked from commit 87184a20cfcfe1523926a2e4a724c1a01c7ae0fb)
   
    BUG=b:291158682
    TEST=emerge- bluez and autotest
   
    Change-Id: I2239bb8e119c0586307acb02a2da6fbe73bca243
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/bluez/+/4697602
    Reviewed-by: Archie Pusaka <apusaka@chromium.org>
    Reviewed-by: Sean Paul <sean@poorly.run>
    Commit-Queue: Abhishek Pandit-Subedi <abhishekpandit@google.com>
    Tested-by: Abhishek Pandit-Subedi <abhishekpandit@google.com>
    Reviewed-on: https://chromium-review.googlesource.com/c/chromiumos/third_party/bluez/+/4724091
    Reviewed-by: Zhengping Jiang <jiangzp@google.com>

M       src/shared/gatt-db.c
M       src/shared/gatt-db.h

https://chromium-review.googlesource.com/4724091
20:07
20:07
CLs: Merged:​crrev/c/4697602, crrev/c/4697603, crrev/c/4697604, crrev/c/4697605, crrev/c/4718886, crrev/c/4718887, crrev/c/4718888, crrev/c/4718889      crrev/c/4697602, crrev/c/4697603, crrev/c/4697604, crrev/c/4697605, crrev/c/4718886, crrev/c/4718887, crrev/c/4718888, crrev/c/4718889, crrev/c/4724091, crrev/c/4724092, crrev/c/4724093, crrev/c/4724094
CLs: Pending:​crrev/c/4724091, crrev/c/4724092, crrev/c/4724093, crrev/c/4724094      <none>

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-01)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-10)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### st...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-18)

Exploitability -  From upstream reporter notes, must have direct access to device to oob read, and has tests showing exploitability
Privileges and Capabilities - In the third_party package bluez, this is an oob read which can leak heap addresses and bypass ASLR, and cause remote code execution
Origin of fix - The issue is already known and fixed upstream in 2021, no CVE was created, the bug was silently fixed causing chromeos to miss the patch.
Mitigations - The issue is mitigated by checking if the offset is valid within the bounds of state->cli_feat array.
Severity assessment - Its an out of bounds read on a third party upstream package, which is a medium severity bug. It is not high severity because the reporter required chaining two gatt vulnerabilities and a memory leak vuln on sdp side to experiment with this. It is not a low severity because there is a potential for leaking Bluetooth information if this is part of a larger exploit.

Explicitly setting severity to medium based on above justification


### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-18)

[Comment Deleted]

### ch...@google.com (2023-10-18)

Congratulations lovepink! 
The VRP Panel has decided to award you $500 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-07)

This issue was migrated from crbug.com/chromium/1464445?no_tracker_redirect=1

[Monorail blocking: b/291158682]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067324)*
