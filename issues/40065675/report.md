# UAF in  webrtc::DataChannelController::OnChannelStateChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [40065675](https://issues.chromium.org/issues/40065675) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>DataChannel |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2023-06-12 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

os version:

- ubuntu 22.04
- MacOS Ventura 13.4  
  
  chromium version:  
  
  Chromium 116.0.5817.0  
  
  Chromium 115.0.5773.4

repro steps:  

1. python3 -m http.server 8000 --dir=|path|  

2. ./chrome --incognito --user-data-dir=/tmp/aa1 <http://localhost:8000/poc.html>  

3. UAF will repro after waiting tens of seconds.

# **Problem Description:** [2578801:2579239:0612/215624.466605:ERROR:sctp\_data\_channel.cc(718)] Queued received data exceeds the max buffer size.

==2578801==ERROR: AddressSanitizer: heap-use-after-free on address 0x51400011465c at pc 0x557e33ec0440 bp 0x7f84aff409b0 sp 0x7f84aff409a8  

READ of size 4 at 0x51400011465c thread T11 (WebRTC\_W\_and\_N)  

#0 0x557e33ec043f in internal\_id ./../../third\_party/webrtc/pc/sctp\_data\_channel.h:216:36  

#1 0x557e33ec043f in webrtc::DataChannelController::OnChannelStateChanged(webrtc::SctpDataChannel\*, webrtc::DataChannelInterface::DataState) ./../../third\_party/webrtc/pc/data\_channel\_controller.cc:80:62  

#2 0x557e47a60183 in webrtc::SctpDataChannel::OnDataReceived(webrtc::DataMessageType, rtc::CopyOnWriteBuffer const&) ./../../third\_party/webrtc/pc/sctp\_data\_channel.cc:721:7  

#3 0x557e4790271d in webrtc::DcSctpTransport::OnMessageReceived(dcsctp::DcSctpMessage) ./../../third\_party/webrtc/media/sctp/dcsctp\_transport.cc:462:25  

#4 0x557e479266e7 in Deliver ./../../third\_party/webrtc/net/dcsctp/socket/callback\_deferrer.cc:27:7  

#5 0x557e479266e7 in operator() ./../../third\_party/webrtc/net/dcsctp/socket/callback\_deferrer.cc:86:58  

#6 0x557e479266e7 in \_\_invoke<(lambda at ../../third\_party/webrtc/net/dcsctp/socket/callback\_deferrer.cc:85:7) &, dcsctp::DcSctpSocketCallbacks &> ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/invoke.h:394:23  

#7 0x557e479266e7 in \_\_call<(lambda at ../../third\_party/webrtc/net/dcsctp/socket/callback\_deferrer.cc:85:7) &, dcsctp::DcSctpSocketCallbacks &> ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/invoke.h:487:9  

#8 0x557e479266e7 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:235:12  

#9 0x557e479266e7 in void std::\_\_Cr::\_\_function::\_\_policy\_invoker<void (dcsctp::DcSctpSocketCallbacks&)>::\_\_call\_impl<std::\_\_Cr::\_\_function::\_\_default\_alloc\_func<dcsctp::CallbackDeferrer::OnMessageReceived(dcsctp::DcSctpMessage)::$\_0, void (dcsctp::DcSctpSocketCallbacks&)>>(std::\_\_Cr::\_\_function::\_\_policy\_storage const\*, dcsctp::DcSctpSocketCallbacks&) ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:719:16  

#10 0x557e4791fdab in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:850:16  

#11 0x557e4791fdab in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_functional/function.h:1162:12  

#12 0x557e4791fdab in dcsctp::CallbackDeferrer::TriggerDeferred() ./../../third\_party/webrtc/net/dcsctp/socket/callback\_deferrer.cc:56:5  

#13 0x557e4790f29c in ~ScopedDeferrer ./../../third\_party/webrtc/net/dcsctp/socket/callback\_deferrer.h:53:44  

