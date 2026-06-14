# race in base/third_party/xdg_mime (crasher)

| Field | Value |
|-------|-------|
| **Issue ID** | [40087467](https://issues.chromium.org/issues/40087467) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink, Internals, Internals>Plugins |
| **Platforms** | Linux |
| **Reporter** | ao...@gmail.com |
| **Assignee** | ts...@chromium.org |
| **Created** | 2011-02-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Opening suitable pages sometimes causes Chrome to crash at various places on startup. These kind of crashes have been happening for a while now, but have been difficult to isolate and reproduce. The last browser test run found several files which seem to trigger this fairly often. One such file is attached. I'll try to narrow down the cause later if others can also reproduce and this is not a duplicate issue.

The crashes look like there could be a memory corruption. Many of the traces have had hosed pointers, often with freeing or allocating going on nearby, so reporting this conservatively as a security issue.

**VERSION**  

Chrome Version: 9.0.597.83 beta (also current dev)  

Operating System: Linux, Ubuntu 10.10 x64\_64

**REPRODUCTION CASE**  

The crash should occur at least once a minute when repeatedly opening the attached file. The following loop should trigger a browser crash about once a minute:  

$ while true; do google-chrome a.html a.html a.html a.html & sleep 1.5; pkill -9 chrome; done

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State:  

Crash state varies a lot. One from 9.0.597.83 beta:

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffe7b62700 (LWP 24653)]  

\_\_strcmp\_sse2 () at ../sysdeps/x86\_64/multiarch/../strcmp.S:107  

107 ../sysdeps/x86\_64/multiarch/../strcmp.S: No such file or directory.  

in ../sysdeps/x86\_64/multiarch/../strcmp.S  

(gdb) bt  

#0 \_\_strcmp\_sse2 () at ../sysdeps/x86\_64/multiarch/../strcmp.S:107  

#1 0x00007ffff1ac43b4 in msort\_with\_tmp (p=<value optimized out>,  

b=<value optimized out>, n=<value optimized out>) at msort.c:105  

#2 0x00007ffff1ac4188 in msort\_with\_tmp (p=<value optimized out>,  

b=<value optimized out>, n=<value optimized out>) at msort.c:54  

#3 0x00007ffff1ac4188 in msort\_with\_tmp (p=<value optimized out>,  

b=<value optimized out>, n=<value optimized out>) at msort.c:54  

#4 0x00007ffff1ac4188 in msort\_with\_tmp (p=<value optimized out>,  

b=<value optimized out>, n=<value optimized out>) at msort.c:54  

#5 0x00007ffff1ac4178 in msort\_with\_tmp (p=0x4b9da40,  

b=<value optimized out>, n=<value optimized out>) at msort.c:53  

#6 0x00007ffff1ac4178 in msort\_with\_tmp (p=0x4b9da40,  

b=<value optimized out>, n=<value optimized out>) at msort.c:53  

#7 0x00007ffff1ac4178 in msort\_with\_tmp (p=0x4b9da40,  

b=<value optimized out>, n=<value optimized out>) at msort.c:53  

#8 0x00007ffff1ac4178 in msort\_with\_tmp (p=0x4b9da40,  

b=<value optimized out>, n=<value optimized out>) at msort.c:53  

#9 0x00007ffff1ac4178 in msort\_with\_tmp (p=0x4b9da40,  

b=<value optimized out>, n=<value optimized out>) at msort.c:53  

#10 0x00007ffff1ac47ec in qsort\_r (b=<value optimized out>,  

n=<value optimized out>, s=0, cmp=0xbd5860, arg=0x0) at msort.c:294  

#11 0x0000000000bd5812 in ?? ()  

#12 0x0000000000bd5533 in ?? ()  

[...]  

(gdb) info registers  

rax 0x0 0  

rbx 0x4bad080 79351936  

rcx 0x2f 47  

rdx 0x0 0  

rsi 0x6d00750063006f 30681274979123311  

rdi 0x4b9da40 79288896  

