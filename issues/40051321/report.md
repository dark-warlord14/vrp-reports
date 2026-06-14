# Security: SEGV_MAPERR with Intl.ListFormat and long strings

| Field | Value |
|-------|-------|
| **Issue ID** | [40051321](https://issues.chromium.org/issues/40051321) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Internationalization, UI>Internationalization |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | an...@googlemail.com |
| **Assignee** | ft...@chromium.org |
| **Created** | 2020-01-22 |
| **Bounty** | $5,000.00 |

## Description

Version: a9a66826332cd6781da92651971925f34dbb3b86
OS: Ubuntu x64
Architecture: x64

Spun-off from: https://bugzilla.mozilla.org/show_bug.cgi?id=1602497

Jeff Walden from Mozilla investigated this a write beyond the allocated characters in ICU code. 


Test case (run with d8):
---
var s = "a".repeat(0xAFFFFFF); // maybe system-dependent

print("len:", new Intl.ListFormat().format(Array(16).fill(s)).length);
---

NOTE: There must be enough free memory to trigger the crash, for example it does crash reproducibly for me with 16GB RAM, but it doesn't crash with only 10GB RAM.


Crashes with:
---
Received signal 11 SEGV_MAPERR 7f6434dbc000

==== C stack trace ===============================

 [0x564c99fb8a64]
 [0x7f67872e9390]
 [0x7f6786930bbc]
 [0x564c9a0f8840]
 [0x564c9a0c85dd]
 [0x564c9a0c882f]
 [0x564c99ffadb3]
 [0x564c99ffb2aa]
 [0x564c9981d672]
 [0x564c999807c3]
 [0x564c99eb9d58]
[end of stack trace]
Segmentation fault (core dumped)
---


Stack trace:
---
#0  __memmove_ssse3 () at ../sysdeps/x86_64/multiarch/memcpy-ssse3.S:2829
#1  0x00007ffff47311c5 in us_arrayCopy(char16_t const*, int, char16_t*, int, int) () at ../../third_party/icu/source/common/unistr.cpp:87
#2  0x00007ffff472ee09 in icu_65::UnicodeString::doAppend(char16_t const*, int, int) () at ../../third_party/icu/source/common/unistr.cpp:1594
#3  0x00007ffff4732e11 in icu_65::UnicodeString::doAppend(icu_65::UnicodeString const&, int, int) () at ../../third_party/icu/source/common/unistr.cpp:1545
#4  0x00007ffff4630c6d in icu_65::UnicodeString::append(icu_65::UnicodeString const&) () at ../../third_party/icu/source/common/unicode/unistr.h:4629
#5  0x00007ffff4696710 in icu_65::SimpleFormatter::format(char16_t const*, int, icu_65::UnicodeString const* const*, icu_65::UnicodeString&, icu_65::UnicodeString const*, signed char, int*, int, UErrorCo$
e&) () at ../../third_party/icu/source/common/simpleformatter.cpp:312
#6  0x00007ffff4696a8c in icu_65::SimpleFormatter::formatAndReplace(icu_65::UnicodeString const* const*, int, icu_65::UnicodeString&, int*, int, UErrorCode&) const ()
    at ../../third_party/icu/source/common/simpleformatter.cpp:243
#7  0x00007ffff39809ed in icu_65::joinStringsAndReplace(icu_65::SimpleFormatter const&, icu_65::UnicodeString const&, icu_65::UnicodeString const&, icu_65::UnicodeString&, signed char, int&, int*, int*, U
ErrorCode&) () at ../../third_party/icu/source/i18n/listformatter.cpp:351
#8  0x00007ffff397ffe2 in icu_65::ListFormatter::format_(icu_65::UnicodeString const*, int, icu_65::UnicodeString&, int, int&, icu_65::FieldPositionHandler*, UErrorCode&) const ()
    at ../../third_party/icu/source/i18n/listformatter.cpp:504
#9  0x00007ffff39806ac in icu_65::ListFormatter::formatStringsToValue(icu_65::UnicodeString const*, int, UErrorCode&) const () at ../../third_party/icu/source/i18n/listformatter.cpp:419
[...]
---


## Timeline

### cl...@chromium.org (2020-01-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5228552700100608.

### es...@chromium.org (2020-01-23)

ICU owners, could you please take a look?

I'm tentatively triaging this as High severity. I can't actually reproduce from Chrome, only from d8. Chrome hangs and eventually the renderer is killed, but I'm not sure if it might still be exploitable or dependent on the system.

[Monorail components: UI>Internationalization]

### sh...@chromium.org (2020-01-24)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### js...@chromium.org (2020-01-26)

Frank, please take a look

[Monorail components: Blink>JavaScript>Internationalization]

### js...@chromium.org (2020-01-26)

