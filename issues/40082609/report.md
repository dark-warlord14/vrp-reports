# Memory corruption in WebSocketChannel::skipBuffer() - underflow in buffer size

| Field | Value |
|-------|-------|
| **Issue ID** | [40082609](https://issues.chromium.org/issues/40082609) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | [Deleted User] |
| **Assignee** | uk...@chromium.org |
| **Created** | 2010-08-09 |
| **Bounty** | $1,337.00 |

## Description

This may be related to https://crbug.com/chromium/51536

Chromium 6.0.490.0 on Mac OS 10.6.4

When Chromium receives a string of '/xff' (5 or more) from a WebSocket server after completing a handshake, the tab immediately crashes.  There are variations of this string with other characters mixed in that also cause an immediate tab crash.

I've even seen the entire browser crash (segfault at 0x0000000018a050a0) as a result of repeatedly crashing tabs with fuzzed WebSocket data, although this is hard to reproduce.  (I have a Mac OS crash report if it's useful)

To reproduce, run the attached websocket.py python server while loading the attached websocket.html in Chromium.  Note that this will probably not work with the current release of Chrome as it uses an older version of the WebSocket protocol.


## Attachments

- [websocket.py](attachments/websocket.py) (text/x-java; charset=us-ascii, 1.3 KB)
- [websocket.html](attachments/websocket.html) (text/plain; charset=us-ascii, 93 B)
- [report1.txt](attachments/report1.txt) (text/x-news; charset=us-ascii, 35.4 KB)
- [report2.txt](attachments/report2.txt) (text/x-news; charset=us-ascii, 36.4 KB)
- [report8.txt](attachments/report8.txt) (text/x-news; charset=us-ascii, 37.5 KB)
- [report4.txt](attachments/report4.txt) (text/x-news; charset=us-ascii, 37.1 KB)
- [report6.txt](attachments/report6.txt) (text/x-news; charset=us-ascii, 36.0 KB)
- [crash.py](attachments/crash.py) (text/x-java; charset=us-ascii, 1.6 KB)
- [report7.txt](attachments/report7.txt) (text/x-news; charset=us-ascii, 37.0 KB)
- [report5.txt](attachments/report5.txt) (text/x-news; charset=us-ascii, 37.5 KB)
- [report3.txt](attachments/report3.txt) (text/x-news; charset=us-ascii, 36.8 KB)
- [crash.html](attachments/crash.html) (text/plain; charset=us-ascii, 129 B)

## Timeline

### ch...@gmail.com (2010-08-09)

Very nice bug... 

The core issue here is the integer underflow in skipBuffer() when a large (or negative) length is passed and then subtracted from m_bufferSize.

There are other major issues though in the caller WebSocketChannel::processBuffer().

There are all sorts of crazy conversions, overflows, and other madness going on with the buffer length any time that bytes with the MSB set are received. I'll try to wrap my head around the madness and re-factor this to something that works.

This specific issue doesn't affect stable but there are very similar issues. I'll take a comprehensive look and file separate bugs.

### ch...@gmail.com (2010-08-10)

[Empty comment from Monorail migration]

### ch...@gmail.com (2010-08-11)

campkei: Let's move discussion to this bug. I haven't been able to replicate a browser crash. What version, arch, and build are you using that you see a crash? 

I can't trigger a breakpoint in a debug build when a socket stream connection is closed when it is in the connect state but if you continue execution everything works itself out fine. Let me know if you can get a reliable repro for the browser crash though. It would almost certainly be a second bug as the cause of this one is very clear.

### [Deleted User] (2010-08-11)

I produced the browser crash on Chromium 6.0.490.0 (55396) on Mac OS 10.6.4, arch i386.  It is 100% reliably reproducible with my configuration (given up to 20 tab refreshes)

I'll see if I can refine the repro further; one reason I think it's difficult to reduce is that it seems to rely on message timing.

In the meantime, let me know if providing you with Mac OS crash reports (or other debugging info) would be useful.


### uk...@chromium.org (2010-08-11)

browser crash would be a different bug than crash in WebSocketChannel::skipBuffer().

Could you provide us Mac OS crash reports, please?

### [Deleted User] (2010-08-11)

Attaching a couple crash reports I have handy.  There are lots of variations of these.

### in...@chromium.org (2010-08-11)

@ukai, will these stacktraces be fixed by your long patch in https://crbug.com/chromium/51739 ?

### [Deleted User] (2010-08-11)

I've refined the browser crash repro to just send the string '\xc9\xb2\xaf\xfd\x84\x82' to Chromium and then hangup.  Otherwise I've made changes to make the crash more likely to occur.  It now crashes the first time the page is loaded 80% of the time on my machine (Chromium 6.0.490.0 on Mac OS 10.6.4)

Attaching the repro ( crash.py server and crash.html )
Also attaching 6 more crash reports produced from this repro.

### ch...@gmail.com (2010-08-11)

campkie: Apparently the browser crash only affects OS X and Linux but I have managed to reproduce it and have a fix that works at least for Linux. We are going to make sure this also covers OS X. Do you want to go ahead and open another bug for this as I believe we now have the WebSocket specific issue wrapped up.

### in...@chromium.org (2010-08-12)

this one is fixed. Campkie, please open a new bug to track the browser crash.

### in...@chromium.org (2010-08-13)

Fix already merged in https://crbug.com/chromium/51739.

### sc...@gmail.com (2010-08-13)

@campkei@iit.edu: congratulations! We'd like to provisionally offer you a $1337 reward for your help in reporting this bug. We are rewarding this higher amount because this is a "high quality report":
- The repro is small and well reduced.
- The repro triggers the bug reliably.
- You are extremely helpful.

We are rewarding at the $1337 level (as opposed to $1000) because this report pointed us towards a little cache of bugs that we were able to notice and address thanks to your report.

Please continue to keep the details confidential until we release the fix in a patch. Also, once we've released the fix, please be considerate that other WebKit-based products might be releasing fix on different timelines.

### [Deleted User] (2010-08-13)

Awesome!  Thanks!

### sc...@gmail.com (2010-08-25)

@campkei: what name would you like us to use for you in order to credit you in our release notes?

### [Deleted User] (2010-08-25)

Name: Keith Campbell

### sc...@gmail.com (2010-11-21)

@campkei: I don't think we paid this one yet? Can you e-mail me, cevans@chromium.org and we'll sort it out.

### sc...@gmail.com (2010-12-02)

Reward is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

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

This issue was migrated from crbug.com/chromium/51630?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/51723]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082609)*