rbp 0x4bab800 0x4bab800  

rsp 0x7fffe7b60da8 0x7fffe7b60da8  

r8 0x4ba0880 79300736  

r9 0x4ba0940 79300928  

r10 0x4ba0920 79300896  

r11 0x206 518  

r12 0x1 1  

r13 0x4bab810 79345680  

r14 0x4bab810 79345680  

r15 0x10 16  

rip 0x7ffff1b0d42a 0x7ffff1b0d42a <\_\_strcmp\_sse2+26>  

eflags 0x10283 [ CF SF IF RF ]  

cs 0x33 51  

ss 0x2b 43  

ds 0x0 0  

es 0x0 0  

fs 0x0 0  

gs 0x0 0  

(gdb) disas $rip-32, $rip+32  

Dump of assembler code from 0x7ffff1b0d40a to 0x7ffff1b0d44a:  

0x00007ffff1b0d40a <strcmp+58>: add %al,%bl  

0x00007ffff1b0d40c: jmp 0x7ffff1b0d410 <\_\_strcmp\_sse2>  

0x00007ffff1b0d40e: nop  

0x00007ffff1b0d40f: nop  

0x00007ffff1b0d410 <\_\_strcmp\_sse2+0>: mov %esi,%ecx  

0x00007ffff1b0d412 <\_\_strcmp\_sse2+2>: mov %edi,%eax  

0x00007ffff1b0d414 <\_\_strcmp\_sse2+4>: and $0x3f,%rcx  

0x00007ffff1b0d418 <\_\_strcmp\_sse2+8>: and $0x3f,%rax  

0x00007ffff1b0d41c <\_\_strcmp\_sse2+12>: cmp $0x30,%ecx  

0x00007ffff1b0d41f <\_\_strcmp\_sse2+15>: ja 0x7ffff1b0d460 <\_\_strcmp\_sse2+80>  

0x00007ffff1b0d421 <\_\_strcmp\_sse2+17>: cmp $0x30,%eax  

0x00007ffff1b0d424 <\_\_strcmp\_sse2+20>: ja 0x7ffff1b0d460 <\_\_strcmp\_sse2+80>  

0x00007ffff1b0d426 <\_\_strcmp\_sse2+22>: movlpd (%rdi),%xmm1  

=> 0x00007ffff1b0d42a <\_\_strcmp\_sse2+26>: movlpd (%rsi),%xmm2  

0x00007ffff1b0d42e <\_\_strcmp\_sse2+30>: movhpd 0x8(%rdi),%xmm1  

0x00007ffff1b0d433 <\_\_strcmp\_sse2+35>: movhpd 0x8(%rsi),%xmm2  

0x00007ffff1b0d438 <\_\_strcmp\_sse2+40>: pxor %xmm0,%xmm0  

0x00007ffff1b0d43c <\_\_strcmp\_sse2+44>: pcmpeqb %xmm1,%xmm0  

0x00007ffff1b0d440 <\_\_strcmp\_sse2+48>: pcmpeqb %xmm2,%xmm1  

0x00007ffff1b0d444 <\_\_strcmp\_sse2+52>: psubb %xmm0,%xmm1  

0x00007ffff1b0d448 <\_\_strcmp\_sse2+56>: pmovmskb %xmm1,%edx  

End of assembler dump.  

(gdb) p $rsi  

$1 = 30681274979123311

The next one was:  

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0x7fffe7b62700 (LWP 26063)]  

0x0000000000b76464 in ?? ()  

(gdb) bt  

#0 0x0000000000b76464 in ?? ()  

#1 0x0000000000b7673d in ?? ()  

#2 0x00007fffdc494e9e in sqlite3\_free () from /usr/lib/libsqlite3.so.0  

#3 0x00007fffdc4c52fd in ?? () from /usr/lib/libsqlite3.so.0  

#4 0x00007fffdc4d200c in ?? () from /usr/lib/libsqlite3.so.0  

#5 0x00007fffdc4f1caa in sqlite3\_exec () from /usr/lib/libsqlite3.so.0  

