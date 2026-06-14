# Occasional heap-use-after-free in non-virtual thunk to AudioDevice::OnStateChanged

| Field | Value |
|-------|-------|
| **Issue ID** | [40054644](https://issues.chromium.org/issues/40054644) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals, Internals>Media |
| **Reporter** | ao...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2012-03-08 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

ASan occasionally reports a heap-use-after-free when opening many pages which usually deal with audio. This is possibly related to the file descriptor bof/uaf mentioned in <https://crbug.com/chromium/115299>, because the sets of files which occasionally trigger this usually also trigger the heap overflow.

**VERSION**  

Chrome Version: 19.0.1061.0 (Developer Build 125107)  

Operating System: Linux (Debian 6.0.4, x86\_64)

**REPRODUCTION CASE**  

Opening the pages in audio.tar.gz in a loop triggers this for me every 10 minutes or so. It usually also hits the file descriptor buffer overflow many times before it. The instructions below should work if you have chrome-asan pointing to a recent ASan build:

$ tar -zxvf audio.tar.gz  

$ cd audio  

$ ./repro.sh

This seems to hit the use-after-free after about 5 minutes on my Core 2 Duo. The machine also went unresponsive in 1 out of 4 tests. Sorry about the messy repro - I tried to get this filed quickly before going mostly offline for a few days.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: ?  

Crash State:

==13194== ERROR: AddressSanitizer heap-use-after-free on address 0x7f51099c0b40 at pc 0x7f511be20802 bp 0x7f5107467ca0 sp 0x7f5107467c98  

READ of size 8 at 0x7f51099c0b40 thread T1  

#0 0x7f511be20802 in non-virtual thunk to AudioDevice::OnStateChanged(AudioStreamState) ???:0  

#1 0x7f511be2ba9e in AudioMessageFilter::OnMessageReceived(IPC::Message const&) ???:0  

#2 0x7f5116fda5ef in IPC::ChannelProxy::Context::TryFilters(IPC::Message const&) ???:0  

#3 0x7f5116fe5562 in IPC::SyncChannel::SyncContext::OnMessageReceived(IPC::Message const&) ???:0  

#4 0x7f5116fcf868 in IPC::Channel::ChannelImpl::DispatchInputData(char const\*, int) ???:0  

#5 0x7f5116fcef0b in IPC::Channel::ChannelImpl::ProcessIncomingMessages() ???:0  

#6 0x7f5116fd3ddd in IPC::Channel::ChannelImpl::OnFileCanReadWithoutBlocking(int) ???:0  

#7 0x7f5116e5d87e in base::MessagePumpLibevent::OnLibeventNotification(int, short, void\*) ???:0  

#8 0x7f5116f93267 in event\_base\_loop ???:0  

#9 0x7f5116e5e06d in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ???:0  

#10 0x7f5116ec3c7e in MessageLoop::RunInternal() ???:0  

#11 0x7f5116ec1e6f in MessageLoop::Run() ???:0  

#12 0x7f5116f3dbdc in base::Thread::ThreadMain() ???:0  

#13 0x7f5116f3421c in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:0  

#14 0x7f511cf67197 in \_\_asan::AsanThread::ThreadStart() ??:0  

0x7f51099c0b40 is located 192 bytes inside of 256-byte region [0x7f51099c0a80,0x7f51099c0b80)  

freed by thread T156 here:  

#0 0x7f511cf61592 in operator delete(void\*) ??:0  

#1 0x7f511c625b54 in media::CompositeFilter::~CompositeFilter() ???:0  

#2 0x7f511c6258ae in media::CompositeFilter::~CompositeFilter() ???:0  

#3 0x7f511c5d6a2c in media::Pipeline::FinishDestroyingFiltersTask() ???:0  

#4 0x7f511c5d26f3 in media::Pipeline::TeardownStateTransitionTask() ???:0  

#5 0x7f5116ec5086 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#6 0x7f5116ec58e6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#7 0x7f5116ec6bcb in MessageLoop::DoWork() ???:0  

#8 0x7f5116ed0fa7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#9 0x7f5116ec3c7e in MessageLoop::RunInternal() ???:0  

#10 0x7f5116ec1e6f in MessageLoop::Run() ???:0  

#11 0x7f5116f3dbdc in base::Thread::ThreadMain() ???:0  

#12 0x7f5116f3421c in base::(anonymous namespace)::ThreadFunc(void\*) base/threading/platform\_thread\_posix.cc:0  

#13 0x7f511cf67197 in \_\_asan::AsanThread::ThreadStart() ??:0  

previously allocated by thread T0 here:  

#0 0x7f511cf61412 in operator new(unsigned long) ??:0  

#1 0x7f511bd5c597 in RenderViewImpl::createMediaPlayer(WebKit::WebFrame\*, WebKit::WebMediaPlayerClient\*) ???:0  

#2 0x7f51188ebb69 in WebKit::WebMediaPlayerClientImpl::loadInternal() ???:0  

#3 0x7f51192f4149 in WebCore::MediaPlayer::loadWithNextMediaEngine(WebCore::MediaPlayerFactory\*) ???:0  

#4 0x7f51192f3155 in WebCore::MediaPlayer::load(WebCore::KURL const&, WebCore::ContentType const&) ???:0  

#5 0x7f5118fee36c in WebCore::HTMLMediaElement::loadResource(WebCore::KURL const&, WebCore::ContentType&) ???:0  

#6 0x7f5118fecffe in WebCore::HTMLMediaElement::selectMediaResource() ???:0  

#7 0x7f5118fdb0e1 in WebCore::HTMLMediaElement::loadTimerFired(WebCore::Timer[WebCore::HTMLMediaElement](javascript:void(0);)\*) ???:0  

#8 0x7f5119269f88 in WebCore::ThreadTimers::sharedTimerFiredInternal() ???:0  

#9 0x7f5116ec5086 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#10 0x7f5116ec58e6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#11 0x7f5116ec6bcb in MessageLoop::DoWork() ???:0  

#12 0x7f5116ed0fa7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#13 0x7f5116ec3c7e in MessageLoop::RunInternal() ???:0  

#14 0x7f5116ec1e6f in MessageLoop::Run() ???:0  

#15 0x7f511bdb3492 in RendererMain(content::MainFunctionParams const&) ???:0  

#16 0x7f5116e1f0e6 in (anonymous namespace)::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:0  

#17 0x7f5116e1d78a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#18 0x7f511561f657 in ChromeMain ??:0  

#19 0x7f511561f5ab in main ???:0  

#20 0x7f510eaefc8d in \_\_libc\_start\_main /home/aurel32/eglibc/eglibc-2.11.3/csu/libc-start.c:260

Thread T1 created by T0 here:  

#0 0x7f511cf61713 in pthread\_create ??:0  

#1 0x7f5116f33ec9 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, unsigned long\*) base/threading/platform\_thread\_posix.cc:0  

#2 0x7f5116f33dca in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate\*, unsigned long\*) ???:0  

#3 0x7f5116f3d4b5 in base::Thread::StartWithOptions(base::Thread::Options const&) ???:0  

#4 0x7f51182708cf in ChildProcess::ChildProcess() ???:0  

#5 0x7f511bd1ca5c in RenderProcessImpl::RenderProcessImpl() ???:0  

#6 0x7f511bdb33d0 in RendererMain(content::MainFunctionParams const&) ???:0  

#7 0x7f5116e1f0e6 in (anonymous namespace)::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:0  

#8 0x7f5116e1d78a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#9 0x7f511561f657 in ChromeMain ??:0  

#10 0x7f511561f5ab in main ???:0  

#11 0x7f510eaefc8d in \_\_libc\_start\_main /home/aurel32/eglibc/eglibc-2.11.3/csu/libc-start.c:260  

Thread T156 created by T0 here:  

#0 0x7f511cf61713 in pthread\_create ??:0  

#1 0x7f5116f33ec9 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate\*, unsigned long\*) base/threading/platform\_thread\_posix.cc:0  

#2 0x7f5116f33dca in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate\*, unsigned long\*) ???:0  

#3 0x7f5116f3d4b5 in base::Thread::StartWithOptions(base::Thread::Options const&) ???:0  

#4 0x7f5116f3d25b in base::Thread::Start() ???:0  

#5 0x7f511c5c3b96 in media::MessageLoopFactory::GetThread(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&) ???:0  

#6 0x7f511c5c39d9 in media::MessageLoopFactory::GetMessageLoop(std::basic\_string<char, std::char\_traits<char>, std::allocator<char> > const&) ???:0  

#7 0x7f511b2dee58 in webkit\_media::WebMediaPlayerImpl::WebMediaPlayerImpl(WebKit::WebFrame\*, WebKit::WebMediaPlayerClient\*, base::WeakPtr<webkit\_media::WebMediaPlayerDelegate>, media::FilterCollection\*, WebKit::WebAudioSourceProvider\*, media::MessageLoopFactory\*, webkit\_media::MediaStreamClient\*, media::MediaLog\*) ???:0  

#8 0x7f511bd5c97a in RenderViewImpl::createMediaPlayer(WebKit::WebFrame\*, WebKit::WebMediaPlayerClient\*) ???:0  

#9 0x7f51188ebb69 in WebKit::WebMediaPlayerClientImpl::loadInternal() ???:0  

#10 0x7f51192f4149 in WebCore::MediaPlayer::loadWithNextMediaEngine(WebCore::MediaPlayerFactory\*) ???:0  

#11 0x7f51192f3155 in WebCore::MediaPlayer::load(WebCore::KURL const&, WebCore::ContentType const&) ???:0  

#12 0x7f5118fee36c in WebCore::HTMLMediaElement::loadResource(WebCore::KURL const&, WebCore::ContentType&) ???:0  

#13 0x7f5118fecffe in WebCore::HTMLMediaElement::selectMediaResource() ???:0  

#14 0x7f5118fdb0e1 in WebCore::HTMLMediaElement::loadTimerFired(WebCore::Timer[WebCore::HTMLMediaElement](javascript:void(0);)\*) ???:0  

#15 0x7f5119269f88 in WebCore::ThreadTimers::sharedTimerFiredInternal() ???:0  

#16 0x7f5116ec5086 in MessageLoop::RunTask(base::PendingTask const&) ???:0  

#17 0x7f5116ec58e6 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) ???:0  

#18 0x7f5116ec6bcb in MessageLoop::DoWork() ???:0  

#19 0x7f5116ed0fa7 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ???:0  

#20 0x7f5116ec3c7e in MessageLoop::RunInternal() ???:0  

#21 0x7f5116ec1e6f in MessageLoop::Run() ???:0  

#22 0x7f511bdb3492 in RendererMain(content::MainFunctionParams const&) ???:0  

#23 0x7f5116e1f0e6 in (anonymous namespace)::ContentMainRunnerImpl::Run() content/app/content\_main\_runner.cc:0  

#24 0x7f5116e1d78a in content::ContentMain(int, char const\*\*, content::ContentMainDelegate\*) ???:0  

#25 0x7f511561f657 in ChromeMain ??:0  

#26 0x7f511561f5ab in main ???:0  

#27 0x7f510eaefc8d in \_\_libc\_start\_main /home/aurel32/eglibc/eglibc-2.11.3/csu/libc-start.c:260  

==13194== ABORTING

Stats: 112M malloced (102M for red zones) by 140506 calls  

Stats: 34M realloced by 5657 calls  

Stats: 110M freed by 125677 calls  

Stats: 0M really freed by 0 calls  

Stats: 240M (61485 full pages) mmaped in 60 calls  

mmaps by size class: 8:131064; 9:8191; 10:16380; 11:4094; 12:3072; 13:2048; 14:1536; 15:640; 16:256; 17:96; 18:144; 19:88;  

mallocs by size class: 8:113352; 9:4190; 10:12453; 11:3842; 12:2213; 13:1889; 14:1459; 15:571; 16:226; 17:93; 18:131; 19:87;  

frees by size class: 8:99752; 9:3578; 10:12032; 11:3721; 12:2180; 13:1872; 14:1446; 15:568; 16:219; 17:91; 18:131; 19:87;  

rfrees by size class:  

Stats: malloc large: 311 small slow: 1615  

Shadow byte and word:  

0x1fea21338168: fd  

0x1fea21338168: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1fea21338148: fa fa fa fa fa fa fa fa  

0x1fea21338150: fd fd fd fd fd fd fd fd  

0x1fea21338158: fd fd fd fd fd fd fd fd  

0x1fea21338160: fd fd fd fd fd fd fd fd  

=>0x1fea21338168: fd fd fd fd fd fd fd fd  

0x1fea21338170: fa fa fa fa fa fa fa fa  

0x1fea21338178: fa fa fa fa fa fa fa fa  

0x1fea21338180: fa fa fa fa fa fa fa fa  

0x1fea21338188: fa fa fa fa fa fa fa fa

## Attachments

- [audio.tar.gz](attachments/audio.tar.gz) (application/x-gzip; charset=binary, 10.7 KB)
- [asan-2.txt](attachments/asan-2.txt) (text/x-c; charset=us-ascii, 9.5 KB)

## Timeline

### in...@chromium.org (2012-03-08)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-08)

Tommi, this looks similar to 115299

### in...@chromium.org (2012-03-08)

Aki, were you able to reproduce these crashes on m17 stable or m18 beta ?

### ao...@gmail.com (2012-03-09)

@inferno I don't have access to build- and test machines at the moment. Based on a quick test with official builds stable didn't crash, beta tabs crashed occasionally and unstable printed "pure virtual method called" with roughly the same interval.

### in...@chromium.org (2012-03-09)

Thanks Aki.

Tommi, m18 is pretty close to release in 2 weeks. We need to make sure to patch this regression.

### sc...@gmail.com (2012-03-09)

@tommi @scherkus -- please confirm receipt of this message :)
cc:ing release manager Karen as it's a release blocker.

