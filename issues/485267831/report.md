# Debug check failed: visited_->find(lit) != visited_->end()

| Field | Value |
|-------|-------|
| **Issue ID** | [485267831](https://issues.chromium.org/issues/485267831) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Parser |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | v8 14.7.0 |
| **Reporter** | qy...@gmail.com |
| **Assignee** | is...@chromium.org |
| **Created** | 2026-02-18 |
| **Bounty** | $7,000.00 |

## Description

# Steps to reproduce the problem

run with:
d8 poc.js

# Problem Description

Parser::ReindexComputedMemberName (src/parsing/parser.cc:2750) calls AstFunctionLiteralIdReindexer::Reindex (src/ast/ast-function-literal-id-reindexer.cc:18) to shift IDs in computed
class member names.
Unlike the arrow-parameter path (src/parsing/parser.cc:2734), this path does not check reindexer.HasStackOverflow() and does not propagate parser stack overflow.

The traversal uses AstTraversalVisitor, where Visit() exits early on stack limit (src/ast/ast.h:2988).
So with deep AST + lazy compile from deep runtime call stack, reindexing may stop mid-tree after mutating only part of nodes.

That creates inconsistent metadata:

- Some FunctionLiteral::function\_literal\_id values are shifted, others are not.
- Some Call::eval\_scope\_info\_index values are shifted, others are not.
- IDs collide in Script::infos() and can mix object kinds (SharedFunctionInfo vs ScopeInfo) at the same index.

This invariant break is directly observable in release runs:

- Script::FindSharedFunctionInfo consistency check fails (src/objects/script.cc:37), because wrong SFI is fetched for a literal ID (StartPosition mismatch).
- BytecodeGenerator::AllocateDeferredConstants fails (src/interpreter/bytecode-generator.cc:1625), because an eval scope-info slot resolves to an SFI instead of ScopeInfo.

In debug, the same root cause appears earlier as:
src/ast/ast-function-literal-id-reindexer.cc:108 (visited\_->find(lit) != visited\_->end()), showing traversal incompleteness.

# Summary

Debug check failed: visited\_->find(lit) != visited\_->end()

# Custom Questions

#### Type of crash:

tab

#### Crash state:

```
#
# Fatal error in ../../src/ast/ast-function-literal-id-reindexer.cc, line 108
# Debug check failed: visited_->find(lit) != visited_->end().
#
#
#
#FailureMessage Object: 0x7ffcdd1f6f68
==== C stack trace ===============================

    /home/qy/new5/v8/out/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x29) [0x75a80d0e60e9]
    /home/qy/new5/v8/out/x64.debug/libv8_libplatform.so(+0x4e29d) [0x75a80d04729d]
    /home/qy/new5/v8/out/x64.debug/libv8_libbase.so(V8_Fatal(char const*, int, char const*, ...)+0x205) [0x75a80d0ba2f5]
    /home/qy/new5/v8/out/x64.debug/libv8_libbase.so(+0x53b8c) [0x75a80d0b9b8c]
    /home/qy/new5/v8/out/x64.debug/libv8_libbase.so(V8_Dcheck(char const*, int, char const*)+0x4d) [0x75a80d0ba3ed]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c3652) [0x75a8072c3652]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c013d) [0x75a8072c013d]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c25aa) [0x75a8072c25aa]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98c001f) [0x75a8072c001f]
    /home/qy/new5/v8/out/x64.debug/libv8.so(+0x98bfbe2) [0x75a8072bfbe2]
Trace/breakpoint trap (core dumped)


```
#### Reporter credit:

qymag1c

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 369 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6262834941853696.

### ch...@google.com (2026-02-18)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### 24...@project.gserviceaccount.com (2026-02-19)

Detailed Report: https://clusterfuzz.com/testcase?key=6262834941853696

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  visited_->find(lit) != visited_->end() in ast-function-literal-id-reindexer.cc
  v8::internal::AstTraversalVisitor<v8::internal::AstFunctionLiteralIdReindexCheck
  v8::internal::AstTraversalVisitor<v8::internal::AstFunctionLiteralIdReindexCheck
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=96058:96059

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6262834941853696

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ch...@google.com (2026-02-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2026-02-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### is...@chromium.org (2026-02-19)

Thank you for the report!

### dx...@google.com (2026-02-20)

Project: v8/v8  

Branch:  main  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7594973>

[parser] Make sure AST visitors handle stack overflow

---


Expand for full commit details
```
     
    ... by enforcing them to explicitly clear the stack overflow state. 
     
    Fixed: 485267831 
    Change-Id: I8bee4e55ceb3fac6536d88edf28b6196a204d5cc 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7594973 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105349}

```

---

Files:

- M `src/ast/ast-function-literal-id-reindexer.cc`
- M `src/ast/ast-traversal-visitor.h`
- M `src/debug/liveedit.cc`
- M `src/parsing/parser.cc`

---

Hash: [b07860d0159521ebeaa4361700fe1cdae4818149](https://chromiumdash.appspot.com/commit/b07860d0159521ebeaa4361700fe1cdae4818149)  

Date: Thu Feb 19 16:40:20 2026


---

### ch...@google.com (2026-02-20)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dx...@google.com (2026-02-20)

[Details redacted due to bug visibility]

Change-Id: I42b0730f20bb1f71f71aacb468c43758ea7edd0c  

<https://chrome-internal-review.git.corp.google.com/9036436>

### ch...@google.com (2026-02-20)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### 24...@project.gserviceaccount.com (2026-02-20)

ClusterFuzz testcase 6262834941853696 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=105348:105349

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-02-21)

Merge review required: M146 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-21)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-21)