andrebargull@, do you know if an upstream bug has been filed against icu?

Adding Markus for UnicodeString


### an...@googlemail.com (2020-01-28)

No, I haven't filed an upstream bug report. 

### ft...@chromium.org (2020-01-29)

[Empty comment from Monorail migration]

### ft...@chromium.org (2020-01-31)

https://unicode-org.atlassian.net/browse/ICU-20958

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu.git/+/9f4020916eb1f28f3666f018fdcbe6c9a37f0e08

commit 9f4020916eb1f28f3666f018fdcbe6c9a37f0e08
Author: Frank Tang <ftang@chromium.org>
Date: Mon Feb 03 19:33:41 2020

Cherrypick fix for SEGV_MAPERR

Avoid int32_t overflow in length addition

See
https://bugs.chromium.org/p/chromium/issues/detail?id=1044570
https://unicode-org.atlassian.net/browse/ICU-20958
https://github.com/unicode-org/icu/pull/971

Bug: chromium:1044570
Change-Id: I52ef1545007d708315e1fd8265ec42d1c706feed
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/2036290
Reviewed-by: Jungshik Shin <jshin@chromium.org>

[modify] https://crrev.com/9f4020916eb1f28f3666f018fdcbe6c9a37f0e08/README.chromium
[add] https://crrev.com/9f4020916eb1f28f3666f018fdcbe6c9a37f0e08/patches/unistr_segmap.patch
[modify] https://crrev.com/9f4020916eb1f28f3666f018fdcbe6c9a37f0e08/source/common/unistr.cpp


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4d09af54617e24ed9969d6f7abb425786c69b993

commit 4d09af54617e24ed9969d6f7abb425786c69b993
Author: Frank Tang <ftang@chromium.org>
Date: Tue Feb 04 04:26:16 2020

Roll ICU to fix SEGV_MAPERR bug

https://chromium.googlesource.com/chromium/deps/icu.git/+log/dbd3825..9f4020916


Bug: chromium:1044570
Change-Id: If3612265bae968fdb64cbd5eeb3ec9d2e0ce3c4a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2036515
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#738068}

[modify] https://crrev.com/4d09af54617e24ed9969d6f7abb425786c69b993/DEPS


### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### ft...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/44380f804da46fb265ab290ed97ee5352a39917a

commit 44380f804da46fb265ab290ed97ee5352a39917a
Author: Frank Tang <ftang@chromium.org>
Date: Wed Feb 05 23:10:06 2020

Fix SEGMAP_ERR by rolling ICU?

Fix Intl.ListFormat long strings cause SEGMAP_ERR
Add slow regression test.

Bug: chromium:1044570
Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Michael Achenbach <machenbach@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66140}

[modify] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/intl.status
[add] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46

commit d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46
Author: Clemens Backes <clemensb@chromium.org>
Date: Thu Feb 06 08:16:26 2020

Revert "Fix SEGMAP_ERR by rolling ICU?"

This reverts commit 44380f804da46fb265ab290ed97ee5352a39917a.

Reason for revert: Breaks tsan, msan and ubsan, e.g. https://ci.chromium.org/p/v8/builders/ci/V8%20Linux64%20TSAN/30187

Original change's description:
> Fix SEGMAP_ERR by rolling ICU?
> 
> Fix Intl.ListFormat long strings cause SEGMAP_ERR
> Add slow regression test.
> 
> Bug: chromium:1044570
> Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
> Reviewed-by: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Michael Achenbach <machenbach@chromium.org>
> Commit-Queue: Frank Tang <ftang@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#66140}

TBR=machenbach@chromium.org,ftang@chromium.org,syg@chromium.org

Change-Id: I079a675b754b413398d327c44bfeded9c7406333
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1044570
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2039355
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66141}

[modify] https://crrev.com/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46/test/intl/intl.status
[delete] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### ft...@chromium.org (2020-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-10)

[Empty comment from Monorail migration]

### mm...@google.com (2020-02-11)

ftang@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### na...@google.com (2020-02-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-11)

Congrats! The Panel decided to award $5,000 for this report!

### na...@google.com (2020-02-11)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-13)

ftang@ We would normally merge high severity security fixes to stable. I'm adding merge-request labels appropriately - let me know if you disagree, and please add your comments on any stability concerns in the fix - do you deem it completely safe to merge to stable?

### ft...@chromium.org (2020-02-13)

agree we should cheery pick this one. I think it is very safe to merge this to stable.

### ft...@chromium.org (2020-02-13)

Do I need perform the merge or someone else will merge it?

### ad...@google.com (2020-02-14)

Yes, please merge to M81 (branch 4044) and M80 (branch 3987)

### mm...@chromium.org (2020-02-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-02-18)

