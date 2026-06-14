# [LangFuzz] Crash with jump to invalid address

| Field | Value |
|-------|-------|
| **Issue ID** | [40079050](https://issues.chromium.org/issues/40079050) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2014-03-07 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0

Steps to reproduce the problem:
1. Load the following HTML file:

<script>
function MjsUnitAssertionError(message) {
  this.stack = new Error("").stack;
}
  function PrettyPrint(value) {  }
  function fail(expectedText, found, name_opt) {
    var message = "Fail" + "ure";
    throw new MjsUnitAssertionError(message);
  };
  assertEquals = function assertEquals(expected, found, name_opt) {
      fail(PrettyPrint(expected), found, name_opt);
  };
  assertThrows = function assertThrows(code, type_opt, cause_opt) {
    throw new MjsUnitAssertionError("Did not throw exception");
  }
var value = (function(){
})();
try {
assertEquals(1, value);
} catch(exc1) {}
function defineSetter(o) {
}
function testfn(f) { return [1].map(f)[0]; }
try {
assertEquals(null, testfn(defineSetter));
} catch(exc1) {}
var str = "[1]";
for (var i = 0; i < 100000; i++ ) {
  str = "[1," + str + "]";
}
try {
assertThrows(function() { JSON.parse(str); }, RangeError);
} catch(exc1) {}
</script>
<script>
var s = "";
for (i = 0; i < (17592185913344); i++) {
  s = s + (i + (i+1));
  s = s.substring(s, (s + 0.5) << 1);
}
assertEquals(57, s.charCodeAt(0));
</script>

What is the expected behavior?
No crash.

What went wrong?
Tab crash with jump to invalid address:

Program received signal SIGSEGV, Segmentation fault.
0x0000000500000000 in ?? ()
(gdb) x /i $pc
=> 0x500000000: Cannot access memory at address 0x500000000

In the d8 shell, I also get an invalid jump, but to 0xa:

==31343== Jump to the invalid address stated on the next line
==31343==    at 0xA: ???
==31343==    by 0x4F03EDD4: ???
==31343==    by 0x4F020D89: ???
==31343==    by 0x80E03F4: v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) (in v8-trunk/out/ia32.release/d8)

Did this work before? N/A 

Chrome version: 35.0.1870.2  Channel: dev
OS Version: Ubuntu 12.04 LTS
Flash Version: Shockwave Flash 11.2 r202

This affects both 32 and 64 bit builds.

## Timeline

### in...@chromium.org (2014-03-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-07)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=6260947760971776

### cl...@chromium.org (2014-03-07)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5663309504184320

### in...@chromium.org (2014-03-07)

Christian, do we need to run the testcase for a long time ?

### de...@googlemail.com (2014-03-07)

Nope, this reproduces pretty much immediately for me, both in d8 and in Chrome.

### in...@chromium.org (2014-03-07)

Marty, can you check if this reproduce on d8 trunk. On CF, it is not reproducing.

### mb...@chromium.org (2014-03-07)

I'm investigating this now. I've been able to reproduce it on older revisions of v8, but not in r19696. Could this have been fixed recently?

### mb...@chromium.org (2014-03-07)

Disregard the previous comment. This seems to be reproducing in chrome with v8 r19696, but I was having some trouble reproducing it with d8.

### mb...@chromium.org (2014-03-07)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-03-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-03-08)

[Empty comment from Monorail migration]

### jk...@chromium.org (2014-03-08)

