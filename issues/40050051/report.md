# Security: Use After Free in the function JavaScriptFrame::Summarize

| Field | Value |
|-------|-------|
| **Issue ID** | [40050051](https://issues.chromium.org/issues/40050051) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | cl...@chromium.org |
| **Created** | 2019-09-04 |
| **Bounty** | $7,500.00 |

## Description

"abstract_code" is not protected by Handle, and is use after a GC, which will cause use after free(gc moved this object)

void JavaScriptFrame::Summarize(std::vector<FrameSummary>* functions) const {
  DCHECK(functions->empty());
  Code code = LookupCode();      
  int offset = static_cast<int>(pc() - code.InstructionStart());
  AbstractCode abstract_code = AbstractCode::cast(code);    ---------------------> the raw point defines here
  Handle<FixedArray> params = GetParameters();  ---------->this function may call a GC.
  FrameSummary::JavaScriptFrameSummary summary(
      isolate(), receiver(), function(), abstract_code, offset, IsConstructor(),
      *params);----------->abstract_code is reused in this line
  functions->push_back(summary);
}


a poc is attached as re.js, run it with the following argument
./d8 --stress-compaction --detailed-error-stack-trace te.js
you'll got a crash backtrace as 

Thread 1 "d8" received signal SIGSEGV, Segmentation fault.
0x00007fed94ccbdfc in v8::base::Relaxed_Load (ptr=...) at atomicops_internals_portable.h:183
183	  return __atomic_load_n(ptr, __ATOMIC_RELAXED);
(gdb) bt
#0  0x00007fed94ccbdfc in v8::base::Relaxed_Load (ptr=...) at atomicops_internals_portable.h:183
#1  0x00007fed94ccbdad in v8::base::AsAtomicImpl<long>::Relaxed_Load<unsigned long> (addr=...) at atomic-utils.h:78
#2  0x00007fed94ccbd20 in v8::internal::FullObjectSlot::Relaxed_Load (this=...) at slots-inl.h:41
#3  0x00007fed94ccbc52 in v8::internal::HeapObject::map_word (this=...) at objects-inl.h:701
#4  0x00007fed94ccbb45 in v8::internal::HeapObject::map (this=...) at objects-inl.h:642
#5  0x00007fed92f013a5 in v8::internal::HeapObject::IsBytecodeArray (this=...) at instance-type-inl.h:64
#6  0x00007fed931da03c in v8::internal::FrameSummary::JavaScriptFrameSummary::JavaScriptFrameSummary (this=..., isolate=..., receiver=..., function=..., abstract_code=..., 
    code_offset=..., is_constructor=..., parameters=...) at frames.cc:1303
#7  0x00007fed931dcd8b in v8::internal::InterpretedFrame::Summarize (this=..., functions=...) at frames.cc:1785
#8  0x00007fed931eaea7 in v8::internal::Isolate::ComputeLocation (this=..., target=...) at isolate.cc:2059
#9  0x00007fed931ea1d7 in v8::internal::Isolate::Throw (this=..., raw_exception=..., location=...) at isolate.cc:1558
#10 0x00007fed92e9a8ed in v8::internal::Isolate::Throw<v8::internal::Object> (this=..., exception=..., location=...) at isolate.h:762
#11 0x00007fed933e828a in v8::internal::IC::ReferenceError (this=..., name=...) at ic.cc:319
#12 0x00007fed933e9197 in v8::internal::LoadIC::Load (this=..., object=..., name=...) at ic.cc:508
#13 0x00007fed933e9f3c in v8::internal::LoadGlobalIC::Load (this=..., name=...) at ic.cc:551
#14 0x00007fed933f72a5 in v8::internal::__RT_impl_Runtime_LoadGlobalIC_Miss (args=..., isolate=...) at ic.cc:2269
#15 0x00007fed933f6d72 in v8::internal::Runtime_LoadGlobalIC_Miss (args_length=..., args_object=..., isolate=...) at ic.cc:2244
#16 0x00007fed9452a920 in Builtins_CEntry_Return1_DontSaveFPRegs_ArgvOnStack_NoBuiltinExit () from /home/ggong/ssd2/v8/v8/out/x64.debug/libv8.so
#17 0x00007fed9469c083 in Builtins_LdaGlobalHandler () from /home/ggong/ssd2/v8/v8/out/x64.debug/libv8.so
#18 0x0000000100000000 in ?? ()
#19 0x00000fd139c5deb1 in ?? ()
#20 0x0000000000000000 in ?? ()

I've only tested this on V8 version 7.6.303.29, but the master branch is affected too.

## Attachments

- [te.js](attachments/te.js) (text/plain, 509 B)

## Timeline

### cl...@chromium.org (2019-09-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5760326368100352.

### cl...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-09-04)

Testcase 5760326368100352 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5760326368100352.

