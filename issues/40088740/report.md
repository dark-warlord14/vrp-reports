# Security: Out-Of-Bounds Read Vulnerability in Skia

| Field | Value |
|-------|-------|
| **Issue ID** | [40088740](https://issues.chromium.org/issues/40088740) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ku...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2017-08-17 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

Out-Of-Bounds Read Vulnerability triggered in Skia. 

Analysis done on LINUX System, Only the reporting was done on Windows System.

PoC has been tested on latest Chrome Linux "asan" build (#495180)as of Aug 17 12:24PM PST. 

Build links have been shared in the Step 1 of the "Reproduction Case" section.

VERSION
Chrome Version: Latest Linux "asan" release build.

Operating System: Ubuntu

REPRODUCTION CASE

1. Download chrome "asan" build from https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180.zip?generation=1502991555420768&alt=media

2. Unzip the downloaded "asan" builds.

3. Change directory to filter_fuzz_stub location.

4. Run the filter_fuzz_stub binary against the PoC.fil testcase file.

5. Check the crash details in the terminal window.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Binary crashes due to trigger of Out-Of-Bounds Read Vulnerability.

See ASAN Output Below: -

[0817/121221.165294:INFO:filter_fuzz_stub.cc(60)] Test case: /root/Desktop/fuzz-106.fil
[0817/121221.169954:INFO:filter_fuzz_stub.cc(37)] Valid stream detected.
ASAN:DEADLYSIGNAL
=================================================================
==17164==ERROR: AddressSanitizer: SEGV on unknown address 0xfe3018ab (pc 0x084f2901 bp 0xbfa0cbf8 sp 0xbfa0cbe0 T0)
==17164==The signal is caused by a READ memory access.
    #0 0x84f2900  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x84f2900)
    #1 0x84eef16  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x84eef16)
    #2 0x84eecee  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x84eecee)
    #3 0x84d8a6a  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x84d8a6a)
    #4 0x8c0a817  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8c0a817)
    #5 0x8c09801  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8c09801)
    #6 0x841e955  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x841e955)
    #7 0x84289cd  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x84289cd)
    #8 0x8426820  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8426820)
    #9 0x82d3b60  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x82d3b60)
    #10 0x82d48cf  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x82d48cf)
    #11 0x8d04622  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8d04622)
    #12 0x83b6a97  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x83b6a97)
    #13 0x82d47f3  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x82d47f3)
    #14 0x82d1884  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x82d1884)
    #15 0x8b16b9c  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8b16b9c)
    #16 0x8256d1d  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8256d1d)
    #17 0x8249d7b  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8249d7b)
    #18 0x8d6cf00  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8d6cf00)
    #19 0x82f7d33  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x82f7d33)
    #20 0x8b1abc2  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8b1abc2)
    #21 0x823e28a  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x823e28a)
    #22 0x82386a5  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x82386a5)
    #23 0x8260c82  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x8260c82)
    #24 0x825016d  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x825016d)
    #25 0x813d208  (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x813d208)
    #26 0xb6db4275  (/lib/i386-linux-gnu/libc.so.6+0x18275)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (/root/Desktop/linux-release-v8-arm%2Fasan-v8-arm-linux-release-495180/asan-v8-arm-linux-release-495180/filter_fuzz_stub+0x84f2900) 
==17164==ABORTING


## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### el...@chromium.org (2017-08-17)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### cl...@chromium.org (2017-08-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6408080261906432.

### rs...@chromium.org (2017-08-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-08-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-08-18)

+awhalley@ (Security TPM)

### aw...@google.com (2017-08-21)

Would somebody be able to confirm this is indeed an M61 regression, and doesn't manifest in M60?

### [Deleted User] (2017-08-22)

A function or two of the call stack may have changed, but I would seriously doubt that this is a regression.

### ku...@gmail.com (2017-08-23)

Hello @awhalley, @mtklein, Google Product Security Team,

Good Morning.

I would like to confirm that the same crash occurs in the linux "asan" "stable" version too 'asan-linux-stable-60.0.3112.90.zip', available at https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-stable-60.0.3112.90.zip?generation=1501801918603656&alt=media

Thanks,
~Kushal.

### aw...@chromium.org (2017-08-24)

Thanks, removing the release block label.

### sh...@chromium.org (2017-09-05)

mtklein: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2017-09-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-09-05)

ClusterFuzz testcase 6408080261906432 is flaky and no longer crashes, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### ku...@gmail.com (2017-09-05)

Hello @awhalley, @mtklein, Google Product Security Team,

Good Afternoon.

I think Clusterfuzz has gotten it all wrong. 

The testcase is still reproducing the same crash consistently on latest Linux ASAN build 499699 available at https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-499699.zip?generation=1504647571990611&alt=media

Also I would like to confirm that the PoC crashes on Mac OS as well.

Thanking You,

Yours Sincerely,
Kushal Arvind Shah.
Security Researcher | Fortinet's FortiGuard Labs.

### ku...@gmail.com (2017-09-06)

Crash confirmed on latest Mac ASAN release # 499858 available at https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/mac-release%2Fasan-mac-release-499858.zip?generation=1504675566563154&alt=media

Thanks,
~Kushal.

### aw...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-06)

Thanks for confirming!

### [Deleted User] (2017-09-08)

I am able to reproduce this at head.

### [Deleted User] (2017-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2017-09-08)

The crash comes from trying to blit one pixel into a 1x1 pixmap at [0, -33554432], which is impossible.  -33554432 is 0x80000000 >> 6, and the 0x80000000 came from an over- or underflowing cast from float.  We can rule out large-magnitude finite values by bounds intersection tests done in float-space, which leaves only non-finite values (inf, NaN) as possible explanations.

To fix this as widely as possible, we're going to try making our path iterators abort immediately if any point in the path contains a non-finite coordinate.  This prevents this crash, and will likely defend against many similar ones.  https://skia-review.googlesource.com/c/skia/+/44420

If this patch turns out to be infeasible to land, we can certainly try something more focused.

### bu...@chromium.org (2017-09-08)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/1170a553be35920fe45d6a454a27d21167060977

commit 1170a553be35920fe45d6a454a27d21167060977
Author: Mike Klein <mtklein@chromium.org>
Date: Fri Sep 08 19:56:38 2017

Don't allow iteration through non-finite points.

Added a unit test too.

BUG=chromium:756563

Change-Id: Ic77a89b4a98d1a553877af9807a3d3bdcd077bb9
Reviewed-on: https://skia-review.googlesource.com/44420
Commit-Queue: Mike Klein <mtklein@chromium.org>
Reviewed-by: Mike Reed <reed@google.com>

[modify] https://crrev.com/1170a553be35920fe45d6a454a27d21167060977/src/core/SkPathRef.cpp
[modify] https://crrev.com/1170a553be35920fe45d6a454a27d21167060977/tests/PathTest.cpp
[modify] https://crrev.com/1170a553be35920fe45d6a454a27d21167060977/include/private/SkPathRef.h


### [Deleted User] (2017-09-08)

To follow up on the line in comments 7+8, this is not a regression.  The call stack recently changed, and _another_ call stack change is likely why ClusterFuzz thought this was fixed a couple days ago.

### bu...@chromium.org (2017-09-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/76782217f4c8dd3bfbdfd2a2fd522bef01b48f37

commit 76782217f4c8dd3bfbdfd2a2fd522bef01b48f37
Author: skia-deps-roller@chromium.org <skia-deps-roller@chromium.org>
Date: Fri Sep 08 22:26:55 2017

Roll src/third_party/skia/ 7f754260f..71c05ead1 (12 commits)

https://skia.googlesource.com/skia.git/+log/7f754260f7fc..71c05ead16d2

$ git log 7f754260f..71c05ead1 --date=short --no-merges --format='%ad %ae %s'
2017-09-08 angle-deps-roller Roll skia/third_party/externals/angle2/ ec3a9cbb5..6f0c17c7d (1 commit)
2017-09-08 egdaniel Revert "Remove isMipMapped from GrSurfaceDesc" and follow up find exact scratch CL
2017-09-08 mtklein Don't allow iteration through non-finite points.
2017-09-07 csmartdalton CCPR: Check for flat lines before crunching on curves
2017-09-08 jvanverth Revert "Revert "Add multitexture support to text and path shaders""
2017-09-08 mtklein update SkJumper stages to clang 5
2017-09-08 egdaniel Update GrResourceCache changeUniqueKey to stay in valid state after each step
2017-09-08 brianosman Skip making a surface context when doing threaded SW paths
2017-09-08 jvanverth Revert "Add multitexture support to text and path shaders"
2017-09-08 bsalomon Revert "Revert "Make TextureOp use multitexturing to batch draws of different SkImages.""
2017-09-07 benjaminwagner Update NexusPlayers to Android O PR6.
2017-09-08 angle-deps-roller Roll skia/third_party/externals/angle2/ 95644f92d..ec3a9cbb5 (2 commits)

Created with:
  roll-dep src/third_party/skia
BUG=756563


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


CQ_INCLUDE_TRYBOTS=master.tryserver.blink:linux_trusty_blink_rel;master.tryserver.chromium.linux:linux_optional_gpu_tests_rel;master.tryserver.chromium.mac:mac_optional_gpu_tests_rel;master.tryserver.chromium.win:win_optional_gpu_tests_rel;master.tryserver.chromium.android:android_optional_gpu_tests_rel
TBR=robertphillips@chromium.org

Change-Id: I0eea71e1b58665b82f47e65e6c80446f6b3affbc
Reviewed-on: https://chromium-review.googlesource.com/658262
Reviewed-by: Skia Deps Roller <skia-deps-roller@chromium.org>
Commit-Queue: Skia Deps Roller <skia-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#500706}
[modify] https://crrev.com/76782217f4c8dd3bfbdfd2a2fd522bef01b48f37/DEPS


### [Deleted User] (2017-09-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-09)

[Empty comment from Monorail migration]

### aw...@google.com (2017-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-15)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2017-09-15)

The patch above, "Don't allow iteration through non-finite points.", would be easy and safe to backport.

### aw...@chromium.org (2017-09-16)

[Comment Deleted]

### aw...@chromium.org (2017-09-16)

[Comment Deleted]

### aw...@chromium.org (2017-09-16)

abdulsyed@ - good for 62

### ab...@google.com (2017-09-18)

Approving merge to M62. Branch:3202

### in...@chromium.org (2017-09-18)

We have made a bunch of changes on ClusterFuzz side, so resetting ClusterFuzz-Wrong label.

### bu...@chromium.org (2017-09-18)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/3414ad74030e09631eadb5f4c996572d7b1a6443

commit 3414ad74030e09631eadb5f4c996572d7b1a6443
Author: Mike Klein <mtklein@chromium.org>
Date: Mon Sep 18 18:25:01 2017

Cherry pick: Don't allow iteration through non-finite points.

Original CL:

    Don't allow iteration through non-finite points.

    Added a unit test too.

    BUG=chromium:756563

    Change-Id: Ic77a89b4a98d1a553877af9807a3d3bdcd077bb9
    Reviewed-on: https://skia-review.googlesource.com/44420
    Commit-Queue: Mike Klein <mtklein@chromium.org>
    Reviewed-by: Mike Reed <reed@google.com>

This cherry picks that to m62 minus its additional unit test, which
had some awkward formatting-based merge conflicts.  Only the change
to SkPathRef.cpp is important here.

Change-Id: Ic3e1fa4244a921064d0c0b8a8afafd72af39df4d
Reviewed-on: https://skia-review.googlesource.com/48043
Reviewed-by: Mike Klein <mtklein@chromium.org>

[modify] https://crrev.com/3414ad74030e09631eadb5f4c996572d7b1a6443/src/core/SkPathRef.cpp
[modify] https://crrev.com/3414ad74030e09631eadb5f4c996572d7b1a6443/include/private/SkPathRef.h


### aw...@chromium.org (2017-09-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-18)

Nice one kushal89.shah@! The VRP panel decided to award $1,000 for this.  They also noted that they would reconsider for a higher amount if you demonstrate how to turn this into a write.

### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-09-20)

Merged -removing label. 

### ku...@gmail.com (2017-09-25)

Hello @awhalley, @mtklein, @rsesek, elawre..., @abdulsyed, @govind, @reed, @fmailta, Google Product Security Team [skia],

Good Afternoon.

Firstly, I would like to thank you for fixing this Vulnerability so quickly and also for the generous bounty, I sincerely appreciate it.

Secondly, since this issue was affecting a Stable version too, I would like to request @awhalley for a CVE-ID for this Vulnerability.

Also, I still haven't received any tax-related document for my previous finds and related bounties, could someone help me on that? 

And I would also like to request for an estimate on the payout time-frame for this one so that I can accordingly diligently file my taxes in the correct financial year.

Eagerly awaiting your reply.

Thanking You,

Yours Sincerely,
Kushal Arvind Shah.
Security Researcher | Fortinet's FortiGuard Labs.

### aw...@google.com (2017-10-02)

(I've followed up with Kushal in email)

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/756563?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088740)*
