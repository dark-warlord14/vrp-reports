# UAF in blink::RTCPeerConnectionHandler::OnIceCandidate

| Field | Value |
|-------|-------|
| **Issue ID** | [40062526](https://issues.chromium.org/issues/40062526) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ht...@chromium.org |
| **Created** | 2023-01-05 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

tested os:  

ubuntu 22.04  

tested chrome version:  

Chromium 110.0.5478.4  

Chromium 111.0.5521.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1089145.zip)

repro steps  

(1)python3 -m http.server 8000 |path to poc folder|  

(2)./chrome --disable-gesture-requirement-for-media-playback <http://localhost:8000/poc.html>  

I can reproduce the issue within a few seconds on my PC. However, but it may not be as stable on other machines. If you are unable to reproduce it stabley, you can try using the script launcher.js (you will need to modify the paths inside) to launch multiple browsers simultaneously. The UAF should be reproduced in a minute.  

(3)  

./launcher.sh 2>&1|grep use-after-free

**Problem Description:**  

==2871694==ERROR: AddressSanitizer: heap-use-after-free on address 0x61700045cca0 at pc 0x55f4a0ba9933 bp 0x7ffe19ad22b0 sp 0x7ffe19ad22a8  

READ of size 8 at 0x61700045cca0 thread T0 (chrome)  

#0 0x55f4a0ba9932 in GetValue ./../../v8/include/cppgc/persistent.h:28:41  

#1 0x55f4a0ba9932 in Get ./../../v8/include/cppgc/persistent.h:191:46  

#2 0x55f4a0ba9932 in operator bool ./../../v8/include/cppgc/persistent.h:179:43  

#3 0x55f4a0ba9932 in blink::RTCPeerConnectionHandler::OnIceCandidate(WTF::String const&, WTF::String const&, int, int, int) ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_peer\_connection\_handler.cc:2261:7  

#4 0x55f4a0bbb917 in blink::RTCPeerConnectionHandler::Observer::OnIceCandidateImpl(WTF::String const&, WTF::String const&, int, int, int, std::Cr::unique\_ptr<webrtc::SessionDescriptionInterface, std::Cr::default\_delete[webrtc::SessionDescriptionInterface](javascript:void(0);)>, std::Cr::unique\_ptr<webrtc::SessionDescriptionInterface, std::Cr::default\_delete[webrtc::SessionDescriptionInterface](javascript:void(0);)>, std::Cr::unique\_ptr<webrtc::SessionDescriptionInterface, std::Cr::default\_delete[webrtc::SessionDescriptionInterface](javascript:void(0);)>, std::Cr::unique\_ptr<webrtc::SessionDescriptionInterface, std::Cr::default\_delete[webrtc::SessionDescriptionInterface](javascript:void(0);)>) ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_peer\_connection\_handler.cc:930:17  

#5 0x55f4a0bbbdf6 in Invoke<void (blink::RTCPeerConnectionHandler::Observer::\*)(const WTF::String &, const WTF::String &, int, int,  

...  

#9 0x55f48c0cb2be in Run ./../../base/functional/callback.h:152:12  

#10 0x55f48c0cb2be in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:157:32  

#11 0x55f48c11dcfa in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:486:11)> ./../../base/task/common/task\_annotator.h:85:5  

#12 0x55f48c11dcfa in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:484:23  

#13 0x55f48c11c9a2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:335:30  

#14 0x55f48c11f32a in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#15 0x55f48bfa19eb in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:48:55  

#16 0x55f48c1200aa in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:644:12  

#17 0x55f48c04548d in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:140:14  

#18 0x55f4a3ecca67 in content::RendererMain(content::MainFunctionParams) ./../../content/renderer/renderer\_main.cc:330:16  

#19 0x55f48ac2d2bc in content::RunOtherNamedProcessTypeMain(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:746:14  

#20 0x55f48ac2f979 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1100:10  