#6 0x00007fffdc7428a3 in tableExists (sqlDB=0x4bf0408, tableName=<value optimized out>) at sdb.c:1657  

[...]

## Attachments

- [a.html](attachments/a.html) (application/octet-stream; charset=binary, 10.1 KB)
- [71586.txt](attachments/71586.txt) (text/plain; charset=us-ascii, 7.9 KB)
- [71586-sort.txt](attachments/71586-sort.txt) (text/x-c; charset=us-ascii, 6.0 KB)
- [71586-threads.txt](attachments/71586-threads.txt) (text/plain; charset=us-ascii, 23.3 KB)
- [b.html](attachments/b.html) (text/plain; charset=us-ascii, 67 B)
- [workaround.diff](attachments/workaround.diff) (text/x-diff; charset=us-ascii, 1.5 KB)

## Timeline

### ao...@gmail.com (2011-02-02)

A more symbolic trace using 11.0.657.0 (Developer Build 73427). This seems to be the most common place where the crash occurs.

### sc...@gmail.com (2011-02-02)

@aohelin: that's an interesting trace in https://crbug.com/chromium/71586#c1, because both of those strings being compared look valid to me. It leads one to suspect a data race condition. Could you provide the output for "info threads" at the time of the crash? If any thread looks like it is also doing something MIME related, please provide its backtrace.
Also, it'd be useful to see the actual faulting instruction (plus registers) inside strcmp() itself.

### sc...@gmail.com (2011-02-02)

Oh, I see the crashes are all over the shop... this may need valgrind :-/

### sc...@gmail.com (2011-02-02)

It would still be useful to sample what the other threads are doing at the exact time of the SIGSEGV. Whoever may have stomped memory won't have moved on very far, especially on a multi-core machine.

### ao...@gmail.com (2011-02-02)

Took a while to get it again to gdb. Loading symbols is a bit slow. I'll add the thread backtraces soon.

### ao...@gmail.com (2011-02-02)

Thread backtraces. This is in one of the other common crash sites. Thread 10 crashed, and 5 looks interesting.

(gdb) thread 5
[Switching to thread 5 (Thread 0x7fffe9478700 (LWP 26507))]#0  __strcmp_sse2 ()
    at ../sysdeps/x86_64/multiarch/../strcmp.S:107
