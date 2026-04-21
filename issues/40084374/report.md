# Extension install crashes browser at onDownloadProgress and onInstallStageChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [40084374](https://issues.chromium.org/issues/40084374) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Reporter** | ad...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-05-23 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36

Steps to reproduce the problem:
1. Place these functions on the page in which the inline installation is run
            chrome.webstore.onInstallStageChanged.addListener(function (stage) {
            });

chrome.webstore.onDownloadProgress.addListener(function (percentDownloaded) {
            });

Reference to these functions at the webstore API: https://developer.chrome.com/extensions/webstore

2. Try to install, uninstall, and install the extension again. More than 90% of the time the second installation will result in a browser crash (segmentation fault).

What is the expected behavior?
For the listeners to run without crashing the browser.

What went wrong?
The browser crashes on either one of the events with the following error:

../../chrome/browser/extensions/api/webstore/webstore_api.cc: No such file or directory.

Crashed report ID: 

How much crashed? Whole browser

Is it a problem with a plugin? No 

Did this work before? No 

Chrome version: 50.0.2661.102  Channel: stable
OS Version: 6.1 (Windows 7, Windows Server 2008 R2)
Flash Version: Shockwave Flash 21.0 r0

## Attachments

- [cb240253-693c-43be-a169-1cf56a91d3bd.txt](attachments/cb240253-693c-43be-a169-1cf56a91d3bd.txt) (text/plain, 141.1 KB)

## Timeline

### ra...@chromium.org (2016-05-24)

[Empty comment from Monorail migration]

### ma...@superhuman.com (2016-06-14)

I can confirm that I have the same behavior. It happens if I attach either listener listed above and even if have nothing inside the callback. I can reproduce it almost 95% of the time.

### ro...@robwu.nl (2016-06-18)

Chrome version: 51.0.2704.79
Suspected commit: c80fe5faf691860c344bcc98aa784a6eeefae08d.

When a webstore event listener is installed before a call to chrome.webstore.install, then WebstoreAPI::OnInlineInstallStart store a IPC::Sender* (a TabHelper) in a list. This list is never cleared, so when the tab is closed before the installation completes, the stale IPC::Sender* pointer is dereferenced.

There are two ways to reproduce this:
1. Visit https://adblockplus.org/
2. Register any webstore event listener:
chrome.webstore.onDownloadProgress.addListener(x => {});
3. Click on the install button (and cancel the dialog).
4. Open https://adblockplus.org in a new tab and close the previous tab.
5. Click on the install button and confirm.

Result:
AddressSanitizer: heap-use-after-free on address 0x615000139508 at pc 0x56190ab7f65d bp 0x7ffc4595fd90 sp 0x7ffc4595fd88
READ of size 8 at 0x615000139508 thread T0 (chrome)
    #0 0x56190ab7f65c in SendInstallMessageIfObserved chrome/browser/extensions/api/webstore/webstore_api.cc:123:7
    #1 0x56190a96bca7 in OnBeginExtensionDownload chrome/browser/extensions/install_tracker.cc:91:3
    #2 0x56190a9db34c in Start chrome/browser/extensions/webstore_installer.cc:366:3
    #3 0x56190a9e5d67 in OnInstallPromptDone chrome/browser/extensions/webstore_standalone_installer.cc:237:3
    #4 0x561907c2e995 in Run base/callback.h:397:12
    #5 0x561907c2e995 in Accept chrome/browser/ui/views/extensions/extension_install_dialog_view.cc:611:0
    #6 0x56190950f0b1 in AcceptWindow ui/views/window/dialog_client_view.cc:75:35

The above reproduction steps would be resolved if WebstoreAPI::OnInlineInstallFinished was properly called (introduced in c80fe5faf691860c344bcc98aa784a6eeefae08d but never called). Still, because the IPC::Sender* is stored as a stale pointer, the crash would still occur if the tab is closed between the start and end of the installation:
1. Visit https://adblockplus.org/
2. Register any webstore event listener:
chrome.webstore.onDownloadProgress.addListener(x => {});
3. Click on the install button and confirm.
4. Close the tab after a split second before completion of the installation (note: make sure that another tab was open before starting step 1, otherwise this step would quit the browser).

Result:
AddressSanitizer: heap-use-after-free on address 0x615000139508 at pc 0x56442380a65d bp 0x7fff294b2630 sp 0x7fff294b2628
READ of size 8 at 0x615000139508 thread T0 (chrome)
    #0 0x56442380a65c in SendInstallMessageIfObserved chrome/browser/extensions/api/webstore/webstore_api.cc:123:7
    #1 0x5644235f73c7 in OnBeginCrxInstall chrome/browser/extensions/install_tracker.cc:110:3
    #2 0x5644235482d5 in NotifyCrxInstallBegin chrome/browser/extensions/crx_installer.cc:835:3
    #3 0x5644235482d5 in InstallCrxFile chrome/browser/extensions/crx_installer.cc:182:0
    #4 0x5644235480da in InstallCrx chrome/browser/extensions/crx_installer.cc:174:3
    #5 0x56442366a267 in StartCrxInstaller chrome/browser/extensions/webstore_installer.cc:750:3
    #6 0x56442366941e in OnDownloadUpdated chrome/browser/extensions/webstore_installer.cc:546:7
    #7 0x564420daff97 in UpdateObservers content/browser/download/download_item_impl.cc:270:3
    #8 0x564420dbcec9 in OnDownloadRenamedToFinalName content/browser/download/download_item_impl.cc:1479:5


