# UNKNOWN in WebKit::WebSpeechRecognitionHandle::operator WTF::PassRefPtr<WebCore::SpeechRecognition>

| Field | Value |
|-------|-------|
| **Issue ID** | [40078145](https://issues.chromium.org/issues/40078145) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Speech |
| **Reporter** | ta...@talater.com |
| **Assignee** | rs...@chromium.org |
| **Created** | 2013-09-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Bug and exploit demoed, including a total browser crash: <http://www.youtube.com/watch?v=WbEP7irlBzE>

There is currently an issue with Chrome's webkitSpeechRecognition that causes it to randomly stop from time to time... A common trick to combat this, is to attach a function to webkitSpeechRecognition's onend event, making it restart itself.  

The problem is, that when you have more than one webkitSpeechRecognition instance using this trick in the browser, they will fight each other, each restarting itself, which will end the other one, causing it to restart, ending the original, and so on in an endless loop.

When this happens, Chrome will start using up all available CPU. I've seen it go up from around 4% CPU to over 180% the second I opened a second tab. It will sometimes even crash the current tab, or even crash the browser completely (see the youtube link above for me crashing the browser with it.)

This can happen without malicious intent, by the user opening two or more sites with webkitSpeechRecognition, or when opening the same site in two or more tabs (very common).

EXPLOITABILITY  

This can easily be used by a malicious user to cause a user's machine to become unstable, unusable, and even crash his browser completely, which is why I've filed this as a security issue.

It can even be done with just one tab:  

One tab can run n+ webkitSpeechRecognition instances and have them compete with each other, causing the machine to become immediately unstable.  

Just run this in your web developer tools console for instant fun:  

var recognition = new webkitSpeechRecognition();  

recognition.onend = function() {  

window.console.log('end');  

recognition.start();  

};  

recognition.start();  

var recognition2 = new webkitSpeechRecognition();  

recognition2.onend = function() {  

window.console.log('end');  

recognition2.start();  

};  

recognition2.start();

**VERSION**  

Verified in 4 Chrome versions between 26 and 31, in two operating systems:  

Chrome Version 29.0.1547.65 Stable + 31.0.1639.0 canary  

Operating System: OS X 10.8.5

Chrome Version: 26.0.1410.64 Stable + 29.0.1547.76 Stable  

Operating System: Windows XP SP3.

**REPRODUCTION CASE**  

Attached are three files showing this in action.  

onend\_start.html is the naive case... This case might happen when a user opens two tabs with webkitSpeechRecognition... open this in two different tabs or windows to see the bug.  

onend\_double.html is an exploit... A malicious user can include this script in a page to make the user's machine unresponsive, and crash.  

onend\_mega.html is the vicious exploit... A malicious user can include this script in a page to make the user's machine melt.  

Any of the above files will cause it to use up all available CPU, and sometimes crash the tab or the entire browser.  

Loading the samples as file:// and not http:// or https:// will cause it to crash the tab every single time... But it will crash the browser/tab from https and http as well, just not every time.

You can also see these samples online:  

<http://talater.com/chrome_speechrecognition_exploits/onend_start.html>  

<http://talater.com/chrome_speechrecognition_exploits/onend_start_double.html>  

<http://talater.com/chrome_speechrecognition_exploits/onend_start_mega.html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab + browser  

Client ID: 7CB1E024-D2C1-6D62-AC62-9F7E56EE6037  

Attached to this report is "Google Chrome\_2013-09-23-010534\_Tals-MacBook-Pro-2.crash" which is from the total browser crash shown in the video above.

## Attachments

- [onend_start_double.html](attachments/onend_start_double.html) (text/html; charset=us-ascii, 474 B)
- [onend_start_mega.html](attachments/onend_start_mega.html) (text/html; charset=us-ascii, 338 B)
- [Google Chrome_2013-09-23-010534_Tals-MacBook-Pro-2.crash](attachments/Google Chrome_2013-09-23-010534_Tals-MacBook-Pro-2.crash) (text/plain; charset=us-ascii, 84.2 KB)
- [onend_start.html](attachments/onend_start.html) (text/html; charset=us-ascii, 292 B)
- [trace.zip](attachments/trace.zip) (application/zip; charset=binary, 9.1 MB)
- [exploit_start.html](attachments/exploit_start.html) (text/html; charset=us-ascii, 294 B)

## Timeline

### ia...@chromium.org (2013-09-24)

In a debug build onend_start_double.html hits the following DCHECK:

FATAL:speech_recognition_dispatcher.cc(240) Check failed: iter != handle_map_.end(). 

CC'ing Blink-Speech team

### cl...@chromium.org (2013-09-24)

ClusterFuzz is now working on this testcase. See https://cluster-fuzz.appspot.com/testcase?key=5317365805875200

### jw...@chromium.org (2013-09-24)

Hans, can you please take a look at this potential security issue? Thanks!

### ha...@chromium.org (2013-09-25)

+tommi who owns speech, and +primiano who might also have some ideas

This seems to be an unfortunate consequence of the way we're handling multiple scripts trying to do speech recognition, where a new session cancels an old one.

I guess a hacky way of solving this is to enforce some time has to elapse between starting consecutive sessions from a renderer :/

### cl...@chromium.org (2013-09-25)

ClusterFuzz thinks that this bug might be eligible for a reward! Forwarding to reward panel for consideration.

### cl...@chromium.org (2013-09-25)

Adding milestone and impact labels.

### cl...@chromium.org (2013-09-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5317365805875200

Uploader: jww@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  WebKit::WebSpeechRecognitionHandle::operator WTF::PassRefPtr<WebCore::SpeechRecognition>
  WebKit::SpeechRecognitionClientProxy::didReceiveError
  content::SpeechRecognitionDispatcher::OnErrorOccurred
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=191189:191323

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97TL-lmcqKaEi9Qx7hnnbTeBsyZyPnriz16sa9f3USkqD-SQipDLBQhjO853diO4zJlGLnEINmPKwnFKT9VVtjnnDmB_Mgd_36A25fvUp4L6LmbZKOA1xMhketitv2WNdt5_EnWOYY9z9Z5EWc8uQ5jK1k_zw



### ha...@chromium.org (2013-09-25)

> I guess a hacky way of solving this is to enforce some time has to elapse between starting consecutive sessions from a renderer :/

We could do this in SpeechRecognitionDispatcherHost::OnStartRequest(), which could make sure to only allow a small number of requests per second, and otherwise drop them or just send an error back directly.

This would solve the problem about making the browser unresponsive, but it doesn't explain why we crash.

### ta...@talater.com (2013-09-25)

By the way, I've noticed that this issue can also happen with just one window, and just one auto restarting webkitSpeechRecognition. If you run http://talater.com/chrome_speechrecognition_exploits/onend_start.html and deny it access, it will also enter the same vicious cycle.

Thanks @ClusterFuzz 

### pr...@chromium.org (2013-09-25)

I am not surprised at all about the fact that we can burn CPU cycles with a few lines of javascript by using Web Speech API. After all, it is not that different than doing the same by looping back events with any other js API (e.g. http://jsfiddle.net/dKAWP/). 
Hans: I don't think we should bother throttling requests, unless we want to talk about a slightly different issue*, which is IMHO out of the scope of this bug. CPU usage is not an issue at all in my opinion (unless we start hogging the entire browser and not only the tab, which is another story).

On the other side, while burning CPU cycles and making the renderer unresponsive is, in my viewpoint, absolutely fine, it is unacceptable that the renderer, or even worse, the entire browser crashes. I think that this bug makes clear that there is a race (or more than one) somewhere and this should be fixed soon. I couldn't reproduce the browser crash, however it seems to happen in the attached youtube video, and it worries me.
In my opinion this is something that should be seriously looked at.

Who is looking into this bug?

In the meantime, many thanks to Tal for the very accurate and detailed report. We much appreciate it. +1 for the reward.

[*] There is a more subtle issue related here: the fairness and the possibility of different tabs to interfere each other. Speech is a shared resource (with respect of multiple renderers potentially using that) which can be used only in exclusive mode (due to the nature of speech recognition). How do we arbitrate simultaneous accesses to this shared resource? I raised my concerns about the race-for-speech starvations in many occasions, e.g., https://code.google.com/p/chromium/issues/detail?id=238800#c19 without any luck.

### pr...@chromium.org (2013-09-25)

Update: I noted that, wile running the attached onend_start_mega.html (when the renderer desperately loops taking as much CPU as it can), that the memory usage of the browser process grows indefinitely.
Therefore I have the strong suspect that the reason why the browser crashed in the attached video after some time is for out-of-memory (which makes me feel a bit better in terms of security).

Concluding, taking a quick look at this, it looks like we have at least two problems here:
1) There is a race somewhere in the renderer, which causes the renderer to crash  (repro: just by clicking on "Deny" in the media permission infobar)
2) There is a memory leak somewhere in the browser, which causes the browser process working set to grow indefinitely.

