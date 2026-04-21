# Stack-buffer-overflow in icu_59::NumberingSystem::createInstance

| Field | Value |
|-------|-------|
| **Issue ID** | [40089169](https://issues.chromium.org/issues/40089169) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sc...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-09-30 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS
length of buffer on stack is ULOC_KEYWORDS_CAPACITY(96), but was filled with ULOC_KEYWORD_AND_VALUES_CAPACITY(100) bytes

```cpp
//uloc.h
#define ULOC_KEYWORDS_CAPACITY 96
#define ULOC_KEYWORD_AND_VALUES_CAPACITY 100

//uloc.cpp
U_CAPI int32_t U_EXPORT2
uloc_getKeywordValue(const char* localeID,
                     const char* keywordName,
                     char* buffer, int32_t bufferCapacity,
                     UErrorCode* status)
953:
              result = u_terminateChars(buffer, bufferCapacity, keyValueLen, status);


//uloc_tag.cpp
U_CAPI int32_t U_EXPORT2
uloc_toLanguageTag(const char* localeID,
                   char* langtag,
                   int32_t langtagCapacity,
                   UBool strict,
                   UErrorCode* status) {
2371:
                    char buf[ULOC_KEYWORD_AND_VALUES_CAPACITY];
                    buf[0] = PRIVATEUSE;
                    buf[1] = SEP;
                    len = uloc_getKeywordValue(localeID, key, &buf[2], sizeof(buf) - 2, &tmpStatus);


//numsys.cpp
NumberingSystem* U_EXPORT2
NumberingSystem::createInstance(const Locale & inLocale, UErrorCode& status) {

    if (U_FAILURE(status)) {
        return NULL;
    }

    UBool nsResolved = TRUE;
    UBool usingFallback = FALSE;
    char buffer[ULOC_KEYWORDS_CAPACITY];
    int32_t count = inLocale.getKeywordValue("numbers",buffer, sizeof(buffer),status);
    if ( count > 0 ) { // @numbers keyword was specified in the locale
        buffer[count] = '\0'; // Make sure it is null terminated.
        if ( !uprv_strcmp(buffer,gDefault) || !uprv_strcmp(buffer,gNative) || 
             !uprv_strcmp(buffer,gTraditional) || !uprv_strcmp(buffer,gFinance)) {
            nsResolved = FALSE;
        }
    } else {
        uprv_strcpy(buffer,gDefault);
        nsResolved = FALSE;
    }

VERSION
Version 60.0.3112.113 (Official Build) (64-bit)
Operating System: [Mac OS, 10.12.6]

REPRODUCTION CASE
var number = 5.0260805378947765e+223;
var nf = new Intl.NumberFormat('bs-u-nu-bzcu-cab-cabs-avnlubs-avnihu-zcu-cab-cbs-avnllubs-avnihq-zcu-cab-cbs-ubs-avnihu-cabs-flus-xxd-vnluy');
var f = nf.format(number);


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION



## Attachments

- [poc.js](attachments/poc.js) (text/plain, 208 B)
- [crash.log](attachments/crash.log) (text/plain, 5.8 KB)
- [patch.diff](attachments/patch.diff) (application/octet-stream, 322 B)

## Timeline

### cl...@chromium.org (2017-09-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4745958029262848.

### cl...@chromium.org (2017-09-30)

Detailed report: https://clusterfuzz.com/testcase?key=4745958029262848

Job Type: linux_asan_d8_dbg
Crash Type: Stack-buffer-overflow WRITE 1
Crash Address: 0x7f753f07b283
Crash State:
  icu_59::NumberingSystem::createInstance
  icu_59::NumberFormat::makeInstance
  icu_59::NumberFormat::makeInstance
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=38691:38692

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4745958029262848

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### in...@chromium.org (2017-09-30)

Regression from https://chromium.googlesource.com/v8/v8/+/339f08d2e9650e05d63c6a756b8302c60ee665b5

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2017-10-01)

Automatically applying components based on information from OWNERS files. If this seems incorrect, please apply the Test-Predator-Wrong-Components label.

### sh...@chromium.org (2017-10-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2017-10-02)

Please add appropriate OSs.

### go...@chromium.org (2017-10-02)

[Comment Deleted]

### sh...@chromium.org (2017-10-03)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2017-10-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-10-05)

Thanks a lot for the report. 

It should check |status| like this:

       int32_t len;
        char collVal[ULOC_KEYWORDS_CAPACITY];
        char tmpLocaleID[ULOC_FULLNAME_CAPACITY];

        len = uloc_getKeywordValue(localeID, "collation", collVal,
            UPRV_LENGTHOF(collVal) - 1, &status);

        if (U_SUCCESS(status) && len > 0) {
            collVal[len] = 0;

I'll prepare a CL.

### sh...@chromium.org (2017-10-06)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-10-06)

For this particular issue, I'll take an upstream fix (in ToT; http://bugs.icu-project.org/trac/changeset/40494 ) instead of mine to make it simpler to merge later. 

I identified similar issues in a few other places. I also have a patch for them. 

I filed an upstream bug (http://bugs.icu-project.org/trac/ticket/13394 : it's not-public, though) with more of my findings. 



### js...@chromium.org (2017-10-06)

A CL is up at https://chromium-review.googlesource.com/#/c/chromium/deps/icu/+/705920 (it's private) 
taking care of other callers of uloc_getKeywordValue as well as the one in numsys.cpp . 

 


### js...@chromium.org (2017-10-06)

I confirmed that the above CL takes care of the reported case. 
Without that, I can reproduce while with the CL applied, I can't reproduce it. 


### js...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu.git/+/7f873c45c23fa1baf1a1d90f449c5c4c34bd8ba6

commit 7f873c45c23fa1baf1a1d90f449c5c4c34bd8ba6
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Oct 10 17:50:52 2017

Clean up the callers of uloc_getKeywordValue()

Bug:770452
Test: See the bug

Change-Id: I5e19012a57507393670d68a7228bdb0831918997
Reviewed-on: https://chromium-review.googlesource.com/705920
Reviewed-by: Mark Mentovai <mark@chromium.org>

[modify] https://crrev.com/7f873c45c23fa1baf1a1d90f449c5c4c34bd8ba6/README.chromium
[add] https://crrev.com/7f873c45c23fa1baf1a1d90f449c5c4c34bd8ba6/patches/loc_keyvalue.patch
[modify] https://crrev.com/7f873c45c23fa1baf1a1d90f449c5c4c34bd8ba6/source/common/locdispnames.cpp
[modify] https://crrev.com/7f873c45c23fa1baf1a1d90f449c5c4c34bd8ba6/source/common/locdspnm.cpp
[modify] https://crrev.com/7f873c45c23fa1baf1a1d90f449c5c4c34bd8ba6/source/i18n/numsys.cpp
[modify] https://crrev.com/7f873c45c23fa1baf1a1d90f449c5c4c34bd8ba6/source/i18n/ucol_sit.cpp


### js...@chromium.org (2017-10-10)

This bug is present in M62 branch as well (and earlier branch all the way to August, 2016). 

inferno@ seems to have misread the year in the following CL to be 2017 instead of 2016. :-) 

https://chromium.googlesource.com/v8/v8/+/339f08d2e9650e05d63c6a756b8302c60ee665b5



### bu...@chromium.org (2017-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/99d3c8f639b6ea5fb4e7931547c95cfc79b33d48

commit 99d3c8f639b6ea5fb4e7931547c95cfc79b33d48
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Oct 10 20:10:57 2017

Roll ICU to 7f873c45

There's only one change in the roll.

 https://chromium.googlesource.com/chromium/deps/icu/+log/08cb9568..7f873c45

TBR=mark@chromium.org

Bug: 770452
Test: See the bug
Change-Id: I6e9c1b8a7e0d2f013517402e7cd7dd434f398b27
Reviewed-on: https://chromium-review.googlesource.com/709939
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#507752}
[modify] https://crrev.com/99d3c8f639b6ea5fb4e7931547c95cfc79b33d48/DEPS


### js...@chromium.org (2017-10-10)

Fixed in ToT. 

will leave it open for me to get to this bug quickly to request for merge after a couple of days baking in canary. 


### js...@chromium.org (2017-10-10)

Will add a test to v8 so that we won't regress (asan bot should catch it if we regress). 



### sh...@chromium.org (2017-10-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/69bd294affaf0dd567d8649f5c02e891473f3e1f

commit 69bd294affaf0dd567d8649f5c02e891473f3e1f
Author: Jungshik Shin <jshin@chromium.org>
Date: Thu Oct 12 06:33:35 2017

Correct the misuse of uloc_{to,from}LanguageTag

- remove unused Runtime_GetLanguageTagVariants
- add test for another related bug (chromium:770452) as well as for 
chromium:770450 . 

Bug: chromium:770450, chromium:770452
Test: intl/general/invalid-locale.js
Cq-Include-Trybots: master.tryserver.v8:v8_linux_noi18n_rel_ng
Change-Id: I4496a4a5421000faa0e37aed85fea21ceb487998
Reviewed-on: https://chromium-review.googlesource.com/710816
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#48483}
[modify] https://crrev.com/69bd294affaf0dd567d8649f5c02e891473f3e1f/src/runtime/runtime-intl.cc
[modify] https://crrev.com/69bd294affaf0dd567d8649f5c02e891473f3e1f/src/runtime/runtime.h
[add] https://crrev.com/69bd294affaf0dd567d8649f5c02e891473f3e1f/test/intl/general/invalid-locale.js


### cl...@chromium.org (2017-10-12)

ClusterFuzz has detected this issue as fixed in range 48480:48481.

Detailed report: https://clusterfuzz.com/testcase?key=4745958029262848

Job Type: linux_asan_d8_dbg
Crash Type: Stack-buffer-overflow WRITE 1
Crash Address: 0x7f753f07b283
Crash State:
  icu_59::NumberingSystem::createInstance
  icu_59::NumberFormat::makeInstance
  icu_59::NumberFormat::makeInstance
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=38691:38692
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=48480:48481

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4745958029262848

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-10-12)

ClusterFuzz testcase 4745958029262848 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-10-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-10-13)

A change in https://crbug.com/chromium/770452#c19 is safe and simple. Asking for merge-approval to M-62. 

If my request for merge to M62 for https://crbug.com/chromium/754053 is also approved, I'll roll ICU to include the fixes for both this and https://crbug.com/chromium/754053. If not, I'll just roll ICU to include the fix for this CL. 



### sh...@chromium.org (2017-10-13)

This bug requires manual review: We are only 3 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-10-13)

Safe and simple merge, tested in canary. Approving for merge: branch:3202

### bu...@chromium.org (2017-10-14)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/2e5dc2d3a0ce32be86b4ff68a7f6e78ee273106c

commit 2e5dc2d3a0ce32be86b4ff68a7f6e78ee273106c
Author: Jungshik Shin <jungshik@google.com>
Date: Sat Oct 14 05:32:24 2017


### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/593b0d895d9adea24ab0a0a51d8a5e891485674c

commit 593b0d895d9adea24ab0a0a51d8a5e891485674c
Author: Jungshik Shin <jshin@chromium.org>
Date: Mon Oct 16 20:56:39 2017

Merged: Correct the misuse of uloc_{to,from}LanguageTag

Revision: 69bd294affaf0dd567d8649f5c02e891473f3e1f

Merge to 6.3 branch

- remove unused Runtime_GetLanguageTagVariants
- add test for another related bug (chromium:770452) as well as for
chromium:770450 .

BUG=chromium:770450,chromium:770452
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=adamk@chromium.org

Cq-Include-Trybots: master.tryserver.v8:v8_linux_noi18n_rel_ng
Change-Id: Ia2c6dd2156c51995fb18228fc3062a86e78d719c
Reviewed-on: https://chromium-review.googlesource.com/721844
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.3@{#9}
Cr-Branched-From: 094a7c93dcdcd921de3883ba4674b7e1a0feffbe-refs/heads/6.3.292@{#1}
Cr-Branched-From: 18b8fbb528a8021e04a029e06eafee50b918bce0-refs/heads/master@{#48432}
[modify] https://crrev.com/593b0d895d9adea24ab0a0a51d8a5e891485674c/src/runtime/runtime-intl.cc
[modify] https://crrev.com/593b0d895d9adea24ab0a0a51d8a5e891485674c/src/runtime/runtime.h
[add] https://crrev.com/593b0d895d9adea24ab0a0a51d8a5e891485674c/test/intl/general/invalid-locale.js


### js...@chromium.org (2017-10-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/9a132a9e7208a042a4c7cc2b71248573f74a4e3e

commit 9a132a9e7208a042a4c7cc2b71248573f74a4e3e
Author: Michael Hablich <hablich@chromium.org>
Date: Tue Oct 17 16:10:36 2017

Revert "Merged: Correct the misuse of uloc_{to,from}LanguageTag"

This reverts commit 593b0d895d9adea24ab0a0a51d8a5e891485674c.

Reason for revert: broke some branch builders like https://build.chromium.org/p/client.v8.branches/builders/V8%20arm%20-%20sim%20-%20beta%20branch%20-%20debug

Original change's description:
> Merged: Correct the misuse of uloc_{to,from}LanguageTag
> 
> Revision: 69bd294affaf0dd567d8649f5c02e891473f3e1f
> 
> Merge to 6.3 branch
> 
> - remove unused Runtime_GetLanguageTagVariants
> - add test for another related bug (chromium:770452) as well as for
> chromium:770450 .
> 
> BUG=chromium:770450,chromium:770452
> LOG=N
> NOTRY=true
> NOPRESUBMIT=true
> NOTREECHECKS=true
> R=​adamk@chromium.org
> 
> Cq-Include-Trybots: master.tryserver.v8:v8_linux_noi18n_rel_ng
> Change-Id: Ia2c6dd2156c51995fb18228fc3062a86e78d719c
> Reviewed-on: https://chromium-review.googlesource.com/721844
> Reviewed-by: Adam Klein <adamk@chromium.org>
> Commit-Queue: Jungshik Shin <jshin@chromium.org>
> Cr-Commit-Position: refs/branch-heads/6.3@{#9}
> Cr-Branched-From: 094a7c93dcdcd921de3883ba4674b7e1a0feffbe-refs/heads/6.3.292@{#1}
> Cr-Branched-From: 18b8fbb528a8021e04a029e06eafee50b918bce0-refs/heads/master@{#48432}

TBR=adamk@chromium.org,hablich@chromium.org,jshin@chromium.org

Change-Id: I37018f8241efe1431f453ff55cf8216a5daa66de
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:770450, chromium:770452
Cq-Include-Trybots: master.tryserver.v8:v8_linux_noi18n_rel_ng
Reviewed-on: https://chromium-review.googlesource.com/723323
Reviewed-by: Michael Hablich <hablich@chromium.org>
Commit-Queue: Michael Hablich <hablich@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.3@{#17}
Cr-Branched-From: 094a7c93dcdcd921de3883ba4674b7e1a0feffbe-refs/heads/6.3.292@{#1}
Cr-Branched-From: 18b8fbb528a8021e04a029e06eafee50b918bce0-refs/heads/master@{#48432}
[modify] https://crrev.com/9a132a9e7208a042a4c7cc2b71248573f74a4e3e/src/runtime/runtime-intl.cc
[modify] https://crrev.com/9a132a9e7208a042a4c7cc2b71248573f74a4e3e/src/runtime/runtime.h
[delete] https://crrev.com/f435a180d199eda0c6777be153aa0ca5541ef599/test/intl/general/invalid-locale.js


### bu...@chromium.org (2017-10-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/bb1e70a61fbf93488ce9e4e6e943e549732ed65d

commit bb1e70a61fbf93488ce9e4e6e943e549732ed65d
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Oct 17 20:58:47 2017

Revert "Revert "Merged: Correct the misuse of uloc_{to,from}LanguageTag""

This reverts commit 9a132a9e7208a042a4c7cc2b71248573f74a4e3e.

Reason for revert: ICU was not rolled in 6.3 branch leading invalid-locale test failure (that was added to test an ICU fix). Now, ICU is rolled in 6.3 branch ( https://chromium-review.googlesource.com/c/v8/v8/+/723564 ). 


Original change's description:
> Revert "Merged: Correct the misuse of uloc_{to,from}LanguageTag"
> 
> This reverts commit 593b0d895d9adea24ab0a0a51d8a5e891485674c.
> 
> Reason for revert: broke some branch builders like https://build.chromium.org/p/client.v8.branches/builders/V8%20arm%20-%20sim%20-%20beta%20branch%20-%20debug
> 
> Original change's description:
> > Merged: Correct the misuse of uloc_{to,from}LanguageTag
> > 
> > Revision: 69bd294affaf0dd567d8649f5c02e891473f3e1f
> > 
> > Merge to 6.3 branch
> > 
> > - remove unused Runtime_GetLanguageTagVariants
> > - add test for another related bug (chromium:770452) as well as for
> > chromium:770450 .
> > 
> > BUG=chromium:770450,chromium:770452
> > LOG=N
> > NOTRY=true
> > NOPRESUBMIT=true
> > NOTREECHECKS=true
> > R=​adamk@chromium.org
> > 
> > Cq-Include-Trybots: master.tryserver.v8:v8_linux_noi18n_rel_ng
> > Change-Id: Ia2c6dd2156c51995fb18228fc3062a86e78d719c
> > Reviewed-on: https://chromium-review.googlesource.com/721844
> > Reviewed-by: Adam Klein <adamk@chromium.org>
> > Commit-Queue: Jungshik Shin <jshin@chromium.org>
> > Cr-Commit-Position: refs/branch-heads/6.3@{#9}
> > Cr-Branched-From: 094a7c93dcdcd921de3883ba4674b7e1a0feffbe-refs/heads/6.3.292@{#1}
> > Cr-Branched-From: 18b8fbb528a8021e04a029e06eafee50b918bce0-refs/heads/master@{#48432}
> 
> TBR=adamk@chromium.org,hablich@chromium.org,jshin@chromium.org
> 
> Change-Id: I37018f8241efe1431f453ff55cf8216a5daa66de
> No-Presubmit: true
> No-Tree-Checks: true
> No-Try: true
> Bug: chromium:770450, chromium:770452
> Cq-Include-Trybots: master.tryserver.v8:v8_linux_noi18n_rel_ng
> Reviewed-on: https://chromium-review.googlesource.com/723323
> Reviewed-by: Michael Hablich <hablich@chromium.org>
> Commit-Queue: Michael Hablich <hablich@chromium.org>
> Cr-Commit-Position: refs/branch-heads/6.3@{#17}
> Cr-Branched-From: 094a7c93dcdcd921de3883ba4674b7e1a0feffbe-refs/heads/6.3.292@{#1}
> Cr-Branched-From: 18b8fbb528a8021e04a029e06eafee50b918bce0-refs/heads/master@{#48432}

TBR=adamk@chromium.org,hablich@chromium.org,jshin@chromium.org

Change-Id: Ie7eac96859c8053c4f1b41b0a9b4f79a44883295
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:770450, chromium:770452
Cq-Include-Trybots: master.tryserver.v8:v8_linux_noi18n_rel_ng
Reviewed-on: https://chromium-review.googlesource.com/723608
Reviewed-by: Michael Hablich <hablich@chromium.org>
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.3@{#23}
Cr-Branched-From: 094a7c93dcdcd921de3883ba4674b7e1a0feffbe-refs/heads/6.3.292@{#1}
Cr-Branched-From: 18b8fbb528a8021e04a029e06eafee50b918bce0-refs/heads/master@{#48432}
[modify] https://crrev.com/bb1e70a61fbf93488ce9e4e6e943e549732ed65d/src/runtime/runtime-intl.cc
[modify] https://crrev.com/bb1e70a61fbf93488ce9e4e6e943e549732ed65d/src/runtime/runtime.h
[add] https://crrev.com/bb1e70a61fbf93488ce9e4e6e943e549732ed65d/test/intl/general/invalid-locale.js


### aw...@chromium.org (2017-10-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-20)

Congratulations scdengyuan@! The Chrome VRP panel has decided to reward $3,000 for this report.  A member of our finance team will be in touch shortly to arrange the details.

### aw...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/dad541bf46354b0ce2cf40b9419673f5edc3564a

commit dad541bf46354b0ce2cf40b9419673f5edc3564a
Author: Jungshik Shin <jshin@chromium.org>
Date: Tue Oct 24 20:45:07 2017

Merged: Correct the misuse of uloc_{to,from}LanguageTag

Merge to 6.2 branch

Revision: 69bd294affaf0dd567d8649f5c02e891473f3e1f

In addition, roll ICU to  21d33b1a09

There are only two changes in the roll. This is to match
Chromium M62's ICU in v8's 6.2 branch

 https://chromium.googlesource.com/chromium/deps/icu/+log/08cb9568..21d33b1a

BUG=chromium:770450,chromium:770452
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=hablich@chromium.org

Cq-Include-Trybots: master.tryserver.v8:v8_linux_noi18n_rel_ng
Change-Id: I79123ff567b822dc9afd9f1a4ebd007353033d8a
Reviewed-on: https://chromium-review.googlesource.com/736032
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.2@{#70}
Cr-Branched-From: efa2ac4129d30c7c72e84c16af3d20b44829f990-refs/heads/6.2.414@{#1}
Cr-Branched-From: a861ebb762a60bf5cc2a274faee3620abfb06311-refs/heads/master@{#47693}
[modify] https://crrev.com/dad541bf46354b0ce2cf40b9419673f5edc3564a/DEPS
[modify] https://crrev.com/dad541bf46354b0ce2cf40b9419673f5edc3564a/src/runtime/runtime-intl.cc
[modify] https://crrev.com/dad541bf46354b0ce2cf40b9419673f5edc3564a/src/runtime/runtime.h
[add] https://crrev.com/dad541bf46354b0ce2cf40b9419673f5edc3564a/test/intl/general/invalid-locale.js


### sc...@gmail.com (2017-10-26)

thx @awhalley, that's great

### aw...@google.com (2017-10-26)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2017-10-27)

hi, @awhalley, the credit here(https://chromereleases.googleblog.com/2017/10/stable-channel-update-for-desktop_26.html) has a mistake, can you plz rename the credit to "Yuan Deng of Ant-financial Light-Year Security Lab" ?

### mb...@chromium.org (2017-11-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### of...@google.com (2018-03-06)

Node.js back-port triage: I don't think this is needed for supported versions of Node.

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/770452?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089169)*
