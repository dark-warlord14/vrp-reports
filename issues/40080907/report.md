# Security: Race condition in workers may cause an exploitable double free by abusing bytearray.compress()

| Field | Value |
|-------|-------|
| **Issue ID** | [40080907](https://issues.chromium.org/issues/40080907) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **CVE IDs** | CVE-2014-0574 |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2014-11-24 |
| **Bounty** | $7,500.00 |

## Description

Race condition in workers may cause an exploitable double free by abusing bytearray.compress()

Tested: Chrome Stable 39.0.2171.65 (pepflashplayer.dll 15.0.0.223 32BIT) on Windows 7 SP1 x64

The issue occurs while sharing a bytearray between two workers. If one worker calls bytearray.compress() while the other uses that bytearray, Flash does not correctly handle the race and may double free the array. This issue is almost the same as CVE-2014-0574, reported at https://code.google.com/p/chromium/issues/detail?id=423703 and corrected at http://helpx.adobe.com/security/products/flash-player/apsb14-24.html.

This is just a poc for the moment, I think exploitation will slightly differs from the previous issue. I hope I'll get something more interesting by the end of the week.

With that poc Pepper Flash crashes most of the time while handling a linked list (pepflashplayer.dll based at 0x69C40000):

CPU Disasm
Address   Hex dump          Command                        
6A1AF981    8B41 0C         MOV EAX,DWORD PTR DS:[ECX+0C]
6A1AF984    8B51 10         MOV EDX,DWORD PTR DS:[ECX+10]
6A1AF987    FF75 0C         PUSH DWORD PTR SS:[EBP+0C]
6A1AF98A    8950 10         MOV DWORD PTR DS:[EAX+10],EDX    ; crash here, eax = 0
6A1AF98D    8B41 10         MOV EAX,DWORD PTR DS:[ECX+10]
6A1AF990    8B51 0C         MOV EDX,DWORD PTR DS:[ECX+0C]
6A1AF993    8950 0C         MOV DWORD PTR DS:[EAX+0C],EDX



Just put DoubleFreeArrayBis.swf to a browsable directory to trigger and compile with Flex:
mxmlc -target-player 15.0 -swf-version 25 DoubleFreeArrayBis.as



## Attachments

- [DoubleFreeArrayBis.zip](attachments/DoubleFreeArrayBis.zip) (application/zip, 3.1 KB)
- [DoubleFreeArrayBis_xpl.zip](attachments/DoubleFreeArrayBis_xpl.zip) (application/zip, 8.0 KB)

## Timeline

### sc...@gmail.com (2014-11-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-11-24)

Quick initial triage

Google Chrome	39.0.2171.65 (Official Build) 
Flash	15.0.0.223
Crash id: a7b0111317cd8465 (64-bit Linux)

Thread 0 CRASHED [SIGSEGV @ 0x00000bc1] MAGIC SIGNATURE THREAD￼
(In the memory manager)

Looks serious enough to me :)

### sc...@gmail.com (2014-11-24)

Adobe acknowledged with ID PSIRT-3159

### bi...@gmail.com (2014-11-26)

So it took less time than expected. Tell me if you see the magic too or if it's just on my computer :S (chrome stable 39.0.2171.71, flash 15.0.0.239).

### bi...@gmail.com (2014-11-26)

* on Windows 7 SP1 x64 *

### sc...@gmail.com (2014-11-26)

Confirmed a calc! Nice.

### sc...@gmail.com (2014-12-04)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### in...@chromium.org (2015-01-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-01-27)

[Empty comment from Monorail migration]

### sc...@gmail.com (2015-02-04)

Fixed: https://helpx.adobe.com/security/products/flash-player/apsb15-03.html

### cl...@chromium.org (2015-02-04)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-02-17)

Merge NA - went out flash update in M40.

### ti...@google.com (2015-04-09)

Congrats - $7500 for this one as well.

### ti...@google.com (2015-05-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-13)

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

This issue was migrated from crbug.com/chromium/436022?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/437469]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080907)*
