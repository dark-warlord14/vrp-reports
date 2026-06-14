# [LangFuzz] Crash at Runtime_QuoteJSONString with invalid write

| Field | Value |
|-------|-------|
| **Issue ID** | [40093291](https://issues.chromium.org/issues/40093291) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | de...@googlemail.com |
| **Assignee** | km...@chromium.org |
| **Created** | 2011-07-31 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code attached crashes Chromium 15.0.838.0 at function "Runtime\_QuoteJSONString" with an invalid write. This test is very fragile, even adding comments(!) to the JS code changes the address of write and maybe even the crash function. I attached only a semi-minimized testcase due to this instability and even this code crashes differently in the shell and Chromium. In my shell I get this:

==3901== Process terminating with default action of signal 11 (SIGSEGV)  

==3901== Access not within mapped region at address 0xB012C20  

==3901== at 0x80B090D: v8::internal::SetElement(v8::internal::Handle[v8::internal::JSObject](javascript:void(0);), unsigned int, v8::internal::Handle[v8::internal::Object](javascript:void(0);), v8::internal::StrictModeFlag) (in /scratch/holler/LangFuzz/v8\_bleeding\_edge/shell)

while in the browser, it crashes differently (see below). This was tested on 32 bit.

**VERSION**  

Chrome Version: 15.0.838.0 (Developer Build 94616 Linux) dev  

Operating System: Ubuntu 11.04, tested on 32 bit

**REPRODUCTION CASE**  

See attachment, too large to inline here.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

length (args=..., isolate=0x3581000) at v8/src/objects-inl.h:2102  

2102 v8/src/objects-inl.h: No such file or directory.  

in v8/src/objects-inl.h  

(gdb) bt  

#0 length (args=..., isolate=0x3581000) at v8/src/objects-inl.h:2102  

#1 IsFlat (args=..., isolate=0x3581000) at v8/src/objects-inl.h:2183  

#2 v8::internal::Runtime\_QuoteJSONString (args=..., isolate=0x3581000)  

at v8/src/runtime.cc:5339  

#3 0x422360b6 in ?? ()  

#4 0x5e5b0185 in ?? ()  

#5 0x5e5af82e in ?? ()  

#6 0x42237481 in ?? ()  

#7 0x42252d43 in ?? ()  

#8 0x422531da in ?? ()  

#9 0x42253c6c in ?? ()  

#10 0x42237481 in ?? ()  

#11 0x422529f4 in ?? ()  

#12 0x422494fa in ?? ()  

#13 0x42239deb in ?? ()  

#14 0x00f63433 in v8::internal::Invoke (construct=<value optimized out>,  

func=..., receiver=..., argc=0, args=0x0, has\_pending\_exception=0xbfffd9af)  

at v8/src/execution.cc:121  

#15 0x00f63b15 in v8::internal::Execution::Call (callable=..., receiver=...,  

argc=0, args=0x0, pending\_exception=0xbfffd9af) at v8/src/execution.cc:158  

#16 0x00f2eff6 in v8::Script::Run (this=0x3723bdc) at v8/src/api.cc:1555  

#17 0x017c7dd8 in WebCore::V8Proxy::runScript (this=0x35e6b80, script=...,  

isInlineCode=false)

(gdb) x /4i $pc  

=> 0x1063193 <v8::internal::Runtime\_QuoteJSONString(v8::internal::Arguments, v8::internal::Isolate\*)+323>: mov 0x3(%edx),%edx  

0x1063196 <v8::internal::Runtime\_QuoteJSONString(v8::internal::Arguments, v8::internal::Isolate\*)+326>: shr %edx  

0x1063198 <v8::internal::Runtime\_QuoteJSONString(v8::internal::Arguments, v8::internal::Isolate\*)+328>:  

je 0x10630aa <v8::internal::Runtime\_QuoteJSONString(v8::internal::Arguments, v8::internal::Isolate\*)+90>  

0x106319e <v8::internal::Runtime\_QuoteJSONString(v8::internal::Arguments, v8::internal::Isolate\*)+334>: mov %esi,(%esp)

(gdb) info registers  

eax 0x31 49  

ecx 0x5e5b0158 1583022424  

edx 0x6 6  

ebx 0x347de8c 55041676  

esp 0xbfffd5c0 0xbfffd5c0  

ebp 0x3581000 0x3581000  

esi 0x3705da61 923130465  

edi 0x1 1  

eip 0x1063193 0x1063193 <v8::internal::Runtime\_QuoteJSONString(v8::internal::Arguments, v8::internal::Isolate\*)+323>  

eflags 0x210246 [ PF ZF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

## Attachments

- [crashQuoteJSON.js](attachments/crashQuoteJSON.js) (text/x-c++; charset=us-ascii, 21.8 KB)

## Timeline

### sc...@gmail.com (2011-08-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-08-02)

Reproed with top of tree. Lasse has offered to take a look.

### lr...@chromium.org (2011-08-02)

[Empty comment from Monorail migration]

### km...@chromium.org (2011-08-02)

Yuck (and thanks for the report).  The bug is triggered by the code:

function f() {
  try {
    throw 0;
  } catch (e) {
    function g() { return e; }
  }
  g();
}

Ignore that it's not obvious what the programmer intends here.  We hoist the declaration of function g to function f's scope, but since http://code.google.com/p/v8/source/detail?r=8496 we compile g's body as if it's inside the catch.

The resulting off by one (in the length of the context chain) enables out of bounds writes (if a context is too short) and trashing the global context (by forcing a context write to overshoot by one).

Fixed in http://code.google.com/p/v8/source/detail?r=8783.

### km...@chromium.org (2011-08-02)

I've temporarily reverted the fix because it led to test failures.  Will reapply ASAP (tomorrow).

### sc...@gmail.com (2011-08-02)

Definitely a High severity based on description :)

### sc...@gmail.com (2011-08-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-02)

[Empty comment from Monorail migration]

### km...@chromium.org (2011-08-03)

I've reapplied the fix to bleeding edge in http://code.google.com/p/v8/source/detail?r=8797.  I've merged it to the 3.4 branch (it does not affect 3.3 and earlier).

### ke...@google.com (2011-08-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-24)

@decoder.oh: Thanks, good regression catch. Repro is kind of ugly, but definitely good for a $500 reward.

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

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-09-23)

Payment in system.

### js...@chromium.org (2011-10-05)

Batch update.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/91120?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093291)*
