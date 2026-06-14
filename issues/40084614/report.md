# faulty webm file causes segfault

| Field | Value |
|-------|-------|
| **Issue ID** | [40084614](https://issues.chromium.org/issues/40084614) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2010-11-05 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

memory corruption resulting from malformed webm video file

the crash is a little different depending on whether --user-dir has been wiped before launching the page, or if the video is being watched a second time, or if it is relaunched after the sad tab appears. sometimes the video can be watched up to 3 times before the sad tab appears.

**VERSION**  

Chrome Version: Chromium 9.0.573.0 Ubuntu 10.10  

Operating System: Linux 2.6.35-23-generic #36-Ubuntu SMP Tue Oct 26 17:13:06 UTC 2010 x86\_64 GNU/Linux  

<http://ppa.launchpad.net/chromium-daily/ppa/ubuntu>

Chrome Version: Chromium 7.0.517.44 Ubuntu 10.10  

Operating System: Linux 2.6.35-23-generic #36-Ubuntu SMP Tue Oct 26 17:13:06 UTC 2010 x86\_64 GNU/Linux  

<http://ppa.launchpad.net/chromium-daily/stable/ubuntu>

Chrome Version: 7.0.517.44  

Operating System: Windows XP

**REPRODUCTION CASE**  

sample html:  

<video src='report.webm' autoplay></video>  

video file attached. I wasn't able to make it smaller yet.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: sad tab  

Crash State:

sample dmesg output:  

Nov 5 22:29:51 kernel: [35737.126312] chromium-browse[30664]: segfault at 7f5201269348 ip 00007f5201269348 sp 00007f51ef54c908 error 15  

Nov 5 22:30:13 kernel: [35758.982369] chromium-browse[30742]: segfault at 0 ip (null) sp 00007ff18f4b3908 error 14  

Nov 5 22:36:19 kernel: [36125.082911] chromium-browse[31029]: segfault at 7f950a174bb0 ip 00007f950a174bb0 sp 00007f94f81db908 error 15  

Nov 5 22:36:37 kernel: [36142.251213] chromium-browse[31080]: segfault at 7f5ba8111bb0 ip 00007f5ba8111bb0 sp 00007f5b97b08908 error 15  

Nov 5 22:36:39 kernel: [36144.991586] chromium-browse[31123]: segfault at 7f5445ef1bb0 ip 00007f5445ef1bb0 sp 00007f5435c43908 error 15  

Nov 5 22:36:42 kernel: [36147.090493] chromium-browse[31166]: segfault at 7faa0cf8bbb0 ip 00007faa0cf8bbb0 sp 00007fa9fb080908 error 15  

Nov 5 22:36:46 kernel: [36151.521066] chromium-browse[31209]: segfault at 7f96e63eda50 ip 00007f96e63eda50 sp 00007f96d43b4908 error 15  

Nov 5 22:36:48 kernel: [36153.596988] chromium-browse[31253]: segfault at 7f10152e8bb0 ip 00007f10152e8bb0 sp 00007f10041d2908 error 15  

Nov 5 22:36:50 kernel: [36155.454062] chromium-browse[31296]: segfault at 7f080b918bb0 ip 00007f080b918bb0 sp 00007f07f9f3b908 error 15  

Nov 5 22:36:52 kernel: [36157.729186] chromium-browse[31341]: segfault at 7f61ff306bb0 ip 00007f61ff306bb0 sp 00007f61edd1c908 error 15  

Nov 5 22:36:57 kernel: [36162.517231] chromium-browse[31385]: segfault at 7f0c4c3ccbb0 ip 00007f0c4c3ccbb0 sp 00007f0c3bc8b908 error 15  

Nov 5 22:36:59 kernel: [36164.519176] chromium-browse[31429]: segfault at 7fd285ba1bb0 ip 00007fd285ba1bb0 sp 00007fd2757f4908 error 15  

Nov 5 22:37:01 kernel: [36166.325317] chromium-browse[31472]: segfault at 7f2d4a458bb0 ip 00007f2d4a458bb0 sp 00007f2d39e89908 error 15  

Nov 5 22:37:03 kernel: [36168.302528] chromium-browse[31515]: segfault at 7f30478afbb0 ip 00007f30478afbb0 sp 00007f3037238908 error 15  

Nov 5 22:53:38 kernel: [37161.319572] chromium-browse[602]: segfault at 7fa2a9e92bb0 ip 00007fa2a9e92bb0 sp 00007fa299472908 error 15  

Nov 5 22:53:42 kernel: [37164.791188] chromium-browse[648]: segfault at 8 ip 00007f72318ff3ec sp 00007f7224300780 error 4 in chromium-browser[7f7230ea0000+2fc6000]  

Nov 5 22:53:46 kernel: [37168.803901] chromium-browse[696]: segfault at 7fad431cfbb0 ip 00007fad431cfbb0 sp 00007fad32968908 error 15  

Nov 5 22:53:49 kernel: [37172.178351] chromium-browse[739]: segfault at 7f046300cbb0 ip 00007f046300cbb0 sp 00007f04526f4908 error 15  

Nov 5 22:53:53 kernel: [37175.962026] chromium-browse[783]: segfault at 7f76ac8a6bb0 ip 00007f76ac8a6bb0 sp 00007f769bff8908 error 15  

Nov 5 22:53:56 kernel: [37178.759798] chromium-browse[827]: segfault at 7f65e9860bb0 ip 00007f65e9860bb0 sp 00007f65d9439908 error 15  

Nov 5 22:53:58 kernel: [37181.635247] chromium-browse[871]: segfault at 7f2591d2dbb0 ip 00007f2591d2dbb0 sp 00007f2580e82908 error 15  

Nov 5 22:54:01 kernel: [37184.681261] chromium-browse[916]: segfault at 7fa485aefbb0 ip 00007fa485aefbb0 sp 00007fa473ab8908 error 15  

Nov 5 22:54:05 kernel: [37187.728179] chromium-browse[959]: segfault at 7f146a0cdbb0 ip 00007f146a0cdbb0 sp 00007f1459452908 error 15  

Nov 5 22:54:15 kernel: [37198.542456] chromium-browse[1017]: segfault at 7f51abb584d0 ip 00007f51abb584d0 sp 00007f5199891908 error 15  

Nov 5 22:54:23 kernel: [37206.358088] chromium-browse[1069]: segfault at 7fc76e0d0a50 ip 00007fc76e0d0a50 sp 00007fc75c9ed908 error 15  

Nov 5 22:55:24 kernel: [37266.747989] chromium-browse[1090]: segfault at 38 ip 00007fc76a726e67 sp 00007fc75c1ec910 error 4 in chromium-browser[7fc76958d000+2fc6000]

first run with -g --single-process:

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffdb461710 (LWP 387)]  