### es...@chromium.org (2019-09-04)

Passing over to v8 sheriff for further triage. Can you please set a Security_Impact label? Thanks!

[Monorail components: Blink>JavaScript]

### ms...@chromium.org (2019-09-05)

+Maya, potentially another thing a smartified gcmole could learn.

### cl...@chromium.org (2019-09-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6237084112519168.

### cl...@chromium.org (2019-09-05)

Testcase 6237084112519168 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6237084112519168.

### cl...@chromium.org (2019-09-05)

I can reproduce locally with '--stress-compaction --detailed-error-stack-trace --gc-interval=1'. Will retry on ClusterFuzz.

### cl...@chromium.org (2019-09-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6227416074027008.

### cl...@chromium.org (2019-09-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5972048660004864.

### cl...@chromium.org (2019-09-05)

Testcase 5972048660004864 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5972048660004864.

### cl...@chromium.org (2019-09-05)

Testcase 6227416074027008 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6227416074027008.

### cl...@chromium.org (2019-09-05)

Clusterfuzz fails to reproduce (maybe because of --disable-in-process-stack-traces), but it reproduces locally. The fix is straight-forward, will upload a CL soon.

FYI, InterpretedFrame::Summarize has the same problem.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/fba03abcfaa11e889bf0623eb58772b1f6a7d89f

commit fba03abcfaa11e889bf0623eb58772b1f6a7d89f
Author: Clemens Hammacher <clemensh@chromium.org>
Date: Thu Sep 05 15:42:59 2019

Correctly handlify two frame {Summarize} methods

{JavaScriptFrame::GetParameters} allocates a new {FixedArray}, hence
all object references need to be handified to survive that allocation.

R=mstarzinger@chromium.org

Bug: chromium:1000635
Change-Id: I76df5ac109bdb6999fe897bdafaf2175344ecca4
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1787429
Reviewed-by: Michael Starzinger <mstarzinger@chromium.org>
Commit-Queue: Clemens Hammacher <clemensh@chromium.org>
Cr-Commit-Position: refs/heads/master@{#63583}

[modify] https://crrev.com/fba03abcfaa11e889bf0623eb58772b1f6a7d89f/src/execution/frames.cc
[add] https://crrev.com/fba03abcfaa11e889bf0623eb58772b1f6a7d89f/test/mjsunit/regress/regress-1000635.js


### cl...@chromium.org (2019-09-05)

This should be merged to M-77 after canary coverage.

### sh...@chromium.org (2019-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-06)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M76. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M77. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-06)

This bug requires manual review: We are only 3 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-09-06)

We are going to M77 Stable launch in couple of days and this is not an RBS. Please target M78.



### cl...@chromium.org (2019-09-06)

Ok, thanks. Will request merge to M-78 once canary coverage is there.

### na...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-09-09)

Not in todays, Canary, postponing backmerge decision to tomorrow.

### cl...@chromium.org (2019-09-11)

Looks good on canary. Requesting merge to M-78.

### sh...@chromium.org (2019-09-11)

This bug requires manual review: We don't branch M78 until 2019-09-05.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-09-11)

Answers to #24:

1. Does your merge fit within the Merge Decision Guidelines?
YES
2. Links to the CLs you are requesting to merge.
commit fba03abcfaa11e889bf0623eb58772b1f6a7d89f
3. Has the change landed and been verified on master/ToT?
YES
4. Why are these changes required in this milestone after branch?
FIXING SECURITY ISSUE
5. Is this a new feature?
NO
6. If it is a new feature, is it behind a flag using finch?
N/A

### sr...@google.com (2019-09-11)

approved for merge to M78, branch:3904

### ad...@google.com (2019-09-11)

Now we've got M77 out the door we should put this in the first security respin, right @lakpamarthy?

### sh...@chromium.org (2019-09-11)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2019-09-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2019-09-12)

Merged to M-78 in https://crrev.com/c/1798683.

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $7,500 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-19)

lakpamarthy@ please can you approve this merge to 77 so it's ready for the next security respin, assuming it's had no trouble in beta. This has a test case attached so it would be especially urgent to get it out there.

### la...@google.com (2019-09-27)

merge approved for M77 branch 3865

### sh...@chromium.org (2019-10-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-10-01)

Merged in https://crrev.com/c/1833691.

### ad...@google.com (2019-10-07)

Assuming impacts all OSs with V8.

### ad...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-07)

[Empty comment from Monorail migration]

### ms...@chromium.org (2019-11-13)

Regarding why GCMole is not catching this - it's possible that the JavaScriptFrameSummary constructor is not correctly inspected as a GC suspect. We already have a similar known issue when the GC suspect is a static function, see https://bugs.chromium.org/p/v8/issues/detail?id=9680.
Will write a test and investigate further.

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1000635?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050051)*
