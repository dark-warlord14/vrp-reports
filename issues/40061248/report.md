# Security:  UAF in PluginVmInstaller::DetectImageType

| Field | Value |
|-------|-------|
| **Issue ID** | [40061248](https://issues.chromium.org/issues/40061248) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ya...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2022-10-06 |
| **Bounty** | $1,000.00 |

## Description

KeyedService\* PluginVmInstallerFactory::BuildServiceInstanceFor(  

content::BrowserContext\* context) const {  

return new PluginVmInstaller(Profile::FromBrowserContext(context)); //[0]  

}  

**-------------------------** ---------  

PluginVmInstaller::StartImport() {  

LOG\_FUNCTION\_CALL();  

DCHECK\_EQ(installing\_state\_, InstallingState::kDownloadingImage);  

UpdateInstallingState(InstallingState::kImporting);  

UpdateProgress(/\*state\_progress=\*/0);

base::ThreadPool::PostTaskAndReply(  

FROM\_HERE, {base::TaskPriority::USER\_VISIBLE, base::MayBlock()},  

base::BindOnce(&PluginVmInstaller::DetectImageType,  

base::Unretained(this)), //[1]  

base::BindOnce(&PluginVmInstaller::OnImageTypeDetected,  

weak\_ptr\_factory\_.GetWeakPtr()));  

}

This is same as [https://crbug.com/chromium/1341907.PluginVmInstaller[0]](https://crbug.com/chromium/1341907.PluginVmInstaller%5B0%5D) Object will be created as a service. When the browser is closed, the service will also be down, the object will be destroyed, and DetectImageType is bound to the callback function as base::Unretained,will continue to execute in the child thread, causing UAF.

Patch

Use weakptr

## Timeline

### [Deleted User] (2022-10-06)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-06)

This is another instance of the KeyedService-and-PostTaskWithoutWeakPtr UAF pattern. Should only occur during browser shutdown.
Also see another possible instance in https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ash/plugin_vm/plugin_vm_installer.cc;drc=0f194feacda7f8b5268e96fc68ee8dc74deefd31;l=634

### lz...@google.com (2022-10-10)

https://crbug.com/chromium/1341907 is fixed. Close this as duplicate.

### lz...@google.com (2022-10-10)

[Empty comment from Monorail migration]

### ya...@gmail.com (2022-10-11)

Hello lziest@,Are you sure this has been fixed, can anunoy@ help confirm it?

### jd...@chromium.org (2022-10-18)

Re-opening per #5.

### jd...@chromium.org (2022-10-18)

Specifically, the reporter said that this is the same _pattern_ as in 1341907, not that it's literally the same bug.

### jd...@chromium.org (2022-10-18)

[Empty comment from Monorail migration]

### al...@google.com (2022-10-18)

As is this report isn't rewardable. Please include a stack trace or something that demonstrates the code path is reachable.

### [Deleted User] (2022-10-18)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-10-18)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-10-18)

While we wait for confirmation on whether this is reachable, in the case it were it'd be a high severity bug.

### gi...@appspot.gserviceaccount.com (2022-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/08739fc6b4a107469642184f6970f5e65cc1f7f2

commit 08739fc6b4a107469642184f6970f5e65cc1f7f2
Author: Timothy Loh <timloh@chromium.org>
Date: Wed Oct 19 22:06:04 2022

Remove base::Unretained usage in PluginVmInstaller

We can't guarantee that the object hasn't been destroyed by the time the
task runs, so we shouldn't use base::Unretained.

Bug: 1371844
Change-Id: Id23509d69d5e8ce7b5fbb8bb275bff99d7fab406
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3965730
Auto-Submit: Timothy Loh <timloh@chromium.org>
Commit-Queue: Joel Hockey <joelhockey@chromium.org>
Reviewed-by: Joel Hockey <joelhockey@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1061266}

[modify] https://crrev.com/08739fc6b4a107469642184f6970f5e65cc1f7f2/chrome/browser/ash/plugin_vm/plugin_vm_installer.h
[modify] https://crrev.com/08739fc6b4a107469642184f6970f5e65cc1f7f2/chrome/browser/ash/plugin_vm/plugin_vm_installer.cc


### [Deleted User] (2022-10-20)

timloh: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2022-10-27)

This codepath requires a device to be enrolled with the enterprise admin having set up Parallels (including getting a license for the device). The user then needs to manually invoke the installer, and then log out the browser at the right time (after the installer has downloaded the image specified by the admin, typically maybe 15GB?) to try and cause a race. From my perspective I don't think either party (user or admin) would be able to do much with this.

### [Deleted User] (2022-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-27)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-03)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug. Thank you for your efforts in reporting this issue to us!

### am...@google.com (2022-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### is...@google.com (2023-05-24)

This issue was migrated from crbug.com/chromium/1371844?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1375913]
[Monorail mergedinto: crbug.com/chromium/1341907]

### dt...@google.com (2025-02-13)

Bulk update of issues accidentally marked as duplicate in issue tracker migration (b/325072672)

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061248)*
