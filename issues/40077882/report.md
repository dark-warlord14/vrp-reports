# Security: use-after-free Speech with changing of the page

| Field | Value |
|-------|-------|
| **Issue ID** | [40077882](https://issues.chromium.org/issues/40077882) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Speech, UI>Browser>Navigation |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-08-05 |
| **Bounty** | $500.00 |

## Description

This is a new security bug and I guess it's looks like use-after-free, actually it's not easy to repro anyway 
I've made a video  http://youtu.be/rSWYLLJZnfU to see how I repro it.

Before trying to repro the crash you do setting on Microsoft settings => No audio devices are installed, like on the 1.PNG .

Repro on : Chrome 29.0.1547.41 Beta.
 
Steps : 

1. Open a new tab.

2. Then open on it repro.html.

3. Click on the page then keep clicking faster as possible on " Try Again " of Speech until the page will 
change back to that new tab with history methode.


Stack Dump :

ChildEBP RetAddr  
03a3f1b4 5420f490 chrome_52a80000!content::SpeechRecognitionManagerImpl::OnRecognitionError+0x46 [c:\b\build\slave\win\build\src\content\browser\speech\speech_recognition_manager_impl.cc @ 388]
03a3f2b0 5420e7e8 chrome_52a80000!content::SpeechRecognitionManagerImpl::RecognitionAllowedCallback+0x191 [c:\b\build\slave\win\build\src\content\browser\speech\speech_recognition_manager_impl.cc @ 217]
03a3f2c8 5420e81f chrome_52a80000!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall content::SpeechRecognitionManagerImpl::*)(int,bool,bool)>,void __cdecl(base::WeakPtr<content::SpeechRecognitionManagerImpl> const &,int const &,bool const &,bool const &)>::MakeItSo+0x4a [c:\b\build\slave\win\build\src\base\bind_internal.h @ 971]
03a3f2e8 53b587b2 chrome_52a80000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::SpeechRecognitionManagerImpl::*)(int,bool,bool)>,void __cdecl(content::SpeechRecognitionManagerImpl *,int,bool,bool),void __cdecl(base::WeakPtr<content::SpeechRecognitionManagerImpl>,int)>,void __cdecl(content::SpeechRecognitionManagerImpl *,int,bool,bool)>::Run+0x1f [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1491]
03a3f2fc 53a65b01 chrome_52a80000!base::internal::InvokeHelper<0,void,base::Callback<void __cdecl(int,history::QueryResults *)>,void __cdecl(int const &,history::QueryResults * const &)>::MakeItSo+0xf [c:\b\build\slave\win\build\src\base\bind_internal.h @ 898]
03a3f314 52aaa881 chrome_52a80000!base::internal::Invoker<2,base::internal::BindState<base::Callback<void __cdecl(bool,bool)>,void __cdecl(bool,bool),void __cdecl(bool,bool)>,void __cdecl(bool,bool)>::Run+0x20 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1253]
03a3f3a8 52aaa491 chrome_52a80000!base::MessageLoop::RunTask+0x34e [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 486]
03a3f4f8 52aac153 chrome_52a80000!base::MessageLoop::DoWork+0x2ec [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 689]
03a3f56c 52aac061 chrome_52a80000!base::MessagePumpForIO::DoRunLoop+0xe7 [c:\b\build\slave\win\build\src\base\message_loop\message_pump_win.cc @ 529]
03a3f58c 52aaa0f1 chrome_52a80000!base::MessagePumpWin::Run+0x3e [c:\b\build\slave\win\build\src\base\message_loop\message_pump_win.h @ 48]
03a3f5b0 52aaa049 chrome_52a80000!base::MessageLoop::RunInternal+0x72 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 442]
03a3f5c0 52aac011 chrome_52a80000!base::RunLoop::Run+0x59 [c:\b\build\slave\win\build\src\base\run_loop.cc @ 46]
03a3f5e8 52d5662a chrome_52a80000!base::Thread::Run+0x34 [c:\b\build\slave\win\build\src\base\threading\thread.cc @ 158]
03a3f6b8 52d4eea6 chrome_52a80000!content::BrowserThreadImpl::IOThreadRun+0x2b [c:\b\build\slave\win\build\src\content\browser\browser_thread_impl.cc @ 165]
03a3f6cc 52aabed2 chrome_52a80000!content::BrowserThreadImpl::Run+0x86 [c:\b\build\slave\win\build\src\content\browser\browser_thread_impl.cc @ 192]
03a3f7f8 52aabc90 chrome_52a80000!base::Thread::ThreadMain+0xdc [c:\b\build\slave\win\build\src\base\threading\thread.cc @ 207]
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\Windows\system32\kernel32.dll - 
03a3f80c 7705ed6c chrome_52a80000!base::`anonymous namespace'::ThreadFunc+0x58 [c:\b\build\slave\win\build\src\base\threading\platform_thread_win.cc @ 78]
WARNING: Stack unwind information not available. Following frames may be wrong.
03a3f818 76f337f5 kernel32!BaseThreadInitThunk+0x12
03a3f858 76f337c8 ntdll!RtlInitializeExceptionChain+0xef
03a3f870 00000000 ntdll!RtlInitializeExceptionChain+0xc2

Regard,
Khalil Zhani

## Attachments

- [repro.html](attachments/repro.html) (text/html; charset=us-ascii, 596 B)
- [1.png](attachments/1.png) (image/png; charset=binary, 20.7 KB)
- [Chrome-last.dmp](attachments/Chrome-last.dmp) (application/octet-stream; charset=binary, 674.0 KB)

## Timeline

### cl...@chromium.org (2013-08-05)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=6424133848006656

### jl...@chromium.org (2013-08-05)

Is there any chance that you could repro this with crash reports enabled and give use the crash ID from chrome://crashes ?

### ch...@gmail.com (2013-08-06)

[Comment Deleted]

### jl...@chromium.org (2013-08-06)

Thanks! ... but that crash ID doesn't seem to exist.

Do you mind trying again ? Does it show-up in chrome://crashes ?

### ch...@gmail.com (2013-08-06)

Sorry that was the wrong Crash ID.
Actually it doesn't show-up in chrome://crashes

### wf...@chromium.org (2013-08-06)

can you confirm that 'Automatically send usage statistics and crash reports to Google' is enabled, and then try repro again, and attach the crash number here?

### ch...@gmail.com (2013-08-06)

Well, I got it on Ubuntu : 73998fa293d034b7

### wf...@chromium.org (2013-08-08)

stacks from the crash report aren't too clear, so I'll try and repro this locally.

### ch...@gmail.com (2013-08-08)

Yep, is better if you try to repro on Beta version.

### ch...@gmail.com (2013-08-08)

First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=077ab524 ebx=00000000 ecx=077ab524 edx=56a1dcb4 esi=007b1100 edi=00000004
eip=00006363 esp=040ef51c ebp=040ef534 iopl=0         nv up ei pl nz na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010206
00006363 ??              ???
0:018> k
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
040ef518 5620ebfa 0x6363
040ef534 5620f490 chrome_54a80000!content::SpeechRecognitionManagerImpl::OnRecognitionError+0x49 [c:\b\build\slave\win\build\src\content\browser\speech\speech_recognition_manager_impl.cc @ 388]
040ef630 5620e7e8 chrome_54a80000!content::SpeechRecognitionManagerImpl::RecognitionAllowedCallback+0x191 [c:\b\build\slave\win\build\src\content\browser\speech\speech_recognition_manager_impl.cc @ 217]
040ef648 5620e81f chrome_54a80000!base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (__thiscall content::SpeechRecognitionManagerImpl::*)(int,bool,bool)>,void __cdecl(base::WeakPtr<content::SpeechRecognitionManagerImpl> const &,int const &,bool const &,bool const &)>::MakeItSo+0x4a [c:\b\build\slave\win\build\src\base\bind_internal.h @ 971]
040ef668 55b587b2 chrome_54a80000!base::internal::Invoker<2,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall content::SpeechRecognitionManagerImpl::*)(int,bool,bool)>,void __cdecl(content::SpeechRecognitionManagerImpl *,int,bool,bool),void __cdecl(base::WeakPtr<content::SpeechRecognitionManagerImpl>,int)>,void __cdecl(content::SpeechRecognitionManagerImpl *,int,bool,bool)>::Run+0x1f [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1491]
040ef67c 55a65b01 chrome_54a80000!base::internal::InvokeHelper<0,void,base::Callback<void __cdecl(int,history::QueryResults *)>,void __cdecl(int const &,history::QueryResults * const &)>::MakeItSo+0xf [c:\b\build\slave\win\build\src\base\bind_internal.h @ 898]
040ef694 54aaa881 chrome_54a80000!base::internal::Invoker<2,base::internal::BindState<base::Callback<void __cdecl(bool,bool)>,void __cdecl(bool,bool),void __cdecl(bool,bool)>,void __cdecl(bool,bool)>::Run+0x20 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 1253]
040ef728 54aaa491 chrome_54a80000!base::MessageLoop::RunTask+0x34e [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 486]
040ef878 54aac153 chrome_54a80000!base::MessageLoop::DoWork+0x2ec [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 689]
040ef8c4 54aac061 chrome_54a80000!base::MessagePumpForIO::DoRunLoop+0xe7 [c:\b\build\slave\win\build\src\base\message_loop\message_pump_win.cc @ 529]
040ef8e4 54aaa0f1 chrome_54a80000!base::MessagePumpWin::Run+0x3e [c:\b\build\slave\win\build\src\base\message_loop\message_pump_win.h @ 48]
040ef908 54aaa049 chrome_54a80000!base::MessageLoop::RunInternal+0x72 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 442]
040ef918 54aac011 chrome_54a80000!base::RunLoop::Run+0x59 [c:\b\build\slave\win\build\src\base\run_loop.cc @ 46]
040ef940 54d5662a chrome_54a80000!base::Thread::Run+0x34 [c:\b\build\slave\win\build\src\base\threading\thread.cc @ 158]
040efa10 54d4eea6 chrome_54a80000!content::BrowserThreadImpl::IOThreadRun+0x2b [c:\b\build\slave\win\build\src\content\browser\browser_thread_impl.cc @ 165]
040efa24 54aabed2 chrome_54a80000!content::BrowserThreadImpl::Run+0x86 [c:\b\build\slave\win\build\src\content\browser\browser_thread_impl.cc @ 192]
040efb50 54aabc90 chrome_54a80000!base::Thread::ThreadMain+0xdc [c:\b\build\slave\win\build\src\base\threading\thread.cc @ 207]
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for C:\Windows\system32\kernel32.dll - 
040efb64 7699ed6c chrome_54a80000!base::`anonymous namespace'::ThreadFunc+0x58 [c:\b\build\slave\win\build\src\base\threading\platform_thread_win.cc @ 78]
040efb70 771037f5 kernel32!BaseThreadInitThunk+0x12
040efbb0 771037c8 ntdll!RtlInitializeExceptionChain+0xef


