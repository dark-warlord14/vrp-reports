# V8 debug check failed: new_target->IsConstructor()

| Field | Value |
|-------|-------|
| **Issue ID** | [40057873](https://issues.chromium.org/issues/40057873) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | et...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2021-11-10 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36

Steps to reproduce the problem:
The earliest version I tested for this vulnerability was v8 6.9, and it also exists in the latest version.

build the latest version of v8 and then

./d8 poc.js

poc
```
function main() {
    'use strict';
    class LeakyPromise extends Promise {
        constructor() {
            super(
                () => { }
            );
        }
    }
    let p1 = new LeakyPromise(class extends LeakyPromise { });
}
main();
```

What is the expected behavior?

What went wrong?
sakura@sakuradeMacBook-Pro:~/Desktop/v8/v8/out/fuzzbuild$ ./d8 poc.js

#
# Fatal error in ../../src/objects/js-objects.cc, line 2040
# Debug check failed: new_target->IsConstructor().
#
#
#
#FailureMessage Object: 0x7ffee61ca450
==== C stack trace ===============================

    0   d8                                  0x0000000109aa8903 v8::base::debug::StackTrace::StackTrace() + 19
    1   d8                                  0x0000000109aad08d v8::platform::(anonymous namespace)::PrintStackTrace() + 45
    2   d8                                  0x0000000109aa0421 V8_Fatal(char const*, int, char const*, ...) + 337
    3   d8                                  0x0000000109a9ff95 v8::base::(anonymous namespace)::DefaultDcheckHandler(char const*, int, char const*) + 21
    4   d8                                  0x000000010a05d5c0 v8::internal::JSObject::New(v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::JSReceiver>, v8::internal::Handle<v8::internal::AllocationSite>) + 608
    5   d8                                  0x000000010a2e2625 v8::internal::__RT_impl_Runtime_NewObject(v8::internal::Arguments, v8::internal::Isolate*) + 245
    6   d8                                  0x000000010ad84fbf Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit + 63
    7   d8                                  0x000000010aea36ca Builtins_PromiseConstructor + 3658
    8   d8                                  0x000000010ab26830 Builtins_JSBuiltinsConstructStub + 144
Received signal 4 <unknown> 000109aa6cb2
Illegal instruction: 4

Did this work before? N/A 

Chrome version: 95.0.4638.69  Channel: stable
OS Version: OS X 10.15.7

credit:
Nan Wang(@eternalsakura13) and Guang Gong of 360 Alpha Lab

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 249 B)

## Timeline

### [Deleted User] (2021-11-10)

[Empty comment from Monorail migration]

### et...@gmail.com (2021-11-10)

please CC higongguang@gmail.com, thanks

### ts...@chromium.org (2021-11-10)

Reporters: Can you explain why you think this is a type confusion rather than just hitting a debug check?  Running d8 built with either -fsanitize=address or fsanitize=vptr doesn't flag any corruption. 

Marking as a functional bug rather than a security issue per-se, but keeping view-restrictions for the moment out of an abundance of caution. Assigning per v8 triage rotation.

### ec...@google.com (2021-11-10)

Not sure why I was added as an owner here. This looks like a runtime issue to me.

[Monorail components: Blink>JavaScript>Runtime]

### is...@chromium.org (2021-11-10)

[Empty comment from Monorail migration]

### et...@gmail.com (2021-11-11)

[Comment Deleted]

### et...@gmail.com (2021-11-11)

[Comment Deleted]

### cl...@chromium.org (2021-11-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5561618844680192.

### cl...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-11)

Detailed Report: https://clusterfuzz.com/testcase?key=5561618844680192

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  new_target->IsConstructor() in js-objects.cc
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=49659:49660

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5561618844680192

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5561618844680192 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### is...@chromium.org (2021-11-11)

There's an issue in Ignition register optimizer.

Smaller repro:
```
function main() {
    'use strict';
    class A {};
    new A(class extends A {});
}
main();
```