#14 0x557e4790f29c in dcsctp::DcSctpSocket::ReceivePacket(rtc::ArrayView<unsigned char const, -4711l>) ./../../third\_party/webrtc/net/dcsctp/socket/dcsctp\_socket.cc:797:1  

#15 0x557e468c45bd in emit<rtc::PacketTransportInternal \*, const char \*, unsigned long, const long &, int> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#16 0x557e468c45bd in emit ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:566:12  

#17 0x557e468c45bd in operator() ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:570:35  

#18 0x557e468c45bd in cricket::DtlsTransport::OnDtlsEvent(rtc::StreamInterface\*, int, int) ./../../third\_party/webrtc/p2p/base/dtls\_transport.cc:706:9  

#19 0x557e468564ff in emit<rtc::StreamInterface \*, int, int> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#20 0x557e468564ff in emit ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:566:12  

#21 0x557e468564ff in operator() ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:570:35  

#22 0x557e468564ff in rtc::OpenSSLStreamAdapter::OnEvent(rtc::StreamInterface\*, int, int) ./../../third\_party/webrtc/rtc\_base/openssl\_stream\_adapter.cc:804:5  

#23 0x557e468be4af in emit<rtc::StreamInterface \*, int, int> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#24 0x557e468be4af in emit ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:566:12  

#25 0x557e468be4af in operator() ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:570:35  

#26 0x557e468be4af in cricket::StreamInterfaceChannel::OnPacketReceived(char const\*, unsigned long) ./../../third\_party/webrtc/p2p/base/dtls\_transport.cc:120:3  

#27 0x557e468c7f98 in HandleDtlsPacket ./../../third\_party/webrtc/p2p/base/dtls\_transport.cc:805:21  

#28 0x557e468c7f98 in cricket::DtlsTransport::OnReadPacket(rtc::PacketTransportInternal\*, char const\*, unsigned long, long const&, int) ./../../third\_party/webrtc/p2p/base/dtls\_transport.cc:635:14  

#29 0x557e468d8a79 in emit<rtc::PacketTransportInternal \*, const char \*, unsigned long, const long &, int> ./../../third\_party/webrtc/rtc\_base/third\_party/sigslot/sigslot.h:331:5  

#30

**Additional Comments:**

\*\*Chrome version: \*\* 115.0.5773.4 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 79.1 KB)
- [poc3.html](attachments/poc3.html) (text/plain, 1.5 KB)

## Timeline

### [Deleted User] (2023-06-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-06-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5599265127333888.

### cl...@chromium.org (2023-06-14)

ClusterFuzz testcase 5599265127333888 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-06-14)

Detailed Report: https://clusterfuzz.com/testcase?key=5599265127333888

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  r. Sending zygote magic failed: Broken pipe (32) in zygote_linux.cc
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1156149

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5599265127333888

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### em...@gmail.com (2023-06-14)

I'm unsure why CF (ClusterFuzz) is unable to reproduce it, but it is easily reproducible through manual testing. Based on the ASan logs, it appears to be related to these two commits. Therefore, it would be helpful to assign it to a colleague from the WebRTC team（tommi@webrtc.org） , for further investigation. Thanks.

https://source.chromium.org/chromium/_/webrtc/src.git/+/add7ac0dedebef70cc4d3c421122e7d1fe05a84f
https://source.chromium.org/chromium/_/webrtc/src.git/+/b00d63c88ba247f54e404d9ba973edea7d0db5bd

### bo...@google.com (2023-06-14)

@emilykim, is the local stun server required to trigger the crash? If so, that would explain why ClusterFuzz couldn't repro. 

CCing @tommi & @deadbeef for visibility while I try a little harder to manually repro because this seems a) likely to be a valid report that b) we may struggle to repro without a WebRTC-specific debug environment that you both probably already have, but I lack. 

[Monorail components: Blink>WebRTC>DataChannel]

### em...@gmail.com (2023-06-14)

