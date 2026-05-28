# Security: UTF chartorune heap-buffer-overflow crash

| Field | Value |
|-------|-------|
| **Issue ID** | [40060367](https://issues.chromium.org/issues/40060367) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>OptimizationGuide |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2022-07-22 |
| **Bounty** | $8,000.00 |

## Description

**VERSION** : trunk

%< - [Run] --------------------

./utf-fuzzer testcase

==46780==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x128e68ea03d1 at pc 0x7ff74706131e bp 0x008ea54ff4c0 sp 0x008ea54ff508  

READ of size 1 at 0x128e68ea03d1 thread T0  

SCARINESS: 12 (1-byte-read-heap-buffer-overflow)  

#0 0x7ff74706131d in charntorune third\_party\utf\src\utf\chartorune.c:29:6  

#1 0x7ff74706145f in LLVMFuzzerTestOneInput third\_party\utf\src\utf\utf\_chartorune\_fuzzer.cc:16:5  

#2 0x7ff7470b2ffe in fuzzer::Fuzzer::ExecuteCallback(unsigned char const \*, unsigned \_\_int64) third\_party\libFuzzer\src\FuzzerLoop.cpp:556:15  

#3 0x7ff7470b1a58 in fuzzer::Fuzzer::RunOne(unsigned char const \*, unsigned \_\_int64, bool, struct fuzzer::InputInfo \*, bool \*) third\_party\libFuzzer\src\FuzzerLoop.cpp:470:3  

#4 0x7ff7470b5be2 in fuzzer::Fuzzer::MutateAndTestOne(void) third\_party\libFuzzer\src\FuzzerLoop.cpp:698:19  

#5 0x7ff7470b7fd1 in fuzzer::Fuzzer::Loop(class std::Cr::vector<struct fuzzer::SizedFile, class fuzzer::fuzzer\_allocator<struct fuzzer::SizedFile>> &) third\_party\libFuzzer\src\FuzzerLoop.cpp:830:5  

#6 0x7ff74708b6a5 in fuzzer::FuzzerDriver(int \*, char \*\*\*, int (\_\_cdecl \*)(unsigned char const \*, unsigned \_\_int64)) third\_party\libFuzzer\src\FuzzerDriver.cpp:824:6  

#7 0x7ff7470ed164 in main third\_party\libFuzzer\src\FuzzerMain.cpp:19:10

%< - [LibFuzzer] --------------------

Source: third\_party/utf/BUILD.gn

```
import("//testing/libfuzzer/fuzzer_test.gni")  
  
fuzzer_test("utf_fuzzer") {  
    sources = [  
        "src/include/utf.h",  
        "src/utf/chartorune.c",  
        "src/utf/utf_fuzzer.cc",  
    ]  
    deps = [":utf"]  
}  

```

%< - [Source] --------------------

Source: third\_party/utf/src/utf/chartorune.c

```
int  
charntorune(Rune \*p, const char \*s, size_t len)  
{  
	unsigned char c, i, m, n, x;  
	Rune r;  
  
	if(len == 0) /\* can't even look at s[0] \*/  
		return 0;  
  
	c = \*s++;  
  
	if(!(c & 0200)) /\* basic byte \*/  
		return (\*p = c, 1);  
  
	if(!(c & 0100)) /\* continuation byte \*/  
		return (\*p = Runeerror, 1);  
  
	n = utftab[c & 077];  
  
	if(n == 0) /\* illegal byte \*/  
		return (\*p = Runeerror, 1);  
  
	if(len == 1) /\* reached len limit \*/  
		return 0;  
  
->	if((\*s & 0300) != 0200) /\* not a continuation byte \*/  
		return (\*p = Runeerror, 1);  

```

Credits: Michael Dau

## Attachments

- [testcase](attachments/testcase) (text/plain, 1 B)
- [utf_fuzzer.cc](attachments/utf_fuzzer.cc) (text/plain, 228 B)

## Timeline

### mi...@gmail.com (2022-07-22)

references for use of library:

1. https://source.chromium.org/search?q=chartorune&ss=chromium 
2. https://source.chromium.org/search?q=charntorune&sq=&ss=chromium

### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-07-25)

Thanks for the report and the fuzzer! This does repro for me locally with both patched in. This is similar to https://crbug.com/chromium/1336768, but the issue here is with the third-party library and not the caller.

In addition to fixing this in Chromium, we should land the fuzzer and submit the patch upstream.

[Monorail components: Internals>OptimizationGuide]

### [Deleted User] (2022-07-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2022-07-27)

So chrome is actually using 2 variants of chartorune (and charntorune), one is libutf in third_party and then several other libraries (re2 and libphonenumber) are using a separate implementation (the signature is identical).

The utf in third_party (https://source.chromium.org/chromium/chromium/src/+/main:third_party/utf/) is the one that is broken. That is a port/modified of the plan9 utf lib. 

The only place in Chrome using charntorune is here (https://source.chromium.org/chromium/chromium/src/+/main:components/translate/core/language_detection/ngram_hash_ops_utils.cc;l=42)

The other usages are either the other version (which does not have the bug) or is not compiled into chrome (e.g., https://source.chromium.org/chromium/chromium/src/+/main:third_party/tflite_support/src/tensorflow_lite_support/custom_ops/kernel/whitespace_tokenizer.cc;l=52 which is not built into tflite_support).

I'm going to lower the priority and request the bug security bug also be lowered as I don't think it is actually triggerable in Chrome today.

The next step actually is to just remove the broken third_party/utf library and use the one that the task api and the language detection util should use (https://github.com/tensorflow/tflite-support/blob/master/workspace9.bzl#L308)


rsesek@ - do you have any concerns or comments about this?





### mc...@chromium.org (2022-07-27)

[Empty comment from Monorail migration]

### mc...@chromium.org (2022-07-27)

Update: looks like we have a symbol collision because of the libphonenumber library (third_party/libphonenumber/dist/cpp/src/phonenumbers/utf/utf.h)

Looks like there was a VERY subtle signature difference between libphonenumber and the current third_party utf functions

e.g., int charntorune(Rune*, const char*, size_t);     vs int charntorune(Rune* r, const char* s, int n). 

so no duplicate in that variant. 

Trying to work up some options. 



### mc...@chromium.org (2022-07-27)

The best options I can think of are:

1) to force libphonenumber to migrate their "copies" of the partial api to something that doesn't squat on the actual library functions then migrate the utf library in third_party to the "correct" one.
2) follow the pattern that re2 did (https://github.com/google/re2/blob/main/util/utf.h) which is make another copy and wrap it in a namespace. This would mean we would have a c++ wrapper around the underlying C api.


2) seems like the faster and probably the nicer/better way to me and follows the other existing third_party case in chrome.

sophiechang@, tbansal@, rsesek@ - wdyt?



### mc...@chromium.org (2022-07-27)

Acutally, I think we should just upstream a patch to libphonenumber that namesapces their copy. They did this for a similar issue before: 

https://github.com/google/libphonenumber/commit/98e96f3a8bd2d4ecbd269855fdb2ac1fcb0adfa8

I'll try to do that and upstream it and have libphonenumber owners pull that in.



### [Deleted User] (2022-08-02)

[Empty comment from Monorail migration]

### mc...@chromium.org (2022-08-03)

Upstream CL is landed to namespace libphonenumber's utf. Will need to wait for a few rolls, then I can start the third_party add and remove of the old/buggy utf library.



### mi...@gmail.com (2022-09-10)

Is there update on this?

### mc...@chromium.org (2022-09-12)

There is an issue with the upstream patch between an internal library and the public one so my patch did not make it into the libphonenumber github repo.

I'll try to make progress this week on landing the patch directly to libphonenumber or falling back to option (2) in https://crbug.com/chromium/1346675#c10 - wrap the C api in a C++ wrapper in a separate namespace to avoid the collision. 



### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### mi...@gmail.com (2022-10-08)

Any update?

### mc...@chromium.org (2022-10-10)

Robert, you just updated something in another third_party library that looked like it might be a viable work around.

Would you take a look? 

### ro...@chromium.org (2022-10-17)

[Empty comment from Monorail migration]

### ro...@chromium.org (2022-10-17)

Ended up triggering a similar fuzz crash with one of my CLs, yay fuzzing!

+ajgo, since this is in ML-land

I think there's an underlying problem here with usage (note the change to the subject line).

chartorune is explicitly unsafe, whereas charntorune is safe since it guarantees to respect a max length. The only place (in open-source) that this is called out is [here in libphonenumber](https://github.com/google/libphonenumber/blob/07294e78abb30138ad8f0771408afedf90900388/cpp/src/phonenumbers/utf/rune.c#L48), although it is mentioned in [Google-internal patches](http://shortn/_y6Si7pxHqk).

This overflow behavior seems to be the same in both libphonenumber and //third_party/utf. Note also utf's [little trick](https://source.chromium.org/chromium/chromium/src/+/main:third_party/utf/src/utf/chartorune.c;l=61;drc=a5fb7662f5a2c5b61c532d949678ce1c4a1dc665) to try to use charntorune under the hood doesn't cut it.

Here's my proposal:
(a) Add fuzzing for charntorune in //third_party/utf
(b) Don't bother with fuzzing on chartorune since we know it is unsafe
(c) Add fuzzing for libphonenumber's Parse
(d) Add some kind of try-bot failure for new usages to chartorune in Chromium, make everybody use charntorune
  * NOTE: There is no existing usage of the unsafe chartorune outside of //third_party. //components/translate is using charntorune correctly
(e) File bugs against each //third_party repo that has a usage of chartorune and have them fix it (ends up just being me anyways)
  re2: [Already checked](https://source.chromium.org/chromium/chromium/src/+/main:third_party/re2/src/re2/parse.cc;l=1396;drc=aaea55c708c63d53a89fb525484aa94747599714)
  tflite_support: On me to land an upstream change

### ro...@chromium.org (2022-10-17)

[Empty comment from Monorail migration]

### aj...@chromium.org (2022-10-17)

Thanks for following up Robert - those steps make sense.

### ro...@chromium.org (2022-10-19)

https://crbug.com/chromium/1346675#c21 was missing one other usage in third_party code (which I also own!) and the upstream change is landing now in cl/481711474. I'll roll the library tomorrow (Wednesday)

### ro...@chromium.org (2022-10-19)

RE (a) Add fuzzing for charntorune in //third_party/utf

charntorune isn't even built into Chrome, so I'll skip this one.

### gi...@appspot.gserviceaccount.com (2022-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c7afc16c7b73d82d4c4faa6f2602b2632bd4ab5a

commit c7afc16c7b73d82d4c4faa6f2602b2632bd4ab5a
Author: Robert Ogden <robertogden@chromium.org>
Date: Wed Oct 19 20:02:25 2022

Remove TFLite Support's whitespace tokenizer

whitespace tokenizer uses an unsafe function, chartorune, which
cannot be easily fixed upstream. In the mean time we'll just remove it
so nobody accidentally uses it.

Bug: 1346675
Change-Id: I7fb3ba52e0f9cdf55ace15c3828550853535cfdf
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3961634
Reviewed-by: Michael Crouse <mcrouse@chromium.org>
Commit-Queue: Robert Ogden <robertogden@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1061197}

[modify] https://crrev.com/c7afc16c7b73d82d4c4faa6f2602b2632bd4ab5a/third_party/tflite_support/README.chromium
[delete] https://crrev.com/f8bfe1aa185896ed165dbcea313d5cab51991e34/third_party/tflite_support/src/tensorflow_lite_support/custom_ops/kernel/whitespace_tokenizer_op_resolver.cc
[delete] https://crrev.com/f8bfe1aa185896ed165dbcea313d5cab51991e34/third_party/tflite_support/src/tensorflow_lite_support/custom_ops/kernel/whitespace_tokenizer_test.cc
[delete] https://crrev.com/f8bfe1aa185896ed165dbcea313d5cab51991e34/third_party/tflite_support/src/tensorflow_lite_support/custom_ops/kernel/whitespace_tokenizer.cc
[add] https://crrev.com/c7afc16c7b73d82d4c4faa6f2602b2632bd4ab5a/third_party/tflite_support/patches/0014-remove-whitespace-tokenizer.patch
[delete] https://crrev.com/f8bfe1aa185896ed165dbcea313d5cab51991e34/third_party/tflite_support/src/tensorflow_lite_support/custom_ops/kernel/whitespace_tokenizer_op_resolver.h
[delete] https://crrev.com/f8bfe1aa185896ed165dbcea313d5cab51991e34/third_party/tflite_support/src/tensorflow_lite_support/custom_ops/kernel/whitespace_tokenizer_op_resolver_wrapper.cc
[delete] https://crrev.com/f8bfe1aa185896ed165dbcea313d5cab51991e34/third_party/tflite_support/src/tensorflow_lite_support/custom_ops/kernel/whitespace_tokenizer_test.py
[delete] https://crrev.com/f8bfe1aa185896ed165dbcea313d5cab51991e34/third_party/tflite_support/src/tensorflow_lite_support/custom_ops/kernel/whitespace_tokenizer.h


### gi...@appspot.gserviceaccount.com (2022-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a59de929c5ff2885556a34ca2984a9bf625abb04

commit a59de929c5ff2885556a34ca2984a9bf625abb04
Author: Robert Ogden <robertogden@chromium.org>
Date: Wed Oct 19 23:28:42 2022

Add fuzzing tests to libphonenumber

Adds two fuzzing tests, one for the basic libphonenumber's Parse.

The other fuzzer is for the charntorune function that is actually
declared in //third_party/utf, but is defined in libphonenumber's
rune.c.

Bug: 1346675
Change-Id: Ie9ad7b3ca66c862d027764c904756281d4e2d675
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3964620
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Reviewed-by: Alex Gough <ajgo@chromium.org>
Commit-Queue: Robert Ogden <robertogden@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1061311}

[add] https://crrev.com/a59de929c5ff2885556a34ca2984a9bf625abb04/third_party/libphonenumber/libphonenumber_fuzzer.cc
[add] https://crrev.com/a59de929c5ff2885556a34ca2984a9bf625abb04/third_party/libphonenumber/charntorune_fuzzer.cc
[modify] https://crrev.com/a59de929c5ff2885556a34ca2984a9bf625abb04/third_party/libphonenumber/BUILD.gn
[modify] https://crrev.com/a59de929c5ff2885556a34ca2984a9bf625abb04/third_party/libphonenumber/README.chromium


### gi...@appspot.gserviceaccount.com (2022-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/92101dcb6ca7108832c06fc2eddfa53459de2c60

commit 92101dcb6ca7108832c06fc2eddfa53459de2c60
Author: Robert Ogden <robertogden@chromium.org>
Date: Wed Oct 19 23:49:36 2022

Add PRESUBMIT warning that chartorune should not be used

charntorune should be used instead.

Note: libphonenumber has this impl of charntorune
(https://github.com/google/libphonenumber/blob/07294e78abb30138ad8f0771408afedf90900388/cpp/src/phonenumbers/utf/rune.c#L48)
that is explicitly memory-safe whereas the version in utf is kinda just
hard-coded to work, but actually doesn't
(https://source.chromium.org/chromium/chromium/src/+/main:third_party/utf/src/utf/chartorune.c;l=61;drc=a5fb7662f5a2c5b61c532d949678ce1c4a1dc665).

Both utf and libphonenumber have headers that declare charntorune, but
only libphonenumber's .cc is built into Chrome.

Bug: 1346675
Change-Id: I2a6527a8ce62debba85f849cf9721c89be1c4054
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3966650
Commit-Queue: Robert Ogden <robertogden@chromium.org>
Reviewed-by: Daniel Cheng <dcheng@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1061327}

[modify] https://crrev.com/92101dcb6ca7108832c06fc2eddfa53459de2c60/PRESUBMIT.py


### ro...@chromium.org (2022-10-24)

[Empty comment from Monorail migration]

### mi...@gmail.com (2022-10-25)

Is the bug qualifying for a bounty?

### [Deleted User] (2022-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-25)

[Empty comment from Monorail migration]

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations, Michael Dau! The VRP Panel has decided to award you $7,000 for this report + $1,000 bonus for the fuzzer that we used. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### pg...@google.com (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1346675?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060367)*
