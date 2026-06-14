# Talos Security Advisory for Google Chrome PDFium (TALOS-2020-1044)

| Field | Value |
|-------|-------|
| **Issue ID** | [40051908](https://issues.chromium.org/issues/40051908) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Regexp, Blink>JavaScript>Runtime |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | jg...@chromium.org |
| **Created** | 2020-04-02 |
| **Bounty** | $5,000.00 |

## Description

Chrome Version :Google Chrome 80.0.3987.158  

**URLs (if applicable) :**  

**Other browsers tested:**  

Add OK or FAIL, along with the version, after other browsers where you  

**have tested this issue:**  

Safari:  

Firefox:  

Edge:

**What steps will reproduce the problem?** (Report and poc attached)  

**(1)**  

**(2)**  

**(3)**

**What is the expected result?**

**What happens instead?**

**Please provide any additional information below. Attach a screenshot if**  

**possible.**

## Attachments

- [google_chrome_pdfium_javascript_regexp_memory_corruption_vulnerability_poc.pdf](attachments/google_chrome_pdfium_javascript_regexp_memory_corruption_vulnerability_poc.pdf) (application/pdf, 620 B)

## Timeline

### dt...@chromium.org (2020-04-02)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2020-04-02)

[Empty comment from Monorail migration]

### ts...@chromium.org (2020-04-02)

[Empty comment from Monorail migration]

### ts...@google.com (2020-04-02)

Seems to be a consequence of --jitless

$ out/Asan/d8
V8 version 8.3.31
d8> var a  = Array(1802).join(" +") + Array(16884).join("A");"A".search(a);"A".search(a);
-1

$ out/Asan/d8 --jitless
V8 version 8.3.31
d8>     var a  = Array(1802).join(" +") + Array(16884).join("A");"A".search(a);"A".search(a);
Received signal 11 SEGV_ACCERR 7e8b0000c024

==== C stack trace ===============================

 [0x55ac20a65e2b]
 [0x55ac22dea906]
 [0x7f756364f520]
 [0x55ac21a38120]
 [0x55ac21a379c7]
 [0x55ac21a415be]
 [0x55ac22c713a3]
[end of stack trace]
Segmentation fault

[Monorail components: Blink>JavaScript]

### ts...@google.com (2020-04-02)

Assigning to V8 triage contact.

### ts...@google.com (2020-04-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-04-03)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5695191957176320.

### cl...@chromium.org (2020-04-03)

Clusterfuzz bisected to 3a0f407d266ec6429a166cf2ec5132f6558d3a51 (Reland "Reland "[regexp] Call the regexp interpreter without CEntry overhead"").

Jakob, can you take a look?

[Monorail components: -Blink>JavaScript -Internals>Plugins>PDF Blink>JavaScript>Regexp]

### [Deleted User] (2020-04-03)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-04-04)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### jg...@chromium.org (2020-04-06)

[Empty comment from Monorail migration]

### jg...@chromium.org (2020-04-06)

The segfault in #4 repros locally in a standard x64 debug build.

### jg...@chromium.org (2020-04-06)

We're attempting to access `registers` OOB:

Thread 1 "d8" received signal SIGSEGV, Segmentation fault.
0x00007f10a74613d3 in v8::internal::(anonymous namespace)::RawMatch<unsigned char> (isolate=0xb1c00000000, code_array=..., subject_string=..., subject=..., registers=0xb1c0000a484, current=0, current_char=10, call_origin=v8::internal::RegExp::kFromJs, backtrack_limit=0)
    at ../../src/regexp/regexp-interpreter.cc:406
406           if (!backtrack_stack.push(registers[insn >> BYTECODE_SHIFT])) {
(gdb) bt
#0  0x00007f10a74613d3 in v8::internal::(anonymous namespace)::RawMatch<unsigned char> (isolate=0xb1c00000000, code_array=..., subject_string=..., subject=..., registers=0xb1c0000a484, current=0, current_char=10, call_origin=v8::internal::RegExp::kFromJs, backtrack_limit=0)
    at ../../src/regexp/regexp-interpreter.cc:406
#1  0x00007f10a7460b88 in v8::internal::IrregexpInterpreter::MatchInternal (isolate=0xb1c00000000, code_array=..., subject_string=..., registers=0xb1c0000a484, registers_length=2, start_position=0, call_origin=v8::internal::RegExp::kFromJs, backtrack_limit=0)
    at ../../src/regexp/regexp-interpreter.cc:994
#2  0x00007f10a74609a2 in v8::internal::IrregexpInterpreter::Match (isolate=0xb1c00000000, regexp=..., subject_string=..., registers=0xb1c0000a484, registers_length=2, start_position=0, call_origin=v8::internal::RegExp::kFromJs) at ../../src/regexp/regexp-interpreter.cc:964
#3  0x00007f10a746e376 in v8::internal::IrregexpInterpreter::MatchForCallFromJs (subject=12214889673017, start_position=0, registers=0xb1c0000a484, registers_length=2, call_origin=v8::internal::RegExp::kFromJs, isolate=0xb1c00000000, regexp=12214887968705)
    at ../../src/regexp/regexp-interpreter.cc:1031
#4  0x00007f10a60fde7e in Builtins_RegExpSearchFast () from /usr/local/google/home/jgruber/src/v8/out/debug/libv8.so
#5  0x00007f10a59e1e43 in Builtins_StringPrototypeSearch () from /usr/local/google/home/jgruber/src/v8/out/debug/libv8.so
#6  0x00007f10a5229675 in Builtins_InterpreterEntryTrampoline () from /usr/local/google/home/jgruber/src/v8/out/debug/libv8.so

The index is

(gdb) p insn >> BYTECODE_SHIFT
$2 = 1802

`registers_length` in frame 1 is 2. 

### jg...@chromium.org (2020-04-06)

This is a general OOB read/write (in a 65k word range around the Isolate's jsregexp_static_offsets_vector). It has been exposed since it was possible to call the regexp interpreter directly from CSA. For jitless mode, since:

https://chromium-review.googlesource.com/c/v8/v8/+/1715451
Is on Canary:    3868
First V8 branch: 7.8.1 (Might not be the rolled version)

For the default (jitting) configuration, since:

https://chromium-review.googlesource.com/c/v8/v8/+/1816501
Is on Canary:    3919
First V8 branch: 7.9.100 (Might not be the rolled version)

Reads / writes are not controlled directly since they are made by the regexp interpreter, following logic of the compiled regexp instance. But it's quite possible that attackers could craft regexp s.t. writes and reads can be made useful, for example by deducing internal regexp interpreter behavior (and thus read values) by looking at the regexp result object.

The root cause is essentially explained here: https://source.chromium.org/chromium/chromium/src/+/master:v8/src/regexp/regexp.cc;l=515;drc=560f2d8bb3f3a72d78e1a7d7654235d53fdcc83c?originalUrl=https:%2F%2Fcs.chromium.org%2F. The interpreter and native code have different expectations on the passed registers array. Native code allocates space for registers on the stack, the interpreter just uses the given registers array. These different expectations were not reflected at the call site here: https://source.chromium.org/chromium/chromium/src/+/master:v8/src/builtins/builtins-regexp-gen.cc;l=417;drc=5306c2e4e655bccaefc2b18646e211b52e92c63b?originalUrl=https:%2F%2Fcs.chromium.org%2F.

The reason this OOB access was not detected earlier is that the registers array is passed as a raw int pointer, and accesses were not bounds-checked in regexp-interpreter.cc.

### jg...@chromium.org (2020-04-06)

My plan is to change interpreter entry point expectations to match those of jitted entry points: 

* `registers` is an array large enough to hold *capture registers*, where '# capture registers' <= '# all registers'.
* It is only modified if the match succeeds.
* Temporary registers are allocated internally.

Additionally:

* Add range DCHECKs for all `registers` accesses in the interpreter. 

### jg...@chromium.org (2020-04-06)

Fix in flight at https://crrev.com/c/2135642. I'll prepare a smaller CL with just the minimal fix for backmerging.

### jg...@chromium.org (2020-04-06)

Correction to #14: I *think* this is not an issue on the shipping config after all. The default setting of --regexp-tier-up-ticks=1 means that the interpreter will be called exactly once. This call is made from the runtime, immediately after generating the bytecode. Only the call from CSA was affected, so if we do not hit that path we are good.

### jg...@chromium.org (2020-04-06)

The minimal fix, intended for backmerging: https://crrev.com/c/2137403

Steps are:

1. Land the minimal fix.
2. Wait for coverage & backmerge.
3. Land the larger CL from #16 on top.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/30658b6b1b672e535e6046fa84674882e29b2279

commit 30658b6b1b672e535e6046fa84674882e29b2279
Author: Jakob Gruber <jgruber@chromium.org>
Date: Mon Apr 06 14:34:34 2020

[regexp] Reserve space for all registers in interpreter

This is a minimal version of https://crrev.com/c/2135642 intended for
backmerges.

Ensure that the interpreter has space for all required registers.

Bug: chromium:1067270
Change-Id: Iefd016b4845fb8698d1e0ef5f6a03df0e66aa576
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2137403
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/master@{#67013}

[modify] https://crrev.com/30658b6b1b672e535e6046fa84674882e29b2279/src/regexp/regexp-interpreter.cc
[add] https://crrev.com/30658b6b1b672e535e6046fa84674882e29b2279/test/mjsunit/regress/regress-1067270.js


### cl...@chromium.org (2020-04-06)

ClusterFuzz testcase 5695191957176320 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=67012:67013

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-04-06)

Is there an estimated timeline for fix and security release?


### jg...@chromium.org (2020-04-06)

The fix landed in #19. Requesting merge to 81 (beta) and 83 (dev) as soon as we have coverage.

PDFium folks, I suppose you will you a merge to 80 (stable)?

### [Deleted User] (2020-04-06)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-06)

This bug requires manual review: We are only 0 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-04-06)

[Empty comment from Monorail migration]

### sr...@google.com (2020-04-06)

jgruber@ M81 is getting promoted to stable tomorrow, So if you merge to M81 that should be enough for stable, M80 is not needed

Can you please help answer the questions for Merge reviews https://crbug.com/chromium/1067270#c24 and #23, 

Also as this is security feature, adding +adetaylor@ to review. 

### pb...@google.com (2020-04-06)

+Adetaylor@(Security TPM)

Since the Cl from https://crbug.com/chromium/1067270#c19 isn't landed on any of the Chrome lower channel, can we consider the fix for next M81 respin.


### pb...@google.com (2020-04-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-07)

jgruber@ are you sure of https://crbug.com/chromium/1067270#c17? And, am I interpreting your comment correctly that this affects zero users of the stable channel? If so, please set this to Security_Impact-None and we should remove all merge requests.

Otherwise - yes, let's merge into the first M81 refresh.

### jg...@chromium.org (2020-04-07)

#30: V8 in chrome is run in multiple configurations. The main config (run in renderer processes) is what I was referring to as 'default'/'shipping'. But PDFium and the proxy resolver (both also inside chrome) use the --jitless configuration. Sorry for the confusion.

The former should not be affected, but the latter are. Thus I believe Security_Impact-None would not be correct.

#23 and #24: 
- Merges requested for https://crrev.com/c/2137403. 
- The change has reached the latest canary 4107 which was published a few minutes ago. 
- No reports yet, I will check back later tomorrow. 
- The change fixes a OOB read/write which affects V8 run in --jitless configuration. 
- The change is as small and safe as possible; for extra confidence I'd like to give this at least a full day in canary before merging.

### jg...@chromium.org (2020-04-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-07)

OK, makes sense - thanks. In that case I'll approve merging to M81 once we've got a couple of days' canary.

### sr...@google.com (2020-04-07)

jgruber@ adetaylor@ we can take this to M83, later this week so it can be in next week dev/beta release so we get more channel coverage before M81 merge.

### ad...@chromium.org (2020-04-07)

Yep that's what I had in mind. I'll approve that now - approving merge to M83 branch 4103. Thanks!

### jg...@chromium.org (2020-04-08)

Canary looking good, merging to M83 now.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ee185bfdefe602da363c08a2485badcc2d5d7172

commit ee185bfdefe602da363c08a2485badcc2d5d7172
Author: Jakob Gruber <jgruber@chromium.org>
Date: Wed Apr 08 05:03:50 2020

Merged: [regexp] Reserve space for all registers in interpreter

This is a minimal version of https://crrev.com/c/2135642 intended for
backmerges.

Ensure that the interpreter has space for all required registers.

(cherry picked from commit 30658b6b1b672e535e6046fa84674882e29b2279)

Tbr: leszeks@chromium.org
No-Try: true
No-Presubmit: true
No-Treechecks: true
Bug: chromium:1067270
Change-Id: Iefd016b4845fb8698d1e0ef5f6a03df0e66aa576
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2137403
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#67013}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2140932
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.3@{#8}
Cr-Branched-From: 1668abddd8147c49c8f2f90b78dc2701f3794a30-refs/heads/8.3.110@{#1}
Cr-Branched-From: 04a7a680a2838e1789f277495181e709e14a17ba-refs/heads/master@{#66926}

[modify] https://crrev.com/ee185bfdefe602da363c08a2485badcc2d5d7172/src/regexp/regexp-interpreter.cc
[add] https://crrev.com/ee185bfdefe602da363c08a2485badcc2d5d7172/test/mjsunit/regress/regress-1067270.js


### jg...@chromium.org (2020-04-08)

[Empty comment from Monorail migration]

### th...@chromium.org (2020-04-08)

For standalone PDFium, I'm rolling DEPS for V8 here: https://pdfium-review.googlesource.com/68490

### na...@google.com (2020-04-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-08)

Congrats! The Panel decided to award $5,000 for this report. 

### na...@google.com (2020-04-08)

[Empty comment from Monorail migration]

### jg...@chromium.org (2020-04-09)

Note: According to omahaproxy the merge in #37 is not part of latest beta 83.0.4103.7.

Canary still looking good.

### jg...@chromium.org (2020-04-09)

I will be OOO until 2020-04-14. I've prepared the merge to 81 at https://crrev.com/c/2144052. Feel free to submit that if the merge is approved, otherwise I can pick this back up on Tuesday.

### jg...@chromium.org (2020-04-14)

Correction to #43: version 83.0.4103.7 is dev channel, not beta.

83.0.4103.7 is still the current dev version, so the merge in #37 still has not reached dev. Is there manual action needed?

### cl...@chromium.org (2020-04-14)

According to the latest release schedule update, another M-83 dev release for desktop and android is planned for today.

### [Deleted User] (2020-04-14)

Do you have a planned date for the public release and disclosure?


### ad...@chromium.org (2020-04-14)

We'd expect this to come out in our next scheduled M81 security respin, which will be next week. However it's not entirely certain yet.

### ad...@google.com (2020-04-15)

Presumably this made it into the dev release 83.0.4103.14.

Approving merge to M81, branch 4044, unless there's any sign of trouble in Canary or dev (I appreciate there won't yet be much in the way of information from dev yet).

### jg...@chromium.org (2020-04-16)

> Presumably this made it into the dev release 83.0.4103.14.

Confirmed.

Merged in https://crrev.com/c/2144052.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/45b8c2bb07d29b99d13081ebe5a7e85952dad4ec

commit 45b8c2bb07d29b99d13081ebe5a7e85952dad4ec
Author: Jakob Gruber <jgruber@chromium.org>
Date: Thu Apr 16 05:27:47 2020

Merged: [regexp] Reserve space for all registers in interpreter

This is a minimal version of https://crrev.com/c/2135642 intended for
backmerges.

Ensure that the interpreter has space for all required registers.

(cherry picked from commit 30658b6b1b672e535e6046fa84674882e29b2279)

Tbr: leszeks@chromium.org
No-Try: true
No-Presubmit: true
No-Treechecks: true
Bug: chromium:1067270
Change-Id: Iefd016b4845fb8698d1e0ef5f6a03df0e66aa576
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2137403
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#67013}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2144052
Reviewed-by: Jakob Gruber <jgruber@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.1@{#61}
Cr-Branched-From: a4dcd39d521d14c4b1cac020812e44ee04a7f244-refs/heads/8.1.307@{#1}
Cr-Branched-From: f22c213304ec3542df87019aed0909b7dafeaa93-refs/heads/master@{#66031}

[modify] https://crrev.com/45b8c2bb07d29b99d13081ebe5a7e85952dad4ec/src/regexp/regexp-interpreter.cc
[add] https://crrev.com/45b8c2bb07d29b99d13081ebe5a7e85952dad4ec/test/mjsunit/regress/regress-1067270.js


### jg...@chromium.org (2020-04-16)

[Empty comment from Monorail migration]

### ma...@chromium.org (2020-04-17)

Looks like the tag bot choked again:
https://ci.chromium.org/p/v8/builders/ci/Auto-tag/2657

Lemme try to bump it manually, so that this merge is taken into account.

### ma...@chromium.org (2020-04-17)

Tagged after https://chromium.googlesource.com/v8/v8/+log/67a2d9761af383e99f84894730418984889add77

### ad...@google.com (2020-04-20)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-04-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/fe60913945bc7c8ff3254a92e0673804432dfb06

commit fe60913945bc7c8ff3254a92e0673804432dfb06
Author: Jakob Gruber <jgruber@chromium.org>
Date: Tue Apr 21 10:13:03 2020

[regexp] Consistent expectations for output registers

... between the interpreter and generated code.

Prior to this CL, pre- and post conditions on the output register
array differed between the interpreter and generated code.

Interpreter
Pre: `output` fits captures and temporary registers.
Post: None.

Generated code
Pre:  `output` fits capture registers.
Post: `output` is modified if and only if the match succeeded.

This CL changes the interpreter to match generated code pre- and
post conditions by allocating space for temporary registers inside
the interpreter.

Drive-by: Add MaxRegisterCount, RegistersForCaptureCount helpers.

Bug: chromium:1067270
Change-Id: I2900ef2f31207d817ec7ead3e0e2215b23b398f0
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2135642
Commit-Queue: Jakob Gruber <jgruber@chromium.org>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/master@{#67268}

[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/builtins/builtins-regexp-gen.cc
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/objects/js-regexp-inl.h
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/objects/js-regexp.h
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/objects/objects.cc
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/regexp/regexp-compiler.cc
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/regexp/regexp-interpreter.cc
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/regexp/regexp-interpreter.h
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/regexp/regexp-macro-assembler.h
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/regexp/regexp.cc
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/src/runtime/runtime-regexp.cc
[modify] https://crrev.com/fe60913945bc7c8ff3254a92e0673804432dfb06/test/cctest/test-regexp.cc


### [Deleted User] (2020-04-21)

Is this planned for today's public disclosure release?


### [Deleted User] (2020-04-22)

Can you provide a date for public disclosure? While the release notes are available via https://chromereleases.googleblog.com/, we want to ensure a coordinated disclosure.

### ad...@chromium.org (2020-04-22)

Hi, apologies for not spotting https://crbug.com/chromium/1067270#c58 in time. Here's the timeline:
1) Fix released (yesterday): a small entry on https://chromereleases.googleblog.com/, as you spotted
2) Sometime in the next few weeks: CVE entry submitted. It will say something like "Out of bounds read and write in PDFium in Google Chrome prior to 81.0.4044.122 allowed a remote attacker to potentially exploit heap corruption via a crafted PDF file." - i.e. it won't have much more information
3) 14 weeks after the bug was fixed, this crbug would be opened to the public.

If you'd like us to move date (3) sooner, so that we open up this bug at the same time as you publish more information, we're open to that. The reason for the 14 week delay is to try to ensure that the vast majority of users have picked up the update. But on request, we are generally OK with opening up a bug as soon as the release is being offered to 100% of users, even if they won't all have accepted, updated and rebooted yet. Unless there are unforeseen problems, that should occur within a week of now. So, let us know if you want us to open up the bug sometime after that but before the 14 weeks.

### [Deleted User] (2020-04-23)

90 day deadline would be 2020-07-02 from initial reporting and we would like to coordinate disclosure on that date (it is only 12-13 days ahead of the 14 weeks from fix)

### ad...@chromium.org (2020-04-23)

Sounds good - please let us know at the time and we'll open up the bug.

### ad...@google.com (2020-05-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-01)

Public disclosure planned for tomorrow 2020-07-02 as mentioned on April 23rd. Open bug


### ad...@chromium.org (2020-07-01)

Thank you! Opening up.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1067270?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>Regexp, Blink>JavaScript>Runtime]
[Monorail mergedwith: crbug.com/chromium/1024697]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051908)*