#21 0x55f48ac271fe in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:344:36  

#22 0x55f48ac27a37 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:372:10  

#23 0x55f47a7527be in ChromeMain ./../../chrome/app/chrome\_main.cc:174:12  

#24 0x7f01efe3fd8f in \_\_libc\_start\_call\_main ./csu/../sysdeps/nptl/libc\_start\_call\_main.h:58:16

0x61700045cca0 is located 160 bytes inside of 728-byte region [0x61700045cc00,0x61700045ced8)  

freed by thread T0 (chrome) here:  

#0 0x55f47a74f48d in operator delete(void\*) *asan\_rtl*:3  

#1 0x55f4a389ca55 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#2 0x55f4a389ca55 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#3 0x55f4a389ca55 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#4 0x55f4a389ca55 in blink::RTCPeerConnection::~RTCPeerConnection() ./../../third\_party/blink/renderer/modules/peerconnection/rtc\_peer\_connection.cc:666:1  

#5 0x55f482297b26 in AddFinalizer ./../../v8/src/heap/cppgc/sweeper.cc:267:13  

#6 0x55f482297b26 in SweepNormalPage<cppgc::internal::(anonymous namespace)::InlinedFinalizationBuilder<cppgc::internal::(anonymous namespace)::RegularFreeHandler> > ./../../v8/src/heap/cppgc/sweeper.cc:376:15  

#7 0x55f482297b26 in VisitNormalPage ./../../v8/src/heap/cppgc/sweeper.cc:587:15  

#8

**Additional Comments:**

\*\*Chrome version: \*\* 110.0.5478.4 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 42.6 KB)
- [launcher.sh](attachments/launcher.sh) (text/plain, 397 B)

## Timeline

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### da...@chromium.org (2023-01-05)

I suspect this is due to holding a unique_ptr in a GC class... but I don't follow how we're bypassing the WeakPtr in these backrtaces.

RTCPeerConnection has a unique_ptr<RTCPeerConnectionHandler>.
RTCPeerConnectionHandler::Observer has a WeakPtr<RTCPeerConnectionHandler>.
RTCPeerConnectionHandler has a WeakPtrFactory<RTCPeerConnectionHandler>.

The ASAN free stack shows RTCPeerConnection is destroyed (during GC sweep) which destroys RTCPeerConnectionHandler which invalidates weak ptr.

So RTCPeerConnectionHandler::Observer's WeakPtr should be invalidated unless it's on a different thread and this is a thread race (WeakPtr can not be used across threads). But no the ASAN log shows everything on thread T0.

### da...@chromium.org (2023-01-05)

I reproduced on ASAN M109 after ~1 minute.

