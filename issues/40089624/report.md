# Memory corruption leading to OOB read symptom in PDF initialization

| Field | Value |
|-------|-------|
| **Issue ID** | [40089624](https://issues.chromium.org/issues/40089624) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Internals, Internals>Plugins>PDF |
| **Reporter** | [Deleted User] |
| **Assignee** | [Deleted User] |
| **Created** | 2011-04-06 |
| **Bounty** | $1,000.00 |

## Description

**This template is ONLY for reporting security bugs. Please use a different**  

**template for other types of bug reports.**

**Please see the following link for instructions on filing security bugs:**  

**<http://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**VULNERABILITY DETAILS**  

hello,

I found a memory corruption bug  

google chrome in vesao10.0.648.204,  

The bug occurred when a chrome handles  

HTML file with many iframes  

PDF files

**VERSION**  

Chrome Version: 10.0.648.204 + stable  

Operating System: windows

**REPRODUCTION CASE**  

open the anex file or enter in this website  

<http://cassiosouza.110mb.com/exploit.html>  

wait the chrome show the message "Oh,no"

Type of crash: OPENNING .PDF FILES  

Crash State:

this is the stacktrack from CHROME

(ed4.f48): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

eax=12351000 ebx=0000efee ecx=1234dfa0 edx=31c606c8 esi=00000000 edi=1234f000  

eip=101c7898 esp=0012f2f0 ebp=0012f314 iopl=0 nv up ei pl nz na pe nc  

cs=001b ss=0023 ds=0023 es=0023 fs=003b gs=0000 efl=00010206  

\*\*\* ERROR: Symbol file could not be found. Defaulted to export symbols for D:\Documents and Settings\Cassio\Configurações locais\Dados de aplicativos\Google\Chrome\Application\10.0.648.204\pdf.dll -  

pdf!PPP\_GetInterface+0x17cba9:  

101c7898 8b08 mov ecx,dword ptr [eax] ds:0023:12351000=????????

**Client ID (if relevant): [see link above]**

## Attachments

- deleted (application/octet-stream, 0 B)
- [CRASH.DMP](attachments/CRASH.DMP) (application/octet-stream; charset=binary, 22.4 KB)
- [fw4.pdf](attachments/fw4.pdf) (application/pdf; charset=binary, 99.9 KB)
- [repro.html](attachments/repro.html) (text/html; charset=us-ascii, 1.7 KB)
- [Crash_Details.txt](attachments/Crash_Details.txt) (text/plain; charset=us-ascii, 4.4 KB)

## Timeline

### [Deleted User] (2011-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2011-04-06)

Thanks for the report. 

Google Chrome 11.0.696.34 (Official Build 80286) - NOT OK
Google Chrome 12.0.727.0 (Official Build 80463) - OK

Full report @ http://crash/reportdetail?reportid=0b75639f2946ea4f



### sc...@gmail.com (2011-04-06)

I can't get this to fire on Linux 64-bit on a M11 debug or opt build.

John, any ideas? Does the stack trace look familiar?

### [Deleted User] (2011-04-06)

FYI: I tried on Win7 x64. Haven't tried on Linux. Might be affecting only windows!

### [Deleted User] (2011-04-06)

[Comment Deleted]

### [Deleted User] (2011-04-06)

[Comment Deleted]

### sc...@gmail.com (2011-04-06)

@mariosoufa: we would prefer you don't publish until we can understand the issue, and make sure it is fixed in the Stable version of Chrome.
It isn't critical, because the PDF and HTML renderers run inside the sandbox. It could however be of "high" severity, which is one notch down from critical.

### [Deleted User] (2011-04-06)

[Comment Deleted]

### sc...@gmail.com (2011-04-06)

@mariosoufa: you might be awarded money, but it relies upon getting to the root cause of the bug. I can't yet reproduce this on Linux. One of my colleagues will try Windows.

### [Deleted User] (2011-04-06)

[Comment Deleted]

### [Deleted User] (2011-04-06)

[Comment Deleted]

### [Deleted User] (2011-04-06)

[Comment Deleted]

### [Deleted User] (2011-04-07)

[Comment Deleted]

### [Deleted User] (2011-04-07)

[Comment Deleted]

### [Deleted User] (2011-04-10)

[Comment Deleted]

### [Deleted User] (2011-04-10)

[Comment Deleted]

### [Deleted User] (2011-04-12)

[Comment Deleted]

### sc...@gmail.com (2011-04-15)

Justin repro'ed it on Windows, I'm still SOL on Linux.
https://crash/reportdetail?reportid=e9dd9fafc6b1d424

### [Deleted User] (2011-04-16)

[Comment Deleted]

### [Deleted User] (2011-04-16)

CRASH DUMP FROM THE BUG.

### sc...@gmail.com (2011-04-17)

I gave up trying to repro it on Linux after lots of trying :)
I've had to pass it on to someone to who develops PDF on Windows.

