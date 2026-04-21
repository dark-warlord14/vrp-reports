# Security: racing UAF during usrsctp_close in usrsctp in webrtc

| Field | Value |
|-------|-------|
| **Issue ID** | [40054325](https://issues.chromium.org/issues/40054325) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ko...@gmail.com |
| **Assignee** | de...@chromium.org |
| **Created** | 2020-12-30 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

usrsctp\_close and sctp\_timeout\_handler functions may run concurrently on separate threads(network[N] & usrsctplib timer[T] thread accordingly)  

Consider the following scenario:  

so->so\_count == 1  

[N] user\_socket.c:2018 executes the following: ACCEPT\_LOCK(); SOCK\_LOCK(so);  

[T] sctputil.c:1883 blocks on SOCK\_LOCK(upcall\_socket);  

[N] user\_socketvar.h:413 so\_count goes to zero and sofree is called  

so->so\_count == 0  

[N] user\_socket.c:285 SOCK\_UNLOCK(so);  

[T] sctputil.c:1883 wakes up and successfully locks SOCK\_LOCK(upcall\_socket); and grabs a ref with soref(upcall\_socket);  

so->so\_count == 1  

[T] sctputil.c:2214 releases the socket again sorele(upcall\_socket);  

so->so\_count == 0  

Later one of the threads will free the socket and the other will use it concurrently and later also try to free.

To test the bug I wrote a small reproducer. It creates a bunch of SctpTransport pairs, connect them to each other. Next I simulate 100% packet loss to ignore DATA packets. Next I send some data. At this point SCTP\_TIMER\_TYPE\_SEND is scheduled for 1000 millis. I sleep for ~1000 millis and try to close the socket at the same time as the timer is handled. To run I use while true; do RACE\_SLEEP\_FROM=1150 RACE\_SLEEP\_TO=1165 ./sctp\_transport\_racer >/dev/null; done; on my machine. Most of the time I get NULL deref, but sometime UAF is triggered.  

I did not check if the bug is reachable from renderer yet. I will do the check very soon.

**VERSION**  

Chrome Version: master, 5073cba99a  

Operating System: found on macos, but it does not matter.

**REPRODUCTION CASE**  

See attached sctp\_transport\_racer.cc

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:  

Crash #1:  

==22339==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160001dcc94 at pc 0x00010ba2a89e bp 0x7ffee4ab6560 sp 0x7ffee4ab6558  

WRITE of size 4 at 0x6160001dcc94 thread T0  

#0 0x10ba2a89d in sctp\_close sctp\_usrreq.c:844  

#1 0x10baf26da in sofree user\_socket.c:287  

#2 0x10bb04917 in usrsctp\_close user\_socket.c:2020  

#3 0x10b73724d in cricket::SctpTransport::CloseSctpSocket() sctp\_transport.cc:948  

#4 0x10b7365c2 in cricket::SctpTransport::~SctpTransport() sctp\_transport.cc:505  

#5 0x10b737802 in cricket::SctpTransport::~SctpTransport() sctp\_transport.cc:502  

#6 0x10b16411d in std::\_\_1::\_\_shared\_ptr\_emplace<cricket::SctpTransport, std::\_\_1::allocator[cricket::SctpTransport](javascript:void(0);) >::\_\_on\_zero\_shared() memory:3621  

#7 0x10b1515a5 in std::\_\_1::\_\_shared\_count::\_\_release\_shared() memory:3455  

#8 0x10b151496 in std::\_\_1::\_\_shared\_weak\_count::\_\_release\_shared() memory:3497  

#9 0x10b15170b in std::\_\_1::shared\_ptr[cricket::SctpTransport](javascript:void(0);)::~shared\_ptr() memory:4226  

#10 0x10b14d0c2 in std::\_\_1::shared\_ptr[cricket::SctpTransport](javascript:void(0);)::~shared\_ptr() memory:4224  

#11 0x10b14e1f6 in std::\_\_1::shared\_ptr[cricket::SctpTransport](javascript:void(0);)::reset() memory:4361  

#12 0x10b14d96a in RunOne(int) sctp\_transport\_racer.cc:126  

#13 0x10b14e75e in main sctp\_transport\_racer.cc:155  

#14 0x7fff6e728cc8 in start+0x0 (libdyld.dylib:x86\_64+0x1acc8)

0x6160001dcc94 is located 532 bytes inside of 632-byte region [0x6160001dca80,0x6160001dccf8)  

freed by thread T39 here:  

#0 0x10c4fe399 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x43399)  

#1 0x10baf27c7 in sodealloc user\_socket.c:241  

#2 0x10baf26e3 in sofree user\_socket.c:302  

#3 0x10baa54c4 in sctp\_timeout\_handler sctputil.c:2214  

#4 0x10b81084d in sctp\_handle\_tick sctp\_callout.c:172  

#5 0x10b810b15 in user\_sctp\_timer\_iterate sctp\_callout.c:214  

#6 0x7fff6e92d108 in \_pthread\_start+0x93 (libsystem\_pthread.dylib:x86\_64+0x6108)  

#7 0x7fff6e928b8a in thread\_start+0xe (libsystem\_pthread.dylib:x86\_64+0x1b8a)

previously allocated by thread T0 here:  

#0 0x10c4fe250 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x43250)  

#1 0x10baf538f in soalloc user\_socket.c:206  

#2 0x10baff206 in socreate user\_socket.c:1251  

#3 0x10baffe29 in usrsctp\_socket user\_socket.c:1346  

#4 0x10b76b66e in cricket::SctpTransport::OpenSctpSocket() sctp\_transport.cc:837  

#5 0x10b73cedc in cricket::SctpTransport::Connect() sctp\_transport.cc:772  

#6 0x10b7466a5 in cricket::SctpTransport::Start(int, int, int) sctp\_transport.cc:576  

#7 0x10b14c1e6 in CreatePair(int, int) sctp\_transport\_racer.cc:66  

#8 0x10b14d3af in RunOne(int) sctp\_transport\_racer.cc:87  

#9 0x10b14e75e in main sctp\_transport\_racer.cc:155  

#10 0x7fff6e728cc8 in start+0x0 (libdyld.dylib:x86\_64+0x1acc8)

Thread T39 created by T0 here:  

#0 0x10c4f838a (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x3d38a)  

#1 0x10ba28111 in sctp\_userspace\_thread\_create sctp\_userspace.c:79  

#2 0x10b810c3f in sctp\_start\_timer\_thread sctp\_callout.c:228  

#3 0x10ba28a07 in sctp\_init sctp\_usrreq.c:144  

#4 0x10baf1923 in usrsctp\_init user\_socket.c:112  

#5 0x10b7bf17b in cricket::SctpTransport::UsrSctpWrapper::InitializeUsrSctp() sctp\_transport.cc:277  

#6 0x10b76d76f in cricket::SctpTransport::UsrSctpWrapper::IncrementUsrSctpUsageCount() sctp\_transport.cc:349  

#7 0x10b76b59a in cricket::SctpTransport::OpenSctpSocket() sctp\_transport.cc:827  

#8 0x10b73cedc in cricket::SctpTransport::Connect() sctp\_transport.cc:772  

#9 0x10b7466a5 in cricket::SctpTransport::Start(int, int, int) sctp\_transport.cc:576  

#10 0x10b14c1e6 in CreatePair(int, int) sctp\_transport\_racer.cc:66  

#11 0x10b14d3af in RunOne(int) sctp\_transport\_racer.cc:87  

#12 0x10b14e75e in main sctp\_transport\_racer.cc:155  

#13 0x7fff6e728cc8 in start+0x0 (libdyld.dylib:x86\_64+0x1acc8)

SUMMARY: AddressSanitizer: heap-use-after-free sctp\_usrreq.c:844 in sctp\_close  

Shadow bytes around the buggy address:  

0x1c2c0003b940: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c2c0003b950: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c2c0003b960: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c2c0003b970: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c2c0003b980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x1c2c0003b990: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x1c2c0003b9a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c2c0003b9b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1c2c0003b9c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1c2c0003b9d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x1c2c0003b9e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

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

Shadow gap: cc  

==22339==ABORTING

Crash #2:  

==21626==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000000 (pc 0x0001077b9695 bp 0x70000620d6e0 sp 0x70000620b980 T17)  

==21626==The signal is caused by a READ memory access.  

==21626==Hint: address points to the zero page.  

(sctp\_transport.cc:327): UninitializeUsrSctp  

#0 0x1077b9695 in cricket::SctpTransport::UsrSctpWrapper::OnSctpOutboundPacket(void\*, void\*, unsigned long, unsigned char, unsigned char) sctp\_transport.cc:392  

#1 0x10790819d in sctp\_lowlevel\_chunk\_output sctp\_output.c:5053  

#2 0x107948811 in sctp\_chunk\_retransmission sctp\_output.c:10365  

#3 0x10792b31a in sctp\_chunk\_output sctp\_output.c:10624  

#4 0x107a97df4 in sctp\_timeout\_handler sctputil.c:1910  

#5 0x10780484d in sctp\_handle\_tick sctp\_callout.c:172  

#6 0x107804b15 in user\_sctp\_timer\_iterate sctp\_callout.c:214  

#7 0x7fff6e92d108 in \_pthread\_start+0x93 (libsystem\_pthread.dylib:x86\_64+0x6108)  

#8 0x7fff6e928b8a in thread\_start+0xe (libsystem\_pthread.dylib:x86\_64+0x1b8a)

Client ID: disabled crash reporting

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Korniltsev Tolya

## Attachments

- [sctp_transport_racer.cc](attachments/sctp_transport_racer.cc) (text/plain, 3.7 KB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 25.0 KB)

## Timeline

### [Deleted User] (2020-12-30)

[Empty comment from Monorail migration]

### mp...@google.com (2020-12-31)

CC'ing some WebRTC people and OWNERS of usrsctplib.

I don't see why this wouldn't be reachable from the renderer so I'll go ahead and add the security labels. A Javascript PoC would be very nice though.

[Monorail components: Blink>WebRTC]

### [Deleted User] (2020-12-31)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ko...@gmail.com (2020-12-31)

So I've caught the second uaf(in the cricket::SctpTransport?) in the renderer. I attach js POC + crash log. It works the same way - racing SCTP_TIMER_TYPE_SEND timer. 
Takes more time to succeed, than the racer in the https://crbug.com/chromium/1162424#c0 (took me ~15 minutes)
I think I should be able to catch the first uaf(in usrsctplib socket close) with exactly the same poc. I will try to run it for a longer time.


### mp...@google.com (2021-01-04)

Assigning to deadbeef@. It looks like there are a lot of outstanding race conditions in usrsctp and none of them are getting fixed. Since we know for sure this one leads to a UAF, I think we are going to need to fix it ourselves.

### mb...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### te...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-01-06)

[Empty comment from Monorail migration]

### hu...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### hu...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### hu...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### mb...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-14)

orphis: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-21)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/49b20f919abe9a21227b0f6f86d223a3fb1e5ee4

