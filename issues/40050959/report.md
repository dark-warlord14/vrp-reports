# Security:Potential Use after free in the function ProfilerListener::CodeCreateEvent

| Field | Value |
|-------|-------|
| **Issue ID** | [40050959](https://issues.chromium.org/issues/40050959) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | hi...@gmail.com |
| **Assignee** | pe...@chromium.org |
| **Created** | 2019-12-12 |
| **Bounty** | $2,000.00 |

## Description

the function ProfilerListener::CodeCreateEvent https://cs.chromium.org/chromium/src/v8/src/profiler/profiler-listener.cc?rcl=5a2f2203c80defe0adc943a2c15ff51da7b24196&l=101 use the same raw point script between Garbage Collect, witch may cause UAF(use after GC move the object) 

void ProfilerListener::CodeCreateEvent(CodeEventListener::LogEventsAndTags tag,
                                       AbstractCode abstract_code,
                                       SharedFunctionInfo shared,
                                       Name script_name, int line, int column) {
  CodeEventsContainer evt_rec(CodeEventRecord::CODE_CREATION);
  CodeCreateEventRecord* rec = &evt_rec.CodeCreateEventRecord_;
  rec->instruction_start = abstract_code.InstructionStart();
  std::unique_ptr<SourcePositionTable> line_table;
  std::unordered_map<int, std::vector<CodeEntryAndLineNumber>> inline_stacks;
  std::unordered_set<std::unique_ptr<CodeEntry>, CodeEntry::Hasher,
                     CodeEntry::Equals>
      cached_inline_entries;
  bool is_shared_cross_origin = false;
  if (shared.script().IsScript()) {
    Script script = Script::cast(shared.script());               ------------------->#1 get the raw point script 
    line_table.reset(new SourcePositionTable());
    HandleScope scope(isolate_);

    is_shared_cross_origin = script.origin_options().IsSharedCrossOrigin();

    // Add each position to the source position table and store inlining stacks
    // for inline positions. We store almost the same information in the
    // profiler as is stored on the code object, except that we transform source
    // positions to line numbers here, because we only care about attributing
    // ticks to a given line.
    for (SourcePositionTableIterator it(abstract_code.source_position_table());  ------>#notice the loop
         !it.done(); it.Advance()) {
      int position = it.source_position().ScriptOffset();
      int inlining_id = it.source_position().InliningId();

      if (inlining_id == SourcePosition::kNotInlined) {
        int line_number = script.GetLineNumber(position) + 1;   -------------------------> #4 raw point is use after heap allocation
        line_table->SetPosition(it.code_offset(), line_number, inlining_id);
      } else {
        DCHECK(abstract_code.IsCode());
        Code code = abstract_code.GetCode();
        std::vector<SourcePositionInfo> stack =
            it.source_position().InliningStack(handle(code, isolate_));----------------> #2 InlineStack may cause a GC through path "InliningStack->SourcePositionInfo->GetPositionInfo->InitLineEnds->CalculateLineEnds->NewFixedArray"
        DCHECK(!stack.empty());

        // When we have an inlining id and we are doing cross-script inlining,
        // then the script of the inlined frames may be different to the script
        // of |shared|.
        int line_number = stack.front().line + 1;
        line_table->SetPosition(it.code_offset(), line_number, inlining_id);

        std::vector<CodeEntryAndLineNumber> inline_stack;
        for (SourcePositionInfo& pos_info : stack) {
          if (pos_info.position.ScriptOffset() == kNoSourcePosition) continue;
          if (pos_info.script.is_null()) continue;

          int line_number =
              pos_info.script->GetLineNumber(pos_info.position.ScriptOffset()) +
              1;

          const char* resource_name =
              (pos_info.script->name().IsName())
                  ? GetName(Name::cast(pos_info.script->name()))
                  : CodeEntry::kEmptyResourceName;

          bool inline_is_shared_cross_origin =
              pos_info.script->origin_options().IsSharedCrossOrigin();

          // We need the start line number and column number of the function for
          // kLeafNodeLineNumbers mode. Creating a SourcePositionInfo is a handy
          // way of getting both easily.
          SourcePositionInfo start_pos_info(------------------> #3 SourcePositionInfo May cause GC too
              SourcePosition(pos_info.shared->StartPosition()),
              pos_info.shared);

          std::unique_ptr<CodeEntry> inline_entry = std::make_unique<CodeEntry>(
              tag, GetFunctionName(*pos_info.shared), resource_name,
              start_pos_info.line + 1, start_pos_info.column + 1, nullptr,
              code.InstructionStart(), inline_is_shared_cross_origin);
          inline_entry->FillFunctionInfo(*pos_info.shared);

          // Create a canonical CodeEntry for each inlined frame and then re-use
          // them for subsequent inline stacks to avoid a lot of duplication.
          CodeEntry* cached_entry = GetOrInsertCachedEntry(
              &cached_inline_entries, std::move(inline_entry));

          inline_stack.push_back({cached_entry, line_number});
        }
        DCHECK(!inline_stack.empty());
        inline_stacks.emplace(inlining_id, std::move(inline_stack));
      }
    }
  }
  rec->entry =
      new CodeEntry(tag, GetFunctionName(shared),
                    GetName(InferScriptName(script_name, shared)), line, column,
                    std::move(line_table), abstract_code.InstructionStart(),
                    is_shared_cross_origin);
  if (!inline_stacks.empty()) {
    rec->entry->SetInlineStacks(std::move(cached_inline_entries),
                                std::move(inline_stacks));
  }

  rec->entry->FillFunctionInfo(shared);
  rec->instruction_size = abstract_code.InstructionSize();
  DispatchCodeEvent(evt_rec);
}

Acturaly, this issue is similar to https://bugs.chromium.org/p/v8/issues/detail?id=9992

## Timeline

### oc...@google.com (2019-12-13)

petermashall, could you please help take a look here?

Assuming high severity and stable impact, but please fix them if incorrect.

[Monorail components: Blink>JavaScript]

### sh...@chromium.org (2019-12-13)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-13)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pe...@chromium.org (2019-12-19)

[Empty comment from Monorail migration]

### pe...@chromium.org (2019-12-19)

[Empty comment from Monorail migration]

### pe...@chromium.org (2019-12-19)

We don't run the CPU profiler in production except if devtools is open and the user uses the performance panel, or if tracing is enabled and the cpu profiler category is turned on.

There is one exception which is an origin trial for the JS self profiling API:
https://chromestatus.com/feature/5170190448852992
https://developers.chrome.com/origintrials/#/view_trial/1346576288583778305

Because of that I'm tempted to say this is not a high severity issue, but Facebook is one of the trial origins, so this will still see wide use even in origin trial. Plus this will go into production at some point in the future so it's good that we caught this now.

We should request backmerges to 79 and 80 once we have a fix.



### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/e7ddb89c535eab5cee947d5dd48c614537d33031

commit e7ddb89c535eab5cee947d5dd48c614537d33031
Author: Peter Marshall <petermarshall@chromium.org>
Date: Thu Dec 19 15:04:56 2019

[cpu-profiler] Handlify ProfilerListener and add no_gc scopes

Bug: chromium:1033407
Change-Id: I59642d64fd111884547605f7a010d40e974d2762
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1975752
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Peter Marshall <petermarshall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65524}