[generated bytecode for function: main (0x09a80025346d <SharedFunctionInfo main>)]
Bytecode length: 51
Parameter count 1
Register count 7
Frame size 56
OSR nesting level: 0
Bytecode Age: 0
         0x9a8002537da @    0 : 10                LdaTheHole
         0x9a8002537db @    1 : c0                Star4
         0x9a8002537dc @    2 : 80 01 00 02       CreateClosure [1], [0], #2
         0x9a8002537e0 @    6 : c3                Star1
         0x9a8002537e1 @    7 : 13 00             LdaConstant [0]
         0x9a8002537e3 @    9 : c2                Star2
         0x9a8002537e4 @   10 : 19 f9 f7          Mov r1, r3
         0x9a8002537e7 @   13 : 65 24 00 f8 03    CallRuntime [DefineClass], r2-r4
         0x9a8002537ec @   18 : bf                Star5
         0x9a8002537ed @   19 : 19 f7 fa          Mov r3, r0
         0x9a8002537f0 @   22 : 80 03 01 02       CreateClosure [3], [1], #2
         0x9a8002537f4 @   26 : c2                Star2                                          <-------------- This is a class constructor r2
         0x9a8002537f5 @   27 : 13 02             LdaConstant [2]
         0x9a8002537f7 @   29 : c1                Star3
         0x9a8002537f8 @   30 : 19 f8 f6          Mov r2, r4                              <-------------- We pass it to the DefineClass in a r4 register
         0x9a8002537fb @   33 : 19 fa f5          Mov r0, r5
         0x9a8002537fe @   36 : 65 24 00 f7 03    CallRuntime [DefineClass], r3-r5
         0x9a800253803 @   41 : be                Star6
         0x9a800253804 @   42 : 0b f5             Ldar r5                                    <--------------  Here it wanted to generate Ldar r2, but REO decided to use r5 (not even r4!)
         0x9a800253806 @   44 : 69 f9 f8 01 00    Construct r1, r2-r2, [0]
         0x9a80025380b @   49 : 0e                LdaUndefined
         0x9a80025380c @   50 : a9                Return



### et...@gmail.com (2021-11-11)

I think this may be a potential security issue and should not be a bug, but I have not found a good way... :(

### et...@gmail.com (2021-11-16)

Hello, can this be considered a security bug?

### le...@chromium.org (2021-11-16)

[Empty comment from Monorail migration]

### le...@chromium.org (2021-11-16)

The register optimizer is fine here, we want to generate Ldar r1 at 42 which should indeed be in r5 (as per 10, 19 and 33).

What's weird, however, is that r5 seems to be mutated after DefineClass:

 -> 0x2ff0082937e6 @   36 : 65 24 00 f7 03    CallRuntime [DefineClass], r3-r5
      [          r3 -> 0x2ff008293765 <FixedArray[7]> ]
      [          r4 -> 0x2ff00810a519 <JSFunction (sfi = 0x2ff008293609)> ]
      [          r5 -> 0x2ff00810a479 <JSFunction A (sfi = 0x2ff0082935d1)> ]
      [ accumulator <- 0x2ff00810a539 <JSObject> ]
 -> 0x2ff0082937eb @   41 : c1                Star3
      [ accumulator -> 0x2ff00810a539 <JSObject> ]
      [          r3 <- 0x2ff00810a539 <JSObject> ]
 -> 0x2ff0082937ec @   42 : 0b f5             Ldar r5
      [          r5 -> 0x2ff00810a539 <JSObject> ]
      [ accumulator <- 0x2ff00810a539 <JSObject> ]

### le...@google.com (2021-11-16)

Ah, this is because DefineClass clobbers the ClassBoilerplate::kPrototypeArgumentIndex argument, which is located on the interpreter's register frame: https://source.chromium.org/chromium/chromium/src/+/main:v8/src/runtime/runtime-classes.cc;l=632;drc=bb9766450d67ee8c4431d5236508795c0c006499

### le...@google.com (2021-11-16)

re: #14 -- I think this could be a security bug, yes: it forces a type confusion between constructor and prototype as the call target of the Construct, so I could imagine a carefully constructed prototype object being able to trigger a call to an arbitrary location.

### et...@gmail.com (2021-11-16)

re #18
Can you change Type to bug-security? thanks :)


