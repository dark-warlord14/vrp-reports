# EXTERNAL-REPORT: Windows kernel crash on invalid font

| Field | Value |
|-------|-------|
| **Issue ID** | [40081970](https://issues.chromium.org/issues/40081970) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals |
| **Platforms** | Windows |
| **Reporter** | cp...@google.com |
| **Assignee** | mo...@google.com |
| **Created** | 2010-07-04 |
| **Bounty** | $1,337.00 |

## Description

The following was reported to security@. The attachment has the entire report including example files that were used to cause the crash.

Hi,

when testing my OTF fuzzer, I observed the attached crash case,
which repeatedly  loads an OTF font. !exploitable says it is
exploitable. Reproducer and WinDBG/Exploitable report are attached.

The test machine has XP SP3 installed, and is fully patched (The font
related Windows XP Hotfix KB979559 was also installed).

> First Chance Exception Type: STATUS_ACCESS_VIOLATION (0xC0000005)
> Exception Sub-Type: Write Access Violation
>=20
> Exception Hash (Major/Minor): 0x27171430.0x4d321348
>=20
> Stack Trace:
> chrome_1c30000!OMX_Deinit+0x3610
> chrome_1c30000!OMX_Deinit+0x36b6
> chrome_1c30000!ChromeMain+0xcb265
> chrome_1c30000!ChromeMain+0xcafbc
> chrome_1c30000!ChromeMain+0x1fbcb8
> chrome_1c30000!ChromeMain+0x175e7d
> chrome_1c30000!Hunspell_create_key+0x1078b
> chrome_1c30000!ChromeMain+0x1c27cb
> chrome_1c30000!Hunspell_create_key+0xe1b0
> chrome_1c30000!ChromeMain+0x1e0713
> chrome_1c30000!ChromeMain+0x1e0694
> chrome_1c30000!ChromeMain+0x1ecf5c
> chrome_1c30000!ChromeMain+0x13bd09
> chrome_1c30000!ChromeMain+0x13bb41
> chrome_1c30000!ChromeMain+0x13cbfb
> chrome_1c30000!ChromeMain+0x13bd19
> chrome_1c30000!ChromeMain+0x13bb41
> chrome_1c30000!ChromeMain+0x13cbfb
> chrome_1c30000!ChromeMain+0x13bd19
> chrome_1c30000!ChromeMain+0x13bb41
> chrome_1c30000!ChromeMain+0x13cbfb
> chrome_1c30000!ChromeMain+0x13bd19
> chrome_1c30000!ChromeMain+0x13bb41
> chrome_1c30000!ChromeMain+0xbf9b5
> chrome_1c30000!ChromeMain+0xc14f6
> chrome_1c30000!Hunspell_create_key+0x1d510d
> chrome_1c30000!Hunspell_create_key+0x1d5090
> chrome_1c30000!Hunspell_create_key+0x18612d
> chrome_1c30000!Hunspell_create_key+0x1964e3
> chrome_1c30000!Hunspell_create_key+0x185fd8
> chrome_1c30000!Hunspell_create_key+0x1a0380
> chrome_1c30000!ChromeMain+0x668
> chrome!SetExtensionID+0x1a9a
> chrome!SetExtensionID+0x2120
> chrome!SetExtensionID+0x44c23
> kernel32!RegisterWaitForInputIdle+0x49
> Instruction Address: 0x00000000025c5332
>=20
> Description: User Mode Write AV
> Short Description: WriteAV
> Exploitability Classification: EXPLOITABLE
> Recommended Bug Title: Exploitable - User Mode Write AV starting at chr=
ome_1c30000!OMX_Deinit+0x0000000000003610 (Hash=3D0x27171430.0x4d321348)
>=20
> User mode write access violations that are not near NULL are exploitabl=
e.


Kind regards
Marc Sch=F6nefeld


## Attachments

- [Bug_Report.txt](attachments/Bug_Report.txt) (application/octet-stream, 118.2 KB)
- [AdobeHeitiStd-Regular.otf.38.fuzz-1](attachments/AdobeHeitiStd-Regular.otf.38.fuzz-1) (data, 6.0 MB)
- [38.v.html](attachments/38.v.html) (text/html, 1.9 KB)
- [419___0.000500___HoboStd.html](attachments/419_0.000500_HoboStd.html) (text/html, 1.9 KB)
- [419___0.000500___HoboStd.otf](attachments/419_0.000500_HoboStd.otf) (data, 29.7 KB)
- [38.v.html.chrome.windbg.txt](attachments/38.v.html.chrome.windbg.txt) (text/x-patch, 7.0 KB)
- [AdobeHeitiStd-Regular.otf.38.fuzz-2](attachments/AdobeHeitiStd-Regular.otf.38.fuzz-2) (data, 5.7 MB)
- [HoboStd-Minimal.otf](attachments/HoboStd-Minimal.otf) (data, 29.7 KB)
- [HoboStd-Original.otf](attachments/HoboStd-Original.otf) (data, 29.7 KB)
- [ots_header_offsize_check.patch](attachments/ots_header_offsize_check.patch) (text/plain; charset=us-ascii, 356 B)

## Timeline

### js...@chromium.org (2010-07-04)

Thanks Chris. The faulting address is within the first four pages of address space, so I expect it's just a wide NULL deref. Unfortunately, he didn't configure symbols <http://dev.chromium.org/developers/how-tos/debugging> so the stack trace provided is useless. I don't have a windows box handy to test atm, but after the holiday weekend one of us can definitely see about hacking a repro out of the HTTP stream he provided take a look at it.


### ta...@gmail.com (2010-07-05)

I was curious, but the attached files appear to be incomplete (at least I was unable to decode anything useful out of it, and the data stream appears to be truncated).

Chris, is the problem on our end or his end?

### in...@chromium.org (2010-07-05)

Even I could not reproduce anything with the files in the report. Chris, can we ask the reporter to send us these files in a zip/attach in bug/put testcase on his or her site - 38.v.html, AdobeHeitiStd-Regular.otf.38.fuzz

### cp...@google.com (2010-07-05)

I have asked the reported to send the attachments to us individually
to avoid truncation issues.

### in...@chromium.org (2010-07-08)

@cpb: ping. any update from the researcher ?

### cp...@google.com (2010-07-08)

No reply as of yet. I'll send another email.

### js...@chromium.org (2010-07-08)

Wow, I just realized that I totally misread that crash dump when I looked at it the other day. Please disregard the part in https://crbug.com/chromium/48283#c1 about a NULL deref. I must have confused another bug. But yeah, we don't have enough information to figure out what this is, so if we don't get a response soon we'll have to close it out as invalid.


### ad...@google.com (2010-07-08)

I've pinged the reporter of the issue and asked him to make the attachment available for download. I've also asked if he'd like to be added to the bug. Hopefully he'll get back to us soon.

### ad...@google.com (2010-07-09)

Adding vulnerability reporter (Marc) to cc list. He's currently traveling and doesn't have access to the original attachments. 

### js...@chromium.org (2010-07-11)

[Empty comment from Monorail migration]

### ad...@google.com (2010-07-13)

attachments received from Marc:

"attached are two reproducers, the first is the original reported issue.

38.v.html
38.v.html.chrome.windbg.txt
AdobeHeitiStd-Regular.otf.38.fuzz

The second is a reproducer that causes a broken otf font displayed on
chrome to reboot on windows.

419___0.000500___HoboStd.otf
419___0.000500___HoboStd.html"

### ad...@google.com (2010-07-13)

NOTE: had to split the fuzz attachment across 2 comments (N.B. file is carved into 2 using "split")

### js...@chromium.org (2010-07-13)

Validating now, but this looks like more manifestations of https://crbug.com/chromium/42961. Adam is circling back with MS again to try and get a status update. But if it's the same root problem, then there's likely nothing we can do to address it in Chrome (short of disabling fonts entirely).


### in...@chromium.org (2010-07-13)

Cannot reproduce any crash with the first set of testcases - 38.v.html, combining the two fuzz files on chrome v5 stable and chromium v6 trunk (6.0.464.0 (52148)) on windoes vista. looks like a windows font issue as Justin said in the comments.

### ta...@gmail.com (2010-07-13)

I can reproduce it on XP, it's obviously a serious Microsoft/Adobe bug.

kd> .trap b19c5824
ErrCode = 00000010
eax=00000002 ebx=e1abc910 ecx=e1abc910 edx=e1084830 esi=e10ff534 edi=e10ff500
eip=e2c3f000 esp=b19c5898 ebp=b19c58b8 iopl=0         nv up ei pl nz na po nc
cs=0008  ss=0010  ds=0023  es=0023  fs=0030  gs=0000             efl=00010202
e2c3f000 ??              ???
kd> kv
  *** Stack trace for last set context - .thread/.cxr resets it
ChildEBP RetAddr  Args to Child              
WARNING: Frame IP not in any known module. Following frames may be wrong.
b19c5894 bffb6b32 e10ff534 ff53f000 bffb8240 0xe2c3f000
b19c58b8 bffb85c8 e23279c8 e12784e8 b19c5928 ATMFD+0x16b32
b19c58c8 bffafa44 e1abc910 e12784e8 e1713ba0 ATMFD+0x185c8
b19c5928 bffaa3aa bffaa371 000056fc e12784e8 ATMFD+0xfa44
b19c59a4 bffa4c00 000056fc 00000000 e12784e8 ATMFD+0xa3aa
b19c59dc bffa5e8c ffffffff e1f12890 00000000 ATMFD+0x4c00
b19c5a58 bffa2ecd 00000000 00000000 58000000 ATMFD+0x5e8c
b19c5b40 bf870d13 00000001 e1f12890 b19c5bf0 ATMFD+0x2ecd
b19c5b70 bf870ca1 00000001 e1f12890 b19c5bf0 win32k!PDEVOBJ::LoadFontFile+0x3a (FPO: [7,1,0])
b19c5ba8 bf96526f 00000000 00000000 e1f12890 win32k!vLoadFontFileView+0x12b (FPO: [11,2,4])
b19c5c5c bf9405a3 e1f12890 00000000 00000000 win32k!PUBLIC_PFTOBJ::hLoadMemFonts+0x6a (FPO: [4,29,4])
b19c5cb4 bf94a104 00750000 e2316d58 00000000 win32k!GreAddFontMemResourceEx+0x76 (FPO: [5,15,4])
b19c5d48 8053d658 012ab000 000056fc 00000000 win32k!NtGdiAddFontMemResourceEx+0xb0 (FPO: [Non-Fpo])
b19c5d48 7c90e514 012ab000 000056fc 00000000 nt!KiFastCallEntry+0xf8 (FPO: [0,0] TrapFrame @ b19c5d64)
0012ed68 00000000 00000000 00000000 00000000 ntdll!KiFastSystemCallRet (FPO: [0,0,0])
kd> r
Last set context:
eax=00000002 ebx=e1abc910 ecx=e1abc910 edx=e1084830 esi=e10ff534 edi=e10ff500
eip=e2c3f000 esp=b19c5898 ebp=b19c58b8 iopl=0         nv up ei pl nz na po nc
cs=0008  ss=0010  ds=0023  es=0023  fs=0030  gs=0000             efl=00010202
e2c3f000 ??              ???
kd> lmv m ATMFD
start    end        module name
bffa0000 bffe5c00   ATMFD      (no symbols)           
    Loaded symbol image file: ATMFD.DLL
    Image path: \SystemRoot\System32\ATMFD.DLL
    Image name: ATMFD.DLL
    Timestamp:        Tue Apr 20 07:30:07 2010 (4BCD3BDF)
    CheckSum:         00049B26
    ImageSize:        00045C00
    File version:     5.1.2.228
    Product version:  5.1.2.228
    File flags:       0 (Mask 3F)
    File OS:          40004 NT Win32
    File type:        3.0 Driver
    File date:        00000000.00000000
    Translations:     0409.04b0
    CompanyName:      Adobe Systems Incorporated
    ProductName:      Adobe Type Manager
    InternalName:     ATMFD
    OriginalFilename: ATMFD.DLL
    ProductVersion:   5.1 Build 228
    FileVersion:      5.1 Build 228
    FileDescription:  Windows NT OpenType/Type 1 Font Driver
    LegalCopyright:   ©1983-1990, 1993-2004 Adobe Systems Inc.
    LegalTrademarks:  Acrobat, Adobe, Multiple Master, ATM, Adobe Type Manager,  PostScript and others are Trademarks of Adobe Systems IncorporatedPostscript, and others are Trademarks of Adobe Systems.


### ta...@gmail.com (2010-07-13)

Chris: can you add yusukes@ to cc, Microsoft will not patch this in a reasonable timeframe, we should adjust OTS to protect chrome users.

### js...@chromium.org (2010-07-13)

@tavis - I assume you got that crash is that dump from the HoboStd font and not the AdobeHeitiStd font?

+yusuke


### sc...@gmail.com (2010-07-13)

So, sounds like there's no actual Chrome fault here?
The serious font bug should be reported to Microsoft....

### js...@chromium.org (2010-07-13)

Yeah, it's not a Chrome issue, but MS still hasn't pushed out a fix. So, we're going to revisit the discussion of any protective measures we can take until they resolve it.

### ta...@gmail.com (2010-07-14)

@jschuh Yep, correct, HoboStd.

### yu...@chromium.org (2010-07-14)

I'm looking into 419___0.000500___HoboStd.otf and the original HoboStd.otf font.

Does anyone know which OpenType table is causing the crash? At least 4 tables (CFF, cmap, hhea, and hmtx) seem to be modified. 


### ta...@gmail.com (2010-07-14)

@Yusukes I'll try to narrow it down.

### ta...@gmail.com (2010-07-14)

I found the original font online, here are the bytes that have been modified:

$ cmp -l HoboStd.otf 419___0.000500___HoboStd\(2\).otf 
  312 375 371
  470 142 342
 1067  40 140
 2140   0 100
 2488   2 102
 3947  46  42
 8109 365 345
 8609 237 233
15823  12   2
18989 223 203
21794 370 374
21979   0  20
23818   4   5
27881 375 275
30344 343 341

Patching the original values back in, the only important one is at byte offset 2488.

Here is the original, and a version modified with the minimal error.

### ta...@gmail.com (2010-07-14)

Looks like the error is in parsing the CFF table.

taviso@nopsled:~/Downloads$ showttf -verbose -headers HoboStd-Minimal.otf > 1
Required tables: glyf and loca have been replaced by CFF => OpenType
taviso@nopsled:~/Downloads$ showttf -verbose -headers HoboStd-Original.otf > 2
Required tables: glyf and loca have been replaced by CFF => OpenType
taviso@nopsled:~/Downloads$ diff -u 1 2
--- 1   2010-07-14 15:33:02.000000000 +0200
+++ 2   2010-07-14 15:33:09.000000000 +0200
@@ -1,7 +1,7 @@
 version='OTTO', numtables=13, searchRange=128 entrySel=3 rangeshift=80
-File Checksum =b1b0affa (should be 0xb1b0afba), diff=ffffffc0
+File Checksum =b1b0afba (should be 0xb1b0afba), diff=0
 BASE checksum=3f624fba actual=3f624fba diff=0 offset=25184 len=52
-CFF  checksum=341d921d actual=341d925d diff=40 offset=2484 len=19356
+CFF  checksum=341d921d actual=341d921d diff=0 offset=2484 len=19356
 DSIG checksum=d7ba6d91 actual=d7ba6d91 diff=0 offset=25236 len=5180
 GPOS checksum=09840b69 actual=09840b69 diff=0 offset=23664 len=1518
 GSUB checksum=6de87013 actual=6de87013 diff=0 offset=22852 len=812


### ta...@gmail.com (2010-07-14)

It seems like we can just verify offSize is < 4? We do this for a few others.

### yu...@chromium.org (2010-07-14)

Thanks for the minimal example!

> It seems like we can just verify offSize is < 4?

Yes, I think so (to be precise, <= 4 and > 0). The spec says OffSize should be 1, 2, 3, or 4.
http://www.adobe.com/devnet/font/pdfs/5176.CFF.pdf (section 3, table 2)

The check was missing since it was possible to parse an otf file without the offSize value in the header...
Attached a tentative patch for OTS r30.

I'm currently confirming that the patch does not reject non-malicious fonts.


### yu...@chromium.org (2010-07-14)

> I'm currently confirming that the patch does not reject non-malicious fonts.

All green. I've just uploaded the fix to rietveld. Tavis, could you review it?
http://codereview.chromium.org/2985009

Assuming the patch looks good to you, I have two questions:

1) How and when should we submit the patch to the OTS svn repository? Is it okay to submit the patch immediately with a obscured patch description like "Fix https://crbug.com/chromium/48283"?
2) Along with the patch, could you review http://codereview.chromium.org/2857028 as well? The change should fix a similar security issue (in CFF parser in Freetype.)