107	in ../sysdeps/x86_64/multiarch/../strcmp.S
(gdb) info registers
rax            0x0	0
rbx            0x7fffe470eb00	140737025993472
rcx            0x0	0
rdx            0x100000000	4294967296
rsi            0x100000000	4294967296
rdi            0x7fffdff89b40	140736950999872
rbp            0x7fffe9476250	0x7fffe9476250
rsp            0x7fffe9476238	0x7fffe9476238
r8             0x7fffdff8cd80	140736951012736
r9             0x7fffdff8cd60	140736951012704
r10            0x7fffdff8cd40	140736951012672
r11            0x206	518
r12            0x1	1
r13            0x7fffdff99810	140736951064592
r14            0x7fffdff99810	140736951064592
r15            0x10	16
rip            0x7ffff0da142a	0x7ffff0da142a <__strcmp_sse2+26>
eflags         0x10283	[ CF SF IF RF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0
(gdb) thread 10
[Switching to thread 10 (Thread 0x7fffe6c73700 (LWP 26512))]#0  __strcmp_sse2
    () at ../sysdeps/x86_64/multiarch/../strcmp.S:106
106	in ../sysdeps/x86_64/multiarch/../strcmp.S
(gdb) info registers
rax            0x0	0
rbx            0x7fffdff94010	140736951042064
rcx            0x0	0
rdx            0x7fffdff8cf40	140736951013184
rsi            0x7fffdff8cf40	140736951013184
rdi            0x0	0
rbp            0x7fffe6c71170	0x7fffe6c71170
rsp            0x7fffe6c71158	0x7fffe6c71158
r8             0x30	48
r9             0x101010101010101	72340172838076673
r10            0x7fffdff8f2c0	140736951022272
r11            0x7ffff0da5756	140737234229078
r12            0x1	1
r13            0x7fffdff98010	140736951058448
r14            0x7fffdff98010	140736951058448
r15            0x10	16
rip            0x7ffff0da1426	0x7ffff0da1426 <__strcmp_sse2+22>
eflags         0x10283	[ CF SF IF RF ]
cs             0x33	51
ss             0x2b	43
ds             0x0	0
es             0x0	0
fs             0x0	0
gs             0x0	0


### ao...@gmail.com (2011-02-02)

Reduced testcase. Same effect and reproduction instructions. Some a's can probably be removed, but the dot seems to be required. Always a bit disappointing to see fun test data reduce to something like this :)

### js...@chromium.org (2011-02-02)

Hmm. Might be a race with the plugin process at startup?

### ao...@gmail.com (2011-02-02)

Mime strings and sorting would fit multiple threads having raced to populate a shared mime database at the same time, and breaking the browser process in the... process.

### sc...@gmail.com (2011-02-03)

Tom, you're a bit of a race wizard. Any chance you're interesting in looking at this bug?

### ao...@gmail.com (2011-02-03)

I just had a quick look here. Might be worth starting at base/third_party/xdg_mime/xdgmime.c. Many functions call xdg_mime_init to make sure the mime data is loaded, and the flag whether it needs to be loaded seems to be a non-protected global variable. It is set to FALSE after the data has been loaded, so there is plenty of time for two threads to race and start reading the data.

### sc...@gmail.com (2011-02-03)

Nice. I wonder which two threads? We only have one file IO thread, and IO tasks (such as loading the MIME db) are supposed to be strictly serialized on that thread. This design is what makes the Chrome UI so responsive.

Maybe a strategic sprinkling of DCHECK(BrowserThread::CurrentlyOn(BrowserThread::IO)); in a debug build would help?

### ao...@gmail.com (2011-02-03)

At least asserts checking if someone has changed need_reread after starting to read the data fire pretty often, as in "base/third_party/xdg_mime/xdgmime.c:467: xdg_mime_init: Assertion `need_reread == (!(0))' failed." I'll have another look at the thread issue with DCHECKs after work unless this has been resolved already. Seems to take a while for me to figure out who is doing what and sharing what with whom :)

### ao...@gmail.com (2011-02-03)

One of the threads seems to be handling a MimeRegistryMessageFilter::OnGetMimeTypeFromExtension, and does an xdg_mime_init() since it has not yet been loaded, and the other thread is doing a net::URLRequestFileJob and does xdg_mime_init() via URLRequestFileJob::GetMimeType. The latter usually seems to have finished loading mime data and has moved on, while the former usually crashes or aborts if the need_reread check is in place.

Different runs show a slightly different position, but this seems to be the common pattern. Adding a mutex or some other exclusion mechanism to mime reading would probably be enough to fix this.

### ao...@gmail.com (2011-02-04)

Crash does not seem to happen if a mutex is added around need_reread. This is just an ugly workaround though, as the whole xdg library is not thread-safe. Chrome itself should probably be checking that no two threads are in the air at the same time calling xdg code. I didn't check yet whether the other thread is bypassing the mime registry and causing the race that way, or if both go through a same point which could enforce single threaded access.

Not sure if this helps. I seem to have ended up spending a moment with morning coffee and evening tea searching for or looking at bugs :)

### js...@chromium.org (2011-02-04)

Given that this appears specific to startup and probably not web triggerable, I'm marking as low severity now.

@tsepez - Could you investigate and work out a fix when you get a chance?

### ts...@chromium.org (2011-02-07)

Adding the asserts as suggested in https://crbug.com/chromium/71586#c12 rapidly results in:


[9418:9424:332127091617:FATAL:mime_util_xdg.cc(554)] Check failed: BrowserThread::CurrentlyOn(BrowserThread::IO). 
Backtrace:
	base::debug::StackTrace::StackTrace() [0x126dd76]
	logging::LogMessage::~LogMessage() [0x1282a22]
	mime_util::GetFileMimeType() [0x129c6e0]
	net::PlatformMimeUtil::GetPlatformMimeTypeFromExtension() [0x181252b]
	net::MimeUtil::GetMimeTypeFromExtension() [0x17fa1d0]
	net::GetMimeTypeFromExtension() [0x17fb518]
	MimeRegistryMessageFilter::OnGetMimeTypeFromExtension() [0xfa3593]
	DispatchToMethod<>() [0xfa3d2d]
	IPC::MessageWithReply<>::Dispatch<>() [0xfa39d2]
	MimeRegistryMessageFilter::OnMessageReceived() [0xfa34c9]
	BrowserMessageFilter::DispatchMessage() [0xa48d3d]
	DispatchToMethod<>() [0xa494e1]
	RunnableMethod<>::Run() [0xa49300]
	MessageLoop::RunTask() [0x1285acc]
	MessageLoop::DeferOrRunPendingTask() [0x1285bba]
	MessageLoop::DoWork() [0x12864ec]
	base::MessagePumpLibevent::Run() [0x125ce5b]
	MessageLoop::RunInternal() [0x12858f0]
	MessageLoop::RunHandler() [0x128578c]
	MessageLoop::Run() [0x128514b]
	base::Thread::Run() [0x12cdb1e]
	base::Thread::ThreadMain() [0x12cdcd9]
	base::(anonymous namespace)::ThreadFunc() [0x12c8cc7]
	start_thread [0x7fc99c3989ca]
	0x7fc999a4570d

as expected.  Probably a layering violation to allow files in base/ to call into browser/ ...

### ts...@chromium.org (2011-02-07)

I take it back.  Looks like a small typo in https://crbug.com/chromium/71586#c12: IO vs. FILE.  Would seem to want to happen in the file thread via chrome/browser/mime_registry_message_filter.cc's 

void MimeRegistryMessageFilter::OverrideThreadForMessage(
    const IPC::Message& message,
    BrowserThread::ID* thread) {
  if (IPC_MESSAGE_CLASS(message) == MimeRegistryMsgStart)
    *thread = BrowserThread::FILE;
}

Changing the asserts to FILE and things are no longer asserting.  Time for more digging.

### [Deleted User] (2011-02-10)

To summarize aohelin's analysis:

- MimeRegistryMessageFilter forwards all messages on the FILE thread (https://crbug.com/chromium/71586#c18)
- URLRequestFileJob::GetMimeType lives on the IO thread (that's where URLRequests live)
- both call into xdg_mime_init via net::GetMimeTypeFromExtension.

It seems clear to me that this is bad.  A mutex solves it, but we usually don't like to block the IO thread on the FILE thread.  It'd be better to make the relevant calls async.

I think it's totally wrong that URLRequestFileJob is calling a blocking disk function from the IO thread anyway.  And looking at the code...

bool URLRequestFileJob::GetMimeType(std::string* mime_type) const {
  // URL requests should not block on the disk!  On Windows this goes to the
  // registry.
  //   http://code.google.com/p/chromium/issues/detail?id=59849
  base::ThreadRestrictions::ScopedAllowIO allow_io;
  DCHECK(request_);
  return GetMimeTypeFromFile(file_path_, mime_type);
}

FFFFFUUUUU

### [Deleted User] (2011-02-10)

Will and I discussed this in person.

We think:
1) Fix the race.  We should put a lock into base/mime_util_xdg.cc because the code it's calling (the xdg stuff) has tons of global state.  Having URLRequestFileJob::GetMimeType() block on a lock is the same amount of jank as the code currently has, so it's not such a bad thing to introduce it first.

2) Fix the jank.  This is a separate issue, and can be done as part of 59849.  I'll comment there with what needs to be done.

### [Deleted User] (2011-02-10)

[Comment Deleted]

### [Deleted User] (2011-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2011-02-10)

The dup'd issue is a ThreadSanitizer report showing that we have this race.  We shoulda caught this earlier.  :~(

