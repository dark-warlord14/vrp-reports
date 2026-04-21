# Security: V8 SEGV_ACCERR 02b6beadbef2

| Field | Value |
|-------|-------|
| **Issue ID** | [40070055](https://issues.chromium.org/issues/40070055) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>GarbageCollection |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | dd...@gmail.com |
| **Assignee** | om...@chromium.org |
| **Created** | 2023-08-21 |
| **Bounty** | $5,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**

Received signal 11 SEGV\_ACCERR 02b6beadbef2

==== C stack trace ===============================

[0x55d2d25a4d42]  

[0x7f82b22c2980]  

[0x55d2d353d3fd]  

[0x55d2d2c97188]  

[0x55d2d2e02638]  

[0x55d2d2d48017]  

[0x55d2d2d3c813]  

[0x55d2d2d3bd2f]  

[0x55d2d2c74866]  

[0x55d2d2c704a4]  

[0x55d2d2c6c564]  

[0x55d2d2c6bb4f]  

[0x55d2d2b849ec]  

[0x55d2d3925361]  

[0x55d2d3924c52]  

[0x55d2d547c6b6]  

[end of stack trace]

**VERSION**  

commit 5301bd881bdc1364d527893fa7f182da0000ab90 (grafted, HEAD, origin/main)  

Author: Lu Yahan [yahan@iscas.ac.cn](mailto:yahan@iscas.ac.cn)  

Date: Fri Aug 18 10:55:24 2023 +0800

**REPRODUCTION CASE**  

build with

```
is_debug = false  
dcheck_always_on = true  
v8_static_library = true  
v8_enable_verify_heap = true  
v8_fuzzilli = true  
sanitizer_coverage_flags = "trace-pc-guard"  
target_cpu = "x64"  

```

and run with

```
--expose-gc --omit-quit --allow-natives-syntax --fuzzing --jit-fuzzing --future --js-staging --shared-string-table --minor-ms  

```

it is not stable need multi run to trigger

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 421 B)
- [poc.js](attachments/poc.js) (text/plain, 686 B)

## Timeline

### [Deleted User] (2023-08-21)

[Empty comment from Monorail migration]

### dd...@gmail.com (2023-08-21)

another poc without syntax error. my fuzzer found it third time in one day, so I think it is not a false positive.

### cl...@chromium.org (2023-08-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4990088414691328.

### cl...@chromium.org (2023-08-21)

Testcase 4990088414691328 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=4990088414691328.

### jd...@chromium.org (2023-08-21)

An unsymbolized stack trace that I can't reproduce isn't much to go on, and I'm skeptical whether this is a real bug. That said, I'm pushing this over to the v8 sheriff to take a closer look.

saelo@: can you try to dig into this a bit? I set the severity and foundin labels very aggressively and they're very provisional. Thanks!

[Monorail components: Blink>JavaScript]

### [Deleted User] (2023-08-21)

[Empty comment from Monorail migration]

### dd...@gmail.com (2023-08-21)

I will try to get symbolized stack trace. The reproduce need run multi d8 instance in same time, I guess.

### dd...@gmail.com (2023-08-22)

[Comment Deleted]

### dd...@gmail.com (2023-08-22)

deleted

### [Deleted User] (2023-08-22)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sa...@google.com (2023-08-23)

