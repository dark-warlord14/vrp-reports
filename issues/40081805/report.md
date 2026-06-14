# Security: heap-use-after-free in content::MediaStreamDispatcher::OnStreamGenerated

| Field | Value |
|-------|-------|
| **Issue ID** | [40081805](https://issues.chromium.org/issues/40081805) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2015-04-06 |
| **Bounty** | $1,000.00 |

## Description

**VERSION**  

Chrome Version: 44.0.2358.0 (Build Dev Win23 ASAN) (32 bits)  

Operating System: Windows 7

- Please watch the video for see how I repro this crash.

==4868==ERROR: AddressSanitizer: heap-use-after-free on address 0x26d38800 at pc 0x16ff57ef bp 0xdeadbeef sp 0x0028b4f0  

READ of size 4 at 0x26d38800 thread T0  

#0 0x16ff57ee in content::MediaStreamDispatcher::OnStreamGenerated C:\b\depot\_tools\win\_toolchain\vs2013\_files\VC\include\list:1448  

#1 0x16ff41bd in content::MediaStreamDispatcher::OnMessageReceived C:\b\build\slave\Win\_ASan\_Release\build\src\base\tuple.h:246  

#2 0x16de9feb in content::RenderFrameImpl::OnMessageReceived C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\render\_frame\_impl.cc:991  

#3 0x19767369 in content::MessageRouter::RouteMessage C:\b\build\slave\Win\_ASan\_Release\build\src\content\common\message\_router.cc:54  

#4 0x19767286 in content::MessageRouter::OnMessageReceived C:\b\build\slave\Win\_ASan\_Release\build\src\content\common\message\_router.cc:46  

#5 0x16b6a26c in content::ChildThreadImpl::OnMessageReceived C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\child\_thread\_impl.cc:627  

#6 0x196acab4 in IPC::ChannelProxy::Context::OnDispatchMessage C:\b\build\slave\Win\_ASan\_Release\build\src\ipc\ipc\_channel\_proxy.cc:282  

#7 0x171fe94b in base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall content::WebRtcLocalAudioRenderer::\*)(me  

dia::AudioParameters const &)>,void \_\_cdecl(content::WebRtcLocalAudioRenderer \*,media::AudioParameters const &),base::internal::TypeList<content::WebRtcLocalAudioRenderer \*,media:  

:AudioParameters> >,base::internal::TypeList<base::internal::UnwrapTraits<content::WebRtcLocalAudioRenderer \*>,base::internal::UnwrapTraits[media::AudioParameters](javascript:void(0);) >,base::interna  

l::InvokeHelper<0,void,base::internal::RunnableAdapter<void (\_\_thiscall content::WebRtcLocalAudioRenderer::\*)(media::AudioParameters const &)>,base::internal::TypeList<content::We  

bRtcLocalAudioRenderer \* const &,media::AudioParameters const &> >,void \_\_cdecl(void)>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\bind\_internal.h:176  

#8 0x102885db in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\callback.h:396  

#9 0x1b74aed7 in content::TaskQueueManager::ProcessTaskFromWorkQueue C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\scheduler\task\_queue\_manager.cc:641  

#10 0x1b749b92 in content::TaskQueueManager::DoWork C:\b\build\slave\Win\_ASan\_Release\build\src\content\child\scheduler\task\_queue\_manager.cc:599  

#11 0x17552410 in base::internal::Invoker<IndexSequence<0,1>,base::internal::BindState<base::internal::RunnableAdapter<void (\_\_thiscall content::TaskQueueManager::\*)(bool)>,vo  

id \_\_cdecl(content::TaskQueueManager \*,bool),base::internal::TypeList<base::WeakPtr[content::TaskQueueManager](javascript:void(0);),bool> >,base::internal::TypeList<base::internal::UnwrapTraits<base::  

