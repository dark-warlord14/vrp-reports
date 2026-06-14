# Security: image_burner arbitrary root file-write

| Field | Value |
|-------|-------|
| **Issue ID** | [40089011](https://issues.chromium.org/issues/40089011) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | vi...@microsoft.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2017-09-14 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS

There’s a bug in BurnerImpl::ValidateTargetPath(...).

Target path is validated against the following regex, it must match at least one of them:

const char* kFilePathPatterns[] =
    { "/dev/sd[a-z]+$", "/dev/mmcblk[0-9]+$" };
const int kFilePathPatternCount = 2;

However there is a missing "^" at the start of each regex.
Thus we can supply /<anything>/dev/sda and it will be accepted as a valid path by image_burner.

Using symlinks, one can abuse this to write to various files as root.

In ValidateTargetPath(...) there is also a check to prevent the root partition from being used as a target file.
This check can be bypassed by using "/./dev/sda" instead of "/dev/sda".



VERSION
ChromeOS 9515.0.0_x86_64

REPRODUCTION CASE

Run attached script as chronos user, it will write to the specified file as root.

## Attachments

- [image_burner_repro.sh](attachments/image_burner_repro.sh) (text/plain, 700 B)

## Timeline

### me...@chromium.org (2017-09-14)

Thank you for the report.

tbarzic: This looks like https://crbug.com/chromium/340512. Can you please confirm if they are same issues?

### me...@chromium.org (2017-09-14)

[Empty comment from Monorail migration]

### tb...@chromium.org (2017-09-14)

it's not the same

### wf...@chromium.org (2017-09-14)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-15)

tbarzic: Are you the right person to own this bug? Can you please evaluate the severity based on https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md ?


### tb...@chromium.org (2017-09-15)

Yes, I'm the right person to own this

I'd say this is a medium severity (given that an attacker would have to be able to run an arbitrary script on the device), but security team might disagree with me.

### mn...@chromium.org (2017-09-18)

Regarding exploitability: This is exposed via DBus to Chrome. On the Chrome side, this is accessible via the image burner private API, which isn't accessible to web content. So another bug would be required to gain code execution in the Chrome browser process.

However, ImageBurner runs as root, so this is a potential vector to escalate a Chrome exploit to root privilege level. We should mitigate this by running image burner only with the privileges it needs, not full root. Filed https://crbug.com/chromium/766130 to track that.

Overall, agreed to Severity-Medium given that this is not exploitable on its own. This is pretty valuable in an exploit chain though, so we should fix this quickly.

[Monorail components: OS>Systems]

### sh...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### tb...@chromium.org (2017-09-18)

Merge request for
https://chromium-review.googlesource.com/c/chromiumos/platform2/+/669957

(I the cl was linked to  https://crbug.com/chromium/340512 by mistake; it's a fix for this issue)

### sh...@chromium.org (2017-09-18)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bh...@google.com (2017-09-20)

Approved for 62. 

### sh...@chromium.org (2017-09-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/53f70c86481e98903c34baa31f97c5cb7d2cb4f9

commit 53f70c86481e98903c34baa31f97c5cb7d2cb4f9
Author: Toni Barzic <tbarzic@google.com>
Date: Mon Sep 25 16:52:52 2017

image-burner: Fix allowed target path regex

The regular expression for allowed image burning targets was missing
a "^".

BUG=chromium:765450
TEST=chromeos-imageburner unittests

Change-Id: I388d0cf9a6fc4c9a72db01369564f3e288e54465
Reviewed-on: https://chromium-review.googlesource.com/669957
Commit-Ready: Toni Barzic <tbarzic@chromium.org>
Tested-by: Toni Barzic <tbarzic@chromium.org>
Reviewed-by: Ben Chan <benchan@chromium.org>
Reviewed-by: Mike Frysinger <vapier@chromium.org>
(cherry picked from commit cedaf66cba5d32c4ca43fe7874ad5479ab1090e0)
Reviewed-on: https://chromium-review.googlesource.com/678595
Reviewed-by: Toni Barzic <tbarzic@chromium.org>
Commit-Queue: Toni Barzic <tbarzic@chromium.org>

[modify] https://crrev.com/53f70c86481e98903c34baa31f97c5cb7d2cb4f9/image-burner/image_burner_impl.cc
[modify] https://crrev.com/53f70c86481e98903c34baa31f97c5cb7d2cb4f9/image-burner/image_burner_impl_unittest.cc


### tb...@chromium.org (2017-09-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-29)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2017-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-14)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-07-20)

This issue was migrated from crbug.com/chromium/765450?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089011)*
