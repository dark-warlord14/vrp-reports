# Security: arbitrarily file write + bypass dangerous file check via DevTools API

| Field | Value |
|-------|-------|
| **Issue ID** | [40090285](https://issues.chromium.org/issues/40090285) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools, Platform>Extensions>API, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | pf...@chromium.org |
| **Created** | 2018-01-24 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS  

The DevTools protocol has a method Page.downloadBehavior that allows one to automatically accept a download. The implementation at the backend unconditionally marks such files as safe, regardless of the file type [1].

Because of this, the file can automatically be opened without warnings via the chrome.downloads.download API, chrome://downloads or the download shelf.

**VERSION**  

Chrome Version: 63.0.3239.132 (stable), 66.0.3330.0 (canary)

**REPRODUCTION CASE**  

I have attached a PoC that fully automates the exploitation via an extension (launching mspaint).

Although the extension is used for exploitation, the actual vulnerability here is the implementation of the DevTools protocol. It should not allow the download protection to be bypassed.

[1] <https://chromium.googlesource.com/chromium/src/+/5646f547e03f79baf219ab6465ceb9cc0740b36c/content/browser/devtools/protocol/devtools_download_manager_delegate.cc#178>

## Attachments

- [debugger-downloadBehavior.zip](attachments/debugger-downloadBehavior.zip) (application/octet-stream, 1.7 KB)
- [debugger-downloadBehavior-mspaint.ogv](attachments/debugger-downloadBehavior-mspaint.ogv) (video/ogg, 523.1 KB)
- [debugger-downloadBehavior-v2.zip](attachments/debugger-downloadBehavior-v2.zip) (application/octet-stream, 1.8 KB)

## Timeline

### el...@chromium.org (2018-01-24)

Note: Cannot repro from a Corp Profile due to admin-controlled permissions blocking.

[Monorail components: Platform>Extensions>API UI>Browser>Downloads]

### ro...@robwu.nl (2018-01-25)

In the report I focused on the dangerous file check bypass (arbitrary code execution outside the sandbox).

Perhaps it is also worth noting that the vulnerable method can also be used to write to arbitrary files. Combined with the ability to read local files (https://crbug.com/chromium/805557) and vulnerabilities to crash or restart Chrome, this could be used to modify Chrome's configuration files to unlock more powers, persistently.

If there is a higher reward for it, I'm willing to develop a PoC exploit.

### me...@chromium.org (2018-01-25)

When I run the repro on Windows 10, I get a Windows security warning dialog for the vbs file. Is the idea to bypass that dialog?

### me...@chromium.org (2018-01-25)

^ I see this on 64.0.3282.119 stable, by the way.

### ro...@robwu.nl (2018-01-25)

@#3 That is a warning from Windows (which may or may not show, depending on the configuration of "SaveZoneInformation"). If you see the warning then it means that Chrome is already attempting to run the program.

Another way to see that Chrome's defence has failed is to run the following from the extension background's console:
   chrome.downloads.search({}, console.log);

... and observe that the "danger" key of the download is "safe" (https://developer.chrome.com/extensions/downloads#type-DangerType).

### me...@chromium.org (2018-01-26)

I'm aware it's the mark-of-the-web dialog from Windows, hence my question about whether it was expected to be bypassed as well, because that's what the video implies :)

I'd like to get an opinion from SafeBrowsing before assigning severity to this, but this seems low severity given the significant user interaction required to run the executable (extension install + accepting OS warning).

[Monorail components: Services>Safebrowsing]

### me...@chromium.org (2018-01-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-27)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2018-01-27)

Severity-low underestimates the severity of this bug. I expected High severity.


> my question about whether it was expected to be bypassed as well

It depends on the configured SaveZoneInformation policies [1]. In my Windows 7 VM, there were no OS warnings, until I remove HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Associations\LowRiskFileTypes (which contained ".vbs").
I have modified the PoC to use .url instead of .vbs. Now my Windows 7 VM launches mspaint again without warnings (see attachment).

MOTW can also be bypassed by saving the file to a filesystem that does not support Alternate Data Streams (ADS), such as a FAT32-formatted USB stick or a network drive. An attacker can either guess the location (or enumerate local drives (e.g. with https://crbug.com/chromium/805557) to find such a location), and use the vulnerable method to write a file to that location.


> low severity given the significant user interaction ... (extension install + accepting OS warning).

Because of the Extension install requirement, I would drop the severity from Critical (escaped sandbox) to High.

The OS warning is Windows-specific and optional (see above).
On Linux, when I launch the above PoC, a text editor is opened via xdg-open (default handler of .vbs), but it could have been any other program or interpreter.

[1] https://support.microsoft.com/en-us/help/883260/information-about-the-attachment-manager-in-microsoft-windows

### ro...@robwu.nl (2018-01-29)

As I remarked in  https://bugs.chromium.org/p/chromium/issues/detail?id=805905#c8 , the Page.setDownloadBehavior method was primarily designed for headless Chrome, so disabling this method for non-headless Chrome sounds like the best fix to me.

### me...@chromium.org (2018-01-29)

It would be useful to mention that you were testing on Windows 7. I tested with multiple VMs Microsoft offers at https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/. Using the PoC v2 in https://crbug.com/chromium/805445#c9:
- IE8 on Win7, IE9 on Win7, IE10 on Win7: No MOTW warning.
- IE11 on Win7, IE11 on Win8 : MOTW warning is displayed.

All Win7 VMs have Windows 7 Enterprise edition (Build 7601: Service Pack 1) for VirtualBox. None of them have the HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Associations\LowRiskFileTypes entry. I suspect the IE version makes a difference here. Can you please try with a VM that has IE11? (that's the only supported IE version at the moment)

Also, I'm well aware MOTW isn't supported on FAT32, but all Windows versions supported by Chrome (Windows 7 and above) default to NTFS installations. Downloading to a FAT32 filesystem is a non-default configuration, because it would either require changing default OS installation or the default download directory.

> On Linux, when I launch the above PoC, a text editor is opened via xdg-open (default handler of .vbs), but it could have been any other program or interpreter.

SafeBrowsing doesn't mark .vbs files as dangerous on Linux anyways [1], so bypassing it doesn't gain anything to the attacker. This isn't different than just using chrome.download.open to open the .vbs file on Linux.

We also discussed this offline, and if there is a reliable bypass of the MOTW warning via devtools, we are happy to reconsider the severity. But currently the only bypass is SafeBrowsing dangerous file types mark, which we'd consider a medium severity on its own. The fact that an extension with powerful permissions is required to use this bypass and that only a subset of users on old, unsupported OS configurations is directly impacted, I think low severity is appropriate.

[1] https://cs.chromium.org/chromium/src/chrome/browser/resources/safe_browsing/download_file_types.asciipb?rcl=694bf0eb3c5de0a290054716b548e4cadf9284ee&l=1395

### me...@chromium.org (2018-01-29)

ericlaw@ pointed that ReFS on Win8 didn't support MoTW either, and that's not an unsupported configuration. With that information, raising this back to severity-medium. I still maintain that severity-high is too high here, because of the two separate mitigating factors (extension install and MOTW on most configs) but I'll leave it to the next sheriff to decide whether this is a fair assessment.

### me...@chromium.org (2018-01-29)

dvallet: Can you please take a look?

### sh...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### dv...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/81ad563077484d112e544347da87c09dd2ba0af8

commit 81ad563077484d112e544347da87c09dd2ba0af8
Author: David Vallet <dvallet@chromium.org>
Date: Wed Jan 31 05:50:14 2018

Always mark content downloaded by devtools delegate as potentially dangerous

Bug: 805445
Change-Id: I7051f519205e178db57e23320ab979f8fa9ce38b
Reviewed-on: https://chromium-review.googlesource.com/894782
Commit-Queue: David Vallet <dvallet@chromium.org>
Reviewed-by: Pavel Feldman <pfeldman@chromium.org>
Cr-Commit-Position: refs/heads/master@{#533215}
[modify] https://crrev.com/81ad563077484d112e544347da87c09dd2ba0af8/content/browser/devtools/protocol/devtools_download_manager_delegate.cc


### va...@chromium.org (2018-02-02)

[Empty comment from Monorail migration]

[Monorail components: -Services>Safebrowsing]

### sh...@chromium.org (2018-02-08)

pfeldman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-02-14)

dvallet: Can this be closed now? Thanks.

### ro...@robwu.nl (2018-02-15)

I have reported two issues,
- safe browsing bypass - fixed.
- writing to arbitrary locations - not fixed yet.

The combination of the two increases the likelihood of a MOTW bypass, because an attacker can write to a filesystem that does not support MOTW, such as a (FAT32-formatted) USB stick.

### dv...@chromium.org (2018-02-15)

We are working on a new interface for downloads: https://crrev.com/c/861546
Once it lands, we'll remove the download path option.

### sh...@chromium.org (2018-02-24)

pfeldman: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2018-03-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-16)

This bug requires manual review: M66 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2018-03-16)

This was fixed before the M66 branch point.

### aw...@chromium.org (2018-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-26)

And $2,000 for this one - cheers!

### aw...@chromium.org (2018-03-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-06-20)

(note that even though this was fixed before M66 branch point, it should have retained the M-66 label)

### aw...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-21)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-12-04)

[Empty comment from Monorail migration]

### is...@google.com (2018-12-04)

This issue was migrated from crbug.com/chromium/805445?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>DevTools, Platform>Extensions>API, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090285)*