==1==ERROR: AddressSanitizer: heap-use-after-free on address 0x617000124c20 at pc 0x564bad4280c0 bp 0x7ffef063c0d0 sp 0x7ffef063c0c8
READ of size 8 at 0x617000124c20 thread T0 (chrome)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x564bad4280bf in GetValue ./../../v8/include/cppgc/persistent.h:28:41
    #1 0x564bad4280bf in Get ./../../v8/include/cppgc/persistent.h:191:46
    #2 0x564bad4280bf in operator bool ./../../v8/include/cppgc/persistent.h:179:43
    #3 0x564bad4280bf in blink::RTCPeerConnectionHandler::OnIceCandidate(WTF::String const&, WTF::String const&, int, int, int) ./../../third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc:2306:7
    #4 0x564bad438375 in blink::RTCPeerConnectionHandler::Observer::OnIceCandidateImpl(WTF::String const&, WTF::String const&, int, int, int, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>) ./../../third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc:939:17
    #5 0x564bad4387e2 in Invoke<void (blink::RTCPeerConnectionHandler::Observer::*)(const WTF::String &, const WTF::String &, int, int, int, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >), cppgc::internal::BasicCrossThreadPersistent<blink::RTCPeerConnectionHandler::Observer, cppgc::internal::StrongCrossThreadPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, WTF::String, WTF::String, int, int, int, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> > > ./../../base/functional/bind_internal.h:646:12
    #6 0x564bad4387e2 in MakeItSo<void (blink::RTCPeerConnectionHandler::Observer::*)(const WTF::String &, const WTF::String &, int, int, int, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >), std::Cr::tuple<cppgc::internal::BasicCrossThreadPersistent<blink::RTCPeerConnectionHandler::Observer, cppgc::internal::StrongCrossThreadPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, WTF::String, WTF::String, int, int, int, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> > > > ./../../base/functional/bind_internal.h:825:12
    #7 0x564bad4387e2 in RunImpl<void (blink::RTCPeerConnectionHandler::Observer::*)(const WTF::String &, const WTF::String &, int, int, int, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >), std::Cr::tuple<cppgc::internal::BasicCrossThreadPersistent<blink::RTCPeerConnectionHandler::Observer, cppgc::internal::StrongCrossThreadPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, WTF::String, WTF::String, int, int, int, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> >, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface> > >, 0UL, 1UL, 2UL, 3UL, 4UL, 5UL, 6UL, 7UL, 8UL, 9UL> ./../../base/functional/bind_internal.h:919:12
    #8 0x564bad4387e2 in base::internal::Invoker<base::internal::BindState<void (blink::RTCPeerConnectionHandler::Observer::*)(WTF::String const&, WTF::String const&, int, int, int, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>), cppgc::internal::BasicCrossThreadPersistent<blink::RTCPeerConnectionHandler::Observer, cppgc::internal::StrongCrossThreadPersistentPolicy, cppgc::internal::IgnoreLocationPolicy, cppgc::internal::DisabledCheckingPolicy>, WTF::String, WTF::String, int, int, int, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>, std::Cr::unique_ptr<webrtc::SessionDescriptionInterface, std::Cr::default_delete<webrtc::SessionDescriptionInterface>>>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:870:12
    #9 0x564b9a884df9 in Run ./../../base/functional/callback.h:174:12
    #10 0x564b9a884df9 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:154:32
    #11 0x564b9a8cbc19 in RunTask<(lambda at ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:451:11)> ./../../base/task/common/task_annotator.h:84:5


0x617000124c20 is located 160 bytes inside of 736-byte region [0x617000124b80,0x617000124e60)
freed by thread T0 (chrome) here:
    #0 0x564b8a3a1f3d in operator delete(void*) _asan_rtl_:3
    #1 0x564bafc55b5a in operator() ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:49:5
    #2 0x564bafc55b5a in reset ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:281:7
    #3 0x564bafc55b5a in ~unique_ptr ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:247:75
    #4 0x564bafc55b5a in blink::RTCPeerConnection::~RTCPeerConnection() ./../../third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:643:1
    #5 0x564b9143d1d7 in AddFinalizer ./../../v8/src/heap/cppgc/sweeper.cc:267:13
    #6 0x564b9143d1d7 in SweepNormalPage<cppgc::internal::(anonymous namespace)::InlinedFinalizationBuilder<cppgc::internal::(anonymous namespace)::RegularFreeHandler> > ./../../v8/src/heap/cppgc/sweeper.cc:376:15
    #7 0x564b9143d1d7 in VisitNormalPage ./../../v8/src/heap/cppgc/sweeper.cc:587:15
    #8 0x564b9143d1d7 in VisitNormalPageImpl ./../../v8/src/heap/cppgc/heap-visitor.h:75:24
    #9 0x564b9143d1d7 in cppgc::internal::HeapVisitor<cppgc::internal::(anonymous namespace)::MutatorThreadSweeper>::Traverse(cppgc::internal::BasePage&) ./../../v8/src/heap/cppgc/heap-visitor.h:47:11
    #10 0x564b91437f3d in SweepPage ./../../v8/src/heap/cppgc/sweeper.cc:538:36