Thanks! I can repro this locally on a regular x64.optdebug build (haven't managed on a debug build or an ASan build though, probably just due to different timing). The machine I was testing this on was under fairly heavy CPU load, which might have an impact. A slightly simpler testcase and fewer flags work for me as well:

    new Float64Array(3853);
    new Uint16Array(6);
    const v8 = new Int8Array(255);
    v8.lastIndexOf(10);
    new Int16Array(819);
    function f14(a15) {
        for (let i17 = 0; i17 < 10000; i17++) {
            new Float32Array(i17);
        }
    }
    const o27 = {
        "type": "function",
    };
    new Worker(f14, o27);
    f14();
    for (let i31 = 0; i31 < 10000; ++i31) {
        isNaN(-Infinity);
    }
    f14(Int8Array);

And only --shared-string-table --minor-ms seems to be enough.

Interestingly, I've never seen it crash without both --shared-string-table and --minor-ms. So maybe the shared heap is necessary to trigger the bug, or it could just affect the timing of other things... 

I will try to bisect this, but I'm not sure it'll work since the testcase is quite unreliable.
Omer, does the stacktrace + sample by any chance already give you an idea of what might be going wrong here?

[Monorail components: Blink>JavaScript>GarbageCollection]

### sa...@google.com (2023-08-24)

Ok I managed to bisect it locally and it bisects to 852ffa43b38caa0594664dcfc593a598b3a69d29 "[heap] Fix bug in allocated lab size accounting" with fairly high confidence. It then needs --minor-mc though (this was before the rename from --minor-mc to --minor-ms). Omer, can you take a look?

### om...@chromium.org (2023-08-29)

I have an idea what could be going on here.
I'm trying to reproduce the crash so that I can confirm my suspicion.

### gi...@appspot.gserviceaccount.com (2023-08-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e420a2de3eea8ed9ce672fac8d54787f7adc35d2

commit e420a2de3eea8ed9ce672fac8d54787f7adc35d2
Author: Omer Katz <omerkatz@chromium.org>
Date: Tue Aug 29 14:04:46 2023

[heap] Fix MakeLinearAllocationAreaIterable for lab extensions

Usually when a LAB is allocated, we compute a limit for it and free the
remaining free space back to the free list.
PagedNewSpace supports LAB "extensions" by not freeing the memory and
instead keeping it allocated such that it could be used later without
going through the freelist again.

Making LAB iterable ignored that extra memory (between `limit()` and
`original_limit_relaxed()`) which meant that in some cases (e.g. when
`top() == limit()` when a client isolate tries to GC due to allocation
failure) calling `MakeLinearAllocationAreaIterable` would not create a
filler. If a shared GC happened during that time, the main isolate would
iterate the client isolate's new space and get lost because the LAB was
missing a filler.

Bug: chromium:1474285
Change-Id: I82c22c8ece6e515a5ef04a99bbfe81e6d2ea29b7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4822566
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Omer Katz <omerkatz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#89682}

[modify] https://crrev.com/e420a2de3eea8ed9ce672fac8d54787f7adc35d2/src/heap/paged-spaces.cc


### om...@chromium.org (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-29)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M117. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2023-08-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-30)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1474285&entry.364066060=External&entry.958145677=Android&entry.958145677=Chrome&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript,Blink>JavaScript>GarbageCollection&entry.975983575=omerkatz@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### om...@chromium.org (2023-08-30)

This bug requires both --minor-ms and --shared-string-table to reproduce. Both are disabled by default and not yet used in production.
Updating impact to none and removing merge requests.

### am...@chromium.org (2023-09-05)

Thank you for the report. This issue appears to be specific to V8 features behind the V8 --experimental flag and are not eligible for a VRP reward. 

### dd...@gmail.com (2023-09-05)

deleted

### am...@chromium.org (2023-09-05)

>>>I have not use experimental flag, and this is cf wrong.
you don't have to run the experimental flag itself or a feature to be behind experimental. Clusterfuzz showing experimental is by design and helps expose when a feature / flag is part of experimental feature sets and that bugs (even security bugs) may be expected

>>>seal will turn off this bug before, right?
Sorry, I don't think I'm following here



### dd...@gmail.com (2023-09-05)

deleted

### dd...@gmail.com (2023-09-05)

deleted

### dd...@gmail.com (2023-09-06)

deleted

### am...@chromium.org (2023-09-06)

Apologies, it appears some things are being conflated. 
Yes, Clusterfuzz will assert that the experimental configuration is being used if one or more flag is specific to the experimental configuration is enabled, as you mentioned. However, my assertion was not related to the CF results above and the flags you list in c#28, but specifically the mention of this issue requiring --shared-string-table and --minor-ms. I was however, incorrect and --shared-string-table is no longer experimental. Apologies for that. 
However, I believe that --minor-ms is as it seems to be yoked to heap / GC efforts that are experimental. I will further look into this tomorrow and update here accordingly.

### dd...@gmail.com (2023-09-06)

deleted

### dd...@gmail.com (2023-09-08)

friendly ping : )

### va...@chromium.org (2023-09-11)

[Empty comment from Monorail migration]

### sa...@google.com (2023-09-11)

Clusterfuzz never managed to reproduce this, I only did that locally, and it only needed --shared-string-table --minor-ms (see https://crbug.com/chromium/1474285#c12), and neither of these flags is marked as experimental.
In any case, Cluterfuzz shouldn't mark this as experimental, I've filed a bug for that: https://crbug.com/1480957

### am...@chromium.org (2023-09-11)

Thanks so much for confirming as well filing the bug for clusterfuzz. 
Updating this issue to return it to the panel queue. 

### dd...@gmail.com (2023-09-11)

Thank you Amy and saelo :)

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. The reward amount was based on this report lacking some of the key characteristics to consider this a baseline quality report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us. 

### dd...@gmail.com (2023-09-15)

deleted

### am...@chromium.org (2023-09-16)

Hello, thanks for your question. We always expect a fully symbolized stack trace and also the full stack should be provided. 
Work had to also be performed by the V8 security team to adjust the POC in order for it to be reproducible. 
Providing these details early in the reporting process is essential in providing clear evidence of a security issue and ensuring that we can effectively and correctly triage the bug. 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### dd...@gmail.com (2023-09-20)

deleted

### [Deleted User] (2023-12-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-12-05)

This issue was migrated from crbug.com/chromium/1474285?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>GarbageCollection]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40070055)*
