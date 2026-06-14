# Chrome sandbox escape due to use of invalid PP_Instance in IPC handler OnMsgDidDeleteInProcessInstance

| Field | Value |
|-------|-------|
| **Issue ID** | [40088095](https://issues.chromium.org/issues/40088095) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>Pepper |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | bb...@chromium.org |
| **Created** | 2017-06-15 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36

Steps to reproduce the problem:
The sandbox process can send the following IPC message to browser process:
IPC_MESSAGE_HANDLER(FrameHostMsg_DidDeleteInProcessInstance,
                        OnMsgDidDeleteInProcessInstance)

The implementation of BrowserPpapiHostImpl::DeleteInstance fails however to verify that the instance is actually an instance to a message it sent:
void BrowserPpapiHostImpl::DeleteInstance(PP_Instance instance) {
  auto it = instance_map_.find(instance);
  DCHECK(it != instance_map_.end());

  // We need to tell the observers for that instance that we are destroyed
  // because we won't have the opportunity to once we remove them from the
  // |instance_map_|. If the instance was deleted, observers for those instances
  // should never call back into the host anyway, so it is safe to tell them
  // that the host is destroyed.
  for (auto& observer : it->second->observer_list)
    observer.OnHostDestroyed();

  instance_map_.erase(it);
}

If the instance (which is controlled by the sandbox process) isn't in the instance_map_ then it will be end(). In this case it's gonna end up reading uninitialized memory in heap and then crash the browser process.

What is the expected behavior?

What went wrong?
Chrome sandbox escape

Did this work before? N/A 

Chrome version: 60.0.3101.0  Channel: dev
OS Version: 10.0
Flash Version: Shockwave Flash 26.0 r0

Credit to Yu Zhou, Yuan Deng of Ant-financial Light-Year Security Lab(蚂蚁金服巴斯光年安全实验室)

## Attachments

- [patch_del.diff](attachments/patch_del.diff) (application/octet-stream, 724 B)

## Timeline

### es...@chromium.org (2017-06-15)

bbudge, PTAL at this Pepper bug as well

[Monorail components: Internals>Plugins>Pepper]

### bb...@chromium.org (2017-06-16)

Hopefully it's a null pointer de-reference, which should crash right away.

Like the other one, we should validate the PP_Instance.

### sh...@chromium.org (2017-06-16)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-16)

[Empty comment from Monorail migration]

### bb...@chromium.org (2017-06-17)

If no one is working on this I can take a shot at it.

### bb...@chromium.org (2017-06-20)

Fix landed in trunk:

https://chromium-review.googlesource.com/c/538908/

### ch...@gmail.com (2017-06-21)

[Comment Deleted]

### bb...@chromium.org (2017-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-06-22)

This bug requires manual review: M60 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), josafat@(ChromeOS), bustamante@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bb...@chromium.org (2017-06-22)

[Comment Deleted]

### bb...@chromium.org (2017-06-22)

[Comment Deleted]

### sh...@chromium.org (2017-06-23)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2017-06-23)

Approving merge to M60. 

### bu...@chromium.org (2017-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2e98fb826886c18acdd55890ee0b52d2aee57394

commit 2e98fb826886c18acdd55890ee0b52d2aee57394
Author: Bill Budge <bbudge@chromium.org>
Date: Fri Jun 23 22:23:17 2017

Validate in-process plugin instance messages.

