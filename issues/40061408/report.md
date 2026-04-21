# UAF in network::WebTransport::TearDown

| Field | Value |
|-------|-------|
| **Issue ID** | [40061408](https://issues.chromium.org/issues/40061408) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>WebTransport |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | va...@chromium.org |
| **Created** | 2022-10-19 |
| **Bounty** | $16,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

macOS 12.6  

ubuntu 22.04

chrome version:  

106.0.5231.2  

Chromium 109.0.5368.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1060816.zip)  

UAF in network::WebTransport::TearDown  

repro steps:  

(1) generate test ssl key  

openssl genrsa 2048 > host.key  

chmod 400 host.key  

openssl req -new -x509 -nodes -sha256 -days 365 -key host.key -out host.cert

(2)generate fingerprint  

openssl x509 -pubkey < "host.cert" | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | base64 > "fingerprints.txt"

(3)install dependency  

pip3 install aioquic

(4)python3 ./webtransport\_server.py ./host.crt ./host.cert ./host.key

(5)  

./chrome --ignore-certificate-errors-spki-list=xx --origin-to-force-quic-on=localhost:4433 <http://localhost:8605/poc.html> --no-sandbox --no-zygote --incognito  

xx is the contents from fingerprints.txt. "--no-sandbox --no-zygote --incognito" These three flag are not necessary, just for the convenience of reproduction. It can be reproduced immediately without these parameters in macOS.But in linux, these flags need to be added to be able to repro stably.

**Problem Description:**  

==1079099==ERROR: AddressSanitizer: heap-use-after-free on address 0x6190001a8338 at pc 0x55a93f4ed887 bp 0x7fdc2a3be6b0 sp 0x7fdc2a3be6a8  

WRITE of size 1 at 0x6190001a8338 thread T4 (Chrome\_ChildIOT)  

#0 0x55a93f4ed886 in CancelWait ./../../mojo/public/cpp/bindings/lib/connector.cc:652:17  

#1 0x55a93f4ed886 in mojo::Connector::PassMessagePipe() ./../../mojo/public/cpp/bindings/lib/connector.cc:233:3  

#2 0x55a93f4ed470 in mojo::Connector::CloseMessagePipe() ./../../mojo/public/cpp/bindings/lib/connector.cc:227:3  

#3 0x55a93f51a5d2 in mojo::internal::MultiplexRouter::CloseMessagePipe() ./../../mojo/public/cpp/bindings/lib/multiplex\_router.cc:573:14  

#4 0x55a93f50d6d6 in mojo::internal::InterfacePtrStateBase::~InterfacePtrStateBase() ./../../mojo/public/cpp/bindings/lib/interface\_ptr\_state.cc:17:14  

#5 0x55a945094621 in ~InterfacePtrState ./../../mojo/public/cpp/bindings/lib/interface\_ptr\_state.h:140:32  

#6 0x55a945094621 in reset ./../../mojo/public/cpp/bindings/remote.h:216:3  

#7 0x55a945094621 in network::WebTransport::TearDown() ./../../services/network/web\_transport.cc:729:11  

#8 0x55a9450a3352 in net::DedicatedWebTransportHttp3Client::TransitionToState(net::WebTransportState) ./../../net/quic/dedicated\_web\_transport\_http3\_client.cc:0:17  

#9 0x55a9450ac233 in net::DedicatedWebTransportHttp3Client::OnConnectionClosed(quic::QuicErrorCode, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, quic::ConnectionCloseSource) ./../../net/quic/dedicated\_web\_transport\_http3\_client.cc:848:3  

#10 0x55a93fe9957f in quic::QuicConnection::TearDownLocalConnectionState(quic::QuicConnectionCloseFrame const&, quic::ConnectionCloseSource) ./../../net/third\_party/quiche/src/quiche/quic/core/quic\_connection.cc:4635:13  