Merge review required: M144 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### is...@chromium.org (2026-02-23)

1. This is a security issue that might theoretically be exploited.
2. <https://chromium-review.googlesource.com/7594973>
3. Not yet, see the progress here: <https://chromiumdash.appspot.com/commit/b07860d0159521ebeaa4361700fe1cdae4818149>
4. This is a more than a year old issue.
5. n/a
6. No, passing a regular V8 test suite is enough.

### dr...@chromium.org (2026-02-25)

No crashes in Canary. Approving merge to all three milestones.

### dx...@google.com (2026-02-26)

Project: v8/v8  

Branch:  refs/branch-heads/14.5  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7613208>

Merged: [parser] Make sure AST visitors handle stack overflow

---


Expand for full commit details
```
     
    ... by enforcing them to explicitly clear the stack overflow state. 
     
    Fixed: 485267831 
    (cherry picked from commit b07860d0159521ebeaa4361700fe1cdae4818149) 
     
    Change-Id: I21df97d19aa7f45fe30fbc3976e559f937f76605 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7613208 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.5@{#28} 
    Cr-Branched-From: f09d67c66114951c0ea3dc9d4b025461670a9557-refs/heads/14.5.201@{#2} 
    Cr-Branched-From: 3f006438f768659ed9776359a421dc432edce53f-refs/heads/main@{#104623}

```

---

Files:

- M `src/ast/ast-function-literal-id-reindexer.cc`
- M `src/ast/ast-traversal-visitor.h`
- M `src/debug/liveedit.cc`
- M `src/parsing/parser.cc`

---

