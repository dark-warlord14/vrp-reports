# Security: [FG-VD-16-084] Adobe Flash Player Handing MP4 Memory Corruption Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40086090](https://issues.chromium.org/issues/40086090) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Flash |
| **Platforms** | Windows |
| **CVE IDs** | CVE-2017-2984 |
| **Reporter** | ke...@gmail.com |
| **Assignee** | na...@google.com |
| **Created** | 2016-11-26 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

It is a use-after-free vulnerability in MP4 processing. The crash occurs in write AV.

**VERSION**  

Adobe Flash Player 23.0.0.207  

Other versions may be affected too

**REPRODUCTION CASE**  

put LoadMP42.swf and FG-VD-16-084\_PoC.mp4 on a server and load <http://127.0.0.1:8080/LoadMP42.swf?file=FG-VD-16-084_PoC.mp4>  

run the following command line.  

flashplayer\_23\_sa\_207.exe <http://127.0.0.1:8080/LoadMP42.swf?file=FG-VD-16-084_PoC.mp4>

Credits:  

This vulnerability was discovered by Kai Lu of Fortinet's FortiGuard Labs.

## Attachments

- [FG-VD-16-084_PoC.mp4](attachments/FG-VD-16-084_PoC.mp4) (video/mp4, 978.8 KB)
- [LoadMP42.swf](attachments/LoadMP42.swf) (application/octet-stream, 1.0 KB)
- [crashlog1.txt](attachments/crashlog1.txt) (text/plain, 5.4 KB)
- [fuzzed-Fri_Nov_25_00-28-43_2016.mp4](attachments/fuzzed-Fri_Nov_25_00-28-43_2016.mp4) (video/mp4, 415.0 KB)
- [flashplayer_23_sa.7z](attachments/flashplayer_23_sa.7z) (application/octet-stream, 4.4 MB)

## Timeline

### do...@chromium.org (2016-11-27)

Forwarding to natashena@ - looks like this is the version of Flash currently shipping with Chrome 54 stable. Can you take a look please?

[Monorail components: Internals>Plugins>Flash]

### do...@chromium.org (2016-11-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-27)

[Empty comment from Monorail migration]

### na...@google.com (2016-11-28)

I'm still having trouble reproducing this, I have not been able to get the standalone player to crash on Windows 10 64, even with pageheap enabled. Is there any way you could send us a sample that crashes in a specific browser, and provide the browser and OS version it is crashing in? Just so you are aware, the VRP reward amount takes into consideration the quality of the report, including how difficult it is to reproduce, so it is best if you provide us with crashing samples.

### ke...@gmail.com (2016-11-28)

attached is the standalone player version.

### ke...@gmail.com (2016-11-28)

It can be stable to be reproduced via standalone player version under pageheap disabled or enabled on Windows Pro 10 x64 and Windows 7 x64. 
The crash info is shown below with pageheap enabled.
(1194.b28): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for FlashPlayer.exe - 
eax=1b130ea0 ebx=00000000 ecx=0bde9000 edx=1b4c0027 esi=1b130ea0 edi=1b131fb4
eip=00d982b8 esp=1be7f724 ebp=1be7f740 iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210206
FlashPlayer!WinMainSandboxed+0x2e92bf:
00d982b8 668911          mov     word ptr [ecx],dx        ds:002b:0bde9000=????
0:023> !heap -p -a ecx
    address 0bde9000 found in
    _DPH_HEAP_ROOT @ 66d1000
    in free-ed allocation (  DPH_HEAP_BLOCK:         VirtAddr         VirtSize)
                                    f663924:          bde8000             4000
    682a9e42 verifier!AVrfDebugPageHeapFree+0x000000c2
    77e7f44e ntdll!RtlDebugFreeHeap+0x0000003c
    77de8bcd ntdll!RtlpFreeHeap+0x00000d3d
    77de79ca ntdll!RtlFreeHeap+0x000000ba
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\WINDOWS\SysWoW64\igd10iumd32.dll - 
    64134e88 igd10iumd32+0x00004e88
    6471fbd9 igd10iumd32!OpenAdapter10_2+0x005e1ad9
    6414ebcf igd10iumd32!OpenAdapter10_2+0x00010acf
    6414ec2c igd10iumd32!OpenAdapter10_2+0x00010b2c
    641acc2d igd10iumd32!OpenAdapter10_2+0x0006eb2d
    641a372a igd10iumd32!OpenAdapter10_2+0x0006562a
    69676640 d3d11!TCLSWrappers<CBuffer>::CLSDestroy+0x00000080
    69669e0c d3d11!CLayeredObjectWithCLS<CBuffer>::Release+0x0000002c
    6966a262 d3d11!NDXGI::CDeviceChild<IDXGIResource1,IDXGISwapChainInternal>::FinalRelease+0x00000089
    696408db d3d11!CLayeredObjectWithCLS<CShaderResourceView>::CContainedObject::Release+0x0000057b
    696318e6 d3d11!CDecodeBuffer::`scalar deleting destructor'+0x0000002b
    69631b77 d3d11!CDecodeContext::FinalRelease+0x00000023
    696254e2 d3d11!CLayeredObjectWithCLS<CAuthenticatedChannel>::CFinalReleaseSentinel::~CFinalReleaseSentinel+0x00000028
    69639caa d3d11!CLayeredObjectWithCLS<CDecodeContext>::~CLayeredObjectWithCLS<CDecodeContext>+0x00000040
    69639c2d d3d11!CLayeredObjectWithCLS<CDecodeContext>::`vector deleting destructor'+0x0000000d
    69639c5f d3d11!CLayeredObjectWithCLS<CDecodeContext>::Release+0x0000000f
    6963f4c2 d3d11!CUseCountedObject<NOutermost::CDeviceChild>::Release+0x00000582
    69625017 d3d11!CLayeredObject<CClassLinkage>::CContainedObject::Release+0x00000027
    00d99a97 FlashPlayer!WinMainSandboxed+0x002eaa9e
    00d9ad35 FlashPlayer!WinMainSandboxed+0x002ebd3c
    00d943fc FlashPlayer!WinMainSandboxed+0x002e5403
    01055685 FlashPlayer!IAEModule_AEModule_PutKernel+0x0009ae55
    01054cca FlashPlayer!IAEModule_AEModule_PutKernel+0x0009a49a
    0104f4ef FlashPlayer!IAEModule_AEModule_PutKernel+0x00094cbf
    00fc5858 FlashPlayer!IAEModule_AEModule_PutKernel+0x0000b028
    00fc6473 FlashPlayer!IAEModule_AEModule_PutKernel+0x0000bc43
    00dbc096 FlashPlayer!WinMainSandboxed+0x0030d09d
    00dbdacb FlashPlayer!WinMainSandboxed+0x0030ead2

 