#11 0x55a93fe8842b in quic::QuicConnection::TearDownLocalConnectionState(quic::QuicErrorCode, quic::QuicIetfTransportErrorCodes, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, quic::ConnectionCloseSource) ./../../net/third\_party/quiche/src/quiche/quic/core/quic\_connection.cc:4621:10  

#12 0x55a93ffef953 in quic::QuicControlFrameManager::WriteOrBufferQuicFrame(quic::QuicFrame) ./../../net/third\_party/quiche/src/quiche/quic/core/quic\_control\_frame\_manager.cc:49:16  

#13 0x55a93fff0181 in quic::QuicControlFrameManager::WriteOrBufferRstStream(unsigned int, quic::QuicResetStreamError, unsigned long) ./../../net/third\_party/quiche/src/quiche/quic/core/quic\_control\_frame\_manager.cc:66:3  

#14 0x55a93ffcd6d9 in quic::QuicSession::MaybeSendRstStreamFrame(unsigned int, quic::QuicResetStreamError, unsigned long) ./../../net/third\_party/quiche/src/quiche/quic/core/quic\_session.cc:892:28  

#15 0x55a93ffffe71 in quic::QuicStream::MaybeSendRstStream(quic::QuicResetStreamError) ./../../net/third\_party/quiche/src/quiche/quic/core/quic\_stream.cc:896:14  

#16 0x55a940001971 in quic::QuicStream::ResetWithError(quic::QuicResetStreamError) ./../../net/third\_party/quiche/src/quiche/quic/core/quic\_stream.cc:602:3  

#17 0x55a94509b5cf in network::WebTransport::Stream::~Stream() ./../../services/network/web\_transport.cc:183:13  

#18 0x55a9450982f5 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#19 0x55a9450982f5 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#20 0x55a9450982f5 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#21 0x55a9450982f5 in ~pair ./../../buildtools/third\_party/libc++/trunk/include/\_\_utility/pair.h:46:29  

#22 0x55a9450982f5 in \_\_destroy\_at<std::Cr::pair<const unsigned int, std::Cr::unique\_ptr<network::WebTransport::Stream, std::Cr::default\_delete[network::WebTransport::Stream](javascript:void(0);) > >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:64:13  

#23 0x55a9450982f5 in destroy\_at<std::Cr::pair<const unsigned int, std::Cr::unique\_ptr<network::WebTransport::Stream, std::Cr::default\_delete[network::WebTransport::Stream](javascript:void(0);) > >, 0> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/construct\_at.h:89:5  

#24 0x55a9450982f5 in destroy<std::Cr::pair<const unsigned int, std::Cr::unique\_ptr<network::WebTransport::Stream, std::Cr::default\_delete[network::WebTransport::Stream](javascript:void(0);) > >, void, void> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/allocator\_traits.h:315:9  

#25 0x55a9450982f5 in std::Cr::\_\_tree<std::Cr::\_\_value\_type<unsigned int, std::Cr::unique\_ptr<network::WebTransport::Stream, std::Cr::default\_delete[network::WebTransport::Stream](javascript:void(0);)>>, std::Cr::\_\_map\_value\_compare<unsigned int, std::Cr::\_\_value\_type<unsigned int, std::Cr::unique\_ptr<network::WebTransport::Stream, std::Cr::default\_delete[network::WebTransport::Stream](javascript:void(0);)>>, std::Cr::less<unsigned int>, true>, std::Cr::allocator<std::Cr::\_\_value\_type<unsigned int, std::Cr::unique\_ptr<network::WebTransport::Stream, std::Cr::default\_delete<network::WebT

**Additional Comments:**

\*\*Chrome version: \*\* 106.0.5231.2 \*\*Channel: \*\* Stable

**OS:** Mac OS

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 435 B)
- [webtransport_server.py](attachments/webtransport_server.py) (text/plain, 9.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 68.3 KB)

## Timeline

### [Deleted User] (2022-10-19)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-10-20)

Thanks for the report! Looks like yhirano@ wrote the code in question but they're no longer active. +some other folks to take a look.

[Monorail components: Blink>Network>WebTransport]