0x00007ffff8f09880 in ?? ()  

(gdb) bt  

#0 0x00007ffff8f09880 in ?? ()  

#1 0x00007ffff61d2e6a in media::FFmpegDemuxer::DemuxTask (this=0x7ffff900f510) at media/filters/ffmpeg\_demuxer.cc:544  

#2 0x00007ffff5b0a3b1 in MessageLoop::RunTask (this=0x7fffdb460a90, task=0x7ffff9442630) at base/message\_loop.cc:417  

#3 0x00007ffff5b0ba2b in MessageLoop::DeferOrRunPendingTask (this=0x7fffdb460a90, pending\_task=<value optimized out>) at base/message\_loop.cc:426  

#4 0x00007ffff5b0bd1d in MessageLoop::DoWork (this=0x7fffdb460a90) at base/message\_loop.cc:533  

#5 0x00007ffff5b0daf9 in base::MessagePumpDefault::Run (this=0x7ffff9304f00, delegate=0x7fffdb460a90) at base/message\_pump\_default.cc:23  

#6 0x00007ffff5b0affc in RunHandler (this=0x7ffff8ef91a0) at base/message\_loop.cc:237  

#7 MessageLoop::Run (this=0x7ffff8ef91a0) at base/message\_loop.cc:215  

#8 0x00007ffff5b2ba55 in base::Thread::ThreadMain (this=0x7ffff9087580) at base/thread.cc:164  

#9 0x00007ffff5b1aeaa in ThreadFunc (closure=0x7ffff8ef91a0) at base/platform\_thread\_posix.cc:35  

#10 0x00007ffff10cb971 in start\_thread () from /lib/libpthread.so.0  

#11 0x00007fffeedc591d in clone () from /lib/libc.so.6  

#12 0x0000000000000000 in ?? ()  

(gdb) i r  