P.S. very curious and unrelated funny note: I've just realized that the WebSocket jsfiddle code snippet I wrote in my previous post manages to crash the renderer in recent canary builds. Filed crbug.com/298060. We should start looking more thoroughly to loops :/

### in...@chromium.org (2013-09-25)

Did you saw our new criteria for possibly issuing higher rewards? See http://www.chromium.org/Home/chromium-security/vulnerability-rewards-program/reward-nomination-process
E.g. If you are able to provide a repro that faulted at an address of 0x41414141, it will qualify for the new higher rewards. Or, if you can show that you have control between free and crash points, etc.

### ta...@talater.com (2013-09-25)

@inferno - I'll do what I can, but I'm afraid I may not know enough about this field to find what you've asked for...
I am doing more research on how to track down more info, as well as how to use AddressSanitizer to provide more details, but if you could provide me with some more detailed info on what you might be looking for, I will gladly use that as the starting point for further research on the subject.

### ia...@chromium.org (2013-09-26)

@primiano:

The renderer crash is caused by the browser process calling SpeechRecognitionDispatcherHost::OnRecognitionEnd followed by SpeechRecognitionDispatcherHost::OnRecognitionError in that order for the same request_id.

On the renderer end these translate to calls to SpeechRecognitionDispatcher::OnRecognitionEnded then SpeechRecognitionDispatcher::OnErrorOccurred.

OnRecognitionEnded will erase the entry for the request_id from the handle_map:
  handle_map_.erase(request_id);

OnErrorOccurred is then called with the same request_id which was just erased; it calls GetHandleFromID:

const WebSpeechRecognitionHandle& SpeechRecognitionDispatcher::GetHandleFromID(
    int request_id) {
  HandleMap::iterator iter = handle_map_.find(request_id);
  DCHECK(iter != handle_map_.end());
  return iter->second;
}

Since the request_id was just erased from the map the find(request_id) returns handle_map_.end(). In a release build the DCHECK doesn't apply so GethandleFromID returns whatever handle_map_.end()->second is (this depends on the implementation of map; it isn't necessarily always NULL and so I wouldn't rule out exploitability just yet.) This is then interpreted as a WebSpeechRecognitionHandle, which is really just a refcounted pointer: later on this reference count is manipulated and the value returned by GetHandleFromID is dereferenced to access the refcount and we crash :) You can verify this by running the testcase in a debug build where you will see the DCHECK failing after a short time.

The underlying cause of the issue is I imagine a bug in the state machine which causes OnRecognitionError to be called after OnRecognitionEnd for the same request_id. I am not familiar with this code though, maybe you have more insight?

### pr...@chromium.org (2013-09-27)

Many thanks for the catch! All you say makes sense, especially if you hit that DCHECK.
Nothing should never ever come after a OnRecognitionEnd event (for a given session id). And the speech_recognition_manager_impl should guarantee it.

This is very well documented in https://code.google.com/p/chromium/codesearch#chromium/src/content/public/browser/speech_recognition_event_listener.h&l=63

My guess at this point is that there has been some change which causes a OnRecognitionError to be thrown after an OnRecognitionEnded.
I have the suspicion that is has something to do with the "not allowed error" coming from the infobar when denying the recognition (in fact I can easilly trigger the crash by clicking on deny in the attached demo), but I need to check for further details.
Any help would be more than appreciated in the meanwhile, as my bandwidth in these weeks is over-saturated :/

### jw...@chromium.org (2013-09-27)

It seems that this is a Windows issue only, but please correct the labeling if I'm wrong about that.

### ta...@talater.com (2013-09-27)

@jww - I'm able to reproduce both the renderer crash, and the memory leak on OSX. The video in my original post actually shows this in OSX and WinXP.

### pr...@chromium.org (2013-09-27)

As visible from the video attached and from the report details it reproduces also on Mac OS X. 
I have personally reproduced on Mac OS X and Linux.
So, I'm afraid this involved all OSes.

### ta...@talater.com (2013-09-27)

OK, it's been a long day learning how to build Chromium from source, and running various tests but I hope the following helps:

I am definitely seeing some sort of memory problem. Looking at HEAP allocations while running one of my demos, there seems to be an issue with abandoned memory, which I believe is caused by it opening more and more threads, and never closing them.

The following was run on Chrome Stable 29.0.1547.65 on OSX 10.8.5
http://youtu.be/CTxwy7gFrXI

It shows mallocs being opened and then staying alive... After about a minute and a half I am seeing the following:
https://www.evernote.com/shard/s8/sh/075b490d-b708-4f25-9943-05d49dd366dc/2773cc95a1d2900d259d3d083eb32572/deep/0/Instruments1.png
The mallocs there just keep growing indefinitely, many of them staying alive.

I don't know if it helps, but these ones seem to be most common:
Address,     Category,        Responsible Library,     Responsible Caller
0x86c298c0,  Malloc 32 Bytes, Google Chrome Framework, 0x2ca0370
0x5ee742e0,  Malloc 32 Bytes, Google Chrome Framework, 0x2d14800
0x5ee66b90,  Malloc 32 Bytes, Google Chrome Framework, 0x2c9c2e0
0x5ee8ea90,  Malloc 32 Bytes, Google Chrome Framework, 0x2c9fdf0
0x5ee66a80,  Malloc 32 Bytes, Google Chrome Framework, 0x2ca0850
0x5ee879e0,  Malloc 32 Bytes, Google Chrome Framework, 0x2ca0890
0x5ee87a00,  Malloc 32 Bytes, Google Chrome Framework, 0x2c9da10
0x774677a0,  Malloc 64 Bytes, libstdc++.6.dylib,       std::string::_Rep::_S_create(unsigned long, unsigned long, std::allocator<char> const&)
0x63f67a70,  Malloc 16 Bytes, Google Chrome Framework, 0x7cede0
0x65c009e0,  Malloc 144 Bytes,Google Chrome Framework, 0x2c9c2e0
0x6bc76510,  Malloc 448 Bytes,Google Chrome Framework, 0x35a070



Looking at the event profiler, it also grows indefinitely as time goes by...  Digging into it, shows that most of it originates with thread_starts.