### [Deleted User] (2022-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-20)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-20)

[Empty comment from Monorail migration]

### ri...@chromium.org (2022-10-24)

The PoC calls network::WebTransport::CreateStream() in a loop and then at some random time calls network::WebTransport::Stream::MayDisposeLater(), and calls network::WebTransport::Dispose(). Because of mojo those calls may happen in an arbitrary order.

### ri...@chromium.org (2022-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-08)

ricea: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2022-11-12)

Friendly ping，is there any update？

### ri...@chromium.org (2022-11-14)

Sorry, I haven't found the root cause yet.

### [Deleted User] (2022-11-28)

ricea: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ri...@chromium.org (2022-11-29)

Sorry, I dropped the ball a bit on this. I will get on it.

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-12-07)

[security marshal] Friendly ping. ricea@ any update on finding the root cause?

### ri...@chromium.org (2022-12-13)

I'm currently waiting to see if https://chromium-review.googlesource.com/c/chromium/src/+/4085132 fixes it.

### em...@gmail.com (2022-12-14)

I tested with the above cl and still reproduce uaf.
I am not very familiar with the web_transport module, please correct me if the analysis is wrong.
(1)When ｜WebTransport｜is destroying,in the destructor of |Stream|, stream->MaybeResetDueToStreamObjectGone[0] may eventually call the reset()[1] function of the freed |client_| object.
The call chain as follow:
    #7 0x56125bb20d55 in network::WebTransport::TearDown() ./../../services/network/web_transport.cc:735:11
    ...
    #13 0x561256891b13 in quic::QuicControlFrameManager::WriteOrBufferQuicFrame(quic::QuicFrame) ./../../net/third_party/quiche/src/quiche/quic/core/quic_control_frame_manager.cc:49:16
    #14 0x561256892341 in quic::QuicControlFrameManager::WriteOrBufferRstStream(unsigned int, quic::QuicResetStreamError, unsigned long) ./../../net/third_party/quiche/src/quiche/quic/core/quic_control_frame_manager.cc:66:3
    #15 0x561256872829 in quic::QuicSession::MaybeSendRstStreamFrame(unsigned int, quic::QuicResetStreamError, unsigned long) ./../../net/third_party/quiche/src/quiche/quic/core/quic_session.cc:919:28
    #16 0x5612568a14a1 in quic::QuicStream::MaybeSendRstStream(quic::QuicResetStreamError) ./../../net/third_party/quiche/src/quiche/quic/core/quic_stream.cc:888:14
    ...
    #18 0x56125bb2860f in network::WebTransport::Stream::~Stream() ./../../services/network/web_transport.cc:183:13

