# Security: UAF in mojo::SimpleWatcher::Context in MojoIpcz feature (browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061250](https://issues.chromium.org/issues/40061250) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2022-10-06 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in mojo::SimpleWatcher::Context in MojoIpcz feature in browser process

**VERSION**  

Chromium 108.0.5342.0 (Developer Build) (64-bit)  

Revision 01282ba43df30470536db4577ff77f8c89478f46-refs/heads/main@{#1055199}  

OS Linux

**REPRODUCTION CASE**

1. put the manifest.json&background.js in the extension dir && put the close.html in the webserver dir with port 80
2. run the command:  
   
   ./chrome --user-data-dir=any --enable-features=MojoIpcz --no-sandbox --load-extension="extension\_path"

PS:  

The success rate of reproduction of this isuue is relatively low  

The success rate is about 1/50

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

See the asan.log

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 1.4 KB)
- [background.js](attachments/background.js) (text/plain, 2.2 KB)
- [close.html](attachments/close.html) (text/plain, 96 B)
- [asan.log](attachments/asan.log) (text/plain, 26.4 KB)
- [issue_reproduce.py](attachments/issue_reproduce.py) (text/plain, 1.3 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 1.4 KB)
- [background.js](attachments/background.js) (text/plain, 2.1 KB)
- [close.html](attachments/close.html) (text/plain, 99 B)
- [asan1.log](attachments/asan1.log) (text/plain, 27.4 KB)
- [asan2.log](attachments/asan2.log) (text/plain, 25.7 KB)
- [asan3.log](attachments/asan3.log) (text/plain, 25.6 KB)
- [asan4.log](attachments/asan4.log) (text/plain, 40.9 KB)
- [asan5.log](attachments/asan5.log) (text/plain, 37.3 KB)

## Timeline

### [Deleted User] (2022-10-06)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-06)

CCing dcheng@ to get their eyes on this.
Haven't tried reproducing given the success rate called out by reporter (1/50) and the already-provided asan.log for review.

[Monorail components: Internals>Mojo]

### an...@chromium.org (2022-10-07)

CCing ajgo@ as well for their take.

### aj...@chromium.org (2022-10-07)

Looks like a valid uaf - 0xasnine - it seems to involve url loaders - perhaps you could try to make a poc that targets those to increase reliability?

However the U is in ipcz/mojo code so this might well be an ipcz lifetime bug. -> rockot (I'll try to repro in the meantime).

Ipcz is not launched yet so Impact=None - Severity = High as this is a uaf in the browser and the poc is simply what is needed to send the appropriate messages from a compromised renderer.

### an...@chromium.org (2022-10-07)

@ajgo - thanks for triaging!

### 0x...@gmail.com (2022-10-09)

This issue can also been triggered in chromiumOS(Linux)
When I test this issue, I fount that the same poc will cause different stacks.
This issue cannot trigger stably ,so I write a python script to reproduce this issue.

1. put the close.html in the webserver with 80 port
2. download the latest linux_asan_build(gsutil cp gs://chromium-browser-asan/linux-release/asan-linux-release-1056747.zip) and unzip it
3. put the manifest.json && background.js into extension dir.
4. Fill the linux_asan_build_dir and extension_path values in the python script.
5. Run the script in linux and wait for the crash~

Sometimes it needs hundreds of tests ,so wait for a little long time if it doesn't crash。

### ro...@google.com (2022-10-10)

This seems very likely to be a side effect of a known issue where SimpleWatcher doesn't make the same dispatch decision in certain scenarios (either posting a task or dispatching immediately) with MojoIpcz enabled vs disabled.

In some cases where we would normally post a task, we're now dispatching immediately and reentering code which is unsafe for reentrancy.

Fixing this is WIP.

### ro...@google.com (2022-10-10)

Actually, got some wires crossed there. Reentrancy is no longer a problem, and I think this UAF is due to incorrect ref counting on the trap event context.

### ro...@google.com (2022-10-10)

[Empty comment from Monorail migration]

### ro...@google.com (2022-10-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7aa3e148916f1f4dfcd1d5a2bc225740102d8dbf

commit 7aa3e148916f1f4dfcd1d5a2bc225740102d8dbf
Author: Ken Rockot <rockot@google.com>
Date: Tue Oct 11 23:39:20 2022

MojoIpcz: Fix race in trap event dispatch

Mojo specifies that events emitted by a trap are mutually exclusive and
that the CANCELLED (i.e. removal) event for a trigger will always be the
last event fired for that trigger.

The MojoIpcz MojoTrap implementation can violate these constraints since
multiple threads may dispatch unrelated events for the same trigger
concurrently. This can lead to crashes when e.g. a CANCELLED event is
fired at the same time as some other type of event, since the latter
event is allowed to make assumptions about lifetime that hold true as
long as a CANCELLED event for the same trigger has not already fired.

This fixes MojoIpcz behavior by maintaining an event queue in each
trap and ensuring that only one thread dispatches events for the
trap at any given time. This also ensures that no events are queued
for a trigger after its removal event.

LOW_COVERAGE_REASON=Coverage requires MojoIpcz to be enabled at
runtime, which will soon be the default testing config.

Fixed: 1371860
Change-Id: Icaa0408ad058390dc0ca53992fba56575d492320
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3943948
Reviewed-by: Alex Gough <ajgo@chromium.org>
Commit-Queue: Alex Gough <ajgo@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Cr-Commit-Position: refs/heads/main@{#1057777}

[modify] https://crrev.com/7aa3e148916f1f4dfcd1d5a2bc225740102d8dbf/mojo/core/ipcz_driver/mojo_trap.cc
[modify] https://crrev.com/7aa3e148916f1f4dfcd1d5a2bc225740102d8dbf/mojo/core/trap_unittest.cc
[modify] https://crrev.com/7aa3e148916f1f4dfcd1d5a2bc225740102d8dbf/mojo/public/cpp/bindings/tests/receiver_unittest.cc
[modify] https://crrev.com/7aa3e148916f1f4dfcd1d5a2bc225740102d8dbf/mojo/public/cpp/bindings/tests/receiver_unittest.test-mojom
[modify] https://crrev.com/7aa3e148916f1f4dfcd1d5a2bc225740102d8dbf/mojo/core/ipcz_driver/mojo_trap.h


### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-20)

[Comment Deleted]

### am...@chromium.org (2022-10-20)

Congratulations, asnine --interesting finding! The VRP Panel has decided to award you $20,000 for this report! Thank you for your efforts in discovering and reporting this issue to us - nice work! 

### am...@chromium.org (2022-10-24)

For some reason the automation didn't update this issue, reward info was sent to finance for processing on Thursday, 10/20

### [Deleted User] (2023-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-01-18)

This issue was migrated from crbug.com/chromium/1371860?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1299283]
[Monorail mergedwith: crbug.com/chromium/1371912]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061250)*
