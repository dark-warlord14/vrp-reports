# UNKNOWN in extensions::WebrtcAudioPrivateFunction::CalculateHMACImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40083448](https://issues.chromium.org/issues/40083448) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebRTC, Platform>Extensions, Platform>Extensions>API |
| **CVE IDs** | CVE-2016-1639 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2015-12-25 |
| **Bounty** | $1,000.00 |

## Description

Chrome Version: Stable 47.0.2526.106 m
Operating System: Windows 7
Type of crash: Browser
Crash ID: 37321703cbf38db9

 
I don't have specific steps to repro this crash, but sometimes I can reproduce it but I don't know what are the steps I took.
This crash happened when I used a new incognito window and I opened gmail then I closed the incognito window.


eax=05c4f7f8 ebx=21f58d50 ecx=2449acc0 edx=674e0ccd esi=05c4f8a0 edi=11cb06d0
eip=756e4500 esp=05c4f7dc ebp=05c4f868 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010246
756e4500 ??              ???
0:013> k
  *** Stack trace for last set context - .thread/.cxr resets it
ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
05c4f7d8 672b388c 0x756e4500
05c4f868 672b41f7 chrome_65bc0000!extensions::WebrtcAudioPrivateFunction::CalculateHMACImpl+0x66 [c:\b\build\slave\win\build\src\chrome\browser\extensions\api\webrtc_audio_private\webrtc_audio_private_api.cc @ 207]
05c4f8bc 672b4469 chrome_65bc0000!extensions::WebrtcAudioPrivateGetSinksFunction::OnOutputDeviceNames+0x5b [c:\b\build\slave\win\build\src\chrome\browser\extensions\api\webrtc_audio_private\webrtc_audio_private_api.cc @ 237]
05c4f8cc 672b3de7 chrome_65bc0000!base::internal::RunnableAdapter<void (__thiscall extensions::WebrtcAudioPrivateFunction::*)(scoped_ptr<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> >,base::DefaultDeleter<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> > > >)>::Run+0x1a [c:\b\build\slave\win\build\src\base\bind_internal.h @ 176]
05c4f8dc 672b4448 chrome_65bc0000!base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall extensions::WebrtcAudioPrivateFunction::*)(scoped_ptr<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> >,base::DefaultDeleter<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> > > >)>,base::internal::TypeList<extensions::WebrtcAudioPrivateFunction * const &,scoped_ptr<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> >,base::DefaultDeleter<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> > > > > >::MakeItSo+0x1c [c:\b\build\slave\win\build\src\base\bind_internal.h @ 294]
05c4f8fc 65c1e84e chrome_65bc0000!base::internal::Invoker<base::IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (__thiscall extensions::WebrtcAudioPrivateFunction::*)(scoped_ptr<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> >,base::DefaultDeleter<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> > > >)>,void __cdecl(extensions::WebrtcAudioPrivateFunction *,scoped_ptr<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> >,base::DefaultDeleter<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> > > >),base::internal::TypeList<extensions::WebrtcAudioPrivateFunction *,base::internal::PassedWrapper<scoped_ptr<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> >,base::DefaultDeleter<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> > > > > > >,base::internal::TypeList<base::internal::UnwrapTraits<extensions::WebrtcAudioPrivateFunction *>,base::internal::UnwrapTraits<base::internal::PassedWrapper<scoped_ptr<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> >,base::DefaultDeleter<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> > > > > > >,base::internal::InvokeHelper<0,void,base::internal::RunnableAdapter<void (__thiscall extensions::WebrtcAudioPrivateFunction::*)(scoped_ptr<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> >,base::DefaultDeleter<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> > > >)>,base::internal::TypeList<extensions::WebrtcAudioPrivateFunction * const &,scoped_ptr<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> >,base::DefaultDeleter<std::list<media::AudioDeviceName,std::allocator<media::AudioDeviceName> > > > > >,void __cdecl(void)>::Run+0x29 [c:\b\build\slave\win\build\src\base\bind_internal.h @ 346]
05c4f960 65c1e630 chrome_65bc0000!base::debug::TaskAnnotator::RunTask+0x158 [c:\b\build\slave\win\build\src\base\debug\task_annotator.cc @ 51]
05c4f9cc 65c1e042 chrome_65bc0000!base::MessageLoop::RunTask+0x181 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 483]
05c4fb00 65c1dbb8 chrome_65bc0000!base::MessageLoop::DoWork+0x478 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 603]
05c4fb14 65c1dadd chrome_65bc0000!base::MessagePumpForIO::DoRunLoop+0x8f [c:\b\build\slave\win\build\src\base\message_loop\message_pump_win.cc @ 496]
*** ERROR: Symbol file could not be found.  Defaulted to export symbols for ole32.dll - 
05c4fbec 76e9eb4d chrome_65bc0000!base::MessageLoop::StartHistogrammer+0xb0 [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 572]
05c4fc18 65bc1a3d ole32!CoTaskMemAlloc+0x101
05c4fc2c 65bc1a14 chrome_65bc0000!`anonymous namespace'::win_heap_malloc+0x1d [c:\b\build\slave\win\build\src\base\allocator\allocator_shim_win.cc @ 58]
05c4fc3c 65bc38af chrome_65bc0000!malloc+0x27 [c:\b\build\slave\win\build\src\base\allocator\allocator_shim_win.cc @ 165]
05c4fc4c 67ac326c chrome_65bc0000!`anonymous namespace'::generic_cpp_alloc+0x1f [c:\b\build\slave\win\build\src\base\allocator\allocator_shim_win.cc @ 102]
05c4fc60 65be4d1b chrome_65bc0000!content::`anonymous namespace'::g_globals+0x4
05c4fc94 65c1a4ba chrome_65bc0000!base::MessageLoop::current+0x3a [c:\b\build\slave\win\build\src\base\message_loop\message_loop.cc @ 186]
05c4fcd0 65c1a29e chrome_65bc0000!base::Thread::ThreadMain+0x153 [c:\b\build\slave\win\build\src\base\threading\thread.cc @ 254]
05c4fcf0 76643c45 chrome_65bc0000!base::`anonymous namespace'::ThreadFunc+0x87 [c:\b\build\slave\win\build\src\base\threading\platform_thread_win.cc @ 84]
05c4fcfc 77c637f5 kernel32!BaseThreadInitThunk+0x12


