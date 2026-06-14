# Security: Crash in content::SpeechRecognitionDispatcher::OnRecognitionEnded()

| Field | Value |
|-------|-------|
| **Issue ID** | [40091012](https://issues.chromium.org/issues/40091012) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Speech |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2018-04-05 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 67.0.3388.0 (Official Build) canary (64-bit)  

Operating System: Mac

**REPRODUCTION CASE**

1. Load the testcase.html
2. Click on the button and wait >> crash!

Received signal 11 SEGV\_MAPERR ffffd132953259b4  

#0 0x55555953af7c base::debug::StackTrace::StackTrace()  

#1 0x55555953aae1 base::debug::(anonymous namespace)::StackDumpSignalHandler()  

#2 0x7ffff7bcb390 <unknown>  

#3 0x55555cd861cf content::SpeechRecognitionDispatcher::OnRecognitionEnded()  

#4 0x55555cd86060 *ZN3IPC8MessageTI31SpeechRecognitionMsg\_Ended\_MetaNSt3\_\_15tupleIJiEEEvE8DispatchIN7content27SpeechRecognitionDispatcherES8\_vMS8\_FviEEEbPKNS\_7MessageEPT\_PT0\_PT1\_T2*  

#5 0x55555cd8529f content::SpeechRecognitionDispatcher::OnMessageReceived()  

#6 0x55555c7fa856 content::RenderFrameImpl::OnMessageReceived()  

#7 0x555559aaf3ab IPC::ChannelProxy::Context::OnDispatchMessage()  

#8 0x55555953c2fd base::debug::TaskAnnotator::RunTask()  

#9 0x555559178222 blink::scheduler::internal::ThreadControllerImpl::DoWork()  

#10 0x55555953c2fd base::debug::TaskAnnotator::RunTask()  

#11 0x555559557767 base::MessageLoop::RunTask()  

#12 0x555559557c47 base::MessageLoop::DoWork()  

#13 0x555559559d0a base::MessagePumpDefault::Run()  

#14 0x55555957a385 base::RunLoop::Run()  

#15 0x55555cd524e0 content::RendererMain()  

#16 0x55555927648e content::RunZygote()  

#17 0x5555592775b8 content::ContentMainRunnerImpl::Run()  

#18 0x5555592811f4 service\_manager::Main()  

#19 0x5555592761e4 content::ContentMain()  

#20 0x5555578e11b3 ChromeMain  

#21 0x7ffff1c83830 \_\_libc\_start\_main

WinDbg output:

rax=000007fe00000001 rbx=00000000003adc08 rcx=00000000057b11b8  

rdx=00000000003adc08 rsi=000000000577e190 rdi=000000000577e1c0  

rip=000007feefaa4d7b rsp=00000000003adbe0 rbp=0000000000000000  

r8=00000fa905e2017e r9=00000faa04a6017f r10=0000000000ff0000  

r11=0000000000005253 r12=000007feefaa4ce4 r13=00000000003ae308  

r14=00000000003ae310 r15=00000000003ae280  

iopl=0 nv up ei pl nz na pe nc  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00010202  

chrome\_child!IsSandboxedProcess+0x81c627:  

000007fe`efaa4d7b ff5040 call qword ptr [rax+40h] ds:000007fe`00000041=????????????????

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 643 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 654.6 KB)

## Timeline

### ch...@gmail.com (2018-04-05)

This is a regression issue as it is observed from M67.

### ch...@gmail.com (2018-04-05)

- This seems like a UaF vulnerability.

