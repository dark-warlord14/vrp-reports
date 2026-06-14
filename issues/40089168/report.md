# Stack-buffer-overflow in Runtime_CanonicalizeLanguageTag

| Field | Value |
|-------|-------|
| **Issue ID** | [40089168](https://issues.chromium.org/issues/40089168) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sc...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2017-09-30 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
//uloc_tag.cpp


2412:
uloc_forLanguageTag(const char* langtag,
                    char* localeID,
                    int32_t localeIDCapacity,
                    int32_t* parsedLength,
                    UErrorCode* status) {
2524:
        len = _appendKeywords(lt, localeID + reslen, localeIDCapacity - reslen, status); // integer overflow
        
_appendKeywords(ULanguageTag* langtag, char* appendAt, int32_t capacity, UErrorCode* status) {
    int32_t kwdBufLength = capacity;
1519:
    kwdBuf = (char*)uprv_malloc(kwdBufLength);

VERSION
Version 60.0.3112.113 (Official Build) (64-bit)
Operating System: [Mac OS, 10.12.6]

REPRODUCTION CASE
var date0 = new Date('1995-12-17T03:24:00');
var dateti1 = new Intl.DateTimeFormat("iw-up-a-caiaup-araup-ai-pdu-sp-bs-up-arscna-zeieiaup-araup-arscia-rews-us-up-arscna-zeieiaup-araup-arsciap-arscna-zeieiaup-araup-arscie-u-sp-bs-uaup-arscia");
d = dateti1.format(date0);



FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
$ ~/v8/out/Debug/d8 poc.js
=================================================================
==30991==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffd3d946acd at pc 0x0000004343c4 bp 0x7ffd3d9464d0 sp 0x7ffd3d945c78
READ of size 159 at 0x7ffd3d946acd thread T0
    #0 0x4343c3 in __interceptor_strlen (/home/scdeny/v8/out/Debug/d8+0x4343c3)
    #1 0x41262ea in uloc_toLanguageTag_59 /home/scdeny/v8/out/Debug/../../third_party/icu/source/common/uloc_tag.cpp:2347:9
    #2 0x3804793 in v8::internal::__RT_impl_Runtime_CanonicalizeLanguageTag(v8::internal::Arguments, v8::internal::Isolate*) /home/scdeny/v8/out/Debug/../../src/runtime/runtime-intl.cc:85:3
    #3 0x3803886 in v8::internal::Runtime_CanonicalizeLanguageTag(int, v8::internal::Object**, v8::internal::Isolate*) /home/scdeny/v8/out/Debug/../../src/runtime/runtime-intl.cc:58:1
    #4 0x7f071adced7e  (<unknown module>)

Address 0x7ffd3d946acd is located in stack of thread T0 at offset 461 in frame
    #0 0x3803def in v8::internal::__RT_impl_Runtime_CanonicalizeLanguageTag(v8::internal::Arguments, v8::internal::Isolate*) /home/scdeny/v8/out/Debug/../../src/runtime/runtime-intl.cc:58

  This frame has 14 object(s):
    [32, 48) 'args'
    [64, 88) 'scope' (line 59)
    [128, 136) 'locale_id_str' (line 63)
    [160, 176) 'locale_id' (line 65)
    [192, 200) 'agg.tmp'
    [224, 232) 'agg.tmp15'
    [256, 264) 'agg.tmp16'
    [288, 292) 'error' (line 72)
    [304, 461) 'icu_result' (line 73)
    [528, 532) 'icu_length' (line 74) <== Memory access at offset 461 partially underflows this variable
    [544, 552) 'coerce' <== Memory access at offset 461 partially underflows this variable
    [576, 733) 'result' (line 82) <== Memory access at offset 461 partially underflows this variable
    [800, 808) 'coerce40'
    [832, 840) 'coerce47'
HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow (/home/scdeny/v8/out/Debug/d8+0x4343c3) in __interceptor_strlen
Shadow bytes around the buggy address:
  0x100027b20d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100027b20d10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100027b20d20: f1 f1 f1 f1 00 00 f2 f2 00 00 00 f2 f2 f2 f2 f2
  0x100027b20d30: 00 f2 f2 f2 00 00 f2 f2 00 f2 f2 f2 00 f2 f2 f2
  0x100027b20d40: 00 f2 f2 f2 04 f2 00 00 00 00 00 00 00 00 00 00
=>0x100027b20d50: 00 00 00 00 00 00 00 00 00[05]f2 f2 f2 f2 f2 f2
  0x100027b20d60: f2 f2 04 f2 00 f2 f2 f2 00 00 00 00 00 00 00 00
  0x100027b20d70: 00 00 00 00 00 00 00 00 00 00 00 05 f2 f2 f2 f2
  0x100027b20d80: f2 f2 f2 f2 00 f2 f2 f2 00 f3 f3 f3 00 00 00 00
  0x100027b20d90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x100027b20da0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==30991==ABORTING




## Attachments

- [patch.diff](attachments/patch.diff) (application/octet-stream, 493 B)

## Timeline

### sc...@gmail.com (2017-09-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-09-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5411230931222528.

### cl...@chromium.org (2017-09-30)

Detailed report: https://clusterfuzz.com/testcase?key=5411230931222528

Job Type: linux_asan_d8_dbg
Crash Type: Stack-buffer-overflow READ {*}
Crash Address: 0x7ff13f79552d
Crash State:
  uloc_toLanguageTag_59
  v8::internal::__RT_impl_Runtime_CanonicalizeLanguageTag
  v8::internal::Runtime_CanonicalizeLanguageTag
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=39415:39416

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5411230931222528

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### in...@chromium.org (2017-09-30)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2017-10-01)

Automatically applying components based on information from OWNERS files. If this seems incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### sh...@chromium.org (2017-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-01)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### in...@chromium.org (2017-10-01)

[Empty comment from Monorail migration]

### ca...@chromium.org (2017-10-02)

Please add appropriate OSs.

### go...@chromium.org (2017-10-02)

[Comment Deleted]

### sh...@chromium.org (2017-10-03)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-10-06)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-10-09)

Please apply appropriate OSs label.

### ro...@chromium.org (2017-10-10)

This is a failure in the Intl library. @jshin, can you please investigate?

### go...@chromium.org (2017-10-10)

Please apply appropriate OSs label. Thank you.

### js...@chromium.org (2017-10-10)

Sorry that I missed this one. Looking into it. 


### js...@chromium.org (2017-10-10)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-10-11)

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

ClusterFuzz has detected this issue as fixed in range 48482:48483.

Detailed report: https://clusterfuzz.com/testcase?key=5411230931222528

Job Type: linux_asan_d8_dbg
Crash Type: Stack-buffer-overflow READ {*}
Crash Address: 0x7ff13f79552d
Crash State:
  uloc_toLanguageTag_59
  v8::internal::__RT_impl_Runtime_CanonicalizeLanguageTag
  v8::internal::Runtime_CanonicalizeLanguageTag
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=39415:39416
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=48482:48483

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5411230931222528

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### js...@chromium.org (2017-10-12)

The fix was landed in time for M63 branch cut. 

inferno@ :  You changed the target from M62 to M63. Do you think it's ok not to merge to M62? 

### cl...@chromium.org (2017-10-12)

ClusterFuzz testcase 5411230931222528 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-10-12)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-10-13)

[Empty comment from Monorail migration]

### js...@chromium.org (2017-10-13)

I believe this should go to M-62 as well. 

Will wait for the canary coverage. 
 
./tools/release/mergeinfo.py 69bd29 says that it does not yet have a canary coverage. 



### js...@chromium.org (2017-10-13)

This is a v8 fix so that it need to be merged to v8's branch that is used in Chrome M63 branch (even though the patch was landed before Chromium's M63 branch cut). 
Requesting for Merging to M63 (v8's 6.3(?) branch). 

Will ask for merging to M62 later. 


### go...@chromium.org (2017-10-13)

[Comment Deleted]

### sh...@chromium.org (2017-10-14)

Your change meets the bar and is auto-approved for M63. Please go ahead and merge the CL to branch 3239 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2017-10-16)

