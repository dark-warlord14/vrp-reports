# UaF in BluetoothAdapter::OnDiscoveryChangeComplete

| Field | Value |
|-------|-------|
| **Issue ID** | [40050691](https://issues.chromium.org/issues/40050691) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Bluetooth |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | if...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2019-11-15 |
| **Bounty** | $20,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36

Steps to reproduce the problem:
1. python copy_binding.py /path/to/out/gen
2. copy /path/to/poc.html ./
3. python3 -m http.server

Then use the chromium with asan open 
./chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/noexist http://localhost:8000/poc.html

What is the expected behavior?

What went wrong?
Adapter object use after free.
Details in asan log.

Did this work before? N/A 

Chrome version: 78.0.3904.87  Channel: stable
OS Version: OS X 10.15.1
Flash Version: 

I have test it on the master branch's newest commit, in the stable channel, if I reset the ptr after scanning complete, another oob will trigger, but it has been patched in the latest commit, https://cs.chromium.org/chromium/src/content/browser/bluetooth/web_bluetooth_service_impl.cc?q=bluetooth_service_impl&sq=package:chromium&g=0&l=11&dlp=chromium&dlf=src/content/browser/bluetooth/web_bluetooth_service_impl.cc&dlc=a255d1be5723813c1a3e793b8388ed61edcea5b1&dlr=81&dlgp=content/browser/bluetooth/web_bluetooth_service_impl.cc&dlgr=chromium/chromium/src&drp=chromium&drf=src/content/browser/bluetooth/web_bluetooth_service_impl.cc&drc=405c014642cc7aea722206149b767d7ef6611b9f&drr=82&drgp=content/browser/bluetooth/web_bluetooth_service_impl.cc&drgr=chromium/chromium/src

## Attachments

- [asan_log.txt](attachments/asan_log.txt) (text/plain, 27.0 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.2 KB)
- [copy_binding.py](attachments/copy_binding.py) (text/plain, 530 B)
- [test.html](attachments/test.html) (text/plain, 233 B)
- [test1.html](attachments/test1.html) (text/plain, 151 B)

## Timeline

### if...@gmail.com (2019-11-15)

copy_binding.py here.

### wf...@chromium.org (2019-11-15)

[Empty comment from Monorail migration]

[Monorail components: Blink>Bluetooth]

### sh...@chromium.org (2019-11-15)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### od...@chromium.org (2019-11-15)

Thank you for filing this bug. I'll take a look since I fixed the other OOB access bug.

### re...@chromium.org (2019-11-15)

This looks like the usual case of callbacks causing |this| to be destroyed while iterating over a member variable. The workaround is usually to move the callbacks into a local variable and, if there are steps that need to be performed after the loop completes, add a WeakPtr to this that can be checked after the loop exits.

We should audit all other callback invocation sites in this file to make sure there aren't other instances of this pattern.

Adding jameshollyer@ for visibility since I believe it was the DiscoverySession refactoring that introduced this loop.

### od...@chromium.org (2019-11-15)

I'm actually reassigning this to James. Thank you James for being able to take this bug.

### if...@gmail.com (2019-11-17)

In fact this bug could be triggered if the #enable-experimental-web-platform-features is enabled, here is another poc in attachments.
Open the test1.html and click the trigger button, you can see the similar asan report.



### if...@gmail.com (2019-11-18)

Oh, I suddenly find that I don't need to enable #enable-experimental-web-platform-features flag in Windows and MacOS, so may be the severity could be critical? Sorry for spam...

### ad...@google.com (2019-11-18)

Bumping to Critical on the basis of https://crbug.com/chromium/1025067#c8.

### sh...@chromium.org (2019-11-18)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-18)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2019-11-18)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-11-18)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-18)

+ Security TPM & Manager

### sr...@google.com (2019-11-18)

adding RBS and removing RBB as M-78 is already in 100% stable. 

+adetaylor@ . looks like the fixes we did last friday exposed this new issue in M78. Pls review. 

### ad...@google.com (2019-11-18)

Actually, re-reading this, I think I jumped the gun when I marked it as Critical. It's "only" at the upper end of High severity, as it still (I believe) requires renderer compromise, MojoJS enablement or similar in order to achieve the sandbox escape.

In that sense it's the same (very high, but not quite critical) severity as the prior two Bluetooth bugs.

Re https://crbug.com/chromium/1025067#c15 - I am doubting that this is a regression from the fixes last week. This was reported on Thursday against 78.0.3904.87. It is *possible* that the changes made last week expose this in a different way, but the issue was pre-existing. I'm removing RBS on that basis.

### re...@chromium.org (2019-11-18)

I'm working on reproducing this issue so that I can get a sense of how easily it can be hit and will provide a fix.

### sr...@google.com (2019-11-18)

Per https://crbug.com/chromium/1025067#c16, removing RBB as this should not block beta release for M78 at this point.

### re...@chromium.org (2019-11-18)

Why does this issue have the OS-Windows and OS-Mac labels? The original report is an ASAN log from Linux. mmoroz@, have you reproduced this on Windows? I so far have failed to reproduce this on macOS.

### ad...@google.com (2019-11-18)

https://crbug.com/chromium/1025067#c8 says it reproduces on Windows and Mac. Feel free to add OS-Linux too. If you think this could (even theoretically) affect Android it would be very useful to add that checkbox too, so it goes into the right queues for the Android release TPMs.

### mm...@google.com (2019-11-18)

Yes, I've added Windows as per https://crbug.com/chromium/1025067#c8. Sorry I should've left an explicit comment. I haven't tried reproducing myself though.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b8ffd1e064d06e233301fc526306a0f61003bebb

commit b8ffd1e064d06e233301fc526306a0f61003bebb
Author: Reilly Grant <reillyg@chromium.org>
Date: Tue Nov 19 02:37:21 2019

[bluetooth] Handle adapter destruction during discovery callbacks

BluetoothAdapter::OnDiscoveryChangeComplete() needs to be able to handle
the case where a callback destroys the BluetoothAdapter.

This issue was not noticed in tests because TestBluetoothAdapter takes a
reference to the BluetoothAdapter when executing these callbacks. It
has been updated to use a WeakPtr as the real backends do.

I noticed that both BluetoothAdapter and nearly all of its subclasses
have a WeakPtrFactory. The factory in the base class has been removed
and subclasses are required to provide their own.

Bug: 1025067
Change-Id: I91f952e01fd3bda618455f294ce0cba2e2a7dad1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1922298
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Ovidio de Jesús Ruiz-Henríquez <odejesush@chromium.org>
Cr-Commit-Position: refs/heads/master@{#716465}

[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter.cc
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter.h
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter_android.cc
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter_android.h
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter_mac.h
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter_mac.mm
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter_unittest.cc
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter_win.cc
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter_win.h
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter_winrt.cc
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluetooth_adapter_winrt.h
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluez/bluetooth_adapter_bluez.cc
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/bluez/bluetooth_adapter_bluez.h
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/cast/bluetooth_adapter_cast.cc
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/cast/bluetooth_adapter_cast.h
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/test/fake_central.cc
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/test/fake_central.h
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/test/mock_bluetooth_adapter.cc
[modify] https://crrev.com/b8ffd1e064d06e233301fc526306a0f61003bebb/device/bluetooth/test/mock_bluetooth_adapter.h


### re...@chromium.org (2019-11-19)

I will verify this change in tomorrow's canary-channel build and request a merge to M-79.

### ad...@chromium.org (2019-11-19)

reillyg@ thanks! Please could you add a comment on the stability risk of the bug? There is talk of releasing this in an M78 stable update, but only if you think it is low risk.

### re...@chromium.org (2019-11-19)

The patch is a little big but I think this is will be safe to merge after verification.

### ad...@chromium.org (2019-11-19)

Thanks. Much appreciated.

### sh...@chromium.org (2019-11-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-20)

Requesting merge to stable M78 because latest trunk commit (716465) appears to be after stable branch point (693954).

Requesting merge to beta M79 because latest trunk commit (716465) appears to be after beta branch point (706915).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-20)

This bug requires manual review: M79's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-11-21)

How is the change looking in canary? Is it fully safe to merge to M79?

### re...@chromium.org (2019-11-22)

I've verified this change on Android canary and it looks good. This change looks safe to merge to M-79. I've verified that the patch applies cleanly.

### go...@chromium.org (2019-11-22)

Approving merge to M79 branch 3945 based on https://crbug.com/chromium/1025067#c31, please merge ASAP.  Thank you.

### go...@chromium.org (2019-11-22)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-22)

Please merge your change to M79 branch 3945 ASAP so we can pick it up for next M79 Beta release. Thank you.

### re...@chromium.org (2019-11-22)

Bugdroid continues to have trouble. This change was merged as https://chromium-review.googlesource.com/c/chromium/src/+/1930093.

### ad...@google.com (2019-11-26)

Adding Android per https://crbug.com/chromium/1025067#c31 and Linux based on earlier mention of Linux.

### na...@google.com (2019-12-02)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $20,000 for this report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### if...@gmail.com (2019-12-05)

Huge thanks! Credit goes to Gengming Liu, Jianyu Chen at Tencent Keen Security Lab

### ad...@chromium.org (2019-12-05)

This is going back up to Critical, because wfh@ has pointed out that the PoC in https://crbug.com/chromium/1025067#c7 does not require "--enable-blink-features=MojoJS" and therefore doesn't require a compromised renderer.

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-11)

reillyg@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ac...@chromium.org (2020-03-31)

Hello, I'm working on a project that needs to merge this CL (https://crrev.com/c/1922298) to M76. 

The CL has 2 parts - one where weak_ptr_factory is replaced, and the other is where we check if the object has been deleted in one of the callbacks_waiting_response_. The second part seems to have been introduced in Discovery Session callback refactor in https://crrev.com/c/1699214. Reilly, could you confirm please? Or did the version of bluetooth_adapter.cc prior to this also have the bug?

### re...@chromium.org (2020-03-31)

The changes around |callbacks_waiting_response_| were required because the OnDiscoveryChangeComplete() method needs to access |this| after running a callback. Before the refactor I don't believe we had any cases of this which needed a check so it should be safe to only merge the CL from this issue.

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1025067?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050691)*
