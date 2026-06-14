# Security: Universal XSS using Flash message loop

| Field | Value |
|-------|-------|
| **Issue ID** | [40083383](https://issues.chromium.org/issues/40083383) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Pepper |
| **CVE IDs** | CVE-2016-1631 |
| **Reporter** | ma...@gmail.com |
| **Assignee** | yz...@chromium.org |
| **Created** | 2015-12-14 |
| **Bounty** | $7,500.00 |

## Description

## **VULNERABILITY DETAILS** From /content/renderer/pepper/ppb\_flash\_message\_loop\_impl.cc:

## int32\_t PPB\_Flash\_MessageLoop\_Impl::InternalRun( const RunFromHostProxyCallback& callback) { (...) // It is possible that the PPB\_Flash\_MessageLoop\_Impl object has been // destroyed when the nested message loop exits. scoped\_refptr<State> state\_protector(state\_); { base::MessageLoop::ScopedNestableTaskAllower allow( base::MessageLoop::current()); base::MessageLoop::current()->Run(); } (...) }

|PPB\_Flash\_MessageLoop\_Impl::InternalRun| doesn't initialize a ScopedPageLoadDeferrer before spinning an event loop. As a result, cross-origin documents can be loaded at an arbitrary javascript execution point.

**VERSION**  

Chrome 47.0.2526.80 (Stable)  

Chrome 48.0.2564.41 (Beta)  

Chrome 49.0.2587.3 (Dev)  

Chromium 49.0.2591.0 + Pepper Flash (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/zip, 2.6 KB)
- [poc.zip](attachments/poc.zip) (application/zip, 3.7 KB)

## Timeline

### js...@chromium.org (2015-12-14)

natashenka@ - Would you mind verifying this report?

### na...@google.com (2015-12-14)

I tested the PoC and it works. This appears to be a Chrome issue as opposed to a Flash issue, so I did not report it to Adobe. 

### cl...@chromium.org (2015-12-14)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-12-16)

Okay, adding a few CCs to figure out who can own this and fix it.

### rs...@chromium.org (2015-12-20)

raymes: Can you please take a look at this issue?

### cl...@chromium.org (2015-12-29)

raymes@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ra...@chromium.org (2016-01-03)

I don't know much about this code or the exploit in question. 

yzsehn@ wrote the original code for the message loop so he would be more familiar with that part. I'm not sure who is familiar with ScopedPageLoadDeferrer and if/how this could be used to fix the problem. jochen@ may have an idea.

### yz...@chromium.org (2016-01-04)

Could you please update the description with the expected/actual output of the test case?

Thanks!

### ma...@gmail.com (2016-01-05)

The actual output is an alert dialog from https://abc.xyz, expected is the lack of it (maybe a single print dialog will pop up). Please find attached a minimized proof of concept that shows the gist of the problem and adds some comments for clarity.

### yz...@chromium.org (2016-01-05)

Thanks, marius.mlynski.

FYI, I have a CL under review which passes your test case.

### cl...@chromium.org (2016-01-20)

yzshen@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-02-03)

yzshen@: Uh oh! This issue is still open and hasn't been updated in the last 28 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### bu...@chromium.org (2016-02-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dd77c2a41c72589d929db0592565125ca629fb2c

commit dd77c2a41c72589d929db0592565125ca629fb2c
Author: yzshen <yzshen@chromium.org>
Date: Tue Feb 09 23:37:14 2016

Fix PPB_Flash_MessageLoop.

This CL suspends script callbacks and resource loads while running nested message loop using PPB_Flash_MessageLoop.

BUG=569496

Review URL: https://codereview.chromium.org/1559113002

Cr-Commit-Position: refs/heads/master@{#374529}

[modify] http://crrev.com/dd77c2a41c72589d929db0592565125ca629fb2c/chrome/test/ppapi/ppapi_browsertest.cc
[modify] http://crrev.com/dd77c2a41c72589d929db0592565125ca629fb2c/content/renderer/pepper/ppb_flash_message_loop_impl.cc
[modify] http://crrev.com/dd77c2a41c72589d929db0592565125ca629fb2c/ppapi/tests/test_flash_message_loop.cc
[modify] http://crrev.com/dd77c2a41c72589d929db0592565125ca629fb2c/ppapi/tests/test_flash_message_loop.h


### la...@google.com (2016-02-11)

I'm making the assumption that Clusterfuzz is going to ask for this to get Merge-Requested to M49, but... in the event that I'm wrong.

### ti...@google.com (2016-02-11)

Your change meets the bar and is auto-approved for M49 (branch: 2623)

### cl...@chromium.org (2016-02-11)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-02-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8093f1f141848e3672ef778764c18e844f1e5198

commit 8093f1f141848e3672ef778764c18e844f1e5198
Author: Yuzhu Shen <yzshen@chromium.org>
Date: Thu Feb 11 17:18:46 2016

Fix PPB_Flash_MessageLoop.

This CL suspends script callbacks and resource loads while running nested message loop using PPB_Flash_MessageLoop.

BUG=569496

Review URL: https://codereview.chromium.org/1559113002

Cr-Commit-Position: refs/heads/master@{#374529}
(cherry picked from commit dd77c2a41c72589d929db0592565125ca629fb2c)

Review URL: https://codereview.chromium.org/1691513004 .

Cr-Commit-Position: refs/branch-heads/2623@{#365}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] http://crrev.com/8093f1f141848e3672ef778764c18e844f1e5198/chrome/test/ppapi/ppapi_browsertest.cc
[modify] http://crrev.com/8093f1f141848e3672ef778764c18e844f1e5198/content/renderer/pepper/ppb_flash_message_loop_impl.cc
[modify] http://crrev.com/8093f1f141848e3672ef778764c18e844f1e5198/ppapi/tests/test_flash_message_loop.cc
[modify] http://crrev.com/8093f1f141848e3672ef778764c18e844f1e5198/ppapi/tests/test_flash_message_loop.h


### bu...@chromium.org (2016-02-15)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/8093f1f141848e3672ef778764c18e844f1e5198

commit 8093f1f141848e3672ef778764c18e844f1e5198
Author: Yuzhu Shen <yzshen@chromium.org>
Date: Thu Feb 11 17:18:46 2016


### ti...@google.com (2016-02-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-02)

Congrats again - $7,500 for this report. I want you to keep these UXSS reports coming but at the same time I also hope we can slow you down at some point :)

CVE-ID to follow.

### ti...@google.com (2016-03-02)

CVE-2016-1631

### sh...@chromium.org (2016-05-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

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

### la...@chromium.org (2021-02-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-02-25)

This issue was migrated from crbug.com/chromium/569496?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083383)*