[modify] https://crrev.com/e7ddb89c535eab5cee947d5dd48c614537d33031/src/profiler/profiler-listener.cc


### pe...@chromium.org (2019-12-20)

Requesting merge for 80,  but I won't do the merge until 2020-01-02 at the earliest.

### sh...@chromium.org (2019-12-20)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
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
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-20)

[Empty comment from Monorail migration]

### sr...@google.com (2019-12-20)

petermarshall@ pls help answer questions in https://crbug.com/chromium/1033407#c9, for merge review, and yes you can merge after Jan 1 2020

### ad...@google.com (2019-12-20)

Per https://crbug.com/chromium/1033407#c6 let's mark this for backport to M79, though per https://crbug.com/chromium/1033407#c8 it looks like it'll need to wait till next decade to get into beta. I'm OK with that - the limited number of affected websites  in the origin trial (or the need to open devtools) means this is not super-urgent to get backported.

### go...@chromium.org (2019-12-20)

+benmason@ &  +pbommana@ for M79 merge visibility.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/1560bbb9ef8690e4b9648f0411e225180df92397

commit 1560bbb9ef8690e4b9648f0411e225180df92397
Author: Peter Marshall <petermarshall@chromium.org>
Date: Thu Jan 02 09:13:34 2020

[cleanup] Refactor CodeEventListener to use handles