previously allocated by thread T0 (chrome) here:
    #0 0x564b8a3a16dd in operator new(unsigned long) _asan_rtl_:3
    #1 0x564bad3e0d2d in make_unique<blink::RTCPeerConnectionHandler, blink::RTCPeerConnectionHandlerClient *&, blink::PeerConnectionDependencyFactory *, scoped_refptr<base::SingleThreadTaskRunner> &, bool &> ./../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:670:26
    #2 0x564bad3e0d2d in blink::PeerConnectionDependencyFactory::CreateRTCPeerConnectionHandler(blink::RTCPeerConnectionHandlerClient*, scoped_refptr<base::SingleThreadTaskRunner>, bool) ./../../third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory.cc:492:10
    #3 0x564bafc55320 in blink::RTCPeerConnection::RTCPeerConnection(blink::ExecutionContext*, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::GoogMediaConstraints*, blink::ExceptionState&) ./../../third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc:598:40
    #4 0x564bafc5049c in Call<blink::ExecutionContext *&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::GoogMediaConstraints *&, blink::ExceptionState &> ./../../v8/include/cppgc/allocation.h:242:32
    #5 0x564bafc5049c in MakeGarbageCollected<blink::RTCPeerConnection, blink::ExecutionContext *&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::GoogMediaConstraints *&, blink::ExceptionState &> ./../../v8/include/cppgc/allocation.h:280:7
    #6 0x564bafc5049c in MakeGarbageCollected<blink::RTCPeerConnection, blink::ExecutionContext *&, webrtc::PeerConnectionInterface::RTCConfiguration, bool, blink::GoogMediaConstraints *&, blink::ExceptionState &> ./../../third_party/blink/renderer/platform/heap/garbage_collected.h:34:10


The WeakPtr and WeakPtrFactory have been around since like 2017.

[Monorail components: Blink>WebRTC]

### da...@chromium.org (2023-01-05)

+mlippautz for maybe some insightful help due to this being a mixture of GC types and non-GC types, and running destructors in sweep is generally bad but not sure how it plays into things here.

### da...@chromium.org (2023-01-05)

Reproduced in M108 (even quicker).

### da...@chromium.org (2023-01-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-05)

[Empty comment from Monorail migration]

### ht...@chromium.org (2023-01-05)

Adding the members of my team who have been wrestling with weak pointers most recently.


### ht...@chromium.org (2023-01-05)

Original poster, since you've been playing around with this:

Does the problem occur if you don't have the window.location.reload() active? I've seen issues before that could only be reproduced when the page was reloaded - the combination of an open/close race and a reload race could give some unique collisions.

(it's almost 11pm here now, so I'll look at this tomorrow)



### em...@gmail.com (2023-01-06)

#9
I have tested it multiple times. On my end, the issue can be stabley reproduced when it includes window.location.reload().
It has also been reproduced without window.location.reload(), which was immediately after the POC was executed. However, it is very unstable, and I have only been able to reproduce it once out of dozens of tests.

### ht...@chromium.org (2023-01-06)

Hm. The line pointed to is "if peer_connection_tracker_", where peer_connection_tracker_ is a weak pointer, but it is inside the RTCPeerConnectionObesrver object, which is pointed to by a std::unique_ptr from the RTCPeerConnection object - and it is the destructor of the RTCPeerConnection object that is noted as being the caller when the object is deleted.


### ht...@chromium.org (2023-01-06)

sorry, peer_connection_tracker_ is in the RTCPeerConnectionHandler object, not the RTCPeerConnectionObserver object.
So the Observer hangs around because there are references to it that are not deleted, but the Handler has gone away.

Having the same object pointed to by weak pointers and by std::unique_ptr seems to be Wrong.


### ht...@chromium.org (2023-01-06)

