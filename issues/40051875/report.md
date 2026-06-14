# Security: UAF  in WebSocket Network Service

| Field | Value |
|-------|-------|
| **Issue ID** | [40051875](https://issues.chromium.org/issues/40051875) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Network>WebSockets |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ra...@gmail.com |
| **Assignee** | ri...@chromium.org |
| **Created** | 2020-03-29 |
| **Bounty** | $20,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/master/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

recently, chromium commit [WebSocket] "Add support to consume Datapipe in network service"[1]  

it recv data to readable datapipe using SimpleWatcher. when network process recv data, WebSocket::OnReadable is called by SimpleWatcher.  

WebSocket::OnReadable call WebSocket::ReadAndSendFromDataPipe that read pending\_send\_data\_frames\_ that wrote in WebSocket::SendMessage[2].

then , readable data is sent to channel in WebSocketChannel::SendFrame.  

However, in WebSocketChannel::SendFrame, we can reset websocket pointer[3]  

it should check return value (CHANNEL\_DELETED).

[1] <https://chromium.googlesource.com/chromium/src/+/307321d474256f41b12b53220e4dec1f2d6fdba8>  

[2] <https://cs.chromium.org/chromium/src/services/network/websocket.cc?rcl=a63eb5b93754ab45ecfa5630cc4af6d85e90518a&l=713>  

[3] <https://cs.chromium.org/chromium/src/net/websockets/websocket_channel.cc?rcl=a63eb5b93754ab45ecfa5630cc4af6d85e90518a&l=376>  

**VERSION**  

Chrome Version: 83.0.4092.0 (Developer Build) (64-bit)  

Operating System: All

**REPRODUCTION CASE**  

./chrome --enable-blink-features=MojoJS <http://localhost/poc.html>  

and need simple websocket server  

Type of crash: network process  

Crash State:  

==82696==ERROR: AddressSanitizer: heap-use-after-free on address 0x617000035c24 at pc 0x55d4644ec87b bp 0x7f0d6417fc30 sp 0x7f0d6417fc28  

READ of size 4 at 0x617000035c24 thread T3 (Chrome\_ChildIOT)  

#0 0x55d4644ec87a (/home/oujin/chromium/src/out/asan/chrome+0x1844087a)  

#1 0x55d4644e6d90 (/home/oujin/chromium/src/out/asan/chrome+0x1843ad90)  

#2 0x55d45fc42d5f (/home/oujin/chromium/src/out/asan/chrome+0x13b96d5f)  

#3 0x55d45fc437f5 (/home/oujin/chromium/src/out/asan/chrome+0x13b977f5)  

#4 0x55d45fc410da (/home/oujin/chromium/src/out/asan/chrome+0x13b950da)  

#5 0x55d457c7024d (/home/oujin/chromium/src/out/asan/chrome+0xbbc424d)  

#6 0x55d457c6f282 (/home/oujin/chromium/src/out/asan/chrome+0xbbc3282)  

#7 0x55d457c637d8 (/home/oujin/chromium/src/out/asan/chrome+0xbbb77d8)  

#8 0x55d457c40e67 (/home/oujin/chromium/src/out/asan/chrome+0xbb94e67)  

#9 0x55d457c0f5d8 (/home/oujin/chromium/src/out/asan/chrome+0xbb635d8)  

#10 0x55d457c0ec82 (/home/oujin/chromium/src/out/asan/chrome+0xbb62c82)  

#11 0x55d457c805bf (/home/oujin/chromium/src/out/asan/chrome+0xbbd45bf)  

#12 0x55d45f8cf9d2 (/home/oujin/chromium/src/out/asan/chrome+0x138239d2)  

#13 0x55d45fb1d289 (/home/oujin/chromium/src/out/asan/chrome+0x13a71289)  

#14 0x55d45f8d0549 (/home/oujin/chromium/src/out/asan/chrome+0x13824549)  

#15 0x55d45f77c7b8 (/home/oujin/chromium/src/out/asan/chrome+0x136d07b8)  

#16 0x55d45f6f463a (/home/oujin/chromium/src/out/asan/chrome+0x1364863a)  

#17 0x55d45f7ce3ab (/home/oujin/chromium/src/out/asan/chrome+0x137223ab)  

#18 0x55d45f8aadd1 (/home/oujin/chromium/src/out/asan/chrome+0x137fedd1)  

#19 0x7f0d7aa7d6b9 (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76b9)

0x617000035c24 is located 548 bytes inside of 680-byte region [0x617000035a00,0x617000035ca8)  

freed by thread T3 (Chrome\_ChildIOT) here:  

#0 0x55d4552978ed (/home/oujin/chromium/src/out/asan/chrome+0x91eb8ed)  

#1 0x55d4644f76ed (/home/oujin/chromium/src/out/asan/chrome+0x1844b6ed)  

#2 0x55d4644e6a05 (/home/oujin/chromium/src/out/asan/chrome+0x1843aa05)  

#3 0x55d4608fac07 (/home/oujin/chromium/src/out/asan/chrome+0x1484ec07)  

#4 0x55d4644ec66e (/home/oujin/chromium/src/out/asan/chrome+0x1844066e)  

#5 0x55d4644e6d90 (/home/oujin/chromium/src/out/asan/chrome+0x1843ad90)  

#6 0x55d45fc42d5f (/home/oujin/chromium/src/out/asan/chrome+0x13b96d5f)  

#7 0x55d45fc437f5 (/home/oujin/chromium/src/out/asan/chrome+0x13b977f5)  

#8 0x55d45fc410da (/home/oujin/chromium/src/out/asan/chrome+0x13b950da)  

#9 0x55d457c7024d (/home/oujin/chromium/src/out/asan/chrome+0xbbc424d)  

#10 0x55d457c6f282 (/home/oujin/chromium/src/out/asan/chrome+0xbbc3282)  

#11 0x55d457c637d8 (/home/oujin/chromium/src/out/asan/chrome+0xbbb77d8)  

#12 0x55d457c40e67 (/home/oujin/chromium/src/out/asan/chrome+0xbb94e67)  

#13 0x55d457c0f5d8 (/home/oujin/chromium/src/out/asan/chrome+0xbb635d8)  

#14 0x55d457c0ec82 (/home/oujin/chromium/src/out/asan/chrome+0xbb62c82)  

#15 0x55d457c805bf (/home/oujin/chromium/src/out/asan/chrome+0xbbd45bf)  

#16 0x55d45f8cf9d2 (/home/oujin/chromium/src/out/asan/chrome+0x138239d2)  

#17 0x55d45fb1d289 (/home/oujin/chromium/src/out/asan/chrome+0x13a71289)  

#18 0x55d45f8d0549 (/home/oujin/chromium/src/out/asan/chrome+0x13824549)  

#19 0x55d45f77c7b8 (/home/oujin/chromium/src/out/asan/chrome+0x136d07b8)  

#20 0x55d45f6f463a (/home/oujin/chromium/src/out/asan/chrome+0x1364863a)  

#21 0x55d45f7ce3ab (/home/oujin/chromium/src/out/asan/chrome+0x137223ab)  

#22 0x55d45f8aadd1 (/home/oujin/chromium/src/out/asan/chrome+0x137fedd1)  

#23 0x7f0d7aa7d6b9 (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76b9)

previously allocated by thread T3 (Chrome\_ChildIOT) here:  

#0 0x55d45529708d (/home/oujin/chromium/src/out/asan/chrome+0x91eb08d)  

#1 0x55d4644f6d6e (/home/oujin/chromium/src/out/asan/chrome+0x1844ad6e)  

#2 0x55d4644f6773 (/home/oujin/chromium/src/out/asan/chrome+0x1844a773)  

#3 0x55d4642ea984 (/home/oujin/chromium/src/out/asan/chrome+0x1823e984)  

#4 0x55d4568245ea (/home/oujin/chromium/src/out/asan/chrome+0xa7785ea)  

#5 0x55d45fbe2450 (/home/oujin/chromium/src/out/asan/chrome+0x13b36450)  

#6 0x55d45fbeeae6 (/home/oujin/chromium/src/out/asan/chrome+0x13b42ae6)  

#7 0x55d45fbfa2ee (/home/oujin/chromium/src/out/asan/chrome+0x13b4e2ee)  

#8 0x55d45fbf8a7c (/home/oujin/chromium/src/out/asan/chrome+0x13b4ca7c)  

#9 0x55d45fbeeae6 (/home/oujin/chromium/src/out/asan/chrome+0x13b42ae6)  

#10 0x55d45fbd82e3 (/home/oujin/chromium/src/out/asan/chrome+0x13b2c2e3)  

#11 0x55d45fbda3fc (/home/oujin/chromium/src/out/asan/chrome+0x13b2e3fc)  

#12 0x55d45fc42d5f (/home/oujin/chromium/src/out/asan/chrome+0x13b96d5f)  

#13 0x55d45fc437f5 (/home/oujin/chromium/src/out/asan/chrome+0x13b977f5)  

#14 0x55d45fc410da (/home/oujin/chromium/src/out/asan/chrome+0x13b950da)  

#15 0x55d457c7024d (/home/oujin/chromium/src/out/asan/chrome+0xbbc424d)  

#16 0x55d457c6f282 (/home/oujin/chromium/src/out/asan/chrome+0xbbc3282)  

#17 0x55d457c637d8 (/home/oujin/chromium/src/out/asan/chrome+0xbbb77d8)  

#18 0x55d457c40e67 (/home/oujin/chromium/src/out/asan/chrome+0xbb94e67)  

#19 0x55d457c0f5d8 (/home/oujin/chromium/src/out/asan/chrome+0xbb635d8)  

#20 0x55d457c0ec82 (/home/oujin/chromium/src/out/asan/chrome+0xbb62c82)  

#21 0x55d457c805bf (/home/oujin/chromium/src/out/asan/chrome+0xbbd45bf)  

#22 0x55d45f8cf9d2 (/home/oujin/chromium/src/out/asan/chrome+0x138239d2)  

#23 0x55d45fb1d289 (/home/oujin/chromium/src/out/asan/chrome+0x13a71289)  

#24 0x55d45f8d0549 (/home/oujin/chromium/src/out/asan/chrome+0x13824549)  

#25 0x55d45f77c7b8 (/home/oujin/chromium/src/out/asan/chrome+0x136d07b8)  

#26 0x55d45f6f463a (/home/oujin/chromium/src/out/asan/chrome+0x1364863a)  

#27 0x55d45f7ce3ab (/home/oujin/chromium/src/out/asan/chrome+0x137223ab)  

#28 0x55d45f8aadd1 (/home/oujin/chromium/src/out/asan/chrome+0x137fedd1)  

#29 0x7f0d7aa7d6b9 (/lib/x86\_64-linux-gnu/libpthread.so.0+0x76b9)

Thread T3 (Chrome\_ChildIOT) created by T0 (chrome) here:  

#0 0x55d455258c3a (/home/oujin/chromium/src/out/asan/chrome+0x91acc3a)  

#1 0x55d45f8a9f9e (/home/oujin/chromium/src/out/asan/chrome+0x137fdf9e)  

#2 0x55d45f7cd4bd (/home/oujin/chromium/src/out/asan/chrome+0x137214bd)  

#3 0x55d46970f200 (/home/oujin/chromium/src/out/asan/chrome+0x1d663200)  

#4 0x55d45df05699 (/home/oujin/chromium/src/out/asan/chrome+0x11e59699)  

#5 0x55d45e68e49c (/home/oujin/chromium/src/out/asan/chrome+0x125e249c)  

#6 0x55d45e81bb7d (/home/oujin/chromium/src/out/asan/chrome+0x1276fb7d)  

#7 0x55d45e68939f (/home/oujin/chromium/src/out/asan/chrome+0x125dd39f)  

#8 0x55d455299b73 (/home/oujin/chromium/src/out/asan/chrome+0x91edb73)  

#9 0x7f0d7329082f (/lib/x86\_64-linux-gnu/libc.so.6+0x2082f)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/oujin/chromium/src/out/asan/chrome+0x1844087a)  

Shadow bytes around the buggy address:  

0x0c2e7fffeb30: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2e7fffeb40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2e7fffeb50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2e7fffeb60: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2e7fffeb70: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x0c2e7fffeb80: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd  

0x0c2e7fffeb90: fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa fa  

0x0c2e7fffeba0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2e7fffebb0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2e7fffebc0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c2e7fffebd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==82696==ABORTING

**CREDIT INFORMATION**  

Reporter credit:Woojin Oh(@pwn\_expoit) of STEALIEN

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 2.6 KB)

