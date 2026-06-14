# V8 HeapObject pointing to JIT memory

| Field | Value |
|-------|-------|
| **Issue ID** | [40093496](https://issues.chromium.org/issues/40093496) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lu...@microsoft.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2018-12-18 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763

Steps to reproduce the problem:
1. I'm currently using V8 debug build with version 7.3.0 (d8-linux-debug-v8-component-58294)
2. OS: x86_64 Linux 4.15.0 / Ubuntu 18.04 
3. Run the PoC with D8 debug build, for example : d8-linux-debug-v8-component-58294/d8 poc.js

What is the expected behavior?

1. An assert:
	abort: CSA_ASSERT failed: IsStrong(object) [../../src/code-stub-assembler.cc:1333]

		==== JS stack trace =========================================

		    0: ExitFrame [pc: 0x7fe2a2508472]
		    1: StubFrame [pc: 0x7fe2a22d174c]
		Security context: 0x05be4e69b039 <JSObject>#0#
		/* ... */

2. Segmentation fault

	(gdb) r test.js
	The program being debugged has been started already.
	Start it from the beginning? (y or n) y
	Starting program: [...]/d8 test.js
	[Thread debugging using libthread_db enabled]
	Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
	[New Thread 0x7ffff44f5700 (LWP 4370)]
	[New Thread 0x7ffff3cf4700 (LWP 4371)]
	[New Thread 0x7ffff34f3700 (LWP 4372)]
	[New Thread 0x7ffff2cf2700 (LWP 4373)]
	[New Thread 0x7ffff24f1700 (LWP 4374)]

	Thread 1 "d8" received signal SIGSEGV, Segmentation fault.
	0x00007ffff7866aab in Builtins_StoreIC ()
	   from [...]/./libv8.so
	(gdb) disas $rip
	Dump of assembler code for function Builtins_StoreIC:

   0x00007ffff78669e0 <+0>:	push   rbp
   0x00007ffff78669e1 <+1>:	mov    rbp,rsp
   0x00007ffff78669e4 <+4>:	push   0x18
   0x00007ffff78669e6 <+6>:	sub    rsp,0x70
   0x00007ffff78669ea <+10>:	mov    QWORD PTR [rbp-0x20],rbx
   0x00007ffff78669ee <+14>:	mov    QWORD PTR [rbp-0x18],rdi
   0x00007ffff78669f2 <+18>:	mov    QWORD PTR [rbp-0x28],rdx
   0x00007ffff78669f6 <+22>:	mov    QWORD PTR [rbp-0x30],rcx
   0x00007ffff78669fa <+26>:	mov    QWORD PTR [rbp-0x38],rsi
   0x00007ffff78669fe <+30>:	mov    QWORD PTR [rbp-0x10],rax
   0x00007ffff7866a02 <+34>:	test   dl,0x1
   0x00007ffff7866a05 <+37>:	je     0x7ffff7866a21 <Builtins_StoreIC+65>
   0x00007ffff7866a07 <+39>:	mov    r8,rdx
   0x00007ffff7866a0a <+42>:	and    r8,0x3
   0x00007ffff7866a0e <+46>:	cmp    r8,0x1
   0x00007ffff7866a12 <+50>:	jne    0x7ffff786e09e <Builtins_StoreIC+30398>
   0x00007ffff7866a18 <+56>:	mov    r8,QWORD PTR [rdx-0x1]   <-- read HeapObject->map into R8
   0x00007ffff7866a1c <+60>:	mov    rdi,r8                   <-- RDI now is HeapObject->map
   0x00007ffff7866a1f <+63>:	jmp    0x7ffff7866a96 <Builtins_StoreIC+182> <--- jump

   [...]

   0x00007ffff7866a96 <+182>:	mov    rax,rdi
   0x00007ffff7866a99 <+185>:	and    rax,0x3
   0x00007ffff7866a9d <+189>:	mov    QWORD PTR [rbp-0x60],rdi
   0x00007ffff7866aa1 <+193>:	cmp    rax,0x1
   0x00007ffff7866aa5 <+197>:	jne    0x7ffff786e0b0 <Builtins_StoreIC+30416>
=> 0x00007ffff7866aab <+203>:	mov    rax,QWORD PTR [rdi-0x1]        <-- seg fault as RDI is an invalid addresss
   0x00007ffff7866aaf <+207>:	cmp    QWORD PTR [r13+0x8],rax
   0x00007ffff7866ab3 <+211>:	jne    0x7ffff786e0c2 <Builtins_StoreIC+30434>
   0x00007ffff7866ab9 <+217>:	mov    rax,rdi
   0x00007ffff7866abc <+220>:	and    rax,0x3
   0x00007ffff7866ac0 <+224>:	cmp    rax,0x1
   0x00007ffff7866ac4 <+228>:	jne    0x7ffff786e0d7 <Builtins_StoreIC+30455>
   0x00007ffff7866aca <+234>:	mov    rax,QWORD PTR [rdi-0x1]
   0x00007ffff7866ace <+238>:	cmp    QWORD PTR [r13+0x8],rax
   0x00007ffff7866ad2 <+242>:	jne    0x7ffff786e0e9 <Builtins_StoreIC+30473>
   0x00007ffff7866ad8 <+248>:	mov    rax,rdi
   0x00007ffff7866adb <+251>:	and    rax,0x3
   0x00007ffff7866adf <+255>:	cmp    rax,0x1
   0x00007ffff7866ae3 <+259>:	jne    0x7ffff786e0fe <Builtins_StoreIC+30494>
   0x00007ffff7866ae9 <+265>:	test   DWORD PTR [rdi+0xf],0x800000
   0x00007ffff7866af0 <+272>:	jne    0x7ffff7872125 <Builtins_StoreIC+46917>
   0x00007ffff7866af6 <+278>:	mov    rax,QWORD PTR [rbp-0x20]
   0x00007ffff7866afa <+282>:	and    rax,0x3
   0x00007ffff7866afe <+286>:	cmp    rax,0x1
   0x00007ffff7866b02 <+290>:	jne    0x7ffff786e110 <Builtins_StoreIC+30512>
   0x00007ffff7866b08 <+296>:	mov    rax,QWORD PTR [rbp-0x20]
   0x00007ffff7866b0c <+300>:	mov    rbx,QWORD PTR [rax-0x1]
   0x00007ffff7866b10 <+304>:	cmp    QWORD PTR [r13+0x90],rbx
   0x00007ffff7866b17 <+311>:	jne    0x7ffff786e122 <Builtins_StoreIC+30530>

    [...]

	(gdb) info register
	rax            0x1	1
	rbx            0x146062e9e0b1	22404208910513
	rcx            0x146062e9db59	22404208909145
	rdx            0x2ccade3a5501	49249823380737            <---- HeapObject
	rsi            0x146062e9ddd9	22404208909785
	rdi            0x5630bb480008c25d	6210669804056527453   <---- HeapObject->map
	rbp            0x7ffffff07470	0x7ffffff07470
	rsp            0x7ffffff073f8	0x7ffffff073f8
	r8             0x5630bb480008c25d	6210669804056527453
	r9             0x2ccade3a5501	49249823380737
	r10            0x7ffff7872832	140737346218034
	r11            0x900000000	38654705664
	r12            0x146062e9ddd9	22404208909785
	r13            0x5555555aa990	93824992586128
	r14            0x0	0
	r15            0x7ffffff07478	140737487336568
	rip            0x7ffff7866aab	0x7ffff7866aab <Builtins_StoreIC+203>
	eflags         0x10246	[ PF ZF IF RF ]
	cs             0x33	51
	ss             0x2b	43
	ds             0x0	0
	es             0x0	0
	fs             0x0	0
	gs             0x0	0

What went wrong?
	The crash happens on Builtins_StoreIC that is called by the JIT code generated for the function "go" to store the 
	value 0x41424344 in the property "a" for the variable v_in (poc line 13). While trying to write the property, 
	we'll read the HeapObject->Map to check the object type, however, v_in object is pointing to the 
	JIT code generated for the "go" function. It'll lead to the crash as it'll interpret instructions as a pointer to Map Object.

	You can confirm it by looking both the call stack and the RDX address (that is the pointer to HeapObject), 
	for example:

	(gdb) bt
	#0  0x00007ffff7866aab in Builtins_StoreIC ()
	from [...] /./libv8.so
	#1  0x00002ccade3a54f9 in ?? ()              <-- JIT code for "go" this is a trampoline to StoreIC
	#2  0x0000000000000000 in ?? ()

	(gdb) x/16i $rdx -1                          <-- RDX is 0x2ccade3a5501
	   0x2ccade3a5500:	pop    rbp
	   0x2ccade3a5501:	ret    0x8
	   0x2ccade3a5504:	movabs rbx,0x7ffff7375630
	   0x2ccade3a550e:	xor    eax,eax
	   0x2ccade3a5510:	movabs rsi,0x146062e81749
	   0x2ccade3a551a:	movabs r10,0x7ffff7a57b40
	   0x2ccade3a5524:	call   r10
	   0x2ccade3a5527:	jmp    0x2ccade3a52ad
	   0x2ccade3a552c:	mov    rdx,QWORD PTR [r13-0x28]
	   0x2ccade3a5530:	jmp    0x2ccade3a5637
	   0x2ccade3a5535:	mov    QWORD PTR [rbp-0x20],rcx
	   0x2ccade3a5539:	mov    rax,r11
	   0x2ccade3a553c:	mov    rbx,QWORD PTR [rbp-0x30]
	   0x2ccade3a5540:	movabs rsi,0x146062e81749
	   0x2ccade3a554a:	movabs r10,0x7ffff7904820
	   0x2ccade3a5554:	call   r10

Did this work before? N/A 

Chrome version: 64.0.3282.140  Channel: n/a
OS Version: 10.0
Flash Version:

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 219 B)
- [mini.js](attachments/mini.js) (text/plain, 372 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### va...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2018-12-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5125001365422080.

### cl...@chromium.org (2018-12-18)

Testcase 5125001365422080 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5125001365422080.

### va...@chromium.org (2018-12-18)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-12-19)

[Empty comment from Monorail migration]

### va...@chromium.org (2018-12-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-01)

marja: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@chromium.org (2019-01-10)

Sorry, I missed this bug since I've been OOO since it was reported. Reassigning to stability sheriff for triage.

### ha...@chromium.org (2019-01-10)

[Empty comment from Monorail migration]

### ha...@chromium.org (2019-01-10)

To memory sheriff for a look.

### jg...@chromium.org (2019-01-10)

Passing on to jkummerow@ for triaging since the description mentions StoreIC or code calling StoreIC. Thanks!

### jk...@chromium.org (2019-01-10)

[Empty comment from Monorail migration]

### jk...@chromium.org (2019-01-10)

I can't repro (with V8 commit 7f21bbc11d0ec0d74b702b2c2728040b14788fe0 aka r58294 as specified in #0).

lupinhei, how long does it typically take until it crashes? Does it need several attempts? Do you have any local modifications to V8? Do you have a larger poc that's more reliable? What are your build flags (contents of args.gn)?

### lu...@microsoft.com (2019-01-10)

jkummerow@:

Hey, so here what I used to repro this bug:

1. The build that I was using came from https://commondatastorage.googleapis.com/v8-asan/index.html?prefix=linux-debug/, the one that I used to repro this bug was: d8-linux-debug-v8-component-58294

2. I'm currently using a Linux VM to repro it (Ubuntu 18.04)

3. I have no local modifications in V8

4. I have a larger PoC that was generated by the fuzzer, but it always repro with both minimized PoC and the original PoC.

Feel free to ask any question that I'll try to help as much as possible :)

### lu...@microsoft.com (2019-01-11)

jkummerow@:

I tried in the latest build the PoC.js and it didn't work, I did some adjust and it should work now in both Windows and Linux (I just compiled V8 for Windows today and it works fine).

Windows:
1. 
Commit: 469754d01c5e7259ba3fd87b4e8dd102214feb24
Flags for args.gn:
is_component_build = true
is_debug = true
symbol_level = 1
target_cpu = "x64"
use_goma = false
v8_enable_backtrace = true
v8_enable_slow_dchecks = true

When you run the PoC (it may require you try multiple times), it'll trigger the following DCHECK:

.\d8.exe .\mini.js
Go Johnny Go


#
# Fatal error in ../..\src/objects.h, line 1012
# Debug check failed: !IsSmi() == Internals::HasHeapObjectTag(ptr()) (1 vs. 0).
#
#
#
#FailureMessage Object: 000000F6371088A8
==== C stack trace ===============================

        v8::base::debug::StackTrace::StackTrace [0x00007FFA2D6616FB+27]
        v8::platform::DefaultPlatform::GetStackTracePrinter [0x00007FFA2E394A28+56]
        V8_Fatal [0x00007FFA2D658197+215]
        v8::base::SetDcheckFunction [0x00007FFA2D657DB3+51]
        v8::internal::CheckObjectType [0x00007FF9F6174BCA+34362]
        Builtins_DeleteProperty [0x00007FF9F6F034B7+503]


2. For Linux:
Go to commondatastorage link from #16 and get the d8-linux-debug-v8-component-58718, run the .js file and it should give you the same DCHECK.


I'm attaching both the minimized (mini.js) as well as the original output (1337.js) and you can try both



### jk...@chromium.org (2019-01-14)

Thanks!

With poc.js from #0, I can repro with a Debug build *without* v8_optimized_debug = false. With a Release build, or with the v8_optimized_debug = false flag present, I can't repro. I also can't repro with ToT; bisection says that the crash disappears with https://chromium-review.googlesource.com/c/v8/v8/+/1402791, but according to #17 that CL probably just breaks the repro (in the sense of no longer reproducing) without actually fixing the bug.

With mini.js from #17 and a full x64.debug build of 469754d01c5e7259ba3fd87b4e8dd102214feb24 on Linux, I can also repro, and catch it in GDB. Investigating...

### jk...@chromium.org (2019-01-15)

I've been playing with variations of mini.js in Release mode, revision = 469754d01c5e7259ba3fd87b4e8dd102214feb24.

-----
var str = "AISpsjFbWLAZEYyNzx8j5y";

function go() {
  try {
    for (var v_in in str) {
      try { go();} catch(e) {}
      try { new Uint32Array(4190);} catch(e) {}
    }
  } catch(e) {}
  //return v_in + "";
  //delete v_in.a;
  print(v_in);
}

go();
-----

Observations:
- putting any print statement (e.g. "print(1)", or "print(e)" into any of the catch(e){} blocks avoids the crash
- dropping any of the try..catch statements avoids the crash
- any of the last three lines ("return v_in + '';", "delete v_in.a", "print(v_in)" triggers the crash
- the crash happens because v_in is suddenly 0xffffffffffffffff
- reducing the length of {str} too far avoids the crash
- reducing the length of the Uint32Array too far avoids the crash
- --trace-gc indicates that we first do a series of Scavenges ("allocation failure"), and eventually switch to just doing Mark-Compacts ("finalize incremental marking via stack guard GC in old space requested"), with a brief transitionary period where both types of GC run are interleaved.
- changing the array from Uint32Array to plain Array avoids the crash and the Mark-Compact GCs (leaving only Scavenges).
- moving the declaration of "var v_in" out of the for-loop's header avoids the crash (e.g. "var v_in; for (v_in in str) {...}", or even out of the try-block)

Which leads me to the following handwavy strawman theory:
When the following coincide:
- a stack overflowing RangeError on an attempt to call a function,
- a mark-compact GC cycle (or maybe just incremental marking being active?),
- a try..catch statement nested within another, where both have empty catch(){} blocks
- a variable declared in a for-loop header
=> Then some stack slot in optimized code gets overwritten (maybe because some live range is too short?).

I don't know where to look for a bug of this kind. Any ideas?


### ja...@chromium.org (2019-01-15)

I looked at this briefly over the weekend, and it looked like the optimizing compiler "forgot" to reload a value from stack slot to register.

As far as I remember, the for in loop had two back edges and one of those was

call r10
jmp <loop-head>

Then in the loop header, r11 was used. The other backedge had a proper reload:

...
mov r11, [rbp-0x10]
...
jmp <loop-head>

This was a bit confusing because I thought we do not do multiple back edges. I did not have time to investigate in more detail.

### jk...@chromium.org (2019-01-23)

Well, can you make some time to investigate in more detail? :-)

### jk...@chromium.org (2019-01-23)

[Comment Deleted]

### ja...@chromium.org (2019-01-23)

Looking now... It is indeed a register allocation problem. It looks like exception handlers are not always getting the right moves. From the disassembly:

 -- B54 start (deconstruct frame) --
 -- <a.js:14:3> --
23d  movq r8,0xf39c5119cd1    ;; object: 0x0f39c5119cd1 <JSFunction print (sfi = 0xf39c5119c99)>
247  movq rsi,[r8+0x1f]
24b  movq rax,[r13-0x28] (root (undefined_value))
24f  push rax
250  movq r8,0x12b63a380179
25a  push r8
25c  push r8
25e  push r12                           ;; <- argument to print, this contained the BAD value that blew up in print.
260  movq rdx,0x55d204294470
26a  movl rcx,0x1
 -- Inlined Trampoline to CallApiCallback --
26f  movq r10,0x7f337b546e00  (CallApiCallback)
279  41ffd2         call r10

Clearly, this block expected the argument to print in register r12. Now let us see how we can get to this block:

 -- B51 start (deferred) --
 -- B52 start (deferred) --
421  movq rdx,r12
 -- B53 start (deferred) --
424  movq r8,[r13-0x20]
428  movq [r13+0x9ab8]
42f  movq r12,rdx
432  jmp 0x2a12e87045fd  <+0x23d>   ;; This jumps to B54 above.

Looking closer at that code, it appears that address 421 should have the argument to print in r12 for this to work.
Inspecting the handler table reveals that 421 is actually exception handler for the return site 3ce. This looks
broken because exception handlers can only legally use the value in rax; register r12 can be (will be) garbage.

Handler Table (size = 9)
  offset   handler
      71  ->   2af
     12c  ->   348
     161  ->   358
     1f4  ->   3f5
     223  ->   405
     2d6  ->   2db
     31d  ->   322
     387  ->   415
     3ce  ->   421

For completeness, the address 3ce is a return address of stack check:

     -- B36 start (deferred) (in loop 29) --
...
3cb  call r10                 ;; Stack check
3ce  movq r12,[rbp-0x50]
     -- B37 start (deferred) (in loop 29) --

That also looks bad because there should not be any move inserted between the call and the end of the basic block.

### ja...@chromium.org (2019-01-24)

We investigated some more with bmeurer@, here are the latest findings:

- The register allocation seems to be always broken for exception handlers of  for-in-loop stack checks. Normal for-loops do not suffer from the problem.

- It is very hard to trigger because it is hard to make a loop stack check throw an exception (since regular stack overflows would be caught by the function-entry stack check). The only way is to be close to the stack limit so that the stack check runtime function is already over the limit when an interrupt is triggered.

- The register allocation bug goes away when splintering is off (--noturbo-preprocess-ranges).

One can see the bug in generated code for simple for-in inside try-catch:


var str = new String("0123456789");
function f() {
  try {
    for (var i in str) {}
  } catch(e) {
    return i;
  }
}
f(); f(); %OptimizeFunctionOnNextCall(f); f();


Here, we get the following exception handler:

                  -- B43 start (deferred) --
                  -- B44 start (deferred) --
                  -- B45 start (deferred) --
0x3db939a031aa   3ea  498bc1         REX.W movq rax,r9
0x3db939a031ad   3ed  e904000000     jmp 0x3db939a031b6  <+0x3f6>

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/19b1538299c4c4d1f1838598eb5869c26c4f7917

commit 19b1538299c4c4d1f1838598eb5869c26c4f7917
Author: Stephan Herhut <herhut@chromium.org>
Date: Thu Jan 24 14:39:38 2019

[regalloc] Splinter to the end of interval if value dies

If a value dies in deferred code, there is no need to reload it at the
end of the deferred code, as it will be dead in the non-deferred code
that follows in control flow order. In the linearized view of register
allocation, this is encoded as a lifetime gap (or the end of an
interval).

Moreover, this may lead to wrong assignments if the value dies
between two deferred blocks and we leave a non-splintered live
range in the middle of deferred code.

Bug: chromium:915975
Change-Id: Iec68fe86f0dfbbac612635a637f3239475906d14
Reviewed-on: https://chromium-review.googlesource.com/c/1433784
Commit-Queue: Stephan Herhut <herhut@chromium.org>
Reviewed-by: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#59068}
[modify] https://crrev.com/19b1538299c4c4d1f1838598eb5869c26c4f7917/src/compiler/backend/live-range-separator.cc


### ja...@chromium.org (2019-01-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-25)

[Empty comment from Monorail migration]

### aw...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-28)

[Empty comment from Monorail migration]

### he...@chromium.org (2019-01-30)

This should be easy to merge back.

### he...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### he...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### ha...@chromium.org (2019-01-30)

Given that this is a super low risk merge and we are right at the beginning of the 72 cycle and that it fixes a crasher, let's merge it to 72 too.

### na...@google.com (2019-01-31)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-01-31)

Congrats! The Panel decided to reward $3,000 for this report :) 

### na...@google.com (2019-01-31)

Someone from finance will be in touch soon. 

Please let us know how you would like to be credited in the release notes. 

### na...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### na...@google.com (2019-01-31)

[Empty comment from Monorail migration]

### lu...@microsoft.com (2019-01-31)

Hi!

#35 and #36

Thank you very much! I'd like to donate my reward to charity, how should I proceed? 

And I'd like to be credited as "Lucas Pinheiro, Microsoft Browser Vulnerability Research"

### sh...@chromium.org (2019-02-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ci...@chromium.org (2019-02-04)

[Empty comment from Monorail migration]

### he...@chromium.org (2019-02-05)

These have been merged into v8 7.2 and 7.3.

### aw...@google.com (2019-02-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### na...@google.com (2020-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/915975?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093496)*
