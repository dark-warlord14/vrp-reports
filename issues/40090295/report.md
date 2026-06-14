# Security: Bad cast to ChromeDownloadManagerDelegate* from DevToolsDownloadManagerDelegate*

| Field | Value |
|-------|-------|
| **Issue ID** | [40090295](https://issues.chromium.org/issues/40090295) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | pf...@chromium.org |
| **Created** | 2018-01-25 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

DownloadPrefs::FromDownloadManager is reachable from several places (e.g. when a download is started) and implemented as follows [1]:  

DownloadPrefs::FromDownloadManager(  

DownloadManager\* download\_manager) {  

ChromeDownloadManagerDelegate\* delegate =  

static\_cast<ChromeDownloadManagerDelegate\*>( // <---- WARNING  

download\_manager->GetDelegate());  

return delegate->download\_prefs(); // <---- undefined behavior after bad cast  

}

At the place marked "WARNING", a bad cast occurs:  

download\_manager->GetDelegate() is cast from content::DownloadManagerDelegate\* to ChromeDownloadManagerDelegate\*.  

But it can also be a DevToolsDownloadManagerDelegate\*, when the DevToolsDownloadManagerDelegate::TakeOver is called  

(via the "Page.setDownloadBehavior" DevTools protocol method [2]) [3].

This can be exploited via Chrome extensions and the remote debugging protocol.

**VERSION**  

Chrome Version: 64.0.3282.119 (stable)

**REPRODUCTION CASE**  

Download and unpack the attached extension and start Chrome:

$ ./chromium --user-data-dir=/tmp/whatever --load-extension=/tmp/downloadBehavior-bad-cast

Received signal 11 SEGV\_MAPERR ffffd86fb80ead74  

#0 0x559f72545b77 base::debug::StackTrace::StackTrace()  

#1 0x559f725456df base::debug::(anonymous namespace)::StackDumpSignalHandler()  

#2 0x7f33a9b63da0 <unknown>  

#3 0x559f735e81f7 subtle::PrefMemberBase::VerifyPref()  

#4 0x559f722dd70d DownloadPrefs::PromptForDownload() <--- The memory here is \*not\* a DownloadPrefs\*  

#5 0x559f722fbc7d DownloadFilePicker::DownloadFilePicker() <--- Calls DownloadPrefs::FromBrowserContext, which calls FromDownloadManager  

#6 0x559f722fe0b6 DownloadTargetDeterminer::DoRequestConfirmation()  

#7 0x559f722fd6d3 DownloadTargetDeterminer::DoLoop()

PS. I find it peculiar that PageHandler::SetDownloadBehavior changes the behavior for BrowserContext\* (which affects all tabs in the same profile), even though the "Page.setDownloadBehavior" DevTools command is only supposed to alter the behavior for a single target (page).

[1] <https://chromium.googlesource.com/chromium/src/+/6fd2b931db44eadcf5c2d33409d8b4e6bf4f6ad7/chrome/browser/download/download_prefs.cc#247>  

[2] <https://chromium.googlesource.com/chromium/src/+/9fa5fa7e7c5aa6f67ee721cd4022de491dc255d1/content/browser/devtools/protocol/page_handler.cc#724>  

[3] <https://chromium.googlesource.com/chromium/src/+/6fd2b931db44eadcf5c2d33409d8b4e6bf4f6ad7/content/browser/devtools/protocol/devtools_download_manager_delegate.cc#57>

## Attachments

- [downloadBehavior-bad-cast.zip](attachments/downloadBehavior-bad-cast.zip) (application/octet-stream, 1.9 KB)
- [asan-manual-repro-63.0.3239.84.log](attachments/asan-manual-repro-63.0.3239.84.log) (text/plain, 17.7 KB)
- [background.js](attachments/background.js) (text/plain, 981 B)
- [manifest.json](attachments/manifest.json) (text/plain, 294 B)
- [asan-manual-repro-64.0.3282.119.log](attachments/asan-manual-repro-64.0.3282.119.log) (text/plain, 14.8 KB)

## Timeline

### ro...@robwu.nl (2018-01-25)

For clarity, content::DownloadManagerDelegate is the base class of
ChromeDownloadManagerDelegate [4] and
DevToolsDownloadManagerDelegate [5].

But download_prefs() is part of ChromeDownloadManagerDelegate (not of the base class) (and both classes have completely different members).


[4] https://chromium.googlesource.com/chromium/src/+/ca91e7d0fceae42b489bb5e09d17e0782917e43e/chrome/browser/download/chrome_download_manager_delegate.h#49
[5] https://chromium.googlesource.com/chromium/src/+/ca91e7d0fceae42b489bb5e09d17e0782917e43e/content/browser/devtools/protocol/devtools_download_manager_delegate.h#27

### me...@chromium.org (2018-01-25)

dgozman: PTAL?

FWIW I seem to be unable to get a crash on Linux with a local and asan builds (even after enabling the auto download). Perhaps I'm missing a step.

### dg...@chromium.org (2018-01-25)

David, mind taking a look?

### ro...@robwu.nl (2018-01-25)

@#2

Odd. I got the crash on my local release build (v63), but not with an ASAN or Debug build, nor the official build from ArchLinux.
Here is another way to trigger the vulnerability (manually because it was the first caller that I picked. There are other extension APIs (e.g. chrome.browsingData and chrome.downloads) that can be used to automate the exploitation).

1. Modify the extension's background.js and delete (or comment out) the line with "a.click();" (so that the DevToolsDownloadManagerDelegate is still installed, but the code path is not yet triggered. Then trigger one of the other code paths, e.g. at https://chromium.googlesource.com/chromium/src/+/0fc0e49c81e22c768f9e1d3e8fe55a401425907d/chrome/browser/devtools/devtools_file_helper.cc#261
2. (Re)load the modified extension.
3. Visit chrome-devtools://devtools/blank in a new tab (not in tab created by the PoC extension because otherwise the DevTools session gets terminated).
4. Open the console and run the following snippet:
DevToolsHost.sendMessageToEmbedder('{"id":1, "method": "save", "params": ["data:,url", "content", true]}');

Chromium 66.0.3330.0 from chromium-browser-continuous crashes after these steps.
The crash of my local ASAN build (Chromium 63.0.3239.84) is detected by ASAN; I have attached the symbolized ASAN trace.

### ro...@robwu.nl (2018-01-25)

Here is the stack trace.

(and also a minimal extension for the manual test)

### ro...@robwu.nl (2018-01-26)

Here's the ASAN report for Chromium 64.0.3282.119, built from source, using the repro from #4 and #5.

It is virtually identical to the one from 63.0.3239.84 (in https://crbug.com/chromium/805905#c5).

### dv...@chromium.org (2018-01-29)

Thanks for the report. 
That part of the code indeed looks problematic.
I could add add check in DevToolsFileHelper to see if the DevToolsDownloadDelegate has taken over, but that wouldn't prevent other code from calling 
DownloadPrefs::FromDownloadManager (which is the one that does the static cast) 

To be sure that this doesn't happen, I'm thinking on adding a isChromeDownloadDelegate method in the DownloadManagerDelegate class to protect all static casts

wdyt? 

### ro...@robwu.nl (2018-01-29)

That suggestion looks like band-aid and not fix the root cause.

At the end of my initial report, I referred to some peculiarity. Namely that the DevTools API affects the whole BrowserContext (profile) instead of the inspected page. The sole purpose of DevToolsDownloadManagerDelegate is to override the download path via DevToolsDownloadManagerDelegate::DetermineDownloadTarget.

That only makes sense if a DevToolsDownloadManagerHelper is installed for the WebContents (i.e. when Page.setDownloadBehavior is called for a target). In all other cases the default (Chrome)DownloadManagerDelegate should be activated. Considering this, DownloadPrefs::FromDownloadManager can be rewritten to (recursively!!) use DevToolsDownloadManagerDelegate::proxy_download_delegate_ to ultimately retrieve a DownloadPrefs* if the class is not a ChromeDownloadManagerDelegate.

An alternative, much easier solution is to reject Page.setDownloadBehavior for non-headless commands. The primary purpose of this method is to support headless Chrome ( https://crbug.com/chromium/696481 ), so that should not be impacted. Another advantage of this solution https://crbug.com/chromium/805445 will be fixed too.

### me...@chromium.org (2018-01-29)

I can repro with the steps in https://crbug.com/chromium/805905#c4. Security-medium as this is a memory corruption that requires a specific extension to be installed.

### me...@chromium.org (2018-01-29)

[Empty comment from Monorail migration]

### dv...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### pf...@chromium.org (2018-01-30)

[Empty comment from Monorail migration]

### pf...@chromium.org (2018-01-31)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-02-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cbb2c0940d4e3914ccd74f6466ff4cb9e50e0e86

commit cbb2c0940d4e3914ccd74f6466ff4cb9e50e0e86
Author: Pavel Feldman <pfeldman@chromium.org>
Date: Thu Feb 01 01:36:25 2018

Don't downcast DownloadManagerDelegate to ChromeDownloadManagerDelegate.

DownloadManager has public SetDelegate method and tests and or other subsystems
can install their own implementations of the delegate.

Bug: 805905
Change-Id: Iecf1e0aceada0e1048bed1e2d2ceb29ca64295b8
TBR: tests updated to follow the API change.
Reviewed-on: https://chromium-review.googlesource.com/894702
Reviewed-by: David Vallet <dvallet@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#533515}
[modify] https://crrev.com/cbb2c0940d4e3914ccd74f6466ff4cb9e50e0e86/chrome/browser/browsing_data/chrome_browsing_data_remover_delegate_unittest.cc
[modify] https://crrev.com/cbb2c0940d4e3914ccd74f6466ff4cb9e50e0e86/chrome/browser/download/download_core_service_impl.cc
[modify] https://crrev.com/cbb2c0940d4e3914ccd74f6466ff4cb9e50e0e86/chrome/browser/download/download_prefs.cc
[modify] https://crrev.com/cbb2c0940d4e3914ccd74f6466ff4cb9e50e0e86/chrome/browser/ui/webui/settings/downloads_handler_unittest.cc


### sh...@chromium.org (2018-02-14)

pfeldman: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-02-14)

pfeldman: Can this be closed now? Thanks.

### sh...@chromium.org (2018-02-28)

pfeldman: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

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

This was fixed before M66 branch point.

### aw...@chromium.org (2018-03-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-03-26)

The VRP panel decided to award $500 for this reporting, that since the delegate isn't attacker controlled, it seems like it might not be exploitable, coupled with the extension/devtools precondition. Happy to reconsider for a higher amount if exploitability can be shown.

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

### aw...@chromium.org (2019-01-04)

[Empty comment from Monorail migration]

### is...@google.com (2019-01-04)

This issue was migrated from crbug.com/chromium/805905?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090295)*