commit 49b20f919abe9a21227b0f6f86d223a3fb1e5ee4
Author: Taylor Brandstetter <deadbeef@webrtc.org>
Date: Thu Jan 21 03:03:47 2021

Fix race with SctpTransport destruction and usrsctp timer thread.

The race occurs if the transport is being destroyed at the same time as
a callback occurs on the usrsctp timer thread (for example, for a
retransmission). Fixed by slightly extending the scope of mutex
acquisition to include posting a task to the network thread, where it's
safe to do further work.

Bug: chromium:1162424
Change-Id: Ia25c96fa51cd4ba2d8690ba03de8af9e9f1605ea
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/202560
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Taylor <deadbeef@webrtc.org>
Cr-Commit-Position: refs/heads/master@{#33048}

[modify] https://crrev.com/49b20f919abe9a21227b0f6f86d223a3fb1e5ee4/media/sctp/sctp_transport.h
[modify] https://crrev.com/49b20f919abe9a21227b0f6f86d223a3fb1e5ee4/media/sctp/sctp_transport.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3dc5ab97fb450b101bc5c384b702d9c532da8dd0

commit 3dc5ab97fb450b101bc5c384b702d9c532da8dd0
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Thu Jan 21 07:15:56 2021

Roll WebRTC from 0be184647794 to 49b20f919abe (2 revisions)

https://webrtc.googlesource.com/src.git/+log/0be184647794..49b20f919abe

2021-01-21 deadbeef@webrtc.org Fix race with SctpTransport destruction and usrsctp timer thread.
2021-01-20 peah@webrtc.org Allow separate dump sets for the data dumper in APM

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/webrtc-chromium-autoroll
Please CC webrtc-chromium-sheriffs-robots@google.com on the revert to ensure that a human
is aware of the problem.

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/master/autoroll/README.md

Bug: chromium:1162424
Tbr: webrtc-chromium-sheriffs-robots@google.com
Change-Id: I5bc6e013069836d57d9401c39ea4313969267d11
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2641483
Reviewed-by: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/master@{#845549}

[modify] https://crrev.com/3dc5ab97fb450b101bc5c384b702d9c532da8dd0/DEPS


### ad...@google.com (2021-01-21)

deadbeef@ if this is fixed, please could you mark it so? Then sheriffbot will add merge requests.

### de...@chromium.org (2021-01-21)

The CL above fixes the crash mentioned in https://crbug.com/chromium/1162424#c4, but not the one in the original report.

The crash from the original report occurs purely in usrsctp code, so we need to either wait for a fix in usrsctp (Michael Tuexen is aware of the problem), or start using usrsctp in single-threaded mode to eliminate the possibility of races with the usrsctp timer thread altogether. I plan on doing the latter, so we're not dependent on Michael for a fix, and because it will insulate us against future issues of this sort.

### mp...@chromium.org (2021-01-22)

I think based on the other races with the timer thread, it's a good idea to run usrsctp in single-threaded mode. Thanks!

### [Deleted User] (2021-01-28)

orphis: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### de...@chromium.org (2021-01-29)

FYI, I haven't forgotten about this. Proposed solution is in discussion: https://webrtc-review.googlesource.com/c/src/+/203361

### [Deleted User] (2021-03-01)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-02)

We commit ourselves to a 60 day deadline for fixing for high severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### te...@chromium.org (2021-03-22)

A proposal to run usrsctp in single threaded mode is currently being reviewed in https://webrtc-review.googlesource.com/c/src/+/209321

### gi...@appspot.gserviceaccount.com (2021-04-14)

The following revision refers to this bug:
  https://webrtc.googlesource.com/src/+/d5d222b6ca943e85c8309f2b574616ed49a9cd2f

commit d5d222b6ca943e85c8309f2b574616ed49a9cd2f
Author: Taylor Brandstetter <deadbeef@webrtc.org>
Date: Tue Apr 13 23:11:47 2021

[Merge M86] - Fix race with SctpTransport destruction and usrsctp timer thread.

The race occurs if the transport is being destroyed at the same time as
a callback occurs on the usrsctp timer thread (for example, for a
retransmission). Fixed by slightly extending the scope of mutex
acquisition to include posting a task to the network thread, where it's
safe to do further work.

Bug: chromium:1162424
Change-Id: Ia25c96fa51cd4ba2d8690ba03de8af9e9f1605ea
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/202560
Reviewed-by: Harald Alvestrand <hta@webrtc.org>
Commit-Queue: Taylor <deadbeef@webrtc.org>
Cr-Original-Commit-Position: refs/heads/master@{#33048}
No-Try: True
No-Presubmit: True
Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/215101
Reviewed-by: Mirko Bonadei <mbonadei@webrtc.org>
Cr-Commit-Position: refs/branch-heads/4240@{#18}
Cr-Branched-From: 93a9d19d4eb53b3f4fb4d22e6c54f2e2824437eb-refs/heads/master@{#31969}

[modify] https://crrev.com/d5d222b6ca943e85c8309f2b574616ed49a9cd2f/media/sctp/sctp_transport.cc
[modify] https://crrev.com/d5d222b6ca943e85c8309f2b574616ed49a9cd2f/media/sctp/sctp_transport.h


### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### ko...@gmail.com (2021-04-29)

It's been 4 month since the report. Should we ping Michael? Or maybe disclose on github?

### de...@chromium.org (2021-04-29)

Michael's last update (from a couple weeks ago) was that he's currently working on crbug.com/1187797. In the last couple days it looks like he's been improving input validation problems, which is what allowed `control_send_queue ` to be nonempty in order to reproduce the issue. But the root cause hasn't been fixed yet.

I'm going to reach out to relevant people to decide what to do, as we can't keep waiting indefinitely.

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-07-08)

(Setting FoundIn-87, which is a bit approximate, but good enough for Sheriffbot to stay happy).

### ad...@google.com (2021-07-14)

deadbeef@ any more news on this one?

### de...@chromium.org (2021-07-14)

I provided a repro program in May and Michael said he'd take a look, but haven't heard anything since then. I'll ping him again.

### [Deleted User] (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-06)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-22)

[Empty comment from Monorail migration]

### te...@chromium.org (2021-10-11)

deadbeef@, any update on this? Maybe ping Michael again?

### de...@chromium.org (2021-10-11)

No updates yet. Would you be able to take this over? You and Florent are CCed on the email thread.

### [Deleted User] (2021-11-15)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-15)

[Empty comment from Monorail migration]

### ad...@google.com (2021-12-02)

dcSCTP is now apparently at 50% rollout so I hope we will shortly be able to mark this as Fixed.

### [Deleted User] (2022-01-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2022-02-01)

adetaylor/deadbeef: Has the dcSCTP rollout completed? Can we mark this as fixed? Thanks.

### ad...@chromium.org (2022-02-01)

I happened to email the team earlier today to ask the same thing... because I too would like to get this old bug marked as Fixed!

### de...@chromium.org (2022-02-01)

From orphis, "It's currently at 1% stable, with a CL in review right now to launch at 10% stable. Hopefully 50% in a week or so and 100% in 2 weeks from now, on all platforms and channels."

Looks like the chromium tracking bug is crbug.com/1243702

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ht...@webrtc.org (2022-03-10)

Now that dcSCTP is at 100% rolled out, closing as "won't fix (obsolete)"



### ko...@gmail.com (2022-03-12)

Does this report qualify for any potential reward in chrome vrp? One uaf was fixed in renderer #17 and second is not fixed but replaced with dcsctp.
Should we disclose the not fixed uaf #1 on github usrsctp?

### am...@chromium.org (2022-04-21)

Hi Tolya, thank you for reaching out about this. This issue got closed as a WontFix by the webrtc dev, because the issue you the issue in your original report was resolved by a refactor of usrsctp rather than a fix for this particular bug. Unfortunately, bugs in the WontFix state do not get picked up by automation for VRP panel assessment, which is why this did not get issue did not get reviewed or responded to by the VRP. 
Because the only fix to be merged was landed and merged back in 2021, we haven't been monitoring the comms on it since it was resolved, so apologies no one responded to you sooner (thank you for reaching over by email). 

I'm going to temporarily update this as Fixed from WontFix so I can label this and it can be reviewed by the VRP Panel. Apologies for this missing our process and thank you for your patience. 

### am...@chromium.org (2022-04-21)

temporary update as Fixed and adding appropriate labels for VRP automation 

### [Deleted User] (2022-04-21)

LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2022-04-21)

Yep, I'd like to second https://crbug.com/chromium/1162424#c62 - sorry for not spotting this and thanks for your patience on this bug!

> Should we disclose the not fixed uaf #1 on github usrsctp?

That's a really good question. This bug will open up in 14 weeks unless we mark it as SecurityEmbargo. I've asked Bjorn or Mirko to comment here about how best to communicate it through to the maintainer.

### rz...@google.com (2022-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-22)

Congratulations, Tolya! The VRP Panel has decided to award you $5,000 for this report. Thank you for reaching out about this issue so we could get this rectified and assess this for a reward. Apologies that it got waylaid and thank you for your patience. A member of our finance team will be in touch soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### rz...@google.com (2022-04-25)

Fix already included in M96

### am...@google.com (2022-04-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-12-11)

Marking this as having been "fixed" in M99 which is about the time that dcSCTP was enabled to 100%. Just to keep various analysis scripts happy.

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1162424?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054325)*
