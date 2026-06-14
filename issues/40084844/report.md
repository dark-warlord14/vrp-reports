# Heap-use-after-free in blink::PaintController::commitNewDisplayItems

| Field | Value |
|-------|-------|
| **Issue ID** | [40084844](https://issues.chromium.org/issues/40084844) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Paint |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | wa...@chromium.org |
| **Created** | 2016-07-14 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5841673557114880

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0xcf18c780
Crash State:
  blink::PaintController::commitNewDisplayItems
  blink::GraphicsLayer::paint
  blink::FrameView::synchronizedPaintRecursively
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=403780:403787

Minimized Testcase (6.08 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94v1XcV8nBiI7P8ThpgCJDercUAnCLtmD5pRdzgpsn72SKS18dfkzjZbceO2VgtZSvl4JCONONW8IeZHIKPRBg7SjNFbd87p9rKFHGnDSM1k5Vv1tDKqG2pJU4qE-HU6UGPoZAWHMG8lBGeQUYoSIJrQV7m8A?testcase_id=5841673557114880

Filer: mmoroz

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### mm...@chromium.org (2016-07-14)

Looks similar to https://crbug.com/chromium/626182, but stacktrace differs a bit (line numbers).

[Monorail components: Blink>Paint]

### sh...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-14)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

M53 beta launch is coming soon.Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix before 6:00 PM PST, Monday (07/18/16). Thank you.

### go...@chromium.org (2016-07-19)

M53 beta launch is next week.Your bug is labelled as Beta ReleaseBlock, pls make sure to land the fix before 6:00 PM PST, Friday (07/22/16). Thank you.

### wa...@chromium.org (2016-07-20)

mmoroz@ where can I find the instruction for building linux_asan_chrome_v8_arm locally?

### wa...@chromium.org (2016-07-20)

Downloaded the config and build, and ran run_gestures_on_device_local.py but it didn't show any problem:

$ python $CF_HOME/src/tools/on_demand/run_gestures_on_device_local.py --config ~/Downloads/config_5841673557114880.zip --build ~/Downloads/asan-v8-arm-linux-release-405116/
Xvfb: no process found
blackbox: no process found
Initializing built-in extension Generic Event Extension
Initializing built-in extension SHAPE
Initializing built-in extension MIT-SHM
Initializing built-in extension XInputExtension
Initializing built-in extension XTEST
Initializing built-in extension BIG-REQUESTS
Initializing built-in extension SYNC
Initializing built-in extension XKEYBOARD
Initializing built-in extension XC-MISC
Initializing built-in extension SECURITY
Initializing built-in extension XINERAMA
Initializing built-in extension XFIXES
Initializing built-in extension RENDER
Initializing built-in extension RANDR
Initializing built-in extension COMPOSITE
Initializing built-in extension DAMAGE
Initializing built-in extension MIT-SCREEN-SAVER
Initializing built-in extension DOUBLE-BUFFER
Initializing built-in extension RECORD
Initializing built-in extension DPMS
Initializing built-in extension Present
Initializing built-in extension DRI3
Initializing built-in extension X-Resource
Initializing built-in extension XVideo
Initializing built-in extension XVideo-MotionCompensation
Initializing built-in extension SELinux
Initializing built-in extension GLX
[dix] Could not init font path element /usr/share/fonts/X11/cyrillic, removing from list!
[dix] Could not init font path element /usr/share/fonts/X11/100dpi/:unscaled, removing from list!
[dix] Could not init font path element /usr/share/fonts/X11/75dpi/:unscaled, removing from list!
[dix] Could not init font path element /usr/share/fonts/X11/100dpi, removing from list!
[dix] Could not init font path element /usr/share/fonts/X11/75dpi, removing from list!
blackbox: managing screen 0 using TrueColor visual 0x21, depth 24
/usr/local/google/home/wangxianzhu/clusterfuzz/scripts/start_schroot /usr/local/google/home/wangxianzhu/Downloads/asan-v8-arm-linux-release-405116/chrome --user-data-dir=/tmp/tmpchgKzX/temp/user_profile_0 --log-net-log=/tmp/tmpchgKzX/temp/net_log_0 --js-flags="--expose-gc --verify-heap" --no-first-run --use-gl=osmesa --disable-gl-drawing-for-tests --no-sandbox /usr/local/google/home/wangxianzhu/clusterfuzz/slave-bot/inputs/fuzzer-testcases/fuzz-515.html
Starting run number: 0
Starting run number: 1
Starting run number: 2
Starting run number: 3
Starting run number: 4
Starting run number: 5
Starting run number: 6
Starting run number: 7
Starting run number: 8
Starting run number: 9
Starting run number: 10
Starting run number: 11
Starting run number: 12
Starting run number: 13
Starting run number: 14
Starting run number: 15
Starting run number: 16
Starting run number: 17
Starting run number: 18
Starting run number: 19
Starting run number: 20
Starting run number: 21
Starting run number: 22
Starting run number: 23
Starting run number: 24
No crash found.
XIO:  fatal IO error 11 (Resource temporarily unavailable) on X server ":1"
      after 588 requests (586 known processed) with 0 events remaining.
blackbox: no process found


### wa...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-07-20)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4545960500002816

Fuzzer: attekett_surku_fuzzer
Job Type: linux_lsan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60800004f320
Crash State:
  blink::PaintController::commitNewDisplayItems
  blink::GraphicsLayer::paint
  blink::FrameView::synchronizedPaintRecursively
  
Recommended Security Severity: High


Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96xUR9nnL2GbGOKPDGwDOMIKRz_HTZkA8iJGETuxazSw_B6BbIOeRIpZDucVwDCFVRGPefKwia9fT34y4FWpbx3dvvmkRjeWD2sUoBlp-wPmsFxNs9PaLIn0GcLJCFZkwFFi3PsakslNM0XOa_a7yueDwWBlnmmHJfcPVEp_kgMJnno2R4?testcase_id=4545960500002816


Filer: wangxianzhu

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### wa...@chromium.org (2016-07-20)

Also couldn't reproduce #10 locally.

### mm...@chromium.org (2016-07-21)

wangxianzhu@, I have no experience with building chrome for ARM. Though there is some documentation (https://chromium.googlesource.com/chromium/src/+/master/docs/linux_chromium_arm.md#Automated-Build-and-Testing)

Also I don't think you need run_gestures_on_device_local.py. 

CC'ing inferno@ and mbarbella@.

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### wa...@chromium.org (2016-07-21)

> Also I don't think you need run_gestures_on_device_local.py.

It is a suggested way to reproduce a clusterfuzz bug locally (https://docs.google.com/document/d/15ZqPDlz3a8Ac08uWWBc-tM4IZzhP-kYEuQAXiJRiH24/edit#heading=h.uoltawkpum5p). If I couldn't reproduce a bug with it, it would be unlikely to reproduce the bug with a local build, right?

### aw...@chromium.org (2016-07-21)

(I'm afraid sheriffbot's label changes were a hiccup - this is still a blocker for Friday's M53)

### bu...@chromium.org (2016-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f6c6259fca56e59fdb6d420f6d809d2c6c8cbdca

commit f6c6259fca56e59fdb6d420f6d809d2c6c8cbdca
Author: Xianzhu Wang <wangxianzhu@chromium.org>
Date: Thu Jul 21 18:55:40 2016

Try to fix crash because of InlineBox deletion in a cached subsequence

Don't know why the crashes occurred on bots. Couldn't reproduce the
crashes reported by clusterfuzz locally. Based on the stack, the crash
are because of deletion of an InlineBox in a cached subsequence.

This partly reverts https://codereview.chromium.org/2160983007/.

BUG=619630,628117
R=chrishtr@chromium.org

Review URL: https://codereview.chromium.org/2170583003 .

Cr-Commit-Position: refs/heads/master@{#406925}

[modify] https://crrev.com/f6c6259fca56e59fdb6d420f6d809d2c6c8cbdca/third_party/WebKit/Source/core/layout/LayoutObject.h
[modify] https://crrev.com/f6c6259fca56e59fdb6d420f6d809d2c6c8cbdca/third_party/WebKit/Source/core/layout/api/LineLayoutItem.h
[modify] https://crrev.com/f6c6259fca56e59fdb6d420f6d809d2c6c8cbdca/third_party/WebKit/Source/core/layout/line/InlineBox.cpp


### cl...@chromium.org (2016-07-21)

ClusterFuzz has detected this issue as fixed in range 405744:405768.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5841673557114880

Fuzzer: attekett_surku_fuzzer
Job Type: linux_asan_chrome_v8_arm
Platform Id: linux

Crash Type: Heap-use-after-free READ 4
Crash Address: 0xcf18c780
Crash State:
  blink::PaintController::commitNewDisplayItems
  blink::GraphicsLayer::paint
  blink::FrameView::synchronizedPaintRecursively
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=403780:403787
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_v8_arm&range=405744:405768

Minimized Testcase (6.08 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94v1XcV8nBiI7P8ThpgCJDercUAnCLtmD5pRdzgpsn72SKS18dfkzjZbceO2VgtZSvl4JCONONW8IeZHIKPRBg7SjNFbd87p9rKFHGnDSM1k5Vv1tDKqG2pJU4qE-HU6UGPoZAWHMG8lBGeQUYoSIJrQV7m8A?testcase_id=5841673557114880

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-07-22)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### mm...@chromium.org (2016-07-22)

Fix without successful local reproduction -- awesome!
Sorry for this hard-to-reproduce case, sometimes it happens.

### sh...@chromium.org (2016-07-22)

[Empty comment from Monorail migration]

### wa...@chromium.org (2016-07-22)

[Empty comment from Monorail migration]

### sh...@google.com (2016-07-22)

Your change meets the bar and is auto-approved for M53 (branch: 2785)

### bu...@chromium.org (2016-07-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/25bb7bb0662cd4ad0c79d33dfce534b0ca630bb2

commit 25bb7bb0662cd4ad0c79d33dfce534b0ca630bb2
Author: Xianzhu Wang <wangxianzhu@chromium.org>
Date: Fri Jul 22 22:05:34 2016

Try to fix crash because of InlineBox deletion in a cached subsequence

Don't know why the crashes occurred on bots. Couldn't reproduce the
crashes reported by clusterfuzz locally. Based on the stack, the crash
are because of deletion of an InlineBox in a cached subsequence.

This partly reverts https://codereview.chromium.org/2160983007/.

BUG=619630,628117
R=chrishtr@chromium.org

Review URL: https://codereview.chromium.org/2170583003 .

Review URL: https://codereview.chromium.org/2180573002 .

Cr-Original-Commit-Position: refs/heads/master@{#406925}
Cr-Commit-Position: refs/branch-heads/2785@{#313}
Cr-Branched-From: 68623971be0cfc492a2cb0427d7f478e7b214c24-refs/heads/master@{#403382}

[modify] https://crrev.com/25bb7bb0662cd4ad0c79d33dfce534b0ca630bb2/third_party/WebKit/Source/core/layout/LayoutObject.h
[modify] https://crrev.com/25bb7bb0662cd4ad0c79d33dfce534b0ca630bb2/third_party/WebKit/Source/core/layout/api/LineLayoutItem.h
[modify] https://crrev.com/25bb7bb0662cd4ad0c79d33dfce534b0ca630bb2/third_party/WebKit/Source/core/layout/line/InlineBox.cpp


### aw...@chromium.org (2016-07-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

Thanks as ever!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@google.com (2017-01-04)

The local unreproducibility of this might be expected because the testcase is marked as unreproducible (which means clusterfuzz could not reproduce it).

### wa...@chromium.org (2017-01-04)

Where can I see the unreproducibility status of the test case? The bug is still marked Reproducible, and at that time the bug was reproducible on the bot.

### is...@google.com (2017-01-04)

This issue was migrated from crbug.com/chromium/628117?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/628998]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084844)*