### [Deleted User] (2011-02-11)

Adding Kostya who found the https://crbug.com/chromium/72042

### kc...@chromium.org (2011-02-11)

As we now have an easy reproducer (do we?), I'd suggest running it under ThreadSanitizer, before and after the fix. 

### js...@chromium.org (2011-02-16)

Bumping up the severity a bit because the other crash stacks make it look like a malicious extension could potentially use this for privilege escalation (although that may be a longshot).

### kc...@chromium.org (2011-03-20)

I start seeing this as a Memcheck report (in addition to ThreadSanitizer report in https://crbug.com/chromium/74042): 
Invalid write of size 8                                                                                                                                                                                                                                                                     
   at 0xD1365C: _xdg_mime_alias_read_from_file (base/third_party/xdg_mime/xdgmimealias.c:153)                                                                                                                                                                                               
   by 0xD12F9A: xdg_mime_init_from_directory (base/third_party/xdg_mime/xdgmime.c:201)                                                                                                                                                                                                      
   by 0xD12AED: xdg_run_command_on_dirs (base/third_party/xdg_mime/xdgmime.c:288)                                                                                                                                                                                                           
   by 0xD13405: xdg_mime_init (base/third_party/xdg_mime/xdgmime.c:456)                                                                                                                                                                                                                     
   by 0xD13490: xdg_mime_get_mime_type_from_file_name (base/third_party/xdg_mime/xdgmime.c:567)                                                                                                                                                                                             
   by 0xCDF4FD: mime_util::GetFileMimeType(FilePath const&) (base/mime_util_xdg.cc:556)                                                                                                                                                                                                     
   by 0x1098BCB: net::PlatformMimeUtil::GetPlatformMimeTypeFromExtension(std::string const&, std::string*) const (net/base/platform_mime_util_linux.cc:23)                                                                                                                                  
   by 0x1086975: net::MimeUtil::GetMimeTypeFromExtension(std::string const&, std::string*) const (net/base/mime_util.cc:171)                                                                                                                                                                
   by 0x1086A55: net::MimeUtil::GetMimeTypeFromFile(FilePath const&, std::string*) const (net/base/mime_util.cc:189)                                                                                                                                                                        
   by 0xFA6800: net::URLRequestFileJob::GetMimeType(std::string*) const (net/url_request/url_request_file_job.cc:283)                                                                                                                                                                       
   by 0xFB04C2: net::URLRequestJob::NotifyHeadersComplete() (net/url_request/url_request_job.cc:470)                                                                                                                                                                                        
   by 0xFA64E6: net::URLRequestFileJob::DidResolve(bool, base::PlatformFileInfo const&) (net/url_request/url_request_file_job.cc:373)                                                                                                                                                       
   by 0xCCE1B8: MessageLoop::RunTask(Task*) (base/message_loop.cc:367)                                                                                                                                                                                                                      
   by 0xCCEE17: MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const&) (base/message_loop.cc:376)                                                                                                                                                                              
   by 0xCCFB52: MessageLoop::DoWork() (base/message_loop.cc:569)                                                                                                                                                                                                                            
   by 0xCB03A8: base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) (base/message_pump_libevent.cc:222)                                                                                                                                                                            
   by 0xCD05CD: MessageLoop::RunInternal() (base/message_loop.cc:342)                                                                                                                                                                                                                       
   by 0xCD0769: MessageLoop::Run() (base/message_loop.cc:239)                                                                                                                                                                                                                               
   by 0xCFB5AB: base::Thread::ThreadMain() (base/threading/thread.cc:164)                                                                                                                                                                                                                   
   by 0xCFAAE9: base::(anonymous namespace)::ThreadFunc(void*) (base/threading/platform_thread_posix.cc:51)                                                                                                                                                                                 
 Address 0x540 is not stack'd, malloc'd or (recently) free'd                        

### js...@chromium.org (2011-03-21)

[Empty comment from Monorail migration]

### ts...@chromium.org (2011-03-30)