ftang@ Cl is approved to get merged to M81 branch i.e., 4044, Please goahead and merge manually asap so that this would be part of M81 Beta release this week.


### ft...@chromium.org (2020-02-18)

ok, I will work on it asap

### ft...@chromium.org (2020-02-18)

https://chromium-review.googlesource.com/c/chromium/src/+/2062095 for M80
https://chromium-review.googlesource.com/c/chromium/src/+/2062096 for M81

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/422e9895092cf54ca0b0f2b9bedb7d5ae22d529e

commit 422e9895092cf54ca0b0f2b9bedb7d5ae22d529e
Author: Frank Tang <ftang@chromium.org>
Date: Tue Feb 18 22:40:26 2020

Roll ICU to fix SEGV_MAPERR bug

https://chromium.googlesource.com/chromium/deps/icu.git/+log/dbd3825..9f4020916


(cherry picked from commit 4d09af54617e24ed9969d6f7abb425786c69b993)

Bug: chromium:1044570
Change-Id: If3612265bae968fdb64cbd5eeb3ec9d2e0ce3c4a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2036515
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#738068}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2062096
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#328}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/422e9895092cf54ca0b0f2b9bedb7d5ae22d529e/DEPS


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/76dadfae0111abecb1c55a9389b579f36168ea05

commit 76dadfae0111abecb1c55a9389b579f36168ea05
Author: Frank Tang <ftang@chromium.org>
Date: Tue Feb 18 22:41:18 2020

Roll ICU to fix SEGV_MAPERR bug

https://chromium.googlesource.com/chromium/deps/icu.git/+log/dbd3825..9f4020916


(cherry picked from commit 4d09af54617e24ed9969d6f7abb425786c69b993)

Bug: chromium:1044570
Change-Id: If3612265bae968fdb64cbd5eeb3ec9d2e0ce3c4a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2036515
Commit-Queue: Jungshik Shin <jshin@chromium.org>
Reviewed-by: Jungshik Shin <jshin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#738068}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2062095
Reviewed-by: Srinivas Sista <srinivassista@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#927}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/76dadfae0111abecb1c55a9389b579f36168ea05/DEPS


### ad...@google.com (2020-02-21)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-21)

andrebargull@googlemail.com, thanks for the report - how would you like to be credited in the Chrome release notes?


### an...@googlemail.com (2020-02-25)

> how would you like to be credited in the Chrome release notes?

Simply mention me by name (i.e. "André Bargull"). Can you mention Jeff Walden from Mozilla in addition to me, because he helped tracking down this issue? Thanks! 

### ad...@google.com (2020-02-25)

Done, thanks.

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/44380f804da46fb265ab290ed97ee5352a39917a

commit 44380f804da46fb265ab290ed97ee5352a39917a
Author: Frank Tang <ftang@chromium.org>
Date: Wed Feb 05 23:10:06 2020

Fix SEGMAP_ERR by rolling ICU?

Fix Intl.ListFormat long strings cause SEGMAP_ERR
Add slow regression test.

Bug: chromium:1044570
Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Michael Achenbach <machenbach@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66140}

[modify] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/intl.status
[add] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46

commit d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46
Author: Clemens Backes <clemensb@chromium.org>
Date: Thu Feb 06 08:16:26 2020

Revert "Fix SEGMAP_ERR by rolling ICU?"

This reverts commit 44380f804da46fb265ab290ed97ee5352a39917a.

Reason for revert: Breaks tsan, msan and ubsan, e.g. https://ci.chromium.org/p/v8/builders/ci/V8%20Linux64%20TSAN/30187

Original change's description:
> Fix SEGMAP_ERR by rolling ICU?
> 
> Fix Intl.ListFormat long strings cause SEGMAP_ERR
> Add slow regression test.
> 
> Bug: chromium:1044570
> Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
> Reviewed-by: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Michael Achenbach <machenbach@chromium.org>
> Commit-Queue: Frank Tang <ftang@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#66140}

TBR=machenbach@chromium.org,ftang@chromium.org,syg@chromium.org

Change-Id: I079a675b754b413398d327c44bfeded9c7406333
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1044570
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2039355
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66141}

[modify] https://crrev.com/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46/test/intl/intl.status
[delete] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/44380f804da46fb265ab290ed97ee5352a39917a

commit 44380f804da46fb265ab290ed97ee5352a39917a
Author: Frank Tang <ftang@chromium.org>
Date: Wed Feb 05 23:10:06 2020

Fix SEGMAP_ERR by rolling ICU?

Fix Intl.ListFormat long strings cause SEGMAP_ERR
Add slow regression test.

Bug: chromium:1044570
Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Michael Achenbach <machenbach@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66140}

[modify] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/intl.status
[add] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46