### le...@google.com (2021-11-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/9b5f39855448c9dc283832063c4e9e1c4dd07246

commit 9b5f39855448c9dc283832063c4e9e1c4dd07246
Author: Leszek Swirski <leszeks@chromium.org>
Date: Tue Nov 16 12:01:16 2021

[runtime] Reset clobbered argument in DefineClass

The caller of DefineClass may not expect its arguments to be mutated, so
add an arguments mutation scope which resets the argument clobbered by
DefineClass.

Bug: chromium:1268738
Change-Id: I03e9cd82535ca1f83353012a92e80f822566e64e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3283077
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77921}

[modify] https://crrev.com/9b5f39855448c9dc283832063c4e9e1c4dd07246/src/runtime/runtime-classes.cc
[modify] https://crrev.com/9b5f39855448c9dc283832063c4e9e1c4dd07246/src/execution/arguments.h


### gi...@appspot.gserviceaccount.com (2021-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6ffcdddbc2d9109dfab0caf7e3e428728e830090

commit 6ffcdddbc2d9109dfab0caf7e3e428728e830090
Author: Nico Hartmann <nicohartmann@chromium.org>
Date: Tue Nov 16 13:57:26 2021

Revert "[runtime] Reset clobbered argument in DefineClass"

This reverts commit 9b5f39855448c9dc283832063c4e9e1c4dd07246.

Reason for revert: https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64%20GC%20Stress%20-%20custom%20snapshot/39804/overview

Original change's description:
> [runtime] Reset clobbered argument in DefineClass
>
> The caller of DefineClass may not expect its arguments to be mutated, so
> add an arguments mutation scope which resets the argument clobbered by
> DefineClass.
>
> Bug: chromium:1268738
> Change-Id: I03e9cd82535ca1f83353012a92e80f822566e64e
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3283077
> Auto-Submit: Leszek Swirski <leszeks@chromium.org>
> Commit-Queue: Igor Sheludko <ishell@chromium.org>
> Reviewed-by: Igor Sheludko <ishell@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#77921}

Bug: chromium:1268738
Change-Id: I878bd78f8ed265c18cd01e3105a69c8a8f876208
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3284886
Owners-Override: Nico Hartmann <nicohartmann@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Commit-Queue: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77924}

[modify] https://crrev.com/6ffcdddbc2d9109dfab0caf7e3e428728e830090/src/runtime/runtime-classes.cc
[modify] https://crrev.com/6ffcdddbc2d9109dfab0caf7e3e428728e830090/src/execution/arguments.h


### [Deleted User] (2021-11-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/85ab0ad7789a7188b4c0b2be3cd3d758134c7de6

commit 85ab0ad7789a7188b4c0b2be3cd3d758134c7de6
Author: Leszek Swirski <leszeks@chromium.org>
Date: Wed Nov 17 09:33:14 2021

Reland "[runtime] Reset clobbered argument in DefineClass"

This is a reland of 9b5f39855448c9dc283832063c4e9e1c4dd07246

Reland fixes:
 * Store a Handle instead of a raw pointer in the scope, to make sure
   the saved object stays alive.

Original change's description:
> [runtime] Reset clobbered argument in DefineClass
>
> The caller of DefineClass may not expect its arguments to be mutated, so
> add an arguments mutation scope which resets the argument clobbered by
> DefineClass.
>
> Bug: chromium:1268738
> Change-Id: I03e9cd82535ca1f83353012a92e80f822566e64e
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3283077
> Auto-Submit: Leszek Swirski <leszeks@chromium.org>
> Commit-Queue: Igor Sheludko <ishell@chromium.org>
> Reviewed-by: Igor Sheludko <ishell@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#77921}

