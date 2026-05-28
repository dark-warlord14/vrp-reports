# Dcheck failure in fixed-array-inl.h

| Field | Value |
|-------|-------|
| **Issue ID** | [458914193](https://issues.chromium.org/issues/458914193) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | p1...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2025-11-08 |
| **Bounty** | $8,000.00 |

## Description

## Description

Compilation error occurs with nested classes having a specific structure. The error manifests as an array bounds check violation in fixed-array-inl.h.

The error happens when attempting to access a WeakFixedArray element at index 6, which is out of bounds.

## Reproduction Case

```
class C1 {}

const v1 = {
    n() {
        try { 
            this.n();
        } catch (e) {}

        class C2 {
            constructor() {
                class C3 extends C1 {
                    constructor() {}
                    a;
                    static {};
                    b;
                    static {
                        let x = 0;
                    }
                }
            }
        };

        new C2();
    }
};
let res = v1.n();

```

Tested on debug build **without ASAN** on Linux x64

**Build flags:**

```
is_debug = true
target_cpu = "x64"
v8_enable_backtrace = true
v8_static_library = true  
is_component_build = false
dcheck_always_on = true
v8_enable_disassembler = true
v8_enable_debugging_features=true
v8_dcheck_always_on = true

```
```
./out/debug/d8 poc.js


#
# Fatal error in ../../src/objects/fixed-array-inl.h, line 116
# Debug check failed: IsInBounds(index).
#
#
#
#FailureMessage Object: 0x7ffec77d5720
==== C stack trace ===============================

    ./out/debug/d8(v8::base::debug::StackTrace::StackTrace()+0x13) [0x55980cf3cbb3]
    ./out/debug/d8(+0x2909abd) [0x55980cf3babd]
    ./out/debug/d8(V8_Fatal(char const*, int, char const*, ...)+0x194) [0x55980cf33774]
    ./out/debug/d8(+0x2901025) [0x55980cf33025]
    ./out/debug/d8(void v8::internal::DeclarationScope::AllocateScopeInfos<v8::internal::Isolate>(v8::internal::ParseInfo*, v8::internal::DirectHandle<v8::internal::Script>, v8::internal::Isolate*)+0x715) [0x55980d153d05]
    ./out/debug/d8(+0x2ac01bf) [0x55980d0f21bf]
    ./out/debug/d8(v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::Handle<v8::internal::SharedFunctionInfo>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*, v8::internal::CreateSourcePositions)+0x88f) [0x55980d0f16cf]
    ./out/debug/d8(v8::internal::Compiler::Compile(v8::internal::Isolate*, v8::internal::DirectHandle<v8::internal::JSFunction>, v8::internal::Compiler::ClearExceptionFlag, v8::internal::IsCompiledScope*)+0x259) [0x55980d0f2909]
    ./out/debug/d8(+0x397500d) [0x55980dfa700d]
    ./out/debug/d8(v8::internal::Runtime_CompileLazy(int, unsigned long*, v8::internal::Isolate*)+0x84) [0x55980dfa6b14]
    ./out/debug/d8(+0x62fb67d) [0x55981092d67d]
Trace/breakpoint trap

```
## Introduced

This vulnerability was introduced in: <https://chromium.googlesource.com/v8/v8/+/a96a186d4d293bb9cc728eac23709b4e79dc358a> (M141 Stable)

## Proposed Fix

Fixing this proved to be quite challenging for me, but for a local fix I discovered that limiting the loop in DeclarationScope::AllocateScopeInfos to infos->length() prevents the crash:

```
diff --git a/src/ast/scopes.cc b/src/ast/scopes.cc
index e406e916459..b2ba7218be0 100644
--- a/src/ast/scopes.cc
+++ b/src/ast/scopes.cc
@@ -2803,7 +2803,7 @@ void DeclarationScope::AllocateScopeInfos(ParseInfo* parse_info,
     // reuse. Also look at the compiled function itself, and reuse its function
     // scope info if it exists.
     for (int i = parse_info->literal()->function_literal_id();
-         i <= parse_info->max_info_id(); ++i) {
+         i <= parse_info->max_info_id() && i < infos->length(); ++i) {
       Tagged<MaybeObject> maybe_info = infos->get(i);
       if (maybe_info.IsWeak()) {
         Tagged<Object> info = maybe_info.GetHeapObjectAssumeWeak();

```

Additionally, reverting the changes made in commit a96a186d4d293bb9cc728eac23709b4e79dc358a also prevents the crash.

## CREDIT INFORMATION

Reporter credit: @p1nky4745

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 471 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2025-11-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5683196616179712.

### jd...@chromium.org (2025-11-10)

Clusterfuzz is struggling to reproduce this. Setting tags very provisionally. Over to v8 security for full triage.

### ch...@google.com (2025-11-11)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-11-11)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-11-11)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### p1...@gmail.com (2025-11-11)

To reproduce in ClusterFuzz, use a build **without asan** and **without slow\_dchecks** (with the flags from the description it reproduces reliably).

I’m not very familiar with how this works, but it seems that at <https://clusterfuzz.com/testcase?key=5683196616179712> my `poc.js` wasn’t uploaded; instead there’s some HTML there.

And the error:

```
/mnt/scratch0/clusterfuzz/bot/inputs/fuzzer-testcases/test.js:2: SyntaxError: Unexpected token 'with'
     Use with Chrome flags:
         ^^^^
SyntaxError: Unexpected token 'with'

```

### cl...@appspot.gserviceaccount.com (2025-11-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5513288414593024.

### cl...@appspot.gserviceaccount.com (2025-11-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6633425918164992.

### cl...@appspot.gserviceaccount.com (2025-11-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4805285335990272.

### ta...@google.com (2025-11-14)

I cannot reproduce it on CF, but I can locally (in multiple configurations, including those with ASan).
Raphael, could you please take a look at it?

### p1...@gmail.com (2025-11-16)

I was trying to understand the root cause of this vulnerability.
Here's what I discovered:

In the JS code we have a recursion block:

```
    n() {
        try { 
            this.n();
        } catch (e) {}

```

To control it, I slightly modified poc.js:

```
class C1 {}
const v1 = {
    count: 0,
    n() {
        if (this.count < 9000) {
                this.count++
            try { 
                this.n();
            } catch (e) {console.log(e);}
        }
        class C2 {
            constructor() {
                class C3 extends C1 {
                    constructor() {}
                    a;
                    static {};
                    b;
                    static {
                        let x = 0;
                    }
                }
            }
        };

        new C2();
    }
};
v1.n();

```

If the recursion is not deep (<7000), we don't reach stack overflow. If the recursion is deep (>9000), we get the error "RangeError: Maximum call stack size exceeded"

At the same time, the scope structure changes:
The `function C3 ()` block is moved to a separate Global scope

```
$ ./out/debug/d8 poc.js --print_scopes
...
Global scope:
function C3 () { // (0x35dc01246c50) (350, 509)
  // strict mode scope
  // will be compiled
  // ClassStaticInitializerFunction
  // 1 stack slots

  varblock { // (0x35dc01247340) (411, 509)
    // strict mode scope
    // NormalFunction
    // local vars:
    LET x;  // (0x35dc01247550) local[0], never assigned, hole initialization elided
  }
}

```

This looks like a side effect of the exception handling mechanism, and it seems this should not be happening.

### p1...@gmail.com (2025-11-16)

And please don’t ignore my recommendation to use a build without `v8_enable_slow_dchecks` to reproduce in ClusterFuzz.

### le...@chromium.org (2025-11-24)

Toon, something is screwy in ScopeInfo allocation here.

### p1...@gmail.com (2025-11-24)

deleted

### ve...@chromium.org (2025-11-25)

Thanks for the report, will be fixed by <https://chromium-review.googlesource.com/c/v8/v8/+/7203465>

Surprising that this went uncaught for this long.

### dx...@google.com (2025-11-25)

Project: v8/v8  

Branch:  main  

Author:  Toon Verwaest [verwaest@chromium.org](mailto:verwaest@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7203465>

Fix class member initializer reparsing logic

---


Expand for full commit details
```
     
    Intertwined static / public member initializers can mix up ids, so unmix them. 
     
    Bug: 458914193 
    Change-Id: If0708b56750a92e03eaa5530cfbff295c2acf630 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7203465 
    Reviewed-by: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Toon Verwaest <verwaest@chromium.org> 
    Auto-Submit: Toon Verwaest <verwaest@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#103958}

```

---

Files:

- M `src/ast/scopes.cc`
- M `src/ast/scopes.h`
- M `src/objects/call-site-info.cc`
- M `src/objects/function-kind.h`
- M `src/objects/shared-function-info.cc`
- M `src/parsing/parser-base.h`
- M `src/parsing/parser.cc`
- M `src/tracing/code-data-source.cc`
- M `test/unittests/objects/object-unittest.cc`

---

Hash: [978f2b8a73fdc1c6d17fa5966dee81393e2f1533](https://chromiumdash.appspot.com/commit/978f2b8a73fdc1c6d17fa5966dee81393e2f1533)  

Date: Tue Nov 25 16:37:52 2025


---

### ch...@google.com (2025-12-01)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M143. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M142 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M143 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142, 143].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2025-12-03)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M143. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: M142 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M143 is already shipping to stable.

**Merge approved:** your change passed merge requirements and is auto-approved for M144. Please go ahead and merge the CL to branch 7559 (refs/branch-heads/7559) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142, 143, 144].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2025-12-08)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2025-12-08)

