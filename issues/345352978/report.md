# libicu multiple vulnerabilities in lastate chromium

| Field | Value |
|-------|-------|
| **Issue ID** | [345352978](https://issues.chromium.org/issues/345352978) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Internationalization |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 125.0.0.0 |
| **Reporter** | pw...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2024-06-06 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

Chromium has not been patched for the vulnerabilities in libicu.

- bidi buffer overflow (<https://github.com/unicode-org/icu/pull/3016>)
- propagate error avoid overflow (<https://github.com/unicode-org/icu/pull/3007>)
- Remove format-overflow warning (<https://github.com/unicode-org/icu/pull/2989>)
- Japanese extended year int32 overflow (<https://github.com/unicode-org/icu/pull/2953>)

# Problem Description

Patches applied in ICU were not modified in chromium.

# Summary

libicu multiple vulnerabilities in lastate chromium

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Timeline

### ke...@chromium.org (2024-06-06)

Thanks for the report.

ftang@: You are already familiar with the reported issues. Can you comment on whether any of them are security vulnerabilities? (After a quick scan, the bidi issue stands out)

Is there a normal process for merging icu security-relevant fixes?

### pg...@google.com (2024-06-11)

Setting severity to match how version divergence bugs are usually triaged
Setting foundin based on the oldest PR merge date (April 11)

### pe...@google.com (2024-06-12)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-06-12)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-06-21)

ftang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ph...@chromium.org (2024-06-24)

[Secondary security shepherd] Pinged ftang@ in chat.

### ap...@google.com (2024-06-26)

Project: chromium/deps/icu
Branch: main

commit e0d7984526f7c2ac4297fc1a56ce2a5f5121a47f
Author: David Yeung <dayeung@chromium.org>
Date:   Wed Jun 26 09:14:43 2024

    Add upstream patch to fix a bidi buffer bug
    
    As this is a potential security issue, see bug for more details.
    
    Bug:345352978
    Change-Id: Ic6b714b8aa0e4a2d2eaf575d3006397714ce830e
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/5653447
    Reviewed-by: Shu-yu Guo <syg@chromium.org>

M       README.chromium
A       patches/bidi_buffer_overflow.patch
M       source/common/ubidiwrt.cpp

https://chromium-review.googlesource.com/5653447


### ap...@google.com (2024-06-26)

Project: chromium/deps/icu
Branch: main

commit 51b178d1e9c16599618cf76b0960eb76e740ce55
Author: David Yeung <dayeung@chromium.org>
Date:   Wed Jun 26 09:15:21 2024

    Add upstream patch to remove format-overflow warning
    
    See bug for more details.
    
    Bug:345352978
    Change-Id: I46c644c5319b09ee0ad099062631dc3e2123a4e4
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/5654974
    Reviewed-by: Shu-yu Guo <syg@chromium.org>

M       README.chromium
A       patches/remove_format_overflow_warning.patch
M       source/tools/pkgdata/pkgdata.cpp

https://chromium-review.googlesource.com/5654974


### ap...@google.com (2024-06-27)

Project: chromium/deps/icu
Branch: main

commit 25d61b388c14ce1eb659b14b4a21758d079851fd
Author: David Yeung <dayeung@chromium.org>
Date:   Wed Jun 26 09:15:23 2024

    Add upstream patch to fix ja extended year overflow bug
    
    See bug for more details.
    
    Bug:345352978
    Change-Id: I93dfd8738063416306a7c517dc8289e1940ee2ed
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/5654976
    Reviewed-by: Shu-yu Guo <syg@chromium.org>

M       README.chromium
A       patches/ja_extended_year_overflow.patch
M       source/i18n/japancal.cpp

https://chromium-review.googlesource.com/5654976


### ap...@google.com (2024-06-27)

Project: chromium/deps/icu
Branch: main

commit 9408c6fd4a39e6fef0e1c4077602e1c83b15f3fb
Author: David Yeung <dayeung@chromium.org>
Date:   Wed Jun 26 09:15:24 2024

    Add upstream patch to propagate tz error to avoid overflow
    
    See bug for more details.
    
    Bug:345352978
    Change-Id: Ia321d6ff5c30c7fbc1e641ec061bdeeebd59afd6
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/5660336
    Reviewed-by: Shu-yu Guo <syg@chromium.org>

M       README.chromium
A       patches/propagate_error_avoid_overflow.patch
M       source/i18n/basictz.cpp
M       source/i18n/calendar.cpp
M       source/i18n/erarules.cpp
M       source/i18n/gregoimp.cpp
M       source/i18n/gregoimp.h
M       source/i18n/indiancal.cpp
M       source/i18n/olsontz.cpp
M       source/i18n/simpletz.cpp
M       source/i18n/timezone.cpp
M       source/i18n/tzrule.cpp
M       source/i18n/vtzone.cpp

https://chromium-review.googlesource.com/5660336


### ap...@google.com (2024-06-28)

Project: chromium/src
Branch: main

commit 817b8a9a2896d8f79ee562a9ea1a35301adc951e
Author: David Yeung <dayeung@chromium.org>
Date:   Fri Jun 28 16:28:04 2024

    Roll ICU
    
    Bug: 345352978
    Change-Id: I9f229f5625b762e8ba65a55e3457694b5022cc41
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5659641
    Commit-Queue: David Yeung <dayeung@chromium.org>
    Reviewed-by: Shu-yu Guo <syg@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1321018}

M       DEPS
M       third_party/icu

https://chromium-review.googlesource.com/5659641


### pe...@google.com (2024-06-29)

Requesting merge to stable (M126) because latest trunk commit (1321018) appears to be after stable branch point (1300313).
Requesting merge to beta (M127) because latest trunk commit (1321018) appears to be after beta branch point (1313161).
Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### am...@chromium.org (2024-07-01)

We are presently in a release freeze, so there is limited Canary data for this lot of changes in the ICU roll. 
Because how / if these issues are exploitable in Chrome and the impact has not been presented, I'm declining backmerge to M126 Stable which will soon become Extended Stable support once M127 is promoted to Stable on 23 July. 
Based on the canary data and looking through the individual fixes, approving for merge to M127. Please merge to branch 6533 at your earliest availability so this fix can be included in the M127 Stable RC cut on 16 July and the final beta of M127 on 17 July. 

### ap...@google.com (2024-07-02)

Project: chromium/src
Branch: refs/branch-heads/6533

commit ffffec2d44226b3c09ae9d4591ce303d48fe400d
Author: David Yeung <dayeung@chromium.org>
Date:   Tue Jul 02 18:59:14 2024

    [M127] Roll ICU
    
    (cherry picked from commit 817b8a9a2896d8f79ee562a9ea1a35301adc951e)
    
    Bug: 345352978
    Change-Id: I9f229f5625b762e8ba65a55e3457694b5022cc41
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5659641
    Commit-Queue: David Yeung <dayeung@chromium.org>
    Reviewed-by: Shu-yu Guo <syg@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1321018}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5671926
    Reviewed-by: Shu-yu Guo <syg@google.com>
    Cr-Commit-Position: refs/branch-heads/6533@{#962}
    Cr-Branched-From: 7e0b87ec6b8cb5cb2969e1479fc25776e582721d-refs/heads/main@{#1313161}

M       DEPS
M       third_party/icu

https://chromium-review.googlesource.com/5671926


### pe...@google.com (2024-07-02)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### da...@chromium.org (2024-07-02)

Sounds good.

I've merged to M127 and sounds like we do not need this in M126.

### pe...@google.com (2024-07-03)

Setting milestone because of s0/s1 severity.

### sp...@google.com (2024-07-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for pointing out public upstream ICU vulnerabilities so that we could make a security relevant change.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-07-03)

Thank you again for this report. Since no demonstration, exploitability, or impact to users was presented here, but we were able to make a security-relevant change, we have extended a thank you reward for your efforts. Thank you for reporting this issue to us!

### rz...@google.com (2024-09-04)

Labelling as not applicable for LTS 120/126 (see [comment #17](https://issues.chromium.org/issues/345352978#comment17))

### pe...@google.com (2024-10-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/345352978)*
