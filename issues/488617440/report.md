# Browser Process Heap-Use-After-Free in Digital Credentials API (Renderer → Browser Memory Corruption)

| Field | Value |
|-------|-------|
| **Issue ID** | [488617440](https://issues.chromium.org/issues/488617440) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Identity>DigitalCredentials |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | wo...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2026-02-28 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

Browser Process Heap-Use-After-Free in Digital Credentials API (Renderer → Browser Memory Corruption)

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

content/browser/webid/digital\_credentials/cross\_device\_transaction\_impl.cc

---

### The problem

#### Please describe the technical details of the vulnerability

# Summary

A Heap Use-After-Free vulnerability exists in the **Browser Process** within the Digital Credentials implementation.

A regression changed error callback execution from asynchronous to synchronous. This allows a `TransactionImpl` object to be destroyed while a background worker thread is still executing inside its context.

This results in:

- Cross-thread lifetime violation
- Use-after-free write in Browser Process memory
- Deterministic heap corruption
- Renderer → Browser security boundary violation

The crash is reproducible and confirmed in ASAN-instrumented Chromium builds.

---

# Affected Component

```
content/browser/webid/digital_credentials/

```

Specifically:

```
cross_device_transaction_impl.cc

```

Tested Version:

```
141.0.7369.0 (Windows x64)

```

---

# Vulnerability Type

- Heap Use-After-Free
- Cross-thread object lifetime violation
- Browser Process memory corruption

---

# Root Cause Analysis

In `cross_device_transaction_impl.cc`, error handling previously dispatched callbacks asynchronously via `PostTask`.

The regression changed this to synchronous execution:

```
// Vulnerable pattern
std::move(callback_).Run(base::unexpected(error));

```
## Lifetime Sequence

1. `callback_` is owned by `DigitalIdentityRequestImpl`
2. Synchronous `.Run()` immediately triggers parent cleanup
3. Cleanup calls `provider_.reset()`
4. `provider_` owns `TransactionImpl`
5. `TransactionImpl` is destroyed
6. Background worker thread is still executing inside `TransactionImpl`
7. Worker resumes execution on freed memory

This creates a classic cross-thread Use-After-Free condition in the Browser Process.

---

# Technical Evidence

## ASAN Crash

```
this is the current crash report "
KEY_VALUES_STRING: 1

    Key  : Analysis.CPU.mSec
    Value: 1484

    Key  : Analysis.Elapsed.mSec
    Value: 7383

    Key  : Analysis.IO.Other.Mb
    Value: 0

    Key  : Analysis.IO.Read.Mb
    Value: 1

    Key  : Analysis.IO.Write.Mb
    Value: 0

    Key  : Analysis.Init.CPU.mSec
    Value: 1218

    Key  : Analysis.Init.Elapsed.mSec
    Value: 6072

    Key  : Analysis.Memory.CommitPeak.Mb
    Value: 2001

    Key  : Analysis.Version.DbgEng
    Value: 10.0.29507.1001

    Key  : Analysis.Version.Description
    Value: 10.2511.5.1 amd64fre

    Key  : Analysis.Version.Ext
    Value: 1.2511.5.1

    Key  : Failure.Bucket
    Value: APPLICATION_FAULT_AVRF_517a7ed_chrome_elf.dll!Unknown

    Key  : Failure.Exception.Code
    Value: 0x517a7ed

    Key  : Failure.Exception.IP.Address
    Value: 0x7ffdd1f5de62

    Key  : Failure.Exception.IP.Module
    Value: chrome_elf

    Key  : Failure.Exception.IP.Offset
    Value: 0x1ade62

    Key  : Failure.Hash
    Value: {83d3484b-61a5-7688-5a33-ec9bb1799d38}

    Key  : Failure.ProblemClass.Primary
    Value: APPLICATION_FAULT

    Key  : Faulting.IP.Type
    Value: Paged

    Key  : Timeline.Process.Start.DeltaSec
    Value: 250

    Key  : WER.Process.Version
    Value: 141.0.7369.0


FILE_IN_CAB:  3479e8e4-5242-4370-96e4-baa39fd3a88f.dmp

NTGLOBALFLAG:  2000000

APPLICATION_VERIFIER_LOADED: 1

CONTEXT:  (.ecxr)
rax=000002193723fdbc rbx=00000095be5ff340 rcx=00000095be5fede0
rdx=0000000000000004 rsi=0000000000000000 rdi=00000012b7cbfdb8
rip=00007ffdd1f5de62 rsp=00000095be5feda0 rbp=00000095be5ff370
 r8=0000000000000096  r9=00000000000000a0 r10=00007ffe7a400000
r11=00007ffe7a4ed775 r12=000002067f580000 r13=00000095be5fedc0
r14=00000095be5fede0 r15=000002193723fdbc
iopl=0         nv up ei pl nz na pe nc
cs=0033  ss=0000  ds=0000  es=0000  fs=0053  gs=002b             efl=00000202
chrome_elf!GetHandleVerifier+0xdd672:
00007ffd`d1f5de62 4c89f1          mov     rcx,r14
Resetting default scope

EXCEPTION_RECORD:  (.exr -1)
ExceptionAddress: 00007ffdd1f5de62 (chrome_elf!GetHandleVerifier+0x00000000000dd672)
   ExceptionCode: 0517a7ed
  ExceptionFlags: 00000000
NumberParameters: 0

PROCESS_NAME:  chrome.exe

ERROR_CODE: (NTSTATUS) 0x517a7ed - <Unable to get error code text>

EXCEPTION_CODE_STR:  517a7ed

STACK_TEXT:  
00000095`be5feda0 00007ffd`57be5cbc     : 00000000`45e0360e 00000095`be5ff560 00000095`be5ff5b0 00000000`00000001 : chrome_elf!GetHandleVerifier+0xdd672
00000095`be5ff3c0 00007ffd`5797a7e0     : 00000095`be5ff640 00001214`7f954c80 00000000`00000000 00007ffd`57924382 : chrome!GetHandleVerifier+0x3655dc
00000095`be5ff600 00007ffd`5797d5c4     : 00000000`00000000 00000095`be5ff980 00000095`be5ffa10 00000000`00000000 : chrome!GetHandleVerifier+0xfa100
00000095`be5ff720 00007ffd`5797a5c4     : 00000095`be5ff900 00007ffd`446b34b2 00000095`be5ffb60 00000000`0000000b : chrome!GetHandleVerifier+0xfcee4
00000095`be5ffa70 00007ffd`5797a219     : 00000000`00000000 00000095`be5ffb60 00000095`be5ffbe0 00000206`7f580000 : chrome!GetHandleVerifier+0xf9ee4
00000095`be5ffae0 00007ffd`5796c160     : 00000000`00000000 00000000`00000000 00000000`00000246 00007ffd`57964e8f : chrome!GetHandleVerifier+0xf9b39
00000095`be5ffc40 00007ffd`578a55b4     : 00000000`00000000 00000000`00000000 00000000`00000002 00000000`00000000 : chrome!GetHandleVerifier+0xeba80
00000095`be5ffd20 00007ffd`ccdbb18d     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome!GetHandleVerifier+0x24ed4
00000095`be5ffe30 00007ffe`7b53e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : clang_rt_asan_dynamic_x86_64!_asan_wrap_CreateThread+0x14d
00000095`be5ffe70 00007ffe`7d2ac40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : KERNEL32!BaseThreadInitThunk+0x17
00000095`be5ffea0 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c


STACK_COMMAND: ~3s; .ecxr ; kb

IP_IN_PAGED_CODE: 
chrome_elf!GetHandleVerifier+dd672
00007ffd`d1f5de62 4c89f1          mov     rcx,r14

SYMBOL_NAME:  chrome_elf+1ade62

MODULE_NAME: chrome_elf

IMAGE_NAME:  chrome_elf.dll

FAILURE_BUCKET_ID:  APPLICATION_FAULT_AVRF_517a7ed_chrome_elf.dll!Unknown

OSPLATFORM_TYPE:  x64

OSNAME:  Windows 10

IMAGE_VERSION:  141.0.7369.0

FAILURE_ID_HASH:  {83d3484b-61a5-7688-5a33-ec9bb1799d38}

Followup:     MachineOwner
---------"

```

Exception:

```
ExceptionCode: 0x517a7ed (ASAN security trap)
Process: chrome.exe (Browser Process)
Thread: Background worker thread

```

Register state at crash:

```
rax = 000002193723fdbc
r15 = 000002193723fdbc

```

Previously observed faulting instruction:

```
mov qword ptr [r13+r15], rax

```

This indicates:

- Attacker-influenced value written
- Write target derived from freed object memory
- ASAN confirms the region was already freed and poisoned

Subsequent crash observed in:

```
chrome_elf!GetHandleVerifier
clang_rt_asan_dynamic_x86_64

```

This is consistent with allocator metadata corruption caused by a UAF write.

---

# Security Boundary Impact

- Triggered from renderer context
- Corrupts memory in privileged Browser Process
- Violates renderer sandbox boundary

This qualifies as:

Renderer → Browser Process memory corruption.

Browser-process UAF vulnerabilities are considered high severity because they affect privileged code execution context.

---

# Reproduction Steps

1. I used win32-release\_x64-media\_asan-win32-release\_x64-1504065.
2. Launch chromium from chromium folder with this flag `chrome.exe --enable-features=FedCmDigitalIdentity`
3. Load the attached `poc.html`.
4. Ensure Bluetooth is enabled.
5. Trigger the Digital Credentials request.
6. Immediately disable Bluetooth.
7. Observe crash in Browser Process (not renderer).

The crash is reproducible and deterministic under ASAN.

---

# Exploitability Discussion

The vulnerability provides:

- Use-after-free write primitive
- Occurs in privileged Browser Process
- Reachable from web content

# Suggested Fix

Restore asynchronous dispatch of the error callback:

```
base::SingleThreadTaskRunner::GetCurrentDefault()->PostTask(
    FROM_HERE,
    base::BindOnce(std::move(callback_), base::unexpected(error))
);

```

This ensures:

- `TransactionImpl` destructor runs after stack unwinds
- Worker thread cannot resume inside freed object
- Object lifetime semantics are preserved

#### Impact analysis

# Impact

- Memory Corruption: Yes
- Use-After-Free: Yes
- Browser Process: Yes
- Renderer → Browser Boundary: Yes
- Remote Triggerable: Yes

This represents high-severity memory corruption in a privileged process.

---

### The cause

#### What version of Chrome have you found the security issue in?

chromium 141.0.7369.0, chrome Version 145.0.7632.117 (Official Build) (64-bit)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

sean wong

## Attachments

- [screen-capture.webm](attachments/screen-capture.webm) (video/webm, 4.9 MB)
- [poc.html](attachments/poc.html) (text/html, 1.7 KB)
- [poc.html](attachments/poc_73858834.html) (text/html, 1.7 KB)
- [chrome.exe_260310_215228.dmp](attachments/chrome.exe_260310_215228.dmp) (application/octet-stream, 678.0 MB)

## Timeline

### wo...@gmail.com (2026-02-28)

Hello,

I am providing additional technical analysis of the previously reported Browser Process Heap Use-After-Free in `cross_device_transaction_impl.cc`.

Further debugging has clarified the nature of the write primitive and its behavior under ASAN vs release builds.

---

# Key New Finding: Stale Field Used as Write Offset

During analysis of the faulting instruction:

```
mov qword ptr [r13+r15], rax

```

The following register state was observed at the time of crash:

```
r13 = 000000ff`a41fe9c0
r15 = f8f8f8f8`f8f8f8f8

```

Under ASAN, `0xF8` is a poison pattern indicating partially addressable redzone memory.

This demonstrates that:

1. `TransactionImpl` is freed
2. ASAN poisons the object memory
3. A member field inside the freed object is later read
4. That stale field value becomes `0xf8f8f8f8f8f8f8f8`
5. The poisoned value is used as an offset in pointer arithmetic
6. A write occurs to `[r13 + r15]`

This confirms the vulnerability is not merely a stale write to a fixed offset, but:

> UAF → stale member read → pointer arithmetic → write

In other words, a freed object field is being interpreted as an offset and used to compute the write target.

---

### wo...@gmail.com (2026-03-01)

```
0:003> !peb
PEB at 00000095badaf000
    InheritedAddressSpace:    No
    ReadImageFileExecOptions: No
    BeingDebugged:            No
    ImageBaseAddress:         00007ff6b95b0000
    NtGlobalFlag:             2000000
    NtGlobalFlag2:            0
    Ldr                       00007ffe7d3f2960
    Ldr.Initialized:          Yes
    Ldr.InInitializationOrderModuleList: 000002067cfa9ee0 . 0000020614116ee0
    Ldr.InLoadOrderModuleList:           000002067cfafec0 . 0000020614116ec0
    Ldr.InMemoryOrderModuleList:         000002067cfafed0 . 0000020614116ed0
                    Base TimeStamp                     Module
            7ff6b95b0000 688eecd0 Aug 03 08:00:00 2025 C:\Users\Forever Young\Downloads\win32-release_x64-media_asan-win32-release_x64-1504065\chrome.exe
            7ffe7d220000 c140bef4 Sep 28 02:51:16 2072 C:\WINDOWS\SYSTEM32\ntdll.dll
            7ffe5c060000 55c2884c Aug 06 01:03:56 2015 C:\WINDOWS\System32\verifier.dll
            7ffe7b510000 9db26d02 Nov 02 20:10:26 2053 C:\WINDOWS\System32\KERNEL32.DLL
            7ffe7a7a0000 ad803701 Mar 29 15:30:57 2062 C:\WINDOWS\System32\KERNELBASE.dll
            7ffdd1db0000 688eecd0 Aug 03 08:00:00 2025 C:\Users\Forever Young\Downloads\win32-release_x64-media_asan-win32-release_x64-1504065\chrome_elf.dll
            7ffdccd60000 6892b602 Aug 06 04:55:14 2025 C:\Users\Forever Young\Downloads\win32-release_x64-media_asan-win32-release_x64-1504065\clang_rt.asan_dynamic-x86_64.dll
            7ffe73cf0000 879cd5a0 Feb 05 11:41:04 2042 C:\WINDOWS\SYSTEM32\VERSION.dll
            7ffe7a400000 53a0792e Jun 17 20:21:50 2014 C:\WINDOWS\System32\ucrtbase.dll
            7ffe53100000 0f259d81 Jan 20 08:49:53 1978 C:\Users\Forever Young\Downloads\win32-release_x64-media_asan-win32-release_x64-1504065\VCRUNTIME140.dll
            7ffe7afc0000 f9219683 Jun 14 14:33:23 2102 C:\WINDOWS\System32\msvcrt.dll
            7ffe7a6c0000 22f85f7a Aug 04 15:58:34 1988 C:\WINDOWS\System32\bcryptprimitives.dll
            7ffe7b600000 1b8feb86 Aug 27 04:06:14 1984 C:\WINDOWS\System32\ADVAPI32.dll
            7ffe7c330000 c869a2d5 Jul 19 09:36:05 2076 C:\WINDOWS\System32\sechost.dll
            7ffe7d030000 1ed1ac1c May 21 14:06:04 1986 C:\WINDOWS\System32\RPCRT4.dll
            7ffe78980000 d67cda44 Jan 12 12:09:24 2084 C:\WINDOWS\system32\ntmarta.dll
            7ffd446b0000 688eecd0 Aug 03 08:00:00 2025 C:\Users\Forever Young\Downloads\win32-release_x64-media_asan-win32-release_x64-1504065\chrome.dll
            7ffe7d150000 e86b4016 Jul 25 09:47:50 2093 C:\WINDOWS\System32\WS2_32.dll
            7ffe7acd0000 071e4ac4 Oct 14 08:48:52 1973 C:\WINDOWS\System32\CRYPT32.dll
            7ffe7c1d0000 e31ffeda Oct 01 10:08:10 2090 C:\WINDOWS\System32\OLEAUT32.dll
            7ffe7af10000 80e99dbf Jul 15 11:05:19 2038 C:\WINDOWS\System32\msvcp_win.dll
             206025a0000 37e3d68e Sep 18 21:14:38 1999 C:\WINDOWS\System32\combase.dll
            7ffe7a370000 b437c2db Oct 23 22:54:03 2065 C:\WINDOWS\System32\WINTRUST.dll
            7ffe5a710000 d3e9bb42 Aug 30 13:13:22 2082 C:\WINDOWS\SYSTEM32\WINMM.dll
            7ffdccb10000 bd9e9c2a Oct 23 14:14:50 2070 C:\Users\Forever Young\Downloads\win32-release_x64-media_asan-win32-release_x64-1504065\dbghelp.dll
            7ffe78260000 ae263655 Aug 02 13:24:21 2062 C:\WINDOWS\SYSTEM32\IPHLPAPI.DLL
            7ffe78e60000 943a18ef Oct 20 22:37:19 2048 C:\WINDOWS\SYSTEM32\USERENV.dll
            7ffe77390000 b7644d3b Jul 02 06:44:59 2067 C:\WINDOWS\SYSTEM32\Secur32.dll
            7ffe729a0000 4a08bbbf May 12 02:58:55 2009 C:\WINDOWS\SYSTEM32\WINHTTP.dll
            7ffe75e20000 c9ff9b0d May 23 08:03:09 2077 C:\WINDOWS\SYSTEM32\DWrite.dll
            7ffe6f830000 c27d72eb May 26 08:15:23 2073 C:\WINDOWS\SYSTEM32\dhcpcsvc.DLL
            7ffe4a150000 6ec24c5f Nov 19 09:14:55 2028 C:\WINDOWS\SYSTEM32\WINSPOOL.DRV
            7ffe7c5c0000 8ef148ee Dec 29 19:25:18 2045 C:\WINDOWS\System32\shcore.dll
            7ffe79670000 fc9efc62 Apr 22 06:22:10 2104 C:\WINDOWS\SYSTEM32\cfgmgr32.dll
            7ffe796f0000 936fa18b May 20 08:50:03 2048 C:\WINDOWS\SYSTEM32\DPAPI.DLL
            7ffe78b00000 50bfa101 Dec 05 22:31:13 2012 C:\WINDOWS\SYSTEM32\SSPICLI.DLL
            7ffe79200000 f976bbbd Aug 18 04:34:53 2102 C:\WINDOWS\SYSTEM32\MSASN1.dll
            7ffe7c3f0000 645b9193 May 10 15:44:03 2023 C:\WINDOWS\System32\USER32.dll
            7ffe7a770000 79be856a Sep 22 12:12:10 2034 C:\WINDOWS\System32\win32u.dll
            7ffe7be20000 cae0e442 Nov 10 05:15:30 2077 C:\WINDOWS\System32\GDI32.dll
            7ffe7aba0000 58eae450 Apr 10 04:48:00 2017 C:\WINDOWS\System32\gdi32full.dll
            7ffe7cee0000 fd9b075c Oct 30 10:40:12 2104 C:\WINDOWS\System32\IMM32.DLL
            7ffe775d0000 c62c55af May 11 12:58:07 2075 C:\WINDOWS\system32\uxtheme.dll
            7ffe78e20000 0aa05cb6 Aug 26 13:40:54 1975 C:\WINDOWS\SYSTEM32\gpapi.dll
            7ffe7c0d0000 b5a94432 Jul 31 05:32:18 2066 C:\WINDOWS\System32\SHLWAPI.dll
            7ffe79b00000 8a0d14c2 May 24 23:44:50 2043 C:\WINDOWS\System32\Windows.Storage.dll
            7ffe73cd0000 490c7e58 Nov 01 19:05:44 2008 C:\WINDOWS\System32\wkscli.dll
            7ffe78250000 339bbf08 Jun 09 11:30:00 1997 C:\WINDOWS\System32\netutils.dll
            7ffe7bf60000 f021df0c Aug 31 04:40:28 2097 C:\WINDOWS\System32\MSCTF.dll
            7ffe78860000 33df25bd Jul 30 14:30:05 1997 C:\WINDOWS\SYSTEM32\kernel.appcore.dll
            7ffe7cd40000 2bc0c26f Apr 06 02:36:15 1993 C:\WINDOWS\System32\ole32.dll
            7ffe79960000 aa6357b3 Aug 02 04:53:55 2060 C:\WINDOWS\SYSTEM32\powrprof.dll
            7ffe79940000 66301530 Apr 30 00:46:24 2024 C:\WINDOWS\SYSTEM32\UMPDC.dll
            7ffe5a450000 f40145dc Sep 22 04:35:24 2099 C:\WINDOWS\WinSxS\amd64_microsoft.windows.common-controls_6595b64144ccf1df_6.0.26100.7824_none_3e0870b2e3345462\COMCTL32.dll
            7ffe79a20000 11c7d492 Jun 15 18:32:34 1979 C:\WINDOWS\System32\profapi.dll
            7ffe79000000 55b03939 Jul 23 03:45:45 2015 C:\WINDOWS\SYSTEM32\CRYPTBASE.dll
            7ffe48b50000 528b0819 Nov 19 09:41:29 2013 C:\WINDOWS\system32\nlansp_c.dll
            7ffe7c6c0000 e04cd3a5 Mar 31 21:15:01 2089 C:\WINDOWS\System32\NSI.dll
            7ffe6f860000 8e2b67f4 Aug 01 17:08:52 2045 C:\WINDOWS\SYSTEM32\dhcpcsvc6.DLL
            7ffe782f0000 aa6cb661 Aug 09 07:28:17 2060 C:\WINDOWS\SYSTEM32\DNSAPI.dll
            7ffe7b070000 96c6ee6e Feb 28 03:06:06 2050 C:\WINDOWS\System32\clbcatq.dll
            7ffe5da20000 8738d8e2 Nov 21 15:28:18 2041 C:\WINDOWS\SYSTEM32\textinputframework.dll
            7ffe7b6c0000 1a9bfd2a Feb 24 03:28:26 1984 C:\WINDOWS\System32\SHELL32.dll
            7ffe7a550000 abccf8d6 May 03 12:09:42 2061 C:\WINDOWS\System32\wintypes.dll
            7ffe5d2c0000 32a3a3ee Dec 03 06:52:14 1996 C:\Windows\System32\Windows.UI.dll
            7ffe773a0000 a91c916a Nov 28 08:08:58 2059 C:\WINDOWS\SYSTEM32\WTSAPI32.dll
            7ffe79700000 c98f1d89 Feb 27 00:13:45 2077 C:\WINDOWS\SYSTEM32\WINSTA.dll
            7ffe74f90000 ae05e5db Jul 09 01:08:27 2062 C:\WINDOWS\SYSTEM32\mscms.dll
            7ffe7c8b0000 e7d89ca8 Apr 05 04:19:36 2093 C:\WINDOWS\System32\SETUPAPI.dll
            7ffe79640000 75668c59 Jun 01 01:21:13 2032 C:\WINDOWS\SYSTEM32\DEVOBJ.dll
            7ffe6b000000 cb8c6422 Mar 20 07:18:42 2078 C:\WINDOWS\System32\MMDevApi.dll
            7ffe4f810000 27969da8 Jan 18 10:03:04 1991 C:\Windows\System32\CapabilityAccessManagerClient.dll
            7ffe69420000 482bfa9d May 15 11:55:57 2008 C:\Windows\System32\usermgrproxy.dll
            7ffe67100000 e8a288a0 Sep 05 08:12:00 2093 C:\WINDOWS\SYSTEM32\usermgrcli.dll
            7ffe5ac60000 e29ffac5 Jun 26 07:40:37 2090 C:\Windows\System32\wpnapps.dll
            7ffe681c0000 d143c6a4 Apr 03 07:25:08 2081 C:\Windows\System32\OneCoreUAPCommonProxyStub.dll
            7ffe780c0000 867fea67 Jul 04 08:53:43 2041 C:\Windows\System32\FirewallAPI.dll
            7ffe78030000 8cf449f4 Dec 08 17:25:56 2044 C:\Windows\System32\fwbase.dll
            7ffe5db70000 bc14473c Dec 28 11:39:24 2069 C:\Windows\System32\FWPolicyIOMgr.dll
            7ffe5cdb0000 b08e318e Nov 12 19:00:14 2063 C:\Windows\System32\InputHost.dll
            7ffe76fb0000 7a37641c Dec 23 04:34:20 2034 C:\Windows\System32\CoreMessaging.dll
            7ffe753c0000 b6a58783 Feb 07 13:50:43 2067 C:\WINDOWS\SYSTEM32\PROPSYS.dll
            7ffe778a0000 ac436cdb Aug 01 08:32:11 2061 C:\WINDOWS\SYSTEM32\dwmapi.dll
            7ffe4bbd0000 0941eab3 Dec 03 18:01:07 1974 C:\WINDOWS\system32\twinapi.dll
            7ffe5f230000 5b18bf5b Jun 07 08:15:07 2018 C:\WINDOWS\system32\XmlLite.dll
            7ffe67e30000 8546c7d3 Nov 08 20:26:43 2040 C:\Windows\System32\Windows.UI.Immersive.dll
            7ffe542c0000 a45e1959 May 21 03:24:57 2057 C:\WINDOWS\system32\dataexchange.dll
            7ffe68a10000 3470d29c Nov 18 02:26:20 1997 C:\WINDOWS\system32\twinapi.appcore.dll
            7ffe46bd0000 9e6a77d4 Mar 22 10:33:40 2054 C:\Windows\System32\Windows.Media.dll
            7ffe74da0000 59eac02d Oct 21 06:34:05 2017 C:\WINDOWS\SYSTEM32\atlthunk.dll
            7ffe52d50000 e6c151fa Sep 05 07:58:34 2092 C:\WINDOWS\SYSTEM32\OLEACC.dll
            7ffe69530000 e92ce8d9 Dec 19 07:15:21 2093 C:\WINDOWS\system32\directmanipulation.dll
            7ffe73f40000 6bb00d29 Apr 03 00:03:37 2027 C:\WINDOWS\SYSTEM32\CoreUIComponents.dll
            7ffe3d2d0000 b43454f3 Oct 21 08:28:19 2065 C:\WINDOWS\system32\explorerframe.dll
            7ffe50b70000 e5f2bc6b Apr 01 15:13:31 2092 C:\Windows\System32\Windows.System.Launcher.dll
            7ffe65840000 5469ffb8 Nov 17 17:01:28 2014 C:\WINDOWS\SYSTEM32\windows.staterepositorycore.dll
            7ffe791a0000 bac98ccb Apr 21 14:55:55 2069 C:\WINDOWS\System32\CRYPTSP.dll
            7ffe787c0000 67f6d4e8 Apr 09 23:13:28 2025 C:\WINDOWS\system32\rsaenh.dll
            7ffe4cdd0000 41d7fb2f Jan 02 16:46:23 2005 C:\Windows\System32\Windows.Networking.Connectivity.dll
            7ffe6b710000 01020286 Jul 15 19:55:34 1970 C:\WINDOWS\System32\npmproxy.dll
            7ffe6f750000 738983f4 Jun 05 05:14:12 2031 C:\WINDOWS\SYSTEM32\wlanapi.dll
            7ffe6f800000 1af143ac Apr 28 19:51:56 1984 C:\WINDOWS\SYSTEM32\MobileNetworking.dll
            7ffe53ac0000 e1d7b6c2 Jan 25 09:57:06 2090 C:\WINDOWS\SYSTEM32\pdh.dll
            7ffe75270000 f763bc6f Jul 11 10:04:15 2101 C:\WINDOWS\System32\netprofm.dll
            7ffe6a970000 1f312046 Aug 01 23:47:02 1986 C:\Windows\System32\Windows.FileExplorer.Common.dll
            7ffe48e20000 9b59a91f Aug 04 03:34:39 2052 C:\Windows\System32\CryptoWinRT.dll
            7ffe60000000 f1609771 Apr 29 22:48:01 2098 C:\Windows\System32\cryptngc.dll
            7ffe79300000 115a0e23 Mar 24 12:08:51 1979 C:\WINDOWS\SYSTEM32\ncrypt.dll
            7ffe792b0000 9f05a157 Jul 18 03:12:07 2054 C:\WINDOWS\SYSTEM32\NTASN1.dll
            7ffe799f0000 3c0ad1d3 Dec 03 04:13:55 2001 C:\WINDOWS\SYSTEM32\bcrypt.dll
            7ffe69760000 c75ca2bb Dec 28 08:35:55 2075 C:\WINDOWS\system32\ngcksp.dll
            7ffe5d420000 4e65e4a5 Sep 06 12:15:17 2011 C:\WINDOWS\system32\PCPKsp.dll
            7ffe60690000 61c88ea9 Dec 26 18:47:53 2021 C:\WINDOWS\SYSTEM32\tbs.dll
            7ffe5aac0000 1dfc92f2 Dec 10 22:45:54 1985 C:\WINDOWS\system32\ncryptprov.dll
            7ffe75be0000 5b66cdb4 Aug 05 13:13:08 2018 C:\WINDOWS\SYSTEM32\WindowsCodecs.dll
            7ffe5b680000 be09470a Jan 12 12:04:10 2071 C:\WINDOWS\SYSTEM32\TextShaping.dll
            7ffe4dd90000 769d6f7e Jan 22 20:53:02 2033 C:\WINDOWS\SYSTEM32\UIAutomationCore.DLL
            7ffe60bd0000 8dca6be3 May 20 03:35:47 2045 C:\Windows\System32\BitsProxy.dll
            7ffe3ddf0000 4e44dca4 Aug 12 10:56:20 2011 C:\Windows\System32\Windows.Devices.Bluetooth.dll
            7ffe640b0000 d5168588 Apr 15 16:56:24 2083 C:\Windows\System32\Windows.Devices.Enumeration.dll
            7ffe6b4e0000 90b2a7e0 Dec 05 15:58:08 2046 C:\Windows\System32\Windows.Devices.Radios.dll
            7ffe603d0000 1ab035da Mar 10 11:35:38 1984 C:\Windows\System32\DevDispItemProvider.dll
            7ffe5ff80000 621adc12 Feb 27 05:04:02 2022 C:\Windows\System32\DDORes.dll
            7ffe6aab0000 f153ed70 Apr 20 08:15:28 2098 C:\Windows\System32\DefaultDeviceManager.dll
            7ffe69b80000 35bf8b95 Jul 29 23:52:37 1998 C:\WINDOWS\system32\BthRadioMedia.dll
    SubSystemData:     00007ffe68c2ad20
    ProcessHeap:       000002067ce50000
    ProcessParameters: 000002067cfa17f0
    CurrentDirectory:  'C:\Users\Forever Young\Downloads\win32-release_x64-media_asan-win32-release_x64-1504065\'
    WindowTitle:  'chrome.exe   --enable-features=FedCmDigitalIdentity'
    ImageFile:    'C:\Users\Forever Young\Downloads\win32-release_x64-media_asan-win32-release_x64-1504065\chrome.exe'
    CommandLine:  'chrome.exe   --enable-features=FedCmDigitalIdentity'
    DllPath:      '< Name not readable >'
    Environment:  000002067d636fa0
        =::=::\
        =C:=C:\Users\Forever Young\Downloads\win32-release_x64-media_asan-win32-release_x64-1504065
        =ExitCode=00000000
        ALLUSERSPROFILE=C:\ProgramData
        APPDATA=C:\Users\Forever Young\AppData\Roaming
        ASAN_OPTIONS=quarantine_size_mb=256:symbolize=1:print_stacktrace=1:debug=1
        CHROME_CRASHPAD_PIPE_NAME=\\.\pipe\crashpad_67180_RJXYJKBEOCUFFITZ
        CommonProgramFiles=C:\Program Files\Common Files
        CommonProgramFiles(x86)=C:\Program Files (x86)\Common Files
        CommonProgramW6432=C:\Program Files\Common Files
        COMPUTERNAME=YEEZOH
        ComSpec=C:\WINDOWS\system32\cmd.exe
        DriverData=C:\Windows\System32\Drivers\DriverData
        EFC_81788_1262719628=1
        EFC_81788_1592913036=1
        EFC_81788_2283032206=1
        EFC_81788_2775293581=1
        EFC_81788_3789132940=1
        FPS_BROWSER_APP_PROFILE_STRING=Internet Explorer
        FPS_BROWSER_USER_PROFILE_STRING=Default
        HOMEDRIVE=C:
        HOMEPATH=\Users\Forever Young
        LOCALAPPDATA=C:\Users\Forever Young\AppData\Local
        LOGONSERVER=\\YEEZOH
        NUMBER_OF_PROCESSORS=8
        OneDrive=C:\Users\Forever Young\OneDrive
        OS=Windows_NT
        Path=C:\Program Files\FireDaemon OpenSSL 3\bin\;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\Program Files\dotnet\;C:\Users\Forever Young\AppData\Local\Programs\Python\Launcher\;C:\Users\Forever Young\AppData\Local\Microsoft\WindowsApps;
        PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
        PROCESSOR_ARCHITECTURE=AMD64
        PROCESSOR_IDENTIFIER=Intel64 Family 6 Model 142 Stepping 10, GenuineIntel
        PROCESSOR_LEVEL=6
        PROCESSOR_REVISION=8e0a
        ProgramData=C:\ProgramData
        ProgramFiles=C:\Program Files
        ProgramFiles(x86)=C:\Program Files (x86)
        ProgramW6432=C:\Program Files
        PROMPT=$P$G
        PSModulePath=C:\Program Files\WindowsPowerShell\Modules;C:\WINDOWS\system32\WindowsPowerShell\v1.0\Modules
        PUBLIC=C:\Users\Public
        SESSIONNAME=Console
        SystemDrive=C:
        SystemRoot=C:\WINDOWS
        TEMP=C:\Users\FOREVE~1\AppData\Local\Temp
        TMP=C:\Users\FOREVE~1\AppData\Local\Temp
        USERDOMAIN=YEEZOH
        USERDOMAIN_ROAMINGPROFILE=YEEZOH
        USERNAME=Forever Young
        USERPROFILE=C:\Users\Forever Young
        windir=C:\WINDOWS
        ZES_ENABLE_SYSMAN=1

```

### wo...@gmail.com (2026-03-03)

hello

### wo...@gmail.com (2026-03-04)

anyone here?

### me...@google.com (2026-03-05)

Thanks for the report.

mamir@: I haven't been able to repro, but could you please take a look?

### me...@google.com (2026-03-05)

Tentatively marking as S0 since it's a UAF in the browser process. If it requires a user interaction like in the repro steps, then we should bump it down to P1.

### ch...@google.com (2026-03-05)

Setting milestone because of s0/s1 severity.

### ma...@chromium.org (2026-03-05)

This bug has been already fixed in <https://crrev.com/c/7143479> (and the fix has rolled out in Chrome 143)

### wo...@gmail.com (2026-03-06)

Hello, I opened the Poc.html in chrome 145, followed the same reproduction steps and chrome freezes/crashes immediately after I toggle off Bluetooth. Please check. Thank you.

### ma...@chromium.org (2026-03-06)

Thank you for the follow-up!
Alright!
I will take a look on the poc.html and report back!

### wo...@gmail.com (2026-03-07)

Hello, did you manage to check the poc.html?

### wo...@gmail.com (2026-03-10)

Hello @matt, did you manage to check the poc in chrome?

### ma...@chromium.org (2026-03-10)

I have checked, and it indeed crashes when turning off bluetooth in the middle of a DC API.
It isn't specific to this poc.html, but for any DC API call.

I a looking into this and I will report back when I find the underlying cause!

Thank you for reporting this bug!

### wo...@gmail.com (2026-03-10)

Hello @matt,

Following up on my previous message regarding the freeze/crash when Bluetooth is disabled during a Digital Credentials API request, You mentioned that " it indeed crashes when turning off bluetooth in the middle of a DC API. It isn't specific to this poc.html, but for any DC API call." so i decided to check the root cause. I performed additional debugging to capture a hang dump and analyze the behavior.

### Environment

- Chrome Version: 145.0.7632.160 (Official Build) (64-bit)
- OS: Windows 10 (10.0.26100.1)
- Trigger: Disable Bluetooth while a Digital Credentials request is active

### Methodology

Since the browser freezes instead of producing a standard crash report, I used **ProcDump** to capture a hang dump while the browser was unresponsive.

Command used:

```
procdump -ma -h <chrome_browser_pid>

```

This captures a full memory dump (`-ma`) when a process becomes unresponsive (`-h`).

ProcDump successfully captured the dump at the moment the browser hung:

```
chrome.exe_260310_215228.dmp

```
### Observed Behavior

When the Digital Credentials request is triggered and Bluetooth is disabled mid-transaction:

1. Chrome becomes completely unresponsive.
2. No crash dialog appears.
3. The browser must be terminated manually.

ProcDump detected the hang and captured the dump.

### Stack Analysis

The browser main thread (`CrBrowserMain`) is blocked attempting to unregister a Bluetooth radio listener:

```
ntdll!RtlEnterCriticalSection
BthRadioMedia!ATL::IConnectionPointImpl::Unadvise
BthRadioMedia!CBthRadioManager::Unadvise
Windows_Devices_Radios!RadioEventListener::UnregisterListener
Windows_Devices_Radios!RadioEventListener::remove_StateChanged
Windows_Devices_Radios!RadioImpl::remove_StateChanged

```

At the same time, another thread is processing the Bluetooth state change event:

```
Windows_Devices_Radios!RadioEventListener::OnInstanceRadioChange
BthRadioMedia!CBthRadioManager::InvokeOnInstanceChange
BthRadioMedia!CBthRadioManager::InvokeAllNotifications
ntdll!TppWorkpExecuteCallback

```
### Root Cause (Based on Dump Analysis)

The hang appears to be caused by a **lock contention / deadlock** in the Bluetooth radio event notification system:

- The notification thread handles the Bluetooth state change event and holds the internal critical section while invoking callbacks.
- Simultaneously, the browser main thread attempts to unregister the radio state listener as part of cleanup when Bluetooth is disabled during the Digital Credentials flow.
- Because the notification thread still holds the same critical section, the main thread blocks indefinitely in `CBthRadioManager::Unadvise`.

Simplified sequence:

```
Digital Credentials request starts
        ↓
Bluetooth discovery active
        ↓
Bluetooth disabled
        ↓
Windows fires radio state change event
        ↓
Thread A: processes notification (holds lock)
Thread B: tries to unregister listener (needs same lock)
        ↓
Deadlock / hang

```
### Key Dump Indicators

The hang dump shows:

```
Failure.Bucket:
BREAKPOINT_AVRF_80000003_BthRadioMedia.dll!ATL::IConnectionPointImpl::Unadvise

```

and the browser main thread waiting on:

```
ntdll!RtlEnterCriticalSection

```

while another thread executes:

```
RadioEventListener::OnInstanceRadioChange

```

which suggests the deadlock occurs during radio state change notification handling.

### Attached Evidence

I have attached the ProcDump hang dump captured during the freeze:

```
chrome.exe_260310_215228.dmp

```
### Exception Analysis

```

KEY_VALUES_STRING: 1

    Key  : Analysis.CPU.mSec
    Value: 3718

    Key  : Analysis.Elapsed.mSec
    Value: 27120

    Key  : Analysis.IO.Other.Mb
    Value: 0

    Key  : Analysis.IO.Read.Mb
    Value: 1

    Key  : Analysis.IO.Write.Mb
    Value: 6

    Key  : Analysis.Init.CPU.mSec
    Value: 500

    Key  : Analysis.Init.Elapsed.mSec
    Value: 3347

    Key  : Analysis.Memory.CommitPeak.Mb
    Value: 322

    Key  : Analysis.Version.DbgEng
    Value: 10.0.29507.1001

    Key  : Analysis.Version.Description
    Value: 10.2511.5.1 amd64fre

    Key  : Analysis.Version.Ext
    Value: 1.2511.5.1

    Key  : Failure.Bucket
    Value: BREAKPOINT_AVRF_80000003_BthRadioMedia.dll!ATL::IConnectionPointImpl_CBthRadioManager,_IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray_::Unadvise

    Key  : Failure.Exception.Code
    Value: 0x80000003

    Key  : Failure.Hash
    Value: {7b36ca12-0843-c0cf-196f-60867978625f}

    Key  : Failure.ProblemClass.Primary
    Value: BREAKPOINT

    Key  : Faulting.IP.Type
    Value: Null

    Key  : Timeline.OS.Boot.DeltaSec
    Value: 698999

    Key  : Timeline.Process.Start.DeltaSec
    Value: 261

    Key  : WER.OS.Branch
    Value: ge_release

    Key  : WER.OS.Version
    Value: 10.0.26100.1

    Key  : WER.Process.Version
    Value: 145.0.7632.160


FILE_IN_CAB:  chrome.exe_260310_215228.dmp

COMMENT:  
*** procdump  -ma -h 66144
*** Hung window detected: 140aa0

NTGLOBALFLAG:  2000000

APPLICATION_VERIFIER_FLAGS:  0

APPLICATION_VERIFIER_LOADED: 1

EXCEPTION_RECORD:  (.exr -1)
ExceptionAddress: 0000000000000000
   ExceptionCode: 80000003 (Break instruction exception)
  ExceptionFlags: 00000000
NumberParameters: 0

FAULTING_THREAD:  13b68

PROCESS_NAME:  chrome.exe

ERROR_CODE: (NTSTATUS) 0x80000003 - {EXCEPTION}  Breakpoint  A breakpoint has been reached.

EXCEPTION_CODE_STR:  80000003

CRITICAL_SECTION:  00000000000007d0 -- (!cs -s 00000000000007d0)

BLOCKING_THREAD:  0

STACK_TEXT:  
00000017`89ffcbe8 00007ffd`7216af5f     : ffffffff`ffffffff 00000000`00000000 00000300`00000556 efefefef`efefef00 : ntdll!NtWaitForAlertByThreadId+0x14
00000017`89ffcbf0 00007ffd`7216c5ff     : 00000000`00000000 00000000`00000000 00007ffd`498cc000 00000000`000007d0 : ntdll!RtlpWaitOnCriticalSection+0x58f
00000017`89ffccf0 00007ffd`7216d872     : 000001ac`c5e29f10 000001ac`a4310001 00000017`89ffce00 00007ffc`93fa142a : ntdll!RtlpEnterCriticalSectionContended+0x1ef
00000017`89ffcd70 00007ffd`498b7746     : 000001ac`c5e29ee8 00000b3c`0150ee70 00000017`89ffce40 000001ac`baefcf70 : ntdll!RtlEnterCriticalSection+0xf2
00000017`89ffcdb0 00007ffd`498b7635     : 000001ac`c5e29ee8 00000000`00000001 00007ffd`498cc048 00000000`00000001 : BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Unadvise+0x36
00000017`89ffcde0 00007ffd`66d289fc     : 00000b3c`04520500 00000000`00000000 000001ac`baefcf70 00000b3c`01e877c0 : BthRadioMedia!CBthRadioManager::Unadvise+0x55
00000017`89ffce20 00007ffd`66d28c2b     : 000001ac`baf5cfc0 00000000`00000000 000001ac`baf5cfc0 00007ffc`96d5e528 : Windows_Devices_Radios!RadioEventListener::UnregisterListener+0x64
00000017`89ffce60 00007ffd`66d2bb22     : 00000000`00000000 00000000`00000000 00000b3c`01d1ed80 00000b3c`016bd200 : Windows_Devices_Radios!RadioEventListener::remove_StateChanged+0x6b
00000017`89ffcea0 00007ffc`9dceee19     : 00000b3c`02a5f4c0 00000b3c`02a5ec80 00007ffc`a21b42f8 00000b3c`02a5ec80 : Windows_Devices_Radios!RadioImpl::remove_StateChanged+0x12
00000017`89ffced0 00007ffc`9dceeb12     : 7fffffff`ffffffff 00007ffc`96d5e528 00000119`a1c74000 00000000`00000001 : chrome!sqlite3_dbdata_init+0xe70289
00000017`89ffd060 00007ffc`9dcf6010     : 00000000`00000001 00000b3c`02c9bcc0 00000b3c`01e87700 00000b3c`01e877c0 : chrome!sqlite3_dbdata_init+0xe6ff82
00000017`89ffd210 00007ffc`9e060753     : 000001ac`a67f9380 00000b3c`01d1ed80 00000000`00000001 00000b3c`01d1ed80 : chrome!sqlite3_dbdata_init+0xe77480
00000017`89ffd250 00007ffc`9e063d30     : 00000000`00000001 00000b3c`009ddf90 00000b3c`009ddf90 00000b38`00019378 : chrome!sqlite3_dbdata_init+0x11e1bc3
00000017`89ffd2e0 00007ffc`9a7986b0     : 00000b3c`017046b0 00000b38`00019378 000001ac`a67f9380 00000b3c`0150ee70 : chrome!sqlite3_dbdata_init+0x11e51a0
00000017`89ffd320 00007ffc`9a79a421     : 00000b3c`04520500 00007ffc`96e3ab3b 00000b3c`0265cd80 00000b3c`0066d780 : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc77b20
00000017`89ffd350 00007ffc`9c5841fc     : 00000000`00000008 00000017`89ffd550 00000b3c`01d1ede0 00007ffc`983d4eaf : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc79891
00000017`89ffd390 00007ffc`9c586af0     : 00000b3c`01d1ed80 00007ffc`977d34a9 000001ac`a67f9380 00000b3c`046ce2a8 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a6366c
00000017`89ffd3d0 00007ffc`9a3eb996     : 00000017`89ffd458 00000017`89ffd4f0 00000b3c`00129738 00007ffc`93e28919 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a65f60
00000017`89ffd410 00007ffc`9a3eb8ce     : 00000000`00000000 00000000`00000000 00000000`00000000 00007ffc`a2d96fb0 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x8cae06
00000017`89ffd530 00007ffc`9a3ee109     : 00005d6e`6a213742 00000017`89ffd658 00000b38`00051140 00007ffc`9c1d4e99 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x8cad3e
00000017`89ffd5f0 00007ffc`9a3ee025     : 00007ffc`a1576a78 00007ffc`a0cc2b0c 00007ffc`a17715e0 00000b3c`025d7c00 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x8cd579
00000017`89ffd6b0 00007ffc`9a798d4f     : 00000b3c`0150ee70 00000b3c`0429cd00 00000000`00000001 00000b3c`0429cc80 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x8cd495
00000017`89ffd6f0 00007ffc`9c58556b     : 00000000`00000006 00000000`00000000 00000000`00000000 00000017`89ffd6c8 : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc781bf
00000017`89ffd740 00007ffc`9c58495a     : 00000000`00000001 00000000`00000033 00000000`00000050 00000b38`00019378 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a649db
00000017`89ffd7e0 00007ffc`9c586cc5     : 80000000`00000050 00000008`00000085 00000000`00000002 00000b3c`04520580 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a63dca
00000017`89ffd8a0 00007ffc`9a798d4f     : 00000000`00000001 00000b3c`04520300 00000000`00000033 80000000`00000038 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a66135
00000017`89ffd940 00007ffc`9a79a6e2     : 00007ffc`a23e736c 00000017`89ffdc10 00000000`00000001 00000000`00000013 : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc781bf
00000017`89ffd990 00007ffc`9dd076b5     : 00000b3c`0198c0e8 000000a2`c0899414 00000000`00000000 00000b3c`016bd200 : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc79b52
00000017`89ffdb50 00007ffc`9a90d0d2     : 00000b38`000c8a88 00000000`00000068 00000b38`00473f58 00000b38`00019378 : chrome!sqlite3_dbdata_init+0xe88b25
00000017`89ffdd20 00007ffc`96a67411     : 00000b38`00019208 00007ffd`721b01a9 00007ffc`93c07da6 00007ffc`93c0794c : chrome!CrashForExceptionInNonABICompliantCodeRange+0xdec542
00000017`89ffdd60 00007ffc`976d351d     : 00000017`89ffe580 00000000`00400000 00000b38`000b80a0 00000b3c`0167c7a0 : chrome!IsSandboxedProcess+0x78ee11
00000017`89ffe550 00007ffc`933efa1d     : 00000017`89ffe6f0 00000017`89ffe7e0 00000000`00000001 00000001`00e3ab3b : chrome!IsSandboxedProcess+0x13faf1d
00000017`89ffe650 00007ffc`97d07d9b     : 00000017`89ffeaa0 00000b38`000192a8 00000000`00000000 00007ffc`96e3ab3b : chrome+0x5fa1d
00000017`89ffe6c0 00007ffc`941053fe     : 00000017`89ffeaa0 00000017`89ffeaa0 00000000`00000000 00007ffc`96e3ab3b : chrome!IsSandboxedProcess+0x1a2f79b
00000017`89ffe760 00007ffc`93c07da6     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`0000009a : chrome!ChromeMain+0x54611e
00000017`89ffe840 00007ffc`93c0794c     : 00000000`7bd05a00 00000000`ffffffff 00000000`00000018 00000b3c`00004300 : chrome!ChromeMain+0x48ac6
00000017`89ffe8b0 00007ffc`93c06586     : 00000017`89ffe9b0 00000b38`00098000 00000000`7bd05a00 00007ffd`7225183d : chrome!ChromeMain+0x4866c
00000017`89ffe970 00007ffc`93bc1a8c     : 00000000`00000000 00000000`00000000 00000000`00000000 00005d6e`6a210b82 : chrome!ChromeMain+0x472a6
00000017`89ffeb70 00007ffc`93bc1151     : 00000017`89ffef01 00007ffc`a19c4535 00000863`7bd05a00 00000b38`0004c338 : chrome!ChromeMain+0x27ac
00000017`89ffece0 00007ffc`93bbf604     : 00007ff7`7be90000 00000b38`000501b0 00000017`89fff120 00000000`00000000 : chrome!ChromeMain+0x1e71
00000017`89ffee00 00007ff7`7beb3c78     : 00007050`000642b0 00007ffc`93bbf2e0 00000017`89fff100 00000000`00000000 : chrome!ChromeMain+0x324
00000017`89fff0c0 00007ff7`7beb1ca4     : 00000017`89fff410 00000017`89fff410 00000000`00000000 00000017`89fff558 : chrome_exe+0x23c78
00000017`89fff350 00007ff7`7bfec242     : 00007ff7`7c0cf600 00007ff7`7bfec2b9 00000000`00000000 00000000`00000000 : chrome_exe+0x21ca4
00000017`89fff750 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!IsSandboxedProcess+0xb63e2
00000017`89fff790 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
00000017`89fff7c0 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c


STACK_COMMAND: ~0s; .ecxr ; kb

SYMBOL_NAME:  BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Unadvise+36

MODULE_NAME: BthRadioMedia

IMAGE_NAME:  BthRadioMedia.dll

FAILURE_BUCKET_ID:  BREAKPOINT_AVRF_80000003_BthRadioMedia.dll!ATL::IConnectionPointImpl_CBthRadioManager,_IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray_::Unadvise

OS_VERSION:  10.0.26100.1

BUILDLAB_STR:  ge_release

OSPLATFORM_TYPE:  x64

OSNAME:  Windows 10

IMAGE_VERSION:  6.2.26100.7309

FAILURE_ID_HASH:  {7b36ca12-0843-c0cf-196f-60867978625f}

Followup:     MachineOwner
---------

0:000> !cs -l
-----------------------------------------
DebugInfo          = 0x000001acc5e2bfd0
Critical section   = 0x000001acc5e29f98 (+0x1ACC5E29F98)
LOCKED
LockCount          = 0x0
WaiterWoken        = No
OwningThread       = 0x000000000001208c
RecursionCount     = 0x1
LockSemaphore      = 0x0
SpinCount          = 0x00000000020007d0
-----------------------------------------
DebugInfo          = 0x000001acc5e2ffd0
Critical section   = 0x000001acc5e29f10 (+0x1ACC5E29F10)
LOCKED
LockCount          = 0x1
WaiterWoken        = No
OwningThread       = 0x000000000001208c
RecursionCount     = 0x1
LockSemaphore      = 0xFFFFFFFF
SpinCount          = 0x00000000020007d0
-----------------------------------------
DebugInfo          = 0x000001acb87f1fd0
Critical section   = 0x000001acbaefcfd0 (+0x1ACBAEFCFD0)
LOCKED
LockCount          = 0x0
WaiterWoken        = No
OwningThread       = 0x0000000000013b68
RecursionCount     = 0x1
LockSemaphore      = 0x0
SpinCount          = 0x00000000020007d0
0:000> ~* kb

.  0  Id: 10260.13b68 Suspend: 0 Teb: 00000017`897ef000 Unfrozen "CrBrowserMain"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`7216af5f     : ffffffff`ffffffff 00000000`00000000 00000300`00000556 efefefef`efefef00 : ntdll!NtWaitForAlertByThreadId+0x14
01 00007ffd`7216c5ff     : 00000000`00000000 00000000`00000000 00007ffd`498cc000 00000000`000007d0 : ntdll!RtlpWaitOnCriticalSection+0x58f
02 00007ffd`7216d872     : 000001ac`c5e29f10 000001ac`a4310001 00000017`89ffce00 00007ffc`93fa142a : ntdll!RtlpEnterCriticalSectionContended+0x1ef
03 00007ffd`498b7746     : 000001ac`c5e29ee8 00000b3c`0150ee70 00000017`89ffce40 000001ac`baefcf70 : ntdll!RtlEnterCriticalSection+0xf2
04 00007ffd`498b7635     : 000001ac`c5e29ee8 00000000`00000001 00007ffd`498cc048 00000000`00000001 : BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Unadvise+0x36
05 00007ffd`66d289fc     : 00000b3c`04520500 00000000`00000000 000001ac`baefcf70 00000b3c`01e877c0 : BthRadioMedia!CBthRadioManager::Unadvise+0x55
06 00007ffd`66d28c2b     : 000001ac`baf5cfc0 00000000`00000000 000001ac`baf5cfc0 00007ffc`96d5e528 : Windows_Devices_Radios!RadioEventListener::UnregisterListener+0x64
07 00007ffd`66d2bb22     : 00000000`00000000 00000000`00000000 00000b3c`01d1ed80 00000b3c`016bd200 : Windows_Devices_Radios!RadioEventListener::remove_StateChanged+0x6b
08 00007ffc`9dceee19     : 00000b3c`02a5f4c0 00000b3c`02a5ec80 00007ffc`a21b42f8 00000b3c`02a5ec80 : Windows_Devices_Radios!RadioImpl::remove_StateChanged+0x12
09 00007ffc`9dceeb12     : 7fffffff`ffffffff 00007ffc`96d5e528 00000119`a1c74000 00000000`00000001 : chrome!sqlite3_dbdata_init+0xe70289
0a 00007ffc`9dcf6010     : 00000000`00000001 00000b3c`02c9bcc0 00000b3c`01e87700 00000b3c`01e877c0 : chrome!sqlite3_dbdata_init+0xe6ff82
0b 00007ffc`9e060753     : 000001ac`a67f9380 00000b3c`01d1ed80 00000000`00000001 00000b3c`01d1ed80 : chrome!sqlite3_dbdata_init+0xe77480
0c 00007ffc`9e063d30     : 00000000`00000001 00000b3c`009ddf90 00000b3c`009ddf90 00000b38`00019378 : chrome!sqlite3_dbdata_init+0x11e1bc3
0d 00007ffc`9a7986b0     : 00000b3c`017046b0 00000b38`00019378 000001ac`a67f9380 00000b3c`0150ee70 : chrome!sqlite3_dbdata_init+0x11e51a0
0e 00007ffc`9a79a421     : 00000b3c`04520500 00007ffc`96e3ab3b 00000b3c`0265cd80 00000b3c`0066d780 : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc77b20
0f 00007ffc`9c5841fc     : 00000000`00000008 00000017`89ffd550 00000b3c`01d1ede0 00007ffc`983d4eaf : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc79891
10 00007ffc`9c586af0     : 00000b3c`01d1ed80 00007ffc`977d34a9 000001ac`a67f9380 00000b3c`046ce2a8 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a6366c
11 00007ffc`9a3eb996     : 00000017`89ffd458 00000017`89ffd4f0 00000b3c`00129738 00007ffc`93e28919 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a65f60
12 00007ffc`9a3eb8ce     : 00000000`00000000 00000000`00000000 00000000`00000000 00007ffc`a2d96fb0 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x8cae06
13 00007ffc`9a3ee109     : 00005d6e`6a213742 00000017`89ffd658 00000b38`00051140 00007ffc`9c1d4e99 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x8cad3e
14 00007ffc`9a3ee025     : 00007ffc`a1576a78 00007ffc`a0cc2b0c 00007ffc`a17715e0 00000b3c`025d7c00 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x8cd579
15 00007ffc`9a798d4f     : 00000b3c`0150ee70 00000b3c`0429cd00 00000000`00000001 00000b3c`0429cc80 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x8cd495
16 00007ffc`9c58556b     : 00000000`00000006 00000000`00000000 00000000`00000000 00000017`89ffd6c8 : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc781bf
17 00007ffc`9c58495a     : 00000000`00000001 00000000`00000033 00000000`00000050 00000b38`00019378 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a649db
18 00007ffc`9c586cc5     : 80000000`00000050 00000008`00000085 00000000`00000002 00000b3c`04520580 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a63dca
19 00007ffc`9a798d4f     : 00000000`00000001 00000b3c`04520300 00000000`00000033 80000000`00000038 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2a66135
1a 00007ffc`9a79a6e2     : 00007ffc`a23e736c 00000017`89ffdc10 00000000`00000001 00000000`00000013 : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc781bf
1b 00007ffc`9dd076b5     : 00000b3c`0198c0e8 000000a2`c0899414 00000000`00000000 00000b3c`016bd200 : chrome!CrashForExceptionInNonABICompliantCodeRange+0xc79b52
1c 00007ffc`9a90d0d2     : 00000b38`000c8a88 00000000`00000068 00000b38`00473f58 00000b38`00019378 : chrome!sqlite3_dbdata_init+0xe88b25
1d 00007ffc`96a67411     : 00000b38`00019208 00007ffd`721b01a9 00007ffc`93c07da6 00007ffc`93c0794c : chrome!CrashForExceptionInNonABICompliantCodeRange+0xdec542
1e 00007ffc`976d351d     : 00000017`89ffe580 00000000`00400000 00000b38`000b80a0 00000b3c`0167c7a0 : chrome!IsSandboxedProcess+0x78ee11
1f 00007ffc`933efa1d     : 00000017`89ffe6f0 00000017`89ffe7e0 00000000`00000001 00000001`00e3ab3b : chrome!IsSandboxedProcess+0x13faf1d
20 00007ffc`97d07d9b     : 00000017`89ffeaa0 00000b38`000192a8 00000000`00000000 00007ffc`96e3ab3b : chrome+0x5fa1d
21 00007ffc`941053fe     : 00000017`89ffeaa0 00000017`89ffeaa0 00000000`00000000 00007ffc`96e3ab3b : chrome!IsSandboxedProcess+0x1a2f79b
22 00007ffc`93c07da6     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`0000009a : chrome!ChromeMain+0x54611e
23 00007ffc`93c0794c     : 00000000`7bd05a00 00000000`ffffffff 00000000`00000018 00000b3c`00004300 : chrome!ChromeMain+0x48ac6
24 00007ffc`93c06586     : 00000017`89ffe9b0 00000b38`00098000 00000000`7bd05a00 00007ffd`7225183d : chrome!ChromeMain+0x4866c
25 00007ffc`93bc1a8c     : 00000000`00000000 00000000`00000000 00000000`00000000 00005d6e`6a210b82 : chrome!ChromeMain+0x472a6
26 00007ffc`93bc1151     : 00000017`89ffef01 00007ffc`a19c4535 00000863`7bd05a00 00000b38`0004c338 : chrome!ChromeMain+0x27ac
27 00007ffc`93bbf604     : 00007ff7`7be90000 00000b38`000501b0 00000017`89fff120 00000000`00000000 : chrome!ChromeMain+0x1e71
28 00007ff7`7beb3c78     : 00007050`000642b0 00007ffc`93bbf2e0 00000017`89fff100 00000000`00000000 : chrome!ChromeMain+0x324
29 00007ff7`7beb1ca4     : 00000017`89fff410 00000017`89fff410 00000000`00000000 00000017`89fff558 : chrome_exe+0x23c78
2a 00007ff7`7bfec242     : 00007ff7`7c0cf600 00007ff7`7bfec2b9 00000000`00000000 00000000`00000000 : chrome_exe+0x21ca4
2b 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!IsSandboxedProcess+0xb63e2
2c 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
2d 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

   1  Id: 10260.e9f8 Suspend: 0 Teb: 00000017`897f7000 Unfrozen "LoaderLockSampler"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000000`00000000 00000b38`000640e0 00000000`00000001 000001ac`a5fa0ed0 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`9788dd3b     : 00000000`00000000 00007ffc`984e2b6a 7fffffff`00000000 00000000`000002a0 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`980a7cb6     : 00000000`00000000 00000000`00000000 7fffffff`ffffffff 00007ffc`94018449 : chrome!IsSandboxedProcess+0x15b573b
03 00007ffc`97d07d9b     : 00000000`00000000 00000b38`000188a8 fffffffc`00000000 00007ffc`96e3ab71 : chrome!IsSandboxedProcess+0x1dcf6b6
04 00007ffc`941053fe     : fffffffc`00000000 00007ffc`97122ea6 00005d6e`68211962 00005d6e`68211b62 : chrome!IsSandboxedProcess+0x1a2f79b
05 00007ffc`947f1b54     : 00000b38`00050330 00007ffc`947f1c26 00000b38`000188a8 00007ffc`94104778 : chrome!ChromeMain+0x54611e
06 00007ffc`947f17f6     : 00000000`00000000 00000000`00000000 00000000`00000001 00007ffc`979f78dd : chrome!ChromeMain+0xc32874
07 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060180 00000000`00000001 00000000`00000000 : chrome!ChromeMain+0xc32516
08 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
09 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
0a 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

   2  Id: 10260.efbc Suspend: 0 Teb: 00000017`897f9000 Unfrozen "BrokerEvent"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f892b1c     : 00007050`000ac0d0 00000000`00000000 00007050`0002c480 00007050`00080060 : ntdll!NtRemoveIoCompletion+0x14
01 00007ff7`7bee32f4     : 00000017`8c7ffe20 00007050`00080060 00000000`00000000 00000000`00000000 : KERNELBASE!GetQueuedCompletionStatus+0x6c
02 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe+0x532f4
03 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
04 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

   3  Id: 10260.53f0 Suspend: 0 Teb: 00000017`897fb000 Unfrozen "HangWatcher"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00007ffc`a21b4d94 00000000`00000024 00000000`00000120 63746157`676e6148 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`971267e0     : 000000a2`c04ee90e 00007ffc`96f7c30e 00000000`00000000 00000000`0000037c : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`9c64ca2e     : 00000000`00000001 00000b38`000ecb40 00000b38`000ecb80 00007ffd`70124970 : chrome!IsSandboxedProcess+0xe4e1e0
03 00007ffc`9c64cb12     : 00000b38`000ecbc0 00000b38`00060a40 00000000`00000001 00007ffd`70124970 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2b2be9e
04 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060a40 00000000`00000001 00000000`00000000 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2b2bf82
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

   4  Id: 10260.b42c Suspend: 0 Teb: 00000017`897fd000 Unfrozen "PerfettoTrace"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f892b1c     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!NtRemoveIoCompletion+0x14
01 00007ffc`968bbba7     : 00000b38`000cb090 00000b38`00473cd0 00000000`00000000 00000000`00000000 : KERNELBASE!GetQueuedCompletionStatus+0x6c
02 00007ffc`968b8963     : 7fffffff`ffffffff 00000b38`00473cd0 00000000`00000001 0000be68`c75fb1cb : chrome!IsSandboxedProcess+0x5e35a7
03 00007ffc`933efa1d     : 00000017`8d7ffa00 00000017`8d7ffaf0 00000000`00000001 00000001`00e3ab3b : chrome!IsSandboxedProcess+0x5e0363
04 00007ffc`97d07d9b     : 00000000`00000000 00000b38`00019a28 fffffffc`00000000 00007ffc`96e3ab3b : chrome+0x5fa1d
05 00007ffc`941053fe     : fffffffc`00000000 00007ffc`97122ea6 00005d6e`6ea11882 00005d6e`6ea11a82 : chrome!IsSandboxedProcess+0x1a2f79b
06 00007ffc`947f1b54     : 00000b38`00473eb0 00007ffc`947f1c26 00000b38`00019a28 00007ffc`94104778 : chrome!ChromeMain+0x54611e
07 00007ffc`947f17f6     : 00000000`00000000 00000000`00000000 00000000`00000001 00007ffc`979f78dd : chrome!ChromeMain+0xc32874
08 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060a90 00000000`00000001 00000000`00000000 : chrome!ChromeMain+0xc32516
09 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
0a 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
0b 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

   5  Id: 10260.baf4 Suspend: 0 Teb: 00000017`89600000 Unfrozen "ThreadPoolServiceThread"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`971267e0     : 000000a2`c0de6bb6 00000b38`00019e20 00000b38`00000000 00000000`000003bc : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`980a7c97     : 00000000`00000019 00000000`00000000 7fffffff`ffffffff 00007ffc`94018449 : chrome!IsSandboxedProcess+0xe4e1e0
03 00007ffc`97d07d9b     : 00000000`00000019 00000b38`00019f28 fffffffc`00000000 00007ffc`96e3ab3b : chrome!IsSandboxedProcess+0x1dcf697
04 00007ffc`941053fe     : fffffffc`00000000 00007ffc`97122ea6 00005d6e`6e211be2 00005d6e`6e2115e2 : chrome!IsSandboxedProcess+0x1a2f79b
05 00007ffc`95e36494     : 00000b38`004735e0 00007ffc`947f1c26 00000b38`00019f28 00007ffc`94104778 : chrome!ChromeMain+0x54611e
06 00007ffc`947f17f6     : 00000000`00000000 00000000`00000000 00000000`00000001 00007ffc`979f78dd : chrome!GetHandleVerifier+0x6054
07 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060b90 00000000`00000001 00000000`00000000 : chrome!ChromeMain+0xc32516
08 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
09 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
0a 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

   6  Id: 10260.ad34 Suspend: 0 Teb: 00000017`89602000 Unfrozen "ThreadPoolSingleThreadCOMSTASharedForegroundBlocking0"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffc`962e57be     : 7fffffff`ffffffff 00000017`8e7ffc30 00000b38`000a9d00 00000b38`000980d0 : win32u!NtUserMsgWaitForMultipleObjectsEx+0x14
01 00007ffc`96922a41     : 00000000`00000000 00000b38`000980d0 7fffffff`ffffffff 00000000`00000000 : chrome!IsSandboxedProcess+0xd1be
02 00007ffc`934061a8     : 00000000`00000001 00007ffc`93405fbf 00000000`000003c8 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64a441
03 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060bd0 00000000`00000001 00000000`00000000 : chrome+0x761a8
04 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
05 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
06 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

   7  Id: 10260.1081c Suspend: 0 Teb: 00000017`89604000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000000`00000000 00000000`00000000 00000000`00000000 00005d6e`6d211a02 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`96922ae0     : 00000000`001a028d 00000b38`000980d0 7fffffff`00000000 00000000`000003a8 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`000003c4 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64a4e0
03 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060be0 00000000`00000001 00000000`00000000 : chrome+0x760b8
04 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
05 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
06 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

   8  Id: 10260.ff28 Suspend: 0 Teb: 00000017`89606000 Unfrozen "ThreadPoolBackgroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`96922ae0     : 00000000`00128730 00000b38`000980d0 7fffffff`00000000 00000000`000003b0 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`93406108     : 00000000`00000001 00007ffc`93405fe1 00000000`000003c0 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64a4e0
03 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060c00 00000000`00000001 00000000`00000000 : chrome+0x76108
04 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
05 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
06 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

   9  Id: 10260.6ccc Suspend: 0 Teb: 00000017`89608000 Unfrozen "ThreadPoolBackgroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`8ffffd00 00007ffc`95e250f9 000000a2`c00b5f95 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`8ffffbb0 00000000`00000000 00000000`00000000 00000000`00000404 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`00143c78 00000b38`000980d0 7fffffff`00000000 00000000`00000404 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`93406108     : 00000000`00000001 00007ffc`93405fe1 00000000`00000434 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060bf0 00000000`00000001 00000000`00000000 : chrome+0x76108
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  10  Id: 10260.10258 Suspend: 0 Teb: 00000017`8960a000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`721d5e0e     : 00000000`00000002 00000000`00000000 00007ffd`721d7a80 000001ac`aea7fe20 : ntdll!NtWaitForWorkViaWorkerFactory+0x14
01 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!TppWorkerThread+0x37e
02 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
03 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  11  Id: 10260.ccc8 Suspend: 0 Teb: 00000017`8960c000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`90fffb80 00007ffc`93bda118 000000a2`bf7aab7a 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`90fffa30 00000000`00000000 00000000`00000000 00000000`00000438 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`001b661d 00000b38`000980d0 7fffffff`00000000 00000000`00000438 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`0000049c 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060bc0 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  12  Id: 10260.ef78 Suspend: 0 Teb: 00000017`8960e000 Unfrozen "Chrome_IOThread"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f892b1c     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!NtRemoveIoCompletion+0x14
01 00007ffc`968bbba7     : 00000b38`000c8a10 00000b3c`00030780 00000000`00000000 00000000`00000000 : KERNELBASE!GetQueuedCompletionStatus+0x6c
02 00007ffc`968b8963     : 000000a2`c351ce59 00000b3c`00030780 00000000`00000000 0000be68`db5fb45b : chrome!IsSandboxedProcess+0x5e35a7
03 00007ffc`933efa1d     : 00000017`917ff590 00000017`917ff680 00000000`00000001 00000001`00e3ab3b : chrome!IsSandboxedProcess+0x5e0363
04 00007ffc`97d07d9b     : 00000000`00000000 00000b38`00018da8 fffffffc`00000000 00007ffc`96e3ab3b : chrome+0x5fa1d
05 00007ffc`941053fe     : 00000000`00000010 00007ffd`6f914b51 fffffffc`00000000 00005d6e`72a11112 : chrome!IsSandboxedProcess+0x1a2f79b
06 00007ffc`95d184eb     : 00000b38`000508a8 00000b38`000508a0 00005d6e`72a11442 00000b3c`0002c3c0 : chrome!ChromeMain+0x54611e
07 00007ffc`947f17f6     : 00000000`00000000 00000000`00000000 00000000`00000001 00007ffc`979f78dd : chrome!ChromeMain+0x215920b
08 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060cb0 00000000`00000001 00000000`00000000 : chrome!ChromeMain+0xc32516
09 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
0a 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
0b 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  13  Id: 10260.9778 Suspend: 0 Teb: 00000017`89610000 Unfrozen "MemoryInfra"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`9788dd3b     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`000004a8 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`980a7cb6     : 00000000`00000000 00000000`00000000 7fffffff`ffffffff 00007ffc`94018449 : chrome!IsSandboxedProcess+0x15b573b
03 00007ffc`97d07d9b     : 00000000`00000000 00000b38`0001a6a8 fffffffc`00000000 00007ffc`96e3ab3b : chrome!IsSandboxedProcess+0x1dcf6b6
04 00007ffc`941053fe     : fffffffc`00000000 00007ffc`97122ea6 00005d6e`72211a12 00005d6e`72211412 : chrome!IsSandboxedProcess+0x1a2f79b
05 00007ffc`947f1b54     : 00000b38`00473040 00007ffc`947f1c26 00000b38`0001a6a8 00007ffc`94104778 : chrome!ChromeMain+0x54611e
06 00007ffc`947f17f6     : 00000000`00000000 00000000`00000000 00000000`00000001 00007ffc`979f78dd : chrome!ChromeMain+0xc32874
07 00007ffc`93b15b47     : 00000000`00000000 00000b38`00060d30 00000000`00000001 00000000`00000000 : chrome!ChromeMain+0xc32516
08 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
09 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
0a 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  14  Id: 10260.11428 Suspend: 0 Teb: 00000017`89612000 Unfrozen "ThreadPoolSingleThreadCOMSTASharedBackgroundBlocking1"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffc`962e57be     : 7fffffff`ffffffff 00000000`00000000 00000b3c`00094b40 00000b3c`00010a90 : win32u!NtUserMsgWaitForMultipleObjectsEx+0x14
01 00007ffc`96922a41     : 00000000`00000000 00000b38`000980d0 7fffffff`ffffffff 00000000`00000000 : chrome!IsSandboxedProcess+0xd1be
02 00007ffc`934061f8     : 00000000`00000001 00007ffc`93405fe1 00000000`000004fc 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64a441
03 00007ffc`93b15b47     : 00000000`00000000 00000b3c`0002cda0 00000000`00000001 00000000`00000000 : chrome+0x761f8
04 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
05 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
06 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  15  Id: 10260.6820 Suspend: 0 Teb: 00000017`89614000 Unfrozen "ThreadPoolSingleThreadCOMSTASharedForeground2"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffc`962e57be     : 7fffffff`ffffffff 00000017`92fffbe0 00000b3c`00094ab0 00000b38`000980d0 : win32u!NtUserMsgWaitForMultipleObjectsEx+0x14
01 00007ffc`96922a41     : 00000000`00000000 00000b38`000980d0 7fffffff`ffffffff 00000000`00000000 : chrome!IsSandboxedProcess+0xd1be
02 00007ffc`934061a8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000500 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64a441
03 00007ffc`93b15b47     : 00000000`00000000 00000b3c`0002cdc0 00000000`00000001 00000000`00000000 : chrome+0x761a8
04 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
05 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
06 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  16  Id: 10260.d194 Suspend: 0 Teb: 00000017`89616000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f892533     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!NtWaitForMultipleObjects+0x14
01 00007ffd`7036ddae     : 00000000`0000061c 00000000`00000000 00000000`0000061c 00000000`00000000 : KERNELBASE!WaitForMultipleObjectsEx+0x123
02 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : combase!WaitCoalesced+0x79 [onecore\com\published\comutils\coalescedwait.cxx @ 70] 
03 00007ffd`70366caf     : 000001ac`b136afc0 00000000`00000000 00000000`0200000a 00000000`0200000a : combase!CROIDTable::WorkerThreadLoop+0xae [onecore\com\combase\dcomrem\refcache.cxx @ 1716] 
04 00007ffd`70366b59     : 000001ac`b13cbdb0 00000000`00000000 00000000`00000000 00000000`00000000 : combase!CRpcThread::WorkerLoop+0x5b [onecore\com\combase\dcomrem\threads.cxx @ 283] 
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : combase!CRpcThreadCache::RpcWorkerThreadEntry+0x29 [onecore\com\combase\dcomrem\threads.cxx @ 77] 
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  17  Id: 10260.ba40 Suspend: 0 Teb: 00000017`89618000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`712904a3     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00001040 : win32u!NtUserMessageCall+0x14
01 00007ffd`712903f9     : 00000000`008b0b82 00000000`00000219 00000000`00008004 000001ac`bf69aec8 : user32!fnINDEVICECHANGE+0x83
02 00007ffd`705ec7a3     : 000001ac`a5c10000 00000000`00000008 00000000`00000000 000001ac`b057bfa8 : user32!DeviceNotificationCallback+0x29
03 00007ffd`70601add     : 00000000`00000001 000001ac`b03ccfb0 00000000`00000000 000001ac`b059bdf0 : sechost!HandleDeviceInterfaceEvents+0x103
04 00007ffd`6e5c89b1     : 000001ac`bb8b2eb0 000001ac`b059bdf0 00000000`00000001 00000000`00000001 : sechost!DeviceNotifyEventCallback+0xad
05 00007ffd`6e5c8734     : 00000000`0000014e 000001ac`b4525fc4 000001ac`bb8b2eb0 00000000`00000000 : cfgmgr32!ProcessDeviceInterfaceEvent+0xd9
06 00007ffd`6e5ce67d     : 000001ac`a5c10000 000001ac`b059bdf0 00000017`00000000 000001ac`b059bff0 : cfgmgr32!ProcessEventBlockList+0x234
07 00007ffd`721d5240     : 00000017`93fff6c8 00000017`93fff4d0 000001ac`b0022fd8 00009dab`08490abd : cfgmgr32!ProcessPlugPlayEventCallback+0x10d
08 00007ffd`721d6291     : 00000000`00000000 00000000`00000000 00007ffd`7223a440 00000000`00000000 : ntdll!TppWorkpExecuteCallback+0x4d0
09 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!TppWorkerThread+0x801
0a 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
0b 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  18  Id: 10260.10ddc Suspend: 0 Teb: 00000017`8961c000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`957ffd30 00007ffc`944f0f93 000000a2`b4fbbbf8 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`957ffbe0 00000000`00000000 00000000`00000000 00000000`00000618 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`001d03b9 00000b38`000980d0 7fffffff`00000000 00000000`00000618 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000680 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00234f20 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  19  Id: 10260.be48 Suspend: 0 Teb: 00000017`8961e000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 7fffffff`ffffffff 00000017`94fff4d0 6a66fe99`30996eba 00000017`94fff480 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`94fff520 00000000`0000002f 00000001`00000000 00000000`00000624 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`0015ebf6 00000b38`000980d0 7fffffff`00000000 00000000`00000624 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000694 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`0002c5e0 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  20  Id: 10260.10760 Suspend: 0 Teb: 00000017`89620000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`95fff920 00007ffc`95ff1a98 000000a2`b4fbba6e 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`95fff7d0 00000000`00000000 00000000`00000000 00000000`00000628 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`001d046c 00000b38`000980d0 7fffffff`00000000 00000000`00000628 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`000006a0 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`0002c5c0 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  21  Id: 10260.11b14 Suspend: 0 Teb: 00000017`89622000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`967ff8d0 00007ffc`953a1859 000000a2`b2d814be 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`967ff780 00000000`00000000 00000000`00000000 00000000`00000620 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`039f9d77 00000b38`000980d0 7fffffff`00000000 00000000`00000620 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`000006e0 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00234fa0 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  22  Id: 10260.d494 Suspend: 0 Teb: 00000017`89624000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 7fffffff`ffffffff 00000017`96fff6b0 6a66fe99`30996eba 00000017`96fff660 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`96fff700 00000000`0000002f 00000001`00000000 00000000`00000630 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`03990f3e 00000b38`000980d0 7fffffff`00000000 00000000`00000630 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000690 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00235600 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  23  Id: 10260.ed30 Suspend: 0 Teb: 00000017`89626000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`977ff880 00007ffc`955707d9 000000a2`b17221a9 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`977ff730 00000000`00000000 00000000`00000000 00000000`00000634 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`03975bbe 00000b38`000980d0 7fffffff`00000000 00000000`00000634 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`000006ac 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`002355e0 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  24  Id: 10260.ac14 Suspend: 0 Teb: 00000017`89628000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`97fff770 00007ffc`93875df9 000000a2`b170af7f 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`97fff620 00000000`00000000 00000000`00000000 00000000`00000644 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`0394a442 00000b38`000980d0 7fffffff`00000000 00000000`00000644 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`000006d4 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`0002c580 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  25  Id: 10260.2708 Suspend: 0 Teb: 00000017`8962a000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f892b1c     : 00000000`00000000 00007ffc`a2d96fb0 00000000`00000001 00000000`000006e4 : ntdll!NtRemoveIoCompletion+0x14
01 00007ffc`9c641c84     : 00000b3c`002355a0 00007ffc`a2f5d4e8 00000000`00000000 00000000`00000000 : KERNELBASE!GetQueuedCompletionStatus+0x6c
02 00007ffc`93b15b47     : 00000000`00000000 00000b3c`002355a0 00000000`00000001 00000000`00000000 : chrome!CrashForExceptionInNonABICompliantCodeRange+0x2b210f4
03 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
04 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
05 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  26  Id: 10260.1180c Suspend: 0 Teb: 00000017`8962c000 Unfrozen "ThreadPoolSingleThreadForegroundBlocking3"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000b3c`000000f9 00007ffc`94a4eeac 000000a2`bfbd52ca 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`98fff440 00000000`00000000 00000000`00000000 00000000`00000678 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`001601b4 00000b38`000980d0 7fffffff`00000000 00000000`00000678 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`93406248     : 00000000`00000001 00007ffc`93405fbf 00000000`00000710 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00670fc0 00000000`00000001 00000000`00000000 : chrome+0x76248
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  27  Id: 10260.10ee0 Suspend: 0 Teb: 00000017`8962e000 Unfrozen "CacheThread_BlockFile"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f892b1c     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!NtRemoveIoCompletion+0x14
01 00007ffc`968bbba7     : 00000b3c`000c7e90 00000b3c`002d3380 00000000`00000000 00000000`00000000 : KERNELBASE!GetQueuedCompletionStatus+0x6c
02 00007ffc`968b8963     : 000000a2`c18081ce 00000b3c`002d3380 00000000`00000000 0000be68`d35fb1cb : chrome!IsSandboxedProcess+0x5e35a7
03 00007ffc`933efa1d     : 00000017`997ffa00 00000017`997ffaf0 00000000`00000001 00000001`00e3ab3b : chrome!IsSandboxedProcess+0x5e0363
04 00007ffc`97d07d9b     : 00000000`00000000 00000b3c`0019c628 fffffffc`00000000 00007ffc`96e3ab3b : chrome+0x5fa1d
05 00007ffc`941053fe     : fffffffc`00000000 00007ffc`97122ea6 00005d6e`7aa11882 00005d6e`7aa11a82 : chrome!IsSandboxedProcess+0x1a2f79b
06 00007ffc`947f1b54     : 00000b3c`0023d850 00007ffc`947f1c26 00000b3c`0019c628 00007ffc`94104778 : chrome!ChromeMain+0x54611e
07 00007ffc`947f17f6     : 00000000`00000000 00000000`00000000 00000000`00000001 00007ffc`979f78dd : chrome!ChromeMain+0xc32874
08 00007ffc`93b15b47     : 00000000`00000000 00000b3c`006719c0 00000000`00000001 00000000`00000000 : chrome!ChromeMain+0xc32516
09 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
0a 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
0b 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  28  Id: 10260.4f24 Suspend: 0 Teb: 00000017`89630000 Unfrozen "CompositorTileWorker1"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`721f4c1e     : 00000017`99fffb58 00000b3c`023d62c0 00000b3c`00013d10 00007ffc`97a848a3 : ntdll!NtWaitForAlertByThreadId+0x14
01 00007ffd`6f892818     : 00000000`00000000 00000b3c`00013cf8 00000000`00000000 00007ffd`721f5640 : ntdll!RtlSleepConditionVariableSRW+0x1de
02 00007ffc`9723669e     : 00000b3c`00013cf0 00007ffc`93e8ee4b 00000000`00004f24 00000b3c`00013d08 : KERNELBASE!SleepConditionVariableSRW+0x38
03 00007ffc`93e8eb51     : 00000b3c`00013cf8 00000b38`000dc120 ffffffff`fffffffe 00007ffc`93b23d4b : chrome!IsSandboxedProcess+0xf5e09e
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`006719a0 00000000`00000001 00000000`00000000 : chrome!ChromeMain+0x2cf871
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  29  Id: 10260.4794 Suspend: 0 Teb: 00000017`89632000 Unfrozen "VideoCaptureThread"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffc`976d3972     : 00007ffc`a2f5d738 00000b3c`0019c7a0 00000000`00000001 00000000`00000000 : win32u!NtUserMsgWaitForMultipleObjectsEx+0x14
01 00007ffc`976d34df     : 00000017`9a7ff8e0 00000000`00000000 00000b3c`0006d600 00000000`00000000 : chrome!IsSandboxedProcess+0x13fb372
02 00007ffc`933efa1d     : 00000017`9a7ffa50 00000017`9a7ffb40 00000000`00000001 00000001`00e3ab3b : chrome!IsSandboxedProcess+0x13faedf
03 00007ffc`97d07d9b     : 00000000`00000000 00000b3c`0019c8a8 fffffffc`00000000 00007ffc`96e3ab3b : chrome+0x5fa1d
04 00007ffc`941053fe     : fffffffc`00000000 000001ac`b016edb0 00005d6e`79a118d2 00005d6e`79a11ad2 : chrome!IsSandboxedProcess+0x1a2f79b
05 00007ffc`947f1b54     : 00000017`9a7ffc30 00007ffc`94bd2993 00000b3c`0019c8a8 00007ffc`94104778 : chrome!ChromeMain+0x54611e
06 00007ffc`947f17f6     : 00000000`00000000 00000b3c`006729e0 00000000`00000001 00007ffc`979f78dd : chrome!ChromeMain+0xc32874
07 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00671840 00000000`00000001 00000000`00000000 : chrome!ChromeMain+0xc32516
08 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
09 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
0a 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  30  Id: 10260.11038 Suspend: 0 Teb: 00000017`89634000 Unfrozen "MemoryListSampler"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 5994340d`d6667a3d 00000017`9afffa30 00000000`00000000 00000000`00000001 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`971267e0     : 000000a2`c0e14ddc 00000000`1dcd6500 00000000`00000000 00000000`000005d8 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`95e1abcc     : 00000000`00000000 ec35e024`01dc89b1 00000000`00000030 00000000`00000011 : chrome!IsSandboxedProcess+0xe4e1e0
03 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00235380 00000000`00000001 00000000`00000000 : chrome!ChromeMain+0x225b8ec
04 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
05 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
06 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  31  Id: 10260.1508c Suspend: 0 Teb: 00000017`89636000 Unfrozen "ThreadPoolSingleThreadSharedBackgroundBlocking4"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00007ffc`0000004e 00007ffc`954b786c 000000a2`b170f160 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`9b7ff6e0 00000000`00000000 00007ffc`00000000 00000000`0000072c : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`039912e1 00000b38`000980d0 7fffffff`00000000 00000000`0000072c : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934063f8     : 00000000`00000001 00007ffc`93405fe1 00000000`00000918 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00716340 00000000`00000001 00000000`00000000 : chrome+0x763f8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  32  Id: 10260.ae58 Suspend: 0 Teb: 00000017`89638000 Unfrozen "ThreadPoolSingleThreadForegroundBlocking5"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000b3c`0000003a 00007ffc`9ce69e0c 000000a2`b205ea9d 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`9bfff900 00000000`00000000 00007ffc`00000000 00000000`000009b8 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`03999047 00000b38`000980d0 7fffffff`00000000 00000000`000009b8 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`93406248     : 00000000`00000001 00007ffc`93405fbf 00000000`00000a38 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`008a5a20 00000000`00000001 00000000`00000000 : chrome+0x76248
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  33  Id: 10260.ef4 Suspend: 0 Teb: 00000017`8963a000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 7fffffff`ffffffff 00000017`9c7ff830 6a66fe99`30996eba 00000017`9c7ff7e0 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`9c7ff880 00000000`0000002f 00000000`00000000 00000000`000009c4 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`0397587f 00000b38`000980d0 7fffffff`00000000 00000000`000009c4 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000a48 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00671c00 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  34  Id: 10260.83f0 Suspend: 0 Teb: 00000017`8963c000 Unfrozen "ThreadPoolSingleThreadSharedForeground6"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000000`00000067 00007ffc`9800f3af 000000a2`bfe2ae5d 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`9cfff570 00000000`00000000 00000000`00000000 00000000`000009d0 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`001e6cb4 00000b38`000980d0 7fffffff`00000000 00000000`000009d0 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`93406158     : 00000000`00000001 00007ffc`93405fbf 00000000`00000acc 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`008a73c0 00000000`00000001 00000000`00000000 : chrome+0x76158
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  35  Id: 10260.15c24 Suspend: 0 Teb: 00000017`8963e000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`9d7ff860 00007ffc`93875df9 000000a2`b170b340 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`9d7ff710 00000000`00015c24 00000000`00000000 00000000`000009dc : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`03946a15 00000b38`000980d0 7fffffff`00000000 00000000`000009dc : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000ad4 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`008a73a0 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  36  Id: 10260.e3d4 Suspend: 0 Teb: 00000017`89640000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`9dfff8e0 00007ffc`93875df9 000000a2`b170b406 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`9dfff790 00000000`0000e3d4 00000003`00000000 00000000`000009e4 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`03946a07 00000b38`000980d0 7fffffff`00000000 00000000`000009e4 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000900 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`008a7360 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  37  Id: 10260.eb6c Suspend: 0 Teb: 00000017`89642000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 7fffffff`ffffffff 00000017`9e7ff920 6a66fe99`30996eba 00000017`9e7ff8d0 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`9e7ff970 00000000`0000eb6c 00000000`00000000 00000000`000009ec : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`03975878 00000b38`000980d0 7fffffff`00000000 00000000`000009ec : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000a4c 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00671e00 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  38  Id: 10260.5314 Suspend: 0 Teb: 00000017`89644000 Unfrozen "ThreadPoolSingleThreadCOMSTASharedForegroundBlocking7"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffc`962e57be     : 7fffffff`ffffffff 00000017`9efff620 00000b3c`00813780 00000b38`000980d0 : win32u!NtUserMsgWaitForMultipleObjectsEx+0x14
01 00007ffc`96922a41     : 00000000`00000000 00000b38`000980d0 7fffffff`ffffffff 00000000`00000000 : chrome!IsSandboxedProcess+0xd1be
02 00007ffc`934061a8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000ba4 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64a441
03 00007ffc`93b15b47     : 00000000`00000000 00000b3c`009f5320 00000000`00000001 00000000`00000000 : chrome+0x761a8
04 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
05 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
06 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  39  Id: 10260.cb28 Suspend: 0 Teb: 00000017`89646000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 00000017`9f7ff8d0 00007ffc`94c2bd06 000000a2`b172231c 00000000`00000000 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`9f7ff780 00000000`00000000 00000000`00000000 00000000`00000b70 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`03975922 00000b38`000980d0 7fffffff`00000000 00000000`00000b70 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000c20 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`00b7c860 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  40  Id: 10260.15b64 Suspend: 0 Teb: 00000017`89648000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 7fffffff`ffffffff 00000017`9ffff850 6a66fe99`30996eba 00000017`9ffff800 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`9ffff8a0 00000000`0000002f 00000000`00000000 00000000`00000b30 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`03975bb5 00000b38`000980d0 7fffffff`00000000 00000000`00000b30 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000c24 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`0093c100 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  41  Id: 10260.e9d0 Suspend: 0 Teb: 00000017`8964a000 Unfrozen "ThreadPoolForegroundWorker"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f88bc5f     : 7fffffff`ffffffff 00000017`a07ff760 6a66fe99`30996eba 00000017`a07ff710 : ntdll!NtWaitForSingleObject+0x14
01 00007ffc`97126950     : 00000017`a07ff7b0 00000000`0000002f 00000000`00000000 00000000`00000bd4 : KERNELBASE!WaitForSingleObjectEx+0xaf
02 00007ffc`96923499     : 00000000`03975871 00000b38`000980d0 7fffffff`00000000 00000000`00000bd4 : chrome!IsSandboxedProcess+0xe4e350
03 00007ffc`934060b8     : 00000000`00000001 00007ffc`93405fbf 00000000`00000c1c 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64ae99
04 00007ffc`93b15b47     : 00000000`00000000 00000b3c`0093c780 00000000`00000001 00000000`00000000 : chrome+0x760b8
05 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
06 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
07 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  42  Id: 10260.8c74 Suspend: 0 Teb: 00000017`8964e000 Unfrozen "DManip Delegate Thread"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`5d713084     : 000001ac`be550000 00000000`00000000 00000000`00000000 00007ffd`722c5904 : win32u!NtUserMsgWaitForMultipleObjectsEx+0x14
01 00007ffd`5d712e1a     : 000001ac`be5bffa0 00000000`00000000 00000000`00000000 00000000`00000000 : directmanipulation!CManagerImpl::_RunDelegateThread+0x114
02 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : directmanipulation!CManagerImpl::_DelegateThreadProc+0xba
03 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
04 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  43  Id: 10260.7674 Suspend: 0 Teb: 00000017`89650000 Unfrozen "ThreadPoolSingleThreadCOMSTASharedBackgroundBlocking8"
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffc`962e57be     : 7fffffff`ffffffff 00000000`00000000 00000b3c`00a45190 00000b3c`01399bd0 : win32u!NtUserMsgWaitForMultipleObjectsEx+0x14
01 00007ffc`96922a41     : 00000000`00000000 00000b38`000980d0 7fffffff`ffffffff 00000000`00000000 : chrome!IsSandboxedProcess+0xd1be
02 00007ffc`934061f8     : 00000000`00000001 00007ffc`93405fe1 00000000`0000126c 00007ffd`70124970 : chrome!IsSandboxedProcess+0x64a441
03 00007ffc`93b15b47     : 00000000`00000000 00000b3c`017998e0 00000000`00000001 00000000`00000000 : chrome+0x761f8
04 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome+0x785b47
05 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
06 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  44  Id: 10260.121f0 Suspend: 0 Teb: 00000017`89658000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f892533     : 00000000`00000000 00000000`00000000 00001f80`0010001b 00000000`00000033 : ntdll!NtWaitForMultipleObjects+0x14
01 00007ffd`6f892401     : 000001ac`c085afc0 00007ffd`6c5f4177 00000000`00000000 00000000`001d3b72 : KERNELBASE!WaitForMultipleObjectsEx+0x123
02 00007ffd`4d3943cb     : 00000000`00000000 00000000`001d3b72 000001ac`c085afa0 00000000`00000000 : KERNELBASE!WaitForMultipleObjects+0x11
03 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : perfos!StandbyMonitorThreadProc+0xdb
04 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
05 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  45  Id: 10260.ceb4 Suspend: 0 Teb: 00000017`8965a000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`721d5e0e     : 00000000`00000002 00000000`00000000 00007ffd`721d7a80 000001ac`a5c82e20 : ntdll!NtWaitForWorkViaWorkerFactory+0x14
01 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!TppWorkerThread+0x37e
02 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
03 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  46  Id: 10260.1208c Suspend: 0 Teb: 00000017`8965c000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f892533     : 00007ffd`702a5cc6 00007ffd`704a3682 00007ffd`70281de4 00007ffd`7038a06e : ntdll!NtWaitForMultipleObjects+0x14
01 00007ffd`702b56c4     : 000000fe`f76f3da5 000001ac`b123d1f0 000001ac`b3b4cd30 00000000`00000001 : KERNELBASE!WaitForMultipleObjectsEx+0x123
02 00007ffd`702c15be     : 00000000`29a9c793 000001ac`b130adb0 00000017`8affe521 00007ffd`7217cca4 : combase!MTAThreadWaitForCall+0xf4 [onecore\com\combase\dcomrem\channelb.cxx @ 7198] 
03 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : combase!MTAThreadDispatchCrossApartmentCall+0xd3 [onecore\com\combase\dcomrem\chancont.cxx @ 234] 
04 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : combase!CSyncClientCall::SwitchAptAndDispatchCall+0x4db [onecore\com\combase\dcomrem\channelb.cxx @ 5750] 
05 00007ffd`702ab237     : 00000000`00000000 000001ac`bbe02ed0 00000000`00000000 000001ac`b130adb0 : combase!CSyncClientCall::SendReceive2+0x69e [onecore\com\combase\dcomrem\channelb.cxx @ 5356] 
06 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : combase!SyncClientCallRetryContext::SendReceiveWithRetry+0x2f [onecore\com\combase\dcomrem\callctrl.cxx @ 1503] 
07 00007ffd`702aac9f     : 000001ac`b130adb0 00000017`8affe670 000001ac`bbe02ed0 000001ac`b123d1f0 : combase!CSyncClientCall::SendReceiveInRetryContext+0x5b [onecore\com\combase\dcomrem\callctrl.cxx @ 581] 
08 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : combase!DefaultSendReceive+0x3c [onecore\com\combase\dcomrem\callctrl.cxx @ 539] 
09 00007ffd`702a6a23     : 00007ffd`70516528 00007ffd`702a6f07 00007ffd`704fd920 000001ac`ba358f98 : combase!CSyncClientCall::SendReceive+0x1df [onecore\com\combase\dcomrem\ctxchnl.cxx @ 802] 
0a (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : combase!CClientChannel::SendReceive+0x49 [onecore\com\combase\dcomrem\ctxchnl.cxx @ 674] 
0b 00007ffd`71a17a91     : 00000000`00000000 000001ac`00000000 000001ac`bbe02ed0 00007ffd`704eacd0 : combase!NdrExtpProxySendReceive+0xb3 [onecore\com\combase\ndr\ndrole\proxy.cxx @ 1899] 
0c 00007ffd`702a5cc6     : 00007ffd`704fd920 00007ffd`70357a0f 000001ac`a4410000 00007ffd`721b010a : rpcrt4!NdrpClientCall3+0x431
0d 00007ffd`704a3682     : 00007ffd`70587718 000001ac`b130adb0 00000000`00000000 00000000`00000000 : combase!ObjectStublessClient+0x146 [onecore\com\combase\ndr\ndrole\amd64\stblsclt.cxx @ 366] 
0e 00007ffd`70281de4     : 000001ac`ba358f98 00000000`00000001 000001ac`c197ffa0 000001ac`b123d1f0 : combase!ObjectStubless+0x42 [onecore\com\combase\ndr\ndrole\amd64\stubless.asm @ 176] 
0f 00007ffd`7038a06e     : 00000000`00000000 00000017`8affef50 00000000`00000000 000001ac`b46f3e38 : combase!RemoteReleaseRifRefHelper+0x80 [onecore\com\combase\dcomrem\marshal.cxx @ 9651] 
10 00007ffd`703f1a16     : 000001ac`b46f3e38 00000000`00000001 00000000`00000001 000001ac`c197ffa0 : combase!RemoteReleaseRifRef+0x222 [onecore\com\combase\dcomrem\marshal.cxx @ 9530] 
11 00007ffd`703c44b0     : 00000000`00000000 00000000`00000000 00000000`00000002 000001ac`b46f3e38 : combase!CStdMarshal::DisconnectCliIPIDs+0x35e [onecore\com\combase\dcomrem\marshal.cxx @ 6226] 
12 00007ffd`703c407a     : 000001ac`b130ad00 00000000`00000000 000001ac`b130ad00 00000000`00000000 : combase!CStdMarshal::DisconnectWorker_ReleasesLock+0x418 [onecore\com\combase\dcomrem\marshal.cxx @ 5545] 
13 00007ffd`702f03b9     : 000001ac`b130adb0 000001ac`b46f3e38 000001ac`b46f3f38 000001ac`c15e0ff0 : combase!CStdMarshal::Disconnect+0xe6 [onecore\com\combase\dcomrem\marshal.cxx @ 5310] 
14 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : combase!CStdIdentity::{dtor}+0xac [onecore\com\combase\dcomrem\stdid.cxx @ 388] 
15 00007ffd`702ef250     : 000001ac`b46f3e30 000001ac`baefcfb8 000001ac`b46f3f88 00000000`00000001 : combase!CStdIdentity::`scalar deleting destructor'+0xc9
16 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : combase!CStdIdentity::CInternalUnk::ReleaseWithCallerAddress+0x1a1 [onecore\com\combase\dcomrem\stdid.cxx @ 947] 
17 00007ffd`66d24ea8     : 00000000`80000000 00000000`00000000 00000000`00000000 00000000`00000000 : combase!CStdIdentity::CInternalUnk::Release+0x1b0 [onecore\com\combase\dcomrem\stdid.cxx @ 853] 
18 00007ffd`66d2814b     : 000001ac`b9e85f98 000001ac`b4b8af70 00000000`00000000 000001ac`b46f3f88 : Windows_Devices_Radios!Microsoft::WRL::ComPtr<Windows::Foundation::IAsyncOperation<Windows::Foundation::Collections::IVectorView<Windows::Devices::Radios::Radio * __ptr64> * __ptr64> >::InternalRelease+0x20
19 00007ffd`66d27690     : 000001ac`c06defd8 00007ffd`66d2a061 00000000`00001974 00007ffd`6f8964a9 : Windows_Devices_Radios!Windows::Internal::Details::GitInvokeHelper<Windows::Foundation::ITypedEventHandler<Windows::Devices::Radios::Radio * __ptr64,IInspectable * __ptr64>,Windows::Internal::GitPtrSupportsAgile<Windows::Foundation::ITypedEventHandler<Windows::Devices::Radios::Radio * __ptr64,IInspectable * __ptr64> >,2>::Invoke+0x9b
1a 00007ffd`66d275e3     : 00000000`00000000 000001ac`baa54fd0 00000017`8afff380 00000000`00001974 : Windows_Devices_Radios!Microsoft::WRL::InvokeTraits<-2>::InvokeDelegates<`Microsoft::WRL::EventSource<Windows::Foundation::ITypedEventHandler<Windows::Devices::Radios::Radio * __ptr64,IInspectable * __ptr64>,Microsoft::WRL::InvokeModeOptions<-2> >::InvokeAll<Windows::Devices::Radios::IRadio * __ptr64,std::nullptr_t>'::`2'::<lambda_1>,Windows::Foundation::ITypedEventHandler<Windows::Devices::Radios::Radio * __ptr64,IInspectable * __ptr64> >+0x80
1b 00007ffd`66d2826f     : 000001ac`b8a59fc8 000001ac`c5e29ee0 000001ac`b8a59fc8 00000017`8afff448 : Windows_Devices_Radios!Microsoft::WRL::EventSource<Windows::Foundation::ITypedEventHandler<Windows::Devices::Radios::Radio * __ptr64,IInspectable * __ptr64>,Microsoft::WRL::InvokeModeOptions<-2> >::DoInvoke<`Microsoft::WRL::EventSource<Windows::Foundation::ITypedEventHandler<Windows::Devices::Radios::Radio * __ptr64,IInspectable * __ptr64>,Microsoft::WRL::InvokeModeOptions<-2> >::InvokeAll<Windows::Devices::Radios::IRadio * __ptr64,std::nullptr_t>'::`2'::<lambda_1> >+0x87
1c 00007ffd`498b56fd     : 00000000`00000000 00000000`00000000 00000000`00000000 000001ac`b88d2fe0 : Windows_Devices_Radios!RadioEventListener::OnInstanceRadioChange+0xaf
1d 00007ffd`498b5090     : 000001ac`c5e29ee0 00000000`00000001 000001ac`b8a59fc8 000001ac`baefcf70 : BthRadioMedia!CBthRadioManager::InvokeOnInstanceChange+0x1d1
1e 00007ffd`721d5240     : 000001ac`c5e29f98 00000017`8afff778 00000000`7ffe0386 000001ac`c06def10 : BthRadioMedia!CBthRadioManager::InvokeAllNotifications+0x10c
1f 00007ffd`721d6291     : 00000000`00000000 00000000`00000000 00007ffd`7223a440 00000000`00000000 : ntdll!TppWorkpExecuteCallback+0x4d0
20 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!TppWorkerThread+0x801
21 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
22 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  47  Id: 10260.c61c Suspend: 0 Teb: 00000017`89660000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`7174b386     : 00000000`00000000 00000000`00000000 00000017`8b7ff710 00000017`8b7ff710 : win32u!NtUserMsgWaitForMultipleObjectsEx+0x14
01 00007ffd`7174a79e     : 00000000`000018f0 00000000`00000000 000001ac`bd283f20 00000000`00000000 : SHCore!WorkThreadManager::CThread::WaitForWork+0x7a
02 00007ffd`71749b57     : 00000000`00000001 00000000`00000000 00000000`00000000 00000000`00000000 : SHCore!WorkThreadManager::CThread::ThreadProc+0xda
03 00007ffd`7012e8d7     : 000001ac`bd283f20 00000000`00000000 00000000`00000000 00000000`00000000 : SHCore!<lambda_9844335fc14345151eefcc3593dd6895>::<lambda_invoker_cdecl>+0x17
04 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
05 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  48  Id: 10260.11394 Suspend: 0 Teb: 00000017`89662000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`6f892533     : 00000000`00000002 00000000`ffffffff 00000000`00000000 000001ac`a4410000 : ntdll!NtWaitForMultipleObjects+0x14
01 00007ffd`70366f3a     : 00000000`00000001 00000000`00000000 00000000`00000001 000001ac`c01b7fc0 : KERNELBASE!WaitForMultipleObjectsEx+0x123
02 00007ffd`70366d74     : 000001ac`c01b7fc0 00000000`00000000 00000000`00000000 000001ac`c01b7fc0 : combase!WaitCoalesced+0xca [onecore\com\published\comutils\coalescedwait.cxx @ 72] 
03 00007ffd`70366b59     : 000001ac`c0284db0 00000000`ffffffff 00000000`00000000 00000000`00000000 : combase!CRpcThread::WorkerLoop+0x120 [onecore\com\combase\dcomrem\threads.cxx @ 329] 
04 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : combase!CRpcThreadCache::RpcWorkerThreadEntry+0x29 [onecore\com\combase\dcomrem\threads.cxx @ 77] 
05 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
06 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  49  Id: 10260.6a7c Suspend: 0 Teb: 00000017`89664000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`721d5e0e     : 00000000`00000002 00000000`00000000 00007ffd`721d7a80 000001ac`a5c82e20 : ntdll!NtWaitForWorkViaWorkerFactory+0x14
01 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!TppWorkerThread+0x37e
02 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
03 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

  50  Id: 10260.1dc8 Suspend: 0 Teb: 00000017`89666000 Unfrozen
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffd`721d5e0e     : 00000000`00000007 00000000`00000000 00007ffd`721d7a80 000001ac`a5c82e20 : ntdll!NtWaitForWorkViaWorkerFactory+0x14
01 00007ffd`7012e8d7     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!TppWorkerThread+0x37e
02 00007ffd`721ec40c     : 00000000`00000000 00000000`00000000 000004f0`fffffb30 000004d0`fffffb30 : kernel32!BaseThreadInitThunk+0x17
03 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2c

```
### Summary

- The freeze occurs when Bluetooth is disabled during an active Digital Credentials transaction.
- ProcDump confirms the browser main thread is blocked while unregistering a radio state listener.
- Another thread simultaneously processes the Bluetooth state change notification while holding the same lock.
- This results in a deadlock and complete browser unresponsiveness.

Please let me know if additional logs, dumps, or reproduction details would be helpful.

Thank you.

### wo...@gmail.com (2026-03-10)

I think this code from `device/bluetooth/bluetooth_adapter_winrt.cc` shows exactly whats happening.

---

# The Stack Trace From chrome Dump

Chrome dump showed the browser thread stuck here:

```
BthRadioMedia!ATL::IConnectionPointImpl::Unadvise
CBthRadioManager::Unadvise
Windows_Devices_Radios!RadioEventListener::remove_StateChanged

```

That means Chromium executed:

```
IRadio::remove_StateChanged(...)

```

which is the WinRT **Bluetooth radio event unsubscribe** call.

---

# The Exact Matching Code:

```
HRESULT hr = radio_->remove_StateChanged(*radio_state_changed_token_);

```

inside:

```
void BluetoothAdapterWinrt::TryRemoveRadioStateChangedHandler()

```

Full snippet:

```
void BluetoothAdapterWinrt::TryRemoveRadioStateChangedHandler() {
  DCHECK(radio_);
  if (!radio_state_changed_token_)
    return;

  HRESULT hr = radio_->remove_StateChanged(*radio_state_changed_token_);
  if (FAILED(hr)) {
    BLUETOOTH_LOG(ERROR) << "Removing Radio State Changed Handler failed: "
                         << logging::SystemErrorCodeToString(hr);
  }

  radio_state_changed_token_.reset();
}

```

This is **exactly the operation the stack trace showed**.

---

# Where That Function Is Called

Look at the destructor:

```
BluetoothAdapterWinrt::~BluetoothAdapterWinrt() {
  if (radio_)
    TryRemoveRadioStateChangedHandler();
}

```

So during cleanup Chromium does:

```
BluetoothAdapterWinrt destructor
↓
TryRemoveRadioStateChangedHandler()
↓
radio_->remove_StateChanged()
↓
Windows radio event system
↓
Unadvise()

```

Which is **exactly the stack i captured**.

---

# Why This Matches the Deadlock

Chrome dump also showed another thread running:

```
RadioEventListener::OnInstanceRadioChange
CBthRadioManager::InvokeAllNotifications

```

So the sequence likely looks like this:

```
Thread A
Bluetooth state change event fires
↓
OnInstanceRadioChange()
↓
InvokeAllNotifications()
↓
holds radio listener lock

```

At the same time:

```
Thread B (browser main thread)
BluetoothAdapterWinrt cleanup
↓
TryRemoveRadioStateChangedHandler()
↓
remove_StateChanged()
↓
needs same lock
↓
deadlock

```

---

# Why my PoC Triggers This

My reproduction sequence:

```
navigator.credentials.get()
↓
Digital Credentials cross-device flow
↓
Bluetooth adapter discovery active
↓
Bluetooth turned OFF
↓
Windows fires radio change event
↓
Chromium tries to remove listener
↓
race condition

```

The **Bluetooth toggle during an active DC transaction** creates the perfect timing window.

---

# The Exact Line That Connects the Dump to the Source

The most telling line in the Chromium source is:

```
radio_->remove_StateChanged(*radio_state_changed_token_);

```

because it directly corresponds to the stack frame:

```
RadioEventListener::remove_StateChanged

```

from chrome dump.

---

# Interesting Subtle Detail

Notice this line:

```
radio_state_changed_token_ = AddTypedEventHandler(...)

```

This means Chromium registers a **WinRT event handler** for radio state changes earlier during initialization.

So the code path is:

```
register event handler
↓
Bluetooth state change
↓
handler invoked
↓
cleanup removes handler
↓
race with event dispatch

```
## That race is exactly what chrome dump suggests.

### wo...@gmail.com (2026-03-10)

sorry forgot to attach the dump.

### ma...@chromium.org (2026-03-11)

I confirm the bug. Thank you for the report!
Although <https://crrev.com/c/7132078> fixed multiple error cases (when the bluetooth permission is denied for example) but, it overlooked one scenario when the Bluetooth adapter gets turned off
during a transaction.

Fix is in review.
<https://crrev.com/c/7656824>

carlosil@ : Could you please assign the proper priority and severity?
This requires the user start a DC flow, and then turn off the Bluetooth adapter which then causes UAF and Chrome to crash immediately.
The DC API is launched but there is almost no usage for it at the moment, especially the cross-device flow.

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  main  

Author:  Mohamed Amir Yosef [mamir@chromium.org](mailto:mamir@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7656824>

[DC] Fix crash when Bluetooth is disabled during a DC flow

---


Expand for full commit details
```
     
    When performing a Digital Credential Request, Chrome crashes if the 
    Bluetooth adapter is powered off while a transaction is in progress. 
    This happens because TransactionImpl (a BluetoothAdapter::Observer) 
    synchronously executes its completion callback upon receiving the 
    AdapterPoweredChanged(false) notification. 
     
    The completion callback synchronously destroys the 
    DigitalIdentityProvider and the TransactionImpl itself. Destroying an 
    observer while the BluetoothAdapter is still iterating over its 
    ObserverList causes a use-after-free or re-entrancy crash. 
     
    This CL fixes the issue by posting a task to execute the completion 
    callback asynchronously, which is the standard pattern for preventing 
    synchronous destruction in observer notifications. 
     
    This is a follow-up to https://crrev.com/c/7132078 which fixed multiple 
    error cases when the bluetooth permission is denied ...etc but 
    overlooked one scenario when the Bluetooth adapter gets turned off 
    during a transaction. 
     
    Fixed: 488617440 
    Change-Id: If78d9d3b5cb8d27b4bcaad48ba8850da2ebae0b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7656824 
    Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org> 
    Reviewed-by: Martin Kreichgauer <martinkr@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1598301}

