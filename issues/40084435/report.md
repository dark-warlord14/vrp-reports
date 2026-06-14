# Security: Arbitrary Memory Read in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40084435](https://issues.chromium.org/issues/40084435) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Reporter** | cw...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2016-06-01 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Attacker can control a register value when it crashes.  

It seems that a pointer is overwritten by an other  

pointer that has a different object type.

**VERSION**  

51.0.2704.63 (stable 32bit)  

Windows 10  

V8 5.1.281.47

## **REPRODUCTION CASE** --------------------------- js code ----------------- this.**defineSetter**("x", function(){}); function go (y = (function rec(a1, a2) { // The position of "AAAA" controls a register value. if (a1.length == a2) { b = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCAAAA"; } rec(a1, a2 + 1); })([,], 0) , b = eval("") ) {} go(x);

Attacker can control the ebx register in the following asm code:  

mov ecx,dword ptr [ebx+edx\*2+7].

(5c78.4e64): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

1370e3a0 8b4c5307 mov ecx,dword ptr [ebx+edx\*2+7] ds:002b:41414154=????????  

0:000:x86> dd ebx  

41414141 ???????? ???????? ???????? ????????

## Timeline

### in...@chromium.org (2016-06-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5886513716133888

### fe...@chromium.org (2016-06-02)

[Empty comment from Monorail migration]

[Monorail components: Infra>Client>V8]

### fe...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

[Monorail components: -Infra>Client>V8 Blink>JavaScript]

### fe...@chromium.org (2016-06-03)

jochen@, could you PTAL or help assign the bug? Thank you.

### jo...@chromium.org (2016-06-03)

[Empty comment from Monorail migration]

### jo...@chromium.org (2016-06-06)

[Empty comment from Monorail migration]

### li...@chromium.org (2016-06-06)

I have a fix at https://codereview.chromium.org/2042793002 . I verified that with this patch, asan does not fail as it does previously. I made a deliberately vague commit message and did not publish a test because of the severity of the security issue and the fact that this bug has been around for a long time.

This bug looks pretty bad, and I believe it's been around as long as destructuring parameters have been. The core of it is that different code ends up compiling accesses to the same variable (b) in different ways. There are subtle nested scopes created by default parameters. If the initialization of "b" calls eval, that informs how b is allocated. The implementation propagated that information forward, but not backward, so later parameters would know how b is allocated and earlier ones would not. This patch propagates the flags in a separate patch afterwards (also needed for whether super is called, which was previously not handed at all).

