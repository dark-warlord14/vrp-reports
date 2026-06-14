# [LangFuzz] Crash at v8::internal::ElementsAccessorBase with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40094845](https://issues.chromium.org/issues/40094845) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | de...@googlemail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2011-09-08 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The one-line javascript testcase below crashes in Chrome 15 and V8 shells, tested on 64 bit. Note that the testcase only works in Chrome or D8, not in shell, because it requires typed arrays.

In addition to the gdb information from the browser, I took a valgrind trace from the d8 shell:

==3451== Invalid read of size 1  

==3451== at 0x45C277: v8::internal::ElementsAccessorBase<v8::internal::ExternalByteElementsAccessor, v8::internal::ExternalByteArray>::Get(v8::internal::FixedArrayBase\*, unsigned int, v8::internal::JSObject\*, v8::internal::Object\*) (in /scratch/holler/LangFuzz/v8\_bleeding\_edge-64/d8)  

==3451== by 0x52EA80: v8::internal::Object::GetElementWithReceiver(v8::internal::Object\*, unsigned int) (in /scratch/holler/LangFuzz/v8\_bleeding\_edge-64/d8)  

==3451== by 0x48B53B: v8::internal::GetElement(v8::internal::Handle[v8::internal::Object](javascript:void(0);), unsigned int) (in /scratch/holler/LangFuzz/v8\_bleeding\_edge-64/d8)  

==3451== by 0x58E844: v8::internal::Runtime\_GetOwnProperty(v8::internal::Arguments, v8::internal::Isolate\*) (in /scratch/holler/LangFuzz/v8\_bleeding\_edge-64/d8)  

==3451== by 0x1F7A7DD5C341: ???  

==3451== by 0x1F7A7DD6934C: ???  

==3451== by 0x1F7A7DD8FD8D: ???  

==3451== by 0x1F7A7DD8FA43: ???  

==3451== by 0x1F7A7DD5CC2D: ???  

==3451== by 0x1F7A7DD8F727: ???  

==3451== by 0x1F7A7DD5CC2D: ???  

==3451== by 0x1F7A7DD8F349: ???  

==3451== Address 0x2a00000001 is not stack'd, malloc'd or (recently) free'd

**VERSION**  

Chrome Version: 15.0.865.0 (Developer Build 98568 Linux)  

Operating System: Ubuntu 11.04 64 bit

**REPRODUCTION CASE**

[0].every(function(){ Object.seal((new Int8Array(42))); });

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State (GDB trace taken from renderer process):

Program received signal SIGSEGV, Segmentation fault.  

0x00007ffff599696c in v8::internal::ElementsAccessorBase<v8::internal::ExternalByteElementsAccessor, v8::internal::ExternalByteArray>::Get(v8::internal::FixedArrayBase\*, unsigned int, v8::internal::JSObject\*, v8::internal::Object\*) ()  

(gdb) bt  

#0 0x00007ffff599696c in v8::internal::ElementsAccessorBase<v8::internal::ExternalByteElementsAccessor, v8::internal::ExternalByteArray>::Get(v8::internal::FixedArrayBase\*, unsigned int, v8::internal::JSObject\*, v8::internal::Object\*) ()  

#1 0x00007ffff585e537 in v8::internal::Object::GetElementWithReceiver(v8::internal::Object\*, unsigned int) ()  

#2 0x00007ffff57cf4ef in v8::internal::GetElement(v8::internal::Handle[v8::internal::Object](javascript:void(0);), unsigned int) ()  

#3 0x00007ffff58bc332 in v8::internal::Runtime\_GetOwnProperty(v8::internal::Arguments, v8::internal::Isolate\*) ()  

#4 0x00002492a762e14e in ?? ()  

#5 0x00002492a762e0c1 in ?? ()  

#6 0x00007fffffffb9d0 in ?? ()  

#7 0x00007fffffffba38 in ?? ()  

#8 0x00002492a7655ecd in ?? ()  

#9 0x000028251208c3b1 in ?? ()  

#10 0x000028251208bd81 in ?? ()  

[..snip.. only unresolved heap addresses here]

(gdb) x /4i $pc  