WeakPtr[content::TaskQueueManager](javascript:void(0);) >,base::internal::UnwrapTraits<bool> >,base::internal::InvokeHelper<1,void,base::internal::RunnableAdapter<void (\_\_thiscall content::TaskQueueMa  

nager::\*)(bool)>,base::internal::TypeList<base::WeakPtr[content::TaskQueueManager](javascript:void(0);) const &,bool const &> >,void \_\_cdecl(void)>::Run C:\b\build\slave\Win\_ASan\_Release\build\src\bas  

e\bind\_internal.h:176  

#12 0x102885db in base::debug::TaskAnnotator::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\callback.h:396  

#13 0x101ae4d2 in base::MessageLoop::RunTask C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:444  

#14 0x101afb80 in base::MessageLoop::DoWork C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:454  

#15 0x10289f1f in base::MessagePumpDefault::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_pump\_default.cc:32  

#16 0x101ad306 in base::MessageLoop::RunHandler C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:410  

#17 0x1028ae8f in base::RunLoop::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\run\_loop.cc:55  

#18 0x101ac728 in base::MessageLoop::Run C:\b\build\slave\Win\_ASan\_Release\build\src\base\message\_loop\message\_loop.cc:303  

#19 0x16e53724 in content::RendererMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\renderer\_main.cc:220  

#20 0x1008d1ff in content::RunNamedProcessTypeMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:383  

#21 0x1008f617 in content::ContentMainRunnerImpl::Run C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main\_runner.cc:775  

#22 0x1008cdbb in content::ContentMain C:\b\build\slave\Win\_ASan\_Release\build\src\content\app\content\_main.cc:19  

#23 0xfcd113f in ChromeMain C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_main.cc:66  

#24 0x9399f3 in MainDllLoader::Launch C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\client\_util.cc:238  

#25 0x93307d in main C:\b\build\slave\Win\_ASan\_Release\build\src\chrome\app\chrome\_exe\_main\_win.cc:157  

#26 0xaddfb9 in \_\_tmainCRTStartup f:\dd\vctools\crt\crtw32\startup\crt0.c:255  

#27 0x75791173 in BaseThreadInitThunk+0x11 (C:\Windows\system32\kernel32.dll+0x51173)  

#28 0x7708b3f4 in RtlInitializeExceptionChain+0x62 (C:\Windows\SYSTEM32\ntdll.dll+0x5b3f4)  

#29 0x7708b3c7 in RtlInitializeExceptionChain+0x35 (C:\Windows\SYSTEM32\ntdll.dll+0x5b3c7)

0x26d38800 is located 0 bytes inside of 24-byte region [0x26d38800,0x26d38818)  

freed by thread T0 here:  

#0 0xac9094 in free c:\b\build\slave\win\_asan\_release\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:42  

#1 0x16ffee4e in content::MediaStreamDispatcher::~MediaStreamDispatcher C:\b\depot\_tools\win\_toolchain\vs2013\_files\VC\include\xmemory0:573  

#2 0x16ff9e1b in content::MediaStreamDispatcher::`scalar deleting destructor' C:\b\build\slave\Win_ASan_Release\build\src\content\renderer\media\media_stream_dispatcher.cc:69 #3 0x1701100b in content::UserMediaClientImpl::~UserMediaClientImpl C:\b\build\slave\Win_ASan_Release\build\src\base\memory\scoped_ptr.h:128 #4 0x1700f75b in content::UserMediaClientImpl::`scalar deleting destructor' C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\user\_media\_client\_impl.cc:117  

#5 0x18a03024 in CFX\_Edit\_UndoItem::Release C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\pdfium\fpdfsdk\src\fxedit\fxet\_edit.cpp:563  

#6 0x16e4d479 in content::RenderFrameImpl::~RenderFrameImpl C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\render\_frame\_impl.cc:711  

#7 0x16e4388b in content::RenderFrameImpl::`scalar deleting destructor' C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\render\_frame\_impl.cc:709  

#8 0x16e09ef2 in content::RenderFrameImpl::frameDetached C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\render\_frame\_impl.cc:2153  

#9 0x127dd0f2 in blink::FrameLoaderClientImpl::detached C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\web\FrameLoaderClientImpl.cpp:331  

#10 0x13f2315f in blink::Frame::detach C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\frame\Frame.cpp:80  

