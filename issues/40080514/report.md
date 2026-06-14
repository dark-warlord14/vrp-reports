# Potential UAF at WebCore::TimerBase::setNextFireTime

| Field | Value |
|-------|-------|
| **Issue ID** | [40080514](https://issues.chromium.org/issues/40080514) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink |
| **Reporter** | [Deleted User] |
| **Assignee** | sk...@chromium.org |
| **Created** | 2014-09-22 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36

Steps to reproduce the problem:
1. Launch Chromium.
2. Enter a URL occurring tab crash in omnibox and go to website.
For example:
http://www.lifehacker.jp/
http://itpro.nikkeibp.co.jp/?rt=nocnt
3. Wait for a few seconds until the page loaded completely.
4. A tab will crash (see "Aw, Snap"). If tab crash is not observed, you may need to scroll or hover over the web contents.

What is the expected behavior?
A tab won't crash.

What went wrong?
"Aw, Snap" error is always reproduced every time.

Additional information about the issue:
- Can be reproduced by Both Debug and Release build.
- Can be reproduced since Chromium 37.
- Can NOT be reproduced by 64-bit build.
- Can NOT be reproduced by Official Build (Google Chrome).
- If I blocked javascript or used AdBlock extensions, the issue become not be reproduced. 
- Some Chromium Derivative products like SRWare Iron and ChromiumPortable based on Chromium 37 have become to reproduce the issue.

Crashed report ID: N/A (I use Chromium, not Google Chrome)

How much crashed? Just one tab

Is it a problem with a plugin? No 

Did this work before? No 

Chrome version: 37.0.2062.120 (Developer Build)  Channel: stable
OS Version: Windows 7
Flash Version: 

I built the Chromium with normally format and tested.

The console of windbg says:

eax=77c22e65 ebx=77c22e00 ecx=00000000 edx=00000000 esi=0167a8f8 edi=00000000
eip=77bf015d esp=0449fdb4 ebp=0449ff48 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246
ntdll!NtWaitForMultipleObjects+0x15:
77bf015d 83c404          add     esp,4
3:057> g
(2444.15f4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
*** WARNING: Unable to verify checksum for c:\cygwin\home\chromium\src\out\Release\chrome_child.dll
eax=800ac52e ebx=4147f4bb ecx=2ec51900 edx=20b08380 esi=2ec51900 edi=2ec51900
eip=0f719fc8 esp=002df7f8 ebp=002df80c iopl=0         nv up ei pl nz ac po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210212
chrome_child!WebCore::TimerBase::setNextFireTime+0x48:
0f719fc8 8b4008          mov     eax,dword ptr [eax+8] ds:002b:800ac536=????????
4:066> g
(2444.15f4): Access violation - code c0000005 (!!! second chance !!!)
eax=800ac52e ebx=4147f4bb ecx=2ec51900 edx=20b08380 esi=2ec51900 edi=2ec51900
eip=0f719fc8 esp=002df7f8 ebp=002df80c iopl=0         nv up ei pl nz ac po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210212
chrome_child!WebCore::TimerBase::setNextFireTime+0x48:
0f719fc8 8b4008          mov     eax,dword ptr [eax+8] ds:002b:800ac536=???????? 

Resource viewer highlights the line:

double newTime = alignedFireTime(newUnalignedTime);

## Timeline

### tz...@chromium.org (2014-09-22)

Looks like a UAF of blink::TimerBase around:
https://chromium.googlesource.com/chromium/blink/+/04a2e778948451fb97d2dc7b631a9fd5eb66930c/Source/platform/ThreadTimers.cpp#130

Maybe, the instance deletes itself in line 127.

skyostil@: Is it related to https://codereview.chromium.org/364873002?

### sk...@chromium.org (2014-09-22)

We'll have a look.

### tz...@chromium.org (2014-09-22)

[Empty comment from Monorail migration]

### rs...@chromium.org (2014-09-23)

Seeing this in production on the crash server as well. I don't see any reports from things newer than M37, though. Severity-High for UAF. Full stack:

http://crash/browse?q=Product.Name%20%3D%20%27Chrome%27%20AND%20stable_signature%20CONTAINS%20%27setNextFireTime%27

Thread 0 CRASHED [EXCEPTION_ACCESS_VIOLATION_READ @ 0x00110042] MAGIC SIGNATURE THREAD
0x61695d38	[chrome_child.dll -timer.cpp:379 ]	WebCore::TimerBase::setNextFireTime(double)
0x6177b919	[chrome_child.dll -threadtimers.cpp:131 ]	WebCore::ThreadTimers::sharedTimerFiredInternal()
0x6177b812	[chrome_child.dll -threadtimers.cpp:108 ]	WebCore::ThreadTimers::sharedTimerFired()
0x6177b6d7	[chrome_child.dll -timer.cc:201 ]	base::Timer::RunScheduledTask()
0x615f71b5	[chrome_child.dll -message_loop.cc:450 ]	base::MessageLoop::RunTask(base::PendingTask const &)
0x615f787b	[chrome_child.dll -message_loop.cc:614 ]	base::MessageLoop::DoDelayedWork(base::TimeTicks *)
0x615f8f34	[chrome_child.dll -message_pump_default.cc:36 ]	base::MessagePumpDefault::Run(base::MessagePump::Delegate *)
0x615f680d	[chrome_child.dll -message_loop.cc:400 ]	base::MessageLoop::RunHandler()
0x615f6700	[chrome_child.dll -message_loop.cc:293 ]	base::MessageLoop::Run()
0x6165e6b1	[chrome_child.dll -renderer_main.cc:250 ]	content::RendererMain(content::MainFunctionParams const &)
0x615efc8a	[chrome_child.dll -content_main_runner.cc:416 ]	content::RunNamedProcessTypeMain(std::basic_string<char,std::char_traits<char>,std::allocator<char> > const &,content::MainFunctionParams const &,content::ContentMainDelegate *)
0x615efbe8	[chrome_child.dll -content_main_runner.cc:762 ]	content::ContentMainRunnerImpl::Run()
0x615dbbe3	[chrome_child.dll -content_main.cc:19 ]	content::ContentMain(content::ContentMainParams const &)
0x615db610	[chrome_child.dll -chrome_main.cc:57 ]	ChromeMain
0x00906a0a	[chrome.exe -client_util.cc:314 ]	MainDllLoader::Launch(HINSTANCE__ *)
0x00906435	[chrome.exe -chrome_exe_main_win.cc:114 ]	wWinMain
0x0092837d	[chrome.exe -crt0.c:251 ]	__tmainCRTStartup
0x750bee1b	[kernel32.dll + 0x0004ee1b ]	BaseThreadInitThunk
0x776437ea	[ntdll.dll + 0x000637ea ]	__RtlUserThreadStart
0x776437bd	[ntdll.dll + 0x000637bd ]	_RtlUserThreadStart

### rs...@chromium.org (2014-09-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-09-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/1810bb5cec9026c64fc34fbbb8fafd01263241d2

commit 1810bb5cec9026c64fc34fbbb8fafd01263241d2
Author: skyostil <skyostil@chromium.org>
Date: Fri Sep 26 10:48:48 2014

Disable forwarding tasks to the Blink scheduler

Disable forwarding tasks to the Blink scheduler to avoid some
regressions which it has introduced.

BUG=391005,415758,415478,412714,416362,416827,417608
TBR=jamesr@chromium.org

Review URL: https://codereview.chromium.org/609483002

Cr-Commit-Position: refs/heads/master@{#296916}

[modify] https://chromium.googlesource.com/chromium/src.git/+/1810bb5cec9026c64fc34fbbb8fafd01263241d2/content/renderer/render_thread_impl.cc


### in...@chromium.org (2014-09-29)

Looks like this was forgotten to be closed.

### cl...@chromium.org (2014-09-29)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### sk...@chromium.org (2014-09-29)

Sorry, that was a speculative revert. Let's see if this was fixed or not.

### al...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### sk...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-06)

alexclarke@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### al...@chromium.org (2014-10-08)

This is still occurring after the revert in https://crbug.com/chromium/416362#c6.  I notice asan complains about a memcpy-param-overlap when running http://www.lifehacker.jp/ but that's in a bunch of code I'm not familiar with.

Our suspect is this is not scheduler related, so I'm unassigning myself.

### cl...@chromium.org (2014-10-10)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-10-12)

It seems like there were two separate issues here. Is the setNextFireTime crash still reproducing on M-38?

### cl...@chromium.org (2014-10-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-10-24)

Please open a new bug for the memcpy-overlap issue with the stacktrace. since this is not related to scheduler stuff, closing.

### in...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### wf...@chromium.org (2014-11-14)

this bug doesn't seem fixed to me, I still see a few crashes on same line as https://crbug.com/chromium/416362#c1 beyond r296916 - was there another CL related to this?

### wf...@chromium.org (2014-11-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-14)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-19)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-19)

[Empty comment from Monorail migration]

### lg...@chromium.org (2014-11-20)

ClusterFuzz is still complaining about the lack of an owner. :-(

skyostil@chromium.org: Could you figure out if this still needs work (and/or if there's anyone it should go to)?

### cl...@chromium.org (2014-11-22)

You have far exceeded the 60-day deadline for fixing this high severity security vulnerability.

We commit ourselves to this deadline and appreciate your utmost priority on this issue.

If you are unable to look into this soon, please find someone else to own this.

- Your friendly ClusterFuzz

### pi...@chromium.org (2014-11-24)

Can someone add some background here... where did this bug come from and why has it been assigned to us? Is it scheduler related? Does this still occur? Do we need to make anyone else aware that it is happening?

### [Deleted User] (2014-11-25)

Hi, all. Thank you for good helps on this issue. I am a first reporter for this. This bug seemed to be about WebCore::TimerBase::setNextFireTime but not to be blink scheduler related.
In the first place, M-37 hasn't implemented a blink scheduler, so it's expected to be something related to blink since M-37? I'm glad that someone find or become a new owner good about blink. I still confirm page crash issue reproduced on M-38, M-39 and later same as mentioned in #1.

### in...@chromium.org (2014-12-19)

This issue is still occuring in M40. e.g. https://crash.corp.google.com/browse?q=Product.Name%20%3D%20%27Chrome%27%20AND%20stable_signature%20CONTAINS%20%27setNextFireTime%27%20AND%20product.version%3D%2741.0.2243.0%27&stbtiq=&reportid=c79c84cfc126718e&index=1

Dominicc, you fixed something in this function in https://code.google.com/p/chromium/issues/detail?id=247310#c3. If you know this code, can you please take a look at this one.

### do...@chromium.org (2014-12-25)

I'm on low bandwidth until 12/30 but I'm happy to help after that.

Context: the issue I fixed was a worker/main thread race assigning timer IDs. This could be related if the timer heap relies on sequential (and not merely increasing) heap IDs (but I don't think that it does rely on that.)

@tzik (https://crbug.com/chromium/416362#c1) where is the timer deleted on line 127? I think that just deletes a pointer to the timer from the heap, not the timer itself.

### tz...@chromium.org (2015-01-05)

Hm, looks like it was not true.
Since we read/write a variable before l127 without crash, I thought it was alive at that point.

### tz...@chromium.org (2015-01-05)

BTW, we are comparing two doubles on x86 CPU.
Don't we hit the trap of 80-bit extended precision of double on the register?

At Timer.cpp:377, if
 * oldTime is a 64-bit double and its value is 0,
 * newTime is a 80-bit double and has a smaller value than the smallest positive value of 64-bit double,
then oldTime != newTime will be true, and following updateHeapIfNeeded will add the timer with m_nextFireTime == 0.
That can make duplicated TimerBase entry in the timerHeap that causes UAF.

### do...@chromium.org (2015-01-06)

Interesting theory. There are comments in time_win.cc that indicate that time has variable resolution and as much as 15.5ms. I wonder if we end up in some situation where n * minimum interval (4ms) is very close to timeGetTime resolution and we end up truncating some delta.

### do...@chromium.org (2015-01-06)

OK, I have stared at this all day and I'm at a bit of a loss. I think it's time to add unittests to platform/Timer. It might also be helpful to stop using 0 as a flag for things like "not repeating" and represent that explicitly. We could also have the timer heap consistency checks check that all of the timers in a heap are for the same thread.

### tz...@chromium.org (2015-01-06)

Sounds nice!

### do...@chromium.org (2015-01-07)

I think this is not Windows-specific. It's informative to search for crashes in sharedTimerFiredInternal. I see 24 crashes in Android 39.0.2171.93 in sharedTimerFiredInternal on the line that calls setNextFireTime. Looking around at sharedTimerFiredInternal crashes generally it looks like the timer heap is corrupt?

I wondered if this had something to do with DOMTimer specifically, since that's the timer with non-trivial "alignment" and suspension, but here's an instance of the crash with:

XMLHttpRequestProgressEventThrottle 431ee8bb04c59480
Timer<CompositorPendingAnimations> 85f83a9c996d0344

### in...@chromium.org (2015-01-07)

No more M39 patches, moving to M40.

### js...@chromium.org (2015-02-12)

Any progress? This has crept up to the top of our stale security bugs list, and unfortunately has completely blown past our normal fix deadline. So, it's becoming a bit urgebnt that we get a fix in.

### do...@chromium.org (2015-02-13)

Not from me; I think we need more data. How would you feel about me adding some release asserts that the timer heap is accessed from the right thread and some consistency checks?

### js...@chromium.org (2015-02-13)

Sounds good to me.

### do...@chromium.org (2015-02-17)

Assigning this to me because I seem to have more cycles than skyostil for it right now. Feel free to poach back. Plan of attack--get more data:

- Stop using 0.0 as special value for non-repeating or whatever (https://crbug.com/chromium/416362#c37)
- Add debug assertions about which pointers are in the timer heap (https://crbug.com/chromium/416362#c35)
- Add assertions about not accessing timers and the heap it's in across threads (")

### do...@chromium.org (2015-02-17)

/https://crbug.com/chromium/416362#c35/https://crbug.com/chromium/416362#c42/

### sk...@chromium.org (2015-02-17)

Thanks for picking this up Dominic.

### ti...@google.com (2015-02-17)

Updating target milestone (M40 is out and M41 is too close).

### ti...@google.com (2015-02-25)

dominicc: any progress here? (re: https://crbug.com/chromium/416362#c44). Grateful for an update, even if that update is no progress.

### do...@chromium.org (2015-02-26)

No progress. I was travelling a lot last week, this week. I should have something today or early next week. (I'm out Friday.)

### do...@chromium.org (2015-02-27)

WIP up at https://codereview.chromium.org/959263002 I am pulling timer's heap-related stuff into its own place to start to rationalize consistency checks.

### al...@chromium.org (2015-02-27)

I'm not sure if this is related, but on the off chance:  I was re-factoring TimerBase to post delayed tasks to the chromium run loop and discovered that sometimes Documents are created but the destructor is not always called when running the webkit_unit_tests.  This results in timers still on the heap where the BaseTimer is pointing to deleted memory.

This might be a problem peculiar to webkit_unit_tests but in case it's not I thought I'd let you know.   An example of this is TEST(ImageResourceTest, MultipartImage) which loads an SVG which results in a document being created but nothing takes ownership of it, and it gets leaked.

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/WebKit/Source/core/svg/graphics/SVGImage.cpp&sq=package:chromium&q=SVGImage::dataChanged&type=cs&l=432  

### do...@chromium.org (2015-03-04)

Thanks for the pointer, I'll investigate. It would certainly be bad to not be destructing documents in the wild.

Quick update: Refactoring and adding assertions ongoing at https://codereview.chromium.org/959263002

Still pretty messy.

I've pulled the stuff related to being in the timer heap into its own type.

Now whenever the "next fire time" changes, it notifies the heap. I don't think this always happened while firing timers.

Similarly, the timer heap manages notifying the thread shared timer when the next-firing timer has changed.

That notification happens through a role interface, so it will be possible to write unit tests.

When popping the heap we set a flag on the entry being popped to make it artificially minimum, instead of dinking with the fire time.

Some things I'm still working on:

The TimerBase, TimerHeapEntry factoring isn't right. Either TimerHeapEntry should become the base type of TimerBase (useful, because it sequesters off the essentials of "next fire time" and that the queue of timer needs); OR TimerBase gets to hold a TimerHeapEntry transiently instead of always having a TimerHeapEntry with parts that are only valid when its in the heap.

0 is still used as a magic value for "no next firing time". My gut feeling is that should be represented explicitly.

Reflecting on this code, "Timer" is a sadly overloaded word. There are lots of abstractions that are unarguably timers (DOMTimer, etc.) However break open the abstraction, and they are built of things that are the "real" timers (the thread shared timer.) Whether something is scheduled or not, and when it will fire next, is a Big Deal for TimerBase, etc. I almost think we need an object to represent a "TimerFiring" or something. That's what TimerHeapEntry is, basically.

### do...@chromium.org (2015-03-09)

Timers are being refactored along these lines: https://docs.google.com/a/chromium.org/document/d/163ow-1wjd6L0rAN3V_U6t12eqVkq4mXDDjVaA4OuvCA/edit#heading=h.qctgo8bntg2p

So the clean-up I was pursuing will mostly be subsumed by that.

Producing the refactoring didn't point to any smoking guns although the lead in https://crbug.com/chromium/416362#c51 is worth investigating.

### ti...@google.com (2015-04-08)

@dominicc - just like an over-eager doctor, I'm here for your monthly checkup. Did you end up pursuing the lead in #51?

### do...@chromium.org (2015-04-09)

Not yet.

### al...@chromium.org (2015-04-09)

FYI, I hope to be able to submit https://codereview.chromium.org/956333002/ (or possibly a slimmed down version) in the next week or so (some chromium side plumbing to do first).  I'm not sure how that will affect the UFA bugs, likely the stack traces will change and if we're lucky we might get some more information to help narrow this down.

### do...@chromium.org (2015-04-24)

I think I can rule out recursion in setNextFireTime as a cause of these crashes; most only have one setNextFireTime on the stack.

https://crash.corp.google.com/dremel_query_ui?q=SELECT%20g.product.name%2C%20g.product.version%2C%20g.ncalls%2C%20COUNT(*)%0AFROM%20(%0A%20%20SELECT%20product.name%2C%20product.version%2C%20SUM(CrashedStackTrace.StackFrame.FunctionName%20CONTAINS%20%27setNextFireTime%27)%20WITHIN%20RECORD%20AS%20ncalls%0A%20%20FROM%20crash.prod.latest%0A%20%20WHERE%20product.version%20%3E%20%2730%27%0A%20%20OMIT%20RECORD%20IF%20(SUM(CrashedStackTrace.StackFrame.FunctionName%20CONTAINS%20%27setNextFireTime%27)%20%3D%200)%0A)%20AS%20g%0AGROUP%20BY%201%2C%202%2C%203%0AORDER%20BY%202%20DESC%2C%201%2C%203

### ti...@google.com (2015-05-08)

@alexclarke - re: #56, are you likely to submit before M44 branch (end of next week)?

### sk...@chromium.org (2015-05-11)

Alex is currently out and I'm working on landing his patch here: https://codereview.chromium.org/1134523002/

There are a number of patches that need to land before that so it's not guaranteed to make M44.

### fe...@chromium.org (2015-05-18)

thanks skyostil@. it's unusual for a high-severity bug to stay open this long so we (security folks) appreciate you picking this up

### bu...@chromium.org (2015-05-21)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195706

------------------------------------------------------------------
r195706 | skyostil@chromium.org | 2015-05-21T17:11:46.132711Z

Changed paths:
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.h?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/CachingCorrectnessTest.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=195706&r2=195705&pathrev=195706
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/Platform.h?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/TextFinderTest.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/Init.cpp?r1=195706&r2=195705&pathrev=195706
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollableAreaTest.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/animation/CompositorAnimationsTestHelper.h?r1=195706&r2=195705&pathrev=195706
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.h?r1=195706&r2=195705&pathrev=195706
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.h?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/TimerTest.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMTimerCoordinator.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceTest.cpp?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.h?r1=195706&r2=195705&pathrev=195706
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/blink_platform.gypi?r1=195706&r2=195705&pathrev=195706
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.cpp?r1=195706&r2=195705&pathrev=195706

Implement timers by posting delayed tasks

This patch refactors TimerBase to post tasks delayed tasks and
deletes the now-obsolete timer heap and shared timer mechanism.

ATTN Sheriffs: If there are weird layout test flakes all of a
sudden, this patch may be the cause since the interleaving of
timers with other posted tasks will change.

Original patch by Alex Clarke <alexclarke@chromium.org>.

BUG=463143,416362,480522

Review URL: https://codereview.chromium.org/1134523002
-----------------------------------------------------------------

### sk...@chromium.org (2015-05-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-21)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=195725

------------------------------------------------------------------
r195725 | jchaffraix@chromium.org | 2015-05-21T20:01:06.743418Z

Changed paths:
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.cpp?r1=195725&r2=195724&pathrev=195725
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.h?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/CachingCorrectnessTest.cpp?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=195725&r2=195724&pathrev=195725
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.cpp?r1=195725&r2=195724&pathrev=195725
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.cpp?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/Init.cpp?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/Platform.h?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/TextFinderTest.cpp?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/animation/CompositorAnimationsTestHelper.h?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollableAreaTest.cpp?r1=195725&r2=195724&pathrev=195725
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.h?r1=195725&r2=195724&pathrev=195725
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.h?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.cpp?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/TimerTest.cpp?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMTimerCoordinator.cpp?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceTest.cpp?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.h?r1=195725&r2=195724&pathrev=195725
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/blink_platform.gypi?r1=195725&r2=195724&pathrev=195725

Revert of Implement timers by posting delayed tasks (patchset #18 id:340001 of https://codereview.chromium.org/1134523002/)

Reason for revert:
The patch made some content_browsertests fail on Linux:
DomSerializerTests.SerializeHTMLDOMWithDocType
DomSerializerTests.SerializeHTMLDOMWithEmptyHead
DomSerializerTests.SerializeHTMLDOMWithEntitiesInText
DomSerializerTests.SerializeHTMLDOMWithMultipleMetaCharsetInOriginalDoc
DomSerializerTests.SerializeHTMLDOMWithNoMetaCharsetInOriginalDoc
DomSerializerTests.SerializeHTMLDOMWithoutDocType
RenderFrameHostManagerTest.DisownOpener

Original issue's description:
> Implement timers by posting delayed tasks
> 
> This patch refactors TimerBase to post tasks delayed tasks and
> deletes the now-obsolete timer heap and shared timer mechanism.
> 
> ATTN Sheriffs: If there are weird layout test flakes all of a
> sudden, this patch may be the cause since the interleaving of
> timers with other posted tasks will change.
> 
> Original patch by Alex Clarke <alexclarke@chromium.org>.
> 
> BUG=463143,416362,480522
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=195706

TBR=jochen@chromium.org,alexclarke@chromium.org,erikcorry@chromium.org,kinuko@chromium.org,rmcilroy@chromium.org,skyostil@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=463143,416362,480522

Review URL: https://codereview.chromium.org/1151633004
-----------------------------------------------------------------

### mb...@chromium.org (2015-05-21)

[Empty comment from Monorail migration]

### sk...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/022f550d73963aa4ce245aeaa0515504d89b2e24

commit 022f550d73963aa4ce245aeaa0515504d89b2e24
Author: skyostil <skyostil@chromium.org>
Date: Fri May 22 17:14:47 2015

scheduler: Allow timer task to be nested

Blink's current shared timer mechanism, which we are trying to replace,
allows timers to execute in nested message loops, but only if the
nested message loop itself was not initiated by a timer. We believe
this limitation is a historical relic which was originally introduced
to prevent multiple invocations of the same timer[1].

When the shared timer is replaced by indivially posted tasks, the
underlying scheduler will ensure that each task is only executed once.
Therefore it should be safe to lift this restriction.

[1] https://trac.webkit.org/changeset/12774

BUG=463143,416362,480522

Review URL: https://codereview.chromium.org/1153763005

Cr-Commit-Position: refs/heads/master@{#331133}

[modify] http://crrev.com/022f550d73963aa4ce245aeaa0515504d89b2e24/components/scheduler/child/web_scheduler_impl.cc


### mb...@chromium.org (2015-05-22)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-29)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196152

------------------------------------------------------------------
r196152 | skyostil@chromium.org | 2015-05-29T15:08:17.797118Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMTimerCoordinator.cpp?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceTest.cpp?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.h?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/blink_platform.gypi?r1=196152&r2=196151&pathrev=196152
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.cpp?r1=196152&r2=196151&pathrev=196152
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.h?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=196152&r2=196151&pathrev=196152
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.cpp?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/Platform.h?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/TextFinderTest.cpp?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/Init.cpp?r1=196152&r2=196151&pathrev=196152
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.cpp?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollableAreaTest.cpp?r1=196152&r2=196151&pathrev=196152
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.h?r1=196152&r2=196151&pathrev=196152
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.h?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.cpp?r1=196152&r2=196151&pathrev=196152
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/TimerTest.cpp?r1=196152&r2=196151&pathrev=196152

Implement timers by posting delayed tasks

This patch refactors TimerBase to post tasks delayed tasks and
deletes the now-obsolete timer heap and shared timer mechanism.

ATTN Sheriffs: If there are weird layout test flakes all of a
sudden, this patch may be the cause since the interleaving of
timers with other posted tasks will change.

Original patch by Alex Clarke <alexclarke@chromium.org>.

BUG=463143,416362,480522

Review URL: https://codereview.chromium.org/1134523002
-----------------------------------------------------------------

### sk...@chromium.org (2015-05-29)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-05-29)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196169

------------------------------------------------------------------
r196169 | mnaganov@chromium.org | 2015-05-29T21:00:45.083038Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.cpp?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/TimerTest.cpp?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMTimerCoordinator.cpp?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceTest.cpp?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.h?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/blink_platform.gypi?r1=196169&r2=196168&pathrev=196169
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.cpp?r1=196169&r2=196168&pathrev=196169
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.h?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=196169&r2=196168&pathrev=196169
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.cpp?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/Platform.h?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/TextFinderTest.cpp?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/Init.cpp?r1=196169&r2=196168&pathrev=196169
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.cpp?r1=196169&r2=196168&pathrev=196169
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollableAreaTest.cpp?r1=196169&r2=196168&pathrev=196169
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.h?r1=196169&r2=196168&pathrev=196169
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.h?r1=196169&r2=196168&pathrev=196169

Revert "Implement timers by posting delayed tasks"

This reverts commit 334040f6e54d29d7890b6f409354cd234b29c24b.

Reason: Breaks GN test:

http://build.chromium.org/p/tryserver.chromium.linux/builders/linux_chromium_gn_rel/builds/93666/steps/html_viewer_unittests%20%28with%20patch%29/logs/stdio

These tests are only built on GN bots, which absent on Blink canary waterfall.

BUG=463143,416362,480522
TBR=jochen@chromium.org,kinuko@chromium.org,skyostil@chromium.org

Review URL: https://codereview.chromium.org/1162753003
-----------------------------------------------------------------

### sk...@chromium.org (2015-06-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-06-02)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196308

------------------------------------------------------------------
r196308 | skyostil@chromium.org | 2015-06-02T11:00:17.565768Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.cpp?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/TimerTest.cpp?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMTimerCoordinator.cpp?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceTest.cpp?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.h?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/blink_platform.gypi?r1=196308&r2=196307&pathrev=196308
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.cpp?r1=196308&r2=196307&pathrev=196308
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.h?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=196308&r2=196307&pathrev=196308
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.cpp?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/Platform.h?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/TextFinderTest.cpp?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/Init.cpp?r1=196308&r2=196307&pathrev=196308
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.cpp?r1=196308&r2=196307&pathrev=196308
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollableAreaTest.cpp?r1=196308&r2=196307&pathrev=196308
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.h?r1=196308&r2=196307&pathrev=196308
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.h?r1=196308&r2=196307&pathrev=196308

Implement timers by posting delayed tasks

This patch refactors TimerBase to post tasks delayed tasks and
deletes the now-obsolete timer heap and shared timer mechanism.

ATTN Sheriffs: If there are weird layout test flakes all of a
sudden, this patch may be the cause since the interleaving of
timers with other posted tasks will change.

Original patch by Alex Clarke <alexclarke@chromium.org>.

BUG=463143,416362,480522

Review URL: https://codereview.chromium.org/1134523002
-----------------------------------------------------------------

### bu...@chromium.org (2015-06-02)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196317

------------------------------------------------------------------
r196317 | skyostil@chromium.org | 2015-06-02T14:26:02.706603Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.cpp?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/TimerTest.cpp?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMTimerCoordinator.cpp?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceTest.cpp?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.h?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/blink_platform.gypi?r1=196317&r2=196316&pathrev=196317
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.cpp?r1=196317&r2=196316&pathrev=196317
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.h?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=196317&r2=196316&pathrev=196317
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.cpp?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/Platform.h?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/TextFinderTest.cpp?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/Init.cpp?r1=196317&r2=196316&pathrev=196317
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.cpp?r1=196317&r2=196316&pathrev=196317
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollableAreaTest.cpp?r1=196317&r2=196316&pathrev=196317
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.h?r1=196317&r2=196316&pathrev=196317
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.h?r1=196317&r2=196316&pathrev=196317

Revert of Implement timers by posting delayed tasks (patchset #21 id:400001 of https://codereview.chromium.org/1134523002/)

Reason for revert:
Reverting once again because this makes ScriptContextSetTest.LifeCycle leak:

http://build.chromium.org/p/tryserver.chromium.linux/builders/linux_chromium_asan_rel_ng/builds/12840/steps/extensions_unittests%20%28with%20patch%29/logs/stdio

The reason is that many of these tests do things backwards: they first initialize Blink and then create a message loop. This means we can't create a real scheduler for Blink and have to jump through hoops to make things work. We could extend this mock scheduler to properly clean things up, but I think I'll instead try to get rid of the mock scheduler completely.

Original issue's description:
> Implement timers by posting delayed tasks
> 
> This patch refactors TimerBase to post tasks delayed tasks and
> deletes the now-obsolete timer heap and shared timer mechanism.
> 
> ATTN Sheriffs: If there are weird layout test flakes all of a
> sudden, this patch may be the cause since the interleaving of
> timers with other posted tasks will change.
> 
> Original patch by Alex Clarke <alexclarke@chromium.org>.
> 
> BUG=463143,416362,480522
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=196308

TBR=alexclarke@chromium.org,erikcorry@chromium.org,jochen@chromium.org,kinuko@chromium.org,rmcilroy@chromium.org,sigbjornf@opera.com,jchaffraix@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=463143,416362,480522

Review URL: https://codereview.chromium.org/1162903005
-----------------------------------------------------------------

### bu...@chromium.org (2015-06-04)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196497

------------------------------------------------------------------
r196497 | skyostil@chromium.org | 2015-06-04T13:11:02.605486Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/TimerTest.cpp?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.cpp?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMTimerCoordinator.cpp?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceTest.cpp?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.h?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/blink_platform.gypi?r1=196497&r2=196496&pathrev=196497
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.cpp?r1=196497&r2=196496&pathrev=196497
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.h?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=196497&r2=196496&pathrev=196497
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.cpp?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/Platform.h?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/TextFinderTest.cpp?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/Init.cpp?r1=196497&r2=196496&pathrev=196497
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.cpp?r1=196497&r2=196496&pathrev=196497
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollableAreaTest.cpp?r1=196497&r2=196496&pathrev=196497
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.h?r1=196497&r2=196496&pathrev=196497
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.h?r1=196497&r2=196496&pathrev=196497

Implement timers by posting delayed tasks

This patch refactors TimerBase to post tasks delayed tasks and
deletes the now-obsolete timer heap and shared timer mechanism.

ATTN Sheriffs: If there are weird layout test flakes all of a
sudden, this patch may be the cause since the interleaving of
timers with other posted tasks will change.

Original patch by Alex Clarke <alexclarke@chromium.org>.

BUG=463143,416362,480522

Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=196308

Review URL: https://codereview.chromium.org/1134523002
-----------------------------------------------------------------

### bu...@chromium.org (2015-06-05)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196552

------------------------------------------------------------------
r196552 | yutak@chromium.org | 2015-06-05T04:28:23.903125Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/blink_platform.gypi?r1=196552&r2=196551&pathrev=196552
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.cpp?r1=196552&r2=196551&pathrev=196552
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.h?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=196552&r2=196551&pathrev=196552
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.cpp?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/Platform.h?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/TextFinderTest.cpp?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/Init.cpp?r1=196552&r2=196551&pathrev=196552
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.cpp?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollableAreaTest.cpp?r1=196552&r2=196551&pathrev=196552
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.h?r1=196552&r2=196551&pathrev=196552
   A http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.h?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.cpp?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/TimerTest.cpp?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMTimerCoordinator.cpp?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceTest.cpp?r1=196552&r2=196551&pathrev=196552
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.h?r1=196552&r2=196551&pathrev=196552

Revert of Implement timers by posting delayed tasks (patchset #22 id:420001 of https://codereview.chromium.org/1134523002/)

Reason for revert:
Broke ASAN and blocking Blink rolls.
http://build.chromium.org/p/tryserver.chromium.linux/builders/linux_chromium_asan_rel_ng/builds/13967


Original issue's description:
> Implement timers by posting delayed tasks
> 
> This patch refactors TimerBase to post tasks delayed tasks and
> deletes the now-obsolete timer heap and shared timer mechanism.
> 
> ATTN Sheriffs: If there are weird layout test flakes all of a
> sudden, this patch may be the cause since the interleaving of
> timers with other posted tasks will change.
> 
> Original patch by Alex Clarke <alexclarke@chromium.org>.
> 
> BUG=463143,416362,480522
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=196308
> 
> Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=196497

TBR=alexclarke@chromium.org,erikcorry@chromium.org,jochen@chromium.org,kinuko@chromium.org,rmcilroy@chromium.org,sigbjornf@opera.com,jchaffraix@chromium.org,skyostil@chromium.org
NOPRESUBMIT=true
NOTREECHECKS=true
NOTRY=true
BUG=463143,416362,480522

Review URL: https://codereview.chromium.org/1167023002
-----------------------------------------------------------------

### bu...@chromium.org (2015-06-05)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=196595

------------------------------------------------------------------
r196595 | skyostil@chromium.org | 2015-06-05T18:30:09.849273Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/scroll/ScrollableAreaTest.cpp?r1=196595&r2=196594&pathrev=196595
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.h?r1=196595&r2=196594&pathrev=196595
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.h?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/TimerTest.cpp?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.cpp?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/frame/DOMTimerCoordinator.cpp?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/fetch/ResourceTest.cpp?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/Timer.h?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/platform/blink_platform.gypi?r1=196595&r2=196594&pathrev=196595
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.cpp?r1=196595&r2=196594&pathrev=196595
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/ThreadTimers.h?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.cpp?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/workers/WorkerThread.h?r1=196595&r2=196594&pathrev=196595
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/PlatformThreadData.cpp?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/public/platform/Platform.h?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/web/tests/TextFinderTest.cpp?r1=196595&r2=196594&pathrev=196595
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/Init.cpp?r1=196595&r2=196594&pathrev=196595
   D http://src.chromium.org/viewvc/blink/trunk/Source/platform/SharedTimer.cpp?r1=196595&r2=196594&pathrev=196595

Implement timers by posting delayed tasks

This patch refactors TimerBase to post tasks delayed tasks and
deletes the now-obsolete timer heap and shared timer mechanism.

ATTN Sheriffs: If there are weird layout test flakes all of a
sudden, this patch may be the cause since the interleaving of
timers with other posted tasks will change.

Original patch by Alex Clarke <alexclarke@chromium.org>.

BUG=463143,416362,480522

Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=196308

Committed: https://src.chromium.org/viewvc/blink?view=rev&revision=196497

Review URL: https://codereview.chromium.org/1134523002
-----------------------------------------------------------------

### sk...@chromium.org (2015-06-11)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-31)

Updating severity for release notes.

### ti...@google.com (2015-08-31)

Congratulations - Our reward panel has decided to award you $2,000 for this report!

Panel notes: $2,000 for this report. For the $3,000 level, you would need to provide a minimized POC with your report.

We shall credit you in the Chrome release notes as "taro.suzuki.dev". Please let me know if you would like to use a different name.

Our finance team should be in contact with you this week. If that doesn't happen or you have any questions, please either update this bug or reach out to me directly at timwillis@

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************


### ti...@google.com (2015-09-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-17)

Bulk update: removing view restriction from closed bugs.

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

### aw...@google.com (2018-06-08)

The reward for this report is being donated to the Against Malaria Foundation :-)

### is...@google.com (2018-06-08)

This issue was migrated from crbug.com/chromium/416362?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/418510]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080514)*