## Timeline

### jw...@chromium.org (2015-12-25)

Can you give us a list of extensions that you have installed? It would especially useful to know if any of those have "Allow in incognito" is checked for them, since it appears that this happens in incognito mode.

Devlin, this code was all written by joi@ back in the day. Can you help me find the appropriate owner to take a look at this. Since it involves HMAC code, I'm also throwing a Hail Mary and CC'ing eroman@ in the hopes that he might know a good owner.

### jw...@chromium.org (2015-12-25)

[Empty comment from Monorail migration]

### ch...@gmail.com (2015-12-25)

I have installed "AudioRecorder" and "Browser Sample" but are not allowed in incognito.

### er...@chromium.org (2015-12-28)

Thanks for the report.

tl;dr: The problem has nothing to do with HMAC, but rather is a use-after-free of the WebrtcAudioPrivateFunction::resource_context_ member.
On a side note, the crash dump also indicates that your machine is "infected" [1]

WebrtcAudioPrivateFunction holds a raw pointer to a content::ResourceContext. This is initialized with GetProfile()->GetResourceContext().

In this case the profile in question is an incognito one, so its lifetime is shorter. When closing the last incognito window the resource context must be getting torn down before the code in question executes. This results in the use of a freed resource_context_ member.

The crash shows that resource_context_ is bogus -- it crashes trying to do a virtual function call, however the vtable (@edx) is completely bogus (in fact it points to a static section of the DLL).

To fix this bug the lifetime of cached ResourceContext in WebrtcAudioPrivateFunction will need to be resolved.  Probably will involve cancel the callback that was posted to IOThread when the profile is destroyed.


Here is the code in question:

203:  GURL security_origin(source_url().GetOrigin());
204:  return content::GetHMACForMediaDeviceID(
205:      resource_context()->GetMediaDeviceIDSalt(),
206:      security_origin,
207:      raw_id);

chrome_65bc0000!extensions::WebrtcAudioPrivateFunction::CalculateHMACImpl+0x46 [c:\b\build\slave\win\build\src\chrome\browser\extensions\api\webrtc_audio_private\webrtc_audio_private_api.cc @ 203]:
  203 672b386c 8d4598          lea     eax,[ebp-68h]
  203 672b386f 50              push    eax
  203 672b3870 8d4b18          lea     ecx,[ebx+18h]
  203 672b3873 e89df29cfe      call    chrome_65bc0000!GURL::GetOrigin (65c82b15)
  207 672b3878 8b8be0000000    mov     ecx,dword ptr [ebx+0E0h]  <==== ECX = resource_context_
  207 672b387e 8d4598          lea     eax,[ebp-68h]
  207 672b3881 57              push    edi
  207 672b3882 50              push    eax
  207 672b3883 8d4590          lea     eax,[ebp-70h]
  207 672b3886 8b11            mov     edx,dword ptr [ecx]    <==== EDX = vptr for resource_context_
  207 672b3888 50              push    eax
  207 672b3889 ff5214          call    dword ptr [edx+14h]    <===== virtual function call for GetMediaDeviceIDSalt().
  207 672b388c 50              push    eax
  207 672b388d 56              push    esi
  207 672b388e e8cf9679ff      call    chrome_65bc0000!content::GetHMACForMediaDeviceID (66a4cf62)
  207 672b3893 83c410          add     esp,10h
  207 672b3896 8d4d90          lea     ecx,[ebp-70h]
  207 672b3899 e852e791fe      call    chrome_65bc0000!base::internal::CallbackBase::~CallbackBase (65bd1ff0)
  207 672b389e 8d4d98          lea     ecx,[ebp-68h]
  207 672b38a1 e8464896fe      call    chrome_65bc0000!GURL::~GURL (65c180ec)
  207 672b38a6 eb0c            jmp     chrome_65bc0000!extensions::WebrtcAudioPrivateFunction::CalculateHMACImpl+0x8e (672b38b4)