### [Deleted User] (2011-04-17)

[Comment Deleted]

### sc...@gmail.com (2011-04-19)

@jam can't reproduce it on Windows trunk.

@jschuh: were you able to reproduce it on trunk or an M12 dev channel build?

### js...@chromium.org (2011-04-19)

I repro'd it on stable, but I had to use a release build.

### ja...@chromium.org (2011-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2011-04-22)

[Comment Deleted]

### sc...@gmail.com (2011-04-22)

It's a WILLFIX but it's a headache to reproduce in a debug build!!

### [Deleted User] (2011-04-23)

[Comment Deleted]

### sc...@gmail.com (2011-04-23)

I need to get a Windows desktop.

### [Deleted User] (2011-04-23)

[Comment Deleted]

### sk...@chromium.org (2011-04-27)

I can repro in an old local build, so I have symbols and source. At this point it looks like use-after-free caused by missing or bad reference counting on the plugin object. 
I find it's hard to trigger and the repro can run for a bit without crashing (I added a a page reload to make sure it eventually does crash). The one crash I've analyzed looks exploitable. I'm trying to find the root cause (or help point Chris in the right direction).

### sk...@chromium.org (2011-04-28)

I think I know what is going on: PPB_Scrollbar_Impl keeps a reference to the PluginInstance without a reference count. Depending on timing, the later can get destroyed while the former continues to use it. The timing may be difficult to get right; the only crash I've seen is when the PPB_Scrollbar_Impl schedules a task while the PluginInstance still exists, and this task must get executed after the PluginInstance has been deleted and its memory reused or freed. It takes a while for this series of events to happen in that order.

At this point, I don't see any reason why linux or mac would not be affected - it may just be really hard to get the timing right.

### sk...@chromium.org (2011-04-28)

It seems the problem is that the "Resource" class (\webkit\plugins\ppapi\resource.cc) keeps a reference to a PluginInstance in the "instance_" property, but it doesn't use AddRef()/Release() to make sure the PluginInstance does not get deleted. So, the PluginInstance can get deleted after which the "instance_" property may still be used, which will access the now freed memory.

I have a patch which seems to fix the crash for me (below). I'm not sure if this is the right approach - please advise.

Index: webkit/plugins/ppapi/resource.cc
===================================================================
--- webkit/plugins/ppapi/resource.cc    (revision 81926)
+++ webkit/plugins/ppapi/resource.cc    (working copy)
@@ -15,9 +15,12 @@

 Resource::Resource(PluginInstance* instance)
     : resource_id_(0), instance_(instance) {
+    instance_->AddRef();
 }

 Resource::~Resource() {
+    if (instance_)
+      instance_->Release();
 }

 PP_Resource Resource::GetReference() {
@@ -39,8 +42,10 @@
       resource_id_);
   resource_id_ = 0;

-  if (instance_destroyed)
+  if (instance_destroyed) {
+    instance_->Release();
     instance_ = NULL;
+  }
 }

 #define DEFINE_TYPE_GETTER(RESOURCE)            \


### sk...@chromium.org (2011-04-28)

@brettw: you show up in the revision history a lot - can you help?

### br...@chromium.org (2011-04-28)

I can repro this reliably with a release pdf.dll. I don't see any instances getting torn down (and I don't see how this page would trigger that, either), so I don't think that's correct.

For skylined's patch, I think that will introduce a reference counting cycle. All the resources *should* be reset when the instance goes away, which is why that pointer is non-owning (it will get LastPluginRefWasDeleted).

I see it reliably on the 54th load completion callback crashing in pdf.dll. I'll try to get symbols for pdf.dll so I can look more.

### sc...@gmail.com (2011-04-29)

Thanks for taking a look, Brett.
Does it really fire reliably at the 54th completion every time? Sounds interesting that it would be so deterministic :)


### sk...@chromium.org (2011-04-29)

