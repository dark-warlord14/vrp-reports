# Security: Buffer Overflow in glBindBuffer

| Field | Value |
|-------|-------|
| **Issue ID** | [40085717](https://issues.chromium.org/issues/40085717) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Reporter** | ne...@gmail.com |
| **Assignee** | cw...@chromium.org |
| **Created** | 2016-10-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

in src/libANGLE/HandleAllocator.cpp see HandleAllocator::reserve. This function is called by glBindBuffer using the user provided handle:

void HandleAllocator::reserve(GLuint handle)  

{  

// ...

```
// Not in released list, reserve in the unallocated list.  
auto boundIt = std::lower_bound(mUnallocatedList.begin(), mUnallocatedList.end(), handle, HandleRangeComparator());  

ASSERT(boundIt != mUnallocatedList.end());  

// function goes on to read and write from boundIt  
// ...  

```

boundIt can be equal to mUnallocatedList.end() if a lower bound is not found, leading to OOB read and write. The sequence of calls `glBindBuffer(GL_ARRAY_BUFFER, 0xFFFFFFFE); glBindBuffer(GL_ARRAY_BUFFER, 0xFFFFFFFF);` is sufficient to trigger this condition.

**VERSION**  

Chrome Version: Trunk Chrome ASAN build. I'm not sure how libANGLE tracks with Chrome, but the code appears about a year old in git.  

Operating System: Ubuntu Linux 16.04

**REPRODUCTION CASE**  

The attached poc.cc builds against libANGLE directly and triggers ASAN errors as shown in the attached log. I wrote a PoC that triggers the bug from NaCL with no user interaction upon visiting a webpage if you're interested.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU process  

Crash State: ASAN traceback is attached due to size

## Attachments

- [poc.cc](attachments/poc.cc) (text/plain, 753 B)
- [asan](attachments/asan) (text/plain, 23.2 KB)
- [additional_logs](attachments/additional_logs) (text/plain, 1.2 KB)

## Timeline

### mm...@chromium.org (2016-10-17)

Thanks for your report! Can you trigger the bug using Chrome (i.e. create such web-page or another file that triggers the overflow while being opened in Chrome)?

cwallez@, could you please take a look?

I'm setting High security severity for now.

[Monorail components: Internals>GPU>ANGLE]

### cw...@chromium.org (2016-10-17)

Thanks for the report, I'm taking a look.

WebGL doesn't allow create on bind, The other way to be able to trigger these calls would be to escape from the JS sandbox and do calls on the GLES2Impl directly, which would go through the GPU command buffer validation that should hide this bug.

Even with all of the above, it is a pretty bad issue that needs immediate attention.

### ne...@gmail.com (2016-10-17)

If you look under additional_logs, I'm able to trigger the error condition (an assert since it's a debug build) from NaCl directly (not via JS since you need to create a handle first). The ANGLE backtrace/testcase is more straightforward so I just posted that first.

I can prepare a package of the NaCL version tonight to help you determine the severity; I just wanted to make you aware of this issue as soon as I found it. It's quite possible that the GPU command buffer validation hides the bug despite it appearing to work for some reason on that trunk ASAN version I tested against.

### mm...@chromium.org (2016-10-17)

[Empty comment from Monorail migration]

### cw...@chromium.org (2016-10-17)

+zmo: I thought NaCl has through the command buffer and would hit https://cs.chromium.org/chromium/src/gpu/command_buffer/service/gles2_cmd_decoder.cc?sq=package:chromium&rcl=1476702996&l=5234 where the ID doesn't get forward to ANGLE.

The standalone poc.cpp will be enough to fix this, no need for an NaCl version, thanks!

### cw...@chromium.org (2016-10-17)

[Empty comment from Monorail migration]

### zm...@chromium.org (2016-10-17)

bind_generate_resource() returns true for Nacl because we strictly follow ES2 semantics for porting purpose.

### cw...@chromium.org (2016-10-17)

This was caused by the HandleAllocator uninitialized range used as [begin, end] and [begin, end) by different parts of the code. Fix is up for review at https://chromium-review.googlesource.com/c/399565/

### bu...@chromium.org (2016-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/c0281d4641a92f4f834b81658b1af674e1fe35d7

commit c0281d4641a92f4f834b81658b1af674e1fe35d7
Author: Corentin Wallez <cwallez@chromium.org>
Date: Mon Oct 17 19:19:01 2016

HandleAllocator: make HandleRange inclusive.

Previously part of the code saw it as [begin, end) while others saw it
as [begin, end].

BUG=angleproject:1052
BUG=chromium:656485

Change-Id: Id8e9e26b167e02a07dfc5341569df53a14d0623d
Reviewed-on: https://chromium-review.googlesource.com/399565
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Corentin Wallez <cwallez@chromium.org>

[modify] https://crrev.com/c0281d4641a92f4f834b81658b1af674e1fe35d7/src/libANGLE/HandleAllocator_unittest.cpp
[modify] https://crrev.com/c0281d4641a92f4f834b81658b1af674e1fe35d7/src/libANGLE/HandleAllocator.h
[modify] https://crrev.com/c0281d4641a92f4f834b81658b1af674e1fe35d7/src/libANGLE/HandleAllocator.cpp


### sh...@chromium.org (2016-10-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-10-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3cb4b0f4121967b4bb8a244d92d825d4a2b14a60

commit 3cb4b0f4121967b4bb8a244d92d825d4a2b14a60
Author: zmo <zmo@chromium.org>
Date: Sat Oct 22 04:11:33 2016

Roll ANGLE 336b147..f017315

https://chromium.googlesource.com/angle/angle.git/+log/336b147..f017315

BUG=chromium:657859,chromium:653454,chromium:653694,chromium:656485
TEST=bots
TBR=kbr@chromium.org
CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.android:android_optional_gpu_tests_rel

Review-Url: https://chromiumcodereview.appspot.com/2442143002
Cr-Commit-Position: refs/heads/master@{#426968}

[modify] https://crrev.com/3cb4b0f4121967b4bb8a244d92d825d4a2b14a60/DEPS
[modify] https://crrev.com/3cb4b0f4121967b4bb8a244d92d825d4a2b14a60/content/test/gpu/gpu_tests/webgl2_conformance_expectations.py


### mb...@chromium.org (2016-10-24)

Tentatively assigning high severity. A poc would still be useful for the reward panel.

### ne...@gmail.com (2016-10-24)

Sure thing. I'll take a look tonight and see whether this makes it through the command buffer validation.

### ne...@gmail.com (2016-10-25)

Unfortunately I'm still building 5 hours later :( I'm going to update as soon as I get a chance to hunt down whether this code is reachable easily from NaCl. The assert failure I was getting in my initial report seems to be unrelated.

### cw...@chromium.org (2016-10-25)

Let me know if this needs to be merged back in M55 and M54

### sh...@chromium.org (2016-10-25)

[Empty comment from Monorail migration]

### ne...@gmail.com (2016-10-26)

The original PoC provided won't hit the buggy code from NaCl. We can successfully call with any client id we want as the resource will be generated, but service_id, not the user's client_id is passed to the real glBindBuffer: https://cs.chromium.org/chromium/src/gpu/command_buffer/service/gles2_cmd_decoder.cc?sq=package:chromium&l=5253

After some more auditing I didn't see any place where the user can influence service_ids for glBind* functions without needing to loop UINT32_MAX times, which is slow.

### sh...@chromium.org (2016-11-08)

cwallez: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-11-22)

cwallez: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cw...@chromium.org (2016-11-22)

Closing as fixed because it is.

### sh...@chromium.org (2016-11-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-12-02)

The panel awarded $1,000 for this report.  They noted they might reconsider if it can be shown to manifest though NaCl.  For future reports please include all reproduction cases.

### ne...@gmail.com (2016-12-02)

I opened a related report that was low severity following a similar pattern: there is a bug in ANGLE that doesn't manifest through the command buffer. That time I made sure to fully check whether it was reachable via Chrome before submitting, as I realize it's time consuming to assess exploitability for the panel.

Thank you for the reward!

### aw...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-03-01)

This issue was migrated from crbug.com/chromium/656485?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085717)*
