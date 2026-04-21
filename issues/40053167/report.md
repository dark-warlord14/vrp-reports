# Security: HeapOverflow in SerialHandle

| Field | Value |
|-------|-------|
| **Issue ID** | [40053167](https://issues.chromium.org/issues/40053167) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Services>Device |
| **Platforms** | Linux, Mac, ChromeOS |
| **Reporter** | le...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2020-08-26 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

|StartWriting|[1] could be called before the SerialPort is opened via IPC. The pending-check will be done in |OnFileCanWriteWithoutBlocking|[2]. But before that, the illegal fd(-1) could be passed into |WatchWritable|[3]. Eventually cause heap overflow at [4].

```
	...  
   
	evep = &epollop->fds[fd];  //<<<--------------  
	op = EPOLL_CTL_ADD;  
	events = 0;  
	if (evep->evread != NULL) {  
		events |= EPOLLIN;  
		op = EPOLL_CTL_MOD;  
	}  
	if (evep->evwrite != NULL) {  
		events |= EPOLLOUT;  
		op = EPOLL_CTL_MOD;  
	}  
	...  
   
	if (ev->ev_events & EV_READ)  
		evep->evread = ev;  
	if (ev->ev_events & EV_WRITE)  
		evep->evwrite = ev;  

```

[1]. <https://source.chromium.org/chromium/chromium/src/+/master:services/device/public/mojom/serial.mojom;l=167;drc=97254d4f8844ae362125e62aee4b209c5fc67534;bpv=1;bpt=0?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

[2]. <https://source.chromium.org/chromium/chromium/src/+/master:services/device/serial/serial_io_handler_posix.cc;l=373;drc=4a991b979bb82defc403bba68c87405bf01ea70c;bpv=1;bpt=0?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

[3]. <https://source.chromium.org/chromium/chromium/src/+/master:services/device/serial/serial_io_handler_posix.cc;l=410;drc=4a991b979bb82defc403bba68c87405bf01ea70c;bpv=1;bpt=0?originalUrl=https:%2F%2Fcs.chromium.org%2F>  

[4]. <https://source.chromium.org/chromium/chromium/src/+/master:base/third_party/libevent/epoll.c;l=280;drc=c7ebe6daa79da2e351345065020cc7f216126f15;bpv=1;bpt=0?originalUrl=https:%2F%2Fcs.chromium.org%2F>

**VERSION**  

Chrome Version: M85 stable  

Operating System: Linux

**REPRODUCTION CASE**

1. Apply the attached token.patch( \* ).
2. $ python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/asan/gen  
   
   $ python -m SimpleHTTPServer
   
   $ out/asan/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/xxxx "<http://localhost:8000/poc.html>"
3. Select any serial device and click the triggerButton.

\* ps: Similar to <https://bugs.chromium.org/p/chromium/issues/detail?id=998548>, the token.patch aims to solve a javascript bug in the mojo API mojoBinding.js, it has nothing to do with the vulnerability itself. This can be fixed from the renderer side or by using the cpp API.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see asan file

**CREDIT INFORMATION**  

Reporter credit: Leecraso and Guang Gong of 360 Alpha Lab working with 360 BugCloud

## Attachments

- [asan](attachments/asan) (text/plain, 15.3 KB)
- [token.patch](attachments/token.patch) (text/plain, 679 B)
- [poc.html](attachments/poc.html) (text/plain, 1.0 KB)

## Timeline

### ts...@chromium.org (2020-08-26)

reillyg - could you take a look? It looks like you've done some work in the past in this area with closed fds, or feel free to re-assign as appropriate. Thanks!

[Monorail components: Internals>Services>Device]

### [Deleted User] (2020-08-26)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-26)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2020-09-03)

reillyg: Friendly ping. This is a high-severity vulnerability affecting stable.

### re...@chromium.org (2020-09-03)

Sorry, I haven't been able to get to this because of Perf. I will have a fix today.

### re...@chromium.org (2020-09-03)

A fix is out for review: https://chromium-review.googlesource.com/c/chromium/src/+/2393001

I have a more holistic fix planned as part of resolving https://crbug.com/chromium/1121774 but this is the minimal mergeable version.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/adc731d678c4c795e7c4c74133a624310e7bc9ae

commit adc731d678c4c795e7c4c74133a624310e7bc9ae
Author: Reilly Grant <reillyg@chromium.org>
Date: Tue Sep 08 19:29:40 2020

serial: Check that port is open before reading or writing

This change adds checks to the platform-specific implementations
of Read() and Write() to make sure that the file descriptor is
valid before. This makes the assumptions validated by later DCHECK
correct.

This cannot be done in the platform-independent layer because test
code depends on being able to call some SerialIoHandler methods
without an actual file descriptor.

Bug: 1121836
Change-Id: If182404cf10a2f3b445b9c80b75fed5df6b5ab4b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2393001
Reviewed-by: James Hollyer <jameshollyer@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/heads/master@{#805016}

[modify] https://crrev.com/adc731d678c4c795e7c4c74133a624310e7bc9ae/services/device/serial/serial_io_handler_posix.cc
[modify] https://crrev.com/adc731d678c4c795e7c4c74133a624310e7bc9ae/services/device/serial/serial_io_handler_win.cc
[modify] https://crrev.com/adc731d678c4c795e7c4c74133a624310e7bc9ae/services/device/serial/serial_port_impl_unittest.cc


### re...@chromium.org (2020-09-08)

Marking this issue fixed. I will request a merge to M-86 after validating the fix is stable on canary-channel tomorrow.

tsepez@, do you think this should be merged to M-86?

### [Deleted User] (2020-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-09)

Requesting merge to stable M85 because latest trunk commit (805016) appears to be after stable branch point (782793).

Requesting merge to beta M86 because latest trunk commit (805016) appears to be after beta branch point (800218).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-09-09)

This bug requires manual review: M86's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### re...@chromium.org (2020-09-09)

1. Does your merge fit within the Merge Decision Guidelines?
Yes.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2393001

3. Has the change landed and been verified on master/ToT?
Yes, I have validated the change on macOS and Windows with Chrome Canary.

4. Why are these changes required in this milestone after branch?
This is a Security_Severity-High issue which affects the M-86 branch. 

5. Is this a new feature?
No.

6. If it is a new feature, is it behind a flag using finch?
N/A

### sr...@google.com (2020-09-09)

reillyg@ does this need to be merged to M85 now? or can this wait for M86 


+adetaylor@

### re...@chromium.org (2020-09-10)

According to the severity guidelines[1] a high-severity issue this should be merged into the current stable milestone.

[1] https://chromium.googlesource.com/chromium/src/+/master/docs/security/severity-guidelines.md

### ad...@chromium.org (2020-09-10)

Yes, I think this is sufficiently simple that we should follow the merge guidelines as normal. Approving merge to M86 (branch 4240) and M85 (branch 4183). We'll likely release this with the final M85 stable security refresh in about 10 days.

reillyg@ please wait for a day of canary coverage before merging anywhere.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e07e479165fc1237e42c755a9f77585affa5bf24

commit e07e479165fc1237e42c755a9f77585affa5bf24
Author: Reilly Grant <reillyg@chromium.org>
Date: Fri Sep 11 23:28:19 2020

serial: Check that port is open before reading or writing

This change adds checks to the platform-specific implementations
of Read() and Write() to make sure that the file descriptor is
valid before. This makes the assumptions validated by later DCHECK
correct.

This cannot be done in the platform-independent layer because test
code depends on being able to call some SerialIoHandler methods
without an actual file descriptor.

(cherry picked from commit adc731d678c4c795e7c4c74133a624310e7bc9ae)

Bug: 1121836
Change-Id: If182404cf10a2f3b445b9c80b75fed5df6b5ab4b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2393001
Reviewed-by: James Hollyer <jameshollyer@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#805016}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2406664
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#632}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/e07e479165fc1237e42c755a9f77585affa5bf24/services/device/serial/serial_io_handler_posix.cc
[modify] https://crrev.com/e07e479165fc1237e42c755a9f77585affa5bf24/services/device/serial/serial_io_handler_win.cc
[modify] https://crrev.com/e07e479165fc1237e42c755a9f77585affa5bf24/services/device/serial/serial_port_impl_unittest.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/21069131d16de0a2e649cf0cb38860f1bbc8ccff

commit 21069131d16de0a2e649cf0cb38860f1bbc8ccff
Author: Reilly Grant <reillyg@chromium.org>
Date: Sat Sep 12 02:30:46 2020

serial: Check that port is open before reading or writing

This change adds checks to the platform-specific implementations
of Read() and Write() to make sure that the file descriptor is
valid before. This makes the assumptions validated by later DCHECK
correct.

This cannot be done in the platform-independent layer because test
code depends on being able to call some SerialIoHandler methods
without an actual file descriptor.

(cherry picked from commit adc731d678c4c795e7c4c74133a624310e7bc9ae)

(cherry picked from commit e07e479165fc1237e42c755a9f77585affa5bf24)

Bug: 1121836
Change-Id: If182404cf10a2f3b445b9c80b75fed5df6b5ab4b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2393001
Reviewed-by: James Hollyer <jameshollyer@chromium.org>
Commit-Queue: Reilly Grant <reillyg@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#805016}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2406664
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4240@{#632}
Cr-Original-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2406151
Cr-Commit-Position: refs/branch-heads/4183@{#1813}
Cr-Branched-From: 740e9e8a40505392ba5c8e022a8024b3d018ca65-refs/heads/master@{#782793}

[modify] https://crrev.com/21069131d16de0a2e649cf0cb38860f1bbc8ccff/services/device/serial/serial_io_handler_posix.cc
[modify] https://crrev.com/21069131d16de0a2e649cf0cb38860f1bbc8ccff/services/device/serial/serial_io_handler_win.cc
[modify] https://crrev.com/21069131d16de0a2e649cf0cb38860f1bbc8ccff/services/device/serial/serial_port_impl_unittest.cc


### ad...@google.com (2020-09-14)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-16)

Congratulations! The VRP panel has decided to award $10,000 for this report.


### ad...@google.com (2020-09-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-24)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-09-29)

reillyg@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1121836?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053167)*