Please merge your change to M144 by 5:00 PM PT today so it gets picked up by this week's beta release. Thank you.

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
Renderer RCE / memory corruption in a sandboxed process with a bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ya...@chromium.org (2025-12-11)

verwaest@ Please submit a merge CL. Thanks

### ch...@google.com (2025-12-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2025-12-15)

Please merge your change to M144 by 10:00 AM  PT tomorrow, Dec 16th so we can take it in for this week's last beta release before the holiday release freeze. Thank you.

### sr...@chromium.org (2025-12-15)

We are cutting the final beta RC before holidays tomorrow around 1pm PST, please make sure all your merges are in before that time so this change goes to beta release before holidays Kick in, 

Jan first week we have stable RC cut for 144, and we dont plan on any releases during release freeze 

### go...@google.com (2025-12-22)

[Bulk Edit]

Reminder M144 is already in Beta and Stable cut is coming soon right after holidays on Jan 6th 10:00 AM PT . Please review this bug and assess if this is indeed a RBS. If not, please remove the RBS label. If so, please make sure to land the fix and request a merge into the release branch ASAP. Thank you.

### dr...@chromium.org (2025-12-29)

At this point I don't think we're going to cherry-pick this into M143, and <https://crrev.com/c/7203465> already landed in M144 so no need to merge there. We hope to make the merge CLs more automated in the future to prevent this kind of thing from falling through the cracks.

### qk...@google.com (2026-01-29)

Labeled as not applicable for M138 because the suspected CL[1] was not included in M138.

[1] <https://chromium-review.googlesource.com/c/v8/v8/+/6722290>

### ch...@google.com (2026-03-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/458914193)*
