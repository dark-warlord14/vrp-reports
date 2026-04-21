# UAF in webrtc::SctpDataChannel::UpdateState (WEBRTC)

| Field | Value |
|-------|-------|
| **Issue ID** | [40069005](https://issues.chromium.org/issues/40069005) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>DataChannel |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2023-08-08 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**

- ubuntu 22.04
- MacOS Ventura 13.4  
  
  chromium version:  
  
  Chromium 117.0.5932.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1180021.zip)  
  
  Chromium 117.0.5911.2

repro steps:  

This UAF is derived from the PoC I previously submitted (<https://bugs.chromium.org/p/chromium/issues/detail?id=1454086#c8>), with modifications including the addition of stress testing code.  

However, the repro is less stable compared to the previous one. So, I wrote a simple testing script and opened multiple browsers simultaneously. The crash repro after waiting for about 60 seconds.  

./test.sh 2>&1 | grep -E 'AddressSanitizer'

From the ASan logs, it's evident that this UAF is different from the previous ones, indicating that it's not caused by incomplete fixes.

# **Problem Description:**

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x50400042a350 at pc 0x55d4d96fcd88 bp 0x7f9599bfbaf0 sp 0x7f9599bfbae8  

READ of size 8 at 0x50400042a350 thread T12 (WebRTC\_W\_and\_N)  

#0 0x55d4d96fcd87 in SetState ./../../third\_party/webrtc/pc/sctp\_data\_channel.cc:842:16  

#1 0x55d4d96fcd87 in webrtc::SctpDataChannel::UpdateState() ./../../third\_party/webrtc/pc/sctp\_data\_channel.cc:793:11  

#2 0x55d4c59626a4 in webrtc::DataChannelController::OnReadyToSend() ./../../third\_party/webrtc/pc/data\_channel\_controller.cc:138:16  

#3 0x55d4d95ac640 in OnConnected ./../../third\_party/webrtc/media/sctp/dcsctp\_transport.cc:507:25  

#4 0x55d4d95ac640 in non-virtual thunk to webrtc::DcSctpTransport::OnConnected() ./../../third\_party/webrtc/media/sctp/dcsctp\_transport.cc:0:0  

#5 0x55d4d95c8d2c in operator() ./../../third\_party/libc++/src/include/\_\_functional/function.h:854:16  

#6 0x55d4d95c8d2c in operator() ./../../third\_party/libc++/src/include/\_\_functional/function.h:1168:12  

#7 0x55d4d95c8d2c in dcsctp::CallbackDeferrer::TriggerDeferred() ./../../third\_party/webrtc/net/dcsctp/socket/callback\_deferrer.cc:56:5  

#8 0x55d4d95b77d9 in ~ScopedDeferrer ./../../third\_party/webrtc/net/dcsctp/socket/callback\_deferrer.h:53:44  

#9 0x55d4d95b77d9 in dcsctp::DcSctpSocket::ReceivePacket(rtc::ArrayView<unsigned char const, -4711l>) ./../../third\_party/webrtc/net/dcsctp/socket/dcsctp\_socket.cc:797:1  

#10 0x55d4d8559d9d in emit<rtc::PacketTransportInternal \*, const char \*, unsigned long, const long &, int> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#11 0x55d4d8559d9d in emit ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:566:12  

#12 0x55d4d8559d9d in operator() ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:570:35  

#13 0x55d4d8559d9d in cricket::DtlsTransport::OnDtlsEvent(rtc::StreamInterface\*, int, int) ./../../third\_party/webrtc/p2p/base/dtls\_transport.cc:706:9  

#14 0x55d4d84eae6f in emit<rtc::StreamInterface \*, int, int> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#15 0x55d4d84eae6f in emit ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:566:12  

#16 0x55d4d84eae6f in operator() ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:570:35  

#17 0x55d4d84eae6f in rtc::OpenSSLStreamAdapter::OnEvent(rtc::StreamInterface\*, int, int) ./../../third\_party/webrtc/rtc\_base/openssl\_stream\_adapter.cc:804:5  

#18 0x55d4d8553aef in emit<rtc::StreamInterface \*, int, int> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#19 0x55d4d8553aef in emit ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:566:12  

#20 0x55d4d8553aef in operator() ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:570:35  

#21 0x55d4d8553aef in cricket::StreamInterfaceChannel::OnPacketReceived(char const\*, unsigned long) ./../../third\_party/webrtc/p2p/base/dtls\_transport.cc:120:3  

#22 0x55d4d855d778 in HandleDtlsPacket ./../../third\_party/webrtc/p2p/base/dtls\_transport.cc:805:21  

#23 0x55d4d855d778 in cricket::DtlsTransport::OnReadPacket(rtc::PacketTransportInternal\*, char const\*, unsigned long, long const&, int) ./../../third\_party/webrtc/p2p/base/dtls\_transport.cc:635:14  

#24 0x55d4d856e2f9 in emit<rtc::PacketTransportInternal \*, const char \*, unsigned long, const long &, int> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#25 0x55d4d856e2f9 in emit ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:566:12  

#26 0x55d4d856e2f9 in operator() ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:570:35  

#27 0x55d4d856e2f9 in cricket::P2PTransportChannel::OnReadPacket(cricket::Connection\*, char const\*, unsigned long, long) ./../../third\_party/webrtc/p2p/base/p2p\_transport\_channel.cc:2217:5  

#28 0x55d4d8541122 in emit<cricket::Connection \*, const char \*, unsigned long, long> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#29 0x55d4d8541122 in emit ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:566:12  

#30 0x55d4d8541122 in operator() ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:570:35  

#31 0x55d4d8541122 in cricket::Connection::OnReadPacket(char const\*, unsigned long, long) ./../../third\_party/webrtc/p2p/base/connection.cc:459:5  

#32 0x55d4d85e6b01 in cricket::UDPPort::HandleIncomingPacket(rtc::AsyncPacketSocket\*, char const\*, unsigned long, rtc::SocketAddress const&, long) ./../../third\_party/webrtc/p2p/base/stun\_port.cc:352:3  

#33 0x55d4e8a8caf4 in emit<rtc::AsyncPacketSocket \*, const char \*, unsigned long, const rtc::SocketAddress &, const long &> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#34 0x55d4e8a8caf4 in emit ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h

**Additional Comments:**

\*\*Chrome version: \*\* 117.0.5911.2 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.9 KB)
- [test.sh](attachments/test.sh) (text/plain, 880 B)
- [uaf-asan.log](attachments/uaf-asan.log) (text/plain, 50.4 KB)
- [heap-buffer-overflow-asan.log](attachments/heap-buffer-overflow-asan.log) (text/plain, 33.3 KB)
- [poc2.html](attachments/poc2.html) (text/plain, 1.9 KB)
- [launcher2.sh](attachments/launcher2.sh) (text/plain, 2.4 KB)