### in...@chromium.org (2010-07-14)

Yusuke, I checked your simple patch and it does match what the spec says. So, I did a LGTM.

### js...@chromium.org (2010-07-14)

Yeah, I'd say it's fine to submit the OTS patch now with an innocuous description. I was planning on talking to laforge@ and kerz@ about another security release next week. So, there shouldn't be much lag on the Chrome side.


### ta...@gmail.com (2010-07-14)

LGTM as well.

I think we're really lucky we have OTS and don't have to rely on anyone else to fix this. Thanks Yusuke!

### js...@chromium.org (2010-07-14)

Just talked to kerz@ and we're going to try to cut the next stable refresh tonight so we can get it through QA and release on Monday or Tuesday.


### js...@chromium.org (2010-07-14)

[Empty comment from Monorail migration]

### ag...@chromium.org (2010-07-14)

Landed in OTS: http://code.google.com/p/ots/source/detail?r=31
Rolled into Chrome: r52357

### bu...@gmail.com (2010-07-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=52387 

------------------------------------------------------------------------
r52387 | jschuh@chromium.org | 2010-07-14 13:45:02 -0700 (Wed, 14 Jul 2010) | 6 lines
Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/375/src/DEPS?r1=52387&r2=52386

Rolling OTS deps to pick up fixes.