Bug: 733548, 733549
Cq-Include-Trybots: master.tryserver.chromium.linux:linux_site_isolation
Change-Id: Ie5572c7bcafa05399b09c44425ddd5ce9b9e4cba
Reviewed-on: https://chromium-review.googlesource.com/538908
Commit-Queue: Bill Budge <bbudge@chromium.org>
Reviewed-by: Raymes Khoury <raymes@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#480696}
Review-Url: https://codereview.chromium.org/2955703002 .
Cr-Commit-Position: refs/branch-heads/3112@{#456}
Cr-Branched-From: b6460e24cf59f429d69de255538d0fc7a425ccf9-refs/heads/master@{#474897}

[modify] https://crrev.com/2e98fb826886c18acdd55890ee0b52d2aee57394/content/browser/renderer_host/pepper/browser_ppapi_host_impl.cc
[modify] https://crrev.com/2e98fb826886c18acdd55890ee0b52d2aee57394/content/browser/renderer_host/pepper/pepper_renderer_connection.cc


### sh...@chromium.org (2017-06-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-06-28)

Hi chinaxiaozhouzhou@. The VRP panel has looked at this, and ask if you could provide a proof of concept, or details about how this could be triggered?

### ch...@gmail.com (2017-06-29)

Chromium Version: 60.0.3101.0 dev
Test on: Windows 7 SP1 x86

Some simple steps to reproduce the vulnerability:
1. Use WinDbg to attach sandbox process and browser process.

2. In the sandbox process, set breakpoint at chrome_child!IPC::ChannelProxy::Context::OnSendMessage. Then replace the original ipc message. Set payload_size 0x4. Set type 0x00010542(FrameHostMsg_DidDeleteInProcessInstance). Set payload 0x41414141.
0:002> dd 0240a410 
0240a410  00000004 00000002 00010542 19032002
0240a420  41414141 00000002 00000001 00000000

3. Continue to run. Now the browser process is crashing.
(8fc.ec0): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=06ccf140 ebx=00000000 ecx=0000017f edx=0d725f40 esi=0d725f40 edi=0858aa70
eip=67278500 esp=06ccf11c ebp=06ccf11c iopl=0         nv up ei pl nz na po nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010202
*** WARNING: Unable to verify checksum for C:\Users\Administrator\AppData\Local\Chromium\Application\60.0.3101.0\chrome.dll
chrome_67110000!base::ObserverListBase<zoom::ZoomObserver>::begin+0x3:
67278500 8b4104          mov     eax,dword ptr [ecx+4] ds:0023:00000183=????????
0:012> kv
ChildEBP RetAddr  Args to Child              
06ccf11c 675e8ca5 06ccf140 101859a0 691bfcc4 chrome_67110000!base::ObserverListBase<zoom::ZoomObserver>::begin+0x3
06ccf154 675f4f11 41414141 06ccf320 00000001 chrome_67110000!content::BrowserPpapiHostImpl::DeleteInstance+0x2f
06ccf180 675f550f 06ccf320 101859a0 101859a0 chrome_67110000!IPC::MessageT<FrameHostMsg_DidDeleteInProcessInstance_Meta,std::tuple<int>,void>::Dispatch<content::PepperRendererConnection,content::PepperRendererConnection,void,void (__thiscall content::PepperRendererConnection::*)(int)>+0x7b
06ccf22c 67357a42 06ccf320 00000002 0d5c8920 chrome_67110000!content::PepperRendererConnection::OnMessageReceived+0xee
06ccf264 67b3cef1 06ccf320 0d5c8908 06ccf320 chrome_67110000!content::BrowserMessageFilter::Internal::OnMessageReceived+0xa6
06ccf278 67b3cec6 0d5c8920 06ccf320 06ccf320 chrome_67110000!IPC::MessageFilterRouter::TryFilters+0x63
06ccf290 67b386c7 06ccf320 06ccf320 0d35bbb8 chrome_67110000!IPC::MessageFilterRouter::TryFilters+0x38
06ccf2c4 67b383f9 06ccf320 691bfcb8 06ccf308 chrome_67110000!IPC::ChannelProxy::Context::TryFilters+0x17
06ccf2d4 67b36932 06ccf320 1022fc88 691bfba4 chrome_67110000!IPC::ChannelProxy::Context::OnMessageReceived+0xe
06ccf308 67b3a5f4 06ccf320 1022fc88 68e26f3c chrome_67110000!IPC::ChannelMojo::OnMessageReceived+0x8d
06ccf350 67b3db15 06ccf448 691bfa01 06ccf400 chrome_67110000!IPC::internal::MessagePipeReader::Receive+0xb4
06ccf494 67b3a402 1022fc88 06ccf5f8 06ccf4c4 chrome_67110000!IPC::mojom::ChannelStubDispatch::Accept+0x2ba
06ccf4a4 6782ba8a 06ccf5f8 0d465510 0858a3c0 chrome_67110000!IPC::mojom::ChannelStub<mojo::RawPtrImplRefTraits<IPC::mojom::Channel> >::Accept+0x18
06ccf4c4 67b3b297 06ccf5f8 0d41f410 0d41f410 chrome_67110000!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x12a
06ccf534 6782ce98 0790dab8 0d41f458 10187cc0 chrome_67110000!IPC::`anonymous namespace'::MojoBootstrapImpl::`scalar deleting destructor'+0xaf
06ccf638 6782cd89 06ccf658 00000000 10187ca0 chrome_67110000!mojo::Connector::ReadSingleMessage+0xb4
06ccf65c 6782cc97 06ccf670 683d5e62 00000000 chrome_67110000!mojo::Connector::ReadAllAvailableMessages+0x2d
06ccf664 683d5e62 00000000 06ccf698 678bbb7d chrome_67110000!mojo::Connector::OnHandleReadyInternal+0x22
06ccf670 678bbb7d 1018a8a0 06ccf694 06ccf9b8 chrome_67110000!base::internal::Invoker<base::internal::BindState<void (__thiscall OneGoogleBarFetcherImpl::*)(net::URLFetcher const *),base::internal::UnretainedWrapper<OneGoogleBarFetcherImpl> >,void __cdecl(net::URLFetcher const *)>::RunOnce+0x11
06ccf698 6764e9e4 1018a8a0 68e27038 68cf9118 chrome_67110000!mojo::SimpleWatcher::OnHandleReady+0x73
06ccf6ac 67431988 678bbb0a 0d21fae4 0d21fae0 chrome_67110000!base::internal::FunctorTraits<void (__thiscall VersionHandler::*)(std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > *,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > *),void>::Invoke<base::WeakPtr<VersionHandler>,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > *,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > *>+0x26
06ccf6c4 68b88472 0d21fad8 0d21fae4 0d21fae0 chrome_67110000!base::internal::InvokeHelper<1,void>::MakeItSo<void (__thiscall VersionHandler::*)(std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > *,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > *),base::WeakPtr<VersionHandler>,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > *,std::basic_string<wchar_t,std::char_traits<wchar_t>,std::allocator<wchar_t> > *>+0x22
06ccf6dc 68b88704 0d21fad8 0d21fadc 0d21fac8 chrome_67110000!base::internal::Invoker<base::internal::BindState<void (__thiscall mojo::SimpleWatcher::*)(int,unsigned int),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int>,void __cdecl(void)>::RunImpl<void (__thiscall mojo::SimpleWatcher::*const &)(int,unsigned int),std::tuple<base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int> const &,0,1,2>+0x17
06ccf6f0 678a90e4 0d21fac8 06ccf9b8 678bbae4 chrome_67110000!base::internal::Invoker<base::internal::BindState<void (__thiscall mojo::SimpleWatcher::*)(int,unsigned int),base::WeakPtr<mojo::SimpleWatcher>,int,unsigned int>,void __cdecl(void)>::Run+0x16
06ccf7c0 6786e349 68cf1b8c 06ccf9b8 7708bf00 chrome_67110000!base::debug::TaskAnnotator::RunTask+0x174
06ccf920 6786dc64 06ccf9b8 7708bf00 00e686f0 chrome_67110000!base::MessageLoop::RunTask+0x409
06ccfa10 678a9c5d 00000000 00e686f0 68c65108 chrome_67110000!base::MessageLoop::DoWork+0x2d4
06ccfa3c 678aa26a 68c08250 06ccfc94 00e584c8 chrome_67110000!base::MessagePumpForIO::DoRunLoop+0xcd
06ccfa64 6786df3b 00e584c8 67887643 00aad1d8 chrome_67110000!base::MessagePumpWin::Run+0x4a
06ccfa6c 67887643 00aad1d8 041412cf 06ccfb44 chrome_67110000!base::MessageLoop::RunHandler+0xb (FPO: [0,0,0])
06ccfadc 6786c2db 06ccfbb0 673d6c00 06ccfc94 chrome_67110000!base::RunLoop::Run+0x33
06ccfae4 673d6c00 06ccfc94 06ccfb04 6785be5d chrome_67110000!base::Thread::Run+0xb
06ccfbb0 673d72fa 06ccfc94 00000000 00aad209 chrome_67110000!content::BrowserThreadImpl::IOThreadRun+0x1e
06ccfc7c 6786c683 06ccfc94 7708bb80 00e5cb30 chrome_67110000!content::BrowserThreadImpl::Run+0xf6
06ccfcc8 67849ec2 00000000 00000000 00e5cb30 chrome_67110000!base::Thread::ThreadMain+0x123
06ccfce4 77093c45 000003a8 06ccfd30 776137f5 chrome_67110000!base::PlatformThread::Sleep+0x112
06ccfcf0 776137f5 00e5cb30 75b76c9d 00000000 kernel32!BaseThreadInitThunk+0xe (FPO: [Non-Fpo])
06ccfd30 776137c8 67849e40 00e5cb30 00000000 ntdll!__RtlUserThreadStart+0x70 (FPO: [Non-Fpo])
06ccfd48 00000000 67849e40 00e5cb30 00000000 ntdll!_RtlUserThreadStart+0x1b (FPO: [Non-Fpo])


The implementation of BrowserPpapiHostImpl::DeleteInstance fails however to verify that the instance is actually an instance to a message it sent. In this case, the instance 0x41414141 isn't in the instance_map_. Then it will read uninitialized memory after end object.


### ch...@gmail.com (2017-06-29)

Some vulnerabilities which are similar to this one:
https://bugs.chromium.org/p/project-zero/issues/detail?id=665
https://bugs.chromium.org/p/chromium/issues/detail?id=249064

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@google.com (2017-07-24)

Congratulations, the panel decided to award $5,000 for this bug, along with 733548.

### aw...@google.com (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gu...@gmail.com (2017-10-09)

unh,but how it can lead to sandbox escape? looks like a bug.

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/733549?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088095)*