### ch...@gmail.com (2013-08-12)

http://go/crash/reportdetail?reportid=cf8efad89f475b23
http://go/crash/reportdetail?reportid=a698e3c22dc52016

### wf...@chromium.org (2013-08-12)

I spent a while trying to repro this on latest trunk, and also beta 29.0.1547.41 - but couldn't.  I'll try again on Windows - do you have any hints on the repro - should I be hitting the 'retry' button, or letting the dialog stay up when the timeout hits history(-1)?

### ch...@gmail.com (2013-08-12)

[Comment Deleted]

### ch...@gmail.com (2013-08-12)

Actually I know is not easily to repro it especially on Linux, anyway as I said you should disable the Microphone for making 'retry' button available always.

You should keep hitting the 'retry' button faster as you can, until the timeout hits history(-1) which makes return to the previous page.

### wf...@chromium.org (2013-08-12)

okay I'll give it another go when I have physical access to a Windows machine.  Can you repro on latest trunk, or best for me to stick to 29.0.1547.41

### wf...@chromium.org (2013-08-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2013-08-12)

[Comment Deleted]

### ch...@gmail.com (2013-08-12)

Ok I've made another video http://youtu.be/QZXpPo64UoE to how to repro this bug on 29.0.1547.49 beta-m, and can you see in the first I couldn't to repro but after I crashed the browser.

