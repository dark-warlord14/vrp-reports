# cros-machine-id-regen should quote file path when computing timestamp path

| Field | Value |
|-------|-------|
| **Issue ID** | [40094787](https://issues.chromium.org/issues/40094787) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | OS>Systems |
| **Platforms** | ChromeOS |
| **Reporter** | tm...@acu.edu |
| **Assignee** | mn...@chromium.org |
| **Created** | 2019-04-30 |
| **Bounty** | $1,000.00 |

## Description

This is similar to another issue I reported in crosh (issue tracker here: https://bugs.chromium.org/p/chromium/issues/detail?id=957896). 

Much like the two bugs in the above issue, an unquoted variable is passed to an echo statement in ~/chromeos/src/third_party/chromiumos-overlay/chromeos-base/chromeos-machine-id-regen/files/cros-machine-id-regen (line 67). I do not think this is exploitable, however it is possible to pass in flags to echo (-e seems the most dangerous one), which could potentially cause issues. 

mnissler@chromium.org goes into the details on why it's not likely exploitable here (https://bugs.chromium.org/p/chromium/issues/detail?id=957705#c2).

## Timeline

### ad...@chromium.org (2019-04-30)

mnissler@, PTAL at this one too.

### ad...@google.com (2019-04-30)

Taking a stab at the right component...

[Monorail components: OS>Systems]

### mn...@chromium.org (2019-05-02)

In addition to my already quoted analysis, I don't think we have any non-test code path that passes in a custom machine id file, so I don't think this is accessible. Still makes sense to fix the quoting.

### mn...@chromium.org (2019-05-02)

[Empty comment from Monorail migration]

### mn...@chromium.org (2019-05-02)

Further note that POSIX specifies echo to not take any options, so -e won't take effect.

### mn...@chromium.org (2019-05-02)

CL with quoting fixes is here: https://chromium-review.googlesource.com/c/chromiumos/overlays/chromiumos-overlay/+/1593297

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/overlays/chromiumos-overlay/+/e1920e64ef07b6960632404596a95cabe8b0d909

commit e1920e64ef07b6960632404596a95cabe8b0d909
Author: Mattias Nissler <mnissler@chromium.org>
Date: Sat May 04 10:18:05 2019

chromeos-base/chromeos-machine-id-regen: Consistify quoting

Some cosmetic updates to quoting for consistency and style guide
compliance.

BUG=chromium:958002
TEST=platform_DBusMachineIdRotation

Change-Id: I07fcec23377d036160c245654c7f9cf703fc9618
Reviewed-on: https://chromium-review.googlesource.com/1593297
Commit-Ready: Mattias Nissler <mnissler@chromium.org>
Tested-by: Mattias Nissler <mnissler@chromium.org>
Reviewed-by: Jorge Lucangeli Obes <jorgelo@chromium.org>

[modify] https://crrev.com/e1920e64ef07b6960632404596a95cabe8b0d909/chromeos-base/chromeos-machine-id-regen/files/cros-machine-id-regen
[rename] https://crrev.com/e1920e64ef07b6960632404596a95cabe8b0d909/chromeos-base/chromeos-machine-id-regen/chromeos-machine-id-regen-0.0.1-r5.ebuild


### va...@chromium.org (2019-05-29)

there is no way that i know of for arbitrary arguments to `echo` to trigger any command execution.

further, the argument to echo is a constant filename and there's no way for users to control this.  so there is no security concern.

i would turn this into a normal Bug rather than Bug-Security with Pri-3.

### mn...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-06-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-08-14)

Congrats! The Panel decided to reward $1,000 for this report!

### na...@google.com (2019-08-14)

[Empty comment from Monorail migration]

### tm...@acu.edu (2019-08-15)

Awesome, thanks a lot :)!

### sh...@chromium.org (2019-09-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-09-24)

This issue was migrated from crbug.com/chromium/958002?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/967926, crbug.com/chromium/967933, crbug.com/chromium/967938, crbug.com/chromium/967943]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094787)*
