# Security: heap-use-after-free in blink::ConsumerWrapper::consumeAudio

| Field | Value |
|-------|-------|
| **Issue ID** | [40081780](https://issues.chromium.org/issues/40081780) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Reporter** | ch...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2015-04-02 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 41.0.2272.118  

Operating System: Windows 7

==7748==ERROR: AddressSanitizer: heap-use-after-free on address 0x0301b4a0 at pc 0x113355db bp 0xdeadbeef sp 0x55cef190  

READ of size 4 at 0x0301b4a0 thread T23  

#0 0x113355da in blink::ConsumerWrapper::consumeAudio C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\exported\WebMediaStreamSource.cpp:209  

#1 0x113927fe in blink::MediaStreamSource::consumeAudio C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\mediastream\MediaStreamSource.cpp:105  

#2 0x1325cae8 in blink::MediaStreamAudioDestinationNode::process C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\webaudio\MediaStreamAudioDestina  

tionNode.cpp:79  

#3 0x12ff527b in blink::AudioNode::processIfNecessary C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\webaudio\AudioNode.cpp:634  

#4 0x1308809b in blink::AudioContext::processAutomaticPullNodes C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\webaudio\AudioContext.cpp:1133  

#5 0x13499b3c in blink::AudioDestinationNode::render C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\webaudio\AudioDestinationNode.cpp:93  

#6 0x1adfc812 in blink::AudioDestination::provideInput C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\audio\AudioDestination.cpp:175  

#7 0x1af7884f in blink::AudioPullFIFO::consume C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\audio\AudioPullFIFO.cpp:65  

#8 0x1adfc4d6 in blink::AudioDestination::render C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\audio\AudioDestination.cpp:164  

#9 0x17529f85 in content::RendererWebAudioDeviceImpl::Render C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\renderer\_webaudiodevice\_impl.cc:90  

#10 0x1a4b5a89 in media::AudioOutputDevice::AudioThreadCallback::Process C:\b\build\slave\Win\_ASan\_Release\build\src\media\audio\audio\_output\_device.cc:297  

#11 0x1a57c99b in media::AudioDeviceThread::Thread::Run C:\b\build\slave\Win\_ASan\_Release\build\src\media\audio\audio\_device\_thread.cc:183  

#12 0x1a57c67c in media::AudioDeviceThread::Thread::ThreadMain C:\b\build\slave\Win\_ASan\_Release\build\src\media\audio\audio\_device\_thread.cc:158

0x0301b4a0 is located 0 bytes inside of 88-byte region [0x0301b4a0,0x0301b4f8)  

freed by thread T0 here:  

#0 0x10d41e4 in free c:\b\build\slave\win\_asan\_release\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:42  

#1 0x174d4c7f in content::WebAudioCapturerSource::`scalar deleting destructor' C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\webaudio\_capturer\_source.cc:2  

7  

#2 0x172b4f71 in content::WebRtcLocalAudioTrack::Stop C:\b\build\slave\Win\_ASan\_Release\build\src\base\memory\ref\_counted.h:192  

#3 0x173b9eb6 in content::MediaStreamCenter::didStopMediaStreamTrack C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\media\_stream\_center.cc:119  

#4 0x1addd3d7 in blink::MediaStreamCenter::didStopMediaStreamTrack C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\mediastream\MediaStreamCenter  

.cpp:94  

#5 0x12c2b850 in blink::MediaStreamTrack::stopTrack C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\mediastream\MediaStreamTrack.cpp:159  

#6 0x12c1a9e0 in blink::Heap::allocate[blink::PositionErrorCallback](javascript:void(0);) C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\modules\v8\V8MediaStreamTrack.c  

pp:267  

#7 0x120631d8 in v8::internal::FunctionCallbackArguments::Call C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\arguments.cc:33  

#8 0x11bf50eb in v8::internal::Builtins::InvokeApiFunction C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1077  

#9 0x11c01e6b in v8::internal::Builtins::Builtins C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1100

previously allocated by thread T0 here:  

#0 0x10d42b8 in malloc c:\b\build\slave\win\_asan\_release\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:58  

#1 0x1be4aa9d in operator new f:\dd\vctools\crt\crtw32\heap\new.cpp:59  

#2 0x172ab278 in content::PeerConnectionDependencyFactory::CreateWebAudioSource C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\webrtc\peer\_connection\_depen  

dency\_factory.cc:508  

#3 0x172aaa63 in content::PeerConnectionDependencyFactory::CreateLocalAudioTrack C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\webrtc\peer\_connection\_depe  

ndency\_factory.cc:463  

#4 0x173b9cdd in content::MediaStreamCenter::didCreateMediaStreamTrack C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\media\_stream\_center.cc:44  

#5 0x173b9ad1 in content::MediaStreamCenter::didCreateMediaStreamTrack C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\media\_stream\_center.cc:96  

#6 0x1addd60c in blink::MediaStreamCenter::didCreateMediaStreamAndTracks C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\mediastream\MediaStream  

Center.cpp:123  

#7 0x1325bba6 in blink::MediaStreamAudioDestinationNode::MediaStreamAudioDestinationNode C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\webaudio  

\MediaStreamAudioDestinationNode.cpp:52  

#8 0x1325b46a in blink::MediaStreamAudioDestinationNode::create C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\webaudio\MediaStreamAudioDestinat  

ionNode.cpp:40  

#9 0x130792d9 in blink::AudioContext::createMediaStreamDestination C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\webaudio\AudioContext.cpp:388  

#10 0x12e30bb4 in blink::ScreenOrientation::setOnchange C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\modules\v8\V8AudioContext.cpp:346  

#11 0x120631d8 in v8::internal::FunctionCallbackArguments::Call C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\arguments.cc:33  

#12 0x11bf50eb in v8::internal::Builtins::InvokeApiFunction C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1077  

#13 0x11c01e6b in v8::internal::Builtins::Builtins C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1100

Thread T23 created by T2 here:  

#0 0x10dee50 in \_\_asan\_wrap\_CreateThread c:\b\build\slave\win\_asan\_release\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_win.cc:93

Thread T2 created by T0 here:  

#0 0x10dee50 in \_\_asan\_wrap\_CreateThread c:\b\build\slave\win\_asan\_release\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_win.cc:93

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\platform\exported\WebMediaStreamSource.cpp:209 blink::Consumer  

Wrapper::consumeAudio  

Shadow bytes around the buggy address:  

0x30603640: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x30603650: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x30603660: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x30603670: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x30603680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x30603690: fa fa fa fa[fd]fd fd fd fd fd fd fd fd fd fd fa  

0x306036a0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x306036b0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 04  

0x306036c0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x306036d0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x306036e0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==7748==ABORTING

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 1022 B)
- [78632.mp4](attachments/78632.mp4) (application/octet-stream, 183.2 KB)

