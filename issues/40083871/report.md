# Crash in v8::internal::StackFrameIterator::StackFrameIterator

| Field | Value |
|-------|-------|
| **Issue ID** | [40083871](https://issues.chromium.org/issues/40083871) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **CVE IDs** | CVE-2016-1678 |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-03-16 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4993595320303616

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x000097dd3bd4
Crash State:
  v8::internal::StackFrameIterator::StackFrameIterator
  v8::internal::Isolate::PrintStack
  v8::internal::Isolate::StackTraceString
  
Regressed: V8: r34570:34571

Minimized Testcase (9.61 Kb): https://cluster-fuzz.appspot.com/download/AMIfv953Nhg-5a0o5TdwTd-mKkdqM_F47EhyPsL0SDxGFxizs4c8nnmwyPCllLbQJb4LYAVVYairqrJZbRXlkbD-V2BUjgm8pBiHVsaZlqghQk4DB-zv-ggRbvAZaPw9RXjcn4oKF4NVl4ZNT_jg6OKJCQVheVd1Fw

Filer: hablich

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### ha...@google.com (2016-03-16)

[Empty comment from Monorail migration]

### da...@chromium.org (2016-03-16)

I'll take a look, hopefully later today.

### cl...@chromium.org (2016-03-16)

[Empty comment from Monorail migration]

### da...@chromium.org (2016-03-17)

The problem is that a lazy deopt gets triggered from a TurboFan-generated function that calls Runtime_NewSloppyArguments, whose entry in the functions' Deoptimization Input Data looks like this:

Deoptimization Input Data (deopt points = 45)
 index  ast id    argc     pc
     0      -1       0    294   <= PC directly after NewSloppyArgument call
     1      22       0     -1
...

The heap overflows, and a GC gets triggered, and the GC looks to see if there are compiled function that have weak references in them that are now dead, specially handing the top frame in ProcessTopOptimizedFrame to treat the references weakly if the optimized function can't lazy deopt at it's currently active PC, and if not, it treats the references in the function as strong references. It uses a function called CanDeoptAt to determine this, but that function checks returns true if the entry for the PC in the Deoptimization Input Data has a matching PC. In this case, however, the ast_id for that PC entry is -1.

Indeed, in ast-graph-builder, BuildArgumentsObject calls PrepareFrameState(object, BailoutId::None());, without a bailout id, and that seems to be the source of the offending Deoptimization Input Data entry.

The comment in BuildArgumentsObject seems misinformed:

// Assign the object to the {arguments} variable. This should never lazy  
// deopt, so it is fine to send invalid bailout id. 

Although it applies to the lines after, it seems that there is an assumption that CreateArguments can't lazy deopt, and that isn't true. 

Note that this bug also seems to be in BuildRestArgumentsArray.

I am gre-assign to Jaro, since he seems to be the expert in all-things-missing-frame-state.

### cl...@chromium.org (2016-03-17)

ClusterFuzz has detected this issue as fixed in range 34852:34853.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4993595320303616

Fuzzer: decoder_langfuzz
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x000097dd3bd4
Crash State:
  v8::internal::StackFrameIterator::StackFrameIterator
  v8::internal::Isolate::PrintStack
  v8::internal::Isolate::StackTraceString
  
Regressed: V8: r34570:34571
Fixed: V8: r34852:34853

Minimized Testcase (9.61 Kb): https://cluster-fuzz.appspot.com/download/AMIfv953Nhg-5a0o5TdwTd-mKkdqM_F47EhyPsL0SDxGFxizs4c8nnmwyPCllLbQJb4LYAVVYairqrJZbRXlkbD-V2BUjgm8pBiHVsaZlqghQk4DB-zv-ggRbvAZaPw9RXjcn4oKF4NVl4ZNT_jg6OKJCQVheVd1Fw

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### ms...@chromium.org (2016-03-17)

Re #4: The comment is BuildArgumentsObject you mentioned is not referring to the creation of the arguments array, it is referring to the assignment operation (built by BuildVariableAssignment). IIRC in your repro the creation caused a deopt, not the assignment. We do not allocate when assigning to VAR-mode variables that are stack-allocated or context-allocated. This can be verified by checking that the BailoutId that is passed in is not used in those cases. So I think the comment is correct an holds IMHO. It just doesn't apply to the lines above that emit a CreateArguments node, as you pointed out.

### wf...@chromium.org (2016-03-25)

if this is fixed can it be marked fixed? is there a merge needed?

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2016-03-27)

[Empty comment from Monorail migration]

### wf...@chromium.org (2016-03-27)

Please update this bug with the CL that this is fixed in, if it's fixed, also marking it fixed.

### cl...@chromium.org (2016-04-01)

jarin@: Uh oh! This issue is still open and hasn't been updated in the last 14 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ja...@chromium.org (2016-04-04)

Fixed by:

commit 946354a7af0b328673ff3b7d7c08ab27c264a2b1
Author: danno <danno@chromium.org>
Date:   Thu Mar 17 11:04:32 2016 -0700

    Ensure no lazy deopts into TurboFan code with deopt entries with no AstID
    
    BUG=595259
    LOG=N
    
    Review URL: https://codereview.chromium.org/1809073002
    
    Cr-Commit-Position: refs/heads/master@{#34868}

### cl...@chromium.org (2016-04-04)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ha...@chromium.org (2016-04-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-04-29)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-05-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@chromium.org (2016-05-18)

I don't think we need to merge this to 50 anymore because it will be succeeded by 51 soon.

### ti...@google.com (2016-05-24)

Updating labels for M51 - also missing milestone.

### ti...@google.com (2016-05-25)

Congrats - $3500 for this report ($3000 for the bug +$500 for the fuzzer).

I'll add this into the next payment run. CVE-ID is CVE-2016-1678.

### aw...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-11)

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

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/595259?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/594912, crbug.com/chromium/595296]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083871)*