Not able to reproduce on tip-of-tree on Linux (self-built Chrome with is_asan=true).

Note that there are race conditions in the code - if the randomly-timed PeerConnection creation hits while the answer is being generated, there will be an error mesage saying that the SDP for setLocalDescription is modified, which isn't allowed. But that shouldn't affect the repro.

I have a suspicion that it's simpler to write an unit test to reproduce it, but that requires that someone else can verify that the POC stops working.





### [Deleted User] (2023-01-06)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@chromium.org (2023-01-08)

I'd conclude similar to what hta@ already wrote:
- RTCPeerConnection is being destroyed (due to being unreachable) which destroys RTCPeerConnectionHandler
- RTCPeerConnectionHandler::Observer is still alive. I see that it's held via CrossThreadPersistent which acts as a root. So even if the handler is destroyed, the observer will be alive for at least one more GC cylce. 

It looks to me like the RTCPeerConnectionHandler has not had its weak_factory_ [2] invalidated when the observer performs the `handler_` check.

Is this code executed concurrently? The ASAN stack trace suggests "thread T0" for all samples but on first sight a race only makes sense to me with multi-threaded code. (The GC will execute dtors on the thread the object was created on.) 

GC + CrossThreadPersistent + WeakPtr is really hard to get right.

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc;l=1085;drc=5582605a536229308e1f74a46995aa2e77fac081;bpv=1;bpt=1?q=rtc_peer_connection_handler.cc:930&ss=chromium
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.h;l=507?q=RTCPeerConnectionHandler&ss=chromium


### gi...@appspot.gserviceaccount.com (2023-01-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9c029334a55e0518f604e3908fd931e104f362e7

commit 9c029334a55e0518f604e3908fd931e104f362e7
Author: Harald Alvestrand <hta@chromium.org>
Date: Mon Jan 09 11:10:54 2023

Check that PC handler is not deleted before using it

The OnSessionDescriptionsUpdated calls may be able to fire events,
which may invoke garbage collection, which may delete the
RTCPeerConnectionHandler object. Guard against this.

Bug: chromium:1405256
Change-Id: Ied45c0e9575a2b67e4b12fadbaa0266602a50b91
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4146479
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1090262}

[modify] https://crrev.com/9c029334a55e0518f604e3908fd931e104f362e7/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler_test.cc
[modify] https://crrev.com/9c029334a55e0518f604e3908fd931e104f362e7/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc


### ht...@chromium.org (2023-01-09)

I believe this fixes the issue - the issue will happen under the following conditions:
- A candidate is surfaced at the exact time a change to a session description happens
- The change to the session description causes an event to be fired
- The event causes a garbage collection, OR the yield implicit in event firing allows other code to be run that causes a garbage collection
- The garbage collection causes the PeerConnection object to be deleted
I hope the original submitter can verify that the fix works for the PoC, since I was unable to reproduce the bug.


### em...@gmail.com (2023-01-09)

Hi,
I tested with the new patch, unfortunately it can still be reproduced. 
Because handler_ is an invalid(freed) address not a nullptr,thus bypassing the detection.


### em...@gmail.com (2023-01-09)

If you can't repro this issue, you can try launcher.js in original report.
./launcher.sh 2>&1|grep use-after-free

It's eay to repro with this script file.


### [Deleted User] (2023-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-09)

Requesting merge to stable M108 because latest trunk commit (1090262) appears to be after stable branch point (1058933).

Requesting merge to beta M109 because latest trunk commit (1090262) appears to be after beta branch point (1070088).

Requesting merge to dev M110 because latest trunk commit (1090262) appears to be after dev branch point (1084008).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@chromium.org (2023-01-09)

OK, so this is a problem, but not the same problem that the fix fixes. Thanks for the verificaiton!
Back to the drawing board.



### ht...@chromium.org (2023-01-10)

Update: Got it to reproduce on Linux! Starting 3 tabs in parallel running the script worked for causing it to reproduce - within 10 minutes.