## Timeline

### ch...@gmail.com (2015-04-02)

Crash ID : 9b70f9356a9cdf27

### in...@chromium.org (2015-04-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-03)

[Empty comment from Monorail migration]

### pe...@chromium.org (2015-04-07)

tommyw is still ooo.

quido, can this be related to you latest fix in WebMediaStreamSource?
Talk to rtoy for questions related to webaudio.



### gu...@chromium.org (2015-04-07)

I haven't submitted any fix for the WebMediaStreamSource bug (469145), but it seems that both are reproduced with the same test case. They are likely to be the same bug.
I'll take a look to see if I can find something.

### [Deleted User] (2015-04-08)

Adding flags so this can be queried more easily // asan_win_trophy

### bu...@chromium.org (2015-04-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/228cd9447121ede4d32ab48c8dfe066736cfdae2

commit 228cd9447121ede4d32ab48c8dfe066736cfdae2
Author: guidou <guidou@chromium.org>
Date: Fri Apr 10 13:00:37 2015

Fix heap-use-after-free issue with WebAudioCapturerSource.

WebAudioCapturerSource registers with a blink WebMediaStreamSource.
When the audio track was stopped, the WebAudioCapturerSource was
destroyed and the WebMediaStreamSource was left with a dangling
pointer, which it tried to use, resulting in access to freed
memory and usually a crashed tab.