#11 0x13fb48c8 in blink::LocalFrame::detach C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\frame\LocalFrame.cpp:281  

#12 0x139a6814 in blink::HTMLFrameOwnerElement::disconnectContentFrame C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\html\HTMLFrameOwnerElement.cp  

p:152  

#13 0x139669b7 in blink::ChildFrameDisconnector::disconnectCollectedFrameOwners C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\ChildFrameDiscon  

nector.cpp:65  

#14 0x1396615f in blink::ChildFrameDisconnector::disconnect C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\ChildFrameDisconnector.cpp:35  

#15 0x137a4e2e in blink::ContainerNode::willRemoveChild C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\ContainerNode.cpp:427  

#16 0x137a3c68 in blink::ContainerNode::removeChild C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\ContainerNode.cpp:556  

#17 0x136f791b in blink::Node::remove C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\Node.cpp:506  

#18 0x161ebf58 in blink::V8XPathExpression::domTemplate C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\core\dom\ChildNode.h:16  

#19 0x11e1fde8 in v8::internal::FunctionCallbackArguments::Call C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\arguments.cc:33  

#20 0x119af3f7 in v8::internal::Builtins::InvokeApiFunction C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1088  

#21 0x119bcb2b in v8::internal::Runtime\_SetAllocationTimeout C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1111

previously allocated by thread T0 here:  

#0 0xac9168 in malloc c:\b\build\slave\win\_asan\_release\build\src\third\_party\llvm\projects\compiler-rt\lib\asan\asan\_malloc\_win.cc:58  

#1 0x1bd2f84d in operator new f:\dd\vctools\crt\crtw32\heap\new.cpp:59  

#2 0x16fedf5a in std::list<content::MediaStreamDispatcher::Request,std::allocator[content::MediaStreamDispatcher::Request](javascript:void(0);) >::push\_back C:\b\depot\_tools\win\_toolchain\vs2013\_f  

iles\VC\include\xmemory0:28  

#3 0x16fedbf7 in content::MediaStreamDispatcher::GenerateStream C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\media\_stream\_dispatcher.cc:79  

#4 0x170004e4 in content::UserMediaClientImpl::requestUserMedia C:\b\build\slave\Win\_ASan\_Release\build\src\content\renderer\media\user\_media\_client\_impl.cc:207  

#5 0x127e7bb7 in blink::UserMediaClientImpl::requestUserMedia C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\web\UserMediaClientImpl.cpp:52  

#6 0x12abbb79 in blink::UserMediaRequest::start C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\mediastream\UserMediaController.h:66  

#7 0x132d4680 in blink::NavigatorMediaStream::webkitGetUserMedia C:\b\build\slave\Win\_ASan\_Release\build\src\third\_party\WebKit\Source\modules\mediastream\NavigatorMediaStream  

.cpp:81  

#8 0x13225d69 in blink::V8WorkerNavigatorPartial::initialize C:\b\build\slave\Win\_ASan\_Release\build\src\out\Release\gen\blink\bindings\modules\v8\V8NavigatorPartial.cpp:477  

#9 0x11e1fde8 in v8::internal::FunctionCallbackArguments::Call C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\arguments.cc:33  

#10 0x119af3f7 in v8::internal::Builtins::InvokeApiFunction C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1088  

#11 0x119bcb2b in v8::internal::Runtime\_SetAllocationTimeout C:\b\build\slave\Win\_ASan\_Release\build\src\v8\src\builtins.cc:1111

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\depot\_tools\win\_toolchain\vs2013\_files\VC\include\list:1448 in content::MediaStreamDispatcher::OnStreamGenerated  

Shadow bytes around the buggy address:  

0x34da70b0: fa fa fd fd fd fa fa fa fd fd fd fd fa fa fd fd  

0x34da70c0: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  

0x34da70d0: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fd  

0x34da70e0: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd  

0x34da70f0: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  

=>0x34da7100:[fd]fd fd fa fa fa fd fd fd fa fa fa fd fd fd fd  

0x34da7110: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd  