TBR=jschuh@chromium.org
BUG=48283
TEST=None.
Review URL: http://codereview.chromium.org/2964012
------------------------------------------------------------------------


### js...@chromium.org (2010-07-14)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-07-14)

[Empty comment from Monorail migration]

### sk...@chromium.org (2010-07-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-07-19)

+adammein

### ma...@chromium.org (2010-07-20)

[Empty comment from Monorail migration]

### ta...@gmail.com (2010-07-20)

Bruce, this is the win32k bug I mentioned to you over email. Thanks for taking a look!

### [Deleted User] (2010-07-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2010-07-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-07-21)

@Marc.Schoenefeld: thank you for the report. Although this seems to be purely a Windows kernel bug, we'd like to offer you $1337 under the Chromium Security Reward program! The panel took into account the severity and significance of the bug as well as the fact your useful report has enabled us to protect our users using our font sanitization layer. We'll get this protection out to our users this week and it should help whilst Microsoft address the root cause. (The full details of this bug will be kept private until that time).

### sc...@gmail.com (2010-07-27)

@Marc.Schoenefeld: Chrome users now protected from kernel bug, courtesy of http://googlechromereleases.blogspot.com/2010/07/stable-channel-update_26.html.

Please e-mail me, cevans@chromium.org, to set up payment.

Thanks again.

### sc...@gmail.com (2010-08-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-08-25)

Payment in the electronic system. As this is your first reward, this is the first time we're wiring to you. Keep an eye out to make sure it arrives :)

### js...@chromium.org (2011-01-04)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/48283?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081970)*