0:023> kb
 # ChildEBP RetAddr  Args to Child              
WARNING: Stack unwind information not available. Following frames may be wrong.
00 1be7f740 00d9a90a 1b4c0368 00000000 1bb0efd0 FlashPlayer!WinMainSandboxed+0x2e92bf
01 1be7f758 00d94478 00000005 0104f73d 1b130ea4 FlashPlayer!WinMainSandboxed+0x2eb911
02 1be7f854 00fc5858 1bfc0580 1bfc0540 1bfc0540 FlashPlayer!WinMainSandboxed+0x2e547f
03 1be7f868 00fc6473 1bfc0540 58c6cbf8 00000004 FlashPlayer!IAEModule_AEModule_PutKernel+0xb028
04 1be7f8a4 00dbc096 1bb0efd0 1b29ab29 000015d1 FlashPlayer!IAEModule_AEModule_PutKernel+0xbc43
05 1be7f8c4 00dbdacb 000004d8 1b29aa29 000015d1 FlashPlayer!WinMainSandboxed+0x30d09d
06 1be7f8fc 00dbb985 1c9e8fd0 00000001 1c9e8fd0 FlashPlayer!WinMainSandboxed+0x30ead2
07 1be7f91c 00dbbacc 1c9e8fd0 1c9e8fd0 1b4bade8 FlashPlayer!WinMainSandboxed+0x30c98c
08 1be7f934 00ce883b 1c9e8fd0 00000001 77a978e0 FlashPlayer!WinMainSandboxed+0x30cad3
09 00000000 00000000 00000000 00000000 00000000 FlashPlayer!WinMainSandboxed+0x239842
0:023> lmvm FlashPlayer
Browse full module list
start    end        module name
00a90000 019ba000   FlashPlayer   (export symbols)       E:\fuzz\flash\fuzzer\flashplayer_23_sa.exe
    Loaded symbol image file: E:\fuzz\flash\fuzzer\flashplayer_23_sa.exe
    Image path: FlashPlayer.exe
    Image name: FlashPlayer.exe
    Browse all global symbols  functions  data
    Timestamp:        Tue Oct 25 17:25:38 2016 (580FF802)
    CheckSum:         00E3E877
    ImageSize:        00F2A000
    File version:     23.0.0.207
    Product version:  23.0.0.207
    File flags:       0 (Mask 3F)
    File OS:          4 Unknown Win32
    File type:        2.0 Dll
    File date:        00000000.00000000
    Translations:     0409.04b0
    CompanyName:      Adobe Systems, Inc.
    ProductName:      Shockwave Flash
    InternalName:     Adobe Flash Player 23.0
    OriginalFilename: SAFlashPlayer.exe
    ProductVersion:   23,0,0,207
    FileVersion:      23,0,0,207
    FileDescription:  Adobe Flash Player 23.0 r0
    LegalCopyright:   Adobe® Flash® Player. Copyright © 1996-2016 Adobe Systems Incorporated. All Rights Reserved. Adobe and Flash are either trademarks or registered trademarks in the United States and/or other countries.
    LegalTrademarks:  Adobe Flash Player


### ke...@gmail.com (2016-11-28)