=================================================================
==3444==ERROR: AddressSanitizer: heap-use-after-free on address 0x012340da8f60 at pc 0x07fed176cbd6 bp 0x00000024c170 sp 0x00
000024c1b8
READ of size 8 at 0x012340da8f60 thread T0
    #0 0x7fed176cbd5  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18640cbd5)
    #1 0x7fed17618db  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1864018db)
    #2 0x7fed17624db  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1864024db)
    #3 0x7fed1762492  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x186402492)
    #4 0x7fed1710a2f  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863b0a2f)
    #5 0x7fed1711ca1  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863b1ca1)
    #6 0x7fed16ddbad  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18637dbad)
    #7 0x7fed16ddad7  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18637dad7)
    #8 0x7fed16d94d2  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863794d2)
    #9 0x7fed16d1946  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x186371946)
    #10 0x7fed16e1713  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x186381713)
    #11 0x7fed16e92ac  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863892ac)
    #12 0x7fecec13f14  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1838b3f14)
    #13 0x7feceba5716  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183845716)
    #14 0x7fecebb2ba9  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183852ba9)
    #15 0x7fecebb569b  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18385569b)
    #16 0x7feceb53011  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1837f3011)
    #17 0x7feccc3a837  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818da837)
    #18 0x7feccc4222c  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818e222c)
    #19 0x7feccc2d5c8  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818cd5c8)
    #20 0x7fece87a415  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18351a415)
    #21 0x7fece87b5a6  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18351b5a6)
    #22 0x7fece8e7b68  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183587b68)
    #23 0x7fece87a06a  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18351a06a)
    #24 0x7fecb3613e7  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1800013e7)
    #25 0x13f837ccc  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140007ccc)
    #26 0x13f832349  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140002349)
    #27 0x13fb76d28  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140346d28)
    #28 0x76d7f56c  (C:\Windows\system32\kernel32.dll+0x78d3f56c)
    #29 0x76fb3280  (C:\Windows\SYSTEM32\ntdll.dll+0x78e83280)

0x012340da8f60 is located 32 bytes inside of 256-byte region [0x012340da8f40,0x012340da9040)
freed by thread T0 here:
    #0 0x13f86a320  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x14003a320)
    #1 0x7fed170f565  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863af565)
    #2 0x7fed170f5a5  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863af5a5)
    #3 0x7fed1710a0e  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863b0a0e)
    #4 0x7fed1711ca1  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863b1ca1)
    #5 0x7fed16ddbad  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18637dbad)
    #6 0x7fed16ddad7  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18637dad7)
    #7 0x7fed16d94d2  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863794d2)
    #8 0x7fed16d1946  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x186371946)
    #9 0x7fed16e1713  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x186381713)
    #10 0x7fed16e92ac  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1863892ac)
    #11 0x7fecec13f14  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1838b3f14)
    #12 0x7feceba5716  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183845716)
    #13 0x7fecebb2ba9  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183852ba9)
    #14 0x7fecebb569b  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18385569b)
    #15 0x7feceb53011  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1837f3011)
    #16 0x7feccc3a837  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818da837)
    #17 0x7feccc4222c  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818e222c)
    #18 0x7feccc2d5c8  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818cd5c8)
    #19 0x7fece87a415  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18351a415)
    #20 0x7fece87b5a6  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18351b5a6)
    #21 0x7fece8e7b68  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183587b68)
    #22 0x7fece87a06a  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18351a06a)
    #23 0x7fecb3613e7  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1800013e7)
    #24 0x13f837ccc  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140007ccc)
    #25 0x13f832349  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140002349)
    #26 0x13fb76d28  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140346d28)
    #27 0x76d7f56c  (C:\Windows\system32\kernel32.dll+0x78d3f56c)
    #28 0x76fb3280  (C:\Windows\SYSTEM32\ntdll.dll+0x78e83280)

previously allocated by thread T44 here:
    #0 0x13f86a4e5  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x14003a4e5)
    #1 0x7fed1763c1c  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x186403c1c)
    #2 0x7fed16e0f37  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x186380f37)
    #3 0x7fed16f3308  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x186393308)
    #4 0x7fecef881cb  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c281cb)
    #5 0x7fecef8e1b5  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c2e1b5)
    #6 0x7fecef8c9e7  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c2c9e7)
    #7 0x7fecefa89e0  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c489e0)
    #8 0x7feced2274f  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1839c274f)
    #9 0x13f861f18  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140031f18)
    #10 0x76d7f56c  (C:\Windows\system32\kernel32.dll+0x78d3f56c)
    #11 0x76fb3280  (C:\Windows\SYSTEM32\ntdll.dll+0x78e83280)