Samples # Self    Symbol Name
7203   20.3%  7203    __read
6735   19.0%  0    0x7cafc0
6735   19.0%  0     0x7f7da0
6735   19.0%  0      0x7f7b80
6735   19.0%  0       0x2cae530
6735   19.0%  0        0x2cae2e0
6735   19.0%  0         0x2d26800
6735   19.0%  0          0x2d28cd0
6735   19.0%  0           0x588800
6735   19.0%  0            0x7e24c0
6735   19.0%  0             0x7e29e0
6735   19.0%  0              0x7ac2a0
6735   19.0%  0               0x7e22a0
6735   19.0%  0                0x7f7f20
6735   19.0%  0                 0x7e2020
6735   19.0%  0                  0x80c6c0
6735   19.0%  0                   0x2b98500
6735   19.0%  0                    0x2b98530
6735   19.0%  0                     0x80c6e0
6735   19.0%  0                      0x808920
6735   19.0%  0                       _pthread_start
6735   19.0%  0                        thread_start
0       0.0%  0                         _pthread_start  0xd39c0
2389    6.7%  2389    mach_msg_trap
2389    6.7%  0    mach_msg
1596    4.5%  0     __CFRunLoopServiceMachPort
1596    4.5%  0      __CFRunLoopRun
1596    4.5%  0       CFRunLoopRunSpecific
1596    4.5%  0        CFRunLoopRunInMode
1596    4.5%  0         RunCurrentEventLoopInMode
1596    4.5%  0          ReceiveNextEventCommon
1596    4.5%  0           BlockUntilNextEventMatchingListInMode
1596    4.5%  0            _DPSNextEvent
1596    4.5%  0             -[NSApplication nextEventMatchingMask:untilDate:inMode:dequeue:]
1596    4.5%  0              -[NSApplication run]
1596    4.5%  0               0x7ad1f0
1596    4.5%  0                0x7acde0
1596    4.5%  0                 0x7e22a0
1596    4.5%  0                  0x7f7f20
1596    4.5%  0                   0x219c30
1596    4.5%  0                    0x2b8cff0
1596    4.5%  0                     0x2b8db00
1596    4.5%  0                      0x2b89950
1596    4.5%  0                       0x6c13f0
1596    4.5%  0                        0x6c1fe0
1596    4.5%  0                         0x6c12d0
1596    4.5%  0                          ChromeMain
1596    4.5%  0                           main
1596    4.5%  0                            0x9af20
0       0.0%  0                             Main Thread  0xd3996
793    2.2% 0     CFRunLoopWakeUp
793    2.2% 0      0x7ace80
793    2.2% 0       0x7e1c50
793    2.2% 0        0x7e1e90
506    1.4% 0         0x2b98810
506    1.4% 0          0x2b98a70
293    0.8% 0           0x2cb2b10
293    0.8% 0            0x2cafa10
293    0.8% 0             0x2cae2e0
293    0.8% 0              0x2d26800
293    0.8% 0               0x2d28cd0
293    0.8% 0                0x588800
293    0.8% 0                 0x7e24c0
293    0.8% 0                  0x7e29e0
293    0.8% 0                   0x7ac2a0
293    0.8% 0                    0x7e22a0
293    0.8% 0                     0x7f7f20
293    0.8% 0                      0x7e2020
293    0.8% 0                       0x80c6c0
293    0.8% 0                        0x2b98500
293    0.8% 0                         0x2b98530
293    0.8% 0                          0x80c6e0
293    0.8% 0                           0x808920
293    0.8% 0                            _pthread_start
293    0.8% 0                             thread_start
0      0.0% 0                              _pthread_start  0xd39c0
1566    4.4%  1566    kevent
1566    4.4%  0    0x81c6b0
1566    4.4%  0     0x81a160
1566    4.4%  0      0x7ac2a0
1566    4.4%  0       0x7e22a0
1566    4.4%  0        0x7f7f20
1566    4.4%  0         0x7e2020
1566    4.4%  0          0x80c6c0
1566    4.4%  0           0x2b98500
1566    4.4%  0            0x2b98530
1566    4.4%  0             0x80c6e0
1566    4.4%  0              0x808920
1566    4.4%  0               _pthread_start
1566    4.4%  0                thread_start
0       0.0%  0                 _pthread_start  0xd39c0


Digging more into events shows more thread_start evidence:
https://www.evernote.com/shard/s8/sh/78fc87c0-abf6-4ab1-b5d4-880bd117551f/008600f571e9769184ef85180fd2f421/deep/0/Instruments4.png

#    Timestamp      Thread                            Core  Time        State         Reason        Priority
1    00:00.795.137  _pthread_start            0xd39ba   3   8.86 s      Blocked       Yielded CPU         46
2    00:00.795.571  _pthread_start            0xd39bf   6   8.86 s      Blocked       Yielded CPU         46
3    00:00.861.050  _pthread_start            0xd39c5   2   8.80 s      Blocked       Yielded CPU         46
4    00:03.859.840  _dispatch_mgr_thread2     0xd39a4   2   5.80 s      Blocked       Yielded CPU         48
5    00:03.860.556  _dispatch_worker_thread2  0xd9aa7   6   5.80 s      Blocked       Yielded CPU         44
6    00:00.821.071  _pthread_start            0xd39bc   4   5.77 s      Blocked       Yielded CPU         46
7    00:06.593.924  _pthread_start            0xd39c4   7   3.06 s      Blocked       Yielded CPU         46
8    00:07.589.594  _pthread_start            0xd39cc   0   2.07 s      Blocked       Yielded CPU         46
9    00:07.590.559  _pthread_start            0xd39bc   0   2.07 s      Blocked       Yielded CPU         46
10   00:07.591.165  _pthread_start            0xd39cb   4   2.07 s      Blocked       Yielded CPU         46
11   00:02.273.151  _pthread_start            0xd39c0   2   1.45 s      Supervisor    System trap (start) 46
12   00:02.273.143  Main Thread               0xd3996   4   1.45 s      Supervisor    System trap (start) 57
13   00:00.988.306  Main Thread               0xd3996   0   1.08 s      Supervisor    System trap (start) 57
14   00:00.988.330  _pthread_start            0xd39c0   6   1.08 s      Supervisor    System trap (start) 46
15   00:06.592.160  _pthread_start            0xd39cc   1   997.34 ms   Blocked       Yielded CPU         46
16   00:06.594.045  _pthread_start            0xd39bc   2   995.67 ms   Blocked       Yielded CPU         46
17   00:03.959.886  Main Thread               0xd3996   2   805.37 ms   Supervisor    System trap (start) 45
18   00:03.959.888  _pthread_start            0xd39c0   4   805.35 ms   Supervisor    System trap (start) 28
19   00:09.054.572  _pthread_start            0xd39f5   3   602.48 ms   Blocked       Yielded CPU         46
20   00:08.523.483  _pthread_start            0xd39f5   2   530.94 ms   Blocked       Yielded CPU         46
21   00:09.203.304  Main Thread               0xd3996   0   452.69 ms   Supervisor    System trap (start) 57
22   00:09.203.300  _pthread_start            0xd39c0   6   452.54 ms   Supervisor    System trap (ended) 46
23   00:05.407.050  Main Thread               0xd3996   6   416.26 ms   Supervisor    System trap (start) 57
24   00:05.407.046  _pthread_start            0xd39c0   0   416.26 ms   Running       System trap (ended) 46
25   00:08.097.165  Main Thread               0xd3996   2   352.24 ms   Running       System trap (ended) 57
26   00:08.097.166  _pthread_start            0xd39c0   6   352.00 ms   Supervisor    System trap (start) 46
27   00:06.046.123  Main Thread               0xd3996   0   340.08 ms   Supervisor    System trap (start) 57
28   00:06.046.298  _pthread_start            0xd39c0   2   339.83 ms   Supervisor    System trap (start) 46
29   00:08.672.029  Main Thread               0xd3996   6   308.40 ms   Supervisor    System trap (start) 57
30   00:08.672.113  _pthread_start            0xd39c0   0   308.32 ms   Supervisor    System trap (start) 46


All the traces are also attached to this messages.

Please let me know if this helps at all or not, or if there is anything else I can help with.


### ta...@talater.com (2013-09-27)

Traces from previous message.

### pr...@chromium.org (2013-09-28)

Hmm I think we are barfing at the wrong tree here Chromium codebase is very huge and approaching it with a memory profiler might be a bit overwhelming. :)