## Timeline

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### bb...@google.com (2023-08-08)

Tenatively settting prio one as this appears superficially similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1454086 while I attempt to try to get in a state to reproduce


### bb...@google.com (2023-08-08)

I can  not reproduce this using MacOS 13.5 and  the latest asan build (asan-mac-release-1160319) 



### bb...@google.com (2023-08-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-08-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6015170708701184.

### cl...@chromium.org (2023-08-08)

Testcase 6015170708701184 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6015170708701184.

### em...@gmail.com (2023-08-09)

[Comment Deleted]

### em...@gmail.com (2023-08-09)

I have tested with asan-mac-release-1160319 (https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/mac-release%2Fasan-mac-release-1160319.zip?generation=1687304373998608&alt=media) multiple times. The issue can be easily reproduced using the "poc2.html" file. It takes around 60 seconds for the issue to repro.

Could you please try the "poc2.html" file provided in the attachment?

Reproduction steps:

- Open Terminal.
-   Navigate to the directory containing "Chromium.app."
-   Run the following command:
Chromium.app/Contents/MacOS/Chromium --incognito --user-data-dir=/tmp/xx --no-sandbox --password-store=basic --use-mock-keychain http://localhost:8000/poc2.html

### em...@gmail.com (2023-08-09)

[Empty comment from Monorail migration]

### bb...@google.com (2023-08-09)

Thanks for that.  reproduces very well with poc2.html

Assigning to @tommi as this appears similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1454086 - Please pass it off to someone more appropriate if I have guessed wrong. 

[Monorail components: Blink>WebRTC>DataChannel]

### [Deleted User] (2023-08-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2023-08-09)

orphis - can you take a look?

### th...@chromium.org (2023-08-15)

[secondary shepherd] orphis@, could you confirm you intend to take a look at this, or if not, could you help re-triage?

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### to...@chromium.org (2023-08-21)

