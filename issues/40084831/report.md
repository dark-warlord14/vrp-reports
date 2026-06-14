# Use-after-poison in content::WebMessagePortChannelImpl::OnMessage

| Field | Value |
|-------|-------|
| **Issue ID** | [40084831](https://issues.chromium.org/issues/40084831) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Core |
| **Platforms** | Mac |
| **Reporter** | at...@gmail.com |
| **Assignee** | tz...@chromium.org |
| **Created** | 2016-07-12 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5079226818756608

Fuzzer: attekett_dom_fuzzer
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ee7424e1d68
Crash State:
  content::WebMessagePortChannelImpl::OnMessage
  bool IPC::MessageT<MessagePortMsg_Message_Meta, std::__1::tuple<std::__1::basic_
  content::WebMessagePortChannelImpl::OnMessageReceived
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=392926:392933

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96jrf3RIR9LqAc_J9K8VSb1ybgozqvCm3hSn2HHg4ojZgGVcxJAqrtrooRfzS5yYtKRXbmKa9Ug5Uy_ChkY6YO5Xfv7yv-Ikmk2WsVx7sMoL4wWwH33Ki3Fx7vNZKRM17uOX7s9heLNMH750a3B8SJDV1u3E_h7YEo1n1ELPv4TiugMEx4?testcase_id=5079226818756608


Filer: mmoroz

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### mm...@chromium.org (2016-07-12)

tzik@, could you please take a look or suggest another owner?

[Monorail components: Internals>Core]

### sh...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

[Comment Deleted]

### go...@chromium.org (2016-07-14)

A friendly reminder that M52 Stable is launching soon! Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and get it merged into the release branch by July 15, 5:00 PM PST in order to make into the desktop Stable final build cut. Thank you!

### go...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f7dbf39be31d8aa9214d5d84da613508d4e06491

commit f7dbf39be31d8aa9214d5d84da613508d4e06491
Author: tzik <tzik@chromium.org>
Date: Thu Jul 14 08:23:49 2016

Delay client registration of MessagePort to MessagePortChannel

MessagePort used to be registered to MessagePortChannel on entangle(),
and be unregisted when the ExecutionContext is stopped or MessagePort
is swept by GC. Once its start() is called, its hasPendingActivity()
will be true and that extends the MessagePort lifetime to stop() or close() call.

However, there's a time gap between the MessagePort instance is marked
as unreachable, and swept by GC system. If MessagePortChannel accesses
the MessagePort in this period, that causes use-after-poison crash.

I.e. there are two pattern of the life of MessagePort.
 1. entangle() + register -> gets unreachable -(poisoned period)-> swept + unregister
 2. entangle() + register -> start() -> stop() + unregister
 3. entangle() + register -> start() -> close() + unregister

(2) and (3) cases are OK, while (1) has a dangerous period.
This CL delays the registration from entangle() to start(), so that
the case (1) doesn't register the MessagePort to MessagePortChannel at all.

BUG=627457

Review-Url: https://codereview.chromium.org/2143003003
Cr-Commit-Position: refs/heads/master@{#405450}

[modify] https://crrev.com/f7dbf39be31d8aa9214d5d84da613508d4e06491/third_party/WebKit/Source/core/dom/MessagePort.cpp


### tz...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-14)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2016-07-14)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### cl...@chromium.org (2016-07-14)

ClusterFuzz has detected this issue as fixed in range 405185:405467.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5079226818756608

Fuzzer: attekett_dom_fuzzer
Job Type: mac_asan_chrome
Platform Id: mac

Crash Type: Use-after-poison READ 8
Crash Address: 0x7ee7424e1d68
Crash State:
  content::WebMessagePortChannelImpl::OnMessage
  bool IPC::MessageT<MessagePortMsg_Message_Meta, std::__1::tuple<std::__1::basic_
  content::WebMessagePortChannelImpl::OnMessageReceived
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=392926:392933
Fixed: https://cluster-fuzz.appspot.com/revisions?job=mac_asan_chrome&range=405185:405467

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96jrf3RIR9LqAc_J9K8VSb1ybgozqvCm3hSn2HHg4ojZgGVcxJAqrtrooRfzS5yYtKRXbmKa9Ug5Uy_ChkY6YO5Xfv7yv-Ikmk2WsVx7sMoL4wWwH33Ki3Fx7vNZKRM17uOX7s9heLNMH750a3B8SJDV1u3E_h7YEo1n1ELPv4TiugMEx4?testcase_id=5079226818756608


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2016-07-15)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-15)