Hmmm... I can reliably crash in PPB_Widget_Impl::Invalidate without the AddRef/Release but not with it. Also, I added this CHECK and it triggers (and I don't think it ever should):

void PPB_Widget_Impl::Invalidate(const PP_Rect* dirty) {
  CHECK(GetReferenceNoAddRef() != 0);
  const PPP_Widget_Dev* widget = static_cast<const PPP_Widget_Dev*>(
      instance()->module()->GetPluginInterface(PPP_WIDGET_DEV_INTERFACE));
  if (!widget)
    return;
  ScopedResourceId resource(this);
  widget->Invalidate(instance()->pp_instance(), resource.id, dirty);
}

@brett: you know how the code works, so I'll leave tracking down the root cause to you if you don't mind.

### br...@chromium.org (2011-05-02)

I've decided the bug I was seeing with the 54th stream is something else. I got a new release build of pdf.dll from John (I was using a random one from some local install of Chrome I have) and that problem goes away.

I did a release build of Chrome and used the release build of pdf.dll, and I loaded the page a bunch of times and I didn't see any crashes.

Skylined: I tried adding your assert and I don't see it getting triggered. What's the stack you're seeing at that point?

### [Deleted User] (2011-05-02)

[Comment Deleted]

### br...@chromium.org (2011-05-03)

To be clear: the new DLL build is not known to fix any bugs, and I decided the problem I was seeing that it fixed is independent of this security bug.

### sc...@gmail.com (2011-05-03)

@brettw: this is definitely a heisenbug; thanks for taking a peek. Do you see a crash if you run an _optimized_ build from trunk, and refresh the repro lots of times? (John, I'd be interested to see if you see anything with that test too. Justin said he was seeing a sad tab in opt but not debug).

### [Deleted User] (2011-05-04)

[Comment Deleted]

### [Deleted User] (2011-05-04)

[Comment Deleted]

### sk...@chromium.org (2011-05-05)

It's really not difficult to trigger for me: I synced source to latest and cleanly rebuild DEBUG Chromium on Windows (with internal PDF code!) and it still crashes almost instantaneous.

@brettw: if you want, I can get you a copy of my build + symbols, but it's probably easier if you try building debug yourself on a windows machine.

I'll browse the code a bit more to get a better understanding of what it's supposed to do, and debug the crashes to see why it's not working.

### sk...@chromium.org (2011-05-05)

To be sure - it's easy to repro with a (modified) local copy of the original "exploit". Save attached files in one folder and load "repro.html" to see the crash. This works in 11.0.696.60 (stable release) as well.

### ja...@chromium.org (2011-05-08)

I just built latest code in Release mode, and tried both the original url and the repro from https://crbug.com/chromium/78639#c45.  I reloaded the former a number of times, and let the latter reload ~20x with no crash.  this doesn't repro.

### [Deleted User] (2011-05-09)

[Comment Deleted]

### [Deleted User] (2011-05-09)

[Comment Deleted]

### in...@chromium.org (2011-05-09)

reopening bug since it still reproduces for @marioso

### [Deleted User] (2011-05-13)

[Comment Deleted]

### in...@chromium.org (2011-05-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-05-26)

Mass update to M12.

### sc...@gmail.com (2011-06-02)

@mariosoufa: I promise that this bug is being taken seriously! Let me explain how seriously:
- I have been unable to reproduce on Linux, therefore I have just ordered a brand new Windows workstation. When it arrives, I will reproduce this bug and fix it.

### [Deleted User] (2011-06-02)

[Comment Deleted]

### sc...@gmail.com (2011-06-08)

Cris and I looked at this in WinDBG + canary. The length in %ecx is crazy big at the time of the crash. But length comes from a very simple string object on the heap. Seems like something might have messed up the heap. Unfortunately, there's all sorts of low-level thread-specific heap code :-/

### [Deleted User] (2011-06-13)

Stacktrace with symbols.

### er...@chromium.org (2011-06-21)

BTW I can reproduce this reliably, see https://crbug.com/chromium/86234.

What I see happening in https://crbug.com/chromium/86234 is that PPB_Scrollbar_Impl::invalidateScrollbarRect() posts a task for PPB_Scrollbar_Impl::NotifyInvalidate.

Then the webkit::ppapi::PluginInstance is deleted.

Then the NotifyInvalidate task runs, and ties to access a deleted PluginInstance.

### sc...@gmail.com (2011-06-21)

@eroman: apologies for re-opening, but are you sure it's the same issue?
We've actually seen two very different bugs based on this repro case:
1) The PPAPI object lifetime issue.
2) A weird crash inside the PDF code (see https://crash/reportdetail?reportid=e9dd9fafc6b1d424 from https://crbug.com/chromium/78639#c18)

Cris Neckar (@cdn) has confirmed that he can still repro the PDF crash on canary, which has the PPAPI object lifetime issue fixed.

So we think there's still somethere here. It's a really hard one.

### [Deleted User] (2011-06-21)

[Comment Deleted]

### in...@chromium.org (2011-07-06)

Moving all M12 bugs to M13. We won't have another M12 patch.

### sc...@gmail.com (2011-07-18)

Ok, starting next week, I have a new Windows7 machine. I'm excited to tackle the last piece of this bug hard.

### [Deleted User] (2011-07-19)

@scarybeasts: Testing with another PDF file, other than that, I get another error
totally different. All different stacktrace, the error location.
You think it's the same bug?

(f08.3c0): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=079d09a0 ebx=01345370 ecx=01345370 edx=02575c75 esi=01345370 edi=013453a4
eip=0256baa4 esp=0013f85c ebp=0013f8a0 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010246
chrome_1c30000!webkit::ppapi::PPB_Widget_Impl::Invalidate+0x8:
0256baa4 8b400c          mov     eax,dword ptr [eax+0Ch] ds:0023:079d09ac=????????
1:019> kp
ChildEBP RetAddr  
0013f8a0 021bc998 chrome_1c30000!webkit::ppapi::PPB_Widget_Impl::Invalidate(struct PP_Rect * dirty = 0x021bc998)+0x8 [d:\b\build\slave\chrome-official\build\src\webkit\plugins\ppapi\ppb_widget_impl.cc @ 99]
0013f8c0 021bca1f chrome_1c30000!MessageLoop::RunTask(class Task * task = 0x013d6378)+0x7d [d:\b\build\slave\chrome-official\build\src\base\message_loop.cc @ 372]
0013f8d0 021bcdba chrome_1c30000!MessageLoop::DeferOrRunPendingTask(struct MessageLoop::PendingTask * pending_task = 0x079d09a0)+0x28 [d:\b\build\slave\chrome-official\build\src\base\message_loop.cc @ 383]
0013f900 021d3525 chrome_1c30000!MessageLoop::DoWork(void)+0x71 [d:\b\build\slave\chrome-official\build\src\base\message_loop.cc @ 573]
0013f92c 021bc919 chrome_1c30000!base::MessagePumpDefault::Run(class base::MessagePump::Delegate * delegate = 0x0013fb48)+0xc2 [d:\b\build\slave\chrome-official\build\src\base\message_pump_default.cc @ 50]
0013f938 021bc89e chrome_1c30000!MessageLoop::RunInternal(void)+0x31 [d:\b\build\slave\chrome-official\build\src\base\message_loop.cc @ 347]
0013f940 021bc792 chrome_1c30000!MessageLoop::RunHandler(void)+0x17 [d:\b\build\slave\chrome-official\build\src\base\message_loop.cc @ 319]
0013f960 01c3f644 chrome_1c30000!MessageLoop::Run(void)+0x15 [d:\b\build\slave\chrome-official\build\src\base\message_loop.cc @ 244]
0013fc7c 01c341e7 chrome_1c30000!RendererMain(struct MainFunctionParams * parameters = 0x0013fcc8)+0x309 [d:\b\build\slave\chrome-official\build\src\content\renderer\renderer_main.cc @ 234]
0013fe3c 004020f9 chrome_1c30000!ChromeMain(struct HINSTANCE__ * instance = 0x00400000, struct sandbox::SandboxInterfaceInfo * sandbox_info = 0x0013ff1c, wchar_t * command_line_unused = 0x000209e8 ""C:\Documents and Settings\C4SS!0\Configurações locais\Dados de aplicativos\Google\Chrome\Application\chrome.exe" --type=renderer --disable-client-side-phishing-detection --lang=pt-BR --force-fieldtest=ConnCountImpact/conn_count_6/ConnnectBackupJobs/ConnectBackupJobsEnabled/DnsImpact/default_enabled_prefetch/DnsParallelism/parallel_default/GlobalSdch/global_enable_sdch/IdleSktToImpact/idle_timeout_60/Prefetch/ContentPrefetchDisabled/ProxyConnectionImpact/proxy_connections_32/SSLFalseStart/FalseStart_disabled/SpdyCwnd/cwndDynamic/SpdyImpact/npn_with_spdy/WebSocketExperiment/default/ --disable-webgl --disable-gl-multisampling --disable-accelerated-compositing --channel=2156.0149CA10.99564755 /prefetch:3")+0x653 [d:\b\build\slave\chrome-official\build\src\chrome\app\chrome_main.cc @ 821]
0013fec4 0040423d chrome!MainDllLoader::Launch(struct HINSTANCE__ * instance = 0x00400000, struct sandbox::SandboxInterfaceInfo * sbox_info = 0x0013ff1c)+0xf0 [d:\b\build\slave\chrome-official\build\src\chrome\app\client_util.cc @ 250]
0013ff30 00453a1b chrome!wWinMain(struct HINSTANCE__ * instance = 0x00400000, struct HINSTANCE__ * __formal = 0x00000000)+0xef [d:\b\build\slave\chrome-official\build\src\chrome\app\chrome_exe_main_win.cc @ 46]
0013ffc0 7c817077 chrome!__tmainCRTStartup(void)+0x112 [f:\dd\vctools\crt_bld\self_x86\crt\src\crt0.c @ 263]
0013fff0 00000000 kernel32!BaseProcessStart+0x23
1:019> .exr -1
ExceptionAddress: 0256baa4 (chrome_1c30000!webkit::ppapi::PPB_Widget_Impl::Invalidate+0x00000008)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 079d09ac
Attempt to read from address 079d09ac
1:019> .lastevent
Last event: f08.3c0: Access violation - code c0000005 (first chance)
  debugger time: Tue Jul 19 11:45:58.000 2011 (UTC - 3:00)
1:019> dv /v
@eax            this = 0x079d09a0
0013f8a4           dirty = 0x021bc998
1:019> dt this
Local var @ eax Type webkit::ppapi::PPB_Widget_Impl*
   +0x004 ref_count_       : ??
   +0x000 __VFN_table : ???? 
   +0x008 resource_id_     : ??
   +0x00c instance_        : ???? 
   +0x010 location_        : PP_Rect
Memory read error 079d09ac


### sc...@gmail.com (2011-07-19)

@MarioSoufa: that most recent stack trace you just posted looks like a bug @cdn fixed recently. What version did you hit it in?

### [Deleted User] (2011-07-19)

Chrome Version 12.0.742.122 stable

### sc...@gmail.com (2011-07-20)

@MarioSoufa: we'd like to offer you a provisional $500 Chromium Security Reward for your help so far! In particular, we believe you were the first to point us towards the specific issue you noted in https://crbug.com/chromium/78639#c62 above.

We reserve the right to offer additional rewards for this bug at a later date. As I note in https://crbug.com/chromium/78639#c61, I still have some investigation to perform on this bug and I am set up to dig into the other crash stack next week with my new Windows machine.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### [Deleted User] (2011-07-20)

Thank you!!!!.
I'm very excited, this is my first reward for finding bugs. :-)
Now, i can buy a new smartphone.

### [Deleted User] (2011-07-26)

Only crash in Windows.

### sc...@gmail.com (2011-07-27)

[Empty comment from Monorail migration]

### ce...@google.com (2011-07-27)

Just checking the repro still works reliably against latest canary (14.0.835.4).
It does: https://crash/reportdetail?reportid=622f3eb287422a70

### sc...@gmail.com (2011-07-29)

Fixed at PDF r1063. I'll merge it to M14 shortly.

@mariosoufa: sorry for the delay on this one. Hard to reproduce, but I got it when my new Windows machine arrived :D
The underlying issue is actually a memory corruption, so the rewards panel will discuss an additional reward.

### sc...@gmail.com (2011-07-29)

@mariosoufa: since you helped with two distinct bugs, we're topping your reward up to $1000 :D This particular aspect (the crash in the PDF code) will be released to stable in Chrome 14.

### [Deleted User] (2011-07-29)

Wow!Thank you very much.

### sc...@gmail.com (2011-07-29)

Merged to M14 at r1064

### [Deleted User] (2011-08-06)

[Comment Deleted]

### sc...@gmail.com (2011-09-09)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### sc...@gmail.com (2011-10-10)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### sc...@gmail.com (2012-07-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/78639?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>Plugins>PDF]
[Monorail mergedwith: crbug.com/chromium/78640, crbug.com/chromium/83935]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089624)*
