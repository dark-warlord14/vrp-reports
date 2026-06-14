# Security: Heap buffer overflow in V8 ValueDeserializer::ReadJSArrayBuffer()

| Field | Value |
|-------|-------|
| **Issue ID** | [40086537](https://issues.chromium.org/issues/40086537) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ng...@tresorit.com |
| **Assignee** | jb...@chromium.org |
| **Created** | 2017-01-17 |
| **Bounty** | $5,500.00 |

## Description

**VULNERABILITY DETAILS**

There is an unchecked allocation in V8 ValueDeserializer::ReadJSArrayBuffer()  

that can cause a heap buffer overflow.  

In case of OOM JSArrayBuffer::SetupAllocationData() doesn't change the  

backing\_store in JSArrayBuffer and returns false. This return value is not  

checked and the buffer is assumed to be of the new length at the next memcpy() call.

It seems to me that backing\_store is somehow reused from a previous array,  

it points to a writable memory area but with smaller length.

I have attached a simple patch that should fix this vulnerability.

The bug was introduced in V8 with <https://codereview.chromium.org/2264403004>  

This has been merged into Chromium with <https://codereview.chromium.org/2283283002>  

Chromium versions from 55.0.2842.0 are affected.

**VERSION**

Chrome Version: Bug was introduced in 55.0.2842.0  

Operating System: Reproducible on Linux x64 but all OSes are affected

**REPRODUCTION CASE**

On Linux x64 the attached files can reproduce this crash with a high probability on  

current Canary builds (commit 94af7a6d022fc5368503a8c47480d012617376f3)  

and with a smaller probability (about 10%) on current stable version  

(Version 55.0.2883.87 (64-bit) on Linux x64).

Sorry for the large asmcrypto.js file in the repro case, but without it  

the probability of triggering this bug is much smaller. Most of the cases  

the tab crashes properly with CRASH\_OOM() in the main thread instead of the  

worker.  

That file was downloaded from an official asmcrypto download page:  

<http://vibornoff.com/asmcrypto.js>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

Type of crash: tab  

Crash State:

Thread 11 "DedicatedWorker" received signal SIGSEGV, Segmentation fault.  

[-------------------------------------------------------------registers--------------------------------------------------------------]  

RAX: 0x33b5f9182311 --> 0x0  

RBX: 0x1e8000  

RCX: 0x187791  

RDX: 0x1e8480  

RSI: 0x1d573e264cf5 --> 0x0  

RDI: 0x33b5f91e3000 --> 0x0  

RBP: 0xe242a437fa8 --> 0xe242a790000 --> 0xe2429c3c1e0 (0x00000e242a790000)  

RSP: 0x7fb6a3ec3438 --> 0x55fd11a3bc18 (<\_ZN2v88internal17ValueDeserializer17ReadJSArrayBufferEv+184>: add QWORD PTR [rbp+0x10],r1  

2)  

RIP: 0x7fb6b2d0ba96 (<\_\_memmove\_avx\_unaligned+710>: rep movs BYTE PTR es:[rdi],BYTE PTR ds:[rsi])  

R8 : 0xffffffff  

R9 : 0x0  

R10: 0x22 (")  

R11: 0x246  

R12: 0x1e8480  

R13: 0xe2429d451b0 --> 0x34bcaeff7d59 --> 0x41000038256c1064  

R14: 0x7fb6a3ec34a8 --> 0x55fd143a6ead (<\_ZN5blink11ScriptState4fromEN2v85LocalINS1\_7ContextEEE+109>: test rax,rax)  

R15: 0x0  

[----------------------------------------------------------------code----------------------------------------------------------------]  

0x7fb6b2d0ba8e <\_\_memmove\_avx\_unaligned+702>: jae 0x7fb6b2d0baa0 <\_\_memmove\_avx\_unaligned+720>  

0x7fb6b2d0ba90 <\_\_memmove\_avx\_unaligned+704>: mov rcx,rdx  

0x7fb6b2d0ba93 <\_\_memmove\_avx\_unaligned+707>: mov rcx,rdx  

=> 0x7fb6b2d0ba96 <\_\_memmove\_avx\_unaligned+710>: rep movs BYTE PTR es:[rdi],BYTE PTR ds:[rsi]  

0x7fb6b2d0ba98 <\_\_memmove\_avx\_unaligned+712>: ret  

0x7fb6b2d0ba99 <\_\_memmove\_avx\_unaligned+713>: nop DWORD PTR [rax+0x0]  

0x7fb6b2d0baa0 <\_\_memmove\_avx\_unaligned+720>: lea rcx,[rsi+rdx\*1]  

0x7fb6b2d0baa4 <\_\_memmove\_avx\_unaligned+724>: vmovdqu ymm4,YMMWORD PTR [rsi]  

[---------------------------------------------------------------stack----------------------------------------------------------------]  

00:0000| rsp 0x7fb6a3ec3438 --> 0x55fd11a3bc18 (<\_ZN2v88internal17ValueDeserializer17ReadJSArrayBufferEv+184>: add QWORD PTR [rbp+0x10],r12)  

01:0008| 0x7fb6a3ec3440 --> 0x42 (B)  

02:0016| 0x7fb6a3ec3448 --> 0x1d573e204003 --> 0x7a8980  

03:0024| 0x7fb6a3ec3450 --> 0x7fb6a3ec3558 --> 0x0  

04:0032| 0x7fb6a3ec3458 --> 0xea6efb0e080 --> 0x50e3b0ef00000003  

05:0040| 0x7fb6a3ec3460 --> 0x7fb6a3ec3558 --> 0x0  

06:0048| 0x7fb6a3ec3468 --> 0x7fb6a3ec36f8 --> 0xe242a437fa0 --> 0xe242a790000 --> 0xe2429c3c1e0 (0x00000e242a790000)  

07:0056| 0x7fb6a3ec3470 --> 0x33b5f9182351 --> 0x0  

[------------------------------------------------------------------------------------------------------------------------------------]  

Legend: stack, code, data, heap, rodata, value  

Stopped reason: SIGSEGV  

0x00007fb6b2d0ba96 in \_\_memmove\_avx\_unaligned () from /lib64/libc.so.6

gdb-peda$ bt  

#0 0x00007fb6b2d0ba96 in \_\_memmove\_avx\_unaligned () from /lib64/libc.so.6  

#1 0x000055fd11a3bc18 in v8::internal::ValueDeserializer::ReadJSArrayBuffer() ()  

#2 0x000055fd11a39ba0 in v8::internal::ValueDeserializer::ReadObjectInternal() ()  

#3 0x000055fd11a399c3 in v8::internal::ValueDeserializer::ReadObject() ()  

#4 0x000055fd113aa07f in v8::ValueDeserializer::ReadValue(v8::Local[v8::Context](javascript:void(0);)) ()  

#5 0x000055fd14438e93 in blink::V8ScriptValueDeserializer::deserialize() ()  

#6 0x000055fd14d9380e in blink::SerializedScriptValueForModulesFactory::deserialize(blink::SerializedScriptValue\*, v8::Isolate\*, blink::HeapVector<blink::Member[blink::MessagePort](javascript:void(0);), 0ul>\*, WTF::Vector<blink::WebBlobInfo, 0ul, WTF::PartitionAllocator> const\*) ()  

#7 0x000055fd15f6e7ea in blink::V8MessageEvent::dataAttributeGetterCustom(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) ()  

#8 0x000020656f0307cb in ?? ()  

#9 0x00007fb6a3ec3848 in ?? ()  

#10 0x00007fb6a3ec3880 in ?? ()  

#11 0x0000000000000000 in ?? ()

gdb-peda$ vmmap $rdi  

Start End Perm Name  

0x000033b5f91e3000 0x000033b5f9200000 ---p mapped

gdb-peda$ vmmap $rdi-1  

Start End Perm Name  

0x000033b5f9180000 0x000033b5f91e3000 rw-p mapped

## Attachments

- [repro.tar.gz](attachments/repro.tar.gz) (application/octet-stream, 27.0 KB)
- [v8.patch](attachments/v8.patch) (application/octet-stream, 871 B)

## Timeline

### do...@chromium.org (2017-01-18)

jbroman: can you please follow this up?

[Monorail components: Blink>JavaScript]

### do...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

### ha...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-18)

[Empty comment from Monorail migration]

### jb...@chromium.org (2017-01-18)

The value-serializer.cc change was merged to 55, yes, but the code isn't enabled until M57.

It looks like v8::ArrayBuffer::New and v8::SharedArrayBuffer::New (which was my reference here) also don't check the result. This is probably why 55 (and presumably older versions) can also be affected. I'm not sure there's an API-compatible way of fixing that (perhaps it should be returning MaybeLocal<ArrayBuffer>). The only mergable fix I can think of there is a CHECK that a buffer was successfully allocated. v8-folk, WDYT?

### ng...@tresorit.com (2017-01-18)

I can confirm that v8::ArrayBuffer::New and v8::SharedArrayBuffer::New miss this check too.
There was also a missing check in runtime-maths.cc before V8 version 5.6.18, so it is still missing in Chromium 55 (current stable). That call was removed in https://codereview.chromium.org/2402363002/diff/60001/src/runtime/runtime-maths.cc

I have rechecked what happens for my repro on 55 and the crash there really happens on the main thread (SIGILL, seems valid OOM handling). On 57 there are both main thread SIGILLs and the reported SIGSEGVs on the worker thread.

This means that currently only the Dev and Canary channels seem to be affected by the bug in ReadJSArrayBuffer(), but the current Stable version has 3 other places too (including the one in runtime-maths.cc)

### jk...@chromium.org (2017-01-19)

re #5 - Crashing on OOM is appropriate. (At least, when it's a system-imposed OOM, i.e. allocation failure. Self-imposed limits, like exceeding max string length or array length or whatever, are arguably a different matter.) So I don't think we need to change the API here.

re #6 - Thanks for checking! (And for the original report too!)

### bu...@chromium.org (2017-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/5e30385d62496544adacc7cb8e3c86694854b9f1

commit 5e30385d62496544adacc7cb8e3c86694854b9f1
Author: jbroman <jbroman@chromium.org>
Date: Thu Jan 19 15:22:17 2017

ValueSerializer: Fail decode if no memory is available when decoding ArrayBuffer.

BUG=chromium:681843

Review-Url: https://codereview.chromium.org/2645673002
Cr-Commit-Position: refs/heads/master@{#42510}

[modify] https://crrev.com/5e30385d62496544adacc7cb8e3c86694854b9f1/src/value-serializer.cc
[modify] https://crrev.com/5e30385d62496544adacc7cb8e3c86694854b9f1/test/unittests/value-serializer-unittest.cc


### jb...@chromium.org (2017-01-19)

#7: I only asked because when they're constructed by script, it can get a RangeError if there's too little memory, without bringing down the system. 

(Chromium has very few uses of this, so I'm not going to add another variant right now. I could imagine node.js or someone else complaining about this, but I suppose they always have the option of allocating the memory beforehand and passing that to v8::ArrayBuffer::New, though.)

### bu...@chromium.org (2017-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/ba2cd16986182ee80973f116ac277b93b7b285bf

commit ba2cd16986182ee80973f116ac277b93b7b285bf
Author: jbroman <jbroman@chromium.org>
Date: Thu Jan 19 16:23:07 2017

Mark JSArrayBuffer::SetupAllocatingData with WARN_UNUSED_RESULT.

Also update a call in cctest to check the result.

BUG=chromium:681843

Review-Url: https://codereview.chromium.org/2647573003
Cr-Commit-Position: refs/heads/master@{#42513}

[modify] https://crrev.com/ba2cd16986182ee80973f116ac277b93b7b285bf/src/objects.h
[modify] https://crrev.com/ba2cd16986182ee80973f116ac277b93b7b285bf/test/cctest/heap/test-page-promotion.cc


### jb...@chromium.org (2017-01-19)

The value-serializer stuff is in M57, but I'd like to consider merging this CL:
https://chromium.googlesource.com/v8/v8/+/ca0f957329828c61f02437f640ed8004a549018a
into M56 (v8 5.6). It should be a safe change (it simply crashes rather than proceeding in the case of memory allocation failure), and it looks like we still have some time before it goes stable.

Not super high priority, given that we haven't had reports SIGSEGV on M56 yet. Not worth merging to stable.

### sh...@chromium.org (2017-01-19)

This bug requires manual review: We are only 11 days from stable.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), gkihumba@(cros), bustamante@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jb...@chromium.org (2017-01-19)

I'm told that V8 branched for 5.7 already, so I'd also like to merge the following into M57:

https://chromium.googlesource.com/v8/v8/+/ca0f957329828c61f02437f640ed8004a549018a
https://chromium.googlesource.com/v8/v8/+/5e30385d62496544adacc7cb8e3c86694854b9f1

### sh...@chromium.org (2017-01-19)

This bug requires manual review: We don't branch M57 until 2017-01-19.
Please contact the milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@google.com (2017-01-19)

Approving for merge into M56

### sh...@chromium.org (2017-01-20)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-01-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-01-23)

+awhalley@ for M57 merge review.

### sh...@chromium.org (2017-01-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-01-23)

jbroman@ - did this get merged into M56 OK?

govind@ - good for 57 Merge.

### go...@chromium.org (2017-01-23)

Approving merge to M57 branch 2987 based on https://crbug.com/chromium/681843#c20. Please merge ASAP. Thank you.

### bu...@chromium.org (2017-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/67fbe8c63c86fd873f3bcf3bfff33df38fd4f2af

commit 67fbe8c63c86fd873f3bcf3bfff33df38fd4f2af
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Tue Jan 24 15:39:18 2017

Merged: Trigger OOM crash if no memory returned in v8::ArrayBuffer::New and v8::SharedArrayBuffe ...

Revision: ca0f957329828c61f02437f640ed8004a549018a

BUG=chromium:681843
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jbroman@chromium.org

Review-Url: https://codereview.chromium.org/2658433002 .
Cr-Commit-Position: refs/branch-heads/5.6@{#88}
Cr-Branched-From: bdd3886218dfe76e8560eb8a18401942452ae859-refs/heads/5.6.326@{#1}
Cr-Branched-From: 879f6599eee6e1dfcbe9a24bf688b261c03e9558-refs/heads/master@{#41014}

[modify] https://crrev.com/67fbe8c63c86fd873f3bcf3bfff33df38fd4f2af/src/api.cc


### bu...@chromium.org (2017-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/94651de33258436a8d07da656486724be8c6cfed

commit 94651de33258436a8d07da656486724be8c6cfed
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Tue Jan 24 15:41:08 2017

Merged: Squashed multiple commits.

Merged: Trigger OOM crash if no memory returned in v8::ArrayBuffer::New and v8::SharedArrayBuffer::New.
Revision: ca0f957329828c61f02437f640ed8004a549018a

Merged: ValueSerializer: Fail decode if no memory is available when decoding ArrayBuffer.
Revision: 5e30385d62496544adacc7cb8e3c86694854b9f1

BUG=chromium:681843
LOG=N
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true
R=jbroman@chromium.org

Review-Url: https://codereview.chromium.org/2657463004 .
Cr-Commit-Position: refs/branch-heads/5.7@{#20}
Cr-Branched-From: 975e9a320b6eaf9f12280c35df98e013beb8f041-refs/heads/5.7.492@{#1}
Cr-Branched-From: 8d76f0e3465a84bbf0bceab114900fbe75844e1f-refs/heads/master@{#42426}

[modify] https://crrev.com/94651de33258436a8d07da656486724be8c6cfed/src/api.cc
[modify] https://crrev.com/94651de33258436a8d07da656486724be8c6cfed/src/value-serializer.cc
[modify] https://crrev.com/94651de33258436a8d07da656486724be8c6cfed/test/unittests/value-serializer-unittest.cc


### jb...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-01-27)

Congratulations, the panel awarded $5,500 for this report!  A member of our finance team will be in touch shortly with more details.

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### aw...@chromium.org (2017-01-27)

[Empty comment from Monorail migration]

### of...@google.com (2017-03-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-04-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### of...@google.com (2018-06-18)

Removing Nodejs-backport-apporved as no active Node.js release lines should be affected. 8.x already should have the fix (V8 6.2), and 6.x (V8 5.1) didn't have the bug.

### is...@google.com (2018-06-18)

This issue was migrated from crbug.com/chromium/681843?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086537)*