Note: the argument for defeating the user gesture requirement doesn't work. You have to click on the page and hit "return".



### [Deleted User] (2023-01-10)

Merge approved: your change passed merge requirements and is auto-approved for M110. Please go ahead and merge the CL to branch 5481 (refs/branch-heads/5481) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-10)

Merge review required: M109 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-10)

Merge review required: M108 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@chromium.org (2023-01-10)

Hold off on the merge requests. The CL did not fix the bug.


### gi...@appspot.gserviceaccount.com (2023-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4732044f24e366373a8d30a37a98226320592d58

commit 4732044f24e366373a8d30a37a98226320592d58
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Jan 11 22:46:35 2023

Make PeerConnectionHandler have a Persistent client link

This prevents garbage collection of RTCPeerConnection while
an RTCPeerConnectionHandler is active. The handler is passivated
when disconnected.

Bug: chromium:1405256
Change-Id: I317d203321698a8f8145565085c9a16747dfb129
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4154998
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1091533}

[modify] https://crrev.com/4732044f24e366373a8d30a37a98226320592d58/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_client.h
[modify] https://crrev.com/4732044f24e366373a8d30a37a98226320592d58/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler_test.cc
[modify] https://crrev.com/4732044f24e366373a8d30a37a98226320592d58/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.h
[modify] https://crrev.com/4732044f24e366373a8d30a37a98226320592d58/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/4732044f24e366373a8d30a37a98226320592d58/third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory_test.cc
[modify] https://crrev.com/4732044f24e366373a8d30a37a98226320592d58/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_client.h
[modify] https://crrev.com/4732044f24e366373a8d30a37a98226320592d58/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker_test.cc
[modify] https://crrev.com/4732044f24e366373a8d30a37a98226320592d58/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### ho...@chromium.org (2023-01-12)

[Empty comment from Monorail migration]

### ho...@chromium.org (2023-01-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/20d494ba7e43c8c28eecbb6f134612f99c1bf31b

commit 20d494ba7e43c8c28eecbb6f134612f99c1bf31b
Author: Tsuyoshi Horo <horo@chromium.org>
Date: Thu Jan 12 05:39:31 2023

Revert "Make PeerConnectionHandler have a Persistent client link"

This reverts commit 4732044f24e366373a8d30a37a98226320592d58.

Reason for revert: Caused failure on WebKit Linux Leak bot. See crbug.com/1406723

Bug: 1406723

Original change's description:
> Make PeerConnectionHandler have a Persistent client link
>
> This prevents garbage collection of RTCPeerConnection while
> an RTCPeerConnectionHandler is active. The handler is passivated
> when disconnected.
>
> Bug: chromium:1405256
> Change-Id: I317d203321698a8f8145565085c9a16747dfb129
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4154998
> Commit-Queue: Harald Alvestrand <hta@chromium.org>
> Reviewed-by: Guido Urdaneta <guidou@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1091533}