This CL makes WebAudioCapturerSource aware of the WebMediaStreamSource
with which it is registered, so that it can be deregistered when the
audio track is stopped.

BUG=473253
TEST=See testcase.html in crbug.com/473253

Review URL: https://codereview.chromium.org/1071063005

Cr-Commit-Position: refs/heads/master@{#324622}

[modify] http://crrev.com/228cd9447121ede4d32ab48c8dfe066736cfdae2/content/renderer/media/webaudio_capturer_source.cc
[modify] http://crrev.com/228cd9447121ede4d32ab48c8dfe066736cfdae2/content/renderer/media/webaudio_capturer_source.h
[modify] http://crrev.com/228cd9447121ede4d32ab48c8dfe066736cfdae2/content/renderer/media/webrtc/peer_connection_dependency_factory.cc


### gu...@chromium.org (2015-04-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-05-11)

Merge Requested to M43 (branch 2357)

### la...@google.com (2015-05-11)

[Automated comment] Request affecting a post-stable build (M42), manual review required.

### la...@google.com (2015-05-11)

[Automated comment] Less than 2 weeks to go before stable on M43, manual review required.

### la...@google.com (2015-05-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2015-05-11)

Not happening for 42.

### la...@google.com (2015-05-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/beca77c820c579ee29ff8387b5a42765ef8ccee4

commit beca77c820c579ee29ff8387b5a42765ef8ccee4
Author: Magnus Jedvert <magjed@google.com>
Date: Tue May 12 15:33:18 2015

Fix heap-use-after-free issue with WebAudioCapturerSource.

WebAudioCapturerSource registers with a blink WebMediaStreamSource.
When the audio track was stopped, the WebAudioCapturerSource was
destroyed and the WebMediaStreamSource was left with a dangling
pointer, which it tried to use, resulting in access to freed
memory and usually a crashed tab.

This CL makes WebAudioCapturerSource aware of the WebMediaStreamSource
with which it is registered, so that it can be deregistered when the
audio track is stopped.

BUG=473253
TEST=See testcase.html in crbug.com/473253

Review URL: https://codereview.chromium.org/1071063005

Cr-Commit-Position: refs/heads/master@{#324622}
(cherry picked from commit 228cd9447121ede4d32ab48c8dfe066736cfdae2)

R=guidou@chromium.org
TBR=henrika, perkj

Review URL: https://codereview.chromium.org/1136803003

Cr-Commit-Position: refs/branch-heads/2357@{#369}
Cr-Branched-From: 59d4494849b405682265ed5d3f5164573b9a939b-refs/heads/master@{#323860}

[modify] http://crrev.com/beca77c820c579ee29ff8387b5a42765ef8ccee4/content/renderer/media/webaudio_capturer_source.cc
[modify] http://crrev.com/beca77c820c579ee29ff8387b5a42765ef8ccee4/content/renderer/media/webaudio_capturer_source.h
[modify] http://crrev.com/beca77c820c579ee29ff8387b5a42765ef8ccee4/content/renderer/media/webrtc/peer_connection_dependency_factory.cc


### bu...@chromium.org (2015-05-14)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/beca77c820c579ee29ff8387b5a42765ef8ccee4

commit beca77c820c579ee29ff8387b5a42765ef8ccee4
Author: Magnus Jedvert <magjed@google.com>
Date: Tue May 12 15:33:18 2015


### ti...@google.com (2015-05-16)

[Empty comment from Monorail migration]

### ti...@google.com (2015-05-28)

Congrats - as mentioned in the release notes, $3000 for this report. We'll take care of payment in the next payment run.

### ti...@google.com (2015-06-25)

We'll process this reward via our new payment process which should only take ~1-2 weeks.  

### cl...@chromium.org (2015-07-17)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-07-24)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

(Note: sorry for the delay here - it turns out in the new payment system, these payments were waiting for a second approval from me).

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/473253?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/469145]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081780)*