[Empty comment from Monorail migration]

### bu...@chromium.org (2011-03-30)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=79851

------------------------------------------------------------------------
r79851 | tsepez@chromium.org | Wed Mar 30 09:59:46 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/base/mime_util_xdg.cc?r1=79851&r2=79850&pathrev=79851

XDG isn't thread safe.  Add a lock around calls to it.

BUG=71586
Review URL: http://codereview.chromium.org/6708072
------------------------------------------------------------------------

### sc...@gmail.com (2011-03-31)

Merged to M11: 80097

### bu...@chromium.org (2011-03-31)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=80097

------------------------------------------------------------------------
r80097 | cevans@chromium.org | Thu Mar 31 16:20:07 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/branches/696/src/base/mime_util_xdg.cc?r1=80097&r2=80096&pathrev=80097

Merge 79851 - XDG isn't thread safe.  Add a lock around calls to it.

BUG=71586
Review URL: http://codereview.chromium.org/6708072

TBR=tsepez@chromium.org
Review URL: http://codereview.chromium.org/6758053
------------------------------------------------------------------------

### kc...@chromium.org (2011-04-14)

I am testing yet another dynamic tool for detecting memory crashers. 
The tool reports similar stacks on Chromium: r81383 / WebKit: r83605
And I do see a similar stack in crash on Chrome 12. 
http://crash/reportdetail?reportid=e70f9fc500b5a7e1

So, is this really fixed? 

  #0 0x0110b2e3  << _xdg_mime_cache_new_from_file  base/third_party/xdg_mime/xdgmimecache.c:156                                                                                                     
  #1 0x01104bd8  << xdg_mime_init_from_directory  base/third_party/xdg_mime/xdgmime.c:148                                                                                                           
  #2 0x011045c5  << xdg_run_command_on_dirs  base/third_party/xdg_mime/xdgmime.c:250                                                                                                                
  #3 0x011062bd  << xdg_mime_init  base/third_party/xdg_mime/xdgmime.c:456                                                                                                                          
  #4 0x01106900  << xdg_mime_get_mime_type_from_file_name  base/third_party/xdg_mime/xdgmime.c:567                                                                                                  
  #5 0x0109525a  << mime_util::GetFileMimeType(FilePath const0x109525a )  /usr/lib/llvm/gcc-4.2/lib/gcc/x86_64-linux-gnu/4.2.1/../../../../include/c++/4.2.1/bits/stl_tree.h:184                    
  #6 0x01973815  << net::PlatformMimeUtil::GetPlatformMimeTypeFromExtension(std::string const0x1973815 , std::string*) const  net/base/platform_mime_util_linux.cc:23                               
  #7 0x0194a1ba  << net::MimeUtil::GetMimeTypeFromExtension(std::string const0x194a1ba , std::string*) const  /usr/lib/llvm/gcc-4.2/lib/gcc/x86_64-linux-gnu/4.2.1/../../../../include/c++/4.2.1/bi»
  #8 0x0194c318  << net::MimeUtil::GetMimeTypeFromFile(FilePath const0x194c318 , std::string*) const  /usr/lib/llvm/gcc-4.2/lib/gcc/x86_64-linux-gnu/4.2.1/../../../../include/c++/4.2.1/bits/stl_v»
  #9 0x0194c367  << net::GetMimeTypeFromFile(FilePath const0x194c367 , std::string*)  /usr/lib/llvm/gcc-4.2/lib/gcc/x86_64-linux-gnu/4.2.1/../../../../include/c++/4.2.1/bits/stl_vector.h:536      
  #10 0x017a25c8  << net::URLRequestFileJob::GetMimeType(std::string*) const  ./base/memory/weak_ptr.h:66                                                                                           
  #11 0x0179adc8  << net::URLRequest::GetMimeType(std::string*)  ./base/memory/ref_counted.h:95                                                                                                     
  #12 0x03f24e8c  << ResourceDispatcherHost::CompleteResponseStarted(net::URLRequest*)  ./base/memory/ref_counted.h:143                                                                             
  #13 0x03f25033  << ResourceDispatcherHost::CompleteResponseStarted(net::URLRequest*)  ./base/memory/ref_counted.h:143                                                                             
  #14 0x03f276b9  << ResourceDispatcherHost::CancelRequestsForRoute(int, int)  ./base/memory/ref_counted.h:143                                                                                      
  #15 0x0179c3a3  << net::URLRequest::ResponseStarted()  ./base/memory/ref_counted.h:95                                                                                                             
  #16 0x017acc14  << net::URLRequestJob::NotifyHeadersComplete()  ./base/memory/ref_counted.h:241                                                                                                   
  #17 0x017a2061  << net::URLRequestFileJob::DidResolve(bool, base::PlatformFileInfo const0x17a2061 )  ./base/memory/weak_ptr.h:66                                                                  
  #18 0x01071226  << MessageLoop::RunTask(Task*)  ./base/synchronization/lock.h:104                                                                                                                 
  #19 0x01071610  << MessageLoop::DeferOrRunPendingTask(MessageLoop::PendingTask const0x1071610 )  ./base/synchronization/lock.h:104                                                                
  #20 0x0107242a  << MessageLoop::DoWork()  ./base/synchronization/lock.h:104                                                                                                                       
  #21 0x0103bcb7  << base::MessagePumpLibevent::Run(base::MessagePump::Delegate*)  /usr/lib/llvm/gcc-4.2/lib/gcc/x86_64-linux-gnu/4.2.1/../../../../include/c++/4.2.1/bits/stl_algobase.h:189       
  #22 0x01072aef  << MessageLoop::RunInternal()  ./base/synchronization/lock.h:104                                                                                                                  
  #23 0x01072ca4  << MessageLoop::Run()  ./base/synchronization/lock.h:104                                                                                                                          
  #24 0x010cf797  << base::Thread::ThreadMain()  ./base/threading/platform_thread.h:57                                                                                                              
  #25 0x010cf368  << base::(anonymous namespace)::ThreadFunc(void*)  base/threading/platform_thread_posix.cc:51    