commit d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46
Author: Clemens Backes <clemensb@chromium.org>
Date: Thu Feb 06 08:16:26 2020

Revert "Fix SEGMAP_ERR by rolling ICU?"

This reverts commit 44380f804da46fb265ab290ed97ee5352a39917a.

Reason for revert: Breaks tsan, msan and ubsan, e.g. https://ci.chromium.org/p/v8/builders/ci/V8%20Linux64%20TSAN/30187

Original change's description:
> Fix SEGMAP_ERR by rolling ICU?
> 
> Fix Intl.ListFormat long strings cause SEGMAP_ERR
> Add slow regression test.
> 
> Bug: chromium:1044570
> Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
> Reviewed-by: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Michael Achenbach <machenbach@chromium.org>
> Commit-Queue: Frank Tang <ftang@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#66140}

TBR=machenbach@chromium.org,ftang@chromium.org,syg@chromium.org

Change-Id: I079a675b754b413398d327c44bfeded9c7406333
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1044570
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2039355
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66141}

[modify] https://crrev.com/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46/test/intl/intl.status
[delete] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/44380f804da46fb265ab290ed97ee5352a39917a

commit 44380f804da46fb265ab290ed97ee5352a39917a
Author: Frank Tang <ftang@chromium.org>
Date: Wed Feb 05 23:10:06 2020

Fix SEGMAP_ERR by rolling ICU?

Fix Intl.ListFormat long strings cause SEGMAP_ERR
Add slow regression test.

Bug: chromium:1044570
Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Michael Achenbach <machenbach@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66140}

[modify] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/intl.status
[add] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46

commit d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46
Author: Clemens Backes <clemensb@chromium.org>
Date: Thu Feb 06 08:16:26 2020

Revert "Fix SEGMAP_ERR by rolling ICU?"

This reverts commit 44380f804da46fb265ab290ed97ee5352a39917a.

Reason for revert: Breaks tsan, msan and ubsan, e.g. https://ci.chromium.org/p/v8/builders/ci/V8%20Linux64%20TSAN/30187

Original change's description:
> Fix SEGMAP_ERR by rolling ICU?
> 
> Fix Intl.ListFormat long strings cause SEGMAP_ERR
> Add slow regression test.
> 
> Bug: chromium:1044570
> Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
> Reviewed-by: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Michael Achenbach <machenbach@chromium.org>
> Commit-Queue: Frank Tang <ftang@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#66140}

TBR=machenbach@chromium.org,ftang@chromium.org,syg@chromium.org

Change-Id: I079a675b754b413398d327c44bfeded9c7406333
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1044570
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2039355
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66141}

[modify] https://crrev.com/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46/test/intl/intl.status
[delete] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/44380f804da46fb265ab290ed97ee5352a39917a

commit 44380f804da46fb265ab290ed97ee5352a39917a
Author: Frank Tang <ftang@chromium.org>
Date: Wed Feb 05 23:10:06 2020

Fix SEGMAP_ERR by rolling ICU?

Fix Intl.ListFormat long strings cause SEGMAP_ERR
Add slow regression test.

Bug: chromium:1044570
Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Michael Achenbach <machenbach@chromium.org>
Commit-Queue: Frank Tang <ftang@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66140}

[modify] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/intl.status
[add] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46

commit d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46
Author: Clemens Backes <clemensb@chromium.org>
Date: Thu Feb 06 08:16:26 2020

Revert "Fix SEGMAP_ERR by rolling ICU?"

This reverts commit 44380f804da46fb265ab290ed97ee5352a39917a.

Reason for revert: Breaks tsan, msan and ubsan, e.g. https://ci.chromium.org/p/v8/builders/ci/V8%20Linux64%20TSAN/30187

Original change's description:
> Fix SEGMAP_ERR by rolling ICU?
> 
> Fix Intl.ListFormat long strings cause SEGMAP_ERR
> Add slow regression test.
> 
> Bug: chromium:1044570
> Change-Id: I20e3523832ac3c69e88c11bd530122bbe782ad01
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2032712
> Reviewed-by: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Michael Achenbach <machenbach@chromium.org>
> Commit-Queue: Frank Tang <ftang@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#66140}

TBR=machenbach@chromium.org,ftang@chromium.org,syg@chromium.org

Change-Id: I079a675b754b413398d327c44bfeded9c7406333
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Bug: chromium:1044570
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2039355
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Commit-Queue: Clemens Backes <clemensb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#66141}

[modify] https://crrev.com/d6dd4a8d7c79265f6e29c56a7262fb952bb4ce46/test/intl/intl.status
[delete] https://crrev.com/44380f804da46fb265ab290ed97ee5352a39917a/test/intl/regress-1044570.js


### [Deleted User] (2020-05-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1044570?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Internationalization, UI>Internationalization]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051321)*