Bug: chromium:1405256
Change-Id: I57b2a7af5bc33cf4d807d612febf755e7d6af6da
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4161131
Commit-Queue: Tsuyoshi Horo <horo@chromium.org>
Reviewed-by: Tsuyoshi Horo <horo@chromium.org>
Reviewed-by: Takashi Sakamoto <tasak@google.com>
Owners-Override: Tsuyoshi Horo <horo@chromium.org>
Reviewed-by: Johann Koenig <johannkoenig@google.com>
Cr-Commit-Position: refs/heads/main@{#1091694}

[modify] https://crrev.com/20d494ba7e43c8c28eecbb6f134612f99c1bf31b/third_party/blink/renderer/modules/peerconnection/mock_rtc_peer_connection_handler_client.h
[modify] https://crrev.com/20d494ba7e43c8c28eecbb6f134612f99c1bf31b/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler_test.cc
[modify] https://crrev.com/20d494ba7e43c8c28eecbb6f134612f99c1bf31b/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.h
[modify] https://crrev.com/20d494ba7e43c8c28eecbb6f134612f99c1bf31b/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/20d494ba7e43c8c28eecbb6f134612f99c1bf31b/third_party/blink/renderer/modules/peerconnection/peer_connection_dependency_factory_test.cc
[modify] https://crrev.com/20d494ba7e43c8c28eecbb6f134612f99c1bf31b/third_party/blink/renderer/modules/peerconnection/peer_connection_tracker_test.cc
[modify] https://crrev.com/20d494ba7e43c8c28eecbb6f134612f99c1bf31b/third_party/blink/renderer/platform/peerconnection/rtc_peer_connection_handler_client.h
[modify] https://crrev.com/20d494ba7e43c8c28eecbb6f134612f99c1bf31b/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### ho...@chromium.org (2023-01-12)

[Empty comment from Monorail migration]

### ho...@chromium.org (2023-01-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5066dd66309d884762e5fb9be04b59582893d09a

commit 5066dd66309d884762e5fb9be04b59582893d09a
Author: Harald Alvestrand <hta@chromium.org>
Date: Thu Jan 12 13:06:55 2023

Delete PeerConnectionHandler in PeerConnection finalizer

Also guard against removal of PC during PeerConnectionHandler
call that may cause garbage collection.

Bug: chromium:1405256
Change-Id: I9adf7b219e2026e07ccc0868c1a85f3b35cd9d26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4154578
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1091801}

[modify] https://crrev.com/5066dd66309d884762e5fb9be04b59582893d09a/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/5066dd66309d884762e5fb9be04b59582893d09a/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### ht...@chromium.org (2023-01-12)

The rolled-back fix had side effects, and did not fix the issue fully. It won't be rolled back in.

A new attempted fix has landed at Cr-Commit-Position: refs/heads/main@{#1091801}

Given the speed at which sheriffbot requests downmerges, I think it would be wise to check with the reporter that this is a real fix before setting status to "fixed" and doing the merge-request thing again.


### em...@gmail.com (2023-01-12)

confirmed. I tested it for about 30 minutes and did not reproduce this issue.
Before the patch, I can quickly reproduce it on my pc. So I think 30 minutes should be enough.

### ht...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### ht...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### ht...@chromium.org (2023-01-13)

Merge review answers:

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

It's an use-after-free, which is labelled as a pri 1 security issue. go/crash seems to indicate that it's happened once in the wild.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/4154578

3. Have the changes been released and tested on canary?

Yes, in 111.0.5536.0

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No, it is a bug fix.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No, the bug is quite hard to reach.


### [Deleted User] (2023-01-13)

Merge review required: M110 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@chromium.org (2023-01-14)

See answers in #40


### ea...@google.com (2023-01-17)

Adding @amyressler for Review

### am...@chromium.org (2023-01-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-17)

merge approved for https://chromium-review.googlesource.com/c/chromium/src/+/4154578
m110 merge approved, please merge to branch 5481 
m109 merge approved, please merge to branch 5414
m108 merge approved, please merge to branch 5359

Please merge at your earliest convenience and before Friday, 10am Pacific so this fix can be included in next week's respins of Stable and Extended Stable.

### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca2b108a0f1ffed3efc69b0dcb5b6dd5020ec7cf

commit ca2b108a0f1ffed3efc69b0dcb5b6dd5020ec7cf
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Jan 18 08:02:48 2023

[Merge M110] Delete PeerConnectionHandler in PeerConnection finalizer

Also guard against removal of PC during PeerConnectionHandler
call that may cause garbage collection.

(cherry picked from commit 5066dd66309d884762e5fb9be04b59582893d09a)

Bug: chromium:1405256
Change-Id: I9adf7b219e2026e07ccc0868c1a85f3b35cd9d26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4154578
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1091801}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4176372
Auto-Submit: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#418}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/ca2b108a0f1ffed3efc69b0dcb5b6dd5020ec7cf/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/ca2b108a0f1ffed3efc69b0dcb5b6dd5020ec7cf/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3534c5277fd7583fc3d55f2c491e8441bb1217ff