We might be able to add some more DCHECKs to scope analysis to catch invalid scope scenarios like this (the outer parameter scope eventually calls eval, and the inner one doesn't realize that it can see the effects of that). I'm not sure exactly where these would go though.

### bu...@chromium.org (2016-06-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/4cc1331c341f5bfbeee54fec521f682a8a406af4

commit 4cc1331c341f5bfbeee54fec521f682a8a406af4
Author: littledan <littledan@chromium.org>
Date: Mon Jun 06 14:30:12 2016

Fix scope flags for default parameters

R=rossberg,adamk
BUG=chromium:616386

Review-Url: https://codereview.chromium.org/2042793002
Cr-Commit-Position: refs/heads/master@{#36755}

[modify] https://crrev.com/4cc1331c341f5bfbeee54fec521f682a8a406af4/src/parsing/parser.cc


### li...@chromium.org (2016-06-06)

Based on Andreas's and Jochen's feedback, I decided to land the patch. The patch landing should fix this security issue. However, I still have some concerns about this code path. I'm still confused by failures like https://build.chromium.org/p/tryserver.v8/builders/v8_linux64_asan_rel_ng_triggered/builds/2517/steps/Ignition%20-%20turbofan/logs/default-parameters-de.. from patch version 1 of https://codereview.chromium.org/2042793002 where the scopes were only declared eval at the end (as opposed to redundantly in the current code, both before parsing the scope and after all scopes are parsed). I don't see any places in the code where the eval-ness is read before we're all done with parsing and doing Scope::Analyze, so I'm not sure what leads to the failure of that version. The new version only adds an additional point to notice that a scope should have its calls_eval bit set, so it should conservatively be only "more correct" than the previous code.

### ad...@chromium.org (2016-06-06)

I'll dig into littledan's concerns from https://crbug.com/chromium/616386#c10 today.

### ad...@chromium.org (2016-06-06)

The aforementioned failures are due to the call to Scope::FinalizeBlockScope in BuildParameterInitializationBlock. FinalizeBlockScope reads the calls_sloppy_eval() bit, and so if it's not set at that point the scope is erroneously removed from the scope chain.

The landed patch looks correct, but I assume the looping at the end of BuildParameterInitializationBlock is now unnecessary?

### li...@chromium.org (2016-06-07)

Actually, I think this patch doesn't solve the underlying problem and should be reverted. Not sure what I was doing wrong yesterday, but when I run the original test case with ASAN on, I still get the same failure that ClusterFuzz got before (it seemed yesterday that it was fixed). I was concerned about the possibility that the process in DeclareAndInitializeVariables would expand out into code that would set the calls_eval bit (which is why there's the extra looping at the end), but that appears to not be the source of the bug.

So far, what I can tell from the ASAN failure is that the attempted stack trace printout from an error being thrown. In GDB, the stack trace is as follows:

(gdb) bt
#0  0x0000000000f51578 in v8::internal::JavaScriptFrame::GetParameter (this=0x7ffe1b5b28c0, index=-1) at ../../src/frames-inl.h:170
#1  0x00000000011d64ca in v8::internal::JavaScriptFrame::receiver (this=0x7ffe1b5b28c0) at ../../src/frames.cc:868
#2  0x00000000011d6115 in v8::internal::JavaScriptFrame::Summarize (this=0x7ffe1b5b28c0, functions=0x7ffe1b5b2bc0, 
    mode=v8::internal::FrameSummary::kExactSummary) at ../../src/frames.cc:859
#3  0x00000000014c67f8 in v8::internal::Isolate::CaptureSimpleStackTrace (this=0x62b000000200, error_object=..., caller=...) at ../../src/isolate.cc:394
#4  0x00000000014c8cd8 in v8::internal::Isolate::CaptureAndSetSimpleStackTrace (this=0x62b000000200, error_object=..., caller=...) at ../../src/isolate.cc:474
#5  0x000000000285a25a in v8::internal::__RT_impl_Runtime_CollectStackTrace (args=..., isolate=0x62b000000200) at ../../src/runtime/runtime-internal.cc:362
#6  0x00000000028596bb in v8::internal::Runtime_CollectStackTrace (args_length=2, args_object=0x7ffe1b5b3940, isolate=0x62b000000200)
    at ../../src/runtime/runtime-internal.cc:351

This shows that the receiver parameter is invalid.

The original test case (which crashes ASAN deterministically) probably runs into an out-of-stack condition, but I see a similar error if I limit the iterations to a small number.

It's hard to come to a minimal test case by editing the provided reproduction. Many edits continue to crash ASAN individually, but if you put them together, they no longer crash it. So I'm just running against this input test case for now.

I'm new to debugging frames so I'm just trying to get caught up on the basics of how frames and stack traces work in order to be able to examine the v8 stack and heap in gdb to figure out what's going wrong exactly.

### cl...@chromium.org (2016-06-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5886513716133888

Uploader: felt@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7ffd383e1808
Crash State:
  v8::internal::JavaScriptFrame::receiver
  v8::internal::JavaScriptFrame::Summarize
  v8::internal::Isolate::CaptureSimpleStackTrace
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=359738:359776