0x34da7120: fd fd fa fa fd fd fd fd fa fa fd fd fd fd fa fa  

0x34da7130: fd fd fd fa fa fa fd fd fd fa fa fa 00 00 00 fa  

0x34da7140: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd  

0x34da7150: fd fa fa fa fd fd fd fd fa fa fd fd fd fa fa fa  

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

==4868==ABORTING

## Attachments

- [78887263.mp4](attachments/78887263.mp4) (application/octet-stream, 361.6 KB)
- [testcase12.html](attachments/testcase12.html) (text/html, 774 B)
- [PoC.html](attachments/PoC.html) (text/html, 891 B)
- [98269021.mp4](attachments/98269021.mp4) (application/octet-stream, 148.4 KB)

## Timeline

### js...@chromium.org (2015-04-07)

Please provide a testcase that doesn't require all the manual interaction. It looks like the only special requirement should be allowing the capture, and everything else should be automated in your PoC.

### ch...@gmail.com (2015-04-07)

I cannot provide a test case that doesn't require all the manual interaction, but I was wrong in the steps what I took in the video, so you can repo the crash easily with those below steps:

- Click in "publish button" and allow the mic.
- Click in "publish button" which is in the iframe and allow the mic. Crash!

### ch...@gmail.com (2015-04-07)

[Empty comment from Monorail migration]

### rs...@chromium.org (2015-04-07)

Mac crash: https://crash.corp.google.com/browse?q=reportid=%273327a78f66a9be17%27. Also affects M41.

### pe...@chromium.org (2015-04-08)

This is similar to crbug/472617 and probably started to happen with oilpan.
What happens is that the RenderFrame is beeing deleted from within the scope of a JS callback from chromium. Ie, the chromium code becomes reentrant. The object notifiying blink is deleted in the scope of the calling method.

So either blink / RenderFrameImpl is changed to make sure its not deleted from within the scope callback , or chromium code needs to be very careful with what happens after the callback.

In this case: 

void MediaStreamDispatcher::OnStreamGenerated(
...

 for (RequestList::iterator it = requests_.begin();
       it != requests_.end(); ++it) {
    Request& request = *it;
    if (request.ipc_request == request_id) {
      Stream new_stream;
      new_stream.handler = request.handler;
      new_stream.audio_array = audio_array;
      new_stream.video_array = video_array;
      label_stream_map_[label] = new_stream;
      if (request.handler.get()) {
        request.handler->OnStreamGenerated(  <--------------------Leads to call into blink.
            request.request_id, label, audio_array, video_array);
        DVLOG(1) << "MediaStreamDispatcher::OnStreamGenerated("
                 << request.request_id << ", " << label << ")";
      }
      requests_.erase(it); <---  "This" have been deleted. -> crash and boom and no good.
      break;
    }
  }
}







### pe...@chromium.org (2015-04-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-04-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/fa7c6fd4aa278dab68c5987b45353e064ce8e0ad

commit fa7c6fd4aa278dab68c5987b45353e064ce8e0ad
Author: perkj <perkj@chromium.org>
Date: Thu Apr 09 14:33:16 2015

This fixes a problem when the RenderFrame is destroyed within the context of a getusermedia callback.
BUG=472617, 474370

TBR=tommi@chromium.org

Review URL: https://codereview.chromium.org/1075833002