rax 0x7ffff8f09850 140737369905232  

rbx 0x7ffff900f510 140737370977552  

rcx 0x0 0  

rdx 0x2 2  

rsi 0x7ffff9443140 140737375383872  

rdi 0x7ffff8ef91a0 140737369837984  

rbp 0x0 0x0  

rsp 0x7fffdb460908 0x7fffdb460908  

r8 0x0 0  

r9 0x1 1  

r10 0x0 0  

r11 0x0 0  

r12 0x7ffff8ef91a0 140737369837984  

r13 0x7fffdb460a90 140736872188560  

r14 0xffffffffffffffff -1  

r15 0x7fffdb460c30 140736872188976  

rip 0x7ffff8f09880 0x7ffff8f09880  

eflags 0x10246 [ PF ZF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

(gdb) disas  

No function contains program counter for selected frame.  

(gdb) disas 0x00007ffff61d2e6a  

Dump of assembler code for function media::FFmpegDemuxer::DemuxTask():  

0x00007ffff61d2de0 <+0>: mov %rbx,-0x18(%rsp)  

0x00007ffff61d2de5 <+5>: mov %rbp,-0x10(%rsp)  

0x00007ffff61d2dea <+10>: mov %rdi,%rbx  

0x00007ffff61d2ded <+13>: mov %r12,-0x8(%rsp)  

0x00007ffff61d2df2 <+18>: sub $0x18,%rsp  

0x00007ffff61d2df6 <+22>: callq 0x7ffff61d2210 [media::FFmpegDemuxer::StreamsHavePendingReads()](javascript:void(0);)  

0x00007ffff61d2dfb <+27>: test %al,%al  

0x00007ffff61d2dfd <+29>: jne 0x7ffff61d2e18 [media::FFmpegDemuxer::DemuxTask()+56](javascript:void(0);)  

0x00007ffff61d2dff <+31>: mov (%rsp),%rbx  

0x00007ffff61d2e03 <+35>: mov 0x8(%rsp),%rbp  

0x00007ffff61d2e08 <+40>: mov 0x10(%rsp),%r12  

0x00007ffff61d2e0d <+45>: add $0x18,%rsp  

0x00007ffff61d2e11 <+49>: retq  

0x00007ffff61d2e12 <+50>: jmp 0x7ffff61d2e18 [media::FFmpegDemuxer::DemuxTask()+56](javascript:void(0);)  

0x00007ffff61d2e14 <+52>: nop  

0x00007ffff61d2e15 <+53>: nop  

0x00007ffff61d2e16 <+54>: nop  

0x00007ffff61d2e17 <+55>: nop  

0x00007ffff61d2e18 <+56>: mov $0x48,%edi  

0x00007ffff61d2e1d <+61>: callq 0x7ffff6dff170 <tc\_new(size\_t)>  

0x00007ffff61d2e22 <+66>: mov %rax,%rbp  

0x00007ffff61d2e25 <+69>: mov $0x9,%ecx  

0x00007ffff61d2e2a <+74>: xor %eax,%eax  

0x00007ffff61d2e2c <+76>: mov %rbp,%rdi  

0x00007ffff61d2e2f <+79>: mov %rbp,%rsi  

0x00007ffff61d2e32 <+82>: rep stos %rax,%es:(%rdi)  

0x00007ffff61d2e35 <+85>: mov 0x28(%rbx),%rdi  

0x00007ffff61d2e39 <+89>: callq 0x7ffff61e1620 <av\_read\_frame(AVFormatContext\*, AVPacket\*)>  

0x00007ffff61d2e3e <+94>: test %eax,%eax  

0x00007ffff61d2e40 <+96>: js 0x7ffff61d2eb0 [media::FFmpegDemuxer::DemuxTask()+208](javascript:void(0);)  

0x00007ffff61d2e42 <+98>: movslq 0x1c(%rbp),%rdx  

0x00007ffff61d2e46 <+102>: mov 0x48(%rbx),%rax  

0x00007ffff61d2e4a <+106>: mov (%rax,%rdx,8),%r12  

0x00007ffff61d2e4e <+110>: test %r12,%r12  

0x00007ffff61d2e51 <+113>: je 0x7ffff61d2e6a [media::FFmpegDemuxer::DemuxTask()+138](javascript:void(0);)  

0x00007ffff61d2e53 <+115>: mov %rbp,%rdi  

0x00007ffff61d2e56 <+118>: callq 0x7ffff61e11d0 <av\_dup\_packet(AVPacket\*)>  

0x00007ffff61d2e5b <+123>: mov (%r12),%rax  

0x00007ffff61d2e5f <+127>: mov %rbp,%rsi  

0x00007ffff61d2e62 <+130>: xor %ebp,%ebp  

0x00007ffff61d2e64 <+132>: mov %r12,%rdi  

0x00007ffff61d2e67 <+135>: callq \*0x38(%rax)  

0x00007ffff61d2e6a <+138>: mov %rbx,%rdi  

0x00007ffff61d2e6d <+141>: callq 0x7ffff61d2210 [media::FFmpegDemuxer::StreamsHavePendingReads()](javascript:void(0);)  

0x00007ffff61d2e72 <+146>: test %al,%al  

0x00007ffff61d2e74 <+148>: jne 0x7ffff61d2ea0 [media::FFmpegDemuxer::DemuxTask()+192](javascript:void(0);)  

0x00007ffff61d2e76 <+150>: mov %rbp,%rdi  

0x00007ffff61d2e79 <+153>: callq 0x7ffff61e11b0 <av\_free\_packet(AVPacket\*)>  

0x00007ffff61d2e7e <+158>: mov %rbp,%rdi  

0x00007ffff61d2e81 <+161>: mov (%rsp),%rbx  

0x00007ffff61d2e85 <+165>: mov 0x8(%rsp),%rbp  

0x00007ffff61d2e8a <+170>: mov 0x10(%rsp),%r12  

0x00007ffff61d2e8f <+175>: add $0x18,%rsp  

0x00007ffff61d2e93 <+179>: jmpq 0x7ffff6dfccc0 <tc\_delete(void\*)>  

0x00007ffff61d2e98 <+184>: jmp 0x7ffff61d2ea0 [media::FFmpegDemuxer::DemuxTask()+192](javascript:void(0);)  

0x00007ffff61d2e9a <+186>: nop  

0x00007ffff61d2e9b <+187>: nop  

0x00007ffff61d2e9c <+188>: nop  

0x00007ffff61d2e9d <+189>: nop  

0x00007ffff61d2e9e <+190>: nop  

0x00007ffff61d2e9f <+191>: nop  

0x00007ffff61d2ea0 <+192>: mov (%rbx),%rax  

0x00007ffff61d2ea3 <+195>: mov %rbx,%rdi  

0x00007ffff61d2ea6 <+198>: callq \*0xa0(%rax)  

0x00007ffff61d2eac <+204>: jmp 0x7ffff61d2e76 [media::FFmpegDemuxer::DemuxTask()+150](javascript:void(0);)  

0x00007ffff61d2eae <+206>: xchg %ax,%ax  

0x00007ffff61d2eb0 <+208>: mov %rbx,%rdi  

0x00007ffff61d2eb3 <+211>: callq 0x7ffff61d2670 [media::FFmpegDemuxer::StreamHasEnded()](javascript:void(0);)  

0x00007ffff61d2eb8 <+216>: jmp 0x7ffff61d2e76 [media::FFmpegDemuxer::DemuxTask()+150](javascript:void(0);)  

End of assembler dump.  

(gdb)

second run:

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffdb059710 (LWP 429)]  