### ch...@gmail.com (2013-08-31)

[Comment Deleted]

### ch...@gmail.com (2013-08-31)

[Comment Deleted]

### ch...@gmail.com (2013-09-03)

[Comment Deleted]

### ch...@gmail.com (2013-09-06)

[Comment Deleted]

### in...@chromium.org (2013-09-06)

There is some user interaction required, but there could be ways to make it more reliable. Bumping up severity as it is also in the browser process.

### [Deleted User] (2013-09-06)


I am busy with a few M31 features and likely won't have time for other issues. Assign the bug to Tommi for further dispatching, and CC me.

### to...@chromium.org (2013-09-06)

I think Tommy might already have landed an experimental fix for this.

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### in...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-27)

tommyw@: you haven't provided any bug update or come up with a fix for this issue in the last 7 days. Please note that this is a medium+ severity security vulnerability that needs your immediate response. If you have a patch in progress and don't want future nags, please add a codereview link and a WIP label. If the issue is already fixed or you can't reproduce it, please close the bug.

### [Deleted User] (2013-09-30)

chromium.khalil: could you please check if the issue is fixed on canary, please?

### ch...@gmail.com (2013-09-30)

 tommyw@, it's Fixed on Canary.

### in...@chromium.org (2013-09-30)

tommyw@, what is link to the experimental fix you landed (which did actually fix the problem for chromium.khalil@) ?

