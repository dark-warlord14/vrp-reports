# [LangFuzz] Crash at v8::internal::Deoptimizer::DoComputeOutputFrames with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40076717](https://issues.chromium.org/issues/40076717) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-12-18 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20121216 Firefox/19.0

Steps to reproduce the problem:
1. Run the attached testcase in d8 with --always-opt

What is the expected behavior?

What went wrong?
Crash:

==15948== Use of uninitialised value of size 4
==15948==    at 0x80A2C0B: v8::internal::Deoptimizer::DoComputeOutputFrames() (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x476DF60B: ???
==15948==    by 0x3DB167A8: ???
==15948==    by 0x3DB2B8D7: ???
==15948==    by 0x3DB22258: ???
==15948==    by 0x3DB13569: ???
==15948==    by 0x80B3FC5: v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x80B5850: v8::internal::Execution::Call(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*, bool) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x805D96F: v8::Script::Run() (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x804DE82: v8::Shell::ExecuteString(v8::Handle<v8::String>, v8::Handle<v8::Value>, bool, bool) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x80500EB: v8::SourceGroup::Execute(v8::Isolate*) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x8050E05: v8::Shell::RunMain(v8::Isolate*, int, char**) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948== 
==15948== Invalid read of size 4
==15948==    at 0x80A2C0B: v8::internal::Deoptimizer::DoComputeOutputFrames() (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x476DF60B: ???
==15948==    by 0x3DB167A8: ???
==15948==    by 0x3DB2B8D7: ???
==15948==    by 0x3DB22258: ???
==15948==    by 0x3DB13569: ???
==15948==    by 0x80B3FC5: v8::internal::Invoke(bool, v8::internal::Handle<v8::internal::JSFunction>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x80B5850: v8::internal::Execution::Call(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Object>, int, v8::internal::Handle<v8::internal::Object>*, bool*, bool) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x805D96F: v8::Script::Run() (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x804DE82: v8::Shell::ExecuteString(v8::Handle<v8::String>, v8::Handle<v8::Value>, bool, bool) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x80500EB: v8::SourceGroup::Execute(v8::Isolate*) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==    by 0x8050E05: v8::Shell::RunMain(v8::Isolate*, int, char**) (in /scratch/holler/LangFuzz/v8-trunk/out/ia32.release/d8)
==15948==  Address 0x3b51f81c is not stack'd, malloc'd or (recently) free'd

Did this work before? N/A 

Chrome version: 25.0.1359.3  Channel: dev
OS Version: Ubuntu 12.04

Not tested in the browser because the issue requires --always-opt to reproduce properly.

## Attachments

- [crash20121218-crashDeoptimize.js](attachments/crash20121218-crashDeoptimize.js) (text/plain; charset=us-ascii, 2.0 KB)

## Timeline

### de...@googlemail.com (2012-12-18)

Forgot to mention that it's possible to reproduce this without --always-opt, but the testcase is much larger and not very stable then. This one should work much better to find the actual issue.

### in...@chromium.org (2012-12-18)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-12-18)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-12-18)

[Empty comment from Monorail migration]

### [Deleted User] (2012-12-18)

Fix is under review (https://codereview.chromium.org/11617018/), needs to be merged back to 3.15 branch, too.

### pa...@chromium.org (2012-12-18)

FWIW, I get a somewhat different stack trace with a debug build from svn trunk:

(gdb) run --always-opt ~/crash20121218-crashDeoptimize.js 
Starting program: /usr/local/google/home/palmer/v8-trunk/out/x64.debug/d8 --always-opt ~/crash20121218-crashDeoptimize.js
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/grte/v3/lib64/libthread_db.so.1".
[New Thread 0x7ffff7ff8700 (LWP 10645)]


#
# Fatal error in ../src/objects-inl.h, line 1754
# CHECK(index >= 0 && index < this->length()) failed
#


Program received signal SIGTRAP, Trace/breakpoint trap.
v8::internal::OS::DebugBreak () at ../src/platform-linux.cc:415
415     }
(gdb) bt
#0  v8::internal::OS::DebugBreak () at ../src/platform-linux.cc:415
#1  0x00000000007ef788 in v8::internal::OS::Abort () at ../src/platform-linux.cc:397
#2  0x0000000000461e28 in V8_Fatal (file=0x826555 "../src/objects-inl.h", line=1754, format=0x826408 "CHECK(%s) failed") at ../src/checks.cc:58
#3  0x000000000040c2b8 in v8::internal::FixedArray::get (this=0x307796581e41, index=1300337983) at ../src/objects-inl.h:1754
#4  0x000000000048af84 in v8::internal::DeoptimizationInputData::ArgumentsStackHeight (this=0x307796581e41, i=1398826318) at ../src/objects.h:4103
#5  0x000000000048904d in v8::internal::Deoptimizer::ComputeOutgoingArgumentSize (this=0xd0c4d0) at ../src/deoptimizer.cc:1368
#6  0x0000000000488f7d in v8::internal::Deoptimizer::ComputeInputFrameSize (this=0xd0c4d0) at ../src/deoptimizer.cc:1341
#7  0x000000000048605b in v8::internal::Deoptimizer::Deoptimizer (this=0xd0c4d0, isolate=0xcc50b0, function=0x30779657fd19, type=v8::internal::Deoptimizer::EAGER, bailout_id=1398826318, from=0x0, 
    fp_to_sp_delta=16, optimized_code=0x0) at ../src/deoptimizer.cc:453
#8  0x0000000000484f7a in v8::internal::Deoptimizer::New (function=0x30779657fd19, type=v8::internal::Deoptimizer::EAGER, bailout_id=1398826318, from=0x0, fp_to_sp_delta=16, isolate=0xcc50b0)
    at ../src/deoptimizer.cc:97
#9  0x00001364a3aa85c0 in ?? ()
#10 0x00007fffffffd1a0 in ?? ()
#11 0x0000000000cc7e18 in ?? ()
#12 0x00007fffffffd290 in ?? ()
#13 0x0000000000000002 in ?? ()
#14 0x0000000000cc5148 in ?? ()
#15 0x0000000100000000 in ?? ()
#16 0x00007ffff716f710 in ?? () from /lib/x86_64-linux-gnu/libc.so.6
#17 0x00001364a3aa8500 in ?? ()
#18 0x0000000000000000 in ?? ()

Notably, no crash with svenpanne's patch applied.

### pa...@chromium.org (2012-12-18)

FWIW, chrome with --js-flags="--always-opt" and the crash script put into an HTML file just seems to hang Chrome (ToT, debug, Linux). Do we think this bug is reachable/exploitable in Chrome?

Judging by svn blame and log, this is a recent regression (12 Nov 2012, V8 version 3.15.2). Affects dev only.

### pa...@chromium.org (2012-12-18)

[Empty comment from Monorail migration]

### de...@googlemail.com (2012-12-18)

The issue is even reproducible without --always-opt, but it gets very complex then.

### [Deleted User] (2012-12-19)

The fix landed as https://code.google.com/p/v8/source/detail?r=13237 in v8's bleeding_edge. We are waiting for some canary coverage before we merge this into the 3.15 branch. The bug itself was introduced in https://code.google.com/p/v8/source/detail?r=12877, which is not in any stable version AFAICT. Furthermore, exploiting this would be *extremely* hard, especially without --always-opt and our ASLR.

### in...@chromium.org (2012-12-19)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-21)

What's the underlying fault here? Just a bad read or also potential memory corruption?

### [Deleted User] (2012-12-21)

The problem was that a jump table containing "push <immediate>; j <someGenericEntry>" pairs was not resized correctly, so it could end up being too small. In the concrete example above, this accidentally resulted in an out-of-bounds read some time later (the stack height was wrong, too, but that didn't show up), but basically anything could happen because a jump might end up not landing at a jump table entry, but somewhere in the code following it. Given the way how and when we use the table (deopting) + ASLR + a GC which moves code around, I seriously doubt that you could construct a reproducible exploit. Famous last words... ;-)

### sc...@gmail.com (2013-01-11)

M25: http://code.google.com/p/v8/source/detail?r=13359

### sc...@gmail.com (2013-01-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-22)

@decoder: another nice one, $1000

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-02-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/166554?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076717)*
