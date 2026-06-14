# Insufficient policy enforcement in Safe Browsing

| Field | Value |
|-------|-------|
| **Issue ID** | [40060235](https://issues.chromium.org/issues/40060235) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | Mac |
| **CVE IDs** | CVE-2020-6402, CVE-2022-1874 |
| **Reporter** | no...@ssd-disclosure.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2022-07-11 |
| **Bounty** | $500.00 |

## Description

**Steps to reproduce the problem:**  

This issue exists in Safe Browsing in Google Chrome.  

Warning is not triggered when downloading executable files with specific extensions.

\* This vulnerability only works on macOS.

I saw two reports previously reported to Chrome. We have investigated these two reports in detail and have found that this patch is incomplete.

CVE-2020-6402: <https://bugs.chromium.org/p/chromium/issues/detail?id=1029375>  

CVE-2022-1874: <https://bugs.chromium.org/p/chromium/issues/detail?id=1251588>

The content of these two reports was that when the executable files called fileloc / atloc and inetloc were downloaded, there was no warning "This type of file can harm your computer. Do you want to keep poc.ftploc anyway", making them vulnerable to arbitrary command execution.

\* Please refer to the demo\_ftploc / demo\_atloc video.

I have found other extensions that say that these commands can be done. This extension is .ftploc / .atloc, and as a result of the confirmation, it was confirmed that it is saved without outputting a warning message.

If the warning is not output when downloading the executable file, it can be used in the exploit as follows.

# Reproduce

1. Download the attachment `poc.ftploc` / `poc.atloc`.
2. There is no warning about downloading this executable file.

# Credit

Dohyun Lee (@l33d0hyun) of SSD Secure Disclosure Labs

**Problem Description:**  

The files whose externsion is ftploc / atloc should be blocked but are not, allowing macOS users of Chrome are at risk as these files are not marked as unsafe.

**Additional Comments:**

\*\*Chrome version: \*\* 103.0.5060.14 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [atloc_exploit.zip](attachments/atloc_exploit.zip) (application/octet-stream, 2.2 KB)
- [Demo_atloc.mov](attachments/Demo_atloc.mov) (video/quicktime, 3.1 MB)
- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 2.2 KB)
- [Demo_ftploc.mov](attachments/Demo_ftploc.mov) (video/quicktime, 2.1 MB)
- [poc.ftploc](attachments/poc.ftploc) (application/octet-stream, 295 B)
- [poc.atloc](attachments/poc.atloc) (application/octet-stream, 295 B)

## Timeline

### no...@ssd-disclosure.com (2022-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-11)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-07-11)

> 1. Download the attachment `poc.ftploc` / `poc.atloc`.

I don’t see anything by that name in anything you’ve attached, and I checked atloc_explot.zip and exploit.zip. Can you check that you’ve provided everything we need for reproduction?

[Monorail components: Services>Safebrowsing]

### jd...@chromium.org (2022-07-11)

Since there was no .ftploc or .atloc file attached, and a quick search of the internet didn't find me its format, I can't actually assess whether this is actually a security issue or not.

If I had to guess, I'd say it's not. I expect .ftploc or .atloc to be similar to downloading a .lnk file on Window -- it can point to an existing exe, but it has no scary payload on its own.

Having said that, drubery@ is better situated to evaluate such things.

I've assigned labels conservatively, assuming that .ftploc/.atloc is indeed a risky extension -- better safe than sorry.

### [Deleted User] (2022-07-11)

[Empty comment from Monorail migration]

### no...@ssd-disclosure.com (2022-07-17)

The two files seems to have been removed (by mistake?)

They also exist inside the .zip files which is a "full" exploit

### no...@ssd-disclosure.com (2022-09-01)

Any plans on addressing this?

### aj...@google.com (2022-12-20)

[Empty comment from Monorail migration]

### dr...@chromium.org (2023-01-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/feceb3816d399fab9f245c7fc979454677c2adb8

commit feceb3816d399fab9f245c7fc979454677c2adb8
Author: Daniel Rubery <drubery@chromium.org>
Date: Wed Jan 25 14:20:22 2023

Add download_file_types entries for ftploc and atloc

These are analogous to fileloc, which we already have an entry for.

Fixed: 1343317
Change-Id: I4cd76ccbaffec5895b51a926bc1b3964f927ed19
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4193336
Auto-Submit: Daniel Rubery <drubery@chromium.org>
Reviewed-by: thefrog <thefrog@chromium.org>
Commit-Queue: thefrog <thefrog@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1096745}

[modify] https://crrev.com/feceb3816d399fab9f245c7fc979454677c2adb8/components/safe_browsing/content/resources/download_file_types.asciipb
[modify] https://crrev.com/feceb3816d399fab9f245c7fc979454677c2adb8/components/safe_browsing/content/resources/download_file_types_experiment.asciipb
[modify] https://crrev.com/feceb3816d399fab9f245c7fc979454677c2adb8/tools/metrics/histograms/enums.xml


### [Deleted User] (2023-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-03)

Thank you for this report. While we don't consider this to be a security bug in Chrome's threat model, but more of a change to a security feature, we did want to thank you for this report. As such, we would like to extend to you a $500 VRP reward. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-02-04)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### no...@ssd-disclosure.com (2023-03-08)

Are you going to ask for a CVE for this item?

Also can you add:
dohyunl@ssd-disclosure.com

To this thread?

### am...@chromium.org (2023-03-08)

Hello, since we do not consider this a security bug in our threat model, this issue won't be issued a CVE. 

### [Deleted User] (2023-03-30)

hello amyressler@chromium.org ,

Except for this case, 1332392, 1029375, 1251588 are recognized as Security bugs and assigned CVE IDs.
In particular, in the case of 1029375 and 1251588, these two cases are very similar to this case.

What exactly is the reason this is classified as a general bug unlike the cases above?

### dr...@chromium.org (2023-03-30)

I will let Amy comment on the CVE process, but I can share some context from a Safe Browsing perspective.

Starting Chrome M105, we changed the way the file type policy is used. Previously, users were seeing warnings based solely on the file type for each of the bugs you listed. But in M105 and later, Safe Browsing server-side evaluation is now considered more authoritative, and we show a lot fewer warnings based only on the file type. This was done because without real evidence of harmful behavior, the warning just wasn't useful to users. That means the code we landed to fix this bug only impacts users when
- Safe Browsing is disabled (but we clearly state the security impact of doing this)
- Safe Browsing servers are down (but this is exceptionally rare)

M105 branched on July 21, so the behavior change was done after 1332392 (which is why we treated it differently), but around the same time this bug was filed.

### [Deleted User] (2023-03-30)

Starting Chrome M105, the way file type policies are used has changed.
However, at the time this vulnerability was reported, M105 had not been branched and the policy change had not been applied and was affecting the Stable version. I believe that bugs reported at a time when the new policy has not been forked should be evaluated differently.

### [Deleted User] (2023-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-03)

This issue was migrated from crbug.com/chromium/1343317?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1402611, crbug.com/chromium/1407127]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060235)*
