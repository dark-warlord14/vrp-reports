# Compiled regexps execute incorrectly on function source strings

| Field | Value |
|-------|-------|
| **Issue ID** | [40084126](https://issues.chromium.org/issues/40084126) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Language |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2016-1688 |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ya...@chromium.org |
| **Created** | 2016-04-19 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36

Steps to reproduce the problem:
See the result of the following code snippet (or attached screenshots):
http://plnkr.co/edit/RFXffpqJRg3L6xoCAbIY?p=preview

What is the expected behavior?
Matching results should be the same

What went wrong?
Calling identical .match() second time results in "null"

Did this work before? Yes Chrome 49

Chrome version: 50.0.2661.75  Channel: stable
OS Version: 10.0
Flash Version: Shockwave Flash 21.0 r0

This regex code is used inside angular.js to extract function parameters for dependency injection.
This bug is causing a crash ("Aw, Snap!") on the real angular project. 
(see Crash ID 97878f1200000000 (d9c92400-5011-485c-a164-aa2544110381) )

## Attachments

- [Chrome_50.png](attachments/Chrome_50.png) (image/png, 132.9 KB)
- [Chrome_49.png](attachments/Chrome_49.png) (image/png, 158.1 KB)

## Timeline

### dp...@chromium.org (2016-04-19)

Yup.

[Monorail components: -Blink Blink>JavaScript]

### ha...@chromium.org (2016-04-20)

Maybe this is because of the RegExp customization hooks we shipped in M50?

[Monorail components: -Blink>JavaScript Blink>JavaScript>Language]

### ha...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### ya...@chromium.org (2016-04-20)

I can reproduce this with 50.0.2661.75 on the given test site.
However, if I copy the code into the console, it works just fine.

### ya...@chromium.org (2016-04-20)

I have a strong suspicion that this is the same bug as v8:4923.

### ya...@chromium.org (2016-04-20)

Reduced repro. Also just confirmed that the fix for v8:4923 fixes this issue as well.

https://bugs.chromium.org/p/v8/issues/detail?id=4923

### ya...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3518e492c0939759ae1a2623bbd606646ee172f1

commit 3518e492c0939759ae1a2623bbd606646ee172f1
Author: yangguo <yangguo@chromium.org>
Date: Wed Apr 20 13:55:20 2016

[regexp] do not assume short external strings have a minimum size.

Short external strings do not cache the resource data, and may be used
for compressible strings. The assumptions about their lengths is
invalid and may lead to oob reads.

R=jkummerow@chromium.org
BUG=v8:4923,chromium:604897
LOG=N

Review URL: https://codereview.chromium.org/1901573003

Cr-Commit-Position: refs/heads/master@{#35660}

[modify] https://crrev.com/3518e492c0939759ae1a2623bbd606646ee172f1/src/arm/code-stubs-arm.cc
[modify] https://crrev.com/3518e492c0939759ae1a2623bbd606646ee172f1/src/arm64/code-stubs-arm64.cc
[modify] https://crrev.com/3518e492c0939759ae1a2623bbd606646ee172f1/src/ia32/code-stubs-ia32.cc
[modify] https://crrev.com/3518e492c0939759ae1a2623bbd606646ee172f1/src/mips/code-stubs-mips.cc
[modify] https://crrev.com/3518e492c0939759ae1a2623bbd606646ee172f1/src/mips64/code-stubs-mips64.cc
[modify] https://crrev.com/3518e492c0939759ae1a2623bbd606646ee172f1/src/objects.h
[modify] https://crrev.com/3518e492c0939759ae1a2623bbd606646ee172f1/src/x64/code-stubs-x64.cc
[modify] https://crrev.com/3518e492c0939759ae1a2623bbd606646ee172f1/test/cctest/cctest.status
[modify] https://crrev.com/3518e492c0939759ae1a2623bbd606646ee172f1/test/cctest/test-regexp.cc


### ya...@chromium.org (2016-04-20)

This needs to be merged as soon as possible, once we have a mips64 port for the fix.

### ha...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### ha...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/7d8e279a7b11cb3c1cbeb424118a20210f9b8eea

commit 7d8e279a7b11cb3c1cbeb424118a20210f9b8eea
Author: bjaideep <bjaideep@ca.ibm.com>
Date: Wed Apr 20 16:52:36 2016

PPC: [regexp] do not assume short external strings have a minimum size.

Port 3518e492c0939759ae1a2623bbd606646ee172f1

Original commit message:

    Short external strings do not cache the resource data, and may be used
    for compressible strings. The assumptions about their lengths is
    invalid and may lead to oob reads.

R=yangguo@chromium.org, joransiu@ca.ibm.com, jyan@ca.ibm.com, michael_dawson@ca.ibm.com, mbrandy@us.ibm.com

BUG=v8:4923,chromium:604897
LOG=N

Review URL: https://codereview.chromium.org/1901593005

Cr-Commit-Position: refs/heads/master@{#35671}

[modify] https://crrev.com/7d8e279a7b11cb3c1cbeb424118a20210f9b8eea/src/ppc/code-stubs-ppc.cc


### cl...@chromium.org (2016-04-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### bu...@chromium.org (2016-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/14c9cbd4cfaa235801e0372178e8af039cb2233f

commit 14c9cbd4cfaa235801e0372178e8af039cb2233f
Author: jyan <jyan@ca.ibm.com>
Date: Thu Apr 21 05:02:43 2016

S390: [regexp] do not assume short external strings have a minimum size.

Port 3518e492c0939759ae1a2623bbd606646ee172f1

Original commit message:

    Short external strings do not cache the resource data, and may be used
    for compressible strings. The assumptions about their lengths is
    invalid and may lead to oob reads.

R=yangguo@chromium.org, joransiu@ca.ibm.com, bjaideep@ca.ibm.com, michael_dawson@ca.ibm.com, mbrandy@us.ibm.com

BUG=v8:4923,chromium:604897
LOG=N

Review URL: https://codereview.chromium.org/1911633002

Cr-Commit-Position: refs/heads/master@{#35682}

[modify] https://crrev.com/14c9cbd4cfaa235801e0372178e8af039cb2233f/src/s390/code-stubs-s390.cc


### bu...@chromium.org (2016-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/b4697727e946e8d96d5345a4db7ff72842d60466

commit b4697727e946e8d96d5345a4db7ff72842d60466
Author: yangguo <yangguo@chromium.org>
Date: Thu Apr 21 05:58:08 2016

MIPS64: [regexp] do not assume short external strings have a minimum size.

Port 3518e492c0939759ae1a2623bbd606646ee172f1

Original commit message:
    Short external strings do not cache the resource data, and may be used
    for compressible strings. The assumptions about their lengths is
    invalid and may lead to oob reads.

R=bmeurer@chromium.org
BUG=v8:4923,chromium:604897
LOG=N

Review URL: https://codereview.chromium.org/1902393004

Cr-Commit-Position: refs/heads/master@{#35683}

[modify] https://crrev.com/b4697727e946e8d96d5345a4db7ff72842d60466/src/mips64/code-stubs-mips64.cc
[modify] https://crrev.com/b4697727e946e8d96d5345a4db7ff72842d60466/test/cctest/cctest.status


### ya...@chromium.org (2016-04-21)

Patches to back merge:

3518e492c0939759ae1a2623bbd606646ee172f1 original patch (ia32, x64, arm, arm64, mips ports)
7d8e279a7b11cb3c1cbeb424118a20210f9b8eea ppc port
644bade748fafb1f2e8ab25ca33473a4c77c006d x87 port
b4697727e946e8d96d5345a4db7ff72842d60466 mips64 port
14c9cbd4cfaa235801e0372178e8af039cb2233f s390 port

The s390 port only needs to be merged to M51, since M50 does not include s390 support yet.

### cl...@chromium.org (2016-04-21)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-22)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### ti...@google.com (2016-04-22)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### ti...@google.com (2016-04-22)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### ya...@chromium.org (2016-04-22)

Another MIPS64 fix to include in the back merges: 71dd5c4380e191f0a4cd1d5b6b044bdf1c04f0f9

### ss...@google.com (2016-04-23)

Looks like there is ongoing work here. What are all these changes, and do we have a full list of what we want to merge into M51 yet? 

### ya...@chromium.org (2016-04-23)

The fix is dependent on CPU architecture, and while the initial fix covered 5 archs, the missing 4 were ported by their respective external maintainers. The last CL to fix the MIPS64 port should be the last one. I don't expect any further changes.

### ya...@chromium.org (2016-04-23)

The list of patches are in https://crbug.com/chromium/604897#c20 and 25.

### ss...@google.com (2016-04-25)

Merge approved for M51 (branch 2704)

### go...@chromium.org (2016-04-26)

Please merge your change before 5:00 PM PST tomorrow (Tuesday) to M51 branch 2704, so we can take it for this week beta. Thank you.

### bu...@chromium.org (2016-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d05748bc7964ac1f9e599406bf779f3a3bb4395e

commit d05748bc7964ac1f9e599406bf779f3a3bb4395e
Author: Yang Guo <yangguo@chromium.org>
Date: Tue Apr 26 12:42:20 2016

Version 5.1.281.18 (cherry-pick)

Merged 3518e492c0939759ae1a2623bbd606646ee172f1
Merged 7d8e279a7b11cb3c1cbeb424118a20210f9b8eea
Merged 644bade748fafb1f2e8ab25ca33473a4c77c006d
Merged b4697727e946e8d96d5345a4db7ff72842d60466
Merged 14c9cbd4cfaa235801e0372178e8af039cb2233f
Merged 71dd5c4380e191f0a4cd1d5b6b044bdf1c04f0f9

[regexp] do not assume short external strings have a minimum size.

PPC: [regexp] do not assume short external strings have a minimum size.

X87: [regexp] do not assume short external strings have a minimum size.

MIPS64: [regexp] do not assume short external strings have a minimum size.

S390: [regexp] do not assume short external strings have a minimum size.

MIPS64: [regexp] do not assume short external strings have a minimum size.

BUG=chromium:604897,chromium:604897,chromium:604897,chromium:604897,v8:4923,v8:4923,v8:4923,v8:4923
LOG=N
R=hablich@chromium.org

Review URL: https://codereview.chromium.org/1923523002 .

Cr-Commit-Position: refs/branch-heads/5.1@{#22}
Cr-Branched-From: 167dc63b4c9a1d0f0fe1b19af93644ac9a561e83-refs/heads/5.1.281@{#1}
Cr-Branched-From: 03953f52bd4a184983a551927c406be6489ef89b-refs/heads/master@{#35282}

[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/include/v8-version.h
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/arm/code-stubs-arm.cc
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/arm64/code-stubs-arm64.cc
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/ia32/code-stubs-ia32.cc
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/mips/code-stubs-mips.cc
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/mips64/code-stubs-mips64.cc
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/objects.h
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/ppc/code-stubs-ppc.cc
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/s390/code-stubs-s390.cc
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/x64/code-stubs-x64.cc
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/src/x87/code-stubs-x87.cc
[modify] https://crrev.com/d05748bc7964ac1f9e599406bf779f3a3bb4395e/test/cctest/test-regexp.cc


### go...@chromium.org (2016-04-26)

Per https://crbug.com/chromium/604897#c31, this is already merged to M51. So removing "Merge-Approved-51" label.

### go...@chromium.org (2016-04-26)

[Comment Deleted]

### ti...@google.com (2016-04-26)

Before we approve merge to M50, Could you please confirm whether this bug is baked and verified in Canary and Beta and safe to merge? 

### ya...@chromium.org (2016-04-27)

The original fixes on M52 has been getting coverage since Canary 2715, which seems to be stable wrt V8.

### ha...@chromium.org (2016-04-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/dfaec1393ed70c11e2b326e87cdca5630062abc6

commit dfaec1393ed70c11e2b326e87cdca5630062abc6
Author: Yang Guo <yangguo@chromium.org>
Date: Thu Apr 28 07:15:42 2016

Version 5.0.71.40 (cherry-pick)

Merged 3518e492c0939759ae1a2623bbd606646ee172f1
Merged 7d8e279a7b11cb3c1cbeb424118a20210f9b8eea
Merged 644bade748fafb1f2e8ab25ca33473a4c77c006d
Merged b4697727e946e8d96d5345a4db7ff72842d60466
Merged 71dd5c4380e191f0a4cd1d5b6b044bdf1c04f0f9

[regexp] do not assume short external strings have a minimum size.

PPC: [regexp] do not assume short external strings have a minimum size.

X87: [regexp] do not assume short external strings have a minimum size.

MIPS64: [regexp] do not assume short external strings have a minimum size.

MIPS64: [regexp] do not assume short external strings have a minimum size.

BUG=chromium:604897,chromium:604897,chromium:604897,v8:4923,v8:4923,v8:4923
LOG=N
R=hablich@chromium.org

Review URL: https://codereview.chromium.org/1927003003 .

Cr-Commit-Position: refs/branch-heads/5.0@{#47}
Cr-Branched-From: ad16e6c2cbd2c6b0f2e8ff944ac245561c682ac2-refs/heads/5.0.71@{#1}
Cr-Branched-From: bd9df50d75125ee2ad37b3d92c8f50f0a8b5f030-refs/heads/master@{#34215}

[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/include/v8-version.h
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/src/arm/code-stubs-arm.cc
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/src/arm64/code-stubs-arm64.cc
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/src/ia32/code-stubs-ia32.cc
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/src/mips/code-stubs-mips.cc
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/src/mips64/code-stubs-mips64.cc
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/src/objects.h
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/src/ppc/code-stubs-ppc.cc
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/src/x64/code-stubs-x64.cc
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/src/x87/code-stubs-x87.cc
[modify] https://crrev.com/dfaec1393ed70c11e2b326e87cdca5630062abc6/test/cctest/test-regexp.cc


### sh...@chromium.org (2016-05-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ya...@chromium.org (2016-05-02)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

Adding reward-topanel to consider this under Chrome's security reward program: https://www.google.com/about/appsecurity/chrome-rewards/



### ti...@google.com (2016-05-25)

Updating severity

### ti...@google.com (2016-05-25)

Thanks for reporting this issue. Our reward panel decided to award you $1,000 for this report. Congratulations!

We've credited you in our release notes as "Max Korenko": https://googlechromereleases.blogspot.com/2016/05/stable-channel-update_25.html - if you'd like to use a different name, please let me know.

Someone from our finance team will be in contact to collect details for payment within 7 days. If that doesn't happen, please either update this bug or contact me at timwillis@.

The CVE-ID for this issue is CVE-2016-1688. Usual boilerplate text below - let me know if you have any questions.

Thanks again for the report!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/604897?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/v8/4923]
[Monorail mergedwith: crbug.com/chromium/604797]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084126)*
