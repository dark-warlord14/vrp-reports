# Download Protection: MPKG file not checked on Mac OS

| Field | Value |
|-------|-------|
| **Issue ID** | [41247664](https://issues.chromium.org/issues/41247664) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Reporter** | ya...@nightwatchcybersecurity.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2016-04-06 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 49.0.2623.87 Official Build  

Operating System: Mac OS X El Capitan, version 10.11.3

**REPRODUCTION CASE**  

MPKG are another alias for PKG files in Mac OS, which are used by the Mac installer. To reproduce, take any .PKG file, rename it to .MPKG and double click. While Mac OS does show a warning for non-app store files, the same warning is shown for .PKG files which are checked by Chrome. MPKG file processing should match.

Sample PKG file:  

<https://github.com/Yubico/yubico.github.com/blob/master/yubikey-neo-manager/releases/yubikey-neo-manager-0.2.2-mac.pkg>

We can try to provide a patch if eligible for Patch Rewards

## Attachments

- [mpkg.patch](attachments/mpkg.patch) (application/octet-stream, 2.9 KB)
- [mpkg_new.patch](attachments/mpkg_new.patch) (application/octet-stream, 2.3 KB)

## Timeline

### np...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-04-19)

Attaching patch

### ya...@nightwatchcybersecurity.com (2016-04-22)

We have a better test case here:
https://theowl.xyz/cr/600908/test.mpkg

This is the same file as this one, just renamed:
https://developers.yubico.com/yubikey-neo-manager/Releases/yubikey-neo-manager-1.4.0-mac.pkg

### va...@chromium.org (2016-05-06)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-05-13)

Just wondering if this issue is still being looked at

### va...@chromium.org (2016-05-27)

Thanks for reporting the issue. I am able to reproduce the issue locally.
A .mpkg file is a meta .PKG file that can link to other .PKG files so we should treat them identically.

jialiul@ -- would you like to take this on?

### ji...@chromium.org (2016-05-27)

+nparker@, Do you mind providing a sample CL of adding new a extension to your shining dynamic file extension list? 

### np...@chromium.org (2016-05-27)

Yup, I'll create a cl for this

### ya...@nightwatchcybersecurity.com (2016-05-29)

@nparker: We are attaching a patch using the new dynamic file extension system

### np...@chromium.org (2016-05-30)

Ah.  I already have a CL pending: https://codereview.chromium.org/2010333004.  Yours was more complete though -- I was missing the GetDownloadType() change.  Thanks!

### bu...@chromium.org (2016-05-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/72b3586479fea68f62a871caba880f609c0dbd79

commit 72b3586479fea68f62a871caba880f609c0dbd79
Author: nparker <nparker@chromium.org>
Date: Tue May 31 23:22:47 2016

Make file type MPKG generate a download ping

BUG=600908
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2010333004
Cr-Commit-Position: refs/heads/master@{#396971}

[modify] https://crrev.com/72b3586479fea68f62a871caba880f609c0dbd79/chrome/browser/resources/safe_browsing/download_file_types.asciipb
[modify] https://crrev.com/72b3586479fea68f62a871caba880f609c0dbd79/chrome/common/safe_browsing/download_protection_util.cc
[modify] https://crrev.com/72b3586479fea68f62a871caba880f609c0dbd79/tools/metrics/histograms/histograms.xml


### np...@chromium.org (2016-05-31)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-06-01)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-06-07)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-06-07)

Is there a reason why the bounty is not $1,000 like the usual SB bypass?

### va...@chromium.org (2016-06-07)

The amount for a baseline report for Download Protection bypass is $500, as listed on [1].

The final amount is always chosen at the discretion of the reward panel.
In this case, the panel decided that the report was baseline quality and the patch trivial.

[1]: https://www.google.com/about/appsecurity/chrome-rewards/index.html

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-06-23)

We haven't heard from anyone regarding the reward

### in...@chromium.org (2017-03-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-03-09)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-03-10)

For all Download Protection VRP bugs: removing label Restrict-View-Google and adding Restrict-View-SecurityTeam instead.

### sh...@chromium.org (2017-03-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-03-11)

This issue was migrated from crbug.com/chromium/600908?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>Safebrowsing, Services>Safebrowsing>VRP]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41247664)*
