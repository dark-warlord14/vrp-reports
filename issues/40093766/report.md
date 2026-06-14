# crash_sender: invalid crash report names can trigger arbitrary file deletion as root

| Field | Value |
|-------|-------|
| **Issue ID** | [40093766](https://issues.chromium.org/issues/40093766) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | se...@ncsc.gov.uk |
| **Assignee** | va...@chromium.org |
| **Created** | 2019-01-16 |
| **Bounty** | $500.00 |

## Description

Summary:

A Mitigation Bypass has been discovered in Chrome OS which affects the latest version. This vulnerability allows an attacker to bypass a security mitigation. This vulnerability has a Severity Score of 2.1 and a Low  Severity Rating (based on the Common Vulnerability Scoring System v2).  The Severity Score and Severity Rating are calculated from the Exploitability and Impact Metrics in Table 1. Table 2 presents a summary of these vulnerability metrics.


Details:

/sbin/crash_sender on Chrome OS is a shell script responsible for collating and uploading various different kinds of crash reports that can be generated if the user is opted into this. 
These are read from the following locations:
/home/chronos/crash (Writable by chronos user) /home/chronos/u-*/crash (Writable by chronos user) /var/spool/crash (Writable by root only)
Since these directories are widely writable and the script runs as root, bugs in it are potentially exploitable. For example as elevation of privilege, or for persistence if a reboot occurs between writing and the next execution. 
In this instance untrusted user controlled filenames are incorrectly escaped in a shell for loop.

Please see the attached report.

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### se...@ncsc.gov.uk (2019-01-16)

Proof Of Concept

483      # Consider any old files which still have no corresponding meta file 
484      # as orphaned ,and remove them.
485      for old_file in $(${FIND} "${dir}" -mindepth 1 \ 
486                        -mmin +$((24 * 60)) -type f); do 
487        if [ ! -e "$(get_base "${old_file}").meta" ]; then 
488          lecho "Removing old orphaned file: ${old_file}." 
489          rm -f -- "${old_file}" 
490        fi 
491      done

Any file (even in sub directories) in the possible locations with a space in it will be treated as two separate items. This check happens before the check for opting into crash stats is performed. Therefore it an always be used to delete any file the script is able to, either as an absolute path or a relative one, with up to one .. included in the path.
An absolute path can be specified as:
    mkdir -p '/home/chronos/crash/absolute /directory/to/delete/from/'    touch -m -t 197001010000 '/home/chronos/crash/absolute /directory/to/delete/from/ filename'
 
Or a relative path: 
    mkdir -p '/home/chronos/crash/missing relative/ ../directory/to/delete/from/'    touch -m -t 197001010000 '/home/chronos/crash/missing relative/ ../directory/to/ delete/from/filename'
 
In the relative path instance, the extra space in 'missing relative' is needed because of the set -e in the script which would otherwise cause rm to fail with "rm: cannot remove '/home/chronos/ crash/relative/': Is a directory" and stop execution of the whole script. 

The whole process is performed within minijail0.

However, this jail is relatively weak. The main practical limitation this imposes for file writing is that /proc is now read only.


Mitigation

Correctly escape filenames in /sbin/crash_sender. Additionally, enhancing the isolation of the crash reporting code and/or avoiding the need to do it in a privileged context would help to mitigate this issue.



Bug Bounty Payment
------------------
If this vulnerability is eligible for a Bug Bounty payment, we ask that the money be donated directly to NSPCC, (Registered Charity Number: 216401), https://www.nspcc.org.uk.

Please contact the NCSC mailbox to inform us of the donation amount and the donation date.


NCSC Contact Information
------------------------
The vulnerability disclosure mailbox is security@ncsc.gov.uk.  Please contact us for our PGP key. 


Crediting NCSC
------------------------
NCSC would appreciate appropriate credit as The UK's National Cyber Security Centre (NCSC) in any advisories which you may publish about this issue.
Verification, Resolution and Release
Please inform NCSC via the security@ncsc.gov.uk mailbox, quoting the NCSC Reference above, should you:
confirm that this is a security issue
allocate the issue a CVE identifier
determine a date to release a patch
determine a date to publish advisories


NCSC Disclosure Policy
------------------------
NCSC has adopted the ISO 29147 approach to vulnerability disclosure and, as such, follows a coordinated disclosure approach with affected parties. We have never publicly disclosed a vulnerability prior to a fix being made available.

NCSC recognises that vendors need a reasonable amount of time to mitigate a vulnerability, for example, to understand the impact to customers, to triage against other vulnerabilities, to implement a fix in coordination with others, and to make that fix available to its customers. As this will vary based on the exact situation NCSC does not define a set time frame in which a fix must be made available, and we are happy to discuss the circumstances of any particular disclosure.

If NCSC believes a vendor is not making appropriate progress with vulnerability resolution, we may, after discussion with the vendor, choose to share the details appropriately (for example, with service providers and our customers) to ensure that we provide appropriate mitigation of the threat to the UK and to UK interests.

Disclaimer
------------------------
Any NCSC findings and recommendations made have not been provided with the intention of avoiding all risks, and following the recommendations will not remove all such risk. Ownership of information risks remains with the relevant system owner at all times.


### jd...@chromium.org (2019-01-16)

Routing to Chrome OS Security for further triage.

### ke...@chromium.org (2019-01-16)

vapier@, what do you think, is this low?

### va...@chromium.org (2019-01-16)

the primitive is uncontrolled file deletion.  so by itself, it's not great, but can't be directly used for further escalation.  but primitives are just waiting to be chained ;).  pending that, "low" sounds about right to me.