The number of threads we have should be constant (or at least bounded) with respect of the operations that we make on the renderer.
What you are seeing there in your traces is the call stack of the pending allocations which have not been freed yet. The reasons why you see _pthread_start in all the call stacks is because simply *every thread begins with _pthread_start*, so it will be always present in all the traces you will have (unless you don't have a stack trace which is deeper than the tracer record level, which is typically 32).
On the other side, you are missing most of the symbols (the 0x1234.. that you are seeing in your trace). Those symbols (especially the topmost ones) contain the much valuable information about the latest method which allocated memory. _pthread_start is just the common ancestor (and the only one for which you seem to have symbols, since it is a system library).

By the way, I don't think we need a lot of symbols or tracing for identifying the memory leak.
The memory leak here does not sound to me to be a thread issue (unless you see hundreds of threads).
I strongly think that the point in which we leak memory is this one:
https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/speech/speech_recognition_manager_impl.cc&l=100

In other words, every time a recognition is requested it is appended to a session table, which keeps around all its information. The session is removed whenever the tab is closed or the recognition ends.
In theory, however, every time a new recognition starts, the outstanding ones should be removed from the table and freed (here https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/speech/speech_recognition_manager_impl.cc&l=163)
However, it looks like for some reason they are not freed. My suspicion is that the infobar confirmation (i.e. Allow/Deny) for some reasons keeps the session around, and that line (abort if primary_session_id_ != session_id) is never hit.
Whatever the cause is, by the way, this is a clearly bug, because we are accumulating memory in the browser process. 

Now that the experimental speech API for speech extensions has been removed and that the concurrent semantics of the x-webkit-speech bubble have been relaxed, the sessions_ table should never ever contain more than one element (effectively, we don't need it at all anymore).

Thanks for the time spent for the report by the way, I guess that just getting the sources and building took some non negligible amount of time!

### ta...@talater.com (2013-09-29)

OK, I was trying to go based on @inferno's suggestions. Is there another thing I can do to help?

> you are missing most of the symbols (the 0x1234..
> that you are seeing in your trace). Those symbols
> (especially the topmost ones) contain the much
> valuable information about the latest method which
> allocated memory. 

Do you mean this: http://is.gd/rG7bAS

> My suspicion is that the infobar confirmation
> (i.e. Allow/Deny) for some reasons keeps the
> session around

Then why does this bug still occur when a user denies the permission request? The info bar no longer opens, but the bug still occurs.

> the sessions_ table should never ever contain more
> than one element

Won't this prevent the page from having more than one "listener"? This may be enough for now, but in the future when SpeechRecognition is more prevalent, doesn't it make sense that a page will be using more than one library to listen, similar to sites that use more than one library for animation, etc. Each in charge of a specific effect (eg a site navigation "listener" + a map control "listener" inside a google maps widget).


### pr...@chromium.org (2013-09-29)

+xians who worked on the media infobar for Web Speech.

> Do you mean this: http://is.gd/rG7bAS
Nope, as you can see in that backtarces, for most levels you can see only the addresses (e.g. 0x7b8fc0 etc. below _read) which are really meaningless. The symbol files (in Windows) are .lib files which, in the very essence, are tables which map those addresses to the equivalent method names and source line information (file.cc:123). If you did a local build you should have your .lib files in the \out folder. Typically you have to instruct the debugger/tracer and sets its "symbol path" to the directory containing symbols (C:\chromium\src\out\Debug\ or similar) so it can lookup those files and resolve symbols while debugging/tracing.

By the way, as regards the leak, I have the final confirmation. I did some debugging today and the leak happens here: https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/renderer_host/media/media_stream_manager.cc&rcl=1380450401&l=195

In essence the onend_start_mega.html creates a bazilion speech recogniton requests. The requests themselves are handled fine in the speech recognition manager (I doublechecked and the SpeechRecognitionManagerImpl is keeping alive only one session, aborting all the others as expected). However the MediaStreamManager requests are never cleaned up, and accumulate (in the browser proc.) causing the OOM.
I wrote a CL which should fix this out-of-memory issue here: http://crrev.com/25045007

> Then why does this bug still occur when a user denies the permission request?
As I said in #11, there are two different issues you found in this bug. The leak is just one of the two problems and will be fixed by the aforementioned CL.
The tab, instead, crashes for a race. ianbeer@ made a very thorough analysis in #14. I need to check the details of the FSM in the next days to see what's happening.

> Won't this prevent the page from having more than one "listener"?
If you want more listeners, you should attach them to the same webkitSpeechRecognition object, not having more objects.

> This may be enough for now, but in the future when SpeechRecognition is more prevalent, doesn't it make sense that a page will be using more than one library to listen.
To be honest, from an engineering perspective, I find this use case a bit odd. You mean having two speech recognizer which capture audio from the same source and produce potentially different results at different times?

> Each in charge of a specific effect (eg a site navigation "listener" + a map control "listener" inside a google maps widget).
I understand the need of having >1 listeners, but, again, this problem should be addressed in JS multiplexing the events coming from the speech recognizer object. Requiring the Web Speech API to allow more than one recognizer to be active at the same time sounds exactly like asking your smartphone to make and handle actively two phone calls at the same time.

### bu...@chromium.org (2013-09-30)

------------------------------------------------------------------------
r225985 | primiano@chromium.org | 2013-09-30T15:41:07.620554Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/speech/speech_recognition_manager_impl.cc?r1=225985&r2=225984&pathrev=225985

Web Speech API: cancel outstanding infobar requests when aborting.

This CL enforces the cancellation of outstanding media requests
for speech recognition sessions which are aborted before getting
the media request approval (i.e. before the user clicks on the
Allow/Deny media access request infobar).

BUG=296690

Review URL: https://codereview.chromium.org/25045007
------------------------------------------------------------------------

### in...@chromium.org (2013-09-30)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-09-30)

Adding Merge-Requested label.

Please do not merge your patch without first checking with the release manager. Once the merge is approved by the release manager, make sure to merge the fix to all the affected branches, i.e stable, beta and trunk (near branch point). Look for the branch information on omahaproxy.appspot.com.

If this fix is not applicable for merge, change this label to Merge-NA.

- Your friendly ClusterFuzz

### cl...@chromium.org (2013-09-30)

[Empty comment from Monorail migration]

### pr...@chromium.org (2013-10-01)

Why this bug has been marked as fixed?
The change that I submitted did just fix the memory leak.
As per my last comment in #23 we still need to address the renderer crash.

### aa...@google.com (2013-10-01)

Sorry about that. Fixing labels.

### cl...@chromium.org (2013-10-01)

Fixing milestone and impact labels.

### pr...@chromium.org (2013-10-01)

There we go, this is the fix for the render crash: http://crrev.com/25550003/
I tried it only on Linux and it seems to fix the renderer crash.
I'll try on Windows tomorrow.
The MediaRequestPermission infobar has introduced a very subtle race. The details about the race are available in the CL description.

===== A little post-mortem of this issue =====
- The exploit provided by Tal has brought to life two different issues in the Web Speech API implementation: an out-of-memory in the browser process and a crash in the renderer.
- As long as I could see there were no UAF or invalid memory accesses in the browser process.
- However, the fact that this exploit didn't end-up in any invalid memory accesses in the browser process was mostly a lucky accident (see details below). It could have been much worse.
- The London office tends to become tremendously warm around 11PM after A/C goes off :-)

===== More technical details =====
Fortunately the classes inside the browser process were robust enough to tolerate double aborts.
Again, this was mostly by (very lucky) accident. It is not expected by design and should not be relied on.
As clearly stated in the speech_recognition_manager.h header [1] the S.R. Manager is in charge of protecting all the implementation of the Web Speech API (e.g. speech_recognizer_impl, engines, ecc).
The S.R. Manager is the front-end which faces the evil world (IPCs from the evil renderer) and must always guarantee that, in any case, all the remaining classes of the Web Speech API work in ideal conditions.
For instance, double-aborting is not an ideal condition.
(It is very funny, though, that in [1] the comment says: "...taking into account also call sequences that might not make sense, e.g., two subsequent AbortSession calls". Fact: two subsequent AbortSession calls was exactly what happened here).

===== Some broader personal considerations =====
This is the third security bug affecting the S.R. Manager in the last six months after the changes to the MediaRequestPermission infobar (prev: crbug.com/244415 and crbug.com/252848).
Just to be clear, I am not trying to blame anyone here (seriously).
If all this happened it was definitely also my bad for not having enough (D)CHECKS in the original code and (definitely not enough) tests.
Furthermore. this API implementation comes from a very unfortunate history, many people left/moved in the same timeframe while new requirements and many deadlines arose.

However, I think that it is evident, at this point, that a refactoring of the S.R. Manager would be beneficial to avoid similar issues in future.
My personal humble advice (we might have a dedicated discussion if you think it's the case) is that the S.R. Manager should use the (already existing) FSM to keep track of the asynchronous completion of the security checks and the infobar.
Keeping track of asynchronous state by hopping on the call stack and using variables placed here and there is IMHO intractable and very prone to bugs. Just to be less academic and more practical, I think that the current start sequence of the S.R. manager is pretty emblematic:

SpeechRecognitionManagerImpl::StartSession
  ChromeSpeechRecognitionManagerDelegate::CheckRecognitionIsAllowed
  (*** Switch to UI Thread ***)
  ChromeSpeechRecognitionManagerDelegate::CheckRenderViewType
    (*** Switch back to IO Thread ***)
    SpeechRecognitionManagerImpl::RecognitionAllowedCallback
      MediaStreamManager::MakeMediaAccessRequest
        SpeechRecognitionManagerImpl::MediaRequestPermissionCallback
          SpeechRecognitionManagerImpl::RecognitionAllowedCallback (*** Again? Reentrant!*** )
            SpeechRecognitionManagerImpl::DispatchEvent(EVENT_START) (Finally, we got there)

My personal opinion is that this call stack should be simplified. While keeping the behavior untouched, all the state of a S.R. session should be moved to and handled exclusively in the manager FSM (which is a very nice and easier to handle single-thread linearization). It would require a bit of refactoring efforts, though.

Kind regards,
Primiano

[1] https://code.google.com/p/chromium/codesearch#chromium/src/content/public/browser/speech_recognition_manager.h&l=19


### pr...@chromium.org (2013-10-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-10-02)

------------------------------------------------------------------------
r226523 | primiano@chromium.org | 2013-10-02T19:22:28.344049Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/speech/speech_recognition_manager_impl.cc?r1=226523&r2=226522&pathrev=226523
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/browser/speech/speech_recognition_manager_impl.h?r1=226523&r2=226522&pathrev=226523

Web Speech API: Fix a race condition causing renderer crash.

The introduction of the MediaRequestPermission (i.e. infobar) has
opened a race window which causes a recognition session to be aborted
twice, causing a consequent crash on the renderer.
The race window is the following:
1) Session 1 is started (SpeechRecognitionManagerImpl::StartSession)
2) Security checks for session 1 are started asynchronously
   (delegate_->CheckRecognitionIsAllowed).