media::FFmpegDemuxer::DemuxTask (this=0x7ffff9014630) at media/filters/ffmpeg\_demuxer.cc:544  

544 media/filters/ffmpeg\_demuxer.cc: No such file or directory.  

in media/filters/ffmpeg\_demuxer.cc  

(gdb) bt  

#0 media::FFmpegDemuxer::DemuxTask (this=0x7ffff9014630) at media/filters/ffmpeg\_demuxer.cc:544  

#1 0x00007ffff5b0a3b1 in MessageLoop::RunTask (this=0x7fffdb058a90, task=0x7ffff953a1e0) at base/message\_loop.cc:417  

#2 0x00007ffff5b0ba2b in MessageLoop::DeferOrRunPendingTask (this=0x7fffdb058a90, pending\_task=<value optimized out>) at base/message\_loop.cc:426  

#3 0x00007ffff5b0bd1d in MessageLoop::DoWork (this=0x7fffdb058a90) at base/message\_loop.cc:533  

#4 0x00007ffff5b0daf9 in base::MessagePumpDefault::Run (this=0x7ffff9148580, delegate=0x7fffdb058a90) at base/message\_pump\_default.cc:23  

#5 0x00007ffff5b0affc in RunHandler (this=0x7ffff9416780) at base/message\_loop.cc:237  