I've been trying to get this to repro on Mac and Linux (asan enabled build) but am unable to.
Looking at the code, it seems to me that if we're somehow able to get into the bad state of an observer going out of scope before it's been unregistered from webrtc, then `RTCDataChannel::ContextDestroyed()` must not be getting called.

### gi...@appspot.gserviceaccount.com (2023-08-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5a2c8e29e79449120b87a267d47be82d611d66d

commit f5a2c8e29e79449120b87a267d47be82d611d66d
Author: Tommi <tommi@chromium.org>
Date: Mon Aug 21 13:09:38 2023

Add CHECKs to RTCDataChannel for proper tear down.

This upgrades an existing DCHECK to a CHECK and adds one more for
the embedded observer implementation.

Bug: 1470992
Change-Id: I3217675a68de98f147c0d6a2234f0335317c23fc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4797850
Reviewed-by: Florent Castelli <orphis@chromium.org>
Commit-Queue: Florent Castelli <orphis@chromium.org>
Auto-Submit: Tomas Gunnarsson <tommi@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1185820}

[modify] https://crrev.com/f5a2c8e29e79449120b87a267d47be82d611d66d/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h
[modify] https://crrev.com/f5a2c8e29e79449120b87a267d47be82d611d66d/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc


### em...@gmail.com (2023-08-21)

The above cl does not seem to fix this bug, and I can still reproduce UAF after patching.

tested version:
Chromium 118.0.5951.0 with patch

repro steps:
In my mac notebook, I can reproduce it stably in one browser, but in Linux, I need to open multiple browsers at the same time to reproduce (test.sh).


### to...@chromium.org (2023-08-22)

Thanks - I'm still not having much luck with reproing but one theory I have now is that a blocking call in webrtc doesn't execute (is dropped/ignored since the worker thread is terminating).

Re https://crbug.com/chromium/1470992#c19 - do you have your own build that you could use for trying a couple of changes out to see if that theory holds?

### em...@gmail.com (2023-08-22)

I can do that. I have my own build.

### to...@chromium.org (2023-08-22)

Here's a diff containing two added "RTC_CHECK" lines that I added to my local build (in the `third_party/webrtc` directory) to see if they'd trigger, but then again the problem isn't reproing for me.  Could you give this a try?

diff --git a/rtc_base/thread.cc b/rtc_base/thread.cc
index 6f101ac8f4..ded8ce662f 100644
--- a/rtc_base/thread.cc
+++ b/rtc_base/thread.cc
@@ -459,6 +459,7 @@ void Thread::PostTaskImpl(absl::AnyInvocable<void() &&> task,
                           const PostTaskTraits& traits,
                           const webrtc::Location& location) {
   if (IsQuitting()) {
+    RTC_CHECK(false) << "PostTaskImpl not succeeding";
     return;
   }
 
@@ -728,8 +729,10 @@ void Thread::BlockingCallImpl(rtc::FunctionView<void()> functor,
   TRACE_EVENT0("webrtc", "Thread::BlockingCall");
 
   RTC_DCHECK(!IsQuitting());
-  if (IsQuitting())
+  if (IsQuitting()) {
+    RTC_CHECK(false) << "Blocking call not succeeding";
     return;
+  }
 
   if (IsCurrent()) {
 #if RTC_DCHECK_IS_ON


### em...@gmail.com (2023-08-22)

UAF still repro after patching, and these two ""RTC_CHECK"s have not been triggered at all.

### pb...@google.com (2023-08-22)

[BULK EDIT] This issue marked as M117 Stable blocker and prevents the promotion of M117 to Stable. M117 is scheduled to get cut M117 Stable RC on Sep-05th please consider this as P) and  fix it asap and verify the fix. 

### [Deleted User] (2023-08-22)

orphis: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2023-08-24)

I'm taking a look

### gi...@appspot.gserviceaccount.com (2023-08-24)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/66bf3f472c3cbf3872b77ff15c2b02bd1b3d88db

commit 66bf3f472c3cbf3872b77ff15c2b02bd1b3d88db
Author: Tommi <tommi@webrtc.org>
Date: Thu Aug 24 13:29:10 2023

Make PendingTaskSafetyFlag compatible with component builds

Bug: chromium:1470992
Change-Id: I06cec9cda36c9de75b970eaf709f9ed3b9f466b4
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/317620
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#40618}

[modify] https://crrev.com/66bf3f472c3cbf3872b77ff15c2b02bd1b3d88db/api/task_queue/BUILD.gn
[modify] https://crrev.com/66bf3f472c3cbf3872b77ff15c2b02bd1b3d88db/api/task_queue/pending_task_safety_flag.h


### to...@chromium.org (2023-08-24)

Re https://crbug.com/chromium/1470992#c23 - thanks for checking. I'm trying out another thing now, trying to reproduce again (unsuccessfully), but would you be able to give this a try as well?

https://chromium-review.googlesource.com/c/chromium/src/+/4808164

### em...@gmail.com (2023-08-24)

It can still be reproduced after patching. I have applied the following 3 CLs. I shouldn't have missed a step, right?
1. https://webrtc-review.googlesource.com/c/src/+/317620
2. https://chromium-review.googlesource.com/c/chromium/src/+/4797850
3. https://chromium-review.googlesource.com/c/chromium/src/+/4808164

I found that opening more browsers under headless is very stable for repro.
Repro steps:
1 Modify the chrome path and poc path in the script.
2 ./launcher.sh 2>&1 |grep -E 'AddressSanitizer'
Wait for dozens of seconds and it will repro immediately


### em...@gmail.com (2023-08-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-08-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/addc4a3cef5bc1b8513a9a4fd1a61572fc2c9529

commit addc4a3cef5bc1b8513a9a4fd1a61572fc2c9529
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Aug 24 17:16:52 2023

Roll WebRTC from 43a5dd86c20d to 66bf3f472c3c (2 revisions)

https://webrtc.googlesource.com/src.git/+log/43a5dd86c20d..66bf3f472c3c

2023-08-24 tommi@webrtc.org Make PendingTaskSafetyFlag compatible with component builds
2023-08-24 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 9a6d0f811c..6dae2061c5 (1187201:1187756)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1470992
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I7db1036f96e78b30b47e693be6c3389a12caddd7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4810422
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1187906}