commit 3534c5277fd7583fc3d55f2c491e8441bb1217ff
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Jan 18 08:02:06 2023

[Merge M109] Delete PeerConnectionHandler in PeerConnection finalizer

Also guard against removal of PC during PeerConnectionHandler
call that may cause garbage collection.

(cherry picked from commit 5066dd66309d884762e5fb9be04b59582893d09a)

Bug: chromium:1405256
Change-Id: I9adf7b219e2026e07ccc0868c1a85f3b35cd9d26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4154578
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1091801}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4176392
Auto-Submit: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#1400}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/3534c5277fd7583fc3d55f2c491e8441bb1217ff/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/3534c5277fd7583fc3d55f2c491e8441bb1217ff/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/02ef9983710df374107967ba0685e190d53f990c

commit 02ef9983710df374107967ba0685e190d53f990c
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Jan 18 08:03:04 2023

[Merge M108] Delete PeerConnectionHandler in PeerConnection finalizer

Also guard against removal of PC during PeerConnectionHandler
call that may cause garbage collection.

(cherry picked from commit 5066dd66309d884762e5fb9be04b59582893d09a)

Bug: chromium:1405256
Change-Id: I9adf7b219e2026e07ccc0868c1a85f3b35cd9d26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4154578
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1091801}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4176412
Auto-Submit: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1347}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/02ef9983710df374107967ba0685e190d53f990c/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/02ef9983710df374107967ba0685e190d53f990c/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ca2b108a0f1ffed3efc69b0dcb5b6dd5020ec7cf

commit ca2b108a0f1ffed3efc69b0dcb5b6dd5020ec7cf
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Jan 18 08:02:48 2023

[Merge M110] Delete PeerConnectionHandler in PeerConnection finalizer

Also guard against removal of PC during PeerConnectionHandler
call that may cause garbage collection.

(cherry picked from commit 5066dd66309d884762e5fb9be04b59582893d09a)

Bug: chromium:1405256
Change-Id: I9adf7b219e2026e07ccc0868c1a85f3b35cd9d26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4154578
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1091801}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4176372
Auto-Submit: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#418}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/ca2b108a0f1ffed3efc69b0dcb5b6dd5020ec7cf/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/ca2b108a0f1ffed3efc69b0dcb5b6dd5020ec7cf/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### gi...@appspot.gserviceaccount.com (2023-01-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/02ef9983710df374107967ba0685e190d53f990c

commit 02ef9983710df374107967ba0685e190d53f990c
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed Jan 18 08:03:04 2023

[Merge M108] Delete PeerConnectionHandler in PeerConnection finalizer

Also guard against removal of PC during PeerConnectionHandler
call that may cause garbage collection.

(cherry picked from commit 5066dd66309d884762e5fb9be04b59582893d09a)

Bug: chromium:1405256
Change-Id: I9adf7b219e2026e07ccc0868c1a85f3b35cd9d26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4154578
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Guido Urdaneta <guidou@chromium.org>
Commit-Queue: Guido Urdaneta <guidou@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1091801}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4176412
Auto-Submit: Harald Alvestrand <hta@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1347}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/02ef9983710df374107967ba0685e190d53f990c/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection_handler.cc
[modify] https://crrev.com/02ef9983710df374107967ba0685e190d53f990c/third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc


### ht...@chromium.org (2023-01-18)

All done!


### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-18)

Congratulations, Cassidy Kim! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug. Thank you for your efforts in reporting this issue to us as well as letting us know the original fix did not mitigate the UAF! 

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-24)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-24)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1405256?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1406723]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062526)*