### to...@chromium.org (2012-03-09)

receipt confirmed.

Can you tell me if this is something that happens on M18 only or does it also happen on dev or canary? I have been unable to repro.

### in...@chromium.org (2012-03-09)

As Aki said above, it was first tested on 19.0.1061.0 dev. Then in c#4, he tested and found that it affects beta too.

### ao...@gmail.com (2012-03-10)

@tommi Looks like the sad tabs which I saw in official beta builds are a distinct less severe issue. I just built ASan beta (18.0.1025.54), which only reports "crashed on unknown address 0x000000000030". This use-after-free keeps reproducing in my freshly built 19.0.1065.0.

### in...@chromium.org (2012-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-03-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=126048

------------------------------------------------------------------------
r126048 | tommi@chromium.org | Sat Mar 10 12:48:45 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/media/audio_device.cc?r1=126048&r2=126047&pathrev=126048
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/media/audio_input_device.cc?r1=126048&r2=126047&pathrev=126048

Don't dereference the callback_ pointer in OnStateChanged if the device has been shut down.
The reason is that the callback object might have been deleted.

BUG=117335
TEST=See repro steps in bug report.
TBR=xians

Review URL: https://chromiumcodereview.appspot.com/9665039
------------------------------------------------------------------------

### sc...@gmail.com (2012-03-10)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-12)