Minimized Testcase (0.15 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96cTJ6dhaVB8t1bPriJDuRSycrFO_heX4XwmMwWd8dwB3ZHemr6Nc_iG_iiuokWaK8XqFq2j8I4GpR-DlnfipbHE3iv5apJPiH0McfITlkqAlsPfoj5vzpmx7iQCuuGNCitW_IkXRmGYDgfWGo4W_XtbEuSug
<script>
function go (y = (function rec() {
 b = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCAAAA"; 
 a2 + 1;
})()
        , b = eval()
        )
{}
go();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### li...@chromium.org (2016-06-09)

Jakob walked me through some debugging of this issue with gdb. It seems that the write to b corrupts the sharedfunctioninfo of rec by overwriting it. B is understood at its write location to be context allocated, but the context does not seem to be big enough and it is written past the end.

If I force a context allocation for the whole function (e.g., put arguments in the function body, or call out to ForceContextAllocation somewhere), the segfault goes away. I think the problem might be related to the complex inner scopes that non-simple arguments have--we probably want the eval to force a context allocation, but maybe it somehow does not bubble up to that.

### ad...@chromium.org (2016-06-14)

What's the status of this bug? It sounds like we should revert the not-fix, but has there been any progress on further investigations here?

### li...@chromium.org (2016-06-14)

I reverted the no-fix (thanks for the lgtm) and have been investigating. Yesterday, I found that it seems to be related to the length of the context chain length (how many contexts to traverse up through) for one of the accesses to b. This led to b being read and written to from the  wrong context, which showed up in Jakob's gdb session. Manually changing the context length in fullcodegen in a hacky way for that case seems to fix the crash (though I still want to do more to verify that it's really fixed). The next step on my end is to figure out what's going wrong in the context chain length calculation.

### bu...@chromium.org (2016-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/78bb3c6ef99fb9149923056b1b25d2a8859e10b7

commit 78bb3c6ef99fb9149923056b1b25d2a8859e10b7
Author: littledan <littledan@chromium.org>
Date: Tue Jun 14 16:46:32 2016

