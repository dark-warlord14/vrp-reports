#  Download Protection: BIN bypasses checking on MacOs

| Field | Value |
|-------|-------|
| **Issue ID** | [41442267](https://issues.chromium.org/issues/41442267) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Reporter** | ya...@nightwatchcybersecurity.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2019-02-20 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 72.0.3626.109 (Official Build) (64-bit) [stable]  

Operating System: MacOS Mojave - 10.14.3

**REPRODUCTION CASE**  

The BIN file extension are opened by the Archive Mounter utility on Mac OS. That means you can take a ZIP file, rename it a BIN and serve it.

To reproduce, take any .ZIP file, and rename as a BIN file. Double click and the file will still be opened as ZIP. This is similar to the issue we reported before here:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=600907>

Attached is a test file using Yubico's package as follows:

1. Download the PKG file:  
   
   <https://developers.yubico.com/yubikey-manager-qt/Releases/yubikey-manager-qt-1.1.0-mac.pkg>
2. Create ZIP file with a BIN extension as follows:  
   
   zip test123.bin yubikey-manager-qt-1.1.0-mac.pkg
3. Download via Chrome, then double click the file, and double click the package

Test file can be found here:  

<http://theowl.xyz/cr/mimes/test123.bin>

Root cause is BIN being whitelisted here:  

<https://cs.chromium.org/chromium/src/chrome/browser/resources/safe_browsing/download_file_types.asciipb?l=29>

## Timeline

### ya...@nightwatchcybersecurity.com (2019-02-26)

@vakh@chromium.org - let me know if you need any additional information

### np...@chromium.org (2019-02-27)

->drubery to triage. We could consider attempting to un-zip all .bin files.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-02-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/54ce18841dc705258a797518a4d918ff60258457

commit 54ce18841dc705258a797518a4d918ff60258457
Author: Daniel Rubery <drubery@chromium.org>
Date: Thu Feb 28 01:29:16 2019

SafeBrowsing: Unpack BINs as ZIPs

MacOS will automatically unpack BIN files as ZIP archives, so we should
extract their contents and check for executables.

Bug: 933637
Change-Id: Ibef7c245cb53ab4519a0f91753bf2885f28b6a80
Reviewed-on: https://chromium-review.googlesource.com/c/1492485
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Auto-Submit: Daniel Rubery <drubery@chromium.org>
Reviewed-by: Nathan Parker <nparker@chromium.org>
Cr-Commit-Position: refs/heads/master@{#636226}
[modify] https://crrev.com/54ce18841dc705258a797518a4d918ff60258457/chrome/browser/resources/safe_browsing/download_file_types.asciipb


### va...@chromium.org (2019-03-01)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-03-25)

The new download_file_types has been pushed.

### sh...@chromium.org (2019-03-26)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2019-04-07)

Hi - is this eligible for VRP?

Thanks

### dr...@chromium.org (2019-04-09)

I think this should qualify, since the amount of user interaction is minimal. Just download the file, double-click the BIN, then double-click the executable.

### na...@google.com (2019-04-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-04-10)

Congrats! The Panel decided to reward $1,000 for this report! 

### na...@google.com (2019-04-10)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2019-04-11)

Thank you. At what point can I disclose?

### ya...@nightwatchcybersecurity.com (2019-04-11)

And also, would a CVE be assigned for something like this?

### sh...@chromium.org (2019-07-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@nightwatchcybersecurity.com (2019-07-03)

Since the view restrictions have been removed, we disclosed the bug publicly here:
https://wwws.nightwatchcybersecurity.com/2019/07/02/another-download-protection-bypass-in-google-chrome-bin-files-in-mac-os/

### is...@google.com (2019-07-03)

This issue was migrated from crbug.com/chromium/933637?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>Safebrowsing, Services>Safebrowsing>VRP]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41442267)*