Bug: chromium:1268738
Change-Id: I934ba2063bf2b0e66a3c42f274419ddd178e4b54
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3289146
Auto-Submit: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Igor Sheludko <ishell@chromium.org>
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#77945}

[modify] https://crrev.com/85ab0ad7789a7188b4c0b2be3cd3d758134c7de6/src/execution/arguments-inl.h
[modify] https://crrev.com/85ab0ad7789a7188b4c0b2be3cd3d758134c7de6/src/runtime/runtime-classes.cc
[modify] https://crrev.com/85ab0ad7789a7188b4c0b2be3cd3d758134c7de6/src/execution/arguments.h


### cl...@chromium.org (2021-11-17)

ClusterFuzz testcase 5561618844680192 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=77944:77945

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### et...@gmail.com (2021-11-18)

Can I get a bounty and cve for this issue?

### le...@chromium.org (2021-11-18)

Assigning to current security sheriff

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-11-18)

Yep! This will be eligible for a CVE and a reward. You'll automatically be considered, see https://crbug.com/chromium/1268738#c28.

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-18)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M96. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M97. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-18)

Merge review required: M97 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-18)

Merge review required: M96 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mp...@chromium.org (2021-11-18)

[Empty comment from Monorail migration]

### le...@chromium.org (2021-11-19)

1. Why does your merge fit within the merge criteria for these milestones?
Medium severity or higher security issue (V8 type confusion)

2. What changes specifically would you like to merge? Please link to Gerrit.
https://chromium-review.googlesource.com/c/v8/v8/+/3289146

3. Have the changes been released and tested on canary?
Released in 98.0.4712.0, on Canary ~1 day so far with no reported issues

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.
No, the repro requires a debug build and I'm confident that the fix in Canary will be an equivalent fix in Beta/Stable

### va...@chromium.org (2021-11-19)

Thanks leszeks@
Please back merge the fix into the V8 branch 9.6 and 9.7

@ Security and Release TPMs. Please consider this fix for the next respin. Thanks!

### va...@chromium.org (2021-11-19)

[Empty comment from Monorail migration]

### le...@chromium.org (2021-11-19)

Merged into 97 in https://chromium-review.googlesource.com/c/v8/v8/+/3289179 and 96 in https://chromium-review.googlesource.com/c/v8/v8/+/3289176

### [Deleted User] (2021-11-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-11-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### et...@gmail.com (2021-11-24)

[Comment Deleted]

### am...@chromium.org (2021-11-24)