Cr-Commit-Position: refs/heads/master@{#324434}

[modify] http://crrev.com/fa7c6fd4aa278dab68c5987b45353e064ce8e0ad/content/renderer/media/user_media_client_impl.cc
[modify] http://crrev.com/fa7c6fd4aa278dab68c5987b45353e064ce8e0ad/content/renderer/media/user_media_client_impl.h
[modify] http://crrev.com/fa7c6fd4aa278dab68c5987b45353e064ce8e0ad/content/renderer/media/user_media_client_impl_unittest.cc


### in...@chromium.org (2015-04-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-04-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-04-09)

[Empty comment from Monorail migration]

### pe...@chromium.org (2015-04-10)

Magjed, Can you please ask for merge approval and merge this next week if all looks good? 

https://codereview.chromium.org/1075833002

### bu...@chromium.org (2015-04-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/64aae326a6b32fdfba377dc5e060fd4713a2295b

commit 64aae326a6b32fdfba377dc5e060fd4713a2295b
Author: perkj <perkj@chromium.org>
Date: Fri Apr 10 14:51:41 2015

Add tests for closing a frame within the scope of a getusermedia callback.

BUG=472617, 474370

Review URL: https://codereview.chromium.org/1073783003

Cr-Commit-Position: refs/heads/master@{#324633}

[modify] http://crrev.com/64aae326a6b32fdfba377dc5e060fd4713a2295b/content/browser/media/webrtc_getusermedia_browsertest.cc
[modify] http://crrev.com/64aae326a6b32fdfba377dc5e060fd4713a2295b/content/test/data/media/getusermedia.html


### ma...@chromium.org (2015-04-14)

Requesting merge to M43.

### la...@google.com (2015-04-14)

[Automated comment] Request affecting a post-stable build (M42), manual review required.

### la...@google.com (2015-04-14)

Approved for M43 (branch: 2357)

### bu...@chromium.org (2015-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0fc74681d3f353c9c7835b33d689882a3cc5807b

commit 0fc74681d3f353c9c7835b33d689882a3cc5807b
Author: Magnus Jedvert <magjed@google.com>
Date: Tue Apr 14 14:32:23 2015

This fixes a problem when the RenderFrame is destroyed within the context of a getusermedia callback.

BUG=472617, 474370
TBR=tommi@chromium.org

Review URL: https://codereview.chromium.org/1075833002

Cr-Commit-Position: refs/heads/master@{#324434}
(cherry picked from commit fa7c6fd4aa278dab68c5987b45353e064ce8e0ad)

Review URL: https://codereview.chromium.org/1088923004

Cr-Commit-Position: refs/branch-heads/2357@{#82}
Cr-Branched-From: 59d4494849b405682265ed5d3f5164573b9a939b-refs/heads/master@{#323860}

[modify] http://crrev.com/0fc74681d3f353c9c7835b33d689882a3cc5807b/content/renderer/media/user_media_client_impl.cc
[modify] http://crrev.com/0fc74681d3f353c9c7835b33d689882a3cc5807b/content/renderer/media/user_media_client_impl.h
[modify] http://crrev.com/0fc74681d3f353c9c7835b33d689882a3cc5807b/content/renderer/media/user_media_client_impl_unittest.cc


### am...@chromium.org (2015-04-14)

Doesn't look like a 42 merge was requested per c#13, removing Merge-Review tag, please re-apply Merge-Requested if a 42 merge is required.

### ma...@chromium.org (2015-04-15)

Requesting merge to M42.

### la...@google.com (2015-04-15)

[Automated comment] Request affecting a post-stable build (M42), manual review required.

### bu...@chromium.org (2015-04-15)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/0fc74681d3f353c9c7835b33d689882a3cc5807b

commit 0fc74681d3f353c9c7835b33d689882a3cc5807b
Author: Magnus Jedvert <magjed@google.com>
Date: Tue Apr 14 14:32:23 2015


### am...@chromium.org (2015-04-17)

Change is too big for M42, merge rejected.

+timwillis@ - please ping me if you feel this is needed for M42, otherwise it'll ship with M43.

### am...@chromium.org (2015-04-17)

this time +timwillis@ for realz

### ti...@google.com (2015-04-17)

Sure - ideally I'd like to potentially consider it for a M42 patch if there's one later in the cycle, but I won't lose any sleep if this lands in M43.

Marking for M43 release.

### ti...@google.com (2015-05-18)

This should be medium severity - updating labels.

### ti...@google.com (2015-05-28)

Congratulations - $1000 for this report. I'll add it to your tab ;)

### ti...@google.com (2015-06-25)

We'll process this reward via our new payment process which should only take ~1-2 weeks.  

### cl...@chromium.org (2015-07-16)

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

This issue was migrated from crbug.com/chromium/474370?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40081805)*
