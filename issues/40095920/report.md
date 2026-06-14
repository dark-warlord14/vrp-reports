# Security: Privilege Elevation via Google Chrome Elevation Service

| Field | Value |
|-------|-------|
| **Issue ID** | [40095920](https://issues.chromium.org/issues/40095920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Installer>Components |
| **Platforms** | Windows |
| **Reporter** | ph...@nccgroup.trust |
| **Assignee** | ga...@chromium.org |
| **Created** | 2019-08-06 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

The Chrome Elevation Service exposes the RunRecoveryCRXElevated method that can be abused by low privileged users to obtain a copy of any file on a host.

Full details included in attached PDF.

**VERSION**

Chrome Version: 75.0.3770.142 (stable)  

Operating System: Windows 10 version 1809 (will probably affect any Windows OS)

**REPRODUCTION CASE**

See attached Visual Studio solution in ChromeRecoveryLPE.zip for functioning PoC (apologies that this is an archive file, but this seemed to be the only practical way to submit a VS solution!).

**CREDIT INFORMATION**

Reporter credit: Phillip Langlois ([phillip.langlois@nccgroup.com](mailto:phillip.langlois@nccgroup.com)) and Edward Torkington ([edward.torkington@nccgroup.com](mailto:edward.torkington@nccgroup.com)), NCC Group

## Attachments

- [ChromeElevationServiceLPE.pdf](attachments/ChromeElevationServiceLPE.pdf) (application/pdf, 486.5 KB)
- [ChromeRecoveryLPE.zip](attachments/ChromeRecoveryLPE.zip) (application/octet-stream, 15.2 KB)

## Timeline

### ke...@chromium.org (2019-08-07)

Thanks for the report. I am not particularly familiar with this component, but to summarize, it is not a vulnerability in Chrome itself, but rather this service becomes a vector for a priv esc on Windows allowing reading of files that the user should not be able to read.

ganesh@: Can you PTAL? There are some suggested mitigations in the report.

wfh@: Do you have any thoughts here? I'm not entirely sure how to flag this since it falls outside of our severity guidelines.

[Monorail components: Internals>Installer]

### ga...@chromium.org (2019-08-07)

Discussing with Sorin, there is one immediate mitigation that we could start with:
* Check the file for CRX and signature validity before copying to the secure location, and then check it again after the copy to the secure location before unpacking.

Other steps that we could take in addition to above:
* Impersonate the caller while reading the file.
* Restrict the paths that we accept as input.


### so...@chromium.org (2019-08-07)

[Empty comment from Monorail migration]

[Monorail components: -Internals>Installer Internals>Installer>Components Security]

### wf...@chromium.org (2019-08-07)

we certainly do consider these within our vulnerability reward program because it's fully within chrome's components. This does look like a medium though, because you can't access this COM endpoint from a renderer, but needs to already be running at medium.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c4982d88cea806589aad7bceabb9dd75aeeb894b

commit c4982d88cea806589aad7bceabb9dd75aeeb894b
Author: S. Ganesh <ganesh@chromium.org>
Date: Thu Aug 08 01:16:57 2019

Add extra check for CRX validity.

We now check the input file for CRX and signature validity before copying to the secure location. This is to prevent us from copying unintended files, including files that may be private to a particular user or group.

Bug: 991125
Change-Id: I9f3092c9fa32b822c4d7249598b0753b4c4a1fd0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1742302
Commit-Queue: S. Ganesh <ganesh@chromium.org>
Reviewed-by: Sorin Jianu <sorin@chromium.org>
Reviewed-by: Will Harris <wfh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#685051}

[modify] https://crrev.com/c4982d88cea806589aad7bceabb9dd75aeeb894b/chrome/elevation_service/elevated_recovery_impl.cc
[modify] https://crrev.com/c4982d88cea806589aad7bceabb9dd75aeeb894b/chrome/elevation_service/elevated_recovery_unittest.cc


### ph...@nccgroup.trust (2019-08-08)

Thanks for the quick response and obviously we're pleased this falls within the reward program!

I have some concerns regarding the patch though - I think the new code is still vulnerable although the attack is slightly more complicated. If I pass a symlink to a valid CRX file, then switch the symlink to point to my real target after the initial validity check, the previous attack should still work. 

James Forshaw has a bunch of tools to make this easy at https://github.com/googleprojectzero/symboliclink-testing-tools. Under some conditions, these tools will fail, but on the face of it the new code seems likely to be exploitable using the BaitAndSwitch code. I will not have time to test this in the next few days, however.

We have found a number of bugs like this in the past couple of weeks and have had some discussions on how to fix them. Our current thinking is that impersonation of the caller is the best approach - in this case, though, I think this might be slightly complicated since you won't be able to copy to the recovery folder whilst impersonating. Perhaps you could read the file into memory whilst impersonating and then write to the recovery folder after reverting?

### so...@chromium.org (2019-08-12)

Thank you. We continue working on this bug (hence it is still "work in progress"). The patch was simple enough to land quickly while we are looking at how to do impersonation.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4f1bca34a5cf12248b47e5c55f06d2a56e4e2f70

commit 4f1bca34a5cf12248b47e5c55f06d2a56e4e2f70
Author: S. Ganesh <ganesh@chromium.org>
Date: Fri Aug 16 01:30:33 2019

Open CRX file with impersonation.

Bug: 991125
Change-Id: I6e389cd7f6af1d2bbba02e7449a41ab7c526236a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1752109
Commit-Queue: S. Ganesh <ganesh@chromium.org>
Reviewed-by: Sorin Jianu <sorin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#687527}

[modify] https://crrev.com/4f1bca34a5cf12248b47e5c55f06d2a56e4e2f70/chrome/elevation_service/elevated_recovery_impl.cc
[modify] https://crrev.com/4f1bca34a5cf12248b47e5c55f06d2a56e4e2f70/chrome/elevation_service/elevated_recovery_unittest.cc
[modify] https://crrev.com/4f1bca34a5cf12248b47e5c55f06d2a56e4e2f70/chrome/elevation_service/run_all_unittests.cc
[modify] https://crrev.com/4f1bca34a5cf12248b47e5c55f06d2a56e4e2f70/chrome/elevation_service/service_main.cc
[modify] https://crrev.com/4f1bca34a5cf12248b47e5c55f06d2a56e4e2f70/chrome/elevation_service/service_main.h
[modify] https://crrev.com/4f1bca34a5cf12248b47e5c55f06d2a56e4e2f70/chrome/elevation_service/service_main_unittest.cc


### ga...@chromium.org (2019-08-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-17)

[Empty comment from Monorail migration]

### na...@google.com (2019-08-19)

[Empty comment from Monorail migration]

### ph...@nccgroup.trust (2019-08-28)

Apologies for the delay in replying, I have been on leave and am not due back until next week. We will take a look at the fix at some point shortly after then. 

In the meantime, could you tell me how the vulnerability reward program works going forward? We've not been through the process with Google before. Also, am I correct in assuming that you will get a CVE id assigned to this bug?

### wf...@chromium.org (2019-09-04)

hello from the VRP panel. In future, please do not attach PDF files but paste the report as plain text into the report.

### na...@google.com (2019-09-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-09-05)

Congrats! The Panel decided to reward $5,000 for this report

### na...@google.com (2019-09-05)

[Empty comment from Monorail migration]

### wf...@chromium.org (2019-09-05)

re: #12, yes a CVE will be assigned closer to the release of the stable milestone that this bug was fixed in - this case it's M78 so you should see some activity next month.

### sh...@chromium.org (2019-09-20)

Not requesting merge to beta (M78) because latest trunk commit (687527) appears to be prior to beta branch point (693954). If this is incorrect, please replace the Merge-na label with Merge-Request-78. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/991125?no_tracker_redirect=1

[Multiple monorail components: Internals>Installer>Components, Security]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095920)*