the bug is def already fixed in M73 after having moved all find/rm logic to C++.  we don't do any whitespace splitting or nonsense there so it'd be immune to this kind of attack.

the bug is def there in M71 and older.

the specific code cited is deleted in M72 (having moved it to C++), but there is a for+find+rm loop left that exhibits the undesirable properties described here.  it's a bit harder to get to as the C++ side has some clean up logic in it that runs before the shell code.  but i think given more effort, you could still execute the primitive.

an easy fix mitigation for the branches would be to blindly delete files with whitespace/path expansions in them.  maybe something like:
  find ... -name '*[^a-zA-Z0-9_.+=%-]*' -delete

[Monorail components: OS>Systems>CrashReporting]

### va...@chromium.org (2019-01-17)

posted this fix for R72:
  https://chromium-review.googlesource.com/1417056

it's not a backport because the changes in R73 are way too invasive for R72, and the code that it's changing doesn't exist in R73.

### sh...@chromium.org (2019-01-17)

This bug requires manual review: We are only 11 days from stable.
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), djmm@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-01-17)

[Empty comment from Monorail migration]

### dj...@google.com (2019-01-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2019-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromiumos/platform2/+/30d25e4354ed7f991d515ac8b17cbba34c081931

commit 30d25e4354ed7f991d515ac8b17cbba34c081931
Author: Mike Frysinger <vapier@chromium.org>
Date: Thu Jan 17 22:46:07 2019

crash-reporter: crash_sender: pre-clean the spool dir

Make sure the find command we run later doesn't improperly split words
if there are corrupt reports in the spool dir.

This isn't a problem in R73+ because the code has already been changed
over to C++.

BUG=chromium:922446
TEST=ran find command by hand on device w/crashes and it only deleted invalid files

Change-Id: Ie205ef0cea58bc00d297d7884439f0028f68437c
Reviewed-on: https://chromium-review.googlesource.com/c/1417056
Reviewed-by: Greg Kerr <kerrnel@chromium.org>
Commit-Queue: Mike Frysinger <vapier@chromium.org>
Tested-by: Mike Frysinger <vapier@chromium.org>

[modify] https://crrev.com/30d25e4354ed7f991d515ac8b17cbba34c081931/crash-reporter/crash_sender.sh


### sh...@chromium.org (2019-01-21)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2019-01-23)

M72 has been merged, but still waiting on M71 ...

### mn...@chromium.org (2019-01-29)

+kbleicher (M71 release owner). Will we do a stable M71 respin this can be considered for?

### sh...@chromium.org (2019-01-29)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### va...@chromium.org (2019-02-07)

afaik, R72 is stable now, so i guess there's no interest in applying the fix to R71

### sh...@chromium.org (2019-02-08)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-11)

[Empty comment from Monorail migration]

### na...@google.com (2019-02-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-02-13)

Congrats! The Panel decided to reward $500 for this report :)

### aw...@google.com (2019-02-20)

Reward will be donated.

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-06-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-13)

[Empty comment from Monorail migration]

### se...@chromeos-software-sheriffbot.google.com.iam.gserviceaccount.com (2021-11-15)

[Empty comment from Monorail migration]

### se...@chromeos-software-sheriffbot.google.com.iam.gserviceaccount.com (2021-11-16)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/922446?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093766)*
