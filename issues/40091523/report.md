# Flash/GPU memory corruption in critical section.

| Field | Value |
|-------|-------|
| **Issue ID** | [40091523](https://issues.chromium.org/issues/40091523) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Internals, Internals>GPU, Internals>Plugins>Flash |
| **Reporter** | ku...@gmail.com |
| **Assignee** | zm...@chromium.org |
| **Created** | 2011-06-03 |
| **Bounty** | $500.00 |

## Description

Test chrome 13.0.782.1 windows 7 sp1

Install testcase.crx

(950.768): Access violation - code c0000005 (!!! second chance !!!)
eax=054edf80 ebx=00000000 ecx=055b9f08 edx=0065ac40 esi=06ddf9f0 edi=0037ef38
eip=0065ac40 esp=0037ee5c ebp=005d5140 iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210206
0065ac40 80726600        xor     byte ptr [edx+66h],0       ds:002b:0065aca6=65
0:000> .exr -1
ExceptionAddress: 0065ac40
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 0065ac40
Attempt to execute non-executable address 0065ac40

(98c.594): Access violation - code c0000005 (!!! second chance !!!)
eax=795475f9 ebx=00000000 ecx=795475f5 edx=02630c80 esi=795475f9 edi=795475f5
eip=772622c2 esp=002befa0 ebp=002befb4 iopl=0         nv up ei pl nz ac po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010212
ntdll!RtlEnterCriticalSection+0x12:
772622c2 f00fba3000      lock btr dword ptr [eax],0   ds:002b:795475f9=????????
0:000> .exr -1
ExceptionAddress: 772622c2 (ntdll!RtlEnterCriticalSection+0x00000012)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 795475f9
Attempt to write to address 795475f9

(bc.524): Access violation - code c0000005 (!!! second chance !!!)
eax=00000010 ebx=00000000 ecx=0602db28 edx=05fa4750 esi=05fa4750 edi=0018f5cc
eip=6dd0e381 esp=0018f450 ebp=005b5140 iopl=0         nv up ei pl nz na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
chrome_6cce0000!CrashUploadList::InformDelegateOfCompletion+0x71:
6dd0e381 8b10            mov     edx,dword ptr [eax]  ds:002b:00000010=????????
0:000> .exr -1
ExceptionAddress: 6dd0e381 (chrome_6cce0000!CrashUploadList::InformDelegateOfCompletion+0x00000071)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 00000010
Attempt to read from address 00000010

## Attachments

- [log.txt](attachments/log.txt) (text/x-c++; charset=us-ascii, 3.6 KB)
- [log3.txt](attachments/log3.txt) (text/x-c++; charset=unknown-8bit, 4.3 KB)
- [testcase.crx](attachments/testcase.crx) (application/octet-stream; charset=binary, 739 B)
- [log2.txt](attachments/log2.txt) (text/x-c++; charset=us-ascii, 3.8 KB)

## Timeline

### sk...@chromium.org (2011-06-03)

A critical section object contains a stale or otherwise invalid pointer, which is accessed. This happens in the BROWSER process and judging from the stack is a problem in the Flash or GPU code.

id:             ntdll32.dll!RtlEnterCriticalSection WriteAV@Arbitrary (91d9250bdedd4a6349101c9563c73c9b)
description:    Security: Attempt to write to unallocated arbitrary memory (@0x7272670A) in ntdll32.dll!RtlEnterCriticalSection
note:           The exception happens in the main process. Based on this information, this is expected to be a critical security issue!
application:    Chromium 14.0.784.0
stack:          ntdll32.dll!RtlEnterCriticalSection
                chrome.dll!base::internal::LockImpl::Lock
                chrome.dll!GpuDataManager::gpu_info
                chrome.dll!`anonymous namespace'::FlashDOMHandler::MaybeRespondToPage
                chrome.dll!CallbackImpl<webkit_glue::BufferedDataSource,void
                chrome.dll!GpuDataManager::RunGpuInfoUpdateCallbacks
                chrome.dll!`anonymous namespace'::TaskClosureAdapter::Run
                chrome.dll!MessageLoop::RunTask
                chrome.dll!MessageLoop::DoWork
                chrome.dll!base::MessagePumpForUI::DoRunLoop
                chrome.dll!base::MessagePumpWin::RunWithDispatcher
                chrome.dll!MessageLoop::RunInternal
                chrome.dll!MessageLoopForUI::Run
                chrome.dll!`anonymous namespace'::RunUIMessageLoop
                chrome.dll!BrowserMain
                chrome.dll!`anonymous namespace'::RunNamedProcessTypeMain
                chrome.dll!ChromeMain
                chrome.exe!MainDllLoader::Launch
                chrome.exe!wWinMain
                chrome.exe!__tmainCRTStartup
                kernel32.dll!BaseThreadInitThunk
                ntdll32.dll!__RtlUserThreadStart
                ntdll32.dll!_RtlUserThreadStart

### sk...@chromium.org (2011-06-03)

The call to EnterCriticalSection is in base\synchronization\lock_impl_win.cc:
void LockImpl::Lock() {
  ::EnterCriticalSection(&os_lock_);
}
At the time of the crash, "this" was:
Local var @ 0x2bd320 Type base::internal::LockImpl*
0x66c59e99 
   +0x000 os_lock_         : _RTL_CRITICAL_SECTION
      +0x000 DebugInfo        : 0x0f94a2e9 _RTL_CRITICAL_SECTION_DEBUG
         +0x000 Type             : ??
         +0x002 CreatorBackTraceIndex : ??
         +0x004 CriticalSection  : ???? 
         +0x008 ProcessLocksList : _LIST_ENTRY
         +0x010 EntryCount       : ??
         +0x014 ContentionCount  : ??
         +0x018 Flags            : ??
         +0x01c CreatorBackTraceIndexHigh : ??
         +0x01e SpareWORD        : ??
      +0x004 LockCount        : 0n910027008
      +0x008 RecursionCount   : 0n417923078
      +0x00c OwningThread     : 0xe90000c7 Void
      +0x010 LockSemaphore    : 0x000765a3 Void
      +0x014 SpinCount        : 0xe8f0ee9
Memory read error 000000000f94a307


ntdll32!RtlEnterCriticalSection:
772c22b0 8bff            mov     edi,edi
772c22b2 55              push    ebp
772c22b3 8bec            mov     ebp,esp
772c22b5 83ec0c          sub     esp,0Ch
772c22b8 56              push    esi
772c22b9 57              push    edi
772c22ba 8b7d08          mov     edi,dword ptr [ebp+8]      <-- "os_lock_"
772c22bd 8d7704          lea     esi,[edi+4]                <-- "os_lock_.LockCount"
772c22c0 8bc6            mov     eax,esi
772c22c2 f00fba3000      lock btr dword ptr [eax],0   ds:002b:66c59e9d=363de900 <-- Crash
772c22c7 0f836e020100    jae     ntdll32!RtlEnterCriticalSection+0x1d (772d253b)
772c22cd 64a118000000    mov     eax,dword ptr fs:[00000018h]
772c22d3 8b4824          mov     ecx,dword ptr [eax+24h]
772c22d6 894f0c          mov     dword ptr [edi+0Ch],ecx
772c22d9 c7470801000000  mov     dword ptr [edi+8],1
772c22e0 5f              pop     edi
772c22e1 33c0            xor     eax,eax
772c22e3 5e              pop     esi
772c22e4 8be5            mov     esp,ebp
772c22e6 5d              pop     ebp
772c22e7 c20400          ret     4

### [Deleted User] (2011-06-03)

Maybe the result of recent changes in the gpu data manager?  Mo, can you please have a look?


### zm...@chromium.org (2011-06-03)

Looks like it's related to Flash using GpuDataManager.  I'll have a look.  In the meantime, cc'ed Finnur on it in case he has some insights.

### fi...@chromium.org (2011-06-03)

Love to help, but cpu is probably a better candidate for Flash issues (unless I'm mistaken)...

### zm...@chromium.org (2011-06-03)

It's due to a lock re-entry.  I'll get a fix up for review shortly after.

### bu...@chromium.org (2011-06-04)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=87898

------------------------------------------------------------------------
r87898 | zmo@google.com | Fri Jun 03 17:14:25 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/gpu/gpu_data_manager.cc?r1=87898&r2=87897&pathrev=87898

Fix a lock re-entry bug in GpuDataManager::UpdateGpuInfo.

The issue is that the registered callbacks could request GPUInfo, so they could re-enter the lock.  Therefore, we should release the lock before we run through callbacks.

BUG=84805
TEST=the issue in 84805 is gone.
Review URL: http://codereview.chromium.org/7054063
------------------------------------------------------------------------

### in...@chromium.org (2011-06-06)

[Empty comment from Monorail migration]

### zm...@chromium.org (2011-06-06)

Will the security team merge this back to M12 and M13 or I do it?

### la...@chromium.org (2011-06-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-06-06)

We will do it for m12 first patch and m13. Thanks for the patch.

### sc...@gmail.com (2011-06-14)

Non-trivial merge to M12, and we typically rate bad extension -> browser corruption as "Medium", so happy to just get in into M13.

### sc...@gmail.com (2011-06-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-06-14)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=88956

------------------------------------------------------------------------
r88956 | cevans@chromium.org | Mon Jun 13 21:27:27 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/782/src/content/browser/gpu/gpu_data_manager.cc?r1=88956&r2=88955&pathrev=88956

Merge 87898 - Fix a lock re-entry bug in GpuDataManager::UpdateGpuInfo.

The issue is that the registered callbacks could request GPUInfo, so they could re-enter the lock.  Therefore, we should release the lock before we run through callbacks.

BUG=84805
TEST=the issue in 84805 is gone.
Review URL: http://codereview.chromium.org/7054063

TBR=zmo@google.com
Review URL: http://codereview.chromium.org/7145020
------------------------------------------------------------------------

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### ku...@gmail.com (2011-11-16)

Still work on chrome 17.0.938.0 dev-m

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

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

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### aj...@chromium.org (2014-06-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Old bug is old. Found this in a cleanup looking for old unrewarded reports. 

If you're still there, we'd like to pay $500 for this report. We'll get in touch seeking payment details within two weeks.

### ti...@google.com (2015-03-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### ss...@google.com (2017-02-07)

Moving old issues out of Internal>Graphics to delete this obsolete component (crbug.com/685425 for details)

[Monorail components: -Internals>Graphics]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/84805?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>GPU, Internals>Plugins>Flash]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091523)*