(2)It is relatively difficult to reproduce uaf with the default startup flags, you need to use the '--no-sandbox' and '--no-zygote'.
Mainly because |control_frames_.size| in WriteOrBufferQuicFrame(#13) function is difficult to exceed |HasBufferedFrames|(1000), but it is easy to meet this condition after using '--no-sandbox' and '--no-zygote'.
void QuicControlFrameManager::WriteOrBufferQuicFrame(QuicFrame frame) {
  const bool had_buffered_frames = HasBufferedFrames();
  control_frames_.emplace_back(frame);
  if (control_frames_.size() > kMaxNumControlFrames) {     ------[2]
    delegate_->OnControlFrameManagerError(  
        QUIC_TOO_MANY_BUFFERED_CONTROL_FRAMES,
        absl::StrCat("More than ", kMaxNumControlFrames,
                     "buffered control frames, least_unacked: ", least_unacked_,
                     ", least_unsent_: ", least_unsent_));
    return;
  }
  if (had_buffered_frames) {
    return;
  }
  WriteBufferedFrames();
}
https://source.chromium.org/chromium/chromium/src/+/main:net/third_party/quiche/src/quiche/quic/core/quic_control_frame_manager.cc;drc=697e7e0df4f2d9bc7189c1358100705662e4c4ef;l=48

~Stream() {
    auto* stream = incoming_ ? incoming_.get() : outgoing_.get();
    if (!stream) {
      return;
    }
    stream->MaybeResetDueToStreamObjectGone();  ----->[0]
  }
https://source.chromium.org/chromium/chromium/src/+/main:services/network/web_transport.cc;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29;l=178

void WebTransport::TearDown() {
  torn_down_ = true;
  receiver_.reset();                           
  handshake_client_.reset();     
  client_.reset();                       ------->[1]client_ has been freed at ~WebTransport(),so trigger uaf here.

  base::SequencedTaskRunner::GetCurrentDefault()->PostTask(
      FROM_HERE,
      base::BindOnce(&WebTransport::Dispose, weak_factory_.GetWeakPtr()));
}
https://source.chromium.org/chromium/chromium/src/+/main:services/network/web_transport.cc;drc=38321ee39cd73ac2d9d4400c56b90613dee5fe29;l=728

fix suggestion:
I thought of two fix ideas.
(1)The first one is to set the destructing flag in the WebTransport destructor and check the flag in the Stream destructor.
diff --git a/services/network/web_transport.h b/services/network/web_transport.h
index 8f62b027aa082..f791879c8fe9d 100644
--- a/services/network/web_transport.h
+++ b/services/network/web_transport.h
@@ -108,7 +108,7 @@ class COMPONENT_EXPORT(NETWORK_SERVICE) WebTransport final

   bool closing_ = false;
   bool torn_down_ = false;

+  bool destructing_ = false;
   // This must be the last member.
   base::WeakPtrFactory<WebTransport> weak_factory_{this};
 };
   diff --git a/services/network/web_transport.cc b/services/network/web_transport.cc
index 2c5f739691e9c..b647b50b70df3 100644
--- a/services/network/web_transport.cc
+++ b/services/network/web_transport.cc
@@ -177,10 +177,15 @@ class WebTransport::Stream final {

   ~Stream() {
     auto* stream = incoming_ ? incoming_.get() : outgoing_.get();
     if (!stream) {
       return;
     }
+    if(!transport_->destructing_){
     stream->MaybeResetDueToStreamObjectGone();
+    }
+
   }
   
(2)The second is to check whether client_ is valid directly in the Stream destructor.
diff --git a/services/network/web_transport.cc b/services/network/web_transport.cc
index 2c5f739691e9c..023a6a91cb59b 100644
--- a/services/network/web_transport.cc
+++ b/services/network/web_transport.cc
@@ -177,10 +177,16 @@ class WebTransport::Stream final {

   ~Stream() {
     auto* stream = incoming_ ? incoming_.get() : outgoing_.get();
     if (!stream) {
       return;
     }
+    if(transport_->client_){
     stream->MaybeResetDueToStreamObjectGone();
+    }
+
   }
I hope my analysis can provide some help in solving the issue,thanks






### em...@gmail.com (2022-12-14)

Sorry I missed some patch code for(1)
diff --git a/services/network/web_transport.cc b/services/network/web_transport.cc
index 2c5f739691e9c..a3cc0a0d4a8fb 100644
--- a/services/network/web_transport.cc
+++ b/services/network/web_transport.cc
-WebTransport::~WebTransport() = default;
-
+//WebTransport::~WebTransport() = default;
+WebTransport::~WebTransport() {
+  destructing_ = true;
+}

### ri...@chromium.org (2022-12-15)

#17 Thank you for your superb repro work and suggested fixes.

+vasilvv Sorry to send this back to you, but I am going to be gone until January. Can you take a look?

### [Deleted User] (2022-12-18)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### va...@chromium.org (2022-12-21)

Made a CL to address this: https://chromium-review.googlesource.com/c/chromium/src/+/4117501

In order to trigger this bug, two conditions have to be met:
(1) The WebTransport object is closed via a peer Mojo pipe going away, not via normal QUIC closure (plausible, and is achieved in repro by reloading the page).
(2) The transport has to have multiple open streams. When the transport is closed, it attempts to reset all of the unclosed streams in the destructor. If any of those trigger a connection error (in the repro case, that is caused by resetting more than 1000 streams and causing the reset buffer to fill up), that connection error causes a WebTransport-under-destruction to be closed again, which involves calling reset() on some Mojo fields that are no longer valid.

The CL fixes this both by always masking out all callbacks once the destructor is called (something we already do for normal closure), and by not sending resets in the middle of the destructor.

Adding ericorth@ for context as a potential reviewer who's currently not OOO.

### gi...@appspot.gserviceaccount.com (2022-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/57c54ae221d60e9f9394d7ee69634d66c9cd26f3

commit 57c54ae221d60e9f9394d7ee69634d66c9cd26f3
Author: Victor Vasiliev <vasilvv@chromium.org>
Date: Wed Dec 21 17:26:42 2022

Ensure clean destruction of network::WebTransport

Once the destruction of the object begins, we should not process any
callbacks, nor should we attempt to reset the streams on a connection
that is already being closed.

Bug: 1376354
Change-Id: Ib49e0ce0b177062cccd0e52368782e291cf8166c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4117501
Reviewed-by: Eric Orth <ericorth@chromium.org>
Commit-Queue: Victor Vasiliev <vasilvv@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1085965}

[modify] https://crrev.com/57c54ae221d60e9f9394d7ee69634d66c9cd26f3/services/network/web_transport.cc
[modify] https://crrev.com/57c54ae221d60e9f9394d7ee69634d66c9cd26f3/services/network/web_transport_unittest.cc


### ri...@chromium.org (2023-01-05)

Fixed?

### va...@chromium.org (2023-01-05)

Yes, though still probably needs verifiction.

### em...@gmail.com (2023-01-05)

After the patch, I never reproduced uaf again.

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-05)

