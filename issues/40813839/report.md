# Browser crash when pasting multiple lines with Text Cursor Indicator enabled (Windows)

| Field | Value |
|-------|-------|
| **Issue ID** | [40813839](https://issues.chromium.org/issues/40813839) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P4 |
| **Component** | UI>Accessibility>Compatibility |
| **Platforms** | Windows |
| **Reporter** | fr...@gmail.com |
| **Assignee** | ks...@microsoft.com |
| **Created** | 2022-01-01 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36

Steps to reproduce the problem:
as in the video

What is the expected behavior?
no crash of Browser

What went wrong?
Browser Crash

Did this work before? N/A 

Chrome version: 96.0.4664.110  Channel: n/a
OS Version: 10.0

## Attachments

- [bandicam 2022-01-01 16-54-05-147.mp4](attachments/bandicam 2022-01-01 16-54-05-147.mp4) (video/mp4, 15.5 MB)
- [bandicam 2022-01-01 20-13-38-715.mp4](attachments/bandicam 2022-01-01 20-13-38-715.mp4) (video/mp4, 17.4 MB)
- [heapBufferOverFlowbandicam 2022-01-02 07-11-57-722.mp4](attachments/heapBufferOverFlowbandicam 2022-01-02 07-11-57-722.mp4) (video/mp4, 4.0 MB)
- [2022-01-02_073922.png](attachments/2022-01-02_073922.png) (image/png, 36.2 KB)
- [printerSearchBox-bandicam 2022-01-02 08-00-58-254.mp4](attachments/printerSearchBox-bandicam 2022-01-02 08-00-58-254.mp4) (video/mp4, 2.5 MB)
- [printer-page-numberbandicam 2022-01-02 10-23-26-589.mp4](attachments/printer-page-numberbandicam 2022-01-02 10-23-26-589.mp4) (video/mp4, 7.4 MB)
- [castbackFeedBackCrash-2022-01-02 10-50-54-376.mp4](attachments/castbackFeedBackCrash-2022-01-02 10-50-54-376.mp4) (video/mp4, 3.1 MB)
- [Personal Information Text Box crash 2022-01-02 11-00-10-084.mp4](attachments/Personal Information Text Box crash 2022-01-02 11-00-10-084.mp4) (video/mp4, 8.7 MB)
- [LoginChromeAccountCrash-2022-01-02 11-11-17-016.mp4](attachments/LoginChromeAccountCrash-2022-01-02 11-11-17-016.mp4) (video/mp4, 6.9 MB)
- [ChromeSearchTextBoxCrash.mp4](attachments/ChromeSearchTextBoxCrash.mp4) (video/mp4, 9.9 MB)
- [DebugConsoleFilterBoxCrash-2022-01-02 11-36-21-700.mp4](attachments/DebugConsoleFilterBoxCrash-2022-01-02 11-36-21-700.mp4) (video/mp4, 4.1 MB)
- [2022-01-02_114133.png](attachments/2022-01-02_114133.png) (image/png, 22.0 KB)
- [2022-01-02_114822.png](attachments/2022-01-02_114822.png) (image/png, 20.8 KB)
- [2022-01-02_115025.png](attachments/2022-01-02_115025.png) (image/png, 9.3 KB)
- [2022-01-02_115158.png](attachments/2022-01-02_115158.png) (image/png, 25.0 KB)
- [2022-01-02_115533.png](attachments/2022-01-02_115533.png) (image/png, 10.1 KB)
- [2022-01-02_121227.png](attachments/2022-01-02_121227.png) (image/png, 34.8 KB)
- [overflow.mp4](attachments/overflow.mp4) (video/mp4, 3.2 MB)
- [0.html](attachments/0.html) (text/plain, 19 B)
- [inputTextBoxCrash.mp4](attachments/inputTextBoxCrash.mp4) (video/mp4, 1.8 MB)
- [bandicam 2022-06-15 08-52-44-993.mp4](attachments/bandicam 2022-06-15 08-52-44-993.mp4) (video/mp4, 5.5 MB)
- [bandicam 2022-06-15 09-08-45-797.mp4](attachments/bandicam 2022-06-15 09-08-45-797.mp4) (video/mp4, 3.1 MB)

## Timeline

### fr...@gmail.com (2022-01-01)


Microsoft (R) Windows Debugger Version 10.0.22000.194 AMD64
Copyright (c) Microsoft Corporation. All rights reserved.

*** wait with pending attach

************* Path validation summary **************
Response                         Time (ms)     Location
Deferred                                       srv*
Symbol search path is: srv*
Executable search path is: 
ModLoad: 00007ff7`d3500000 00007ff7`d3762000   C:\Program Files\Google\Chrome\Application\chrome.exe
ModLoad: 00007ffc`b5840000 00007ffc`b5a47000   C:\Windows\SYSTEM32\ntdll.dll
ModLoad: 00007ffc`b3da0000 00007ffc`b3e5d000   C:\Windows\System32\KERNEL32.DLL
ModLoad: 00007ffc`b3110000 00007ffc`b3484000   C:\Windows\System32\KERNELBASE.dll
ModLoad: 00007ffc`83640000 00007ffc`8376b000   C:\Program Files\Google\Chrome\Application\96.0.4664.110\chrome_elf.dll
ModLoad: 00007ffc`ad030000 00007ffc`ad03a000   C:\Windows\SYSTEM32\VERSION.dll
ModLoad: 00007ffc`b3f30000 00007ffc`b3fd3000   C:\Windows\System32\msvcrt.dll
ModLoad: 00007ffc`b3be0000 00007ffc`b3c8c000   C:\Windows\System32\ADVAPI32.dll
ModLoad: 00007ffc`b5710000 00007ffc`b57ad000   C:\Windows\System32\sechost.dll
ModLoad: 00007ffc`b4400000 00007ffc`b4521000   C:\Windows\System32\RPCRT4.dll
ModLoad: 00007ffc`b24e0000 00007ffc`b24ec000   C:\Windows\SYSTEM32\CRYPTBASE.DLL
ModLoad: 00007ffc`b35b0000 00007ffc`b3630000   C:\Windows\System32\bcryptPrimitives.dll
ModLoad: 00007ffc`b0730000 00007ffc`b0764000   C:\Windows\system32\ntmarta.dll
ModLoad: 00007ffc`b3490000 00007ffc`b35a1000   C:\Windows\System32\ucrtbase.dll
ModLoad: 00007ffc`b41b0000 00007ffc`b435c000   C:\Windows\System32\user32.dll
ModLoad: 00007ffc`b3040000 00007ffc`b3066000   C:\Windows\System32\win32u.dll
ModLoad: 00007ffc`b3d60000 00007ffc`b3d89000   C:\Windows\System32\GDI32.dll
ModLoad: 00007ffc`b2d40000 00007ffc`b2e52000   C:\Windows\System32\gdi32full.dll
ModLoad: 00007ffc`b3070000 00007ffc`b310d000   C:\Windows\System32\msvcp_win.dll
ModLoad: 00007ffc`b57b0000 00007ffc`b57e1000   C:\Windows\System32\IMM32.DLL
ModLoad: 00007ffc`b4e90000 00007ffc`b5612000   C:\Windows\System32\SHELL32.dll
ModLoad: 00007ffc`b0ef0000 00007ffc`b1752000   C:\Windows\SYSTEM32\windows.storage.dll
ModLoad: 00007ffc`b4a30000 00007ffc`b4da8000   C:\Windows\System32\combase.dll
ModLoad: 00007ffc`b0d80000 00007ffc`b0ee6000   C:\Windows\SYSTEM32\wintypes.dll
ModLoad: 00007ffc`b37d0000 00007ffc`b38ba000   C:\Windows\System32\SHCORE.dll
ModLoad: 00007ffc`b4db0000 00007ffc`b4e0d000   C:\Windows\System32\shlwapi.dll
ModLoad: 00007ffc`48af0000 00007ffc`532df000   C:\Program Files\Google\Chrome\Application\96.0.4664.110\chrome.dll
ModLoad: 00007ffc`b4530000 00007ffc`b459f000   C:\Windows\System32\WS2_32.dll
ModLoad: 00007ffc`b36f0000 00007ffc`b37c6000   C:\Windows\System32\OLEAUT32.dll
ModLoad: 00007ffc`b2e60000 00007ffc`b2ec6000   C:\Windows\System32\WINTRUST.dll
ModLoad: 00007ffc`b2ed0000 00007ffc`b3032000   C:\Windows\System32\CRYPT32.dll
ModLoad: 00007ffc`ad500000 00007ffc`ad533000   C:\Windows\SYSTEM32\WINMM.dll
ModLoad: 00007ffc`9fca0000 00007ffc`9fec1000   C:\Windows\SYSTEM32\dbghelp.dll
ModLoad: 00007ffc`b19b0000 00007ffc`b19dd000   C:\Windows\SYSTEM32\IPHLPAPI.DLL
ModLoad: 00007ffc`91160000 00007ffc`9159e000   C:\Windows\SYSTEM32\UIAutomationCore.DLL
ModLoad: 00007ffc`9c030000 00007ffc`9c03c000   C:\Windows\SYSTEM32\Secur32.dll
ModLoad: 00007ffc`b2370000 00007ffc`b2399000   C:\Windows\SYSTEM32\USERENV.dll
ModLoad: 00007ffc`98d20000 00007ffc`98f7f000   C:\Windows\SYSTEM32\DWrite.dll
ModLoad: 00007ffc`8f680000 00007ffc`8f71a000   C:\Windows\SYSTEM32\WINSPOOL.DRV
ModLoad: 00007ffc`ae0b0000 00007ffc`ae1bc000   C:\Windows\SYSTEM32\WINHTTP.dll
ModLoad: 00007ffc`ae550000 00007ffc`ae56e000   C:\Windows\SYSTEM32\dhcpcsvc.DLL
ModLoad: 00007ffc`b2090000 00007ffc`b20d0000   C:\Windows\SYSTEM32\SSPICLI.DLL
ModLoad: 00007ffc`b2520000 00007ffc`b2532000   C:\Windows\System32\MSASN1.dll
ModLoad: 00007ffc`b0490000 00007ffc`b053c000   C:\Windows\system32\uxtheme.dll
ModLoad: 00007ffc`b2310000 00007ffc`b2334000   C:\Windows\SYSTEM32\gpapi.dll
ModLoad: 00007ffc`ad010000 00007ffc`ad027000   C:\Windows\SYSTEM32\wkscli.dll
ModLoad: 00007ffc`b19a0000 00007ffc`b19ac000   C:\Windows\SYSTEM32\netutils.dll
ModLoad: 00007ffc`b38c0000 00007ffc`b3a5a000   C:\Windows\System32\ole32.dll
ModLoad: 00007ffc`b1e70000 00007ffc`b1e88000   C:\Windows\SYSTEM32\kernel.appcore.dll
ModLoad: 00007ffc`b3a60000 00007ffc`b3b7e000   C:\Windows\System32\MSCTF.dll
ModLoad: 00007ffc`a4200000 00007ffc`a44a5000   C:\Windows\WinSxS\amd64_microsoft.windows.common-controls_6595b64144ccf1df_6.0.22000.120_none_9d947278b86cc467\COMCTL32.dll
ModLoad: 00007ffc`b2ab0000 00007ffc`b2aba000   C:\Windows\System32\DPAPI.dll
ModLoad: 00007ffc`82e70000 00007ffc`82e8f000   C:\Windows\system32\nlansp_c.dll
ModLoad: 00007ffc`b3fe0000 00007ffc`b3fe9000   C:\Windows\System32\NSI.dll
ModLoad: 00007ffc`ae280000 00007ffc`ae299000   C:\Windows\SYSTEM32\dhcpcsvc6.DLL
ModLoad: 00007ffc`b1a20000 00007ffc`b1b07000   C:\Windows\SYSTEM32\DNSAPI.dll
ModLoad: 00007ffc`b3cb0000 00007ffc`b3d5f000   C:\Windows\System32\clbcatq.dll
ModLoad: 00007ffc`99550000 00007ffc`9967d000   C:\Windows\SYSTEM32\textinputframework.dll
ModLoad: 00007ffc`ab2d0000 00007ffc`ab536000   C:\Windows\System32\twinapi.appcore.dll
ModLoad: 00007ffc`965f0000 00007ffc`966b8000   C:\Windows\system32\twinapi.dll
ModLoad: 00007ffc`99d80000 00007ffc`99f08000   C:\Windows\System32\Windows.UI.dll
ModLoad: 00007ffc`b2c70000 00007ffc`b2c91000   C:\Windows\SYSTEM32\profapi.dll
ModLoad: 00007ffc`af510000 00007ffc`af524000   C:\Windows\SYSTEM32\WTSAPI32.dll
ModLoad: 00007ffc`b2590000 00007ffc`b25f3000   C:\Windows\SYSTEM32\WINSTA.dll
ModLoad: 00007ffc`aa920000 00007ffc`aa9d9000   C:\Windows\SYSTEM32\mscms.dll
ModLoad: 00007ffc`b26b0000 00007ffc`b26d7000   C:\Windows\SYSTEM32\bcrypt.dll
ModLoad: 00007ffc`b2a40000 00007ffc`b2a8c000   C:\Windows\SYSTEM32\cfgmgr32.dll
ModLoad: 00007ffc`ab9d0000 00007ffc`aba6c000   C:\Windows\System32\MMDevApi.dll
ModLoad: 00007ffc`b29c0000 00007ffc`b29ec000   C:\Windows\System32\DEVOBJ.dll
ModLoad: 00007ffc`93cd0000 00007ffc`93e34000   C:\Windows\System32\wpnapps.dll
ModLoad: 00007ffc`aaa10000 00007ffc`ab225000   C:\Windows\System32\OneCoreUAPCommonProxyStub.dll
ModLoad: 00007ffc`b18c0000 00007ffc`b1963000   C:\Windows\System32\FirewallAPI.dll
ModLoad: 00007ffc`b1850000 00007ffc`b1885000   C:\Windows\System32\fwbase.dll
ModLoad: 00007ffc`a4f40000 00007ffc`a51c1000   C:\Windows\System32\msxml6.dll
ModLoad: 00007ffc`af210000 00007ffc`af307000   C:\Windows\SYSTEM32\PROPSYS.dll
ModLoad: 00007ffc`a41f0000 00007ffc`a41fd000   C:\Windows\SYSTEM32\LINKINFO.dll
ModLoad: 00007ffc`93b30000 00007ffc`93b8d000   C:\Windows\system32\dataexchange.dll
ModLoad: 00007ffc`b29f0000 00007ffc`b2a3d000   C:\Windows\SYSTEM32\powrprof.dll
ModLoad: 00007ffc`b27e0000 00007ffc`b27f3000   C:\Windows\SYSTEM32\UMPDC.dll
ModLoad: 00007ffc`b0870000 00007ffc`b089f000   C:\Windows\SYSTEM32\dwmapi.dll
ModLoad: 00007ffc`2b690000 00007ffc`2be68000   C:\Windows\System32\Windows.Media.dll
ModLoad: 00007ffc`aa9e0000 00007ffc`aa9ed000   C:\Windows\SYSTEM32\atlthunk.dll
ModLoad: 00007ffc`95b00000 00007ffc`95b69000   C:\Windows\SYSTEM32\OLEACC.dll
ModLoad: 00007ffc`9a850000 00007ffc`9a8ed000   C:\Windows\system32\directmanipulation.dll
ModLoad: 00007ffc`afee0000 00007ffc`b0012000   C:\Windows\SYSTEM32\CoreMessaging.dll
ModLoad: 00007ffc`ad180000 00007ffc`ad4ed000   C:\Windows\SYSTEM32\CoreUIComponents.dll
ModLoad: 00007ffc`8fd40000 00007ffc`8ffb0000   C:\Windows\system32\explorerframe.dll
ModLoad: 00007ffc`b45a0000 00007ffc`b4a0b000   C:\Windows\System32\SETUPAPI.dll
ModLoad: 00007ffc`a48f0000 00007ffc`a4a2b000   C:\Windows\System32\Windows.System.Launcher.dll
ModLoad: 00007ffc`ab930000 00007ffc`ab9c2000   C:\Windows\System32\msvcp110_win.dll
ModLoad: 00007ffc`a5750000 00007ffc`a576b000   C:\Windows\SYSTEM32\windows.staterepositorycore.dll
ModLoad: 00007ffc`ad140000 00007ffc`ad155000   C:\Windows\System32\threadpoolwinrt.dll
ModLoad: 00007ffc`b2280000 00007ffc`b22e7000   C:\Windows\system32\mswsock.dll
ModLoad: 00007ffc`b24c0000 00007ffc`b24d8000   C:\Windows\System32\CRYPTSP.dll
ModLoad: 00007ffc`b1dd0000 00007ffc`b1e05000   C:\Windows\system32\rsaenh.dll
ModLoad: 00007ffc`82e20000 00007ffc`82e51000   C:\Windows\System32\cryptnet.dll
ModLoad: 00007ffc`ad0c0000 00007ffc`ad13b000   C:\Windows\SYSTEM32\wlanapi.dll
ModLoad: 00007ffc`ad0a0000 00007ffc`ad0be000   C:\Windows\SYSTEM32\MobileNetworking.dll
ModLoad: 00007ffc`6fd70000 00007ffc`6ffe8000   C:\Windows\System32\Windows.Devices.Bluetooth.dll
ModLoad: 00007ffc`a1b30000 00007ffc`a1bff000   C:\Windows\System32\Windows.Devices.Enumeration.dll
ModLoad: 00007ffc`ab810000 00007ffc`ab84f000   C:\Windows\System32\Windows.Devices.Radios.dll
ModLoad: 00007ffc`937f0000 00007ffc`93811000   C:\Windows\System32\DevDispItemProvider.dll
ModLoad: 00007ffc`a2ad0000 00007ffc`a2ade000   C:\Windows\System32\DDORes.dll
ModLoad: 00007ffc`a1ae0000 00007ffc`a1ae8000   C:\Windows\System32\DefaultDeviceManager.dll
ModLoad: 00007ffc`90630000 00007ffc`9067d000   C:\Windows\System32\CapabilityAccessManagerClient.dll
ModLoad: 00007ffc`ab7a0000 00007ffc`ab7c1000   C:\Windows\system32\BthRadioMedia.dll
(2aac.294): Break instruction exception - code 80000003 (first chance)
ntdll!DbgBreakPoint:
00007ffc`b58e6ee0 cc              int     3
0:053> g
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
onecore\com\combase\objact\objact.cxx(4080)\combase.dll!00007FFCB4A9EFE5: (caller: 00007FFCB4A9B9F2) ReturnHr(18) tid(3c2c) 80040154 没有注册类
onecore\com\combase\dcomrem\resolver.cxx(2217)\combase.dll!00007FFCB4A9C368: (caller: 00007FFCB4A9AC0E) ReturnHr(19) tid(3c2c) 80040154 没有注册类
onecore\com\combase\dcomrem\resolver.cxx(2420)\combase.dll!00007FFCB4A9AC36: (caller: 00007FFCB4A9B656) ReturnHr(20) tid(3c2c) 80040154 没有注册类
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
onecore\com\combase\objact\objact.cxx(4080)\combase.dll!00007FFCB4A9EFE5: (caller: 00007FFCB4A9B9F2) ReturnHr(21) tid(3c2c) 80040154 没有注册类
onecore\com\combase\dcomrem\resolver.cxx(2217)\combase.dll!00007FFCB4A9C368: (caller: 00007FFCB4A9AC0E) ReturnHr(22) tid(3c2c) 80040154 没有注册类
onecore\com\combase\dcomrem\resolver.cxx(2420)\combase.dll!00007FFCB4A9AC36: (caller: 00007FFCB4A9B656) ReturnHr(23) tid(3c2c) 80040154 没有注册类
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.1684): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
(2aac.2d74): C++ EH exception - code e06d7363 (first chance)
onecore\com\combase\objact\objact.cxx(4080)\combase.dll!00007FFCB4A9EFE5: (caller: 00007FFCB4A9B9F2) ReturnHr(24) tid(1500) 80040154 没有注册类
ModLoad: 00007ffc`a44b0000 00007ffc`a44c6000   C:\Windows\System32\BitsProxy.dll
(2aac.1684): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome!Ordinal0+0x8059a5:
00007ffc`492f59a5 440fb70451      movzx   r8d,word ptr [rcx+rdx*2] ds:00003062`06394a58=????
0:000> kb
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffc`4c7922a7     : 00000000`0000352d 00007ffc`4c7882c8 a28aa873`d6374d5a aaaaaaaa`aaaaaaaa : chrome!Ordinal0+0x8059a5
01 00007ffc`4c796685     : aaaaaaaa`aaaaaaaa 000079e2`d31f0962 000000c2`fffffffe 00000000`ffffffff : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xa95a87
02 00007ffc`4c79dba5     : aaaaaaaa`00000001 aaaaaaaa`aaaaaa01 1a45ee73`535f5283 a28aa873`d6374d5a : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xa99e65
03 00007ffc`4c96cc12     : 00003062`0edac000 00007ffc`4e089191 00000000`00000000 00000000`00000000 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaa1385
04 00007ffc`4c7858e6     : 000000c2`39dfd180 00003062`0b24c000 00000000`00000000 00007ffc`4c7851a8 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xc703f2
05 00007ffc`4c7abffd     : 00003062`08f47150 00003062`08f47150 000000c2`39dfcfb0 000000c2`39dfd148 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xa890c6
06 00007ffc`4c7abf0b     : 00003062`0b21c000 00003062`0b2010e0 00003062`0b2010e0 00007ffc`4b4829c2 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaaf7dd
07 00007ffc`4c7ac0c0     : 000001c3`999d1b40 00000000`00000058 00000000`00000058 00007ffc`91219c43 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaaf6eb
08 00007ffc`912f0412     : 000000c2`39dfd280 00007ffc`912198da 00007ffc`914a3d10 00003062`08f47090 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaaf8a0
09 00007ffc`913baa92     : 000000c2`39dfd1b0 00000000`00000000 00000000`00000000 00000000`00000000 : UIAutomationCore!AccUtils::get_textAtOffset+0x72
0a 00007ffc`913bd07a     : 00000000`0000352d 00000000`00000000 00000000`00000000 000000c2`39dfd5a0 : UIAutomationCore!IA2ProxyTextRange::Endpoint::GetIA2Bounds+0xa6
0b 00007ffc`913bcb3b     : 00000000`00000000 000000c2`39dfd5a0 000001c3`999d1ae0 000001c3`928da6e0 : UIAutomationCore!IA2ProxyTextRange::Endpoint::GetUnitEndpointsInternal+0x47e
0c 00007ffc`913bf9f3     : 00000000`00000000 000000c2`39dfd700 00000000`00000000 000001c3`9299f2d0 : UIAutomationCore!IA2ProxyTextRange::Endpoint::GetUnitEndpoints+0x83
0d 00007ffc`913c0144     : 00000000`00000001 00000000`00000001 00000000`00000001 00000000`00000017 : UIAutomationCore!IA2ProxyTextRange::Endpoint::MoveByUnit+0x19b
0e 00007ffc`913c0057     : 000000c2`39dfd940 00000000`00000001 00000000`00000001 00007ffc`91166cae : UIAutomationCore!IA2ProxyTextRange::MoveEndpointByUnitInternal+0x74
0f 00007ffc`9126fd6a     : 000000c2`39dfd9c8 00007ffc`9121859f 000001c3`928c7980 00007ffc`911c7732 : UIAutomationCore!IA2ProxyTextRange::MoveEndpointByUnit+0x87
10 00007ffc`9132555e     : 000001c3`999c1cb0 000000c2`39dfd9c8 000001c3`9299f260 00000000`00000001 : UIAutomationCore!ProviderCallouts::MoveEndpointByUnit+0x6a
11 00007ffc`91167400     : 000001c3`9299f260 00000000`00000138 000000c2`505ffa90 00007ffc`91167438 : UIAutomationCore!RemotePatternStub::TextRange_MoveEndpointByUnit+0x6e
12 00007ffc`911651d3     : 00000000`00000000 00000000`00000003 00000000`00000000 00007ffc`b315b3fb : UIAutomationCore!RemotePatternStub::OnMessage+0x60
13 00007ffc`9119ece1     : 000001c3`9299f260 000001c3`928da6b0 000001c3`999c1e60 00000000`00000022 : UIAutomationCore!InvokePatternMethodOnCorrectContext_Callback+0xe3
14 00007ffc`9119ea2a     : 00000000`0007fd7c 000000c2`39dfeab8 00000000`00000001 00000000`00000000 : UIAutomationCore!HandleHookMessage+0x261
15 00007ffc`b41ccbd0     : 000000c2`3959d000 00000000`0000c08b 00000000`0000c08b 000000c2`39dfeab8 : UIAutomationCore!HookMessageWndProc+0x2a
16 00007ffc`b41d496d     : 000000c2`39dfed70 00007ffc`b58e70c4 00000000`00000000 00003062`00064a88 : user32!fnHkINLPCWPSTRUCTW+0xf0
17 00007ffc`b58e7224     : 00000000`00000000 00000000`00000000 00000000`00000030 00000319`d3f7ceb7 : user32!_fnDWORD+0x3d
18 00007ffc`b30413b4     : 00007ffc`b41c9d2f 000079e2`d31f2e02 aaaaaaaa`aaaaaaaa 00003062`00064a88 : ntdll!KiUserCallbackDispatcher+0x24
19 00007ffc`b41c9d2f     : 000079e2`d31f2e02 aaaaaaaa`aaaaaaaa 00003062`00064a88 00007ffc`4b8f3621 : win32u!NtUserPeekMessage+0x14
1a 00007ffc`b41c9c9a     : 00000000`00000001 000001c3`8f116ed0 00000000`00000000 aaaaaaaa`aaaaaaaa : user32!_PeekMessage+0x3f
1b 00007ffc`4b8caea0     : 00003062`00064a88 aaaaaaaa`aaaaaaaa 00003062`000b8140 000001c3`90eac868 : user32!PeekMessageW+0x13a
1c 00007ffc`48e9c164     : 00003062`00064a98 00007ffc`4b7488bb 7fffffff`ffffffff 00003062`00064b48 : chrome!GetHandleVerifier+0x18e7980
1d 00007ffc`49471b67     : 000079e2`d31f2ba2 00000000`00000030 000000c2`00000001 00007ffc`51ef13c0 : chrome!Ordinal0+0x3ac164
1e 00007ffc`49566831     : 000079e2`d31f2b12 00000000`00000030 00000319`cfbab9e2 00007ffc`4bb49327 : chrome!ChromeMain+0x4c1e7
1f 00007ffc`4bce84e5     : 00003062`0054bb80 00000000`00000000 00000319`cfafb15c 00000319`cfb008c1 : chrome!ChromeMain+0x140eb1
20 00007ffc`493814b1     : aaaaaaaa`aaaaaaaa 00000000`00000000 00006b66`00084060 00000000`ffffffff : chrome!ovly_debug_event+0xd1a65
21 00007ffc`4bc32e72     : 00000000`00000000 00007ffc`4bc32d74 00003062`000743c0 00003062`000743c0 : chrome!Ordinal0+0x8914b1
22 00007ffc`4bc328e4     : 000000c2`39dff280 000000c2`39dff2e0 00006b66`00070460 00000000`00000000 : chrome!ovly_debug_event+0x1c3f2
23 00007ffc`49373c2f     : 000000c2`39dff2e0 00000000`00000000 00007ffc`517f3db4 00000000`00000004 : chrome!ovly_debug_event+0x1be64
24 00007ffc`49426ab2     : 000000c2`39dff3d8 00007ffc`48f5c2fa 00000000`00000001 00000000`00000001 : chrome!Ordinal0+0x883c2f
25 00007ffc`49425b0a     : 00003062`000740c0 00007ff7`d3500000 000000c2`39dff6f0 00000000`00000000 : chrome!ChromeMain+0x1132
26 00007ff7`d35a72b0     : 00000000`00000201 00007ffc`49425980 00000000`00000000 000000c2`39dff710 : chrome!ChromeMain+0x18a
27 00007ff7`d35a6e57     : 00000000`00000001 00000000`00000000 000000c2`39dffac0 00007ffc`b5884583 : chrome_exe!GetHandleVerifier+0x50920
28 00007ff7`d35ed1c2     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!GetHandleVerifier+0x504c7
29 00007ffc`b3db54e0     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!GetHandleVerifier+0x96832
2a 00007ffc`b584485b     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : KERNEL32!BaseThreadInitThunk+0x10
2b 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2b
0:000> r
rax=000030620e1b0301 rbx=000000c239dfcca8 rcx=000030620638e000
rdx=000000000000352c rsi=000000c239dfcd28 rdi=000000000000352c
rip=00007ffc492f59a5 rsp=000000c239dfcc68 rbp=aaaaaaaaaaaaaaaa
 r8=0000000000000080  r9=0000000000002710 r10=7f7f7f7f7f7f7f7f
r11=0000306209074710 r12=0000000000000001 r13=000000c239dfd180
r14=000000c239dfce10 r15=aaaaaaaaaaaaaaaa
iopl=0         nv up ei ng nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010282
chrome!Ordinal0+0x8059a5:
00007ffc`492f59a5 440fb70451      movzx   r8d,word ptr [rcx+rdx*2] ds:00003062`06394a58=????


### [Deleted User] (2022-01-01)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-01-01)

00-open browser , command is `chrome --user-data-dir=./userdata http://127.0.0.1`

01-open some tabs of different sites

02-windbg to attach the browser Process

03-going to search tabs, paste many lines of this as in the video

chrome --user-data-dir=./userdata http://127.0.0.1

04-if everything is ok, we can see the windbg pasued!!

### fr...@gmail.com (2022-01-01)

here are two videos to reproduce this:


### fr...@gmail.com (2022-01-01)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-01-01)

Browser Version is the latest Stable Release :

Google Chrome	96.0.4664.110 (正式版本) （64 位） (cohort: Stable)
修订版本	d5ef0e8214bc14c9b5bbf69a1515e431394c62a6-refs/branch-heads/4664@{#1283}
操作系统	Windows 11 Version 21H2 (Build 22000.194)
JavaScript	V8 9.6.180.21
用户代理	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36
命令行	"C:\Program Files\Google\Chrome\Application\chrome.exe" --flag-switches-begin --flag-switches-end --origin-trial-disabled-features=CaptureHandle
可执行文件路径	C:\Program Files\Google\Chrome\Application\chrome.exe
个人资料路径	C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default

### fr...@gmail.com (2022-01-01)

we can reproduce this issue in chrome://settings/  search text box, to reproduce this is also easy , we just need to paste rubish text is OK
I pasted the follow lines many times:
chrome --user-data-dir=./userdata http://127.0.0.1

and the stable release of Chrome is pasued in windbg ,the windbg's out put like this:




Microsoft (R) Windows Debugger Version 10.0.22000.194 AMD64
Copyright (c) Microsoft Corporation. All rights reserved.

*** wait with pending attach

************* Path validation summary **************
Response                         Time (ms)     Location
Deferred                                       srv*
Symbol search path is: srv*
Executable search path is: 
ModLoad: 00007ff7`28f90000 00007ff7`291f2000   C:\Program Files\Google\Chrome\Application\chrome.exe
ModLoad: 00007ffe`d3f70000 00007ffe`d4170000   C:\Windows\SYSTEM32\ntdll.dll
ModLoad: 00007ffe`d2fd0000 00007ffe`d308c000   C:\Windows\System32\KERNEL32.DLL
ModLoad: 00007ffe`d15d0000 00007ffe`d192f000   C:\Windows\System32\KERNELBASE.dll
ModLoad: 00007ffe`c4fb0000 00007ffe`c4fba000   C:\Windows\SYSTEM32\VERSION.dll
ModLoad: 00007ffe`d2ab0000 00007ffe`d2b53000   C:\Windows\System32\msvcrt.dll
ModLoad: 00007ffe`b5980000 00007ffe`b5aab000   C:\Program Files\Google\Chrome\Application\96.0.4664.110\chrome_elf.dll
ModLoad: 00007ffe`d2ba0000 00007ffe`d2c4c000   C:\Windows\System32\ADVAPI32.dll
ModLoad: 00007ffe`d3090000 00007ffe`d312e000   C:\Windows\System32\sechost.dll
ModLoad: 00007ffe`d33d0000 00007ffe`d34ef000   C:\Windows\System32\RPCRT4.dll
ModLoad: 00007ffe`d0cd0000 00007ffe`d0cdc000   C:\Windows\SYSTEM32\CRYPTBASE.DLL
ModLoad: 00007ffe`d1550000 00007ffe`d15ce000   C:\Windows\System32\bcryptPrimitives.dll
ModLoad: 00007ffe`cfa80000 00007ffe`cfab4000   C:\Windows\system32\ntmarta.dll
ModLoad: 00007ffe`d1c50000 00007ffe`d1d60000   C:\Windows\System32\ucrtbase.dll
ModLoad: 00007ffe`d3d10000 00007ffe`d3eb5000   C:\Windows\System32\user32.dll
ModLoad: 00007ffe`d19d0000 00007ffe`d19f6000   C:\Windows\System32\win32u.dll
ModLoad: 00007ffe`d2660000 00007ffe`d268b000   C:\Windows\System32\GDI32.dll
ModLoad: 00007ffe`d1b30000 00007ffe`d1c41000   C:\Windows\System32\gdi32full.dll
ModLoad: 00007ffe`d1930000 00007ffe`d19d0000   C:\Windows\System32\msvcp_win.dll
ModLoad: 00007ffe`d2b60000 00007ffe`d2b91000   C:\Windows\System32\IMM32.DLL
ModLoad: 00007ffe`9a2b0000 00007ffe`a4a9f000   C:\Program Files\Google\Chrome\Application\96.0.4664.110\chrome.dll
ModLoad: 00007ffe`d25e0000 00007ffe`d2651000   C:\Windows\System32\WS2_32.dll
ModLoad: 00007ffe`d3130000 00007ffe`d3207000   C:\Windows\System32\OLEAUT32.dll
ModLoad: 00007ffe`d2690000 00007ffe`d2a01000   C:\Windows\System32\combase.dll
ModLoad: 00007ffe`d1a00000 00007ffe`d1a6a000   C:\Windows\System32\WINTRUST.dll
ModLoad: 00007ffe`d1d60000 00007ffe`d1ebf000   C:\Windows\System32\CRYPT32.dll
ModLoad: 00007ffe`c5420000 00007ffe`c5447000   C:\Windows\SYSTEM32\WINMM.dll
ModLoad: 00007ffe`c5180000 00007ffe`c5392000   C:\Windows\SYSTEM32\dbghelp.dll
ModLoad: 00007ffe`d07d0000 00007ffe`d07fd000   C:\Windows\SYSTEM32\IPHLPAPI.DLL
ModLoad: 00007ffe`be280000 00007ffe`be68c000   C:\Windows\SYSTEM32\UIAutomationCore.DLL
ModLoad: 00007ffe`c5590000 00007ffe`c559c000   C:\Windows\SYSTEM32\Secur32.dll
ModLoad: 00007ffe`d0b60000 00007ffe`d0b8e000   C:\Windows\SYSTEM32\USERENV.dll
ModLoad: 00007ffe`ba4f0000 00007ffe`ba74f000   C:\Windows\SYSTEM32\DWrite.dll
ModLoad: 00007ffe`bc710000 00007ffe`bc7a8000   C:\Windows\SYSTEM32\WINSPOOL.DRV
ModLoad: 00007ffe`c99d0000 00007ffe`c9ad2000   C:\Windows\SYSTEM32\WINHTTP.dll
ModLoad: 00007ffe`ca990000 00007ffe`ca9ad000   C:\Windows\SYSTEM32\dhcpcsvc.DLL
ModLoad: 00007ffe`d0f30000 00007ffe`d0f71000   C:\Windows\SYSTEM32\SSPICLI.DLL
ModLoad: 00007ffe`d0f10000 00007ffe`d0f22000   C:\Windows\System32\MSASN1.dll
ModLoad: 00007ffe`cf7f0000 00007ffe`cf894000   C:\Windows\system32\uxtheme.dll
ModLoad: 00007ffe`d0b00000 00007ffe`d0b25000   C:\Windows\SYSTEM32\gpapi.dll
ModLoad: 00007ffe`d2420000 00007ffe`d247f000   C:\Windows\System32\SHLWAPI.dll
ModLoad: 00007ffe`d1ec0000 00007ffe`d1fab000   C:\Windows\System32\shcore.dll
ModLoad: 00007ffe`c99b0000 00007ffe`c99c7000   C:\Windows\SYSTEM32\wkscli.dll
ModLoad: 00007ffe`d08e0000 00007ffe`d08ec000   C:\Windows\SYSTEM32\netutils.dll
ModLoad: 00007ffe`d2480000 00007ffe`d25b5000   C:\Windows\System32\ole32.dll
ModLoad: 00007ffe`cff40000 00007ffe`cff57000   C:\Windows\SYSTEM32\kernel.appcore.dll
ModLoad: 00007ffe`d2c60000 00007ffe`d2d7c000   C:\Windows\System32\MSCTF.dll
ModLoad: 00007ffe`c5dd0000 00007ffe`c6075000   C:\Windows\WinSxS\amd64_microsoft.windows.common-controls_6595b64144ccf1df_6.0.20348.1_none_88d3d41d702dedea\COMCTL32.dll
ModLoad: 00007ffe`d1330000 00007ffe`d133a000   C:\Windows\System32\DPAPI.dll
ModLoad: 00007ffe`a97a0000 00007ffe`a97bf000   C:\Windows\system32\nlansp_c.dll
ModLoad: 00007ffe`d3210000 00007ffe`d3219000   C:\Windows\System32\NSI.dll
ModLoad: 00007ffe`ca9b0000 00007ffe`ca9c9000   C:\Windows\SYSTEM32\dhcpcsvc6.DLL
ModLoad: 00007ffe`d0800000 00007ffe`d08dd000   C:\Windows\SYSTEM32\DNSAPI.dll
ModLoad: 00007ffe`d3320000 00007ffe`d33cf000   C:\Windows\System32\clbcatq.dll
ModLoad: 00007ffe`c81f0000 00007ffe`c8305000   C:\Windows\SYSTEM32\textinputframework.dll
ModLoad: 00007ffe`d3550000 00007ffe`d3caa000   C:\Windows\System32\SHELL32.dll
ModLoad: 00007ffe`c67b0000 00007ffe`c6ff5000   C:\Windows\SYSTEM32\windows.storage.dll
ModLoad: 00007ffe`ca9d0000 00007ffe`cabf6000   C:\Windows\System32\twinapi.appcore.dll
ModLoad: 00007ffe`bf820000 00007ffe`bf8d7000   C:\Windows\system32\twinapi.dll
ModLoad: 00007ffe`bf420000 00007ffe`bf5a3000   C:\Windows\System32\Windows.UI.dll
ModLoad: 00007ffe`d1480000 00007ffe`d14a1000   C:\Windows\SYSTEM32\profapi.dll
ModLoad: 00007ffe`cdd40000 00007ffe`cdd54000   C:\Windows\SYSTEM32\WTSAPI32.dll
ModLoad: 00007ffe`c9900000 00007ffe`c99af000   C:\Windows\SYSTEM32\mscms.dll
ModLoad: 00007ffe`c98b0000 00007ffe`c98c3000   C:\Windows\SYSTEM32\ColorAdapterClient.dll
ModLoad: 00007ffe`d11e0000 00007ffe`d1243000   C:\Windows\SYSTEM32\WINSTA.dll
ModLoad: 00007ffe`c1cc0000 00007ffe`c1d52000   C:\Windows\System32\MMDevApi.dll
ModLoad: 00007ffe`d11b0000 00007ffe`d11dc000   C:\Windows\System32\DEVOBJ.dll
ModLoad: 00007ffe`d1140000 00007ffe`d118c000   C:\Windows\SYSTEM32\cfgmgr32.dll
ModLoad: 00007ffe`bf5b0000 00007ffe`bf712000   C:\Windows\System32\wpnapps.dll
ModLoad: 00007ffe`c8de0000 00007ffe`c95e2000   C:\Windows\System32\OneCoreUAPCommonProxyStub.dll
ModLoad: 00007ffe`d0200000 00007ffe`d02a1000   C:\Windows\System32\FirewallAPI.dll
ModLoad: 00007ffe`d0190000 00007ffe`d01c5000   C:\Windows\System32\fwbase.dll
ModLoad: 00007ffe`b5890000 00007ffe`b5976000   C:\Windows\System32\MsSpellCheckingFacility.dll
ModLoad: 00007ffe`c8180000 00007ffe`c81e4000   C:\Windows\System32\Bcp47Langs.dll
ModLoad: 00007ffe`c7000000 00007ffe`c7046000   C:\Windows\System32\FWPolicyIOMgr.dll
ModLoad: 00007ffe`cbfe0000 00007ffe`cc0e1000   C:\Windows\SYSTEM32\PROPSYS.dll
ModLoad: 00007ffe`ccc20000 00007ffe`ccc2d000   C:\Windows\SYSTEM32\LINKINFO.dll
ModLoad: 00007ffe`c3090000 00007ffe`c30ad000   C:\Windows\SYSTEM32\MPR.dll
ModLoad: 00007ffe`c1d90000 00007ffe`c1dec000   C:\Windows\system32\dataexchange.dll
ModLoad: 00007ffe`d1420000 00007ffe`d146d000   C:\Windows\SYSTEM32\powrprof.dll
ModLoad: 00007ffe`d1400000 00007ffe`d1413000   C:\Windows\SYSTEM32\UMPDC.dll
ModLoad: 00007ffe`cfba0000 00007ffe`cfbcf000   C:\Windows\SYSTEM32\dwmapi.dll
ModLoad: 00007ffe`b0dc0000 00007ffe`b158d000   C:\Windows\System32\Windows.Media.dll
ModLoad: 00007ffe`c3180000 00007ffe`c318d000   C:\Windows\SYSTEM32\atlthunk.dll
ModLoad: 00007ffe`c2270000 00007ffe`c22d9000   C:\Windows\SYSTEM32\OLEACC.dll
ModLoad: 00007ffe`b8c30000 00007ffe`b8cd0000   C:\Windows\system32\directmanipulation.dll
ModLoad: 00007ffe`cf370000 00007ffe`cf497000   C:\Windows\SYSTEM32\CoreMessaging.dll
ModLoad: 00007ffe`cbc70000 00007ffe`cbfd6000   C:\Windows\SYSTEM32\CoreUIComponents.dll
ModLoad: 00007ffe`bce60000 00007ffe`bd097000   C:\Windows\system32\explorerframe.dll
ModLoad: 00007ffe`d1fb0000 00007ffe`d241a000   C:\Windows\System32\SETUPAPI.dll
ModLoad: 00007ffe`d0a70000 00007ffe`d0ad8000   C:\Windows\system32\mswsock.dll
ModLoad: 00007ffe`d0cb0000 00007ffe`d0cc8000   C:\Windows\System32\CRYPTSP.dll
ModLoad: 00007ffe`d0600000 00007ffe`d0635000   C:\Windows\system32\rsaenh.dll
ModLoad: 00007ffe`d0e00000 00007ffe`d0e27000   C:\Windows\System32\bcrypt.dll
ModLoad: 00007ffe`a6c00000 00007ffe`a6c31000   C:\Windows\System32\cryptnet.dll
ModLoad: 00007ffe`af940000 00007ffe`afbaf000   C:\Windows\System32\Windows.Devices.Bluetooth.dll
ModLoad: 00007ffe`b0580000 00007ffe`b064e000   C:\Windows\System32\Windows.Devices.Enumeration.dll
ModLoad: 00007ffe`c5050000 00007ffe`c5172000   C:\Windows\System32\Windows.System.Launcher.dll
ModLoad: 00007ffe`cb310000 00007ffe`cb3a2000   C:\Windows\System32\msvcp110_win.dll
ModLoad: 00007ffe`c72a0000 00007ffe`c72de000   C:\Windows\System32\Windows.Devices.Radios.dll
ModLoad: 00007ffe`c4f70000 00007ffe`c4f88000   C:\Windows\SYSTEM32\windows.staterepositorycore.dll
ModLoad: 00007ffe`b5760000 00007ffe`b582a000   C:\Windows\system32\msctfuimanager.dll
ModLoad: 00007ffe`b4320000 00007ffe`b44df000   C:\Windows\system32\DUI70.dll
ModLoad: 00007ffe`b4280000 00007ffe`b4319000   C:\Windows\system32\DUser.dll
ModLoad: 00007ffe`d1340000 00007ffe`d13e4000   C:\Windows\SYSTEM32\sxs.dll
ModLoad: 00007ffe`c9b80000 00007ffe`c9bc9000   C:\Windows\System32\UIAnimation.dll
ModLoad: 00007ffe`cb510000 00007ffe`cb793000   C:\Windows\system32\d3d11.dll
ModLoad: 00007ffe`cf930000 00007ffe`cfa12000   C:\Windows\system32\dxgi.dll
ModLoad: 00007ffe`cac00000 00007ffe`cb2fd000   C:\Windows\SYSTEM32\D3D10Warp.dll
ModLoad: 00007ffe`cc530000 00007ffe`cc56e000   C:\Windows\SYSTEM32\directxdatabasehelper.dll
ModLoad: 00007ffe`ca930000 00007ffe`ca96a000   C:\Windows\SYSTEM32\dxcore.dll
ModLoad: 00007ffe`ce420000 00007ffe`ce634000   C:\Windows\SYSTEM32\dcomp.dll
ModLoad: 00007ffe`be690000 00007ffe`be72e000   C:\Windows\SYSTEM32\TextShaping.dll
ModLoad: 00007ffe`cdbb0000 00007ffe`cdbe7000   C:\Windows\system32\xmllite.dll
ModLoad: 00007ffe`ce870000 00007ffe`ce941000   C:\Windows\System32\OneCoreCommonProxyStub.dll
ModLoad: 00007ffe`c4fc0000 00007ffe`c5043000   C:\Windows\SYSTEM32\webauthn.dll
(880.ca8): Break instruction exception - code 80000003 (first chance)
ntdll!DbgBreakPoint:
00007ffe`d40126a0 cc              int     3
0:039> g
ModLoad: 00007ffe`bb6e0000 00007ffe`bb759000   C:\Windows\SYSTEM32\cryptngc.dll
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): C++ EH exception - code e06d7363 (first chance)
(880.dd0): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome!Ordinal0+0x8059a5:
00007ffe`9aab59a5 440fb70451      movzx   r8d,word ptr [rcx+rdx*2] ds:000015d6`00de30da=????
0:000> kb
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffe`9df522a7     : 00000000`0000286e 00007ffe`9df482c8 5239fa8d`18360f18 aaaaaaaa`aaaaaaaa : chrome!Ordinal0+0x8059a5
01 00007ffe`9df56685     : aaaaaaaa`aaaaaaaa 0000b065`881927f9 0000001f`fffffffe 00000000`ffffffff : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xa95a87
02 00007ffe`9df5dba5     : aaaaaaaa`00000001 aaaaaaaa`aaaaaa01 15f9a2d3`e56e9be5 5239fa8d`18360f18 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xa99e65
03 00007ffe`9e12cc12     : 00000126`ecc18960 00000000`00000000 0000001f`45dfd8e0 00000000`00000000 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaa1385
04 00007ffe`9df458e6     : 00007ffe`a4199838 00000000`00005150 00000000`00000000 00007ffe`9df451a8 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xc703f2
05 00007ffe`9df6bffd     : 000015d6`000306d0 000015d6`000306d0 0000001f`45dfd710 0000001f`45dfd8a8 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xa890c6
06 00007ffe`9df6bf0b     : 000015d6`0269a000 000015d6`026014c0 000015d6`026014a0 00007ffe`9cc429c2 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaaf7dd
07 00007ffe`9df6c0c0     : 00000126`ef9db3f0 00000000`00000005 00000126`ef9db330 00000000`00000058 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaaf6eb
08 00007ffe`be45930a     : 00000000`00000000 00000000`00000001 00007ffe`be56ac20 000015d6`00030610 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaaf8a0
09 00007ffe`be4e927a     : 0000001f`45dfd910 00000000`00000000 00000000`00000000 0000001f`45dfd910 : UIAutomationCore!AccUtils::get_textAtOffset+0x72
0a 00007ffe`be4eb943     : 00000000`0000286e 00000000`00000000 00000000`00000000 0000001f`45dfdd00 : UIAutomationCore!IA2ProxyTextRange::Endpoint::GetIA2Bounds+0xa6
0b 00007ffe`be4eb40b     : 00000000`00000000 0000001f`45dfdd00 00000000`00000001 00000000`00000000 : UIAutomationCore!IA2ProxyTextRange::Endpoint::GetUnitEndpointsInternal+0x45b
0c 00007ffe`be4ee2fb     : 00000000`00000000 0000001f`45dfde70 00000000`00000000 00000126`ef96a938 : UIAutomationCore!IA2ProxyTextRange::Endpoint::GetUnitEndpoints+0x73
0d 00007ffe`be4eea67     : 00000000`00000000 00000000`00000000 00000000`ffffffff 00007ffe`be5678c0 : UIAutomationCore!IA2ProxyTextRange::Endpoint::MoveByUnit+0x19b
0e 00007ffe`be4ee960     : 0000001f`45dfe0b0 00000000`00000000 00000126`ef96a910 00000000`00000000 : UIAutomationCore!IA2ProxyTextRange::MoveEndpointByUnitInternal+0x77
0f 00007ffe`be3e4e26     : 0000001f`45dfe138 00000126`e8e50000 00000000`00000020 00007ffe`be2fda31 : UIAutomationCore!IA2ProxyTextRange::MoveEndpointByUnit+0x70
10 00007ffe`be320e97     : 00000126`efa0b460 0000001f`45dfe138 00000126`ef96a910 00000000`00000000 : UIAutomationCore!ProviderCallouts::MoveEndpointByUnit+0x6a
11 00007ffe`be31cdda     : 00000126`ef96a910 00000000`00000010 0000001f`45dfe2c0 00007ffe`be2eb39c : UIAutomationCore!RemotePatternStub::TextRange_MoveEndpointByUnit+0x57
12 00007ffe`be2ff352     : 00000000`00000000 00000000`00000030 00000000`00000000 00000000`00000003 : UIAutomationCore!RemotePatternStub::OnMessage+0x66
13 00007ffe`be2a87cf     : 00000126`ef96a910 00000126`efa072a0 00000126`efa0b340 00000000`00000022 : UIAutomationCore!InvokePatternMethodOnCorrectContext_Callback+0x122
14 00007ffe`be2ff1dc     : 00000126`00000000 00007ffe`be2ff230 00000000`00000000 00007ffe`00000000 : UIAutomationCore!ComInvoker::CallTarget+0x47f
15 00007ffe`be2ffd7c     : 00000000`1c23f349 0000001f`45dfe4b9 0000001f`45dfe478 00000000`ffffff9e : UIAutomationCore!InvokePatternMethodOnCorrectContext+0xc0
16 00007ffe`be2ff8dc     : 00000000`0000327b 00000000`0000327b 0000001f`45dfe4a8 0000001f`45dfe590 : UIAutomationCore!`anonymous namespace'::ProcessIncomingRequestNoThrow+0x3c8
17 00007ffe`be28a52d     : 00000126`ef86d200 0000001f`45dfe4b9 00000000`0000327b 00000000`80000000 : UIAutomationCore!ProcessIncomingRequest+0x30
18 00007ffe`be2bcdf7     : 00000126`ec880000 00000126`efa0ae90 00000000`0000001d 00000126`ec880000 : UIAutomationCore!HookBasedServerConnectionManager::HookCallback+0x2ad
19 00007ffe`be2a9830     : 00000000`00004085 00000126`ef86e000 00000000`000000b0 00000000`00001080 : UIAutomationCore!HookUtil<&HookBasedClientConnection::HookCallback,0>::CallOut+0x17
1a 00007ffe`be2a9487     : 00000000`000049e0 00000001`f31cf174 00000013`7f216e8d aaaaaaaa`aaaaaaaa : UIAutomationCore!HandleSyncHookMessage+0x320
1b 00007ffe`d3d34e4c     : 0000001f`455d0000 00000000`0000c09c 00000000`0000c09c 00000000`00000000 : UIAutomationCore!HookUtil<&HookBasedClientConnection::HookCallback,0>::CallWndProc+0x37
1c 00007ffe`d3d3612d     : 0000001f`45dfe9f0 00007ffe`d4012884 00000000`00000000 000015d6`000a0c08 : user32!fnHkINLPCWPSTRUCTW+0xec
1d 00007ffe`d40129e4     : aaaaaaaa`aaaaaaaa 000015d6`000a0c08 000015d6`015f95a4 00000001`f31cf1de : user32!_fnDWORD+0x3d
1e 00007ffe`d19d1064     : 00007ffe`d3d21dc3 0000b065`88191bb9 aaaaaaaa`aaaaaaaa 000015d6`000a0c08 : ntdll!KiUserCallbackDispatcherContinue
1f 00007ffe`d3d21dc3     : 0000b065`88191bb9 aaaaaaaa`aaaaaaaa 000015d6`000a0c08 00007ffe`9d0b3621 : win32u!NtUserPeekMessage+0x14
20 00007ffe`d3d21d2f     : 00000000`00000000 00000126`e9870640 00000000`00000001 aaaaaaaa`aaaaaaaa : user32!_PeekMessage+0x43
21 00007ffe`9d08aea0     : 000015d6`000a0c08 aaaaaaaa`aaaaaaaa 000015d6`000b8140 00000126`eb664fc0 : user32!PeekMessageW+0x13f
22 00007ffe`9a65c164     : 0000001f`45dfed08 00007ffe`9cf088bb 7fffffff`ffffffff 000015d6`000a0cc8 : chrome!GetHandleVerifier+0x18e7980
23 00007ffe`9ac31b67     : 00000000`00000000 00007ffe`9ad268b3 000011e6`00000001 00000000`45dfee01 : chrome!Ordinal0+0x3ac164
24 00007ffe`9ad26831     : 00000000`00000030 00000000`00000030 00000001`ef0c480f 00007ffe`9d309327 : chrome!ChromeMain+0x4c1e7
25 00007ffe`9d4a84e5     : 0000001f`45dfeea0 00000000`00000018 00000001`ef08e8e1 00000001`ef092126 : chrome!ChromeMain+0x140eb1
26 00007ffe`9ab414b1     : aaaaaaaa`aaaaaaaa 00000000`00000000 000011e6`000a00c0 00000000`ffffffff : chrome!ovly_debug_event+0xd1a65
27 00007ffe`9d3f2e72     : 00000000`00000000 00007ffe`9d3f2d74 000015d6`0006c3c0 000015d6`0006c3c0 : chrome!Ordinal0+0x8914b1
28 00007ffe`9d3f28e4     : 0000001f`45dfef00 0000001f`45dfef60 000011e6`0008c4b0 00000000`00000000 : chrome!ovly_debug_event+0x1c3f2
29 00007ffe`9ab33c2f     : 0000001f`45dfef60 00000000`00000000 00007ffe`a2fb3db4 00000000`00000004 : chrome!ovly_debug_event+0x1be64
2a 00007ffe`9abe6ab2     : 0000001f`45dff058 00007ffe`9a71c2fa 00000000`00000001 00000000`00000001 : chrome!Ordinal0+0x883c2f
2b 00007ffe`9abe5b0a     : 000015d6`0006c120 00007ff7`28f90000 0000001f`45dff370 00000000`00000000 : chrome!ChromeMain+0x1132
2c 00007ff7`290372b0     : 00000000`00000101 00007ffe`9abe5980 00000000`00000000 0000001f`45dff390 : chrome!ChromeMain+0x18a
2d 00007ff7`29036e57     : 00000000`0000000a 00000000`00000000 0000001f`45dff740 00007ffe`d3f9a343 : chrome_exe!GetHandleVerifier+0x50920
2e 00007ff7`2907d1c2     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!GetHandleVerifier+0x504c7
2f 00007ffe`d2fe4ed0     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!GetHandleVerifier+0x96832
30 00007ffe`d3fee20b     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : KERNEL32!BaseThreadInitThunk+0x10
31 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2b
0:000> r
rax=000015d60170b501 rbx=0000001f45dfd408 rcx=000015d600dde000
rdx=000000000000286d rsi=0000001f45dfd488 rdi=000000000000286d
rip=00007ffe9aab59a5 rsp=0000001f45dfd3c8 rbp=aaaaaaaaaaaaaaaa
 r8=0000000000000080  r9=0000000000002710 r10=7f7f7f7f7f7f7f7f
r11=000015d600870710 r12=0000000000000001 r13=0000001f45dfd8e0
r14=0000001f45dfd570 r15=aaaaaaaaaaaaaaaa
iopl=0         nv up ei ng nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010282
chrome!Ordinal0+0x8059a5:
00007ffe`9aab59a5 440fb70451      movzx   r8d,word ptr [rcx+rdx*2] ds:000015d6`00de30da=????
0:000> SRV*C:\symbols*http://msdl.microsoft.com/download/symbols;SRV*C:\symbols*http://chromium-browser-symsrv.commondatastorage.googleapis.com
Couldn't resolve error at 'RV*C:\symbols*http://msdl.microsoft.com/download/symbols;SRV*C:\symbols*http://chromium-browser-symsrv.commondatastorage.googleapis.com'
0:000> ld chrome*
Symbols already loaded for chrome_exe
Symbols already loaded for chrome
Symbols loaded for chrome_elf
0:000> .reload
Reloading current modules
................................................................
.....................................................

************* Symbol Loading Error Summary **************
Module name            Error
SharedUserData         No error - symbol load deferred
chrome                 The system cannot find the file specified

You can troubleshoot most symbol related issues by turning on symbol loading diagnostics (!sym noisy) and repeating the command that caused symbols to be loaded.
You should also verify that your symbol search path (.sympath) is correct.
0:000> SRV*C:\symbols*http://chromium-browser-symsrv.commondatastorage.googleapis.com
Couldn't resolve error at 'RV*C:\symbols*http://chromium-browser-symsrv.commondatastorage.googleapis.com'

************* Path validation summary **************
Response                         Time (ms)     Location
Deferred                                       srv*http://chromium-browser-symsrv.commondatastorage.googleapis.com
0:000> .reload
Reloading current modules
................................................................
.....................................................

************* Symbol Loading Error Summary **************
Module name            Error
SharedUserData         No error - symbol load deferred
chrome                 The system cannot find the file specified

You can troubleshoot most symbol related issues by turning on symbol loading diagnostics (!sym noisy) and repeating the command that caused symbols to be loaded.
You should also verify that your symbol search path (.sympath) is correct.
0:000> ld chrome*
Symbols loaded for chrome_exe
Symbols already loaded for chrome
Symbols loaded for chrome_elf
0:000> kb
 # RetAddr               : Args to Child                                                           : Call Site
00 00007ffe`9df522a7     : 00000000`0000286e 00007ffe`9df482c8 5239fa8d`18360f18 aaaaaaaa`aaaaaaaa : chrome!Ordinal0+0x8059a5
01 00007ffe`9df56685     : aaaaaaaa`aaaaaaaa 0000b065`881927f9 0000001f`fffffffe 00000000`ffffffff : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xa95a87
02 00007ffe`9df5dba5     : aaaaaaaa`00000001 aaaaaaaa`aaaaaa01 15f9a2d3`e56e9be5 5239fa8d`18360f18 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xa99e65
03 00007ffe`9e12cc12     : 00000126`ecc18960 00000000`00000000 0000001f`45dfd8e0 00000000`00000000 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaa1385
04 00007ffe`9df458e6     : 00007ffe`a4199838 00000000`00005150 00000000`00000000 00007ffe`9df451a8 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xc703f2
05 00007ffe`9df6bffd     : 000015d6`000306d0 000015d6`000306d0 0000001f`45dfd710 0000001f`45dfd8a8 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xa890c6
06 00007ffe`9df6bf0b     : 000015d6`0269a000 000015d6`026014c0 000015d6`026014a0 00007ffe`9cc429c2 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaaf7dd
07 00007ffe`9df6c0c0     : 00000126`ef9db3f0 00000000`00000005 00000126`ef9db330 00000000`00000058 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaaf6eb
08 00007ffe`be45930a     : 00000000`00000000 00000000`00000001 00007ffe`be56ac20 000015d6`00030610 : chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0xaaf8a0
09 00007ffe`be4e927a     : 0000001f`45dfd910 00000000`00000000 00000000`00000000 0000001f`45dfd910 : UIAutomationCore!AccUtils::get_textAtOffset+0x72
0a 00007ffe`be4eb943     : 00000000`0000286e 00000000`00000000 00000000`00000000 0000001f`45dfdd00 : UIAutomationCore!IA2ProxyTextRange::Endpoint::GetIA2Bounds+0xa6
0b 00007ffe`be4eb40b     : 00000000`00000000 0000001f`45dfdd00 00000000`00000001 00000000`00000000 : UIAutomationCore!IA2ProxyTextRange::Endpoint::GetUnitEndpointsInternal+0x45b
0c 00007ffe`be4ee2fb     : 00000000`00000000 0000001f`45dfde70 00000000`00000000 00000126`ef96a938 : UIAutomationCore!IA2ProxyTextRange::Endpoint::GetUnitEndpoints+0x73
0d 00007ffe`be4eea67     : 00000000`00000000 00000000`00000000 00000000`ffffffff 00007ffe`be5678c0 : UIAutomationCore!IA2ProxyTextRange::Endpoint::MoveByUnit+0x19b
0e 00007ffe`be4ee960     : 0000001f`45dfe0b0 00000000`00000000 00000126`ef96a910 00000000`00000000 : UIAutomationCore!IA2ProxyTextRange::MoveEndpointByUnitInternal+0x77
0f 00007ffe`be3e4e26     : 0000001f`45dfe138 00000126`e8e50000 00000000`00000020 00007ffe`be2fda31 : UIAutomationCore!IA2ProxyTextRange::MoveEndpointByUnit+0x70
10 00007ffe`be320e97     : 00000126`efa0b460 0000001f`45dfe138 00000126`ef96a910 00000000`00000000 : UIAutomationCore!ProviderCallouts::MoveEndpointByUnit+0x6a
11 00007ffe`be31cdda     : 00000126`ef96a910 00000000`00000010 0000001f`45dfe2c0 00007ffe`be2eb39c : UIAutomationCore!RemotePatternStub::TextRange_MoveEndpointByUnit+0x57
12 00007ffe`be2ff352     : 00000000`00000000 00000000`00000030 00000000`00000000 00000000`00000003 : UIAutomationCore!RemotePatternStub::OnMessage+0x66
13 00007ffe`be2a87cf     : 00000126`ef96a910 00000126`efa072a0 00000126`efa0b340 00000000`00000022 : UIAutomationCore!InvokePatternMethodOnCorrectContext_Callback+0x122
14 00007ffe`be2ff1dc     : 00000126`00000000 00007ffe`be2ff230 00000000`00000000 00007ffe`00000000 : UIAutomationCore!ComInvoker::CallTarget+0x47f
15 00007ffe`be2ffd7c     : 00000000`1c23f349 0000001f`45dfe4b9 0000001f`45dfe478 00000000`ffffff9e : UIAutomationCore!InvokePatternMethodOnCorrectContext+0xc0
16 00007ffe`be2ff8dc     : 00000000`0000327b 00000000`0000327b 0000001f`45dfe4a8 0000001f`45dfe590 : UIAutomationCore!`anonymous namespace'::ProcessIncomingRequestNoThrow+0x3c8
17 00007ffe`be28a52d     : 00000126`ef86d200 0000001f`45dfe4b9 00000000`0000327b 00000000`80000000 : UIAutomationCore!ProcessIncomingRequest+0x30
18 00007ffe`be2bcdf7     : 00000126`ec880000 00000126`efa0ae90 00000000`0000001d 00000126`ec880000 : UIAutomationCore!HookBasedServerConnectionManager::HookCallback+0x2ad
19 00007ffe`be2a9830     : 00000000`00004085 00000126`ef86e000 00000000`000000b0 00000000`00001080 : UIAutomationCore!HookUtil<&HookBasedClientConnection::HookCallback,0>::CallOut+0x17
1a 00007ffe`be2a9487     : 00000000`000049e0 00000001`f31cf174 00000013`7f216e8d aaaaaaaa`aaaaaaaa : UIAutomationCore!HandleSyncHookMessage+0x320
1b 00007ffe`d3d34e4c     : 0000001f`455d0000 00000000`0000c09c 00000000`0000c09c 00000000`00000000 : UIAutomationCore!HookUtil<&HookBasedClientConnection::HookCallback,0>::CallWndProc+0x37
1c 00007ffe`d3d3612d     : 0000001f`45dfe9f0 00007ffe`d4012884 00000000`00000000 000015d6`000a0c08 : user32!fnHkINLPCWPSTRUCTW+0xec
1d 00007ffe`d40129e4     : aaaaaaaa`aaaaaaaa 000015d6`000a0c08 000015d6`015f95a4 00000001`f31cf1de : user32!_fnDWORD+0x3d
1e 00007ffe`d19d1064     : 00007ffe`d3d21dc3 0000b065`88191bb9 aaaaaaaa`aaaaaaaa 000015d6`000a0c08 : ntdll!KiUserCallbackDispatcherContinue
1f 00007ffe`d3d21dc3     : 0000b065`88191bb9 aaaaaaaa`aaaaaaaa 000015d6`000a0c08 00007ffe`9d0b3621 : win32u!NtUserPeekMessage+0x14
20 00007ffe`d3d21d2f     : 00000000`00000000 00000126`e9870640 00000000`00000001 aaaaaaaa`aaaaaaaa : user32!_PeekMessage+0x43
21 00007ffe`9d08aea0     : 000015d6`000a0c08 aaaaaaaa`aaaaaaaa 000015d6`000b8140 00000126`eb664fc0 : user32!PeekMessageW+0x13f
22 00007ffe`9a65c164     : 0000001f`45dfed08 00007ffe`9cf088bb 7fffffff`ffffffff 000015d6`000a0cc8 : chrome!GetHandleVerifier+0x18e7980
23 00007ffe`9ac31b67     : 00000000`00000000 00007ffe`9ad268b3 000011e6`00000001 00000000`45dfee01 : chrome!Ordinal0+0x3ac164
24 00007ffe`9ad26831     : 00000000`00000030 00000000`00000030 00000001`ef0c480f 00007ffe`9d309327 : chrome!ChromeMain+0x4c1e7
25 00007ffe`9d4a84e5     : 0000001f`45dfeea0 00000000`00000018 00000001`ef08e8e1 00000001`ef092126 : chrome!ChromeMain+0x140eb1
26 00007ffe`9ab414b1     : aaaaaaaa`aaaaaaaa 00000000`00000000 000011e6`000a00c0 00000000`ffffffff : chrome!ovly_debug_event+0xd1a65
27 00007ffe`9d3f2e72     : 00000000`00000000 00007ffe`9d3f2d74 000015d6`0006c3c0 000015d6`0006c3c0 : chrome!Ordinal0+0x8914b1
28 00007ffe`9d3f28e4     : 0000001f`45dfef00 0000001f`45dfef60 000011e6`0008c4b0 00000000`00000000 : chrome!ovly_debug_event+0x1c3f2
29 00007ffe`9ab33c2f     : 0000001f`45dfef60 00000000`00000000 00007ffe`a2fb3db4 00000000`00000004 : chrome!ovly_debug_event+0x1be64
2a 00007ffe`9abe6ab2     : 0000001f`45dff058 00007ffe`9a71c2fa 00000000`00000001 00000000`00000001 : chrome!Ordinal0+0x883c2f
2b 00007ffe`9abe5b0a     : 000015d6`0006c120 00007ff7`28f90000 0000001f`45dff370 00000000`00000000 : chrome!ChromeMain+0x1132
2c 00007ff7`290372b0     : 00000000`00000101 00007ffe`9abe5980 00000000`00000000 0000001f`45dff390 : chrome!ChromeMain+0x18a
2d 00007ff7`29036e57     : 00000000`0000000a 00000000`00000000 0000001f`45dff740 00007ffe`d3f9a343 : chrome_exe!GetHandleVerifier+0x50920
2e 00007ff7`2907d1c2     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!GetHandleVerifier+0x504c7
2f 00007ffe`d2fe4ed0     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : chrome_exe!GetHandleVerifier+0x96832
30 00007ffe`d3fee20b     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : KERNEL32!BaseThreadInitThunk+0x10
31 00000000`00000000     : 00000000`00000000 00000000`00000000 00000000`00000000 00000000`00000000 : ntdll!RtlUserThreadStart+0x2b
0:000> r
rax=000015d60170b501 rbx=0000001f45dfd408 rcx=000015d600dde000
rdx=000000000000286d rsi=0000001f45dfd488 rdi=000000000000286d
rip=00007ffe9aab59a5 rsp=0000001f45dfd3c8 rbp=aaaaaaaaaaaaaaaa
 r8=0000000000000080  r9=0000000000002710 r10=7f7f7f7f7f7f7f7f
r11=000015d600870710 r12=0000000000000001 r13=0000001f45dfd8e0
r14=0000001f45dfd570 r15=aaaaaaaaaaaaaaaa
iopl=0         nv up ei ng nz na pe nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010282
chrome!Ordinal0+0x8059a5:
00007ffe`9aab59a5 440fb70451      movzx   r8d,word ptr [rcx+rdx*2] ds:000015d6`00de30da=????
0:000> lm m chrome*
Browse full module list
start             end                 module name
00007ff7`28f90000 00007ff7`291f2000   chrome_exe   (export symbols)       C:\Program Files\Google\Chrome\Application\chrome.exe
00007ffe`9a2b0000 00007ffe`a4a9f000   chrome     (export symbols)       C:\Program Files\Google\Chrome\Application\96.0.4664.110\chrome.dll
00007ffe`b5980000 00007ffe`b5aab000   chrome_elf   (export symbols)       C:\Program Files\Google\Chrome\Application\96.0.4664.110\chrome_elf.dll


### fr...@gmail.com (2022-01-01)

this long search operation will crash all process of asan including the cmd window,so I did not post any msg of asan .

### fr...@gmail.com (2022-01-01)

I can confirm that It is a heap buffer OverFlow ,the asan out put is that. But it can quickly crash the asan window.
here is the video:


### fr...@gmail.com (2022-01-01)

May be we can reproduce this bug many places where there is a search box in browser.


### fr...@gmail.com (2022-01-02)

printer search box triggered video

### fr...@gmail.com (2022-01-02)

may be we can make a limitation to the printer page number


### fr...@gmail.com (2022-01-02)

cast feedback email text box crash video :


### fr...@gmail.com (2022-01-02)

Personal Information Text Box crash


### fr...@gmail.com (2022-01-02)

Login Chrome Account Textbox Crash:


### fr...@gmail.com (2022-01-02)

Chrome Search Box Crash:


### fr...@gmail.com (2022-01-02)

DebugConsoleFilterBoxCrash:


### fr...@gmail.com (2022-01-02)

there are some other places can trigger , but all are the same issue.


### fr...@gmail.com (2022-01-02)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-01-02)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-01-02)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-01-02)

other placers :



### fr...@gmail.com (2022-01-02)

in print review can trigger:


### ke...@chromium.org (2022-01-03)

Thank you for the report. Can you please go to chrome://crashes and provide a crash ID for one of these crashes?

Crash reporting would need to be turned on for it to be generated.

### fr...@gmail.com (2022-01-03)

when make a deep review, I saw some warnings that was similar to https://crbug.com/chromium/1283417,
I dont know whether this is the same to https://crbug.com/chromium/1283417.
But if it is, plz feel free to merge the two issues to one.

### [Deleted User] (2022-01-03)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fr...@gmail.com (2022-01-03)

we can see the crash type from the video , even if it was dissappeared quickly.
Pause the video and the type dissplaied is heap buffer overflow.

### fr...@gmail.com (2022-01-03)

Sorry to bother you that :
does all int3 opration code treated as NO security bug?
Encounted another browser crash that not CHECK() function cause.

### fr...@gmail.com (2022-01-03)

[Comment Deleted]

### dr...@chromium.org (2022-01-05)

I'm struggling to reproduce this. It would be very helpful to have the result of chrome://crashes. Can you provide the crash id's from that page?

### fr...@gmail.com (2022-01-06)

if any convient , copy the next line ,then paste to the search bar, as the following video.
I think it will be the most convient heap buffer over flow .
 the line is :
chrome --user-data-dir=./userdata "https://127.0.0.1/poc.html"

### [Deleted User] (2022-01-06)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fr...@gmail.com (2022-01-06)

yesterday's stable release have not patched.
and all the above pictures input textbox are affected , they triggered the same vul i think.

### fr...@gmail.com (2022-01-06)

copy the line ,and press button Ctrl+V, until the browser crash.
the line can be :
chrome --user-data-dir=./userdata "https://127.0.0.1/poc.html"

### fr...@gmail.com (2022-01-06)


状态：	未上传
本机崩溃上下文：	186855e5-055e-4d30-b340-015a6db5bb79
 should i upload it ?
usually there is  a firewall to make it not upload 

### fr...@gmail.com (2022-01-06)

https://bugs.chromium.org/p/chromium/issues/detail?id=1283701#c11
this asan out put we can see it is heap buffer over flow.

### dr...@chromium.org (2022-01-06)

Please try to upload it, since that would definitely help me triage this. If it fails, we'll see what else we can do.

Where did the Chrome binary come from? Is it a local build or a production build? Can you try this without windbg attached, in case that's changing the behavior in some way?

### fr...@gmail.com (2022-01-06)

sorry bro . the binarys are all official release newest stable release or asan version downloaded by gsutil.

### fr...@gmail.com (2022-01-06)

[Comment Deleted]

### [Deleted User] (2022-01-06)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fr...@gmail.com (2022-01-07)

628393d5-8ae3-43bc-b03d-f063698faa64
uploaded

### fr...@gmail.com (2022-01-07)

[Comment Deleted]

### fr...@gmail.com (2022-01-07)

崩溃时间：2022年1月7日星期五 上午8:32:37
状态：	已上传
已上传的崩溃报告 ID：	2ff1e6bb62a4ebe4
上传时间：	2022年1月7日星期五 上午8:39:47


### fr...@gmail.com (2022-01-07)

[Comment Deleted]

### dr...@chromium.org (2022-01-10)

Thanks for the crash ID!

dtseng@ - I was never able to reproduce this bug, but we do have a valid crash report now with ID 2ff1e6bb62a4ebe4. Hopefully the crash report has enough information to make some progress here?

### [Deleted User] (2022-01-10)

[Empty comment from Monorail migration]

### dt...@chromium.org (2022-01-10)

To aleventhal for triage.

### fr...@gmail.com (2022-01-11)

https://bugs.chromium.org/p/chromium/issues/detail?id=1283701#c45
dear p0, to be honest , It is really Convenient to trigger.
All need to do is :
use Ctrl+C to copy a line of words(any words is ok),
press Ctrl+v to a text box(you can select a place above this comment in the picture) , never Let your hands go until the browser crash.
the feeling is just like we are in the year of 1998 , in order to make a stack buffer overflow to over write the return address of function.
then the Browser crash happened!
and there are really lots of places can triggered In the latest Official Release of Chrome.
Any questions are Ok for me , I will try my best.

### fr...@gmail.com (2022-01-11)

When Press Ctrl+v , make sure not lift our hand.
That is to say: Keep Pressing Ctrl+V until browser crashed.
Any messages are OK , I will try my best.

### al...@chromium.org (2022-01-11)

Hi Kurt/Daniel, can either of you take a look? It involves IA2ProxyTextRange::Endpoint::GetIA2Bounds() in UIAutomationCore.dll.
It sounds like the repro steps are just to hold down control+v to paste in a textfield.

0x00007fffc7f56ff5	(chrome.dll -utf16_indexing.cc:13)		gfx::IsValidCodePointIndex(std::__1::basic_string<char16_t,std::__1::char_traits<char16_t>,std::__1::allocator<char16_t> > const &,unsigned __int64)
0x00007fffcbd971e9	(chrome.dll -ax_position.h:2410)		ui::AXPosition<ui::AXNodePosition,ui::AXNode>::AsLeafTextPositionBeforeCharacter()
0x00007fffcbd9b9eb	(chrome.dll -ax_position.h:2505)		ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreateNextCharacterPosition(ui::AXBoundaryBehavior)
0x00007fffcbda3459	(chrome.dll -ax_position.h:1673)		ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreatePositionAtTextBoundary(ax::mojom::TextBoundary,ax::mojom::MoveDirection,ui::AXBoundaryBehavior)
0x00007fffcbf62661	(chrome.dll -browser_accessibility.cc:1211)		content::BrowserAccessibility::FindTextBoundary(ax::mojom::TextBoundary,int,ax::mojom::MoveDirection,ax::mojom::TextAffinity)
0x00007fffcbd89a56	(chrome.dll -ax_platform_node_base.cc:2008)		ui::AXPlatformNodeBase::FindTextBoundary(ax::mojom::TextBoundary,int,ax::mojom::MoveDirection,ax::mojom::TextAffinity)
0x00007fffcbdb2837	(chrome.dll -ax_platform_node_win.cc:8025)		ui::AXPlatformNodeWin::FindBoundary
0x00007fffcbdb2721	(chrome.dll -ax_platform_node_win.cc:3640)		ui::AXPlatformNodeWin::IAccessibleTextGetTextForOffsetType
0x00007fffcbdb2906	(chrome.dll -ax_platform_node_win.cc:3695)		ui::AXPlatformNodeWin::get_textAtOffset(long,IA2TextBoundaryType,long *,long *,wchar_t * *)
0x00007fffe66c9309	(UIAutomationCore.DLL + 0x001d9309)		AccUtils::get_textAtOffset(IAccessibleText *,long,IA2TextBoundaryType,long *,long *,unsigned short * *)
0x00007fffe6759279	(UIAutomationCore.DLL + 0x00269279)		IA2ProxyTextRange::Endpoint::GetIA2Bounds(CachedAcc2Node const &,long,IA2ProxyTextRange::Endpoint::InternalBoundaryType,IA2ProxyTextRange::Endpoint::UnitBoundsRequired)
0x00007fffe675b942	(UIAutomationCore.DLL + 0x0026b942)		IA2ProxyTextRange::Endpoint::GetUnitEndpointsInternal(IA2ProxyTextRange::Endpoint::InternalBoundaryType,IA2ProxyTextRange::Endpoint::UnitDirection,int,IA2ProxyTextRange::Endpoint::UnitBoundsRequired,bool)
0x00007fffe675b40a	(UIAutomationCore.DLL + 0x0026b40a)		IA2ProxyTextRange::Endpoint::GetUnitEndpoints(TextUnit,IA2ProxyTextRange::Endpoint::UnitDirection,IA2ProxyTextRange::Endpoint::UnitBoundsRequired)
0x00007fffe675e2fa	(UIAutomationCore.DLL + 0x0026e2fa)		IA2ProxyTextRange::Endpoint::MoveByUnit(TextUnit,int,IA2ProxyTextRange::Endpoint::UnitDirection,IA2ProxyTextRange::Endpoint::EndpointType,bool)
0x00007fffe675ea66	(UIAutomationCore.DLL + 0x0026ea66)		IA2ProxyTextRange::MoveEndpointByUnitInternal(TextPatternRangeEndpoint,TextUnit,int,bool)
0x00007fffe675e95f	(UIAutomationCore.DLL + 0x0026e95f)		IA2ProxyTextRange::MoveEndpointByUnit(TextPatternRangeEndpoint,TextUnit,int,int *)
0x00007fffe6654e25	(UIAutomationCore.DLL + 0x00164e25)		ProviderCallouts::MoveEndpointByUnit(ITextRangeProvider *,TextPatternRangeEndpoint,TextUnit,int,int *)
0x00007fffe6590e96	(UIAutomationCore.DLL + 0x000a0e96)		RemotePatternStub::TextRange_MoveEndpointByUnit(IUnknown *,IServerConnection *,BasicArrayPair<int> *,ITargetContextInvoker *,UIAutomationCoreProto::PatternMethodRequestMsg const &,UIAutomationCoreProto::PatternMethodResponseMsg &)
0x00007fffe658cdd9	(UIAutomationCore.DLL + 0x0009cdd9)		RemotePatternStub::OnMessage(IUnknown *,BasicArrayPair<int> *,ITargetContextInvoker *,IServerConnection *,Protocol_MethodId,UIAutomationCoreProto::PatternMethodRequestMsg const &,UIAutomationCoreProto::PatternMethodResponseMsg &)
0x00007fffe656f351	(UIAutomationCore.DLL + 0x0007f351)		InvokePatternMethodOnCorrectContext_Callback(void *)
0x00007fffe65187ce	(UIAutomationCore.DLL + 0x000287ce)		ComInvoker::CallTarget(long (*)(void *),void *)
0x00007fffe656f1db	(UIAutomationCore.DLL + 0x0007f1db)		InvokePatternMethodOnCorrectContext(IWeakReference *,BasicArrayPair<int> *,ITargetContextInvoker *,IServerConnection *,Protocol_MethodId,UIAutomationCoreProto::PatternMethodRequestMsg const &,UIAutomationCoreProto::PatternMethodResponseMsg &,ReleaseCollection *)
0x00007fffe656fd7b	(UIAutomationCore.DLL + 0x0007fd7b)		static  `anonymous namespace'::ProcessIncomingRequestNoThrow()
0x00007fffe656f8db	(UIAutomationCore.DLL + 0x0007f8db)		ProcessIncomingRequest(UIAutomationCoreProto::UiaCoreRequestMsg const &,UIAutomationCoreProto::UiaCoreResponseMsg &,IServerConnection *,unsigned int,Protocol_MethodId,ReleaseCollection *)
0x00007fffe64fa52c	(UIAutomationCore.DLL + 0x0000a52c)		HookBasedServerConnectionManager::HookCallback(void *,unsigned long,void * *,unsigned long *,void * *)
0x00007fffe652cdf6	(UIAutomationCore.DLL + 0x0003cdf6)		HookUtil<&HookBasedClientConnection::HookCallback(void *,unsigned long,void * *,unsigned long *,void * *),0>::CallOut(void *,unsigned long,void * *,unsigned long *,void * *)
0x00007fffe651982f	(UIAutomationCore.DLL + 0x0002982f)		HandleSyncHookMessage(tagCWPSTRUCT *,unsigned long,void (*)(void *,unsigned long,void * *,unsigned long *,void * *),void (*)(int,void *))
0x00007fffe6519486	(UIAutomationCore.DLL + 0x00029486)		HookUtil<&HookBasedClientConnection::HookCallback(void *,unsigned long,void * *,unsigned long *,void * *),0>::CallWndProc(int,unsigned __int64,__int64)
0x00007ffff9a24e4b	(user32.dll + 0x00024e4b)		fnHkINLPCWPSTRUCTW(tagWND *,unsigned int,unsigned __int64,__int64,unsigned __int64)
0x00007ffff9a2612c	(user32.dll + 0x0002612c)		_fnDWORD
0x00007ffffaed29e3	(ntdll.dll + 0x000a29e3)		KiUserCallbackDispatch
0x00007ffff8411063	(win32u.dll + 0x00001063)		NtUserPeekMessage
0x00007ffff9a11dc2	(user32.dll + 0x00011dc2)		_PeekMessage(tagMSG *,HWND__ *,unsigned int,unsigned int,unsigned int,unsigned int,int)
0x00007ffff9a11d2e	(user32.dll + 0x00011d2e)		PeekMessageW
0x00007fffcaf2665b	(chrome.dll -message_pump_win.cc:215)		base::MessagePumpForUI::DoRunLoop()
0x00007fffc7825e5a	(chrome.dll -message_pump_win.cc:78)		base::MessagePumpWin::Run(base::MessagePump::Delegate *)
0x00007fffc7d81259	(chrome.dll -thread_controller_with_message_pump_impl.cc:468)		base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool,base::TimeDelta)
0x00007fffc7f6b99c	(chrome.dll -run_loop.cc:140)		base::RunLoop::Run(base::Location const &)
0x00007fffc84bc998	(chrome.dll -browser_main_loop.cc:992)		content::BrowserMainLoop::RunMainMessageLoop()
0x00007fffc7fc2570	(chrome.dll -browser_main.cc:49)		content::BrowserMain(content::MainFunctionParams const &)
0x00007fffc7fc05ee	(chrome.dll -content_main_runner_impl.cc:1137)		content::ContentMainRunnerImpl::RunBrowser
0x00007fffc7fb611c	(chrome.dll -content_main_runner_impl.cc:1004)		content::ContentMainRunnerImpl::Run(bool)
0x00007fffc7c933d1	(chrome.dll -content_main.cc:418)		content::ContentMain(content::ContentMainParams const &)
0x00007fffc7c92579	(chrome.dll -chrome_main.cc:172)		ChromeMain
0x00007ff7404b8c3b	(chrome.exe -main_dll_loader_win.cc:170)		MainDllLoader::Launch(HINSTANCE__ *,base::TimeTicks)
0x00007ff7404b87c9	(chrome.exe -chrome_exe_main_win.cc:382)		wWinMain
0x00007ff74051fd81	(chrome.exe -exe_common.inl:288)		__scrt_common_main_seh


### fr...@gmail.com (2022-01-11)

[Comment Deleted]

### [Deleted User] (2022-01-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-12)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-01-14)

[Comment Deleted]

### fr...@gmail.com (2022-01-14)

sorry to bother you that , I awared we can use Clipboard in extension. That is to say In extension may be we can make  browser heap buffer overflow without manual Interaction.
I tried to make it without extension but did not acheived.
Is there a url to make a review of severity level i can have?
Thanks for your reading!
any how , the heap bufferoverflow is just hold on Ctrl+V is OK

### ks...@microsoft.com (2022-01-15)

Hey frustreated@, thanks for the excellent bug report!

I just put up a patch to fix this issue: https://chromium-review.googlesource.com/c/chromium/src/+/3390756

I have two potential mitigations for you in the mean time:

1) Disable the Windows Text Cursor Indicator - this is necessary for the crash, and the source of all of the calls into UIAutomationCore.DLL in the stack. This feature is off-by-default, so most users won't see this crash at all.

2) Keep the Text Cursor Indicator enabled but run Chrome with native UIA Automation enabled (this is under the command line flag --enable-experimental-ui-automation). This should avoid the crash, but you will lose the Text Cursor indicator in browser UI like the address bar.  

Once my fix lands and reaches a build, you can stop doing any mitigations.

### ks...@microsoft.com (2022-01-15)

[Empty comment from Monorail migration]

[Monorail components: UI>Accessibility>Compatibility]

### fr...@gmail.com (2022-01-15)

[Comment Deleted]

### fr...@gmail.com (2022-01-15)

[Comment Deleted]

### fr...@gmail.com (2022-01-18)

as I checked this guide

https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md

This Browser Process Heap Buffer Overflow can be tirggered without any special flag from full sandboxed render process.

And ALL we need to trigger this vul is to paste lines of words to text box.

we can search Mojo operations from https://source.chromium.org/ by key words of 
interface\s+\w+\s+{ f:\.mojom$ -f:test  paste 

and it did have some Mojom interfaces.

Even though , Chrome supports navigator.clipboard and document.execCommand.

So I think the security level can be High severity.

If this is not right , plz forget it .

### ks...@microsoft.com (2022-01-18)

Just wanted to make sure these factors are accounted for:

1. This relies on a non-default Windows accessibility setting (Show Text Cursor). Only a small % of users will have this enabled.

2. It should also only be possible on Windows (anything in UIAutomationCore required to trigger this is Windows-only)

Updating "OS" fields.

### fr...@gmail.com (2022-01-19)

On Windows Normal <input type="text"> can triggered and here is the poc and video.

It was first finded on Chrome Settings , so all the viedo and picture are make on Chrome Settings.
Sorry to give the later Info.

### fr...@gmail.com (2022-01-19)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-01-19)

here is the crash id 
Status:	Uploaded
Uploaded Crash Report ID:	df36313a4745601e
Upload Time:	Wednesday, January 19, 2022 at 10:34:21 AM
Local Crash Context:	fc7b669b-10d4-4ff3-898d-72008df5d8d9

### fr...@gmail.com (2022-01-19)

If it is convient , I think it's possible that https://crbug.com/chromium/1283417 have some similar with this Issue.
I am not very Sure, but from the video there is really some similar addresses (LowPart of x64 addr).

And that Issue is also triggered without any special flag with full sandbox lead to heap Buffer OverFlow.

If it is same ,feel free to merge to one issue.


### [Deleted User] (2022-02-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-02-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/59f90461bb82380a64e7a0b5a78b9221a5633176

commit 59f90461bb82380a64e7a0b5a78b9221a5633176
Author: Kurt Catti-Schmidt (SCHMIDT) <kschmi@microsoft.com>
Date: Sat Feb 05 03:11:07 2022

Fix AXPosition crash in AsLeafTextPositionBeforeCharacter

The cause of this crash occurs when iterating in
AsLeafTextPositionBeforeCharacter, because the check for
"text_position->AtEndOfAnchor" will never be correct for invalid
positions.

The proposed fix here is to simply return early for invalid positions.
There was already a similar check in AsLeafTextPositionAfterCharacter
for what looks like the same symptoms in this section:

// The following situation should not be possible but there are
// existing crashes in the field.
//
// TODO(nektar): Remove this workaround as soon as the source of
// the bug is identified.

A unit test was added for the new behaviors.

Bug: 1283701
Change-Id: I437955348b5df0d038a30ed7c2238dbb584b509b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3390756
Reviewed-by: Nektarios Paisios <nektar@chromium.org>
Commit-Queue: Kurt Catti-Schmidt <kschmi@microsoft.com>
Cr-Commit-Position: refs/heads/main@{#967576}

[modify] https://crrev.com/59f90461bb82380a64e7a0b5a78b9221a5633176/ui/accessibility/ax_node_position_unittest.cc
[modify] https://crrev.com/59f90461bb82380a64e7a0b5a78b9221a5633176/ui/accessibility/ax_position.h


### fr...@gmail.com (2022-03-16)

hello , long time no update.
no merge to stable ?
no cve?

### dr...@chromium.org (2022-03-16)

[Empty comment from Monorail migration]

### ks...@microsoft.com (2022-03-17)

Hey there! We haven't seen significant reports of this crash in the public, so we haven't had an urgent need to expedite it to stable. 

The fix is available in Canary and Beta, which will be promoted to stable in the next few weeks. 

I am not familiar with initiating the CVE process - adding timwillis@google.com - can you help out here?

### fr...@gmail.com (2022-03-19)

thanks!!!

### fr...@gmail.com (2022-03-20)

sadly to tell that the latest canary chrome did not patch well.

and i Test version 102.0.4953.0 (正式版本) canary （64 位） (cohort: Clang-64) 

we can still trigger crash .

### fr...@gmail.com (2022-03-20)

=================================================================
==13088==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12948a19f2b6 at pc 0x7ffd113825e3 bp 0x00ef50bfd9d0 sp 0x00ef50bfda18
READ of size 2 at 0x12948a19f2b6 thread T0
==13088==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffd113825e2 in gfx::IsValidCodePointIndex C:\b\s\w\ir\cache\builder\src\ui\gfx\utf16_indexing.cc:14
    #1 0x7ffd08831303 in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::AsLeafTextPositionBeforeCharacter C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:2598
    #2 0x7ffd0883948b in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreateBoundaryStartPosition C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:3074
    #3 0x7ffd088202c6 in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreateNextLineStartPosition C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:2873
    #4 0x7ffd08811a2f in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreatePositionAtTextBoundary C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:1894
    #5 0x7ffd0880f7ca in ui::AXPlatformNodeBase::FindTextBoundary C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_base.cc:2102
    #6 0x7ffd088b87ef in ui::AXPlatformNodeWin::FindBoundary C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:7686
    #7 0x7ffd088b823b in ui::AXPlatformNodeWin::IAccessibleTextGetTextForOffsetType C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:4313
    #8 0x7ffd088b89f2 in ui::AXPlatformNodeWin::get_textAtOffset C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:4368
    #9 0x7ffd5dea9309 in WindowPattern_WaitForInputIdle+0x702e9 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1801d9309)
    #10 0x7ffd5df36ee7 in WindowPattern_WaitForInputIdle+0xfdec7 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180266ee7)
    #11 0x7ffd5df36704 in WindowPattern_WaitForInputIdle+0xfd6e4 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180266704)
    #12 0x7ffd5de2439f in UiaRaiseNotificationEvent+0x470f (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18015439f)
    #13 0x7ffd5deb8c7b in WindowPattern_WaitForInputIdle+0x7fc5b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1801e8c7b)
    #14 0x7ffd5dd705fe in UiaRegisterProviderCallback+0x29fae (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1800a05fe)
    #15 0x7ffd5dd6cdd9 in UiaRegisterProviderCallback+0x26789 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18009cdd9)
    #16 0x7ffd5dd4f351 in UiaRegisterProviderCallback+0x8d01 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f351)
    #17 0x7ffd5dcf87ce  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1800287ce)
    #18 0x7ffd5dd4f1db in UiaRegisterProviderCallback+0x8b8b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f1db)
    #19 0x7ffd5dd4fd7b in UiaRegisterProviderCallback+0x972b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007fd7b)
    #20 0x7ffd5dd4f8db in UiaRegisterProviderCallback+0x928b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f8db)
    #21 0x7ffd5dcda52c  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18000a52c)
    #22 0x7ffd5dd0cdf6 in UiaReturnRawElementProvider+0xfa06 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18003cdf6)
    #23 0x7ffd5dcf982f  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18002982f)
    #24 0x7ffd5dcf9486  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180029486)
    #25 0x7ffd76524e4b in Ordinal2555+0x1fb (C:\Windows\System32\user32.dll+0x180024e4b)
    #26 0x7ffd7652612c in PostMessageW+0x10c (C:\Windows\System32\user32.dll+0x18002612c)
    #27 0x7ffd777929e3 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a29e3)
    #28 0x7ffd75111063 in NtUserPeekMessage+0x13 (C:\Windows\System32\win32u.dll+0x180001063)
    #29 0x7ffd76511dc2 in PeekMessageW+0x1d2 (C:\Windows\System32\user32.dll+0x180011dc2)
    #30 0x7ffd76511d2e in PeekMessageW+0x13e (C:\Windows\System32\user32.dll+0x180011d2e)
    #31 0x7ffd1090fcd1 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:494
    #32 0x7ffd1090f643 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:209
    #33 0x7ffd1090da28 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #34 0x7ffd1373ba60 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:497
    #35 0x7ffd107db323 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #36 0x7ffd09503b8d in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1070
    #37 0x7ffd095091d3 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:155
    #38 0x7ffd094fd10d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #39 0x7ffd1040c9d3 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:642
    #40 0x7ffd1040fb4c in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1154
    #41 0x7ffd1040ec7e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1021
    #42 0x7ffd1040b64b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:407
    #43 0x7ffd1040bdd4 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:435
    #44 0x7ffd054414ca in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:176
    #45 0x7ff6ad4f5b16 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #46 0x7ff6ad4f2b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:382
    #47 0x7ff6ad8ee3eb in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #48 0x7ffd76ea4ecf in BaseThreadInitThunk+0xf (C:\Windows\System32\KERNEL32.DLL+0x180014ecf)
    #49 0x7ffd7776e20a in RtlUserThreadStart+0x2a (C:\Windows\SYSTEM32\ntdll.dll+0x18007e20a)

0x12948a19f2b6 is located 646 bytes to the right of 20016-byte region [0x12948a19a200,0x12948a19f030)
allocated by thread T0 here:
    #0 0x7ff6ad59e58b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ffd231fd69e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ffd070bf4e5 in std::__1::basic_string<char16_t,std::__1::char_traits<char16_t>,std::__1::allocator<char16_t> >::__grow_by_and_replace C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\string:2255
    #3 0x7ffd070bf23d in std::__1::basic_string<char16_t,std::__1::char_traits<char16_t>,std::__1::allocator<char16_t> >::__assign_no_alias<1> C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\string:2319
    #4 0x7ffd11fa1167 in ui::AXNode::GetHypertext C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_node.cc:881
    #5 0x7ffd08824d5d in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::MaxTextOffset C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:4123
    #6 0x7ffd088271c1 in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::AsTreePosition C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:1325
    #7 0x7ffd0882a899 in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::AsLeafTreePosition C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:1426
    #8 0x7ffd0882914d in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::IsIgnored C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:473
    #9 0x7ffd11fc879e in ui::`anonymous namespace'::ComputeUnignoredSelectionEndpoint C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_tree.cc:2622
    #10 0x7ffd11fc8314 in ui::AXTree::GetUnignoredSelection C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_tree.cc:2674
    #11 0x7ffd092c9c1b in content::BrowserAccessibility::GetUnignoredSelection C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility.cc:1360
    #12 0x7ffd0880e1aa in ui::AXPlatformNodeBase::GetSelectionOffsets C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_base.cc:1893
    #13 0x7ffd088b6b75 in ui::AXPlatformNodeWin::get_caretOffset C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:4194
    #14 0x7ffd5df36dc6 in WindowPattern_WaitForInputIdle+0xfdda6 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180266dc6)
    #15 0x7ffd5df385c8 in WindowPattern_WaitForInputIdle+0xff5a8 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1802685c8)
    #16 0x7ffd5df36e83 in WindowPattern_WaitForInputIdle+0xfde63 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180266e83)
    #17 0x7ffd5df36704 in WindowPattern_WaitForInputIdle+0xfd6e4 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180266704)
    #18 0x7ffd5de2439f in UiaRaiseNotificationEvent+0x470f (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18015439f)
    #19 0x7ffd5deb8c7b in WindowPattern_WaitForInputIdle+0x7fc5b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1801e8c7b)
    #20 0x7ffd5dd705fe in UiaRegisterProviderCallback+0x29fae (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1800a05fe)
    #21 0x7ffd5dd6cdd9 in UiaRegisterProviderCallback+0x26789 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18009cdd9)
    #22 0x7ffd5dd4f351 in UiaRegisterProviderCallback+0x8d01 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f351)
    #23 0x7ffd5dcf87ce  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1800287ce)
    #24 0x7ffd5dd4f1db in UiaRegisterProviderCallback+0x8b8b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f1db)
    #25 0x7ffd5dd4fd7b in UiaRegisterProviderCallback+0x972b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007fd7b)
    #26 0x7ffd5dd4f8db in UiaRegisterProviderCallback+0x928b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f8db)
    #27 0x7ffd5dcda52c  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18000a52c)

SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\ui\gfx\utf16_indexing.cc:14 in gfx::IsValidCodePointIndex
Shadow bytes around the buggy address:
  0x0493179b3e00: 00 00 00 00 00 00 fa fa fa fa fa fa fa fa fa fa
  0x0493179b3e10: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0493179b3e20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0493179b3e30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0493179b3e40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x0493179b3e50: fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa fa fa
  0x0493179b3e60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0493179b3e70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0493179b3e80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0493179b3e90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0493179b3ea0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==13088==ABORTING

### fr...@gmail.com (2022-03-20)

the crash is the same to https://crbug.com/chromium/1283417.

and the tirgger methord is not changed.

### fr...@gmail.com (2022-03-25)

[Comment Deleted]

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-06-10)

Security marshal here. kschmi@, are you able to reproduce the crashing as noted in frustreated@'s recent comments?

### ks...@microsoft.com (2022-06-13)

I cannot reproduce this crash in 105.0.5119.0

I enabled the Text Cursor Indicator in Windows settings on both Windows 10 and Windows 11 and am unable to reproduce any related crashes (or DCHECK's) via typing in a text input. I launched Chrome with and without --enable-experimental-ui-automation enabled. Either way, I am unable to reproduce. I tried typing in the google.com search box as well as a blank <textarea> and a few other text inputs and was unable to reproduce this crash. I also tried the latest ASAN build under https://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=win32-release_x64/ and was unable to repro.

The fix listed above was in the code that frustreated@gmail.com listed in the call stack provided, so the issue identified in this bug appears to be fixed.

I did discover a different issue in cs.chromium.org when testing there - I opened 1336043. It's a DCHECK, and it seems harmless in this case, so it's not a security issue. It doesn't hit under ASAN because ASAN is release only (so no DCHECK's), however it does give more reassurance that 1336043 is not a security issue.

I'm going to mark this bug as fixed and close it out. frustreated@, if you are able to provide a repro that shows the stack above, please reactivate, with updated repro steps.

### th...@chromium.org (2022-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-06-15)

the latest stable release is not patched .
I will check the version you provieded today.
thanks for your check!!


### fr...@gmail.com (2022-06-15)

the latest version of 
Chromium	105.0.5121.0 (开发者内部版本) （64 位）
is not patched 
here is the video

when we are going to reproduce this in asan version chrome ,it is not very fast to trigger, may be there are more check or something else eating the cpu of pc.

here is the video


### fr...@gmail.com (2022-06-15)

if possible plz make reporter as 


CREDIT INFORMATION
Reporter credit: avboy1337

### fr...@gmail.com (2022-06-15)

and this time its going to be another issue type uaf as folloging 


C:\Users\Administrator\Desktop\asan-win32-release_x64-1014184>chrome.exe --user-data-dir=./userdata
[1468:1908:0615/090820.523:ERROR:device_event_log_impl.cc(214)] [09:08:20.522] Bluetooth: bluetooth_adapter_winrt.cc:1074 Getting Default Adapter failed.
=================================================================
==1468==ERROR: AddressSanitizer: heap-use-after-free on address 0x11e85a265a82 at pc 0x7ff8271b283f bp 0x0091a6ffd950 sp 0x0091a6ffd998
READ of size 2 at 0x11e85a265a82 thread T0
==1468==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ff8271b283e in gfx::IsValidCodePointIndex C:\b\s\w\ir\cache\builder\src\ui\gfx\utf16_indexing.cc:14
    #1 0x7ff81e15be5f in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::AsLeafTextPositionBeforeCharacter C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:2578
    #2 0x7ff81e163dc5 in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreateBoundaryStartPosition C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:3058
    #3 0x7ff81e14bafc in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreateNextLineStartPosition C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:2857
    #4 0x7ff81e13c7e7 in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreatePositionAtTextBoundary C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:1893
    #5 0x7ff81e13a584 in ui::AXPlatformNodeBase::FindTextBoundary C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_base.cc:2174
    #6 0x7ff81e1e16c7 in ui::AXPlatformNodeWin::FindBoundary C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:7795
    #7 0x7ff81e1e1113 in ui::AXPlatformNodeWin::IAccessibleTextGetTextForOffsetType C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:4270
    #8 0x7ff81e1e18ca in ui::AXPlatformNodeWin::get_textAtOffset C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:4325
    #9 0x7ff85fa69309 in WindowPattern_WaitForInputIdle+0x702e9 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1801d9309)
    #10 0x7ff85faf6ee7 in WindowPattern_WaitForInputIdle+0xfdec7 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180266ee7)
    #11 0x7ff85faf6704 in WindowPattern_WaitForInputIdle+0xfd6e4 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180266704)
    #12 0x7ff85f9e439f in UiaRaiseNotificationEvent+0x470f (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18015439f)
    #13 0x7ff85fa78c7b in WindowPattern_WaitForInputIdle+0x7fc5b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1801e8c7b)
    #14 0x7ff85f9305fe in UiaRegisterProviderCallback+0x29fae (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1800a05fe)
    #15 0x7ff85f92cdd9 in UiaRegisterProviderCallback+0x26789 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18009cdd9)
    #16 0x7ff85f90f351 in UiaRegisterProviderCallback+0x8d01 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f351)
    #17 0x7ff85f8b87ce  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1800287ce)
    #18 0x7ff85f90f1db in UiaRegisterProviderCallback+0x8b8b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f1db)
    #19 0x7ff85f90fd7b in UiaRegisterProviderCallback+0x972b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007fd7b)
    #20 0x7ff85f90f8db in UiaRegisterProviderCallback+0x928b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f8db)
    #21 0x7ff85f89a52c  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18000a52c)
    #22 0x7ff85f8ccdf6 in UiaReturnRawElementProvider+0xfa06 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18003cdf6)
    #23 0x7ff85f8b982f  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18002982f)
    #24 0x7ff85f8b9486  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180029486)
    #25 0x7ff874834e4b in Ordinal2555+0x1fb (C:\Windows\System32\user32.dll+0x180024e4b)
    #26 0x7ff87483612c in PostMessageW+0x10c (C:\Windows\System32\user32.dll+0x18002612c)
    #27 0x7ff875dd29e3 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a29e3)
    #28 0x7ff873b31063 in NtUserPeekMessage+0x13 (C:\Windows\System32\win32u.dll+0x180001063)
    #29 0x7ff874821dc2 in PeekMessageW+0x1d2 (C:\Windows\System32\user32.dll+0x180011dc2)
    #30 0x7ff874821d2e in PeekMessageW+0x13e (C:\Windows\System32\user32.dll+0x180011d2e)
    #31 0x7ff82677005b in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:494
    #32 0x7ff82676f993 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:209
    #33 0x7ff82676dce4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #34 0x7ff8295500c2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:535
    #35 0x7ff8266208a7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #36 0x7ff81efe74e7 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1039
    #37 0x7ff81efec8cb in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:157
    #38 0x7ff81efe0a2d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #39 0x7ff8261d7c5f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:678
    #40 0x7ff8261dafb5 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1188
    #41 0x7ff8261da0d3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1059
    #42 0x7ff8261d68d7 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:407
    #43 0x7ff8261d7060 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:435
    #44 0x7ff81ada14be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #45 0x7ff7fb6d5d52 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #46 0x7ff7fb6d2b74 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:385
    #47 0x7ff7fbadc4df in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #48 0x7ff874f04ecf in BaseThreadInitThunk+0xf (C:\Windows\System32\KERNEL32.DLL+0x180014ecf)
    #49 0x7ff875dae20a in RtlUserThreadStart+0x2a (C:\Windows\SYSTEM32\ntdll.dll+0x18007e20a)

0x11e85a265a82 is located 6274 bytes inside of 20016-byte region [0x11e85a264200,0x11e85a269030)
freed by thread T0 here:
    #0 0x7ff7fb77e13b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff8201b47c6 in content::BrowserAccessibilityComWin::UpdateStep1ComputeWinAttributes C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_com_win.cc:1476
    #2 0x7ff8201b9e46 in content::BrowserAccessibilityManagerWin::OnAtomicUpdateFinished C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager_win.cc:741
    #3 0x7ff827d78d67 in ui::AXTree::Unserialize C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_tree.cc:1332
    #4 0x7ff81edaee72 in content::BrowserAccessibilityManager::Unserialize C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager.cc:225
    #5 0x7ff81edb0952 in content::BrowserAccessibilityManager::OnAccessibilityEvents C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager.cc:460
    #6 0x7ff81fbafd69 in content::RenderFrameHostImpl::HandleAXEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_impl.cc:7789
    #7 0x7ff81edcb9f8 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::*)(const ui::AXTreeID &, mojo::StructPtr<content::mojom::AXUpdatesAndEvents>, int),base::WeakPtr<content::RenderFrameHostImpl>,ui::AXTreeID,mojo::StructPtr<content::mojom::AXUpdatesAndEvents>,int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:749
    #8 0x7ff82955fa0f in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post_task_and_reply_impl.cc:100
    #9 0x7ff829560253 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:749
    #10 0x7ff8266bfe84 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #11 0x7ff82954e5bd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:408
    #12 0x7ff82954d7ba in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:286
    #13 0x7ff82676fa36 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:214
    #14 0x7ff82676dce4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #15 0x7ff8295500c2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:535
    #16 0x7ff8266208a7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #17 0x7ff81efe74e7 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1039
    #18 0x7ff81efec8cb in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:157
    #19 0x7ff81efe0a2d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #20 0x7ff8261d7c5f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:678
    #21 0x7ff8261dafb5 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1188
    #22 0x7ff8261da0d3 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1059
    #23 0x7ff8261d68d7 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:407
    #24 0x7ff8261d7060 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:435
    #25 0x7ff81ada14be in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:177
    #26 0x7ff7fb6d5d52 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:167
    #27 0x7ff7fb6d2b74 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:385

previously allocated by thread T0 here:
    #0 0x7ff7fb77e23b in malloc C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:98
    #1 0x7ff839aff32e in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new_scalar.cpp:35
    #2 0x7ff81d9f4c37 in std::Cr::basic_string<char16_t,std::Cr::char_traits<char16_t>,std::Cr::allocator<char16_t> >::__grow_by C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\string:2282
    #3 0x7ff8266a3767 in std::Cr::basic_string<char16_t,std::Cr::char_traits<char16_t>,std::Cr::allocator<char16_t> >::assign<const char *> C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\string:2486
    #4 0x7ff82669c28a in base::UTF8ToUTF16 C:\b\s\w\ir\cache\builder\src\base\strings\utf_string_conversions.cc:223
    #5 0x7ff82669c87d in base::UTF8ToUTF16 C:\b\s\w\ir\cache\builder\src\base\strings\utf_string_conversions.cc:230
    #6 0x7ff81ed9fa52 in content::BrowserAccessibility::GetValueForControl C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility.cc:924
    #7 0x7ff81e12fa81 in ui::AXPlatformNodeBase::GetValueForControl C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_base.cc:1196
    #8 0x7ff8201b461f in content::BrowserAccessibilityComWin::UpdateStep1ComputeWinAttributes C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_com_win.cc:1476
    #9 0x7ff8201b9e46 in content::BrowserAccessibilityManagerWin::OnAtomicUpdateFinished C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager_win.cc:741
    #10 0x7ff827d78d67 in ui::AXTree::Unserialize C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_tree.cc:1332
    #11 0x7ff81edaee72 in content::BrowserAccessibilityManager::Unserialize C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager.cc:225
    #12 0x7ff81edb0952 in content::BrowserAccessibilityManager::OnAccessibilityEvents C:\b\s\w\ir\cache\builder\src\content\browser\accessibility\browser_accessibility_manager.cc:460
    #13 0x7ff81fbafd69 in content::RenderFrameHostImpl::HandleAXEvents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\render_frame_host_impl.cc:7789
    #14 0x7ff81edcb9f8 in base::internal::Invoker<base::internal::BindState<void (content::RenderFrameHostImpl::*)(const ui::AXTreeID &, mojo::StructPtr<content::mojom::AXUpdatesAndEvents>, int),base::WeakPtr<content::RenderFrameHostImpl>,ui::AXTreeID,mojo::StructPtr<content::mojom::AXUpdatesAndEvents>,int>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:749
    #15 0x7ff82955fa0f in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post_task_and_reply_impl.cc:100
    #16 0x7ff829560253 in base::internal::Invoker<base::internal::BindState<void (*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:749
    #17 0x7ff8266bfe84 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135
    #18 0x7ff82954e5bd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:408
    #19 0x7ff82954d7ba in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:286
    #20 0x7ff82676fa36 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:214
    #21 0x7ff82676dce4 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #22 0x7ff8295500c2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:535
    #23 0x7ff8266208a7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #24 0x7ff81efe74e7 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1039
    #25 0x7ff81efec8cb in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:157
    #26 0x7ff81efe0a2d in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #27 0x7ff8261d7c5f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:678

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\ui\gfx\utf16_indexing.cc:14 in gfx::IsValidCodePointIndex
Shadow bytes around the buggy address:
  0x03d1653ccb00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03d1653ccb10: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03d1653ccb20: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03d1653ccb30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03d1653ccb40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x03d1653ccb50:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03d1653ccb60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03d1653ccb70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03d1653ccb80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03d1653ccb90: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x03d1653ccba0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==1468==ABORTING

### fr...@gmail.com (2022-06-15)

[Comment Deleted]

### fr...@gmail.com (2022-06-15)

as this issue was make Status Closed , i have to make a new issue as uaf here
 https://crbug.com/chromium/1336495


### aj...@google.com (2022-06-22)

this may not be fixed yet, will investigate.

### aj...@chromium.org (2022-06-22)

Hi frustreated - could you let us know the Windows version you are using - this might help us develop our own repro

### aj...@chromium.org (2022-06-22)

[Empty comment from Monorail migration]

### aj...@chromium.org (2022-06-22)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-06-24)

the latest version of Chromium	105.0.5141.0 (开发者内部版本) （64 位）is not patched 


==14176==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x12557bc9fbbe at pc 0x7ffb2d61b0df bp 0x00563b3fde30 sp 0x00563b3fde78
READ of size 2 at 0x12557bc9fbbe thread T0
==14176==WARNING: Failed to use and restart external symbolizer!
    #0 0x7ffb2d61b0de in gfx::IsValidCodePointIndex C:\b\s\w\ir\cache\builder\src\ui\gfx\utf16_indexing.cc:14
    #1 0x7ffb245f6817 in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::AsLeafTextPositionBeforeCharacter C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:2578
    #2 0x7ffb245fe61e in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreateBoundaryStartPosition C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:3058
    #3 0x7ffb245e63b2 in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreateNextLineStartPosition C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:2857
    #4 0x7ffb245d71eb in ui::AXPosition<ui::AXNodePosition,ui::AXNode>::CreatePositionAtTextBoundary C:\b\s\w\ir\cache\builder\src\ui\accessibility\ax_position.h:1893
    #5 0x7ffb245d4f82 in ui::AXPlatformNodeBase::FindTextBoundary C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_base.cc:2174
    #6 0x7ffb2467cdc1 in ui::AXPlatformNodeWin::FindBoundary C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:7811
    #7 0x7ffb2467c80d in ui::AXPlatformNodeWin::IAccessibleTextGetTextForOffsetType C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:4282
    #8 0x7ffb2467cfc4 in ui::AXPlatformNodeWin::get_textAtOffset C:\b\s\w\ir\cache\builder\src\ui\accessibility\platform\ax_platform_node_win.cc:4337
    #9 0x7ffbc7149309 in WindowPattern_WaitForInputIdle+0x702e9 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1801d9309)
    #10 0x7ffbc71d6ee7 in WindowPattern_WaitForInputIdle+0xfdec7 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180266ee7)
    #11 0x7ffbc71d6704 in WindowPattern_WaitForInputIdle+0xfd6e4 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180266704)
    #12 0x7ffbc70c439f in UiaRaiseNotificationEvent+0x470f (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18015439f)
    #13 0x7ffbc7158c7b in WindowPattern_WaitForInputIdle+0x7fc5b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1801e8c7b)
    #14 0x7ffbc70105fe in UiaRegisterProviderCallback+0x29fae (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1800a05fe)
    #15 0x7ffbc700cdd9 in UiaRegisterProviderCallback+0x26789 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18009cdd9)
    #16 0x7ffbc6fef351 in UiaRegisterProviderCallback+0x8d01 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f351)
    #17 0x7ffbc6f987ce  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x1800287ce)
    #18 0x7ffbc6fef1db in UiaRegisterProviderCallback+0x8b8b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f1db)
    #19 0x7ffbc6fefd7b in UiaRegisterProviderCallback+0x972b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007fd7b)
    #20 0x7ffbc6fef8db in UiaRegisterProviderCallback+0x928b (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18007f8db)
    #21 0x7ffbc6f7a52c  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18000a52c)
    #22 0x7ffbc6facdf6 in UiaReturnRawElementProvider+0xfa06 (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18003cdf6)
    #23 0x7ffbc6f9982f  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x18002982f)
    #24 0x7ffbc6f99486  (C:\Windows\SYSTEM32\UIAutomationCore.DLL+0x180029486)
    #25 0x7ffbe7c44e4b in Ordinal2555+0x1fb (C:\Windows\System32\user32.dll+0x180024e4b)
    #26 0x7ffbe7c4612c in PostMessageW+0x10c (C:\Windows\System32\user32.dll+0x18002612c)
    #27 0x7ffbe7eb29e3 in KiUserCallbackDispatcher+0x23 (C:\Windows\SYSTEM32\ntdll.dll+0x1800a29e3)
    #28 0x7ffbe55d1063 in NtUserPeekMessage+0x13 (C:\Windows\System32\win32u.dll+0x180001063)
    #29 0x7ffbe7c31dc2 in PeekMessageW+0x1d2 (C:\Windows\System32\user32.dll+0x180011dc2)
    #30 0x7ffbe7c31d2e in PeekMessageW+0x13e (C:\Windows\System32\user32.dll+0x180011d2e)
    #31 0x7ffb2cbfaec1 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:494
    #32 0x7ffb2cbfa78f in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:209
    #33 0x7ffb2cbf8929 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78
    #34 0x7ffb2f9d29dd in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:554
    #35 0x7ffb2cabd13f in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:141
    #36 0x7ffb2547db55 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc:1036
    #37 0x7ffb25482ab7 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_runner_impl.cc:157
    #38 0x7ffb25476b81 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser_main.cc:30
    #39 0x7ffb2c6740a7 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:678
    #40 0x7ffb2c677583 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1188
    #41 0x7ffb2c676638 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc:1059
    #42 0x7ffb2c672d3f in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:407
    #43 0x7ffb2c6734a9 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc:435
    #44 0x7ffb212514ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc:182
    #45 0x7ff70e6f56fe in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc:162
    #46 0x7ff70e6f2ae4 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc:395
    #47 0x7ff70eaf809f in __scrt_common_main_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288
    #48 0x7ffbe5fd4ecf in BaseThreadInitThunk+0xf (C:\Windows\System32\KERNEL32.DLL+0x180014ecf)
    #49 0x7ffbe7e8e20a in RtlUserThreadStart+0x2a (C:\Windows\SYSTEM32\ntdll.dll+0x18007e20a)

Address 0x12557bc9fbbe is a wild pointer inside of access range of size 0x000000000002.
SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\s\w\ir\cache\builder\src\ui\gfx\utf16_indexing.cc:14 in gfx::IsValidCodePointIndex
Shadow bytes around the buggy address:
  0x044c2b393f20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044c2b393f30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044c2b393f40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044c2b393f50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044c2b393f60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x044c2b393f70: fa fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa fa
  0x044c2b393f80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044c2b393f90: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044c2b393fa0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044c2b393fb0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x044c2b393fc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==14176==ABORTING

### [Deleted User] (2022-06-24)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2022-06-25)

Thanks - could you provide your /Windows/ Version?

### fr...@gmail.com (2022-06-25)

Server 2022 21H 20348.169

### [Deleted User] (2022-06-25)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ks...@microsoft.com (2022-06-29)

I was finally able to reproduce this. I had some difficulties getting an ASAN build to work, and from there, it's still difficult for me to repro.

It seems that my fix in https://chromium-review.googlesource.com/c/chromium/src/+/3390756 made it less likely to occur, but that there's still a window where this is possible.

The crash is in:

gfx::IsValidCodePointIndex(
                  text_position->GetText(),
                  static_cast<size_t>(text_position->text_offset_)

text_position->text_offset_ is beyond MaxTextOffset, hence the buffer-overflow/crash.

Nektarios@, is it possible for the AsLeafTextPosition call here to convert a valid position to one that goes beyond MaxTextOffset? I was considering moving the MaxTextOffset check I added to be after the AsLeafTextPosition call, but I want to make sure that's going to be a complete fix.

My repro is as follows:

1. Enable Windows Text Cursor Indicator https://www.how2shout.com/how-to/enable-text-cursor-indicator-windows-10.html
2. Navigate to chrome://settings
3. Paste a very long string repeatedly in the search box (pasting a mix of Unicode and ASCII characters seems to make this more reproducible).

Also, I'm going to be away all next week and partially this week. So Nektarios, I am assigning this one over to you, as I won't be able to work on it for a bit. If you don't have a chance to fix this by the time I'm back (7/11), I can pick it back up. 

### [Deleted User] (2022-06-30)

nektar: Uh oh! This issue still open and hasn't been updated in the last 180 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aj...@chromium.org (2022-06-30)

(might calm down the bot)

### [Deleted User] (2022-07-14)

nektar: Uh oh! This issue still open and hasn't been updated in the last 194 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### fr...@gmail.com (2022-09-01)

[Comment Deleted]

### fr...@gmail.com (2022-09-24)

is there any update please

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### fl...@google.com (2022-10-06)

Heya kschmi@, would you be willing to take this one on again?  Chatted with Nektar and I don't think they have the cycles for it right now.

### fr...@gmail.com (2022-10-18)

I think this was patched , and now there is going to be a stable crash , but there is no info about over flow tips.

### fr...@gmail.com (2022-11-13)

any update?
now it is 107 version .
really a long time no updates.

### aj...@chromium.org (2022-11-14)

I am not able to reproduce this in current Chrome stable. As indicated in https://crbug.com/chromium/1283701#c80 this relies on a non-default setting on Windows and very unusual user gestures.

### fr...@gmail.com (2022-11-15)

i am tired to argu about this issue

01-the first time this issue occured , we can crash browser from render process , no need to triger it from chrome://settings ,we can see the viedo here https://bugs.chromium.org/p/chromium/issues/detail?id=1283701#c64
may be we can say it is not possible happend from this unusual user gestures.

But I think this is not a easy case as usual.

02-then https://crbug.com/chromium/1283701 was closed , but i find it did not patched successfully just like https://bugs.chromium.org/p/chromium/issues/detail?id=1283701#c94

Again, also from this method(just like https://bugs.chromium.org/p/chromium/issues/detail?id=1283701#c110 said : unusual user gestures) , we can trigger another issue of use after free ,although it was patched in https://bugs.chromium.org/p/chromium/issues/detail?id=1336495#c_ts1655342292 and https://bugs.chromium.org/p/chromium/issues/detail?id=1333970
these two issues are Duplicated ,so plz lets say that the issue trigger methord used very unusual user gestures.

I think its just because I just use this very unusual methord to find the uaf and this heap buffer overflow. But the same issue can be triggerd by different methords as the Duplicated uaf.
Some times we just solved problems with different methords and i just tried my best to updated these info to google as soon as possible.


Some other software like teams also not patched this unusual user gestures problem.
wish you lucky.

### am...@chromium.org (2022-11-17)

Due to the high level of mitigations here, updating to severity-low 

### am...@google.com (2022-11-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-18)

Congratulations! The VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug. A member of our finance team will be in touch with you to arrange payment. In the interim, please let us know what name/handle/tag/other identifier you would like us to use in acknowledging you for this issue. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-11-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-14)

While there is a fix for this that made the crash less likely to occur, it seems that we were unable to fully reproduce the reported issue and were no longer to even after it was reportedly reproducible. It moreso seems that triggering this issue would require a series of implausible user gestures. Therefore, I don't consider this issue "fixed" but also this does not appear that it is a potentially exploitable security issue given the progression of this report. To accurately reflect the report and actions, updating this issue to a Bug.

### fr...@gmail.com (2022-12-24)

don't wanna to prove it any more. do as what you want and help yourself.

### [Deleted User] (2023-02-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@google.com (2023-11-13)

Thanks for submitting this. I see that it is fixed in a newer version of Chrome. I’m resolving this bug now since the fix will be coming to you soon. If you have further questions or concerns, please feel free to reopen this bug or open a new one and I’ll be happy to look into it further.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1283701?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### am...@chromium.org (2024-05-20)

Hello -- the finance team did not receive a response from their attempts to process this reward payment to you. As is our policy for abandoned rewards, this reward amount is being doubled and donated to a charitable cause.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40813839)*