### sc...@gmail.com (2011-04-14)

The version of Chrome of referenced in http://crash/reportdetail?reportid=e70f9fc500b5a7e1 is 12.0.712.0, which is r79102 and therefore does not contain Tom's fix.

Could you go in to more detail on what your new dynamic tool is reporting, exactly? It's hard to tell from just a stack trace.

### sc...@gmail.com (2011-04-14)

Compare https://crash/search?query=product%3A%22Chrome_Linux%22+version%3A%2212.0.712.0%22+MimeUtil
(noisy)
vs.
https://crash/search?query=product%3A%22Chrome_Linux%22+version%3A%2212.0.725.0%22+MimeUtil

Pretty clean :)

### kc...@chromium.org (2011-04-14)

The new tool tells me that the memory accessed in _xdg_mime_cache_new_from_file has been freed long ago. 
So long ago, that the tool lost track of where it has been free-ed. 
Could be a false positive of course, the tool is just a few days old. :) 
I am rerunning with different settings (larger free-delay buffer and red zones)... 
Let me update this bug once I have a better report.



### sc...@gmail.com (2011-04-14)

@aohelin: we're happy to be without this race, it was also causing stability issues. Accordingly, please have a $500 Chromium Security Reward :)

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

### ao...@gmail.com (2011-04-15)

Excellent, thanks :)

### sc...@gmail.com (2011-04-22)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-05-04)

Invoice finalized; payment is in e-payment system; it can take a couple of weeks.

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

### bu...@chromium.org (2013-03-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### gl...@chromium.org (2014-03-25)

[Empty comment from Monorail migration]

### gl...@chromium.org (2014-04-01)

[Empty comment from Monorail migration]

### as...@chromium.org (2014-06-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/71586?no_tracker_redirect=1

[Multiple monorail components: Blink, Internals, Internals>Plugins]
[Monorail mergedwith: crbug.com/chromium/72042]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40087467)*