Requesting merge to stable M108 because latest trunk commit (1085965) appears to be after stable branch point (1058933).

Requesting merge to beta M109 because latest trunk commit (1085965) appears to be after beta branch point (1070088).

Requesting merge to dev M110 because latest trunk commit (1085965) appears to be after dev branch point (1084008).

Merge approved: your change passed merge requirements and is auto-approved for M110. Please go ahead and merge the CL to branch 5481 (refs/branch-heads/5481) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

Merge review required: M108 is already shipping to stable.

Merge review required: M109 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [108, 109].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-05)

This fix has been on canary for over two weeks, unless there are any potential risks of backmerging that are not apparent, please backmerge this fix immediately to branch 5414 so this fix can be included in a recut of Stable RC for M109. 

Also, please backmerge to branch 5359 so this fix can be included in M108/Extended. 

### ma...@google.com (2023-01-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/67447fd1618bb99e54a4fbc936a60253f72a898b

commit 67447fd1618bb99e54a4fbc936a60253f72a898b
Author: Victor Vasiliev <vasilvv@chromium.org>
Date: Fri Jan 06 00:03:48 2023

Ensure clean destruction of network::WebTransport

Once the destruction of the object begins, we should not process any
callbacks, nor should we attempt to reset the streams on a connection
that is already being closed.

(cherry picked from commit 57c54ae221d60e9f9394d7ee69634d66c9cd26f3)

Bug: 1376354
Change-Id: Ib49e0ce0b177062cccd0e52368782e291cf8166c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4117501
Reviewed-by: Eric Orth <ericorth@chromium.org>
Commit-Queue: Victor Vasiliev <vasilvv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1085965}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4139958
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#147}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/67447fd1618bb99e54a4fbc936a60253f72a898b/services/network/web_transport.cc
[modify] https://crrev.com/67447fd1618bb99e54a4fbc936a60253f72a898b/services/network/web_transport_unittest.cc


### [Deleted User] (2023-01-06)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### rz...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-01-06)

1. https://crrev.com/c/4143058
2. Low, no conflicts
3. 110
4. Yes

### am...@chromium.org (2023-01-11)