=> 0x7ffff599696c <\_ZN2v88internal20ElementsAccessorBaseINS0\_28ExternalByteElementsAccessorENS0\_17ExternalByteArrayEE3GetEPNS0\_14FixedArrayBaseEjPNS0\_8JSObjectEPNS0\_6ObjectE+12>: movsbl (%rax,%rdx,1),%eax  

0x7ffff5996970 <\_ZN2v88internal20ElementsAccessorBaseINS0\_28ExternalByteElementsAccessorENS0\_17ExternalByteArrayEE3GetEPNS0\_14FixedArrayBaseEjPNS0\_8JSObjectEPNS0\_6ObjectE+16>: shl $0x20,%rax  

0x7ffff5996974 <\_ZN2v88internal20ElementsAccessorBaseINS0\_28ExternalByteElementsAccessorENS0\_17ExternalByteArrayEE3GetEPNS0\_14FixedArrayBaseEjPNS0\_8JSObjectEPNS0\_6ObjectE+20>: retq  

0x7ffff5996975 <\_ZN2v88internal20ElementsAccessorBaseINS0\_28ExternalByteElementsAccessorENS0\_17ExternalByteArrayEE3GetEPNS0\_14FixedArrayBaseEjPNS0\_8JSObjectEPNS0\_6ObjectE+21>:  

jmp 0x7ffff5996978 <\_ZN2v88internal20ElementsAccessorBaseINS0\_28ExternalByteElementsAccessorENS0\_17ExternalByteArrayEE3GetEPNS0\_14FixedArrayBaseEjPNS0\_8JSObjectEPNS0\_6ObjectE+24>

(gdb) info register  

rax 0x2a00000000 180388626432  

rbx 0x28251208bd81 44139681463681  

rcx 0x28251208bd81 44139681463681  

rdx 0x1 1  

rsi 0x28251208d069 44139681468521  

rdi 0x7ffff8478840 140737358825536  

rbp 0x7ffff85410a8 0x7ffff85410a8  

rsp 0x7fffffffb8a8 0x7fffffffb8a8  

r8 0x28251208bd81 44139681463681  

r9 0x1 1  

r10 0x0 0  

r11 0x1 1  

r12 0x1 1  

r13 0x28251208bd81 44139681463681  

r14 0x7ffff8541000 140737359646720  

r15 0x7ffff87a5138 140737362153784  

rip 0x7ffff599696c 0x7ffff599696c <v8::internal::ElementsAccessorBase<v8::internal::ExternalByteElementsAccessor, v8::internal::ExternalByteArray>::Get(v8::internal::FixedArrayBase\*, unsigned int, v8::internal::JSObject\*, v8::internal::Object\*)+12>

## Timeline

### js...@chromium.org (2011-09-08)

Forwarding on to the v8 guys.

### da...@chromium.org (2011-09-09)

I'll take a look.

### da...@chromium.org (2011-09-09)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-09-12)

This bug allowed a external elements array to be interpreted as as number dictionary due to missing checks that prevented external elements arrays from getting normalized. I didn't spend a lot of time figuring out how it could be exploited, but it's a pretty egregious breakage of the type system, allowing arbitrary user-defined ints to be interrupted as object pointers. 

Fixed in v8:r9213 and merged into 3.3.10.37, 3.4.14.21 and 3.5.10.7 (M13-M15).

### sc...@gmail.com (2011-09-12)

Thanks Danno!

(Note to self: marking Merge-Approved until I work out if this made the M14 final build)

### sc...@gmail.com (2011-09-16)

Ah, this made it into 14.0.835.163
Cool.


### sc...@gmail.com (2011-09-16)

@decoder.oh: really nice bug, thanks for the 1-liner repro! Seems obviously good for a $1000 Chromium Security Reward.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-09-23)

Payment in system.

### de...@googlemail.com (2011-10-01)

No payment has been issued for this, please check your data. Thanks.

### sc...@gmail.com (2011-10-01)

See https://crbug.com/chromium/95920#c8, "Payment in system.", dated Sep 23rd. That's only a week old; the latency on payment (inter-bank wires etc). can be a lot higher.

### de...@googlemail.com (2011-10-01)

Sorry, what I meant was I didn't even receive the system email that I usually get. But if it's in the system, then just ignore this (and the ones from my email if that's the same issue) :). Thanks for looking into this.

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-09-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/95920?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094845)*
