# Crash with three-way self Jitsi Meet call

| Field | Value |
|-------|-------|
| **Issue ID** | [432035817](https://issues.chromium.org/issues/432035817) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>Codecs |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jo...@gmail.com |
| **Assignee** | ma...@google.com |
| **Created** | 2025-07-15 |
| **Bounty** | $7,000.00 |

## Description

IMPORTANT: Your crash has already been automatically reported to our crash system. Please file this bug only if you can provide more information about it.


Chrome Version: 138.0.7204.158
Operating System: Mac OS X 15.5.0

URL (if applicable) where crash occurred: https://beta.meet.jit.si/ATestJitsiConference/.

Can you reproduce this crash?

What steps will reproduce this crash? (If it's not reproducible, what were you doing just before the crash?)
1. Join a three-way call to the same Jitsi Meet conference, in three separate tabs.  Turn on sending video on each tab.  Turn on background blur for each video.
2. Pull out the three tabs to three separate windows, all visible on-screen.
3. Wait.

All three tabs crashed for me near-simultaneously.  I have uploaded all three crashes.  The three crash IDs are:

Crash from Tuesday, July 15, 2025 at 3:49:02 PM
Status:	Uploaded
Uploaded Crash Report ID:	859a626b13b72cf4
Upload Time:	Tuesday, July 15, 2025 at 4:04:03 PM
Local Crash Context:	9e038f09-8976-45b5-8199-eae8e159ef68

Crash from Tuesday, July 15, 2025 at 3:48:39 PM
Status:	Uploaded
Uploaded Crash Report ID:	4687da90671adb6e
Upload Time:	Tuesday, July 15, 2025 at 4:04:03 PM
Local Crash Context:	10632e25-608c-4274-b3fd-7c5255fe0a9b

Crash from Tuesday, July 15, 2025 at 3:48:35 PM
Status:	Uploaded
Uploaded Crash Report ID:	f9d9ae28f307b76a
Upload Time:	Tuesday, July 15, 2025 at 4:04:03 PM
Local Crash Context:	78a40942-7628-4a1f-8a03-99b59c3251d6

****DO NOT CHANGE BELOW THIS LINE****
Crash ID: crash/f9d9ae28f307b76a

## Attachments

- Chrome-138-crashes.txt (text/plain, 23.0 KB)
- chrome-asan-crash-stackwalk-stacks.txt (text/plain, 964.4 KB)
- chrome-asan-crash-stackwalk.txt (text/plain, 279.3 KB)
- chrome-asan-crash.txt (text/plain, 31.5 KB)

## Timeline

### jo...@gmail.com (2025-07-15)

redacted

### jo...@gmail.com (2025-07-16)

I repeated the test as described above, and it crashed again in about 20 minutes, so it seems to be reproducible.  Again, all three tabs crashed near-simultaneously.  The three new crash IDs are:

Crash from Tuesday, July 15, 2025 at 4:37:23 PM
Status:	Uploaded
Uploaded Crash Report ID:	280ca97ffe49fd73
Upload Time:	Wednesday, July 16, 2025 at 11:32:38 AM
Local Crash Context:	457ec388-8484-4cc5-8b80-6102e28bdd82

Crash from Tuesday, July 15, 2025 at 4:36:58 PM
Status:	Uploaded
Uploaded Crash Report ID:	07268a78349fe201
Upload Time:	Wednesday, July 16, 2025 at 11:32:39 AM
Local Crash Context:	efd440cb-a79c-49e7-b17c-7d53193166c2

Crash from Tuesday, July 15, 2025 at 4:36:55 PM
Status:	Uploaded
Uploaded Crash Report ID:	a5367a4d72bc2063
Upload Time:	Wednesday, July 16, 2025 at 11:32:38 AM
Local Crash Context:	964ac523-1a02-4264-82d2-0ec765a7b7ee

A symbolicated minidump_stacktrace of the crashes doesn't look like it shows any commonality between the crashes beyond partition_alloc - you probably have access to this but I've attached the stack traces I generated anyway.

Given Chrome's tab isolation the fact that all three tabs crash simultaneously hopefully narrows down what the problem could be?  

### jo...@gmail.com (2025-07-17)

I built an asan-enabled Chromium and re-ran my test, and got an asan heap overflow error in libaom.  (It's a read not a write, but once things have gone wrong presumably a write could follow.).

Information attached, I assume the actual crash is not useful given that it's a locally-built binary.

### ht...@google.com (2025-07-21)

This is not a duplicate of the duplicated-to bug. Please don't mark it as such.


### nh...@chromium.org (2025-07-21)

The crash report crash/859a626b13b72cf4 appears to most closely match the stack trace in the provided asan report.

ssilkin: can you investigate this or find an appropriate owner?

### ht...@google.com (2025-07-21)

adding @ma...@google.com  in case AV1 expertise is the right place to go with this.


### ch...@google.com (2025-07-22)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-07-22)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ss...@google.com (2025-07-22)

<https://crash.corp.google.com/browse?q=stable_signature%3D%27static+void+partition_alloc%3A%3Ainternal%3A%3ACorruptionDetected-e4a8b7e8%27>

Probably this aom\_free(): <https://source.chromium.org/chromium/chromium/src/+/refs/tags/138.0.7194.0:third_party/libaom/source/libaom/av1/encoder/ratectrl.c;l=3800>

@marpan , @jianj , Could you please take a look?

### ma...@google.com (2025-07-23)

Was able to reproduce the crash (via the asan report, #4). Will likely merge in this fix tomorrow: https://aomedia-review.googlesource.com/c/aom/+/201661.  Didn't get the crash with the fix after a few runs.

### dx...@google.com (2025-07-23)

Project: aom  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/201661>

rtc: Restrict usage of src\_sad\_blk\_64x64 to single spatial layer

---


Expand for full commit details
```
     
    For blk_sad usage: disallow for spatial layers. 
     
    This is a possible fix for the crash in the issue below. 
     
    The issue seems to be incorrect setting of svc->mi_cols/rows_full_resoln (used for the allocation of src_sad_blk_64x64 for spatial layers) for the case of switching up layers (2SL to 3SL) and then passing in lower resolution for the top layer after the switch. 
     
    The performance effect of src_sad_blk_64x64 for spatial layered encoding is expected to be small/minimal, so ok to disable. Will follow-up with a unittest and maybe re-enable the feature with the proper fix. 
     
    Bug b:433046392, b:432035817 
     
    Change-Id: Id0b2b36771fffef75bc89f51cf62709d5b6ad606

```

---

Files:

- M `av1/encoder/ratectrl.c`

---

Hash: 820b4991a9c76831a8631ea93077f71fa240c15f  

Date: Wed Jul 23 03:15:32 2025


---

### ma...@google.com (2025-07-24)

Will roll the fix into chromium tomorrow.

### dx...@google.com (2025-07-24)

Project: chromium/src  

Branch:  main  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/6781964>

Roll src/third\_party/libaom/source/libaom/ a48eee7fd..f6055d0dc (8 commits)

---


Expand for full commit details
```
     
    https://aomedia.googlesource.com/aom.git/+log/a48eee7fd280..f6055d0dc007 
     
    $ git log a48eee7fd..f6055d0dc --date=short --no-merges --format='%ad %ae %s' 
    2025-07-22 jianj Cosmetic: Fix clang-tidy warnings 
    2025-07-22 marpan rtc: Restrict usage of src_sad_blk_64x64 to single spatial layer 
    2025-07-22 juliobbv Enable screen detection mode 2 for image-focused tunings 
    2025-07-22 wtc DatarateTestPsnr: Fix CONFIG_INTERNAL_STATS check 
    2025-07-22 yunqingwang Add two shorts files for end-to-end tests 
    2025-01-09 phancke Allow per-frame calculation of PSNR 
    2025-07-22 jianj Remove tools/auto_refactor 
    2025-07-18 juliobbv Misc code review feedback follow-up 
     
    Created with: 
      roll-dep src/third_party/libaom/source/libaom 
    R=jzern@google.coom 
     
    Bug: b:307414544, b:432035817, b:433046392, webrtc:388070060 
    Change-Id: Ia68d6ff9fc38d5341b59fdb86198fff8c4e7e529 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6781964 
    Commit-Queue: Marco Paniconi <marpan@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Reviewed-by: James Zern <jzern@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1491583}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/config/config/aom_version.h`
- M `third_party/libaom/source/libaom`

---

Hash: [daa4b000f48a2e283ef4a1977d945a988f78a590](http://crrev.com/daa4b000f48a2e283ef4a1977d945a988f78a590)  

Date: Thu Jul 24 17:56:37 2025


---

### ma...@google.com (2025-07-28)

Jonathan, can you verify on your side if the issue is fixed?

### ch...@google.com (2025-07-29)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-07-31)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M138. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [138, 139].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ma...@google.com (2025-07-31)

Which CLs should be backmerged? (Please include Gerrit links.)
https://aomedia-review.git.corp.google.com/c/aom/+/201661

Has this fix been verified on Canary to not pose any stability regressions?
Yes

Does this fix pose any potential non-verifiable stability risks?
No

Does this fix pose any known compatibility risks?
No

Does it require manual verification by the test team? If so, please describe required testing.
No

### pg...@google.com (2025-07-31)

nothing relevant to the fix seen in canary/dev as far as i can tell -

cherry pick approved for M139 for <https://aomedia-review.git.corp.google.com/c/aom/+/201661>! please cherry pick to 7258 ASAP to attempt get this fix into the next M139 release!

merge for 138 on pause for now due to scheduling - we will comment back on the bug next week!

### dx...@google.com (2025-08-01)

Project: aom  

Branch:  m139-7258  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/202081>

rtc: Restrict usage of src\_sad\_blk\_64x64 to single spatial layer

---


Expand for full commit details
```
     
    For blk_sad usage: disallow for spatial layers. 
     
    This is a possible fix for the crash in the issue below. 
     
    The issue seems to be incorrect setting of svc->mi_cols/rows_full_resoln (used for the allocation of src_sad_blk_64x64 for spatial layers) for the case of switching up layers (2SL to 3SL) and then passing in lower resolution for the top layer after the switch. 
     
    The performance effect of src_sad_blk_64x64 for spatial layered encoding is expected to be small/minimal, so ok to disable. Will follow-up with a unittest and maybe re-enable the feature with the proper fix. 
     
    Bug b:433046392, b:432035817 
     
    Change-Id: Id0b2b36771fffef75bc89f51cf62709d5b6ad606 
    (cherry picked from commit 820b4991a9c76831a8631ea93077f71fa240c15f)

```

---

Files:

- M `av1/encoder/ratectrl.c`

---

Hash: 90c632fc6c01cd8637186c783ca8012bab3c3260  

Date: Wed Jul 23 03:15:32 2025


---

### dx...@google.com (2025-08-01)

Project: chromium/src  

Branch:  refs/branch-heads/7258  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/6813429>

[Merge M139] Restrict src\_sad\_blk\_64x64 to single spatial layer

---


Expand for full commit details
```
     
    Cherry-pick the fix for this issue. 
     
    Bug: b:433046392, b:432035817 
    Change-Id: I86540ae7dc7f6f8ecbc54cae94ec11a6520628c7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6813429 
    Reviewed-by: James Zern <jzern@google.com> 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Commit-Queue: Marco Paniconi <marpan@google.com> 
    Cr-Commit-Position: refs/branch-heads/7258@{#2357} 
    Cr-Branched-From: f600d0656fd5b5fe4a82981f533d31ed6939e2e4-refs/heads/main@{#1477651}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/libaom`

---

Hash: [ff41ba7fa7ddf30c58768a56750a7fdaf65dbfb8](http://crrev.com/ff41ba7fa7ddf30c58768a56750a7fdaf65dbfb8)  

Date: Fri Aug 1 21:22:36 2025


---

### pe...@google.com (2025-08-01)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ma...@google.com (2025-08-04)

Was this issue a regression for the milestone it was found in?
Yes

Is this issue related to a change or feature merged after the latest LTS Milestone?
No

### jo...@gmail.com (2025-08-05)

Please also see <https://issues.chromium.org/issues/436603869> - there's also an unguarded write to `src_sad_blk_64x64` which is causing out-of-bounds writes.

### am...@chromium.org (2025-08-06)

Please CP and backmerge this fix to M138 Extended / branch 7204 by EOD Monday, 11 August

### dx...@google.com (2025-08-07)

Project: aom  

Branch:  m138-7204  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://aomedia-review.googlesource.com/202101>

rtc: Restrict usage of src\_sad\_blk\_64x64 to single spatial layer

---


Expand for full commit details
```
     
    For blk_sad usage: disallow for spatial layers. 
     
    This is a possible fix for the crash in the issue below. 
     
    The issue seems to be incorrect setting of svc->mi_cols/rows_full_resoln (used for the allocation of src_sad_blk_64x64 for spatial layers) for the case of switching up layers (2SL to 3SL) and then passing in lower resolution for the top layer after the switch. 
     
    The performance effect of src_sad_blk_64x64 for spatial layered encoding is expected to be small/minimal, so ok to disable. Will follow-up with a unittest and maybe re-enable the feature with the proper fix. 
     
    Bug b:433046392, b:432035817 
     
    Change-Id: Id0b2b36771fffef75bc89f51cf62709d5b6ad606 
    (cherry picked from commit 820b4991a9c76831a8631ea93077f71fa240c15f)

```

---

Files:

- M `av1/encoder/ratectrl.c`

---

Hash: 1a5d58271aa6133b6fa7da9fa365290cc4f2cc4d  

Date: Wed Jul 23 03:15:32 2025


---

### dx...@google.com (2025-08-07)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/6825313>

[Merge M138] Restrict src\_sad\_blk\_64x64 to single spatial layer

---


Expand for full commit details
```
     
    Cherry-pick the fix for this issue. 
     
    Bug: b:433046392, b:432035817 
    Change-Id: Ia7beb92901cb10050d000b2d71eaa09ca8036581 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6825313 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Reviewed-by: James Zern <jzern@google.com> 
    Commit-Queue: Marco Paniconi <marpan@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#2859} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/libaom`

---

Hash: [9cdbabd599165debf52b936c61959e1293b5794f](http://crrev.com/9cdbabd599165debf52b936c61959e1293b5794f)  

Date: Thu Aug 7 02:44:11 2025


---

### pg...@google.com (2025-08-12)

hello @reporter - how would you like to be credited for this report?

### sp...@google.com (2025-08-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
report of memory corruption in a sandboxed process / the renderer 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2025-08-29)

Project: chromium/src  

Branch:  refs/branch-heads/7204\_184  

Author:  Marco Paniconi [marpan@google.com](mailto:marpan@google.com)  

Link:    <https://chromium-review.googlesource.com/6897209>

[CfM-R138][Merge M138] Restrict src\_sad\_blk\_64x64 to single spatial layer

---


Expand for full commit details
```
     
    Cherry-pick the fix for this issue. 
     
    Bug: b:433046392, b:432035817 
    Change-Id: Ia7beb92901cb10050d000b2d71eaa09ca8036581 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6825313 
    Reviewed-by: Wan-Teh Chang <wtc@google.com> 
    Reviewed-by: James Zern <jzern@google.com> 
    Commit-Queue: Marco Paniconi <marpan@google.com> 
    Cr-Original-Commit-Position: refs/branch-heads/7204@{#2859} 
    Cr-Original-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6897209 
    Reviewed-by: Kyle Williams <kdgwill@chromium.org> 
    Auto-Submit: Joshua Pius <joshuapius@google.com> 
    Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
    Owners-Override: Joshua Pius <joshuapius@google.com> 
    Commit-Queue: Joshua Pius <joshuapius@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204_184@{#15} 
    Cr-Branched-From: 7ea839044480a944888296dc0cccc5afb60b736c-refs/branch-heads/7204@{#2436} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `DEPS`
- M `third_party/libaom/README.chromium`
- M `third_party/libaom/source/libaom`

---

Hash: [4ac713469d5143f128789572620e3a9721210a2c](https://chromiumdash.appspot.com/commit/4ac713469d5143f128789572620e3a9721210a2c)  

Date: Fri Aug 29 19:25:57 2025


---

### qk...@google.com (2025-09-04)

Labelled as not applicable for 132-LTS because there is no M132 branch on libaom repository and I'm not sure if this issue can happen on M132.

### ch...@google.com (2025-11-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### na...@gmail.com (2025-11-08)

Was this crash related to a device with my email address? Nasiyisrael2414@gmail.com is my email

## Bounty Award

> report of memory corruption in a sandboxed process / the renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/432035817)*