[Comment Deleted]

### em...@gmail.com (2023-06-14)

Actually, there is no need to set up a local STUN server.
I have uploaded a new POC, can you try this again?
Thanks.

### bo...@google.com (2023-06-14)

Thanks! I was able to reproduce on x64 Linux using an Asan build from tip of tree. 

Setting severity High due to memory corruption in the sandboxed renderer process and routing to owners. 

I need to set FoundIn, but I have to step away from my desk briefly and I'll do that first thing upon returning. 

### bo...@google.com (2023-06-14)

Repro'ed on extended so setting FoundIn-114

### [Deleted User] (2023-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2023-06-20)

Taking a look

### gi...@appspot.gserviceaccount.com (2023-06-22)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/eec1810760ccbdf95c68ed0d2c2ae10a8575551a

commit eec1810760ccbdf95c68ed0d2c2ae10a8575551a
Author: Tommi <tommi@webrtc.org>
Date: Thu Jun 22 08:13:52 2023

Avoid touching channel after OnSctpDataChannelClosed

Bug: chromium:1454086
Change-Id: I39573b706c4031d091c45a182b13cb3b2dba6233
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/309920
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Cr-Commit-Position: refs/heads/main@{#40332}

[modify] https://crrev.com/eec1810760ccbdf95c68ed0d2c2ae10a8575551a/pc/data_channel_controller.cc


### gi...@appspot.gserviceaccount.com (2023-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/944a456b12107e7fda381c895d5ddebbd1245700

commit 944a456b12107e7fda381c895d5ddebbd1245700
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jun 22 12:05:48 2023

Roll WebRTC from c3a74024bf4d to eec1810760cc (2 revisions)

https://webrtc.googlesource.com/src.git/+log/c3a74024bf4d..eec1810760cc

2023-06-22 tommi@webrtc.org Avoid touching channel after OnSctpDataChannelClosed
2023-06-22 webrtc-version-updater@webrtc-ci.iam.gserviceaccount.com Update WebRTC code version (2023-06-22T04:01:55).

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

Bug: chromium:1454086
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I4d46715be809668cfed3f42c3389e565fb69ef1d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4636176
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1161140}

[modify] https://crrev.com/944a456b12107e7fda381c895d5ddebbd1245700/DEPS


### to...@chromium.org (2023-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-23)

Requesting merge to stable M114 because latest trunk commit (1161140) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1161140) appears to be after beta branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1161140) appears to be after dev branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-24)

Requesting merge to stable M114 because latest trunk commit (1161140) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1161140) appears to be after beta branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1161140) appears to be after dev branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-25)

Requesting merge to stable M114 because latest trunk commit (1161140) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1161140) appears to be after beta branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1161140) appears to be after dev branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2023-06-25)

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://webrtc-review.googlesource.com/c/src/+/309920

2. Has this fix been tested on Canary?

Yes

3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

Yes, the fix doesn't change any functionality. It moves a read operation prior to the point of where an object was getting deleted in a particular situation, thus addressing the UAF issue and not introducing additional complexity.

4. Does this fix pose any known compatibility risks?

No

5. Does it require manual verification by the test team? If so, please describe required testing.

Yes, please. For verification I've used the test files provided in https://crbug.com/chromium/1454086#c8 and the original report.

### [Deleted User] (2023-06-26)

Requesting merge to stable M114 because latest trunk commit (1161140) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1161140) appears to be after beta branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1161140) appears to be after dev branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2023-06-26)

1.  https://webrtc-review.googlesource.com/c/src/+/309920
2. Yes
3. Yes, the fix doesn't change any functionality. It moves a read operation prior to the point of where an object was getting deleted in a particular situation, thus addressing the UAF issue and not introducing additional complexity.
4. No
5. Yes, please. For verification I've used the test files provided in https://crbug.com/chromium/1454086#c8 and the original report.



### [Deleted User] (2023-06-27)