** Bulk Edit **

Please merge your change to M63 branch 3239 before 5:00 PM PT Monday (10/16) so we can take it in for next dev release. Thank you.

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


### go...@chromium.org (2017-10-16)

Per https://crbug.com/chromium/770450#c31, this is already merged to M63.

### js...@chromium.org (2017-10-17)

The fix missed the 1st train for M62 stable. Asking for merge approval to M62 (v8 6.2 branch) for a respin of M62 stable.

### sh...@chromium.org (2017-10-17)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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


### ab...@chromium.org (2017-10-19)

Can you confirm if this is still required for M62 (unclear if fix was reverted or not)? How critical is this and what is the full impact if we wait until M63? This seems to be touching all platforms as well and we're already at stable ramp-up for M62. 

### aw...@chromium.org (2017-10-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-20)

And $1000 for this one - thanks!

### aw...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-10-23)

+hablich@/adamk@ - can you please review this merge from V8 perspective?

### js...@chromium.org (2017-10-23)

Sorry for the late reply. What needs to be done (after approval from Michael) is:


1. Roll ICU in 6.2 branch (of v8) as was done for 6.3 branch
( https://chromium-review.googlesource.com/c/v8/v8/+/723564 )

2. Cherry-pick in 6.2 branch
https://chromium.googlesource.com/v8/v8.git/+/bb1e70a61fbf93488ce9e4e6e943e549732ed65d
   

### js...@chromium.org (2017-10-23)

For 6.2 branch, I'll make two CLs above and ask for the approval. 


### ha...@chromium.org (2017-10-24)

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


### ab...@chromium.org (2017-10-25)

Since it was merged, removing Merge-Approved

### sc...@gmail.com (2017-10-26)

thx @awhalley, :)

### mb...@chromium.org (2017-11-07)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-17)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-17)

[Empty comment from Monorail migration]

### aw...@google.com (2017-11-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### of...@google.com (2018-03-07)

Node.js backport triage: seems to be present on Node 6.x (V8 4.5) only (ASAN build).

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/770450?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089168)*