[modify] https://crrev.com/addc4a3cef5bc1b8513a9a4fd1a61572fc2c9529/DEPS
[modify] https://crrev.com/addc4a3cef5bc1b8513a9a4fd1a61572fc2c9529/third_party/webrtc


### to...@chromium.org (2023-08-24)

Thanks emilykim8708 - very helpful. I'm traveling right now with somewhat limited means to test but I believe I've found the issue. Would you mind trying this CL out?

https://webrtc-review.googlesource.com/c/src/+/317700

### em...@gmail.com (2023-08-25)

#32
I tested it for more than half an hour and did not repro this issue again.

### gi...@appspot.gserviceaccount.com (2023-08-25)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/70cea9bda8b8815be3c5bae4b6fa8053713efcac

commit 70cea9bda8b8815be3c5bae4b6fa8053713efcac
Author: Tommi <tommi@webrtc.org>
Date: Thu Aug 24 23:12:04 2023

[SctpDataChannel] Don't use PostTask for observer registration.

Instead, use BlockingCall to match with how unregistration is done.
This is needed because the ThreadWrapper implementation in Chromium, overriding the Thread implementation in WebRTC, does not order sent (blocking) tasks along with posted tasks.

That makes the functional difference that Thread1 posting and sending
tasks to Thread2, can not assume that the tasks run in the order they
were posted and sent. I.e. in this case:

  // Running on Thread1.
  thread2->PostTask([](){ Foo(); });
  thread2->BlockingCall([](){ Bar(); });

Thread2 may actually execute Bar() first, and then Foo().

Bug: chromium:1470992
Change-Id: I1f83f12ce39c09279c0f2b3bc71c3a33e2cb16c5
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/317700
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#40624}

[modify] https://crrev.com/70cea9bda8b8815be3c5bae4b6fa8053713efcac/pc/sctp_data_channel.cc


### gi...@appspot.gserviceaccount.com (2023-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/617e10a19c3cbe5367dfa6ecf474d83acec94d83

commit 617e10a19c3cbe5367dfa6ecf474d83acec94d83
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Aug 25 14:05:34 2023

Roll WebRTC from 0720e9ac1dd4 to 92fe5c4db3bf (3 revisions)

https://webrtc.googlesource.com/src.git/+log/0720e9ac1dd4..92fe5c4db3bf

