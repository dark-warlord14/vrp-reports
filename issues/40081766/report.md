# Security: Flash: Uninitialized stack variable while parsing an MPD file can corrupt memory

| Field | Value |
|-------|-------|
| **Issue ID** | [40081766](https://issues.chromium.org/issues/40081766) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Reporter** | bi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-03-31 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Loading a weird MPD file can corrupt flash player's memory.

**VERSION**  

Chrome version 41.0.2272.101, Flash 17.0.0.134  

Operating System: Win 7 x64 SP1

**REPRODUCTION CASE**  

I'm ripping most of this from scarybeasts' sources. I'm sure he's ok with that =D.

"To reproduce, host the attached SWF and other files on a web server (e.g. localhost) and load it like this:"

"<http://localhost/PlayManifest.swf?file=gen.mpd>"

"To compile the .as file, I had to use special flags to flex:"

"mxmlc -target-player 14.0 -swf-version 25 -static-link-runtime-shared-libraries ./PlayManifest.as"  

"(This also requires that you have v14.0 of playerglobals.swc installed. Any newer version should also be fine.)"

On Win7 x64 sp1 with Chrome 32 bit, crash like this:  

6AA8B67C | 8B C3 | mov eax,ebx |  

6AA8B67E | E8 A1 05 00 00 | call pepflashplayer.6AA8BC24 |  

6AA8B683 | EB A8 | jmp pepflashplayer.6AA8B62D |  

6AA8B685 | 89 88 D0 00 00 00 | mov dword ptr ds:[eax+D0],ecx | // crash here, eax points somewhere in pepflashplayer.dll  

6AA8B68B | 8B 88 88 00 00 00 | mov ecx,dword ptr ds:[eax+88] |  

6AA8B691 | 33 D2 | xor edx,edx |  

6AA8B693 | 3B CA | cmp ecx,edx |  

6AA8B695 | 74 07 | je pepflashplayer.6AA8B69E |  

6AA8B697 | 39 11 | cmp dword ptr ds:[ecx],edx |  

6AA8B699 | 0F 95 C1 | setne cl |

At first sight this looks to be an uninitialized stack variable but I might be wrong.

## Attachments

- [AVSSUninitStack.zip](attachments/AVSSUninitStack.zip) (application/zip, 9.4 KB)

## Timeline

### sc...@gmail.com (2015-04-01)

Sent to Adobe. P0 deadline tracking at https://code.google.com/p/google-security-research/issues/detail?id=316.

### sc...@gmail.com (2015-04-04)

Adobe id is PSIRT-3543.

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

This issue was migrated from crbug.com/chromium/472201?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081766)*
