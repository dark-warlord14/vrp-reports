# Load Timer fired on deleted HTMLMediaElement

| Field | Value |
|-------|-------|
| **Issue ID** | [40083165](https://issues.chromium.org/issues/40083165) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ku...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2010-09-13 |
| **Bounty** | $1,000.00 |

## Description

test 7.0.517.0 dev
testcase.htm
===============
<body onload="document.getElementById('crash').innerHTML=1">
<map id="crash">
<video src="AAA">
</body>

When trying to reproduce the testcase if got a full tab crash here is logout 
forget catch the dmp :S


## Timeline

### ku...@gmail.com (2010-09-13)

(988.c4): Access violation - code c0000005 (!!! second chance !!!)
eax=04a20004 ebx=00004000 ecx=00000001 edx=00000000 esi=04a20000 edi=04149000
eip=027bd778 esp=01c1fc68 ebp=01c1fc70 iopl=0         nv up ei ng nz ac pe cy
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000297
chrome_1c30000!UnwindUpVec+0x50:
027bd778 8b448efc        mov     eax,dword ptr [esi+ecx*4-4] ds:0023:04a20000=????????
Missing image name, possible paged-out or corrupt data.
Missing image name, possible paged-out or corrupt data.
Missing image name, possible paged-out or corrupt data.
0:010> .exr -1
ExceptionAddress: 027bd778 (chrome_1c30000!UnwindUpVec+0x00000050)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000000
   Parameter[1]: 04a20000
Attempt to read from address 04a20000
0:010> kP
ChildEBP RetAddr  
01c1fc70 027bcac2 chrome_1c30000!UnwindUpVec+0x50 [f:\dd\vctools\crt_bld\SELF_X86\crt\src\Intel\MEMCPY.ASM @ 322]
01c1fc8c 01c40d5b chrome_1c30000!memmove_s(
			void * dst = 0x04149000, 
			unsigned int sizeInBytes = 4, 
			void * src = 0x04a20000, 
			unsigned int count = 4)+0x54 [f:\dd\vctools\crt_bld\self_x86\crt\src\memmove_s.c @ 58]
01c1fca4 01df568c chrome_1c30000!std::vector<char,std::allocator<char> >::_Ucopy<char *>(
			char * _First = 0x01df55c2 "]???", 
			char * _Last = 0x04a20004 "--- memory read error at address 0x04a20004 ---", 
			char * _Ptr = 0x00000001 "--- memory read error at address 0x00000001 ---")+0x16 [c:\program files (x86)\microsoft visual studio 9.0\vc\include\vector @ 1141]
01c1fcbc 01df55c2 chrome_1c30000!std::vector<char,std::allocator<char> >::_Insert<char *>(
			class std::_Vector_const_iterator<char,std::allocator<char> > _Where = class std::_Vector_const_iterator<char,std::allocator<char> >, 

### ku...@gmail.com (2010-09-13)

			char * _First = 0x04a20000 "--- memory read error at address 0x04a20000 ---", 
			char * _Last = 0x04a20004 "--- memory read error at address 0x04a20004 ---", 
			struct std::forward_iterator_tag __formal = struct std::forward_iterator_tag)+0xc6 [c:\program files (x86)\microsoft visual studio 9.0\vc\include\vector @ 983]
01c1fcd8 0249dee7 chrome_1c30000!std::vector<char,std::allocator<char> >::insert<char *>(
			class std::_Vector_const_iterator<char,std::allocator<char> > _Where = class std::_Vector_const_iterator<char,std::allocator<char> >, 
			char * _First = 0x04a20000 "--- memory read error at address 0x04a20000 ---", 
			char * _Last = 0x04a20004 "--- memory read error at address 0x04a20004 ---")+0x17 [c:\program files (x86)\microsoft visual studio 9.0\vc\include\vector @ 890]
01c1fd08 0249eada chrome_1c30000!disk_cache::EntryImpl::UserBuffer::Write(
			int offset = 1, 
			class net::IOBuffer * buf = 0x00000000, 
			int len = 4)+0xa0 [d:\b\slave\chrome-official\build\src\net\disk_cache\entry_impl.cc @ 199]
01c1fd44 024a6719 chrome_1c30000!disk_cache::EntryImpl::WriteDataImpl(
			int index = 1, 
			int offset = 0, 
			class net::IOBuffer * buf = 0x04969f50, 
			int buf_len = 4, 
			class CallbackRunner<Tuple1<int> > * callback = 0x040fff20, 
			bool truncate = false)+0x10f [d:\b\slave\chrome-official\build\src\net\disk_cache\entry_impl.cc @ 595]
01c1fd7c 024a6482 chrome_1c30000!disk_cache::BackendIO::ExecuteEntryOperation(void)+0x149 [d:\b\slave\chrome-official\build\src\net\disk_cache\in_flight_backend_io.cc @ 236]
01c1fd90 01cf285a chrome_1c30000!disk_cache::BackendIO::ExecuteOperation(void)+0x14 [d:\b\slave\chrome-official\build\src\net\disk_cache\in_flight_backend_io.cc @ 26]
01c1fdc0 01cf28e6 chrome_1c30000!MessageLoop::RunTask(
			class Task * task = 0x04104760)+0x97 [d:\b\slave\chrome-official\build\src\base\message_loop.cc @ 409]
01c1fdd0 01cf2a7c chrome_1c30000!MessageLoop::DeferOrRunPendingTask(
			struct MessageLoop::PendingTask * pending_task = 0x04a20004)+0x28 [d:\b\slave\chrome-official\build\src\base\message_loop.cc @ 420]
01c1fe00 01d06c68 chrome_1c30000!MessageLoop::DoWork(void)+0x71 [d:\b\slave\chrome-official\build\src\base\message_loop.cc @ 524]
01c1fe14 01d0673f chrome_1c30000!base::MessagePumpForIO::DoRunLoop(void)+0x6f [d:\b\slave\chrome-official\build\src\base\message_pump_win.cc @ 465]
01c1fe30 01d0657c chrome_1c30000!base::MessagePumpWin::RunWithDispatcher(
			class base::MessagePump::Delegate * delegate = 0x04a20004, 
			class base::MessagePumpWin::Dispatcher * dispatcher = 0x00000000)+0x38 [d:\b\slave\chrome-official\build\src\base\message_pump_win.cc @ 53]
01c1fe3c 01cf2609 chrome_1c30000!base::MessagePumpWin::Run(
			class base::MessagePump::Delegate * delegate = 0x025bae82)+0xe [d:\b\slave\chrome-official\build\src\base\message_pump_win.h @ 80]
01c1fe48 01cf258e chrome_1c30000!MessageLoop::RunInternal(void)+0x31 [d:\b\slave\chrome-official\build\src\base\message_loop.cc @ 257]

### ku...@gmail.com (2010-09-13)


01c1fe50 01cf253c chrome_1c30000!MessageLoop::RunHandler(void)+0x17 [d:\b\slave\chrome-official\build\src\base\message_loop.cc @ 228]
01c1fe70 025bae82 chrome_1c30000!MessageLoop::Run(void)+0x15 [d:\b\slave\chrome-official\build\src\base\message_loop.cc @ 207]
01c1fe74 025baf28 chrome_1c30000!base::Thread::Run(
			class MessageLoop * message_loop = 0x01cfad51)+0x9 [d:\b\slave\chrome-official\build\src\base\thread.cc @ 141]
01c1ffb0 01cfad51 chrome_1c30000!base::Thread::ThreadMain(void)+0xa3 [d:\b\slave\chrome-official\build\src\base\thread.cc @ 167]


### ku...@gmail.com (2010-09-13)

fulltab crash only come out once

### [Deleted User] (2010-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2010-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2010-09-14)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-09-14)

[Empty comment from Monorail migration]

### in...@chromium.org (2010-09-14)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-09-14)

I just had a chance to look at this. It does seem to be a stale pointer on trunk. The HTMLMediaElement seems to have been deleted before its timer fired.

### in...@chromium.org (2010-09-14)

Filed Webkit Bug - https://bugs.webkit.org/show_bug.cgi?id=45765

### la...@chromium.org (2010-09-20)

This seems like something we can patch into a beta release, as opposed to being a blocker... 

Since the issue doesn't appear to be actively worked on I'm removing it's beta blocking status.

### js...@chromium.org (2010-09-30)

Just an update. I have a fix that makes the load event delay asynchronous (which is how the spec is written). Unfortunately it also breaks two of the layout tests for media loading. So, I'll need a chance to look at both the standard and the tests and see what's wrong and what needs to change.

### in...@chromium.org (2010-10-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2010-10-04)

Landed upstream at: http://trac.webkit.org/changeset/69043

Need to merge to 517.

### sc...@gmail.com (2010-10-05)

@kuzzcc: congratulations! We'd like to provisionally reward this at the $1000 level, thanks to the simple, clear test case and inclusion of useful exception record.

### ku...@gmail.com (2010-10-11)

Thanks for the reward.

### in...@chromium.org (2010-10-11)

Merged to 517 in r69499.

### sc...@gmail.com (2010-11-12)

Payment is in electronic system.

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-22)

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

This issue was migrated from crbug.com/chromium/55346?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083165)*