#6 MessageLoop::Run (this=0x7ffff9416780) at base/message\_loop.cc:215  

#7 0x00007ffff5b2ba55 in base::Thread::ThreadMain (this=0x7ffff90c3880) at base/thread.cc:164  

#8 0x00007ffff5b1aeaa in ThreadFunc (closure=0x7ffff9416780) at base/platform\_thread\_posix.cc:35  

#9 0x00007ffff10cb971 in start\_thread () from /lib/libpthread.so.0  

#10 0x00007fffeedc591d in clone () from /lib/libc.so.6  

#11 0x0000000000000000 in ?? ()  

(gdb) disas  

Dump of assembler code for function media::FFmpegDemuxer::DemuxTask():  

0x00007ffff61d2de0 <+0>: mov %rbx,-0x18(%rsp)  

0x00007ffff61d2de5 <+5>: mov %rbp,-0x10(%rsp)  

0x00007ffff61d2dea <+10>: mov %rdi,%rbx  

0x00007ffff61d2ded <+13>: mov %r12,-0x8(%rsp)  

0x00007ffff61d2df2 <+18>: sub $0x18,%rsp  

0x00007ffff61d2df6 <+22>: callq 0x7ffff61d2210 [media::FFmpegDemuxer::StreamsHavePendingReads()](javascript:void(0);)  

0x00007ffff61d2dfb <+27>: test %al,%al  

0x00007ffff61d2dfd <+29>: jne 0x7ffff61d2e18 [media::FFmpegDemuxer::DemuxTask()+56](javascript:void(0);)  

0x00007ffff61d2dff <+31>: mov (%rsp),%rbx  

0x00007ffff61d2e03 <+35>: mov 0x8(%rsp),%rbp  

0x00007ffff61d2e08 <+40>: mov 0x10(%rsp),%r12  

0x00007ffff61d2e0d <+45>: add $0x18,%rsp  

0x00007ffff61d2e11 <+49>: retq  

0x00007ffff61d2e12 <+50>: jmp 0x7ffff61d2e18 [media::FFmpegDemuxer::DemuxTask()+56](javascript:void(0);)  

0x00007ffff61d2e14 <+52>: nop  

0x00007ffff61d2e15 <+53>: nop  

0x00007ffff61d2e16 <+54>: nop  

0x00007ffff61d2e17 <+55>: nop  

0x00007ffff61d2e18 <+56>: mov $0x48,%edi  

0x00007ffff61d2e1d <+61>: callq 0x7ffff6dff170 <tc\_new(size\_t)>  

0x00007ffff61d2e22 <+66>: mov %rax,%rbp  

0x00007ffff61d2e25 <+69>: mov $0x9,%ecx  

0x00007ffff61d2e2a <+74>: xor %eax,%eax  

0x00007ffff61d2e2c <+76>: mov %rbp,%rdi  

0x00007ffff61d2e2f <+79>: mov %rbp,%rsi  

0x00007ffff61d2e32 <+82>: rep stos %rax,%es:(%rdi)  

0x00007ffff61d2e35 <+85>: mov 0x28(%rbx),%rdi  

0x00007ffff61d2e39 <+89>: callq 0x7ffff61e1620 <av\_read\_frame(AVFormatContext\*, AVPacket\*)>  

0x00007ffff61d2e3e <+94>: test %eax,%eax  

0x00007ffff61d2e40 <+96>: js 0x7ffff61d2eb0 [media::FFmpegDemuxer::DemuxTask()+208](javascript:void(0);)  

0x00007ffff61d2e42 <+98>: movslq 0x1c(%rbp),%rdx  

0x00007ffff61d2e46 <+102>: mov 0x48(%rbx),%rax  

0x00007ffff61d2e4a <+106>: mov (%rax,%rdx,8),%r12  

0x00007ffff61d2e4e <+110>: test %r12,%r12  

0x00007ffff61d2e51 <+113>: je 0x7ffff61d2e6a [media::FFmpegDemuxer::DemuxTask()+138](javascript:void(0);)  