The crash info is shown below with pageheap disabled.
(e6c.e28): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=0cab800a ebx=04d6bb9c ecx=00000000 edx=00000000 esi=04d6b1e8 edi=00000070
eip=00d9a24b esp=0c51f83c ebp=0c51f850 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210246
FlashPlayer!WinMainSandboxed+0x2eb252:
00d9a24b 0178fa          add     dword ptr [eax-6],edi ds:002b:0cab8004=????????
0:024> kb
 # ChildEBP RetAddr  Args to Child              
WARNING: Stack unwind information not available. Following frames may be wrong.
00 0c51f850 00d9a90a 04e8e8c8 00000000 06a62008 FlashPlayer!WinMainSandboxed+0x2eb252
01 0c51f868 00d94478 00000005 0104f73d 04d6b1ec FlashPlayer!WinMainSandboxed+0x2eb911
02 0c51f964 00fc5858 0c66f060 0c66f020 0c66f020 FlashPlayer!WinMainSandboxed+0x2e547f
03 0c51f978 00fc6473 0c66f020 b2dee7c7 00000004 FlashPlayer!IAEModule_AEModule_PutKernel+0xb028
04 0c51f9b4 00dbc096 06a62008 06b2bbd9 000015d1 FlashPlayer!IAEModule_AEModule_PutKernel+0xbc43
05 0c51f9d4 00dbdacb 000004d8 06b2bad9 000015d1 FlashPlayer!WinMainSandboxed+0x30d09d
06 0c51fa0c 00dbb985 04e90d10 00000001 04e90d10 FlashPlayer!WinMainSandboxed+0x30ead2
07 0c51fa2c 00dbbacc 04e90d10 04e90d10 04e62700 FlashPlayer!WinMainSandboxed+0x30c98c
08 0c51fa44 00ce883b 04e90d10 00000001 77a978e0 FlashPlayer!WinMainSandboxed+0x30cad3
09 00000000 00000000 00000000 00000000 00000000 FlashPlayer!WinMainSandboxed+0x239842
0:024> lmvm FlashPlayer
Browse full module list
start    end        module name
00a90000 019ba000   FlashPlayer   (export symbols)       E:\fuzz\flash\fuzzer\flashplayer_23_sa.exe
    Loaded symbol image file: E:\fuzz\flash\fuzzer\flashplayer_23_sa.exe
    Image path: FlashPlayer.exe
    Image name: FlashPlayer.exe
    Browse all global symbols  functions  data
    Timestamp:        Tue Oct 25 17:25:38 2016 (580FF802)
    CheckSum:         00E3E877
    ImageSize:        00F2A000
    File version:     23.0.0.207
    Product version:  23.0.0.207
    File flags:       0 (Mask 3F)
    File OS:          4 Unknown Win32
    File type:        2.0 Dll
    File date:        00000000.00000000
    Translations:     0409.04b0
    CompanyName:      Adobe Systems, Inc.
    ProductName:      Shockwave Flash
    InternalName:     Adobe Flash Player 23.0
    OriginalFilename: SAFlashPlayer.exe
    ProductVersion:   23,0,0,207
    FileVersion:      23,0,0,207
    FileDescription:  Adobe Flash Player 23.0 r0
    LegalCopyright:   Adobe® Flash® Player. Copyright © 1996-2016 Adobe Systems Incorporated. All Rights Reserved. Adobe and Flash are either trademarks or registered trademarks in the United States and/or other countries.
    LegalTrademarks:  Adobe Flash Player


### ke...@gmail.com (2016-11-28)

I also tested these cases and they can be reproduced stably all in other browsers, such as IE, Firefox on Windows 10 Pro x64 and Windows 7 x64. I'm not sure why it's hard to reproduce in Chrome.  At least, it can be reproduced via standalone player version and other popular browsers(IE, Firefox) from my test results. I need more time to investigate the reason why it's hard to reproduce in Chrome. Please let me know if any issue related to reproduce it with standalone player version.

### ke...@gmail.com (2016-11-28)

I understand what you said about the criterion of VRP reward. I try my best to provide more details to you.
Please first forward it to Adobe for further investigation.  
Glad to hear feedback from you.
Thanks!

Regards,
Kevin

### na...@google.com (2016-11-30)

This is PSIRT-6068.

### sh...@chromium.org (2016-12-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-01-26)

[Empty comment from Monorail migration]

### na...@google.com (2017-02-13)

This was fixed as CVE-2017-2984 

### na...@google.com (2017-02-13)

This was fixed as CVE-2017-2984.

### aw...@chromium.org (2017-02-13)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-02-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-16)

The older reward-topanel https://crbug.com/chromium/664395 has been merged into this one. Please manually review this issue to see if the duplicate is potentially eligible for a reward.



### sh...@chromium.org (2017-02-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-02-18)

$500 for this one!

### aw...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-02-19)

Your change meets the bar and is auto-approved for M57. Please go ahead and merge the CL to branch 2987 manually. Please contact milestone owner if you have questions.
Owners: amineer@(clank), cmasso@(bling), ketakid@(cros), govind@(desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2017-02-20)

No merge needed.

### aw...@google.com (2017-03-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-05-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-05-25)

This issue was migrated from crbug.com/chromium/668830?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/664395]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40086090)*