3) Session 2 is started. This causes an immediate abort of session 1.
4) The oustanding security check for session 1 completes and returns
   a nack. The nack causes an abort of session 1 (in
   RecognitionAllowedCallback). However, session 1 was already aborted
   in 3).
5) The double abort is not tolerated by the renderer, which crashes.

This CL closes the race window with a not-so-elegant fix.
A refactoring of the speech_recognition_manager_impl.cc is STRONGLY
adviced (Hint: use and extend the already existing FSM to keep track
of the asynchronous completion of security checks. Don't introduce
extra state with extra variables).

BUG=296690,116954

Review URL: https://codereview.chromium.org/25550003
------------------------------------------------------------------------

### ke...@chromium.org (2013-10-02)

primiano@: Thanks for that. Does this fix the browser hang as well or is another CL necessary for that?

### pr...@chromium.org (2013-10-02)

I tried right now on Windows and I confirm that both the OOM and the renderer crash are fixed with these two CLs.
As regards the CPU usage: there was never a proper browser hang, as there is nothing which stalls completely either the browser or the renderer.
However, it is true that with the onend_start_mega.html exploit, there is a non negligible amount of CPU time spent on both browser and renderer. This is due to the the IPC traffic than must be dispatched and handled, even for not doing anything useful.
The browser is still usable, however the slowdown is noticeable (at least on a standard laptop).

To be honest, I don't know if we should do something in this regard inside the Web Speech API implementation (following hans@ suggestion #4 for instance) or at a broader level. I can reproduce very similar behaviors using many other JS APIs and following the same pattern Tal has used in his exploit (i.e. short-circuit events to hog IPC communication).
I would really appreciate your honest feedback on this point.
It is not really a technical issue. If we decide to to this on our side, it is just a few lines change, a matter of replacing a PostTask with a PostDelayedTask. I am not sure that this is the right thing to do, though.
Maybe we should start a discussion on chromium-dev.

What do you think?

In the meantime I would mark the security bug as fixed, unless Tal has other findings after r226523.
Thanks for the collaboration.

### ta...@talater.com (2013-10-02)

In my original "mega exploit", I was running many instances side by side in order to prove a point of the severity of the bug... but if the core reason behind it is indeed solved by these latest commits, then I completely agree with @primiano that any slowdown left in this script now is just... well... (intentionally) inefficient JavasSripting, and not a real issue.