### cl...@chromium.org (2013-10-01)

Adding Merge-Requested label.

Please do not merge your fix without first checking with the release manager. 

Once the merge is approved by the release manager, make sure to merge the fix to all the affected branches, i.e stable, beta and trunk (near branch point). You can find branch information on omahaproxy.appspot.com.

If the fix does not merge cleanly or is too risky on uptake on these branches, please change the M-* label to indicate the next milestone.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2013-10-01)

inferno@: <https://src.chromium.org/viewvc/chrome?view=rev&revision=220936> is the fix for the issue I could trigger on linux which very happily seems to have fixed the issue on Windows as well. Same as for bug #262606.

### in...@chromium.org (2013-10-01)

if this fix fixed 262606, then we should dupe that bug against this one.

### cl...@chromium.org (2013-10-02)

Migrating old milestone labels.

### in...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

[Comment Deleted]

### cl...@chromium.org (2013-10-11)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone labels first. Make sure to re-request merge for every milestone in the Merge-To-M-* label. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2013-10-18)

[Empty comment from Monorail migration]

### la...@google.com (2013-10-18)

The patch in question is already in M31 (cut at r224845), which should include r220936.

### in...@chromium.org (2013-10-21)

No more m30s.

### mb...@chromium.org (2013-10-22)

Thanks for the report! This one qualifies for a $500 reward. It did not qualify for a higher reward because of the level of user interaction required to reproduce the issue.

### mb...@chromium.org (2013-11-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-11-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-14)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-02-06)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/268565?no_tracker_redirect=1

[Multiple monorail components: Blink>Speech, UI>Browser>Navigation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077882)*