Requesting merge to stable M114 because latest trunk commit (1161140) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1161140) appears to be after beta branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1161140) appears to be after dev branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2023-06-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-27)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us --nice work! 

### [Deleted User] (2023-06-28)

Requesting merge to stable M114 because latest trunk commit (1161140) appears to be after stable branch point (1135570).

Requesting merge to beta M115 because latest trunk commit (1161140) appears to be after beta branch point (1148114).

Requesting merge to dev M116 because latest trunk commit (1161140) appears to be after dev branch point (1160321).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [114, 115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-06-28)

all merges approved for https://webrtc-review.googlesource.com/c/src/+/309920
Please merge this fix to M116/branch 5845, M115/ branch 5790, and M114 / branch 5735 at your earliest convenience. 
Please merge to M116 at soonest so this can go out in the next M116 before release freeze on Friday. 



### gi...@appspot.gserviceaccount.com (2023-06-29)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/ebf9a1faf81f30f9fb6d1a9390545e562c62ec06

commit ebf9a1faf81f30f9fb6d1a9390545e562c62ec06
Author: Tommi <tommi@webrtc.org>
Date: Thu Jun 22 08:13:52 2023

[M116] Avoid touching channel after OnSctpDataChannelClosed

(cherry picked from commit eec1810760ccbdf95c68ed0d2c2ae10a8575551a)

Bug: chromium:1454086
Change-Id: I39573b706c4031d091c45a182b13cb3b2dba6233
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/309920
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Cr-Original-Commit-Position: refs/heads/main@{#40332}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/310920
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/5845@{#1}
Cr-Branched-From: f80cf814353d11a9f22bef5ce5e8868f2c72f0d0-refs/heads/main@{#40319}

[modify] https://crrev.com/ebf9a1faf81f30f9fb6d1a9390545e562c62ec06/pc/data_channel_controller.cc


### gi...@appspot.gserviceaccount.com (2023-06-29)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/43670de877297a980bfdd1353dd2eb68360e2f2a

commit 43670de877297a980bfdd1353dd2eb68360e2f2a
Author: Tommi <tommi@webrtc.org>
Date: Thu Jun 22 08:13:52 2023

[M115] Avoid touching channel after OnSctpDataChannelClosed

(cherry picked from commit eec1810760ccbdf95c68ed0d2c2ae10a8575551a)

Bug: chromium:1454086
Change-Id: I39573b706c4031d091c45a182b13cb3b2dba6233
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/309920
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Cr-Original-Commit-Position: refs/heads/main@{#40332}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/310921
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/5790@{#6}
Cr-Branched-From: 2eacbbc03a4a41ea658661225eb1c8fc07884c33-refs/heads/main@{#40122}

[modify] https://crrev.com/43670de877297a980bfdd1353dd2eb68360e2f2a/pc/data_channel_controller.cc


### gi...@appspot.gserviceaccount.com (2023-06-29)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/a624ee1be7a11e795a849edb2a27dc1137d2b63d

commit a624ee1be7a11e795a849edb2a27dc1137d2b63d
Author: Tommi <tommi@webrtc.org>
Date: Thu Jun 22 08:13:52 2023

[M114] Avoid touching channel after OnSctpDataChannelClosed

(cherry picked from commit eec1810760ccbdf95c68ed0d2c2ae10a8575551a)

Bug: chromium:1454086
Change-Id: I39573b706c4031d091c45a182b13cb3b2dba6233
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/309920
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Tomas Gunnarsson <tommi@webrtc.org>
Cr-Original-Commit-Position: refs/heads/main@{#40332}
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/310922
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/5735@{#5}
Cr-Branched-From: df7df199abd619e75b9f1d9a7e12fc3f3f748775-refs/heads/main@{#39949}

[modify] https://crrev.com/a624ee1be7a11e795a849edb2a27dc1137d2b63d/pc/data_channel_controller.cc


### am...@google.com (2023-06-29)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1454086?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065675)*
