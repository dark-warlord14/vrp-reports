# Security: Use After Free in Flash MessageChannel.send()

| Field | Value |
|-------|-------|
| **Issue ID** | [40080921](https://issues.chromium.org/issues/40080921) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-11-28 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

There's a use after free in MessageChannel.send(). Apparently, running concurrent workers and having the page reloaded can trigger the bug.

**VERSION**  

Chrome Version: [39.0.2171.71] + [stable]  

Operating System: [Windows 7 SP1 x64]

```
Steps to repro:  
    .one worker calls MessageChannel.send()  
    .the page is reloaded at this time  
    .a second worker maps the freed space with a vector of 0x7F0 bytes  
  
To trigger we have to call BitmapData.copyPixelsToByteArray() using a shared bytearray. Though totally unrelated, it seems necessary!  
  
On success, flash crashes while dereferencing 0x41424344.  
With pepflashplayer based at 0x6D390000, these lines are called after entering MessageChannel.send:  

```

CPU Disasm  

Address Hex dump Command Comments  

6D6A9480 8B46 5C MOV EAX,DWORD PTR DS:[ESI+5C]  

6D6A9483 8B0CB8 MOV ECX,DWORD PTR DS:[EDI\*4+EAX]  

6D6A9486 3BCB CMP ECX,EBX  

6D6A9488 74 05 JE SHORT 6D6A948F  

6D6A948A 8B01 MOV EAX,DWORD PTR DS:[ECX]  

6D6A948C FF50 04 CALL DWORD PTR DS:[EAX+4] ; call the function below  

6D6A948F 4F DEC EDI  

6D6A9490 ^ 79 EE JNS SHORT 6D6A9480

CPU Disasm  

Address Hex dump Command Comments  

6D6A8A08 8B49 04 MOV ECX,DWORD PTR DS:[ECX+4]  

6D6A8A0B 8B41 08 MOV EAX,DWORD PTR DS:[ECX+8]  

6D6A8A0E 8B40 14 MOV EAX,DWORD PTR DS:[EAX+14]  

6D6A8A11 8B40 04 MOV EAX,DWORD PTR DS:[EAX+4] ; the bad reference is kept here  

6D6A8A14 80B8 D4050000 0 CMP BYTE PTR DS:[EAX+5D4],0  

6D6A8A1B 75 12 JNE SHORT 6D6A8A2F  

6D6A8A1D 8B80 F8000000 MOV EAX,DWORD PTR DS:[EAX+0F8]  

6D6A8A23 85C0 TEST EAX,EAX  

6D6A8A25 74 08 JE SHORT 6D6A8A2F  

6D6A8A27 FF71 24 PUSH DWORD PTR DS:[ECX+24]  

6D6A8A2A E8 8246EFFF CALL 6D59D0B1 ; call the function below  

6D6A8A2F C3 RETN

CPU Disasm  

Address Hex dump Command Comments  

6D59D0B1 56 PUSH ESI  

6D59D0B2 8BF0 MOV ESI,EAX  

6D59D0B4 807E 71 00 CMP BYTE PTR DS:[ESI+71],0 ; esi = 0x41424344 if the vector replaced the freed space  

6D59D0B8 75 50 JNE SHORT 6D59D10A  

6D59D0BA 8B06 MOV EAX,DWORD PTR DS:[ESI]  

6D59D0BC 8BCE MOV ECX,ESI  

6D59D0BE FF50 10 CALL DWORD PTR DS:[EAX+10]

```
Tested on Chrome Stable 39.0.2171.71, Flash 15.0.0.239 on Windows 7 SP1 x64.  
Compile with mxmlc -target-player 15.0 -swf-version 25 OverAndOut.as.  
Just put OverAndOut.swf along with OverAndOut.html in a browsable directory and run the html.  

```

## Attachments

- [MessageChannel_uaf.zip](attachments/MessageChannel_uaf.zip) (application/zip, 4.4 KB)

## Timeline

### ke...@chromium.org (2014-11-28)

Chris: I am assigning all of these Flash bugs to you for triage. Please let me know if there is something else I should be doing with them.

### cl...@chromium.org (2014-12-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-12-01)

Got it, I think, on 32-bit Windows:

https://crash.corp.google.com/browse?stbtiq=d1055f741da810d2

Thread 10 CRASHED [EXCEPTION_ACCESS_VIOLATION_READ @ 0x414243b5] MAGIC SIGNATURE THREAD

### sc...@gmail.com (2014-12-01)

Sent to Adobe.

### sc...@gmail.com (2014-12-02)

Adobe tracking as PSIRT-3164

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-04)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-07)

Fixed in the Flash included here: http://googlechromereleases.blogspot.com/2015/02/stable-channel-update.html

https://helpx.adobe.com/security/products/flash-player/apsb15-04.html

### cl...@chromium.org (2015-02-07)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

Merge not required - see #9.

### ti...@google.com (2015-04-09)

Congrats - $5000 for this report.

Notes from panel: "PoC shows control of ESI, but it's effectively control of EIP because the asm code is loading a vtable from ESI."

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-16)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-06-03)

Processing via our *new* e-payment system should only take a 7-10 days and the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/437441?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080921)*