2023-08-25 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 2c59b7b527..6aaff43ef6 (1188138:1188260)
2023-08-25 joachimr@meta.com Check use_rtx() in PeerConnectionFactory::GetRtpSenderCapabilities
2023-08-25 tommi@webrtc.org [SctpDataChannel] Don't use PostTask for observer registration.

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1470992
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: Id9aa46363c223e3a8751e1ba936270ee5f1c7e3d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4811774
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1188319}

[modify] https://crrev.com/617e10a19c3cbe5367dfa6ecf474d83acec94d83/DEPS
[modify] https://crrev.com/617e10a19c3cbe5367dfa6ecf474d83acec94d83/third_party/webrtc


### to...@chromium.org (2023-08-25)

Marking as fixed. Thanks a lot for the help emilykim8708@.

### [Deleted User] (2023-08-25)

Requesting merge to beta M117 because latest trunk commit (1188319) appears to be after beta branch point (1181205).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2023-08-25)

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://webrtc-review.googlesource.com/c/src/+/317700

2. Has this fix been tested on Canary?

Not yet. The next canary (26th of august or later) will contain the fix. The fix has been tested manually with local builds.

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

Yes. No functional regressions expected, stability will improve.

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes. Following the steps outlined in https://crbug.com/chromium/1470992#c8 (later comments also include improvements to those steps).

### [Deleted User] (2023-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-26)

Requesting merge to beta M117 because latest trunk commit (1188319) appears to be after beta branch point (1181205).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-27)

Requesting merge to beta M117 because latest trunk commit (1188319) appears to be after beta branch point (1181205).

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [117].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-08-28)

Merge approved for M117! please cherry pick the fix to branch 5938 by Tuesday EOD (MTV time) to get this into M117 beta!

### pg...@google.com (2023-08-30)

Sorry for the mistake next week's beta is the last release so the cut for stable will be earlier - please merge the fix by Thursday Aug 30 EOD (MTV time) to get this into M117 stable!

### gi...@appspot.gserviceaccount.com (2023-08-30)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/d95382fab7dcac8867d9811c4630367c4454cb7d

commit d95382fab7dcac8867d9811c4630367c4454cb7d
Author: Tommi <tommi@webrtc.org>
Date: Thu Aug 24 23:12:04 2023

[M117][SctpDataChannel] Don't use PostTask for observer registration.

Instead, use BlockingCall to match with how unregistration is done.
This is needed because the ThreadWrapper implementation in Chromium, overriding the Thread implementation in WebRTC, does not order sent (blocking) tasks along with posted tasks.

That makes the functional difference that Thread1 posting and sending
tasks to Thread2, can not assume that the tasks run in the order they
were posted and sent. I.e. in this case:

  // Running on Thread1.
  thread2->PostTask([](){ Foo(); });
  thread2->BlockingCall([](){ Bar(); });

Thread2 may actually execute Bar() first, and then Foo().

(cherry picked from commit 70cea9bda8b8815be3c5bae4b6fa8053713efcac)

No-Try: true
Bug: chromium:1470992
Change-Id: I1f83f12ce39c09279c0f2b3bc71c3a33e2cb16c5
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/317700
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Cr-Original-Commit-Position: refs/heads/main@{#40624}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/318360
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/5938@{#1}
Cr-Branched-From: 82e5f91a2bdf955aa870142008fbdc9ac12f6acd-refs/heads/main@{#40524}

[modify] https://crrev.com/d95382fab7dcac8867d9811c4630367c4454cb7d/pc/sctp_data_channel.cc


### pg...@google.com (2023-08-31)

setting OSes liberally - if any platform is certainly not impacted, please remove!

### [Deleted User] (2023-08-31)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2023-09-01)

Re https://crbug.com/chromium/1470992#c47:

1) No. I believe the issue has been around for longer.
2) No (same answer as for 1.)

Merging the fix for LTS makes sense to me.

### vo...@google.com (2023-09-05)

[Empty comment from Monorail migration]

### vo...@google.com (2023-09-05)

Change can't be applied to 114 (BlockingCall is already used there).

### am...@google.com (2023-09-07)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-07)

Congratulations Cassidy Kim! The VRP Panel has decided to award you $10,000 for this report! Thank you for your efforts from report to resolution on this issue -- excellent work! 

### am...@google.com (2023-09-09)

[Empty comment from Monorail migration]

### rz...@google.com (2023-09-12)

Changed code in the RegisterObserver doesn't exist in 108.

### [Deleted User] (2023-12-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1470992?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40069005)*
