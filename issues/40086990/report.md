# Security: heap-buffer-overflow hashtable.

| Field | Value |
|-------|-------|
| **Issue ID** | [40086990](https://issues.chromium.org/issues/40086990) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings, Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nt...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2017-03-07 |
| **Bounty** | $3,000.00 |

## Description

this is working in the latest version with asan. the asan stacktrace if from long time ago and i didnt updated but still crashing i tried in 59.0.3034.0

**VERSION**  

Chrome Version: stable, dev

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

## Attachments

- poc.html (text/plain, 459 B)
- [stacktrace](attachments/stacktrace) (text/plain, 24.1 KB)

## Timeline

### cl...@chromium.org (2017-03-07)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6061368416665600

### cl...@chromium.org (2017-03-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6061368416665600

Job Type: linux_asan_chrome_mp
Crash Type: Use-after-poison READ 8
Crash Address: 0x7e85f2ca3f00
Crash State:
  blink::getter
  v8::internal::PropertyCallbackArguments::Call
  v8::internal::Object::GetPropertyWithAccessor
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=338684:338804

Reproducer Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96O90Ja7sQ_IgB5BbJp3bA8AhsRa_jzTyoSRBxTXAI3Le8NaGxYBqwhtvfu832ArX0nmq5n5gLHDAE4B5x-dbksZCNEwGWSM1BJXIbYoZJDygSCnvx3vwPGDRdPBy1QXFU1Y_fpBSd4w9IYrQ0sNV9JfQvlJVioGgN0WVBI2jKccMOE-wRezlQuZC0a0xoXf5nlRRub3iG7Ux3_K-ASVeG4MO5K_2hvHKPA_WhqaCyNkXRkCjk1nBvWIy4yILydlfPaDoDamE1GrbFFyCZDoxC89Gp3vVl4Kt55XqMNtuhnlrUCrdemLDP6cqdEsQwYTnXvrHXQBWaj-j5dll-vMBk8SSraawFcp4hwNVMCSyTr5BRqSHI?testcase_id=6061368416665600


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### sh...@chromium.org (2017-03-08)

[Empty comment from Monorail migration]

### do...@chromium.org (2017-03-13)

haraken/ishell: this looks like V8 is trying to get a property on HTMLDocument, but that property is gone. I can't see anything really relevant in the Blink or V8 changelogs (but they date back to 2015). Do you mind taking a look?

[Monorail components: Blink>Bindings Blink>JavaScript]

### mm...@google.com (2017-03-13)

[Comment Deleted]

### mm...@google.com (2017-03-13)

[Comment Deleted]

### ha...@chromium.org (2017-03-13)

yukishiino: Would you mind taking a look at this?


### sh...@chromium.org (2017-03-13)

[Empty comment from Monorail migration]

### nt...@gmail.com (2017-03-15)

can i know which flags are you using in ASAN (clusterfuzz) if im a little bit more free i will take a look and do the analysis this weekend

### yu...@chromium.org (2017-03-15)

Thanks for the offer.

GN args
----
enable_ipc_fuzzer = true
goma_dir = "/b/c/goma_client"
is_asan = true
is_component_build = false
is_debug = false
is_lsan = true
sanitizer_coverage_flags = "edge"
use_goma = true
v8_enable_verify_heap = true
----

ASAN_OPTIONS = redzone=128:symbolize=0:detect_stack_use_after_return=1:alloc_dealloc_mismatch=0:print_scariness=1:check_malloc_usable_size=0:max_uar_stack_size_log=16:use_sigaltstack=1:strict_memcmp=0:detect_container_overflow=1:allocator_may_return_null=1:coverage=0:detect_odr_violation=0:fast_unwind_on_fatal=1:handle_segv=1:malloc_context_size=128

command line flags
--js-flags="--expose-gc --verify-heap" --no-first-run --use-gl=osmesa


### is...@chromium.org (2017-03-15)

[Empty comment from Monorail migration]

### is...@chromium.org (2017-03-16)

[Empty comment from Monorail migration]

### is...@chromium.org (2017-03-16)

After doing manipulations in the test case we end up in a state where the document and another element share the same elements backing store. Investigating...

### is...@chromium.org (2017-03-16)

Here's what happened:

  var e1 = document.createElement("A1");
  Object.preventExtensions(e1);
  Object.preventExtensions(document);
  // document and e1 now share the canonical empty elements dictionary as an elements backing store
  var e2 = document.createElementNS("http://www.w3.org/1999/xhtml", 'form');
  e2.name = 1;
  document.documentElement.appendChild(e2);
  // e2 is added to the document as an callback accessor property and since its name is "1" it's added
  // to the document's elements backing store (which is the canonical empty elements dictionary).

  // The code below executes the accessor created for the document receiver with an element receiver
  // which has incompatible blink object associated with it.
  e1[1];

This issue does not happen in non-api code because we don't even try to modify the object if it's non-extensible.


### jo...@chromium.org (2017-03-16)

I interpret the spec as it's not allowed to preventExtension on API objects with interceptors. (and Object.preventExtensions(document) also throws in Firefox.

### bu...@chromium.org (2017-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/17ac7c5f4d712c914030e1fb7247d2083b04b929

commit 17ac7c5f4d712c914030e1fb7247d2083b04b929
Author: Igor Sheludko <ishell@chromium.org>
Date: Thu Mar 16 16:22:26 2017

[runtime] Ensure that canonical empty dictionaries reallocate upon addition.

BUG=chromium:699166

Change-Id: Ifd460a454d2bf36cff6b114ecd9163ef4fbdc79e
Reviewed-on: https://chromium-review.googlesource.com/456416
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>
Reviewed-by: Ulan Degenbaev <ulan@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/master@{#43869}
[modify] https://crrev.com/17ac7c5f4d712c914030e1fb7247d2083b04b929/src/heap/heap.cc
[modify] https://crrev.com/17ac7c5f4d712c914030e1fb7247d2083b04b929/src/objects-printer.cc
[modify] https://crrev.com/17ac7c5f4d712c914030e1fb7247d2083b04b929/src/objects.cc
[modify] https://crrev.com/17ac7c5f4d712c914030e1fb7247d2083b04b929/src/objects.h


### is...@chromium.org (2017-03-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-03-17)

Your change meets the bar and is auto-approved for M58. Please go ahead and merge the CL to branch 3029 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-03-17)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@google.com (2017-03-17)

Approving merge to M57 Chrome OS. ishell@ please merge by eod today.

### bu...@chromium.org (2017-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/faa24cfc604024e501ce9a8e081f7b9f20684365

commit faa24cfc604024e501ce9a8e081f7b9f20684365
Author: Jakob Kummerow <jakob.kummerow@gmail.com>
Date: Fri Mar 17 20:01:04 2017

Merged: [runtime] Ensure that canonical empty dictionaries reallocate upon addition.

Revision: 17ac7c5f4d712c914030e1fb7247d2083b04b929

BUG=chromium:699166
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Change-Id: I2277e0a422817398bf0b219290b784322115e9a0
Reviewed-on: https://chromium-review.googlesource.com/456341
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/branch-heads/5.7@{#148}
Cr-Branched-From: 975e9a320b6eaf9f12280c35df98e013beb8f041-refs/heads/5.7.492@{#1}
Cr-Branched-From: 8d76f0e3465a84bbf0bceab114900fbe75844e1f-refs/heads/master@{#42426}
[modify] https://crrev.com/faa24cfc604024e501ce9a8e081f7b9f20684365/src/heap/heap.cc
[modify] https://crrev.com/faa24cfc604024e501ce9a8e081f7b9f20684365/src/objects-printer.cc
[modify] https://crrev.com/faa24cfc604024e501ce9a8e081f7b9f20684365/src/objects.cc
[modify] https://crrev.com/faa24cfc604024e501ce9a8e081f7b9f20684365/src/objects.h


### cl...@chromium.org (2017-03-17)

ClusterFuzz has detected this issue as fixed in range 457736:457748.

Detailed report: https://clusterfuzz.com/testcase?key=6061368416665600

Job Type: linux_asan_chrome_mp
Crash Type: Use-after-poison READ 8
Crash Address: 0x7e85f2ca3f00
Crash State:
  blink::getter
  v8::internal::PropertyCallbackArguments::Call
  v8::internal::Object::GetPropertyWithAccessor
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=338684:338804
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=457736:457748

Reproducer Testcase: https://clusterfuzz.com/download/AMIfv96O90Ja7sQ_IgB5BbJp3bA8AhsRa_jzTyoSRBxTXAI3Le8NaGxYBqwhtvfu832ArX0nmq5n5gLHDAE4B5x-dbksZCNEwGWSM1BJXIbYoZJDygSCnvx3vwPGDRdPBy1QXFU1Y_fpBSd4w9IYrQ0sNV9JfQvlJVioGgN0WVBI2jKccMOE-wRezlQuZC0a0xoXf5nlRRub3iG7Ux3_K-ASVeG4MO5K_2hvHKPA_WhqaCyNkXRkCjk1nBvWIy4yILydlfPaDoDamE1GrbFFyCZDoxC89Gp3vVl4Kt55XqMNtuhnlrUCrdemLDP6cqdEsQwYTnXvrHXQBWaj-j5dll-vMBk8SSraawFcp4hwNVMCSyTr5BRqSHI?testcase_id=6061368416665600


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### bu...@chromium.org (2017-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/9e3d9af6fb741a2f30feaf2e549ac476d0814360

commit 9e3d9af6fb741a2f30feaf2e549ac476d0814360
Author: Jakob Kummerow <jakob.kummerow@gmail.com>
Date: Fri Mar 17 20:31:19 2017

Merged: [runtime] Ensure that canonical empty dictionaries reallocate upon addition.

Revision: 17ac7c5f4d712c914030e1fb7247d2083b04b929

BUG=chromium:699166
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Change-Id: I83b26ea71d58ea3576894e2bd8bd217415ce654d
Reviewed-on: https://chromium-review.googlesource.com/456703
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/branch-heads/5.8@{#35}
Cr-Branched-From: eda659cc5e307f20ac1ad542ba12ab32eaf4c7ef-refs/heads/5.8.283@{#1}
Cr-Branched-From: 4310cd02d2160b1457baed81a2f40063eb264a21-refs/heads/master@{#43429}
[modify] https://crrev.com/9e3d9af6fb741a2f30feaf2e549ac476d0814360/src/heap/heap.cc
[modify] https://crrev.com/9e3d9af6fb741a2f30feaf2e549ac476d0814360/src/objects-printer.cc
[modify] https://crrev.com/9e3d9af6fb741a2f30feaf2e549ac476d0814360/src/objects.cc
[modify] https://crrev.com/9e3d9af6fb741a2f30feaf2e549ac476d0814360/src/objects.h


### jk...@chromium.org (2017-03-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-03-17)

Detailed report: https://clusterfuzz.com/testcase?key=6061368416665600

Job Type: linux_asan_chrome_mp
Crash Type: Use-after-poison READ 8
Crash Address: 0x7e85f2ca3f00
Crash State:
  blink::getter
  v8::internal::PropertyCallbackArguments::Call
  v8::internal::Object::GetPropertyWithAccessor
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=338684:338804
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=457736:457748

Reproducer Testcase: https://clusterfuzz.com/download/AMIfv96O90Ja7sQ_IgB5BbJp3bA8AhsRa_jzTyoSRBxTXAI3Le8NaGxYBqwhtvfu832ArX0nmq5n5gLHDAE4B5x-dbksZCNEwGWSM1BJXIbYoZJDygSCnvx3vwPGDRdPBy1QXFU1Y_fpBSd4w9IYrQ0sNV9JfQvlJVioGgN0WVBI2jKccMOE-wRezlQuZC0a0xoXf5nlRRub3iG7Ux3_K-ASVeG4MO5K_2hvHKPA_WhqaCyNkXRkCjk1nBvWIy4yILydlfPaDoDamE1GrbFFyCZDoxC89Gp3vVl4Kt55XqMNtuhnlrUCrdemLDP6cqdEsQwYTnXvrHXQBWaj-j5dll-vMBk8SSraawFcp4hwNVMCSyTr5BRqSHI?testcase_id=6061368416665600


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2017-03-18)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-21)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-28)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### aw...@google.com (2017-03-31)

Many thanks for the report! The VRP panel has decided to award $3,000 for this bug.  A member of our finance team will be in touch to arrange payment.

Also, please let me know how you'd like to be credited if this bug gets mentioned in release notes.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2017-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/699166?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Bindings, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086990)*