Hash: [7c6fbddaea8b34279bc297bb03db2c1fd22a3fce](https://chromiumdash.appspot.com/commit/7c6fbddaea8b34279bc297bb03db2c1fd22a3fce)  

Date: Thu Feb 19 16:40:20 2026


---

### dx...@google.com (2026-02-26)

Project: v8/v8  

Branch:  refs/branch-heads/14.4  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7613207>

Merged: [parser] Make sure AST visitors handle stack overflow

---


Expand for full commit details
```
     
    ... by enforcing them to explicitly clear the stack overflow state. 
     
    Fixed: 485267831 
    (cherry picked from commit b07860d0159521ebeaa4361700fe1cdae4818149) 
     
    Change-Id: I1275011898d51001c4e7ab6d5dc01dd67c4e345f 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7613207 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.4@{#60} 
    Cr-Branched-From: 80acc26727d5a34e77dabeebe7c9213ec1bd4768-refs/heads/14.4.258@{#1} 
    Cr-Branched-From: ce7e597e90f6df3fa4b6df224bc613b80c635450-refs/heads/main@{#104020}

```

---

Files:

- M `src/ast/ast-function-literal-id-reindexer.cc`
- M `src/ast/ast-traversal-visitor.h`
- M `src/debug/liveedit.cc`
- M `src/parsing/parser.cc`

---

Hash: [36494ca53126f5e835f020d68ed8a5823f0748b0](https://chromiumdash.appspot.com/commit/36494ca53126f5e835f020d68ed8a5823f0748b0)  

Date: Thu Feb 19 16:40:20 2026


---

### dx...@google.com (2026-02-26)

Project: v8/v8  

Branch:  refs/branch-heads/14.6  

Author:  Igor Sheludko [ishell@chromium.org](mailto:ishell@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7613209>

Merged: [parser] Make sure AST visitors handle stack overflow

---


Expand for full commit details
```
     
    ... by enforcing them to explicitly clear the stack overflow state. 
     
    Fixed: 485267831 
    (cherry picked from commit b07860d0159521ebeaa4361700fe1cdae4818149) 
     
    Change-Id: I89bcf61287917cb13216e1fe8fcaf4bbd95c9b35 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7613209 
    Auto-Submit: Igor Sheludko <ishell@chromium.org> 
    Commit-Queue: Igor Sheludko <ishell@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/14.6@{#15} 
    Cr-Branched-From: e04c3a1a2543bdbee7beac8846c9cbe8f657636f-refs/heads/14.6.202@{#1} 
    Cr-Branched-From: 3b0b01e6594ec362369dc16f069012a81748c8ba-refs/heads/main@{#105132}

```

---

Files:

- M `src/ast/ast-function-literal-id-reindexer.cc`
- M `src/ast/ast-traversal-visitor.h`
- M `src/debug/liveedit.cc`
- M `src/parsing/parser.cc`

---

Hash: [5251912fda3917d373b24190c36739b5af26c01d](https://chromiumdash.appspot.com/commit/5251912fda3917d373b24190c36739b5af26c01d)  

Date: Thu Feb 19 16:40:20 2026


---

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Baseline. Renderer RCE / memory corruption in a sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ve...@chromium.org (2026-03-13)

Fwiw I don't think this is a security bug because of 1) strict SFI verification on infos() access; and 2) strict scope info verification. Do you have a way to get around that?

### ve...@chromium.org (2026-03-13)

Those 2 checks you're hitting in release more are exactly the safety net that makes this not be a security bug. Is there a way around it? If not, I'd downgrade this to a bug.

### dx...@google.com (2026-05-29)

Project: v8/v8  

Branch:  main  

Author:  Michael Lippautz [mlippautz@chromium.org](mailto:mlippautz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7883043>

[test] Last batch of regression tests

---


Expand for full commit details
```
     
    TAG=AGY 
     
    Bug: 517688821 
     
    Bug: 40061466 
    Bug: 40066473 
    Bug: 342456991 
    Bug: 343507800 
    Bug: 366381662 
    Bug: 368311899 
    Bug: 372269618 
    Bug: 383647255 
    Bug: 392521083 
    Bug: 398999390 
    Bug: 40059920 
    Bug: 40060821 
    Bug: 40064370 
    Bug: 40065138 
    Bug: 40282100 
    Bug: 40892749 
    Bug: 41484971 
    Bug: 420636529 
    Bug: 42203224 
    Bug: 423459708 
    Bug: 450328966 
    Bug: 452296415 
    Bug: 469143679 
    Bug: 476233066 
    Bug: 478659010 
    Bug: 485267831 
    Bug: 508811477 
    Change-Id: I692cb14ebeac04eaa77c867e9377ebd19b4b909b 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7883043 
    Auto-Submit: Michael Lippautz <mlippautz@chromium.org> 
    Commit-Queue: Michael Lippautz <mlippautz@chromium.org> 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Leszek Swirski <leszeks@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#107659}

```

---

Files:

- A `test/mjsunit/compiler/regress-40061466.js`
- A `test/mjsunit/maglev/regress-40066473.js`
- A `test/mjsunit/regress/regress-342456991.js`
- A `test/mjsunit/regress/regress-343507800.js`
- A `test/mjsunit/regress/regress-366381662.js`
- A `test/mjsunit/regress/regress-368311899.js`
- A `test/mjsunit/regress/regress-372269618.js`
- A `test/mjsunit/regress/regress-383647255.js`
- A `test/mjsunit/regress/regress-392521083.js`
- A `test/mjsunit/regress/regress-398999390.js`
- A `test/mjsunit/regress/regress-40059920.js`
- A `test/mjsunit/regress/regress-40060821.js`
- A `test/mjsunit/regress/regress-40064370.js`
- A `test/mjsunit/regress/regress-40065138.js`
- A `test/mjsunit/regress/regress-40282100.js`
- A `test/mjsunit/regress/regress-40892749.js`
- A `test/mjsunit/regress/regress-41484971.js`
- A `test/mjsunit/regress/regress-420636529.js`
- A `test/mjsunit/regress/regress-42203224.js`
- A `test/mjsunit/regress/regress-423459708.js`
- A `test/mjsunit/regress/regress-450328966.js`
- A `test/mjsunit/regress/regress-452296415.js`
- A `test/mjsunit/regress/regress-469143679.js`
- A `test/mjsunit/regress/regress-476233066-1.js`
- A `test/mjsunit/regress/regress-476233066-2.js`
- A `test/mjsunit/regress/regress-478659010.js`
- A `test/mjsunit/regress/regress-485267831.js`
- A `test/mjsunit/regress/regress-508811477.js`

---

Hash: [a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc](https://chromiumdash.appspot.com/commit/a5d1a1cc6911f1d1c7f30da136c8f252b05a58dc)  

Date: Fri May 29 12:59:59 2026


---

### ch...@google.com (2026-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485267831)*