Thread T44 created by T3 here:
    #0 0x13f860e40  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140030e40)
    #1 0x7feced21cab  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1839c1cab)
    #2 0x7fecefa773a  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c4773a)
    #3 0x7fecefa7384  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c47384)
    #4 0x7fecef9c753  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c3c753)
    #5 0x7fecefa056f  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c4056f)
    #6 0x7fecef9d0d6  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c3d0d6)
    #7 0x7fecefa4174  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c44174)
    #8 0x7fecefa3cf6  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c43cf6)
    #9 0x7fecefa4b1a  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183c44b1a)
    #10 0x7feced703a8  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183a103a8)
    #11 0x7fecfd764b0  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x184a164b0)
    #12 0x7fecfd7440d  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x184a1440d)
    #13 0x7fecc4ddcef  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18117dcef)
    #14 0x7fecc4dc95f  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18117c95f)
    #15 0x7fecc4d12a8  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1811712a8)
    #16 0x7fecc4aedd1  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18114edd1)
    #17 0x7fecc480790  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x181120790)
    #18 0x7fecee290dd  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183ac90dd)
    #19 0x7fecee2875c  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183ac875c)
    #20 0x7fecee25520  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183ac5520)
    #21 0x7feced6a054  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183a0a054)
    #22 0x7feccc596f3  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818f96f3)
    #23 0x7fecee10f54  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183ab0f54)
    #24 0x7feced2274f  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1839c274f)
    #25 0x13f861f18  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140031f18)
    #26 0x76d7f56c  (C:\Windows\system32\kernel32.dll+0x78d3f56c)
    #27 0x76fb3280  (C:\Windows\SYSTEM32\ntdll.dll+0x78e83280)

Thread T3 created by T0 here:
    #0 0x13f860e40  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140030e40)
    #1 0x7feced21cab  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1839c1cab)
    #2 0x7fecee1019b  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183ab019b)
    #3 0x7feccc3294f  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818d294f)
    #4 0x7feccc30960  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818d0960)
    #5 0x7feccc415ec  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818e15ec)
    #6 0x7feccc2d554  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1818cd554)
    #7 0x7fece87a415  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18351a415)
    #8 0x7fece87b5a6  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18351b5a6)
    #9 0x7fece8e7b68  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x183587b68)
    #10 0x7fece87a06a  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18351a06a)
    #11 0x7fecb3613e7  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x1800013e7)
    #12 0x13f837ccc  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140007ccc)
    #13 0x13f832349  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140002349)
    #14 0x13fb76d28  (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.exe+0x140346d28)
    #15 0x76d7f56c  (C:\Windows\system32\kernel32.dll+0x78d3f56c)
    #16 0x76fb3280  (C:\Windows\SYSTEM32\ntdll.dll+0x78e83280)

SUMMARY: AddressSanitizer: heap-use-after-free (C:\Users\admin\Desktop\asan-win32-release_x64-548420\chrome.dll+0x18640cbd5)

Shadow bytes around the buggy address:
  0x0025a8a35190: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
  0x0025a8a351a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0025a8a351b0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa
  0x0025a8a351c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0025a8a351d0: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
=>0x0025a8a351e0: fa fa fa fa fa fa fa fa fd fd fd fd[fd]fd fd fd
  0x0025a8a351f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0025a8a35200: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa
  0x0025a8a35210: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x0025a8a35220: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa
  0x0025a8a35230: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd
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
==3444==ABORTING
 

### ji...@chromium.org (2018-04-05)

Find a corresponding crash report: https://crash.corp.google.com/browse?q=stable_signature%3D%27content%3A%3ASpeechRecognitionDispatcher%3A%3AOnRecognitionEnded-6fe7bd11%27&stbtiq=&reportid=&index=0



[Monorail components: Blink>Speech]