0x00007ffff61d2e53 <+115>: mov %rbp,%rdi  

0x00007ffff61d2e56 <+118>: callq 0x7ffff61e11d0 <av\_dup\_packet(AVPacket\*)>  

=> 0x00007ffff61d2e5b <+123>: mov (%r12),%rax  

0x00007ffff61d2e5f <+127>: mov %rbp,%rsi  

0x00007ffff61d2e62 <+130>: xor %ebp,%ebp  

0x00007ffff61d2e64 <+132>: mov %r12,%rdi  

0x00007ffff61d2e67 <+135>: callq \*0x38(%rax)  

0x00007ffff61d2e6a <+138>: mov %rbx,%rdi  

0x00007ffff61d2e6d <+141>: callq 0x7ffff61d2210 [media::FFmpegDemuxer::StreamsHavePendingReads()](javascript:void(0);)  

0x00007ffff61d2e72 <+146>: test %al,%al  

0x00007ffff61d2e74 <+148>: jne 0x7ffff61d2ea0 [media::FFmpegDemuxer::DemuxTask()+192](javascript:void(0);)  

0x00007ffff61d2e76 <+150>: mov %rbp,%rdi  

0x00007ffff61d2e79 <+153>: callq 0x7ffff61e11b0 <av\_free\_packet(AVPacket\*)>  

0x00007ffff61d2e7e <+158>: mov %rbp,%rdi  

0x00007ffff61d2e81 <+161>: mov (%rsp),%rbx  

0x00007ffff61d2e85 <+165>: mov 0x8(%rsp),%rbp  

---Type <return> to continue, or q <return> to quit---  

0x00007ffff61d2e8a <+170>: mov 0x10(%rsp),%r12  

0x00007ffff61d2e8f <+175>: add $0x18,%rsp  

0x00007ffff61d2e93 <+179>: jmpq 0x7ffff6dfccc0 <tc\_delete(void\*)>  

0x00007ffff61d2e98 <+184>: jmp 0x7ffff61d2ea0 [media::FFmpegDemuxer::DemuxTask()+192](javascript:void(0);)  

0x00007ffff61d2e9a <+186>: nop  

0x00007ffff61d2e9b <+187>: nop  

0x00007ffff61d2e9c <+188>: nop  

0x00007ffff61d2e9d <+189>: nop  

0x00007ffff61d2e9e <+190>: nop  

0x00007ffff61d2e9f <+191>: nop  

0x00007ffff61d2ea0 <+192>: mov (%rbx),%rax  

0x00007ffff61d2ea3 <+195>: mov %rbx,%rdi  

0x00007ffff61d2ea6 <+198>: callq \*0xa0(%rax)  

0x00007ffff61d2eac <+204>: jmp 0x7ffff61d2e76 [media::FFmpegDemuxer::DemuxTask()+150](javascript:void(0);)  

0x00007ffff61d2eae <+206>: xchg %ax,%ax  

0x00007ffff61d2eb0 <+208>: mov %rbx,%rdi  

0x00007ffff61d2eb3 <+211>: callq 0x7ffff61d2670 [media::FFmpegDemuxer::StreamHasEnded()](javascript:void(0);)  

0x00007ffff61d2eb8 <+216>: jmp 0x7ffff61d2e76 [media::FFmpegDemuxer::DemuxTask()+150](javascript:void(0);)  

End of assembler dump.  

(gdb) i r  

rax 0x0 0  

rbx 0x7ffff9014630 140737370998320  

rcx 0x0 0  

rdx 0x2 2  

rsi 0x0 0  

rdi 0x7ffff9416780 140737375201152  

rbp 0x7ffff9416780 0x7ffff9416780  

rsp 0x7fffdb058910 0x7fffdb058910  

r8 0x0 0  

r9 0x1 1  

r10 0x0 0  

r11 0x0 0  

r12 0x75746e756255 129142929842773  

r13 0x7fffdb058a90 140736867961488  

r14 0xffffffffffffffff -1  

r15 0x7fffdb058c30 140736867961904  

rip 0x7ffff61d2e5b 0x7ffff61d2e5b [media::FFmpegDemuxer::DemuxTask()+123](javascript:void(0);)  