Just a cleanup, should not change behavior, although we will allocate
more handles in some cases.

Also re-orders some of the implementations of the interface to try
and keep things consistent.

Included cleanup: Change CodeEventDispatcher so that it now implements
CodeEventListener, given that it had that exact interface already.
Also remove the macro dispatch to try and make things a bit easier to
read.

Bug: chromium:1033407
Change-Id: Id943b10c49f102d9783d8f4cf3a8c43e04364c77
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1976390
Reviewed-by: Ross McIlroy <rmcilroy@chromium.org>
Reviewed-by: Clemens Backes <clemensb@chromium.org>
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Peter Marshall <petermarshall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65571}

[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/builtins/builtins.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/codegen/compiler.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/deoptimizer/deoptimizer.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/diagnostics/perf-jit.h
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/logging/code-events.h
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/logging/log.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/logging/log.h
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/objects/objects.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/profiler/profiler-listener.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/profiler/profiler-listener.h
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/regexp/arm/regexp-macro-assembler-arm.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/regexp/arm64/regexp-macro-assembler-arm64.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/regexp/ia32/regexp-macro-assembler-ia32.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/regexp/mips/regexp-macro-assembler-mips.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/regexp/mips64/regexp-macro-assembler-mips64.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/regexp/ppc/regexp-macro-assembler-ppc.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/regexp/s390/regexp-macro-assembler-s390.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/regexp/x64/regexp-macro-assembler-x64.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/runtime/runtime-test.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/snapshot/code-serializer.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/snapshot/serializer.h
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/src/wasm/function-compiler.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/test/cctest/test-cpu-profiler.cc
[modify] https://crrev.com/1560bbb9ef8690e4b9648f0411e225180df92397/test/cctest/test-log.cc


### pe...@chromium.org (2020-01-02)

Merge guidelines:
1. Yes due to security issue.
2. https://chromium-review.googlesource.com/c/v8/v8/+/1975752
3. Yes, landed and no issues
4. Existing security bug
5. Not a new feature
6. N/A

I'm ready to merge when we have merge approval.

### sr...@google.com (2020-01-02)

Merge approved for M80, branch:3987

+adetaylor@ FYI

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/afdd55e8f5a853d410c04a7cf37679fb870714a0

commit afdd55e8f5a853d410c04a7cf37679fb870714a0
Author: Peter Marshall <petermarshall@chromium.org>
Date: Fri Jan 03 09:01:26 2020

Merged: [cpu-profiler] Handlify ProfilerListener and add no_gc scopes

Revision: e7ddb89c535eab5cee947d5dd48c614537d33031

BUG=chromium:1033407
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
TBR=sigurds@chromium.org

Change-Id: I30020b5fb76aebe0aa98cf8b4a134f9088184009
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1980703
Reviewed-by: Peter Marshall <petermarshall@chromium.org>
Commit-Queue: Peter Marshall <petermarshall@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.0@{#16}
Cr-Branched-From: 69827db645fcece065bf16a795a4ec8d3a51057f-refs/heads/8.0.426@{#2}
Cr-Branched-From: 2fe1552c5809d0dd92e81d36a5535cbb7c518800-refs/heads/master@{#65318}

[modify] https://crrev.com/afdd55e8f5a853d410c04a7cf37679fb870714a0/src/profiler/profiler-listener.cc


### pe...@chromium.org (2020-01-03)

Merge to 80 is done, I can merge to 79 if required/approved

### pb...@chromium.org (2020-01-05)

pertermarshall@ I will approve for M79 merge once we have M80 Beta coverage next week. 

### sh...@chromium.org (2020-01-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### na...@google.com (2020-01-06)

[Empty comment from Monorail migration]

### sr...@google.com (2020-01-06)

Please help complete the merges to M80 branch:3987 by eod Monday Jan 6 so your changes can be included in this week's beta release. 

### pe...@chromium.org (2020-01-07)

Will check next week.

### na...@google.com (2020-01-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-09)

Congrats! The Panel decided to reward $2,000 for this report!

### na...@google.com (2020-01-09)

[Empty comment from Monorail migration]

### pb...@chromium.org (2020-01-10)

Please let us know how is the change looking in Beta?

If everything looks good we would like to get the CL merged to M79 Stable ASAP.

### pe...@chromium.org (2020-01-13)

Beta looks good to me.

### go...@chromium.org (2020-01-13)

Approving merge to M79 branch 3945 based on https://crbug.com/chromium/1033407#c28. Please merge ASAP so we can take it in for this week M79 stable respin. Thank you.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/97d4eb67e406f3a4f48901c4a6720f8f9c4c9dde

commit 97d4eb67e406f3a4f48901c4a6720f8f9c4c9dde
Author: Peter Marshall <petermarshall@chromium.org>
Date: Tue Jan 14 13:21:37 2020

Merged: [cpu-profiler] Handlify ProfilerListener and add no_gc scopes

Revision: e7ddb89c535eab5cee947d5dd48c614537d33031

BUG=chromium:1033407
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=sigurds@chromium.org

TBR=sigurds@chromium.org

Change-Id: I96f581419f27ac35fabb2ffab1d20bff8a06460c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2000598
Reviewed-by: Peter Marshall <petermarshall@chromium.org>
Commit-Queue: Peter Marshall <petermarshall@chromium.org>
Cr-Commit-Position: refs/branch-heads/7.9@{#65}
Cr-Branched-From: be181e241c6da9baa49a424b7d91613c8ebf76f8-refs/heads/7.9.317@{#1}
Cr-Branched-From: 0d7889d0b14939fa5c09c39a0a5eb155b74163e4-refs/heads/master@{#64307}

[modify] https://crrev.com/97d4eb67e406f3a4f48901c4a6720f8f9c4c9dde/src/profiler/profiler-listener.cc


### pe...@chromium.org (2020-01-14)

Merged to 79 completed

### mm...@chromium.org (2020-01-14)

petermarshall@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### go...@chromium.org (2020-01-14)

+cindyb@ (Chrome OS M79 Release TPM)

### ad...@google.com (2020-01-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-01-15)

[Empty comment from Monorail migration]

### hi...@gmail.com (2020-01-21)

Please help change my credit information from "Guang Gong of Alpha Team" to "Guang Gong of Alpha Lab" from now on, thanks.

### ad...@chromium.org (2020-01-21)

higongguang@ - specifically, "Guang Gong of Alpha Lab" or "Guang Gong of Alpha Lab, Qihoo 360"?

(For now I've put the former). Thanks for all your continuing great reports.

### mm...@chromium.org (2020-01-21)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-01-21)

Hey Peter, thanks a lot for submitting the analysis form. Can the CPU profiler be enabled via command line flags? That way it would be trivial for us to enable it on a trial basis for JS fuzzers running on ClusterFuzz.

### hi...@gmail.com (2020-01-22)

adetaylor@  "Guang Gong of Alpha Lab, Qihoo 360", Thanks

### ad...@google.com (2020-01-22)

Done, thanks.

### pe...@chromium.org (2020-01-22)

Opened this bug for adding a flag to D8 for the fuzzer: https://bugs.chromium.org/p/v8/issues/detail?id=10150

### ad...@chromium.org (2020-02-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1033407?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050959)*