+ awhalley@ to confirm once it is baked in canary whether it is ok to take this merge in for M52 stable release next week or wait until next stable release  (This is M52 stable blocker bug).

### aw...@chromium.org (2016-07-18)

Looks good to merge to M52.

### go...@chromium.org (2016-07-18)

Approving merge to M52 branch 2743 based on https://crbug.com/chromium/627457#c15. Please merge ASAP before 5:00 PM PST today (Monday) as we're cutting M52 Stable RC today and this bug is marked as M52 Stable blocker. Thank you.

Also does this require a merge to M53?

### bu...@chromium.org (2016-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/575679ba79b22c21a6b2d58c42b1412cbf58e481

commit 575679ba79b22c21a6b2d58c42b1412cbf58e481
Author: Taiju Tsuiki <tzik@google.com>
Date: Mon Jul 18 17:56:43 2016

Delay client registration of MessagePort to MessagePortChannel

MessagePort used to be registered to MessagePortChannel on entangle(),
and be unregisted when the ExecutionContext is stopped or MessagePort
is swept by GC. Once its start() is called, its hasPendingActivity()
will be true and that extends the MessagePort lifetime to stop() or close() call.

However, there's a time gap between the MessagePort instance is marked
as unreachable, and swept by GC system. If MessagePortChannel accesses
the MessagePort in this period, that causes use-after-poison crash.

I.e. there are two pattern of the life of MessagePort.
 1. entangle() + register -> gets unreachable -(poisoned period)-> swept + unregister
 2. entangle() + register -> start() -> stop() + unregister
 3. entangle() + register -> start() -> close() + unregister

(2) and (3) cases are OK, while (1) has a dangerous period.
This CL delays the registration from entangle() to start(), so that
the case (1) doesn't register the MessagePort to MessagePortChannel at all.

BUG=627457

Review-Url: https://codereview.chromium.org/2143003003
Cr-Commit-Position: refs/heads/master@{#405450}
(cherry picked from commit f7dbf39be31d8aa9214d5d84da613508d4e06491)

Review URL: https://codereview.chromium.org/2156293002 .

Cr-Commit-Position: refs/branch-heads/2743@{#663}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/575679ba79b22c21a6b2d58c42b1412cbf58e481/third_party/WebKit/Source/core/dom/MessagePort.cpp


### tz...@chromium.org (2016-07-18)

Yes, M53 requires this fix too.

### go...@chromium.org (2016-07-18)

Approving merge to M53 branch 2785 based on https://crbug.com/chromium/627457#c15. Please try to merge this before 5:00 PM PST today in order to make it to tomorrow's M53 Dev release. Thank you.

### bu...@chromium.org (2016-07-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7b600704b01eb15d7cce4e30a6c8d4c2a1645673

commit 7b600704b01eb15d7cce4e30a6c8d4c2a1645673
Author: Taiju Tsuiki <tzik@google.com>
Date: Mon Jul 18 18:14:03 2016

Delay client registration of MessagePort to MessagePortChannel

MessagePort used to be registered to MessagePortChannel on entangle(),
and be unregisted when the ExecutionContext is stopped or MessagePort
is swept by GC. Once its start() is called, its hasPendingActivity()
will be true and that extends the MessagePort lifetime to stop() or close() call.

However, there's a time gap between the MessagePort instance is marked
as unreachable, and swept by GC system. If MessagePortChannel accesses
the MessagePort in this period, that causes use-after-poison crash.

I.e. there are two pattern of the life of MessagePort.
 1. entangle() + register -> gets unreachable -(poisoned period)-> swept + unregister
 2. entangle() + register -> start() -> stop() + unregister
 3. entangle() + register -> start() -> close() + unregister

(2) and (3) cases are OK, while (1) has a dangerous period.
This CL delays the registration from entangle() to start(), so that
the case (1) doesn't register the MessagePort to MessagePortChannel at all.

BUG=627457

Review-Url: https://codereview.chromium.org/2143003003
Cr-Commit-Position: refs/heads/master@{#405450}
(cherry picked from commit f7dbf39be31d8aa9214d5d84da613508d4e06491)

Review URL: https://codereview.chromium.org/2154263003 .

Cr-Commit-Position: refs/branch-heads/2785@{#186}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/7b600704b01eb15d7cce4e30a6c8d4c2a1645673/third_party/WebKit/Source/core/dom/MessagePort.cpp


### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

And $3,500 for this one.  Thanks as ever for a great fuzzer!

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-10-20)

This issue was migrated from crbug.com/chromium/627457?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084831)*
