# Chrome 32 bit only: Float argument passed to function is garbage inside the function

| Field | Value |
|-------|-------|
| **Issue ID** | [40087556](https://issues.chromium.org/issues/40087556) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>WebAssembly |
| **Platforms** | Windows |
| **Reporter** | ga...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2017-05-05 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3085.1 Safari/537.36

Steps to reproduce the problem:
1. Refer attached WAST_BUGGY.txt. Note the signature of __testfunmangled
2. Note how this function is getting called
3. Note the statement immediately after the call site (if it matters for code generation inside chrome). The second last argument passed is 650.1 (say) as printed immediately before this call
4. Note the definitions of helper functions
5. After The call in step 3, inside first line of function __testfunmangled the value of second last argument is garbage (eg 1e-34) as printed to console or seen in debug tools - BUG

What is the expected behavior?
In step 5, the expected behavior is the value should be same as passed by caller (650.1)
This works fine in Chrome 64 bit 
This works fine in Firefox 32 bit and all 64 bit browsers (Edge Insider, Safari TP, FF)

What went wrong?
After The call in step 3, inside first line of function __testfunmangled the value of second last argument is garbage (eg 1e-34) as printed to console or seen in debug tools - BUG

Did this work before? No 

Chrome version: 60.0.3085.1  Channel: n/a
OS Version: 10.0
Flash Version: Shockwave Flash 26.0 r0

I tried to create a test case(see attached a.cpp) but the emscripten toolchain did not generate the same WASM instruction set as the actual large codebase - So compiling a.cpp does not cause the bug to reproduce. It is attached for illustration purpose only.
Also discussed at:
https://groups.google.com/forum/#!searchin/emscripten-discuss/chrome%7Csort:relevance/emscripten-discuss/enLqQMj_bmM/o3LG4t_HAQAJ

## Attachments

- [a.cpp](attachments/a.cpp) (text/plain, 719 B)
- [WAST_BUGGY.txt](attachments/WAST_BUGGY.txt) (text/plain, 1.9 KB)
- [WAST_ok.txt](attachments/WAST_ok.txt) (text/plain, 1.7 KB)
- [b.cpp](attachments/b.cpp) (text/plain, 688 B)
- [test.zip](attachments/test.zip) (application/octet-stream, 88.5 KB)

## Timeline

### ga...@gmail.com (2017-05-05)

Note that if I debug wasm using devtool (chrome 32 bit) and put a breakpoint at wasm function just before the call site and single step through wasm code, the bug does not happen. But if i put a breakpoint inside the called function (__testfunmangled in the attached example) - i get garbage value as second last parameter(as seen in dev tools) of the function (last int argument is fine)

### ds...@chromium.org (2017-05-05)

[Empty comment from Monorail migration]

[Monorail components: -Blink Blink>JavaScript>WebAssembly]

### mt...@chromium.org (2017-05-05)

Andreas, I believe this is down your alley.

Adding Clemens for the odd debug-time behavior described in #1

### cl...@chromium.org (2017-05-05)

Sounds like a problem in compiled code only.

The debugging experience makes sense: If also the caller is executed in the interpreter, everything is working as intended. If just the callee is interpreted, then garbage is passed. Hence garbage must be produced inside the caller (which is optimized code).

I can have a further look next week.

### ah...@chromium.org (2017-05-08)

Hi gauravdewan007@gmail.com, I tried to reproduce this issue, but I don't know how I should use the files you provided, and I was not able to reproduce the problem with a test case I wrote myself. Would it be possible for you to send me a .wasm file which triggers the bug, or a .js file or .html file which I can run and debug in chrome/v8? Thanks!

### ga...@gmail.com (2017-05-11)

The bug occurs in a large proprietary codebase. I have collected the wasm stack machine instruction (WASM text file) around the point of failure. Does loading this wast file (by removing comments in this file) and calling __testfunmangled reproduce the bug ?
If not, it may be due to complex interaction of compilation process inside chrome. The page at http://mbebenita.github.io/WasmExplorer/ helps to get firefox x86 disassembly - if there is a similar tool for chrome, I can run offline and share the disassembly around the affected function

### br...@chromium.org (2017-08-16)

[Empty comment from Monorail migration]

### br...@chromium.org (2017-08-16)

[Empty comment from Monorail migration]

### ti...@chromium.org (2017-08-31)

#6 can you provide a simpler repro for this issue? As per #5 it was not clear how to go about reproducing this. We may need to write more tests in this area but a small repro would be very valuable here.


### ga...@gmail.com (2017-09-22)

Looks like other folks are hitting similar issue:

https://groups.google.com/forum/#!topic/emscripten-discuss/9Y5TjFReETQ
Now there is a simple repro test case for that issue


### ga...@gmail.com (2017-09-22)

on forum, ming_zhao reported the issue with code generation in wasm chrome 32 bit- and that issue is reproducible in chrome canary version 63.0.3221.0 (32 bit). Attached is b.cpp which when compiled using emscripten 1.37.9 (but i guess any version of emscripten would work)
em++ b.cpp -s WASM=1 -o bb.html
The generated wasm and html are attached in test.zip
Simple unzip test.zip and run (any webserver) http-server -p 8000 in test folder and visit localhost:8000/bb.html in chrome 32 bit. The last argument y4 is shown as 0 which is incorrect
output in chrome 32 bit:
FloatTest::FloatTest,x1:32.263725,y1:-36.779434,x2:31.802177,y2:-37.039062,x3:31.802177,y3:-37.039062,x4:31.802177,y4:-37.039062
FloatTest-void init,x1:32.263725,y1:-36.779434,x2:31.802177,y2:-37.039062,x3:31.802177,y3:-37.039062,x4:31.802177,y4:0.000000


### ah...@chromium.org (2017-09-22)

Thank you gauravdewan007@gmail.com, I can reproduce the issue and will start to investigate.

### cl...@chromium.org (2017-09-26)

This is a security issue. We mess up the stack if float32 values are passed to wasm functions in special situations.

We isolated the problem, fix is on it's way.

### bu...@chromium.org (2017-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8f0cd1c244a766d11a0447de6c1fb45af728ed29

commit 8f0cd1c244a766d11a0447de6c1fb45af728ed29
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Wed Sep 27 13:49:55 2017

[turbofan] Fix passing float parameters on the stack

There was an issue with passing float32 parameters, if the value was
spilled on the stack and passed as stack parameter.
First, we sometimes reduced the stack pointer by 8 bytes instead of 4,
and second, there was a mismatch between movsd and movss.

R=titzer@chromium.org

Bug: chromium:718858
Change-Id: Ia884df369ddd95adeff3733f9715f589996f0b65
Also-By: ahaas@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/684738
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Reviewed-by: Ben Titzer <titzer@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#48181}
[modify] https://crrev.com/8f0cd1c244a766d11a0447de6c1fb45af728ed29/src/compiler/ia32/code-generator-ia32.cc
[add] https://crrev.com/8f0cd1c244a766d11a0447de6c1fb45af728ed29/test/mjsunit/wasm/many-parameters.js
[modify] https://crrev.com/8f0cd1c244a766d11a0447de6c1fb45af728ed29/test/mjsunit/wasm/wasm-constants.js


### cl...@chromium.org (2017-09-29)

This has >24h canary coverage now. Requesting backmerge.

### sh...@chromium.org (2017-09-29)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-09-29)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-09-29)

+ asymmetric - can you please confirm if it's okay to merge this for M62 from a security perspective?

### sh...@chromium.org (2017-09-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/bfaacb8afbc695e0c33cb361b46c9e0a33c64219

commit bfaacb8afbc695e0c33cb361b46c9e0a33c64219
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Mon Oct 02 08:26:26 2017

[wasm] Add flag for memory tracing

With --wasm-trace-memory, both compiled code and the interpreter will
output each memory load or store. This helps to debug miscompilations in
emscripten or in V8, like the referenced bug.

R=titzer@chromium.org

Bug: chromium:718858
Change-Id: I90704d164975b11c65677f86947ab102242d5153
Reviewed-on: https://chromium-review.googlesource.com/684316
Reviewed-by: Ben Titzer <titzer@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#48255}
[modify] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/BUILD.gn
[modify] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/src/compiler/wasm-compiler.cc
[modify] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/src/compiler/wasm-compiler.h
[modify] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/src/flag-definitions.h
[modify] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/src/runtime/runtime-test.cc
[modify] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/src/runtime/runtime.h
[modify] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/src/v8.gyp
[add] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/src/wasm/memory-tracing.cc
[add] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/src/wasm/memory-tracing.h
[modify] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/src/wasm/wasm-interpreter.cc
[add] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/test/message/wasm-trace-memory-interpreted.js
[add] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/test/message/wasm-trace-memory-interpreted.out
[add] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/test/message/wasm-trace-memory.js
[add] https://crrev.com/bfaacb8afbc695e0c33cb361b46c9e0a33c64219/test/message/wasm-trace-memory.out


### cl...@chromium.org (2017-10-02)

FYI: The memory tracing flag would not be backmerged, just the CL in #14.

### aw...@google.com (2017-10-02)

abdulsyed@ - Good for M62

### aw...@google.com (2017-10-02)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-10-02)

Approving cl in #14 for Merge to M62. Branch 3202. 

### bu...@chromium.org (2017-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1356ff47f9f23205b3c73dcc0f75708153aa82e9

commit 1356ff47f9f23205b3c73dcc0f75708153aa82e9
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Wed Oct 04 12:36:31 2017

Merged: [turbofan] Fix passing float parameters on the stack

There was an issue with passing float32 parameters, if the value was
spilled on the stack and passed as stack parameter.
First, we sometimes reduced the stack pointer by 8 bytes instead of 4,
and second, there was a mismatch between movsd and movss.

R=​titzer@chromium.org
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

Bug: chromium:718858
Change-Id: Ia884df369ddd95adeff3733f9715f589996f0b65
Also-By: ahaas@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/684738
Reviewed-by: Andreas Haas <ahaas@chromium.org>
Reviewed-by: Ben Titzer <titzer@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#48181}(cherry picked from commit 8f0cd1c244a766d11a0447de6c1fb45af728ed29)
Reviewed-on: https://chromium-review.googlesource.com/700374
Cr-Commit-Position: refs/branch-heads/6.2@{#58}
Cr-Branched-From: efa2ac4129d30c7c72e84c16af3d20b44829f990-refs/heads/6.2.414@{#1}
Cr-Branched-From: a861ebb762a60bf5cc2a274faee3620abfb06311-refs/heads/master@{#47693}
[modify] https://crrev.com/1356ff47f9f23205b3c73dcc0f75708153aa82e9/src/compiler/ia32/code-generator-ia32.cc
[add] https://crrev.com/1356ff47f9f23205b3c73dcc0f75708153aa82e9/test/mjsunit/wasm/many-parameters.js
[modify] https://crrev.com/1356ff47f9f23205b3c73dcc0f75708153aa82e9/test/mjsunit/wasm/wasm-constants.js


### cl...@chromium.org (2017-10-04)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-05)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-06)

Congratulations gauravdewan007@! The Chrome VRP (g.co/ChromeBugRewards) panel decided to award $3,000 for this bug.  A member of our finance team will be in touch to arrange for payment.

Note that in the future if you find other security bugs (and I hope you do!) please use the security template which will allow it to be triaged correctly. 

### aw...@chromium.org (2017-10-06)

[Empty comment from Monorail migration]

### ga...@gmail.com (2017-10-15)

Thanks for the information.Here is my acknowledgment information:
Gaurav Dewan(@007gauravdewan) of Adobe Systems India Pvt. Ltd.

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

### is...@google.com (2020-02-17)

This issue was migrated from crbug.com/chromium/718858?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/768407]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087556)*
