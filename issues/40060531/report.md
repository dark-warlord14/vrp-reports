# Security: Potential UAF in WebstoreInstallWithPrompt

| Field | Value |
|-------|-------|
| **Issue ID** | [40060531](https://issues.chromium.org/issues/40060531) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | om...@talon-sec.com |
| **Assignee** | db...@chromium.org |
| **Created** | 2022-08-08 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

The WebstoreInstallWithPrompt class holds `std::unique_ptr<content::WebContents> dummy_web_contents_` member which uses `Profile\*` that can be freed during the lifetime of the object (f.e. by process shutdown, profile sign-out etc..).  

In `~BrowserContextImpl` there is a check to see if there are any references that weren't freed before it's own destruction, and if this is the case a DumpWithoutCrashing is called.

**VERSION**  

Chrome Version: 104.0.5112.81 (stable)  

Operating System: Any (tested on Windows 10 21H2 19044.1826)

**REPRODUCTION CASE**  

The bug is reproduceable using the `/install-chrome-app` command-line switch, f.e.:  

"C:\Program Files\Google\Chrome\Application\chrome.exe" /install-chrome-app=gbkeegbaiigmenfmjfclcdgdpimamgkj

Chrome will try to download the Chrome App/Extension by the id, which will trigger a use of `WebstoreInstallWithPromptAppsOnly` that inherits from `WebstoreInstallWithPrompt`. If the user profile is destroyed during the download, the bug will occur.  

I simulated a slow network using NetLimiter, so the download of the app will not complete quickly, then closed the browser/sign-out the profile while still downloading.  

I attach the memory dump that was created + a patch for the suggested fix.  

The suggested fix adds a `ProfileObserver` to `WebstoreInstallWithPrompt`, so we can abort the install in case of the profile being destructed. I noticed a similar approach in `WebstoreReinstaller` with `WebContentsObserver`.

Type of crash: browser  

Crash State:  

CONTEXT: (.ecxr)  

rax=000000aef7dfdf60 rbx=000000aef7dfe4b0 rcx=000000aef7dfdf60  

rdx=00000000000000aa rsi=000000aef7dfdf60 rdi=0000000000000000  

rip=00007ffe1b6e6697 rsp=000000aef7dfdf40 rbp=000000aef7dfe500  

r8=00000000000004d0 r9=aaaaaaaaaaaaaaaa r10=00000fffb8da7ef6  

r11=000000aef7dfdf60 r12=aaaaaaaaaaaaaaaa r13=aaaaaaaaaaaaaaaa  

r14=aaaaaaaaaaaaaaaa r15=000000aef7dfe5e0  

iopl=0 nv up ei pl nz na pe nc  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00000202  

chrome\_elf!crash\_reporter::DumpWithoutCrashing+0x37:  

00007ffe`1b6e6697 4889f1 mov rcx,rsi  

Resetting default scope

EXCEPTION\_RECORD: (.exr -1)  

ExceptionAddress: 00007ffe1b6e6697 (chrome\_elf!crash\_reporter::DumpWithoutCrashing+0x0000000000000037)  

ExceptionCode: 0517a7ed  

ExceptionFlags: 00000000  

NumberParameters: 0

PROCESS\_NAME: chrome.exe

ERROR\_CODE: (NTSTATUS) 0x517a7ed - <Unable to get error code text>

EXCEPTION\_CODE\_STR: 517a7ed

STACK\_TEXT:  

000000ae`f7dfdf40 00007ffd`c17ed3dd : 00000000`00000000 00007ffd`c0e3f013 00000000`00000000 00000000`00000000 : chrome\_elf!crash\_reporter::DumpWithoutCrashing+0x37  

000000ae`f7dfe450 00007ffd`bdf2c7b2 : fffffffe`00000000 00007ffd`c137c7b2 fffffffe`00000000 0000448a`0008f400 : chrome!base::debug::DumpWithoutCrashing+0x18d  

000000ae`f7dfe510 00007ffd`bdf2bf71 : 00000000`00000000 00007ffd`c75a7d61 00007ffd`c75a7d3e 000079c4`000000d2 : chrome!content::BrowserContextImpl::~BrowserContextImpl+0x6d2  

000000ae`f7dfe680 00007ffd`bdf2be34 : 0000448a`00228088 0000448a`000bf900 0000448a`000bf878 00000000`00000000 : chrome!content::BrowserContext::~BrowserContext+0x61  

000000ae`f7dfe760 00007ffd`be41dc60 : 0000448a`00228088 fffffffe`00000000 0000448a`000bf800 0000448a`0005cb08 : chrome!Profile::~Profile+0x164  

000000ae`f7dfe7e0 00000000`00000000 : 00000000`00000000 00000000`00000000 0000448a`028bfd30 0000448a`028bfd30 : chrome!ProfileImpl::~ProfileImpl+0x50

**CREDIT INFORMATION**  

Reporter credit: [Omri Bushari (Talon Cyber Security)]

## Attachments

- [b689c891-178f-488e-977b-52fd8c0d5f42.dmp](attachments/b689c891-178f-488e-977b-52fd8c0d5f42.dmp) (application/octet-stream, 1.3 MB)
- [chrome-browser-extensions-webstore_install_with_prompt.cc.patch](attachments/chrome-browser-extensions-webstore_install_with_prompt.cc.patch) (text/plain, 1.9 KB)
- [chrome-browser-extensions-webstore_install_with_prompt.h.patch](attachments/chrome-browser-extensions-webstore_install_with_prompt.h.patch) (text/plain, 1.4 KB)
- [chrome-browser-extensions-webstore_standalone_installer.cc.patch](attachments/chrome-browser-extensions-webstore_standalone_installer.cc.patch) (text/plain, 871 B)
- [05c36e4c-0201-45ef-91d0-4c59f68e2c8f.dmp](attachments/05c36e4c-0201-45ef-91d0-4c59f68e2c8f.dmp) (application/octet-stream, 1.4 MB)

## Timeline

### [Deleted User] (2022-08-08)

[Empty comment from Monorail migration]

### ma...@google.com (2022-08-08)

Thanks for the report. Extensions team, could you take a look at this one?

Tentatively marking this Severity-Medium. It's a browser process UAF, but mitigated by profile destruction, which also needs to be timed with an extension installation.

[Monorail components: Platform>Extensions]

### [Deleted User] (2022-08-08)

[Empty comment from Monorail migration]

### om...@talon-sec.com (2022-08-09)

Forgot to add Eran Rom (also from Talon Cyber Security) to the credit info. He assisted me in this issue.

### om...@talon-sec.com (2022-08-09)

I attach 2 more files:
1. There is another small patch to fix WebstoreStandaloneInstaller in case the 'callback_' member is empty (which is the case in WebstoreInstallWithPromptAppsOnly). No need to DCHECK as the class allow empty callbacks to be sent to the ctor.
2. During my attempts to initiate this bug, I started the browser as incognito:
"C:\Program Files\Google\Chrome\Application\chrome.exe" /install-chrome-app=gbkeegbaiigmenfmjfclcdgdpimamgkj -incognito
Then, while still downloading the extension, I opened a new window with other profile, and then closed the first (incognito) window. It resulted in a crash, probably because of the CHECK in `~ProfileDestroyer`. I attach the dump.

### [Deleted User] (2022-08-09)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-09)

[Empty comment from Monorail migration]

### rd...@chromium.org (2022-08-18)

Thank you for the report!

Dave, I think you've tackled a few issues like this - do you have the bandwidth to take this one on?

### [Deleted User] (2022-08-23)

dbertoni: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### db...@chromium.org (2022-09-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/00d6470762a2779ff156f66e6b3b96bf9f33245a

commit 00d6470762a2779ff156f66e6b3b96bf9f33245a
Author: David Bertoni <dbertoni@chromium.org>
Date: Wed Sep 14 18:55:08 2022

[Extensions] Fix a UAF in WebstoreStandaloneInstaller.

This CL adds code to observer the lifetime of the Profile and abort the
install if the Profile is being destroyed.

Bug: 1351177
Change-Id: Idde8e633dc2c5385f21e281e73f7723fbc8f5a8d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3872256
Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org>
Commit-Queue: David Bertoni <dbertoni@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1047035}

[modify] https://crrev.com/00d6470762a2779ff156f66e6b3b96bf9f33245a/chrome/browser/extensions/webstore_standalone_installer.h
[modify] https://crrev.com/00d6470762a2779ff156f66e6b3b96bf9f33245a/chrome/browser/extensions/webstore_standalone_installer.cc


### db...@chromium.org (2022-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-15)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-30)

Congratulations, Omri! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated [1] security bug. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

[1] https://g.co/chrome/vrp 


### am...@google.com (2022-10-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1351177?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060531)*
