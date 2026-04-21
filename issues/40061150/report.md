# Security: Type confusion in V8

| Field | Value |
|-------|-------|
| **Issue ID** | [40061150](https://issues.chromium.org/issues/40061150) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | p4...@gmail.com |
| **Assignee** | jg...@chromium.org |
| **Created** | 2022-09-26 |
| **Bounty** | $10,000.00 |

## Description

See details at https://crbug.com/chromium/1368046#c2.




## Attachments

- [test.js](attachments/test.js) (text/plain, 2.6 KB)

## Timeline

### p4...@gmail.com (2022-09-26)

This template is ONLY for reporting security bugs. If you are reporting a
Download Protection Bypass bug, please use the "Security - Download
Protection" template. For all other reports, please use a different
template.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com
/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs:
https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP:
http://g.co/ChromeBugRewards

NOTE: Security bugs are normally made public once a fix has been widely
deployed.

-------------------------

VULNERABILITY DETAILS
It's a type confusion bug in maglev of V8. It can confusion any V8 object as **Context**.

In `Runtime_PushCatchContext`, when getting `isolate->context()`, it get a wrong object ,and then confuse it as Context. The wrong object can be controlled as any js object(smi or HeapObject).
```c++
RUNTIME_FUNCTION(Runtime_PushCatchContext) {
  HandleScope scope(isolate);
  DCHECK_EQ(2, args.length());
  Handle<Object> thrown_object = args.at(0);
  Handle<ScopeInfo> scope_info = args.at<ScopeInfo>(1);
  Handle<Context> current(isolate->context(), isolate);
  return *isolate->factory()->NewCatchContext(current, scope_info,
                                              thrown_object);
}
```

VERSION
v8 Version: commit 27d8c2e99378f1ba8e7c24500772d9dab137c002
Operating System: Win64 

REPRODUCTION CASE
run the test.js in d8 with flag " --allow-natives-syntax --maglev"


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [render]
Crash State: 
In debug version, it will crash at a DCHECK where checking the correctness of context.
#
# Fatal error in ..\..\src\runtime\runtime-scopes.cc, line 600
# Debug check failed: isolate->context().is_null() || isolate->context().IsContext().
#
#
#
#FailureMessage Object: 000012D356BF5C40

In release version, it will crash at an access-violation
=================================================================
==12632==ERROR: AddressSanitizer: access-violation on unknown address 0x000041414141 (pc 0x7ff7700b56ca bp 0x00adaf5fed60 sp 0x00adaf5fece0 T0)
==12632==The signal is caused by a READ memory access.
==12632==*** WARNING: Failed to initialize DbgHelp!              ***
==12632==*** Most likely this means that the app is already      ***
==12632==*** using DbgHelp, possibly with incompatible flags.    ***
==12632==*** Due to technical reasons, symbolization might crash ***
==12632==*** or produce wrong results.                           ***



### [Deleted User] (2022-09-26)

[Empty comment from Monorail migration]

### jg...@chromium.org (2022-09-26)

Looking.. Removing security labels since ML is not yet enabled.

[Monorail components: -Blink>JavaScript]

### p4...@gmail.com (2022-09-26)

[Comment Deleted]

### jg...@chromium.org (2022-09-26)

We're incorrectly passing Smi 547397793 as the `context` to Runtime_PushCatchContext.

### p4...@gmail.com (2022-09-26)

[Comment Deleted]

### jg...@chromium.org (2022-09-26)

I don't think we're consistent about which labels to set/unset in these cases. While Maglev is still off-by-default, bugs in src/maglev have no security impact and are not security bugs.

### jg...@chromium.org (2022-09-26)

(We explicitly *are* still interested in bug reports though - thanks for the effort!)

### jg...@chromium.org (2022-09-26)

Simplified repro:

function f(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11) {
  for (let i = 0; i < 0; i++) {}
  try {
    throw 42;
  } catch (e) {
  }
}

%PrepareFunctionForOptimization(f);
f(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42);
f(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42);
%OptimizeMaglevOnNextCall(f);
f(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42);

### jg...@chromium.org (2022-09-26)

Well, we seem to plug in the wrong stack slot for the context:

 mov    rsi,QWORD PTR [rbp-0x38]
 (gdb) p $rsi >> 1
 $4 = 42

### jg...@chromium.org (2022-09-27)

Looks like a bug in direct moves for setting up exception handlers https://source.chromium.org/chromium/chromium/src/+/main:v8/src/maglev/maglev-code-generator.cc;l=563;drc=a432cd59d51281057ba2a2673ca645a9600bb927

   Block b6 (exception handler)
[...]
    46/44: φₑ a11 → [stack:1|t]
    47/45: φₑ r1 → [stack:3|t]

-->

                  dir move 0x55c1a3c295c8
0x7f63c0004417   3d7  4c8b5570             REX.W movq r10,[rbp+0x70]
0x7f63c000441b   3db  4c8955d8             REX.W movq [rbp-0x28],r10
                  dir move 0x55c1a3c298c0
0x7f63c000441f   3df  4c8b55d8             REX.W movq r10,[rbp-0x28]
0x7f63c0004423   3e3  4c8955c8             REX.W movq [rbp-0x38],r10

a11 is clobbering r1 (the context).

### p4...@gmail.com (2022-09-28)

[Comment Deleted]

### jg...@chromium.org (2022-09-28)

Thanks, I haven't seen crbug.com/1323841#c9 before, news to me. Alright, Bug-Security and Impact-None it is!

### am...@chromium.org (2022-09-28)

Thanks for re-adjusting to security bug and setting impact to none jgruber@. Adding severity-high as this is type confusion/memory corruption in V8. 

### jg...@chromium.org (2022-09-28)

More info: the problem seems to be that {direct,materialising} moves for exception handler trampolines don't consider possible ordering conflicts at all. These may happen though due to stack slot reuse, i.e. an exception phi target may equal another exception phi's source slot. The fix is to use the parallel move resolver for all these moves.

### gi...@appspot.gserviceaccount.com (2022-10-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/5646b9c3c0edb2d688603c3de72c382018d449a6

commit 5646b9c3c0edb2d688603c3de72c382018d449a6
Author: Jakob Linke <jgruber@chromium.org>
Date: Tue Oct 04 09:16:17 2022

[maglev] Use the parallel move resolver for handler trampolines

Due to stack slot reuse, any of the moves that are part of the handler
trampoline may conflict and thus need parallel move resolution.

Materialisations (= calls to the NewHeapNumber builtin) add an addtl
complication since a) materialising moves can also be part of any
move conflict, b) the builtin call may clobber arbitrary registers,
and c) materialisation need a spot to store the NewHeapNumber result.
We resolve this by materialising into new temporary stack slots
before the main move sequence, and popping into the final target
locations after the main move sequence.

Bug: v8:7700
Change-Id: I1734faf189d02e38af07a817a9b647e2dce54f22
Fixed: chromium:1368046
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3921515
Auto-Submit: Jakob Linke <jgruber@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Jakob Linke <jgruber@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83511}

[modify] https://crrev.com/5646b9c3c0edb2d688603c3de72c382018d449a6/src/maglev/maglev-regalloc.cc
[modify] https://crrev.com/5646b9c3c0edb2d688603c3de72c382018d449a6/src/maglev/maglev-ir.h
[modify] https://crrev.com/5646b9c3c0edb2d688603c3de72c382018d449a6/src/maglev/maglev-code-generator.cc
[add] https://crrev.com/5646b9c3c0edb2d688603c3de72c382018d449a6/test/mjsunit/maglev/regress/regress-1368046.js


### jg...@chromium.org (2022-10-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-10-04)

ClusterFuzz testcase 6602289408311296 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=83510:83511

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-04)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations, Bohan Liu! The VRP panel has decided to award you $10,000 for this report! Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-10)

Hello Bohan, all attachments, such as POCs and patches, are considered part of the original report, so I have undeleted them.

### is...@google.com (2023-02-10)

This issue was migrated from crbug.com/chromium/1368046?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1370426]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061150)*