As for limiting the number of consecutive sessions that can be opened per second (suggestion #4), I believe that might be a good strategy (and maybe even not just for SpeechRecognition). I've actually implemented just such a limiter in my own SpeechRecognition library - annyang (https://www.talater.com/annyang/)

There were quite a few bugs related to the security check which I've ran into, not all of them have been detailed above yet.

I am currently rebuilding Chromium from the latest revision, and will hopefully be able to also confirm them all as fixed in a few hours... if not, I will update here, or open separate bugs as needed.

### cl...@chromium.org (2013-10-03)

Adding Merge-Requested label.

Please do not merge your fix without first checking with the release manager. 

Once the merge is approved by the release manager, make sure to merge the fix to all the affected branches, i.e stable, beta and trunk (near branch point). You can find branch information on omahaproxy.appspot.com.

If the fix does not merge cleanly or is too risky on uptake on these branches, please change the M-* label to indicate the next milestone.

- Your friendly ClusterFuzz

### ta...@talater.com (2013-10-03)

I've rebuilt using r226603, and actually found the browser to be *a lot* more crashy: http://youtu.be/n5FwaIhVzTU
In fact I am now experiencing very consistent total browser crashes with the exploit urls listed above.

I am not familiar with your svn flow, so let me just make sure... If I have an up to date svn wc on my machine (r226614), and I build using "ninja -C out/Release chrome" I should be getting the latest build with your fixes, right? I even looked in the source code of the files you changed on my local working copy, and they included your fixes.

Am I missing something?

### pr...@chromium.org (2013-10-03)

Hmm my suspicion is that it is not "more crashy". Just now it's being hitting something else when the recognition is allowed. In the video looks like it crashes only after clicking allow.
My bad, I didn't test the Allow code path. I'll take a look to it in the next days.
Reopening the bug.

### pr...@chromium.org (2013-10-04)

It looks like http://crrev.com/25045007 fixed the memory leak but now created a regression (crashing browser). The repro steps are visible in the video, I am able to reproduce 100% on Mac OS X.

I am not familiar with the infobar code (that's why I'm passing to xians) and I can't see anything particularly wrong being called on the speech classes.

Xians: It looks like when "Allow" is pressed, the UI tries to call Accept() on the MediaStreamInfoBarDelegate.
However the MediaStreamInfoBarDelegate instance is gone at that point, because it looks like to be destroyed together with web_contents (the infobar is attached to WebContents in MediaStreamInfoBarDelegate::Create) and we end up in a UaF.
In essence it looks like that the infobar UI outlives the webcontents even when they are destroyed.

Can you take a look?

Below there's the UaF stack trace I get on Mac.

Program received signal EXC_BAD_ACCESS, Could not access memory.
Reason: KERN_INVALID_ADDRESS at address: 0x42100008
0x08625b88 in -[ConfirmInfoBarController ok:] (self=0x21e97660, _cmd=0x91ba258b, sender=0x1b3b5bb0) at ../../chrome/browser/ui/cocoa/infobars/confirm_infobar_controller.mm:22
22        if ([self delegate]->AsConfirmInfoBarDelegate()->Accept())
(gdb) bt
#0  0x08625b88 in -[ConfirmInfoBarController ok:] (self=0x21e97660, _cmd=0x91ba258b, sender=0x1b3b5bb0) at ../../chrome/browser/ui/cocoa/infobars/confirm_infobar_controller.mm:22
#1  0x95f545d3 in -[NSObject performSelector:withObject:] ()
#2  0x91400ad2 in -[NSApplication sendAction:to:from:] ()
#3  0x004ff582 in -[BrowserCrApplication sendAction:to:from:] (self=0x1b04ad60, _cmd=0x91b75f9d, anAction=0x91ba258b, aTarget=0x21e97660, sender=0x1b3b5bb0) at ../../chrome/browser/chrome_browser_application_mac.mm:412
#4  0x914008e0 in -[NSControl sendAction:to:] ()
#5  0x914007ef in -[NSCell _sendActionFrom:] ()
#6  0x913fed60 in -[NSCell trackMouse:inRect:ofView:untilMouseUp:] ()
#7  0x913fe59f in -[NSButtonCell trackMouse:inRect:ofView:untilMouseUp:] ()
#8  0x913fdcb9 in -[NSControl mouseDown:] ()
#9  0x913f5921 in -[NSWindow sendEvent:] ()
#10 0x0856e06c in -[ChromeEventProcessingWindow sendEvent:] (self=0x1b0c87d0, _cmd=0x91b70db1, event=0x1b6f3ad0) at ../../chrome/browser/ui/cocoa/chrome_event_processing_window.mm:134
#11 0x085fd63a in -[FramedBrowserWindow sendEvent:] (self=0x1b0c87d0, _cmd=0x91b70db1, event=0x1b6f3ad0) at ../../chrome/browser/ui/cocoa/framed_browser_window.mm:265
#12 0x913f090f in -[NSApplication sendEvent:] ()
#13 0x004ff70e in -[BrowserCrApplication sendEvent:] (self=0x1b04ad60, _cmd=0x91b70db1, event=0x1b6f3ad0) at ../../chrome/browser/chrome_browser_application_mac.mm:425
#14 0x9130a62c in -[NSApplication run] ()
#15 0x01c65d10 in base::MessagePumpNSApplication::DoRun (this=0x1b05f570, delegate=0x1b064be0) at ../../base/message_loop/message_pump_mac.mm:835
#16 0x01c649a8 in base::MessagePumpCFRunLoopBase::Run (this=0x1b05f570, delegate=0x1b064be0) at ../../base/message_loop/message_pump_mac.mm:399
#17 0x01d38123 in base::MessageLoop::RunInternal (this=0x1b064be0) at ../../base/message_loop/message_loop.cc:441
#18 0x01d37fdb in base::MessageLoop::RunHandler (this=0x1b064be0) at ../../base/message_loop/message_loop.cc:413
#19 0x01d9b5a8 in base::RunLoop::Run (this=0xbffff2b8) at ../../base/run_loop.cc:47
#20 0x0050c0b8 in ChromeBrowserMainParts::MainMessageLoopRun (this=0x1b043dc0, result_code=0x1b522c6c) at ../../chrome/browser/chrome_browser_main.cc:1580
#21 0x08b818d7 in content::BrowserMainLoop::RunMainMessageLoopParts (this=0x1b522c60) at ../../content/browser/browser_main_loop.cc:693
#22 0x08b8db2f in content::BrowserMainRunnerImpl::Run (this=0x1b5240f0) at ../../content/browser/browser_main_runner.cc:121
#23 0x08b7c7cc in content::BrowserMain (parameters=@0xbffff7f8) at ../../content/browser/browser_main.cc:26
#24 0x01bf27cb in content::RunNamedProcessTypeMain (process_type=@0xbffff818, main_function_params=@0xbffff7f8, delegate=0xbffffa50) at ../../content/app/content_main_runner.cc:458
#25 0x01bf3e98 in content::ContentMainRunnerImpl::Run (this=0x1b043130) at ../../content/app/content_main_runner.cc:781
#26 0x01bf1c57 in content::ContentMain (argc=2, argv=0xbffffad0, delegate=0xbffffa50) at ../../content/app/content_main.cc:35
#27 0x0000725c in ChromeMain (argc=2, argv=0xbffffad0) at ../../chrome/app/chrome_main.cc:39
#28 0x00001f7b in main (argc=2, argv=0xbffffad0) at ../../chrome/app/chrome_exe_main_mac.cc:16
Current language:  auto; currently objective-c++

### in...@chromium.org (2013-10-04)

[Empty comment from Monorail migration]

### [Deleted User] (2013-10-04)

I will try to take a look at the infobar problem on Monday, but then  will be OOO until Thursday.

primiano, does the infobar crash happen both with/without your lately CL?

### pr...@chromium.org (2013-10-04)

Happen only after http://crrev.com/25045007.
Without that CL the infobar (or just the delegate, I think) was leaking and there was no UAF/crash.

### cl...@chromium.org (2013-10-05)

ClusterFuzz has detected this issue as fixed in range 226466:226525.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5317365805875200

Uploader: jww@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x000000000000
Crash State:
  - crash stack -
  WebKit::WebSpeechRecognitionHandle::operator WTF::PassRefPtr<WebCore::SpeechRecognition>
  WebKit::SpeechRecognitionClientProxy::didReceiveError
  content::SpeechRecognitionDispatcher::OnErrorOccurred
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=191189:191323
Fixed: https://cluster-fuzz.appspot.com/revisions?range=226466:226525

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97TL-lmcqKaEi9Qx7hnnbTeBsyZyPnriz16sa9f3USkqD-SQipDLBQhjO853diO4zJlGLnEINmPKwnFKT9VVtjnnDmB_Mgd_36A25fvUp4L6LmbZKOA1xMhketitv2WNdt5_EnWOYY9z9Z5EWc8uQ5jK1k_zw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### [Deleted User] (2013-10-06)


I took a closer look at the whole thread, previously the OOM issue is because we are pending the requests on the side and never delete them. This is not good but not really a security issue since we can still run into the similar problems by opening hundreds of getUserMedia or video/audio tags, I believe there are plenty of JS APIs failing on protecting such case.

After http://crrev.com/25045007, speech is able to cancel the request on the UI before make a new request. The JS pages are doing delete/create in a loop, which will trigger infobar_service->ReplaceInfoBar(old_infobar, infobar.Pass()) in MediaStreamInfoBarDelegate line 59. While the users click on the infobar, somehow the delegate has been freed but accessed, that is how the crash happens.

I am not sure if the problem is in ReplaceInfoBar, or simply we should not allow delete/create the infobar in a row.

+ Peter for suggestion.


### pr...@chromium.org (2013-10-06)

I made some further investigation. It looks to me there is some race in the mac/cocoa implementation of the infobar.
I am not 100% sure though, I don't know any detail about WebRTC media infobar, so can't really tell if is the client (media_stream_infobar) misbehaving or the infobar code itself.  I could repro only on Mac OS, though.

I added some instrumentation prints to track down the issue (crrev.com/26198002).

It looks like there is a race interval (~200-300 ms on my mac) between the callback to InfoBarContainer::RemoveInfoBar (and the consequent InfoBarCocoa dtor) and the UI update.
In other words, in the 200-300 ms immediately after the call to InfoBarContainer::ReplaceInfoBar, the click to the UI are dispatched to the previous controller (which has been freed) rather than the new one.

I'm attached a slightly modified version of the repro case.
Repro steps are the following:
 - open the exploit_start.html (from a web server, not file://).
 - When the infobar pops out reload the page.
 - At this point you should see in the log the Js restarting aggressively the recognition every 200 ms.
 - Click on Allow: here it crashes.

This is the output that I get from the instrumentation:
=============================================
InfoBarContainer::ReplaceInfoBar old_delegate: 0x7acbb1f0    new_delegate: 0x7e0b1d20
 ConfirmInfoBarDelegate::CreateInfoBar infobar: 0x7e0a4190  controller: 0x7e0a4460
 InfoBarContainer::RemoveInfoBar infobar: 0x7ac5d860  delegate: 0x7acbb1f0
 InfoBarCocoa DTOR  controller: 0x7acc6df0  delegate: 0x0

InfoBarContainer::ReplaceInfoBar old_delegate: 0x7e0b1d20    new_delegate: 0x7e0ae9f0
 ConfirmInfoBarDelegate::CreateInfoBar infobar: 0x7e03e420  controller: 0x7e0a4b00
 InfoBarContainer::RemoveInfoBar infobar: 0x7e0a4190  delegate: 0x7e0b1d20
 InfoBarCocoa DTOR  controller: 0x7e0a4460  delegate: 0x0

 ALLOW InfobarController: 0x7e0a4460  (delegate: 0x9)  !!!! This refers to the old (destroyed) controller, not the new one (0x7e0a4b00). If the JS timeout was >= 500, this would have been correct and no crash would have happened. 
=============================================

Changing the value of the setTimeout  call (in the exploit_start.html repro case) from 200 to 500 ms avoids the crash. 200 ms or below are enough on my laptop to make the crash happen.

Unfortunately I'm afraid I can't help more at this point: I don't have any background in the infobar design, I don't speak Objective-C and I don't know the principles of the Cocoa MVC.

P.S.
> we can still run into the similar problems by opening hundreds of getUserMedia or video/audio tags
^__^ Personally, the idea of JS being able to cause an OOM in the browser process makes me pretty nervous. Sounds to me like a user-space process being able to cause an OOM into a softirq in kernel space. But that is just my personal opinion and I might have a wrong perception.

### [Deleted User] (2013-10-07)

We don't have our own webrtc infobar, we use the ConfirmInforbar which is also used by lots of other clients.

I agree with Primiano's analysis that there is a racing between tearing down the UI and the corresponding controller/delegate. It is not sure if webrtc is the only client supporting cancel/create requests in a row, but if not, other infobar clients might be hit by the same issue.
I can also confirm that clicking on any of the infobar button, like the learn more link, deny, allow can also trigger the crash.

ReplaceInfobar is supposed to handle a smooth replacement between the old and new infobars, so we have to fix the racing there. 

I am assign the bug to Peter since the logging points to the infobar code. Peter, feel free to assign the bug back to me if you see anything wrong with the media_stream_infobar_delegate.cc or media_capture_devices_dispatcher.cc. I will continue to assist until the problem is resolved.

Primiano, I agree that that is good point, probably we can set a limit on the number of requests to protect the cases, I am going to discuss with my colleagues about it.

### pk...@chromium.org (2013-10-07)

->rsesek since he reviewed the Mac infobar refactor (I don't speak Mac either).

I don't understand how clicks are being dispatched to the previous controller after InfoBarContainer::RemoveInfobar() runs.  That's supposed to synchronously hide the old infobar, so it shouldn't be around for the user to click anymore.  Then ReplaceInfoBar() calls AddInfoBar() which should synchronously show the new infobar.

Robert, can you determine how a click is getting dispatched to a cocoa InfobarController that's already supposed to be invisible?

### rs...@chromium.org (2013-10-07)

These stack frames from the above trace are key:

#6  0x913fed60 in -[NSCell trackMouse:inRect:ofView:untilMouseUp:] ()
#7  0x913fe59f in -[NSButtonCell trackMouse:inRect:ofView:untilMouseUp:] ()
#8  0x913fdcb9 in -[NSControl mouseDown:] ()
#9  0x913f5921 in -[NSWindow sendEvent:] ()

When a button enters -mouseDown: it spins a nested run loop, which will call out to the MessageLoop and service its work (otherwise it would starve). It's therefore possible that that a task is being pumped that is causing the infobar that is spinning the loop to be deleted.

### rs...@chromium.org (2013-10-07)

Peter, does the above answer your question?

### pk...@chromium.org (2013-10-07)

Robert and I chatted about this some and he asked me to write something up.

(1) The problem

Somebody clicks on an infobar button.  The browser starts running a nested loop, but that loop regularly services tasks from the main loop too.  Now a webpage triggers an infobar replace on the main loop, which deletes the infobar being clicked on.  Now the user releases the mouse button and we send a mouse event to the deleted object.

(2) The solution, in general

There are two possible ways to handle this.  One way tries to keep all the relevant objects alive while the nested loop runs, so they can handle events.  The other way tries to safely drop events from the nested loop on the floor after the infobar has been destroyed.

The first class of solution is problematic because once an infobar has been removed/replaced, it also no longer has an owner.  So there's no easy way for it to correctly "handle" events.  Therefore, we want to drop events on the floor somehow.

(3) The solution, specifically

The Mac infobar implementation has a C++ "InfoBarCocoa" subclass of the cross-platform C++ InfoBar object; InfoBarCocoa then owns an InfoBarController, which is the ObjC implementation that implements the Mac-specific logic.  InfoBarCocoa is a barebones bridge that exists to proxy calls from InfoBarController to the cross-platform RemoveSelf() and owner() functions.

When the infobar container wishes to delete an infobar, it calls InfoBarContainer::PlatformSpecificRemoveInfoBar(), which on Mac winds up posting a DeleteSoon() to delete the C++ infobar object.  Once that task runs, it deletes the InfoBar (and thus the InfoBarCocoa), which in turn deletes the InfoBarController since the InfoBarCocoa owns it via scoped_nsobject<>.  (Note that after my infobar system refactor in https://codereview.chromium.org/22694006/ , InfoBar will delete itself in InfoBar::MaybeDelete(), which will be called directly from InfoBarContainer::Hide().)

This suggests that one way to fix this bug is:

(i) Have some sort of InfoBarController function that uses a "keepalive" object to do a scoped [self retain] for the life of the nested event loop, a la https://codereview.chromium.org/7715019/
(ii) Change InfoBarController's |infobar_| raw pointer to a WeakPtr and make InfoBarController's isOwned() function return false if the weak pointer is NULL

This should keep the InfoBarController alive long enough to handle all events, safely drop them on the floor when they can't be processed, and delete the InfoBarController once the InfoBarCocoa is dead AND there's no nested loop spinning.

Robert is going to do the actual implementation here.

### rs...@chromium.org (2013-10-08)

I've confirmed the hypothesis that the DeleteSoon task is being pumped while in the nested -mouseDown: loop. I think the solution (ii) makes most sense, and I do not think that (i) even is applicable since it's a C++ object that's being UAF'd rather than a Cocoa one.

* thread #1: tid = 0x1c03, 0x0862609d Chromium Framework`InfoBarCocoa::~InfoBarCocoa(this=0x1ba77a80) + 45 at infobar_cocoa.mm:18, stop reason = breakpoint 1.3
    frame #0: 0x0862609d Chromium Framework`InfoBarCocoa::~InfoBarCocoa(this=0x1ba77a80) + 45 at infobar_cocoa.mm:18
    frame #1: 0x0862604b Chromium Framework`InfoBarCocoa::~InfoBarCocoa(this=0x1ba77a80) + 43 at infobar_cocoa.mm:18
    frame #2: 0x08625fee Chromium Framework`InfoBarCocoa::~InfoBarCocoa(this=0x1ba77a80) + 46 at infobar_cocoa.mm:18
    frame #3: 0x0862869d Chromium Framework`base::DeleteHelper<InfoBarCocoa>::DoDelete(object=0x1ba77a80) + 61 at sequenced_task_runner_helpers.h:39
    frame #4: 0x01ceb3e0 Chromium Framework`base::internal::RunnableAdapter<void (this=0xbfffcde0, a1=0x1bab1bc0)(void const*)>::Run(void const* const&) + 80 at bind_internal.h:171
    frame #5: 0x01ceb321 Chromium Framework`base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (runnable=(null), a1=0x1bab1bc0)(void const*)>, void (void const* const&)>::MakeItSo(base::internal::RunnableAdapter<void (*)(void const*)>, void const* const&) + 65 at bind_internal.h:871
    frame #6: 0x01ceb27f Chromium Framework`base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (base=0x1bab1bb0)(void const*)>, void ()(void const*), void ()(void const*)>, void ()(void const*)>::Run(base::internal::BindStateBase*) + 95 at bind_internal.h:1166
    frame #7: 0x07805bdb Chromium Framework`base::Callback<void (this=0xbfffd084)>::Run() const + 75 at callback.h:396
    frame #8: 0x01ce7d6b Chromium Framework`base::MessageLoop::RunTask(this=0x1d147ce0, pending_task=0xbfffd070) + 1211 at message_loop.cc:491
    frame #9: 0x01ce81e2 Chromium Framework`base::MessageLoop::DeferOrRunPendingTask(this=0x1d147ce0, pending_task=0xbfffd070) + 98 at message_loop.cc:503
    frame #10: 0x01ce84b2 Chromium Framework`base::MessageLoop::DoWork(this=0x1d147ce0) + 322 at message_loop.cc:617
    frame #11: 0x01c141f8 Chromium Framework`base::MessagePumpCFRunLoopBase::RunWork(this=0x1d148a00) + 168 at message_pump_mac.mm:488
    frame #12: 0x01c137b2 Chromium Framework`base::MessagePumpCFRunLoopBase::RunWorkSource(info=0x1d148a00) + 50 at message_pump_mac.mm:463
    frame #13: 0x942ec04f CoreFoundation`__CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__ + 15
    frame #14: 0x942eba79 CoreFoundation`__CFRunLoopDoSources0 + 233
    frame #15: 0x94311826 CoreFoundation`__CFRunLoopRun + 934
    frame #16: 0x9431101a CoreFoundation`CFRunLoopRunSpecific + 378
    frame #17: 0x94310e8b CoreFoundation`CFRunLoopRunInMode + 123
    frame #18: 0x90e8df5a HIToolbox`RunCurrentEventLoopInMode + 242
    frame #19: 0x90e8dcc9 HIToolbox`ReceiveNextEventCommon + 374
    frame #20: 0x90e8db44 HIToolbox`BlockUntilNextEventMatchingListInMode + 88
    frame #21: 0x9628d93a AppKit`_DPSNextEvent + 724
    frame #22: 0x9628d16c AppKit`-[NSApplication nextEventMatchingMask:untilDate:inMode:dequeue:] + 119
    frame #23: 0x96378429 AppKit`-[NSWindow nextEventMatchingMask:] + 95
    frame #24: 0x96377b3b AppKit`-[NSCell trackMouse:inRect:ofView:untilMouseUp:] + 1346
    frame #25: 0x9637759f AppKit`-[NSButtonCell trackMouse:inRect:ofView:untilMouseUp:] + 511
    frame #26: 0x96376cb9 AppKit`-[NSControl mouseDown:] + 867
    frame #27: 0x9636e921 AppKit`-[NSWindow sendEvent:] + 6968
    frame #28: 0x085686bc Chromium Framework`-[ChromeEventProcessingWindow sendEvent:](self=0x1d185f20, _cmd=0x96ae9db1, event=0x20365280) + 108 at chrome_event_processing_window.mm:134
    frame #29: 0x085f7e0a Chromium Framework`-[FramedBrowserWindow sendEvent:](self=0x1d185f20, _cmd=0x96ae9db1, event=0x20365280) + 762 at framed_browser_window.mm:265
    frame #30: 0x9636990f AppKit`-[NSApplication sendEvent:] + 4278
    frame #31: 0x004ebbee Chromium Framework`-[BrowserCrApplication sendEvent:](self=0x1d579bf0, _cmd=0x96ae9db1, event=0x20365280) + 110 at chrome_browser_application_mac.mm:425
    frame #32: 0x9628362c AppKit`-[NSApplication run] + 951
    frame #33: 0x01c151c0 Chromium Framework`base::MessagePumpNSApplication::DoRun(this=0x1d148a00, delegate=0x1d147ce0) + 416 at message_pump_mac.mm:835
    frame #34: 0x01c13e58 Chromium Framework`base::MessagePumpCFRunLoopBase::Run(this=0x1d148a00, delegate=0x1d147ce0) + 104 at message_pump_mac.mm:399
    frame #35: 0x01ce7573 Chromium Framework`base::MessageLoop::RunInternal(this=0x1d147ce0) + 291 at message_loop.cc:441
    frame #36: 0x01ce742b Chromium Framework`base::MessageLoop::RunHandler(this=0x1d147ce0) + 43 at message_loop.cc:413
    frame #37: 0x01d4a9f8 Chromium Framework`base::RunLoop::Run(this=0xbffff1f8) + 72 at run_loop.cc:47
    frame #38: 0x004f8408 Chromium Framework`ChromeBrowserMainParts::MainMessageLoopRun(this=0x1d553890, result_code=0x1d551aac) + 600 at chrome_browser_main.cc:1580
    frame #39: 0x08b7afb7 Chromium Framework`content::BrowserMainLoop::RunMainMessageLoopParts(this=0x1d551aa0) + 167 at browser_main_loop.cc:693
    frame #40: 0x08b8752f Chromium Framework`content::BrowserMainRunnerImpl::Run(this=0x1d54d020) + 479 at browser_main_runner.cc:121
    frame #41: 0x08b75eac Chromium Framework`content::BrowserMain(parameters=0xbffff738) + 316 at browser_main.cc:26
    frame #42: 0x01ba1ccb Chromium Framework`content::RunNamedProcessTypeMain(process_type=0xbffff758, main_function_params=0xbffff738, delegate=0xbffff990) + 267 at content_main_runner.cc:458
    frame #43: 0x01ba3308 Chromium Framework`content::ContentMainRunnerImpl::Run(this=0x1d5476c0) + 680 at content_main_runner.cc:777
    frame #44: 0x01ba1157 Chromium Framework`content::ContentMain(argc=2, argv=0xbffffa0c, delegate=0xbffff990) + 167 at content_main.cc:35
    frame #45: 0x0000716c Chromium Framework`ChromeMain(argc=2, argv=0xbffffa0c) + 76 at chrome_main.cc:39
    frame #46: 0x00001f7b Chromium`main(argc=2, argv=0xbffffa0c) + 43 at chrome_exe_main_mac.cc:16
    frame #47: 0x00001f45 Chromium`start + 53
Process 69453 resuming
Command #2 'c' continued the target.
[69453:3851:1008/133355:INFO:CONSOLE(7)] "end", source: http://localhost:62173/exploit_start.html (7)
Process 69453 stopped
* thread #1: tid = 0x1c03, 0x08620548 Chromium Framework`-[ConfirmInfoBarController ok:](self=0x1bae7010, _cmd=0x96b1b58b, sender=0x1be9db30) + 104 at confirm_infobar_controller.mm:22, stop reason = EXC_BAD_ACCESS (code=2, address=0x9)


### pk...@chromium.org (2013-10-08)

(i) and (ii) were not distinct solutions.  They're the two steps to solve one solution.

The proposal is to keep the ObjC object alive, but not the C++ object.  You can't keep the C++ object alive without completely reworking the cross-platform model.  (i) keeps the ObjC object alive; (ii) prevents it from doing the UAF on the dead C++ object.

### rs...@chromium.org (2013-10-09)

I've developed another solution where the InfoBarController owns the InfoBarCocoa, rather than the other way around. This is how the ownership is structured for most objects (including BrowserWindow), and the justification for such is largely the issue being seen here -- ObjC objects can still be on screen when the model is deleted.

https://codereview.chromium.org/26541006/

### cl...@chromium.org (2013-10-10)

Fixing bug priority based on security_severity-* and releaseblock-* labels.

### pr...@chromium.org (2013-10-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-10-17)

------------------------------------------------------------------------
r229099 | rsesek@chromium.org | 2013-10-17T12:07:02.874403Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/cocoa/infobars/infobar_controller.h?r1=229099&r2=229098&pathrev=229099
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/cocoa/infobars/infobar_cocoa.h?r1=229099&r2=229098&pathrev=229099
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/cocoa/infobars/infobar_controller.mm?r1=229099&r2=229098&pathrev=229099
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/cocoa/infobars/infobar_cocoa.mm?r1=229099&r2=229098&pathrev=229099
   M http://src.chromium.org/viewvc/chrome/trunk/src/chrome/browser/ui/cocoa/infobars/infobar_container_controller.mm?r1=229099&r2=229098&pathrev=229099

Flip the ownership of InfoBarCocoa and InfoBarController so that the Controller owns the model.

This is consistent with other ownership relationships in Cocoa.

BUG=296690

Review URL: https://codereview.chromium.org/26541006
------------------------------------------------------------------------

### in...@chromium.org (2013-10-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-11-13)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-30)

[Empty comment from Monorail migration]

### mb...@chromium.org (2013-12-10)

Thanks for the report! This one qualifies for a $1000 reward. Race conditions often qualify at lower reward levels, but this one seemed fairly consistent.

### ta...@talater.com (2013-12-15)

Thanks, glad I could help.

### pa...@chromium.org (2013-12-18)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-12-18)

Hey Tal, I just kicked off our payment process on this for the reward, which can take a few weeks. Someone should be in touch to sign you up. Thanks again for your help making Chrome more secure!

### pa...@chromium.org (2013-12-20)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-01-22)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/296690?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078145)*