eflags 0x10202 [ IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

(gdb)

ffmpeg\_demuxer.cc:

```
536     if (packet.get()) {  
537       // If a packet is returned by FFmpeg's av_parser_parse2()  
538       // the packet will reference an inner memory of FFmpeg.  
539       // In this case, the packet's "destruct" member is NULL,  
540       // and it MUST be duplicated. This fixes issue with MP3 and possibly  
541       // other codecs.  It is safe to call this function even if the packet does  
542       // not refer to inner memory from FFmpeg.  
543       av_dup_packet(packet.get());  

```

==> 544 demuxer\_stream->EnqueuePacket(packet.release());  

545 }  

546 }

## Attachments

- [report.webm](attachments/report.webm) (application/ogg; charset=binary, 190.0 KB)

## Timeline

### sc...@gmail.com (2010-11-05)

@miaubiz: great report, awesome, thank you.
First question, what name should we use for credit should this result in a security advisory?

### sc...@gmail.com (2010-11-05)

Andrew, the localized condition is captured by this debug check:

DCHECK_LT(packet->stream_index, static_cast<int>(packet_streams_.size()));

The index is 2 but the size is 1. So here, we then pull an out-of-bounds object pointer from our array in the next line:

FFmpegDemuxerStream* demuxer_stream = packet_streams_[packet->stream_index];

And then of course everything goes to hell.


The obvious immediate question is:
- Is this a condition that a corrupt stream can easily trigger, or are we only getting into this state because of some previous root cause?

### sc...@gmail.com (2010-11-05)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-05)

[Empty comment from Monorail migration]

### bu...@gmail.com (2010-11-05)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=65269

------------------------------------------------------------------------
r65269 | scherkus@chromium.org | Fri Nov 05 15:56:12 PDT 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/ffmpeg/ffmpeg_unittest.cc?r1=65269&r2=65268&pathrev=65269

Adding a test case to ffmpeg_unittests for https://crbug.com/chromium/62127.

BUG=62127
TEST=ffmpeg_unittests

Review URL: http://codereview.chromium.org/4590003
------------------------------------------------------------------------

### sc...@gmail.com (2010-11-06)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-11-06)

Defensive patch up for review.
The good news here is that operator[] on std::vector for Windows, at least, should crash cleanly on an OOB index, even in an optimized build. This may be exploitable only on Linux. Not sure about the Mac runtime.

### mi...@gmail.com (2010-11-06)

@scarybeast: please credit miaubiz





### bu...@gmail.com (2010-11-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=65346

------------------------------------------------------------------------
r65346 | cevans@chromium.org | Sun Nov 07 20:26:09 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/filters/ffmpeg_demuxer.cc?r1=65346&r2=65345&pathrev=65346

Make sure that ffmpeg returning us an invalid stream cannot damage us too
badly.

BUG=62127
TEST=Added by Andrew

Review URL: http://codereview.chromium.org/4619001
------------------------------------------------------------------------

### bu...@gmail.com (2010-11-08)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=65350

------------------------------------------------------------------------
r65350 | cevans@chromium.org | Sun Nov 07 21:17:39 PST 2010

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/552/src/media/filters/ffmpeg_demuxer.cc?r1=65350&r2=65349&pathrev=65350

Merge 65346 - Make sure that ffmpeg returning us an invalid stream cannot damage us too
badly.

BUG=62127
TEST=Added by Andrew

Review URL: http://codereview.chromium.org/4619001

TBR=scherkus@chromium.org
Review URL: http://codereview.chromium.org/4635003
------------------------------------------------------------------------

### sc...@gmail.com (2010-11-08)

Fixed and merged to M8 branch.
The fix should hit a Beta release this week, and make its way to stable a few weeks after that when Chrome 8 is released :)


### sc...@gmail.com (2010-11-08)

@miaubiz: congratulations! This bug report provisionally qualifies for a $1000 Chromium Security Reward.
Thank you for taking the trouble to write a very thorough report, with a good repro file, register dumps and stack traces. Thanks also for testing with multiple different versions! It is because of these things that the panel awarded at the higher $1000 level.

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

### [Deleted User] (2010-11-11)

Verified with chrome 8.0.552.200 on Ubuntu 10.10

### sc...@gmail.com (2010-11-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-03)

@miaubiz: fix is live to all users! Thanks again; and e-mail cevans@chromium.org to get set up to collect the reward.

### sc...@gmail.com (2010-12-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2010-12-20)

Payment is in the electronic system.

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/62127?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084614)*