Slightly modified repro that crashes with current x64 debug d8 (it's kinda brittle since it depends on GC timing), --hydrogen-filter=crash is possible but not necessary:

function CurveBall(message) {
  this.prop = new Error("").stack;
}
function throw_curveball() {
  throw new CurveBall("bar");
}
for (var i = 0; i < 3; ++i) {
  try {
    throw_curveball();
  } catch(exc1) {}
}
var str = "";
for (var i = 0; i < 20000; i++ ) {
  str = "a" + str;
}
(function crash() {
var s = "";
for (i = 0; i < (300000); i++) {
  s = s + i;
  s = s.substring(s, (s + 0) << 1);
}
throw_curveball();
})();


What happens is that MarkCompactCollector::ClearAndDeoptimizeDependentCode zaps all EMBEDDED_OBJECT references in a code object and replaces them with references to {undefined}. Theoretically that's fine, but in the case at hand the code object in question has an activation and no lazy bailout before one of those freshly zapped references is used. This is the code object when it is generated:

                  ;;; <@122,#103> sal-t
0x311aaf168549   329  e8b251faff     call 0x311aaf10d700     ;; code: BINARY_OP_IC, UNINITIALIZED
0x311aaf16854e   334  90             nop
0x311aaf16854f   335  90             nop
                  ;;; <@124,#106> push-argument
0x311aaf168550   336  ff75b8         push [rbp-0x48]
                  ;;; <@126,#107> push-argument
0x311aaf168553   339  ff75b8         push [rbp-0x48]
                  ;;; <@128,#108> push-argument
0x311aaf168556   342  50             push rax
                  ;;; <@130,#96> constant-t
0x311aaf168557   343  48bf81ebe046dd270000 REX.W movq rdi,0x27dd46e0eb81    ;; debug: position 353
                                                             ;; object: 0x27dd46e0eb81 <JS Function substring (SharedFunctionInfo 0x7d660f388a1)>
                  ;;; <@132,#109> call-js-function
0x311aaf168561   353  488b772f       REX.W movq rsi,[rdi+0x2f]    ;; debug: position 387
0x311aaf168565   357  ff5717         call [rdi+0x17]
                  ;;; <@134,#110> lazy-bailout
                  ;;; <@136,#112> load-global-cell
0x311aaf168568   360  48bbe8e5d0395a340000 REX.W movq rbx,0x345a39d0e5e8    ;; debug: position 339
                                                             ;; property cell
0x311aaf168572   370  488b1b         REX.W movq rbx,[rbx]

The sal-t at offset 329 triggers GC, which replaces the constant at 343 with {undefined}, which the call at 357 treats as a JSFunction and calls it... bad idea. The lazy bailout after that latter call comes too late. This is the code object after patching (and crashing):

0x311aaf168549   329  e812dbffff     call 0x311aaf166060
0x311aaf16854e   334  90             nop                                   ;; <-- note no lazy deopt here
0x311aaf16854f   335  90             nop
0x311aaf168550   336  ff75b8         push [rbp-0x48]
0x311aaf168553   339  ff75b8         push [rbp-0x48]
0x311aaf168556   342  50             push rax
0x311aaf168557   343  48bf2141f060d6070000 REX.W movq rdi,0x7d660f04121    ;; <-- undefined!
0x311aaf168561   353  488b772f       REX.W movq rsi,[rdi+0x2f]
0x311aaf168565   357  ff5717         call [rdi+0x17]                       ;; <-- ka-boom!
0x311aaf168568   360  49ba3260f0ae1a310000 REX.W movq r10,0x311aaef06032
0x311aaf168572   370  41ffd2         call r10

I don't know yet what the best fix is. 
Shouldn't the sal-t have a lazy bailout right after it? LChunkBuilder::MarkAsCall would have inserted one if HBitwiseBinaryOperation::RepresentationChanged hadn't decided that we can clear all side effects since the ToNumber conversion of the HShl's inputs is not observable.
Another angle: we're deoptimizing a code object that's currently being executed just because a dying map has a "dependent code" reference to it. That seems a bit overzealous.

The GC timing dependence could make bisection difficult. M34 is definitely affected (http://go/crash/3ff1f91eb440e943), I haven't looked further.

I'm not sure about the security impact. In the repro case above, the address we're jumping to can't be controlled, it'll always be {undefined}+0x17. However similar repro cases might exist where a different offset may be used, or where instead of calling we might dereference (or even write to?) an invalid value -- most likely it would just crash, but I can't rule out that there's an unlucky situation where more subtle damage can be caused.

### de...@googlemail.com (2014-03-08)

If the jump address is always {undefined}+0x17, why does it differ then between the browser (where it jumped to 0x500000000) vs. the d8 shell (where it jumped to 0xa)?

### jk...@chromium.org (2014-03-08)

That's because the value there is always a 5 encoded as a Smi: 5 << 1 in your ia32 d8, 5 << 32 in your x64 browser ;-)

### jk...@chromium.org (2014-03-08)

> similar repro cases might exist where a different offset may be used, 
> or where instead of calling we might dereference (or even write to?) 
> an invalid value

https://crbug.com/chromium/350554 is one of those.

+CC Jaro who has looked at LazyDeopt-related issues recently and may have some ideas what to do here.

### pa...@chromium.org (2014-03-10)

[Empty comment from Monorail migration]

### jk...@chromium.org (2014-03-11)

I have a fix at https://codereview.chromium.org/194703008/.

### jk...@chromium.org (2014-03-12)

Fixed in V8: https://code.google.com/p/v8/source/detail?r=19834

Will roll into Chromium later today, and backmerge after Canary coverage.

### cl...@chromium.org (2014-03-12)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### jk...@chromium.org (2014-03-19)

Merged to M33 and M34 as V8 versions 3.23.17.28 and 3.24.35.18, respectively.

### de...@googlemail.com (2014-03-21)

I'm still seeing a very similar testcase reproducing on v8-trunk but not on v8-bleeding edge. Is this supposed to be fixed on v8-trunk r19958?

Btw, these crashes sometimes show up as jumps to *random* invalid addresses, not just 0x500000000. So I'm quite sure this can be used for arbitrary code execution.

### ul...@chromium.org (2014-03-21)

I fixed a related issue in https://code.google.com/p/v8/source/detail?r=20155, not sure if that one fixes your test too.

### mb...@chromium.org (2014-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-04-04)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Comment Deleted]

### ti...@chromium.org (2014-04-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-14)

Thanks for the report - $2000 for this one. I'll start the payment process today.

### ti...@chromium.org (2014-04-15)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-04-18)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you (Ref #233619). Thanks again for your help!

### cl...@chromium.org (2014-06-18)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/350434?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/350554, crbug.com/chromium/350563, crbug.com/chromium/350886]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079050)*
