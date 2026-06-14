# Security: MidiHostMsg_SendData vector OOB on Android

| Field | Value |
|-------|-------|
| **Issue ID** | [40081367](https://issues.chromium.org/issues/40081367) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Android |
| **CVE IDs** | CVE-2015-1232 |
| **Reporter** | gz...@gmail.com |
| **Assignee** | yh...@chromium.org |
| **Created** | 2015-02-07 |
| **Bounty** | $7,500.00 |

## Description

MidiHostMsg\_SendData is handled in content/browser/media/midi\_host.cc:90:  

void MidiHost::OnSendData(uint32 port,  

...  

midi\_manager\_->DispatchSendMidiData(this, port, data, timestamp);

MidiManager implementation on Android at media/midi/midi\_manager\_usb.cc:42 does:  

void MidiManagerUsb::DispatchSendMidiData(MidiManagerClient\* client,  

uint32\_t port\_index,  

...  

DCHECK\_LT(port\_index, output\_streams\_.size());  

output\_streams\_[port\_index]->Send(data);

Where output\_streams\_ is a ScopedVector<UsbMidiOutputStream>. port\_index is controlled by a compromised renderer and is only validated by a DCHECK. Only the Android implementation of MidiManager lacks validation. Other platforms seem to be good.

**VERSION**  

Chrome Version: M40 stable, M41 beta  

Operating System: Android

**REPRODUCTION CASE**  

From the renderer:  

Send(new MidiHostMsg\_SendData(0x41414141 >> 2, data, 0));

PoC renderer patch is attached. Build Android Release content shell and run. I tested it with ToT 598c3e9b0e.

## Attachments

- [midi_poc.patch](attachments/midi_poc.patch) (application/octet-stream, 916 B)
- [crash.txt](attachments/crash.txt) (text/plain, 1.0 KB)

## Timeline

### in...@chromium.org (2015-02-08)

Very nice catch!

Marty, can you please see if we can reproduce this. 

### in...@chromium.org (2015-02-08)

Marty, ignore c#1. We will let the dev handle this.

### js...@chromium.org (2015-02-08)

Looks like yhirano introduced the vulnerability about a week ago, here: https://chromium.googlesource.com/chromium/src/+/a2a4a77c398d65391bd3f46ac90ce79718cf3823

Should be an easy fix of converting it from a DCHECK to a normal failure.

### gz...@gmail.com (2015-02-08)

#3: Introduced in 2014 actually. A year ago.

### cl...@chromium.org (2015-02-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-08)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### bu...@chromium.org (2015-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5576cbc1d3e214dfbb5d3ffcdbe82aa8ba0088fc

commit 5576cbc1d3e214dfbb5d3ffcdbe82aa8ba0088fc
Author: yhirano <yhirano@chromium.org>
Date: Mon Feb 09 15:13:28 2015

MidiManagerUsb should not trust indices provided by renderer.

MidiManagerUsb::DispatchSendMidiData takes |port_index| parameter. As it is
provided by a renderer possibly under the control of an attacker, we must
validate the given index before using it.

BUG=456516

Review URL: https://codereview.chromium.org/907793002

Cr-Commit-Position: refs/heads/master@{#315303}

[modify] http://crrev.com/5576cbc1d3e214dfbb5d3ffcdbe82aa8ba0088fc/media/midi/midi_manager_usb.cc
[modify] http://crrev.com/5576cbc1d3e214dfbb5d3ffcdbe82aa8ba0088fc/media/midi/midi_manager_usb_unittest.cc


### yh...@chromium.org (2015-02-10)

Request merge for beta

### yh...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### pe...@google.com (2015-02-10)

Approved for M41 (branch: 2272)

### pe...@google.com (2015-02-10)

[Automated comment] Commit may have occurred before M42 branch point (2/21/2015), needs manual review.

### cl...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### pe...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9a67a2f028353884c5a0d11a7dc13f08da52d8a2

commit 9a67a2f028353884c5a0d11a7dc13f08da52d8a2
Author: Yutaka Hirano <yhirano@chromium.org>
Date: Thu Feb 12 03:53:45 2015

MidiManagerUsb should not trust indices provided by renderer.

MidiManagerUsb::DispatchSendMidiData takes |port_index| parameter. As it is
provided by a renderer possibly under the control of an attacker, we must
validate the given index before using it.

BUG=456516

Review URL: https://codereview.chromium.org/907793002

Cr-Commit-Position: refs/heads/master@{#315303}
(cherry picked from commit 5576cbc1d3e214dfbb5d3ffcdbe82aa8ba0088fc)
TBR=toyoshim@chromium.org

Review URL: https://codereview.chromium.org/916223003

Cr-Commit-Position: refs/branch-heads/2272@{#277}
Cr-Branched-From: 827a380cfdb31aa54c8d56e63ce2c3fd8c3ba4d4-refs/heads/master@{#310958}

[modify] http://crrev.com/9a67a2f028353884c5a0d11a7dc13f08da52d8a2/media/midi/midi_manager_usb.cc
[modify] http://crrev.com/9a67a2f028353884c5a0d11a7dc13f08da52d8a2/media/midi/midi_manager_usb_unittest.cc


### gz...@gmail.com (2015-02-13)

Not sure if it was clear, but this also impacts stable. Security_Impact-Stable label is missing.

### in...@chromium.org (2015-02-13)

Thanks!

### yh...@chromium.org (2015-02-16)

[Empty comment from Monorail migration]

### pe...@google.com (2015-02-16)

[Automated comment] Request affecting a post-stable build (M40), manual review required.

### yh...@chromium.org (2015-02-17)

[Empty comment from Monorail migration]

### ma...@google.com (2015-02-17)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-23)

pennymac: unless there's a revert somewhere here, this looks like it is already in branch 2272. If you concur, let's remove the merge-review tags and consider this done.

### pe...@chromium.org (2015-02-23)

[Empty comment from Monorail migration]

### ti...@google.com (2015-02-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-03)

Congratulations - $7,500 for what appears to be your first report to us :)

Notes from reward panel: Great high-quality report! For reference, the $10,000 level is for when you can demonstrate in your report good control of EIP or similarly powerful register.

I'll credit you in the release notes as "gzobqq" - let me know if you'd like to use a different name.

A CVE will also be assigned to this bug for your reference. Someone from our finance team will get in contact with you in the next two weeks collect details to arrange payment. Please update this bug or contact me directly if that doesn't happen.

### ti...@google.com (2015-03-03)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-08)

Updating CVE (we had a duplicate on this end). New CVE is CVE-2015-1232.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-03-17)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-05-19)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/456516?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081367)*
