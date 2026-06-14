# [LangFuzz] Crash on heap with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40092204](https://issues.chromium.org/issues/40092204) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2011-06-25 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The given testcase crashes in Chromium 14 and V8 with an invalid read. The read address seems to depend on the script details. For the testcase attached here, the address is 0xc0001eb, for a larger test I have (less minimized), it is showing:

==7201== Invalid read of size 8  

==7201== at 0x9F4B367: ???  

...  

==7201== Address 0x2e580b47 is not stack'd, malloc'd or (recently) free'd

**VERSION**  

Chrome Version: 14.0.802.0 (Developer Build 90326 Linux)  

Operating System: Ubuntu 11.04

**REPRODUCTION CASE**

function arrayEvery(arr, fun) {  

return Array.prototype.every.call(arr, fun);  

}  

function arraysEqual(a1, a2) {  

arrayEvery(a1, function (v, i) {  

});  

}  

function args(a) {  

return arguments;  

}  

try {  

assertEq(arraysEqual(args(1), [1]), true);  

} catch (e) {}  

value = '123';  

try {  

actual = Array.prototype.every.call(value, function (v, index, array) {  

});  

} catch (e) {}

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0xb3dbb9f7 in ?? ()  

(gdb) bt  

#0 0xb3dbb9f7 in ?? ()  

#1 0xb3da9761 in ?? ()  

#2 0xb3dc22ed in ?? ()  

#3 0xb3dbacfa in ?? ()  

#4 0xb3dabd6b in ?? ()  

#5 0x00fcdb93 in v8::internal::Invoke (construct=<value optimized out>,  

func=..., receiver=..., argc=0, args=0x0, has\_pending\_exception=0xbfffd94f)  

at v8/src/execution.cc:121  

#6 0x00fce275 in v8::internal::Execution::Call (callable=..., receiver=...,  

argc=0, args=0x0, pending\_exception=0xbfffd94f) at v8/src/execution.cc:158  

#7 0x00f9a2e6 in v8::Script::Run (this=0x355714c) at v8/src/api.cc:1552  

#8 0x016cd778 in WebCore::V8Proxy::runScript (this=0x3465000, script=...,  

isInlineCode=false)  

at third\_party/WebKit/Source/WebCore/bindings/v8/V8Proxy.cpp:435

(gdb) info registers  

eax 0x0 0  

ecx 0x6 6  

edx 0xb3dda655 -1277319595  

ebx 0xc0001ec 201327084  

esp 0xbfffd6a0 0xbfffd6a0  

ebp 0xbfffd6b8 0xbfffd6b8  

esi 0xb3e042d5 -1277148459  

edi 0x2 2  

eip 0xb3dbb9f7 0xb3dbb9f7  

eflags 0x10246 [ PF ZF IF RF ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

(gdb) x /8i $pc  

=> 0xb3dbb9f7: cmpl $0xb3d884a1,-0x1(%ebx)  

0xb3dbb9fe: jne 0xb3dbba4b  

0xb3dbba04: mov 0x3(%ebx),%ecx  

0xb3dbba07: sub $0x4,%ecx  

0xb3dbba0a: cmp %ecx,%eax  

0xb3dbba0c: jge 0xb3dbba2a  

0xb3dbba12: mov 0xf(%ebx,%eax,2),%ecx  

0xb3dbba16: cmp $0xb3dc807d,%ecx

## Timeline

### sc...@gmail.com (2011-06-25)

Confirmed on trunk, also affects x86_64 with similar register value :)


(gdb) disass $rip,$rip+20
Dump of assembler code from 0x7fffbc0cb2c7 to 0x7fffbc0cb2db:
=> 0x00007fffbc0cb2c7:	cmp    %r10,-0x1(%rbx)
   0x00007fffbc0cb2cb:	jne    0x7fffbc0cb339
   0x00007fffbc0cb2d1:	mov    0x7(%rbx),%rcx
   0x00007fffbc0cb2d5:	lea    (%r12,%r12,1),%r10
   0x00007fffbc0cb2d9:	sub    %r10,%rcx

rbx            0xc0001ec	201327084


Does not seem to affect M12, M13.
Unsure of severity for now, we'll have to see what the fix is.

### ag...@chromium.org (2011-06-27)

[Empty comment from Monorail migration]

### ag...@chromium.org (2011-06-27)

This was a recent regression introduced when we changed the handling of the arguments object. Thanks for the report. Fixed on bleeding_edge.

### sc...@gmail.com (2011-06-27)

Thanks, @decoder.oh! This seems like a object type confusion so definitely worth me sending it to the rewards panel.

### sc...@gmail.com (2011-08-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-24)

$1000

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

### sc...@gmail.com (2011-08-29)

Payment in system...

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

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

This issue was migrated from crbug.com/chromium/87478?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092204)*