### cl...@chromium.org (2018-04-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4824276558151680.

### ch...@gmail.com (2018-04-05)

Minimized Testcase:

var recognition = new webkitSpeechRecognition();
  recognition.onend = function(){document.location='https://yahoo.com';recognition.start()}		
  recognition.start();

### sh...@chromium.org (2018-04-06)

Users experienced this crash on the following builds:

Mac Canary 67.0.3389.0 -  0.92 CPM, 2 reports, 1 clients (signature content::SpeechRecognitionDispatcher::OnRecognitionEnded)

If this update was incorrect, please add "Fracas-Wrong" label to prevent future updates.

- Go/Fracas

### sh...@chromium.org (2018-04-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ji...@chromium.org (2018-04-06)

tommi@, could you take a look at this crash? Thanks!
Please feel free to lower the priority/severity if you see fit. 

### to...@chromium.org (2018-04-06)

guido - can you help?

### gu...@chromium.org (2018-04-10)

[Empty comment from Monorail migration]

### av...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### av...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### av...@chromium.org (2018-04-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/748bc4a04fa53912389c6d3d566ef1c95bc8bb75

commit 748bc4a04fa53912389c6d3d566ef1c95bc8bb75
Author: Guido Urdaneta <guidou@chromium.org>
Date: Thu Apr 12 07:43:13 2018

Make blink::SpeechRecognitionClient/Proxy garbage collected.

Also change WebSpeechRecognizerClient to wrap a WebPrivatePtr to
SpeechRecognitionClientProxy instead of being an interface.

Before this CL, content::SpeechRecognitionDispatcher kept a raw
pointer to WebSpeechRecognitionClient to communicate with
SpeechRecognitionClientProxy. This pointer can become dangling
while SpeechRecognitionDispatcher is still alive due to Blink
garbage collection.

After this CL, WebSpeechRecognitionClient keeps the
SpeechRecognitionClientProxy object in Blink alive while
SpeechRecognitionDispatcher is still alive in content.

Drive-by: Minor lint fixes in MockWebSpeechRecognizer.

Bug: 829213
Change-Id: I520e96e3e9b9b56908c1ab02e02e49f82d4d2bf9
Reviewed-on: https://chromium-review.googlesource.com/1005063
Reviewed-by: Kentaro Hara <haraken@chromium.org>
Reviewed-by: Dominic Mazzoni <dmazzoni@chromium.org>
Reviewed-by: Tommi <tommi@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/master@{#550084}
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/content/renderer/speech_recognition_dispatcher.cc
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/content/renderer/speech_recognition_dispatcher.h
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/content/shell/test_runner/mock_web_speech_recognizer.cc
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/content/shell/test_runner/mock_web_speech_recognizer.h
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/third_party/blink/public/web/web_speech_recognizer.h
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/third_party/blink/public/web/web_speech_recognizer_client.h
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/third_party/blink/renderer/modules/exported/BUILD.gn
[add] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/third_party/blink/renderer/modules/exported/web_speech_recognizer_client.cc
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/third_party/blink/renderer/modules/speech/speech_recognition_client.h
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/third_party/blink/renderer/modules/speech/speech_recognition_client_proxy.cc
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/third_party/blink/renderer/modules/speech/speech_recognition_client_proxy.h
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/third_party/blink/renderer/modules/speech/speech_recognition_controller.cc
[modify] https://crrev.com/748bc4a04fa53912389c6d3d566ef1c95bc8bb75/third_party/blink/renderer/modules/speech/speech_recognition_controller.h


### gu...@chromium.org (2018-04-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-20)

Nice one khalil, $3,000 for this report - thanks!

### aw...@chromium.org (2018-04-20)

[Empty comment from Monorail migration]

### ch...@gmail.com (2018-04-20)

Nice reward! Thanks as ever!

### aw...@google.com (2018-04-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-07-19)

This issue was migrated from crbug.com/chromium/829213?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/820607, crbug.com/chromium/828629, crbug.com/chromium/828634]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091012)*
