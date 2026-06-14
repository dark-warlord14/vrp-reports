# [v8] Uninitialized wasm_compiled_module for deserialized module

| Field | Value |
|-------|-------|
| **Issue ID** | [40090400](https://issues.chromium.org/issues/40090400) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Mac |
| **Reporter** | cw...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2018-02-05 |
| **Bounty** | $3,500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36

Steps to reproduce the problem:
I've tested this code in 6.5-lkgr and master branch, and this also can be reproduced in v8 6.4 if we turn on --wasm-jit-to-native flag.

Execute the following code using d8 with --allow-natives-syntax flag.
```
// Flags: --allow-natives-syntax

load('test/mjsunit/wasm/wasm-constants.js');
load('test/mjsunit/wasm/wasm-module-builder.js');
let kTableSize = 3;

var builder = new WasmModuleBuilder();
var sig_index1 = builder.addType(kSig_i_v);
builder.addFunction('main', kSig_i_ii).addBody([
    kExprGetLocal,
    0,
    kExprCallIndirect,
    sig_index1,
    kTableZero
]).exportAs('main');
builder.setFunctionTableBounds(kTableSize, kTableSize);
var m1_bytes = builder.toBuffer();
var m1 = new WebAssembly.Module(m1_bytes);

var serialized_m1 = %SerializeWasmModule(m1);
var m1_clone = %DeserializeWasmModule(serialized_m1, m1_bytes);
var i1 = new WebAssembly.Instance(m1_clone);

i1.exports.main(123123);
```

What is the expected behavior?
not crash

What went wrong?
This results in segfault.
```
$ ./out/x64.release/d8 wasm.js --allow-natives-syntax
Received signal 11 SEGV_MAPERR 000900000007

==== C stack trace ===============================

 [0x55d067044d95]
 [0x7f2e57b56390]
 [0x55d066f45d64]
 [0x55d066d28a5b]
 [0x55d0668f9b59]
 [0x55d0668d5fb3]
 [0x55d0668d5c01]
 [0x55d0668de219]
 [0x55d0668e0293]
 [0x55d0668e1677]
 [0x7f2e57074830]
 [0x55d0668d402a]
[end of stack trace]
[1]    22535 segmentation fault  ./out/x64.release/d8 wasm.js --allow-natives-syntax
```

Did this work before? N/A 

Chrome version:   Channel: beta
OS Version: OS X 10.13.3
Flash Version:

## Timeline

### cw...@gmail.com (2018-02-05)

I guess this CL fixes this issue: https://chromium-review.googlesource.com/#/c/v8/v8/+/901306

### el...@chromium.org (2018-02-05)

Thanks for the report and patch!

[Monorail components: Blink>JavaScript>WebAssembly]

### cl...@chromium.org (2018-02-05)

Thanks for the report. Will take a look.

### bu...@chromium.org (2018-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/34a8204a1e35acfa3db52d4159a78bb80a2ffa15

commit 34a8204a1e35acfa3db52d4159a78bb80a2ffa15
Author: Choongwoo Han <cwhan.tunz@gmail.com>
Date: Mon Feb 05 16:48:00 2018

[wasm] Set wasm_compiled_module for script of deserialized module

Bug: chromium:808980
Change-Id: I7a89c6e30f473821f676fd5771365103072c78f1
Reviewed-on: https://chromium-review.googlesource.com/901306
Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#51099}
[modify] https://crrev.com/34a8204a1e35acfa3db52d4159a78bb80a2ffa15/src/wasm/wasm-serialization.cc
[add] https://crrev.com/34a8204a1e35acfa3db52d4159a78bb80a2ffa15/test/mjsunit/regress/wasm/regress-808980.js


### cl...@chromium.org (2018-02-05)

Let's merge this to 65 once it got some canary coverage.

### cl...@chromium.org (2018-02-05)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-06)

Your change meets the bar and is auto-approved for M65. Please go ahead and merge the CL to branch 3325 manually. Please contact milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-06)

Pls merge your change to M65 branch 3325 before 2:00 PM PT tomorrow, Wednesday (02/07/18). Thank you.

### bu...@chromium.org (2018-02-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f8a8a0b0d43583135cd77b643e498cb6f0ad700a

commit f8a8a0b0d43583135cd77b643e498cb6f0ad700a
Author: Choongwoo Han <cwhan.tunz@gmail.com>
Date: Wed Feb 07 15:59:29 2018

Merged: [wasm] Set wasm_compiled_module for script of deserialized module

Bug: chromium:808980
Change-Id: I7a89c6e30f473821f676fd5771365103072c78f1
Reviewed-on: https://chromium-review.googlesource.com/901306
Reviewed-by: Clemens Hammacher <clemensh@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#51099}(cherry picked from commit 34a8204a1e35acfa3db52d4159a78bb80a2ffa15)

NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Change-Id: I06e3d1e90b6f133bfa6d4a91caeb0d9fd0a8fc39
Reviewed-on: https://chromium-review.googlesource.com/906709
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/branch-heads/6.5@{#31}
Cr-Branched-From: 73c55f57fe8506011ff854b15026ca765b669700-refs/heads/6.5.254@{#1}
Cr-Branched-From: 594a1a0b6e551397cfdf50870f6230da34db2dc8-refs/heads/master@{#50664}
[modify] https://crrev.com/f8a8a0b0d43583135cd77b643e498cb6f0ad700a/src/wasm/wasm-serialization.cc
[add] https://crrev.com/f8a8a0b0d43583135cd77b643e498cb6f0ad700a/test/mjsunit/regress/wasm/regress-808980.js


### cl...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-19)

Nice one cwhan.tunz@! The Chrome VRP panel decided to award $3,500 for this report :-)

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-17)

This issue was migrated from crbug.com/chromium/808980?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090400)*
