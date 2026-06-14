# Security: Race condition in Flash workers may cause an exploitable double free by abusing bytearray.writeObject

| Field | Value |
|-------|-------|
| **Issue ID** | [40081355](https://issues.chromium.org/issues/40081355) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2014-0574, CVE-2015-0312 |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-02-06 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

Race condition in Flash workers may cause an exploitable double free by abusing bytearray.writeObject.

**VERSION**  

Chrome Version: 40.0.2214.111 stable, Flash 16.0.0.305  

Operating System: Win7 SP1 x64

The bug is very similar to CVE-2014-0574 or CVE-2015-0312.  

There's a thread writing to a bytearray and another one running bytearray.writeObject() followed by clear().  

During this process a race condition may occur which leads to delete the bytearray twice. The idea consists  

in reallocating the freed space with multiple bytearrays and checking them one by one. At some point, there  

should be two bytearrays pointing to the same buffer. If we free one of them and reallocate a vector here,  

we can overwrite its length with the other which is enough to read/write anywhere in memory.

Tested on Chrome 40.0.2214.111, Flash 16.0.0.305 on Windows 7 SP1 x64.  

Compile with mxmlc -target-player 15.0 -swf-version 25 DoubleFreeArrayQuad.as.  

Just put DoubleFreeArrayQuad.swf in a browsable directory and run the swf.

Some potential crashes :  

CPU Disasm  

Address Hex dump Command Comments  

6AB20A4F 8941 10 MOV DWORD PTR DS:[ECX+10],EAX  

6AB20A52 8B50 0C MOV EDX,DWORD PTR DS:[EAX+0C]  

6AB20A55 5F POP EDI  

6AB20A56 8951 0C MOV DWORD PTR DS:[ECX+0C],EDX  

6AB20A59 5E POP ESI  

6AB20A5A 894A 10 MOV DWORD PTR DS:[EDX+10],ECX ; crash here  

6AB20A5D 8948 0C MOV DWORD PTR DS:[EAX+0C],ECX  

6AB20A60 5B POP EBX  

6AB20A61 C2 0800 RETN 8

CPU Disasm  

Address Hex dump Command Comments  

69BDECBA 66:FF46 10 INC WORD PTR DS:[ESI+10]  

69BDECBE 8B06 MOV EAX,DWORD PTR DS:[ESI]  

69BDECC0 66:8B4E 10 MOV CX,WORD PTR DS:[ESI+10]  

69BDECC4 85C0 TEST EAX,EAX  

69BDECC6 74 08 JE SHORT 69BDECD0  

69BDECC8 8B10 MOV EDX,DWORD PTR DS:[EAX] ; crash here  

69BDECCA 8916 MOV DWORD PTR DS:[ESI],EDX  

69BDECCC 8BD8 MOV EBX,EAX  

69BDECCE EB 19 JMP SHORT 69BDECE9

## Attachments

- [DoubleFreeArrayQuad.zip](attachments/DoubleFreeArrayQuad.zip) (application/zip, 10.4 KB)

## Timeline

### wf...@chromium.org (2015-02-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-06)

Thanks. I've got this :)

### js...@chromium.org (2015-02-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-07)

There was a boss. And he did some calculating. Nice.

Report sent to Adobe; I'll update with the PSIRT tracking ID when I get it.

### sc...@gmail.com (2015-02-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-07)

@biloulehibou: also, when are you going to start exploiting on 64-bit Windows, just to be extra 1337? :-D

### sc...@gmail.com (2015-02-07)

Adobe tracking id: PSIRT-3288

### bi...@gmail.com (2015-02-07)

For 64b I'll show you at pwn2own, eventually ;).

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

This issue was migrated from crbug.com/chromium/456101?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081355)*
