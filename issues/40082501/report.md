# Another Windows kernel bug in the CFF font parser

| Field | Value |
|-------|-------|
| **Issue ID** | [40082501](https://issues.chromium.org/issues/40082501) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals |
| **Reporter** | sc...@gmail.com |
| **Assignee** | yu...@chromium.org |
| **Created** | 2010-08-03 |
| **Bounty** | $1,337.00 |

## Description

Not Chromium's fault again, but maybe we can also defend against this new kernel bug via OTS.

From Yusuke:

---
The BSoD reproduced on my Windows XP laptop (X60) too.

I extracted the malformed font from his html (attached) and checked
which table is causing the crash.  It seems that his font is modified
version of "ヒラギノ明朝 ProN W3.otf" (a Japanese font used in Mac OS X) and
the modified tables are "vmtx" and "CFF."  Probably the latter (CFF)
is the culprit, once again.
...
The OffSize in the font is in the
correct range. I haven't looked in depth yet, but it seems that one of
"subroutine calls" in font hinting code in CFF causes the crash since
Adobe's font analyzer (FDK-2.5) says:

$ wine FDK/Tools/win/tx.exe -dcf ~/extracted.otf
tx.exe: --- /home/yusukes/extracted.otf
tx.exe: invalid subr call
tx.exe: fatal error
...
Font hinting language for CFF is a very simple,
stack-based one similar to Forth. The spec of the language is only ~30
pages of PDF: http://www.microsoft.com/typography/otspec/charstr2.htm
I'll try to write checker code for OTS tomorrow (Aug 4, Tokyo time)
which checks the following:

- checks if the code calls undefined subroutines.
- (if the check above doesn't do the trick,) checks if all subroutines
correctly end with "return" or "endchar" operators.
- (if the check above doesn't do the trick,) checks if the call graph
contains a loop which should cause a stack overflow.
- ...
---

## Attachments

- [extracted.otf.bz2](attachments/extracted.otf.bz2) (application/x-bzip2; charset=binary, 6.2 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### sc...@gmail.com (2010-08-03)

Tavis -- is Bruce still a good contact at Microsoft? Should I cc: him?

### js...@chromium.org (2010-08-03)

[Empty comment from Monorail migration]

### yu...@chromium.org (2010-08-04)

I have almost finished implementing the font hinting language interpreter which could refuse malformed fonts like extracted.otf as well as the otf font which was used to jail break iPhone4.

(just for my own reference) TODOs left are:
- fix handlers for hstem, vstem, roll and hintmask operators.
- write unit tests.
- code cleanup.


### yu...@chromium.org (2010-08-05)

+agl
http://codereview.chromium.org/3023041


### yu...@chromium.org (2010-08-05)

Security team,
If necessary, please report the details of the issue to Microsoft.

The font hinting code in extracted.otf has (at least) 3 problems:

1. CharString #3770 (0-origin): too few argument for the stem operator.
2. CharString #5792: Undefined operator (0x10) is used.
3. CharString #13363: call operator is used even though both Local and Global Subrs (subroutine definitions) are empty.

I guess the third one causes the kernel crash.

Thanks,
Yusuke


### ag...@chromium.org (2010-08-05)

I'm reading the spec now. I'll do the code review immediately afterwards.

### sc...@gmail.com (2010-08-06)

Interesting. This hinting language sounds very powerful. Can we possibly hope to determine whether a given hinting program will e.g. use excessive stack depth, without solving the halting problem?

### bu...@gmail.com (2010-08-06)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55189 

------------------------------------------------------------------------
r55189 | yusukes@chromium.org | 2010-08-05 22:27:40 -0700 (Thu, 05 Aug 2010) | 8 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=55189&r2=55188

OTS DEPS roll to r34.
Support validation of font hinting code (Adobe Type2 Charstring format.)

BUG=51070
TEST=Verified that Chromium renderer does not crash with the exploit HTML on Windows Vista.
TBR=agl

Review URL: http://codereview.chromium.org/3007039
------------------------------------------------------------------------


### yu...@chromium.org (2010-08-06)

I've just submitted a patch (OTS r34) which should protect Windows XP users from malicious font hinting code. I also rolled DEPS for tot Chrome (r55189). Please merge the DEPS change to the stable Chrome if necessary.

> Can we possibly hope to determine whether a given hinting program will e.g. use excessive stack depth, without solving the halting problem?

I believe my OTS change can do it (if not perfect):

// The validation will fail if one of the following conditions is met:
//  1. The code uses more than 48 values of argument stack.
//  2. The code uses deeply nested subroutine calls (more than 10 levels.)
//  3. The code passes invalid number of operands to an operator.
//  4. The code calls an undefined global or local subroutine.
//  5. The code uses one of the following operators that are unlikely used in
//     an ordinary fonts, and could be dangerous: random, put, get, index, roll.

Do the checks above make sense?


### in...@chromium.org (2010-08-06)

Needs to be merged to 472 and 375.

### sc...@gmail.com (2010-08-06)

Ah, I see from the language spec that there is no support for jumping (and therefore looping) so indeed it should be possible to statically determine the max stack depth used by a given routine or subroutine. Excellent.

### ta...@gmail.com (2010-08-06)

Reproduced here as well, another adobe font manager bug.

kd> .cxr
Resetting default scope
kd> .bugcheck
Bugcheck code 00000050
Arguments f000ff8b 00000000 bffd08a7 00000002
kd> kv
ChildEBP RetAddr  Args to Child              
b200b97c 804f7bad 00000003 f000ff8b 00000000 nt!RtlpBreakWithStatusInstruction (FPO: [1,0,0])
b200b9c8 804f879a 00000003 c0603c00 c0780078 nt!KiBugCheckDebugBreak+0x19 (FPO: [Non-Fpo])
b200bda8 804f8cc5 00000050 f000ff8b 00000000 nt!KeBugCheck2+0x574 (FPO: [6,242,4])
b200bdc8 8051cc67 00000050 f000ff8b 00000000 nt!KeBugCheckEx+0x1b (FPO: [5,0,0])
b200be28 80540554 00000000 f000ff8b 00000000 nt!MmAccessFault+0x8e7 (FPO: [4,14,4])
b200be28 bffd08a7 00000000 f000ff8b 00000000 nt!KiTrap0E+0xcc (FPO: [0,0] TrapFrame @ b200be40)
WARNING: Stack unwind information not available. Following frames may be wrong.
b200bedc bffca97e 00000000 00010000 00040000 ATMFD+0x308a7
b200c5bc bffcc0a8 e23d0638 bffd9628 b200c7f0 ATMFD+0x2a97e
b200c674 bffc02e2 e23d0638 bffd9628 b200c7f0 ATMFD+0x2c0a8
b200c754 bffc037f e23d0638 b200c7f0 b200c874 ATMFD+0x202e2
b200c77c bffb18df e23d0638 bffd9628 b200c7f0 ATMFD+0x2037f
b200c8e4 bffb1cca 0000000b b200c9e8 e1279330 ATMFD+0x118df
b200c930 bffa3350 0000000b b200c9e8 00000000 ATMFD+0x11cca
b200c988 bf8434cb e1b61010 e11a6008 00000001 ATMFD+0x3350
b200c9b8 bf8550e5 e1b61010 e11a6008 00000001 win32k!PDEVOBJ::QueryFontData+0x3c (FPO: [7,1,0])
b200ca28 bf83d8e5 e11a622c e13e0afc e1b2d2d8 win32k!xInsertMetricsRFONTOBJ+0x92 (FPO: [3,16,4])
b200ca5c bf8f74b3 00000001 b200ca84 b200ccb0 win32k!RFONTOBJ::bGetGlyphMetrics+0x129 (FPO: [5,5,4])
b200ccf4 bf8f726d 04010327 00000eba 00000001 win32k!GreGetCharWidthW+0x160 (FPO: [6,156,4])
b200cd44 8053d658 04010327 00000eba 00000001 win32k!NtGdiGetCharWidthW+0xe9 (FPO: [Non-Fpo])
b200cd44 7c90e514 04010327 00000eba 00000001 nt!KiFastCallEntry+0xf8 (FPO: [0,0] TrapFrame @ b200cd64)
kd> .trap b200be40
ErrCode = 00000000
eax=10037db6 ebx=00018f56 ecx=00000000 edx=00000000 esi=f000ff53 edi=00050000
eip=bffd08a7 esp=b200beb4 ebp=b200bedc iopl=0         nv up ei pl nz ac po cy
cs=0008  ss=0010  ds=0023  es=0023  fs=0030  gs=0000             efl=00010213
ATMFD+0x308a7:
bffd08a7 8b4e38          mov     ecx,dword ptr [esi+38h] ds:0023:f000ff8b=????????
kd> r @esi
Last set context:
esi=f000ff53

Bruce is probably the right person to ping, can you add him to CC chris?

### ta...@gmail.com (2010-08-06)

@yusukes Sounds fine to me, but #5 sounds like it might break legitimate fonts? Why is random dangerous?

### ta...@gmail.com (2010-08-06)

Ah, I just realised this must be so you can make the analysis deterministic. Oops.

Good idea.

### ta...@gmail.com (2010-08-06)

I just looked at the adobe code, there's a whole bunch of undocumented opcodes, like "blend" and "extendnmbr", it's definitely wise to whitelist the ones we recognise. It's unlikely these undocumented operations have seen much testing.

### in...@chromium.org (2010-08-06)

Looks like this bug might need more changes, so keeping it back to status "Started".

### in...@chromium.org (2010-08-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-06)

cc: Bruce.
Hey Bruce! Another CFF font parsing related Windows kernel bug for you. Distinct from the last one. Tavis believes it to also be exploitable.

### bd...@microsoft.com (2010-08-06)

Thanks for the note Chris. We will investigate this asap.

### sc...@gmail.com (2010-08-06)

Thanks for the awesome bug, Marc! Since it is:
- Distinct from the other one
- Exploitable according to Tavis
- Not our fault but still something we can protect our users from
... we will also reward this at the $1337 level. Congrats!

### yu...@chromium.org (2010-08-09)

> I just looked at the adobe code, there's a whole bunch of undocumented opcodes, like "blend" and "extendnmbr", it's definitely wise to whitelist the ones we recognise. It's unlikely these undocumented operations have seen much testing.

You mean that we should reject fonts that use undocumented operators like blend, correct? If so, OTS r34 is already doing it.

> @yusukes Sounds fine to me, but #5 sounds like it might break legitimate fonts?

In theory, #5 could reject legitimate fonts, but I believe it is okay in practice.
I have checked ~450 CFF fonts, and found that no fonts used the operators (i.e. random, put, get, index, roll.)


### yu...@chromium.org (2010-08-09)

Uploaded http://codereview.chromium.org/3027049 which fixes potential problems in r34 Tavis pointed out.


### yu...@chromium.org (2010-08-10)

OTS r35 is landed, and I have rolled DEPS for tot Chrome (r55537).
http://code.google.com/p/ots/source/detail?r=35
http://src.chromium.org/viewvc/chrome?view=rev&revision=55537

@inferno
I believe all known issues of OTS have been resolved.


### bu...@gmail.com (2010-08-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55537 

------------------------------------------------------------------------
r55537 | yusukes@chromium.org | 2010-08-10 00:13:25 -0700 (Tue, 10 Aug 2010) | 6 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=55537&r2=55536

OTS roll to r35.

BUG=51070
TBR=agl

Review URL: http://codereview.chromium.org/3156001
------------------------------------------------------------------------


### in...@chromium.org (2010-08-11)

Thanks Yusuke for quickly this.

I have rolled DEPS to OTS r35 on both 375 and 472.

Mark, can you please see if DEPS change is picked up on these branches. I think on trunk, it automatically does, but on 375, 472 might need a manual trigger.

### in...@chromium.org (2010-08-11)

Bugdroid is down, so here are the revision numbers - 
http://src.chromium.org/viewvc/chrome?view=rev&revision=55731, http://src.chromium.org/viewvc/chrome?view=rev&revision=55730.

### in...@chromium.org (2010-08-11)

Had a talk with Kerz. He said it should be be automatically picked up in next beta build. 

### bu...@gmail.com (2010-08-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55730 

------------------------------------------------------------------------
r55730 | inferno@chromium.org | 2010-08-11 09:20:50 -0700 (Wed, 11 Aug 2010) | 7 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/472/src/DEPS?r1=55730&r2=55729

Merge 55537 - OTS roll to r35.

BUG=51070

Review URL: http://codereview.chromium.org/3156001

Review URL: http://codereview.chromium.org/3118008
------------------------------------------------------------------------


### bu...@gmail.com (2010-08-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=55731 

------------------------------------------------------------------------
r55731 | inferno@chromium.org | 2010-08-11 09:22:47 -0700 (Wed, 11 Aug 2010) | 7 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/375/src/DEPS?r1=55731&r2=55730

Merge 55537 - OTS roll to r35.

BUG=51070

Review URL: http://codereview.chromium.org/3156001

Review URL: http://codereview.chromium.org/3160005
------------------------------------------------------------------------


### sc...@gmail.com (2010-08-18)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-25)

Payment in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/51070?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082501)*