[1] Means a third party program externally manipulated the Chrome settings. See https://support.google.com/chrome/answer/6086368?hl=en

### jw...@chromium.org (2015-12-28)

Thanks, Eric! In that case, I'm still going to leave it with Devlin to triage.

### jw...@chromium.org (2015-12-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-29)

[Empty comment from Monorail migration]

### ch...@gmail.com (2016-01-13)

Any updates on this bug?

### cl...@chromium.org (2016-01-19)

rdevlin.cronin@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ch...@gmail.com (2016-01-28)

Any updates?

### ch...@gmail.com (2016-02-03)

rdevlin.cronin@: Could you please take a look at this issue?

### in...@chromium.org (2016-02-09)

Pbos@, this looks more like a webrtc issue. Can you please help to triage.

### cl...@chromium.org (2016-02-09)

pbos@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### pb...@chromium.org (2016-02-09)

tommi@ this looks like the Chromium side, can you help triage?

### to...@chromium.org (2016-02-09)

Guido - can you take a look?

### bu...@chromium.org (2016-02-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c4e893a3352c34e1a22ec6afad115887a69f576e

commit c4e893a3352c34e1a22ec6afad115887a69f576e
Author: guidou <guidou@chromium.org>
Date: Fri Feb 12 21:30:29 2016

Store device salt callback instead of resource context in WebRTC Audio Private API

The resource context pointer was used only to get access to the device
ID salt callback. However, the resource context pointer can become dangling and cause
use-after-free issues.

BUG=572224

Review URL: https://codereview.chromium.org/1692913003

Cr-Commit-Position: refs/heads/master@{#375259}

[modify] http://crrev.com/c4e893a3352c34e1a22ec6afad115887a69f576e/chrome/browser/extensions/api/webrtc_audio_private/webrtc_audio_private_api.cc
[modify] http://crrev.com/c4e893a3352c34e1a22ec6afad115887a69f576e/chrome/browser/extensions/api/webrtc_audio_private/webrtc_audio_private_api.h


### in...@chromium.org (2016-02-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-13)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### gu...@chromium.org (2016-02-15)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-15)

Your change meets the bar and is auto-approved for M49 (branch: 2623)

### bu...@chromium.org (2016-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/048b308e940105b66e242ec9e0e2efe7d7adf0a4

commit 048b308e940105b66e242ec9e0e2efe7d7adf0a4
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Feb 17 00:16:51 2016

Store device salt callback instead of resource context in WebRTC Audio Private API

The resource context pointer was used only to get access to the device
ID salt callback. However, the resource context pointer can become dangling and cause
use-after-free issues.

BUG=572224

Review URL: https://codereview.chromium.org/1692913003

Cr-Commit-Position: refs/heads/master@{#375259}
(cherry picked from commit c4e893a3352c34e1a22ec6afad115887a69f576e)

Review URL: https://codereview.chromium.org/1703733002 .

Cr-Commit-Position: refs/branch-heads/2623@{#418}
Cr-Branched-From: 92d77538a86529ca35f9220bd3cd512cbea1f086-refs/heads/master@{#369907}

[modify] http://crrev.com/048b308e940105b66e242ec9e0e2efe7d7adf0a4/chrome/browser/extensions/api/webrtc_audio_private/webrtc_audio_private_api.cc
[modify] http://crrev.com/048b308e940105b66e242ec9e0e2efe7d7adf0a4/chrome/browser/extensions/api/webrtc_audio_private/webrtc_audio_private_api.h


### bu...@chromium.org (2016-02-17)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/048b308e940105b66e242ec9e0e2efe7d7adf0a4

commit 048b308e940105b66e242ec9e0e2efe7d7adf0a4
Author: Guido Urdaneta <guidou@chromium.org>
Date: Wed Feb 17 00:16:51 2016


### ti...@google.com (2016-02-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-02)

Congrats - $1,000 for this report. I'll follow up with a CVE-ID shortly and we'll mention this in the release notes later today.

### ti...@google.com (2016-03-02)

CVE-2016-1639

### ti...@google.com (2016-03-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-05-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/572224?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebRTC, Platform>Extensions, Platform>Extensions>API]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083448)*