The increased/bonus amount you mention is for the V8 exploit bonus [https://bughunters.google.com/about/rules/5745167867576320 -> V8 Exploit Bonus], the primary criteria for which is "reports affecting V8 which clearly demonstrate exploitability may qualify for increased rewards". This report did not clearly demonstrate exploitability or provide an analysis of how exploitability would be achieved. It was the analysis and explanation from the V8 team in https://crbug.com/chromium/1268738#c18 that provided this. 

### et...@gmail.com (2021-11-24)

[Comment Deleted]

### et...@gmail.com (2021-11-24)

[Comment Deleted]

### et...@gmail.com (2021-11-24)

[Comment Deleted]

### am...@chromium.org (2021-11-24)

Hello, thanks for your question. The VRP Panel had a in-depth discussion about this report like we do with all reports just yesterday. As mentioned in my comment above (https://crbug.com/chromium/1268738#c42) the primarily eligibility parameter is for "reports affecting V8 which clearly demonstrate exploitability", meaning the report submitted by the researcher (you) would have to clearly demonstrate that exploitability. 
To be eligible for the V8 exploit bonus, you would need to have clearly demonstrated that in the report rather than depending on the V8 team to perform that analysis and determine that. In https://crbug.com/chromium/1268738#c13, you convey the security impact of this issue is only potentially speculative and you were unable to find a way to exploit. We still appreciate the effort and your findings in the report, which is why it was still eligible for and received a VRP reward - with the V8 team providing that analysis of this being an exploitable security issue, but this report is not eligible for the V8 exploit bonus. 

### et...@gmail.com (2021-11-24)

[Comment Deleted]

### am...@chromium.org (2021-11-24)

You're very welcome for the reply. As mentioned, we did already have this discussion within the VRP Panel and the reward amount was deemed appropriate and the report not eligible for the V8 exploit bonus. We look forward to future reports and glad to hear you will consider this feedback in those future reports. 

### ve...@chromium.org (2021-11-24)

Actually I'm not convinced this causes security-relevant type confusion.

This only allows you to swap the super constructor (a JSFunction, JSProxy, or null) for a JSObject. In the given example this leaks into [[construct]] as the privileged new.target parameter, which could lead to an issue, but doesn't as the code beyond the DCHECK gracefully handles it not being a constructor. You'd need to find another place where the interpreter has an internal use for a super constructor (JSFunction, JSProxy, or null) and a use that's unsafe. Since the interpreter generally has very little knowledge of the values floating around, I wouldn't be surprised if there are no such uses.

### am...@google.com (2021-11-24)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-11-29)

Your change has been approved for M97 branch,please go ahead and merge the CL's to M97 branch:4692 manually asap so that they would be part of this week's first M97 Beta release.

### le...@chromium.org (2021-11-30)

Already merged.

### [Deleted User] (2021-12-06)

[Empty comment from Monorail migration]

### et...@gmail.com (2021-12-07)

Can I get a cve for this issue？

### ad...@chromium.org (2021-12-07)

Yes - I'll take care of it tomorrow, and adjust the release notes to credit you - sorry for the omission - the commit was oddly labeled so our processes didn't pick it up.

### va...@chromium.org (2021-12-07)

Cleanup as V8-postmortem was added without the PM comment.

### [Deleted User] (2021-12-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-12-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-12-07)

CVE assigned and release notes updated - https://chromereleases.googleblog.com/2021/12/stable-channel-update-for-desktop.html - sorry about that!

### va...@chromium.org (2021-12-07)

Cleanup as V8-postmortem was added without the PM comment.

### [Deleted User] (2021-12-08)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.975983575=leszeks@chromium.org&entry.307501673=1268738&entry.364066060=External&entry.958145677=Linux&entry.958145677=Mac&entry.958145677=Windows&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Runtime Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-12-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/1da4b373a72137fb386927c0e4984520d46b0448

commit 1da4b373a72137fb386927c0e4984520d46b0448
Author: Stephen Roettger <sroettger@google.com>
Date: Wed May 18 12:55:18 2022

Replace more args.set_at usages with ChangeValueScope

args.set_at lead to a vulnerability in the past where the caller
(ignition) didn't expect the callee to overwrite the arguments.

The current usage doesn't look like an issue, but let's preemptively
remove these usages so that they don't lead to issues in the future.

Change-Id: I64e1f84ad1833b2b2f96cd7503bdde00f344404c
Bug: chromium:1268738
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3644965
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Commit-Queue: Stephen Röttger <sroettger@google.com>
Cr-Commit-Position: refs/heads/main@{#80641}

[modify] https://crrev.com/1da4b373a72137fb386927c0e4984520d46b0448/src/builtins/builtins-api.cc
[modify] https://crrev.com/1da4b373a72137fb386927c0e4984520d46b0448/src/builtins/builtins-array.cc
[modify] https://crrev.com/1da4b373a72137fb386927c0e4984520d46b0448/src/builtins/builtins-utils-inl.h
[modify] https://crrev.com/1da4b373a72137fb386927c0e4984520d46b0448/src/builtins/builtins-utils.h


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1268738?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057873)*