M109/Stable and M108/Extended have been release so we are out of the window of a potential recut; please merge this fix to branch 5414 and branch 5359 so this fix can be included in the next Stable and Extended Stable security updates. TY. 

### gm...@google.com (2023-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-12)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1f8e86d2cc9214b7ac67140f5ff58a7829f4dc6e

commit 1f8e86d2cc9214b7ac67140f5ff58a7829f4dc6e
Author: Victor Vasiliev <vasilvv@chromium.org>
Date: Thu Jan 12 21:47:37 2023

Ensure clean destruction of network::WebTransport

Once the destruction of the object begins, we should not process any
callbacks, nor should we attempt to reset the streams on a connection
that is already being closed.

(cherry picked from commit 57c54ae221d60e9f9394d7ee69634d66c9cd26f3)

Bug: 1376354
Change-Id: Ib49e0ce0b177062cccd0e52368782e291cf8166c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4117501
Reviewed-by: Eric Orth <ericorth@chromium.org>
Commit-Queue: Victor Vasiliev <vasilvv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1085965}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4139980
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#1353}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/1f8e86d2cc9214b7ac67140f5ff58a7829f4dc6e/services/network/web_transport.cc
[modify] https://crrev.com/1f8e86d2cc9214b7ac67140f5ff58a7829f4dc6e/services/network/web_transport_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e545559df5387c7cc1e13c4070153d1d402ccc66

commit e545559df5387c7cc1e13c4070153d1d402ccc66
Author: Victor Vasiliev <vasilvv@chromium.org>
Date: Thu Jan 12 22:03:48 2023

Ensure clean destruction of network::WebTransport

Once the destruction of the object begins, we should not process any
callbacks, nor should we attempt to reset the streams on a connection
that is already being closed.

(cherry picked from commit 57c54ae221d60e9f9394d7ee69634d66c9cd26f3)

Bug: 1376354
Change-Id: Ib49e0ce0b177062cccd0e52368782e291cf8166c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4117501
Reviewed-by: Eric Orth <ericorth@chromium.org>
Commit-Queue: Victor Vasiliev <vasilvv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1085965}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4139783
Reviewed-by: Kenichi Ishibashi <bashi@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1326}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/e545559df5387c7cc1e13c4070153d1d402ccc66/services/network/web_transport.cc
[modify] https://crrev.com/e545559df5387c7cc1e13c4070153d1d402ccc66/services/network/web_transport_unittest.cc


### am...@google.com (2023-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-12)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $16,000 for this report, including a patch bonus. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### em...@gmail.com (2023-01-13)

Thank you!~
And please credit to  chichoo Kim(chichoo) and Cassidy Kim(@cassidy6564) for this issue.

### am...@google.com (2023-01-14)

[Empty comment from Monorail migration]

### gm...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-24)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ec0c63c3f55ae84663a73ec9cf20effa3f4cd6f2

commit ec0c63c3f55ae84663a73ec9cf20effa3f4cd6f2
Author: Victor Vasiliev <vasilvv@chromium.org>
Date: Wed Jan 25 09:45:20 2023

[M102-LTS] Ensure clean destruction of network::WebTransport

Once the destruction of the object begins, we should not process any
callbacks, nor should we attempt to reset the streams on a connection
that is already being closed.

(cherry picked from commit 57c54ae221d60e9f9394d7ee69634d66c9cd26f3)

Bug: 1376354
Change-Id: Ib49e0ce0b177062cccd0e52368782e291cf8166c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4117501
Commit-Queue: Victor Vasiliev <vasilvv@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1085965}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4143058
Reviewed-by: Victor Vasiliev <vasilvv@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1424}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/ec0c63c3f55ae84663a73ec9cf20effa3f4cd6f2/services/network/web_transport.cc
[modify] https://crrev.com/ec0c63c3f55ae84663a73ec9cf20effa3f4cd6f2/services/network/web_transport_unittest.cc


### rz...@google.com (2023-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1376354?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061408)*