Aki, Chamal, are you still able to reproduce this bug after r126048  ?

### ao...@gmail.com (2012-03-12)

@inferno Reproduces on 19.0.1067.0 (Developer Build 126099) :( Seemed to take longer, but the repro is too non-deterministic to say for sure.

### to...@chromium.org (2012-03-12)

I think I know what the issue is now and it does make sense that it would take longer.  If I'm right, then there were two problems and I only fixed one of them in my previous cl.  Fix coming shortly.

### ch...@gmail.com (2012-03-12)

Inferno, I also can reproduce the issue still.

### bu...@chromium.org (2012-03-12)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=126147

------------------------------------------------------------------------
r126147 | tommi@chromium.org | Mon Mar 12 09:20:49 PDT 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/media/audio_device.cc?r1=126147&r2=126146&pathrev=126147
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/media/audio_device.h?r1=126147&r2=126146&pathrev=126147
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/media/audio_input_device.h?r1=126147&r2=126146&pathrev=126147
 M http://src.chromium.org/viewvc/chrome/trunk/src/content/renderer/media/audio_input_device.cc?r1=126147&r2=126146&pathrev=126147

Set callback_ to NULL inside Stop.
This prevents a race between Stop() and a kAudioStreamError
status notification that might occur after the callback object has been deleted.

BUG=117335
TEST=See bug description

Review URL: https://chromiumcodereview.appspot.com/9662052
------------------------------------------------------------------------

### to...@chromium.org (2012-03-12)

crossing fingers that this be it.

### ao...@gmail.com (2012-03-12)

Looks good so far. The uaf turned up every 40 or so rounds in 126099, but after applying patches from https://crbug.com/chromium/117335#c17 this hasn't happened so far at 150 rounds. I'll leave it running overnight to be sure.

### al...@chromium.org (2012-03-12)

[Comment Deleted]

### ch...@gmail.com (2012-03-13)

I can still reproduce the issue mentioned by me in 117341.

### ao...@gmail.com (2012-03-13)

LGTM. Only the fd issues turned up after running the original repro a few orders of magnitude longer than it previously took to hit this. Maybe Chamal has another bug or a better repro?

### in...@chromium.org (2012-03-13)

Yes Aki, we have reopened Chamal's https://crbug.com/chromium/117341 for analysis.

### ao...@gmail.com (2012-03-13)

Ah, https://crbug.com/chromium/117341 is the file descriptor uaf mentioned in vulnerability details. It still reproduces also here. The bug this issue was about is fixed.

### sc...@gmail.com (2012-03-14)

Race condition. We're tending towards $500 / Medium for those! Thanks for helping track it down!

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ao...@gmail.com (2012-03-15)

@scarybeasts excellent :)

### ao...@gmail.com (2012-03-28)

@scarybeasts Nearly forgot - this one goes to Red Cross.

### sc...@gmail.com (2012-03-30)

Reward upped to $1337 and donated

### im...@chromium.org (2012-04-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/117335?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Media]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054644)*