[Monorail components: Platform>Extensions]

### es...@chromium.org (2016-06-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-19)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 27 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-06-19)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-06-28)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-06-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d30a8bd191f17b61938fc87890bffc80049b0774

commit d30a8bd191f17b61938fc87890bffc80049b0774
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Thu Jun 30 16:02:29 2016

[Extensions] Rework inline installation observation

Instead of observing through the WebstoreAPI, observe directly in the TabHelper.
This is a great deal less code, more direct, and also fixes a lifetime issue
with the TabHelper being deleted before the inline installation completes.

BUG=613949

Review-Url: https://codereview.chromium.org/2103663002
Cr-Commit-Position: refs/heads/master@{#403188}

[delete] https://crrev.com/92e65345e6377de1ac9c2f3d783dde6f7b1aa65b/chrome/browser/extensions/api/webstore/webstore_api.cc
[delete] https://crrev.com/92e65345e6377de1ac9c2f3d783dde6f7b1aa65b/chrome/browser/extensions/api/webstore/webstore_api.h
[modify] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/browser/extensions/browser_context_keyed_service_factories.cc
[modify] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/browser/extensions/tab_helper.cc
[modify] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/browser/extensions/tab_helper.h
[modify] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/browser/extensions/webstore_inline_installer_browsertest.cc
[modify] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/browser/extensions/webstore_standalone_installer.cc
[modify] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/chrome_browser_extensions.gypi
[modify] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/chrome_common.gypi
[add] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/common/extensions/webstore_install_result.cc
[modify] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/common/extensions/webstore_install_result.h
[add] https://crrev.com/d30a8bd191f17b61938fc87890bffc80049b0774/chrome/test/data/extensions/api_test/webstore_inline_install/double_install.html


### rd...@chromium.org (2016-07-06)

Should be fixed.  This made the M53 cut, but I'd like to merge to M52 if possible.  M51 is probably unnecessary at this point.

### sh...@chromium.org (2016-07-07)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### rd...@chromium.org (2016-07-14)

It's been baking for a couple of weeks now, and I haven't seen any bugs or crashes related to it, so I think we're good to go.

### go...@chromium.org (2016-07-14)

Approving merge to M52 branch 2743 based on https://crbug.com/chromium/613949#c14 after discussing with awhalley@ as the change is also in M53 dev. Please merge ASAP. Thank you.

### bu...@chromium.org (2016-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2bde772815413a04017f6610fae1bc986c0767ba

commit 2bde772815413a04017f6610fae1bc986c0767ba
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Jul 14 17:58:49 2016

[Extensions] Rework inline installation observation

Instead of observing through the WebstoreAPI, observe directly in the TabHelper.
This is a great deal less code, more direct, and also fixes a lifetime issue
with the TabHelper being deleted before the inline installation completes.

BUG=613949

Review-Url: https://codereview.chromium.org/2103663002
Cr-Commit-Position: refs/heads/master@{#403188}
(cherry picked from commit d30a8bd191f17b61938fc87890bffc80049b0774)

Review URL: https://codereview.chromium.org/2148343002 .

Cr-Commit-Position: refs/branch-heads/2743@{#626}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[delete] https://crrev.com/620e709cdbc678b2d2e5d576902e02be93333b69/chrome/browser/extensions/api/webstore/webstore_api.cc
[delete] https://crrev.com/620e709cdbc678b2d2e5d576902e02be93333b69/chrome/browser/extensions/api/webstore/webstore_api.h
[modify] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/browser/extensions/browser_context_keyed_service_factories.cc
[modify] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/browser/extensions/tab_helper.cc
[modify] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/browser/extensions/tab_helper.h
[modify] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/browser/extensions/webstore_inline_installer_browsertest.cc
[modify] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/browser/extensions/webstore_standalone_installer.cc
[modify] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/chrome_browser_extensions.gypi
[modify] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/chrome_common.gypi
[add] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/common/extensions/webstore_install_result.cc
[modify] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/common/extensions/webstore_install_result.h
[add] https://crrev.com/2bde772815413a04017f6610fae1bc986c0767ba/chrome/test/data/extensions/api_test/webstore_inline_install/double_install.html


### aw...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

Congratulations! The panel has awarded $500 for this bug. A member of our finance team will be in touch within the next few weeks.

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### aw...@google.com (2016-10-06)

Hello - our finance team is having a hard time reaching you - is there a better email address to use?

### sh...@chromium.org (2016-10-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/613949?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084374)*