```

---

Files:

- M `content/browser/digital_credentials/cross_device_transaction_impl.cc`
- M `content/browser/digital_credentials/cross_device_transaction_impl_unittest.cc`

---

Hash: [952d06969915c8e44f9ab6008be6f14f6338901e](https://chromiumdash.appspot.com/commit/952d06969915c8e44f9ab6008be6f14f6338901e)  

Date: Thu Mar 12 09:51:15 2026


---

### wo...@gmail.com (2026-03-12)

Thank you for the quick investigation and fix. I appreciate the detailed explanation in the commit message, it's great to see the asynchronous task posting approach used to safely handle the observer lifecycle during the Bluetooth adapter state change. Thanks again for addressing the issue so quickly.

### ch...@google.com (2026-03-13)

Security Merge Request Consideration: Requesting merge to stable (M146) because latest trunk commit (1598301) appears to be after stable branch point (1582197).
Security Merge Request Consideration: Requesting merge to beta (M147) because latest trunk commit (1598301) appears to be after beta branch point (1596535).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ma...@chromium.org (2026-03-13)

1. Which CLs should be backmerged? (Please include Gerrit links.)
   <https://chromium-review.googlesource.com/7656824>
2. Has this fix been verified on Canary to not pose any stability regressions?
   Yes
3. Does this fix pose any potential non-verifiable stability risks?
   No.
4. Does this fix pose any known compatibility risks?
   No.
5. Does it require manual verification by the test team? If so, please describe required testing.
   (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!
   No. I verified myself.

### ch...@google.com (2026-03-13)

**Merge approved:** your change passed merge requirements and is auto-approved for M147. Please go ahead and merge the CL to branch 7727 (refs/branch-heads/7727) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-03-13)

Merge review required: M146 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dx...@google.com (2026-03-13)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Mohamed Amir Yosef [mamir@chromium.org](mailto:mamir@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7666097>

[DC] Fix crash when Bluetooth is disabled during a DC flow

---


Expand for full commit details
```
     
    When performing a Digital Credential Request, Chrome crashes if the 
    Bluetooth adapter is powered off while a transaction is in progress. 
    This happens because TransactionImpl (a BluetoothAdapter::Observer) 
    synchronously executes its completion callback upon receiving the 
    AdapterPoweredChanged(false) notification. 
     
    The completion callback synchronously destroys the 
    DigitalIdentityProvider and the TransactionImpl itself. Destroying an 
    observer while the BluetoothAdapter is still iterating over its 
    ObserverList causes a use-after-free or re-entrancy crash. 
     
    This CL fixes the issue by posting a task to execute the completion 
    callback asynchronously, which is the standard pattern for preventing 
    synchronous destruction in observer notifications. 
     
    This is a follow-up to https://crrev.com/c/7132078 which fixed multiple 
    error cases when the bluetooth permission is denied ...etc but 
    overlooked one scenario when the Bluetooth adapter gets turned off 
    during a transaction. 
     
    (cherry picked from commit 952d06969915c8e44f9ab6008be6f14f6338901e) 
     
    Fixed: 488617440 
    Change-Id: If78d9d3b5cb8d27b4bcaad48ba8850da2ebae0b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7656824 
    Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org> 
    Reviewed-by: Martin Kreichgauer <martinkr@google.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1598301} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666097 
    Auto-Submit: Mohamed Amir Yosef <mamir@chromium.org> 
    Commit-Queue: Rafał Godlewski <rgod@google.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Reviewed-by: Rafał Godlewski <rgod@google.com> 
    Cr-Commit-Position: refs/branch-heads/7727@{#229} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `content/browser/digital_credentials/cross_device_transaction_impl.cc`
- M `content/browser/digital_credentials/cross_device_transaction_impl_unittest.cc`

---

Hash: [50b2f565dbb343446cdb528c2d6dc6d4ea91dbb7](https://chromiumdash.appspot.com/commit/50b2f565dbb343446cdb528c2d6dc6d4ea91dbb7)  

Date: Fri Mar 13 11:18:28 2026


---

### pe...@google.com (2026-03-13)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### dr...@chromium.org (2026-03-15)

Approved to merge to M146.

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Mohamed Amir Yosef [mamir@chromium.org](mailto:mamir@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7665928>

[M146][DC] Fix crash when Bluetooth is disabled during a DC flow

---


Expand for full commit details
```
     
    When performing a Digital Credential Request, Chrome crashes if the 
    Bluetooth adapter is powered off while a transaction is in progress. 
    This happens because TransactionImpl (a BluetoothAdapter::Observer) 
    synchronously executes its completion callback upon receiving the 
    AdapterPoweredChanged(false) notification. 
     
    The completion callback synchronously destroys the 
    DigitalIdentityProvider and the TransactionImpl itself. Destroying an 
    observer while the BluetoothAdapter is still iterating over its 
    ObserverList causes a use-after-free or re-entrancy crash. 
     
    This CL fixes the issue by posting a task to execute the completion 
    callback asynchronously, which is the standard pattern for preventing 
    synchronous destruction in observer notifications. 
     
    This is a follow-up to https://crrev.com/c/7132078 which fixed multiple 
    error cases when the bluetooth permission is denied ...etc but 
    overlooked one scenario when the Bluetooth adapter gets turned off 
    during a transaction. 
     
    (cherry picked from commit 952d06969915c8e44f9ab6008be6f14f6338901e) 
     
    Fixed: 488617440 
    Change-Id: If78d9d3b5cb8d27b4bcaad48ba8850da2ebae0b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7656824 
    Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org> 
    Reviewed-by: Martin Kreichgauer <martinkr@google.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1598301} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665928 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2647} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `content/browser/digital_credentials/cross_device_transaction_impl.cc`
- M `content/browser/digital_credentials/cross_device_transaction_impl_unittest.cc`

---

Hash: [ece57e3e74e2531296978a9257417a410e1a3166](https://chromiumdash.appspot.com/commit/ece57e3e74e2531296978a9257417a410e1a3166)  

Date: Mon Mar 16 11:15:53 2026


---

### pe...@google.com (2026-03-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-17)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7665600>
2. Medium - The target files were moved from `//content/browser/webid` to `//content/browser/digitial_credentials`. So, I needed to adjust the changes manually.
3. 146
4. Yes, In M138, `cross_device_transaction_impl.cc` and `cross_device_transaction_impl_unittest.cc` were located in `//content/browser/webid/digital_credentials`, but the issue existed in M138 because it has the suspected code in the files.

### pe...@google.com (2026-03-18)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-18)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7673041
2. Low - There was no conflict.
3. 146
4. Yes, M144 has the problem codes as well.

### wf...@chromium.org (2026-03-18)

this requires unusual user interactions which mitigates this somewhat significantly - bumping it down to (at most) sev-high for this.

### wf...@chromium.org (2026-03-18)

(it might even be sev-medium since turning off Bluetooth is such an unusual interaction and it must race the exploit)

### wo...@gmail.com (2026-03-18)

Thank you for the review and discussion around exploitability.

I would like to provide additional technical clarification regarding the interaction requirement and why I believe this issue may still meet S0 criteria.

While the trigger involves powering off Bluetooth during a Digital Credential (DC) flow, the vulnerability itself is:

A deterministic browser-process heap use-after-free

Reachable from a renderer-initiated API flow

Occurring in a non-sandboxed process

Triggered during synchronous ObserverList iteration

# 1: The Interaction Is Not a Strong Security Boundary

Turning off Bluetooth is:

A single OS-level toggle

Does not require special privileges

Does not require granting new permissions

Does not require navigating away or complex UI interaction

From an exploitation modeling perspective, this resembles:

Inducing network disconnect

Closing a lid

Changing adapter state

These are state transitions, not privileged security gates.

Chrome security guidance historically treats “simple user state changes” differently from:

Download + open

Install extension

Grant dangerous permission

Multi-step gesture chains

The DC flow itself is renderer-triggerable. The Bluetooth state change merely advances execution into the vulnerable path.

---

# 2: The Race Characterization

The vulnerability occurs because:

TransactionImpl (BluetoothAdapter::Observer)
→ receives AdapterPoweredChanged(false)
→ synchronously executes completion callback
→ destroys itself during ObserverList iteration

This is not a probabilistic heap race.

The destruction occurs synchronously inside the notification call stack.

As long as Bluetooth is powered off during the transaction window, the UAF is reliably triggered.

This is structurally similar to past high-severity Chromium observer lifetime bugs.

# 3: Exploitability Characteristics

The bug provides:

Browser process heap corruption

Use-after-free on a C++ object with virtual methods

Occurring during controlled renderer → browser transition

In a process without sandbox containment

Even if interaction is required, once triggered, the primitive is a classic lifetime violation with known historical exploitability patterns.

Interaction does not meaningfully constrain exploitation from a determined attacker model.

### wo...@gmail.com (2026-03-19)

Hi team,

Just a friendly follow-up regarding the reward review for this report. Since the issue was fixed 7 days ago, I wanted to check whether there are any updates on the bounty processing timeline.

Thanks for the quick fix.

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Moderately mitigated memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### wo...@gmail.com (2026-03-20)

Hello VRP Team,

Thank you for reviewing the report and for the award decision. I appreciate the time spent evaluating the issue.

I would like to respectfully request reconsideration of the reward classification, specifically regarding the “moderately mitigated” assessment.

While the issue does require a Bluetooth state change during an active Digital Credential transaction, I believe the mitigation impact may have been overstated for the following technical reasons:

1. Renderer → Browser Memory Corruption:
   The vulnerability is reachable from renderer-controlled flow and results in a heap use-after-free in the browser process (non-sandboxed). This crosses a major security boundary and corrupts high-privilege memory.
2. Deterministic Lifetime Violation (Not a Random Race):
   The bug is not a speculative timing issue but a structural observer re-entrancy flaw. The completion callback synchronously destroys the observing object during "ObserverList" iteration. This is a well-known unsafe pattern that has historically led to exploitable conditions when heap grooming is applied.
3. User Interaction Characterization:
   Turning off Bluetooth during an active credential transaction may be considered uncommon, but it is not security-hardening or a true mitigation barrier. It does not require elevated privileges, special configuration, or non-standard hardware. From an exploitation modeling perspective, it is a device state transition, not a security boundary.
4. Exploitability Surface:
   Because destruction occurs synchronously inside the adapter notification loop, the freed object remains reachable during continued iteration. This creates a classical browser-process UAF scenario where heap reallocation strategies could potentially influence post-free behavior.

Given that this is memory corruption in a non-sandboxed process, reachable via renderer-triggered flow, and involving deterministic object lifetime mismanagement, I believe it may align more closely with high-severity memory corruption rather than a moderately mitigated classification.

### an...@google.com (2026-03-27)

Approved for M138 and M144

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Mohamed Amir Yosef [mamir@chromium.org](mailto:mamir@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7673041>

[M144-LTS][DC] Fix crash when Bluetooth is disabled during a DC flow

---


Expand for full commit details
```
     
    When performing a Digital Credential Request, Chrome crashes if the 
    Bluetooth adapter is powered off while a transaction is in progress. 
    This happens because TransactionImpl (a BluetoothAdapter::Observer) 
    synchronously executes its completion callback upon receiving the 
    AdapterPoweredChanged(false) notification. 
     
    The completion callback synchronously destroys the 
    DigitalIdentityProvider and the TransactionImpl itself. Destroying an 
    observer while the BluetoothAdapter is still iterating over its 
    ObserverList causes a use-after-free or re-entrancy crash. 
     
    This CL fixes the issue by posting a task to execute the completion 
    callback asynchronously, which is the standard pattern for preventing 
    synchronous destruction in observer notifications. 
     
    This is a follow-up to https://crrev.com/c/7132078 which fixed multiple 
    error cases when the bluetooth permission is denied ...etc but 
    overlooked one scenario when the Bluetooth adapter gets turned off 
    during a transaction. 
     
    (cherry picked from commit 952d06969915c8e44f9ab6008be6f14f6338901e) 
     
    (cherry picked from commit 50b2f565dbb343446cdb528c2d6dc6d4ea91dbb7) 
     
    Fixed: 488617440 
    Change-Id: If78d9d3b5cb8d27b4bcaad48ba8850da2ebae0b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7656824 
    Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org> 
    Reviewed-by: Martin Kreichgauer <martinkr@google.com> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1598301} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666097 
    Auto-Submit: Mohamed Amir Yosef <mamir@chromium.org> 
    Commit-Queue: Rafał Godlewski <rgod@google.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Reviewed-by: Rafał Godlewski <rgod@google.com> 
    Cr-Original-Commit-Position: refs/branch-heads/7727@{#229} 
    Cr-Original-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673041 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4820} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `content/browser/digital_credentials/cross_device_transaction_impl.cc`
- M `content/browser/digital_credentials/cross_device_transaction_impl_unittest.cc`

---

Hash: [6e4fcceab5549d48fa8f8ead2d2e6270b201d653](https://chromiumdash.appspot.com/commit/6e4fcceab5549d48fa8f8ead2d2e6270b201d653)  

Date: Thu Apr 16 04:35:39 2026


---

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Gyuyoung Kim [qkim@google.com](mailto:qkim@google.com)  

Link:    <https://chromium-review.googlesource.com/7665600>

[M138-LTS][DC] Fix crash when Bluetooth is disabled during a DC flow

---


Expand for full commit details
```
     
    When performing a Digital Credential Request, Chrome crashes if the 
    Bluetooth adapter is powered off while a transaction is in progress. 
    This happens because TransactionImpl (a BluetoothAdapter::Observer) 
    synchronously executes its completion callback upon receiving the 
    AdapterPoweredChanged(false) notification. 
     
    The completion callback synchronously destroys the 
    DigitalIdentityProvider and the TransactionImpl itself. Destroying an 
    observer while the BluetoothAdapter is still iterating over its 
    ObserverList causes a use-after-free or re-entrancy crash. 
     
    This CL fixes the issue by posting a task to execute the completion 
    callback asynchronously, which is the standard pattern for preventing 
    synchronous destruction in observer notifications. 
     
    This is a follow-up to https://crrev.com/c/7132078 which fixed multiple 
    error cases when the bluetooth permission is denied ...etc but 
    overlooked one scenario when the Bluetooth adapter gets turned off 
    during a transaction. 
     
    (cherry picked from commit 952d06969915c8e44f9ab6008be6f14f6338901e) 
     
    (cherry picked from commit 50b2f565dbb343446cdb528c2d6dc6d4ea91dbb7) 
     
    Fixed: 488617440 
    Change-Id: If78d9d3b5cb8d27b4bcaad48ba8850da2ebae0b5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7656824 
    Commit-Queue: Mohamed Amir Yosef <mamir@chromium.org> 
    Reviewed-by: Martin Kreichgauer <martinkr@google.com> 
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1598301} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666097 
    Auto-Submit: Mohamed Amir Yosef <mamir@chromium.org> 
    Commit-Queue: Rafał Godlewski <rgod@google.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Reviewed-by: Rafał Godlewski <rgod@google.com> 
    Cr-Original-Commit-Position: refs/branch-heads/7727@{#229} 
    Cr-Original-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7665600 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Reviewed-by: Mohamed Amir Yosef <mamir@chromium.org> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3540} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `content/browser/webid/digital_credentials/cross_device_transaction_impl.cc`
- M `content/browser/webid/digital_credentials/cross_device_transaction_impl_unittest.cc`

---

Hash: [2124bed238b98fa5e6db4563643f5f980c971261](https://chromiumdash.appspot.com/commit/2124bed238b98fa5e6db4563643f5f980c971261)  

Date: Thu Apr 16 04:41:57 2026


---

### wo...@gmail.com (2026-04-17)

Hello [mamir@chromium.org](mailto:mamir@chromium.org), kindly check this report. its a regression to this report. the crash still occurs. <https://issues.chromium.org/issues/503763493>

Key : Analysis.Memory.CommitPeak.Mb
Value: 1725

```
Key  : Analysis.Version.DbgEng
Value: 10.0.29547.1002

Key  : Analysis.Version.Description
Value: 10.2602.27.2 amd64fre

Key  : Analysis.Version.Ext
Value: 1.2602.27.2

Key  : Failure.Bucket
Value: BREAKPOINT_80000003_BthRadioMedia.dll!ATL::IConnectionPointImpl_CBthRadioManager,_IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray_::Unadvise

Key  : Failure.Exception.Code
Value: 0x80000003

Key  : Failure.Hash
Value: {63fbc647-1b3c-4f88-e831-a46bf0c108a4}

Key  : Failure.ProblemClass.Primary
Value: BREAKPOINT

Key  : Faulting.IP.Type
Value: Null

Key  : Timeline.OS.Boot.DeltaSec
Value: 14002

Key  : Timeline.Process.Start.DeltaSec
Value: 865

Key  : WER.OS.Branch
Value: vb_release

Key  : WER.OS.Version
Value: 10.0.19041.1

Key  : WER.Process.Version
Value: 149.0.7793.0

```

FILE\_IN\_CAB: chrome.exe\_260417\_181508.dmp

COMMENT:  

\*\*\* procdump -ma 3824
\*\*\* Manual dump

NTGLOBALFLAG: 0

APPLICATION\_VERIFIER\_FLAGS: 0

EXCEPTION\_RECORD: (.exr -1)
ExceptionAddress: 0000000000000000
ExceptionCode: 80000003 (Break instruction exception)
ExceptionFlags: 00000000
NumberParameters: 0

FAULTING\_THREAD: 1354

PROCESS\_NAME: chrome.exe

ERROR\_CODE: (NTSTATUS) 0x80000003 - {EXCEPTION} Breakpoint A breakpoint has been reached.

EXCEPTION\_CODE\_STR: 80000003

CRITICAL\_SECTION: 0000116226cea180 -- (!cs -s 0000116226cea180)

BLOCKING\_THREAD: 269a36d0

STACK\_TEXT:  

00000030`7cbfdca8 00007ffc`432f38ad : 000011b6`28199b20 000011b6`27d6c9c0 0000113c`288130f0 0000113e`2a9c7a68 : ntdll!NtWaitForAlertByThreadId+0x14
00000030`7cbfdcb0 00007ffc`432f3762 : 00000000`00000000 00000000`00000000 00000030`7cbfdd98 000011b6`27cf5738 : ntdll!RtlpWaitOnAddressWithTimeout+0x81
00000030`7cbfdce0 00007ffc`432f357d : 000011b6`27cf5730 00000000`00001722 00000000`00000000 00001162`26cea3b0 : ntdll!RtlpWaitOnAddress+0xae
00000030`7cbfdd50 00007ffc`432bfcb4 : 00000136`26980000 00000236`c4fdae60 00000000`fffffffa 00001162`26cea180 : ntdll!RtlpWaitOnCriticalSection+0xfd
00000030`7cbfde30 00007ffc`432bfae2 : 000011b6`27ed7300 000011b6`27ed7280 00000000`00000001 00007ffc`290d7d6e : ntdll!RtlpEnterCriticalSectionContended+0x1c4
00000030`7cbfde90 00007ffc`290dee50 : 0000078f`35bc37b3 00001162`26cea180 00001162`26cea320 00001150`27395cf8 : ntdll!RtlEnterCriticalSection+0x42
00000030`7cbfdec0 00007ffc`290def50 : 000011b6`27cf5708 00001150`27395cb0 000011b6`280bce00 00000000`00000000 : BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID\_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Unadvise+0x34
00000030`7cbfdef0 00007ffc`3045640d : 00000000`00000000 00000000`00000000 00001150`27395d10 000011b6`280bce00 : BthRadioMedia!CBthRadioManager::Unadvise+0x50
00000030`7cbfdf30 00007ffc`30457faf : 000011b6`27cf5708 00000000`00000000 00000000`00000000 00000000`00000000 : Windows\_Devices\_Radios!RadioEventListener::UnregisterListener+0x49
00000030`7cbfdf60 00007ffb`c7c64b48 : 00001150`27395d10 00000030`7cbfdfc0 00000030`7cbfdff0 00000030`7cbfe010 : Windows\_Devices\_Radios!RadioImpl::remove\_StateChanged+0xcf
00000030`7cbfdfa0 00007ffb`c7c63cd9 : 00000030`7cbfe120 0000113e`27242c90 00000236`c4ffffa0 000011b6`27fffd00 : chrome!device::BluetoothAdapterWinrt::TryRemoveRadioStateChangedHandler+0x178
00000030`7cbfe040 00007ffb`c7c8f240 : 00000030`7cbfd930 00000000`00000000 00001162`26cea188 00001162`26cea180 : chrome!device::BluetoothAdapterWinrt::~BluetoothAdapterWinrt+0x1e9
00000030`7cbfe170 00007ffb`c8bff18c : 0000113a`2a2ed550 0000113a`2a2ed558 00000030`7cbfe238 00000136`26980000 : chrome!device::BluetoothAdapterWinrt::~BluetoothAdapterWinrt+0x10
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::RefCounted<device::BluetoothAdapter,base::DefaultRefCountedTraits<device::BluetoothAdapter> >::DeleteInternal+0x36 (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::DefaultRefCountedTraits[device::BluetoothAdapter](javascript:void(0);)::Destruct+0x36
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::RefCounted<device::BluetoothAdapter,base::DefaultRefCountedTraits<device::BluetoothAdapter> >::Release+0x5d (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!scoped\_refptr[device::BluetoothAdapter](javascript:void(0);)::Release+0x5d
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!scoped_refptr<device::BluetoothAdapter>::~scoped_refptr+0x80 00000030`7cbfe1b0 00007ffb`c8c067b0 : 00000000`00000001 00001152`3bfa03e0 000011b6`27fffc40 000011b6`28199128 : chrome!device::cablev2::Discovery::~Discovery+0x2ac 00000030`7cbfe210 00007ffb`b777e66c : 00000030`7cbfe430 00001156`28bb31e0 00001162`26cea188 00001162`26cea180 : chrome!device::cablev2::Discovery::~Discovery+0x10 (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::\_\_Cr::default\_delete[device::FidoDiscoveryBase](javascript:void(0);)::operator()+0x24
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<device::FidoDiscoveryBase,std::__Cr::default_delete<device::FidoDiscoveryBase> >::reset+0x40 (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::\_\_Cr::unique\_ptr<device::FidoDiscoveryBase,std::\_\_Cr::default\_delete[device::FidoDiscoveryBase](javascript:void(0);) >::~unique\_ptr+0x40
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!content::digital_credentials::cross_device::RequestDispatcher::~RequestDispatcher+0x92 00000030`7cbfe250 00007ffb`b778143c : 00000000`00000040 00007ffb`eadf9d20 00000136`26980000 000011b6`27d6c2e0 : chrome!content::digital_credentials::cross_device::RequestDispatcher::~RequestDispatcher+0x9c (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::\_\_Cr::default\_delete[content::digital\_credentials::cross\_device::RequestDispatcher](javascript:void(0);)::operator()+0x2e
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<content::digital_credentials::cross_device::RequestDispatcher,std::__Cr::default_delete<content::digital_credentials::cross_device::RequestDispatcher> >::reset+0x4f (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::\_\_Cr::unique\_ptr<content::digital\_credentials::cross\_device::RequestDispatcher,std::\_\_Cr::default\_delete[content::digital\_credentials::cross\_device::RequestDispatcher](javascript:void(0);) >::~unique\_ptr+0x4f
00000030`7cbfe290 00007ffb`b7785970 : 000011b6`28199100 00000136`26980000 00000000`00000001 00001158`2ba7fd80 : chrome!content::digital\_credentials::cross\_device::TransactionImpl::~TransactionImpl+0x18c
00000030`7cbfe2e0 00007ffb`bdb42206 : 000011b6`28199000 000011b6`28199240 000011b6`27d6c400 00007ffb`eadfaba7 : chrome!content::digital\_credentials::cross\_device::TransactionImpl::~TransactionImpl+0x10
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::default_delete<content::digital_credentials::cross_device::Transaction>::operator()+0x24 (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::\_\_Cr::unique\_ptr<content::digital\_credentials::cross\_device::Transaction,std::\_\_Cr::default\_delete[content::digital\_credentials::cross\_device::Transaction](javascript:void(0);) >::reset+0x40
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<content::digital_credentials::cross_device::Transaction,std::__Cr::default_delete<content::digital_credentials::cross_device::Transaction> >::~unique_ptr+0x40 00000030`7cbfe320 00007ffb`bdb4abf0 : 00000136`26980000 0000114c`2da15980 000011b6`27fffba0 000011b6`28199100 : chrome!DigitalIdentityProviderDesktop::~DigitalIdentityProviderDesktop+0x106 00000030`7cbfe360 00007ffb`b61f3632 : 0000113e`269a36d0 00000236`c4fad858 00000030`7cbfe410 00007ffb`c080ca5d : chrome!DigitalIdentityProviderDesktop::~DigitalIdentityProviderDesktop+0x10 (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::\_\_Cr::default\_delete[content::DigitalIdentityProvider](javascript:void(0);)::operator()+0x30
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!std::__Cr::unique_ptr<content::DigitalIdentityProvider,std::__Cr::default_delete<content::DigitalIdentityProvider> >::reset+0x58 00000030`7cbfe3a0 00007ffb`b61f329e : 000011b6`27fd7768 00007ffb`eae1b419 000011b6`27d07000 00000030`7cbfe4f0 : chrome!content::DigitalIdentityRequestImpl::CompleteRequestWithStatus+0x202 00000030`7cbfe480 00007ffb`b61fa9a0 : 000011b6`27edf880 00000136`2654f188 000011b6`27ed7028 000011b6`27ed7020 : chrome!content::DigitalIdentityRequestImpl::CompleteRequest+0x19e 00000030`7cbfe520 00007ffb`b61fa714 : 00000fff`7d3053b8 00007ffb`eae1b419 000011b6`27d07000 0000113c`291cdcd0 : chrome!base::internal::DecayedFunctorTraits<void (content::DigitalIdentityRequestImpl::*)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> &&>::Invoke<void (content::DigitalIdentityRequestImpl::*)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),const base::WeakPtr<content::DigitalIdentityRequestImpl> &,base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics> >+0x1e0 (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::internal::InvokeHelper<1,base::internal::FunctorTraits<void (content::DigitalIdentityRequestImpl::\*&&)(base::expected[content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics](javascript:void(0);)),base::WeakPtr[content::DigitalIdentityRequestImpl](javascript:void(0);) &&>,void,0>::MakeItSo+0x64
(Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::internal::Invoker<base::internal::FunctorTraits<void (content::DigitalIdentityRequestImpl::*&&)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> &&>,base::internal::BindState<1,1,0,void (content::DigitalIdentityRequestImpl::*)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> >,void (base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>)>::RunImpl+0x7e 00000030`7cbfe5e0 00007ffb`bdb45ec8 : 00001160`269a2898 0000113a`269a0d90 00000030`7cbfe6f0 00007ffb`c087edcf : chrome!base::internal::Invoker<base::internal::FunctorTraits<void (content::DigitalIdentityRequestImpl::*&&)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> &&>,base::internal::BindState<1,1,0,void (content::DigitalIdentityRequestImpl::*)(base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>),base::WeakPtr<content::DigitalIdentityRequestImpl> >,void (base::expected<content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics>)>::RunOnce+0x144 (Inline Function) --------`-------- : --------`-------- --------`-------- --------`-------- --------`-------- : chrome!base::OnceCallback<void (base::expected[content::DigitalIdentityProvider::DigitalCredential,content::DigitalIdentityProvider::RequestStatusForMetrics](javascript:void(0);))>::Run+0x8f
00000030`7cbfe680 00007ffb`bdb437e8 : 000011b6`27edf380 000011b6`27edf3a0 00000030`7cbfe7a0 00000030`7cbfe7a0 : chrome!DigitalIdentityProviderDesktop::EndRequestWithError+0x228
00000030`7cbfe740 00007ffb`bdb49802 : 00000136`26980000 00000026`c4ca9e31 000011b6`27ee01b0 000011b6`27ee0280 : chrome!DigitalIdentityProviderDesktop::OnFinished+0x218

STACK\_COMMAND: ~0s; .ecxr ; kb

SYMBOL\_NAME: BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID\_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Unadvise+34

MODULE\_NAME: BthRadioMedia

IMAGE\_NAME: BthRadioMedia.dll

FAILURE\_BUCKET\_ID: BREAKPOINT\_80000003\_BthRadioMedia.dll!ATL::IConnectionPointImpl\_CBthRadioManager,*IID\_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray*::Unadvise

OS\_VERSION: 10.0.19041.1

BUILDLAB\_STR: vb\_release

OSPLATFORM\_TYPE: x64

OSNAME: Windows 10

IMAGE\_VERSION: 6.2.19041.746

FAILURE\_ID\_HASH: {63fbc647-1b3c-4f88-e831-a46bf0c108a4}

## Followup: MachineOwner

## 0:000> !cs -s 0000116226cea180

Critical section = 0x0000116226cea180 (+0x116226CEA180)
DebugInfo = 0x00007ffbe317d080
LOCKED
LockCount = 0xFFFFFFFF
WaiterWoken = Yes
OwningThread = 0x0000113e269a36d0
RecursionCount = 0xBEBEBEBE
LockSemaphore = 0x2A2ED550
SpinCount = 0x0000113a2a2ed550
ntdll!RtlpStackTraceDataBase is NULL. Probably the stack traces are not enabled.
0:000> lmvm BthRadioMedia
Browse full module list
start end module name
00007ffc`290d0000 00007ffc`290ef000 BthRadioMedia (pdb symbols) C:\ProgramData\Dbg\sym\BthRadioMedia.pdb\0BD64DF67BB251C018DE698325D4CED81\BthRadioMedia.pdb
Loaded symbol image file: BthRadioMedia.dll
Image path: C:\Windows\System32\BthRadioMedia.dll
Image name: BthRadioMedia.dll
Browse all global symbols functions data Symbol Reload
Image was built with /Brepro flag.
Timestamp: CD2FAD7E (This is a reproducible build file hash, not a timestamp)
CheckSum: 0001C4FF
ImageSize: 0001F000
Mapping Form: Loaded
File version: 6.2.19041.746
Product version: 10.0.19041.746
File flags: 0 (Mask 3F)
File OS: 40004 NT Win32
File type: 2.0 Dll
File date: 00000000.00000000
Translations: 0409.04b0
Information from resource tables:
CompanyName: Microsoft Corporation
ProductName: Microsoft® Windows® Operating System
InternalName: BTHRADIOMEDIA
OriginalFilename: BTHRADIOMEDIA.dll
ProductVersion: 10.0.19041.746
FileVersion: 10.0.19041.746 (WinBuild.160101.0800)
FileDescription: Bluetooth Radio Media Provider
LegalCopyright: © Microsoft Corporation. All rights reserved.
0:000> .exr -1
ExceptionAddress: 0000000000000000
ExceptionCode: 80000003 (Break instruction exception)
ExceptionFlags: 00000000
NumberParameters: 0
0:000> x /D /d BthRadioMedia!a\*
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

00007ffc`290e2aa0 BthRadioMedia!ATL::CComClassFactory::`vftable' = <no type information>
00007ffc`290e2d70 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`vftable' = <no type information>
00007ffc`290e2cf0 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::`vftable' = <no type information>
00007ffc`290e9a50 BthRadioMedia!ATL::_AtlBaseModule = <no type information> 00007ffc`290e2ac8 BthRadioMedia!ATL::CComObjectCached[ATL::CComClassFactory](javascript:void(0);)::`vftable' = <no type information> 00007ffc`290e9b50 BthRadioMedia!ATL::g\_strmgr = <no type information>
00007ffc`290e2b70 BthRadioMedia!ATL::CWin32Heap::`vftable' = <no type information>
00007ffc`290e9120 BthRadioMedia!ATL::CAtlException` RTTI Type Descriptor' = <no type information>
00007ffc`290e2e28 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::`vftable' = <no type information>
00007ffc`290e2e50 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::`vftable' = <no type information>
00007ffc`290e9ce0 BthRadioMedia!ATL::_pPerfRegFunc = <no type information> 00007ffc`290e2ea8 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::`vftable' = <no type information> 00007ffc`290e9ab0 BthRadioMedia!ATL::\_AtlWinModule = <no type information>
00007ffc`290e9a00 BthRadioMedia!ATL::_AtlComModule = <no type information> 00007ffc`290e9b38 BthRadioMedia!ATL::g\_strheap = <no type information>
00007ffc`290e2d98 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`vftable' = <no type information>
00007ffc`290e9980 BthRadioMedia!ATL::CAtlBaseModule::m_bInitFailed = <no type information> 00007ffc`290e9ce8 BthRadioMedia!ATL::\_pPerfUnRegFunc = <no type information>
00007ffc`290e2dd8 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`vftable' = <no type information>
00007ffc`290e99a0 BthRadioMedia!ATL::IConnectionPointContainerImpl<CBthRadioManager>::pConnMap = <no type information> 00007ffc`290e2b40 BthRadioMedia!ATL::CAtlStringMgr::`vftable' = <no type information> 00007ffc`290e2d30 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::`vftable' = <no type information> 00007ffc`290e9978 BthRadioMedia!ATL::\_pAtlModule = <no type information>
0:000> x /D /f BthRadioMedia!a\*
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

00007ffc`290d5d64 BthRadioMedia!ATL::AtlFindExtension (void) 00007ffc`290d3ce0 BthRadioMedia!ATL::`dynamic atexit destructor for '_AtlBaseModule'' (void) 00007ffc`290d3d00 BthRadioMedia!ATL::`dynamic atexit destructor for 'g_strheap'' (void) 00007ffc`290d3cd0 BthRadioMedia!ATL::`dynamic atexit destructor for '_AtlComModule'' (void) 00007ffc`290d3d10 BthRadioMedia!ATL::`dynamic atexit destructor for 'g_strmgr'' (void) 00007ffc`290d11c0 BthRadioMedia!ATL::`dynamic initializer for '_AtlBaseModule'' (void) 00007ffc`290d11e0 BthRadioMedia!ATL::`dynamic initializer for '_AtlWinModule'' (void) 00007ffc`290d11a0 BthRadioMedia!ATL::`dynamic initializer for '_AtlComModule'' (void) 00007ffc`290d3cf0 BthRadioMedia!ATL::`dynamic atexit destructor for '_AtlWinModule'' (void) 00007ffc`290d1240 BthRadioMedia!ATL::`dynamic initializer for 'g_strmgr'' (void) 00007ffc`290d1200 BthRadioMedia!ATL::`dynamic initializer for 'g_strheap'' (void) 00007ffc`290d7af0 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::QueryInterface (public: virtual long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::QueryInterface(struct \_GUID const &,void \* \*))
00007ffc`290d7030 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::EnumConnections (public: virtual long __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::EnumConnections(struct IEnumConnections * *)) 00007ffc`290d5dc8 BthRadioMedia!ATL::AtlHresultFromLastError (long \_\_cdecl ATL::AtlHresultFromLastError(void))
00007ffc`290d37e0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::AddRef ([thunk]:public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioManager>::AddRef`adjustor{32}' (void))
00007ffc`290d65c0 BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA> >::Clone (public: virtual long __cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA> >::Clone(struct IEnumConnections * *)) 00007ffc`290d8148 BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA> >::Skip (public: virtual long \_\_cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA> >::Skip(unsigned long))
00007ffc`290d7574 BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> >::Init (public: long __cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >::Init(struct IConnectionPoint * *,struct IConnectionPoint * *,struct IUnknown *,enum ATL::CComEnumFlags)) 00007ffc`290d5ac0 BthRadioMedia!ATL::CComObjectCached[ATL::CComClassFactory](javascript:void(0);)::AddRef (public: virtual unsigned long \_\_cdecl ATL::CComObjectCached<class ATL::CComClassFactory>::AddRef(void))
00007ffc`290d12a0 BthRadioMedia!ATL::CAtlModule::Lock (public: virtual long __cdecl ATL::CAtlModule::Lock(void)) 00007ffc`290d52dc BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::~CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> (public: virtual \_\_cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::~CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>(void))
00007ffc`290d37f0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::QueryInterface ([thunk]:public: virtual long __cdecl ATL::CComObject<class CBthRadioManager>::QueryInterface`adjustor{32}' (struct \_GUID const &,void \* \*))
00007ffc`290d1320 BthRadioMedia!ATL::CAtlStringMgr::Clone (public: virtual struct ATL::IAtlStringMgr * __cdecl ATL::CAtlStringMgr::Clone(void)) 00007ffc`290d9ab4 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::~CSimpleStringT<unsigned short,0> (public: \_\_cdecl ATL::CSimpleStringT<unsigned short,0>::~CSimpleStringT<unsigned short,0>(void))
00007ffc`290d84cc BthRadioMedia!ATL::_Copy<tagCONNECTDATA>::destroy (public: static void __cdecl ATL::_Copy<struct tagCONNECTDATA>::destroy(struct tagCONNECTDATA *)) 00007ffc`290d67f8 BthRadioMedia!ATL::CComCreator<ATL::CComObject<CBthRadioManager> >::CreateInstance (public: static long \_\_cdecl ATL::CComCreator<class ATL::CComObject<class CBthRadioManager> >::CreateInstance(void \*,struct \_GUID const &,void \* \*))
00007ffc`290d7820 BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> >::Next (public: virtual long __cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >::Next(unsigned long,struct IConnectionPoint * *,unsigned long *)) 00007ffc`290de310 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::QueryInterface (public: virtual long \_\_cdecl ATL::CComObject<class CBthRadioInstance>::QueryInterface(struct \_GUID const &,void \* \*))
00007ffc`290d9c44 BthRadioMedia!ATL::AtlFindStringResourceInstance (struct HINSTANCE__ * __cdecl ATL::AtlFindStringResourceInstance(unsigned int,unsigned short)) 00007ffc`290e1840 BthRadioMedia!ATL::CAtlStringMgr::Free (public: virtual void \_\_cdecl ATL::CAtlStringMgr::Free(struct ATL::CStringData \*))
00007ffc`290d5270 BthRadioMedia!ATL::CComPtrBase<IUnknown>::CComPtrBase<IUnknown> (protected: __cdecl ATL::CComPtrBase<struct IUnknown>::CComPtrBase<struct IUnknown>(struct IUnknown *)) 00007ffc`290d98b4 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > > (public: \_\_cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >(unsigned short const \*))
00007ffc`290dbd10 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::`vector deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class CBthRadioInstance>::`vector deleting destructor'(unsigned int)) 00007ffc`290d84cc BthRadioMedia!ATL::\_CopyInterface<IConnectionPoint>::destroy (public: static void \_\_cdecl ATL::\_CopyInterface<struct IConnectionPoint>::destroy(struct IConnectionPoint \* \*))
00007ffc`290d9cf0 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::CheckImplicitLoad (private: bool __cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::CheckImplicitLoad(void const *)) 00007ffc`290d630c BthRadioMedia!ATL::AtlThrowImpl (void \_\_cdecl ATL::AtlThrowImpl(long))
00007ffc`290d3450 BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::Reset (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::Reset(void)) 00007ffc`290d1330 BthRadioMedia!ATL::CAtlStringMgr::GetNilString (public: virtual struct ATL::CStringData \* \_\_cdecl ATL::CAtlStringMgr::GetNilString(void))
00007ffc`290d6c9c BthRadioMedia!ATL::CRegKey::DeleteSubKey (public: long __cdecl ATL::CRegKey::DeleteSubKey(unsigned short const *)) 00007ffc`290d9874 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::CSimpleStringT<unsigned short,0> (public: \_\_cdecl ATL::CSimpleStringT<unsigned short,0>::CSimpleStringT<unsigned short,0>(struct ATL::IAtlStringMgr \*))
00007ffc`290d632c BthRadioMedia!ATL::AtlUnRegisterTypeLib (long __cdecl ATL::AtlUnRegisterTypeLib(struct HINSTANCE__ *,unsigned short const *)) 00007ffc`290d5a40 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::AddRef (public: virtual unsigned long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::AddRef(void))
00007ffc`290de420 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::QueryInterface (public: virtual long __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::QueryInterface(struct _GUID const &,void * *)) 00007ffc`290d7738 BthRadioMedia!ATL::CComCriticalSection::Init (public: long \_\_cdecl ATL::CComCriticalSection::Init(void))
00007ffc`290d9af8 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::operator= (public: class ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > > & __cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::operator=(char const *)) 00007ffc`290d1280 BthRadioMedia!ATL::CComCoClass<CBthRadioManager,&CLSID\_BthRadioManager>::GetObjectDescription (public: static unsigned short const \* \_\_cdecl ATL::CComCoClass<class CBthRadioManager,&struct \_GUID const CLSID\_BthRadioManager>::GetObjectDescription(void))
00007ffc`290d735c BthRadioMedia!ATL::CAtlComModule::ExecuteObjectMain (public: void __cdecl ATL::CAtlComModule::ExecuteObjectMain(bool)) 00007ffc`290d8488 BthRadioMedia!ATL::\_CopyInterface<IConnectionPoint>::copy (public: static long \_\_cdecl ATL::\_CopyInterface<struct IConnectionPoint>::copy(struct IConnectionPoint \* \*,struct IConnectionPoint \* \*))
00007ffc`290d8030 BthRadioMedia!ATL::CComObject<CBthRadioManager>::Release (public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioManager>::Release(void)) 00007ffc`290d5f6c BthRadioMedia!ATL::AtlRegisterClassCategoriesHelper (long \_\_cdecl ATL::AtlRegisterClassCategoriesHelper(struct \_GUID const &,struct ATL::\_ATL\_CATMAP\_ENTRY const \*,int))
00007ffc`290d7490 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::GetConnectionInterface (public: virtual long __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::GetConnectionInterface(struct _GUID *)) 00007ffc`290dbd10 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::`scalar deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class CBthRadioInstance>::`scalar deleting destructor'(unsigned int))
00007ffc`290d63e8 BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> >::Clone (public: virtual long __cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >::Clone(struct IEnumConnectionPoints * *)) 00007ffc`290dae64 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::SetString (public: void \_\_cdecl ATL::CSimpleStringT<unsigned short,0>::SetString(unsigned short const \*,int))
00007ffc`290dbf00 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::AddRef (public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::AddRef(void)) 00007ffc`290d3450 BthRadioMedia!ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::Reset (public: virtual long \_\_cdecl ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::Reset(void))
00007ffc`290e1920 BthRadioMedia!ATL::CWin32Heap::Reallocate (public: virtual void * __cdecl ATL::CWin32Heap::Reallocate(void *,unsigned __int64)) 00007ffc`290d1280 BthRadioMedia!ATL::CComObjectRootBase::GetCategoryMap (public: static struct ATL::\_ATL\_CATMAP\_ENTRY const \* \_\_cdecl ATL::CComObjectRootBase::GetCategoryMap(void))
00007ffc`290dac40 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::Reallocate (private: void __cdecl ATL::CSimpleStringT<unsigned short,0>::Reallocate(int)) 00007ffc`290d8188 BthRadioMedia!ATL::CAtlModuleT<CBthRadioModule>::UnregisterServer (public: long \_\_cdecl ATL::CAtlModuleT<class CBthRadioModule>::UnregisterServer(int,struct \_GUID const \*))
00007ffc`290d9d48 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::CloneData (private: static struct ATL::CStringData * __cdecl ATL::CSimpleStringT<unsigned short,0>::CloneData(struct ATL::CStringData *)) 00007ffc`290d5df0 BthRadioMedia!ATL::AtlLoadTypeLib (long **cdecl ATL::AtlLoadTypeLib(struct HINSTANCE** \*,unsigned short const \*,unsigned short \* \*,struct ITypeLib \* \*))
00007ffc`290d2d15 BthRadioMedia!amsg_exit (_amsg_exit) 00007ffc`290d5b1c BthRadioMedia!ATL::AtlCallTermFunc (void \_\_cdecl ATL::AtlCallTermFunc(struct ATL::\_ATL\_MODULE70 \*))
00007ffc`290d5890 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::`scalar deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::`scalar deleting destructor'(unsigned int)) 00007ffc`290d6a50 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::CreateInstance (public: static long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::CreateInstance(class ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> > \* \*))
00007ffc`290d32c0 BthRadioMedia!ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::Clone (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::Clone(struct IEnumConnections * *)) 00007ffc`290d552c BthRadioMedia!ATL::CComObject<CBthRadioManager>::~CComObject<CBthRadioManager> (public: virtual \_\_cdecl ATL::CComObject<class CBthRadioManager>::~CComObject<class CBthRadioManager>(void))
00007ffc`290e1790 BthRadioMedia!ATL::CAtlStringMgr::Allocate (public: virtual struct ATL::CStringData * __cdecl ATL::CAtlStringMgr::Allocate(int,int)) 00007ffc`290d34ac BthRadioMedia!ATL::CComMultiThreadModel::SafeDecrementReference (public: static unsigned long \_\_cdecl ATL::CComMultiThreadModel::SafeDecrementReference(long \*))
00007ffc`290d9c14 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::AllocSysString (public: unsigned short * __cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::AllocSysString(void)const ) 00007ffc`290d2bf8 BthRadioMedia!atexit (atexit)
00007ffc`290d5200 BthRadioMedia!ATL::CComObject<CBthRadioManager>::CComObject<CBthRadioManager> (public: __cdecl ATL::CComObject<class CBthRadioManager>::CComObject<class CBthRadioManager>(void *)) 00007ffc`290d3f0c BthRadioMedia!ATL::CComBSTR::~CComBSTR (public: \_\_cdecl ATL::CComBSTR::~CComBSTR(void))
00007ffc`290d3810 BthRadioMedia!ATL::CComObject<CBthRadioManager>::Release ([thunk]:public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioManager>::Release`adjustor{32}' (void))
00007ffc`290d77b8 BthRadioMedia!ATL::InlineIsEqualUnknown (int __cdecl ATL::InlineIsEqualUnknown(struct _GUID const &)) 00007ffc`290d8100 BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint> >::Skip (public: virtual long \_\_cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint> >::Skip(unsigned long))
00007ffc`290d5a80 BthRadioMedia!ATL::CComObject<CBthRadioManager>::AddRef (public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioManager>::AddRef(void)) 00007ffc`290d8330 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID\_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::\_LocCPQueryInterface (public: virtual long \_\_cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct \_GUID const IID\_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::\_LocCPQueryInterface(struct \_GUID const &,void \* \*))
00007ffc`290d323c BthRadioMedia!ATL::CComAutoCriticalSection::~CComAutoCriticalSection (public: __cdecl ATL::CComAutoCriticalSection::~CComAutoCriticalSection(void)) 00007ffc`290d12c0 BthRadioMedia!ATL::CComObjectRootBase::ObjectMain (public: static void \_\_cdecl ATL::CComObjectRootBase::ObjectMain(bool))
00007ffc`290d31e8 BthRadioMedia!ATL::CComAutoCriticalSection::CComAutoCriticalSection (public: __cdecl ATL::CComAutoCriticalSection::CComAutoCriticalSection(void)) 00007ffc`290d4f70 BthRadioMedia!ATL::AtlAdd<unsigned \_\_int64> (long \_\_cdecl ATL::AtlAdd<unsigned \_\_int64>(unsigned \_\_int64 \*,unsigned \_\_int64,unsigned \_\_int64))
00007ffc`290d3840 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::Release ([thunk]:public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioInstance>::Release`adjustor{8}' (void))
00007ffc`290d3820 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::AddRef ([thunk]:public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioInstance>::AddRef`adjustor{8}' (void))
00007ffc`290d73b0 BthRadioMedia!ATL::IConnectionPointContainerImpl<CBthRadioManager>::FindConnectionPoint (public: virtual long __cdecl ATL::IConnectionPointContainerImpl<class CBthRadioManager>::FindConnectionPoint(struct _GUID const &,struct IConnectionPoint * *)) 00007ffc`290dac94 BthRadioMedia!ATL::CStringData::Release (public: void \_\_cdecl ATL::CStringData::Release(void))
00007ffc`290d7a94 BthRadioMedia!ATL::CRegKey::QueryDWORDValue (public: long __cdecl ATL::CRegKey::QueryDWORDValue(unsigned short const *,unsigned long &)) 00007ffc`290deaa0 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::Release (public: virtual unsigned long \_\_cdecl ATL::CComObject<class CBthRadioInstance>::Release(void))
00007ffc`290d5890 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::`vector deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::`vector deleting destructor'(unsigned int)) 00007ffc`290e1820 BthRadioMedia!ATL::CWin32Heap::Allocate (public: virtual void \* \_\_cdecl ATL::CWin32Heap::Allocate(unsigned \_\_int64))
00007ffc`290d3550 BthRadioMedia!ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::Skip (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::Skip(unsigned long)) 00007ffc`290d6b48 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::CreateInstance (public: static long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::CreateInstance(class ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> > \* \*))
00007ffc`290d7d10 BthRadioMedia!ATL::CComObject<CBthRadioManager>::QueryInterface (public: virtual long __cdecl ATL::CComObject<class CBthRadioManager>::QueryInterface(struct _GUID const &,void * *)) 00007ffc`290e1890 BthRadioMedia!ATL::CWin32Heap::GetSize (public: virtual unsigned \_\_int64 \_\_cdecl ATL::CWin32Heap::GetSize(void \*))
00007ffc`290daf48 BthRadioMedia!ATL::_AtlGetStringResourceImage (struct ATL::ATLSTRINGRESOURCEIMAGE const * __cdecl ATL::_AtlGetStringResourceImage(struct HINSTANCE__ *,struct HRSRC__ *,unsigned int)) 00007ffc`290d77f0 BthRadioMedia!ATL::CComClassFactory::LockServer (public: virtual long \_\_cdecl ATL::CComClassFactory::LockServer(int))
00007ffc`290d13c4 BthRadioMedia!ATL::CAtlBaseModule::CAtlBaseModule (public: __cdecl ATL::CAtlBaseModule::CAtlBaseModule(void)) 00007ffc`290d12d0 BthRadioMedia!ATL::CAtlModule::Unlock (public: virtual long \_\_cdecl ATL::CAtlModule::Unlock(void))
00007ffc`290d17c4 BthRadioMedia!ATL::CAtlBaseModule::~CAtlBaseModule (public: __cdecl ATL::CAtlBaseModule::~CAtlBaseModule(void)) 00007ffc`290d5a10 BthRadioMedia!ATL::CAtlModuleT<CBthRadioModule>::AddCommonRGSReplacements (public: virtual long \_\_cdecl ATL::CAtlModuleT<class CBthRadioModule>::AddCommonRGSReplacements(struct IRegistrarBase \*))
00007ffc`290dbec0 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::AddRef (public: virtual unsigned long __cdecl ATL::CComObject<class CBthRadioInstance>::AddRef(void)) 00007ffc`290d80b0 BthRadioMedia!ATL::CComObjectCached[ATL::CComClassFactory](javascript:void(0);)::Release (public: virtual unsigned long \_\_cdecl ATL::CComObjectCached<class ATL::CComClassFactory>::Release(void))
00007ffc`290d77e4 BthRadioMedia!ATL::CComObjectRootEx<ATL::CComMultiThreadModel>::InternalRelease (public: unsigned long __cdecl ATL::CComObjectRootEx<class ATL::CComMultiThreadModel>::InternalRelease(void)) 00007ffc`290d146c BthRadioMedia!ATL::CAtlWinModule::CAtlWinModule (public: \_\_cdecl ATL::CAtlWinModule::CAtlWinModule(void))
00007ffc`290d6c40 BthRadioMedia!ATL::CComClassFactory::CreateInstance (public: virtual long __cdecl ATL::CComClassFactory::CreateInstance(struct IUnknown *,struct _GUID const &,void * *)) 00007ffc`290d5d18 BthRadioMedia!ATL::AtlCrtErrorCheck (int \_\_cdecl ATL::AtlCrtErrorCheck(int))
00007ffc`290d1778 BthRadioMedia!ATL::CAtlWinModule::~CAtlWinModule (public: __cdecl ATL::CAtlWinModule::~CAtlWinModule(void)) 00007ffc`290d33c0 BthRadioMedia!ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::Next (public: virtual long \_\_cdecl ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::Next(unsigned long,struct tagCONNECTDATA \*,unsigned long \*))
00007ffc`290d7e10 BthRadioMedia!ATL::CComObjectCached<ATL::CComClassFactory>::QueryInterface (public: virtual long __cdecl ATL::CComObjectCached<class ATL::CComClassFactory>::QueryInterface(struct _GUID const &,void * *)) 00007ffc`290dbd50 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::`scalar deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::`scalar deleting destructor'(unsigned int))
00007ffc`290d52a4 BthRadioMedia!ATL::_ATL_SAFE_ALLOCA_IMPL::CAtlSafeAllocBufferManager<ATL::CCRTAllocator>::~CAtlSafeAllocBufferManager<ATL::CCRTAllocator> (public: __cdecl ATL::_ATL_SAFE_ALLOCA_IMPL::CAtlSafeAllocBufferManager<class ATL::CCRTAllocator>::~CAtlSafeAllocBufferManager<class ATL::CCRTAllocator>(void)) 00007ffc`290dc0fc BthRadioMedia!ATL::CComObject<CBthRadioInstance>::CreateInstance (public: static long \_\_cdecl ATL::CComObject<class CBthRadioInstance>::CreateInstance(class ATL::CComObject<class CBthRadioInstance> \* \*))
00007ffc`290d6798 BthRadioMedia!ATL::CRegKey::Close (public: long __cdecl ATL::CRegKey::Close(void)) 00007ffc`290e1860 BthRadioMedia!ATL::CWin32Heap::Free (public: virtual void \_\_cdecl ATL::CWin32Heap::Free(void \*))
00007ffc`290d12c0 BthRadioMedia!ATL::CComCriticalSection::~CComCriticalSection (public: __cdecl ATL::CComCriticalSection::~CComCriticalSection(void)) 00007ffc`290e16cc BthRadioMedia!ATL::CSimpleArray<unsigned short,ATL::CSimpleArrayEqualHelper<unsigned short> >::RemoveAll (public: void \_\_cdecl ATL::CSimpleArray<unsigned short,class ATL::CSimpleArrayEqualHelper<unsigned short> >::RemoveAll(void))
00007ffc`290d9de0 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::Empty (public: void __cdecl ATL::CSimpleStringT<unsigned short,0>::Empty(void)) 00007ffc`290dbf3c BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID\_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Advise (public: virtual long \_\_cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct \_GUID const IID\_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::Advise(struct IUnknown \*,unsigned long \*))
00007ffc`290d58d0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`scalar deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class CBthRadioManager>::`scalar deleting destructor'(unsigned int)) 00007ffc`290db818 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::~CComObject<CBthRadioInstance> (public: virtual \_\_cdecl ATL::CComObject<class CBthRadioInstance>::~CComObject<class CBthRadioInstance>(void))
00007ffc`290dacc4 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::SetLength (private: void __cdecl ATL::CSimpleStringT<unsigned short,0>::SetLength(int)) 00007ffc`290d54bc BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::~CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> > (public: virtual \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::~CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >(void))
00007ffc`290da038 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::Fork (private: void __cdecl ATL::CSimpleStringT<unsigned short,0>::Fork(int)) 00007ffc`290d1648 BthRadioMedia!ATL::CWin32Heap::~CWin32Heap (public: virtual \_\_cdecl ATL::CWin32Heap::~CWin32Heap(void))
00007ffc`290d1290 BthRadioMedia!ATL::CAtlModule::GetLockCount (public: virtual long __cdecl ATL::CAtlModule::GetLockCount(void)) 00007ffc`290dabd4 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::PrepareWrite2 (private: void \_\_cdecl ATL::CSimpleStringT<unsigned short,0>::PrepareWrite2(int))
00007ffc`290d8444 BthRadioMedia!ATL::_Copy<tagCONNECTDATA>::copy (public: static long __cdecl ATL::_Copy<struct tagCONNECTDATA>::copy(struct tagCONNECTDATA *,struct tagCONNECTDATA const *)) 00007ffc`290d9ab4 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::~CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > > (public: \_\_cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::~CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >(void))
00007ffc`290d7f18 BthRadioMedia!ATL::CAtlModuleT<CBthRadioModule>::RegisterServer (public: long __cdecl ATL::CAtlModuleT<class CBthRadioModule>::RegisterServer(int,struct _GUID const *)) 00007ffc`290dbd50 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::`vector deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::`vector deleting destructor'(unsigned int))
00007ffc`290d34e0 BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::Skip (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::Skip(unsigned long)) 00007ffc`290d5594 BthRadioMedia!ATL::CComObjectRootEx[ATL::CComMultiThreadModel](javascript:void(0);)::~CComObjectRootEx[ATL::CComMultiThreadModel](javascript:void(0);) (public: \_\_cdecl ATL::CComObjectRootEx<class ATL::CComMultiThreadModel>::~CComObjectRootEx<class ATL::CComMultiThreadModel>(void))
00007ffc`290dbd90 BthRadioMedia!ATL::CComDynamicUnkArray::Add (public: unsigned long __cdecl ATL::CComDynamicUnkArray::Add(struct IUnknown *)) 00007ffc`290d531c BthRadioMedia!ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel>::~CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> (public: virtual \_\_cdecl ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>::~CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel>(void))
00007ffc`290d76f8 BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA> >::Init (public: long __cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA> >::Init(struct tagCONNECTDATA *,struct tagCONNECTDATA *,struct IUnknown *,enum ATL::CComEnumFlags)) 00007ffc`290d4f94 BthRadioMedia!ATL::AtlMultiply<unsigned \_\_int64> (long \_\_cdecl ATL::AtlMultiply<unsigned \_\_int64>(unsigned \_\_int64 \*,unsigned \_\_int64,unsigned \_\_int64))
00007ffc`290dc1f4 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::CreateInstance (public: static long __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::CreateInstance(class ATL::CComObject<class CBthRadioInstanceCollection> * *)) 00007ffc`290db55c BthRadioMedia!ATL::CComObject<CBthRadioInstance>::CComObject<CBthRadioInstance> (public: \_\_cdecl ATL::CComObject<class CBthRadioInstance>::CComObject<class CBthRadioInstance>(void \*))
00007ffc`290d50e4 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> > (public: __cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >(void *)) 00007ffc`290deb20 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::Release (public: virtual unsigned long \_\_cdecl ATL::CComObject<class CBthRadioInstanceCollection>::Release(void))
00007ffc`290d58d0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::`vector deleting destructor' (public: virtual void \* \_\_cdecl ATL::CComObject<class CBthRadioManager>::`vector deleting destructor'(unsigned int)) 00007ffc`290d544c BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::~CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> > (public: virtual \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::~CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >(void))
00007ffc`290d67d0 BthRadioMedia!ATL::CComCreator2<ATL::CComCreator<ATL::CComObject<CBthRadioManager> >,ATL::CComFailCreator<-2147221232> >::CreateInstance (public: static long __cdecl ATL::CComCreator2<class ATL::CComCreator<class ATL::CComObject<class CBthRadioManager> >,class ATL::CComFailCreator<-2147221232> >::CreateInstance(void *,struct _GUID const &,void * *)) 00007ffc`290d4fc8 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> > (public: \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >(void \*))
00007ffc`290d6920 BthRadioMedia!ATL::CComCreator<ATL::CComObjectCached<ATL::CComClassFactory> >::CreateInstance (public: static long __cdecl ATL::CComCreator<class ATL::CComObjectCached<class ATL::CComClassFactory> >::CreateInstance(void *,struct _GUID const &,void * *)) 00007ffc`290e18b0 BthRadioMedia!ATL::CAtlStringMgr::Reallocate (public: virtual struct ATL::CStringData \* \_\_cdecl ATL::CAtlStringMgr::Reallocate(struct ATL::CStringData \*,int,int))
00007ffc`290d535c BthRadioMedia!ATL::CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> >::~CComEnumImpl<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint> > (public: virtual __cdecl ATL::CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >::~CComEnumImpl<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint> >(void)) 00007ffc`290d74f0 BthRadioMedia!ATL::CAtlModule::GetGITPtr (public: virtual long \_\_cdecl ATL::CAtlModule::GetGITPtr(struct IGlobalInterfaceTable \* \*))
00007ffc`290d7a38 BthRadioMedia!ATL::CRegKey::Open (public: long __cdecl ATL::CRegKey::Open(struct HKEY__ *,unsigned short const *,unsigned long)) 00007ffc`290d5850 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::`vector deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::`vector deleting destructor'(unsigned int))
00007ffc`290d7fb0 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&_GUID_b196b287_bab4_101a_b69c_00aa00341d07,tagCONNECTDATA,ATL::_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::Release (public: virtual unsigned long __cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct __s_GUID const _GUID_b196b287_bab4_101a_b69c_00aa00341d07,struct tagCONNECTDATA,class ATL::_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::Release(void)) 00007ffc`290d5810 BthRadioMedia!ATL::CRegKey::~CRegKey (public: \_\_cdecl ATL::CRegKey::~CRegKey(void))
00007ffc`290d6db0 BthRadioMedia!ATL::IConnectionPointContainerImpl<CBthRadioManager>::EnumConnectionPoints (public: virtual long __cdecl ATL::IConnectionPointContainerImpl<class CBthRadioManager>::EnumConnectionPoints(struct IEnumConnectionPoints * *)) 00007ffc`290d3780 BthRadioMedia!alloca\_probe (\_alloca\_probe)
00007ffc`290daf30 BthRadioMedia!ATL::CSimpleStringT<unsigned short,0>::ThrowMemoryException (protected: static void __cdecl ATL::CSimpleStringT<unsigned short,0>::ThrowMemoryException(void)) 00007ffc`290d3800 BthRadioMedia!ATL::CComObject<CBthRadioManager>::Release ([thunk]:public: virtual unsigned long \_\_cdecl ATL::CComObject<class CBthRadioManager>::Release`adjustor{8}' (void)) 00007ffc`290e1710 BthRadioMedia!ATL::CAtlStringMgr::`vector deleting destructor' (public: virtual void * __cdecl ATL::CAtlStringMgr::`vector deleting destructor'(unsigned int))
00007ffc`290d581c BthRadioMedia!ATL::CComPtr<IMediaRadioManagerNotifySink>::~CComPtr<IMediaRadioManagerNotifySink> (public: __cdecl ATL::CComPtr<struct IMediaRadioManagerNotifySink>::~CComPtr<struct IMediaRadioManagerNotifySink>(void)) 00007ffc`290daaf8 BthRadioMedia!ATL::CStringT<unsigned short,ATL::StrTraitATL<unsigned short,ATL::ChTraitsCRT<unsigned short> > >::LoadStringW (public: int **cdecl ATL::CStringT<unsigned short,class ATL::StrTraitATL<unsigned short,class ATL::ChTraitsCRT<unsigned short> > >::LoadStringW(struct HINSTANCE** \*,unsigned int))
00007ffc`290e1750 BthRadioMedia!ATL::CWin32Heap::`scalar deleting destructor' (public: virtual void \* **cdecl ATL::CWin32Heap::`scalar deleting destructor'(unsigned int)) 00007ffc`290e163c BthRadioMedia!ATL::CAtlBaseModule::GetHInstanceAt (public: struct HINSTANCE** \* \_\_cdecl ATL::CAtlBaseModule::GetHInstanceAt(int))
00007ffc`290d3830 BthRadioMedia!ATL::CComObject<CBthRadioInstance>::QueryInterface ([thunk]:public: virtual long __cdecl ATL::CComObject<class CBthRadioInstance>::QueryInterface`adjustor{8}' (struct \_GUID const &,void \* \*))
00007ffc`290db5c0 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::CComObject<CBthRadioInstanceCollection> (public: __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::CComObject<class CBthRadioInstanceCollection>(void *)) 00007ffc`290d7c00 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::QueryInterface (public: virtual long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::QueryInterface(struct \_GUID const &,void \* \*))
00007ffc`290d5270 BthRadioMedia!ATL::CComPtrBase<CBthRadioInstance>::CComPtrBase<CBthRadioInstance> (protected: __cdecl ATL::CComPtrBase<class CBthRadioInstance>::CComPtrBase<class CBthRadioInstance>(class CBthRadioInstance *)) 00007ffc`290d14e0 BthRadioMedia!ATL::CAtlStringMgr::CAtlStringMgr (public: \_\_cdecl ATL::CAtlStringMgr::CAtlStringMgr(struct ATL::IAtlMemMgr \*))
00007ffc`290d5910 BthRadioMedia!ATL::CComObjectCached<ATL::CComClassFactory>::`scalar deleting destructor' (public: void \* \_\_cdecl ATL::CComObjectCached<class ATL::CComClassFactory>::`scalar deleting destructor'(unsigned int)) 00007ffc`290d5850 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::`scalar deleting destructor' (public: virtual void * __cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::`scalar deleting destructor'(unsigned int))
00007ffc`290d55c0 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::~IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray> (public: __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::~IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>(void)) 00007ffc`290d3330 BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::Next (public: virtual long \_\_cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::Next(unsigned long,struct IConnectionPoint \* \*,unsigned long \*))
00007ffc`290d74c0 BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::GetConnectionPointContainer (public: virtual long __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::GetConnectionPointContainer(struct IConnectionPointContainer * *)) 00007ffc`290d5cbc BthRadioMedia!ATL::AtlComPtrAssign (struct IUnknown \* \_\_cdecl ATL::AtlComPtrAssign(struct IUnknown \* \*,struct IUnknown \*))
00007ffc`290d8224 BthRadioMedia!ATL::_ATL_SAFE_ALLOCA_IMPL::_AtlVerifyStackAvailable (bool __cdecl ATL::_ATL_SAFE_ALLOCA_IMPL::_AtlVerifyStackAvailable(unsigned __int64)) 00007ffc`290d792c BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA> >::Next (public: virtual long \_\_cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA> >::Next(unsigned long,struct tagCONNECTDATA \*,unsigned long \*))
00007ffc`290dee1c BthRadioMedia!ATL::IConnectionPointImpl<CBthRadioManager,&IID_IMediaRadioManagerNotifySink,ATL::CComDynamicUnkArray>::Unadvise (public: virtual long __cdecl ATL::IConnectionPointImpl<class CBthRadioManager,&struct _GUID const IID_IMediaRadioManagerNotifySink,class ATL::CComDynamicUnkArray>::Unadvise(unsigned long)) 00007ffc`290d37d0 BthRadioMedia!ATL::CComObject<CBthRadioManager>::AddRef ([thunk]:public: virtual unsigned long \_\_cdecl ATL::CComObject<class CBthRadioManager>::AddRef`adjustor{8}' (void)) 00007ffc`290d53d4 BthRadioMedia!ATL::CComEnumImpl<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA> >::~CComEnumImpl<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA> > (public: virtual \_\_cdecl ATL::CComEnumImpl<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA> >::~CComEnumImpl<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA> >(void))
00007ffc`290d3250 BthRadioMedia!ATL::CComEnum<IEnumConnectionPoints,&_GUID_b196b285_bab4_101a_b69c_00aa00341d07,IConnectionPoint * __ptr64,ATL::_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel>::Clone (public: virtual long __cdecl ATL::CComEnum<struct IEnumConnectionPoints,&struct __s_GUID const _GUID_b196b285_bab4_101a_b69c_00aa00341d07,struct IConnectionPoint *,class ATL::_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel>::Clone(struct IEnumConnectionPoints * *)) 00007ffc`290d1340 BthRadioMedia!ATL::CAtlComModule::CAtlComModule (public: \_\_cdecl ATL::CAtlComModule::CAtlComModule(void))
00007ffc`290d16f4 BthRadioMedia!ATL::CAtlComModule::~CAtlComModule (public: __cdecl ATL::CAtlComModule::~CAtlComModule(void)) 00007ffc`290d5b9c BthRadioMedia!ATL::AtlComModuleGetClassObject (long \_\_cdecl ATL::AtlComModuleGetClassObject(struct ATL::\_ATL\_COM\_MODULE70 \*,struct \_GUID const &,struct \_GUID const &,void \* \*))
00007ffc`290e1710 BthRadioMedia!ATL::CAtlStringMgr::`scalar deleting destructor' (public: virtual void \* \_\_cdecl ATL::CAtlStringMgr::`scalar deleting destructor'(unsigned int)) 00007ffc`290d5a40 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnections,&\_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,tagCONNECTDATA,ATL::\_Copy<tagCONNECTDATA>,ATL::CComMultiThreadModel> >::AddRef (public: virtual unsigned long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnections,&struct \_\_s\_GUID const \_GUID\_b196b287\_bab4\_101a\_b69c\_00aa00341d07,struct tagCONNECTDATA,class ATL::\_Copy<struct tagCONNECTDATA>,class ATL::CComMultiThreadModel> >::AddRef(void))
00007ffc`290db8b4 BthRadioMedia!ATL::CComObject<CBthRadioInstanceCollection>::~CComObject<CBthRadioInstanceCollection> (public: virtual __cdecl ATL::CComObject<class CBthRadioInstanceCollection>::~CComObject<class CBthRadioInstanceCollection>(void)) 00007ffc`290d7fb0 BthRadioMedia!ATL::CComObject<ATL::CComEnum<IEnumConnectionPoints,&\_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,IConnectionPoint \* \_\_ptr64,ATL::\_CopyInterface<IConnectionPoint>,ATL::CComMultiThreadModel> >::Release (public: virtual unsigned long \_\_cdecl ATL::CComObject<class ATL::CComEnum<struct IEnumConnectionPoints,&struct \_\_s\_GUID const \_GUID\_b196b285\_bab4\_101a\_b69c\_00aa00341d07,struct IConnectionPoint \*,class ATL::\_CopyInterface<struct IConnectionPoint>,class ATL::CComMultiThreadModel> >::Release(void))
00007ffc`290e1750 BthRadioMedia!ATL::CWin32Heap::`vector deleting destructor' (public: virtual void \* \_\_cdecl ATL::CWin32Heap::`vector deleting destructor'(unsigned int))

### wo...@gmail.com (2026-04-19)

Detailed analysis here <https://issues.chromium.org/u/9/issues/503810612>

### ch...@google.com (2026-06-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488617440)*
