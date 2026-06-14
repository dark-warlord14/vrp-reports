# [LangFuzz] Crash at v8::internal::Object::Lookup

| Field | Value |
|-------|-------|
| **Issue ID** | [40094693](https://issues.chromium.org/issues/40094693) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>JavaScript |
| **Reporter** | de...@googlemail.com |
| **Assignee** | km...@chromium.org |
| **Created** | 2011-09-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The javascript code below causes Chromium 15 to crash in V8.

**VERSION**  

Chrome Version: 15.0.871.0 (Developer Build 99583 Linux)  

Operating System: Ubuntu 11.04

**REPRODUCTION CASE**

function Test() {  

var left = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";  

var right = "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY";  

for (var i = 0; i < 100000; i++) {  

var cons = left + right;  

var substring = cons.substring(20, 80);  

try {  

with ({Test: 'inner' + i})  

continue;  

} finally { }  

}  

}  

Test();

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

Program received signal SIGSEGV, Segmentation fault.  

0x0103e85d in v8::internal::Object::Lookup(v8::internal::String\*, v8::internal::LookupResult\*) ()  

(gdb) bt  

#0 0x0103e85d in v8::internal::Object::Lookup(v8::internal::String\*, v8::internal::LookupResult\*) ()  

#1 0x35524479 in ?? ()  

Backtrace stopped: previous frame inner to this frame (corrupt stack?)  

(gdb) info register  

eax 0x35524021 894582817  

ecx 0xffffffff -1  

edx 0x0 0  

ebx 0x3555894 55924884  

esp 0xbfffd4e0 0xbfffd4e0  

ebp 0x3fcee081 0x3fcee081  

esi 0xbfffd5c4 -1073752636  

edi 0x2685366d 646264429  

eip 0x103e85d 0x103e85d <v8::internal::Object::Lookup(v8::internal::String\*, v8::internal::LookupResult\*)+93>  

eflags 0x210293 [ CF AF SF IF RF ID ]  

cs 0x73 115  

ss 0x7b 123  

ds 0x7b 123  

es 0x7b 123  

fs 0x0 0  

gs 0x33 51  

(gdb) x /4i $pc  

=> 0x103e85d <\_ZN2v88internal6Object6LookupEPNS0\_6StringEPNS0\_12LookupResultE+93>: mov (%ecx),%eax  

0x103e85f <\_ZN2v88internal6Object6LookupEPNS0\_6StringEPNS0\_12LookupResultE+95>: and $0xffffe000,%eax  

0x103e864 <\_ZN2v88internal6Object6LookupEPNS0\_6StringEPNS0\_12LookupResultE+100>: mov 0x14(%eax),%ebp  

0x103e867 <\_ZN2v88internal6Object6LookupEPNS0\_6StringEPNS0\_12LookupResultE+103>: cmp 0x12c(%ebp),%edx

## Timeline

### js...@chromium.org (2011-09-06)

This looks like a straight NULL deref, but I don't have enough context to be sure. Punting off  to the V8 guys for further analysis and a fix.

### ag...@chromium.org (2011-09-07)

Probably something with the weird try/with/finally/continue structure?

### km...@chromium.org (2011-09-07)

I'll take this one.

### km...@chromium.org (2011-09-07)

[Empty comment from Monorail migration]

### km...@chromium.org (2011-09-07)

Thanks for the report.  We were not correctly restoring the context for abrupt exit (break, continue) from inside a with or catch nested inside the try block of try/finally.

Fixed in http://code.google.com/p/v8/source/detail?r=9160

This affects V8's 3.5 branch, so I'll push the fix there.

### sc...@gmail.com (2011-09-07)

Seems like a nasty corruption?

### js...@chromium.org (2011-09-07)

@kmillikin - I'm trying to clarify the impact. Are you saying the context pointer is corrupt or freed at this state (which would potentially be exploitable)? Or are you saying that the context pointer is in a predictable but non-dangerous state (e.g. NULL) when we crash. When I looked in the debugger, it appeared that we always crash dereffing -1 in READ_FIELD because the HeapObject's this pointer is NULL. However, I'm not sure if the conditions that get us to this state could be manipulated to some dangerous effect.

### km...@chromium.org (2011-09-07)

Hi jschuh, it's the same severity as https://crbug.com/chromium/91120.

The context pointer can be made to point to some other context in the same context chain (implemented as a linked list of contexts) or to be NULL.  Contexts have varying predictable lengths and we will normally index into them without a bounds check from generated code.

So this could be used to get controlled read/write access to other objects in the V8 heap; an attacker would also have to control/predict where those objects are.

### sc...@gmail.com (2011-09-07)

Thanks Kevin!!

### sc...@gmail.com (2011-09-08)

@decoder.oh: thanks for catching these regressions! Another $1000 for this one.

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

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/95485?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>JavaScript]
[Monorail mergedwith: crbug.com/chromium/95659]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094693)*