Revert of Fix scope flags for default parameters (patchset #2 id:20001 of https://codereview.chromium.org/2042793002/ )

Reason for revert:
Does not fix the bug it intended to fix.

Original issue's description:
> Fix scope flags for default parameters
>
> R=rossberg,adamk
> BUG=chromium:616386
>
> Committed: https://crrev.com/4cc1331c341f5bfbeee54fec521f682a8a406af4
> Cr-Commit-Position: refs/heads/master@{#36755}

TBR=adamk@chromium.org,rossberg@chromium.org,jochen@chromium.org
# Not skipping CQ checks because original CL landed more than 1 days ago.
BUG=chromium:616386

Review-Url: https://codereview.chromium.org/2062593002
Cr-Commit-Position: refs/heads/master@{#36976}

[modify] https://crrev.com/78bb3c6ef99fb9149923056b1b25d2a8859e10b7/src/parsing/parser.cc


### li...@chromium.org (2016-06-14)

I wonder if the context register is somehow getting confused, and pointing to the context for b's initialization block when executing the code for y's initialization block.

### li...@chromium.org (2016-06-15)

Looking back a few versions, it seems like we've had a segfault for this test case as long as default parameters have shipped.

### li...@chromium.org (2016-06-16)

New theory: It looks like there's a mismatch between what fullcodegen thinks is the scope chain in two different places:
- Looking at the disassembly, it seems like a block scope is created for the function in "y = ...". This is caused by the eval within the function forcing context allocation for the inner scope in the RecordEvalCall() call from BuildParameterInitializationBlock
- Based on printfs added to Scope::ContextChainLength, it seems that the scope chain at compile time does not include this block scope. The param_scope needs to be inserted as its parent scope, but it doesn't seem to be there when trying to read "b" and looking into how many runtime contexts to traverse up to get there. The traversal just includes rec's scope and the go's scope, as far as I can tell.

Presumably, Parser::PatternRewriter::DeclareAndInitializeVariables is responsible for redoing the scope chain of rec and adding in param_scope (right?). I'm trying to understand how that works and why it might not be happening.

### li...@chromium.org (2016-06-17)

Seems like there's no attempt to rewrite the scope of function parameter defaults, even when a new scope is introduced! I tried adding an extra call to "RewriteParameterInitializerScope(stack_limit(), initial_value, scope_, param_scope);" inside of BuildParameterInitializationBlock when building a new param_scope (before the actual DeclareAndInitializeVariables call) and that seemed to avoid the crash in release mode; however, it breaks several DCHECKs in scopes.cc, so more work is needed to get that in a usable state (or to use --print-scopes).

Note to the previous comment: You don't need to add printfs to observe the scope mismatch, just looking at --print-scopes vs %DisassembleFunction with --code-comments is enough to see the clear mismatch.

### li...@chromium.org (2016-06-21)

I uploaded a patch which Adam and I came up with here: https://codereview.chromium.org/2077283004 . It attempts to rewrite the scopes appropriately. However, the tests included run into the same DCHECK failure as https://bugs.chromium.org/p/chromium/issues/detail?id=620119 in one of the modes. More tests are needed as well.

### bu...@chromium.org (2016-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/0e14baf712955a1993f742647bb2adc293702b80

commit 0e14baf712955a1993f742647bb2adc293702b80
Author: littledan <littledan@chromium.org>
Date: Wed Jun 22 18:20:00 2016

Rewrite scopes of non-simple default arguments

Default parameters have additional declaration block scopes inserted
around them when something in the function scope calls eval. This
patch sets the parent scope of the expressions introduced due to
those defaults to the new block scope.

R=adamk
BUG=chromium:616386

Review-Url: https://codereview.chromium.org/2077283004
Cr-Commit-Position: refs/heads/master@{#37198}

[modify] https://crrev.com/0e14baf712955a1993f742647bb2adc293702b80/src/parsing/parameter-initializer-rewriter.cc
[modify] https://crrev.com/0e14baf712955a1993f742647bb2adc293702b80/src/parsing/parser.cc
[modify] https://crrev.com/0e14baf712955a1993f742647bb2adc293702b80/src/parsing/pattern-rewriter.cc
[add] https://crrev.com/0e14baf712955a1993f742647bb2adc293702b80/test/mjsunit/regress/regress-616386.js


### li...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-22)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### go...@chromium.org (2016-06-22)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

Also is this applicable to all OS or any specific OS?

### li...@chromium.org (2016-06-22)

Govind, You are right, we should wait a couple days for Canary to show the stability of this patch. That has not happened yet. However, once we do get that data, it is important for the patch to be merged promptly.

This patch is applicable to all OSes.

### go...@chromium.org (2016-06-22)

Ok, please update the bug once it is well baked in canary. I will approve M52 merge then. Thank you.

### li...@chromium.org (2016-06-22)

Would an M51 merge be appropriate at that time as well?

### go...@chromium.org (2016-06-22)

+ awhalley@ (Security TPM on M51 merge)

### bu...@chromium.org (2016-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/dd50262933d2ac087da32be887a7c18385fd998e

commit dd50262933d2ac087da32be887a7c18385fd998e
Author: littledan <littledan@chromium.org>
Date: Wed Jun 22 19:57:36 2016

Revert of Rewrite scopes of non-simple default arguments (patchset #5 id:80001 of https://codereview.chromium.org/2077283004/ )

Reason for revert:
Seems to close tree (but it could be an infra issue)

Original issue's description:
> Rewrite scopes of non-simple default arguments
>
> Default parameters have additional declaration block scopes inserted
> around them when something in the function scope calls eval. This
> patch sets the parent scope of the expressions introduced due to
> those defaults to the new block scope.
>
> R=adamk
> BUG=chromium:616386
>
> Committed: https://crrev.com/0e14baf712955a1993f742647bb2adc293702b80
> Cr-Commit-Position: refs/heads/master@{#37198}

TBR=adamk@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=chromium:616386

Review-Url: https://codereview.chromium.org/2081323006
Cr-Commit-Position: refs/heads/master@{#37201}

[modify] https://crrev.com/dd50262933d2ac087da32be887a7c18385fd998e/src/parsing/parameter-initializer-rewriter.cc
[modify] https://crrev.com/dd50262933d2ac087da32be887a7c18385fd998e/src/parsing/parser.cc
[modify] https://crrev.com/dd50262933d2ac087da32be887a7c18385fd998e/src/parsing/pattern-rewriter.cc
[delete] https://crrev.com/8d830a5aab1c688dc0c3a1690e2ceab145b23bc3/test/mjsunit/regress/regress-616386.js


### ti...@google.com (2016-06-22)

[Automated comment] Reverts referenced in bugdroid comments, after merge request, needs manual review.

### ti...@google.com (2016-06-22)

[Automated comment] Reverts referenced in bugdroid comments, after merge request, needs manual review.

### ti...@google.com (2016-06-22)

[Automated comment] Reverts referenced in bugdroid comments, after merge request, needs manual review.

### bu...@chromium.org (2016-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/2601900dda887f5dc5c1849be68934de9295b908

commit 2601900dda887f5dc5c1849be68934de9295b908
Author: littledan <littledan@chromium.org>
Date: Wed Jun 22 21:07:53 2016

Reland of write scopes of non-simple default arguments (patchset #1 id:1 of https://codereview.chromium.org/2081323006/ )

Reason for revert:
Infra issue appears to be over

TBR=adamk@chromium.org

Original issue's description:
> Revert of Rewrite scopes of non-simple default arguments (patchset #5 id:80001 of https://codereview.chromium.org/2077283004/ )
>
> Reason for revert:
> Seems to close tree (but it could be an infra issue)
>
> Original issue's description:
> > Rewrite scopes of non-simple default arguments
> >
> > Default parameters have additional declaration block scopes inserted
> > around them when something in the function scope calls eval. This
> > patch sets the parent scope of the expressions introduced due to
> > those defaults to the new block scope.
> >
> > R=adamk
> > BUG=chromium:616386
> >
> > Committed: https://crrev.com/0e14baf712955a1993f742647bb2adc293702b80
> > Cr-Commit-Position: refs/heads/master@{#37198}
>
> TBR=adamk@chromium.org
> # Skipping CQ checks because original CL landed less than 1 days ago.
> NOPRESUBMIT=true
> NOTREECHECKS=true
> NOTRY=true
> BUG=chromium:616386
>
> Committed: https://crrev.com/dd50262933d2ac087da32be887a7c18385fd998e
> Cr-Commit-Position: refs/heads/master@{#37201}

TBR=adamk@chromium.org
# Skipping CQ checks because original CL landed less than 1 days ago.
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=chromium:616386

Review-Url: https://codereview.chromium.org/2086353003
Cr-Commit-Position: refs/heads/master@{#37202}

[modify] https://crrev.com/2601900dda887f5dc5c1849be68934de9295b908/src/parsing/parameter-initializer-rewriter.cc
[modify] https://crrev.com/2601900dda887f5dc5c1849be68934de9295b908/src/parsing/parser.cc
[modify] https://crrev.com/2601900dda887f5dc5c1849be68934de9295b908/src/parsing/pattern-rewriter.cc
[add] https://crrev.com/2601900dda887f5dc5c1849be68934de9295b908/test/mjsunit/regress/regress-616386.js


### sh...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-06-23)

ClusterFuzz has detected this issue as fixed in range 401251:401526.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5886513716133888

Uploader: felt@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7ffd383e1808
Crash State:
  v8::internal::JavaScriptFrame::receiver
  v8::internal::JavaScriptFrame::Summarize
  v8::internal::Isolate::CaptureSimpleStackTrace
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=359738:359776
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=401251:401526

Minimized Testcase (0.15 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96cTJ6dhaVB8t1bPriJDuRSycrFO_heX4XwmMwWd8dwB3ZHemr6Nc_iG_iiuokWaK8XqFq2j8I4GpR-DlnfipbHE3iv5apJPiH0McfITlkqAlsPfoj5vzpmx7iQCuuGNCitW_IkXRmGYDgfWGo4W_XtbEuSug?testcase_id=5886513716133888
<script>
function go (y = (function rec() {
 b = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCAAAA"; 
 a2 + 1;
})()
        , b = eval()
        )
{}
go();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-06-23)

ClusterFuzz has detected this issue as fixed in range 401251:401526.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5886513716133888

Uploader: felt@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7ffd383e1808
Crash State:
  v8::internal::JavaScriptFrame::receiver
  v8::internal::JavaScriptFrame::Summarize
  v8::internal::Isolate::CaptureSimpleStackTrace
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=359738:359776
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=401251:401526

Minimized Testcase (0.15 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96cTJ6dhaVB8t1bPriJDuRSycrFO_heX4XwmMwWd8dwB3ZHemr6Nc_iG_iiuokWaK8XqFq2j8I4GpR-DlnfipbHE3iv5apJPiH0McfITlkqAlsPfoj5vzpmx7iQCuuGNCitW_IkXRmGYDgfWGo4W_XtbEuSug?testcase_id=5886513716133888
<script>
function go (y = (function rec() {
 b = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCAAAA"; 
 a2 + 1;
})()
        , b = eval()
        )
{}
go();
</script>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### go...@chromium.org (2016-06-24)

could you please clarify which change or revert you want to merge in to M52 branch as I see multiple cls are listed. 

Also before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### li...@chromium.org (2016-06-24)

The change appears to be baked in Canary now, as I don't see obviously related crashes in Chromecrash (though the crash rate is a little high right now). The patch that should be merged is https://codereview.chromium.org/2077283004 ; it was temporarily reverted for what turned out to be unrelated infrastructure failures, but I don't know of any problems with the patch.

### go...@chromium.org (2016-06-24)

Approving merge to M52 branch 2743 for https://codereview.chromium.org/2077283004 as per https://crbug.com/chromium/616386#c41. Please merge asap. Thank you.

### bu...@chromium.org (2016-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/559143978207787f4976404d66c30e8a70fb9580

commit 559143978207787f4976404d66c30e8a70fb9580
Author: Adam Klein <adamk@chromium.org>
Date: Tue Jun 28 01:09:33 2016

Version 5.2.361.25 (cherry-pick)

Merged 0e14baf712955a1993f742647bb2adc293702b80

Rewrite scopes of non-simple default arguments

BUG=chromium:616386
LOG=N
R=littledan@chromium.org

Review URL: https://codereview.chromium.org/2102933002 .

Cr-Commit-Position: refs/branch-heads/5.2@{#31}
Cr-Branched-From: 2cd36d6d0439ddfbe84cd90e112dced85084ec95-refs/heads/5.2.361@{#1}
Cr-Branched-From: 3fef34e02388e07d46067c516320f1ff12304c8e-refs/heads/master@{#36332}

[modify] https://crrev.com/559143978207787f4976404d66c30e8a70fb9580/include/v8-version.h
[modify] https://crrev.com/559143978207787f4976404d66c30e8a70fb9580/src/parsing/parameter-initializer-rewriter.cc
[modify] https://crrev.com/559143978207787f4976404d66c30e8a70fb9580/src/parsing/parser.cc
[modify] https://crrev.com/559143978207787f4976404d66c30e8a70fb9580/src/parsing/pattern-rewriter.cc
[add] https://crrev.com/559143978207787f4976404d66c30e8a70fb9580/test/mjsunit/regress/regress-616386.js


### sh...@chromium.org (2016-06-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2016-06-28)

Should we backport this patch to 5.1?

### ad...@chromium.org (2016-06-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-13)

[Empty comment from Monorail migration]

### li...@chromium.org (2016-09-13)

To the reward panel: This was a very serious bug. The test case demonstrated writing into memory that may be used as part of code execution.

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

Congratulations, the panel rewarded $5,000 for this bug!

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-29)

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

### ha...@chromium.org (2017-04-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/616386?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084435)*