## Timeline

### jd...@chromium.org (2020-03-30)

ricea@: can you PTAL at this? Thanks very much. Feel free to re-assign if necessary, but I think you were Keita's manager.

[Monorail components: Blink>Network>WebSockets]

### ri...@chromium.org (2020-03-30)

Reproduced.

### ri...@chromium.org (2020-03-30)

+yhirano as he is reviewing the CL.

### [Deleted User] (2020-03-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/51920a88537bee54671abe3aa2a7b692bacae60d

commit 51920a88537bee54671abe3aa2a7b692bacae60d
Author: Adam Rice <ricea@chromium.org>
Date: Tue Mar 31 17:34:42 2020

WebSocket: Check the return value from SendFrame

network::WebSocket should return immediately if the return value of
net::WebSocket::SendFrame is CHANNEL_DELETED. It was not doing so. Add
the necessary return statements.

Also add WARN_UNUSED_RESULT to SendFrame() to make sure it is checked in
future.

Tested manually. No unit tests for this change because
network::WebSocket has no unit tests.

BUG=1065704

Change-Id: I0c7e0cf57f3a98fc80461ec50df59513146eff89
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2123961
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Commit-Queue: Adam Rice <ricea@chromium.org>
Cr-Commit-Position: refs/heads/master@{#754997}

[modify] https://crrev.com/51920a88537bee54671abe3aa2a7b692bacae60d/net/websockets/websocket_channel.h
[modify] https://crrev.com/51920a88537bee54671abe3aa2a7b692bacae60d/net/websockets/websocket_channel_test.cc
[modify] https://crrev.com/51920a88537bee54671abe3aa2a7b692bacae60d/services/network/websocket.cc
[modify] https://crrev.com/51920a88537bee54671abe3aa2a7b692bacae60d/services/network/websocket.h


### ri...@chromium.org (2020-03-31)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-31)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-04-01)

ricea@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ra...@gmail.com (2020-04-03)

* in windows , network service is unsandboxed process. so it can lead to sandbox escape


### mm...@google.com (2020-04-03)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-06)

[Empty comment from Monorail migration]

### na...@google.com (2020-04-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-04-08)

Congrats! The Panel decided to award $20,000 for this report. 

### na...@google.com (2020-04-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-07-07)

This issue was migrated from crbug.com/chromium/1065704?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051875)*
